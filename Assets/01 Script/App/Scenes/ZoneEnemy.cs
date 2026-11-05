// Một địch trong khung ải tiếp theo của đảo (prefab Assets/04 Prefabs/Items/DichAi): chân dung và nhãn (cấp, BOSS, cường hóa ±%).
// Khung phủ kín khung dưới; chân dung và nhãn đứng trên dòng thưởng. ZoneScene xếp các địch từ trái sang, mỗi con rộng bằng nhãn
// của nó (tối thiểu 112), nhãn dài như "Lv190 BOSS +95%" không lòi ra mép khung hay đè con bên cạnh.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class ZoneEnemy : MonoBehaviour
    {
        const float MinWidth = 112, LabelPad = 12;

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
            portrait.Bind(h, en.boss ? 96 : 80, false, Teams.EnemyFormStar(en));
            level.text = ZoneChapterRow.EnemyLabel(en);
            level.color = en.boss || en.buff > 0 ? Theme.Red : Theme.Ink;
        }

        // bề ngang con này chiếm trong hàng địch
        public float Width => Mathf.Max(MinWidth, level.GetPreferredValues(level.text).x + LabelPad);

        // dời cả con để tâm chân dung và nhãn ở x (tính từ mép trái khung dưới)
        public void PlaceAt(float x) => ((RectTransform)transform).anchoredPosition = new Vector2(x - level.rectTransform.anchoredPosition.x, 0);
    }
}
