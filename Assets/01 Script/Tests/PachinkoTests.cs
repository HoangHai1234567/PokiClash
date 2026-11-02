// Máy bi so với bản web (golden): 6.000 bi cùng cách thả (tỉ lệ từng ô lệch dưới 1 điểm phần trăm, không bi nào kẹt),
// 600 lần mở rương ở ×1/×3/×5 khớp từng thưởng, mốc Huyền thoại cả hai nhánh, ×N nhân thưởng ô, giới hạn mỗi đợt theo cấp.
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class PachinkoTests
    {
        static Dictionary<string, object> golden;
        static Dictionary<string, object> G => golden ??= J.Obj(MiniJson.Parse(TestData.Read("Golden/pachinko.json")));
        static readonly string[] SlotKey = { "skill", "ult", "passive" };

        static string LandKey(PEvent e) => e.cup ? $"cup:{Pachinko.Key(e.reward)}" : $"slot{e.slot}:{Pachinko.Key(e.reward)}";

        [Test]
        public void ThaBi6000_TiLeKhopBanWeb_KhongKet()
        {
            var g = J.Obj(G, "drop");
            int total = J.Int(g, "total");
            var board = new Board(7);
            var count = new Dictionary<string, int>();
            var first = new List<string>();
            int landed = 0, dropped = 0, frame = 0;
            while (landed < total && frame < 200000)
            {
                if (dropped < total && frame % 6 == 0)
                {
                    board.Drop(Board.BW / 2 + ((dropped * 0.6180339887498949 % 1) * 2 - 1) * Board.Swing, 1);
                    dropped++;
                }
                foreach (var e in board.Step(1.0 / 60))
                {
                    if (!e.land) continue;
                    landed++;
                    var k = LandKey(e);
                    count[k] = count.TryGetValue(k, out var c) ? c + 1 : 1;
                    if (first.Count < 400) first.Add(k);
                }
                frame++;
            }
            Assert.AreEqual(total, landed, "mọi bi đều rơi vào ô hoặc cốc");
            var want = J.Obj(g, "landCount");
            var fails = new List<string>();
            foreach (var k in want.Keys.Union(count.Keys))
            {
                double pw = J.Num(want, k) / total * 100, pu = (count.TryGetValue(k, out var c) ? c : 0) / (double)total * 100;
                if (System.Math.Abs(pw - pu) >= 1) fails.Add($"{k}: web {pw:0.00}%, unity {pu:0.00}%");
            }
            Assert.IsEmpty(fails, string.Join("\n", fails));
            var wf = J.Arr(g, "firstLands");
            int same = 0;
            for (int i = 0; i < wf.Count && i < first.Count && (string)wf[i] == first[i]; i++) same++;
            TestContext.WriteLine($"Trùng từng bi với web: {same}/{wf.Count} bi đầu; khung {frame} (web {J.Int(g, "frames")})");
            // sin/cos góc lệch là đa thức (Board.SinSmall/CosSmall), mọi phép còn lại là IEEE: Unity và web ra cùng từng bi
            Assert.AreEqual(wf.Count, same, "400 bi đầu rơi vào cùng chỗ với web");
            Assert.AreEqual(J.Int(g, "frames"), frame, "cùng số khung");
        }

        [Test]
        public void MoRuong600Lan_KhopBanWeb()
        {
            var d = TestData.Load();
            var c = J.Obj(G, "chest");
            var s = SaveData.New(d, 0);
            foreach (var id in new[] { "vo_su", "nu_hoa", "ca_ngua" }) s.Hero(id).owned = true;
            s.zones[(int)Elem.Thuy] = 8;
            var r = new Rng(11);
            int i = 0;
            foreach (var x in J.Arr(c, "opens"))
            {
                var o = J.Obj(x);
                var kind = Pachinko.FromKey(J.Str(o, "kind"));
                var got = Pachinko.OpenChest(s, d, kind, J.Int(o, "x"), r);
                var want = J.Arr(o, "r");
                string at = $"lần {i++} ({J.Str(o, "kind")} ×{J.Int(o, "x")})";
                Assert.AreEqual(want.Count, got.Count, at + " số thưởng");
                for (int k = 0; k < want.Count; k++)
                {
                    var w = J.Arr(want[k]);
                    var g = got[k];
                    switch ((string)w[0])
                    {
                        case "card":
                            Assert.AreEqual(RewardKind.Card, g.k, at);
                            Assert.AreEqual((string)w[1], g.drop.hero, at);
                            Assert.AreEqual((string)w[2], SlotKey[(int)g.drop.slot], at);
                            Assert.AreEqual((string)w[3], g.drop.card, at);
                            Assert.AreEqual((string)w[4], Keys.Of(g.drop.rarity), at);
                            break;
                        case "shards":
                            Assert.AreEqual(RewardKind.Shards, g.k, at);
                            Assert.AreEqual((string)w[1], g.res.hero, at);
                            Assert.AreEqual((double)w[2], g.res.n, at);
                            Assert.AreEqual((bool)w[3], g.res.unlocked, at);
                            Assert.AreEqual((double)w[4], g.res.converted, at);
                            break;
                        case "exp":
                            Assert.AreEqual(RewardKind.Exp, g.k, at);
                            Assert.AreEqual((double)w[1], g.n, at);
                            Assert.AreEqual((double)w[2], g.ups, at);
                            break;
                        case "stones":
                            Assert.AreEqual(RewardKind.Stones, g.k, at);
                            break;
                        case "balls":
                            Assert.AreEqual(RewardKind.Balls, g.k, at);
                            Assert.AreEqual((double)w[1], g.n, at);
                            break;
                    }
                }
            }
            var save = J.Obj(c, "save");
            Assert.AreEqual(J.Int(save, "level"), s.level);
            Assert.AreEqual(J.Int(save, "exp"), s.exp);
            Assert.AreEqual(J.Int(save, "balls"), s.balls);
        }

        [Test]
        public void MocHuyenThoai_HaiNhanh()
        {
            var d = TestData.Load();
            var lg = J.Obj(G, "legend");
            foreach (var owned in new[] { false, true })
            {
                var want = J.Obj(lg, owned ? "owned" : "fresh");
                var s = SaveData.New(d, 0);
                s.balls = 1000;
                if (owned) s.Hero("ca_sa").owned = true;
                int at = -1;
                Reward got = null;
                for (int i = 0; i < 120 && at < 0; i++)
                {
                    var r = Pachinko.SpendBall(s, d, 3);
                    if (r != null)
                    {
                        at = s.ballsSpent;
                        got = r;
                    }
                }
                Assert.AreEqual(J.Int(want, "at"), at, "vượt mốc ở");
                var wr = J.Obj(want, "reward");
                if (!owned)
                {
                    Assert.AreEqual(RewardKind.Hero, got.k);
                    Assert.AreEqual("ca_sa", got.hero);
                    Assert.IsTrue(s.Hero("ca_sa").owned);
                }
                else
                {
                    Assert.AreEqual(RewardKind.LegendCopies, got.k);
                    Assert.AreEqual(J.Str(wr, "slot"), SlotKey[(int)got.slot]);
                    Assert.AreEqual(15, got.n);
                    Assert.AreEqual(15, s.Hero("ca_sa").Card(got.slot).copies);
                }
                Assert.IsNull(Pachinko.SpendBall(s, d, 3), "chỉ một lần");
            }
        }

        [Test]
        public void CuocXN_NhanThuongO_VaGioiHanDot()
        {
            var d = TestData.Load();
            var s = SaveData.New(d, 0);
            var r = Pachinko.SlotReward(s, d.Cfg, SlotKind.Exp15, 3);
            Assert.AreEqual(45, r.n, "ô EXP 15 ở ×3: +45 XP");
            int balls = s.balls;
            Pachinko.SlotReward(s, d.Cfg, SlotKind.Ball, 5);
            Assert.AreEqual(balls + 5, s.balls);
            Assert.AreEqual(RewardKind.Chest, Pachinko.SlotReward(s, d.Cfg, SlotKind.ChestGold, 2).k);
            Assert.AreEqual(20, d.Cfg.MaxPerDrop(5));
            Assert.AreEqual(30, d.Cfg.MaxPerDrop(15));
            CollectionAssert.AreEqual(new[] { 1, 2, 3 }, Progress.XAllowed(new SaveData { level = 5 }, d.Cfg));
        }

        [Test]
        public void MatMay_KetVangVaOKhuat()
        {
            var b = new Board(1);
            var vault = b.cups.Where(c => c.r == 0).ToList();
            Assert.AreEqual(1, vault.Count, "một két chữ nhật");
            Assert.AreEqual(SlotKind.ChestGold, vault[0].reward);
            Assert.AreEqual(2, b.cups.Count(c => c.r > 0 && c.reward == SlotKind.ChestSilver), "hai cốc bạc");
            Assert.AreEqual(Board.SlotLayout.Length, b.slots.Count);
            int mid = b.slots.Count / 2;
            Assert.AreEqual(SlotKind.ChestGold, b.slots[mid].reward, "ô giữa là ô vàng khuất");
            // ô vàng khuất nằm trọn dưới đáy két
            Assert.LessOrEqual(Board.VaultX - Board.FloorHalf, b.slots[mid].x0);
            Assert.GreaterOrEqual(Board.VaultX + Board.FloorHalf, b.slots[mid].x1);
            Assert.AreEqual(Board.Right - Board.Left, Board.SlotW.Sum(), 1e-9, "tổng độ rộng ô bằng bề ngang máy");
            foreach (var s in b.slots) Assert.GreaterOrEqual(s.x1 - s.x0, 22, "ô đủ rộng cho bi 18");
            Assert.AreEqual(2, b.segs.Count(s => s.kind == SegKind.Roof));
            Assert.AreEqual(2, b.segs.Count(s => s.kind == SegKind.Floor));
            Assert.AreEqual(Board.SlotLayout.Length - 1, b.segs.Count(s => s.kind == SegKind.Divider));
        }

        [Test]
        public void SinCosGocNho_SaiSoDuoi1e13()
        {
            for (int i = -200; i <= 200; i++)
            {
                double x = i * 0.001;
                Assert.AreEqual(System.Math.Sin(x), Board.SinSmall(x), 1e-13, "sin " + x);
                Assert.AreEqual(System.Math.Cos(x), Board.CosSmall(x), 1e-13, "cos " + x);
            }
        }

        [Test]
        public void BangTiLe_CoDuBayLoaiO_TongBangMot()
        {
            var cfg = TestData.Load().Cfg;
            Assert.AreEqual(6000, cfg.ratesBalls);
            foreach (SlotKind k in System.Enum.GetValues(typeof(SlotKind))) Assert.Greater(cfg.Rate(Pachinko.Key(k)), 0.02, Pachinko.Key(k));
            Assert.AreEqual(1, cfg.rates.Sum(r => r.p), 0.002);
        }
    }
}
