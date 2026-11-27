// Popup ưu đãi kiểu mới, học bố cục popup gói của Clash of Critters (người dùng 2026-11-27: "icon quá nhỏ ... thiết kế lại pack này theo style
// của clash of critters ... panel pop up nên đổi kiểu"; sau đó duyệt tông màn cửa hàng bản 3 và dặn "làm popup và trang con cùng tông màu này
// luôn"). Prefab Assets/04 Prefabs/Dialogs/PopUuDai (biến thể tờ giấy gốc HopThoai, ẩn tờ giấy, khung riêng), menu "PokiClash/Prefab/Hộp thoại
// và màn/Cửa hàng: popup ưu đãi (PopUuDai)". Tông bản 3 (ShopHue, Assets/03 Art/Shop/v3, GD_Claude/26 mục 15):
// - Khung chàm tối caro viền mực; đầu là thẻ hai mảng màu tươi (the_nen tô màu chính, the_phai caro chéo tô màu phụ, the_tia sao nổ) như thẻ
//   cửa hàng, hình gói to tràn quá mép trên (gói tướng thì mặt tướng), ruy băng đỏ "Giá trị ×N" chìa mép, đồng hồ góc trái, tên vàng trong
//   dải tối đáy thẻ.
// - Thân: gói nhận theo ngày (Quà Nhập Môn) là 3 ô NGÀY 1-3; nhóm chọn một (Khởi Hành 3 bậc) là 3 ô bậc, mỗi ô một nút giá; gói thường là
//   lưới ô món (Items/OMonCuaHang, ô kem vạch số tối) to. Dưới: nhãn "Chỉ mua 1 lần", nút giá xanh lá to thở; ngoài khung "Hôm nay không hiện nữa".
// - Hết bi / Sắp hết bi (kind "refill", hợp đồng với phiên làm sự kiện máy bi): lần đầu (first) chỉ ô miễn phí (quảng cáo nhận bi, Cây bi ở
//   Nhà, Lọ Bi); sau đó 3 ô gói refill_1..3 + hàng nút miễn phí (quảng cáo, Tới Nhà).
// - Nhóm chọn một (bản 4, người dùng 2026-11-27 gửi popup nạp đầu Critters: "thiết kế lại theo cái này, độ cao tăng dần, giá trị phải để thẳng
//   trên đầu luôn làm nổi bật, list từng thứ to và rõ ràng. Không cần khung đen, làm thành pop up full screen nền tối"; "thông tin còn bao
//   nhiêu tiếng để hẳn trên đầu làm rõ ràng ra"): nhánh riêng ShowGroup, không khung, không thẻ đầu; nền tối phủ cả màn (nen_toi + caro mờ);
//   đầu: hình gói to bên trái đè băng tím tên vàng, ngay dưới là viên đỏ đồng hồ to "Còn 1 ngày 19 giờ"; các ô cột cao dần theo bậc, đáy
//   thẳng hàng, huy hiệu sao nổ "×N GIÁ TRỊ" trên đỉnh mỗi ô (đập vào lần lượt), món xếp một cột ô to; dưới: "Bạn chỉ được mua 1 gói!".
//   Nhãn giá trị theo ShopPack.tag nếu có (ba bậc Khởi Hành ×5 / ×10 / ×20, chỉ là nhãn). Nền ô màu trơn + hoa văn mờ (OfferPopColumn.Plain).
// - Hết bi có gói (ShowRefillGroup) cùng kiểu cột cao dần; gói theo ngày (ShowDaysGroup: Quà Nhập Môn) cùng nền tối, ô ngày cao bằng nhau,
//   huy hiệu giá trị ở đầu, nút giá to; Hết bi lần đầu cũng nền tối (mỗi cách miễn phí một ô); quà trở lại (ShowComeback) hai ô quà đã nhận
//   + Gói Trở Lại. Khung bản 3 (Layout, Head, Grid) chỉ còn làm đường lui khi ưu đãi không tìm thấy.
// - Gói lẻ (ShowSingle) và Lọ Bi (ShowPiggy, người dùng 2026-11-27: "đổi luôn popup gói lẻ theo style này", "căn chỉnh phần này vào giữa")
//   cùng nền tối: đầu như gói theo ngày, các món trong một ô trơn hoa văn đặt giữa, dòng phụ + nút giá to dưới.
// - Hiệu ứng (người dùng: "thêm fx glow ánh sáng các kiểu vào cho đẹp"; Quà Nhập Môn "phải nhấn mạnh giá trị, làm thêm hiệu ứng"): quầng
//   sáng ấm phập phồng + vầng tia xoay sau hình gói, quầng hồng + tia xoay ngược sau huy hiệu giá trị, lấp lánh (UI/Kit/Twinkle.cs); ngày 3
//   có quầng + tia riêng. Gói theo ngày 3 ngày xếp tam giác: ngày 1 dưới trái → ngày 2 trên giữa → ngày 3 dưới phải (ô to nhất), mũi tên
//   cong vẽ tay nối (mui_ten.png).
// - Popup khác (Chuỗi Quà, giới thiệu thẻ / quỹ, quà hôm nay) vẫn dùng tờ ShopSheet.
using System;
using System.Collections;
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
    public sealed class OfferPopup : Dialog
    {
        [Serializable]
        public struct Parts
        {
            public RectTransform sheet, header, value, content, pills, buyWrap, closeBtn;
            public Image headBg, headPanel, headRays, packArt;
            public TextMeshProUGUI title, sub, valueText, limit, timer;
            public GridLayoutGroup grid;
            public HorizontalLayoutGroup row;
            public GameObject limitPill, timerPill;
            public SketchButton buy, mute;
            public RectTransform freeRow; // hàng nút miễn phí của popup Hết bi (quảng cáo, Tới Nhà)
            public SketchButton freeAd, freeHome;
            // nhóm chọn một (bản 4): khung bản 3 ẩn đi, nền tối phủ màn, băng tên, đồng hồ to
            public GameObject frame, backdrop;
            public RectTransform banner, bigTimer;
            public TextMeshProUGUI bannerTitle, bigTimerText;
            public Image bigTimerBg;
            // huy hiệu giá trị ở đầu (gói theo ngày: một giá cho cả gói)
            public RectTransform headBadge;
            public TextMeshProUGUI headBadgeText, headBadgeSub;
            public RectTransform fxPack, fxBadge, fxDay; // cụm hiệu ứng dựng sẵn: sau hình gói, sau huy hiệu giá trị, sau ô ngày 3
            public Image[] arrows; // mũi tên cong ngày 1 → 2 → 3
        }

        [SerializeField] Parts p;
        [SerializeField] ShopItemCell itemPrefab;
        [SerializeField] OfferPopColumn columnPrefab;

        // khung (điểm của khung 1080): bề rộng, lề, bề rộng nội dung, cao thẻ đầu
        public const float W = 960, Inset = 16, ContentW = 880, HeaderH = 450;
        // nhóm chọn một: bề rộng, cao vùng đầu (hình gói, băng tên, đồng hồ), chỗ huy hiệu chìa trên ô cao nhất
        public const float GroupW = 1040, GroupHeadH = 340, BadgeRoom = 118;
        static readonly Color Urgent = new Color32(0xe8, 0x28, 0x5a, 0xff), TimerRed = new Color32(0xd8, 0x22, 0x4e, 0xff);

        bool bought, muted, breathing, grouped;
        double until;
        float packY0, timerTick;
        bool alive;
        readonly List<RectTransform> pops = new List<RectTransform>(), badges = new List<RectTransform>();

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static ShopConfig C => App.Data.Cfg.shop;
        static double Now => SaveService.Now();

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, ShopItemCell item, OfferPopColumn column)
        {
            p = parts;
            itemPrefab = item;
            columnPrefab = column;
        }

        public static bool Available => Theme.Prefabs && Theme.Prefabs.dialogs.Any(d => d is OfferPopup);

        // popup bán (offer, comeback, refill) kiểu mới; closed(đã mua, tích "Hôm nay không hiện nữa")
        public static bool Handles(Popup pop) => Available && (pop.kind == "offer" || pop.kind == "comeback" || pop.kind == "refill" || pop.kind == "piggy");

        public static OfferPopup Open(Popup pop, Action<bool, bool> closed)
        {
            OfferPopup v = null;
            v = App.Modals.Open<OfferPopup>(() => closed?.Invoke(v != null && v.bought, v != null && v.muted));
            v.Show(pop);
            return v;
        }

        // ---------- dựng ----------

        void Show(Popup pop)
        {
            p.freeRow.gameObject.SetActive(false);
            if (pop.kind == "refill")
            {
                ShowRefill(pop);
                return;
            }
            if (pop.kind == "piggy")
            {
                ShowPiggy(pop);
                return;
            }
            var o = Shop.FindOffer(S, pop.id);
            var pk = o?.pack != null ? C.Pack(o.pack) : null;
            string title = o != null ? ShopService.OfferName(o) : Loc.T("Ưu đãi");
            string sub = null;
            if (pop.kind == "comeback")
            {
                var gift = Shop.Resolve(S, D, C.comebackGift, true, null);
                Shop.Grant(S, D, gift, Now, new Rng(Rng.RandomSeed()));
                App.Save.Save();
                ShopLog.Event("claim", "Quà trở lại", 0);
                ShowComeback(pop, o, pk, gift);
                return;
            }

            // nhóm chọn một (nạp đầu 3 bậc): các gói cùng nhóm thành ô
            var group = o?.pack != null && pk?.group == o.pack
                ? new[] { o }.Concat(Shop.Live(S, Now).Where(x => x.pack != null && x.pack != o.pack && C.Pack(x.pack)?.group == o.pack))
                    .Where(x => !x.bought && (x.until <= 0 || x.until > Now)).OrderBy(x => C.Pack(x.pack)?.price ?? x.price).ToList()
                : null;
            bool isGroup = group != null && group.Count > 1;
            if (isGroup)
            {
                ShowGroup(pop, o, pk, group);
                return;
            }
            bool isDays = !isGroup && pk != null && pk.kind == "days" && pk.days != null && pk.days.Count > 0;
            if (isDays && o != null)
            {
                ShowDaysGroup(pop, o, pk);
                return;
            }
            if (o != null && pop.kind != "comeback")
            {
                ShowSingle(pop, o, pk);
                return;
            }

            sub ??= pop.warn ? Loc.T("Sắp hết giờ!") :
                isGroup ? Loc.T("Chọn một gói: mua gói nào thì các gói kia đóng lại.") :
                isDays ? Loc.F("Mua một lần, nhận quà {0} ngày liền!", pk.days.Count) :
                o?.tpl == "relief" ? Loc.T("Mạnh hơn cho ải đang kẹt.") :
                o?.tpl == "hot" ? Loc.T("Chỉ trong 10 phút!") :
                o?.tpl == "jump" && o.hero != null && D.Hero(o.hero) != null ? JumpLine(o) : pk?.Desc;

            var items = o != null ? Shop.OfferItems(S, D, o) : new List<ShopItem>();
            Head(title, sub, HueOf(o, pk, isGroup), pop.kind == "comeback" && o == null ? ShopUi.TplArt("comeback") ?? HeaderArt(o, pk, items) : HeaderArt(o, pk, items),
                o != null && !isGroup ? Shop.OfferMult(S, D, o) : isGroup ? group.Max(x => Shop.OfferMult(S, D, x)) : 0, isGroup);

            float contentH = Grid(items);

            // giới hạn, đồng hồ, nút giá
            until = isGroup ? group.Min(x => x.until > 0 ? x.until : double.MaxValue) : o?.until ?? 0;
            if (until >= double.MaxValue) until = 0;
            p.pills.gameObject.SetActive(true);
            p.limit.text = Loc.T("Chỉ mua 1 lần");
            p.timerPill.SetActive(until > 0);
            UpdateTimer();
            p.buyWrap.gameObject.SetActive(!isGroup && o != null);
            if (!isGroup && o != null)
            {
                p.buy.SetText(ShopService.Price(pk?.price ?? o.price));
                p.buy.SetOnClick(() => ShopService.BuyOffer(o.uid, AfterBuy));
            }
            Mute(!pop.free);
            Layout(contentH, !isGroup && o != null);
            alive = true;
            StartCoroutine(Intro());
        }

        // thẻ đầu: màu, hình gói, nhãn giá trị, tên, dòng phụ
        void Head(string title, string sub, ShopHue hue, Sprite art, double mult, bool upTo)
        {
            p.title.text = title;
            p.sub.text = sub ?? "";
            p.headBg.color = hue.fill;
            p.headPanel.color = hue.panel;
            p.headRays.color = hue.rays;
            Theme.SetSprite(p.packArt, art);
            p.packArt.preserveAspect = true;
            bool show = mult >= 1.5;
            p.value.gameObject.SetActive(show);
            if (show) p.valueText.text = upTo ? Loc.F("Tới ×{0}", Math.Round(mult)) : ShopHue.ValueText(mult);
        }

        void Mute(bool on)
        {
            p.mute.gameObject.SetActive(on);
            SetMute();
            p.mute.SetOnClick(() =>
            {
                muted = !muted;
                SetMute();
            });
        }

        // xếp các khối theo chiều dọc: thẻ đầu, dòng phụ, nội dung, hàng nút miễn phí, nhãn, nút giá; cao khung theo nội dung
        void Layout(float contentH, bool hasBuy)
        {
            bool strip = p.freeRow.gameObject.activeSelf, pills = p.pills.gameObject.activeSelf;
            p.header.sizeDelta = new Vector2(W - 2 * Inset, HeaderH);
            p.header.anchoredPosition = new Vector2(0, -Inset);
            float y = -Inset - HeaderH;
            Place((RectTransform)p.sub.transform, y - 44); // tâm dòng phụ
            y -= 88;
            p.content.sizeDelta = new Vector2(ContentW, contentH);
            Place(p.content, y);
            y -= contentH + 22;
            if (strip)
            {
                Place(p.freeRow, y);
                y -= 104 + 18;
            }
            if (pills)
            {
                Place(p.pills, y);
                y -= 54 + 20;
            }
            if (hasBuy)
            {
                Place(p.buyWrap, y - 68); // tâm khung nút
                y -= 136;
            }
            y -= 34;
            p.sheet.sizeDelta = new Vector2(W, -y);
            Place((RectTransform)p.mute.transform, y - 26); // dưới khung
            // hình gói (tâm) tràn quá mép trên thẻ đầu 60
            var pr = p.packArt.rectTransform;
            pr.sizeDelta = new Vector2(430, 430);
            packY0 = 60 - 215;
            pr.anchoredPosition = new Vector2(0, packY0);
        }

        static void Place(RectTransform r, float y) => r.anchoredPosition = new Vector2(r.anchoredPosition.x, y);

        // màu thẻ theo loại gói, như thẻ cửa hàng bản 3: hồng (quà nhập môn, trở lại), vàng (khởi hành), nho (gói tướng), cam (hẹn giờ),
        // dung nham (nóng)
        static ShopHue HueOf(ActiveOffer o, ShopPack pk, bool group)
        {
            if (o == null) return ShopHue.Berry;
            if (group || pk?.group == "launch") return ShopHue.Gold;
            if (pk != null && pk.kind == "days") return ShopHue.Berry;
            switch (o.tpl)
            {
                case "jump":
                case "companion":
                case "nearstar":
                case "newisle":
                    return ShopHue.Grape;
                case "hot": return ShopHue.Lava;
                case "comeback": return ShopHue.Berry;
                default: return ShopHue.Sunset;
            }
        }

        // hình gói riêng (bản 2) > mặt tướng (gói tướng) > icon loại ưu đãi (ShopUi.TplArt) > hình theo món
        static Sprite HeaderArt(ActiveOffer o, ShopPack pk, List<ShopItem> items)
        {
            var own = pk != null ? ShopUi.PackArt(pk.id) : null;
            if (own) return own;
            var hero = items.FirstOrDefault(i => i.k == "shards")?.h ?? o?.hero;
            var h = hero != null ? D.Hero(hero) : null;
            var face = h != null ? HeroArt.Face(h) : null;
            return face ? face : ShopUi.OfferArt(o) ?? ShopPage.ArtFor(items);
        }

        static string JumpLine(ActiveOffer o)
        {
            string name = D.Hero(o.hero).name;
            var pw = Offers.JumpPower(S, D, o.hero);
            return pw.pack > pw.best && pw.best > 0
                ? Loc.F("{0} về đội ngay, lực chiến {1} (tướng mạnh nhất của bạn: {2}).", name, pw.pack, pw.best)
                : Loc.F("{0} về đội ngay: đủ mảnh lên sao, kèm thẻ và đá tiến hóa.", name);
        }

        // ---------- nội dung ----------

        void ClearContent()
        {
            foreach (Transform t in new[] { p.grid.transform, p.row.transform })
                for (int i = t.childCount - 1; i >= 0; i--) Destroy(t.GetChild(i).gameObject);
            pops.Clear();
            badges.Clear();
        }

        void UseRow(float gap)
        {
            ClearContent();
            p.grid.gameObject.SetActive(false);
            p.row.gameObject.SetActive(true);
            p.row.spacing = gap;
        }

        // gói thường: lưới ô món to (ít món thì ô to hơn)
        float Grid(List<ShopItem> items)
        {
            ClearContent();
            p.row.gameObject.SetActive(false);
            p.grid.gameObject.SetActive(true);
            int n = Mathf.Max(1, items.Count);
            int cols = n <= 4 ? n : n <= 6 ? 3 : 4;
            int rows = Mathf.CeilToInt(n / (float)cols);
            const float gap = 20;
            float w = Mathf.Min(n <= 2 ? 250 : n <= 4 ? 200 : 190, (ContentW - (cols - 1) * gap) / cols);
            p.grid.cellSize = new Vector2(w, w);
            p.grid.spacing = new Vector2(gap, gap);
            p.grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            p.grid.constraintCount = cols;
            foreach (var it in items) pops.Add((RectTransform)Ui.Spawn(itemPrefab, p.grid.transform).Set(it).transform);
            return rows * w + (rows - 1) * gap;
        }

        static readonly ShopHue[] DayHue = { ShopHue.Berry, ShopHue.Sky, ShopHue.Gold, ShopHue.Grape, ShopHue.Mint, ShopHue.Sunset, ShopHue.Lava };

        // gói nhận theo ngày (người dùng 2026-11-27 gửi popup Quà Nhập Môn: "pop up này cũng sửa theo style vừa làm"): nền tối phủ màn như
        // nhóm chọn một; đầu: hình gói + băng tên + viên đỏ đồng hồ to + huy hiệu "×N GIÁ TRỊ" (một giá cho cả gói); mỗi ngày một ô cao bằng
        // nhau (quà mỗi ngày ngang nhau, như ô ngày gói 3 ngày của Critters) nền trơn hoa văn không dải đáy, "NGÀY 1" trên đầu, "Nhận ngay"
        // ở ngày 1, món một cột ô to; dưới: dòng "Mua một lần, nhận quà 3 ngày liền!", nút giá to thở
        void ShowDaysGroup(Popup pop, ActiveOffer o, ShopPack pk)
        {
            EnterGroupLook();
            p.bannerTitle.text = ShopService.OfferName(o);
            Theme.SetSprite(p.packArt, HeaderArt(o, pk, Shop.OfferItems(S, D, o)));
            p.packArt.preserveAspect = true;
            p.sub.text = pop.warn ? Loc.T("Sắp hết giờ!") : Loc.F("Mua một lần, nhận quà {0} ngày liền!", pk.days.Count);
            p.sub.fontSizeMax = 36;
            HeadRow(o.until, ShopUi.ShownMult(o));
            bool tri = pk.days.Count == 3;
            float h = tri ? DaysTriangle(pk) : DaysColumns(pk) + 30;
            p.buyWrap.gameObject.SetActive(true);
            p.buy.SetText(ShopService.Price(pk.price));
            p.buy.SetOnClick(() => ShopService.BuyOffer(o.uid, AfterBuy));
            Mute(!pop.free);
            LayoutGroup(h, false, true);
            HeadFx();
            alive = true;
            StartCoroutine(Intro());
        }

        // hàng đầu của popup một giá: viên đỏ đồng hồ to (nếu hẹn giờ) + huy hiệu "×N GIÁ TRỊ" bên phải
        void HeadRow(double untilMs, double mult)
        {
            until = untilMs;
            p.bigTimer.gameObject.SetActive(until > 0);
            p.bigTimer.anchoredPosition = new Vector2(40, -236);
            p.bigTimer.sizeDelta = new Vector2(440, 84);
            UpdateTimer();
            if (p.headBadge && mult >= 1.5)
            {
                p.headBadge.gameObject.SetActive(true);
                p.headBadgeText.text = "×" + Math.Round(mult);
                p.headBadgeSub.text = Loc.T("GIÁ TRỊ");
                badges.Add(p.headBadge);
            }
        }

        // ba ngày xếp tam giác: ngày 1 dưới trái → ngày 2 trên giữa → ngày 3 dưới phải (ô to nhất, có quầng + tia), mũi tên cong nối; trả cao
        // vùng nội dung (gồm chỗ nhãn "Nhận ngay" chìa)
        float DaysTriangle(ShopPack pk)
        {
            UseRow(0);
            p.row.enabled = false; // đặt tay
            var lists = Enumerable.Range(0, 3).Select(i => Shop.Resolve(S, D, pk.days[i].items, pk.scale, null)).ToList();
            const float cs = 140, big = 190;
            float hd = OfferPopColumn.HeadH, half = (GroupW - 40) / 2;
            Vector2 Size(int m, float c, float minW) => new Vector2(Mathf.Max(minW, m * c + (m - 1) * 10 + 60), hd + 14 + c + 36);
            var sizes = new[]
            {
                Size(Mathf.Max(1, lists[0].Count), cs, 230), Size(Mathf.Max(1, lists[1].Count), cs, 230), Size(Mathf.Max(1, lists[2].Count), big, 300),
            };
            // tâm ngang, mép trên (tính từ đỉnh vùng nội dung)
            var pos = new[] { new Vector2(-half + sizes[0].x / 2 + 8, 200), new Vector2(0, 34), new Vector2(half - sizes[2].x / 2 - 8, 186) };
            var nodes = new RectTransform[3];
            float bottom = 0;
            DayFx(new Vector2(pos[2].x, -(pos[2].y + sizes[2].y / 2)), sizes[2]); // quầng + tia sau cả ba ô
            for (int i = 0; i < 3; i++)
            {
                var col = Ui.Spawn(columnPrefab, p.row.transform).Set(Loc.F("NGÀY {0}", i + 1), DayHue[i % DayHue.Length], sizes[i]);
                var r = col.Rect;
                r.anchorMin = r.anchorMax = new Vector2(0.5f, 1);
                r.pivot = new Vector2(0.5f, 1);
                r.anchoredPosition = new Vector2(pos[i].x, -pos[i].y);
                col.Plain(false);
                int m = Mathf.Max(1, lists[i].Count);
                float c = i == 2 ? big : cs;
                col.Fill(itemPrefab, lists[i], m, new Vector2(c, c), hd + 10, 24, true);
                if (i == 0) col.Tag(Loc.T("Nhận ngay"), Theme.GreenD);
                nodes[i] = r;
                bottom = Mathf.Max(bottom, pos[i].y + sizes[i].y);
            }
            // mũi tên 1 → 2 (góc trên trái, đi lên rẽ phải), 2 → 3 (góc trên phải, xoay -90°: đi phải rẽ xuống)
            var a1 = Arrow(0, new Vector2(-half * 0.56f, -108), 0);
            var a2 = Arrow(1, new Vector2(half * 0.56f, -108), -90);
            pops.Add(nodes[0]);
            if (a1) pops.Add(a1);
            pops.Add(nodes[1]);
            if (a2) pops.Add(a2);
            pops.Add(nodes[2]);
            return bottom + 20;
        }

        // mũi tên cong dựng sẵn (prefab, tắt sẵn): đặt chỗ, xoay, bật
        RectTransform Arrow(int i, Vector2 pos, float rot)
        {
            if (p.arrows == null || i >= p.arrows.Length || !p.arrows[i]) return null;
            var rt = p.arrows[i].rectTransform;
            rt.anchoredPosition = pos;
            rt.localEulerAngles = new Vector3(0, 0, rot);
            p.arrows[i].gameObject.SetActive(true);
            return rt;
        }

        // ngày 3 (quà lớn): cụm quầng ấm + tia xoay + lấp lánh dựng sẵn sau các ô (con của vùng nội dung, trước hàng ô), co theo cỡ ô
        void DayFx(Vector2 center, Vector2 size)
        {
            if (!p.fxDay) return;
            p.fxDay.anchoredPosition = center;
            p.fxDay.localScale = Vector3.one * (Mathf.Max(size.x, size.y) / 330f);
            p.fxDay.gameObject.SetActive(true);
        }

        // hiệu ứng đầu popup (dựng sẵn sau băng tên): quầng sáng ấm + vầng tia + lấp lánh sau hình gói; quầng hồng + tia ngược + lấp lánh sau
        // huy hiệu giá trị khi huy hiệu hiện
        void HeadFx()
        {
            var art = p.packArt.rectTransform;
            if (p.fxPack)
            {
                p.fxPack.anchoredPosition = new Vector2(art.anchoredPosition.x, packY0);
                p.fxPack.gameObject.SetActive(true);
            }
            if (p.fxBadge)
            {
                bool on = p.headBadge && p.headBadge.gameObject.activeSelf;
                p.fxBadge.gameObject.SetActive(on);
                if (on) p.fxBadge.anchoredPosition = p.headBadge.anchoredPosition;
            }
        }

        // ---------- gói lẻ, Lọ Bi (bản 4) ----------

        string OfferLine(Popup pop, ActiveOffer o, ShopPack pk) =>
            pop.warn ? Loc.T("Sắp hết giờ!") :
            o.tpl == "relief" ? Loc.T("Mạnh hơn cho ải đang kẹt.") :
            o.tpl == "hot" ? Loc.T("Chỉ trong 10 phút!") :
            o.tpl == "jump" && o.hero != null && D.Hero(o.hero) != null ? JumpLine(o) : pk?.Desc;

        void ShowSingle(Popup pop, ActiveOffer o, ShopPack pk)
        {
            EnterGroupLook();
            var items = Shop.OfferItems(S, D, o);
            p.bannerTitle.text = ShopService.OfferName(o);
            Theme.SetSprite(p.packArt, HeaderArt(o, pk, items));
            p.packArt.preserveAspect = true;
            p.sub.text = OfferLine(pop, o, pk) ?? "";
            p.sub.fontSizeMax = 34;
            HeadRow(o.until, ShopUi.ShownMult(o));
            float h = ItemsNode(items, HueOf(o, pk, false), Loc.T("BẠN NHẬN ĐƯỢC"));
            p.buyWrap.gameObject.SetActive(true);
            p.buy.SetText(ShopService.Price(pk?.price ?? o.price));
            p.buy.SetOnClick(() => ShopService.BuyOffer(o.uid, AfterBuy));
            Mute(!pop.free);
            LayoutGroup(h + 30, false, true);
            HeadFx();
            alive = true;
            StartCoroutine(Intro());
        }

        void ShowPiggy(Popup pop)
        {
            EnterGroupLook();
            var st = Shop.Of(S);
            int n = (int)Math.Floor(st.piggy);
            double cap = Shop.PiggyCap(S, C);
            var pk = C.Pack("piggy");
            p.bannerTitle.text = Shop.PiggyFull(S, C) ? Loc.T("Lọ Bi đầy rồi!") : Loc.T("Lọ Bi");
            Theme.SetSprite(p.packArt, ShopUi.PackArt("piggy") ?? ShopUi.Balls(3));
            p.packArt.preserveAspect = true;
            bool can = Shop.PiggyCanBreak(S, C, Now);
            double wait = Shop.PiggyWait(S, C, Now);
            p.sub.text = can ? Loc.T("Đập lọ để lấy hết bi đã tích. Mỗi bi bạn thả bỏ 1 bi vào lọ.")
                : wait > 0 ? Loc.F("Lọ vừa đập. Đập lại được sau {0}.", ShopUi.Clock(wait))
                : Loc.F("Đủ {0} bi mới đập được. Mỗi bi bạn thả bỏ 1 bi vào lọ.", Math.Ceiling(cap * C.piggy.minPct));
            p.sub.fontSizeMax = 32;
            HeadRow(0, pk != null && pk.price > 0 ? n / (pk.price * C.valuePerUsd) : 0);
            float h = ItemsNode(new List<ShopItem> { new ShopItem { k = "balls", n = Math.Max(n, 0) } }, ShopHue.Gold,
                Loc.F("LỌ ĐANG CÓ {0}/{1}", NumFmt.Short(n), NumFmt.Short((int)cap)));
            p.buyWrap.gameObject.SetActive(can && pk != null);
            if (can && pk != null)
            {
                p.buy.SetText(Loc.F("Đập lọ {0}", ShopService.Price(pk.price)));
                p.buy.SetOnClick(() => ShopService.BuyPack("piggy", AfterBuy));
            }
            Mute(!pop.free);
            LayoutGroup(h + 30, false, can && pk != null);
            HeadFx();
            alive = true;
            StartCoroutine(Intro());
        }

        // quà trở lại (người dùng 2026-11-27: "đổi luôn popup quà trở lại theo style này"): nền tối, phong thư + băng "Mừng bạn trở lại!" +
        // đồng hồ / huy hiệu giá trị của Gói Trở Lại; hai ô cạnh nhau: "QUÀ ĐÃ NHẬN" (lá, nhãn "Miễn phí", quà vừa vào túi) và gói trả tiền
        // (hồng); dưới: "Quà trở lại đã vào túi!" + nút giá của gói
        void ShowComeback(Popup pop, ActiveOffer o, ShopPack pk, List<ShopItem> gift)
        {
            EnterGroupLook();
            p.bannerTitle.text = Loc.T("Mừng bạn trở lại!");
            Theme.SetSprite(p.packArt, ShopUi.TplArt("comeback") ?? ShopUi.Balls(3));
            p.packArt.preserveAspect = true;
            p.sub.text = Loc.T("Quà trở lại đã vào túi!");
            p.sub.fontSizeMax = 36;
            HeadRow(o?.until ?? 0, o != null ? ShopUi.ShownMult(o) : 0);
            var offerItems = o != null ? Shop.OfferItems(S, D, o) : new List<ShopItem>();
            var parts = new List<(List<ShopItem> items, ShopHue hue, string head, string tag)>();
            if (gift.Count > 0) parts.Add((gift, ShopHue.Mint, Loc.T("QUÀ ĐÃ NHẬN"), Loc.T("Miễn phí")));
            if (offerItems.Count > 0) parts.Add((offerItems, ShopHue.Berry, ShopService.OfferName(o).ToUpperInvariant(), null));
            const float gap = 28;
            UseRow(gap);
            p.row.childAlignment = TextAnchor.LowerCenter;
            float maxW = parts.Count > 1 ? (GroupW - 40 - gap) / 2 : GroupW - 60, h = 0;
            foreach (var (items, hue, head, tag) in parts)
            {
                int n = Mathf.Max(1, items.Count);
                int cols = parts.Count > 1 ? Mathf.Min(2, n) : n <= 4 ? n : 3;
                int rows = Mathf.CeilToInt(n / (float)cols);
                float cs = parts.Count > 1 ? (n == 1 ? 190 : 160) : n <= 2 ? 220 : 190;
                float w = Mathf.Min(maxW, Mathf.Max(380, cols * cs + (cols - 1) * 10 + 70));
                float hh = OfferPopColumn.HeadH + 16 + rows * cs + (rows - 1) * 14 + 36;
                var col = Ui.Spawn(columnPrefab, p.row.transform).Set(head, hue, new Vector2(w, hh));
                col.Plain(false);
                col.Fill(itemPrefab, items, cols, new Vector2(cs, cs), OfferPopColumn.HeadH + 10, 24, true);
                if (tag != null) col.Tag(tag, Theme.GreenD);
                pops.Add(col.Rect);
                h = Mathf.Max(h, hh);
            }
            bool buy = o != null && offerItems.Count > 0;
            p.buyWrap.gameObject.SetActive(buy);
            if (buy)
            {
                p.buy.SetText(ShopService.Price(pk?.price ?? o.price));
                p.buy.SetOnClick(() => ShopService.BuyOffer(o.uid, AfterBuy));
            }
            Mute(!pop.free);
            LayoutGroup(h + 30, false, buy);
            HeadFx();
            alive = true;
            StartCoroutine(Intro());
        }

        // một ô trơn hoa văn đặt giữa chứa các món (lưới, ít món thì ô to); trả cao ô
        float ItemsNode(List<ShopItem> items, ShopHue hue, string head)
        {
            UseRow(0);
            p.row.childAlignment = TextAnchor.LowerCenter;
            int n = Mathf.Max(1, items.Count);
            int cols = n <= 4 ? n : n <= 6 ? 3 : 4;
            int rows = Mathf.CeilToInt(n / (float)cols);
            float cs = n <= 2 ? 220 : n <= 4 ? 190 : 170;
            float w = Mathf.Min(GroupW - 60, Mathf.Max(420, cols * cs + (cols - 1) * 10 + 70));
            float h = OfferPopColumn.HeadH + 16 + rows * cs + (rows - 1) * 14 + 36;
            var col = Ui.Spawn(columnPrefab, p.row.transform).Set(head, hue, new Vector2(w, h));
            col.Plain(false);
            col.Fill(itemPrefab, items, cols, new Vector2(cs, cs), OfferPopColumn.HeadH + 10, 24, true);
            pops.Add(col.Rect);
            return h;
        }

        // ô ngày cao bằng nhau, đủ chỗ cho ngày nhiều món nhất (ô món một cột, cỡ tới 210)
        float DaysColumns(ShopPack pk)
        {
            int n = pk.days.Count;
            const float gap = 22, cellGap = 14;
            UseRow(gap);
            p.row.childAlignment = TextAnchor.LowerCenter;
            float w = Mathf.Min(330, (GroupW - 40 - (n - 1) * gap) / n);
            var lists = Enumerable.Range(0, n).Select(i => Shop.Resolve(S, D, pk.days[i].items, pk.scale, null)).ToList();
            int most = lists.Max(l => Mathf.Max(1, l.Count));
            float cs = Mathf.Min(210, w - 60);
            float h = Mathf.Max(480, OfferPopColumn.HeadH + 20 + most * cs + (most - 1) * cellGap + 34);
            for (int i = 0; i < n; i++)
            {
                var col = Ui.Spawn(columnPrefab, p.row.transform).Set(Loc.F("NGÀY {0}", i + 1), DayHue[i % DayHue.Length], new Vector2(w, h));
                col.Plain(false);
                col.Fill(itemPrefab, lists[i], 1, new Vector2(cs, cs), OfferPopColumn.HeadH + 12, 24, true);
                if (i == 0) col.Tag(Loc.T("Nhận ngay"), Theme.GreenD);
                pops.Add(col.Rect);
            }
            return h;
        }

        // ---------- nhóm chọn một (bản 4: nền tối phủ màn, cột cao dần, huy hiệu giá trị trên đỉnh) ----------

        void ShowGroup(Popup pop, ActiveOffer lead, ShopPack pk, List<ActiveOffer> group)
        {
            EnterGroupLook();
            p.bannerTitle.text = ShopService.OfferName(lead);
            Theme.SetSprite(p.packArt, HeaderArt(lead, pk, Shop.OfferItems(S, D, lead)));
            p.packArt.preserveAspect = true;
            p.sub.text = Loc.T("Bạn chỉ được mua 1 gói!");
            p.sub.fontSizeMax = 38;
            until = group.Min(x => x.until > 0 ? x.until : double.MaxValue);
            if (until >= double.MaxValue) until = 0;
            p.bigTimer.gameObject.SetActive(until > 0);
            UpdateTimer();
            // cao ô cao nhất theo cao màn (đầu + chỗ huy hiệu + dòng dưới + nút "Hôm nay không hiện nữa")
            float hMax = Mathf.Clamp(ScreenH - 820, 800, 1320);
            GroupColumns(group, hMax);
            Mute(!pop.free);
            LayoutGroup(hMax + BadgeRoom, false);
            HeadFx();
            alive = true;
            StartCoroutine(Intro());
        }

        float ScreenH
        {
            get
            {
                float h = ((RectTransform)transform).rect.height;
                return h < 1000 ? 1920 : h;
            }
        }

        // dáng chung của popup nhiều bậc (chọn một gói, Hết bi): tắt khung bản 3 + thẻ đầu, bật nền tối phủ màn và băng tên
        void EnterGroupLook()
        {
            grouped = true;
            if (p.frame) p.frame.SetActive(false);
            if (p.backdrop) p.backdrop.SetActive(true);
            p.header.gameObject.SetActive(false);
            p.value.gameObject.SetActive(false);
            p.pills.gameObject.SetActive(false);
            p.buyWrap.gameObject.SetActive(false);
            p.bigTimer.gameObject.SetActive(false);
            p.banner.gameObject.SetActive(true);
        }

        // các ô gói: cao dần theo giá (bậc sau cao hơn bậc trước một nấc), đáy thẳng hàng; ô món một cột, cùng cỡ ở mọi ô (cỡ lớn nhất vừa ô
        // chật nhất)
        void GroupColumns(List<ActiveOffer> list, float hMax)
        {
            int n = list.Count;
            const float gap = 22, step = 80, top = 108, cellGap = 14;
            float foot = OfferPopColumn.FootH + 16;
            UseRow(gap);
            p.row.childAlignment = TextAnchor.LowerCenter;
            float w = Mathf.Min(330, (GroupW - 40 - (n - 1) * gap) / n);
            var lists = list.Select(x => Shop.OfferItems(S, D, x)).ToList();
            float cs = Mathf.Min(190, w - 60);
            for (int i = 0; i < n; i++)
            {
                float hi = hMax - (n - 1 - i) * step;
                int m = Mathf.Max(1, lists[i].Count);
                cs = Mathf.Min(cs, (hi - top - foot - (m - 1) * cellGap) / m);
            }
            cs = Mathf.Max(90, Mathf.Floor(cs));
            ShopHue[] hues = { ShopHue.Sky, ShopHue.Grape, ShopHue.Sunset, ShopHue.Lava };
            for (int i = 0; i < n; i++)
            {
                var x = list[i];
                var pk = x.pack != null ? C.Pack(x.pack) : null;
                float hi = hMax - (n - 1 - i) * step;
                var col = Ui.Spawn(columnPrefab, p.row.transform).Set("", hues[i % hues.Length], new Vector2(w, hi));
                col.Plain().Badge(ShopUi.ShownMult(x), i % 2 == 0 ? -5 : 4);
                col.Fill(itemPrefab, lists[i], 1, new Vector2(cs, cs), top, OfferPopColumn.FootH, false);
                col.Button(ShopService.Price(pk?.price ?? x.price), () => ShopService.BuyOffer(x.uid, AfterBuy));
                pops.Add(col.Rect);
                if (col.BadgeRect) badges.Add(col.BadgeRect);
            }
        }

        // xếp dọc: đầu (hình gói trái, băng tên + đồng hồ / dòng phụ phải), hàng ô (chừa chỗ huy hiệu chìa), dòng "chỉ được mua 1 gói" (khi
        // dòng phụ không nằm trên), hàng nút miễn phí (Hết bi), nút tắt dưới
        void LayoutGroup(float contentH, bool subTop, bool buy = false)
        {
            var pr = p.packArt.rectTransform;
            pr.sizeDelta = new Vector2(330, 330);
            packY0 = -GroupHeadH / 2;
            pr.anchoredPosition = new Vector2(-GroupW / 2 + 180, packY0);
            pr.localEulerAngles = Vector3.zero;
            var sr = (RectTransform)p.sub.transform;
            if (subTop)
            {
                sr.sizeDelta = new Vector2(600, 100);
                sr.anchoredPosition = new Vector2(150, -250);
                p.sub.fontSizeMax = 32;
            }
            float y = -GroupHeadH;
            p.content.sizeDelta = new Vector2(GroupW - 40, contentH);
            Place(p.content, y);
            y -= contentH + 26;
            if (!subTop)
            {
                Place(sr, y - 30);
                y -= 60 + 20;
            }
            if (buy)
            {
                Place(p.buyWrap, y - 70); // tâm khung nút
                y -= 140 + 10;
            }
            if (p.freeRow.gameObject.activeSelf)
            {
                Place(p.freeRow, y);
                y -= 104 + 24;
            }
            p.sheet.sizeDelta = new Vector2(GroupW, -y);
            Place((RectTransform)p.mute.transform, y - 16);
        }

        // ---------- Hết bi ----------

        void ShowRefill(Popup pop)
        {
            until = 0;
            var packs = pop.first ? new List<ShopPack>() : Enumerable.Range(1, 3).Select(i => C.Pack("refill_" + i)).Where(x => x != null).ToList();
            if (packs.Count > 0)
            {
                ShowRefillGroup(pop, packs);
                return;
            }
            // Hết bi lần đầu (chỉ cách miễn phí; người dùng 2026-11-27: "đổi luôn popup Hết bi lần đầu theo style này"): nền tối phủ màn, đống
            // bi + băng "Hết bi!" + dòng phụ, mỗi cách một ô trơn hoa văn cao bằng nhau (quảng cáo nhận bi, Cây bi, Lọ Bi), nút trong dải đáy ô
            EnterGroupLook();
            p.bannerTitle.text = pop.warn ? Loc.T("Sắp hết bi!") : Loc.T("Hết bi!");
            Theme.SetSprite(p.packArt, ShopUi.Balls(3));
            p.packArt.preserveAspect = true;
            p.sub.text = pop.warn ? Loc.F("Còn {0} bi. Bổ sung để thả tiếp, lên cấp cho mọi tướng.", S.balls) : Loc.T("Bi để thả máy bi, lên cấp cho mọi tướng.");
            float contentH = FreeColumns();
            Mute(!pop.free);
            LayoutGroup(contentH + 30, true);
            HeadFx();
            alive = true;
            StartCoroutine(Intro());
        }

        // Hết bi có gói (người dùng 2026-11-27: "làm popup Hết bi theo kiểu cột cao dần luôn"): như nhóm chọn một gói; đầu là đống bi + băng
        // "Hết bi!" + dòng phụ; ô cột cao dần, hình gói (túi, giỏ, thùng bi) lớn dần theo bậc, ô số bi dưới hình; hàng nút miễn phí dưới
        void ShowRefillGroup(Popup pop, List<ShopPack> packs)
        {
            EnterGroupLook();
            p.bannerTitle.text = pop.warn ? Loc.T("Sắp hết bi!") : Loc.T("Hết bi!");
            Theme.SetSprite(p.packArt, ShopUi.Balls(3));
            p.packArt.preserveAspect = true;
            p.sub.text = pop.warn ? Loc.F("Còn {0} bi. Bổ sung để thả tiếp, lên cấp cho mọi tướng.", S.balls) : Loc.T("Bi để thả máy bi, lên cấp cho mọi tướng.");
            const float hMax = 720;
            RefillColumns(packs, hMax);
            FreeStrip();
            Mute(!pop.free);
            LayoutGroup(hMax + BadgeRoom, true);
            HeadFx();
            alive = true;
            StartCoroutine(Intro());
        }

        void RefillColumns(List<ShopPack> packs, float hMax)
        {
            int n = packs.Count;
            const float gap = 22, step = 80, top = 108, cs = 150, cellGap = 14;
            UseRow(gap);
            p.row.childAlignment = TextAnchor.LowerCenter;
            float w = Mathf.Min(330, (GroupW - 40 - (n - 1) * gap) / n);
            ShopHue[] hues = { ShopHue.Sky, ShopHue.Grape, ShopHue.Sunset };
            for (int i = 0; i < n; i++)
            {
                var pk = packs[i];
                var items = Shop.Resolve(S, D, pk.items, pk.scale, null);
                float hi = hMax - (n - 1 - i) * step;
                int m = Mathf.Max(1, items.Count);
                float art = Mathf.Max(90, hi - top - cellGap - m * cs - (m - 1) * cellGap - 16 - OfferPopColumn.FootH);
                var col = Ui.Spawn(columnPrefab, p.row.transform).Set("", hues[i % hues.Length], new Vector2(w, hi));
                col.Plain().Badge(ShopUi.ShownMult(pk), i % 2 == 0 ? -5 : 4);
                col.ArtAt(ShopUi.PackArt(pk.id) ?? ShopPage.ArtFor(items), top, new Vector2(Mathf.Min(w - 30, art), art));
                col.Fill(itemPrefab, items, 1, new Vector2(cs, cs), top + art + cellGap, OfferPopColumn.FootH, false);
                string id = pk.id;
                col.Button(ShopService.Price(pk.price), () => ShopService.BuyPack(id, AfterBuy));
                pops.Add(col.Rect);
                if (col.BadgeRect) badges.Add(col.BadgeRect);
            }
        }

        // lần hết bi đầu: chỉ cách miễn phí (quảng cáo, Cây bi, Lọ Bi), mỗi cách một ô
        float FreeColumns()
        {
            const float h = 540, gap = 22;
            UseRow(gap);
            p.row.childAlignment = TextAnchor.LowerCenter;
            var cols = new List<Action<OfferPopColumn, float>>();
            if (Ads.Ready && Ads.Left(Ads.FreeBalls) > 0)
                cols.Add((col, w) =>
                {
                    col.Set(Loc.T("MIỄN PHÍ"), ShopHue.Mint, new Vector2(w, h));
                    FillOne(col, ShopService.FreeBallsN, w, h);
                    col.Buy.gameObject.SetActive(true);
                    Ads.Bind(col.Buy, Loc.T("Xem"), Ads.FreeBalls);
                    col.Buy.SetColor(Theme.Blue);
                    col.Buy.SetOnClick(WatchAd);
                });
            int stock = Trees.Open(S, D.Cfg) > 0 ? Trees.Stock(S, D.Cfg, Now) : -1;
            if (stock >= 0)
                cols.Add((col, w) =>
                {
                    col.Set(Loc.T("CÂY BI"), ShopHue.Sky, new Vector2(w, h));
                    FillOne(col, stock, w, h);
                    if (stock > 0) col.Button(Loc.T("Tới Nhà"), GoHome);
                    else col.Done(Loc.T("Ra bi theo giờ"));
                });
            if (Shop.PiggyCanBreak(S, C, Now))
                cols.Add((col, w) =>
                {
                    var pk = C.Pack("piggy");
                    col.Set(Loc.T("LỌ BI"), ShopHue.Berry, new Vector2(w, h));
                    FillOne(col, (int)Math.Floor(Shop.Of(S).piggy), w, h);
                    col.Button(Loc.F("Đập lọ {0}", ShopService.Price(pk.price)), () => ShopService.BuyPack("piggy", AfterBuy));
                });
            if (cols.Count == 0)
                cols.Add((col, w) =>
                {
                    col.Set(Loc.T("THẮNG ẢI"), ShopHue.Slate, new Vector2(w, h));
                    col.Done(Loc.T("Thắng ải để có thêm bi"));
                });
            int n = cols.Count;
            float cw = Mathf.Min(320, (GroupW - 40 - (n - 1) * gap) / n);
            foreach (var make in cols)
            {
                var col = Ui.Spawn(columnPrefab, p.row.transform);
                make(col, cw);
                col.Plain();
                pops.Add(col.Rect);
            }
            return h;
        }

        void FillOne(OfferPopColumn col, int balls, float w, float h)
        {
            float cs = Mathf.Min(220, Mathf.Min(w - 70, h - OfferPopColumn.HeadH - OfferPopColumn.FootH - 20));
            col.Fill(itemPrefab, new List<ShopItem> { new ShopItem { k = "balls", n = Math.Max(0, balls) } }, 1, new Vector2(cs, cs),
                OfferPopColumn.HeadH + 10, OfferPopColumn.FootH, false);
        }

        // hàng nút miễn phí dưới 3 gói: xem quảng cáo nhận bi, Cây bi ở Nhà
        void FreeStrip()
        {
            bool ad = Ads.Ready && Ads.Left(Ads.FreeBalls) > 0;
            int stock = Trees.Open(S, D.Cfg) > 0 ? Trees.Stock(S, D.Cfg, Now) : 0;
            p.freeRow.gameObject.SetActive(ad || stock > 0);
            p.freeAd.gameObject.SetActive(ad);
            if (ad)
            {
                Ads.Bind(p.freeAd, Loc.F("Xem: +{0} bi", ShopService.FreeBallsN), Ads.FreeBalls);
                p.freeAd.SetColor(Theme.Blue);
                p.freeAd.SetOnClick(WatchAd);
            }
            p.freeHome.gameObject.SetActive(stock > 0);
            if (stock > 0)
            {
                p.freeHome.SetText(Loc.F("Cây bi {0}: Tới Nhà", stock));
                p.freeHome.SetOnClick(GoHome);
            }
        }

        void WatchAd() => ShopService.FreeBalls(() =>
        {
            if (this) Close();
        });

        void GoHome()
        {
            Close();
            App.Router.Go(SceneIds.Home);
        }

        // ---------- nút ----------

        void SetMute()
        {
            p.mute.SetText(muted ? Loc.T("Đã tắt tới mai") : Loc.T("Hôm nay không hiện nữa"));
            p.mute.SetRole(muted ? BtnColor.Green : BtnColor.Paper);
        }

        void AfterBuy(bool ok)
        {
            if (!ok || !this) return;
            bought = true;
            Close();
        }

        void UpdateTimer()
        {
            if (until <= 0) return;
            double left = until - Now;
            p.timer.text = left > 0 ? Loc.F("Còn {0}", ShopUi.Clock(left)) : Loc.T("Hết giờ");
            if (grouped && p.bigTimerText)
            {
                p.bigTimerText.text = p.timer.text;
                p.bigTimerBg.color = left < 3600000 ? Urgent : TimerRed;
            }
            if (left <= 0)
            {
                p.buy.Interactable = false;
                foreach (Transform c in p.row.transform)
                    if (c.TryGetComponent<OfferPopColumn>(out var col)) col.Buy.Interactable = false;
            }
        }

        // ---------- nhịp ----------

        IEnumerator Intro()
        {
            var art = p.packArt.rectTransform;
            art.localScale = Vector3.zero;
            p.value.localScale = Vector3.zero;
            foreach (var r in pops) r.localScale = Vector3.zero;
            foreach (var r in badges) r.localScale = Vector3.zero;
            p.buyWrap.localScale = Vector3.zero;
            yield return Wait(0.12f);
            StartCoroutine(Pop(art, 1.18f, 0.34f));
            App.Audio.Play("pick", 0.6f, 1.1f);
            for (int i = 0; i < pops.Count; i++)
            {
                yield return Wait(0.06f);
                if (pops[i]) StartCoroutine(Pop(pops[i], 1.1f, 0.26f));
            }
            yield return Wait(0.08f);
            // huy hiệu giá trị từng ô đập vào lần lượt (bậc sau mạnh hơn)
            for (int i = 0; i < badges.Count; i++)
            {
                if (!badges[i]) continue;
                yield return Pop(badges[i], 1.3f + 0.08f * i, 0.22f);
                App.Audio.Play("stamp", 0.7f + 0.1f * i, 1 + 0.06f * i);
                Haptics.Play(Haptic.UiTap);
            }
            if (p.value.gameObject.activeSelf)
            {
                // nhãn giá trị đập vào
                yield return Pop(p.value, 1.25f, 0.22f);
                App.Audio.Play("stamp", 0.8f);
                Haptics.Play(Haptic.UiTap);
            }
            if (p.buyWrap.gameObject.activeSelf) yield return Pop(p.buyWrap, 1.15f, 0.28f);
        }

        void Update()
        {
            if (!alive) return;
            float tt = Time.unscaledTime;
            // hình gói dập dềnh, nghiêng nhẹ
            var art = p.packArt.rectTransform;
            if (art.localScale.x > 0.99f && art.localScale.x < 1.01f)
            {
                art.anchoredPosition = new Vector2(art.anchoredPosition.x, packY0 + 9 * Mathf.Sin(tt * 2.1f));
                art.localEulerAngles = new Vector3(0, 0, 2.2f * Mathf.Sin(tt * 1.3f));
            }
            // nút giá thở 1,0 ↔ 1,06
            if (p.buyWrap.gameObject.activeSelf && p.buyWrap.localScale.x >= 0.999f || breathing)
            {
                breathing = true;
                float b = 0.5f - 0.5f * Mathf.Cos(tt * Mathf.PI * 2 / 1.2f);
                p.buyWrap.localScale = Vector3.one * (1 + 0.06f * b);
            }
            // đồng hồ to của nhóm chọn một: dưới 1 giờ thì phập phồng
            if (grouped && p.bigTimer && p.bigTimer.gameObject.activeSelf)
            {
                bool urgent = until > 0 && until - Now < 3600000;
                float k = urgent ? 1 + 0.05f * (0.5f - 0.5f * Mathf.Cos(tt * Mathf.PI * 2 / 0.8f)) : 1;
                p.bigTimer.localScale = new Vector3(k, k, 1);
            }
            timerTick -= Time.unscaledDeltaTime;
            if (timerTick <= 0)
            {
                timerTick = 0.5f;
                UpdateTimer();
            }
        }

        static IEnumerator Pop(RectTransform rt, float peak, float d)
        {
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                if (!rt) yield break;
                float k = t / d;
                rt.localScale = Vector3.one * (k < 0.6f ? Mathf.Lerp(0, peak, 1 - Mathf.Pow(1 - k / 0.6f, 2)) : Mathf.Lerp(peak, 1, (k - 0.6f) / 0.4f));
                yield return null;
            }
            if (rt) rt.localScale = Vector3.one;
        }

        static IEnumerator Wait(float s)
        {
            for (float t = 0; t < s; t += Time.unscaledDeltaTime) yield return null;
        }
    }
}
