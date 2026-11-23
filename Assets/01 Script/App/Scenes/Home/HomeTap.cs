// Bắt chạm trên mặt đất Nhà (ảnh nền, raycastTarget): đổi điểm chạm ra toạ độ bản đồ (px từ góc trên trái, y xuống) rồi báo HomeScene.
// - Chạm: OnTap.
// - Nhấn xuống trúng bóng ma (đang xây / dời): OnPress trả true thì ngón đó cầm bóng ma luôn, kéo là dời (OnGrabMove, OnGrabEnd).
// - Giữ yên HoldTime giây trên công trình (như Clash of Critters, Clash of Clans): OnHold trả true thì nhấc công trình lên, cùng ngón kéo đi.
// - Còn lại (kéo bản đồ, chụm hai ngón): chuyển nguyên sự kiện cho LandView ở lớp cha. Mặt đất bắt IDragHandler nên EventSystem gửi kéo
//   tới đây trước; không chuyển thì bản đồ hết kéo được.
using System;
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class HomeTap : MonoBehaviour, IPointerClickHandler, IPointerDownHandler, IPointerUpHandler, IBeginDragHandler, IDragHandler, IEndDragHandler
    {
        public const float HoldTime = 0.45f;

        public Action<Vector2> OnTap;
        public Func<Vector2, bool> OnPress;
        public Func<Vector2, bool> OnHold;
        public Action<Vector2> OnGrabMove;
        public Action<Vector2> OnGrabEnd;
        public GameObject pass; // LandView

        PointerEventData down; // ngón đang nhấn (EventSystem cập nhật vị trí mỗi khung)
        // camera của cú nhấn, lưu lúc nhấn: ngoài hàm sự kiện down.pressEventCamera có thể là null (InputSystemUIInputModule dùng chung
        // một PointerEventData cho ba nút chuột; khung ngón rung, xử lý xong nút giữa thì trạng thái nhấn là của nút giữa), Update đổi
        // chỗ giữ ra ô sai, nhấc nhầm công trình
        Camera downCam;
        float downT;
        bool grab, grabDrag, held, noClick, panned;

        public bool Grabbing => grab;

        Vector2 Map(Vector2 screen, Camera cam)
        {
            var rt = (RectTransform)transform;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(rt, screen, cam, out var local);
            var r = rt.rect;
            return new Vector2(local.x - r.xMin, r.yMax - local.y);
        }

        public void OnPointerDown(PointerEventData e)
        {
            if (down != null) return; // ngón thứ hai: để LandView chụm
            down = e;
            downCam = e.pressEventCamera;
            downT = Time.unscaledTime;
            held = panned = grabDrag = false;
            noClick = false;
            grab = OnPress != null && OnPress(Map(e.position, e.pressEventCamera));
            if (grab) noClick = true;
        }

        void Update()
        {
            if (down == null || grab || held || panned) return;
            if (Time.unscaledTime - downT < HoldTime) return;
            held = true;
            if (OnHold != null && OnHold(Map(down.position, downCam)))
            {
                grab = true;
                noClick = true;
            }
        }

        public void OnPointerUp(PointerEventData e)
        {
            if (down == null || e.pointerId != down.pointerId) return;
            if (grab && !grabDrag)
            {
                grab = false;
                OnGrabEnd?.Invoke(Map(e.position, e.pressEventCamera));
            }
            if (!grabDrag) down = null; // đang kéo bóng ma thì OnEndDrag (đến sau) dọn
        }

        public void OnPointerClick(PointerEventData e)
        {
            if (noClick)
            {
                noClick = false;
                return;
            }
            OnTap?.Invoke(Map(e.position, e.pressEventCamera));
        }

        bool Mine(PointerEventData e) => grab && down != null && e.pointerId == down.pointerId;

        public void OnBeginDrag(PointerEventData e)
        {
            if (Mine(e))
            {
                grabDrag = true;
                OnGrabMove?.Invoke(Map(e.position, e.pressEventCamera));
                return;
            }
            if (grab) return; // đang cầm công trình: ngón khác không kéo bản đồ
            if (down != null && e.pointerId == down.pointerId) panned = true;
            if (pass) ExecuteEvents.Execute(pass, e, ExecuteEvents.beginDragHandler);
        }

        public void OnDrag(PointerEventData e)
        {
            if (Mine(e))
            {
                OnGrabMove?.Invoke(Map(e.position, e.pressEventCamera));
                return;
            }
            if (grab) return;
            if (pass) ExecuteEvents.Execute(pass, e, ExecuteEvents.dragHandler);
        }

        public void OnEndDrag(PointerEventData e)
        {
            if (Mine(e) && grabDrag)
            {
                grab = grabDrag = false;
                down = null;
                OnGrabEnd?.Invoke(Map(e.position, e.pressEventCamera));
                return;
            }
            if (pass) ExecuteEvents.Execute(pass, e, ExecuteEvents.endDragHandler);
            if (down != null && e.pointerId == down.pointerId) down = null;
        }

        void OnDisable()
        {
            down = null;
            grab = grabDrag = held = noClick = panned = false;
        }
    }
}
