// Một ô gói trong tờ cửa hàng / popup ưu đãi (prefab Assets/04 Prefabs/Items/OGoi, menu "PokiClash/Prefab/Khác/Hộp thoại và màn∕Cửa hàng: dựng hết"): tờ giấy,
// tên, mô tả, hàng món (ô thưởng Items/OThuong thu nhỏ, xuống hàng khi nhiều), nhãn "giá trị ×N" (sticker đỏ), đồng hồ bút chì đếm ngược,
// nút chính (giá / Nhận / Mở) và nút phụ (×2 quảng cáo, Mở 10), dòng ghi chú, dấu "Đã mua" che ô.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class PackCell : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image card;
            public TextMeshProUGUI title, desc, timer, note, done;
            public RectTransform items; // lưới ô thưởng (GridLayoutGroup, thu nhỏ bằng localScale)
            public UiStamp value;
            public SketchButton buy, extra;
            public LayoutElement layout;
        }

        [SerializeField] Parts p;
        [SerializeField] RewardTile tilePrefab;

        public const float ItemScale = 0.66f;
        const int PerRow = 5;
        double until;
        float nextTick;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, RewardTile tile)
        {
            p = parts;
            tilePrefab = tile;
        }

        public RectTransform Rect => (RectTransform)transform;
        public SketchButton BuyButton => p.buy;
        public SketchButton ExtraButton => p.extra;

        // đặt lại về ô trống: tên, mô tả
        public PackCell Set(string title, string desc)
        {
            p.title.text = title;
            p.desc.text = desc ?? "";
            p.desc.gameObject.SetActive(!string.IsNullOrEmpty(desc));
            p.card.color = Theme.Paper;
            p.value.gameObject.SetActive(false);
            p.timer.gameObject.SetActive(false);
            p.note.gameObject.SetActive(false);
            p.done.gameObject.SetActive(false);
            p.buy.gameObject.SetActive(false);
            p.extra.gameObject.SetActive(false);
            for (int i = p.items.childCount - 1; i >= 0; i--) Destroy(p.items.GetChild(i).gameObject);
            p.items.gameObject.SetActive(false);
            until = 0;
            Fit();
            return this;
        }

        public PackCell Tint(Color c)
        {
            p.card.color = c;
            return this;
        }

        public PackCell Items(IEnumerable<ShopItem> items)
        {
            foreach (var it in items) ShopUi.Tile(Ui.Spawn(tilePrefab, p.items), it);
            Fit();
            return this;
        }

        public PackCell Rewards(List<Reward> rewards)
        {
            ChestDialog.BuildTiles(rewards, tilePrefab, p.items);
            Fit();
            return this;
        }

        public RewardTile HeroTile(HeroDef h, string count)
        {
            var t = Ui.Spawn(tilePrefab, p.items).Hero(h, count);
            Fit();
            return t;
        }

        // nhãn giá trị: chỉ hiện khi hời rõ (×1,5 trở lên)
        public PackCell Value(double mult)
        {
            bool on = mult >= 1.5;
            p.value.gameObject.SetActive(on);
            if (on) p.value.Set(Loc.F("giá trị ×{0}", Math.Round(mult)), Theme.Red);
            return this;
        }

        public PackCell Timer(double untilMs)
        {
            until = untilMs;
            p.timer.gameObject.SetActive(untilMs > 0);
            Tick();
            return this;
        }

        public PackCell Note(string text, Color? color = null)
        {
            p.note.gameObject.SetActive(!string.IsNullOrEmpty(text));
            p.note.text = text ?? "";
            p.note.color = color ?? Theme.Ink2;
            Fit();
            return this;
        }

        public PackCell Button(string label, BtnColor role, Action click, bool on = true)
        {
            p.buy.gameObject.SetActive(true);
            p.buy.name = "nut_" + label;
            p.buy.SetRole(role);
            p.buy.SetText(label);
            p.buy.Interactable = on;
            p.buy.SetOnClick(click);
            return this;
        }

        // nút quảng cáo: ghi lượt còn, hết lượt thì xám
        public PackCell AdButton(string label, string placement, Action click, bool extra = false)
        {
            var b = extra ? p.extra : p.buy;
            b.gameObject.SetActive(true);
            b.name = "nut_qc_" + placement;
            b.SetRole(BtnColor.Blue);
            Ads.Bind(b, label, placement);
            b.SetOnClick(click);
            if (!Ads.Ready) b.gameObject.SetActive(false);
            Fit();
            return this;
        }

        public PackCell Extra(string label, BtnColor role, Action click, bool on = true)
        {
            p.extra.gameObject.SetActive(true);
            p.extra.name = "nut2_" + label;
            p.extra.SetRole(role);
            p.extra.SetText(label);
            p.extra.Interactable = on;
            p.extra.SetOnClick(click);
            Fit();
            return this;
        }

        // đã mua / đã nhận: dấu đè, tắt nút
        public PackCell Done(string text)
        {
            p.done.gameObject.SetActive(true);
            p.done.text = text;
            p.buy.gameObject.SetActive(false);
            p.extra.gameObject.SetActive(false);
            p.card.color = Theme.Hex("#e6f7d9");
            Fit();
            return this;
        }

        // chiều cao ô theo số hàng món
        void Fit()
        {
            int n = p.items.childCount;
            p.items.gameObject.SetActive(n > 0);
            int rows = n == 0 ? 0 : (n + PerRow - 1) / PerRow;
            float itemsH = rows * (RewardTile.H + 24) * ItemScale;
            var le = p.items.GetComponent<LayoutElement>();
            if (le) le.preferredHeight = itemsH;
            float h = 120 + itemsH + (p.desc.gameObject.activeSelf ? 60 : 0) + (p.note.gameObject.activeSelf ? 40 : 0);
            if (p.extra.gameObject.activeSelf) h = Mathf.Max(h, 290);
            if (p.layout) p.layout.preferredHeight = Mathf.Max(h, 200);
        }

        void Tick()
        {
            if (until <= 0) return;
            double left = until - SaveService.Now();
            p.timer.text = left > 0 ? Loc.F("Còn {0}", ShopUi.Clock(left)) : Loc.T("Hết giờ");
            p.timer.color = left < 3600000 ? Theme.RedD : Theme.Ink2;
            if (left <= 0) p.buy.Interactable = false;
        }

        void Update()
        {
            if (until <= 0 || Time.unscaledTime < nextTick) return;
            nextTick = Time.unscaledTime + 0.5f;
            Tick();
        }
    }

    // vẽ món cửa hàng thành ô thưởng; đồng hồ; tên món
    public static class ShopUi
    {
        public static readonly Color GoldTint = Theme.Hex("#f6c343");

        public static string Clock(double ms)
        {
            var t = TimeSpan.FromMilliseconds(Math.Max(0, ms));
            if (t.TotalDays >= 1) return Loc.F("{0} ngày {1} giờ", (int)t.TotalDays, t.Hours);
            return $"{(int)t.TotalHours:00}:{t.Minutes:00}:{t.Seconds:00}";
        }

        // trứng capsule bậc tier (Assets/03 Art/Shop/trung_<bậc>.png, ArtGen/Shop/cat_trung.py)
        public static Sprite Egg(int tier) => App.Art.Get("trung_" + Mathf.Clamp(tier, 0, Eggs.Tiers - 1));
        public static Color TierColor(int tier) => Theme.Hex(Elements.RarityColor((Rarity)Mathf.Clamp(tier, 0, Eggs.Tiers - 1)));
        public static string EggName(int tier) => App.Data.Cfg.shop.Egg(tier)?.Name ?? Loc.T("Trứng");
        // nền ô trứng: màu bậc pha giấy
        public static Color EggBg(int tier) => Color.Lerp(TierColor(tier), Theme.Paper, 0.72f);

        public static string ItemName(ShopItem it)
        {
            it = Shop.Norm(it);
            switch (it.k)
            {
                case "balls": return Loc.T("Bi");
                case Shop.Egg: return EggName(it.r);
                case Shop.Ticket: return it.r == 2 ? Loc.T("Vé tướng Hiếm") : it.r == 3 ? Loc.T("Vé tướng Sử thi") : Loc.T("Vé chọn tướng");
                case Shop.TicketWeek: return Loc.T("Vé tướng tuần");
                case "evo": return Loc.T("Đá tiến hóa");
                case "stones": return Loc.T("Đá tiềm năng");
                case "crystal": return Loc.T("Đá tinh");
                case "copies": return Loc.T("Bản sao thẻ");
                case "week_card": return Loc.T("Thẻ Tuần");
                case "month_card": return Loc.T("Thẻ Phiêu Lưu");
                case "no_ads": return Loc.T("Bỏ quảng cáo");
                default: return it.k;
            }
        }

        public static void Tile(RewardTile t, ShopItem it)
        {
            var art = App.Art;
            it = Shop.Norm(it);
            string n = "×" + NumFmt.Short(it.n);
            switch (it.k)
            {
                case "balls": t.Item(art.Icon("ball"), n, ItemName(it)); break;
                // trứng: ô màu bậc, nhãn "nở mảnh" cho người chơi biết trứng ra mảnh tướng
                case Shop.Egg: t.Item(Egg(it.r), n, ItemName(it), (Rarity)Mathf.Clamp(it.r, 0, Eggs.Tiers - 1)).Tag(Loc.T("nở mảnh"), TierColor(it.r)); break;
                case Shop.Ticket: t.Item(art.Icon("team"), n, ItemName(it), it.r >= 3 ? Rarity.Epic : Rarity.Rare); break;
                case Shop.TicketWeek: t.Item(art.Icon("star"), n, ItemName(it), Rarity.Epic); break;
                case "evo": t.EvoStones(it.n); break;
                case "stones": t.Item(art.Icon("rock"), n, ItemName(it), Rarity.Epic); break;
                case "crystal": t.Item(art.Icon("shard"), n, ItemName(it), Rarity.Legend); break;
                case "shards":
                    var h = App.Data.Hero(it.h);
                    if (h != null) t.Hero(h, n);
                    else t.Item(art.Icon("shard"), n, Loc.T("Mảnh tướng"));
                    break;
                case "copies":
                    var oh = App.Data.Hero(it.h);
                    t.Item(art.Icon("cards"), n, oh != null ? Loc.F("Thẻ {0}", oh.name) : ItemName(it), Rarity.Rare);
                    break;
                case "week_card": t.Item(art.Icon("clock"), "7", ItemName(it), Rarity.Rare); break;
                case "month_card": t.Item(art.Icon("clock"), "30", ItemName(it), Rarity.Epic); break;
                case "no_ads": t.Item(art.Icon("tv"), "", ItemName(it), Rarity.Epic); break;
                default: t.Item(art.Icon("star"), n, ItemName(it)); break;
            }
        }
    }
}
