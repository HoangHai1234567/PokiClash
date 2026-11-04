// Một đối thủ trong hộp Chuẩn bị trận (prefab Assets/04 Prefabs/Items/DoiThu): chân dung, tên dạng kèm cấp, nhãn hệ và lực chiến (icon
// kiếm + số, menu "PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)" thêm vào prefab), dòng ghi chú ("Boss", "Cường hóa
// +12%", "Yếu hơn 20%", "Lính, không thu phục"), và 3 hàng chỉ số to khi vào trận: Máu, Công, Thủ (menu "PokiClash/Prefab/Hộp chuẩn bị:
// chỉ số địch"). Người dùng dặn 2026-11-04: chỉ số địch to, rõ; không so với tướng người chơi (dễ hiểu lầm). Chữ cấp riêng cũ để ẩn.
// Khung phủ kín khung "doi_thu", dời ngang theo vị trí của đối thủ; hàng chỉ số ở đáy, chân dung đặt trên hàng chỉ số.
// Tướng tiến hóa trong trận (ải tướng, boss) chỉ hiện dạng đầu với chỉ số của dạng đó; đầu mục của hộp ghi luật tiến hóa.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class PrepFoe : MonoBehaviour
    {
        // chiều cao phần hàng chỉ số ở đáy ô (chân dung, tên, nhãn hệ, lực chiến nằm trên)
        public const float StatsH = 150;

        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI heroName, level;
        [SerializeField] UiElemTag elem;
        [SerializeField] GameObject boss;
        [SerializeField] TextMeshProUGUI power;
        [Tooltip("Số Máu, Công, Thủ (menu PokiClash/Prefab/Hộp chuẩn bị: chỉ số địch)")]
        [SerializeField] TextMeshProUGUI[] stats;

        // Dùng khi nướng prefab (Editor).
        public void Setup(HeroPortrait por, TextMeshProUGUI nameText, UiElemTag elemTag, TextMeshProUGUI levelText, GameObject bossText)
        {
            portrait = por;
            heroName = nameText;
            elem = elemTag;
            level = levelText;
            boss = bossText;
        }

        // x: lệch ngang so với giữa khung; s: chỉ số khi vào trận (HeroStats.InBattle, tướng tiến hóa là dạng đầu); power: lực chiến
        // (HeroStats.Power, tướng tiến hóa tính cả dòng), 0 thì ẩn
        public void Bind(HeroDef h, StageEnemy en, float x, Stats s, int powerValue = 0)
        {
            Power(powerValue);
            if (stats != null)
                for (int i = 0; i < stats.Length && i < 3; i++)
                    if (stats[i]) stats[i].text = TeamPower.Text((int)Math.Round(i == 0 ? s.hp : i == 1 ? s.atk : s.def));
            name = "doi_thu_" + h.id;
            ((RectTransform)transform).anchoredPosition = new Vector2(x, 0);
            int star = Teams.EnemyFormStar(en);
            portrait.Bind(h, en.boss ? 270 : 250, false, star); // khung chân dung có lề trên
            portrait.Rect.anchoredPosition = new Vector2(0, (en.boss ? 104 : 112) + StatsH);
            heroName.text = NameLv(h.Form(App.Data.Cfg.formStars, star).name, en.level);
            elem.Set(h.elem);
            level.gameObject.SetActive(false);
            // dòng ghi chú: boss, cường hóa của ải (đảo 70 ải), lính
            string buff = en.buff > 0 ? $"Cường hóa +{Math.Round(en.buff * 100)}%" : en.buff < 0 ? $"Yếu hơn {Math.Round(-en.buff * 100)}%" : null;
            string line = en.boss ? (buff != null ? $"Boss · {buff}" : "Boss") : buff ?? (h.minion ? "Lính, không thu phục" : null);
            boss.SetActive(line != null);
            if (line == null) return;
            if (h.minion && !en.boss && en.buff != 0) line += " · lính";
            BossText(line, en.boss || en.buff > 0 ? Theme.Red : en.buff < 0 ? Theme.Hex("#3a8a3a") : Theme.Ink2);
        }

        static string NameLv(string n, int lv) => $"{n} <size=82%><color=#8a7560>Lv{lv}</color></size>";

        void Power(int v)
        {
            if (!power) return;
            power.transform.parent.gameObject.SetActive(v > 0);
            power.text = TeamPower.Text(v);
        }

        void BossText(string t, Color color)
        {
            var tmp = boss.GetComponentInChildren<TextMeshProUGUI>(true);
            if (!tmp) return;
            tmp.text = t;
            tmp.color = color;
        }
    }
}
