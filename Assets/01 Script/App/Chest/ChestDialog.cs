// Hộp mở rương (prefab Assets/04 Prefabs/Dialogs/MoRuong): tiêu đề, rương lắc rồi bật, thưởng hiện sau khi bật thành lưới ô hình
// (Items/OThuong, menu "PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)" gán): XP / bi / đá, thẻ gộp bản sao "×n", mảnh tướng.
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
        [SerializeField] RewardTile tilePrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, ChestIcon chestIcon, GridLayoutGroup grid, RectTransform row, SketchButton btn, RewardTile tile)
        {
            title = titleText;
            chest = chestIcon;
            cardGrid = grid;
            buttonRow = row;
            button = btn;
            tilePrefab = tile;
        }

        public RewardTile TilePrefab => tilePrefab;

        // ô thưởng của một danh sách thưởng (dùng chung với màn mở nhiều rương MachineChestOpen): XP, bi, đá trước, rồi thẻ (gộp
        // bản sao "×n"), rồi mảnh tướng
        public static List<RewardTile> BuildTiles(List<Reward> rewards, RewardTile prefab, Transform parent)
        {
            var d = App.Data;
            var tiles = new List<RewardTile>();
            RewardTile Tile() { var t = Ui.Spawn(prefab, parent); tiles.Add(t); return t; }
            int exp = rewards.Where(q => q.k == RewardKind.Exp).Sum(q => q.n);
            int balls = rewards.Where(q => q.k == RewardKind.Balls).Sum(q => q.n);
            int stones = rewards.Where(q => q.k == RewardKind.Stones).Sum(q => q.n);
            if (exp > 0) Tile().Item(App.Art.Icon("exp"), $"×{exp}", "XP");
            if (balls > 0) Tile().Item(App.Art.Icon("ball"), $"×{balls}", "Bi");
            if (stones > 0) Tile().Item(App.Art.Icon("rock"), $"×{stones}", "Đá tiềm năng", Rarity.Epic);
            var cards = rewards.Where(q => q.k == RewardKind.Card)
                .GroupBy(q => (q.drop.hero, q.drop.slot))
                .Select(g => (drop: g.First().drop, n: g.Count()))
                .ToList();
            foreach (var (drop, n) in cards)
            {
                var cd = d.Card(drop.card);
                Tile().Card(cd, App.Art.Icon(cd.icon), d.Hero(drop.hero), n, drop.rarity);
            }
            foreach (var r in rewards.Where(q => q.k == RewardKind.Shards))
            {
                var res = r.res;
                var t = Tile().Hero(d.Hero(res.hero), $"×{res.n}");
                if (res.unlocked) t.Tag("MỞ KHÓA!", Theme.Red);
                else if (res.converted > 0) t.Tag($"→ {res.converted} thẻ", Theme.Paper2);
            }
            return tiles;
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
            // hồi hộp theo độ quý: gỗ lắc 0,65 giây nhỏ dần; bạc 0,85 giây; vàng 1,1 giây lắc mạnh dần rồi mới bật
            bool gold = kind == SlotKind.ChestGold, silver = kind == SlotKind.ChestSilver;
            float shake = gold ? 1.1f : silver ? 0.85f : 0.65f;
            for (float t = 0; t < shake && !closed(); t += Time.unscaledDeltaTime)
            {
                float k = t / shake;
                float amp = gold ? 6 + 8 * k : 9 * (1 - k * 0.6f);
                ic.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * (gold ? 48 : 42)) * amp);
                yield return null;
            }
            if (closed()) yield break;
            ic.localEulerAngles = Vector3.zero;
            chest.Open(); // ảnh rương mở (nếu có ảnh gen)
            App.Audio.Play("chest");
            Haptics.Play(gold ? Haptic.OpenGold : silver ? Haptic.OpenSilver : Haptic.OpenWood);
            App.I.StartCoroutine(ChestBox.Pop(ic, 1.25f));
            Rewards(rewards);
            buttonRow.gameObject.SetActive(true);
            while (!closed()) yield return null;
        }

        // thưởng của một rương: mọi thứ là ô hình (Items/OThuong) trong một lưới: XP, bi, đá trước, rồi thẻ (gộp bản sao "×n"),
        // rồi mảnh tướng (MỞ KHÓA! khi đủ mảnh, "→ n thẻ" khi tướng đã có và mảnh đổi thành bản sao thẻ). Ô bật lần lượt.
        void Rewards(List<Reward> rewards)
        {
            var tiles = BuildTiles(rewards, tilePrefab, cardGrid.transform);
            if (tiles.Count == 0) return;

            // hộp rộng 940, lề trong ~840: tới 5 ô một hàng
            int perRow = Mathf.Min(5, tiles.Count), rows = (tiles.Count + perRow - 1) / perRow;
            cardGrid.gameObject.SetActive(true);
            cardGrid.cellSize = new Vector2(RewardTile.W, RewardTile.H);
            cardGrid.spacing = new Vector2(18, 28); // chừa chỗ nhãn ô hàng dưới
            cardGrid.constraintCount = perRow;
            cardGrid.GetComponent<LayoutElement>().preferredHeight = rows * RewardTile.H + (rows - 1) * 28 + 16;
            for (int i = 0; i < tiles.Count; i++) App.I.StartCoroutine(PopLater(tiles[i].Rect, i * 0.07f));
        }

        static IEnumerator PopLater(RectTransform rt, float delay)
        {
            rt.localScale = Vector3.zero;
            yield return new WaitForSecondsRealtime(delay);
            if (rt) yield return ChestBox.Pop(rt, 1.15f);
        }
    }
}
