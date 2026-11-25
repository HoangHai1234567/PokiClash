// Tour thử bộ bài tráo ở ô chọn thẻ (người dùng 2026-11-25): vào Thủy ải 3 (tướng Cầu Gai dạng cuối), chụp từng khung (ScreenCapture cỡ 1):
// 1_chia: lượt đầu, bộ bài hiện ra, tráo kiểu Riffle uốn lá, chia 3 lá lật mặt; 2_<kiểu>: chọn lá giữa 4 lần, mỗi lần ép một kiểu tráo
// (Chặt ba xấp, Thả từng xấp, Xoa bài, Trải dải: lá chọn bay vào hàng, hai lá về bộ, tráo, chia lại);
// 3_hiem: ép lượt thẻ Hiếm, Sử thi, Huyền thoại (soi viền shader, khựng trước khi lật, bung lúc lật); 4_vien: viền đứng yên 1,2 giây;
// 5_dich: chọn nốt, ra đòn, lượt địch rút lá từ bộ bay vào hàng thẻ địch.
// Menu "PokiClash/Thử/Trận/Bộ bài tráo: chia, lật, viền độ hiếm (chụp)" hoặc cờ Temp/draft_deck_tour.flag (Unity đang không Play: tự Play,
// chạy cả khi Unity nằm nền, xong Stop). Bản lưu sao lưu đầu tour, trả lại trong finally. Ảnh và nhat_ky.txt ở Temp/PokiShots/draft_deck/.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class DraftDeckTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "draft_deck");
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/draft_deck_tour.flag"));
        const string Hero = "tien_la";
        static double nextPoll, tourStart;

        static void Log(string s)
        {
            Debug.Log("[Bộ bài] " + s);
            File.AppendAllText(Path.Combine(Dir, "nhat_ky.txt"), s + System.Environment.NewLine);
        }

        [MenuItem("PokiClash/Thử/Trận/Bộ bài tráo: chia, lật, viền độ hiếm (chụp)", priority = 125)]
        static void Try()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Run(false));
                return;
            }
            File.WriteAllText(Flag, "1");
        }

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            if (!EditorApplication.isPlayingOrWillChangePlaymode)
            {
                if (!File.Exists(Flag)) return;
                File.Delete(Flag);
                SessionState.SetBool("DraftDeckTour", true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("DraftDeckTour", false)) Application.runInBackground = true;
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                Debug.LogWarning("[Bộ bài] Tour quá 150 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("DraftDeckTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("DraftDeckTour", false);
                BootTitle.Dismiss();
                App.I.StartCoroutine(Run(true));
            }
        }

        static IEnumerator Run(bool stopAfter)
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            try
            {
                var s = App.Save.Data;
                var hp = s.Hero(Hero);
                hp.owned = true;
                hp.star = 11;
                s.team = new List<string> { Hero };
                if (s.level < 7) s.level = 7;
                DraftDeck.ForceStyle = (int)DraftDeck.Style.Riffle; // lần tráo đầu (bộ mới hiện) kiểu Riffle uốn lá
                App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = 3 });
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Battle) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                var ctl = Object.FindAnyObjectByType<BattleController>();
                var view = Object.FindAnyObjectByType<BattleView>();
                if (!ctl || !view)
                {
                    Log("LỖI: không thấy BattleController / BattleView");
                    yield break;
                }
                var b = ctl.Battle;

                // 1: lượt đầu của người chơi, bộ bài chia
                t0 = Time.realtimeSinceStartup;
                while (!(b.phase == Phase.Picking && b.turn.side == 0 && view.Dealing) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                Log($"1_chia: bắt đầu chia sau {Time.realtimeSinceStartup - t0:0.00}s, thẻ: {Offer(b)}");
                float d0 = Time.realtimeSinceStartup;
                yield return Shots("1_chia", 1.7f, 1, () => $"dealing {view.Dealing}");
                while (view.Dealing && Time.realtimeSinceStartup - d0 < 5) yield return null;
                Log($"1_chia: chia xong sau {Time.realtimeSinceStartup - d0:0.00}s");

                // 2: chọn lá giữa 4 lần, mỗi lần ép một kiểu tráo: bay vào hàng, hai lá về bộ, tráo, chia lại
                foreach (var style in new[] { DraftDeck.Style.Chop, DraftDeck.Style.Overhand, DraftDeck.Style.Wash, DraftDeck.Style.Fan })
                {
                    yield return WaitPlayer(ctl);
                    if (b.phase != Phase.Picking || b.turn.side != 0) break;
                    DraftDeck.ForceStyle = (int)style;
                    float p0 = Time.realtimeSinceStartup;
                    ctl.TestPick(1);
                    string tagS = "2_" + style.ToString().ToLowerInvariant();
                    var watch = App.I.StartCoroutine(Shots(tagS, 1.45f, 1, () => $"dealing {view.Dealing} bay {view.Flying}"));
                    while (Time.realtimeSinceStartup - p0 < 0.05f || view.Dealing)
                    {
                        if (Time.realtimeSinceStartup - p0 > 5) break;
                        yield return null;
                    }
                    Log($"{tagS}: từ lúc chạm tới khi chia lại xong {Time.realtimeSinceStartup - p0:0.00}s, thẻ mới: {Offer(b)}");
                    yield return watch;
                }
                DraftDeck.ForceStyle = -1;

                // 3: ép lượt thẻ Hiếm / Sử thi / Huyền thoại
                yield return WaitPlayer(ctl);
                var d = App.Data;
                var ids = new[] { Rarity.Rare, Rarity.Epic, Rarity.Legend }
                    .Select(r => d.Pool.FirstOrDefault(c => c.rarity == r)?.id).Where(x => x != null).ToList();
                if (ids.Count == 3 && b.phase == Phase.Picking)
                {
                    b.turn.offer = ids;
                    float r0 = Time.realtimeSinceStartup;
                    view.RenderOffer(false);
                    var w3 = App.I.StartCoroutine(Shots("3_hiem", 2.0f, 1, () => $"dealing {view.Dealing}"));
                    while (view.Dealing && Time.realtimeSinceStartup - r0 < 5) yield return null;
                    Log($"3_hiem: {Offer(b)} chia xong sau {Time.realtimeSinceStartup - r0:0.00}s");
                    yield return w3;
                    yield return Shots("4_vien", 1.2f, 3, null);
                }
                else Log("3_hiem: thiếu thẻ Hiếm / Sử thi / Huyền thoại trong bộ chung");

                // 5: chọn nốt, ra đòn, lượt địch rút từ bộ
                for (int k = 0; k < 6 && b.phase == Phase.Picking && b.turn.side == 0; k++)
                {
                    yield return WaitPlayer(ctl);
                    if (b.phase != Phase.Picking || b.turn.side != 0) break;
                    ctl.TestPick(k % 3);
                    yield return new WaitForSecondsRealtime(0.1f);
                }
                t0 = Time.realtimeSinceStartup;
                while (!(b.phase == Phase.Picking && b.turn.side == 1) && b.phase != Phase.Over && Time.realtimeSinceStartup - t0 < 30) yield return null;
                Log($"5_dich: lượt địch sau {Time.realtimeSinceStartup - t0:0.00}s (pha {b.phase})");
                float e0 = Time.realtimeSinceStartup;
                yield return Shots("5_dich", 3.2f, 2, () => $"bay {view.Flying} hàng {b.turn.queue.Count}");
                while (b.phase == Phase.Picking && b.turn.side == 1 && Time.realtimeSinceStartup - e0 < 10) yield return null;
                Log($"5_dich: địch chọn xong sau {Time.realtimeSinceStartup - e0:0.00}s");
                yield return new WaitForSecondsRealtime(0.5f);
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
            Log("Xong bộ bài: " + Dir);
            if (stopAfter)
            {
                yield return new WaitForSecondsRealtime(1f);
                tourStart = 0;
                EditorApplication.isPlaying = false;
            }
        }

        static string Offer(Battle b) => string.Join(", ", b.turn.offer.Select(id => $"{id}({App.Data.Card(id)?.rarity})"));

        static IEnumerator WaitPlayer(BattleController ctl)
        {
            float t0 = Time.realtimeSinceStartup;
            while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 20) yield return null;
        }

        // chụp mỗi every khung trong len giây; info: dòng nhật ký kèm mỗi ảnh
        static IEnumerator Shots(string name, float len, int every, System.Func<string> info)
        {
            float start = Time.realtimeSinceStartup;
            int n = 0, f = 0;
            var sb = new System.Text.StringBuilder();
            while (Time.realtimeSinceStartup - start < len)
            {
                if (f++ % every == 0)
                {
                    yield return new WaitForEndOfFrame();
                    var tex = ScreenCapture.CaptureScreenshotAsTexture();
                    if (tex)
                    {
                        File.WriteAllBytes(Path.Combine(Dir, $"{name}_{n:000}.jpg"), tex.EncodeToJPG(82));
                        Object.DestroyImmediate(tex);
                    }
                    sb.AppendLine($"  {name}_{n:000} t={Time.realtimeSinceStartup - start:0.000} {info?.Invoke()}");
                    n++;
                }
                yield return null;
            }
            File.AppendAllText(Path.Combine(Dir, "nhat_ky.txt"), sb.ToString());
        }
    }
}
