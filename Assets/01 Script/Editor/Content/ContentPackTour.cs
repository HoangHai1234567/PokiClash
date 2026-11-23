// Tour thử gói tải sau (GD_Claude/27_TaiNoiDungSau.md). Menu "PokiClash/Tải sau/Tour thử" hoặc cờ Temp/content_pack_tour.flag (Unity
// đang không Play thì tự vào Play). Sao lưu bản lưu, xong trả lại rồi Stop. Log "[Tải sau]", ảnh Temp/PokiShots/tai_sau/*.png:
//  1. vào đảo Hỏa: gói hoa nạp xong mới vào, ảnh bản đồ có thật (không phải ảnh thay thế / trống);
//  2. vào một ải Hỏa có địch ngoài dòng khởi đầu: tướng địch có hình;
//  3. giả lập gói chưa tải + mất mạng, chạm đảo Kim: ở lại sảnh, gói kim Failed, có lời báo;
//  4. bật lại mạng, chạm đảo Kim: chờ tải giả (có lời báo đang tải) rồi vào đảo.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ContentPackTour
    {
        static double nextPoll, tourStart;
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/content_pack_tour.flag"));
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/tai_sau"));

        [MenuItem("PokiClash/Tải sau/Tour thử (vào đảo, trận, mất mạng)", priority = 170)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Tour());
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
                SessionState.SetBool("ContentPackTour", true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 180)
            {
                Debug.LogWarning("[Tải sau] Tour quá 180 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("ContentPackTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("ContentPackTour", false);
                BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            Directory.CreateDirectory(Dir);
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static IEnumerator Until(System.Func<bool> ok, float timeout)
        {
            float end = Time.realtimeSinceStartup + timeout;
            while (!ok() && Time.realtimeSinceStartup < end) yield return null;
        }

        static IEnumerator Go(string scene, object args)
        {
            App.Router.Go(scene, args);
            yield return null;
            yield return Until(() => !App.Router.Busy, 30);
            yield return new WaitForSecondsRealtime(0.5f);
        }

        static string MapSprite()
        {
            var img = Object.FindObjectsByType<Image>(FindObjectsSortMode.None).FirstOrDefault(i => i.name.StartsWith("anh_land_") || i.name.StartsWith("anh_zone_"));
            return img ? $"{img.name}: {(img.sprite ? img.sprite.name : "TRỐNG")}" : "không thấy ảnh bản đồ";
        }

        static IEnumerator Tour()
        {
            int fails = 0;
            void Check(bool ok, string what)
            {
                if (!ok) fails++;
                Debug.Log($"[Tải sau] {(ok ? "đạt" : "HỎNG")}: {what}");
            }

            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            ContentPacks.SimulateMissing = false;
            ContentPacks.SimulateOffline = false;
            try
            {
                if (App.Router.Current != SceneIds.Hub) yield return Go(SceneIds.Hub, null);

                // 1. đảo Hỏa
                yield return Go(SceneIds.Zone, Elem.Hoa);
                Check(App.Router.Current == SceneIds.Zone, $"vào đảo Hỏa (màn {App.Router.Current})");
                Check(ContentPacks.Ready("hoa"), $"gói hoa {ContentPacks.StateOf("hoa")}");
                string map = MapSprite();
                Check(map.Contains("land_hoa") || map.Contains("zone_hoa"), "ảnh bản đồ " + map);
                yield return new WaitForSecondsRealtime(1f);
                yield return Shot("1_dao_hoa");

                // 2. trận ở đảo Hỏa có địch ngoài dòng khởi đầu
                var d = App.Data;
                var st = d.Stages.Where(x => x.zone == Elem.Hoa && x.enemies.Any(e => !d.Starters.Contains(e.hero))).OrderBy(x => x.idx).FirstOrDefault();
                if (st != null)
                {
                    yield return Go(SceneIds.Battle, new BattleArgs { stageId = st.id });
                    Check(App.Router.Current == SceneIds.Battle, $"vào ải {st.id} ({st.name})");
                    yield return new WaitForSecondsRealtime(2.5f);
                    var actors = Object.FindObjectsByType<AolaActor>(FindObjectsSortMode.None);
                    int withAnim = actors.Count(a => a.HasAnim);
                    Check(actors.Length > 0 && withAnim == actors.Length, $"tướng trên sân có hình: {withAnim}/{actors.Length}");
                    yield return Shot("2_tran_hoa");
                    yield return Go(SceneIds.Hub, null);
                }
                else Check(false, "không tìm được ải Hỏa có địch ngoài dòng khởi đầu");

                // 3. gói chưa tải + mất mạng: ở lại sảnh
                ContentPacks.SimulateMissing = true;
                ContentPacks.SimulateOffline = true;
                App.Router.Go(SceneIds.Zone, Elem.Kim);
                yield return Until(() => !App.Router.Busy, 20);
                yield return new WaitForSecondsRealtime(0.3f);
                Check(App.Router.Current == SceneIds.Hub, $"mất mạng: ở lại sảnh (màn {App.Router.Current})");
                Check(ContentPacks.StateOf("kim") == ContentPacks.State.Failed, $"gói kim {ContentPacks.StateOf("kim")} ({ContentPacks.Error("kim")})");
                yield return Shot("3_mat_mang");

                // 4. có mạng lại: chờ tải giả rồi vào
                ContentPacks.SimulateOffline = false;
                App.Router.Go(SceneIds.Zone, Elem.Kim);
                yield return new WaitForSecondsRealtime(1.5f);
                Check(ContentPacks.StateOf("kim") == ContentPacks.State.Downloading, $"đang tải gói kim ({ContentPacks.StateOf("kim")}, {ContentPacks.Progress("kim"):P0})");
                yield return Shot("4_dang_tai");
                yield return Until(() => !App.Router.Busy, 30);
                yield return new WaitForSecondsRealtime(1f);
                Check(App.Router.Current == SceneIds.Zone && ContentPacks.Ready("kim"), $"vào đảo Kim sau khi tải (màn {App.Router.Current}, gói {ContentPacks.StateOf("kim")})");
                map = MapSprite();
                Check(map.Contains("land_kim") || map.Contains("zone_kim"), "ảnh bản đồ " + map);
                yield return Shot("5_dao_kim");
                yield return Go(SceneIds.Hub, null);
            }
            finally
            {
                ContentPacks.SimulateMissing = false;
                ContentPacks.SimulateOffline = false;
            }
            if (backup != null)
            {
                File.WriteAllText(path, backup);
                App.Save.Load();
                Debug.Log("[Tải sau] Đã trả lại bản lưu.");
            }
            Debug.Log($"[Tải sau] Tour xong: {(fails == 0 ? "đạt hết" : fails + " mục hỏng")}. Ảnh: {Dir}");
            tourStart = 0;
            EditorApplication.isPlaying = false;
        }
    }
}
