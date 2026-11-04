// Tiềm năng so với bản web (golden potential.json): 60 lần khai phá có khoá ô và giữ mới / giữ cũ, trần tổng, phần cộng và hiệu ứng
// đầu trận của đội, 6 trận thật có hiệu ứng đầu trận, Hang (đội địch, thứ trong tuần, lượt, đá). Thêm: tỉ lệ độ hiếm trên 100.000 lần quay,
// giá có khoá, lưu rồi đọc lại. Số hiệp 6 trận thật tính lại bên Unity 2026-11-03 khi Chiêu đổi sang ra đòn ngay lúc bấm,
// và 2026-11-04 khi đổi luật rút thẻ.
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
            for (int i = 0; i < 4; i++)
            {
                var w = i < want.Count ? J.Obj(want[i]) : null;
                Assert.AreEqual(w == null, got[i] == null, $"{at} ô {i} trống");
                if (w == null) continue;
                Assert.AreEqual(J.Str(w, "k"), Potential.Key(got[i].k), $"{at} ô {i} loại");
                Assert.AreEqual(J.Int(w, "r"), got[i].r, $"{at} ô {i} độ hiếm");
            }
        }

        [Test]
        public void KhaiPha60Lan_KhoaO_GiuMoiGiuCu_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.Hero("giot_suong").star = 4;
            s.Hero("vo_su").owned = true;
            s.Hero("vo_su").star = 2;
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
        public void TranTong_PhanCong_HieuUngDauTran_KhopBanWeb()
        {
            var d = TestData.Load();
            var t = J.Obj(G, "totals");
            var lines = J.Arr(t, "lines").Select(x => new PotLine { k = Potential.FromKey(J.Str(J.Obj(x), "k")), r = J.Int(J.Obj(x), "r") }).ToList();
            var tot = Potential.Totals(d.Cfg, lines);
            var wt = J.Obj(t, "totals");
            for (int k = 0; k < 8; k++) Assert.AreEqual(J.Num(wt, Potential.KindKeys[k]), tot[k], Potential.KindKeys[k]);
            Assert.AreEqual(0.4, tot[(int)PotKind.Atk], 1e-12, "3 dòng Công Huyền thoại (48%) chặn ở 40%");

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
                    Assert.AreEqual(J.Num(mods, "hpPct"), m.mods.hpPct, m.heroId);
                    Assert.AreEqual(J.Num(mods, "atkPct"), m.mods.atkPct, m.heroId);
                    Assert.AreEqual(J.Num(mods, "defPct"), m.mods.defPct, m.heroId);
                    Assert.AreEqual(J.Num(mods, "spd"), m.mods.spd, m.heroId);
                }
                var st = J.Obj(o, "start");
                Assert.AreEqual(st == null, m.start == null, m.heroId + " start");
                if (st != null)
                {
                    Assert.AreEqual(J.Num(st, "mana"), m.start.mana, m.heroId);
                    Assert.AreEqual(J.Num(st, "rage"), m.start.rage, m.heroId);
                    Assert.AreEqual(J.Num(st, "crit"), m.start.crit, m.heroId);
                    Assert.AreEqual(J.Num(st, "lifesteal"), m.start.lifesteal, m.heroId);
                }
            }
        }

        static SaveData FightSave(GameData d)
        {
            var s = SaveData.New(d, 0);
            s.level = 6;
            s.Hero("vo_su").owned = true;
            s.team = new List<string> { "giot_suong", "vo_su" };
            s.Hero("giot_suong").potential = new[] { new PotLine { k = PotKind.Rage, r = 3 }, new PotLine { k = PotKind.Crit, r = 4 }, new PotLine { k = PotKind.Atk, r = 2 }, null };
            s.Hero("vo_su").potential = new[] { new PotLine { k = PotKind.Mana, r = 2 }, new PotLine { k = PotKind.Lifesteal, r = 3 }, null, null };
            return s;
        }

        [Test]
        public void TranCoHieuUngDauTran_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = FightSave(d);
            foreach (var x in J.Arr(G, "fights"))
            {
                var o = J.Obj(x);
                var team = Teams.Player(s, null, d);
                team.ai = true;
                var b = Battle.Create(d, team, Teams.Enemy(d.Stage(J.Int(o, "stage")), d), (uint)J.Num(o, "seed"), 6, 6);
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
        public void Hang_DoiDich_ThuTrongTuan_LuotVaDa_KhopBanWeb()
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
            int d0 = J.Int(g, "caveDay");
            foreach (var x in J.Arr(g, "caveSteps"))
            {
                var o = J.Obj(x);
                string op = J.Str(o, "op");
                object r = op == "win" ? (object)(double)Potential.WinCave(s, d.Cfg, d0, J.Int(o, "arg"))
                    : op == "ad" ? AdGate.Use(s, d.Cfg, d0, AdGate.CaveExtra)
                    : (object)Potential.CavePick(s, d.Cfg, d0, Keys.ToElem(J.Str(o, "arg")));
                Assert.AreEqual(J.Get(o, "r"), r, op);
                Assert.AreEqual(J.Int(o, "left"), Potential.CaveLeft(s, d.Cfg, d0), op + " lượt còn");
                Assert.AreEqual(J.Int(o, "stones"), s.potentialStones, op + " đá");
            }
        }

        [Test]
        public void TiLeDoHiem_100000LanQuay_GiaCoKhoa_LuuDocLai()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.Hero("giot_suong").star = 4;
            s.potentialStones = 1_000_000;
            var rng = new Rng(7);
            var count = new int[5];
            var kinds = new int[8];
            var none = new bool[4];
            for (int i = 0; i < 25000; i++)
            {
                var res = Potential.Spin(s, d.Cfg, "giot_suong", none, rng);
                foreach (var x in res)
                {
                    count[x.r]++;
                    kinds[(int)x.k]++;
                }
                Potential.Keep(s, "giot_suong", true);
            }
            double[] want = { 55, 28, 12, 4.5, 0.5 };
            for (int r = 0; r < 5; r++) Assert.AreEqual(want[r], count[r] / 1000.0, r == 4 ? 0.15 : 0.5, "độ hiếm " + r);
            foreach (var k in kinds) Assert.AreEqual(12.5, k / 1000.0, 0.5, "8 loại đều nhau");

            // 3 ô mở, khoá 1 ô có dòng: 2 + 2 = 4 đá; khoá 3 ô: không quay được
            s.Hero("giot_suong").star = 3;
            var locks = new List<bool> { true, false, false };
            Assert.AreEqual(4, Potential.SpinCost(s, d.Cfg, "giot_suong", locks));
            var before = s.Hero("giot_suong").potential[0];
            var res2 = Potential.Spin(s, d.Cfg, "giot_suong", locks, rng);
            Assert.AreEqual(before.k, res2[0].k);
            Assert.AreEqual(before.r, res2[0].r);
            Assert.IsNull(Potential.Spin(s, d.Cfg, "giot_suong", new List<bool> { true, true, true }, rng), "khoá tối đa 2 ô");
            s.potentialStones = 1;
            Assert.IsNull(Potential.Spin(s, d.Cfg, "giot_suong", none, rng), "thiếu đá");

            s.cave = new CaveDay { day = 9, wins = 2, pick = Elem.Moc };
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var back));
            for (int i = 0; i < 4; i++)
            {
                var a = s.Hero("giot_suong").potential[i];
                var b = back.Hero("giot_suong").potential[i];
                Assert.AreEqual(a == null, b == null);
                if (a != null) Assert.AreEqual((a.k, a.r), (b.k, b.r));
            }
            Assert.IsNotNull(back.Hero("giot_suong").potentialNew, "kết quả chờ chọn được giữ khi tắt game");
            Assert.AreEqual(1, back.potentialStones);
            Assert.AreEqual(Elem.Moc, back.cave.pick);
            Assert.AreEqual(2, back.cave.wins);
        }
    }
}
