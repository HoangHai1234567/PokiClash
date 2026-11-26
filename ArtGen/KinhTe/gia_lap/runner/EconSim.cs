// Giả lập kinh tế cả game cho một người chơi ảo: ải, AFK, cây bi, trang trại (gần đúng cho Nhà), máy bi, cửa hàng + Offer Engine, quảng
// cáo thưởng, đảo Casino (câu cá, đua, lều may rủi, chợ đen, hầm đấu, quán trọ). Mọi luật gọi thẳng lõi game (PokiClash.Core); phần
// "người chơi làm gì" (xem quảng cáo nào, mua gói nào, cược bao nhiêu) là giả định của persona, ghi ở Persona.
// Mở rộng ProgressSim (Core/ProgressSim.cs): cùng cách chọn ải, tỉ lệ thắng = máy tự đánh + mức "người giỏi hơn máy".
// Chưa mô phỏng: Đền Huy Hiệu, Hang Tiềm Năng (cộng đá gần đúng theo cấp như ProgressSim.SideEvo), công trình Nhà ngoài cây bi và ruộng.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;

public sealed class Persona
{
    public int id;
    public string eng, mon, cas; // nhãn nhóm
    public int sessions, battles;
    public double skill, dayProb = 1;
    public double adRate; // xác suất nhận một cơ hội quảng cáo
    public int adCap; // số quảng cáo nhiều nhất mỗi ngày người này chịu xem
    public int spend; // 0 không trả, 1 chi ít, 2 chi vừa, 3 chi lớn
    public double budget; // trần USD trong 30 ngày
    public int casino; // 0 không chơi đảo, 1 thận trọng (chỉ cược có lợi), 2 máu me (cược to, chơi hết lượt)
    public uint seed;
    public int startShift; // lệch ngày bắt đầu (vị trí trong vòng sự kiện 14 ngày)
}

public sealed class Ledger
{
    public readonly SortedDictionary<string, double> ballsIn = new SortedDictionary<string, double>(), ballsOut = new SortedDictionary<string, double>(),
        shards = new SortedDictionary<string, double>(), evo = new SortedDictionary<string, double>(), stones = new SortedDictionary<string, double>(),
        crystals = new SortedDictionary<string, double>(), copies = new SortedDictionary<string, double>(), exp = new SortedDictionary<string, double>(),
        usd = new SortedDictionary<string, double>(), ads = new SortedDictionary<string, double>(), count = new SortedDictionary<string, double>(),
        iapValue = new SortedDictionary<string, double>();

    public static void Add(SortedDictionary<string, double> m, string k, double v)
    {
        if (v == 0) return;
        m[k] = (m.TryGetValue(k, out var x) ? x : 0) + v;
    }
}

// Các đổi luật cần sửa code game (chưa có trong lõi): giả lập ở runner để đo trước. Đọc từ khối "sim" trong balance.json của bộ số.
public sealed class SimRules
{
    // Từ 2026-11-26 các luật sau đã nằm trong game (đọc từ balance.json), máy giả lập gọi thẳng lõi: số trận đánh lại đủ bi
    // (stageBalls.replayFull / replayPct), lượt trao ngay của Bỏ quảng cáo (ads.noAdsInstant), Lọ Bi cách nhau (piggy.gapDays),
    // Gói Tiếp Sức không tính dòng "thả bi" khi bi chưa đủ lên một cấp (Offers.FreeFix), thẻ thừa đổi đá tiềm năng.
    public double[] mocPower; // hệ số sức theo mốc tướng 1..10 của mỗi đảo (null: theo độ hiếm như game)
    public List<int[]> grants = new List<int[]>(); // {ngày, mốc, sao, cấp thẻ, đá tiến hóa kèm}: ngày đó người chơi được mở khoá tướng mốc đó của đảo cùng hệ tướng khởi đầu
    public List<string> x2Packs = new List<string>(); // gói kèm vật phẩm "x2 EXP máy bi": lần vào máy kế tiếp EXP nhân đôi (tối đa x2Balls bi)
    public int x2Balls = 20000;
    public int piggyRotate; // Lọ Bi chỉ mở 3 ngày đầu mỗi chu kỳ N ngày (0: luôn mở)

    public static SimRules Read(string balanceJson)
    {
        var r = new SimRules();
        var o = J.Obj(J.Obj(MiniJson.Parse(balanceJson)), "sim");
        if (o == null) return r;
        foreach (var x in J.Arr(o, "x2Packs")) if (x is string t) r.x2Packs.Add(t);
        r.x2Balls = J.Int(o, "x2Balls", r.x2Balls);
        r.piggyRotate = J.Int(o, "piggyRotate", r.piggyRotate);
        var mp = J.Arr(o, "mocPower");
        if (mp.Count > 0) r.mocPower = mp.Select(x => x is double v ? v : 1).ToArray();
        foreach (var g in J.Arr(o, "grants"))
        {
            var go = J.Obj(g);
            if (go != null) r.grants.Add(new[] { J.Int(go, "day", 1), J.Int(go, "moc", 1), J.Int(go, "star", 1), J.Int(go, "card", 1), J.Int(go, "evo", 0) });
        }
        return r;
    }
}

public sealed class EconSim
{
    public static SimRules Rules = new SimRules();

    // tướng mốc k (1..10) của từng đảo: tướng chủ lực của ải tướng / mini boss / boss thứ k
    public static Dictionary<Elem, List<string>> Moc(GameData d)
    {
        var m = new Dictionary<Elem, List<string>>();
        foreach (var z in d.Zones)
            m[z.id] = d.ZoneStages(z.id).Where(st => st.tag == StageTag.Hero || st.kind != StageKind.Normal).OrderBy(st => st.idx)
                .Select(st => Teams.StageLead(st, d).hero).ToList();
        return m;
    }

    void Grants()
    {
        foreach (var g in Rules.grants)
        {
            if (g[0] != dayIdx + 1) continue;
            var list = Moc(d)[d.Hero(s.starter).elem];
            if (g[1] < 1 || g[1] > list.Count) continue;
            var hp = s.Hero(list[g[1] - 1]);
            hp.owned = true;
            hp.star = Math.Max(hp.star, g[2]);
            foreach (var slot in Progress.Slots) hp.Card(slot).lv = Math.Max(hp.Card(slot).lv, Math.Min(cfg.cardMax, g[3]));
            s.evoStones += g[4]; // đá tiến hóa kèm gói
            Count("tướng được mở khoá (giả lập gói)");
        }
    }
    bool x2Pending;
    const double H = 3600000, Day = 86400000;
    readonly GameData d;
    readonly BalanceConfig cfg;
    readonly Persona p;
    readonly SaveData s;
    readonly Rng rng;
    readonly Dictionary<string, double> cache;
    readonly int days, simN;
    public readonly Ledger L = new Ledger();
    readonly double t0;
    double now;
    int dayIdx, adsToday, sessionOfDay;
    double usdTotal;
    int refillBuysToday, lastWeekHero = -1, lossStage, lossStreak;
    bool boughtDailyEgg;
    readonly HashSet<string> flags = new HashSet<string>();

