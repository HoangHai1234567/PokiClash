// Kéo bản đồ sảnh (đặt trên khung_anh của Screens/Hub, dựng bằng menu "PokiClash/Prefab/Sảnh và đảo/Đảo sảnh: ghép ảnh, kéo, mây viền"):
// kéo dời lớp ảnh (anh_nen_world: biển, đảo, mây viền, bảng vùng) trong giới hạn lề của ảnh đảo; quá giới hạn thì kéo nặng tay
// (dây chun) rồi bật về; thả tay thì trôi theo đà. Ra rìa là gặp vành mây che chỗ cho các đảo sau.
// Chạm (không kéo) vẫn tới bảng vùng, công trình bên dưới: kéo quá ngưỡng của EventSystem thì mới thành kéo.
// Phóng to thu nhỏ nhẹ (đảo Casino, người dùng 2026-11-27): zoomMin < zoomMax thì hai ngón chụm / mở (hoặc lăn chuột) phóng lớp kéo quanh
// điểm giữa hai ngón; giới hạn kéo tính theo mức phóng (vùng nội dung = lớp kéo + lề kéo + kéo dư trên / dưới luôn phủ khung); chụm quá
// mức thì nặng tay rồi bật về. Mặc định zoomMin = zoomMax = 1: không phóng, kéo như cũ (sảnh, Nhà nông).
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class HubPan : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler, IScrollHandler
    {
        [SerializeField] RectTransform target;
        [Tooltip("Giới hạn kéo, tỉ lệ theo cỡ lớp ảnh (x: ngang, y: dọc)")]
        [SerializeField] Vector2 limit = new Vector2(200 / 1080f, 200 / 1920f);
        [SerializeField] float rubber = 0.35f, spring = 10f, decay = 4f;
        [Tooltip("Kéo dư thêm (đơn vị UI) để mép trên / dưới bản đồ ra khỏi thanh trên / hàng nút đáy (bến tàu sát mép dưới)")]
        [SerializeField] float padTop, padBottom;
        [Tooltip("Phóng nhỏ nhất / lớn nhất (bằng nhau: không phóng). Thu nhỏ quá cỡ phủ khung thì giữ mép trên, lộ thêm biển phía dưới")]
        [SerializeField] float zoomMin = 1, zoomMax = 1;

        Vector2 offset, velocity;
        Vector2? glide; // đích lướt tới (đưa một đảo vào giữa màn), kéo tay thì huỷ
        bool dragging;
        float zoom = 1;
        readonly Dictionary<int, Vector2> fingers = new Dictionary<int, Vector2>(); // ngón đang kéo: điểm màn hình
        float pinchDist;

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform layer, Vector2 limitFrac)
        {
            target = layer;
            limit = limitFrac;
        }

        public void SetPads(float top, float bottom)
        {
            padTop = top;
            padBottom = bottom;
        }

        // Dùng khi dựng prefab (Editor).
        public void SetZoom(float min, float max)
        {
            zoomMin = Mathf.Min(min, max);
            zoomMax = Mathf.Max(min, max);
        }

        bool CanZoom => zoomMax > zoomMin + 0.001f;
        public float Zoom => zoom;

        Vector2 Max => new Vector2(target.rect.width * limit.x, target.rect.height * limit.y);

        // khoảng dời được ở mức phóng z: offset.y dương đẩy ảnh lên (lộ mép dưới). Vùng nội dung (toạ độ lớp kéo) = khung lớp kéo nới thêm
        // lề kéo và kéo dư trên / dưới; khung nhìn (khung cha) luôn nằm trong vùng nội dung đã phóng. z = 1 trùng giới hạn cũ.
        void Range(float z, out Vector2 lo, out Vector2 hi)
        {
            var r = target.rect;
            var m = Max;
            var view = target.parent is RectTransform pr ? pr.rect : r;
            var bas = (Vector2)target.localPosition - target.anchoredPosition;
            float cx0 = r.xMin - m.x, cx1 = r.xMax + m.x, cy0 = r.yMin - m.y - padBottom, cy1 = r.yMax + m.y + padTop;
            lo = new Vector2(view.xMax - bas.x - z * cx1, view.yMax - bas.y - z * cy1);
            hi = new Vector2(view.xMin - bas.x - z * cx0, view.yMin - bas.y - z * cy0);
            // nội dung hẹp hơn khung (thu nhỏ): ngang canh giữa, dọc giữ mép trên
            if (lo.x > hi.x) lo.x = hi.x = (lo.x + hi.x) * 0.5f;
            if (lo.y > hi.y) hi.y = lo.y;
        }

        Vector2 Clamp(Vector2 o) => Clamp(o, zoom);

        Vector2 Clamp(Vector2 o, float z)
        {
            Range(z, out var lo, out var hi);
            return new Vector2(Mathf.Clamp(o.x, lo.x, hi.x), Mathf.Clamp(o.y, lo.y, hi.y));
        }

        // về giữa (vào sảnh)
        public void Recenter()
        {
            offset = velocity = Vector2.zero;
            glide = null;
            zoom = 1;
            fingers.Clear();
            dragging = false;
            Apply();
        }

        void OnEnable() => Recenter();

        // đặt chỗ nhìn (Nhà: lướt tới Nhà chính lúc vào)
        public void SetOffset(Vector2 o)
        {
            offset = o;
            velocity = Vector2.zero;
            Apply();
        }

        // lướt êm tới chỗ nhìn có điểm p (con bất kỳ của lớp kéo) ở giữa màn, kẹp trong giới hạn kéo
        public void GlideTo(RectTransform p)
        {
            if (!p || !target) return;
            Vector2 local = target.InverseTransformPoint(p.position);
            glide = Clamp(-local * zoom);
            velocity = Vector2.zero;
        }

        // đặt ngay chỗ nhìn để điểm p (con của lớp kéo) hiện ở vị trí thế giới w, kẹp trong giới hạn (bến tàu: chuyến tàu qua mây)
        public void FrameAt(RectTransform p, Vector3 w)
        {
            if (!p || !target) return;
            var parent = target.parent;
            Vector2 delta = parent ? (Vector2)parent.InverseTransformVector(w - p.position) : (Vector2)(w - p.position);
            offset = Clamp(offset + delta);
            velocity = Vector2.zero;
            glide = null;
            Apply();
        }

        public bool Gliding => glide.HasValue;

        public void OnBeginDrag(PointerEventData e)
        {
            dragging = true;
            glide = null;
            velocity = Vector2.zero;
            if (!CanZoom) return;
            fingers[e.pointerId] = e.position;
            if (fingers.Count == 2) pinchDist = PinchDist();
        }

        public void OnDrag(PointerEventData e)
        {
            if (CanZoom)
            {
                if (!fingers.ContainsKey(e.pointerId)) return;
                if (fingers.Count >= 2)
                {
                    var midOld = PinchMid();
                    fingers[e.pointerId] = e.position;
                    float dist = PinchDist();
                    ZoomAt(midOld, PinchMid(), zoom * dist / pinchDist, e.pressEventCamera, true);
                    pinchDist = dist;
                    velocity = Vector2.zero;
                    return;
                }
                fingers[e.pointerId] = e.position;
            }
            var d = e.delta / Scale();
            Range(zoom, out var lo, out var hi);
            // quá giới hạn: kéo nặng dần
            if ((offset.x > hi.x && d.x > 0) || (offset.x < lo.x && d.x < 0)) d.x *= rubber;
            if ((offset.y > hi.y && d.y > 0) || (offset.y < lo.y && d.y < 0)) d.y *= rubber;
            offset += d;
            velocity = d / Mathf.Max(Time.unscaledDeltaTime, 0.001f);
            Apply();
        }

        public void OnEndDrag(PointerEventData e)
        {
            if (!CanZoom)
            {
                dragging = false;
                return;
            }
            fingers.Remove(e.pointerId);
            if (fingers.Count == 1) velocity = Vector2.zero; // còn một ngón: kéo tiếp, không trôi theo cú chụm
            if (fingers.Count == 0) dragging = false;
        }

        public void OnScroll(PointerEventData e)
        {
            if (!CanZoom || !target) return;
            glide = null;
            velocity = Vector2.zero;
            ZoomAt(e.position, e.position, zoom * (1 + e.scrollDelta.y * 0.1f), e.pressEventCamera, false);
        }

        float PinchDist()
        {
            var it = fingers.Values.GetEnumerator();
            it.MoveNext();
            var a = it.Current;
            it.MoveNext();
            return Mathf.Max(1, Vector2.Distance(a, it.Current));
        }

        Vector2 PinchMid()
        {
            var s = Vector2.zero;
            foreach (var f in fingers.Values) s += f;
            return s / Mathf.Max(1, fingers.Count);
        }

        // điểm màn hình → toạ độ khung cha của lớp kéo
        Vector2 ParentPoint(Vector2 screen, Camera cam)
        {
            var parent = target.parent as RectTransform;
            if (!parent) return screen / Scale();
            RectTransformUtility.ScreenPointToLocalPointInRectangle(parent, screen, cam, out var l);
            return l;
        }

        // phóng quanh một điểm màn hình: điểm bản đồ dưới ngón (from) đi theo ngón (to); chụm quá mức thì nặng tay (soft), bật về ở Update
        void ZoomAt(Vector2 fromScreen, Vector2 toScreen, float z, Camera cam, bool soft)
        {
            float lo = zoomMin * (soft ? 0.95f : 1), hi = zoomMax * (soft ? 1.08f : 1);
            z = Mathf.Clamp(z, lo, hi);
            if (Mathf.Approximately(z, zoom) && fromScreen == toScreen) return;
            var bas = (Vector2)target.localPosition - target.anchoredPosition;
            var from = ParentPoint(fromScreen, cam);
            var to = ParentPoint(toScreen, cam);
            var m = (from - bas - offset) / zoom; // điểm lớp kéo dưới ngón
            zoom = z;
            offset = to - bas - z * m;
            if (!soft) offset = Clamp(offset);
            Apply();
        }

        float Scale()
        {
            var c = target ? target.GetComponentInParent<Canvas>() : null;
            return c ? c.scaleFactor : 1;
        }

        NotchBleed notch; // vùng tai thỏ thấy luôn bản đồ (App/NotchBleed)

        void Update()
        {
            notch.Tick(this);
            if (dragging || !target) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            // chụm quá mức (thả tay): bật về quanh giữa khung
            float zc = Mathf.Clamp(zoom, Mathf.Min(zoomMin, 1), Mathf.Max(zoomMax, 1));
            if (!Mathf.Approximately(zc, zoom))
            {
                var bas = (Vector2)target.localPosition - target.anchoredPosition;
                var c = target.parent is RectTransform pr ? pr.rect.center : Vector2.zero;
                var m = (c - bas - offset) / zoom;
                zoom = Mathf.Lerp(zoom, zc, 1 - Mathf.Exp(-spring * dt));
                if (Mathf.Abs(zoom - zc) < 0.002f) zoom = zc;
                offset = c - bas - zoom * m;
            }
            if (glide.HasValue)
            {
                offset = Vector2.Lerp(offset, glide.Value, 1 - Mathf.Exp(-5f * dt));
                if ((offset - glide.Value).sqrMagnitude < 1)
                {
                    offset = glide.Value;
                    glide = null;
                }
                Apply();
                return;
            }
            offset += velocity * dt;
            velocity *= Mathf.Exp(-decay * dt);
            // bật về trong giới hạn
            var clamped = Clamp(offset);
            if (clamped != offset)
            {
                offset = Vector2.Lerp(offset, clamped, 1 - Mathf.Exp(-spring * dt));
                if (clamped.x != offset.x && Mathf.Sign(velocity.x) == Mathf.Sign(offset.x - clamped.x)) velocity.x = 0;
                if (clamped.y != offset.y && Mathf.Sign(velocity.y) == Mathf.Sign(offset.y - clamped.y)) velocity.y = 0;
            }
            if (velocity.sqrMagnitude < 1 && (offset - clamped).sqrMagnitude < 0.25f) velocity = Vector2.zero;
            Apply();
        }

        void Apply()
        {
            if (!target) return;
            target.anchoredPosition = offset;
            if (CanZoom) target.localScale = new Vector3(zoom, zoom, 1); // không phóng (sảnh, Nhà nông): không đụng cỡ lớp kéo
        }
    }
}
