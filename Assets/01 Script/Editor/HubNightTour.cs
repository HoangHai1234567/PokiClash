// Tour chụp đèn đêm các đảo ở sảnh (đang Play): "PokiClash/Thử/Sảnh đèn đêm các đảo: 12h, 17h30, 18h30, 21h, từng đảo".
// Mở hết đảo (bỏ diễn tan mây), chụp cả bản đồ theo giờ, rồi lướt tới từng đảo lúc 21h chụp hai khung (thấy lửa nhảy), chạm đảo Thổ chụp
// lúc nhún. Ảnh vào Temp/PokiShots/sanh_dem/; xong trả bản lưu và giờ máy như trước.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HubNightTour
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "sanh_dem");

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Sảnh đèn đêm các đảo: 12h, 17h30, 18h30, 21h, từng đảo (đang Play)", priority = 141)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator WaitRouter(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*.jpg")) File.Delete(f);
            try
            {
                var s = App.Save.Data;
                var d = App.Data;
                s.intro = true;
                if (string.IsNullOrEmpty(s.starter))
                    s.ChooseStarter(d.Starters.FirstOrDefault(id => d.Hero(id)?.elem == Elem.Moc) ?? d.Starters[0]);
                if (!HubIslands.TutorialDone(s)) s.zones[(int)Elem.Moc] = 1;
                HubIslands.SetShown(s, HubIslands.All);
                App.Router.Go(SceneIds.Notebook);
                yield return WaitRouter(SceneIds.Notebook);
                App.Router.Go(SceneIds.Hub);
                yield return WaitRouter(SceneIds.Hub);
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(1.5f);
                var pan = Object.FindAnyObjectByType<HubPan>();
                if (pan) pan.SetOffset(Vector2.zero);
                foreach (var (tag, h) in new[] { ("12h", 12f), ("17h30", 17.5f), ("18h30", 18.5f), ("21h", 21f) })
                {
                    DayCycle.Override = h;
                    yield return new WaitForSecondsRealtime(1.2f);
                    yield return Shot("1_toan_" + tag);
                }
                DayCycle.Override = 21f;
                var arts = Object.FindObjectsByType<HubIslandArt>(FindObjectsSortMode.None);
                foreach (var e in new[] { Elem.Hoa, Elem.Kim, Elem.Moc, Elem.Tho, Elem.Thuy })
                {
                    var art = System.Array.Find(arts, a => a.Zone == e);
                    if (!art || !pan) continue;
                    pan.GlideTo((RectTransform)art.transform);
                    yield return new WaitForSecondsRealtime(1.5f);
                    yield return Shot($"2_{e.ToString().ToLower()}_a", 3);
                    yield return new WaitForSecondsRealtime(0.17f);
                    yield return Shot($"2_{e.ToString().ToLower()}_b", 3);
                }
                var tho = System.Array.Find(arts, a => a.Zone == Elem.Tho);
                if (tho && pan)
                {
                    pan.GlideTo((RectTransform)tho.transform);
                    yield return new WaitForSecondsRealtime(1.5f);
                    tho.Poke();
                    yield return new WaitForSecondsRealtime(0.12f);
                    yield return Shot("3_tho_nhun", 3);
                }
                Debug.Log("[Thử] Xong sảnh đèn đêm: " + Path.GetFullPath(Dir));
            }
            finally
            {
                DayCycle.Override = null;
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        // k > 1: cho camera chính vẽ vào ảnh lớn gấp k (ScreenCapture superSize làm vỡ canvas World Space); chỉ có lớp World Space
        static IEnumerator Shot(string name, int k = 1)
        {
            yield return new WaitForEndOfFrame();
            Texture2D tex;
            var cam = Camera.main;
            if (k <= 1 || !cam) tex = ScreenCapture.CaptureScreenshotAsTexture();
            else
            {
                int w = Screen.width * k, h = Screen.height * k;
                var rt = RenderTexture.GetTemporary(w, h, 24);
                var prev = cam.targetTexture;
                cam.targetTexture = rt;
                cam.Render();
                cam.targetTexture = prev;
                var act = RenderTexture.active;
                RenderTexture.active = rt;
                tex = new Texture2D(w, h, TextureFormat.RGB24, false);
                tex.ReadPixels(new Rect(0, 0, w, h), 0, 0);
                tex.Apply();
                RenderTexture.active = act;
                RenderTexture.ReleaseTemporary(rt);
            }
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(85));
            Object.DestroyImmediate(tex);
        }
    }
}
