// Một ô thẻ thưởng trong hộp mở rương: thẻ mini thu nhỏ theo số thẻ, tên tướng, nhãn "×n" khi có bản sao; prefab Items/ThuongThe.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class RewardCardCell : MonoBehaviour
    {
        [SerializeField] UiCard card;
        [SerializeField] TextMeshProUGUI heroName;
        [SerializeField] GameObject badge;
        [SerializeField] TextMeshProUGUI badgeText;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiCard c, TextMeshProUGUI hero, GameObject copies, TextMeshProUGUI copiesText)
        {
            card = c;
            heroName = hero;
            badge = copies;
            badgeText = copiesText;
        }

        public void Bind(CardDef cd, int lv, Sprite icon, string hero, Color rarity, int n, float k, Vector2 cell)
        {
            name = "o_" + cd.id;
            card.Bind(cd, lv, icon);
            card.transform.localScale = Vector3.one * k;
            heroName.text = hero;
            heroName.color = rarity;
            heroName.rectTransform.sizeDelta = new Vector2(cell.x + 4, 36);
            badge.SetActive(n > 1);
            badgeText.text = "×" + n;
        }
    }
}
