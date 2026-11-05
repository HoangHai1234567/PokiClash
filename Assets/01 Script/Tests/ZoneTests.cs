// Đảo hệ so với bản web (golden): thưởng ải lần đầu và đánh lại, tặng tướng, rương mốc;
// cùng luật mở ải lần lượt, độ khó, đảo gợi ý, điều kiện mở công trình side meta.
// zones.json (ải 1 rơi mảnh): tính lại bên Unity 2026-11-03 (5 tướng khởi đầu, GD_Claude/15_TuongKhoiDau.md).
using System;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class ZoneTests
    {
        static readonly string[] SlotKey = { "skill", "ult", "passive" };

        // ô đội theo cấp người chơi (15_TuongKhoiDau.md; web mở theo số đảo đã xong): lúc đầu 1 ô, ô 2 ở cấp 10, ô 3 ở cấp 30
        [Test]
        public void ODoi_MoTheoCapNguoiChoi()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            Assert.AreEqual(1, Progress.TeamSlots(s), "mới chơi");
            foreach (var e in Elements.All) s.zones[(int)e] = Islands.Size(e);
            Assert.AreEqual(1, Progress.TeamSlots(s), "xong hết đảo mà cấp 1 vẫn 1 ô");
            s.level = 59;
            Assert.AreEqual(1, Progress.TeamSlots(s), "cấp 59");
            s.level = 60;
            Assert.AreEqual(2, Progress.TeamSlots(s), "cấp 60");
            s.level = 199;
            Assert.AreEqual(2, Progress.TeamSlots(s), "cấp 199");
            s.level = 200;
            Assert.AreEqual(3, Progress.TeamSlots(s), "cấp 200");
            Assert.AreEqual("đạt cấp 60", Progress.SlotNeed(1));
            Assert.AreEqual("đạt cấp 200", Progress.SlotNeed(2));
        }

        [Test]
        public void ThuongAi_VaRuongMoc_KhopBanWeb()
        {
            var d = TestData.Load();
            var g = J.Obj(MiniJson.Parse(TestData.Read("Golden/zones.json")));
            var s = SaveData.New(d, 0);
            var r = new Rng(9);
            int k = 0;
            foreach (var x in J.Arr(g, "steps"))
            {
                var o = J.Obj(x);
                string at = $"bước {k++}";
                if (J.Str(o, "t") == "win")
                {
                    var rw = Progress.WinStage(s, d, J.Int(o, "id"), r);
                    Assert.AreEqual(J.Int(o, "balls"), rw.balls, at + " bi");
                    Assert.AreEqual(J.Bool(o, "first"), rw.first, at + " lần đầu");
                    var sh = J.Arr(o, "shards");
                    Assert.AreEqual(sh.Count, rw.shards.Count, at + " số lần mảnh");
                    for (int i = 0; i < sh.Count; i++)
                    {
                        var w = J.Arr(sh[i]);
                        Assert.AreEqual((string)w[0], rw.shards[i].hero, at);
                        Assert.AreEqual((double)w[1], rw.shards[i].n, at);
                        Assert.AreEqual((bool)w[2], rw.shards[i].unlocked, at);
                        Assert.AreEqual((double)w[3], rw.shards[i].converted, at);
                    }
                }
                else
                {
                    Keys.TryElem(J.Str(o, "z"), out var z);
                    var c = Progress.ClaimZoneChest(s, d, z, r);
                    var want = J.Obj(o, "r");
                    if (want == null)
                    {
                        Assert.IsNull(c, at + " chưa đủ ải");
                        continue;
                    }
                    Assert.IsNotNull(c, at);
                    Assert.AreEqual(J.Int(want, "balls"), c.balls, at + " bi rương");
                    Assert.AreEqual(J.Bool(want, "big"), c.big, at);
                    var cards = J.Arr(want, "cards");
                    Assert.AreEqual(cards.Count, c.cards.Count, at + " số thẻ");
                    for (int i = 0; i < cards.Count; i++)
                    {
                        var w = J.Arr(cards[i]);
                        Assert.AreEqual((string)w[0], c.cards[i].hero, at);
                        Assert.AreEqual((string)w[1], SlotKey[(int)c.cards[i].slot], at);
                        Assert.AreEqual((string)w[2], c.cards[i].card, at);
                        Assert.AreEqual((string)w[3], Keys.Of(c.cards[i].rarity), at);
                    }
                }
            }
            var end = J.Obj(g, "end");
            var zones = J.Obj(end, "zones");
            foreach (var e in Elements.All) Assert.AreEqual(J.Int(zones, Keys.Of(e)), s.zones[(int)e], "tiến độ " + e);
            var chests = J.Obj(end, "zoneChests");
            foreach (var e in Elements.All) Assert.AreEqual(J.Int(chests, Keys.Of(e)), s.zoneChests[(int)e], "rương " + e);
            Assert.AreEqual(J.Int(end, "balls"), s.balls);
            foreach (var kv in J.Obj(end, "clears")) Assert.AreEqual((int)(double)kv.Value, s.clears[int.Parse(kv.Key)], "số lần qua ải " + kv.Key);
            var owned = new List<string>();
            foreach (var h in d.Heroes) if (s.Hero(h.id).owned) owned.Add(h.id);
            CollectionAssert.AreEquivalent(J.Arr(end, "owned").ConvertAll(x => (string)x), owned);
        }

        [Test]
        public void MoAiLanLuot_DaoKhacKhongAnhHuong()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Thuy] = 2;
            var hoa = new List<StageDef>(d.ZoneStages(Elem.Hoa));
            Assert.IsTrue(Progress.StageOpen(s, hoa[0]), "ải 1 Đảo Hỏa mở ngay");
            Assert.IsFalse(Progress.StageOpen(s, hoa[1]), "ải 2 Đảo Hỏa khoá");
            var thuy = new List<StageDef>(d.ZoneStages(Elem.Thuy));
            Assert.IsTrue(Progress.StageCleared(s, thuy[1]));
            Assert.IsTrue(Progress.StageOpen(s, thuy[2]));
            Assert.IsFalse(Progress.StageOpen(s, thuy[3]));
            Assert.AreEqual(thuy[2].id, Progress.NextStage(s, d, Elem.Thuy).id);
        }

        [Test]
        public void ThuongAi_CongThuc()
        {
            var d = TestData.Load();
            // như nhau ở mọi đảo (đảo song song): 1 + (ải − 1)/14 bi, lần đầu ải tướng +2, mini boss +4, boss +8
            var boss = d.Stages.Find(x => x.zone == Elem.Thuy && x.kind == StageKind.Boss);
            Assert.AreEqual(70, boss.idx);
            Assert.AreEqual(5 + 8, Progress.StageBalls(d, boss, true), "boss Thủy ải 70, lần đầu");
            Assert.AreEqual(5, Progress.StageBalls(d, boss, false), "đánh lại boss Thủy");
            Assert.AreEqual(1 + 2, Progress.StageBalls(d, d.Stage(1), true), "ải 1: ải tướng");
            Assert.AreEqual(1, Progress.StageBalls(d, d.Stage(3), true), "ải 3: ải lính");
            var moc = d.ZoneStages(Elem.Moc).ToList();
            Assert.AreEqual(Progress.StageBalls(d, boss, true), Progress.StageBalls(d, moc[69], true), "boss Mộc bằng boss Thủy");
            Assert.AreEqual(2 + 4, Progress.StageBalls(d, moc[19], true), "mini boss Mộc ải 20");
            // đảo 8 ải (tạm, còn đảo Thổ): số ải quy về thang 70 ải, ải 8 như ải 70
            var thoBoss = d.ZoneStages(Elem.Tho).Last();
            Assert.AreEqual(8, thoBoss.idx);
            Assert.AreEqual(5 + 8, Progress.StageBalls(d, thoBoss, true));
            Assert.AreEqual(5, Progress.StageBalls(d, thoBoss, false), "đánh lại boss Thổ");
            Assert.AreEqual(Progress.StageBalls(d, boss, true), Progress.StageBalls(d, d.ZoneStages(Elem.Kim).Last(), true), "boss Kim bằng boss Thủy");
        }

        [Test]
        public void DoKho_VaDaoGoiY()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            // 5 đảo song song: đảo nào cũng bắt đầu từ cấp 1, boss cuối 190–200
            foreach (var z in d.Zones)
            {
                Assert.AreEqual(1, z.levelMin, z.name);
                Assert.That(z.levelMax, Is.InRange(190, 200), z.name);
                Assert.AreEqual(z.levelMax, d.ZoneStages(z.id).Max(st => st.enemies.Max(e => e.level)), z.name + ": boss cuối là cấp cao nhất");
                Assert.AreEqual(Progress.Difficulty.Fit, Progress.DifficultyOf(s, d, z), z.name + ": ải 1 Vừa sức");
            }
            Assert.AreEqual(Elem.Thuy, Progress.RecommendedZone(s, d).id, "bằng cấp thì theo thứ tự đảo");
            // độ khó theo ải kế tiếp: Thủy qua 8 ải
            s.zones[(int)Elem.Thuy] = 8;
            int next = Progress.NextLevel(s, d, Elem.Thuy);
            Assert.AreEqual(d.ZoneStages(Elem.Thuy).First(st => st.idx == 9).enemies.Max(e => e.level), next);
            s.level = next + Progress.EasyMargin;
            Assert.AreEqual(Progress.Difficulty.Easy, Progress.DifficultyOf(s, d, d.Zone(Elem.Thuy)));
            s.level = next;
            Assert.AreEqual(Progress.Difficulty.Fit, Progress.DifficultyOf(s, d, d.Zone(Elem.Thuy)));
            s.level = next - Progress.LevelSlack;
            Assert.AreEqual(Progress.Difficulty.Hard, Progress.DifficultyOf(s, d, d.Zone(Elem.Thuy)));
            s.level = next - Progress.LevelSlack - 1;
            Assert.AreEqual(Progress.Difficulty.Wall, Progress.DifficultyOf(s, d, d.Zone(Elem.Thuy)));
            Assert.AreNotEqual(Elem.Thuy, Progress.RecommendedZone(s, d).id, "Thủy đi trước: gợi ý đảo có ải kế cấp thấp hơn");
            foreach (var e in Elements.All) s.zones[(int)e] = Math.Min(8, Islands.Size(e) - 1);
            s.zones[(int)Elem.Moc] = 5;
            Assert.AreEqual(Elem.Moc, Progress.RecommendedZone(s, d).id, "Mộc chậm nhất (ải kế cấp thấp nhất)");
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            Assert.AreEqual("Đã chinh phục", Progress.DifficultyText(Progress.DifficultyOf(s, d, d.Zone(Elem.Thuy))));
            Assert.AreEqual(0, Progress.NextLevel(s, d, Elem.Thuy));
            Assert.AreEqual(Elem.Tho, Progress.CounterOf(Elem.Thuy), "Thổ khắc Thủy");
        }

        [Test]
        public void CongTrinhSideMeta_DieuKienMo()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            Assert.IsFalse(Progress.FarmOpen(s));
            Assert.IsFalse(Progress.BadgesOpen(s));
            Assert.IsFalse(Progress.CaveOpen(s));
            Progress.UnlockHero(s, "vo_su");
            Progress.UnlockHero(s, "nu_hoa");
            Assert.IsTrue(Progress.FarmOpen(s), "3 tướng mở Trang trại");
            // Đền Huy Hiệu: thắng mini boss đầu của một đảo bất kỳ (đảo song song)
            s.zones[(int)Elem.Moc] = Islands.MiniAt(Elem.Moc) - 1;
            Assert.IsFalse(Progress.BadgesOpen(s), "chưa hạ mini boss Mộc");
            s.zones[(int)Elem.Moc] = Islands.MiniAt(Elem.Moc);
            Assert.IsTrue(Progress.BadgesOpen(s), "hạ mini boss Mộc (ải 20)");
            // Hang Tiềm Năng: theo cấp người chơi
            s.level = Progress.CaveLevel - 1;
            Assert.IsFalse(Progress.CaveOpen(s));
            s.level = Progress.CaveLevel;
            Assert.IsTrue(Progress.CaveOpen(s));
        }
    }
}
