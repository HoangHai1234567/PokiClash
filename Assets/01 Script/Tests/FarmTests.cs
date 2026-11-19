// Trang trại so với bản web (golden farm.json): công thức năng suất / thời lượng / nghỉ, rồi chạy lại từng bước (đặt, rút, nghỉ, tự xếp,
// tăng tốc, thu hoạch, lùi giờ, tua) và so cả trạng thái sau mỗi bước. Thêm: ví dụ trong design, kho 12 giờ, lưu rồi đọc lại.
// farm.json (Võ Sư lên Khá): tính lại bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md).
// 2026-11-16: bỏ 31 tướng cũ không còn suất đảo, tướng mẫu đổi sang tướng thay cùng hệ (SaveCodec.BoTuongCu); golden tính lại bằng
// menu "PokiClash/Thử/Tính lại golden theo tướng mẫu của test" (GoldenFixtureMenu).
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class FarmTests
    {
        const double H = 3600000;

        static SaveData Setup(GameData d)
        {
            var s = SaveData.New(d, 0, TestData.OldStarter); // bản lưu mẫu của golden (TestData.OldStarter)
            foreach (var id in new[] { "cao_da", "tien_la", "so_ngoc", "nguu_quyen" }) s.Hero(id).owned = true;
            s.level = 9;
            s.Hero("so_ngoc").star = 6; // Bạc 1★ = 3 sao cũ (trang trại tính theo sao cũ, StarTier.Legacy; golden giữ nguyên)
            return s;
        }

        [Test]
        public void CongThuc_VaTungBuoc_KhopBanWeb()
        {
            var d = TestData.Load();
            var g = J.Obj(MiniJson.Parse(TestData.Read("Golden/farm.json")));
            var s = Setup(d);
            double t0 = J.Num(g, "t0");
            Assert.AreEqual(J.Int(g, "open"), Farm.SpotsOpen(d.Cfg, s.level));
            foreach (var x in J.Arr(g, "formula"))
            {
                var o = J.Obj(x);
                string h = J.Str(o, "hero");
                Assert.AreEqual(J.Num(o, "hours"), Farm.Hours(s, d, h), h + " giờ làm");
                Assert.AreEqual(J.Num(o, "rest"), Farm.RestMin(s, d, h), h + " phút nghỉ");
                var rates = J.Arr(o, "rates");
                for (int i = 0; i < rates.Count; i++) Assert.AreEqual((double)rates[i], Farm.Rate(s, d, h, i), $"{h} chỗ {i}");
            }
            int k = 0;
            foreach (var x in J.Arr(g, "steps"))
            {
                var o = J.Obj(x);
                string op = J.Str(o, "op"), at = $"bước {k++} ({op})";
                double now = t0 + J.Num(o, "t") * H;
                var a = J.Get(o, "a");
                var want = J.Get(o, "r");
                switch (op)
                {
                    case "tick": Assert.AreEqual(want, Farm.Tick(s, d, now), at); break;
                    case "place": Assert.AreEqual(want, Farm.Place(s, d, now, (int)(double)a, J.Str(o, "b")), at); break;
                    case "remove": Assert.AreEqual(want, Farm.Remove(s, d, now, (int)(double)a), at); break;
                    case "harvest": Assert.AreEqual((double)want, Farm.Harvest(s, d, now), at); break;
                    case "boost": Assert.AreEqual(want, Farm.Boost(s, d, now), at); break;
                    case "travel": Farm.Travel(s, (double)a * H); break;
                    case "auto":
                    {
                        var got = Farm.Auto(s, d, now);
                        var w = J.Arr(want);
                        Assert.AreEqual(w.Count, got.Count, at);
                        for (int i = 0; i < w.Count; i++)
                        {
                            var e = J.Arr(w[i]);
                            Assert.AreEqual((double)e[0], got[i].spot, at);
                            Assert.AreEqual((string)e[1], got[i].hero, at);
                        }
                        break;
                    }
                }
                var wf = J.Obj(o, "farm");
                var f = s.farm;
                Assert.AreEqual(J.Num(wf, "lastTick"), f.lastTick, at + " lastTick");
                Assert.AreEqual(J.Num(wf, "boostUntil"), f.boostUntil, at + " boostUntil");
                var ws = J.Arr(wf, "spots");
                for (int i = 0; i < ws.Count; i++)
                {
                    var sp = J.Obj(ws[i]);
                    Assert.AreEqual(J.Str(sp, "hero"), f.spots[i].hero, $"{at} chỗ {i} tướng");
                    Assert.AreEqual(J.Num(sp, "energy"), f.spots[i].energy, $"{at} chỗ {i} sức");
                    Assert.AreEqual(J.Num(sp, "stock"), f.spots[i].stock, $"{at} chỗ {i} bi");
                }
                var wr = J.Obj(wf, "rest");
                Assert.AreEqual(wr.Count, f.rest.Count, at + " số tướng nghỉ");
                foreach (var kv in wr) Assert.AreEqual((double)kv.Value, f.rest[kv.Key], at + " nghỉ " + kv.Key);
                Assert.AreEqual(J.Int(o, "balls"), s.balls, at + " bi");
            }
        }

        [Test]
        public void ViDu_CaDai_LuuDocLai()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.Hero("thach_giai").owned = true; // ví dụ tính tay theo một tướng Thủy Thường (Thạch Giải; trước là Tiểu Y, bỏ 2026-11-16)
            s.level = 5;
            Assert.AreEqual(2.5, Farm.Rate(s, d, "thach_giai", 0), 1e-9, "Thạch Giải 1 sao ở Ao vịt (hợp hệ): 2 × 1,25 = 2,5 bi/giờ, không tăng theo cấp");
            s.level = 20;
            Assert.AreEqual(2.5, Farm.Rate(s, d, "thach_giai", 0), 1e-9, "cấp 20 vẫn 2,5");
            s.level = 5;
            Assert.AreEqual(8, Farm.Hours(s, d, "thach_giai"), "ca 8 giờ ở 1 sao");
            s.Hero("thach_giai").star = 6; // Bạc 1★ = 3 sao cũ (StarTier.Legacy)
            Assert.AreEqual(10, Farm.Hours(s, d, "thach_giai"), "+1 giờ mỗi sao cũ");
            s.Hero("thach_giai").star = 1;
            Assert.AreEqual(60, Farm.RestMin(s, d, "thach_giai"), "8 giờ × 15 phút, chặn ở 60");
            Assert.IsFalse(Farm.Open(s, d.Cfg), "1 tướng chưa mở");
            foreach (var id in new[] { "cao_da", "tien_la" }) s.Hero(id).owned = true;
            Assert.IsTrue(Farm.Open(s, d.Cfg));
            s.level = 40;
            Assert.AreEqual(4, Farm.SpotsOpen(d.Cfg, 40), "cấp 40: 4 chỗ");
            Assert.AreEqual(70, Farm.SpotLevel(d.Cfg, 4), "chỗ thứ 5 mở ở cấp 70");
            Assert.IsTrue(Farm.Place(s, d, 0, 0, "thach_giai"));
            // tướng hết sức sau 8 giờ: vắng 12 giờ vẫn chỉ có năng suất × 8
            Farm.Tick(s, d, 12 * H);
            Assert.AreEqual(Farm.Rate(s, d, "thach_giai", 0) * 8, s.farm.spots[0].stock, 1e-9);
            Assert.IsFalse(Farm.Place(s, d, 12 * H, 1, "thach_giai"), "đang làm ở chỗ khác");
            Assert.IsTrue(Farm.Remove(s, d, 12 * H, 0));
            Assert.IsFalse(Farm.Place(s, d, 12 * H + 30 * 60000, 1, "thach_giai"), "đang nghỉ");
            Assert.IsTrue(Farm.Place(s, d, 12 * H + 61 * 60000, 1, "thach_giai"), "nghỉ đủ 60 phút");
            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var back));
            Assert.AreEqual("thach_giai", back.farm.spots[1].hero);
            Assert.AreEqual(s.farm.spots[0].stock, back.farm.spots[0].stock);
            Assert.AreEqual(s.farm.lastTick, back.farm.lastTick);
        }
    }
}
