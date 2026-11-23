// Tour thử phần rừng màn Nhà (người dùng 2026-11-23): bong bóng bi trên ô rừng, bảng Dọn, cây bay lên trời từng khung, gió lay cây,
// cây lắc, bướm / ong / đàn chim. Menu "PokiClash/Thử/Nhà và side meta/Nhà và side meta∕Nhà: rừng bay, gió, chim bướm (chụp)" hoặc cờ Temp/home_forest_tour.flag (Unity
// đang không Play). Bản lưu thử (Nhà dựng lại, cấp 30, ban ngày), xong trả lại Nhà, cấp, bi, tướng đã có rồi Stop.
// Ảnh: Temp/PokiShots/forest/rung_*.png; log "[Rừng]".
using System.Collections;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HomeForestTour
    {
        const BindingFlags F = BindingFlags.NonPublic | BindingFlags.Instance;
        static double nextPoll, tourStart;
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/home_forest_tour.flag"));

        [MenuItem("PokiClash/Thử/Nhà và side meta/Nhà và side meta∕Nhà: rừng bay, gió, chim bướm (chụp)", priority = 210)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "1");
        }

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            if (!EditorApplication.isPlayingOrWillChangePlaymode)
            {
                if (!File.Exists(Flag)) return;
                File.Delete(Flag);
                SessionState.SetBool("HomeForestTour", true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 120)
            {
                Debug.LogWarning("[Rừng] Tour quá 120 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("HomeForestTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("HomeForestTour", false);
                BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        static object Get(object o, string field) => o.GetType().GetField(field, F)?.GetValue(o);
        static void Set(object o, string field, object v) => o.GetType().GetField(field, F)?.SetValue(o, v);
        static object Call(object o, string method, params object[] args) => o.GetType().GetMethod(method, F)?.Invoke(o, args);

        static IEnumerator Tour()
        {
            var dir = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/forest"));
            Directory.CreateDirectory(dir);
            var s = App.Save.Data;
            var keepHome = s.home;
            int keepLevel = s.level, keepBalls = s.balls;
            var keepOwned = App.Data.Heroes.Take(6).Select(h => (h.id, s.Hero(h.id).owned)).ToList();
            foreach (var h in App.Data.Heroes.Take(6)) s.Hero(h.id).owned = true;
            s.home = null;
            if (s.level < 30) s.level = 30;
            DayCycle.Override = 11f;
            App.Router.Go(SceneIds.Home);
            HomeScene home = null;
            for (float t = 0; t < 25 && !(home && App.Router.CurrentRoot == home); t += 0.25f)
            {
                yield return new WaitForSecondsRealtime(0.25f);
                home = Object.FindFirstObjectByType<HomeScene>();
                // Nhà mới dựng: lần đầu cập bến máy lướt lên Nhà chính 1,1 giây (HomeScene.Update) làm lệch các khung chụp; bỏ cú lướt đó
                if (App.Save.Data.home != null) App.Save.Data.home.dockIntro = true;
            }
            for (float t = 0; t < 10 && PierShip.Active && PierShip.Active.Busy; t += 0.25f) yield return new WaitForSecondsRealtime(0.25f);
            yield return new WaitForSecondsRealtime(2.5f);
            if (home) Set(home, "shipArriving", false);
            void Shot(string n)
            {
                ScreenCapture.CaptureScreenshot(Path.Combine(dir, "rung_" + n + ".png"));
                Debug.Log("[Rừng] chụp " + n);
            }
            if (!home)
            {
                Debug.LogWarning("[Rừng] không vào được màn Nhà");
            }
            else
            {
                var hs = App.Save.Data.home;
                var d = App.Data;
                var c = d.Cfg.home;
                hs.wood = 5000;
                hs.ore = 5000;
                int n = Home.LotsPerSide(c), lot = -1;
                for (int l = 0; l < n * n && lot < 0; l++)
                    if (Home.CanClear(s, d, l) == HomeErr.Ok)
                        lot = l;
                var view = Get(home, "landView") as LandView;
                Debug.Log($"[Rừng] ô dọn thử: {lot} (vòng {(lot >= 0 ? Home.Ring(c, lot) : -1)}, bi {(lot >= 0 ? Home.RingOf(c, lot)?.balls ?? 0 : 0)})");
                if (lot >= 0 && view)
                {
                    var (i, j) = Home.LotIJ(c, lot);
                    var mid = (Vector2)Call(home, "CellTop", i * c.lot + c.lot / 2f, j * c.lot + c.lot / 2f);
                    home.Refresh();
                    view.Show(mid - new Vector2(0, 260), 1f, 0); // ô rừng ở nửa dưới khung: còn chỗ phía trên thấy cây bay
                    yield return new WaitForSecondsRealtime(1.6f); // Labels mỗi giây: bong bóng hiện
                    Shot("1_bong_bong");
                    yield return null;
                    yield return null;
                    yield return new WaitForSecondsRealtime(0.4f);
                    Call(home, "TapLot", lot);
                    yield return new WaitForSecondsRealtime(0.6f);
                    Shot("2_bang_don");
                    yield return null;
                    yield return null;
                    // dọn rồi cho xong ngay (như quảng cáo rút giờ): cây bay, bi bay
                    var e = Home.ClearLot(s, d, SaveService.Now(), lot);
                    Debug.Log($"[Rừng] ClearLot {e}");
                    hs.clearing[lot] = SaveService.Now() - 1;
                    Home.Tick(s, d, SaveService.Now());
                    int ballsBefore = s.balls;
                    Call(home, "ReportCleared");
                    var fly = Get(home, "flyTrees") as IList;
                    Debug.Log($"[Rừng] cây đang bay: {fly?.Count ?? -1}; bi {ballsBefore}");
                    float t0 = Time.unscaledTime;
                    for (int k = 0; k < 24; k++) // 24 khung cách 0,066 s (~1,6 s): ghép GIF soi nhịp nén giãn
                    {
                        float at = 0.02f + k * 0.066f;
                        while (Time.unscaledTime - t0 < at) yield return null;
                        Shot("3_bay_" + k.ToString("00"));
                        yield return null;
                    }
                    yield return new WaitForSecondsRealtime(0.8f);
                    Shot("3_bay_xong");
                    yield return null;
                    yield return null;
                }
                // bướm, ong (khung đang nhìn: quanh làng)
                var main = Home.Main(hs);
                if (main != null && view)
                {
                    int ms = Home.Def(d.Cfg, main.def).size;
                    view.Show((Vector2)Call(home, "CellTop", main.gx + ms / 2f, main.gy + ms + 3f), 1f, 0);
                }
                yield return new WaitForSecondsRealtime(3f);
                Shot("4_buom_ong");
                yield return null;
                yield return null;
                var crit = Get(home, "critters") as IList;
                int on = 0;
                if (crit != null)
                    foreach (var o in crit)
                        if ((bool)o.GetType().GetField("on").GetValue(o))
                            on++;
                Debug.Log($"[Rừng] bướm/ong/chim đang bay: {on}/{crit?.Count ?? -1}");
                // bướm, ong, đàn chim: 20 khung cách 0,1 s
                Set(home, "flockWait", 0f);
                yield return new WaitForSecondsRealtime(0.5f);
                for (int k = 0; k < 20; k++)
                {
                    Shot("5_song_" + k.ToString("00"));
                    yield return new WaitForSecondsRealtime(0.1f);
                }
                // cây lắc: soi một ô rừng còn khoá
                for (int l = 0; l < n * n; l++)
                {
                    if (hs.lots.Contains(l) || Home.LotKind(c, l) == "hill") continue;
                    var (i2, j2) = Home.LotIJ(c, l);
                    view.Show((Vector2)Call(home, "CellTop", i2 * c.lot + c.lot / 2f, j2 * c.lot + c.lot / 2f), 1f, 0);
                    break;
                }
                yield return new WaitForSecondsRealtime(1f);
                Set(home, "shakeWait", 0f); // một cây lắc ngay trong chuỗi
                for (int k = 0; k < 20; k++) // gió: 20 khung cách 0,08 s
                {
                    Shot("6_gio_" + k.ToString("00"));
                    yield return new WaitForSecondsRealtime(0.08f);
                }
                var shake = Get(home, "shakeImg") as UnityEngine.UI.Image;
                Debug.Log($"[Rừng] cây lắc: {(shake ? shake.name + " góc " + shake.rectTransform.localEulerAngles.z.ToString("0.0") : "không")}");
                yield return new WaitForSecondsRealtime(0.5f);
            }
            DayCycle.Override = null;
            s.home = keepHome;
            s.level = keepLevel;
            s.balls = keepBalls;
            foreach (var (id, owned) in keepOwned) s.Hero(id).owned = owned;
            App.Save.Save();
            Debug.Log("[Rừng] Xong tour (đã trả bản lưu)");
            tourStart = 0;
            EditorApplication.isPlaying = false;
        }
    }
}
