// Thử hộp chi tiết tướng và đội hình (đang Play, 2026-11-23; người dùng: "các icon tướng bị lệch, sao dạng cuối lại chưa phải đứng cuối,
// kiểm tra cho tất cả các tướng", "lực chiến và tên bị nhỏ quá và cố dồn vào 1 ô"). Menu "PokiClash/Thử/Tướng: thanh tiến hóa mọi tướng +
// bảng tên đội hình (đang Play)": sang màn Tướng chụp đội hình; mở hộp chi tiết lần lượt mọi tướng, cắt vùng thanh tiến hóa (mốc, nút
// Tiến hóa, sao, tên bậc) thành ảnh nhỏ <stt>_<mã>.png. Ảnh vào Temp/PokiShots/thanh_tien_hoa/. Không đổi bản lưu.
using System.Collections;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HeroStripShots
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "thanh_tien_hoa");

        [MenuItem("PokiClash/Thử/Tướng/Tướng: thanh tiến hóa mọi tướng + bảng tên đội hình (đang Play)", priority = 146)]
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
            foreach (var f in Directory.GetFiles(Dir, "*.png")) File.Delete(f);
            if (App.Router.Current != SceneIds.Heroes) App.Router.Go(SceneIds.Heroes);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(2f); // tướng đội hình dựng sticker
            yield return new WaitForEndOfFrame();
            var full = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, "0_doi_hinh.png"), full.EncodeToPNG());
            Object.Destroy(full);

            var heroes = App.Data.Heroes.ToList();
            for (int i = 0; i < heroes.Count; i++)
            {
                var h = heroes[i];
                HeroDetail.Open(h.id);
                yield return new WaitForSecondsRealtime(0.45f); // hộp trượt vào, nút Tiến hóa đặt cỡ ở LateUpdate
                var strip = Object.FindAnyObjectByType<EvolutionStrip>();
                if (strip)
                {
                    yield return new WaitForEndOfFrame();
                    Crop((RectTransform)strip.transform, Path.Combine(Dir, $"{i + 1:00}_{h.id}.png"));
                }
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.25f);
            }
            Debug.Log($"[Thử] Thanh tiến hóa: {heroes.Count} tướng, ảnh ở {Path.GetFullPath(Dir)}");
        }

        // cắt vùng của rt trên màn (thêm lề trên cho chân dung mốc, lề dưới cho sao, tên bậc, dòng giá)
        static void Crop(RectTransform rt, string path)
        {
            var cam = rt.GetComponentInParent<Canvas>()?.rootCanvas.worldCamera;
            var c = new Vector3[4];
            rt.GetWorldCorners(c);
            Vector2 a = RectTransformUtility.WorldToScreenPoint(cam, c[0]), b = RectTransformUtility.WorldToScreenPoint(cam, c[2]);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            int x0 = Mathf.Clamp(Mathf.FloorToInt(Mathf.Min(a.x, b.x)) - 70, 0, tex.width - 1);
            int x1 = Mathf.Clamp(Mathf.CeilToInt(Mathf.Max(a.x, b.x)) + 70, x0 + 1, tex.width);
            int y0 = Mathf.Clamp(Mathf.FloorToInt(Mathf.Min(a.y, b.y)) - 40, 0, tex.height - 1);
            int y1 = Mathf.Clamp(Mathf.CeilToInt(Mathf.Max(a.y, b.y)) + 40, y0 + 1, tex.height);
            var crop = new Texture2D(x1 - x0, y1 - y0, TextureFormat.RGBA32, false);
            crop.SetPixels(tex.GetPixels(x0, y0, x1 - x0, y1 - y0));
            crop.Apply();
            File.WriteAllBytes(path, crop.EncodeToPNG());
            Object.Destroy(crop);
            Object.Destroy(tex);
        }
    }
}