    // theo ngày (chỉ số 0 = lúc mới chơi)
    public readonly int[] level, cleared, zonesDone, owned, stars, ballsHeld, power, adsCum, sessionsCum;
    public readonly double[] usdCum, droppedCum, ballsInCum, shardsCum;
    public int finishedDay = -1, maxLevelDay = -1, brokenDay = -1;
    public const int BrokenAt = 1000000; // người chơi thường không bao giờ cầm tới 1 triệu bi (gói lớn nhất 90.000)
    public bool timedOut;
    public int stoppedDay = -1;
    // trần tính theo giờ CPU của tiến trình (tiến trình chạy ưu tiên thấp có thể bị treo chờ CPU rất lâu: giờ đồng hồ không dùng được)
    readonly double cpu0 = System.Diagnostics.Process.GetCurrentProcess().TotalProcessorTime.TotalSeconds;
    public static double WallLimit = 300;
    public static readonly int[] SnapDays = { 1, 3, 7, 14, 21, 30 };
    public readonly SortedDictionary<int, Dictionary<string, SortedDictionary<string, double>>> snaps = new SortedDictionary<int, Dictionary<string, SortedDictionary<string, double>>>();

    public EconSim(GameData data, Persona persona, int days, int simN, Dictionary<string, double> cache)
    {
        d = data;
        cfg = d.Cfg;
        p = persona;
        this.days = days;
        this.simN = simN;
        this.cache = cache;
        rng = new Rng(p.seed);
        // bắt đầu 0 giờ một ngày thật (lịch sự kiện đảo tính từ ngày mốc); mỗi người lệch vài ngày để rải đều vòng sự kiện
        t0 = new DateTimeOffset(2026, 12, 1, 0, 0, 0, TimeZoneInfo.Local.GetUtcOffset(new DateTime(2026, 12, 1))).ToUnixTimeMilliseconds() + p.startShift * Day;
        string starter = d.Starters[(int)(p.seed % (uint)d.Starters.Count)];
        s = SaveData.New(d, (long)t0, starter);
        s.intro = true;
        int n = days + 1;
        level = new int[n]; cleared = new int[n]; zonesDone = new int[n]; owned = new int[n]; stars = new int[n]; ballsHeld = new int[n]; power = new int[n];
        adsCum = new int[n]; sessionsCum = new int[n];
        usdCum = new double[n]; droppedCum = new double[n]; ballsInCum = new double[n]; shardsCum = new double[n];
    }

    public SaveData Save => s;

    // ---------- đo ----------

    long ShardTotal()
    {
        long n = 0;
        foreach (var h in d.Heroes)
        {
            var hp = s.Hero(h.id);
            if (hp == null) continue;
            n += hp.shards;
            if (!hp.owned) continue;
            n += h.shards;
            for (int g = 2; g <= hp.star; g++)
            {
                int c = Progress.ShardCost(cfg, h, g);
                if (c != int.MaxValue) n += c;
            }
        }
        return n;
    }

    long CopyTotal()
    {
        long n = 0;
        foreach (var kv in s.heroes)
            foreach (var slot in Progress.Slots)
            {
                var c = kv.Value.Card(slot);
                n += c.copies;
                for (int lv = 1; lv < c.lv; lv++) n += cfg.cardReq[Math.Min(lv, cfg.cardReq.Length - 1)];
            }
        return n;
    }

    double[] expCum;
    double ExpTotal()
    {
        if (expCum == null)
        {
            expCum = new double[cfg.maxLevel + 2];
            for (int lv = 1; lv <= cfg.maxLevel; lv++) expCum[lv + 1] = expCum[lv] + Progress.ExpToNext(lv, cfg);
        }
        return expCum[Math.Min(s.level, cfg.maxLevel + 1)] + s.exp;
    }

    // chạy một việc, ghi phần tài nguyên đổi vào nguồn src; trứng và vé nhận trong việc đó dùng luôn (mảnh tính cho nguồn này)
    // skip: phần bi đổi đã ghi ở chỗ khác (dòng cược / trả của bàn, bi đã thả), trừ ra khỏi phần ghi ở đây
    void Do(string src, Action a, Func<double> skip = null)
    {
        int b0 = s.balls, e0 = s.evoStones, st0 = s.potentialStones, cr0 = s.potentialCrystals;
        long sh0 = ShardTotal(), cp0 = CopyTotal();
        double x0 = ExpTotal();
        a();
        UseBag();
        int db = s.balls - b0 - (int)Math.Round(skip?.Invoke() ?? 0);
        if (s.balls > BrokenAt)
        {
            // bi phình vô hạn (vòng lặp tự nuôi): ghi ngày vỡ, chặn lại để khỏi tràn số
            if (brokenDay < 0) brokenDay = dayIdx + 1;
            s.balls = BrokenAt;
        }
        if (db > 0) Ledger.Add(L.ballsIn, src, db);
        else Ledger.Add(L.ballsOut, src, -db);
        Ledger.Add(L.shards, src, ShardTotal() - sh0);
        if (s.evoStones > e0) Ledger.Add(L.evo, src, s.evoStones - e0);
        if (s.potentialStones > st0) Ledger.Add(L.stones, src, s.potentialStones - st0);
        if (s.potentialCrystals > cr0) Ledger.Add(L.crystals, src, s.potentialCrystals - cr0);
        Ledger.Add(L.copies, src, CopyTotal() - cp0);
        Ledger.Add(L.exp, src, ExpTotal() - x0);
    }

    void Count(string k, double v = 1) => Ledger.Add(L.count, k, v);

    // nở hết trứng trong túi, dùng hết vé
    void UseBag()
    {
        if (s.shop == null) return;
        for (int tier = 0; tier < Eggs.Tiers; tier++)
        {
            int n = Eggs.Bag(s, tier);
            if (n <= 0) continue;
            var got = Eggs.Open(s, d, tier, n, true, now, rng);
            Count("egg_open_" + tier, n);
            if (got.Any(h => h.tier >= (int)Rarity.Legend)) flags.Add("legend_hatch");
        }
        var st = s.shop;
        int guard = 0;
        while (st.tickets.Count > 0 && guard++ < 50)
        {
            var ch = Shop.TicketChoicesOf(s, d, st.tickets[0], now);
            if (ch.Count == 0) { st.tickets.RemoveAt(0); continue; }
            // ưu tiên tướng chưa có hiếm nhất, không thì tướng trong đội gần lên sao
            var pick = ch.Where(h => !s.Hero(h).owned).OrderByDescending(h => (int)d.Hero(h).rarity).FirstOrDefault() ?? ch[0];
            if (Shop.UseTicket(s, d, false, 0, pick, now, rng) == null) st.tickets.RemoveAt(0);
            Count("ticket_used");
        }
        guard = 0;
        while (st.Item(Shop.TicketWeek) > 0 && guard++ < 20)
        {
            var feat = Shop.FeaturedNow(d, now);
            var pick = feat.FirstOrDefault(h => !s.Hero(h).owned) ?? feat.FirstOrDefault();
            if (pick == null || Shop.UseTicket(s, d, true, 0, pick, now, rng) == null) break;
        }
    }

    // ---------- quảng cáo, tiền ----------

