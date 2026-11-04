// Hộp chi tiết thẻ (Sổ thẻ, thẻ riêng trong hộp chi tiết tướng): thẻ lớn ở cấp lv, câu dẫn, cấp mở, ghi chú (thẻ chung không lên cấp,
// ra lại được trong lượt hay không; thẻ riêng ghi cấp và cách lên cấp).
// Prefab Assets/04 Prefabs/Dialogs/ChiTietThe.
using PokiClash.Core;
using TMPro;
using UnityEngine;
using PokiClash.UI;

namespace PokiClash
{
    public sealed class CardDetailDialog : Dialog
    {
        [SerializeField] UiCard card;
        [SerializeField] TextMeshProUGUI flavor, unlock, note;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiCard bigCard, TextMeshProUGUI flavorText, TextMeshProUGUI unlockText)
        {
            card = bigCard;
            flavor = flavorText;
            unlock = unlockText;
        }

        public void Show(CardDef c, int lv = 1)
        {
            card.Bind(c, lv, App.Art.Icon(c.icon));
            flavor.gameObject.SetActive(!string.IsNullOrEmpty(c.flavor));
            flavor.text = $"<i>{c.flavor}</i>";
            bool locked = c.unlock > App.Save.Data.level;
            unlock.gameObject.SetActive(locked);
            unlock.text = $"Vào bộ rút khi người chơi lên cấp {c.unlock}.";
            if (note)
                note.text = c.kind == CardKind.Pool
                    ? c.repeat ? "Thẻ chung không lên cấp, ra lại được trong lượt." : "Thẻ chung không lên cấp, mỗi lượt chọn một lần."
                    : $"Thẻ riêng của tướng, cấp {lv}/{App.Data.Cfg.cardMax}: đủ bản sao thì lên cấp ở hộp chi tiết tướng.";
        }
    }
}
