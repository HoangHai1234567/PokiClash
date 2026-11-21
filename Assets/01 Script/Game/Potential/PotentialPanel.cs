// Tiềm năng của một tướng: nút "Tiềm năng" trong hộp chi tiết tướng mở hộp riêng để khoá ô, khai phá (PotentialDialog,
// prefab Assets/04 Prefabs/Dialogs/TiemNang) và hộp chọn "Giữ mới" / "Giữ cũ" (PotentialCompareDialog, Dialogs/TiemNangSoSanh).
// Ô chưa mở ghi "Mở ở <bậc> n sao". Kết quả khai phá chưa chọn được giữ trong bản lưu (mở lại thì hỏi tiếp).
// 2026-11-17: 6 ô, bộ (phần thưởng khi đủ dòng cùng nhóm), đá tinh (ô thưởng tô màu riêng, icon đá).
using System;
using System.Collections.Generic;
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

        // màu đá tinh (icon đá tô lam ngọc, khác đá tiềm năng và đá tiến hóa)
        public static readonly Color CrystalTint = new Color32(0x4f, 0xd8, 0xe8, 0xff);

        // ô thưởng đá tinh
        public static RewardTile CrystalTile(RewardTile t, int n) => t.Item(Icon("rock"), $"×{n}", Loc.T("Đá tinh"), Rarity.Rare, CrystalTint);

        public static string LineText(BalanceConfig cfg, PotLine x) => Potential.Text(x.k, Potential.Value(cfg, x));

        // "Máu +13%, Công +5%, Nộ đầu trận +20" (hoặc "chưa có"); gồm phần thưởng bộ
        public static string TotalsText(BalanceConfig cfg, PotLine[] lines)
        {
            var t = Potential.Final(cfg, lines);
            var parts = Potential.Kinds.Where(k => t[(int)k] > 0).Select(k => Potential.Text(k, t[(int)k])).ToList();
            return parts.Count > 0 ? string.Join(", ", parts) : Loc.T("chưa có");
        }

        // dòng bộ: "Cuồng Chiến 3/3: Công +4% · Kiên Thành 1/3"; bộ chưa có dòng nào thì bỏ
        public static string SetsText(BalanceConfig cfg, PotLine[] lines)
        {
            var parts = new List<string>();
            foreach (var set in cfg.potential.sets)
            {
                int n = Potential.SetCount(set, lines), lv = Potential.SetLevel(set, lines);
                if (n == 0) continue;
                int need = lv < set.need.Length ? set.need[lv] : set.need[set.need.Length - 1];
                var bonus = string.Join(", ", Potential.SetBonusOf(set, lv).Select(b => Potential.Text(b.k, b.v)));
                parts.Add($"{set.Name} {n}/{need}" + (lv > 0 ? $": {bonus}" : ""));
            }
            return parts.Count > 0 ? Loc.T("Bộ: ") + string.Join(" · ", parts) : Loc.T("Bộ: chưa có (3 dòng cùng nhóm thì có thưởng bộ)");
        }

        // nhóm bộ của một loại dòng ("Cuồng Chiến") hoặc rỗng
        public static string SetOf(BalanceConfig cfg, PotKind k) =>
            cfg.potential.sets.FirstOrDefault(s => Array.IndexOf(s.kinds, Potential.Key(k)) >= 0)?.Name ?? "";

        // luật bộ, một dòng mỗi bộ: "Cuồng Chiến (Công, Chí mạng, Nộ): 3 dòng Công +4%; 5 dòng Công +8%, Chí mạng +4%"
        public static string SetRules(BalanceConfig cfg) =>
            string.Join("\n", cfg.potential.sets.Select(set =>
                $"{set.Name} ({string.Join(", ", set.kinds.Where(Potential.IsKey).Select(k => Potential.ShortName(Potential.FromKey(k))))}): " +
                string.Join("; ", Enumerable.Range(1, set.need.Length).Select(lv =>
                    Loc.F("{0} dòng ", set.need[lv - 1]) + string.Join(", ", Potential.SetBonusOf(set, lv).Select(b => Potential.Text(b.k, b.v)))))));

        // chữ trong ô nhỏ: "Mở ở Bạc 1 sao", "Trống" hoặc "Máu\n+13%"
        public static string CellText(BalanceConfig cfg, PotLine x, bool on, int slot, HeroDef hero = null) =>
            !on ? Potential.SlotNeed(cfg, slot, hero)
            : x == null ? Loc.T("Trống")
            : $"{Potential.ShortName(x.k)}\n{Potential.Amount(x.k, Potential.Value(cfg, x))}";

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
