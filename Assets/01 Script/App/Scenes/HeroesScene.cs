// Tướng (chép heroesScreen của Web/src/view/screens/heroes.ts): lưới 3 cột thẻ tướng, tướng đã có xếp trước.
// Mỗi thẻ là một bản sao prefab Items/TheTuong (HeroTile). Chạm thẻ mở hộp chi tiết.
// Prefab màn hình Assets/04 Prefabs/Screens/Heroes.
using System.Linq;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class HeroesScene : SceneRoot
    {
        public override string Title => "Tướng";

        [SerializeField] RectTransform grid;
        [SerializeField] HeroTile tilePrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform gridRt, HeroTile tile)
        {
            grid = gridRt;
            tilePrefab = tile;
        }

        public override void Enter(object args) => Render();

        public override void Refresh() => Render();

        void Render()
        {
            if (!grid) return;
            for (int i = grid.childCount - 1; i >= 0; i--) Destroy(grid.GetChild(i).gameObject);
            var d = App.Data;
            var s = App.Save.Data;
            var list = d.Heroes.OrderByDescending(h => s.Hero(h.id).owned).ToList();
            for (int i = 0; i < list.Count; i++)
            {
                string id = list[i].id;
                var tile = Ui.Spawn(tilePrefab, grid);
                tile.Bind(list[i], s, d, i, () =>
                {
                    App.Audio.Play("click");
                    HeroDetail.Open(id, Render);
                });
            }
        }
    }
}
