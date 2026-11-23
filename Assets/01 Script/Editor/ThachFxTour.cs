// Menu thử (đang Play): Thiên Thạch Thú (suất cu_phu, ải 60 đảo Thổ, mini boss; rig tinh_hach_1, hiệu ứng HatThach.cs; 2026-11-17) ra trận
// một mình: đòn thường (vồ xé), chiêu mana (hai tay xoa, năm thiên thạch lao vào đối thủ), chiêu cuối (quả cầu thiên thạch, lửa xé gió, nổ
// lớn). Dùng ThoFxTour.Try: ảnh Temp/PokiShots/tho_fx/cu_phu_<sao>sao_<danh|mana|ult>_<n>.jpg. Sao 1 = dạng 1 Thiên Thạch Thú Non (rig
// tinh_hach_non, ba thiên thạch, n_thach_xoay1 / n_thach_cau1; 2026-11-18), sao 6 = dạng 2 (rig tinh_hach_1); cỡ 0,92 / 1,1.
using UnityEditor;

namespace PokiClash.EditorTools
{
    public static class ThachFxTour
    {
        [MenuItem("PokiClash/Thử/Tướng/Đảo Thổ/riêng Thiên Thạch Thú (sao 1, dạng 1 Non), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryThienThach() => ThoFxTour.Try("cu_phu", 1);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thổ/riêng Thiên Thạch Thú (sao 6, dạng 2), đòn thường, chiêu mana, chiêu cuối (đang Play)", priority = 125)]
        static void TryThienThach6() => ThoFxTour.Try("cu_phu", 6);
    }
}
