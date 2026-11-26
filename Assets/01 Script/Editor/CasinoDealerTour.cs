// Lượt chụp lều Đêm Bài có Lão Mực (GD_Claude/31, mốc D3). Cờ Temp/casino_bj_dealer_tour.flag: vào Play, ép lều Blackjack mở hôm nay
// (chỉ trong bộ nhớ), bỏ hộp Cách chơi, rồi chụp CHUỖI KHUNG đều 20 khung/giây (Time.captureDeltaTime: game chạy theo khung chụp,
// không theo giờ thật, nên chuỗi không giật dù chụp chậm): vào lều (greet), ba ván dò trước hạt giống (Tách + xoè bài, Gấp đôi,
// dealer rút hồi hộp), chơi theo gợi ý.
// Ra Temp/PokiShots/casino_bj_dealer/f_0001.jpg… (ArtGen/Casino/dealer/d3/lam_gif.py ghép ảnh động). Bản lưu sao lưu đầu lượt,
// trả lại trong finally (luật tour-sao-luu-ban-luu).
using System;
using System.Collections;
using System.IO;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class CasinoDealerTour
    {
        const float Fps = 20;
        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_bj_dealer");
        static int frame;

        static IEnumerator Go(string id)
        {
            App.Router.Go(id, id);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        // chụp mọi khung tới khi điều kiện dừng đúng hoặc hết giờ (giây game)
        static IEnumerator Record(float maxSecs, Func<bool> stop = null)
        {
            float t = 0;
            while (t < maxSecs && (stop == null || !stop()))
            {
                yield return new WaitForEndOfFrame();
                var tex = ScreenCapture.CaptureScreenshotAsTexture();
                if (tex)
                {
                    frame++;
                    File.WriteAllBytes(Path.Combine(ShotDir, $"f_{frame:0000}.jpg"), tex.EncodeToJPG(80));
                    Object.DestroyImmediate(tex);
                }
                t += 1f / Fps;
            }
        }

        // hạt giống đầu tiên (1..20000) mà ván chia bằng nó thoả điều kiện (Blackjack.Deal dùng rng y như lúc chơi)
        static uint FindSeed(Func<BjGame, bool> want, BlackjackConfig c)
        {
            for (uint s = 1; s < 20000; s++)
            {
                var g = Blackjack.Deal(10, new Rng(s), c);
                if (want(g)) return s;
            }
            return 1;
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(ShotDir);
            foreach (var f in Directory.GetFiles(ShotDir, "*.jpg")) File.Delete(f);
            frame = 0;
            var cfg = App.Data.Cfg.casino;
            CasinoEvent added = null;
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 60);
                s.balls = Mathf.Max(s.balls, 20000);
                var st = Casino.Of(s);
                st.intro = true;
                Casino.MarkSeen(s, "howto:" + Casino.Blackjack);
                string today = DateTime.Now.ToString("yyyy-MM-dd");
                added = new CasinoEvent { id = "tour_bj_dealer", name = "Đêm Bài", booth = Casino.Blackjack, start = today, end = today };
                cfg.events.Add(added);
                Time.captureDeltaTime = 1f / Fps;
                yield return Go(SceneIds.CasinoBlackjack);
                App.Modals.CloseAll();
                var bj = Object.FindAnyObjectByType<BlackjackScene>();
                if (!bj) yield break;
                yield return Record(3.0f);                                     // vào lều: greet, bong bóng
                // ba ván dò trước hạt giống (lõi tính y như lúc chơi): ván miễn phí có đôi để Tách (kèm xoè bài đầu phiên), ván bậc 3
                // (chip xanh lá) Gấp đôi, ván bậc 4 (chip vàng) người chơi dằn ngay và dealer phải rút khi đang 12–16 (run, mồ hôi)
                var c = Casino.C(App.Data).blackjack;
                var plans = new (string tierBtn, Func<BjGame, bool> want)[]
                {
                    (null, g => g.phase == BjPhase.Player && Blackjack.Can(g, BjAct.Split) && Blackjack.Advice(g) == BjAct.Split),
                    ("bac_2", g => g.phase == BjPhase.Player && Blackjack.Advice(g) == BjAct.Double),
                    ("bac_3", g =>
                    {
                        if (g.phase != BjPhase.Player || Blackjack.Advice(g) != BjAct.Stand) return false;
                        int t2 = Blackjack.Total(new System.Collections.Generic.List<BjCard> { g.dealer[0], g.dealer[1] }, out _);
                        Blackjack.Act(g, BjAct.Stand, c);
                        return t2 >= 12 && t2 <= 16 && g.dealer.Count >= 3;
                    }),
                };
                foreach (var (tierBtn, want) in plans)
                {
                    if (tierBtn != null)
                    {
                        var b = System.Linq.Enumerable.FirstOrDefault(bj.GetComponentsInChildren<SketchButton>(true), x => x.name == tierBtn);
                        if (b) b.SimulateClick();
                        yield return Record(0.3f);
                    }
                    uint seed = FindSeed(want, c);
                    bj.SeedForTest(seed);
                    bj.PlayForTest();                                          // chia bài
                    yield return Record(14f, () => !bj.Animating);
                    int guard = 0;
                    while (bj.GameNow != null && bj.GameNow.phase == BjPhase.Player && guard++ < 10)
                    {
                        yield return Record(0.5f);                             // ngập ngừng như người chơi nghĩ
                        bj.PlayForTest();
                        yield return Record(12f, () => !bj.Animating);
                    }
                    yield return Record(3.0f);                                 // phản ứng của Lão Mực
                    App.Modals.CloseAll();
                }
                Debug.Log($"[Thử] Xong Đêm Bài có Lão Mực: {frame} khung ở " + Path.GetFullPath(ShotDir));
            }
            finally
            {
                Time.captureDeltaTime = 0;
                if (added != null) cfg.events.Remove(added);
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
        }

        static double nextPoll, tourStart;
        static bool tourRunning;
        static string Flag(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            var tour = Flag("casino_bj_dealer_tour.flag");
            if (File.Exists(tour) && !tourRunning)
            {
                if (!EditorApplication.isPlaying)
                {
                    if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true;
                    return;
                }
                Application.runInBackground = true; // Unity nằm nền thì vòng game đứng
                if (App.I == null || App.Router == null || App.Router.Busy || App.Router.Current == null) return;
                File.Delete(tour);
                tourRunning = true;
                tourStart = EditorApplication.timeSinceStartup;
                App.I.StartCoroutine(TourThenStop());
                return;
            }
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 400)
            {
                tourRunning = false;
                Time.captureDeltaTime = 0;
                EditorApplication.isPlaying = false;
            }
        }

        static IEnumerator TourThenStop()
        {
            yield return new WaitForSecondsRealtime(3f);
            yield return Run();
            yield return new WaitForSecondsRealtime(0.5f);
            tourRunning = false;
            EditorApplication.isPlaying = false;
        }
    }
}
