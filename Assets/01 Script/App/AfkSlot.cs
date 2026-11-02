// Một ô trong khay rương AFK (prefab mục Items/RuongAfk, gốc là nút giấy): hình rương, giờ còn lại / "Mở được" / "Chờ".
// Hộp AFK sinh đủ số ô theo khay (4, Thẻ Phiêu Lưu 5) và đặt tên "afk_ruong_<i>".
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class AfkSlot : MonoBehaviour
    {
        [SerializeField] SketchButton button;
        [SerializeField] RectTransform chest;
        [SerializeField] TextMeshProUGUI label;

        public SketchButton Button => button;

        // Dùng khi nướng prefab (Editor).
        public void Setup(SketchButton btn, RectTransform chestRt, TextMeshProUGUI text)
        {
            button = btn;
            chest = chestRt;
            label = text;
        }

        // đặt ô: x lệch so với giữa khay, w bề rộng ô (cao 200)
        public void Arrange(float x, float w)
        {
            button.Rect.Place(new Vector2(0.5f, 0.5f), new Vector2(x, 0), new Vector2(w, 200));
            var le = button.GetComponent<LayoutElement>();
            if (le) le.preferredWidth = w;
            label.rectTransform.sizeDelta = new Vector2(w - 10, 40);
        }

        // has: ô có rương; ready: tới giờ mở (rương lắc); text: chữ dưới rương
        public void Set(bool has, bool ready, string text)
        {
            chest.gameObject.SetActive(has);
            if (!has)
            {
                label.text = "";
                button.SetColor(Theme.Paper2);
                return;
            }
            button.SetColor(ready ? Theme.Hex("#e6f7d9") : Theme.Paper);
            label.color = ready ? Theme.GreenD : Theme.Ink;
            label.text = text;
            chest.localEulerAngles = new Vector3(0, 0, ready ? Mathf.Sin(Time.unscaledTime * Mathf.PI * 2 / 1.4f) * 6 : 0);
        }
    }
}
