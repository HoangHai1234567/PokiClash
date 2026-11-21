// Camera của đảo vùng đất (GD_Claude/18, góp ý 2026-11-18 "gần quá, cho zoom ra vào, vào đảo phải nhìn được toàn đảo"): đặt trên
// khung cuộn của Screens/Zone (cùng chỗ ScrollRect, menu PokiClash/Đảo vùng đất/Dựng nước, ảnh); đảo vùng đất tắt ScrollRect, bật cái này.
// - Một ngón kéo: dời bản đồ, thả tay trôi theo đà; ra quá mép thì nặng tay rồi bật về.
// - Hai ngón chụm / mở (hoặc lăn chuột): zoom quanh điểm giữa hai ngón; zoom nhỏ nhất là vừa khít cả đảo trong khung nhìn (trừ khung
//   trên, khung dưới), lớn nhất 1 (cỡ thật của chấm ải, tướng). Vào đảo dùng CoverZoom: bản đồ vừa phủ kín khung (máy dọc là vừa khít
//   chiều cao đảo, kéo ngang xem hết); người dùng 2026-11-18: "được zoom ra như vậy nhưng khi vào thì không zoom ra nhiều như vậy".
// - Show(điểm, zoom, giây): lướt tới; bản đồ nhỏ hơn khung thì canh giữa.
// Toạ độ bản đồ: (x, y) px vùng đất, gốc trên trái, y xuống. Toạ độ khung: từ góc trên trái khung nhìn, y xuống.
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using PokiClash.Core;

namespace PokiClash
{
    public sealed class LandView : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler, IScrollHandler
    {
        [SerializeField] float rubber = 0.35f, spring = 10f, decay = 4.5f, maxZoom = 1f;

        RectTransform content;
        Vector2 size;          // cỡ bản đồ (px vùng đất)
        float insetT, insetB;  // khung trên, khung dưới che mất bao nhiêu của khung nhìn
        Vector4 margin;        // vùng được nhìn ra ngoài ảnh (trái, phải, trên, dưới; px bản đồ): vành mây (người dùng 2026-11-18:
                               // zoom ra tối đa chỉ tới khi mây phủ kín màn, kéo không được lộ phần trắng quanh mây)
        const float MaxOver = 120; // kéo quá mép tối đa (px khung), chụm quá zoom nhỏ nhất tối đa 3%
        Vector2 pos, vel;      // anchoredPosition của lớp nội dung (neo trên trái), tốc trôi
        float zoom = 1;
        bool dragging;
        readonly Dictionary<int, Vector2> fingers = new Dictionary<int, Vector2>();
        float pinchDist;
        // lướt tới
        bool tween;
        float tT, tDur, z0, z1;
        Vector2 p0, p1;
        Vector2 lastView;

        public bool On { get; private set; }
        public float Zoom => zoom;
        public float MinZoom { get; private set; } = 1;
        public float MaxZoom => maxZoom;

        // zoom lúc vào đảo: bản đồ vừa phủ kín phần khung không bị che
        public float CoverZoom
        {
            get
            {
                var v = ViewSize;
                if (v.x <= 0 || size.x <= 0) return 1;
                return Mathf.Clamp(Mathf.Max(v.x / size.x, Mathf.Max(1, WinH) / size.y), MinZoom, maxZoom);
            }
        }
        public event Action Changed; // zoom hoặc chỗ đổi (cập nhật cỡ chấm, bảng tên, tướng nào đang trong khung)

        RectTransform View => (RectTransform)content.parent;
        public Vector2 ViewSize => content ? View.rect.size : Vector2.zero;
        float WinH => ViewSize.y - insetT - insetB;

        public void Begin(RectTransform layer, Vector2 mapSize, float top, float bottom, Vector4 around = default)
        {
            content = layer;
            size = mapSize;
            insetT = top;
            insetB = bottom;
            margin = around;
            On = true;
            enabled = true;
            tween = false;
            vel = Vector2.zero;
            fingers.Clear();
            MinZoom = Fit();
            zoom = MinZoom;
            pos = PosFor(size * 0.5f, zoom);
            lastView = ViewSize;
            Apply();
        }

        public void End()
        {
            On = false;
            fingers.Clear();
            if (content) content.localScale = Vector3.one;
        }

        float Fit()
        {
            var v = ViewSize;
            if (v.x <= 0 || size.x <= 0) return 1;
            // có vành mây: zoom ra tối đa là khi ảnh + vành mây vừa phủ kín cả màn; không có thì vừa khít cả đảo trong khung
            if (margin != Vector4.zero)
                return Mathf.Min(maxZoom, Mathf.Max(v.x / (size.x + margin.x + margin.y), v.y / (size.y + margin.z + margin.w)));
            return Mathf.Min(maxZoom, Mathf.Min(v.x / size.x, Mathf.Max(1, WinH) / size.y));
        }

