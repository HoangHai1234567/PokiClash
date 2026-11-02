// Mang hình tướng aola vào bản build để xem trên máy thật (chủ dự án 2026-11-02: "để tất cả các tướng kể cả aola, đây là
// prototype thôi"). AllBuilds bật: mọi bản build đều mang; tắt (trước khi phát hành công khai): chỉ Development Build mang.
// Trước build (sau PreBuildCheck): chép mọi tướng có export/anim.json trong thư mục reskin
// (AolaActor.FindDir) vào Assets/StreamingAssets/PokiDev/reskin. Mỗi tướng gồm anim.json, portrait.png và đúng các hình anim.json
// trỏ tới (đường dẫn tương đối từ reskin/<tên>, như pet<id>_parts/chars hay reskin/<tên>/sprites), giữ nguyên cấu trúc.
// Thêm stamp.txt để máy biết build mới. Sau build (và khi mở Editor, phòng build hỏng giữa chừng) xoá thư mục đó.
// Không mang thì chỉ cảnh báo là trên máy sẽ không có tướng. Lúc chạy: Game/Heroes/AolaDevPack.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
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

        // Prototype: mọi bản build mang hình tướng aola (hình của Baitian). Đặt false trước khi phát hành công khai.
        public static readonly bool AllBuilds = true;

        static string Pack => Path.Combine(Application.dataPath, "StreamingAssets", AolaDevPack.Folder);

        public void OnPreprocessBuild(BuildReport report)
        {
            Clean();
            if (!AllBuilds && (report.summary.options & BuildOptions.Development) == 0)
            {
                Debug.LogWarning("[Tướng aola] AolaDevBuild.AllBuilds tắt và đây không phải Development Build: bản build không mang hình tướng, " +
                                 "lên máy sẽ không thấy tướng.");
                return;
            }
            var src = AolaActor.FindDir();
            if (string.IsNullOrEmpty(src) || !Directory.Exists(src))
            {
                Debug.LogWarning("[Tướng aola] Không tìm thấy thư mục reskin (menu PokiClash/Tự tìm thư mục aola): bản build không có tướng.");
                return;
            }
            var files = Collect(src, out int heroes, out var missing);
            long bytes = 0;
            var dst = Path.Combine(Pack, "reskin");
            foreach (var rel in files)
            {
                var to = Path.Combine(dst, rel);
                Directory.CreateDirectory(Path.GetDirectoryName(to));
                File.Copy(Path.Combine(src, rel), to, true);
                bytes += new FileInfo(to).Length;
            }
            File.WriteAllText(Path.Combine(Pack, AolaDevPack.Stamp), DateTime.Now.Ticks.ToString());
            foreach (var m in missing.Take(10)) Debug.LogWarning("[Tướng aola] Thiếu hình: " + m);
            Debug.Log($"[Tướng aola] Mang {heroes} tướng, {files.Count} file, {bytes / 1e6:0.0} MB vào bản build ({missing.Count} hình thiếu).");
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
            var want = Collect(AolaActor.FindDir(), out int heroes, out _);
            using (var zip = new System.IO.Compression.ZipArchive(File.OpenRead(apk), System.IO.Compression.ZipArchiveMode.Read))
            {
                var prefix = "assets/" + AolaDevPack.Folder + "/";
                bool stamp = zip.GetEntry(prefix + AolaDevPack.Stamp) != null;
                var lack = want.Where(r => zip.GetEntry(prefix + "reskin/" + r.Replace('\\', '/')) == null).ToList();
                foreach (var r in lack.Take(10)) Debug.LogError("[Tướng aola] APK thiếu " + r);
                Debug.Log($"[Tướng aola] APK: stamp {(stamp ? "có" : "THIẾU")}, {want.Count - lack.Count}/{want.Count} file của {heroes} tướng.");
            }
            Debug.Log($"[Tướng aola] Gói tạm đã dọn: {!Directory.Exists(Pack)}");
        }
    }
}
