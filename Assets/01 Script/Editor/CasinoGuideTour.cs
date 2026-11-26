// Tour thử lời dẫn của Lão Mực trên đảo Casino (D6 + D7, 2026-11-27; App/Scenes/Casino/CasinoGuide.cs, lớp phủ GuideOverlay):
// xoá cờ "đã nghe" của đảo trong bản lưu (chỉ trong lúc chạy), rồi lần lượt: ra đảo (Lão Mực đón ở bến, góc màn, khoanh Tháp và Bến câu),
// Quán trọ (hộp thoại, khoanh bảng việc), Bến câu (góc màn) + một câu bình phẩm Cá Vua, Chợ đen (góc màn), lều Đêm Bài (chính ông nói
// trên sân khấu, không tối màn), Hầm đấu. Mỗi câu chụp một ảnh rồi chạm giả để qua câu kế.
// Menu "PokiClash/Thử/Đảo Casino/Lão Mực dẫn: đón ở bến, các trò (chụp)" hoặc cờ Temp/casino_guide_tour.flag (Unity không Play thì tự
// Play, chạy cả khi Unity nằm nền, xong Stop). Bản lưu sao lưu đầu tour, trả lại cuối tour. Ảnh: Temp/PokiShots/casino_muc/.
using System.Collections;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class CasinoGuideTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "casino_muc");
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/casino_guide_tour.flag"));
        const string Key = "CasinoGuideTour";
        static double nextPoll, tourStart;

        static void Log(string s)
        {
            Debug.Log("[Lão Mực dẫn] " + s);
            File.AppendAllText(Path.Combine(Dir, "nhat_ky.txt"), s + System.Environment.NewLine);
        }

        [MenuItem("PokiClash/Thử/Đảo Casino/Lão Mực dẫn: đón ở bến, các trò (chụp)", priority = 152)]
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
                SessionState.SetBool(Key, true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false)) Application.runInBackground = true;
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 240)
            {
                Debug.LogWarning("[Lão Mực dẫn] Tour quá 240 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool(Key, false);
                BootTitle.Dismiss();
                App.I.StartCoroutine(SessionState.GetBool(Key + "Hub", false) ? HubShot() : Run(true));
                SessionState.SetBool(Key + "Hub", false);
            }
        }

        // đảo Casino trên bản đồ sảnh (menu HubCasinoMenu): kéo về góc dưới trái, chụp; cờ Temp/casino_guide_tour.flag có chữ "sanh"
        [MenuItem("PokiClash/Thử/Đảo Casino/Đảo Casino trên bản đồ sảnh (chụp)", priority = 153)]
        static void TryHub()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(HubShot());
                return;
            }
            SessionState.SetBool(Key + "Hub", true);
            File.WriteAllText(Flag, "sanh");
        }

        static IEnumerator HubShot()
        {
            Directory.CreateDirectory(Dir);
            yield return Go(SceneIds.Hub);
            yield return new WaitForSecondsRealtime(1.5f);
            App.Modals.CloseAll();
            var pan = Object.FindAnyObjectByType<HubPan>();
            if (pan)
            {
                pan.SetOffset(new Vector2(3000, 3000)); // dây chun kéo về sát giới hạn dưới trái
                yield return new WaitForSecondsRealtime(2.4f);
            }
            App.Modals.CloseAll();
            yield return Shot("8_sanh_dao_casino");
            Log("8_sanh_dao_casino: xong");
            yield return new WaitForSecondsRealtime(0.5f);
            EditorApplication.isPlaying = false;
        }

        static IEnumerator WaitRouter(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(82));
            Object.DestroyImmediate(tex);
        }

        // chờ lớp phủ hiện câu Lão Mực, chụp, chạm giả; lặp tới khi hết câu (hoặc hết giờ chờ)
        static IEnumerator Lines(string tag, int max = 6, float wait = 5)
        {
            for (int i = 0; i < max; i++)
            {
                float t0 = Time.realtimeSinceStartup;
                while ((GuideOverlay.I == null || GuideOverlay.I.ShownId == null) && Time.realtimeSinceStartup - t0 < wait) yield return null;
                if (GuideOverlay.I == null || GuideOverlay.I.ShownId == null)
                {
                    Log($"{tag}: hết câu sau {i} câu");
                    yield break;
                }
                string id = GuideOverlay.I.ShownId;
                yield return new WaitForSecondsRealtime(0.5f); // Lão Mực trồi lên, clip mở câu
                yield return Shot($"{tag}_{i}");
                Log($"{tag}_{i}: {id} ({GuideOverlay.I.ShownMode})");
                GuideOverlay.I.DebugTap();
                yield return new WaitForSecondsRealtime(0.25f);
            }
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Modals.CloseAll();
            App.Router.Go(scene, args);
            yield return WaitRouter(scene);
            yield return new WaitForSecondsRealtime(0.8f);
        }

        static IEnumerator Run(bool stopAfter)
        {
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir)) File.Delete(f);
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            bool hints = App.Save.Data.settings.hints;
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 40);
                s.balls = Mathf.Max(s.balls, 20000);
                s.settings.hints = true;
                Tutorial.Off = false;
                Casino.TestAllBooths = true;
                var st = Casino.Of(s);
                st.intro = false;
                st.seen.RemoveAll(k => k.StartsWith("howto:"));

                yield return Go(SceneIds.Casino);
                yield return Lines("1_ben", 6, 8);
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("1_ben_xong");

                App.Modals.CloseAll();
                CasinoGames.Open(Casino.Inn, null);
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Lines("2_quan_tro");
                App.Modals.CloseAll();

                yield return Go(SceneIds.CasinoFishing, Casino.Fishing);
                yield return Lines("3_ben_cau");
                CasinoGuide.Caught(true, false, false, Rarity.Legend); // câu bình phẩm Cá Vua (ghi chú tự tắt, không chặn chạm)
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("3_ben_cau_ca_vua");
                yield return new WaitForSecondsRealtime(3.2f);

                yield return Go(SceneIds.CasinoMarket, Casino.Market);
                yield return Lines("4_cho_den");

                yield return Go(SceneIds.CasinoBlackjack, Casino.Blackjack);
                yield return Lines("5_dem_bai");

                yield return Go(SceneIds.CasinoUnderground);
                yield return Lines("6_ham_dau");

                yield return Go(SceneIds.CasinoRace, Casino.Race);
                yield return Lines("7_truong_dua");
                Log("Xong: " + Dir);
            }
            finally
            {
                Casino.TestAllBooths = false;
                App.Save.Data.settings.hints = hints;
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
            yield return new WaitForSecondsRealtime(1.5f);
            if (stopAfter) EditorApplication.isPlaying = false;
        }
    }
}