    int Today => Shop.Today(now);

    bool TryAd(string place)
    {
        if (p.adRate <= 0 || !Tutorial.CoreDone(s)) return false;
        if (AdGate.Left(s, cfg, Today, place) <= 0) return false;
        bool instant = AdGate.UseInstant(s, cfg, Today);
        if (!instant)
        {
            if (adsToday >= p.adCap) return false;
            if (!rng.Chance(p.adRate)) return false;
            if (Shop.UseAdSkip(s, cfg.shop, now)) instant = true;
        }
        if (!AdGate.Use(s, cfg, Today, place)) return false;
        Shop.OnAd(s, now);
        if (!instant)
        {
            adsToday++;
            Ledger.Add(L.ads, place, 1);
        }
        else Ledger.Add(L.ads, place + "(trao ngay)", 1);
        return true;
    }

    // trần chi của persona, rải theo ngày (dồn về đầu: ngày 1 đã được tiêu 30% trần, tới ngày 22 được tiêu hết)
    // chạy dài hơn 30 ngày: mỗi tháng thêm một lần trần (30 ngày đầu y như cũ)
    bool CanPay(double usd) => p.spend > 0 && usdTotal + usd <= p.budget * Math.Min(Math.Ceiling((dayIdx + 1) / 30.0), (dayIdx + 9) / 30.0) + 0.001;

    void Paid(string product, double usd)
    {
        usdTotal += usd;
        Ledger.Add(L.usd, product, usd);
        Count("buy:" + product);
    }

    bool BuyPack(string id)
    {
        var pack = cfg.shop.Pack(id);
        if (pack == null || !CanPay(pack.price) || !Shop.CanBuy(s, d, pack, now)) return false;
        if (id == "piggy")
        {
            if (Rules.piggyRotate > 0 && dayIdx % Rules.piggyRotate >= 3) return false;
        }
        double v = Shop.PackValue(s, d, pack);
        bool ok = false;
        Do("iap:" + id, () => ok = Shop.BuyPack(s, d, id, now, rng) != null);
        if (ok)
        {
            Paid(id, pack.price);
            Ledger.Add(L.iapValue, id, v);
            if (Rules.x2Packs.Contains(id)) x2Pending = true;
        }
        return ok;
    }

    // xác suất mua một ưu đãi tự bật theo nhóm chi tiêu (giả định)
    double WantOffer(string tpl, double price)
    {
        switch (p.spend)
        {
            // Gói Vượt Mốc ("jump"): người chi ít mua bản 4,99 USD một nửa số lần; người chi vừa mua tới 19,99; người chi lớn mua hết
            case 1: return tpl == "starter3" ? 0.9 : tpl == "launch" ? 0.5 : tpl == "jump" ? (price <= 4.99 ? 0.5 : 0) : price <= 1.99 ? 0.25 : 0;
            case 2: return tpl == "starter3" || tpl.StartsWith("launch") ? 0.95 : tpl == "jump" ? (price <= 9.99 ? 0.6 : price <= 19.99 ? 0.3 : 0.05)
                : price <= 4.99 ? 0.5 : price <= 9.99 ? 0.25 : 0.05;
            case 3: return 0.9;
            default: return 0;
        }
    }

    void HandlePopups(List<Popup> pops)
    {
        foreach (var pop in pops)
        {
            Offers.Shown(s, d, pop, now);
            bool bought = false;
            switch (pop.kind)
            {
                case "offer":
                case "comeback":
                {
                    var o = Shop.FindOffer(s, pop.id);
                    if (o == null) break;
                    Count("popup:" + o.tpl);
                    // nhóm chọn một (nạp đầu 3 bậc): người chi ít lấy bậc 1, chi vừa bậc 2, chi lớn bậc 3
                    if (o.pack != null && cfg.shop.Pack(o.pack)?.group == o.pack)
                    {
                        var tiers = cfg.shop.packs.Where(q => q.group == o.pack).OrderBy(q => q.price).ToList();
                        var want = tiers[Math.Min(tiers.Count - 1, Math.Max(0, p.spend - 1))];
                        var alt = Shop.Live(s, now).FirstOrDefault(a2 => a2.pack == want.id);
                        if (alt != null) o = alt;
                    }
                    if (o.price > 0 && CanPay(o.price) && rng.Chance(WantOffer(o.tpl, o.price)))
                    {
                        double v = Shop.Value(cfg.shop, d, Shop.OfferItems(s, d, o));
                        bool ok = false;
                        Do("iap:" + o.tpl, () => ok = Shop.BuyOffer(s, d, o.uid, now, rng) != null);
                        if (ok)
                        {
                            Paid(o.tpl, o.price);
                            Ledger.Add(L.iapValue, o.tpl, v);
                            bought = true;
                        }
                    }
                    break;
                }
                case "piggy":
                    Count("popup:piggy");
                    if (p.spend >= 2) bought = BuyPack("piggy");
                    break;
                case "intro":
                    Count("popup:intro_" + pop.id);
                    if (pop.id == "week_card" && p.spend >= 1 && rng.Chance(p.spend == 1 ? 0.6 : 0.95)) bought = BuyPack("week_card");
                    if (pop.id == "fund" && p.spend >= 2) bought = BuyPack("fund");
                    break;
                case "chain": Count("popup:chain"); break;
                case "refill": Count("popup:refill"); break;
                case "claims": break;
            }
            Offers.Closed(s, pop, bought, false, now);
        }
    }

    void ClaimFree()
    {
        if (!Tutorial.CoreDone(s)) return;
        if (Shop.GiftReady(s, now))
        {
            bool twice = TryAd(AdGate.DailyGift);
            Do(twice ? "qc:quà ngày ×2" : "quà ngày", () => Shop.ClaimGift(s, d, twice, now, rng));
        }
        if (Shop.CardClaimable(s, "week", now)) Do("iap:week_card", () => Shop.ClaimCard(s, d, "week", now, rng));
        if (Shop.CardClaimable(s, "month", now)) Do("iap:adventure_pass", () => Shop.ClaimCard(s, d, "month", now, rng));
        foreach (var id in s.shop.days.Keys.ToList())
            if (Shop.DayClaimable(s, d, id, now)) Do("iap:" + id, () => Shop.ClaimDay(s, d, id, now, rng));
        for (int i = 0; i < cfg.shop.fund.Count; i++)
        {
            int k = i;
            if (Shop.FundClaimable(s, cfg.shop, k, false)) Do("quỹ (hàng free)", () => Shop.FundClaim(s, d, k, false, now, rng));
            if (Shop.FundClaimable(s, cfg.shop, k, true)) Do("iap:fund", () => Shop.FundClaim(s, d, k, true, now, rng));
        }
        // Chuỗi Quà: ô miễn phí nhận hết; ô trả tiền theo nhóm chi
        for (int guard = 0; guard < 10 && Shop.ChainLive(s, now); guard++)
        {
            var def = Shop.ChainNow(s, cfg.shop);
            int step = s.shop.chainStep;
            if (def == null || step >= def.steps.Count) break;
            var cs = def.steps[step];
            if (cs.price <= 0)
            {
                Do("chuỗi quà (ô free)", () => Shop.ChainTake(s, d, step, false, now, rng));
                continue;
            }
            double want = p.spend == 3 ? 0.9 : p.spend == 2 ? (cs.price <= 2.99 ? 0.6 : 0.3) : p.spend == 1 ? (cs.price <= 0.99 ? 0.3 : 0) : 0;
            if (flags.Contains("chain_stop_" + s.shop.chainCycle) || !CanPay(cs.price) || !rng.Chance(want))
            {
                flags.Add("chain_stop_" + s.shop.chainCycle);
                break;
            }
            double v = Shop.Value(cfg.shop, d, Shop.Resolve(s, d, cs.items, true, null));
            Do("iap:chain", () => Shop.ChainTake(s, d, step, true, now, rng));
            Paid("chain", cs.price);
            Ledger.Add(L.iapValue, "chain", v);
        }
        for (int i = 0; i < cfg.shop.adMilestones.Count; i++)
        {
            int k = i;
            if (Shop.AdMilestoneReady(s, cfg.shop, k, now)) Do("qc:mốc quảng cáo", () => Shop.ClaimAdMilestone(s, d, k, now, rng));
        }
    }

