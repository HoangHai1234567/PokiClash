// Đền Huy Hiệu: khung giới thiệu (sao cả đền, mốc quà kế tiếp, luật sao; thanh tới mốc kế), rồi 5 bệ theo hệ (theo thứ tự đảo). Mỗi bệ:
// huy hiệu bậc cao nhất (hoặc bóng mờ), bậc đang đánh và tiến độ, sao của dãy, phần cộng, đặc tính hệ, nút "Thử thách" mở danh sách trận
// của bậc (đã thắng có sao và "Đánh lại" khi chưa đủ 3 sao, trận đang đánh có nút "Đánh", sau đó khoá; "‹" / "›" xem bậc khác).
// Dãy chưa mở ghi điều kiện. Trận mở hộp chuẩn bị dùng chung với đảo.
// Prefab màn hình Assets/04 Prefabs/Screens/Badges (nền, khung cuộn, khung giới thiệu gioi_thieu/chu); mỗi bệ là bản sao prefab
// Items/BenHuyHieu (BadgePedestal), sinh một lần rồi gán lại khi làm mới; danh sách trận là hộp Dialogs/DanhSachTranHuyHieu (BadgeListDialog).
// 2026-11-17: thanh mốc sao (thanh_moc_sao) do menu "PokiClash/Prefab/Đền Huy Hiệu: sao trận, chọn bậc, mốc sao" dựng; chưa có thì chỉ chữ.
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class BadgesScene : SceneRoot
    {
        public override string Title => Loc.T("Đền Huy Hiệu");

        [SerializeField] RectTransform list; // cột dọc trong khung cuộn: khung giới thiệu rồi các bệ
        [SerializeField] BadgePedestal pedestalPrefab;
        [SerializeField] BadgeListDialog listPrefab;
        [SerializeField] TextMeshProUGUI intro; // 2026-11-17: chữ khung giới thiệu (trống thì tìm gioi_thieu/chu)
        [SerializeField] UiBar starBar; // 2026-11-17: thanh tới mốc sao kế (có thể trống)

        readonly List<BadgePedestal> pedestals = new List<BadgePedestal>();

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform listRt, BadgePedestal pedestal, BadgeListDialog listDialog)
        {
            list = listRt;
            pedestalPrefab = pedestal;
            listPrefab = listDialog;
        }

        public override void Enter(object args)
        {
            Build();
            if (args is Elem z) OpenList(z);
        }

        public override void Refresh() => Build();

        void Build()
        {
            if (!list) return;
            RenderIntro();
            var zones = D.Zones.OrderBy(x => x.order).ToList();
            while (pedestals.Count < zones.Count) pedestals.Add(Ui.Spawn(pedestalPrefab, list));
            for (int i = pedestals.Count - 1; i >= zones.Count; i--)
            {
                Destroy(pedestals[i].gameObject);
                pedestals.RemoveAt(i);
            }
            for (int i = 0; i < zones.Count; i++)
            {
                var z = zones[i].id;
                pedestals[i].Bind(zones[i], S, D, () => OpenList(z));
            }
        }

        // sao cả đền, mốc kế tiếp và quà, luật sao
        void RenderIntro()
        {
            if (!intro) intro = list.Find("gioi_thieu/chu")?.GetComponent<TextMeshProUGUI>();
            var cfg = D.Cfg;
            int total = Badges.TotalStars(S, cfg), next = Badges.NextGift(S, cfg);
            string gift = "";
            if (next > 0)
            {
                var g = Badges.GiftOf(cfg, next);
                var parts = new List<string>();
                if (!string.IsNullOrEmpty(g.chest)) parts.Add(Pachinko.ChestName(Pachinko.FromKey(g.chest)));
                if (g.evo > 0) parts.Add(Loc.F("{0} đá tiến hóa", g.evo));
                if (g.crystal > 0) parts.Add(Loc.F("{0} đá tinh", g.crystal));
                if (g.stones > 0) parts.Add(Loc.F("{0} đá tiềm năng", g.stones));
                gift = Loc.F("Mốc kế {0} sao: {1}.", Badges.GiftAt(cfg, next), string.Join(", ", parts));
            }
            else gift = Loc.T("Đã nhận hết mốc sao.");
            if (intro)
            {
                // ngắn để vừa khung (bản dài tràn mất dòng đầu, 2026-11-17); luật sao chi tiết nằm ở hộp danh sách trận
                intro.text = Loc.F("Sao đền: {0}/{1}. {2}\n", total, Badges.MaxStars(cfg), gift) +
                             Loc.F("Mỗi trận 3 sao: thắng · không ai gục · thắng trong {0} hiệp mỗi địch. Đánh lại để lấy thêm sao.", cfg.badges.starRounds);
                if (!intro.enableAutoSizing) // chữ quá dài thì co lại (không lớn hơn cỡ gốc), không tràn khỏi khung
                {
                    intro.fontSizeMax = intro.fontSize;
                    intro.fontSizeMin = Mathf.Min(16, intro.fontSize);
                    intro.enableAutoSizing = true;
                }
            }
            if (starBar)
            {
                int from = next > 1 ? Badges.GiftAt(cfg, next - 1) : 0, to = next > 0 ? Badges.GiftAt(cfg, next) : total;
                starBar.gameObject.SetActive(next > 0);
                if (next > 0) starBar.Set(total - from, to - from, 0, null, true);
            }
        }

        // danh sách trận của bậc đang đánh (đã xong dãy thì bậc cuối, để đánh lại lấy sao)
        void OpenList(Elem z)
        {
            var cfg = D.Cfg;
            if (!Badges.LineOpen(S, z)) return;
            int tier = Badges.Current(S, cfg, z)?.tier ?? Badges.MaxTier(cfg);
            App.Modals.Open(listPrefab).Show(z, tier, (t, idx) => StagePrep.OpenBadge(z, t, idx));
        }
    }
}
