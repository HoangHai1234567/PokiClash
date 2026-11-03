// Vòng thử AFK theo ải (đang Play từ Boot): đảo Thủy đã qua 30 ải, chưa chọn ải AFK.
// 1. hộp AFK ở sảnh ghi ải tự chọn (ải 30, Vây Lam); 2. đảo Thủy có nhãn AFK dưới ải 30; 3. chạm ải 29 (đã thắng): có nút
// "AFK ải này", bấm thì thành "Đang AFK", mảnh 5 giờ tròn của ải 30 nhận luôn, nhãn dời xuống ải 29; 4. ải 31 (chưa thắng) không có
// nút; 5. hộp AFK ghi ải 29 (Ma Kết, Mi Nhi), nút Đổi ải sang đảo Thủy. Ảnh "afk_<tên>.png" vào Temp/PokiShots (không xoá ảnh khác).
// Giữ bản lưu như cũ.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;
using Progress = PokiClash.Core.Progress;

namespace PokiClash.EditorTools
{
    public static class AfkStageTour
    {
        const double H = 3600000;

        [MenuItem("PokiClash/Thử/AFK theo ải: nút ở ải đã thắng, nhãn trên đảo (đang Play)", priority = 115)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[AFK ải] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static void Check(bool ok, string what)
        {
            if (ok) Debug.Log("[AFK ải] Đúng: " + what);
            else Debug.LogError("[AFK ải] SAI: " + what);
        }

        static StageDef Thuy(int idx) => App.Data.ZoneStages(Elem.Thuy).First(x => x.idx == idx);

        static string Texts(Component root) => string.Join(" | ", root.GetComponentsInChildren<TextMeshProUGUI>(false).Select(t => t.text));

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var s = App.Save.Data;
            var d = App.Data;
            App.Modals.CloseAll();

            for (int i = 0; i < s.zones.Length; i++) s.zones[i] = 0;
            s.zones[(int)Elem.Thuy] = 30;
            s.afk = new AfkState { lastTick = PokiClash.Game.SaveService.Now() - 5.5 * H };
            App.Save.Save();

            // 1. hộp AFK ở sảnh: ải tự chọn
            yield return Go(SceneIds.Hub);
            AfkPanel.Open();
            yield return new WaitForSecondsRealtime(0.8f);
            var panel = Object.FindAnyObjectByType<AfkPanel>();
            string pt = panel ? Texts(panel) : "";
            Check(pt.Contains("Ải 30") && pt.Contains("Vây Lam"), $"hộp AFK ghi ải tự chọn 30, rơi Vây Lam: {pt}");
            yield return Shot("hop_tu_chon");
            App.Modals.CloseAll();

            // 2. đảo: nhãn AFK dưới ải 30
            yield return Go(SceneIds.Zone, Elem.Thuy);
            var tag = GameObject.Find("nhan_afk");
            Check(tag && tag.activeInHierarchy, "đảo Thủy có nhãn AFK");
            yield return Shot("dao_tu_chon");

            // 3. ải 29 đã thắng: nút AFK ải này, bấm thì Đang AFK
            var gate = Thuy(29);
            StagePrep.Open(gate.id);
            yield return new WaitForSecondsRealtime(0.8f);
            var btn = AfkButton();
            Check(btn && btn.gameObject.activeInHierarchy && btn.Label.text == "AFK ẢI NÀY", $"ải 29 có nút AFK ải này ({(btn ? btn.Label.text : "không có")})");
            yield return Shot("chuan_bi_29");
            var pos0 = tag ? ((RectTransform)tag.transform).anchoredPosition : Vector2.zero;
            if (btn) btn.SimulateClick();
            yield return new WaitForSecondsRealtime(0.6f);
            Check(Afk.Picked(s, gate), "bấm xong: đội AFK ải 29");
            Check(btn && btn.Label.text == "ĐANG AFK", $"nút thành Đang AFK ({(btn ? btn.Label.text : "")})");
            Check(s.afk.hours < 1 && s.afk.hours > 0.4, $"5 giờ tròn của ải 30 đã nhận, còn {s.afk.hours:0.00} giờ");
            tag = GameObject.Find("nhan_afk");
            Check(tag && ((RectTransform)tag.transform).anchoredPosition != pos0, "nhãn AFK dời sang ải 29");
            yield return Shot("chuan_bi_29_dang_afk");
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("dao_29");

            // 4. ải 31 chưa thắng: không có nút
            StagePrep.Open(Thuy(31).id);
            yield return new WaitForSecondsRealtime(0.8f);
            btn = AfkButton();
            Check(btn && !btn.gameObject.activeInHierarchy, "ải 31 (chưa thắng) không có nút AFK");
            yield return Shot("chuan_bi_31");
            App.Modals.CloseAll();

            // 5. hộp AFK ở sảnh: ải 29, Đổi ải sang đảo
            yield return Go(SceneIds.Hub);
            AfkPanel.Open();
            yield return new WaitForSecondsRealtime(0.8f);
            panel = Object.FindAnyObjectByType<AfkPanel>();
            pt = panel ? Texts(panel) : "";
            Check(pt.Contains("Ải 29") && pt.Contains("Ma Kết") && pt.Contains("Mi Nhi"), $"hộp AFK ghi ải 29, rơi Ma Kết, Mi Nhi: {pt}");
            var change = panel ? panel.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "afk_doi_ai") : null;
            Check(change && change.gameObject.activeInHierarchy, "có nút Đổi ải");
            yield return Shot("hop_29");
            if (change) change.SimulateClick();
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != SceneIds.Zone) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            Check(App.Router.Current == SceneIds.Zone, "Đổi ải sang màn đảo");
            yield return new WaitForSecondsRealtime(0.5f);

            if (backup != null) File.WriteAllText(path, backup);
            else if (File.Exists(path)) File.Delete(path);
            App.Save.Load();
            App.Bars.Refresh();
            yield return Go(SceneIds.Hub);
            Debug.Log($"[AFK ải] Xong vòng thử: {PlayTour.ShotDir}");
        }

        static SketchButton AfkButton()
        {
            var prep = Object.FindAnyObjectByType<StagePrepDialog>();
            return prep ? prep.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "nut_afk") : null;
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Router.Go(scene, args);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != scene) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.8f);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"afk_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }
    }
}
