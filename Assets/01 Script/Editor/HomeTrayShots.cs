// Thử màn Nhà (đang Play, 2026-11-20): tướng đúng tỉ lệ theo HeroForm.size, nét rig không vỡ (PetPart lọc thu nhỏ), khay Xây có icon
// công trình. Menu "PokiClash/Thử/Nhà và side meta/Nhà: cỡ tướng + khay Xây có icon (đang Play)": sang Nhà, 12h, chụp toàn màn, kéo máy tới từng tướng
// to nhất / nhỏ nhất đang hiện rig chụp gần (1x, zoom đang có), rồi bấm Xây chụp khay. Ảnh vào Temp/PokiShots/nha_khay/. Không đổi bản lưu.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HomeTrayShots
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "nha_khay");

        [MenuItem("PokiClash/Thử/Nhà và side meta/Nhà: cỡ tướng + khay Xây có icon (đang Play)", priority = 143)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static IEnumerator Run()
        {
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*.png")) File.Delete(f);
            if (App.Router.Current != SceneIds.Home) App.Router.Go(SceneIds.Home);
            HomeScene home = null;
            for (float t = 0; t < 25 && !(home && App.Router.CurrentRoot == home); t += 0.25f)
            {
                yield return new WaitForSecondsRealtime(0.25f);
                home = Object.FindFirstObjectByType<HomeScene>();
            }
            for (float t = 0; t < 10 && PierShip.Active && PierShip.Active.Busy; t += 0.25f) yield return new WaitForSecondsRealtime(0.25f);
            yield return new WaitForSecondsRealtime(3f);
            if (!home)
            {
                Debug.LogWarning("[Thử] Không vào được màn Nhà");
                yield break;
            }
            DayCycle.Override = 12f;
            var view = Object.FindAnyObjectByType<LandView>();
            var pets = Object.FindObjectsByType<FarmPet>(FindObjectsSortMode.None);
            var sized = pets.Select(p => (p, k: (float)HeroArt.FormOf(App.Data.Hero(p.Hero)).size)).OrderBy(x => x.k).ToList();
            Debug.Log("[Thử] Nhà cỡ tướng: " + string.Join(", ", sized.Select(x => $"{x.p.Hero} {x.k:0.##} {x.p.State}")));
            yield return Shot("0_toan");
            // thứ tự vẽ quanh nhà chính (người dùng 2026-11-21: "lúc ở trên lúc ở dưới"): kéo máy về công trình lớn nhất, chụp 8 ảnh
            // cách nhau 1 giây để thấy tướng đi ngang trước / sau nhà, cây bi, ao
            var big = Object.FindObjectsByType<HomeObject>(FindObjectsSortMode.None)
                .Where(o => o.Id >= 0 && o.gameObject.activeInHierarchy)
                .OrderByDescending(o => o.Rt.sizeDelta.x * o.Rt.sizeDelta.y).FirstOrDefault();
            if (view && big)
            {
                var vr0 = (RectTransform)view.transform;
                var cam0 = vr0.GetComponentInParent<Canvas>()?.rootCanvas.worldCamera;
                var c0 = RectTransformUtility.WorldToScreenPoint(cam0, vr0.TransformPoint(vr0.rect.center));
                RectTransformUtility.ScreenPointToWorldPointInRectangle(vr0, c0, cam0, out var w0);
                var corners = new Vector3[4];
                big.Rt.GetWorldCorners(corners);
                view.ShiftWorld(w0 - (corners[0] + corners[2]) * 0.5f);
                for (int k = 0; k < 8; k++)
                {
                    yield return new WaitForSecondsRealtime(1f);
                    yield return Shot($"h_{k}");
                }
            }
            if (view && sized.Count > 0)
            {
                var vr = (RectTransform)view.transform;
                var cam = vr.GetComponentInParent<Canvas>()?.rootCanvas.worldCamera;
                var picks = new[] { sized.Last().p, sized.First().p, sized[sized.Count / 2].p };
                int i = 0;
                foreach (var pet in picks.Distinct())
                {
                    var center = RectTransformUtility.WorldToScreenPoint(cam, vr.TransformPoint(vr.rect.center));
                    RectTransformUtility.ScreenPointToWorldPointInRectangle(vr, center, cam, out var cw);
                    view.ShiftWorld(cw - pet.transform.position);
                    yield return new WaitForSecondsRealtime(1.5f);
                    yield return Shot($"{++i}_gan_{pet.Hero}");
                }
            }
            var build = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None)
                .FirstOrDefault(b => b.Label && b.Label.text.Trim().ToUpperInvariant() == "XÂY");
            if (build)
            {
                build.SimulateClick();
                yield return new WaitForSecondsRealtime(1f);
                yield return Shot("9_khay_xay");
                build.SimulateClick(); // "Xong": về thường
            }
            else Debug.LogWarning("[Thử] Không thấy nút Xây");
            DayCycle.Override = null;
            Debug.Log("[Thử] Xong cỡ tướng + khay Xây: " + Path.GetFullPath(Dir));
        }
    }
}