        // điểm bản đồ → điểm khung
        public Vector2 ToView(Vector2 m) => new Vector2(pos.x + m.x * zoom, m.y * zoom - pos.y);

        // điểm khung → điểm bản đồ
        Vector2 ToMap(Vector2 v, float z, Vector2 p) => new Vector2((v.x - p.x) / z, (v.y + p.y) / z);

        // chỗ lớp nội dung để điểm m nằm giữa phần khung không bị che
        Vector2 PosFor(Vector2 m, float z)
        {
            var v = ViewSize;
            var c = new Vector2(v.x * 0.5f, insetT + WinH * 0.5f);
            return Clamp(new Vector2(c.x - m.x * z, m.y * z - c.y), z);
        }

        // giữ bản đồ phủ kín khung (trừ khung trên, dưới); bản đồ nhỏ hơn khung thì canh giữa
        Vector2 Clamp(Vector2 p, float z)
        {
            var v = ViewSize;
            if (margin != Vector4.zero)
            {
                // khung nhìn luôn nằm trong ảnh + vành mây (không lộ khối phủ ngoài)
                float W2 = (size.x + margin.x + margin.y) * z, H2 = (size.y + margin.z + margin.w) * z;
                p.x = W2 >= v.x ? Mathf.Clamp(p.x, v.x - (size.x + margin.y) * z, margin.x * z) : (v.x - W2) * 0.5f + margin.x * z;
                p.y = H2 >= v.y ? Mathf.Clamp(p.y, -margin.z * z, (size.y + margin.w) * z - v.y) : -((v.y - H2) * 0.5f + margin.z * z);
                return p;
            }
            float W = size.x * z, H = size.y * z;
            p.x = W >= v.x ? Mathf.Clamp(p.x, v.x - W, 0) : (v.x - W) * 0.5f;
            p.y = H >= WinH ? Mathf.Clamp(p.y, -insetT, H - (v.y - insetB)) : -(insetT + (WinH - H) * 0.5f);
            return p;
        }

        public void Show(Vector2 m, float z, float dur)
        {
            if (!On) return;
            z = Mathf.Clamp(z, MinZoom, maxZoom);
            var to = PosFor(m, z);
            vel = Vector2.zero;
            if (dur <= 0)
            {
                tween = false;
                zoom = z;
                pos = to;
                Apply();
                return;
            }
            tween = true;
            tT = 0;
            tDur = dur;
            z0 = zoom;
            z1 = z;
            p0 = pos;
            p1 = to;
        }

        public void ShowAll(float dur) => Show(size * 0.5f, MinZoom, dur);

        // dời bản đồ một vectơ thế giới (điểm đang ở a sẽ hiện ở a + d), giữ trong mép: bến tàu màn Nhà đặt máy theo tàu lúc cập bến
        public void ShiftWorld(Vector3 d)
        {
            if (!On) return;
            tween = false;
            vel = Vector2.zero;
            pos = Clamp(pos + (Vector2)View.InverseTransformVector(d), zoom);
            Apply();
        }

        // dời bản đồ d px khung (y xuống), giữ trong mép: màn Nhà kéo quái tới mép khung thì bản đồ tự trôi theo
        public void Nudge(Vector2 d)
        {
            if (!On || d == Vector2.zero) return;
            tween = false;
            vel = Vector2.zero;
            pos = Clamp(new Vector2(pos.x + d.x, pos.y - d.y), zoom);
            Apply();
        }

        // tour thử: trạng thái để ghi log
        public string Describe() =>
            Loc.F("zoom {0:0.###} (min {1:0.###}, max {2:0.###}) pos {3} view {4} tween {5} kéo {6} ngón {7}", zoom, MinZoom, maxZoom, pos, ViewSize, tween, dragging, fingers.Count);

        Vector2 Local(PointerEventData e)
        {
            RectTransformUtility.ScreenPointToLocalPointInRectangle(View, e.position, e.pressEventCamera, out var l);
            var r = View.rect;
            return new Vector2(l.x - r.xMin, r.yMax - l.y);
        }

