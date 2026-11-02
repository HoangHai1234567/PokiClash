// Con dấu "THẮNG" / "THUA" / "LÊN CẤP": chữ to nghiêng trong vòng mực màu. Prefab Assets/04 Prefabs/Kit/ConDau.
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    public sealed class UiStamp : MonoBehaviour
    {
        [SerializeField] Image ring;
        [SerializeField] TextMeshProUGUI label;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image image, TextMeshProUGUI text)
        {
            ring = image;
            label = text;
        }

        public void Set(string text, Color color)
        {
            ring.color = color;
            label.color = color;
            label.text = text.ToUpperInvariant();
            Rect.sizeDelta = new Vector2(Mathf.Max(360, text.Length * 84 + 80), 190);
        }
    }
}
