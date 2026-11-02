// Lắc qua lại (rương nhận được).
using UnityEngine;

namespace PokiClash
{
    public sealed class Wobble : MonoBehaviour
    {
        public float angle = 8, period = 1.6f;

        void Update() => transform.localEulerAngles = new Vector3(0, 0, Mathf.Sin(Time.unscaledTime * Mathf.PI * 2 / period) * angle);
    }
}
