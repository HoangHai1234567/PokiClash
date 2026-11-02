// Lượt thử soi hiệu ứng máy bi (đang Play): thả liền 20 bi rồi dừng máy giữa chừng để chụp vệt bi; sau đó bật từng bộ hiệu ứng
// (đinh, nấm, ô, cốc, lúc thả, rương cấp 2 và 3, rương vàng) và tự tua giờ hạt tới từng mốc để chụp, vì hạt chỉ sống 0,1–0,5 giây.
// Ảnh vào Temp/PokiShots, số 200 trở đi. Bản lưu trả lại như trước khi thử.
using System.Collections;
using System.IO;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class MachineFxTour
    {
        static int shot;

        [MenuItem("PokiClash/Thử/Máy bi: soi hiệu ứng (đang Play)", priority = 113)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"{shot++}_{name}_{tex.width}x{tex.height}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static bool Click(string label)
        {
            foreach (var b in Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None))
                if (b.Label && b.Label.text == label.ToUpperInvariant() && b.isActiveAndEnabled)
                {
                    b.SimulateClick();
                    return true;
                }
            Debug.LogWarning("[Thử] Không thấy nút " + label);
            return false;
        }

        // tua giờ hạt (máy đang dừng) thêm step giây rồi chụp
        static IEnumerator Advance(MachineBoard v, float step, string name)
        {
            v.Sync(step, step, Board.BW / 2, 0);
            yield return Shot(name);
        }

        static IEnumerator Run()
        {
            shot = 200;
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
            yield return new WaitForSecondsRealtime(0.8f);
            var v = Object.FindAnyObjectByType<MachineBoard>();
            var b = v.Board;

            // 1. vệt bi và đinh sáng lúc bi đang lăn
            Click("×1");
            Click("Thả liền 20");
            yield return new WaitForSecondsRealtime(1.5f);
            m.enabled = false;
            yield return Shot("fx_bi_lan");
            Debug.Log($"[Thử] Hạt đang sống: {v.Fx.Live}, bi đang lăn: {b.balls.Count}");

            // 2. đinh, nấm, ô, cốc, lúc thả cùng lúc, chụp ở 0,03 / 0,08 / 0,15 / 0,25 giây
            int bumper = b.pegs.FindIndex(q => q.kind == PegKind.Bumper);
            int peg = b.pegs.FindIndex(q => q.kind == PegKind.Peg);
            v.Flash(bumper);
            for (int i = 0; i < 3; i++) v.Flash(peg + i * 3);
            v.SlotFx(1);
            v.SlotFx(4);
            v.SlotFx(8);
            var cup = b.cups.Find(c => c.r > 0);
            v.CupFx(cup.x, cup.y);
            v.Launch(Board.BW / 2);
            float age = 0;
            foreach (var at in new[] { 0.03f, 0.08f, 0.15f, 0.25f })
            {
                yield return Advance(v, at - age, $"fx_cham_{Mathf.RoundToInt(at * 100):00}");
                age = at;
            }
            yield return Advance(v, 0.6f, "fx_cham_het");

            // 3. rương rơi vào: cấp 2 (gỗ ô trái) và cấp 3 (vàng ô khuất)
            var left = b.slots[0];
            var mid = b.slots[5];
            v.Burst((left.x0 + left.x1) / 2, Board.Floor - 10, MachineBoard.ChestColor(SlotKind.ChestWood));
            v.ChestFx((left.x0 + left.x1) / 2, Board.Floor - 10, 2);
            v.Float((left.x0 + left.x1) / 2, Board.Floor - 30, "Rương Gỗ!", MachineBoard.ChestColor(SlotKind.ChestWood), 30);
            v.ChestFx((mid.x0 + mid.x1) / 2, Board.Floor - 10, 3);
            age = 0;
            foreach (var at in new[] { 0.05f, 0.12f, 0.25f, 0.45f })
            {
                yield return Advance(v, at - age, $"fx_ruong_{Mathf.RoundToInt(at * 100):00}");
                age = at;
            }
            yield return Advance(v, 0.8f, "fx_ruong_het");

            // 4. rương vàng ở két
            v.Burst(Board.VaultX, 505, MachineBoard.ChestColor(SlotKind.ChestGold), 1.8f);
            v.JackpotFx(Board.VaultX, 505);
            v.Glow(5, 2);
            age = 0;
            foreach (var at in new[] { 0.03f, 0.1f, 0.2f, 0.35f, 0.5f })
            {
                yield return Advance(v, at - age, $"fx_jackpot_{Mathf.RoundToInt(at * 100):00}");
                age = at;
            }

            // 5. chạy tiếp tới hết đợt, đóng các hộp mở rương
            m.enabled = true;
            t0 = Time.realtimeSinceStartup;
            while ((!m.Idle || App.Modals.Count > 0) && Time.realtimeSinceStartup - t0 < 60)
            {
                if (App.Modals.Count > 0)
                {
                    yield return new WaitForSecondsRealtime(0.8f);
                    App.Modals.Back();
                }
                yield return null;
            }
            yield return Shot("fx_sau");
            if (backup != null)
            {
                File.WriteAllText(path, backup);
                App.Save.Load();
                App.Bars.Refresh();
            }
            Debug.Log($"[Thử] Xong soi hiệu ứng máy bi: ảnh trong {PlayTour.ShotDir}");
        }
    }
}
