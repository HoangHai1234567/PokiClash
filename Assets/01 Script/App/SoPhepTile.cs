// Một ô của Sổ Phép (prefab mục Items/OSoPhep, 20 bản sao đặt sẵn trong Dialogs/SoPhep; menu "PokiClash/Prefab/Hộp thoại và màn/Sổ Phép").
// Khung giấy, icon, tên, cấp (ô cấp), giá. Trạng thái không dùng sáng tối (bộ UI Sa Bàn): chưa vẽ là giấy trắng viền mực, vẽ được thì
// nhãn giá đậm, đã vẽ thì tô màu sáp của chương kèm dấu tích; ô đang chọn có viền mực dày. Chương khoá thì cả khối mờ (SoPhepDialog).
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class SoPhepTile : MonoBehaviour
    {
        [SerializeField] Image bg, icon, tick, frame;
        [SerializeField] TextMeshProUGUI title, level, price;
        [SerializeField] ClickCatcher click;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, Image iconImg, Image tickImg, Image frameImg, TextMeshProUGUI titleText, TextMeshProUGUI levelText,
            TextMeshProUGUI priceText, ClickCatcher catcher)
        {
            bg = bgImg;
            icon = iconImg;
            tick = tickImg;
            frame = frameImg;
            title = titleText;
            level = levelText;
            price = priceText;
            click = catcher;
        }

        // màu sáp của 4 chương (tô khi đã vẽ)
        static readonly Color[] Crayon = { Theme.Hex("#ffe6a3"), Theme.Hex("#cfe8c2"), Theme.Hex("#d6e4f7"), Theme.Hex("#ecd9f5") };

        public void Bind(SoPhepNode n, Sprite iconSprite, int lv, int face, bool canBuy, int cost, bool selected, Action onClick)
        {
            bool owned = lv > 0, maxed = lv >= n.MaxLv;
            bg.color = owned ? Crayon[Mathf.Clamp(n.ch, 0, Crayon.Length - 1)] : Theme.CardFill;
            Theme.SetSprite(icon, iconSprite);
            icon.color = owned || canBuy ? Color.white : new Color(0.55f, 0.52f, 0.48f, 0.85f);
            title.text = n.FaceCount > 1 && !n.IsElem ? n.FaceName(face) : n.Name; // ô chọn: mặt đang chọn; ô 5 hệ: tên ô (hệ ở bảng đáy)
            title.color = owned || canBuy ? Theme.Ink : Theme.Ink2;
            level.gameObject.SetActive(n.MaxLv > 1);
            level.text = $"{lv}/{n.MaxLv}";
            price.gameObject.SetActive(!maxed);
            price.text = n.stones > 0 && lv == 0 ? Loc.F("{0} nét · {1} đá", cost, n.stones) : Loc.F("{0} nét", cost);
            price.color = canBuy ? Theme.Ink : Theme.Ink3;
            price.fontStyle = canBuy ? FontStyles.Bold : FontStyles.Normal;
            tick.gameObject.SetActive(maxed);
            frame.gameObject.SetActive(selected);
            click.OnClick = onClick;
        }
    }
}
