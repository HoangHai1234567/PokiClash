// Hướng dẫn người mới (Core/Tutorial, GD_Claude/25_FTUE.md): cờ trong bản lưu, bản lưu cũ coi như xong, trận hướng dẫn (thẻ rút sẵn,
// khoá thua ngầm), máy bi lần đầu (kết quả ép), rương đầu, đảo tan mây theo bước, sảnh hiện dần, cây bi đầu có sẵn bi.
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class TutorialTests
    {
        static GameData D => TestData.Load();

        [TearDown]
        public void Back() => Tutorial.Off = false;

        // người chơi mới thật: game tạo bản lưu chưa chọn tướng
        static SaveData Fresh(string starter = "ti_tach")
        {
            var s = SaveData.New(D, 0, null);
            if (starter != null)
            {
                s.intro = true;
                s.ChooseStarter(starter);
            }
            return s;
        }

        [Test]
        public void BanLuuMoi_ChuaXongBuocNao_DanhDauThiXong()
        {
            var s = Fresh();
            Assert.IsFalse(Tutorial.IsLegacy(s));
            Assert.IsFalse(Tutorial.Done(s, Tutorial.Intro));
            Assert.IsFalse(Tutorial.CoreDone(s));
            Tutorial.Mark(s, Tutorial.Intro);
            Tutorial.Mark(s, Tutorial.Intro);
            Assert.IsTrue(Tutorial.Done(s, Tutorial.Intro));
            Assert.IsFalse(Tutorial.Done(s, Tutorial.Island));
            Assert.AreEqual(Tutorial.Intro, s.extra["ftue"], "đánh dấu hai lần không lặp mã");
            // qua bản lưu
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), D, out var back));
            Assert.IsTrue(Tutorial.Done(back, Tutorial.Intro));
            Assert.IsFalse(Tutorial.Done(back, Tutorial.Island));
        }

        [Test]
        public void BanLuuCu_DaChoi_CoiNhuXongHet()
        {
            var s = SaveData.New(D, 0); // test, máy tự chơi: không có cờ
            s.zones[(int)Elem.Thuy] = 5;
            Assert.IsTrue(Tutorial.IsLegacy(s));
            Assert.IsTrue(Tutorial.CoreDone(s));
            Assert.IsTrue(Tutorial.Done(s, Tutorial.StatusTip(StatusId.Burn)));
            foreach (Tutorial.HubPart p in System.Enum.GetValues(typeof(Tutorial.HubPart)))
                Assert.IsTrue(Tutorial.Shows(s, D, p, 0), $"bản cũ hiện đủ: {p}");
            Assert.IsNull(Tutorial.NextUnlock(s, D), "bản cũ không báo mở tính năng");
        }

        [Test]
        public void TatHuongDan_MoiBuocCoiNhuXong()
        {
            var s = Fresh();
            Tutorial.Off = true;
            Assert.IsTrue(Tutorial.Done(s, Tutorial.Balls));
            Assert.IsNull(Tutorial.BattleFor(s, D, D.ZoneStages(Elem.Thuy).First(st => st.idx == 1)));
        }

        [Test]
        public void TranHuongDan_TranGuong_ThenTranKhacHe()
        {
            var s = Fresh("ti_tach");
            var thuy1 = D.ZoneStages(Elem.Thuy).First(st => st.idx == 1);
            var hoa1 = D.ZoneStages(Elem.Hoa).First(st => st.idx == 1);
            Assert.AreEqual(Elem.Hoa, Tutorial.CounterIsland(s, D), "Thủy khắc Hỏa");
            var first = Tutorial.BattleFor(s, D, thuy1);
            Assert.IsNotNull(first, "trận gương có kịch bản");
            CollectionAssert.AreEqual(new[] { "nem_da", "mai_vuot", "bang_gac" }, first.NextOffer(D));
            Assert.IsNull(first.NextOffer(D), "lần rút sau rút thường");
            Assert.IsNull(Tutorial.BattleFor(s, D, D.ZoneStages(Elem.Thuy).First(st => st.idx == 2)), "ải 2 không có kịch bản");
            Tutorial.Mark(s, Tutorial.Balls);
            Assert.IsNull(Tutorial.BattleFor(s, D, thuy1), "trận gương đã xong");
            var second = Tutorial.BattleFor(s, D, hoa1);
            Assert.IsNotNull(second, "trận 2 ở đảo mình khắc có kịch bản");
            for (int i = 0; i < 5; i++) Assert.IsNull(second.NextOffer(D));
            Assert.Contains("gam_gu", second.NextOffer(D), "lượt 2 có Gầm Gừ để kịp đầy nộ");
            Tutorial.Mark(s, Tutorial.Shards);
            Assert.IsNull(Tutorial.BattleFor(s, D, hoa1));
        }

        [Test]
        public void KhoaThuaNgam_MauKhongDuoiSan()
        {
            // người chơi cấp 1 đấu địch cấp rất cao: trận thường thua, trận có kịch bản thì máu phe mình không dưới 20%
            var s = Fresh("ti_tach");
            var st = D.ZoneStages(Elem.Thuy).First(x => x.idx == 1);
            var strong = new StageDef
            {
                id = st.id, zone = st.zone, idx = st.idx, name = st.name, kind = st.kind,
                enemies = new List<StageEnemy> { new StageEnemy { hero = st.enemies[0].hero, level = 60 } },
            };
            for (int seed = 1; seed <= 5; seed++)
            {
                var plain = Battle.Create(D, Teams.Player(s, s.team, D), Teams.Enemy(strong, D), (uint)seed, 1, 60);
                BattleSim.Run(plain);
                Assert.AreEqual(1, plain.winner, "không kịch bản: thua");

                var b = Battle.Create(D, Teams.Player(s, s.team, D), Teams.Enemy(strong, D), (uint)seed, 1, 60);
                b.script = new BattleScript { floor = Tutorial.LoseFloor };
                BattleSim.Run(b);
                var me = b.sides[0].fighters[0];
                Assert.IsFalse(me.dead, "kịch bản: không gục");
                Assert.GreaterOrEqual(me.hp, System.Math.Ceiling(me.maxHp * Tutorial.LoseFloor) - 0.001, "máu không dưới sàn");
            }
        }

        [Test]
        public void MayBiLanDau_KetQuaEp_LenCap2_RuongDau2BanSaoChieu()
        {
            var cfg = D.Cfg;
            var board = new Board(7) { odds = cfg.odds };
            foreach (var o in Tutorial.MachineOutcomes) board.forced.Enqueue(o);
            var got = new List<int>();
            for (int i = 0; i < Tutorial.MachineOutcomes.Length; i++) got.Add(board.Launch(1).target);
            CollectionAssert.AreEqual(Tutorial.MachineOutcomes, got);
            Assert.AreEqual(0, board.forced.Count);
            Assert.GreaterOrEqual(board.Launch(1).target, 0, "hết hàng ép thì theo bảng tỉ lệ");

            // EXP của 5 bi đầu đủ lên cấp 2
            var s = Fresh("ti_tach");
            int exp = Tutorial.MachineOutcomes.Take(5).Sum(o => Pachinko.Exp(Board.SlotLayout[o]));
            Progress.AddExp(s, exp, cfg);
            Assert.AreEqual(2, s.level, $"5 bi đầu {exp} EXP lên cấp 2");
            Assert.AreEqual(Board.SlotLayout.Length, Tutorial.MachineOutcomes[5], "bi thứ 6 vào cốc thẻ");
            Assert.AreEqual(SlotKind.ChestSilver, Board.GiftReward, "cốc thẻ ra rương bạc");

            var h = D.Hero("ti_tach");
            var first = Tutorial.FirstChest(s, D);
            Assert.AreEqual(2, first.Count);
            Assert.IsTrue(first.All(r => r.k == RewardKind.Card && r.drop.hero == h.id && r.drop.slot == CardSlot.Skill));
            Assert.AreEqual(2, s.Hero(h.id).skill.copies);
            Assert.IsTrue(Progress.CanUpCard(s, cfg, h.id, CardSlot.Skill), "đủ bản sao nâng Chiêu");
            Assert.IsNull(Tutorial.FirstChest(s, D), "chỉ rương đầu");
        }

        // lỗi 2026-11-23: lớp phủ lỡ cú chạm nút Lên cấp thì cờ C10 không có, sảnh ép vào màn Tướng mãi khi còn đủ bản sao
        [Test]
        public void NangChieu_DaLenCapMaThieuCo_KhongEpNua()
        {
            var cfg = D.Cfg;
            var s = Fresh("ti_tach");
            s.zones[(int)Elem.Thuy] = 1;
            Assert.IsFalse(Tutorial.UpCardDue(s, D), "chưa có bản sao: không ép");
            var c = s.Hero("ti_tach").Card(CardSlot.Skill);
            c.copies = 2;
            Assert.IsTrue(Tutorial.UpCardDue(s, D), "đủ 2 bản sao, Chiêu cấp 1: ép nâng");
            c.copies = 2 + Progress.CardReq(cfg, 2);
            Assert.IsTrue(Progress.UpCard(s, cfg, "ti_tach", CardSlot.Skill));
            Assert.IsTrue(Progress.CanUpCard(s, cfg, "ti_tach", CardSlot.Skill), "còn đủ bản sao nâng tiếp");
            Assert.IsFalse(Tutorial.Done(s, Tutorial.UpCard), "giả lập lớp phủ lỡ cú chạm: chưa có cờ");
            Assert.IsFalse(Tutorial.UpCardDue(s, D), "Chiêu đã cấp 2: không ép vào màn Tướng nữa");
            Tutorial.Off = true;
            Assert.IsFalse(Tutorial.UpCardDue(s, D), "tắt hướng dẫn: không ép");
        }

        [Test]
        public void DaoTanMay_TheoBuoc()
        {
            var s = Fresh("thach_nhan");
            Assert.AreEqual(HubIslands.Bit(Elem.Tho), HubIslands.Open(s, D), "chọn tướng: tan đảo cùng hệ");
            s.zones[(int)Elem.Tho] = 1;
            Assert.AreEqual(HubIslands.Bit(Elem.Tho), HubIslands.Open(s, D), "thắng ải đầu: chờ xong máy bi, nâng Chiêu");
            Tutorial.Mark(s, Tutorial.UpCard);
            Assert.AreEqual(HubIslands.All, HubIslands.Open(s, D));
        }

        [Test]
        public void SanhHienDan()
        {
            var s = Fresh();
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Machine, 0));
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Heroes, 0));
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Next, 0));
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Afk, 0));
            Tutorial.Mark(s, Tutorial.Balls);
            Assert.IsTrue(Tutorial.Shows(s, D, Tutorial.HubPart.Machine, 0));
            Tutorial.Mark(s, Tutorial.NoBalls);
            Assert.IsTrue(Tutorial.Shows(s, D, Tutorial.HubPart.Heroes, 0));
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Next, 0));
            Tutorial.Mark(s, Tutorial.Free);
            Assert.IsTrue(Tutorial.Shows(s, D, Tutorial.HubPart.Next, 0));
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Cave, 0), "Hang chỉ hiện từ cấp 20");
            s.level = 20;
            Assert.IsTrue(Tutorial.Shows(s, D, Tutorial.HubPart.Cave, 0));
        }

        [Test]
        public void CayBiDau_CoSan10Bi_MotLan()
        {
            var s = Fresh();
            s.zones[(int)Elem.Thuy] = 1;
            Tutorial.SeedTree(s, D.Cfg, 1000);
            Assert.AreEqual(0, Trees.Stock(s, D.Cfg, 1000), "chưa mở Nhà: chưa có cây");
            TreesTests.OpenHome(s, D); // cây bi mở cùng Nhà (2026-11-23)
            Tutorial.SeedTree(s, D.Cfg, 1000);
            Assert.AreEqual(Tutorial.TreeSeedBalls, Trees.Stock(s, D.Cfg, 1000));
            Trees.Harvest(s, D.Cfg, 1000);
            Tutorial.SeedTree(s, D.Cfg, 1000);
            Assert.AreEqual(0, Trees.Stock(s, D.Cfg, 1000), "chỉ lần đầu");
        }

        [Test]
        public void MoTinhNang_SauChuoiBatBuoc_TheoThuTu()
        {
            var s = Fresh();
            s.level = 30;
            s.zones[(int)Elem.Thuy] = 1; // cây 2 mở ở cấp 30; cây bi mở cùng Nhà (2026-11-23)
            Assert.IsNull(Tutorial.NextUnlock(s, D), "chưa xong chuỗi bắt buộc thì chưa báo");
            Tutorial.Mark(s, Tutorial.Free);
            var u = Tutorial.NextUnlock(s, D);
            Assert.AreEqual("h_cave", u.id, "cấp 30: Hang trước");
            Tutorial.Mark(s, u.id);
            Assert.IsNull(Tutorial.NextUnlock(s, D), "chưa có Nhà thì chưa có cây bi");
            TreesTests.OpenHome(s, D);
            Assert.AreEqual("g1", Tutorial.NextUnlock(s, D)?.id, "mở Nhà (cây bi đến cùng Nhà)");
            Tutorial.Mark(s, "g1");
            // cây bi 2, 3... đã mở theo cấp (balance.json trees.unlockLevels), mỗi lần vào sảnh báo một cái
            for (int k = 2; k <= Trees.Open(s, D.Cfg); k++)
            {
                Assert.AreEqual("h_tree" + k, Tutorial.NextUnlock(s, D)?.id, $"rồi cây bi thứ {k}");
                Tutorial.Mark(s, "h_tree" + k);
            }
            Assert.IsNull(Tutorial.NextUnlock(s, D));
            Assert.IsTrue(Tutorial.Pages(D.Cfg).All(p => !string.IsNullOrEmpty(p.title) && !string.IsNullOrEmpty(p.text)));
        }

        // sau trận 2 (người dùng 2026-11-24): Sổ thẻ hiện ngay; Nhà mở sau 2 ải (không cần 3 tướng), nút Nhà hiện từ lúc báo "Nhà đã mở";
        // Cửa hàng hiện khi đã đi hết Nhà (giới thiệu công trình, hái Cây bi đầu); đặt Cây bi thuộc chuỗi bắt buộc
        [Test]
        public void SauTran2_SoThe_Nha_CuaHang_TheoThuTu()
        {
            var s = Fresh();
            s.zones[(int)Tutorial.Starter(s, D).elem] = 1; // trận 1
            Assert.IsFalse(Home.Open(s, D.Cfg), "1 ải: Nhà chưa mở");
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Cards, 0));
            s.zones[(int)Tutorial.CounterIsland(s, D)] = 1; // trận 2
            Assert.IsTrue(Tutorial.Battle2Won(s, D));
            Assert.AreEqual(1, s.heroes.Values.Count(h => h.owned), "chỉ tướng đồng hành");
            Assert.IsTrue(Home.Open(s, D.Cfg), "2 ải: Nhà mở dù mới 1 tướng");
            Assert.IsTrue(Trees.Open(s, D.Cfg) > 0, "cây bi đến cùng Nhà");
            Assert.IsTrue(Tutorial.Shows(s, D, Tutorial.HubPart.Cards, 0), "Sổ thẻ ngay sau trận 2");
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Home, 0), "nút Nhà chờ lời báo");
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Shop, 0));
            Tutorial.MarkAll(s, Tutorial.CardsGo, Tutorial.HomeNews, Tutorial.HomeGo);
            Assert.IsTrue(Tutorial.Shows(s, D, Tutorial.HubPart.Home, 0));
            Assert.IsFalse(Tutorial.Shows(s, D, Tutorial.HubPart.Shop, 0), "chưa đi hết Nhà");
            Tutorial.MarkAll(s, Tutorial.HomeMain, Tutorial.HomeFarm, Tutorial.HomeWood);
            Assert.IsFalse(Tutorial.HomeToured(s), "còn hái Cây bi");
            Tutorial.MarkAll(s, Tutorial.TreePlaced, Tutorial.TreeTap);
            Assert.IsTrue(Tutorial.HomeToured(s));
            Assert.IsTrue(Tutorial.Shows(s, D, Tutorial.HubPart.Shop, 0));
            Assert.IsFalse(Tutorial.CoreDone(s), "còn báo Cửa hàng, lời chào cuối");
            Assert.IsTrue(Tutorial.IsCore(Tutorial.TreeBuild) && Tutorial.IsCore(Tutorial.TreeTap), "đặt Cây bi không tắt theo công tắc Gợi ý");
            Assert.IsFalse(Tutorial.IsCore(Tutorial.AfkBtn));
        }

        // khắc hệ (2026-11-27): bài học vòng Tương khắc thuộc chuỗi bắt buộc, các gợi ý nút / tướng bị khắc theo công tắc Gợi ý; mã bước
        // không trùng nhau (cờ lưu dạng chuỗi mã cách dấu phẩy)
        [Test]
        public void KhacHe_BaiHocBatBuoc_GoiYTheoCongTac_MaKhongTrung()
        {
            Assert.IsTrue(Tutorial.IsCore(Tutorial.CounterWheel), "bài học vòng Tương khắc không tắt theo công tắc Gợi ý");
            foreach (var id in new[] { Tutorial.WheelTile, Tutorial.WheelPick, Tutorial.CounteredTeam })
                Assert.IsFalse(Tutorial.IsCore(id), id);
            var ids = typeof(Tutorial).GetFields(System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static)
                .Where(f => f.IsLiteral && f.FieldType == typeof(string) && f.Name != nameof(Tutorial.Legacy))
                .Select(f => (string)f.GetRawConstantValue()).ToList();
            Assert.AreEqual(ids.Count, ids.Distinct().Count(), "trùng mã bước: " + string.Join(", ", ids.GroupBy(x => x).Where(g => g.Count() > 1).Select(g => g.Key)));
            var s = Fresh();
            Tutorial.Begin(s);
            Assert.IsFalse(Tutorial.Done(s, Tutorial.CounterWheel));
            Tutorial.Mark(s, Tutorial.CounterWheel);
            Assert.IsTrue(Tutorial.Done(s, Tutorial.CounterWheel));
            Assert.IsFalse(Tutorial.Done(s, Tutorial.CounterIsle), "đánh dấu bài học không đánh dấu luôn bước khoanh đảo");
            Assert.IsTrue(Tutorial.Pages(D.Cfg).Any(p => p.step == Tutorial.Counter && p.text.Contains("×0,75") && p.text.Contains("×1,5")));
        }
    }
}
