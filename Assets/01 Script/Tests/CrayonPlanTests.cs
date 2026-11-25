// Kế hoạch bút chì màu của màn mở khoá tướng (Core/CrayonPlan): hình hai màu viền mực ra hai nhóm màu đúng màu, nét mực không thành
// nhóm; đường các bút tô kín mọi điểm của nhóm mình; ảnh rỗng ra null; vệt sáp chỉ ghi vào kênh của nhóm.
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class CrayonPlanTests
    {
        const int W = 160, H = 100;

        // nửa trái đỏ, nửa phải xanh, viền mực nâu sẫm dày 2 điểm quanh và giữa; ngoài hình trong suốt
        static byte[] TwoTone(out bool[] red, out bool[] blue)
        {
            var a = new byte[W * H * 4];
            red = new bool[W * H];
            blue = new bool[W * H];
            for (int y = 10; y < 90; y++)
            for (int x = 10; x < 150; x++)
            {
                int i = y * W + x;
                bool ink = x < 12 || x >= 148 || y < 12 || y >= 88 || (x >= 79 && x < 81);
                byte r, g, b;
                if (ink) (r, g, b) = ((byte)60, (byte)50, (byte)42);
                else if (x < 80) (r, g, b) = ((byte)225, (byte)70, (byte)55);
                else (r, g, b) = ((byte)60, (byte)130, (byte)220);
                a[i * 4] = r;
                a[i * 4 + 1] = g;
                a[i * 4 + 2] = b;
                a[i * 4 + 3] = 255;
                if (!ink && x < 80) red[i] = true;
                if (!ink && x >= 80) blue[i] = true;
            }
            return a;
        }

        [Test]
        public void HaiMau_HaiNhom_DungMau_NetMucKhongThanhNhom()
        {
            var plan = CrayonPlan.Make(TwoTone(out _, out _), W, H, false, true);
            Assert.IsNotNull(plan);
            Assert.AreEqual(2, plan.Colors.Count);
            int red = plan.Nearest(225 / 255f, 70 / 255f, 55 / 255f), blue = plan.Nearest(60 / 255f, 130 / 255f, 220 / 255f);
            Assert.AreNotEqual(red, blue);
            Assert.AreEqual(225 / 255f, plan.Colors[red][0], 0.03f);
            Assert.AreEqual(220 / 255f, plan.Colors[blue][2], 0.03f);
            Assert.LessOrEqual(plan.Pens.Count, CrayonPlan.MaxPens);
            foreach (var p in plan.Pens) Assert.Greater(p.Length, 0);
        }

        [Test]
        public void ChayHetDuong_ToKinMoiDiemCuaNhom()
        {
            var plan = CrayonPlan.Make(TwoTone(out var red, out var blue), W, H, false, true);
            int cw = (W + 1) / 2, ch = (H + 1) / 2;
            float kx = cw / (float)W, ky = ch / (float)H;
            var cov = new byte[cw * ch * 4];
            foreach (var p in plan.Pens)
            {
                int g = p.Group;
                p.Strokes(0, p.Length, plan.Brush * 0.3f, (x, y, seg) => CrayonPlan.Stamp(cov, cw, ch, g, x * kx, y * ky, plan.Brush * kx, 1));
            }
            int gr = plan.Nearest(225 / 255f, 70 / 255f, 55 / 255f), gb = plan.Nearest(60 / 255f, 130 / 255f, 220 / 255f);
            int miss = 0, total = 0;
            for (int y = 0; y < H; y++)
            for (int x = 0; x < W; x++)
            {
                int i = y * W + x;
                if (!red[i] && !blue[i]) continue;
                total++;
                int c = (y * ch / H * cw + x * cw / W) * 4 + (red[i] ? gr : gb);
                if (cov[c] < 128) miss++;
            }
            Assert.Less(miss, total * 0.01f, $"sót {miss}/{total} điểm");
        }

        [Test]
        public void AnhRong_Null()
        {
            Assert.IsNull(CrayonPlan.Make(new byte[W * H * 4], W, H, false, true));
            Assert.IsNull(CrayonPlan.Make(null, W, H, false, true));
        }

        [Test]
        public void VetSap_ChiGhiKenhCuaNhom_GiuGiaTriLonHon()
        {
            var cov = new byte[16 * 16 * 4];
            CrayonPlan.Stamp(cov, 16, 16, 2, 8, 8, 4, 1);
            Assert.AreEqual(255, cov[(8 * 16 + 8) * 4 + 2]);
            Assert.AreEqual(0, cov[(8 * 16 + 8) * 4 + 0]);
            Assert.AreEqual(0, cov[(0 * 16 + 0) * 4 + 2]); // ngoài bán kính
            CrayonPlan.Stamp(cov, 16, 16, 2, 8, 8, 4, 0.3f);
            Assert.AreEqual(255, cov[(8 * 16 + 8) * 4 + 2]);
        }
    }
}
