// AFK: đội tự đánh một ải đã qua khi người chơi vắng, ra mảnh tướng của ải đó (tỉ lệ thấp) và rương AFK. Chép Web/src/core/afk.ts.
// AFK theo ải (người dùng chọn 2026-11-03, Unity khác web): người chơi chọn ải đã thắng ("AFK ải này" ở hộp chuẩn bị trận); chưa
// chọn thì đội AFK ở ải xa nhất đã qua có rơi mảnh. Mỗi giờ tròn shardChance ra 1 mảnh, tướng bốc theo tỉ lệ rơi của ải
// (bỏ tướng tặng). Đổi ải thì mảnh của các giờ tròn đã dồn tính theo ải cũ và nhận luôn, phần lẻ giữ lại.
// Bi thụ động đến từ cây bi (Trees.cs).
// Đồng hồ theo đoạn: mỗi lần tính cộng phần giờ mới từ afk.lastTick; phần nằm trong đoạn tăng tốc tính ×2;
// giờ hiệu dụng chặn ở afkCapH tới khi nhận; giờ máy lùi thì bỏ qua đoạn đó.
// Cứ chestEveryH giờ hiệu dụng ra 1 rương AFK (khay tối đa chestSlots); rương đầu khay đếm chestOpenH giờ rồi mở được,
// mở xong (hoặc tới giờ) thì rương kế đếm tiếp. Thẻ Phiêu Lưu: khay 5 ô, rương mở trong 1 giờ.
using System;
using System.Collections.Generic;
using System.Linq;

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
        public int stage; // ải đội đã AFK (0: chưa qua ải nào)
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

        // ---------- ải AFK ----------

        // tướng rơi mảnh khi AFK ở ải st: các dòng rơi của ải, bỏ tướng tặng (trùng tướng thì lấy dòng đầu)
        public static List<StageDrop> Pool(StageDef st)
        {
            var outL = new List<StageDrop>();
            if (st == null) return outL;
            foreach (var dr in st.drops)
                if (!dr.gift && dr.chance > 0 && !outL.Exists(x => x.hero == dr.hero)) outL.Add(dr);
            return outL;
        }

        // ải đội đang AFK: ải đã chọn (còn hợp lệ), không thì ải xa nhất đã qua có rơi mảnh (đảo sau trước, ải sau trước);
        // không ải nào rơi mảnh thì ải xa nhất đã qua; chưa qua ải nào thì null
        public static StageDef Stage(SaveData s, GameData d)
        {
            var picked = d.Stage(s.afk.stage);
            if (picked != null && Progress.StageCleared(s, picked)) return picked;
            StageDef far = null;
            foreach (var z in d.Zones.OrderByDescending(z => z.order))
                foreach (var st in d.ZoneStages(z.id).Where(x => x.idx <= s.zones[(int)z.id]).OrderByDescending(x => x.idx))
                {
                    if (Pool(st).Count > 0) return st;
                    far ??= st;
                }
            return far;
        }

        // ải st đang được AFK do người chơi chọn (không tính ải tự chọn)
        public static bool Picked(SaveData s, StageDef st) => st != null && s.afk.stage == st.id && Progress.StageCleared(s, st);

        // mỗi giờ tròn một lần thử ra 1 mảnh (× mult) của một tướng trong bể ải AFK, bốc theo tỉ lệ rơi
        static void Roll(SaveData s, GameData d, AfkClaim r, int hours, int mult, Rng rng)
        {
            var pool = Pool(d.Stage(r.stage));
            for (int h = 0; h < hours; h++)
                if (pool.Count > 0 && rng.Chance(d.Cfg.afk.shardChance))
                    r.shards.Add(Progress.AddShards(s, d, rng.Weighted(pool, x => x.chance).hero, 1 * mult, rng));
        }

        // nhận mảnh (× mult) của ải đang AFK
        public static AfkClaim Claim(SaveData s, GameData d, double now, int mult, Rng rng)
        {
            var p = Pending(s, d.Cfg, now);
            var r = new AfkClaim { hours = p.hours, stage = Stage(s, d)?.id ?? 0 };
            Roll(s, d, r, (int)Math.Floor(p.hours), mult, rng);
            s.afk.hours = 0;
            s.afkSince = (long)now;
            return r;
        }

        // chọn ải AFK (phải đã qua): ải khác ải đang AFK thì mảnh của các giờ tròn đã dồn tính theo ải cũ, nhận luôn, giữ phần lẻ.
        // Trả null nếu ải chưa qua.
        public static AfkClaim SetStage(SaveData s, GameData d, int stageId, double now, Rng rng)
        {
            var st = d.Stage(stageId);
            if (st == null || !Progress.StageCleared(s, st)) return null;
            Tick(s, d.Cfg, now);
            var r = new AfkClaim { stage = Stage(s, d)?.id ?? 0 };
            if (r.stage != stageId)
            {
                int whole = (int)Math.Floor(s.afk.hours);
                r.hours = whole;
                Roll(s, d, r, whole, 1, rng);
                s.afk.hours -= whole;
            }
            s.afk.stage = stageId;
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
