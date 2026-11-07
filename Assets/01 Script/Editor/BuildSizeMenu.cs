// Dung lượng build (người dùng 2026-11-03: bản Android phải khoảng 60-70 MB, ảnh gen xong là tối ưu luôn):
// menu "PokiClash/Dung lượng: ảnh nặng trong build" liệt kê ảnh trong Assets/03 Art theo cỡ lưu thật ở nền đang chọn (định dạng
// đã nhập, cả mipmap), cộng theo thư mục, đánh dấu ảnh không nén; ghi Temp/PokiShots/dung_luong.txt.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using UnityEditor;
using UnityEditor.Build;
using UnityEngine;

namespace PokiClash.EditorTools
{
    // Nút Build (cửa sổ Build/Build Profiles) bản Android: nén gói dữ liệu LZ4HC thay vì LZ4 mặc định (data.unity3d nhỏ hơn,
    // không mất chất lượng, build lâu hơn một chút; máy đọc nhanh như LZ4).
    [InitializeOnLoad]
    static class BuildLz4HC
    {
        static BuildLz4HC() => BuildPlayerWindow.RegisterBuildPlayerHandler(Build);

        static void Build(BuildPlayerOptions o)
        {
            if (o.target == BuildTarget.Android) o.options |= BuildOptions.CompressWithLz4HC;
            BuildCodeSize.Apply();
            // bản thử không cần logo Unity lúc mở (Unity 6 Personal cho tắt; ProjectSettings cũng đã tắt, phòng bản cũ ghi đè)
            if (PlayerSettings.SplashScreen.show) PlayerSettings.SplashScreen.show = false;
            try { BuildPlayerWindow.DefaultBuildMethods.BuildPlayer(o); }
            finally { FontBuildRestore.Restore(); }
        }
    }

    // Cỡ code Android (libil2cpp 17 MB nén trong APK 0.0.5, 2026-11-07): IL2CPP sinh code gọn (OptimizeSize: chậm hơn chút ở code
    // generic, game này không đáng kể) và strip mức Low (bỏ code không dùng ở mọi assembly nhưng giữ thận trọng; SROptions có
    // link.xml). Mặc định cũ là Minimal (chỉ strip thư viện .NET và UnityEngine). Đặt khi mở Editor và trước mỗi lần bấm Build.
    [InitializeOnLoad]
    static class BuildCodeSize
    {
        static BuildCodeSize() => EditorApplication.delayCall += Apply;

        public static void Apply()
        {
            var t = NamedBuildTarget.Android;
            if (PlayerSettings.GetIl2CppCodeGeneration(t) != Il2CppCodeGeneration.OptimizeSize)
                PlayerSettings.SetIl2CppCodeGeneration(t, Il2CppCodeGeneration.OptimizeSize);
            var strip = PlayerSettings.GetManagedStrippingLevel(t);
            if (strip == ManagedStrippingLevel.Disabled || strip == ManagedStrippingLevel.Minimal)
                PlayerSettings.SetManagedStrippingLevel(t, ManagedStrippingLevel.Low);
        }
    }

    // TMP (TMP_PreBuildProcessor) xoá chữ đã xếp của phông động bật "Clear Dynamic Data On Build" ngay trước mỗi lần build và ghi
    // đè file .asset: APK mang phông rỗng (nhẹ hơn ~2-3 MB, máy tự xếp chữ khi cần) nhưng chữ trong Editor hỏng (2026-11-07 sau
    // build đo: thẻ đảo ở sảnh hiện "À ế"). Chép file phông ra Temp trước TMP, chép lại sau build; build dừng giữa chừng thì chép
    // lại khi Editor nạp code.
    sealed class FontBuildRestore : IPreprocessBuildWithReport, IPostprocessBuildWithReport
    {
        const string FontDir = "Assets/03 Art/Fonts";
        public int callbackOrder => -100; // trước TMP_PreBuildProcessor (0)
        static string Backup => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiFontBackup"));

