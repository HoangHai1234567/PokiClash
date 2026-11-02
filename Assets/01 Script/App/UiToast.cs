// Một thông báo ngắn (prefab Assets/04 Prefabs/Dialogs/ThongBao): khung giấy mỏng tự giãn theo chữ, icon tuỳ chọn.
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class UiToast : MonoBehaviour
    {
        [SerializeField] Image icon;
        [SerializeField] TextMeshProUGUI label;
        [SerializeField] LayoutElement labelLayout;
        [SerializeField] CanvasGroup group;

        public RectTransform Rect => (RectTransform)transform;
        public CanvasGroup Group => group;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image iconImg, TextMeshProUGUI text, LayoutElement textLayout, CanvasGroup cg)
        {
            icon = iconImg;
            label = text;
            labelLayout = textLayout;
            group = cg;
        }

        public void Set(string text, Sprite sprite)
        {
            icon.gameObject.SetActive(sprite != null);
            if (sprite != null) PokiClash.UI.Theme.SetSprite(icon, sprite);
            label.text = text;
            labelLayout.preferredWidth = Mathf.Min(label.GetPreferredValues(text, 9999, 100).x, 860);
        }
    }
}
