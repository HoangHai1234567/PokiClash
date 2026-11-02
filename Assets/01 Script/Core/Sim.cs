// Máy tự chơi hàng loạt và mô phỏng máy bi, cho cửa sổ Cân bằng, mục "Máy tự chơi" của Sổ tay bản dev và test so với web.
// Chép Web/src/core/sim.ts (bảng theo đảo: hạt giống 1000 + i × 7919, cả hai bên do máy chọn) và scripts/sim.ts (máy bi).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public struct SimCell
    {
        public int n, win;
        public double rounds; // tổng số hiệp
        public double WinRate => n > 0 ? (double)win / n : 0;
        public double AvgRounds => n > 0 ? rounds / n : 0;
    }

    public sealed class PachinkoReport
    {
        public int balls, frames;
        public readonly Dictionary<SlotKind, int> count = new Dictionary<SlotKind, int>();
        public readonly Dictionary<string, int> byPlace = new Dictionary<string, int>(); // "ô3:ball", "cốc:chest_gold"
        public readonly Dictionary<SlotKind, (double exp, double balls, double cards)> chestEv = new Dictionary<SlotKind, (double, double, double)>();
        public double expPerBall, backPerBall, cardsPerBall;

        public double Rate(SlotKind k) => count.TryGetValue(k, out var c) ? (double)c / balls : 0;
    }

    public static class Sim
    {
        // 5 mức cấp quanh khoảng đề nghị của đảo
        public static int[] Levels(ZoneDef z) =>
            new[] { z.levelMin - 2, z.levelMin, Js.RoundInt((z.levelMin + z.levelMax) / 2.0), z.levelMax, z.levelMax + 2 }.Select(l => Math.Max(1, l)).ToArray();

        // bản lưu giả cho một ô của bảng: đội, cấp, sao, cấp cả 3 thẻ
        public static SaveData Setup(GameData d, IList<string> team, int level, int star, int card)
        {
            var s = SaveData.New(d, 0);
            s.level = level;
            s.team = new List<string>(team);
            foreach (var h in team)
            {
                var p = s.Hero(h);
                if (p == null) continue;
                p.owned = true;
                p.star = star;
                p.skill.lv = p.ult.lv = p.passive.lv = card;
            }
            return s;
        }

        static TeamSetup PlayerAi(GameData d, SaveData s, IList<string> team, StatMods bonus, BattleStart start = null)
        {
            var t = Teams.Player(s, team, d);
            t.ai = true;
            if (bonus != null && !bonus.IsEmpty)
                foreach (var m in t.members)
                    m.mods = new StatMods { hpPct = bonus.hpPct, atkPct = bonus.atkPct, defPct = bonus.defPct, spd = bonus.spd };
            if (start != null)
                foreach (var m in t.members)
                    m.start = new BattleStart { mana = start.mana, rage = start.rage, crit = start.crit, lifesteal = start.lifesteal };
            return t;
        }

        // tiềm năng mẫu cho công cụ: 0 không có; 1 trung bình (kỳ vọng của 4 dòng ngẫu nhiên); 2 trần (Công Huyền thoại ×3 chặn 40% + Máu Huyền thoại)
        public static (double[] totals, string name) PotentialPreset(BalanceConfig cfg, int kind)
        {
            var pc = cfg.potential;
            if (kind == 1)
            {
                double wsum = pc.rarityWeight.Sum();
                var t = new double[8];
                for (int k = 0; k < 8; k++)
                {
                    double e = 0;
                    for (int r = 0; r < pc.rarityWeight.Length; r++) e += pc.rarityWeight[r] / wsum * pc.Val(k, r);
                    t[k] = Math.Min(pc.caps[k], 4 * e / 8);
                }
                return (t, "trung bình");
            }
            if (kind == 2)
            {
                var lines = new[]
                {
                    new PotLine { k = PotKind.Atk, r = 4 }, new PotLine { k = PotKind.Atk, r = 4 }, new PotLine { k = PotKind.Atk, r = 4 }, new PotLine { k = PotKind.Hp, r = 4 },
                };
                return (Potential.Totals(cfg, lines), "trần");
            }
            return (new double[8], "không");
        }

        // n trận một ải với bản lưu s (đội của s hoặc team), hạt giống seed + i × 7919, thẻ chung mở theo cấp s.level
        public static SimCell Stage(GameData d, SaveData s, StageDef st, int n, uint seed = 1000, IList<string> team = null, StatMods bonus = null, BattleStart start = null)
        {
            var cell = new SimCell { n = n };
            var tm = team ?? s.team;
            for (int i = 0; i < n; i++)
            {
                var b = Battle.Create(d, PlayerAi(d, s, tm, bonus, start), Teams.Enemy(st), (uint)(seed + i * 7919), s.level, s.level);
                BattleSim.Run(b);
                if (b.winner == 0) cell.win++;
                cell.rounds += b.round;
            }
            return cell;
        }

        // một bậc thử thách huy hiệu: n trận mỗi trận của bậc (hạt giống của trận + k × 7919, như npm run sim -- badges)
        public static (int win, int total, int lastWin) BadgeTier(GameData d, SaveData s, Elem z, int tier, int n)
        {
            int cnt = Badges.Count(d.Cfg, tier), win = 0, total = 0, last = 0;
            for (int i = 1; i <= cnt; i++)
            {
                var st = Badges.Stage(d, z, tier, i);
                for (int k = 0; k < n; k++)
                {
                    var b = Battle.Create(d, PlayerAi(d, s, s.team, null), Teams.Enemy(st), (uint)(Badges.Seed(d, z, tier, i) + k * 7919),
                        s.level, Math.Max(s.level, st.enemies[0].level));
                    BattleSim.Run(b);
                    if (b.winner == 0)
                    {
                        win++;
                        if (i == cnt) last++;
                    }
                    total++;
                }
            }
            return (win, total, last);
        }

        // ---------- máy bi ----------

        // thả total bi đều theo dãy tỉ lệ vàng (như bảng tỉ lệ của export_data.ts), mở thử mỗi loại rương chestOpens lần
        public static PachinkoReport Machine(GameData d, double[] slotW = null, int total = 6000, int chestOpens = 20000, uint seed = 7)
        {
            var rep = new PachinkoReport { balls = total };
            var board = new Board(seed, slotW);
            int landed = 0, dropped = 0, frame = 0;
            while (landed < total && frame < 400000)
            {
                if (dropped < total && frame % 6 == 0)
                {
                    board.Drop(Board.BW / 2 + ((dropped * 0.6180339887498949 % 1) * 2 - 1) * Board.Swing, 1);
                    dropped++;
                }
                foreach (var e in board.Step(1.0 / 60))
                {
                    if (!e.land) continue;
                    landed++;
                    rep.count[e.reward] = rep.count.TryGetValue(e.reward, out var c) ? c + 1 : 1;
                    var place = e.cup ? $"cốc:{Pachinko.Key(e.reward)}" : $"ô{e.slot}:{Pachinko.Key(e.reward)}";
                    rep.byPlace[place] = rep.byPlace.TryGetValue(place, out var c2) ? c2 + 1 : 1;
                }
                frame++;
            }
            rep.frames = frame;
            var rng = new Rng(3);
            foreach (var kind in new[] { SlotKind.ChestWood, SlotKind.ChestSilver, SlotKind.ChestGold })
            {
                double exp = 0, balls = 0, cards = 0;
                for (int i = 0; i < chestOpens; i++)
                    foreach (var r in Pachinko.OpenChest(SaveData.New(d, 0), d, kind, 1, rng))
                    {
                        if (r.k == RewardKind.Exp) exp += r.n;
                        else if (r.k == RewardKind.Balls) balls += r.n;
                        else if (r.k == RewardKind.Card) cards++;
                    }
                rep.chestEv[kind] = (exp / chestOpens, balls / chestOpens, cards / chestOpens);
            }
            foreach (var kv in rep.count)
            {
                double p = (double)kv.Value / total;
                if (Pachinko.Exp(kv.Key) > 0) rep.expPerBall += p * Pachinko.Exp(kv.Key);
                else if (kv.Key == SlotKind.Ball) rep.backPerBall += p;
                else
                {
                    var ev = rep.chestEv[kv.Key];
                    rep.expPerBall += p * ev.exp;
                    rep.backPerBall += p * ev.balls;
                    rep.cardsPerBall += p * ev.cards;
                }
            }
            return rep;
        }
    }
}
