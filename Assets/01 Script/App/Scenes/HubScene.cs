// Sảnh (chép worldScreen của Web/src/view/screens/world.ts): đảo lớn chia 5 vùng hệ, làng máy bi ở giữa.
// Không khoá vùng nào: bảng tên ghi cấp đề nghị, độ khó so với cấp người chơi, tiến độ. Mũi tên nhún chỉ đảo nên đánh.
// Rìa làng có chỗ cho công trình side meta (phác chì khi chưa mở). Hàng nút tròn ở đáy. Lần đầu hiện màn giới thiệu.
// Prefab màn hình Assets/04 Prefabs/Screens/Hub: vùng đảo (Items/BangVung) và công trình (Items/CongTrinh) đặt sẵn theo toạ độ ảnh.
using System;
using System.Collections;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HubScene : SceneRoot
    {
        public override TopBar Bar => TopBar.Hud;
        public override string Title => "Sảnh";

        // công trình side meta theo thứ tự đặt trên sảnh: tên, icon, điều kiện mở, lệch so với làng (toạ độ ảnh)
        public static readonly (string name, string icon, string need, float dx, float dy)[] Buildings =
        {
            ("Trang trại", "seed", "Có 3 tướng để mở Trang trại", -0.27f, 0.035f),
            ("Đền Huy Hiệu", "crown", "Thắng boss Đảo Thủy để mở Đền Huy Hiệu", 0.27f, 0.035f),
            ("Hang Tiềm Năng", "rock", "Thắng mini boss Đảo Hỏa để mở Hang Tiềm Năng", 0f, 0.155f),
            ("Cây bi", "leaf", "Qua ải 1 để có cây bi đầu tiên", -0.27f, 0.155f),
        };

        // một nút tròn ở hàng đáy; chấm đỏ số (nếu có) bật theo dữ liệu
        [Serializable]
        public struct BottomButton
        {
            public SketchButton button;
            public RectTransform badge;
            public TextMeshProUGUI badgeText;
        }

        [SerializeField] RectTransform[] clouds;
        [SerializeField] HubZone[] zones;
        [SerializeField] ClickCatcher village;
        [SerializeField] TextMeshProUGUI villageBalls;
        [SerializeField] HubBuilding[] buildings; // theo thứ tự Buildings
        [SerializeField] BottomButton[] bottom; // Tướng, Sổ thẻ, Máy Bi, Đánh tiếp, Sổ tay

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform[] cloudRts, HubZone[] zoneItems, ClickCatcher villageClick, TextMeshProUGUI villageText,
            HubBuilding[] buildingItems, BottomButton[] bottomButtons)
        {
            clouds = cloudRts;
            zones = zoneItems;
            village = villageClick;
            villageBalls = villageText;
            buildings = buildingItems;
            bottom = bottomButtons;
        }

        public override void Enter(object args)
        {
            Render();
            if (!App.Save.Data.intro) StartCoroutine(IntroLater());
        }

        public override void Refresh() => Render();

        IEnumerator IntroLater()
        {
            yield return new WaitForSecondsRealtime(0.5f);
            Dialogs.Intro();
        }

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        void Render()
        {
            if (zones == null || !village) return; // chưa nướng prefab màn hình
            var d = App.Data;
            var s = App.Save.Data;
            var recoZone = Progress.RecommendedZone(s, d);
            foreach (var item in zones)
            {
                var z = d.Zone(item.Zone);
                item.gameObject.SetActive(z != null);
                if (z == null) continue;
                int prog = s.zones[(int)z.id];
                item.Bind(z, prog, Progress.DifficultyOf(z, s.level, prog >= 8), z == recoZone);
                item.SetOnClick(() =>
                {
                    App.Audio.Play("click");
                    App.Router.Go(SceneIds.Zone, z.id);
                });
            }
            villageBalls.text = $"{s.balls} bi đang có";
            village.OnClick = () =>
            {
                App.Audio.Play("click");
                App.Router.Go(SceneIds.Machine);
            };
            SideMeta(s);
            BottomRow(s, recoZone);
        }

        // công trình side meta ở rìa làng: hiện khi mở, trước đó phác chì kèm điều kiện mở
        void SideMeta(SaveData s)
        {
            var d = App.Data;
            for (int i = 0; i < buildings.Length && i < Buildings.Length; i++)
            {
                var item = Buildings[i];
                bool temple = item.icon == "crown", cave = item.icon == "rock", farm = item.icon == "seed", tree = item.icon == "leaf";
                bool open = farm ? Farm.Open(s, d.Cfg) : temple ? Progress.BadgesOpen(s) : cave ? Progress.CaveOpen(s) : tree && Trees.Open(s, d.Cfg) > 0;
                double now = PokiClash.Game.SaveService.Now();
                // chấm báo: có dãy huy hiệu vừa mở, chưa đánh trận nào; trang trại cần chăm; cây bi đầy
                bool alert = (temple && open && Badges.HasNew(s, d)) || (farm && open && Farm.Alert(s, d, now)) || (tree && open && Trees.Full(s, d.Cfg, now));
                buildings[i].Bind(item.name, open, alert, () =>
                {
                    if (tree && open)
                    {
                        App.Audio.Play("click");
                        TreePanel.Open();
                        return;
                    }
                    if ((temple || cave || farm) && open)
                    {
                        App.Audio.Play("click");
                        App.Router.Go(temple ? SceneIds.Badges : cave ? SceneIds.Cave : SceneIds.Farm);
                        return;
                    }
                    App.Audio.Play(open ? "click" : "error");
                    App.Toasts.Show(open ? $"{item.name}: sắp có ở bản sau" : item.need, Icon(open ? "info" : "lock"));
                });
            }
        }

        // hàng nút tròn: Tướng (số việc chờ), Sổ thẻ, Máy Bi (to, số bi), Đánh tiếp, Sổ tay
        void BottomRow(SaveData s, ZoneDef recoZone)
        {
            var d = App.Data;
            MainButton(0, () => App.Router.Go(SceneIds.Heroes), Progress.HeroAlerts(s, d));
            MainButton(1, () => App.Router.Go(SceneIds.Cards));
            MainButton(2, () => App.Router.Go(SceneIds.Machine), s.balls);
            MainButton(3, () => App.Router.Go(SceneIds.Zone, recoZone.id));
            MainButton(4, () => App.Router.Go(SceneIds.Notebook));
        }

        void MainButton(int i, Action go, int dot = 0)
        {
            if (bottom == null || i >= bottom.Length) return;
            var b = bottom[i];
            b.button.SetOnClick(go);
            if (!b.badge) return;
            b.badge.gameObject.SetActive(dot > 0);
            if (dot <= 0) return;
            string txt = dot > 99 ? "99+" : dot.ToString();
            b.badge.sizeDelta = new Vector2(Mathf.Max(52, 22 * txt.Length + 26), 50);
            b.badgeText.text = txt;
        }

        void Update()
        {
            if (clouds == null) return;
            // mây trôi
            float w = PokiCanvas.RefW + 520;
            for (int i = 0; i < clouds.Length; i++)
            {
                if (!clouds[i]) continue;
                float period = 70 + i * 25;
                float k = Mathf.Repeat(Time.unscaledTime / period + i * 0.33f, 1f);
                clouds[i].anchoredPosition = new Vector2(-260 + k * w, -(260 + i * 500));
            }
        }
    }
}
