// Vùng tai thỏ / lỗ camera trong suốt (người dùng 2026-11-27: "bỏ cái phần màu xanh nước biển ở trên đi để nó trong suốt", "phần safe zone
// camera giờ bạn để trong suốt hết cho tôi"). Khung nhìn bản đồ (có RectMask2D) nằm trong vùng an toàn, nên phía trên vùng an toàn chỉ còn
// lớp nền của canvas (màn đảo: dải biển lặp sea_tile). Nới vùng cắt của mask lên tới mép trên màn (padding trên âm): bản đồ, biển quanh
// đảo, mây vành vẽ tràn lên vùng tai thỏ. Khung, lề che, giới hạn kéo, mức zoom giữ nguyên. Chỉ nới khi mép trên khung trùng mép trên vùng
// an toàn. Gọi mỗi khung từ LandView (đảo, Nhà) và HubPan (sảnh, Casino); chỉ tính lại khi màn / vùng an toàn đổi.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public struct NotchBleed
    {
        static readonly Vector3[] C = new Vector3[4];

        RectMask2D mask;
        bool looked;
        Rect lastSafe;
        Vector2Int lastScreen;
        float lastTop;

        public void Tick(Component owner)
        {
            if (!looked)
            {
                looked = true;
                mask = owner ? owner.GetComponent<RectMask2D>() : null;
            }
            if (!mask) return;
            var safe = SafeRect();
            var scr = new Vector2Int(Screen.width, Screen.height);
            var rt = mask.rectTransform;
            float top = rt.rect.yMax;
            if (safe == lastSafe && scr == lastScreen && Mathf.Approximately(top, lastTop)) return;
            lastSafe = safe;
            lastScreen = scr;
            lastTop = top;
            var p = mask.padding;
            p.w = -Bleed(rt, safe);
            mask.padding = p;
        }

        static Rect SafeRect()
        {
            var s = SafeArea.Simulated;
            return s.width > 0 ? new Rect(s.x * Screen.width, s.y * Screen.height, s.width * Screen.width, s.height * Screen.height) : Screen.safeArea;
        }

        // khoảng từ mép trên r tới mép trên màn (đơn vị local của r) nếu mép trên r nằm ở mép trên vùng an toàn; không thì 0
        static float Bleed(RectTransform r, Rect safe)
        {
            float sh = Screen.height;
            if (sh <= 0 || safe.yMax >= sh - 0.5f) return 0;
            var canvas = r.GetComponentInParent<Canvas>();
            if (!canvas) return 0;
            ((RectTransform)canvas.rootCanvas.transform).GetWorldCorners(C);
            float top = C[1].y, perPx = (C[1].y - C[0].y) / sh;
            if (perPx <= 0) return 0;
            float safeTop = top - (sh - safe.yMax) * perPx;
            r.GetWorldCorners(C);
            float rTop = C[1].y;
            if (Mathf.Abs(rTop - safeTop) > 3 * perPx) return 0;
            float s = r.lossyScale.y;
            return s > 0 ? Mathf.Max(0, (top - rTop) / s) : 0;
        }
    }
}
