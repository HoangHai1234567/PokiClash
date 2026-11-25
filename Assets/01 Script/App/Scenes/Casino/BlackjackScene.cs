// Scene lều Đêm Bài (Blackjack) của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.6, mốc C7). Prefab Screens/CasinoBlackjack (menu
// "PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene"). Lõi: Core/Casino/Blackjack.cs. Phần chung (bậc cược, hũ, chế độ): CasinoTableScene.
// - Bàn: hàng bài dealer (lá thứ hai úp tới khi ván xong), tổng điểm dealer; 2 tay của người chơi (tay thứ hai chỉ hiện khi Tách), mỗi tay:
//   bài, tổng, cược, kết quả; tay đang chơi viền vàng.
// - Nút: Chia bài (giá cược / Ván miễn phí / Ván tập), Rút, Dằn, Gấp đôi, Tách (gấp đôi / tách trả thêm cược của tay).
// - Gợi ý chiến thuật cơ bản ("Nên: Rút") cho người mới, tắt / bật bằng nút Gợi ý (nhớ trong bản lưu).
// - Lá bài dựng bằng code từ ô dựng sẵn: khung giấy, hạng (A, 2–10, J, Q, K), chất là icon hệ Kim / Mộc / Thủy / Hỏa.
// Mọi vật dựng sẵn trong prefab (8 lá mỗi hàng), không sinh lúc chạy. Diễn chia bài để sau (người dùng 2026-11-25: giao diện, animation chỉnh sau).
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BlackjackScene : CasinoTableScene
    {
        [System.Serializable]
        public struct Card
        {
            public GameObject root;
            public Image face, suit, back;
            public TextMeshProUGUI rank;
        }

        [System.Serializable]
        public struct HandUi
        {
            public GameObject root;
            public Image frame;
            public Card[] cards;
            public TextMeshProUGUI total, result;
        }

        [SerializeField] Card[] dealer;
        [SerializeField] TextMeshProUGUI dealerTotal;
        [SerializeField] HandUi[] hands;
        [SerializeField] TextMeshProUGUI hint, banner;
        [SerializeField] SketchButton deal, hit, stand, dbl, split, hintToggle;

        public override string Title => Loc.T("Đêm Bài");
        protected override string Game => Casino.Blackjack;
        protected override CasinoTable Table => D.Cfg.casino.blackjack;
        protected override bool Busy => game != null && game.phase == BjPhase.Player;

        protected override string HelpText =>
            Loc.T("Rút bài cho tổng gần 21 nhất mà không quá 21. A là 1 hoặc 11, J Q K là 10.") + "\n" +
            Loc.T("Dealer rút tới 17 thì dừng. Blackjack (A + lá 10 ngay hai lá đầu) trả 3:2, thắng trả 1:1, hoà trả lại cược.") + "\n" +
            Loc.T("Gấp đôi: cược thêm bằng cược đầu, nhận đúng một lá. Tách: hai lá cùng điểm tách thành hai tay, mỗi tay một cược.");

        BjGame game;
        bool settled;

        bool HintOn => !Casino.Of(S).seen.Contains("bjhint:off");

        // Dùng khi dựng prefab (Editor).
        public void Setup(Card[] dealerCards, TextMeshProUGUI dealerSum, HandUi[] handList, TextMeshProUGUI hintText, TextMeshProUGUI bannerText,
            SketchButton dealBtn, SketchButton hitBtn, SketchButton standBtn, SketchButton dblBtn, SketchButton splitBtn, SketchButton hintBtn)
        {
            dealer = dealerCards; dealerTotal = dealerSum; hands = handList; hint = hintText; banner = bannerText;
            deal = dealBtn; hit = hitBtn; stand = standBtn; dbl = dblBtn; split = splitBtn; hintToggle = hintBtn;
        }

        public BjGame GameNow => game;

        protected override void EnterTable()
        {
            game = null;
            settled = false;
            deal.SetOnClick(Deal);
            hit.SetOnClick(() => Act(BjAct.Hit));
            stand.SetOnClick(() => Act(BjAct.Stand));
            dbl.SetOnClick(() => Act(BjAct.Double));
            split.SetOnClick(() => Act(BjAct.Split));
            hintToggle.SetOnClick(ToggleHint);
            banner.text = Loc.T("Chọn mức cược rồi bấm Chia bài");
            Draw();
        }

        // rời lều giữa ván có cược: máy tự chơi nốt theo chiến thuật cơ bản rồi tính (không mất cược oan)
        public override void Exit()
        {
            if (game == null || settled) return;
            while (game.phase == BjPhase.Player) Blackjack.ActPaid(S, D, game, Blackjack.Advice(game), Now);
            settled = true;
            int staked = game.Staked;
            var jar = Blackjack.Finish(S, D, game, game.tier, Now, rng);
            App.Save.Save();
            int net = game.mode == TableMode.Paid ? game.payout - staked : game.mode == TableMode.Free ? Casino.FreeWin(game.payout, staked) : 0;
            if (game.mode != TableMode.Practice) App.Toasts.Show(Loc.F("Đêm Bài: ván bỏ dở đã tính, {0} bi", net >= 0 ? "+" + net : net.ToString()), Icon("ball"));
            if (jar.full && jar.rewards.Count > 0) App.Toasts.Show(Loc.T("Hũ bàn đầy: ") + CasinoUi.Rewards(jar.rewards), Icon("chest"));
            game = null;
        }

        protected override void OnTierChanged() => Draw();

        void Deal()
        {
            if (Busy) return;
            var mode = Mode;
            var g = Blackjack.StartAs(S, D, tier, mode, Now, rng, out var why);
            if (g == null)
            {
                NoBalls(why);
                return;
            }
            game = g;
            settled = false;
            App.Audio.Play("deal");
            App.Save.Save();
            banner.text = mode == TableMode.Free ? Loc.T("Ván miễn phí!") : mode == TableMode.Practice ? Loc.T("Ván tập") : "";
            if (game.phase == BjPhase.Done) Settle();
            RenderTable();
            Draw();
        }

        void Act(BjAct a)
        {
            if (game == null || !Blackjack.Can(game, a)) return;
            if (!Blackjack.ActPaid(S, D, game, a, Now))
            {
                NoBalls(Loc.T("Không đủ bi"));
                return;
            }
            App.Audio.Play(a == BjAct.Stand ? "click" : "deal");
            if (game.phase == BjPhase.Done) Settle();
            else App.Save.Save();
            RenderTable();
            Draw();
        }

        void Settle()
        {
            if (settled || game == null || game.phase != BjPhase.Done) return;
            settled = true;
            int staked = game.Staked;
            var jar = Blackjack.Finish(S, D, game, game.tier, Now, rng);
            int net = game.mode == TableMode.Paid ? game.payout - staked : game.mode == TableMode.Free ? Casino.FreeWin(game.payout, staked) : 0;
            bool anyWin = game.results.Any(r => r > 0), allPush = game.results.All(r => r == 0);
            string head = game.dealerPeekBj ? Loc.T("Dealer có Blackjack!") : game.results.Any(r => r == 2) ? Loc.T("Blackjack!")
                : anyWin ? Loc.T("Thắng!") : allPush ? Loc.T("Hoà") : Loc.T("Thua");
            banner.text = head + " " + (game.mode == TableMode.Practice ? Loc.T("(ván tập)")
                : net > 0 ? Loc.F("+{0} bi", net) : net < 0 ? Loc.F("−{0} bi", -net) : "");
            if (!anyWin) App.Audio.Play(allPush ? "click" : "stamp", 0.5f);
            AfterRound(net, game.mode == TableMode.Paid ? jar : null, null);
        }

        void ToggleHint()
        {
            var st = Casino.Of(S);
            if (HintOn) st.seen.Add("bjhint:off");
            else st.seen.Remove("bjhint:off");
            App.Save.Save();
            Draw();
        }

        // ---------- vẽ ----------

        static string RankText(int r) => r == 1 ? "A" : r == 11 ? "J" : r == 12 ? "Q" : r == 13 ? "K" : r.ToString();
        static readonly Elem[] Suits = { Elem.Kim, Elem.Moc, Elem.Thuy, Elem.Hoa };

        static void BindCard(Card ui, BjCard? c, bool hidden)
        {
            ui.root.SetActive(c != null);
            if (c == null) return;
            ui.back.gameObject.SetActive(hidden);
            ui.rank.gameObject.SetActive(!hidden);
            ui.suit.gameObject.SetActive(!hidden);
            if (hidden) return;
            var e = Suits[Mathf.Clamp(c.Value.suit, 0, 3)];
            ui.rank.text = RankText(c.Value.rank);
            ui.rank.color = Color.Lerp(Theme.Of(e), Theme.Ink, 0.35f);
            Theme.SetSprite(ui.suit, App.Art.Icon(ElemIcon(e)));
        }

        void Draw()
        {
            bool live = game != null && game.phase == BjPhase.Player;
            // dealer
            for (int i = 0; i < dealer.Length; i++)
                BindCard(dealer[i], game != null && i < game.dealer.Count ? game.dealer[i] : (BjCard?)null, live && i == 1);
            dealerTotal.text = game == null ? "" : live ? Loc.F("Dealer: {0} + ?", game.Up.rank == 1 ? 11 : game.Up.Value)
                : Blackjack.Total(game.dealer, out _) > 21 ? Loc.F("Dealer: {0} (quá 21)", Blackjack.Total(game.dealer, out _))
                : Loc.F("Dealer: {0}", Blackjack.Total(game.dealer, out _));
            // tay người chơi
            for (int h = 0; h < hands.Length; h++)
            {
                var ui = hands[h];
                var hand = game != null && h < game.hands.Count ? game.hands[h] : null;
                ui.root.SetActive(hand != null || h == 0);
                for (int i = 0; i < ui.cards.Length; i++)
                    BindCard(ui.cards[i], hand != null && i < hand.cards.Count ? hand.cards[i] : (BjCard?)null, false);
                ui.frame.color = live && game.active == h ? Theme.Yellow : new Color(1, 1, 1, 0.25f);
                if (hand == null)
                {
                    ui.total.text = Loc.F("Cược {0} bi", BetNow);
                    ui.result.text = "";
                    continue;
                }
                string bet = game.mode == TableMode.Paid ? Loc.F("cược {0} bi", hand.bet) : game.mode == TableMode.Free ? Loc.T("miễn phí") : Loc.T("ván tập");
                ui.total.text = Loc.F("{0} điểm", hand.Total) + (hand.Soft && hand.Total < 21 ? " " + Loc.T("(mềm)") : "") + " · " + bet +
                                (hand.doubled ? " · " + Loc.T("gấp đôi") : "");
                if (game.phase == BjPhase.Done && h < game.results.Length)
                {
                    int r = game.results[h];
                    ui.result.text = r == 2 ? Loc.T("Blackjack!") : r == 1 ? Loc.T("Thắng") : r == 0 ? Loc.T("Hoà") : hand.Bust ? Loc.T("Quá 21") : Loc.T("Thua");
                    ui.result.color = r > 0 ? Theme.GreenD : r == 0 ? Theme.Ink2 : Theme.RedD;
                }
                else ui.result.text = hand.Bust ? Loc.T("Quá 21") : "";
            }
            // nút
            deal.gameObject.SetActive(!live);
            var mode = Mode;
            deal.SetText(mode == TableMode.Free ? Loc.T("Ván miễn phí") : mode == TableMode.Practice ? Loc.T("Ván tập")
                : Loc.F("Chia bài · {0} bi", BetNow));
            deal.SetRole(mode == TableMode.Practice ? BtnColor.Blue : BtnColor.Green);
            foreach (var (b, a) in new[] { (hit, BjAct.Hit), (stand, BjAct.Stand), (dbl, BjAct.Double), (split, BjAct.Split) })
            {
                b.gameObject.SetActive(live);
                b.Locked = !(live && Blackjack.Can(game, a));
            }
            hit.SetText(Loc.T("Rút"));
            stand.SetText(Loc.T("Dằn"));
            dbl.SetText(game != null && game.mode == TableMode.Paid && game.Hand != null ? Loc.F("Gấp đôi · {0}", game.Hand.bet) : Loc.T("Gấp đôi"));
            split.SetText(Loc.T("Tách"));
            hintToggle.SetText(HintOn ? Loc.T("Gợi ý: bật") : Loc.T("Gợi ý: tắt"));
            hint.gameObject.SetActive(live && HintOn);
            if (live && HintOn)
            {
                var adv = Blackjack.Advice(game);
                hint.text = Loc.F("Nên: {0}", adv == BjAct.Hit ? Loc.T("Rút") : adv == BjAct.Stand ? Loc.T("Dằn") : adv == BjAct.Double ? Loc.T("Gấp đôi") : Loc.T("Tách"));
            }
        }

        // ---------- cho lượt chụp ----------

        public void PlayForTest()
        {
            if (!Busy) Deal();
            if (game != null && game.phase == BjPhase.Player) Act(Blackjack.Advice(game));
        }
    }
}
