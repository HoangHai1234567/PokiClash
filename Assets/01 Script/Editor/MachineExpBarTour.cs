// Tour soi huy hiệu cấp trên thanh kinh nghiệm máy bi (2026-11-27, thay vòng cấp cũ bằng huy hiệu của thanh trên): vào máy bi,
// chụp lúc đứng yên, rồi gọi LevelPop chụp lúc huy hiệu nhún. Menu "PokiClash/Thử/Máy bi/huy hiệu cấp thanh EXP (chụp)" hoặc cờ
// Temp/machine_exp_bar_tour.flag (Unity không Play: tự vào Play, xong tự Stop). Không ghi bản lưu.
// Ảnh: Temp/PokiShots/exp_bar/*.png; log "[Huy hiệu]".
using System.Collections;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class MachineExpBarTour
    {
        const BindingFlags F = BindingFlags.NonPublic | BindingFlags.Instance;
        static double nextPoll, tourStart;
        static bool stopAfter;
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/machine_exp_bar_tour.flag"));
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/exp_bar"));

        [MenuItem("PokiClash/Thử/Máy bi/huy hiệu cấp thanh EXP (chụp)", priority = 120)]
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
                SessionState.SetBool("MachineExpBarTour", true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                Debug.LogWarning("[Huy hiệu] Tour quá 150 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("MachineExpBarTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("MachineExpBarTour", false);
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
            Debug.Log("[Huy hiệu] chụp " + name);
        }

        static readonly Vector3[] Variants =
        {
            new Vector3(22, -30, 150), new Vector3(24, -24, 140), new Vector3(30, -12, 130), new Vector3(36, 0.5f, 120), new Vector3(46, 0.5f, 150),
        };

        static IEnumerator Tour()
        {
            App.Router.Go(SceneIds.Machine);
            float t0 = Time.realtimeSinceStartup;
            MachineScene scene = null;
            while ((!(scene = Object.FindAnyObjectByType<MachineScene>()) || App.Router.Busy) && Time.realtimeSinceStartup - t0 < 25) yield return null;
            yield return new WaitForSecondsRealtime(2f);
            var bar = Object.FindAnyObjectByType<MachineExpBar>();
            if (!scene || !bar)
            {
                Debug.LogWarning("[Huy hiệu] không vào được máy bi");
            }
            else
            {
                var badge = bar.transform.Find("vong_cap") as RectTransform;
                if (badge)
                {
                    var c = new Vector3[4];
                    badge.GetWorldCorners(c);
                    Debug.Log($"[Huy hiệu] vong_cap scale {badge.localScale.x:0.###}, size {badge.rect.size}, góc thế giới {c[0]} → {c[2]}");
                }
                yield return Shot("1_dung_yen");
                // nhún lên cấp: PopCurve đỉnh 1,35 ở 0,08 giây
                bar.GetType().GetMethod("LevelPop", F)?.Invoke(bar, null);
                yield return new WaitForSecondsRealtime(0.08f);
                yield return Shot("2_nhun_len_cap");
                yield return new WaitForSecondsRealtime(1f);
                // các khung màn (9:16 là khung thấp nhất: thanh EXP sát dưới thanh trên của app), xong trả Game view về khung cũ
                var gv = typeof(Editor).Assembly.GetType("UnityEditor.GameView");
                var win = gv != null ? EditorWindow.GetWindow(gv) : null;
                var idx = gv?.GetProperty("selectedSizeIndex", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                object orig = win && idx != null ? idx.GetValue(win) : null;
                foreach (var f in GameViewSizes.Frames)
                {
                    if (!GameViewSizes.Select(f.x, f.y)) continue;
                    yield return new WaitForSecondsRealtime(0.6f);
                    yield return Shot($"3_khung_{f.x}x{f.y}");
                }
                // thử chỗ đặt khác (chỉ lúc chạy, không ghi prefab): (x tâm, y tâm so với giữa thanh, đường kính mép vòng tròn)
                if (badge)
                {
                    var keepPos = badge.anchoredPosition;
                    var keepScale = badge.localScale;
                    var dia = badge.Find("dia") as RectTransform;
                    float edge = dia ? dia.sizeDelta.x * MachineExpBarMenu.EdgeFrac : 124;
                    foreach (var f in new[] { GameViewSizes.Frames[0], GameViewSizes.Frames[1] })
                    {
                        if (!GameViewSizes.Select(f.x, f.y)) continue;
                        yield return new WaitForSecondsRealtime(0.6f);
                        foreach (var v in Variants)
                        {
                            badge.anchoredPosition = new Vector2(v.x, v.y);
                            badge.localScale = Vector3.one * (v.z / edge);
                            yield return null;
                            yield return Shot($"4_thu_{f.x}x{f.y}_x{v.x}_y{v.y}_d{v.z}");
                        }
                    }
                    badge.anchoredPosition = keepPos;
                    badge.localScale = keepScale;
                }
                if (orig != null)
                    gv.GetMethod("SizeSelectionCallback", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)?.Invoke(win, new[] { orig, null });
                else Debug.LogWarning("[Huy hiệu] không đọc được khung Game view cũ: Game view đang để khung máy tính bảng");
            }
            Debug.Log("[Huy hiệu] Xong tour: " + Dir);
            if (stopAfter)
            {
                stopAfter = false;
                tourStart = 0;
                EditorApplication.isPlaying = false;
            }
        }
    }
}
