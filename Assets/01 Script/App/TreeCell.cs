// Một ô cây trong hộp Cây bi (prefab mục Items/OCay, gốc là khung giấy mỏng): lá, thanh đầy, số bi / sức chứa;
// cây chưa mở thì lá xám, ẩn thanh, ghi điều kiện mở. Hộp sinh đủ số cây theo cấu hình và đặt tên "cay_<i>".
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class TreeCell : MonoBehaviour
    {
        [SerializeField] Image leaf;
        [SerializeField] UiBar bar;
        [SerializeField] TextMeshProUGUI label;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image leafImg, UiBar fillBar, TextMeshProUGUI text)
        {
            leaf = leafImg;
            bar = fillBar;
            label = text;
        }

        // cây đã mở: stock / cap (đầy thì lá lắc, chữ xanh)
        public void SetOpen(double stock, double cap)
        {
            leaf.color = Color.white;
            bar.gameObject.SetActive(true);
            bar.Set((float)stock, (float)cap, 0, "");
            bool full = stock >= cap;
            label.text = $"{Mathf.FloorToInt((float)stock)}/{cap:0}";
            label.color = full ? Theme.GreenD : Theme.Ink;
            leaf.rectTransform.localEulerAngles = new Vector3(0, 0, full ? Mathf.Sin(Time.unscaledTime * Mathf.PI * 2 / 1.4f) * 6 : 0);
        }

        // cây chưa mở: điều kiện mở
        public void SetLocked(string need)
        {
            leaf.color = new Color(0.45f, 0.42f, 0.4f, 0.5f);
            bar.gameObject.SetActive(false);
            label.text = need;
            label.color = Theme.Ink3;
        }
    }
}
