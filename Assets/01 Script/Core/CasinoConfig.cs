// Cấu hình đảo Casino (GD_Claude/29_DaoCasino.md, 2026-11-25): khối "casino" trong balance.json. Lớp [Serializable], chỉ List và mảng
// phẳng để Unity lưu được trong BalanceConfigAsset (như HomeConfig, ShopConfig). Số là số đầu, đo lại bằng ProgressSim.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    // một món thưởng của đảo: như ShopItem (k, n, h, r) cộng tỉ lệ ra (chance < 1: có lúc ra). Thêm k riêng của đảo: "bait" (mồi câu).
    // h đặc biệt: "*guest" (tướng khách mời của sự kiện đang mở), "*elem:<hệ>" (tướng ngẫu nhiên của hệ), các "*…" khác như cửa hàng.
    [Serializable]
    public class CasinoItem
    {
        public string k;
        public int n = 1;
        public string h;
        public int r = -1;
        public double chance = 1;

        public ShopItem ToShop() => new ShopItem { k = k, n = n, h = h, r = r };
    }

    [Serializable]
    public class CasinoItems
    {
        public List<CasinoItem> items = new List<CasinoItem>();
    }

    // trò mở theo cấp người chơi (và số tướng đang có)
    [Serializable]
    public class CasinoUnlock
    {
        public string id; // fishing, inn, race, booths, market, underground
        public int level;
        public int heroes;
    }

    // sự kiện: lều (booth) mở theo vòng lặp tính từ ngày mốc (anchor), hoặc theo ngày cố định start..end (yyyy-MM-dd, gồm cả hai đầu)
    [Serializable]
    public class CasinoEvent
    {
        public string id, name;
        public string Name => Loc.T(name);
        public string booth; // blackjack, roulette, slot, race_fest
        public int period, offset, length; // vòng lặp (ngày): mở khi (ngày − mốc − offset) mod period < length
        public string start, end; // ngày cố định (ưu tiên hơn vòng lặp nếu có)
        public string guest; // tướng khách mời cố định; rỗng: chọn theo lần mở
        public double mult = 1; // hệ số thưởng (Lễ Hội Đua)
    }

    // bàn may rủi: bậc cược (bi gốc, nhân bậc cấp), cấp mở từng bậc, trần ván mỗi ngày, Hũ bàn
    [Serializable]
    public class CasinoTable
    {
        public int[] bets = new int[0];
        public int[] betLevel = new int[0];
        public int daily;
        public int jarBets = 30; // sức chứa hũ = jarBets × cược gốc của bậc cao nhất đã dùng
        public List<CasinoItems> jar = new List<CasinoItems>(); // rương hũ theo bậc cao nhất đã dùng
    }

    [Serializable]
    public class BlackjackConfig : CasinoTable
    {
        public double bjPays = 1.5;
    }

    [Serializable]
    public class RouletteConfig : CasinoTable
    {
        public int chips = 5; // số chip tối đa mỗi vòng
        public int elemPays = 4, numPays = 4, singlePays = 24, starPays = 24;
        public int starTier = 2; // ô Sao Vàng cho thêm mảnh khách mời khi cược từ bậc này (0-based) trở lên
        public int starShards = 2;
        // trọng số ra của 26 ô (ô i = hệ i / 5, số i % 5 + 1; ô 25 Sao Vàng). Rỗng = 26 ô đều nhau (1/26). Đây là chỗ CHỈNH TỈ LỆ RA:
        // viên bi trên màn chỉ diễn theo ô lõi đã chọn (Core/Casino/RouletteBall.cs). Hoàn trả hiện trong Cách chơi tính theo đây.
        public int[] weights = new int[0];
    }

    // một kiểu thắng trên đường của máy quả: ba biểu tượng sym (Sao thay được), trả pays × cược mỗi đường
    [Serializable]
    public class SlotPay
    {
        public int sym;
        public int pays;
    }

    [Serializable]
    public class SlotReel
    {
        public int[] strip = new int[0];
    }

    [Serializable]
    public class SlotsConfig : CasinoTable
    {
        public List<SlotReel> reels = new List<SlotReel>(); // 3 cuộn; biểu tượng: 0..4 ngọc hệ (thứ tự Elem), 5 bi, 6 huy hiệu, 7 Sao, 8 Rương
        public List<SlotPay> pays = new List<SlotPay>();
        public int wildPays; // ba Sao trên một đường
        public int scatter2; // hai Rương ở đâu cũng được: × tổng cược
        public int freeSpins = 5; // ba Rương: lượt miễn phí
        public int[] badgeShards = new int[0]; // ba huy hiệu trên một đường: mảnh khách mời theo bậc cược
    }

    [Serializable]
    public class RaceCup
    {
        public string name;
        public string Name => Loc.T(name);
        public int level; // cấp người chơi để mở hạng
        public int oppLevel, oppStar; // tướng máy
        public int fee; // lệ phí gốc (nhân bậc cấp)
        public double skill; // độ giỏi cổ vũ của tướng máy (0..1)
        public List<CasinoItem> week = new List<CasinoItem>(); // quà tuần khi đủ điểm
    }

    [Serializable]
    public class RaceConfig
    {
        // luật cược (người dùng 2026-11-26): đặt 1 trong runners con, betMin..betMax bi, daily lần mỗi ngày; hạng của con được chọn rút
        // theo bảng tỉ lệ nội suy giữa oddsLow (cược thấp nhất) và oddsHigh (cược cao nhất), cược càng cao càng khó thắng
        public double seg = 60; // độ dài mỗi chặng
        public int segs = 3;
        public int daily = 5; // số lần đặt cược mỗi ngày
        public int runners = 5; // số tướng mỗi cuộc đua
        public int betMin = 10, betMax = 500;
        public int[] chips = { 50, 100, 200, 500 }; // các mức cược bấm nhanh
        public double[] pay = { 3, 2, 1, 0, 0 }; // bi nhận về = cược × pay[hạng] (nhất ×3, nhì ×2, ba hoà, còn lại mất)
        public double[] oddsLow = { 0.18, 0.20, 0.24 }, oddsHigh = { 0.09, 0.13, 0.24 }; // tỉ lệ về nhất / nhì / ba
        // kịch bản cuộc đua (Race.Script)
        public double raceSec = 20; // con về nhất chạy hết đường trong bấy nhiêu giây
        public double gapMin = 0.12, gapMax = 0.5; // hai hạng liền nhau về cách nhau (giây)
        public double spread = 4.5; // lệch tối đa so với nhịp chung giữa cuộc đua (đơn vị đường)
        public double keyMin = 1.3, keyMax = 2.3; // khoảng cách giữa hai mốc đổi nhịp (giây)
        public double startSec = 0.8, endSec = 2.6; // đầu cuộc đua chạy chụm; mốc kịch tính cách đích bấy nhiêu giây
        public double surge = 3.2, surgeSec = 0.9; // vọt lên ≥ surge đơn vị giữa hai mốc: bứt tốc dồn trong surgeSec giây
        public double stunDrop = 3.6, stunMax = 1.2; // tụt ≥ stunDrop: bị húc choáng, đứng yên tối đa stunMax giây
        public double comeback = 0.55, tease = 0.6; // con về nhất còn ở sau trước nước rút; con mình chọn (sẽ thua) đang dẫn trước nước rút
        public int[] points = { 3, 2, 1, 0, 0 };
        public int weekPts = 10;
        public List<RaceCup> cups = new List<RaceCup>();
    }

    [Serializable]
    public class FishDef
    {
        public string id, name;
        public string Name => Loc.T(name);
        public Elem elem;
        public Rarity rar;
        public bool night; // chỉ cắn ban đêm (19 giờ – 5 giờ)
        public double min, max; // cỡ (cm)
    }

    [Serializable]
    public class FishRod
    {
        public int cost; // bi để lên cấp này
        public double zone; // phần thanh của vùng xanh
        public int spots; // số chỗ câu mở
    }

    [Serializable]
    public class FishSpot
    {
        public string name;
        public string Name => Loc.T(name);
        public double[] rar = new double[5]; // trọng số độ hiếm
    }

    [Serializable]
    public class FishingConfig
    {
        public int freeBait = 10, baitPack = 5, baitPrice = 30;
        public double farBonus = 1; // quăng xa nhất: trọng số độ hiếm k nhân (1 + farBonus × lực × k / 4)
        public double biteWindow = 0.6;
        public double[] pull = { 1, 1.5, 2.2, 3, 4 }; // độ vùng vẫy theo độ hiếm (giao diện dùng)
        public int[] first = { 10, 15, 25, 50, 100 }; // bi khi bắt lần đầu một loài
        public int[] price = { 3, 6, 12, 30, 80 }; // giá bán gốc theo độ hiếm (× cỡ 0,8–1,5)
        public int setShards = 5; // đủ 6 loài một hệ
        public double kingChance = 0.15, kingAssist = 0.25; // gặp Cá Vua mỗi lần quăng ở chỗ cuối; tướng khắc hệ cá: vùng xanh +25%
        public int kingRod = 3; // cấp cần câu để gặp Cá Vua
        public List<FishRod> rods = new List<FishRod>();
        public List<FishSpot> spots = new List<FishSpot>();
        public List<FishDef> fish = new List<FishDef>();
        public List<FishDef> kings = new List<FishDef>(); // mỗi tuần một con, theo thứ tự
        public List<CasinoItem> king = new List<CasinoItem>(); // thưởng Cá Vua
        public FishDef Fish(string id) => fish.Find(f => f.id == id) ?? kings.Find(f => f.id == id);
    }

    // một mẫu hàng của chợ đen
    [Serializable]
    public class MarketOffer
    {
        public string kind; // shards, evo, crystal, stones, copies, bait, mystery
        public int n = 1;
        public double w = 1;
        public double mark = 1.5; // giá = giá gốc × mark (bi)
        public int price; // giá cố định (bait, mystery)
        public bool night; // chỉ ban đêm
        public Rarity rar = Rarity.Rare; // shards: độ hiếm tối thiểu của tướng
        public string[] defs = new string[0]; // home: trang trí Nhà có thể bày (mã công trình kind deco); cần đã mở Nhà
    }

    [Serializable]
    public class MarketConfig
    {
        public int slots = 6, nightSlots = 2;
        public int[] periods = { 0, 8, 16 }; // giờ đổi hàng
        public int[] refresh = { 20, 40, 80, 120, 160 }; // giá làm mới sớm, hết mảng thì hết lượt
        public int copySell = 6; // bi mỗi bản sao thừa (thẻ đã tối đa cấp)
        public List<MarketOffer> offers = new List<MarketOffer>();
        public List<ChestRoll> mystery = new List<ChestRoll>(); // Túi hàng lậu (công bố tỉ lệ)
    }

    [Serializable]
    public class UgMember
    {
        public string hero;
        public int level, star = 1, card = 1;
    }

    // luật ngày: atk / hp / def (cộng phần trăm p cho tướng hệ elem, rỗng: mọi tướng, cả hai bên); picks (số lần chọn mỗi lượt của
    // người chơi = n); solo (mỗi bên 1 tướng); buff (đội địch mạnh thêm p)
    [Serializable]
    public class UgRule
    {
        public string kind;
        public string elem;
        public double p;
        public int n;
    }

    [Serializable]
    public class UgEntry
    {
        public string name;
        public string Name => Loc.T(name);
        public UgRule rule = new UgRule();
        public List<UgMember> team = new List<UgMember>();
        public string lead; // tướng chủ lực (mảnh thưởng); rỗng: tướng đầu đội
    }

    [Serializable]
    public class UgDay
    {
        public string date; // ghi đè ngày cố định (yyyy-MM-dd); rỗng: ngày trong vòng lặp
        public List<UgEntry> entries = new List<UgEntry>(); // theo bậc
    }

    [Serializable]
    public class UgTier
    {
        public string name;
        public string Name => Loc.T(name);
        public int level; // cấp đội mẫu khi cân (runner ugcal); không còn khoá bậc theo cấp người chơi (người dùng 2026-11-26)
        public int fee;
        public int shards; // mảnh tướng chủ lực khi thắng lần đầu trong ngày
        public List<CasinoItem> items = new List<CasinoItem>();
        public bool weekly; // Nhà Vô Địch: một lần mỗi tuần, chỉ chủ nhật
    }

    [Serializable]
    public class UndergroundConfig
    {
        public double winMult = 2.5, rewinMult = 1; // bi thắng lần đầu / thắng lại × lệ phí
        public int daily = 5; // số trận Hầm đấu mỗi ngày (thắng, thua, đánh lại đều tính; người dùng 2026-11-26)
        public List<CasinoItem> rewin = new List<CasinoItem>();
        public List<UgTier> tiers = new List<UgTier>(); // tier cuối có weekly = true là Nhà Vô Địch
        public List<UgDay> rotation = new List<UgDay>(); // vòng lặp ngày
        public List<UgDay> dates = new List<UgDay>(); // ghi đè
    }

    [Serializable]
    public class InnQuest
    {
        public string id, kind; // kind: fish, fish_rare, race, race_top3, table, ug_win, market_buy, drop
        public string text; // chữ, {0} = n
        public string Text => Loc.F(text, n);
        public int n;
        public string need; // trò cần mở (fishing, race, booths, market, underground); rỗng: luôn có
        public List<CasinoItem> items = new List<CasinoItem>();
    }

    [Serializable]
    public class InnConfig
    {
        public int count = 3;
        public List<InnQuest> quests = new List<InnQuest>();
        public List<CasinoItem> all = new List<CasinoItem>(); // xong cả 3
    }

    [Serializable]
    public class CasinoConfig
    {
        public int openLevel = 8;
        public string anchor = "2026-11-23"; // ngày mốc của vòng sự kiện và vòng đội ngầm (thứ Hai)
        // vùng (mã nước 2 chữ) tắt ba lều may rủi (mục 8: nước coi hộp may rủi trả tiền là cờ bạc); Remote Config sau này đè
        public string[] tablesBlock = { "BE" };
        public List<CasinoUnlock> unlocks = new List<CasinoUnlock>();
        public List<CasinoEvent> events = new List<CasinoEvent>();
        public BlackjackConfig blackjack = new BlackjackConfig();
        public RouletteConfig roulette = new RouletteConfig();
        public SlotsConfig slots = new SlotsConfig();
        public RaceConfig race = new RaceConfig();
        public FishingConfig fishing = new FishingConfig();
        public MarketConfig market = new MarketConfig();
        public UndergroundConfig underground = new UndergroundConfig();
        public InnConfig inn = new InnConfig();

        public CasinoUnlock Unlock(string id) => unlocks.Find(u => u.id == id);

        public CasinoTable Table(string id) => id == "blackjack" ? blackjack : id == "roulette" ? roulette : id == "slot" ? (CasinoTable)slots : null;

        // ---------- kiểm ----------

        public List<string> Validate(GameData d)
        {
            var err = new List<string>();
            if (unlocks.Count == 0) return err; // chưa có khối casino: bỏ qua
            foreach (var id in new[] { "fishing", "inn", "race", "booths", "market", "underground" })
                if (Unlock(id) == null) err.Add($"casino.unlocks: thiếu {id}");
            if (Days(anchor) < 0) err.Add($"casino.anchor: ngày sai \"{anchor}\"");
            foreach (var e in events)
            {
                if (Table(e.booth) == null && e.booth != "race_fest") err.Add($"casino.events.{e.id}: lều lạ \"{e.booth}\"");
                bool fixedDate = !string.IsNullOrEmpty(e.start);
                if (fixedDate && (Days(e.start) < 0 || Days(e.end) < Days(e.start))) err.Add($"casino.events.{e.id}: ngày sai");
                if (!fixedDate && (e.period <= 0 || e.length <= 0 || e.length > e.period)) err.Add($"casino.events.{e.id}: vòng lặp sai");
                if (!string.IsNullOrEmpty(e.guest) && d?.Hero(e.guest) == null) err.Add($"casino.events.{e.id}: không có tướng {e.guest}");
            }
            foreach (var (name, t) in new (string, CasinoTable)[] { ("blackjack", blackjack), ("roulette", roulette), ("slots", slots) })
            {
                if (t.bets.Length == 0 || t.bets.Length != t.betLevel.Length) err.Add($"casino.{name}: bets / betLevel lệch");
                if (t.jar.Count != t.bets.Length) err.Add($"casino.{name}: jar phải có {t.bets.Length} bậc");
                if (t.daily <= 0) err.Add($"casino.{name}: daily phải > 0");
            }
            if (roulette.weights.Length != 0 && (roulette.weights.Length != 26 || roulette.weights.Any(w => w < 0) || roulette.weights.Sum() <= 0))
                err.Add("casino.roulette.weights: cần đúng 26 số không âm, tổng > 0 (hoặc bỏ trống)");
            if (slots.reels.Count != 3 || slots.reels.Any(r => r.strip.Length < 3)) err.Add("casino.slots: cần 3 cuộn, mỗi cuộn ≥ 3 ô");
            if (slots.reels.Any(r => r.strip.Any(x => x < 0 || x > 8))) err.Add("casino.slots: biểu tượng 0..8");
            if (race.cups.Count == 0) err.Add("casino.race.cups: rỗng");
            if (race.runners < 2 || race.runners > 5) err.Add("casino.race: runners phải 2..5 (màn dựng sẵn 5 làn)");
            if (race.pay.Length < race.runners || race.points.Length < race.runners) err.Add("casino.race: pay / points thiếu hạng");
            if (race.betMin <= 0 || race.betMax < race.betMin || race.daily <= 0) err.Add("casino.race: betMin / betMax / daily sai");
            if (race.oddsLow.Length != race.oddsHigh.Length || race.oddsLow.Sum() > 1 || race.oddsHigh.Sum() > 1) err.Add("casino.race: oddsLow / oddsHigh sai");
            if (race.raceSec <= race.endSec + race.startSec + race.keyMax || race.gapMin < 0 || race.gapMax < race.gapMin) err.Add("casino.race: raceSec / gap sai");
            if (fishing.rods.Count == 0 || fishing.spots.Count == 0) err.Add("casino.fishing: thiếu rods / spots");
            foreach (var e in Elements.All)
                if (fishing.fish.Count(f => f.elem == e) != 6) err.Add($"casino.fishing: hệ {Keys.Of(e)} phải có 6 loài");
            foreach (var f in fishing.fish.Concat(fishing.kings))
                if (f.min <= 0 || f.max < f.min) err.Add($"casino.fishing.{f.id}: cỡ sai");
            if (fishing.fish.Select(f => f.id).Distinct().Count() != fishing.fish.Count) err.Add("casino.fishing: trùng id cá");
            if (market.offers.Count == 0) err.Add("casino.market.offers: rỗng");
            foreach (var o in market.offers.Where(o => o.kind == "home"))
                foreach (var id in o.defs)
                    if (d.Cfg.home.Def(id) == null || !Home.IsDeco(d.Cfg.home.Def(id))) err.Add($"casino.market: '{id}' không phải trang trí Nhà");
            if (underground.rotation.Count == 0) err.Add("casino.underground.rotation: rỗng");
            int normal = underground.tiers.Count(t => !t.weekly);
            foreach (var day in underground.rotation.Concat(underground.dates))
            {
                string tag = string.IsNullOrEmpty(day.date) ? $"rotation[{underground.rotation.IndexOf(day)}]" : day.date;
                if (day.entries.Count < normal) err.Add($"casino.underground.{tag}: cần {normal} đội");
                foreach (var en in day.entries)
                {
                    if (en.team.Count == 0 || en.team.Count > 3) err.Add($"casino.underground.{tag}.{en.name}: đội 1–3 tướng");
                    foreach (var m in en.team)
                        if (d?.Hero(m.hero) == null) err.Add($"casino.underground.{tag}.{en.name}: không có tướng {m.hero}");
                    if (!string.IsNullOrEmpty(en.lead) && en.team.All(m => m.hero != en.lead)) err.Add($"casino.underground.{tag}.{en.name}: lead không trong đội");
                    var k = en.rule?.kind;
                    if (!string.IsNullOrEmpty(k) && !new[] { "atk", "hp", "def", "picks", "solo", "buff" }.Contains(k))
                        err.Add($"casino.underground.{tag}.{en.name}: luật lạ {k}");
                }
            }
            if (inn.quests.Count < inn.count) err.Add("casino.inn: ít nhiệm vụ hơn count");
            return err;
        }

        // số ngày từ 1/1/1970 của "yyyy-MM-dd" (−1 nếu sai)
        public static int Days(string ymd)
        {
            if (string.IsNullOrEmpty(ymd)) return -1;
            if (!DateTime.TryParseExact(ymd, "yyyy-MM-dd", System.Globalization.CultureInfo.InvariantCulture,
                    System.Globalization.DateTimeStyles.None, out var t)) return -1;
            return (int)(t - new DateTime(1970, 1, 1)).TotalDays;
        }

        // ---------- đọc balance.json ----------

        static List<CasinoItem> Items(object arr)
        {
            var list = new List<CasinoItem>();
            foreach (var x in J.Arr(arr))
            {
                var o = J.Obj(x);
                if (o == null) continue;
                list.Add(new CasinoItem { k = J.Str(o, "k"), n = J.Int(o, "n", 1), h = J.Str(o, "h"), r = J.Int(o, "r", -1), chance = J.Num(o, "chance", 1) });
            }
            return list;
        }

        static int[] Ints(object arr) => J.Arr(arr).Select(x => x is double v ? (int)v : 0).ToArray();
        static double[] Nums(object arr) => J.Arr(arr).Select(x => x is double v ? v : 0).ToArray();

        static void ReadTable(CasinoTable t, Dictionary<string, object> o)
        {
            if (o == null) return;
            t.bets = Ints(J.Get(o, "bets"));
            t.betLevel = Ints(J.Get(o, "betLevel"));
            t.daily = J.Int(o, "daily");
            t.jarBets = J.Int(o, "jarBets", t.jarBets);
            foreach (var x in J.Arr(o, "jar")) t.jar.Add(new CasinoItems { items = Items(x) });
        }

        static UgDay Day(Dictionary<string, object> o)
        {
            var day = new UgDay { date = J.Str(o, "date") };
            foreach (var x in J.Arr(o, "entries"))
            {
                var eo = J.Obj(x);
                var ro = J.Obj(eo, "rule");
                var en = new UgEntry
                {
                    name = J.Str(eo, "name"), lead = J.Str(eo, "lead"),
                    rule = ro == null ? new UgRule() : new UgRule { kind = J.Str(ro, "kind"), elem = J.Str(ro, "elem"), p = J.Num(ro, "p"), n = J.Int(ro, "n") },
                };
                foreach (var m in J.Arr(eo, "team"))
                {
                    var mo = J.Obj(m);
                    en.team.Add(new UgMember { hero = J.Str(mo, "hero"), level = J.Int(mo, "level", 1), star = J.Int(mo, "star", 1), card = J.Int(mo, "card", 1) });
                }
                day.entries.Add(en);
            }
            return day;
        }

        static FishDef Fish(object x)
        {
            var o = J.Obj(x);
            return new FishDef
            {
                id = J.Str(o, "id"), name = J.Str(o, "name"), elem = Keys.ToElem(J.Str(o, "elem")), rar = Keys.ToRarity(J.Str(o, "rar", "common")),
                night = J.Bool(o, "night"), min = J.Num(o, "min"), max = J.Num(o, "max"),
            };
        }

        public static CasinoConfig Parse(Dictionary<string, object> o, Func<List<object>, List<ChestRoll>> rolls)
        {
            var c = new CasinoConfig();
            if (o == null) return c;
            c.openLevel = J.Int(o, "openLevel", c.openLevel);
            c.anchor = J.Str(o, "anchor", c.anchor);
            if (o.ContainsKey("tablesBlock"))
                c.tablesBlock = J.Arr(o, "tablesBlock").OfType<string>().Select(x => x.Trim().ToUpperInvariant()).Where(x => x.Length > 0).ToArray();
            foreach (var x in J.Arr(o, "unlocks"))
            {
                var u = J.Obj(x);
                c.unlocks.Add(new CasinoUnlock { id = J.Str(u, "id"), level = J.Int(u, "level"), heroes = J.Int(u, "heroes") });
            }
            foreach (var x in J.Arr(o, "events"))
            {
                var e = J.Obj(x);
                c.events.Add(new CasinoEvent
                {
                    id = J.Str(e, "id"), name = J.Str(e, "name"), booth = J.Str(e, "booth"),
                    period = J.Int(e, "period"), offset = J.Int(e, "offset"), length = J.Int(e, "length"),
                    start = J.Str(e, "start"), end = J.Str(e, "end"), guest = J.Str(e, "guest"), mult = J.Num(e, "mult", 1),
                });
            }

            var bj = J.Obj(o, "blackjack");
            ReadTable(c.blackjack, bj);
            if (bj != null) c.blackjack.bjPays = J.Num(bj, "bjPays", 1.5);

            var ro = J.Obj(o, "roulette");
            ReadTable(c.roulette, ro);
            if (ro != null)
            {
                var r = c.roulette;
                r.chips = J.Int(ro, "chips", r.chips);
                r.elemPays = J.Int(ro, "elemPays", r.elemPays);
                r.numPays = J.Int(ro, "numPays", r.numPays);
                r.singlePays = J.Int(ro, "singlePays", r.singlePays);
                r.starPays = J.Int(ro, "starPays", r.starPays);
                r.starTier = J.Int(ro, "starTier", r.starTier);
                r.starShards = J.Int(ro, "starShards", r.starShards);
                if (ro.ContainsKey("weights")) r.weights = Ints(ro["weights"]);
            }

            var so = J.Obj(o, "slots");
            ReadTable(c.slots, so);
            if (so != null)
            {
                var s = c.slots;
                foreach (var x in J.Arr(so, "reels")) s.reels.Add(new SlotReel { strip = Ints(x) });
                foreach (var x in J.Arr(so, "pays"))
                {
                    var p = J.Obj(x);
                    s.pays.Add(new SlotPay { sym = J.Int(p, "sym"), pays = J.Int(p, "pays") });
                }
                s.wildPays = J.Int(so, "wildPays");
                s.scatter2 = J.Int(so, "scatter2");
                s.freeSpins = J.Int(so, "freeSpins", s.freeSpins);
                s.badgeShards = Ints(J.Get(so, "badgeShards"));
            }

            var rc = J.Obj(o, "race");
            if (rc != null)
            {
                var r = c.race;
                r.seg = J.Num(rc, "seg", r.seg);
                r.segs = J.Int(rc, "segs", r.segs);
                r.daily = J.Int(rc, "daily", r.daily);
                r.runners = J.Int(rc, "runners", r.runners);
                r.betMin = J.Int(rc, "betMin", r.betMin);
                r.betMax = J.Int(rc, "betMax", r.betMax);
                if (J.Get(rc, "chips") != null) r.chips = Ints(J.Get(rc, "chips"));
                if (J.Get(rc, "pay") != null) r.pay = Nums(J.Get(rc, "pay"));
                if (J.Get(rc, "oddsLow") != null) r.oddsLow = Nums(J.Get(rc, "oddsLow"));
                if (J.Get(rc, "oddsHigh") != null) r.oddsHigh = Nums(J.Get(rc, "oddsHigh"));
                r.raceSec = J.Num(rc, "raceSec", r.raceSec);
                r.gapMin = J.Num(rc, "gapMin", r.gapMin);
                r.gapMax = J.Num(rc, "gapMax", r.gapMax);
                r.spread = J.Num(rc, "spread", r.spread);
                r.keyMin = J.Num(rc, "keyMin", r.keyMin);
                r.keyMax = J.Num(rc, "keyMax", r.keyMax);
                r.startSec = J.Num(rc, "startSec", r.startSec);
                r.endSec = J.Num(rc, "endSec", r.endSec);
                r.surge = J.Num(rc, "surge", r.surge);
                r.surgeSec = J.Num(rc, "surgeSec", r.surgeSec);
                r.stunDrop = J.Num(rc, "stunDrop", r.stunDrop);
                r.stunMax = J.Num(rc, "stunMax", r.stunMax);
                r.comeback = J.Num(rc, "comeback", r.comeback);
                r.tease = J.Num(rc, "tease", r.tease);
                if (J.Get(rc, "points") != null) r.points = Ints(J.Get(rc, "points"));
                r.weekPts = J.Int(rc, "weekPts", r.weekPts);
                foreach (var x in J.Arr(rc, "cups"))
                {
                    var cu = J.Obj(x);
                    r.cups.Add(new RaceCup
                    {
                        name = J.Str(cu, "name"), level = J.Int(cu, "level"), oppLevel = J.Int(cu, "oppLevel"), oppStar = J.Int(cu, "oppStar", 1),
                        fee = J.Int(cu, "fee"), skill = J.Num(cu, "skill"), week = Items(J.Get(cu, "week")),
                    });
                }
            }

            var fo = J.Obj(o, "fishing");
            if (fo != null)
            {
                var f = c.fishing;
                f.freeBait = J.Int(fo, "freeBait", f.freeBait);
                f.baitPack = J.Int(fo, "baitPack", f.baitPack);
                f.baitPrice = J.Int(fo, "baitPrice", f.baitPrice);
                f.farBonus = J.Num(fo, "farBonus", f.farBonus);
                f.biteWindow = J.Num(fo, "biteWindow", f.biteWindow);
                if (J.Get(fo, "pull") != null) f.pull = Nums(J.Get(fo, "pull"));
                if (J.Get(fo, "first") != null) f.first = Ints(J.Get(fo, "first"));
                if (J.Get(fo, "price") != null) f.price = Ints(J.Get(fo, "price"));
                f.setShards = J.Int(fo, "setShards", f.setShards);
                f.kingChance = J.Num(fo, "kingChance", f.kingChance);
                f.kingAssist = J.Num(fo, "kingAssist", f.kingAssist);
                f.kingRod = J.Int(fo, "kingRod", f.kingRod);
                foreach (var x in J.Arr(fo, "rods"))
                {
                    var ro2 = J.Obj(x);
                    f.rods.Add(new FishRod { cost = J.Int(ro2, "cost"), zone = J.Num(ro2, "zone"), spots = J.Int(ro2, "spots", 1) });
                }
                foreach (var x in J.Arr(fo, "spots"))
                {
                    var sp = J.Obj(x);
                    f.spots.Add(new FishSpot { name = J.Str(sp, "name"), rar = Nums(J.Get(sp, "rar")) });
                }
                foreach (var x in J.Arr(fo, "fish")) f.fish.Add(Fish(x));
                foreach (var x in J.Arr(fo, "kings")) f.kings.Add(Fish(x));
                f.king = Items(J.Get(fo, "king"));
            }

            var mo = J.Obj(o, "market");
            if (mo != null)
            {
                var m = c.market;
                m.slots = J.Int(mo, "slots", m.slots);
                m.nightSlots = J.Int(mo, "nightSlots", m.nightSlots);
                if (J.Get(mo, "periods") != null) m.periods = Ints(J.Get(mo, "periods"));
                if (J.Get(mo, "refresh") != null) m.refresh = Ints(J.Get(mo, "refresh"));
                m.copySell = J.Int(mo, "copySell", m.copySell);
                foreach (var x in J.Arr(mo, "offers"))
                {
                    var of = J.Obj(x);
                    m.offers.Add(new MarketOffer
                    {
                        kind = J.Str(of, "kind"), n = J.Int(of, "n", 1), w = J.Num(of, "w", 1), mark = J.Num(of, "mark", 1.5), price = J.Int(of, "price"),
                        night = J.Bool(of, "night"), rar = Keys.ToRarity(J.Str(of, "rar", "rare")),
                        defs = J.Arr(of, "defs").OfType<string>().ToArray(),
                    });
                }
                m.mystery = rolls(J.Arr(mo, "mystery"));
            }

            var uo = J.Obj(o, "underground");
            if (uo != null)
            {
                var u = c.underground;
                u.winMult = J.Num(uo, "winMult", u.winMult);
                u.daily = J.Int(uo, "daily", u.daily);
                u.rewinMult = J.Num(uo, "rewinMult", u.rewinMult);
                u.rewin = Items(J.Get(uo, "rewin"));
                foreach (var x in J.Arr(uo, "tiers"))
                {
                    var t = J.Obj(x);
                    u.tiers.Add(new UgTier
                    {
                        name = J.Str(t, "name"), level = J.Int(t, "level"), fee = J.Int(t, "fee"), shards = J.Int(t, "shards"),
                        items = Items(J.Get(t, "items")), weekly = J.Bool(t, "weekly"),
                    });
                }
                foreach (var x in J.Arr(uo, "rotation")) u.rotation.Add(Day(J.Obj(x)));
                foreach (var x in J.Arr(uo, "dates")) u.dates.Add(Day(J.Obj(x)));
            }

            var io = J.Obj(o, "inn");
            if (io != null)
            {
                c.inn.count = J.Int(io, "count", c.inn.count);
                foreach (var x in J.Arr(io, "quests"))
                {
                    var q = J.Obj(x);
                    c.inn.quests.Add(new InnQuest
                    {
                        id = J.Str(q, "id"), kind = J.Str(q, "kind"), text = J.Str(q, "text"), n = J.Int(q, "n", 1), need = J.Str(q, "need"),
                        items = Items(J.Get(q, "items")),
                    });
                }
                c.inn.all = Items(J.Get(io, "all"));
            }
            return c;
        }
    }
}
