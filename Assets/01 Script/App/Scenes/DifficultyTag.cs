// Nhãn độ khó của đảo (Dễ / Vừa sức / Khó / Quá mạnh! / Đã chinh phục): khung mỏng tô màu theo độ khó, chữ trắng viền.
// Nằm trong prefab mục Items/BangVung (sảnh), màn Đảo và hộp Chuẩn bị trận.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class DifficultyTag : MonoBehaviour
    {
        [SerializeField] Image bg;
        [SerializeField] TextMeshProUGUI text;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, TextMeshProUGUI label)
        {
            bg = bgImg;
            text = label;
        }

        public static Color ColorOf(Progress.Difficulty df) =>
            df == Progress.Difficulty.Easy ? Theme.Hex("#8fd16a") : df == Progress.Difficulty.Fit ? Theme.Hex("#4fbf6a")
            : df == Progress.Difficulty.Hard ? Theme.Hex("#f3a02d") : df == Progress.Difficulty.Wall ? Theme.Red : Theme.Yellow;

        public void Set(Progress.Difficulty df)
        {
            bg.color = ColorOf(df);
            text.text = Progress.DifficultyText(df);
        }
    }
}
