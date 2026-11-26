// Phần chung của ba lều may rủi đảo Casino (GD_Claude/29_DaoCasino.md mục 6.6–6.7, 8, 12; mốc C7): Blackjack (BlackjackScene),
// Vòng Xoay (RouletteScene), Máy Quả (SlotScene). Mỗi lều một scene, chỉ mở khi sự kiện của lều đang mở (Casino.BoothOpen).
// - Hàng bậc cược (4 nút, bậc chưa tới cấp thì khoá), dòng chơi có trách nhiệm "Hôm nay đã cược / đã thắng / còn N ván có thưởng",
//   dòng chế độ (ván đầu miễn phí, ván tập khi hết lượt), Hũ bàn (thanh đầy + rương bậc kế), khách mời của sự kiện, nút Cách chơi
//   (tự mở lần đầu vào lều).
// - Không popup bán bi / ưu đãi ở đây (OfferHost bỏ qua scene bàn); hết bi thì chỉ báo, mời đi chỗ khác.
// - Hiệu ứng thắng tỉ lệ với số thắng thật (thắng nhỏ kêu nhỏ).
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public abstract class CasinoTableScene : SceneRoot
    {
        [SerializeField] protected SketchButton[] tiers;
        [SerializeField] protected TextMeshProUGUI today, modeText, guestText, jarText;
        [SerializeField] protected UiBar jarBar;
        [SerializeField] protected SketchButton help;
        // bản gọn (cả ba lều): bậc cược, tờ tin, Hũ bàn, Cách chơi nằm trong MỘT bảng gập; nút gập ở góc trái dưới ghi mức cược đang chọn
        [SerializeField] protected SketchButton infoToggle;
        [SerializeField] protected RectTransform infoPanel;

        public override string BackTo => SceneIds.Casino;

        protected static SaveData S => App.Save.Data;
        protected static GameData D => App.Data;
        protected static double Now => SaveService.Now();
        protected static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        protected int tier;
        protected Rng rng;

        protected abstract string Game { get; }
        protected abstract CasinoTable Table { get; }
        protected abstract string HelpText { get; }
        // đang giữa ván (không đổi bậc, không rời lều giữa chừng mà mất cược)
        protected abstract bool Busy { get; }

        public static string ElemIcon(Elem e) => e == Elem.Hoa ? "e_hoa" : e == Elem.Thuy ? "e_thuy" : e == Elem.Moc ? "e_moc" : e == Elem.Kim ? "e_kim" : "e_tho";

        // Dùng khi dựng prefab (Editor).
        public void SetupTable(SketchButton[] tierBtns, TextMeshProUGUI todayText, TextMeshProUGUI mode, TextMeshProUGUI guest, UiBar jar,
            TextMeshProUGUI jarLabel, SketchButton helpBtn)
        {
            tiers = tierBtns; today = todayText; modeText = mode; guestText = guest; jarBar = jar; jarText = jarLabel; help = helpBtn;
        }

        // Dùng khi dựng prefab (Editor): nút gập + bảng chứa phần chung.
        public void SetupInfo(SketchButton toggle, RectTransform panel)
        {
            infoToggle = toggle; infoPanel = panel;
        }

        protected bool InfoOpen => infoPanel && infoPanel.gameObject.activeSelf;

        protected void SetInfo(bool open)
        {
            if (!infoPanel) return;
            infoPanel.gameObject.SetActive(open);
            if (infoToggle) infoToggle.SetRole(open ? BtnColor.Yellow : BtnColor.Paper);
        }

        public override void Enter(object args)
        {
            rng = new Rng(Rng.RandomSeed());
            var s = S;
            // bậc mặc định: bậc cao nhất đã mở mà còn đủ bi cho 5 ván, không thì bậc 1
            tier = Enumerable.Range(0, Table.bets.Length).LastOrDefault(i => Casino.BetOpen(s, Table, i) && s.balls >= 5 * Casino.Bet(s, D, Table, i));
            for (int i = 0; i < tiers.Length; i++)
            {
                int k = i;
                tiers[i].SetOnClick(() => PickTier(k));
            }
            help.SetText(Loc.T("Cách chơi"));
            help.SetOnClick(ShowHelp);
            if (infoToggle)
            {
                infoToggle.SetOnClick(() =>
                {
                    if (Busy) return;
                    SetInfo(!InfoOpen);
                });
                SetInfo(false);
            }
            EnterTable();
            RenderTable();
            if (!Casino.BoothOpen(s, D, Game, Now))
            {
                App.Toasts.Show(Loc.T("Lều này đã nhổ đi rồi, hẹn đoàn sau"), Icon("flag"));
                return;
            }
            if (!Casino.Of(s).seen.Contains("howto:" + Game))
            {
                Casino.MarkSeen(s, "howto:" + Game);
                App.Save.Save();
                ShowHelp();
            }
        }

        protected abstract void EnterTable();

        // lượt chụp: gieo lại bộ sinh số của bàn để ván kế ra đúng bài đã dò trước (Editor/CasinoDealerTour.cs)
        public void SeedForTest(uint seed) => rng = new Rng(seed);

        void PickTier(int k)
        {
            if (Busy) return;
            if (!Casino.BetOpen(S, Table, k))
            {
                App.Toasts.Show(Loc.F("Mở ở cấp {0}", Casino.BetLevel(Table, k)), Icon("lock"));
                return;
            }
            tier = k;
            App.Audio.Play("bet");
            RenderTable();
            OnTierChanged();
            SetInfo(false);   // chọn xong mức cược thì gập bảng
        }

        protected virtual void OnTierChanged() { }

        protected TableMode Mode => Casino.ModeOf(S, D, Game, Now);

        // bậc thật của ván kế (ván đầu miễn phí luôn ở bậc 1)
        protected int PlayTier => Mode == TableMode.Free ? 0 : tier;

        protected int BetNow => Casino.Bet(S, D, Table, PlayTier);

        protected void RenderTable()
        {
            var s = S;
            var d = D;
            double now = Now;
            var st = Casino.Roll(s, d, now);
            if (infoToggle) infoToggle.SetText(Loc.F("Cược {0} bi", NumFmt.Short(BetNow)));
            for (int i = 0; i < tiers.Length; i++)
            {
                bool has = i < Table.bets.Length;
                tiers[i].gameObject.SetActive(has);
                if (!has) continue;
                bool open = Casino.BetOpen(s, Table, i);
                tiers[i].SetText(open ? Loc.F("{0} bi", NumFmt.Short(Casino.Bet(s, d, Table, i))) : Loc.F("Cấp {0}", Casino.BetLevel(Table, i)));
                tiers[i].SetRole(i == PlayTier ? BtnColor.Yellow : BtnColor.Paper); // ván miễn phí luôn ở bậc 1
                tiers[i].Locked = !open;
            }
            int left = Casino.PlaysLeft(s, d, Game, now);
            today.text = Loc.F("Hôm nay đã cược {0} bi · đã thắng {1} bi · còn {2} ván có thưởng", st.betToday, st.wonToday, left);
            var mode = Mode;
            modeText.gameObject.SetActive(mode != TableMode.Paid);
            modeText.text = mode == TableMode.Free ? Loc.T("Ván đầu miễn phí: không mất bi, thắng thì nhận phần lời")
                : Loc.T("Hết ván có thưởng hôm nay: ván tập (không cược, không thưởng)");
            modeText.color = mode == TableMode.Free ? Theme.GreenD : Theme.BlueD;
            // Hũ bàn: đầy theo bi đã cược, rương theo bậc cao nhất đã dùng
            float frac = (float)Casino.JarFrac(s, d, Game, now);
            jarBar.Set(frac * 100, 100, 0, Loc.F("Hũ bàn {0}%", Mathf.FloorToInt(frac * 100)), true);
            var jar = st.Jar(Game);
            int jt = Mathf.Clamp(Mathf.Max(jar.tier, PlayTier), 0, Table.jar.Count - 1);
            jarText.text = Table.jar.Count > 0 ? Loc.F("Hũ đầy: {0}", CasinoUi.Items(Table.jar[jt].items)) : "";
            var span = Casino.Booth(d, Game, now);
            var g = d.Hero(Casino.GuestOf(d, Game, now) ?? "");
            guestText.text = (span != null ? Loc.F("{0} · còn {1}", span.ev.Name, ShopUi.Clock(Casino.Left(span, now))) : Loc.T("Lều đã đóng")) +
                             (g != null ? "\n" + Loc.F("Khách mời: {0} (mảnh ở Hũ bàn bậc cao)", g.name) : "");
        }

        void ShowHelp()
        {
            var c = Table;
            string bets = string.Join(" / ", Enumerable.Range(0, c.bets.Length).Select(i => Casino.Bet(S, D, c, i).ToString()));
            App.Modals.Alert(Title, HelpText + "\n\n" +
                                    Loc.F("Bậc cược: {0} bi (bậc cao mở theo cấp). Mỗi ngày {1} ván có thưởng; hết thì chơi ván tập.", bets, c.daily) + "\n" +
                                    Loc.T("Hũ bàn: mọi bi đã cược (thắng hay thua) đổ vào hũ; hũ đầy cho rương theo bậc cao nhất đã cược, bậc cao có mảnh tướng khách mời."),
                Loc.T("Đã hiểu"));
        }

        // trả kết quả ván có cược: hiệu ứng theo số thắng thật, hũ đầy thì mở rương
        protected void AfterRound(int net, JarResult jar, System.Collections.Generic.List<Reward> extra)
        {
            if (net > 0)
            {
                bool big = net >= BetNow * 5;
                App.Audio.Play(big ? "prize" : "coin", big ? 1f : 0.6f);
                Haptics.Play(big ? Haptic.Win : Haptic.UiTap);
            }
            if (extra != null && extra.Count > 0) App.Toasts.Show(CasinoUi.Rewards(extra), Icon("star"));
            App.Save.Save();
            RenderTable();
            if (jar != null && jar.full && jar.rewards.Count > 0)
                StartCoroutine(ChestBox.Show(Loc.T("Hũ bàn đầy!"), jar.tier >= 2 ? SlotKind.ChestGold : SlotKind.ChestSilver, null, jar.rewards, Loc.T("Nhận")));
        }

        // thiếu bi: chỉ báo, không gạ mua (mục 8)
        protected void NoBalls(string why)
        {
            App.Audio.Play("error");
            App.Toasts.Show(why == Loc.T("Không đủ bi") ? Loc.T("Không đủ bi. Thử bậc thấp hơn, hoặc ghé Bến câu, Trường đua kiếm thêm") : why, Icon("ball"));
        }
    }
}
