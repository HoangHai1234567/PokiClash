// Màn giới thiệu lần đầu (Dialogs.Intro): "Sổ Tay Phiêu Lưu", 4 ô, "Bắt đầu!" ghi đã xem. Nội dung cố định trong prefab
// Assets/04 Prefabs/Dialogs/GioiThieu.
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class IntroDialog : Dialog
    {
        [SerializeField] SketchButton start;

        // Dùng khi nướng prefab (Editor).
        public void Setup(SketchButton startButton) => start = startButton;

        void Awake() => start.SetOnClick(() =>
        {
            App.Save.Data.intro = true;
            App.Save.Save();
            Close();
        });
    }
}
