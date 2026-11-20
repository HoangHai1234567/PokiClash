// Sảnh (chép worldScreen của Web/src/view/screens/world.ts): đảo lớn chia 5 vùng hệ, làng máy bi ở giữa.
// Bản đồ thế giới (người dùng 2026-11-19, ArtGen/Islands/sanh_moi): năm đảo liền nhau có địa hình cao thấp, kéo được 4 hướng, vành mây
// che miền chưa mở; không còn làng máy bi trên đảo, công trình side meta ra cột nút cố định. Mây che từng đảo (HubFog): mới chơi che
// hết, chọn tướng khởi đầu thì tan đảo cùng hệ, xong trận hướng dẫn (tạm: thắng ải đầu) thì tan nốt (HubIslands). Mỗi đảo mới mở
// diễn tan mây một lần, khoá chạm trong lúc diễn, camera lướt tới đảo đó.
// Không khoá vùng nào: bảng tên ghi cấp đề nghị, độ khó so với cấp người chơi, tiến độ. Mũi tên nhún chỉ đảo nên đánh.
// Rìa làng có chỗ cho công trình side meta (phác chì khi chưa mở). Hàng nút tròn ở đáy. Lần đầu hiện màn giới thiệu.
// Prefab màn hình Assets/04 Prefabs/Screens/Hub: vùng đảo (Items/BangVung) và công trình (Items/CongTrinh) đặt sẵn theo toạ độ ảnh.
// Ảnh đảo ghép từ đảo gen rời (ArtGen/Islands/compose_islands.py), kéo được (HubPan), ra rìa là vành mây; dựng bằng menu
// "PokiClash/Prefab/Đảo sảnh: ghép ảnh, kéo, mây viền".
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
            ("Nhà", "seed", "Có 3 tướng để mở Nhà", -0.27f, 0.035f), // Nhà thay Trang trại (2026-11-18), icon giữ "seed"
            ("Đền Huy Hiệu", "crown", "Thắng mini boss đầu tiên ở một đảo bất kỳ để mở Đền Huy Hiệu", 0.27f, 0.035f),
            ("Hang Tiềm Năng", "rock", $"Đạt cấp {Progress.CaveLevel} để mở Hang Tiềm Năng", 0f, 0.155f),
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
        [Tooltip("Mây che từng đảo của bản đồ thế giới (menu PokiClash/Prefab/Sảnh bản đồ thế giới)")]
        [SerializeField] HubFog fog;
        [SerializeField] HubPan pan;
        [Tooltip("Tàu ở bến cạnh đảo Thủy (menu PokiClash/Prefab/Bến tàu: ...)")]
        [SerializeField] PierShip pier;
        [Tooltip("Ảnh từng đảo trên bản đồ: bấm theo hình đảo, nhún, đèn đêm của đảo (HubIslandArt)")]
        [SerializeField] HubIslandArt[] islandArts = new HubIslandArt[0];
        [Tooltip("Giao diện cố định (hàng nút đáy, cột thẻ công trình): ẩn lúc chuyến tàu qua mây")]
        [SerializeField] CanvasGroup[] chrome = new CanvasGroup[0];
        Coroutine chromeFade;

        Coroutine reveal;

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

        // Dùng khi dựng prefab (Editor): bản đồ thế giới.
        public void SetupMap(HubFog fogLayer, HubPan panLayer)
        {
            fog = fogLayer;
            pan = panLayer;
        }

        public void SetupIslands(HubIslandArt[] arts) => islandArts = arts;

        public void SetupPier(PierShip p, CanvasGroup[] chromeGroups)
        {
            pier = p;
            chrome = chromeGroups;
        }

        public override void Chrome(bool on, bool fade)
        {
            if (chromeFade != null) StopCoroutine(chromeFade);
            chromeFade = null;
            if (fade && isActiveAndEnabled) chromeFade = StartCoroutine(FadeChrome(on));
            else
                foreach (var g in chrome)
                    if (g)
                    {
                        g.alpha = on ? 1 : 0;
                        g.blocksRaycasts = on;
                    }
        }

        IEnumerator FadeChrome(bool on)
        {
            foreach (var g in chrome)
                if (g) g.blocksRaycasts = on;
            float from = chrome.Length > 0 && chrome[0] ? chrome[0].alpha : 0, to = on ? 1 : 0;
            for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
            {
                foreach (var g in chrome)
                    if (g) g.alpha = Mathf.Lerp(from, to, t / 0.25f);
                yield return null;
            }
            foreach (var g in chrome)
                if (g) g.alpha = to;
            chromeFade = null;
        }

        // bến tàu: camera cho chuyến tàu qua mây (đặt ngay / lướt tới tàu), chạm tàu là về Nhà
        void HookPier()
        {
            if (!pier) return;
            pier.Frame = (p, w) =>
            {
                if (pan) pan.FrameAt(p, w);
            };
            pier.Glide = GlideTo;
            pier.OnTap = () =>
            {
                var s = App.Save.Data;
                if (Home.Open(s, App.Data.Cfg))
                {
                    App.Audio.Play("click");
                    App.Router.Go(SceneIds.Home);
                }
                else
                {
                    App.Audio.Play("error");
                    var farm = System.Array.Find(Buildings, b => b.icon == "seed");
                    App.Toasts.Show(farm.need ?? "Nhà chưa mở", Icon("lock"));
                }
            };
        }

        IEnumerator GlideTo(RectTransform p)
        {
            if (!pan) yield break;
            pan.GlideTo(p);
            float t0 = Time.unscaledTime;
            while (pan.Gliding && Time.unscaledTime - t0 < 1f) yield return null;
        }

        public override void Enter(object args)
        {
            HookPier();
            Chrome(true, false);
            Render();
            var start = StartFocus();
            if (pan && start) pan.GlideTo(start);
            if (!App.Save.Data.intro || App.Save.Data.starter == null) StartCoroutine(IntroLater());
        }

        public override void Refresh() => Render();

        // người chơi mới: màn giới thiệu, rồi chọn tướng khởi đầu (bản lưu chưa có starter thì mở hộp chọn mỗi lần vào sảnh)
        IEnumerator IntroLater()
        {
            while (App.Booting) yield return null; // màn mở game còn che sảnh
            yield return new WaitForSecondsRealtime(0.5f);
            void PickStarter()
            {
                if (App.Save.Data.starter == null) Dialogs.Starter(_ => Render());
            }
            if (!App.Save.Data.intro) Dialogs.Intro(PickStarter);
            else PickStarter();
        }

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        void Render()
        {
            if (zones == null) return; // chưa nướng prefab màn hình
            var d = App.Data;
            var s = App.Save.Data;
            int open = HubIslands.Open(s, d);
            var recoZone = RecoZone(s, d, open);
            foreach (var item in zones)
            {
                var z = d.Zone(item.Zone);
                item.gameObject.SetActive(z != null);
                if (z == null) continue;
                int prog = s.zones[(int)z.id];
                item.Bind(z, prog, Progress.NextLevel(s, d, z.id), Progress.DifficultyOf(s, d, z), z == recoZone && open != 0);
                Action go = () =>
                {
                    App.Audio.Play("click");
                    App.Router.Go(SceneIds.Zone, z.id);
                };
                item.SetOnClick(go);
                // bấm vào hình đảo cũng vào đảo (đảo nhún nhẹ); đảo chưa mở (mây che) thì không sáng, không nhận bấm
                foreach (var art in islandArts)
                    if (art && art.Zone == z.id)
                    {
                        art.OnClick = go;
                        art.SetOpen((open & HubIslands.Bit(z.id)) != 0);
                    }
            }
            if (villageBalls) villageBalls.text = $"{s.balls} bi đang có";
            if (village)
                village.OnClick = () =>
                {
                    App.Audio.Play("click");
                    App.Router.Go(SceneIds.Machine);
                };
            SideMeta(s);
            BottomRow(s, recoZone);
            Fog(s, d, open);
        }

        // đảo nên đánh: chưa mở hết thì là đảo đã mở (đảo của tướng khởi đầu)
        static ZoneDef RecoZone(SaveData s, GameData d, int open)
        {
            var reco = Progress.RecommendedZone(s, d);
            if (open == HubIslands.All || open == 0 || (open & HubIslands.Bit(reco.id)) != 0) return reco;
            foreach (var e in Elements.All)
                if ((open & HubIslands.Bit(e)) != 0 && d.Zone(e) != null)
                    return d.Zone(e);
            return reco;
        }

        // chỗ nhìn lúc vào sảnh: đảo vừa mở (sắp diễn tan mây), không thì đảo nên đánh
        RectTransform StartFocus()
        {
            if (!fog) return null;
            var s = App.Save.Data;
            var d = App.Data;
            int open = HubIslands.Open(s, d), fresh = open & ~HubIslands.Shown(s);
            if (fresh != 0 && fresh != HubIslands.All)
                foreach (var e in Elements.All)
                    if ((fresh & HubIslands.Bit(e)) != 0)
                        return fog.Center(e);
            if (fresh == HubIslands.All || open == 0) return null; // mở cả bản đồ / chưa mở gì: nhìn toàn cảnh từ giữa
            return fog.Center(RecoZone(s, d, open).id);
        }

        // mây che các đảo chưa mở; đảo mới mở mà chưa diễn thì diễn tan mây
        void Fog(SaveData s, GameData d, int open)
        {
            if (!fog || reveal != null) return; // đang diễn tan mây: không dựng lại mây giữa chừng
            int shown = HubIslands.Shown(s) & open;
            int fresh = open & ~shown;
            fog.Apply(HubIslands.All & ~shown, LockedTap);
            if (fresh != 0 && reveal == null) reveal = StartCoroutine(Reveal(fresh));
        }

        void LockedTap(Elem e)
        {
            App.Audio.Play("error");
            var s = App.Save.Data;
            string msg = string.IsNullOrEmpty(s.starter)
                ? "Chọn bạn đồng hành để mở đảo đầu tiên"
                : $"{App.Data.Zone(e)?.name ?? "Đảo"}: hoàn thành trận đầu tiên để mở";
            App.Toasts.Show(msg, Icon("lock"));
        }

        IEnumerator Reveal(int fresh)
        {
            // chờ màn chuyển xong, hộp thoại (chọn tướng khởi đầu) đóng
            while (App.Booting || App.Router.Busy || (App.Modals != null && App.Modals.Count > 0)) yield return null;
            var cover = FindAnyObjectByType<CloudCover>(FindObjectsInactive.Include);
            if (cover) cover.Block(true);
            yield return new WaitForSecondsRealtime(0.35f);
            int n = 0;
            foreach (var e in Elements.All)
                if ((fresh & HubIslands.Bit(e)) != 0)
                    n++;
            if (n == 1)
            {
                foreach (var e in Elements.All)
                    if ((fresh & HubIslands.Bit(e)) != 0)
                    {
                        if (pan && fog.Center(e)) pan.GlideTo(fog.Center(e));
                        float t0 = Time.unscaledTime;
                        while (pan && pan.Gliding && Time.unscaledTime - t0 < 1.5f) yield return null;
                        yield return fog.Reveal(e);
                    }
            }
            else
            {
                // mở nhiều đảo một lúc: lần lượt tan từng đảo, cách nhau một nhịp ngắn, camera giữ toàn cảnh
                Coroutine last = null;
                foreach (var e in Elements.All)
                    if ((fresh & HubIslands.Bit(e)) != 0)
                    {
                        last = StartCoroutine(fog.Reveal(e));
                        yield return new WaitForSecondsRealtime(0.45f);
                    }
                if (last != null) yield return last;
            }
            HubIslands.SetShown(App.Save.Data, HubIslands.Shown(App.Save.Data) | fresh);
            // lưu ngay (người dùng 2026-11-20: "mây chỉ che toàn bộ đảo lần đầu tiên thôi, từ các lần sau boot vào là mây không che nữa"):
            // trước đây chờ lần lưu kế tiếp, tắt game trước đó thì lần boot sau mây che lại, diễn tan lại
            App.Save.Save();
            if (cover) cover.Block(false);
            reveal = null;
        }

        void OnDisable()
        {
            if (reveal == null) return;
            StopCoroutine(reveal);
            reveal = null;
            var cover = FindAnyObjectByType<CloudCover>(FindObjectsInactive.Include);
            if (cover) cover.Block(false);
        }

        // công trình side meta ở rìa làng: hiện khi mở, trước đó phác chì kèm điều kiện mở
        void SideMeta(SaveData s)
        {
            var d = App.Data;
            for (int i = 0; i < buildings.Length && i < Buildings.Length; i++)
            {
                var item = Buildings[i];
                bool temple = item.icon == "crown", cave = item.icon == "rock", farm = item.icon == "seed", tree = item.icon == "leaf";
                bool open = farm ? Home.Open(s, d.Cfg) : temple ? Progress.BadgesOpen(s) : cave ? Progress.CaveOpen(s) : tree && Trees.Open(s, d.Cfg) > 0;
                double now = PokiClash.Game.SaveService.Now();
                // chấm báo: có dãy huy hiệu vừa mở, chưa đánh trận nào; Nhà cần chăm; cây bi đầy
                bool alert = (temple && open && Badges.HasNew(s, d)) || (farm && open && Home.Alert(s, d, now)) || (tree && open && Trees.Full(s, d.Cfg, now));
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
                        App.Router.Go(temple ? SceneIds.Badges : cave ? SceneIds.Cave : SceneIds.Home);
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
