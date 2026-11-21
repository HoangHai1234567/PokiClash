// Nút tròn icon của màn Nhà (kiểu nút thao tác của Clash of Critters, GD_Claude/22_Critters_Home.md mục 7): biến thể prefab của
// Kit/Nut_Tron (nút sticker lõi màu), thêm icon giữa nút, chữ ngắn dưới nút (trắng viền mực cho đọc được trên bản đồ), dòng giá
// dưới chữ và chấm đỏ góc trên. Prefab Items/NutVongNha dựng bằng menu "PokiClash/Prefab/Nhà: giao diện kiểu Critters"
// (Editor/HomeSceneMenu.cs). Dùng cho vòng nút quanh vật đang chọn (HomeRing) và hàng nút dưới màn Nhà.
// Nút khoá (thiếu gỗ, thợ bận...): mờ, chạm thì lắc + kêu lỗi (SketchButton) và gọi denied (báo lý do).
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HomeRingButton : MonoBehaviour, IPointerClickHandler
    {
        [SerializeField] SketchButton button;
        [SerializeField] Image icon;
        [SerializeField] TextMeshProUGUI caption;
        [SerializeField] RectTransform costBg;
        [SerializeField] TextMeshProUGUI cost;
        [SerializeField] GameObject dot;

        Action denied;

        public SketchButton Button => button;
        public RectTransform Rt => (RectTransform)transform;

        // Dùng khi dựng prefab (Editor).
        public void Setup(SketchButton b, Image iconImg, TextMeshProUGUI captionText, RectTransform costRt, TextMeshProUGUI costText, GameObject dotGo)
        {
            button = b;
            icon = iconImg;
            caption = captionText;
            costBg = costRt;
            cost = costText;
            dot = dotGo;
        }

        // icon, chữ dưới nút, dòng giá (null = ẩn), màu lõi, bật / khoá, việc khi bấm, việc khi bấm lúc khoá (báo lý do)
        public void Set(Sprite s, string text, string costText, BtnColor color, bool on, Action act, Action whenDenied = null)
        {
            if (icon)
            {
                icon.sprite = s;
                icon.enabled = s;
                icon.color = on ? Color.white : new Color(1, 1, 1, 0.6f);
            }
            SetCaption(text);
            if (costBg) costBg.gameObject.SetActive(!string.IsNullOrEmpty(costText));
            if (cost) cost.text = costText ?? "";
            button.SetRole(color);
            button.Interactable = on;
            button.SetOnClick(act);
            denied = whenDenied;
        }

        // chữ nằm trong viên giấy (cho đọc được trên cỏ sáng): bật / tắt cả viên
        public void SetCaption(string text)
        {
            if (!caption) return;
            var holder = caption.transform.parent != transform ? caption.transform.parent.gameObject : caption.gameObject;
            holder.SetActive(!string.IsNullOrEmpty(text));
            caption.text = text ?? "";
        }

        public void SetIcon(Sprite s)
        {
            if (!icon) return;
            icon.sprite = s;
            icon.enabled = s;
        }

        // chấm đỏ: có đồ chờ thu, có việc làm được
        public void Dot(bool on)
        {
            if (dot && dot.activeSelf != on) dot.SetActive(on);
        }

        // SketchButton khoá không gọi việc bấm: nút này nhận cùng cú chạm để báo lý do
        public void OnPointerClick(PointerEventData e)
        {
            if (button && !button.Interactable && !button.Locked) denied?.Invoke();
        }
    }
}
