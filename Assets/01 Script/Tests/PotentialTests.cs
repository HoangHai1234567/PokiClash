// Tiềm năng so với golden potential.json: 60 lần khai phá có khoá ô và giữ mới / giữ cũ, phần cộng và hiệu ứng đầu trận của đội, 6 trận
// thật có hiệu ứng đầu trận, đội địch của Hang, thứ trong tuần. Thêm: trần tổng, tỉ lệ độ hiếm và loại trên 100.000 dòng, giá có khoá, lưu
// rồi đọc lại; 6 ô, bản lưu cũ 4 ô, đá tinh, bộ, hiệu ứng đầu trận mới (khiên, giảm sát thương, né); Hang 10 tầng mở lần lượt, thưởng
// lần đầu, đá tinh lượt đầu ngày.
// Số hiệp 6 trận thật tính lại bên Unity 2026-11-03 khi Chiêu đổi sang ra đòn ngay lúc bấm, và 2026-11-04 khi đổi luật rút thẻ.
// 2026-11-16: bỏ 31 tướng cũ không còn suất đảo, tướng mẫu đổi sang tướng thay cùng hệ (SaveCodec.BoTuongCu); golden tính lại bằng
// menu "PokiClash/Thử/Tính lại golden theo tướng mẫu của test" (GoldenFixtureMenu).
// 2026-11-17 (tăng dày nội dung, GD_Claude/20_TangDayNoiDung.md): sao tổng 1..20 nên tướng mẫu khai phá ở sao 8 (4 ô) và 3 (2 ô); 11 loại
// dòng (Tốc không quay ra nữa); bộ Cuồng Chiến làm phần cộng của Tí Tách đổi. "spins", "members", "fights" tính lại bằng GoldenFixtureMenu,
// "caveStages" (đủ 10 tầng) bằng IslandGenMenu. "totals" và "caveSteps" của golden không dùng nữa (kỳ vọng tính trong test theo cấu hình).
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class PotentialTests
    {
        static Dictionary<string, object> G => J.Obj(MiniJson.Parse(TestData.Read("Golden/potential.json")));

        static void SameLines(List<object> want, PotLine[] got, string at)
        {
            for (int i = 0; i < Potential.Slots; i++)
            {
                var w = i < want.Count ? J.Obj(want[i]) : null;
                var x = Potential.LineAt(got, i);
                Assert.AreEqual(w == null, x == null, $"{at} ô {i} trống");
                if (w == null) continue;
                Assert.AreEqual(J.Str(w, "k"), Potential.Key(x.k), $"{at} ô {i} loại");
                Assert.AreEqual(J.Int(w, "r"), x.r, $"{at} ô {i} độ hiếm");
            }
        }

        [Test]
        public void KhaiPha60Lan_KhoaO_GiuMoiGiuCu_KhopGolden()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0, TestData.OldStarter); // bản lưu mẫu của golden (TestData.OldStarter)
            s.Hero("ti_tach").star = 8; // 4 ô (Bạc 3 sao)
            s.Hero("cao_da").owned = true;
            s.Hero("cao_da").star = 3; // 2 ô (Đồng 3 sao)
            s.potentialStones = 300;
            var rng = new Rng(41);
            int i = 0;
            foreach (var x in J.Arr(G, "spins"))
            {
                var o = J.Obj(x);
                string hero = J.Str(o, "hero"), at = $"lần {i++}";
                var locks = J.Arr(o, "locks").Select(v => (bool)v).ToList();
                Assert.AreEqual(J.Int(o, "cost"), Potential.SpinCost(s, d.Cfg, hero, locks), at + " giá");
                var res = Potential.Spin(s, d.Cfg, hero, locks, rng);
                var wres = J.Get(o, "res");
                Assert.AreEqual(wres == null, res == null, at + " quay được");
                if (res != null)
                {
                    SameLines(J.Arr(wres), res, at + " kết quả");
                    Potential.Keep(s, hero, J.Bool(o, "keepNew"));
                }
                Assert.AreEqual(J.Int(o, "stones"), s.potentialStones, at + " đá");
                SameLines(J.Arr(o, "pot"), s.Hero(hero).potential, at + " sau khi chọn");
            }
        }

        [Test]
        public void TranTong_PhanCong_HieuUngDauTran_KhopGolden()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            // trần: 3 dòng Công Huyền thoại chặn ở trần Công; hai ô cùng loại cộng dồn
            var lines = new List<PotLine> { new PotLine { k = PotKind.Atk, r = 4 }, new PotLine { k = PotKind.Atk, r = 4 }, new PotLine { k = PotKind.Atk, r = 4 },
                new PotLine { k = PotKind.Hp, r = 2 }, new PotLine { k = PotKind.Hp, r = 1 } };
            var tot = Potential.Totals(cfg, lines);
            Assert.AreEqual(System.Math.Min(cfg.potential.caps[(int)PotKind.Atk], 3 * cfg.potential.Val((int)PotKind.Atk, 4)), tot[(int)PotKind.Atk], 1e-12);
            Assert.AreEqual(cfg.potential.Val((int)PotKind.Hp, 2) + cfg.potential.Val((int)PotKind.Hp, 1), tot[(int)PotKind.Hp], 1e-12);

            var s = FightSave(d);
            var team = Teams.Player(s, null, d);
            var wm = J.Arr(G, "members");
            Assert.AreEqual(wm.Count, team.members.Count);
            for (int k = 0; k < wm.Count; k++)
            {
                var o = J.Obj(wm[k]);
                var m = team.members[k];
                var mods = J.Obj(o, "mods");
                Assert.AreEqual(mods == null, m.mods == null, m.heroId + " mods");
                if (mods != null)
                {
                    Assert.AreEqual(J.Num(mods, "hpPct"), m.mods.hpPct, 1e-12, m.heroId);
                    Assert.AreEqual(J.Num(mods, "atkPct"), m.mods.atkPct, 1e-12, m.heroId);
                    Assert.AreEqual(J.Num(mods, "defPct"), m.mods.defPct, 1e-12, m.heroId);
                    Assert.AreEqual(J.Num(mods, "spd"), m.mods.spd, m.heroId);
                }
                var st = J.Obj(o, "start");
                Assert.AreEqual(st == null, m.start == null, m.heroId + " start");
                if (st != null)
                {
                    Assert.AreEqual(J.Num(st, "mana"), m.start.mana, m.heroId);
                    Assert.AreEqual(J.Num(st, "rage"), m.start.rage, m.heroId);
                    Assert.AreEqual(J.Num(st, "crit"), m.start.crit, 1e-12, m.heroId);
                    Assert.AreEqual(J.Num(st, "lifesteal"), m.start.lifesteal, 1e-12, m.heroId);
                }
            }
        }

        static SaveData FightSave(GameData d)
        {
            var s = SaveData.New(d, 0, TestData.OldStarter); // bản lưu mẫu của golden (TestData.OldStarter)
            s.level = 6;
            s.Hero("cao_da").owned = true;
            s.team = new List<string> { "ti_tach", "cao_da" };
            s.Hero("ti_tach").potential = new[] { new PotLine { k = PotKind.Rage, r = 3 }, new PotLine { k = PotKind.Crit, r = 4 }, new PotLine { k = PotKind.Atk, r = 2 }, null };
            s.Hero("cao_da").potential = new[] { new PotLine { k = PotKind.Mana, r = 2 }, new PotLine { k = PotKind.Lifesteal, r = 3 }, null, null };
            return s;
        }

        [Test]
        public void TranCoHieuUngDauTran_KhopGolden()
        {
            var d = TestData.Load();
            var s = FightSave(d);
            foreach (var x in J.Arr(G, "fights"))
            {
                var o = J.Obj(x);
                var team = Teams.Player(s, null, d);
                team.ai = true;
                var b = Battle.Create(d, team, Teams.Enemy(TestData.AtLevel(d.Stage(J.Int(o, "stage")), J.Int(o, "foeLevel")), d), (uint)J.Num(o, "seed"), 6, 6);
                string at = $"ải {J.Int(o, "stage")} hạt giống {J.Num(o, "seed")}";
                var f0 = b.sides[0].fighters[0];
                var ws = J.Obj(o, "start");
                Assert.AreEqual(J.Num(ws, "mana"), f0.mana, at + " mana đầu trận");
                Assert.AreEqual(J.Num(ws, "rage"), f0.rage, at + " nộ đầu trận");
                var wb = J.Arr(ws, "buffs");
                Assert.AreEqual(wb.Count, f0.buffs.Count, at + " buff cả trận");
                BattleSim.Run(b);
                Assert.AreEqual(J.Int(o, "winner"), b.winner, at + " bên thắng");
                Assert.AreEqual(J.Int(o, "round"), b.round, at + " số hiệp");
            }
        }

        [Test]
        public void Hang_DoiDich_ThuTrongTuan_KhopGolden()
        {
            var d = TestData.Load();
            var g = G;
            foreach (var x in J.Arr(g, "caveStages"))
            {
                var o = J.Obj(x);
                var st = Potential.CaveStage(d, Keys.ToElem(J.Str(o, "zone")), J.Int(o, "tier"));
                Assert.AreEqual(J.Int(o, "id"), st.id);
                var we = J.Arr(o, "enemies");
                for (int k = 0; k < we.Count; k++)
                {
                    var e = J.Arr(we[k]);
                    Assert.AreEqual((string)e[0], st.enemies[k].hero);
                    Assert.AreEqual((double)e[1], st.enemies[k].level);
                    Assert.AreEqual((bool)e[2], st.enemies[k].boss);
                    if (e.Count > 3) Assert.AreEqual((double)e[3], st.enemies[k].buff, 1e-9);
                }
            }
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Hoa] = 4;
            foreach (var x in J.Arr(g, "caveDays"))
            {
                var o = J.Obj(x);
                int day = J.Int(o, "day");
                Assert.AreEqual(J.Int(o, "weekday"), Potential.WeekdayOf(day), "thứ của ngày " + day);
                var we = J.Str(o, "elem");
                var ge = Potential.CaveElem(s, d.Cfg, day);
                Assert.AreEqual(we, ge is Elem e ? Keys.Of(e) : null, "hệ boss ngày " + day);
            }
        }

        [Test]
        public void Hang_TangMoLanLuot_ThuongLanDau_Luot_DaTinh()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var cv = cfg.cave;
            var s = SaveData.New(d, 0);
            const int day = 20003; // Thứ Hai (ngày 20000 là Thứ Sáu): boss hệ Kim
            Assert.AreEqual(Elem.Kim, Potential.CaveElem(s, cfg, day));
            Assert.IsTrue(Potential.CaveCanEnter(s, cfg, day, 0), "tầng 1 mở sẵn");
            Assert.IsFalse(Potential.CaveCanEnter(s, cfg, day, 1), "tầng 2 mở khi qua tầng 1");

            var w = Potential.WinCave(s, cfg, day, 0);
            Assert.IsTrue(w.first);
            Assert.AreEqual(cv.tiers[0].stones, w.stones);
            Assert.AreEqual(cv.tiers[0].stones + cv.tiers[0].firstStones, s.potentialStones, "đá của lượt + thưởng lần đầu");
            Assert.AreEqual(cv.tiers[0].firstCrystals, s.potentialCrystals);
            Assert.AreEqual(1, s.caveFloor);
            Assert.AreEqual(cv.winsPerDay - 1, Potential.CaveLeft(s, cfg, day));
            Assert.IsTrue(Potential.CaveCanEnter(s, cfg, day, 1));

            // thắng lại tầng 1: chỉ đá của lượt
            int st0 = s.potentialStones;
            w = Potential.WinCave(s, cfg, day, 0);
            Assert.IsFalse(w.first);
            Assert.AreEqual(st0 + cv.tiers[0].stones, s.potentialStones);
            Potential.WinCave(s, cfg, day, 0);
            Assert.AreEqual(0, Potential.CaveLeft(s, cfg, day));
            Assert.IsFalse(Potential.CaveCanEnter(s, cfg, day, 0), "hết lượt: tầng đã qua không vào được");
            Assert.IsTrue(Potential.CaveCanEnter(s, cfg, day, 1), "hết lượt vẫn đánh được tầng chưa qua lần đầu");
            st0 = s.potentialStones;
            w = Potential.WinCave(s, cfg, day, 1);
            Assert.IsTrue(w.first);
            Assert.AreEqual(0, w.stones, "hết lượt: không có đá của lượt");
            Assert.AreEqual(st0 + cv.tiers[1].firstStones, s.potentialStones);
            Assert.AreEqual(2, s.caveFloor);

            // quảng cáo +1 lượt
            Assert.IsTrue(AdGate.Use(s, cfg, day, AdGate.CaveExtra));
            Assert.AreEqual(cv.adExtra, Potential.CaveLeft(s, cfg, day));

            // đá tinh: lượt thắng đầu tiên trong ngày ở tầng crystalFloor trở lên
            var c = SaveData.New(d, 0);
            c.caveFloor = cv.tiers.Count;
            int top = cv.crystalFloor - 1;
            Assert.AreEqual(cv.crystalDaily, Potential.WinCave(c, cfg, day, top).crystals);
            Assert.AreEqual(0, Potential.WinCave(c, cfg, day, top).crystals, "lượt thứ hai trong ngày không có");
            var c2 = SaveData.New(d, 0);
            c2.caveFloor = cv.tiers.Count;
            Assert.AreEqual(0, Potential.WinCave(c2, cfg, day, top - 1).crystals, "tầng thấp hơn không có");
            Assert.AreEqual(0, Potential.WinCave(c2, cfg, day, top).crystals, "chỉ lượt đầu tiên trong ngày");

            // tầng: cấp tăng dần, tầng cuối quanh cấp 200, 2 địch cùng hệ
            for (int t = 1; t < cv.tiers.Count; t++) Assert.Greater(cv.tiers[t].level, cv.tiers[t - 1].level);
            Assert.GreaterOrEqual(cv.tiers[cv.tiers.Count - 1].level, 190);
            var stg = Potential.CaveStage(d, Elem.Thuy, cv.tiers.Count - 1);
            Assert.AreEqual(2, stg.enemies.Count);
            Assert.IsTrue(stg.enemies.All(e => d.Hero(e.hero).elem == Elem.Thuy));
        }

        [Test]
        public void TiLeDoHiem_100000Dong_GiaCoKhoa_LuuDocLai()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0, TestData.OldStarter); // bản lưu mẫu của golden (TestData.OldStarter)
            s.Hero("ti_tach").star = 8; // 4 ô
            s.potentialStones = 1_000_000;
            var rng = new Rng(7);
            var count = new int[5];
            var kinds = new int[Potential.KindCount];
            var none = new bool[Potential.Slots];
            for (int i = 0; i < 25000; i++)
            {
                var res = Potential.Spin(s, cfg, "ti_tach", none, rng);
                for (int k = 0; k < 4; k++)
                {
                    count[res[k].r]++;
                    kinds[(int)res[k].k]++;
                }
                Assert.IsNull(res[4], "ô chưa mở không quay");
                Potential.Keep(s, "ti_tach", true);
            }
            double[] want = { 55, 28, 12, 4.5, 0.5 };
            for (int r = 0; r < 5; r++) Assert.AreEqual(want[r], count[r] / 1000.0, r == 4 ? 0.15 : 0.5, "độ hiếm " + r);
            int rollable = Potential.Kinds.Count(k => Potential.KindWeight(cfg, k) > 0);
            Assert.AreEqual(0, kinds[(int)PotKind.Spd], "Tốc không quay ra (Tốc không có tác dụng trong trận)");
            foreach (var k in Potential.Kinds.Where(k => Potential.KindWeight(cfg, k) > 0))
                Assert.AreEqual(100.0 / rollable, kinds[(int)k] / 1000.0, 0.5, "các loại đều nhau: " + Potential.Key(k));

            // 3 ô mở, khoá 1 ô có dòng: 2 + 2 = 4 đá; khoá 4 ô (quá maxLocks): không quay được
            s.Hero("ti_tach").star = 6;
            var locks = new List<bool> { true, false, false };
            Assert.AreEqual(2 + cfg.potential.lockCost, Potential.SpinCost(s, cfg, "ti_tach", locks));
            var before = s.Hero("ti_tach").potential[0];
            var res2 = Potential.Spin(s, cfg, "ti_tach", locks, rng);
            Assert.AreEqual(before.k, res2[0].k);
            Assert.AreEqual(before.r, res2[0].r);
            Potential.Keep(s, "ti_tach", false);
            s.Hero("ti_tach").star = 8;
            Assert.IsNull(Potential.Spin(s, cfg, "ti_tach", new List<bool> { true, true, true, true }, rng), $"khoá tối đa {cfg.potential.maxLocks} ô");
            s.potentialStones = 1;
            Assert.IsNull(Potential.Spin(s, cfg, "ti_tach", none, rng), "thiếu đá");

            s.cave = new CaveDay { day = 9, wins = 2, pick = Elem.Moc };
            s.potentialCrystals = 4;
            s.caveFloor = 3;
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var back));
            for (int i = 0; i < Potential.Slots; i++)
            {
                var a = Potential.LineAt(s.Hero("ti_tach").potential, i);
                var b = Potential.LineAt(back.Hero("ti_tach").potential, i);
                Assert.AreEqual(a == null, b == null);
                if (a != null) Assert.AreEqual((a.k, a.r), (b.k, b.r));
            }
            Assert.AreEqual(1, back.potentialStones);
            Assert.AreEqual(4, back.potentialCrystals);
            Assert.AreEqual(3, back.caveFloor);
            Assert.AreEqual(Elem.Moc, back.cave.pick);
            Assert.AreEqual(2, back.cave.wins);
        }

        [Test]
        public void SauO_BanLuuCu4O_DaTinh_Bo_HieuUngDauTranMoi()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            // ô mở theo sao tổng: sao cũ 1..5 (đổi sang 1, 3, 6, 8, 11) giữ số ô đã mở như trước
            int[] old = { 1, 3, 6, 8, 11 };
            for (int i = 0; i < old.Length; i++) Assert.AreEqual(i + 1, Potential.OpenSlots(cfg, old[i]), "sao cũ " + (i + 1));
            Assert.AreEqual(Potential.Slots, Potential.OpenSlots(cfg, StarTier.MaxStar));

            // bản lưu cũ: mảng 4 ô
            var s = SaveData.New(d, 0, TestData.OldStarter);
            var p = s.Hero("ti_tach");
            p.star = StarTier.MaxStar;
            p.potential = new[] { new PotLine { k = PotKind.Atk, r = 1 }, null, null, null };
            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var back));
            Assert.AreEqual(Potential.Slots, back.Hero("ti_tach").potential.Length, "đọc ra đủ 6 ô");
            Assert.AreEqual(PotKind.Atk, back.Hero("ti_tach").potential[0].k);

            // khai phá bằng đá tinh: 1 đá tinh thay phần đá của các ô quay; mọi ô quay ra từ Hiếm trở lên
            var rng = new Rng(11);
            s.potentialStones = 0;
            s.potentialCrystals = 0;
            var none = new bool[Potential.Slots];
            Assert.IsNull(Potential.Spin(s, cfg, "ti_tach", none, rng, true), "không có đá tinh");
            s.potentialCrystals = 2;
            Assert.AreEqual(0, Potential.SpinCost(s, cfg, "ti_tach", none, true));
            var res = Potential.Spin(s, cfg, "ti_tach", none, rng, true);
            Assert.AreEqual(1, s.potentialCrystals);
            Assert.IsTrue(res.All(x => x != null && x.r >= 2), "đá tinh: mọi ô từ Hiếm");
            Potential.Keep(s, "ti_tach", true);
            var locks = new List<bool> { true, true, false, false, false, false };
            Assert.AreEqual(2 * cfg.potential.lockCost, Potential.SpinCost(s, cfg, "ti_tach", locks, true), "đá tinh: ô khoá vẫn tính đá");
            Assert.IsNull(Potential.Spin(s, cfg, "ti_tach", locks, rng, true), "thiếu đá cho ô khoá");

            // bộ: đủ need[0] dòng cùng nhóm thì cộng phần thưởng bộ (ngoài trần)
            var set = cfg.potential.sets.First(x => x.key == "cong");
            var lines = set.kinds.Take(set.need[0]).Select(k => new PotLine { k = Potential.FromKey(k), r = 0 }).ToArray();
            Assert.AreEqual(1, Potential.SetLevel(set, lines));
            var plain = Potential.Totals(cfg, lines);
            var fin = Potential.Final(cfg, lines);
            foreach (var (k, v) in Potential.SetBonusOf(set, 1)) Assert.AreEqual(plain[(int)k] + v, fin[(int)k], 1e-12, "bộ cấp 1: " + Potential.Key(k));
            Assert.AreEqual(0, Potential.SetLevel(set, lines.Take(set.need[0] - 1)));

            // hiệu ứng đầu trận mới: khiên, giảm sát thương, né
            p.potential = new[] { new PotLine { k = PotKind.Shield, r = 4 }, new PotLine { k = PotKind.Guard, r = 4 }, new PotLine { k = PotKind.Dodge, r = 4 }, null, null, null };
            var st = Potential.Start(s, d, "ti_tach");
            Assert.AreEqual(cfg.potential.Val((int)PotKind.Shield, 4), st.shield, 1e-12);
            s.team = new List<string> { "ti_tach" };
            var b = Battle.Create(d, Teams.Player(s, null, d), Teams.Enemy(d.Stage(1), d), 1);
            var f = b.sides[0].fighters[0];
            Assert.AreEqual(Js.Round(f.maxHp * st.shield), f.shield, "khiên đầu trận");
            Assert.AreEqual(-st.guard, Battle.BuffSum(f, Stat.DmgTaken), 1e-12, "giảm sát thương nhận");
            Assert.AreEqual(st.dodge, Battle.BuffSum(f, Stat.Dodge), 1e-12, "né đòn");
        }

        // câu 14 (GD_Claude/12): màn Tướng (HeroDetailDialog, TeamLineup) và trận phải ra cùng chỉ số khi tướng có huy hiệu, tiềm năng,
        // bộ. Hai nơi cùng gọi HeroStats.Compute(..., Potential.Mods); báo "lệch" cũ là do menu thử so tướng không cộng với tướng đầu đội.
        [Test]
        public void ChiSoManTuong_KhopTrongTran_KhiCoHuyHieuTiemNang()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0, TestData.OldStarter);
            s.level = 120;
            var p = s.Hero("ti_tach");
            p.star = 8;
            var set = cfg.potential.sets.First(x => x.key == "cong");
            p.potential = set.kinds.Take(set.need[0]).Select(k => new PotLine { k = Potential.FromKey(k), r = 3 })
                .Concat(new[] { new PotLine { k = PotKind.Hp, r = 4 } }).ToArray();
            var h = d.Hero("ti_tach");
            s.badges[(int)h.elem].tier = 6;
            s.badges[((int)h.elem + 1) % 5].tier = 3; // dãy khác hệ: chỉ cộng phần cả đội
            var ui = HeroStats.Compute(cfg, h, s.level, p.star, false, Potential.Mods(s, d, h));
            var raw = HeroStats.Compute(cfg, h, s.level, p.star);
            Assert.Greater(ui.hp, raw.hp, "có huy hiệu, tiềm năng thì chỉ số màn Tướng phải cao hơn chỉ số gốc");
            var b = Battle.Create(d, Teams.Player(s, new[] { "ti_tach" }, d), Teams.Enemy(d.Stage(1), d), 1);
            var f = b.ActiveOf(0);
            Assert.AreEqual("ti_tach", f.hero.id);
            Assert.AreEqual(ui.hp, f.maxHp, "máu");
            Assert.AreEqual(ui.atk, f.atk, "công");
            Assert.AreEqual(ui.def, f.def, "thủ");
        }
    }
}
