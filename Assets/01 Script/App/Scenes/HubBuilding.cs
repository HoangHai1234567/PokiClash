// Một công trình side meta ở rìa làng trên sảnh (prefab mục Items/CongTrinh; bốn bản sao đặt sẵn trong Screens/Hub):
// khung giấy, icon, tên, chấm đỏ báo việc. Chưa mở thì phác chì (khung mờ, icon và chữ xám).
// Kiểu huy hiệu (badge, menu "PokiClash/Prefab/Sảnh và đảo/Nút sảnh: huy hiệu", người dùng 2026-11-27: icon "bị chìm vào phần back,
// không đẹp và nhỏ quá"): khung giấy trong suốt (giữ làm vùng chạm), icon là huy hiệu vành vàng lòng màu đậm, tên chữ sáng trên băng tối.
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HubBuilding : MonoBehaviour
    {
        [SerializeField] Image bg, icon, dot;
        [SerializeField] TextMeshProUGUI label;
        [SerializeField] ClickCatcher click;
        [SerializeField] bool badge;
        // kiểu ô vuông (Editor/HubTileMenu.cs, người dùng 2026-11-27: icon hai cột sảnh "to rõ ràng, hình vuông bo tròn, có viền trắng"
        // như Clash of Critters): bg là lòng ô (Shop/v3/o_san_nen) tô màu tint, viền trắng là ảnh con, icon là hình to tràn mép trên,
        // tên chữ trắng viền mực ở đáy ô
        [SerializeField] bool tile;
        [SerializeField] Color tint = Color.white;

        public static readonly Color BadgeLabel = Theme.Hex("#fff1d2"), BadgeLabelLocked = Theme.Hex("#b9ad9c");
        static readonly Color LockedGray = new Color(0.55f, 0.55f, 0.6f, 1);

        public bool Badge => badge;
        public bool Tile => tile;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, Image iconImg, TextMeshProUGUI text, Image alertDot, ClickCatcher catcher)
        {
            bg = bgImg;
            icon = iconImg;
            label = text;
            dot = alertDot;
            click = catcher;
        }

        // Dùng khi nướng prefab (Editor): icon cố định của công trình.
        public void SetIcon(Sprite s) => icon.sprite = s;

        // Dùng khi nướng prefab (Editor): bật kiểu huy hiệu (icon là huy hiệu, nhãn đã dời lên băng tối)
        public void SetBadge(bool on) => badge = on;

        // Dùng khi nướng prefab (Editor): bật kiểu ô vuông, màu lòng ô
        public void SetTile(bool on, Color c)
        {
            tile = on;
            tint = c;
            if (on) badge = false;
        }

        public Image Bg => bg;
        public Image Icon => icon;
        public Image Dot => dot;
        public TextMeshProUGUI Label => label;

        // alert: chấm đỏ (dãy huy hiệu mới, trang trại cần chăm, cây bi đầy)
        public void Bind(string title, bool open, bool alert, Action onClick)
        {
            label.text = title;
            if (tile)
            {
                // chưa mở: lòng ô ngả xám, hình xám, chữ xám nhạt
                bg.color = open ? tint : Color.Lerp(tint, LockedGray, 0.75f);
                icon.color = open ? Color.white : new Color(0.62f, 0.6f, 0.6f, 1);
                label.color = open ? Color.white : BadgeLabelLocked;
            }
            else if (badge)
            {
                // khung giấy trong suốt nhưng vẫn nhận chạm; chưa mở thì huy hiệu ngả xám
                bg.color = Color.clear;
                icon.color = open ? Color.white : new Color(0.62f, 0.6f, 0.6f, 1);
                label.color = open ? BadgeLabel : BadgeLabelLocked;
            }
            else
            {
                bg.color = open ? Theme.CardFill : new Color(0.93f, 0.9f, 0.84f, 0.55f);
                icon.color = open ? Color.white : new Color(0.45f, 0.42f, 0.4f, 0.6f);
                label.color = open ? Theme.Ink : Theme.Ink3;
            }
            dot.gameObject.SetActive(alert);
            click.OnClick = onClick;
        }
    }
}
