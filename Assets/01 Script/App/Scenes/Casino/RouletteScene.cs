// Scene lều Vòng Xoay Ngũ Hành (Roulette) của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.7, mốc C7). Prefab Screens/CasinoRoulette (menu
// "PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene"). Lõi: Core/Casino/Roulette.cs. Phần chung: CasinoTableScene.
// - Bánh xe 26 ô xếp vòng (5 hệ × số 1–5, ô Sao Vàng); chạm một ô là đặt chip Ô đơn (trả 24:1). Viên bi chạy quanh vành rồi dừng ở ô ra.
// - Bàn cược: 5 cửa Hệ (4:1), 5 cửa Số (4:1), cửa Sao Vàng (24:1, cược từ bậc 3 được thêm mảnh khách mời); mỗi chạm một chip,
//   tối đa 5 chip mỗi vòng (mỗi chip bằng mức cược của bậc đang chọn). Bỏ chip, Quay.
// - Kết quả: ô ra, cửa thắng sáng lên, bi thắng / thua; Tỉ lệ (bảng trả, hoàn trả 96,2%) trong Cách chơi.
// Mọi vật dựng sẵn trong prefab (26 ô, 11 cửa), không sinh lúc chạy.
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
        [System.Serializable]
        public struct Pocket
        {
            public Button button;
            public Image dot;
            public TextMeshProUGUI num, chips;
        }

        [System.Serializable]
        public struct Spot
        {
            public SketchButton button;
            public TextMeshProUGUI chips;
        }

        [SerializeField] RectTransform wheel, ball;
        [SerializeField] Pocket[] pockets;
        [SerializeField] TextMeshProUGUI center, chipLine, banner;
        [SerializeField] Spot[] elems, nums;
        [SerializeField] Spot star;
        [SerializeField] SketchButton clear, spin;

        public override string Title => Loc.T("Vòng Xoay Ngũ Hành");
        protected override string Game => Casino.Roulette;
        protected override CasinoTable Table => C;
        protected override bool Busy => spinning;

        static RouletteConfig C => D.Cfg.casino.roulette;

        protected override string HelpText =>
            Loc.T("Bánh xe có 26 ô: 5 hệ, mỗi hệ số 1 tới 5, và một ô Sao Vàng. Đặt chip rồi quay, viên bi dừng ở ô nào thì cửa trúng ô đó thắng.") + "\n" +
            Loc.F("Hệ: trúng một trong 5 ô của hệ, trả {0}:1. Số: trúng một trong 5 ô cùng số, trả {1}:1. Ô đơn (chạm ô trên bánh xe): trả {2}:1. Sao Vàng: trả {3}:1, cược từ bậc {4} được thêm mảnh tướng khách mời.",
                C.elemPays, C.numPays, C.singlePays, C.starPays, C.starTier + 1) + "\n" +
            Loc.F("Tối đa {0} chip mỗi vòng. Mọi cửa hoàn trả {1}% (25/26).", C.chips, (Roulette.Rtp(C, RlKind.Elem) * 100).ToString("0.0"));

        readonly List<RlBet> bets = new List<RlBet>();
        bool spinning;
        float ballAngle;
        int lastPocket = -1;
        List<int> lastWins = new List<int>();

        const float Radius = 238;

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform wheelRt, RectTransform ballRt, Pocket[] pocketList, TextMeshProUGUI centerText, TextMeshProUGUI chipText,
            TextMeshProUGUI bannerText, Spot[] elemSpots, Spot[] numSpots, Spot starSpot, SketchButton clearBtn, SketchButton spinBtn)
        {
            wheel = wheelRt; ball = ballRt; pockets = pocketList; center = centerText; chipLine = chipText; banner = bannerText;
            elems = elemSpots; nums = numSpots; star = starSpot; clear = clearBtn; spin = spinBtn;
        }

        public static float AngleOf(int pocket) => 90f - pocket * 360f / Roulette.Pockets; // ô 0 ở đỉnh, xếp theo chiều kim đồng hồ

        protected override void EnterTable()
        {
            bets.Clear();
            spinning = false;
            lastPocket = -1;
            lastWins.Clear();
            for (int i = 0; i < pockets.Length; i++)
            {
                int k = i;
                pockets[i].button.onClick.RemoveAllListeners();
                if (i != Roulette.StarPocket) pockets[i].button.onClick.AddListener(() => Add(RlKind.Single, k));
                else pockets[i].button.onClick.AddListener(() => Add(RlKind.Star, 0));
            }
            for (int i = 0; i < elems.Length; i++)
            {
                int k = i;
                elems[i].button.SetText(Loc.F("{0} ×{1}", Elements.Name(Elements.All[i]), C.elemPays));
                elems[i].button.SetOnClick(() => Add(RlKind.Elem, k));
            }
            for (int i = 0; i < nums.Length; i++)
            {
                int k = i + 1;
                nums[i].button.SetText(Loc.F("Số {0} ×{1}", k, C.numPays));
                nums[i].button.SetOnClick(() => Add(RlKind.Num, k));
            }
            star.button.SetText(Loc.F("Sao Vàng ×{0}", C.starPays));
            star.button.SetOnClick(() => Add(RlKind.Star, 0));
            clear.SetOnClick(() =>
            {
                if (spinning) return;
                bets.Clear();
                Draw();
            });
            spin.SetOnClick(Spin);
            ballAngle = AngleOf(0);
            PlaceBall(ballAngle);
            banner.text = Loc.T("Chạm cửa cược để đặt chip, rồi bấm Quay");
            Draw();
        }

        protected override void OnTierChanged() => Draw();

        void Add(RlKind k, int v)
        {
            if (spinning) return;
            if (bets.Count >= C.chips)
            {
                App.Toasts.Show(Loc.F("Tối đa {0} chip mỗi vòng", C.chips), Icon("info"));
                return;
            }
            if (lastPocket >= 0)
            {
                lastPocket = -1;
                lastWins.Clear();
            }
            bets.Add(new RlBet { kind = k, v = v });
            App.Audio.Play("bet", 0.8f, 1f + bets.Count * 0.05f);
            Draw();
        }

        int Count(RlKind k, int v) => bets.Count(b => b.kind == k && (k == RlKind.Star || b.v == v));

        void Spin()
        {
            if (spinning) return;
            if (bets.Count == 0)
            {
                App.Toasts.Show(Loc.T("Đặt ít nhất một chip"), Icon("info"));
                return;
            }
            var mode = Mode;
            var r = Roulette.PlayAs(S, D, bets, tier, mode, Now, rng, out var jar, out var extra, out var why);
            if (r == null)
            {
                NoBalls(why);
                return;
            }
            App.Save.Save();
            StartCoroutine(Run(r, mode, jar, extra));
        }

        IEnumerator Run(RlSpin r, TableMode mode, JarResult jar, List<Reward> extra)
        {
            spinning = true;
            banner.text = mode == TableMode.Free ? Loc.T("Vòng miễn phí!") : mode == TableMode.Practice ? Loc.T("Vòng tập") : Loc.T("Bánh xe đang quay...");
            center.text = "";
            Draw();
            App.Audio.Play("whoosh");
            // viên bi chạy ngược chiều kim đồng hồ 3 vòng rồi dừng đúng ô ra (chậm dần)
            float from = ballAngle, to = AngleOf(r.pocket);
            float delta = Mathf.Repeat(from - to, 360f) + 360f * 3;
            const float T = 2.4f;
            float tick = 0;
            for (float t = 0; t < T; t += Time.unscaledDeltaTime)
            {
                float k = 1 - Mathf.Pow(1 - t / T, 3);
                ballAngle = from - delta * k;
                PlaceBall(ballAngle);
                tick += Time.unscaledDeltaTime * (1 - k) * 14;
                if (tick > 1)
                {
                    tick = 0;
                    App.Audio.Play("peg", 0.3f);
                }
                yield return null;
            }
            ballAngle = to;
            PlaceBall(ballAngle);
            lastPocket = r.pocket;
            lastWins = r.wins.ToList();
            int net = mode == TableMode.Paid ? r.payout - r.staked : mode == TableMode.Free ? Casino.FreeWin(r.payout, r.staked) : 0;
            center.text = r.pocket == Roulette.StarPocket ? Loc.T("Sao Vàng") : Elements.Name(Roulette.ElemOf(r.pocket)) + " " + Roulette.NumOf(r.pocket);
            banner.text = r.wins.Count == 0 ? (mode == TableMode.Practice ? Loc.T("Trượt (vòng tập)") : mode == TableMode.Free ? Loc.T("Trượt, không mất gì") : Loc.F("Trượt · −{0} bi", r.staked))
                : mode == TableMode.Practice ? Loc.F("Trúng {0} cửa (vòng tập)", r.wins.Count)
                : Loc.F("Trúng {0} cửa · {1} bi", r.wins.Count, net >= 0 ? "+" + net : net.ToString());
            if (r.wins.Count == 0) App.Audio.Play("stamp", 0.5f);
            spinning = false;
            bets.Clear();
            AfterRound(net, mode == TableMode.Paid ? jar : null, extra);
            Draw();
        }

        void PlaceBall(float angle)
        {
            float a = angle * Mathf.Deg2Rad;
            ball.anchoredPosition = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * (Radius - 52);
        }

        // ---------- vẽ ----------

        void Draw()
        {
            int bet = BetNow;
            var mode = Mode;
            for (int i = 0; i < pockets.Length; i++)
            {
                var p = pockets[i];
                bool won = lastPocket == i;
                int n = i == Roulette.StarPocket ? Count(RlKind.Star, 0) : Count(RlKind.Single, i);
                p.chips.gameObject.SetActive(n > 0);
                p.chips.text = n.ToString(); // số chip trên ô (phông không có ●)
                p.dot.transform.localScale = Vector3.one * (won ? 1.35f : 1f);
            }
            for (int i = 0; i < elems.Length; i++) BindSpot(elems[i], Count(RlKind.Elem, i), lastPocket >= 0 && lastPocket != Roulette.StarPocket && lastPocket / 5 == i);
            for (int i = 0; i < nums.Length; i++) BindSpot(nums[i], Count(RlKind.Num, i + 1), lastPocket >= 0 && lastPocket != Roulette.StarPocket && Roulette.NumOf(lastPocket) == i + 1);
            BindSpot(star, Count(RlKind.Star, 0), lastPocket == Roulette.StarPocket);
            chipLine.text = Loc.F("Chip: {0}/{1} · mỗi chip {2} bi · tổng {3} bi", bets.Count, C.chips, bet, bets.Count * bet) +
                            (mode == TableMode.Paid ? "" : " · " + (mode == TableMode.Free ? Loc.T("miễn phí") : Loc.T("vòng tập")));
            spin.SetText(mode == TableMode.Free ? Loc.T("Quay miễn phí") : mode == TableMode.Practice ? Loc.T("Quay tập") : Loc.F("Quay · {0} bi", bets.Count * bet));
            spin.SetRole(mode == TableMode.Practice ? BtnColor.Blue : BtnColor.Green);
            spin.Locked = spinning || bets.Count == 0;
            clear.SetText(Loc.T("Bỏ chip"));
            clear.Locked = spinning || bets.Count == 0;
        }

        static void BindSpot(Spot s, int n, bool hit)
        {
            s.chips.gameObject.SetActive(n > 0);
            s.chips.text = Loc.F("{0} chip", n);
            s.button.SetRole(hit ? BtnColor.Yellow : BtnColor.Paper);
        }

        // ---------- cho lượt chụp ----------

        public bool Spinning => spinning;

        public void BetForTest()
        {
            Add(RlKind.Elem, 2);
            Add(RlKind.Num, 3);
            Add(RlKind.Single, 7);
            Add(RlKind.Star, 0);
        }

        public void SpinForTest() => Spin();
    }
}
