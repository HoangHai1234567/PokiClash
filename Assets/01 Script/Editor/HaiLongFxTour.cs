// Menu thử (đang Play, mở từ Boot): Hải Long (boss cuối đảo Thủy) — chiêu mana LOẠT THỦY TIA (HatHaiLongTia.cs, 2026-11-25: mỗi đầu bắn
// một tia Water Laser) và chiêu cuối từng dạng, trong trận và trong hộp chi tiết tướng. Dùng bộ chạy của ThuyFxTour (ảnh vào
// Temp/PokiShots/thuy_fx/hai_long_<dạng>_<đòn>_<n>.jpg; hộp chi tiết: tên ảnh theo RunViewer).
using UnityEditor;

namespace PokiClash.EditorTools
{
    public static class HaiLongFxTour
    {
        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/loạt thủy tia Hải Long, chiêu mana và chiêu cuối từng dạng (đang Play)", priority = 140)]
        static void Try() => ThuyFxTour.TryOnly("hai_long");

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/loạt thủy tia Hải Long chạy chậm 0,4× (đang Play)", priority = 141)]
        static void TryCham() => ThuyFxTour.TryOnlyCham(0.4f, "hai_long");

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/loạt thủy tia Hải Long trong hộp chi tiết tướng (đang Play)", priority = 142)]
        static void TryHop() => ThuyFxTour.TryViewerOnly("hai_long");
    }
}
