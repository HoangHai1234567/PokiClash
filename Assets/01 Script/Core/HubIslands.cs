// Đảo nào trên bản đồ sảnh đã tan mây (người dùng 2026-11-19): mới chơi mây che hết; chọn tướng khởi đầu thì tan mây đảo cùng hệ với
// tướng đó; xong trận hướng dẫn thì tan nốt các đảo còn lại. Trận hướng dẫn chưa làm: tạm coi là xong khi đã thắng một ải bất kỳ.
// Số đảo đã diễn cảnh tan mây lưu trong SaveData.extra["hubShown"] (bit = Elem), chỉ đổi trong bộ nhớ, lần lưu kế tiếp ghi xuống.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public static class HubIslands
    {
        const string ShownKey = "hubShown";

        public static int All => Elements.All.Aggregate(0, (m, e) => m | Bit(e));

        public static int Bit(Elem e) => 1 << (int)e;

        // xong trận hướng dẫn (tạm: đã thắng ít nhất một ải ở bất kỳ đảo nào)
        public static bool TutorialDone(SaveData s) => s?.zones != null && s.zones.Any(z => z > 0);

        // các đảo đã tan mây (bit = Elem)
        public static int Open(SaveData s, GameData d)
        {
            if (s == null || string.IsNullOrEmpty(s.starter)) return 0;
            if (TutorialDone(s)) return All;
            var h = d?.Hero(s.starter);
            return h != null ? Bit(h.elem) : All;
        }

        public static bool IsOpen(SaveData s, GameData d, Elem e) => (Open(s, d) & Bit(e)) != 0;

        public static int Shown(SaveData s)
        {
            if (s?.extra == null || !s.extra.TryGetValue(ShownKey, out var o) || o == null) return 0;
            try
            {
                return Convert.ToInt32(o);
            }
            catch (Exception)
            {
                return 0;
            }
        }

        public static void SetShown(SaveData s, int mask)
        {
            if (s?.extra == null) return;
            s.extra[ShownKey] = (double)mask;
        }
    }
}