    // mua theo lịch của nhóm chi tiêu (giả định), mỗi ngày xét một lần ở phiên đầu
    void Shopping()
    {
        if (p.spend == 0 || !Tutorial.CoreDone(s)) return;
        int day = dayIdx;
        // nạp đầu 3 bậc chọn 1 (ngày 2), trước các gói khác
        if (day == 1) BuyPack(p.spend == 1 ? "first_1" : p.spend == 2 ? "first_2" : "first_3");
        if (p.spend >= 1)
        {
            if (!Shop.CardActive(s, "week", now) && (s.level >= 10 || day >= 2) && rng.Chance(p.spend == 1 ? 0.5 : 0.95)) BuyPack("week_card");
            if (!AdGate.PassActive(s, now) && day >= (p.spend == 1 ? 4 : 1) && (p.spend >= 2 || p.seed % 2 == 0)) BuyPack("adventure_pass");
        }
        if (p.spend >= 2)
        {
            if (!s.shop.fund && s.level >= 10) BuyPack("fund");
            if (!AdGate.NoAds(s) && p.adRate > 0 && day >= 2) BuyPack("no_ads");
            if (Shop.PiggyFull(s, cfg.shop)) BuyPack("piggy");
            if (rng.Chance(p.spend == 3 ? 0.9 : 0.35)) BuyPack("egg_daily");
            int wk = Shop.Week(Today);
            if (wk != lastWeekHero && rng.Chance(p.spend == 3 ? 0.9 : 0.4))
            {
                lastWeekHero = wk;
                BuyPack("weekly_hero");
            }
            if (p.spend == 2)
            {
                if (day == 3 && Shop.FirstBonus(s, cfg.shop.Pack("balls_2"))) BuyPack("balls_2");
                if (day == 12 && Shop.FirstBonus(s, cfg.shop.Pack("balls_3"))) BuyPack("balls_3");
            }
        }
        // các gói mới của bộ số gộp (không có trong dữ liệu thì BuyPack tự bỏ qua)
        if (NeedEvo() && rng.Chance(p.spend == 1 ? 0.15 : p.spend == 2 ? 0.5 : 0.9)) BuyPack("evo_daily");
        if (p.spend >= 2 && NeedEvo() && day % 7 == 4) BuyPack("evo_week");
        if (Casino.Open(s, d))
            foreach (var sp in Casino.Active(d, now))
            {
                if (!flags.Add("evpack:" + sp.Key)) continue;
                if (rng.Chance(p.spend == 1 ? 0.3 : p.spend == 2 ? 0.6 : 0.95)) BuyPack("event_1");
                if (p.spend >= 2 && rng.Chance(p.spend == 2 ? 0.4 : 0.9)) BuyPack("event_2");
                if (p.spend >= 3) BuyPack("event_3");
            }
        if (p.spend >= 3)
        {
            // lần đầu tặng đôi: mỗi 2 ngày một bậc bi từ nhỏ tới lớn; sau đó mỗi tuần một Thùng bi
            if (day % 2 == 1)
            {
                var next = Enumerable.Range(1, 6).Select(i => cfg.shop.Pack("balls_" + i)).FirstOrDefault(x => x != null && Shop.FirstBonus(s, x));
                if (next != null) BuyPack(next.id);
                else if (day % 7 == 1) BuyPack("balls_4");
            }
            if (day % 7 == 2) BuyPack("egg_3x10");
            if (day % 14 == 6) BuyPack("egg_4x10");
        }
    }

    // ---------- trận ----------

    static double Strength(GameData d, SaveData s, HeroDef h) =>
        HeroStats.Power(d.Cfg, h, Teams.MemberOf(s, h.id, d)) * Math.Sqrt(Progress.CardSum(s, h.id) / 3.0);

    List<string> BestTeam(StageDef target)
    {
        var foe = target != null ? d.Hero(Teams.StageLead(target, d).hero).elem : (Elem?)null;
        double Edge(HeroDef h) => foe is Elem e
            ? Math.Sqrt(Elements.Mult(h.elem, e, h.id == s.starter, false) / Elements.Mult(e, h.elem, false, h.id == s.starter))
            : 1;
        var team = d.Heroes.Where(h => s.Hero(h.id).owned)
            .OrderByDescending(h => Strength(d, s, h) * Edge(h)).ThenBy(h => d.Heroes.IndexOf(h))
            .Take(Progress.TeamSlots(s)).Select(h => h.id).ToList();
        s.team = team;
        return team;
    }

    double WinChance(StageDef st, List<string> team, double boost = 0)
    {
        var key = $"{st.id}|{s.level}|{s.starter}|" + string.Join(",", team.Select(h =>
        {
            var hp = s.Hero(h);
            return $"{h}:{hp.star}:{hp.skill.lv}{hp.ult.lv}{hp.passive.lv}";
        })) + "|" + SoPhep.Key(s) + (boost > 0 ? "|b" : "");
        if (!cache.TryGetValue(key, out var bot))
        {
            var bonus = boost > 0 ? new StatMods { hpPct = boost, atkPct = boost } : null;
            bot = Sim.Stage(d, s, st, simN, 1000, team, bonus).WinRate;
            cache[key] = bot;
        }
        return Math.Min(1, bot + p.skill);
    }

