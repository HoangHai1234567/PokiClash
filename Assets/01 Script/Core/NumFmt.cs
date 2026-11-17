// Số gọn để hiện (người dùng dặn 2026-11-17): chỉ số, lực chiến từ 1000 trở lên ghi theo k / M, dấu chấm thập phân như ví dụ "3.3k".
//   999 -> "999", 1000 -> "1k", 3300 -> "3.3k", 57640 -> "57.6k", 602579 -> "603k", 1434603 -> "1.43M", 25600000 -> "25.6M"
// Chỉ dùng cho chữ hiện ra; trận và bản lưu vẫn giữ số đủ. Số nguyên dưới 1000 giữ nguyên (TeamPower.Text vẫn dùng cho số cần đủ).
using System;
using System.Globalization;

namespace PokiClash.Core
{
    public static class NumFmt
    {
        static readonly CultureInfo Inv = CultureInfo.InvariantCulture;

        public static string Short(double v)
        {
            if (double.IsNaN(v) || double.IsInfinity(v)) return "0";
            if (v < 0) return "-" + Short(-v);
            v = Math.Round(v);
            if (v < 1000) return v.ToString("0", Inv);
            if (v < 100_000) return Trim(Math.Floor(v / 100) / 10) + "k"; // 1 chữ số thập phân, cắt xuống để 999.9k không nhảy thành 1000k
            if (v < 1_000_000) return Math.Floor(v / 1000).ToString("0", Inv) + "k";
            if (v < 10_000_000) return Trim(Math.Floor(v / 10_000) / 100) + "M";
            if (v < 1_000_000_000) return Trim(Math.Floor(v / 100_000) / 10) + "M";
            return Trim(Math.Floor(v / 10_000_000) / 100) + "B";
        }

        public static string Short(int v) => Short((double)v);

        static string Trim(double x) => x.ToString("0.##", Inv);
    }
}
