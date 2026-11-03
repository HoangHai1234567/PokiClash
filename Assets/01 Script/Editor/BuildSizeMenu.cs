// Dung lượng build (người dùng 2026-11-03: bản Android phải khoảng 60-70 MB, ảnh gen xong là tối ưu luôn):
// menu "PokiClash/Dung lượng: ảnh nặng trong build" liệt kê ảnh trong Assets/03 Art theo cỡ lưu thật ở nền đang chọn (định dạng
// đã nhập, cả mipmap), cộng theo thư mục, đánh dấu ảnh không nén; ghi Temp/PokiShots/dung_luong.txt.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using UnityEditor;
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
            // bản thử không cần logo Unity lúc mở (Unity 6 Personal cho tắt; ProjectSettings cũng đã tắt, phòng bản cũ ghi đè)
            if (PlayerSettings.SplashScreen.show) PlayerSettings.SplashScreen.show = false;
            BuildPlayerWindow.DefaultBuildMethods.BuildPlayer(o);
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
