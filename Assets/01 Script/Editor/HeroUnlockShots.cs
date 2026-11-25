// Chụp màn mở khoá tướng theo khung (soi bút chì màu, thu hình vừa trang; 2026-11-25). Không cần bấm menu (Unity dùng chung nhiều
// phiên): ghi mã tướng cách nhau dấu phẩy vào Temp/unlock_shots.flag. Unity (không Play, biên dịch xong) mở Boot, vào Play, chạy cả
// khi nằm nền, diễn lần lượt từng tướng, chụp mỗi 0,2 s vào Temp/PokiShots/mo_khoa_but_mau/<mã>_<số>.jpg, xong thì Stop.
// Cảnh đang mở có thay đổi chưa lưu thì bỏ (không đè việc của phiên khác). Màn mở khoá không ghi bản lưu.
using System.Collections;
using System.IO;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HeroUnlockShots
    {
        const string Key = "UnlockShotsIds";
        static double nextPoll;
        static string FlagPath => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/unlock_shots.flag"));
        static string Dir => Path.Combine(PlayTour.ShotDir, "mo_khoa_but_mau");

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 0.5;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            if (!EditorApplication.isPlayingOrWillChangePlaymode)
            {
                if (!File.Exists(FlagPath)) return;
                var ids = File.ReadAllText(FlagPath).Trim();
                File.Delete(FlagPath);
                const string boot = "Assets/00 Scenes/Boot.unity";
                var active = UnityEngine.SceneManagement.SceneManager.GetActiveScene();
                if (active.path != boot)
                {
                    if (active.isDirty)
                    {
                        Debug.LogWarning("[Mở khoá tướng] Cảnh đang mở chưa lưu: bỏ lượt chụp.");
                        return;
                    }
                    UnityEditor.SceneManagement.EditorSceneManager.OpenScene(boot);
                }
                SessionState.SetString(Key, ids);
                EditorApplication.isPlaying = true;
                return;
            }
            if (!EditorApplication.isPlaying) return;
            var s = SessionState.GetString(Key, "");
            if (s == "") return;
            Application.runInBackground = true; // game tắt Run In Background: Unity nằm nền thì Play đứng
            if (App.I == null || App.Router == null || App.Router.CurrentRoot == null) return;
            SessionState.EraseString(Key);
            BootTitle.Dismiss();
            App.I.StartCoroutine(Run(s.Split(',')));
        }

        static IEnumerator Run(string[] ids)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Booting || BootTitle.Current || StoryIntro.Current) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(1.5f);
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            int shots = 0;
            foreach (var raw in ids)
            {
                var id = raw.Trim();
                var h = App.Data.Hero(id);
                if (h == null)
                {
                    Debug.LogWarning("[Mở khoá tướng] Không có tướng " + id);
                    continue;
                }
                var form = HeroArt.FormOf(h).aola;
                t0 = Time.realtimeSinceStartup;
                while (!string.IsNullOrEmpty(form) && !Game.AolaActor.Ready(form) && Time.realtimeSinceStartup - t0 < 10) yield return null;
                HeroUnlockView.Play(new[] { id });
                float start = Time.realtimeSinceStartup;
                for (int k = 0; Time.realtimeSinceStartup - start < 7.2f; k++)
                {
                    yield return new WaitForSecondsRealtime(0.2f);
                    yield return new WaitForEndOfFrame();
                    var tex = ScreenCapture.CaptureScreenshotAsTexture();
                    File.WriteAllBytes(Path.Combine(Dir, $"{id}_{k:00}.jpg"), tex.EncodeToJPG(82));
                    Object.Destroy(tex);
                    shots++;
                }
                var v = Object.FindAnyObjectByType<HeroUnlockView>();
                if (v)
                    foreach (var b in v.GetComponentsInChildren<SketchButton>())
                        if (b.name == "nut_tiep") b.SimulateClick();
                yield return new WaitForSecondsRealtime(0.6f);
            }
            Debug.Log($"[Mở khoá tướng] Chụp xong {shots} ảnh ở {Dir}");
            EditorApplication.isPlaying = false;
        }
    }
}
