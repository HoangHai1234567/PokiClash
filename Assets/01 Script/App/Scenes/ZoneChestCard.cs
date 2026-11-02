// Một thẻ thưởng trong hộp rương mốc của đảo (prefab Assets/04 Prefabs/Items/TheRuongDao): thẻ mini và tên tướng nhận bản sao.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class ZoneChestCard : MonoBehaviour
    {
        [SerializeField] UiCard card;
        [SerializeField] TextMeshProUGUI heroName;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiCard c, TextMeshProUGUI hero)
        {
            card = c;
            heroName = hero;
        }

        public void Bind(CardDef cd, int lv, Sprite icon, string hero)
        {
            card.Bind(cd, lv, icon);
            heroName.text = hero;
        }
    }
}
