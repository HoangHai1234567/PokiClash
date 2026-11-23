// Vòng nút quanh vật đang chọn ở màn Nhà (học nút thao tác pbui_buildi_operationbar_item của Clash of Critters, người dùng 2026-11-22:
// "các button / điều khiển chức năng chưa rõ ràng, đục sâu vào Clash of Critters"): thay bảng chữ ở đáy. Các nút tròn icon
// (HomeRingButton) xếp hình quạt trên đầu vật, nhãn tên + một dòng trạng thái nằm dưới chân vật; cả cụm bám theo vật khi kéo, phóng bản đồ
// (đổi toạ độ qua camera mỗi khung, không nằm trong lớp kéo nên cỡ nút không đổi theo phóng). Vật sát mép trên thì quạt lật xuống dưới chân.
// Hiện thì từng nút nảy ra lần lượt (như hoạt cảnh anfx_btn_click_bite của Critters). Prefab: nút "vong" trong nha_ui của Screens/Home
// (menu "PokiClash/Prefab/Nhà và side meta/Nhà và side meta∕Nhà: giao diện kiểu Critters").
using System;
using System.Collections.Generic;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    // một nút của vòng: icon (tên trong ArtLibrary hoặc sprite), chữ ngắn, dòng giá, màu lõi, bật / khoá, việc bấm, việc khi khoá
    public struct RingItem
    {
        public Sprite icon;
        public string label, cost;
        public BtnColor color;
        public bool on;
        public Action act, denied;

        public RingItem(Sprite icon, string label, BtnColor color, Action act, string cost = null, bool on = true, Action denied = null)
        {
            this.icon = icon;
            this.label = label;
            this.color = color;
            this.act = act;
            this.cost = cost;
            this.on = on;
            this.denied = denied;
        }
    }

    public sealed class HomeRing : MonoBehaviour
    {
        // khoảng cách giữa hai nút, độ cong quạt (px hạ mỗi px² lệch giữa), khoảng trên đỉnh vật, lề màn
        public const float Step = 150, Curve = 0.0009f, Lift = 96, Margin = 70, TagGap = 22, PopLen = 0.28f, PopStagger = 0.045f;
        // dưới tâm nút còn: nửa nút + chữ + dòng giá + khe (nhãn tên không được chạm phần này khi vật nhỏ như mốc ô rừng)
        public const float BelowButton = 56 + 36 + 40 + 12;

        [SerializeField] HomeRingButton[] slots; // dựng sẵn trong prefab (tắt)
        [SerializeField] RectTransform tag; // nhãn tên dưới chân vật
        [SerializeField] TextMeshProUGUI tagTitle, tagSub;

        RectTransform target;
        Canvas targetCanvas, ownCanvas;
        int count;
        float popT = -1;
        float topInset, bottomInset;
        readonly Vector3[] corners = new Vector3[4];

        public bool On => gameObject.activeSelf && target;
        public RectTransform Target => target;
        RectTransform Rt => (RectTransform)transform;

        // Dùng khi dựng prefab (Editor).
        public void Setup(HomeRingButton[] buttons, RectTransform tagRt, TextMeshProUGUI title, TextMeshProUGUI sub)
        {
            slots = buttons;
            tag = tagRt;
            tagTitle = title;
            tagSub = sub;
        }

        // vùng trên (thanh trên, dòng tài nguyên) và dưới (hàng nút) mà vòng không được lấn
        public void Insets(float top, float bottom)
        {
            topInset = top;
            bottomInset = bottom;
        }

        // hiện vòng quanh t (vật đang chọn); pop: nảy lại từng nút (chọn vật mới), false: chỉ thay chữ, giá (đếm giờ mỗi giây)
        public void Show(RectTransform t, string title, string sub, IList<RingItem> items, bool pop)
        {
            if (target != t) targetCanvas = t ? t.GetComponentInParent<Canvas>() : null;
            target = t;
            if (!ownCanvas) ownCanvas = GetComponentInParent<Canvas>();
            gameObject.SetActive(true);
            count = Mathf.Min(items?.Count ?? 0, slots.Length);
            for (int i = 0; i < slots.Length; i++)
            {
                var s = slots[i];
                if (!s) continue;
                bool use = i < count;
                s.gameObject.SetActive(use);
                if (!use) continue;
                var it = items[i];
                s.Set(it.icon, it.label, it.cost, it.color, it.on, it.act, it.denied);
                s.Dot(false);
            }
            if (tag)
            {
                bool hasTag = !string.IsNullOrEmpty(title) || !string.IsNullOrEmpty(sub);
                tag.gameObject.SetActive(hasTag);
                if (tagTitle)
                {
                    tagTitle.gameObject.SetActive(!string.IsNullOrEmpty(title));
                    tagTitle.text = title ?? "";
                }
                if (tagSub)
                {
                    tagSub.gameObject.SetActive(!string.IsNullOrEmpty(sub));
                    tagSub.text = sub ?? "";
                }
            }
            if (pop) popT = 0;
            Layout(); // đặt ngay khung này (khỏi nháy ở chỗ cũ)
        }

        public void Hide()
        {
            target = null;
            popT = -1;
            if (gameObject.activeSelf) gameObject.SetActive(false);
        }

        void LateUpdate()
        {
            if (!target || !target.gameObject.activeInHierarchy)
            {
                Hide();
                return;
            }
            Layout();
            if (popT >= 0) Pop(Time.unscaledDeltaTime);
        }

        // khung của vật trong toạ độ của vòng: (giữa x, đỉnh, chân)
        bool Bounds(out float cx, out float top, out float bottom)
        {
            cx = top = bottom = 0;
            if (!target) return false;
            target.GetWorldCorners(corners);
            var camT = targetCanvas && targetCanvas.renderMode != RenderMode.ScreenSpaceOverlay ? targetCanvas.worldCamera : null;
            var camO = ownCanvas && ownCanvas.renderMode != RenderMode.ScreenSpaceOverlay ? ownCanvas.worldCamera : null;
            float minX = float.MaxValue, maxX = float.MinValue, minY = float.MaxValue, maxY = float.MinValue;
            for (int i = 0; i < 4; i++)
            {
                var sp = RectTransformUtility.WorldToScreenPoint(camT, corners[i]);
                if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(Rt, sp, camO, out var lp)) return false;
                minX = Mathf.Min(minX, lp.x);
                maxX = Mathf.Max(maxX, lp.x);
                minY = Mathf.Min(minY, lp.y);
                maxY = Mathf.Max(maxY, lp.y);
            }
            cx = (minX + maxX) / 2;
            // ảnh công trình có khoảng trống trên đầu: hạ đỉnh một chút cho quạt sát vật
            top = maxY - (maxY - minY) * 0.12f;
            bottom = minY;
            return true;
        }

        void Layout()
        {
            if (!Bounds(out float cx, out float top, out float bottom)) return;
            var r = Rt.rect;
            float yMax = r.yMax - topInset, yMin = r.yMin + bottomInset;
            // quạt trên đầu; không đủ chỗ trên (vật sát thanh trên) thì lật xuống dưới chân, nhãn lên trên đầu
            float fanH = 200;
            bool below = top + Lift + fanH > yMax && bottom - Lift - fanH > yMin;
            float half = (count - 1) * Step / 2;
            float x0 = Mathf.Clamp(cx, r.xMin + Margin + half, r.xMax - Margin - half);
            float lowest = float.MaxValue;
            for (int i = 0; i < count; i++)
            {
                var s = slots[i];
                if (!s) continue;
                float dx = i * Step - half;
                float y = below ? bottom - Lift + Curve * dx * dx : top + Lift - Curve * dx * dx;
                y = Mathf.Clamp(y, yMin + 90, yMax - 70);
                lowest = Mathf.Min(lowest, y);
                s.Rt.anchoredPosition = new Vector2(x0 + dx, y) - AnchorOffset(s.Rt);
            }
            if (tag && tag.gameObject.activeSelf)
            {
                // nhãn dưới chân vật, nhưng luôn dưới chữ + giá của nút thấp nhất (vật nhỏ: mốc ô rừng, quái)
                float ty = below ? top + TagGap : Mathf.Min(bottom - TagGap, count > 0 ? lowest - BelowButton : bottom - TagGap);
                float tw = tag.rect.width / 2;
                float tx = Mathf.Clamp(cx, r.xMin + Margin * 0.5f + tw, r.xMax - Margin * 0.5f - tw);
                ty = Mathf.Clamp(ty, yMin + 40, yMax - 40);
                tag.pivot = new Vector2(0.5f, below ? 0 : 1);
                tag.anchoredPosition = new Vector2(tx, ty) - AnchorOffset(tag);
            }
        }

        // vòng neo giữa: anchoredPosition tính từ điểm neo, toạ độ trên tính từ tâm khung
        Vector2 AnchorOffset(RectTransform child)
        {
            var r = Rt.rect;
            var a = (child.anchorMin + child.anchorMax) / 2;
            return new Vector2(r.xMin + a.x * r.width, r.yMin + a.y * r.height);
        }

        // từng nút nảy ra: 0 → 1,15 → 1, lệch nhau PopStagger giây
        void Pop(float dt)
        {
            popT += dt;
            bool done = true;
            for (int i = 0; i < count; i++)
            {
                var s = slots[i];
                if (!s) continue;
                float t = (popT - i * PopStagger) / PopLen;
                float k = t <= 0 ? 0 : t >= 1 ? 1 : t < 0.6f ? Mathf.Lerp(0, 1.15f, t / 0.6f) : Mathf.Lerp(1.15f, 1, (t - 0.6f) / 0.4f);
                s.transform.localScale = Vector3.one * k;
                if (t < 1) done = false;
            }
            if (tag) tag.localScale = Vector3.one * Mathf.Clamp01(popT / 0.18f);
            if (done) popT = -1;
        }

        void OnDisable()
        {
            for (int i = 0; i < slots.Length; i++)
                if (slots[i])
                    slots[i].transform.localScale = Vector3.one;
            if (tag) tag.localScale = Vector3.one;
        }
    }
}
