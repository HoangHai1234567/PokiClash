// Kéo bản đồ sảnh (đặt trên khung_anh của Screens/Hub, dựng bằng menu "PokiClash/Prefab/Sảnh và đảo/Đảo sảnh: ghép ảnh, kéo, mây viền"):
// kéo dời lớp ảnh (anh_nen_world: biển, đảo, mây viền, bảng vùng) trong giới hạn lề của ảnh đảo; quá giới hạn thì kéo nặng tay
// (dây chun) rồi bật về; thả tay thì trôi theo đà. Ra rìa là gặp vành mây che chỗ cho các đảo sau.
// Chạm (không kéo) vẫn tới bảng vùng, công trình bên dưới: kéo quá ngưỡng của EventSystem thì mới thành kéo.
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class HubPan : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler
    {
        [SerializeField] RectTransform target;
        [Tooltip("Giới hạn kéo, tỉ lệ theo cỡ lớp ảnh (x: ngang, y: dọc)")]
        [SerializeField] Vector2 limit = new Vector2(200 / 1080f, 200 / 1920f);
        [SerializeField] float rubber = 0.35f, spring = 10f, decay = 4f;
        [Tooltip("Kéo dư thêm (đơn vị UI) để mép trên / dưới bản đồ ra khỏi thanh trên / hàng nút đáy (bến tàu sát mép dưới)")]
        [SerializeField] float padTop, padBottom;

        Vector2 offset, velocity;
        Vector2? glide; // đích lướt tới (đưa một đảo vào giữa màn), kéo tay thì huỷ
        bool dragging;

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

        Vector2 Max => new Vector2(target.rect.width * limit.x, target.rect.height * limit.y);

        // khoảng dời được: offset.y dương đẩy ảnh lên (lộ mép dưới)
        Vector2 Lo => new Vector2(-Max.x, -Max.y - padTop);
        Vector2 Hi => new Vector2(Max.x, Max.y + padBottom);

        Vector2 Clamp(Vector2 o)
        {
            Vector2 lo = Lo, hi = Hi;
            return new Vector2(Mathf.Clamp(o.x, lo.x, hi.x), Mathf.Clamp(o.y, lo.y, hi.y));
        }

        // về giữa (vào sảnh)
        public void Recenter()
        {
            offset = velocity = Vector2.zero;
            glide = null;
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
            glide = Clamp(-local);
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
        }

        public void OnDrag(PointerEventData e)
        {
            var d = e.delta / Scale();
            Vector2 lo = Lo, hi = Hi;
            // quá giới hạn: kéo nặng dần
            if ((offset.x > hi.x && d.x > 0) || (offset.x < lo.x && d.x < 0)) d.x *= rubber;
            if ((offset.y > hi.y && d.y > 0) || (offset.y < lo.y && d.y < 0)) d.y *= rubber;
            offset += d;
            velocity = d / Mathf.Max(Time.unscaledDeltaTime, 0.001f);
            Apply();
        }

        public void OnEndDrag(PointerEventData e) => dragging = false;

        float Scale()
        {
            var c = target ? target.GetComponentInParent<Canvas>() : null;
            return c ? c.scaleFactor : 1;
        }

        void Update()
        {
            if (dragging || !target) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
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
            if (target) target.anchoredPosition = offset;
        }
    }
}
