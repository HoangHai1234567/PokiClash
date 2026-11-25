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
            // golden chụp ở bản web với cây 5 bi mỗi giờ, chứa 50, cây sau ở cấp 30/50/80/110: chạy cơ chế trên đúng số đó
            // (balance.json đổi số 2026-11-24), xong trả lại
            var keep = d.Cfg.trees;
            d.Cfg.trees = new TreesConfig { perHour = 5, cap = 50, unlockLevels = new System.Collections.Generic.List<int> { 30, 50, 80, 110 } };
            try
            {
                Replay(d);
            }
            finally
            {
                d.Cfg.trees = keep;
            }
        }

        static void Replay(GameData d)
        {
            var g = J.Obj(MiniJson.Parse(TestData.Read("Golden/trees.json")));
            double t0 = J.Num(g, "t0");
            var s = SaveData.New(d, 0);
            OpenHome(s, d); // cây bi mở cùng Nhà (2026-11-23); bản web chưa có Nhà
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
                        else s.zones[(int)Keys.ToElem((string)arg)] = Islands.Size(Keys.ToElem((string)arg));
                        break;
                    case "level": s.level = (int)(double)arg; break; // cây 2–5 mở theo cấp người chơi (đảo song song, 2026-11-05)
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
            OpenHome(s, d);
            Assert.AreEqual(0, Trees.Open(s, d.Cfg), "chưa qua ải nào: chưa có cây");
            s.zones[(int)Elem.Thuy] = 1;
            s.level = d.Cfg.trees.unlockLevels[1];
            Assert.AreEqual(3, Trees.Open(s, d.Cfg), "qua ải 1, đủ cấp mở cây 3: 3 cây");
            // số theo balance.json (2026-11-24: 4 bi mỗi giờ, chứa đủ 24 giờ)
            double rate = d.Cfg.trees.perHour, cap = d.Cfg.trees.cap, full = cap / rate;
            Assert.Less(5 * rate, cap, "5 giờ chưa đầy");
            Trees.Tick(s, d.Cfg, 0);
            Assert.AreEqual(3 * (int)(5 * rate), Trees.Stock(s, d.Cfg, 5 * H), "5 giờ: 5 lần tốc độ mỗi cây");
            Assert.AreEqual(3 * (int)cap, Trees.Stock(s, d.Cfg, full * H), "đủ giờ: đầy");
            Assert.AreEqual(3 * (int)cap, Trees.Stock(s, d.Cfg, (full + 20) * H), "đầy thì ngừng");
            Assert.IsTrue(Trees.Full(s, d.Cfg, (full + 20) * H));
            Assert.IsFalse(Trees.Tick(s, d.Cfg, (full + 10) * H), "lùi giờ máy");
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var back));
            Assert.AreEqual(s.trees.lastTick, back.trees.lastTick);
            CollectionAssert.AreEqual(s.trees.stock, back.trees.stock);
            Assert.AreEqual(3 * (int)cap, Trees.Harvest(back, d.Cfg, (full + 10) * H));
            Assert.AreEqual(0, Trees.Stock(back, d.Cfg, (full + 10) * H));
        }

        [Test]
        public void CayBi_MoCungNha()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Thuy] = 1;
            Assert.AreEqual(0, Trees.Open(s, d.Cfg), "qua ải 1 mà chưa mở Nhà: chưa có cây (cây bi ở trong Nhà)");
            OpenHome(s, d);
            Assert.AreEqual(1, Trees.Open(s, d.Cfg), "mở Nhà: có cây đầu");
        }

        // cây bi mở cùng Nhà (2026-11-23): cho bản lưu đủ tướng để mở Nhà (Farm.Open)
        internal static void OpenHome(SaveData s, GameData d)
        {
            foreach (var h in d.Heroes)
            {
                if (Home.Open(s, d.Cfg)) break;
                s.Hero(h.id).owned = true;
            }
        }
    }
}
