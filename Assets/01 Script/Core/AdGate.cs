// Cổng quảng cáo thưởng (chép Web/src/core/ads.ts): đếm lượt theo chỗ đặt trong ngày theo giờ máy, ngày mới thì đặt lại,
// giờ máy lùi về ngày trước thì giữ nguyên số đã dùng (không mở lại lượt). Quyền lợi gói: Thẻ Phiêu Lưu (hạn), Bỏ quảng cáo (cờ).
// Nguyên tắc: không bán bi, đá tiềm năng hay lượt quay máy bi.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    public sealed class AdState
    {
        public int day;
        public Dictionary<string, int> used = new Dictionary<string, int>();
    }

    public sealed class Entitlements
    {
        public double passUntil; // ms: hết Thẻ Phiêu Lưu
        public bool noAds;
    }

    public static class AdGate
    {
        public const int Unlimited = 999;
        public const string TreeDouble = "tree_double", AfkChestOpen = "afk_chest_open", AfkBoost = "afk_boost", FarmBoost = "farm_boost", CaveExtra = "cave_extra";

        public static AdState Of(SaveData s) => s.ads ?? (s.ads = new AdState());

        static AdState Roll(SaveData s, int day)
        {
            var a = Of(s);
            if (day > a.day)
            {
                a.day = day;
                a.used.Clear();
            }
            return a;
        }

        public static int Limit(BalanceConfig cfg, string p) => cfg.ads.limits.Find(x => x.p == p)?.n ?? 0;
        public static int Used(SaveData s, int day, string p) => Roll(s, day).used.TryGetValue(p, out var n) ? n : 0;

        public static int Left(SaveData s, BalanceConfig cfg, int day, string p)
        {
            int lim = Limit(cfg, p);
            return lim > 0 ? lim - Used(s, day, p) : Unlimited;
        }

        public static bool Use(SaveData s, BalanceConfig cfg, int day, string p)
        {
            if (Left(s, cfg, day, p) <= 0) return false;
            var a = Roll(s, day);
            a.used[p] = (a.used.TryGetValue(p, out var n) ? n : 0) + 1;
            return true;
        }

        public static Entitlements Ent(SaveData s) => s.ent ?? (s.ent = new Entitlements());
        public static bool PassActive(SaveData s, double now) => s.ent != null && s.ent.passUntil > now;
        public static bool NoAds(SaveData s) => s.ent != null && s.ent.noAds;

        // mua (cửa hàng đã báo thành công): Thẻ Phiêu Lưu cộng dồn hạn; Bỏ quảng cáo một lần
        public static bool Buy(SaveData s, BalanceConfig cfg, string id, double now)
        {
            var e = Ent(s);
            if (id == "adventure_pass")
            {
                e.passUntil = Math.Max(now, e.passUntil) + cfg.ads.pass.days * 86400000.0;
                return true;
            }
            if (id == "no_ads" && !e.noAds)
            {
                e.noAds = true;
                return true;
            }
            return false;
        }
    }
}
