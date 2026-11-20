// Lượt soi máy bi (đang Play, 2026-11-19): (1) thả một bi, chụp dày lúc bi ra miệng ống, lăn ép vòm, đâm gờ đỉnh rồi văng xuống;
// (2) thêm 3 rương (vàng, bạc, gỗ) vào khay rồi mở: chụp dày từng pha của rương đầu (gồng, bật nắp, giấy màu, thưởng vọt ra),
// rồi mở tất cả và bảng tổng kết. Ảnh vào Temp/PokiShots, số 500 trở đi. Bản lưu trả lại như trước khi thử.
using System.Collections;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class MachineLaunchChestTour
    {
        static int shot;

        [MenuItem("PokiClash/Thử/Máy bi: soi phóng bi và mở rương (đang Play)", priority = 117)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Soi phóng bi, mở rương: cần đang Play");
                return;
            }
            App.I.StartCoroutine(Run(true));
        }

        // chỉ mở 3 rương (không thả bi), chụp dày lúc chờ chạm 3,6 giây (rương nhắc mở: lắc, hé nắp có sáng; lấp lánh) — 2026-11-21
        [MenuItem("PokiClash/Thử/Máy bi: soi mở 3 rương (đang Play)", priority = 118)]
        static void TryChests()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Soi mở 3 rương: cần đang Play");
                return;
            }
            App.I.StartCoroutine(Run(false));
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"{shot++}_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static IEnumerator Wait(float s)
        {
            for (float t = 0; t < s; t += Time.unscaledDeltaTime) yield return null;
        }

        static IEnumerator Run(bool drop)
        {
            shot = 500;
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var s = App.Save.Data;
            s.balls = Mathf.Max(s.balls, 50);
            s.chests.Clear();
            App.Save.Save();
            App.Router.Go(SceneIds.Machine);
            float t0 = Time.realtimeSinceStartup;
            MachineScene m = null;
            while ((!(m = Object.FindAnyObjectByType<MachineScene>()) || App.Router.Busy) && Time.realtimeSinceStartup - t0 < 20) yield return null;
            yield return Wait(1.2f);
            if (!m)
            {
                Debug.LogWarning("[Thử] Không vào được màn máy bi");
                yield break;
            }

            if (drop)
            {
                // 1. thả một bi: chụp mỗi 0,06 giây trong 1,6 giây (làn, miệng ống, dọc vòm, gờ đỉnh)
                var dropOne = typeof(MachineScene).GetMethod("DropOne", BindingFlags.NonPublic | BindingFlags.Instance);
                dropOne?.Invoke(m, null);
                for (int i = 0; i < 27; i++)
                {
                    yield return Shot($"phong_{i:00}");
                    yield return Wait(0.06f);
                }
                // chờ bi rơi xong
                t0 = Time.realtimeSinceStartup;
                var view = Object.FindAnyObjectByType<MachineBoard>();
                while (view && view.Board.balls.Count > 0 && Time.realtimeSinceStartup - t0 < 15) yield return null;
                yield return Wait(2.5f); // kẹo bay hết, bảng thu
                while (App.Modals.Count > 0)
                {
                    App.Modals.Back();
                    yield return Wait(0.4f);
                }
            }

            // 2. mở 3 rương
            foreach (var k in new[] { "chest_gold", "chest_silver", "chest_wood" })
                s.chests.Add(new PendingChest { kind = k, x = 1 });
            App.Save.Save();
            typeof(MachineScene).GetMethod("OpenFromTray", BindingFlags.NonPublic | BindingFlags.Instance)?.Invoke(m, null);
            yield return Wait(0.3f);
            yield return Shot("ruong_bay_vao");
            yield return Wait(0.9f);
            yield return Shot("ruong_cho");
            if (!drop)
                for (int i = 0; i < 24; i++)
                {
                    yield return Wait(0.15f);
                    yield return Shot($"cho_{i:00}");
                }
            var open = Object.FindAnyObjectByType<MachineChestOpen>();
            var chests = open ? open.GetComponentsInChildren<UnityEngine.UI.Button>().Where(b => b.name == "than_ruong").ToList() : null;
            if (chests != null && chests.Count > 0)
            {
                // rương đầu theo bố cục (vàng): gồng 0,6 giây, bật, giấy màu, thưởng vọt ra
                chests[0].onClick.Invoke();
                for (int i = 0; i < 24; i++)
                {
                    yield return Shot($"mo_{i:00}");
                    yield return Wait(0.07f);
                }
                yield return Wait(0.4f);
                var all = open.GetComponentsInChildren<SketchButton>().FirstOrDefault(b => b.name == "nut_Mở tất cả");
                if (all) all.SimulateClick();
                for (int i = 0; i < 10; i++)
                {
                    yield return Shot($"mo_het_{i:00}");
                    yield return Wait(0.12f);
                }
                yield return Wait(1.6f);
                yield return Shot("tong_ket");
                var ok = open ? open.GetComponentsInChildren<SketchButton>().FirstOrDefault(b => b.name.StartsWith("nut_Nhận") || b.name.StartsWith("nut_Mở tiếp")) : null;
                if (ok) ok.SimulateClick();
                yield return Wait(1.2f);
            }
            else Debug.LogWarning("[Thử] Không thấy màn mở rương nhóm");
            while (App.Modals.Count > 0)
            {
                App.Modals.Back();
                yield return Wait(0.4f);
            }
            yield return Shot("xong");
            if (backup != null) File.WriteAllText(path, backup);
            App.Save.Load();
            Debug.Log($"[Thử] Soi phóng bi, mở rương: ảnh {PlayTour.ShotDir} 500–{shot - 1}");
        }
    }
}
