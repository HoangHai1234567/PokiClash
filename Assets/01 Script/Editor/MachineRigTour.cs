// Lượt soi rig rương AtomSpine (đang Play, GD_Claude/23 giai đoạn 1): thêm 3 rương (vàng, bạc, gỗ) vào khay, vào máy bi, ghi log rig
// của từng nút khay (bật chưa, clip), chụp dày một vòng clip "nhac" (nắp hé, sáng lọt khe), rồi mở từ khay và chụp pha gồng, bật nắp.
// Ảnh vào Temp/PokiShots, số 700 trở đi. Bản lưu trả lại như trước khi thử.
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
    public static class MachineRigTour
    {
        static int shot;

        [MenuItem("PokiClash/Thử/Máy bi/rig rương nhắc mở (đang Play)", priority = 118)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Rig rương: cần đang Play");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture(); // superSize bỏ mất lớp UI phủ màn hình
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"{shot++}_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static IEnumerator Wait(float s)
        {
            for (float t = 0; t < s; t += Time.unscaledDeltaTime) yield return null;
        }

        static IEnumerator Run()
        {
            shot = 700;
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var s = App.Save.Data;
            s.balls = Mathf.Max(s.balls, 50);
            s.chests.Clear();
            foreach (var k in new[] { "chest_gold", "chest_silver", "chest_wood" })
                s.chests.Add(new PendingChest { kind = k, x = 1 });
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
            // log rig của từng nút khay
            var pf = typeof(MachineScene).GetField("p", BindingFlags.NonPublic | BindingFlags.Instance);
            var parts = pf?.GetValue(m);
            var tray = parts?.GetType().GetField("tray")?.GetValue(parts) as SketchButton[];
            if (tray != null)
                foreach (var b in tray)
                {
                    var ic = b ? b.GetComponentInChildren<ChestIcon>(true) : null;
                    Debug.Log($"[Thử] Khay {(b ? b.name : "-")}: hiện={(b && b.gameObject.activeInHierarchy)} icon={(ic ? ic.name : "không có")} rig={(ic && ic.RigOn)} clip={(ic && ic.Rig ? ic.Rig.CurrentClip : "-")}");
                }
            // một vòng "nhac" (3,2 giây): chụp mỗi 0,16 giây
            for (int i = 0; i < 21; i++)
            {
                yield return Shot($"nhac_{i:00}");
                yield return Wait(0.16f);
            }
            // mở từ khay: rương bay vào, chạm rương đầu, chụp gồng và bật nắp
            typeof(MachineScene).GetMethod("OpenFromTray", BindingFlags.NonPublic | BindingFlags.Instance)?.Invoke(m, null);
            yield return Wait(1.3f);
            yield return Shot("cho_mo");
            var open = Object.FindAnyObjectByType<MachineChestOpen>();
            var chests = open ? open.GetComponentsInChildren<UnityEngine.UI.Button>().Where(b => b.name == "than_ruong").ToList() : null;
            if (chests != null && chests.Count > 0)
            {
                chests[0].onClick.Invoke();
                for (int i = 0; i < 16; i++)
                {
                    yield return Shot($"mo_{i:00}");
                    yield return Wait(0.07f);
                }
                yield return Wait(1.0f);
                yield return Shot("mo_xong");
                var all = open.GetComponentsInChildren<SketchButton>().FirstOrDefault(b => b.name == "nut_Mở tất cả");
                if (all) all.SimulateClick();
                yield return Wait(3f);
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
            if (backup != null) File.WriteAllText(path, backup);
            App.Save.Load();
            Debug.Log($"[Thử] Rig rương: ảnh {PlayTour.ShotDir} 700–{shot - 1}");
        }
    }
}
