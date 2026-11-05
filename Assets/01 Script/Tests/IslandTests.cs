// Hệ thống 70 ải so với bản web (Golden/islands.json, lần xuất cuối 2026-11-03): cỡ đảo, mini boss đầu, rương mốc, bi lần đầu và
// đánh lại, đội địch từng ải (cấp, sao, thẻ, boss, phần cộng của địch khớp từng bit); lính tìm được nhưng không thu phục.
// Cập nhật bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md): sức địch đảo Thủy từ ải 4, ải 1 đảo Hỏa và Thổ.
// Cập nhật 2026-11-04 (cấp địch theo cấp người chơi, 14_HeThongAi.md): đảo Thủy cấp 1–15, các đảo sau dời lên 15–30.
// Cập nhật 2026-11-05: đảo Mộc thành 70 ải (Editor/IslandGen.cs), golden tính lại bằng menu "Tính lại golden islands.json".
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class IslandTests
    {
        static System.Collections.Generic.Dictionary<string, object> G => J.Obj(MiniJson.Parse(TestData.Read("Golden/islands.json")));

        [Test]
        public void CoDao_MiniBoss_RuongMoc_KhopBanWeb()
        {
            var d = TestData.Load();
            foreach (var x in J.Arr(G, "zones"))
            {
                var o = J.Obj(x);
                var z = Keys.ToElem(J.Str(o, "id"));
                Assert.AreEqual(J.Int(o, "size"), Islands.Size(z), Keys.Of(z) + " số ải");
                Assert.AreEqual(J.Int(o, "miniAt"), Islands.MiniAt(z), Keys.Of(z) + " mini boss đầu");
                CollectionAssert.AreEqual(J.Arr(o, "chests").Select(v => (int)(double)v).ToArray(), Islands.Chests(z), Keys.Of(z) + " rương");
                var lv = J.Arr(o, "level");
                Assert.AreEqual((int)(double)lv[0], d.Zone(z).levelMin, Keys.Of(z));
                Assert.AreEqual((int)(double)lv[1], d.Zone(z).levelMax, Keys.Of(z));
            }
            Assert.IsTrue(Islands.IsLong(Elem.Thuy));
            Assert.IsTrue(Islands.IsLong(Elem.Moc));
            Assert.IsTrue(Islands.IsLong(Elem.Hoa));
            Assert.IsFalse(Islands.IsLong(Elem.Kim));
        }

        [Test]
        public void TungAi_ThuongBi_DoiDich_KhopBanWeb()
        {
            var d = TestData.Load();
            var stages = J.Arr(G, "stages");
            Assert.AreEqual(d.Stages.Count, stages.Count);
            foreach (var x in stages)
            {
                var o = J.Obj(x);
                var st = d.Stage(J.Int(o, "id"));
                string at = $"ải {st.id}";
                Assert.AreEqual(J.Str(o, "tag"), Keys.Of(st.tag), at + " kiểu ải");
                if (st.tag != StageTag.None) Assert.AreEqual(J.Int(o, "chapter"), st.chapter, at + " chặng");
                var balls = J.Arr(o, "balls");
                Assert.AreEqual((int)(double)balls[0], Progress.StageBalls(d, st, true), at + " bi lần đầu");
                Assert.AreEqual((int)(double)balls[1], Progress.StageBalls(d, st, false), at + " bi đánh lại");
                var want = J.Arr(o, "members");
                var team = Teams.Enemy(st, d).members;
                Assert.AreEqual(want.Count, team.Count, at + " số địch");
                for (int i = 0; i < want.Count; i++)
                {
                    var w = J.Obj(want[i]);
                    var m = team[i];
                    string at2 = $"{at} địch {i + 1} ({m.heroId})";
                    Assert.AreEqual(J.Str(w, "hero"), m.heroId, at2);
                    Assert.AreEqual(J.Int(w, "level"), m.level, at2 + " cấp");
                    Assert.AreEqual(J.Int(w, "star"), m.star, at2 + " sao");
                    var cards = J.Arr(w, "cards");
                    Assert.AreEqual((int)(double)cards[0], m.cardSkill, at2);
                    Assert.AreEqual((int)(double)cards[1], m.cardUlt, at2);
                    Assert.AreEqual((int)(double)cards[2], m.cardPassive, at2);
                    Assert.AreEqual(J.Bool(w, "boss"), m.boss, at2 + " boss");
                    Assert.AreEqual(J.Bool(w, "evo"), m.evo, at2 + " tiến hóa");
                    Assert.AreEqual(J.Str(w, "trait"), m.trait, at2 + " bị động boss");
                    var mods = J.Obj(w, "mods");
                    if (mods == null)
                    {
                        Assert.IsNull(m.mods, at2 + " không có phần cộng");
                        continue;
                    }
                    Assert.IsNotNull(m.mods, at2 + " phần cộng");
                    Assert.AreEqual(J.Num(mods, "hpPct"), m.mods.hpPct, at2 + " máu");
                    Assert.AreEqual(J.Num(mods, "atkPct"), m.mods.atkPct, at2 + " công");
                    Assert.AreEqual(J.Num(mods, "defPct"), m.mods.defPct, at2 + " thủ");
                    Assert.AreEqual(J.Num(mods, "spd"), m.mods.spd, at2 + " tốc");
                }
            }
        }

        // bị động boss (người dùng dặn 2026-11-05): chỉ mini boss, boss ở 5 mốc cuối (ải 30–70); boss cuối đảo chắc chắn có; không phải
        // con nào cũng có; con có bị động chỉ số (cường hóa) thấp hơn con không có; trong trận bị động boss chạy như bị động thường
        [Test]
        public void BiDongBoss_5MocCuoi()
        {
            var d = TestData.Load();
            foreach (var z in new[] { Elem.Thuy, Elem.Moc })
            {
                var heads = d.ZoneStages(z).Where(st => st.tag == StageTag.Hero && st.idx >= 30).ToList();
                Assert.AreEqual(5, heads.Count, z + ": 5 mốc cuối");
                Assert.AreEqual(StageKind.Boss, heads[4].kind);
                Assert.IsNotNull(heads[4].enemies[0].trait, z + ": boss cuối đảo phải có bị động");
                var with = heads.Where(st => st.kind == StageKind.Mini && st.enemies[0].trait != null).ToList();
                var without = heads.Where(st => st.enemies[0].trait == null).ToList();
                Assert.IsNotEmpty(with, z + ": có mini boss mang bị động");
                Assert.IsNotEmpty(without, z + ": có mini boss không bị động");
                Assert.Less(with.Max(st => st.enemies[0].buff), without.Min(st => st.enemies[0].buff), z + ": có bị động thì cường hóa thấp hơn");
                foreach (var st in d.ZoneStages(z).Where(st => st.idx < 30))
                    Assert.IsTrue(st.enemies.All(e => e.trait == null), $"{z} ải {st.idx}: chỉ 5 mốc cuối có bị động");
            }
            foreach (var c in d.Traits)
            {
                Assert.AreEqual(CardKind.Passive, c.kind, c.id);
                Assert.IsNotNull(d.Hero(c.owner), c.id);
                Assert.IsTrue(d.Stages.Any(st => st.enemies.Any(e => e.trait == c.id && e.hero == c.owner)), c.id + " gắn cho đúng tướng");
            }
            // trận thật ở ải boss Mộc: bị động boss (phản đòn khi bị đánh) có chạy, và chỉ boss mới chạy
            var boss = d.ZoneStages(Elem.Moc).Last();
            var tr = boss.enemies[0].trait;
            var p = new TeamSetup { name = "Bạn", ai = true };
            foreach (var id in new[] { "bu_long", "meo_quyen" })
                p.members.Add(new Member { heroId = id, level = boss.enemies[0].level, star = 5, cardSkill = 5, cardUlt = 5, cardPassive = 5 });
            int fired = 0;
            for (uint seed = 1; seed <= 10; seed++)
            {
                var log = new List<BattleEvent>();
                BattleSim.Run(Battle.Create(d, p, Teams.Enemy(boss, d), seed), 0.15, log);
                foreach (var e in log.Where(e => e.t == EvType.Passive && e.card == tr))
                {
                    Assert.AreEqual(1, e.side, "bị động boss chỉ ở bên địch");
                    fired++;
                }
            }
            Assert.Greater(fired, 0, "bị động boss chạy trong trận");
            // dữ liệu trong game nạp từ asset Unity, nơi chuỗi null thành "": coi như không có bị động boss, trận vẫn chạy
            var plain = TestData.AtLevel(d.Stage(1), 1);
            foreach (var e in plain.enemies) e.trait = "";
            Assert.IsNull(Teams.Enemy(plain, d).members[0].trait);
            Assert.DoesNotThrow(() => BattleSim.Run(Battle.Create(d, p, Teams.Enemy(plain, d), 1)));
        }

        [Test]
        public void Linh_TimDuoc_KhongThuPhuc_KhongRoiManh()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            foreach (var m in d.Minions)
            {
                Assert.AreSame(m, d.Hero(m.id), m.id);
                Assert.IsTrue(m.minion, m.id);
                Assert.IsFalse(d.Heroes.Contains(m), m.id + " không nằm trong danh sách tướng");
                Assert.IsNull(s.Hero(m.id), m.id + " không có trong bản lưu");
                foreach (var id in new[] { m.skill, m.ult, m.passive }) Assert.IsNotNull(d.Card(id), id);
            }
            var used = d.Stages.SelectMany(st => st.enemies).Select(e => e.hero).Where(h => d.Hero(h).minion).Distinct().ToList();
            CollectionAssert.AreEquivalent(d.Minions.Select(m => m.id), used, "mọi lính đều có ải");
            Assert.IsFalse(d.Stages.SelectMany(st => st.drops).Any(dr => d.Hero(dr.hero).minion), "lính không rơi mảnh");
            // ải 1 Đảo Thủy: Giọt Sương (tướng khởi đầu hệ Thủy; người chọn nó thì đấu với bóng), yếu hơn 20%
            var first = d.Stage(1);
            Assert.AreEqual(StageTag.Hero, first.tag);
            Assert.AreEqual("giot_suong", first.enemies[0].hero);
            Assert.AreEqual(-0.2, first.enemies[0].buff, 1e-12);
        }
    }
}
