// Xoay đều quanh tâm (vầng tia sau icon ưu đãi ở sảnh, 2026-11-27): độ / giây, âm là ngược chiều kim đồng hồ.
using UnityEngine;

namespace PokiClash
{
    public sealed class Spin : MonoBehaviour
    {
        public float speed = 20;

        void Update() => transform.Rotate(0, 0, -speed * Time.unscaledDeltaTime);
    }
}
