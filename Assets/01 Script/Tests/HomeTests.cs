// Nhà (Core/Home.cs, GD_Claude/21_Nha_Home.md, 2026-11-18): dữ liệu, khoảnh đầu, luật đặt chỗ, xây và đội thợ, dọn ô rừng, sản xuất
// (bi, gỗ, quặng và đá tiến hóa, lò rèn ăn quặng, bánh), chỗ tướng (tổng theo cấp Nhà, chỗ ra bi theo đường Trang trại cũ), tưới tiêu,
// trang trí và điểm đẹp, gộp Trang trại cũ, lưu rồi đọc lại, lùi giờ máy.
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class HomeTests
    {
        const double H = 3600000, M = 60000;

        static SaveData NewSave(GameData d, int level = 1)
        {
            var s = SaveData.New(d, 0, TestData.OldStarter);
            foreach (var id in new[] { "vo_su", "tien_la", "so_ngoc", "nguu_quyen", "thach_giai", "ca_den" })
                if (s.Hero(id) != null) s.Hero(id).owned = true;
            s.level = level;
            return s;
        }

        static HomeBuilding B(SaveData s, string def) => s.home.buildings.First(b => b.def == def);

        [Test]
        public void DuLieu_HopLe()
        {
            var d = TestData.Load();
            var c = d.Cfg.home;
            CollectionAssert.IsEmpty(c.Validate());
            Assert.AreEqual(48, c.grid);
            Assert.AreEqual(8, c.lot);
            Assert.AreEqual(10, c.levels.Count, "10 cấp Nhà chính");
            Assert.AreEqual(3, c.rings.Count);
            foreach (var id in new[] { "main", "field", "orchard", "sawmill", "pond", "mine", "forge", "kitchen", "storage", "well", "waterwheel", "hotspring", "tree" })
                Assert.IsNotNull(c.Def(id), id);
            Assert.AreEqual(6, c.Def("main").size);
            Assert.AreEqual(6, c.Def("mine").size);
            Assert.AreEqual(4, c.Def("field").size);
            Assert.AreEqual(2, c.Def("well").size);
            Assert.AreEqual(Elem.Tho, c.Def("field").elem);
            Assert.AreEqual(Elem.Thuy, c.Def("pond").elem);
            Assert.AreEqual(Elem.Kim, c.Def("forge").elem);
            Assert.AreEqual(Elem.Hoa, c.Def("kitchen").elem);
            Assert.AreEqual(c.Def("field").rate, d.Cfg.farm.@base, "ruộng ra bi bằng trang trại cũ");
            Assert.AreEqual(3, AdGate.Limit(d.Cfg, "home_speed"));
        }

        [Test]
        public void KhoanhDau_VaBoCuc()
        {
            var d = TestData.Load();
            var s = NewSave(d);
            var h = Home.Of(s, d, 0);
            Assert.AreEqual(7, h.lots.Count, "khoảnh đầu 2 x 2 ô rừng và ba ô ven biển tới bến");
            Assert.AreEqual("dirt", Home.TileAt(h, d.Cfg.home, 20, 20), "đường đất từ bến lên Nhà chính");
            Assert.AreEqual(1, Home.Level(h));
            Assert.AreEqual(1, Home.Builders(h, d.Cfg.home));
            foreach (var def in new[] { "main", "field", "orchard", "sawmill", "storage" }) Assert.AreEqual(1, Home.CountOf(h, def), def);
            Assert.AreEqual(0, Home.CountOf(h, "tree"), "chưa qua ải nào thì chưa có Cây bi");
            Assert.AreEqual(4, Home.TotalSlots(h, d.Cfg.home));
            Assert.AreEqual(1, B(s, "field").slots.Count);
            Assert.AreEqual(0, Home.Ring(d.Cfg.home, h.lots[0]));
            Assert.AreEqual(d.Cfg.home.woodCap + 300, Home.WoodCap(h, d.Cfg), "kho cấp 1 thêm 300 gỗ");
        }

        [Test]
        public void DatCho_Chong_Khoa_Chan_Mach()
        {
            var d = TestData.Load();
            var s = NewSave(d);
            Home.Of(s, d, 0);
            var main = B(s, "main");
            Assert.AreEqual(HomeErr.Overlap, Home.CanPlace(s, d, "well", main.gx + 1, main.gy + 1));
            Assert.AreEqual(HomeErr.Ok, Home.CanPlace(s, d, "well", 30, 34));
            Assert.AreEqual(HomeErr.Locked, Home.CanPlace(s, d, "well", 10, 30), "ô rừng chưa mở");
            Assert.AreEqual(HomeErr.Locked, Home.CanPlace(s, d, "well", 23, 30), "chân thoi chìa ra ô rừng chưa mở");
            Assert.AreEqual(HomeErr.OutOfMap, Home.CanPlace(s, d, "well", 47, 47));
            s.home.lots.Add(Home.LotIndex(d.Cfg.home, 1, 1));
            Assert.AreEqual(HomeErr.Blocked, Home.CanPlace(s, d, "well", 10, 10), "hồ chặn");
            s.home.lots.Add(Home.LotIndex(d.Cfg.home, 2, 4));
            Assert.AreEqual(HomeErr.Ok, Home.CanPlace(s, d, "mine", 17, 33), "Mỏ trên mạch quặng");
            Assert.AreEqual(HomeErr.NeedOre, Home.CanPlace(s, d, "mine", 26, 33), "Mỏ ngoài mạch quặng");
            Assert.AreEqual(HomeErr.Blocked, Home.CanPlace(s, d, "well", 18, 34), "mạch quặng để dành cho Mỏ");
            s.home.lots.Add(Home.LotIndex(d.Cfg.home, 1, 2));
            s.home.lots.Add(Home.LotIndex(d.Cfg.home, 2, 2));
            Assert.AreEqual(HomeErr.Ok, Home.CanPlace(s, d, "waterwheel", 12, 17), "cối nước sát suối (cột gx 11)");
            Assert.AreEqual(HomeErr.Blocked, Home.CanPlace(s, d, "waterwheel", 10, 17), "suối chặn");
            Assert.AreEqual(HomeErr.NeedStream, Home.CanPlace(s, d, "waterwheel", 16, 17));
            // dời Nhà chính về chỗ cũ của nó vẫn được (bỏ qua chính nó)
            Assert.AreEqual(HomeErr.Ok, Home.CanPlace(s, d, "main", main.gx, main.gy, main.id));
        }

        [Test]
        public void Xay_DoiTho_XongTheoGio()
        {
            var d = TestData.Load();
            var s = NewSave(d);
            var h = Home.Of(s, d, 0);
            Assert.AreEqual(HomeErr.HomeLevel, Home.Build(s, d, 0, "well", 30, 34), "giếng mở ở Nhà cấp 2");
            Assert.AreEqual(HomeErr.Count, Home.Build(s, d, 0, "field", 30, 34), "Nhà cấp 1 chỉ một ruộng");
            // lên Nhà cấp 2: cần cấp 10 và 60 gỗ
            var main = B(s, "main");
            Assert.AreEqual(HomeErr.PlayerLevel, Home.Upgrade(s, d, 0, main.id));
            s.level = 10;
            Assert.AreEqual(HomeErr.Cost, Home.Upgrade(s, d, 0, main.id));
            h.wood = 100;
            Assert.AreEqual(HomeErr.Ok, Home.Upgrade(s, d, 0, main.id));
            Assert.AreEqual(40, h.wood);
            Assert.AreEqual(2, main.job);
            Assert.AreEqual(1, Home.Level(h), "đang nâng cấp vẫn là cấp cũ");
            Assert.AreEqual(HomeErr.Builder, Home.CanClear(s, d, Home.LotIndex(d.Cfg.home, 2, 3)), "một đội thợ đang bận");
            Home.Tick(s, d, 5 * M);
            Assert.AreEqual(2, Home.Level(h), "5 phút sau xong");
            Assert.AreEqual(0, main.job);
            // giếng: 25 gỗ, 5 phút
            Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, 5 * M, "well", 30, 34, out var well));
            Assert.AreEqual(15, h.wood);
            Assert.AreEqual(1, well.job);
            h.wood = 100;
            Assert.AreEqual(HomeErr.Builder, Home.CanBuild(s, d, "pond"));
            Assert.IsTrue(Home.SpeedUp(s, d, 6 * M, well.id), "rút 30 phút");
            Assert.AreEqual(0, well.job);
            // trang trí đặt ngay, không cần thợ, không giới hạn số
            h.wood = 50;
            Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, 6 * M, "flowerbed", 31, 37, out var fb));
            Assert.AreEqual(0, fb.job);
            Assert.AreEqual(HomeErr.Locked, Home.CanBuild(s, d, "cup_fish"), "cúp câu cá chỉ có từ thưởng");
            Assert.IsTrue(Home.Store(s, d, fb.id));
            Assert.AreEqual(1, h.bag["flowerbed"]);
            double w = h.wood;
            Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, 6 * M, "flowerbed", 32, 37));
            Assert.AreEqual(w, h.wood, "đặt lại từ túi không tốn gỗ");
            Assert.IsFalse(h.bag.ContainsKey("flowerbed"));
            Assert.IsFalse(Home.Store(s, d, well.id), "công trình không cất vào túi");
        }

        [Test]
        public void DonRung_KeDat_KhoaCap_ThuongGo()
        {
            var d = TestData.Load();
            var c = d.Cfg.home;
            var s = NewSave(d);
            var h = Home.Of(s, d, 0);
            int near = Home.LotIndex(c, 2, 3), far = Home.LotIndex(c, 1, 3), hill = Home.LotIndex(c, 0, 0);
            Assert.AreEqual(1, Home.Ring(c, near));
            Assert.AreEqual(2, Home.Ring(c, far));
            Assert.AreEqual(HomeErr.NotAdjacent, Home.CanClear(s, d, far));
            Assert.AreEqual(HomeErr.Locked, Home.CanClear(s, d, hill));
            Assert.AreEqual(HomeErr.Cost, Home.CanClear(s, d, near));
            h.wood = 200;
            Assert.AreEqual(HomeErr.Ok, Home.ClearLot(s, d, 0, near));
            Assert.AreEqual(160, h.wood, "vòng 1: 40 gỗ");
            Assert.AreEqual(HomeErr.Builder, Home.CanClear(s, d, Home.LotIndex(c, 3, 2)));
            int balls0 = s.balls;
            Home.Tick(s, d, 10 * M);
            Assert.IsTrue(h.lots.Contains(near));
            Assert.AreEqual(190, h.wood, "dọn xong rơi 30 gỗ");
            Assert.AreEqual(balls0 + 15, s.balls, "dọn xong được 15 bi để thả");
            CollectionAssert.AreEqual(new[] { near }, h.cleared, "màn Nhà báo thưởng ô vừa dọn");
            Assert.AreEqual((65, 0, 10.0), Home.ClearCost(h, c, Home.LotIndex(c, 3, 2)), "ô thứ hai của vòng 1 đắt thêm 25 gỗ");
            Assert.AreEqual(HomeErr.HomeLevel, Home.CanClear(s, d, far), "vòng 2 cần Nhà cấp 3");
            // Nhà cấp 1 chỉ mở tới 9 ô rừng (7 ô khoảnh đầu + 2)
            h.wood = 1000;
            Assert.AreEqual(HomeErr.Ok, Home.ClearLot(s, d, 10 * M, Home.LotIndex(c, 3, 2)));
            Home.Tick(s, d, 30 * M);
            Assert.AreEqual(9, h.lots.Count);
            Assert.AreEqual(HomeErr.Count, Home.CanClear(s, d, Home.LotIndex(c, 4, 2)));
        }

        [Test]
        public void SanXuat_Bi_Go_Kho_ThuHoach()
        {
            var d = TestData.Load();
            var s = NewSave(d);
            var h = Home.Of(s, d, 0);
            var field = B(s, "field");
            var saw = B(s, "sawmill");
            Assert.AreEqual(HomeErr.Ok, Home.Place(s, d, 0, field.id, 0, "vo_su"));
            Assert.AreEqual(HomeErr.HeroBusy, Home.Place(s, d, 0, saw.id, 0, "vo_su"), "một tướng một chỗ");
            Assert.AreEqual(HomeErr.Ok, Home.Place(s, d, 0, saw.id, 0, "tien_la"));
            double rf = Home.Rate(s, d, "vo_su", field), rs = Home.Rate(s, d, "tien_la", saw);
            Assert.AreEqual(Home.Hours(s, d, "vo_su"), field.slots[0].energy);
            int balls = s.balls;
            var y = Home.HarvestAll(s, d, 3 * H);
            Assert.AreEqual((int)System.Math.Floor(rf * 3 + 1e-9), y.balls);
            Assert.AreEqual(balls + y.balls, s.balls);
            Assert.AreEqual((int)System.Math.Floor(rs * 3 + 1e-9), y.wood);
            // kho đồ của ô chặn ở capH giờ, hết ca thì ngừng
            Home.Tick(s, d, 40 * H);
            Assert.AreEqual(0, field.slots[0].energy);
            Assert.IsTrue(Home.Alert(s, d, 40 * H));
            Assert.LessOrEqual(field.slots[0].stock, rf * Home.CapHours(d.Cfg, d.Cfg.home.Def("field"), 1) + 1e-9);
            // gỗ chặn ở sức chứa kho
            h.wood = Home.WoodCap(h, d.Cfg) - 2;
            Home.Harvest(s, d, 40 * H, saw.id);
            Assert.AreEqual(Home.WoodCap(h, d.Cfg), h.wood);
            Assert.Greater(saw.slots[0].stock, 0, "phần không vừa kho vẫn ở ô");
            // rút: tướng nghỉ, ăn bánh thì hết nghỉ
            Assert.IsTrue(Home.Remove(s, d, 40 * H, field.id, 0));
            Assert.Greater(Home.RestLeft(h, "vo_su", 40 * H), 0);
            Assert.AreEqual(HomeErr.Cost, Home.Feed(s, d, 40 * H, "vo_su"));
            h.bread = 1;
            Assert.AreEqual(HomeErr.Ok, Home.Feed(s, d, 40 * H, "vo_su"));
            Assert.AreEqual(0, h.bread);
            Assert.IsTrue(Home.Free(s, h, "vo_su", 40 * H));
        }

        [Test]
        public void ChoTuong_TongTheoCapNha_BiTheoTrangTraiCu()
        {
            var d = TestData.Load();
            var s = NewSave(d, 39);
            var h = Home.Of(s, d, 0);
            Assert.AreEqual(3, Home.BallSlots(s, d.Cfg), "cấp 39: 3 chỗ bi như Trang trại cũ");
            // cho Nhà lên cấp 4 (6 chỗ), xây thêm ruộng, vườn
            B(s, "main").level = 4;
            h.lots.AddRange(new[] { Home.LotIndex(d.Cfg.home, 2, 3), Home.LotIndex(d.Cfg.home, 3, 2) });
            h.wood = 1000;
            h.ore = 100;
            Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, 0, "field", 30, 34, out var f2));
            Home.Tick(s, d, 2 * M);
            Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, 2 * M, "orchard", 34, 34, out var o2));
            Home.Tick(s, d, 4 * M);
            var heroes = new[] { "vo_su", "tien_la", "so_ngoc", "nguu_quyen", "thach_giai" };
            var ballB = new[] { B(s, "field"), B(s, "orchard"), f2, o2 };
            int k = 0;
            foreach (var b in ballB)
            {
                var e = Home.Place(s, d, 4 * M, b.id, 0, heroes[k]);
                if (k < Home.BallSlots(s, d.Cfg)) Assert.AreEqual(HomeErr.Ok, e, "chỗ bi " + k);
                else Assert.AreEqual(HomeErr.BallSlots, e, "quá chỗ bi của Trang trại cũ");
                k++;
            }
            Assert.AreEqual(HomeErr.Ok, Home.Place(s, d, 4 * M, B(s, "sawmill").id, 0, heroes[4]), "xưởng gỗ không tính vào chỗ bi");
        }

        [Test]
        public void Mo_LoRen_TuoiTieu_DatMau()
        {
            var d = TestData.Load();
            var c = d.Cfg.home;
            var s = NewSave(d, 60);
            var h = Home.Of(s, d, 0);
            B(s, "main").level = 5;
            h.lots.AddRange(new[] { Home.LotIndex(c, 2, 4), Home.LotIndex(c, 3, 5), Home.LotIndex(c, 2, 3) });
            h.wood = 2000;
            h.ore = 50;
            // Mỏ: quặng, tích phần lẻ đá tiến hóa
            Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, 0, "mine", 17, 33, out var mine));
            Home.Tick(s, d, 20 * M);
            Assert.AreEqual(HomeErr.Ok, Home.Place(s, d, 20 * M, mine.id, 0, "vo_su"));
            double rm = Home.Rate(s, d, "vo_su", mine);
            Home.Tick(s, d, 20 * M + 4 * H);
            Assert.AreEqual(rm * 4 * c.evoPerOre, mine.acc, 1e-9);
            mine.acc = 1.2;
            var y = Home.Harvest(s, d, 20 * M + 4 * H, mine.id);
            Assert.AreEqual(1, y.evo);
            Assert.AreEqual((int)System.Math.Floor(rm * 4 + 1e-9), y.ore);
            // Lò rèn: ra đá tiềm năng, ăn orePerStone quặng mỗi viên; hết quặng thì ngừng
            Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, 20 * M + 4 * H, "forge", 30, 34, out var forge));
            double t = 20 * M + 4 * H + 30 * M;
            Home.Tick(s, d, t);
            Assert.AreEqual(HomeErr.Ok, Home.Place(s, d, t, forge.id, 0, "nguu_quyen"));
            h.ore = 5;
            Home.Tick(s, d, t + 8 * H);
            Assert.AreEqual(1.0, forge.slots[0].stock, 1e-9, "5 quặng chỉ đủ một viên");
            Assert.AreEqual(0, h.ore, 1e-9);
            // tưới tiêu: ruộng trong bán kính giếng +10%; đất màu +10%
            var field = B(s, "field");
            double r0 = Home.Rate(s, d, "tien_la", field);
            Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, t + 8 * H, "well", field.gx + 4 + 2, field.gy, out var well));
            Home.Tick(s, d, t + 9 * H);
            Assert.AreEqual(r0 * 1.1, Home.Rate(s, d, "tien_la", field), 1e-9, "giếng cách 2 ô");
            Assert.AreEqual(HomeErr.Ok, Home.Move(s, d, well.id, 30, 44));
            Assert.AreEqual(0, Home.Irrigation(h, d.Cfg, field), "dời giếng ra xa");
            Assert.AreEqual(HomeErr.Ok, Home.Move(s, d, field.id, 24, 40));
            Assert.AreEqual(c.fertileBonus, Home.Fertile(c, c.Def("field"), field), "ruộng trên đất màu");
        }

        [Test]
        public void DiemDep_MocQua()
        {
            var d = TestData.Load();
            var s = NewSave(d);
            var h = Home.Of(s, d, 0);
            Assert.AreEqual(0, Home.Beauty(h, d.Cfg));
            Assert.IsNull(Home.ClaimBeauty(s, d));
            h.wood = 100;
            for (int i = 0; i < 5; i++) Assert.AreEqual(HomeErr.Ok, Home.Build(s, d, 0, "flowerbed", 30 + i, 34));
            Assert.AreEqual(10, Home.Beauty(h, d.Cfg));
            Assert.AreEqual(1, Home.BeautyTier(h, d.Cfg));
            double rest0 = Farm.RestMin(s, d, "vo_su");
            Assert.AreEqual(rest0 * (1 - d.Cfg.home.restPerTier), Home.RestMin(s, d, "vo_su"), 1e-9);
            double w = h.wood;
            var g = Home.ClaimBeauty(s, d);
            Assert.IsNotNull(g);
            Assert.AreEqual(w + g.wood, h.wood);
            Assert.IsNull(Home.ClaimBeauty(s, d), "mỗi mốc nhận một lần");
        }

        [Test]
        public void GopTrangTraiCu_VaCayBi()
        {
            var d = TestData.Load();
            var s = NewSave(d, 9);
            s.zones[0] = 1; // qua ải 1: có Cây bi đầu
            Farm.Place(s, d, 0, 0, "thach_giai"); // ao vịt (Thủy)
            Farm.Place(s, d, 0, 1, "vo_su"); // ruộng rau (Thổ)
            Farm.Remove(s, d, 1.9 * H, 1); // rút lúc 1,9 giờ: tới lúc gộp (2 giờ) vẫn đang nghỉ
            Farm.Place(s, d, 1.9 * H, 2, "tien_la"); // vườn cây (Mộc)
            int balls = s.balls;
            double now = 2 * H;
            double farmStock = Farm.Stock(s, d, now);
            var h = Home.Of(s, d, now);
            Assert.IsNull(s.farm, "trang trại đã gộp vào Nhà");
            Assert.AreEqual(balls + (int)farmStock, s.balls, "bi đang tích của trang trại về túi");
            Assert.AreEqual(1, Home.CountOf(h, "pond"), "ao vịt có tướng thành Ao cá");
            Assert.AreEqual("thach_giai", B(s, "pond").slots[0].hero);
            Assert.AreEqual("tien_la", B(s, "orchard").slots[0].hero);
            Assert.Greater(Home.RestLeft(h, "vo_su", now), 0, "tướng đang nghỉ vẫn nghỉ");
            Assert.AreEqual(1, Home.CountOf(h, "tree"), "Cây bi đã mở được đặt vào nhà");
            Assert.AreEqual(0, B(s, "tree").tree);
            foreach (var b in h.buildings)
                Assert.AreEqual(HomeErr.Ok, Home.CanPlace(s, d, b.def, b.gx, b.gy, b.id), b.def + " nằm chỗ hợp lệ");
        }

        [Test]
        public void LatO_DatCatNuoc_MepTheoHangXom()
        {
            var d = TestData.Load();
            var c = d.Cfg.home;
            var s = NewSave(d);
            var h = Home.Of(s, d, 0);
            Assert.AreEqual(2, c.tile);
            Assert.AreEqual(24, Home.TilesPerSide(c));
            h.wood = 20;
            h.ore = 2;
            // ô lát (15,17) = ô lưới 30..31 x 34..35: trống, trong khoảnh đầu
            Assert.AreEqual(HomeErr.Ok, Home.Paint(s, d, 15, 17, "dirt"));
            Assert.AreEqual(19, h.wood);
            Assert.AreEqual("dirt", Home.TileAt(h, c, 15, 17));
            Assert.AreEqual(HomeErr.Busy, Home.CanPaint(s, d, 15, 17, "dirt"), "đã là đất");
            Assert.AreEqual(HomeErr.Locked, Home.CanPaint(s, d, 5, 15, "sand"), "ô rừng chưa mở");
            var main = B(s, "main");
            Assert.AreEqual(HomeErr.Overlap, Home.CanPaint(s, d, main.gx / 2 + 1, main.gy / 2 + 1, "sand"), "không lát dưới công trình");
            Assert.AreEqual(HomeErr.Ok, Home.Paint(s, d, 16, 17, "stone"));
            Assert.AreEqual(1, h.ore);
            // nước chặn xây
            Assert.AreEqual(HomeErr.Ok, Home.Paint(s, d, 15, 18, "water"));
            Assert.AreEqual(HomeErr.Blocked, Home.CanPlace(s, d, "well", 30, 36));
            double w0 = h.wood;
            Assert.AreEqual(HomeErr.Ok, Home.Paint(s, d, 15, 18, "sand"), "lát đè: hoàn giá nước (3 gỗ), trả giá cát (1 gỗ)");
            Assert.AreEqual(w0 + 3 - 1, h.wood);
            Assert.AreEqual(HomeErr.Ok, Home.Paint(s, d, 15, 18, "grass"));
            Assert.AreEqual(w0 + 3, h.wood, "xoá về cỏ: hoàn đủ, đổi ô không mất tài nguyên");
            Assert.IsNull(Home.TileAt(h, c, 15, 18));
            Assert.AreEqual(HomeErr.Ok, Home.CanPlace(s, d, "well", 30, 36));
            // không lát lên suối, hồ, mạch quặng
            h.lots.Add(Home.LotIndex(c, 1, 2));
            Assert.AreEqual(HomeErr.Blocked, Home.CanPaint(s, d, 5, 9, "sand"), "ô lát (5,9) chứa suối cột gx 11");
            // mép: hàng xóm cùng loại
            h.wood = 20;
            Home.Paint(s, d, 15, 18, "dirt");
            Home.Paint(s, d, 14, 17, "dirt");
            int m = Home.TileMask(h, c, 15, 17);
            Assert.AreEqual(0, m & 1, "+tx là đường đá, khác loại");
            Assert.AreNotEqual(0, m & 2, "+ty là đất");
            Assert.AreNotEqual(0, m & 4, "-tx là đất");
            Assert.AreEqual(0, m & 8);
            Assert.AreEqual(0, m & 0x20, "góc (-tx,+ty) chưa lát");
            Assert.AreEqual(0, Home.TileMask(h, c, 0, 0), "ô cỏ không có mép");
            // lưu rồi đọc lại
            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var r));
            Assert.AreEqual("stone", Home.TileAt(r.home, c, 16, 17));
            Assert.AreEqual(json, SaveCodec.Write(r));
        }

        [Test]
        public void LuuDocLai_VaLuiGio()
        {
            var d = TestData.Load();
            var s = NewSave(d, 12);
            var h = Home.Of(s, d, 10 * H);
            h.wood = 77;
            h.ore = 5.5;
            h.bread = 2;
            Home.Place(s, d, 10 * H, B(s, "field").id, 0, "vo_su");
            Home.Bag(h, "cup_fish", 1);
            h.clearing[Home.LotIndex(d.Cfg.home, 2, 3)] = 11 * H;
            Home.Tick(s, d, 10.5 * H);
            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var r));
            Assert.AreEqual(json, SaveCodec.Write(r), "đọc rồi ghi lại y nguyên");
            Assert.AreEqual(77, r.home.wood);
            Assert.AreEqual(5.5, r.home.ore);
            Assert.AreEqual(1, r.home.bag["cup_fish"]);
            Assert.AreEqual(h.buildings.Count, r.home.buildings.Count);
            Assert.AreEqual("vo_su", r.home.buildings.First(b => b.def == "field").slots[0].hero);
            Assert.AreEqual(11 * H, r.home.clearing[Home.LotIndex(d.Cfg.home, 2, 3)]);
            // lùi giờ máy: bỏ qua đoạn đó, không ra đồ
            double stock = B(s, "field").slots[0].stock;
            Assert.IsFalse(Home.Tick(s, d, 9 * H));
            Assert.AreEqual(stock, B(s, "field").slots[0].stock);
            Assert.IsTrue(Home.Tick(s, d, 9.5 * H));
        }
    }
}
