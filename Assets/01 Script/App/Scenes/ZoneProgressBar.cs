// Thanh tiến độ viền mực của đảo (số ải đã qua / số ải của đảo), phần đầy tô màu hệ.
// Nằm trong prefab mục Items/BangVung (sảnh) và màn Đảo.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ZoneProgressBar : MonoBehaviour
    {
        [SerializeField] Image fill;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image fillImg) => fill = fillImg;

        // p: 0..1; bằng 0 thì ẩn phần đầy
        public void Set(Color color, float p)
        {
            fill.color = color;
            fill.rectTransform.anchorMax = new Vector2(Mathf.Clamp01(p), 1);
            fill.gameObject.SetActive(p > 0);
        }
    }
}
