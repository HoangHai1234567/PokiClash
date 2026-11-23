// Menu thử (đang Play): Thổ Tinh (suất giap_nham, ải 70 đảo Thổ = ải 350, final boss; dạng 1 Tiểu Thổ Tinh rig thach_de_non, dạng 2 Thổ Tinh
// rig thach_de_1; hiệu ứng HatThoTinh.cs, đối thủ co vào vỏ đá / bẹp / giật theo mảnh bay StageViewThoTinh.cs; 2026-11-18): đòn thường "Thiên
// Chuỳ" (nhảy nện), chiêu mana "Nguyệt Nhận" (gầm, mảnh lưng phóng: dạng 1 sáu mảnh vỏ, dạng 2 mười lưỡi trăng), chiêu cuối "Hằng Tinh Diệt"
// (4,70 s: thiên thạch bọc, ép co, mặt trời, tia nhiệt, nổ nấm, đáp). Chụp nhỏ liên tục vào
// Temp/PokiShots/tho_fx/tinh_<ta|dich>_d<1|2>_<danh|mana|ult>_<n>.jpg (chiêu cuối chụp 6,2 s cho thấy cả mây nấm tan và cú đáp).
// Phe ta: đội chỉ có Thổ Tinh ở ải 3 (sao 1 = dạng 1, sao 6 = dạng 2); phe địch: ải 350 (Thổ Tinh boss ra đòn từ phía trên sân vào đội mình;
// dạng 1 thì tạm hạ cấp địch về 1), tạm tắt tiến hoá trong trận. Xong trả lại bản lưu / dữ liệu ải như trước. Bản chép gọn của ThoFxTour.RunBun.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class ThoTinhFxTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "tho_fx");

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thổ/riêng Tiểu Thổ Tinh (sao 1, dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryTa1() => Start(false, 1);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thổ/riêng Thổ Tinh (sao 6, dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryTa2() => Start(false, 2);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thổ/Tiểu Thổ Tinh ở PHE ĐỊCH (ải 70, dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryDich1() => Start(true, 1);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thổ/Thổ Tinh ở PHE ĐỊCH (ải 70, boss dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryDich2() => Start(true, 2);

        static void Start(bool dich, int dang)
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(Run(dich, dang));
        }

        static IEnumerator Run(bool dich, int dang)
        {
            const string hero = "giap_nham";
            const int ai70 = 350;
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            string ten = "tinh_" + (dich ? "dich" : "ta") + "_d" + dang;
            foreach (var f in Directory.GetFiles(Dir, ten + "_*.jpg")) File.Delete(f);
            StageDef st0 = null;
            bool evo0 = false;
            int lv0 = 0;
            try
            {
                var hd = App.Data.Hero(hero);
                if (hd == null)
                {
                    Debug.LogError("[Thử] Không có tướng " + hero);
                    yield break;
                }
                var s = App.Save.Data;
                if (s.level < 7) s.level = 7;
                int sid = 3;
                if (dich)
                {
                    st0 = App.Data.Stage(ai70);
                    if (st0 == null || st0.enemies.Count == 0) yield break;
                    evo0 = st0.enemies[0].evo;
                    lv0 = st0.enemies[0].level;
                    st0.enemies[0].evo = false;
                    if (dang == 1) st0.enemies[0].level = 1;                // cấp 1 = dạng 1 (như ThoFxTour.PheDich)
                    sid = ai70;
                }
                else
                {
                    var hp = s.Hero(hero);
                    hp.owned = true;
                    hp.star = dang == 1 ? 1 : 6;
                    s.team = new List<string> { hero };
                }
                App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = sid });
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Battle) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(0.5f);
                var ctl = Object.FindAnyObjectByType<BattleController>();
                var st = Object.FindAnyObjectByType<StageView>();
                if (!ctl || !st)
                {
                    Debug.LogError("[Thử] Không thấy BattleController hoặc StageView");
                    yield break;
                }
                st.speed = 1;
                t0 = Time.realtimeSinceStartup;
                while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 20) yield return null;
                yield return new WaitForSecondsRealtime(0.6f);
                int side = dich ? 1 : 0, n = 0;
                st.Play(side, StageView.Attack);
                float start = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - start < 1.7f) yield return Shot($"{ten}_danh_{n++:00}");
                yield return new WaitForSecondsRealtime(0.4f);
                n = 0;
                st.Play(side, StageView.Cast, () => st.Beam(side));
                start = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - start < 2.8f) yield return Shot($"{ten}_mana_{n++:00}");
                yield return new WaitForSecondsRealtime(0.6f);
                n = 0;
                st.Play(side, StageView.Skill, () => st.UltFx(side));
                start = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - start < 6.2f) yield return Shot($"{ten}_ult_{n++:00}");
                yield return new WaitForSecondsRealtime(0.4f);
                Debug.Log($"[Thử] {ten}: xong");
            }
            finally
            {
                if (st0 != null && st0.enemies.Count > 0)
                {
                    st0.enemies[0].evo = evo0;
                    st0.enemies[0].level = lv0;
                }
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong Thổ Tinh: " + Dir);
        }

        // chụp nhỏ (720 rộng, jpg) bằng cách tự render camera (Editor không có tiêu điểm thì Game view không vẽ); như ThoFxTour.Shot
        static IEnumerator Shot(string name)
        {
            yield return new WaitForSecondsRealtime(0.06f);
            int w = 720, h = Mathf.RoundToInt(720f * Screen.height / Mathf.Max(1, Screen.width));
            var cams = Camera.allCameras;
            System.Array.Sort(cams, (x, y) => x.depth.CompareTo(y.depth));
            foreach (var c in cams)
                if (c.targetTexture) c.Render();
            var rt = RenderTexture.GetTemporary(w, h, 24, RenderTextureFormat.ARGB32);
            var prev = RenderTexture.active;
            foreach (var c in cams)
            {
                if (c.targetTexture) continue;
                c.targetTexture = rt;
                c.Render();
                c.targetTexture = null;
            }
            RenderTexture.active = rt;
            var tex = new Texture2D(w, h, TextureFormat.RGB24, false);
            tex.ReadPixels(new Rect(0, 0, w, h), 0, 0);
            tex.Apply();
            RenderTexture.active = prev;
            RenderTexture.ReleaseTemporary(rt);
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(85));
            Object.DestroyImmediate(tex);
        }
    }
}
