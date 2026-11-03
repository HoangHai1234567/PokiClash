// Hộp rương mốc của đảo (prefab Assets/04 Prefabs/Dialogs/RuongDao): "Rương nửa đảo" (đảo 8 ải) / "Rương ải N" (đảo 70 ải) /
// "Rương chinh phục", rương, hàng ô thưởng (Items/OThuong: bi rồi từng thẻ kèm tướng chủ; menu "PokiClash/Prefab/Popup gọn (ô thưởng,
// đội hình, lực chiến)" gán), dòng báo khi chưa có thẻ, nút Nhận. Dòng số bi cũ để ẩn. Thưởng đã cộng vào bản lưu trước khi mở.
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
        [SerializeField] RewardTile tilePrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, Image chestImg, TextMeshProUGUI ballsText, RectTransform cardRow, GameObject emptyText,
            SketchButton okButton, RewardTile tile)
        {
            title = titleText;
            chest = chestImg;
            balls = ballsText;
            cards = cardRow;
            empty = emptyText;
            ok = okButton;
            tilePrefab = tile;
        }

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public void Show(Progress.ZoneChest r, SaveData s, GameData d)
        {
            var at = Islands.Chests(r.zone);
            title.text = r.big ? "Rương chinh phục!" : at.Length > 2 ? $"Rương ải {at[r.n]}" : "Rương nửa đảo";
            chest.color = r.big ? Color.white : Theme.Hex("#d6dee8");
            balls.gameObject.SetActive(false);
            for (int i = cards.childCount - 1; i >= 0; i--) Destroy(cards.GetChild(i).gameObject);
            Ui.Spawn(tilePrefab, cards).Item(Icon("ball"), $"×{r.balls}", "Bi");
            foreach (var c in r.cards)
            {
                var cd = d.Card(c.card);
                Ui.Spawn(tilePrefab, cards).Card(cd, Icon(cd.icon), d.Hero(c.hero), 1, c.rarity);
            }
            var le = cards.GetComponent<LayoutElement>();
            if (le) le.preferredHeight = RewardTile.H;
            empty.SetActive(r.cards.Count == 0);
            ok.SetOnClick(Close);
        }
    }
}
