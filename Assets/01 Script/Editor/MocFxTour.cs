// Menu thử (đang Play, mở từ Boot): tướng đảo Mộc có chiêu bằng hạt lá (StageView.MocFx, HatMoc.cs) ra trận: chiêu mana ở dạng cuối,
// rồi chiêu cuối ở từng dạng. Dùng lại bộ chạy của ThuyFxTour (ảnh chụp vào Temp/PokiShots/thuy_fx/<tướng>_<dạng>_<đòn>_<n>.jpg).
using UnityEditor;

namespace PokiClash.EditorTools
{
    public static class MocFxTour
    {
        [MenuItem("PokiClash/Thử/Đảo Mộc: hạt lá Mầm Ú, chiêu mana và chiêu cuối từng dạng (đang Play)", priority = 128)]
        static void Try() => ThuyFxTour.TryOnly("mam_u");

        [MenuItem("PokiClash/Thử/Đảo Mộc: hạt gai Cầu Gai, chiêu mana và chiêu cuối từng dạng (đang Play)", priority = 129)]
        static void TryGai() => ThuyFxTour.TryOnly("tien_la");

        [MenuItem("PokiClash/Thử/Đảo Mộc: đá và cầu năng lượng Gạc Đá, chiêu mana và chiêu cuối từng dạng (đang Play)", priority = 130)]
        static void TryDa() => ThuyFxTour.TryOnly("gac_da");

        [MenuItem("PokiClash/Thử/Đảo Mộc: cầu năng lượng Lộc Phong, chiêu mana và chiêu cuối từng dạng (đang Play)", priority = 131)]
        static void TryLoc() => ThuyFxTour.TryOnly("bom_la");

        [MenuItem("PokiClash/Thử/Đảo Mộc: vòi phun và dậm rừng Lâm Tượng, chiêu mana và chiêu cuối từng dạng (đang Play)", priority = 132)]
        static void TryVoi() => ThuyFxTour.TryOnly("phong_linh");

        [MenuItem("PokiClash/Thử/Đảo Mộc: lá găm và thiên thạch đá Linh Điểu, chiêu mana và chiêu cuối từng dạng (đang Play)", priority = 133)]
        static void TryChim() => ThuyFxTour.TryOnly("gio_loc");

        [MenuItem("PokiClash/Thử/Đảo Mộc: dây gai và quả cầu dây leo người cây, chiêu mana và chiêu cuối từng dạng (đang Play)", priority = 134)]
        static void TryNguoiCay() => ThuyFxTour.TryOnly("long_vuot");

        [MenuItem("PokiClash/Thử/Đảo Mộc: bạt kiếm và ảo ảnh loạn trảm Voọc Tướng, chiêu mana và chiêu cuối (đang Play)", priority = 135)]
        static void TryKiem() => ThuyFxTour.TryOnly("tho_hoang");
    }
}
