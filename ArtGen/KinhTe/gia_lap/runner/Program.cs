using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using PokiClash.Core;

static class Program
{
    static string R(string set, string f) => File.ReadAllText(Path.Combine("data", set, f));

    public static GameData Load(string set)
    {
        var d = GameData.FromJson(R(set, "heroes.json"), R(set, "cards.json"), R(set, "zones.json"), R(set, "stages.json"), R(set, "balance.json"));
        foreach (var e in d.Validate()) Console.WriteLine("LOI du lieu: " + e);
        return d;
    }

    static int Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
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
        return 0;
    }
}
