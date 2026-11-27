// Thẻ ngang to của cửa hàng (prefab Items/TheCuaHang): gói nổi bật / ưu đãi hẹn giờ. Bản 3 (2026-11-27, học thẻ gói Clash of Critters,
// GD_Claude/26 mục 15): nền màu tươi ba lớp (nền chính có sao nổ sau hình, mảng phải cắt chéo caro), dải tên tối dưới đáy, hình hoặc mặt
// tướng bên trái, ô món kem bên phải, nhãn đỏ "Giá trị ×N" góc trên phải, đồng hồ góc trên trái, nút giá xanh lá. ShopPage.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ShopCard : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image bg, panel, rays, art, heroArt, valueBg;
            public TextMeshProUGUI title, desc, timer, done, note, valueText;
            public RectTransform items; // hàng ô món (canh phải)
            public SketchButton buy, extra;
        }

        [SerializeField] Parts p;
        [SerializeField] ShopItemCell cellPrefab;
        [SerializeField] GameObject timerBox; // nền viên thuốc của đồng hồ (chữ là con)
        ShopHue hue;
        double until;
        float next;

        public void Setup(Parts parts, ShopItemCell cell, GameObject timerBg)
        {
            p = parts;
            cellPrefab = cell;
            timerBox = timerBg;
        }

        void ShowTimer(bool on)
        {
            if (timerBox) timerBox.SetActive(on);
            else p.timer.gameObject.SetActive(on);
        }

        public RectTransform Rect => (RectTransform)transform;
        public SketchButton Buy => p.buy;

        void Paint(ShopHue h)
        {
            p.bg.color = h.fill;
            p.panel.color = h.panel;
            p.rays.color = h.rays;
        }

        public ShopCard Set(string title, string desc, ShopHue h)
        {
            hue = h;
            Paint(h);
            p.title.text = title;
            p.desc.text = desc ?? "";
            p.desc.gameObject.SetActive(!string.IsNullOrEmpty(desc));
            p.art.gameObject.SetActive(false);
            p.heroArt.gameObject.SetActive(false);
            ShowTimer(false);
            p.done.gameObject.SetActive(false);
            p.note.gameObject.SetActive(false);
            p.valueBg.gameObject.SetActive(false);
            p.buy.gameObject.SetActive(false);
            p.extra.gameObject.SetActive(false);
            for (int i = p.items.childCount - 1; i >= 0; i--) Destroy(p.items.GetChild(i).gameObject);
            p.items.gameObject.SetActive(false);
            until = 0;
            Height(Tall);
            return this;
        }

        public const float Tall = 400, Short = 250;

        void Height(float h)
        {
            if (TryGetComponent<LayoutElement>(out var le)) le.preferredHeight = h;
        }

        // thẻ gọn (không có hàng món): Khôi phục giao dịch, Tỉ lệ, vé
        public ShopCard Compact()
        {
            Height(Short);
            return this;
        }

        public ShopCard Art(Sprite s)
        {
            p.art.gameObject.SetActive(s);
            Theme.SetSprite(p.art, s);
            p.art.preserveAspect = true;
            return this;
        }

        // mặt tướng (gói tướng tuần, gói đồng hành): ảnh thẻ tướng thay hình to; chưa có mặt tướng (gói tải sau) thì hình gói fallback
        public ShopCard Hero(HeroDef h, Sprite fallback = null)
        {
            var s = h != null ? HeroArt.Face(h) : null;
            p.heroArt.gameObject.SetActive(s);
            if (s) Theme.SetSprite(p.heroArt, s);
            else if (fallback) Art(fallback);
            p.heroArt.preserveAspect = true;
            return this;
        }

        // ô món canh phải; 5 món trở lên thì thu nhỏ cho khỏi đè hình gói
        public ShopCard Items(IEnumerable<ShopItem> items)
        {
            foreach (var it in items) Ui.Spawn(cellPrefab, p.items).Set(it);
            int n = p.items.childCount;
            p.items.gameObject.SetActive(n > 0);
            p.items.localScale = Vector3.one * (n >= 5 ? ItemScale5 : ItemScale);
            return this;
        }

        public const float ItemScale = 0.84f, ItemScale5 = 0.74f;

        // nhãn giá trị: chỉ hiện khi hời rõ (×1,5 trở lên)
        public ShopCard Value(double mult)
        {
            bool on = mult >= 1.5;
            p.valueBg.gameObject.SetActive(on);
            if (on) p.valueText.text = ShopHue.ValueText(mult);
            return this;
        }

        public ShopCard Timer(double untilMs)
        {
            until = untilMs;
            ShowTimer(untilMs > 0);
            Tick();
            return this;
        }

        public ShopCard Note(string text, Color? color = null)
        {
            p.note.gameObject.SetActive(!string.IsNullOrEmpty(text));
            p.note.text = text ?? "";
            p.note.color = color ?? Color.white;
            return this;
        }

        public ShopCard Button(string label, BtnColor role, Action click, bool on = true)
        {
            p.buy.gameObject.SetActive(true);
            p.buy.name = "nut_" + label;
            ShopHue.Paint(p.buy, role);
            p.buy.SetText(label);
            p.buy.Interactable = on;
            p.buy.SetOnClick(click);
            return this;
        }

        public ShopCard Extra(string label, BtnColor role, Action click, bool on = true)
        {
            p.extra.gameObject.SetActive(true);
            p.extra.name = "nut2_" + label;
            ShopHue.Paint(p.extra, role);
            p.extra.SetText(label);
            p.extra.Interactable = on;
            p.extra.SetOnClick(click);
            return this;
        }

        public ShopCard AdExtra(string label, string placement, Action click)
        {
            p.extra.gameObject.SetActive(Ads.Ready);
            p.extra.name = "nut_qc_" + placement;
            p.extra.SetRole(BtnColor.Blue);
            Ads.Bind(p.extra, label, placement);
            p.extra.SetOnClick(click);
            return this;
        }

        // đã mua / đã nhận: chữ trong dải tên, tắt nút, nền ngả xám
        public ShopCard Done(string text)
        {
            p.done.gameObject.SetActive(true);
            p.done.text = text;
            p.buy.gameObject.SetActive(false);
            p.extra.gameObject.SetActive(false);
            Paint(hue.Dim());
            return this;
        }

        void Tick()
        {
            if (until <= 0) return;
            double left = until - SaveService.Now();
            p.timer.text = left > 0 ? ShopUi.Clock(left) : Loc.T("Hết giờ");
            if (left <= 0) p.buy.Interactable = false;
        }

        void Update()
        {
            if (until <= 0 || Time.unscaledTime < next) return;
            next = Time.unscaledTime + 0.5f;
            Tick();
        }
    }
}
