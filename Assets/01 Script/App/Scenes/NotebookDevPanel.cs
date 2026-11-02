// Phần dev của tờ giấy Sổ tay (con "ban_dev" trong prefab Assets/04 Prefabs/Screens/Notebook): Bảng thử, Chỉnh số, Máy tự chơi.
// Chỉ giữ tham chiếu; việc làm nằm ở App/Dev/NotebookDev.cs (bọc #if, chỉ Editor và Development Build). Bản phát hành tắt phần này.
// Lớp này không bọc #if để prefab không mất script ở bản phát hành.
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class NotebookDevPanel : MonoBehaviour
    {
        // một ô chỉnh số: khoá trong BalanceConfig, chữ số, nút − / +
        [Serializable]
        public struct TuneCell
        {
            public string key;
            public TextMeshProUGUI value;
            public SketchButton minus, plus;
        }

        [Serializable]
        public struct Parts
        {
            public SketchButton[] tools; // Bảng thử, cùng thứ tự NotebookDev.Tools
            public TuneCell[] tune;
            public SketchButton tuneReset; // "Về số gốc"
            public TextMeshProUGUI botNote, botStage, botResult;
            public SketchButton botPrev, botNext, botRun;
        }

        [SerializeField] Parts p;

        public Parts Refs => p;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;
    }
}
