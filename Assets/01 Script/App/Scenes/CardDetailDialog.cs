// Hộp chi tiết thẻ (Sổ thẻ, thẻ riêng trong hộp chi tiết tướng): thẻ lớn ở cấp lv, câu dẫn, cấp mở, ghi chú (thẻ chung không lên cấp,
// ra lại được trong lượt hay không; thẻ riêng ghi cấp và cách lên cấp), kèm luật chi tiết của cơ chế mới (CardText.Note, 2026-11-17).
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
            unlock.text = Loc.F("Vào bộ rút khi người chơi lên cấp {0}.", c.unlock);
            if (note)
            {
                note.text = c.kind == CardKind.Pool
                    ? c.repeat ? Loc.T("Thẻ chung không lên cấp, ra lại được trong lượt.") : Loc.T("Thẻ chung không lên cấp, mỗi lượt chọn một lần.")
                    : Loc.F("Thẻ riêng của tướng, cấp {0}/{1}: đủ bản sao thì lên cấp ở hộp chi tiết tướng.", lv, App.Data.Cfg.cardMax);
                // luật của cơ chế mới (độc, phản đòn, combo, kết liễu, cường hóa, cộng hưởng; 2026-11-17)
                string rule = CardText.Note(c);
                if (rule.Length > 0) note.text += $"\n<size=85%>{rule}</size>";
            }
        }
    }
}
