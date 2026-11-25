// Roulette (lều Vòng Xoay Ngũ Hành, GD_Claude/29_DaoCasino.md mục 6.7): bánh xe 26 ô = 5 hệ × số 1–5 (ô i: hệ Elements.All[i / 5],
// số i % 5 + 1) cộng ô Sao Vàng (25). Cửa: Hệ (5 ô, trả 4:1), Số (5 ô, 4:1), Ô đơn (24:1), Sao Vàng (24:1, cược từ bậc starTier được thêm
// mảnh khách mời). Mọi cửa hoàn trả 25/26 ≈ 96,2%. Tối đa `chips` chip mỗi vòng, mỗi chip một mức cược của bậc đang chọn.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum RlKind { Elem, Num, Single, Star }

    public sealed class RlBet
    {
        public RlKind kind;
        public int v; // Elem: chỉ số hệ (thứ tự Elements.All); Num: 1..5; Single: ô 0..24; Star: bỏ qua
        public int amount;
    }

    public sealed class RlSpin
    {
        public int pocket; // 0..25
        public int payout; // tổng bi trả lại (gồm cả cược thắng)
        public int staked;
        public int starShards; // mảnh khách mời (Sao Vàng)
        public List<int> wins = new List<int>(); // chỉ số cược thắng
    }

    public static class Roulette
    {
        public const int Pockets = 26, StarPocket = 25;

        public static Elem ElemOf(int pocket) => Elements.All[pocket / 5];
        public static int NumOf(int pocket) => pocket % 5 + 1;

        public static bool Hits(RlBet b, int pocket)
        {
            if (pocket == StarPocket) return b.kind == RlKind.Star;
            switch (b.kind)
            {
                case RlKind.Elem: return pocket / 5 == b.v;
                case RlKind.Num: return NumOf(pocket) == b.v;
                case RlKind.Single: return pocket == b.v;
                default: return false;
            }
        }

        public static int Pays(RouletteConfig c, RlKind k) =>
            k == RlKind.Elem ? c.elemPays : k == RlKind.Num ? c.numPays : k == RlKind.Single ? c.singlePays : c.starPays;

        // số ô thắng của cửa (để hiện tỉ lệ)
        public static int Cover(RlKind k) => k == RlKind.Elem || k == RlKind.Num ? 5 : 1;

        public static double Rtp(RouletteConfig c, RlKind k) => Cover(k) * (Pays(c, k) + 1) / (double)Pockets;

        public static RlSpin Spin(RouletteConfig c, IList<RlBet> bets, int tier, Rng rng)
        {
            var r = new RlSpin { pocket = rng.Int(0, Pockets - 1), staked = bets.Sum(b => b.amount) };
            for (int i = 0; i < bets.Count; i++)
            {
                var b = bets[i];
                if (!Hits(b, r.pocket)) continue;
                r.wins.Add(i);
                r.payout += b.amount * (Pays(c, b.kind) + 1);
                if (b.kind == RlKind.Star && tier >= c.starTier) r.starShards = Math.Max(r.starShards, c.starShards);
            }
            return r;
        }

        // ---------- trên bản lưu ----------

        public static string Check(SaveData s, GameData d, IList<RlBet> bets, int tier, double now)
        {
            var c = Casino.C(d).roulette;
            if (!Casino.BoothOpen(s, d, Casino.Roulette, now)) return Loc.T("Lều Vòng Xoay chưa mở");
            if (!Casino.BetOpen(s, c, tier)) return Loc.F("Mở ở cấp {0}", Casino.BetLevel(c, tier));
            if (bets.Count == 0) return Loc.T("Đặt ít nhất một chip");
            if (bets.Count > c.chips) return Loc.F("Tối đa {0} chip mỗi vòng", c.chips);
            if (Casino.PlaysLeft(s, d, Casino.Roulette, now) <= 0) return Loc.T("Hết vòng hôm nay");
            if (s.balls < bets.Sum(b => b.amount)) return Loc.T("Không đủ bi");
            return null;
        }

        // quay có cược: trả cược, quay, trả thắng, mảnh Sao Vàng, đổ hũ; null nếu không quay được (why)
        public static RlSpin Play(SaveData s, GameData d, IList<RlBet> bets, int tier, double now, Rng rng, out JarResult jar, out List<Reward> extra, out string why)
        {
            jar = new JarResult();
            extra = new List<Reward>();
            why = Check(s, d, bets, tier, now);
            if (why != null) return null;
            var c = Casino.C(d).roulette;
            int bet = Casino.Bet(s, d, c, tier);
            foreach (var b in bets) b.amount = bet;
            int total = bets.Sum(b => b.amount);
            if (!Casino.Stake(s, d, total, now)) { why = Loc.T("Không đủ bi"); return null; }
            Casino.UsePlay(s, d, Casino.Roulette, now);
            Casino.Track(s, d, "table", 1, now);
            var r = Spin(c, bets, tier, rng);
            Casino.Win(s, d, r.payout, now);
            if (r.starShards > 0)
                extra = Casino.Grant(s, d, new List<CasinoItem> { new CasinoItem { k = "shards", n = r.starShards, h = "*guest" } }, now, rng,
                    Casino.GuestOf(d, Casino.Roulette, now));
            jar = Casino.Pour(s, d, Casino.Roulette, tier, total, now, rng);
            return r;
        }
    }
}