        public void OnBeginDrag(PointerEventData e)
        {
            if (!On) return;
            tween = false;
            vel = Vector2.zero;
            dragging = true;
            fingers[e.pointerId] = Local(e);
            if (fingers.Count == 2) pinchDist = PinchDist();
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

        public void OnDrag(PointerEventData e)
        {
            if (!On || !fingers.ContainsKey(e.pointerId)) return;
            var now = Local(e);
            var prev = fingers[e.pointerId];
            if (fingers.Count >= 2)
            {
                var midOld = PinchMid();
                fingers[e.pointerId] = now;
                float d = PinchDist();
                var mid = PinchMid();
                ZoomAt(midOld, mid, zoom * d / pinchDist, true);
                pinchDist = d;
                return;
            }
            fingers[e.pointerId] = now;
            var delta = now - prev;
            var raw = pos + new Vector2(delta.x, -delta.y);
            var cl = Clamp(raw, zoom);
            // quá mép: kéo nặng dần
            if (!Mathf.Approximately(raw.x, cl.x)) delta.x *= rubber;
            if (!Mathf.Approximately(raw.y, cl.y)) delta.y *= rubber;
            pos += new Vector2(delta.x, -delta.y);
            // nhún quá mép có giới hạn: kéo mạnh tay cũng không lộ phần trắng quanh vành mây
            var lim = Clamp(pos, zoom);
            pos = new Vector2(Mathf.Clamp(pos.x, lim.x - MaxOver, lim.x + MaxOver), Mathf.Clamp(pos.y, lim.y - MaxOver, lim.y + MaxOver));
            vel = new Vector2(delta.x, -delta.y) / Mathf.Max(Time.unscaledDeltaTime, 0.001f);
            Apply();
        }

        public void OnEndDrag(PointerEventData e)
        {
            fingers.Remove(e.pointerId);
            if (fingers.Count == 1) vel = Vector2.zero;
            if (fingers.Count == 0) dragging = false;
        }

        public void OnScroll(PointerEventData e)
        {
            if (!On) return;
            tween = false;
            var at = Local(e);
            ZoomAt(at, at, zoom * (1 + e.scrollDelta.y * 0.12f), false);
        }

        // zoom quanh một điểm khung: điểm bản đồ dưới ngón (from) đi theo ngón (to); chụm quá giới hạn thì nặng tay rồi bật về
        void ZoomAt(Vector2 from, Vector2 to, float z, bool soft)
        {
            float lo = MinZoom * (soft ? 0.97f : 1), hi = maxZoom * (soft ? 1.12f : 1);
            z = Mathf.Clamp(z, lo, hi);
            var m = ToMap(from, zoom, pos);
            zoom = z;
            pos = new Vector2(to.x - m.x * z, m.y * z - to.y);
            var lim = Clamp(pos, zoom);
            pos = soft ? new Vector2(Mathf.Clamp(pos.x, lim.x - MaxOver, lim.x + MaxOver), Mathf.Clamp(pos.y, lim.y - MaxOver, lim.y + MaxOver)) : lim;
            Apply();
        }

        // khung nhìn đổi cỡ (xoay, tai thỏ, khung đầu tiên chưa xếp xong) mà chưa tính lại thì tính ngay: zoom vừa đảo, giữ trong mép.
        // Màn gọi trước khi đặt máy ngay (bến tàu), để khung sau Update không dời máy nữa.
        public void Sync()
        {
            if (!On || !content || ViewSize == lastView) return;
            lastView = ViewSize;
            bool atMin = Mathf.Approximately(zoom, MinZoom);
            MinZoom = Fit();
            if (atMin || zoom < MinZoom) zoom = MinZoom;
            pos = Clamp(pos, zoom);
            Apply();
        }

        void Update()
        {
            if (!On || !content) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            Sync();
            if (tween)
            {
                tT += dt;
                float k = Mathf.Clamp01(tT / tDur);
                k = 1 - (1 - k) * (1 - k) * (1 - k);
                zoom = Mathf.Lerp(z0, z1, k);
                pos = Vector2.Lerp(p0, p1, k);
                if (tT >= tDur) tween = false;
                Apply();
                return;
            }
            if (dragging) return;
            bool moved = false;
            // zoom quá giới hạn (chụm mạnh tay): bật về quanh giữa khung
            float zc = Mathf.Clamp(zoom, MinZoom, maxZoom);
            if (!Mathf.Approximately(zc, zoom))
            {
                var v = ViewSize;
                var c = new Vector2(v.x * 0.5f, insetT + WinH * 0.5f);
                var m = ToMap(c, zoom, pos);
                zoom = Mathf.Lerp(zoom, zc, 1 - Mathf.Exp(-spring * dt));
                if (Mathf.Abs(zoom - zc) < 0.002f) zoom = zc;
                pos = new Vector2(c.x - m.x * zoom, m.y * zoom - c.y);
                moved = true;
            }
            if (vel.sqrMagnitude > 1)
            {
                pos += vel * dt;
                vel *= Mathf.Exp(-decay * dt);
                moved = true;
            }
            var cl = Clamp(pos, zoom);
            if ((cl - pos).sqrMagnitude > 0.25f)
            {
                pos = Vector2.Lerp(pos, cl, 1 - Mathf.Exp(-spring * dt));
                if (!Mathf.Approximately(cl.x, pos.x) && Mathf.Sign(vel.x) == Mathf.Sign(pos.x - cl.x)) vel.x = 0;
                if (!Mathf.Approximately(cl.y, pos.y) && Mathf.Sign(vel.y) == Mathf.Sign(pos.y - cl.y)) vel.y = 0;
                moved = true;
            }
            if (moved) Apply();
        }

        void Apply()
        {
            content.localScale = new Vector3(zoom, zoom, 1);
            content.anchoredPosition = pos;
            Changed?.Invoke();
        }
    }
}
