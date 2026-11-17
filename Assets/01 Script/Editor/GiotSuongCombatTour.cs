// Menu thử (đang Play): một tướng một mình vào ải 3 ở các mốc sao của từng dạng; tới lượt chọn thẻ (trận đứng yên) thì tự cho sân
// chạy lần lượt: bắn tia (chiêu mana), chiêu cuối, đánh thường, rồi đối thủ đánh; chụp nhỏ liên tục vào
// Temp/PokiShots/<id>_combat/s<sao>_<đòn>_<n>.jpg; xong trả lại bản lưu như trước.
// Để soi: con ra đòn nằm trên con kia, chiêu cuối lao tới đối thủ, chiêu mana bắn tia to nhỏ theo dạng.
// Tên lớp còn theo Giọt Sương (tướng đầu tiên có menu này); menu của Giọt Sương và các tướng Thủy cũ bỏ cùng tướng 2026-11-16.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class GiotSuongCombatTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, dir);
        static string hero = "ti_tach", dir = "ti_tach_combat";
        static int[] stars = { 1, 5 };

        // Tí Tách (tướng khởi đầu hệ Thủy, ải 1 đảo Thủy, 2 dạng); ảnh vào ti_tach_combat/
        [MenuItem("PokiClash/Thử/Đảo Thủy: Tí Tách ra trận ở 2 dạng (đang Play)", priority = 112)]
        static void Try() => Start("ti_tach", "ti_tach_combat", 1, 11); // sao tổng (bậc sao 2026-11-17): dạng 2 từ 6

        // Thanh Long (boss cuối đảo Mộc, 2026-11-09, skill pokiclash-hero-fx): idle có lá bay, mây trôi; đòn có vệt cầu, vòng bật, lá văng;
        // chiêu ba sét; lúc trúng sân khựng, màn rung, đối thủ bật lùi (AtomikGame.impact*); ảnh vào thanh_long_combat/
        [MenuItem("PokiClash/Thử/Đảo Mộc: Thanh Long ra trận ở 3 dạng (đang Play)", priority = 122)]
        static void TryThanhLong() => Start("thanh_long", "thanh_long_combat", 1, 6, 11);

        // Cầu Gai (suất tien_la, ải 1 đảo Mộc, 2026-11-12): cắn, gồng bung gai, chiêu cuối lăn tông thẳng (AolaSticker.Rams)
        [MenuItem("PokiClash/Thử/Đảo Mộc: Cầu Gai ra trận ở 2 dạng (đang Play)", priority = 122)]
        static void TryCauGai() => Start("tien_la", "cau_gai_combat", 1, 11);

        // Hỏa Cung (suất kim_su, ải 10 đảo Hỏa, 2026-11-13): quỷ lửa bắn cung, tên là mảnh của rig do game lái tới đối thủ (far / fly_*)
        [MenuItem("PokiClash/Thử/Đảo Hỏa: Hỏa Cung ra trận ở 2 dạng (đang Play)", priority = 122)]
        static void TryHoaCung() => Start("kim_su", "hoa_cung_combat", 1, 11);

        [MenuItem("PokiClash/Thử/Hỏa Cung tiến hóa: clip evolve của dạng .atomik (đang Play)", priority = 123)]
        static void TryEvolveHoaCung()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            dir = "hoa_cung_tien_hoa";
            App.I.StartCoroutine(Evolve("kim_su"));
        }

        // mở hộp chi tiết ở sao cuối của từng dạng (trừ dạng chót), bấm nút hack tiến hóa, chụp liên tục clip tiến hóa tới khi dạng
        // sau hiện; ảnh vào <dir>/<mốc>_<n>.jpg (menu đầu tiên là Giọt Sương 2026-11-08, bỏ cùng tướng 2026-11-16)
        static IEnumerator Evolve(string id)
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            const System.Reflection.BindingFlags Any = System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic |
                                                      System.Reflection.BindingFlags.Instance;
            try
            {
                // mọi mốc đổi dạng (sao cuối của mỗi dạng trừ dạng chót): mỗi mốc một lượt, ảnh <mốc>_<n>.jpg
                var h = App.Data.Hero(id);
                int round = 0;
                for (int star = 1; star < App.Data.Cfg.maxStar; star++)
                {
                    var from = HeroArt.FormOf(h, star).aola;
                    var to = HeroArt.FormOf(h, star + 1).aola;
                    if (from == to) continue;
                    round++;
                    var hp = App.Save.Data.Hero(id);
                    hp.owned = true;
                    hp.star = star;
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                    HeroDetail.Open(id, null);
                    yield return new WaitForSecondsRealtime(1.5f);
                    yield return Shot($"{round}_00_truoc");
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
                    while (Time.realtimeSinceStartup - t0 < 4.8f) yield return Shot($"{round}_{++n:00}");
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
            Debug.Log($"[Thử] Xong {id} tiến hóa: " + Dir);
        }

        static void Start(string id, string folder, params int[] at)
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            hero = id;
            dir = folder;
            stars = at;
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            try
            {
                foreach (int star in stars)
                {
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
                    st.speed = 1; // sân chạy chậm (×1 thật đã nhanh gấp 3) để chụp đủ khung mà soi
                    // chờ lượt chọn thẻ (trận đứng yên) rồi tự cho sân chạy từng đòn của tướng thử (phía 0), cuối cùng đối thủ đánh
                    t0 = Time.realtimeSinceStartup;
                    while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 20) yield return null;
                    yield return new WaitForSecondsRealtime(0.6f);
                    Debug.Log($"[Thử] {hero} sao {star}: bắn tia {(st.CanBeam(0) ? "có" : "KHÔNG")}");
                    var acts = new (string name, int side, string clip, bool beam, float len)[]
                    {
                        ("ban", 0, StageView.Cast, true, 2.4f), ("chieu_cuoi", 0, StageView.Skill, false, 3.6f),
                        ("danh", 0, StageView.Attack, false, 1.8f), ("dich_danh", 1, StageView.Attack, false, 1.6f),
                        ("dich_ban", 1, StageView.Cast, true, 2.0f),
                    };
                    foreach (var (name, side, clip, beam, len) in acts)
                    {
                        if (beam) st.Play(side, clip, () => st.Beam(side));
                        else st.Play(side, clip);
                        float start = Time.realtimeSinceStartup;
                        int n = 0;
                        while (Time.realtimeSinceStartup - start < len) yield return Shot($"s{star}_{name}_{n++:00}");
                        yield return new WaitForSecondsRealtime(0.4f);
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
            Debug.Log($"[Thử] Xong {hero} ra trận: " + Dir);
        }

        // chụp nhỏ (540 x 960, jpg) bằng cách tự render camera (Editor không có tiêu điểm thì Game view không vẽ)
        static IEnumerator Shot(string name)
        {
            yield return new WaitForSecondsRealtime(0.08f);
            int w = Screen.width / 2, h = Screen.height / 2;
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
