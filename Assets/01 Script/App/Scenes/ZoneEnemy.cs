// Một địch trong khung ải tiếp theo của đảo (prefab Assets/04 Prefabs/Items/DichAi): chân dung và nhãn (cấp, BOSS, cường hóa ±%).
// Khung phủ kín khung dưới; địch thứ i dời ngang i × 112.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class ZoneEnemy : MonoBehaviour
    {
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI level;

        // Dùng khi nướng prefab (Editor).
        public void Setup(HeroPortrait por, TextMeshProUGUI lv)
        {
            portrait = por;
            level = lv;
        }

        public void Bind(HeroDef h, StageEnemy en, int i)
        {
            name = "dich_" + i;
            ((RectTransform)transform).anchoredPosition = new Vector2(i * 112, 0);
            portrait.Bind(h, en.boss ? 96 : 80, false, Teams.EnemyFormStar(en));
            level.text = ZoneChapterRow.EnemyLabel(en);
            level.color = en.boss || en.buff > 0 ? Theme.Red : Theme.Ink;
        }
    }
}
