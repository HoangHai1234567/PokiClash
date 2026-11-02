// AFK so với bản web (golden afk.json): chạy lại từng bước (tính giờ, tăng tốc, nhận, mở rương, lùi giờ máy, lượt quảng cáo, tua)
// và so kết quả cùng toàn bộ trạng thái AFK sau mỗi bước. Thêm các tình huống của spec: đầy 12 giờ, tăng tốc rồi tắt game.
using System.Collections.Generic;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class AfkTests
    {
        const double H = 3600000;
        static readonly string[] SlotKey = { "skill", "ult", "passive" };

        [Test]
        public void ChayLaiTungBuoc_KhopBanWeb()
        {
            var d = TestData.Load();
            var g = J.Obj(MiniJson.Parse(TestData.Read("Golden/afk.json")));
            double t0 = J.Num(g, "t0");
            var s = SaveData.New(d, (long)t0);
            foreach (var id in new[] { "vo_su", "nu_hoa" }) s.Hero(id).owned = true;
            var rng = new Rng(21);
            int i = 0;
            foreach (var x in J.Arr(g, "steps"))
            {
                var st = J.Obj(x);
                string op = J.Str(st, "op");
                string at = $"bước {i++} ({op})";
                var want = J.Get(st, "r");
                switch (op)
                {
                    case "tick":
                        Assert.AreEqual((bool)want, Afk.Tick(s, d.Cfg, J.Num(st, "t")), at);
                        break;
                    case "pending":
                    {
                        var p = Afk.Pending(s, d.Cfg, J.Num(st, "t"));
                        var w = J.Obj(want);
                        Assert.AreEqual(J.Num(w, "hours"), p.hours, at);
                        Assert.AreEqual(J.Bool(w, "full"), p.full, at);
                        break;
                    }
                    case "boost":
                        Assert.AreEqual((bool)want, Afk.Boost(s, d.Cfg, J.Num(st, "t")), at);
                        break;
                    case "claim":
                    {
                        var c = Afk.Claim(s, d, J.Num(st, "t"), J.Int(st, "mult"), rng);
                        var w = J.Obj(want);
                        Assert.AreEqual(J.Num(w, "hours"), c.hours, at);
                        var ws = J.Arr(w, "shards");
                        Assert.AreEqual(ws.Count, c.shards.Count, at + " số lần ra mảnh");
                        for (int k = 0; k < ws.Count; k++)
                        {
                            var e = J.Arr(ws[k]);
                            Assert.AreEqual((string)e[0], c.shards[k].hero, at);
                            Assert.AreEqual((double)e[1], c.shards[k].n, at);
                        }
                        break;
                    }
                    case "open":
                        Rewards(Afk.OpenChest(s, d, J.Num(st, "t"), rng, J.Bool(st, "early")), want, at);
                        break;
                    case "ad":
                    {
                        var p = J.Str(st, "kind") == "open" ? AdGate.AfkChestOpen : AdGate.AfkBoost;
                        int day = J.Int(st, "day");
                        var w = J.Arr(want);
                        Assert.AreEqual((bool)w[0], AdGate.Use(s, d.Cfg, day, p), at);
                        Assert.AreEqual((double)w[1], AdGate.Left(s, d.Cfg, day, p), at);
                        break;
                    }
                    case "travel":
                        Afk.Travel(s, J.Num(st, "ms"));
                        break;
                    case "zone":
                        s.zones[(int)Keys.ToElem(J.Str(st, "zone"))] = J.Int(st, "n");
                        break;
                }
                State(s, d, st, at);
            }
        }

        static void Rewards(List<Reward> got, object want, string at)
        {
            if (want == null)
            {
                Assert.IsNull(got, at);
                return;
            }
            var w = J.Arr(want);
            Assert.IsNotNull(got, at);
            Assert.AreEqual(w.Count, got.Count, at);
            for (int k = 0; k < w.Count; k++)
            {
                var e = J.Arr(w[k]);
                var r = got[k];
                switch ((string)e[0])
                {
                    case "card":
                        Assert.AreEqual(RewardKind.Card, r.k, at);
                        Assert.AreEqual((string)e[1], r.drop.hero, at);
                        Assert.AreEqual((string)e[2], SlotKey[(int)r.drop.slot], at);
                        Assert.AreEqual((string)e[3], r.drop.card, at);
                        break;
                    case "exp":
                        Assert.AreEqual(RewardKind.Exp, r.k, at);
                        Assert.AreEqual((double)e[1], r.n, at);
                        break;
                    case "stones":
                        Assert.AreEqual(RewardKind.Stones, r.k, at);
                        break;
                    case "balls":
                        Assert.AreEqual(RewardKind.Balls, r.k, at);
                        Assert.AreEqual((double)e[1], r.n, at);
                        break;
                }
            }
        }

        static void State(SaveData s, GameData d, Dictionary<string, object> st, string at)
        {
            var a = J.Obj(st, "afk");
            Assert.AreEqual(J.Num(a, "hours"), s.afk.hours, at + " hours");
            Assert.AreEqual(J.Num(a, "lastTick"), s.afk.lastTick, at + " lastTick");
            Assert.AreEqual(J.Num(a, "boostUntil"), s.afk.boostUntil, at + " boostUntil");
            Assert.AreEqual(J.Num(a, "chestAcc"), s.afk.chestAcc, at + " chestAcc");
            Assert.AreEqual(J.Num(a, "chainAt"), s.afk.chainAt, at + " chainAt");
            var wc = J.Arr(a, "chests");
            Assert.AreEqual(wc.Count, s.afk.chests.Count, at + " số rương");
            for (int k = 0; k < wc.Count; k++) Assert.AreEqual((double)wc[k], s.afk.chests[k], at + " rương " + k);
            var times = Afk.ChestTimes(s, d.Cfg, J.Num(st, "t"));
            var wt = J.Arr(st, "times");
            for (int k = 0; k < wt.Count; k++) Assert.AreEqual(J.Num(J.Obj(wt[k]), "ready"), times[k].ready, at + " giờ mở " + k);
            Assert.AreEqual(J.Int(st, "balls"), s.balls, at + " bi");
            Assert.AreEqual(J.Int(st, "exp"), s.exp, at + " exp");
            Assert.AreEqual(J.Int(st, "level"), s.level, at + " cấp");
            Assert.AreEqual((long)J.Num(st, "afkSince"), s.afkSince, at + " afkSince");
        }

        [Test]
        public void Day12Gio_KhayDay_KhongRaBi()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Thuy] = 8;
            s.zones[(int)Elem.Hoa] = 2;
            var p = Afk.Pending(s, d.Cfg, 20 * H);
            Assert.AreEqual(12, p.hours);
            Assert.IsTrue(p.full);
            int balls = s.balls;
            Afk.Claim(s, d, 20 * H, 1, new Rng(3));
            Assert.AreEqual(balls, s.balls, "AFK không còn ra bi (bi ở cây bi)");
            Assert.AreEqual(4, s.afk.chests.Count, "khay đầy 4 rương");
        }

        [Test]
        public void TangToc_RoiTatGame5Gio_Bang7Gio()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Thuy] = 1;
            Assert.IsTrue(Afk.Boost(s, d.Cfg, 0));
            Assert.AreEqual(7, Afk.Pending(s, d.Cfg, 5 * H).hours, 1e-9);
            Assert.IsFalse(Afk.Tick(s, d.Cfg, 2 * H), "lùi giờ máy");
            Assert.AreEqual(7, Afk.Pending(s, d.Cfg, 2 * H).hours, 1e-9, "lùi giờ không trừ, không cộng");
        }

        [Test]
        public void BanLuuCu_KhongCoAfk_TinhTuAfkSince()
        {
            var d = TestData.Load();
            var json = SaveCodec.Write(SaveData.New(d, 1000)).Replace("\"afk\":{", "\"afk_cu\":{");
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(json, d, out var s));
            Assert.AreEqual(1000, s.afk.lastTick);
        }
    }
}
