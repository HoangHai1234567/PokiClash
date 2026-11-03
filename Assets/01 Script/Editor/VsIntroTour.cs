// Vòng thử màn VS truyện tranh và dải tuyệt kỹ (đang Play từ Boot): vào ba trận (ải 1 một địch, ải ba địch, ải boss đảo Thủy) với
// đội 3 tướng, chụp màn VS lúc khung trượt vào, lúc dấu VS đóng, lúc giữ; trên trận cuối gọi dải tuyệt kỹ cho phe mình rồi phe địch,
// chụp giữa dải. Ảnh "vs_<tên>.png" vào Temp/PokiShots (không xoá ảnh khác). Giữ bản lưu như cũ.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;
using Progress = PokiClash.Core.Progress;

namespace PokiClash.EditorTools
{
    public static class VsIntroTour
    {
        [MenuItem("PokiClash/Thử/Màn VS truyện tranh, dải tuyệt kỹ (đang Play)", priority = 115)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[VS] Mở Boot.unity và bấm Play trước.");
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

            // đội 3 tướng: mở đủ ô đội (cấp người chơi tới mốc ô cuối, Progress.SlotLevels)
            foreach (var h in new[] { "giot_suong", "vo_su", "tieu_y" }) Progress.UnlockHero(s, h);
            s.team = new List<string> { "giot_suong", "vo_su", "tieu_y" };
            s.level = Mathf.Max(s.level, Progress.SlotLevels[Progress.TeamSlotMax - 1]);
            App.Save.Save();

            var three = d.Stages.FirstOrDefault(st => st.enemies.Count >= 3);
            var boss = d.Stages.FirstOrDefault(st => st.zone == Elem.Thuy && st.enemies.Any(e => e.boss));
            var stages = new List<(StageDef st, string tag)> { (d.Stage(1), "ai1") };
            if (three != null) stages.Add((three, "ba_dich"));
            if (boss != null) stages.Add((boss, "boss"));
            foreach (var (st, tag) in stages)
            {
                yield return Go(SceneIds.Hub);
                App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = st.id });
                BattleIntro intro = null;
                float t0 = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - t0 < 20)
                {
                    var v = Object.FindAnyObjectByType<BattleView>();
                    intro = v ? v.Intro : null;
                    if (intro && intro.gameObject.activeInHierarchy) break;
                    yield return null;
                }
                if (!intro || !intro.gameObject.activeInHierarchy)
                {
                    Debug.LogError($"[VS] Ải {st.id}: không thấy màn VS bật lên.");
                    continue;
                }
                float start = Time.realtimeSinceStartup;
                foreach (var (at, n) in new[] { (0.16f, "truot"), (0.52f, "dau_vs"), (1.3f, "giu") })
                {
                    while (Time.realtimeSinceStartup - start < at) yield return null;
                    yield return Shot($"{tag}_{n}");
                }
                while (intro.gameObject.activeInHierarchy && Time.realtimeSinceStartup - start < 6) yield return null;
                yield return new WaitForSecondsRealtime(0.3f);
                yield return Shot($"{tag}_vao_tran");
                Debug.Log($"[VS] Ải {st.id} ({st.enemies.Count} địch): màn VS {Time.realtimeSinceStartup - start:0.00}s.");
            }

            // dải tuyệt kỹ trên trận đang mở: phe mình rồi phe địch
            var view = Object.FindAnyObjectByType<BattleView>();
            var ctl = Object.FindAnyObjectByType<BattleController>();
            if (view && view.UltCut && ctl)
            {
                for (int side = 0; side < 2; side++)
                {
                    var f = ctl.Battle.ActiveOf(side);
                    var card = d.Card(f.hero.ult);
                    var run = view.UltCut.Play(f.hero, f.Name, Teams.LookStar(d.Cfg, f), card != null ? card.name : "Tuyệt Kỹ",
                        side == 0, (RectTransform)view.Stage.transform, 1);
                    App.I.StartCoroutine(run);
                    yield return new WaitForSecondsRealtime(0.1f);
                    yield return Shot($"tuyet_ky_{side}_vao");
                    yield return new WaitForSecondsRealtime(0.35f);
                    yield return Shot($"tuyet_ky_{side}");
                    yield return new WaitForSecondsRealtime(1.2f);
                }
            }
            else Debug.LogError("[VS] Không thấy dải tuyệt kỹ (BattleView.p.ultCut).");

            // trả bản lưu như trước; trước đó chưa có file thì xoá file vòng thử vừa ghi (người chơi mới)
            if (backup != null) File.WriteAllText(path, backup);
            else if (File.Exists(path)) File.Delete(path);
            App.Save.Load();
            App.Bars.Refresh();
            yield return Go(SceneIds.Hub);
            Debug.Log($"[VS] Xong vòng thử màn VS: {PlayTour.ShotDir}");
        }

        static IEnumerator Go(string scene)
        {
            App.Router.Go(scene);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != scene) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.5f);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"vs_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }
    }
}
