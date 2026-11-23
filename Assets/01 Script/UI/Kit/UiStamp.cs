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
            // 84 → 72 mỗi chữ: dấu nghiêng rộng quá thì góc dưới phải cắt dòng tên ải bên dưới (soát UI 2026-11-23)
            Rect.sizeDelta = new Vector2(Mathf.Max(360, text.Length * 72 + 80), 190);
        }
    }
}
