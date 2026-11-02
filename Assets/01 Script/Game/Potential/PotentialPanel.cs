// Tiềm năng của một tướng: dải gọn trong hộp chi tiết tướng (PotentialStrip), hộp riêng để khoá ô, khai phá (PotentialDialog,
// prefab Assets/04 Prefabs/Dialogs/TiemNang) và hộp chọn "Giữ mới" / "Giữ cũ" (PotentialCompareDialog, Dialogs/TiemNangSoSanh).
// Ô chưa mở ghi "Mở ở n sao". Kết quả khai phá chưa chọn được giữ trong bản lưu (mở lại thì hỏi tiếp).
using System;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public static class PotentialPanel
    {
        public static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;
        public static Color RarityColor(int r) => Theme.Of((Rarity)r);
        public static string RarityName(int r) => Elements.RarityName((Rarity)r);

        public static string LineText(BalanceConfig cfg, PotLine x) => Potential.Text(x.k, Potential.Value(cfg, x));

        // "Máu +13%, Công +5%, Nộ đầu trận +20" (hoặc "chưa có")
        public static string TotalsText(BalanceConfig cfg, PotLine[] lines)
        {
            var t = Potential.Totals(cfg, lines);
            var parts = Potential.Kinds.Where(k => t[(int)k] > 0).Select(k => Potential.Text(k, t[(int)k])).ToList();
            return parts.Count > 0 ? string.Join(", ", parts) : "chưa có";
        }

        // chữ trong ô nhỏ của dải: "Mở ở n sao", "Trống" hoặc "Máu\n+13%"
        public static string CellText(BalanceConfig cfg, PotLine x, bool on, int slot) =>
            !on ? $"Mở ở {cfg.potential.slotStar[slot]} sao"
            : x == null ? "Trống"
            : $"{Potential.Name(x.k)}\n+{(Potential.IsPct(x.k) ? Math.Round(Potential.Value(cfg, x) * 100) + "%" : Potential.Value(cfg, x).ToString("0"))}";

        // ---------- hộp tiềm năng ----------

        // changed: gọi khi hộp đóng (hộp chi tiết tướng vẽ lại)
        public static Modal Open(string id, Action changed)
        {
            var dlg = App.Modals.Open<PotentialDialog>(changed);
            dlg.Show(id);
            return dlg.Modal;
        }
    }
}
