// Hộp nhận huy hiệu khi xong một bậc ở Đền Huy Hiệu (prefab Assets/04 Prefabs/Dialogs/TranHuyHieu): huy hiệu lớn, tên huy hiệu
// màu hệ, phần thưởng chỉ số, nút "Mở <rương>" (tên mo_ruong_huy_hieu). Đóng hộp thì trận mở rương.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class BadgeWinDialog : Dialog
    {
        [SerializeField] BadgeIcon badge;
        [SerializeField] TextMeshProUGUI title, text;
        [SerializeField] SketchButton open;

        // Dùng khi nướng prefab (Editor).
        public void Setup(BadgeIcon badgeIcon, TextMeshProUGUI titleText, TextMeshProUGUI bodyText, SketchButton openBtn)
        {
            badge = badgeIcon;
            title = titleText;
            text = bodyText;
            open = openBtn;
        }

        public void Show(Elem zone, int tier, string titleText, string body, string buttonLabel)
        {
            badge.Bind(zone, tier, 300);
            title.text = titleText;
            title.color = Theme.Of(zone);
            text.text = body;
            open.SetText(buttonLabel);
            open.SetOnClick(Close);
        }
    }
}
