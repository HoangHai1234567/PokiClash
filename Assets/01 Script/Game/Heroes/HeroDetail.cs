// Hộp chi tiết tướng (chép openHero của Web/src/view/screens/heroes.ts): lối vào tĩnh, mở prefab Assets/04 Prefabs/Dialogs/ChiTietTuong
// (HeroDetailDialog: ô xem 4 clip, thông tin, chỉ số, 3 thẻ riêng, tiềm năng, tiến hóa, nút đội); tướng chưa có thì ghi mảnh và nơi rơi.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;

namespace PokiClash
{
    public static class HeroDetail
    {
        // onChange: gọi mỗi khi bản lưu đổi trong hộp (màn Tướng vẽ lại lưới)
        public static Modal Open(string id, Action onChange = null)
        {
            var dlg = App.Modals.Open<HeroDetailDialog>();
            dlg.Show(id, onChange);
            return dlg.Modal;
        }

        // "Mảnh rơi ở Đảo Kim ải 7, ải 8; ải boss đã qua còn rơi khi AFK, và đôi khi trong rương máy bi."
        public static string DropSources(GameData d, HeroDef hero)
        {
            var parts = new List<string>();
            foreach (var z in d.Zones)
            {
                var idx = d.ZoneStages(z.id).Where(st => st.drops.Any(x => x.hero == hero.id)).Select(st => $"ải {st.idx}").ToList();
                if (idx.Count > 0) parts.Add($"{z.name} {string.Join(", ", idx)}");
            }
            string legend = hero.id == d.LegendMilestoneHero ? $" Thả đủ {d.Cfg.legendMilestone} bi ở máy bi để nhận chắc chắn lần đầu." : "";
            if (parts.Count == 0) return (legend != "" ? legend.Trim() : "Mảnh rơi trong rương máy bi.");
            return $"Mảnh rơi ở {string.Join("; ", parts)}; ải boss đã qua còn rơi khi AFK, và đôi khi trong rương máy bi.{legend}";
        }
    }
}
