// Sổ thẻ (chép cardsScreen của Web/src/view/screens/cards.ts): khung "Cách xếp thẻ", chú giải độ hiếm kèm trọng số rút,
// lưới 23 thẻ chung (thẻ chưa mở xám, "Mở ở cấp n"). Chạm thẻ xem chi tiết và mô tả ở cấp 5.
// Prefab màn hình Assets/04 Prefabs/Screens/Cards; thẻ sinh từ prefab kit theo dữ liệu, hộp chi tiết là Dialogs/ChiTietThe.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CardsScene : SceneRoot
    {
        public override string Title => "Sổ thẻ";

        [SerializeField] RectTransform grid;
        [SerializeField] LayoutElement gridLayout;
        [SerializeField] TextMeshProUGUI[] legend; // 5 độ hiếm, Thường → Huyền thoại
        [SerializeField] CardDetailDialog detailPrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform gridRt, TextMeshProUGUI[] legendTexts, CardDetailDialog detail)
        {
            grid = gridRt;
            gridLayout = grid.GetComponent<LayoutElement>();
            legend = legendTexts;
            detailPrefab = detail;
        }

        public override void Enter(object args)
        {
            var d = App.Data;
            var save = App.Save.Data;
            for (int r = 0; r < legend.Length; r++)
                legend[r].text = LegendText(d, (Rarity)r);

            int rows = (d.Pool.Count + 2) / 3;
            gridLayout.preferredHeight = rows * (UiCard.NormalSize.y + 40);
            for (int i = grid.childCount - 1; i >= 0; i--) Destroy(grid.GetChild(i).gameObject);
            foreach (var c in d.Pool)
            {
                var card = c;
                string locked = c.unlock > save.level ? $"Mở ở cấp {c.unlock}" : null;
                UiCard.Create(grid, c, 1, false, App.Art.Icon(c.icon), locked, () => App.Modals.Open(detailPrefab).Show(card));
            }
        }

        public static string LegendText(GameData d, Rarity r) => $"{Elements.RarityName(r)} · nặng {d.Cfg.PoolWeight(r)}";
    }
}
