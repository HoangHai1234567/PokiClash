// Hang Tiềm Năng: hệ boss hôm nay (theo thứ trong tuần; Thứ Bảy, Chủ nhật người chơi chọn), lượt thắng còn trong ngày và "+1 lượt"
// (quảng cáo), 4 tầng (cấp đề nghị, đá thưởng, boss và tướng phụ, nút Vào). Thua không mất lượt; không quét, không AFK.
// Prefab màn hình Assets/04 Prefabs/Screens/Cave (nền, khung cuộn, khung "hom_nay" có sẵn hàng chọn hệ và nút +1 lượt);
// mỗi tầng là một bản sao prefab Items/TangHang (CaveTierRow), sinh một lần rồi gán lại khi làm mới.
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
    public sealed class CaveScene : SceneRoot
    {
        public override string Title => "Hang Tiềm Năng";

        static readonly string[] DayNames = { "Chủ nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy" };

        [SerializeField] RectTransform list;
        [SerializeField] LayoutElement head;
        [SerializeField] TextMeshProUGUI headTitle, stones, left, info;
        [SerializeField] GameObject pickRow;
        [SerializeField] SketchButton[] picks; // nút chọn hệ (cuối tuần), theo thứ tự đảo
        [SerializeField] SketchButton ad;
        [SerializeField] CaveTierRow tierPrefab;

        readonly List<CaveTierRow> tiers = new List<CaveTierRow>();

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static int Today => Afk.Today(SaveService.Now());
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform listRt, LayoutElement headLayout, TextMeshProUGUI titleText, TextMeshProUGUI stonesText, TextMeshProUGUI leftText,
            TextMeshProUGUI infoText, GameObject pickRowGo, SketchButton[] pickButtons, SketchButton adButton, CaveTierRow tier)
        {
            list = listRt;
            head = headLayout;
            headTitle = titleText;
            stones = stonesText;
            left = leftText;
            info = infoText;
            pickRow = pickRowGo;
            picks = pickButtons;
            ad = adButton;
            tierPrefab = tier;
        }

        public override void Enter(object args) => Render();

        public override void Refresh() => Render();

        void Render()
        {
            if (!list) return;
            var cfg = D.Cfg;
            int day = Today;

            // đầu: hệ boss hôm nay, lượt, đá
            var elem = Potential.CaveElem(S, cfg, day);
            int wd = Potential.WeekdayOf(day);
            bool choose = cfg.cave.Weekday(wd) == null;
            head.preferredHeight = choose ? 380 : 300;
            float y = choose ? -180 : -100; // dòng lượt dưới hàng chọn hệ (nếu có)
            headTitle.text = $"{DayNames[wd]}: " + (elem is Elem e ? $"boss hệ {Elements.Name(e)}" : "chọn hệ boss");
            headTitle.color = elem is Elem e2 ? Theme.Of(e2) : Theme.Ink;
            stones.text = S.potentialStones.ToString();
            pickRow.SetActive(choose);
            if (choose)
            {
                // cuối tuần: chọn hệ boss cho hôm nay
                int k = 0;
                foreach (var z in D.Zones.OrderBy(x => x.order))
                {
                    if (k >= picks.Length) break;
                    var zid = z.id;
                    var b = picks[k++];
                    b.gameObject.SetActive(true);
                    b.name = "chon_" + Keys.Of(zid);
                    b.SetText(Elements.Name(zid));
                    b.SetRole(elem == zid ? BtnColor.Yellow : BtnColor.Paper);
                    b.SetOnClick(() =>
                    {
                        Potential.CavePick(S, cfg, day, zid);
                        App.Save.Save();
                        Render();
                    });
                }
                for (; k < picks.Length; k++) picks[k].gameObject.SetActive(false);
            }
            int leftWins = Potential.CaveLeft(S, cfg, day);
            int total = cfg.cave.winsPerDay + AdGate.Used(S, day, AdGate.CaveExtra) * cfg.cave.adExtra;
            left.text = leftWins > 0 ? $"Lượt thắng còn hôm nay: {leftWins}/{total} · thua không mất lượt" : "Hết lượt hôm nay";
            left.color = leftWins > 0 ? Theme.Ink : Theme.RedD;
            left.rectTransform.anchoredPosition = new Vector2(left.rectTransform.anchoredPosition.x, y);
            info.rectTransform.anchoredPosition = new Vector2(info.rectTransform.anchoredPosition.x, y - 60);
            bool showAd = leftWins <= 0 && Ads.Ready && Ads.Left(Ads.CaveExtra) > 0;
            ad.gameObject.SetActive(showAd);
            if (showAd)
                ad.SetOnClick(() =>
                    Ads.Show(Ads.CaveExtra, ok =>
                    {
                        if (ok)
                        {
                            App.Save.Save();
                            App.Toasts.Show("+1 lượt Hang hôm nay", Icon("rock"));
                        }
                        Render();
                    }));

            // các tầng: bản sao prefab mục, sinh một lần
            int n = cfg.cave.tiers.Count;
            while (tiers.Count < n) tiers.Add(Ui.Spawn(tierPrefab, list));
            for (int tier = 0; tier < tiers.Count; tier++)
            {
                bool shown = tier < n;
                tiers[tier].gameObject.SetActive(shown);
                if (!shown) continue;
                int t = tier;
                tiers[tier].Bind(D, S, tier, elem, elem != null && leftWins > 0, () =>
                {
                    if (elem is Elem ze) StagePrep.OpenCave(ze, t, day);
                });
            }
        }
    }
}
