// sim.exe pop <bộ số> <từ> <tới> [ngày=30] [simN=6]   : chạy người chơi ảo id trong [từ, tới), ghi res/<bộ số>/p<id>.json
// sim.exe time                                        : đo ProgressSim sẵn có (đối chiếu)
// 300 người = 3 mức chơi × 5 nhóm tiền × 2 (không ra đảo / có ra đảo) × 10 người. Mỗi ô 10 người khác hạt giống; cặp "không đảo / có đảo"
// dùng chung hạt giống để so trực tiếp tác động của đảo Casino.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;

static class Program
{
    static string R(string set, string f) => File.ReadAllText(Path.Combine("data", set, f));

    public static GameData Load(string set)
    {
        var d = GameData.FromJson(R(set, "heroes.json"), R(set, "cards.json"), R(set, "zones.json"), R(set, "stages.json"), R(set, "balance.json"));
        foreach (var e in d.Validate()) Console.WriteLine("LOI du lieu: " + e);
        foreach (var e in d.Cfg.casino.Validate(d)) Console.WriteLine("LOI casino: " + e);
        return d;
    }

    public static readonly string[] Eng = { "chăm", "vừa", "ít" };
    public static readonly string[] Mon = { "F0 không QC", "FA xem QC", "P1 chi ít", "P2 chi vừa", "P3 chi lớn" };

    public static Persona Make(int id)
    {
        int r = id % 10, c = id / 10 % 2, m = id / 20 % 5, e = id / 100;
        var p = new Persona { id = id, eng = Eng[e], mon = Mon[m] };
        switch (e)
        {
            case 0: p.sessions = 6; p.battles = 5; p.skill = 0.18; p.dayProb = 1; break;
            case 1: p.sessions = 3; p.battles = 3; p.skill = 0.12; p.dayProb = 0.95; break;
            default: p.sessions = 1; p.battles = 2; p.skill = 0.08; p.dayProb = 0.8; break;
        }
        p.skill += (r % 5 - 2) * 0.015;
        switch (m)
        {
            case 0: break;
            case 1:
                // xem ít / xem nhiều xen kẽ theo r chẵn lẻ (không trùng với cách chia đảo thận trọng r < 5 / máu me r >= 5)
                if (r % 2 == 0) { p.adRate = 0.5; p.adCap = 6; p.mon += " (ít)"; }
                else { p.adRate = 0.95; p.adCap = 25; p.mon += " (nhiều)"; }
                break;
            case 2: p.adRate = 0.7; p.adCap = 10; p.spend = 1; p.budget = 15; break;
            case 3: p.adRate = 0.8; p.adCap = 15; p.spend = 2; p.budget = 80; break;
            case 4: p.adRate = 0.5; p.adCap = 10; p.spend = 3; p.budget = 600; break;
        }
        p.casino = c == 0 ? 0 : r < 5 ? 1 : 2;
        p.cas = p.casino == 0 ? "không ra đảo" : p.casino == 1 ? "đảo thận trọng" : "đảo máu me";
        p.seed = (uint)(1000003 * (e * 50 + m * 10 + r) + 12345);
        p.startShift = (r + m * 3) % 14;
        return p;
    }

    static string Num(double v) => v == Math.Floor(v) && Math.Abs(v) < 1e15 ? ((long)v).ToString(CultureInfo.InvariantCulture) : v.ToString("0.###", CultureInfo.InvariantCulture);
    static string Str(string s) => "\"" + s.Replace("\\", "\\\\").Replace("\"", "\\\"") + "\"";
    static string Map(SortedDictionary<string, double> m) => "{" + string.Join(",", m.Select(kv => Str(kv.Key) + ":" + Num(kv.Value))) + "}";
    static string Arr(IEnumerable<int> a) => "[" + string.Join(",", a) + "]";
    static string Arr(IEnumerable<double> a) => "[" + string.Join(",", a.Select(Num)) + "]";

