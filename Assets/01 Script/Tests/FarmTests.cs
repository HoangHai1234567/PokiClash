// Trang trại so với bản web (golden farm.json): công thức năng suất / thời lượng / nghỉ, rồi chạy lại từng bước (đặt, rút, nghỉ, tự xếp,
// tăng tốc, thu hoạch, lùi giờ, tua) và so cả trạng thái sau mỗi bước. Thêm: ví dụ trong design, kho 12 giờ, lưu rồi đọc lại.
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
            var s = SaveData.New(d, 0);
            foreach (var id in new[] { "vo_su", "nu_hoa", "ca_ngua", "bo_de" }) s.Hero(id).owned = true;
            s.level = 9;
            s.Hero("ca_ngua").star = 3;
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
            s.Hero("tieu_y").owned = true; // ví dụ tính tay theo Tiểu Y (Thường); tướng khởi đầu giờ là Giọt Sương
            s.level = 5;
            Assert.AreEqual(2.5, Farm.Rate(s, d, "tieu_y", 0), 1e-9, "Tiểu Y 1 sao ở Ao vịt (hợp hệ): 2 × 1,25 = 2,5 bi/giờ, không tăng theo cấp");
            s.level = 20;
            Assert.AreEqual(2.5, Farm.Rate(s, d, "tieu_y", 0), 1e-9, "cấp 20 vẫn 2,5");
            s.level = 5;
            Assert.AreEqual(8, Farm.Hours(s, d, "tieu_y"), "ca 8 giờ ở 1 sao");
            s.Hero("tieu_y").star = 3;
            Assert.AreEqual(10, Farm.Hours(s, d, "tieu_y"), "+1 giờ mỗi sao");
            s.Hero("tieu_y").star = 1;
            Assert.AreEqual(60, Farm.RestMin(s, d, "tieu_y"), "8 giờ × 15 phút, chặn ở 60");
            Assert.IsFalse(Farm.Open(s, d.Cfg), "1 tướng chưa mở");
            foreach (var id in new[] { "vo_su", "nu_hoa" }) s.Hero(id).owned = true;
            Assert.IsTrue(Farm.Open(s, d.Cfg));
            s.level = 9;
            Assert.AreEqual(4, Farm.SpotsOpen(d.Cfg, 9), "cấp 9: 4 chỗ");
            Assert.AreEqual(11, Farm.SpotLevel(d.Cfg, 4), "chỗ thứ 5 mở ở cấp 11");
            Assert.IsTrue(Farm.Place(s, d, 0, 0, "tieu_y"));
            // tướng hết sức sau 8 giờ: vắng 12 giờ vẫn chỉ có năng suất × 8
            Farm.Tick(s, d, 12 * H);
            Assert.AreEqual(Farm.Rate(s, d, "tieu_y", 0) * 8, s.farm.spots[0].stock, 1e-9);
            Assert.IsFalse(Farm.Place(s, d, 12 * H, 1, "tieu_y"), "đang làm ở chỗ khác");
            Assert.IsTrue(Farm.Remove(s, d, 12 * H, 0));
            Assert.IsFalse(Farm.Place(s, d, 12 * H + 30 * 60000, 1, "tieu_y"), "đang nghỉ");
            Assert.IsTrue(Farm.Place(s, d, 12 * H + 61 * 60000, 1, "tieu_y"), "nghỉ đủ 60 phút");
            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var back));
            Assert.AreEqual("tieu_y", back.farm.spots[1].hero);
            Assert.AreEqual(s.farm.spots[0].stock, back.farm.spots[0].stock);
            Assert.AreEqual(s.farm.lastTick, back.farm.lastTick);
        }
    }
}
