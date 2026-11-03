// Cây bi trên sảnh (chép Web/src/core/trees.ts): mỗi cây ra perHour bi mỗi giờ, chứa tối đa cap, đầy thì ngừng; hái là lấy phần nguyên
// của mọi cây, giữ phần lẻ. Đồng hồ theo đoạn như AFK: giờ máy lùi thì bỏ qua đoạn đó. Cây mới mở bắt đầu từ lần tính sau khi mở.
// Thẻ Phiêu Lưu: tốc độ và sức chứa ×treeMult (đoạn có thẻ tính riêng; hết thẻ thì cây đang chứa quá mức thường giữ nguyên, ngừng ra).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class TreeState
    {
        public double lastTick;
        public List<double> stock = new List<double>(); // bi đang có ở từng cây đã mở
    }

    public static class Trees
    {
        const double H = 3600000;

        public static int Open(SaveData s, BalanceConfig cfg)
        {
            if (Progress.TotalCleared(s) == 0) return 0;
            return 1 + cfg.trees.unlockZones.Count(z => Progress.ZoneDone(s, z));
        }

        public static TreeState Of(SaveData s, double now) => s.trees ?? (s.trees = new TreeState { lastTick = now });

        static double Mult(SaveData s, BalanceConfig cfg, double now) => AdGate.PassActive(s, now) ? cfg.ads.pass.treeMult : 1;
        public static double Cap(SaveData s, BalanceConfig cfg, double now) => cfg.trees.cap * Mult(s, cfg, now);
        public static double Rate(SaveData s, BalanceConfig cfg, double now) => cfg.trees.perHour * Mult(s, cfg, now);

        static void Grow(TreeState t, TreesConfig c, double hours, double m)
        {
            for (int i = 0; i < t.stock.Count; i++)
                if (t.stock[i] < c.cap * m) t.stock[i] = Math.Min(c.cap * m, t.stock[i] + c.perHour * m * hours);
        }

        // tính tới now; false nếu giờ máy bị lùi
        public static bool Tick(SaveData s, BalanceConfig cfg, double now)
        {
            var t = Of(s, now);
            if (now < t.lastTick)
            {
                t.lastTick = now;
                return false;
            }
            double until = s.ent?.passUntil ?? 0;
            double passEnd = Math.Min(now, until);
            if (passEnd > t.lastTick) Grow(t, cfg.trees, (passEnd - t.lastTick) / H, cfg.ads.pass.treeMult);
            double from = Math.Max(t.lastTick, until);
            if (now > from) Grow(t, cfg.trees, (now - from) / H, 1);
            int n = Open(s, cfg);
            while (t.stock.Count < n) t.stock.Add(0);
            t.lastTick = now;
            return true;
        }

        // bi hái được ngay (phần nguyên)
        public static int Stock(SaveData s, BalanceConfig cfg, double now)
        {
            Tick(s, cfg, now);
            return Of(s, now).stock.Sum(x => (int)Math.Floor(x));
        }

        // hái mọi cây (× mult khi xem quảng cáo "Hái ×2"): lấy phần nguyên, giữ phần lẻ
        public static int Harvest(SaveData s, BalanceConfig cfg, double now, int mult = 1)
        {
            Tick(s, cfg, now);
            var t = Of(s, now);
            int n = 0;
            for (int i = 0; i < t.stock.Count; i++)
            {
                int k = (int)Math.Floor(t.stock[i]);
                t.stock[i] -= k;
                n += k;
            }
            s.balls += n * mult;
            return n * mult;
        }

        // chấm báo ở sảnh: có cây đã đầy
        public static bool Full(SaveData s, BalanceConfig cfg, double now)
        {
            Tick(s, cfg, now);
            double cap = Cap(s, cfg, now);
            return Of(s, now).stock.Any(x => x >= cap);
        }

        // bảng thử: giả như đã trôi qua ms
        public static void Travel(SaveData s, double ms)
        {
            if (s.trees != null) s.trees.lastTick -= ms;
        }
    }
}
