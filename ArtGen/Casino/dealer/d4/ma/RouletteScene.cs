// Scene lều Vòng Xoay Ngũ Hành (Roulette) của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.7; dealer Lão Mực: GD_Claude/31 mục 4.3,
// mốc D4). Prefab Screens/CasinoRoulette (menu "PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene"). Lõi: Core/Casino/Roulette.cs
// (chọn ô ra theo tỉ lệ trong cấu hình), Core/Casino/RouletteBall.cs (mô phỏng viên bi). Phần chung: CasinoTableScene.
// - Sân khấu (stage, dưới Canvas/Nen, co theo màn như ảnh nền): nền lều → Lão Mực lớp sau → mặt bàn (mép bàn + khay chip + nỉ) → bảng
//   cược nỉ (hàng = 5 hệ, cột = số 1–5, góc = Sao Vàng; chạm ô là đặt một chip) → chip → bánh xe to sát người chơi (lòng chảo, mâm
//   xoay, trục, viên bi, nửa vành gần) → Lão Mực lớp trước (tay) → bi đang bay → chữ, bong bóng thoại.
// - LÕI QUYẾT ĐỊNH Ô RA, VẬT LÝ CHỈ DIỄN: bấm Quay thì lõi chọn ô và tính tiền ngay (Roulette.PlayAs). Lúc Lão Mực quất mâm,
//   RouletteBall.Plan tìm một cú thả bi thật (chỉ đổi lực thả) mà mô phỏng cho bi nằm đúng ô đó, màn phát lại đường đi đã ghi:
//   bi chạy quanh vách, chậm dần, rơi xuống sườn dốc, va mấu chắn, lách cách qua vách ngăn rồi nằm vào ô. Không có khung nào "kéo" bi.
// - Mâm luôn quay chậm; Lão Mực quất thì mâm tăng tốc (trong lúc tăng tốc pha mâm được nắn tối đa vài ô cho khớp cú thả), sau đó
//   chậm dần theo đúng công thức của mô phỏng (RlTrack.Rotor).
// - Lão Mực: mời đặt cửa (rl_invite), "hết đặt" (rl_no_more), quất mâm + búng bi (rl_spin, sự kiện quay / tha_bi), dõi theo bi
//   (rl_watch, kéo thời gian theo góc bi), chỉ ô ra (rl_point), vơ chip thua (take), gạt chip thắng (pay), phản ứng (react_*).
//   Rig thiếu clip nào thì màn tự bỏ qua bước diễn đó, không kẹt.
// Mọi vật dựng sẵn trong prefab (36 ô cược, 8 chip, 2 chồng chip, bong bóng), không sinh lúc chạy.
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
    public sealed class RouletteScene : CasinoTableScene
    {
        [Serializable]
        public struct Cell
        {
            public RectTransform root;
            public Button button;
            public Image frame;
            public TextMeshProUGUI label;
            public Color color;   // màu gốc của ô
        }

        [Serializable]
        public struct Chip
        {
            public RectTransform root;
            public Image img;
            public CanvasGroup group;
        }

        [Serializable]
        public struct Stack
        {
            public RectTransform root;
            public Image img;
            public TextMeshProUGUI label;
        }

        // ---- bố cục trên sân khấu (đơn vị canvas, gốc ở mép trên giữa sân khấu 1080 x 1920; xem CasinoTablesMenu.BuildRoulette) ----
        public const float StageW = 1080, StageH = 1920;
        public const float RigScale = 0.70f, RimY = 650;                          // Lão Mực nhỏ hơn lều bài (0,79) để chừa bàn cho bánh xe
        public static readonly Vector2 WheelCenter = new Vector2(0, -1500);       // tâm mặt phẳng ô của bánh xe
        public const float WheelR = 320;                                          // bán kính vành ngoài
        public static readonly Vector2 BetSpot = new Vector2(0, -916);            // ô gom chip = CHIP (0, 120) của rig: 650 + 380 x 0,7
        public static readonly Vector2 WinSpot = new Vector2(84, -916);
        public static readonly Vector2 TraySpot = new Vector2(116, -678);         // khay nhà cái (rig: x 166, TRAY_Y 460)
        public const float GridX0 = -450, GridTop = -775, HeadW = 150, HeadH = 75, CellW = 150, CellH = 80;
        const float LaneX = 430;                                                  // chip về tay người chơi đi dọc hai bên bánh xe

        public static Vector2 CellPos(RlKind k, int v)
        {
            float rowY(int e) => GridTop - HeadH - (e + 0.5f) * CellH;
            float colX(int n) => GridX0 + HeadW + (n + 0.5f) * CellW;
            switch (k)
            {
                case RlKind.Elem: return new Vector2(GridX0 + HeadW * 0.5f, rowY(v));
                case RlKind.Num: return new Vector2(colX(v - 1), GridTop - HeadH * 0.5f);
                case RlKind.Single: return new Vector2(colX(v % 5), rowY(v / 5));
                default: return new Vector2(GridX0 + HeadW * 0.5f, GridTop - HeadH * 0.5f);
            }
        }

        [SerializeField] RectTransform stage, flyLayer;
        [SerializeField] DealerRig dealerRig;
        [SerializeField] CanvasGroup layout;
        [SerializeField] Cell[] singles, elems, nums;
        [SerializeField] Cell star;
        [SerializeField] Chip[] chips;
        [SerializeField] Stack win;
        [SerializeField] RectTransform wheel, rotor, ball, flyBall, marker;
        [SerializeField] RectTransform bubble;
        [SerializeField] TextMeshProUGUI bubbleText, banner;
        [SerializeField] SketchButton clear, spin;
        [SerializeField] Sprite[] chipSprites, stackSprites;   // theo bậc cược 0..3: đỏ, xanh dương, xanh lá, vàng

        public override string Title => Loc.T("Vòng Xoay Ngũ Hành");
        protected override string Game => Casino.Roulette;
        protected override CasinoTable Table => C;
        protected override bool Busy => spinning;

        static RouletteConfig C => D.Cfg.casino.roulette;

        protected override string HelpText
        {
            get
            {
                Roulette.RtpRange(C, out double lo, out double hi);
                string rtp = Math.Abs(hi - lo) < 1e-6
                    ? Loc.F("Mọi cửa hoàn trả {0}%.", (lo * 100).ToString("0.0"))
                    : Loc.F("Hoàn trả từ {0}% tới {1}% tuỳ cửa.", (lo * 100).ToString("0.0"), (hi * 100).ToString("0.0"));
                return Loc.T("Bánh xe có 26 ô: 5 hệ, mỗi hệ số 1 tới 5, và một ô Sao Vàng. Đặt chip lên bảng cược rồi bấm Quay; viên bi nằm ở ô nào thì cửa trúng ô đó thắng.") + "\n" +
                       Loc.F("Hệ (cột đầu): trúng một trong 5 ô của hệ, trả {0}:1. Số (hàng đầu): trúng một trong 5 ô cùng số, trả {1}:1. Ô đơn: trả {2}:1. Sao Vàng: trả {3}:1, cược từ bậc {4} được thêm mảnh tướng khách mời.",
                           C.elemPays, C.numPays, C.singlePays, C.starPays, C.starTier + 1) + "\n" +
                       Loc.F("Tối đa {0} chip mỗi vòng.", C.chips) + " " + rtp;
            }
        }

        readonly List<RlBet> bets = new List<RlBet>();
        bool spinning;
        int lastPocket = -1;
        bool dimmed;                 // đang báo ô ra: ô không trúng lùi tối (tới hết phần trả tiền)
        int winStreak;
        Coroutine bubbleCo;
        readonly Coroutine[] chipCo = new Coroutine[16];
        string lastEvent;
        readonly HashSet<string> seenEv = new HashSet<string>();
        Vector2 lastStage;

        // ---- mâm và bi ----
        enum Rot { Idle, Whip, Track }
        Rot rot;
        float clock;                 // giây của màn (theo Time.deltaTime: lượt chụp khoá nhịp vẫn đúng)
        double rotA0;                // góc mâm ở mốc rotT0
        float rotT0;
        double whipPrev, whipShift;  // tốc độ mâm trước cú quất; pha phải nắn thêm (rad) tới lúc bi vào
        float whipGap;               // giây từ cú quất tới lúc bi vào đường chạy
        const float WhipRamp = 0.32f, Flight = 0.26f;
        RlTrack track;
        float entryT;                // mốc bi vào đường chạy
        int hitAt;
        enum BallAt { Rest, Hidden, Flight, Roll }
        BallAt ballAt;
        double idleBallAngle;        // bi nằm ở góc này trong hệ mâm khi chưa có cú thả nào
        Vector3 flightFrom;
        float flightT0;
        bool watching;

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform stageRt, RectTransform fly, DealerRig rig, CanvasGroup layoutGroup, Cell[] singleCells, Cell[] elemCells,
            Cell[] numCells, Cell starCell, Chip[] chipPool, Stack winStack, RectTransform wheelRt, RectTransform rotorRt, RectTransform ballRt,
            RectTransform flyBallRt, RectTransform markerRt, RectTransform bubbleRt, TextMeshProUGUI bubbleLabel, TextMeshProUGUI bannerText,
            SketchButton clearBtn, SketchButton spinBtn, Sprite[] chipSp, Sprite[] stackSp)
        {
            stage = stageRt; flyLayer = fly; dealerRig = rig; layout = layoutGroup; singles = singleCells; elems = elemCells; nums = numCells;
            star = starCell; chips = chipPool; win = winStack; wheel = wheelRt; rotor = rotorRt; ball = ballRt; flyBall = flyBallRt;
            marker = markerRt; bubble = bubbleRt; bubbleText = bubbleLabel; banner = bannerText; clear = clearBtn; spin = spinBtn;
            chipSprites = chipSp; stackSprites = stackSp;
        }

        public DealerRig Dealer => dealerRig;
        public bool Spinning => spinning;
        public RlTrack TrackNow => track;
        public int LastPocket => lastPocket;

        protected override void EnterTable()
        {
            bets.Clear();
            spinning = false;
            lastPocket = -1;
            winStreak = 0;
            watching = false;
            track = null;
            rot = Rot.Idle;
            rotA0 = UnityEngine.Random.value * Math.PI * 2;
            rotT0 = clock;
            idleBallAngle = (UnityEngine.Random.Range(0, RouletteWheel.Slots) + 0.5) * RouletteWheel.Step;
            ballAt = BallAt.Rest;
            for (int i = 0; i < singles.Length; i++)
            {
                int k = i;
                Bind(singles[i], () => Add(RlKind.Single, k));
            }
            for (int i = 0; i < elems.Length; i++)
            {
                int k = i;
                Bind(elems[i], () => Add(RlKind.Elem, k));
            }
            for (int i = 0; i < nums.Length; i++)
            {
                int k = i + 1;
                Bind(nums[i], () => Add(RlKind.Num, k));
            }
            Bind(star, () => Add(RlKind.Star, 0));
            foreach (var c in elems) c.label.text = "×" + C.elemPays;
            for (int i = 0; i < nums.Length; i++) nums[i].label.text = (i + 1) + " <size=62%>×" + C.numPays + "</size>";
            star.label.text = "×" + C.starPays;
            clear.SetOnClick(ClearBets);
            spin.SetOnClick(Spin);
            if (dealerRig)
            {
                dealerRig.Fired -= OnDealerEvent;
                dealerRig.Fired += OnDealerEvent;
            }
            foreach (var c in chips) c.root.gameObject.SetActive(false);
            win.root.gameObject.SetActive(false);
            marker.gameObject.SetActive(false);
            flyBall.gameObject.SetActive(false);
            if (layout) layout.alpha = 1;
            FitStage();
            PlaceWheel();
            Draw();
            var mode = Mode;
            if (dealerRig) dealerRig.Play("greet", () => { if (!spinning && bets.Count == 0 && dealerRig) dealerRig.Play("rl_invite"); });
            Say(mode == TableMode.Free ? Loc.T("Vòng đầu ta khao, trượt không mất gì.")
                : mode == TableMode.Practice ? Loc.T("Hôm nay hết vòng có thưởng rồi, quay tập cho vui nhé.")
                : Loc.T("Đặt chip vào hệ, vào số, hay liều một ô. Bi dừng đâu, ta trả đó."), 3.2f);
        }

        static void Bind(Cell c, Action click)
        {
            c.button.onClick.RemoveAllListeners();
            c.button.onClick.AddListener(() => click());
        }

        void OnDestroy()
        {
            if (dealerRig) dealerRig.Fired -= OnDealerEvent;
        }

        void OnDealerEvent(string e)
        {
            lastEvent = e;
            seenEv.Add(e);
        }

        protected override void OnTierChanged()
        {
            for (int i = 0; i < bets.Count && i < chips.Length; i++) chips[i].img.sprite = ChipSprite();
            Draw();
        }

        Sprite ChipSprite() => chipSprites != null && chipSprites.Length > 0 ? chipSprites[Mathf.Clamp(PlayTier, 0, chipSprites.Length - 1)] : null;
        Sprite StackSprite() => stackSprites != null && stackSprites.Length > 0 ? stackSprites[Mathf.Clamp(PlayTier, 0, stackSprites.Length - 1)] : null;

        // ---------- đặt chip ----------

        int Count(RlKind k, int v, int upTo) => bets.Take(upTo).Count(b => b.kind == k && (k == RlKind.Star || b.v == v));

        // chip thứ i nằm ở ô của nó, chồng lệch dần nếu ô đã có chip
        Vector2 ChipPos(int i)
        {
            var b = bets[i];
            int under = Count(b.kind, b.v, i);
            return CellPos(b.kind, b.kind == RlKind.Star ? 0 : b.v) + new Vector2(50 + under * 7, 12 + under * 9);   // góc trên phải của ô, không che số
        }

        void Add(RlKind k, int v)
        {
            if (spinning) return;
            int max = Mathf.Min(C.chips, chips.Length);
            if (bets.Count >= max)
            {
                App.Toasts.Show(Loc.F("Tối đa {0} chip mỗi vòng", max), Icon("info"));
                return;
            }
            if (lastPocket >= 0)
            {
                lastPocket = -1;
                marker.gameObject.SetActive(false);
            }
            bets.Add(new RlBet { kind = k, v = v });
            int i = bets.Count - 1;
            var c = chips[i];
            c.img.sprite = ChipSprite();
            c.group.alpha = 1;
            c.root.localScale = Vector3.one;
            var to = ChipPos(i);
            float lane = to.x >= 0 ? LaneX : -LaneX;   // chip vào bàn dọc làn bên cạnh bánh xe (không chui qua dưới bánh xe)
            MoveChip(i, Slide(c.root, new Vector2(lane, -2000), to, 0.26f, null, new Vector2(lane, to.y - 80)));
            App.Audio.Play("bet", 0.8f, 1f + bets.Count * 0.05f);
            if (dealerRig && dealerRig.IsIdle || dealerRig && dealerRig.Current == "rl_invite")
            {
                if (k == RlKind.Star)
                {
                    Say(Loc.T("Sao Vàng? Gan đấy."), 1.6f);
                    dealerRig.Play("bet_watch");
                }
                else if (bets.Count == 1) dealerRig.Play("bet_watch");
            }
            Draw();
        }

        void ClearBets()
        {
            if (spinning || bets.Count == 0) return;
            for (int i = 0; i < bets.Count && i < chips.Length; i++) MoveChip(i, SlideAway(chips[i], 0.2f));
            bets.Clear();
            App.Audio.Play("click");
            Draw();
        }

        void Spin()
        {
            if (spinning) return;
            if (bets.Count == 0)
            {
                App.Toasts.Show(Loc.T("Đặt ít nhất một chip"), Icon("info"));
                return;
            }
            var mode = Mode;
            int playTier = PlayTier;
            // LÕI chọn ô ra và tính tiền ngay ở đây; phần sau chỉ diễn
            var r = Roulette.PlayAs(S, D, bets, tier, mode, Now, rng, out var jar, out var extra, out var why);
            if (r == null)
            {
                NoBalls(why);
                return;
            }
            App.Save.Save();
            SetInfo(false);
            StartCoroutine(Run(r, mode, playTier, jar, extra));
        }

        // ---------- một vòng quay ----------

        IEnumerator Run(RlSpin r, TableMode mode, int playTier, JarResult jar, List<Reward> extra)
        {
            spinning = true;
            lastPocket = -1;
            marker.gameObject.SetActive(false);
            HideBubble();
            Draw();
            banner.text = mode == TableMode.Free ? Loc.T("Vòng miễn phí!") : mode == TableMode.Practice ? Loc.T("Vòng tập") : Loc.T("Hết đặt!");
            // hết đặt: Lão Mực xua tay, nhặt bi khỏi ô cũ
            Say(Loc.T("Hết đặt!"), 1.0f);
            StartCoroutine(PopBallOut());
            yield return Clip("rl_no_more", 0.62f);   // xua tay xong (0,42 s) là quất mâm luôn

            // quất mâm + búng bi
            int slot = RouletteWheel.SlotOf(r.pocket);
            bool act = dealerRig && dealerRig.Has("rl_spin");
            float gap = (act ? EventGap("rl_spin", "quay", "tha_bi", 0.6f) : 0.3f) + Flight;
            seenEv.Clear();
            if (act)
            {
                dealerRig.Play("rl_spin");
                yield return WaitEvent("quay", 2.5f);
            }
            Whip(slot, gap);
            App.Audio.Play("whoosh", 0.9f);
            if (act) yield return WaitEvent("tha_bi", gap - Flight + 0.25f);
            else yield return new WaitForSeconds(gap - Flight);
            // bi bay từ bàn tay tới điểm vào đường chạy, tới đúng mốc entryT
            if (clock < entryT - 0.04f)
            {
                flightFrom = act ? dealerRig.BoneWorld("tay_pb") : StageWorld(TraySpot);
                flightT0 = clock;
                ballAt = BallAt.Flight;
            }
            App.Audio.Play("launch", 0.5f, 1.3f);
            banner.text = mode == TableMode.Free ? Loc.T("Vòng miễn phí!") : mode == TableMode.Practice ? Loc.T("Vòng tập") : Loc.T("Bánh xe đang quay...");
            if (layout) StartCoroutine(Fade(layout, 0.62f, 0.3f));
            while (clock < entryT) yield return null;

            // bi lăn: Update phát lại đường đi; Lão Mực dõi theo
            float watchFrom = entryT + 0.35f;
            float reveal = entryT + track.capture + 0.45f;
            while (clock < reveal)
            {
                if (!watching && clock >= watchFrom && dealerRig && dealerRig.Has("rl_watch")) watching = true;
                yield return null;
            }

            // ô ra
            watching = false;
            if (dealerRig) dealerRig.EndScrub();
            lastPocket = r.pocket;
            dimmed = true;
            if (layout) StartCoroutine(Fade(layout, 1f, 0.2f));
            string name = r.pocket == Roulette.StarPocket ? Loc.T("Sao Vàng") : Elements.Name(Roulette.ElemOf(r.pocket)) + " " + Roulette.NumOf(r.pocket);
            int net = mode == TableMode.Paid ? r.payout - r.staked : mode == TableMode.Free ? Casino.FreeWin(r.payout, r.staked) : 0;
            banner.text = name + " · " + (r.wins.Count == 0
                ? (mode == TableMode.Practice ? Loc.T("trượt (vòng tập)") : mode == TableMode.Free ? Loc.T("trượt, không mất gì") : Loc.F("trượt · −{0} bi", r.staked))
                : mode == TableMode.Practice ? Loc.F("trúng {0} cửa (vòng tập)", r.wins.Count)
                : Loc.F("trúng {0} cửa · {1} bi", r.wins.Count, net >= 0 ? "+" + net : net.ToString()));
            PlaceMarker(r.pocket);
            Draw();
            Say(Loc.F("{0}!", name), 1.6f);
            if (r.wins.Count == 0) App.Audio.Play("stamp", 0.5f);
            if (dealerRig && dealerRig.Has("rl_point"))
            {
                yield return PlayUntil("rl_point", "chi", 1.2f);
                yield return new WaitForSeconds(0.5f);   // giữ dáng chỉ một nhịp cho người chơi kịp nhìn ô ra
            }
            else yield return new WaitForSeconds(0.5f);

            yield return Money(r, mode, playTier, net);
            spinning = false;
            dimmed = false;
            bets.Clear();
            AfterRound(net, mode == TableMode.Paid ? jar : null, extra);
            Draw();
        }

        // cú quất: mâm tăng tốc từ tốc độ hiện tại lên OmegaSpin; tìm cú thả bi nằm đúng ô (lõi đã chọn) cho góc mâm lúc bi vào
        void Whip(int slot, float gap)
        {
            double a = RotorNow(), w = RotorSpeedNow();
            rot = Rot.Whip;
            rotA0 = a;
            rotT0 = clock;
            whipPrev = w;
            whipGap = gap;
            whipShift = 0;
            double natural = WhipAngle(gap);          // góc mâm lúc bi vào nếu không nắn pha
            track = RouletteBall.Plan(slot, natural, RouletteBall.OmegaSpin, rng, 3);
            whipShift = track != null ? track.rotor0 - natural : 0;
            entryT = clock + gap;
            hitAt = 0;
        }

        // góc mâm sau t giây kể từ cú quất (tốc độ trượt mượt từ whipPrev lên OmegaSpin trong WhipRamp giây, rồi giữ) + phần nắn pha
        double WhipAngle(float t)
        {
            double u = Mathf.Clamp01(t / WhipRamp);
            double a = rotA0 + whipPrev * Math.Min(t, WhipRamp) + (RouletteBall.OmegaSpin - whipPrev) * WhipRamp * (u * u * u - u * u * u * u * 0.5);
            if (t > WhipRamp) a += RouletteBall.OmegaSpin * (t - WhipRamp);
            float s = Mathf.Clamp01(t / Mathf.Max(0.05f, whipGap));
            return a + whipShift * (s * s * (3 - 2 * s));
        }

        double RotorNow()
        {
            switch (rot)
            {
                case Rot.Whip: return WhipAngle(clock - rotT0);
                case Rot.Track: return track.Rotor(clock - entryT);
                default: return rotA0 + RouletteBall.OmegaIdle * (clock - rotT0);
            }
        }

        double RotorSpeedNow() => rot == Rot.Track ? track.RotorSpeed(clock - entryT) : rot == Rot.Whip ? RouletteBall.OmegaSpin : RouletteBall.OmegaIdle;

        void Update()
        {
            // sân khấu co theo màn: phủ kín như ảnh nền (đổi cỡ cửa sổ / xoay máy)
            if (stage && stage.parent is RectTransform p && p.rect.size != lastStage) FitStage();
            clock += Time.deltaTime;
            if (rot == Rot.Whip && clock >= entryT && track != null)
            {
                rot = Rot.Track;
                if (ballAt == BallAt.Flight || ballAt == BallAt.Hidden) ballAt = BallAt.Roll;
            }
            PlaceWheel();
            if (ballAt == BallAt.Roll && track != null)
            {
                float t = clock - entryT;
                while (hitAt < track.hits.Count && track.hits[hitAt].t <= t) Sound(track.hits[hitAt++]);
            }
            if (watching && dealerRig && track != null && (ballAt == BallAt.Roll || ballAt == BallAt.Rest))
            {
                track.Sample(clock - entryT, out float bx, out float by, out _);
                // rl_watch dài 2 giây cho một vòng bi: t = 0 bi ở góc 40°, bi đi theo chiều kim đồng hồ khi t tăng
                float deg = Mathf.Atan2(by, bx) * Mathf.Rad2Deg;
                float u = Mathf.Repeat((40f - deg) / 360f, 1f);
                dealerRig.Scrub("rl_watch", u * 2f, Time.deltaTime);
            }
        }

        void Sound(RlHit h)
        {
            switch (h.kind)
            {
                case RlHitKind.Roll: App.Audio.Play("peg", 0.08f + 0.16f * h.power, 0.55f + 0.5f * h.power); break;
                case RlHitKind.Diamond:
                    App.Audio.Play("peg", 0.55f + 0.3f * h.power, 0.8f);
                    Haptics.Play(Haptic.UiTap);
                    break;
                case RlHitKind.Fret: App.Audio.Play("peg", 0.3f + 0.4f * h.power, 1.35f + 0.3f * h.power); break;
                case RlHitKind.Land: App.Audio.Play("deal", 0.15f + 0.3f * h.power); break;
                case RlHitKind.Settle: App.Audio.Play("bet", 0.45f, 0.8f); break;
            }
        }

        // điểm (x, y, độ nảy z) trong hệ lòng chảo -> chỗ trên bánh xe (so với tâm mặt phẳng ô)
        public static Vector2 Project(float x, float y, float z)
        {
            float r = Mathf.Sqrt(x * x + y * y);
            return new Vector2(WheelR * x, WheelR * (RouletteWheel.TiltK * y + RouletteWheel.TiltKz * (RouletteWheel.Height(r) + z + RouletteWheel.BallR)));
        }

        void PlaceWheel()
        {
            if (!rotor) return;
            double a = RotorNow();
            rotor.localRotation = Quaternion.Euler(0, 0, (float)(a * 180.0 / Math.PI % 360.0));
            switch (ballAt)
            {
                case BallAt.Rest:
                {
                    float bx, by, bz = 0;
                    if (track != null) track.Sample(clock - entryT, out bx, out by, out bz);
                    else
                    {
                        double g = idleBallAngle + a;
                        bx = (float)Math.Cos(g) * RouletteWheel.RPocket;
                        by = (float)Math.Sin(g) * RouletteWheel.RPocket;
                    }
                    ball.anchoredPosition = Project(bx, by, bz);
                    break;
                }
                case BallAt.Roll:
                {
                    track.Sample(clock - entryT, out float bx, out float by, out float bz);
                    ball.anchoredPosition = Project(bx, by, bz);
                    if (!ball.gameObject.activeSelf) ball.gameObject.SetActive(true);
                    ball.localScale = Vector3.one;
                    if (flyBall.gameObject.activeSelf) flyBall.gameObject.SetActive(false);
                    if (clock - entryT > track.duration) ballAt = BallAt.Rest;
                    break;
                }
                case BallAt.Flight:
                {
                    // cung từ bàn tay tới điểm vào đường chạy (góc EntryAngle, tì vách), tới nơi đúng mốc entryT
                    float u = Mathf.Clamp01((clock - flightT0) / Mathf.Max(0.05f, entryT - flightT0));
                    float ca = (float)Math.Cos(RouletteBall.EntryAngle), sa = (float)Math.Sin(RouletteBall.EntryAngle);
                    Vector3 to = wheel.TransformPoint(Project(ca * RouletteWheel.RTrack, sa * RouletteWheel.RTrack, 0.05f));
                    // điểm giữa lệch về phía trước hướng lăn (bi vào theo tiếp tuyến, chiều kim đồng hồ) và nhô lên
                    Vector3 tangent = wheel.TransformVector(new Vector3(-sa * -1f, ca * -1f * RouletteWheel.TiltK, 0)).normalized;
                    Vector3 mid = Vector3.Lerp(flightFrom, to, 0.6f) - tangent * stage.lossyScale.x * 90f + stage.TransformVector(new Vector3(0, 40, 0));
                    float e = u * u * (3 - 2 * u);
                    flyBall.position = Vector3.Lerp(Vector3.Lerp(flightFrom, mid, e), Vector3.Lerp(mid, to, e), e);
                    if (!flyBall.gameObject.activeSelf) flyBall.gameObject.SetActive(true);
                    break;
                }
            }
        }

        IEnumerator PopBallOut()
        {
            float t = 0;
            while (t < 0.14f)
            {
                t += Time.deltaTime;
                ball.localScale = Vector3.one * Mathf.Lerp(1f, 0.2f, t / 0.14f);
                yield return null;
            }
            ball.gameObject.SetActive(false);
            ballAt = BallAt.Hidden;
        }

        void PlaceMarker(int pocket)
        {
            marker.anchoredPosition = CellPos(pocket == Roulette.StarPocket ? RlKind.Star : RlKind.Single, pocket) + new Vector2(-34, 12);
            marker.gameObject.SetActive(true);
            StartCoroutine(Pop(marker, 1f, 1.5f, 0.22f));
        }

        // ---------- tiền: vơ chip thua, trả chip thắng, phản ứng ----------

        IEnumerator Money(RlSpin r, TableMode mode, int playTier, int net)
        {
            var winIdx = new HashSet<int>(r.wins);
            var lose = Enumerable.Range(0, Mathf.Min(bets.Count, chips.Length)).Where(i => !winIdx.Contains(i)).ToList();
            var won = Enumerable.Range(0, Mathf.Min(bets.Count, chips.Length)).Where(i => winIdx.Contains(i)).ToList();
            bool any = won.Count > 0;
            bool big = any && (r.pocket == Roulette.StarPocket || r.payout >= r.staked * 4);
            winStreak = any ? winStreak + 1 : 0;
            bool outOfPlays = mode == TableMode.Paid && Casino.PlaysLeft(S, D, Game, Now) <= 0;
            Action after = outOfPlays ? (Action)Sulk : null;

            if (mode != TableMode.Paid)
            {
                // vòng miễn phí / vòng tập: chip thua về lại tay người chơi
                foreach (int i in lose) MoveChip(i, SlideAway(chips[i], 0.3f));
            }
            else if (lose.Count > 0)
            {
                if (!any) Say(Pick(Loc.T("Khè khè, của ta hết!"), Loc.T("Lần sau nhé, khách."), Loc.T("Bàn này ta làm chủ mà.")), 2f);
                yield return TakeIn(lose);
            }
            if (any)
            {
                Say(big ? Loc.T("Cái gì?! Trúng to thế!") : Pick(Loc.T("Hừ... hên thôi!"), Loc.T("Vòng sau ta gỡ."), Loc.T("Chà, khá đấy.")), 2f);
                // chồng chip nhà cái trả: tiền thắng của các cửa trúng (vòng miễn phí: phần lời thật nhận)
                int paid = mode == TableMode.Paid ? r.payout - won.Count * (r.staked / Mathf.Max(1, bets.Count)) : net;
                if (mode != TableMode.Practice && paid > 0) yield return PayOut(playTier, paid);
                yield return new WaitForSeconds(0.25f);
                foreach (int i in won) MoveChip(i, SlideAway(chips[i], 0.36f));
                if (win.root.gameObject.activeSelf) yield return LeaveStack();
                yield return WaitClip("pay");
                string react = winStreak >= 3 ? "grumpy" : big ? "react_win_big" : "react_win_small";
                if (winStreak >= 3)
                {
                    Say(Loc.T("Ba vòng liền?! Xui xẻo!"), 2f);
                    winStreak = 0;
                }
                if (dealerRig) dealerRig.Play(react, after);
            }
            else
            {
                yield return WaitClip("take");
                if (mode != TableMode.Paid) Say(Loc.T("Trượt rồi. May cho khách là chưa mất gì."), 2f);
                if (dealerRig) dealerRig.Play(mode == TableMode.Paid ? "react_lose" : "react_push", after);
            }
            yield return new WaitForSeconds(0.45f);
        }

        void Sulk()
        {
            if (!dealerRig) return;
            dealerRig.Play("sulk");
            Say(Loc.T("Hôm nay thế đủ rồi. Mai ghé, ta còn khối chiêu."), 3f);
        }

        // take: hai bàn tay úp thành chữ V ở ô gom (cham_chip): cú đập làm chip thua nảy vào lòng chữ V, rồi theo tay về khay (vo_xong)
        IEnumerator TakeIn(List<int> lose)
        {
            if (!dealerRig || !dealerRig.Has("take"))
            {
                foreach (int i in lose) MoveChip(i, Slide(chips[i].root, chips[i].root.anchoredPosition, TraySpot, 0.4f, () => chips[i].root.gameObject.SetActive(false)));
                yield return new WaitForSeconds(0.45f);
                yield break;
            }
            seenEv.Clear();
            lastEvent = null;
            bool done = false, held = false;
            dealerRig.Play("take", () => done = true);
            var from = lose.Select(i => chips[i].root.anchoredPosition).ToList();
            float hop = 0;
            while (!done)
            {
                if (seenEv.Contains("cham_chip") && !held)
                {
                    held = true;
                    App.Audio.Play("bet", 0.7f);
                    Haptics.Play(Haptic.UiTap);
                }
                if (held)
                {
                    hop = Mathf.Min(1, hop + Time.deltaTime / 0.2f);
                    var mid = Mid();
                    for (int k = 0; k < lose.Count; k++)
                    {
                        // nảy thành cung vào giữa hai bàn tay, xong thì bám theo tay
                        var target = mid + new Vector2((k - (lose.Count - 1) * 0.5f) * 20, 0);
                        float e = hop * hop * (3 - 2 * hop);
                        chips[lose[k]].root.anchoredPosition = Vector2.Lerp(from[k], target, e) + new Vector2(0, 46 * Mathf.Sin(hop * Mathf.PI));
                    }
                }
                if (seenEv.Contains("vo_xong")) break;
                yield return null;
            }
            float t = 0;
            while (t < 0.2f)
            {
                t += Time.deltaTime;
                foreach (int i in lose) chips[i].group.alpha = 1 - t / 0.2f;
                yield return null;
            }
            foreach (int i in lose)
            {
                chips[i].root.gameObject.SetActive(false);
                chips[i].group.alpha = 1;
            }
        }

        Vector2 Mid() => (StageLocal(dealerRig.BoneWorld("tay_tb")) + StageLocal(dealerRig.BoneWorld("tay_pb"))) * 0.5f + new Vector2(0, -32);

        // pay: tay phải gạt chồng chip thắng từ khay ra ô gom (theo bàn tay từ giây 0,6 tới sự kiện tra_chip)
        IEnumerator PayOut(int playTier, int amount)
        {
            var sp = stackSprites != null && stackSprites.Length > 0 ? stackSprites[Mathf.Clamp(playTier, 0, stackSprites.Length - 1)] : null;
            if (sp) win.img.sprite = sp;
            win.label.text = Loc.F("+{0} bi", NumFmt.Short(amount));
            win.root.gameObject.SetActive(false);
            if (!dealerRig || !dealerRig.Has("pay"))
            {
                yield return Slide(win.root, TraySpot, WinSpot, 0.35f);
                yield break;
            }
            seenEv.Clear();
            bool done = false;
            dealerRig.Play("pay", () => done = true);
            while (!done)
            {
                float ct = dealerRig.Current == "pay" ? dealerRig.State.ClipTime : 99;
                if (ct >= 0.6f && !seenEv.Contains("tra_chip") && ct < 1.3f)
                {
                    if (!win.root.gameObject.activeSelf) win.root.gameObject.SetActive(true);
                    win.root.anchoredPosition = StageLocal(dealerRig.BoneWorld("tay_pb")) + new Vector2(-30, -36);
                }
                if (seenEv.Contains("tra_chip") || ct >= 1.3f) break;
                yield return null;
            }
            win.root.gameObject.SetActive(true);
            yield return Slide(win.root, win.root.anchoredPosition, WinSpot, 0.12f);
            App.Audio.Play("coin", 0.6f);
        }

        IEnumerator LeaveStack()
        {
            var p0 = win.root.anchoredPosition;
            yield return Slide(win.root, p0, new Vector2(LaneX, -2000), 0.42f, null, new Vector2(LaneX, p0.y - 60));
            win.root.gameObject.SetActive(false);
        }

        // mỗi chip chỉ một chuyển động một lúc (chip vừa bỏ / vừa trả có thể được đặt lại ngay)
        void MoveChip(int i, IEnumerator move)
        {
            if (i < chipCo.Length && chipCo[i] != null) StopCoroutine(chipCo[i]);
            var co = StartCoroutine(move);
            if (i < chipCo.Length) chipCo[i] = co;
        }

        // chip về phía người chơi: vòng ra làn bên cạnh bánh xe rồi trôi xuống khỏi màn
        IEnumerator SlideAway(Chip c, float dur)
        {
            var p0 = c.root.anchoredPosition;
            float lane = p0.x >= 0 ? LaneX : -LaneX;
            yield return Slide(c.root, p0, new Vector2(lane, -2000), dur, null, new Vector2(lane, p0.y - 80));
            c.root.gameObject.SetActive(false);
        }

        IEnumerator Slide(RectTransform rt, Vector2 from, Vector2 to, float dur, Action done = null, Vector2? via = null)
        {
            rt.gameObject.SetActive(true);
            float t = 0;
            while (t < dur)
            {
                t += Time.deltaTime;
                float u = Mathf.Clamp01(t / dur);
                float e = 1 - (1 - u) * (1 - u) * (1 - u);
                rt.anchoredPosition = via.HasValue
                    ? Vector2.Lerp(Vector2.Lerp(from, via.Value, e), Vector2.Lerp(via.Value, to, e), e)
                    : Vector2.Lerp(from, to, e);
                yield return null;
            }
            rt.anchoredPosition = to;
            done?.Invoke();
        }

        static IEnumerator Fade(CanvasGroup g, float to, float dur)
        {
            float from = g.alpha, t = 0;
            while (t < dur)
            {
                t += Time.deltaTime;
                g.alpha = Mathf.Lerp(from, to, t / dur);
                yield return null;
            }
            g.alpha = to;
        }

        static IEnumerator Pop(RectTransform rt, float baseScale, float peak, float dur)
        {
            float t = 0;
            while (t < dur)
            {
                t += Time.deltaTime;
                float s = baseScale * Mathf.Lerp(1, peak, Mathf.Sin(Mathf.Clamp01(t / dur) * Mathf.PI));
                rt.localScale = new Vector3(s, s, 1);
                yield return null;
            }
            rt.localScale = new Vector3(baseScale, baseScale, 1);
        }

        // ---------- Lão Mực: clip, sự kiện ----------

        // khoảng giây giữa hai sự kiện của một clip (đọc từ rig); thiếu thì lấy mặc định
        float EventGap(string clip, string a, string b, float def)
        {
            if (!dealerRig || !dealerRig.Has(clip)) return def;
            int i = dealerRig.Asset.FindClip(clip);
            var ev = dealerRig.Asset.anims[i].ev;
            if (ev == null) return def;
            float ta = -1, tb = -1;
            foreach (var e in ev)
            {
                if (e.name == a && ta < 0) ta = e.t;
                if (e.name == b && tb < 0) tb = e.t;
            }
            return ta >= 0 && tb > ta ? tb - ta : def;
        }

        IEnumerator WaitEvent(string ev, float maxWait)
        {
            float w = 0;
            while (!seenEv.Contains(ev) && w < maxWait)
            {
                w += Time.deltaTime;
                yield return null;
            }
        }

        // phát clip và chờ một sự kiện của nó (hoặc clip hết / quá giờ)
        IEnumerator PlayUntil(string clip, string ev, float maxWait)
        {
            if (!dealerRig || !dealerRig.Has(clip)) yield break;
            seenEv.Clear();
            bool done = false;
            dealerRig.Play(clip, () => done = true);
            float w = 0;
            while (!seenEv.Contains(ev) && !done && w < maxWait)
            {
                w += Time.deltaTime;
                yield return null;
            }
        }

        IEnumerator Clip(string name, float maxWait)
        {
            if (!dealerRig || !dealerRig.Has(name)) yield break;
            bool done = false;
            dealerRig.Play(name, () => done = true);
            float t = 0;
            while (!done && t < maxWait)
            {
                t += Time.deltaTime;
                yield return null;
            }
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

        // ---------- sân khấu ----------

        void FitStage()
        {
            if (!stage || !(stage.parent is RectTransform p)) return;
            lastStage = p.rect.size;
            float s = Mathf.Max(p.rect.width / StageW, p.rect.height / StageH);
            if (s <= 0 || float.IsNaN(s)) s = 1;
            stage.localScale = new Vector3(s, s, 1);
        }

        // chỗ "anchored" trên sân khấu (gốc ở mép trên giữa) ra toạ độ thế giới
        Vector3 StageWorld(Vector2 anchored) =>
            stage.TransformPoint(new Vector3(anchored.x, anchored.y + stage.rect.height * (1 - stage.pivot.y), 0));

        Vector2 StageLocal(Vector3 world)
        {
            var p = (Vector2)stage.InverseTransformPoint(world);
            return p - new Vector2(0, stage.rect.height * (1 - stage.pivot.y));
        }

        // ---------- bong bóng thoại ----------

        static string Pick(params string[] lines) => lines[UnityEngine.Random.Range(0, lines.Length)];

        void Say(string text, float secs)
        {
            if (!bubble) return;
            if (bubbleCo != null) StopCoroutine(bubbleCo);
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

        void Draw()
        {
            int bet = BetNow;
            var mode = Mode;
            bool shown = lastPocket >= 0;
            for (int i = 0; i < singles.Length; i++) Tint(singles[i], shown, lastPocket == i);
            for (int i = 0; i < elems.Length; i++) Tint(elems[i], shown, shown && lastPocket != Roulette.StarPocket && lastPocket / 5 == i);
            for (int i = 0; i < nums.Length; i++) Tint(nums[i], shown, shown && lastPocket != Roulette.StarPocket && Roulette.NumOf(lastPocket) == i + 1);
            Tint(star, shown, lastPocket == Roulette.StarPocket);
            if (!spinning && !shown)
                banner.text = bets.Count == 0 ? Loc.T("Chạm ô trên bảng cược để đặt chip")
                    : Loc.F("Chip {0}/{1} · mỗi chip {2} bi", bets.Count, Mathf.Min(C.chips, chips.Length), bet) +
                      (mode == TableMode.Paid ? "" : " · " + (mode == TableMode.Free ? Loc.T("miễn phí") : Loc.T("vòng tập")));
            spin.SetText(mode == TableMode.Free ? Loc.T("Quay miễn phí") : mode == TableMode.Practice ? Loc.T("Quay tập")
                : bets.Count > 0 ? Loc.F("Quay · {0} bi", bets.Count * bet) : Loc.T("Quay"));
            spin.SetRole(mode == TableMode.Practice ? BtnColor.Blue : BtnColor.Green);
            spin.Locked = spinning || bets.Count == 0;
            clear.SetText(Loc.T("Bỏ chip"));
            clear.Locked = spinning || bets.Count == 0;
        }

        // có kết quả: ô trúng giữ màu và nhô lên, ô khác lùi tối
        void Tint(Cell c, bool shown, bool hit)
        {
            c.frame.color = !(shown && dimmed) || hit ? c.color : Color.Lerp(c.color, new Color(0.13f, 0.15f, 0.3f, c.color.a), 0.55f);
            c.root.localScale = Vector3.one * (shown && hit ? 1.07f : 1f);
            if (shown && hit) c.root.SetAsLastSibling();
        }

        // ---------- cho lượt chụp ----------

        public void BetForTest(params (RlKind k, int v)[] list)
        {
            if (list == null || list.Length == 0) list = new[] { (RlKind.Elem, 3), (RlKind.Num, 3), (RlKind.Single, 17), (RlKind.Star, 0) };
            foreach (var (k, v) in list) Add(k, v);
        }

        public void SpinForTest() => Spin();
    }
}
