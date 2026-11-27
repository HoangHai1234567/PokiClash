// Ô cột của popup ưu đãi kiểu mới (OfferPopup, prefab Assets/04 Prefabs/Items/PopCot), tông cửa hàng bản 3 (ShopHue, Assets/03 Art/Shop/v3):
// ô đứng nền màu tươi (o_nen tô màu chính, dải tối đáy) + sao nổ (o_tia), tên trắng viền mực trên đầu ("NGÀY 1" của gói nhận theo ngày như ô
// ngày gói 3 ngày của Clash of Critters, hoặc tên bậc của nhóm chọn một như ba cột xanh / tím / cam của họ), hình gói nhỏ, ruy băng đỏ
// "Giá trị ×N", lưới ô món (Items/OMonCuaHang, cỡ đặt lúc chạy), nhãn góc trái ("Nhận ngay"), nút giá xanh lá trong dải tối đáy.
// Popup chọn một gói (bản 4, người dùng 2026-11-27 gửi popup nạp đầu Critters: "độ cao tăng dần, giá trị phải để thẳng trên đầu luôn làm nổi
// bật, list từng thứ to và rõ ràng"): không tên bậc, không hình gói; huy hiệu sao nổ hồng (huy_hieu.png) đè giữa mép trên ghi "×N" to +
// "GIÁ TRỊ", thở nhẹ; món xếp một cột ô to. Nền ô: màu trơn + hoa văn lát mờ (hoa_van.png, mảnh hình cột trái cửa hàng) thay sao nổ.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class OfferPopColumn : MonoBehaviour
    {
        // cao dải tên trên đầu, dải tối đáy (chỗ nút giá)
        public const float HeadH = 74, FootH = 104;

        [Serializable]
        public struct Parts
        {
            public Image bg, rays, art, tag, valueBg;
            public TextMeshProUGUI head, tagText, valueText, done;
            public RectTransform items;
            public GridLayoutGroup grid;
            public SketchButton buy;
            public RectTransform badge; // huy hiệu giá trị trên đỉnh (popup chọn một gói)
            public TextMeshProUGUI badgeText, badgeSub;
            public Image pattern; // hoa văn lát mờ thay sao nổ (popup chọn một gói / Hết bi)
            public Sprite plainFoot, plainBare; // nền trơn (không caro thoi): có dải đáy cho nút giá / không dải (ô ngày)
        }

        [SerializeField] Parts p;

        public RectTransform Rect => (RectTransform)transform;
        public SketchButton Buy => p.buy;
        public RectTransform BadgeRect => p.badge && p.badge.gameObject.activeSelf ? p.badge : null;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        public OfferPopColumn Set(string head, ShopHue hue, Vector2 size)
        {
            Rect.sizeDelta = size;
            var le = GetComponent<LayoutElement>();
            if (le)
            {
                le.preferredWidth = size.x;
                le.preferredHeight = size.y;
            }
            p.head.text = head;
            p.head.gameObject.SetActive(!string.IsNullOrEmpty(head));
            if (p.badge) p.badge.gameObject.SetActive(false);
            p.rays.gameObject.SetActive(true);
            if (p.pattern) p.pattern.gameObject.SetActive(false);
            p.bg.color = hue.fill;
            p.rays.color = hue.rays;
            p.art.gameObject.SetActive(false);
            p.tag.gameObject.SetActive(false);
            p.valueBg.gameObject.SetActive(false);
            p.done.gameObject.SetActive(false);
            p.buy.gameObject.SetActive(false);
            for (int i = p.items.childCount - 1; i >= 0; i--) Destroy(p.items.GetChild(i).gameObject);
            return this;
        }

        // ô món: lưới cols cột, ô cỡ cell; vùng món từ top (dưới dải tên / hình) tới bottom (trên dải đáy); dồn giữa theo chiều dọc khi center
        public OfferPopColumn Fill(ShopItemCell prefab, List<ShopItem> items, int cols, Vector2 cell, float top, float bottom, bool center)
        {
            p.items.offsetMax = new Vector2(p.items.offsetMax.x, -top);
            p.items.offsetMin = new Vector2(p.items.offsetMin.x, bottom);
            p.grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            p.grid.constraintCount = Mathf.Max(1, cols);
            p.grid.cellSize = cell;
            p.grid.childAlignment = center ? TextAnchor.MiddleCenter : TextAnchor.UpperCenter;
            foreach (var it in items) Ui.Spawn(prefab, p.items).Set(it);
            return this;
        }

        public OfferPopColumn Art(Sprite s, float height)
        {
            p.art.gameObject.SetActive(s);
            if (!s) return this;
            Theme.SetSprite(p.art, s);
            p.art.preserveAspect = true;
            var r = p.art.rectTransform;
            r.sizeDelta = new Vector2(r.sizeDelta.x, height);
            return this;
        }

        public OfferPopColumn Tag(string text, Color c)
        {
            p.tag.gameObject.SetActive(true);
            p.tagText.text = text;
            p.tag.color = c;
            return this;
        }

        public OfferPopColumn Value(double mult)
        {
            bool on = mult >= 1.5;
            p.valueBg.gameObject.SetActive(on);
            if (on) p.valueText.text = "×" + Math.Round(mult);
            return this;
        }

        // nền màu trơn + hoa văn vẽ tay mờ (người dùng: sao nổ "như bị stretch ra"; hoa văn giống cột trái cửa hàng)
        public OfferPopColumn Plain(bool foot = true)
        {
            p.rays.gameObject.SetActive(false);
            var s = foot ? p.plainFoot : p.plainBare;
            if (s) Theme.SetSprite(p.bg, s);
            if (p.pattern)
            {
                p.pattern.gameObject.SetActive(true);
                p.pattern.rectTransform.offsetMin = new Vector2(14, foot ? FootH + 2 : 14);
            }
            return this;
        }

        // hình gói đặt theo chỗ: tâm ngang, mép trên cách đỉnh ô top, khung size (giữ tỉ lệ)
        public OfferPopColumn ArtAt(Sprite s, float top, Vector2 size)
        {
            Art(s, size.y);
            if (!s) return this;
            var r = p.art.rectTransform;
            r.anchoredPosition = new Vector2(0, -top);
            r.sizeDelta = size;
            return this;
        }

        // huy hiệu giá trị trên đỉnh ô (popup chọn một gói): "×N" to, "GIÁ TRỊ" nhỏ; nghiêng chút cho sống
        public OfferPopColumn Badge(double mult, float tilt)
        {
            bool on = p.badge && mult >= 1.5;
            if (p.badge) p.badge.gameObject.SetActive(on);
            if (!on) return this;
            p.badgeText.text = "×" + Math.Round(mult);
            p.badgeSub.text = Loc.T("GIÁ TRỊ");
            p.badge.localEulerAngles = new Vector3(0, 0, tilt);
            return this;
        }

        // nút giá xanh lá (bản 3)
        public OfferPopColumn Button(string text, Action click)
        {
            p.buy.gameObject.SetActive(true);
            ShopHue.Paint(p.buy, BtnColor.Green);
            p.buy.SetText(text);
            p.buy.SetOnClick(click);
            return this;
        }

        public OfferPopColumn Done(string text)
        {
            p.buy.gameObject.SetActive(false);
            p.done.gameObject.SetActive(true);
            p.done.text = text;
            return this;
        }
    }
}
