// Đo cân bằng 5 tướng khởi đầu (GD_Claude/15_TuongKhoiDau.md, mục 3). Chạy trong Editor, không cần Play, dữ liệu đọc thẳng từ
// Assets/02 Data/Json; kết quả ghi Logs/CanBang/tuong_khoi_dau.md (bảng trận) và tuong_khoi_dau_tien_do.md (tiến độ).
// - Vòng tròn: 5 tướng đấu tay đôi từng cặp ở cấp 1, 4, 8.
// - Đảo Thủy: 70 ải × 5 lựa chọn theo luật mới (ô 2 ở ải 3, quà theo lựa chọn, tướng đồng hành), kèm luật cũ (1 ô, quà Võ Sư) để so.
// - Các đảo 8 ải: tướng khởi đầu đánh một mình, có và không có luật tướng đồng hành.
// - Tiến độ: 30 ngày × 3 kiểu người chơi × 5 lựa chọn (menu riêng, chạy lâu hơn).
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class StarterBalanceMenu
    {
        static string DataDir => Path.Combine(Application.dataPath, "02 Data", "Json");
        static string LogDir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Logs/CanBang"));

        // thứ tự kiểu ải như bảng ở 14_HeThongAi.md
        static readonly string[] KeyOrder = { "hero", "minion", "buff", "group", "elite", "mini", "pair", "gate", "boss" };

        static GameData Load()
        {
            string R(string f) => File.ReadAllText(Path.Combine(DataDir, f));
            return GameData.FromJson(R("heroes.json"), R("cards.json"), R("zones.json"), R("stages.json"), R("balance.json"));
        }

        static string KeyName(string k) =>
            k == "mini" ? "Mini boss" : k == "boss" ? "Boss" : k == "normal" ? "Ải thường" : Islands.TagName(Keys.ToStageTag(k));

        static string Pct(double v) => $"{Math.Round(v * 100)}%";

        static void Bar(string title, string info, float t)
        {
            if (EditorUtility.DisplayCancelableProgressBar(title, info, t)) throw new OperationCanceledException();
        }

        [MenuItem("PokiClash/Cân bằng nhanh/Tướng khởi đầu: vòng tròn, đảo Thủy, đảo bị khắc (ghi Logs, CanBang)", priority = 27)]
        static void Battles()
        {
            var d = Load();
            var t0 = DateTime.Now;
            var sb = new StringBuilder();
            var starters = d.Starters;
            string Name(string id) => d.Hero(id).name;
            try
            {
                // 1. vòng tròn
                const int duelN = 200;
                var levels = new[] { 1, 4, 8 };
                sb.Append($"# Tướng khởi đầu: số đo ({DateTime.Now:yyyy-MM-dd HH:mm})\n\n");
                sb.Append($"## Vòng tròn ({duelN} trận mỗi cặp, đổi bên, không có tướng đồng hành)\n\n");
                sb.Append("Ô là tỉ lệ thắng của tướng ở hàng trước tướng ở cột. Đạt khi trung bình 50% ± 5, cặp trung tính 40–60%.\n\n");
                foreach (var lv in levels)
                {
                    sb.Append($"Cấp {lv} (sao {Sim.StarAt(d.Cfg, lv)}):\n\n| | {string.Join(" | ", starters.Select(Name))} | Trung bình |\n|---|{string.Concat(starters.Select(_ => "---|"))}---|\n");
                    foreach (var a in starters)
                    {
                        Bar("Tướng khởi đầu", $"Vòng tròn cấp {lv}: {Name(a)}", 0.05f * Array.IndexOf(levels, lv));
                        var cells = starters.Select(b => a == b ? (double?)null : Sim.Duel(d, a, b, lv, duelN)).ToList();
                        var ha = d.Hero(a);
                        string Cell(string b, double? v)
                        {
                            if (v == null) return "–";
                            double m = Elements.Mult(ha.elem, d.Hero(b).elem);
                            return Pct(v.Value) + (m > 1 ? " (khắc)" : m < 1 ? " (bị khắc)" : "");
                        }
                        sb.Append($"| {Name(a)} | {string.Join(" | ", starters.Select((b, i) => Cell(b, cells[i])))} | {Pct(cells.Where(x => x != null).Average(x => x.Value))} |\n");
                    }
                    sb.Append("\n");
                }

                // 2. đảo Thủy 70 ải, luật mới và luật cũ
                const int n = 100;
                var rows = new Dictionary<(string, bool), List<Sim.StarterRow>>();
                int k = 0;
                foreach (var old in new[] { false, true })
                    foreach (var st in starters)
                    {
                        Bar("Tướng khởi đầu", $"Đảo Thủy {(old ? "luật cũ" : "luật mới")}: {Name(st)}", 0.15f + 0.6f * k++ / (2 * starters.Count));
                        rows[(st, old)] = Sim.StarterIsland(d, st, Elem.Thuy, n, old);
                    }
                foreach (var old in new[] { false, true })
                {
                    sb.Append(old
                        ? $"## Đảo Thủy, luật cũ để so ({n} trận mỗi ải): 1 ô suốt đảo, quà ải 3 luôn là Võ Sư, không có tướng đồng hành\n\n"
                        : $"## Đảo Thủy, luật mới ({n} trận mỗi ải): ô 2 mở ở ải 3, quà theo lựa chọn, tướng đồng hành\n\n");
                    sb.Append("Cấp bằng cấp địch cao nhất của ải, sao theo cấp, cấp thẻ bằng sao; đội chỉ gồm tướng khởi đầu và tướng tặng.\n\n");
                    sb.Append($"| Kiểu ải | {string.Join(" | ", starters.Select(Name))} | Chênh |\n|---|{string.Concat(starters.Select(_ => "---|"))}---|\n");
                    foreach (var key in KeyOrder)
                    {
                        var avg = starters.Select(st => rows[(st, old)].Where(r => Sim.StageKey(r.st) == key).Select(r => r.cell.WinRate).DefaultIfEmpty(-1).Average()).ToList();
                        if (avg.All(x => x < 0)) continue;
                        int cnt = rows[(starters[0], old)].Count(r => Sim.StageKey(r.st) == key);
                        sb.Append($"| {KeyName(key)} ({cnt} ải) | {string.Join(" | ", avg.Select(Pct))} | {Math.Round((avg.Max() - avg.Min()) * 100)} điểm |\n");
                    }
                    var all = starters.Select(st => rows[(st, old)].Average(r => r.cell.WinRate)).ToList();
                    sb.Append($"| **Cả đảo** | {string.Join(" | ", all.Select(Pct))} | {Math.Round((all.Max() - all.Min()) * 100)} điểm |\n\n");
                }
                sb.Append("Ải 1–5 từng lựa chọn (luật mới):\n\n| Ải | " + string.Join(" | ", starters.Select(Name)) + " |\n|---|" + string.Concat(starters.Select(_ => "---|")) + "\n");
                for (int i = 0; i < 5; i++)
                {
                    var st0 = rows[(starters[0], false)][i].st;
                    sb.Append($"| {st0.idx} {st0.name} ({string.Join(", ", st0.enemies.Select(e => Name(e.hero)))}) | " +
                              string.Join(" | ", starters.Select(st => $"{Pct(rows[(st, false)][i].cell.WinRate)} ({string.Join("+", rows[(st, false)][i].team.Select(Name))})")) + " |\n");
                }
                sb.Append("\n");

                // 3. các đảo 8 ải: tướng khởi đầu một mình, có và không có luật tướng đồng hành
                sb.Append($"## Các đảo khác: tướng khởi đầu đánh một mình ({n / 2} trận mỗi ải), không / có luật tướng đồng hành\n\n");
                sb.Append($"| Đảo | {string.Join(" | ", starters.Select(Name))} |\n|---|{string.Concat(starters.Select(_ => "---|"))}\n");
                foreach (var z in d.Zones.OrderBy(z => z.order).Where(z => z.id != Elem.Thuy))
                {
                    Bar("Tướng khởi đầu", $"Đảo {z.name}", 0.8f + 0.04f * z.order);
                    var cells = starters.Select(stId =>
                    {
                        double Avg(bool partner) => d.ZoneStages(z.id).Average(st =>
                        {
                            int lv = st.enemies.Max(e => e.level), star = Sim.StarAt(d.Cfg, lv);
                            return Sim.Stage(d, Sim.Setup(d, new[] { stId }, lv, star, star, partner ? stId : null), st, n / 2).WinRate;
                        });
                        double m = Elements.Mult(d.Hero(stId).elem, z.id), bad = Elements.Mult(z.id, d.Hero(stId).elem);
                        string tag = m > 1 ? " khắc" : bad > 1 ? " **bị khắc**" : "";
                        return $"{Pct(Avg(false))} / {Pct(Avg(true))}{tag}";
                    });
                    sb.Append($"| {z.name} | {string.Join(" | ", cells)} |\n");
                }

                Directory.CreateDirectory(LogDir);
                var path = Path.Combine(LogDir, "tuong_khoi_dau.md");
                File.WriteAllText(path, sb.ToString(), new UTF8Encoding(false));
                Debug.Log($"[Tướng khởi đầu] Xong trong {(DateTime.Now - t0).TotalSeconds:0} giây, ghi {path}\n{sb}");
            }
            catch (OperationCanceledException)
            {
                Debug.Log("[Tướng khởi đầu] Đã dừng.\n" + sb);
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        [MenuItem("PokiClash/Cân bằng nhanh/Tướng khởi đầu: tiến độ 30 ngày × 5 lựa chọn (ghi Logs, CanBang)", priority = 28)]
        static void Pace()
        {
            var d = Load();
            var t0 = DateTime.Now;
            var sb = new StringBuilder($"# Tướng khởi đầu: tiến độ 30 ngày ({DateTime.Now:yyyy-MM-dd HH:mm})\n\n");
            sb.Append("Đạt khi kiểu Vừa: ngày xong đảo Thủy chênh tối đa 1 ngày, số ải qua ở ngày 30 chênh tối đa 10%.\n\n");
            var cache = new Dictionary<string, double>();
            var profiles = ProgressSim.DefaultProfiles();
            try
            {
                foreach (var p in profiles)
                {
                    sb.Append($"## {p.name} ({p.sessions} lần × {p.battles} trận mỗi ngày)\n\n| Tướng | Xong Thủy | Xong Hỏa | Ải đã qua ngày 7 / 14 / 30 | Cấp ngày 7 / 14 / 30 | Bi ải |\n|---|---|---|---|---|---|\n");
                    var cleared = new List<int>();
                    var thuy = new List<int>();
                    foreach (var st in d.Starters)
                    {
                        Bar("Tướng khởi đầu: tiến độ", $"{p.name}: {d.Hero(st).name}",
                            (Array.IndexOf(profiles, p) * d.Starters.Count + d.Starters.IndexOf(st)) / (float)(profiles.Length * d.Starters.Count));
                        var r = ProgressSim.Run(d, p, 30, 1, 8, cache, null, st);
                        string Day(Elem z) => r.zoneDay[(int)z] < 0 ? "chưa" : "ngày " + r.zoneDay[(int)z];
                        sb.Append($"| {d.Hero(st).name} | {Day(Elem.Thuy)} | {Day(Elem.Hoa)} | {r.cleared[7]} / {r.cleared[14]} / {r.cleared[30]} | " +
                                  $"{r.level[7]} / {r.level[14]} / {r.level[30]} | {r.ballsFromStages} |\n");
                        cleared.Add(r.cleared[30]);
                        thuy.Add(r.zoneDay[(int)Elem.Thuy] < 0 ? 31 : r.zoneDay[(int)Elem.Thuy]);
                    }
                    sb.Append($"\nChênh: xong Thủy {thuy.Max() - thuy.Min()} ngày, ải qua ngày 30 {Math.Round(100.0 * (cleared.Max() - cleared.Min()) / Math.Max(1, cleared.Max()))}%.\n\n");
                }
                Directory.CreateDirectory(LogDir);
                var path = Path.Combine(LogDir, "tuong_khoi_dau_tien_do.md");
                File.WriteAllText(path, sb.ToString(), new UTF8Encoding(false));
                Debug.Log($"[Tướng khởi đầu] Tiến độ xong trong {(DateTime.Now - t0).TotalSeconds:0} giây, ghi {path}\n{sb}");
            }
            catch (OperationCanceledException)
            {
                Debug.Log("[Tướng khởi đầu] Tiến độ: đã dừng.\n" + sb);
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }
    }
}
