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

        [Header("Thử trong Editor")]
        [Tooltip("Scene mở đầu tiên (để trống là Hub)")]
        public string firstScene = SceneIds.Hub;

        // màn mở game đang che sảnh: hộp giới thiệu, nút Back chờ nó xong
        public static bool Booting => BootTitle.Current != null;

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

            GameDb.Build(heroDb, cardDb, zoneDb, balance);
            Theme.Init(uiAssets);
            ArtLibrary.Current = artLibrary;

            // camera vẽ mọi canvas: gắn lại các canvas của App (Awake của chúng có thể chạy trước)
            PokiCanvas.UiCamera = cam;
            foreach (var pc in GetComponentsInChildren<PokiCanvas>(true)) pc.Attach();

            Audio = audioService;
            Audio.Init();
            SketchButton.Sound = n => Audio.Play(n);

            Bars = bars;
            Modals = modals;
            Toasts = toasts;
            cloud.CloseNow();
            Router = router;
        }

        void Start()
        {
            // máy thật: ghi file lưu ở luồng phụ (mỗi lần chạm đều lưu); Editor ghi ngay vì tour ghi đè file lưu rồi Load
            Save = new SaveService(Data) { WriteInBackground = !Application.isEditor };
            Save.Changed += OnSaveChanged;
            bool ok = Save.Load();
            if (!ok)
            {
                // báo trước khi làm mới (bản cũ đã giữ thành .bak)
                Modals.Alert("Bản lưu", Save.Notice, "Bắt đầu lại", () =>
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

        void Go()
        {
            ApplySettings();
            var first = !string.IsNullOrEmpty(PendingFirst) ? PendingFirst : string.IsNullOrEmpty(firstScene) ? SceneIds.Hub : firstScene;
            // chạy thẳng vào sảnh (không phải bấm Play ở scene khác): màn mở game diễn trên sảnh đang nạp
            if (string.IsNullOrEmpty(PendingFirst) && first == SceneIds.Hub && !SkipBoot) BootTitle.Spawn(bootTitle);
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
            yield return I.cloud.Close();
            mid?.Invoke();
            yield return new WaitForSecondsRealtime(0.06f);
            yield return I.cloud.Open();
        }

        // nút Back của Android / phím Esc: đóng hộp thoại trên cùng, không có thì quay lại
        public static void Back()
        {
            if (Router.Busy || Booting) return;
            if (Modals.Back()) return;
            Router.Back();
        }

        void Update()
        {
            var kb = Keyboard.current;
            if (kb != null && kb.escapeKey.wasPressedThisFrame) Back();
        }
    }
}
