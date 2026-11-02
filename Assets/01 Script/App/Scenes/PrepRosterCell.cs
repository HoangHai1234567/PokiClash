// Một ô kho tướng trong hộp chọn đội (prefab Assets/04 Prefabs/Items/OKho): khung (vàng khi trong đội), chân dung, tên (kèm số thứ tự ra trận),
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

        // showArrow: khắc hoặc bị khắc tướng chính của địch (arrowIcon: mũi tên lên / xuống); order: thứ tự ra trận (0 = chưa chọn)
        public void Bind(HeroDef h, bool inTeam, bool showArrow, Sprite arrowIcon, Action onClick, int order = 0)
        {
            name = "kho_" + h.id;
            bg.color = inTeam ? Theme.Hex("#ffe9a0") : Color.white;
            portrait.Bind(h, 128);
            heroName.text = order > 0 ? $"{order}. {h.name}" : h.name;
            arrow.gameObject.SetActive(showArrow);
            if (showArrow) arrow.sprite = arrowIcon;
            click.OnClick = onClick;
        }
    }
}
