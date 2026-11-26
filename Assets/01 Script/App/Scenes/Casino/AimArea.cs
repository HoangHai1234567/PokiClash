// Vùng chạm của mặt hồ Bến câu (GD_Claude/32 mục 4): báo lúc nhấn, kéo, nhả kèm vị trí màn hình để FishingPanel ngắm chỗ thả phao.
using System;
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class AimArea : MonoBehaviour, IPointerDownHandler, IPointerUpHandler, IBeginDragHandler, IDragHandler
    {
        public Action<PointerEventData> Down, Drag, Up;
        public void OnPointerDown(PointerEventData e) => Down?.Invoke(e);
        public void OnPointerUp(PointerEventData e) => Up?.Invoke(e);
        public void OnBeginDrag(PointerEventData e) => Drag?.Invoke(e);
        public void OnDrag(PointerEventData e) => Drag?.Invoke(e);
    }
}
