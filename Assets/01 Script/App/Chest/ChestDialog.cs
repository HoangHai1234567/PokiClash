// Hộp mở rương (prefab Assets/04 Prefabs/Dialogs/MoRuong): tiêu đề, rương lắc rồi bật, thưởng hiện sau khi bật:
// chip EXP / bi / đá (Items/ThuongChip), lưới thẻ mini kèm tên tướng, gộp bản sao "×n" (Items/ThuongThe), mảnh tướng (Items/ThuongManh).
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ChestDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI title;
        [SerializeField] ChestIcon chest;
        [SerializeField] GridLayoutGroup cardGrid;
        [SerializeField] RectTransform buttonRow;
        [SerializeField] SketchButton button;
        [SerializeField] RewardChipRow chipPrefab;
        [SerializeField] RewardCardCell cardPrefab;
        [SerializeField] RewardShardRow shardPrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, ChestIcon chestIcon, GridLayoutGroup grid, RectTransform row, SketchButton btn,
            RewardChipRow chipItem, RewardCardCell cardItem, RewardShardRow shardItem)
        {
            title = titleText;
            chest = chestIcon;
            cardGrid = grid;
            buttonRow = row;
            button = btn;
            chipPrefab = chipItem;
            cardPrefab = cardItem;
            shardPrefab = shardItem;
        }

        public IEnumerator Play(string titleText, SlotKind kind, Color? fill, List<Reward> rewards, string buttonLabel, Func<bool> closed)
        {
            title.text = titleText;
            var ic = chest.Bind(kind, 230, fill).Rect;
            button.SetText(buttonLabel);
            button.SetOnClick(Close);
            cardGrid.gameObject.SetActive(false);
            buttonRow.gameObject.SetActive(false);
            App.Audio.Play("whoosh");
            for (float t = 0; t < 0.65f && !closed(); t += Time.unscaledDeltaTime)
            {
                ic.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * 42) * 9 * (1 - t / 0.65f * 0.6f));
                yield return null;
            }
            if (closed()) yield break;
            ic.localEulerAngles = Vector3.zero;
            App.Audio.Play("chest");
            App.I.StartCoroutine(ChestBox.Pop(ic, 1.25f));
            Rewards(rewards);
            buttonRow.gameObject.SetActive(true);
            while (!closed()) yield return null;
        }

        // thưởng của một rương: chip EXP / bi / đá trước lưới thẻ, mảnh tướng sau lưới thẻ (trên hàng nút)
        void Rewards(List<Reward> rewards)
        {
            var d = App.Data;
            var s = App.Save.Data;
            var body = (RectTransform)cardGrid.transform.parent;
            int at = cardGrid.transform.GetSiblingIndex();
            foreach (var r in rewards.Where(q => q.k == RewardKind.Exp || q.k == RewardKind.Balls || q.k == RewardKind.Stones))
            {
                var row = Ui.Spawn(chipPrefab, body);
                row.transform.SetSiblingIndex(at++);
                string icon = r.k == RewardKind.Exp ? "exp" : r.k == RewardKind.Balls ? "ball" : "rock";
                string text = r.k == RewardKind.Exp ? $"+{r.n} XP" : r.k == RewardKind.Balls ? $"+{r.n} bi" : $"+{r.n} đá tiềm năng";
                row.Bind(App.Art.Icon(icon), text, r.k == RewardKind.Stones ? 460 : 320);
                App.I.StartCoroutine(ChestBox.Pop(row.Chip, 1.15f));
            }
            var cards = rewards.Where(q => q.k == RewardKind.Card)
                .GroupBy(q => (q.drop.hero, q.drop.slot))
                .Select(g => (drop: g.First().drop, n: g.Count()))
                .ToList();
            if (cards.Count > 0)
            {
                // hộp rộng 940, lề trong ~840: cỡ thẻ theo số thẻ khác nhau
                int nc = cards.Count;
                float k = nc <= 4 ? 0.95f : nc <= 8 ? 0.8f : nc <= 12 ? 0.58f : 0.5f;
                int perRow = nc <= 4 ? nc : nc <= 8 ? 4 : nc <= 12 ? 6 : 7;
                var cell = new Vector2(UiCard.MiniSize.x * k + 12, UiCard.MiniSize.y * k + 44);
                int rows = (cards.Count + perRow - 1) / perRow;
                cardGrid.gameObject.SetActive(true);
                cardGrid.cellSize = cell;
                cardGrid.constraintCount = perRow;
                cardGrid.GetComponent<LayoutElement>().preferredHeight = rows * cell.y + (rows - 1) * 10;
                foreach (var (drop, n) in cards)
                {
                    var cd = d.Card(drop.card);
                    var col = Ui.Spawn(cardPrefab, cardGrid.transform);
                    col.Bind(cd, s.Hero(drop.hero).Card(drop.slot).lv, App.Art.Icon(cd.icon), d.Hero(drop.hero).name, Theme.Of(drop.rarity), n, k, cell);
                    App.I.StartCoroutine(ChestBox.Pop(col.Rect, 1.12f));
                }
            }
            foreach (var r in rewards.Where(q => q.k == RewardKind.Shards))
            {
                var res = r.res;
                var h = d.Hero(res.hero);
                var row = Ui.Spawn(shardPrefab, body);
                row.transform.SetSiblingIndex(buttonRow.GetSiblingIndex());
                row.Bind(h, res.unlocked ? $"Mở khóa {h.name}!" : res.converted > 0 ? $"{h.name} +{res.n} mảnh\n(đã có tướng: thành {res.converted} bản sao thẻ)" : $"{h.name} +{res.n} mảnh");
            }
        }
    }
}
