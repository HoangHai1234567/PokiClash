// Tờ popup ưu đãi (prefab Assets/04 Prefabs/Dialogs/CuaHang, biến thể tờ giấy gốc HopThoai; menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết"):
// mọi popup (ưu đãi hẹn giờ, Hết bi, Lọ Bi, Chuỗi Quà, quà hôm nay, Quà Trở Lại, giới thiệu thẻ / quỹ) và các trang con (quỹ, chuỗi,
// chọn tướng bằng vé): tiêu đề, dòng phụ, danh sách ô gói cuộn dọc (Items/OGoi), ô "Hôm nay không hiện nữa" (popup bán).
// Cửa hàng chính là màn toàn màn hình ShopPage (2026-11-23); hàng tab của tờ này không dùng nữa. GD_Claude/26 mục 5–7, 13.
// Bản 3 (2026-11-27, người dùng: "làm popup và trang con cùng tông màu này luôn"; mục 17): tờ tối viền mực, băng tím tiêu đề vàng, ô gói
// màu tươi theo loại (ShopHue). Popup bán (offer, comeback, refill) là OfferPopup (phiên khác làm).
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
    public sealed class ShopSheet : Dialog
    {
        [Serializable]
        public struct Parts
        {
            public TextMeshProUGUI title, sub;
            public RectTransform tabRow;
            public SketchButton[] tabs; // offers, balls, heroes, perks
            public GameObject[] dots;
            public ScrollRect scroll;
            public RectTransform list;
            public LayoutElement scrollLayout;
            public SketchButton mute;
        }

        [SerializeField] Parts p;
        [SerializeField] PackCell cellPrefab;
        [SerializeField] float maxListH = 1240;

        public static readonly string[] TabIds = { "offers", "balls", "eggs", "perks" };

        Action redraw;
        bool muted, bought;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static ShopConfig C => App.Data.Cfg.shop;
        static double Now => SaveService.Now();
        static Rng R => new Rng(Rng.RandomSeed());

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, PackCell cell)
        {
            p = parts;
            cellPrefab = cell;
        }

        public static ShopSheet Current { get; private set; }

        void OnDestroy()
        {
            if (Current == this) Current = null;
        }

        // ---------- mở ----------

        // cửa hàng chính: màn toàn màn hình (tabId: offers, free, eggs, balls, perks; "heroes" cũ = eggs)
        public static void OpenShop(string tabId = "offers") => ShopPage.Open(tabId);

        // popup ưu đãi; closed(đã mua, tích "Hôm nay không hiện nữa")
        // popup bán (offer, comeback) dùng popup kiểu mới OfferPopup (học Clash of Critters, 2026-11-27) khi đã dựng prefab: trả null
        public static ShopSheet OpenPopup(Popup pop, Action<bool, bool> closed)
        {
            if (OfferPopup.Handles(pop))
            {
                OfferPopup.Open(pop, closed);
                return null;
            }
            ShopSheet s = null;
            s = App.Modals.Open<ShopSheet>(() => closed?.Invoke(s != null && s.bought, s != null && s.muted));
            s.Popup(pop);
            return s;
        }

        // trang con mở chồng lên tờ đang mở (quỹ, chọn tướng, chuỗi)
        static ShopSheet Sub(Action<ShopSheet> draw)
        {
            var s = App.Modals.Open<ShopSheet>(() =>
            {
                Current?.Redraw();
                ShopPage.Current?.Redraw();
            });
            s.Tabs(false);
            s.Mute(false);
            s.redraw = () => draw(s);
            s.Redraw();
            return s;
        }

        public void Redraw()
        {
            if (!this) return;
            Clear();
            redraw?.Invoke();
            FitList();
        }

        // ---------- khung ----------

        void Header(string title, string sub)
        {
            p.title.text = title;
            p.sub.text = sub ?? "";
            p.sub.gameObject.SetActive(!string.IsNullOrEmpty(sub));
        }

        void Tabs(bool on) => p.tabRow.gameObject.SetActive(on);

        void Mute(bool on)
        {
            p.mute.gameObject.SetActive(on);
            if (!on) return;
            SetMuteText();
            p.mute.SetOnClick(() =>
            {
                muted = !muted;
                SetMuteText();
            });
        }

        // phông không có ô tích: đã tích thì nút xanh, chữ đổi (GD_Claude/26 mục 7.7)
        void SetMuteText()
        {
            p.mute.SetText(muted ? Loc.T("Đã tắt tới mai") : Loc.T("Hôm nay không hiện nữa"));
            p.mute.SetRole(muted ? BtnColor.Green : BtnColor.Paper);
        }

        void Clear()
        {
            for (int i = p.list.childCount - 1; i >= 0; i--) Destroy(p.list.GetChild(i).gameObject);
        }

        PackCell Cell(string title, string desc = null) => Ui.Spawn(cellPrefab, p.list).Set(title, desc);
        PackCell Cell(string title, string desc, ShopHue hue) => Ui.Spawn(cellPrefab, p.list).Set(title, desc, hue);

        // màu ô gói theo loại: bi trời, trứng nho, quỹ vàng, thẻ trời, bỏ quảng cáo nho, còn lại cam hồng
        static ShopHue PackHue(ShopPack pk) =>
            pk.tab == "balls" ? ShopHue.Sky : pk.tab == "eggs" ? ShopHue.Grape : pk.kind == "fund" ? ShopHue.Gold : pk.kind == "card" ? ShopHue.Sky :
            pk.kind == "noads" ? ShopHue.Grape : ShopHue.Sunset;

        void FitList()
        {
            Canvas.ForceUpdateCanvases();
            LayoutRebuilder.ForceRebuildLayoutImmediate(p.list);
            float h = LayoutUtility.GetPreferredHeight(p.list);
            p.scrollLayout.preferredHeight = Mathf.Clamp(h, 200, maxListH);
            p.scroll.verticalNormalizedPosition = 1;
        }

        // ---------- các loại ô ----------

        void GiftCell()
        {
            var items = Shop.Resolve(S, D, C.dailyGift, true, null);
            var c = Cell(Loc.T("Quà hôm nay"), Loc.T("Mỗi ngày một phần quà miễn phí."), ShopHue.Mint).Items(items);
            if (!Shop.GiftReady(S, Now))
            {
                c.Done(Loc.T("Đã nhận, mai quay lại"));
                return;
            }
            c.Button(Loc.T("Nhận"), BtnColor.Green, () => ShopService.Gift(false, Redraw));
            c.AdButton(Loc.T("Nhận ×2"), Ads.DailyGiftAd, () => ShopService.Gift(true, Redraw), extra: true);
        }

        void ClaimCells()
        {
            foreach (var id in new[] { "week", "month" })
            {
                if (!Shop.CardClaimable(S, id, Now)) continue;
                var def = C.Card(id);
                Cell(Loc.F("{0}: quà ngày", def.Name), Loc.F("Còn {0}.", ShopUi.Clock(Shop.CardUntil(S, id) - Now)), ShopHue.Sky)
                    .Items(Shop.Resolve(S, D, def.daily, true, null))
                    .Button(Loc.T("Nhận"), BtnColor.Green, () => ShopService.Free(Shop.ClaimCard(S, D, id, Now, R), def.Name, _ => Redraw()));
            }
            if (S.shop == null) return;
            foreach (var kv in S.shop.days.ToList())
            {
                var pk = C.Pack(kv.Key);
                if (pk == null || !Shop.DayClaimable(S, D, kv.Key, Now)) continue;
                int day = kv.Value.claimed + 1;
                Cell(Loc.F("{0}: ngày {1}", pk.Name, day), null, ShopHue.Berry)
                    .Items(Shop.Resolve(S, D, pk.days[kv.Value.claimed].items, pk.scale, null))
                    .Button(Loc.T("Nhận"), BtnColor.Green, () => ShopService.Free(Shop.ClaimDay(S, D, kv.Key, Now, R), pk.Name, _ => Redraw()));
            }
        }

        public static void OpenChain() => Sub(DrawChainOn);

        // dòng giới thiệu Gói Vượt Mốc: lực chiến tướng trong gói (sau khi dùng hết đồ của gói) cạnh tướng mạnh nhất đang có
        static string JumpLine(ActiveOffer o)
        {
            string name = D.Hero(o.hero).name;
            var pw = Offers.JumpPower(S, D, o.hero);
            return pw.pack > pw.best && pw.best > 0
                ? Loc.F("{0} về đội ngay, lực chiến {1} (tướng mạnh nhất của bạn: {2}). Đủ mảnh lên sao, kèm thẻ và đá tiến hóa.", name, pw.pack, pw.best)
                : Loc.F("{0} về đội ngay: đủ mảnh lên sao, kèm thẻ và đá tiến hóa.", name);
        }

        void OfferCell(ActiveOffer o, bool popup)
        {
            var pk = o.pack != null ? C.Pack(o.pack) : null;
            string desc = pk?.Desc;
            if (pk != null && pk.kind == "days") desc = Loc.T("Mua một lần, nhận 3 ngày liền (vào game mỗi ngày để nhận).");
            var c = Cell(ShopService.OfferName(o), desc, ShopHue.Offer(o)).Items(Shop.OfferItems(S, D, o)).Value(Shop.OfferMult(S, D, o)).Timer(o.until);
            if (o.bought)
            {
                c.Done(Loc.T("Đã mua"));
                return;
            }
            c.Button(ShopService.Price(pk?.price ?? o.price), BtnColor.Orange, () => ShopService.BuyOffer(o.uid, ok => AfterBuy(ok, popup)));
        }

        void PackCellFor(ShopPack pk)
        {
            var items = Shop.Resolve(S, D, pk.items, pk.scale, null);
            bool first = Shop.FirstBonus(S, pk);
            string desc = pk.Desc;
            if (pk.weekly && pk.items.Any(i => i.k == Shop.TicketWeek))
                desc = Loc.F("{0} Tướng tuần: {1}.", desc, string.Join(", ", Shop.FeaturedNow(D, Now).Select(h => D.Hero(h)?.name)));
            var c = Cell(pk.Name, first ? desc : pk.firstDouble ? "" : desc, PackHue(pk)).Items(items).Value(Shop.PackMult(S, D, pk));
            if (first) c.Note(Loc.T("Lần đầu tặng gấp đôi bi!"), Theme.RedD);
            int left = Shop.Left(S, pk, Now);
            if (pk.kind == "noads" && AdGate.NoAds(S) || left <= 0)
            {
                c.Done(pk.daily ? Loc.T("Mai mua tiếp") : pk.weekly ? Loc.T("Tuần sau mua tiếp") : Loc.T("Đã mua"));
                return;
            }
            if (pk.limit > 0 && left < int.MaxValue && pk.limit > 1) c.Note(Loc.F("Còn {0} lượt", left));
            c.Button(ShopService.Price(pk.price), BtnColor.Orange, () => ShopService.BuyPack(pk.id, ok => AfterBuy(ok, false)));
        }

        void FreeBallsCell()
        {
            Cell(Loc.T("Bi miễn phí"), Loc.T("Xem quảng cáo nhận bi."), ShopHue.Sky)
                .Items(new[] { new ShopItem { k = "balls", n = ShopService.FreeBallsN } })
                .AdButton(Loc.T("Xem"), Ads.FreeBalls, () => ShopService.FreeBalls(Redraw));
        }

        void CardCell(ShopPack pk)
        {
            var card = Shop.CardOf(C, pk);
            string id = card?.id ?? "week";
            bool on = Shop.CardActive(S, id, Now);
            var c = Cell(pk.Name, pk.Desc, ShopHue.Sky).Items(Shop.Resolve(S, D, pk.items, pk.scale, null)).Value(Shop.PackMult(S, D, pk));
            if (on) c.Note(Loc.F("Đang có · còn {0}", ShopUi.Clock(Shop.CardUntil(S, id) - Now)), Theme.GreenD).Hue(ShopHue.Mint);
            c.Button(on ? Loc.F("Gia hạn {0}", ShopService.Price(pk.price)) : ShopService.Price(pk.price), BtnColor.Orange,
                () => ShopService.BuyPack(pk.id, ok => AfterBuy(ok, false)));
            if (Shop.CardClaimable(S, id, Now))
                c.Extra(Loc.T("Quà ngày"), BtnColor.Green, () => ShopService.Free(Shop.ClaimCard(S, D, id, Now, R), pk.Name, _ => Redraw()));
        }

        void FundEntry(ShopPack pk)
        {
            var st = Shop.Of(S);
            int ready = Shop.FundReady(S, C);
            var c = Cell(pk.Name, pk.Desc, ShopHue.Gold).Value(Shop.PackMult(S, D, pk));
            if (ready > 0) c.Note(Loc.F("{0} mốc chờ nhận", ready), Theme.RedD);
            if (!st.fund) c.Button(ShopService.Price(pk.price), BtnColor.Orange, () => ShopService.BuyPack(pk.id, ok => AfterBuy(ok, false)));
            c.Extra(Loc.T("Xem quỹ"), BtnColor.Paper, OpenFund);
        }

        void PiggyCell(bool popup = false)
        {
            var st = Shop.Of(S);
            int n = (int)Math.Floor(st.piggy);
            double cap = Shop.PiggyCap(S, C);
            var pk = C.Pack("piggy");
            var c = Cell(Loc.T("Lọ Bi"), Loc.F("Lọ đang có {0}/{1} bi. Mỗi bi bạn thả bỏ 1 bi vào lọ.", n, cap), ShopHue.Gold)
                .Items(new[] { new ShopItem { k = "balls", n = Math.Max(n, 0) } })
                .Value(pk.price > 0 ? n / (pk.price * C.valuePerUsd) : 0);
            if (Shop.PiggyCanBreak(S, C, Now))
                c.Button(Loc.F("Đập lọ {0}", ShopService.Price(pk.price)), BtnColor.Orange, () => ShopService.BuyPack("piggy", ok => AfterBuy(ok, popup)));
            else if (Shop.PiggyWait(S, C, Now) > 0) c.Note(Loc.F("Lọ vừa đập. Đập lại được sau {0}.", ShopUi.Clock(Shop.PiggyWait(S, C, Now))));
            else c.Note(Loc.F("Đủ {0} bi mới đập được.", Math.Ceiling(cap * C.piggy.minPct)));
        }

        static void DrawChainOn(ShopSheet s)
        {
            var def = Shop.ChainNow(S, C);
            var st = Shop.Of(S);
            s.Header(Loc.F("Chuỗi Quà: {0}", def?.Name), Loc.F("Còn {0}", ShopUi.Clock(st.chainUntil - Now)));
            if (def == null) return;
            for (int i = 0; i < def.steps.Count; i++)
            {
                var cs = def.steps[i];
                int k = i;
                var c = s.Cell(Loc.F("Ô {0}", i + 1), null, cs.price > 0 ? ShopHue.Grape : ShopHue.Mint).Items(Shop.Resolve(S, D, cs.items, true, null));
                if (cs.price > 0) c.Value(Shop.Mult(C, D, Shop.Resolve(S, D, cs.items, true, null), cs.price));
                if (i < st.chainStep) c.Done(cs.price > 0 ? Loc.T("Đã mua") : Loc.T("Đã nhận"));
                else if (i == st.chainStep && Shop.ChainLive(S, Now))
                    c.Button(cs.price > 0 ? ShopService.Price(cs.price) : Loc.T("Nhận miễn phí"), cs.price > 0 ? BtnColor.Orange : BtnColor.Green,
                        () => ShopService.ChainTake(k, _ => s.Redraw()));
                else c.Note(Loc.T("Mở sau ô trước"), Theme.Ink3);
            }
        }

        // ---------- trang con ----------

        public static void OpenFund() => Sub(s =>
        {
            var st = Shop.Of(S);
            s.Header(Loc.T("Quỹ Phiêu Lưu"), st.fund ? Loc.T("Đã mua: nhận cả hai hàng ở mỗi mốc.") : Loc.T("Hàng miễn phí cho mọi người; mua quỹ để nhận hàng lớn."));
            for (int i = 0; i < C.fund.Count; i++)
            {
                var f = C.fund[i];
                int k = i;
                var paid = Shop.Resolve(S, D, f.paid, true, null);
                var free = Shop.Resolve(S, D, f.free, true, null);
                var c = s.Cell(Loc.F("Cấp {0}", f.lv), null, S.level >= f.lv ? ShopHue.Gold : ShopHue.Slate).Items(free.Concat(paid));
                bool canFree = Shop.FundClaimable(S, C, i, false), canPaid = Shop.FundClaimable(S, C, i, true);
                bool gotFree = st.fundFree.Contains(i), gotPaid = st.fundPaid.Contains(i);
                if (S.level < f.lv)
                {
                    c.Note(Loc.F("Tới cấp {0} để nhận", f.lv), Theme.Ink3);
                    continue;
                }
                if (gotFree && (gotPaid || !st.fund))
                {
                    if (gotPaid) c.Done(Loc.T("Đã nhận"));
                    else c.Note(Loc.T("Đã nhận hàng miễn phí. Mua quỹ để nhận hàng lớn."), Theme.Ink2);
                    continue;
                }
                if (canFree) c.Button(Loc.T("Nhận miễn phí"), BtnColor.Green, () => ShopService.Free(Shop.FundClaim(S, D, k, false, Now, R), Loc.T("Quỹ Phiêu Lưu"), _ => s.Redraw()));
                if (canPaid) c.Extra(Loc.T("Nhận hàng lớn"), BtnColor.Orange, () => ShopService.Free(Shop.FundClaim(S, D, k, true, Now, R), Loc.T("Quỹ Phiêu Lưu"), _ => s.Redraw()));
            }
        });

        public static void OpenTicket(bool week, int index) => Sub(s =>
        {
            var st = Shop.Of(S);
            if (week ? st.Item(Shop.TicketWeek) <= 0 : index >= st.tickets.Count)
            {
                s.Close();
                return;
            }
            var choices = week ? Shop.FeaturedNow(D, Now) : Shop.TicketChoicesOf(S, D, st.tickets[index], Now);
            s.Header(week ? Loc.T("Vé tướng tuần") : Loc.T("Vé chọn tướng"), Loc.T("Chọn một tướng: chưa có thì nhận đủ mảnh mở khoá, đã có thì nhận mảnh lên sao."));
            foreach (var hid in choices)
            {
                var h = D.Hero(hid);
                if (h == null) continue;
                int n = Shop.TicketShards(S, D, hid);
                var g = Progress.ShardGoal(S, D, hid);
                var c = s.Cell(h.name, (S.Hero(hid).owned ? Loc.T("Đã có · ") : Loc.T("Chưa có · ")) + Elements.RarityName(h.rarity) + " · " + Elements.Name(h.elem),
                    ShopHue.Tier((int)h.rarity));
                c.HeroTile(h, "×" + n).Tag(g.need > 0 ? $"{g.have}/{g.need}" : "", Theme.Paper2);
                c.Button(Loc.T("Chọn"), BtnColor.Green, () => App.Modals.Confirm(Loc.T("Chọn tướng"), Loc.F("Dùng vé lấy {0} mảnh {1}?", n, h.name), Loc.T("Chọn"), () =>
                {
                    s.Close();
                    ShopService.UseTicket(week, index, hid);
                }, null, BtnColor.Green));
            }
        });

        void AfterBuy(bool ok, bool popup)
        {
            if (!ok) return;
            if (popup)
            {
                bought = true;
                Close();
                return;
            }
            Redraw();
        }

        // ---------- popup ----------

        void Popup(Popup pop)
        {
            Tabs(false);
            Mute(!pop.free);
            switch (pop.kind)
            {
                case "offer":
                {
                    var o = Shop.FindOffer(S, pop.id);
                    // nhóm chọn một (nạp đầu 3 bậc): các gói cùng nhóm vẽ ngay dưới gói đứng đầu
                    var sibs = o?.pack != null && C.Pack(o.pack)?.group == o.pack
                        ? Shop.Live(S, Now).Where(x => x.pack != null && x.pack != o.pack && C.Pack(x.pack)?.group == o.pack).OrderBy(x => x.price).ToList()
                        : new List<ActiveOffer>();
                    string sub = pop.warn ? Loc.T("Sắp hết giờ!") : sibs.Count > 0 ? Loc.T("Chọn một trong các gói: mua gói nào thì các gói kia đóng lại.") :
                        o?.tpl == "relief" ? Loc.T("Mạnh hơn cho ải đang kẹt.") :
                        o?.tpl == "hot" ? Loc.T("Chỉ trong 10 phút!") :
                        o?.tpl == "jump" && o.hero != null && D.Hero(o.hero) != null
                            ? JumpLine(o) : null;
                    Header(o != null ? ShopService.OfferName(o) : Loc.T("Ưu đãi"), sub);
                    redraw = () =>
                    {
                        if (o != null) OfferCell(o, true);
                        foreach (var x in sibs)
                            if (!x.bought && (x.until <= 0 || x.until > Now)) OfferCell(x, true);
                    };
                    break;
                }
                case "comeback":
                {
                    var o = Shop.FindOffer(S, pop.id);
                    var gift = Shop.Grant(S, D, Shop.Resolve(S, D, C.comebackGift, true, null), Now, R);
                    App.Save.Save();
                    Header(Loc.T("Mừng bạn trở lại!"), Loc.T("Quà trở lại đã vào túi."));
                    redraw = () =>
                    {
                        Cell(Loc.T("Quà trở lại"), null, ShopHue.Mint).Rewards(gift).Done(Loc.T("Đã nhận"));
                        if (o != null) OfferCell(o, true);
                    };
                    break;
                }
                case "intro":
                {
                    var pk = C.Pack(pop.id);
                    Header(pk?.Name ?? "", pop.id == "fund" ? Loc.T("Mua một lần, nhận thưởng lớn ở mỗi mốc cấp.") : Loc.T("Quà mỗi ngày trong 7 ngày."));
                    redraw = () =>
                    {
                        if (pk == null) return;
                        if (pk.kind == "card") CardCell(pk);
                        else if (pk.kind == "fund") FundEntry(pk);
                        else PackCellFor(pk);
                    };
                    break;
                }
                case "refill":
                    if (pop.warn) Header(Loc.T("Sắp hết bi!"), Loc.F("Còn {0} bi. Bổ sung để thả tiếp, lên cấp cho mọi tướng.", S.balls));
                    else Header(Loc.T("Hết bi!"), Loc.T("Bi để thả máy bi, lên cấp cho mọi tướng."));
                    redraw = () => DrawRefill(pop.first);
                    break;
                case "piggy":
                    Header(Loc.T("Lọ Bi đầy rồi!"), Loc.T("Đập lọ để lấy hết bi đã tích."));
                    redraw = () => PiggyCell(true);
                    break;
                case "chain":
                    redraw = () => DrawChainOn(this);
                    break;
                case "claims":
                    Header(Loc.T("Quà hôm nay"), null);
                    redraw = () =>
                    {
                        Cell(Loc.T("Nhận hết quà hôm nay"), null, ShopHue.Mint).Button(Loc.T("Nhận hết"), BtnColor.Green, () => ShopService.ClaimAll(Close));
                        GiftCell();
                        ClaimCells();
                    };
                    break;
                default:
                    Header(Loc.T("Cửa hàng"), null);
                    break;
            }
            Redraw();
        }

        void DrawRefill(bool first)
        {
            FreeBallsCell();
            double now = Now;
            int stock = Trees.Stock(S, D.Cfg, now);
            if (Trees.Open(S, D.Cfg) > 0)
            {
                var c = Cell(Loc.T("Cây bi"), stock > 0 ? Loc.F("Cây đang có {0} bi chờ hái ở Nhà.", stock) : Loc.T("Cây bi ra bi theo giờ ở Nhà."), ShopHue.Mint);
                if (stock > 0) c.Button(Loc.T("Tới Nhà"), BtnColor.Green, () =>
                {
                    Close();
                    App.Router.Go(SceneIds.Home);
                });
            }
            else Cell(Loc.T("Thắng ải để có thêm bi"), Loc.T("Mỗi trận thắng cho bi; ải lần đầu cho nhiều hơn."), ShopHue.Slate);
            if (Shop.PiggyCanBreak(S, C, Now)) PiggyCell(true);
            if (first) return;
            for (int i = 1; i <= 3; i++)
                if (C.Pack("refill_" + i) is ShopPack pk)
                {
                    var items = Shop.Resolve(S, D, pk.items, pk.scale, null);
                    Cell(pk.Name, null, ShopHue.Sky).Items(items).Value(Shop.PackMult(S, D, pk))
                        .Button(ShopService.Price(pk.price), BtnColor.Orange, () => ShopService.BuyPack(pk.id, ok => AfterBuy(ok, true)));
                }
        }
    }
}
