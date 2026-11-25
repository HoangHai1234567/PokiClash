// Máy quả (lều Hội Máy Quả, GD_Claude/29_DaoCasino.md mục 6.7): 3 cuộn × 3 hàng, 5 đường (giữa, trên, dưới, chéo xuống, chéo lên).
// Biểu tượng: 0..4 ngọc hệ (thứ tự Elements.All), 5 bi, 6 huy hiệu tướng khách mời, 7 Sao (thay mọi biểu tượng trừ Rương), 8 Rương.
// - Mỗi cuộn dừng ở một ô ngẫu nhiên đều của dải cuộn (strip) và hiện 3 ô liền nhau: hình trên cuộn là đúng phân bố thật, KHÔNG xếp
//   biểu tượng lớn sát đường thắng (không suýt trúng giả).
// - Đường: ba cùng biểu tượng (Sao thay được) trả pays × cược mỗi đường (cược mỗi đường = tổng cược / 5); ba Sao trả wildPays.
//   Ba huy hiệu trên một đường: thêm mảnh khách mời theo bậc cược (badgeShards).
// - Rương ở đâu cũng được: 2 cái trả scatter2 × tổng cược; 3 cái trở lên: freeSpins lượt miễn phí cùng mức cược (trúng lại được cộng thêm).
// - Exact(): hoàn trả chính xác tính trên mọi tổ hợp dừng (test, bảng tỉ lệ).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class SlotSpin
    {
        public int[] stops = new int[3];
        public int[,] grid = new int[3, 3]; // [cuộn, hàng]
        public List<(int line, int sym, int pays)> lines = new List<(int, int, int)>();
        public int chests;
        public int payout; // bi trả về (không gồm lượt miễn phí)
        public int badgeLines;
        public bool free; // lượt này là lượt miễn phí
        public int freeWon; // số lượt miễn phí vừa trúng
    }

    public sealed class SlotRound
    {
        public int bet, tier;
        public List<SlotSpin> spins = new List<SlotSpin>(); // lượt chính rồi các lượt miễn phí
        public int Payout => spins.Sum(x => x.payout);
        public int BadgeLines => spins.Sum(x => x.badgeLines);
    }

    public static class Slots
    {
        public const int Wild = 7, Chest = 8, Badge = 6, BallSym = 5, Lines = 5, MaxFree = 50;
        public static readonly int[][] LineRows = { new[] { 1, 1, 1 }, new[] { 0, 0, 0 }, new[] { 2, 2, 2 }, new[] { 0, 1, 2 }, new[] { 2, 1, 0 } };

        public static int Sym(SlotReel r, int stop, int row)
        {
            int n = r.strip.Length;
            return r.strip[((stop - 1 + row) % n + n) % n];
        }

        // trả của một đường (× cược mỗi đường) và biểu tượng thắng (−1 nếu không)
        public static int LinePays(SlotsConfig c, int a, int b, int d, out int sym)
        {
            sym = -1;
            if (a == Chest || b == Chest || d == Chest) return 0;
            if (a == Wild && b == Wild && d == Wild)
            {
                sym = Wild;
                return c.wildPays;
            }
            int bs = a != Wild ? a : b != Wild ? b : d;
            if ((a == bs || a == Wild) && (b == bs || b == Wild) && (d == bs || d == Wild))
            {
                var p = c.pays.Find(x => x.sym == bs);
                if (p == null || p.pays <= 0) return 0;
                sym = bs;
                return p.pays;
            }
            return 0;
        }

        // một lượt quay ở các ô dừng stops; bet là tổng cược
        public static SlotSpin Eval(SlotsConfig c, int[] stops, int bet)
        {
            var sp = new SlotSpin { stops = (int[])stops.Clone() };
            for (int r = 0; r < 3; r++)
                for (int row = 0; row < 3; row++)
                {
                    int x = Sym(c.reels[r], stops[r], row);
                    sp.grid[r, row] = x;
                    if (x == Chest) sp.chests++;
                }
            double lineBet = bet / (double)Lines;
            double pay = 0;
            for (int l = 0; l < LineRows.Length; l++)
            {
                var rows = LineRows[l];
                int p = LinePays(c, sp.grid[0, rows[0]], sp.grid[1, rows[1]], sp.grid[2, rows[2]], out int sym);
                if (p <= 0) continue;
                sp.lines.Add((l, sym, p));
                pay += p * lineBet;
                if (sym == Badge) sp.badgeLines++;
            }
            if (sp.chests == 2) pay += c.scatter2 * bet;
            if (sp.chests >= 3) sp.freeWon = c.freeSpins;
            sp.payout = (int)Math.Floor(pay + 1e-9);
            return sp;
        }

        public static SlotSpin Spin(SlotsConfig c, int bet, Rng rng)
        {
            var stops = new int[3];
            for (int r = 0; r < 3; r++) stops[r] = rng.Int(0, c.reels[r].strip.Length - 1);
            return Eval(c, stops, bet);
        }

        // lượt chính và mọi lượt miễn phí nó kéo theo
        public static SlotRound Round(SlotsConfig c, int bet, int tier, Rng rng)
        {
            var round = new SlotRound { bet = bet, tier = tier };
            var first = Spin(c, bet, rng);
            round.spins.Add(first);
            int left = first.freeWon, done = 0;
            while (left > 0 && done < MaxFree)
            {
                var sp = Spin(c, bet, rng);
                sp.free = true;
                round.spins.Add(sp);
                left += sp.freeWon - 1;
                done++;
            }
            return round;
        }

        // hoàn trả chính xác (phần bi, gồm lượt miễn phí trúng lại), tỉ lệ trúng (có trả hoặc có lượt miễn phí), xác suất ra lượt miễn phí,
        // số đường huy hiệu trung bình mỗi lượt
        public static (double rtp, double hit, double freeP, double badge) Exact(SlotsConfig c)
        {
            int n0 = c.reels[0].strip.Length, n1 = c.reels[1].strip.Length, n2 = c.reels[2].strip.Length;
            const int bet = 5 * 1000; // để chia đường không làm tròn
            double sum = 0, hits = 0, free = 0, badge = 0, n = 0;
            var stops = new int[3];
            for (int i = 0; i < n0; i++)
                for (int j = 0; j < n1; j++)
                    for (int k = 0; k < n2; k++)
                    {
                        stops[0] = i;
                        stops[1] = j;
                        stops[2] = k;
                        var sp = Eval(c, stops, bet);
                        sum += sp.payout;
                        if (sp.payout > 0 || sp.freeWon > 0) hits++;
                        if (sp.freeWon > 0) free++;
                        badge += sp.badgeLines;
                        n++;
                    }
            double b = sum / n / bet, p = free / n;
            double rtp = b / Math.Max(1e-9, 1 - c.freeSpins * p);
            return (rtp, hits / n, p, badge / n);
        }

        // ---------- trên bản lưu ----------

        public static string Check(SaveData s, GameData d, int tier, double now)
        {
            var c = Casino.C(d).slots;
            if (!Casino.BoothOpen(s, d, Casino.Slot, now)) return Loc.T("Lều Máy Quả chưa mở");
            if (!Casino.BetOpen(s, c, tier)) return Loc.F("Mở ở cấp {0}", Casino.BetLevel(c, tier));
            if (Casino.PlaysLeft(s, d, Casino.Slot, now) <= 0) return Loc.T("Hết lượt hôm nay");
            if (s.balls < Casino.Bet(s, d, c, tier)) return Loc.T("Không đủ bi");
            return null;
        }

        // quay có cược: trả cược, quay (gồm lượt miễn phí), trả thắng, mảnh huy hiệu, đổ hũ
        public static SlotRound Play(SaveData s, GameData d, int tier, double now, Rng rng, out JarResult jar, out List<Reward> extra, out string why)
        {
            jar = new JarResult();
            extra = new List<Reward>();
            why = Check(s, d, tier, now);
            if (why != null) return null;
            var c = Casino.C(d).slots;
            int bet = Casino.Bet(s, d, c, tier);
            if (!Casino.Stake(s, d, bet, now)) { why = Loc.T("Không đủ bi"); return null; }
            Casino.UsePlay(s, d, Casino.Slot, now);
            Casino.Track(s, d, "table", 1, now);
            var round = Round(c, bet, tier, rng);
            Casino.Win(s, d, round.Payout, now);
            int shards = tier < c.badgeShards.Length ? c.badgeShards[tier] * round.BadgeLines : 0;
            if (shards > 0)
                extra = Casino.Grant(s, d, new List<CasinoItem> { new CasinoItem { k = "shards", n = shards, h = "*guest" } }, now, rng,
                    Casino.GuestOf(d, Casino.Slot, now));
            jar = Casino.Pour(s, d, Casino.Slot, tier, bet, now, rng);
            return round;
        }
    }
}
