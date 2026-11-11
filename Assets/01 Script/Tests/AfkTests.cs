// AFK theo golden afk.json: chạy lại từng bước (tính giờ, tăng tốc, nhận, mở rương, lùi giờ máy, lượt quảng cáo, tua, đổi ải AFK)
// và so kết quả cùng toàn bộ trạng thái AFK sau mỗi bước. Golden chụp từ web rồi tính lại bên Unity khi đổi sang AFK theo ải
// (2026-11-03: mảnh rơi theo ải AFK, có thêm bước "stage"). Thêm các tình huống của spec: đầy 12 giờ, tăng tốc rồi tắt game; và của
// AFK theo ải: ải tự chọn, mảnh đúng tướng của ải, đổi ải giữ phần giờ lẻ.
using System.Collections.Generic;
using System.Linq;
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
                        Claim(Afk.Claim(s, d, J.Num(st, "t"), J.Int(st, "mult"), rng), want, at);
                        break;
                    case "stage":
                        Claim(Afk.SetStage(s, d, J.Int(st, "id"), J.Num(st, "t"), rng), want, at);
                        break;
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

        static void Claim(AfkClaim c, object want, string at)
        {
            if (want == null)
            {
                Assert.IsNull(c, at);
                return;
            }
            var w = J.Obj(want);
            Assert.IsNotNull(c, at);
            Assert.AreEqual(J.Num(w, "hours"), c.hours, at);
            Assert.AreEqual(J.Int(w, "stage"), c.stage, at + " ải AFK");
            var ws = J.Arr(w, "shards");
            Assert.AreEqual(ws.Count, c.shards.Count, at + " số lần ra mảnh");
            for (int k = 0; k < ws.Count; k++)
            {
                var e = J.Arr(ws[k]);
                Assert.AreEqual((string)e[0], c.shards[k].hero, at);
                Assert.AreEqual((double)e[1], c.shards[k].n, at);
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
            Assert.AreEqual(J.Int(a, "stage"), s.afk.stage, at + " stage");
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
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
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

        // ---------- AFK theo ải ----------

        static StageDef Thuy(GameData d, int idx) => d.ZoneStages(Elem.Thuy).First(x => x.idx == idx);

        [Test]
        public void AiTuChon_AiXaNhatCoRoiManh()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            Assert.IsNull(Afk.Stage(s, d), "chưa qua ải nào");
            s.zones[(int)Elem.Thuy] = 31; // ải 31 không rơi mảnh
            Assert.AreEqual(30, Afk.Stage(s, d).idx);
            s.zones[(int)Elem.Thuy] = 2; // ải 2 không rơi mảnh, ải 1 rơi Tí Tách
            Assert.AreEqual(1, Afk.Stage(s, d).idx);
            Assert.IsFalse(Afk.Picked(s, Thuy(d, 1)), "ải tự chọn không tính là đã chọn");
        }

        [Test]
        public void ChonAi_ManhDungTuongCuaAi_DoiAiGiuGioLe()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.zones[(int)Elem.Thuy] = 30;
            var gate = Thuy(d, 29); // Cửa ải: Sò Ngọc, Hà Bá (suất của Ma Kết, Mi Nhi tới 2026-11-11, cùng độ hiếm)
            Assert.IsNull(Afk.SetStage(s, d, Thuy(d, 31).id, 0, new Rng(1)), "ải chưa qua");
            Assert.IsNotNull(Afk.SetStage(s, d, gate.id, 0, new Rng(1)));
            Assert.AreEqual(gate.id, Afk.Stage(s, d).id);
            Assert.IsTrue(Afk.Picked(s, gate));

            var heroes = new HashSet<string>();
            var rng = new Rng(7);
            for (int i = 1; i <= 40; i++)
                foreach (var x in Afk.Claim(s, d, i * 12 * H, 1, rng).shards) heroes.Add(x.hero);
            CollectionAssert.IsSubsetOf(heroes, new[] { "so_ngoc", "ha_ba" });
            Assert.AreEqual(2, heroes.Count, "40 lần × 12 giờ: ra mảnh cả hai tướng của ải");

            // đổi ải sau 5,5 giờ: 5 giờ tròn tính theo ải cũ và nhận luôn, giữ 0,5 giờ
            var r = Afk.SetStage(s, d, Thuy(d, 15).id, (40 * 12 + 5.5) * H, rng);
            Assert.AreEqual(gate.id, r.stage);
            Assert.AreEqual(5, r.hours);
            Assert.AreEqual(0.5, s.afk.hours, 1e-9);
            Assert.AreEqual(Thuy(d, 15).id, Afk.Stage(s, d).id);
            Assert.AreEqual(0, Afk.SetStage(s, d, Thuy(d, 15).id, (40 * 12 + 6) * H, rng).hours, "chọn lại đúng ải đang AFK: không nhận gì");
        }

        [Test]
        public void BanLuu_GiuAiAfk()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            s.afk.stage = 15;
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var back));
            Assert.AreEqual(15, back.afk.stage);
        }
    }
}
