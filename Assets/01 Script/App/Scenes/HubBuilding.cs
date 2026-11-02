// Một công trình side meta ở rìa làng trên sảnh (prefab mục Items/CongTrinh; bốn bản sao đặt sẵn trong Screens/Hub):
// khung giấy, icon, tên, chấm đỏ báo việc. Chưa mở thì phác chì (khung mờ, icon và chữ xám).
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

        // alert: chấm đỏ (dãy huy hiệu mới, trang trại cần chăm, cây bi đầy)
        public void Bind(string title, bool open, bool alert, Action onClick)
        {
            bg.color = open ? Theme.CardFill : new Color(0.93f, 0.9f, 0.84f, 0.55f);
            icon.color = open ? Color.white : new Color(0.45f, 0.42f, 0.4f, 0.6f);
            label.text = title;
            label.color = open ? Theme.Ink : Theme.Ink3;
            dot.gameObject.SetActive(alert);
            click.OnClick = onClick;
        }
    }
}
