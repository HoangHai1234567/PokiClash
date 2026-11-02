// Huy hiệu hệ: huy chương tô màu theo bậc, biểu tượng hệ ở giữa; bậc 0 (chưa có) là bóng xám mờ.
// Prefab Assets/04 Prefabs/Kit/HuyHieu.
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BadgeIcon : MonoBehaviour
    {
        [SerializeField] Image medal, elem;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image medalImg, Image elemImg)
        {
            medal = medalImg;
            elem = elemImg;
        }

        // hệ e bậc tier, cao size (rộng theo tỉ lệ hình)
        public void Bind(Elem e, int tier, float size)
        {
            name = $"huy_hieu_{Keys.Of(e)}_{tier}";
            medal.color = BadgeArt.ColorOf(tier);
            Rect.sizeDelta = new Vector2(size * 96 / 112f, size);
            elem.sprite = App.Art ? App.Art.Icon("e_" + Keys.Of(e)) : null;
            elem.color = tier > 0 ? Color.white : new Color(1, 1, 1, 0.45f);
            elem.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -size * 0.17f), new Vector2(size * 0.5f, size * 0.5f), new Vector2(0.5f, 1));
        }
    }
}
