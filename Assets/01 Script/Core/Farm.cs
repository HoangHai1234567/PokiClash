// Trang trại (chép Web/src/core/farm.ts): 8 chỗ làm, mỗi chỗ hợp một hệ. Đồng hồ theo đoạn (giờ máy lùi thì bỏ qua đoạn đó, như AFK):
// mỗi chỗ trừ sức và cộng bi theo năng suất, kho chặn ở 12 giờ sản lượng; rút tướng thì tướng nghỉ; thu hoạch lấy phần nguyên, giữ phần lẻ;
// tự xếp chọn cặp (chỗ trống, tướng rảnh) năng suất cao nhất. Sức làm tách khỏi trận.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class FarmSpot
    {
        public string hero; // null = trống
        public double energy; // giờ làm còn lại của ca
        public double stock; // bi tích (số thực)
    }

    public sealed class FarmState
    {
        public double lastTick, boostUntil;
        public List<FarmSpot> spots = new List<FarmSpot>();
        public Dictionary<string, double> rest = new Dictionary<string, double>(); // tướng → hết nghỉ lúc (ms)
    }

    public static class Farm
    {
        const double H = 3600000;

        public static FarmState Fresh(BalanceConfig cfg, double now)
        {
            var f = new FarmState { lastTick = now };
            for (int i = 0; i < cfg.farm.spots.Count; i++) f.spots.Add(new FarmSpot());
            return f;
        }

        public static FarmState Of(SaveData s, BalanceConfig cfg, double now) => s.farm ?? (s.farm = Fresh(cfg, now));

        public static bool Open(SaveData s, BalanceConfig cfg) => s.heroes.Values.Count(h => h.owned) >= cfg.farm.minHeroes;
        public static int SpotsOpen(BalanceConfig cfg, int level) => cfg.farm.openSpots + cfg.farm.spotLevels.Count(l => level >= l);
        // cấp mở chỗ i (0 nếu mở ngay)
        public static int SpotLevel(BalanceConfig cfg, int i) => i < cfg.farm.openSpots ? 0 : cfg.farm.spotLevels[i - cfg.farm.openSpots];

        // bi mỗi giờ của tướng ở chỗ i
        public static double Rate(SaveData s, GameData d, string hero, int i)
        {
            var c = d.Cfg.farm;
            var h = d.Hero(hero);
            double r = c.@base * c.rarityPower[(int)h.rarity] * (1 + c.lvStep * (s.level - 1)) * (1 + c.starStep * (s.Hero(hero).star - 1));
            if (h.elem == c.spots[i].elem) r *= c.match;
            return r;
        }

        public static double Hours(SaveData s, GameData d, string hero)
        {
            var c = d.Cfg.farm;
            return c.durBase + c.durStar * (s.Hero(hero).star - 1) + c.durRarity * (int)d.Hero(hero).rarity;
        }

        public static double RestMin(SaveData s, GameData d, string hero)
        {
            var c = d.Cfg.farm;
            return Math.Min(c.restMax, Math.Max(c.restMin, Hours(s, d, hero) * c.restPerHour));
        }

        // tính tới now; false nếu giờ máy bị lùi (bỏ qua đoạn đó)
        public static bool Tick(SaveData s, GameData d, double now)
        {
            var c = d.Cfg.farm;
            var f = Of(s, d.Cfg, now);
            if (now < f.lastTick)
            {
                f.lastTick = now;
                return false;
            }
            double dt = (now - f.lastTick) / H;
            for (int i = 0; i < f.spots.Count; i++)
            {
                var sp = f.spots[i];
                if (sp.hero == null || sp.energy <= 0) continue;
                double work = Math.Min(dt, sp.energy);
                double boosted = Math.Max(0, Math.Min(f.lastTick + work * H, f.boostUntil) - f.lastTick) / H;
                double rate = Rate(s, d, sp.hero, i);
                sp.energy -= work;
                sp.stock = Math.Min(rate * c.capHours, sp.stock + rate * (work + boosted * (c.boostMult - 1)));
            }
            foreach (var k in f.rest.Where(kv => kv.Value <= now).Select(kv => kv.Key).ToList()) f.rest.Remove(k);
            f.lastTick = now;
            return true;
        }

        public static int Working(FarmState f, string hero) => f.spots.FindIndex(sp => sp.hero == hero);
        public static double RestLeft(FarmState f, string hero, double now) => Math.Max(0, (f.rest.TryGetValue(hero, out var t) ? t : 0) - now);
        public static bool Free(SaveData s, FarmState f, string hero, double now) =>
            s.Hero(hero) != null && s.Hero(hero).owned && Working(f, hero) < 0 && RestLeft(f, hero, now) <= 0;

        public static bool Place(SaveData s, GameData d, double now, int i, string hero)
        {
            Tick(s, d, now);
            var f = Of(s, d.Cfg, now);
            if (i >= SpotsOpen(d.Cfg, s.level) || f.spots[i].hero != null || !Free(s, f, hero, now)) return false;
            f.spots[i].hero = hero;
            f.spots[i].energy = Hours(s, d, hero);
            return true;
        }

        // rút tướng: tướng nghỉ theo công thức (rút giữa ca vẫn nghỉ đủ); bi tích vẫn ở chỗ
        public static bool Remove(SaveData s, GameData d, double now, int i)
        {
            Tick(s, d, now);
            var f = Of(s, d.Cfg, now);
            var sp = f.spots[i];
            if (sp.hero == null) return false;
            f.rest[sp.hero] = now + RestMin(s, d, sp.hero) * 60000;
            sp.hero = null;
            sp.energy = 0;
            return true;
        }

        // thu hoạch: lấy phần nguyên của mọi chỗ, giữ phần lẻ
        public static int Harvest(SaveData s, GameData d, double now)
        {
            Tick(s, d, now);
            int total = 0;
            foreach (var sp in Of(s, d.Cfg, now).spots)
            {
                int n = (int)Math.Floor(sp.stock);
                sp.stock -= n;
                total += n;
            }
            s.balls += total;
            return total;
        }

        public static int Stock(SaveData s, GameData d, double now)
        {
            Tick(s, d, now);
            return Of(s, d.Cfg, now).spots.Sum(sp => (int)Math.Floor(sp.stock));
        }

        // tự xếp: lặp chọn cặp (chỗ trống, tướng rảnh) có năng suất cao nhất
        public static List<(int spot, string hero)> Auto(SaveData s, GameData d, double now)
        {
            Tick(s, d, now);
            var f = Of(s, d.Cfg, now);
            var placed = new List<(int, string)>();
            while (true)
            {
                int bi = -1;
                string bh = null;
                double br = 0;
                for (int i = 0; i < SpotsOpen(d.Cfg, s.level); i++)
                {
                    if (f.spots[i].hero != null) continue;
                    foreach (var h in d.Heroes)
                    {
                        if (!Free(s, f, h.id, now)) continue;
                        double r = Rate(s, d, h.id, i);
                        if (bh == null || r > br)
                        {
                            bi = i;
                            bh = h.id;
                            br = r;
                        }
                    }
                }
                if (bh == null) break;
                Place(s, d, now, bi, bh);
                placed.Add((bi, bh));
            }
            return placed;
        }

        public static bool Boosting(FarmState f, double now) => f.boostUntil > now;

        // năng suất ×2 trong boostH giờ (sau khi xem quảng cáo farm_boost); không chồng khi đang tăng
        public static bool Boost(SaveData s, GameData d, double now)
        {
            Tick(s, d, now);
            var f = Of(s, d.Cfg, now);
            if (f.boostUntil > now) return false;
            f.boostUntil = now + d.Cfg.farm.boostH * H;
            return true;
        }

        // chấm báo ở sảnh: có tướng hết sức hoặc kho đầy (hoặc vừa mở mà chưa đặt tướng nào)
        public static bool Alert(SaveData s, GameData d, double now)
        {
            if (!Open(s, d.Cfg)) return false;
            if (s.farm == null) return true;
            Tick(s, d, now);
            var f = s.farm;
            for (int i = 0; i < f.spots.Count; i++)
            {
                var sp = f.spots[i];
                if (sp.hero != null && (sp.energy <= 0 || sp.stock >= Rate(s, d, sp.hero, i) * d.Cfg.farm.capHours)) return true;
            }
            return false;
        }

        // bảng thử: giả như đã trôi qua ms
        public static void Travel(SaveData s, double ms)
        {
            var f = s.farm;
            if (f == null) return;
            f.lastTick -= ms;
            if (f.boostUntil != 0) f.boostUntil -= ms;
            foreach (var k in f.rest.Keys.ToList()) f.rest[k] -= ms;
        }
    }
}
