// Chốt sprite atlas trước build (2026-11-27). Atlas hạt Fx/hat.spriteatlasv2 nhập hỏng từ chiều 2026-11-23 (Unity bị tắt giữa lượt
// "Gán gói ảnh hạt", đúng lúc đang dựng lại atlas): Unity nhận file là DefaultAsset nên build không gom ảnh hạt, 1458 ảnh vào gói rời ở
// RGBA32 không nén (443 MB trước nén), APK 168 → 232 → 278 MB qua hai bản mà Console không báo lỗi nào. Nhập lại riêng file atlas là hết.
// Trước build (PokiBuild.Run và nút Build qua BuildLz4HC): mọi .spriteatlasv2 trong Assets phải nạp ra SpriteAtlas; hỏng thì nhập lại;
// vẫn hỏng thì không build. Đường build khác (menu Đo dung lượng APK...) dừng ở OnPreprocessBuild.
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;
using UnityEngine.U2D;

namespace PokiClash.EditorTools
{
    public sealed class AtlasGuard : IPreprocessBuildWithReport
    {
        public int callbackOrder => -200;

        // atlas không nạp ra SpriteAtlas (nhập hỏng)
        public static List<string> Broken()
        {
            var res = new List<string>();
            foreach (var f in Directory.GetFiles(Application.dataPath, "*.spriteatlasv2", SearchOption.AllDirectories))
            {
                string p = "Assets" + f.Substring(Application.dataPath.Length).Replace('\\', '/');
                if (AssetDatabase.GetMainAssetTypeAtPath(p) != typeof(SpriteAtlas)) res.Add(p);
            }
            return res;
        }

        // nhập lại atlas hỏng; false: vẫn còn hỏng, đừng build
        public static bool Ensure()
        {
            var bad = Broken();
            if (bad.Count == 0) return true;
            Debug.LogWarning($"[Build] {bad.Count} sprite atlas nhập hỏng (ảnh nguồn sẽ vào gói rời, không nén), nhập lại: {string.Join(", ", bad)}");
            foreach (var p in bad) AssetDatabase.ImportAsset(p, ImportAssetOptions.ForceUpdate);
            bad = Broken();
            if (bad.Count == 0)
            {
                Debug.Log("[Build] Đã nhập lại sprite atlas, build tiếp.");
                return true;
            }
            Debug.LogError($"[Build] Không build: sprite atlas vẫn hỏng sau khi nhập lại: {string.Join(", ", bad)}. " +
                           "Dựng lại bằng menu PokiClash/Build/Sprite Atlas … (dựng lại).");
            return false;
        }

        public void OnPreprocessBuild(BuildReport report)
        {
            var bad = Broken();
            if (bad.Count > 0)
                throw new BuildFailedException($"Sprite atlas nhập hỏng: {string.Join(", ", bad)}. Build qua menu PokiClash/Build (tự nhập lại) " +
                                               "hoặc Reimport file đó rồi build lại.");
        }
    }
}
