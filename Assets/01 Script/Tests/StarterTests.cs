// Chọn 1 trong 5 tướng khởi đầu (GD_Claude/15_TuongKhoiDau.md): người chơi mới chưa có tướng, chọn xong có đúng 1; mỗi hệ một tướng
// thu phục được ở chặng đầu đảo cùng hệ (ải 1, riêng Nụ Hoa ở ải 2 đảo Mộc và Bu Lông ở ải 2 đảo Kim từ 2026-11-05); bản lưu v4 -> v5; ô đội 2 mở ở ải 3 đảo Thủy cùng quà theo lựa chọn; tướng đồng hành không bị khắc hệ.
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class StarterTests
    {
        [Test]
        public void NguoiChoiMoi_ChuaChon_ChonXongCoDung1Tuong()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0, null);
            Assert.IsNull(s.starter);
            Assert.IsEmpty(s.team);
            Assert.IsFalse(s.heroes.Values.Any(h => h.owned), "chưa chọn thì chưa có tướng nào");
            Assert.AreEqual(1, Progress.TeamSlots(s));

            foreach (var id in d.Starters)
            {
                var c = SaveData.New(d, 0, id);
                Assert.AreEqual(id, c.starter);
                CollectionAssert.AreEqual(new[] { id }, c.team);
                CollectionAssert.AreEqual(new[] { id }, c.heroes.Where(kv => kv.Value.owned).Select(kv => kv.Key).ToArray(), id);
                Assert.AreEqual(0, d.Hero(id).FormIndex(d.Cfg.formStars, c.Hero(id).star), id + " ở dạng 1");
                Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(c), d, out var back));
                Assert.AreEqual(id, back.starter, "ghi rồi đọc lại giữ tướng khởi đầu");
            }
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var none));
            Assert.IsNull(none.starter, "chưa chọn thì đọc lại vẫn chưa chọn");
            Assert.AreEqual("giot_suong", SaveData.New(d, 0).starter, "mặc định cho test và máy tự chơi: tướng đầu danh sách");
        }

        [Test]
        public void MoiHeMotTuong_ThuPhucO_ChangDau_DaoCungHe_RoiManh()
        {
            var d = TestData.Load();
            Assert.IsEmpty(d.Validate());
            Assert.AreEqual(5, d.Starters.Count);
            CollectionAssert.AreEquivalent(Elements.All, d.Starters.Select(id => d.Hero(id).elem), "mỗi hệ một tướng");
            foreach (var id in d.Starters)
            {
                var h = d.Hero(id);
                Assert.AreEqual(Rarity.Uncommon, h.rarity, id + " cùng độ hiếm Khá");
                Assert.AreEqual(3, h.forms.Length, id + " dòng 3 dạng");
                var at = d.StarterStage(id);
                Assert.IsNotNull(at, id);
                // đảo Mộc nhường ải 1 cho Tiên Lá, đảo Kim cho Bọ Cạp Đồng (10 tướng người dùng chọn 2026-11-05): Nụ Hoa, Bu Lông
                // đứng cùng một lính ở ải 2
                if (h.elem == Elem.Moc || h.elem == Elem.Kim)
                {
                    Assert.AreEqual(2, at.idx, id);
                    Assert.AreEqual(h.elem == Elem.Moc ? "tien_la" : "bo_cap", d.ZoneStages(h.elem).First(st => st.idx == 1).enemies[0].hero);
                }
                else
                {
                    Assert.AreEqual(1, at.idx, id);
                    Assert.AreEqual(1, at.enemies.Count, id);
                }
                var dr = at.drops.Single(x => x.hero == id);
                Assert.AreEqual(1, dr.chance, id + " lần đầu chắc chắn rơi mảnh");
                Assert.AreEqual(2, dr.min, id);
                Assert.AreEqual(4, dr.max, id);
                Assert.IsFalse(dr.gift, id + " phải thu phục, không tặng");
            }
        }

        [Test]
        public void BanLuuV4_CoGiotSuong_CoiNhuDaChonGiotSuong()
        {
            var d = TestData.Load();
            string V4(SaveData s) => SaveCodec.Write(s).Replace($"\"v\":{d.Cfg.saveVersion}", "\"v\":4");

            var old = SaveData.New(d, 0, null);
            old.Hero("giot_suong").owned = old.Hero("vo_su").owned = true;
            old.team = new List<string> { "vo_su", "giot_suong" };
            Assert.AreEqual(LoadStatus.Migrated, SaveCodec.Read(V4(old), d, out var a));
            Assert.AreEqual("giot_suong", a.starter);
            CollectionAssert.AreEqual(new[] { "vo_su", "giot_suong" }, a.team, "đội giữ nguyên");

            var noGs = SaveData.New(d, 0, null);
            noGs.Hero("vo_su").owned = true;
            Assert.AreEqual(LoadStatus.Migrated, SaveCodec.Read(V4(noGs), d, out var b));
            Assert.AreEqual("vo_su", b.starter, "không có Giọt Sương thì tướng đầu tiên đã có");

            Assert.AreEqual(LoadStatus.Migrated, SaveCodec.Read(V4(SaveData.New(d, 0, null)), d, out var c));
            Assert.IsNull(c.starter, "không có tướng nào thì để chọn");
        }

        [Test]
        public void Qua3AiDaoThuy_QuaTheoLuaChon_VaoODoiKhiCoOTrong()
        {
            var d = TestData.Load();
            var rng = new Rng(5);
            foreach (var id in d.Starters)
            {
                var s = SaveData.New(d, 0, id);
                for (int i = 1; i <= 3; i++) Progress.WinStage(s, d, d.ZoneStages(Elem.Thuy).First(st => st.idx == i).id, rng);
                Assert.AreEqual(1, Progress.TeamSlots(s), id + ": cấp 1 vẫn 1 ô");
                string gift = id == "thach_nhan" ? "meo_quyen" : "vo_su";
                Assert.IsTrue(s.Hero(gift).owned, $"{id}: quà ải 3 là {gift}");
                CollectionAssert.AreEqual(new[] { id }, s.team, id + ": hết ô thì quà không vào đội");
                // có ô trống (cấp 10) thì tướng tặng vào đội ngay
                var s2 = SaveData.New(d, 0, id);
                s2.level = Progress.SlotLevels[1];
                for (int i = 1; i <= 3; i++) Progress.WinStage(s2, d, d.ZoneStages(Elem.Thuy).First(st => st.idx == i).id, rng);
                CollectionAssert.AreEqual(new[] { id, gift }, s2.team, id + ": quà vào ô đội 2 còn trống");
                Assert.AreEqual(id == "thach_nhan", !s.Hero("vo_su").owned, id + ": Võ Sư");
                // đội trên đảo Thủy: một tướng khắc Thủy (Thổ) và một tướng trung tính
                var owned = s.heroes.Where(kv => kv.Value.owned).Select(kv => d.Hero(kv.Key)).ToList();
                Assert.AreEqual(2, owned.Count, id);
                Assert.AreEqual(1, owned.Count(h => Elements.Mult(h.elem, Elem.Thuy, h.id == id, false) > 1), id + ": một tướng khắc đảo");
                Assert.AreEqual(1, owned.Count(h => Elements.Mult(h.elem, Elem.Thuy, h.id == id, false) == 1
                                                   && Elements.Mult(Elem.Thuy, h.elem, false, h.id == id) == 1), id + ": một tướng trung tính");
            }
        }

        [Test]
        public void TuongDongHanh_KhongBiKhac_VanKhacDuoc()
        {
            // Hỏa bị Thủy khắc; Thủy khắc Hỏa
            Assert.AreEqual(0.75, Elements.Mult(Elem.Hoa, Elem.Thuy));
            Assert.AreEqual(1, Elements.Mult(Elem.Hoa, Elem.Thuy, true, false), "đồng hành đánh hệ khắc mình vẫn ×1");
            Assert.AreEqual(1, Elements.Mult(Elem.Thuy, Elem.Hoa, false, true), "bị hệ khắc mình đánh vẫn ×1");
            Assert.AreEqual(1.5, Elements.Mult(Elem.Thuy, Elem.Hoa, true, false), "đồng hành khắc thì vẫn ×1,5");
            Assert.AreEqual(1.5, Elements.Mult(Elem.Thuy, Elem.Hoa, false, false));

            // trong trận: tướng khởi đầu của bản lưu là tướng đồng hành, địch thì không
            var d = TestData.Load();
            var s = SaveData.New(d, 0, "su_tu_lua");
            var stage = d.ZoneStages(Elem.Thuy).First(st => st.idx == 1);
            var b = Battle.Create(d, Teams.Player(s, null, d), Teams.Enemy(stage, d), 1);
            Assert.IsTrue(b.ActiveOf(0).partner);
            Assert.IsFalse(b.ActiveOf(1).partner);
            Assert.AreEqual(1, Battle.ElemMult(b.ActiveOf(0), b.ActiveOf(1)));
            Assert.AreEqual(1, Battle.ElemMult(b.ActiveOf(1), b.ActiveOf(0)));
        }
    }
}
