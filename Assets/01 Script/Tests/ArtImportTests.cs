// Bộ cắt sheet ảnh gen: lưới 4 × 4 nền trong suốt -> 16 ảnh đúng tên, đã gọt mép; tên icon trong bảng khớp dữ liệu thẻ.
using System.IO;
using System.Linq;
using NUnit.Framework;
using PokiClash.EditorTools;
using UnityEngine;

namespace PokiClash.Tests
{
    public class ArtImportTests
    {
        [Test]
        public void CatSheet4x4_Du16Anh_GotMep()
        {
            var dir = Path.Combine(Path.GetTempPath(), "pokiclash_sheet_" + System.Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(dir);
            try
            {
                const int n = 512, cell = 128;
                var tex = new Texture2D(n, n, TextureFormat.RGBA32, false);
                var px = new Color32[n * n];
                // mỗi ô một hình vuông 60 px ở giữa
                for (int y = 0; y < n; y++)
                    for (int x = 0; x < n; x++)
                    {
                        int cx = x % cell, cy = y % cell;
                        bool on = cx >= 34 && cx < 94 && cy >= 34 && cy < 94;
                        px[y * n + x] = on ? new Color32(200, 60, 40, 255) : new Color32(0, 0, 0, 0);
                    }
                tex.SetPixels32(px);
                tex.Apply();
                var file = Path.Combine(dir, "IC_Resources.png");
                File.WriteAllBytes(file, tex.EncodeToPNG());
                Object.DestroyImmediate(tex);

                int made = ArtImporter.CutSheet(file, ArtImporter.Sheets["IC_Resources"], dir);
                Assert.AreEqual(16, made);
                var ball = new Texture2D(2, 2);
                ball.LoadImage(File.ReadAllBytes(Path.Combine(dir, "icon_ball.png")));
                Assert.AreEqual(68, ball.width, "60 px + 4 px mỗi bên");
                Assert.AreEqual(68, ball.height);
                Object.DestroyImmediate(ball);
                Assert.IsTrue(File.Exists(Path.Combine(dir, "icon_pencil.png")));
            }
            finally
            {
                Directory.Delete(dir, true);
            }
        }

        [Test]
        public void TenIconTrongBangCat_PhuDuIconCuaThe()
        {
            var d = TestData.Load();
            var names = ArtImporter.Sheets.Values.Where(s => s.prefix == "icon_").SelectMany(s => s.names).ToHashSet();
            var missing = d.Pool.Concat(d.Innate).Select(c => c.icon).Distinct().Where(i => !names.Contains(i)).ToList();
            Assert.IsEmpty(missing, "icon thẻ chưa có ô trong sheet: " + string.Join(", ", missing));
        }
    }
}
