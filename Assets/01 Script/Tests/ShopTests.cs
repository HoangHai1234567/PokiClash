// Cửa hàng, Rương Tướng, ưu đãi (GD_Claude/26_CuaHang_IAP_QuangCao.md): cấu hình hợp lệ, mua gói (lần đầu tặng đôi, giới hạn ngày), gói
// nhận theo ngày, tỉ lệ và bảo hiểm Rương Tướng, Lọ Bi, thẻ tuần / tháng, chuỗi, quỹ, mốc quảng cáo, thang giá, trần popup, gói sau khi
// thua, bản lưu.
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class ShopTests
    {
        const double D = Shop.Day, H = Shop.Hour;
        const double T0 = 20500 * D + 10 * H; // giờ gốc của test (ms)

        static SaveData New(GameData d)
        {
            var s = SaveData.New(d, (long)T0);
            Tutorial.Skip(s); // xong hướng dẫn: cửa hàng, ưu đãi mở
            return s;
        }

        [Test]
        public void CauHinh_HopLe()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            CollectionAssert.IsEmpty(c.Validate());
            Assert.Greater(c.packs.Count, 15);
            Assert.AreEqual("poki_99", ShopConfig.Product(0.99));
            Assert.AreEqual("poki_9999", ShopConfig.Product(99.99));
            foreach (var p in c.packs) Assert.IsTrue(p.price >= 0 && (p.price == 0 || ShopConfig.Product(p.price).StartsWith("poki_")), p.id);
            // giá trị ×N của gói người mới lớn hơn bậc bi thường (gói đầu phải hời rõ)
            var s = New(d);
            Assert.Greater(Shop.PackMult(s, d, c.Pack("starter3")), 5, "Quà Nhập Môn");
            Assert.Greater(Shop.PackMult(s, d, c.Pack("launch")), 3, "Gói Khởi Hành");
            Assert.AreEqual(1, Shop.PackMult(s, d, c.Pack("balls_1")), 0.02, "Túi bi là giá gốc");
        }

        [Test]
        public void MuaBi_LanDauTangDoi_NhanBacCap()
        {
            var d = TestData.Load();
            var s = New(d);
            int b0 = s.balls;
            var got = Shop.BuyPack(s, d, "balls_1", T0, new Rng(1));
            Assert.NotNull(got);
            Assert.AreEqual(b0 + 200, s.balls, "lần đầu 100 + tặng 100");
            Shop.BuyPack(s, d, "balls_1", T0, new Rng(1));
            Assert.AreEqual(b0 + 300, s.balls, "lần hai không tặng");
            s.level = 60; // bậc ×2
            int b1 = s.balls;
            Shop.BuyPack(s, d, "balls_1", T0, new Rng(1));
            Assert.AreEqual(b1 + 200, s.balls, "cấp 60: số bi ×2");
            Assert.AreEqual(3 * 0.99, Shop.Spent(s, T0, 30), 1e-6);
        }

        [Test]
        public void GioiHanNgay_TrungHiemHomNay()
        {
            var d = TestData.Load();
            var s = New(d);
            Assert.NotNull(Shop.BuyPack(s, d, "egg_daily", T0, new Rng(1)));
            Assert.IsNull(Shop.BuyPack(s, d, "egg_daily", T0 + H, new Rng(1)), "mỗi ngày 1 lần");
            Assert.NotNull(Shop.BuyPack(s, d, "egg_daily", T0 + D, new Rng(1)), "hôm sau mua lại được");
            Assert.AreEqual(2, s.shop.Item(Eggs.Key(2)), "2 Trứng Hiếm trong túi");
        }

        [Test]
        public void GoiTheoNgay_NhanTungNgay()
        {
            var d = TestData.Load();
            var s = New(d);
            int b0 = s.balls;
            var got = Shop.BuyPack(s, d, "starter3", T0, new Rng(1));
            Assert.NotNull(got, "mua xong nhận ngày 1 luôn");
            Assert.AreEqual(b0 + 300, s.balls);
            Assert.AreEqual(1, s.shop.Item(Eggs.Key(2)), "ngày 1: Trứng Hiếm");
            Assert.IsFalse(Shop.DayClaimable(s, d, "starter3", T0 + H), "cùng ngày chưa nhận ngày 2");
            Assert.IsNull(Shop.BuyPack(s, d, "starter3", T0 + D, new Rng(1)), "chỉ mua một lần");
            Assert.NotNull(Shop.ClaimDay(s, d, "starter3", T0 + D, new Rng(1)), "ngày 2");
            Assert.AreEqual(1, s.shop.tickets.Count, "ngày 2: vé chọn tướng");
            Assert.AreEqual(2, Shop.TicketRarity(s.shop.tickets[0]), "vé Hiếm");
            Assert.IsNull(Shop.ClaimDay(s, d, "starter3", T0 + D, new Rng(1)));
            Assert.NotNull(Shop.ClaimDay(s, d, "starter3", T0 + 5 * D, new Rng(1)), "ngày 3 (vắng vài ngày vẫn nhận tiếp)");
            Assert.IsFalse(Shop.DayClaimable(s, d, "starter3", T0 + 9 * D), "hết 3 ngày");
        }

        [Test]
        public void Trung_NoDungBac_CoLucLenBac()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            Assert.IsEmpty(c.Validate(), "cấu hình cửa hàng hợp lệ");
            var s = New(d);
            var rng = new Rng(7);
            const int N = 4000;
            for (int tier = 0; tier < Eggs.Tiers; tier++)
            {
                int up = 0;
                foreach (var h in Eggs.Open(s, d, tier, N, false, T0, rng))
                {
                    Assert.IsTrue(h.tier == tier || h.tier == tier + 1, "chỉ nở đúng bậc hoặc lên một bậc");
                    Assert.AreEqual((Rarity)h.tier, d.Hero(h.reward.hero).rarity, "tướng đúng bậc trứng sau khi nở");
                    var def = c.Egg(h.tier);
                    Assert.That(h.reward.n, Is.InRange(def.min, def.max));
                    if (h.Up) up++;
                }
                Assert.AreEqual(c.Egg(tier).up, up / (double)N, 0.02, "tỉ lệ lên bậc " + tier);
            }
        }

        [Test]
        public void Trung_NoTuTui_RaManh()
        {
            var d = TestData.Load();
            var s = New(d);
            s.shop = s.shop ?? new ShopState();
            s.shop.AddItem(Eggs.Key(3), 3);
            var got = Eggs.Open(s, d, 3, 5, true, T0, new Rng(3));
            Assert.AreEqual(3, got.Count, "túi có 3 thì nở 3");
            Assert.AreEqual(0, s.shop.Item(Eggs.Key(3)));
            Assert.IsTrue(got.All(h => h.reward.k == RewardKind.Shards && h.reward.n > 0 && h.reward.res != null));
            StringAssert.Contains(c(d).Egg(4).Name, Eggs.OddsText(d, T0));
        }

        static ShopConfig c(GameData d) => d.Cfg.shop;

        [Test]
        public void Trung_RuongCuDoiThanhTrung()
        {
            var d = TestData.Load();
            // bản lưu cũ còn Rương Tướng / Rương Tướng Vàng trong túi
            var o = new Dictionary<string, object> { ["items"] = new Dictionary<string, object> { [Shop.HeroChest] = 4.0, [Shop.GoldChest] = 2.0 } };
            var st = Shop.Read(o);
            Assert.AreEqual(4, st.Item(Eggs.Key(1)), "Rương Tướng → Trứng Khá");
            Assert.AreEqual(2, st.Item(Eggs.Key(3)), "Rương Tướng Vàng → Trứng Sử thi");
            Assert.AreEqual(0, st.Item(Shop.HeroChest));
            // món cũ trong ưu đãi đang mở cũng trao thành trứng
            var s = New(d);
            var got = Shop.Grant(s, d, new List<ShopItem> { new ShopItem { k = Shop.GoldChest, n = 1 } }, T0, new Rng(1));
            Assert.AreEqual(RewardKind.Egg, got[0].k);
            Assert.AreEqual(1, s.shop.Item(Eggs.Key(3)));
            Assert.Greater(Shop.Value(d.Cfg.shop, d, new ShopItem { k = Shop.HeroChest, n = 1 }), 0, "giá trị món cũ tính như trứng");
        }

        [Test]
        public void VeChonTuong_SauTuong_NhanDuMoKhoa()
        {
            var d = TestData.Load();
            var s = New(d);
            Shop.Grant(s, d, new List<ShopItem> { new ShopItem { k = Shop.Ticket, n = 1, r = 2 } }, T0, new Rng(1));
            var choices = Shop.TicketChoicesOf(s, d, s.shop.tickets[0], T0);
            Assert.AreEqual(d.Cfg.shop.ticketChoices, choices.Count);
            Assert.IsTrue(choices.All(h => (int)d.Hero(h).rarity <= 2), "vé Hiếm: chỉ tướng tới Hiếm");
            var pick = choices.First(h => !s.Hero(h).owned);
            var r = Shop.UseTicket(s, d, false, 0, pick, T0, new Rng(1));
            Assert.NotNull(r);
            Assert.IsTrue(s.Hero(pick).owned, "đủ mảnh mở khoá");
            Assert.AreEqual(0, s.shop.tickets.Count);
            // vé theo hệ (Gói Đảo Mới)
            Shop.Grant(s, d, new List<ShopItem> { new ShopItem { k = Shop.Ticket, n = 1, r = 3, h = "e:hoa" } }, T0, new Rng(1));
            Assert.IsTrue(Shop.TicketChoicesOf(s, d, s.shop.tickets[0], T0).All(h => d.Hero(h).elem == Elem.Hoa));
        }

        [Test]
        public void LoBi_DapXong_PhaiChoGapDays()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            for (int i = 0; i < 400; i++) Shop.PiggyAdd(s, c, 10);
            Assert.IsTrue(Shop.PiggyCanBreak(s, c, T0));
            Assert.NotNull(Shop.BuyPack(s, d, "piggy", T0, new Rng(1)));
            for (int i = 0; i < 400; i++) Shop.PiggyAdd(s, c, 10);
            Assert.IsTrue(Shop.PiggyFull(s, c));
            Assert.IsFalse(Shop.PiggyCanBreak(s, c, T0 + H), "vừa đập: phải chờ");
            Assert.IsNull(Shop.BuyPack(s, d, "piggy", T0 + H, new Rng(1)));
            Assert.Greater(Shop.PiggyWait(s, c, T0 + H), 0);
            Assert.IsTrue(Shop.PiggyCanBreak(s, c, T0 + c.piggy.gapDays * D + H));
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var s2));
            Assert.AreEqual(s.shop.piggyAt, s2.shop.piggyAt, "bản lưu giữ mốc đập");
        }

        [Test]
        public void BoQuangCao_TraoNgay_CoTranMoiNgay()
        {
            var d = TestData.Load();
            var s = New(d);
            int day = Shop.Today(T0), lim = d.Cfg.ads.noAdsInstant;
            Assert.Greater(lim, 0);
            Assert.IsFalse(AdGate.UseInstant(s, d.Cfg, day), "chưa mua Bỏ quảng cáo");
            AdGate.Buy(s, d.Cfg, "no_ads", T0);
            for (int i = 0; i < lim; i++) Assert.IsTrue(AdGate.UseInstant(s, d.Cfg, day));
            Assert.IsFalse(AdGate.UseInstant(s, d.Cfg, day), "hết lượt trao ngay hôm nay: xem quảng cáo như thường");
            Assert.AreEqual(0, AdGate.InstantLeft(s, d.Cfg, day));
            Assert.IsTrue(AdGate.UseInstant(s, d.Cfg, day + 1), "ngày mới có lại");
        }

        [Test]
        public void TiepSuc_ThaBi_ChiTinhKhiDuLenMotCap()
        {
            var d = TestData.Load();
            var s = New(d);
            s.level = 100;
            s.exp = 0;
            s.balls = 25;
            Assert.IsNull(Offers.FreeFix(s, d), "25 bi ở cấp 100 không đủ lên cấp: không coi là còn cách miễn phí");
            s.balls = (int)(Progress.ExpToNext(100, d.Cfg) / Offers.ExpPerBall) + 5;
            Assert.IsNotNull(Offers.FreeFix(s, d));
        }

        [Test]
        public void ThieuCap_TinhSoCapVaSoBiCanTha()
        {
            var d = TestData.Load();
            var s = New(d);
            var st = d.Stages.First(x => x.enemies.Max(e => e.level) >= 60);
            int foe = st.enemies.Max(e => e.level);
            s.level = foe - 4;
            s.exp = 0;
            var g = Offers.GapTo(s, d, st);
            Assert.AreEqual(foe, g.foe);
            Assert.AreEqual(4, g.gap);
            double exp = 0;
            for (int lv = s.level; lv < foe; lv++) exp += Progress.ExpToNext(lv, d.Cfg);
            Assert.GreaterOrEqual(g.balls, exp / Offers.ExpPerBall, "làm tròn lên");
            Assert.LessOrEqual(g.balls, exp / Offers.ExpPerBall * 1.1, "lệch không quá 10%");
            s.level = foe;
            Assert.AreEqual(0, Offers.GapTo(s, d, st).gap, "ngang cấp địch: không thiếu");
            Assert.AreEqual(0, Offers.GapTo(s, d, st).balls);
            Assert.AreEqual(0, Offers.GapTo(s, d, null).gap);
        }

        [Test]
        public void TiepSuc_DangThieuCap_ChuYeuLaBi()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var st = d.Stages.First(x => x.enemies.Max(e => e.level) >= 60);
            double BallShare(int level)
            {
                var s = New(d);
                s.level = level;
                s.shop = new ShopState { installAt = T0 - 10 * D, lastSeen = T0 - H, sessions = 5 };
                s.shop.offers.lossStage = st.id;
                var o = Offers.Build(s, d, "relief", null, T0, new Rng(1));
                Assert.NotNull(o);
                double all = o.items.Sum(it => Shop.Value(c, d, it)), balls = o.items.Where(it => it.k == "balls").Sum(it => Shop.Value(c, d, it));
                return balls / all;
            }
            int foe = st.enemies.Max(e => e.level);
            Assert.Greater(BallShare(foe - 10), 0.7, "thiếu cấp: trên 70% giá trị gói là bi");
            Assert.Less(BallShare(foe + 5), BallShare(foe - 10), "đủ cấp: gói nghiêng về mảnh, thẻ của tướng chủ lực");
        }

        [Test]
        public void VuotMoc_QuaMoc3_ChaoTuongDiTruoc3Moc_TronBo()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            s.level = 40; // đã mở bậc Bạc (cấp 30), chưa mở bậc Vàng (cấp 95)
            s.shop = new ShopState { installAt = T0 - 10 * D, lastSeen = T0 - H, sessions = 5 };
            var ms = Offers.MilestoneStages(d, Elem.Thuy);
            Assert.AreEqual(10, ms.Count, "mỗi đảo 10 mốc");
            List<Popup> Win(StageDef st)
            {
                s.clears[st.id] = (s.clears.TryGetValue(st.id, out var n) ? n : 0) + 1;
                return Offers.On(s, d, new OfferCtx { e = OfferEvent.BattleWon, stage = st.id }, T0, new Rng(1));
            }
            Assert.IsFalse(Win(ms[1]).Any(p => p.key == "jump"), "mốc 2: chưa chào");
            var pops = Win(ms[2]).Where(p => p.key == "jump").ToList();
            Assert.AreEqual(1, pops.Count, "lần đầu qua mốc 3: chào Gói Vượt Mốc");
            var o = Shop.FindOffer(s, pops[0].id);
            string hero = Teams.StageLead(ms[5], d).hero;
            Assert.AreEqual(hero, o.hero, "tướng mốc 6 của đảo");
            Assert.GreaterOrEqual(o.price, c.caps.jumpPrices[0] - 0.001);
            Assert.GreaterOrEqual(Shop.OfferMult(s, d, o), 4.9, "giá trị khoảng ×5 trở lên");
            Assert.IsFalse(Win(ms[2]).Any(p => p.key == "jump"), "đánh lại ải mốc: không chào nữa");
            Assert.IsFalse(Win(ms[3]).Any(p => p.key == "jump"), "đang có một gói mở: không chồng gói");
            int evo0 = s.evoStones;
            Assert.NotNull(Shop.BuyOffer(s, d, o.uid, T0, new Rng(2)));
            Assert.IsTrue(s.Hero(hero).owned, "mua xong có tướng");
            // dùng hết đồ trong gói: lên sao / tiến hóa tới hết bậc Bạc (cấp 40 chưa cho lên Vàng)
            for (int i = 0; i < 40 && (Progress.StarUp(s, d, hero) || Progress.Evolve(s, d, hero)); i++) { }
            var path = Progress.PathCost(d.Cfg, d.Hero(hero), 1, s.level, c.caps.jumpMaxStar);
            Assert.AreEqual(path.to, s.Hero(hero).star, "đủ mảnh và đá để lên tới mức cấp người chơi cho phép");
            Assert.Greater(path.to, 5, "cấp 40: sang được bậc Bạc");
            Assert.GreaterOrEqual(s.evoStones, evo0, "đá của gói vừa đủ, không ăn vào đá người chơi đang có");
            // qua mốc cao: tướng chào là mốc cuối; đã có tướng đó thì thôi
            Assert.AreEqual(Teams.StageLead(ms[9], d).hero, Offers.JumpHero(s, d, ms[7]));
            s.Hero(Teams.StageLead(ms[9], d).hero).owned = true;
            Assert.IsNull(Offers.JumpHero(s, d, ms[7]));
            Assert.IsNull(Offers.JumpHero(s, d, ms[9]), "mốc cuối: không còn tướng đi trước");
        }

        [Test]
        public void VuotMoc_LucChienTuongTrongGoi_HonTuongDangCo()
        {
            var d = TestData.Load();
            var s = New(d);
            s.level = 40;
            var ms = Offers.MilestoneStages(d, Elem.Thuy);
            string hero = Teams.StageLead(ms[5], d).hero;
            var pw = Offers.JumpPower(s, d, hero);
            Assert.Greater(pw.best, 0, "người chơi có tướng khởi đầu");
            Assert.Greater(pw.pack, pw.best, "tướng mốc 6 lên hết bậc Bạc mạnh hơn tướng khởi đầu 1 sao cùng cấp");
            Assert.AreEqual((0, 0), Offers.JumpPower(s, d, null));
        }

        [Test]
        public void VuotMoc_CapThapGoiRe_CapCaoGoiDat()
        {
            var d = TestData.Load();
            var ms = Offers.MilestoneStages(d, Elem.Thuy);
            double Price(int level, int moc)
            {
                var s = New(d);
                s.level = level;
                s.shop = new ShopState { installAt = T0 - 10 * D, lastSeen = T0 - H, sessions = 5 };
                var o = Offers.Build(s, d, "jump", Teams.StageLead(ms[moc - 1], d).hero, T0, new Rng(1));
                Assert.NotNull(o);
                return o.price;
            }
            Assert.LessOrEqual(Price(20, 6), 9.99, "mới chơi: gói tướng mốc 6 rẻ");
            Assert.Greater(Price(100, 10), Price(20, 6), "mốc 10 ở cấp cao đắt hơn hẳn");
            Assert.GreaterOrEqual(Price(100, 10), 19.99);
        }

        [Test]
        public void NapDau3Bac_MuaMotGoi_HaiGoiKiaDong()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var tiers = c.packs.Where(p => p.group == "launch").OrderBy(p => p.price).ToList();
            Assert.AreEqual(3, tiers.Count, "ba bậc Khởi Hành");
            Assert.AreEqual("launch", tiers[0].id, "bậc rẻ nhất đứng đầu nhóm");
            for (int i = 1; i < tiers.Count; i++)
                Assert.Greater(Shop.PackMult(New(d), d, tiers[i]), Shop.PackMult(New(d), d, tiers[i - 1]), "bậc cao hơn thì hời hơn");
            var s = New(d);
            s.shop = new ShopState { installAt = T0 - 3 * D, lastSeen = T0 - H, sessions = 5 };
            s.shop.offers.done.Add("starter3");
            var pops = Offers.Open(s, d, T0, new Rng(1));
            Assert.IsTrue(pops.Any(p => p.key == "launch"), "ngày 2 trở đi: popup Gói Khởi Hành");
            var live = Shop.Live(s, T0).Where(o => o.pack != null && c.Pack(o.pack).group == "launch").ToList();
            Assert.AreEqual(3, live.Count, "ba gói mở cùng lúc");
            Assert.AreEqual(1, live.Select(o => o.until).Distinct().Count(), "cùng một đồng hồ");
            var mid = live.First(o => o.pack == tiers[1].id);
            Assert.NotNull(Shop.BuyOffer(s, d, mid.uid, T0 + H, new Rng(2)));
            Assert.IsEmpty(Shop.Live(s, T0 + H).Where(o => o.pack != null && c.Pack(o.pack).group == "launch"), "mua một gói: cả nhóm đóng");
            Assert.IsFalse(Shop.CanBuy(s, d, tiers[0], T0 + H));
            Assert.IsFalse(Shop.CanBuy(s, d, tiers[2], T0 + H));
            Assert.IsNull(Shop.BuyPack(s, d, tiers[2].id, T0 + H, new Rng(3)), "không mua bù bậc khác");
        }

        [Test]
        public void LoBi_TichDayDap()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            double cap = Shop.PiggyCap(s, c);
            Assert.AreEqual(c.piggy.cap, cap);
            Assert.IsFalse(Shop.PiggyCanBreak(s, c, T0));
            Assert.IsNull(Shop.BuyPack(s, d, "piggy", T0, new Rng(1)), "chưa đủ 40%");
            bool full = false;
            for (int i = 0; i < 300 && !full; i++) full = Shop.PiggyAdd(s, c, 10);
            Assert.IsTrue(full);
            Assert.AreEqual(cap, s.shop.piggy);
            Assert.IsFalse(Shop.PiggyAdd(s, c, 10), "đầy rồi không báo lại");
            int b0 = s.balls;
            Assert.NotNull(Shop.BuyPack(s, d, "piggy", T0, new Rng(1)));
            Assert.AreEqual(b0 + (int)cap, s.balls);
            Assert.AreEqual(0, s.shop.piggy);
            Assert.Greater(Shop.PiggyCap(s, c), cap, "đập xong sức chứa lần sau lớn hơn");
        }

        [Test]
        public void TheTuan_TheThang_NhanMoiNgay()
        {
            var d = TestData.Load();
            var s = New(d);
            int b0 = s.balls;
            Assert.NotNull(Shop.BuyPack(s, d, "week_card", T0, new Rng(1)));
            Assert.AreEqual(b0 + 300, s.balls, "nhận ngay 300");
            Assert.IsTrue(Shop.CardActive(s, "week", T0 + 6 * D));
            Assert.IsFalse(Shop.CardActive(s, "week", T0 + 8 * D));
            Assert.AreEqual(1.5, Shop.TreeCapMult(s, d.Cfg.shop, T0 + D), 1e-9);
            Assert.NotNull(Shop.ClaimCard(s, d, "week", T0, new Rng(1)));
            Assert.IsNull(Shop.ClaimCard(s, d, "week", T0 + H, new Rng(1)), "mỗi ngày một lần");
            Assert.NotNull(Shop.ClaimCard(s, d, "week", T0 + D, new Rng(1)));
            // tháng = Thẻ Phiêu Lưu cũ + quà
            Assert.NotNull(Shop.BuyPack(s, d, "adventure_pass", T0, new Rng(1)));
            Assert.IsTrue(AdGate.PassActive(s, T0 + 29 * D));
            Assert.AreEqual(1, s.shop.Item(Eggs.Key(3)), "Thẻ Phiêu Lưu: 1 Trứng Sử thi");
            Assert.IsTrue(Shop.UseAdSkip(s, d.Cfg.shop, T0), "1 lượt quảng cáo trao ngay mỗi ngày");
            Assert.IsFalse(Shop.UseAdSkip(s, d.Cfg.shop, T0 + H));
            Assert.IsTrue(Shop.UseAdSkip(s, d.Cfg.shop, T0 + D));
        }

        [Test]
        public void Chuoi_LanLuot_MienPhiXenTraTien()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            Shop.ChainStart(s, c, T0);
            Assert.IsTrue(Shop.ChainLive(s, T0 + H));
            Assert.IsNull(Shop.ChainTake(s, d, 1, true, T0, new Rng(1)), "chưa tới ô 2");
            Assert.IsNull(Shop.ChainTake(s, d, 0, true, T0, new Rng(1)), "ô 1 miễn phí, không mua");
            Assert.NotNull(Shop.ChainTake(s, d, 0, false, T0, new Rng(1)));
            Assert.IsNull(Shop.ChainTake(s, d, 1, false, T0, new Rng(1)), "ô 2 trả tiền");
            Assert.NotNull(Shop.ChainTake(s, d, 1, true, T0, new Rng(1)));
            Assert.AreEqual(2, s.shop.chainStep);
            Assert.IsFalse(Shop.ChainLive(s, T0 + c.chainHours * H + 1));
        }

        [Test]
        public void Quy_MocCap()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            s.level = 12;
            Assert.IsTrue(Shop.FundClaimable(s, c, 0, false), "hàng miễn phí cấp 10");
            Assert.IsFalse(Shop.FundClaimable(s, c, 0, true), "chưa mua quỹ");
            Assert.IsFalse(Shop.FundClaimable(s, c, 1, false), "chưa cấp 15");
            Assert.NotNull(Shop.BuyPack(s, d, "fund", T0, new Rng(1)));
            Assert.NotNull(Shop.FundClaim(s, d, 0, true, T0, new Rng(1)));
            Assert.IsNull(Shop.FundClaim(s, d, 0, true, T0, new Rng(1)));
            Assert.IsNull(Shop.BuyPack(s, d, "fund", T0, new Rng(1)), "mua một lần");
        }

        [Test]
        public void MocQuangCao_VaQuaNgay()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            for (int i = 0; i < 3; i++) Shop.OnAd(s, T0);
            Assert.IsTrue(Shop.AdMilestoneReady(s, c, 0, T0));
            Assert.IsFalse(Shop.AdMilestoneReady(s, c, 1, T0));
            Assert.NotNull(Shop.ClaimAdMilestone(s, d, 0, T0, new Rng(1)));
            Assert.IsFalse(Shop.AdMilestoneReady(s, c, 0, T0));
            Assert.AreEqual(0, Shop.AdsToday(s, T0 + D), "qua ngày đếm lại");
            int b0 = s.balls;
            Assert.NotNull(Shop.ClaimGift(s, d, true, T0, new Rng(1)));
            Assert.AreEqual(b0 + 2 * c.dailyGift[0].n, s.balls, "quà ngày ×2 (quảng cáo)");
            Assert.IsNull(Shop.ClaimGift(s, d, false, T0, new Rng(1)));
        }

        [Test]
        public void ThangGia_LenXuong()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            Assert.AreEqual(0.99, Shop.LadderPrice(s, c, T0), 1e-9);
            Shop.LadderBought(s, c, 0.99, T0);
            Assert.AreEqual(1.99, Shop.LadderPrice(s, c, T0), 1e-9, "mua thì lên một bậc");
            Shop.LadderBought(s, c, 1.99, T0);
            Assert.AreEqual(4.99, Shop.LadderPrice(s, c, T0 + D), 1e-9);
            Assert.AreEqual(1.99, Shop.LadderPrice(s, c, T0 + 8 * D), 1e-9, "7 ngày không mua: xuống một bậc");
            Shop.LadderBought(s, c, 19.99, T0 + 8 * D);
            Assert.AreEqual(9.99, Shop.LadderPrice(s, c, T0 + 8 * D), 1e-9, "mua lớn: gói kế xuống một bậc");
        }

        [Test]
        public void Popup_KhongBanTruocKhiXongHuongDan()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, (long)T0, null); // người chơi mới thật: chưa chọn tướng, hướng dẫn chưa xong
            Assert.IsEmpty(Offers.Open(s, d, T0, new Rng(1)));
            Assert.IsEmpty(Offers.On(s, d, new OfferCtx { e = OfferEvent.BattleLost, stage = 5 }, T0, new Rng(1)).Where(p => !p.free));
        }

        [Test]
        public void Popup_TranVaHomNayKhongHienNua()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            s.shop = new ShopState { installAt = T0 - 10 * D, lastSeen = T0 - H, sessions = 5 };
            for (int i = 0; i < 30; i++) s.balls += 0;
            // vào game nhiều lần: mỗi lần tối đa perOpen popup bán, cả ngày tối đa perDay
            int paid = 0;
            for (int k = 0; k < 10; k++)
            {
                double now = T0 + k * (c.caps.gapMin + 1) * 60000;
                var list = Offers.Open(s, d, now, new Rng((uint)(k + 1)));
                var sell = list.Where(p => !p.free).ToList();
                Assert.LessOrEqual(sell.Count, c.caps.perOpen, "lần " + k);
                foreach (var p in list) Offers.Shown(s, d, p, now);
                foreach (var p in list) Offers.Closed(s, p, false, false, now);
                paid += sell.Count;
            }
            Assert.LessOrEqual(paid, c.caps.perDay, "cả ngày");
            // tích "Hôm nay không hiện nữa": thôi tới hôm sau
            var s2 = New(d);
            s2.shop = new ShopState { installAt = T0 - 10 * D, lastSeen = T0 - H, sessions = 5 };
            Offers.Closed(s2, new Popup { kind = "offer", key = "x" }, false, true, T0);
            Assert.AreEqual(0, Offers.Room(s2, d, T0 + H));
            Assert.Greater(Offers.Room(s2, d, T0 + D), 0);
        }

        [Test]
        public void SauKhiThua_ChiBanKhiHetCachMienPhi()
        {
            var d = TestData.Load();
            var c = d.Cfg.shop;
            var s = New(d);
            s.shop = new ShopState { installAt = T0 - 10 * D, lastSeen = T0 - H, sessions = 5 };
            List<Popup> Lose(bool free, double now) => Offers.On(s, d, new OfferCtx { e = OfferEvent.BattleLost, stage = 42, freeFix = free }, now, new Rng(1));
            Assert.IsEmpty(Lose(false, T0), "thua lần 1");
            Assert.IsEmpty(Lose(false, T0 + 60000), "thua lần 2");
            Assert.IsEmpty(Lose(true, T0 + 120000), "thua lần 3 nhưng còn cách miễn phí");
            var p = Lose(false, T0 + 180000);
            Assert.AreEqual(1, p.Count, "thua lần 4, hết cách miễn phí: Gói Tiếp Sức");
            var o = Shop.FindOffer(s, p[0].id);
            Assert.AreEqual("relief", o.tpl);
            Assert.AreEqual(2 * H, o.until - (T0 + 180000), 1, "mở 2 giờ");
            Assert.Greater(Shop.OfferMult(s, d, o), 3, "giá trị khoảng ×4");
            Assert.IsEmpty(Lose(false, T0 + 240000), "24 giờ mới có gói tiếp sức nữa");
            // thắng ải đó thì đếm lại
            Offers.On(s, d, new OfferCtx { e = OfferEvent.BattleWon, stage = 42 }, T0 + 300000, new Rng(1));
            Assert.AreEqual(0, s.shop.offers.lossStreak);
        }

        [Test]
        public void HetBi_CoPopupCachNhau20Phut()
        {
            var d = TestData.Load();
            var s = New(d);
            var p = Offers.On(s, d, new OfferCtx { e = OfferEvent.OutOfBalls }, T0, new Rng(1));
            Assert.AreEqual(1, p.Count);
            Assert.IsTrue(p[0].first, "lần đầu: chỉ quảng cáo và Cây bi");
            Offers.Shown(s, d, p[0], T0);
            Assert.IsEmpty(Offers.On(s, d, new OfferCtx { e = OfferEvent.OutOfBalls }, T0 + 5 * 60000, new Rng(1)));
            var p2 = Offers.On(s, d, new OfferCtx { e = OfferEvent.OutOfBalls }, T0 + 21 * 60000, new Rng(1));
            Assert.AreEqual(1, p2.Count);
            Assert.IsFalse(p2[0].first);
        }

        [Test]
        public void SapHetBi_PopupGoiBi_SauLanHetBiDau_DongThi24Gio()
        {
            var d = TestData.Load();
            var s = New(d);
            s.balls = 12;
            var low = new OfferCtx { e = OfferEvent.LowBalls };
            Assert.IsFalse(Offers.On(s, d, low, T0, new Rng(1)).Any(p => p.kind == "refill"), "chưa gặp Hết bi lần nào: chưa bán gói bi");
            var out1 = Offers.On(s, d, new OfferCtx { e = OfferEvent.OutOfBalls }, T0, new Rng(1));
            Offers.Shown(s, d, out1[0], T0);
            Offers.Closed(s, out1[0], false, false, T0);
            Assert.IsEmpty(Offers.On(s, d, low, T0 + 5 * 60000, new Rng(1)), "chung nhịp 20 phút với Hết bi");

            double t = T0 + 21 * 60000;
            var p = Offers.On(s, d, low, t, new Rng(1));
            Assert.AreEqual(1, p.Count);
            Assert.AreEqual("refill", p[0].kind);
            Assert.IsTrue(p[0].warn, "Sắp hết bi");
            Assert.IsFalse(p[0].free, "popup bán: tính vào trần");
            Assert.AreEqual(12, p[0].ballsMax, "bi nhiều lên trước lúc hiện thì bỏ");
            Offers.Shown(s, d, p[0], t);
            Offers.Closed(s, p[0], false, false, t);
            Assert.IsEmpty(Offers.On(s, d, low, t + 30 * 60000, new Rng(1)).Where(q => q.kind == "refill"), "đóng thì 24 giờ mới bật lại");
            Assert.AreEqual(1, Offers.On(s, d, new OfferCtx { e = OfferEvent.OutOfBalls }, t + 30 * 60000, new Rng(1)).Count, "hết hẳn bi vẫn có popup Hết bi");
            Assert.AreEqual(1, Offers.On(s, d, low, t + 25 * H, new Rng(1)).Count(q => q.kind == "refill"), "qua 24 giờ bật lại");
        }

        [Test]
        public void SapHetBi_SauDotTha_KhongTungUuDaiBatNgo()
        {
            var d = TestData.Load();
            var s = New(d);
            s.balls = 12;
            // chưa gặp Hết bi nên không có popup gói bi; vừa thả xong (không phải lúc vào máy) thì không tung Ưu Đãi Bất Ngờ
            for (uint i = 0; i < 20; i++)
                Assert.IsEmpty(Offers.On(s, d, new OfferCtx { e = OfferEvent.LowBalls }, T0 + i * 7 * H, new Rng(i + 1)));
        }

        [Test]
        public void QuaNhapMon_PopupTuPhien2_DongHoTuLanPopup()
        {
            var d = TestData.Load();
            var s = New(d);
            var first = Offers.Open(s, d, T0, new Rng(1));
            Assert.IsFalse(first.Any(p => p.kind == "offer" && Shop.FindOffer(s, p.id)?.pack == "starter3"), "phiên 1 chưa popup");
            var o = s.shop.offers.active.Find(x => x.pack == "starter3");
            Assert.NotNull(o, "đã có trong danh sách ưu đãi");
            Assert.AreEqual(0, o.until, "chưa chạy đồng hồ");
            var second = Offers.Open(s, d, T0 + 40 * 60000, new Rng(1));
            var pop = second.FirstOrDefault(p => p.id == o.uid);
            Assert.NotNull(pop, "phiên 2 popup");
            Offers.Shown(s, d, pop, T0 + 40 * 60000);
            Assert.AreEqual(72 * H, o.until - (T0 + 40 * 60000), 1);
            Assert.NotNull(Shop.BuyOffer(s, d, o.uid, T0 + H, new Rng(1)));
            Assert.AreEqual(1, Shop.Bought(s, "starter3"));
        }

        [Test]
        public void BanLuu_GiuNguyenCuaHang()
        {
            var d = TestData.Load();
            var s = New(d);
            Shop.BuyPack(s, d, "week_card", T0, new Rng(1));
            Shop.BuyPack(s, d, "starter3", T0, new Rng(1));
            Shop.PiggyAdd(s, d.Cfg.shop, 123);
            Offers.Build(s, d, "flash", null, T0, new Rng(1));
            Shop.OnAd(s, T0);
            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var r));
            Assert.AreEqual(json, SaveCodec.Write(r), "đọc rồi ghi lại y hệt");
            Assert.AreEqual(123, r.shop.piggy);
            Assert.IsTrue(Shop.CardActive(r, "week", T0 + D));
            Assert.AreEqual(1, r.shop.offers.active.Count(o => o.tpl == "flash"));
        }
    }
}
