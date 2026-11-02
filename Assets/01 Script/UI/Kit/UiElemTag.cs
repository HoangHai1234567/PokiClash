// Nhãn hệ: khung phẳng màu hệ, tên hệ chữ trắng viền mực. Prefab Assets/04 Prefabs/Kit/NhanHe (cao 44).
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    public sealed class UiElemTag : MonoBehaviour
    {
        [SerializeField] Image bg;
        [SerializeField] TextMeshProUGUI label;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image image, TextMeshProUGUI text)
        {
            bg = image;
            label = text;
        }

        public void Set(Elem e)
        {
            name = "he_" + Keys.Of(e);
            bg.color = Theme.Of(e);
            label.text = Elements.Name(e);
        }

        public void SetHeight(float h)
        {
            Rect.sizeDelta = new Vector2(h * 2.4f, h);
            label.fontSize = h * 0.62f;
        }
    }
}
