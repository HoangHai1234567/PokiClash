// Chợ đen (GD_Claude/29_DaoCasino.md mục 6.4): đổi với lái buôn (game không máy chủ, không đổi giữa người chơi).
// - `slots` ô hàng, đổi mới ở các mốc giờ `periods` (giờ máy); ban đêm thêm `nightSlots` ô hàng đêm. Làm mới sớm tốn bi theo `refresh`
//   (theo số lần trong ngày, hết mảng là hết lượt).
// - Giá = giá gốc "bi quy đổi" của cửa hàng (ShopConfig.value) × mark × bậc cấp; bait, mystery có giá cố định (× bậc cấp).
// - Mảnh tướng: tướng đã có hoặc đã có mảnh, từ độ hiếm `rar` trở lên; không may rủi (biết trước tướng nào, bao nhiêu mảnh).
// - Túi hàng lậu: bảng `mystery` (công bố tỉ lệ), mở bằng Pachinko.RollChest.
// - Thu mua: cá trong giỏ (Fishing.SellCreel), bản sao thẻ thừa (thẻ đã tối đa cấp) đổi đá tiềm năng (copyPerStone bản một đá, trần stoneDaily mỗi ngày).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class MkSlot
    {
        public int idx;
        public MarketOffer offer;
        public List<ShopItem> items = new List<ShopItem>(); // rỗng với mystery
        public int price;
        public bool bought;
        public bool night;
        public string deco; // home: mã trang trí Nhà
    }

    public static class BlackMarket
    {
        static MarketConfig C(GameData d) => Casino.C(d).market;

        public static int Period(GameData d, double now)
        {
            var p = C(d).periods;
            double h = Casino.Hour(now);
            int k = 0;
            for (int i = 0; i < p.Length; i++) if (h >= p[i]) k = i;
            return k;
        }

        public static int Stamp(GameData d, double now) => Casino.Today(now) * Math.Max(1, C(d).periods.Length) + Period(d, now);

        // mili giây tới lần đổi hàng kế
        public static double NextRefresh(GameData d, double now)
        {
            var p = C(d).periods;
            double h = Casino.Hour(now);
            double next = p.Where(x => x > h).Select(x => (double)x).DefaultIfEmpty(24 + (p.Length > 0 ? p[0] : 0)).First();
            return (next - h) * 3600000.0;
        }

        static void Sync(SaveData s, GameData d, double now)
        {
            var st = Casino.Roll(s, d, now);
            int stamp = Stamp(d, now);
            if (st.mkStamp != stamp)
            {
                st.mkStamp = stamp;
                st.mkRoll = 0;
                st.mkBought.Clear();
            }
            if (st.mkRefreshDay != Casino.Today(now))
            {
                st.mkRefreshDay = Casino.Today(now);
                st.mkRefresh = 0;
            }
        }

        // tướng cho ô mảnh: đã có (còn lên được sao) hoặc đã có mảnh, độ hiếm từ r trở lên
        static List<string> ShardHeroes(SaveData s, GameData d, Rarity r) =>
            d.Heroes.Where(h => !h.minion && h.rarity >= r)
                .Where(h => { var p = s.Hero(h.id); return p != null && ((p.owned && p.star < StarTier.MaxStar) || (!p.owned && p.shards > 0)); })
                .Select(h => h.id).OrderBy(x => x, StringComparer.Ordinal).ToList();

        static int PriceOf(SaveData s, GameData d, MarketOffer o, List<ShopItem> items)
        {
            double band = Casino.Band(s, d);
            if (o.price > 0) return Shop.RoundBalls(o.price * band);
            return Shop.RoundBalls(Shop.Value(d.Cfg.shop, d, items) * o.mark * band);
        }

        static MkSlot Make(SaveData s, GameData d, MarketOffer o, int idx, Rng rng)
        {
            var sl = new MkSlot { idx = idx, offer = o, night = o.night };
            switch (o.kind)
            {
                case "shards":
                {
                    var pool = ShardHeroes(s, d, o.rar);
                    if (pool.Count == 0) pool = ShardHeroes(s, d, Rarity.Common);
                    if (pool.Count == 0) return null;
                    sl.items.Add(new ShopItem { k = "shards", n = o.n, h = rng.Pick(pool) });
                    break;
                }
                case "copies":
                {
                    var owned = d.Heroes.Where(h => !h.minion && s.Hero(h.id)?.owned == true).Select(h => h.id).OrderBy(x => x, StringComparer.Ordinal).ToList();
                    if (owned.Count == 0) return null;
                    sl.items.Add(new ShopItem { k = "copies", n = o.n, h = rng.Pick(owned) });
                    break;
                }
                case "evo":
                case "crystal":
                case "stones":
                case "balls":
                    sl.items.Add(new ShopItem { k = o.kind, n = o.n });
                    break;
                case Casino.Bait:
                case "mystery":
                    break;
                case "home":
                {
                    // trang trí Nhà (mục 6.4 "Đồ Nhà"): chỉ khi đã mở Nhà; mỗi lượt hàng một món trong danh sách
                    if (s.home == null || !Home.Open(s, d.Cfg)) return null;
                    var defs = o.defs.Where(x => d.Cfg.home.Def(x) != null).ToList();
                    if (defs.Count == 0) return null;
                    sl.deco = rng.Pick(defs);
                    break;
                }
                default:
                    return null;
            }
            sl.price = o.kind == Casino.Bait || o.kind == "home" ? Shop.RoundBalls(Math.Max(1, o.price) * Casino.Band(s, d)) : PriceOf(s, d, o, sl.items);
            return sl;
        }

        // hàng đang bày (tất định theo lượt hàng, số lần làm mới, ngày đêm)
        public static List<MkSlot> Stock(SaveData s, GameData d, double now)
        {
            Sync(s, d, now);
            var st = Casino.Of(s);
            var c = C(d);
            var rng = new Rng((uint)(st.mkStamp * 2654435761u + (uint)st.mkRoll * 40503u + 7));
            var outL = new List<MkSlot>();
            void Fill(IList<MarketOffer> pool, int n)
            {
                var left = pool.ToList();
                int guard = 0;
                while (outL.Count < n && left.Count > 0 && guard++ < 50)
                {
                    var o = rng.Weighted(left, x => x.w);
                    if (o.kind == "evo" || o.kind == "crystal" || o.kind == "mystery" || o.kind == Casino.Bait || o.kind == "home") left.Remove(o); // tối đa 1 ô mỗi loại này
                    var sl = Make(s, d, o, outL.Count, rng);
                    if (sl == null) { left.Remove(o); continue; }
                    outL.Add(sl);
                }
            }
            Fill(c.offers.Where(o => !o.night).ToList(), c.slots);
            if (Casino.Night(now)) Fill(c.offers.Where(o => o.night).ToList(), c.slots + c.nightSlots);
            foreach (var sl in outL) sl.bought = st.mkBought.Contains(sl.idx);
            return outL;
        }

        // giá làm mới sớm (−1: hết lượt hôm nay)
        public static int RefreshCost(SaveData s, GameData d, double now)
        {
            Sync(s, d, now);
            var r = C(d).refresh;
            int k = Casino.Of(s).mkRefresh;
            return k < r.Length ? Shop.RoundBalls(r[k] * Casino.Band(s, d)) : -1;
        }

        public static bool Refresh(SaveData s, GameData d, double now)
        {
            int cost = RefreshCost(s, d, now);
            if (cost < 0 || !Casino.Spend(s, cost)) return false;
            var st = Casino.Of(s);
            st.mkRefresh++;
            st.mkRoll++;
            st.mkBought.Clear();
            return true;
        }

        public static List<Reward> Buy(SaveData s, GameData d, int idx, double now, Rng rng, out string why)
        {
            why = null;
            if (!Casino.Unlocked(s, d, Casino.Market)) { why = Casino.Need(s, d, Casino.Market); return null; }
            var sl = Stock(s, d, now).Find(x => x.idx == idx);
            if (sl == null) { why = Loc.T("Hàng đã đổi"); return null; }
            if (sl.bought) { why = Loc.T("Đã mua"); return null; }
            if (!Casino.Spend(s, sl.price)) { why = Loc.T("Không đủ bi"); return null; }
            Casino.Of(s).mkBought.Add(idx);
            Casino.Track(s, d, "market_buy", 1, now);
            if (sl.offer.kind == Casino.Bait)
                return Casino.Grant(s, d, new List<CasinoItem> { new CasinoItem { k = Casino.Bait, n = sl.offer.n } }, now, rng);
            if (sl.offer.kind == "mystery") return OpenMystery(s, d, rng);
            if (sl.offer.kind == "home")
            {
                Home.Bag(s.home, sl.deco, Math.Max(1, sl.offer.n));
                return new List<Reward> { new Reward { k = RewardKind.Deco, n = Math.Max(1, sl.offer.n), id = sl.deco } };
            }
            return Shop.Grant(s, d, sl.items, now, rng);
        }

        // mở Túi hàng lậu: giá túi nhân bậc cấp nên bi trong túi cũng nhân bậc cấp (không thì càng lên cấp túi càng lỗ)
        public static List<Reward> OpenMystery(SaveData s, GameData d, Rng rng)
        {
            var r = Pachinko.RollChest(s, d, new ChestTable { kind = "casino_mystery", rolls = C(d).mystery }, 1, rng);
            double band = Casino.Band(s, d);
            foreach (var x in r)
            {
                if (x.k != RewardKind.Balls || band <= 1) continue;
                int extra = Shop.RoundBalls(x.n * band) - x.n;
                if (extra <= 0) continue;
                s.balls += extra;
                x.n += extra;
            }
            return r;
        }

        public static int MysteryPrice(SaveData s, GameData d)
        {
            var o = C(d).offers.Find(x => x.kind == "mystery");
            return o == null ? 0 : Shop.RoundBalls(Math.Max(1, o.price) * Casino.Band(s, d));
        }

        // ---------- thu mua ----------

        public static int SpareCopies(SaveData s, GameData d)
        {
            int n = 0;
            foreach (var kv in s.heroes)
            {
                if (!kv.Value.owned) continue;
                foreach (var slot in Progress.Slots)
                {
                    var cp = kv.Value.Card(slot);
                    if (cp.lv >= d.Cfg.cardMax) n += cp.copies;
                }
            }
            return n;
        }

        // số đá tiềm năng đổi được ngay từ thẻ thừa: copyPerStone bản một đá, không quá phần trần còn lại hôm nay
        public static int SpareValue(SaveData s, GameData d, double now) =>
            Math.Min(SpareCopies(s, d) / Math.Max(1, C(d).copyPerStone), SpareStonesLeft(s, d, now));

        public static int SpareStonesLeft(SaveData s, GameData d, double now) => Math.Max(0, C(d).stoneDaily - Casino.Roll(s, d, now).spareStones);

        // đổi thẻ thừa lấy đá tiềm năng; trả số đá. Chỉ trừ đúng số bản đã đổi (theo thứ tự tướng trong dữ liệu), phần lẻ và phần quá
        // trần giữ lại cho hôm sau. KHÔNG đổi ra bi: bi thả ra lại ra thẻ và trứng, thành vòng lặp tự nuôi (GD_Claude/33 mục 2.1)
        public static int SellSpare(SaveData s, GameData d, double now)
        {
            int stones = SpareValue(s, d, now);
            if (stones <= 0) return 0;
            int need = stones * Math.Max(1, C(d).copyPerStone);
            foreach (var h in d.Heroes)
            {
                var hp = s.Hero(h.id);
                if (hp == null || !hp.owned) continue;
                foreach (var slot in Progress.Slots)
                {
                    var cp = hp.Card(slot);
                    if (need <= 0 || cp.lv < d.Cfg.cardMax || cp.copies <= 0) continue;
                    int take = Math.Min(cp.copies, need);
                    cp.copies -= take;
                    need -= take;
                }
            }
            s.potentialStones += stones;
            Casino.Of(s).spareStones += stones;
            return stones;
        }

        // tỉ lệ Túi hàng lậu (để hiện)
        public static List<(ChestRoll roll, double p)> MysteryOdds(GameData d)
        {
            var m = C(d).mystery;
            double tot = m.Sum(r => r.w);
            return m.Select(r => (r, tot > 0 ? r.w / tot : 0)).ToList();
        }
    }
}
