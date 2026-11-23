// Thử hướng dẫn đặt Cây bi ở Nhà và chạm tán lá (đang Play, 2026-11-23). Giả người chơi mới vừa mở Nhà: cờ hướng dẫn chỉ còn chuỗi bắt
// buộc xong (c17) và G1–G2, bỏ mọi Cây bi trong nhà, bật Gợi ý. Vào Nhà, đi lần lượt G3a (nút Xây) → G3b (thẻ Cây bi đầu khay) → G3c
// (bóng ma, rồi Đặt) → G3d (chạm cây) bằng chạm giả của lớp phủ, chụp mỗi bước vào Temp/PokiShots (3xx_*.png). Ở G3d chạm vào một
// điểm trên tán lá nằm ngoài các ô dưới chân cây (HomeScene.OnTap) và kiểm số bi có tăng. Xong trả lại bản lưu như trước khi thử.
using System.Collections;
using System.IO;
using System.Reflection;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HomeTreeTour
    {
        const BindingFlags Any = BindingFlags.Instance | BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public;
        static int shot;

        [MenuItem("PokiClash/Thử/Nhà và side meta/Nhà và side meta∕Nhà: hướng dẫn đặt Cây bi, chạm tán lá (đang Play)", priority = 125)]
        static void Run()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(Tour());
        }

        static IEnumerator Tour()
        {
            shot = 300;
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            try
            {
                var s = App.Save.Data;
                var d = App.Data;
                double now = PokiClash.Game.SaveService.Now();
                foreach (var h in d.Heroes)
                {
                    if (Home.Open(s, d.Cfg)) break;
                    s.Hero(h.id).owned = true;
                }
                if (PokiClash.Core.Progress.TotalCleared(s) == 0) s.zones[0] = 1;
                Home.Of(s, d, now);
                s.home.buildings.RemoveAll(b => b.def == "tree");
                Tutorial.Begin(s);
                Tutorial.MarkAll(s, Tutorial.Free, "g1", "g2");
                s.settings.hints = true;
                App.Save.Save();
                Debug.Log($"[Thử cây bi] Cây chờ đặt: {Home.TreesWaiting(s, d)}, bi {s.balls}");

                App.Router.Go(SceneIds.Home);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Home) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(4f); // tàu cập bến, máy lướt lên Nhà chính
                var home = Object.FindAnyObjectByType<HomeScene>();
                if (!home)
                {
                    Debug.LogError("[Thử cây bi] Không thấy màn Nhà");
                    yield break;
                }

                yield return Step(Tutorial.TreeBuild, "xay", true);
                yield return Step(Tutorial.TreeTray, "khay", true);
                yield return Step(Tutorial.TreeSpot, "bong_ma", false);
                home.GetType().GetMethod("PlaceGhost", Any).Invoke(home, null);
                Debug.Log($"[Thử cây bi] Đã đặt: cây trong nhà {Home.CountOf(s.home, "tree")}, cờ g3t {Tutorial.Done(s, Tutorial.TreePlaced)}");

                yield return WaitShown(Tutorial.TreeTap);
                yield return Shot("hai");
                // chạm tán lá: điểm ở 30% chiều cao khung hình cây, giữa ngang; phải nằm ngoài các ô dưới chân
                var objs = (System.Collections.Generic.Dictionary<int, HomeObject>)home.GetType().GetField("objs", Any).GetValue(home);
                HomeBuilding tree = s.home.buildings.Find(b => b.def == "tree");
                var o = objs[tree.id];
                var r = (Rect)home.GetType().GetMethod("ViewRect", Any).Invoke(null, new object[] { o.Rt });
                var p = new Vector2(r.center.x, r.yMin + r.height * 0.3f);
                var cell = (Vector2Int)home.GetType().GetMethod("CellAt", Any).Invoke(home, new object[] { p });
                var foot = Home.InMap(d.Cfg.home, cell.x, cell.y) ? Home.At(s.home, d.Cfg, cell.x, cell.y) : null;
                int before = s.balls;
                home.GetType().GetMethod("OnTap", Any).Invoke(home, new object[] { p });
                Debug.Log($"[Thử cây bi] Chạm tán lá tại {p} (ô {cell}, dưới chân là {(foot == null ? "đất trống" : foot.def)}): bi {before} → {s.balls}" +
                          (foot != tree && s.balls > before ? " ĐẠT" : " TRƯỢT"));
                yield return new WaitForSecondsRealtime(1.2f); // bi bay lên chip
                if (GuideOverlay.I && GuideOverlay.I.ShownId == Tutorial.TreeTap) GuideOverlay.I.DebugTap();
                yield return Shot("da_hai");
                Debug.Log($"[Thử cây bi] Cờ g3h {Tutorial.Done(s, Tutorial.TreeTap)}");
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                    App.Bars.Refresh();
                    Debug.Log("[Thử cây bi] Đã trả lại bản lưu như trước khi thử.");
                }
            }
            App.Router.Go(SceneIds.Hub);
            Debug.Log("[Thử cây bi] Xong.");
        }

        static IEnumerator WaitShown(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((!GuideOverlay.I || GuideOverlay.I.ShownId != id) && Time.realtimeSinceStartup - t0 < 12) yield return null;
            Debug.Log($"[Thử cây bi] Bước {id}: {(GuideOverlay.I && GuideOverlay.I.ShownId == id ? "hiện" : "KHÔNG hiện")} ({(GuideOverlay.I ? GuideOverlay.I.DebugState : "-")})");
            yield return new WaitForSecondsRealtime(0.9f); // nét khoanh vẽ xong
        }

        static IEnumerator Step(string id, string name, bool tap)
        {
            yield return WaitShown(id);
            yield return Shot(name);
            if (tap && GuideOverlay.I && GuideOverlay.I.ShownId == id) GuideOverlay.I.DebugTap();
            yield return new WaitForSecondsRealtime(0.5f);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"{shot++}_cay_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }
    }
}
