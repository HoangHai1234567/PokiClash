// Máy bi: bấm thả thì bi phóng lên làn phải, ra bàn ở hốc trên phải, dội qua đinh và nấm rồi rơi vào ô EXP / rương (bàn chép máy
// tham khảo, Core/Pachinko.cs). Ô rơi chọn theo bảng tỉ lệ cfg.odds rồi phát đường bi vật lý rơi đúng ô đó; lúc rảnh, máy thử sẵn
// vài đường mỗi khung (Board.Warm) để lúc phóng lấy ngay. Hai nấm lớn có vòng tiến độ (cfg.rings): mỗi lần chạm cộng nấc theo
// cược, đầy thì ra quà (rương vào khay, bi về dòng đếm).
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
// Đang thả (từ bi đầu tới khi đợt xong hẳn: bi rơi hết, bảng số đổ EXP, mở rương, Lên cấp) thì khoá mọi nút trừ Thả bi / Thả liền
// (2026-11-20): bảng tỉ lệ, cược, khay rương, thanh mốc quà, nút quay lại và phím Back. Nút khoá mờ, chạm im lặng (SketchButton.Locked).
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
        const double Tick = Board.Dt;
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
            // bản 2 (concept 2, GD_Claude/23, menu "PokiClash/Prefab/Máy bi: bố cục bản 2"): chỗ bảng số trên đỉnh vòm (bảng dựng lúc vào
            // màn đúng chỗ này, thanh kinh nghiệm không dời), khung khay (chỉ hiện rương bậc cao nhất kèm tổng số, chạm mở cả khay), viên
            // cược bấm đổi mức (thay cột cược), ảnh của viên. Bóng đèn bulbs khi đó là lớp sáng fx2_den_* phủ bóng vẽ sẵn trên thân máy.
            public RectTransform scoreSlot, trayFrame;
            public SketchButton betCycle;
            public UnityEngine.UI.Image betCycleArt;
        }

        [SerializeField] Parts p;
        bool V2 => p.scoreSlot;

        Board board;
        MachineBoard view;
        MachineScoreBoard score; // bảng số dưới thanh kinh nghiệm (dựng lúc vào màn)
        UnityEngine.UI.Button barBtn; // chạm thanh mốc (như ô quà)
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
        readonly Dictionary<int, int> pegHits = new Dictionary<int, int>(); // bi id → số lần chạm đinh (tiếng cao dần)

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

        // đang thả: từ bi đầu của đợt tới khi đợt xong hẳn (cả lúc mở rương từ khay); trong lúc này chỉ nút thả nhận chạm
        bool Busy => session > 0 || ending || opening;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        public override void Enter(object args)
        {
            rng = new Rng(Rng.RandomSeed());
            board = new Board(Rng.RandomSeed()) { odds = D.Cfg.odds.Length > 0 ? D.Cfg.odds : null };
            view = p.machine;
            view.Bind(board);
            for (int i = 0; i < D.Cfg.rings.Count && i < S.rings.Length; i++)
            {
                view.RingReward(i, D.Cfg.rings[i]);
                view.SetRing(i, RingFill(i), true);
            }
            view.Hold.Down = StartHold;
            view.Hold.Up = () => holding = false;

            p.rates.SetOnClick(Rates);
            BindBets();
            if (p.betCycle) p.betCycle.SetOnClick(CycleBet);
            foreach (var b in p.tray) b.SetOnClick(OpenFromTray);
            p.drop.ClickSound = null;
            p.dropHold.Down = StartHold;
            p.dropHold.Up = () => holding = false;
            p.auto.SetOnClick(Auto);
            if (p.giftButton) p.giftButton.onClick.AddListener(GiftInfo);
            barBtn = p.legendBar.GetComponent<UnityEngine.UI.Button>();
            if (barBtn) barBtn.onClick.AddListener(GiftInfo);
            x = Progress.XBest(S, D.Cfg, lastX);
            maxX = Progress.XBest(S, D.Cfg, int.MaxValue);
            giftShown = null;
            if (p.expBar)
            {
                p.expBar.Bind();
                p.expBar.LeveledUp -= OnBarLevel;
                p.expBar.LeveledUp += OnBarLevel;
            }
            BuildScore();
            RefreshUi();
            view.SetMult(x, false);
            RebuildTray();
        }

        // bảng số (chép bảng LED của máy tham khảo): chiếm chỗ thanh kinh nghiệm ở đầu máy (vòng cấp + rãnh), cao tới mép trên mặt
        // chơi; thanh dời lên vòm tủ, nằm trên bảng. Màn dùng lại thì giữ bảng cũ (thanh đã dời).
        void BuildScore()
        {
            if (!p.expBar) return;
            var bar = (RectTransform)p.expBar.transform;
            var block = bar.parent as RectTransform;
            var old = block ? block.Find("bang_so") : null;
            if (old)
            {
                score = old.GetComponent<MachineScoreBoard>();
                if (score) score.Clear();
                return;
            }
            if (!block || !view.FloatTextPrefab) return;
            if (V2)
            {
                // bản 2: bảng to trên đỉnh vòm, đúng chỗ dựng sẵn; thanh kinh nghiệm ở trên cùng, không dời
                var slot = p.scoreSlot;
                var sr = new Rect(slot.anchoredPosition.x - slot.pivot.x * slot.rect.width, -slot.anchoredPosition.y - (1 - slot.pivot.y) * slot.rect.height,
                    slot.rect.width, slot.rect.height);
                score = MachineScoreBoard.Build(block, sr, view.FloatTextPrefab);
                if (score) score.Rect.SetSiblingIndex(slot.GetSiblingIndex() + 1);
                return;
            }
            var ap = bar.anchoredPosition;
            var size = bar.rect.size;
            float y = -ap.y - 2;
            var r = new Rect(ap.x - 6, y, size.x + 12, MachineTop + 4 - y);
            score = MachineScoreBoard.Build(block, r, view.FloatTextPrefab);
            if (!score) return; // chưa có prefab bảng số: EXP bay thẳng lên thanh như cũ
            score.Rect.SetSiblingIndex(bar.GetSiblingIndex()); // thanh vẽ đè lên bảng
            bar.anchoredPosition = ap + new Vector2(0, size.y + 2);
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
            bool idle = !Busy;
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
                    var nb = p.betCycle ? p.betCycle : xBtns.Find(q => q.x == top).b;
                    if (nb) StartCoroutine(PopRect(nb.Rect, !p.betCycle && top == x ? 1.08f : 1f));
                }
                maxX = top;
            }
            view.SetMult(x, false);
            view.LowFlash = s.settings.lowFlash;
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
            if (p.betCycle)
            {
                // viên cược bản 2: một viên, chữ ×N, bấm đổi sang mức mở kế tiếp
                p.betCycle.SetColor(Clear);
                p.betCycle.SetText("×" + x);
                p.betCycle.Interactable = true;
                if (p.betCycleArt) SetSprite(p.betCycleArt, "pk_v2_cuoc");
            }
            // thanh đếm bản 2 có icon bi ở đầu: chỉ số; bản cũ: câu đủ
            p.counter.text = V2 ? (session > 0 ? $"{session}/{max}" : $"{s.balls}") : session > 0 ? $"Đợt này: {session}/{max}" : $"{s.balls} bi · tốn {x}/lần";
            p.auto.SetText(V2 ? $"Liền ×{max}" : p.autoDome ? $"Thả liền\n{max}" : $"Thả liền {max}"); // bản 2: chú thích dưới nút
            if (p.dropDome) p.drop.SetColor(Clear);
            else p.drop.SetColor(CanDrop() ? Theme.Red : Color.Lerp(Theme.Red, Theme.Paper3, 0.6f));
            if (p.autoDome) p.auto.SetColor(Clear);
            UpdateDomes(0);
            RefreshMilestone();
            Lock(!idle);
        }

        // khoá mọi nút trừ Thả bi / Thả liền (mờ, chạm im lặng), cả nút quay lại trên thanh trên; phím Back chặn ở OnBack.
        // Thanh mốc quà chỉ thôi nhận chạm, không mờ (vẫn chạy theo từng bi).
        void Lock(bool on)
        {
            if (p.rates) p.rates.Locked = on;
            foreach (var q in xBtns) q.b.Locked = on;
            if (p.betCycle) p.betCycle.Locked = on;
            foreach (var b in p.tray) b.Locked = on;
            if (p.giftButton) p.giftButton.interactable = !on;
            if (barBtn) barBtn.interactable = !on;
            if (App.Bars) App.Bars.LockBack(on);
            TrayRigs(!on);
        }

        // rương chờ trong khay (rig AtomSpine, GD_Claude/23): máy rảnh thì nhắc mở (nhún, lắc, nắp hé có sáng ấm lọt khe), các nút lệch
        // nhịp nhau cho khỏi nhảy cùng lúc; đang thả, đang mở thì chỉ đứng thở. Thiếu rig thì ảnh tĩnh như cũ.
        void TrayRigs(bool idle)
        {
            if (p.tray == null) return;
            for (int i = 0; i < p.tray.Length; i++)
            {
                var b = p.tray[i];
                if (!b || !b.gameObject.activeInHierarchy) continue;
                var ic = b.GetComponentInChildren<ChestIcon>(true);
                if (!ic) continue;
                // icon khay nướng sẵn trong prefab: gán bậc một lần trong lần chạy này (Kind, ảnh gen không lưu trong prefab)
                if (!ic.Bound || ic.Kind != TrayKinds[i]) ic.Bind(TrayKinds[i], ic.Rect.sizeDelta.x);
                ic.PlayRig(idle ? "nhac" : "cho", true, idle ? i * 1.07f : 0);
            }
        }

        // nút vòm: đang giữ thì nắp lún (chữ dời xuống theo nắp) và vòng đứt nhịp ra ngoài 0,4 giây một nhịp; hết bi hay hết lượt
        // đợt thì nắp xám; cược lớn nắp vàng có sao. Nút thả liền: đang thả liền thì nắp lún xanh ngọc.
        void UpdateDomes(float dt)
        {
            if (p.dropDome && V2)
            {
                // nút PUSH bản 2 (vòm sao vàng; lún, xám, hồng cược lớn). Nhịp của nút máy tham khảo: rảnh thì cứ 15 giây nhảy một lần
                // ở giây 13,48 (cao ×1,038 → 0,988 → 1,027 → 1 trong 0,42 giây); đang giữ thì ảnh lún, thấp thêm chút
                bool down = holding;
                bool ready = CanDrop();
                SetSprite(p.dropDome, down ? "pk_push_lun" : !ready ? "pk_push_het" : x >= BigBet ? "pk_push_lon" : "pk_push_thuong");
                float sy = 1;
                if (down) sy = 0.96f;
                else if (ready && session == 0)
                {
                    float c = time % 15f - 13.48f;
                    if (c >= 0 && c < 0.42f) sy = MachineFx.Curve(PushHop, c);
                }
                var dr = p.dropDome.rectTransform;
                dr.localScale = new Vector3(1 + (1 - sy) * 0.4f, sy, 1);
            }
            else if (p.dropDome)
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
            if (p.autoDome) SetSprite(p.autoDome, V2 ? (autoLeft > 0 ? "pk_v2_lien_bat" : "pk_v2_lien") : autoLeft > 0 ? "pk_nut_lien_bat" : "pk_nut_lien");
        }

        static readonly float[] PushHop = { 0, 1, 0.1f, 1.038f, 0.2f, 0.988f, 0.31f, 1.027f, 0.42f, 1 };

        // ---------- kịch bản đèn vòm (GD_Claude/23 giai đoạn 2) ----------
        // nền theo trạng thái: hết bi / hết lượt thì chạy chậm, thưa (1 bóng trong 5); sẵn sàng thì cứ ba bóng sáng một chạy 3,5 bước/giây
        // (cược lớn 6) và mỗi 6 giây một đợt sóng quét qua cả dãy; đang thả 9 bước/giây. Đè lên trên là đợt diễn một lần: quét (ô EXP),
        // toả từ giữa hai lần (rương gỗ, bạc), dồn từ hai đầu vào giữa rồi nháy (lên cấp), nháy xen vàng hồng (jackpot, partyT).
        enum BulbShow { None, Sweep, Center, Fill, Tease }
        BulbShow show;
        float showT, waveT;

        void Show(BulbShow s)
        {
            if (partyT > 0 && s != BulbShow.Tease) return; // đang nháy jackpot: để yên
            show = s;
            showT = 0;
        }

        void UpdateBulbs(float dt)
        {
            if (p.bulbs == null || p.bulbs.Length == 0) return;
            int n = p.bulbs.Length;
            bool low = S.settings.lowFlash;
            bool ready = CanDrop();
            bulbStep += dt * (session > 0 ? 9 : !ready ? 1.5f : x >= BigBet ? 6 : 3.5f);
            if (partyT > 0) partyT -= dt;
            waveT += dt;
            if (show != BulbShow.None) showT += dt;
            int step = (int)bulbStep;
            for (int i = 0; i < n; i++)
            {
                var b = p.bulbs[i];
                if (!b) continue;
                if (!b.gameObject.activeSelf) b.gameObject.SetActive(true);
                int lit = 0; // 0 tắt, 1 vàng, 2 hồng
                if (partyT > 0)
                {
                    // jackpot: hai nửa dãy đổi màu cho nhau 8 lần/giây (giảm nhấp nháy: 3 lần/giây, cả dãy sáng)
                    int ph = (int)(partyT * (low ? 3 : 8));
                    lit = low ? (ph % 2 == 0 ? 1 : 2) : ((i + ph) % 2 == 0 ? 1 : 2);
                }
                else if (show == BulbShow.Tease)
                {
                    // báo trước jackpot: đèn dồn về giữa ngày càng nhanh
                    float sp = 10 + showT * 30;
                    int mid = n / 2, d = Mathf.Abs(i - mid);
                    lit = ((int)(showT * sp) - d) % 3 == 0 ? 1 : 0;
                    if (showT > 1.6f) show = BulbShow.None;
                }
                else if (show == BulbShow.Sweep)
                {
                    float head = showT / 0.5f * (n + 3);
                    float g = head - i;
                    lit = g >= 0 && g < 3 ? 1 : 0;
                    if (showT > 0.6f) show = BulbShow.None;
                }
                else if (show == BulbShow.Center)
                {
                    float r = showT % 0.45f / 0.45f * (n / 2 + 2);
                    float d = Mathf.Abs(i - (n - 1) / 2f);
                    lit = Mathf.Abs(d - r) < 1.2f ? 2 : 0;
                    if (showT > 0.9f) show = BulbShow.None;
                }
                else if (show == BulbShow.Fill)
                {
                    float f = showT / 0.6f * (n / 2 + 1);
                    float d = Mathf.Min(i, n - 1 - i);
                    lit = showT < 0.6f ? (d < f ? 1 : 0) : ((int)((showT - 0.6f) * (low ? 3 : 8)) % 2 == 0 ? 1 : 0);
                    if (showT > 1.1f) show = BulbShow.None;
                }
                else if (session == 0 && ready && waveT % 6f < 0.6f)
                {
                    // rảnh mà còn bi: sóng quét qua cả dãy mỗi 6 giây, mời thả
                    float g = waveT % 6f / 0.6f * (n + 3) - i;
                    lit = g >= 0 && g < 3 ? 2 : (((i - step) % 3 + 3) % 3 == 0 ? 1 : 0);
                }
                else if (V2 && (ready || session > 0))
                {
                    // bản 2: hai nhóm xen kẽ như vòm 87 bóng của máy tham khảo (bản đục 2026-11-20). Rảnh: chu kỳ 1,43 giây (cả hai
                    // nhóm 0,31 → A 0,54 → B 0,54); đang thả: 0,5 giây (A 0,2 → tối 0,05 → B 0,2 → tối 0,05). Cứ 5 bóng một bóng hồng.
                    int g;
                    if (session > 0)
                    {
                        float c = time % 0.5f;
                        g = c < 0.2f ? 0 : c < 0.25f ? -1 : c < 0.45f ? 1 : -1;
                    }
                    else
                    {
                        float c = time % 1.43f;
                        g = c < 0.31f ? 2 : c < 0.85f ? 0 : c < 1.39f ? 1 : 2;
                    }
                    lit = g == 2 || g >= 0 && i % 2 == g ? (i % 5 == 2 ? 2 : 1) : 0;
                }
                else
                {
                    int every = ready || session > 0 ? 3 : 5;
                    lit = ((i - step) % every + every) % every == 0 ? (i % 2 == 0 ? 1 : 2) : 0;
                }
                if (V2)
                {
                    // lớp sáng phủ bóng vẽ sẵn: tắt là trong suốt
                    SetSprite(b, lit == 2 ? "fx2_den_hong" : "fx2_den_vang");
                    float a = lit == 0 ? 0 : 1;
                    if (b.color.a != a) b.color = new Color(1, 1, 1, a);
                }
                else SetSprite(b, lit == 0 ? "pk_den_tat" : lit == 1 ? "pk_den_sang" : "pk_den_sang_hong");
            }
        }

        // ---------- báo trước jackpot, đèn chạy qua ô (GD_Claude/23 giai đoạn 2, 3) ----------
        // kết quả mỗi bi đã chọn trước (Ball.target), nên biết trước bi nào vào ô rương vàng: còn khoảng 0,6 giây (bi xuống thấp)
        // thì đèn dồn về giữa, máy chậm dần, khối máy phóng to nhẹ về phía ô, tiếng tích tắc cao dần. Bi rơi đúng ô đó (thật, không phải
        // "suýt trúng"). Thả một bi (không thả liền) thì đèn chạy qua các ô khi bi xuống thấp, dừng ở ô thật lúc bi rơi.
        readonly HashSet<int> teased = new HashSet<int>();
        int rolledFor = -1;
        float teaseT, tickT, tickPitch;
        RectTransform zoomRoot;
        Vector2 zoomPos0, zoomPivot;
        Vector3 zoomScale0;
        float zoomCur = 1, zoomWant = 1;
        const float TeaseY = 175, RollY = 260, ZoomMax = 1.06f; // RollY: bắt đầu chạy qua ô khi bi còn cách miệng ô chừng này (khoảng 0,7 giây)

        int GoldSlot()
        {
            for (int i = 0; i < board.slots.Count; i++)
                if (board.slots[i].reward == SlotKind.ChestGold) return i;
            return -1;
        }

        void WatchBalls(float dt)
        {
            int gold = GoldSlot();
            Ball single = board.balls.Count == 1 ? board.balls[0] : null;
            foreach (var b in board.balls)
            {
                if (b.lane >= 0 || b.target < 0 || b.target >= board.slots.Count) continue;
                var sl = board.slots[b.target];
                if (b.target == gold && !teased.Contains(b.id) && b.y > sl.y0 - TeaseY)
                {
                    teased.Add(b.id);
                    StartTease(b.target);
                }
            }
            // đèn chạy qua ô: chỉ khi một bi (thả liền nhiều bi thì rối), bi không vào ô jackpot (đã có báo trước riêng)
            if (single != null && single.lane < 0 && single.target >= 0 && single.target < board.slots.Count && single.target != gold &&
                rolledFor != single.id && single.y > board.slots[single.target].y0 - RollY)
            {
                rolledFor = single.id;
                view.StartRoll();
            }
            if (teaseT > 0)
            {
                teaseT -= dt;
                tickT -= dt;
                if (tickT <= 0)
                {
                    tickT = 0.085f;
                    tickPitch = Mathf.Min(2f, tickPitch + 0.07f);
                    App.Audio.Play("pick", 0.5f, tickPitch);
                }
            }
            UpdateZoom(dt);
        }

        void OnBarLevel() => Show(BulbShow.Fill);

        void StartTease(int slot)
        {
            Show(BulbShow.Tease);
            teaseT = 0.75f;
            tickT = 0;
            tickPitch = 1f;
            Haptics.Play(Haptic.Peg);
            if (!S.settings.lowFlash) ZoomTo(slot, ZoomMax);
        }

        // phóng khối máy quanh miệng ô (giữ điểm đó đứng yên); scale 1 = trả về
        void ZoomTo(int slot, float scale)
        {
            if (!zoomRoot)
            {
                zoomRoot = view ? view.Root.parent as RectTransform : null;
                if (!zoomRoot) return;
                zoomPos0 = zoomRoot.anchoredPosition;
                zoomScale0 = zoomRoot.localScale;
            }
            if (slot >= 0 && slot < board.slots.Count)
            {
                var sl = board.slots[slot];
                zoomPivot = zoomRoot.InverseTransformPoint(view.World((sl.x0 + sl.x1) / 2, sl.y0));
            }
            zoomWant = scale;
        }

        void UpdateZoom(float dt)
        {
            if (!zoomRoot || Mathf.Approximately(zoomCur, zoomWant)) return;
            zoomCur = Mathf.MoveTowards(zoomCur, zoomWant, dt * (zoomWant > zoomCur ? 0.12f : 0.1f));
            zoomRoot.localScale = zoomScale0 * zoomCur;
            zoomRoot.anchoredPosition = zoomPos0 + (1 - zoomCur) * zoomPivot;
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
                p.legendBar.Set(Mathf.Min(s.ballsSpent, need), need, 0, V2 ? $"{Mathf.Min(s.ballsSpent, need)}/{need} bi" : $"Huyền thoại: {Mathf.Min(s.ballsSpent, need)}/{need} bi");
                ShowGift("legend", null);
            }
            else if (gifts)
            {
                if (giftBusy > 0) p.legendBar.Set(1, 1, 0, "Nhận quà!");
                else
                {
                    p.legendBar.Set(s.gift, g.n, 0, V2 ? $"{s.gift}/{g.n} bi" : $"{Pachinko.GiftName(g)}: {s.gift}/{g.n} bi"); // bản 2: thanh hẹp, quà đã vẽ ở ô quà
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
            if (Busy) return;
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

        // viên cược bản 2: bấm thì sang mức mở kế tiếp (hết thì về ×1); viên nhún như nút cược máy tham khảo (cao 0,9 → 1,1 → 1 trong
        // 0,167 giây). Còn mức chưa đủ bi: lúc quay về ×1 báo mức kế cần bao nhiêu bi.
        void CycleBet()
        {
            if (Busy) return;
            var allowed = Progress.XAllowed(S, D.Cfg);
            var steps = D.Cfg.xSteps;
            if (steps.Count == 0) return;
            int i = steps.FindIndex(q => q.x == x);
            int next = -1;
            for (int k = i + 1; k < steps.Count; k++)
                if (allowed.Contains(steps[k].x))
                {
                    next = k;
                    break;
                }
            if (next < 0)
            {
                var locked = steps.Find(q => !allowed.Contains(q.x));
                if (locked != null) App.Toasts.Show($"Có {locked.balls} bi để mở ×{locked.x} (đang có {S.balls})", App.Art.Icon("ball"));
                next = 0;
            }
            PickX(steps[next].x, steps[next].balls);
            StartCoroutine(BetSquash(p.betCycle.Rect));
        }

        static IEnumerator BetSquash(RectTransform r)
        {
            for (float t = 0; t < 0.167f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.167f;
                float sy = k < 0.4f ? Mathf.Lerp(1, 0.9f, k / 0.4f) : k < 0.75f ? Mathf.Lerp(0.9f, 1.1f, (k - 0.4f) / 0.35f) : Mathf.Lerp(1.1f, 1, (k - 0.75f) / 0.25f);
                r.localScale = new Vector3(1 + (1 - sy) * 0.5f, sy, 1);
                yield return null;
            }
            r.localScale = Vector3.one;
        }

        void PickX(int bx, int need)
        {
            if (Busy) return; // nút đã khoá, chặn thêm cho công cụ bấm hộ
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
            if (p.trayFrame)
            {
                // bản 2: khung khay chỉ hiện rương bậc cao nhất đang có, số là tổng rương trong khay (chạm mở cả khay)
                int total = S.chests.Count, first = -1;
                for (int i = 0; i < TrayKinds.Length && i < p.tray.Length; i++)
                {
                    string key = Pachinko.Key(TrayKinds[i]);
                    bool has = S.chests.Any(c => c.kind == key);
                    if (has && first < 0) first = i;
                    var b = p.tray[i];
                    b.gameObject.SetActive(has && first == i);
                    if (first != i) continue;
                    p.trayCounts[i].text = "×" + total;
                    // nằm thẳng trên ván gỗ của khung: bỏ nền giấy của nút, rương vào giữa khung (bù chỗ icon lệch trong nút)
                    b.SetColor(Clear);
                    var ic = b.GetComponentInChildren<ChestIcon>(true);
                    if (ic)
                    {
                        Vector2 off = b.Rect.InverseTransformPoint(ic.Rect.TransformPoint(ic.Rect.rect.center));
                        off -= b.Rect.rect.center;
                        b.Rect.anchoredPosition = new Vector2(-off.x * b.Rect.localScale.x, 6);
                    }
                }
                p.trayEmpty.SetActive(first < 0);
                TrayRigs(!Busy);
                return;
            }
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
            TrayRigs(!Busy);
        }

        Vector3 TrayPoint() => p.trayFrame ? p.trayFrame.TransformPoint(p.trayFrame.rect.center) : p.trayCol.TransformPoint(new Vector3(0, -100, 0));

        // ---------- thả ----------

        bool CanDrop() => !ending && !opening && S.balls >= x && session < D.Cfg.MaxPerDrop(S.level);

        static float RingFill(int i) => i < D.Cfg.rings.Count && D.Cfg.rings[i].n > 0 ? (float)S.rings[i] / D.Cfg.rings[i].n : 0;

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
            board.Launch(x);
            view.Launch();
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
                foreach (var e in board.Step())
                {
                    if (!e.land)
                    {
                        view.Flash(e.peg);
                        // tiếng đinh cao dần theo số lần chạm của chính bi đó (GD_Claude/23 giai đoạn 4)
                        pegHits.TryGetValue(e.ball.id, out var hits);
                        pegHits[e.ball.id] = ++hits;
                        if (App.Audio.Peg((float)e.speed, hits)) Haptics.Play(Haptic.Peg);
                        int ring = System.Array.IndexOf(board.ringPeg, e.peg);
                        if (ring >= 0) RingHit(ring, e.ball.mult);
                    }
                    else
                    {
                        pegHits.Remove(e.ball.id);
                        OnLand(e.reward, e.slot, e.ball.x, e.ball.y, e.ball.mult);
                    }
                }
            }
            WatchBalls(dt);
            view.Blend = Mathf.Clamp01((float)(acc / Tick));
            // rảnh tay (không chạy chậm): thử sẵn vài đường bi cho các ô còn thiếu trong kho
            if (slowT <= 0) board.Warm(2);
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
            view.Sync(dt, dt * sim, CanDrop() ? x : 0);
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

        // ---------- vòng nấm ----------

        // bi chạm nấm lớn: vòng cộng nấc (×cược); đầy thì nấm phồng, loé, quà bay ra từ nấm (rương vào khay, bi về dòng đếm)
        void RingHit(int ring, int mult)
        {
            var got = Pachinko.RingHit(S, D.Cfg, ring, mult);
            var pg = board.pegs[board.ringPeg[ring]];
            if (got.Count > 0) view.RingFull(ring);
            view.SetRing(ring, RingFill(ring));
            dirty = true;
            foreach (var g in got)
            {
                var from = view.World(pg.x, pg.y);
                switch (g.k)
                {
                    case RewardKind.Chest:
                        S.chests.Add(new PendingChest { kind = Pachinko.Key(g.chest), x = 1 });
                        view.Float(pg.x, pg.y - pg.r - 8, Pachinko.ChestName(g.chest) + "!", MachineBoard.ChestColor(g.chest), 28);
                        App.Audio.Play("chest", 0.9f, 1.1f);
                        Haptics.Play(Haptic.LandSilver);
                        StartCoroutine(FlyChest(g.chest, from));
                        SaveNow();
                        break;
                    case RewardKind.Balls:
                        view.Float(pg.x, pg.y - pg.r - 8, $"+{g.n} bi", MachineBoard.BallPink, 28);
                        App.Audio.Play("coin", 0.9f, 1.15f);
                        Haptics.Play(Haptic.LandSmall);
                        FlyBalls(from, g.n);
                        break;
                    case RewardKind.Exp:
                        view.Float(pg.x, pg.y - pg.r - 8, $"+{g.n} XP", MachineBoard.XpColor, 28);
                        GainExp(from, g.n);
                        App.Audio.Play("land");
                        break;
                }
            }
        }

        // ---------- bi rơi ----------

        void OnLand(SlotKind kind, int slot, double bx, double by, int mult)
        {
            var r = Pachinko.SlotReward(S, D.Cfg, kind, mult);
            bool gold = kind == SlotKind.ChestGold;
            view.StopRoll(); // đèn chạy qua ô dừng ở ô thật
            // đèn vòm diễn một lần theo giá trị: ô thường quét, rương gỗ / bạc toả từ giữa (jackpot nháy riêng trong Jackpot)
            if (!gold) Show(r.k == RewardKind.Chest ? BulbShow.Center : BulbShow.Sweep);
            if (slot >= 0)
            {
                view.Glow(slot, gold ? 2 : r.k == RewardKind.Chest ? 1 : 0);
                view.SlotFx(slot);
            }
            else view.CupFx(bx, by);
            switch (r.k)
            {
                case RewardKind.Exp:
                    // ô EXP: kẹo phụt, cụm "kẹo + số" bật ở miệng ô; kẹo bay về bảng số khi cụm vừa bật xong (0,3 giây)
                    if (slot >= 0) view.ExpPop(slot, bx, by, r.n);
                    else view.Float(bx, by - 20, $"+{r.n} XP", MachineBoard.XpColor);
                    GainExp(view.World(bx, by - 24), r.n, slot >= 0 ? 0.3f : 0);
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
                    if (gold) Jackpot(bx, by - 10, col, slot);
                    else Haptics.Play(kind == SlotKind.ChestSilver ? Haptic.LandSilver : Haptic.LandWood);
                    SaveNow();
                    StartCoroutine(FlyChest(kind, view.World(bx, by)));
                    break;
            }
        }

        // EXP rơi vào ô / từ nấm: kẹo bay lên bảng số (hết đợt bảng mới đổ lên thanh); không có bảng thì bay thẳng lên thanh
        void GainExp(Vector3 from, int n, float delay = 0)
        {
            if (!p.expBar) return;
            if (score) score.Receive(p.expBar, from, n, delay);
            else p.expBar.Fly(from, n);
        }

        // rương vàng: chạy chậm, rung mặt máy, vòng loé thứ hai to hơn, ba tiếng xu lên cao dần
        void Jackpot(double bx, double by, Color col, int slot = -1)
        {
            bool low = S.settings.lowFlash;
            slowT = SlowHold + SlowRamp;
            view.Shake(low ? ShakeAmp * 0.4f : ShakeAmp, ShakeTime);
            view.Burst(bx, by, col, 1.8f);
            view.JackpotFx(bx, by);
            partyT = low ? 1.6f : 1.8f;
            show = BulbShow.None;
            Haptics.Play(Haptic.LandGold);
            StartCoroutine(Jingle());
            // GD_Claude/23 giai đoạn 3: chữ "JACKPOT!" nảy từng chữ giữa máy, vòi xu phun từ ô, khối máy về cỡ cũ sau khi mừng
            view.Banner("JACKPOT!", Theme.Hex("#ffd84a"));
            if (slot >= 0) view.CoinFountain(slot);
            StartCoroutine(ZoomBack(1.1f));
        }

        IEnumerator ZoomBack(float after)
        {
            yield return new WaitForSecondsRealtime(after);
            if (!leaving) ZoomTo(-1, 1);
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
            // bảng số đổ EXP của đợt lên thanh (kẹo bay từ bảng tới đầu thanh, số đếm lùi)
            if (score && p.expBar && !leaving) yield return score.Collect(p.expBar);
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
            if (S.chests.Count == 0 || Busy) return;
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
                // mở theo nhóm tối đa 5 rương như màn mở capsule của máy tham khảo; rương quý trước, cùng loại theo thứ tự rơi vào
                var group = S.chests.OrderBy(q => Rank(q.kind)).Take(5).ToList();
                var items = new List<MachineChestOpen.Item>();
                foreach (var c in group)
                {
                    S.chests.Remove(c);
                    var kind = Pachinko.FromKey(c.kind);
                    int cx = Mathf.Max(1, c.x);
                    items.Add(new MachineChestOpen.Item { kind = kind, x = cx, rewards = Pachinko.OpenChest(S, D, kind, cx, rng) });
                }
                SaveNow();
                RebuildTray();
                int left = S.chests.Count;
                // EXP trong rương: bản lưu đã cộng, thanh giữ lại tới khi đóng màn mở rương rồi mới nhận theo chùm kẹo toả ra từ giữa màn
                int chestExp = items.Sum(it => it.rewards == null ? 0 : it.rewards.Where(r => r.k == RewardKind.Exp).Sum(r => r.n));
                if (p.expBar && chestExp > 0) p.expBar.Held += chestExp;
                if (Frame && view.FloatTextPrefab && view.ParticlePrefab && MachineChestOpen.Ready)
                    yield return MachineChestOpen.Play(Frame, items, left, TrayPoint(), view.FloatTextPrefab, view.ParticlePrefab);
                else
                    foreach (var it in items)
                        yield return ChestBox.Show(Pachinko.ChestName(it.kind) + (it.x > 1 ? $" ×{it.x}" : ""), it.kind, null, it.rewards, "Nhận");
                if (p.expBar && chestExp > 0)
                {
                    int k = MachineExpBar.SprayCount(chestExp), total = chestExp;
                    var bar = p.expBar;
                    bar.Spray(MachineScoreBoard.Candy, Frame ? Frame.position : bar.TipWorld, () => bar.TipWorld, k, 0.05f,
                        i => bar.Deposit(MachineExpBar.Part(total, k, i)), 62, 150);
                }
                RefreshUi();
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

        void Rates()
        {
            if (Busy) return;
            App.Modals.Open(p.ratesDialog).Show(D.Cfg);
        }

        // ---------- rời máy ----------

        // nút quay lại / phím Back: chặn trong lúc đang thả (hộp đang mở vẫn đóng được: App.Back đóng hộp trước khi gọi tới đây)
        public override void OnBack()
        {
            if (Busy) return;
            base.OnBack();
        }

        public override void Exit()
        {
            leaving = true;
            holding = false;
            autoLeft = 0;
            partyT = 0;
            show = BulbShow.None;
            teaseT = 0;
            pegHits.Clear();
            if (view) view.StopRoll();
            if (zoomRoot) // khối máy về cỡ, chỗ cũ (đang phóng to báo trước jackpot)
            {
                zoomRoot.localScale = zoomScale0;
                zoomRoot.anchoredPosition = zoomPos0;
                zoomCur = zoomWant = 1;
            }
            Lock(false);
            if (board != null) UpdateDomes(0); // nắp nút thả bật lên, chữ về chỗ
            slowT = 0;
            giftBusy = 0;
            giftPopT = giftPunchT = counterPopT = -1;
            if (p.expBar) p.expBar.Clear();
            if (score) score.Clear();
            if (board == null) return;
            var s = S;
            // bi còn bay: tính như đã rơi vào ô đã chọn cho nó (vật lý thuần thì EXP 10), rương vào hàng chờ
            foreach (var b in board.balls)
            {
                var kind = b.target < 0 ? SlotKind.Exp10 : b.target < board.slots.Count ? board.slots[b.target].reward : board.cups[b.target - board.slots.Count].reward;
                if (Pachinko.SlotReward(s, D.Cfg, kind, b.mult).k == RewardKind.Chest) s.chests.Add(new PendingChest { kind = Pachinko.Key(kind), x = b.mult });
            }
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
