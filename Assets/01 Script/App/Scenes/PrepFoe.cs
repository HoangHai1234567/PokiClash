// Một đối thủ trong hộp Chuẩn bị trận (prefab Assets/04 Prefabs/Items/DoiThu): chân dung, tên kèm cấp, nhãn hệ và lực chiến (icon kiếm
// + số, menu "PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)" thêm vào prefab), dòng dưới ("Boss: máu ×1,8",
// "Cường hóa +12%", "Yếu hơn 20%", "Lính, không thu phục"). Chữ cấp riêng cũ để ẩn.
// Khung phủ kín khung "doi_thu" (cao 420 cho chân dung to), dời ngang theo vị trí của đối thủ. Boss tiến hóa: mỗi dạng một ô (BindForm).
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class PrepFoe : MonoBehaviour
    {
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI heroName, level;
        [SerializeField] UiElemTag elem;
        [SerializeField] GameObject boss;
        [SerializeField] TextMeshProUGUI power;

        // Dùng khi nướng prefab (Editor).
        public void Setup(HeroPortrait por, TextMeshProUGUI nameText, UiElemTag elemTag, TextMeshProUGUI levelText, GameObject bossText)
        {
            portrait = por;
            heroName = nameText;
            elem = elemTag;
            level = levelText;
            boss = bossText;
        }

        // x: lệch ngang so với giữa khung; mods: phần cộng của địch (Islands.EnemyMods) để ghi đúng máu boss
        // power: lực chiến (HeroStats.Power), 0 thì ẩn
        public void Bind(HeroDef h, StageEnemy en, float x, StatMods mods = null, int powerValue = 0)
        {
            Power(powerValue);
            name = "doi_thu_" + h.id;
            ((RectTransform)transform).anchoredPosition = new Vector2(x, 0);
            portrait.Bind(h, en.boss ? 310 : 280, false, Teams.EnemyFormStar(en)); // khung chân dung có lề trên
            portrait.Rect.anchoredPosition = new Vector2(0, en.boss ? 104 : 112);
            heroName.text = NameLv(h.name, en.level);
            elem.Set(h.elem);
            level.gameObject.SetActive(false);
            // dòng dưới: boss (máu ×), cường hóa của ải (đảo 70 ải), lính
            var cfg = App.Data.Cfg;
            double hp = 1 + (mods?.hpPct ?? 0);
            string line = en.boss ? $"Boss: máu ×{Num(cfg.bossHp * (en.evo ? cfg.bossEvoHp : 1) * hp)}" // boss tiến hóa dòng 1 dạng gánh máu cả dòng
                : en.buff > 0 ? $"Cường hóa +{System.Math.Round(en.buff * 100)}%"
                : en.buff < 0 ? $"Yếu hơn {System.Math.Round(-en.buff * 100)}%"
                : h.minion ? "Lính, không thu phục" : null;
            boss.SetActive(line != null);
            if (line == null) return;
            if (h.minion && !en.boss && en.buff != 0) line += " · lính";
            BossText(line, en.boss || en.buff > 0 ? Theme.Red : en.buff < 0 ? Theme.Hex("#3a8a3a") : Theme.Ink2);
        }

        // boss tiến hóa (dòng n dạng): ô của dạng form, dạng sau to hơn
        public void BindForm(HeroDef h, StageEnemy en, int form, float x, BalanceConfig cfg, int powerValue = 0)
        {
            Power(powerValue);
            int n = h.forms.Length;
            name = $"doi_thu_{h.id}_{form + 1}";
            ((RectTransform)transform).anchoredPosition = new Vector2(x, 0);
            float height = 236 + 56f * form / System.Math.Max(1, n - 1);
            portrait.Bind(h, height, false, Teams.FormStar(cfg, form));
            portrait.Rect.anchoredPosition = new Vector2(0, 116 - 10f * form / System.Math.Max(1, n - 1));
            heroName.text = NameLv(h.forms[form].name, en.level);
            elem.Set(h.elem);
            level.gameObject.SetActive(false);
            boss.SetActive(true);
            BossText(form == 0 ? $"Boss · dạng 1/{n}" : $"Tiến hóa · dạng {form + 1}/{n}", Theme.Red);
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

        static string Num(double v) => (System.Math.Round(v * 10) / 10).ToString("0.#", System.Globalization.CultureInfo.InvariantCulture).Replace('.', ',');
    }
}
