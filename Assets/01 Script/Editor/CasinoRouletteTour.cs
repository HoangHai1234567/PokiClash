// Lượt chụp lều Vòng Xoay có Lão Mực (GD_Claude/31, mốc D4). Cờ Temp/casino_rl_dealer_tour.flag: vào Play, ép lều Roulette mở hôm nay
// (chỉ trong bộ nhớ), bỏ hộp Cách chơi, rồi chụp CHUỖI KHUNG đều 20 khung/giây (Time.captureDeltaTime: game chạy theo khung chụp):
// vào lều (greet, mời đặt cửa), ba vòng dò trước hạt giống của lõi: vòng miễn phí trúng 3 cửa (Hỏa 3), vòng bậc 2 trượt hết (Lão
// Mực vơ chip), vòng bậc 3 trúng Sao Vàng. Mỗi vòng kiểm bi nằm đúng ô lõi đã chọn (so vị trí bi với mâm), in vào log.
// Ra Temp/PokiShots/casino_rl_dealer/f_0001.jpg… (ArtGen/Casino/dealer/d4/lam_gif.py ghép ảnh động). Bản lưu sao lưu đầu lượt,
// trả lại trong finally (luật tour-sao-luu-ban-luu).
using System;
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class CasinoRouletteTour
    {
        const float Fps = 20;
        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_rl_dealer");
        static int frame;

        static IEnumerator Go(string id)
        {
            App.Router.Go(id, id);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

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

        // hạt giống đầu tiên mà lõi quay ra đúng ô muốn (Roulette.Spin dùng rng y như lúc chơi)
        static uint FindSeed(RouletteConfig c, int pocket)
        {
            var one = new System.Collections.Generic.List<RlBet> { new RlBet { kind = RlKind.Star, amount = 1 } };
            for (uint s = 1; s < 20000; s++)
                if (Roulette.Spin(c, one, 0, new Rng(s)).pocket == pocket) return s;
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
                CasinoGuide.SkipAll(s); // tour: không hiện lời dẫn của Lão Mực (chặn chạm)
                Casino.MarkSeen(s, "howto:" + Casino.Roulette);
                string today = DateTime.Now.ToString("yyyy-MM-dd");
                added = new CasinoEvent { id = "tour_rl_dealer", name = "Vòng Xoay Ngũ Hành", booth = Casino.Roulette, start = today, end = today };
                cfg.events.Add(added);
                Time.captureDeltaTime = 1f / Fps;
                yield return Go(SceneIds.CasinoRoulette);
                App.Modals.CloseAll();
                var rl = Object.FindAnyObjectByType<RouletteScene>();
                if (!rl) yield break;
                yield return Record(4.6f);                                     // vào lều: greet, mời đặt cửa
                // bảng thông tin gập ở góc trái dưới: mở ra xem rồi gập lại
                var info = rl.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(x => x.name == "thong_tin");
                if (info)
                {
                    info.SimulateClick();
                    yield return Record(1.2f);
                    info.SimulateClick();
                    yield return Record(0.3f);
                }
                var c = Casino.C(App.Data).roulette;
                // (nút bậc cược, các chip, ô lõi phải ra)
                var plans = new (string tierBtn, (RlKind, int)[] bets, int pocket)[]
                {
                    (null, new[] { (RlKind.Elem, 3), (RlKind.Num, 3), (RlKind.Single, 17), (RlKind.Star, 0) }, 17),      // Hỏa 3: trúng 3 cửa
                    ("bac_1", new[] { (RlKind.Elem, 1), (RlKind.Num, 5), (RlKind.Single, 12), (RlKind.Single, 3), (RlKind.Elem, 4) }, 16),   // Hỏa 2: trượt hết
                    ("bac_2", new[] { (RlKind.Star, 0), (RlKind.Star, 0), (RlKind.Elem, 0) }, Roulette.StarPocket),       // Sao Vàng
                };
                int round = 0;
                foreach (var (tierBtn, bets, pocket) in plans)
                {
                    round++;
                    if (tierBtn != null)
                    {
                        var b = rl.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(x => x.name == tierBtn);
                        if (b) b.SimulateClick();
                        yield return Record(0.3f);
                    }
                    foreach (var bet in bets)
                    {
                        rl.BetForTest(bet);
                        yield return Record(0.45f);
                    }
                    yield return Record(0.6f);
                    rl.SeedForTest(FindSeed(c, pocket));
                    rl.SpinForTest();
                    yield return Record(30f, () => !rl.Spinning);
                    // kiểm: bi nằm đúng ô lõi chọn
                    var tr = rl.TrackNow;
                    int got = tr != null ? RouletteWheel.PocketAt(tr.slot) : -1;
                    Debug.Log($"[Thử] Vòng Xoay vòng {round}: lõi ra ô {rl.LastPocket}, muốn {pocket}, bi nằm vị trí {(tr != null ? tr.slot : -1)} = ô {got}; " +
                              (tr != null ? $"{tr.duration:0.00}s, rời vách {tr.dropTime:0.00}s, {tr.laps10 / 10f} vòng, {tr.diamondHits} mấu, {tr.hops} lần nảy, {tr.tries} cú thử, lệch pha {tr.shift} ô" : "không có đường bi") +
                              (got == pocket && rl.LastPocket == pocket ? " · ĐÚNG" : " · SAI"));
                    yield return Record(3.0f);                                 // phản ứng của Lão Mực
                    App.Modals.CloseAll();
                }
                Debug.Log($"[Thử] Xong Vòng Xoay có Lão Mực: {frame} khung ở " + Path.GetFullPath(ShotDir));
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
            var build = Flag("casino_rl_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                CasinoTablesMenu.BuildRouletteOnly();   // chỉ dựng lại lều Vòng Xoay
                return;
            }
            var tour = Flag("casino_rl_dealer_tour.flag");
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
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 500)
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
