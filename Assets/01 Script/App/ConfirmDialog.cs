// Hộp xác nhận hai nút (ModalService.Confirm): tiêu đề, câu chữ, nút thôi (giấy) và nút đồng ý (màu theo việc).
// Prefab Assets/04 Prefabs/Dialogs/XacNhan.
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class ConfirmDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI title, text;
        [SerializeField] SketchButton no, yes;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI bodyText, SketchButton noButton, SketchButton yesButton)
        {
            title = titleText;
            text = bodyText;
            no = noButton;
            yes = yesButton;
        }

        public void Show(string titleText, string body, string yesLabel, Action onYes, string noLabel, BtnColor yesColor)
        {
            title.text = titleText;
            text.text = body;
            no.SetText(noLabel);
            no.SetOnClick(Close);
            yes.SetText(yesLabel);
            yes.SetRole(yesColor);
            yes.SetOnClick(() =>
            {
                Close();
                onYes?.Invoke();
            });
        }
    }
}
