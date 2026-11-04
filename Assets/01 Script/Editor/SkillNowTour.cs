// Menu thử (đang Play): Chiêu ra đòn ngay lúc bấm (2026-11-03). Giọt Sương một mình vào ải 3, chọn 1 thẻ, nạp đầy mana, bấm nút Chiêu
// (qua đúng nút trên màn), chụp nhỏ liên tục lúc chiêu chạy vào Temp/PokiShots/chieu_ngay/; kiểm: máu địch giảm ngay, hàng thẻ và số lần
// chọn giữ nguyên, vẫn đang chọn; rồi chọn nốt và chụp lúc ra đòn. Xong trả lại bản lưu như trước.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class SkillNowTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "chieu_ngay");

        [MenuItem("PokiClash/Thử/Chiêu ra đòn ngay rồi chọn tiếp (đang Play)", priority = 113)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Until(System.Func<bool> cond, float timeout)
        {
            float t0 = Time.realtimeSinceStartup;
            while (!cond() && Time.realtimeSinceStartup - t0 < timeout) yield return null;
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            try
            {
                var s = App.Save.Data;
                s.Hero("giot_suong").owned = true;
                s.team = new List<string> { "giot_suong" };
                if (s.level < 7) s.level = 7;
                App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = 3 });
                yield return Until(() => !App.Router.Busy && App.Router.Current == SceneIds.Battle, 30);
                yield return new WaitForSecondsRealtime(0.5f);
                var ctl = Object.FindAnyObjectByType<BattleController>();
                var view = Object.FindAnyObjectByType<BattleView>();
                if (!ctl || !view)
                {
                    Debug.LogError("[Thử] Không thấy BattleController hoặc BattleView");
                    yield break;
                }
                yield return Until(() => ctl.WaitingPlayer, 30);
                yield return new WaitForSecondsRealtime(0.4f);
                ctl.TestPick(0);
                yield return Until(() => ctl.WaitingPlayer, 5);

                var b = ctl.Battle;
                var foe = b.ActiveOf(1);
                b.ActiveOf(0).mana = b.Data.Cfg.maxMana;
                view.RenderBottom(false);
                yield return new WaitForSecondsRealtime(0.3f);
                double hp0 = foe.hp + foe.shield;
                int q0 = b.turn.queue.Count, left0 = b.turn.picksLeft;
                yield return Shot("0_truoc_chieu");
                view.OnInnate?.Invoke(InnateKind.Skill, view.SkillBtn);
                int n = 0;
                float start = Time.realtimeSinceStartup;
                yield return null;
                while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - start < 6) yield return Shot($"1_chieu_{n++:00}");
                yield return new WaitForSecondsRealtime(0.3f);
                yield return Shot("2_sau_chieu");
                bool ok = foe.hp + foe.shield < hp0 && b.turn.queue.Count == q0 && b.turn.picksLeft == left0 && b.phase == Phase.Picking && b.turn.skillUsed;
                Debug.Log($"[Thử] Chiêu ra ngay: {(ok ? "ĐẠT" : "LỖI")}: máu+khiên địch {hp0} → {foe.hp + foe.shield}, hàng thẻ {q0} → {b.turn.queue.Count}, " +
                          $"còn chọn {left0} → {b.turn.picksLeft}, pha {b.phase}, chiếu {Time.realtimeSinceStartup - start:0.0} s ({n} ảnh)");

                // chọn nốt rồi chụp lúc ra đòn (cuối lượt không bắn chiêu lần nữa)
                while (ctl.WaitingPlayer && b.phase == Phase.Picking && b.turn.side == 0)
                {
                    ctl.TestPick(0);
                    yield return new WaitForSecondsRealtime(0.1f);
                    yield return Until(() => ctl.WaitingPlayer || b.phase != Phase.Picking, 5);
                }
                start = Time.realtimeSinceStartup;
                n = 0;
                while (Time.realtimeSinceStartup - start < 3) yield return Shot($"3_ra_don_{n++:00}");

                // chiêu hạ tướng đối thủ (ải 3 có tướng dự bị): hết lúc chọn, thẻ đã xếp chạy, địch đưa tướng khác ra, trận không kẹt
                App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = 3 });
                yield return Until(() => !App.Router.Busy && App.Router.Current == SceneIds.Battle, 30);
                yield return new WaitForSecondsRealtime(0.5f);
                ctl = Object.FindAnyObjectByType<BattleController>();
                view = Object.FindAnyObjectByType<BattleView>();
                yield return Until(() => ctl.WaitingPlayer, 30);
                ctl.TestPick(0);
                yield return Until(() => ctl.WaitingPlayer, 5);
                b = ctl.Battle;
                foe = b.ActiveOf(1);
                b.ActiveOf(0).mana = b.Data.Cfg.maxMana;
                foe.hp = 1;
                foe.shield = 0;
                view.RenderBottom(false);
                view.OnInnate?.Invoke(InnateKind.Skill, view.SkillBtn);
                start = Time.realtimeSinceStartup;
                n = 0;
                while (b.turn.side == 0 && b.phase != Phase.Over && Time.realtimeSinceStartup - start < 15)
                {
                    yield return Shot($"4_ha_dich_{n++:00}");
                    yield return new WaitForSecondsRealtime(0.25f);
                }
                yield return Shot("5_luot_dich");
                bool ok2 = foe.dead && b.turn.side == 1 && b.ActiveOf(1) != foe && !b.ActiveOf(1).dead;
                Debug.Log($"[Thử] Chiêu hạ địch: {(ok2 ? "ĐẠT" : "LỖI")}: địch cũ gục {foe.dead}, lượt bên {b.turn.side}, pha {b.phase}, " +
                          $"tướng địch ra sân {b.ActiveOf(1).hero.name}, sau {Time.realtimeSinceStartup - start:0.0} s");
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
            Debug.Log("[Thử] Xong Chiêu ra ngay: " + Dir);
        }

        // chụp nhỏ (nửa màn, jpg) bằng cách tự render camera (Editor không có tiêu điểm thì Game view không vẽ)
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