    StageDef AfkTarget()
    {
        if (HeroStats.HeroMult != null)
        {
            StageDef best = null;
            double bp = 0;
            foreach (var st in d.Stages.Where(x => Progress.StageCleared(s, x)))
                foreach (var dr in Afk.Pool(st))
                {
                    var hp = s.Hero(dr.hero);
                    if (hp == null || hp.star >= StarTier.MaxStar) continue;
                    if (hp.owned && Progress.NextStep(s, d, dr.hero) != Progress.StarStep.StarUp) continue; // đang chờ đá tiến hóa: mảnh chưa dùng được
                    double pwr = HeroStats.PowerOfHero(d.Hero(dr.hero));
                    if (pwr > bp) { bp = pwr; best = st; }
                }
            return best;
        }
        foreach (var h in d.Heroes.Where(x => s.Hero(x.id).owned && s.Hero(x.id).star < StarTier.MaxStar)
                     .OrderByDescending(x => s.Hero(x.id).star).ThenByDescending(x => Strength(d, s, x)))
        {
            StageDef best = null;
            double bw = 0;
            foreach (var st in d.Stages.Where(x => Progress.StageCleared(s, x)))
            {
                var pool = Afk.Pool(st);
                double sum = pool.Sum(x => x.chance), w = pool.Where(x => x.hero == h.id).Sum(x => x.chance);
                if (w <= 0) continue;
                if (w / sum >= bw) { bw = w / sum; best = st; }
            }
            if (best == null) continue;
            var g = Progress.ShardGoal(s, d, h.id);
            return g.need > 0 && g.have < g.need ? best : null;
        }
        return null;
    }

    bool FreeFix(List<string> team)
    {
        return Offers.FreeFix(s, d, team) != null;
    }

    void Battles()
    {
        for (int b = 0; b < p.battles; b++)
        {
            var zone = Progress.RecommendedZone(s, d);
            var target = Progress.NextStage(s, d, zone.id);
            var team = BestTeam(target);
            if (team.Count == 0) break;
            double pw = target != null ? WinChance(target, team) : 0;
            bool farm = false;
            if (target == null || pw < 0.3)
            {
                if (target != null) Count("tường (ải kế < 30%)");
                // ải đã qua nhiều bi nhất mà gần chắc thắng (thử tối đa 6 ải, bỏ boss / mini boss)
                var cand = d.Stages.Where(st => Progress.StageCleared(s, st) && st.kind == StageKind.Normal)
                    .OrderByDescending(st => Progress.StageBalls(d, st, false)).ThenByDescending(st => st.id).Take(6);
                StageDef pick = null;
                foreach (var st in cand)
                    if (WinChance(st, team) >= 0.7) { pick = st; break; }
                if (pick != null)
                {
                    target = pick;
                    pw = WinChance(pick, team);
                    farm = true;
                }
            }
            if (target == null) break;
            Count(farm ? "trận đánh lại" : "trận ải mới");
            bool win = rng.Chance(pw);
            if (!win && !farm)
            {
                if (target.id == lossStage) lossStreak++;
                else { lossStage = target.id; lossStreak = 1; }
                Count("thua");
                var pops = Offers.On(s, d, new OfferCtx { e = OfferEvent.BattleLost, stage = target.id, freeFix = FreeFix(team) }, now, rng);
                HandlePopups(pops);
                Upgrade(); // gói Tiếp sức vừa mua (mảnh, bản sao): dùng ngay
                // từ lần thua 2 liền: nút quảng cáo Tiếp sức +15%
                if (lossStreak >= 2 && TryAd(AdGate.BattleRetry))
                {
                    Count("trận tiếp sức");
                    win = rng.Chance(WinChance(target, team, cfg.shop.retryBoost));
                }
            }
            if (!win) continue;
            if (target.id == lossStage) lossStreak = 0;
            Count("thắng");
            StageReward rw = null;
            var tg = target;
            Do(farm ? "ải (đánh lại)" : "ải (lần đầu)", () =>
            {
                rw = Progress.WinStage(s, d, tg.id, rng, now);
            });
            if (TryAd(AdGate.WinDouble))
                Do("qc:thưởng ải ×2", () =>
                {
                    s.balls += rw.balls;
                    foreach (var sh in rw.shards) Progress.AddShards(s, d, sh.hero, sh.n, rng);
                    s.evoStones += rw.evoStones;
                });
            HandlePopups(Offers.On(s, d, new OfferCtx { e = OfferEvent.BattleWon, stage = tg.id, boss = tg.kind == StageKind.Boss && rw.first }, now, rng));
        }
    }

    // ---------- máy bi ----------

    static readonly SlotKind[] Kinds = (SlotKind[])Enum.GetValues(typeof(SlotKind));
    double[] hitAcc;
    bool upgradeAsked;

    void OpenChest(SlotKind k, int x)
    {
        // nâng Rương Gỗ → Bạc bằng quảng cáo: một lần mỗi lần vào máy
        if (k == SlotKind.ChestWood && !upgradeAsked)
        {
            upgradeAsked = true;
            if (TryAd(AdGate.ChestUpgrade)) k = SlotKind.ChestSilver;
        }
        Pachinko.OpenChest(s, d, k, x, rng);
    }

    // thả hết bi; nhiều bi thì thả ở mức cược cao nhất đang mở (tốn x bi, thưởng × x: kỳ vọng như nhau). Trả số bi đã thả
    int DropAll()
    {
        if (hitAcc == null) hitAcc = new double[cfg.ringHits.Length];
        int dropped = 0, guard = 0;
        while (s.balls >= 1 && guard++ < 400000 && brokenDay < 0)
        {
            if (s.balls > BrokenAt) { brokenDay = dayIdx + 1; break; }
            int x = s.balls >= 1500 ? Progress.XBest(s, cfg, 10) : 1;
            if (s.balls > 200000) x = Math.Max(x, s.balls / 20000);
            var legend = Pachinko.SpendBall(s, d, x);
            Shop.PiggyAdd(s, cfg.shop, x);
            foreach (var g in Pachinko.GiftAdd(s, d, Pachinko.GiftCredit(s, cfg, x, legend)))
                if (g.k == RewardKind.Chest) OpenChest(g.chest, 1); // rương mốc quà, vòng nấm không nhân cược (như MachineScene)
            dropped += x;
            var k = rng.Weighted(Kinds, kk => cfg.Rate(Pachinko.Key(kk)));
            if (k == SlotKind.ChestGold) flags.Add("jackpot");
            if (Pachinko.SlotReward(s, cfg, k, x).k == RewardKind.Chest) OpenChest(k, x);
            for (int i = 0; i < hitAcc.Length; i++)
            {
                hitAcc[i] += cfg.ringHits[i];
                for (; hitAcc[i] >= 1; hitAcc[i]--)
                    foreach (var g in Pachinko.RingHit(s, cfg, i, x))
                        if (g.k == RewardKind.Chest) OpenChest(g.chest, 1); // rương mốc quà, vòng nấm không nhân cược (như MachineScene)
            }
        }
        return dropped;
    }

    void Machine()
    {
        MachineInner();
    }

    // vật phẩm x2 EXP: EXP của lần vào máy này nhân đôi (phần của tối đa x2Balls bi đầu)
    void MachineX2(double exp0, double dropped0)
    {
        double exp = ExpTotal() - exp0, dropped = (L.count.TryGetValue("bi đã thả", out var dr) ? dr : 0) - dropped0;
        if (exp <= 0 || dropped <= 0) return;
        double part = Math.Min(1, Rules.x2Balls / dropped);
        Do("iap:x2 EXP máy bi", () => Progress.AddExp(s, (int)Math.Round(exp * part), cfg));
        Count("lần dùng x2 EXP");
    }

    void MachineInner()
    {
        bool x2 = x2Pending;
        x2Pending = false;
        double exp0 = ExpTotal(), dropped0 = L.count.TryGetValue("bi đã thả", out var d0) ? d0 : 0;
        MachineCore();
        if (x2) MachineX2(exp0, dropped0);
    }

