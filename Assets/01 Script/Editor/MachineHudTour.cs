// Tour soi đầu máy bi (người dùng 2026-11-27): thanh kinh nghiệm + ô cấp đẩy lên theo khoảng dư trên đầu máy, nút PUSH to hơn có quầng
// sáng thở khi bấm được, bong bóng "Mốc sau ×M / cần N bi" trên viên cược khi đã ở mức cao nhất đang mở (MachineScene.LiftHeader,
// BuildPushGlow, BuildBetNote). Vào máy bi, cho số bi vừa đủ mở mức thứ hai của xSteps (chưa đủ mức thứ ba), chọn mức đó; chụp ở các
// khung màn GameViewSizes.Frames (9:16, 9:20, 3:4) hai nhịp quầng; rồi hết bi (quầng tắt, bong bóng báo mức ×2). Sao lưu và trả bản lưu,
// trả Game view về khung cũ. Menu "PokiClash/Thử/Máy bi/đầu máy, nút PUSH, bong bóng mốc cược (chụp)" hoặc cờ Temp/machine_hud_tour.flag
// (Unity không Play: tự vào Play, xong tự Stop). Ảnh: Temp/PokiShots/dau_may/*.png; log "[Đầu máy]".
using System.Collections;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class MachineHudTour
    {
        const BindingFlags F = BindingFlags.NonPublic | BindingFlags.Instance;
        static double nextPoll, tourStart;
        static bool stopAfter;
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/machine_hud_tour.flag"));
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/dau_may"));

        [MenuItem("PokiClash/Thử/Máy bi/đầu máy, nút PUSH, bong bóng mốc cược (chụp)", priority = 120)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "menu");
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
                SessionState.SetBool("MachineHudTour", true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                Debug.LogWarning("[Đầu máy] Tour quá 150 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("MachineHudTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("MachineHudTour", false);
                Application.runInBackground = true; // Unity nằm nền vẫn chạy vòng game
                stopAfter = true;
                BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(Dir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static void Call(object o, string m) => o.GetType().GetMethod(m, F)?.Invoke(o, null);
        static void Set(object o, string f, object v) => o.GetType().GetField(f, F)?.SetValue(o, v);

        static IEnumerator Tour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var gv = typeof(Editor).Assembly.GetType("UnityEditor.GameView");
            var win = gv != null ? EditorWindow.GetWindow(gv) : null;
            var idx = gv?.GetProperty("selectedSizeIndex", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            object orig = win && idx != null ? idx.GetValue(win) : null;
            try
            {
                App.Router.Go(SceneIds.Machine);
                float t0 = Time.realtimeSinceStartup;
                MachineScene scene = null;
                while ((!(scene = Object.FindAnyObjectByType<MachineScene>()) || App.Router.Busy) && Time.realtimeSinceStartup - t0 < 25) yield return null;
                yield return new WaitForSecondsRealtime(1.5f);
                if (!scene)
                {
                    Debug.LogWarning("[Đầu máy] không vào được máy bi");
                    yield break;
                }
                var s = App.Save.Data;
                var steps = App.Data.Cfg.xSteps;
                if (steps.Count >= 2)
                {
                    // vừa đủ mức thứ hai, chưa đủ mức thứ ba: viên ở mức cao nhất đang mở → bong bóng báo mức kế
                    s.balls = Mathf.Max(steps[1].balls, steps[1].x);
                    Set(scene, "x", steps[1].x);
                    scene.Refresh();
                }
                yield return new WaitForSecondsRealtime(0.6f);
                foreach (var f in GameViewSizes.Frames)
                {
                    if (!GameViewSizes.Select(f.x, f.y)) continue;
                    yield return new WaitForSecondsRealtime(0.5f);
                    Call(scene, "LiftHeader"); // đổi khung màn: tính lại khoảng dư trên đầu máy
                    yield return new WaitForSecondsRealtime(0.3f);
                    yield return Shot($"1_khung_{f.x}x{f.y}_a");
                    yield return new WaitForSecondsRealtime(0.8f);
                    yield return Shot($"1_khung_{f.x}x{f.y}_b");
                }
                // hết bi: quầng tắt, viên về ×1, bong bóng báo mức ×2
                s.balls = 0;
                scene.Refresh();
                yield return new WaitForSecondsRealtime(1.2f);
                yield return Shot("2_het_bi");
                Debug.Log("[Đầu máy] Xong tour: " + Dir);
            }
            finally
            {
                if (orig != null)
                    gv.GetMethod("SizeSelectionCallback", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)?.Invoke(win, new[] { orig, null });
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
                if (stopAfter)
                {
                    stopAfter = false;
                    tourStart = 0;
                    EditorApplication.isPlaying = false;
                }
            }
        }
    }
}
