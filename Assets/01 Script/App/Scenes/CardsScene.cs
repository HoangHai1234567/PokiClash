// Sổ thẻ (chép cardsScreen của Web/src/view/screens/cards.ts): khung "Cách xếp thẻ", chú giải độ hiếm kèm trọng số rút,
// lưới thẻ chung (75 thẻ từ 2026-11-17, xếp theo độ hiếm rồi cấp mở, cuộn dọc; thẻ chưa mở xám, "Mở ở cấp n"). Chạm thẻ xem chi tiết.
// Prefab màn hình Assets/04 Prefabs/Screens/Cards; thẻ sinh từ prefab kit theo dữ liệu, hộp chi tiết là Dialogs/ChiTietThe.
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CardsScene : SceneRoot
    {
        public override string Title => Loc.T("Sổ thẻ");

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
            // độ hiếm rồi cấp mở (OrderBy giữ thứ tự dữ liệu khi bằng nhau)
            foreach (var c in d.Pool.OrderBy(x => x.rarity).ThenBy(x => x.unlock))
            {
                var card = c;
                string locked = c.unlock > save.level ? Loc.F("Mở ở cấp {0}", c.unlock) : null;
                UiCard.Create(grid, c, 1, false, App.Art.Icon(c.icon), locked, () => App.Modals.Open(detailPrefab).Show(card));
            }
            // hướng dẫn sau trận 2 (C18–C19, 2026-11-24): vào Sổ thẻ là xong bước ép chạm; để người chơi xem một lúc rồi gợi ý về sảnh
            if (!Tutorial.CoreDone(save) && !Tutorial.Done(save, Tutorial.CardsGo))
            {
                Tutorial.Mark(save, Tutorial.CardsGo);
                App.Save.Save();
            }
            if (!Tutorial.CoreDone(save) && !Tutorial.Done(save, Tutorial.CardsBack)) StartCoroutine(TutorBack());
        }

        System.Collections.IEnumerator TutorBack()
        {
            yield return new WaitForSecondsRealtime(2.5f);
            while (App.Modals.Count > 0 || !Guide.Idle) yield return null; // đang xem chi tiết một thẻ
            Guide.Hint(Tutorial.CardsBack, "bar.back", Loc.T("Xem xong thì về sảnh."), 8);
        }

        public static string LegendText(GameData d, Rarity r) => Loc.F("{0} · nặng {1}", Elements.RarityName(r), d.Cfg.PoolWeight(r));
    }
}
