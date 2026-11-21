// Hộp thoại dùng ở nhiều scene: "Lên cấp!" (con dấu tím, cấp mới, thẻ chung vừa vào bộ rút) và màn giới thiệu.
// Prefab Dialogs/LenCap, Dialogs/GioiThieu (tra trong Theme.Prefabs.dialogs).
using System;
using System.Linq;
using PokiClash.Core;

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
            Haptics.Play(Haptic.LevelUp);
            var newCards = d.Pool.Where(c => c.unlock > from && c.unlock <= to).ToList();
            // nút cược máy bi mở theo số bi đang có, không theo cấp (BalanceConfig.xSteps); dòng thứ hai (trước là "mở nút ×N") nay ghi
            // mọi tướng mạnh lên bao nhiêu và tính năng vừa mở theo cấp (GD_Claude/25_FTUE.md bước C4, chặng H)
            var dlg = App.Modals.Open<LevelUpDialog>(onClose);
            dlg.Show(to, Gains(d, from, to),
                newCards.Count > 0 ? Loc.T("Thẻ mới vào bộ rút: ") + string.Join(", ", newCards.Select(c => c.name)) : null);
            return dlg.Modal;
        }

        // "Mọi tướng mạnh hơn x%" và các mốc cấp vừa qua (Hang, cây bi, ô đội, tiến hóa, 30 bi mỗi lần thả)
        static string Gains(GameData d, int from, int to)
        {
            var cfg = d.Cfg;
            double pct = (Math.Pow(1 + cfg.lvStep, to - from) - 1) * 100;
            var opened = new System.Collections.Generic.List<string>();
            bool Passed(int lv) => from < lv && to >= lv;
            if (Passed(Progress.CaveLevel)) opened.Add(Loc.T("Hang Tiềm Năng"));
            foreach (var lv in cfg.trees.unlockLevels)
                if (Passed(lv))
                    opened.Add(Loc.T("thêm một cây bi"));
            for (int i = 1; i < Progress.SlotLevels.Length; i++)
                if (Passed(Progress.SlotLevels[i]))
                    opened.Add(Loc.F("ô đội thứ {0}", i + 1));
            if (cfg.evoLevel.Length > 0 && Passed(cfg.evoLevel[0])) opened.Add(Loc.T("tiến hóa lên Bạc"));
            for (int i = 1; i < cfg.evoLevel.Length; i++)
                if (Passed(cfg.evoLevel[i]))
                    opened.Add(Loc.F("tiến hóa bậc {0}", i + 1));
            if (Passed(cfg.maxPerDropLevel)) opened.Add(Loc.F("thả {0} bi mỗi đợt", cfg.maxPerDropHigh));
            string s = Loc.F("Mọi tướng mạnh hơn {0}%", Math.Max(1, (int)Math.Round(pct)));
            return opened.Count > 0 ? s + "\n" + Loc.T("Mở khoá: ") + string.Join(", ", opened) : s;
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
