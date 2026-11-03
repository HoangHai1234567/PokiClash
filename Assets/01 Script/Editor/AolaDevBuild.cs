// ĐÃ THÔI DÙNG (2026-11-02): hình tướng nay nhập vào Assets thành prefab tướng (Editor/AolaImport), bản build mang theo như
// asset thường. Bước build giờ chỉ dọn bản chép cũ trong StreamingAssets; phần chép bên dưới để lại cho tới khi chủ dự án
// quyết xoá file này cùng AolaDevPack, AolaPngPack, PalettePng.
// Cũ: mang hình tướng aola vào bản build để xem trên máy thật (chủ dự án 2026-11-02: "để tất cả các tướng kể cả aola, đây là
// prototype thôi"). AllBuilds bật: mọi bản build đều mang; tắt (trước khi phát hành công khai): chỉ Development Build mang.
// Trước build (sau PreBuildCheck): chép mọi tướng có export/anim.json trong thư mục reskin
// (AolaImport.FindDir) vào Assets/StreamingAssets/PokiDev/reskin. Mỗi tướng gồm anim.json, portrait.png và đúng các hình anim.json
// trỏ tới (đường dẫn tương đối từ reskin/<tên>, như pet<id>_parts/chars hay reskin/<tên>/sprites), giữ nguyên cấu trúc.
// Hình chép vào được thu nhỏ về độ nét RenderTexture thật sự dùng (SizePlan; ma trận anim.json chỉnh theo, Rescale) rồi ghi
// PNG 256 màu (AolaPngPack, cache ở Library/PokiAolaPng): 262 MB gốc còn khoảng 25 MB, RAM trên máy giảm theo. Build Android
// thì anim.json ghi dạng anim.json.gz (APK để StreamingAssets không nén; AolaDevPack giải nén khi chép ra máy).
// Thêm stamp.txt để máy biết build mới. Sau build (và khi mở Editor, phòng build hỏng giữa chừng) xoá thư mục đó.
// Không mang thì chỉ cảnh báo là trên máy sẽ không có tướng. Lúc chạy: Game/Heroes/AolaDevPack.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public sealed class AolaDevBuild : IPreprocessBuildWithReport, IPostprocessBuildWithReport
    {
        public int callbackOrder => 10; // sau PreBuildCheck (0), để bước kiểm tra không thấy bản chép tạm

        // Thôi chép: hình đã nằm trong Assets, chép nữa thì bản build mang hai lần.
        public static readonly bool Enabled = false;

        static string Pack => Path.Combine(Application.dataPath, "StreamingAssets", AolaDevPack.Folder);

        public void OnPreprocessBuild(BuildReport report)
        {
            Clean();
            if (!Enabled) return;
            var src = AolaImport.FindDir();
            if (string.IsNullOrEmpty(src) || !Directory.Exists(src))
            {
                Debug.LogWarning("[Tướng aola] Không tìm thấy thư mục reskin (menu PokiClash/Tự tìm thư mục aola): bản build không có tướng.");
                return;
            }
            var files = Collect(src, out int heroes, out var missing);
            var plan = SizePlan(src);
            long bytes = 0, before = 0, px0 = 0, px1 = 0;
            int packed = 0, cached = 0;
            // APK để StreamingAssets không nén: hình thu nhỏ về cỡ cần và đổi sang PNG 256 màu (AolaPngPack), anim.json chỉnh ma
            // trận theo cỡ mới và gzip trên Android (máy giải nén khi chép ra)
            bool gz = report.summary.platform == BuildTarget.Android;
            var dst = Path.Combine(Pack, "reskin");
            var made = new Dictionary<string, (int w, int h, int nw, int nh)>(StringComparer.OrdinalIgnoreCase); // cỡ gốc → cỡ đã ghi
            try
            {
                // hình trước, anim.json sau (cần cỡ hình đã ghi)
                var order = files.Where(r => !IsJson(r)).Concat(files.Where(IsJson)).ToList();
                for (int i = 0; i < order.Count; i++)
                {
                    var rel = order[i];
                    var from = Path.GetFullPath(Path.Combine(src, rel));
                    var to = Path.Combine(dst, rel);
                    Directory.CreateDirectory(Path.GetDirectoryName(to));
                    before += new FileInfo(from).Length;
                    if (i % 40 == 0) EditorUtility.DisplayProgressBar("Nén hình tướng aola", rel, (float)i / order.Count);
                    if (rel.EndsWith(".png", StringComparison.OrdinalIgnoreCase))
                    {
                        AolaPngPack.Size(from, out int w, out int h);
                        int nw = -1, nh = -1;
                        if (plan.TryGetValue(from, out var want)) (nw, nh) = want;
                        var data = AolaPngPack.Get(from, nw, nh, out bool hit);
                        AolaPngPack.Size(data, out int ow, out int oh);
                        made[from] = (w, h, ow, oh);
                        px0 += (long)w * h;
                        px1 += (long)ow * oh;
                        File.WriteAllBytes(to, data);
                        packed++;
                        if (hit) cached++;
                    }
                    else if (IsJson(rel))
                    {
                        var json = Encoding.UTF8.GetBytes(Rescale(from, made));
                        if (gz)
                        {
                            to += AolaDevPack.Gz;
                            using (var o = File.Create(to))
                            using (var z = new System.IO.Compression.GZipStream(o, System.IO.Compression.CompressionLevel.Optimal))
                                z.Write(json, 0, json.Length);
                        }
                        else File.WriteAllBytes(to, json);
                    }
                    else File.Copy(from, to, true);
                    bytes += new FileInfo(to).Length;
                }
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
            File.WriteAllText(Path.Combine(Pack, AolaDevPack.Stamp), DateTime.Now.Ticks.ToString());
            foreach (var m in missing.Take(10)) Debug.LogWarning("[Tướng aola] Thiếu hình: " + m);
            Debug.Log($"[Tướng aola] Mang {heroes} tướng, {files.Count} file vào bản build: {before / 1e6:0.0} MB nén còn {bytes / 1e6:0.0} MB; " +
                      $"điểm ảnh {px0 / 1e6:0}M còn {px1 / 1e6:0}M ({packed} hình, {cached} lấy từ cache Library/PokiAolaPng; {missing.Count} hình thiếu).");
        }

        public void OnPostprocessBuild(BuildReport report) => Clean();

        // build hỏng giữa chừng thì bước sau build không chạy: dọn khi Editor nạp lại
        [InitializeOnLoadMethod]
        static void CleanOnLoad()
        {
            if (!BuildPipeline.isBuildingPlayer) Clean();
        }

        static void Clean()
        {
            var pack = Pack;
            if (Directory.Exists(pack)) Directory.Delete(pack, true);
            if (File.Exists(pack + ".meta")) File.Delete(pack + ".meta");
            // thư mục StreamingAssets chỉ có vì bước này thì xoá luôn
            var sa = Path.GetDirectoryName(pack);
            if (Directory.Exists(sa) && !Directory.EnumerateFileSystemEntries(sa).Any())
            {
                Directory.Delete(sa);
                if (File.Exists(sa + ".meta")) File.Delete(sa + ".meta");
            }
        }

        // đường dẫn tương đối (từ thư mục reskin) của mọi file cần: anim.json, portrait.png, hình anim.json trỏ tới
        public static List<string> Collect(string reskin, out int heroes, out List<string> missing)
        {
            var root = Path.GetFullPath(reskin).TrimEnd('\\', '/');
            var set = new SortedSet<string>(StringComparer.OrdinalIgnoreCase);
            missing = new List<string>();
            heroes = 0;
            foreach (var dir in Directory.GetDirectories(root))
            {
                var anim = Path.Combine(dir, "export", "anim.json");
                if (!File.Exists(anim)) continue;
                heroes++;
                Add(root, anim, set, missing);
                var portrait = Path.Combine(dir, "export", "portrait.png");
                if (File.Exists(portrait)) Add(root, portrait, set, missing);
                var json = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(anim));
                foreach (var sp in (List<object>)json["sprites"])
                    Add(root, Path.GetFullPath(Path.Combine(dir, (string)sp)), set, missing);
            }
            return set.ToList();
        }

        static void Add(string root, string full, SortedSet<string> set, List<string> missing)
        {
            full = Path.GetFullPath(full);
            if (!full.StartsWith(root + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase) || !File.Exists(full))
            {
                missing.Add(full);
                return;
            }
            set.Add(full.Substring(root.Length + 1));
        }

        static bool IsJson(string rel) => rel.EndsWith(".json", StringComparison.OrdinalIgnoreCase);

        // Tướng aola được vẽ vào RenderTexture (AolaSticker): tối đa 1024 điểm cho khung 3,4 lần chiều cao dáng đứng, tức dáng đứng
        // cao tối đa ~301 điểm dù màn to cỡ nào. Hình mảnh chỉ cần đủ nét cho mức đó, chừa thêm Margin.
        const float PxPerHeight = 1024f / 3.4f;
        const float Margin = 1.25f;

        // Cỡ đích của mỗi hình mảnh (đường dẫn đầy đủ): độ phóng lớn nhất hình được vẽ ra trong mọi clip của mọi tướng dùng nó,
        // quy ra điểm RenderTexture. Chỉ ghi hình cần thu nhỏ.
        static Dictionary<string, (int w, int h)> SizePlan(string reskin)
        {
            var root = Path.GetFullPath(reskin).TrimEnd('\\', '/');
            var need = new Dictionary<string, double>(StringComparer.OrdinalIgnoreCase);
            var size = new Dictionary<string, (int w, int h)>(StringComparer.OrdinalIgnoreCase);
            foreach (var dir in Directory.GetDirectories(root))
            {
                var anim = Path.Combine(dir, "export", "anim.json");
                if (!File.Exists(anim)) continue;
                var json = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(anim));
                var sprites = ((List<object>)json["sprites"]).Select(s => Path.GetFullPath(Path.Combine(dir, (string)s))).ToList();
                var dims = sprites.Select(p =>
                {
                    if (!size.TryGetValue(p, out var d))
                    {
                        if (!File.Exists(p) || !AolaPngPack.Size(p, out int w, out int h)) w = h = 0;
                        size[p] = d = (w, h);
                    }
                    return d;
                }).ToList();
                var clips = (Dictionary<string, object>)json["clips"];
                if (!clips.TryGetValue(AolaActor.Idle, out var idleObj)) continue;
                // chiều cao dáng đứng (điểm clip): khung bao khung đầu của clip đứng, như AolaActor tính
                double top = double.MaxValue, bottom = double.MinValue;
                foreach (List<object> row in (List<object>)((List<object>)((Dictionary<string, object>)idleObj)["frames"])[0])
                {
                    var (w, h) = dims[Convert.ToInt32(row[0])];
                    double b = Convert.ToDouble(row[2]), d = Convert.ToDouble(row[4]), ty = Convert.ToDouble(row[6]);
                    foreach (var (x, y) in new[] { (0, 0), (w, 0), (0, h), (w, h) })
                    {
                        double py = b * x + d * y + ty;
                        top = Math.Min(top, py);
                        bottom = Math.Max(bottom, py);
                    }
                }
                double k = PxPerHeight / Math.Max(1, bottom - top) * Margin;
                foreach (var clip in clips.Values)
                    foreach (List<object> frame in (List<object>)((Dictionary<string, object>)clip)["frames"])
                        foreach (List<object> row in frame)
                        {
                            var p = sprites[Convert.ToInt32(row[0])];
                            double a = Convert.ToDouble(row[1]), b = Convert.ToDouble(row[2]), c = Convert.ToDouble(row[3]), d = Convert.ToDouble(row[4]);
                            double s = Math.Max(Math.Sqrt(a * a + b * b), Math.Sqrt(c * c + d * d)) * k;
                            need.TryGetValue(p, out double old);
                            need[p] = Math.Max(old, s);
                        }
            }
            var plan = new Dictionary<string, (int w, int h)>(StringComparer.OrdinalIgnoreCase);
            foreach (var kv in need)
            {
                var (w, h) = size[kv.Key];
                double s = Math.Min(1, kv.Value);
                if (w == 0 || s >= 1) continue;
                int nw = Math.Max(1, (int)Math.Round(w * s)), nh = Math.Max(1, (int)Math.Round(h * s));
                if (nw < w || nh < h) plan[kv.Key] = (nw, nh);
            }
            return plan;
        }

        // anim.json cho bản build: ma trận của hình đã thu nhỏ chia theo tỉ lệ cỡ (ma trận đổi điểm hình → điểm clip, nên hình
        // nhỏ đi thì hệ số lớn lên; khung hình, chỗ neo, bóng giữ nguyên). Ghi gọn một dòng.
        static string Rescale(string animPath, Dictionary<string, (int w, int h, int nw, int nh)> made)
        {
            var dir = Path.GetDirectoryName(Path.GetDirectoryName(animPath)); // reskin/<tên>
            var json = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(animPath));
            var sprites = (List<object>)json["sprites"];
            var sx = new double[sprites.Count];
            var sy = new double[sprites.Count];
            for (int i = 0; i < sprites.Count; i++)
            {
                sx[i] = sy[i] = 1;
                if (made.TryGetValue(Path.GetFullPath(Path.Combine(dir, (string)sprites[i])), out var m) && m.w > 0 && m.h > 0)
                {
                    sx[i] = (double)m.nw / m.w;
                    sy[i] = (double)m.nh / m.h;
                }
            }
            foreach (var clip in ((Dictionary<string, object>)json["clips"]).Values)
                foreach (List<object> frame in (List<object>)((Dictionary<string, object>)clip)["frames"])
                    foreach (List<object> row in frame)
                    {
                        int i = Convert.ToInt32(row[0]);
                        if (sx[i] == 1 && sy[i] == 1) continue;
                        row[1] = Math.Round(Convert.ToDouble(row[1]) / sx[i], 6);
                        row[2] = Math.Round(Convert.ToDouble(row[2]) / sx[i], 6);
                        row[3] = Math.Round(Convert.ToDouble(row[3]) / sy[i], 6);
                        row[4] = Math.Round(Convert.ToDouble(row[4]) / sy[i], 6);
                    }
            return MiniJson.Write(json);
        }

        // Build Android như nút Build (không Development) ra Temp/PokiApkCheck, rồi soi APK như AolaDevPack đọc trên máy:
        // có stamp, và mọi file Collect liệt kê nằm ở assets/PokiDev/reskin/<đường dẫn>.
        [MenuItem("PokiClash/Build/Kiểm tra gói tướng (build Android ra Temp)", priority = 41)]
        static void CheckApk()
        {
            var apk = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiApkCheck/check.apk"));
            Directory.CreateDirectory(Path.GetDirectoryName(apk));
            var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions
            {
                scenes = EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path).ToArray(),
                target = BuildTarget.Android,
                locationPathName = apk,
                options = BuildOptions.None,
            });
            Debug.Log($"[Tướng aola] Build thử: {report.summary.result}, {new FileInfo(apk).Length / 1e6:0} MB, {report.summary.totalTime.TotalSeconds:0} giây");
            if (report.summary.result != BuildResult.Succeeded) return;
            var want = Collect(AolaImport.FindDir(), out int heroes, out _);
            using (var zip = new System.IO.Compression.ZipArchive(File.OpenRead(apk), System.IO.Compression.ZipArchiveMode.Read))
            {
                var prefix = "assets/" + AolaDevPack.Folder + "/";
                bool stamp = zip.GetEntry(prefix + AolaDevPack.Stamp) != null;
                var lack = want.Where(r =>
                {
                    var e = prefix + "reskin/" + r.Replace('\\', '/');
                    return zip.GetEntry(e) == null && zip.GetEntry(e + AolaDevPack.Gz) == null; // anim.json nằm dạng .gz
                }).ToList();
                foreach (var r in lack.Take(10)) Debug.LogError("[Tướng aola] APK thiếu " + r);
                Debug.Log($"[Tướng aola] APK: stamp {(stamp ? "có" : "THIẾU")}, {want.Count - lack.Count}/{want.Count} file của {heroes} tướng.");
            }
            Debug.Log($"[Tướng aola] Gói tạm đã dọn: {!Directory.Exists(Pack)}");
        }
    }
}
