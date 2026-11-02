// Hộp "Lên cấp!" (Dialogs.LevelUp): con dấu tím, cấp mới, nút cược vừa mở, thẻ chung vừa vào bộ rút (hai dòng sau ẩn khi trống).
// Prefab Assets/04 Prefabs/Dialogs/LenCap.
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class LevelUpDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI level, newX, newCards;
        [SerializeField] SketchButton ok;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI levelText, TextMeshProUGUI newXText, TextMeshProUGUI newCardsText, SketchButton okButton)
        {
            level = levelText;
            newX = newXText;
            newCards = newCardsText;
            ok = okButton;
        }

        void Awake() => ok.SetOnClick(Close);

        public void Show(int to, string unlockX, string cards)
        {
            level.text = $"Cấp {to}";
            newX.gameObject.SetActive(!string.IsNullOrEmpty(unlockX));
            newX.text = unlockX;
            newCards.gameObject.SetActive(!string.IsNullOrEmpty(cards));
            newCards.text = cards;
        }
    }
}
