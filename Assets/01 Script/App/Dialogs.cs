// Hộp thoại dùng ở nhiều scene: "Lên cấp!" (con dấu tím, cấp mới, thẻ chung vừa vào bộ rút) và màn giới thiệu.
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
            // nút cược máy bi mở theo số bi đang có, không theo cấp (BalanceConfig.xSteps), nên dòng "mở nút ×N" để trống
            var dlg = App.Modals.Open<LevelUpDialog>(onClose);
            dlg.Show(to, null,
                newCards.Count > 0 ? "Thẻ mới vào bộ rút: " + string.Join(", ", newCards.Select(c => c.name)) : null);
            return dlg.Modal;
        }

        // Màn giới thiệu lần đầu ("Sổ Tay Phiêu Lưu", 4 ô, "Bắt đầu!"), chỉ hiện một lần.
        public static Modal Intro(Action onClose = null) => App.Modals.Open<IntroDialog>(onClose).Modal;

        // Chọn 1 trong 5 tướng khởi đầu (bản lưu chưa có starter), bắt buộc.
        public static Modal Starter(Action<string> onPicked = null)
        {
            var dlg = App.Modals.Open<StarterDialog>(mandatory: true);
            dlg.Show(onPicked);
            return dlg.Modal;
        }
    }
}
