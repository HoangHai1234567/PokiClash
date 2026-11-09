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
        public readonly double[] ringHits = new double[2]; // số lần chạm nấm trái, phải mỗi bi
        public double flightMedian, triesPerBall; // thời gian bay trung vị (giây), số lần thử vật lý mỗi bi
        public int misses; // số bi không tìm được đường rơi đúng kết quả đã chọn

        public double Rate(SlotKind k) => count.TryGetValue(k, out var c) ? (double)c / balls : 0;
    }

    public static class Sim
    {
        // 5 mức cấp quanh khoảng đề nghị của đảo
        public static int[] Levels(ZoneDef z) =>
            new[] { z.levelMin - 2, z.levelMin, Js.RoundInt((z.levelMin + z.levelMax) / 2.0), z.levelMax, z.levelMax + 2 }.Select(l => Math.Max(1, l)).ToArray();

        // bản lưu giả cho một ô của bảng: đội, cấp, sao, cấp cả 3 thẻ; starter: tướng khởi đầu đã chọn (tướng đồng hành), null = không có
        public static SaveData Setup(GameData d, IList<string> team, int level, int star, int card, string starter = null)
        {
            var s = SaveData.New(d, 0, starter);
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
                var b = Battle.Create(d, PlayerAi(d, s, tm, bonus, start), Teams.Enemy(st, d), (uint)(seed + i * 7919), s.level, s.level);
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
                    var b = Battle.Create(d, PlayerAi(d, s, s.team, null), Teams.Enemy(st, d), (uint)(Badges.Seed(d, z, tier, i) + k * 7919),
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

        // ---------- tướng khởi đầu (GD_Claude/15_TuongKhoiDau.md) ----------

        // sao người chơi có ở cấp level nếu theo kịp (sao n khi đủ cấp cfg.starLevel[n], như npm run sim -- island)
        public static int StarAt(BalanceConfig cfg, int level)
        {
            int star = 1;
            while (star < cfg.maxStar && star + 1 < cfg.starLevel.Length && cfg.starLevel[star + 1] <= level) star++;
            return star;
        }

        // đội khi tới ải st, chọn tướng khởi đầu starter: tướng khởi đầu và tướng tặng ở các ải trước của đảo (quà theo tướng khởi đầu),
        // tối đa số ô đã mở ở cấp bằng cấp địch của ải (ô 2 từ cấp 10), tướng khắc tướng chính của ải ra sân trước.
        // Không tính tướng thu phục bằng mảnh.
        // oldRules: luật trước khi có 5 tướng khởi đầu (1 ô suốt đảo đầu, quà luôn là tướng gốc, không có tướng đồng hành).
        public static List<string> StarterTeam(GameData d, string starter, StageDef st, bool oldRules = false)
        {
            var s = SaveData.New(d, 0, oldRules ? null : starter);
            s.level = st.enemies.Max(e => e.level);
            s.zones[(int)st.zone] = st.idx - 1;
            var owned = new List<string> { starter };
            foreach (var x in d.ZoneStages(st.zone))
                if (x.idx < st.idx)
                    foreach (var dr in x.drops)
                        if (dr.gift)
                        {
                            var h = oldRules ? dr.hero : dr.HeroFor(s);
                            if (!owned.Contains(h)) owned.Add(h);
                        }
            int slots = oldRules ? 1 : Progress.TeamSlots(s);
            var foe = d.Hero(Teams.StageLead(st, d).hero).elem;
            bool Partner(string h) => !oldRules && h == starter;
            double Edge(string h) => Elements.Mult(d.Hero(h).elem, foe, Partner(h), false) - Elements.Mult(foe, d.Hero(h).elem, false, Partner(h));
            return owned.OrderByDescending(Edge).ThenByDescending(h => (int)d.Hero(h).rarity).Take(slots).ToList();
        }

        public sealed class StarterRow
        {
            public StageDef st;
            public int level, star;
            public List<string> team;
            public SimCell cell;
        }

        // n trận mỗi ải của đảo z: cấp bằng cấp địch cao nhất của ải, sao theo cấp, cấp thẻ bằng sao, đội theo StarterTeam
        public static List<StarterRow> StarterIsland(GameData d, string starter, Elem z, int n, bool oldRules = false)
        {
            var rows = new List<StarterRow>();
            foreach (var st in d.ZoneStages(z))
            {
                int lv = st.enemies.Max(e => e.level), star = StarAt(d.Cfg, lv);
                var team = StarterTeam(d, starter, st, oldRules);
                var s = Setup(d, team, lv, star, star, oldRules ? null : starter);
                rows.Add(new StarterRow { st = st, level = lv, star = star, team = team, cell = Stage(d, s, st, n) });
            }
            return rows;
        }

        // kiểu ải để gom bảng như npm run sim -- island: mini boss, boss, còn lại theo kiểu ải (đảo 8 ải: "normal")
        public static string StageKey(StageDef st) =>
            st.kind == StageKind.Mini ? "mini" : st.kind == StageKind.Boss ? "boss" : Keys.Of(st.tag) ?? "normal";

        // tay đôi a với b cùng cấp, sao theo cấp, cấp thẻ bằng sao, không có tướng đồng hành; nửa số trận đổi bên. Trả tỉ lệ thắng của a.
        public static double Duel(GameData d, string a, string b, int level, int n, uint seed = 1000)
        {
            int star = StarAt(d.Cfg, level), win = 0;
            var s = Setup(d, new[] { a, b }, level, star, star);
            for (int i = 0; i < n; i++)
            {
                bool flip = i % 2 == 1;
                var ta = PlayerAi(d, s, new[] { a }, null);
                var tb = PlayerAi(d, s, new[] { b }, null);
                var bt = Battle.Create(d, flip ? tb : ta, flip ? ta : tb, (uint)(seed + i * 7919), level, level);
                BattleSim.Run(bt);
                if (bt.winner == (flip ? 1 : 0)) win++;
            }
            return (double)win / n;
        }

        // ---------- máy bi ----------

        // phóng total bi theo bảng tỉ lệ của cấu hình (mỗi bi cách nhau 10 khung, như giữ nút thả), đếm chỗ rơi, số lần chạm từng
        // nấm, thời gian bay; mở thử mỗi loại rương chestOpens lần; cộng giá trị vòng nấm theo số lần chạm đo được
        public static PachinkoReport Machine(GameData d, int total = 6000, int chestOpens = 20000, uint seed = 7)
        {
            var rep = new PachinkoReport { balls = total };
            var board = new Board(seed) { odds = d.Cfg.odds.Length > 0 ? d.Cfg.odds : null };
            int landed = 0, dropped = 0, frame = 0;
            var times = new List<double>();
            while (landed < total && frame < 400000)
            {
                if (dropped < total && frame % 10 == 0)
                {
                    board.Launch(1);
                    dropped++;
                }
                foreach (var e in board.Step())
                {
                    if (!e.land)
                    {
                        int ring = Array.IndexOf(board.ringPeg, e.peg);
                        if (ring >= 0) rep.ringHits[ring]++;
                        continue;
                    }
                    landed++;
                    times.Add(e.ball.age);
                    rep.count[e.reward] = rep.count.TryGetValue(e.reward, out var c) ? c + 1 : 1;
                    var place = e.cup ? $"cốc:{Pachinko.Key(e.reward)}" : $"ô{e.slot}:{Pachinko.Key(e.reward)}";
                    rep.byPlace[place] = rep.byPlace.TryGetValue(place, out var c2) ? c2 + 1 : 1;
                }
                frame++;
            }
            for (int i = 0; i < rep.ringHits.Length; i++) rep.ringHits[i] /= Math.Max(1, landed);
            times.Sort();
            rep.flightMedian = times.Count > 0 ? times[times.Count / 2] : 0;
            rep.misses = board.misses;
            rep.triesPerBall = (double)board.tries / Math.Max(1, total);
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
            // vòng nấm: mỗi bi chạm ringHits[i] lần, đủ n lần ra một quà
            for (int i = 0; i < d.Cfg.rings.Count && i < rep.ringHits.Length; i++)
            {
                var g = d.Cfg.rings[i];
                if (g.n <= 0) continue;
                double fills = rep.ringHits[i] / g.n;
                if (g.k == "balls") rep.backPerBall += fills * g.v;
                else if (g.k == "exp") rep.expPerBall += fills * g.v;
                else
                {
                    var ev = rep.chestEv[Pachinko.FromKey(g.k)];
                    rep.expPerBall += fills * ev.exp;
                    rep.backPerBall += fills * ev.balls;
                    rep.cardsPerBall += fills * ev.cards;
                }
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
