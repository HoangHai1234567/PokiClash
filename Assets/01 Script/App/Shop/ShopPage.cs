// Màn cửa hàng toàn màn hình (người dùng 2026-11-23: "bố cục shop nhìn xấu quá, học tập clash of critters"; GD_Claude/26 mục 13). Prefab
// Assets/04 Prefabs/Dialogs/CuaHangLon (biến thể tờ giấy gốc HopThoai trải kín màn, menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết").
// Một trang cuộn dài chia mục như cửa hàng của Clash of Critters, hàng nút mục trên cùng nhảy tới mục (chấm đỏ khi có quà chờ):
//   Ưu đãi (thẻ ngang to: ưu đãi hẹn giờ, Chuỗi Quà, Lọ Bi) · Miễn phí (quà hôm nay, quà thẻ / gói theo ngày, bi và trứng xem quảng cáo,
//   mốc quảng cáo) · Trứng (túi trứng chờ nở, lưới trứng theo bậc, gói ×10, gói tướng tuần, vé, tỉ lệ) · Bi (lưới 6 gói bi có hình
//   riêng, "Lần đầu ×2") · Đặc quyền (Thẻ Tuần, Thẻ Phiêu Lưu, Quỹ, Bỏ quảng cáo; khôi phục giao dịch).
// Popup ưu đãi, trang con (quỹ, chuỗi, vé) vẫn là tờ giấy ShopSheet mở chồng lên.
// Bản 3 (người dùng 2026-11-27: "thiết kế shop như clash of critters, nền tối, các gói IAP màu tươi nổi"; GD_Claude/26 mục 15): nền tối caro,
// cột mục dọc bên trái (hình gói + tên, mục đang xem có ô tím → lam), băng tím tiêu đề mục, thẻ / ô màu tươi (ShopHue), nút giá xanh lá.
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
    public sealed class ShopPage : Dialog
    {
        [Serializable]
        public struct Parts
        {
            public TextMeshProUGUI title, balls;
            public SketchButton[] nav; // cột mục trái, theo Sections (nền nút là ô chọn: hiện ở mục đang xem)
            public GameObject[] navDots;
            public ScrollRect scroll;
            public RectTransform content;
            public RectTransform safe; // khung an_toan (SafeArea) chứa chữ và nút; tờ giấy trải kín màn (2026-11-24)
        }

        [SerializeField] Parts p;
        [SerializeField] ShopSection sectionPrefab;
        [SerializeField] ShopGrid gridPrefab;
        [SerializeField] ShopTile tilePrefab;
        [SerializeField] ShopCard cardPrefab;

        public static readonly string[] Sections = { "offers", "free", "eggs", "balls", "perks" };
        public static readonly string[] NavNames = { "Ưu đãi", "Miễn phí", "Trứng", "Bi", "Đặc quyền" };

        // bề rộng cột mục trái và trang cuộn bên phải (màn 1080): 190 + 14 + 858 + 18
        public const float SideW = 190, ContentW = 858;

        readonly Dictionary<string, RectTransform> anchors = new Dictionary<string, RectTransform>();
        string jumpTo;
        int shownBalls = -1;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static ShopConfig C => App.Data.Cfg.shop;
        static double Now => SaveService.Now();
        static Rng R => new Rng(Rng.RandomSeed());

        public static ShopPage Current { get; private set; }

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, ShopSection section, ShopGrid grid, ShopTile tile, ShopCard card)
        {
            p = parts;
            sectionPrefab = section;
            gridPrefab = grid;
            tilePrefab = tile;
            cardPrefab = card;
        }

        void OnDestroy()
        {
            if (Current == this) Current = null;
        }

        // tờ trải kín màn: nút đóng (con của tờ giấy, ModalService gắn) dời xuống bằng phần tai thỏ mà khung an_toan đã chừa
        void Start()
        {
            if (!p.safe || !(p.safe.parent is RectTransform page)) return;
            var close = (RectTransform)GetComponent<ModalSheet>().Close.transform;
            close.anchoredPosition += new Vector2(0, -(1 - p.safe.anchorMax.y) * page.rect.height);
        }

        // ---------- mở ----------

        // section: offers, free, eggs, balls, perks (tab cũ "heroes" = eggs)
        public static ShopPage Open(string section = null)
        {
            if (Current) Current.Modal?.Close();
            var s = App.Modals.Open<ShopPage>();
            Current = s;
            Offers.EnsureStarter(S, D, Now);
            s.jumpTo = section == "heroes" ? "eggs" : section ?? "offers"; // mở không chỉ mục: về đầu trang
            s.Nav();
            s.Redraw();
            ShopLog.Event("shop_open", section ?? "offers", 0);
            return s;
        }

        public void Redraw()
        {
            if (!this) return;
            float keep = p.scroll.verticalNormalizedPosition;
            for (int i = p.content.childCount - 1; i >= 0; i--) Destroy(p.content.GetChild(i).gameObject);
            anchors.Clear();
            DrawOffers();
            DrawFree();
            DrawEggs();
            DrawBalls();
            DrawPerks();
            Canvas.ForceUpdateCanvases();
            LayoutRebuilder.ForceRebuildLayoutImmediate(p.content);
            if (jumpTo != null)
            {
                Jump(jumpTo);
                jumpTo = null;
            }
            else p.scroll.verticalNormalizedPosition = keep;
            Dots();
        }

        // ---------- khung ----------

        void Nav()
        {
            p.title.text = Loc.T("Cửa hàng");
            for (int i = 0; i < p.nav.Length && i < Sections.Length; i++)
            {
                string id = Sections[i];
                p.nav[i].Label.text = Loc.T(NavNames[i]); // chữ thường như thẻ mẫu (SetText viết hoa)
                p.nav[i].SetOnClick(() => Jump(id));
            }
        }

        void Jump(string id)
        {
            if (!anchors.TryGetValue(id, out var a) || !a) return;
            Canvas.ForceUpdateCanvases();
            float viewH = p.scroll.viewport.rect.height, contentH = p.content.rect.height;
            float y = Mathf.Clamp(-a.anchoredPosition.y - a.rect.height * (1 - a.pivot.y) - 8, 0, Mathf.Max(0, contentH - viewH));
            p.content.anchoredPosition = new Vector2(p.content.anchoredPosition.x, y);
            p.scroll.velocity = Vector2.zero;
        }

        void Dots()
        {
            var st = Shop.Of(S);
            bool[] on =
            {
                false,
                Offers.AnyClaim(S, D, Now) || Enumerable.Range(0, C.adMilestones.Count).Any(i => Shop.AdMilestoneReady(S, C, i, Now)),
                Eggs.BagTotal(S) + st.tickets.Count + st.Item(Shop.TicketWeek) > 0,
                false,
                Shop.FundReady(S, C) > 0 && st.fund,
            };
            for (int i = 0; i < p.navDots.Length && i < on.Length; i++)
                if (p.navDots[i]) p.navDots[i].SetActive(on[i]);
        }

        void Update()
        {
            if (S == null || S.balls == shownBalls) return;
            shownBalls = S.balls;
            p.balls.text = NumFmt.Short(S.balls);
        }

        void LateUpdate()
        {
            // mục đang xem (ô chọn tím → lam hiện sau nút): mục cuối cùng có đầu đã lên tới mép trên khung
            if (Time.frameCount % 10 != 0) return;
            float top = p.content.anchoredPosition.y;
            string cur = "offers";
            foreach (var id in Sections)
                if (anchors.TryGetValue(id, out var a) && a && -a.anchoredPosition.y - a.rect.height <= top + 40) cur = id;
            // cuộn chạm đáy (mục cuối ngắn hơn khung, đầu mục không lên tới mép trên): chọn mục cuối
            if (p.content.rect.height > p.scroll.viewport.rect.height && p.scroll.verticalNormalizedPosition <= 0.002f) cur = Sections[Sections.Length - 1];
            for (int i = 0; i < p.nav.Length && i < Sections.Length; i++)
                p.nav[i].SetColor(Sections[i] == cur ? Color.white : new Color(1, 1, 1, 0));
        }

        // ---------- dựng ----------

        void Section(string id, string title, double until = 0)
        {
            var s = Ui.Spawn(sectionPrefab, p.content).Set(title, until);
            s.name = "muc_" + id;
            if (id != null && !anchors.ContainsKey(id)) anchors[id] = (RectTransform)s.transform;
        }

        ShopGrid Grid(int cols, float h) => Ui.Spawn(gridPrefab, p.content).Set(cols, h);
        ShopTile Tile(ShopGrid g, string title, string sub, ShopHue bg) => Ui.Spawn(tilePrefab, g.Rect).Set(title, sub, bg);
        ShopCard Card(string title, string desc, ShopHue bg) => Ui.Spawn(cardPrefab, p.content).Set(title, desc, bg);

        // hình to cho một gói: trứng bậc cao nhất trong gói, không có thì đống bi theo số, không nữa thì vé / đá / icon (hình bản 2 nếu có)
        public static Sprite ArtFor(List<ShopItem> items)
        {
            var egg = items.Where(i => i.k == Shop.Egg).OrderByDescending(i => i.r).FirstOrDefault();
            if (egg != null) return ShopUi.Egg(egg.r);
            var balls = items.FirstOrDefault(i => i.k == "balls");
            if (balls != null) return BallArt(balls.n);
            if (items.Any(i => i.k == Shop.Ticket || i.k == Shop.TicketWeek)) return App.Art.HasArt("goi2_ve") ? App.Art.Get("goi2_ve") : App.Art.Icon("team");
            var evo = items.FirstOrDefault(i => i.k == "evo");
            if (evo != null) return App.Art.HasArt("goi2_da_nho") ? App.Art.Get(evo.n >= 10 ? "goi2_da_lon" : "goi2_da_nho") : App.Art.Icon("potion");
            return App.Art.Icon("star");
        }

        // hình riêng của gói nếu có (Assets/03 Art/Shop/v2), không thì theo món
        static Sprite ArtFor(ShopPack pk, List<ShopItem> items) => (pk != null ? ShopUi.PackArt(pk.id) : null) ?? ArtFor(items);

        // đống bi theo số bi (6 hình như 6 gói bi: nắm, túi, rổ, thùng, rương, xe); số bi gói nhân theo bậc cấp nên quy về bậc 1 trước
        public static Sprite BallArt(int n)
        {
            double b = n / Math.Max(1, C.Band(S.level));
            int[] steps = { 0, 300, 900, 2000, 5000, 11000 };
            int k = 1;
            for (int i = 0; i < steps.Length; i++)
                if (b >= steps[i]) k = i + 1;
            return ShopUi.Balls(k);
        }

        static ShopHue OfferColor(ActiveOffer o) => ShopHue.Offer(o);

        void DrawOffers()
        {
            var live = Shop.Live(S, Now).OrderBy(o => o.until <= 0 ? double.MaxValue : o.until).ToList();
            bool chain = Shop.ChainLive(S, Now), piggy = Shop.PiggyOpen(S);
            Section("offers", Loc.T("Ưu đãi"));
            if (live.Count == 0 && !chain && !piggy)
            {
                Card(Loc.T("Chưa có ưu đãi mới"), Loc.T("Ưu đãi hẹn giờ hiện ở đây khi có. Ghé lại sau nhé!"), ShopHue.Slate).Compact();
                return;
            }
            foreach (var o in live) OfferCard(o);
            if (chain) ChainCard();
            if (piggy) PiggyCard();
        }

        void OfferCard(ActiveOffer o)
        {
            var pk = o.pack != null ? C.Pack(o.pack) : null;
            var items = Shop.OfferItems(S, D, o);
            string desc = pk != null && pk.kind == "days" ? Loc.T("Mua một lần, nhận 3 ngày liền (vào game mỗi ngày để nhận).") : pk?.Desc;
            var c = Card(ShopService.OfferName(o), desc, OfferColor(o)).Items(items).Value(ShopUi.ShownMult(o)).Timer(o.until);
            // gói có hình riêng (Quà Nhập Môn, Khởi Hành...) dùng hình đó; gói tướng (Vượt Mốc, Tiếp Sức) giữ mặt tướng; còn lại icon loại ưu
            // đãi (Ưu Đãi Nóng, Đảo Mới, Trở Lại...), chưa có thì hình theo món
            var hero = items.FirstOrDefault(i => i.k == "shards")?.h;
            var own = pk != null ? ShopUi.PackArt(pk.id) : null;
            var kind = ShopUi.OfferArt(o) ?? ArtFor(items);
            if (own) c.Art(own);
            else if (hero != null && D.Hero(hero) != null) c.Hero(D.Hero(hero), kind);
            else c.Art(kind);
            if (o.bought) c.Done(Loc.T("Đã mua"));
            else c.Button(ShopService.Price(pk?.price ?? o.price), BtnColor.Orange, () => ShopService.BuyOffer(o.uid, ok => After(ok)));
        }

        void ChainCard()
        {
            var def = Shop.ChainNow(S, C);
            var st = Shop.Of(S);
            if (def == null) return;
            var next = st.chainStep < def.steps.Count ? Shop.Resolve(S, D, def.steps[st.chainStep].items, true, null) : new List<ShopItem>();
            Card(Loc.F("Chuỗi Quà: {0}", def.Name), Loc.F("Đã mở {0}/{1} ô. Ô miễn phí xen giữa các ô trả tiền.", st.chainStep, def.steps.Count), ShopHue.Grape)
                .Art(ShopUi.TplArt("chain") ?? ArtFor(next)).Items(next).Timer(st.chainUntil)
                .Button(Loc.T("Xem"), BtnColor.Green, ShopSheet.OpenChain);
        }

        void PiggyCard()
        {
            var st = Shop.Of(S);
            int n = (int)Math.Floor(st.piggy);
            double cap = Shop.PiggyCap(S, C);
            var pk = C.Pack("piggy");
            var c = Card(Loc.T("Lọ Bi"), Loc.F("Lọ đang có {0}/{1} bi. Mỗi bi bạn thả bỏ 1 bi vào lọ.", n, cap), ShopHue.Gold)
                .Art(ShopUi.PackArt("piggy") ?? ShopUi.Balls(2)).Value(pk.price > 0 ? n / (pk.price * C.valuePerUsd) : 0);
            if (Shop.PiggyCanBreak(S, C, Now)) c.Button(Loc.F("Đập lọ {0}", ShopService.Price(pk.price)), BtnColor.Orange, () => ShopService.BuyPack("piggy", ok => After(ok)));
            else if (Shop.PiggyWait(S, C, Now) > 0) c.Note(Loc.F("Lọ vừa đập. Đập lại được sau {0}.", ShopUi.Clock(Shop.PiggyWait(S, C, Now))));
            else c.Note(Loc.F("Đủ {0} bi mới đập được.", Math.Ceiling(cap * C.piggy.minPct)));
        }

        void DrawFree()
        {
            Section("free", Loc.T("Quà miễn phí"));
            // quà hôm nay: thẻ ngang; bấm mở màn nhận quà nền đen (DailyGiftView: ×2 quảng cáo trước, nhận thường sau). Chưa dựng prefab
            // màn đó thì hai nút Nhận / Nhận ×2 như cũ
            var gift = Shop.Resolve(S, D, C.dailyGift, true, null);
            var g = Card(Loc.T("Quà hôm nay"), Loc.T("Mỗi ngày một phần quà miễn phí."), ShopHue.Mint).Art(ArtFor(gift)).Items(gift);
            if (!Shop.GiftReady(S, Now)) g.Done(Loc.T("Đã nhận, mai quay lại"));
            else if (Theme.Prefabs && Theme.Prefabs.dailyGift) g.Button(Loc.T("Mở quà"), BtnColor.Green, () => DailyGiftView.Open(Redraw));
            else
            {
                g.Button(Loc.T("Nhận"), BtnColor.Green, () => ShopService.Gift(false, Redraw));
                g.AdExtra(Loc.T("Nhận ×2"), Ads.DailyGiftAd, () => ShopService.Gift(true, Redraw));
            }
            // quà thẻ / gói theo ngày đang chờ
            foreach (var id in new[] { "week", "month" })
            {
                if (!Shop.CardClaimable(S, id, Now)) continue;
                var def = C.Card(id);
                var items = Shop.Resolve(S, D, def.daily, true, null);
                Card(Loc.F("{0}: quà ngày", def.Name), Loc.F("Còn {0}.", ShopUi.Clock(Shop.CardUntil(S, id) - Now)), ShopHue.Sky).Art(ArtFor(items)).Items(items)
                    .Button(Loc.T("Nhận"), BtnColor.Green, () => ShopService.Free(Shop.ClaimCard(S, D, id, Now, R), def.Name, _ => Redraw()));
            }
            if (S.shop != null)
                foreach (var kv in S.shop.days.ToList())
                {
                    var pk = C.Pack(kv.Key);
                    if (pk == null || !Shop.DayClaimable(S, D, kv.Key, Now)) continue;
                    var items = Shop.Resolve(S, D, pk.days[kv.Value.claimed].items, pk.scale, null);
                    Card(Loc.F("{0}: ngày {1}", pk.Name, kv.Value.claimed + 1), null, ShopHue.Berry).Art(ArtFor(items)).Items(items)
                        .Button(Loc.T("Nhận"), BtnColor.Green, () => ShopService.Free(Shop.ClaimDay(S, D, kv.Key, Now, R), pk.Name, _ => Redraw()));
                }
            // bi, trứng xem quảng cáo, mốc quảng cáo hôm nay
            var grid = Grid(3, 430);
            Tile(grid, Loc.F("+{0} bi", ShopService.FreeBallsN), Loc.T("Bi miễn phí"), ShopHue.Sky).Art(ShopUi.Balls(1))
                .Ribbon(Loc.T("Miễn phí"), Theme.Green).AdButton(Loc.T("Xem"), Ads.FreeBalls, () => ShopService.FreeBalls(Redraw));
            Tile(grid, ShopUi.EggName(0), Loc.T("1 lần mỗi ngày"), ShopHue.Tier(0)).Art(ShopUi.Egg(0))
                .Ribbon(Loc.T("Miễn phí"), Theme.Green).AdButton(Loc.T("Nở"), Ads.FreeEgg, () => ShopService.FreeEgg(Redraw));
            int seen = Shop.AdsToday(S, Now);
            for (int i = 0; i < C.adMilestones.Count; i++)
            {
                var m = C.adMilestones[i];
                int k = i;
                var items = Shop.Resolve(S, D, m.items, true, null);
                var t = Tile(grid, Loc.F("Xem {0} quảng cáo", m.n), Loc.F("Hôm nay {0}/{1}", Math.Min(seen, m.n), m.n), ShopHue.Gold).Art(ArtFor(items), Count(items));
                if (Shop.Of(S).adClaimed.Contains(i)) t.Done(Loc.T("Đã nhận"));
                else t.Button(Loc.T("Nhận"), BtnColor.Green, () => ShopService.Free(Shop.ClaimAdMilestone(S, D, k, Now, R), Loc.T("Mốc quảng cáo"), _ => Redraw()),
                    Shop.AdMilestoneReady(S, C, i, Now)).Dot(Shop.AdMilestoneReady(S, C, i, Now));
            }
        }

        // số ghi góc hình: "×N" của món chính
        static string Count(List<ShopItem> items)
        {
            var main = items.OrderByDescending(i => i.k == Shop.Egg ? 2 : i.k == "balls" ? 1 : 0).FirstOrDefault();
            return main == null || main.n <= 1 ? null : "×" + NumFmt.Short(main.n);
        }

        void DrawEggs()
        {
            var st = Shop.Of(S);
            Section("eggs", Loc.T("Trứng tướng"));
            // túi trứng chờ nở
            var bag = Enumerable.Range(0, Eggs.Tiers).Where(t => Eggs.Bag(S, t) > 0).ToList();
            if (bag.Count > 0)
            {
                var bg = Grid(3, 430);
                foreach (int t in bag)
                {
                    int n = Eggs.Bag(S, t), tier = t;
                    Tile(bg, ShopUi.EggName(t), Loc.F("Nở {0}–{1} mảnh", C.Egg(t)?.min ?? 12, C.Egg(t)?.max ?? 16), ShopHue.Tier(t)).Art(ShopUi.Egg(t), "×" + n)
                        .Ribbon(Loc.T("Trong túi"), Theme.GreenD).Dot(true)
                        .Button(n > 1 ? Loc.F("Nở {0}", Math.Min(10, n)) : Loc.T("Nở"), BtnColor.Green, () => ShopService.HatchEggs(tier, Math.Min(10, n), Redraw));
                }
            }
            // lưới trứng bán: Trứng Hiếm hôm nay, mỗi bậc một quả, gói ×10
            var grid = Grid(3, 430);
            foreach (var pk in C.packs.Where(x => x.tab == "eggs" && x.items.Count == 1 && x.items[0].k == Shop.Egg).OrderBy(x => x.sort))
            {
                var it = pk.items[0];
                var t = Tile(grid, pk.Name, Loc.F("Nở {0}–{1} mảnh", C.Egg(it.r)?.min ?? 12, C.Egg(it.r)?.max ?? 16), ShopHue.Tier(it.r)).Value(ShopUi.ShownMult(pk));
                if (it.n > 1) t.Stack(ShopUi.Egg(it.r), 3, "×" + it.n);
                else t.Art(ShopUi.Egg(it.r));
                if (pk.daily) t.Ribbon(Loc.T("Hôm nay"), Theme.Red);
                else if (pk.id == "egg_2x10") t.Ribbon(Loc.T("Bán chạy"), Theme.Orange);
                PackButton(t, pk);
            }
            // gói tướng tuần, vé, tỉ lệ
            foreach (var pk in C.packs.Where(x => x.tab == "eggs" && !(x.items.Count == 1 && x.items[0].k == Shop.Egg)).OrderBy(x => x.sort))
            {
                var items = Shop.Resolve(S, D, pk.items, pk.scale, null);
                var feat = Shop.FeaturedNow(D, Now);
                string desc = pk.weekly && pk.items.Any(i => i.k == Shop.TicketWeek)
                    ? Loc.F("{0} Tướng tuần: {1}.", pk.Desc, string.Join(", ", feat.Select(h => D.Hero(h)?.name))) : pk.Desc;
                var c = Card(pk.Name, desc, ShopHue.Grape).Items(items).Value(ShopUi.ShownMult(pk));
                // gói tướng tuần: mặt tướng tuần (cho biết tướng nào ra nhiều); gói đá, vé: hình riêng bản 2
                bool weeklyHero = pk.weekly && pk.items.Any(i => i.k == Shop.TicketWeek);
                if (weeklyHero && feat.Count > 0 && D.Hero(feat[0]) != null) c.Hero(D.Hero(feat[0]), ArtFor(pk, items));
                else c.Art(ArtFor(pk, items));
                int left = Shop.Left(S, pk, Now);
                if (left <= 0) c.Done(pk.weekly ? Loc.T("Tuần sau mua tiếp") : Loc.T("Đã mua"));
                else c.Button(ShopService.Price(pk.price), BtnColor.Orange, () => ShopService.BuyPack(pk.id, ok => After(ok)));
            }
            if (st.tickets.Count > 0)
                Card(Loc.T("Vé chọn tướng"), Loc.F("Bạn có {0} vé: chọn 1 trong 6 tướng gợi ý, nhận đủ mảnh mở khoá.", st.tickets.Count), ShopHue.Sky)
                    .Art(ShopUi.PackArt("ticket_rare") ?? App.Art.Icon("team")).Compact().Button(Loc.T("Dùng vé"), BtnColor.Green, () => ShopSheet.OpenTicket(false, 0));
            if (st.Item(Shop.TicketWeek) > 0)
                Card(Loc.T("Vé tướng tuần"), Loc.F("Bạn có {0} vé: chọn 1 trong 2 tướng tuần.", st.Item(Shop.TicketWeek)), ShopHue.Sky)
                    .Art(App.Art.Icon("star")).Compact().Button(Loc.T("Dùng vé"), BtnColor.Green, () => ShopSheet.OpenTicket(true, 0));
            var names = Shop.FeaturedNow(D, Now).Select(h => D.Hero(h)?.name).Where(x => x != null);
            Card(Loc.T("Tỉ lệ trứng"), Loc.F("Trứng bậc nào nở mảnh tướng bậc đó. Tướng tuần (ra nhiều hơn): {0}.", string.Join(", ", names)), ShopHue.Slate)
                .Art(ShopUi.Egg(2)).Compact().Button(Loc.T("Tỉ lệ"), BtnColor.Paper, () => App.Modals.Alert(Loc.T("Tỉ lệ trứng"), Eggs.OddsText(D, Now)));
        }

        void DrawBalls()
        {
            Section("balls", Loc.T("Bi"));
            var grid = Grid(3, 430);
            int k = 0;
            foreach (var pk in C.packs.Where(x => x.tab == "balls").OrderBy(x => x.sort))
            {
                var items = Shop.Resolve(S, D, pk.items, pk.scale, null);
                int n = items.Where(i => i.k == "balls").Sum(i => i.n);
                bool first = Shop.FirstBonus(S, pk);
                // hình theo thứ tự gói (nắm, túi, rổ, thùng, rương, xe: trùng tên gói)
                var art = ShopUi.Balls(Math.Min(6, ++k));
                var t = Tile(grid, Loc.F("{0} bi", NumFmt.Short(n)), pk.Name, ShopHue.Sky).Art(art).Value(ShopUi.ShownMult(pk));
                if (first) t.Ribbon(Loc.T("Lần đầu ×2"), Theme.Red);
                PackButton(t, pk);
            }
        }

        void DrawPerks()
        {
            Section("perks", Loc.T("Đặc quyền"));
            var grid = Grid(2, 470);
            foreach (var pk in C.packs.Where(x => x.tab == "perks").OrderBy(x => x.sort))
            {
                // hình riêng bản 2 (lịch 7 ngày, sổ phiêu lưu, bậc quỹ, TV ngủ); chưa có thì icon cũ thu nhỏ
                string icon = pk.kind == "card" ? (Shop.CardOf(C, pk)?.id == "month" ? "crown" : "clock") : pk.kind == "fund" ? "coin" : pk.kind == "noads" ? "tv" : "star";
                var own = ShopUi.PackArt(pk.id);
                var t = Tile(grid, pk.Name, Short(pk.Desc), pk.kind == "fund" ? ShopHue.Gold : pk.kind == "noads" ? ShopHue.Grape : ShopHue.Sky)
                    .Art(own ? own : App.Art.Icon(icon), null, own ? 1f : 0.62f)
                    .Value(ShopUi.ShownMult(pk));
                if (pk.kind == "card")
                {
                    var card = Shop.CardOf(C, pk);
                    string id = card?.id ?? "week";
                    bool on = Shop.CardActive(S, id, Now);
                    if (on) t.Ribbon(Loc.F("Còn {0}", ShopUi.Clock(Shop.CardUntil(S, id) - Now)), Theme.GreenD);
                    if (Shop.CardClaimable(S, id, Now))
                        t.Button(Loc.T("Quà ngày"), BtnColor.Green, () => ShopService.Free(Shop.ClaimCard(S, D, id, Now, R), pk.Name, _ => Redraw())).Dot(true);
                    else t.Button(on ? Loc.F("Gia hạn {0}", ShopService.Price(pk.price)) : ShopService.Price(pk.price), BtnColor.Orange,
                        () => ShopService.BuyPack(pk.id, ok => After(ok)));
                }
                else if (pk.kind == "fund")
                {
                    int ready = Shop.FundReady(S, C);
                    if (ready > 0 && Shop.Of(S).fund) t.Ribbon(Loc.F("{0} mốc chờ nhận", ready), Theme.Red).Dot(true);
                    t.Button(Shop.Of(S).fund ? Loc.T("Xem quỹ") : ShopService.Price(pk.price), Shop.Of(S).fund ? BtnColor.Green : BtnColor.Orange, ShopSheet.OpenFund);
                }
                else PackButton(t, pk);
            }
            Card(Loc.T("Khôi phục giao dịch"), Loc.T("Đổi máy hay cài lại game: lấy lại gói mua một lần (Bỏ quảng cáo)."), ShopHue.Slate).Compact()
                .Button(Loc.T("Khôi phục"), BtnColor.Paper, () =>
                    App.Toasts.Show(Store.Ready ? Loc.T("Đã kiểm tra giao dịch") : Loc.T("Cửa hàng chưa sẵn sàng"), App.Art.Icon("check")));
        }

        // mô tả ngắn trong ô (câu đầu)
        static string Short(string s)
        {
            if (string.IsNullOrEmpty(s)) return s;
            int i = s.IndexOf(';');
            if (i < 0) i = s.IndexOf('.');
            return i > 0 && i < s.Length - 1 ? s.Substring(0, i) + "…" : s;
        }

        void PackButton(ShopTile t, ShopPack pk)
        {
            int left = Shop.Left(S, pk, Now);
            if (pk.kind == "noads" && AdGate.NoAds(S) || left <= 0)
            {
                t.Done(pk.daily ? Loc.T("Mai mua tiếp") : pk.weekly ? Loc.T("Tuần sau mua tiếp") : Loc.T("Đã mua"));
                return;
            }
            t.Button(ShopService.Price(pk.price), BtnColor.Orange, () => ShopService.BuyPack(pk.id, ok => After(ok)));
        }

        void After(bool ok)
        {
            if (ok) Redraw();
        }
    }
}
