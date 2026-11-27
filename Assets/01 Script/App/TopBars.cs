// Thanh trên dùng chung cho mọi scene (trong prefab App ở Boot, đổi theo SceneRoot.Bar):
// - Hud (sảnh): vòng cấp có cung EXP, chip bi, nút AFK (số bi chờ hoặc số phút, nhún khi có từ 5 bi, chấm đỏ khi có rương AFK mở được), nút Sổ tay;
//   Thanh Hud dùng chung cho sảnh, Nhà và đảo Casino (người dùng 2026-11-27: "các UI này sống qua các màn home/đảo chính/đảo casino ...
//   ở 2 scene kia bỏ tên và nút back đi"), đi kèm giao diện sảnh chung LobbyDock (hàng nút đáy, cột công trình, cột ưu đãi); Sổ tay mở từ
//   màn nào thì quay lại màn đó.
// - Back (scene con): nút quay lại, tên scene, ô cấp tròn, chip bi.
// Chip bi chỉ hiện ở máy bi và đảo Casino (người dùng 2026-11-27: "Phần số bi chỉ cần hiện khi ở máy pinball hoặc đảo casino"); túi bi đầy
// (BallBag) thì số đỏ.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class TopBars : MonoBehaviour
    {
        [SerializeField] RectTransform hud, back;
        [SerializeField] Image expArc;
        [SerializeField] TextMeshProUGUI lvText, ballsText, backTitle, backLv, backBalls;
        [SerializeField] SketchButton afkBtn, notebookBtn, backBtn;
        [SerializeField] GameObject afkDot;
        // ô cấp tròn của thanh màn con (chép Hud/vong_cap, menu "PokiClash/Prefab/Máy bi: thanh túi bi, ô cấp tròn", 2026-11-27: người dùng
        // "ô level để nhất quán 1 kiểu ô tròn level ở màn đảo chính thôi"): thay chip "Cấp N"; máy bi có vòng cấp riêng nên ẩn
        [SerializeField] GameObject backBadge;
        [SerializeField] Image backArc;
        [SerializeField] TextMeshProUGUI backLvNum;
        // giao diện sảnh chung (App.prefab, nút sanh_chung; menu "PokiClash/Prefab/Sảnh và đảo/Sảnh chung: ..."): hiện cùng thanh Hud
        [SerializeField] LobbyDock lobby;

        // Dùng khi dựng prefab (Editor).
        public void SetLobby(LobbyDock dock) => lobby = dock;

        // Dùng khi nướng prefab (Editor): ô cấp tròn của thanh màn con
        public void SetBackBadge(GameObject badge, Image arc, TextMeshProUGUI num)
        {
            backBadge = badge;
            backArc = arc;
            backLvNum = num;
        }

        TextMeshProUGUI afkText;
        Color ballsInk, backBallsInk;
        bool afkPulse;
        float refreshTimer;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform hudRt, RectTransform backRt, Image arc, TextMeshProUGUI lv, TextMeshProUGUI balls, TextMeshProUGUI title,
            TextMeshProUGUI bLv, TextMeshProUGUI bBalls, SketchButton afk, SketchButton notebook, SketchButton backButton, GameObject dot)
        {
            hud = hudRt;
            back = backRt;
            expArc = arc;
            lvText = lv;
            ballsText = balls;
            backTitle = title;
            backLv = bLv;
            backBalls = bBalls;
            afkBtn = afk;
            notebookBtn = notebook;
            backBtn = backButton;
            afkDot = dot;
        }

        void Awake()
        {
            afkText = afkBtn.Label;
            ballsInk = ballsText.color;
            backBallsInk = backBalls.color;
            afkBtn.SetOnClick(() => App.OpenAfk?.Invoke());
            // Sổ tay nhận màn đang đứng (sảnh, Nhà, đảo Casino) để quay lại đó
            notebookBtn.SetOnClick(() => App.Router.Go(SceneIds.Notebook, App.Router.Current));
            backBtn.SetOnClick(App.Back);
            Guide.Mark("bar.back", backBtn);
            Guide.Mark("bar.afk", afkBtn);
            Show(TopBar.None, "");
        }

        public void Show(TopBar kind, string title)
        {
            hud.gameObject.SetActive(kind == TopBar.Hud);
            back.gameObject.SetActive(kind == TopBar.Back);
            backTitle.text = title ?? "";
            string scene = App.Router != null ? App.Router.Current : null;
            if (lobby) lobby.Show(kind == TopBar.Hud);
            bool balls = BallsHere(scene);
            Chip(ballsText).SetActive(balls);
            Chip(backBalls).SetActive(balls);
            if (backBadge)
            {
                Chip(backLv).SetActive(false);
                // bỏ ô cấp tròn ở mọi màn con (người dùng 2026-11-27, Sổ thẻ rồi Hội Quả: "bỏ icon level nhỏ kiểu này đi ... bỏ hết trong
                // các màn nào giống như này"); cấp xem ở vòng cấp của thanh sảnh
                backBadge.SetActive(false);
            }
            backBtn.Locked = false;
            ballsHeld = 0;
            Refresh();
        }

        // khoá nút quay lại (máy bi lúc đang thả: mờ, chạm im lặng); đổi màn thì Show tự mở lại
        public void LockBack(bool on) => backBtn.Locked = on;

        public void SetTitle(string title) => backTitle.text = title;

        // màn có hiện số bi: máy bi, đảo Casino và các trò trên đảo
        public static bool BallsHere(string scene) => scene == SceneIds.Machine || scene != null && scene.StartsWith(SceneIds.Casino);

        static GameObject Chip(TextMeshProUGUI t) => (t.transform.parent ? t.transform.parent : t.transform).gameObject;

        public static string Fmt(int n) => n >= 10000 ? (n / 1000f).ToString("0.#") + "k" : n.ToString();

        // chip bi đang hiện (thanh sảnh hoặc thanh màn con): đồ bay về đây (bi Cây bi ở Nhà); chip bi đang ẩn (chỉ hiện ở máy bi, đảo
        // Casino) mà kệ sảnh chung đang hiện thì là nút giữa của kệ (bi "chui vào ô" Casino / Máy Bi); null nếu thanh đang ẩn
        public RectTransform BallChip
        {
            get
            {
                var t = back && back.gameObject.activeInHierarchy ? backBalls : hud && hud.gameObject.activeInHierarchy ? ballsText : null;
                var chip = t ? (RectTransform)(t.transform.parent ? t.transform.parent : t.transform) : null;
                if (chip && chip.gameObject.activeInHierarchy) return chip;
                var dock = lobby && lobby.Visible ? lobby : null;
                var mid = dock && dock.Bottom != null && dock.Bottom.Length > 2 ? dock.Bottom[2].button : null;
                return mid && mid.gameObject.activeInHierarchy ? mid.Rect : chip;
            }
        }

        // vòng cấp đang hiện (thanh sảnh: vòng có cung EXP; thanh màn con: ô cấp tròn): kinh nghiệm bay về đây (RewardFly); null nếu không có
        public RectTransform LevelRing
        {
            get
            {
                if (hud && hud.gameObject.activeInHierarchy && expArc) return (RectTransform)(expArc.transform.parent ? expArc.transform.parent : expArc.transform);
                if (back && back.gameObject.activeInHierarchy && backBadge && backBadge.activeInHierarchy) return (RectTransform)backBadge.transform;
                return null;
            }
        }

        // bi vừa bay tới chip: chip nảy nhẹ (số đếm chạy do Refresh)
        public void PunchBalls(float k = 0.35f)
        {
            var chip = BallChip;
            if (chip) UiMotion.Of(chip).Punch(k);
        }

        // lớp cho đồ bay về chip (phủ cả màn, trên canvas của màn): vẽ trên mọi thứ của màn và trên chip lúc tới
        public RectTransform FlyLayer => transform as RectTransform;

        // bi đã cộng vào bản lưu nhưng còn đang bay: chip chưa đếm phần này (lưu xong Refresh vẫn hiện số cũ); mỗi viên tới thì nhả
        // phần của nó, chip đếm chạy lên. Đổi màn thì nhả hết.
        int ballsHeld;

        public void HoldBalls(int n) => ballsHeld = Mathf.Max(0, ballsHeld + n);

        public void ReleaseBalls(int n)
        {
            ballsHeld = Mathf.Max(0, ballsHeld - n);
            Refresh();
        }

        public void Refresh()
        {
            var s = App.Save?.Data;
            if (s == null) return;
            var cfg = GameData.Current.Cfg;
            float p = s.level >= cfg.maxLevel ? 1 : (float)s.exp / Mathf.Max(1, Progress.ExpToNext(s.level, cfg));
            expArc.fillAmount = Mathf.Clamp01(p);
            lvText.text = s.level.ToString();
            // số bi đổi thì đếm chạy rồi chip nảy (bộ UI Sa Bàn); trừ phần bi còn đang bay tới chip
            int balls = Mathf.Max(0, s.balls - ballsHeld);
            NumberTicker.Set(ballsText, balls, v => Fmt((int)v));
            NumberTicker.Set(backBalls, balls, v => Fmt((int)v));
            bool full = BallBag.Full(s, cfg, PokiClash.Game.SaveService.Now());
            ballsText.color = full ? Theme.RedD : ballsInk;
            backBalls.color = full ? Theme.RedD : backBallsInk;
            backLv.text = Loc.F("Cấp {0}", s.level);
            if (backArc) backArc.fillAmount = Mathf.Clamp01(p);
            if (backLvNum) backLvNum.text = s.level.ToString();
            // người mới: nút AFK ẩn tới khi AFK đã có mảnh hoặc rương (GD_Claude/25_FTUE.md bước F1)
            afkBtn.gameObject.SetActive(Tutorial.Shows(s, GameData.Current, Tutorial.HubPart.Afk, PokiClash.Game.SaveService.Now()));
            // nút đồng hồ: chưa qua ải nào thì ghi "AFK"; có bi trên cây thì ghi số bi, không thì số giờ AFK đã dồn
            if (Progress.TotalCleared(s) == 0)
            {
                afkText.text = "AFK";
                afkPulse = false;
                afkDot.SetActive(false);
            }
            else
            {
                double now = PokiClash.Game.SaveService.Now();
                var ap = Afk.Pending(s, cfg, now);
                int tree = Trees.Stock(s, cfg, now);
                afkText.text = tree > 0 ? $"+{tree}" : ap.hours >= 1 ? $"{(int)ap.hours}g" : $"{(int)(ap.hours * 60)}p";
                afkPulse = Trees.Full(s, cfg, now);
                afkDot.SetActive(Afk.ReadyChests(s, cfg, now) > 0);
            }
            refreshTimer = 0;
            if (lobby) lobby.Refresh();
        }

        void Update()
        {
            // số AFK đổi theo giờ: làm mới mỗi 20 giây khi đang ở sảnh
            if (hud.gameObject.activeSelf && (refreshTimer += Time.unscaledDeltaTime) > 20) Refresh();
            // nút AFK nhún nhịp nhàng khi có từ 5 bi chờ (web: pulse 1 giây)
            float s = afkPulse ? 1 + 0.08f * (0.5f - 0.5f * Mathf.Cos(Time.unscaledTime * Mathf.PI * 2)) : 1;
            afkBtn.Rect.localScale = new Vector3(s, s, 1);
        }
    }
}
