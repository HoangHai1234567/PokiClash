// Cây bi so với bản web (golden trees.json): mở theo tiến độ, ra đều, đầy thì ngừng, hái giữ phần lẻ, hái ×2, lùi giờ máy,
// tua, Thẻ Phiêu Lưu (×1,5 tốc độ và sức chứa); thêm các tình huống ví dụ và lưu rồi đọc lại.
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class TreesTests
    {
        const double H = 3600000;

        [Test]
        public void ChayLaiTungBuoc_KhopBanWeb()
        {
            var d = TestData.Load();
            var g = J.Obj(MiniJson.Parse(TestData.Read("Golden/trees.json")));
            double t0 = J.Num(g, "t0");
            var s = SaveData.New(d, 0);
            int i = 0;
            foreach (var x in J.Arr(g, "steps"))
            {
                var o = J.Obj(x);
                string op = J.Str(o, "op"), at = $"bước {i++} ({op})";
                double t = t0 + J.Num(o, "h") * H;
                var arg = J.Get(o, "arg");
                var want = J.Get(o, "r");
                switch (op)
                {
                    case "tick": Assert.AreEqual(want, Trees.Tick(s, d.Cfg, t), at); break;
                    case "stock": Assert.AreEqual((double)want, Trees.Stock(s, d.Cfg, t), at); break;
                    case "harvest": Assert.AreEqual((double)want, Trees.Harvest(s, d.Cfg, t), at); break;
                    case "harvest2": Assert.AreEqual((double)want, Trees.Harvest(s, d.Cfg, t, 2), at); break;
                    case "travel": Trees.Travel(s, (double)arg * H); break;
                    case "zone":
                        if ((string)arg == "clear1") s.zones[(int)Elem.Thuy] = 1;
                        else s.zones[(int)Keys.ToElem((string)arg)] = 8;
                        break;
                    case "pass": Assert.AreEqual(want, AdGate.Buy(s, d.Cfg, "adventure_pass", t), at); break;
                }
                Assert.AreEqual(J.Int(o, "open"), Trees.Open(s, d.Cfg), at + " số cây mở");
                Assert.AreEqual(J.Num(o, "cap"), Trees.Cap(s, d.Cfg, t), at + " sức chứa");
                Assert.AreEqual(J.Int(o, "balls"), s.balls, at + " bi");
                var wt = J.Obj(o, "trees");
                if (wt == null)
                {
                    Assert.IsNull(s.trees, at);
                    continue;
                }
                Assert.AreEqual(J.Num(wt, "lastTick"), s.trees.lastTick, at + " lastTick");
                var ws = J.Arr(wt, "stock");
                Assert.AreEqual(ws.Count, s.trees.stock.Count, at + " số cây");
                for (int k = 0; k < ws.Count; k++) Assert.AreEqual((double)ws[k], s.trees.stock[k], 1e-9, at + " cây " + k);
            }
        }

        [Test]
        public void ViDu_Day10Gio_DayThiNgung_LuuDocLai()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            Assert.AreEqual(0, Trees.Open(s, d.Cfg), "chưa qua ải nào: chưa có cây");
            s.zones[(int)Elem.Thuy] = 8;
            s.zones[(int)Elem.Hoa] = 8;
            Assert.AreEqual(3, Trees.Open(s, d.Cfg), "qua ải 1, boss Thủy, boss Hỏa: 3 cây");
            Trees.Tick(s, d.Cfg, 0);
            Assert.AreEqual(3 * 25, Trees.Stock(s, d.Cfg, 5 * H), "5 giờ: 25 bi mỗi cây");
            Assert.AreEqual(3 * 50, Trees.Stock(s, d.Cfg, 10 * H), "10 giờ: đầy 50");
            Assert.AreEqual(3 * 50, Trees.Stock(s, d.Cfg, 30 * H), "đầy thì ngừng");
            Assert.IsTrue(Trees.Full(s, d.Cfg, 30 * H));
            Assert.IsFalse(Trees.Tick(s, d.Cfg, 20 * H), "lùi giờ máy");
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var back));
            Assert.AreEqual(s.trees.lastTick, back.trees.lastTick);
            CollectionAssert.AreEqual(s.trees.stock, back.trees.stock);
            Assert.AreEqual(150, Trees.Harvest(back, d.Cfg, 20 * H));
            Assert.AreEqual(0, Trees.Stock(back, d.Cfg, 20 * H));
        }
    }
}
