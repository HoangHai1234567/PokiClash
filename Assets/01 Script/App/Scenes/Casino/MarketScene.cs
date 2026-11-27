// Scene Chợ đen của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.4, mốc C6; mỗi trò một scene). Prefab Screens/CasinoMarket (menu
// "PokiClash/Prefab/Đảo Casino/Chợ đen: dựng scene"). Lõi: Core/Casino/BlackMarket.cs.
// - Trên: lời lái buôn (đổi theo mốc hàng, ngày / đêm), đồng hồ đổi hàng, số lần làm mới hôm nay.
// - Kệ: 6 ô hàng ngày (2 hàng × 3) + 2 ô hàng đêm (hàng thứ ba, chỉ bày từ 19 giờ tới 5 giờ; ban ngày là bảng báo). Mỗi ô: ô thưởng
//   (Items/OThuong), dòng ghi chú loại hàng, nút giá; mua xong thì dấu "Đã mua" và tô xanh như ô cửa hàng.
// - Mua: hỏi lại (tên, giá); Túi hàng lậu mở bằng hộp rương chung (ChestBox), món khác báo bằng dòng thưởng.
// - Làm mới sớm (giá tăng dần, hết lượt thì khoá), Tỉ lệ túi lậu (công bố tỉ lệ, hộp may rủi).
// - Thu mua: bán cả giỏ cá (Fishing.SellCreel); bản sao thẻ thừa của thẻ đã tối đa cấp đổi lấy đá tiềm năng, có trần mỗi ngày
//   (BlackMarket.SellSpare; không đổi ra bi, GD_Claude/33 mục 2.1).
// Mọi vật dựng sẵn trong prefab (8 ô), không sinh lúc chạy.
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
    public sealed class MarketScene : SceneRoot
    {
        [System.Serializable]
        public struct Slot
        {
            public GameObject root;
            public Image card;
            public RewardTile tile;
            public TextMeshProUGUI note, sold, tag;
            public SketchButton buy;
        }

        [SerializeField] TextMeshProUGUI talk, info;
        [SerializeField] Slot[] slots;
        [SerializeField] TextMeshProUGUI nightNote;
        [SerializeField] SketchButton refresh, odds;
        [SerializeField] TextMeshProUGUI fishText, spareText;
        [SerializeField] SketchButton sellFish, sellSpare;

        public override string Title => Loc.T("Chợ đen");
        public override string BackTo => SceneIds.Casino;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public static readonly Color NightTint = new Color(0.78f, 0.80f, 0.93f, 1f);
        static readonly Color DoneTint = Theme.Hex("#e6f7d9");

        int stamp = -1;
        bool night;
        float nextTick;
        Rng rng;

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextMeshProUGUI talkText, TextMeshProUGUI infoText, Slot[] slotList, TextMeshProUGUI nightText, SketchButton refreshBtn,
            SketchButton oddsBtn, TextMeshProUGUI fish, TextMeshProUGUI spare, SketchButton fishBtn, SketchButton spareBtn)
        {
            talk = talkText; info = infoText; slots = slotList; nightNote = nightText; refresh = refreshBtn; odds = oddsBtn;
            fishText = fish; spareText = spare; sellFish = fishBtn; sellSpare = spareBtn;
        }

        public override void Enter(object args)
        {
            rng = new Rng(Rng.RandomSeed());
            refresh.SetOnClick(Restock);
            odds.SetOnClick(Odds);
            sellFish.SetOnClick(SellFish);
            sellSpare.SetOnClick(SellSpare);
            Render();
            CasinoGuide.Market(); // lần đầu: Lão Mực trồi lên góc màn giới thiệu chợ
        }

        public override void Refresh() => Render();

        void Update()
        {
            if (Time.unscaledTime < nextTick) return;
            nextTick = Time.unscaledTime + 0.5f;
            // sang mốc hàng mới (0, 8, 16 giờ) hoặc ngày / đêm đổi thì bày lại kệ; không thì chỉ chạy đồng hồ
            double now = Now;
            if (BlackMarket.Stamp(D, now) != stamp || Casino.Night(now) != night) Render();
            else Clock(now);
        }

        // ---------- vẽ ----------

        void Render()
        {
            var s = S;
            var d = D;
            double now = Now;
            stamp = BlackMarket.Stamp(d, now);
            night = Casino.Night(now);
            var stock = BlackMarket.Stock(s, d, now);
            var c = d.Cfg.casino.market;
            talk.text = Talk(stock);
            Clock(now);
            // ô hàng ngày điền từ đầu; ô hàng đêm luôn ở hàng thứ ba (sau c.slots ô ngày)
            var day = stock.Where(x => !x.night).ToList();
            var nite = stock.Where(x => x.night).ToList();
            for (int i = 0; i < slots.Length; i++)
            {
                bool nightRow = i >= c.slots;
                var sl = nightRow ? (i - c.slots < nite.Count ? nite[i - c.slots] : null) : (i < day.Count ? day[i] : null);
                BindSlot(slots[i], sl, nightRow);
            }
            if (nightNote)
            {
                nightNote.transform.parent.gameObject.SetActive(!night && c.nightSlots > 0); // bảng báo (tờ giấy chứa chữ) thay hàng ô đêm
                nightNote.text = Loc.T("Hàng đêm") + "\n" + Loc.T("Từ 19 giờ tối tới 5 giờ sáng, lái buôn bày thêm 2 ô hàng hiếm.");
            }
            int cost = BlackMarket.RefreshCost(s, d, now);
            refresh.SetText(cost < 0 ? Loc.T("Hết lượt làm mới") : Loc.F("Làm mới · {0} bi", cost));
            refresh.Locked = cost < 0;
            odds.SetText(Loc.T("Tỉ lệ túi lậu"));
            // thu mua
            var st = Casino.Of(s);
            int fishV = Fishing.CreelValue(s, d);
            fishText.text = st.creel.Count > 0 ? Loc.F("Giỏ cá: {0} con", st.creel.Count) : Loc.T("Giỏ cá trống");
            sellFish.SetText(fishV > 0 ? Loc.F("Bán · {0} bi", fishV) : Loc.T("Bán"));
            sellFish.Locked = fishV <= 0;
            int spareN = BlackMarket.SpareCopies(s, d), spareV = BlackMarket.SpareValue(s, d, now);
            bool spareCap = spareN >= c.copyPerStone && BlackMarket.SpareStonesLeft(s, d, now) <= 0; // đủ thẻ nhưng hết lượt đổi hôm nay
            spareText.text = spareN > 0 ? Loc.F("Bản sao thẻ thừa: {0} ({1} bản đổi 1 đá tiềm năng)", spareN, c.copyPerStone)
                : Loc.T("Chưa có bản sao thẻ thừa (thẻ đã tối đa cấp)");
            sellSpare.SetText(spareV > 0 ? Loc.F("Đổi · {0} đá", spareV) : spareCap ? Loc.T("Hết lượt hôm nay") : Loc.T("Đổi"));
            sellSpare.Locked = spareV <= 0;
        }

        void Clock(double now)
        {
            var c = D.Cfg.casino.market;
            int used = Casino.Of(S).mkRefreshDay == Casino.Today(now) ? Casino.Of(S).mkRefresh : 0;
            info.text = Loc.F("Đổi hàng sau {0}", ShopUi.Clock(BlackMarket.NextRefresh(D, now))) + " · " +
                        Loc.F("làm mới hôm nay {0}/{1}", used, c.refresh.Length);
        }

        // lời lái buôn: theo lượt hàng (cố định trong lượt), có câu riêng ban đêm và khi có đồ để thu mua
        string Talk(List<MkSlot> stock)
        {
            var s = S;
            if (Casino.Of(s).creel.Count > 0 || BlackMarket.SpareCopies(s, D) > 0)
                return Loc.T("Có cá trong giỏ thì ta mua, thẻ thừa thì ta đổi đá tiềm năng cho.");
            if (night) return Loc.T("Hàng đêm bày rồi đấy. Thứ này ban ngày không có đâu.");
            if (stock.Count > 0 && stock.All(x => x.bought)) return Loc.T("Hết hàng rồi! Đợi lượt hàng sau, hoặc trả chút bi để ta lục kho.");
            string[] lines =
            {
                Loc.T("Hàng mới về. Mảnh tướng ở đây biết trước, không may rủi, chỉ hơi chát."),
                Loc.T("Đêm xuống ta bày thêm hàng hiếm. Ghé lại sau 7 giờ tối nhé."),
                Loc.T("Túi hàng lậu thì hên xui, tỉ lệ ta dán ngay đây, không giấu ai."),
            };
            return lines[(stamp % lines.Length + lines.Length) % lines.Length];
        }

        void BindSlot(Slot ui, MkSlot sl, bool nightRow)
        {
            // hàng đêm ban ngày: ẩn ô, bảng báo hiện thay
            ui.root.SetActive(sl != null);
            if (sl == null) return;
            var art = App.Art;
            var o = sl.offer;
            switch (o.kind)
            {
                case Casino.Bait:
                    // chưa có icon cá / mồi (C8 gen): tạm hạt mồi "seed" ("fish" không có, rơi về ngôi sao)
                    ui.tile.Item(art.Icon("seed"), "×" + o.n, Loc.T("Mồi câu"), Rarity.Common);
                    break;
                case "mystery":
                    ui.tile.Item(art.Icon("chest"), "?", Loc.T("Túi hàng lậu"), Rarity.Epic);
                    break;
                case "home":
                    // icon khay Xây của Nhà (icon_home_<mã>)
                    ui.tile.Item(art.Icon("home_" + sl.deco), "×" + Mathf.Max(1, o.n), D.Cfg.home.Def(sl.deco)?.Name ?? sl.deco, Rarity.Rare);
                    break;
                default:
                    if (sl.items.Count > 0) ShopUi.Tile(ui.tile, sl.items[0]);
                    break;
            }
            ui.note.text = Note(sl);
            ui.tag.transform.parent.gameObject.SetActive(nightRow);
            ui.tag.text = Loc.T("Hàng đêm");
            ui.sold.gameObject.SetActive(sl.bought);
            ui.sold.text = Loc.T("Đã mua");
            ui.card.color = sl.bought ? DoneTint : nightRow ? NightTint : Theme.Paper;
            ui.buy.gameObject.SetActive(!sl.bought);
            ui.buy.SetText(Loc.F("{0} bi", NumFmt.Short(sl.price)));
            ui.buy.SetRole(S.balls >= sl.price ? BtnColor.Green : BtnColor.Paper);
            var idx = sl.idx;
            ui.buy.SetOnClick(() => Buy(idx));
        }

        static string Note(MkSlot sl)
        {
            switch (sl.offer.kind)
            {
                case "shards": return Loc.T("Biết trước, không may rủi");
                case "copies": return Loc.T("Bản sao thẻ của tướng này");
                case "evo":
                case "crystal": return Loc.T("Hàng hiếm, có hạn");
                case "stones": return Loc.T("Nâng tiềm năng tướng");
                case Casino.Bait: return Loc.T("Dùng ở Bến câu");
                case "mystery": return Loc.T("Hên xui, xem Tỉ lệ");
                case "home": return Loc.T("Trang trí Nhà, vào túi đồ");
                default: return "";
            }
        }

        static string ItemName(MkSlot sl)
        {
            var o = sl.offer;
            if (o.kind == Casino.Bait) return Loc.F("{0} mồi câu", o.n);
            if (o.kind == "mystery") return Loc.T("Túi hàng lậu");
            if (o.kind == "home") return Mathf.Max(1, o.n) + " " + (D.Cfg.home.Def(sl.deco)?.Name ?? sl.deco);
            if (sl.items.Count == 0) return o.kind;
            var it = sl.items[0];
            if (it.k == "shards") return Loc.F("{0} mảnh {1}", it.n, D.Hero(it.h)?.name ?? it.h);
            if (it.k == "copies") return Loc.F("{0} bản sao thẻ {1}", it.n, D.Hero(it.h)?.name ?? it.h);
            return it.n + " " + ShopUi.ItemName(it);
        }

        // ---------- thao tác ----------

        void Buy(int idx)
        {
            var s = S;
            var d = D;
            var sl = BlackMarket.Stock(s, d, Now).Find(x => x.idx == idx);
            if (sl == null || sl.bought)
            {
                Render();
                return;
            }
            if (s.balls < sl.price)
            {
                App.Audio.Play("error");
                App.Toasts.Show(Loc.F("Cần {0} bi, bạn có {1}", sl.price, s.balls), Icon("ball"));
                return;
            }
            App.Modals.Confirm(Loc.T("Mua hàng"), Loc.F("Mua {0} với {1} bi?", ItemName(sl), sl.price), Loc.T("Mua"), () => DoBuy(idx), null,
                BtnColor.Green);
        }

        void DoBuy(int idx)
        {
            var s = S;
            var d = D;
            var sl = BlackMarket.Stock(s, d, Now).Find(x => x.idx == idx);
            bool mystery = sl?.offer.kind == "mystery";
            var r = BlackMarket.Buy(s, d, idx, Now, rng, out var why);
            if (r == null)
            {
                App.Audio.Play("error");
                App.Toasts.Show(why, Icon("lock"));
                Render();
                return;
            }
            App.Save.Save();
            App.Audio.Play("coin");
            Haptics.Play(Haptic.UiTap);
            Render();
            if (mystery) StartCoroutine(ChestBox.Show(Loc.T("Túi hàng lậu"), SlotKind.ChestSilver, null, r, Loc.T("Nhận")));
            else
            {
                App.Toasts.Show(CasinoUi.Rewards(r), Icon("shop"));
                CasinoGuide.Bought(); // Lão Mực bình phẩm (thỉnh thoảng)
            }
            int k = UiOf(idx);
            // món mua bay từ ô hàng về ô chứa (RewardFly); túi hàng lậu bay từ hộp nhận quà
            if (!mystery && k >= 0) RewardFly.Rewards(r, slots[k].root.transform.position);
            if (k >= 0) StartCoroutine(ChestBox.Pop((RectTransform)slots[k].root.transform, 1.08f));
        }

        // ô giao diện của ô hàng idx (ô ngày điền từ đầu, ô đêm ở hàng thứ ba), −1 nếu không hiện
        int UiOf(int idx)
        {
            var c = D.Cfg.casino.market;
            var stock = BlackMarket.Stock(S, D, Now);
            var day = stock.Where(x => !x.night).ToList();
            var nite = stock.Where(x => x.night).ToList();
            int i = day.FindIndex(x => x.idx == idx);
            if (i >= 0) return i < c.slots && i < slots.Length ? i : -1;
            i = nite.FindIndex(x => x.idx == idx);
            return i >= 0 && c.slots + i < slots.Length ? c.slots + i : -1;
        }

        void Restock()
        {
            var s = S;
            int cost = BlackMarket.RefreshCost(s, D, Now);
            if (cost < 0) return;
            if (s.balls < cost)
            {
                App.Audio.Play("error");
                App.Toasts.Show(Loc.F("Cần {0} bi, bạn có {1}", cost, s.balls), Icon("ball"));
                return;
            }
            if (!BlackMarket.Refresh(s, D, Now)) return;
            App.Save.Save();
            App.Audio.Play("deal");
            Render();
            talk.text = Loc.T("Được rồi, để ta lục kho xem còn gì...");
        }

        // tỉ lệ Túi hàng lậu (công bố, như máy bi)
        void Odds()
        {
            var d = D;
            double band = Casino.Band(S, d);
            var sb = new System.Text.StringBuilder();
            sb.AppendLine(Loc.F("Giá túi: {0} bi. Mỗi túi ra một món:", BlackMarket.MysteryPrice(S, d)));
            sb.AppendLine();
            foreach (var (roll, p) in BlackMarket.MysteryOdds(d))
                sb.AppendLine($"{RollText(roll, band)}: {p * 100:0.#}%");
            App.Modals.Alert(Loc.T("Tỉ lệ túi lậu"), sb.ToString().TrimEnd(), Loc.T("Đóng"));
        }

        static string RollText(ChestRoll r, double band)
        {
            string Range(int a, int b) => a == b ? a.ToString() : $"{a}–{b}";
            switch (r.k)
            {
                case "balls": return Loc.F("{0} bi", Range(Shop.RoundBalls(r.min * band), Shop.RoundBalls(r.max * band)));
                case "stones": return Loc.F("{0} đá tiềm năng", Range(r.min, r.max));
                case "evo": return Loc.F("{0} đá tiến hóa", Range(r.min, r.max));
                case "shards": return Loc.F("{0} mảnh tướng", Range(r.min, r.max));
                case "egg": return Range(r.min, r.max) + " " + ShopUi.EggName(r.tier);
                default: return r.k;
            }
        }

        void SellFish()
        {
            int v = Fishing.SellCreel(S, D);
            if (v <= 0) return;
            App.Save.Save();
            App.Audio.Play("coin");
            App.Toasts.Show(Loc.F("Bán cá được {0} bi", v), Icon("ball"));
            RewardFly.Balls(v, sellFish.transform.position);
            Render();
        }

        void SellSpare()
        {
            var s = S;
            int v = BlackMarket.SpareValue(s, D, Now), n = v * D.Cfg.casino.market.copyPerStone;
            if (v <= 0) return;
            App.Modals.Confirm(Loc.T("Đổi thẻ thừa"),
                Loc.F("Đổi {0} bản sao thẻ thừa (thẻ đã tối đa cấp, không dùng được nữa) lấy {1} đá tiềm năng? Mỗi ngày đổi tối đa {2} đá.", n, v, D.Cfg.casino.market.stoneDaily),
                Loc.T("Đổi"), () =>
                {
                    int got = BlackMarket.SellSpare(S, D, Now);
                    if (got <= 0) return;
                    App.Save.Save();
                    App.Audio.Play("coin");
                    App.Toasts.Show(Loc.F("Đổi thẻ thừa được {0} đá tiềm năng", got), Icon("rock"));
                    RewardFly.Send(RewardFly.To.Cave, App.Art.Icon("rock"), sellSpare.transform.position, got);
                    Render();
                }, null, BtnColor.Green);
        }

        // ---------- cho lượt chụp ----------

        // mua ô hàng ngày đầu tiên chưa mua, bỏ qua hỏi lại (lượt chụp)
        public bool BuyFirstForTest(string kind = null)
        {
            var sl = BlackMarket.Stock(S, D, Now).FirstOrDefault(x => !x.bought && (kind == null || x.offer.kind == kind));
            if (sl == null) return false;
            DoBuy(sl.idx);
            return true;
        }
    }
}
