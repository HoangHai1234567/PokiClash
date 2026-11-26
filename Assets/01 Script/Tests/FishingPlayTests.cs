// Bến câu kiểu Clash of Critters (Core/Casino/Fishing.cs, người dùng dặn 2026-11-26): hạng cân theo cỡ, số nhịp theo độ hiếm và hạng cân,
// Cá Vua tối đa nhịp; phân bố hạng cân của cỡ ngẫu nhiên gần 56 / 24 / 14 / 6 %.
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class FishingPlayTests
    {
        static GameData D => TestData.Load();
        static FishingConfig C => D.Cfg.casino.fishing;

        [Test]
        public void HangCan_TheoCo()
        {
            var f = new FishDef { min = 10, max = 20 };
            Assert.AreEqual(0, Fishing.SizeClass(f, 10));
            Assert.AreEqual(0, Fishing.SizeClass(f, 13.9));
            Assert.AreEqual(1, Fishing.SizeClass(f, 14));
            Assert.AreEqual(2, Fishing.SizeClass(f, 17));
            Assert.AreEqual(3, Fishing.SizeClass(f, 19));
            Assert.AreEqual(3, Fishing.SizeClass(f, 20));
            Assert.AreEqual(0, Fishing.SizeClass(new FishDef { min = 5, max = 5 }, 5), "khoảng cỡ rỗng");
        }

        [Test]
        public void SoNhip_TheoDoHiem_VaHangCan()
        {
            foreach (var f in C.fish)
            {
                int small = Fishing.Ticks(new FishBite { fish = f, size = f.min });
                int big = Fishing.Ticks(new FishBite { fish = f, size = f.max });
                Assert.AreEqual(System.Math.Min(Fishing.MaxTicks, 2 * (int)f.rar), small, f.id);
                Assert.AreEqual(System.Math.Min(Fishing.MaxTicks, 2 * (int)f.rar + 1), big, f.id);
            }
            var common = C.fish.First(f => f.rar == Rarity.Common);
            Assert.AreEqual(0, Fishing.Ticks(new FishBite { fish = common, size = common.min }), "cá nhỏ: chạm một lần");
            var king = C.kings[0];
            Assert.AreEqual(Fishing.MaxTicks, Fishing.Ticks(new FishBite { fish = king, size = king.min, king = true }));
            Assert.AreEqual(0, Fishing.Ticks(null));
        }

        [Test]
        public void HangCan_PhanBo()
        {
            var f = new FishDef { min = 10, max = 30 };
            var rng = new Rng(11);
            var n = new int[4];
            const int N = 20000;
            for (int i = 0; i < N; i++) n[Fishing.SizeClass(f, Fishing.Size(f, rng))]++;
            double[] want = { 0.56, 0.24, 0.14, 0.06 };
            for (int k = 0; k < 4; k++) Assert.AreEqual(want[k], n[k] / (double)N, 0.03, "hạng " + k);
        }
    }
}
