// Chụp thử màn chọn tướng khởi đầu (vòng 3D, 2026-11-24): mở màn (không chọn), chụp lúc con đầu tung chiêu, giữa hai con, rồi xoay
// tới con 2 và con 4; xong đóng màn. Ảnh ra Temp/PokiShots/chon_tuong/. Bản lưu không đổi (không bấm Chọn).
using System.Collections;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class StarterRingShots
    {
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/chon_tuong"));

        [MenuItem("PokiClash/Thử/Người chơi mới/Màn chọn tướng: vòng 3D, chụp (đang Play)", priority = 143)]
        static void Run()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.Log("[Chọn tướng] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Tour());
        }

        static IEnumerator Tour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.3f);
            var dlg = App.Modals.Open<StarterDialog>(mandatory: true);
            dlg.Show();
            yield return new WaitForSecondsRealtime(1.2f);
            yield return Shot("0_mo");
            yield return new WaitForSecondsRealtime(0.5f); // con đầu tung chiêu lúc dừng hẳn
            yield return Shot("1_chieu");
            dlg.DebugRotate(0.5f);
            yield return new WaitForSecondsRealtime(0.3f);
            yield return Shot("2_giua_hai_con");
            dlg.DebugRotate(1);
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("3_con_2");
            dlg.DebugRotate(3);
            yield return new WaitForSecondsRealtime(2.2f);
            yield return Shot("4_con_4");
            dlg.DebugRotate(-1);
            yield return new WaitForSecondsRealtime(5f); // chờ vài trò vui
            yield return Shot("5_con_5");
            dlg.Close();
            Debug.Log("[Chọn tướng] Đã chụp vòng 3D: " + Dir);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(85));
            Object.Destroy(tex);
        }
    }
}
