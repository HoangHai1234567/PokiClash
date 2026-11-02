// Hộp thoại dùng ở nhiều scene: "Lên cấp!" (con dấu tím, cấp mới, nút cược vừa mở, thẻ chung vừa vào bộ rút) và màn giới thiệu.
// Prefab Dialogs/LenCap, Dialogs/GioiThieu (tra trong Theme.Prefabs.dialogs).
using System;
using System.Linq;

namespace PokiClash
{
    public static class Dialogs
    {
        // Gọi sau hộp kết quả trận, sau khi mở hết rương máy bi, hoặc sau "+EXP" của bảng thử. Lên nhiều cấp thì gom hết vào một hộp.
        public static Modal LevelUp(int from, int to, Action onClose = null)
        {
            if (to <= from) return null;
            var d = App.Data;
            App.Audio.Play("level");
            var newCards = d.Pool.Where(c => c.unlock > from && c.unlock <= to).ToList();
            var newX = d.Cfg.xSteps.Where(x => x.lv > from && x.lv <= to).ToList();
            var dlg = App.Modals.Open<LevelUpDialog>(onClose);
            dlg.Show(to,
                newX.Count > 0 ? "Mở nút " + string.Join(", ", newX.Select(x => "×" + x.x)) + " ở máy bi" : null,
                newCards.Count > 0 ? "Thẻ mới vào bộ rút: " + string.Join(", ", newCards.Select(c => c.name)) : null);
            return dlg.Modal;
        }

        // Màn giới thiệu lần đầu ("Sổ Tay Phiêu Lưu", 4 ô, "Bắt đầu!"), chỉ hiện một lần.
        public static Modal Intro() => App.Modals.Open<IntroDialog>().Modal;
    }
}
