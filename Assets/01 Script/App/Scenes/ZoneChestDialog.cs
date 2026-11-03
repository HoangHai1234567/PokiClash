// Hộp rương mốc của đảo (prefab Assets/04 Prefabs/Dialogs/RuongDao): "Rương nửa đảo" (đảo 8 ải) / "Rương ải N" (đảo 70 ải) /
// "Rương chinh phục", rương, số bi,
// hàng thẻ mini kèm tên tướng (Items/TheRuongDao), dòng báo khi chưa có thẻ, nút Nhận. Thưởng đã cộng vào bản lưu trước khi mở.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ZoneChestDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI title, balls;
        [SerializeField] Image chest;
        [SerializeField] RectTransform cards;
        [SerializeField] GameObject empty;
        [SerializeField] SketchButton ok;
        [SerializeField] ZoneChestCard cardPrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, Image chestImg, TextMeshProUGUI ballsText, RectTransform cardRow, GameObject emptyText,
            SketchButton okButton, ZoneChestCard cardItem)
        {
            title = titleText;
            chest = chestImg;
            balls = ballsText;
            cards = cardRow;
            empty = emptyText;
            ok = okButton;
            cardPrefab = cardItem;
        }

        public void Show(Progress.ZoneChest r, SaveData s, GameData d)
        {
            var at = Islands.Chests(r.zone);
            title.text = r.big ? "Rương chinh phục!" : at.Length > 2 ? $"Rương ải {at[r.n]}" : "Rương nửa đảo";
            chest.color = r.big ? Color.white : Theme.Hex("#d6dee8");
            balls.text = $"+{r.balls} bi";
            for (int i = cards.childCount - 1; i >= 0; i--) Destroy(cards.GetChild(i).gameObject);
            foreach (var c in r.cards)
            {
                var cd = d.Card(c.card);
                var col = Ui.Spawn(cardPrefab, cards);
                col.Bind(cd, s.Hero(c.hero).Card(c.slot).lv, App.Art ? App.Art.Icon(cd.icon) : null, d.Hero(c.hero).name);
            }
            empty.SetActive(r.cards.Count == 0);
            ok.SetOnClick(Close);
        }
    }
}