    void MachineCore()
    {
        upgradeAsked = false;
        if (s.balls < 1) { Count("vào máy không có bi"); }
        if (Tutorial.CoreDone(s) && s.balls > 0 && s.balls < 20)
            HandlePopups(Offers.On(s, d, new OfferCtx { e = OfferEvent.LowBalls }, now, rng));
        int total = 0, adsHere = 0;
        for (int round = 0; round < 8; round++)
        {
            int n = 0;
            Do("máy bi (trả lại)", () => n = DropAll(), () => -n);
            total += n;
            Ledger.Add(L.ballsOut, "máy bi (thả)", n);
            if (flags.Remove("jackpot")) HandlePopups(Offers.On(s, d, new OfferCtx { e = OfferEvent.Jackpot }, now, rng));
            if (!Tutorial.CoreDone(s)) break;
            // hết bi
            Count("hết bi");
            HandlePopups(Offers.On(s, d, new OfferCtx { e = OfferEvent.OutOfBalls }, now, rng));
            bool more = false;
            if (adsHere < 2 && TryAd(AdGate.FreeBalls))
            {
                adsHere++;
                Do("qc:bi miễn phí", () => s.balls += Shop.RoundBalls(cfg.shop.adBalls * cfg.shop.Band(s.level)));
                more = true;
            }
            else if (p.spend >= 2 && refillBuysToday < (p.spend == 3 ? 2 : 1) && rng.Chance(p.spend == 3 ? 0.8 : 0.25))
            {
                if (BuyPack(p.spend == 3 ? "refill_3" : "refill_2"))
                {
                    refillBuysToday++;
                    more = true;
                }
            }
            if (!more) break;
        }
        if (total > 0 && Casino.Open(s, d)) Casino.Track(s, d, "drop", total, now);
        Ledger.Add(L.count, "bi đã thả", total);
    }

    // ---------- nâng cấp ----------

    int sideEvo;

    void Upgrade()
    {
        foreach (var h in d.Heroes)
        {
            if (!s.Hero(h.id).owned) continue;
            foreach (var slot in Progress.Slots)
                while (Progress.UpCard(s, cfg, h.id, slot)) Count("nâng thẻ");
            while (Progress.StarUp(s, d, h.id)) Count("lên sao");
        }
        for (bool more = true; more;)
        {
            more = false;
            foreach (var h in d.Heroes.Where(x => s.Hero(x.id).owned).OrderByDescending(x => Strength(d, s, x)))
            {
                if (Progress.Evolve(s, d, h.id))
                {
                    Count("tiến hóa");
                    while (Progress.StarUp(s, d, h.id)) Count("lên sao");
                    more = true;
                    break;
                }
                if (Progress.NextStep(s, d, h.id) == Progress.StarStep.Evolve && s.level >= Progress.EvolveCost(s, d, h.id).level) break;
            }
        }
        SoPhep.AutoBuy(s, cfg);
    }

    // ---------- đảo Casino ----------

    int TableTier(CasinoTable t, int want)
    {
        int best = -1;
        for (int i = 0; i < t.bets.Length && i <= want; i++)
            if (Casino.BetOpen(s, t, i) && s.balls >= Casino.Bet(s, d, t, i) * 8) best = i;
        return best;
    }

    void CasinoVisit()
    {
        if (p.casino == 0 || !Casino.Open(s, d)) return;
        bool wild = p.casino == 2;
        Casino.Roll(s, d, now);
        if (!Casino.LuckyFlipped(s, now)) Casino.FlipLucky(s, now);
        Casino.InnToday(s, d, now);
        Count("lượt ra đảo");

        // câu cá: hết mồi miễn phí (và mồi nhiệm vụ)
        if (Casino.Unlocked(s, d, Casino.Fishing))
        {
            Do("đảo:câu cá", () =>
            {
                for (int guard = 0; guard < 40 && Fishing.BaitLeft(s, d, now) > 0; guard++)
                {
                    var bite = Fishing.Cast(s, d, rng.Int(0, Fishing.Spots(s, d) - 1), 1, now, rng, out var why);
                    if (bite == null) break;
                    Count("quăng câu");
                    if (rng.Chance(Math.Pow(0.93, Fishing.Ticks(bite)))) Fishing.Land(s, d, bite, now, rng);
                }
                Fishing.SellCreel(s, d);
            });
        }

        // đua: thận trọng cược mức có lợi (100), máu me cược tối đa
        if (Casino.Unlocked(s, d, Casino.Race))
        {
            var rc = Casino.C(d).race;
            while (Casino.PlaysLeft(s, d, Casino.Race, now) > 0)
            {
                int bet = wild ? rc.betMax : 100;
                while (bet > rc.betMin && s.balls < bet * (wild ? 1 : 3)) bet = rc.chips.Where(c => c < bet).DefaultIfEmpty(rc.betMin).Max();
                if (s.balls < bet) break;
                var lineup = Race.Lineup(d, rc, (uint)(rng.Next() * uint.MaxValue));
                var g = Race.Start(s, d, lineup, rng.Int(0, lineup.Count - 1), bet, now, rng, out var why);
                if (g == null) break;
                Race.Run(rc, g);
                int b0 = s.balls;
                Race.Finish(s, d, g, now);
                Ledger.Add(L.ballsOut, "đảo:đua (cược)", bet);
                Ledger.Add(L.ballsIn, "đảo:đua (trả)", s.balls - b0);
                Count("lượt đua");
            }
            int cup = Race.WeekCup(s, d);
            if (Race.WeekReady(s, d, cup, now)) Do("đảo:cúp đua tuần", () => Race.ClaimWeek(s, d, cup, now, rng));
        }

        // lều may rủi đang mở: thận trọng chơi 10 ván bậc thấp (đủ nhiệm vụ quán trọ), máu me chơi hết lượt ở bậc cao nhất
        Tables(wild);

        // chợ đen
        if (Casino.Unlocked(s, d, Casino.Market))
        {
            foreach (var sl in BlackMarket.Stock(s, d, now))
            {
                if (sl.bought) continue;
                string kind = sl.offer.kind;
                bool want;
                if (wild) want = (kind == "shards" || kind == "evo" || kind == "crystal" || kind == "mystery" || kind == "copies") && sl.price <= s.balls * 0.5;
                else
                    want = (kind == "shards" && sl.items.Count > 0 && s.team.Contains(sl.items[0].h) && sl.price <= s.balls * 0.25)
                           || (kind == "evo" && NeedEvo() && sl.price <= s.balls * 0.3);
                if (!want) continue;
                int idx = sl.idx;
                Do("đảo:chợ đen", () => BlackMarket.Buy(s, d, idx, now, rng, out var why));
                Count("mua chợ đen");
            }
            if (BlackMarket.SpareCopies(s, d) > 0) Do("đảo:đổi thẻ thừa", () => BlackMarket.SellSpare(s, d, now));
        }

        // hầm đấu: 5 trận / ngày, đánh các bậc cao nhất mà lực chiến đội mình đủ (thận trọng ≥ địch, máu me ≥ 80% địch)
        if (Casino.Unlocked(s, d, Casino.Underground))
        {
            var team = BestTeam(null);
            int mine = TeamPower.Of(cfg, d, Teams.Player(s, team, d));
            var tiers = Underground.TiersToday(d, now).Where(t => !Underground.WonToday(s, d, t, now))
                .Where(t => Underground.Power(d, Underground.Entry(d, t, now)) <= mine * (wild ? 1.25 : 1.0)).OrderByDescending(t => t).ToList();
            foreach (int tier in tiers)
            {
                if (Underground.FightsLeft(s, d, now) <= 0) break;
                int fee = Underground.Fee(s, d, tier);
                if (s.balls < fee) continue;
                var e = Underground.Entry(d, tier, now);
                if (!Underground.Pay(s, d, tier, now, out var why)) continue;
                Ledger.Add(L.ballsOut, "đảo:hầm đấu (lệ phí)", fee);
                var t0p = Teams.Player(s, team.Take(Underground.TeamLimit(e)).ToList(), d);
                t0p.ai = true;
                Underground.ApplyRule(d, e.rule, t0p, false);
                var bt = Battle.Create(d, t0p, Underground.Enemy(d, e), (uint)(rng.Next() * uint.MaxValue), s.level, s.level);
                BattleSim.Run(bt);
                bool won = bt.winner == 0 || rng.Chance(p.skill * 0.5);
                Count(won ? "hầm đấu thắng" : "hầm đấu thua");
                int t = tier;
                Do("đảo:hầm đấu (thưởng)", () => Underground.Finish(s, d, t, won, now, rng));
            }
        }

        // quán trọ
        if (Casino.Unlocked(s, d, Casino.Inn))
            Do("đảo:quán trọ", () =>
            {
                foreach (var q in Casino.InnToday(s, d, now))
                    if (Casino.QuestDone(s, q)) Casino.ClaimQuest(s, d, q.id, now, rng);
                if (Casino.InnAllReady(s, d, now)) Casino.ClaimInnAll(s, d, now, rng);
            });
    }