        public void OnPreprocessBuild(UnityEditor.Build.Reporting.BuildReport report)
        {
            Restore(); // bản chép của lần build trước còn sót
            Directory.CreateDirectory(Backup);
            foreach (var guid in AssetDatabase.FindAssets("t:TMP_FontAsset", new[] { FontDir }))
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var font = AssetDatabase.LoadMainAssetAtPath(path);
                if (font) AssetDatabase.SaveAssetIfDirty(font);
                File.Copy(path, Path.Combine(Backup, Path.GetFileName(path)), true);
            }
        }

        public void OnPostprocessBuild(UnityEditor.Build.Reporting.BuildReport report) => EditorApplication.delayCall += Restore;

        [InitializeOnLoadMethod]
        static void OnLoad() => EditorApplication.delayCall += Restore;

        public static void Restore()
        {
            if (!Directory.Exists(Backup) || BuildPipeline.isBuildingPlayer) return;
            var files = Directory.GetFiles(Backup, "*.asset");
            var paths = new List<string>();
            foreach (var f in files)
            {
                var dst = FontDir + "/" + Path.GetFileName(f);
                if (!File.Exists(dst)) continue;
                File.Copy(f, dst, true);
                paths.Add(dst);
            }
            Directory.Delete(Backup, true);
            foreach (var p in paths) AssetDatabase.ImportAsset(p, ImportAssetOptions.ForceUpdate);
            if (paths.Count > 0) Debug.Log($"[Dung lượng] Chép lại {paths.Count} phông sau build (TMP đã xoá chữ của chúng trước build).");
        }
    }

    public static class BuildSizeMenu
    {
        [MenuItem("PokiClash/Dung lượng: ảnh nặng trong build", priority = 90)]
        static void Report()
        {
            var util = typeof(Editor).Assembly.GetType("UnityEditor.TextureUtil");
            var storage = util?.GetMethod("GetStorageMemorySizeLong", BindingFlags.Static | BindingFlags.Public);
            var rows = new List<(string path, long bytes, string fmt, int w, int h, int mips)>();
            foreach (var guid in AssetDatabase.FindAssets("t:Texture2D", new[] { "Assets/03 Art" }))
            {
                string path = AssetDatabase.GUIDToAssetPath(guid);
                var tex = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
                if (!tex) continue;
                long bytes = storage != null ? (long)storage.Invoke(null, new object[] { tex }) : UnityEngine.Profiling.Profiler.GetRuntimeMemorySizeLong(tex);
                rows.Add((path, bytes, tex.format.ToString(), tex.width, tex.height, tex.mipmapCount));
            }
            rows.Sort((a, b) => b.bytes.CompareTo(a.bytes));
            var sb = new StringBuilder();
            sb.AppendLine($"Nền: {EditorUserBuildSettings.activeBuildTarget}; {rows.Count} ảnh, tổng {rows.Sum(r => r.bytes) / 1048576f:0.0} MB; " +
                          $"ép nén lúc nhập: {EditorUserBuildSettings.overrideTextureCompression}, ép cỡ: {EditorUserBuildSettings.overrideMaxTextureSize}");
            sb.AppendLine("Theo thư mục:");
            foreach (var g in rows.GroupBy(r => Group(r.path)).OrderByDescending(g => g.Sum(r => r.bytes)))
                sb.AppendLine($"  {g.Sum(r => r.bytes) / 1048576f,7:0.0} MB  {g.Count(),4}  {g.Key}");
            var raw = rows.Where(r => r.fmt.StartsWith("RGBA") || r.fmt.StartsWith("RGB") || r.fmt.StartsWith("ARGB")).ToList();
            sb.AppendLine($"Không nén: {raw.Count} ảnh, {raw.Sum(r => r.bytes) / 1048576f:0.0} MB");
            foreach (var r in raw.Take(20)) sb.AppendLine($"  {r.bytes / 1024f,8:0} KB  {r.fmt} {r.w}x{r.h} mip {r.mips}  {r.path}");
            // cách nhập của vài ảnh không nén (tìm vì sao không nén)
            foreach (var r in raw.Where(r => r.path.EndsWith("_portrait.png")).Take(1).Concat(raw.Where(r => !r.path.EndsWith("_portrait.png")).Take(2)))
            {
                var ti = (TextureImporter)AssetImporter.GetAtPath(r.path);
                var an = ti.GetPlatformTextureSettings("Android");
                sb.AppendLine($"  cách nhập {r.path}: kiểu {ti.textureType}, nén {ti.textureCompression}, mip {ti.mipmapEnabled}, đọc ghi {ti.isReadable}, " +
                              $"Android ghi đè {an.overridden} {an.format} max {an.maxTextureSize} nén {an.textureCompression}, tự chọn {ti.GetAutomaticFormat("Android")}");
            }
            sb.AppendLine("Nặng nhất:");
            foreach (var r in rows.Take(40)) sb.AppendLine($"  {r.bytes / 1024f,8:0} KB  {r.fmt} {r.w}x{r.h} mip {r.mips}  {r.path}");
            string dir = PlayTour.ShotDir;
            Directory.CreateDirectory(dir);
            File.WriteAllText(Path.Combine(dir, "dung_luong.txt"), sb.ToString());
            Debug.Log("[Dung lượng] " + sb.ToString().Split('\n')[0] + " → " + Path.Combine(dir, "dung_luong.txt"));
        }

        // Build Android như nút Build (không Development, LZ4HC, cài đặt code BuildCodeSize) ra Temp/PokiApkSize/size.apk rồi ghi các
        // phần nặng nhất của APK vào Temp/PokiShots/apk_size.txt. Chỉ chạy khi nền đang chọn là Android (đổi nền thì nhập lại mọi ảnh).
        [MenuItem("PokiClash/Build/Đo dung lượng APK (build Android ra Temp)", priority = 42)]
        public static void MeasureApk()
        {
            if (EditorUserBuildSettings.activeBuildTarget != BuildTarget.Android)
            {
                Debug.LogError("[Dung lượng] Nền đang chọn không phải Android; chuyển nền trước (đổi nền sẽ nhập lại mọi ảnh).");
                return;
            }
            BuildCodeSize.Apply();
            var apk = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiApkSize/size.apk"));
            Directory.CreateDirectory(Path.GetDirectoryName(apk));
            var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions
            {
                scenes = EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path).ToArray(),
                target = BuildTarget.Android,
                locationPathName = apk,
                options = BuildOptions.CompressWithLz4HC,
            });
            FontBuildRestore.Restore();
            var sb = new StringBuilder();
            sb.AppendLine($"Build {report.summary.result}, {report.summary.totalTime.TotalSeconds:0} giây → {apk}");
            if (report.summary.result == UnityEditor.Build.Reporting.BuildResult.Succeeded && File.Exists(apk))
            {
                sb.AppendLine($"APK {new FileInfo(apk).Length / 1e6:0.0} MB");
                using var zip = System.IO.Compression.ZipFile.OpenRead(apk);
                foreach (var e in zip.Entries.OrderByDescending(e => e.CompressedLength).Take(12))
                    sb.AppendLine($"  {e.CompressedLength / 1e6,7:0.00} MB (giải nén {e.Length / 1e6,7:0.00})  {e.FullName}");
            }
            Directory.CreateDirectory(PlayTour.ShotDir);
            File.WriteAllText(Path.Combine(PlayTour.ShotDir, "apk_size.txt"), sb.ToString());
            Debug.Log("[Dung lượng] " + sb.ToString().Replace("\n", " | "));
        }

        // nhóm: chân dung, atlas tướng tách riêng; còn lại theo thư mục con của Assets/03 Art
        static string Group(string path)
        {
            if (path.EndsWith("_portrait.png")) return "Heroes: chân dung";
            if (path.EndsWith("_atlas.png")) return "Heroes: atlas";
            var parts = path.Split('/');
            return parts.Length > 3 ? parts[2] + "/" + parts[3] : path;
        }
    }
}
