// Viền ngoài cho bút chì màn mở khoá tướng (Core/Contour): hình tròn ra một vòng sát mép, hai mảng ra hai vòng (lớn trước), vòng
// ngược chiều kim đồng hồ bắt đầu ở đỉnh, mảng vụn bị bỏ.
using System;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class ContourTests
    {
        static byte[] Discs(int w, int h, params (float x, float y, float r)[] ds)
        {
            var a = new byte[w * h];
            for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
                foreach (var d in ds)
                    if ((x + 0.5f - d.x) * (x + 0.5f - d.x) + (y + 0.5f - d.y) * (y + 0.5f - d.y) <= d.r * d.r)
                        a[y * w + x] = 255;
            return a;
        }

        static float SignedArea(float[] l)
        {
            double s = 0;
            int n = l.Length / 2;
            for (int i = 0; i < n; i++)
            {
                int j = (i + 1) % n;
                s += (double)l[2 * i] * l[2 * j + 1] - (double)l[2 * j] * l[2 * i + 1];
            }
            return (float)(s / 2);
        }

        [Test]
        public void HinhTron_MotVong_SatMep_NguocChieuKim_BatDauODinh()
        {
            var loops = Contour.Loops(Discs(128, 128, (64, 64, 40)), 128, 128);
            Assert.AreEqual(1, loops.Count);
            var l = loops[0];
            for (int i = 0; i < l.Length; i += 2)
            {
                float r = (float)Math.Sqrt((l[i] - 64) * (l[i] - 64) + (l[i + 1] - 64) * (l[i + 1] - 64));
                Assert.That(r, Is.InRange(37f, 41.5f), $"điểm {i / 2} cách tâm {r}");
            }
            Assert.Greater(SignedArea(l), 0, "vòng phải ngược chiều kim đồng hồ (y lên)");
            Assert.Greater(l[1], 64 + 36, "điểm đầu ở đỉnh hình");
            Assert.That(Math.Abs(SignedArea(l)), Is.InRange(Math.PI * 38 * 38, Math.PI * 41 * 41));
        }

        [Test]
        public void HaiManh_HaiVong_LonTruoc_BoManhVun()
        {
            var a = Discs(160, 100, (40, 50, 12), (110, 50, 30), (150, 90, 1.2f));
            var loops = Contour.Loops(a, 160, 100);
            Assert.AreEqual(2, loops.Count, "mảng vụn (vài điểm ảnh) bị bỏ");
            Assert.Greater(Math.Abs(SignedArea(loops[0])), Math.Abs(SignedArea(loops[1])));
            Assert.Greater(loops[0][0], 80, "vòng đầu là mảng lớn bên phải");
        }

        [Test]
        public void Hop_VaMatNaRong()
        {
            var a = Discs(64, 64, (20, 30, 5));
            var b = Contour.Bounds(a, 64, 64);
            Assert.NotNull(b);
            Assert.That(b[0], Is.InRange(14, 16));
            Assert.That(b[2], Is.InRange(23, 25));
            Assert.IsNull(Contour.Bounds(new byte[64 * 64], 64, 64));
            Assert.AreEqual(0, Contour.Loops(new byte[64 * 64], 64, 64).Count);
        }
    }
}
