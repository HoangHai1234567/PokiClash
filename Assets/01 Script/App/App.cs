// Gốc của game, sống ở scene Boot suốt phiên (DontDestroyOnLoad): nạp dữ liệu, bản lưu, nối các dịch vụ dùng chung
// (âm thanh, chuyển scene, hộp thoại, thông báo, thanh trên), rồi mở scene Hub.
// Prefab Assets/04 Prefabs/App/App.prefab chứa sẵn camera, EventSystem, âm thanh, canvas thanh trên và canvas phủ.
// Chạy trước mọi component khác trong Boot (camera UI, Theme, dữ liệu phải có trước khi canvas và thanh trên Awake).
using System;
using System.Collections;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.InputSystem;

namespace PokiClash
{
    [DefaultExecutionOrder(-100)]
    public sealed class App : MonoBehaviour
    {
        [Header("Dữ liệu (menu PokiClash/Nhập dữ liệu)")]
        public HeroDb heroDb;
        public CardDb cardDb;
        public ZoneDb zoneDb;
        public BalanceConfigAsset balance;

        [Header("Giao diện")]
        public UiAssets uiAssets;
        public ArtLibrary artLibrary;

        [Header("Màn mở game (menu PokiClash/Prefab/Màn mở game: sa bàn)")]
        public BootTitle bootTitle;

        [Header("Chuyến tàu qua mây: sảnh ↔ Nhà, màn tải (menu PokiClash/Prefab/Bến tàu: ...)")]
        public ShipVoyage voyagePrefab;

        [Header("Cốt truyện mở đầu, lần đầu vào game (menu PokiClash/Prefab/Cốt truyện mở đầu)")]
        public StoryIntro storyPrefab;

        [Header("Thử trong Editor")]
        [Tooltip("Scene mở đầu tiên (để trống là Hub)")]
        public string firstScene = SceneIds.Hub;

        // màn mở game / màn tải đang che sảnh: hộp giới thiệu, nút Back chờ nó xong
        public static bool Booting => BootTitle.Current != null || ShipVoyage.Booting || StoryIntro.Current != null;

        // mây chuyển scene đang che hoặc đang chặn chạm (lớp phủ hướng dẫn chờ)
        public static bool Covered => I && I.cloud && (I.cloud.Closed || I.cloud.Blocking);

#if UNITY_EDITOR
        // menu "PokiClash/Thử/Bỏ màn mở game": Play vào thẳng sảnh
        public const string SkipBootPref = "PokiClash.SkipBoot";
        static bool SkipBoot => UnityEditor.EditorPrefs.GetBool(SkipBootPref, false);
#else
        const bool SkipBoot = false;
#endif

        // bấm Play thẳng ở một scene chức năng: scene đó nạp Boot rồi Boot mở lại scene đó
        public static string PendingFirst;
        public static object PendingArgs;

        public static App I { get; private set; }
        public static GameData Data => GameData.Current;
        public static SaveService Save { get; private set; }
        public static AudioService Audio { get; private set; }
        public static SceneRouter Router { get; private set; }
        public static ModalService Modals { get; private set; }
        public static ToastService Toasts { get; private set; }
        public static TopBars Bars { get; private set; }
        public static ArtLibrary Art => ArtLibrary.Current;

        // nút AFK ở thanh trên sảnh
        public static Action OpenAfk = AfkPanel.Open;

        // Vào Play không reload domain (menu PokiClash/Cài đặt/3): mỗi lần Play trả static về như lúc mới chạy. SubsystemRegistration
        // chạy trước khi nạp scene, nên SceneRoot.Awake vẫn đặt PendingFirst sau đó.
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics()
        {
            PendingFirst = null;
            PendingArgs = null;
            I = null;
            Save = null;
            Audio = null;
            Router = null;
            Modals = null;
            Toasts = null;
            Bars = null;
            OpenAfk = AfkPanel.Open;
        }

        [Header("Phần của prefab App (menu PokiClash/Prefab/3. Nướng khung app)")]
        [SerializeField] Camera cam;
        [SerializeField] AudioService audioService;
        [SerializeField] TopBars bars;
        [SerializeField] ModalService modals;
        [SerializeField] ToastService toasts;
        [SerializeField] CloudCover cloud;
        [SerializeField] SceneRouter router;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Camera camera, AudioService audio, TopBars topBars, ModalService modalService, ToastService toastService, CloudCover cover, SceneRouter sceneRouter)
        {
            cam = camera;
            audioService = audio;
            bars = topBars;
            modals = modalService;
            toasts = toastService;
            cloud = cover;
            router = sceneRouter;
        }

