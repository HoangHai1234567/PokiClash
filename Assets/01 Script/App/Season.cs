// Mùa trong game (người dùng 2026-11-27: "tạo ra các mùa cho game, hiện đang là mùa đông giáng sinh"). Mùa chọn theo ngày trên máy,
// mỗi mùa là một khoảng ngày lặp lại hằng năm (bảng Table). Mùa bật phần trang trí ở sảnh (HubSeason: tuyết rơi, tuyết phủ đảo, ông già
// Noel bay ngang) và bài nhạc sảnh riêng (AudioService.MusicFor → HubMusic). Thêm mùa mới: thêm SeasonId, một dòng Table, phần trang trí
// trong HubSeason và bài "sanh_<mùa>".
// Thử: menu "PokiClash/Thử/Mùa/..." ghi PlayerPrefs DevKey (không có hoặc -1: theo ngày; 0: không mùa; 1: Noel).
using System;
using UnityEngine;

namespace PokiClash
{
    public enum SeasonId
    {
        None = 0,
        Noel = 1, // mùa đông Giáng sinh
    }

    public static class Season
    {
        public const string DevKey = "dev_season";

        // (mùa, tháng bắt đầu, ngày bắt đầu, tháng kết thúc, ngày kết thúc), tính cả hai đầu; qua năm mới được (tháng 11 → tháng 1)
        static readonly (SeasonId id, int m0, int d0, int m1, int d1)[] Table =
        {
            (SeasonId.Noel, 11, 20, 1, 6),
        };

        public static SeasonId Current
        {
            get
            {
                int dev = PlayerPrefs.GetInt(DevKey, -1);
                return dev >= 0 ? (SeasonId)dev : ByDate(DateTime.Now);
            }
        }

        public static SeasonId ByDate(DateTime t)
        {
            int v = t.Month * 100 + t.Day;
            foreach (var s in Table)
            {
                int a = s.m0 * 100 + s.d0, b = s.m1 * 100 + s.d1;
                if (a <= b ? v >= a && v <= b : v >= a || v <= b) return s.id;
            }
            return SeasonId.None;
        }

        // khoá nhạc sảnh theo mùa (bài chưa nạp thì AudioService lùi về "sanh")
        public static string HubMusic => Current == SeasonId.Noel ? "sanh_noel" : "sanh";

        // nhạc màn tải lúc mở game: trong mùa phát luôn bài sảnh của mùa (màn tải đi thẳng vào sảnh, nhạc nối liền); ngoài mùa: chủ đề chính
        public static string LoadMusic => Current == SeasonId.Noel ? "sanh_noel" : "chude";

        // khoá nhạc gốc của một bài theo mùa ("sanh_noel" → "sanh"); bài thường trả nguyên
        public static string BaseMusic(string key) => key != null && key.EndsWith("_noel") ? key.Substring(0, key.Length - 5) : key;
    }
}
