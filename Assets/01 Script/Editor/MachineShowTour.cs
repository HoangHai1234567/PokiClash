// Lượt soi giai đoạn 2–3 của máy bi (đang Play, GD_Claude/23): (1) máy rảnh: đèn làn chạy lên, đèn vòm sóng mời thả; (2) thả một bi
// thường: đèn chạy qua ô rồi dừng ở ô thật; (3) ép một bi vào ô rương vàng (đổi tạm Board.odds, chỉ trên bàn đang chạy, rồi trả lại):
// chụp phóng, loé miệng ống, báo trước (đèn dồn, phóng to), rơi ô, chữ JACKPOT, vòi xu. Ảnh vào Temp/PokiShots số 800 trở đi.
// Bản lưu trả lại như trước khi thử.
using System.Collections;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class MachineShowTour
    {
        static int shot;

        [MenuItem("PokiClash/Thử/Máy bi/đèn, phóng, jackpot (đang Play)", priority = 119)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Đèn, jackpot: cần đang Play");
                return;
            }
            App.I.StartCoroutine(Run());
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
            shot = 800;
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
            yield return Wait(1.0f);
            if (!m)
            {
                Debug.LogWarning("[Thử] Không vào được màn máy bi");
                yield break;
            }
            // 1. rảnh: đèn làn, đèn vòm
            for (int i = 0; i < 4; i++)
            {
                yield return Shot($"ranh_{i}");
                yield return Wait(0.15f);
            }
            var board = typeof(MachineScene).GetField("board", BindingFlags.NonPublic | BindingFlags.Instance)?.GetValue(m) as Board;
            var drop = typeof(MachineScene).GetMethod("DropOne", BindingFlags.NonPublic | BindingFlags.Instance);
            if (board == null || drop == null)
            {
                Debug.LogWarning("[Thử] Không lấy được bàn hoặc DropOne");
                yield break;
            }
            // 2. một bi thường (trước jackpot, cho khỏi bị màn mở rương phủ): ép vào ô EXP đầu tiên để chắc có đèn chạy qua ô (bi rơi
            // vào cốc thì không chạy), rồi trả bảng tỉ lệ
            var keep0 = board.odds;
            int exp = board.slots.FindIndex(sl => sl.reward == SlotKind.Exp10 || sl.reward == SlotKind.Exp5);
            if (keep0 != null && exp >= 0)
            {
                var f0 = new double[keep0.Length];
                f0[exp] = 1;
                board.odds = f0;
            }
            drop.Invoke(m, null);
            board.odds = keep0;
            Debug.Log($"[Thử] Bi thường: mục tiêu {board.balls.LastOrDefault()?.target} (ô EXP {exp})");
            for (int i = 0; i < 40; i++)
            {
                yield return Shot($"thuong_{i:00}");
                yield return Wait(0.09f);
            }
            t0 = Time.realtimeSinceStartup;
            while (!m.Idle && Time.realtimeSinceStartup - t0 < 10) yield return null;
            yield return Wait(1.5f);
            while (App.Modals.Count > 0)
            {
                App.Modals.Back();
                yield return Wait(0.3f);
            }
            // 3. ép bi vào ô rương vàng
            int gold = board.slots.FindIndex(sl => sl.reward == SlotKind.ChestGold);
            var keep = board.odds;
            if (gold >= 0 && keep != null)
            {
                var forced = new double[keep.Length];
                forced[gold] = 1;
                board.odds = forced;
                drop.Invoke(m, null);
                board.odds = keep;
                Debug.Log($"[Thử] Ép bi vào ô rương vàng (ô {gold}), mục tiêu bi: {board.balls.LastOrDefault()?.target}");
                for (int i = 0; i < 46; i++)
                {
                    yield return Shot($"jackpot_{i:00}");
                    yield return Wait(0.09f);
                }
            }
            else Debug.LogWarning("[Thử] Không thấy ô rương vàng / bảng tỉ lệ");
            // chờ đợt xong (mở rương vàng): đóng các hộp
            t0 = Time.realtimeSinceStartup;
            while (!m.Idle && Time.realtimeSinceStartup - t0 < 25)
            {
                var open = Object.FindAnyObjectByType<MachineChestOpen>();
                if (open)
                {
                    var all = open.GetComponentsInChildren<PokiClash.UI.SketchButton>().FirstOrDefault(b => b.name == "nut_Mở tất cả");
                    if (all) all.SimulateClick();
                    yield return Wait(2.5f);
                    var ok = open ? open.GetComponentsInChildren<PokiClash.UI.SketchButton>().FirstOrDefault(b => b.name.StartsWith("nut_Nhận") || b.name.StartsWith("nut_Mở tiếp")) : null;
                    if (ok) ok.SimulateClick();
                }
                while (App.Modals.Count > 0)
                {
                    App.Modals.Back();
                    yield return Wait(0.3f);
                }
                yield return Wait(0.3f);
            }
            yield return Wait(0.8f);
            while (App.Modals.Count > 0)
            {
                App.Modals.Back();
                yield return Wait(0.3f);
            }
            if (backup != null) File.WriteAllText(path, backup);
            App.Save.Load();
            Debug.Log($"[Thử] Đèn, jackpot: ảnh {PlayTour.ShotDir} 800–{shot - 1}");
        }
    }
}
