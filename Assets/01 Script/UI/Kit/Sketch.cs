// Sprite giấy và mực của bộ UI: khung viền mực bo lệch góc, bóng cứng, nút có gờ và gạch sáp, thanh, viên thuốc, sao, mây,
// băng keo, giấy kẻ ô. Nướng sẵn thành PNG ở Assets/03 Art/Baked/Sketch, lúc chạy chỉ tra bảng.
// Sprite "mã hoá" (tên texture bắt đầu bằng sk_, dùng material Theme.Kit): R = độ sáng phần tô, G = mực, B = vùng gạch sáp, A = độ phủ.
using UnityEngine;

namespace PokiClash.UI
{
    public static class Sketch
    {
        public static Sprite Panel => Get(nameof(Panel));
        public static Sprite PanelThin => Get(nameof(PanelThin));
        public static Sprite PanelFlat => Get(nameof(PanelFlat));
        public static Sprite Button => Get(nameof(Button));
        public static Sprite ButtonPressed => Get(nameof(ButtonPressed));
        public static Sprite Round => Get(nameof(Round));
        public static Sprite RoundPressed => Get(nameof(RoundPressed));
        public static Sprite CardFrame => Get(nameof(CardFrame));
        public static Sprite Pill => Get(nameof(Pill));
        public static Sprite BarTrack => Get(nameof(BarTrack));
        public static Sprite BarFill => Get(nameof(BarFill));
        public static Sprite Dot => Get(nameof(Dot));
        public static Sprite InkDot => Get(nameof(InkDot));
        public static Sprite Star => Get(nameof(Star));
        public static Sprite Cloud => Get(nameof(Cloud));
        public static Sprite Tape => Get(nameof(Tape));
        public static Sprite Ring => Get(nameof(Ring));
        public static Sprite Ring360 => Get(nameof(Ring360));
        public static Sprite PaperGrid => Get(nameof(PaperGrid));
        public static Sprite Burst => Get(nameof(Burst));
        public static Sprite DashRing => Get(nameof(DashRing));
        public static Sprite LinedPaper => Get(nameof(LinedPaper));
        public static Sprite CloudPuff => Get(nameof(CloudPuff));
        public static Sprite Stick => Get(nameof(Stick));
        public static Sprite Medal => Get(nameof(Medal));
        public static Sprite Chest => Get(nameof(Chest));
        public static Sprite White => Get(nameof(White));

        // sprite nào dùng material mã hoá kênh (còn lại dùng Theme.Plain)
        public static bool IsEncoded(Sprite s) => s != null && s.texture != null && s.texture.name.StartsWith("sk_");

        static Sprite Get(string name) => BakedArt.Current ? BakedArt.Current.Sketch(name) : null;
    }
}
