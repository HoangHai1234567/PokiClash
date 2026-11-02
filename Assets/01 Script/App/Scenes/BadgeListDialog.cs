// Hộp danh sách trận của bậc đang đánh ở Đền Huy Hiệu (prefab Assets/04 Prefabs/Dialogs/DanhSachTranHuyHieu): đầu hộp (huy hiệu,
// "Hệ · Bậc", số trận và phần thưởng xong bậc), mỗi trận là một bản sao prefab Items/TranHuyHieu (BadgeStageRow).
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class BadgeListDialog : Dialog
    {
        [SerializeField] RectTransform body; // tờ giấy (dọc, tự giãn): các trận sinh nối sau đầu hộp
        [SerializeField] BadgeIcon badge;
        [SerializeField] TextMeshProUGUI title, sub;
        [SerializeField] BadgeStageRow rowPrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform sheet, BadgeIcon badgeIcon, TextMeshProUGUI titleText, TextMeshProUGUI subText, BadgeStageRow row)
        {
            body = sheet;
            badge = badgeIcon;
            title = titleText;
            sub = subText;
            rowPrefab = row;
        }

        // bậc tier của hệ z, đang ở trận at; onFight(i): đã đóng hộp, mở chuẩn bị trận i
        public void Show(Elem z, int tier, int at, Action<int> onFight)
        {
            var d = App.Data;
            var cfg = d.Cfg;
            int n = Badges.Count(cfg, tier);
            badge.Bind(z, tier, 120);
            title.text = $"{Elements.Name(z)} · {Badges.TierName(cfg, tier)}";
            title.color = Theme.Of(z);
            sub.text = $"{n} trận, đánh lần lượt · xong bậc: +{Badges.Bonus(cfg, tier) * 100:0}% cho tướng hệ {Elements.Name(z)} và {Pachinko.ChestName(Pachinko.FromKey(cfg.badges.chest[tier - 1]))}";
            for (int i = 1; i <= n; i++)
            {
                int idx = i;
                var row = Ui.Spawn(rowPrefab, body);
                row.Bind(d, Badges.Stage(d, z, tier, i), i, n, i < at, i == at, () =>
                {
                    Close();
                    onFight(idx);
                });
            }
        }
    }
}
