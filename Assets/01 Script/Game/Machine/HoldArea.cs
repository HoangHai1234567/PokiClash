// Vùng chạm-giữ (mặt máy, nút "Thả bi"): báo lúc nhấn và lúc nhả.
using System;
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class HoldArea : MonoBehaviour, IPointerDownHandler, IPointerUpHandler
    {
        public Action Down, Up;
        public void OnPointerDown(PointerEventData e) => Down?.Invoke();
        public void OnPointerUp(PointerEventData e) => Up?.Invoke();
    }
}
