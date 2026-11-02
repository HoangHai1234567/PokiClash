// Trận: thanh riêng của trận (không dùng thanh trên chung). args = BattleArgs (ải, đội) hoặc số ải.
// Nút Back của Android mở hộp tạm dừng.
// Prefab màn hình Assets/04 Prefabs/Screens/Battle: gốc mang BattleScene, BattleController, BattleView; giao diện trận dựng sẵn trong khung.
using UnityEngine;

namespace PokiClash
{
    public sealed class BattleScene : SceneRoot
    {
        public override TopBar Bar => TopBar.None;
        public override string Title => "Trận";
        public override string BackTo => SceneIds.Zone;

        [SerializeField] BattleController ctl;
        bool started;

        // Dùng khi nướng prefab (Editor).
        public void Setup(BattleController controller) => ctl = controller;

        public override void Enter(object args)
        {
            var a = args as BattleArgs ?? new BattleArgs { stageId = args is int id ? id : 1 };
            started = true;
            ctl.Begin(a);
        }

        public override void Exit()
        {
            if (started && ctl) ctl.Stop();
        }

        public override void OnBack()
        {
            if (started && ctl) ctl.Menu();
        }
    }
}
