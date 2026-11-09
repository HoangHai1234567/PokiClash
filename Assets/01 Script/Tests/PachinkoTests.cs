// Máy bi: bàn chép máy tham khảo (hình học, vật liệu), 6.000 bi phóng theo bảng tỉ lệ (mỗi bi rơi đúng kết quả đã chọn, tỉ lệ
// lệch bảng dưới 4 độ lệch chuẩn, không bi nào kẹt, cùng hạt giống ra cùng kết quả), vòng nấm; so với bản web (golden): 600 lần mở rương
// ở ×1/×3/×5 khớp từng thưởng, mốc Huyền thoại cả hai nhánh; ×N nhân thưởng ô, giới hạn mỗi đợt theo cấp.
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

        // phóng total bi, mỗi 10 khung một bi (như giữ nút thả); trả về kết quả từng bi theo thứ tự phóng
        static List<int> Drop(Board board, int total, out int frames, out double maxAge)
        {
            var byId = new SortedDictionary<int, int>();
            int dropped = 0, frame = 0;
            maxAge = 0;
            while (byId.Count < total && frame < 400000)
            {
                if (dropped < total && frame % 10 == 0)
                {
                    board.Launch(1);
                    dropped++;
                }
                foreach (var e in board.Step())
                {
                    if (!e.land) continue;
                    int o = board.OutcomeOf(e);
                    if (e.ball.target >= 0) Assert.AreEqual(e.ball.target, o, "bi rơi đúng kết quả đã chọn");
                    byId[e.ball.id] = o;
                    maxAge = System.Math.Max(maxAge, e.ball.age);
                }
                frame++;
            }
            frames = frame;
            return byId.Values.ToList();
        }

        [Test]
        public void ThaBi6000_TiLeTheoBang_KhongKet_ChayLaiGiongNhau()
        {
            var cfg = TestData.Load().Cfg;
            const int total = 6000;
            var board = new Board(7) { odds = cfg.odds };
            var outs = Drop(board, total, out int frames, out double maxAge);
            Assert.AreEqual(total, outs.Count, "mọi bi đều rơi vào ô hoặc cốc");
            Assert.AreEqual(0, board.misses, "lần nào cũng tìm được đường bi đúng kết quả");
            Assert.Less(maxAge, 20, "không bi nào kẹt");
            double sum = cfg.odds.Sum();
            var fails = new List<string>();
            for (int i = 0; i < board.Outcomes; i++)
            {
                double want = cfg.odds[i] / sum * 100, got = outs.Count(o => o == i) * 100.0 / total;
                double sigma = System.Math.Sqrt(want * (100 - want) / total); // độ lệch chuẩn do chọn ngẫu nhiên (điểm %)
                if (System.Math.Abs(want - got) > 4 * sigma) fails.Add($"kết quả {i}: bảng {want:0.0}%, ra {got:0.00}%");
            }
            Assert.IsEmpty(fails, string.Join("\n", fails));
            TestContext.WriteLine($"{board.tries / (double)total:0.00} lần thử vật lý mỗi bi, {frames / 60.0:0} giây máy");
            var again = Drop(new Board(7) { odds = cfg.odds }, 400, out _, out _);
            CollectionAssert.AreEqual(outs.Take(400).ToList(), again, "cùng hạt giống thì cùng kết quả");
        }

        [Test]
        public void VatLyThuan_CocTheNhieuHonHanBang()
        {
            // lý do phải chọn kết quả trước: vật lý thuần của chính bàn này cho cốc thẻ khoảng 20 %, bảng công bố chỉ 3,3 %
            var board = new Board(3);
            var outs = Drop(board, 1500, out _, out _);
            double cup = outs.Count(o => o == board.slots.Count) * 100.0 / outs.Count;
            Assert.Greater(cup, 8);
            TestContext.WriteLine($"Vật lý thuần: cốc thẻ {cup:0.0}%");
        }

        [Test]
        public void MoRuong600Lan_KhopBanWeb()
        {
            var d = TestData.Load();
            var c = J.Obj(G, "chest");
            var s = SaveData.New(d, 0);
            foreach (var id in new[] { "vo_su", "nu_hoa", "ca_ngua" }) s.Hero(id).owned = true;
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
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
            Assert.AreEqual(30, d.Cfg.MaxPerDrop(104));
        }

        [Test]
        public void CuocMoTheoSoBiDangCo()
        {
            var cfg = TestData.Load().Cfg;
            int need3 = cfg.xSteps.Find(q => q.x == 3).balls, need10 = cfg.xSteps.Find(q => q.x == 10).balls;
            Assert.Greater(need3, 0, "×3 cần giữ bi mới mở");
            CollectionAssert.AreEqual(new[] { 1, 2 }, Progress.XAllowed(new SaveData { balls = 0, level = 200 }, cfg), "cấp cao không mở cược");
            CollectionAssert.AreEqual(new[] { 1, 2, 3 }, Progress.XAllowed(new SaveData { balls = need3 }, cfg));
            Assert.AreEqual(2, Progress.XBest(new SaveData { balls = need3 - 1 }, cfg, 10), "tụt dưới mốc ×3 thì về ×2");
            Assert.AreEqual(10, Progress.XBest(new SaveData { balls = need10 }, cfg, 10));
            Assert.AreEqual(3, Progress.XBest(new SaveData { balls = need10 }, cfg, 3), "không vượt mức đang chọn");
        }

        [Test]
        public void MocQua_SauHuyenThoai_TinhTheoBiVaVongLai()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            Assert.GreaterOrEqual(cfg.gifts.Count, 2);
            var s = SaveData.New(d, 0);
            s.balls = 100000;
            // trước mốc Huyền thoại: không tính
            Reward legend = null;
            while (legend == null)
            {
                legend = Pachinko.SpendBall(s, d, 7);
                if (legend == null) Assert.AreEqual(0, Pachinko.GiftCredit(s, cfg, 7, legend));
            }
            // lần thả vượt mốc chỉ tính phần dư
            int over = s.ballsSpent - cfg.legendMilestone;
            Assert.AreEqual(over, Pachinko.GiftCredit(s, cfg, 7, legend));
            Assert.AreEqual(0, Pachinko.GiftAdd(s, d, over).Count);
            Assert.AreEqual(over, s.gift);
            // đủ n của mốc đang chạy thì nhận đúng quà, phần dư sang mốc kế; hết bảng thì vòng lại
            var first = Pachinko.GiftAdd(s, d, cfg.gifts[0].n - over + 1);
            Assert.AreEqual(1, first.Count);
            Assert.AreEqual(1, s.giftTier);
            Assert.AreEqual(1, s.gift, "phần dư sang mốc kế");
            for (int i = 1; i <= cfg.gifts.Count; i++)
            {
                var g = cfg.gifts[i % cfg.gifts.Count];
                Assert.AreSame(g, Pachinko.GiftNow(s, cfg));
                int b = s.balls;
                var got = Pachinko.GiftAdd(s, d, g.n);
                Assert.AreEqual(1, got.Count, $"mốc {i}");
                if (g.k == "balls") Assert.AreEqual(b + g.v, s.balls);
                else if (g.k == "exp") Assert.AreEqual(RewardKind.Exp, got[0].k);
                else Assert.AreEqual(Pachinko.FromKey(g.k), got[0].chest);
            }
            Assert.AreEqual(cfg.gifts.Count + 1, s.giftTier);
            Assert.AreEqual(1, s.gift);
            // lưu rồi đọc lại giữ mốc
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var back));
            Assert.AreEqual(s.gift, back.gift);
            Assert.AreEqual(s.giftTier, back.giftTier);
        }

        [Test]
        public void MatMay_ChepBanThamKhao()
        {
            var b = new Board(1);
            const double U = Board.U;
            Assert.AreEqual(0.081 * U, Board.BallR, 1e-9, "bi r 0,081 u");
            Assert.AreEqual(22, b.pegs.Count(p => p.kind == PegKind.Peg), "22 đinh");
            Assert.IsTrue(b.pegs.Where(p => p.kind == PegKind.Peg).All(p => System.Math.Abs(p.r - 0.15 * U) < 1e-9 && p.e == 0.8 && p.f == 0));
            var top = b.pegs[b.topPeg];
            Assert.AreEqual(PegKind.Top, top.kind);
            Assert.AreEqual(0.9, top.e, "nấm đỉnh nảy 0,9");
            foreach (int i in b.ringPeg)
            {
                Assert.AreEqual(PegKind.Bumper, b.pegs[i].kind);
                Assert.AreEqual(0.55 * U, b.pegs[i].r, 1e-9);
                Assert.AreEqual(Board.Fric, b.pegs[i].f);
            }
            Assert.Less(b.pegs[b.ringPeg[0]].x, b.pegs[b.ringPeg[1]].x, "nấm 0 bên trái");
            Assert.AreEqual(4, b.segs.Count(s => s.kind == SegKind.Roof), "mái hai cánh, mỗi cánh hai thanh");
            Assert.AreEqual(2, b.segs.Count(s => s.kind == SegKind.Floor), "đáy V hai thanh");
            Assert.AreEqual(4, b.segs.Count(s => s.kind == SegKind.Divider), "4 vách ô");
            Assert.AreEqual(25, b.segs.Count(s => s.kind == SegKind.Wall), "khung 26 điểm");
            Assert.AreEqual(5, b.slots.Count);
            Assert.AreEqual(Board.SlotLayout.Length + 1, b.Outcomes);
            Assert.AreEqual(1, b.cups.Count);
            Assert.AreEqual(SlotKind.ChestSilver, b.cups[0].reward, "cốc dưới mái: rương bạc");
            // ô khuất giữa đáy nằm dưới đáy V (đáy V che trọn bề ngang ô)
            var mid = b.slots[2];
            Assert.AreEqual(SlotKind.ChestGold, mid.reward);
            var floor = b.segs.Where(s => s.kind == SegKind.Floor).ToList();
            Assert.LessOrEqual(floor.Min(s => System.Math.Min(s.x1, s.x2)) - floor[0].r, mid.x0);
            Assert.GreaterOrEqual(floor.Max(s => System.Math.Max(s.x1, s.x2)) + floor[0].r, mid.x1);
            // khe đỉnh mái lọt bi: hai đầu trong của mái cách nhau hơn đường kính bi (đã trừ bề dày thanh)
            var roof = b.segs.Where(s => s.kind == SegKind.Roof).ToList();
            double inL = roof.Where(s => s.x1 < Board.X(0)).Max(s => System.Math.Max(s.x1, s.x2));
            double inR = roof.Where(s => s.x1 > Board.X(0)).Min(s => System.Math.Min(s.x1, s.x2));
            Assert.Greater(inR - inL - 2 * roof[0].r, 2 * Board.BallR, "khe đỉnh mái");
            // mọi thứ nằm trong khung máy
            Assert.IsTrue(b.lane.All(q => q.x > 0 && q.x < Board.BW && q.y > 0 && q.y < Board.BH), "làn phóng trong khung máy");
            Assert.IsTrue(b.pegs.All(p => p.x > 0 && p.x < Board.BW && p.y - p.r > -1 && p.y < Board.BH));
        }

        [Test]
        public void MatMay_AnhGhepKhopHinhHoc()
        {
            // ảnh mặt máy tĩnh ghép theo ArtGen/Pachinko/refs/mat_may.json: file phải khớp hình học trong code
            var path = System.IO.Path.Combine(TestData.DataDir, "..", "..", "ArtGen", "Pachinko", "refs", "mat_may.json");
            Assert.IsTrue(System.IO.File.Exists(path), "thiếu " + path);
            string want = new Board(1).GeometryJson().Replace("\r\n", "\n"), got = System.IO.File.ReadAllText(path).Replace("\r\n", "\n");
            Assert.AreEqual(want, got, "đổi bàn thì chạy menu \"PokiClash/Prefab/Máy bi: xuất hình học mặt máy\" rồi ghep_ban.py");
        }

        [Test]
        public void VongNam_DuNNacRaQua_PhanDuGiuLai()
        {
            var d = TestData.Load();
            var cfg = d.Cfg;
            Assert.AreEqual(2, cfg.rings.Count, "hai vòng nấm");
            var s = SaveData.New(d, 0);
            var g = cfg.rings[1];
            int balls = s.balls;
            for (int i = 0; i < g.n - 1; i++) Assert.IsEmpty(Pachinko.RingHit(s, cfg, 1, 1));
            var got = Pachinko.RingHit(s, cfg, 1, 1);
            Assert.AreEqual(1, got.Count);
            Assert.AreEqual(0, s.rings[1]);
            if (g.k == "balls") Assert.AreEqual(balls + g.v, s.balls);
            // cược ×N: mỗi lần chạm N nấc, dư giữ lại
            var c = cfg.rings[0];
            got = Pachinko.RingHit(s, cfg, 0, c.n + 3);
            Assert.AreEqual(1, got.Count);
            Assert.AreEqual(3, s.rings[0]);
            Assert.AreEqual(RewardKind.Chest, got[0].k);
            Assert.AreEqual(Pachinko.FromKey(c.k), got[0].chest);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(s), d, out var back));
            CollectionAssert.AreEqual(s.rings, back.rings, "lưu rồi đọc lại giữ vòng nấm");
        }

        [Test]
        public void BangTiLe_TheoOdds_TongBangMot()
        {
            var cfg = TestData.Load().Cfg;
            Assert.AreEqual(Board.SlotLayout.Length + 1, cfg.odds.Length, "bảng tỉ lệ: 5 ô đáy và cốc");
            Assert.AreEqual(1, cfg.rates.Sum(r => r.p), 1e-6);
            Assert.AreEqual(0.017, cfg.Rate("chest_gold"), 1e-6, "ô khuất 1,7 %");
            Assert.AreEqual(0.033, cfg.Rate("chest_silver"), 1e-6, "cốc thẻ 3,3 %");
            Assert.AreEqual(0.51, cfg.Rate("exp5"), 1e-6);
            Assert.AreEqual(0.44, cfg.Rate("exp10"), 1e-6);
            Assert.AreEqual(2, cfg.ringHits.Length);
            Assert.Greater(cfg.ringHits.Min(), 0.3, "bi chạm nấm khá thường");
        }
    }
}
