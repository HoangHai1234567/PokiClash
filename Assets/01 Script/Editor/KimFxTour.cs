// Menu thử (đang Play): tướng đảo Kim có hiệu ứng riêng (StageView.KimFx / KimAtk) ra trận một mình: đòn thường, chiêu mana, chiêu cuối.
// Chụp nhỏ liên tục vào Temp/PokiShots/kim_fx/<tướng>_<dạng>_<đòn>_<n>.jpg; xong trả lại bản lưu như trước. Cách chạy chép HoaFxTour.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class KimFxTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "kim_fx");

        // Thiết Tinh (2026-11-16): tinh linh tinh thể sắt, suất bo_cap; dạng 1 Thiết Tinh Nhi ở 1 sao, dạng 2 từ 3 sao (formStars)
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thiết Tinh (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThietTinh() => Try("bo_cap", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thiết Tinh Nhi (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThietTinhNhi() => Try("bo_cap", 1);

        // Thiết Vệ (2026-11-16): chiến binh sắt khiên giáo, suất doc_giac (HatGiao.cs); dạng 1 Thiết Vệ Nhi ở 1 sao, dạng 2 Thiết Vệ ở 5 sao
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thiết Vệ (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThietVe() => Try("doc_giac", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thiết Vệ Nhi (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThietVeNhi() => Try("doc_giac", 1);

        // Thiết Khoáng (2026-11-16): tinh linh quặng sắt chui đất, suất bo_ngua (rig quang_sat_<k>); dạng 1 Thiết Khoáng Nhi ở 1 sao, dạng 2 ở 5 sao
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thiết Khoáng (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThietKhoang() => Try("bo_ngua", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thiết Khoáng Nhi (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThietKhoangNhi() => Try("bo_ngua", 1);

        // Quỷ Xích (2026-11-16): quỷ béo móc xích, suất khien_bac (HatXich.cs); dạng 1 Quỷ Xích Nhi ở 1 sao, dạng 2 Quỷ Xích ở 5 sao
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Quỷ Xích (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryQuyXich() => Try("khien_bac", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Quỷ Xích Nhi (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryQuyXichNhi() => Try("khien_bac", 1);

        // Thiết Cưa (2026-11-16): tinh linh đuôi máy cưa, suất phi_thuong (rig cua_xich_1, cả hai dạng chung một rig, chưa có VFX riêng)
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thiết Cưa, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThietCua() => Try("phi_thuong", 1);

        // Vong Kỵ (2026-11-16): kỵ sĩ cổ đại bị nguyền, suất tam_kiem (rig ky_nguyen_<k>, HatHon.cs); dạng 1 Vong Kỵ Nhi ở 1 sao, dạng 2 Vong Kỵ ở 5 sao
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Vong Kỵ (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryVongKy() => Try("tam_kiem", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Vong Kỵ Nhi (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryVongKyNhi() => Try("tam_kiem", 1);

        // Sói Giáp (2026-11-16): sói chiến binh khiên búa, suất chien_than (rig soi_giap_<k>, HatSoi.cs); dạng 1 Sói Giáp Con ở 1 sao, dạng 2 Sói Giáp ở 5 sao
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Sói Giáp (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TrySoiGiap() => Try("chien_than", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Sói Giáp Con (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TrySoiGiapCon() => Try("chien_than", 1);

        // Thần Cơ (2026-11-16): robot hủy diệt cổ đại, suất thiet_phu (rig robot_co_<k>, HatRobot.cs); dạng 1 Thần Cơ Nhi ở 1 sao, dạng 2 Thần Cơ ở 5 sao
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thần Cơ (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThanCo() => Try("thiet_phu", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Thần Cơ Nhi (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryThanCoNhi() => Try("thiet_phu", 1);

        // Pháo Giáp (2026-11-17): thú giáp pháo, suất ung_thep (rig thu_phao_<k>, HatPhao.cs); dạng 1 Pháo Giáp Nhi ở 1 sao, dạng 2 Pháo Giáp ở 5 sao
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Pháo Giáp (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryPhaoGiap() => Try("ung_thep", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Pháo Giáp Nhi (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryPhaoGiapNhi() => Try("ung_thep", 1);

        // Nhật Vương (2026-11-17): vua robot quyền trượng Mặt Trời, suất kim_nghe boss ải 70 (rig vua_may_<k>, HatVua.cs); dạng 1 Nhật Hoàng Tử ở 1 sao, dạng 2 Nhật Vương ở 5 sao
        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Nhật Vương (dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryNhatVuong() => Try("kim_nghe", 5);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Kim/riêng Nhật Hoàng Tử (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryNhatHoangTu() => Try("kim_nghe", 1);

        public static void Try(string hero, int star)
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(Run(hero, star));
        }

        static IEnumerator Run(string hero, int star)
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            string ten = $"{hero}_{star}sao";
            foreach (var f in Directory.GetFiles(Dir, ten + "_*.jpg")) File.Delete(f);
            try
            {
                if (App.Data.Hero(hero) == null) yield break;
                var s = App.Save.Data;
                var hp = s.Hero(hero);
                hp.owned = true;
                hp.star = star;
                s.team = new List<string> { hero };
                if (s.level < 7) s.level = 7;
                App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = 3 });
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
                int n = 0;
                st.Play(0, StageView.Attack);
                float start = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - start < 1.5f) yield return Shot($"{ten}_danh_{n++:00}");
                yield return new WaitForSecondsRealtime(0.4f);
                n = 0;
                st.Play(0, StageView.Cast, () => st.Beam(0));
                start = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - start < 3.0f) yield return Shot($"{ten}_mana_{n++:00}");
                yield return new WaitForSecondsRealtime(0.6f);
                n = 0;
                st.Play(0, StageView.Skill, () => st.UltFx(0));
                start = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - start < 4.2f) yield return Shot($"{ten}_ult_{n++:00}");
                yield return new WaitForSecondsRealtime(0.4f);
                Debug.Log($"[Thử] {ten}: xong");
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong đảo Kim: " + Dir);
        }

        // chụp nhỏ (720 rộng, jpg) bằng cách tự render camera (Editor không có tiêu điểm thì Game view không vẽ)
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
