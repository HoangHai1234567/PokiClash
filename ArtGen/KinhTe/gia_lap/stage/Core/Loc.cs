// Đa ngôn ngữ (2026-11-21): tiếng Việt là gốc và chính là khoá. Bảng của ngôn ngữ khác (Assets/Resources/Loc/<mã>/*.json,
// mỗi file một object phẳng { "chuỗi Việt": "bản dịch" }) do Game/Data/LocService nạp rồi gọi Loc.Use.
//   Loc.T("Mở ngay")              chữ cố định
//   Loc.F("Ải {0} · {1}", idx, n) chữ có chỗ điền (string.Format, bản dịch được đổi thứ tự {1} {0})
// Tiếng Việt (mặc định, test, golden): T trả nguyên chuỗi. Thiếu bản dịch thì giữ tiếng Việt và báo OnMiss (bản dev ghi lại).
// Tên có số đuôi ("Ruộng Bậc Thang 3") tra phần chữ rồi gắn lại số; khoảng trắng hai đầu ("Cấp ") giữ nguyên.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    public static class Loc
    {
        public const string Vi = "vi", En = "en";

        public static string Lang { get; private set; } = Vi;
        public static bool IsEn => Lang == En;

        static Dictionary<string, string> table = new Dictionary<string, string>();

        // chuỗi chưa dịch (chỉ báo chuỗi có dấu tiếng Việt)
        public static Action<string> OnMiss;

        public static void Use(string lang, Dictionary<string, string> t)
        {
            Lang = string.IsNullOrEmpty(lang) ? Vi : lang;
            table = Lang == Vi || t == null ? new Dictionary<string, string>() : t;
        }

        public static void UseVi() => Use(Vi, null);

        public static string T(string vi)
        {
            if (Lang == Vi || string.IsNullOrEmpty(vi)) return vi;
            if (Find(vi, out var s)) return s;
            if (LooksVi(vi)) OnMiss?.Invoke(vi);
            return vi;
        }

        public static string F(string viFormat, params object[] args) => string.Format(T(viFormat), args);

        // tra bản dịch, không báo thiếu (quét chữ trong prefab: nhiều chữ là số, tên riêng không cần dịch)
        public static bool Find(string vi, out string res)
        {
            res = vi;
            if (Lang == Vi || string.IsNullOrEmpty(vi)) return false;
            if (table.TryGetValue(vi, out res)) return true;

            // khoảng trắng hai đầu: "Cấp " tra "Cấp"
            int a = 0, b = vi.Length;
            while (a < b && char.IsWhiteSpace(vi[a])) a++;
            while (b > a && char.IsWhiteSpace(vi[b - 1])) b--;
            if (b > a && (a > 0 || b < vi.Length) && table.TryGetValue(vi.Substring(a, b - a), out res))
            {
                res = vi.Substring(0, a) + res + vi.Substring(b);
                return true;
            }

            // số đuôi: "Ruộng Bậc Thang 3" tra "Ruộng Bậc Thang"
            int k = b;
            while (k > a && char.IsDigit(vi[k - 1])) k--;
            if (k < b && k - 1 > a && vi[k - 1] == ' ' && table.TryGetValue(vi.Substring(a, k - 1 - a), out res))
            {
                res = vi.Substring(0, a) + res + vi.Substring(k - 1);
                return true;
            }
            res = vi;
            return false;
        }

        // có chữ cái riêng của tiếng Việt (dấu, ă â đ ê ô ơ ư)
        public static bool LooksVi(string s)
        {
            if (s == null) return false;
            foreach (char c in s)
            {
                if (c >= 'Ạ' && c <= 'ỹ') return true; // Latin mở rộng thêm: ạ ả ấ ầ ... ỹ
                switch (c)
                {
                    case 'à': case 'á': case 'â': case 'ã': case 'è': case 'é': case 'ê': case 'ì': case 'í':
                    case 'ò': case 'ó': case 'ô': case 'õ': case 'ù': case 'ú': case 'ý': case 'ă': case 'đ':
                    case 'ĩ': case 'ũ': case 'ơ': case 'ư':
                    case 'À': case 'Á': case 'Â': case 'Ã': case 'È': case 'É': case 'Ê': case 'Ì': case 'Í':
                    case 'Ò': case 'Ó': case 'Ô': case 'Õ': case 'Ù': case 'Ú': case 'Ý': case 'Ă': case 'Đ':
                    case 'Ĩ': case 'Ũ': case 'Ơ': case 'Ư':
                        return true;
                }
            }
            return false;
        }
    }
}
