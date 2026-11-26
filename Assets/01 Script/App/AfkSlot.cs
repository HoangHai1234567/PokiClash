// Một ô trong khay rương AFK (prefab Items/RuongAfk, menu "PokiClash/Prefab/Hộp thoại và màn/AFK: hộp Đội tự đi ải"; người dùng
// 2026-11-27: hộp cũ "nhìn không rõ ràng, khó hiểu và xấu", rương vẽ tạm "cũng xấu"). Gốc là nút giấy; trong có rương gỗ thật
// (Kit/Ruong: ảnh pk_ruong_go và rig AtomSpine như máy bi), thanh đếm giờ nhỏ, chữ dưới rương. Bốn trạng thái:
//   - trống: thẻ giấy sẫm, bóng rương mờ (chỗ rương sẽ vào);
//   - chờ (rương xếp sau, chưa tới lượt đếm): rương nhạt, chữ "Chờ";
//   - đang đếm: rương thở (rig "cho"), giờ còn lại, thanh đầy dần;
//   - mở được: thẻ xanh, rương nhún nhắc (rig "nhac"), chữ "MỞ!".
// Hộp AFK dựng sẵn đủ ô cho khay lớn nhất (Thẻ Phiêu Lưu 5 ô), đặt chỗ và ẩn bớt lúc chạy.
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class AfkSlot : MonoBehaviour
    {
        public enum State { Empty, Waiting, Counting, Ready }

        [SerializeField] SketchButton button;
        [SerializeField] ChestIcon chest;
        [SerializeField] CanvasGroup chestFade; // độ đậm của rương (trống: bóng mờ, chờ: nhạt)
        [SerializeField] TextMeshProUGUI label;
        [SerializeField] RectTransform barBack, barFill; // thanh đếm giờ (rộng thanh fill = tiến độ × rộng nền)

        public static readonly Color ReadyColor = Theme.Hex("#dff3cf");
        const float ChestW = 0.72f; // bề ngang rương so với bề ngang ô

        public SketchButton Button => button;
        public RectTransform Rect => (RectTransform)transform;

        State state = (State)(-1);
        float width = -1;

        // Dùng khi nướng prefab (Editor).
        public void Setup(SketchButton btn, ChestIcon chestIcon, CanvasGroup fade, TextMeshProUGUI text, RectTransform back, RectTransform fill)
        {
            button = btn;
            chest = chestIcon;
            chestFade = fade;
            label = text;
            barBack = back;
            barFill = fill;
        }

        // đặt ô: x lệch so với giữa khay (gốc ô ở mép trên), w bề rộng ô
        public void Arrange(float x, float w)
        {
            Rect.anchoredPosition = new Vector2(x, Rect.anchoredPosition.y);
            Rect.sizeDelta = new Vector2(w, Rect.sizeDelta.y);
            if (Mathf.Abs(w - width) < 0.5f) return;
            width = w;
            if (chest) chest.Bind(Core.SlotKind.ChestWood, w * ChestW);
            state = (State)(-1); // rương vừa Bind lại: chạy lại clip rig ở lần Set kế
        }

        // st: trạng thái; text: chữ dưới rương; progress: tiến độ đếm giờ (0–1, chỉ dùng khi đang đếm); phase: lệch nhịp rig giữa các ô
        public void Set(State st, string text, float progress = 0, float phase = 0)
        {
            label.text = text;
            bool counting = st == State.Counting;
            if (barBack) barBack.gameObject.SetActive(counting);
            if (counting && barFill && barBack)
                barFill.sizeDelta = new Vector2(Mathf.Max(barBack.rect.height, barBack.rect.width * Mathf.Clamp01(progress)), barFill.sizeDelta.y);
            if (st == state) return;
            state = st;
            button.SetColor(st == State.Empty ? Theme.Paper2 : st == State.Ready ? ReadyColor : Theme.Paper);
            label.color = st == State.Ready ? Theme.GreenD : st == State.Counting ? Theme.Ink : Theme.Ink2;
            label.fontStyle = st == State.Ready ? FontStyles.Bold : FontStyles.Normal;
            if (chestFade) chestFade.alpha = st == State.Empty ? 0.16f : st == State.Waiting ? 0.6f : 1;
            if (!chest) return;
            // rig chỉ chạy ở rương đang đếm (thở) và rương mở được (nhắc); rương trống, chờ để ảnh tĩnh cho nhẹ
            if (st == State.Ready) chest.PlayRig("nhac", true, phase);
            else if (st == State.Counting) chest.PlayRig("cho", true, phase);
            else chest.StopRig();
        }
    }
}
