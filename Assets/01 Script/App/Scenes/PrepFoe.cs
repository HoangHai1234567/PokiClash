// Một đối thủ trong hộp Chuẩn bị trận (prefab Assets/04 Prefabs/Items/DoiThu): chân dung, tên, nhãn hệ, cấp, dòng "Boss: máu ×1,8".
// Khung phủ kín khung "doi_thu", dời ngang theo vị trí của đối thủ.
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
            portrait.Bind(h, en.boss ? 168 : 132, false, Teams.EnemyStar(en.level));
            portrait.Rect.anchoredPosition = new Vector2(0, en.boss ? 106 : 116);
            heroName.text = h.name;
            elem.Set(h.elem);
            level.text = $"Lv{en.level}";
            boss.SetActive(en.boss);
        }
    }
}
