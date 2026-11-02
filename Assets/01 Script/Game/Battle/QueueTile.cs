// Một ô trong hàng thẻ của trận (prefab Assets/04 Prefabs/Items/TranO): chỗ cố định trong hàng (cho layout) và tấm thẻ bên trong
// (dải màu độ hiếm, icon, tên) để nhô lên khi đang chạy, mờ đi khi đã chạy. Cũng dùng làm ô bay từ hàng thẻ lên đầu tướng.
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class QueueTile : MonoBehaviour
    {
        [SerializeField] LayoutElement layout;
        [SerializeField] Image card, band, icon;
        [SerializeField] CanvasGroup group;
        [SerializeField] TextMeshProUGUI label;

        public RectTransform Rect => (RectTransform)transform;
        public RectTransform Card => card.rectTransform;
        public CanvasGroup Group => group;

        // Dùng khi nướng prefab (Editor).
        public void Setup(LayoutElement le, Image cardImg, Image bandImg, Image iconImg, CanvasGroup cg, TextMeshProUGUI text)
        {
            layout = le;
            card = cardImg;
            band = bandImg;
            icon = iconImg;
            group = cg;
            label = text;
        }

        // w: bề rộng ô (112, ô đòn kết 128)
        public void Bind(Sprite iconSprite, string title, Color bandColor, Color fill, bool skill, float w = 112)
        {
            name = "o_" + title;
            Size(w);
            card.color = fill;
            band.color = bandColor;
            icon.sprite = iconSprite;
            label.text = title;
            label.color = skill ? Theme.BlueD : Theme.Ink;
            ResetState();
        }

        // chép hình của ô khác (ô bay)
        public void CopyFrom(QueueTile o)
        {
            name = o.name;
            Size(o.layout.preferredWidth);
            card.color = o.card.color;
            band.color = o.band.color;
            icon.sprite = o.icon.sprite;
            label.text = o.label.text;
            label.color = o.label.color;
            ResetState();
        }

        void Size(float w)
        {
            layout.preferredWidth = w;
            Rect.sizeDelta = new Vector2(w, 140);
            label.rectTransform.sizeDelta = new Vector2(w - 10, 28);
        }

        void ResetState()
        {
            group.alpha = 1;
            Card.localScale = Vector3.one;
            Card.localEulerAngles = Vector3.zero;
            Card.anchoredPosition = Vector2.zero;
        }

        // đã chạy: mờ, thu nhỏ
        public void Done()
        {
            group.alpha = 0.4f;
            Card.localScale = new Vector3(0.9f, 0.9f, 1);
        }

        // đang chạy: nhô lên, nghiêng
        public void Now()
        {
            Card.localScale = new Vector3(1.15f, 1.15f, 1);
            Card.localEulerAngles = new Vector3(0, 0, 3);
            Card.anchoredPosition = new Vector2(0, 20);
        }
    }
}
