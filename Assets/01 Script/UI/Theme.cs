// Bảng màu và phông của "sổ tay phiêu lưu" (chép biến CSS của Web/src/view/style.css). Khung web 540 × 960 = Unity 1080 × 1920: mọi cỡ × 2.
using PokiClash.Core;
using TMPro;
using UnityEngine;

namespace PokiClash.UI
{
    public static class Theme
    {
        public static readonly Color Ink = Hex("#2b2118");
        public static readonly Color Ink2 = Hex("#5a4636");
        public static readonly Color Ink3 = Hex("#8a7560");
        public static readonly Color Paper = Hex("#fbf4e2");
        public static readonly Color Paper2 = Hex("#f3e7c9");
        public static readonly Color Paper3 = Hex("#e6d4a8");
        public static readonly Color CardFill = Hex("#fffaf0");
        public static readonly Color Red = Hex("#e8553f");
        public static readonly Color RedD = Hex("#b8382a");
        public static readonly Color Orange = Hex("#f39a2d");
        public static readonly Color Yellow = Hex("#f7c948");
        public static readonly Color Green = Hex("#6cbf4f");
        public static readonly Color GreenD = Hex("#3f8f33");
        public static readonly Color Teal = Hex("#3fb8a9");
        public static readonly Color Blue = Hex("#4a90d9");
        public static readonly Color BlueD = Hex("#2f66a8");
        public static readonly Color Purple = Hex("#9a6ad6");
        public static readonly Color Pink = Hex("#f07fa6");
        public static readonly Color Sky = Hex("#cfe8f3");
        public static readonly Color Mana = Hex("#4a9be8");
        public static readonly Color Rage = Hex("#f2702a");
        public static readonly Color Hp = Hex("#5cc04a");
        public static readonly Color Exp = Hex("#b783e6");
        public static readonly Color Ghost = Hex("#f7d48a"); // vệt vàng lùi chậm sau khi mất máu
        public static readonly Color Shield = new Color(160 / 255f, 200 / 255f, 240 / 255f, 0.85f);
        public static readonly Color BarTrack = Hex("#fff8e8");
        public static readonly Color Desk = Hex("#3a281d"); // nền bàn ngoài khung (máy tính bảng)
        public static readonly Color Dim = new Color(43 / 255f, 33 / 255f, 24 / 255f, 0.55f); // nền tối sau hộp thoại
        public static readonly Color TapeYellow = new Color(1f, 236 / 255f, 170 / 255f, 0.78f);
        public static readonly Color TapeBlue = new Color(170 / 255f, 214 / 255f, 1f, 0.75f);
        public static readonly Color TapePink = new Color(1f, 190 / 255f, 214 / 255f, 0.78f);
        public static readonly Color TapeGreen = new Color(190 / 255f, 236 / 255f, 170 / 255f, 0.78f);

        public static Color Hex(string hex)
        {
            return ColorUtility.TryParseHtmlString(hex, out var c) ? c : Color.magenta;
        }

        public static Color Of(Elem e) => Hex(Elements.Color(e));
        public static Color Of(Rarity r) => Hex(Elements.RarityColor(r));

        // ---------- phông ----------

        public static UiAssets Assets { get; private set; }
        public static TMP_FontAsset Title => Assets ? Assets.title : TMP_Settings.defaultFontAsset;
        public static TMP_FontAsset Bold => Assets ? Assets.bold : TMP_Settings.defaultFontAsset;
        public static TMP_FontAsset Body => Assets ? Assets.body : TMP_Settings.defaultFontAsset;
        public static Material Kit => Assets ? Assets.kit : null;
        public static Material Plain => Assets ? Assets.plain : null;
        public static UiKit Prefabs => Assets ? Assets.prefabs : null;

        public static void Init(UiAssets assets)
        {
            Assets = assets;
            BakedArt.Current = assets ? assets.baked : null;
            Shader.SetGlobalColor("_PokiInk", Ink);
            // nhiễu mượt 2 kênh (RG) cho shader nét rung, nướng sẵn ở Assets/03 Art/Baked/PokiNoise.png
            Shader.SetGlobalTexture("_PokiNoise", BakedArt.Current ? BakedArt.Current.noise : null);
            SetBoil(true);
        }

        public static void SetBoil(bool on) => Shader.SetGlobalFloat("_PokiBoil", on ? 1f : 0f);

        // Đổi ảnh của một Image kèm material hợp với ảnh: sprite giấy và mực mã hoá kênh (Kit), ảnh thường (Plain).
        public static void SetSprite(UnityEngine.UI.Image img, Sprite s)
        {
            img.sprite = s;
            img.material = Sketch.IsEncoded(s) ? Kit : Plain;
        }

        // Chữ viền mực (như -webkit-text-stroke của web). width: 0..1 theo vùng SDF; material nướng sẵn cho mỗi phông và cỡ viền.
        public static Material Outlined(TMP_FontAsset font, float width)
        {
            if (font == null || !BakedArt.Current) return null;
            return BakedArt.Current.Outline(font, Mathf.RoundToInt(width * 100));
        }
    }
}
