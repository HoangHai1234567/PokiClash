// Hộp mở rương (prefab Assets/04 Prefabs/Dialogs/MoRuong): tiêu đề, rương lắc rồi bật, thưởng hiện sau khi bật thành lưới ô hình
// (Items/OThuong, menu "PokiClash/Prefab/Hộp thoại và màn/Popup gọn (ô thưởng, đội hình, lực chiến)" gán): XP / bi / đá tiềm năng / đá tiến hóa, thẻ gộp
// bản sao "×n", mảnh tướng.
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

        // ô thưởng của một danh sách thưởng (dùng chung với màn mở nhiều rương MachineChestOpen): XP, bi, đá tiềm năng, đá tiến hóa
        // trước, rồi thẻ (gộp bản sao "×n"), rồi mảnh tướng
        public static List<RewardTile> BuildTiles(List<Reward> rewards, RewardTile prefab, Transform parent)
        {
            var d = App.Data;
            var tiles = new List<RewardTile>();
            RewardTile Tile() { var t = Ui.Spawn(prefab, parent); tiles.Add(t); return t; }
            int exp = rewards.Where(q => q.k == RewardKind.Exp).Sum(q => q.n);
            int balls = rewards.Where(q => q.k == RewardKind.Balls).Sum(q => q.n);
            int stones = rewards.Where(q => q.k == RewardKind.Stones).Sum(q => q.n);
            int evo = rewards.Where(q => q.k == RewardKind.EvoStones).Sum(q => q.n);
            if (exp > 0) Tile().Item(App.Art.Icon("exp"), $"×{exp}", "XP");
            if (balls > 0) Tile().Item(App.Art.Icon("ball"), $"×{balls}", Loc.T("Bi"));
            if (stones > 0) Tile().Item(App.Art.Icon("rock"), $"×{stones}", Loc.T("Đá tiềm năng"), Rarity.Epic);
            if (evo > 0) Tile().EvoStones(evo);
            // cửa hàng (Shop, 2026-11-23): đá tinh, trứng vào túi, vé chọn tướng, quyền lợi
            int crystal = rewards.Where(q => q.k == RewardKind.Crystal).Sum(q => q.n);
            if (crystal > 0) ShopUi.Tile(Tile(), new ShopItem { k = "crystal", n = crystal });
            // trứng vào túi: ô màu bậc, nhãn "nở mảnh"
            foreach (var g in rewards.Where(q => q.k == RewardKind.Egg).GroupBy(q => q.id))
                ShopUi.Tile(Tile(), new ShopItem { k = Shop.Egg, r = Eggs.TierOf(g.Key), n = g.Sum(q => q.n) });
            foreach (var g in rewards.Where(q => q.k == RewardKind.HeroChest || q.k == RewardKind.GoldChest || q.k == RewardKind.Ticket || q.k == RewardKind.Perk)
                         .GroupBy(q => (q.k, q.id)))
            {
                var r = g.First();
                string k = r.k == RewardKind.HeroChest ? Shop.HeroChest : r.k == RewardKind.GoldChest ? Shop.GoldChest
                    : r.k == RewardKind.Ticket ? r.id ?? Shop.Ticket : r.id == "week" ? "week_card" : r.id == "month" ? "month_card" : r.id ?? "no_ads";
                if (r.k == RewardKind.Perk && r.id == "fund") Tile().Item(App.Art.Icon("crown"), "", Loc.T("Quỹ Phiêu Lưu"), Rarity.Epic);
                else ShopUi.Tile(Tile(), new ShopItem { k = k, n = g.Sum(q => q.n) });
            }
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
                if (res.unlocked) t.Tag(Loc.T("MỞ KHÓA!"), Theme.Red);
                else if (res.converted > 0) t.Tag(Loc.F("→ {0} thẻ", res.converted), Theme.Paper2);
                else
                {
                    // tiến độ mảnh: mở khoá (chưa có) hoặc lên sao kế (đã có; 2026-11-17 mảnh dồn để lên sao)
                    var g = Progress.ShardGoal(App.Save.Data, d, res.hero);
                    if (g.need > 0) t.Tag($"{g.have}/{g.need}", g.have >= g.need ? Theme.Yellow : Theme.Paper2);
                }
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
            bool gold = kind == SlotKind.ChestGold, silver = kind == SlotKind.ChestSilver;
            // rương có rig AtomSpine (ảnh gen, không tô màu riêng; người dùng 2026-11-27: rương AFK vẽ tạm "xấu"): nhắc (nhún, nắp hé),
            // gồng (rig tự lắc, nén, sáng lọt khe; code lắc thêm nửa biên độ), bật nắp rồi lòng sáng, như màn mở rương máy bi
            bool rigged = chest.PlayRig("nhac");
            if (rigged)
            {
                for (float t = 0; t < 0.45f && !closed(); t += Time.unscaledDeltaTime) yield return null;
                float gong = gold ? 0.6f : silver ? 0.45f : 0.36f;
                chest.PlayRig("gong", false);
                chest.Rig.speed = 0.6f / gong;
                for (float t = 0; t < gong && !closed(); t += Time.unscaledDeltaTime)
                {
                    float k = t / gong;
                    ic.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * (gold ? 48 : 42)) * (3 + 4 * k));
                    yield return null;
                }
                if (closed()) yield break;
                ic.localEulerAngles = Vector3.zero;
                chest.Rig.speed = 1;
                chest.PlayRig("bat", false);
                chest.Rig.Queue("mo", true);
                App.Audio.Play("chestOpen");
            }
            else
            {
                // hồi hộp theo độ quý: gỗ lắc 0,65 giây nhỏ dần; bạc 0,85 giây; vàng 1,1 giây lắc mạnh dần rồi mới bật
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
            }
            Haptics.Play(gold ? Haptic.OpenGold : silver ? Haptic.OpenSilver : Haptic.OpenWood);
            if (!rigged) App.I.StartCoroutine(ChestBox.Pop(ic, 1.25f)); // rig: clip bật nắp đã bóp giãn sẵn
            Rewards(rewards);
            buttonRow.gameObject.SetActive(true);
            while (!closed()) yield return null;
        }

        // thưởng của một rương: mọi thứ là ô hình (Items/OThuong) trong một lưới: XP, bi, đá trước, rồi thẻ (gộp bản sao "×n"),
        // rồi mảnh tướng (MỞ KHÓA! khi đủ mảnh, tiến độ "có/cần" mảnh mở khoá hoặc lên sao, "→ n thẻ" khi tướng đã tối đa sao và mảnh
        // đổi thành bản sao thẻ). Ô bật lần lượt.
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
