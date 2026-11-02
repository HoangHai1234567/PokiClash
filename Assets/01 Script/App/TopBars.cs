// Thanh trên dùng chung cho mọi scene (trong prefab App ở Boot, đổi theo SceneRoot.Bar):
// - Hud (sảnh): vòng cấp có cung EXP, chip bi, nút AFK (số bi chờ hoặc số phút, nhún khi có từ 5 bi, chấm đỏ khi có rương AFK mở được), nút Sổ tay;
// - Back (scene con): nút quay lại, tên scene, chip cấp, chip bi.
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

        TextMeshProUGUI afkText;
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
            afkBtn.SetOnClick(() => App.OpenAfk?.Invoke());
            notebookBtn.SetOnClick(() => App.Router.Go(SceneIds.Notebook));
            backBtn.SetOnClick(App.Back);
            Show(TopBar.None, "");
        }

        public void Show(TopBar kind, string title)
        {
            hud.gameObject.SetActive(kind == TopBar.Hud);
            back.gameObject.SetActive(kind == TopBar.Back);
            backTitle.text = title ?? "";
            Refresh();
        }

        public void SetTitle(string title) => backTitle.text = title;

        public static string Fmt(int n) => n >= 10000 ? (n / 1000f).ToString("0.#") + "k" : n.ToString();

        public void Refresh()
        {
            var s = App.Save?.Data;
            if (s == null) return;
            var cfg = GameData.Current.Cfg;
            float p = s.level >= cfg.maxLevel ? 1 : (float)s.exp / Mathf.Max(1, Progress.ExpToNext(s.level, cfg));
            expArc.fillAmount = Mathf.Clamp01(p);
            lvText.text = s.level.ToString();
            ballsText.text = Fmt(s.balls);
            backBalls.text = Fmt(s.balls);
            backLv.text = $"Cấp {s.level}";
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
