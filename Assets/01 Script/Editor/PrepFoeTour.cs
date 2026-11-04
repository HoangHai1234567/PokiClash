// Vòng thử hộp Chuẩn bị trận và tai thỏ (đang Play từ Boot; người dùng dặn 2026-11-04: ô đối thủ chân dung trái, chỉ số phải, chữ to,
// cấp rõ; thanh trên tránh camera). Ảnh "cb_<tên>.png" vào Temp/PokiShots (không xoá ảnh khác). Giữ bản lưu như cũ.
// - Hộp chuẩn bị: ải 1 địch thường, 1 boss (ải cuối Đảo Thủy), 2 địch, 3 địch; khung 1080×1920.
// - Đảo Thủy lúc mới qua 2 ải: tướng trên bệ ải chưa mở là bóng sẫm (soi độ nét chân dung sau khi đổi mức nén).
// - Tai thỏ: khung 1080×2400, vùng an toàn giả (SafeArea.Simulated) chừa trên TopInset điểm; chụp sảnh, đảo, tướng, trận, hộp chuẩn bị.
//   Ảnh tai thỏ có thêm "_cam" là bản vẽ chấm camera giả lên giữa dải trên (vẽ trên ảnh chụp, không vào game).
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;
using Progress = PokiClash.Core.Progress;

namespace PokiClash.EditorTools
{
    public static class PrepFoeTour
    {
        const float TopInset = 130; // tai thỏ trên máy 1080×2400 (điểm ảnh)

        [MenuItem("PokiClash/Thử/Hộp chuẩn bị: ô đối thủ, cấp, tai thỏ (đang Play)", priority = 123)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Chuẩn bị] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var s = App.Save.Data;
            var d = App.Data;
            App.Modals.CloseAll();
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa" }) Progress.UnlockHero(s, id);
            s.team = new System.Collections.Generic.List<string> { "giot_suong", "vo_su", "nu_hoa" };
            s.level = 12;
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy) - 1;
            App.Save.Save();

            GameViewSizes.Select(1080, 1920);
            yield return Go(SceneIds.Zone, Elem.Thuy);
            var thuy = d.Stages.Where(st => st.zone == Elem.Thuy).OrderBy(st => st.idx).ToList();
            var cases = new (string tag, StageDef st)[]
            {
                ("1_thuong", thuy.First(st => st.enemies.Count == 1 && !st.enemies[0].boss)),
                ("1_boss", thuy.Last()),
                ("2_dich", thuy.FirstOrDefault(st => st.enemies.Count == 2)),
                ("3_dich", thuy.FirstOrDefault(st => st.enemies.Count == 3) ?? d.Stages.FirstOrDefault(st => st.enemies.Count == 3)),
            };
            foreach (var (tag, st) in cases)
            {
                if (st == null)
                {
                    Debug.LogWarning($"[Chuẩn bị] Không có ải kiểu {tag}");
                    continue;
                }
                StagePrep.Open(st.id);
                yield return new WaitForSecondsRealtime(0.7f);
                yield return Shot($"{tag}_ai{st.idx}", false);
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.3f);
            }

            // bóng sẫm tướng trên bệ ải chưa mở (người dùng: chân dung mờ, nhất là lúc còn bóng sẫm)
            s.zones[(int)Elem.Thuy] = 2;
            App.Save.Save();
            yield return Go(SceneIds.Hub);
            yield return Go(SceneIds.Zone, Elem.Thuy);
            yield return Shot("dao_bong_sam", false);
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy) - 1;
            App.Save.Save();

            // tai thỏ
            GameViewSizes.Select(1080, 2400);
            yield return null;
            SafeArea.Simulated = new Rect(0, 0, 1, 1 - TopInset / 2400f);
            foreach (var (scene, args) in new (string, object)[] { (SceneIds.Hub, null), (SceneIds.Zone, Elem.Thuy), (SceneIds.Heroes, null), (SceneIds.Cards, null) })
            {
                yield return Go(scene, args);
                yield return Shot("tai_tho_" + scene.ToLowerInvariant(), true);
            }
            StagePrep.Open(cases[1].st.id);
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("tai_tho_chuan_bi", true);
            App.Modals.CloseAll();
            yield return Go(SceneIds.Battle, new BattleArgs { stageId = thuy[6].id });
            yield return new WaitForSecondsRealtime(1.5f);
            yield return Shot("tai_tho_tran", true);
            SafeArea.Simulated = default;
            GameViewSizes.Select(1080, 1920);
            yield return Go(SceneIds.Hub);

            if (backup != null)
            {
                File.WriteAllText(path, backup);
                App.Save.Load();
                App.Bars.Refresh();
            }
            Debug.Log($"[Chuẩn bị] Xong vòng thử: ảnh cb_*.png trong {PlayTour.ShotDir}");
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Router.Go(scene, args);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != scene) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.6f);
        }

        // cam: vẽ thêm bản có chấm camera giả giữa dải tai thỏ
        static IEnumerator Shot(string name, bool cam)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"cb_{name}.png"), tex.EncodeToPNG());
            if (cam)
            {
                // ảnh chụp gốc ở dưới: dải tai thỏ là các dòng trên cùng (y lớn)
                int r = 26, cx = tex.width / 2, cy = tex.height - Mathf.RoundToInt(TopInset * tex.height / 2400f / 2);
                for (int y = cy - r; y <= cy + r; y++)
                for (int x = cx - r; x <= cx + r; x++)
                    if ((x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r) tex.SetPixel(x, y, Color.black);
                tex.Apply();
                File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"cb_{name}_cam.png"), tex.EncodeToPNG());
            }
            Object.Destroy(tex);
        }
    }
}
