// Nút Chiêu / Tuyệt kỹ ở hàng dưới của trận (dựng sẵn hai nút trong prefab Screens/Battle): icon thẻ, tên, giá hoặc "Đã xếp",
// vạch nộ (Tuyệt kỹ), mờ khi chưa dùng được, viền vàng khi sẵn sàng.
using System;
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class InnateButton : MonoBehaviour
    {
        [SerializeField] Image icon, glow;
        [SerializeField] ClickCatcher click;
        [SerializeField] TextMeshProUGUI cardName, cost;
        [SerializeField] RectTransform meterFill; // chỉ Tuyệt kỹ
        [SerializeField] CanvasGroup group;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image iconImg, Image glowImg, ClickCatcher catcher, TextMeshProUGUI nameText, TextMeshProUGUI costText, RectTransform fill, CanvasGroup cg)
        {
            icon = iconImg;
            glow = glowImg;
            click = catcher;
            cardName = nameText;
            cost = costText;
            meterFill = fill;
            group = cg;
        }

        // why: lý do chưa dùng được ("" = dùng được); rage: nộ của tướng (vạch nộ, 100 là đầy)
        public void Bind(CardDef card, Sprite iconSprite, bool used, string why, bool ready, double rage, Action onClick)
        {
            Rect.localScale = Vector3.one;
            click.OnClick = onClick;
            icon.sprite = iconSprite;
            cardName.text = card.name;
            cost.text = used ? "Đã xếp" : CardText.CostText(card);
            if (meterFill) meterFill.anchorMax = new Vector2(Mathf.Min(1, (float)rage / 100f), 1);
            group.alpha = used ? 0.45f : why != "" ? 0.6f : 1;
            glow.gameObject.SetActive(ready);
        }
    }
}
