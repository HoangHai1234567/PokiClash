// Hộp thoại dạng tờ giấy dán băng keo: nền tối mờ, trượt vào hơi nghiêng, nút đóng góc phải.
// Bắt buộc (kết quả trận, chọn tướng thay) thì không có nút đóng và chạm ra ngoài không đóng. Mở chồng được, đóng theo thứ tự.
// Mỗi hộp là một bản sao của prefab tờ giấy gốc (Assets/04 Prefabs/Dialogs/HopThoai).
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class Modal
    {
        public RectTransform Root; // phủ kín (nền tối)
        public RectTransform Sheet; // tờ giấy
        public RectTransform Body; // nơi đặt nội dung (dọc, tự giãn)
        public bool Mandatory;
        public Action OnClose;
        internal ModalService Owner;
        internal ModalSheet View;
        public bool IsOpen => Root != null;

        public void Close() => Owner?.Close(this);
    }

    public sealed class ModalService : MonoBehaviour
    {
        readonly List<Modal> stack = new List<Modal>();

        RectTransform Layer => (RectTransform)transform;
        public int Count => stack.Count;

        // Hộp riêng: bản sao của biến thể tờ giấy (bề rộng, bắt buộc chỉnh trên prefab). Gán dữ liệu bằng hàm Show của hộp.
        // mandatory: ghi đè cờ bắt buộc của prefab cho lần mở này.
        public T Open<T>(T prefab, Action onClose = null, bool? mandatory = null) where T : Dialog
        {
            var d = Ui.Spawn(prefab, Layer);
            var view = d.GetComponent<ModalSheet>();
            if (mandatory.HasValue) view.SetMandatory(mandatory.Value);
            d.Modal = Show(view, onClose);
            return d;
        }

        // Hộp dùng ở nhiều nơi: prefab tra theo kiểu trong Theme.Prefabs.dialogs.
        public T Open<T>(Action onClose = null, bool? mandatory = null) where T : Dialog => Open(Theme.Prefabs.GetDialog<T>(), onClose, mandatory);

        Modal Show(ModalSheet view, Action onClose)
        {
            var m = new Modal { Mandatory = view.Mandatory, OnClose = onClose, Owner = this, View = view };
            view.name = "Hop thoai " + stack.Count;
            view.Catcher.OnClick = () =>
            {
                if (!m.Mandatory) Close(m);
            };
            view.Close.SetOnClick(() => Close(m));
            m.Root = view.Root;
            m.Sheet = view.Sheet;
            m.Body = view.Sheet;
            stack.Add(m);
            StartCoroutine(SlideIn(view.Sheet, view.Dim));
            return m;
        }

        // Hộp báo nhanh: tiêu đề, câu chữ, một nút (prefab Dialogs/Bao).
        public Modal Alert(string title, string text, string ok = "OK", Action onOk = null, bool mandatory = true)
        {
            var d = Open<AlertDialog>(mandatory: mandatory);
            d.Show(title, text, ok, onOk);
            return d.Modal;
        }

        // Hộp xác nhận hai nút (prefab Dialogs/XacNhan).
        public Modal Confirm(string title, string text, string yes, Action onYes, string no = "Thôi", BtnColor yesColor = BtnColor.Red)
        {
            var d = Open<ConfirmDialog>();
            d.Show(title, text, yes, onYes, no, yesColor);
            return d.Modal;
        }

        public void Close(Modal m)
        {
            if (!m.IsOpen) return;
            stack.Remove(m);
            var view = m.View;
            m.Root = null;
            m.View = null;
            StartCoroutine(FadeOut(view));
            m.OnClose?.Invoke();
        }

        public void CloseAll()
        {
            for (int i = stack.Count - 1; i >= 0; i--) Close(stack[i]);
        }

        // nút Back của Android: đóng hộp trên cùng nếu không bắt buộc. Trả true nếu đã xử lý.
        public bool Back()
        {
            if (stack.Count == 0) return false;
            var top = stack[stack.Count - 1];
            if (!top.Mandatory) Close(top);
            return true;
        }

        IEnumerator SlideIn(RectTransform sheet, Image dim)
        {
            var target = sheet.anchoredPosition;
            var dimColor = dim.color;
            const float dur = 0.32f;
            for (float t = 0; t < dur; t += Time.unscaledDeltaTime)
            {
                if (!sheet) yield break;
                float k = t / dur;
                // web: translateY(60px) rotate(4deg) scale(0.9), nảy (0.2, 1.5, 0.4, 1)
                float e = 1 - Mathf.Pow(1 - k, 3) + Mathf.Sin(k * Mathf.PI) * 0.12f;
                sheet.anchoredPosition = target + new Vector2(0, -120 * (1 - e));
                sheet.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(4, -0.6f, e));
                float s = Mathf.Lerp(0.9f, 1, e);
                sheet.localScale = new Vector3(s, s, 1);
                dim.color = new Color(dimColor.r, dimColor.g, dimColor.b, dimColor.a * Mathf.Clamp01(k * 1.8f));
                yield return null;
            }
            if (!sheet) yield break;
            sheet.anchoredPosition = target;
            sheet.localEulerAngles = new Vector3(0, 0, -0.6f);
            sheet.localScale = Vector3.one;
            dim.color = dimColor;
        }

        IEnumerator FadeOut(ModalSheet view)
        {
            var cg = view.Group;
            cg.blocksRaycasts = false;
            for (float t = 0; t < 0.15f; t += Time.unscaledDeltaTime)
            {
                if (!view) yield break;
                cg.alpha = 1 - t / 0.15f;
                yield return null;
            }
            if (view) Destroy(view.gameObject);
        }
    }
}
