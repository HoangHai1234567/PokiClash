// Tour chụp bản đồ thế giới ở sảnh (đang Play): "PokiClash/Thử/Sảnh bản đồ thế giới: mây che, mở đảo, kéo 4 hướng".
// 1. Người chơi mới: chưa có tướng khởi đầu, mây che hết (hộp chọn tướng hiện), chụp rồi đóng hộp;
// 2. chọn tướng khởi đầu hệ Mộc: diễn tan mây đảo Mộc, chụp liên tục;
// 3. thắng ải 1 (tạm thay trận hướng dẫn): vào lại sảnh, diễn tan mây bốn đảo còn lại, chụp liên tục;
// 4. kéo tới 4 góc, chụp; chạm vào cột công trình bên phải không cần.
// Ảnh vào Temp/PokiShots/sanh/; xong trả bản lưu như trước.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HubMapTour
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "sanh");

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Sảnh bản đồ thế giới: mây che, mở đảo, kéo 4 hướng (đang Play)", priority = 140)]
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

        static IEnumerator GoHub()
        {
            App.Router.Go(SceneIds.Notebook);
            yield return WaitRouter(SceneIds.Notebook);
            App.Router.Go(SceneIds.Hub);
            yield return WaitRouter(SceneIds.Hub);
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
                string moc = d.Starters.FirstOrDefault(id => d.Hero(id)?.elem == Elem.Moc) ?? d.Starters[0];
                // 1. người chơi mới
                s.intro = true;
                s.starter = null;
                for (int i = 0; i < s.zones.Length; i++) s.zones[i] = 0;
                HubIslands.SetShown(s, 0);
                yield return GoHub();
                yield return new WaitForSecondsRealtime(1.6f);
                yield return Shot("1_moi_choi_hop_chon");
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot("1_moi_choi_may_che_het");
                // 2. chọn tướng khởi đầu hệ Mộc
                s.ChooseStarter(moc);
                Object.FindAnyObjectByType<HubScene>()?.Refresh();
                for (int k = 0; k < 12; k++)
                {
                    yield return new WaitForSecondsRealtime(k == 0 ? 0.3f : 0.32f);
                    yield return Shot($"2_tan_moc_{k:00}");
                }
                yield return new WaitForSecondsRealtime(1f);
                yield return Shot("2_moc_da_mo");
                // 3. thắng ải 1 đảo Mộc (tạm thay trận hướng dẫn): tan nốt
                s.zones[(int)Elem.Moc] = 1;
                yield return GoHub();
                for (int k = 0; k < 14; k++)
                {
                    yield return new WaitForSecondsRealtime(k == 0 ? 0.3f : 0.35f);
                    yield return Shot($"3_tan_het_{k:00}");
                }
                yield return new WaitForSecondsRealtime(1.2f);
                yield return Shot("3_mo_het");
                // 4. kéo 4 hướng
                var pan = Object.FindAnyObjectByType<HubPan>();
                foreach (var (tag, o) in new[] { ("tren_trai", new Vector2(3000, -3000)), ("tren_phai", new Vector2(-3000, -3000)),
                             ("duoi_trai", new Vector2(3000, 3000)), ("duoi_phai", new Vector2(-3000, 3000)), ("giua", Vector2.zero) })
                {
                    pan.SetOffset(o);
                    yield return new WaitForSecondsRealtime(2.2f); // dây chun kéo về sát giới hạn
                    yield return Shot("4_keo_" + tag);
                }
                // 5. chạm đảo: nhún, quầng bừng lên (Poke: không chuyển màn)
                var arts = Object.FindObjectsByType<HubIslandArt>(FindObjectsSortMode.None);
                var thuy = System.Array.Find(arts, a => a.Zone == Elem.Thuy);
                if (thuy && pan)
                {
                    pan.GlideTo((RectTransform)thuy.transform);
                    yield return new WaitForSecondsRealtime(1.4f);
                    yield return Shot("5_dao_sang");
                    thuy.Poke();
                    for (int k = 0; k < 7; k++)
                    {
                        yield return new WaitForSecondsRealtime(0.06f);
                        yield return Shot($"5_nhun_{k}");
                    }
                }
                Debug.Log("[Thử] Xong sảnh bản đồ thế giới: " + Path.GetFullPath(Dir));
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(82));
            Object.DestroyImmediate(tex);
        }
    }
}
