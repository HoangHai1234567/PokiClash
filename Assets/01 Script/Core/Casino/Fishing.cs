// Câu cá (Bến câu, GD_Claude/29_DaoCasino.md mục 6.2). Lõi chọn cá, mồi, Sổ Cá, Cá Vua, bán cá, cần câu; giao diện làm phần quăng
// (lực 0..1), chờ phao, giật (biteWindow giây), kéo (thanh căng với vùng xanh Zone, cá vùng theo pull của độ hiếm).
// - Mồi: freeBait mồi miễn phí mỗi ngày, rồi mồi mua / thưởng (CasinoState.bait). Không hồi theo giờ.
// - Chỗ câu mở theo cấp cần câu; độ hiếm theo trọng số của chỗ, quăng càng xa càng nặng về hiếm; loài "night" chỉ cắn 19 giờ – 5 giờ;
//   hệ may mắn hôm nay (Bói sao) nặng gấp đôi.
// - Cá Vua: mỗi tuần một con (kings theo tuần), chỉ ở chỗ cuối, cần câu từ kingRod; gọi một tướng phụ kéo: tướng khắc hệ cá thì vùng xanh
//   to thêm kingAssist.
// - Bắt lần đầu một loài: bi first[độ hiếm]; đủ 6 loài một hệ: setShards mảnh tướng hệ đó + cúp câu cá cho Nhà.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class FishBite
    {
        public FishDef fish;
        public double size;
        public bool king;
        public int spot;
        public double wait; // giây chờ phao chìm
        public double pull; // độ vùng vẫy
    }

    public sealed class FishCatch
    {
        public FishDef fish;
        public double size;
        public bool first, record, king;
        public List<Reward> rewards = new List<Reward>();
        public Elem? setDone; // vừa đủ 6 loài của hệ này
    }

    public static class Fishing
    {
        static FishingConfig C(GameData d) => Casino.C(d).fishing;

        public static int FreeLeft(SaveData s, GameData d, double now) => Math.Max(0, C(d).freeBait - Casino.Roll(s, d, now).freeBaitUsed);

        public static int BaitLeft(SaveData s, GameData d, double now) => FreeLeft(s, d, now) + Casino.Of(s).bait;

        public static FishRod Rod(SaveData s, GameData d) => C(d).rods[Math.Max(0, Math.Min(Casino.Of(s).rod, C(d).rods.Count) - 1)];

        public static int Spots(SaveData s, GameData d) => Math.Min(C(d).spots.Count, Rod(s, d).spots);

        // giá lên cấp cần câu kế (−1 nếu đã tối đa)
        public static int RodCost(SaveData s, GameData d)
        {
            int next = Casino.Of(s).rod; // chỉ số 0-based của cấp kế
            return next >= C(d).rods.Count ? -1 : Shop.RoundBalls(C(d).rods[next].cost * Casino.Band(s, d));
        }

        public static bool UpgradeRod(SaveData s, GameData d)
        {
            int cost = RodCost(s, d);
            if (cost < 0 || !Casino.Spend(s, cost)) return false;
            Casino.Of(s).rod++;
            return true;
        }

        public static int BaitCost(SaveData s, GameData d) => Shop.RoundBalls(C(d).baitPrice * Casino.Band(s, d));

        public static bool BuyBait(SaveData s, GameData d)
        {
            if (!Casino.Spend(s, BaitCost(s, d))) return false;
            Casino.Of(s).bait += C(d).baitPack;
            return true;
        }

        public static FishDef KingOf(GameData d, double now)
        {
            var k = C(d).kings;
            return k.Count == 0 ? null : k[((Casino.Week(Casino.Today(now)) % k.Count) + k.Count) % k.Count];
        }

        public static bool KingAvailable(SaveData s, GameData d, int spot, double now) =>
            KingOf(d, now) != null && spot == C(d).spots.Count - 1 && Casino.Of(s).rod >= C(d).kingRod
            && Casino.Of(s).kingWeek != Casino.Week(Casino.Today(now));

        // trọng số độ hiếm ở chỗ spot với lực quăng power (0..1)
        public static double[] RarWeights(FishingConfig c, int spot, double power)
        {
            var w = (double[])c.spots[spot].rar.Clone();
            for (int k = 0; k < w.Length; k++) w[k] *= 1 + c.farBonus * Math.Max(0, Math.Min(1, power)) * k / 4.0;
            return w;
        }

        // chọn cá (không đụng bản lưu)
        public static FishBite Pick(FishingConfig c, int spot, double power, bool night, Elem? lucky, bool kingOk, FishDef king, Rng rng)
        {
            if (kingOk && king != null && rng.Chance(c.kingChance))
                return new FishBite { fish = king, king = true, spot = spot, size = Size(king, rng), wait = rng.Range(2.5, 4.5), pull = c.pull[c.pull.Length - 1] * 1.25 };
            var w = RarWeights(c, spot, power);
            for (int guard = 0; guard < 10; guard++)
            {
                int k = Weighted(w, rng);
                var cand = c.fish.Where(f => (int)f.rar == k && (night || !f.night)).ToList();
                if (cand.Count == 0)
                {
                    w[k] = 0;
                    if (w.All(x => x <= 0)) break;
                    continue;
                }
                var f = rng.Weighted(cand, x => lucky.HasValue && x.elem == lucky.Value ? 2.0 : 1.0);
                return new FishBite { fish = f, spot = spot, size = Size(f, rng), wait = rng.Range(1.2, 3.5), pull = c.pull[Math.Min((int)f.rar, c.pull.Length - 1)] };
            }
            var any = c.fish[0];
            return new FishBite { fish = any, spot = spot, size = Size(any, rng), wait = 2, pull = c.pull[0] };
        }

        static int Weighted(double[] w, Rng rng)
        {
            double tot = w.Sum(), x = rng.Next() * tot;
            for (int i = 0; i < w.Length; i++)
            {
                x -= w[i];
                if (x < 0) return i;
            }
            return w.Length - 1;
        }

        // cỡ: lệch về nhỏ (con to hiếm hơn)
        public static double Size(FishDef f, Rng rng) => Math.Round(f.min + (f.max - f.min) * Math.Pow(rng.Next(), 1.6), 1);

        // vùng xanh (phần thanh): theo cần câu; Cá Vua có tướng phụ khắc hệ cá thì to thêm
        public static double Zone(SaveData s, GameData d, FishBite b, string assist)
        {
            double z = Rod(s, d).zone;
            if (b != null && b.king && assist != null)
            {
                var h = d.Hero(assist);
                if (h != null && Elements.Beats(h.elem) == b.fish.elem) z *= 1 + C(d).kingAssist;
            }
            return z;
        }

        // quăng: tốn một mồi (miễn phí trước); null nếu hết mồi / chỗ chưa mở
        public static FishBite Cast(SaveData s, GameData d, int spot, double power, double now, Rng rng, out string why)
        {
            why = null;
            var c = C(d);
            if (!Casino.Unlocked(s, d, Casino.Fishing)) { why = Casino.Need(s, d, Casino.Fishing); return null; }
            if (spot < 0 || spot >= Spots(s, d)) { why = Loc.T("Nâng cần câu để câu chỗ này"); return null; }
            var st = Casino.Roll(s, d, now);
            if (FreeLeft(s, d, now) > 0) st.freeBaitUsed++;
            else if (st.bait > 0) st.bait--;
            else { why = Loc.T("Hết mồi"); return null; }
            return Pick(c, spot, power, Casino.Night(now), Casino.LuckyActive(s, now), KingAvailable(s, d, spot, now), KingOf(d, now), rng);
        }

        // lượt câu đầu đời: chắc chắn trúng một con Thường ở gần bờ (hướng dẫn người mới)
        public static FishBite FirstCast(SaveData s, GameData d, double now, Rng rng)
        {
            var c = C(d);
            var st = Casino.Roll(s, d, now);
            if (FreeLeft(s, d, now) > 0) st.freeBaitUsed++;
            var f = c.fish.FirstOrDefault(x => x.rar == Rarity.Common && !x.night) ?? c.fish[0];
            return new FishBite { fish = f, spot = 0, size = Size(f, rng), wait = 1.5, pull = c.pull[0] * 0.6 };
        }

        // kéo được cá: Sổ Cá, giỏ cá, thưởng lần đầu, đủ bộ hệ, Cá Vua
        public static FishCatch Land(SaveData s, GameData d, FishBite b, double now, Rng rng)
        {
            var c = C(d);
            var st = Casino.Roll(s, d, now);
            var res = new FishCatch { fish = b.fish, size = b.size, king = b.king };
            if (!st.dex.TryGetValue(b.fish.id, out var rec)) st.dex[b.fish.id] = rec = new FishRec();
            res.first = rec.n == 0;
            res.record = b.size > rec.best;
            rec.n++;
            rec.best = Math.Max(rec.best, b.size);
            Casino.Track(s, d, "fish", 1, now);
            if (b.fish.rar >= Rarity.Rare) Casino.Track(s, d, "fish_rare", 1, now);
            if (b.king)
            {
                st.kingWeek = Casino.Week(Casino.Today(now));
                res.rewards.AddRange(Casino.Grant(s, d, c.king.Select(x => Elemize(x, b.fish.elem)).ToList(), now, rng));
                return res;
            }
            st.creel.Add(new CaughtFish { id = b.fish.id, size = b.size });
            if (res.first)
            {
                int bi = c.first[Math.Min((int)b.fish.rar, c.first.Length - 1)];
                res.rewards.AddRange(Casino.Grant(s, d, new List<CasinoItem> { new CasinoItem { k = "balls", n = bi } }, now, rng));
                string ek = Keys.Of(b.fish.elem);
                if (!st.sets.Contains(ek) && c.fish.Where(f => f.elem == b.fish.elem).All(f => st.dex.ContainsKey(f.id)))
                {
                    st.sets.Add(ek);
                    res.setDone = b.fish.elem;
                    res.rewards.AddRange(Casino.Grant(s, d, new List<CasinoItem> { new CasinoItem { k = "shards", n = c.setShards, h = "*elem:" + ek } }, now, rng));
                    if (s.home != null && !string.IsNullOrEmpty(d.Cfg.home.fishDeco)) Home.Bag(s.home, d.Cfg.home.fishDeco, 1);
                }
            }
            return res;
        }

        static CasinoItem Elemize(CasinoItem x, Elem e) =>
            x.h == "*elem" ? new CasinoItem { k = x.k, n = x.n, h = "*elem:" + Keys.Of(e), r = x.r, chance = x.chance } : x;

        // ---------- bán ----------

        public static int Price(GameData d, CaughtFish f)
        {
            var c = C(d);
            var def = c.Fish(f.id);
            if (def == null) return 0;
            double t = def.max > def.min ? (f.size - def.min) / (def.max - def.min) : 0;
            return (int)Math.Round(c.price[Math.Min((int)def.rar, c.price.Length - 1)] * (0.8 + 0.7 * Math.Max(0, Math.Min(1, t))));
        }

        public static int CreelValue(SaveData s, GameData d) =>
            Shop.RoundBalls(Casino.Of(s).creel.Sum(f => Price(d, f)) * Casino.Band(s, d)) * (Casino.Of(s).creel.Count > 0 ? 1 : 0);

        public static int SellCreel(SaveData s, GameData d)
        {
            int v = CreelValue(s, d);
            if (v <= 0) return 0;
            s.balls += v;
            Casino.Of(s).creel.Clear();
            return v;
        }

        public static int Caught(SaveData s, Elem? e = null, GameData d = null) =>
            Casino.Of(s).dex.Count(kv => kv.Value.n > 0 && (e == null || d?.Cfg.casino.fishing.fish.Find(f => f.id == kv.Key)?.elem == e));
    }
}
