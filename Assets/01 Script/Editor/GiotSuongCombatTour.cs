// Menu thử (đang Play): Giọt Sương một mình vào ải 3 (đối thủ là quái thường hình aola gốc, không có clip bắn) ở sao 1, 3, 5; tới lượt chọn thẻ (trận đứng yên) thì tự cho sân chạy lần lượt:
// bắn tia (chiêu mana), chiêu cuối, đánh thường, rồi đối thủ đánh; chụp nhỏ liên tục vào Temp/PokiShots/gs_combat/s<sao>_<đòn>_<n>.jpg;
// xong trả lại bản lưu như trước.
// Để soi: con ra đòn nằm trên con kia, chiêu cuối lao tới đối thủ, chiêu mana bắn tia nước to nhỏ theo dạng.
// Menu Tiểu Y (sao 1, 5: hai dạng): dạng 1 (thuy_1319, 2026-11-04) đâm đinh ba, bắn tia từ mũi đinh ba, chiêu cuối ném quả cầu nước
// bay tới nổ ở thân đối thủ (AolaActor hiệu ứng ở xa, anim.json "far_center"); dạng 2 còn hình gốc aola; ảnh vào tieu_y_combat/.
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
        static string hero = "giot_suong", dir = "gs_combat";
        static int[] stars = { 1, 3, 5 };

        [MenuItem("PokiClash/Thử/Giọt Sương ra trận: đánh, bắn tia, chiêu cuối ở 3 dạng (đang Play)", priority = 112)]
        static void Try() => Start("giot_suong", "gs_combat", 1, 3, 5);

        [MenuItem("PokiClash/Thử/Tiểu Y ra trận: đâm đinh ba, bắn tia, ném cầu nước ở 2 dạng (đang Play)", priority = 113)]
        static void TryTieuY() => Start("tieu_y", "tieu_y_combat", 1, 5);

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
                    // chờ lượt chọn thẻ (trận đứng yên) rồi tự cho sân chạy từng đòn của Giọt Sương (phía 0), cuối cùng đối thủ đánh
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
