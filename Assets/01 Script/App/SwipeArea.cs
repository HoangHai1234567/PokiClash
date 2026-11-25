// Vùng vuốt trong suốt (vòng chọn tướng khởi đầu, 2026-11-24): kéo ngang và chạm, chuyển cho màn chủ qua các hàm gán. Cần một
// Graphic nhận chạm trên cùng GameObject (ảnh trong suốt), đặt trên cùng các thứ cần vuốt để không bị hình bên dưới giành sự kiện.
using System;
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class SwipeArea : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler, IPointerClickHandler
    {
        public Action Began; // bắt đầu kéo
        public Action<Vector2> Dragged; // độ dời mỗi khung, px màn hình
        public Action Ended; // thả tay sau khi kéo
        public Action<Vector2> Tapped; // chạm không kéo, toạ độ màn hình

        public void OnBeginDrag(PointerEventData e) => Began?.Invoke();
        public void OnDrag(PointerEventData e) => Dragged?.Invoke(e.delta);
        public void OnEndDrag(PointerEventData e) => Ended?.Invoke();

        public void OnPointerClick(PointerEventData e)
        {
            if (!e.dragging) Tapped?.Invoke(e.position);
        }
    }
}
