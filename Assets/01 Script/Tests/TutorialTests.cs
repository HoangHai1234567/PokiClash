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
            s.zones[(int)Elem.Thuy] = 1; // cây bi 1 mở khi qua ải đầu, cây 2 ở cấp 30
            Assert.IsNull(Tutorial.NextUnlock(s, D), "chưa xong chuỗi bắt buộc thì chưa báo");
            Tutorial.Mark(s, Tutorial.Free);
            var u = Tutorial.NextUnlock(s, D);
            Assert.AreEqual("h_cave", u.id, "cấp 30: Hang trước");
            Tutorial.Mark(s, u.id);
            Assert.AreEqual("h_tree2", Tutorial.NextUnlock(s, D)?.id, "rồi cây bi thứ 2, mỗi lần vào sảnh một cái");
            Tutorial.Mark(s, "h_tree2");
            Assert.IsNull(Tutorial.NextUnlock(s, D));
            Assert.IsTrue(Tutorial.Pages().All(p => !string.IsNullOrEmpty(p.title) && !string.IsNullOrEmpty(p.text)));
        }
    }
}
