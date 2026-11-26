// Cửa hàng (GD_Claude/26_CuaHang_IAP_QuangCao.md, 2026-11-23): trạng thái lưu, mua gói, trao vật phẩm, thẻ tuần / tháng, gói nhận theo
// ngày, Lọ Bi, Chuỗi Quà, Quỹ Phiêu Lưu, quà ngày, bảng mốc quảng cáo, vé chọn tướng, tướng tuần. C# thuần (test được ngoài Unity).
// Cửa hàng thật (Store) báo mua thành công rồi mới gọi Buy*; ở đây chỉ ghi và trao. Giờ là mili giây (như SaveService.Now).
// Đổi chốt cũ "không bán bi" (07_MayBi.md 2026-10-30): người dùng duyệt bán bi và Rương Tướng 2026-11-23.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class Spend
    {
        public double t, usd;
    }

    public sealed class DaysState
    {
        public int buyDay, claimed; // ngày mua, số ngày đã nhận
    }

    public sealed class CardState
    {
        public double until; // ms hết thẻ
        public int lastDay = -1; // ngày nhận quà ngày gần nhất
    }

    // ưu đãi đang mở (hẹn giờ): nội dung chốt lúc bật (Offers.Build), hoặc gói cố định (pack)
    public sealed class ActiveOffer
    {
        public string uid, tpl, pack, hero;
        public double price, until, created; // until 0: chưa chạy đồng hồ (Quà Nhập Môn chờ lần popup đầu)
        public List<ShopItem> items = new List<ShopItem>();
        public bool bought, ladder, popped, warned; // ladder: giá theo thang (mua thì lên bậc); popped: đã popup; warned: đã báo sắp hết
    }

    public sealed class OfferBook
    {
        public List<ActiveOffer> active = new List<ActiveOffer>();
        public Dictionary<string, int> dismiss = new Dictionary<string, int>();
        public Dictionary<string, double> dismissAt = new Dictionary<string, double>();
        public int autoDay, autoCount, muteDay = -1, flashDay, flashCount, nearDay = -1, seenZones = -1, seq;
        public double lastAuto, lastBuy, lastAd, lastFlash, lastRelief, lastRefill;
        public int lossStage, lossStreak;
        public bool refillSeen; // đã gặp popup Hết bi lần nào chưa (lần đầu chỉ có quảng cáo và Cây bi)
        public List<string> seenOwned; // null: chưa quét lần nào
        public List<string> done = new List<string>(); // cờ một lần: starter3, launch, intro_week, intro_fund...
    }

    public sealed class ShopState
    {
        public Dictionary<string, int> bought = new Dictionary<string, int>(); // gói → số lần mua cả đời
        public Dictionary<string, int> periodKey = new Dictionary<string, int>(); // gói giới hạn ngày / tuần: kỳ của lần mua gần nhất
        public Dictionary<string, int> periodN = new Dictionary<string, int>(); // số lần mua trong kỳ đó
        public List<string> firstDone = new List<string>(); // gói đã dùng lần tặng đôi
        public Dictionary<string, int> items = new Dictionary<string, int>(); // túi: egg_0..egg_4 (trứng theo bậc), ticket_week
        public List<int> tickets = new List<int>(); // vé chọn tướng: độ hiếm cao nhất của từng vé (-1: tới Sử thi)
        public List<Spend> spend = new List<Spend>();
        public int ladder;
        public double ladderAt;
        public double installAt, lastSeen;
        public int sessions;
        public Dictionary<string, DaysState> days = new Dictionary<string, DaysState>();
        public Dictionary<string, CardState> cards = new Dictionary<string, CardState>();
        public double piggy;
        public double piggyAt; // ms lần đập Lọ Bi gần nhất (0: chưa đập)
        public int piggyBreaks;
        public bool piggyFullShown;
        public int chainCycle = -1, chainStep;
        public double chainUntil, chainNext;
        public bool fund;
        public List<int> fundPaid = new List<int>(), fundFree = new List<int>();
        public int adDay = -1, adCount;
        public List<int> adClaimed = new List<int>();
        public int giftDay = -1, skipDay = -1, skipUsed;
        public OfferBook offers = new OfferBook();

        public int Item(string k) => items.TryGetValue(k, out var n) ? n : 0;
        public void AddItem(string k, int n) => items[k] = Math.Max(0, Item(k) + n);
    }

    public static class Shop
    {
        public const double Day = 86400000, Hour = 3600000;
        public const string Egg = Eggs.Item, Ticket = "ticket", TicketWeek = "ticket_week";
        // Rương Tướng / Rương Tướng Vàng cũ (trước 2026-11-23): còn trong bản lưu, ưu đãi đang mở thì đọc thành trứng Khá / Sử thi
        public const string HeroChest = "hero_chest", GoldChest = "gold_chest";

        public static ShopItem Norm(ShopItem it)
        {
            if (it == null) return null;
            if (it.k == HeroChest) return new ShopItem { k = Egg, n = it.n, r = (int)Rarity.Uncommon };
            if (it.k == GoldChest) return new ShopItem { k = Egg, n = it.n, r = (int)Rarity.Epic };
            return it;
        }

        public static ShopState Of(SaveData s) => s.shop ?? (s.shop = new ShopState());
        public static int Today(double now) => Afk.Today(now);
        public static int Week(int day) => (int)Math.Floor((day + 3) / 7.0); // tuần bắt đầu thứ Hai (ngày 0 = thứ Năm 1/1/1970)

        // ---------- giá trị (nhãn "giá trị ×N") ----------

        public static double ShardValue(ShopConfig c, Rarity r) =>
            c.Value(r == Rarity.Common ? "shard_common" : r == Rarity.Uncommon ? "shard_uncommon" : r == Rarity.Rare ? "shard_rare" : r == Rarity.Epic ? "shard_epic" : "shard_legend");

        public static double Value(ShopConfig c, GameData d, ShopItem it)
        {
            it = Norm(it);
            switch (it.k)
            {
                case "balls": return it.n * c.Value("balls");
                case "shards":
                    var h = it.h != null && !it.h.StartsWith("*") ? d.Hero(it.h) : null;
                    return it.n * ShardValue(c, h?.rarity ?? Rarity.Rare);
                case "copies": return it.n * c.Value("copies");
                case Egg: return it.n * c.Value(Eggs.Key(it.r));
                case Ticket: case TicketWeek: case "evo": case "stones": case "crystal":
                    return it.n * c.Value(it.k);
                default: return 0;
            }
        }

        public static double Value(ShopConfig c, GameData d, IEnumerable<ShopItem> items) => items.Sum(it => Value(c, d, it));

        // giá trị ×N so với bảng giá gốc ($0,99 = 100 bi quy đổi); 0 nếu miễn phí
        public static double Mult(ShopConfig c, GameData d, IEnumerable<ShopItem> items, double price) =>
            price <= 0 ? 0 : Value(c, d, items) / (price * c.valuePerUsd);

        public static double PackValue(SaveData s, GameData d, ShopPack p)
        {
            var c = d.Cfg.shop;
            switch (p.kind)
            {
                case "days": return p.days.Sum(day => Value(c, d, Resolve(s, d, day.items, p.scale, null)));
                case "card":
                    var card = CardOf(c, p);
                    double v = Value(c, d, Resolve(s, d, p.items.Where(i => i.k != "week_card" && i.k != "month_card").ToList(), true, null));
                    return card == null ? v : v + card.days * Value(c, d, Resolve(s, d, card.daily, true, null));
                case "fund": return c.fund.Sum(f => Value(c, d, Resolve(s, d, f.paid, true, null)));
                case "piggy": return Math.Floor(Of(s).piggy);
                default: return Value(c, d, Resolve(s, d, p.items, p.scale, null));
            }
        }

        public static double PackMult(SaveData s, GameData d, ShopPack p) => p.price <= 0 ? 0 : PackValue(s, d, p) / (p.price * d.Cfg.shop.valuePerUsd);

        // ---------- tướng tuần, vé chọn tướng ----------

        // 2 tướng (Hiếm, Sử thi) xoay vòng mỗi tuần, cố định theo số tuần: tỉ lệ ra ×featuredMult trong Rương Tướng, gói tướng tuần
        public static List<string> Featured(GameData d, int week)
        {
            var pool = d.Heroes.Where(h => h.rarity == Rarity.Rare || h.rarity == Rarity.Epic).Select(h => h.id).OrderBy(x => x, StringComparer.Ordinal).ToList();
            var rng = new Rng((uint)(week * 7919 + 17));
            var list = new List<string>();
            int n = Math.Min(d.Cfg.shop.featuredCount, pool.Count);
            while (list.Count < n)
            {
                var h = rng.Pick(pool);
                if (!list.Contains(h)) list.Add(h);
            }
            return list;
        }

        public static List<string> FeaturedNow(GameData d, double now) => Featured(d, Week(Today(now)));

        static double StarRatio(SaveData s, GameData d, string hero)
        {
            var g = Progress.ShardGoal(s, d, hero);
            return g.need > 0 ? (double)g.have / g.need : 0;
        }

        // tướng chủ lực: tướng đầu đội chưa tối đa sao (không có thì tướng khởi đầu)
        public static string Carry(SaveData s, GameData d)
        {
            foreach (var h in s.team)
                if (s.Hero(h) != null && Progress.ShardGoal(s, d, h).need > 0) return h;
            return s.team.FirstOrDefault() ?? s.starter ?? d.Heroes[0].id;
        }

        // tướng trong đội gần lên sao nhất (null nếu không ai đạt min)
        public static string Near(SaveData s, GameData d, double min)
        {
            string best = null;
            double bv = min;
            foreach (var h in s.team)
            {
                var p = s.Hero(h);
                if (p == null || !p.owned) continue;
                double r = StarRatio(s, d, h);
                if (r >= bv && r < 1)
                {
                    bv = r;
                    best = h;
                }
            }
            return best;
        }

        // 6 tướng gợi ý của vé: 3 tướng chưa có gom mảnh nhiều nhất, 3 tướng trong đội gần lên sao nhất, thiếu thì bù ngẫu nhiên (hạt theo
        // ngày, mở lại vẫn ra như cũ). maxR: độ hiếm cao nhất (-1: tới Sử thi); elem: chỉ một hệ (null: mọi hệ)
        public static List<string> TicketChoices(SaveData s, GameData d, int maxR, Elem? elem, double now)
        {
            int top = maxR < 0 ? (int)Rarity.Epic : maxR;
            var pool = d.Heroes.Where(h => (int)h.rarity <= top && (elem == null || h.elem == elem)).ToList();
            var rng = new Rng((uint)(Today(now) * 131 + top * 17 + (elem.HasValue ? (int)elem.Value + 1 : 0)));
            int want = d.Cfg.shop.ticketChoices;
            var list = new List<string>();
            foreach (var h in pool.Where(h => !s.Hero(h.id).owned).OrderByDescending(h => StarRatio(s, d, h.id)).ThenBy(h => rng.Next()).Take(want / 2))
                list.Add(h.id);
            foreach (var h in pool.Where(h => s.Hero(h.id).owned && s.team.Contains(h.id) && Progress.ShardGoal(s, d, h.id).need > 0)
                         .OrderByDescending(h => StarRatio(s, d, h.id)).Take(want - list.Count))
                list.Add(h.id);
            var rest = pool.Where(h => !list.Contains(h.id)).OrderBy(h => rng.Next()).ToList();
            foreach (var h in rest)
            {
                if (list.Count >= want) break;
                list.Add(h.id);
            }
            return list;
        }

        // mã một vé trong túi: hàng đơn vị là độ hiếm cao nhất (9: tới Sử thi), hàng chục là hệ + 1 (0: mọi hệ; món ghi h = "e:hoa")
        public static int TicketCode(ShopItem it)
        {
            int r = it.r < 0 ? 9 : Math.Min(it.r, 4);
            int e = it.h != null && it.h.StartsWith("e:") ? (int)Keys.ToElem(it.h.Substring(2)) + 1 : 0;
            return r + e * 10;
        }

        public static int TicketRarity(int code) => code % 10 == 9 ? -1 : code % 10;
        public static Elem? TicketElem(int code) => code / 10 > 0 ? (Elem)(code / 10 - 1) : (Elem?)null;

        public static List<string> TicketChoicesOf(SaveData s, GameData d, int code, double now) => TicketChoices(s, d, TicketRarity(code), TicketElem(code), now);

        // mảnh nhận khi chọn tướng bằng vé: tướng chưa có thì đủ mở khoá, đã có thì ticketShards
        public static int TicketShards(SaveData s, GameData d, string hero)
        {
            var p = s.Hero(hero);
            if (p.owned) return d.Cfg.shop.ticketShards;
            return Math.Max(1, d.Hero(hero).shards - p.shards);
        }

        // dùng vé (week: vé tướng tuần) chọn hero; false nếu không có vé hoặc tướng không nằm trong danh sách
        public static Reward UseTicket(SaveData s, GameData d, bool week, int index, string hero, double now, Rng rng)
        {
            var st = Of(s);
            List<string> choices;
            if (week)
            {
                if (st.Item(TicketWeek) <= 0) return null;
                choices = FeaturedNow(d, now);
            }
            else
            {
                if (index < 0 || index >= st.tickets.Count) return null;
                choices = TicketChoicesOf(s, d, st.tickets[index], now);
            }
            if (!choices.Contains(hero)) return null;
            int n = TicketShards(s, d, hero);
            if (week) st.AddItem(TicketWeek, -1);
            else st.tickets.RemoveAt(index);
            return new Reward { k = RewardKind.Shards, n = n, hero = hero, res = Progress.AddShards(s, d, hero, n, rng) };
        }

        // ---------- đổi món có tham số thành món cụ thể ----------

        public static string ResolveHero(SaveData s, GameData d, string h, string ctx)
        {
            if (h == null) return null;
            switch (h)
            {
                case "*feat": return Featured(d, Week(Today(Of(s).lastSeen > 0 ? Of(s).lastSeen : 0))).FirstOrDefault();
                case "*carry": return Carry(s, d);
                case "*near": return Near(s, d, 0) ?? Carry(s, d);
                case "*new": case "*ctx": return ctx ?? Carry(s, d);
                default: return h.StartsWith("*") ? Carry(s, d) : h;
            }
        }

        // món cụ thể: hero thật, bi đã nhân bậc cấp (scale), mảnh "n = 0" là số còn thiếu để lên sao
        public static List<ShopItem> Resolve(SaveData s, GameData d, List<ShopItem> items, bool scale, string ctx)
        {
            var c = d.Cfg.shop;
            var outL = new List<ShopItem>();
            foreach (var it in items)
            {
                var x = Norm(it).Copy();
                if (x.k == "balls" && scale) x.n = RoundBalls(x.n * c.Band(s.level));
                if (x.k == "shards" || x.k == "copies")
                {
                    x.h = ResolveHero(s, d, x.h, ctx);
                    if (x.h == null || d.Hero(x.h) == null) continue;
                    if (x.k == "shards" && x.n <= 0)
                    {
                        var g = Progress.ShardGoal(s, d, x.h);
                        x.n = Math.Max(1, g.need - g.have);
                    }
                }
                outL.Add(x);
            }
            return outL;
        }

        public static int RoundBalls(double n) => n < 50 ? Math.Max(1, (int)Math.Round(n)) : (int)Math.Round(n / 10) * 10;

        // ---------- trao ----------

        // trao món đã cụ thể hoá; trả danh sách thưởng để hộp nhận thưởng vẽ ô
        public static List<Reward> Grant(SaveData s, GameData d, List<ShopItem> items, double now, Rng rng)
        {
            var st = Of(s);
            var outL = new List<Reward>();
            foreach (var raw in items)
            {
                var it = Norm(raw);
                switch (it.k)
                {
                    case "balls":
                        s.balls += it.n;
                        outL.Add(new Reward { k = RewardKind.Balls, n = it.n });
                        break;
                    case Egg:
                        st.AddItem(Eggs.Key(it.r), it.n);
                        outL.Add(new Reward { k = RewardKind.Egg, n = it.n, id = Eggs.Key(it.r) });
                        break;
                    case TicketWeek:
                        st.AddItem(it.k, it.n);
                        outL.Add(new Reward { k = RewardKind.Ticket, n = it.n, id = it.k });
                        break;
                    case Ticket:
                        for (int i = 0; i < it.n; i++) st.tickets.Add(TicketCode(it));
                        outL.Add(new Reward { k = RewardKind.Ticket, n = it.n, id = Ticket });
                        break;
                    case "evo":
                        s.evoStones += it.n;
                        outL.Add(new Reward { k = RewardKind.EvoStones, n = it.n });
                        break;
                    case "stones":
                        s.potentialStones += it.n;
                        outL.Add(new Reward { k = RewardKind.Stones, n = it.n });
                        break;
                    case "crystal":
                        s.potentialCrystals += it.n;
                        outL.Add(new Reward { k = RewardKind.Crystal, n = it.n });
                        break;
                    case "shards":
                        if (s.Hero(it.h) == null) break;
                        outL.Add(new Reward { k = RewardKind.Shards, n = it.n, hero = it.h, res = Progress.AddShards(s, d, it.h, it.n, rng) });
                        break;
                    case "copies":
                    {
                        var h = d.Hero(it.h);
                        if (h == null || !s.Hero(it.h).owned) break;
                        for (int i = 0; i < it.n; i++)
                        {
                            var slot = rng.Pick(Progress.Slots);
                            var card = Progress.CardOf(h, slot);
                            var drop = new Progress.CardDrop { hero = it.h, slot = slot, card = card, rarity = d.Card(card).rarity };
                            Progress.GiveCard(s, drop);
                            outL.Add(new Reward { k = RewardKind.Card, drop = drop });
                        }
                        break;
                    }
                    case "week_card":
                    case "month_card":
                    {
                        string id = it.k == "week_card" ? "week" : "month";
                        var def = d.Cfg.shop.Card(id);
                        var cs = st.cards.TryGetValue(id, out var cur) ? cur : st.cards[id] = new CardState();
                        if (id == "month")
                        {
                            AdGate.Buy(s, d.Cfg, "adventure_pass", now); // Thẻ Phiêu Lưu: quyền lợi cũ (cây ×1,5, khay AFK, rương 1 giờ)
                            cs.until = s.ent.passUntil;
                        }
                        else cs.until = Math.Max(now, cs.until) + (def?.days ?? 7) * Day;
                        outL.Add(new Reward { k = RewardKind.Perk, n = 1, id = id });
                        break;
                    }
                    case "no_ads":
                        AdGate.Buy(s, d.Cfg, "no_ads", now);
                        outL.Add(new Reward { k = RewardKind.Perk, n = 1, id = "no_ads" });
                        break;
                }
            }
            return outL;
        }

        // ---------- mua ----------

        static int PeriodOf(ShopPack p, double now) => p.daily ? Today(now) : p.weekly ? Week(Today(now)) : 0;

        public static int Bought(SaveData s, string id) => Of(s).bought.TryGetValue(id, out var n) ? n : 0;

        // còn mua được mấy lần (int.MaxValue: không giới hạn)
        public static int Left(SaveData s, ShopPack p, double now)
        {
            if (p.limit <= 0) return int.MaxValue;
            var st = Of(s);
            if (p.daily || p.weekly)
            {
                int key = PeriodOf(p, now);
                int n = st.periodKey.TryGetValue(p.id, out var k) && k == key && st.periodN.TryGetValue(p.id, out var c) ? c : 0;
                return Math.Max(0, p.limit - n);
            }
            return Math.Max(0, p.limit - Bought(s, p.id));
        }

        // gói thuộc nhóm chọn một mà người chơi đã mua một gói khác trong nhóm
        public static bool GroupTaken(SaveData s, ShopConfig c, ShopPack p)
        {
            if (p == null || string.IsNullOrEmpty(p.group)) return false;
            foreach (var q in c.packs)
                if (q.group == p.group && q.id != p.id && Bought(s, q.id) > 0) return true;
            return false;
        }

        public static bool CanBuy(SaveData s, GameData d, ShopPack p, double now)
        {
            if (p == null || Left(s, p, now) <= 0) return false;
            if (GroupTaken(s, d.Cfg.shop, p)) return false;
            if (p.kind == "noads" && AdGate.NoAds(s)) return false;
            if (p.kind == "piggy" && !PiggyCanBreak(s, d.Cfg.shop, now)) return false;
            if (p.kind == "fund" && Of(s).fund) return false;
            if (p.kind == "days" && Of(s).days.ContainsKey(p.id)) return false;
            return true;
        }

        static void Record(SaveData s, ShopPack p, double price, double now)
        {
            var st = Of(s);
            if (p != null)
            {
                st.bought[p.id] = Bought(s, p.id) + 1;
                if (p.daily || p.weekly)
                {
                    int key = PeriodOf(p, now);
                    int n = st.periodKey.TryGetValue(p.id, out var k) && k == key && st.periodN.TryGetValue(p.id, out var c) ? c : 0;
                    st.periodKey[p.id] = key;
                    st.periodN[p.id] = n + 1;
                }
            }
            if (price > 0)
            {
                st.spend.Add(new Spend { t = now, usd = price });
                st.spend.RemoveAll(x => x.t < now - 60 * Day);
            }
            st.offers.lastBuy = now;
        }

        // mua gói cố định (cửa hàng đã báo thành công). null nếu không mua được.
        public static List<Reward> BuyPack(SaveData s, GameData d, string id, double now, Rng rng)
        {
            var c = d.Cfg.shop;
            var p = c.Pack(id);
            if (!CanBuy(s, d, p, now)) return null;
            var st = Of(s);
            // nhóm chọn một: mua gói này thì ưu đãi đang mở của các gói còn lại trong nhóm đóng ngay
            if (!string.IsNullOrEmpty(p.group))
                foreach (var o in st.offers.active)
                    if (o.pack != null && o.pack != p.id && !o.bought && c.Pack(o.pack)?.group == p.group) o.until = now;
            List<Reward> got;
            switch (p.kind)
            {
                case "days":
                    st.days[p.id] = new DaysState { buyDay = Today(now), claimed = 0 };
                    got = ClaimDay(s, d, p.id, now, rng) ?? new List<Reward>();
                    break;
                case "fund":
                    st.fund = true;
                    got = new List<Reward> { new Reward { k = RewardKind.Perk, n = 1, id = "fund" } };
                    break;
                case "piggy":
                {
                    int n = (int)Math.Floor(st.piggy);
                    s.balls += n;
                    st.piggy = 0;
                    st.piggyBreaks++;
                    st.piggyAt = now;
                    st.piggyFullShown = false;
                    got = new List<Reward> { new Reward { k = RewardKind.Balls, n = n } };
                    break;
                }
                default:
                {
                    var items = Resolve(s, d, p.items, p.scale, null);
                    if (p.firstDouble && !st.firstDone.Contains(p.id))
                    {
                        st.firstDone.Add(p.id);
                        foreach (var it in items.Where(i => i.k == "balls")) it.n *= 2;
                    }
                    got = Grant(s, d, items, now, rng);
                    break;
                }
            }
            Record(s, p, p.price, now);
            return got;
        }

        // giá hiện (gói theo ngày đã mua thì không bán nữa)
        public static bool FirstBonus(SaveData s, ShopPack p) => p.firstDouble && !Of(s).firstDone.Contains(p.id);

        // ---------- gói nhận theo ngày (Quà Nhập Môn) ----------

        // ngày kế có nhận được hôm nay không
        public static bool DayClaimable(SaveData s, GameData d, string id, double now)
        {
            var p = d.Cfg.shop.Pack(id);
            if (p == null || !Of(s).days.TryGetValue(id, out var ds) || ds.claimed >= p.days.Count) return false;
            return Today(now) >= ds.buyDay + ds.claimed;
        }

        public static List<Reward> ClaimDay(SaveData s, GameData d, string id, double now, Rng rng)
        {
            if (!DayClaimable(s, d, id, now)) return null;
            var p = d.Cfg.shop.Pack(id);
            var ds = Of(s).days[id];
            var items = Resolve(s, d, p.days[ds.claimed].items, p.scale, null);
            ds.claimed++;
            return Grant(s, d, items, now, rng);
        }

        // ---------- thẻ tuần / tháng ----------

        public static PassCardDef CardOf(ShopConfig c, ShopPack p)
        {
            var it = p.items.FirstOrDefault(i => i.k == "week_card" || i.k == "month_card");
            return it == null ? null : c.Card(it.k == "week_card" ? "week" : "month");
        }

        public static bool CardActive(SaveData s, string id, double now)
        {
            if (id == "month") return AdGate.PassActive(s, now);
            return s.shop != null && s.shop.cards.TryGetValue(id, out var cs) && cs.until > now;
        }

        public static double CardUntil(SaveData s, string id) =>
            id == "month" ? s.ent?.passUntil ?? 0 : s.shop != null && s.shop.cards.TryGetValue(id, out var cs) ? cs.until : 0;

        public static bool CardClaimable(SaveData s, string id, double now)
        {
            if (!CardActive(s, id, now)) return false;
            var st = Of(s);
            var cs = st.cards.TryGetValue(id, out var cur) ? cur : st.cards[id] = new CardState { until = CardUntil(s, id) };
            return cs.lastDay < Today(now);
        }

        public static List<Reward> ClaimCard(SaveData s, GameData d, string id, double now, Rng rng)
        {
            if (!CardClaimable(s, id, now)) return null;
            var def = d.Cfg.shop.Card(id);
            Of(s).cards[id].lastDay = Today(now);
            return def == null ? new List<Reward>() : Grant(s, d, Resolve(s, d, def.daily, true, null), now, rng);
        }

        // sức chứa cây bi × (Thẻ Tuần)
        public static double TreeCapMult(SaveData s, ShopConfig c, double now) => CardActive(s, "week", now) ? c.Card("week")?.treeCap ?? 1 : 1;

        // Thẻ Phiêu Lưu: lượt quảng cáo trao ngay hôm nay còn không; dùng thì trừ
        public static bool UseAdSkip(SaveData s, ShopConfig c, double now)
        {
            if (!CardActive(s, "month", now)) return false;
            var st = Of(s);
            int day = Today(now);
            if (st.skipDay != day)
            {
                st.skipDay = day;
                st.skipUsed = 0;
            }
            if (st.skipUsed >= (c.Card("month")?.adSkips ?? 0)) return false;
            st.skipUsed++;
            return true;
        }

        // ---------- Lọ Bi ----------

        public static double PiggyCap(SaveData s, ShopConfig c) =>
            Math.Round(c.piggy.cap * Math.Min(c.piggy.maxMult, 1 + c.piggy.grow * Of(s).piggyBreaks) * c.Band(s.level));

        public static bool PiggyOpen(SaveData s) => Tutorial.CoreDone(s);
        public static bool PiggyFull(SaveData s, ShopConfig c) => Of(s).piggy >= PiggyCap(s, c);
        // đập được: đủ minPct sức chứa và đã qua gapDays từ lần đập trước. Không có thời gian chờ thì người thả nhiều bi đập liên tục
        // (giả lập: 28 lần một tháng), Lọ Bi rẻ gấp 5 lần gói bi nên gói bi thành thừa (GD_Claude/33 mục 2.5)
        public static bool PiggyCanBreak(SaveData s, ShopConfig c, double now) =>
            Of(s).piggy >= PiggyCap(s, c) * c.piggy.minPct && PiggyWait(s, c, now) <= 0;

        // còn bao lâu (ms) mới đập lại được; 0: không phải chờ
        public static double PiggyWait(SaveData s, ShopConfig c, double now)
        {
            double at = Of(s).piggyAt;
            return at <= 0 ? 0 : Math.Max(0, at + c.piggy.gapDays * Day - now);
        }

        // mỗi bi thả (đã tính cược) bỏ vào lọ; đầy thì thôi. Trả true khi vừa đầy.
        public static bool PiggyAdd(SaveData s, ShopConfig c, int balls)
        {
            if (!PiggyOpen(s) || balls <= 0) return false;
            var st = Of(s);
            double cap = PiggyCap(s, c);
            bool was = st.piggy >= cap;
            st.piggy = Math.Min(cap, st.piggy + balls);
            return !was && st.piggy >= cap;
        }

        // ---------- Chuỗi Quà ----------

        public static bool ChainLive(SaveData s, double now) => s.shop != null && s.shop.chainCycle >= 0 && s.shop.chainUntil > now;

        public static ChainDef ChainNow(SaveData s, ShopConfig c) =>
            c.chains.Count == 0 || s.shop == null || s.shop.chainCycle < 0 ? null : c.chains[s.shop.chainCycle % c.chains.Count];

        // mở đợt chuỗi mới (Offers gọi lúc vào game khi tới hạn)
        public static void ChainStart(SaveData s, ShopConfig c, double now)
        {
            var st = Of(s);
            st.chainCycle++;
            st.chainStep = 0;
            st.chainUntil = now + c.chainHours * Hour;
            st.chainNext = now + c.chainEveryDays * Day;
        }

        // nhận ô miễn phí kế, hoặc mua ô trả tiền kế (cửa hàng đã báo thành công). null nếu ô không phải ô kế hoặc sai loại.
        public static List<Reward> ChainTake(SaveData s, GameData d, int step, bool paid, double now, Rng rng)
        {
            var c = d.Cfg.shop;
            var def = ChainNow(s, c);
            var st = Of(s);
            if (def == null || !ChainLive(s, now) || step != st.chainStep || step >= def.steps.Count) return null;
            var cs = def.steps[step];
            if ((cs.price > 0) != paid) return null;
            st.chainStep++;
            if (paid) Record(s, null, cs.price, now);
            return Grant(s, d, Resolve(s, d, cs.items, true, null), now, rng);
        }

        // ---------- Quỹ Phiêu Lưu ----------

        public static bool FundClaimable(SaveData s, ShopConfig c, int i, bool paid) =>
            i >= 0 && i < c.fund.Count && s.level >= c.fund[i].lv && (paid ? Of(s).fund && !Of(s).fundPaid.Contains(i) : !Of(s).fundFree.Contains(i));

        public static List<Reward> FundClaim(SaveData s, GameData d, int i, bool paid, double now, Rng rng)
        {
            var c = d.Cfg.shop;
            if (!FundClaimable(s, c, i, paid)) return null;
            (paid ? Of(s).fundPaid : Of(s).fundFree).Add(i);
            return Grant(s, d, Resolve(s, d, paid ? c.fund[i].paid : c.fund[i].free, true, null), now, rng);
        }

        public static int FundReady(SaveData s, ShopConfig c) =>
            Enumerable.Range(0, c.fund.Count).Count(i => FundClaimable(s, c, i, false) || FundClaimable(s, c, i, true));

        // ---------- quà ngày, bảng mốc quảng cáo ----------

        public static bool GiftReady(SaveData s, double now) => Of(s).giftDay < Today(now);

        public static List<Reward> ClaimGift(SaveData s, GameData d, bool twice, double now, Rng rng)
        {
            if (!GiftReady(s, now)) return null;
            Of(s).giftDay = Today(now);
            var items = Resolve(s, d, d.Cfg.shop.dailyGift, true, null);
            if (twice)
                foreach (var it in items)
                    it.n *= 2;
            return Grant(s, d, items, now, rng);
        }

        static void RollAds(ShopState st, int day)
        {
            if (st.adDay == day) return;
            st.adDay = day;
            st.adCount = 0;
            st.adClaimed.Clear();
        }

        // một lượt quảng cáo xem xong (hoặc trao ngay nhờ Bỏ quảng cáo / Thẻ Phiêu Lưu)
        public static void OnAd(SaveData s, double now)
        {
            var st = Of(s);
            RollAds(st, Today(now));
            st.adCount++;
            st.offers.lastAd = now;
        }

        public static int AdsToday(SaveData s, double now)
        {
            var st = Of(s);
            RollAds(st, Today(now));
            return st.adCount;
        }

        public static bool AdMilestoneReady(SaveData s, ShopConfig c, int i, double now) =>
            i >= 0 && i < c.adMilestones.Count && AdsToday(s, now) >= c.adMilestones[i].n && !Of(s).adClaimed.Contains(i);

        public static List<Reward> ClaimAdMilestone(SaveData s, GameData d, int i, double now, Rng rng)
        {
            var c = d.Cfg.shop;
            if (!AdMilestoneReady(s, c, i, now)) return null;
            Of(s).adClaimed.Add(i);
            return Grant(s, d, Resolve(s, d, c.adMilestones[i].items, true, null), now, rng);
        }

        // ---------- nhóm người chơi, thang giá ----------

        public enum Segment { New, Free, Small, Mid, Big }

        public static double Spent(SaveData s, double now, double days) => s.shop == null ? 0 : s.shop.spend.Where(x => x.t >= now - days * Day).Sum(x => x.usd);

        public static bool EverPaid(SaveData s) => s.shop != null && s.shop.spend.Count > 0;

        public static Segment SegmentOf(SaveData s, double now)
        {
            if (!Tutorial.CoreDone(s) || (s.shop?.sessions ?? 0) <= 1) return Segment.New;
            if (s.shop == null || s.shop.spend.Count == 0) return Segment.Free;
            double m = Spent(s, now, 30);
            return m > 100 ? Segment.Big : m >= 20 ? Segment.Mid : Segment.Small;
        }

        // giá theo thang của người chơi (Travel Deal của Royal Match): mua thì lên một bậc, 7 ngày không mua thì xuống một bậc
        public static double LadderPrice(SaveData s, ShopConfig c, double now)
        {
            Decay(s, c, now);
            return c.ladder[Math.Min(c.ladder.Length - 1, Math.Max(0, Of(s).ladder))];
        }

        public static void Decay(SaveData s, ShopConfig c, double now)
        {
            var st = Of(s);
            if (st.ladder <= 0 || st.ladderAt <= 0) return;
            double gap = c.caps.ladderDownDays * Day;
            while (st.ladder > 0 && now - st.ladderAt > gap)
            {
                st.ladder--;
                st.ladderAt += gap;
            }
        }

        // mua một gói theo thang ở giá price: lên một bậc; mua lớn thì gói kế xuống một bậc
        public static void LadderBought(SaveData s, ShopConfig c, double price, double now)
        {
            var st = Of(s);
            int idx = Array.FindIndex(c.ladder, p => Math.Abs(p - price) < 0.005);
            if (idx < 0) idx = st.ladder;
            st.ladder = price >= c.caps.bigBuy ? Math.Max(0, idx - 1) : Math.Min(c.ladder.Length - 1, idx + 1);
            st.ladderAt = now;
        }

        // ---------- ưu đãi đang mở ----------

        public static IEnumerable<ActiveOffer> Live(SaveData s, double now) =>
            s.shop == null ? Enumerable.Empty<ActiveOffer>() : s.shop.offers.active.Where(o => !o.bought && (o.until <= 0 || o.until > now));

        public static ActiveOffer FindOffer(SaveData s, string uid) => s.shop?.offers.active.Find(o => o.uid == uid);

        // nội dung cụ thể của ưu đãi (gói cố định: theo gói)
        public static List<ShopItem> OfferItems(SaveData s, GameData d, ActiveOffer o)
        {
            if (o.pack == null) return o.items;
            var p = d.Cfg.shop.Pack(o.pack);
            if (p == null) return new List<ShopItem>();
            return p.kind == "days" ? p.days.SelectMany(x => Resolve(s, d, x.items, p.scale, null)).ToList() : Resolve(s, d, p.items, p.scale, o.hero);
        }

        public static double OfferMult(SaveData s, GameData d, ActiveOffer o) =>
            o.pack != null && d.Cfg.shop.Pack(o.pack) is ShopPack p ? PackMult(s, d, p) : Mult(d.Cfg.shop, d, o.items, o.price);

        // mua ưu đãi (cửa hàng đã báo thành công)
        public static List<Reward> BuyOffer(SaveData s, GameData d, string uid, double now, Rng rng)
        {
            var o = FindOffer(s, uid);
            if (o == null || o.bought || (o.until > 0 && o.until <= now)) return null;
            List<Reward> got;
            if (o.pack != null)
            {
                got = BuyPack(s, d, o.pack, now, rng);
                if (got == null) return null;
            }
            else
            {
                got = Grant(s, d, o.items, now, rng);
                Record(s, null, o.price, now);
            }
            o.bought = true;
            if (o.ladder) LadderBought(s, d.Cfg.shop, o.price, now);
            return got;
        }

        // dọn ưu đãi đã hết giờ hoặc đã mua quá 2 ngày
        public static void Prune(SaveData s, double now)
        {
            if (s.shop == null) return;
            s.shop.offers.active.RemoveAll(o => (o.until > 0 && o.until < now - 2 * Day) || (o.bought && o.created < now - 2 * Day));
        }

        // ---------- bản lưu ----------

        static List<object> WriteItems(List<ShopItem> items) =>
            items.Select(i => (object)new Dictionary<string, object> { ["k"] = i.k, ["n"] = i.n, ["h"] = i.h, ["r"] = i.r }).ToList();

        static List<ShopItem> ReadItems(object arr)
        {
            var list = new List<ShopItem>();
            foreach (var x in J.Arr(arr))
            {
                var o = J.Obj(x);
                if (o != null) list.Add(new ShopItem { k = J.Str(o, "k"), n = J.Int(o, "n", 1), h = J.Str(o, "h"), r = J.Int(o, "r", -1) });
            }
            return list;
        }

        static Dictionary<string, object> IntMap(Dictionary<string, int> m) => m.ToDictionary(kv => kv.Key, kv => (object)kv.Value);
        static Dictionary<string, object> NumMap(Dictionary<string, double> m) => m.ToDictionary(kv => kv.Key, kv => (object)kv.Value);

        static Dictionary<string, int> ReadIntMap(object o)
        {
            var m = new Dictionary<string, int>();
            foreach (var kv in J.Obj(o) ?? new Dictionary<string, object>())
                if (kv.Value is double v) m[kv.Key] = (int)v;
            return m;
        }

        static Dictionary<string, double> ReadNumMap(object o)
        {
            var m = new Dictionary<string, double>();
            foreach (var kv in J.Obj(o) ?? new Dictionary<string, object>())
                if (kv.Value is double v) m[kv.Key] = v;
            return m;
        }

        static List<object> Ints(IEnumerable<int> xs) => xs.Select(x => (object)x).ToList();
        static List<int> ReadInts(object arr) => J.Arr(arr).Where(x => x is double).Select(x => (int)(double)x).ToList();
        static List<string> ReadStrs(object arr) => J.Arr(arr).OfType<string>().ToList();

        public static Dictionary<string, object> Write(ShopState st)
        {
            var b = st.offers;
            return new Dictionary<string, object>
            {
                ["bought"] = IntMap(st.bought), ["periodKey"] = IntMap(st.periodKey), ["periodN"] = IntMap(st.periodN),
                ["firstDone"] = st.firstDone.Cast<object>().ToList(), ["items"] = IntMap(st.items), ["tickets"] = Ints(st.tickets),
                ["spend"] = st.spend.Select(x => (object)new Dictionary<string, object> { ["t"] = x.t, ["usd"] = x.usd }).ToList(),
                ["ladder"] = st.ladder, ["ladderAt"] = st.ladderAt, ["installAt"] = st.installAt, ["lastSeen"] = st.lastSeen, ["sessions"] = st.sessions,
                ["days"] = st.days.ToDictionary(kv => kv.Key, kv => (object)new Dictionary<string, object> { ["buyDay"] = kv.Value.buyDay, ["claimed"] = kv.Value.claimed }),
                ["cards"] = st.cards.ToDictionary(kv => kv.Key, kv => (object)new Dictionary<string, object> { ["until"] = kv.Value.until, ["lastDay"] = kv.Value.lastDay }),
                ["piggy"] = st.piggy, ["piggyAt"] = st.piggyAt, ["piggyBreaks"] = st.piggyBreaks, ["piggyFullShown"] = st.piggyFullShown,
                ["chainCycle"] = st.chainCycle, ["chainStep"] = st.chainStep, ["chainUntil"] = st.chainUntil, ["chainNext"] = st.chainNext,
                ["fund"] = st.fund, ["fundPaid"] = Ints(st.fundPaid), ["fundFree"] = Ints(st.fundFree),
                ["adDay"] = st.adDay, ["adCount"] = st.adCount, ["adClaimed"] = Ints(st.adClaimed),
                ["giftDay"] = st.giftDay, ["skipDay"] = st.skipDay, ["skipUsed"] = st.skipUsed,
                ["offers"] = new Dictionary<string, object>
                {
                    ["active"] = b.active.Select(o => (object)new Dictionary<string, object>
                    {
                        ["uid"] = o.uid, ["tpl"] = o.tpl, ["pack"] = o.pack, ["hero"] = o.hero, ["price"] = o.price, ["until"] = o.until, ["created"] = o.created,
                        ["items"] = WriteItems(o.items), ["bought"] = o.bought, ["ladder"] = o.ladder, ["popped"] = o.popped, ["warned"] = o.warned,
                    }).ToList(),
                    ["dismiss"] = IntMap(b.dismiss), ["dismissAt"] = NumMap(b.dismissAt),
                    ["autoDay"] = b.autoDay, ["autoCount"] = b.autoCount, ["muteDay"] = b.muteDay, ["flashDay"] = b.flashDay, ["flashCount"] = b.flashCount,
                    ["nearDay"] = b.nearDay, ["seenZones"] = b.seenZones, ["seq"] = b.seq,
                    ["lastAuto"] = b.lastAuto, ["lastBuy"] = b.lastBuy, ["lastAd"] = b.lastAd, ["lastFlash"] = b.lastFlash, ["lastRelief"] = b.lastRelief,
                    ["lastRefill"] = b.lastRefill, ["lossStage"] = b.lossStage, ["lossStreak"] = b.lossStreak, ["refillSeen"] = b.refillSeen,
                    ["seenOwned"] = b.seenOwned?.Cast<object>().ToList(), ["done"] = b.done.Cast<object>().ToList(),
                },
            };
        }

        public static ShopState Read(Dictionary<string, object> o)
        {
            if (o == null) return null;
            var st = new ShopState
            {
                bought = ReadIntMap(J.Get(o, "bought")), periodKey = ReadIntMap(J.Get(o, "periodKey")), periodN = ReadIntMap(J.Get(o, "periodN")),
                firstDone = ReadStrs(J.Get(o, "firstDone")), items = ReadIntMap(J.Get(o, "items")), tickets = J.Arr(o, "tickets").Where(x => x is double).Select(x => (int)(double)x).ToList(),
                ladder = J.Int(o, "ladder"), ladderAt = J.Num(o, "ladderAt"), installAt = J.Num(o, "installAt"), lastSeen = J.Num(o, "lastSeen"), sessions = J.Int(o, "sessions"),
                piggy = J.Num(o, "piggy"), piggyAt = J.Num(o, "piggyAt"), piggyBreaks = J.Int(o, "piggyBreaks"), piggyFullShown = J.Bool(o, "piggyFullShown"),
                chainCycle = J.Int(o, "chainCycle", -1), chainStep = J.Int(o, "chainStep"), chainUntil = J.Num(o, "chainUntil"), chainNext = J.Num(o, "chainNext"),
                fund = J.Bool(o, "fund"), fundPaid = ReadInts(J.Get(o, "fundPaid")), fundFree = ReadInts(J.Get(o, "fundFree")),
                adDay = J.Int(o, "adDay", -1), adCount = J.Int(o, "adCount"), adClaimed = ReadInts(J.Get(o, "adClaimed")),
                giftDay = J.Int(o, "giftDay", -1), skipDay = J.Int(o, "skipDay", -1), skipUsed = J.Int(o, "skipUsed"),
            };
            // túi cũ: Rương Tướng → trứng Khá, Rương Tướng Vàng → trứng Sử thi (2026-11-23)
            foreach (var old in new[] { HeroChest, GoldChest })
                if (st.items.TryGetValue(old, out var n))
                {
                    st.items.Remove(old);
                    if (n > 0) st.AddItem(Eggs.Key(Norm(new ShopItem { k = old }).r), n);
                }
            foreach (var x in J.Arr(o, "spend"))
                if (J.Obj(x) is Dictionary<string, object> so) st.spend.Add(new Spend { t = J.Num(so, "t"), usd = J.Num(so, "usd") });
            foreach (var kv in J.Obj(o, "days") ?? new Dictionary<string, object>())
                if (J.Obj(kv.Value) is Dictionary<string, object> dso) st.days[kv.Key] = new DaysState { buyDay = J.Int(dso, "buyDay"), claimed = J.Int(dso, "claimed") };
            foreach (var kv in J.Obj(o, "cards") ?? new Dictionary<string, object>())
                if (J.Obj(kv.Value) is Dictionary<string, object> cso) st.cards[kv.Key] = new CardState { until = J.Num(cso, "until"), lastDay = J.Int(cso, "lastDay", -1) };
            var bo = J.Obj(o, "offers");
            if (bo != null)
            {
                var b = st.offers;
                foreach (var x in J.Arr(bo, "active"))
                {
                    var ao = J.Obj(x);
                    if (ao == null) continue;
                    b.active.Add(new ActiveOffer
                    {
                        uid = J.Str(ao, "uid"), tpl = J.Str(ao, "tpl"), pack = J.Str(ao, "pack"), hero = J.Str(ao, "hero"), price = J.Num(ao, "price"),
                        until = J.Num(ao, "until"), created = J.Num(ao, "created"), items = ReadItems(J.Get(ao, "items")), bought = J.Bool(ao, "bought"),
                        ladder = J.Bool(ao, "ladder"), popped = J.Bool(ao, "popped"), warned = J.Bool(ao, "warned"),
                    });
                }
                b.dismiss = ReadIntMap(J.Get(bo, "dismiss"));
                b.dismissAt = ReadNumMap(J.Get(bo, "dismissAt"));
                b.autoDay = J.Int(bo, "autoDay");
                b.autoCount = J.Int(bo, "autoCount");
                b.muteDay = J.Int(bo, "muteDay", -1);
                b.flashDay = J.Int(bo, "flashDay");
                b.flashCount = J.Int(bo, "flashCount");
                b.nearDay = J.Int(bo, "nearDay", -1);
                b.seenZones = J.Int(bo, "seenZones", -1);
                b.seq = J.Int(bo, "seq");
                b.lastAuto = J.Num(bo, "lastAuto");
                b.lastBuy = J.Num(bo, "lastBuy");
                b.lastAd = J.Num(bo, "lastAd");
                b.lastFlash = J.Num(bo, "lastFlash");
                b.lastRelief = J.Num(bo, "lastRelief");
                b.lastRefill = J.Num(bo, "lastRefill");
                b.lossStage = J.Int(bo, "lossStage");
                b.lossStreak = J.Int(bo, "lossStreak");
                b.refillSeen = J.Bool(bo, "refillSeen");
                b.seenOwned = J.Get(bo, "seenOwned") is List<object> so ? so.OfType<string>().ToList() : null;
                b.done = ReadStrs(J.Get(bo, "done"));
            }
            return st;
        }
    }
}
