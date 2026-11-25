// Scene Bến câu của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.2; người dùng dặn 2026-11-25 "mỗi gameplay 1 scene"): scene CasinoFishing,
// prefab Screens/CasinoFishing (menu "PokiClash/Prefab/Đảo Casino/Bến câu: dựng scene"), tấm chơi là FishingPanel. Quay lại thì về đảo.
// (Trước 2026-11-25 là scene chung CasinoPlay cho mọi trò; đã tách: mỗi trò tương tác một scene riêng.)
using PokiClash.Core;
using UnityEngine;

namespace PokiClash
{
    public sealed class FishingScene : SceneRoot
    {
        [SerializeField] FishingPanel fishing;

        public override string Title => Loc.T("Bến câu");
        public override string BackTo => SceneIds.Casino;

        // Dùng khi dựng prefab (Editor).
        public void Setup(FishingPanel fish) => fishing = fish;

        public FishingPanel Fishing => fishing;

        public override void Enter(object args)
        {
            if (fishing) fishing.Open(null);
        }
    }
}
