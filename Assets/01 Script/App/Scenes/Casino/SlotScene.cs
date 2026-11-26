// Scene lều Hội Máy Quả (máy quả 3×3, 5 đường) của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.7; GD_Claude/31 mốc D5). Prefab
// Screens/CasinoSlot (menu "PokiClash/Prefab/Đảo Casino/Lều Máy Quả: dựng scene", Editor/CasinoSlotMenu.cs). Lõi: Core/Casino/Slots.cs.
// Phần chung: CasinoTableScene (bản gọn: nút "thông tin" + bảng gập ở góc trái dưới).
// - Sân khấu 1080 x 1920 dưới Canvas/Nen: nền lều, Lão Mực sau quầy bên phải (DealerRig, lớp thân bị cắt ở mép quầy), máy quả
//   "Háu Ăn" đứng trên bục (rig AtomSpine ArtGen/Casino/may_qua, cũng vẽ bằng DealerRig + DealerLayer), hình ba cuộn (SlotReels) nằm
//   trong ô cuộn và méo theo thân máy, tay Lão Mực vẽ trên cùng.
// - Bấm Quay: Lão Mực kéo cần (clip sl_pull) và máy bị giật (clip pull) phát CÙNG MỘT KHUNG (tay bám đúng núm cần); cuộn giật lùi rồi
//   VỌT lên tốc độ máy quả thật (ReelSpeed ô / giây, hình nhoè thành vệt, kêu lạch cạch), ba cuộn nổ máy lệch nhau một nhịp, hãm
//   gấp rồi dừng lần lượt trái sang phải đúng ô dừng lõi đã chọn (hình trên cuộn là dải thật của cuộn, không xếp suýt trúng), mỗi
//   cuộn dừng máy "cạch" một cái (stop_1..3). Hai cuộn đầu đã khớp một đường lớn thật thì cuộn cuối chạy lâu hơn, máy nín thở (tease).
//   Kết quả: lose / win / free (3 Rương) / jackpot (huy hiệu khách mời hoặc thắng từ 20 lần cược).
// - Sự kiện của rig máy: nha_bi (phun vài viên bi ở miệng), no .. het_no (bi phun liên tục lúc jackpot), dap (rung màn).
// - Quay nhanh và lượt miễn phí: bỏ đoạn kéo cần, cuộn dừng nhanh, không tự quay.
// Mọi vật dựng sẵn trong prefab, không sinh lúc chạy.
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
    public sealed class SlotScene : CasinoTableScene
    {
        public const float StageW = 1080, StageH = 1920;
        // nhịp khớp clip của rig máy (ArtGen/Casino/may_qua/rig/hoat_anh.py): cần bị giật ở 0,47 s của clip pull (dài 0,9 s)
        const float PullKeo = 0.47f, PullLen = 0.9f, StopLen = 0.4f, Stop3Len = 0.5f, TeaseExtra = 0.8f;
        // cuộn: tốc độ lúc chạy đều (ô / giây; máy thật ~ 30–40), tăng tốc trong SpinUp giây, hãm trong SpinDown giây cuối,
        // cuộn sau nổ máy trễ hơn cuộn trước StartLag giây
        const float ReelSpeed = 38f, SpinUp = 0.16f, SpinDown = 0.26f, StartLag = 0.05f;
        static readonly float[] StopNormal = { 0.85f, 1.3f, 1.8f }, StopQuick = { 0.30f, 0.42f, 0.56f };

        [SerializeField] RectTransform stage, fly;
        [SerializeField] DealerRig machine, dealer;
        [SerializeField] SlotReels reels;
        [SerializeField] Image[] balls;
        [SerializeField] RectTransform bubble;
        [SerializeField] TextMeshProUGUI bubbleText;
        [SerializeField] TextMeshProUGUI lines, banner;
        [SerializeField] SketchButton spin, quick, pays;

        public override string Title => Loc.T("Hội Máy Quả");
        protected override string Game => Casino.Slot;
        protected override CasinoTable Table => C;
        protected override bool Busy => spinning;

        static SlotsConfig C => D.Cfg.casino.slots;

        protected override string HelpText =>
            Loc.T("Quay 3 cuộn. Ba biểu tượng giống nhau trên một trong 5 đường (ba hàng ngang, hai đường chéo) thì thắng; Sao thay được mọi biểu tượng trừ Rương.") + "\n" +
            Loc.T("Hai Rương ở đâu cũng được: trả gấp đôi cược. Ba Rương: được lượt quay miễn phí cùng mức cược.") + "\n" +
            Loc.T("Ba huy hiệu khách mời trên một đường: thêm mảnh tướng khách mời. Không có tự quay; Quay nhanh chỉ bỏ bớt diễn.");

        bool spinning, fast;
        SlotRound last;
        int[] shown = new int[3];
        Vector2 lastStage;
        Coroutine bubbleCo;
        static (double rtp, double hit, double freeP, double badge)? exact;

        // bi phun (hiệu ứng): mỗi viên một Image trong pool
        Vector2[] ballPos, ballVel;
        float[] ballLife, ballSpin;
        int ballNext;
        bool fountain;
        float fountainAcc, shake;

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform stageRt, RectTransform flyRt, DealerRig machineRig, DealerRig dealerRig, SlotReels reelsUi, Image[] ballPool,
            RectTransform bubbleRt, TextMeshProUGUI bubbleLabel, TextMeshProUGUI linesText, TextMeshProUGUI bannerText,
            SketchButton spinBtn, SketchButton quickBtn, SketchButton paysBtn)
        {
            stage = stageRt; fly = flyRt; machine = machineRig; dealer = dealerRig; reels = reelsUi; balls = ballPool;
            bubble = bubbleRt; bubbleText = bubbleLabel; lines = linesText; banner = bannerText; spin = spinBtn; quick = quickBtn; pays = paysBtn;
        }

        static readonly string[] LineName = { "Đường giữa", "Đường trên", "Đường dưới", "Chéo xuống", "Chéo lên" };

        public static string SymName(int sym)
        {
            if (sym >= 0 && sym < 5) return Loc.F("ngọc {0}", Elements.Name(Elements.All[sym]));
            switch (sym)
            {
                case Slots.BallSym: return Loc.T("bi");
                case Slots.Badge: return Loc.T("huy hiệu khách mời");
                case Slots.Wild: return Loc.T("Sao");
                case Slots.Chest: return Loc.T("Rương");
                default: return "?";
            }
        }

        protected override void EnterTable()
        {
            spinning = false;
            last = null;
            fountain = false;
            shake = 0;
            spin.SetOnClick(Spin);
            quick.SetOnClick(() =>
            {
                fast = !fast;
                Draw();
            });
            pays.SetText(Loc.T("Bảng trả"));
            pays.SetOnClick(PayTable);
            HideBalls();
            FitStage();
            if (reels)
            {
                reels.Bind(C);
                // khung lúc vào: một ô dừng ngẫu nhiên của dải thật
                shown = (int[])Slots.Spin(C, 0, rng).stops.Clone();
                reels.Show(shown);
                reels.Wins(null);
            }
            lines.text = "";
            banner.text = Loc.T("Bấm Quay để thử vận");
            if (machine)
            {
                machine.Fired -= OnMachineEvent;
                machine.Fired += OnMachineEvent;
                machine.Play("appear");
            }
            var mode = Mode;
            if (Guiding) // lần đầu: Lão Mực đang dẫn (CasinoGuide), không chào riêng
            {
                Draw();
                return;
            }
            if (dealer) dealer.Play("greet");
            Say(mode == TableMode.Free ? Loc.T("Lượt đầu ta khao, trượt không mất gì.")
                : mode == TableMode.Practice ? Loc.T("Hôm nay hết lượt có thưởng rồi, quay tập cho vui nhé.")
                : Loc.T("Ba hình giống nhau trên một đường là trúng. Cái máy này thật thà hơn ta đấy."), 3.2f);
            Draw();
        }

        protected override void OnTierChanged() => Draw();

        protected override DealerRig StageDealer => dealer;

        void OnDisable()
        {
            fountain = false;
            HideBalls();
            if (bubbleCo != null) StopCoroutine(bubbleCo);
            bubbleCo = null;
            if (bubble) bubble.gameObject.SetActive(false);
        }

        void Draw()
        {
            var mode = Mode;
            spin.SetText(mode == TableMode.Free ? Loc.T("Quay miễn phí") : mode == TableMode.Practice ? Loc.T("Quay tập") : Loc.F("Quay · {0} bi", BetNow));
            spin.SetRole(mode == TableMode.Practice ? BtnColor.Blue : BtnColor.Green);
            spin.Locked = spinning;
            quick.SetText(fast ? Loc.T("Quay nhanh: bật") : Loc.T("Quay nhanh: tắt"));
            quick.SetRole(fast ? BtnColor.Yellow : BtnColor.Paper);
        }

        void Spin()
        {
            if (spinning) return;
            var mode = Mode;
            var round = Slots.PlayAs(S, D, tier, mode, Now, rng, out var jar, out var extra, out var why);
            if (round == null)
            {
                NoBalls(why);
                return;
            }
            App.Save.Save();
            SetInfo(false);
            StartCoroutine(Run(round, mode, jar, extra));
        }

        IEnumerator Run(SlotRound round, TableMode mode, JarResult jar, List<Reward> extra)
        {
            spinning = true;
            last = round;
            Draw();
            lines.text = "";
            for (int k = 0; k < round.spins.Count; k++)
            {
                var sp = round.spins[k];
                bool quickSpin = sp.free || fast;
                banner.text = sp.free ? Loc.F("Lượt miễn phí {0}/{1}", k, round.spins.Count - 1)
                    : mode == TableMode.Free ? Loc.T("Lượt miễn phí đầu tiên!") : mode == TableMode.Practice ? Loc.T("Quay tập") : Loc.T("Đang quay...");
                yield return SpinOne(sp, quickSpin);
                var winCells = new HashSet<int>();
                foreach (var (line, sym, p) in sp.lines)
                    for (int r = 0; r < 3; r++) winCells.Add(r * 3 + Slots.LineRows[line][r]);
                if (sp.chests >= 2)
                    for (int r = 0; r < 3; r++)
                        for (int row = 0; row < 3; row++)
                            if (sp.grid[r, row] == Slots.Chest) winCells.Add(r * 3 + row);
                if (reels) reels.Wins(winCells);
                var parts = sp.lines.Select(l => Loc.F("{0}: 3 {1} ×{2}", Loc.T(LineName[l.line]), SymName(l.sym), l.pays)).ToList();
                if (sp.chests == 2) parts.Add(Loc.F("2 Rương ×{0} cược", C.scatter2));
                if (sp.freeWon > 0) parts.Add(Loc.F("3 Rương: +{0} lượt miễn phí!", sp.freeWon));
                lines.text = parts.Count > 0 ? string.Join("\n", parts) : Loc.T("Không trúng đường nào");
                if (sp.payout > 0 || sp.freeWon > 0) App.Audio.Play(sp.freeWon > 0 ? "prize" : "coin", 0.5f + Mathf.Min(0.5f, sp.payout / (float)Mathf.Max(1, round.bet) * 0.1f));
                yield return Result(sp, round.bet, quickSpin, mode);
            }
            int total = round.Payout;
            int net = mode == TableMode.Paid ? total - round.bet : mode == TableMode.Free ? Casino.FreeWin(total, round.bet) : 0;
            string free = round.spins.Count > 1 ? " " + Loc.F("({0} lượt miễn phí)", round.spins.Count - 1) : "";
            banner.text = mode == TableMode.Practice ? (total > 0 ? Loc.F("Trúng {0} bi (quay tập, không nhận)", total) : Loc.T("Trượt (quay tập)"))
                : total > 0 ? Loc.F("Trúng {0} bi", total) + free + " · " + (net >= 0 ? Loc.F("lời {0}", net) : Loc.F("lỗ {0}", -net))
                : mode == TableMode.Free ? Loc.T("Trượt, không mất gì") : Loc.F("Trượt · −{0} bi", round.bet);
            spinning = false;
            AfterRound(net, mode == TableMode.Paid ? jar : null, extra);
            if (mode == TableMode.Paid && Casino.PlaysLeft(S, D, Game, Now) <= 0)
                Say(Loc.T("Hôm nay thế đủ rồi. Mai ghé, ta còn khối chiêu."), 3f);
            Draw();
        }

        // hai cuộn đầu đã khớp một đường đáng giá THẬT (huy hiệu, ba Sao, hoặc trả từ 10 lần cược đường): cuộn cuối chạy lâu hơn
        bool TeaseWorthy(SlotSpin sp)
        {
            foreach (var rows in Slots.LineRows)
            {
                int a = sp.grid[0, rows[0]], b = sp.grid[1, rows[1]];
                if (a == Slots.Chest || b == Slots.Chest) continue;
                if (a != b && a != Slots.Wild && b != Slots.Wild) continue;
                int bs = a != Slots.Wild ? a : b;
                if (bs == Slots.Badge || bs == Slots.Wild) return true;
                var p = C.pays.Find(x => x.sym == bs);
                if (p != null && p.pays >= 10) return true;
            }
            return false;
        }

        static float Ease(float x)
        {
            x = Mathf.Clamp01(x);
            return x * x * (3 - 2 * x);
        }

        // một lượt quay: (Lão Mực kéo cần, máy bị giật) -> cuộn giật lùi rồi chạy -> dừng lần lượt, mỗi cuộn dừng máy "cạch" một cái
        IEnumerator SpinOne(SlotSpin sp, bool quickSpin)
        {
            if (reels) reels.Wins(null);
            var st = quickSpin ? StopQuick : StopNormal;
            float t0 = quickSpin ? 0.06f : PullKeo;     // lúc cuộn bắt đầu chạy
            bool tease = !quickSpin && TeaseWorthy(sp);
            float[] stopAt = { t0 + st[0], t0 + st[1], t0 + st[2] + (tease ? TeaseExtra : 0) };
            if (quickSpin)
            {
                if (machine) machine.Loop("spin", 0.08f);
            }
            else
            {
                // hai clip phát cùng một khung: tay Lão Mực bám đúng núm cần (đường núm nướng sẵn trong sl_pull)
                if (machine) machine.Play("pull");
                if (dealer) dealer.Play("sl_pull");
            }
            var from = (int[])shown.Clone();
            // dải cuộn lặp vòng: lùi quỹ đạo dừng đi trọn số vòng sao cho lúc tăng tốc xong nó nằm ngay DƯỚI chỗ cuộn đang đứng, để từ lúc
            // nổ máy tới lúc dừng hình chỉ chạy một chiều xuống
            var lap = new float[3];
            for (int r = 0; r < 3; r++)
            {
                int n = Mathf.Max(1, C.reels[r].strip.Length);
                float rem = stopAt[r] - (t0 + StartLag * r + SpinUp);
                float atUp = sp.stops[r] + (rem >= SpinDown ? ReelSpeed * (rem - SpinDown * 0.5f) : ReelSpeed * Mathf.Max(0, rem) * Mathf.Max(0, rem) / (2f * SpinDown));
                float want = from[r] + 0.3f - ReelSpeed * SpinUp * 0.5f;
                lap[r] = Mathf.Ceil((atUp - want) / n) * n;
            }
            var done = new bool[3];
            bool started = false, looped = quickSpin;
            float t = 0, nextAt = -1, nextTick = 0;
            string nextClip = null;
            while (true)
            {
                t += Time.deltaTime;
                if (!started && t >= t0)
                {
                    started = true;
                    App.Audio.Play("slLever", 0.9f); // cần gạt (gen Magnific, ArtGen/Sfx/casino)
                }
                if (!looped && t >= PullLen - 0.06f)
                {
                    looped = true;
                    if (machine) machine.Loop("spin");
                }
                bool anyFast = false;
                for (int r = 0; r < 3; r++)
                {
                    if (!reels) break;
                    float go = t0 + StartLag * r;        // cuộn r nổ máy
                    if (t < go - 0.10f) reels.Set(r, from[r], 0);
                    else if (t < go) reels.Set(r, from[r] + 0.3f * Ease((t - (go - 0.10f)) / 0.10f), 0);   // giật lùi lấy đà
                    else if (t < stopAt[r])
                    {
                        // còn rem giây tới lúc dừng: chạy đều ReelSpeed, SpinDown giây cuối hãm đều về 0 (quãng còn lại = diện tích dưới
                        // đường tốc độ, nên dừng đúng ô, không giật)
                        float rem = stopAt[r] - t;
                        float left = rem >= SpinDown ? ReelSpeed * (rem - SpinDown * 0.5f) : ReelSpeed * rem * rem / (2f * SpinDown);
                        float v = rem >= SpinDown ? ReelSpeed : ReelSpeed * rem / SpinDown;
                        float up = Mathf.Clamp01((t - go) / SpinUp);
                        v *= up;
                        // lúc mới nổ máy: đi từ ô đang hiện (đã giật lùi) vào dòng chạy, tăng tốc dần
                        float p = sp.stops[r] + left - lap[r];
                        if (up < 1) p = Mathf.Lerp(from[r] + 0.3f - ReelSpeed * SpinUp * 0.5f * up * up, p, up * up);
                        reels.Set(r, p, v);
                        anyFast |= v > 8f;
                    }
                    else
                    {
                        float s = t - stopAt[r];
                        // quá đà xuống một chút rồi nảy về
                        reels.Set(r, sp.stops[r] - (s < 0.16f ? 0.24f * Mathf.Sin(Mathf.PI * s / 0.16f) * (1 - s / 0.16f) : 0), 0);
                    }
                }
                // tiếng lạch cạch của cuộn: dày lúc cả ba cùng chạy, thưa dần khi từng cuộn dừng
                if (anyFast && t >= nextTick)
                {
                    int running = (done[0] ? 0 : 1) + (done[1] ? 0 : 1) + (done[2] ? 0 : 1);
                    nextTick = t + (running >= 3 ? 0.055f : running == 2 ? 0.075f : 0.1f);
                    App.Audio.Play("peg", 0.16f, 0.9f + 0.1f * running);
                }
                for (int r = 0; r < 3; r++)
                {
                    if (done[r] || t < stopAt[r]) continue;
                    done[r] = true;
                    App.Audio.Play("slStop" + (r + 1), 0.6f + 0.2f * r); // mỗi cuộn một tiếng dừng
                    if (machine && (!quickSpin || r == 2))
                    {
                        machine.Play(r == 0 ? "stop_1" : r == 1 ? "stop_2" : "stop_3", null, 0.06f);
                        nextAt = r < 2 ? t + StopLen - 0.05f : -1;
                        nextClip = r == 1 && tease ? "tease" : "spin";
                    }
                }
                if (nextAt > 0 && t >= nextAt)
                {
                    nextAt = -1;
                    if (machine) machine.Loop(nextClip);
                }
                if (done[2] && t >= stopAt[2] + (quickSpin ? 0.22f : Stop3Len - 0.08f)) break;
                yield return null;
            }
            shown = (int[])sp.stops.Clone();
            if (reels) reels.Show(shown);
        }

        float ClipLen(string clip)
        {
            if (!machine || !machine.Has(clip)) return 0;
            return machine.Asset.anims[machine.Asset.FindClip(clip)].dur;
        }

        IEnumerator Result(SlotSpin sp, int bet, bool quickSpin, TableMode mode)
        {
            bool jackpot = sp.badgeLines > 0 || bet > 0 && sp.payout >= bet * 20;
            bool won = sp.payout > 0 || sp.freeWon > 0;
            string clip = jackpot ? "jackpot" : sp.freeWon > 0 ? "free" : sp.payout > 0 ? "win" : "lose";
            float len = ClipLen(clip);
            if (machine) machine.Play(clip, null, 0.06f);
            if (jackpot)
            {
                Haptics.Play(Haptic.Win);
                if (dealer) dealer.Play("react_win_big");
                App.Audio.Play("mucBoing");
                Say(Pick(Loc.T("Trời đất, nổ hũ rồi!"), Loc.T("Cái máy phản chủ này!")), 2.4f);
            }
            else if (!quickSpin)
            {
                if (won)
                {
                    if (dealer) dealer.Play("react_win_small");
                    if (Random.value < 0.5f) Say(Pick(Loc.T("Hừ... hên thôi!"), Loc.T("Chà, khá đấy.")), 1.6f);
                }
                else if (Random.value < 0.34f)
                {
                    if (dealer) dealer.Play(mode == TableMode.Paid ? "react_lose" : "react_push");
                    Say(Pick(Loc.T("Khè khè, lần sau nhé."), Loc.T("Máy đói rồi, cho nó ăn tiếp đi.")), 1.6f);
                }
            }
            float wait = jackpot ? len : sp.freeWon > 0 ? len : won ? (quickSpin ? 0.7f : len) : (quickSpin ? 0.3f : Mathf.Min(len, 0.85f));
            yield return new WaitForSeconds(Mathf.Max(0.15f, wait));
        }

        // ---------- sự kiện của rig máy: bi phun, rung màn ----------

        void OnMachineEvent(string ev)
        {
            switch (ev)
            {
                case "nha_bi":
                    Burst("mieng", 7, 760, 70);
                    break;
                case "no":
                    fountain = true;
                    Burst("mieng", 10, 1100, 60);
                    App.Audio.Play("prize", 1f);
                    break;
                case "het_no":
                    fountain = false;
                    break;
                case "dap":
                    fountain = false;
                    shake = 0.28f;
                    App.Audio.Play("land", 1f);
                    break;
                case "keo":
                    App.Audio.Play("click", 0.8f);
                    break;
            }
        }

        void EnsureBalls()
        {
            if (balls == null || ballPos != null && ballPos.Length == balls.Length) return;
            ballPos = new Vector2[balls.Length];
            ballVel = new Vector2[balls.Length];
            ballLife = new float[balls.Length];
            ballSpin = new float[balls.Length];
        }

        void HideBalls()
        {
            if (balls == null) return;
            EnsureBalls();
            for (int i = 0; i < balls.Length; i++)
            {
                ballLife[i] = 0;
                if (balls[i]) balls[i].gameObject.SetActive(false);
            }
        }

        // n viên bi bắn ra từ một xương của máy: hướng lên, toả `spread` độ hai bên
        void Burst(string bone, int n, float speed, float spread)
        {
            if (balls == null || balls.Length == 0 || !machine || !fly) return;
            EnsureBalls();
            Vector2 at = fly.InverseTransformPoint(machine.BoneWorld(bone));
            for (int k = 0; k < n; k++)
            {
                int i = ballNext;
                ballNext = (ballNext + 1) % balls.Length;
                if (!balls[i]) continue;
                float a = (90f + Random.Range(-spread, spread)) * Mathf.Deg2Rad;
                float v = speed * Random.Range(0.55f, 1.1f);
                ballPos[i] = at + new Vector2(Random.Range(-40f, 40f), Random.Range(-10f, 10f));
                ballVel[i] = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * v;
                ballLife[i] = 1.5f;
                ballSpin[i] = Random.Range(-360f, 360f);
                balls[i].gameObject.SetActive(true);
                float sc = Random.Range(0.75f, 1.15f);
                balls[i].rectTransform.localScale = new Vector3(sc, sc, 1);
                balls[i].color = Color.white;
            }
        }

        void Update()
        {
            // sân khấu co theo màn: phủ kín như ảnh nền
            if (stage && stage.parent is RectTransform p && p.rect.size != lastStage) FitStage();
            float dt = Time.deltaTime;
            if (fountain)
            {
                fountainAcc += dt * 46f;
                while (fountainAcc >= 1)
                {
                    fountainAcc -= 1;
                    Burst(Random.value < 0.7f ? "mieng" : "sao", 1, 1150, 55);
                }
            }
            if (ballPos != null)
                for (int i = 0; i < balls.Length; i++)
                {
                    if (ballLife[i] <= 0 || !balls[i]) continue;
                    ballLife[i] -= dt;
                    if (ballLife[i] <= 0)
                    {
                        balls[i].gameObject.SetActive(false);
                        continue;
                    }
                    ballVel[i].y -= 2600f * dt;
                    ballPos[i] += ballVel[i] * dt;
                    var rt = balls[i].rectTransform;
                    rt.anchoredPosition = ballPos[i];
                    rt.localRotation = Quaternion.Euler(0, 0, ballSpin[i] * (1.5f - ballLife[i]));
                    if (ballLife[i] < 0.25f) balls[i].color = new Color(1, 1, 1, ballLife[i] / 0.25f);
                }
            if (stage)
            {
                // rung màn lúc máy rơi bẹp: hai dáng đổi nhau, tắt dần
                if (shake > 0)
                {
                    shake -= dt;
                    float k = Mathf.Clamp01(shake / 0.28f);
                    float s = Mathf.FloorToInt(Time.time * 30f) % 2 == 0 ? 1 : -1;
                    stage.anchoredPosition = shake > 0 ? new Vector2(10f * s * k, -14f * k) : Vector2.zero;
                }
            }
        }

        void FitStage()
        {
            if (!stage || !(stage.parent is RectTransform p)) return;
            lastStage = p.rect.size;
            float s = Mathf.Max(p.rect.width / StageW, p.rect.height / StageH);
            if (s <= 0 || float.IsNaN(s)) s = 1;
            stage.localScale = new Vector3(s, s, 1);
        }

        // ---------- bong bóng thoại của Lão Mực ----------

        static string Pick(params string[] choices) => choices[Random.Range(0, choices.Length)];

        void Say(string text, float secs)
        {
            if (!bubble || !isActiveAndEnabled) return;
            if (bubbleCo != null) StopCoroutine(bubbleCo);
            CasinoGuide.Mumble(); // Lão Mực lầm bầm
            bubbleCo = StartCoroutine(SayCo(text, secs));
        }

        IEnumerator SayCo(string text, float secs)
        {
            bubbleText.text = text;
            bubble.gameObject.SetActive(true);
            float t = 0;
            while (t < 0.12f)
            {
                t += Time.deltaTime;
                float s = Mathf.Lerp(1f, 1.08f, Mathf.Sin(Mathf.Clamp01(t / 0.12f) * Mathf.PI));
                bubble.localScale = new Vector3(s, s, 1);
                yield return null;
            }
            bubble.localScale = Vector3.one;
            yield return new WaitForSeconds(secs);
            bubble.gameObject.SetActive(false);
            bubbleCo = null;
        }

        // bảng trả: từng biểu tượng × cược mỗi đường, Sao, Rương; hoàn trả tính chính xác trên mọi tổ hợp dừng
        void PayTable()
        {
            exact ??= Slots.Exact(C);
            var e = exact.Value;
            var sb = new System.Text.StringBuilder();
            sb.AppendLine(Loc.F("Cược {0} bi chia đều 5 đường ({1} bi mỗi đường).", BetNow, BetNow / (float)Slots.Lines));
            foreach (var p in C.pays.OrderByDescending(x => x.pays))
                sb.AppendLine(Loc.F("3 {0}: ×{1} cược đường", SymName(p.sym), p.pays));
            sb.AppendLine(Loc.F("3 Sao: ×{0} cược đường", C.wildPays));
            sb.AppendLine(Loc.F("2 Rương ở đâu cũng được: ×{0} tổng cược. 3 Rương: {1} lượt miễn phí", C.scatter2, C.freeSpins));
            var bs = C.badgeShards;
            if (bs.Length > 0) sb.AppendLine(Loc.F("3 huy hiệu trên một đường: +{0} mảnh khách mời (theo bậc cược)", string.Join(" / ", bs)));
            sb.AppendLine();
            sb.AppendLine(Loc.F("Hoàn trả {0}% · trúng {1}% số lượt · ra lượt miễn phí {2}%", (e.rtp * 100).ToString("0.0"), (e.hit * 100).ToString("0"),
                (e.freeP * 100).ToString("0.0")));
            App.Modals.Alert(Loc.T("Bảng trả"), sb.ToString().TrimEnd(), Loc.T("Đóng"));
        }

        // ---------- cho lượt chụp ----------

        public bool Spinning => spinning;
        public void SpinForTest() => Spin();
        public DealerRig MachineForTest => machine;
    }
}
