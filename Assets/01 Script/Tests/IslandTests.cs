// Hệ thống 70 ải so với bản web (Golden/islands.json, lần xuất cuối 2026-11-03): cỡ đảo, mini boss đầu, rương mốc, bi lần đầu và
// đánh lại, đội địch từng ải (cấp, sao, thẻ, boss, phần cộng của địch khớp từng bit); lính tìm được nhưng không thu phục.
// Cập nhật bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md): sức địch đảo Thủy từ ải 4, ải 1 đảo Hỏa và Thổ.
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
            Assert.IsFalse(Islands.IsLong(Elem.Hoa));
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
