// Ngưỡng kéo theo chỗ chạm (người dùng 2026-11-27: "tap phản hồi trong shop bị delay và scroll chưa được mượt"). App đặt ngưỡng kéo chung
// ~2,5 mm (2026-11-20: giữ tướng, chạm camera trên bản đồ không bị trôi), nên danh sách cuộn phải kéo 40–45 px trên điện thoại mới bắt đầu
// chạy, cảm giác dính và trễ. Lúc nhấn xuống, dò chỗ chạm: thứ nhận kéo là ScrollRect của danh sách (không phải khung bản đồ LandView,
// HubPan) thì hạ ngưỡng còn ~1 mm cho lần chạm đó; chạm chỗ khác thì trả ngưỡng chung. App.Update gọi Tick mỗi khung.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.UI;

namespace PokiClash
{
    public static class ListDrag
    {
        static readonly List<RaycastResult> Hits = new List<RaycastResult>();
        static int normal = -1; // ngưỡng chung (App đặt lúc mở game)
        static bool low;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void Reset()
        {
            normal = -1;
            low = false;
        }

        public static void Tick()
        {
            var es = EventSystem.current;
            var ptr = Pointer.current;
            if (!es || ptr == null) return;
            if (!low) normal = es.pixelDragThreshold;
            if (!ptr.press.wasPressedThisFrame) return;
            bool list = InList(es, ptr.position.ReadValue());
            if (list && !low)
            {
                normal = es.pixelDragThreshold;
                es.pixelDragThreshold = Mathf.Min(normal, Mathf.Max(10, Mathf.RoundToInt((Screen.dpi > 0 ? Screen.dpi : 160) * 0.045f)));
                low = true;
            }
            else if (!list && low)
            {
                es.pixelDragThreshold = normal;
                low = false;
            }
        }

        // thứ sẽ nhận kéo ở chỗ chạm (như EventSystem chọn: cha gần nhất có IDragHandler) là ScrollRect của danh sách
        static bool InList(EventSystem es, Vector2 pos)
        {
            Hits.Clear();
            es.RaycastAll(new PointerEventData(es) { position = pos }, Hits);
            if (Hits.Count == 0 || !Hits[0].gameObject) return false;
            var h = ExecuteEvents.GetEventHandler<IDragHandler>(Hits[0].gameObject);
            Hits.Clear();
            return h && h.TryGetComponent<ScrollRect>(out var sr) && sr.enabled && !h.GetComponent<LandView>() && !h.GetComponent<HubPan>();
        }
    }
}
