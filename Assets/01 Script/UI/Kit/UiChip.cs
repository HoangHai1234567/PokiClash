// Chip tài nguyên: biểu tượng tròn + số (bi, đá, mảnh...) trên viên giấy. Prefab Assets/04 Prefabs/Kit/Chip (cao 72).
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    public sealed class UiChip : MonoBehaviour
    {
        [SerializeField] Image icon;
        [SerializeField] TextMeshProUGUI value;

        public Image Icon => icon;
        public TextMeshProUGUI Value => value;
        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image iconImg, TextMeshProUGUI text)
        {
            icon = iconImg;
            value = text;
        }

        // icon null: chấm mực
        public void Set(Sprite sprite, Color tint, string text)
        {
            Theme.SetSprite(icon, sprite != null ? sprite : Sketch.InkDot);
            icon.color = tint;
            value.text = text;
        }

        // cao h: icon tròn lấn ra mép trái, số cỡ 0,56 h
        public void SetHeight(float h, float width = 200)
        {
            Rect.sizeDelta = new Vector2(width, h);
            icon.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(-6, 3), new Vector2(h + 8, h + 8), new Vector2(0, 0.5f));
            value.fontSize = h * 0.56f;
            value.rectTransform.Stretch(h + 6, 0, 14, 6);
        }
    }
}
