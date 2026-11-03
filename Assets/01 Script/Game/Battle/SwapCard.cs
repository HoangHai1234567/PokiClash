// Một tướng để chọn trong hộp "Chọn tướng ra sân" (prefab Assets/04 Prefabs/Items/TranTheDoi): chân dung, tên, máu,
// gợi ý khắc hệ với tướng địch đang đứng. Chạm để chọn.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class SwapCard : MonoBehaviour
    {
        [SerializeField] ClickCatcher click;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI nameText, hp, tip;

        // Dùng khi nướng prefab (Editor).
        public void Setup(ClickCatcher catcher, HeroPortrait por, TextMeshProUGUI nameLbl, TextMeshProUGUI hpLbl, TextMeshProUGUI tipLbl)
        {
            click = catcher;
            portrait = por;
            nameText = nameLbl;
            hp = hpLbl;
            tip = tipLbl;
        }

        public void Bind(Fighter f, int index, Fighter foe, Action onClick)
        {
            name = "tuong_" + index;
            click.OnClick = onClick;
            portrait.Bind(f.hero, 150, false, f.star);
            nameText.text = f.hero.name;
            hp.text = $"{f.hp}/{f.maxHp}";
            double em = Battle.ElemMult(f, foe), bad = Battle.ElemMult(foe, f);
            tip.gameObject.SetActive(em > 1 || bad > 1);
            tip.text = em > 1 ? "Khắc địch" : "Bị khắc";
            tip.color = em > 1 ? Theme.GreenD : Theme.Red;
        }
    }
}
