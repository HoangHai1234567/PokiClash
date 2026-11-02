// 40 tướng (change expand-roster-40): dạng theo sao và bản lưu v3 -> v4 khớp bản web (Golden/roster.json, xuất bằng
// Web/scripts/export_golden.ts).
using System.Collections.Generic;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class RosterTests
    {
        static Dictionary<string, object> Golden() => J.Obj(MiniJson.Parse(TestData.Read("Golden/roster.json")));

        [Test]
        public void DanhSach40Tuong_8MoiHe()
        {
            var d = TestData.Load();
            Assert.IsEmpty(d.Validate());
            Assert.AreEqual(40, d.Heroes.Count);
            for (int e = 0; e < 5; e++)
                Assert.AreEqual(8, d.Heroes.FindAll(h => (int)h.elem == e).Count, ((Elem)e).ToString());
            Assert.AreEqual(new[] { "giot_suong" }, d.Starters.ToArray());
            foreach (var id in new[] { "gia_bi", "su_gia", "y_trach", "van_quan", "hac_duc" })
                Assert.IsNull(d.Hero(id), id + " đã gộp hoặc bỏ");
            Assert.AreEqual(new[] { "goc_1831", "goc_1832", "goc_2955" }, System.Array.ConvertAll(d.Hero("lam_quan").forms, f => f.aola));
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
            // bản lưu v3 có Y Trạch trong đội: đọc ra v4, Y Trạch gộp vào Tiểu Y, đủ 40 tướng
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
            Assert.AreEqual(40, r.heroes.Count);
        }
    }
}
