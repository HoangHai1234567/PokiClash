// Menu thử (đang Play): tướng có cú lao, cú vươn lớn ra chiêu mana, chiêu cuối trong trận (tour của HoaFxTour, ảnh ở
// Temp/PokiShots/hoa_fx). Soi lỗi thân ra ngoài khung ảnh của AolaSticker (2026-11-19: "tướng biến mất giữa chiêu như chui vào mask").
using UnityEditor;

namespace PokiClash.EditorTools
{
    public static class KhungTuongTour
    {
        [MenuItem("PokiClash/Thử/Khung tướng: chiêu có cú lao lớn, 5 tướng (đang Play)", priority = 126)]
        static void Try() => HoaFxTour.TryOnly("su_tu_lua", "tho_hoang", "ha_ba", "huyen_viem", "bo_cap");
    }
}
