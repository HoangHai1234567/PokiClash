// Kéo bản đồ sảnh (đặt trên khung_anh của Screens/Hub, dựng bằng menu "PokiClash/Prefab/Đảo sảnh: ghép ảnh, kéo, mây viền"):
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

        Vector2 offset, velocity;
        bool dragging;

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform layer, Vector2 limitFrac)
        {
            target = layer;
            limit = limitFrac;
        }

        Vector2 Max => new Vector2(target.rect.width * limit.x, target.rect.height * limit.y);

        // về giữa (vào sảnh)
        public void Recenter()
        {
            offset = velocity = Vector2.zero;
            Apply();
        }

        void OnEnable() => Recenter();

        public void OnBeginDrag(PointerEventData e)
        {
            dragging = true;
            velocity = Vector2.zero;
        }

        public void OnDrag(PointerEventData e)
        {
            var d = e.delta / Scale();
            var max = Max;
            // quá giới hạn: kéo nặng dần
            if (Mathf.Abs(offset.x) > max.x && Mathf.Sign(d.x) == Mathf.Sign(offset.x)) d.x *= rubber;
            if (Mathf.Abs(offset.y) > max.y && Mathf.Sign(d.y) == Mathf.Sign(offset.y)) d.y *= rubber;
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
            var max = Max;
            offset += velocity * dt;
            velocity *= Mathf.Exp(-decay * dt);
            // bật về trong giới hạn
            var clamped = new Vector2(Mathf.Clamp(offset.x, -max.x, max.x), Mathf.Clamp(offset.y, -max.y, max.y));
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
