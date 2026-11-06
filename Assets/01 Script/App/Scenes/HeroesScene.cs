// Tướng (chép heroesScreen của Web/src/view/screens/heroes.ts): trên là đội hình (TeamLineup: 3 tướng trong đội, vuốt ngang),
// dưới là lưới 3 cột thẻ tướng: chỉ tướng đã có (xếp trước, theo lực chiến giảm dần) và tướng chưa mở mà đã có mảnh (bóng sẫm, nhiều mảnh
// trước); tướng chưa có mảnh nào thì ẩn (người dùng dặn 2026-11-03). Mỗi thẻ là một bản sao prefab Items/TheTuong (HeroTile).
// Chạm thẻ mở hộp chi tiết. Prefab màn hình Assets/04 Prefabs/Screens/Heroes.
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class HeroesScene : SceneRoot
    {
        public override string Title => "Tướng";

        [SerializeField] RectTransform grid;
        [SerializeField] HeroTile tilePrefab;
        [SerializeField] TeamLineup lineup;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform gridRt, HeroTile tile)
        {
            grid = gridRt;
            tilePrefab = tile;
        }

        bool popIn; // vào màn: ô tướng nảy ra lần lượt (làm mới sau đó thì không)

        public override void Enter(object args)
        {
            popIn = true;
            if (lineup) lineup.Bind(RenderGrid);
            RenderGrid();
            popIn = false;
        }

        public override void Refresh()
        {
            if (lineup) lineup.Bind(RenderGrid);
            RenderGrid();
        }

        void RenderGrid()
        {
            if (!grid) return;
            for (int i = grid.childCount - 1; i >= 0; i--) Destroy(grid.GetChild(i).gameObject);
            var d = App.Data;
            var s = App.Save.Data;
            var list = d.Heroes.Where(h => s.Hero(h.id).owned || s.Hero(h.id).shards > 0)
                .OrderByDescending(h => s.Hero(h.id).owned)
                .ThenByDescending(h => s.Hero(h.id).owned ? HeroStats.Power(d.Cfg, h, Teams.MemberOf(s, h.id, d)) : s.Hero(h.id).shards).ToList();
            for (int i = 0; i < list.Count; i++)
            {
                string id = list[i].id;
                var tile = Ui.Spawn(tilePrefab, grid);
                tile.Bind(list[i], s, d, i, () =>
                {
                    App.Audio.Play("click");
                    HeroDetail.Open(id, Refresh);
                });
                // bộ UI Sa Bàn: ô tướng nhún nhẹ tại chỗ; lúc vào màn thì nảy ra lần lượt từ dưới lên
                var m = PokiClash.UI.UiMotion.Of(tile);
                m.idleLift = 4;
                m.idleTilt = 0.4f;
                m.idlePeriod = 3.8f;
                m.idle = true;
                m.spawnFrom = PokiClash.UI.UiMotion.SpawnFrom.Up;
                if (popIn) m.Spawn(0.12f + i * 0.04f);
            }
        }
    }
}
