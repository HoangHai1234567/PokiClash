// Bảng màu màn cửa hàng bản 3 (người dùng 2026-11-27: "thiết kế shop như clash of critters, nền tối, gói IAP màu tươi nổi"; GD_Claude/26
// mục 15). Thẻ / ô nền xám (Assets/03 Art/Shop/v3, ArtGen/Shop/v3/ve_ui.py) tô bằng ba màu: nền chính (trái, có sao nổ), mảng phải cắt
// chéo (caro thoi), sao nổ. Nút mua tô xanh lá như thẻ mẫu.
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public readonly struct ShopHue
    {
        public readonly Color fill, panel, rays;

        public ShopHue(string fill, string panel, string rays)
        {
            this.fill = Theme.Hex(fill);
            this.panel = Theme.Hex(panel);
            this.rays = Theme.Hex(rays);
        }

        public ShopHue(Color fill, Color panel, Color rays)
        {
            this.fill = fill;
            this.panel = panel;
            this.rays = rays;
        }

        // vàng + tím (gói khởi hành, quỹ), cam + hồng (ưu đãi hẹn giờ), hồng + tím (quà nhập môn, gói theo ngày), trời + chàm (bi, thẻ),
        // lá + lam (miễn phí), nho + hồng (trứng, chuỗi), dung nham + vàng (ưu đãi nóng), xám chàm (thẻ thông tin: tỉ lệ, khôi phục)
        public static readonly ShopHue Gold = new ShopHue("#ffc21a", "#8a3cf0", "#fff4c8");
        public static readonly ShopHue Sunset = new ShopHue("#ff8a2a", "#ff3d6e", "#ffe9a8");
        public static readonly ShopHue Berry = new ShopHue("#ff5c93", "#9b3cf0", "#ffd9ea");
        public static readonly ShopHue Sky = new ShopHue("#2fa8ff", "#6a4cf5", "#d8f6ff");
        public static readonly ShopHue Mint = new ShopHue("#3fcf6a", "#1fa3c9", "#eaffc8");
        public static readonly ShopHue Grape = new ShopHue("#b04ef0", "#ff4fa8", "#f3dcff");
        public static readonly ShopHue Lava = new ShopHue("#f2483f", "#ffb21a", "#ffe0b0");
        public static readonly ShopHue Slate = new ShopHue("#6c74a8", "#4a4f80", "#dfe4ff");

        // thẻ / popup ưu đãi: Quà Nhập Môn hồng, Khởi Hành vàng tím (như thẻ mẫu), ưu đãi nóng đỏ, gói đỡ khi thua lá, còn lại cam hồng
        public static ShopHue Offer(ActiveOffer o) =>
            o.pack == "starter3" ? Berry : o.pack != null && App.Data.Cfg.shop.Pack(o.pack)?.group == "launch" ? Gold : o.tpl == "hot" ? Lava :
            o.tpl == "relief" ? Mint : Sunset;

        // ô trứng: màu bậc, mảng phải tối hơn
        public static ShopHue Tier(int tier)
        {
            var c = ShopUi.TierColor(tier);
            return new ShopHue(c, Color.Lerp(c, Color.black, 0.3f), Color.white);
        }

        public ShopHue Dim()
        {
            var g = new Color(0.45f, 0.45f, 0.55f);
            return new ShopHue(Color.Lerp(fill, g, 0.7f), Color.Lerp(panel, g, 0.7f), Color.Lerp(rays, g, 0.5f));
        }

        // nút mua / nhận: xanh lá thẻ mẫu; quảng cáo: lam; phụ: giấy
        public static readonly Color Lime = Theme.Hex("#8de02e");

        public static void Paint(SketchButton b, BtnColor role)
        {
            if (role == BtnColor.Orange || role == BtnColor.Green)
            {
                b.SetRole(BtnColor.Green); // chữ trắng viền mực
                b.SetColor(Lime);
            }
            else b.SetRole(role);
        }

        // nhãn "Giá trị ×8": viết hoa chữ đầu
        public static string ValueText(double mult)
        {
            var s = Loc.F("giá trị ×{0}", System.Math.Round(mult));
            return s.Length > 0 ? char.ToUpper(s[0]) + s.Substring(1) : s;
        }
    }
}
