// Scene lều Đêm Bài (Blackjack) của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.6; dealer Lão Mực: GD_Claude/31_LaoMuc_Dealer.md mục 3, 4.2,
// mốc D3). Prefab Screens/CasinoBlackjack (menu "PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene"). Lõi: Core/Casino/Blackjack.cs.
// Phần chung (bậc cược, hũ, chế độ): CasinoTableScene.
// - Sân khấu (stage, dưới Canvas/Nen, co theo màn như ảnh nền): nền lều → Lão Mực lớp sau → mặt bàn (mép bàn + khay chip) → bài dealer,
//   cỗ bài, chồng chip cược, bài người chơi → Lão Mực lớp trước (tay) → lá đang bay → chữ trên bàn, bong bóng thoại.
// - Lõi tính trước cả ván, màn chỉ DIỄN LẠI theo thứ tự lõi đã chia (Sync): chia 4 lá p-d-p-d (lá thứ hai của dealer úp), lá rút, tách
//   (lá thứ hai bay sang tay 2), lật lá úp, dealer rút, rồi tiền: thắng thì Lão Mực gạt chip từ khay ra (pay), thua thì hai tay vơ
//   chồng chip về khay (take), kèm phản ứng (react_*), bong bóng câu thoại ngắn.
// - Lá bay từ bàn tay Lão Mực (xương tay_pb, sự kiện "bung" của clip deal) tới ô; rig chưa có clip deal thì bay từ cỗ bài.
// - Ván đầu mỗi lần vào lều: Lão Mực xoè bài (shuffle; hình cỗ bài trên nỉ ẩn từ "nhac_bai" tới "dat_bai"). Tách: hai tay gạt
//   (split, lá dạt ở "tach"). Gấp đôi: nhướn mắt xoa tay (double), lá thêm đặt ÚP NẰM NGANG, tới lượt dealer mới lật. Dealer rút
//   khi tổng 12–16: run, đổ mồ hôi (deal_self_tense). Chồng chip theo màu bậc cược (đỏ, xanh dương, xanh lá, vàng).
// - Nút: Chia bài (giá cược / Ván miễn phí / Ván tập), Rút, Dằn, Gấp đôi, Tách; gợi ý chiến thuật cơ bản ("Nên: Rút") bật / tắt bằng
//   nút trong bảng thông tin gập (góc trái dưới, cạnh Cách chơi).
// Mọi vật dựng sẵn trong prefab (8 lá mỗi hàng, 2 chồng chip, bong bóng), không sinh lúc chạy.
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
    public sealed class BlackjackScene : CasinoTableScene
    {
        [Serializable]
        public struct Card
        {
            public RectTransform root;
            public Image face, suit, back;
            public TextMeshProUGUI rank;
        }

        [Serializable]
        public struct HandUi
        {
            public RectTransform root;
            public Card[] cards;
            public TextMeshProUGUI total, result;
            public Image marker;
        }

        [Serializable]
        public struct Stack
        {
            public RectTransform root;
            public Image img;
            public TextMeshProUGUI label;
        }

        // bố cục trên sân khấu (đơn vị canvas, gốc ở mép trên giữa sân khấu 1080 x 1920; mép bàn sau ở y −1000, xem CasinoTablesMenu)
        public const float StageW = 1080, StageH = 1920;
        public static readonly Vector2 DealerRow = new Vector2(0, -1140);
        public const float DealerScale = 0.9f, DealerGap = 74;                       // bài dealer xa người xem hơn nên nhỏ hơn
        public const float HandScale = 1.3f, HandGap = 82, SplitGap = 52, SplitX = 250;  // bài người chơi gần người xem: to, dễ đọc
        public const float HandY = -1475;
        public static readonly Vector2 BetSpot = new Vector2(0, -1300);   // = ô cược CHIP (0, 120) của rig: TableY 1000 + 380 x 0,79
        public static readonly Vector2 WinSpot = new Vector2(96, -1300);
        public static readonly Vector2 TraySpot = new Vector2(131, -1046);  // khay nhà cái (rig: x 166, TRAY_Y 460)
        public static readonly Vector2 OffTable = new Vector2(0, -2000);  // chip rời bàn về phía người chơi

        [SerializeField] RectTransform stage, flyLayer;
        [SerializeField] DealerRig dealerRig;
        [SerializeField] RectTransform deck;
        [SerializeField] Card[] dealer;
        [SerializeField] TextMeshProUGUI dealerTotal;
        [SerializeField] HandUi[] hands;
        [SerializeField] Stack bet, win;
        [SerializeField] RectTransform bubble;
        [SerializeField] TextMeshProUGUI bubbleText;
        [SerializeField] TextMeshProUGUI hint, banner;
        [SerializeField] SketchButton deal, hit, stand, dbl, split, hintToggle;
        [SerializeField] Sprite[] stackSprites; // chồng chip theo bậc cược 0..3: đỏ, xanh dương, xanh lá, vàng

        public override string Title => Loc.T("Đêm Bài");
        protected override string Game => Casino.Blackjack;
        protected override CasinoTable Table => D.Cfg.casino.blackjack;
        protected override bool Busy => game != null && game.phase == BjPhase.Player || anim;

        protected override string HelpText =>
            Loc.T("Rút bài cho tổng gần 21 nhất mà không quá 21. A là 1 hoặc 11, J Q K là 10.") + "\n" +
            Loc.T("Dealer rút tới 17 thì dừng. Blackjack (A + lá 10 ngay hai lá đầu) trả 3:2, thắng trả 1:1, hoà trả lại cược.") + "\n" +
            Loc.T("Gấp đôi: cược thêm bằng cược đầu, nhận đúng một lá. Tách: hai lá cùng điểm tách thành hai tay, mỗi tay một cược.");

        BjGame game;
        bool settled, anim;
        Coroutine syncCo, bubbleCo;
        // những gì đang HIỆN trên bàn (có thể chậm hơn lõi trong lúc diễn)
        int shownDealer, shownHands;
        readonly int[] shownCards = new int[2];
        bool holeOpen, shuffled;
        readonly bool[] ddHidden = new bool[2];   // lá gấp đôi của tay h đang úp nằm ngang (lật ở lượt dealer)
        int winStreak;
        string lastEvent;
        readonly HashSet<string> seenEv = new HashSet<string>();   // sự kiện của clip đang chờ (xoá khi bắt đầu chờ clip mới)
        Vector2 lastStage;

        bool HintOn => !Casino.Of(S).seen.Contains("bjhint:off");

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform stageRt, RectTransform fly, DealerRig rig, RectTransform deckRt, Card[] dealerCards, TextMeshProUGUI dealerSum,
            HandUi[] handList, Stack betStack, Stack winStack, RectTransform bubbleRt, TextMeshProUGUI bubbleLabel, TextMeshProUGUI hintText,
            TextMeshProUGUI bannerText, SketchButton dealBtn, SketchButton hitBtn, SketchButton standBtn, SketchButton dblBtn, SketchButton splitBtn,
            SketchButton hintBtn, Sprite[] stacks)
        {
            stackSprites = stacks;
            stage = stageRt; flyLayer = fly; dealerRig = rig; deck = deckRt; dealer = dealerCards; dealerTotal = dealerSum; hands = handList;
            bet = betStack; win = winStack; bubble = bubbleRt; bubbleText = bubbleLabel; hint = hintText; banner = bannerText;
            deal = dealBtn; hit = hitBtn; stand = standBtn; dbl = dblBtn; split = splitBtn; hintToggle = hintBtn;
        }

        public BjGame GameNow => game;
        public DealerRig Dealer => dealerRig;
        public bool Animating => anim;

        protected override void EnterTable()
        {
            game = null;
            settled = false;
            anim = false;
            shuffled = false;
            winStreak = 0;
            deal.SetOnClick(Deal);
            hit.SetOnClick(() => Act(BjAct.Hit));
            stand.SetOnClick(() => Act(BjAct.Stand));
            dbl.SetOnClick(() => Act(BjAct.Double));
            split.SetOnClick(() => Act(BjAct.Split));
            hintToggle.SetOnClick(ToggleHint);
            banner.text = "";
            if (dealerRig)
            {
                dealerRig.Fired -= OnDealerEvent;
                dealerRig.Fired += OnDealerEvent;
            }
            FitStage();
            ClearTable();
            Draw();
            var mode = Mode;
            if (Guiding) return; // lần đầu: Lão Mực đang dẫn (CasinoGuide), không chào riêng
            if (dealerRig) dealerRig.Play("greet");
            Say(mode == TableMode.Free ? Loc.T("Ván đầu ta khao, thua không mất gì.")
                : mode == TableMode.Practice ? Loc.T("Hôm nay hết ván có thưởng rồi, chơi tập cho vui nhé.")
                : Loc.T("Chào khách! Chọn mức cược rồi bấm Chia bài."), 3f);
        }

        protected override DealerRig StageDealer => dealerRig;

        void OnDestroy()
        {
            if (dealerRig) dealerRig.Fired -= OnDealerEvent;
        }

        void OnDealerEvent(string e)
        {
            lastEvent = e;
            seenEv.Add(e);
        }

        // phát clip và chờ một sự kiện của nó (hoặc clip hết / quá giờ); trả về qua yield
        IEnumerator PlayUntil(string clip, string ev, float maxWait = 1.6f)
        {
            if (!dealerRig || !dealerRig.Has(clip)) yield break;
            seenEv.Clear();
            lastEvent = null;
            bool done = false;
            dealerRig.Play(clip, () => done = true);
            float w = 0;
            while (!seenEv.Contains(ev) && !done && w < maxWait)
            {
                w += Time.deltaTime;
                yield return null;
            }
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

        void Update()
        {
            // sân khấu co theo màn: phủ kín như ảnh nền (đổi cỡ cửa sổ / xoay máy)
            if (stage && stage.parent is RectTransform p && p.rect.size != lastStage) FitStage();
        }

        void FitStage()
        {
            if (!stage || !(stage.parent is RectTransform p)) return;
            lastStage = p.rect.size;
            float s = Mathf.Max(p.rect.width / StageW, p.rect.height / StageH);
            if (s <= 0 || float.IsNaN(s)) s = 1;
            stage.localScale = new Vector3(s, s, 1);
        }

        // ---------- thao tác ----------

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
            App.Save.Save();
            SetInfo(false);   // bảng thông tin gập (đè góc trái bàn) thì đóng khi chia bài
            ClearTable();
            banner.text = mode == TableMode.Free ? Loc.T("Ván miễn phí!") : mode == TableMode.Practice ? Loc.T("Ván tập") : "";
            HideBubble();
            Kick();
        }

        void Act(BjAct a)
        {
            if (anim || game == null || !Blackjack.Can(game, a)) return;
            if (!Blackjack.ActPaid(S, D, game, a, Now))
            {
                NoBalls(Loc.T("Không đủ bi"));
                return;
            }
            App.Audio.Play(a == BjAct.Stand ? "click" : "bet");
            if (game.phase != BjPhase.Done) App.Save.Save();
            if (a == BjAct.Double || a == BjAct.Split) BindBet(true);
            Kick();
        }

        void Kick()
        {
            if (syncCo != null) return;
            syncCo = StartCoroutine(Sync());
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

        // ---------- diễn lại ván theo lõi ----------

        IEnumerator Sync()
        {
            anim = true;
            Draw();
            while (game != null)
            {
                var g = game;
                // chồng chip cược trượt lên ô cược (ván có cược / miễn phí)
                if (shownDealer == 0 && shownCards[0] == 0)
                {
                    if (!shuffled)
                    {
                        shuffled = true;
                        yield return Shuffle();
                    }
                    if (g.mode != TableMode.Practice) yield return SlideBetIn();
                    // chia 4 lá: người - dealer - người - dealer (lá thứ hai của dealer úp)
                    shownHands = 1;
                    for (int i = 0; i < 2; i++)
                    {
                        yield return DealTo(0, shownCards[0]);
                        yield return DealDealer(shownDealer, i == 1);
                    }
                    // nhìn trộm lá úp khi lá ngửa là A hoặc 10
                    if (g.Up.rank == 1 || g.Up.Value == 10) yield return Peek();
                    continue;
                }
                // tách: lá thứ hai bay sang tay 2
                if (g.hands.Count > shownHands)
                {
                    yield return SplitMove();
                    continue;
                }
                // lá rút của từng tay
                int h = Enumerable.Range(0, Mathf.Min(g.hands.Count, hands.Length)).FirstOrDefault(k => shownCards[k] < g.hands[k].cards.Count && shownCards[k] < hands[k].cards.Length);
                if (h < g.hands.Count && shownCards[h] < g.hands[h].cards.Count && shownCards[h] < hands[h].cards.Length)
                {
                    yield return DealTo(h, shownCards[h]);
                    if (g.hands[h].Bust && !ddHidden[h]) Say(Loc.T("Quá 21 rồi, khè khè!"), 1.6f);
                    continue;
                }
                if (g.phase != BjPhase.Done) break;
                // lượt dealer: lật lá úp rồi rút
                if (!holeOpen)
                {
                    yield return Reveal();
                    continue;
                }
                if (shownDealer < g.dealer.Count && shownDealer < dealer.Length)
                {
                    yield return DealDealer(shownDealer, false);
                    continue;
                }
                if (!settled)
                {
                    Settle();
                    Draw();
                    yield return Money();
                }
                break;
            }
            anim = false;
            syncCo = null;
            Draw();
        }

        // một lá tới tay h, ô i
        IEnumerator DealTo(int h, int i)
        {
            var hand = game.hands[h];
            var c = hand.cards[i];
            var ui = hands[h].cards[i];
            // gấp đôi: Lão Mực nhướn mắt xoa tay, lá thêm đặt úp nằm ngang tới lượt dealer
            bool dd = hand.doubled && i == 2;
            if (dd)
            {
                ddHidden[h] = true;
                Say(Loc.T("Chơi lớn hả?"), 1.2f);
                if (dealerRig && dealerRig.Has("double")) yield return Clip("double");
            }
            shownCards[h] = i + 1;
            LayoutHands(false);
            yield return Fly(ui, CardPos(h, i), HandScale, c, dd, "deal", dd ? 90f : 0f);
        }

        IEnumerator DealDealer(int i, bool hidden)
        {
            var c = game.dealer[i];
            var ui = dealer[i];
            shownDealer = i + 1;
            string clip = "deal_self";
            if (i >= 2 && game.phase == BjPhase.Done)
            {
                int t = Blackjack.Total(game.dealer.Take(i).ToList(), out _);
                if (t >= 12 && t <= 16)
                {
                    Say(Loc.T("Hừm..."), 0.8f);
                    clip = "deal_self_tense";   // dễ quá 21: run, đổ mồ hôi
                }
            }
            LayoutDealer(false);
            yield return Fly(ui, DealerPos(i, shownDealer), DealerScale, c, hidden, clip);
            if (shownDealer == game.dealer.Count && holeOpen && Blackjack.Total(game.dealer, out _) > 21)
            {
                Say(Loc.T("Hừ... quá 21."), 1.6f);
                if (dealerRig && dealerRig.Has("bust_self"))
                {
                    App.Audio.Play("mucBoing");
                    yield return Clip("bust_self");
                }
            }
        }

        // lá bay: từ bàn tay Lão Mực (clip deal / deal_self, sự kiện "bung") hoặc từ cỗ bài, cung nhẹ, xoay, đáp, lật nếu là lá ngửa
        // landRot: góc lá lúc nằm (lá gấp đôi nằm ngang 90 độ)
        IEnumerator Fly(Card ui, Vector2 to, float scale, BjCard c, bool hidden, string clip, float landRot = 0)
        {
            bool toDealer = clip.StartsWith("deal_self", StringComparison.Ordinal);
            BindCard(ui, c, true);
            var rt = ui.root;
            Vector3 from = deck ? deck.position : rt.position;
            if (dealerRig && dealerRig.Has(clip))
            {
                yield return PlayUntil(clip, "bung", 1.5f);
                from = dealerRig.BoneWorld("tay_pb");
            }
            App.Audio.Play("deal", 0.8f);
            // bay trên lớp bay (trên tay Lão Mực), tính trong toạ độ thế giới; đáp xong trả về chỗ cũ trong cây (dưới lớp tay)
            int idx = rt.GetSiblingIndex();
            var parent = rt.parent;
            rt.SetParent(flyLayer, false);
            rt.gameObject.SetActive(true);
            Vector3 a = from, b = StageWorld(to);
            Vector3 mid = (a + b) * 0.5f + stage.TransformVector(new Vector3(0, 70, 0));
            float dur = 0.3f, t = 0;
            // lá búng cho người chơi xoay 1–2 vòng; lá Lão Mực tự đặt trước mặt chỉ lượn nhẹ
            float spin = toDealer ? UnityEngine.Random.Range(-25f, 25f) : UnityEngine.Random.Range(1, 3) * (UnityEngine.Random.value < 0.5f ? -360f : 360f);
            while (t < dur)
            {
                t += Time.deltaTime;
                float u = Mathf.Clamp01(t / dur);
                float e = 1 - (1 - u) * (1 - u);
                rt.position = Vector3.Lerp(Vector3.Lerp(a, mid, e), Vector3.Lerp(mid, b, e), e);
                float sc = Mathf.Lerp(0.6f, scale, e);
                rt.localScale = new Vector3(sc, sc, 1);
                rt.localRotation = Quaternion.Euler(0, 0, spin * (1 - e) + landRot * e);
                yield return null;
            }
            rt.SetParent(parent, false);
            rt.SetSiblingIndex(idx);
            rt.anchoredPosition = to;
            rt.localRotation = Quaternion.Euler(0, 0, landRot);
            rt.localScale = new Vector3(scale, scale, 1);
            // đáp: nảy nhẹ
            yield return Pop(rt, scale, 1.06f, 0.08f);
            if (!hidden) yield return Flip(ui, c, scale);
            Draw();
        }

        IEnumerator Pop(RectTransform rt, float baseScale, float peak, float dur)
        {
            float t = 0;
            while (t < dur)
            {
                t += Time.deltaTime;
                float k = Mathf.Sin(Mathf.Clamp01(t / dur) * Mathf.PI);
                float s = baseScale * Mathf.Lerp(1, peak, k);
                rt.localScale = new Vector3(s, s, 1);
                yield return null;
            }
            rt.localScale = new Vector3(baseScale, baseScale, 1);
        }

        // lật: bóp ngang về 0, đổi mặt, bung lại
        IEnumerator Flip(Card ui, BjCard c, float scale)
        {
            var rt = ui.root;
            float t = 0, half = 0.07f;
            while (t < half)
            {
                t += Time.deltaTime;
                rt.localScale = new Vector3(scale * (1 - Mathf.Clamp01(t / half)), scale, 1);
                yield return null;
            }
            BindCard(ui, c, false);
            t = 0;
            while (t < half)
            {
                t += Time.deltaTime;
                rt.localScale = new Vector3(scale * Mathf.Clamp01(t / half), scale, 1);
                yield return null;
            }
            rt.localScale = new Vector3(scale, scale, 1);
        }

        IEnumerator Peek()
        {
            bool bj = game.dealerPeekBj;
            // lá úp nhấc lên một chút như bị hé góc (khớp lúc tay Lão Mực kẹp lá trong clip peek: 0,35 – 0,95 s)
            if (dealerRig && dealerRig.Has("peek"))
            {
                StartCoroutine(LiftHole(0.35f, 0.6f));
                yield return Clip("peek");
            }
            else yield return LiftHole(0f, 0.5f);
            Say(bj ? Loc.T("Ha! Blackjack của ta!") : Loc.T("Hừm... chưa có gì."), 1.4f);
        }

        IEnumerator LiftHole(float delay, float dur)
        {
            if (delay > 0) yield return new WaitForSeconds(delay);
            {
                var rt = dealer[1].root;
                var p0 = rt.anchoredPosition;
                float t = 0;
                while (t < dur)
                {
                    t += Time.deltaTime;
                    float k = Mathf.Sin(Mathf.Clamp01(t / dur) * Mathf.PI);
                    rt.anchoredPosition = p0 + new Vector2(0, 14 * k);
                    rt.localRotation = Quaternion.Euler(0, 0, 6 * k);
                    yield return null;
                }
                rt.anchoredPosition = p0;
                rt.localRotation = Quaternion.identity;
            }
        }

        IEnumerator Reveal()
        {
            // lá gấp đôi úp nằm ngang: lật trước (tới lượt dealer mới biết)
            for (int h = 0; h < hands.Length; h++)
            {
                if (!ddHidden[h] || game.hands.Count <= h || game.hands[h].cards.Count < 3) continue;
                ddHidden[h] = false;
                yield return Flip(hands[h].cards[2], game.hands[h].cards[2], HandScale);
                Draw();
                if (game.hands[h].Bust) Say(Loc.T("Quá 21 rồi, khè khè!"), 1.6f);
                yield return new WaitForSeconds(0.25f);
            }
            holeOpen = true;
            if (dealerRig && dealerRig.Has("reveal")) yield return PlayUntil("reveal", "lat", 1.5f);
            else yield return new WaitForSeconds(0.15f);
            if (game.dealer.Count > 1) yield return Flip(dealer[1], game.dealer[1], DealerScale);
            Draw();
            yield return new WaitForSeconds(0.25f);
        }

        IEnumerator SplitMove()
        {
            if (dealerRig && dealerRig.Has("split"))
            {
                Say(Loc.T("Tách thì tách!"), 1.2f);
                yield return PlayUntil("split", "tach", 1.2f);
            }
            shownHands = 2;
            // lá thứ hai của tay 1 (đã nằm ở tay 1 ô 1) giờ là lá đầu của tay 2
            var from = hands[0].cards[1];
            var to = hands[1].cards[0];
            BindCard(to, game.hands[1].cards[0], false);
            to.root.gameObject.SetActive(true);
            to.root.position = from.root.position;
            to.root.localScale = from.root.localScale;
            from.root.gameObject.SetActive(false);
            shownCards[0] = 1;
            shownCards[1] = 1;
            LayoutHands(true);
            yield return new WaitForSeconds(0.22f);
            Draw();
        }

        // xoè bài đầu phiên: hình cỗ bài trên nỉ ẩn khi Lão Mực nhấc lên (nhac_bai), hiện lại khi đặt xuống (dat_bai)
        IEnumerator Shuffle()
        {
            if (!dealerRig || !dealerRig.Has("shuffle")) yield break;
            Say(Loc.T("Xào bài nào!"), 1.6f);
            seenEv.Clear();
            bool done = false;
            dealerRig.Play("shuffle", () => done = true);
            float w = 0;
            while (!done && w < 4f && !seenEv.Contains("dat_bai"))
            {
                w += Time.deltaTime;
                if (deck && seenEv.Contains("nhac_bai") && deck.gameObject.activeSelf) deck.gameObject.SetActive(false);
                if (seenEv.Contains("go_bai") && !seenEv.Contains("go_bai:am"))
                {
                    seenEv.Add("go_bai:am");
                    App.Audio.Play("deal", 0.9f);
                }
                yield return null;
            }
            if (deck) deck.gameObject.SetActive(true);
            yield return new WaitForSeconds(0.1f);
        }

        // ---------- tiền: trả / vơ chip, phản ứng ----------

        IEnumerator Money()
        {
            var g = game;
            bool anyWin = g.results.Any(r => r > 0), allPush = g.results.All(r => r == 0);
            bool bj = g.results.Any(r => r == 2);
            bool practice = g.mode == TableMode.Practice;
            winStreak = anyWin ? winStreak + 1 : allPush ? winStreak : 0;
            bool outOfPlays = Casino.PlaysLeft(S, D, Game, Now) <= 0 && g.mode == TableMode.Paid;
            if (anyWin)
            {
                Say(bj ? Loc.T("Blackjack?! Hên thôi!") : Pick(Loc.T("Hừ... hên thôi!"), Loc.T("Ván sau ta gỡ."), Loc.T("Chà, khá đấy.")), 2f);
                if (!practice) yield return PayOut();
                yield return ChipsLeave(true);
                yield return WaitClip("pay");
                string react = winStreak >= 3 ? "grumpy" : bj || g.payout >= g.Staked * 3 ? "react_win_big" : "react_win_small";
                if (winStreak >= 3)
                {
                    Say(Loc.T("Ba ván liền?! Xui xẻo!"), 2f);
                    winStreak = 0;
                }
                if (dealerRig) dealerRig.Play(react, outOfPlays ? (Action)(() => Sulk()) : null);
            }
            else if (allPush)
            {
                Say(Loc.T("Hoà. Chẳng ai mất gì."), 1.8f);
                yield return ChipsLeave(false);
                if (dealerRig) dealerRig.Play("react_push", outOfPlays ? (Action)(() => Sulk()) : null);
            }
            else
            {
                Say(g.dealerPeekBj ? Loc.T("Ha! Blackjack của ta!") : Pick(Loc.T("Khè khè, của ta hết!"), Loc.T("Lần sau nhé, khách."), Loc.T("Bàn này ta làm chủ mà.")), 2f);
                if (!practice) yield return TakeIn();
                yield return WaitClip("take");
                if (dealerRig) dealerRig.Play("react_lose", outOfPlays ? (Action)(() => Sulk()) : null);
            }
        }

        void Sulk()
        {
            if (!dealerRig) return;
            dealerRig.Play("sulk");
            Say(Loc.T("Hôm nay thế đủ rồi. Mai ghé, ta còn khối chiêu."), 3f);
        }

        // pay: tay phải gạt chồng chip thắng từ khay ra cạnh chồng cược (theo bàn tay từ giây 0,6 tới sự kiện tra_chip)
        IEnumerator PayOut()
        {
            win.root.gameObject.SetActive(false);
            win.label.text = "";
            if (!dealerRig || !dealerRig.Has("pay"))
            {
                yield return Slide(win, TraySpot, WinSpot, 0.35f);
                yield break;
            }
            lastEvent = null;
            bool done = false;
            dealerRig.Play("pay", () => done = true);
            while (!done)
            {
                float ct = dealerRig.Current == "pay" ? dealerRig.State.ClipTime : 99;
                if (ct >= 0.6f && lastEvent != "tra_chip" && ct < 1.3f)
                {
                    if (!win.root.gameObject.activeSelf) win.root.gameObject.SetActive(true);
                    var hand = StageLocal(dealerRig.BoneWorld("tay_pb"));
                    win.root.anchoredPosition = hand + new Vector2(-34, -40);
                }
                if (lastEvent == "tra_chip" || ct >= 1.3f) break;
                yield return null;
            }
            win.root.gameObject.SetActive(true);
            var p0 = win.root.anchoredPosition;
            yield return Slide(win, p0, WinSpot, 0.12f);
            App.Audio.Play("coin", 0.6f);
        }

        // take: hai bàn tay quây chồng chip (cham_chip) rồi kéo về khay (vo_xong); chip theo giữa hai bàn tay
        IEnumerator TakeIn()
        {
            if (!dealerRig || !dealerRig.Has("take"))
            {
                yield return Slide(bet, bet.root.anchoredPosition, TraySpot, 0.4f);
                bet.root.gameObject.SetActive(false);
                yield break;
            }
            lastEvent = null;
            bool done = false, held = false;
            dealerRig.Play("take", () => done = true);
            Vector2 grip = Vector2.zero;
            while (!done)
            {
                if (lastEvent == "cham_chip" && !held)
                {
                    held = true;
                    grip = bet.root.anchoredPosition - Mid();
                    App.Audio.Play("bet", 0.7f);
                }
                if (held) bet.root.anchoredPosition = Mid() + grip * 0.6f;
                if (lastEvent == "vo_xong") break;
                yield return null;
            }
            // vào khay: mờ đi
            float t = 0;
            var cg = bet.root.GetComponent<CanvasGroup>();
            while (t < 0.2f && cg)
            {
                t += Time.deltaTime;
                cg.alpha = 1 - t / 0.2f;
                yield return null;
            }
            bet.root.gameObject.SetActive(false);
            if (cg) cg.alpha = 1;
        }

        Vector2 Mid() => (StageLocal(dealerRig.BoneWorld("tay_tb")) + StageLocal(dealerRig.BoneWorld("tay_pb"))) * 0.5f + new Vector2(0, -36);

        // chip về phía người chơi (thắng: cả chồng cược + chồng thắng; hoà: chồng cược)
        IEnumerator ChipsLeave(bool both)
        {
            yield return new WaitForSeconds(0.25f);
            var a = bet.root.gameObject.activeSelf ? Slide(bet, bet.root.anchoredPosition, OffTable, 0.35f) : null;
            if (both && win.root.gameObject.activeSelf) StartCoroutine(Slide(win, win.root.anchoredPosition, OffTable + new Vector2(60, 0), 0.38f));
            if (a != null) yield return a;
            bet.root.gameObject.SetActive(false);
            win.root.gameObject.SetActive(false);
        }

        IEnumerator SlideBetIn()
        {
            BindBet(false);
            bet.root.gameObject.SetActive(true);
            App.Audio.Play("bet", 0.8f);
            yield return Slide(bet, OffTable, BetSpot, 0.25f);
            if (game != null && game.mode == TableMode.Paid && tier >= 2 && dealerRig && dealerRig.Has("bet_watch"))
            {
                Say(Loc.T("Chơi lớn hả?"), 1.2f);
                yield return Clip("bet_watch");
            }
        }

        IEnumerator Slide(Stack s, Vector2 from, Vector2 to, float dur)
        {
            s.root.gameObject.SetActive(true);
            float t = 0;
            while (t < dur)
            {
                t += Time.deltaTime;
                float u = Mathf.Clamp01(t / dur);
                float e = 1 - (1 - u) * (1 - u) * (1 - u);
                s.root.anchoredPosition = Vector2.Lerp(from, to, e);
                yield return null;
            }
            s.root.anchoredPosition = to;
        }

        // chờ clip đang phát (nếu đúng là clip đó) hết, tối đa 3 giây
        IEnumerator WaitClip(string name)
        {
            float t = 0;
            while (dealerRig && dealerRig.Current == name && t < 3f)
            {
                t += Time.deltaTime;
                yield return null;
            }
        }

        IEnumerator Clip(string name)
        {
            if (!dealerRig) yield break;
            bool done = false;
            dealerRig.Play(name, () => done = true);
            float t = 0;
            while (!done && t < 6f)
            {
                t += Time.deltaTime;
                yield return null;
            }
        }

        // chỗ "anchored" trên sân khấu (gốc ở mép trên giữa) ra toạ độ thế giới
        Vector3 StageWorld(Vector2 anchored) =>
            stage.TransformPoint(new Vector3(anchored.x, anchored.y + stage.rect.height * (1 - stage.pivot.y), 0));

        Vector2 StageLocal(Vector3 world)
        {
            var p = (Vector2)stage.InverseTransformPoint(world);
            // gốc toạ độ của các vật trên sân khấu ở mép trên giữa (neo (0.5, 1))
            return p - new Vector2(0, stage.rect.height * (1 - stage.pivot.y));
        }

        void BindBet(bool bump)
        {
            if (game == null) return;
            if (stackSprites != null && stackSprites.Length > 0)
            {
                var sp = stackSprites[Mathf.Clamp(game.tier, 0, stackSprites.Length - 1)];
                if (sp)
                {
                    bet.img.sprite = sp;
                    win.img.sprite = sp;
                }
            }
            int staked = game.Staked;
            bet.label.text = game.mode == TableMode.Paid ? Loc.F("{0} bi", NumFmt.Short(staked)) : game.mode == TableMode.Free ? Loc.T("miễn phí") : "";
            if (bump && bet.root.gameObject.activeSelf) StartCoroutine(Pop(bet.root, 1f, 1.15f, 0.16f));
        }

        // ---------- bong bóng thoại ----------

        static string Pick(params string[] lines) => lines[UnityEngine.Random.Range(0, lines.Length)];

        void Say(string text, float secs)
        {
            if (!bubble) return;
            if (bubbleCo != null) StopCoroutine(bubbleCo);
            CasinoGuide.Mumble(); // Lão Mực lầm bầm
            bubbleCo = StartCoroutine(SayCo(text, secs));
        }

        IEnumerator SayCo(string text, float secs)
        {
            bubbleText.text = text;
            bubble.gameObject.SetActive(true);
            yield return Pop(bubble, 1f, 1.08f, 0.12f);
            yield return new WaitForSeconds(secs);
            bubble.gameObject.SetActive(false);
            bubbleCo = null;
        }

        void HideBubble()
        {
            if (bubbleCo != null) StopCoroutine(bubbleCo);
            bubbleCo = null;
            if (bubble) bubble.gameObject.SetActive(false);
        }

        // ---------- vẽ ----------

        static string RankText(int r) => r == 1 ? "A" : r == 11 ? "J" : r == 12 ? "Q" : r == 13 ? "K" : r.ToString();
        static readonly Elem[] Suits = { Elem.Kim, Elem.Moc, Elem.Thuy, Elem.Hoa };

        static void BindCard(Card ui, BjCard? c, bool hidden)
        {
            if (c == null)
            {
                ui.root.gameObject.SetActive(false);
                return;
            }
            ui.back.gameObject.SetActive(hidden);
            ui.rank.gameObject.SetActive(!hidden);
            ui.suit.gameObject.SetActive(!hidden);
            if (hidden) return;
            var e = Suits[Mathf.Clamp(c.Value.suit, 0, 3)];
            ui.rank.text = RankText(c.Value.rank);
            ui.rank.color = Color.Lerp(Theme.Of(e), Theme.Ink, 0.35f);
            Theme.SetSprite(ui.suit, App.Art.Icon(ElemIcon(e)));
        }

        Vector2 DealerPos(int i, int n) => DealerRow + new Vector2((i - (n - 1) * 0.5f) * DealerGap, 0);

        Vector2 CardPos(int h, int i)
        {
            bool sp = shownHands > 1;
            int n = Mathf.Max(1, shownCards[h]);
            float cx = sp ? (h == 0 ? -SplitX : SplitX) : 0;
            float gap = sp ? SplitGap : HandGap;
            return new Vector2(cx + (i - (n - 1) * 0.5f) * gap, HandY);
        }

        // dời các lá đang hiện về chỗ mới khi thêm lá (giữ hàng cân giữa); lá cuối đang bay tự tới chỗ
        void LayoutDealer(bool all)
        {
            for (int i = 0; i < shownDealer - (all ? 0 : 1); i++) StartCoroutine(MoveTo(dealer[i].root, DealerPos(i, shownDealer), 0.15f));
        }

        void LayoutHands(bool all)
        {
            for (int h = 0; h < hands.Length; h++)
            for (int i = 0; i < shownCards[h]; i++)
            {
                bool last = !all && i == shownCards[h] - 1;
                if (last) continue;
                StartCoroutine(MoveTo(hands[h].cards[i].root, CardPos(h, i), 0.15f));
            }
        }

        static IEnumerator MoveTo(RectTransform rt, Vector2 to, float dur)
        {
            var from = rt.anchoredPosition;
            float t = 0;
            while (t < dur)
            {
                t += Time.deltaTime;
                rt.anchoredPosition = Vector2.Lerp(from, to, Mathf.SmoothStep(0, 1, t / dur));
                yield return null;
            }
            rt.anchoredPosition = to;
        }

        void ClearTable()
        {
            shownDealer = 0;
            shownHands = 1;
            shownCards[0] = shownCards[1] = 0;
            holeOpen = false;
            ddHidden[0] = ddHidden[1] = false;
            if (deck) deck.gameObject.SetActive(true);
            foreach (var c in dealer)
            {
                c.root.gameObject.SetActive(false);
                c.root.localRotation = Quaternion.identity;
            }
            foreach (var h in hands)
            foreach (var c in h.cards)
            {
                c.root.gameObject.SetActive(false);
                c.root.localRotation = Quaternion.identity;
            }
            bet.root.gameObject.SetActive(false);
            win.root.gameObject.SetActive(false);
        }

        void Draw()
        {
            bool live = game != null && game.phase == BjPhase.Player && !anim;
            // tổng điểm dealer: chỉ tính các lá đang hiện ngửa
            if (game == null || shownDealer == 0) dealerTotal.text = "";
            else
            {
                var vis = game.dealer.Take(shownDealer).ToList();
                if (!holeOpen && vis.Count > 1) dealerTotal.text = Loc.F("Dealer: {0} + ?", vis[0].rank == 1 ? 11 : vis[0].Value);
                else
                {
                    int t = Blackjack.Total(vis, out _);
                    dealerTotal.text = t > 21 ? Loc.F("Dealer: {0} (quá 21)", t) : Loc.F("Dealer: {0}", t);
                }
            }
            // tay người chơi
            for (int h = 0; h < hands.Length; h++)
            {
                var ui = hands[h];
                var hand = game != null && h < game.hands.Count && h < shownHands ? game.hands[h] : null;
                int n = hand != null ? Mathf.Min(shownCards[h], hand.cards.Count) : 0;
                ui.marker.gameObject.SetActive(game != null && game.phase == BjPhase.Player && shownHands > 1 && game.active == h);
                if (ui.marker.gameObject.activeSelf) ui.marker.rectTransform.anchoredPosition = new Vector2(shownHands > 1 ? (h == 0 ? -SplitX : SplitX) : 0, HandY - 142);
                if (hand == null || n == 0)
                {
                    ui.total.text = h == 0 && game == null ? Loc.F("Cược {0} bi", BetNow) : "";
                    ui.result.text = "";
                    continue;
                }
                bool hid = ddHidden[h] && n >= 3;
                var vis = hand.cards.Take(n).Where((x, k) => !(hid && k == 2)).ToList();
                int tot = Blackjack.Total(vis, out bool soft);
                float cx = shownHands > 1 ? (h == 0 ? -SplitX : SplitX) : 0;
                ui.total.rectTransform.anchoredPosition = new Vector2(cx, HandY - 124);
                ui.result.rectTransform.anchoredPosition = new Vector2(cx, HandY + 118);
                ui.total.text = (hid ? Loc.F("{0} điểm + ?", tot) : Loc.F("{0} điểm", tot)) + (soft && tot < 21 && !hid ? " " + Loc.T("(mềm)") : "") +
                                (hand.doubled ? " · " + Loc.T("gấp đôi") : "");
                if (game.phase == BjPhase.Done && settled && h < game.results.Length)
                {
                    int r = game.results[h];
                    ui.result.text = r == 2 ? Loc.T("Blackjack!") : r == 1 ? Loc.T("Thắng") : r == 0 ? Loc.T("Hoà") : hand.Bust ? Loc.T("Quá 21") : Loc.T("Thua");
                    ui.result.color = r > 0 ? Theme.Yellow : r == 0 ? Color.white : new Color(1f, 0.55f, 0.5f);
                }
                else ui.result.text = tot > 21 ? Loc.T("Quá 21") : "";
            }
            // nút
            deal.gameObject.SetActive(!live && !(game != null && game.phase == BjPhase.Player));
            deal.Locked = anim;
            var mode = Mode;
            deal.SetText(mode == TableMode.Free ? Loc.T("Ván miễn phí") : mode == TableMode.Practice ? Loc.T("Ván tập")
                : Loc.F("Chia bài · {0} bi", BetNow));
            deal.SetRole(mode == TableMode.Practice ? BtnColor.Blue : BtnColor.Green);
            bool playing = game != null && game.phase == BjPhase.Player;
            foreach (var (b, a) in new[] { (hit, BjAct.Hit), (stand, BjAct.Stand), (dbl, BjAct.Double), (split, BjAct.Split) })
            {
                b.gameObject.SetActive(playing);
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
            if (anim) return;
            if (game == null || game.phase == BjPhase.Done) Deal();
            else if (game.phase == BjPhase.Player) Act(Blackjack.Advice(game));
        }
    }
}
