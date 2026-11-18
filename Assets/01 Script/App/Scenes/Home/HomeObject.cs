// Một vật trên bản đồ Nhà (prefab Items/NhaVat, dựng bằng menu "PokiClash/Prefab/Nhà: dựng màn"): công trình, trang trí, khối rừng,
// bóng ma lúc xây. Ảnh neo ở góc dưới chân thoi (pivot lấy từ home_art.json); nhãn nổi trên đầu (tên, cấp, giờ còn lại); bong bóng
// báo có đồ để thu. HomeScene đặt vị trí, cỡ và thứ tự vẽ.
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HomeObject : MonoBehaviour
    {
        [SerializeField] Image img;
        [SerializeField] TextMeshProUGUI label;
        [SerializeField] Image bubble, bubbleIcon;

        public RectTransform Rt => (RectTransform)transform;
        public Image Img => img;
        public int Id { get; set; } = -1; // công trình (id) hoặc -2 - ô rừng
        public float Depth { get; set; } // y góc dưới (px từ trên xuống): lớn hơn vẽ sau

        // Dùng khi dựng prefab (Editor).
        public void Setup(Image image, TextMeshProUGUI text, Image bubbleBg, Image icon)
        {
            img = image;
            label = text;
            bubble = bubbleBg;
            bubbleIcon = icon;
        }

        // sprite, cỡ hiển thị (px), pivot (góc dưới chân thoi), toạ độ góc dưới tính từ góc trên trái bản đồ (y xuống)
        public void Place(Sprite s, Vector2 size, Vector2 pivot, Vector2 at)
        {
            Theme.SetSprite(img, s);
            img.preserveAspect = false;
            var rt = Rt;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = pivot;
            rt.sizeDelta = size;
            rt.anchoredPosition = new Vector2(at.x, -at.y);
            Depth = at.y;
        }

        public void Tint(Color c) => img.color = c;

        public void Label(string text)
        {
            if (!label) return;
            label.gameObject.SetActive(!string.IsNullOrEmpty(text));
            label.text = text ?? "";
        }

        public void Bubble(Sprite icon)
        {
            if (!bubble) return;
            bubble.gameObject.SetActive(icon);
            if (icon && bubbleIcon) Theme.SetSprite(bubbleIcon, icon);
        }
    }
}
