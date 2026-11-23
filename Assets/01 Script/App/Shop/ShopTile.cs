// Ô đứng trong lưới cửa hàng (prefab Items/OCuaHang): trứng, gói bi, quà miễn phí, đặc quyền: nền màu, nhãn góc trái (Lần đầu ×2,
// Bán chạy), hình to (một hình hoặc chồng 3 quả), số "×10", tên, dòng phụ, sticker "×N", nút giá, dấu "Đã mua", chấm đỏ. ShopPage.
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
            public Image bg, art, ribbon, dot;
            public Image[] stack; // các quả xếp chồng (gói nhiều trứng), bật theo số
            public TextMeshProUGUI title, sub, count, ribbonText, done;
            public UiStamp value;
            public SketchButton buy;
        }

        [SerializeField] Parts p;
        public void Setup(Parts parts) => p = parts;
        public RectTransform Rect => (RectTransform)transform;
        public SketchButton Buy => p.buy;

        public ShopTile Set(string title, string sub, Color bg)
        {
            p.title.text = title;
            p.sub.text = sub ?? "";
            p.sub.gameObject.SetActive(!string.IsNullOrEmpty(sub));
            p.bg.color = bg;
            p.art.gameObject.SetActive(false);
            foreach (var s in p.stack) s.gameObject.SetActive(false);
            p.count.gameObject.SetActive(false);
            p.ribbon.gameObject.SetActive(false);
            p.value.gameObject.SetActive(false);
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

        // sticker giá trị: chỉ khi hời rõ (×1,5 trở lên)
        public ShopTile Value(double mult)
        {
            bool on = mult >= 1.5;
            p.value.gameObject.SetActive(on);
            if (on) p.value.Set("×" + Math.Round(mult), Theme.Red);
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
            p.buy.SetRole(role);
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
            p.bg.color = Color.Lerp(p.bg.color, Theme.Paper3, 0.55f);
            return this;
        }
    }
}
