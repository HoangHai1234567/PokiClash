// Chụp thử Sổ Phép (GD_Claude/28_SoPhep.md) khi đang Play: sổ vẽ theo gợi ý ở cấp 150 (đầu sổ, cuối sổ, ô chọn đang chọn), rồi một trận
// với nút "Lật trang" (trước và sau khi bấm). Sao lưu bản lưu trước khi thử và trả lại sau (như PlayTour.WithSaveBackup); tắt hướng dẫn.
// Ảnh ra Temp/PokiShots/so_phep/.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class SoPhepShots
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "so_phep");

        [MenuItem("PokiClash/Thử/Sổ Phép: màn sổ và nút Lật trang, chụp (đang Play)", priority = 146)]
        static void Run()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.Log("[Sổ Phép] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Tour());
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(85));
            Object.Destroy(tex);
        }

        static IEnumerator Wait(float s)
        {
            for (float t = 0; t < s; t += Time.unscaledDeltaTime) yield return null;
        }

        static IEnumerator Tour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            bool off = Tutorial.Off;
            Tutorial.Off = true;
            var s = App.Save.Data;
            var d = App.Data;
            s.level = Mathf.Max(s.level, 150);
            s.evoStones = Mathf.Max(s.evoStones, 60);
            s.sophep = new SoPhepState();
            SoPhep.AutoBuy(s, d.Cfg);
            App.Modals.CloseAll();
            while (App.Router.Busy) yield return null;
            var dlg = SoPhepDialog.Open();
            yield return Wait(0.9f);
            yield return Shot("0_so_dau");
            var scroll = dlg.GetComponentInChildren<ScrollRect>();
            if (scroll) scroll.verticalNormalizedPosition = 0;
            yield return Wait(0.4f);
            yield return Shot("1_so_cuoi");
            // chọn ô Vào Sân | Rút Lui (chương 2, ô 2) để thấy nút mặt
            var tiles = dlg.GetComponentsInChildren<SoPhepTile>(true);
            if (tiles.Length > 6) tiles[6].GetComponent<ClickCatcher>().OnClick?.Invoke();
            if (scroll) scroll.verticalNormalizedPosition = 0.75f;
            yield return Wait(0.4f);
            yield return Shot("2_o_chon");
            App.Modals.CloseAll();
            yield return Wait(0.3f);

            // trận ở ải đã qua (cấp 150 có sổ): chụp lúc chọn thẻ, bấm Lật trang, chụp lại
            var st = d.Stages.Where(x => x.tag == StageTag.None && PokiClash.Core.Progress.StageCleared(s, x)).OrderByDescending(x => x.idx).FirstOrDefault() ?? d.Stage(1);
            App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = st.id });
            float t0 = Time.realtimeSinceStartup;
            BattleView view = null;
            while (Time.realtimeSinceStartup - t0 < 20)
            {
                view = Object.FindAnyObjectByType<BattleView>();
                if (!App.Router.Busy && view && view.OfferCards.Count > 0 && !view.Dealing) break;
                yield return null;
            }
            yield return Wait(1.0f);
            yield return Shot("3_tran");
            var btn = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).FirstOrDefault(b => b.name == "nut_lat_trang" && b.isActiveAndEnabled);
            if (btn)
            {
                btn.SimulateClick();
                yield return Wait(0.3f);
                for (float w = 0; view && view.Dealing && w < 4; w += Time.unscaledDeltaTime) yield return null; // bộ bài tráo, chia lại
                yield return Wait(0.4f);
                yield return Shot("4_lat_trang");
            }
            else Debug.LogWarning("[Sổ Phép] Không thấy nút Lật trang đang hiện trong trận");
            App.Router.Go(SceneIds.Hub);
            while (App.Router.Busy) yield return null;
            yield return Wait(0.5f);
            if (backup != null)
            {
                File.WriteAllText(path, backup);
                App.Save.Load();
                App.Bars.Refresh();
            }
            Tutorial.Off = off;
            Debug.Log("[Sổ Phép] Đã chụp: " + Dir + (btn ? "" : " (thiếu nút Lật trang)"));
        }
    }
}
