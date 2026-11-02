// Hộp báo nhanh (ModalService.Alert): tiêu đề (ẩn nếu trống), câu chữ, một nút. Prefab Assets/04 Prefabs/Dialogs/Bao.
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class AlertDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI title, text;
        [SerializeField] SketchButton ok;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI bodyText, SketchButton okButton)
        {
            title = titleText;
            text = bodyText;
            ok = okButton;
        }

        public void Show(string titleText, string body, string okLabel, Action onOk)
        {
            title.gameObject.SetActive(!string.IsNullOrEmpty(titleText));
            title.text = titleText ?? "";
            text.text = body;
            ok.SetText(okLabel);
            ok.SetOnClick(() =>
            {
                Close();
                onOk?.Invoke();
            });
        }
    }
}
