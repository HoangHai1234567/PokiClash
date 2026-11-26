// Đua tướng (Trường đua, GD_Claude/29_DaoCasino.md mục 6.3). Luật cược (người dùng 2026-11-26): "đặt 1 trong 5 con ... đặt max là 500
// bóng, mình có thể kiểm soát tỉ lệ thắng thua. nếu về nhất x3, về nhì x2, về 3 thì hòa tiền, 4, 5 mất tiền. 1 ngày được chơi 5 lần.
// Tiền cược càng cao bạn phải cho người chơi tỉ lệ thắng càng thấp. Làm cuộc đua gay cấn hơn, các con đua nhau sát hơn, có những
// lúc vọt lên kiểu bất ngờ."
// - Mỗi cuộc đua 5 tướng ngẫu nhiên (Lineup), mỗi tướng một làn. Người chơi chọn một con và đặt betMin..betMax bi.
// - Hạng của con được chọn RÚT TRƯỚC theo bảng tỉ lệ (PlaceOdds): mức cược thấp dùng oddsLow, cao dùng oddsHigh, ở giữa nội suy; phần còn
//   lại chia đều cho các hạng không trả thưởng. Các con khác xếp ngẫu nhiên vào hạng còn lại. Đua tập (không cược): mọi hạng như nhau.
// - Trả thưởng: cược × pay[hạng] (3, 2, 1, 0, 0); phần lời nhân hệ số Lễ Hội Đua. Điểm cúp tuần theo hạng như cũ.
// - Cuộc đua là một kịch bản dựng sẵn từ hạt giống, không phải mô phỏng tự do: cả đoàn chạy theo một nhịp chung (về nhất sau raceSec
//   giây), mỗi con lệch khỏi nhịp theo các mốc ngẫu nhiên cách nhau keyMin..keyMax giây, trong ±spread đơn vị, nên cả đoàn bám sát và
//   đổi ngôi liên tục. Giữa hai mốc: vọt lên ≥ surge đơn vị thì thành cú BỨT TỐC dồn trong surgeSec giây (sự kiện Gust); tụt ≥ stunDrop
//   thì thành BỊ HÚC CHOÁNG, đứng yên tối đa stunMax giây (sự kiện Hit, kẻ húc là con gần nhất). Mốc trước nước rút cài kịch tính: con
//   sẽ về nhất hay còn ở sau (comeback), con mình chọn mà sẽ thua hay đang dẫn (tease). Mốc cuối đưa từng con về đích đúng giờ đã định,
//   hai hạng liền nhau cách gapMin..gapMax giây (sát nút).
// - Mô phỏng nhịp 1/30 giây, tất định theo hạt giống; Events ghi bứt tốc, bị húc, về đích để giao diện diễn.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum RaceEv { Hit, Trip, Dodge, Gust, Finish } // Trip, Dodge: luật cũ, không còn sinh ra

    public sealed class RaceEvent
    {
        public double t;
        public int a, b; // Hit: a húc b; Gust, Finish: a (b = −1)
        public RaceEv kind;
    }

    public sealed class RaceRunner
    {
        public string hero;
        public Elem elem;
        public bool player; // con người chơi đặt cược
        public int place; // hạng đã định (0 = nhất)
        public double finishAt; // giờ về đích đã định
        // kịch bản: tại giây keyT[k] lệch keyO[k] đơn vị so với nhịp chung; keyKind[k] là cách đi tới mốc k (0 đều, 1 bứt tốc, 2 bị húc
        // choáng keyDur[k] giây rồi chạy tiếp)
        public double[] keyT = new double[0], keyO = new double[0], keyDur = new double[0];
        public byte[] keyKind = new byte[0];
        // trạng thái chạy
        public int key; // đang ở đoạn giữa mốc key và key + 1
        public double pos, speed, finishT = -1, stunUntil, gustUntil;
        public int hits, stuns; // số lần húc trúng, số lần bị choáng (để hiện)

        public bool Stunned(double t) => t < stunUntil;
    }

    public sealed class RaceGame
    {
        public Elem[] terrain = new Elem[0];
        public List<RaceRunner> runners = new List<RaceRunner>();
        public List<RaceEvent> events = new List<RaceEvent>();
        public double t, pace; // pace: tốc nhịp chung (đơn vị / giây)
        public bool done;
        public int bet; // bi đã đặt (0: đua tập)
        public RaceRunner Player => runners.Find(r => r.player);
        public int PlayerIndex => runners.FindIndex(r => r.player);
        public double Length(RaceConfig c) => c.seg * c.segs;
    }

    public sealed class RaceResult
    {
        public int place; // 0-based
        public int runners;
        public int balls, points; // balls: bi nhận về (gồm cả tiền cược nếu thắng / hoà)
        public bool weekReady;
    }

    public static class Race
    {
        public const double Dt = 1 / 30.0;
        const byte Even = 0, Surge = 1, Stun = 2;

        public static Elem[] TrackOf(RaceConfig c, int day)
        {
            var rng = new Rng((uint)(day * 2246822519u + 3266489917u));
            var t = new Elem[c.segs];
            for (int i = 0; i < t.Length; i++) t[i] = Elements.All[rng.Int(0, Elements.All.Length - 1)];
            return t;
        }

        // đoàn đua: runners tướng khác nhau, ngẫu nhiên theo hạt giống
        public static List<string> Lineup(GameData d, RaceConfig c, uint seed)
        {
            var rng = new Rng(seed);
            var pool = d.Heroes.Where(h => !h.minion).ToList();
            var list = new List<string>();
            for (int i = 0; i < c.runners && pool.Count > 0; i++)
            {
                var h = rng.Pick(pool);
                pool.Remove(h);
                list.Add(h.id);
            }
            return list;
        }

        // tỉ lệ con được chọn về từng hạng theo mức cược; n: số tướng. Đua tập (bet ≤ 0): đều nhau.
        public static double[] PlaceOdds(RaceConfig c, int bet, int n)
        {
            var p = new double[Math.Max(1, n)];
            if (bet <= 0)
            {
                for (int i = 0; i < p.Length; i++) p[i] = 1.0 / p.Length;
                return p;
            }
            double k = c.betMax > c.betMin ? Math.Max(0, Math.Min(1, (bet - c.betMin) / (double)(c.betMax - c.betMin))) : 1;
            int paid = Math.Min(p.Length, Math.Min(c.oddsLow.Length, c.oddsHigh.Length));
            double sum = 0;
            for (int i = 0; i < paid; i++)
            {
                p[i] = Math.Max(0, c.oddsLow[i] + (c.oddsHigh[i] - c.oddsLow[i]) * k);
                sum += p[i];
            }
            if (paid >= p.Length || sum >= 1)
            {
                for (int i = 0; i < p.Length; i++) p[i] /= Math.Max(1e-9, sum);
                return p;
            }
            for (int i = paid; i < p.Length; i++) p[i] = (1 - sum) / (p.Length - paid);
            return p;
        }

        // bi trả về trên mỗi bi cược (trung bình) ở mức cược này: để cân và để test
        public static double Rtp(RaceConfig c, int bet, int n)
        {
            var p = PlaceOdds(c, bet, n);
            double ev = 0;
            for (int i = 0; i < p.Length; i++) ev += p[i] * (i < c.pay.Length ? c.pay[i] : 0);
            return ev;
        }

        // dựng cuộc đua: rút hạng cho con được chọn theo mức cược, xếp các con khác, viết kịch bản đường chạy
        public static RaceGame Setup(GameData d, RaceConfig c, IList<string> lineup, int pick, int bet, int day, uint seed)
        {
            var rng = new Rng(seed);
            var g = new RaceGame { terrain = TrackOf(c, day), bet = Math.Max(0, bet) };
            int n = lineup.Count;
            pick = Math.Max(0, Math.Min(n - 1, pick));
            // hạng
            var odds = PlaceOdds(c, bet, n);
            double x = rng.Next(), acc = 0;
            int mine = n - 1;
            for (int i = 0; i < n; i++)
            {
                acc += odds[i];
                if (x < acc) { mine = i; break; }
            }
            var rest = Enumerable.Range(0, n).Where(i => i != mine).ToList();
            for (int i = rest.Count - 1; i > 0; i--)
            {
                int j = rng.Int(0, i);
                (rest[i], rest[j]) = (rest[j], rest[i]);
            }
            double len = g.Length(c);
            g.pace = len / Math.Max(1, c.raceSec);
            var at = new double[n]; // giờ về đích theo hạng: hai hạng liền nhau sát nút
            at[0] = c.raceSec;
            for (int i = 1; i < n; i++) at[i] = at[i - 1] + rng.Range(c.gapMin, c.gapMax);
            int k = 0;
            for (int i = 0; i < n; i++)
            {
                var h = d.Hero(lineup[i]);
                var r = new RaceRunner { hero = lineup[i], elem = h != null ? h.elem : Elem.Kim, player = i == pick, place = i == pick ? mine : rest[k++] };
                r.finishAt = at[r.place];
                Script(c, g, r, n, rng);
                g.runners.Add(r);
            }
            return g;
        }

        // kịch bản đường chạy của một con: các mốc lệch nhịp, mốc kịch tính trước nước rút, mốc về đích
        static void Script(RaceConfig c, RaceGame g, RaceRunner r, int n, Rng rng)
        {
            double len = g.Length(c), v = g.pace, s = c.spread;
            double end = len - v * r.finishAt; // độ lệch lúc về đích (≤ 0: về sau con nhất)
            // càng về cuối càng lộ dần hạng thật, nhưng phần lớn độ tụt dồn vào nước rút
            double Bias(double t) => end * Math.Pow(Math.Max(0, Math.Min(1, t / r.finishAt)), 3);
            var kt = new List<double> { 0, c.startSec };
            var ko = new List<double> { 0, 0 };
            double tDrama = r.finishAt - c.endSec;
            for (double t = c.startSec + rng.Range(c.keyMin, c.keyMax); t < tDrama - c.keyMin * 0.6; t += rng.Range(c.keyMin, c.keyMax))
            {
                kt.Add(t);
                ko.Add(Bias(t) + rng.Range(-s, s));
            }
            double drama;
            if (r.place == 0) drama = rng.Chance(c.comeback) ? rng.Range(-s, -s * 0.35) : rng.Range(-s * 0.3, s * 0.6); // lội ngược dòng
            else if (r.player && r.place >= 2) drama = rng.Chance(c.tease) ? rng.Range(s * 0.45, s) : rng.Range(-s, s); // dẫn rồi hụt hơi
            else drama = rng.Range(-s, s);
            kt.Add(tDrama);
            ko.Add(Bias(tDrama) * 0.5 + drama);
            kt.Add(r.finishAt);
            ko.Add(end);
            int m = kt.Count;
            r.keyT = kt.ToArray();
            r.keyO = ko.ToArray();
            r.keyKind = new byte[m];
            r.keyDur = new double[m];
            for (int i = 2; i < m; i++)
            {
                double d = r.keyO[i] - r.keyO[i - 1], span = r.keyT[i] - r.keyT[i - 1];
                if (d >= c.surge)
                {
                    r.keyKind[i] = Surge;
                    r.keyDur[i] = Math.Min(c.surgeSec, span);
                }
                else if (d <= -c.stunDrop && i < m - 1) // không cho choáng ngay trước vạch đích
                {
                    r.keyKind[i] = Stun;
                    r.keyDur[i] = Math.Min(Math.Min(c.stunMax, -d / v), span * 0.75);
                }
            }
        }

        static double Smooth(double u) => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u);

        // độ lệch so với nhịp chung ở giây t (đoạn mốc r.key → r.key + 1)
        static double Offset(RaceGame g, RaceRunner r, double t)
        {
            int k = r.key;
            if (k >= r.keyT.Length - 1) return r.keyO[r.keyO.Length - 1];
            double t0 = r.keyT[k], t1 = r.keyT[k + 1], o0 = r.keyO[k], o1 = r.keyO[k + 1];
            double span = Math.Max(1e-6, t1 - t0), dur = r.keyDur[k + 1];
            switch (r.keyKind[k + 1])
            {
                case Surge:
                {
                    double u = Math.Min(1, (t - t0) / Math.Max(1e-6, dur));
                    return o0 + (o1 - o0) * (1 - (1 - u) * (1 - u)); // dồn vào đầu đoạn, chậm dần
                }
                case Stun:
                {
                    if (t - t0 <= dur) return o0 - g.pace * (t - t0); // đứng yên: nhịp chung chạy đi, mình tụt lại
                    double os = o0 - g.pace * dur;
                    return os + (o1 - os) * Smooth((t - t0 - dur) / Math.Max(1e-6, span - dur));
                }
                default:
                    return o0 + (o1 - o0) * Smooth((t - t0) / span);
            }
        }

        // tốc đang chạy (đơn vị / giây) để giao diện chỉnh nhịp bước
        public static double Speed(RaceConfig c, RaceGame g, RaceRunner r) => r.speed;

        // một nhịp Dt
        public static void Step(RaceConfig c, RaceGame g)
        {
            if (g.done) return;
            double len = g.Length(c), t = g.t + Dt;
            int n = g.runners.Count;
            for (int i = 0; i < n; i++)
            {
                var r = g.runners[i];
                if (r.finishT >= 0) continue;
                // sang đoạn mới: bứt tốc / bị húc bắt đầu ở đầu đoạn
                while (r.key < r.keyT.Length - 2 && t >= r.keyT[r.key + 1])
                {
                    r.key++;
                    byte kind = r.keyKind[r.key + 1];
                    if (kind == Surge)
                    {
                        r.gustUntil = r.keyT[r.key] + r.keyDur[r.key + 1];
                        g.events.Add(new RaceEvent { t = g.t, a = i, b = -1, kind = RaceEv.Gust });
                    }
                    else if (kind == Stun)
                    {
                        r.stunUntil = r.keyT[r.key] + r.keyDur[r.key + 1];
                        r.stuns++;
                        int by = Nearest(g, i);
                        if (by >= 0) g.runners[by].hits++;
                        g.events.Add(new RaceEvent { t = g.t, a = by, b = i, kind = RaceEv.Hit });
                    }
                }
                double np = Math.Max(r.pos, g.pace * t + Offset(g, r, t)); // không bao giờ lùi
                if (t >= r.finishAt)
                {
                    np = len;
                    r.finishT = r.finishAt;
                    g.events.Add(new RaceEvent { t = g.t, a = i, b = -1, kind = RaceEv.Finish });
                }
                else np = Math.Min(np, len - 0.02); // chưa tới giờ thì chưa chạm vạch: hạng về đích luôn đúng kịch bản
                r.speed = (np - r.pos) / Dt;
                r.pos = np;
            }
            g.t = t;
            if (g.runners.All(r => r.finishT >= 0) || g.t > 120) g.done = true;
        }

        // con gần nhất còn đang chạy và không choáng (kẻ húc); −1 nếu không có
        static int Nearest(RaceGame g, int i)
        {
            int best = -1;
            double bestD = double.MaxValue;
            for (int j = 0; j < g.runners.Count; j++)
            {
                var o = g.runners[j];
                if (j == i || o.finishT >= 0 || o.Stunned(g.t)) continue;
                double d = Math.Abs(o.pos - g.runners[i].pos);
                if (d < bestD) { bestD = d; best = j; }
            }
            return best;
        }

        // chạy hết
        public static void Run(RaceConfig c, RaceGame g)
        {
            int guard = 0;
            while (!g.done && guard++ < 100000) Step(c, g);
        }

        // chưa về đích xếp sau, theo quãng đã chạy
        public static List<int> Order(RaceGame g) =>
            Enumerable.Range(0, g.runners.Count).OrderBy(i => g.runners[i].finishT < 0 ? 1 : 0)
                .ThenBy(i => g.runners[i].finishT < 0 ? -g.runners[i].pos : g.runners[i].finishT).ThenBy(i => i).ToList();

        public static int PlaceOf(RaceGame g) => Order(g).IndexOf(g.PlayerIndex);

        // bi nhận về: cược × pay[hạng]; phần lời (trên tiền cược) nhân mult (Lễ Hội Đua)
        public static int Payout(RaceConfig c, int bet, int place, double mult = 1)
        {
            double k = place >= 0 && place < c.pay.Length ? c.pay[place] : 0;
            if (k <= 0 || bet <= 0) return 0;
            return (int)Math.Round(bet * (k > 1 ? 1 + (k - 1) * mult : k));
        }

        // ---------- trên bản lưu ----------

        public static bool CupOpen(SaveData s, GameData d, int cup) => cup >= 0 && cup < Casino.C(d).race.cups.Count && s.level >= Casino.C(d).race.cups[cup].level;

        // hạng cúp của tuần: hạng cao nhất đã mở theo cấp (điểm cúp và quà tuần tính cho hạng này)
        public static int WeekCup(SaveData s, GameData d)
        {
            int cup = 0;
            for (int i = 0; i < Casino.C(d).race.cups.Count; i++)
                if (CupOpen(s, d, i)) cup = i;
            return cup;
        }

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

        // Đặt cược và bắt đầu đua. bet > 0: cần còn lượt hôm nay, betMin..betMax, đủ bi (trừ ngay). bet = 0: đua tập, không tốn lượt,
        // không thưởng. why khác null nếu không đua được.
        public static RaceGame Start(SaveData s, GameData d, IList<string> lineup, int pick, int bet, double now, Rng rng, out string why)
        {
            why = null;
            var c = Casino.C(d).race;
            if (!Casino.Unlocked(s, d, Casino.Race)) { why = Casino.Need(s, d, Casino.Race); return null; }
            if (lineup == null || lineup.Count < 2 || pick < 0 || pick >= lineup.Count) { why = Loc.T("Chọn một tướng để đặt cược"); return null; }
            if (bet > 0)
            {
                if (Casino.PlaysLeft(s, d, Casino.Race, now) <= 0) { why = Loc.T("Hết lượt hôm nay"); return null; }
                if (bet < c.betMin || bet > c.betMax) { why = Loc.F("Đặt từ {0} tới {1} bi", c.betMin, c.betMax); return null; }
                if (!Casino.Spend(s, bet)) { why = Loc.T("Không đủ bi"); return null; }
                Casino.UsePlay(s, d, Casino.Race, now);
            }
            return Setup(d, c, lineup, pick, bet, Casino.Today(now), (uint)(rng.Next() * uint.MaxValue));
        }

        // đua xong: trả thưởng theo hạng (phần lời × Lễ Hội Đua), điểm cúp tuần, nhiệm vụ quán trọ
        public static RaceResult Finish(SaveData s, GameData d, RaceGame g, double now)
        {
            var c = Casino.C(d).race;
            var res = new RaceResult { place = PlaceOf(g), runners = g.runners.Count };
            if (!g.done) return res;
            Casino.Track(s, d, "race", 1, now);
            if (res.place < 3) Casino.Track(s, d, "race_top3", 1, now);
            if (g.bet <= 0) return res; // đua tập
            RollWeek(s, d, now);
            var st = Casino.Of(s);
            int cup = WeekCup(s, d);
            res.balls = Payout(c, g.bet, res.place, Casino.RaceMult(d, now));
            Casino.Win(s, d, res.balls, now);
            res.points = res.place < c.points.Length ? c.points[res.place] : 0;
            if (cup < st.cupPts.Length) st.cupPts[cup] = Math.Min(c.weekPts, st.cupPts[cup] + res.points);
            res.weekReady = WeekReady(s, d, cup, now);
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
