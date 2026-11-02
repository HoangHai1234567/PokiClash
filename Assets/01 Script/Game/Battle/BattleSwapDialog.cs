// Hộp bắt buộc "Chọn tướng ra sân" khi tướng đang đánh gục (prefab Assets/04 Prefabs/Dialogs/TranDoiTuong):
// một ô (Items/TranTheDoi) cho mỗi tướng còn đứng, gợi ý khắc hệ.
using System;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class BattleSwapDialog : Dialog
    {
        [SerializeField] RectTransform row;
        [SerializeField] SwapCard cardPrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform rowRt, SwapCard card)
        {
            row = rowRt;
            cardPrefab = card;
        }

        // onPick(chỉ số tướng) gọi trước khi đóng hộp
        public void Show(Battle b, Action<int> onPick)
        {
            for (int i = row.childCount - 1; i >= 0; i--) Destroy(row.GetChild(i).gameObject);
            var foe = b.ActiveOf(1);
            for (int i = 0; i < b.sides[0].fighters.Count; i++)
            {
                var f = b.sides[0].fighters[i];
                if (f.dead) continue;
                int idx = i;
                var card = Ui.Spawn(cardPrefab, row);
                card.Bind(f, i, foe, () =>
                {
                    App.Audio.Play("click");
                    onPick?.Invoke(idx);
                    Close();
                });
            }
        }
    }
}
