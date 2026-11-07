// Tướng (chép heroesScreen của Web/src/view/screens/heroes.ts): trên là đội hình (TeamLineup: 3 tướng trong đội, vuốt ngang),
// dưới là lưới 3 cột thẻ tướng: chỉ tướng đã có (xếp trước, theo lực chiến giảm dần) và tướng chưa mở mà đã có mảnh (bóng sẫm, nhiều mảnh
// trước); tướng chưa có mảnh nào thì ẩn (người dùng dặn 2026-11-03). Mỗi thẻ là một bản sao prefab Items/TheTuong (HeroTile).
// Chạm thẻ mở hộp chi tiết. Prefab màn hình Assets/04 Prefabs/Screens/Heroes.
// Làm mới (lên cấp, tiến hóa, đổi đội: mỗi lần lưu gọi Refresh, hộp chi tiết gọi thêm lần nữa) giữ các ô đã dựng và gán lại dữ liệu,
// chỉ dựng thêm ô khi lưới dài ra: phá đi dựng lại cả lưới mỗi lần bấm làm máy giật (người dùng báo 2026-11-07).
using System.Collections.Generic;
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
        readonly List<HeroTile> tiles = new List<HeroTile>(); // ô đã dựng, theo thứ tự trong lưới

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
            // lần đầu: bỏ ô mẫu còn trong prefab
            if (tiles.Count == 0)
                for (int i = grid.childCount - 1; i >= 0; i--) Destroy(grid.GetChild(i).gameObject);
            var d = App.Data;
            var s = App.Save.Data;
            var list = d.Heroes.Where(h => s.Hero(h.id).owned || s.Hero(h.id).shards > 0)
                .OrderByDescending(h => s.Hero(h.id).owned)
                .ThenByDescending(h => s.Hero(h.id).owned ? HeroStats.Power(d.Cfg, h, Teams.MemberOf(s, h.id, d)) : s.Hero(h.id).shards).ToList();
            for (int i = 0; i < list.Count; i++)
            {
                string id = list[i].id;
                HeroTile tile;
                if (i < tiles.Count) tile = tiles[i];
                else
                {
                    tile = Ui.Spawn(tilePrefab, grid);
                    tiles.Add(tile);
                    // bộ UI Sa Bàn: ô tướng nhún nhẹ tại chỗ; lúc vào màn thì nảy ra lần lượt từ dưới lên
                    var mo = PokiClash.UI.UiMotion.Of(tile);
                    mo.idleLift = 4;
                    mo.idleTilt = 0.4f;
                    mo.idlePeriod = 3.8f;
                    mo.idle = true;
                    mo.spawnFrom = PokiClash.UI.UiMotion.SpawnFrom.Up;
                }
                tile.gameObject.SetActive(true);
                tile.Bind(list[i], s, d, i, () =>
                {
                    App.Audio.Play("click");
                    HeroDetail.Open(id, Refresh);
                });
                if (popIn) PokiClash.UI.UiMotion.Of(tile).Spawn(0.12f + i * 0.04f);
            }
            // lưới ngắn lại (hiếm): ẩn ô thừa, giữ để dùng lại
            for (int i = list.Count; i < tiles.Count; i++) tiles[i].gameObject.SetActive(false);
        }
    }
}