    static string Json(Persona p, EconSim e, double sec, int cacheN)
    {
        var sb = new StringBuilder();
        var s = e.Save;
        var L = e.L;
        sb.Append("{");
        sb.Append($"\"id\":{p.id},\"eng\":{Str(p.eng)},\"mon\":{Str(p.mon)},\"cas\":{Str(p.cas)},\"spend\":{p.spend},\"casino\":{p.casino},");
        sb.Append($"\"sessions\":{p.sessions},\"battles\":{p.battles},\"adCap\":{p.adCap},\"starter\":{Str(s.starter)},");
        sb.Append($"\"finishedDay\":{e.finishedDay},\"maxLevelDay\":{e.maxLevelDay},\"brokenDay\":{e.brokenDay},\"stoppedDay\":{e.stoppedDay},\"timedOut\":{(e.timedOut ? "true" : "false")},\"sec\":{Num(sec)},\"cache\":{cacheN},");
        sb.Append($"\"level\":{Arr(e.level)},\"cleared\":{Arr(e.cleared)},\"zonesDone\":{Arr(e.zonesDone)},\"owned\":{Arr(e.owned)},\"stars\":{Arr(e.stars)},");
        sb.Append($"\"ballsHeld\":{Arr(e.ballsHeld)},\"power\":{Arr(e.power)},\"adsCum\":{Arr(e.adsCum)},\"sessionsCum\":{Arr(e.sessionsCum)},");
        sb.Append($"\"usdCum\":{Arr(e.usdCum)},\"droppedCum\":{Arr(e.droppedCum)},\"ballsInCum\":{Arr(e.ballsInCum)},\"shardsCum\":{Arr(e.shardsCum)},");
        sb.Append($"\"evoLeft\":{s.evoStones},\"stonesLeft\":{s.potentialStones},\"crystalsLeft\":{s.potentialCrystals},");
        sb.Append($"\"heroes\":{{{string.Join(",", s.heroes.Where(kv => kv.Value.owned).Select(kv => Str(kv.Key) + ":" + kv.Value.star))}}},");
        sb.Append($"\"ballsIn\":{Map(L.ballsIn)},\"ballsOut\":{Map(L.ballsOut)},\"shards\":{Map(L.shards)},\"evo\":{Map(L.evo)},\"stones\":{Map(L.stones)},");
        sb.Append($"\"crystals\":{Map(L.crystals)},\"copies\":{Map(L.copies)},\"exp\":{Map(L.exp)},\"usd\":{Map(L.usd)},\"iapValue\":{Map(L.iapValue)},");
        sb.Append($"\"ads\":{Map(L.ads)},\"count\":{Map(L.count)},");
        sb.Append("\"snap\":{" + string.Join(",", e.snaps.Select(kv => "\"" + kv.Key + "\":{" + string.Join(",", kv.Value.Select(x => Str(x.Key) + ":" + Map(x.Value))) + "}")) + "}");
        sb.Append("}");
        return sb.ToString();
    }

