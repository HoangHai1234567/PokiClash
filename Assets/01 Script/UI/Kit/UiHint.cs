// Bong bóng gợi ý (giấy vàng nhạt, cao theo chữ). Prefab Assets/04 Prefabs/Kit/GoiY (rộng 520).
using TMPro;
using UnityEngine;

namespace PokiClash.UI
{
    public sealed class UiHint : MonoBehaviour
    {
        [SerializeField] TextMeshProUGUI label;

        public RectTransform Rect => (RectTransform)transform;
        public TextMeshProUGUI Label => label;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI text) => label = text;

        public void Set(string text, float width)
        {
            label.text = text;
            Rect.sizeDelta = new Vector2(width, Rect.sizeDelta.y);
        }
    }
}
