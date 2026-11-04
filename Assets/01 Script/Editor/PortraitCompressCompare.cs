// So mức nén chân dung tướng (người dùng 2026-11-04: chân dung mờ, nhất là bóng sẫm lúc chưa có tướng). Nén thử trong bộ nhớ, không
// đụng ảnh trong project: đọc <dạng>_portrait.png, nén ASTC 8x8 / 6x6 / 4x4 (chất lượng Normal như lúc nhập), giải nén lại rồi ghi PNG
// Temp/PokiShots/nen/<dạng>_<mức>.png (512 × 512, như ảnh gốc) để ghép bảng so bên ngoài. Thêm bản mipmap nửa (256, "_m1"): chân dung
// hiện cỡ 130–250 điểm (tướng trên bệ ải, ô đội) là Unity lấy mức này, khối nén phủ gấp đôi ảnh gốc.
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class PortraitCompressCompare
    {
        static readonly string[] Forms = { "goc_16", "goc_1313", "goc_546", "thuy_7", "goc_1831", "goc_1691", "thuy_1319" };
        static readonly (string tag, TextureFormat fmt)[] Levels =
            { ("8x8", TextureFormat.ASTC_8x8), ("6x6", TextureFormat.ASTC_6x6), ("5x5", TextureFormat.ASTC_5x5), ("4x4", TextureFormat.ASTC_4x4) };

        [MenuItem("PokiClash/Thử/Chân dung: so mức nén ASTC (Temp/PokiShots/nen)", priority = 302)]
        static void Run()
        {
            var dir = Path.Combine(PlayTour.ShotDir, "nen");
            Directory.CreateDirectory(dir);
            foreach (var form in Forms)
            {
                var path = $"{AolaImport.ResDir}/{form}/{form}_portrait.png";
                if (!File.Exists(path))
                {
                    Debug.LogWarning($"[Nén] Không có {path}");
                    continue;
                }
                var src = new Texture2D(2, 2, TextureFormat.RGBA32, false);
                src.LoadImage(File.ReadAllBytes(path));
                var half = Half(src);
                foreach (var (img, suffix) in new[] { (src, ""), (half, "_m1") })
                {
                    File.WriteAllBytes(Path.Combine(dir, $"{form}_goc{suffix}.png"), img.EncodeToPNG());
                    foreach (var (tag, fmt) in Levels)
                    {
                        var t = new Texture2D(img.width, img.height, TextureFormat.RGBA32, false);
                        t.SetPixels32(img.GetPixels32());
                        t.Apply();
                        EditorUtility.CompressTexture(t, fmt, TextureCompressionQuality.Normal);
                        var back = new Texture2D(t.width, t.height, TextureFormat.RGBA32, false);
                        back.SetPixels32(t.GetPixels32()); // giải nén trên CPU
                        back.Apply();
                        File.WriteAllBytes(Path.Combine(dir, $"{form}_{tag}{suffix}.png"), back.EncodeToPNG());
                        Object.DestroyImmediate(t);
                        Object.DestroyImmediate(back);
                    }
                }
                Object.DestroyImmediate(src);
                Object.DestroyImmediate(half);
            }
            Debug.Log($"[Nén] Xong: {dir}");
        }

        // Đang Play: dựng hai cảnh (đảo Thủy mới qua 2 ải: tướng trên bệ ải chưa mở là bóng sẫm; hộp chuẩn bị ải 3 địch), thay tạm ảnh
        // mọi chân dung đang hiện bằng bản nén thử (đủ mipmap như lúc nhập, giải nén lại từng mức trên CPU nên card nào cũng vẽ được),
        // chụp từng mức vào Temp/PokiShots/nen/<cảnh>_<mức>.png, trả ảnh cũ và bản lưu cũ.
        [MenuItem("PokiClash/Thử/Chân dung: thay thử mức nén trên màn đang mở (đang Play)", priority = 303)]
        static void InGame()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunInGame());
        }

        static System.Collections.IEnumerator RunInGame()
        {
            var save = App.Save.FilePath;
            string backup = File.Exists(save) ? File.ReadAllText(save) : null;
            var s = App.Save.Data;
            App.Modals.CloseAll();
            s.zones[(int)Core.Elem.Thuy] = 2;
            App.Save.Save();
            App.Router.Go(SceneIds.Hub);
            yield return new WaitForSecondsRealtime(1.5f);
            App.Router.Go(SceneIds.Zone, Core.Elem.Thuy);
            yield return new WaitForSecondsRealtime(2f);
            yield return Capture("dao");
            var st = App.Data.Stages.First(x => x.zone == Core.Elem.Thuy && x.enemies.Count == 3);
            s.zones[(int)Core.Elem.Thuy] = st.idx;
            StagePrep.Open(st.id);
            yield return new WaitForSecondsRealtime(1f);
            yield return Capture("chuan_bi");
            App.Modals.CloseAll();
            if (backup != null)
            {
                File.WriteAllText(save, backup);
                App.Save.Load();
            }
            Debug.Log($"[Nén] Xong chụp các mức nén: {Path.Combine(PlayTour.ShotDir, "nen")}");
        }

        static System.Collections.IEnumerator Capture(string scene)
        {
            var dir = Path.Combine(PlayTour.ShotDir, "nen");
            Directory.CreateDirectory(dir);
            var bodies = new System.Collections.Generic.List<(UnityEngine.UI.Image img, Sprite orig)>();
            foreach (var p in Object.FindObjectsByType<HeroPortrait>(FindObjectsSortMode.None))
            {
                var img = p.GetComponentsInChildren<UnityEngine.UI.Image>(true).FirstOrDefault(i => i.name == "than");
                if (img && img.enabled && img.sprite) bodies.Add((img, img.sprite));
            }
            var made = new System.Collections.Generic.List<Object>();
            foreach (var (tag, fmt) in new[] { ("hien_tai", (TextureFormat)0) }.Concat(Levels).Append(("goc", TextureFormat.RGBA32)))
            {
                foreach (var (img, orig) in bodies)
                {
                    if (tag == "hien_tai")
                    {
                        img.sprite = orig;
                        continue;
                    }
                    var tex = Decoded(AssetDatabase.GetAssetPath(orig.texture), fmt);
                    var sp = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), orig.pivot / orig.rect.size, 100, 0, SpriteMeshType.FullRect);
                    made.Add(tex);
                    made.Add(sp);
                    img.sprite = sp;
                }
                yield return null;
                yield return new WaitForEndOfFrame();
                var shot = ScreenCapture.CaptureScreenshotAsTexture();
                File.WriteAllBytes(Path.Combine(dir, $"{scene}_{tag}.png"), shot.EncodeToPNG());
                Object.Destroy(shot);
            }
            foreach (var (img, orig) in bodies) img.sprite = orig;
            foreach (var o in made) Object.Destroy(o);
            Debug.Log($"[Nén] {scene}: thay {bodies.Count} chân dung");
        }

        // ảnh chân dung có mipmap; fmt khác RGBA32 thì nén ASTC rồi giải nén lại từng mức
        static Texture2D Decoded(string path, TextureFormat fmt)
        {
            var src = new Texture2D(2, 2, TextureFormat.RGBA32, true);
            src.LoadImage(File.ReadAllBytes(path));
            src.Apply(true);
            if (fmt == TextureFormat.RGBA32) return src;
            var c = new Texture2D(src.width, src.height, TextureFormat.RGBA32, true);
            for (int m = 0; m < src.mipmapCount; m++) c.SetPixels32(src.GetPixels32(m), m);
            c.Apply(false);
            EditorUtility.CompressTexture(c, fmt, TextureCompressionQuality.Normal);
            var o = new Texture2D(src.width, src.height, TextureFormat.RGBA32, true);
            for (int m = 0; m < c.mipmapCount && m < o.mipmapCount; m++) o.SetPixels32(c.GetPixels32(m), m);
            o.Apply(false);
            o.wrapMode = TextureWrapMode.Clamp;
            Object.DestroyImmediate(src);
            Object.DestroyImmediate(c);
            return o;
        }

        // mipmap nửa: trung bình 2 × 2 (màu nhân alpha trước khi cộng, như mipmap của ảnh trong suốt)
        static Texture2D Half(Texture2D src)
        {
            int w = src.width / 2, h = src.height / 2;
            var a = src.GetPixels();
            var o = new Color[w * h];
            for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
            {
                Color sum = default;
                float al = 0;
                for (int dy = 0; dy < 2; dy++)
                for (int dx = 0; dx < 2; dx++)
                {
                    var c = a[(y * 2 + dy) * src.width + x * 2 + dx];
                    sum += new Color(c.r * c.a, c.g * c.a, c.b * c.a, 0);
                    al += c.a;
                }
                o[y * w + x] = al > 0 ? new Color(sum.r / al, sum.g / al, sum.b / al, al / 4) : Color.clear;
            }
            var t = new Texture2D(w, h, TextureFormat.RGBA32, false);
            t.SetPixels(o);
            t.Apply();
            return t;
        }
    }
}