    bool NeedEvo() => d.Heroes.Any(h => s.Hero(h.id).owned && Progress.NextStep(s, d, h.id) == Progress.StarStep.Evolve
                                         && s.level >= Progress.EvolveCost(s, d, h.id).level && !Progress.CanEvolve(s, d, h.id));

    // một ván ở bàn: dòng cược / trả ghi riêng (gộp), quà hũ và mảnh ghi vào "đảo:hũ bàn"
    bool Round(string game, Func<bool> play)
    {
        var st = Casino.Of(s);
        double bet0 = st.betAll, won0 = st.wonAll;
        bool ok = false;
        Do("đảo:hũ bàn + mảnh khách mời", () => ok = play(), () => (st.wonAll - won0) - (st.betAll - bet0));
        if (!ok) return false;
        Ledger.Add(L.ballsOut, "đảo:" + game + " (cược)", st.betAll - bet0);
        Ledger.Add(L.ballsIn, "đảo:" + game + " (trả)", st.wonAll - won0);
        Count("ván " + game);
        return true;
    }

    void Tables(bool wild)
    {
        var cc = Casino.C(d);
        int want = wild ? 3 : 0;
        // thận trọng: 10 ván bậc thấp mỗi bàn (đủ nhiệm vụ quán trọ); máu me: hết lượt có thưởng ở bậc cao nhất đủ bi
        int Rounds(string g) => wild ? 999 : Math.Max(0, 10 - Casino.Roll(s, d, now).Play(g));
        if (Casino.BoothOpen(s, d, Casino.Blackjack, now))
            for (int i = Rounds(Casino.Blackjack); i > 0; i--)
            {
                var mode = Casino.ModeOf(s, d, Casino.Blackjack, now);
                if (mode == TableMode.Practice) break;
                int tier = mode == TableMode.Free ? 0 : TableTier(cc.blackjack, want);
                if (tier < 0) break;
                if (!Round("blackjack", () =>
                    {
                        var g = Blackjack.StartAs(s, d, tier, mode, now, rng, out var why);
                        if (g == null) return false;
                        int guard = 0;
                        while (g.phase == BjPhase.Player && guard++ < 30)
                        {
                            // thận trọng: chiến thuật cơ bản; máu me: rút tới 15 rồi dừng
                            var a = wild ? (g.Hand.Total < 15 ? BjAct.Hit : BjAct.Stand) : Blackjack.Advice(g);
                            if (!Blackjack.ActPaid(s, d, g, a, now))
                                Blackjack.ActPaid(s, d, g, g.Hand.Total < 17 && Blackjack.Can(g, BjAct.Hit) ? BjAct.Hit : BjAct.Stand, now);
                        }
                        Blackjack.Finish(s, d, g, tier, now, rng);
                        return true;
                    })) break;
            }
        if (Casino.BoothOpen(s, d, Casino.Roulette, now))
            for (int i = Rounds(Casino.Roulette); i > 0; i--)
            {
                var mode = Casino.ModeOf(s, d, Casino.Roulette, now);
                if (mode == TableMode.Practice) break;
                int tier = mode == TableMode.Free ? 0 : TableTier(cc.roulette, want);
                if (tier < 0) break;
                var bets = new List<RlBet> { new RlBet { kind = RlKind.Elem, v = rng.Int(0, 4) } };
                if (wild)
                {
                    bets.Add(new RlBet { kind = RlKind.Num, v = rng.Int(1, 5) });
                    bets.Add(new RlBet { kind = RlKind.Single, v = rng.Int(0, 24) });
                    bets.Add(new RlBet { kind = RlKind.Star });
                }
                if (mode == TableMode.Paid && s.balls < bets.Count * Casino.Bet(s, d, cc.roulette, tier)) break;
                if (!Round("roulette", () => Roulette.PlayAs(s, d, bets, tier, mode, now, rng, out var jar, out var extra, out var why) != null)) break;
            }
        if (Casino.BoothOpen(s, d, Casino.Slot, now))
            for (int i = Rounds(Casino.Slot); i > 0; i--)
            {
                var mode = Casino.ModeOf(s, d, Casino.Slot, now);
                if (mode == TableMode.Practice) break;
                int tier = mode == TableMode.Free ? 0 : TableTier(cc.slots, want);
                if (tier < 0) break;
                if (!Round("slot", () => Slots.PlayAs(s, d, tier, mode, now, rng, out var jar, out var extra, out var why) != null)) break;
            }
    }

    // ---------- phiên, ngày ----------

