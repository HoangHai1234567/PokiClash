// Kiểm tra trước build: bản phát hành không được chứa hình hay dữ liệu chuyển động của Baitian (aola).
// Báo lỗi (dừng build) nếu Assets có ảnh/JSON nằm trong đường dẫn có "aola" hoặc ảnh pet*_parts, hoặc build bật POKICLASH_DEV
// mà không phải Development Build. Code BanThu cũ (thư mục 01 Script/BanThu) chỉ cảnh báo vì chủ dự án giữ lại.
// Ngoại lệ: hình tướng aola nhập thành prefab (Assets/03 Art/Heroes, Editor/AolaImport) được vào bản build khi HeroArtInBuild
// bật (prototype, chủ dự án chốt 2026-11-02); tắt trước khi phát hành công khai thì build báo lỗi cho tới khi thay hết hình.
// Công cụ dev chạy trong game (01 Script/App/Dev: bảng thử, chỉnh số, máy tự chơi, ghi trận) phải bọc kín
// "#if UNITY_EDITOR || DEVELOPMENT_BUILD" để không vào bản phát hành.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public sealed class PreBuildCheck : IPreprocessBuildWithReport
    {
        public int callbackOrder => 0;

        // Prototype: hình tướng aola (hình của Baitian) vào mọi bản build. Đặt false trước khi phát hành công khai.
        public static readonly bool HeroArtInBuild = true;

        static readonly Regex PetParts = new Regex(@"pet\d*_parts", RegexOptions.IgnoreCase);
        static readonly string[] MediaExt = { ".png", ".jpg", ".jpeg", ".json", ".swf", ".atlas" };

        public void OnPreprocessBuild(BuildReport report)
        {
            var errors = Scan(out var warnings);
            foreach (var w in warnings) Debug.LogWarning("[Kiểm tra build] " + w);
            bool dev = (report.summary.options & BuildOptions.Development) != 0;
            var defines = PlayerSettings.GetScriptingDefineSymbols(NamedBuildTarget.FromBuildTargetGroup(report.summary.platformGroup));
            errors.AddRange(DevGuards());
            if (!dev && defines.Split(';').Contains("POKICLASH_DEV"))
                errors.Add("Bản phát hành đang bật define POKICLASH_DEV (hình aola sẽ được nạp). Tắt define hoặc chọn Development Build.");
            if (errors.Count > 0)
                throw new BuildFailedException("Kiểm tra trước build không đạt:\n- " + string.Join("\n- ", errors));
        }

        [MenuItem("PokiClash/Kiểm tra trước build", priority = 30)]
        static void Menu()
        {
            var errors = Scan(out var warnings);
            foreach (var w in warnings) Debug.LogWarning("[Kiểm tra build] " + w);
            errors.AddRange(DevGuards());
            foreach (var e in errors) Debug.LogError("[Kiểm tra build] " + e);
            if (errors.Count == 0) Debug.Log($"[Kiểm tra build] Đạt: không có hình aola trong Assets ({warnings.Count} cảnh báo).");
        }

        // biên dịch thử script của người chơi như bản phát hành (không Development): công cụ dev bị bỏ mà code vẫn phải biên dịch được
        [MenuItem("PokiClash/Biên dịch thử bản phát hành", priority = 31)]
        static void CompileRelease()
        {
            var target = EditorUserBuildSettings.activeBuildTarget;
            var settings = new UnityEditor.Build.Player.ScriptCompilationSettings
            {
                target = target, group = BuildPipeline.GetBuildTargetGroup(target), options = UnityEditor.Build.Player.ScriptCompilationOptions.None,
            };
            var dir = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiReleaseCompile"));
            var r = UnityEditor.Build.Player.PlayerBuildInterface.CompilePlayerScripts(settings, dir);
            bool ok = r.assemblies != null && r.assemblies.Contains("PokiClash.Game.dll");
            if (ok) Debug.Log($"[Kiểm tra build] Biên dịch bản phát hành ({target}) đạt: {string.Join(", ", r.assemblies.Where(a => a.StartsWith("PokiClash")))}");
            else Debug.LogError($"[Kiểm tra build] Biên dịch bản phát hành ({target}) lỗi, xem Console.");
        }

        public const string DevGuard = "#if UNITY_EDITOR || DEVELOPMENT_BUILD";
        public static string DevDir => Path.Combine(Application.dataPath, "01 Script", "App", "Dev");

        // mỗi file công cụ dev: dòng lệnh đầu tiên là DevGuard, dòng lệnh cuối là #endif
        public static List<string> DevGuards()
        {
            var errors = new List<string>();
            if (!Directory.Exists(DevDir)) return errors;
            foreach (var f in Directory.EnumerateFiles(DevDir, "*.cs", SearchOption.AllDirectories))
            {
                var lines = File.ReadAllLines(f).Select(l => l.Trim()).Where(l => l.Length > 0).ToList();
                if (lines.Count == 0 || lines[0] != DevGuard || lines[lines.Count - 1] != "#endif")
                    errors.Add($"Công cụ dev chưa bọc kín \"{DevGuard}\" … \"#endif\": Assets/01 Script/App/Dev/{Path.GetFileName(f)}");
            }
            return errors;
        }

        public static List<string> Scan(out List<string> warnings)
        {
            var errors = new List<string>();
            warnings = new List<string>();
            var root = Application.dataPath;
            foreach (var f in Directory.EnumerateFiles(root, "*", SearchOption.AllDirectories))
            {
                var rel = "Assets" + f.Substring(root.Length).Replace('\\', '/');
                if (rel.EndsWith(".meta")) continue;
                var ext = Path.GetExtension(rel).ToLowerInvariant();
                var lower = rel.ToLowerInvariant();
                if (rel.StartsWith(AolaImport.ArtDir + "/"))
                {
                    if (!HeroArtInBuild && (ext == ".png" || ext == ".bytes"))
                        errors.Add($"Hình tướng aola trong Assets (PreBuildCheck.HeroArtInBuild tắt): {rel}");
                }
                else if (MediaExt.Contains(ext) && (lower.Contains("/aola") || lower.Contains("aola/") || PetParts.IsMatch(lower)))
                    errors.Add($"Có tệp aola trong Assets: {rel}");
                else if (ext == ".cs" && !lower.Contains("/editor/"))
                {
                    var text = File.ReadAllText(f);
                    if (text.Contains("aola/reskin") || text.Contains("ProjectAtomik"))
                    {
                        if (lower.Contains("/01 script/banthu/")) warnings.Add($"Code BanThu cũ còn đường dẫn aola cứng: {rel} (không vào build nếu gỡ BanThu)");
                        else errors.Add($"Code có đường dẫn aola cứng: {rel}");
                    }
                }
            }
            return errors;
        }
    }
}
