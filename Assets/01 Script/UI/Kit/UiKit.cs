// Prefab của bộ kit (Assets/04 Prefabs/Kit, dựng bằng menu "PokiClash/Prefab/2. Nướng bộ kit"): nút 5 cỡ, khung, chip, thanh,
// nhãn hệ, sao, băng keo, con dấu, gợi ý, thẻ bài. Sửa prefab là mọi chỗ dùng đổi theo.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    [CreateAssetMenu(menuName = "PokiClash/UiKit", fileName = "UiKit")]
    public sealed class UiKit : ScriptableObject
    {
        [Header("Nút theo cỡ")]
        public SketchButton buttonBig;
        public SketchButton buttonNormal;
        public SketchButton buttonSmall;
        public SketchButton buttonTiny;
        public SketchButton buttonRound;

        [Header("Khung và mảnh trang trí")]
        public Image panel;
        public Image panelThin;
        public Image tape;
        public UiStamp stamp;
        public UiHint hint;

        [Header("Chỉ số")]
        public UiChip chip;
        public UiBar bar;
        public UiElemTag elemTag;
        public UiStars stars;

        [Header("Thẻ bài")]
        public UiCard card;
        public UiCard cardMini;

        [Header("Tướng, huy hiệu")]
        public HeroPortrait portrait;
        public BadgeIcon badge;

        [Header("Rương")]
        public ChestIcon chest;

        [Header("Canvas màn hình (Nen / An toan / Khung)")]
        public PokiCanvas canvas;

        [Header("Hộp thoại mở từ nhiều nơi (tra theo kiểu)")]
        public List<Dialog> dialogs = new List<Dialog>();

        // Prefab hộp có component kiểu T trong danh sách dialogs.
        public T GetDialog<T>() where T : Dialog
        {
            foreach (var d in dialogs)
                if (d is T t) return t;
            throw new System.Exception($"UiKit thiếu hộp {typeof(T).Name}: chạy PokiClash/Prefab/4. Nướng màn hình.");
        }

        public SketchButton Button(BtnSize s) =>
            s == BtnSize.Big ? buttonBig : s == BtnSize.Small ? buttonSmall : s == BtnSize.Tiny ? buttonTiny : s == BtnSize.Round ? buttonRound : buttonNormal;
    }
}
