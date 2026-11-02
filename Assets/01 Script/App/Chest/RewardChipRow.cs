// Một dòng thưởng chip (EXP, bi, đá) trong hộp mở rương; prefab Items/ThuongChip.
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class RewardChipRow : MonoBehaviour
    {
        [SerializeField] UiChip chip;

        public RectTransform Chip => chip.Rect;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiChip c) => chip = c;

        public void Bind(Sprite icon, string text, float width)
        {
            chip.Set(icon, Color.white, text);
            chip.Rect.sizeDelta = new Vector2(width, 84);
        }
    }
}
