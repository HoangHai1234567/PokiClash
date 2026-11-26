// Đảo Casino (Core/Casino.cs, Core/Casino/*.cs, GD_Claude/29_DaoCasino.md): cấu hình hợp lệ; mở theo cấp và số tướng; lịch sự kiện
// (vòng 14 ngày từ mốc, ngày cố định đè vòng lặp); trần lượt theo ngày; bậc cược nhân bậc cấp; Hũ bàn; hoàn trả Blackjack (chiến thuật
// cơ bản), Roulette (25/26), máy quả (tính chính xác); đua tất định và cổ vũ có ích; câu cá (mồi, Sổ Cá, đủ bộ); chợ đen (hàng tất định,
// làm mới, mua); đấu trường ngầm (đội theo ngày, Nhà Vô Địch chủ nhật, thưởng thắng lần đầu / thắng lại); quán trọ; bản lưu đọc ghi.
using System;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public class CasinoTests
    {
        static GameData D => TestData.Load();
        static CasinoConfig C => D.Cfg.casino;

        // trưa theo giờ máy của ngày y-m-d (Casino.Today dùng giờ máy)
        static double Noon(int y, int m, int d, int hour = 12) =>
            new DateTimeOffset(new DateTime(y, m, d, hour, 0, 0, DateTimeKind.Local)).ToUnixTimeMilliseconds();

        static SaveData Save(int level, int balls = 100000, int heroes = 6)
        {
            var s = SaveData.New(D, 0, TestData.OldStarter);
            s.level = level;
            s.balls = balls;
            foreach (var h in D.Heroes.Where(h => !h.minion).Take(heroes)) s.Hero(h.id).owned = true;
            return s;
        }

        [Test]
        public void CauHinh_HopLe()
        {
            Assert.IsEmpty(C.Validate(D), string.Join("\n", C.Validate(D)));
            Assert.AreEqual(30, C.fishing.fish.Count);
            Assert.AreEqual(5, C.fishing.kings.Count);
            Assert.AreEqual(5, C.race.cups.Count);
            Assert.AreEqual(14, C.underground.rotation.Count);
            Assert.AreEqual(4, C.events.Count);
        }

        [Test]
        public void MoKhoa_TheoCap_VaSoTuong()
        {
            var s = Save(7, heroes: 2);
            Assert.IsFalse(Casino.Open(s, D));
            s.level = 8;
            Assert.IsTrue(Casino.Open(s, D));
            Assert.IsTrue(Casino.Unlocked(s, D, Casino.Fishing));
            Assert.IsFalse(Casino.Unlocked(s, D, Casino.Race));
            s.level = 15;
            Assert.IsFalse(Casino.Unlocked(s, D, Casino.Race), "cần 4 tướng");
            StringAssert.Contains("4", Casino.Need(s, D, Casino.Race));
            foreach (var h in D.Heroes.Where(h => !h.minion).Take(4)) s.Hero(h.id).owned = true;
            Assert.IsTrue(Casino.Unlocked(s, D, Casino.Race));
            Assert.IsFalse(Casino.Unlocked(s, D, Casino.Underground));
            CollectionAssert.Contains(Casino.NewlyOpen(s, D), Casino.Race);
            Casino.MarkSeen(s, "open:" + Casino.Race);
            CollectionAssert.DoesNotContain(Casino.NewlyOpen(s, D), Casino.Race);
        }

        [Test]
        public void SuKien_Vong14Ngay_TuMoc()
        {
            // mốc 2026-11-23 (thứ Hai): Đêm Bài ngày 1–3 của vòng, nghỉ ngày 4, Vòng Xoay 5–7, nghỉ 8, Máy Quả 9–11, Lễ Hội Đua 12–14
            Assert.AreEqual("blackjack", Casino.Active(D, Noon(2026, 11, 25)).Single().ev.booth);
            Assert.IsEmpty(Casino.Active(D, Noon(2026, 11, 26)));
            Assert.AreEqual("roulette", Casino.Active(D, Noon(2026, 11, 27)).Single().ev.booth);
            Assert.AreEqual("slot", Casino.Active(D, Noon(2026, 12, 2)).Single().ev.booth);
            Assert.AreEqual("race_fest", Casino.Active(D, Noon(2026, 12, 5)).Single().ev.booth);
            Assert.AreEqual(1.25, Casino.RaceMult(D, Noon(2026, 12, 5)));
            var again = Casino.Active(D, Noon(2026, 12, 7)).Single();
            Assert.AreEqual("blackjack", again.ev.booth);
            Assert.AreEqual(1, again.occ, "lần mở thứ hai");
            // còn 12 giờ khi đang trưa ngày cuối
            Assert.AreEqual(12 * 3600000.0, Casino.Left(Casino.Active(D, Noon(2026, 11, 25)).Single(), Noon(2026, 11, 25)), 1000);
            var up = Casino.Upcoming(D, Noon(2026, 11, 26), 2);
            Assert.AreEqual("roulette", up[0].ev.booth);
            // khách mời ổn định theo lần mở, là tướng Hiếm / Sử thi
            var sp = Casino.Active(D, Noon(2026, 11, 25)).Single();
            string g = Casino.Guest(D, sp);
            Assert.AreEqual(g, Casino.Guest(D, Casino.Active(D, Noon(2026, 11, 24)).Single()));
            Assert.That(D.Hero(g).rarity == Rarity.Rare || D.Hero(g).rarity == Rarity.Epic);
        }

        [Test]
        public void SuKien_NgayCoDinh_DeVongLap()
        {
            var saved = C.events;
            try
            {
                C.events = new List<CasinoEvent>(saved) { new CasinoEvent { id = "le", name = "Lễ", booth = "blackjack", start = "2026-11-25", end = "2026-11-26" } };
                Assert.AreEqual("le", Casino.Active(D, Noon(2026, 11, 26)).Single().ev.id, "ngày nghỉ của vòng lặp: chỉ sự kiện cố định");
                Assert.AreEqual("le", Casino.Active(D, Noon(2026, 11, 25)).Single().ev.id, "cố định đè Đêm Bài cùng lều");
            }
            finally
            {
                D.Cfg.casino.events = saved;
            }
        }

        [Test]
        public void TranLuot_TheoNgay_VaBacCuoc()
        {
            var s = Save(80);
            double now = Noon(2026, 11, 25);
            var rng = new Rng(1);
            Assert.AreEqual(C.blackjack.daily, Casino.PlaysLeft(s, D, Casino.Blackjack, now));
            for (int i = 0; i < C.blackjack.daily; i++)
            {
                var g = Blackjack.Start(s, D, 0, now, rng, out var why);
                Assert.IsNotNull(g, why);
                while (g.phase == BjPhase.Player) Blackjack.Act(g, BjAct.Stand, C.blackjack);
                Blackjack.Finish(s, D, g, 0, now, rng);
            }
            Assert.AreEqual(0, Casino.PlaysLeft(s, D, Casino.Blackjack, now));
            Assert.IsNull(Blackjack.Start(s, D, 0, now, rng, out var why2));
            Assert.IsNotNull(why2);
            Assert.AreEqual(C.blackjack.daily, Casino.PlaysLeft(s, D, Casino.Blackjack, now + Casino.Day), "sang ngày mới");
            // bậc cược nhân bậc cấp (cấp 80: ×2 theo bandLv / bandMult của cửa hàng)
            Assert.AreEqual(Shop.RoundBalls(C.blackjack.bets[3] * D.Cfg.shop.Band(80)), Casino.Bet(s, D, C.blackjack, 3));
            var low = Save(30);
            Assert.IsFalse(Casino.BetOpen(low, C.blackjack, 3));
            Assert.IsNull(Blackjack.Start(low, D, 3, now, rng, out _), "bậc chưa mở");
            // lều đóng hôm nay
            Assert.IsNull(Blackjack.Start(s, D, 0, Noon(2026, 11, 26), rng, out var why3));
            StringAssert.Contains("chưa mở", why3);
        }

        [Test]
        public void HuBan_DayTheoBiDaCuoc_TraoTheoBacCaoNhat()
        {
            var s = Save(80);
            double now = Noon(2026, 11, 25);
            var rng = new Rng(2);
            var t = C.blackjack;
            double band = D.Cfg.shop.Band(80);
            int bet0 = Casino.Bet(s, D, t, 0);
            // đổ tới gần đầy ở bậc 0 rồi một ván bậc 3: sức chứa tăng theo bậc 3, chưa đầy
            for (int i = 0; i < t.jarBets - 1; i++) Assert.IsFalse(Casino.Pour(s, D, Casino.Blackjack, 0, bet0, now, rng).full);
            Assert.IsFalse(Casino.Pour(s, D, Casino.Blackjack, 3, Casino.Bet(s, D, t, 3), now, rng).full, "lên bậc 3 thì hũ to ra");
            Assert.AreEqual(3, Casino.Of(s).Jar(Casino.Blackjack).tier);
            JarResult res = null;
            for (int i = 0; i < 100 && (res == null || !res.full); i++) res = Casino.Pour(s, D, Casino.Blackjack, 3, Casino.Bet(s, D, t, 3), now, rng);
            Assert.IsTrue(res.full);
            Assert.AreEqual(3, res.tier);
            Assert.IsTrue(res.rewards.Any(r => r.k == RewardKind.Shards), "bậc 3 có mảnh khách mời");
            Assert.Less(Casino.JarFrac(s, D, Casino.Blackjack, now), 1);
        }

        [Test]
        public void Blackjack_ChienThuatCoBan_HoanTraGan100()
        {
            var c = C.blackjack;
            var rng = new Rng(12345);
            long staked = 0, paid = 0;
            for (int i = 0; i < 300000; i++)
            {
                var g = Blackjack.Deal(100, rng, c);
                while (g.phase == BjPhase.Player) Blackjack.Act(g, Blackjack.Advice(g), c);
                staked += g.Staked;
                paid += g.payout;
            }
            double rtp = paid / (double)staked;
            Assert.That(rtp, Is.InRange(0.985, 1.005), $"hoàn trả {rtp:P2}");
        }

        [Test]
        public void Blackjack_Diem_VaGoiY()
        {
            List<BjCard> H(params int[] r) => r.Select(x => new BjCard { rank = x }).ToList();
            Assert.AreEqual(21, Blackjack.Total(H(1, 13), out bool soft));
            Assert.IsTrue(soft);
            Assert.AreEqual(12, Blackjack.Total(H(1, 1), out soft));
            Assert.AreEqual(17, Blackjack.Total(H(1, 6), out soft));
            Assert.IsTrue(soft);
            Assert.AreEqual(17, Blackjack.Total(H(10, 6, 1), out soft));
            Assert.IsFalse(soft);
            BjGame G(int up, params int[] mine)
            {
                var g = new BjGame { phase = BjPhase.Player, rng = new Rng(1) };
                g.hands.Add(new BjHand { bet = 10, cards = H(mine) });
                g.dealer.AddRange(H(up, 5));
                return g;
            }
            Assert.AreEqual(BjAct.Hit, Blackjack.Advice(G(10, 10, 6)), "16 gặp 10: rút");
            Assert.AreEqual(BjAct.Stand, Blackjack.Advice(G(6, 10, 3)), "13 gặp 6: dừng");
            Assert.AreEqual(BjAct.Double, Blackjack.Advice(G(6, 6, 5)), "11: gấp đôi");
            Assert.AreEqual(BjAct.Split, Blackjack.Advice(G(10, 1, 1)), "đôi A: tách");
            Assert.AreEqual(BjAct.Stand, Blackjack.Advice(G(6, 10, 10)), "đôi 10: dừng");
        }

        [Test]
        public void Blackjack_TachVaGapDoi_TraThemCuoc()
        {
            var s = Save(80);
            double now = Noon(2026, 11, 25);
            // tìm hạt giống chia ra đôi để tách
            for (uint seed = 1; seed < 5000; seed++)
            {
                var rng = new Rng(seed);
                int before = s.balls;
                var g = Blackjack.Start(s, D, 0, now, rng, out _);
                if (g == null) break;
                int bet = g.baseBet;
                if (Blackjack.Can(g, BjAct.Split))
                {
                    Assert.IsTrue(Blackjack.ActPaid(s, D, g, BjAct.Split, now));
                    Assert.AreEqual(before - 2 * bet, s.balls);
                    Assert.AreEqual(2, g.hands.Count);
                    while (g.phase == BjPhase.Player) Blackjack.Act(g, BjAct.Stand, C.blackjack);
                    int mid = s.balls;
                    Blackjack.Finish(s, D, g, 0, now, rng);
                    Assert.AreEqual(mid + g.payout, s.balls);
                    return;
                }
                while (g.phase == BjPhase.Player) Blackjack.Act(g, BjAct.Stand, C.blackjack);
                Blackjack.Finish(s, D, g, 0, now, rng);
                if (Casino.PlaysLeft(s, D, Casino.Blackjack, now) == 0) now += Casino.Day * 14; // lần mở sau
            }
            Assert.Fail("không gặp đôi để tách");
        }

        [Test]
        public void Roulette_MoiCua_HoanTra25Phan26()
        {
            var c = C.roulette;
            foreach (RlKind k in Enum.GetValues(typeof(RlKind))) Assert.AreEqual(25 / 26.0, Roulette.Rtp(c, k), 1e-9, k.ToString());
            var r = Roulette.Spin(c, new List<RlBet> { new RlBet { kind = RlKind.Elem, v = 0, amount = 10 } }, 0, new Rng(3));
            bool win = r.pocket != Roulette.StarPocket && r.pocket / 5 == 0;
            Assert.AreEqual(win ? 50 : 0, r.payout);
        }

        [Test]
        public void Roulette_TiLeRa_TheoTrongSo()
        {
            // rỗng = 26 ô đều nhau; đặt trọng số thì lõi bốc đúng theo trọng số, hoàn trả từng cửa tính theo đó
            var c = new RouletteConfig();
            Assert.AreEqual(1 / 26.0, Roulette.Chance(c, 7), 1e-12);
            Roulette.RtpRange(c, out double lo, out double hi);
            Assert.AreEqual(25 / 26.0, lo, 1e-9);
            Assert.AreEqual(25 / 26.0, hi, 1e-9);
            c.weights = Enumerable.Repeat(4, 26).ToArray();
            c.weights[Roulette.StarPocket] = 1;   // Sao Vàng hiếm đi 4 lần
            c.weights[0] = 0;                     // ô Kim 1 không bao giờ ra
            double total = c.weights.Sum();
            Assert.AreEqual(1 / total, Roulette.Chance(c, Roulette.StarPocket), 1e-12);
            Assert.AreEqual(0, Roulette.Chance(c, 0), 1e-12);
            Assert.AreEqual(16 / total, Roulette.Chance(c, new RlBet { kind = RlKind.Elem, v = 0 }), 1e-12);
            Assert.AreEqual((1 / total) * (c.starPays + 1), Roulette.RtpOf(c, new RlBet { kind = RlKind.Star }), 1e-12);
            var rng = new Rng(11);
            var n = new int[26];
            int rounds = 200000;
            var none = new List<RlBet>();
            for (int i = 0; i < rounds; i++) n[Roulette.Spin(c, none, 0, rng).pocket]++;
            Assert.AreEqual(0, n[0]);
            Assert.AreEqual(1 / total, n[Roulette.StarPocket] / (double)rounds, 0.002);
            Assert.AreEqual(4 / total, n[13] / (double)rounds, 0.004);
        }

        [Test]
        public void Roulette_Bi_NamDungOLoiChon()
        {
            // cách xếp ô quanh mâm: 26 vị trí, mỗi ô một chỗ, hệ xen kẽ
            for (int p = 0; p < Roulette.Pockets; p++) Assert.AreEqual(p, RouletteWheel.PocketAt(RouletteWheel.SlotOf(p)));
            for (int s = 0; s < 24; s++)
                Assert.AreNotEqual(RouletteWheel.PocketAt(s) / 5, RouletteWheel.PocketAt(s + 1) / 5, "hai ô cạnh nhau cùng hệ");
            // với mọi ô lõi chọn và mọi góc mâm: tìm được cú thả bi mà mô phỏng cho bi nằm đúng ô đó, trong khoảng lực thả tự nhiên
            var rng = new Rng(2026);
            int worst = 0;
            for (int rep = 0; rep < 6; rep++)
                for (int pocket = 0; pocket < Roulette.Pockets; pocket++)
                {
                    double rot0 = rng.Range(0, Math.PI * 2);
                    var tr = RouletteBall.Plan(RouletteWheel.SlotOf(pocket), rot0, RouletteBall.OmegaSpin, rng, 3);
                    Assert.IsNotNull(tr);
                    Assert.AreEqual(pocket, RouletteWheel.PocketAt(tr.slot));
                    Assert.LessOrEqual(tr.tries, 3000, "phải ép nhãn mâm");
                    Assert.LessOrEqual(Math.Abs(tr.shift), 3);
                    Assert.That(-tr.ballSpeed0, Is.InRange(RouletteBall.BallMin, RouletteBall.BallMax));
                    Assert.That(tr.duration, Is.InRange(3.5f, 12f));
                    worst = Math.Max(worst, tr.tries);
                    // phát lại: mô phỏng lại cùng tham số ra cùng chỗ nằm (tất định); lúc nằm yên bi ở đúng ô trên mâm
                    tr.Sample(tr.duration + 1.5f, out float x, out float y, out float z);
                    double beta = Math.Atan2(y, x) - tr.Rotor(tr.duration + 1.5f);
                    beta = (beta % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2);
                    Assert.AreEqual(tr.slot, (int)Math.Floor(beta / RouletteWheel.Step));
                    Assert.AreEqual(0, z, 1e-6);
                    Assert.AreEqual(RouletteWheel.RPocket, Math.Sqrt(x * x + y * y), 0.02);
                }
            Assert.Less(worst, 400, "số cú thử nhiều nhất");
        }

        [Test]
        public void Roulette_SaoVang_ThemManhKhachMoi()
        {
            var s = Save(80);
            double now = Noon(2026, 11, 28);
            for (uint seed = 1; seed < 3000; seed++)
            {
                var bets = new List<RlBet> { new RlBet { kind = RlKind.Star } };
                var r = Roulette.Play(s, D, bets, 2, now, new Rng(seed), out _, out var extra, out var why);
                Assert.IsNotNull(r, why);
                if (r.pocket == Roulette.StarPocket)
                {
                    Assert.AreEqual(C.roulette.starShards, r.starShards);
                    Assert.IsTrue(extra.Any(x => x.k == RewardKind.Shards));
                    return;
                }
                if (Casino.PlaysLeft(s, D, Casino.Roulette, now) == 0) now += Casino.Day * 14;
            }
            Assert.Fail("không ra Sao Vàng");
        }

        [Test]
        public void MayQua_HoanTraChinhXac_VaTyLeTrung()
        {
            var x = Slots.Exact(C.slots);
            Assert.That(x.rtp, Is.InRange(0.94, 0.97), $"hoàn trả {x.rtp:P2}");
            Assert.That(x.hit, Is.InRange(0.3, 0.5), "không thắng vụn mọi lượt");
            Assert.Greater(x.freeP, 0);
            Assert.Greater(x.badge, 0);
        }

        [Test]
        public void MayQua_KhongXepSuytTrung_CuonDungTheoDai()
        {
            // ô hiện trên cuộn đúng là 3 ô liền nhau của dải tại ô dừng
            var c = C.slots;
            var sp = Slots.Spin(c, 50, new Rng(9));
            for (int r = 0; r < 3; r++)
                for (int row = 0; row < 3; row++)
                    Assert.AreEqual(Slots.Sym(c.reels[r], sp.stops[r], row), sp.grid[r, row]);
        }

        [Test]
        public void Dua_KichBan_TatDinh_VeDungHang_BamSat()
        {
            var c = C.race;
            var lineup = Race.Lineup(D, c, 11);
            Assert.AreEqual(c.runners, lineup.Count);
            Assert.AreEqual(lineup.Count, lineup.Distinct().Count(), "5 tướng khác nhau");
            RaceGame Run(uint seed, int bet)
            {
                var g = Race.Setup(D, c, lineup, 2, bet, 20500, seed);
                Race.Run(c, g);
                return g;
            }
            var a = Run(77, 100);
            var b = Run(77, 100);
            CollectionAssert.AreEqual(Race.Order(a), Race.Order(b), "cùng hạt giống: cùng kết quả");
            Assert.AreEqual(a.events.Count, b.events.Count);
            int n = 300, surges = 0, hits = 0, leads = 0;
            double maxGap = 0;
            for (uint seed = 1; seed <= n; seed++)
            {
                var g = Race.Setup(D, c, lineup, (int)(seed % 5), 100, 20500, seed);
                int lead = -1;
                double last = -1;
                while (!g.done)
                {
                    Race.Step(c, g);
                    foreach (var r in g.runners) Assert.GreaterOrEqual(r.speed, -1e-9, "không con nào chạy lùi");
                    if (g.runners.All(r => r.finishT < 0) && g.t > 2)
                    {
                        var by = g.runners.OrderByDescending(r => r.pos).ToList();
                        maxGap = System.Math.Max(maxGap, by[0].pos - by[by.Count - 1].pos);
                        int now = g.runners.IndexOf(by[0]);
                        if (now != lead && g.t - last > 0.5) { leads++; lead = now; last = g.t; }
                    }
                }
                var order = Race.Order(g);
                for (int i = 0; i < order.Count; i++) Assert.AreEqual(i, g.runners[order[i]].place, "về đích đúng hạng đã định");
                Assert.That(g.t, Is.InRange(c.raceSec, c.raceSec + c.gapMax * 4 + 0.2), "cả đoàn về sát nhau");
                surges += g.events.Count(e => e.kind == RaceEv.Gust);
                hits += g.events.Count(e => e.kind == RaceEv.Hit);
            }
            Assert.Greater(surges / (double)n, 2.0, "mỗi cuộc đua có vài cú bứt tốc");
            Assert.Greater(hits / (double)n, 1.0, "mỗi cuộc đua có húc nhau, choáng");
            Assert.Greater(leads / (double)n, 4.0, "đổi ngôi đầu nhiều lần");
            Assert.Less(maxGap, 40, "đầu đoàn và cuối đoàn không cách nhau quá một màn");
        }

        [Test]
        public void Dua_Cuoc_CangCaoCangKhoThang()
        {
            var c = C.race;
            Assert.AreEqual(5, c.daily);
            Assert.AreEqual(500, c.betMax);
            CollectionAssert.AreEqual(new double[] { 3, 2, 1, 0, 0 }, c.pay);
            double prev = double.MaxValue;
            foreach (int bet in new[] { c.betMin, 50, 100, 200, 350, c.betMax })
            {
                var p = Race.PlaceOdds(c, bet, 5);
                Assert.AreEqual(1, p.Sum(), 1e-9);
                double win = p[0] + p[1];
                Assert.Less(win, prev + 1e-12, $"cược {bet}: tỉ lệ thắng không tăng");
                prev = win;
            }
            Assert.Greater(Race.PlaceOdds(c, c.betMin, 5)[0], Race.PlaceOdds(c, c.betMax, 5)[0] + 0.03, "cược cao khó về nhất hơn hẳn");
            Assert.Less(Race.Rtp(c, c.betMax, 5), 0.9, "cược tối đa: nhà cái lời");
            Assert.That(Race.Rtp(c, c.betMin, 5), Is.InRange(0.9, 1.0), "cược nhỏ: gần hoà, không lãi chắc (GD_Claude/33 việc 9)");
            // hạng rút thật khớp bảng tỉ lệ
            var lineup = Race.Lineup(D, c, 3);
            foreach (int bet in new[] { 50, 500 })
            {
                var cnt = new int[5];
                int n = 6000;
                for (uint seed = 1; seed <= n; seed++) cnt[Race.Setup(D, c, lineup, 0, bet, 20500, seed * 2654435761u).Player.place]++;
                var p = Race.PlaceOdds(c, bet, 5);
                for (int i = 0; i < 5; i++) Assert.AreEqual(p[i], cnt[i] / (double)n, 0.025, $"cược {bet}, hạng {i + 1}");
            }
            Assert.AreEqual(300, Race.Payout(c, 100, 0));
            Assert.AreEqual(200, Race.Payout(c, 100, 1));
            Assert.AreEqual(100, Race.Payout(c, 100, 2));
            Assert.AreEqual(0, Race.Payout(c, 100, 3));
            Assert.AreEqual(400, Race.Payout(c, 100, 0, 1.5), "Lễ Hội Đua nhân phần lời");
        }

        [Test]
        public void Dua_DatCuoc_NamLuot_TraThuong_DiemTuan()
        {
            var s = Save(50);
            double now = Noon(2026, 11, 25);
            var rng = new Rng(4);
            var c = C.race;
            var lineup = Race.Lineup(D, c, 9);
            s.balls = 5000;
            Assert.IsNull(Race.Start(s, D, lineup, 0, c.betMax + 1, now, rng, out var why), "quá mức cược tối đa");
            Assert.IsNotNull(why);
            Assert.AreEqual(5000, s.balls);
            int cup = Race.WeekCup(s, D);
            for (int i = 0; i < c.daily; i++)
            {
                int before = s.balls, pts = Race.Points(s, D, cup, now);
                var g = Race.Start(s, D, lineup, i % lineup.Count, 200, now, rng, out why);
                Assert.IsNotNull(g, why);
                Assert.AreEqual(before - 200, s.balls, "trừ tiền cược ngay");
                Race.Run(c, g);
                var res = Race.Finish(s, D, g, now);
                Assert.AreEqual(Race.Payout(c, 200, res.place), res.balls);
                Assert.AreEqual(before - 200 + res.balls, s.balls);
                Assert.AreEqual(System.Math.Min(c.weekPts, pts + c.points[res.place]), Race.Points(s, D, cup, now));
            }
            Assert.AreEqual(0, Casino.PlaysLeft(s, D, Casino.Race, now));
            Assert.IsNull(Race.Start(s, D, lineup, 0, 100, now, rng, out why), "hết 5 lượt hôm nay");
            int left = s.balls;
            var free = Race.Start(s, D, lineup, 0, 0, now, rng, out why);
            Assert.IsNotNull(free, "đua tập không cược vẫn được");
            Race.Run(c, free);
            Assert.AreEqual(0, Race.Finish(s, D, free, now).balls);
            Assert.AreEqual(left, s.balls);
            Assert.AreEqual(c.daily, Casino.PlaysLeft(s, D, Casino.Race, now + Casino.Day), "hôm sau có lại lượt");
            Casino.Of(s).cupPts[cup] = c.weekPts;
            Assert.IsTrue(Race.WeekReady(s, D, cup, now));
            Assert.IsNotEmpty(Race.ClaimWeek(s, D, cup, now, rng));
            Assert.IsFalse(Race.WeekReady(s, D, cup, now));
            Assert.AreEqual(0, Race.Points(s, D, cup, now + 7 * Casino.Day), "tuần sau đếm lại");
        }

        [Test]
        public void CauCa_Moi_SoCa_DuBo()
        {
            var s = Save(30);
            double now = Noon(2026, 11, 25);
            var rng = new Rng(5);
            for (int i = 0; i < C.fishing.freeBait; i++) Assert.IsNotNull(Fishing.Cast(s, D, 0, 0.5, now, rng, out _));
            Assert.IsNull(Fishing.Cast(s, D, 0, 0.5, now, rng, out var why));
            StringAssert.Contains("mồi", why);
            Assert.IsTrue(Fishing.BuyBait(s, D));
            Assert.IsNotNull(Fishing.Cast(s, D, 0, 0.5, now, rng, out _));
            Assert.IsNotNull(Fishing.Cast(s, D, 2, 0.5, now, rng, out _), "rạn đá mở sẵn (bỏ nâng cấp cần, 2026-11-26)");
            // bắt đủ 6 loài hệ Thủy: lần đầu mỗi loài có bi, đủ bộ có mảnh
            FishCatch last = null;
            foreach (var f in C.fishing.fish.Where(x => x.elem == Elem.Thuy))
                last = Fishing.Land(s, D, new FishBite { fish = f, size = f.max }, now, rng);
            Assert.AreEqual(Elem.Thuy, last.setDone);
            Assert.IsTrue(last.rewards.Any(r => r.k == RewardKind.Shards));
            Assert.AreEqual(6, Casino.Of(s).creel.Count);
            int v = Fishing.CreelValue(s, D);
            int b0 = s.balls;
            Assert.AreEqual(v, Fishing.SellCreel(s, D));
            Assert.AreEqual(b0 + v, s.balls);
            Assert.IsEmpty(Casino.Of(s).creel);
        }

        [Test]
        public void ChoDen_HangTatDinh_LamMoi_Mua()
        {
            var s = Save(40);
            double now = Noon(2026, 11, 25, 10);
            var a = BlackMarket.Stock(s, D, now).Select(x => x.offer.kind + x.price).ToList();
            var b = BlackMarket.Stock(s, D, now).Select(x => x.offer.kind + x.price).ToList();
            CollectionAssert.AreEqual(a, b);
            Assert.AreEqual(C.market.slots, a.Count, "ban ngày không có hàng đêm");
            Assert.AreEqual(C.market.slots + C.market.nightSlots, BlackMarket.Stock(s, D, Noon(2026, 11, 25, 21)).Count);
            int before = s.balls;
            var sl = BlackMarket.Stock(s, D, now)[0];
            Assert.IsNotNull(BlackMarket.Buy(s, D, sl.idx, now, new Rng(1), out var why), why);
            Assert.AreEqual(before - sl.price, s.balls);
            Assert.IsNull(BlackMarket.Buy(s, D, sl.idx, now, new Rng(1), out _), "đã mua");
            int cost = BlackMarket.RefreshCost(s, D, now);
            Assert.IsTrue(BlackMarket.Refresh(s, D, now));
            Assert.Greater(BlackMarket.RefreshCost(s, D, now), cost, "làm mới lần sau đắt hơn");
            Assert.IsFalse(BlackMarket.Stock(s, D, now)[0].bought);
        }

        [Test]
        public void Ngam_DoiTheoNgay_NhaVoDichChuNhat_Thuong()
        {
            double mon = Noon(2026, 11, 23), sun = Noon(2026, 11, 29);
            Assert.AreSame(C.underground.rotation[0], Underground.DayOf(D, Casino.Today(mon)));
            Assert.AreSame(C.underground.rotation[1], Underground.DayOf(D, Casino.Today(mon + Casino.Day)));
            int champ = C.underground.tiers.FindIndex(t => t.weekly);
            CollectionAssert.DoesNotContain(Underground.TiersToday(D, mon), champ);
            CollectionAssert.Contains(Underground.TiersToday(D, sun), champ);
            var s = Save(60);
            var rng = new Rng(6);
            int fee = Underground.Fee(s, D, 0);
            int before = s.balls;
            Assert.IsTrue(Underground.Pay(s, D, 0, mon, out var why), why);
            Assert.AreEqual(before - fee, s.balls);
            var r1 = Underground.Finish(s, D, 0, true, mon, rng);
            Assert.IsTrue(r1.first);
            Assert.AreEqual((int)Math.Round(fee * C.underground.winMult), r1.balls);
            Assert.IsTrue(r1.rewards.Any(x => x.k == RewardKind.Shards && x.res?.hero == Underground.Lead(Underground.Entry(D, 0, mon))));
            Assert.IsTrue(Underground.Pay(s, D, 0, mon, out _));
            var r2 = Underground.Finish(s, D, 0, true, mon, rng);
            Assert.IsFalse(r2.first);
            Assert.AreEqual((int)Math.Round(fee * C.underground.rewinMult), r2.balls);
            // không khoá bậc theo cấp (2026-11-26): Hầm đấu mở là đánh được mọi bậc; chưa mở Hầm đấu thì không bậc nào đánh được
            for (int i = 0; i < C.underground.tiers.Count; i++) Assert.IsTrue(Underground.TierOpen(s, D, i), "bậc " + i);
            Assert.IsFalse(Underground.TierOpen(Save(C.Unlock(Casino.Underground).level - 1), D, 0), "chưa mở Hầm đấu");
            Assert.IsTrue(Underground.Pay(s, D, 4, mon, out why), why);
            // trần trận mỗi ngày (2026-11-26): thắng, thua, đánh lại đều tính; hết lượt thì không trừ lệ phí; sang ngày mới có lại
            Assert.AreEqual(C.underground.daily - 3, Underground.FightsLeft(s, D, mon));
            while (Underground.FightsLeft(s, D, mon) > 0) Assert.IsTrue(Underground.Pay(s, D, 1, mon, out why), why);
            int ballsLeft = s.balls;
            Assert.IsFalse(Underground.Pay(s, D, 1, mon, out why));
            Assert.AreEqual(ballsLeft, s.balls, "hết lượt thì không trừ lệ phí");
            Assert.AreEqual(C.underground.daily, Underground.FightsLeft(s, D, mon + Casino.Day));
            // 10 bậc thường; lực chiến đội ra sân tăng dần đều, bậc sau không quá 2,3 lần bậc trước (trước đây Vàng → Huyền Thoại gấp 9)
            int normalTiers = Underground.NormalTiers(D);
            Assert.AreEqual(10, normalTiers);
            foreach (var day in C.underground.rotation)
                for (int k = 1; k < normalTiers; k++)
                {
                    int p0 = Underground.Power(D, day.entries[k - 1]), p1 = Underground.Power(D, day.entries[k]);
                    Assert.Greater(p1, p0 * 1.2, $"{day.entries[k].name}: {p0} → {p1}");
                    Assert.Less(p1, p0 * 2.3, $"{day.entries[k].name}: {p0} → {p1}");
                }
            // số tướng ra sân, lực chiến, giờ đổi đội
            foreach (var e in C.underground.rotation[0].entries)
            {
                Assert.AreEqual(Underground.Enemy(D, e).members.Count, Underground.Count(e));
                Assert.Greater(Underground.Power(D, e), 0);
            }
            Assert.AreEqual(12 * 3600000.0, Underground.NextChange(mon), 1000);
            // đội địch áp luật ngày
            foreach (var day in C.underground.rotation)
                foreach (var e in day.entries)
                {
                    var t = Underground.Enemy(D, e);
                    Assert.AreEqual(Math.Min(e.team.Count, Underground.TeamLimit(e)), t.members.Count);
                }
        }

        [Test]
        public void QuanTro_NhiemVu_TheoDoi_Nhan()
        {
            var s = Save(40);
            double now = Noon(2026, 11, 25);
            var rng = new Rng(8);
            var qs = Casino.InnToday(s, D, now);
            Assert.AreEqual(C.inn.count, qs.Count);
            foreach (var q in qs) Casino.Track(s, D, q.kind, q.n, now);
            Assert.IsFalse(Casino.InnAllReady(s, D, now));
            foreach (var q in qs) Assert.IsNotEmpty(Casino.ClaimQuest(s, D, q.id, now, rng));
            Assert.IsEmpty(Casino.ClaimQuest(s, D, qs[0].id, now, rng), "không nhận hai lần");
            Assert.IsTrue(Casino.InnAllReady(s, D, now));
            Assert.IsNotEmpty(Casino.ClaimInnAll(s, D, now, rng));
            Assert.IsFalse(Casino.InnAllReady(s, D, now));
            Assert.AreEqual(C.inn.count, Casino.InnToday(s, D, now + Casino.Day).Count);
            Assert.AreEqual(0, Casino.InnProg(s, qs[0].id), "sang ngày mới xoá tiến độ");
        }

        [Test]
        public void QuanTro_ViecLeu_ChiRaNgayCoLeu()
        {
            // vòng 14 ngày từ mốc 2026-11-23: ngày 4 và 8 nghỉ, ngày 12–14 Lễ Hội Đua (không phải bàn may rủi)
            foreach (var day in new[] { 26, 30 })
            {
                double now = Noon(2026, 11, day);
                Assert.IsFalse(Casino.Active(D, now).Any(sp => C.Table(sp.ev.booth) != null), "ngày " + day + " không có lều bàn");
                var qs = Casino.InnToday(Save(60), D, now);
                Assert.AreEqual(C.inn.count, qs.Count);
                CollectionAssert.DoesNotContain(qs.Select(q => q.kind).ToList(), "table", "ngày " + day);
            }
            // ngày có lều bàn: việc lều vào bể (cấp 60 mở hết trò, đủ 8 việc trong bể)
            var pool = C.inn.quests.Where(q => q.kind == "table").ToList();
            Assert.IsNotEmpty(pool);
            bool seen = false;
            for (int day = 23; day <= 25 && !seen; day++)
                for (int k = 0; k < 14 && !seen; k++)
                    seen = Casino.InnToday(Save(60), D, Noon(2026, 11, day) + k * 14 * Casino.Day).Any(q => q.kind == "table");
            Assert.IsTrue(seen, "việc lều có ra vào ngày Đêm Bài");
        }

        [Test]
        public void Ban_VanDauMienPhi_VanTap_VungTatLeu()
        {
            double now = Noon(2026, 11, 23); // Đêm Bài (ngày 1 của vòng)
            var s = Save(40);
            Assert.AreEqual(TableMode.Free, Casino.ModeOf(s, D, Casino.Blackjack, now));
            int b0 = s.balls;
            var g = Blackjack.StartAs(s, D, 2, TableMode.Free, now, new Rng(3), out var why);
            Assert.IsNotNull(g, why);
            Assert.AreEqual(0, g.tier, "ván miễn phí ở bậc 1");
            Assert.AreEqual(b0, s.balls, "không trả cược");
            while (g.phase == BjPhase.Player) Assert.IsTrue(Blackjack.ActPaid(s, D, g, Blackjack.Advice(g), now));
            Assert.AreEqual(b0, s.balls, "gấp đôi / tách cũng miễn phí");
            Blackjack.Finish(s, D, g, g.tier, now, new Rng(3));
            Assert.AreEqual(b0 + Casino.FreeWin(g.payout, g.Staked), s.balls, "thắng nhận phần lời, thua không mất");
            Assert.AreEqual(TableMode.Paid, Casino.ModeOf(s, D, Casino.Blackjack, now), "chỉ một ván miễn phí");
            Assert.AreEqual(C.blackjack.daily, Casino.PlaysLeft(s, D, Casino.Blackjack, now), "ván miễn phí không tính lượt");
            // hết lượt có thưởng: ván tập
            Casino.Roll(s, D, now).plays[Casino.Blackjack] = C.blackjack.daily;
            Assert.AreEqual(TableMode.Practice, Casino.ModeOf(s, D, Casino.Blackjack, now));
            for (uint seed = 1; seed < 30; seed++)
            {
                b0 = s.balls;
                var p = Blackjack.StartAs(s, D, 0, TableMode.Practice, now, new Rng(seed), out why);
                Assert.IsNotNull(p, why);
                while (p.phase == BjPhase.Player) Blackjack.ActPaid(s, D, p, Blackjack.Advice(p), now);
                Blackjack.Finish(s, D, p, p.tier, now, new Rng(seed));
                Assert.AreEqual(b0, s.balls, "ván tập không mất, không được");
            }
            // vòng xoay, máy quả: ván đầu miễn phí không trả cược
            double rlDay = Noon(2026, 11, 27), slDay = Noon(2026, 12, 1);
            b0 = s.balls;
            var r = Roulette.PlayAs(s, D, new List<RlBet> { new RlBet { kind = RlKind.Elem, v = 0 } }, 1, Casino.ModeOf(s, D, Casino.Roulette, rlDay), rlDay,
                new Rng(5), out _, out _, out why);
            Assert.IsNotNull(r, why);
            Assert.AreEqual(b0 + Casino.FreeWin(r.payout, r.staked), s.balls);
            b0 = s.balls;
            var sr = Slots.PlayAs(s, D, 1, Casino.ModeOf(s, D, Casino.Slot, slDay), slDay, new Rng(6), out _, out _, out why);
            Assert.IsNotNull(sr, why);
            Assert.AreEqual(b0 + Casino.FreeWin(sr.Payout, sr.bet), s.balls);
            Assert.AreEqual(TableMode.Paid, Casino.ModeOf(s, D, Casino.Slot, slDay));
            // vùng tắt lều may rủi (casino.tablesBlock)
            Casino.Region = "be";
            try
            {
                Assert.IsFalse(Casino.TablesAllowed(D));
                Assert.IsFalse(Casino.BoothOpen(s, D, Casino.Blackjack, now));
                Assert.IsNull(Blackjack.StartAs(s, D, 0, TableMode.Practice, now, new Rng(1), out _));
            }
            finally
            {
                Casino.Region = "";
            }
            Assert.IsTrue(Casino.BoothOpen(s, D, Casino.Blackjack, now));
        }

        [Test]
        public void ChoDen_TheThua_DoiDaTiemNang_CoTranNgay_KhongRaBi()
        {
            var s = Save(40);
            var m = C.market;
            double now = Noon(2026, 11, 25, 10);
            Assert.AreEqual(0, BlackMarket.SellSpare(s, D, now), "chưa có thẻ thừa");
            var hp = s.Hero(TestData.OldStarter);
            hp.skill.lv = D.Cfg.cardMax;
            hp.skill.copies = m.copyPerStone * (m.stoneDaily + 3) + 7; // nhiều hơn trần ngày
            int balls = s.balls, stones = s.potentialStones;
            Assert.AreEqual(m.stoneDaily, BlackMarket.SpareValue(s, D, now));
            Assert.AreEqual(m.stoneDaily, BlackMarket.SellSpare(s, D, now));
            Assert.AreEqual(balls, s.balls, "không ra bi");
            Assert.AreEqual(stones + m.stoneDaily, s.potentialStones);
            Assert.AreEqual(m.copyPerStone * 3 + 7, hp.skill.copies, "chỉ trừ số bản đã đổi");
            Assert.AreEqual(0, BlackMarket.SellSpare(s, D, now), "hết trần hôm nay");
            Assert.AreEqual(3, BlackMarket.SellSpare(s, D, now + Casino.Day), "hôm sau đổi tiếp");
            Assert.AreEqual(7, hp.skill.copies, "phần lẻ giữ lại");
        }

        [Test]
        public void Ngam_ThangKhongLaiBi()
        {
            Assert.LessOrEqual(C.underground.winMult, 1.1, "Hầm đấu thưởng mảnh và đá, không phải nguồn bi (GD_Claude/33 việc 2)");
        }

        [Test]
        public void ChoDen_DoNha_ChiKhiMoNha_VaoTui()
        {
            var home = C.market.offers.Find(o => o.kind == "home");
            Assert.IsNotNull(home, "dữ liệu có hàng Đồ Nhà");
            // chưa mở Nhà: không bày Đồ Nhà (thử nhiều lượt hàng)
            var s = Save(60);
            for (int k = 0; k < 40; k++)
            {
                s.casino = null;
                double t = Noon(2026, 11, 1) + k * Casino.Day;
                Assert.IsFalse(BlackMarket.Stock(s, D, t).Any(x => x.offer.kind == "home"), "chưa mở Nhà");
            }
            // mở Nhà: có lượt hàng bày Đồ Nhà; mua thì vào túi Nhà
            for (int z = 0; z < s.zones.Length; z++) s.zones[z] = 2;
            Home.Of(s, D, 0);
            Assert.IsTrue(Home.Open(s, D.Cfg));
            MkSlot sl = null;
            double when = 0;
            for (int k = 0; k < 120 && sl == null; k++)
            {
                s.casino = null;
                when = Noon(2026, 11, 1) + k * Casino.Day;
                sl = BlackMarket.Stock(s, D, when).FirstOrDefault(x => x.offer.kind == "home");
            }
            Assert.IsNotNull(sl, "có lượt hàng bày Đồ Nhà");
            CollectionAssert.Contains(home.defs, sl.deco);
            int had = s.home.bag.TryGetValue(sl.deco, out var n0) ? n0 : 0;
            var r = BlackMarket.Buy(s, D, sl.idx, when, new Rng(2), out var why);
            Assert.IsNotNull(r, why);
            Assert.AreEqual(RewardKind.Deco, r[0].k);
            Assert.AreEqual(had + home.n, s.home.bag[sl.deco]);
        }

        [Test]
        public void ChoDen_TuiLau_BiNhanBacCap()
        {
            var lo = Save(1);
            var hi = Save(150);
            Assert.Greater(Casino.Band(hi, D), 1.0);
            Assert.AreEqual(Shop.RoundBalls(C.market.offers.Find(o => o.kind == "mystery").price * Casino.Band(hi, D)), BlackMarket.MysteryPrice(hi, D));
            // cùng hạt giống: túi ra bi thì cấp cao nhận bi nhân bậc cấp
            for (uint seed = 1; seed < 200; seed++)
            {
                int b0 = lo.balls, b1 = hi.balls;
                var r0 = BlackMarket.OpenMystery(lo, D, new Rng(seed));
                var r1 = BlackMarket.OpenMystery(hi, D, new Rng(seed));
                if (r0[0].k != RewardKind.Balls) continue;
                Assert.AreEqual(Shop.RoundBalls(r0[0].n * Casino.Band(hi, D)), r1[0].n, "seed " + seed);
                Assert.AreEqual(r0[0].n, lo.balls - b0);
                Assert.AreEqual(r1[0].n, hi.balls - b1);
            }
        }

        [Test]
        public void BanLuu_DocGhi_Casino()
        {
            var s = Save(60);
            double now = Noon(2026, 11, 25);
            var st = Casino.Roll(s, D, now);
            st.dex["ca_moi_bac"] = new FishRec { n = 2, best = 15.5 };
            st.creel.Add(new CaughtFish { id = "ca_moi_bac", size = 12 });
            st.Jar(Casino.Blackjack).fill = 120;
            st.cupPts = new[] { 3, 0, 0, 0, 0 };
            st.innProg["fish5"] = 2;
            st.seen.Add("open:fishing");
            string js = SaveCodec.Write(s);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(js, D, out var s2));
            Assert.AreEqual(15.5, s2.casino.dex["ca_moi_bac"].best);
            Assert.AreEqual(120, s2.casino.jars[Casino.Blackjack].fill);
            Assert.AreEqual(3, s2.casino.cupPts[0]);
            CollectionAssert.Contains(s2.casino.seen, "open:fishing");
            Assert.AreEqual(js, SaveCodec.Write(s2));
            // bản lưu chưa có khoá casino vẫn đọc được
            var fresh = Save(10);
            Assert.AreEqual(LoadStatus.Ok, SaveCodec.Read(SaveCodec.Write(fresh), D, out var s3));
            Assert.IsNull(s3.casino);
        }

        [Test]
        public void BoiSao_CoDinhTheoNgay()
        {
            double now = Noon(2026, 11, 25);
            Assert.AreEqual(Casino.Lucky(now), Casino.Lucky(now + 3600000));
            var s = Save(10);
            Assert.IsNull(Casino.LuckyActive(s, now));
            Assert.AreEqual(Casino.Lucky(now), Casino.FlipLucky(s, now));
            Assert.AreEqual(Casino.Lucky(now), Casino.LuckyActive(s, now));
            Assert.IsNull(Casino.LuckyActive(s, now + Casino.Day));
        }
    }
}
