// AFK: ải đã qua tự đánh khi người chơi vắng, ra mảnh tướng boss (tỉ lệ thấp) và rương AFK. Chép Web/src/core/afk.ts.
// Bi thụ động đến từ cây bi (Trees.cs).
// Đồng hồ theo đoạn: mỗi lần tính cộng phần giờ mới từ afk.lastTick; phần nằm trong đoạn tăng tốc tính ×2;
// giờ hiệu dụng chặn ở afkCapH tới khi nhận; giờ máy lùi thì bỏ qua đoạn đó.
// Cứ chestEveryH giờ hiệu dụng ra 1 rương AFK (khay tối đa chestSlots); rương đầu khay đếm chestOpenH giờ rồi mở được,
// mở xong (hoặc tới giờ) thì rương kế đếm tiếp. Thẻ Phiêu Lưu: khay 5 ô, rương mở trong 1 giờ.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    public struct AfkPending
    {
        public double hours;
        public bool full;
    }

    public sealed class AfkClaim
    {
        public double hours;
        public List<ShardResult> shards = new List<ShardResult>();
    }

    public static class Afk
    {
        const double H = 3600000;

        // ngày theo giờ máy (đặt lại lượt quảng cáo lúc 0 giờ): tzMin = số phút lệch so với UTC (+420 ở Việt Nam)
        public static int LocalDay(double now, double tzMin) => (int)Math.Floor((now + tzMin * 60000) / 86400000);

        public static int Today(double now) =>
            LocalDay(now, TimeZoneInfo.Local.GetUtcOffset(DateTimeOffset.FromUnixTimeMilliseconds((long)now).UtcDateTime).TotalMinutes);

        // số ô khay và giờ mở rương (Thẻ Phiêu Lưu đổi cả hai)
        public static int Slots(SaveData s, BalanceConfig cfg, double now) => AdGate.PassActive(s, now) ? cfg.ads.pass.afkSlots : cfg.afk.chestSlots;
        public static double OpenH(SaveData s, BalanceConfig cfg, double now) => AdGate.PassActive(s, now) ? cfg.ads.pass.afkOpenH : cfg.afk.chestOpenH;

        // rương đã đủ giờ dồn mà khay còn chỗ: vào khay lúc at
        static void Flush(AfkState a, AfkConfig c, double at, int slots)
        {
            if (a.chestAcc >= c.chestEveryH && a.chests.Count < slots)
            {
                a.chests.Add(at);
                a.chestAcc = 0;
            }
        }

        // cộng giờ hiệu dụng trong đoạn [from, to] với hệ số r; dừng khi đầy giờ; ra rương đúng lúc dồn đủ
        static void Advance(AfkState a, AfkConfig c, double cap, double from, double to, double r, int slots)
        {
            double t = from;
            while (t < to)
            {
                double room = cap - a.hours;
                if (room <= 0) return;
                double avail = (to - t) / H * r;
                double toChest = a.chests.Count >= slots ? double.PositiveInfinity : c.chestEveryH - a.chestAcc;
                double gain = Math.Min(Math.Min(avail, room), toChest);
                a.hours += gain;
                a.chestAcc = Math.Min(c.chestEveryH, a.chestAcc + gain);
                t += gain / r * H;
                if (gain == toChest)
                {
                    a.chests.Add(t);
                    a.chestAcc = 0;
                    continue;
                }
                return; // hết đoạn hoặc đầy giờ
            }
        }

        // tính tới now; trả false nếu giờ máy bị lùi (đoạn đó bỏ qua, đồng hồ tính tiếp từ now)
        public static bool Tick(SaveData s, BalanceConfig cfg, double now)
        {
            var a = s.afk;
            var c = cfg.afk;
            if (now < a.lastTick)
            {
                a.lastTick = now;
                return false;
            }
            if (Progress.TotalCleared(s) == 0)
            {
                a.lastTick = now;
                return true;
            }
            int slots = Slots(s, cfg, now);
            Flush(a, c, a.lastTick, slots);
            double boostEnd = Math.Min(now, a.boostUntil);
            if (boostEnd > a.lastTick) Advance(a, c, cfg.afkCapH, a.lastTick, boostEnd, c.boostMult, slots);
            double from = Math.Max(a.lastTick, a.boostUntil);
            if (now > from) Advance(a, c, cfg.afkCapH, from, now, 1, slots);
            a.lastTick = now;
            return true;
        }

        public static AfkPending Pending(SaveData s, BalanceConfig cfg, double now)
        {
            Tick(s, cfg, now);
            double hours = s.afk.hours;
            return new AfkPending { hours = hours, full = hours >= cfg.afkCapH };
        }

        // nhận mảnh (× mult): mỗi giờ tròn một lần thử
        public static AfkClaim Claim(SaveData s, GameData d, double now, int mult, Rng rng)
        {
            var p = Pending(s, d.Cfg, now);
            var r = new AfkClaim { hours = p.hours };
            var pool = Progress.AfkBossPool(s, d);
            for (int h = 0; h < Math.Floor(p.hours); h++)
                if (pool.Count > 0 && rng.Chance(d.Cfg.afk.shardChance)) r.shards.Add(Progress.AddShards(s, d, rng.Pick(pool), 1 * mult, rng));
            s.afk.hours = 0;
            s.afkSince = (long)now;
            return r;
        }

        // giờ bắt đầu đếm và giờ mở được của từng rương trong khay
        public static List<(double start, double ready)> ChestTimes(SaveData s, BalanceConfig cfg, double now)
        {
            var a = s.afk;
            double prev = a.chainAt, openH = OpenH(s, cfg, now);
            var list = new List<(double, double)>();
            foreach (var at in a.chests)
            {
                double start = Math.Max(at, prev);
                prev = start + openH * H;
                list.Add((start, prev));
            }
            return list;
        }

        public static int ReadyChests(SaveData s, BalanceConfig cfg, double now)
        {
            int n = 0;
            foreach (var t in ChestTimes(s, cfg, now)) if (t.ready <= now) n++;
            return n;
        }

        // mở rương đầu khay; early: "Mở ngay" (đã xem quảng cáo) khi chưa tới giờ. Chưa tới giờ mà không early thì null.
        public static List<Reward> OpenChest(SaveData s, GameData d, double now, Rng rng, bool early = false)
        {
            Tick(s, d.Cfg, now);
            var a = s.afk;
            if (a.chests.Count == 0) return null;
            var t = ChestTimes(s, d.Cfg, now)[0];
            if (now < t.ready && !early) return null;
            a.chainAt = Math.Min(now, t.ready);
            a.chests.RemoveAt(0);
            Flush(a, d.Cfg.afk, now, Slots(s, d.Cfg, now));
            return Pachinko.RollChest(s, d, d.Cfg.afk.chest, 1, rng);
        }

        public static bool Boosting(SaveData s, double now) => s.afk.boostUntil > now;

        // bật tăng tốc ×2 trong boostH giờ (không chồng khi đang tăng tốc)
        public static bool Boost(SaveData s, BalanceConfig cfg, double now)
        {
            Tick(s, cfg, now);
            if (s.afk.boostUntil > now) return false;
            s.afk.boostUntil = now + cfg.afk.boostH * H;
            return true;
        }

        // bảng thử: giả như đã trôi qua ms (lùi mọi mốc giờ đã lưu)
        public static void Travel(SaveData s, double ms)
        {
            var a = s.afk;
            s.afkSince -= (long)ms;
            a.lastTick -= ms;
            if (a.boostUntil != 0) a.boostUntil -= ms;
            if (a.chainAt != 0) a.chainAt -= ms;
            for (int i = 0; i < a.chests.Count; i++) a.chests[i] -= ms;
        }
    }
}
