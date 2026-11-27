// Giao diện sảnh chung (người dùng 2026-11-27: "thiết kế lại để các UI này sống qua các màn home/đảo chính/đảo casino, chỉ tắt khi vào các
// scene bên trong thôi. ở 2 scene kia bỏ tên và nút back đi"). Nằm trong App.prefab, cùng canvas với thanh trên (Canvas thanh tren, nút
// sanh_chung ngay dưới Thanh tren), nên sống qua mọi màn: hiện khi màn dùng thanh Hud (sảnh, Nhà, đảo Casino; TopBars.Show gọi Show),
// ẩn ở các màn bên trong. Gồm:
// - hàng nút đáy kệ gỗ (hang_nut, dựng bằng HubDockMenu): Cửa hàng, Tướng, Máy Bi, Sổ thẻ, Nhà. Ô dẫn tới màn đang đứng đổi thành
//   "Đảo chính" (về sảnh, icon bản đồ): ở Nhà là ô Nhà, ở đảo Casino là nút Máy Bi giữa (Tháp Máy Bi vẫn chạm được trên đảo);
// - cột công trình bên phải (cot_cong_trinh, HubBuilding theo HubScene.Buildings): Đền Huy Hiệu, Hang Tiềm Năng, Sổ Phép;
// - cột ưu đãi bên trái (cua_hang_san, HubShop tự cập nhật; nằm trong vùng an toàn của cùng canvas, dựng bằng ShopMenu.BuildHub).
// Canvas thanh trên (thứ tự 10) vẽ trên lớp chuyến tàu (9): đi tàu sảnh ↔ Nhà / đảo thì giao diện đứng yên, thế giới trôi (ShipVoyage
// chụp màn không kèm canvas này). Đang chuyển màn thì không nhận chạm. Màn cần chỗ đáy riêng (chế độ Xây / Lát ô của Nhà) gọi Hold để ẩn tạm.
// Ba cụm dời từ Screens/Hub sang bằng menu "PokiClash/Prefab/Sảnh và đảo/Sảnh chung: dời hàng nút, cột công trình, cột ưu đãi sang App"
// (Editor/LobbyDockMenu.cs); các menu dựng hàng nút / cột (HubDockMenu, HubTileMenu, HubBadgeMenu, SoPhepMenu, ShopMenu.BuildHub) sửa ở App.prefab.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class LobbyDock : MonoBehaviour
    {
        // mép trên của kệ chung tính từ đáy khung (đơn vị canvas, theo HubDockMenu: kệ 196, thẻ 176 tâm ở 104, băng keo nhô; nút Máy Bi 236
        // tâm ở 154): màn có hàng nút riêng đặt trên mức này
        public const float ShelfTop = 214, CenterTop = 290;

        // một nút ở hàng đáy; chấm đỏ số (nếu có) bật theo dữ liệu
        [Serializable]
        public struct BottomButton
        {
            public SketchButton button;
            public RectTransform badge;
            public TextMeshProUGUI badgeText;
        }

        public static LobbyDock I { get; private set; }

        [SerializeField] BottomButton[] bottom = new BottomButton[0]; // Cửa hàng, Tướng, Máy Bi, Sổ thẻ, Nhà (người dùng 2026-11-23)
        [SerializeField] HubBuilding[] buildings = new HubBuilding[0]; // theo thứ tự HubScene.Buildings

        // Dùng khi dựng prefab (Editor).
        public void Setup(BottomButton[] bottomButtons, HubBuilding[] buildingItems)
        {
            bottom = bottomButtons;
            buildings = buildingItems;
        }

        public BottomButton[] Bottom => bottom;
        public HubBuilding[] Buildings => buildings;

        // đang hiện (màn dùng thanh Hud, không màn nào giữ ẩn)
        public bool Visible => shown && holds.Count == 0;

        // nút "Đảo chính" ở màn đang đứng (Nhà: ô Nhà, đảo Casino: nút Máy Bi), null ở sảnh
        public SketchButton IslandButton { get; private set; }

        bool shown;
        readonly List<UnityEngine.Object> holds = new List<UnityEngine.Object>();
        HubShop shop;
        CanvasGroup group, shopGroup;
        float[] sideY, sideTilt; // chỗ và góc nghiêng gốc (prefab) của từng thẻ trong cột công trình

        // ảnh / chữ gốc của ô đổi thành "Đảo chính" (trả lại khi về sảnh)
        Image homeIcon, centerIcon;
        TextMeshProUGUI homeLabel, centerLabel;
        Sprite homeSprite, centerSprite;
        string homeText, centerText;
        bool homeSwapped, centerSwapped;

        static SaveData S => App.Save?.Data;
        static GameData D => App.Data;
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        void Awake()
        {
            I = this;
            group = GetComponent<CanvasGroup>();
            if (!group) group = gameObject.AddComponent<CanvasGroup>();
            var canvas = GetComponentInParent<PokiCanvas>(true);
            shop = canvas ? canvas.GetComponentInChildren<HubShop>(true) : null;
            if (shop)
            {
                shopGroup = shop.GetComponent<CanvasGroup>();
                if (!shopGroup) shopGroup = shop.gameObject.AddComponent<CanvasGroup>();
            }
            if (bottom.Length > 4 && bottom[4].button)
            {
                homeIcon = FindImage(bottom[4].button.transform, "icon");
                homeLabel = bottom[4].button.Label;
            }
            if (bottom.Length > 2 && bottom[2].button)
            {
                centerIcon = FindImage(bottom[2].button.transform, "icon");
                var row = bottom[2].button.transform.parent ? bottom[2].button.transform.parent.parent : null;
                var ribbon = row ? row.Find("bang_keo_Máy Bi") : null;
                centerLabel = ribbon ? ribbon.GetComponentInChildren<TextMeshProUGUI>(true) : null;
            }
            Apply();
        }

        void OnDestroy()
        {
            if (I == this) I = null;
        }

        static Image FindImage(Transform root, string name) =>
            root.GetComponentsInChildren<Image>(true).FirstOrDefault(i => i.name == name);

        // TopBars.Show: màn dùng thanh Hud thì hiện
        public void Show(bool on)
        {
            shown = on;
            holds.RemoveAll(h => !h);
            Apply();
            if (on) Render();
        }

        // màn giữ ẩn tạm (key: màn đó; màn bị gỡ thì tự nhả)
        public static void Hold(UnityEngine.Object key, bool on)
        {
            if (!I || !key) return;
            if (on && !I.holds.Contains(key)) I.holds.Add(key);
            else if (!on) I.holds.Remove(key);
            I.Apply();
        }

        void Apply()
        {
            bool on = Visible;
            foreach (Transform c in transform)
                if (c.gameObject.activeSelf != on)
                    c.gameObject.SetActive(on);
            if (shop && shop.gameObject.activeSelf != on) shop.gameObject.SetActive(on);
        }

        // dữ liệu lưu đổi (TopBars.Refresh)
        public void Refresh()
        {
            if (Visible) Render();
        }

        void Update()
        {
            // đang chuyển màn (mây, chuyến tàu): giao diện đứng yên nhưng không nhận chạm
            bool live = App.Router == null || !App.Router.Busy;
            if (group.blocksRaycasts != live) group.blocksRaycasts = live;
            if (shopGroup && shopGroup.blocksRaycasts != live) shopGroup.blocksRaycasts = live;
        }

        void Render()
        {
            var s = S;
            if (s == null || D == null) return;
            SideMeta(s);
            BottomRow(s);
        }

        // ---------- cột công trình ----------

        // hiện khi tới lúc theo hướng dẫn; chưa mở thì báo điều kiện
        void SideMeta(SaveData s)
        {
            var d = D;
            var items = HubScene.Buildings;
            double now = PokiClash.Game.SaveService.Now();
            for (int i = 0; i < buildings.Length && i < items.Length; i++)
            {
                if (!buildings[i]) continue;
                var item = items[i];
                bool temple = item.icon == "crown", cave = item.icon == "rock", farm = item.icon == "seed", tree = item.icon == "leaf",
                    book = item.icon == "pencil";
                bool open = farm ? Home.Open(s, d.Cfg) : temple ? Progress.BadgesOpen(s) : cave ? Progress.CaveOpen(s) : book ? SoPhep.Open(s, d.Cfg) :
                    tree && Trees.Open(s, d.Cfg) > 0;
                // người mới: công trình chỉ hiện khi tới gần lúc mở (GD_Claude/25_FTUE.md mục 5)
                var part = farm ? Tutorial.HubPart.Home : temple ? Tutorial.HubPart.Temple : cave ? Tutorial.HubPart.Cave :
                    book ? Tutorial.HubPart.SoPhep : Tutorial.HubPart.Trees;
                // Nhà dời xuống hàng nút đáy, Cây bi dời vào Nhà (2026-11-23): hai thẻ đó ở cột ẩn hẳn
                buildings[i].gameObject.SetActive(!farm && !tree && Tutorial.Shows(s, d, part, now));
                if (tree) Guide.Mark("hub.tree", buildings[i]);
                if (book) Guide.Mark("hub.sophep", buildings[i]);
                // chấm báo: có dãy huy hiệu vừa mở, chưa đánh trận nào; Nhà cần chăm; cây bi đầy; Sổ Phép có nút học được
                bool alert = (temple && open && Badges.HasNew(s, d)) || (farm && open && Home.Alert(s, d, now)) || (tree && open && Trees.Full(s, d.Cfg, now)) ||
                             (book && open && d.Cfg.sophep.nodes.Any(n => SoPhep.Block(s, d.Cfg, n.id) == ""));
                string name = item.name, need = item.need;
                buildings[i].Bind(name, open, alert, () =>
                {
                    if (tree && open)
                    {
                        App.Audio.Play("click");
                        TreePanel.Open();
                        return;
                    }
                    if (book && open)
                    {
                        App.Audio.Play("click");
                        Guide.Skip("h_sophep2");
                        SoPhepDialog.Open();
                        return;
                    }
                    if ((temple || cave || farm) && open)
                    {
                        App.Audio.Play("click");
                        App.Router.Go(temple ? SceneIds.Badges : cave ? SceneIds.Cave : SceneIds.Home);
                        return;
                    }
                    App.Audio.Play(open ? "click" : "error");
                    App.Toasts.Show(open ? Loc.F("{0}: sắp có ở bản sau", name) : need, Icon(open ? "info" : "lock"));
                });
            }
            StackSide();
        }

        // xếp các thẻ đang hiện liền nhau từ chỗ thẻ đầu, không chừa chỗ của thẻ ẩn
        void StackSide()
        {
            if (sideY == null || sideY.Length != buildings.Length)
            {
                sideY = new float[buildings.Length];
                sideTilt = new float[buildings.Length];
                for (int i = 0; i < buildings.Length; i++)
                    if (buildings[i])
                    {
                        sideY[i] = ((RectTransform)buildings[i].transform).anchoredPosition.y;
                        sideTilt[i] = buildings[i].transform.localEulerAngles.z;
                    }
            }
            int k = 0;
            for (int i = 0; i < buildings.Length; i++)
            {
                if (!buildings[i] || !buildings[i].gameObject.activeSelf) continue;
                var rt = (RectTransform)buildings[i].transform;
                rt.anchoredPosition = new Vector2(rt.anchoredPosition.x, sideY[k]);
                rt.localEulerAngles = new Vector3(0, 0, sideTilt[k]);
                k++;
            }
        }

        // ---------- hàng nút đáy ----------

        // Cửa hàng, Tướng (số việc chờ), Máy Bi (to, số bi), Sổ thẻ, Nhà (chấm "!" khi Nhà cần chăm); ô của màn đang đứng thành "Đảo chính"
        void BottomRow(SaveData s)
        {
            var d = D;
            double now = PokiClash.Game.SaveService.Now();
            string cur = App.Router ? App.Router.Current : null;
            bool atHome = cur == SceneIds.Home, atCasino = cur == SceneIds.Casino;
            IslandButton = null;
            // người mới: nút hiện dần theo hướng dẫn (Máy Bi sau trận thắng đầu, Tướng sau máy bi, Cửa hàng sau chuỗi bắt buộc, Nhà khi có 2 tướng…)
            MainButton(0, () => ShopSheet.OpenShop(), Offers.AnyClaim(s, d, now) ? 1 : 0, "hub.shop", Tutorial.Shows(s, d, Tutorial.HubPart.Shop, now));
            MainButton(1, () => App.Router.Go(SceneIds.Heroes), Progress.HeroAlerts(s, d), "hub.heroes", Tutorial.Shows(s, d, Tutorial.HubPart.Heroes, now));
            // nút giữa (người dùng 2026-11-25): ra đảo Casino "Bến Lữ Khách" (Tháp Máy Bi ở giữa đảo); đảo chưa mở thì vào thẳng máy bi
            bool machineOn = Tutorial.Shows(s, d, Tutorial.HubPart.Machine, now);
            SwapCenter(atCasino);
            if (atCasino)
            {
                MainButton(2, GoIsland, 0, null, true);
                IslandButton = bottom.Length > 2 ? bottom[2].button : null;
            }
            // không chấm số bi ở góc (người dùng 2026-11-27: "bỏ noti số đỏ góc phải đi"; số bi đã có trên thanh trên)
            else MainButton(2, () => App.Router.Go(Casino.Open(s, d) ? SceneIds.Casino : SceneIds.Machine), 0, "hub.machine", machineOn);
            MainButton(3, () => App.Router.Go(SceneIds.Cards), 0, "hub.cards", Tutorial.Shows(s, d, Tutorial.HubPart.Cards, now));
            SwapHome(atHome);
            if (atHome)
            {
                MainButton(4, GoIsland, 0, null, true);
                IslandButton = bottom.Length > 4 ? bottom[4].button : null;
            }
            else
            {
                bool homeOpen = Home.Open(s, d.Cfg);
                MainButton(4, () => GoHome(false), homeOpen && Home.Alert(s, d, now) ? 1 : 0, "hub.home", Tutorial.Shows(s, d, Tutorial.HubPart.Home, now), "!");
            }
        }

        static void GoIsland() => App.Router.Go(SceneIds.Hub);

        // về Nhà (nút Nhà ở hàng đáy, con tàu ở bến sảnh); chưa mở thì báo điều kiện. click: tự kêu "click" (nút SketchButton đã tự kêu)
        public static void GoHome(bool click)
        {
            var s = App.Save.Data;
            if (Home.Open(s, App.Data.Cfg))
            {
                if (click) App.Audio.Play("click");
                App.Router.Go(SceneIds.Home);
                return;
            }
            App.Audio.Play("error");
            var farm = Array.Find(HubScene.Buildings, b => b.icon == "seed");
            App.Toasts.Show(farm.need ?? Loc.T("Nhà chưa mở"), Icon("lock"));
        }

        void SwapHome(bool island)
        {
            if (!homeSwapped && island)
            {
                homeSprite = homeIcon ? homeIcon.sprite : null;
                homeText = homeLabel ? homeLabel.text : null;
            }
            if (island == homeSwapped) return;
            homeSwapped = island;
            if (homeIcon) Theme.SetSprite(homeIcon, island ? Icon("map") : homeSprite);
            if (homeLabel) homeLabel.text = island ? Loc.T("Đảo chính") : homeText;
        }

        // nút giữa: ở đảo Casino là "Đảo chính" (về sảnh). Nơi khác: đảo Casino đã mở thì icon casino (bàn roulette đỏ đen + bài + xúc
        // xắc, Fallback/Icons/casino.png) và chữ "Casino" (người dùng 2026-11-27: "icon này nên đổi sang icon kiểu khác để hiểu đây là đảo
        // casino chứ không chỉ pachinko"); chưa mở thì nút vào thẳng máy bi nên giữ icon máy bi và chữ "Máy Bi" của prefab (hướng dẫn người
        // mới gọi "Máy Bi").
        void SwapCenter(bool island)
        {
            if (!centerSwapped)
            {
                centerSprite = centerIcon ? centerIcon.sprite : null;
                centerText = centerLabel ? centerLabel.text : null;
                centerSwapped = true; // đã giữ ảnh / chữ gốc của prefab
            }
            bool casino = !island && S != null && D != null && Casino.Open(S, D);
            if (centerIcon) Theme.SetSprite(centerIcon, island ? Icon("map") : casino ? Icon("casino") : centerSprite);
            if (centerLabel) centerLabel.text = island ? Loc.T("Đảo chính") : casino ? Loc.T("Casino") : centerText;
        }

        // mark: chữ trên chấm đỏ thay cho số (Nhà: "!")
        void MainButton(int i, Action go, int dot = 0, string key = null, bool show = true, string mark = null)
        {
            if (bottom == null || i >= bottom.Length || !bottom[i].button) return;
            var b = bottom[i];
            // ẩn cả ô (nút, băng keo, chấm số) và băng chữ đi kèm (Máy Bi có băng chữ "bang_keo_Máy Bi" nằm ngoài ô)
            var slot = b.button.transform.parent;
            if (slot && (slot.name.StartsWith("o_") || slot.name.StartsWith("nut_")))
            {
                if (slot.gameObject.activeSelf != show) slot.gameObject.SetActive(show);
                var tape = slot.parent ? slot.parent.Find("bang_keo_" + slot.name.Substring(slot.name.IndexOf('_') + 1)) : null;
                if (tape && tape.gameObject.activeSelf != show) tape.gameObject.SetActive(show);
            }
            else if (b.button.gameObject.activeSelf != show) b.button.gameObject.SetActive(show);
            if (key != null) Guide.Mark(key, b.button);
            b.button.SetOnClick(go);
            if (!b.badge) return;
            b.badge.gameObject.SetActive(dot > 0);
            if (dot <= 0) return;
            string txt = mark ?? (dot > 99 ? "99+" : dot.ToString());
            b.badge.sizeDelta = new Vector2(Mathf.Max(52, 22 * txt.Length + 26), 50);
            b.badgeText.text = txt;
        }
    }
}
