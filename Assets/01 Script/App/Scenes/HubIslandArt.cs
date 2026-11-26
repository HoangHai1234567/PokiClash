// Một đảo trên bản đồ thế giới sảnh (ảnh đảo tách riêng, ArtGen/Islands/sanh_moi/tach_dao.py).
// - Bấm theo đúng hình đảo: mặt nạ thô nướng sẵn lúc dựng prefab (không cần bật đọc ảnh); kéo bản đồ vẫn thông qua (HubPan ở cha).
// - Bấm: gọi OnClick (sảnh: vào đảo như bấm bảng tên). Bỏ nhún khi chạm (người dùng 2026-11-26: "bỏ phần tap nhún đảo khi tap vào đảo đi");
//   Poke() vẫn nhún cho các lượt chụp cũ (HubMapTour, HubNightTour).
// - Đèn đêm (người dùng 2026-11-20: "buổi đêm các đảo sáng lên, người chơi phải biết click được vào đảo; ban ngày không cần sáng, chiều tối
//   thì cần; không dùng mũi tên"; bỏ quầng sáng thở cả ngày của 2026-11-19): nhóm "dem_<hệ>" trên lớp nhuộm đêm (đuốc thắp, chỗ phát
//   sáng; shader tự sáng theo giờ qua _PokiNight) nhún cùng đảo, ẩn khi đảo chưa mở (mây che). Dựng: HubNightMenu.
// Dựng bằng menu "PokiClash/Prefab/Sảnh bản đồ thế giới" (HubMapMenu): gốc "dao_<hệ>" (phủ khung ảnh đảo, gốc ở chân đảo) có con
// "hinh" (ảnh đảo, component này).
using System;
using PokiClash.Core;
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class HubIslandArt : MonoBehaviour, ICanvasRaycastFilter, IPointerClickHandler
    {
        [SerializeField] Elem zone;
        [SerializeField] RectTransform root; // gốc nhún (chân đảo)
        [Tooltip("Nhóm đèn đêm của đảo (lớp den_dao, trên lớp nhuộm): nhún cùng đảo, ẩn khi đảo chưa mở")]
        [SerializeField] RectTransform night;
        [SerializeField] int maskW, maskH;
        [SerializeField] byte[] mask = new byte[0]; // 1 = đất, hàng từ trên xuống

        public Elem Zone => zone;
        public Action OnClick;

        bool open = true;
        float bounce = 1;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Elem z, RectTransform bounceRoot, int w, int h, byte[] bits)
        {
            zone = z;
            root = bounceRoot;
            maskW = w;
            maskH = h;
            mask = bits;
        }

        // Dùng khi dựng prefab (Editor, HubNightMenu).
        public void SetNight(RectTransform group) => night = group;

        public void SetOpen(bool on)
        {
            open = on;
            if (night && night.gameObject.activeSelf != on) night.gameObject.SetActive(on);
        }

        public bool IsRaycastLocationValid(Vector2 sp, Camera cam)
        {
            if (!open || mask == null || mask.Length == 0) return false;
            var rt = (RectTransform)transform;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(rt, sp, cam, out var lp)) return false;
            var r = rt.rect;
            float u = (lp.x - r.xMin) / r.width, v = (lp.y - r.yMin) / r.height;
            if (u < 0 || u >= 1 || v < 0 || v >= 1) return false;
            int x = Mathf.Clamp((int)(u * maskW), 0, maskW - 1), y = Mathf.Clamp((int)((1 - v) * maskH), 0, maskH - 1);
            return mask[y * maskW + x] != 0;
        }

        public void OnPointerClick(PointerEventData e)
        {
            if (!open) return;
            OnClick?.Invoke();
        }

        // chỉ nhún (tour thử)
        public void Poke() => bounce = 0;

        void Update()
        {
            if (!root) return;
            var s = Vector3.one;
            if (bounce < 1)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
                bounce = Mathf.Min(1, bounce + dt / 0.45f);
                float w = Mathf.Sin(bounce * Mathf.PI * 3) * (1 - bounce);
                s = new Vector3(1 + 0.035f * w, 1 - 0.055f * w, 1);
            }
            if (root.localScale != s) root.localScale = s;
            if (night && night.localScale != s) night.localScale = s;
        }
    }
}
