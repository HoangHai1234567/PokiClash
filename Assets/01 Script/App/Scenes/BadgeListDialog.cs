// Hộp danh sách trận của một bậc ở Đền Huy Hiệu (prefab Assets/04 Prefabs/Dialogs/DanhSachTranHuyHieu): đầu hộp (huy hiệu,
// "Hệ · Bậc", số trận, sao của bậc, phần thưởng xong bậc, đặc tính hệ mở ở bậc này), mỗi trận là một bản sao prefab Items/TranHuyHieu
// (BadgeStageRow). 2026-11-17: nút "‹" / "›" (bac_truoc, bac_sau) xem bậc đã qua để đánh lại lấy sao; nút do menu
// "PokiClash/Prefab/Nhà và side meta/Đền Huy Hiệu: sao trận, chọn bậc, mốc sao" dựng (prefab cũ không có nút thì chỉ xem bậc mở hộp).
using System;
using System.Collections.Generic;
using System.Linq;
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
        [SerializeField] SketchButton prev, next; // 2026-11-17, có thể trống

        readonly List<BadgeStageRow> rows = new List<BadgeStageRow>();
        Elem zone;
        int shown;
        Action<int, int> fight;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform sheet, BadgeIcon badgeIcon, TextMeshProUGUI titleText, TextMeshProUGUI subText, BadgeStageRow row)
        {
            body = sheet;
            badge = badgeIcon;
            title = titleText;
            sub = subText;
            rowPrefab = row;
        }

        // bậc cao nhất xem được: bậc đang đánh (hoặc bậc cuối nếu đã xong dãy)
        static int TopTier(SaveData s, BalanceConfig cfg, Elem z) => Badges.Current(s, cfg, z)?.tier ?? Badges.MaxTier(cfg);

        // mở ở bậc tier của hệ z; onFight(bậc, trận): đã đóng hộp, mở chuẩn bị trận
        public void Show(Elem z, int tier, Action<int, int> onFight)
        {
            zone = z;
            fight = onFight;
            if (prev) prev.SetOnClick(() => Render(shown - 1));
            if (next) next.SetOnClick(() => Render(shown + 1));
            Render(tier);
        }

        void Render(int tier)
        {
            var d = App.Data;
            var s = App.Save.Data;
            var cfg = d.Cfg;
            int top = TopTier(s, cfg, zone);
            shown = tier = Mathf.Clamp(tier, 1, top);
            int n = Badges.Count(cfg, tier);
            var cur = Badges.Current(s, cfg, zone);
            badge.Bind(zone, tier, 120);
            title.text = $"{Elements.Name(zone)} · {Badges.TierName(cfg, tier)}";
            title.color = Theme.Of(zone);
            var parts = new List<string>
            {
                Loc.F("{0} trận · {1}/{2} sao", n, Badges.TierStars(s, cfg, zone, tier), 3 * n),
                Loc.F("Xong bậc: hệ {0} +{1:0}% · {2}", Elements.Name(zone), Badges.Bonus(cfg, tier) * 100, Pachinko.ChestName(Pachinko.FromKey(cfg.badges.chest[Mathf.Min(tier, cfg.badges.chest.Count) - 1]))) +
                (tier <= cfg.badges.evo.Length && cfg.badges.evo[tier - 1] > 0 ? Loc.F(" · {0} đá tiến hóa", cfg.badges.evo[tier - 1]) : "") +
                (tier <= cfg.badges.crystal.Length && cfg.badges.crystal[tier - 1] > 0 ? Loc.F(" · {0} đá tinh", cfg.badges.crystal[tier - 1]) : ""),
            };
            if (cfg.badges.traitTiers.Contains(tier)) parts.Add((Badges.TraitLevel(cfg, tier) == 1 ? Loc.T("Mở ") : Loc.T("Nâng ")) + Badges.TraitText(cfg, zone, Badges.TraitLevel(cfg, tier)));
            sub.text = string.Join("\n", parts);
            if (prev) prev.Interactable = tier > 1;
            if (next) next.Interactable = tier < top;

            while (rows.Count < n) rows.Add(Ui.Spawn(rowPrefab, body));
            for (int i = 0; i < rows.Count; i++) rows[i].gameObject.SetActive(i < n);
            for (int i = 1; i <= n; i++)
            {
                int idx = i, t = tier;
                bool won = Badges.Won(s, cfg, zone, tier, i);
                bool now = cur != null && cur.Value.tier == tier && cur.Value.i == i;
                rows[i - 1].Bind(d, Badges.Stage(d, zone, tier, i), i, n, won, now, Badges.Stars(s, cfg, zone, tier, i), () =>
                {
                    Close();
                    fight(t, idx);
                });
            }
        }
    }
}
