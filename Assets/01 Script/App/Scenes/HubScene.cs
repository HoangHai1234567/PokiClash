// Sảnh (chép worldScreen của Web/src/view/screens/world.ts): đảo lớn chia 5 vùng hệ, làng máy bi ở giữa.
// Bản đồ thế giới (người dùng 2026-11-19, ArtGen/Islands/sanh_moi): năm đảo liền nhau có địa hình cao thấp, kéo được 4 hướng, vành mây
// che miền chưa mở; không còn làng máy bi trên đảo, công trình side meta ra cột nút cố định. Mây che từng đảo (HubFog): mới chơi che
// hết, chọn tướng khởi đầu thì tan đảo cùng hệ, xong trận hướng dẫn (tạm: thắng ải đầu) thì tan nốt (HubIslands). Mỗi đảo mới mở
// diễn tan mây một lần, khoá chạm trong lúc diễn, camera lướt tới đảo đó.
// Không khoá vùng nào: bảng tên ghi cấp đề nghị, độ khó so với cấp người chơi, tiến độ. Mũi tên nhún chỉ đảo nên đánh.
// Rìa làng có chỗ cho công trình side meta (phác chì khi chưa mở). Hàng nút tròn ở đáy. Lần đầu hiện màn giới thiệu.
// Prefab màn hình Assets/04 Prefabs/Screens/Hub: vùng đảo (Items/BangVung) và công trình (Items/CongTrinh) đặt sẵn theo toạ độ ảnh.
// Ảnh đảo ghép từ đảo gen rời (ArtGen/Islands/compose_islands.py), kéo được (HubPan), ra rìa là vành mây; dựng bằng menu
// "PokiClash/Prefab/Sảnh và đảo/Sảnh và đảo∕Đảo sảnh: ghép ảnh, kéo, mây viền".
using System;
using System.Collections;
using System.Linq;
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
        public override string Title => Loc.T("Sảnh");

        // công trình side meta theo thứ tự đặt trên sảnh: tên, icon, điều kiện mở, lệch so với làng (toạ độ ảnh)
        // (dựng mỗi lần đọc để chữ theo ngôn ngữ đang dùng)
        public static (string name, string icon, string need, float dx, float dy)[] Buildings => new[]
        {
            (Loc.T("Nhà"), "seed", Loc.T("Có 3 tướng để mở Nhà"), -0.27f, 0.035f), // Nhà thay Trang trại (2026-11-18), icon giữ "seed"
            (Loc.T("Đền Huy Hiệu"), "crown", Loc.T("Thắng mini boss đầu tiên ở một đảo bất kỳ để mở Đền Huy Hiệu"), 0.27f, 0.035f),
            (Loc.T("Hang Tiềm Năng"), "rock", Loc.F("Đạt cấp {0} để mở Hang Tiềm Năng", Progress.CaveLevel), 0f, 0.155f),
            // Cây bi dời vào Nhà (2026-11-23): thẻ ở cột ẩn hẳn, giữ chỗ trong mảng cho khớp HubScene.buildings của prefab
            (Loc.T("Cây bi"), "leaf", Loc.T("Qua ải 1 để có cây bi đầu tiên"), -0.27f, 0.155f),
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
        [SerializeField] BottomButton[] bottom; // Cửa hàng, Tướng, Máy Bi, Sổ thẻ, Nhà (người dùng 2026-11-23)
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
            pier.OnTap = () => GoHome(true);
        }

        // về Nhà (nút Nhà ở hàng đáy, con tàu ở bến); chưa mở thì báo điều kiện. click: tự kêu "click" (nút SketchButton đã tự kêu)
        void GoHome(bool click)
        {
            var s = App.Save.Data;
            if (Home.Open(s, App.Data.Cfg))
            {
                if (click) App.Audio.Play("click");
                App.Router.Go(SceneIds.Home);
                return;
            }
            App.Audio.Play("error");
            var farm = System.Array.Find(Buildings, b => b.icon == "seed");
            App.Toasts.Show(farm.need ?? Loc.T("Nhà chưa mở"), Icon("lock"));
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
            softTip = false;
            HookPier();
            Chrome(true, false);
            Render();
            var start = StartFocus();
            if (pan && start) pan.GlideTo(start);
            if (!App.Save.Data.intro || App.Save.Data.starter == null) StartCoroutine(IntroLater());
        }

        public override void Refresh() => Render();

        // người chơi mới: lời mở đầu (GD_Claude/25_FTUE.md bước A2, thay hộp giới thiệu 4 khung), rồi chọn tướng khởi đầu (bản lưu
        // chưa có starter thì mở hộp chọn mỗi lần vào sảnh). Chưa dựng lớp phủ hướng dẫn thì dùng hộp giới thiệu cũ.
        IEnumerator IntroLater()
        {
            while (App.Booting) yield return null; // màn mở game còn che sảnh
            yield return new WaitForSecondsRealtime(0.5f);
            void PickStarter()
            {
                if (App.Save.Data.starter == null) Dialogs.Starter(_ => Render());
            }
            void Seen()
            {
                App.Save.Data.intro = true;
                App.Save.Save();
                PickStarter();
            }
            if (App.Save.Data.intro) PickStarter();
            // lời chào do nhân vật chính của cốt truyện nói (cậu bé thuần thú sư cầm sổ phép, GD_Claude/25_FTUE.md mục 11)
            else if (!Guide.Show(Tutorial.Intro, Guide.Mode.Say, null,
                         Loc.T("Sổ phép đưa mình tới đây... Năm hòn đảo, năm hệ. Phải tìm một bạn đồng hành đã!"), Seen, true, Guide.Me))
                Dialogs.Intro(PickStarter);
        }

        // ---------- hướng dẫn người mới trên sảnh (GD_Claude/25_FTUE.md) ----------

        Coroutine tutor;

        // chọn bước hướng dẫn kế tiếp theo trạng thái bản lưu (tắt game giữa chừng thì vào lại đúng bước), chờ sảnh rảnh rồi mới hiện
        void TutorNext()
        {
            if (tutor != null || !isActiveAndEnabled) return;
            tutor = StartCoroutine(TutorLater());
        }

        IEnumerator TutorLater()
        {
            yield return new WaitForSecondsRealtime(0.4f);
            // App chưa sẵn (script nạp lại giữa Play làm mất các dịch vụ tĩnh): thôi
            if (App.Router == null || App.Modals == null || App.Save == null)
            {
                tutor = null;
                yield break;
            }
            while (App.Booting || App.Router.Busy || reveal != null || App.Modals.Count > 0 || !Guide.Idle) yield return null;
            tutor = null;
            var s = App.Save.Data;
            if (!s.intro || string.IsNullOrEmpty(s.starter) || Tutorial.Off) yield break;
            TutorStep(s, App.Data);
        }

        void TutorStep(SaveData s, GameData d)
        {
            var h = Tutorial.Starter(s, d);
            if (h == null) return;
            var cfg = d.Cfg;
            // A6–A7: vào đảo của tướng đồng hành, đánh ải 1 (trận gương)
            if (Progress.TotalCleared(s) == 0)
            {
                if (!Tutorial.Done(s, Tutorial.Home1))
                    Guide.Say(Tutorial.Home1, Loc.F("{0} là nhà mình. Đi nào!", d.Zone(h.elem)?.name ?? Elements.Name(h.elem)), TutorNext);
                else
                {
                    if (pan && fog && fog.Center(h.elem) && !Guide.Pending(Tutorial.Island)) pan.GlideTo(fog.Center(h.elem));
                    Guide.Force(Tutorial.Island, "hub.zone." + h.elem, Loc.T("Chạm đảo để vào."), null, true);
                }
                return;
            }
            // B8, C7: thả hết bi trong Máy Bi (lần đầu có kết quả viết sẵn)
            if (!Tutorial.Done(s, Tutorial.NoBalls))
            {
                if (s.balls > 0 || s.chests.Count > 0)
                {
                    Guide.Force(Tutorial.Balls, "hub.machine",
                        Tutorial.Done(s, Tutorial.Drop) ? Loc.T("Thả hết bi trong Máy Bi nhé.") : Loc.T("Bi! Thả bi vào Máy Bi để lên cấp."), null, true);
                    return;
                }
                Guide.Skip(Tutorial.Balls, Tutorial.NoBalls);
            }
            // C8: nâng Chiêu bằng 2 bản sao của rương đầu
            if (!Tutorial.Done(s, Tutorial.UpCard))
            {
                if (Progress.CanUpCard(s, cfg, h.id, CardSlot.Skill))
                {
                    Guide.Force(Tutorial.Heroes, "hub.heroes", Loc.F("Nâng cấp Chiêu cho {0}.", h.name), null, true);
                    return;
                }
                Guide.Skip(Tutorial.Heroes, Tutorial.HeroTile, Tutorial.UpCard);
                Render(); // 4 đảo còn lại tan mây
                return;
            }
            // C11–C12: 4 đảo còn lại, rồi trận 2 ở đảo mình khắc
            if (!Tutorial.Done(s, Tutorial.Isles))
            {
                Guide.SayMe(Tutorial.Isles, Loc.T("Bốn đảo nữa! Mỗi đảo có một bạn đang chờ."), TutorNext);
                return;
            }
            var ce = Tutorial.CounterIsland(s, d);
            if (!Tutorial.Done(s, Tutorial.CounterIsle))
            {
                if (s.zones[(int)ce] == 0)
                {
                    // đảo cần khoanh có thể nằm ngoài khung nhìn (sau khi 4 đảo tan mây), mà nền tối chặn kéo bản đồ: lướt camera tới trước
                    if (pan && fog && fog.Center(ce)) pan.GlideTo(fog.Center(ce));
                    Guide.Force(Tutorial.CounterIsle, "hub.zone." + ce,
                        Loc.F("{0}: {1} khắc {2}, đòn của bạn ×1,5.", d.Zone(ce)?.name ?? Elements.Name(ce), Elements.Name(h.elem), Elements.Name(ce)), null, true);
                    return;
                }
                Guide.Skip(Tutorial.CounterIsle, Tutorial.CounterGo, Tutorial.Counter);
            }
            // C17 (trận 2 đã thắng mà chưa nghe lời chào, vd. tắt game ở hộp kết quả)
            if (!Tutorial.CoreDone(s))
            {
                if (s.zones[(int)ce] > 0)
                {
                    Guide.Skip(Tutorial.Shards);
                    Guide.Say(Tutorial.Free, Loc.T("Giờ bạn tự đi nhé. Quên luật thì mở Sổ tay, mục Cách chơi."), Render);
                }
                return;
            }
            // sau chuỗi bắt buộc: khoảnh khắc mở tính năng (xếp hàng), rồi gợi ý theo lúc, mỗi lần vào sảnh một cái
            double now = PokiClash.Game.SaveService.Now();
            var u = Tutorial.NextUnlock(s, d);
            if (u != null)
            {
                Guide.Show(u.id, Guide.Mode.Say, null, $"<b>{u.title}</b>\n{u.text}", () =>
                {
                    Render();
                    if (u.id != "g1") return;
                    if (pan && pier && pier.transform is RectTransform shipRt) pan.GlideTo(shipRt); // con tàu ở bến có thể ngoài khung nhìn
                    Guide.Force("g2", "hub.ship", Loc.T("Chạm con tàu để về Nhà."));
                }, false, s.starter);
                return;
            }
            if (softTip) return;
            softTip = true;
            if (Tutorial.Shows(s, d, Tutorial.HubPart.Afk, now) && Guide.Hint(Tutorial.AfkBtn, "bar.afk",
                    Loc.F("Lúc bạn vắng, {0} vẫn đánh ải đã qua: ra mảnh và rương.", h.name)))
                return;
            // E3 (hái cây bi) dời vào Nhà cùng Cây bi (2026-11-23): HomeScene.Tutor
            if (Tutorial.Shows(s, d, Tutorial.HubPart.Cards, now) && Guide.Hint(Tutorial.CardsBook, "hub.cards", Loc.T("Xem mọi thẻ trong Sổ thẻ.")))
                return;
            if (s.heroes.Any(kv => kv.Value.owned && Progress.CanStarUp(s, d, kv.Key)) &&
                Guide.Hint(Tutorial.StarUp, "hub.heroes", Loc.T("Mảnh dư dùng để lên sao: mạnh thêm.")))
                return;
            softTip = false; // không có gì để gợi ý: lần làm mới sau xét lại
        }

        bool softTip; // đã hiện một gợi ý mềm trong lần vào sảnh này

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
                Guide.Mark("hub.zone." + z.id, item);
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
            if (villageBalls) villageBalls.text = Loc.F("{0} bi đang có", s.balls);
            if (village)
                village.OnClick = () =>
                {
                    App.Audio.Play("click");
                    App.Router.Go(SceneIds.Machine);
                };
            SideMeta(s);
            BottomRow(s);
            Fog(s, d, open);
            if (pier) Guide.Mark("hub.ship", pier);
            TutorNext();
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
                ? Loc.T("Chọn bạn đồng hành để mở đảo đầu tiên")
                : Progress.TotalCleared(s) > 0 ? Loc.F("{0}: sắp mở, làm theo hướng dẫn nhé", App.Data.Zone(e)?.name ?? Loc.T("Đảo"))
                : Loc.F("{0}: hoàn thành trận đầu tiên để mở", App.Data.Zone(e)?.name ?? Loc.T("Đảo"));
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
            TutorNext();
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
                // người mới: công trình chỉ hiện khi tới gần lúc mở (GD_Claude/25_FTUE.md mục 5)
                var part = farm ? Tutorial.HubPart.Home : temple ? Tutorial.HubPart.Temple : cave ? Tutorial.HubPart.Cave : Tutorial.HubPart.Trees;
                // Nhà dời xuống hàng nút đáy, Cây bi dời vào Nhà (2026-11-23): hai thẻ đó ở cột ẩn hẳn
                buildings[i].gameObject.SetActive(!farm && !tree && Tutorial.Shows(s, d, part, now));
                if (tree) Guide.Mark("hub.tree", buildings[i]);
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
                    App.Toasts.Show(open ? Loc.F("{0}: sắp có ở bản sau", item.name) : item.need, Icon(open ? "info" : "lock"));
                });
            }
            StackSide();
        }

        float[] sideY, sideTilt; // chỗ và góc nghiêng gốc (prefab) của từng thẻ trong cột công trình

        // xếp các thẻ đang hiện liền nhau từ chỗ thẻ đầu, không chừa chỗ của thẻ ẩn (Nhà đã dời xuống hàng đáy, thẻ chưa tới lúc hiện)
        void StackSide()
        {
            if (sideY == null)
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

        // hàng nút đáy (người dùng 2026-11-23): Cửa hàng, Tướng (số việc chờ), Máy Bi (to, số bi), Sổ thẻ, Nhà (chấm "!" khi Nhà cần chăm).
        // Đã bỏ Đánh tiếp và Sổ tay (Sổ tay mở bằng nút bánh răng trên thanh trên); Nhà dời từ cột công trình xuống đây.
        void BottomRow(SaveData s)
        {
            var d = App.Data;
            double now = PokiClash.Game.SaveService.Now();
            // người mới: nút hiện dần theo hướng dẫn (Máy Bi sau trận thắng đầu, Tướng sau máy bi, Cửa hàng sau chuỗi bắt buộc, Nhà khi có 2 tướng…)
            MainButton(0, Shop, PokiClash.Core.Offers.AnyClaim(s, d, now) ? 1 : 0, "hub.shop", Tutorial.Shows(s, d, Tutorial.HubPart.Shop, now));
            MainButton(1, () => App.Router.Go(SceneIds.Heroes), Progress.HeroAlerts(s, d), "hub.heroes", Tutorial.Shows(s, d, Tutorial.HubPart.Heroes, now));
            MainButton(2, () => App.Router.Go(SceneIds.Machine), s.balls, "hub.machine", Tutorial.Shows(s, d, Tutorial.HubPart.Machine, now));
            MainButton(3, () => App.Router.Go(SceneIds.Cards), 0, "hub.cards", Tutorial.Shows(s, d, Tutorial.HubPart.Cards, now));
            bool homeOpen = Home.Open(s, d.Cfg);
            MainButton(4, () => GoHome(false), homeOpen && Home.Alert(s, d, now) ? 1 : 0, "hub.home", Tutorial.Shows(s, d, Tutorial.HubPart.Home, now), "!");
        }

        // Cửa hàng (GD_Claude/26_CuaHang_IAP_QuangCao.md, phiên cửa hàng 2026-11-23); chấm đỏ khi có quà miễn phí chờ nhận
        static void Shop() => ShopSheet.OpenShop();

        // mark: chữ trên chấm đỏ thay cho số (Nhà: "!")
        void MainButton(int i, Action go, int dot = 0, string key = null, bool show = true, string mark = null)
        {
            if (bottom == null || i >= bottom.Length) return;
            var b = bottom[i];
            // ẩn cả ô (nút, băng keo, chấm số) và băng chữ đi kèm (Máy Bi có băng chữ "bang_keo_Máy Bi" nằm ngoài ô)
            var slot = b.button.transform.parent;
            if (slot && (slot.name.StartsWith("o_") || slot.name.StartsWith("nut_")))
            {
                slot.gameObject.SetActive(show);
                var tape = slot.parent ? slot.parent.Find("bang_keo_" + slot.name.Substring(slot.name.IndexOf('_') + 1)) : null;
                if (tape) tape.gameObject.SetActive(show);
            }
            else b.button.gameObject.SetActive(show);
            Guide.Mark(key, b.button);
            b.button.SetOnClick(go);
            if (!b.badge) return;
            b.badge.gameObject.SetActive(dot > 0);
            if (dot <= 0) return;
            string txt = mark ?? (dot > 99 ? "99+" : dot.ToString());
            b.badge.sizeDelta = new Vector2(Mathf.Max(52, 22 * txt.Length + 26), 50);
            b.badgeText.text = txt;
        }

        float tutorPoll;

        void Update()
        {
            // hướng dẫn: bước bị bỏ (chỗ cần khoanh chưa sẵn) thì vài giây xét lại một lần
            if ((tutorPoll += Time.unscaledDeltaTime) > 2.5f)
            {
                tutorPoll = 0;
                if (App.I && Guide.Idle) TutorNext();
            }
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

        // bảng tên đảo né cột thẻ công trình, hàng nút đáy và mép màn khi kéo bản đồ (soát UI 2026-11-23); giao diện ẩn (chuyến tàu)
        // thì chỉ né mép màn
        void LateUpdate()
        {
            if (zones == null || zones.Length == 0) return;
            float k = Screen.width / PokiCanvas.RefW, edge = 14 * k;
            float bottomY = edge, topY = Screen.height - (SceneRoot.BarHeight + 10) * k;
            var block = new Rect();
            bool chromeOn = chrome.Length == 0 || !chrome[0] || chrome[0].alpha > 0.5f;
            if (chromeOn)
            {
                if (bottom != null)
                    foreach (var b in bottom)
                    {
                        if (b.button && b.button.gameObject.activeInHierarchy) bottomY = Mathf.Max(bottomY, ScreenRect(b.button.Rect).yMax + 8 * k);
                        if (b.badge && b.badge.gameObject.activeInHierarchy) bottomY = Mathf.Max(bottomY, ScreenRect(b.badge).yMax + 6 * k);
                    }
                bool any = false;
                if (buildings != null)
                    foreach (var hb in buildings)
                    {
                        if (!hb || !hb.gameObject.activeInHierarchy) continue;
                        var r = ScreenRect((RectTransform)hb.transform);
                        block = any ? Rect.MinMaxRect(Mathf.Min(block.xMin, r.xMin), Mathf.Min(block.yMin, r.yMin), Mathf.Max(block.xMax, r.xMax), Mathf.Max(block.yMax, r.yMax)) : r;
                        any = true;
                    }
                if (any) block = Rect.MinMaxRect(block.xMin - 10 * k, block.yMin - 10 * k, Screen.width, block.yMax + 10 * k);
            }
            var safe = Rect.MinMaxRect(edge, bottomY, Screen.width - edge, topY);
            foreach (var z in zones)
                if (z && z.gameObject.activeInHierarchy) z.KeepInView(safe, block, 300 * k, Time.unscaledDeltaTime);
        }

        static readonly Vector3[] screenCorners = new Vector3[4];

        // khung trên màn (điểm ảnh) của một phần giao diện, theo camera canvas chứa nó
        static Rect ScreenRect(RectTransform rt)
        {
            var cv = rt.GetComponentInParent<Canvas>();
            var root = cv ? cv.rootCanvas : null;
            var cam = root && root.renderMode != RenderMode.ScreenSpaceOverlay ? root.worldCamera : null;
            rt.GetWorldCorners(screenCorners);
            Vector2 a = RectTransformUtility.WorldToScreenPoint(cam, screenCorners[0]), b = RectTransformUtility.WorldToScreenPoint(cam, screenCorners[2]);
            return Rect.MinMaxRect(Mathf.Min(a.x, b.x), Mathf.Min(a.y, b.y), Mathf.Max(a.x, b.x), Mathf.Max(a.y, b.y));
        }
    }
}
