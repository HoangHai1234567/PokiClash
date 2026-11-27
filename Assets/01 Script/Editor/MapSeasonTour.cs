// Tour thử tuyết rơi mùa Noel ở màn Nhà và đảo Casino (MapSeason trong HubSeason.cs; người dùng 2026-11-27). Menu
// "PokiClash/Thử/Mùa/Chụp tuyết Nhà và Casino" hoặc cờ Temp/map_season_tour.flag (Unity không Play: tự vào Play từ Boot, chạy, Stop): ép
// Noel, vào Nhà chụp ban ngày 2 khung cách 0,4 giây (bông phải dời), kéo bản đồ rồi đo tuyết có dời theo không, chụp ban đêm; rồi ra đảo
// Casino làm như vậy. Log ghi số ảnh đổi sang bản tuyết phủ (SeasonSkin); cuối tour tắt mùa, đếm ảnh còn mang bản tuyết (phải 0). Xong trả mùa ép, giờ ép và bản lưu như cũ. Ảnh Temp/PokiShots/mua_noel_map/, log "[Mùa map]".
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class MapSeasonTour
    {
        const string Key = "MapSeasonTour", DevKeep = "MapSeasonTourDev";
        static double nextPoll, tourStart;
        static bool fromFlag;
        static int shot;
        static readonly List<string> log = new List<string>();
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/map_season_tour.flag"));
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/mua_noel_map"));

        [MenuItem("PokiClash/Thử/Mùa/Chụp tuyết Nhà và Casino", priority = 321)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                SessionState.SetInt(DevKeep, PlayerPrefs.GetInt(Season.DevKey, -1));
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "menu");
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
                SessionState.SetInt(DevKeep, PlayerPrefs.GetInt(Season.DevKey, -1));
                PlayerPrefs.SetInt(Season.DevKey, (int)SeasonId.Noel);
                PlayerPrefs.Save();
                SessionState.SetBool(Key, true);
                tourStart = EditorApplication.timeSinceStartup;
                NuocFxMenu.PlayTuBoot();
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false)) Application.runInBackground = true;
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 300)
            {
                Debug.LogWarning("[Mùa map] Tour quá 300 giây: dừng Play.");
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
            Debug.Log("[Mùa map] " + s);
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

        static IEnumerator Go(string id)
        {
            App.Modals.CloseAll();
            App.Router.Go(id);
            yield return new WaitForSecondsRealtime(0.3f);
            yield return Until(() => !App.Router.Busy && App.Router.Current == id, 30);
            yield return Until(() => ShipVoyage.I == null || !ShipVoyage.I.isActiveAndEnabled, 20);
            yield return Until(() => MapSeason.Current && MapSeason.Current.Snow, 5);
            yield return new WaitForSecondsRealtime(1.2f);
            App.Modals.CloseAll();
        }

        static string State(string where)
        {
            var m = MapSeason.Current;
            if (!m) return $"{where}: KHÔNG có MapSeason";
            var sky = m.Snow ? m.Snow.transform.parent : null;
            string sib = sky ? $"lớp trời '{sky.name}' con thứ {sky.GetSiblingIndex()} của '{sky.parent.name}' (sau: " +
                               (sky.GetSiblingIndex() + 1 < sky.parent.childCount ? sky.parent.GetChild(sky.GetSiblingIndex() + 1).name : "không có") + ")" : "";
            string skin = m.Skin ? $"tuyết phủ: {m.Skin.ImageSwaps} ảnh đổi khi quét, {m.Skin.DataSwaps} mục dữ liệu đổi" : "KHÔNG có SeasonSkin";
            return $"{where}: mùa {m.Built}, tuyết rơi {(m.Snow ? $"có {m.Snow.count} bông, hiện {m.Snow.isActiveAndEnabled}" : "KHÔNG")}, {sib}; {skin}";
        }

        static IEnumerator Tour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            shot = 0;
            log.Clear();
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            int devBefore = SessionState.GetInt(DevKeep, -1);
            var hourBefore = DayCycle.Override;
            try
            {
                yield return Until(() => !BootTitle.Current && !App.Booting && !App.Router.Busy, 20);
                PlayerPrefs.SetInt(Season.DevKey, (int)SeasonId.Noel);
                DayCycle.Override = 11f;

                // Nhà
                yield return Go(SceneIds.Home);
                Note(State("Nhà"));
                yield return Shot("nha_1_ngay", 0.2f);
                yield return Shot("nha_2_ngay_sau_0.4s", 0.4f);
                var lv = Object.FindAnyObjectByType<LandView>();
                if (lv && MapSeason.Current && MapSeason.Current.Snow)
                {
                    var sc0 = MapSeason.Current.Snow.scroll;
                    var root = lv.transform;
                    var probe = typeof(LandView).GetField("content", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)?.GetValue(lv) as Transform ?? root.GetChild(0);
                    Vector3 w0 = root.InverseTransformPoint(probe.position);
                    lv.ShiftWorld(lv.transform.TransformVector(new Vector3(260, -180, 0)));
                    yield return null;
                    yield return null;
                    Vector3 w1 = root.InverseTransformPoint(probe.position);
                    Note($"Nhà kéo bản đồ: bản đồ dời {(Vector2)(w1 - w0)}, tuyết dời {MapSeason.Current.Snow.scroll - sc0}");
                    yield return Shot("nha_3_sau_keo", 0.05f);
                }
                DayCycle.Override = 22f;
                yield return Shot("nha_4_dem", 1.5f);
                DayCycle.Override = 11f;

                // đảo Casino
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 40);
                Casino.Of(s).intro = true;
                CasinoGuide.SkipAll(s);
                yield return Go(SceneIds.Casino);
                Note(State("Casino"));
                yield return Shot("casino_1_ngay", 0.2f);
                yield return Shot("casino_2_ngay_sau_0.4s", 0.4f);
                var pan = Object.FindAnyObjectByType<HubPan>();
                if (pan && MapSeason.Current && MapSeason.Current.Snow)
                {
                    var sc0 = MapSeason.Current.Snow.scroll;
                    pan.SetOffset(new Vector2(300, 0));
                    yield return null;
                    yield return null;
                    Note($"Casino kéo bản đồ (+300, 0): tuyết dời {MapSeason.Current.Snow.scroll - sc0}");
                    yield return Shot("casino_3_sau_keo", 0.05f);
                    pan.SetOffset(Vector2.zero);
                }
                DayCycle.Override = 22f;
                yield return Shot("casino_4_dem", 1.5f);
                // tắt mùa: mọi ảnh phải về bản thường
                DayCycle.Override = 11f;
                PlayerPrefs.SetInt(Season.DevKey, (int)SeasonId.None);
                if (MapSeason.Current)
                {
                    MapSeason.Current.Apply();
                    yield return null;
                    int left = 0;
                    foreach (var img in MapSeason.Current.GetComponentsInChildren<UnityEngine.UI.Image>(true))
                        if (SeasonSkin.IsSkin(img.sprite)) left++;
                    Note($"tắt mùa ở Casino: còn {left} ảnh mang bản tuyết (phải 0), tuyết rơi {(MapSeason.Current.Snow ? "CÒN" : "đã tắt")}");
                }
                yield return Shot("casino_5_het_mua", 0.5f);
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
                Debug.Log("[Mùa map] KẾT THÚC TOUR");
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
