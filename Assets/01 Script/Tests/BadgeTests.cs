// Đền Huy Hiệu so với bản web (golden badges.json): đội địch của cả 200 trận thử thách (cấp, tướng, boss, hạt giống),
// chỉ số có phần cộng huy hiệu, 5 trận đánh thật bậc Đồng hệ Thủy, một đoạn tiến độ (mở đền, thắng, lên bậc, rương).
// Thêm: thua không mất tiến độ, phần cộng theo bậc cao nhất không cộng dồn, không có huy hiệu thì không có mods.
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class BadgeTests
    {
        static System.Collections.Generic.Dictionary<string, object> G => J.Obj(MiniJson.Parse(TestData.Read("Golden/badges.json")));

        [Test]
        public void DoiDich200Tran_KhopBanWeb()
        {
            var d = TestData.Load();
            int n = 0;
            foreach (var x in J.Arr(G, "stages"))
            {
                var o = J.Obj(x);
                var z = Keys.ToElem(J.Str(o, "zone"));
                int tier = J.Int(o, "tier"), i = J.Int(o, "i");
                var st = Badges.Stage(d, z, tier, i);
                string at = $"{J.Str(o, "zone")} bậc {tier} trận {i}";
                Assert.AreEqual(J.Int(o, "id"), st.id, at);
                Assert.AreEqual((uint)J.Num(o, "seed"), Badges.Seed(d, z, tier, i), at);
                Assert.AreEqual(J.Str(o, "kind"), st.kind == StageKind.Boss ? "boss" : "mini", at);
                var we = J.Arr(o, "enemies");
                Assert.AreEqual(we.Count, st.enemies.Count, at);
                for (int k = 0; k < we.Count; k++)
                {
                    var e = J.Arr(we[k]);
                    Assert.AreEqual((string)e[0], st.enemies[k].hero, at);
                    Assert.AreEqual((double)e[1], st.enemies[k].level, at);
                    Assert.AreEqual((bool)e[2], st.enemies[k].boss, at);
                }
                n++;
            }
            Assert.AreEqual(200, n);
        }

        static SaveData StatSave(GameData d)
        {
            var s = SaveData.New(d, 0);
            foreach (var id in new[] { "vo_su", "nu_hoa", "ca_ngua", "phap_luan" }) s.Hero(id).owned = true;
            s.badges[(int)Elem.Thuy].tier = 2;
            s.badges[(int)Elem.Hoa].tier = 5;
            return s;
        }

        [Test]
        public void ChiSoCoHuyHieu_VaTranThat_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = StatSave(d);
            foreach (var x in J.Arr(G, "stats"))
            {
                var o = J.Obj(x);
                var h = d.Hero(J.Str(o, "hero"));
                var m = Teams.MemberOf(s, h.id, d);
                Assert.AreEqual(J.Get(o, "mods") == null, m.mods == null, h.id + " có phần cộng");
                var st = HeroStats.Compute(d.Cfg, h, 9, 2, false, m.mods);
                var w = J.Obj(o, "stats");
                Assert.AreEqual(J.Num(w, "hp"), st.hp, h.id);
                Assert.AreEqual(J.Num(w, "atk"), st.atk, h.id);
                Assert.AreEqual(J.Num(w, "def"), st.def, h.id);
                Assert.AreEqual(J.Num(w, "spd"), st.spd, h.id);
            }
            s.level = 9;
            s.team = new System.Collections.Generic.List<string> { "giot_suong", "ca_ngua", "phap_luan" };
            foreach (var x in J.Arr(G, "fights"))
            {
                var o = J.Obj(x);
                int i = J.Int(o, "i");
                var stage = Badges.Stage(d, Elem.Thuy, 1, i);
                var team = Teams.Player(s, null, d);
                team.ai = true;
                var b = Battle.Create(d, team, Teams.Enemy(stage, d), Badges.Seed(d, Elem.Thuy, 1, i), 9, System.Math.Max(9, stage.enemies[0].level));
                BattleSim.Run(b);
                Assert.AreEqual(J.Int(o, "winner"), b.winner, $"trận {i} bên thắng");
                Assert.AreEqual(J.Int(o, "round"), b.round, $"trận {i} số hiệp");
            }
        }

        [Test]
        public void TienDo_MoDen_LenBac_Ruong_KhopBanWeb()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.zones[(int)Elem.Kim] = 4;
            var rng = new Rng(31);
            var steps = J.Arr(G, "steps");
            var first = J.Obj(steps[0]);
            Assert.AreEqual(J.Bool(first, "temple"), Badges.TempleOpen(s));
            var zones = d.Zones.Select(z => z.id).ToList();
            var lines = J.Arr(first, "lines");
            for (int k = 0; k < zones.Count; k++) Assert.AreEqual((bool)lines[k], Badges.LineOpen(s, zones[k]), Keys.Of(zones[k]));
            for (int k = 1; k < steps.Count; k++)
            {
                var o = J.Obj(steps[k]);
                var z = Keys.ToElem(J.Str(o, "zone"));
                var r = Badges.Win(s, d, z, rng);
                string at = $"bước {k}";
                Assert.AreEqual(J.Int(o, "gain"), r?.balls ?? 0, at + " bi thưởng");
                Assert.AreEqual(J.Int(o, "tierDone"), r?.tierDone ?? 0, at);
                var wr = J.Arr(o, "rewards");
                Assert.AreEqual(wr.Count, r?.rewards.Count ?? 0, at + " số thưởng rương");
                for (int q = 0; q < wr.Count; q++)
                {
                    var e = J.Arr(wr[q]);
                    if ((string)e[0] == "card") Assert.AreEqual((string)e[2], r.rewards[q].drop.card, at);
                    else Assert.AreEqual((double)e[1], r.rewards[q].n, at);
                }
                var cur = J.Obj(o, "cur");
                var mine = Badges.Current(s, d.Cfg, z);
                Assert.AreEqual(cur == null, mine == null, at + " trận đang đánh");
                if (cur != null)
                {
                    Assert.AreEqual(J.Int(cur, "tier"), mine.Value.tier, at);
                    Assert.AreEqual(J.Int(cur, "i"), mine.Value.i, at);
                }
                Assert.AreEqual(J.Int(o, "balls"), s.balls, at + " tổng bi");
                var wb = J.Obj(J.Obj(o, "badges"), J.Str(o, "zone"));
                Assert.AreEqual(J.Int(wb, "tier"), s.badges[(int)z].tier, at + " bậc");
                Assert.AreEqual(J.Int(wb, "won"), s.badges[(int)z].won, at + " đã thắng");
                Assert.AreEqual(J.Int(o, "level"), s.level, at + " cấp");
                Assert.AreEqual(J.Int(o, "exp"), s.exp, at + " exp");
            }
        }

        [Test]
        public void ThuaKhongMatTienDo_PhanCongKhongCongDon_LuuDocLai()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            Assert.IsNull(Teams.MemberOf(s, "giot_suong", d).mods, "chưa có huy hiệu thì không có phần cộng");
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.badges[(int)Elem.Thuy].won = 3;
            // thua: không gọi Win, trận đang đánh vẫn là 4
            Assert.AreEqual((1, 4), Badges.Current(s, d.Cfg, Elem.Thuy).Value);
            s.badges[(int)Elem.Thuy].tier = 3;
            var m = Badges.Mods(s, d.Cfg, Elem.Thuy);
            Assert.AreEqual(0.12, m.hpPct, 1e-12, "bậc Vàng +12%, không cộng 5 + 8 + 12");
            var h = d.Hero("giot_suong");
            var plain = HeroStats.Compute(d.Cfg, h, 5, 1);
            var boosted = HeroStats.Compute(d.Cfg, h, 5, 1, false, Teams.MemberOf(s, "giot_suong", d).mods);
            Assert.AreEqual(plain.hp * 1.12, boosted.hp, 1.0);
            Assert.IsNull(Teams.MemberOf(s, "vo_su", d).mods, "hệ khác không được cộng");
            var json = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var back));
            Assert.AreEqual(3, back.badges[(int)Elem.Thuy].tier);
            Assert.AreEqual(3, back.badges[(int)Elem.Thuy].won);
        }
    }
}
