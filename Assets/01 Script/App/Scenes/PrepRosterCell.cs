// Một ô kho tướng trong hộp Chuẩn bị trận (prefab Assets/04 Prefabs/Items/OKho): khung (vàng khi trong đội), chân dung, tên,
// mũi tên khắc hệ (xanh khắc, đỏ bị khắc). Tên "kho_<id>" để vòng thử bấm.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class PrepRosterCell : MonoBehaviour
    {
        [SerializeField] Image bg, arrow;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI heroName;
        [SerializeField] ClickCatcher click;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, HeroPortrait por, TextMeshProUGUI nameText, Image arrowImg, ClickCatcher catcher)
        {
            bg = bgImg;
            portrait = por;
            heroName = nameText;
            arrow = arrowImg;
            click = catcher;
        }

        // showArrow: khắc hoặc bị khắc tướng chính của địch (arrowIcon: mũi tên lên / xuống)
        public void Bind(HeroDef h, bool inTeam, bool showArrow, Sprite arrowIcon, Action onClick)
        {
            name = "kho_" + h.id;
            bg.color = inTeam ? Theme.Hex("#ffe9a0") : Color.white;
            portrait.Bind(h, 100);
            heroName.text = h.name;
            arrow.gameObject.SetActive(showArrow);
            if (showArrow) arrow.sprite = arrowIcon;
            click.OnClick = onClick;
        }
    }
}
