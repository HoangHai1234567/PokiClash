// Bộ build riêng cho điện thoại (người dùng 2026-11-21: "viết thêm kiểu plugin build riêng cho mobile android ios tối ưu dung lượng
// và hiệu năng"). Menu PokiClash/Build:
//  - Android thử (APK): như nút Build, ra Build/<tên>_<phiên bản>_<yyMMddHH>.apk
//  - Android phát hành (AAB cho Google Play): bật thêm R8 (thu gọn code Java; dự án không có plugin Java riêng)
//  - iOS (xuất project Xcode): IL2CPP sinh code gọn, strip mức Low như Android; mở thư mục ra trên máy Mac để build
// Mỗi lần build: bỏ scene không phải màn chơi (SkipScenes), bỏ thư mục thừa trong Resources (BuildExclude), nén gói dữ liệu LZ4HC,
// cài đặt riêng của kiểu build chỉ áp trong lúc build rồi trả lại (ProjectSettings không đổi sau build), xong ghi báo cáo dung lượng
// (BuildSizeReport: theo nhóm, so lần trước, ngân sách). Nút Build của cửa sổ Build Profiles cũng chạy phần bỏ + báo cáo (BuildLz4HC).
// Nền đang chọn phải đúng nền của kiểu build: đổi nền làm Unity nhập lại mọi ảnh (lâu), nên không tự đổi, tự chuyển trong Build Profiles.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class PokiBuild
    {
        public enum Kind { AndroidTest, AndroidRelease, IOS }

        // có trong danh sách scene của Build Settings nhưng không phải màn chơi (scene mẫu của template, bàn thử aola)
        public static readonly string[] SkipScenes = { "SampleScene", "BanThu" };

        public static string OutDir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Build"));

        [MenuItem("PokiClash/Build/Android thử (APK)", priority = 20)]
        static void MenuAndroidTest() => Run(Kind.AndroidTest);

        [MenuItem("PokiClash/Build/Android phát hành (AAB cho Google Play)", priority = 21)]
        static void MenuAndroidRelease() => Run(Kind.AndroidRelease);

        [MenuItem("PokiClash/Build/iOS (xuất project Xcode)", priority = 22)]
        static void MenuIos() => Run(Kind.IOS);

        // Xem trước, không build: thứ sẽ bỏ và phần chúng chiếm ở lần build gần nhất.
        [MenuItem("PokiClash/Build/Xem trước: những gì sẽ bỏ khỏi bản build", priority = 25)]
        static void MenuPreview()
        {
            var scenes = Scenes(EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path));
            var skipped = EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path).Except(scenes).ToList();
            var plan = BuildExclude.Plan(scenes);
            var last = BuildReport.GetLatestReport();
            long was = BuildSizeReport.SizeIn(last, plan.Select(p => p.path));
            Debug.Log($"[Build] Xem trước: bỏ {skipped.Count} scene ({string.Join(", ", skipped.Select(Path.GetFileNameWithoutExtension))}), " +
                      $"{plan.Count} thư mục thừa trong Resources; ở lần build gần nhất ({last?.summary.outputPath}) chúng chiếm {was / 1048576.0:0.0} MB " +
                      $"trước nén:\n{string.Join(", ", plan.Select(p => Path.GetFileName(p.path)))}");
        }

        [MenuItem("PokiClash/Build/Báo cáo dung lượng lần build gần nhất", priority = 26)]
        static void MenuLastReport()
        {
            var r = BuildReport.GetLatestReport();
            if (r == null) Debug.LogWarning("[Build] Chưa có báo cáo build nào (Library/LastBuild.buildreport).");
            else BuildSizeReport.Write(r, null, "đọc lại báo cáo build");
        }

        public static string[] Scenes(IEnumerable<string> paths) =>
            paths.Where(p => !SkipScenes.Contains(Path.GetFileNameWithoutExtension(p))).ToArray();

        static string Safe(string s) => new string(s.Where(c => char.IsLetterOrDigit(c) || c == '_' || c == '-').ToArray());

        public static BuildReport Run(Kind kind)
        {
            var target = kind == Kind.IOS ? BuildTarget.iOS : BuildTarget.Android;
            if (BuildPipeline.isBuildingPlayer) return null;
            if (EditorUserBuildSettings.activeBuildTarget != target)
            {
                Debug.LogError($"[Build] Nền đang chọn là {EditorUserBuildSettings.activeBuildTarget}, kiểu build này cần {target}. Chuyển nền trong " +
                               "File > Build Profiles trước (Unity sẽ nhập lại mọi ảnh, lâu).");
                return null;
            }
            // atlas nhập hỏng thì ảnh nguồn vào gói rời không nén (vụ atlas hạt 2026-11-23, +110 MB): nhập lại, vẫn hỏng thì dừng
            if (!AtlasGuard.Ensure()) return null;
            string name = $"{Safe(PlayerSettings.productName)}_{PlayerSettings.bundleVersion}_{DateTime.Now:yyMMddHH}";
            string path = kind == Kind.AndroidTest ? Path.Combine(OutDir, name + ".apk")
                : kind == Kind.AndroidRelease ? Path.Combine(OutDir, name + ".aab")
                : Path.Combine(OutDir, "iOS_" + name);
            // hai bản build trong cùng một giờ: thêm _2, _3 thay vì ghi đè bản trước (2026-11-23)
            for (int i = 2; File.Exists(path) || Directory.Exists(path); i++)
            {
                string ext = Path.GetExtension(path), stem = kind == Kind.IOS ? "iOS_" + name : name;
                path = Path.Combine(OutDir, $"{stem}_{i}{(kind == Kind.IOS ? "" : ext)}");
            }
            Directory.CreateDirectory(OutDir);
            var opts = new BuildPlayerOptions
            {
                scenes = Scenes(EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path)),
                target = target,
                targetGroup = BuildPipeline.GetBuildTargetGroup(target),
                locationPathName = path,
                options = BuildOptions.CompressWithLz4HC,
            };
            if (kind == Kind.AndroidRelease && !PlayerSettings.Android.useCustomKeystore)
                Debug.LogWarning("[Build] AAB đang ký bằng khoá debug: Google Play không nhận. Đặt keystore trong Player Settings > Publishing Settings.");
            if (kind != Kind.AndroidTest && PlayerSettings.applicationIdentifier.Contains("com.unity.template"))
                Debug.LogWarning($"[Build] Mã ứng dụng vẫn là mã của template ({PlayerSettings.applicationIdentifier}): đổi trước khi đưa lên cửa hàng.");

            var undo = ApplySettings(kind);
            List<BuildExclude.Item> excluded = null;
            SecureBuild.Token secBalance = null;
            BuildReport report = null;
            try
            {
                excluded = BuildExclude.Plan(opts.scenes);
                BuildExclude.Apply(excluded);
                if (kind == Kind.AndroidRelease || kind == Kind.IOS)
                {
                    secBalance = SecureBuild.StripBalance();
                    ArtEncryptStrip.StripForBuild(opts.scenes); // tự no-op nếu chưa bật (menu Bảo mật)
                }
                report = BuildPipeline.BuildPlayer(opts);
            }
            finally
            {
                ArtEncryptStrip.Restore();
                SecureBuild.Restore(secBalance);
                BuildExclude.Restore();
                undo();
                try { FontBuildRestore.Restore(); }
                catch (Exception e) { Debug.LogWarning("[Build] Chép lại phông: " + e.Message); }
            }
            BuildSizeReport.Write(report, excluded, KindName(kind));
            if (report != null && report.summary.result != BuildResult.Succeeded)
                Debug.LogError($"[Build] {KindName(kind)}: {report.summary.result}, {report.summary.totalErrors} lỗi (xem Console).");
            return report;
        }

        static string KindName(Kind k) => k == Kind.AndroidTest ? "Android thử" : k == Kind.AndroidRelease ? "Android phát hành" : "iOS";

        // Cài đặt riêng của kiểu build; trả về hàm trả lại giá trị cũ (chỉ những gì đã đổi).
        static Action ApplySettings(Kind kind)
        {
            var undo = new List<Action>();

            void Set<T>(Func<T> get, Action<T> set, T value)
            {
                var old = get();
                if (EqualityComparer<T>.Default.Equals(old, value)) return;
                set(value);
                undo.Add(() => set(old));
            }

            // màn chờ đã tắt trong ProjectSettings nhưng còn bật "logo Unity" thì ảnh logo (1,2 MB trước nén) vẫn vào gói
            Set(() => PlayerSettings.SplashScreen.showUnityLogo, v => PlayerSettings.SplashScreen.showUnityLogo = v, PlayerSettings.SplashScreen.show);
            if (kind == Kind.IOS)
            {
                var t = NamedBuildTarget.iOS;
                Set(() => PlayerSettings.GetScriptingBackend(t), v => PlayerSettings.SetScriptingBackend(t, v), ScriptingImplementation.IL2CPP);
                Set(() => PlayerSettings.GetIl2CppCodeGeneration(t), v => PlayerSettings.SetIl2CppCodeGeneration(t, v), Il2CppCodeGeneration.OptimizeSize);
                Set(() => PlayerSettings.GetManagedStrippingLevel(t), v => PlayerSettings.SetManagedStrippingLevel(t, v), ManagedStrippingLevel.Low);
            }
            else
            {
                BuildCodeSize.Apply(); // IL2CPP sinh code gọn + strip Low (đặt sẵn từ 2026-11-07)
                bool aab = kind == Kind.AndroidRelease;
                Set(() => EditorUserBuildSettings.buildAppBundle, v => EditorUserBuildSettings.buildAppBundle = v, aab);
                if (aab) Set(() => PlayerSettings.Android.minifyRelease, v => PlayerSettings.Android.minifyRelease = v, true);
                // Gói tải sau (GD_Claude/27): AAB bật Split Application Binary thì Addressables for Android tách 5 nhóm noi_dung_<hệ> thành
                // asset pack fast-follow; APK thử phải tắt (bật trên APK sinh file OBB), khi đó gói nằm sẵn trong APK (bản đủ).
                Set(() => PlayerSettings.Android.splitApplicationBinary, v => PlayerSettings.Android.splitApplicationBinary = v, aab);
            }
            // build ghi ProjectSettings xuống đĩa lúc đang mang giá trị tạm: trả xong thì ghi lại ngay
            return () =>
            {
                for (int i = undo.Count - 1; i >= 0; i--) undo[i]();
                if (undo.Count > 0) AssetDatabase.SaveAssets();
            };
        }
    }
}
