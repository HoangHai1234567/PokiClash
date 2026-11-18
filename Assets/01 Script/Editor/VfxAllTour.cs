// Menu thử (đang Play): MỌI tướng lần lượt ra trận ở sao cuối, mỗi tướng chụp đòn thường, chiêu mana, chiêu cuối. Dùng cho trang so sánh
// hiệu ứng trước / sau một đợt sửa (ArtGen/XemVfx). Ảnh vào Temp/PokiShots/vfx_all/<đợt>/<tướng>/<danh|mana|ult>_<n>.jpg, kèm
// <đợt>/ds.json (tướng, hệ, số ảnh mỗi đòn). Xong trả lại bản lưu như trước. Chạy 57 tướng mất khoảng 12 phút.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class VfxAllTour
    {
        static string dot = "truoc";
        static string[] only;
        static string Root => Path.Combine(PlayTour.ShotDir, "vfx_all", dot);

        [MenuItem("PokiClash/Thử/Hiệu ứng mọi tướng: chụp bản TRƯỚC (đang Play)", priority = 140)]
        static void Truoc() => Start("truoc", null);

        [MenuItem("PokiClash/Thử/Hiệu ứng mọi tướng: chụp bản SAU (đang Play)", priority = 140)]
        static void Sau() => Start("sau", null);

        // gọi từ code khác (vd. chụp lại vài tướng): VfxAllTour.Start("sau", "hoa_nhan", "kim_su")
        public static void Start(string d, params string[] ids)
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            dot = d;
            only = ids != null && ids.Length > 0 ? ids : null;
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (only == null && Directory.Exists(Root)) Directory.Delete(Root, true);
            Directory.CreateDirectory(Root);
            var list = new List<string>();
            foreach (var h in App.Data.Heroes) if (only == null || System.Array.IndexOf(only, h.id) >= 0) list.Add(h.id);
            var counts = new Dictionary<string, int[]>();
            try
            {
                foreach (var hero in list)
                {
                    var def = App.Data.Hero(hero);
                    if (def == null) continue;
                    string dir = Path.Combine(Root, hero);
                    if (Directory.Exists(dir)) Directory.Delete(dir, true);
                    Directory.CreateDirectory(dir);
                    var s = App.Save.Data;
                    var hp = s.Hero(hero);
                    hp.owned = true;
                    hp.star = App.Data.Cfg.maxStar;
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
                        Debug.LogError("[Thử] Không thấy BattleController hoặc StageView ở tướng " + hero);
                        continue;
                    }
                    st.speed = 1;
                    t0 = Time.realtimeSinceStartup;
                    while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 20) yield return null;
                    yield return new WaitForSecondsRealtime(0.6f);
                    var c = new int[3];
                    float start;
                    int n = 0;
                    st.Play(0, StageView.Attack);
                    start = Time.realtimeSinceStartup;
                    while (Time.realtimeSinceStartup - start < 2.0f) yield return Shot(dir, $"danh_{n++:00}");
                    c[0] = n;
                    yield return new WaitForSecondsRealtime(0.5f);
                    n = 0;
                    st.Play(0, StageView.Cast, () => st.Beam(0));
                    start = Time.realtimeSinceStartup;
                    while (Time.realtimeSinceStartup - start < 3.0f) yield return Shot(dir, $"mana_{n++:00}");
                    c[1] = n;
                    yield return new WaitForSecondsRealtime(0.6f);
                    n = 0;
                    st.Play(0, StageView.Skill, () => st.UltFx(0));
                    start = Time.realtimeSinceStartup;
                    while (Time.realtimeSinceStartup - start < 4.2f) yield return Shot(dir, $"ult_{n++:00}");
                    c[2] = n;
                    counts[hero] = c;
                    yield return new WaitForSecondsRealtime(0.4f);
                    Debug.Log($"[Thử] vfx_all {dot}: {hero} xong ({c[0]}/{c[1]}/{c[2]} ảnh)");
                }
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
                WriteList(counts);
            }
            App.Router.Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong hiệu ứng mọi tướng: " + Root);
        }

        static void WriteList(Dictionary<string, int[]> counts)
        {
            // gộp với ds.json cũ (chụp lại vài tướng thì giữ phần còn lại)
            var file = Path.Combine(Root, "ds.json");
            var sb = new StringBuilder("{\n");
            bool first = true;
            foreach (var h in App.Data.Heroes)
            {
                if (!counts.TryGetValue(h.id, out var c))
                {
                    var dir = Path.Combine(Root, h.id);
                    if (!Directory.Exists(dir)) continue;
                    c = new[] { Count(dir, "danh_"), Count(dir, "mana_"), Count(dir, "ult_") };
                }
                if (!first) sb.Append(",\n");
                first = false;
                sb.Append($"  \"{h.id}\": {{\"name\": \"{h.name}\", \"elem\": \"{h.elem.ToString().ToLowerInvariant()}\", \"danh\": {c[0]}, \"mana\": {c[1]}, \"ult\": {c[2]}}}");
            }
            sb.Append("\n}\n");
            File.WriteAllText(file, sb.ToString(), new UTF8Encoding(false));
        }

        static int Count(string dir, string prefix) => Directory.GetFiles(dir, prefix + "*.jpg").Length;

        // chụp nhỏ (720 rộng, jpg) bằng cách tự render camera như HoaFxTour.Shot (Editor không có tiêu điểm thì Game view không vẽ)
        static IEnumerator Shot(string dir, string name)
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
            File.WriteAllBytes(Path.Combine(dir, name + ".jpg"), tex.EncodeToJPG(82));
            Object.DestroyImmediate(tex);
        }
    }
}
