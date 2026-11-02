// Quảng cáo thưởng và gói so với bản web (golden ads.json): giới hạn mỗi chỗ, qua ngày, lùi ngày không mở lại lượt;
// Thẻ Phiêu Lưu (cây bi ×1,5, khay 5 ô, rương mở 1 giờ, cộng dồn hạn, hết hạn về số gốc); Bỏ quảng cáo mua một lần;
// bước di chuyển bản lưu v2 -> v3; rà danh sách gói: không có gói nào cho bi, đá tiềm năng hay lượt quay máy bi.
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class AdsTests
    {
        static Dictionary<string, object> Golden() => J.Obj(MiniJson.Parse(TestData.Read("Golden/ads.json")));

        [Test]
        public void GioiHanMoiNgay_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            int i = 0;
            foreach (var x in J.Arr(Golden(), "steps"))
            {
                var o = J.Obj(x);
                int day = J.Int(o, "day");
                string p = J.Str(o, "p"), at = $"bước {i++} ({p}, ngày {day})";
                Assert.AreEqual(J.Bool(o, "r"), AdGate.Use(s, d.Cfg, day, p), at);
                Assert.AreEqual(J.Int(o, "left"), AdGate.Left(s, d.Cfg, day, p), at + " lượt còn");
                var w = J.Obj(o, "state");
                Assert.AreEqual(J.Int(w, "day"), s.ads.day, at + " ngày");
                var wu = J.Obj(w, "used");
                Assert.AreEqual(wu.Count, s.ads.used.Count, at + " số chỗ");
                foreach (var kv in wu) Assert.AreEqual((int)(double)kv.Value, s.ads.used[kv.Key], at + " " + kv.Key);
            }
        }

        [Test]
        public void GioiHan_TheoSpec()
        {
            var d = TestData.Load();
            var want = new Dictionary<string, int> { [AdGate.TreeDouble] = 3, [AdGate.AfkChestOpen] = 4, [AdGate.AfkBoost] = 3, [AdGate.FarmBoost] = 3, [AdGate.CaveExtra] = 1 };
            foreach (var kv in want)
            {
                var s = SaveData.New(d, 0);
                for (int k = 0; k < kv.Value; k++) Assert.IsTrue(AdGate.Use(s, d.Cfg, 100, kv.Key), kv.Key + " lượt " + (k + 1));
                Assert.IsFalse(AdGate.Use(s, d.Cfg, 100, kv.Key), kv.Key + ": hết lượt");
                Assert.AreEqual(0, AdGate.Left(s, d.Cfg, 100, kv.Key));
                Assert.AreEqual(0, AdGate.Left(s, d.Cfg, 99, kv.Key), kv.Key + ": lùi giờ máy về hôm qua không mở lại lượt");
                Assert.AreEqual(kv.Value, AdGate.Left(s, d.Cfg, 101, kv.Key), kv.Key + ": qua ngày mới đếm lại từ 0");
            }
            // Bỏ quảng cáo không bỏ giới hạn ngày
            var n = SaveData.New(d, 0);
            AdGate.Buy(n, d.Cfg, "no_ads", 0);
            for (int k = 0; k < 3; k++) AdGate.Use(n, d.Cfg, 5, AdGate.AfkBoost);
            Assert.IsFalse(AdGate.Use(n, d.Cfg, 5, AdGate.AfkBoost), "đã mua Bỏ quảng cáo vẫn theo giới hạn mỗi ngày");
        }

        [Test]
        public void TheoPhieuLuu_KhopBanWeb()
        {
            var d = TestData.Load();
            var g = Golden();
            double t0 = J.Num(g, "t0");
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Thuy] = 8;
            s.afk.lastTick = t0;
            var steps = J.Arr(g, "pass").Select(J.Obj).ToList();
            double t15 = t0 + 15 * 3600000.0;

            void Snap(Dictionary<string, object> w, double t, string at)
            {
                Assert.AreEqual(J.Int(w, "stock"), Trees.Stock(s, d.Cfg, t), at + " bi trên cây");
                Assert.AreEqual(J.Num(w, "cap"), Trees.Cap(s, d.Cfg, t), at + " sức chứa cây");
                var wtr = J.Arr(w, "trees");
                Assert.AreEqual(wtr.Count, s.trees.stock.Count, at + " số cây");
                for (int k = 0; k < wtr.Count; k++) Assert.AreEqual((double)wtr[k], s.trees.stock[k], 1e-9, at + " cây " + k);
                Assert.AreEqual(J.Int(w, "slots"), Afk.Slots(s, d.Cfg, t), at + " số ô");
                Assert.AreEqual(J.Bool(w, "pass"), AdGate.PassActive(s, t), at + " còn thẻ");
                Assert.AreEqual(J.Num(w, "hours"), s.afk.hours, at + " giờ");
                Assert.AreEqual(J.Int(w, "balls"), s.balls, at + " bi");
                var wc = J.Arr(w, "chests");
                Assert.AreEqual(wc.Count, s.afk.chests.Count, at + " số rương");
                for (int k = 0; k < wc.Count; k++) Assert.AreEqual((double)wc[k], s.afk.chests[k], at + " rương " + k);
                var times = Afk.ChestTimes(s, d.Cfg, t);
                var wt = J.Arr(w, "times");
                Assert.AreEqual(wt.Count, times.Count, at + " số giờ mở");
                for (int k = 0; k < wt.Count; k++)
                {
                    Assert.AreEqual(J.Num(J.Obj(wt[k]), "start"), times[k].start, at + " bắt đầu " + k);
                    Assert.AreEqual(J.Num(J.Obj(wt[k]), "ready"), times[k].ready, at + " mở được " + k);
                }
            }

            void Pending(Dictionary<string, object> w, double t, string at)
            {
                var p = Afk.Pending(s, d.Cfg, t);
                var wr = J.Obj(w, "r");
                Assert.AreEqual(J.Num(wr, "hours"), p.hours, at);
                Assert.AreEqual(J.Bool(wr, "full"), p.full, at);
            }

            Snap(steps[0], t0, "bắt đầu");
            Assert.AreEqual(J.Bool(steps[1], "r"), AdGate.Buy(s, d.Cfg, "adventure_pass", t0));
            Assert.AreEqual(J.Num(steps[1], "until"), s.ent.passUntil, "hạn thẻ");
            Snap(steps[1], t0, "mua thẻ");
            Assert.AreEqual(J.Bool(steps[2], "r"), AdGate.Buy(s, d.Cfg, "adventure_pass", t0 + 1000));
            Assert.AreEqual(J.Num(steps[2], "until"), s.ent.passUntil, "gia hạn cộng dồn");
            Snap(steps[2], t0 + 1000, "gia hạn");
            Pending(steps[3], t15, "AFK có thẻ");
            Snap(steps[3], t15, "15 giờ sau");
            Assert.AreEqual(J.Int(steps[4], "r"), Trees.Harvest(s, d.Cfg, t15), "hái cây có thẻ (×1,5 tốc độ và sức chứa)");
            Snap(steps[4], t15, "đã hái");
            var wn = J.Arr(steps[5], "r");
            Assert.AreEqual((bool)wn[0], AdGate.Buy(s, d.Cfg, "no_ads", t15), "mua Bỏ quảng cáo");
            Assert.AreEqual((bool)wn[1], AdGate.Buy(s, d.Cfg, "no_ads", t15), "mua lại Bỏ quảng cáo");
            Assert.AreEqual(J.Bool(steps[5], "noAds"), AdGate.NoAds(s));
            Snap(steps[5], t15, "bỏ quảng cáo");
            double tEnd = s.ent.passUntil + 3600000;
            Pending(steps[6], tEnd, "hết hạn thẻ");
            Snap(steps[6], tEnd, "hết hạn thẻ");
        }

        [Test]
        public void QuyenLoi_LuuVaDocLai()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            AdGate.Use(s, d.Cfg, 20500, AdGate.AfkBoost);
            AdGate.Use(s, d.Cfg, 20500, AdGate.CaveExtra);
            AdGate.Buy(s, d.Cfg, "adventure_pass", 1_900_000_000_000);
            AdGate.Buy(s, d.Cfg, "no_ads", 0);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var r));
            Assert.AreEqual(20500, r.ads.day);
            Assert.AreEqual(1, r.ads.used[AdGate.AfkBoost]);
            Assert.AreEqual(1, r.ads.used[AdGate.CaveExtra]);
            Assert.AreEqual(s.ent.passUntil, r.ent.passUntil);
            Assert.IsTrue(r.ent.noAds);
        }

        [Test]
        public void DiChuyenBanLuuV2_KhopBanWeb()
        {
            foreach (var x in J.Arr(Golden(), "migrate"))
            {
                var o = J.Obj(x);
                var tree = J.Obj(MiniJson.Parse(MiniJson.Write(J.Obj(o, "in"))));
                SaveCodec.MigrateAdsV2(tree);
                Assert.AreEqual(MiniJson.Write(J.Obj(o, "out")), MiniJson.Write(tree));
            }
        }

        [Test]
        public void DiChuyenBanLuuV2_DocDuoc()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            var json = SaveCodec.Write(s).Replace($"\"v\":{d.Cfg.saveVersion}", "\"v\":2")
                .Replace("\"afk\":{", "\"afk\":{\"adDay\":20500,\"adOpen\":2,\"adBoost\":1,");
            Assert.AreEqual(LoadStatus.Migrated, SaveCodec.Read(json, d, out var r), json);
            Assert.AreEqual(d.Cfg.saveVersion, r.v, "v2 lên tới bản hiện tại qua mọi bước");
            Assert.AreEqual(2, AdGate.Used(r, 20500, AdGate.AfkChestOpen));
            Assert.AreEqual(1, AdGate.Used(r, 20500, AdGate.AfkBoost));
        }

        [Test]
        public void DanhSachGoi_KhongBanBiDaLuotQuay()
        {
            var d = TestData.Load();
            CollectionAssert.AreEquivalent(new[] { "adventure_pass", "no_ads" }, d.Cfg.ads.products.Select(p => p.id).ToArray(), "chỉ có 2 gói khởi điểm");
            foreach (var p in d.Cfg.ads.products)
            {
                var s = SaveData.New(d, 0);
                s.zones[(int)Elem.Thuy] = 8;
                int balls = s.balls, stones = s.potentialStones, chests = s.chests.Count, afkChests = s.afk.chests.Count;
                Assert.IsTrue(AdGate.Buy(s, d.Cfg, p.id, 0), p.id);
                Assert.AreEqual(balls, s.balls, p.id + ": không cho bi");
                Assert.AreEqual(stones, s.potentialStones, p.id + ": không cho đá tiềm năng");
                Assert.AreEqual(chests, s.chests.Count, p.id + ": không cho lượt quay / rương máy bi");
                Assert.AreEqual(afkChests, s.afk.chests.Count, p.id + ": không cho rương");
                // mô tả không hứa một lượng bi / đá đem bán, không nhắc lượt quay (tăng tốc cây bi là quyền lợi, không phải bán bi)
                string text = (p.name + " " + p.desc).ToLowerInvariant();
                StringAssert.DoesNotMatch(@"\d[\d.,]*\s*(bi|đá)", text, p.id + " mô tả");
                StringAssert.DoesNotContain("lượt quay", text, p.id + " mô tả");
                StringAssert.DoesNotContain("đá tiềm năng", text, p.id + " mô tả");
            }
        }
    }
}
