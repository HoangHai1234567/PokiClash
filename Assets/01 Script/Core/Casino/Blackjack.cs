// Blackjack (lều Đêm Bài, GD_Claude/29_DaoCasino.md mục 6.6). Luật quen thuộc:
// - hộp bài vô hạn (mỗi lá rút độc lập: hạng 1..13, chất là 4 trong 5 hệ, chỉ để vẽ), không đếm bài được;
// - dealer nhìn trộm khi lá ngửa là A hoặc 10: có blackjack thì ván kết thúc ngay (người chơi chỉ mất cược gốc, blackjack của mình thì hoà);
// - dealer dừng ở 17 mềm; blackjack trả bjPays (3:2), thắng 1:1, hoà trả lại;
// - gấp đôi với hai lá bất kỳ (cả sau khi tách); tách một lần (2 tay); tách A thì mỗi tay nhận 1 lá rồi dừng; 21 sau khi tách không là blackjack;
// - không bảo hiểm, không đầu hàng.
// Advice: chiến thuật cơ bản cho luật này (gợi ý người mới, máy tự chơi đo hoàn trả).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public struct BjCard
    {
        public int rank; // 1 = A, 11..13 = J Q K
        public int suit; // 0..3 → hệ Kim, Mộc, Thủy, Hỏa (hình)
        public int Value => rank >= 10 ? 10 : rank;
    }

    public enum BjAct { Hit, Stand, Double, Split }

    public enum BjPhase { Player, Done }

    public sealed class BjHand
    {
        public List<BjCard> cards = new List<BjCard>();
        public int bet;
        public bool doubled, split, standing;

        public int Total => Blackjack.Total(cards, out _);
        public bool Soft { get { Blackjack.Total(cards, out bool soft); return soft; } }
        public bool Bust => Total > 21;
        public bool Natural => !split && cards.Count == 2 && Total == 21;
        public bool SplitAces => split && cards.Count > 0 && cards[0].rank == 1;
        public bool Finished => standing || Bust || doubled || Total == 21 || (SplitAces && cards.Count >= 2);
    }

    public sealed class BjGame
    {
        public int baseBet;
        public List<BjHand> hands = new List<BjHand>();
        public List<BjCard> dealer = new List<BjCard>();
        public int active; // tay đang chơi
        public BjPhase phase;
        public bool dealerPeekBj; // dealer có blackjack lúc nhìn trộm
        public int payout; // tổng bi trả lại (gồm cả cược) khi xong
        public int[] results = new int[0]; // từng tay: 2 blackjack, 1 thắng, 0 hoà, −1 thua
        public Rng rng;

        public BjHand Hand => active < hands.Count ? hands[active] : null;
        public int Staked => hands.Sum(h => h.bet);
        public BjCard Up => dealer[0];
    }

    public static class Blackjack
    {
        public static BjCard Draw(Rng rng) => new BjCard { rank = rng.Int(1, 13), suit = rng.Int(0, 3) };

        public static int Total(List<BjCard> cards, out bool soft)
        {
            int t = 0, aces = 0;
            foreach (var c in cards)
            {
                t += c.Value;
                if (c.rank == 1) aces++;
            }
            soft = false;
            if (aces > 0 && t + 10 <= 21)
            {
                t += 10;
                soft = true;
            }
            return t;
        }

        // chia ván mới; nếu dealer hoặc người chơi có blackjack thì ván xong ngay
        public static BjGame Deal(int bet, Rng rng, BlackjackConfig c)
        {
            var g = new BjGame { baseBet = bet, rng = rng };
            var h = new BjHand { bet = bet };
            g.hands.Add(h);
            h.cards.Add(Draw(rng));
            g.dealer.Add(Draw(rng));
            h.cards.Add(Draw(rng));
            g.dealer.Add(Draw(rng));
            bool peek = g.Up.rank == 1 || g.Up.Value == 10;
            if (peek && Total(g.dealer, out _) == 21)
            {
                g.dealerPeekBj = true;
                Settle(g, c);
                return g;
            }
            if (h.Natural)
            {
                Settle(g, c);
                return g;
            }
            g.phase = BjPhase.Player;
            return g;
        }

        public static bool Can(BjGame g, BjAct a)
        {
            var h = g.Hand;
            if (g.phase != BjPhase.Player || h == null || h.Finished) return false;
            switch (a)
            {
                case BjAct.Hit:
                case BjAct.Stand: return true;
                case BjAct.Double: return h.cards.Count == 2;
                case BjAct.Split: return g.hands.Count == 1 && h.cards.Count == 2 && h.cards[0].Value == h.cards[1].Value;
                default: return false;
            }
        }

        // thao tác của người chơi; gấp đôi / tách cần thêm bi (bằng cược gốc) mà người gọi đã trả trước
        public static void Act(BjGame g, BjAct a, BlackjackConfig c)
        {
            if (!Can(g, a)) return;
            var h = g.Hand;
            switch (a)
            {
                case BjAct.Hit:
                    h.cards.Add(Draw(g.rng));
                    break;
                case BjAct.Stand:
                    h.standing = true;
                    break;
                case BjAct.Double:
                    h.bet *= 2;
                    h.doubled = true;
                    h.cards.Add(Draw(g.rng));
                    break;
                case BjAct.Split:
                    var h2 = new BjHand { bet = h.bet, split = true };
                    h.split = true;
                    h2.cards.Add(h.cards[1]);
                    h.cards.RemoveAt(1);
                    h.cards.Add(Draw(g.rng));
                    h2.cards.Add(Draw(g.rng));
                    g.hands.Add(h2);
                    break;
            }
            Advance(g, c);
        }

        // sang tay kế khi tay hiện tại xong; hết tay thì dealer rút rồi tính
        static void Advance(BjGame g, BlackjackConfig c)
        {
            while (g.active < g.hands.Count && g.hands[g.active].Finished) g.active++;
            if (g.active >= g.hands.Count) Settle(g, c);
        }

        static void Settle(BjGame g, BlackjackConfig c)
        {
            g.phase = BjPhase.Done;
            bool anyLive = !g.dealerPeekBj && g.hands.Any(h => !h.Bust && !h.Natural);
            if (anyLive)
                while (true)
                {
                    int t = Total(g.dealer, out bool soft);
                    if (t > 17 || (t == 17)) break; // dừng ở 17 mềm
                    g.dealer.Add(Draw(g.rng));
                }
            int dt = Total(g.dealer, out _);
            bool dealerBj = g.dealer.Count == 2 && dt == 21;
            g.results = new int[g.hands.Count];
            int pay = 0;
            for (int i = 0; i < g.hands.Count; i++)
            {
                var h = g.hands[i];
                int r;
                if (h.Natural) r = dealerBj ? 0 : 2;
                else if (dealerBj) r = -1;
                else if (h.Bust) r = -1;
                else if (dt > 21 || h.Total > dt) r = 1;
                else if (h.Total == dt) r = 0;
                else r = -1;
                g.results[i] = r;
                if (r == 2) pay += h.bet + (int)Math.Floor(h.bet * c.bjPays);
                else if (r == 1) pay += h.bet * 2;
                else if (r == 0) pay += h.bet;
            }
            g.payout = pay;
        }

        // ---------- chiến thuật cơ bản (hộp vô hạn, dealer dừng 17 mềm, gấp đôi sau tách, nhìn trộm) ----------

        public static BjAct Advice(BjGame g)
        {
            var h = g.Hand;
            if (h == null) return BjAct.Stand;
            int up = g.Up.rank == 1 ? 11 : g.Up.Value;
            bool canDouble = Can(g, BjAct.Double);
            if (Can(g, BjAct.Split))
            {
                int v = h.cards[0].rank == 1 ? 11 : h.cards[0].Value;
                bool split;
                switch (v)
                {
                    case 11: case 8: split = true; break;
                    case 10: case 5: split = false; break;
                    case 9: split = up != 7 && up != 10 && up != 11; break;
                    case 7: split = up <= 7; break;
                    case 6: split = up <= 6; break;
                    case 4: split = up == 5 || up == 6; break;
                    default: split = up <= 7; break; // 2, 3
                }
                if (split) return BjAct.Split;
            }
            int t = Total(h.cards, out bool soft);
            if (soft)
            {
                if (t >= 20) return BjAct.Stand;
                if (t == 19) return up == 6 && canDouble ? BjAct.Double : BjAct.Stand;
                if (t == 18)
                {
                    if (up >= 3 && up <= 6) return canDouble ? BjAct.Double : BjAct.Stand;
                    if (up == 2 || up == 7 || up == 8) return BjAct.Stand;
                    return BjAct.Hit;
                }
                bool dbl = t == 17 ? up >= 3 && up <= 6 : t >= 15 ? up >= 4 && up <= 6 : up >= 5 && up <= 6;
                return dbl && canDouble ? BjAct.Double : BjAct.Hit;
            }
            if (t >= 17) return BjAct.Stand;
            if (t >= 13) return up <= 6 ? BjAct.Stand : BjAct.Hit;
            if (t == 12) return up >= 4 && up <= 6 ? BjAct.Stand : BjAct.Hit;
            if (t == 11) return canDouble ? BjAct.Double : BjAct.Hit;
            if (t == 10) return up <= 9 && canDouble ? BjAct.Double : BjAct.Hit;
            if (t == 9) return up >= 3 && up <= 6 && canDouble ? BjAct.Double : BjAct.Hit;
            return BjAct.Hit;
        }

        // ---------- chơi trên bản lưu ----------

        // bắt đầu ván có cược (false nếu bàn đóng, hết lượt, thiếu bi, bậc chưa mở)
        public static BjGame Start(SaveData s, GameData d, int tier, double now, Rng rng, out string why)
        {
            var c = Casino.C(d).blackjack;
            why = null;
            if (!Casino.BoothOpen(s, d, Casino.Blackjack, now)) { why = Loc.T("Lều Đêm Bài chưa mở"); return null; }
            if (!Casino.BetOpen(s, c, tier)) { why = Loc.F("Mở ở cấp {0}", Casino.BetLevel(c, tier)); return null; }
            if (Casino.PlaysLeft(s, d, Casino.Blackjack, now) <= 0) { why = Loc.T("Hết ván hôm nay"); return null; }
            int bet = Casino.Bet(s, d, c, tier);
            if (!Casino.Stake(s, d, bet, now)) { why = Loc.T("Không đủ bi"); return null; }
            Casino.UsePlay(s, d, Casino.Blackjack, now);
            Casino.Track(s, d, "table", 1, now);
            return Deal(bet, rng, c);
        }

        // gấp đôi / tách trên bản lưu: trả thêm cược gốc của tay rồi làm
        public static bool ActPaid(SaveData s, GameData d, BjGame g, BjAct a, double now)
        {
            var c = Casino.C(d).blackjack;
            if (!Can(g, a)) return false;
            if (a == BjAct.Double || a == BjAct.Split)
                if (!Casino.Stake(s, d, g.Hand.bet, now)) return false;
            Act(g, a, c);
            return true;
        }

        // ván xong: trả tiền thắng, đổ hũ (theo tổng đã cược của ván)
        public static JarResult Finish(SaveData s, GameData d, BjGame g, int tier, double now, Rng rng)
        {
            if (g.phase != BjPhase.Done) return new JarResult();
            Casino.Win(s, d, g.payout, now);
            return Casino.Pour(s, d, Casino.Blackjack, tier, g.Staked, now, rng);
        }
    }
}
