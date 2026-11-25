// Đua tướng (Trường đua, GD_Claude/29_DaoCasino.md mục 6.3). Người dùng 2026-11-25: "random 3-5 tướng mỗi lane chạy đua nhau, trên
// đường chạy tướng có thể đánh nhau cho vui vui, có tướng bị choáng stun, nó cũng kiểu random ai về nhất cho vui thôi".
// - Mỗi cuộc đua ngẫu nhiên minRunners..maxRunners tướng (người chơi + tướng của thám hiểm gia khác), mỗi tướng một làn.
// - Đường đua đổi theo ngày: segs chặng, mỗi chặng một địa hình theo hệ. Chỉ số tốc, sao, cấp, địa hình chỉ lệch nhẹ; dao động mỗi chặng
//   lớn hơn, nên về nhất phần lớn là hên xui.
// - Đánh nhau: tướng đang chạy, hết hồi chiêu, có tướng khác trong tầm fightRange thì mỗi giây có fightRate cơ hội lao vào đánh tướng gần
//   nhất (ưu tiên tướng phía trước). Trúng (hitChance): đối thủ choáng stunSec giây (đứng yên). Hụt: kẻ đánh tự vấp, choáng trip giây.
//   Đối thủ đang được cổ vũ (khiên guardSec giây): né, kẻ đánh vấp.
// - Gió thuận: mỗi giây gustRate cơ hội một tướng được +gust tốc trong gustSec giây.
// - Cổ vũ (người chơi, mỗi chặng một lần, theo vòng sáng): Tốt +cheer[1] tốc, Tuyệt +cheer[2] tốc và khiên né đòn; tướng máy cổ vũ theo độ giỏi.
// - Thưởng: lệ phí × placeK[hạng] × số tướng (trung bình gần hoà vốn khi ai cũng như nhau), điểm cúp tuần theo hạng.
// - Mô phỏng nhịp 1/30 giây, tất định theo hạt giống và lần chạm; Events ghi đánh nhau, né, vấp, gió để giao diện diễn.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum RaceEv { Hit, Trip, Dodge, Gust, Finish }

    public sealed class RaceEvent
    {
        public double t;
        public int a, b; // a: kẻ đánh / tướng được gió / về đích; b: đối thủ (−1 nếu không)
        public RaceEv kind;
    }

    public sealed class RaceRunner
    {
        public string hero;
        public Elem elem;
        public int star, level;
        public bool player;
        public double baseSpeed;
        public double[] noise = new double[0]; // theo chặng
        public int[] npcCheer = new int[0]; // tướng máy: chất lượng cổ vũ theo chặng
        // trạng thái chạy
        public double pos, finishT = -1;
        public int seg = -1, cheered = -1;
        public double segT0, boostUntil, boost, stunUntil, guardUntil, cool, gustUntil;
        public int[] cheerQ;
        public int hits, stuns; // số lần đánh trúng, số lần bị choáng (để hiện)

        public bool Stunned(double t) => t < stunUntil;
    }

    public sealed class RaceGame
    {
        public int cup;
        public Elem[] terrain = new Elem[0];
        public List<RaceRunner> runners = new List<RaceRunner>();
        public List<RaceEvent> events = new List<RaceEvent>();
        public double t;
        public bool done;
        public int fee; // lệ phí đã trả (0: đua tập)
        public Rng rng; // ngẫu nhiên lúc chạy (đánh nhau, gió), cùng hạt giống với lúc dựng
        public RaceRunner Player => runners.Find(r => r.player);
        public int PlayerIndex => runners.FindIndex(r => r.player);
        public double Length(RaceConfig c) => c.seg * c.segs;
    }

    public sealed class RaceResult
    {
        public int place; // 0-based
        public int runners;
        public int balls, points;
        public bool weekReady;
    }

    public static class Race
    {
        public const double Dt = 1 / 30.0, NpcCheerDelay = 0.55;

        public static Elem[] TrackOf(RaceConfig c, int day)
        {
            var rng = new Rng((uint)(day * 2246822519u + 3266489917u));
            var t = new Elem[c.segs];
            for (int i = 0; i < t.Length; i++) t[i] = Elements.All[rng.Int(0, Elements.All.Length - 1)];
            return t;
        }

        public static double BaseSpeed(RaceConfig c, HeroDef h, int star, int levelDiff, Elem? lucky)
        {
            double v = c.spdBase * (1 + c.spdK * (h.stats[5] - c.spdMid) / 10.0);
            v *= 1 + c.starK * (Math.Max(1, star) - 1);
            v *= 1 + c.lvK * Math.Max(-c.lvClamp, Math.Min(c.lvClamp, levelDiff));
            if (lucky.HasValue && h.elem == lucky.Value) v *= 1 + c.lucky;
            return v;
        }

        public static double Terrain(RaceConfig c, Elem terrain, Elem hero) =>
            terrain == hero ? c.same : Elements.Beats(terrain) == hero ? c.weak : 1;

        static int NpcQ(double skill, Rng rng)
        {
            double x = rng.Next();
            if (x < skill * 0.45) return 2;
            if (x < skill * 0.45 + 0.25 + skill * 0.2) return 1;
            return 0;
        }

        public static int RunnerCount(RaceConfig c, Rng rng) => rng.Int(Math.Max(2, c.minRunners), Math.Max(c.minRunners, c.maxRunners));

        // dựng cuộc đua: số tướng ngẫu nhiên, tướng máy chọn ngẫu nhiên (khác tướng người chơi), xáo làn
        public static RaceGame Setup(GameData d, RaceConfig c, int cupIdx, HeroDef mine, int myStar, int myLevel, int day, uint seed, Elem? lucky)
        {
            var cup = c.cups[Math.Max(0, Math.Min(cupIdx, c.cups.Count - 1))];
            var rng = new Rng(seed);
            var g = new RaceGame { cup = cupIdx, terrain = TrackOf(c, day) };
            int n = RunnerCount(c, rng);
            var pool = d.Heroes.Where(h => !h.minion && h.id != mine.id).ToList();
            g.runners.Add(new RaceRunner
            {
                hero = mine.id, elem = mine.elem, star = myStar, level = myLevel, player = true,
                baseSpeed = BaseSpeed(c, mine, myStar, myLevel - cup.oppLevel, lucky),
            });
            for (int i = 1; i < n && pool.Count > 0; i++)
            {
                var h = rng.Pick(pool);
                pool.Remove(h);
                int star = Math.Max(1, cup.oppStar + rng.Int(-1, 1));
                g.runners.Add(new RaceRunner { hero = h.id, elem = h.elem, star = star, level = cup.oppLevel, baseSpeed = BaseSpeed(c, h, star, 0, null) });
            }
            foreach (var r in g.runners)
            {
                r.noise = new double[c.segs];
                r.npcCheer = new int[c.segs];
                r.cheerQ = Enumerable.Repeat(-1, c.segs).ToArray();
                for (int k = 0; k < c.segs; k++)
                {
                    r.noise[k] = rng.Range(-c.noise, c.noise);
                    r.npcCheer[k] = NpcQ(cup.skill, rng);
                }
                r.cool = rng.Range(0.6, 1.8); // không đánh ngay khi xuất phát
            }
            for (int i = g.runners.Count - 1; i > 0; i--)
            {
                int j = rng.Int(0, i);
                (g.runners[i], g.runners[j]) = (g.runners[j], g.runners[i]);
            }
            g.rng = new Rng(seed ^ 0x9E3779B9u);
            return g;
        }

        public static double Speed(RaceConfig c, RaceGame g, RaceRunner r)
        {
            if (r.Stunned(g.t)) return 0;
            int k = Math.Max(0, Math.Min(c.segs - 1, r.seg));
            double v = r.baseSpeed * Terrain(c, g.terrain[k], r.elem) * (1 + r.noise[k]);
            if (g.t < r.boostUntil) v *= 1 + r.boost;
            if (g.t < r.gustUntil) v *= 1 + c.gust;
            return v;
        }

        public static int CheerSeg(RaceGame g)
        {
            var p = g.Player;
            if (p == null || p.finishT >= 0 || p.seg < 0 || p.cheered >= p.seg) return -1;
            return p.seg;
        }

        public static double SinceSegStart(RaceGame g) => g.Player == null ? 0 : g.t - g.Player.segT0;

        static void ApplyCheer(RaceConfig c, RaceGame g, RaceRunner r, int q)
        {
            r.cheered = r.seg;
            if (r.seg >= 0 && r.seg < r.cheerQ.Length) r.cheerQ[r.seg] = q;
            q = Math.Max(0, Math.Min(c.cheer.Length - 1, q));
            r.boost = c.cheer[q];
            r.boostUntil = g.t + c.cheerSec;
            if (q >= 2) r.guardUntil = g.t + c.guardSec; // Tuyệt: khiên né đòn
        }

        // người chơi cổ vũ với chất lượng q (0 Hụt, 1 Tốt, 2 Tuyệt)
        public static bool Cheer(RaceConfig c, RaceGame g, int q)
        {
            if (CheerSeg(g) < 0) return false;
            ApplyCheer(c, g, g.Player, q);
            return true;
        }

        // một nhịp Dt
        public static void Step(RaceConfig c, RaceGame g)
        {
            if (g.done) return;
            double len = g.Length(c);
            var rng = g.rng ?? (g.rng = new Rng(1));
            int n = g.runners.Count;
            // đánh nhau, gió
            for (int i = 0; i < n; i++)
            {
                var r = g.runners[i];
                if (r.finishT >= 0) continue;
                r.cool -= Dt;
                if (c.gustRate > 0 && rng.Chance(c.gustRate * Dt / Math.Max(1, n)))
                {
                    r.gustUntil = g.t + c.gustSec;
                    g.events.Add(new RaceEvent { t = g.t, a = i, b = -1, kind = RaceEv.Gust });
                }
                if (r.Stunned(g.t) || r.cool > 0 || !rng.Chance(c.fightRate * Dt)) continue;
                // đối thủ gần nhất trong tầm, ưu tiên phía trước
                int best = -1;
                double bestD = double.MaxValue;
                for (int j = 0; j < n; j++)
                {
                    if (j == i) continue;
                    var o = g.runners[j];
                    if (o.finishT >= 0 || o.Stunned(g.t)) continue;
                    double dx = o.pos - r.pos;
                    if (Math.Abs(dx) > c.fightRange) continue;
                    double score = Math.Abs(dx) - (dx > 0 ? c.fightRange * 0.5 : 0);
                    if (score < bestD) { bestD = score; best = j; }
                }
                if (best < 0) continue;
                var t = g.runners[best];
                r.cool = c.fightCool;
                if (g.t < t.guardUntil)
                {
                    r.stunUntil = g.t + c.trip;
                    g.events.Add(new RaceEvent { t = g.t, a = i, b = best, kind = RaceEv.Dodge });
                }
                else if (rng.Chance(c.hitChance))
                {
                    t.stunUntil = g.t + c.stunSec;
                    t.cool = Math.Max(t.cool, c.stunSec + 0.6);
                    t.stuns++;
                    r.hits++;
                    g.events.Add(new RaceEvent { t = g.t, a = i, b = best, kind = RaceEv.Hit });
                }
                else
                {
                    r.stunUntil = g.t + c.trip;
                    r.stuns++;
                    g.events.Add(new RaceEvent { t = g.t, a = i, b = best, kind = RaceEv.Trip });
                }
            }
            // chạy
            for (int i = 0; i < n; i++)
            {
                var r = g.runners[i];
                if (r.finishT >= 0) continue;
                int seg = Math.Min(c.segs - 1, (int)Math.Floor(r.pos / c.seg));
                if (seg != r.seg)
                {
                    r.seg = seg;
                    r.segT0 = g.t;
                }
                if (!r.player && r.cheered < r.seg && g.t - r.segT0 >= NpcCheerDelay) ApplyCheer(c, g, r, r.npcCheer[r.seg]);
                double v = Speed(c, g, r);
                double np = r.pos + v * Dt;
                if (np >= len)
                {
                    r.finishT = g.t + (len - r.pos) / Math.Max(1e-6, v);
                    r.pos = len;
                    g.events.Add(new RaceEvent { t = g.t, a = i, b = -1, kind = RaceEv.Finish });
                }
                else r.pos = np;
            }
            g.t += Dt;
            if (g.runners.All(r => r.finishT >= 0) || g.t > 120) g.done = true;
        }

        // chạy hết với chất lượng cổ vũ cố định của người chơi theo chặng (cheerAt: giây sau khi vào chặng)
        public static void Run(RaceConfig c, RaceGame g, int[] cheers, double cheerAt = 0.6)
        {
            int guard = 0;
            while (!g.done && guard++ < 100000)
            {
                int k = CheerSeg(g);
                if (k >= 0 && cheers != null && k < cheers.Length && SinceSegStart(g) >= cheerAt) Cheer(c, g, cheers[k]);
                Step(c, g);
            }
        }

        public static List<int> Order(RaceGame g) =>
            Enumerable.Range(0, g.runners.Count).OrderBy(i => g.runners[i].finishT < 0 ? double.MaxValue - g.runners[i].pos : g.runners[i].finishT).ThenBy(i => i).ToList();

        public static int PlaceOf(RaceGame g) => Order(g).IndexOf(g.PlayerIndex);

        // bi trả theo hạng: lệ phí × placeK[hạng] × số tướng
        public static int Payout(RaceConfig c, int fee, int place, int runners, double mult = 1) =>
            (int)Math.Round(fee * (place < c.placeK.Length ? c.placeK[place] : 0) * runners * mult);

        // ---------- trên bản lưu ----------

        public static int Fee(SaveData s, GameData d, int cup) => Shop.RoundBalls(Casino.C(d).race.cups[cup].fee * Casino.Band(s, d));

        public static bool CupOpen(SaveData s, GameData d, int cup) => cup >= 0 && cup < Casino.C(d).race.cups.Count && s.level >= Casino.C(d).race.cups[cup].level;

        static void RollWeek(SaveData s, GameData d, double now)
        {
            var st = Casino.Roll(s, d, now);
            int wk = Casino.Week(Casino.Today(now));
            int n = Casino.C(d).race.cups.Count;
            if (st.raceWeek != wk || st.cupPts.Length != n)
            {
                if (st.raceWeek != wk)
                {
                    st.cupPts = new int[n];
                    st.cupClaimed = 0;
                }
                else Array.Resize(ref st.cupPts, n);
                st.raceWeek = wk;
            }
        }

        public static int Points(SaveData s, GameData d, int cup, double now)
        {
            RollWeek(s, d, now);
            var st = Casino.Of(s);
            return cup < st.cupPts.Length ? st.cupPts[cup] : 0;
        }

        public static bool WeekReady(SaveData s, GameData d, int cup, double now) =>
            Points(s, d, cup, now) >= Casino.C(d).race.weekPts && (Casino.Of(s).cupClaimed & (1 << cup)) == 0;

        public static bool WeekClaimed(SaveData s, int cup) => (Casino.Of(s).cupClaimed & (1 << cup)) != 0;

        // bắt đầu đua: hết lượt có thưởng thì đua tập (không lệ phí, không thưởng); why khác null nếu không đua được
        public static RaceGame Start(SaveData s, GameData d, int cup, string hero, double now, Rng rng, out string why)
        {
            why = null;
            var c = Casino.C(d).race;
            if (!Casino.Unlocked(s, d, Casino.Race)) { why = Casino.Need(s, d, Casino.Race); return null; }
            if (!CupOpen(s, d, cup)) { why = Loc.F("Mở ở cấp {0}", c.cups[Math.Max(0, Math.Min(cup, c.cups.Count - 1))].level); return null; }
            var p = s.Hero(hero);
            var h = d.Hero(hero);
            if (p == null || !p.owned || h == null) { why = Loc.T("Chưa có tướng này"); return null; }
            int fee = 0;
            if (Casino.PlaysLeft(s, d, Casino.Race, now) > 0)
            {
                fee = Fee(s, d, cup);
                if (!Casino.Spend(s, fee)) { why = Loc.T("Không đủ bi"); return null; }
                Casino.UsePlay(s, d, Casino.Race, now);
            }
            var g = Setup(d, c, cup, h, p.star, s.level, Casino.Today(now), (uint)(rng.Next() * uint.MaxValue), Casino.LuckyActive(s, now));
            g.fee = fee;
            return g;
        }

        // đua xong: thưởng theo hạng và số tướng (× Lễ Hội Đua), điểm cúp tuần, nhiệm vụ quán trọ
        public static RaceResult Finish(SaveData s, GameData d, RaceGame g, double now)
        {
            var c = Casino.C(d).race;
            var res = new RaceResult { place = PlaceOf(g), runners = g.runners.Count };
            if (!g.done) return res;
            Casino.Track(s, d, "race", 1, now);
            if (res.place < 3) Casino.Track(s, d, "race_top3", 1, now);
            if (g.fee <= 0) return res; // đua tập
            RollWeek(s, d, now);
            var st = Casino.Of(s);
            res.balls = Payout(c, g.fee, res.place, res.runners, Casino.RaceMult(d, now));
            Casino.Win(s, d, res.balls, now);
            res.points = res.place < c.points.Length ? c.points[res.place] : 0;
            if (g.cup < st.cupPts.Length) st.cupPts[g.cup] = Math.Min(c.weekPts, st.cupPts[g.cup] + res.points);
            res.weekReady = WeekReady(s, d, g.cup, now);
            return res;
        }

        public static List<Reward> ClaimWeek(SaveData s, GameData d, int cup, double now, Rng rng)
        {
            if (!WeekReady(s, d, cup, now)) return new List<Reward>();
            Casino.Of(s).cupClaimed |= 1 << cup;
            return Casino.Grant(s, d, Casino.C(d).race.cups[cup].week, now, rng);
        }
    }
}
