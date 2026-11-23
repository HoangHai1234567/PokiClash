// Thẻ ngang to của cửa hàng (prefab Items/TheCuaHang): gói nổi bật / ưu đãi hẹn giờ: hình hoặc mặt tướng bên trái, tên, mô tả, hàng
// ô thưởng thu nhỏ, đồng hồ, sticker giá trị, nút giá và nút phụ. ShopPage.
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
            public Image bg, art, heroArt;
            public TextMeshProUGUI title, desc, timer, done, note;
            public RectTransform items; // hàng ô thưởng (thu nhỏ)
            public UiStamp value;
            public SketchButton buy, extra;
        }

        [SerializeField] Parts p;
        [SerializeField] RewardTile tilePrefab;
        [SerializeField] GameObject timerBox; // nền viên thuốc của đồng hồ (chữ là con)
        double until;
        float next;

        public void Setup(Parts parts, RewardTile tile, GameObject timerBg)
        {
            p = parts;
            tilePrefab = tile;
            timerBox = timerBg;
        }

        void ShowTimer(bool on)
        {
            if (timerBox) timerBox.SetActive(on);
            else p.timer.gameObject.SetActive(on);
        }

        public RectTransform Rect => (RectTransform)transform;
        public SketchButton Buy => p.buy;

        public ShopCard Set(string title, string desc, Color bg)
        {
            p.title.text = title;
            p.desc.text = desc ?? "";
            p.desc.gameObject.SetActive(!string.IsNullOrEmpty(desc));
            p.bg.color = bg;
            p.art.gameObject.SetActive(false);
            p.heroArt.gameObject.SetActive(false);
            ShowTimer(false);
            p.done.gameObject.SetActive(false);
            p.note.gameObject.SetActive(false);
            p.value.gameObject.SetActive(false);
            p.buy.gameObject.SetActive(false);
            p.extra.gameObject.SetActive(false);
            for (int i = p.items.childCount - 1; i >= 0; i--) Destroy(p.items.GetChild(i).gameObject);
            until = 0;
            Height(Tall);
            return this;
        }

        public const float Tall = 380, Short = 230;

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

        // mặt tướng (gói tướng tuần, gói đồng hành): ảnh thẻ tướng thay hình to
        public ShopCard Hero(HeroDef h)
        {
            var s = h != null ? HeroArt.Face(h) : null;
            p.heroArt.gameObject.SetActive(s);
            if (s) Theme.SetSprite(p.heroArt, s);
            p.heroArt.preserveAspect = true;
            return this;
        }

        public ShopCard Items(IEnumerable<ShopItem> items)
        {
            foreach (var it in items) ShopUi.Tile(Ui.Spawn(tilePrefab, p.items), it);
            return this;
        }

        public ShopCard Rewards(List<Reward> rewards)
        {
            ChestDialog.BuildTiles(rewards, tilePrefab, p.items);
            return this;
        }

        public ShopCard Value(double mult)
        {
            bool on = mult >= 1.5;
            p.value.gameObject.SetActive(on);
            if (on) p.value.Set(Loc.F("giá trị ×{0}", Math.Round(mult)), Theme.Red);
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
            p.note.color = color ?? Theme.Ink2;
            return this;
        }

        public ShopCard Button(string label, BtnColor role, Action click, bool on = true)
        {
            p.buy.gameObject.SetActive(true);
            p.buy.name = "nut_" + label;
            p.buy.SetRole(role);
            p.buy.SetText(label);
            p.buy.Interactable = on;
            p.buy.SetOnClick(click);
            return this;
        }

        public ShopCard Extra(string label, BtnColor role, Action click, bool on = true)
        {
            p.extra.gameObject.SetActive(true);
            p.extra.name = "nut2_" + label;
            p.extra.SetRole(role);
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

        public ShopCard Done(string text)
        {
            p.done.gameObject.SetActive(true);
            p.done.text = text;
            p.buy.gameObject.SetActive(false);
            p.extra.gameObject.SetActive(false);
            p.bg.color = Color.Lerp(p.bg.color, Theme.Paper3, 0.55f);
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
