// Nhịp thở cho icon nổi (người dùng 2026-11-27: icon ưu đãi ở sảnh "phải có hiệu ứng breath"): hít vào thì giãn dọc nhiều hơn ngang và nhô
// lên chút, thở ra thì về; nhịp êm (sin), lệch pha theo phase để các icon cạnh nhau không phồng cùng lúc. Gắn vào hình (không gắn vào nút để
// vùng chạm đứng yên). Pulse (cùng thư mục) là phồng đều cho chấm đỏ / nút đủ điều kiện.
using UnityEngine;

namespace PokiClash
{
    public sealed class Breathe : MonoBehaviour
    {
        [Tooltip("Độ giãn dọc lúc hít sâu nhất (0,08 = 8%); ngang bằng 60% số này")]
        public float amount = 0.08f;
        [Tooltip("Giây cho một hơi (hít + thở)")]
        public float period = 1.8f;
        [Tooltip("Lệch pha 0..1 (icon thứ hai, thứ ba...)")]
        public float phase;
        [Tooltip("Nhô lên bao nhiêu điểm lúc hít sâu nhất")]
        public float lift = 4;

        Vector3 baseScale = Vector3.one;
        Vector2 basePos;
        RectTransform rt;

        void Awake()
        {
            baseScale = transform.localScale;
            rt = transform as RectTransform;
            if (rt) basePos = rt.anchoredPosition;
        }

        void OnDisable()
        {
            transform.localScale = baseScale;
            if (rt) rt.anchoredPosition = basePos;
        }

        void Update()
        {
            float k = 0.5f - 0.5f * Mathf.Cos((Time.unscaledTime / period + phase) * Mathf.PI * 2);
            transform.localScale = new Vector3(baseScale.x * (1 + amount * 0.6f * k), baseScale.y * (1 + amount * k), baseScale.z);
            if (rt) rt.anchoredPosition = basePos + new Vector2(0, lift * k);
        }
    }
}