    static int Main(string[] args)
    {
        Console.OutputEncoding = Encoding.UTF8;
        string what = args.Length > 0 ? args[0] : "time";
        if (what == "time")
        {
            var d = Load("goc");
            var sw = Stopwatch.StartNew();
            var cache = new Dictionary<string, double>();
            foreach (var p in ProgressSim.DefaultProfiles())
            {
                var rep = ProgressSim.Run(d, p, 30, 1, 8, cache);
                Console.WriteLine($"{p.name}: cấp {rep.level[7]} / {rep.level[14]} / {rep.level[30]} (ngày 7/14/30), ải {rep.cleared[7]} / {rep.cleared[14]} / {rep.cleared[30]}, " +
                                  $"trận {rep.battles} thắng {rep.wins}, bi thả {rep.ballsDropped} (ải {rep.ballsFromStages}, cây {rep.ballsFromTrees}, trại {rep.ballsFromFarm}), " +
                                  $"cache {cache.Count}, {sw.Elapsed.TotalSeconds:F1}s");
            }
            return 0;
        }
        if (what == "jump")
        {
            // sim.exe jump <bộ số>: Gói Vượt Mốc dựng ra thế nào theo cấp người chơi và mốc tướng (giá, món, giá trị)
            var d = Load(args.Length > 1 ? args[1] : "goc");
            var c = d.Cfg.shop;
            var ms = Offers.MilestoneStages(d, Elem.Thuy);
            foreach (int lv in new[] { 15, 40, 70, 100, 160 })
                foreach (int moc in new[] { 6, 7, 9, 10 })
                {
                    var s = SaveData.New(d, 0);
                    Tutorial.Skip(s);
                    s.level = lv;
                    var h = d.Hero(Teams.StageLead(ms[moc - 1], d).hero);
                    var o = Offers.Build(s, d, "jump", h.id, 1e12, new Rng(1));
                    Console.WriteLine($"cấp {lv,3} | mốc {moc,2} {h.name} ({h.rarity}) | {o.price,6:F2} USD | ×{Shop.OfferMult(s, d, o):F1} | " +
                                      string.Join(", ", o.items.Select(it => it.k + " " + it.n)));
                }
            return 0;
        }
        if (what == "dbg")
        {
            // sim.exe dbg <bộ số> <đảo>: tỉ lệ thắng (máy tự đánh, 40 trận) của từng tướng mốc ở vài ải, theo cấp người chơi
            string set = args[1];
            var d = Load(set);
            EconSim.Rules = SimRules.Read(R(set, "balance.json"));
            if (EconSim.Rules.mocPower != null)
            {
                HeroStats.HeroMult = new Dictionary<string, double>();
                foreach (var kv in EconSim.Moc(d))
                    for (int k = 0; k < kv.Value.Count && k < EconSim.Rules.mocPower.Length; k++)
                        HeroStats.HeroMult[kv.Value[k]] = EconSim.Rules.mocPower[k];
            }
            var zone = d.Zones.First(z => Keys.Of(z.id) == args[2]);
            var moc = EconSim.Moc(d)[zone.id];
            foreach (int idx in new[] { 12, 25, 37, 40, 52 })
            {
                var st = d.ZoneStages(zone.id).First(x => x.idx == idx);
                int elv = st.enemies.Max(e => e.level);
                Console.WriteLine($"Ải {idx} ({st.kind}, địch cấp {elv}, buff {st.enemies[0].buff:F2}, {st.enemies.Count} địch):");
                foreach (int k in new[] { 1, 3, 6, 9, 10 })
                {
                    var line = new List<string>();
                    foreach (int dl in new[] { -30, -20, -10, 0 })
                    {
                        int lv = Math.Max(1, elv + dl);
                        var sv = Sim.Setup(d, new[] { moc[k - 1] }, lv, 6, 3);
                        line.Add($"cấp {lv}: {Sim.Stage(d, sv, st, 40).WinRate:P0}");
                    }
                    Console.WriteLine($"   mốc {k} {moc[k - 1]} (6 sao, thẻ 3): " + string.Join(" | ", line));
                }
            }
            return 0;
        }
        if (what == "pop")
        {
            string set = args[1];
            int from = int.Parse(args[2]), to = int.Parse(args[3]);
            int days = args.Length > 4 ? int.Parse(args[4]) : 30, simN = args.Length > 5 ? int.Parse(args[5]) : 6;
            var d = Load(set);
            EconSim.Rules = SimRules.Read(R(set, "balance.json"));
            if (EconSim.Rules.mocPower != null)
            {
                HeroStats.HeroMult = new Dictionary<string, double>();
                foreach (var kv in EconSim.Moc(d))
                    for (int k = 0; k < kv.Value.Count && k < EconSim.Rules.mocPower.Length; k++)
                        HeroStats.HeroMult[kv.Value[k]] = EconSim.Rules.mocPower[k];
            }
            Casino.TestAllBooths = false;
            string dir = Path.Combine("res", set);
            Directory.CreateDirectory(dir);
            var cache = new Dictionary<string, double>();
            for (int id = from; id < to; id++)
            {
                var p = Make(id);
                var sw = Stopwatch.StartNew();
                var e = new EconSim(d, p, days, simN, cache);
                e.Run();
                string outF = Path.Combine(dir, $"p{id:000}.json");
                File.WriteAllText(outF + ".tmp", Json(p, e, sw.Elapsed.TotalSeconds, cache.Count), new UTF8Encoding(false));
                if (File.Exists(outF)) File.Delete(outF);
                File.Move(outF + ".tmp", outF);
                Console.WriteLine($"{set} #{id} {p.eng} | {p.mon} | {p.cas}: cấp {e.level[days]}, ải {e.cleared[days]}, ${e.usdCum[days]:F2}, {sw.Elapsed.TotalSeconds:F0}s");
                if (Environment.GetEnvironmentVariable("PROF") != null) Console.WriteLine("   " + string.Join(", ", EconSim.ProfT.Select(kv => $"{kv.Key} {kv.Value:F1}s")));
                if (cache.Count > 400000) cache.Clear();
            }
            return 0;
        }
        return 0;
    }
}
