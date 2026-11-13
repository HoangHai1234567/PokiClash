// Menu thử (đang Play): các tướng đảo Hỏa ra trận lần lượt ở sao cuối, mỗi tướng: chiêu mana (hạt lửa thay tia nước: cầu lửa, kim
// lửa, phun lửa, cầu dung nham) rồi chiêu cuối (clip CHIÊU + hạt: thiên thạch, dung nham phun, lốc xoáy, nổ lớn; StageView.UltFx).
// Chụp nhỏ liên tục vào Temp/PokiShots/hoa_fx/<tướng>_<đòn>_<n>.jpg; xong trả lại bản lưu như trước. Bảng chiêu ở StageView.FireFx.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HoaFxTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "hoa_fx");
        static readonly string[] Heroes = { "hoa_tinh", "huyen_viem", "lan_hoa", "hoa_nhan", "nham_than", "kim_su", "hong_lien", "giap_long", "nguu_quyen" };
        static string[] only;
        static int sao; // > 0: số sao của tướng trong tour trận (mặc định sao cuối); dùng xong tự về 0

        [MenuItem("PokiClash/Thử/Đảo Hỏa: hạt lửa chiêu mana, chiêu cuối 9 tướng (đang Play)", priority = 124)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            only = null;
            App.I.StartCoroutine(Run());
        }

        // riêng Nham Thần (golem lõi lửa, 2026-11-13): phun lửa từ họng, chiêu cuối cuộn thành cầu lửa lăn tông (AolaSticker.Rams)
        [MenuItem("PokiClash/Thử/Đảo Hỏa: riêng Nham Thần, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryNhamThan() => TryOnly("nham_than");

        // TRẬN THẬT ải 15 đảo Hỏa (ải 85 "Sườn Núi Khói": địch là Nham Thần có tiến hóa): đội mình một Nham Thần sao cuối, tự đánh ở nhịp
        // thường; chụp liên tục từ lúc ra sân tới hết trận vào hoa_fx/tran_<n>.jpg (golem phía địch, ra sân, tiến hóa, chết)
        [MenuItem("PokiClash/Thử/Đảo Hỏa: trận thật ải 15, Nham Thần hai phía (đang Play)", priority = 124)]
        static void TryNhamThanTran()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunTran());
        }

        static IEnumerator RunTran()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            try
            {
                var s = App.Save.Data;
                var hp = s.Hero("nham_than");
                hp.owned = true;
                hp.star = App.Data.Cfg.maxStar;
                s.team = new List<string> { "nham_than" };
                if (s.level < 55) s.level = 55;
                App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = 85 });
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Battle) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                var ctl = Object.FindAnyObjectByType<BattleController>();
                var st = Object.FindAnyObjectByType<StageView>();
                if (!ctl || !st)
                {
                    Debug.LogError("[Thử] Không thấy BattleController hoặc StageView");
                    yield break;
                }
                st.speed = 1;
                int n = 0;
                t0 = Time.realtimeSinceStartup;
                while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 25)
                {
                    yield return Shot($"tran_{n++:000}");
                    yield return new WaitForSecondsRealtime(0.1f);
                }
                ctl.TestPick(0);
                t0 = Time.realtimeSinceStartup;
                while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 5) yield return null;
                ctl.TestPick(1);
                t0 = Time.realtimeSinceStartup;
                while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 5) yield return null;
                ctl.SetAuto(true);
                t0 = Time.realtimeSinceStartup;
                // Battle.phase là trạng thái của LUẬT (tính xong trước khi sân diễn): chờ hộp kết quả hiện mới là hết trận trên màn hình
                while (App.Modals.Count == 0 && Time.realtimeSinceStartup - t0 < 160)
                {
                    yield return Shot($"tran_{n++:000}");
                    yield return new WaitForSecondsRealtime(0.2f);
                }
                Debug.Log($"[Thử] Trận ải 85: {ctl.Battle.round} hiệp, {(ctl.Battle.winner == 0 ? "thắng" : "thua")}, {n} ảnh");
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
            App.Router.Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong trận thật Nham Thần: " + Dir);
        }

        // dạng 1 (Nham Con): cùng tour nhưng tướng ở 1 sao
        [MenuItem("PokiClash/Thử/Đảo Hỏa: riêng Nham Con (dạng 1), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryNhamCon()
        {
            sao = 1;
            TryOnly("nham_than");
        }

        [MenuItem("PokiClash/Thử/Đảo Hỏa: riêng Nham Thần trong hộp chi tiết tướng (đang Play)", priority = 125)]
        static void TryNhamThanViewer()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            only = new[] { "nham_than" };
            App.I.StartCoroutine(RunViewer());
        }

        // riêng Hỏa Cung (quỷ lửa bắn cung, suất kim_su, 2026-11-13): thêm đòn thường (một mũi tên của rig bay tới đối thủ) trước chiêu mana
        [MenuItem("PokiClash/Thử/Đảo Hỏa: riêng Hỏa Cung, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryHoaCung() => TryOnly("kim_su");

        // riêng Hỏa Quy (rùa golem lửa, suất nguu_quyen, 2026-11-13): đòn thường bò tới húc sừng, chiêu mana há mồm bắn cầu lửa, chiêu cuối hút
        // lửa trên lưng về sừng rồi hất sừng phóng cầu
        [MenuItem("PokiClash/Thử/Đảo Hỏa: riêng Hỏa Quy, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryHoaQuy() => TryOnly("nguu_quyen");

        // riêng Viêm Đao (quỷ lửa cầm đao, suất giap_long, 2026-11-13): đòn thường bổ đao cối xay, chiêu mana bổ đao cắm đất (dung nham trào dưới
        // chân địch), chiêu cuối lao tới liên hoàn chém rồi nhảy bổ
        [MenuItem("PokiClash/Thử/Đảo Hỏa: riêng Viêm Đao, đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 124)]
        static void TryViemDao() => TryOnly("giap_long");

        // hộp chi tiết tướng: mở từng tướng Hỏa (sao cuối), bấm Chiêu rồi Mana trên ô xem, chụp vào hoa_fx/xem_<tướng>_<clip>_<n>.jpg
        [MenuItem("PokiClash/Thử/Đảo Hỏa: hạt lửa trong hộp chi tiết tướng (đang Play)", priority = 125)]
        static void TryViewer()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunViewer());
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
                    foreach (var (clip, len) in new[] { (HeroViewer.Skill, 3.4f), (HeroViewer.Cast, 2.6f) })
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
            Debug.Log("[Thử] Xong hộp chi tiết đảo Hỏa: " + Dir);
        }

        public static void TryOnly(params string[] ids)
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            only = ids;
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
                foreach (var hero in only ?? Heroes)
                {
                    if (App.Data.Hero(hero) == null) continue;
                    var s = App.Save.Data;
                    var hp = s.Hero(hero);
                    hp.owned = true;
                    hp.star = sao > 0 ? sao : App.Data.Cfg.maxStar;
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
                    int n = 0;
                    if (hero == "kim_su" || hero == "nham_than" || hero == "nguu_quyen" || hero == "giap_long")
                    {
                        st.Play(0, StageView.Attack);
                        start = Time.realtimeSinceStartup;
                        while (Time.realtimeSinceStartup - start < (hero == "giap_long" ? 2.1f : 1.5f)) yield return Shot($"{hero}_danh_{n++:00}");
                        yield return new WaitForSecondsRealtime(0.4f);
                        n = 0;
                    }
                    st.Play(0, StageView.Cast, () => st.Beam(0));
                    start = Time.realtimeSinceStartup;
                    while (Time.realtimeSinceStartup - start < 2.6f) yield return Shot($"{hero}_mana_{n++:00}");
                    yield return new WaitForSecondsRealtime(0.6f);
                    st.Play(0, StageView.Skill, () => st.UltFx(0));
                    start = Time.realtimeSinceStartup;
                    n = 0;
                    while (Time.realtimeSinceStartup - start < 3.8f) yield return Shot($"{hero}_ult_{n++:00}");
                    yield return new WaitForSecondsRealtime(0.4f);
                    Debug.Log($"[Thử] {hero}: xong");
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
            sao = 0;
            App.Router.Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong đảo Hỏa hạt lửa: " + Dir);
        }

        // chụp nhỏ (nửa màn, jpg) bằng cách tự render camera (Editor không có tiêu điểm thì Game view không vẽ)
        static IEnumerator Shot(string name)
        {
            yield return new WaitForSecondsRealtime(0.06f);
            int w = 720, h = Mathf.RoundToInt(720f * Screen.height / Mathf.Max(1, Screen.width)); // cố định 720 rộng: Game view nhỏ thì vẫn soi được
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
