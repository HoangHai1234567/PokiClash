// Một đối thủ trong hộp Chuẩn bị trận (prefab Assets/04 Prefabs/Items/DoiThu): chân dung, tên, nhãn hệ, cấp, dòng "Boss: máu ×1,8".
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

        // Dùng khi nướng prefab (Editor).
        public void Setup(HeroPortrait por, TextMeshProUGUI nameText, UiElemTag elemTag, TextMeshProUGUI levelText, GameObject bossText)
        {
            portrait = por;
            heroName = nameText;
            elem = elemTag;
            level = levelText;
            boss = bossText;
        }

        // x: lệch ngang so với giữa khung
        public void Bind(HeroDef h, StageEnemy en, float x)
        {
            name = "doi_thu_" + h.id;
            ((RectTransform)transform).anchoredPosition = new Vector2(x, 0);
            portrait.Bind(h, en.boss ? 290 : 250, false, Teams.EnemyFormStar(en)); // khung chân dung có lề: thân tướng khoảng 60%
            portrait.Rect.anchoredPosition = new Vector2(0, en.boss ? 104 : 112);
            heroName.text = h.name;
            elem.Set(h.elem);
            level.text = $"Lv{en.level}";
            boss.SetActive(en.boss);
            // boss ải 8 dòng 1 dạng: không tiến hóa nhưng gánh máu cả dòng
            if (en.evo) BossText($"Boss: máu ×{Num(App.Data.Cfg.bossHp * App.Data.Cfg.bossEvoHp)}");
        }

        // boss tiến hóa (dòng n dạng): ô của dạng form, dạng sau to hơn
        public void BindForm(HeroDef h, StageEnemy en, int form, float x, BalanceConfig cfg)
        {
            int n = h.forms.Length;
            name = $"doi_thu_{h.id}_{form + 1}";
            ((RectTransform)transform).anchoredPosition = new Vector2(x, 0);
            float height = 236 + 56f * form / System.Math.Max(1, n - 1);
            portrait.Bind(h, height, false, Teams.FormStar(cfg, form));
            portrait.Rect.anchoredPosition = new Vector2(0, 116 - 10f * form / System.Math.Max(1, n - 1));
            heroName.text = h.forms[form].name;
            elem.Set(h.elem);
            level.text = $"Lv{en.level}";
            boss.SetActive(true);
            BossText(form == 0 ? $"Boss · dạng 1/{n}" : $"Tiến hóa · dạng {form + 1}/{n}");
        }

        void BossText(string t)
        {
            var tmp = boss.GetComponentInChildren<TextMeshProUGUI>(true);
            if (tmp) tmp.text = t;
        }

        static string Num(double v) => (System.Math.Round(v * 10) / 10).ToString("0.#", System.Globalization.CultureInfo.InvariantCulture).Replace('.', ',');
    }
}
