// Vòng thử chọn tướng khởi đầu (đang Play từ Boot, GD_Claude/15_TuongKhoiDau.md): người chơi mới mở hộp chọn (chụp, chạm từng
// tướng); rồi với mỗi tướng: chọn, hộp chuẩn bị ải 1 đảo Thủy (bóng của mình hoặc Giọt Sương thật) và ải 1 đảo cùng hệ, quà ải 3,
// ô đội 2 khoá ở cấp 1 và mở ở cấp 10. Ảnh "k_<tên>.png" vào Temp/PokiShots (không xoá ảnh khác). Giữ bản lưu như cũ.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;
using Progress = PokiClash.Core.Progress;

namespace PokiClash.EditorTools
{
    public static class StarterTour
    {
        [MenuItem("PokiClash/Thử/Chọn tướng khởi đầu: hộp chọn, ải 1 từng tướng, ô đội 2 (đang Play)", priority = 119)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Khởi đầu] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var d = App.Data;
            App.Modals.CloseAll();

            // người chơi mới: hộp chọn tướng (bỏ qua màn giới thiệu)
            App.Save.Reset();
            App.Save.Data.intro = true;
            App.Save.Save();
            yield return Go(SceneIds.Hub);
            float t0 = Time.realtimeSinceStartup;
            while (Object.FindAnyObjectByType<StarterDialog>() == null && Time.realtimeSinceStartup - t0 < 5) yield return null;
            var dlg = Object.FindAnyObjectByType<StarterDialog>();
            if (!dlg) Debug.LogError("[Khởi đầu] Không thấy hộp chọn tướng khi bản lưu chưa có tướng khởi đầu.");
            else
            {
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("chon");
                foreach (var id in d.Starters.Skip(1))
                {
                    var cell = dlg.GetComponentsInChildren<PrepRosterCell>().FirstOrDefault(c => c.name == "kho_" + id);
                    cell?.GetComponentInChildren<ClickCatcher>()?.OnClick?.Invoke();
                    yield return new WaitForSecondsRealtime(0.4f);
                    yield return Shot("chon_" + id);
                }
            }
            App.Modals.CloseAll();

            int errors = 0;
            foreach (var id in d.Starters)
            {
                App.Save.Reset();
                var s = App.Save.Data;
                s.intro = true;
                s.ChooseStarter(id);
                App.Save.Save();
                yield return Go(SceneIds.Hub);
                // ải 1 đảo Thủy và ải 1 đảo cùng hệ
                foreach (var z in new[] { Elem.Thuy, d.Hero(id).elem }.Distinct())
                {
                    StagePrep.Open(d.ZoneStages(z).First(st => st.idx == 1).id);
                    yield return new WaitForSecondsRealtime(0.8f);
                    yield return Shot($"{id}_ai1_{Keys.Of(z)}");
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                // qua 3 ải đầu: nhận quà; ô 2 còn khoá tới cấp 10, rồi mở
                var rng = new Rng(3);
                if (Progress.TeamSlots(s) != 1) { Debug.LogError($"[Khởi đầu] {id}: lúc đầu phải 1 ô đội"); errors++; }
                foreach (var st in d.ZoneStages(Elem.Thuy).Where(st => st.idx <= 3)) Progress.WinStage(s, d, st.id, rng);
                string gift = d.ZoneStages(Elem.Thuy).First(st => st.idx == 3).drops.First(x => x.gift).HeroFor(s);
                if (Progress.TeamSlots(s) != 1 || !s.Hero(gift).owned) { Debug.LogError($"[Khởi đầu] {id}: qua ải 3 phải có {gift}, ô 2 còn khoá"); errors++; }
                var ai4 = d.ZoneStages(Elem.Thuy).First(st => st.idx == 4).id;
                foreach (var lv in new[] { 1, Progress.SlotLevels[1] })
                {
                    s.level = lv;
                    App.Save.Save();
                    StagePrep.Open(ai4);
                    yield return new WaitForSecondsRealtime(0.8f);
                    yield return Shot($"{id}_ai4_cap{lv}");
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
            }

            // trả bản lưu như trước; trước đó chưa có file thì xoá file vòng thử vừa ghi
            if (backup != null) File.WriteAllText(path, backup);
            else if (File.Exists(path)) File.Delete(path);
            App.Save.Load();
            App.Bars.Refresh();
            yield return Go(SceneIds.Hub);
            Debug.Log($"[Khởi đầu] Xong vòng thử ({errors} lỗi): {PlayTour.ShotDir}");
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Router.Go(scene, args);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != scene) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.5f);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"k_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }
    }
}