    void Session()
    {
        var sw0 = System.Diagnostics.Stopwatch.StartNew();
        HandlePopups(Offers.Open(s, d, now, rng));
        ClaimFree();
        if (sessionOfDay == 0) Shopping();
        Prof("open+shop", sw0);

        // cây bi, AFK, rương AFK
        int ripe = Trees.Stock(s, cfg, now);
        bool x2 = ripe > 0 && TryAd(AdGate.TreeDouble);
        Do("cây bi", () => Trees.Harvest(s, cfg, now, 1));
        if (x2) Do("qc:cây bi ×2", () => s.balls += ripe);
        Do("AFK (mảnh)", () => Afk.Claim(s, d, now, 1, rng));
        var afkAt = AfkTarget();
        if (afkAt == null)
        {
            int keep = s.afk.stage;
            s.afk.stage = 0;
            afkAt = Afk.Stage(s, d);
            s.afk.stage = keep;
        }
        if (afkAt != null && afkAt.id != s.afk.stage) Do("AFK (mảnh)", () => Afk.SetStage(s, d, afkAt.id, now, rng));
        Do("AFK (rương)", () => { while (Afk.OpenChest(s, d, now, rng) != null) Count("rương AFK"); });
        while (s.afk.chests.Count > 0 && TryAd(AdGate.AfkChestOpen))
            Do("qc:mở ngay rương AFK", () => { if (Afk.OpenChest(s, d, now, rng, true) != null) Count("rương AFK"); });

        Prof("afk+tree", sw0);
        // ruộng vườn của Nhà (mô hình trang trại cũ, gần đúng như ProgressSim)
        if (Home.Open(s, cfg))
            Do("Nhà (ruộng)", () =>
            {
                Farm.Harvest(s, d, now);
                var f = Farm.Of(s, cfg, now);
                for (int i = 0; i < f.spots.Count; i++)
                    if (f.spots[i].hero != null && f.spots[i].energy <= 0) Farm.Remove(s, d, now, i);
                Farm.Auto(s, d, now);
            });

        var sw = System.Diagnostics.Stopwatch.StartNew();
        Battles();
        Prof("battles", sw);
        CasinoVisit();
        Prof("casino", sw);
        Machine();
        Prof("machine", sw);

        foreach (var z in Elements.All)
            Do("rương mốc đảo", () => { while (Progress.ClaimZoneChest(s, d, z, rng) != null) { } });
        int side = ProgressSim.SideEvo(s.level) - sideEvo;
        if (side > 0)
        {
            s.evoStones += side;
            sideEvo += side;
            Ledger.Add(L.evo, "Đền + Hang (gần đúng)", side);
        }
        // trứng miễn phí bằng quảng cáo
        if (TryAd(AdGate.FreeEgg)) Do("qc:trứng miễn phí", () => Eggs.Open(s, d, 0, 1, false, now, rng));
        ClaimFree(); // mốc quảng cáo vừa đạt
        if (flags.Remove("legend_hatch")) HandlePopups(Offers.On(s, d, new OfferCtx { e = OfferEvent.LegendChest }, now, rng));
        Upgrade();
        if (NeedEvo()) Count("phiên kẹt đá tiến hóa");
        if (!Afk.Boosting(s, now) && !Afk.Pending(s, cfg, now).full && TryAd(AdGate.AfkBoost)) Afk.Boost(s, cfg, now);
        Prof("rest", sw);
        if (!Tutorial.CoreDone(s)) Tutorial.Skip(s); // hết phiên đầu: coi như xong chuỗi hướng dẫn bắt buộc
        Count("phiên");
    }

    public static readonly SortedDictionary<string, double> ProfT = new SortedDictionary<string, double>();
    static void Prof(string k, System.Diagnostics.Stopwatch sw)
    {
        ProfT[k] = (ProfT.TryGetValue(k, out var x) ? x : 0) + sw.Elapsed.TotalSeconds;
        sw.Restart();
    }

    void Mark(int day)
    {
        level[day] = s.level;
        cleared[day] = Progress.TotalCleared(s);
        zonesDone[day] = Progress.ZonesDone(s);
        owned[day] = s.heroes.Count(kv => kv.Value.owned);
        stars[day] = s.heroes.Where(kv => kv.Value.owned).Sum(kv => kv.Value.star);
        ballsHeld[day] = s.balls;
        var team = s.team.Where(h => s.Hero(h)?.owned == true).ToList();
        power[day] = team.Count > 0 ? TeamPower.Of(cfg, d, Teams.Player(s, team, d)) : 0;
        usdCum[day] = usdTotal;
        adsCum[day] = (int)L.ads.Where(kv => !kv.Key.EndsWith(")")).Sum(kv => kv.Value);
        sessionsCum[day] = (int)(L.count.TryGetValue("phiên", out var n) ? n : 0);
        droppedCum[day] = L.count.TryGetValue("bi đã thả", out var dr) ? dr : 0;
        ballsInCum[day] = L.ballsIn.Where(kv => !kv.Key.StartsWith("máy bi") && !kv.Key.Contains("(trả)")).Sum(kv => kv.Value);
        shardsCum[day] = L.shards.Sum(kv => kv.Value);
        if (Array.IndexOf(SnapDays, day) >= 0)
        {
            SortedDictionary<string, double> C(SortedDictionary<string, double> m) => new SortedDictionary<string, double>(m);
            snaps[day] = new Dictionary<string, SortedDictionary<string, double>>
            {
                ["ballsIn"] = C(L.ballsIn), ["ballsOut"] = C(L.ballsOut), ["shards"] = C(L.shards), ["evo"] = C(L.evo), ["usd"] = C(L.usd), ["ads"] = C(L.ads), ["count"] = C(L.count),
            };
        }
        if (finishedDay < 0 && Progress.ZonesDone(s) >= 5) finishedDay = day;
        if (maxLevelDay < 0 && s.level >= cfg.maxLevel) maxLevelDay = day;
    }

    public void Run()
    {
        Mark(0);
        for (int day = 0; day < days; day++)
        {
            dayIdx = day;
            adsToday = 0;
            refillBuysToday = 0;
            int before = Progress.TotalCleared(s);
            Grants();
            if (day == 0 || rng.Chance(p.dayProb))
            {
                for (int k = 0; k < p.sessions && brokenDay < 0; k++)
                {
                    sessionOfDay = k;
                    now = t0 + (day * 24 + 8 + 15.0 * (k + 0.5) / p.sessions) * H;
                    Session();
                }
                if (Progress.TotalCleared(s) == before && Progress.ZonesDone(s) < 5) Count("ngày không qua ải mới");
            }
            else Count("ngày nghỉ");
            Mark(day + 1);
            if (System.Diagnostics.Process.GetCurrentProcess().TotalProcessorTime.TotalSeconds - cpu0 > WallLimit) timedOut = true;
            if (brokenDay >= 0 || timedOut)
            {
                // kinh tế đã vỡ (hoặc quá giờ): dừng người này, các ngày sau giữ số của ngày dừng
                stoppedDay = day + 1;
                for (int k = day + 2; k <= days; k++)
                {
                    level[k] = level[day + 1]; cleared[k] = cleared[day + 1]; zonesDone[k] = zonesDone[day + 1]; owned[k] = owned[day + 1]; stars[k] = stars[day + 1];
                    ballsHeld[k] = ballsHeld[day + 1]; power[k] = power[day + 1]; adsCum[k] = adsCum[day + 1]; sessionsCum[k] = sessionsCum[day + 1];
                    usdCum[k] = usdCum[day + 1]; droppedCum[k] = droppedCum[day + 1]; ballsInCum[k] = ballsInCum[day + 1]; shardsCum[k] = shardsCum[day + 1];
                }
                break;
            }
        }
    }
}
