// Tour chụp bến tàu, chuyến tàu qua mây, màn tải (đang Play): "PokiClash/Thử/Bến tàu: sảnh → Nhà → sảnh, màn tải".
// 1. vào sảnh (mây thường), lướt tới bến, chụp tàu đậu;
// 2. sang Nhà (chuyến tàu đi lên), chụp mỗi 0,2 giây tới khi chuyển xong;
// 3. về sảnh (chuyến tàu đi xuống), chụp như trên;
// 4. màn tải: BeginBoot rồi vào lại sảnh, chụp như trên;
// 5. màn tải lúc hoàng hôn (18h20) và ban đêm (22h), ép giờ DayCycle.
// Ảnh vào Temp/PokiShots/ben_tau/.
using System.Collections;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class ShipVoyageTour
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "ben_tau");

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Bến tàu: sảnh → Nhà → sảnh, màn tải (đang Play)", priority = 141)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Wait(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id || App.Booting) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        static IEnumerator Film(string tag, string id, float step = 0.2f)
        {
            float t0 = Time.realtimeSinceStartup;
            int n = 0;
            while (Time.realtimeSinceStartup - t0 < 20)
            {
                yield return Shot($"{tag}_{n:00}");
                n++;
                if (!App.Router.Busy && App.Router.Current == id && !App.Booting) break;
                float t1 = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - t1 < step) yield return null;
            }
            yield return new WaitForSecondsRealtime(0.4f);
            yield return Shot($"{tag}_xong");
        }

        static IEnumerator Run()
        {
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*.jpg")) File.Delete(f);
            float tb = Time.realtimeSinceStartup;
            while ((App.Booting || App.Router.Busy) && Time.realtimeSinceStartup - tb < 30) yield return null; // màn tải lúc Play
            App.Modals.CloseAll();
            if (App.Router.Current != SceneIds.Hub)
            {
                App.Router.Go(SceneIds.Hub);
                yield return Wait(SceneIds.Hub);
            }
            yield return new WaitForSecondsRealtime(0.8f);
            App.Modals.CloseAll();
            var pier = PierShip.Active;
            var pan = Object.FindAnyObjectByType<HubPan>();
            if (pier && pan)
            {
                pan.GlideTo(pier.ShipRect);
                yield return new WaitForSecondsRealtime(1.4f);
            }
            yield return Shot("0_ben_sanh");
            // 2. sang Nhà
            App.Router.Go(SceneIds.Home);
            yield return Film("1_di_nha", SceneIds.Home);
            yield return new WaitForSecondsRealtime(0.8f);
            App.Modals.CloseAll();
            // 3. về sảnh
            App.Router.Go(SceneIds.Hub);
            yield return Film("2_ve_dao", SceneIds.Hub);
            yield return new WaitForSecondsRealtime(0.8f);
            App.Modals.CloseAll();
            // 4. màn tải
            if (ShipVoyage.I)
            {
                ShipVoyage.I.BeginBoot();
                App.Router.Go(SceneIds.Hub);
                yield return Film("3_man_tai", SceneIds.Hub, 0.25f);
                // tàu cập bến dưới rồi tự chạy nhanh vòng ngoài đảo lên bến trên (người chơi vẫn tương tác)
                for (int k = 0; k < 10; k++)
                {
                    yield return new WaitForSecondsRealtime(0.4f);
                    yield return Shot($"3_chuyen_ben_{k:00}");
                }
                var pier2 = PierShip.Active;
                var pan2 = Object.FindAnyObjectByType<HubPan>();
                if (pier2 && pan2)
                {
                    pan2.GlideTo(pier2.ShipRect);
                    yield return new WaitForSecondsRealtime(1.6f);
                    yield return Shot("3_ben_tren");
                }
            }
            // 5. màn tải và sảnh lúc hoàng hôn, ban đêm (DayCycle ép giờ): mây, biển, tàu, đèn lồng theo giờ
            foreach (var (tag, hour) in new[] { ("4_hoang_hon", 18.3f), ("5_dem", 22f) })
            {
                DayCycle.Override = hour;
                yield return new WaitForSecondsRealtime(0.8f);
                if (ShipVoyage.I)
                {
                    ShipVoyage.I.BeginBoot();
                    App.Router.Go(SceneIds.Hub);
                    yield return Film(tag, SceneIds.Hub, 0.5f);
                }
            }
            DayCycle.Override = null;
            Debug.Log("[Thử] Xong bến tàu: " + Path.GetFullPath(Dir));
        }

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
