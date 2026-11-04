// Thử chống thông báo dồn (ToastService, người dùng báo 2026-11-04: bấm liên tục ở máy bi khi hết bi thì thông báo chồng thành cột).
// Menu "PokiClash/Thử/Thông báo dồn (đang Play)": gọi 8 lần cùng một thông báo rồi 5 thông báo khác nhau, đếm số thông báo đang hiện
// (đúng: 1 sau loạt trùng; tối đa ToastService.MaxShown sau loạt khác nhau) và chụp màn vào Temp/PokiShots/x_thong_bao_don_*.png.
using System.Collections;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class ToastCheckMenu
    {
        [MenuItem("PokiClash/Thử/Thông báo dồn (đang Play)", priority = 301)]
        static void Run()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(Check());
        }

        static IEnumerator Check()
        {
            var host = App.Toasts.transform;
            for (int i = 0; i < 8; i++)
            {
                App.Toasts.Show("Hết bi rồi! Thắng ải để có thêm bi", App.Art.Icon("ball"));
                yield return new WaitForSecondsRealtime(0.08f);
            }
            yield return new WaitForSecondsRealtime(0.3f);
            int same = Count(host);
            for (int i = 0; i < 5; i++)
            {
                App.Toasts.Show($"Thông báo thử {i + 1}", App.Art.Icon("star"));
                yield return new WaitForSecondsRealtime(0.08f);
            }
            yield return new WaitForSecondsRealtime(0.6f);
            int diff = Count(host);
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            var dir = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots"));
            Directory.CreateDirectory(dir);
            File.WriteAllBytes(Path.Combine(dir, $"x_thong_bao_don_{tex.width}x{tex.height}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
            Debug.Log($"[Thử] Thông báo dồn: sau 8 lần trùng còn {same} (cần 1); sau 5 thông báo khác nhau còn {diff} (tối đa {ToastService.MaxShown})");
        }

        // số thông báo còn hiện rõ (bỏ cái đang mờ đi)
        static int Count(Transform host)
        {
            int n = 0;
            foreach (Transform c in host)
            {
                var cg = c.GetComponent<CanvasGroup>();
                if (c.gameObject.activeSelf && (!cg || cg.alpha > 0.95f)) n++;
            }
            return n;
        }
    }
}
