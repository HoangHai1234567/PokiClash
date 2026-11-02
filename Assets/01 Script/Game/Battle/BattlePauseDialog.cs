// Hộp tạm dừng trận (prefab Assets/04 Prefabs/Dialogs/TranTamDung): tên ải, mẹo xếp thẻ và khắc hệ, "Đánh tiếp", "Bỏ trận (tính thua)".
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class BattlePauseDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI where;
        [SerializeField] SketchButton resume, quit;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI whereText, SketchButton resumeBtn, SketchButton quitBtn)
        {
            where = whereText;
            resume = resumeBtn;
            quit = quitBtn;
        }

        // whereText: "Đảo · Ải n: tên"; onQuit gọi sau khi đóng hộp
        public void Show(string whereText, Action onQuit)
        {
            where.text = whereText;
            resume.SetOnClick(Close);
            quit.SetOnClick(() =>
            {
                Close();
                onQuit?.Invoke();
            });
        }
    }
}
