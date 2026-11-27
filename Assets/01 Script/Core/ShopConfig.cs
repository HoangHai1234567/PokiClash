// Cấu hình cửa hàng, gói bán, ưu đãi, quảng cáo thưởng mở rộng (GD_Claude/26_CuaHang_IAP_QuangCao.md, 2026-11-23): khối "shop" trong
// balance.json. Lớp [Serializable], chỉ List và mảng phẳng để Unity lưu được trong BalanceConfigAsset (như HomeConfig). Số là số đầu,
// chỉnh bằng ProgressSim và số đo thật.
// Giá tính bằng USD theo bậc giá của store; mã sản phẩm store suy từ giá (Product): các gói cùng giá dùng chung một mã consumable,
// nội dung do game trao. "Bỏ quảng cáo" là mã non-consumable riêng.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    // một món trong gói. k: balls, egg (trứng capsule, r = bậc 0..4; hero_chest / gold_chest cũ đọc thành trứng Khá / Sử thi), ticket
    // (vé chọn tướng, r = độ hiếm cao nhất), ticket_week (chọn 1 trong 2 tướng
    // tuần), evo, stones, crystal, shards (h: id tướng hoặc "*feat" tướng tuần, "*carry" tướng chủ lực đội, "*near" tướng sắp lên sao,
    // "*new" tướng vừa mở), copies (bản sao thẻ của h), week_card, month_card, no_ads
    [Serializable]
    public class ShopItem
    {
        public string k;
        public int n = 1;
        public string h;
        public int r = -1;

        public ShopItem Copy() => new ShopItem { k = k, n = n, h = h, r = r };
    }

    [Serializable]
    public class ShopDay
    {
        public List<ShopItem> items = new List<ShopItem>();
    }

    // gói cố định. tab: offers, balls, heroes, perks, "" (chỉ hiện qua popup). kind: pack, days (mua một lần, nhận theo ngày), card
    // (thẻ tuần / tháng), fund, piggy, noads
    [Serializable]
    public class ShopPack
    {
        public string id, name, desc, tab = "", kind = "pack";
        public string Name => Loc.T(name);
        public string Desc => Loc.T(desc);
        public double price;
        public int limit; // tổng số lần mua (0: không giới hạn)
        public bool daily, weekly; // limit tính theo ngày / tuần thay vì cả đời
        public double hours; // gói hẹn giờ: mở bao lâu kể từ lần hiện đầu (0: không hẹn giờ)
        public bool firstDouble; // lần đầu mua tặng gấp đôi bi
        public bool scale; // số bi nhân theo bậc cấp người chơi
        // nhóm chọn một (nạp đầu 3 bậc): các gói cùng group chỉ mua được MỘT gói, mua rồi thì ưu đãi của các gói còn lại đóng.
        // group ghi id của gói đứng đầu nhóm (gói có popup và bong bóng); rỗng: gói thường
        public string group;
        // nhãn giá trị hiển thị "×N" thay cho số tính theo món (người dùng 2026-11-27: ba bậc Khởi Hành ghi ×5 / ×10 / ×20 cho thấy bậc giá
        // gấp 2, gấp 4 thì hời hơn; chỉ là nhãn, quà không đổi); 0: tính theo món (Shop.PackMult / OfferMult)
        public double tag;
        public int sort;
        public List<ShopItem> items = new List<ShopItem>();
        public List<ShopDay> days = new List<ShopDay>(); // kind days: ngày 1, 2, 3...
    }

    // trứng capsule bậc tier (= độ hiếm tướng): nở min–max mảnh một tướng bậc đó; up: cơ hội nở lên một bậc (Core/Eggs.cs)
    [Serializable]
    public class EggDef
    {
        public int tier;
        public string name;
        public string Name => Loc.T(name);
        public int min = 12, max = 16;
        public double up;
    }

    // mẫu ưu đãi động: nội dung tính lúc bật theo nhu cầu (Offers.Build). value: giá trị ×N nhắm tới; hours: mở bao lâu
    [Serializable]
    public class OfferTpl
    {
        public string id, name;
        public string Name => Loc.T(name);
        public double hours = 2, value = 4;
        public double price; // 0: theo thang giá của người chơi
        public List<ShopItem> items = new List<ShopItem>(); // món cố định thêm vào (Quà Trở Lại...)
    }

    [Serializable]
    public class OfferCaps
    {
        public int perOpen = 2, perDay = 4, firstDay = 1;
        public double gapMin = 3, afterBuyMin = 10, afterAdSec = 5;
        public double dismissH = 24, dismiss3H = 72;
        public double flashGapH = 6, flashChance = 0.25, flashChancePayer = 0.35, lowChance = 0.3, hotChance = 0.3, lowPct = 0.2;
        public int flashPerDay = 2;
        public int reliefLosses = 3;
        public double reliefGapH = 24, refillGapMin = 20, comebackDays = 3, ladderDownDays = 7, bigBuy = 19.99, nearStarPct = 0.8;
        public double reopenMin = 30; // quay lại game sau bấy nhiêu phút thì tính là một lần vào game mới (hàng popup lúc vào)
        // Gói Vượt Mốc (mẫu "jump", GD_Claude/34 mục 2): qua ải tướng mốc jumpFrom trở lên thì chào tướng đi trước jumpAhead mốc;
        // lên sao tối đa tới sao tổng jumpMaxStar (15 = hết bậc Vàng); jumpCopies bản sao thẻ mỗi bậc sao; giá là bậc thấp nhất
        // của jumpPrices mà gói đạt × value của mẫu (thang riêng, dày hơn thang ưu đãi, để gói không phải độn nhiều bi cho đủ giá)
        public int jumpFrom = 3, jumpAhead = 3, jumpMaxStar = 15, jumpCopies = 3;
        public double[] jumpPrices = { 4.99, 9.99, 14.99, 19.99, 29.99, 49.99, 99.99 };
    }

    [Serializable]
    public class PiggyConfig
    {
        public double cap = 2000, minPct = 0.4, grow = 0.2, maxMult = 2, price = 4.99;
        public double gapDays = 3; // số ngày tối thiểu giữa hai lần đập (GD_Claude/33 việc 15)
    }

    [Serializable]
    public class ChainStep
    {
        public double price; // 0: miễn phí
        public List<ShopItem> items = new List<ShopItem>();
    }

    [Serializable]
    public class ChainDef
    {
        public string id, name;
        public string Name => Loc.T(name);
        public List<ChainStep> steps = new List<ChainStep>();
    }

    [Serializable]
    public class FundStep
    {
        public int lv;
        public List<ShopItem> paid = new List<ShopItem>(), free = new List<ShopItem>();
    }

    [Serializable]
    public class PassCardDef
    {
        public string id, name;
        public string Name => Loc.T(name);
        public int days = 7;
        public List<ShopItem> now = new List<ShopItem>(), daily = new List<ShopItem>();
        public double treeCap = 1; // thẻ tuần: sức chứa cây bi ×
        public int adSkips; // thẻ tháng: số lượt quảng cáo trao ngay mỗi ngày
    }

    [Serializable]
    public class AdMilestone
    {
        public int n;
        public List<ShopItem> items = new List<ShopItem>();
    }

    [Serializable]
    public class ValueOf
    {
        public string k;
        public double v;
    }

    [Serializable]
    public class ShopConfig
    {
        public double valuePerUsd = 101.0101; // $0,99 = 100 bi quy đổi
        public List<ValueOf> value = new List<ValueOf>();
        public int[] bandLv = { 1 };
        public double[] bandMult = { 1 };
        public double[] ladder = { 0.99, 1.99, 4.99, 9.99, 19.99, 49.99 };
        public double ownedBias = 0.6, featuredMult = 3;
        public int featuredCount = 2, ticketShards = 20, ticketChoices = 6;
        public int adBalls = 30; // bi mỗi lượt quảng cáo free_balls (nhân bậc cấp)
        public double retryBoost = 0.15; // Tiếp sức (quảng cáo battle_retry): +15% công và máu cả đội trong trận đánh lại
        public List<ShopPack> packs = new List<ShopPack>();
        public List<EggDef> eggs = new List<EggDef>();
        public List<OfferTpl> offers = new List<OfferTpl>();
        public OfferCaps caps = new OfferCaps();
        public PiggyConfig piggy = new PiggyConfig();
        public double chainHours = 72;
        public int chainEveryDays = 14;
        public List<ChainDef> chains = new List<ChainDef>();
        public double fundPrice = 9.99;
        public List<FundStep> fund = new List<FundStep>();
        public List<PassCardDef> cards = new List<PassCardDef>();
        public List<AdMilestone> adMilestones = new List<AdMilestone>();
        public List<ShopItem> dailyGift = new List<ShopItem>();
        public List<ShopItem> comebackGift = new List<ShopItem>();

        public ShopPack Pack(string id) => packs.Find(p => p.id == id);
        public EggDef Egg(int tier) => eggs.Find(e => e.tier == tier);
        public OfferTpl Offer(string id) => offers.Find(o => o.id == id);
        public PassCardDef Card(string id) => cards.Find(c => c.id == id);
        public double Value(string k) => value.Find(v => v.k == k)?.v ?? 0;

        // mã sản phẩm store theo giá (consumable dùng chung theo bậc), Bỏ quảng cáo riêng (non-consumable)
        public static string Product(double price) => "poki_" + (int)Math.Round(price * 100);
        public const string NoAdsProduct = "poki_noads";

        // hệ số bi theo bậc cấp người chơi
        public double Band(int level)
        {
            double m = 1;
            for (int i = 0; i < bandLv.Length && i < bandMult.Length; i++)
                if (level >= bandLv[i]) m = bandMult[i];
            return m;
        }

        public List<string> Validate()
        {
            var err = new List<string>();
            var ids = new HashSet<string>();
            foreach (var p in packs)
            {
                if (string.IsNullOrEmpty(p.id)) err.Add("shop.packs: gói thiếu id");
                else if (!ids.Add(p.id)) err.Add($"shop.packs: trùng id {p.id}");
                if (p.price < 0) err.Add($"shop.packs.{p.id}: giá âm");
                if (p.kind == "days" && p.days.Count == 0) err.Add($"shop.packs.{p.id}: gói theo ngày không có ngày nào");
            }
            for (int t = 0; t < Eggs.Tiers; t++)
            {
                var e = Egg(t);
                if (e == null) err.Add($"shop.eggs: thiếu trứng bậc {t}");
                else if (e.min <= 0 || e.max < e.min) err.Add($"shop.eggs.{t}: min/max sai");
                else if (e.up < 0 || e.up >= 1) err.Add($"shop.eggs.{t}: up phải trong [0, 1)");
            }
            if (bandLv.Length != bandMult.Length) err.Add("shop.bands: lv và mult khác số phần tử");
            if (ladder.Length == 0) err.Add("shop.ladder: rỗng");
            foreach (var id in new[] { "flash", "hot", "relief", "companion", "nearstar", "newisle", "jump", "comeback", "refill" })
                if (Offer(id) == null) err.Add($"shop.offers: thiếu mẫu {id}");
            foreach (var id in new[] { "week", "month" })
                if (Card(id) == null) err.Add($"shop.cards: thiếu thẻ {id}");
            return err;
        }

        // ---------- đọc balance.json ----------

        static List<ShopItem> Items(object arr)
        {
            var list = new List<ShopItem>();
            foreach (var x in J.Arr(arr))
            {
                var o = J.Obj(x);
                if (o == null) continue;
                list.Add(new ShopItem { k = J.Str(o, "k"), n = J.Int(o, "n", 1), h = J.Str(o, "h"), r = J.Int(o, "r", -1) });
            }
            return list;
        }

        static double[] Nums(object arr) => J.Arr(arr).Select(x => x is double d ? d : 0).ToArray();
        static int[] Ints(object arr) => J.Arr(arr).Select(x => x is double d ? (int)d : 0).ToArray();

        public static ShopConfig FromJson(Dictionary<string, object> o)
        {
            var c = new ShopConfig();
            if (o == null) return c;
            c.valuePerUsd = J.Num(o, "valuePerUsd", c.valuePerUsd);
            foreach (var kv in J.Obj(o, "value") ?? new Dictionary<string, object>())
                if (kv.Value is double v) c.value.Add(new ValueOf { k = kv.Key, v = v });
            var bands = J.Arr(o, "bands");
            if (bands.Count > 0)
            {
                c.bandLv = bands.Select(b => J.Int(J.Obj(b), "lv", 1)).ToArray();
                c.bandMult = bands.Select(b => J.Num(J.Obj(b), "m", 1)).ToArray();
            }
            if (J.Arr(o, "ladder").Count > 0) c.ladder = Nums(J.Get(o, "ladder"));
            c.ownedBias = J.Num(o, "ownedBias", c.ownedBias);
            c.featuredMult = J.Num(o, "featuredMult", c.featuredMult);
            c.featuredCount = J.Int(o, "featuredCount", c.featuredCount);
            c.ticketShards = J.Int(o, "ticketShards", c.ticketShards);
            c.ticketChoices = J.Int(o, "ticketChoices", c.ticketChoices);
            c.adBalls = J.Int(o, "adBalls", c.adBalls);
            c.retryBoost = J.Num(o, "retryBoost", c.retryBoost);
            foreach (var x in J.Arr(o, "packs"))
            {
                var p = J.Obj(x);
                if (p == null) continue;
                var pk = new ShopPack
                {
                    id = J.Str(p, "id"), name = J.Str(p, "name", ""), desc = J.Str(p, "desc", ""), tab = J.Str(p, "tab", ""),
                    kind = J.Str(p, "kind", "pack"), price = J.Num(p, "price"), limit = J.Int(p, "limit"), daily = J.Bool(p, "daily"),
                    weekly = J.Bool(p, "weekly"), hours = J.Num(p, "hours"), firstDouble = J.Bool(p, "firstDouble"), scale = J.Bool(p, "scale"), group = J.Str(p, "group"),
                    tag = J.Num(p, "tag"), sort = J.Int(p, "sort"), items = Items(J.Get(p, "items")),
                };
                foreach (var d in J.Arr(p, "days")) pk.days.Add(new ShopDay { items = Items(d) });
                c.packs.Add(pk);
            }
            foreach (var x in J.Arr(o, "eggs"))
            {
                var e = J.Obj(x);
                if (e == null) continue;
                c.eggs.Add(new EggDef { tier = J.Int(e, "tier"), name = J.Str(e, "name", ""), min = J.Int(e, "min", 12), max = J.Int(e, "max", 16), up = J.Num(e, "up") });
            }
            foreach (var x in J.Arr(o, "offers"))
            {
                var t = J.Obj(x);
                if (t == null) continue;
                c.offers.Add(new OfferTpl
                {
                    id = J.Str(t, "id"), name = J.Str(t, "name", ""), hours = J.Num(t, "hours", 2), value = J.Num(t, "value", 4), price = J.Num(t, "price"),
                    items = Items(J.Get(t, "items")),
                });
            }
            var cp = J.Obj(o, "caps");
            if (cp != null)
            {
                var k = c.caps;
                k.perOpen = J.Int(cp, "perOpen", k.perOpen);
                k.perDay = J.Int(cp, "perDay", k.perDay);
                k.firstDay = J.Int(cp, "firstDay", k.firstDay);
                k.gapMin = J.Num(cp, "gapMin", k.gapMin);
                k.afterBuyMin = J.Num(cp, "afterBuyMin", k.afterBuyMin);
                k.afterAdSec = J.Num(cp, "afterAdSec", k.afterAdSec);
                k.dismissH = J.Num(cp, "dismissH", k.dismissH);
                k.dismiss3H = J.Num(cp, "dismiss3H", k.dismiss3H);
                k.flashGapH = J.Num(cp, "flashGapH", k.flashGapH);
                k.flashChance = J.Num(cp, "flashChance", k.flashChance);
                k.flashChancePayer = J.Num(cp, "flashChancePayer", k.flashChancePayer);
                k.lowChance = J.Num(cp, "lowChance", k.lowChance);
                k.hotChance = J.Num(cp, "hotChance", k.hotChance);
                k.lowPct = J.Num(cp, "lowPct", k.lowPct);
                k.flashPerDay = J.Int(cp, "flashPerDay", k.flashPerDay);
                k.reliefLosses = J.Int(cp, "reliefLosses", k.reliefLosses);
                k.reliefGapH = J.Num(cp, "reliefGapH", k.reliefGapH);
                k.refillGapMin = J.Num(cp, "refillGapMin", k.refillGapMin);
                k.comebackDays = J.Num(cp, "comebackDays", k.comebackDays);
                k.ladderDownDays = J.Num(cp, "ladderDownDays", k.ladderDownDays);
                k.bigBuy = J.Num(cp, "bigBuy", k.bigBuy);
                k.jumpFrom = J.Int(cp, "jumpFrom", k.jumpFrom);
                k.jumpAhead = J.Int(cp, "jumpAhead", k.jumpAhead);
                k.jumpMaxStar = J.Int(cp, "jumpMaxStar", k.jumpMaxStar);
                k.jumpCopies = J.Int(cp, "jumpCopies", k.jumpCopies);
                if (J.Arr(cp, "jumpPrices").Count > 0) k.jumpPrices = Nums(J.Get(cp, "jumpPrices"));
                k.nearStarPct = J.Num(cp, "nearStarPct", k.nearStarPct);
                k.reopenMin = J.Num(cp, "reopenMin", k.reopenMin);
            }
            var pg = J.Obj(o, "piggy");
            if (pg != null)
                c.piggy = new PiggyConfig
                {
                    cap = J.Num(pg, "cap", 2000), minPct = J.Num(pg, "minPct", 0.4), grow = J.Num(pg, "grow", 0.2), maxMult = J.Num(pg, "maxMult", 2),
                    price = J.Num(pg, "price", 4.99), gapDays = J.Num(pg, "gapDays", 3),
                };
            c.chainHours = J.Num(o, "chainHours", c.chainHours);
            c.chainEveryDays = J.Int(o, "chainEveryDays", c.chainEveryDays);
            foreach (var x in J.Arr(o, "chains"))
            {
                var ch = J.Obj(x);
                if (ch == null) continue;
                var def = new ChainDef { id = J.Str(ch, "id"), name = J.Str(ch, "name", "") };
                foreach (var s in J.Arr(ch, "steps"))
                {
                    var so = J.Obj(s);
                    def.steps.Add(new ChainStep { price = J.Num(so, "price"), items = Items(J.Get(so, "items")) });
                }
                c.chains.Add(def);
            }
            c.fundPrice = J.Num(o, "fundPrice", c.fundPrice);
            foreach (var x in J.Arr(o, "fund"))
            {
                var f = J.Obj(x);
                if (f != null) c.fund.Add(new FundStep { lv = J.Int(f, "lv"), paid = Items(J.Get(f, "paid")), free = Items(J.Get(f, "free")) });
            }
            foreach (var x in J.Arr(o, "cards"))
            {
                var cd = J.Obj(x);
                if (cd == null) continue;
                c.cards.Add(new PassCardDef
                {
                    id = J.Str(cd, "id"), name = J.Str(cd, "name", ""), days = J.Int(cd, "days", 7), now = Items(J.Get(cd, "now")), daily = Items(J.Get(cd, "daily")),
                    treeCap = J.Num(cd, "treeCap", 1), adSkips = J.Int(cd, "adSkips"),
                });
            }
            foreach (var x in J.Arr(o, "adMilestones"))
            {
                var m = J.Obj(x);
                if (m != null) c.adMilestones.Add(new AdMilestone { n = J.Int(m, "n"), items = Items(J.Get(m, "items")) });
            }
            c.dailyGift = Items(J.Get(o, "dailyGift"));
            c.comebackGift = Items(J.Get(o, "comebackGift"));
            return c;
        }
    }
}
