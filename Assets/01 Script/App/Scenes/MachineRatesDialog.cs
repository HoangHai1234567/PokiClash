// Hộp "Tỉ lệ của máy" (nút Tỉ lệ ở Máy bi): tỉ lệ mỗi ô theo bảng tỉ lệ (cfg.odds), vòng hai nấm, phần thưởng trong 3 loại rương,
// ghi chú. Prefab Assets/04 Prefabs/Dialogs/TiLeMayBi (nướng 7 dòng tỉ lệ cho bàn cũ: 3 dòng đầu có icon rương kit, 4 dòng sau có
// ảnh icon): Show xếp dòng có quà là rương vào các dòng icon rương, dòng còn lại vào các dòng ảnh icon, ghi lại tên (chữ còn lại
// trong cùng dòng), số và icon; dòng thừa ẩn.
using System.Linq;
using PokiClash.Core;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class MachineRatesDialog : Dialog
    {
        // dòng tỉ lệ ô, theo thứ tự hiện
        public static readonly (SlotKind k, string name)[] Rows =
        {
            (SlotKind.ChestGold, "Rương vàng (ô khuất giữa đáy, dưới đáy V)"),
            (SlotKind.ChestSilver, "Rương bạc (cốc dưới mái)"),
            (SlotKind.Exp10, "EXP 10 (2 ô giữa)"),
            (SlotKind.Exp5, "EXP 5 (2 ô ngoài)"),
        };

        // bảng thưởng trong rương, theo thứ tự dựng trong prefab
        public static readonly SlotKind[] Chests = { SlotKind.ChestWood, SlotKind.ChestSilver, SlotKind.ChestGold };

        [SerializeField] TextMeshProUGUI intro, footer;
        [SerializeField] TextMeshProUGUI[] rates; // theo Rows
        [SerializeField] TextMeshProUGUI[] chests; // theo Chests

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI introText, TextMeshProUGUI[] rateTexts, TextMeshProUGUI[] chestTexts, TextMeshProUGUI footerText)
        {
            intro = introText;
            rates = rateTexts;
            chests = chestTexts;
            footer = footerText;
        }

        public void Show(BalanceConfig cfg)
        {
            intro.text = Intro(cfg);
            var lines = Lines(cfg);
            var chestLines = lines.Where(l => l.icon.StartsWith("chest")).ToList();
            var otherLines = lines.Where(l => !l.icon.StartsWith("chest")).ToList();
            for (int i = 0; i < rates.Length; i++)
            {
                var row = rates[i].transform.parent;
                var chest = row ? row.GetComponentInChildren<ChestIcon>(true) : null;
                var queue = chest ? chestLines : otherLines;
                bool on = queue.Count > 0;
                if (row && row != transform) row.gameObject.SetActive(on);
                else rates[i].gameObject.SetActive(on);
                if (!on) continue;
                var line = queue[0];
                queue.RemoveAt(0);
                rates[i].text = line.value;
                var name = NameOf(rates[i]);
                if (name) name.text = line.name;
                if (chest) chest.Bind(Pachinko.FromKey(line.icon), chest.Rect.sizeDelta.x);
                else
                {
                    var icon = IconOf(row, rates[i], name);
                    if (icon && App.Art) icon.sprite = App.Art.Icon(line.icon);
                }
            }
            for (int i = 0; i < Chests.Length && i < chests.Length; i++) chests[i].text = ChestLine(cfg, Chests[i]);
            footer.text = Footer(cfg);
        }

        // các dòng: tỉ lệ từng loại ô, rồi vòng hai nấm (trái, phải); icon: khoá rương (chest_*) hoặc tên icon (exp, ball)
        public static System.Collections.Generic.List<(string name, string value, string icon)> Lines(BalanceConfig cfg)
        {
            var list = Rows.Select(r => (r.name, Pct(cfg.Rate(Pachinko.Key(r.k))), Pachinko.IsChest(r.k) ? Pachinko.Key(r.k) : "exp")).ToList();
            for (int i = 0; i < cfg.rings.Count; i++)
            {
                var g = cfg.rings[i];
                string side = i == 0 ? "Nấm trái" : "Nấm phải";
                double hits = i < cfg.ringHits.Length ? cfg.ringHits[i] : 0;
                list.Add(($"{side}: đủ {g.n} lần chạm ra {Pachinko.GiftName(g)}", hits > 0 ? $"≈ {Num(hits)} lần/bi" : "",
                    g.k.StartsWith("chest") ? g.k : g.k == "balls" ? "ball" : "exp"));
            }
            return list;
        }

        // ảnh icon đầu dòng: ảnh con có hình, không phải chữ của dòng
        static UnityEngine.UI.Image IconOf(Transform row, TextMeshProUGUI value, TextMeshProUGUI name)
        {
            if (!row) return null;
            foreach (var img in row.GetComponentsInChildren<UnityEngine.UI.Image>(true))
                if (img.transform != row && img.sprite && (!name || img.transform != name.transform) && img.transform != value.transform) return img;
            return null;
        }

        // chữ tên dòng: chữ còn lại trong cùng dòng với ô số
        static TextMeshProUGUI NameOf(TextMeshProUGUI value)
        {
            var row = value.transform.parent;
            if (!row) return null;
            foreach (var t in row.GetComponentsInChildren<TextMeshProUGUI>(true))
                if (t != value) return t;
            return null;
        }

        static string Num(double v) => v.ToString("0.#").Replace('.', ',');

        public static string Intro(BalanceConfig cfg) =>
            "Mỗi lần thả, máy chọn ô theo bảng dưới rồi phóng bi theo một đường vật lý rơi đúng ô đó. " +
            "×N nhân mọi thưởng, kể cả số thẻ trong rương; vòng nấm cộng N nấc mỗi lần chạm.";

        public static string Pct(double p)
        {
            double v = p * 100;
            double r = v >= 10 ? System.Math.Round(v) : System.Math.Round(v, 1);
            return "≈ " + r.ToString("0.#").Replace('.', ',') + " %";
        }

        public static string ChestLine(BalanceConfig cfg, SlotKind k)
        {
            var tb = cfg.Chest(Pachinko.Key(k));
            double tot = tb.rolls.Sum(q => q.w);
            var parts = tb.rolls.Select(q =>
            {
                string what = q.k == "balls" ? "bi" : q.k == "exp" ? "EXP" : q.k == "cards" ? "thẻ" : q.k == "stones" ? "đá tiềm năng" : "mảnh tướng";
                string range = q.max > q.min ? $"{q.min}–{q.max}" : q.min.ToString();
                string rar = q.rar.Count > 0
                    ? " (" + string.Join(", ", q.rar.Select(rw => $"{Elements.RarityName(rw.rarity)} {rw.w.ToString("0.##").Replace('.', ',')}")) + ")"
                    : "";
                return $"{System.Math.Round(q.w / tot * 100)}% {what} {range}{rar}";
            });
            return $"<b>{Pachinko.ChestName(k)}:</b> " + string.Join("; ", parts);
        }

        public static string Footer(BalanceConfig cfg) =>
            "Thẻ trong rương là bản sao thẻ nội tại của tướng bạn đã có, mỗi thẻ rút riêng. Thẻ Huyền thoại trong Rương vàng: 0,01 % mỗi thẻ. " +
            $"Mảnh tướng lấy từ boss đã gặp. Thả đủ {cfg.legendMilestone} bi: chắc chắn ra tướng Huyền thoại đầu tiên." +
            (cfg.gifts.Count > 0
                ? " Sau đó là mốc quà, tính theo số bi đã thả (cược ×N tính N bi), hết thì vòng lại: " +
                  string.Join(", ", cfg.gifts.Select(g => $"{g.n} bi {Pachinko.GiftName(g)}")) + "."
                : "") +
            " Nút cược mở theo số bi đang có: " + string.Join(", ", cfg.xSteps.Where(q => q.balls > 0).Select(q => $"×{q.x} từ {q.balls} bi")) + ".";
    }
}
