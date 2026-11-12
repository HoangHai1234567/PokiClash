// Menu thử (đang Play): các tướng đảo Thủy có chiêu nước bằng hạt (StageView.WaterFx, HatNuoc.cs) ra trận lần lượt. Mỗi tướng: chiêu
// mana ở dạng cuối, rồi chiêu cuối ở TỪNG dạng (chiêu cuối chọn theo dạng). Chụp nhỏ liên tục vào
// Temp/PokiShots/thuy_fx/<tướng>_<dạng>_<đòn>_<n>.jpg; xong trả lại bản lưu như trước.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class ThuyFxTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "thuy_fx");
        static readonly string[] Heroes = { "tieu_y", "canh_cut", "mi_nhi", "ma_ket", "vay_lam", "kuba", "thuong_lam", "huyen_vu", "lam_quan" };
        static string[] only;

        [MenuItem("PokiClash/Thử/Đảo Thủy: hạt nước chiêu mana, chiêu cuối từng dạng (đang Play)", priority = 126)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            only = null;
            App.I.StartCoroutine(Run());
        }

        // hộp chi tiết tướng: mở từng tướng Thủy (sao cuối), bấm Chiêu rồi Mana trên ô xem
        [MenuItem("PokiClash/Thử/Đảo Thủy: hạt nước trong hộp chi tiết tướng (đang Play)", priority = 127)]
        static void TryViewer()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunViewer());
        }

        public static void TryOnly(params string[] ids)
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            only = ids;
            App.I.StartCoroutine(Run());
        }

        // sao nhỏ nhất cho ra dạng form (0 là dạng đầu)
        static int StarOf(int form)
        {
            var fs = App.Data.Cfg.formStars;
            return form <= 0 || fs == null || fs.Length == 0 ? 1 : fs[Mathf.Min(form, fs.Length) - 1];
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            try
            {
                foreach (var hero in only ?? Heroes)
                {
                    var def = App.Data.Hero(hero);
                    if (def == null) continue;
                    int forms = Mathf.Max(1, def.forms != null ? def.forms.Length : 1);
                    for (int form = forms - 1; form >= 0; form--)
                    {
                        var s = App.Save.Data;
                        var hp = s.Hero(hero);
                        hp.owned = true;
                        hp.star = StarOf(form);
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
                        float start;
                        int n;
                        // đòn đánh thường có hiệu ứng riêng (StageView.FireAtk): chụp trước chiêu
                        if (StageView.FireAtk(def) != null)
                        {
                            st.Play(0, StageView.Attack);
                            start = Time.realtimeSinceStartup;
                            n = 0;
                            while (Time.realtimeSinceStartup - start < 2.0f) yield return Shot($"{hero}_{form + 1}_atk_{n++:00}");
                            yield return new WaitForSecondsRealtime(0.4f);
                        }
                        if (form == forms - 1)
                        {
                            st.Play(0, StageView.Cast, () => st.Beam(0));
                            start = Time.realtimeSinceStartup;
                            n = 0;
                            while (Time.realtimeSinceStartup - start < 3.0f) yield return Shot($"{hero}_{form + 1}_mana_{n++:00}");
                            yield return new WaitForSecondsRealtime(0.5f);
                        }
                        st.Play(0, StageView.Skill, () => st.UltFx(0));
                        start = Time.realtimeSinceStartup;
                        n = 0;
                        while (Time.realtimeSinceStartup - start < 4.4f) yield return Shot($"{hero}_{form + 1}_ult_{n++:00}");
                        yield return new WaitForSecondsRealtime(0.3f);
                        Debug.Log($"[Thử] {hero} dạng {form + 1}: xong");
                        App.Router.Go(SceneIds.Hub);
                        t0 = Time.realtimeSinceStartup;
                        while ((App.Router.Busy || App.Router.Current != SceneIds.Hub) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                        yield return new WaitForSecondsRealtime(0.3f);
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
            App.Router.Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong đảo Thủy hạt nước: " + Dir);
        }

        static IEnumerator RunViewer()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            try
            {
                foreach (var hero in only ?? Heroes)
                {
                    if (App.Data.Hero(hero) == null) continue;
                    var hp = App.Save.Data.Hero(hero);
                    hp.owned = true;
                    hp.star = App.Data.Cfg.maxStar;
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                    HeroDetail.Open(hero, null);
                    yield return new WaitForSecondsRealtime(1.6f);
                    var v = Object.FindAnyObjectByType<HeroViewer>();
                    if (!v)
                    {
                        Debug.LogError("[Thử] Không thấy HeroViewer");
                        yield break;
                    }
                    foreach (var (clip, len) in new[] { (HeroViewer.Skill, 4.0f), (HeroViewer.Cast, 2.8f) })
                    {
                        v.Play(clip);
                        float start = Time.realtimeSinceStartup;
                        int n = 0;
                        while (Time.realtimeSinceStartup - start < len) yield return Shot($"xem_{hero}_{clip}_{n++:00}");
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
            Debug.Log("[Thử] Xong hộp chi tiết đảo Thủy: " + Dir);
        }

        // chụp nhỏ (720 rộng, jpg) bằng cách tự render camera (Editor không có tiêu điểm thì Game view không vẽ)
        static IEnumerator Shot(string name)
        {
            yield return new WaitForSecondsRealtime(0.1f);
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
