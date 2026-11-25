// Sổ Phép (Core/SoPhep.cs, GD_Claude/28_SoPhep.md): cấu hình 4 chương 20 ô 40 nét 100 đá; nét theo cấp và EXP thừa sau cấp 200;
// cổng chương (cấp, nét đã vẽ, chúa tể), ô chốt cần 3 ô khác, mua, tẩy sổ hoàn nét và đá; sổ trống không đổi trận; luật trận: số thẻ,
// đổi bộ, số lần chọn, mana dự bị, khiên khi vào sân, đổi tướng giữa lượt, kết liễu, Tuyệt kỹ miễn nộ, vẽ lại.
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class SoPhepTests
    {
        static GameData D => TestData.Load();
        static BalanceConfig Cfg => D.Cfg;

        static SaveData Save(int level)
        {
            var s = SaveData.New(D, 0, TestData.OldStarter);
            s.level = level;
            return s;
        }

        // trận của Tí Tách (và Cào Đá nếu two) với luật r, gặp ải 1
        static Battle Fight(BattleRules r, bool two = false, uint seed = 7)
        {
            var s = Save(60);
            var team = new List<string> { "ti_tach" };
            if (two)
            {
                s.Hero("cao_da").owned = true;
                team.Add("cao_da");
            }
            var t0 = Teams.Player(s, team, D);
            t0.rules = r;
            var b = Battle.Create(D, t0, Teams.Enemy(D.Stage(1), D), seed, s.level, s.level);
            b.StartBattle();
            return b;
        }

        [Test]
        public void CauHinh_BonChuong_HaiMuoiO_BonMuoiNet_TramDa()
        {
            var c = Cfg.sophep;
            Assert.AreEqual(4, c.chapters.Count);
            Assert.AreEqual(20, c.nodes.Count);
            for (int ch = 0; ch < 4; ch++) Assert.AreEqual(5, c.nodes.Count(n => n.ch == ch), $"chương {ch} có 5 ô");
            Assert.AreEqual(40, SoPhep.Total(Cfg), "vẽ đủ cả sổ cần 40 nét");
            Assert.AreEqual(40, SoPhep.MaxPoints(Cfg), "nguồn nét vừa đủ 40");
            Assert.AreEqual(100, SoPhep.TotalStones(Cfg));
            Assert.AreEqual(30, SoPhep.LevelPoints(c, 200), "cấp 53–198 tận cùng 3, 8");
            foreach (var step in c.path) Assert.NotNull(c.Node(step.Split(':')[0]), "đường gợi ý: " + step);
            foreach (var n in c.nodes) Assert.IsNotEmpty(SoPhep.Describe(n, 0, 1), "chữ của ô " + n.id);
        }

        [Test]
        public void NguonNet_TheoCap_VaExpThuaSauCap200()
        {
            var s = Save(49);
            Assert.AreEqual(0, SoPhep.Earned(s, Cfg));
            s.level = 50;
            Assert.AreEqual(3, SoPhep.Earned(s, Cfg));
            s.level = 53;
            Assert.AreEqual(4, SoPhep.Earned(s, Cfg));
            s.level = 58;
            Assert.AreEqual(5, SoPhep.Earned(s, Cfg));
            s.level = 198;
            Assert.AreEqual(33, SoPhep.Earned(s, Cfg));
            s.level = 200;
            s.exp = 0;
            int cap = Progress.ExpToNext(200, Cfg);
            Progress.AddExp(s, cap + 2 * Cfg.sophep.expPerPoint + 5, Cfg);
            Assert.AreEqual(200, s.level);
            Assert.AreEqual(cap, s.exp, "thanh EXP vẫn chặn ở cấp tối đa");
            Assert.AreEqual(2, s.sophep.expPoints);
            Assert.AreEqual(5, s.sophep.expBank, 1e-9);
            Assert.AreEqual(35, SoPhep.Earned(s, Cfg));
            Progress.AddExp(s, 20 * Cfg.sophep.expPerPoint, Cfg);
            Assert.AreEqual(7, s.sophep.expPoints, "tối đa 7 nét từ EXP");
            Assert.AreEqual(0, s.sophep.expBank, "đủ nét thì EXP thừa bỏ như cũ");
            Assert.AreEqual(40, SoPhep.Earned(s, Cfg));
            // dưới cấp tối đa: EXP không góp vào sổ
            var t = Save(120);
            Progress.AddExp(t, 1000, Cfg);
            Assert.IsNull(t.sophep);
        }

        [Test]
        public void CongChuong_OChot_Mua_TaySoHoanNetVaDa()
        {
            var s = Save(55);
            Assert.IsTrue(SoPhep.ChapterOpen(s, Cfg, 0));
            Assert.IsFalse(SoPhep.ChapterOpen(s, Cfg, 1), "chương 2 cần cấp 60");
            Assert.IsTrue(SoPhep.Buy(s, Cfg, "lat_trang"));
            Assert.IsTrue(SoPhep.Buy(s, Cfg, "lat_trang"));
            Assert.AreEqual(3, SoPhep.Spent(s, Cfg), "Lật Trang cấp 1 + cấp 2 = 1 + 2 nét");
            Assert.AreEqual(1, SoPhep.Free(s, Cfg));
            Assert.AreEqual("Đã vẽ đủ", SoPhep.Block(s, Cfg, "lat_trang"));
            Assert.IsFalse(SoPhep.Buy(s, Cfg, "chot_1"), "ô chốt cần 3 ô khác trong chương");
            Assert.IsFalse(SoPhep.Buy(s, Cfg, "rong_don"), "thiếu nét (cần 2)");
            s.level = 60;
            Assert.IsFalse(SoPhep.ChapterOpen(s, Cfg, 1), "chương 2 cần đã vẽ 4 nét");
            Assert.IsTrue(SoPhep.Buy(s, Cfg, "mat_tinh"));
            Assert.IsTrue(SoPhep.ChapterOpen(s, Cfg, 1));
            // ô chốt chương 2 tốn 20 đá
            s.level = 190;
            foreach (var id in new[] { "muc_cho", "vao_rut", "tiep_suc" }) Assert.IsTrue(SoPhep.Buy(s, Cfg, id), id);
            s.evoStones = 25;
            SoPhep.SetFace(s, Cfg, "chot_2", 1);
            Assert.IsTrue(SoPhep.Buy(s, Cfg, "chot_2"));
            Assert.AreEqual(5, s.evoStones);
            Assert.AreEqual(20, s.sophep.stones);
            Assert.IsFalse(SoPhep.ChapterOpen(s, Cfg, 3), "chương 4 cần hạ một chúa tể");
            int spent = SoPhep.Spent(s, Cfg);
            SoPhep.Reset(s);
            Assert.AreEqual(0, SoPhep.Spent(s, Cfg));
            Assert.AreEqual(25, s.evoStones, "tẩy sổ hoàn đá");
            Assert.AreEqual(1, SoPhep.Face(s, "chot_2"), "tẩy sổ giữ mặt đã chọn");
            Assert.Greater(spent, 0);
            // lưu rồi đọc lại
            SoPhep.Buy(s, Cfg, "lat_trang");
            SaveCodec.Read(SaveCodec.Write(s), D, out var back);
            Assert.AreEqual(1, SoPhep.Lv(back, "lat_trang"));
            Assert.AreEqual(1, SoPhep.Face(back, "chot_2"));
        }

        [Test]
        public void SoTrong_KhongDoiTran_VaBiaSoKhongCongSuc()
        {
            var s = Save(150);
            Assert.IsNull(SoPhep.Rules(s, Cfg));
            Assert.IsNull(Teams.Player(s, null, D).rules);
            s.level = 200;
            s.zones[0] = Islands.Size(Elements.All[0]);
            s.sophep = new SoPhepState();
            s.sophep.lv["bia_so"] = 1;
            Assert.IsNull(SoPhep.Rules(s, Cfg), "Bìa Sổ là trang trí");
            Assert.IsTrue(SoPhep.HasCover(s, Cfg));
        }

        [Test]
        public void DuongGoiY_VeTheoThuTu()
        {
            var s = Save(200);
            s.zones[0] = Islands.Size(Elements.All[0]);
            s.evoStones = 500;
            s.sophep = new SoPhepState { expPoints = 7 };
            int n = SoPhep.AutoBuy(s, Cfg);
            Assert.AreEqual(Cfg.sophep.path.Count, n, "đủ nét, đủ đá: vẽ hết đường gợi ý");
            Assert.AreEqual(40, SoPhep.Spent(s, Cfg));
            Assert.AreEqual(400, s.evoStones);
        }

        [Test]
        public void LuatRutThe_SoThe_DoiBo_SoLanChon()
        {
            var b = Fight(new BattleRules { firstOfferAdd = 1, lastOffer = 5, rerolls = 1 });
            Assert.AreEqual(Phase.Picking, b.phase);
            Assert.AreEqual(0, b.turn.side);
            Assert.AreEqual(4, b.turn.offer.Count, "Rộng Tay: lần chọn đầu 3 + 1");
            Assert.IsTrue(b.CanReroll());
            var old = new List<string>(b.turn.offer);
            b.Reroll();
            Assert.AreEqual(0, b.RerollsLeft(0));
            Assert.IsFalse(b.CanReroll());
            Assert.IsFalse(b.turn.offer.SequenceEqual(old), "đổi bộ ra bộ khác");
            for (int k = 0; k < 3; k++) b.Pick(0);
            Assert.AreEqual(3, b.turn.offer.Count, "lần chọn giữa: 3 thẻ");
            b.Pick(0);
            Assert.AreEqual(1, b.turn.picksLeft);
            Assert.AreEqual(5, b.turn.offer.Count, "Trang Cuối: lần chọn cuối 5 thẻ");

            var c = Fight(new BattleRules { picks = 6, offer = 2 });
            Assert.AreEqual(6, c.turn.picksTotal, "Thêm Lượt: 6 lần chọn");
            Assert.AreEqual(2, c.turn.offer.Count, "mỗi lần 2 thẻ");
        }

        [Test]
        public void LuatDoiTuong_ManaDuBi_KhienVaoSan_DoiGiuaLuot()
        {
            var b = Fight(new BattleRules { benchMana = 5, swapInShield = 0.15, midSwaps = 1 }, true);
            var bench = b.sides[0].fighters[1];
            Assert.AreEqual(b.Data.Cfg.benchMana + 5, bench.mana, 1e-9, "Mực Chờ: mana dự bị lượt đầu");
            b.Pick(0);
            Assert.IsTrue(b.CanSwap(1), "Đổi Vai: đổi được cả khi đã chọn thẻ");
            b.Swap(1);
            Assert.AreEqual(1, b.sides[0].active);
            Assert.AreEqual(Js.Round(bench.maxHp * 0.15), bench.shield, "Vào Sân: khiên 15% máu");
            Assert.AreEqual(0, b.sides[0].rs.midSwaps);

            var plain = Fight(null, true);
            plain.Pick(0);
            Assert.IsFalse(plain.CanSwap(1), "không có sổ: đã chọn thẻ thì hết lúc đổi tướng");
        }

        [Test]
        public void LuatKetLieu_VaTuyetKyMienNo()
        {
            var b = Fight(new BattleRules { executeBelow = 0.999, ultDiscount = 0.5 });
            var me = b.ActiveOf(0);
            var ult = b.InnateCard(me, InnateKind.Ult).card;
            me.mana = b.Data.Cfg.maxMana; // Tuyệt kỹ còn tốn mana; Chữ Ký chỉ bớt nộ
            me.rage = Js.Round(ult.costRage * 0.5);
            Assert.AreEqual(me.rage, b.UltRage(me, ult, InnateKind.Ult));
            Assert.AreEqual("", b.InnateBlock(InnateKind.Ult), "Chữ Ký: Tuyệt kỹ đầu tiên chỉ cần nửa nộ");
            b.UseInnate(InnateKind.Ult);
            Assert.AreEqual(0, me.rage, "trừ nửa nộ");
            Assert.AreEqual(ult.costRage, b.UltRage(me, ult, InnateKind.Ult), "chỉ lần đầu");
            var foe = b.ActiveOf(1);
            while (b.phase == Phase.Picking) b.Pick(0);
            b.Execute();
            Assert.IsTrue(foe.dead || foe.boss, "Nét Kết: đòn đầu để địch dưới ngưỡng thì kết liễu (ải 1 không phải boss)");
        }

        [Test]
        public void LuatVeLai_MotLanMoiTran()
        {
            // trận khó: ải cuối đảo đầu ở cấp 1, tướng gục chắc chắn; có Vẽ Lại thì đúng một lần hồi sinh của bên mình
            var s = Save(1);
            var t0 = Teams.Player(s, new List<string> { "ti_tach" }, D);
            t0.rules = new BattleRules { revivePct = 0.3 };
            t0.ai = true;
            var last = D.ZoneStages(Elements.All[0]).Last();
            var b = Battle.Create(D, t0, Teams.Enemy(last, D), 3, 1, 200);
            var log = new List<BattleEvent>();
            BattleSim.Run(b, 0.15, log);
            Assert.AreEqual(1, b.winner, "trận này phải thua");
            Assert.IsTrue(b.sides[0].rs.reviveUsed, "Vẽ Lại đã dùng");
            Assert.GreaterOrEqual(log.Count(e => e.t == EvType.Revive && e.side == 0), 1, "có sự kiện hồi sinh của bên mình");
            Assert.IsTrue(b.sides[0].fighters.All(f => f.dead), "chỉ một lần: lần gục sau là gục hẳn");
        }
    }
}
