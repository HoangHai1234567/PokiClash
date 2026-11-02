// Hộp chi tiết thẻ chung (Sổ thẻ): thẻ lớn, câu dẫn, cấp mở, ghi chú. Prefab Assets/04 Prefabs/Dialogs/ChiTietThe.
using PokiClash.Core;
using TMPro;
using UnityEngine;
using PokiClash.UI;

namespace PokiClash
{
    public sealed class CardDetailDialog : Dialog
    {
        [SerializeField] UiCard card;
        [SerializeField] TextMeshProUGUI flavor, unlock;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiCard bigCard, TextMeshProUGUI flavorText, TextMeshProUGUI unlockText)
        {
            card = bigCard;
            flavor = flavorText;
            unlock = unlockText;
        }

        public void Show(CardDef c)
        {
            card.Bind(c, 1, App.Art.Icon(c.icon));
            flavor.gameObject.SetActive(!string.IsNullOrEmpty(c.flavor));
            flavor.text = $"<i>{c.flavor}</i>";
            bool locked = c.unlock > App.Save.Data.level;
            unlock.gameObject.SetActive(locked);
            unlock.text = $"Vào bộ rút khi người chơi lên cấp {c.unlock}.";
        }
    }
}
