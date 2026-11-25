// Vòng thử cảm giác trận (2026-11-16, bộ GameFeel): vào Thủy ải 3, Thủy ải 70 (boss), Thổ ải 70 (boss cuối), chọn 5 thẻ (từ 2026-11-25
// mỗi lần chờ bộ bài tráo, chia, lật xong rồi chạm ngay), chụp từng khung lúc chọn và lúc ra đòn vào Temp/PokiShots/game_feel/,
// ghi nhật ký độ epic, số thẻ đang bay, và mỗi cú trúng: khựng, đẩy màn, rung (đọc trường riêng của StageView).
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class GameFeelTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "game_feel");
        const BindingFlags Any = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance;
        const string Hero = "tien_la"; // Cầu Gai, tướng khởi đầu Mộc (giot_suong bị xoá 2026-11-16)

        // ghi cả vào file (công cụ đọc console chỉ lấy dòng đầu của log nhiều dòng)
        static void Log(string s)
        {
            Debug.Log("[Thử] " + s);
            File.AppendAllText(Path.Combine(Dir, "nhat_ky.txt"), s + System.Environment.NewLine);
        }

        [MenuItem("PokiClash/Thử/Trận/Cảm giác trận: chọn thẻ nhanh và đòn trúng ở ải đầu, ải cuối (đang Play)", priority = 124)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
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
                foreach (int stageId in new[] { 3, 70, 350 })
                {
                    var s = App.Save.Data;
                    var hp = s.Hero(Hero);
                    hp.owned = true;
                    hp.star = 11; // Vàng 1★: dạng cuối (bậc sao 2026-11-17; trước là 5 sao)
                    s.team = new List<string> { Hero };
                    if (s.level < 7) s.level = 7;
                    App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stageId });
                    float t0 = Time.realtimeSinceStartup;
                    while ((App.Router.Busy || App.Router.Current != SceneIds.Battle) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                    yield return new WaitForSecondsRealtime(0.5f);
                    var ctl = Object.FindAnyObjectByType<BattleController>();
                    var st = Object.FindAnyObjectByType<StageView>();
                    var view = Object.FindAnyObjectByType<BattleView>();
                    if (!ctl || !st || !view)
                    {
                        Debug.LogError("[Thử] Không thấy BattleController / StageView / BattleView");
                        yield break;
                    }
                    t0 = Time.realtimeSinceStartup;
                    while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 25) yield return null;
                    yield return new WaitForSecondsRealtime(0.8f);
                    string tag = "ai" + stageId;
                    Log($"{tag}: Epic {st.Epic:0.00}, Power phe mình {st.Power(0):0.00}, phe địch {st.Power(1):0.00}");

                    // chọn 5 thẻ: mỗi lần chờ bộ bài chia xong (thẻ đã lật) rồi chạm ngay
                    int picksBefore = ctl.Battle.turn.queue.Count;
                    var watch = App.I.StartCoroutine(Shots(tag + "_chon", 7f));
                    int maxFly = 0;
                    float pickStart = Time.realtimeSinceStartup;
                    for (int k = 0; k < 5; k++)
                    {
                        float w0 = Time.realtimeSinceStartup;
                        while (view.Dealing && Time.realtimeSinceStartup - w0 < 4)
                        {
                            maxFly = Mathf.Max(maxFly, view.Flying);
                            if (stageId == 3) TraceFly(view);
                            yield return null;
                        }
                        ctl.TestPick(k % 3);
                        float w = Time.realtimeSinceStartup;
                        while (Time.realtimeSinceStartup - w < 0.12f)
                        {
                            maxFly = Mathf.Max(maxFly, view.Flying);
                            if (stageId == 3) TraceFly(view);
                            yield return null;
                        }
                    }
                    Log($"{tag}: 5 lần chọn (chờ bộ bài chia mỗi lần) mất {Time.realtimeSinceStartup - pickStart:0.00} giây");
                    if (stageId == 3)
                    {
                        float w2 = Time.realtimeSinceStartup;
                        while (Time.realtimeSinceStartup - w2 < 0.5f)
                        {
                            TraceFly(view);
                            yield return null;
                        }
                    }
                    int picked = ctl.Battle.turn.queue.Count - picksBefore;
                    Log($"{tag}: 5 chạm → nhận {picked} thẻ, tối đa {maxFly} thẻ bay cùng lúc");
                    yield return watch;

                    // ra đòn: chụp và ghi khựng, đẩy màn, rung mỗi khung có thay đổi
                    var fFreeze = typeof(StageView).GetField("freeze", Any);
                    var fBump = typeof(StageView).GetField("bump", Any);
                    var fTrauma = typeof(StageView).GetField("trauma", Any);
                    var shots = App.I.StartCoroutine(Shots(tag + "_danh", 6f));
                    float start = Time.realtimeSinceStartup, lastBump = 0;
                    var log = new System.Text.StringBuilder();
                    // mỗi cú trúng đặt đẩy màn mới (lớn hơn phần đang hồi): bắt lúc đó, đọc khựng còn lại và rung
                    while (Time.realtimeSinceStartup - start < 6f)
                    {
                        float fr = (float)fFreeze.GetValue(st);
                        var bp = (Vector2)fBump.GetValue(st);
                        float tr = (float)fTrauma.GetValue(st);
                        if (bp.magnitude > lastBump + 0.5f)
                            log.AppendLine($"  t={Time.realtimeSinceStartup - start:0.00}s đẩy màn {bp.magnitude:0.0}, khựng còn {fr * 1000:0}ms, rung {tr:0.00}");
                        lastBump = bp.magnitude;
                        yield return null;
                    }
                    yield return shots;
                    Log($"{tag}: các cú trúng trong 6 giây đầu lượt:\n{log}");
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
            Log("Xong cảm giác trận: " + Dir);
        }

        // vết thẻ bay: bản sao UiCard đang bật trong lớp phủ (toạ độ local của lớp phủ, cỡ, góc)
        static void TraceFly(BattleView view)
        {
            var sb = new System.Text.StringBuilder($"  f{Time.frameCount} bay {view.Flying}:");
            foreach (Transform c in view.Overlay)
                if (c.gameObject.activeSelf && c.TryGetComponent<UI.UiCard>(out _))
                    sb.Append($" ({c.localPosition.x:0},{c.localPosition.y:0} s{c.localScale.x:0.00} r{c.localEulerAngles.z:0})");
            if (Time.frameCount % 6 == 0)
            {
                var ov = view.Overlay;
                sb.Append($" | lớp phủ pivot {ov.pivot} rect {ov.rect} | hàng:");
                foreach (Transform c in view.QRow)
                    if (c.gameObject.activeSelf)
                    {
                        var lp = ov.InverseTransformPoint(c.position);
                        var qt = c.GetComponent<QueueTile>();
                        var lc = qt ? ov.InverseTransformPoint(qt.Card.position) : lp;
                        sb.Append($" {c.name}({lp.x:0},{lp.y:0}|card {lc.x:0},{lc.y:0})");
                    }
            }
            File.AppendAllText(Path.Combine(Dir, "nhat_ky.txt"), sb + System.Environment.NewLine);
        }

        static IEnumerator Shots(string name, float len)
        {
            float start = Time.realtimeSinceStartup;
            int n = 0;
            while (Time.realtimeSinceStartup - start < len) yield return Shot($"{name}_{n++:00}");
        }

        // chụp khung đang hiện bằng ScreenCapture (không gán targetTexture cho camera: việc đó làm canvas Screen Space Camera tính lại cỡ
        // giữa chừng, toạ độ UI trong lúc thẻ bay bị lệch)
        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(80));
            Object.DestroyImmediate(tex);
        }
    }
}
