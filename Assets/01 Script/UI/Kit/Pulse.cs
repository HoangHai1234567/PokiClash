// Nhịp phồng nhẹ (nút đủ điều kiện, chấm đỏ báo việc).
using UnityEngine;

namespace PokiClash
{
    public sealed class Pulse : MonoBehaviour
    {
        public float amount = 0.06f, period = 1f;
        Vector3 baseScale = Vector3.one;

        void Start() => baseScale = transform.localScale;

        void Update()
        {
            float s = 1 + amount * (0.5f - 0.5f * Mathf.Cos(Time.unscaledTime * Mathf.PI * 2 / period));
            transform.localScale = baseScale * s;
        }
    }
}
