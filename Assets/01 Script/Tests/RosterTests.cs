// 40 tướng (change expand-roster-40): dạng theo sao và bản lưu v3 -> v4 khớp bản web (Golden/roster.json, xuất bằng
// Web/scripts/export_golden.ts).
// roster.json (tướng trên nút ải 71, 95): tính lại bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md).
using System.Collections.Generic;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class RosterTests
    {
        static Dictionary<string, object> Golden() => J.Obj(MiniJson.Parse(TestData.Read("Golden/roster.json")));

        [Test]
        public void DanhSach78Tuong_Thuy13_Hoa17_Kim16_Moc15_Tho17()
        {
            // 40 tướng 8 mỗi hệ, Thủy thêm 5 (2026-11-02, kịch bản đảo Thủy), Mộc thêm 7, Hỏa thêm 8, Kim thêm 8 (2026-11-05, 10 tướng mỗi đảo), Hỏa thêm Ngưu Quyền ở ải 20, Thổ thêm 9 (2026-11-06)
            var d = TestData.Load();
            Assert.IsEmpty(d.Validate());
            Assert.AreEqual(78, d.Heroes.Count);
            for (int e = 0; e < 5; e++)
                Assert.AreEqual((Elem)e == Elem.Thuy ? 13 : (Elem)e == Elem.Hoa ? 17 : (Elem)e == Elem.Kim ? 16 : (Elem)e == Elem.Moc ? 15 : 17, d.Heroes.FindAll(h => (int)h.elem == e).Count, ((Elem)e).ToString());
            // 5 tướng khởi đầu, mỗi hệ một, theo thứ tự đảo (15_TuongKhoiDau.md)
            Assert.AreEqual(new[] { "giot_suong", "su_tu_lua", "bu_long", "nu_hoa", "thach_nhan" }, d.Starters.ToArray());
            foreach (var id in new[] { "gia_bi", "su_gia", "y_trach", "van_quan", "hac_duc" })
                Assert.IsNull(d.Hero(id), id + " đã gộp hoặc bỏ");
            // Lam Quân dòng 1831 → 1832 → 2955; hình vẽ lại trên rig aola từ 2026-11-07 (thuy_, trước là goc_)
            Assert.AreEqual(new[] { "thuy_1831", "thuy_1832", "thuy_2955" }, System.Array.ConvertAll(d.Hero("lam_quan").forms, f => f.aola));
            // Thanh Long là dòng 青龙 (214 → 215 → 1749), dòng 格非 cũ thành Long Vuốt
            Assert.AreEqual(new[] { "goc_214", "goc_215", "goc_1749" }, System.Array.ConvertAll(d.Hero("thanh_long").forms, f => f.aola));
            Assert.AreEqual(new[] { "goc_1219", "goc_1220" }, System.Array.ConvertAll(d.Hero("long_vuot").forms, f => f.aola));
            // đảo Kim (2026-11-05): boss Kim Nghê là dòng 克亚 → 克里亚斯 (2 dạng, aola không có siêu tiến hóa)
            Assert.AreEqual(new[] { "goc_1840", "goc_1841" }, System.Array.ConvertAll(d.Hero("kim_nghe").forms, f => f.aola));
        }

        [Test]
        public void DangTheoSao_KhopBanWeb()
        {
            var d = TestData.Load();
            foreach (var x in J.Arr(Golden(), "forms"))
            {
                var o = J.Obj(x);
                var h = d.Hero(J.Str(o, "id"));
                Assert.AreEqual(J.Int(o, "n"), h.forms.Length, h.id);
                var idx = J.Arr(o, "idx");
                for (int star = 1; star <= 5; star++)
                    Assert.AreEqual((int)(double)idx[star - 1], h.FormIndex(d.Cfg.formStars, star), $"{h.id} sao {star}");
            }
            // dòng 3 dạng: sao 1–2 dạng 1, sao 3–4 dạng 2, sao 5 dạng 3
            Assert.AreEqual("Vạn Quân", d.Cfg.FormOf(d.Hero("lam_quan"), 3).name);
            Assert.AreEqual("Hắc Dực Vạn Quân", d.Cfg.FormOf(d.Hero("lam_quan"), 5).name);
            Assert.AreEqual("Y Trạch", d.Cfg.FormOf(d.Hero("tieu_y"), 5).name);
        }

        // nhận tướng (tướng khởi đầu, tặng, thu phục đủ mảnh) thì ở sao 1, tức dạng thấp nhất của dòng tiến hóa
        [Test]
        public void TuongMoiNhan_ODangThapNhat()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            var r = new Rng(3);
            foreach (var id in d.Starters)
                Assert.AreEqual(0, d.Hero(id).FormIndex(d.Cfg.formStars, s.Hero(id).star), id + " khởi đầu");
            for (int i = 0; i < d.Heroes.Count; i++)
            {
                var h = d.Heroes[i];
                if (s.Hero(h.id).owned) continue;
                if (i % 2 == 0) Assert.IsTrue(Progress.AddShards(s, d, h.id, h.shards, r).unlocked, h.id + " đủ mảnh");
                else Progress.UnlockHero(s, h.id); // tặng tướng, mốc Huyền thoại máy bi
                var p = s.Hero(h.id);
                Assert.IsTrue(p.owned, h.id);
                Assert.AreEqual(1, p.star, h.id + " sao khi nhận");
                Assert.AreSame(h.forms[0], d.Cfg.FormOf(h, p.star), h.id + " dạng khi nhận");
            }
        }

        // thanh mốc tiến hóa: mốc chia đều (mốc cuối ở cuối thanh), thanh đầy khi tới dạng cuối
        [Test]
        public void ThanhTienHoa_MocCuoiOCuoiThanh()
        {
            var fs = TestData.Load().Cfg.formStars; // sao 3, sao 5
            float[] three = { 0, 0.25f, 0.5f, 0.75f, 1 }, two = { 0, 0.5f, 1, 1, 1 };
            for (int star = 1; star <= 5; star++)
            {
                Assert.AreEqual(three[star - 1], EvolutionStrip.Fill(fs, 3, star), 1e-5, $"3 dạng, sao {star}");
                Assert.AreEqual(two[star - 1], EvolutionStrip.Fill(fs, 2, star), 1e-5, $"2 dạng, sao {star}");
                Assert.AreEqual(1, EvolutionStrip.Fill(fs, 1, star), 1e-5, $"1 dạng, sao {star}");
            }
        }

        // tướng đứng trên nút ải ở màn đảo: boss, không thì địch cấp cao nhất, bằng cấp thì độ hiếm; boss tiến hóa hiện dạng 1
        [Test]
        public void TuongTrenNutAi_KhopBanWeb()
        {
            var d = TestData.Load();
            var leads = J.Arr(Golden(), "leads");
            Assert.AreEqual(d.Stages.Count, leads.Count);
            foreach (var x in leads)
            {
                var o = J.Obj(x);
                var st = d.Stages.Find(s => s.id == J.Int(o, "id"));
                var en = Teams.StageLead(st, d);
                Assert.AreEqual(J.Str(o, "hero"), en.hero, $"ải {st.id}");
                Assert.AreEqual(J.Int(o, "star"), Teams.EnemyFormStar(en), $"ải {st.id} sao");
            }
        }

        [Test]
        public void DiChuyenBanLuuV3_KhopBanWeb()
        {
            foreach (var x in J.Arr(Golden(), "migrate"))
            {
                var o = J.Obj(x);
                var tree = J.Obj(MiniJson.Parse(MiniJson.Write(J.Obj(o, "in"))));
                SaveCodec.MigrateRosterV3(tree);
                Assert.AreEqual(MiniJson.Write(J.Obj(o, "out")), MiniJson.Write(tree));
            }
        }

        [Test]
        public void DiChuyenBanLuuV3_DocDuoc()
        {
            // bản lưu v3 có Y Trạch trong đội: đọc ra v4, Y Trạch gộp vào Tiểu Y, đủ tướng
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            var tree = J.Obj(MiniJson.Parse(SaveCodec.Write(s)));
            tree["v"] = 3.0;
            var hs = J.Obj(tree, "heroes");
            var yt = J.Obj(MiniJson.Parse(MiniJson.Write(J.Obj(hs, "tieu_y"))));
            yt["owned"] = true;
            yt["star"] = 3.0;
            hs["y_trach"] = yt;
            tree["team"] = new List<object> { "y_trach", "giot_suong" };
            Assert.AreEqual(LoadStatus.Migrated, SaveCodec.Read(MiniJson.Write(tree), d, out var r));
            Assert.AreEqual(d.Cfg.saveVersion, r.v);
            Assert.IsTrue(r.Hero("tieu_y").owned);
            Assert.AreEqual(3, r.Hero("tieu_y").star);
            Assert.IsNull(r.Hero("y_trach"));
            Assert.AreEqual(new[] { "tieu_y", "giot_suong" }, r.team.ToArray());
            Assert.AreEqual(d.Heroes.Count, r.heroes.Count);
        }
    }
}
