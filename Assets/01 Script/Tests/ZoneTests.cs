// Đảo hệ so với bản web (golden): thưởng ải lần đầu và đánh lại, tặng tướng, rương mốc;
// cùng luật mở ải lần lượt, độ khó, đảo gợi ý, điều kiện mở công trình side meta.
using System.Collections.Generic;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class ZoneTests
    {
        static readonly string[] SlotKey = { "skill", "ult", "passive" };

        // ô đội mở theo số đảo đã xong (TEAM_SLOT_ZONES của bản web): 0 đảo 1 ô, 1 đảo 2 ô, 3 đảo 3 ô
        [Test]
        public void ODoi_MoTheoSoDaoDaXong()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            Assert.AreEqual(1, Progress.TeamSlots(s), "mới chơi");
            s.zones[(int)Elem.Thuy] = 7;
            Assert.AreEqual(1, Progress.TeamSlots(s), "chưa hạ boss Thủy");
            s.zones[(int)Elem.Thuy] = 8;
            Assert.AreEqual(2, Progress.TeamSlots(s), "xong 1 đảo");
            s.zones[(int)Elem.Hoa] = 8;
            Assert.AreEqual(2, Progress.TeamSlots(s), "xong 2 đảo");
            s.zones[(int)Elem.Kim] = 8;
            Assert.AreEqual(3, Progress.TeamSlots(s), "xong 3 đảo");
            s.zones[(int)Elem.Moc] = s.zones[(int)Elem.Tho] = 8;
            Assert.AreEqual(3, Progress.TeamSlots(s), "tối đa 3");
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
            var boss8 = d.Stage(8);
            Assert.AreEqual(3 + 0 + 3 + 5 + 7, Progress.StageBalls(d, boss8, true));
            Assert.AreEqual(6, Progress.StageBalls(d, boss8, false), "đánh lại boss Thủy: 6 bi cơ bản");
            Assert.AreEqual(9, Progress.StageBalls(d, d.Stage(3), true), "ải 3 Đảo Thủy: +9 bi");
        }

        [Test]
        public void DoKho_VaDaoGoiY()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            Assert.AreEqual(Progress.Difficulty.Fit, Progress.DifficultyOf(d.Zone(Elem.Thuy), 1, false), "Đảo Thủy: Vừa sức");
            foreach (var e in new[] { Elem.Hoa, Elem.Kim, Elem.Moc, Elem.Tho })
                Assert.AreEqual(Progress.Difficulty.Wall, Progress.DifficultyOf(d.Zone(e), 1, false), e + ": Quá mạnh!");
            Assert.AreEqual(Elem.Thuy, Progress.RecommendedZone(s, d).id);
            s.zones[(int)Elem.Thuy] = 8;
            s.level = 4;
            Assert.AreEqual(Elem.Hoa, Progress.RecommendedZone(s, d).id, "xong Thủy, cấp 4: gợi ý Hỏa");
            Assert.AreEqual("Đã chinh phục", Progress.DifficultyText(Progress.DifficultyOf(d.Zone(Elem.Thuy), 4, true)));
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
            s.zones[(int)Elem.Thuy] = 8;
            Assert.IsTrue(Progress.BadgesOpen(s));
            s.zones[(int)Elem.Hoa] = 4;
            Assert.IsTrue(Progress.CaveOpen(s));
        }
    }
}
