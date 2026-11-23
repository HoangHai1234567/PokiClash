// Tour chụp tướng ở màn Nhà (đang Play): "PokiClash/Thử/Nhà: tướng chạy rig, đêm sáng nhẹ (12h, 21h)".
// Sang Nhà (chuyến tàu qua mây), chụp cả màn lúc 12h và 21h, kéo máy tới một tướng đang đi lại chụp gần (camera vẽ gấp đôi) hai giờ đó,
// ghi log số tướng đã chạy rig. Không đổi bản lưu; xong trả giờ máy. Ảnh vào Temp/PokiShots/nha_dem/.
using System.Collections;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HomeNightTour
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "nha_dem");

        [MenuItem("PokiClash/Thử/Nhà và side meta/Nhà và side meta∕Nhà: tướng chạy rig, đêm sáng nhẹ (12h, 21h) (đang Play)", priority = 142)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Run()
        {
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*.jpg")) File.Delete(f);
            try
            {
                if (App.Router.Current != SceneIds.Home) App.Router.Go(SceneIds.Home);
                HomeScene home = null;
                for (float t = 0; t < 25 && !(home && App.Router.CurrentRoot == home); t += 0.25f)
                {
                    yield return new WaitForSecondsRealtime(0.25f);
                    home = Object.FindFirstObjectByType<HomeScene>();
                }
                for (float t = 0; t < 10 && PierShip.Active && PierShip.Active.Busy; t += 0.25f) yield return new WaitForSecondsRealtime(0.25f);
                yield return new WaitForSecondsRealtime(3f); // máy lướt lên Nhà chính, rig dựng dần mỗi khung một con
                if (!home)
                {
                    Debug.LogWarning("[Thử] Không vào được màn Nhà");
                    yield break;
                }
                DayCycle.Override = 12f;
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot("1_toan_12h");
                DayCycle.Override = 21f;
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot("2_toan_21h");
                Log("toàn màn");

                // tới gần một tướng đang rảnh (đi lại) trong khung
                var pets = Object.FindObjectsByType<FarmPet>(FindObjectsSortMode.None);
                // con đứng trước công trình (làm / hết sức) thường thoáng hơn con đi lang thang sát mép rừng
                var pet = pets.FirstOrDefault(p => p.State == FarmPet.Mode.Work || p.State == FarmPet.Mode.Tired)
                          ?? pets.FirstOrDefault(p => p.State == FarmPet.Mode.Roam || p.State == FarmPet.Mode.Walk) ?? pets.FirstOrDefault();
                var view = Object.FindAnyObjectByType<LandView>();
                if (pet && view)
                {
                    var vr = (RectTransform)view.transform;
                    var cam = vr.GetComponentInParent<Canvas>()?.rootCanvas.worldCamera;
                    var center = RectTransformUtility.WorldToScreenPoint(cam, vr.TransformPoint(vr.rect.center));
                    RectTransformUtility.ScreenPointToWorldPointInRectangle(vr, center, cam, out var cw);
                    view.ShiftWorld(cw - pet.transform.position);
                    yield return new WaitForSecondsRealtime(1.2f);
                    yield return Shot("3_gan_21h_a", 2);
                    yield return new WaitForSecondsRealtime(0.4f);
                    yield return Shot("3_gan_21h_b", 2);
                    DayCycle.Override = 12f;
                    yield return new WaitForSecondsRealtime(0.8f);
                    yield return Shot("4_gan_12h", 2);
                    Log("gần " + pet.Hero);
                }
                Debug.Log("[Thử] Xong tướng màn Nhà: " + Path.GetFullPath(Dir));
            }
            finally
            {
                DayCycle.Override = null;
            }
        }

        static void Log(string tag)
        {
            var pets = Object.FindObjectsByType<FarmPet>(FindObjectsSortMode.None);
            int rig = pets.Count(p => p.GetComponentsInChildren<RawImage>(false).Any(r => r.texture is RenderTexture));
            Debug.Log($"[Thử] Nhà ({tag}): {pets.Length} tướng, {rig} đang hiện rig, trạng thái: " +
                      string.Join(", ", pets.GroupBy(p => p.State).Select(g => $"{g.Key} {g.Count()}")));
        }

        // k > 1: camera chính vẽ vào ảnh lớn gấp k (chỉ lớp World Space)
        static IEnumerator Shot(string name, int k = 1)
        {
            yield return new WaitForEndOfFrame();
            Texture2D tex;
            var cam = Camera.main;
            if (k <= 1 || !cam) tex = ScreenCapture.CaptureScreenshotAsTexture();
            else
            {
                int w = Screen.width * k, h = Screen.height * k;
                var rt = RenderTexture.GetTemporary(w, h, 24);
                var prev = cam.targetTexture;
                cam.targetTexture = rt;
                cam.Render();
                cam.targetTexture = prev;
                var act = RenderTexture.active;
                RenderTexture.active = rt;
                tex = new Texture2D(w, h, TextureFormat.RGB24, false);
                tex.ReadPixels(new Rect(0, 0, w, h), 0, 0);
                tex.Apply();
                RenderTexture.active = act;
                RenderTexture.ReleaseTemporary(rt);
            }
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(85));
            Object.DestroyImmediate(tex);
        }
    }
}
