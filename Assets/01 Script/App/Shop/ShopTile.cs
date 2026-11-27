// Ô đứng trong lưới cửa hàng (prefab Items/OCuaHang): trứng, gói bi, quà miễn phí, đặc quyền. Bản 3 (2026-11-27, học ô gói Clash of
// Critters, GD_Claude/26 mục 15): nền màu tươi có caro thoi và sao nổ sau hình, tên trắng viền mực trên đầu, hình to (một hình hoặc chồng 3
// quả), số "×10", dòng phụ, nhãn góc trái (Lần đầu ×2, Bán chạy), nhãn đỏ "×N" góc phải, dải tối dưới đáy chứa nút giá xanh lá / dấu
// "Đã mua", chấm đỏ. ShopPage.
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
    public sealed class ShopTile : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image bg, rays, art, ribbon, dot, valueBg;
            public Image[] stack; // các quả xếp chồng (gói nhiều trứng), bật theo số
            public TextMeshProUGUI title, sub, count, ribbonText, done, valueText;
            public SketchButton buy;
        }

        [SerializeField] Parts p;
        ShopHue hue;
        public void Setup(Parts parts) => p = parts;
        public RectTransform Rect => (RectTransform)transform;
        public SketchButton Buy => p.buy;

        void Paint(ShopHue h)
        {
            p.bg.color = h.fill;
            p.rays.color = h.rays;
        }

        public ShopTile Set(string title, string sub, ShopHue h)
        {
            hue = h;
            Paint(h);
            p.title.text = title;
            p.sub.text = sub ?? "";
            p.sub.gameObject.SetActive(!string.IsNullOrEmpty(sub));
            p.art.gameObject.SetActive(false);
            foreach (var s in p.stack) s.gameObject.SetActive(false);
            p.count.gameObject.SetActive(false);
            p.ribbon.gameObject.SetActive(false);
            p.valueBg.gameObject.SetActive(false);
            p.done.gameObject.SetActive(false);
            p.dot.gameObject.SetActive(false);
            p.buy.gameObject.SetActive(false);
            return this;
        }

        // scale: thu hình trong khung (icon vector to quá thì 0,6)
        public ShopTile Art(Sprite s, string count = null, float scale = 1)
        {
            p.art.rectTransform.localScale = Vector3.one * scale;
            p.art.gameObject.SetActive(s);
            Theme.SetSprite(p.art, s);
            p.art.preserveAspect = true;
            p.count.gameObject.SetActive(!string.IsNullOrEmpty(count));
            p.count.text = count ?? "";
            return this;
        }

        // n quả cùng hình xếp chồng (gói ×10: ba quả), số ghi góc
        public ShopTile Stack(Sprite s, int shown, string count)
        {
            p.art.gameObject.SetActive(false);
            for (int i = 0; i < p.stack.Length; i++)
            {
                p.stack[i].gameObject.SetActive(i < shown);
                Theme.SetSprite(p.stack[i], s);
                p.stack[i].preserveAspect = true;
            }
            p.count.gameObject.SetActive(!string.IsNullOrEmpty(count));
            p.count.text = count ?? "";
            return this;
        }

        public ShopTile Ribbon(string text, Color c)
        {
            p.ribbon.gameObject.SetActive(!string.IsNullOrEmpty(text));
            p.ribbon.color = c;
            p.ribbonText.text = text ?? "";
            return this;
        }

        // nhãn giá trị: chỉ khi hời rõ (×1,5 trở lên)
        public ShopTile Value(double mult)
        {
            bool on = mult >= 1.5;
            p.valueBg.gameObject.SetActive(on);
            if (on) p.valueText.text = "×" + Math.Round(mult);
            return this;
        }

        public ShopTile Dot(bool on)
        {
            p.dot.gameObject.SetActive(on);
            return this;
        }

        public ShopTile Button(string label, BtnColor role, Action click, bool on = true)
        {
            p.buy.gameObject.SetActive(true);
            p.buy.name = "nut_" + label;
            ShopHue.Paint(p.buy, role);
            p.buy.SetText(label);
            p.buy.Interactable = on;
            p.buy.SetOnClick(click);
            return this;
        }

        public ShopTile AdButton(string label, string placement, Action click)
        {
            p.buy.gameObject.SetActive(Ads.Ready);
            p.buy.name = "nut_qc_" + placement;
            p.buy.SetRole(BtnColor.Blue);
            Ads.Bind(p.buy, label, placement);
            p.buy.SetOnClick(click);
            return this;
        }

        public ShopTile Done(string text)
        {
            p.done.gameObject.SetActive(true);
            p.done.text = text;
            p.buy.gameObject.SetActive(false);
            Paint(hue.Dim());
            return this;
        }
    }
}
