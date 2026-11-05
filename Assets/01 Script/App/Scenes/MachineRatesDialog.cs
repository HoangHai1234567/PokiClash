// Hộp "Tỉ lệ của máy" (nút Tỉ lệ ở Máy bi): tỉ lệ mỗi ô đo bằng mô phỏng, phần thưởng trong 3 loại rương, ghi chú.
// Prefab Assets/04 Prefabs/Dialogs/TiLeMayBi; các dòng dựng sẵn theo Rows / Chests, Show gán số theo cấu hình.
using System.Linq;
using PokiClash.Core;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class MachineRatesDialog : Dialog
    {
        // dòng tỉ lệ, theo thứ tự dựng trong prefab
        public static readonly (SlotKind k, string name)[] Rows =
        {
            (SlotKind.ChestGold, "Rương vàng (két giữa máy và ô khuất dưới két)"),
            (SlotKind.ChestSilver, "Rương bạc (2 cốc hai bên)"),
            (SlotKind.ChestWood, "Rương gỗ (2 ô mép)"),
            (SlotKind.Exp15, "EXP 15 (2 ô)"),
            (SlotKind.Exp10, "EXP 10 (2 ô cạnh ô vàng)"),
            (SlotKind.Exp5, "EXP 5 (2 ô)"),
            (SlotKind.Ball, "Hoàn 1 bi (2 ô)"),
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
            for (int i = 0; i < Rows.Length && i < rates.Length; i++) rates[i].text = Pct(cfg.Rate(Pachinko.Key(Rows[i].k)));
            for (int i = 0; i < Chests.Length && i < chests.Length; i++) chests[i].text = ChestLine(cfg, Chests[i]);
            footer.text = Footer(cfg);
        }

        public static string Intro(BalanceConfig cfg) =>
            $"Đo bằng mô phỏng {cfg.ratesBalls:#,0} bi".Replace(',', '.') + " với máng thả đung đưa đều. ×N nhân mọi thưởng, kể cả số thẻ trong rương.";

        public static string Pct(double p)
        {
            double v = p * 100;
            double r = v >= 10 ? System.Math.Round(v) : System.Math.Round(v * 2) / 2;
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
