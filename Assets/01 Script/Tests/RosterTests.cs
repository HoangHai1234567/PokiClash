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
        public void DanhSach88Tuong_Thuy23_Hoa17_Kim16_Moc15_Tho17()
        {
            // 40 tướng 8 mỗi hệ, Thủy thêm 5 (2026-11-02, kịch bản đảo Thủy), Mộc thêm 7, Hỏa thêm 8, Kim thêm 8 (2026-11-05, 10 tướng mỗi đảo), Hỏa thêm Ngưu Quyền ở ải 20, Thổ thêm 9 (2026-11-06),
            // Thủy thêm 10 tướng mới thay 10 suất đảo Thủy (2026-11-11, ArtGen/Spine/quai/DAC_TA_LO_THUY.md; tướng cũ vẫn giữ)
            var d = TestData.Load();
            Assert.IsEmpty(d.Validate());
            Assert.AreEqual(88, d.Heroes.Count);
            for (int e = 0; e < 5; e++)
                Assert.AreEqual((Elem)e == Elem.Thuy ? 23 : (Elem)e == Elem.Hoa ? 17 : (Elem)e == Elem.Kim ? 16 : (Elem)e == Elem.Moc ? 15 : 17, d.Heroes.FindAll(h => (int)h.elem == e).Count, ((Elem)e).ToString());
            // 5 tướng khởi đầu, mỗi hệ một, theo thứ tự đảo (15_TuongKhoiDau.md); hệ Thủy: Tí Tách thay Giọt Sương từ 2026-11-11
            Assert.AreEqual(new[] { "ti_tach", "su_tu_lua", "bu_long", "nu_hoa", "thach_nhan" }, d.Starters.ToArray());
            Assert.IsNotNull(d.Hero("giot_suong"), "tướng cũ mất suất đảo vẫn trong danh sách");
            foreach (var id in new[] { "gia_bi", "su_gia", "y_trach", "van_quan", "hac_duc" })
                Assert.IsNull(d.Hero(id), id + " đã gộp hoặc bỏ");
            // Lam Quân 3 dạng; từ 2026-11-08 là thú huyền thoại .atomik tự thiết kế (Bồ Lao, ArtGen/Spine/beast.py), mã hình <id>_<k>
            // (trước: rig aola thuy_1831 → thuy_1832 → thuy_2955)
            Assert.AreEqual(new[] { "lam_quan_1", "lam_quan_2", "lam_quan_3" }, System.Array.ConvertAll(d.Hero("lam_quan").forms, f => f.aola));
            // Thanh Long 3 dạng, Long Vuốt 2 dạng; từ 2026-11-08 là hình .atomik vẽ lại theo concept đã duyệt (ArtGen/Spine/build_moc.py,
            // beast.py), mã hình <id>_<k> (trước: rig aola goc_214 → 215 → 1749, goc_1219 → 1220)
            // 2026-11-13: hình của suất này nay là rồng trúc bốn cánh (boss cuối đảo Mộc, rig ArtGen/Spine/moc_vuong_rig.py); rig mới mới có
            // một dạng nên cả ba dạng tạm trỏ chung moc_vuong_1 (thư mục thanh_long_* cũ còn nguyên; quai/doi_moc_vuong.py --ve_cu trả lại)
            Assert.AreEqual(new[] { "moc_vuong_1", "moc_vuong_1", "moc_vuong_1" }, System.Array.ConvertAll(d.Hero("thanh_long").forms, f => f.aola));
            Assert.AreEqual(new[] { "long_vuot_1", "long_vuot_2" }, System.Array.ConvertAll(d.Hero("long_vuot").forms, f => f.aola));
            // đảo Kim (2026-11-05): boss Kim Nghê là dòng 克亚 → 克里亚斯 (2 dạng, aola không có siêu tiến hóa); từ 2026-11-09 là hình
            // .atomik vẽ lại (ArtGen/Spine/build_kim.py), mã hình <id>_<k> (trước: rig aola goc_1840 → goc_1841)
            Assert.AreEqual(new[] { "kim_nghe_1", "kim_nghe_2" }, System.Array.ConvertAll(d.Hero("kim_nghe").forms, f => f.aola));
            // đảo Thổ (2026-11-10): boss Giáp Nham .atomik vẽ lại (ArtGen/Spine/build_tho.py; trước: goc_1273 → goc_1274)
            Assert.AreEqual(new[] { "giap_nham_1", "giap_nham_2" }, System.Array.ConvertAll(d.Hero("giap_nham").forms, f => f.aola));
            // lô 10 tướng mới đảo Thủy (2026-11-11): .atomik dựng từ quái tham khảo, mã hình <id>_<k>; dòng 1–9 hai dạng, Hải Long ba dạng
            Assert.AreEqual(new[] { "ti_tach_1", "ti_tach_2" }, System.Array.ConvertAll(d.Hero("ti_tach").forms, f => f.aola));
            Assert.AreEqual(new[] { "hai_long_1", "hai_long_2", "hai_long_3" }, System.Array.ConvertAll(d.Hero("hai_long").forms, f => f.aola));
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
            // v4 gộp Y Trạch vào Tiểu Y, rồi v6 chuyển Tiểu Y sang Thạch Giải, Giọt Sương sang Tí Tách
            Assert.IsTrue(r.Hero("thach_giai").owned);
            Assert.AreEqual(3, r.Hero("thach_giai").star);
            Assert.IsFalse(r.Hero("tieu_y").owned, "tướng cũ bỏ khỏi bản lưu, đọc lại thành chưa có");
            Assert.IsNull(r.Hero("y_trach"));
            Assert.AreEqual(new[] { "thach_giai", "ti_tach" }, r.team.ToArray());
            Assert.AreEqual(d.Heroes.Count, r.heroes.Count);
        }

        [Test]
        public void DiChuyenBanLuuV5_TuongCuThuy_SangTuongMoi()
        {
            // bản lưu v5 có tướng cũ đảo Thủy: đọc ra v6, tiến trình chuyển sang tướng mới cùng suất, tướng cũ thành chưa có
            var d = TestData.Load();
            var s = SaveData.New(d, 0, "giot_suong");
            s.Hero("giot_suong").star = 4;
            s.Hero("giot_suong").shards = 7;
            s.Hero("giot_suong").skill.lv = 3;
            s.Hero("lam_quan").owned = true;
            s.Hero("lam_quan").shards = 5;
            s.Hero("hai_long").shards = 2; // tướng mới đã có mảnh: cộng dồn
            s.Hero("kuba").shards = 9; // chưa sở hữu, chỉ có mảnh
            s.team = new List<string> { "giot_suong", "lam_quan", "vo_su" };
            var tree = J.Obj(MiniJson.Parse(SaveCodec.Write(s)));
            tree["v"] = 5.0;
            Assert.AreEqual(LoadStatus.Migrated, SaveCodec.Read(MiniJson.Write(tree), d, out var r));
            Assert.AreEqual(d.Cfg.saveVersion, r.v);
            Assert.AreEqual("ti_tach", r.starter);
            Assert.IsTrue(r.Hero("ti_tach").owned);
            Assert.AreEqual(4, r.Hero("ti_tach").star);
            Assert.AreEqual(7, r.Hero("ti_tach").shards);
            Assert.AreEqual(3, r.Hero("ti_tach").skill.lv);
            Assert.IsTrue(r.Hero("hai_long").owned);
            Assert.AreEqual(7, r.Hero("hai_long").shards);
            Assert.IsFalse(r.Hero("lien_kinh").owned);
            Assert.AreEqual(9, r.Hero("lien_kinh").shards);
            foreach (var old in new[] { "giot_suong", "lam_quan", "kuba" })
            {
                Assert.IsFalse(r.Hero(old).owned, old);
                Assert.AreEqual(0, r.Hero(old).shards, old);
            }
            Assert.AreEqual(new[] { "ti_tach", "hai_long", "vo_su" }, r.team.ToArray());
            Assert.AreEqual(d.Heroes.Count, r.heroes.Count);
        }
    }
}
