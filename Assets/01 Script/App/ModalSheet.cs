// Tờ giấy gốc của hộp thoại (prefab Assets/04 Prefabs/Dialogs/HopThoai): nền tối nhận chạm, tờ giấy tự giãn theo nội dung,
// lưới kẻ ô, băng keo, nút đóng góc phải. Mỗi hộp riêng là biến thể (prefab variant) của tờ giấy này, kèm component kế thừa Dialog;
// bề rộng, bắt buộc (không nút đóng, chạm ngoài không đóng), dính mép trên chỉnh trên biến thể.
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ModalSheet : MonoBehaviour
    {
        [SerializeField] Image dim;
        [SerializeField] ClickCatcher catcher;
        [SerializeField] RectTransform sheet;
        [SerializeField] SketchButton close;
        [SerializeField] CanvasGroup group;
        [Tooltip("Bắt buộc: không nút đóng, chạm ra ngoài không đóng")]
        [SerializeField] bool mandatory;
        [Tooltip("Dính mép trên (cách 140) thay vì giữa màn")]
        [SerializeField] bool top;

        public RectTransform Root => (RectTransform)transform;
        public Image Dim => dim;
        public ClickCatcher Catcher => catcher;
        public RectTransform Sheet => sheet;
        public SketchButton Close => close;
        public CanvasGroup Group => group;
        public bool Mandatory => mandatory;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image dimImg, ClickCatcher click, RectTransform sheetRt, SketchButton closeBtn, CanvasGroup cg)
        {
            dim = dimImg;
            catcher = click;
            sheet = sheetRt;
            close = closeBtn;
            group = cg;
        }

        // Bề rộng tờ giấy (khung 1080), bắt buộc, dính mép trên.
        public void Configure(float width, bool isMandatory, bool atTop)
        {
            mandatory = isMandatory;
            top = atTop;
            sheet.anchorMin = sheet.anchorMax = new Vector2(0.5f, top ? 1 : 0.5f);
            sheet.pivot = new Vector2(0.5f, top ? 1 : 0.5f);
            sheet.anchoredPosition = new Vector2(0, top ? -140 : 0);
            sheet.sizeDelta = new Vector2(width, sheet.sizeDelta.y);
            close.gameObject.SetActive(!mandatory);
        }

        // Bật tắt bắt buộc cho một lần mở (hộp báo dùng chung).
        public void SetMandatory(bool isMandatory)
        {
            mandatory = isMandatory;
            close.gameObject.SetActive(!mandatory);
        }
    }

    // Gốc của một hộp thoại riêng (đặt trên biến thể của tờ giấy gốc). ModalService.Open(prefab) gắn Modal để đóng.
    public abstract class Dialog : MonoBehaviour
    {
        public Modal Modal { get; internal set; }
        public void Close() => Modal?.Close();
    }
}
