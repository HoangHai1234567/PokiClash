// Báo cáo dung lượng sau mỗi lần build (bộ build PokiBuild và nút Build của cửa sổ Build Profiles, người dùng 2026-11-21): ghi
// Build/BaoCao/<tên gói>.txt (đọc) và .json (để lần sau so).
//  - Gói ra (APK, AAB): các phần nặng nhất đã nén, đọc thẳng file zip.
//  - Tài nguyên theo nhóm và theo loại (cỡ trong gói dữ liệu, trước nén LZ4HC). Tướng .atomik tách atlas với dữ liệu khoá, lưới.
//  - So với lần build trước cùng nền: nhóm nào phình hay gọn đi, asset nào mới nặng thêm.
//  - Ngân sách Android (người dùng 2026-11-03: bản Android 60-70 MB): vượt thì báo vàng trong Console.
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class BuildSizeReport
    {
        public const float AndroidBudgetMB = 70;
        public static string Dir => Path.Combine(PokiBuild.OutDir, "BaoCao");

        [Serializable]
        sealed class Row
        {
            public string k;
            public long b;
            public int n;
        }

        [Serializable]
        sealed class Snapshot
        {
            public string name, platform, time, how;
            public long output, assets;
            public List<Row> groups = new List<Row>();
            public List<Row> items = new List<Row>(); // asset từ 8 KB trở lên
        }

        static string MB(long b) => (b / 1048576.0).ToString("0.00") + " MB";

        static long Get(Dictionary<string, long> d, string k) => d.TryGetValue(k, out var v) ? v : 0;

        static string Signed(long b) => (b >= 0 ? "+" : "−") + MB(Math.Abs(b));

        // Nhóm của một phần trong gói dữ liệu (đường dẫn nguồn + kiểu đối tượng).
        public static string Group(string src, Type type)
        {
            if (string.IsNullOrEmpty(src)) return "(không rõ nguồn)";
            if (src.EndsWith(".atomik"))
                return type == typeof(Texture2D) ? "Tướng .atomik: atlas" : type == typeof(Material) ? "Tướng .atomik: material" : "Tướng .atomik: khoá, lưới";
            if (src.EndsWith("_portrait.png")) return "Tướng: chân dung";
            if (src.Contains("/Heroes/Resources/")) return "Tướng: ảnh khác";
            var parts = src.Split('/');
            if (src.StartsWith("Assets/03 Art/Baked/") && parts.Length > 4) return "Baked/" + parts[3];
            if (src.StartsWith("Assets/03 Art/Fx/") && parts.Length > 4) return "Fx/" + parts[3];
            if (src.StartsWith("Assets/03 Art/") && parts.Length > 3) return parts[2];
            if (src.StartsWith("Assets/04 Prefabs/")) return "Prefab";
            if (src.StartsWith("Assets/00 Scenes/")) return "Scene";
            if (src.StartsWith("Assets/02 Data/")) return "Dữ liệu (02 Data)";
            if (src.StartsWith("Assets/") && parts.Length > 2) return parts[1];
            if (src.StartsWith("Packages/") && parts.Length > 1) return "Package " + parts[1];
            if (src.Contains("unity_builtin_extra") || src.Contains("unity default resources") || src.StartsWith("Built-in")) return "Unity có sẵn";
            return src.Length > 40 ? src.Substring(0, 40) : src;
        }

        public static void Write(BuildReport report, List<BuildExclude.Item> excluded, string how)
        {
            if (report == null) return;
            var s = report.summary;
            if (s.result != BuildResult.Succeeded)
            {
                Debug.LogWarning($"[Build] Kết quả {s.result}: không ghi báo cáo dung lượng.");
                return;
            }
            string outPath = s.outputPath;
            string name = Path.GetFileNameWithoutExtension(outPath.TrimEnd('/', '\\'));
            var snap = new Snapshot { name = name, platform = s.platform.ToString(), time = DateTime.Now.ToString("yyyy-MM-dd HH:mm"), how = how };
            snap.output = File.Exists(outPath) ? new FileInfo(outPath).Length
                : Directory.Exists(outPath) ? new DirectoryInfo(outPath).EnumerateFiles("*", SearchOption.AllDirectories).Sum(f => f.Length) : (long)s.totalSize;

            var groups = new Dictionary<string, Row>();
            var types = new Dictionary<string, long>();
            var items = new Dictionary<string, long>();
            long loose = 0; // ảnh nguồn của sprite atlas vào gói thành ảnh rời (atlas không gom được)
            int looseN = 0;
            foreach (var pa in report.packedAssets)
                foreach (var c in pa.contents)
                {
                    long b = (long)c.packedSize;
                    if (c.type == typeof(Texture2D) && !string.IsNullOrEmpty(c.sourceAssetPath) && AtlasMenu.InAtlas(c.sourceAssetPath))
                    {
                        loose += b;
                        looseN++;
                    }
                    string g = Group(c.sourceAssetPath, c.type);
                    if (!groups.TryGetValue(g, out var r)) groups[g] = r = new Row { k = g };
                    r.b += b;
                    r.n++;
                    string t = c.type != null ? c.type.Name : "?";
                    types[t] = Get(types, t) + b;
                    string src = string.IsNullOrEmpty(c.sourceAssetPath) ? "(không rõ nguồn)" : c.sourceAssetPath;
                    items[src] = Get(items, src) + b;
                }
            snap.assets = groups.Values.Sum(r => r.b);
            snap.groups = groups.Values.OrderByDescending(r => r.b).ToList();
            snap.items = items.Where(kv => kv.Value >= 8192).OrderByDescending(kv => kv.Value).Select(kv => new Row { k = kv.Key, b = kv.Value }).ToList();

            var prev = Previous(snap.platform, name);
            var sb = new StringBuilder();
            sb.AppendLine($"{name} ({snap.platform}, {how}) lúc {snap.time}, build {s.totalTime.TotalMinutes:0.0} phút");
            // kiểu nén gói dữ liệu: LZ4 thường to hơn LZ4HC ~5% (bản 0.5.1 nút Build bị LZ4, 2026-11-23)
            // có cờ LZ4 là Unity nén LZ4 thường, kể cả khi có thêm cờ LZ4HC (đo trên khối của data.unity3d bản 0.5.1)
            bool hc = (s.options & BuildOptions.CompressWithLz4HC) != 0 && (s.options & BuildOptions.CompressWithLz4) == 0;
            var comp = hc ? "LZ4HC" : (s.options & BuildOptions.CompressWithLz4) != 0 ? "LZ4 (chưa phải LZ4HC!)" : "không nén";
            sb.AppendLine($"Nén gói dữ liệu: {comp}");
            if (!hc && (s.platform == BuildTarget.Android || s.platform == BuildTarget.iOS))
                Debug.LogWarning($"[Build] {name}: gói dữ liệu nén {comp}, không phải LZ4HC (to hơn vài MB). Build qua menu PokiClash/Build.");
            // vụ atlas hạt 2026-11-23: atlas nhập hỏng, 1458 ảnh hạt vào gói rời RGBA32 (443 MB trước nén) mà không ai thấy qua hai bản
            if (loose > 1048576)
            {
                sb.AppendLine($"ẢNH NGUỒN CỦA SPRITE ATLAS VÀO GÓI RỜI: {looseN} ảnh, {MB(loose)} trước nén (atlas không gom được: nhập hỏng, " +
                              "hoặc ảnh bị trỏ thẳng dạng Texture2D). Nhập lại file .spriteatlasv2 rồi build lại.");
                Debug.LogError($"[Build] {name}: {looseN} ảnh nguồn của sprite atlas vào gói rời ({MB(loose)} trước nén). Xem báo cáo dung lượng.");
            }
            sb.AppendLine($"Gói ra: {MB(snap.output)}  {outPath}" + (prev != null ? $"  (lần trước {prev.name}: {MB(prev.output)}, {Signed(snap.output - prev.output)})" : ""));
            bool android = s.platform == BuildTarget.Android;
            if (android && snap.output > AndroidBudgetMB * 1048576)
                sb.AppendLine($"VƯỢT NGÂN SÁCH {AndroidBudgetMB} MB thêm {MB(snap.output - (long)(AndroidBudgetMB * 1048576))}");
            if (File.Exists(outPath) && (outPath.EndsWith(".apk") || outPath.EndsWith(".aab")))
            {
                sb.AppendLine("Phần nặng nhất trong gói (đã nén):");
                using var zip = ZipFile.OpenRead(outPath);
                foreach (var e in zip.Entries.OrderByDescending(e => e.CompressedLength).Take(10))
                    sb.AppendLine($"  {MB(e.CompressedLength),10}  (giải nén {MB(e.Length)})  {e.FullName}");
                // AAB: mỗi module / asset pack là một thư mục gốc. Bản cài = base + gói install-time; gói tải sau (GD_Claude/27) tính riêng.
                // Cỡ đã nén trong file .aab, gần với cỡ tải về Play tính (Play nén lại khi giao).
                if (outPath.EndsWith(".aab"))
                {
                    sb.AppendLine("Theo module (đã nén trong .aab):");
                    foreach (var g in zip.Entries.GroupBy(e => e.FullName.Split('/')[0]).OrderByDescending(g => g.Sum(e => e.CompressedLength)))
                    {
                        string kindName = g.Key == "base" ? "bản cài" : g.Key.StartsWith("noi_dung_") ? "tải sau (fast-follow)" :
                            g.Key.StartsWith("Unity") || g.Key == "AddressablesAssetPack" ? "bản cài (install-time)" : "";
                        sb.AppendLine($"  {MB(g.Sum(e => e.CompressedLength)),10}  {g.Key}  {kindName}");
                    }
                    long install = zip.Entries.Where(e => { var k = e.FullName.Split('/')[0]; return !k.StartsWith("noi_dung_") && k != "BUNDLE-METADATA" && k != "META-INF"; })
                        .Sum(e => e.CompressedLength);
                    long later = zip.Entries.Where(e => e.FullName.StartsWith("noi_dung_")).Sum(e => e.CompressedLength);
                    sb.AppendLine($"Bản cài ~{MB(install)}, 5 gói tải sau {MB(later)}");
                }
            }
            if (excluded != null && excluded.Count > 0)
            {
                sb.AppendLine($"Bỏ khỏi bản build: {excluded.Count} thư mục ({excluded[0].why}...)");
                sb.AppendLine("  " + string.Join(", ", excluded.Select(e => Path.GetFileName(e.path))));
            }
            sb.AppendLine($"Tài nguyên trong gói dữ liệu (trước nén): {MB(snap.assets)}" + (prev != null ? $" ({Signed(snap.assets - prev.assets)})" : ""));
            sb.AppendLine("Theo nhóm:");
            var prevGroups = prev?.groups.ToDictionary(r => r.k, r => r.b);
            foreach (var r in snap.groups.Take(30))
            {
                string d = prevGroups != null ? "  " + Signed(r.b - Get(prevGroups, r.k)) : "";
                sb.AppendLine($"  {MB(r.b),10} {r.n,6}  {r.k}{d}");
            }
            sb.AppendLine("Theo loại:");
            foreach (var kv in types.OrderByDescending(kv => kv.Value).Take(10)) sb.AppendLine($"  {MB(kv.Value),10}  {kv.Key}");
            if (prev != null)
            {
                var pi = prev.items.ToDictionary(r => r.k, r => r.b);
                var grown = snap.items.Select(r => (r.k, d: r.b - Get(pi, r.k))).Where(x => x.d >= 200 * 1024).OrderByDescending(x => x.d).Take(15).ToList();
                var cur = snap.items.ToDictionary(r => r.k, r => r.b);
                var gone = prev.items.Where(r => !cur.ContainsKey(r.k) && r.b >= 200 * 1024).OrderByDescending(r => r.b).Take(15).ToList();
                if (grown.Count > 0)
                {
                    sb.AppendLine("Mới hoặc nặng thêm so với lần trước:");
                    foreach (var x in grown) sb.AppendLine($"  {Signed(x.d),10}  {x.k}");
                }
                if (gone.Count > 0)
                {
                    sb.AppendLine("Không còn trong bản build:");
                    foreach (var r in gone) sb.AppendLine($"  {MB(r.b),10}  {r.k}");
                }
            }
            sb.AppendLine("Nặng nhất:");
            foreach (var r in snap.items.Take(40)) sb.AppendLine($"  {MB(r.b),10}  {r.k}");

            Directory.CreateDirectory(Dir);
            string txt = Path.Combine(Dir, name + ".txt");
            File.WriteAllText(txt, sb.ToString());
            File.WriteAllText(Path.Combine(Dir, name + ".json"), JsonUtility.ToJson(snap));
            string line = $"[Build] {name}: gói {MB(snap.output)}" + (prev != null ? $" ({Signed(snap.output - prev.output)} so với {prev.name})" : "") +
                          $", tài nguyên {MB(snap.assets)}" + (excluded?.Count > 0 ? $", bỏ {excluded.Count} thư mục thừa" : "") + $". Báo cáo: {txt}";
            if (android && snap.output > AndroidBudgetMB * 1048576) Debug.LogWarning(line + $" — vượt ngân sách {AndroidBudgetMB} MB");
            else Debug.Log(line);
        }

        // báo cáo gần nhất cùng nền (trừ chính lần này)
        static Snapshot Previous(string platform, string except)
        {
            if (!Directory.Exists(Dir)) return null;
            foreach (var f in new DirectoryInfo(Dir).GetFiles("*.json").OrderByDescending(f => f.LastWriteTimeUtc))
            {
                if (Path.GetFileNameWithoutExtension(f.Name) == except) continue;
                try
                {
                    var s = JsonUtility.FromJson<Snapshot>(File.ReadAllText(f.FullName));
                    if (s != null && s.platform == platform) return s;
                }
                catch (Exception) { /* file hỏng: bỏ qua */ }
            }
            return null;
        }

        // Ước phần các thư mục sắp bỏ đã chiếm trong một bản build (byte trong gói dữ liệu, trước nén).
        public static long SizeIn(BuildReport report, IEnumerable<string> dirs)
        {
            if (report == null) return 0;
            var pre = dirs.Select(d => d + "/").ToArray();
            long sum = 0;
            foreach (var pa in report.packedAssets)
                foreach (var c in pa.contents)
                    if (!string.IsNullOrEmpty(c.sourceAssetPath) && pre.Any(c.sourceAssetPath.StartsWith))
                        sum += (long)c.packedSize;
            return sum;
        }
    }
}
