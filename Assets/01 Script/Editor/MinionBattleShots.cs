// Thử quái lính .atomik (2026-11-20, quái lính 5 đảo vẽ lại bằng AtomSpine): vào trận ải đầu tiên có lính đứng đầu của từng đảo (lính bậc 1), cho máy tự
// đánh ở nhịp thường, chụp màn mỗi 0,3 giây trong 18 giây (đội Tí Tách cấp 3) vào Temp/PokiShots/linh_<đảo>_<i>.png. Đảo đọc ở Temp/PokiShots/linh_dao.txt
// (mỗi dòng một mã: thuy, moc, hoa, kim, tho); không có file thì cả 5. Bản lưu được trả lại như trước khi thử.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class MinionBattleShots
    {
        static string Dir => PlayTour.ShotDir;

        [MenuItem("PokiClash/Thử/Quái lính: trận có lính mỗi đảo, chụp khung (đang Play)", priority = 129)]
        static void Run()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(Tour());
        }

        static IEnumerator Tour()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            var all = new[] { Elem.Thuy, Elem.Moc, Elem.Hoa, Elem.Kim, Elem.Tho };
            var list = new List<Elem>(all);
            var cfg = Path.Combine(Dir, "linh_dao.txt");
            if (File.Exists(cfg))
            {
                var want = File.ReadAllLines(cfg).Select(l => l.Trim()).Where(l => l.Length > 0).ToHashSet();
                list = all.Where(z => want.Contains(Keys.Of(z))).ToList();
            }
            var s = App.Save.Data;
            s.intro = true;
            s.level = 3; // đội yếu (Tí Tách cấp thấp) để lính sống đủ lâu mà đánh, phun, ra chiêu
            s.Hero("ti_tach").owned = true;
            s.team = new List<string> { "ti_tach" };
            App.Save.Save();
            foreach (var zone in list)
            {
                var st = App.Data.ZoneStages(zone).First(x => x.enemies.Count > 0 && App.Data.Hero(x.enemies[0].hero).minion); // ải đầu có lính đứng đầu
                string tag = Keys.Of(zone);
                App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = st.id });
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Battle) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                var ctl = Object.FindAnyObjectByType<BattleController>();
                if (!ctl)
                {
                    Debug.LogError($"[Thử] linh {tag}: không thấy BattleController");
                    continue;
                }
                t0 = Time.realtimeSinceStartup;
                while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 30) yield return null;
                ctl.SetAuto(true);
                for (int i = 0; i < 60; i++)
                {
                    yield return new WaitForSecondsRealtime(0.3f);
                    yield return new WaitForEndOfFrame();
                    var tex = ScreenCapture.CaptureScreenshotAsTexture();
                    File.WriteAllBytes(Path.Combine(Dir, $"linh_{tag}_{i:00}.png"), tex.EncodeToPNG());
                    Object.Destroy(tex);
                    if (ctl.Battle.phase == Phase.Over && App.Modals.Count > 0) break;
                }
                Debug.Log($"[Thử] linh {tag}: ải {st.id} ({string.Join(", ", st.enemies.Select(e => e.hero))}), {ctl.Battle.round} hiệp");
                App.Modals.CloseAll();
                App.Router.Go(SceneIds.Hub);
                t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Hub) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            }
            if (backup != null)
            {
                File.WriteAllText(path, backup);
                App.Save.Load();
                App.Bars.Refresh();
            }
            Debug.Log($"[Thử] Xong quái lính: ảnh linh_*.png trong {Dir}");
        }
    }
}
