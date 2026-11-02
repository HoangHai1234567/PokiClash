// Hộp chuẩn bị trận (chép openPrep của Web/src/view/screens/zone.ts): tên đảo và ải, nhãn MINI BOSS / BOSS ĐẢO, cảnh báo quá sức,
// đối thủ, phần thưởng, 3 ô đội hình (chạm để bỏ), kho tướng có mũi tên khắc hệ, "Xuất trận!" (xám khi đội trống).
// Dùng chung cho trận thử thách của Đền Huy Hiệu (OpenBadge) và Hang Tiềm Năng (OpenCave): đầu hộp, thưởng và đích đến khác.
// Lối vào tĩnh; hộp là prefab dùng chung Assets/04 Prefabs/Dialogs/ChuanBiTran (StagePrepDialog).
using PokiClash.Core;

namespace PokiClash
{
    public static class StagePrep
    {
        public static Modal Open(int id) => Open(App.Data.Stage(id), null);

        // trận i của bậc tier, dãy huy hiệu hệ z
        public static Modal OpenBadge(Elem z, int tier, int i) => Open(Badges.Stage(App.Data, z, tier, i), new BadgeRef { zone = z, tier = tier, i = i });

        // tầng tier của Hang Tiềm Năng, boss hệ z, ngày day
        public static Modal OpenCave(Elem z, int tier, int day) => Open(Potential.CaveStage(App.Data, z, tier), null, new CaveRef { zone = z, tier = tier, day = day });

        static Modal Open(StageDef st, BadgeRef badge, CaveRef cave = null)
        {
            var dlg = App.Modals.Open<StagePrepDialog>();
            dlg.Show(st, badge, cave);
            return dlg.Modal;
        }
    }
}
