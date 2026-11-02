// Hình rương (thân tô màu + khoá tròn), prefab kit Kit/Ruong. Bind đặt loại, bề rộng, màu thân.
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ChestIcon : MonoBehaviour
    {
        [SerializeField] Image body, lockImg;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bodyImg, Image lockImage)
        {
            body = bodyImg;
            lockImg = lockImage;
        }

        public ChestIcon Bind(SlotKind kind, float w, Color? fill = null)
        {
            name = "ruong_" + Pachinko.Key(kind);
            body.color = fill ?? MachineBoard.ChestColor(kind);
            Rect.sizeDelta = new Vector2(w, w * 88 / 96f);
            lockImg.color = kind == SlotKind.ChestGold ? Theme.Orange : Theme.Hex("#ffd24a");
            lockImg.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -w * 0.05f), new Vector2(w * 0.22f, w * 0.22f));
            return this;
        }
    }
}
