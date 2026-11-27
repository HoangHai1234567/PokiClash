// Mùa trong game (Season, HubSeason; người dùng 2026-11-27):
// - menu "PokiClash/Thử/Mùa/Theo ngày | Noel | Không mùa": ép mùa để thử (PlayerPrefs Season.DevKey); đang Play thì dựng lại sảnh (Nhà, đảo Casino) ngay;
// - tour "PokiClash/Thử/Mùa/Chụp sảnh mùa Noel" hoặc cờ Temp/hub_season_tour.flag (Unity không Play: tự vào Play, chạy, Stop): ép Noel,
//   vào sảnh, chụp ban ngày, cho ông già Noel bay ngay và chụp 3 lúc, chụp ban đêm, ghi bài nhạc đang phát; xong trả mùa ép, giờ ép
//   và bản lưu như cũ. Ảnh Temp/PokiShots/mua_noel/, log "[Mùa]".
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class SeasonMenu
    {
        const string Key = "HubSeasonTour", DevKeep = "HubSeasonTourDev";
        static double nextPoll, tourStart;
        static bool fromFlag, loadShots;
        static int shot;
        static readonly List<string> log = new List<string>();
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/hub_season_tour.flag"));
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/mua_noel"));

        static void Set(int v)
        {
            if (v < 0) PlayerPrefs.DeleteKey(Season.DevKey);
            else PlayerPrefs.SetInt(Season.DevKey, v);
            PlayerPrefs.Save();
            Debug.Log($"[Mùa] Mùa đang dùng: {Season.Current}" + (v < 0 ? " (theo ngày)" : " (ép)"));
            if (EditorApplication.isPlaying && HubSeason.Current) HubSeason.Current.Apply();
            if (EditorApplication.isPlaying && MapSeason.Current) MapSeason.Current.Apply(); // Nhà, đảo Casino
        }

        [MenuItem("PokiClash/Thử/Mùa/Theo ngày", priority = 300)]
        static void ByDate() => Set(-1);

        [MenuItem("PokiClash/Thử/Mùa/Noel", priority = 301)]
        static void Noel() => Set((int)SeasonId.Noel);

        [MenuItem("PokiClash/Thử/Mùa/Không mùa", priority = 302)]
        static void None() => Set((int)SeasonId.None);

        [MenuItem("PokiClash/Thử/Mùa/Ông già Noel bay ngay (đang Play)", priority = 310)]
        static void FlyNow()
        {
            if (EditorApplication.isPlaying && HubSeason.Current && HubSeason.Current.Santa) HubSeason.Current.Santa.FlyNow();
        }

        [MenuItem("PokiClash/Thử/Mùa/Chụp sảnh mùa Noel", priority = 320)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                ResetDir();
                SessionState.SetInt(DevKeep, PlayerPrefs.GetInt(Season.DevKey, -1));
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "menu");
        }

        static void ResetDir()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            shot = 0;
            log.Clear();
        }

        // màn tải lúc mở game (chuyến tàu đi lên, logo, thanh tải): 3 ảnh cách 0,7 giây
        static IEnumerator LoadShots()
        {
            var vs = VoyageSeason.Current;
            bool santa = ShipVoyage.I && ShipVoyage.I.GetComponentInChildren<SantaFlyby>(true);
            Note($"màn tải: mùa {(vs ? vs.Built.ToString() : "KHÔNG có VoyageSeason")}, tuyết rơi {(vs && vs.Snow ? "có" : "KHÔNG")}, " +
                 $"ông già Noel {(santa ? "CÓ (sai: chỉ ở sảnh)" : "không (đúng)")}, nhạc đang phát {App.Audio.CurrentMusic}");
            for (int i = 0; i < 3 && ShipVoyage.Booting; i++)
            {
                yield return new WaitForSecondsRealtime(0.7f);
                yield return new WaitForEndOfFrame();
                var tex = ScreenCapture.CaptureScreenshotAsTexture();
                File.WriteAllBytes(Path.Combine(Dir, $"0{i}_tai_{i + 1}.jpg"), tex.EncodeToJPG(88));
                Object.Destroy(tex);
            }
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
                ResetDir();
                // ép Noel ngay từ màn tải; mùa ép cũ trả lại cuối tour
                SessionState.SetInt(DevKeep, PlayerPrefs.GetInt(Season.DevKey, -1));
                PlayerPrefs.SetInt(Season.DevKey, (int)SeasonId.Noel);
                PlayerPrefs.Save();
                SessionState.SetBool(Key, true);
                loadShots = false;
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false)) Application.runInBackground = true; // Unity nằm nền thì vòng game đứng
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false) && !loadShots && App.I != null && ShipVoyage.Booting)
            {
                loadShots = true;
                App.I.StartCoroutine(LoadShots());
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 240)
            {
                Debug.LogWarning("[Mùa] Tour quá 240 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null && !App.Booting)
            {
                SessionState.SetBool(Key, false);
                fromFlag = true;
                if (BootTitle.Current) BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        static void Note(string s)
        {
            log.Add(s);
            Debug.Log("[Mùa] " + s);
        }

        static IEnumerator Until(System.Func<bool> ok, float seconds)
        {
            float t0 = Time.realtimeSinceStartup;
            while (!ok() && Time.realtimeSinceStartup - t0 < seconds) yield return null;
        }

        static IEnumerator Shot(string name, float wait = 0.8f)
        {
            yield return new WaitForSecondsRealtime(wait);
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, $"{shot++:00}_{name}.jpg"), tex.EncodeToJPG(88));
            Object.Destroy(tex);
        }

        static IEnumerator Tour()
        {
            Directory.CreateDirectory(Dir);
            shot = 10; // ảnh sảnh đánh số từ 10 (ảnh màn tải 00–02)
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            int devBefore = SessionState.GetInt(DevKeep, -1);
            var hourBefore = DayCycle.Override;
            try
            {
                yield return Until(() => !BootTitle.Current && !App.Booting && !App.Router.Busy, 20);
                PlayerPrefs.SetInt(Season.DevKey, (int)SeasonId.Noel);
                DayCycle.Override = 11f;
                App.Modals.CloseAll();
                if (App.Router.Current != SceneIds.Hub)
                {
                    App.Router.Go(SceneIds.Hub);
                    yield return new WaitForSecondsRealtime(0.3f);
                    yield return Until(() => !App.Router.Busy && App.Router.Current == SceneIds.Hub, 30);
                }
                yield return Until(() => HubSeason.Current != null, 5);
                var hs = HubSeason.Current;
                if (!hs)
                {
                    Note("KHÔNG thấy HubSeason trên sảnh");
                    yield break;
                }
                hs.Apply();
                yield return new WaitForSecondsRealtime(2.5f); // nhạc nối mờ sang bài mùa
                App.Modals.CloseAll();
                Note($"mùa {hs.Built}: tuyết phủ {hs.Covers} đảo ({hs.CoverList}), tuyết rơi {(hs.Snow ? "có" : "KHÔNG")}, ông già Noel {(hs.Santa ? "có" : "KHÔNG")}; " +
                     $"nhạc sảnh {App.Audio.SceneMusic}, đang phát {App.Audio.CurrentMusic}");
                yield return Shot("1_ngay");
                if (hs.Santa)
                {
                    hs.Santa.FlyNow();
                    yield return Shot("2_noel_bay_a", 2.2f);
                    // kéo bản đồ giữa chuyến: ông già Noel phải dời cùng đảo (gắn với thế giới, không đứng yên như giao diện)
                    var pan = Object.FindAnyObjectByType<HubPan>();
                    var isl = Object.FindAnyObjectByType<HubIslandArt>();
                    if (pan && isl && hs.Santa.Team)
                    {
                        var root = hs.transform;
                        Vector3 s0 = root.InverseTransformPoint(hs.Santa.Team.position), i0 = root.InverseTransformPoint(isl.transform.position);
                        pan.SetOffset(new Vector2(220, -160));
                        yield return null;
                        yield return null;
                        Vector3 s1 = root.InverseTransformPoint(hs.Santa.Team.position), i1 = root.InverseTransformPoint(isl.transform.position);
                        Note($"kéo bản đồ: đảo dời {(i1 - i0).magnitude:0} điểm, ông già Noel dời {(s1 - s0).magnitude:0} điểm, " +
                             $"lệch so với đảo {((s1 - i1) - (s0 - i0)).magnitude:0} điểm (vài điểm là quãng bay trong 2 khung)");
                        yield return Shot("2b_sau_keo_ban_do", 0.05f);
                        pan.SetOffset(Vector2.zero);
                    }
                    yield return Shot("3_noel_bay_b", 2.0f);
                    yield return Shot("4_noel_bay_c", 2.2f);
                    Note("ông già Noel đang bay: " + hs.Santa.Flying);
                    yield return Until(() => !hs.Santa.Flying, 8);
                }
                DayCycle.Override = 22f;
                yield return Shot("5_dem", 1.5f);
                DayCycle.Override = 18.2f;
                yield return Shot("6_hoang_hon", 1.0f);
                Note($"Xong: {shot} ảnh ở {Dir}");
            }
            finally
            {
                if (devBefore < 0) PlayerPrefs.DeleteKey(Season.DevKey);
                else PlayerPrefs.SetInt(Season.DevKey, devBefore);
                PlayerPrefs.Save();
                DayCycle.Override = hourBefore;
                App.Modals.CloseAll();
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                    Note(File.ReadAllText(path) == backup ? "đã trả bản lưu cũ (đọc lại khớp)" : "CẢNH BÁO: bản lưu đọc lại không khớp bản sao lưu");
                }
                File.WriteAllLines(Path.Combine(Dir, "log.txt"), log);
                Debug.Log("[Mùa] KẾT THÚC TOUR");
                if (fromFlag)
                {
                    fromFlag = false;
                    tourStart = 0;
                    EditorApplication.isPlaying = false;
                }
            }
        }
    }
}
