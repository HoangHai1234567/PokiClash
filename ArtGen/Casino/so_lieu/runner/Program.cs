using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;

static class Program
{
    static GameData D;

    static string R(string f) => File.ReadAllText(Path.Combine("data", f));

    static int Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        D = GameData.FromJson(R("heroes.json"), R("cards.json"), R("zones.json"), R("stages.json"), R("balance.json"));
        var err = D.Validate();
        err.AddRange(D.Cfg.casino.Validate(D));
        foreach (var e in err) Console.WriteLine("LOI: " + e);
        string what = args.Length > 0 ? args[0] : "all";
        if (what == "all" || what == "bj") Bj();
        if (what == "all" || what == "rl") Rl();
        if (what == "all" || what == "slot") Slot();
        if (what == "all" || what == "race") RaceRates();
        if (what == "all" || what == "ug") Ug(args.Length > 1 ? int.Parse(args[1]) : 20);
        if (what == "ugcal") UgCal(args.Length > 1 ? int.Parse(args[1]) : 40);
        if (what == "ugpow") UgPow(args.Length > 1 ? double.Parse(args[1]) : 6000, args.Length > 2 ? double.Parse(args[2]) : 600000,
            args.Length > 3 ? double.Parse(args[3]) : 800000);
        if (what == "all" || what == "save") SaveRound();
        if (what == "all" || what == "ev") Events();
        if (what == "all" || what == "fish") Fish();
        if (what == "all" || what == "mk") Market();
        return err.Count > 0 ? 1 : 0;
    }

    static void Bj()
    {
        var c = D.Cfg.casino.blackjack;
        var rng = new Rng(12345);
        long staked = 0, paid = 0;
        int n = 1000000;
        int[] res = new int[4];
        for (int i = 0; i < n; i++)
        {
            var g = Blackjack.Deal(100, rng, c);
            while (g.phase == BjPhase.Player) Blackjack.Act(g, Blackjack.Advice(g), c);
            staked += g.Staked;
            paid += g.payout;
        }
        Console.WriteLine($"Blackjack chiến thuật cơ bản: hoàn trả {paid / (double)staked:P3} trên tiền cược, {paid / (100.0 * n):P3} trên cược gốc ({n} ván)");
        // người mới: rút tới 15 rồi dừng, không gấp đôi / tách
        staked = paid = 0;
        for (int i = 0; i < 300000; i++)
        {
            var g = Blackjack.Deal(100, rng, c);
            while (g.phase == BjPhase.Player) Blackjack.Act(g, g.Hand.Total < 15 ? BjAct.Hit : BjAct.Stand, c);
            staked += g.Staked;
            paid += g.payout;
        }
        Console.WriteLine($"Blackjack người mới (rút tới 15): hoàn trả {paid / (double)staked:P3}");
    }

    static void Rl()
    {
        var c = D.Cfg.casino.roulette;
        foreach (RlKind k in Enum.GetValues(typeof(RlKind))) Console.WriteLine($"Roulette {k}: hoàn trả {Roulette.Rtp(c, k):P3}");
        var rng = new Rng(7);
        long st = 0, pd = 0;
        for (int i = 0; i < 400000; i++)
        {
            var bets = new List<RlBet> { new RlBet { kind = RlKind.Elem, v = rng.Int(0, 4), amount = 10 }, new RlBet { kind = RlKind.Single, v = rng.Int(0, 24), amount = 10 } };
            var r = Roulette.Spin(c, bets, 0, rng);
            st += r.staked;
            pd += r.payout;
        }
        Console.WriteLine($"Roulette mô phỏng: {pd / (double)st:P3}");
    }

    static void Slot()
    {
        var c = D.Cfg.casino.slots;
        var x = Slots.Exact(c);
        Console.WriteLine($"Máy quả chính xác: hoàn trả {x.rtp:P3}, trúng {x.hit:P1}, ra lượt miễn phí {x.freeP:P2}, đường huy hiệu mỗi lượt {x.badge:F4}");
        var rng = new Rng(99);
        long st = 0, pd = 0;
        int n = 300000;
        for (int i = 0; i < n; i++)
        {
            var r = Slots.Round(c, 50, 0, rng);
            st += 50;
            pd += r.Payout;
        }
        Console.WriteLine($"Máy quả mô phỏng: {pd / (double)st:P3}");
    }

    static void RaceRates()
    {
        var c = D.Cfg.casino.race;
        foreach (int bet in new[] { c.betMin, 50, 100, 200, 350, c.betMax })
        {
            int n = 20000;
            var cnt = new int[c.runners];
            double back = 0, len = 0, surges = 0, hits = 0, leads = 0, gap = 0, close = 0;
            for (int i = 0; i < n; i++)
            {
                var lineup = Race.Lineup(D, c, (uint)(i * 31 + 7));
                var g = Race.Setup(D, c, lineup, i % lineup.Count, bet, 20000 + i, (uint)(i * 7919 + 3));
                int lead = -1;
                double last = -1, worst = 0;
                while (!g.done)
                {
                    Race.Step(c, g);
                    if (g.runners.All(r => r.finishT < 0) && g.t > 2)
                    {
                        var by = g.runners.OrderByDescending(r => r.pos).ToList();
                        worst = Math.Max(worst, by[0].pos - by[by.Count - 1].pos);
                        int now = g.runners.IndexOf(by[0]);
                        if (now != lead && g.t - last > 0.5) { leads++; lead = now; last = g.t; }
                    }
                }
                int p = Race.PlaceOf(g);
                cnt[p]++;
                back += Race.Payout(c, bet, p);
                len += g.t;
                gap += worst;
                var fin = g.runners.Select(r => r.finishT).OrderBy(x => x).ToList();
                close += fin[1] - fin[0];
                surges += g.events.Count(e => e.kind == RaceEv.Gust);
                hits += g.events.Count(e => e.kind == RaceEv.Hit);
            }
            Console.WriteLine($"Đua cược {bet,3}: hạng " + string.Join(" / ", cnt.Select(x => (x / (double)n).ToString("P1"))) +
                              $" | hoàn trả {back / (n * (double)bet):F3} (bảng {Race.Rtp(c, bet, c.runners):F3}) | dài {len / n:F1}s | bứt tốc {surges / n:F1}, húc {hits / n:F1}, " +
                              $"đổi ngôi đầu {leads / n:F1} | đầu-cuối xa nhất {gap / n:F1} | nhất-nhì cách {close / n:F2}s");
        }
    }

    // đội người chơi mẫu cho một trận ngầm: 3 tướng Hiếm / Sử thi, ưu tiên khắc hệ chủ lực địch, sao theo cấp, thẻ cấp 4
    static (SaveData s, List<string> team) RefTeam(UgEntry e, int lv)
    {
        int star = Math.Max(1, Math.Min(20, Sim.StarAt(D.Cfg, lv)));
        var leadElem = D.Hero(e.team[0].hero).elem;
        var team = D.Heroes.Where(h => !h.minion && h.rarity >= Rarity.Rare && h.rarity <= Rarity.Epic)
            .OrderByDescending(h => Elements.Beats(h.elem) == leadElem ? 1 : 0).ThenBy(h => h.id).Take(3).Select(h => h.id).ToList();
        return (Sim.Setup(D, team, lv, star, 4), team);
    }

    static double WinRate(UgEntry e, int lv, int n)
    {
        var (s, team) = RefTeam(e, lv);
        int win = 0;
        for (int i = 0; i < n; i++)
        {
            var t0 = Teams.Player(s, team.Take(Underground.TeamLimit(e)).ToList(), D);
            t0.ai = true;
            Underground.ApplyRule(D, e.rule, t0, false);
            var b = Battle.Create(D, t0, Underground.Enemy(D, e), (uint)(2000 + i * 7919), s.level, s.level);
            BattleSim.Run(b);
            if (b.winner == 0) win++;
        }
        return win / (double)n;
    }

    // dò cấp từng đội ngầm theo LỰC CHIẾN (người dùng 2026-11-26: bậc Vàng 68k sang Huyền Thoại 600k "gap lớn quá"): lực chiến đội ra
    // sân (Underground.Power, đã tính luật ngày của địch) tăng theo cấp số nhân từ lo (bậc đầu) tới hi (bậc thường cuối), Nhà Vô Địch = champ.
    // Sao theo cấp (Sim.StarAt) + extraStar của bậc. Ghi ug_levels.json (gen_casino.py đọc lại).
    static void UgPow(double lo, double hi, double champ)
    {
        var c = D.Cfg.casino.underground;
        int normal = c.tiers.Count(t => !t.weekly);
        int[] extraStar = { 2, 1, 1 };
        var outDays = new List<string>();
        for (int day = 0; day < c.rotation.Count; day++)
        {
            var ud = c.rotation[day];
            var lvs = new List<string>();
            var line = new List<string>();
            for (int k = 0; k < ud.entries.Count; k++)
            {
                var e = ud.entries[k];
                double target = k >= normal ? champ : lo * Math.Pow(hi / lo, normal > 1 ? k / (double)(normal - 1) : 0);
                int ex = k < extraStar.Length ? extraStar[k] : 0;
                void Set(int lv)
                {
                    foreach (var m in e.team)
                    {
                        m.level = lv;
                        m.star = Math.Max(1, Math.Min(20, Sim.StarAt(D.Cfg, lv) + ex));
                    }
                }
                int best = 1;
                double bestErr = double.MaxValue;
                for (int lv = 1; lv <= 200; lv++)
                {
                    Set(lv);
                    double err = Math.Abs(Math.Log(Underground.Power(D, e) / target));
                    if (err < bestErr) { bestErr = err; best = lv; }
                }
                Set(best);
                int pw = Underground.Power(D, e);
                lvs.Add($"[{best}, {e.team[0].star}]");
                line.Add($"{c.tiers[Math.Min(k, c.tiers.Count - 1)].name} {Underground.Count(e)}t cấp {best} sao {e.team[0].star}: {pw / 1000.0:0.#}k (đích {target / 1000:0.#}k)");
            }
            outDays.Add("[" + string.Join(", ", lvs) + "]");
            Console.WriteLine($"Ngày {day}: " + string.Join(" | ", line));
        }
        File.WriteAllText(Path.Combine("..", "ug_levels.json"), "[" + string.Join(",\n", outDays) + "]");
    }

    // dò cấp đội địch cho từng đội để trúng tỉ lệ thắng mục tiêu của bậc (đội mẫu ở cấp mở bậc); ghi ug_levels.json
    static void UgCal(int n)
    {
        var c = D.Cfg.casino.underground;
        double[] target = { 0.8, 0.7, 0.55, 0.4, 0.25, 0.1 };
        int[] extraStar = { 2, 1, 0, 0, 0, 0 };
        var outDays = new List<string>();
        for (int day = 0; day < c.rotation.Count; day++)
        {
            var ud = c.rotation[day];
            var lvs = new List<string>();
            var line = new List<string>();
            for (int k = 0; k < ud.entries.Count; k++)
            {
                var e = ud.entries[k];
                var tier = c.tiers[Math.Min(k, c.tiers.Count - 1)];
                int lo = Math.Max(1, tier.level - 30), hi = Math.Min(200, tier.level + 45);
                while (hi - lo > 1)
                {
                    int mid = (lo + hi) / 2;
                    foreach (var m in e.team)
                    {
                        m.level = mid;
                        m.star = Math.Max(1, Math.Min(20, Sim.StarAt(D.Cfg, mid) + extraStar[Math.Min(k, 5)]));
                    }
                    if (WinRate(e, tier.level, n) >= target[Math.Min(k, 5)]) lo = mid; else hi = mid;
                }
                foreach (var m in e.team)
                {
                    m.level = lo;
                    m.star = Math.Max(1, Math.Min(20, Sim.StarAt(D.Cfg, lo) + extraStar[Math.Min(k, 5)]));
                }
                double wr = WinRate(e, tier.level, n * 2);
                lvs.Add($"[{lo}, {e.team[0].star}]");
                line.Add($"{tier.name}: cấp {lo} sao {e.team[0].star} thắng {wr:P0}");
            }
            outDays.Add("[" + string.Join(", ", lvs) + "]");
            Console.WriteLine($"Ngày {day}: " + string.Join(" | ", line));
        }
        File.WriteAllText(Path.Combine("..", "ug_levels.json"), "[" + string.Join(",\n", outDays) + "]");
    }

    static void Ug(int n)
    {
        var c = D.Cfg.casino.underground;
        // đội người chơi mẫu: 3 tướng Khá / Hiếm hợp hệ với địch? dùng đội trung bình (theo simTeams nếu có), sao theo cấp người chơi
        var teamIds = D.Heroes.Where(h => !h.minion && (h.rarity == Rarity.Rare)).Select(h => h.id).OrderBy(x => x).ToList();
        for (int day = 0; day < c.rotation.Count; day++)
        {
            var ud = c.rotation[day];
            var line = new List<string>();
            for (int k = 0; k < ud.entries.Count; k++)
            {
                var e = ud.entries[k];
                var tier = c.tiers[Math.Min(k, c.tiers.Count - 1)];
                int lv = tier.level;
                int star = Math.Max(1, Math.Min(20, Sim.StarAt(D.Cfg, lv)));
                // đội: 3 tướng Hiếm, ưu tiên khắc hệ của chủ lực địch
                var leadElem = D.Hero(e.team[0].hero).elem;
                var team = D.Heroes.Where(h => !h.minion && h.rarity >= Rarity.Rare && h.rarity <= Rarity.Epic)
                    .OrderByDescending(h => Elements.Beats(h.elem) == leadElem ? 1 : 0).ThenBy(h => h.id).Take(3).Select(h => h.id).ToList();
                var s = Sim.Setup(D, team, lv, star, 4);
                int win = 0;
                for (int i = 0; i < n; i++)
                {
                    var t0 = Teams.Player(s, team.Take(Underground.TeamLimit(e)).ToList(), D);
                    t0.ai = true;
                    Underground.ApplyRule(D, e.rule, t0, false);
                    var b = Battle.Create(D, t0, Underground.Enemy(D, e), (uint)(2000 + i * 7919), s.level, s.level);
                    BattleSim.Run(b);
                    if (b.winner == 0) win++;
                }
                line.Add($"{tier.name}:{win * 100 / n}%");
            }
            Console.WriteLine($"Ngầm ngày {day}: " + string.Join("  ", line));
        }
    }

    static void SaveRound()
    {
        var s = SaveData.New(D, 0, "ti_tach");
        s.level = 60;
        double now = 1795000000000;
        var rng = new Rng(3);
        var st = Casino.Roll(s, D, now);
        st.dex["ca_moi_bac"] = new FishRec { n = 2, best = 15.5 };
        st.creel.Add(new CaughtFish { id = "ca_moi_bac", size = 12 });
        st.Jar("blackjack").fill = 120;
        st.cupPts = new[] { 3, 0, 0, 0, 0 };
        st.innProg["fish5"] = 2;
        string js = SaveCodec.Write(s);
        var status = SaveCodec.Read(js, D, out var s2);
        var st2 = s2.casino;
        bool ok = st2 != null && st2.dex["ca_moi_bac"].best == 15.5 && st2.creel.Count == 1 && st2.jars["blackjack"].fill == 120 && st2.cupPts[0] == 3
                  && st2.innProg["fish5"] == 2 && st2.day == st.day && SaveCodec.Write(s2) == js;
        Console.WriteLine($"Bản lưu đọc ghi casino: {(ok ? "khớp" : "LỆCH")} ({status})");
    }

    static void Events()
    {
        double now = new DateTimeOffset(2026, 11, 25, 12, 0, 0, TimeSpan.FromHours(7)).ToUnixTimeMilliseconds();
        for (int k = 0; k < 15; k++)
        {
            double t = now + k * Casino.Day;
            var act = Casino.Active(D, t);
            Console.WriteLine($"{Underground.Ymd(Casino.Today(t))}: " + string.Join(", ", act.Select(a => $"{a.ev.name} (#{a.occ}, khách {Casino.Guest(D, a)}, còn {Casino.Left(a, t) / 3600000:F0} giờ)"))
                              + (act.Count == 0 ? "(nghỉ) sắp: " + string.Join(", ", Casino.Upcoming(D, t, 2).Select(u => u.ev.name + " " + Underground.Ymd(u.startDay))) : ""));
        }
    }

    static void Fish()
    {
        var c = D.Cfg.casino.fishing;
        var rng = new Rng(5);
        for (int spot = 0; spot < c.spots.Count; spot++)
            foreach (double power in new[] { 0.2, 1.0 })
            {
                var cnt = new int[5];
                double val = 0;
                int n = 20000;
                for (int i = 0; i < n; i++)
                {
                    var b = Fishing.Pick(c, spot, power, false, null, false, null, rng);
                    cnt[(int)b.fish.rar]++;
                    val += Fishing.Price(D, new CaughtFish { id = b.fish.id, size = b.size });
                }
                Console.WriteLine($"Câu {c.spots[spot].name} lực {power}: " + string.Join(" ", cnt.Select((x, i) => $"{(Rarity)i}:{x * 100.0 / n:F0}%")) + $" | giá TB {val / n:F1} bi");
            }
        // người chơi: 10 mồi/ngày, vài ngày
        var s = SaveData.New(D, 0, "ti_tach");
        s.level = 30;
        double now = 1795000000000;
        int balls0 = s.balls;
        for (int day = 0; day < 7; day++)
        {
            double t = now + day * Casino.Day;
            for (int k = 0; k < 10; k++)
            {
                var b = Fishing.Cast(s, D, 0, 0.7, t, rng, out var why);
                if (b == null) { Console.WriteLine("  " + why); break; }
                if (rng.Chance(0.75)) Fishing.Land(s, D, b, t, rng);
            }
            Fishing.SellCreel(s, D);
        }
        Console.WriteLine($"Câu 7 ngày (gần bờ, 75% kéo được): +{s.balls - balls0} bi, Sổ Cá {s.casino.dex.Count} loài");
    }

    static void Market()
    {
        var s = SaveData.New(D, 0, "ti_tach");
        s.level = 40;
        foreach (var h in new[] { "so_ngoc", "khien_bac", "hong_lien" }) { s.Hero(h).owned = true; }
        s.balls = 5000;
        double now = new DateTimeOffset(2026, 11, 25, 21, 0, 0, TimeSpan.FromHours(7)).ToUnixTimeMilliseconds();
        var stock = BlackMarket.Stock(s, D, now);
        foreach (var sl in stock)
            Console.WriteLine($"Chợ ô {sl.idx}: {sl.offer.kind} {string.Join(",", sl.items.Select(i => i.k + "×" + i.n + (i.h != null ? " " + i.h : "")))} giá {sl.price}{(sl.night ? " (đêm)" : "")}");
        Console.WriteLine($"Làm mới: {BlackMarket.RefreshCost(s, D, now)} bi; đổi hàng sau {BlackMarket.NextRefresh(D, now) / 3600000:F1} giờ");
        var rng = new Rng(1);
        var r = BlackMarket.Buy(s, D, 0, now, rng, out var why);
        Console.WriteLine($"Mua ô 0: {(r == null ? why : string.Join(", ", r.Select(x => x.k + " " + x.n)))}; còn {s.balls} bi");
        foreach (var (roll, p) in BlackMarket.MysteryOdds(D)) Console.WriteLine($"  Túi hàng lậu: {roll.k} {roll.min}-{roll.max}: {p:P0}");
    }
}
