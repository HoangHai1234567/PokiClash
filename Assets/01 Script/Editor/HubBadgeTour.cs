// Tour soi nút sảnh kiểu huy hiệu (HubBadgeMenu, 2026-11-27): vào sảnh, chụp ở khung 1080 x 1920 (đủ nét) rồi 1080 x 2400, trả Game view
// về khung cũ. Cờ Temp/hub_badge_tour.flag (Unity không Play: tự vào Play, xong tự Stop) hoặc menu
// "PokiClash/Thử/Sảnh/nút huy hiệu (chụp)". Không ghi bản lưu. Ảnh: Temp/PokiShots/nut_sanh/*.png; log "[Nút sảnh]".
// Chế độ "về sảnh" (người dùng 2026-11-27: "về home lại mất nút setting"): cờ Temp/hub_badge_back_tour.flag hoặc menu
// "PokiClash/Thử/Sảnh/nút bánh răng sau khi về sảnh (chụp)": bấm nút bánh răng vào Sổ tay rồi quay lại, đi Nhà, Tướng, Hang rồi quay lại;
// mỗi lần về sảnh chụp một ảnh và ghi trạng thái nút (Temp/PokiShots/nut_sanh/ve_log.txt); ở màn Nhà soi nút bánh răng của thanh màn con,
// bấm vào Sổ tay rồi quay lại phải về Nhà. Sao lưu bản lưu đầu tour, trả lại cuối tour.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HubBadgeTour
    {
        static double nextPoll, tourStart;
        static bool stopAfter, backMode;
        static readonly List<string> log = new List<string>();
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/hub_badge_tour.flag"));
        static string BackFlag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/hub_badge_back_tour.flag"));
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/nut_sanh"));

        [MenuItem("PokiClash/Thử/Sảnh/nút huy hiệu (chụp)")]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "menu");
        }

        [MenuItem("PokiClash/Thử/Sảnh/nút bánh răng sau khi về sảnh (chụp)")]
        static void RunBack()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(BackTour());
                return;
            }
            File.WriteAllText(BackFlag, "menu");
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
                bool shots = File.Exists(Flag), back = File.Exists(BackFlag);
                if (!shots && !back) return;
                if (shots) File.Delete(Flag);
                if (back) File.Delete(BackFlag);
                SessionState.SetBool("HubBadgeTour", true);
                SessionState.SetBool("HubBadgeTourBack", back && !shots);
                tourStart = EditorApplication.timeSinceStartup;
                // Play từ cảnh Boot dù đang mở cảnh khác (mở Hub.unity thì Play không có App, tour không chạy)
                NuocFxMenu.PlayTuBoot();
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 240)
            {
                Debug.LogWarning("[Nút sảnh] Tour quá 240 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("HubBadgeTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("HubBadgeTour", false);
                backMode = SessionState.GetBool("HubBadgeTourBack", false);
                Application.runInBackground = true; // Unity nằm nền vẫn chạy vòng game
                stopAfter = true;
                BootTitle.Dismiss();
                App.I.StartCoroutine(backMode ? BackTour() : Tour());
            }
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(Dir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
            Debug.Log("[Nút sảnh] chụp " + name);
        }

        static IEnumerator Tour()
        {
            if (!(App.Router.CurrentRoot is HubScene)) App.Router.Go(SceneIds.Hub);
            float t0 = Time.realtimeSinceStartup;
            while ((!(App.Router.CurrentRoot is HubScene) || App.Router.Busy) && Time.realtimeSinceStartup - t0 < 25) yield return null;
            yield return new WaitForSecondsRealtime(3f);
            var gv = typeof(Editor).Assembly.GetType("UnityEditor.GameView");
            var win = gv != null ? EditorWindow.GetWindow(gv) : null;
            var idx = gv?.GetProperty("selectedSizeIndex", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            object orig = win && idx != null ? idx.GetValue(win) : null;
            foreach (var f in new[] { GameViewSizes.Frames[0], GameViewSizes.Frames[1] })
            {
                if (!GameViewSizes.Select(f.x, f.y)) continue;
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot($"sanh_{f.x}x{f.y}");
            }
            if (orig != null)
                gv.GetMethod("SizeSelectionCallback", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)?.Invoke(win, new[] { orig, null });
            Debug.Log("[Nút sảnh] Xong tour: " + Dir);
            Finish();
        }

        static void Finish()
        {
            if (!stopAfter) return;
            stopAfter = false;
            tourStart = 0;
            EditorApplication.isPlaying = false;
        }

        // ---------- chế độ về sảnh ----------

        const BindingFlags Priv = BindingFlags.NonPublic | BindingFlags.Instance;

        static void Note(string s)
        {
            log.Add(s);
            Debug.Log("[Nút sảnh] " + s);
        }

        static SketchButton Notebook() => App.Bars ? typeof(TopBars).GetField("notebookBtn", Priv)?.GetValue(App.Bars) as SketchButton : null;

        // nút Sổ tay của thanh màn con (màn Nhà)
        static SketchButton BackNotebook() => App.Bars ? typeof(TopBars).GetField("backNotebook", Priv)?.GetValue(App.Bars) as SketchButton : null;

        static IEnumerator Tap(SketchButton btn)
        {
            if (!btn) yield break;
            btn.OnPointerDown(null);
            yield return new WaitForSecondsRealtime(0.12f);
            btn.OnPointerUp(null);
            btn.OnPointerClick(null);
        }

        static string State(SketchButton btn = null)
        {
            btn = btn ? btn : Notebook();
            if (!btn) return "KHÔNG có notebookBtn";
            var rt = btn.Rect;
            var bg = typeof(SketchButton).GetField("bg", Priv)?.GetValue(btn) as Image;
            string off = "";
            for (var t = rt.parent; t; t = t.parent)
                if (!t.gameObject.activeSelf) off += t.name + " ";
            float group = 1;
            foreach (var g in btn.GetComponentsInParent<CanvasGroup>(true)) group *= g.alpha;
            var c = new Vector3[4];
            rt.GetWorldCorners(c);
            var cam = PokiCanvas.UiCamera;
            Vector2 a = RectTransformUtility.WorldToScreenPoint(cam, c[0]), b = RectTransformUtility.WorldToScreenPoint(cam, c[2]);
            var canvas = btn.GetComponentInParent<Canvas>();
            string kids = "";
            foreach (Transform k in rt) kids += $"{k.name}:{(k.gameObject.activeSelf ? "bật" : "tắt")} ";
            string bgs = bg ? $"bg {bg.name} bật {bg.enabled} hiện {bg.gameObject.activeInHierarchy} sprite {(bg.sprite ? bg.sprite.name : "null")} màu {bg.color} alpha {bg.canvasRenderer.GetAlpha():0.00}" : "bg null";
            return $"nút hiện {btn.gameObject.activeInHierarchy} (tự {btn.gameObject.activeSelf}), cha tắt [{off}], nhóm alpha {group:0.00}, " +
                   $"canvas {(canvas ? canvas.name + (canvas.enabled ? " bật" : " TẮT") + " thứ tự " + canvas.sortingOrder : "không")}, scale {rt.localScale}, " +
                   $"chỗ {rt.anchoredPosition}, cỡ {rt.sizeDelta}, trên màn {a} → {b} (màn {Screen.width}x{Screen.height}), {bgs}, con [{kids}]";
        }

        static IEnumerator WaitScene(string id, float timeout = 25)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Current != id || App.Router.Busy) && Time.realtimeSinceStartup - t0 < timeout) yield return null;
            if (App.Router.Current != id) Note($"CẢNH BÁO: chờ {id} quá {timeout} giây (đang ở {App.Router.Current})");
        }

        static IEnumerator BackHome(string tag)
        {
            App.Modals.CloseAll();
            App.Back();
            yield return WaitScene(SceneIds.Hub);
            yield return new WaitForSecondsRealtime(2f);
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.5f);
            Note($"{tag}: {State()}");
            yield return Shot("ve_" + tag);
        }

        static IEnumerator BackTour()
        {
            log.Clear();
            var path = App.Save.FilePath;
            byte[] backup = File.Exists(path) ? File.ReadAllBytes(path) : null;
            try
            {
                if (!(App.Router.CurrentRoot is HubScene)) App.Router.Go(SceneIds.Hub);
                yield return WaitScene(SceneIds.Hub);
                yield return new WaitForSecondsRealtime(3f);
                App.Modals.CloseAll();
                Note($"0_sanh_dau: {State()}");
                yield return Shot("ve_0_sanh_dau");

                // bấm nút bánh răng như người chơi (đè, thả, chạm) vào Sổ tay rồi quay lại
                yield return Tap(Notebook());
                yield return WaitScene(SceneIds.Notebook);
                yield return new WaitForSecondsRealtime(1.5f);
                yield return BackHome("1_tu_so_tay");

                foreach (var (id, tag) in new[] { (SceneIds.Home, "2_tu_nha"), (SceneIds.Heroes, "3_tu_tuong"), (SceneIds.Cave, "4_tu_hang") })
                {
                    App.Router.Go(id);
                    yield return WaitScene(id);
                    yield return new WaitForSecondsRealtime(2f);
                    if (id == SceneIds.Home)
                    {
                        // màn Nhà: nút bánh răng trên thanh màn con; bấm vào Sổ tay rồi quay lại phải về Nhà
                        App.Modals.CloseAll();
                        yield return new WaitForSecondsRealtime(0.5f);
                        Note(BackNotebook() ? $"nha: {State(BackNotebook())}" : "nha: KHÔNG có nút Sổ tay của thanh màn con");
                        yield return Shot("ve_nha_0");
                        yield return Tap(BackNotebook());
                        yield return WaitScene(SceneIds.Notebook);
                        yield return new WaitForSecondsRealtime(1.5f);
                        App.Back();
                        yield return WaitScene(SceneIds.Home);
                        yield return new WaitForSecondsRealtime(2f);
                        App.Modals.CloseAll();
                        Note($"nha_tu_so_tay: đang ở {App.Router.Current}; " + (BackNotebook() ? State(BackNotebook()) : "KHÔNG có nút"));
                        yield return Shot("ve_nha_1_tu_so_tay");
                    }
                    yield return BackHome(tag);
                }
                Note("Xong: " + Dir);
            }
            finally
            {
                App.Modals.CloseAll();
                if (backup != null)
                {
                    File.WriteAllBytes(path, backup);
                    App.Save.Load();
                    bool same = File.ReadAllBytes(path).Length == backup.Length;
                    Note(same ? "đã trả bản lưu cũ" : "CẢNH BÁO: bản lưu đọc lại lệch cỡ bản sao lưu");
                }
                Directory.CreateDirectory(Dir);
                File.WriteAllLines(Path.Combine(Dir, "ve_log.txt"), log);
                Debug.Log("[Nút sảnh] KẾT THÚC TOUR về sảnh");
                Finish();
            }
        }
    }
}