        // mã nước 2 chữ theo cài đặt vùng của máy (tạm, tới khi có Remote Config / giờ mạng); không đọc được thì rỗng (không chặn)
        static string DeviceRegion()
        {
            try
            {
                var r = System.Globalization.RegionInfo.CurrentRegion;
                return r != null && r.TwoLetterISORegionName.Length == 2 ? r.TwoLetterISORegionName : "";
            }
            catch (Exception)
            {
                return "";
            }
        }

        void Awake()
        {
            if (I != null)
            {
                Destroy(gameObject);
                return;
            }
            I = this;
            DontDestroyOnLoad(gameObject);
            Application.targetFrameRate = 60;
#if UNITY_EDITOR
            Application.runInBackground = true; // để Play mode chạy tiếp khi Editor không có tiêu điểm (thử qua MCP)
#endif
            // ngưỡng thành kéo theo mật độ điểm ảnh (~2,5 mm), không dưới 10 px của prefab: màn nét 10 px chỉ là ngón rung nhẹ, chạm / giữ
            // thành kéo nên bản đồ trôi và chạm bị huỷ (người dùng 2026-11-20: "khi hold vào các tướng hay tap cam toàn bị move")
            var es = UnityEngine.EventSystems.EventSystem.current ? UnityEngine.EventSystems.EventSystem.current
                : GetComponentInChildren<UnityEngine.EventSystems.EventSystem>(true);
            if (es) es.pixelDragThreshold = Mathf.Max(10, Mathf.RoundToInt((Screen.dpi > 0 ? Screen.dpi : 160) * 0.1f));

            LocService.Init(); // ngôn ngữ trước dữ liệu: GameDb.Build dịch tên tướng, thẻ, đảo, ải
            Casino.Region = DeviceRegion(); // đảo Casino: vùng tắt lều may rủi (casino.tablesBlock)
            // CHƯA PHÁT HÀNH: mở cả ba lều may rủi mọi ngày, bỏ mốc cấp của lều (người dùng 2026-11-26: "cứ để mở các event đi, đã phát hành
            // đâu"). Lịch thật vẫn ở balance.json casino.events; trước khi phát hành XOÁ dòng này để lều theo lịch (GD_Claude/31 mục D3).
            Casino.TestAllBooths = true;
            GameDb.Build(heroDb, cardDb, zoneDb, balance);
            Theme.Init(uiAssets);
            ArtLibrary.Current = artLibrary;
            LocService.Tree(gameObject);

            // camera vẽ mọi canvas: gắn lại các canvas của App (Awake của chúng có thể chạy trước)
            PokiCanvas.UiCamera = cam;
            foreach (var pc in GetComponentsInChildren<PokiCanvas>(true)) pc.Attach();

            Audio = audioService;
            Audio.Init();
            SketchButton.Sound = n =>
            {
                Audio.Play(n);
                // bấm nút một tích rất nhẹ, công tắc tích rõ hơn; "error" (nút khoá) do AudioService.Play rung
                if (n != "error") Haptics.Play(n == "toggle" ? Haptic.UiToggle : Haptic.UiTap);
            };

            Bars = bars;
            Modals = modals;
            Toasts = toasts;
            cloud.CloseNow();
            Router = router;
            Router.Entered += r => Audio.SceneMusic = AudioService.MusicFor(Router.Current, r, Audio.SceneMusic); // nhạc theo scene
            if (voyagePrefab)
            {
                var v = Instantiate(voyagePrefab);
                v.name = voyagePrefab.name;
                LocService.Tree(v);
                DontDestroyOnLoad(v.gameObject);
                Router.SetVoyage(v);
            }
        }

        void Start()
        {
            // gói tải sau (GD_Claude/27): xin tải trước mọi gói chưa có trên máy, theo thứ tự đảo (fast-follow thường đã tự tải từ lúc cài)
            if (Data != null)
                PokiClash.Game.ContentPacks.Prefetch(System.Linq.Enumerable.Select(Data.Zones, z => PokiClash.Core.Keys.Of(z.id)));
            // máy thật: ghi file lưu ở luồng phụ (mỗi lần chạm đều lưu); Editor ghi ngay vì tour ghi đè file lưu rồi Load
            Save = new SaveService(Data) { WriteInBackground = !Application.isEditor };
            Save.Changed += OnSaveChanged;
            bool ok = Save.Load();
            if (!ok)
            {
                // báo trước khi làm mới (bản cũ đã giữ thành .bak)
                Modals.Alert(Loc.T("Bản lưu"), Save.Notice, Loc.T("Bắt đầu lại"), () =>
                {
                    Save.CreateNew();
                    Go();
                });
                StartCoroutine(CloudOf().Open());
                return;
            }
            ApplySettings();
            Go();
        }

        CloudCover CloudOf() => cloud;

