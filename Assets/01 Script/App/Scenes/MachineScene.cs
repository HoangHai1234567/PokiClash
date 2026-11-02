// Máy bi: thả bi qua đinh, rơi vào ô EXP / hoàn bi / rương (chép Web/src/view/screens/machine.ts).
// Nút ×N là mức cược: tốn N bi mỗi lần thả, thưởng ×N. Mỗi đợt tối đa MaxPerDrop(cấp) bi; đợt xong (mọi bi đã rơi) thì mở
// lần lượt rương trong khay, rồi hộp "Huyền thoại!" (nếu vừa vượt mốc), rồi "Lên cấp!". Rương chờ nằm trong bản lưu.
// Prefab màn hình Assets/04 Prefabs/Screens/Machine (mặt máy, cột cược, khay rương 3 nút dựng sẵn, nút thả); hộp Dialogs/TiLeMayBi, Dialogs/HuyenThoai.
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
            public TextMeshProUGUI[] betLocks; // chữ "Cấp n" trên nút cược chưa mở
            public SketchButton[] tray; // nút khay theo TrayKinds
            public TextMeshProUGUI[] trayCounts; // "×n" trên nút khay
            public GameObject trayEmpty; // "(trống)"
            public TextMeshProUGUI counter, legendText;
            public UiBar legendBar;
            public MachineRatesDialog ratesDialog;
            public LegendMilestoneDialog legendDialog;
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
            x = lastX;
            RefreshUi();
            RebuildTray();
        }

        // bản lưu đổi từ nơi khác (bảng thử, thanh trên): làm mới; khay chỉ dựng lại khi máy rảnh (trong đợt, rương bay vào rồi mới hiện)
        public override void Refresh()
        {
            RefreshUi();
            if (session == 0 && !ending && !opening) RebuildTray();
        }

        // nút cược dựng sẵn theo cfg.xSteps lúc nướng: gán lại mức và cấp mở theo dữ liệu, nút thừa ẩn
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
                int bx = steps[i].x, lv = steps[i].lv;
                b.name = "cuoc_x" + bx;
                b.SetText("×" + bx);
                b.SetOnClick(() => PickX(bx, lv));
                p.betLocks[i].text = $"Cấp {lv}";
                xBtns.Add((b, p.betLocks[i], bx));
            }
        }

        // ---------- giao diện ----------

        void RefreshUi()
        {
            if (board == null) return;
            var s = S;
            var allowed = Progress.XAllowed(s, D.Cfg);
            if (!allowed.Contains(x)) x = 1;
            foreach (var (b, lockText, bx) in xBtns)
            {
                bool ok = allowed.Contains(bx);
                b.Interactable = ok;
                if (ok) b.SetColor(bx == x ? Theme.Yellow : Theme.Paper);
                b.Rect.localScale = Vector3.one * (bx == x ? 1.08f : 1f);
                lockText.gameObject.SetActive(!ok);
                if (ok) b.Label.rectTransform.Stretch(8, 4, 14, 14);
                else b.Label.rectTransform.Stretch(8, 0, 14, 40);
            }
            int max = D.Cfg.MaxPerDrop(s.level);
            p.counter.text = session > 0 ? $"Đợt này: {session}/{max}" : $"{s.balls} bi · tốn {x}/lần";
            p.auto.SetText($"Thả liền {max}");
            p.drop.SetColor(CanDrop() ? Theme.Red : Color.Lerp(Theme.Red, Theme.Paper3, 0.6f));
            // vừa vượt mốc trong đợt: thanh dừng ở đầy cho tới hộp "Huyền thoại!" cuối đợt
            int need = D.Cfg.legendMilestone;
            bool done = s.legendDone && bigReward == null;
            p.legendBar.gameObject.SetActive(!done);
            p.legendText.gameObject.SetActive(done);
            if (!done) p.legendBar.Set(Mathf.Min(s.ballsSpent, need), need, 0, $"Huyền thoại chắc chắn: {Mathf.Min(s.ballsSpent, need)}/{need}");
            else p.legendText.text = LegendDoneText(D);
        }

        public static string LegendDoneText(GameData d) => $"Đã nhận {d.Hero(d.LegendMilestoneHero).name}. Từ giờ Huyền thoại rất hiếm.";

        void PickX(int bx, int lv)
        {
            if (session > 0 || ending)
            {
                App.Toasts.Show("Đợt đang chạy, chờ bi rơi hết rồi đổi cược", App.Art.Icon("ball"));
                return;
            }
            x = lastX = bx;
            RefreshUi();
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
            if (session > 0 && board.balls.Count == 0 && !holding && autoLeft == 0 && !ending) StartCoroutine(SessionEnd());
            if (dirty && (saveTimer += dt) > 0.5f) SaveNow();
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

        IEnumerator SessionEnd()
        {
            ending = true;
            session = 0;
            holding = false;
            SaveNow();
            RefreshUi();
            // chờ rương cuối bay vào khay, chữ nổi cuối kịp hiện
            yield return new WaitForSecondsRealtime(S.chests.Count > 0 ? 0.75f : 0.3f);
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
            slowT = 0;
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
