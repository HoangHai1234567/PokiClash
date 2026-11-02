// Nhún lên xuống (mũi tên gợi ý, sticker đội trưởng).
using UnityEngine;

namespace PokiClash
{
    public sealed class Bob : MonoBehaviour
    {
        public float amount = 12, period = 1.4f;
        Vector2 basePos;
        RectTransform rt;

        void Start()
        {
            rt = (RectTransform)transform;
            basePos = rt.anchoredPosition;
        }

        void Update()
        {
            if (rt) rt.anchoredPosition = basePos + new Vector2(0, Mathf.Sin(Time.unscaledTime * Mathf.PI * 2 / period) * amount);
        }
    }
}
