// Trứng capsule (người dùng 2026-11-23: "phần rương đổi sang dạng trứng capsule đi để dễ hiểu hơn ... chia trứng theo tier thường hiếm...
// như những tướng trong game"; GD_Claude/26 mục 13). Thay Rương Tướng / Rương Tướng Vàng: 5 bậc trùng độ hiếm tướng (Thường, Khá, Hiếm,
// Sử thi, Huyền thoại); trứng bậc nào nở mảnh một tướng bậc đó (min–max mảnh), có chút cơ hội nở lên một bậc (up, như Starr Drop đổi
// màu). Món trong gói: { k: "egg", r: bậc }; trong túi: khoá egg_<bậc>. Chọn tướng trong bậc như Rương Tướng cũ: ownedBias phần là
// tướng đang có / đang góp mảnh, tướng tuần ×featuredMult. Hai rương cũ (hero_chest, gold_chest) đọc thành trứng Khá / Sử thi (Shop.Norm).
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace PokiClash.Core
{
    // một quả đã nở: bậc trứng lúc đầu, bậc sau khi nở (có thể lên một bậc), thưởng mảnh
    public sealed class Hatch
    {
        public int from, tier;
        public Reward reward;
        public bool Up => tier > from;
    }

    public static class Eggs
    {
        public const string Item = "egg";
        public const int Tiers = 5;

        public static string Key(int tier) => "egg_" + Math.Max(0, Math.Min(Tiers - 1, tier));

        public static int TierOf(string key) =>
            key != null && key.StartsWith("egg_", StringComparison.Ordinal) && int.TryParse(key.Substring(4), out var t) && t >= 0 && t < Tiers ? t : -1;

        public static int Bag(SaveData s, int tier) => Shop.Of(s).Item(Key(tier));
        public static int BagTotal(SaveData s) => Enumerable.Range(0, Tiers).Sum(t => Bag(s, t));

        public static string PickHero(SaveData s, GameData d, Rarity r, List<string> featured, Rng rng)
        {
            var c = d.Cfg.shop;
            var all = d.Heroes.Where(h => h.rarity == r).ToList();
            if (all.Count == 0) all = d.Heroes.ToList();
            var going = all.Where(h => s.Hero(h.id).owned || s.Hero(h.id).shards > 0).ToList();
            var pool = going.Count > 0 && rng.Chance(c.ownedBias) ? going : all;
            return rng.Weighted(pool, h => featured != null && featured.Contains(h.id) ? c.featuredMult : 1).id;
        }

        // nở n quả bậc tier. fromBag: lấy trong túi (thiếu thì nở số có được); false: trứng không qua túi (quảng cáo).
        public static List<Hatch> Open(SaveData s, GameData d, int tier, int n, bool fromBag, double now, Rng rng)
        {
            var outL = new List<Hatch>();
            var c = d.Cfg.shop;
            if (tier < 0 || tier >= Tiers || n <= 0) return outL;
            var st = Shop.Of(s);
            if (fromBag)
            {
                n = Math.Min(n, st.Item(Key(tier)));
                st.AddItem(Key(tier), -n);
            }
            var featured = Shop.FeaturedNow(d, now);
            for (int i = 0; i < n; i++)
            {
                var def = c.Egg(tier);
                int t = tier;
                if (def != null && t < Tiers - 1 && rng.Chance(def.up)) t++;
                var got = c.Egg(t) ?? def;
                var hero = PickHero(s, d, (Rarity)t, featured, rng);
                int min = got?.min ?? 12, max = Math.Max(min, got?.max ?? 16);
                int count = rng.Int(min, max);
                outL.Add(new Hatch
                {
                    from = tier, tier = t,
                    reward = new Reward { k = RewardKind.Shards, n = count, hero = hero, res = Progress.AddShards(s, d, hero, count, rng) },
                });
            }
            return outL;
        }

        // bảng tỉ lệ công khai (nút "Tỉ lệ", Apple 3.1.1 / Google Play)
        public static string OddsText(GameData d, double now)
        {
            var c = d.Cfg.shop;
            var sb = new StringBuilder();
            foreach (var e in c.eggs.OrderBy(x => x.tier))
            {
                sb.Append("<b>").Append(e.Name).Append("</b>: ")
                    .Append(Loc.F("{0}–{1} mảnh một tướng {2}", e.min, e.max, Elements.RarityName((Rarity)e.tier)));
                if (e.up > 0 && e.tier < Tiers - 1)
                    sb.Append(Loc.F(" · {0}% nở lên {1}", (e.up * 100).ToString("0.#"), Elements.RarityName((Rarity)(e.tier + 1))));
                sb.Append('\n');
            }
            var feat = Shop.FeaturedNow(d, now).Select(h => d.Hero(h)?.name).Where(x => x != null);
            sb.Append(Loc.F("Tướng tuần (tỉ lệ ×{0} trong bậc của mình): {1}.", c.featuredMult, string.Join(", ", feat))).Append('\n');
            sb.Append(Loc.F("Trong một bậc: {0}% ra tướng bạn đang có hoặc đang góp mảnh, còn lại chia đều.", Math.Round(c.ownedBias * 100)));
            return sb.ToString();
        }
    }
}
