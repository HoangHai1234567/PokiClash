// Một ô gói trong tờ popup / trang con của cửa hàng (prefab Assets/04 Prefabs/Items/OGoi; menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng
// hết" hoặc "Cửa hàng: tờ popup + cụm sảnh"). Bản 3 (2026-11-27, cùng tông màn cửa hàng, GD_Claude/26 mục 17): nền màu tươi ba lớp (ShopHue),
// dải tên tối dưới đáy; phía trên: mô tả trắng, hàng ô món kem (Items/OMonCuaHang; quà dạng Reward và ô tướng của trang vé dùng ô thưởng chung
// Items/OThuong), ghi chú; góc phải nhãn đỏ "Giá trị ×N", đồng hồ viên tối; nút giá xanh lá và nút phụ; chữ "Đã mua".
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
            public Image card, panel, rays, valueBg;
            public TextMeshProUGUI title, desc, timer, note, done, valueText;
            public GameObject timerBox;
            public RectTransform items; // lưới món (GridLayoutGroup, thu nhỏ bằng localScale)
            public SketchButton buy, extra;
            public LayoutElement layout;
        }

        [SerializeField] Parts p;
        [SerializeField] ShopItemCell cellPrefab;
        [SerializeField] RewardTile tilePrefab;

        public const float ItemScale = 0.8f, Strip = 100;
        const int PerRow = 5;
        ShopHue hue = ShopHue.Sunset;
        double until;
        float nextTick;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, ShopItemCell cell, RewardTile tile)
        {
            p = parts;
            cellPrefab = cell;
            tilePrefab = tile;
        }

        public RectTransform Rect => (RectTransform)transform;
        public SketchButton BuyButton => p.buy;
        public SketchButton ExtraButton => p.extra;

        // đặt lại về ô trống: tên, mô tả, màu
        public PackCell Set(string title, string desc) => Set(title, desc, ShopHue.Sunset);

        public PackCell Set(string title, string desc, ShopHue h)
        {
            p.title.text = title;
            p.desc.text = desc ?? "";
            p.desc.gameObject.SetActive(!string.IsNullOrEmpty(desc));
            Hue(h);
            p.valueBg.gameObject.SetActive(false);
            p.timerBox.SetActive(false);
            p.note.gameObject.SetActive(false);
            p.done.gameObject.SetActive(false);
            p.buy.gameObject.SetActive(false);
            p.extra.gameObject.SetActive(false);
            for (int i = p.items.childCount - 1; i >= 0; i--) Destroy(p.items.GetChild(i).gameObject);
            until = 0;
            Fit();
            return this;
        }

        public PackCell Hue(ShopHue h)
        {
            hue = h;
            Paint(h);
            return this;
        }

        // sao nổ mờ (ô gói không có hình bên trái, sao nổ đậm làm chìm chữ trắng)
        void Paint(ShopHue h)
        {
            p.card.color = h.fill;
            p.panel.color = h.panel;
            p.rays.color = new Color(h.rays.r, h.rays.g, h.rays.b, 0.35f);
        }

        GridLayoutGroup Grid => p.items.GetComponent<GridLayoutGroup>();

        public PackCell Items(IEnumerable<ShopItem> items)
        {
            Grid.cellSize = new Vector2(ShopItemCell.Size, ShopItemCell.Size);
            foreach (var it in items) Ui.Spawn(cellPrefab, p.items).Set(it);
            Fit();
            return this;
        }

        // quà dạng Reward (Quà trở lại): ô thưởng chung, tên trắng
        public PackCell Rewards(List<Reward> rewards)
        {
            Grid.cellSize = new Vector2(RewardTile.W, RewardTile.H);
            ChestDialog.BuildTiles(rewards, tilePrefab, p.items);
            foreach (var t in p.items.GetComponentsInChildren<RewardTile>(true)) t.Caption(Color.white);
            Fit();
            return this;
        }

        // ô tướng (trang vé): ô thưởng chung, tên tướng đã ở dòng tên ô gói
        public RewardTile HeroTile(HeroDef h, string count)
        {
            Grid.cellSize = new Vector2(RewardTile.W, RewardTile.H);
            var t = Ui.Spawn(tilePrefab, p.items).Hero(h, count);
            t.Caption(Color.white, false);
            Fit();
            return t;
        }

        // nhãn giá trị: chỉ hiện khi hời rõ (×1,5 trở lên)
        public PackCell Value(double mult)
        {
            bool on = mult >= 1.5;
            p.valueBg.gameObject.SetActive(on);
            if (on) p.valueText.text = ShopHue.ValueText(mult);
            return this;
        }

        public PackCell Timer(double untilMs)
        {
            until = untilMs;
            p.timerBox.SetActive(untilMs > 0);
            Tick();
            return this;
        }

        // màu ghi chú vốn chọn cho nền giấy (mực đỏ, xanh, xám): làm sáng cho đọc được trên nền màu tươi
        public PackCell Note(string text, Color? color = null)
        {
            p.note.gameObject.SetActive(!string.IsNullOrEmpty(text));
            p.note.text = text ?? "";
            var c = color ?? Color.white;
            p.note.color = c.grayscale < 0.6f ? Color.Lerp(c, Color.white, 0.6f) : c;
            Fit();
            return this;
        }

        public PackCell Button(string label, BtnColor role, Action click, bool on = true)
        {
            p.buy.gameObject.SetActive(true);
            p.buy.name = "nut_" + label;
            ShopHue.Paint(p.buy, role);
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
            ShopHue.Paint(p.extra, role);
            p.extra.SetText(label);
            p.extra.Interactable = on;
            p.extra.SetOnClick(click);
            Fit();
            return this;
        }

        // đã mua / đã nhận: chữ trong dải tên, tắt nút, nền ngả xám
        public PackCell Done(string text)
        {
            p.done.gameObject.SetActive(true);
            p.done.text = text;
            p.buy.gameObject.SetActive(false);
            p.extra.gameObject.SetActive(false);
            Paint(hue.Dim());
            Fit();
            return this;
        }

        // chiều cao ô: phần trên (mô tả, hàng món, ghi chú) + dải tên đáy
        void Fit()
        {
            int n = p.items.childCount;
            p.items.gameObject.SetActive(n > 0);
            var g = Grid;
            int rows = n == 0 ? 0 : (n + PerRow - 1) / PerRow;
            float itemsH = rows == 0 ? 0 : (rows * g.cellSize.y + (rows - 1) * g.spacing.y) * ItemScale;
            var le = p.items.GetComponent<LayoutElement>();
            if (le) le.preferredHeight = itemsH;
            float top = 24 + (p.desc.gameObject.activeSelf ? 66 : 0) + (itemsH > 0 ? itemsH + 10 : 0) + (p.note.gameObject.activeSelf ? 46 : 0);
            float h = top + Strip;
            if (p.extra.gameObject.activeSelf) h = Mathf.Max(h, Strip + 116);
            if (p.layout) p.layout.preferredHeight = Mathf.Max(h, 200);
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

        // trứng capsule bậc tier: bản 2 (Assets/03 Art/Shop/v2/trung2_<bậc>.png, ArtGen/Shop/v2/cat_v2.py, 2026-11-27). Bản đầu
        // (trung_<bậc>.png) đã bỏ khỏi game 2026-11-27 cho nhẹ bản build.
        public static Sprite Egg(int tier) => App.Art.Get("trung2_" + Mathf.Clamp(tier, 0, Eggs.Tiers - 1));

        // đường nối vòm / thân của hình trứng, tính từ đỉnh ảnh xuống (ArtGen/Shop/v2/trung2.json)
        static readonly float[] Seam = { 0.4934f, 0.551f, 0.5155f, 0.4745f, 0.5261f };
        public static float EggSeam(int tier) => Seam[Mathf.Clamp(tier, 0, Seam.Length - 1)];

        // hình gói cửa hàng bản 2 (Assets/03 Art/Shop/v2, gen 2026-11-27 học bố cục hình gói Clash of Critters: vật to, viền sticker trắng dày,
        // bậc càng cao càng nhiều vàng, ngọc). Bản đầu goi_bi_<k> đã bỏ 2026-11-27.
        public static Sprite Balls(int k) => App.Art.Get("goi2_bi_" + k);

        // hình riêng của gói theo mã gói (null: gói không có hình riêng, nơi gọi tự chọn theo món)
        public static Sprite PackArt(string id)
        {
            string n;
            switch (id)
            {
                case "starter3": n = "goi2_nhap_mon"; break;
                case "launch": n = "goi2_khoi_hanh_1"; break;
                case "launch_2": n = "goi2_khoi_hanh_2"; break;
                case "launch_3": n = "goi2_khoi_hanh_3"; break;
                case "piggy": n = "goi2_lo_bi"; break;
                case "weekly_hero": n = "goi2_tuong_tuan"; break;
                case "week_card": n = "goi2_the_tuan"; break;
                case "adventure_pass": n = "goi2_the_phieu_luu"; break;
                case "fund": n = "goi2_quy"; break;
                case "no_ads": n = "goi2_bo_qc"; break;
                case "evo_daily": n = "goi2_da_nho"; break;
                case "evo_week": n = "goi2_da_lon"; break;
                case "ticket_rare": n = "goi2_ve"; break;
                case "refill_1": n = "goi2_bi_2"; break;
                case "refill_2": n = "goi2_bi_3"; break;
                case "refill_3": n = "goi2_bi_4"; break;
                default: return null;
            }
            return App.Art.HasArt(n) ? App.Art.Get(n) : null;
        }

        // icon riêng của loại ưu đãi động (Assets/03 Art/Shop/v2/uu2_<mã mẫu>.png, ArtGen/Shop/v2/cat_v2.py, gen 2026-11-27 cùng bộ hình gói bản 2):
        // flash hộp quà tia sét, hot trứng trong lửa + đồng hồ, relief phao + bình hồi sức, companion giỏ + bóng tim, nearstar huy chương sao +
        // mũi tên, jump tên lửa, newisle đảo + vé, comeback phong thư, chain ba hộp quà xích nối; mẫu chưa có icon riêng thì "uu2_offer" (thẻ
        // giá sao). Chưa nhập ảnh thì null, nơi gọi tự chọn theo món.
        public static Sprite TplArt(string tpl)
        {
            if (string.IsNullOrEmpty(tpl)) return null;
            if (App.Art.HasArt("uu2_" + tpl)) return App.Art.Get("uu2_" + tpl);
            return App.Art.HasArt("uu2_offer") ? App.Art.Get("uu2_offer") : null;
        }

        // hình của một ưu đãi đang mở: gói cố định thì hình gói (không có thì null), ưu đãi động thì icon loại ưu đãi
        public static Sprite OfferArt(ActiveOffer o) => o == null ? null : o.pack != null ? PackArt(o.pack) : TplArt(o.tpl);

        // nhãn giá trị hiển thị: gói có nhãn cố định (ShopPack.tag: ba bậc Khởi Hành ×5 / ×10 / ×20) thì lấy nhãn, không thì tính theo món
        public static double ShownMult(ActiveOffer o)
        {
            var pk = o?.pack != null ? App.Data.Cfg.shop.Pack(o.pack) : null;
            return pk != null && pk.tag > 0 ? pk.tag : Shop.OfferMult(App.Save.Data, App.Data, o);
        }

        public static double ShownMult(ShopPack pk) => pk.tag > 0 ? pk.tag : Shop.PackMult(App.Save.Data, App.Data, pk);

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

        // hình, số, tên, độ hiếm của một món (ô thưởng RewardTile, ô món thẻ cửa hàng ShopItemCell); hero != null: mảnh tướng (mặt tướng)
        public struct ItemLook
        {
            public Sprite icon;
            public string count, name;
            public Rarity? rarity;
            public Color tint;
            public HeroDef hero;
            public int eggTier; // -1: không phải trứng
        }

        public static ItemLook Look(ShopItem it)
        {
            var art = App.Art;
            it = Shop.Norm(it);
            var l = new ItemLook { count = "×" + NumFmt.Short(it.n), name = ItemName(it), tint = Color.white, eggTier = -1 };
            switch (it.k)
            {
                case "balls": l.icon = art.Icon("ball"); break;
                case Shop.Egg:
                    l.icon = Egg(it.r);
                    l.rarity = (Rarity)Mathf.Clamp(it.r, 0, Eggs.Tiers - 1);
                    l.eggTier = it.r;
                    break;
                // vé: hình vé vàng bản 2 (icon hai người cũ khó hiểu trong popup chọn gói, 2026-11-27)
                case Shop.Ticket: l.icon = art.HasArt("goi2_ve") ? art.Get("goi2_ve") : art.Icon("team"); l.rarity = it.r >= 3 ? Rarity.Epic : Rarity.Rare; break;
                case Shop.TicketWeek: l.icon = art.HasArt("goi2_ve") ? art.Get("goi2_ve") : art.Icon("star"); l.rarity = Rarity.Epic; break;
                // đá tiến hóa (2026-11-17): icon đá tiềm năng tô tím lam, khung Huyền thoại (như RewardTile.EvoStones)
                case "evo": l.icon = art.Icon("rock"); l.rarity = Rarity.Legend; l.tint = RewardTile.EvoTint; break;
                case "stones": l.icon = art.Icon("rock"); l.rarity = Rarity.Epic; break;
                case "crystal": l.icon = art.Icon("shard"); l.rarity = Rarity.Legend; break;
                case "shards":
                    l.hero = App.Data.Hero(it.h);
                    if (l.hero == null)
                    {
                        l.icon = art.Icon("shard");
                        l.name = Loc.T("Mảnh tướng");
                    }
                    else l.name = l.hero.name;
                    break;
                case "copies":
                    var oh = App.Data.Hero(it.h);
                    l.icon = art.Icon("cards");
                    l.rarity = Rarity.Rare;
                    if (oh != null) l.name = Loc.F("Thẻ {0}", oh.name);
                    break;
                case "week_card": l.icon = art.Icon("clock"); l.count = "7"; l.rarity = Rarity.Rare; break;
                case "month_card": l.icon = art.Icon("clock"); l.count = "30"; l.rarity = Rarity.Epic; break;
                case "no_ads": l.icon = art.Icon("tv"); l.count = ""; l.rarity = Rarity.Epic; break;
                default: l.icon = art.Icon("star"); break;
            }
            return l;
        }

        public static void Tile(RewardTile t, ShopItem it)
        {
            var l = Look(it);
            if (l.hero != null)
            {
                t.Hero(l.hero, l.count);
                return;
            }
            t.Item(l.icon, l.count, l.name, l.rarity, l.tint == Color.white ? (Color?)null : l.tint);
            // trứng: nhãn "nở mảnh" cho người chơi biết trứng ra mảnh tướng
            if (l.eggTier >= 0) t.Tag(Loc.T("nở mảnh"), TierColor(l.eggTier));
        }
    }
}
