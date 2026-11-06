// Máy bi: thả bi qua đinh, rơi vào ô EXP / hoàn bi / rương (chép Web/src/view/screens/machine.ts).
// Nút ×N là mức cược: tốn N bi mỗi lần thả, thưởng ×N. Mức cược mở theo số bi đang có (cfg.xSteps, như máy tham khảo: nhiều bi
// thì được thả nhanh hơn); bi tụt dưới mốc thì hết đợt cược tự về mức cao nhất còn mở. Mỗi đợt tối đa MaxPerDrop(cấp) bi; đợt xong
// (mọi bi đã rơi) thì mở lần lượt rương trong khay, rồi hộp "Huyền thoại!" (nếu vừa vượt mốc), rồi "Lên cấp!". Rương chờ nằm trong bản lưu.
// Hàng dưới cùng bên phải là thanh mốc: mốc Huyền thoại (một lần), xong thì các mốc quà vòng lại (cfg.gifts): tiêu đủ n bi thì
// ô quà ở đầu thanh nhún, quà bay ra (rương vào khay, sao EXP lên thanh, bi về dòng đếm) rồi ô quà đổi sang quà kế.
// Prefab màn hình Assets/04 Prefabs/Screens/Machine (mặt máy, cột cược, khay rương 3 nút dựng sẵn, nút thả); hộp Dialogs/TiLeMayBi, Dialogs/HuyenThoai.
// Ô quà dựng bằng menu "PokiClash/Prefab/Máy bi: mốc quà".
// Trên đầu máy là thanh kinh nghiệm (MachineExpBar): EXP rơi vào ô bay lên thanh. Số trên ô đổi theo mức cược (MachineBoard.SetMult).
// Nút vẽ tay (2026-11-06, học máy tham khảo, gói ArtGen/Pachinko/gui_gpt/bo_moi): nút thả là nút vòm to giữa dưới máy (4 trạng thái),
// nút thả liền vòm nhỏ, viên cược tròn, đèn vòm chạy; dựng bằng menu "PokiClash/Prefab/Máy bi: nút tròn, viên cược, đèn vòm".
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class MachineScene : SceneRoot
    {
        public override string Title => "Máy bi";

        public const float MachineTop = 100; // mép trên máy trong khối giữa
        public const float BlockH = 1530;
        const double Tick = 1.0 / 120;
        static int lastX = 1; // mức cược nhớ trong lần chơi này

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)] // Play không reload domain
        static void ResetStatics() => lastX = 1;

        // khay "Rương chờ": thứ tự nút dựng sẵn, vàng trên cùng
        public static readonly SlotKind[] TrayKinds = { SlotKind.ChestGold, SlotKind.ChestSilver, SlotKind.ChestWood };

        [System.Serializable]
        public struct Parts
        {
            public MachineBoard machine;
            public RectTransform trayCol;
            public SketchButton rates, drop, auto;
            public HoldArea dropHold; // chạm-giữ trên nút "Thả bi"
            public SketchButton[] bets; // nút cược theo cfg.xSteps lúc nướng
            public TextMeshProUGUI[] betLocks; // chữ "n bi" trên nút cược chưa mở
            public SketchButton[] tray; // nút khay theo TrayKinds
            public TextMeshProUGUI[] trayCounts; // "×n" trên nút khay
            public GameObject trayEmpty; // "(trống)"
            public TextMeshProUGUI counter, legendText;
            public UiBar legendBar;
            public MachineRatesDialog ratesDialog;
            public LegendMilestoneDialog legendDialog;
            public MachineExpBar expBar; // thanh kinh nghiệm trên đầu máy (menu "PokiClash/Prefab/Máy bi: thanh kinh nghiệm")
            // ô quà ở đầu thanh mốc (menu "PokiClash/Prefab/Máy bi: mốc quà"): rương kit, hoặc icon bi/XP/sao kèm số
            public RectTransform giftBadge;
            public ChestIcon giftChest;
            public UnityEngine.UI.Image giftIcon;
            public TextMeshProUGUI giftCount;
            public UnityEngine.UI.Button giftButton; // chạm thanh hoặc ô quà: báo các mốc kế
            // nút tròn vẽ tay (menu "PokiClash/Prefab/Máy bi: nút tròn, viên cược, đèn vòm"; học nút vòm của máy tham khảo): ảnh vòm
            // của nút thả và nút thả liền (nền SketchButton để trong suốt), vòng đứt nhịp quanh nút thả khi giữ, ảnh viên cược theo
            // thứ tự bets, bóng đèn rời đặt khít bóng vẽ trên vòm tủ (chạy vòng, nhanh hơn khi đang thả, cả dãy nháy khi trúng két)
            public UnityEngine.UI.Image dropDome, autoDome, holdRing;
            public UnityEngine.UI.Image[] betTokens;
            public UnityEngine.UI.Image[] bulbs;
        }

        [SerializeField] Parts p;

        Board board;
        MachineBoard view;
        Rng rng;
        readonly List<(SketchButton b, TextMeshProUGUI lockText, int x)> xBtns = new List<(SketchButton, TextMeshProUGUI, int)>();

        int x = 1;
        bool holding;
        float holdTimer, time, saveTimer;
        double acc;
        int session; // số lần thả trong đợt này
        int autoLeft;
        int lvFrom = -1; // cấp lúc bắt đầu đợt / lúc mở rương, để báo "Lên cấp!" một lần sau cùng
        Reward bigReward; // mốc Huyền thoại vừa vượt trong đợt
        bool ending, opening, leaving, dirty;
        float slowT; // còn bao lâu chạy chậm (rương vàng)
        int giftBusy; // quà mốc đang nhận: thanh giữ đầy, ô quà chưa đổi sang quà kế
        float giftPopT = -1, giftPunchT = -1, counterPopT = -1;
        string giftShown; // quà đang hiện ở ô quà (đổi thì nhún vào)
        int maxX; // mức cược cao nhất đang mở, để báo khi có đủ bi mở thêm mức
        float ringT, bulbStep, partyT; // vòng giữ nút; bước chạy đèn vòm; còn bao lâu cả dãy đèn nháy (trúng két)
        bool domeDown; // ảnh nút thả đang ở trạng thái lún (chữ dời theo nắp)

        // nút thả: cược từ mức này dùng nắp vàng có sao (cùng mốc với bi vàng, MachineBoard.BallColor)
        const int BigBet = 5;
        static readonly Color Clear = new Color(1, 1, 1, 0);
        static readonly Dictionary<string, Sprite> art = new Dictionary<string, Sprite>();

        static Sprite Art(string n)
        {
            if (!art.TryGetValue(n, out var s) || !s) art[n] = s = App.Art ? App.Art.Get(n) : null;
            return s;
        }

        static void SetSprite(UnityEngine.UI.Image img, string n)
        {
            var s = Art(n);
            if (img && s && img.sprite != s) img.sprite = s;
        }

        // rương vàng: máy chạy chậm SlowScale lần trong SlowHold giây rồi nhanh dần lại trong SlowRamp giây, máng thả tạm ngừng;
        // mặt máy rung, vòng loé đôi, nhạc mừng ngắn. Chỉ rương vàng có những thứ này (tiếng và hình tỉ lệ với giá trị thật).
        public const float SlowScale = 0.3f, SlowHold = 0.45f, SlowRamp = 0.25f, ShakeAmp = 14f, ShakeTime = 0.4f;

        // cho công cụ thử
        public int Session => session;
        public bool Idle => session == 0 && !ending && !opening && board != null && board.balls.Count == 0;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        public override void Enter(object args)
        {
            rng = new Rng(Rng.RandomSeed());
            board = new Board(Rng.RandomSeed());
            view = p.machine;
            view.Bind(board);
            view.Hold.Down = StartHold;
            view.Hold.Up = () => holding = false;

            p.rates.SetOnClick(Rates);
            BindBets();
            foreach (var b in p.tray) b.SetOnClick(OpenFromTray);
            p.drop.ClickSound = null;
            p.dropHold.Down = StartHold;
            p.dropHold.Up = () => holding = false;
            p.auto.SetOnClick(Auto);
            if (p.giftButton) p.giftButton.onClick.AddListener(GiftInfo);
            var barBtn = p.legendBar.GetComponent<UnityEngine.UI.Button>();
            if (barBtn) barBtn.onClick.AddListener(GiftInfo);
            x = Progress.XBest(S, D.Cfg, lastX);
            maxX = Progress.XBest(S, D.Cfg, int.MaxValue);
            giftShown = null;
            if (p.expBar) p.expBar.Bind();
            RefreshUi();
            view.SetMult(x, false);
            RebuildTray();
        }

        // bản lưu đổi từ nơi khác (bảng thử, thanh trên): làm mới; khay chỉ dựng lại khi máy rảnh (trong đợt, rương bay vào rồi mới hiện)
        public override void Refresh()
        {
            RefreshUi();
            if (session == 0 && !ending && !opening) RebuildTray();
        }

        // nút cược dựng sẵn theo cfg.xSteps lúc nướng: gán lại mức và số bi cần có theo dữ liệu, nút thừa ẩn
        void BindBets()
        {
            var steps = D.Cfg.xSteps;
            if (steps.Count > p.bets.Length)
                Debug.LogWarning($"[Máy bi] Prefab có {p.bets.Length} nút cược, cấu hình có {steps.Count} mức: nướng lại màn Máy bi (ghi đè)");
            xBtns.Clear();
            for (int i = 0; i < p.bets.Length; i++)
            {
                var b = p.bets[i];
                b.gameObject.SetActive(i < steps.Count);
                if (i >= steps.Count) continue;
                int bx = steps[i].x, need = steps[i].balls;
                b.name = "cuoc_x" + bx;
                b.SetText("×" + bx);
                b.SetOnClick(() => PickX(bx, need));
                p.betLocks[i].text = $"{need} bi";
                xBtns.Add((b, p.betLocks[i], bx));
            }
        }

        static int Need(int bx) => D.Cfg.xSteps.Find(q => q.x == bx)?.balls ?? 0;

        // nút cược chưa mở: mờ như nút tắt nhưng vẫn chạm được (báo cần bao nhiêu bi)
        static Color Locked => Color.Lerp(Theme.Paper, Theme.Paper3, 0.75f) * new Color(1, 1, 1, 0.75f);

        // ---------- giao diện ----------

        void RefreshUi()
        {
            if (board == null) return;
            var s = S;
            var allowed = Progress.XAllowed(s, D.Cfg);
            bool idle = session == 0 && !ending && !opening;
            // bi tụt dưới mốc của mức đang chọn: hết đợt mới hạ (đợt đang chạy giữ nguyên cược), về mức cao nhất còn mở
            if (!allowed.Contains(x) && idle)
            {
                int nx = Progress.XBest(s, D.Cfg, x);
                App.Toasts.Show($"Còn {s.balls} bi, cược về ×{nx} (×{x} cần có {Need(x)} bi)", App.Art.Icon("ball"));
                x = lastX = nx;
            }
            // có đủ bi mở thêm mức: báo và nhún nút mới (như bảng "mốc tiếp theo" của máy tham khảo)
            if (idle)
            {
                int top = Progress.XBest(s, D.Cfg, int.MaxValue);
                if (top > maxX)
                {
                    App.Toasts.Show($"Có {s.balls} bi: mở cược ×{top}, thả nhanh hơn", App.Art.Icon("ball"));
                    App.Audio.Play("pick", 0.7f, 1.2f);
                    var nb = xBtns.Find(q => q.x == top).b;
                    if (nb) StartCoroutine(PopRect(nb.Rect, top == x ? 1.08f : 1f));
                }
                maxX = top;
            }
            view.SetMult(x, false);
            if (p.expBar) p.expBar.Sync();
            int topX = D.Cfg.xSteps.Count > 0 ? D.Cfg.xSteps[D.Cfg.xSteps.Count - 1].x : 1;
            for (int i = 0; i < xBtns.Count; i++)
            {
                var (b, lockText, bx) = xBtns[i];
                bool ok = allowed.Contains(bx);
                var token = p.betTokens != null && i < p.betTokens.Length ? p.betTokens[i] : null;
                b.Interactable = true;
                b.Label.alpha = ok ? 1 : 0.6f;
                b.Rect.localScale = Vector3.one * (bx == x ? 1.08f : 1f);
                lockText.gameObject.SetActive(!ok);
                if (token)
                {
                    // viên cược vẽ tay: thường, đang chọn (vàng), mức cao nhất đang chọn (tím), khoá (xám có ổ khoá)
                    b.SetColor(Clear);
                    SetSprite(token, !ok ? "pk_cuoc_khoa" : bx != x ? "pk_cuoc" : bx == topX ? "pk_cuoc_max" : "pk_cuoc_chon");
                    b.Label.color = ok && bx == x && bx == topX ? Color.white : Theme.Ink;
                    if (ok) b.Label.rectTransform.Stretch(10, 10, 10, 12);
                    else b.Label.rectTransform.Stretch(14, 16, 14, 52);
                    continue;
                }
                b.SetColor(!ok ? Locked : bx == x ? Theme.Yellow : Theme.Paper);
                if (ok) b.Label.rectTransform.Stretch(8, 4, 14, 14);
                else b.Label.rectTransform.Stretch(8, 0, 14, 40);
            }
            int max = D.Cfg.MaxPerDrop(s.level);
            p.counter.text = session > 0 ? $"Đợt này: {session}/{max}" : $"{s.balls} bi · tốn {x}/lần";
            p.auto.SetText(p.autoDome ? $"Thả liền\n{max}" : $"Thả liền {max}"); // nắp vòm nhỏ: hai dòng
            if (p.dropDome) p.drop.SetColor(Clear);
            else p.drop.SetColor(CanDrop() ? Theme.Red : Color.Lerp(Theme.Red, Theme.Paper3, 0.6f));
            if (p.autoDome) p.auto.SetColor(Clear);
            UpdateDomes(0);
            RefreshMilestone();
        }

        // nút vòm: đang giữ thì nắp lún (chữ dời xuống theo nắp) và vòng đứt nhịp ra ngoài 0,4 giây một nhịp; hết bi hay hết lượt
        // đợt thì nắp xám; cược lớn nắp vàng có sao. Nút thả liền: đang thả liền thì nắp lún xanh ngọc.
        void UpdateDomes(float dt)
        {
            if (p.dropDome)
            {
                bool down = holding;
                SetSprite(p.dropDome, down ? "pk_nut_tha_nhan" : !CanDrop() ? "pk_nut_tha_het" : x >= BigBet ? "pk_nut_tha_lon" : "pk_nut_tha");
                if (down != domeDown && p.drop.Label)
                {
                    float shift = p.drop.Rect.rect.height * 0.08f; // nắp lún: tâm nắp xuống khoảng 8 % chiều cao nút
                    p.drop.Label.rectTransform.anchoredPosition += new Vector2(0, down ? -shift : shift);
                    domeDown = down;
                }
            }
            if (p.holdRing)
            {
                bool on = holding;
                if (p.holdRing.gameObject.activeSelf != on) p.holdRing.gameObject.SetActive(on);
                if (on)
                {
                    ringT += dt;
                    float k = ringT % 0.4f / 0.4f;
                    p.holdRing.rectTransform.localScale = Vector3.one * (1 + 0.3f * k);
                    p.holdRing.color = new Color(Theme.Yellow.r, Theme.Yellow.g, Theme.Yellow.b, 0.95f * (1 - k));
                }
                else ringT = 0;
            }
            if (p.autoDome) SetSprite(p.autoDome, autoLeft > 0 ? "pk_nut_lien_bat" : "pk_nut_lien");
        }

        // đèn vòm: cứ ba bóng sáng một (vàng, hồng xen nhau), chạy vòng 3,5 bước/giây, cược lớn 6, đang thả 9; trúng két thì cả dãy
        // nháy 8 lần/giây
        void UpdateBulbs(float dt)
        {
            if (p.bulbs == null || p.bulbs.Length == 0) return;
            bulbStep += dt * (session > 0 ? 9 : x >= BigBet ? 6 : 3.5f);
            if (partyT > 0) partyT -= dt;
            int step = (int)bulbStep;
            bool flashOn = (int)(partyT * 8) % 2 == 0;
            for (int i = 0; i < p.bulbs.Length; i++)
            {
                var b = p.bulbs[i];
                if (!b) continue;
                if (!b.gameObject.activeSelf) b.gameObject.SetActive(true);
                bool on = partyT > 0 ? flashOn : ((i - step) % 3 + 3) % 3 == 0;
                SetSprite(b, !on ? "pk_den_tat" : i % 2 == 0 ? "pk_den_sang" : "pk_den_sang_hong");
            }
        }

        // thanh mốc: mốc Huyền thoại cho tới khi nhận (vừa vượt trong đợt thì đứng đầy tới hộp "Huyền thoại!" cuối đợt),
        // rồi mốc quà đang chạy; lúc đang nhận quà thì giữ đầy
        void RefreshMilestone()
        {
            var s = S;
            var cfg = D.Cfg;
            bool legend = !s.legendDone || bigReward != null;
            var g = Pachinko.GiftNow(s, cfg);
            bool gifts = !legend && g != null && p.giftBadge;
            p.legendBar.gameObject.SetActive(legend || gifts);
            p.legendText.gameObject.SetActive(!legend && !gifts);
            if (p.giftBadge) p.giftBadge.gameObject.SetActive(legend || gifts);
            if (legend)
            {
                int need = cfg.legendMilestone;
                p.legendBar.Set(Mathf.Min(s.ballsSpent, need), need, 0, $"Huyền thoại: {Mathf.Min(s.ballsSpent, need)}/{need} bi");
                ShowGift("legend", null);
            }
            else if (gifts)
            {
                if (giftBusy > 0) p.legendBar.Set(1, 1, 0, "Nhận quà!");
                else
                {
                    p.legendBar.Set(s.gift, g.n, 0, $"{Pachinko.GiftName(g)}: {s.gift}/{g.n} bi");
                    ShowGift(g.k + s.giftTier, g);
                }
            }
            else p.legendText.text = LegendDoneText(D);
        }

        // ô quà ở đầu thanh mốc: rương (kit Ruong) hoặc icon kèm số; đổi quà thì nhún vào
        void ShowGift(string key, GiftStep g)
        {
            if (!p.giftBadge || key == giftShown) return;
            bool first = giftShown == null;
            giftShown = key;
            bool chest = g != null && g.k.StartsWith("chest");
            if (p.giftChest)
            {
                p.giftChest.gameObject.SetActive(chest);
                if (chest) p.giftChest.Bind(Pachinko.FromKey(g.k), p.giftChest.Rect.sizeDelta.x);
            }
            if (p.giftIcon)
            {
                p.giftIcon.gameObject.SetActive(!chest);
                if (!chest) p.giftIcon.sprite = App.Art.Icon(g == null ? "star" : g.k == "balls" ? "ball" : "exp");
            }
            if (p.giftCount)
            {
                p.giftCount.gameObject.SetActive(g != null && !chest);
                if (g != null && !chest) p.giftCount.text = "+" + g.v;
            }
            if (!first) giftPopT = 0;
        }

        // chạm thanh mốc: báo các mốc kế (bi còn phải thả tính dồn)
        void GiftInfo()
        {
            var s = S;
            var cfg = D.Cfg;
            if (!s.legendDone)
            {
                App.Toasts.Show($"Thả thêm {Mathf.Max(0, cfg.legendMilestone - s.ballsSpent)} bi: chắc chắn ra tướng Huyền thoại. Sau đó là các mốc quà.", App.Art.Icon("star"));
                return;
            }
            if (cfg.gifts.Count == 0) return;
            var parts = new List<string>();
            int left = 0;
            for (int i = 0; i < Mathf.Min(3, cfg.gifts.Count); i++)
            {
                var g = Pachinko.GiftAt(s, cfg, i);
                left += i == 0 ? g.n - s.gift : g.n;
                parts.Add($"{Pachinko.GiftName(g)} sau {left} bi");
            }
            App.Toasts.Show("Mốc quà: " + string.Join(" · ", parts), App.Art.Icon("chest"));
        }

        static readonly float[] GiftPop = { 0, 1, 0.08f, 1.35f, 0.25f, 0.92f, 0.4f, 1 };

        IEnumerator PopRect(RectTransform rt, float rest)
        {
            for (float t = 0; t < 0.4f && rt; t += Time.unscaledDeltaTime)
            {
                rt.localScale = Vector3.one * rest * MachineFx.Curve(GiftPop, t);
                yield return null;
            }
            if (rt) rt.localScale = Vector3.one * rest;
        }

        public static string LegendDoneText(GameData d) => $"Đã nhận {d.Hero(d.LegendMilestoneHero).name}. Từ giờ Huyền thoại rất hiếm.";

        void PickX(int bx, int need)
        {
            if (session > 0 || ending)
            {
                App.Toasts.Show("Đợt đang chạy, chờ bi rơi hết rồi đổi cược", App.Art.Icon("ball"));
                return;
            }
            if (!Progress.XAllowed(S, D.Cfg).Contains(bx))
            {
                App.Audio.Play("error");
                App.Toasts.Show($"Cần có {need} bi để mở ×{bx} (đang có {S.balls})", App.Art.Icon("ball"));
                return;
            }
            bool changed = bx != x;
            x = lastX = bx;
            // số trên ô nhún theo cược mới, chữ "×N" to nổi giữa máy (như bảng hệ số bật lên của máy tham khảo)
            view.SetMult(x);
            RefreshUi();
            if (!changed) return;
            view.Float(Board.BW / 2, Board.BH * 0.4, "×" + x, Theme.Hex("#f39a2d"), 64);
            App.Audio.Play("pick", 0.7f, 0.9f + Mathf.Min(x, 10) * 0.03f);
        }

        // khay "Rương chờ": đếm theo loại, vàng trên cùng; chạm để mở. Nút loại không có rương ẩn, nút còn lại xếp từ trên xuống.
        void RebuildTray()
        {
            if (board == null) return;
            float y = -48;
            int shown = 0;
            for (int i = 0; i < TrayKinds.Length && i < p.tray.Length; i++)
            {
                string key = Pachinko.Key(TrayKinds[i]);
                int n = S.chests.Count(c => c.kind == key);
                var b = p.tray[i];
                b.gameObject.SetActive(n > 0);
                if (n == 0) continue;
                b.Rect.anchoredPosition = new Vector2(0, y);
                p.trayCounts[i].text = "×" + n;
                y -= 124;
                shown++;
            }
            p.trayEmpty.SetActive(shown == 0);
        }

        Vector3 TrayPoint() => p.trayCol.TransformPoint(new Vector3(0, -100, 0));

        // ---------- thả ----------

        bool CanDrop() => !ending && !opening && S.balls >= x && session < D.Cfg.MaxPerDrop(S.level);

        double LauncherX => Board.BW / 2 + Mathf.Sin(time * 1.25f) * Board.Swing;

        bool DropOne()
        {
            if (!CanDrop()) return false;
            if (session == 0) lvFrom = S.level;
            var r = Pachinko.SpendBall(S, D, x);
            if (r != null) bigReward = r;
            int credit = Pachinko.GiftCredit(S, D.Cfg, x, r);
            if (credit > 0) giftPunchT = 0;
            foreach (var g in Pachinko.GiftAdd(S, D, credit))
            {
                // rương mốc quà vào hàng chờ như rương ở ô (không nhân cược: mốc đã tính theo số bi)
                if (g.k == RewardKind.Chest) S.chests.Add(new PendingChest { kind = Pachinko.Key(g.chest), x = 1 });
                StartCoroutine(GiftClaim(g));
            }
            board.Drop(LauncherX + (Random.value - 0.5) * 4, x);
            view.Launch(LauncherX);
            session++;
            dirty = true;
            App.Audio.Play("click");
            Haptics.Play(Haptic.Drop);
            RefreshUi();
            return true;
        }

        void StartHold()
        {
            if (leaving || App.Modals.Count > 0) return;
            if (!CanDrop())
            {
                DenyDrop();
                return;
            }
            holding = true;
            DropOne();
            holdTimer = 0;
        }

        void DenyDrop()
        {
            if (ending || opening) return;
            App.Audio.Play("error");
            int max = D.Cfg.MaxPerDrop(S.level);
            string msg = session >= max ? $"Tối đa {max} bi một đợt, chờ bi rơi hết"
                : S.balls <= 0 ? "Hết bi rồi! Thắng ải để có thêm bi" : $"Cần {x} bi cho mỗi lần thả ×{x}";
            App.Toasts.Show(msg, App.Art.Icon("ball"));
        }

        void Auto()
        {
            if (autoLeft > 0) return;
            autoLeft = Mathf.Min(D.Cfg.MaxPerDrop(S.level) - session, S.balls / x);
            if (ending || opening) autoLeft = 0;
            if (autoLeft <= 0)
            {
                autoLeft = 0;
                DenyDrop();
                return;
            }
            DropOne();
            autoLeft--;
            holdTimer = 0;
        }

        void Update()
        {
            if (board == null || leaving) return;
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            time += dt;
            float sim = 1;
            if (slowT > 0)
            {
                slowT -= dt;
                sim = slowT > SlowRamp ? SlowScale : Mathf.Lerp(1, SlowScale, Mathf.Max(0, slowT) / SlowRamp);
            }
            acc += dt * sim;
            while (acc >= Tick)
            {
                acc -= Tick;
                foreach (var e in board.Step(Tick))
                {
                    if (!e.land)
                    {
                        view.Flash(e.peg);
                        if (App.Audio.Peg((float)e.speed)) Haptics.Play(Haptic.Peg);
                    }
                    else OnLand(e.reward, e.slot, e.ball.x, System.Math.Min(e.ball.y, Board.Floor), e.ball.mult);
                }
            }
            // máng thả tạm ngừng khi đang chạy chậm
            if ((holding || autoLeft > 0) && slowT <= 0)
            {
                holdTimer += dt;
                if (holdTimer > 0.16f)
                {
                    holdTimer = 0;
                    if (!DropOne())
                    {
                        if (holding) DenyDrop();
                        holding = false;
                        autoLeft = 0;
                    }
                    else if (autoLeft > 0) autoLeft--;
                }
            }
            view.Sync(dt, dt * sim, LauncherX, CanDrop() ? x : 0);
            UpdateDomes(dt);
            UpdateBulbs(dt);
            AnimateMilestone(dt);
            if (session > 0 && board.balls.Count == 0 && !holding && autoLeft == 0 && !ending) StartCoroutine(SessionEnd());
            if (dirty && (saveTimer += dt) > 0.5f) SaveNow();
        }

        // ô quà nhún (nhận, đổi quà), thanh mốc nhún mỗi lần bi tính vào mốc (dáng như khung thanh EXP), dòng đếm nhún khi bi quà về
        void AnimateMilestone(float dt)
        {
            if (giftPopT >= 0 && p.giftBadge)
            {
                giftPopT += dt;
                float end = GiftPop[GiftPop.Length - 2];
                p.giftBadge.localScale = Vector3.one * (giftPopT >= end ? 1 : MachineFx.Curve(GiftPop, giftPopT));
                if (giftPopT >= end) giftPopT = -1;
            }
            if (giftPunchT >= 0)
            {
                giftPunchT += dt;
                var c = MachineExpBar.PunchCurve;
                float end = c[c.Length - 2];
                float k = giftPunchT >= end ? 0 : MachineFx.Curve(c, giftPunchT);
                p.legendBar.transform.localScale = new Vector3(1 + MachineExpBar.PunchX * k, 1 + MachineExpBar.PunchY * k, 1);
                if (giftPunchT >= end) giftPunchT = -1;
            }
            if (counterPopT >= 0)
            {
                counterPopT += dt;
                float end = GiftPop[GiftPop.Length - 2];
                float s = counterPopT >= end ? 1 : 1 + (MachineFx.Curve(GiftPop, counterPopT) - 1) * 0.5f;
                p.counter.rectTransform.localScale = Vector3.one * s;
                if (counterPopT >= end) counterPopT = -1;
            }
        }

        void SaveNow()
        {
            dirty = false;
            saveTimer = 0;
            App.Save.Save();
        }

        // ---------- bi rơi ----------

        void OnLand(SlotKind kind, int slot, double bx, double by, int mult)
        {
            var r = Pachinko.SlotReward(S, D.Cfg, kind, mult);
            bool gold = kind == SlotKind.ChestGold;
            if (slot >= 0)
            {
                view.Glow(slot, gold ? 2 : r.k == RewardKind.Chest ? 1 : 0);
                view.SlotFx(slot);
            }
            else view.CupFx(bx, by);
            switch (r.k)
            {
                case RewardKind.Exp:
                    view.Float(bx, by - 20, $"+{r.n} XP", MachineBoard.XpColor);
                    if (p.expBar) p.expBar.Fly(view.World(bx, by), r.n);
                    App.Audio.Play("land");
                    Haptics.Play(Haptic.LandSmall);
                    dirty = true;
                    break;
                case RewardKind.Balls:
                    view.Float(bx, by - 20, $"+{r.n} bi", MachineBoard.BallPink);
                    App.Audio.Play("coin");
                    Haptics.Play(Haptic.LandSmall);
                    dirty = true;
                    break;
                default:
                    S.chests.Add(new PendingChest { kind = Pachinko.Key(kind), x = mult });
                    var col = MachineBoard.ChestColor(kind);
                    view.Burst(bx, by - 10, col);
                    view.ChestFx(bx, by - 10, gold ? 3 : 2);
                    view.Float(bx, by - 30, Pachinko.ChestName(kind) + "!", col, gold ? 36 : 30);
                    App.Audio.Play("chest");
                    if (gold) Jackpot(bx, by - 10, col);
                    else Haptics.Play(kind == SlotKind.ChestSilver ? Haptic.LandSilver : Haptic.LandWood);
                    SaveNow();
                    StartCoroutine(FlyChest(kind, view.World(bx, by)));
                    break;
            }
        }

        // rương vàng: chạy chậm, rung mặt máy, vòng loé thứ hai to hơn, ba tiếng xu lên cao dần
        void Jackpot(double bx, double by, Color col)
        {
            slowT = SlowHold + SlowRamp;
            view.Shake(ShakeAmp, ShakeTime);
            view.Burst(bx, by, col, 1.8f);
            view.JackpotFx(bx, by);
            view.CloudFace("pk_may_tha_wow", 1.2f);
            partyT = 1.2f;
            Haptics.Play(Haptic.LandGold);
            StartCoroutine(Jingle());
        }

        IEnumerator Jingle()
        {
            for (int i = 0; i < 3 && !leaving; i++)
            {
                yield return new WaitForSecondsRealtime(0.09f);
                App.Audio.Play("coin", 0.8f, 1 + i * 0.12f);
            }
        }

        // rương bay từ chỗ rơi vào khay (bản sao prefab kit Kit/Ruong, xoá khi tới nơi)
        IEnumerator FlyChest(SlotKind kind, Vector3 from)
        {
            var ic = MachineBoard.ChestIcon(Frame, kind, 88);
            ic.position = from;
            var to = TrayPoint();
            for (float t = 0; t < 0.62f; t += Time.unscaledDeltaTime)
            {
                if (!ic) yield break;
                float k = t / 0.62f;
                float e = 1 - (1 - k) * (1 - k);
                var pos = Vector3.Lerp(from, to, e);
                pos.y += Mathf.Sin(k * Mathf.PI) * 0.12f * Vector3.Distance(from, to);
                ic.position = pos;
                ic.localScale = Vector3.one * Mathf.Lerp(1.15f, 0.8f, k);
                yield return null;
            }
            if (ic) Destroy(ic.gameObject);
            RebuildTray();
        }

        // ---------- mốc quà ----------

        // nhận quà mốc (bản lưu đã cộng lúc thả): thanh đứng đầy, ô quà nhún, loé to, quà bay ra; rồi ô quà đổi sang quà kế
        IEnumerator GiftClaim(Reward g)
        {
            giftBusy++;
            RefreshMilestone();
            var from = p.giftBadge ? p.giftBadge.position : TrayPoint();
            giftPopT = 0;
            giftPunchT = 0;
            if (p.expBar) p.expBar.Burst(from, true);
            App.Audio.Play(g.k == RewardKind.Chest ? "chest" : "coin", 0.9f, 1.1f);
            Haptics.Play(Haptic.LandSilver);
            yield return new WaitForSecondsRealtime(0.3f);
            if (!leaving)
                switch (g.k)
                {
                    case RewardKind.Chest:
                        StartCoroutine(FlyChest(g.chest, from));
                        break;
                    case RewardKind.Exp:
                        if (p.expBar) p.expBar.Fly(from, g.n);
                        break;
                    case RewardKind.Balls:
                        FlyBalls(from, g.n);
                        break;
                }
            yield return new WaitForSecondsRealtime(0.45f);
            giftBusy--;
            RefreshUi();
        }

        // bi quà bay từ ô quà về dòng đếm bi, tới nơi dòng đếm nhún (số bi đã cộng sẵn trong bản lưu)
        void FlyBalls(Vector3 from, int n)
        {
            int k = Mathf.Clamp(n / 3, 2, 5);
            var to = p.counter.rectTransform.TransformPoint(p.counter.rectTransform.rect.center);
            for (int i = 0; i < k; i++)
            {
                float pitch = 1.1f + i * 0.05f;
                System.Action arrive = () =>
                {
                    counterPopT = 0;
                    App.Audio.Play("pick", 0.5f, pitch);
                };
                if (p.expBar) p.expBar.FlyIcon(App.Art.Icon("ball"), from, to, i * 0.05f, arrive);
                else arrive();
            }
        }

        IEnumerator SessionEnd()
        {
            ending = true;
            session = 0;
            holding = false;
            SaveNow();
            RefreshUi();
            // chờ rương cuối bay vào khay, chữ nổi cuối kịp hiện, sao EXP cuối bay tới thanh
            yield return new WaitForSecondsRealtime(S.chests.Count > 0 ? 0.75f : 0.3f);
            for (float t = 0; p.expBar && p.expBar.Busy && !leaving && t < 2; t += Time.unscaledDeltaTime) yield return null;
            if (S.chests.Count > 0 && !leaving) yield return OpenChests();
            if (bigReward != null && !leaving)
            {
                var r = bigReward;
                bigReward = null;
                yield return Legend(r);
            }
            if (!leaving) LevelUp();
            ending = false;
            RefreshUi();
        }

        void LevelUp()
        {
            if (lvFrom >= 0 && S.level > lvFrom)
            {
                Haptics.Play(Haptic.LevelUp);
                Dialogs.LevelUp(lvFrom, S.level);
            }
            lvFrom = -1;
        }

        // ---------- rương ----------

        void OpenFromTray()
        {
            if (S.chests.Count == 0 || opening || ending) return;
            if (session > 0)
            {
                App.Toasts.Show("Chờ bi rơi hết rồi mở rương", App.Art.Icon("chest"));
                return;
            }
            StartCoroutine(OpenFromTrayRun());
        }

        IEnumerator OpenFromTrayRun()
        {
            ending = true;
            lvFrom = S.level;
            yield return OpenChests();
            if (!leaving) LevelUp();
            ending = false;
            RefreshUi();
        }

        static int Rank(string kind) => kind == "chest_gold" ? 0 : kind == "chest_silver" ? 1 : 2;

        IEnumerator OpenChests()
        {
            opening = true;
            RefreshUi();
            while (S.chests.Count > 0 && !leaving)
            {
                // rương quý mở trước, cùng loại thì theo thứ tự rơi vào
                var c = S.chests.OrderBy(q => Rank(q.kind)).First();
                S.chests.Remove(c);
                var kind = Pachinko.FromKey(c.kind);
                int cx = Mathf.Max(1, c.x);
                var rewards = Pachinko.OpenChest(S, D, kind, cx, rng);
                SaveNow();
                RebuildTray();

                int left = S.chests.Count;
                yield return ChestBox.Show(Pachinko.ChestName(kind) + (cx > 1 ? $" ×{cx}" : ""), kind, null,
                    rewards, left > 0 ? $"Mở tiếp ({left})" : "Nhận");
            }
            opening = false;
            RebuildTray();
            RefreshUi();
        }

        // ---------- mốc Huyền thoại ----------

        IEnumerator Legend(Reward r)
        {
            var h = D.Hero(r.hero);
            if (r.k == RewardKind.LegendCopies)
            {
                App.Toasts.Show($"Mốc {D.Cfg.legendMilestone} bi: +{r.n} bản sao thẻ Huyền thoại của {h.name}", App.Art.Icon("star"));
                yield break;
            }
            bool closed = false;
            App.Audio.Play("level");
            App.Modals.Open(p.legendDialog, () => closed = true).Show(h, D.Cfg.legendMilestone);
            while (!closed) yield return null;
        }

        // ---------- bảng tỉ lệ ----------

        void Rates() => App.Modals.Open(p.ratesDialog).Show(D.Cfg);

        // ---------- rời máy ----------

        public override void Exit()
        {
            leaving = true;
            holding = false;
            autoLeft = 0;
            partyT = 0;
            if (board != null) UpdateDomes(0); // nắp nút thả bật lên, chữ về chỗ
            slowT = 0;
            giftBusy = 0;
            giftPopT = giftPunchT = counterPopT = -1;
            if (p.expBar) p.expBar.Clear();
            if (board == null) return;
            var s = S;
            // bi còn lăn: tính như rơi vào ô EXP 10 (EXP 10 × mức cược)
            foreach (var b in board.balls) Pachinko.SlotReward(s, D.Cfg, SlotKind.Exp10, b.mult);
            board.balls.Clear();
            session = 0;
            if (bigReward != null)
            {
                var h = D.Hero(bigReward.hero);
                App.Toasts.Show(bigReward.k == RewardKind.Hero ? $"Mốc {D.Cfg.legendMilestone} bi: nhận {h.name}!" : $"+{bigReward.n} bản sao thẻ Huyền thoại của {h.name}", App.Art.Icon("star"));
                bigReward = null;
            }
            if (lvFrom >= 0 && s.level > lvFrom) App.Toasts.Show($"Lên cấp {s.level}!", App.Art.Icon("exp"));
            lvFrom = -1;
            SaveNow();
        }
    }
}
