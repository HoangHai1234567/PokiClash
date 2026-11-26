// Tiến trình so với bản web (golden): chỉ số 11 tướng × cấp 1/10/20/30 × sao 1/3/5 × boss, chuỗi thẻ rơi từ rương,
// chuỗi mảnh tướng; và luật nâng thẻ, bậc sao (lên sao bằng mảnh, tiến hóa bằng đá, 2026-11-17), độ hiếm theo suất ải.
// progression.json (chỉ số 5 tướng khởi đầu, Võ Sư): tính lại bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md).
// 2026-11-16: bỏ 31 tướng cũ không còn suất đảo, tướng mẫu đổi sang tướng thay cùng hệ (SaveCodec.BoTuongCu); golden tính lại bằng
// menu "PokiClash/Thử/Tính lại golden theo tướng mẫu của test" (GoldenFixtureMenu).
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class ProgressionTests
    {
        static Dictionary<string, object> golden;
        static Dictionary<string, object> G => golden ??= J.Obj(MiniJson.Parse(TestData.Read("Golden/progression.json")));

        static readonly string[] SlotKey = { "skill", "ult", "passive" };

        [Test]
        public void ChiSoTuong_KhopBanWeb()
        {
            var d = TestData.Load();
            int n = 0;
            foreach (var x in J.Arr(G, "stats"))
            {
                var o = J.Obj(x);
                var st = HeroStats.Compute(d.Cfg, d.Hero(J.Str(o, "id")), J.Int(o, "lv"), J.Int(o, "st"), J.Bool(o, "boss"));
                string at = $"{J.Str(o, "id")} cấp {J.Int(o, "lv")} sao {J.Int(o, "st")} boss {J.Bool(o, "boss")}";
                Assert.AreEqual(J.Num(o, "hp"), st.hp, at + " máu");
                Assert.AreEqual(J.Num(o, "atk"), st.atk, at + " công");
                Assert.AreEqual(J.Num(o, "def"), st.def, at + " thủ");
                Assert.AreEqual(J.Num(o, "spd"), st.spd, at + " tốc");
                n++;
            }
            Assert.AreEqual(d.Heroes.Count * 4 * 3 * 2, n);
        }

        [Test]
        public void ModsCongThemPhanTram()
        {
            var d = TestData.Load();
            var h = d.Hero("hai_long");
            var a = HeroStats.Compute(d.Cfg, h, 10, 1);
            var b = HeroStats.Compute(d.Cfg, h, 10, 1, false, new StatMods { atkPct = 0.1, spd = 3 });
            Assert.AreEqual(a.hp, b.hp);
            Assert.AreEqual(Js.Round(a.atk * 1.1), b.atk, 1);
            Assert.AreEqual(a.spd + 3, b.spd);
            // Khiên Bạc (Hiếm) mạnh hơn Thiết Tinh (Khá, tướng khởi đầu hệ Kim từ 2026-11-16) cùng cấp, cùng sao
            var c = HeroStats.Compute(d.Cfg, d.Hero("bo_cap"), 10, 1);
            var v = HeroStats.Compute(d.Cfg, d.Hero("khien_bac"), 10, 1);
            Assert.Greater(v.hp + v.atk + v.def, c.hp + c.atk + c.def);
        }

        [Test]
        public void TheRoiTuRuong_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0, TestData.OldStarter); // bản lưu mẫu của golden (TestData.OldStarter)
            foreach (var id in new[] { "cao_da", "so_ngoc", "giap_long", "giap_nham" }) s.Hero(id).owned = true;
            var r = new Rng(77);
            var want = J.Arr(G, "drops");
            for (int i = 0; i < want.Count; i++)
            {
                var drop = Progress.RollCardDrop(s, d, (Rarity)r.Int(0, 4), r);
                var w = J.Arr(want[i]);
                if (want[i] == null)
                {
                    Assert.IsNull(drop, $"lần {i}");
                    continue;
                }
                Assert.IsNotNull(drop, $"lần {i}");
                Assert.AreEqual((string)w[0], drop.hero, $"lần {i}: tướng");
                Assert.AreEqual((string)w[1], SlotKey[(int)drop.slot], $"lần {i}: ô");
                Assert.AreEqual((string)w[2], drop.card, $"lần {i}: thẻ");
                Assert.AreEqual((string)w[3], Keys.Of(drop.rarity), $"lần {i}: độ hiếm");
            }
        }

        [Test]
        public void TheRoi_LuiDoHiem_KhongCoThiNull()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0); // chỉ có Tí Tách (tướng khởi đầu mặc định từ 2026-11-11): thẻ thường/khá...
            var drop = Progress.RollCardDrop(s, d, Rarity.Legend, new Rng(1));
            Assert.IsNotNull(drop);
            Assert.AreEqual("ti_tach", drop.hero);
            s.Hero("ti_tach").owned = false;
            Assert.IsNull(Progress.RollCardDrop(s, d, Rarity.Epic, new Rng(1)), "không có tướng nào: null (đổi thành EXP)");
        }

        [Test]
        public void ManhTuong_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            var r = new Rng(5);
            foreach (var x in J.Arr(G, "shards"))
            {
                var w = J.Arr(x);
                string hero = d.Heroes[r.Int(0, d.Heroes.Count - 1)].id;
                int n = r.Int(1, 6);
                var res = Progress.AddShards(s, d, hero, n, r);
                Assert.AreEqual((string)w[0], hero);
                Assert.AreEqual((double)w[1], n);
                Assert.AreEqual((bool)w[2], res.unlocked, hero + " mở");
                Assert.AreEqual((double)w[3], res.converted, hero + " đổi thành bản sao");
            }
            foreach (var x in J.Arr(G, "shardEnd"))
            {
                var w = J.Arr(x);
                var p = s.Hero((string)w[0]);
                Assert.AreEqual((bool)w[1], p.owned, (string)w[0]);
                Assert.AreEqual((double)w[2], p.shards, (string)w[0]);
                Assert.AreEqual((double)w[3], p.skill.copies);
                Assert.AreEqual((double)w[4], p.ult.copies);
                Assert.AreEqual((double)w[5], p.passive.copies);
            }
        }

        [Test]
        public void NangThe_TieuBanSao_CapToiDaGiuBanSao()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0);
            Progress.UnlockHero(s, "cao_da");
            var c = s.Hero("cao_da").skill;
            Assert.IsFalse(Progress.CanUpCard(s, cfg, "cao_da", CardSlot.Skill));
            c.copies = 2;
            Assert.IsTrue(Progress.UpCard(s, cfg, "cao_da", CardSlot.Skill));
            Assert.AreEqual(2, c.lv);
            Assert.AreEqual(0, c.copies);
            // Phun Đá (Tê Thiềm, thay Thiết Quyền của Võ Sư 2026-11-19) cấp 2: mô tả theo số thật
            Assert.AreEqual("Gây 115% Công sát thương. Địch −17% Thủ 2 lượt.", CardText.Text(d.Card(d.Hero("cao_da").skill), 2, cfg.cardLvStep));
            c.copies = 100;
            while (Progress.UpCard(s, cfg, "cao_da", CardSlot.Skill)) { }
            Assert.AreEqual(5, c.lv);
            Assert.AreEqual(100 - 4 - 8 - 15, c.copies, "cấp tối đa: bản sao còn lại được giữ");
            Assert.AreEqual(int.MaxValue, Progress.CardReq(cfg, 5));
        }

        // bậc sao (2026-11-17, StarTier): lên sao trong bậc tốn mảnh của tướng, đủ 5 sao thì tiến hóa sang 1 sao bậc sau, tốn đá tiến hóa
        // và cần cấp người chơi; không còn điều kiện tổng cấp thẻ
        [Test]
        public void LenSao_TonManh_TienHoa_TonDaVaCap()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0);
            var h = d.Hero("ti_tach"); // tướng khởi đầu mặc định, Khá
            var p = s.Hero("ti_tach");
            Assert.AreEqual(Progress.StarStep.StarUp, Progress.NextStep(s, d, "ti_tach"));
            int c2 = Progress.ShardCost(cfg, h, 2);
            Assert.AreEqual(cfg.shardCost[0], c2, "Khá: giá gốc");
            p.shards = c2 - 1;
            Assert.IsFalse(Progress.CanStarUp(s, d, "ti_tach"), "thiếu mảnh");
            Assert.AreEqual(0, Progress.HeroAlerts(s, d));
            p.shards = c2 + 3;
            Assert.AreEqual(1, Progress.HeroAlerts(s, d), "một việc chờ: lên sao");
            Assert.AreEqual((c2 + 3, c2), Progress.ShardGoal(s, d, "ti_tach"));
            Assert.IsTrue(Progress.StarUp(s, d, "ti_tach"));
            Assert.AreEqual(2, p.star);
            Assert.AreEqual(3, p.shards, "mảnh thừa giữ lại");
            Assert.AreEqual("Đồng 2 sao", StarTier.Label(p.star));

            // Đồng 5 sao: bước kế là tiến hóa, mảnh không dùng được nữa (để dành cho bậc sau)
            p.star = 5;
            p.shards = 999;
            Assert.AreEqual(Progress.StarStep.Evolve, Progress.NextStep(s, d, "ti_tach"));
            Assert.IsFalse(Progress.CanStarUp(s, d, "ti_tach"));
            Assert.AreEqual(0, Progress.ShardCost(cfg, h, 6), "sao 1 của bậc lên bằng tiến hóa");
            Assert.AreEqual((999, 0), Progress.ShardGoal(s, d, "ti_tach"));
            var c = Progress.EvolveCost(cfg, h, 1);
            Assert.AreEqual((cfg.evoStones[0], cfg.evoLevel[0]), c);
            Assert.AreEqual(c, Progress.EvolveCost(s, d, "ti_tach"));
            s.evoStones = c.stones;
            s.level = c.level - 1;
            Assert.IsFalse(Progress.CanEvolve(s, d, "ti_tach"), "thiếu cấp người chơi");
            Assert.AreEqual(0, Progress.HeroAlerts(s, d));
            s.level = c.level;
            s.evoStones = c.stones - 1;
            Assert.IsFalse(Progress.CanEvolve(s, d, "ti_tach"), "thiếu đá");
            Assert.IsFalse(Progress.Evolve(s, d, "ti_tach"));
            s.evoStones = c.stones + 2;
            Assert.AreEqual(1, Progress.HeroAlerts(s, d), "một việc chờ: tiến hóa");
            Assert.IsTrue(Progress.Evolve(s, d, "ti_tach"));
            Assert.AreEqual(6, p.star);
            Assert.AreEqual("Bạc 1 sao", StarTier.Label(p.star));
            Assert.AreEqual(2, s.evoStones, "đá trừ đúng giá");
            Assert.AreEqual(999, p.shards, "tiến hóa không tốn mảnh");
            Assert.AreEqual(1, h.FormIndex(cfg.formStars, p.star), "Bạc 1 sao là dạng 2");
            Assert.IsTrue(Progress.StarUp(s, d, "ti_tach"), "lên Bạc 2 sao bằng mảnh để dành");
            // bậc theo dạng (2026-11-19): Tí Tách 2 dạng nên bậc Bạc trải sao tổng 6..20; Bạc 2 sao là sao tổng 10, gộp mảnh sao 7..10
            Assert.AreEqual(10, p.star);
            Assert.AreEqual("Bạc 2 sao", StarTier.Label(cfg, h, p.star));
            Assert.AreEqual(999 - Enumerable.Range(7, 4).Sum(g => Progress.ShardCost(cfg, h, g)), p.shards, "gộp mảnh các sao tổng ở giữa");
            // Bạc 2 → 3 sao đi qua đầu bậc Vàng của thang cũ: cần cấp như mốc tiến hóa cũ, không tốn đá
            var up = Progress.StarUpCost(s, d, "ti_tach");
            Assert.AreEqual(13, up.to);
            Assert.AreEqual(cfg.evoLevel[1], up.level);
            p.shards = 999;
            s.level = up.level - 1;
            Assert.IsFalse(Progress.CanStarUp(s, d, "ti_tach"), "thiếu cấp người chơi");
            s.level = up.level;
            int stones = s.evoStones;
            Assert.IsTrue(Progress.StarUp(s, d, "ti_tach"));
            Assert.AreEqual(stones, s.evoStones, "lên sao không tốn đá");
            Assert.AreEqual(Progress.StarStep.StarUp, Progress.NextStep(s, d, "ti_tach"), "không còn tiến hóa sau bậc cuối");

            // tối đa: không lên sao, không tiến hóa
            p.star = StarTier.MaxStar;
            Assert.AreEqual(Progress.StarStep.Max, Progress.NextStep(s, d, "ti_tach"));
            Assert.IsFalse(Progress.CanStarUp(s, d, "ti_tach"));
            Assert.IsFalse(Progress.CanEvolve(s, d, "ti_tach"));
            Assert.AreEqual((int.MaxValue, int.MaxValue), Progress.EvolveCost(cfg, h, StarTier.Count));
        }

        // bảng giá: mỗi sao trong bậc đắt dần, bậc sau đắt hơn bậc trước, độ hiếm cao tốn nhiều mảnh hơn; đá và cấp mở bậc tăng dần
        [Test]
        public void GiaManh_Da_TangTheoBacVaDoHiem()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            Assert.AreEqual(StarTier.MaxStar, cfg.maxStar);
            Assert.AreEqual(new[] { 6, 11 }, cfg.formStars, "dạng 2 ở Bạc 1 sao, dạng 3 ở Vàng 1 sao");
            Assert.AreEqual(StarTier.Count, cfg.tierPower.Length);
            Assert.AreEqual(StarTier.Count * (StarTier.PerTier - 1), cfg.shardCost.Length);
            Assert.AreEqual(5, cfg.shardRarity.Length);
            Assert.AreEqual(StarTier.Count - 1, cfg.evoStones.Length);
            Assert.AreEqual(StarTier.Count - 1, cfg.evoLevel.Length);
            var kha = d.Hero("ti_tach");
            int prevTier = 0;
            for (int t = 0; t < StarTier.Count; t++)
            {
                int sum = 0;
                for (int k = 2; k <= StarTier.PerTier; k++)
                {
                    int star = StarTier.Star(t, k);
                    if (k > 2) Assert.Greater(Progress.ShardCost(cfg, kha, star), Progress.ShardCost(cfg, kha, star - 1), $"sao {star}");
                    sum += Progress.ShardCost(cfg, kha, star);
                }
                Assert.Greater(sum, prevTier, $"bậc {StarTier.Name(t)} đắt hơn bậc trước");
                prevTier = sum;
            }
            for (int r = 1; r < 5; r++) Assert.Greater(cfg.shardRarity[r], cfg.shardRarity[r - 1]);
            Assert.Greater(Progress.ShardCost(cfg, d.Hero("hai_long"), StarTier.MaxStar), Progress.ShardCost(cfg, kha, StarTier.MaxStar), "Huyền thoại tốn hơn Khá");
            for (int t = 2; t < StarTier.Count; t++)
            {
                Assert.Greater(Progress.EvolveCost(cfg, kha, t).stones, Progress.EvolveCost(cfg, kha, t - 1).stones);
                Assert.Greater(Progress.EvolveCost(cfg, kha, t).level, Progress.EvolveCost(cfg, kha, t - 1).level);
            }
        }

        // chỉ số: mỗi sao trong bậc cộng ít, tiến hóa sang bậc sau là cú nhảy rõ
        [Test]
        public void HeSoSao_TrongBacIt_TienHoaNhayRo()
        {
            var cfg = TestData.Load().Cfg;
            Assert.AreEqual(1, HeroStats.StarMult(cfg, 1));
            for (int star = 2; star <= StarTier.MaxStar; star++)
            {
                double r = HeroStats.StarMult(cfg, star) / HeroStats.StarMult(cfg, star - 1);
                if (StarTier.InTier(star) == 1) Assert.Greater(r, 1.1, $"tiến hóa lên sao {star}");
                else Assert.That(r, Is.InRange(1.0001, 1.04), $"lên sao {star} trong bậc");
            }
        }

        // độ hiếm theo suất ải (GD_Claude/20_TangDayNoiDung.md): ải 70 (boss cuối đảo) Huyền thoại, 40/50/60 Sử thi, 20/30 Hiếm, 10/15 Khá,
        // 5 Thường; ải 1 là tướng khởi đầu, Khá (luật 5 tướng khởi đầu cùng Khá, 15_TuongKhoiDau.md). Huyền thoại hơn Sử thi cùng cấp,
        // cùng sao ít nhất 30% lực chiến (boss cuối đảo phải cách xa tướng ải 60)
        [Test]
        public void DoHiemTheoSuatAi_HuyenThoaiHonSuThi30PhanTram()
        {
            var d = TestData.Load();
            Rarity Want(int idx) => idx == 70 ? Rarity.Legend : idx >= 40 ? Rarity.Epic : idx >= 20 ? Rarity.Rare : idx == 5 ? Rarity.Common : Rarity.Uncommon;
            int[] shards = { 10, 15, 20, 30, 50 };
            foreach (var st in d.Stages)
            {
                if (st.tag != StageTag.Hero) continue;
                var h = d.Hero(st.enemies[0].hero);
                Assert.AreEqual(Want(st.idx), h.rarity, $"{h.id} ở ải {st.idx} {st.zone}");
                Assert.AreEqual(shards[(int)h.rarity], h.shards, $"{h.id}: số mảnh mở khoá theo độ hiếm");
            }
            Assert.AreEqual(Rarity.Legend, d.Hero("hai_long").rarity);
            Assert.AreEqual(Rarity.Epic, d.Hero("han_ngac").rarity);
            foreach (int lv in new[] { 1, 100, 200 })
                foreach (int star in new[] { 1, 11, StarTier.MaxStar })
                {
                    int a = HeroStats.Power(d.Cfg, d.Hero("hai_long"), new Member { heroId = "hai_long", level = lv, star = star });
                    int b = HeroStats.Power(d.Cfg, d.Hero("han_ngac"), new Member { heroId = "han_ngac", level = lv, star = star });
                    Assert.Greater(a, b * 1.3, $"cấp {lv} sao {star}: Hải Long {a}, Hàn Ngạc {b}");
                }
            for (int r = 1; r < 5; r++) Assert.Greater(HeroStats.PowerOf((Rarity)r), HeroStats.PowerOf((Rarity)(r - 1)));
        }

        // mảnh của tướng đã có dồn để lên sao; tướng đã tối đa sao thì mỗi mảnh đổi thành một bản sao thẻ; mở khoá thừa mảnh thì giữ
        [Test]
        public void ManhTuongDaCo_DonLenSao_ToiDaThiDoiBanSao()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            var r = new Rng(1);
            var p = s.Hero("ti_tach");
            int Copies() => p.skill.copies + p.ult.copies + p.passive.copies;
            var res = Progress.AddShards(s, d, "ti_tach", 4, r);
            Assert.AreEqual(0, res.converted);
            Assert.AreEqual(4, p.shards);
            Assert.AreEqual(0, Copies());
            p.star = StarTier.MaxStar;
            p.shards = 0;
            res = Progress.AddShards(s, d, "ti_tach", 3, r);
            Assert.AreEqual(3, res.converted);
            Assert.AreEqual(0, p.shards);
            Assert.AreEqual(3, Copies());
            var hl = d.Hero("hai_long");
            res = Progress.AddShards(s, d, "hai_long", hl.shards + 2, r);
            Assert.IsTrue(res.unlocked);
            Assert.AreEqual(2, s.Hero("hai_long").shards, "mảnh thừa khi mở khoá làm mảnh lên sao");
            Assert.AreEqual((2, Progress.ShardCost(d.Cfg, hl, 2)), Progress.ShardGoal(s, d, "hai_long"));
            Assert.AreEqual((0, d.Hero("han_ngac").shards), Progress.ShardGoal(s, d, "han_ngac"), "chưa có: cần mảnh mở khoá");
        }

        // đá tiến hóa: lần đầu qua ải tướng / mini boss / boss cuối đảo, rương mốc đảo; qua lại boss có tỉ lệ nhỏ, ải thường không có
        [Test]
        public void DuongExp_DauGameNhuCu_VeSauDocHon()
        {
            var cfg = TestData.Load().Cfg;
            Assert.Greater(cfg.expLateBase, 0);
            for (int lv = 1; lv <= 15; lv++)
                Assert.AreEqual(Js.RoundInt(cfg.expBase * System.Math.Pow(lv, cfg.expPow)), Progress.ExpToNext(lv, cfg), $"cấp {lv}: đầu game không đổi");
            Assert.Greater(Progress.ExpToNext(100, cfg), 2 * cfg.expBase * System.Math.Pow(100, cfg.expPow), "cấp 100 đắt hơn gấp đôi đường cũ");
            Assert.Greater(Progress.ExpToNext(200, cfg), 3 * cfg.expBase * System.Math.Pow(200, cfg.expPow), "cấp 200 đắt hơn gấp ba đường cũ");
            for (int lv = 2; lv <= cfg.maxLevel; lv++) Assert.GreaterOrEqual(Progress.ExpToNext(lv, cfg), Progress.ExpToNext(lv - 1, cfg));
        }

        [Test]
        public void DanhLaiAi_QuaSoTranDuBi_ThiGiamBi()
        {
            var d = TestData.Load();
            var sb = d.Cfg.stageBalls;
            Assert.Greater(sb.replayFull, 0);
            var s = SaveData.New(d, 0);
            var r = new Rng(5);
            var st = d.ZoneStages(Elem.Thuy).First(x => x.idx == 30);
            double now = 20500 * 86400000.0 + 3600000;
            Assert.IsTrue(Progress.WinStage(s, d, st.id, r, now).first);
            int full = Progress.StageBalls(d, st, false);
            for (int i = 0; i < sb.replayFull; i++)
            {
                var w = Progress.WinStage(s, d, st.id, r, now);
                Assert.AreEqual(full, w.balls);
                Assert.IsFalse(w.reduced);
            }
            var w2 = Progress.WinStage(s, d, st.id, r, now);
            Assert.IsTrue(w2.reduced);
            Assert.AreEqual(System.Math.Max(1, (int)System.Math.Round(full * sb.replayPct)), w2.balls);
            Assert.IsFalse(Progress.WinStage(s, d, st.id, r, now + 86400000.0).reduced, "ngày mới nhận đủ lại");
            Assert.IsFalse(Progress.WinStage(s, d, st.id, r).reduced, "không truyền giờ thì không tính");
            var next = d.ZoneStages(Elem.Thuy).First(x => x.idx == 31);
            Assert.IsFalse(Progress.WinStage(s, d, next.id, r, now).reduced, "ải mới luôn đủ bi");
        }

        [Test]
        public void DaTienHoa_LanDauQuaAi_RuongMoc_QuaLaiBoss()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0);
            var r = new Rng(3);
            var thuy = d.ZoneStages(Elem.Thuy).ToList();
            Assert.AreEqual(StageTag.Hero, thuy[0].tag);
            Assert.AreEqual(StageKind.Mini, thuy[19].kind);
            Assert.AreEqual(StageKind.Boss, thuy[69].kind);
            var w1 = Progress.WinStage(s, d, thuy[0].id, r);
            Assert.AreEqual(cfg.evoFirst[0], w1.evoStones, "lần đầu qua ải tướng");
            var w2 = Progress.WinStage(s, d, thuy[1].id, r);
            Assert.AreEqual(0, w2.evoStones, "ải thường");
            Assert.AreEqual(w1.evoStones, s.evoStones);
            Assert.AreEqual(cfg.evoFirst[1], Progress.StageEvo(cfg, thuy[19], true, r));
            Assert.AreEqual(cfg.evoFirst[2], Progress.StageEvo(cfg, thuy[69], true, r));
            Assert.Greater(cfg.evoFirst[2], cfg.evoFirst[1], "boss cuối đảo nhiều nhất");
            Assert.AreEqual(0, Progress.StageEvo(cfg, thuy[1], false, r), "qua lại ải thường không ra đá");
            int n = 0;
            for (int i = 0; i < 4000; i++) n += Progress.StageEvo(cfg, thuy[69], false, r);
            Assert.AreEqual(cfg.evoReplayBoss * 4000, n, 4000 * 0.03, "qua lại boss");
            s.zones[(int)Elem.Thuy] = 10;
            int before = s.evoStones;
            var c = Progress.ClaimZoneChest(s, d, Elem.Thuy, r);
            Assert.AreEqual(cfg.evoChest[0], c.evoStones, "rương mốc ải 10");
            Assert.AreEqual(before + c.evoStones, s.evoStones);
            s.zones[(int)Elem.Thuy] = 70;
            Progress.ZoneChest s2 = null;
            while (Progress.ZoneChestReady(s, Elem.Thuy) >= 0) s2 = Progress.ClaimZoneChest(s, d, Elem.Thuy, r);
            Assert.IsTrue(s2.big);
            Assert.AreEqual(cfg.evoChest[cfg.evoChest.Length - 1], s2.evoStones, "rương chinh phục");
        }

        [Test]
        public void LenCap_GiuExpThua_VaQuaHaiCap()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            int need = Progress.ExpToNext(1, d.Cfg) + Progress.ExpToNext(2, d.Cfg);
            int ups = Progress.AddExp(s, need + 7, d.Cfg);
            Assert.AreEqual(2, ups);
            Assert.AreEqual(3, s.level);
            Assert.AreEqual(7, s.exp);
        }
    }
}
