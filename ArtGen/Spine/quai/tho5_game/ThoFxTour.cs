// Menu thử (đang Play): năm tướng đầu đảo Thổ (2026-11-17, rig Sword x Staff, hiệu ứng HatTho.cs; StageView.ThoFx / ThoAtk) ra trận một
// mình: đòn thường, chiêu mana, chiêu cuối. Chụp nhỏ liên tục vào Temp/PokiShots/tho_fx/<tướng>_<sao>sao_<đòn>_<n>.jpg; xong trả lại bản lưu
// như trước. Chép KimFxTour. Ba tướng đầu + Sa Long có hai rig (dạng 1 ở 1 sao, dạng 2 từ 6 sao, formStars): menu dạng 2 chụp ở sao 6;
// menu tiến hoá mở hộp chi tiết ở sao cuối dạng 1, bấm nút hack tiến hoá, chụp clip `evolve` (chép GiotSuongCombatTour.Evolve); menu phe
// địch cho tướng Thổ ra đòn từ phía trên sân (soi tràn mép).
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class ThoFxTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "tho_fx");
        static readonly string[] Nam = { "thach_nhan", "lung_vuong", "cao_da", "ho_khoan", "phu_van" };
        static readonly string[] HaiRig = { "thach_nhan", "lung_vuong", "cao_da", "ho_khoan" };

        [MenuItem("PokiClash/Thử/Đảo Thổ: DẠNG 2 của 4 tướng (sao 6) lần lượt, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryDang2()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunAll(HaiRig, 6));
        }

        [MenuItem("PokiClash/Thử/Đảo Thổ: TIẾN HOÁ 4 tướng (hộp chi tiết, nút hack, clip evolve) (đang Play)", priority = 125)]
        static void TryTienHoa()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(EvolveAll(HaiRig));
        }

        // PHE ĐỊCH (trên sân): ải mở đầu của tướng (đảo Thổ), tạm đặt cấp địch cho đúng dạng (cấp 35 = sao 6 = dạng 2; cấp 1 = dạng 1), bỏ tiến
        // hoá trong trận, rồi cho tướng địch (side 1) ra đòn thường, chiêu mana, chiêu cuối vào đội mình: soi hiệu ứng có tràn mép trên sân không.
        // Chỉ sửa dữ liệu trong bộ nhớ lúc Play (không ghi file), trả lại cấp cũ khi xong. Ảnh tho_fx/dich_<tướng>_<dạng>_<đòn>_<n>.jpg
        static readonly (string hero, int stage)[] AiMoDau = { ("thach_nhan", 281), ("lung_vuong", 285), ("cao_da", 290), ("ho_khoan", 295) };

        [MenuItem("PokiClash/Thử/Đảo Thổ: 4 tướng dạng 2 ở PHE ĐỊCH (trên sân), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryPheDich()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(PheDich(35, "d2"));
        }

        static IEnumerator PheDich(int level, string nhan)
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            try
            {
                foreach (var (hero, sid) in AiMoDau)
                {
                    var st0 = App.Data.Stage(sid);
                    if (st0 == null || st0.enemies.Count == 0) continue;
                    var e = st0.enemies[0];
                    int lv0 = e.level;
                    bool evo0 = e.evo;
                    e.level = level;
                    e.evo = false;
                    string ten = $"dich_{hero}_{nhan}";
                    foreach (var f in Directory.GetFiles(Dir, ten + "_*.jpg")) File.Delete(f);
                    try
                    {
                        var s = App.Save.Data;
                        if (s.level < 7) s.level = 7;
                        App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = sid });
                        float t0 = Time.realtimeSinceStartup;
                        while ((App.Router.Busy || App.Router.Current != SceneIds.Battle) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                        yield return new WaitForSecondsRealtime(0.5f);
                        var ctl = Object.FindAnyObjectByType<BattleController>();
                        var st = Object.FindAnyObjectByType<StageView>();
                        if (!ctl || !st) yield break;
                        st.speed = 1;
                        t0 = Time.realtimeSinceStartup;
                        while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 20) yield return null;
                        yield return new WaitForSecondsRealtime(0.6f);
                        int n = 0;
                        st.Play(1, StageView.Attack);
                        float start = Time.realtimeSinceStartup;
                        while (Time.realtimeSinceStartup - start < 1.6f) yield return Shot($"{ten}_danh_{n++:00}");
                        yield return new WaitForSecondsRealtime(0.4f);
                        n = 0;
                        st.Play(1, StageView.Cast, () => st.Beam(1));
                        start = Time.realtimeSinceStartup;
                        while (Time.realtimeSinceStartup - start < 3.0f) yield return Shot($"{ten}_mana_{n++:00}");
                        yield return new WaitForSecondsRealtime(0.6f);
                        n = 0;
                        st.Play(1, StageView.Skill, () => st.UltFx(1));
                        start = Time.realtimeSinceStartup;
                        while (Time.realtimeSinceStartup - start < 4.2f) yield return Shot($"{ten}_ult_{n++:00}");
                        yield return new WaitForSecondsRealtime(0.4f);
                        Debug.Log($"[Thử] {ten}: xong");
                    }
                    finally
                    {
                        e.level = lv0;
                        e.evo = evo0;
                    }
                    App.Router.Go(SceneIds.Hub);
                    float t1 = Time.realtimeSinceStartup;
                    while ((App.Router.Busy || App.Router.Current == SceneIds.Battle) && Time.realtimeSinceStartup - t1 < 20) yield return null;
                    yield return new WaitForSecondsRealtime(0.8f);
                }
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            Debug.Log("[Thử] Xong phe địch đảo Thổ: " + Dir);
        }

        // mở hộp chi tiết ở sao cuối của dạng 1, bấm nút hack tiến hoá, chụp liên tục clip tiến hoá: ảnh tho_fx/tien_hoa/<tướng>_<n>.jpg
        static IEnumerator EvolveAll(string[] ids)
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            string thu = Path.Combine(Dir, "tien_hoa");
            if (Directory.Exists(thu)) Directory.Delete(thu, true);
            Directory.CreateDirectory(thu);
            const System.Reflection.BindingFlags Any = System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic |
                                                      System.Reflection.BindingFlags.Instance;
            try
            {
                foreach (var id in ids)
                {
                    var h = App.Data.Hero(id);
                    if (h == null) continue;
                    for (int star = 1; star < App.Data.Cfg.maxStar; star++)
                    {
                        var from = HeroArt.FormOf(h, star).aola;
                        var to = HeroArt.FormOf(h, star + 1).aola;
                        if (from == to) continue;
                        var hp = App.Save.Data.Hero(id);
                        hp.owned = true;
                        hp.star = star;
                        App.Modals.CloseAll();
                        yield return new WaitForSecondsRealtime(0.3f);
                        HeroDetail.Open(id, null);
                        yield return new WaitForSecondsRealtime(1.5f);
                        yield return Shot(Path.Combine("tien_hoa", $"{id}_00_truoc"));
                        var dlg = Object.FindAnyObjectByType<HeroDetailDialog>();
                        var parts = dlg ? dlg.GetType().GetField("p", Any)?.GetValue(dlg) : null;
                        var hack = parts?.GetType().GetField("hackStar", Any)?.GetValue(parts) as UI.SketchButton;
                        if (!hack)
                        {
                            Debug.LogError("[Thử] Không thấy hộp chi tiết hoặc nút hack tiến hóa");
                            yield break;
                        }
                        Debug.Log($"[Thử] {h.name} {star} sao ({from}) → {star + 1} sao ({to})");
                        hack.SimulateClick();
                        float t0 = Time.realtimeSinceStartup;
                        int n = 0;
                        while (Time.realtimeSinceStartup - t0 < 4.8f) yield return Shot(Path.Combine("tien_hoa", $"{id}_{++n:00}"));
                        break;
                    }
                }
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Modals.CloseAll();
            Debug.Log("[Thử] Xong tiến hoá đảo Thổ: " + thu);
        }

        [MenuItem("PokiClash/Thử/Đảo Thổ: cả 5 tướng đầu lần lượt, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryCaNam()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunAll(Nam, 1));
        }

        // Thạch Giáp (tatu mai đá hổ phách, suất thach_nhan ải 1, rig cong_da_1)
        [MenuItem("PokiClash/Thử/Đảo Thổ: riêng Thạch Giáp, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryThachGiap() => Try("thach_nhan", 1);

        // Sa Tích (thằn lằn áo choàng đất nung, suất lung_vuong ải 5, rig than_lan_cat_1)
        [MenuItem("PokiClash/Thử/Đảo Thổ: riêng Sa Tích, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TrySaTich() => Try("lung_vuong", 1);

        // Tê Thiềm (cóc tê giác đất nung, suất cao_da ải 10, rig thu_da_1)
        [MenuItem("PokiClash/Thử/Đảo Thổ: riêng Tê Thiềm, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryTeThiem() => Try("cao_da", 1);

        // Sa Long (rồng giáp sa thạch, suất ho_khoan ải 15, rig rong_cat_1)
        [MenuItem("PokiClash/Thử/Đảo Thổ: riêng Sa Long, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TrySaLong() => Try("ho_khoan", 1);

        // Sơn Viên (vượn núi đá bốn tay, suất phu_van ải 20, rig quy_nui_1)
        [MenuItem("PokiClash/Thử/Đảo Thổ: riêng Sơn Viên, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TrySonVien() => Try("phu_van", 1);

        public static void Try(string hero, int star)
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(Run(hero, star));
        }

        static IEnumerator RunAll(string[] heroes, int star)
        {
            foreach (var h in heroes)
            {
                yield return Run(h, star);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current == SceneIds.Battle) && Time.realtimeSinceStartup - t0 < 20) yield return null;
                yield return new WaitForSecondsRealtime(0.8f);
            }
            Debug.Log("[Thử] Xong cả " + heroes.Length + " tướng đảo Thổ: " + Dir);
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
            Debug.Log("[Thử] Xong đảo Thổ: " + Dir);
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
