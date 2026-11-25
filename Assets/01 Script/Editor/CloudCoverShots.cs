// Chụp mây chuyển scene (CloudCover, hai đám mây vẽ tay 2026-11-24): đang ở sảnh thì chuyển sang màn Tướng rồi về, chụp lúc mây đang
// khép, khép kín, đang tách. Ảnh ra Temp/PokiShots/may_chuyen/. Không đổi bản lưu.
using System.Collections;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class CloudCoverShots
    {
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/may_chuyen"));

        [MenuItem("PokiClash/Thử/Giao diện/Mây chuyển scene: chụp (đang Play)", priority = 205)]
        static void Run()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.Log("[Mây] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Tour());
        }

        static IEnumerator Tour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            App.Modals.CloseAll();
            foreach (var to in new[] { SceneIds.Heroes, SceneIds.Hub })
            {
                float t0 = Time.realtimeSinceStartup;
                App.Router.Go(to);
                foreach (var at in new[] { 0.2f, 0.38f, 0.6f })
                {
                    while (Time.realtimeSinceStartup - t0 < at) yield return null;
                    yield return new WaitForEndOfFrame();
                    var tex = ScreenCapture.CaptureScreenshotAsTexture();
                    File.WriteAllBytes(Path.Combine(Dir, $"{to}_{at:0.00}s.jpg"), tex.EncodeToJPG(85));
                    Object.Destroy(tex);
                }
                while (App.Router.Busy) yield return null;
                yield return new WaitForSecondsRealtime(0.5f);
            }
            Debug.Log("[Mây] Đã chụp: " + Dir);
        }
    }
}
