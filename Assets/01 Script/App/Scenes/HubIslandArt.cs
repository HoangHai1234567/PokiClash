// Một đảo trên bản đồ thế giới sảnh (ảnh đảo tách riêng, ArtGen/Islands/sanh_moi/tach_dao.py). Người dùng 2026-11-19: "làm các đảo ở đảo
// chính có hiệu ứng kiểu glowing nhẹ với gam màu chủ đạo của đảo đó để người chơi biết họ có thể click vào đó và khi click thì nhún nhẹ".
// - Chi tiết chính của đảo phát sáng (người dùng: "chọn 1 chi tiết chính của đảo làm sáng lên": Mộc cây thần, Kim ông mặt trời, Hỏa miệng
//   núi lửa, Thổ đền mặt trời; Thủy cổng rồng): quầng mềm quanh viền chi tiết (sanh_sang_<hệ>, bên trong trống nên chi tiết giữ nguyên
//   màu: không sáng loang cả đảo vì "màu nó mờ đi"), cộng sáng màu hệ, thở nhẹ; đảo chưa mở (mây che) thì tắt.
// - Bấm theo đúng hình đảo: mặt nạ thô nướng sẵn lúc dựng prefab (không cần bật đọc ảnh); kéo bản đồ vẫn thông qua (HubPan ở cha).
// - Bấm: đảo (cùng quầng) nhún: bẹp xuống, nảy lên, lắng lại quanh chân đảo; rồi gọi OnClick (sảnh: vào đảo như bấm bảng tên).
// Dựng bằng menu "PokiClash/Prefab/Sảnh bản đồ thế giới" (HubMapMenu): gốc "dao_<hệ>" (phủ khung ảnh đảo, gốc ở chân đảo) có con
// "sang" (quầng) rồi "hinh" (ảnh đảo, component này).
using System;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HubIslandArt : MonoBehaviour, ICanvasRaycastFilter, IPointerClickHandler
    {
        [SerializeField] Elem zone;
        [SerializeField] RectTransform root; // gốc nhún (chân đảo)
        [SerializeField] Image glow;
        [SerializeField] int maskW, maskH;
        [SerializeField] byte[] mask = new byte[0]; // 1 = đất, hàng từ trên xuống

        public Elem Zone => zone;
        public Action OnClick;

        bool open = true;
        float t, bounce = 1, glowA;
        Color tint = Color.white;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Elem z, RectTransform bounceRoot, Image glowImg, int w, int h, byte[] bits)
        {
            zone = z;
            root = bounceRoot;
            glow = glowImg;
            maskW = w;
            maskH = h;
            mask = bits;
        }

        void Awake()
        {
            // màu chủ đạo của hệ, pha trắng cho sáng lên trên biển (Thủy lam trên biển lam: pha nhiều hơn)
            var c = Theme.Of(zone);
            tint = Color.Lerp(c, Color.white, zone == Elem.Thuy ? 0.4f : 0.15f);
            t = (int)zone * 0.9f;
        }

        public void SetOpen(bool on) => open = on;

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
            bounce = 0;
            OnClick?.Invoke();
        }

        // chỉ nhún (tour thử)
        public void Poke() => bounce = 0;

        void Update()
        {
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            t += dt;
            if (glow)
            {
                // thở nhẹ 2,6 giây một nhịp; bấm thì bừng lên rồi lắng
                float want = open ? 0.32f + 0.5f * (0.5f + 0.5f * Mathf.Sin(t * 2.4f)) : 0;
                if (bounce < 1) want = Mathf.Max(want, 1 - bounce * 0.5f);
                glowA = Mathf.Lerp(glowA, want, 1 - Mathf.Exp(-8 * dt));
                bool on = glowA > 0.01f;
                if (glow.enabled != on) glow.enabled = on;
                if (on) glow.color = new Color(tint.r, tint.g, tint.b, glowA);
            }
            if (root)
            {
                if (bounce < 1)
                {
                    bounce = Mathf.Min(1, bounce + dt / 0.45f);
                    float w = Mathf.Sin(bounce * Mathf.PI * 3) * (1 - bounce);
                    root.localScale = new Vector3(1 + 0.035f * w, 1 - 0.055f * w, 1);
                }
                else if (root.localScale != Vector3.one) root.localScale = Vector3.one;
            }
        }
    }
}
