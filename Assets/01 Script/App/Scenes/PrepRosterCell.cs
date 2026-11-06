// Một ô kho tướng: khung (vàng khi trong đội), chân dung, tên, mũi tên khắc hệ (xanh khắc, đỏ bị khắc). Tên "kho_<id>" để vòng thử bấm.
// - Items/OKho (hộp chọn tướng khởi đầu): ô gọn, số thứ tự ra trận ghi trước tên.
// - Items/OChonDoi (hộp chọn đội, menu "PokiClash/Prefab/Hộp chọn đội: ô tướng, khung cuộn"): thêm dải màu hệ sau chân dung, hàng sao,
//   lực chiến, số thứ tự ra trận trong tròn xanh ở góc trên trái; mũi tên nằm trong góc trên phải.
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
        [Tooltip("Cao chân dung")]
        [SerializeField] float portraitH = 128;

        // phần thêm của ô chọn đội (Items/OChonDoi); ô gọn để trống
        [SerializeField] Image band;
        [SerializeField] UiStars stars;
        [SerializeField] TextMeshProUGUI power;
        [SerializeField] GameObject orderBadge;
        [SerializeField] TextMeshProUGUI orderText;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, HeroPortrait por, TextMeshProUGUI nameText, Image arrowImg, ClickCatcher catcher)
        {
            bg = bgImg;
            portrait = por;
            heroName = nameText;
            arrow = arrowImg;
            click = catcher;
        }

        // Ô chọn đội (Editor): cao chân dung, dải hệ, sao, lực chiến, tròn số thứ tự.
        public void SetupPick(float portraitHeight, Image bandImg, UiStars starRow, TextMeshProUGUI powerText, GameObject badge, TextMeshProUGUI badgeText)
        {
            portraitH = portraitHeight;
            band = bandImg;
            stars = starRow;
            power = powerText;
            orderBadge = badge;
            orderText = badgeText;
        }

        // showArrow: khắc hoặc bị khắc tướng chính của địch (arrowIcon: mũi tên lên / xuống); order: thứ tự ra trận (0 = chưa chọn)
        public void Bind(HeroDef h, bool inTeam, bool showArrow, Sprite arrowIcon, Action onClick, int order = 0)
        {
            name = "kho_" + h.id;
            bg.color = inTeam ? Theme.Hex("#ffe9a0") : orderBadge ? Theme.CardFill : Color.white;
            portrait.Bind(h, portraitH);
            heroName.text = order > 0 && !orderBadge ? $"{order}. {h.name}" : h.name;
            if (orderBadge)
            {
                orderBadge.SetActive(order > 0);
                if (orderText) orderText.text = order.ToString();
            }
            if (band)
            {
                var c = Theme.Of(h.elem);
                band.color = new Color(c.r, c.g, c.b, 0.35f);
            }
            arrow.gameObject.SetActive(showArrow);
            if (showArrow) arrow.sprite = arrowIcon;
            click.OnClick = onClick;
        }

        // sao và lực chiến (ô chọn đội)
        public void SetStats(int star, int maxStar, int heroPower)
        {
            if (stars) stars.Set(star, maxStar);
            if (power) power.text = TeamPower.Text(heroPower);
        }
    }
}
