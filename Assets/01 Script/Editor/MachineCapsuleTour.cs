// Lượt thử bảng số và màn mở rương nhóm của máy bi (đang Play, 2026-11-10): thả liền một đợt (kẹo bay từ ô lên bảng số, số đếm,
// cuối đợt thu số lên thanh), rồi thêm 5 rương vào khay và mở (bay vào, lơ lửng, mở một rương theo từng pha, mở tất cả, tổng kết).
// Ảnh vào Temp/PokiShots, số 400 trở đi. Bản lưu trả lại như trước khi thử.
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
    public static class MachineCapsuleTour
    {
        static int shot;

        [MenuItem("PokiClash/Thử/Máy bi: bảng số và mở rương nhóm (đang Play)", priority = 115)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(Run());
        }

        // bi rơi vào ô EXP (gọi thẳng OnLand cho một ô EXP 10): chụp liền 16 khung để soi kẹo bóp giãn, cụm "kẹo + số", kẹo
        // phụt, vệt bay về bảng số. Ảnh 450 trở đi.
        [MenuItem("PokiClash/Thử/Máy bi: soi kẹo ô EXP (đang Play)", priority = 116)]
        static void TrySlot()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunSlot());
        }

        static IEnumerator RunSlot()
        {
            shot = 450;
            App.Router.Go(SceneIds.Machine);
            float t0 = Time.realtimeSinceStartup;
            MachineScene m = null;
            while ((!(m = Object.FindAnyObjectByType<MachineScene>()) || App.Router.Busy) && Time.realtimeSinceStartup - t0 < 20) yield return null;
            yield return Wait(1f);
            var v = Object.FindAnyObjectByType<MachineBoard>();
            int slot = v.Board.slots.FindIndex(q => Pachinko.Exp(q.reward) >= 10);
            var sl = v.Board.slots[slot];
            var land = typeof(MachineScene).GetMethod("OnLand", BindingFlags.NonPublic | BindingFlags.Instance);
            land.Invoke(m, new object[] { sl.reward, slot, (sl.x0 + sl.x1) / 2, sl.y0 + 10, 1 });
            for (int i = 0; i < 16; i++)
            {
                yield return new WaitForEndOfFrame();
                var tex = ScreenCapture.CaptureScreenshotAsTexture();
                Directory.CreateDirectory(PlayTour.ShotDir);
                File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"{shot++}_o_exp_{i}.png"), tex.EncodeToPNG());
                Object.Destroy(tex);
                yield return null;
            }
            Debug.Log($"[Thử] Kẹo ô EXP: ảnh 450–{shot - 1}");
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

        static IEnumerator Run()
        {
            shot = 400;
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var s = App.Save.Data;
            s.level = 5;
            s.balls = 400;
            s.chests.Clear();
            App.Save.Save();
            App.Router.Go(SceneIds.Machine);
            float t0 = Time.realtimeSinceStartup;
            MachineScene m = null;
            while ((!(m = Object.FindAnyObjectByType<MachineScene>()) || App.Router.Busy) && Time.realtimeSinceStartup - t0 < 20) yield return null;
            yield return Wait(1f);
            yield return Shot("bs_ranh");

            // thả liền: kẹo bay lên bảng, số đếm
            var auto = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None)
                .FirstOrDefault(b => b.Label && b.Label.text.Replace('\n', ' ').StartsWith("THẢ LIỀN"));
            if (auto) auto.SimulateClick();
            else Debug.LogWarning("[Thử] Không thấy nút Thả liền");
            for (int i = 0; i < 10; i++)
            {
                yield return Wait(0.45f);
                yield return Shot($"bs_tha_{i}");
            }
            // chờ hết bi rồi chụp lúc thu số lên thanh
            t0 = Time.realtimeSinceStartup;
            var board = Object.FindAnyObjectByType<MachineScoreBoard>();
            while (m && m.Session > 0 && Time.realtimeSinceStartup - t0 < 30) yield return null;
            for (int i = 0; i < 6; i++)
            {
                yield return Shot($"bs_thu_{i}");
                yield return Wait(0.2f);
            }
            // rương rơi trong đợt mở ngay cuối đợt: bấm qua (mở tất cả / nhận) cho tới khi màn mở rương đóng
            t0 = Time.realtimeSinceStartup;
            while (Time.realtimeSinceStartup - t0 < 20)
            {
                yield return Wait(0.6f);
                var open = Object.FindAnyObjectByType<MachineChestOpen>();
                if (!open)
                {
                    if (Time.realtimeSinceStartup - t0 > 4) break;
                    continue;
                }
                // chỉ nút trong màn mở rương (máy cũng có nút tên nut_tha_bi, nut_tha_lien)
                var b = open.GetComponentsInChildren<SketchButton>().FirstOrDefault(q => q.name.StartsWith("nut_"));
                if (b) b.SimulateClick();
                else open.GetComponentsInChildren<UnityEngine.UI.Button>().FirstOrDefault(q => q.name == "than_ruong")?.onClick.Invoke();
            }
            yield return Wait(0.5f);
            while (App.Modals.Count > 0)
            {
                App.Modals.Back();
                yield return Wait(0.4f);
            }
            yield return Wait(1f);
            yield return Shot("bs_sau_thu");

            // 5 rương: 2 vàng, 2 bạc, 1 gỗ; mở từ khay
            foreach (var k in new[] { "chest_gold", "chest_silver", "chest_wood", "chest_silver", "chest_gold" })
                s.chests.Add(new PendingChest { kind = k, x = 1 });
            App.Save.Save();
            typeof(MachineScene).GetMethod("OpenFromTray", BindingFlags.NonPublic | BindingFlags.Instance)?.Invoke(m, null);
            yield return Wait(0.35f);
            yield return Shot("mr_bay_vao");
            yield return Wait(0.9f);
            yield return Shot("mr_lo_lung");
            var chests = Object.FindObjectsByType<UnityEngine.UI.Button>(FindObjectsSortMode.None).Where(b => b.name == "than_ruong").ToList();
            if (chests.Count > 0)
            {
                chests[0].onClick.Invoke();
                foreach (var (dt, nm) in new[] { (0.15f, "lac"), (0.17f, "bat"), (0.08f, "chop"), (0.15f, "nap_than"), (0.3f, "thuong_nay"), (0.6f, "da_mo") })
                {
                    yield return Wait(dt);
                    yield return Shot("mr_" + nm);
                }
            }
            var all = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).FirstOrDefault(b => b.name == "nut_Mở tất cả");
            if (all) all.SimulateClick();
            else Debug.LogWarning("[Thử] Không thấy nút Mở tất cả");
            for (int i = 0; i < 4; i++)
            {
                yield return Wait(0.35f);
                yield return Shot($"mr_mo_het_{i}");
            }
            yield return Wait(1.2f);
            yield return Shot("mr_tong_ket_0");
            yield return Wait(1.2f);
            yield return Shot("mr_tong_ket_1");
            var ok = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).FirstOrDefault(b => b.name.StartsWith("nut_Nhận") || b.name.StartsWith("nut_Mở tiếp"));
            if (ok) ok.SimulateClick();
            yield return Wait(1.5f);
            while (App.Modals.Count > 0)
            {
                App.Modals.Back();
                yield return Wait(0.4f);
            }
            yield return Shot("mr_xong");

            if (backup != null) File.WriteAllText(path, backup);
            App.Save.Load();
            Debug.Log($"[Thử] Bảng số, mở rương nhóm: ảnh {PlayTour.ShotDir} 400–{shot - 1}");
        }
    }
}
