// Đền Huy Hiệu: 5 bệ theo hệ (theo thứ tự đảo). Mỗi bệ: huy hiệu bậc cao nhất (hoặc bóng mờ), bậc đang đánh và tiến độ n/5 hay n/10,
// phần cộng hiện tại, nút "Thử thách" mở danh sách trận của bậc (đã thắng có dấu tích, trận đang đánh có nút "Đánh", sau đó khoá).
// Dãy chưa mở ghi điều kiện. Trận mở hộp chuẩn bị dùng chung với đảo.
// Prefab màn hình Assets/04 Prefabs/Screens/Badges (nền, khung cuộn, khung giới thiệu); mỗi bệ là bản sao prefab Items/BenHuyHieu
// (BadgePedestal), sinh một lần rồi gán lại khi làm mới; danh sách trận là hộp Dialogs/DanhSachTranHuyHieu (BadgeListDialog).
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class BadgesScene : SceneRoot
    {
        public override string Title => "Đền Huy Hiệu";

        [SerializeField] RectTransform list; // cột dọc trong khung cuộn: khung giới thiệu rồi các bệ
        [SerializeField] BadgePedestal pedestalPrefab;
        [SerializeField] BadgeListDialog listPrefab;

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

        // danh sách trận của bậc đang đánh
        void OpenList(Elem z)
        {
            var cfg = D.Cfg;
            var cur = Badges.Current(S, cfg, z);
            if (cur == null) return;
            var (tier, at) = cur.Value;
            App.Modals.Open(listPrefab).Show(z, tier, at, idx => StagePrep.OpenBadge(z, tier, idx));
        }
    }
}
