// Ô món trong thẻ cửa hàng bản 3 (prefab Items/OMonCuaHang, GD_Claude/26 mục 15): ô vuông kem viền mực, hình món (icon, trứng bậc, mặt
// tướng), vạch tối dưới ghi số trắng; món có độ hiếm thì nền pha màu bậc. Học ô món thẻ gói Clash of Critters (không chữ tên, nhìn hình là ra).
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ShopItemCell : MonoBehaviour
    {
        public const float Size = 128;
        static readonly Color Cream = Theme.Hex("#fff3cf");

        [SerializeField] Image frame, icon;
        [SerializeField] TextMeshProUGUI count;
        [SerializeField] RectTransform heroBox; // khung cắt chân dung (tướng chưa có ảnh mặt vẽ tay)

        public void Setup(Image frameImg, Image iconImg, TextMeshProUGUI countText, RectTransform heroClip)
        {
            frame = frameImg;
            icon = iconImg;
            count = countText;
            heroBox = heroClip;
        }

        public ShopItemCell Set(ShopItem it)
        {
            var l = ShopUi.Look(it);
            var s = l.hero != null ? HeroArt.Face(l.hero) : l.icon;
            Theme.SetSprite(icon, s);
            icon.preserveAspect = true;
            icon.color = l.tint;
            // mảnh tướng chưa có ảnh mặt: phần đầu chân dung trong khung cắt (như ô thưởng RewardTile)
            bool portrait = l.hero != null && !s && heroBox && Theme.Prefabs && Theme.Prefabs.portrait;
            icon.gameObject.SetActive(!portrait);
            if (portrait) HeroArt.FitHead(Ui.Spawn(Theme.Prefabs.portrait, heroBox), l.hero, 0, heroBox.rect.size);
            // bi: số trơn (1.200); món khác: ×N
            count.text = Shop.Norm(it).k == "balls" ? NumFmt.Short(Shop.Norm(it).n) : l.count;
            count.gameObject.SetActive(!string.IsNullOrEmpty(count.text));
            var r = l.hero != null ? l.hero.rarity : l.rarity;
            frame.color = r.HasValue ? Color.Lerp(ShopUi.TierColor((int)r.Value), Color.white, 0.62f) : Cream;
            name = "mon_" + Shop.Norm(it).k;
            return this;
        }
    }
}