        // Sổ tay: đổi ngôn ngữ lúc chạy (2026-11-21). Dựng lại dữ liệu (tên đã dịch), dịch lại khung app và màn tải, nạp lại scene đang mở.
        public static void SetLanguage(string lang)
        {
            if (I == null || lang == Loc.Lang) return;
            LocService.Set(lang);
            GameDb.Build(I.heroDb, I.cardDb, I.zoneDb, I.balance);
            LocService.Tree(I.gameObject);
            if (ShipVoyage.I) LocService.Tree(ShipVoyage.I);
            Bars.Refresh();
            Router.Go(string.IsNullOrEmpty(Router.Current) ? SceneIds.Hub : Router.Current);
        }

        void Go()
        {
            ApplySettings();
            var first = !string.IsNullOrEmpty(PendingFirst) ? PendingFirst : string.IsNullOrEmpty(firstScene) ? SceneIds.Hub : firstScene;
            // chạy thẳng vào sảnh (không phải bấm Play ở scene khác): màn tải tàu đi trên biển (người dùng 2026-11-19, thay màn
            // sa bàn BootTitle), nạp xong thì tàu đi qua mây cập bến sảnh
            if (string.IsNullOrEmpty(PendingFirst) && first == SceneIds.Hub && !SkipBoot)
            {
                // lần đầu vào game: đoạn cốt truyện trước màn tải (mây còn khép che dưới nó), xem xong ghi cờ rồi vào màn tải như thường
                if (storyPrefab && StoryIntro.Needed(Save.Data))
                {
                    var st = Instantiate(storyPrefab);
                    st.name = storyPrefab.name;
                    LocService.Tree(st.gameObject);
                    // truyện mờ dần thì màn tải phải nằm sẵn bên dưới; trước đây mờ xong mới mở mây, bật màn tải nên lộ hai đám mây khép
                    // 0,4 giây ("nháy nhanh 2 đám mây che xong mới sang boot", APK 2026-11-27)
                    st.Play(() =>
                    {
                        Destroy(st.gameObject);
                        Go();
                    }, () =>
                    {
                        Tutorial.Mark(Save.Data, Tutorial.Story);
                        Save.Save();
                        if (ShipVoyage.I)
                        {
                            cloud.OpenNow();
                            ShipVoyage.I.BeginBoot();
                        }
                    });
                    return;
                }
                if (ShipVoyage.I)
                {
                    cloud.OpenNow();
                    if (!ShipVoyage.Booting) ShipVoyage.I.BeginBoot(); // đã bật lúc truyện mở đầu bắt đầu mờ
                }
                else BootTitle.Spawn(bootTitle);
            }
            Router.Go(first, PendingArgs);
            PendingFirst = null;
            PendingArgs = null;
        }

        // vào nền, thoát: chờ ghi nền xong (Android có thể giết app ngay sau khi vào nền)
        void OnApplicationPause(bool paused)
        {
            if (paused) Save?.Flush();
        }

        void OnApplicationQuit() => Save?.Flush();

        void OnSaveChanged()
        {
            ApplySettings();
            Bars.Refresh();
            if (Router.CurrentRoot) Router.CurrentRoot.Refresh();
        }

        public static void ApplySettings()
        {
            var st = Save?.Data?.settings;
            if (st == null) return;
            Theme.SetBoil(true); // hoạt cảnh đảo/trận luôn chạy (công tắc "Nét vẽ rung" đã bỏ 2026-11-06; chụp đứng hình tắt tạm rồi gọi lại đây)
            Audio.Enabled = st.sound;
            Haptics.Enabled = st.haptics;
        }

        // khép mây, làm việc giữa chừng (lúc đã che kín), rồi mở mây (màn mở game tắt dưới mây)
        public static IEnumerator CoverThen(Action mid)
        {
            Audio?.Play("whoosh");
            Haptics.Play(Haptic.Transition);
            yield return I.cloud.Close();
            mid?.Invoke();
            yield return new WaitForSecondsRealtime(0.06f);
            yield return I.cloud.Open();
        }

        // nút Back của Android / phím Esc: đóng hộp thoại trên cùng, không có thì quay lại
        public static void Back()
        {
            if (StoryIntro.Current)
            {
                StoryIntro.Current.Finish(); // Back trên cốt truyện = Bỏ qua
                return;
            }
            if (Router.Busy || Booting) return;
            if (Modals.Back()) return;
            Router.Back();
        }

        void Update()
        {
            PokiClash.Game.ContentPacks.Tick(); // hàng chờ gói tải sau (GD_Claude/27)
            ListDrag.Tick(); // danh sách cuộn: ngưỡng kéo nhỏ hơn bản đồ
            var kb = Keyboard.current;
            if (kb != null && kb.escapeKey.wasPressedThisFrame) Back();
        }
    }
}
