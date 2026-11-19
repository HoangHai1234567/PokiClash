// Màn Nhà (GD_Claude/21_Nha_Home.md, mốc H2), thay Trang trại. Luật ở Core/Home. Prefab Assets/04 Prefabs/Screens/Home dựng bằng menu
// "PokiClash/Prefab/Nhà: dựng màn" (Editor/HomeSceneMenu.cs).
// - Bản đồ: ảnh nền đảo (home_base: đồng cỏ hình thoi, cao nguyên, hồ, suối, mạch quặng, bãi cát, biển, rừng rìa trên) kéo, phóng to thu nhỏ nhẹ (LandView của màn Đảo, chế độ phủ kín màn);
//   lưới thoi 72 x 72 (người dùng dặn 2026-11-19: đảo to cho quái đi khắp nơi, máy không cần thấy hết đảo), ô 96 x 48 px; gốc lưới
//   (góc trên ô 0,0) đo trên ảnh nền (home_art.json, ảnh ghép bằng ArtGen/Home/base/compose_base72.py).
// - Quái (FarmPet của Trang trại, cảnh chủ là màn này): tướng rảnh đi lang thang trên đất đã mở (tối đa MaxRoam con), tướng đang làm
//   đứng trước công trình cử động theo việc, tướng đang nghỉ ngủ cạnh Nhà chính. Quái chỉ vào làm khi người chơi kéo thả nó vào công
//   trình hoặc chọn trong bảng công trình (hộp chọn tướng); không có Tự xếp.
// - Bến tàu ở mũi dưới (PierShip, dựng bằng ShipBuild.Pier của phiên sảnh): chuyến tàu qua mây sảnh ↔ Nhà cập bến / rời bến ở đây; tàu
//   cập bến xong thì máy lướt lên Nhà chính; chạm tàu là về đảo.
// - Lớp: ô lát (đất, cát, đường đá, nước) → vật (khối rừng trên ô chưa mở, công trình, trang trí; vẽ xa trước gần sau theo góc dưới
//   chân thoi) → sáng tối (DayNight dùng chung với các đảo: nhuộm theo giờ máy, tia nắng; đèn công trình bật khi tối) → mây che rìa
//   (từng đám rời dựng sẵn trong prefab, CloudRing toả quanh tàu).
// - Chạm: công trình → bảng (thu, giao/rút tướng, nâng cấp); ô rừng → dọn; chế độ xây: khay công trình, chạm đất để dời bóng ma, Đặt;
//   chế độ lát: chọn loại ô, chạm đất để lát.
// - Chế độ xây hiện lưới thoi phát sáng trên đất đã mở (người dùng dặn 2026-11-19; shader PokiClash/UIHomeGrid trên ảnh "luoi" nằm trên
//   ô lát, dưới công trình): mờ dần ra xa chỗ đang đặt, chân thoi công trình đang đặt sáng xanh (đặt được) / đỏ (không), viền phập phồng.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HomeScene : SceneRoot, IFarmPetHost
    {
        public override string Title => "Nhà";

        const float CW = 96, CH = 48; // một ô lưới: ngang, dọc (px)
        const float TreeScale = 192f / 150f * 0.85f; // cây rời: chân cỏ 150 px ở ảnh gen = 2 ô lưới; thu 0,85 cho cân với nhà
        const float TopInset = SceneRoot.BarHeight + 70, BottomInset = 230; // khung trên (thanh, dòng tài nguyên), dưới (hàng nút, gợi ý)

        enum Mode { Normal, Build, Paint }

        [Serializable]
        public struct ArtMeta
        {
            public string id; // home_b_<def> | home_forest_a.. | home_cloud_..
            public Sprite sprite;
            public Vector2 pivot;
            public float foot; // bề ngang chân thoi trong ảnh (px)
            public int cells;
        }

        // cây rời trong atlas home_trees (rải ngẫu nhiên trong ô rừng chưa mở): nhóm tall / special / palm / small
        [Serializable]
        public struct TreeArt
        {
            public string id, group;
            public Sprite sprite;
            public Vector2 pivot;
        }

        [Serializable]
        public struct NamedSprite
        {
            public string id;
            public Sprite sprite;
        }

        [Header("Bản đồ")]
        [SerializeField] LandView landView; // không đặt tên "view": trùng trường PokiCanvas view của SceneRoot
        [SerializeField] RectTransform world; // lớp kéo, cỡ bằng ảnh nền đã phóng
        [SerializeField] Image ground;
        [SerializeField] HomeTap tap;
        [SerializeField] RectTransform tileLayer, objLayer, lightLayer, cloudLayer;
        [SerializeField] Vector2 gridTop; // góc trên ô (0,0), px từ góc trên trái bản đồ
        [SerializeField] HomeObject objPrefab;
        [SerializeField] Image tilePrefab, glowPrefab, cloudPrefab;
        [SerializeField] ArtMeta[] art;
        [SerializeField] Sprite glowSprite;
        [SerializeField] Image treePrefab;
        [SerializeField] TreeArt[] treeArt;
        [SerializeField] NamedSprite[] tileArt; // fill_<loại>, lip_<loại>_<mép>, cor_<loại>_<góc>, bank_<mép> (ArtGen/Home/tiles/make_tiles.py)

        [Header("Quái")]
        [SerializeField] RectTransform fxLayer; // lớp hạt, cùng khung với lớp vật
        [SerializeField] FarmPet petPrefab;
        [SerializeField] FarmFx fxPrefab;
        [SerializeField] Sprite[] props; // theo FarmProp
        [SerializeField] FarmPickerDialog pickerPrefab;
        [SerializeField] PierShip pier; // tàu đậu ở bến mũi dưới
        [SerializeField] Image gridImg; // lưới phát sáng của chế độ xây
        Material gridMat;
        float gridFade;
        readonly float[] gridLots = new float[64];
        [SerializeField] CanvasGroup chrome; // giao diện cố định (nha_ui): dòng tài nguyên, gợi ý, hàng nút, khay, bảng chọn
        Coroutine chromeFade;

        [Header("Giao diện")]
        [SerializeField] TextMeshProUGUI res, hint;
        [SerializeField] SketchButton btnBuild, btnPaint, btnHarvest, btnSail;
        [SerializeField] RectTransform tray;
        [SerializeField] SketchButton trayPrefab;
        [SerializeField] RectTransform panel;
        [SerializeField] TextMeshProUGUI panelTitle, panelBody;
        [SerializeField] SketchButton panelA, panelB, panelC, panelD;

        readonly Dictionary<int, HomeObject> objs = new Dictionary<int, HomeObject>(); // id công trình → vật
        readonly Dictionary<int, HomeObject> forests = new Dictionary<int, HomeObject>(); // ô rừng → mốc (nhãn "Dọn …")
        readonly Dictionary<int, List<(Image img, float depth)>> forestTrees = new Dictionary<int, List<(Image, float)>>();
        readonly List<Image> tileImgs = new List<Image>();
        Dictionary<string, Sprite> tileMap;
        string tileSig;
        readonly List<(Image img, int id)> lights = new List<(Image, int)>();
        HomeObject ghost;
        string ghostDef, paintTile = "dirt";
        Vector2Int ghostAt;
        int moveId = -1; // đang dời công trình này (bóng ma thay chỗ nó); -1 = bóng ma xây mới
        Vector2Int grabOffset; // ô dưới ngón trừ góc bóng ma lúc cầm lên
        Mode mode;
        int selBuilding = -1, selLot = -1;
        float timer, clock, sortTimer;
        readonly Dictionary<string, FarmPet> pets = new Dictionary<string, FarmPet>();
        readonly List<FarmFx> fxPool = new List<FarmFx>();
        readonly List<(Transform t, float d)> order = new List<(Transform, float)>();
        readonly List<Vector2Int> walkCells = new List<Vector2Int>();
        bool petsPlaced;
        int focusWait; // chờ khung nhìn đứng yên vài khung rồi mới đặt máy vào Nhà chính
        bool shipArriving, shipSeenBusy; // chuyến tàu đang cập bến: xong thì máy lướt lên Nhà chính
        float shipDockedAt = -1; // lúc tàu đứng yên ở bến (chờ 0,4 giây rồi mới lướt)
        Vector2 focusView;
        int dragHover = -1; // công trình đang sáng dưới quái đang kéo
        const int MaxRoam = 14, MaxSleep = 4;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static HomeConfig C => App.Data.Cfg.home;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi nướng prefab (Editor).
        public void SetupMap(LandView viewComp, RectTransform worldRt, Image groundImg, HomeTap tapComp, RectTransform tilesRt, RectTransform objsRt,
            RectTransform lightsRt, RectTransform cloudsRt, Vector2 top, HomeObject obj, Image tile, Image glow, Image cloud, ArtMeta[] metas, Sprite glowSp,
            Image tree, TreeArt[] trees, NamedSprite[] tileSprites)
        {
            landView = viewComp;
            treePrefab = tree;
            treeArt = trees;
            tileArt = tileSprites;
            world = worldRt;
            ground = groundImg;
            tap = tapComp;
            tileLayer = tilesRt;
            objLayer = objsRt;
            lightLayer = lightsRt;
            cloudLayer = cloudsRt;
            gridTop = top;
            objPrefab = obj;
            tilePrefab = tile;
            glowPrefab = glow;
            cloudPrefab = cloud;
            art = metas;
            glowSprite = glowSp;
        }

        // Dùng khi nướng prefab (Editor).
        public void SetupUi(TextMeshProUGUI resText, TextMeshProUGUI hintText, SketchButton build, SketchButton paint, SketchButton harvest,
            SketchButton sail, RectTransform trayRt, SketchButton trayItem, RectTransform panelRt, TextMeshProUGUI title, TextMeshProUGUI body,
            SketchButton a, SketchButton b, SketchButton c, SketchButton d)
        {
            panelD = d;
            res = resText;
            hint = hintText;
            btnBuild = build;
            btnPaint = paint;
            btnHarvest = harvest;
            btnSail = sail;
            tray = trayRt;
            trayPrefab = trayItem;
            panel = panelRt;
            panelTitle = title;
            panelBody = body;
            panelA = a;
            panelB = b;
            panelC = c;
        }

        // Dùng khi nướng prefab (Editor).
        public void SetupPets(RectTransform fx, FarmPet pet, FarmFx fxItem, Sprite[] propSprites, FarmPickerDialog picker)
        {
            fxLayer = fx;
            petPrefab = pet;
            fxPrefab = fxItem;
            props = propSprites;
            pickerPrefab = picker;
        }

        // Dùng khi nướng prefab (Editor).
        public void SetupPier(PierShip p) => pier = p;

        // Dùng khi nướng prefab (Editor).
        public void SetupGrid(Image grid) => gridImg = grid;

        // ---------- lưới phát sáng (chế độ xây) ----------

        void InitGrid()
        {
            if (!gridImg || !gridImg.material) return;
            if (!gridMat)
            {
                gridMat = new Material(gridImg.material); // bản riêng: đổi số mỗi khung không đụng tới vật liệu gốc
                gridImg.material = gridMat;
            }
            gridMat.SetVector("_GridTop", gridTop);
            gridMat.SetVector("_Cell", new Vector4(CW, CH, 0, 0));
            gridMat.SetVector("_Size", world.rect.size);
            gridMat.SetFloat("_Grid", C.grid);
            gridMat.SetFloat("_Lot", C.lot);
            gridMat.SetFloat("_LotsSide", Home.LotsPerSide(C));
            gridFade = 0;
            gridMat.SetFloat("_Fade", 0);
            gridImg.enabled = false;
            gridImg.raycastTarget = false;
        }

        // ô rừng đã mở (lưới chỉ vẽ trên đất xây được)
        void GridLots(HomeState h)
        {
            if (!gridMat) return;
            int n = Home.LotsPerSide(C);
            for (int i = 0; i < gridLots.Length; i++) gridLots[i] = 0;
            foreach (var l in h.lots)
                if (l >= 0 && l < n * n && l < gridLots.Length) gridLots[l] = 1;
            gridMat.SetFloatArray("_Lots", gridLots);
        }

        // chân thoi công trình đang đặt / dời: chỗ, cỡ, xanh / đỏ
        void GridGhost(bool ok)
        {
            if (!gridMat) return;
            if (!ghost)
            {
                gridMat.SetVector("_Ghost", Vector4.zero);
                return;
            }
            gridMat.SetVector("_Ghost", new Vector4(ghostAt.x, ghostAt.y, Home.Def(D.Cfg, ghostDef).size, 1));
            gridMat.SetColor("_GhostCol", ok ? new Color(0.35f, 1f, 0.45f, 1) : new Color(1f, 0.32f, 0.28f, 1));
        }

        void FadeGrid(float dt)
        {
            if (!gridMat) return;
            float want = mode == Mode.Build ? 1 : 0;
            if (Mathf.Approximately(gridFade, want) && gridImg.enabled == want > 0) return;
            gridFade = Mathf.MoveTowards(gridFade, want, dt * 5);
            gridMat.SetFloat("_Fade", gridFade);
            gridImg.enabled = gridFade > 0.01f;
        }

        // Dùng khi nướng prefab (Editor).
        public void SetupChrome(CanvasGroup ui) => chrome = ui;

        // chuyến tàu qua mây (ShipVoyage) ẩn giao diện cố định trước khi chụp màn làm nền trôi (thế giới liền, giao diện không trôi theo),
        // hiện lại khi tàu cập bến; thế giới, quái, công trình không ẩn. fade: mờ dần 0,25 giây
        public override void Chrome(bool on, bool fade)
        {
            if (!chrome) return;
            if (chromeFade != null) StopCoroutine(chromeFade);
            chromeFade = null;
            chrome.blocksRaycasts = on;
            if (fade && isActiveAndEnabled) chromeFade = StartCoroutine(FadeChrome(on ? 1 : 0));
            else chrome.alpha = on ? 1 : 0;
        }

        System.Collections.IEnumerator FadeChrome(float to)
        {
            float from = chrome.alpha;
            for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
            {
                chrome.alpha = Mathf.Lerp(from, to, t / 0.25f);
                yield return null;
            }
            chrome.alpha = to;
            chromeFade = null;
        }

        // ---------- toạ độ ----------

        // góc trên của ô (gx, gy), px từ góc trên trái bản đồ (y xuống)
        Vector2 CellTop(float gx, float gy) => new Vector2(gridTop.x + (gx - gy) * CW / 2, gridTop.y + (gx + gy) * CH / 2);

        Vector2Int CellAt(Vector2 p)
        {
            float u = (p.x - gridTop.x) / (CW / 2), v = (p.y - gridTop.y) / (CH / 2);
            return new Vector2Int(Mathf.FloorToInt((u + v) / 2), Mathf.FloorToInt((v - u) / 2));
        }

        ArtMeta Meta(string id) => art.FirstOrDefault(a => a.id == id);

        // điểm bản đồ (px, y xuống) → toạ độ ô liên tục; và ngược lại toạ độ trong lớp vật (localPosition, gốc giữa lớp) của quái
        Vector2 CellF(Vector2 p)
        {
            float u = (p.x - gridTop.x) / (CW / 2), v = (p.y - gridTop.y) / (CH / 2);
            return new Vector2((u + v) / 2, (v - u) / 2);
        }

        Vector2 ToLocal(Vector2 m)
        {
            var r = objLayer.rect;
            return new Vector2(r.xMin + m.x, r.yMax - m.y);
        }

        Vector2 ToMap(Vector2 l)
        {
            var r = objLayer.rect;
            return new Vector2(l.x - r.xMin, r.yMax - l.y);
        }

        // ---------- vào màn ----------

        public override void Enter(object args)
        {
            if (!world) return;
            Chrome(true, false); // vào màn không qua chuyến tàu: giao diện hiện sẵn (chuyến tàu tự ẩn rồi hiện lại)
            InitGrid();
            var s = S;
            Home.Tick(s, D, Now);
            App.Save.Save();
            btnBuild.SetOnClick(() => SetMode(mode == Mode.Build ? Mode.Normal : Mode.Build));
            btnPaint.SetOnClick(() => SetMode(mode == Mode.Paint ? Mode.Normal : Mode.Paint));
            btnHarvest.SetOnClick(HarvestAll);
            btnSail.SetOnClick(() => App.Router.Go(SceneIds.Hub));
            tap.OnTap = OnTap;
            tap.OnPress = OnPress;
            tap.OnHold = OnHold;
            tap.OnGrabMove = OnGrabMove;
            tap.OnGrabEnd = OnGrabEnd;
            tap.pass = landView ? landView.gameObject : null; // kéo, chụm bản đồ: mặt đất chuyển cho LandView
            SetMode(Mode.Normal);
            petsPlaced = false;
            Render();
            if (s.home.cleared.Count > 0) ReportCleared(); // dọn xong lúc vắng
            // phủ kín màn (vành nhỏ để LandView dùng chế độ phủ kín): zoom ra nhẹ tới khi bản đồ vừa phủ màn, vào tối đa maxZoom
            if (landView) landView.Begin(world, world.rect.size, TopInset, BottomInset, new Vector4(2, 2, 2, 2));
            FocusOn(Home.Main(s.home));
            focusWait = 3;
            focusView = Vector2.zero;
            shipArriving = false;
            if (pier)
            {
                // chuyến tàu qua mây (ShipVoyage) gọi lúc tàu sắp vào bến: đặt máy ngay theo tàu, bỏ lượt đặt máy vào Nhà chính
                pier.Frame = (p, w) =>
                {
                    focusWait = 0;
                    shipArriving = true;
                    shipSeenBusy = false;
                    shipDockedAt = -1;
                    if (!landView || !landView.On) return;
                    // đặt máy NGAY (chuyến tàu chụp màn ở khung sau): tính nốt đổi cỡ khung còn chờ, zoom 1 quanh tàu, rồi dời cho tàu ra đúng w
                    landView.Sync();
                    var lp = world.InverseTransformPoint(p.position);
                    landView.Show(new Vector2(lp.x, -lp.y), 1f, 0);
                    landView.ShiftWorld(w - p.position);
                };
                pier.Glide = GlideTo;
                pier.OnTap = () => App.Router.Go(SceneIds.Hub);
            }
        }

        // máy lướt tới điểm p (con của lớp kéo), chờ xong: tàu rời bến về đảo
        System.Collections.IEnumerator GlideTo(RectTransform p)
        {
            if (!landView || !landView.On || !p) yield break;
            var lp = world.InverseTransformPoint(p.position); // lớp kéo neo trên trái: y local âm đi xuống
            landView.Show(new Vector2(lp.x, -lp.y), landView.Zoom, 0.6f);
            yield return new WaitForSecondsRealtime(0.65f);
        }

        public override void Exit()
        {
            if (landView) landView.End();
        }

        public override void Refresh() => Render();

        void FocusOn(HomeBuilding b)
        {
            if (b == null || !landView) return;
            var n = Home.Def(D.Cfg, b.def).size;
            landView.Show(CellTop(b.gx + n / 2f, b.gy + n / 2f), 1f, 0);
        }

        void Update()
        {
            if (!world || App.I == null || App.Save?.Data == null || App.Data == null) return; // chưa khởi động xong hoặc đang dừng Play
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.1f);
            clock += dt;
            FadeGrid(dt);
            if (shipArriving && pier)
            {
                if (pier.Busy)
                {
                    shipSeenBusy = true;
                    shipDockedAt = -1;
                }
                else if (shipSeenBusy && shipDockedAt < 0) shipDockedAt = Time.unscaledTime;
                else if (shipSeenBusy && Time.unscaledTime - shipDockedAt >= 0.4f) // tàu đứng yên 0,4 giây rồi mới lướt
                {
                    shipArriving = false;
                    // chỉ lần đầu tới Nhà máy mới lướt lên Nhà chính; từ lần thứ hai máy đứng ở bến, người chơi tự kéo (người dùng 2026-11-19)
                    var m = S.home.dockIntro ? null : Home.Main(S.home);
                    if (m != null)
                    {
                        S.home.dockIntro = true;
                        App.Save.Save();
                    }
                    if (m != null && landView && landView.On)
                    {
                        int n = Home.Def(D.Cfg, m.def).size;
                        landView.Show(CellTop(m.gx + n / 2f, m.gy + n / 2f), 1f, 1.1f); // tàu cập bến xong: lướt lên Nhà chính
                    }
                }
            }
            if (focusWait > 0 && landView && landView.On)
            {
                var v = landView.ViewSize;
                if (v.x <= 0 || v != focusView)
                {
                    focusView = v;
                    focusWait = 3;
                }
                else if (--focusWait == 0) FocusOn(Home.Main(S.home));
            }
            NightLights();
            if (pets.Count > 0 && (sortTimer += dt) > 0.12f)
            {
                sortTimer = 0;
                SortAll(); // quái đi lại: chỉnh thứ tự vẽ với cây, công trình
            }
            if ((timer += dt) < 1f) return;
            timer = 0;
            Home.Tick(S, D, Now);
            if (S.home.cleared.Count > 0) ReportCleared();
            Labels();
            SyncPets(S.home); // hết ca, hết nghỉ
        }

        // ô rừng dọn xong (lúc đang xem hoặc lúc vắng): cây biến mất, báo bi để thả (bi, gỗ đã cộng trong bản lưu)
        void ReportCleared()
        {
            var h = S.home;
            int balls = h.cleared.Sum(lot => Home.RingOf(C, lot)?.balls ?? 0);
            int n = h.cleared.Count;
            h.cleared.Clear();
            App.Save.Save();
            Render();
            App.Bars.Refresh();
            App.Audio.Play("coin");
            string what = n > 1 ? $"Đã dọn {n} ô rừng" : "Đã dọn rừng";
            App.Toasts.Show(balls > 0 ? $"{what}: +{balls} bi để thả" : what, Icon("ball"));
        }

        // ---------- dựng ----------

        void Render()
        {
            var s = S;
            var d = D;
            var h = Home.Of(s, d, Now);
            res.text = $"Gỗ {Mathf.FloorToInt((float)h.wood)}/{Home.WoodCap(h, d.Cfg):0}   Quặng {Mathf.FloorToInt((float)h.ore)}/{Home.OreCap(h, d.Cfg):0}   " +
                       $"Bánh {h.bread}   Nhà cấp {Home.Level(h)}   Tướng {Home.UsedSlots(h)}/{Home.TotalSlots(h, C)}";
            RenderTiles(h);
            RenderForests(h);
            RenderBuildings(h);
            GridLots(h);
            SyncPets(h);
            Sort();
            Labels();
        }

        // ô lát nối liền theo hàng xóm (học Clash of Critters): nền ô, rồi mép giữa hai loại do loại thấp vẽ môi của loại cao chờm vào mình
        // (cỏ > đường đá > cát > đất > nước), góc trong có tuýp, mép xa (-tx, -ty) của ô nước thấy vách bờ đất
        static readonly string[] Prio = { "water", "dirt", "sand", "stone", "grass" };

        static int PrioOf(string t)
        {
            int i = Array.IndexOf(Prio, t ?? "grass");
            return i < 0 ? Prio.Length - 1 : i;
        }

        Sprite TileSp(string id)
        {
            tileMap ??= (tileArt ?? new NamedSprite[0]).Where(t => t.sprite).GroupBy(t => t.id).ToDictionary(g => g.Key, g => g.First().sprite);
            return tileMap.TryGetValue(id, out var sp) ? sp : null;
        }

        void RenderTiles(HomeState h)
        {
            var c = C;
            int n = Home.TilesPerSide(c);
            string sig = string.Join(",", h.tiles.OrderBy(kv => kv.Key).Select(kv => kv.Key + kv.Value));
            if (sig == tileSig) return;
            tileSig = sig;
            foreach (var im in tileImgs) Destroy(im.gameObject);
            tileImgs.Clear();
            string T(int x, int y) => Home.TileAt(h, c, x, y) ?? "grass";
            var keys = h.tiles.Keys.OrderBy(k => k / n + k % n).ToList();
            foreach (var k in keys) AddTile("fill_" + h.tiles[k], k / n, k % n);
            foreach (var k in keys)
            {
                int x = k / n, y = k % n;
                string t = h.tiles[k];
                if (t == "water")
                    for (int e = 2; e <= 3; e++)
                        if (T(x + Home.Around[e].dx, y + Home.Around[e].dy) != "water") AddTile("bank_" + e, x, y);
                for (int e = 0; e < 4; e++)
                {
                    var nb = T(x + Home.Around[e].dx, y + Home.Around[e].dy);
                    if (nb != t && PrioOf(nb) > PrioOf(t)) AddTile($"lip_{nb}_{e}", x, y);
                }
                for (int q = 0; q < 4; q++)
                {
                    var n1 = T(x + Home.Around[q].dx, y + Home.Around[q].dy);
                    var n2 = T(x + Home.Around[(q + 1) % 4].dx, y + Home.Around[(q + 1) % 4].dy);
                    var dg = T(x + Home.Around[4 + q].dx, y + Home.Around[4 + q].dy);
                    if (n1 == t && n2 == t && dg != t && PrioOf(dg) > PrioOf(t)) AddTile($"cor_{dg}_{q}", x, y);
                }
            }
        }

        // ảnh ô lát 224 x 128: chân thoi 192 x 96 (2 x 2 ô lưới) đặt giữa, góc trên ở (112, 16)
        void AddTile(string name, int tx, int ty)
        {
            var sp = TileSp(name);
            if (!sp) return;
            var img = Ui.Spawn(tilePrefab, tileLayer);
            Theme.SetSprite(img, sp);
            img.color = Color.white;
            img.raycastTarget = false;
            float k = C.tile * CW / 192f;
            var top = CellTop(tx * C.tile, ty * C.tile);
            var rt = img.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = new Vector2(0.5f, 1 - 16f / 128f);
            rt.sizeDelta = new Vector2(224 * k, 128 * k);
            rt.anchoredPosition = new Vector2(top.x, -top.y);
            tileImgs.Add(img);
        }

        // rừng trên ô chưa mở: khoảng 16 cây rời rải theo lưới lệch ngẫu nhiên (hạt giống theo ô, lần nào cũng như nhau) + vài bụi, đá,
        // gốc cây; ô sát biển có cọ, thỉnh thoảng có cây đặc biệt (anh đào, cổ thụ). Cùng một atlas nên vẽ chung một lượt.
        void RenderForests(HomeState h)
        {
            var c = C;
            int n = Home.LotsPerSide(c);
            if (!forestTrees.ContainsKey(RimKey)) SpawnRim();
            for (int lot = 0; lot < n * n; lot++)
            {
                bool locked = !h.lots.Contains(lot) && Home.LotKind(c, lot) != "hill";
                if (!locked)
                {
                    if (forestTrees.TryGetValue(lot, out var old))
                    {
                        foreach (var (img, _) in old) Destroy(img.gameObject);
                        forestTrees.Remove(lot);
                    }
                    if (forests.TryGetValue(lot, out var mk))
                    {
                        Destroy(mk.gameObject);
                        forests.Remove(lot);
                    }
                    continue;
                }
                if (!forestTrees.ContainsKey(lot)) SpawnForest(lot);
                // ô chưa mở: cây tối nhẹ (người dùng dặn 2026-11-18); đang dọn thì mờ thêm
                var col = LockedTint;
                if (h.clearing.ContainsKey(lot)) col.a = 0.7f;
                foreach (var (img, _) in forestTrees[lot]) img.color = col;
            }
        }

        static readonly Color LockedTint = new Color(0.8f, 0.82f, 0.78f, 1f);

        void SpawnForest(int lot)
        {
            var c = C;
            int n = Home.LotsPerSide(c), L = c.lot;
            var (i, j) = Home.LotIJ(c, lot);
            var rnd = new System.Random(lot * 7919 + 17);
            float R(float lo, float hi) => lo + (float)rnd.NextDouble() * (hi - lo);
            bool beach = i == n - 1 || j == n - 1;
            var art = treeArt ?? new TreeArt[0];
            var tall = art.Where(t => t.group == "tall" && t.sprite).ToArray();
            var special = art.Where(t => t.group == "special" && t.sprite).ToArray();
            var palm = art.Where(t => t.group == "palm" && t.sprite).ToArray();
            var small = art.Where(t => t.group == "small" && t.sprite).ToArray();
            var list = new List<(Image, float)>();
            forestTrees[lot] = list;
            // mốc nhãn của ô (vô hình)
            var mk = Ui.Spawn(objPrefab, objLayer);
            mk.Id = -2 - lot;
            mk.Place(null, new Vector2(1, 1), new Vector2(0.5f, 0), CellTop(i * L + L / 2f, j * L + L / 2f));
            mk.Img.enabled = false;
            forests[lot] = mk;
            if (tall.Length == 0) return;
            // lưới cây cách 2 ô (ô rừng 12 x 12: 6 x 6 cây) lệch ngẫu nhiên, thêm đồ nhỏ theo diện tích
            int k2 = Mathf.Max(1, L / 2);
            for (int a = 0; a < k2; a++)
            for (int b = 0; b < k2; b++)
            {
                float gx = i * L + 1 + a * 2 + R(-0.7f, 0.7f), gy = j * L + 1 + b * 2 + R(-0.7f, 0.7f);
                double roll = rnd.NextDouble();
                var pool = beach && palm.Length > 0 && roll < 0.22 ? palm : special.Length > 0 && roll > 0.93 ? special : tall;
                AddTree(pool[rnd.Next(pool.Length)], gx, gy, R(0.9f, 1.15f), rnd.Next(2) == 0, list);
            }
            int smallN = Mathf.RoundToInt(3f * L * L / 64f);
            for (int k = 0; k < smallN && small.Length > 0; k++)
                AddTree(small[rnd.Next(small.Length)], i * L + R(0.6f, L - 0.6f), j * L + R(0.6f, L - 0.6f), R(0.85f, 1.1f), rnd.Next(2) == 0, list);
        }

        const int RimKey = -1000; // khoá của rìa rừng trong forestTrees (ô rừng là 0..35)

        // rìa rừng ngoài hai cạnh trên của lưới: một dải cây rời sâu 6 ô nối ô rừng với rừng vẽ sẵn trên ảnh nền, không mở được
        void SpawnRim()
        {
            var c = C;
            var art = treeArt ?? new TreeArt[0];
            var tall = art.Where(t => t.group == "tall" && t.sprite).ToArray();
            var list = new List<(Image, float)>();
            forestTrees[RimKey] = list;
            if (tall.Length == 0) return;
            var rnd = new System.Random(4241);
            float R(float lo, float hi) => lo + (float)rnd.NextDouble() * (hi - lo);
            const int Depth = 6;
            var size = world.rect.size;
            for (float gx = -Depth + 1; gx < c.grid; gx += 2.2f)
            for (float gy = -Depth + 1; gy < c.grid; gy += 2.2f)
            {
                if (gx >= 0 && gy >= 0) continue; // trong lưới
                float x = gx + R(-0.7f, 0.7f), y = gy + R(-0.7f, 0.7f);
                var p = CellTop(x, y);
                if (p.x < -80 || p.x > size.x + 80 || p.y < 30) continue;
                AddTree(tall[rnd.Next(tall.Length)], x, y, R(0.9f, 1.15f), rnd.Next(2) == 0, list);
            }
            foreach (var (img, _) in list) img.color = LockedTint;
        }

        void AddTree(TreeArt t, float gx, float gy, float sc, bool flip, List<(Image, float)> list)
        {
            if (gx > C.grid - 4 && gy > C.grid - 4) return; // bến ở mũi dưới: không cho cây mọc đè
            var img = Ui.Spawn(treePrefab, objLayer);
            Theme.SetSprite(img, t.sprite);
            img.raycastTarget = false;
            var p = CellTop(gx, gy);
            var rt = img.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = t.pivot;
            rt.sizeDelta = t.sprite.rect.size * TreeScale * sc;
            rt.localScale = new Vector3(flip ? -1 : 1, 1, 1);
            rt.anchoredPosition = new Vector2(p.x, -p.y);
            list.Add((img, p.y));
        }

        void RenderBuildings(HomeState h)
        {
            var cfg = D.Cfg;
            foreach (var id in objs.Keys.Where(id => h.buildings.All(b => b.id != id)).ToList())
            {
                Destroy(objs[id].gameObject);
                objs.Remove(id);
            }
            foreach (var b in h.buildings)
            {
                var df = Home.Def(cfg, b.def);
                var m = Meta("home_b_" + b.def);
                if (!objs.TryGetValue(b.id, out var o))
                {
                    o = Ui.Spawn(objPrefab, objLayer);
                    o.Id = b.id;
                    objs[b.id] = o;
                }
                PlaceObject(o, df, m, b.gx, b.gy);
                o.Img.raycastTarget = false;
                o.Tint(b.job == 1 ? new Color(1, 1, 1, 0.6f) : Color.white);
            }
        }

        void PlaceObject(HomeObject o, HomeBuildingDef df, ArtMeta m, int gx, int gy)
        {
            var bottom = CellTop(gx + df.size, gy + df.size);
            if (m.sprite)
            {
                float k = df.size * CW / Mathf.Max(1, m.foot);
                o.Place(m.sprite, m.sprite.rect.size * k, m.pivot, bottom);
            }
            else o.Place(null, new Vector2(df.size * CW, df.size * CH), new Vector2(0.5f, 0), bottom); // chưa có ảnh: chân thoi trắng
        }

        // xa (y góc dưới nhỏ) vẽ trước; mốc nhãn ô rừng, quái đang kéo và bóng ma luôn trên cùng. Chỉ dời con nào lệch chỗ (lớp vật có
        // hơn nghìn cây: dời hết mỗi lần thì chậm)
        void Sort() => SortAll();

        void SortAll()
        {
            order.Clear();
            foreach (var o in objs.Values) order.Add((o.transform, o.Depth));
            foreach (var kv in forestTrees)
                foreach (var (img, d) in kv.Value) order.Add((img.transform, d));
            foreach (var m in forests.Values) order.Add((m.transform, float.MaxValue / 2));
            foreach (var p in pets.Values) order.Add((p.transform, PetDepth(p)));
            if (ghost) order.Add((ghost.transform, float.MaxValue));
            order.Sort((a, b) => a.d.CompareTo(b.d));
            for (int i = 0; i < order.Count; i++)
                if (i >= objLayer.childCount || objLayer.GetChild(i) != order[i].t) order[i].t.SetSiblingIndex(i);
        }

        // y chân quái; đứng trước mặt tường của công trình (ngoài cạnh gx + n hoặc gy + n) mà chồng lên hình thì vẽ sau công trình
        float PetDepth(FarmPet p)
        {
            if (p.State == FarmPet.Mode.Drag) return float.MaxValue / 4;
            var m = ToMap(p.Pos);
            float d = m.y;
            var cell = CellF(m);
            foreach (var b in S.home.buildings)
            {
                if (!objs.TryGetValue(b.id, out var o) || !o.gameObject.activeSelf || d >= o.Depth) continue;
                int n = Home.Def(D.Cfg, b.def).size;
                if (cell.x < b.gx + n && cell.y < b.gy + n) continue; // sau lưng công trình
                float x0 = CellTop(b.gx, b.gy + n).x - 40, x1 = CellTop(b.gx + n, b.gy).x + 40;
                if (m.x > x0 && m.x < x1) d = Mathf.Max(d, o.Depth + 0.5f);
            }
            return d;
        }

        // nhãn trên đầu: đang xây / nâng cấp (giờ còn), đồ đầy kho; ô rừng đang dọn
        void Labels()
        {
            var s = S;
            var h = s.home;
            if (h == null) return;
            double now = Now;
            foreach (var b in h.buildings)
            {
                if (!objs.TryGetValue(b.id, out var o)) continue;
                string text = b.job != 0 ? $"{(b.job == 1 ? "Xây" : "Lên cấp")} {Clock((b.until - now) / 60000)}" : null;
                o.Label(text);
                o.Bubble(Home.Stock(b) > 0 ? Icon(OutIcon(Home.Def(D.Cfg, b.def).output)) : null);
            }
            foreach (var kv in forests)
                kv.Value.Label(h.clearing.TryGetValue(kv.Key, out var until) ? "Dọn " + Clock((until - now) / 60000) : null);
            if (selBuilding >= 0 || selLot >= 0) RefreshPanel();
        }

        static string OutIcon(string output) => output switch
        {
            "balls" => "ball",
            "wood" => "leaf",
            "ore" => "rock",
            "fish" => "wave",
            "stones" => "gem",
            "bread" => "flame",
            _ => "info",
        };

        static string Clock(double minutes)
        {
            int m = (int)Math.Ceiling(Math.Max(0, minutes));
            return m >= 60 ? $"{m / 60}g{m % 60:00}" : $"{m}p";
        }

        // ---------- mây che rìa ----------
        // Từng đám mây rời dựng sẵn trong prefab (menu dựng màn, lớp "may"), CloudRing của phiên sảnh lo trôi nhẹ và toả quanh tàu
        // (PierShip.Active); chuyến tàu qua mây mang các đám này sang dải mây lúc chụp màn. Màn không dời mây nữa.

        // đèn công trình khi trời tối (DayCycle dùng chung với các đảo): quầng ấm ở cửa sổ, lò
        static readonly Dictionary<string, Vector2> LampAt = new Dictionary<string, Vector2>
        {
            ["main"] = new Vector2(0.0f, 0.45f), ["kitchen"] = new Vector2(-0.1f, 0.35f), ["forge"] = new Vector2(-0.1f, 0.3f),
            ["storage"] = new Vector2(0.15f, 0.35f), ["waterwheel"] = new Vector2(0.1f, 0.4f), ["mine"] = new Vector2(-0.12f, 0.28f),
        };

        void NightLights()
        {
            if (!glowPrefab || !glowSprite || S.home == null) return;
            float night = DayCycle.Night(DayCycle.Hour);
            var h = S.home;
            // khớp số đèn với công trình có đèn
            var want = h.buildings.Where(b => LampAt.ContainsKey(b.def) && b.job != 1 && objs.ContainsKey(b.id)).ToList();
            if (want.Count != lights.Count || want.Where((b, i) => lights[i].id != b.id).Any())
            {
                foreach (var l in lights) Destroy(l.img.gameObject);
                lights.Clear();
                foreach (var b in want)
                {
                    var img = Ui.Spawn(glowPrefab, lightLayer);
                    Theme.SetSprite(img, glowSprite);
                    img.raycastTarget = false;
                    lights.Add((img, b.id));
                }
            }
            for (int i = 0; i < lights.Count; i++)
            {
                var (img, id) = lights[i];
                var o = objs[id];
                var b = want[i];
                var off = LampAt[b.def];
                var rt = img.rectTransform;
                var ort = o.Rt;
                float w = ort.sizeDelta.x;
                rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(w * 0.5f, w * 0.5f);
                rt.anchoredPosition = ort.anchoredPosition + new Vector2(off.x * w, off.y * ort.sizeDelta.y);
                float a = night * (0.7f + 0.3f * Mathf.Sin(clock * 3.1f + id));
                img.enabled = a > 0.02f;
                img.color = new Color(1, 0.85f, 0.5f, a);
            }
        }

        // ---------- chế độ ----------

        void SetMode(Mode m)
        {
            mode = m;
            if (m != Mode.Build) EndGhost();
            selBuilding = selLot = -1;
            panel.gameObject.SetActive(false);
            btnBuild.SetText(m == Mode.Build ? "Xong" : "Xây");
            btnPaint.SetText(m == Mode.Paint ? "Xong" : "Lát ô");
            hint.text = m == Mode.Build ? "Chọn công trình ở khay để xây, hoặc chạm / nhấn giữ công trình trên đảo để dời; kéo hoặc chạm đất để đổi chỗ, rồi bấm Đặt."
                : m == Mode.Paint ? "Chọn loại ô, chạm đất để lát. Cỏ để xoá."
                : "Kéo quái đang dạo thả vào công trình để giao việc, hoặc chạm công trình để chọn tướng. Nhấn giữ công trình để dời.";
            BuildTray();
        }

        void BuildTray()
        {
            for (int i = tray.childCount - 1; i >= 0; i--) Destroy(tray.GetChild(i).gameObject);
            tray.gameObject.SetActive(mode != Mode.Normal);
            if (mode == Mode.Build)
            {
                foreach (var df in C.buildings.Where(b => b.kind != "main" && b.kind != "tree"))
                {
                    var e = Home.CanBuild(S, D, df.id);
                    if (e == HomeErr.NotFound) continue;
                    if (df.reward && e == HomeErr.Locked) continue; // trang trí thưởng chưa có
                    var (w, o, _, _) = Home.BuildCost(df);
                    var btn = Ui.Spawn(trayPrefab, tray);
                    string cost = (w > 0 ? $"{w} gỗ" : "") + (o > 0 ? $" {o} quặng" : "");
                    btn.SetText($"{df.name}\n{(e == HomeErr.Ok ? cost : Why(e, df))}");
                    btn.Interactable = e == HomeErr.Ok;
                    var id = df.id;
                    btn.SetOnClick(() => StartGhost(id));
                }
            }
            else if (mode == Mode.Paint)
            {
                foreach (var t in new[] { new HomeTileDef { id = "grass", name = "Cỏ" } }.Concat(C.tiles))
                {
                    var btn = Ui.Spawn(trayPrefab, tray);
                    btn.SetText($"{t.name}{(t.id == paintTile ? " ✓" : "")}\n{(t.wood > 0 ? t.wood + " gỗ" : "")}{(t.ore > 0 ? $" {t.ore} quặng" : "")}");
                    var id = t.id;
                    btn.SetOnClick(() =>
                    {
                        paintTile = id;
                        BuildTray();
                    });
                }
            }
        }

        static string Why(HomeErr e, HomeBuildingDef df) => e switch
        {
            HomeErr.HomeLevel => $"Nhà cấp {df.home}",
            HomeErr.Count => "Đủ số",
            HomeErr.Cost => "Thiếu gỗ",
            HomeErr.Builder => "Thợ bận",
            HomeErr.Locked => "Chưa có",
            _ => "",
        };

        void StartGhost(string def)
        {
            var pos = Home.FindSpot(S, D, def);
            if (pos == null)
            {
                App.Toasts.Show("Hết chỗ trống: dọn thêm rừng", Icon("lock"));
                return;
            }
            EndGhost();
            ghost = Ui.Spawn(objPrefab, objLayer);
            ghostDef = def;
            ghostAt = new Vector2Int(pos.Value.gx, pos.Value.gy);
            UpdateGhost();
            var df = Home.Def(D.Cfg, def);
            tray.gameObject.SetActive(false);
            KeepVisible(CellTop(ghostAt.x + df.size / 2f, ghostAt.y + df.size / 2f));
            ShowPanel(df.name, BuildText(df), ("Đặt", PlaceGhost), ("Thôi", CancelGhost), (null, null));
        }

        // dời công trình (người dùng dặn 2026-11-18, như Clash of Critters): ở chế độ xây chạm công trình để nhấc lên; bóng ma xanh / đỏ thay
        // chỗ nó, chạm đất để đổi chỗ, Đặt thì dời (không tốn gì, tướng, đồ tích, giờ xây vẫn giữ), Thôi thì về chỗ cũ
        void StartMove(HomeBuilding b, bool pan = true)
        {
            if (mode != Mode.Build) SetMode(Mode.Build);
            EndGhost();
            moveId = b.id;
            if (objs.TryGetValue(b.id, out var o)) o.gameObject.SetActive(false);
            ghost = Ui.Spawn(objPrefab, objLayer);
            ghostDef = b.def;
            ghostAt = new Vector2Int(b.gx, b.gy);
            UpdateGhost();
            var df = Home.Def(D.Cfg, b.def);
            tray.gameObject.SetActive(false); // khay che nửa màn: ẩn khi đang dời
            if (pan) KeepVisible(CellTop(b.gx + df.size / 2f, b.gy + df.size / 2f));
            App.Audio.Play("click");
            ShowPanel($"Dời {df.name}", MoveText, ("Đặt", PlaceGhost), ("Thôi", CancelGhost), (null, null));
        }

        // điểm bản đồ đang bị bảng chọn (nửa dưới) hoặc thanh trên che thì kéo máy cho nó ra giữa khung
        void KeepVisible(Vector2 mapPt)
        {
            if (!landView || !landView.On) return;
            var v = landView.ToView(mapPt);
            var size = landView.ViewSize;
            if (v.y > size.y * 0.58f || v.y < TopInset + 80 || v.x < 60 || v.x > size.x - 60) landView.Show(mapPt, landView.Zoom, 0.3f);
        }

        const string MoveText = "Nhấn giữ rồi kéo công trình, hoặc chạm đất để chọn chỗ mới (xanh là đặt được), rồi bấm Đặt.";

        // ---------- nhấn giữ, kéo (HomeTap) ----------

        // nhấn xuống trúng bóng ma đang xây / dời: cầm lên kéo luôn
        bool OnPress(Vector2 p)
        {
            if (!ghost || mode != Mode.Build) return false;
            var cell = CellAt(p);
            int n = Home.Def(D.Cfg, ghostDef).size;
            if (cell.x < ghostAt.x || cell.y < ghostAt.y || cell.x >= ghostAt.x + n || cell.y >= ghostAt.y + n) return false;
            grabOffset = cell - ghostAt;
            UpdateGhost();
            return true;
        }

        // giữ yên trên công trình (chế độ thường hoặc xây): nhấc lên, cùng ngón kéo đi
        bool OnHold(Vector2 p)
        {
            if (mode == Mode.Paint) return false;
            var cell = CellAt(p);
            if (!Home.InMap(C, cell.x, cell.y)) return false;
            var b = Home.At(S.home, D.Cfg, cell.x, cell.y);
            if (b == null || b.id == moveId) return false;
            StartMove(b, false);
            grabOffset = cell - new Vector2Int(b.gx, b.gy);
            UpdateGhost();
            Haptics.Play(Haptic.CardTap);
            return true;
        }

        void OnGrabMove(Vector2 p)
        {
            if (!ghost) return;
            var at = CellAt(p) - grabOffset;
            if (at == ghostAt) return;
            ghostAt = at;
            UpdateGhost();
            Haptics.Play(Haptic.Peg, 0.4f);
        }

        void OnGrabEnd(Vector2 p)
        {
            if (!ghost) return;
            UpdateGhost(); // hạ xuống
            var e = Home.CanPlace(S, D, ghostDef, ghostAt.x, ghostAt.y, moveId);
            panelBody.text = (moveId >= 0 ? MoveText : BuildText(Home.Def(D.Cfg, ghostDef))) + (e == HomeErr.Ok ? "" : $"\nChỗ này chưa đặt được: {ErrText(e)}.");
        }

        void CancelGhost()
        {
            EndGhost();
            panel.gameObject.SetActive(false);
        }

        // bỏ bóng ma; đang dời thì hiện lại công trình ở chỗ cũ
        void EndGhost()
        {
            if (ghost) Destroy(ghost.gameObject);
            ghost = null;
            ghostDef = null;
            GridGhost(false);
            if (moveId >= 0 && objs.TryGetValue(moveId, out var o) && o) o.gameObject.SetActive(true);
            moveId = -1;
            if (tray) tray.gameObject.SetActive(mode != Mode.Normal);
        }

        string BuildText(HomeBuildingDef df)
        {
            var (w, o, _, min) = Home.BuildCost(df);
            string what = df.kind == "prod" ? $"Làm ra: {OutName(df.output)}. Hợp hệ {Elements.Name(df.elem)}." : df.kind == "support" ? Support(df) : $"Điểm đẹp +{df.beauty}.";
            return $"{what}\nGiá: {w} gỗ{(o > 0 ? $", {o} quặng" : "")}{(min > 0 ? $", {Clock(min)}" : "")}. Cỡ {df.size}x{df.size}.";
        }

        static string Support(HomeBuildingDef df) => df.id switch
        {
            "storage" => "Thêm sức chứa gỗ, quặng.",
            "well" => "Tưới ruộng, vườn quanh giếng.",
            "waterwheel" => "Tưới rộng; phải sát suối.",
            "hotspring" => "Tướng nghỉ nhanh hơn.",
            _ => "",
        };

        static string OutName(string o) => o switch
        {
            "balls" => "bi",
            "wood" => "gỗ",
            "ore" => "quặng, ít đá tiến hóa",
            "fish" => "câu cá: bi, thẻ, cúp",
            "stones" => "đá tiềm năng (ăn quặng)",
            "bread" => "bánh (tướng ăn thì hết nghỉ)",
            _ => o,
        };

        void UpdateGhost()
        {
            if (!ghost) return;
            var df = Home.Def(D.Cfg, ghostDef);
            PlaceObject(ghost, df, Meta("home_b_" + ghostDef), ghostAt.x, ghostAt.y);
            bool ok = Home.CanPlace(S, D, ghostDef, ghostAt.x, ghostAt.y, moveId) == HomeErr.Ok;
            ghost.Tint(ok ? new Color(0.75f, 1f, 0.75f, 0.85f) : new Color(1f, 0.6f, 0.6f, 0.85f));
            GridGhost(ok);
            ghost.Img.raycastTarget = false;
            ghost.Label(null);
            ghost.Bubble(null);
            if (tap && tap.Grabbing) ghost.Rt.anchoredPosition += new Vector2(0, 18); // đang cầm: nhấc lên một chút
            Sort();
        }

        void PlaceGhost()
        {
            var e = moveId >= 0 ? Home.Move(S, D, moveId, ghostAt.x, ghostAt.y) : Home.Build(S, D, Now, ghostDef, ghostAt.x, ghostAt.y);
            if (e != HomeErr.Ok)
            {
                App.Audio.Play("error");
                App.Toasts.Show(ErrText(e), Icon("lock"));
                return;
            }
            App.Audio.Play("click");
            EndGhost();
            panel.gameObject.SetActive(false);
            App.Save.Save();
            Render();
            BuildTray();
        }

        static string ErrText(HomeErr e) => e switch
        {
            HomeErr.Overlap => "Chồng lên công trình khác",
            HomeErr.Locked => "Ô rừng chưa dọn",
            HomeErr.Blocked => "Chỗ này không xây được",
            HomeErr.NeedOre => "Mỏ phải đặt trên mạch quặng",
            HomeErr.NeedStream => "Cối nước phải sát suối",
            HomeErr.OutOfMap => "Ra ngoài đảo",
            HomeErr.Cost => "Thiếu gỗ hoặc quặng",
            HomeErr.Builder => "Đội thợ đang bận",
            HomeErr.HomeLevel => "Cần nâng Nhà chính",
            HomeErr.PlayerLevel => "Cần lên cấp",
            HomeErr.Count => "Đã đủ số công trình loại này",
            HomeErr.MaxLevel => "Đã tối đa",
            HomeErr.NotAdjacent => "Phải kề đất đã mở",
            HomeErr.Busy => "Đang bận",
            HomeErr.TotalSlots => "Hết chỗ tướng (nâng Nhà chính)",
            HomeErr.BallSlots => "Hết chỗ ra bi (lên cấp)",
            HomeErr.HeroBusy => "Tướng đang bận",
            _ => e.ToString(),
        };

        // ---------- chạm ----------

        void OnTap(Vector2 p)
        {
            var cell = CellAt(p);
            var s = S;
            var d = D;
            if (mode == Mode.Build)
            {
                if (!ghost)
                {
                    var hit = Home.InMap(C, cell.x, cell.y) ? Home.At(s.home, d.Cfg, cell.x, cell.y) : null;
                    if (hit != null) StartMove(hit);
                    return;
                }
                var n = Home.Def(d.Cfg, ghostDef).size;
                ghostAt = new Vector2Int(cell.x - n / 2, cell.y - n / 2);
                UpdateGhost();
                return;
            }
            if (mode == Mode.Paint)
            {
                var e = Home.Paint(s, d, Mathf.FloorToInt(cell.x / (float)C.tile), Mathf.FloorToInt(cell.y / (float)C.tile), paintTile);
                if (e == HomeErr.Ok)
                {
                    App.Save.Save();
                    Render();
                }
                else if (e != HomeErr.Busy) App.Toasts.Show(ErrText(e), Icon("lock"));
                return;
            }
            if (!Home.InMap(C, cell.x, cell.y))
            {
                panel.gameObject.SetActive(false);
                return;
            }
            var b = Home.At(s.home, d.Cfg, cell.x, cell.y);
            if (b != null)
            {
                selBuilding = b.id;
                selLot = -1;
                App.Audio.Play("click");
                RefreshPanel();
                return;
            }
            int lot = Home.LotOfCell(C, cell.x, cell.y);
            if (!s.home.lots.Contains(lot) && Home.LotKind(C, lot) != "hill")
            {
                selLot = lot;
                selBuilding = -1;
                App.Audio.Play("click");
                RefreshPanel();
                return;
            }
            selBuilding = selLot = -1;
            panel.gameObject.SetActive(false);
        }

        void RefreshPanel()
        {
            var s = S;
            var d = D;
            var h = s.home;
            double now = Now;
            if (selLot >= 0)
            {
                if (h.clearing.TryGetValue(selLot, out var until))
                {
                    ShowPanel("Đang dọn rừng", $"Còn {Clock((until - now) / 60000)}.", ("Rút 30 phút", () => SpeedUp(-1, selLot)), (null, null), (null, null));
                    return;
                }
                var e = Home.CanClear(s, d, selLot);
                var (w, o, min) = Home.ClearCost(h, C, selLot);
                var ring = Home.RingOf(C, selLot);
                string need = ring == null ? "" : $"Cần Nhà cấp {ring.home}{(ring.player > 0 ? $", cấp {ring.player}" : "")}. ";
                ShowPanel("Ô rừng", $"{need}Giá {w} gỗ{(o > 0 ? $", {o} quặng" : "")}, {Clock(min)}. Dọn xong rơi {ring?.reward ?? 0} gỗ." +
                                    (e == HomeErr.Ok ? "" : $"\n{ErrText(e)}."),
                    (e == HomeErr.Ok ? "Dọn" : null, () => ClearLot(selLot)), (null, null), (null, null));
                return;
            }
            var b = Home.Find(h, selBuilding);
            if (b == null)
            {
                panel.gameObject.SetActive(false);
                return;
            }
            var df = Home.Def(d.Cfg, b.def);
            string title = $"{df.name}{(Home.IsDeco(df) ? "" : $" cấp {b.level}")}";
            var lines = new List<string>();
            if (b.job != 0) lines.Add($"{(b.job == 1 ? "Đang xây" : "Đang lên cấp")}: còn {Clock((b.until - now) / 60000)}.");
            if (df.kind == "prod")
            {
                lines.Add($"Làm ra {OutName(df.output)}. Có {Home.Stock(b)} chờ thu.");
                for (int i = 0; i < b.slots.Count; i++)
                {
                    var sl = b.slots[i];
                    lines.Add(sl.hero == null ? $"Ô {i + 1}: trống"
                        : $"Ô {i + 1}: {d.Hero(sl.hero)?.name}, {Home.Rate(s, d, sl.hero, b):0.#}/giờ, còn {Clock(sl.energy * 60)}");
                }
            }
            else if (df.kind == "support") lines.Add(Support(df));
            else if (df.kind == "tree") lines.Add("Cây bi ra bi theo giờ.");
            else if (df.kind == "main") lines.Add($"Gỗ {h.wood:0}/{Home.WoodCap(h, d.Cfg):0}, quặng {h.ore:0}/{Home.OreCap(h, d.Cfg):0}. Thợ {Home.Busy(h)}/{Home.Builders(h, C)}.");
            var up = Home.UpgradeCost(d.Cfg, b);
            var ue = Home.CanUpgrade(s, d, b.id);
            string upLabel = up == null ? null : $"Lên cấp {up.Value.wood} gỗ{(up.Value.ore > 0 ? $" {up.Value.ore} quặng" : "")}";
            if (up != null && ue != HomeErr.Ok && ue != HomeErr.Cost) lines.Add($"Lên cấp: {ErrText(ue)}.");
            bool prod = df.kind == "prod" && b.job != 1;
            // chỗ trống thì chọn tướng vào chỗ đó; đủ người thì đổi ca ô mệt nhất (hộp chọn tướng có nút rút ra)
            int empty = b.slots.FindIndex(sl => sl.hero == null);
            int tired = b.slots.Count == 0 ? -1 : b.slots.Select((sl, i) => (sl, i)).OrderBy(x => x.sl.energy).First().i;
            (string, Action) heroBtn = !prod ? (null, null)
                : empty >= 0 ? ("Giao tướng", () => Picker(b.id, empty))
                : tired >= 0 ? ("Đổi ca", () => Picker(b.id, tired)) : (null, null);
            (string, Action) third = b.job != 0 ? ("Rút 30 phút", () => SpeedUp(b.id, -1))
                : Home.IsDeco(df) ? ("Cất", () => StoreDeco(b.id)) : (upLabel, () => Upgrade(b.id));
            var bid = b.id;
            ShowPanel(title, string.Join("\n", lines), (prod ? "Thu" : null, () => Harvest(b.id)), heroBtn, third, ("Dời", () =>
            {
                var mb = Home.Find(S.home, bid);
                if (mb != null) StartMove(mb);
            }));
        }

        void ShowPanel(string title, string body, (string label, Action act) a, (string label, Action act) b, (string label, Action act) c,
            (string label, Action act) d = default)
        {
            panel.gameObject.SetActive(true);
            panelTitle.text = title;
            panelBody.text = body;
            void Bind(SketchButton btn, (string label, Action act) x)
            {
                btn.gameObject.SetActive(x.label != null);
                if (x.label == null) return;
                btn.SetText(x.label);
                btn.SetOnClick(x.act);
            }
            Bind(panelA, a);
            Bind(panelB, b);
            Bind(panelC, c);
            if (panelD) Bind(panelD, d);
        }

        // ---------- việc ----------

        void Done(HomeErr e)
        {
            if (e != HomeErr.Ok)
            {
                App.Audio.Play("error");
                App.Toasts.Show(ErrText(e), Icon("lock"));
                return;
            }
            App.Audio.Play("click");
            App.Save.Save();
            Render();
        }

        void ClearLot(int lot) => Done(Home.ClearLot(S, D, Now, lot));
        void Upgrade(int id) => Done(Home.Upgrade(S, D, Now, id));

        void StoreDeco(int id)
        {
            if (!Home.Store(S, D, id)) return;
            selBuilding = -1;
            panel.gameObject.SetActive(false);
            Done(HomeErr.Ok);
        }

        void SpeedUp(int id, int lot)
        {
            Ads.Show(AdGate.HomeSpeed, ok =>
            {
                if (!ok) return;
                Home.SpeedUp(S, D, Now, id, lot);
                Done(HomeErr.Ok);
            });
        }

        // hộp chọn tướng cho ô slot của công trình id (dùng lại hộp của Trang trại); người chơi tự chọn, không tự giao
        void Picker(int id, int slot)
        {
            if (!pickerPrefab) return;
            App.Modals.Open(pickerPrefab).ShowHome(id, slot, reopen =>
            {
                Render();
                if (reopen) Picker(id, slot);
            });
        }

        void Harvest(int id) => ShowYield(Home.Harvest(S, D, Now, id));

        void HarvestAll() => ShowYield(Home.HarvestAll(S, D, Now));

        void ShowYield(HomeYield y)
        {
            if (!y.Any)
            {
                App.Toasts.Show("Chưa có gì để thu", Icon("info"));
                return;
            }
            var parts = new List<string>();
            if (y.balls > 0) parts.Add($"+{y.balls} bi");
            if (y.wood > 0) parts.Add($"+{y.wood} gỗ");
            if (y.ore > 0) parts.Add($"+{y.ore} quặng");
            if (y.evo > 0) parts.Add($"+{y.evo} đá tiến hóa");
            if (y.stones > 0) parts.Add($"+{y.stones} đá tiềm năng");
            if (y.bread > 0) parts.Add($"+{y.bread} bánh");
            if (y.other.Count > 0) parts.Add($"+{y.other.Count} thưởng câu");
            if (y.deco.Count > 0) parts.Add("+cúp câu cá");
            App.Audio.Play("coin");
            App.Toasts.Show(string.Join(", ", parts), Icon("ball"));
            App.Save.Save();
            Render();
        }

        // ---------- quái (FarmPet; cảnh chủ IFarmPetHost) ----------

        // ô của quái làm việc: id công trình * 8 + ô tướng
        static int SpotOf(int id, int slot) => id * 8 + slot;

        // việc theo công trình → cử động, đồ nghề của FarmPet (veg cuốc, smithy búa, duck rắc, orchard hái, bakery nhào)
        string WorkKind(HomeBuilding b)
        {
            if (b == null) return null;
            return b.def switch
            {
                "field" => "veg",
                "orchard" => "orchard",
                "pond" => "duck",
                "kitchen" => "bakery",
                _ => "smithy", // xưởng gỗ, mỏ, lò rèn
            };
        }

        // chỗ đứng làm việc (px bản đồ): ô 0 ngoài mặt trái, ô 1 ngoài mặt phải, ô 2 ở mũi trước
        Vector2 SlotMap(HomeBuilding b, int slot)
        {
            int n = Home.Def(D.Cfg, b.def).size;
            return (slot % 3) switch
            {
                0 => CellTop(b.gx + n * 0.4f, b.gy + n + 0.7f),
                1 => CellTop(b.gx + n + 0.7f, b.gy + n * 0.4f),
                _ => CellTop(b.gx + n + 0.6f, b.gy + n + 0.6f),
            };
        }

        public float SpotFace(int spot) => spot < 0 ? 1 : (spot % 8) % 3 == 0 ? 1 : -1;

        // chỗ ngủ: dọc mặt trái Nhà chính
        Vector2 BedMap(int i)
        {
            var m = Home.Main(S.home);
            if (m == null) return CellTop(C.grid / 2f, C.grid / 2f);
            int n = Home.Def(D.Cfg, "main").size;
            return CellTop(m.gx + 0.8f + i * 1.3f, m.gy + n + 0.9f + (i % 2) * 0.5f);
        }

        bool WalkableAt(Vector2 cellF) => Home.Walkable(S.home, D.Cfg, Mathf.FloorToInt(cellF.x), Mathf.FloorToInt(cellF.y));

        bool LineClear(Vector2 a, Vector2 b)
        {
            float len = (b - a).magnitude;
            int steps = Mathf.Max(1, Mathf.CeilToInt(len / 0.4f));
            for (int i = 1; i <= steps; i++)
                if (!WalkableAt(Vector2.Lerp(a, b, i / (float)steps))) return false;
            return true;
        }

        // điểm đi chơi gần chỗ đứng: ô đi được trong bán kính 6 ô, đường thẳng không xuyên công trình, hồ, suối
        public Vector2 RoamPoint(Vector2 near)
        {
            var c0 = CellF(ToMap(near));
            for (int k = 0; k < 14; k++)
            {
                var a = UnityEngine.Random.insideUnitCircle * 6f;
                var to = c0 + a;
                if (!WalkableAt(to) || !LineClear(c0, to)) continue;
                return ToLocal(CellTop(to.x, to.y));
            }
            return near;
        }

        // thả ra chỗ không đi được (công trình, nước, rừng) thì về ô đi được gần nhất
        public Vector2 ClampMeadow(Vector2 pt)
        {
            var c0 = CellF(ToMap(pt));
            if (WalkableAt(c0)) return pt;
            int cx = Mathf.FloorToInt(c0.x), cy = Mathf.FloorToInt(c0.y);
            for (int r = 1; r < 24; r++)
            for (int x = cx - r; x <= cx + r; x++)
            for (int y = cy - r; y <= cy + r; y++)
            {
                if (Mathf.Max(Mathf.Abs(x - cx), Mathf.Abs(y - cy)) != r) continue;
                if (Home.Walkable(S.home, D.Cfg, x, y)) return ToLocal(CellTop(x + 0.5f, y + 0.5f));
            }
            return pt;
        }

        // chỗ thả quái lúc mới vào màn: rải khắp đất đã mở
        Vector2 RoamStart()
        {
            if (walkCells.Count == 0)
            {
                var c = C;
                for (int x = 0; x < c.grid; x++)
                for (int y = 0; y < c.grid; y++)
                    if (Home.Walkable(S.home, D.Cfg, x, y)) walkCells.Add(new Vector2Int(x, y));
            }
            if (walkCells.Count == 0) return ToLocal(BedMap(0));
            var cell = walkCells[UnityEngine.Random.Range(0, walkCells.Count)];
            return ToLocal(CellTop(cell.x + UnityEngine.Random.value, cell.y + UnityEngine.Random.value));
        }

        // mỗi tướng một con: đang làm đứng ở công trình, rảnh đi khắp đất đã mở, vừa rút ra thì ngủ cạnh Nhà chính
        void SyncPets(HomeState h)
        {
            if (!petPrefab || h == null) return;
            var s = S;
            var d = D;
            double now = Now;
            walkCells.Clear();
            var want = new Dictionary<string, (FarmPet.Mode mode, int spot)>();
            foreach (var b in h.buildings)
                for (int i = 0; i < b.slots.Count; i++)
                    if (b.slots[i].hero != null && b.job != 1 && !want.ContainsKey(b.slots[i].hero))
                        want[b.slots[i].hero] = (b.slots[i].energy > 0 ? FarmPet.Mode.Work : FarmPet.Mode.Tired, SpotOf(b.id, i));
            var owned = d.Heroes.Where(x => s.Hero(x.id) != null && s.Hero(x.id).owned && !want.ContainsKey(x.id)).ToList();
            foreach (var x in owned.Where(x => Home.RestLeft(h, x.id, now) > 0).OrderBy(x => Home.RestLeft(h, x.id, now)).Take(MaxSleep))
                want[x.id] = (FarmPet.Mode.Sleep, -1);
            var team = s.team ?? new List<string>();
            foreach (var x in owned.Where(x => Home.Free(s, h, x.id, now))
                         .OrderBy(x => team.Contains(x.id) ? 0 : 1).ThenByDescending(x => s.Hero(x.id).star).ThenByDescending(x => (int)x.rarity)
                         .Take(MaxRoam))
                want[x.id] = (FarmPet.Mode.Roam, -1);

            foreach (var id in pets.Keys.Where(id => !want.ContainsKey(id)).ToList())
            {
                Destroy(pets[id].gameObject);
                pets.Remove(id);
            }
            int sleepIdx = 0;
            foreach (var kv in want)
            {
                var (mode, spot) = kv.Value;
                var wb = spot >= 0 ? Home.Find(h, spot / 8) : null;
                string kind = WorkKind(wb);
                bool work = mode == FarmPet.Mode.Work || mode == FarmPet.Mode.Tired;
                Vector2 at = wb != null ? ToLocal(SlotMap(wb, spot % 8)) : mode == FarmPet.Mode.Sleep ? ToLocal(BedMap(sleepIdx++)) : Vector2.zero;
                if (!pets.TryGetValue(kv.Key, out var pet))
                {
                    pet = Ui.Spawn(petPrefab, objLayer);
                    pet.Bind(this, d.Hero(kv.Key));
                    pets[kv.Key] = pet;
                    if (mode == FarmPet.Mode.Roam) pet.Place(mode, RoamStart(), -1, null);
                    else if (!petsPlaced || mode == FarmPet.Mode.Sleep) pet.Place(mode, at, spot, kind);
                    else
                    {
                        // tướng mới vào làm mà chưa có trên bản đồ: từ đất trống gần đó nhảy sang
                        pet.Place(FarmPet.Mode.Roam, ClampMeadow(at), -1, null);
                        pet.WalkTo(at, mode, spot, kind);
                    }
                    continue;
                }
                if (pet.State == FarmPet.Mode.Drag) continue;
                bool roamish = (pet.State == FarmPet.Mode.Roam || pet.State == FarmPet.Mode.Walk) && mode == FarmPet.Mode.Roam && pet.Spot < 0;
                if (roamish)
                {
                    // chỗ đang đứng vừa bị xây, lát nước: đi ra
                    if (pet.State == FarmPet.Mode.Roam && !WalkableAt(CellF(ToMap(pet.Pos)))) pet.WalkTo(ClampMeadow(pet.Pos), FarmPet.Mode.Roam, -1, null);
                    continue;
                }
                bool same = pet.State == mode && pet.Spot == spot;
                bool workSwap = pet.Spot == spot && spot >= 0 && work && (pet.State == FarmPet.Mode.Work || pet.State == FarmPet.Mode.Tired);
                if (mode == FarmPet.Mode.Roam)
                {
                    if (pet.State != FarmPet.Mode.Walk || pet.Spot >= 0) pet.WalkTo(ClampMeadow(pet.Pos), FarmPet.Mode.Roam, -1, null);
                    continue;
                }
                if (same || workSwap)
                {
                    if ((pet.Pos - at).sqrMagnitude > 16 || !same) pet.Place(mode, at, spot, kind); // công trình vừa dời, hết sức tại chỗ
                    continue;
                }
                pet.WalkTo(at, mode, spot, kind);
            }
            petsPlaced = true;
        }

        public void PetTapped(FarmPet pet)
        {
            if (pet.State == FarmPet.Mode.Sleep)
            {
                var h = S.home;
                var hd = D.Hero(pet.Hero);
                string id = pet.Hero;
                double left = Home.RestLeft(h, id, Now) / 60000;
                selBuilding = selLot = -1;
                ShowPanel($"{hd.name} đang nghỉ", $"Còn {Math.Ceiling(left):0} phút. Có {h.bread} bánh (Bếp làm ra): cho ăn thì hết nghỉ ngay.",
                    (h.bread > 0 ? "Cho ăn bánh" : null, () =>
                    {
                        var e = Home.Feed(S, D, Now, id);
                        panel.gameObject.SetActive(false);
                        if (e == HomeErr.Ok) App.Toasts.Show($"{hd.name} hết nghỉ", Icon("flame"));
                        Done(e);
                    }), (null, null), (null, null));
                return;
            }
            if (pet.Spot < 0) return;
            selBuilding = pet.Spot / 8;
            selLot = -1;
            RefreshPanel();
        }

        // công trình dưới chân quái đang kéo (theo ô chân, rộng thêm một ô quanh chân thoi cho dễ trúng)
        HomeBuilding DropTarget(Vector2 local)
        {
            var c = CellF(ToMap(local));
            int x = Mathf.FloorToInt(c.x), y = Mathf.FloorToInt(c.y);
            HomeBuilding best = null;
            float bd = float.MaxValue;
            foreach (var b in S.home.buildings)
            {
                var df = Home.Def(D.Cfg, b.def);
                if (df.kind != "prod") continue;
                int n = df.size;
                if (x < b.gx - 1 || y < b.gy - 1 || x > b.gx + n || y > b.gy + n) continue;
                float dd = (new Vector2(b.gx + n / 2f, b.gy + n / 2f) - c).sqrMagnitude;
                if (dd < bd)
                {
                    bd = dd;
                    best = b;
                }
            }
            return best;
        }

        public void PetDragging(FarmPet pet, Vector2 pt)
        {
            var b = DropTarget(pt);
            int id = b?.id ?? -1;
            if (id != dragHover)
            {
                if (dragHover >= 0) RenderBuildings(S.home); // trả màu cũ
                dragHover = id;
                if (b != null && objs.TryGetValue(id, out var o))
                {
                    int slot = b.slots.FindIndex(sl => sl.hero == null);
                    bool ok = slot >= 0 && Home.CanPlaceHero(S, D, Now, id, slot, pet.Hero) == HomeErr.Ok;
                    o.Tint(ok ? new Color(0.78f, 1f, 0.78f, 1f) : new Color(1f, 0.75f, 0.72f, 1f));
                    Haptics.Play(Haptic.Peg, 0.4f);
                }
            }
            // tới mép khung thì bản đồ trôi theo
            if (!landView || !landView.On) return;
            var v = landView.ToView(ToMap(pt));
            var size = landView.ViewSize;
            float edge = 110, sp = 900 * Time.unscaledDeltaTime;
            var dlt = Vector2.zero;
            if (v.x < edge) dlt.x = sp * (1 - v.x / edge);
            else if (v.x > size.x - edge) dlt.x = -sp * (1 - (size.x - v.x) / edge);
            if (v.y < TopInset + edge) dlt.y = sp * (1 - (v.y - TopInset) / edge);
            else if (v.y > size.y - BottomInset) dlt.y = -sp * (1 - (size.y - v.y) / BottomInset);
            landView.Nudge(dlt);
        }

        public bool PetDropped(FarmPet pet, Vector2 pt)
        {
            var b = DropTarget(pt);
            dragHover = -1;
            RenderBuildings(S.home);
            if (b == null) return false;
            var s = S;
            var d = D;
            double now = Now;
            Home.Tick(s, d, now);
            var df = Home.Def(d.Cfg, b.def);
            var hd = d.Hero(pet.Hero);
            int slot = b.slots.FindIndex(sl => sl.hero == null);
            if (slot < 0)
            {
                App.Toasts.Show($"{df.name} đủ người: chạm công trình để đổi ca", Icon("team"));
                return false;
            }
            var e = Home.Place(s, d, now, b.id, slot, pet.Hero);
            if (e != HomeErr.Ok)
            {
                App.Audio.Play("error");
                App.Toasts.Show(ErrText(e), Icon("lock"));
                return false;
            }
            App.Save.Save();
            App.Audio.Play("buff");
            bool match = df.hasElem && hd.elem == df.elem;
            App.Toasts.Show($"{hd.name} vào {df.name}: {FarmScene.Dec(Home.Rate(s, d, pet.Hero, b))} {FarmHeroRow.Unit(df.output)}/giờ{(match ? " (hợp hệ)" : "")}", Icon(OutIcon(df.output)));
            pet.Place(FarmPet.Mode.Work, ToLocal(SlotMap(b, slot)), SpotOf(b.id, slot), WorkKind(b));
            Render();
            return true;
        }

        // ---------- hạt (FarmFx) ----------

        public Sprite Prop(FarmProp k)
        {
            int i = (int)k;
            if (props != null && i < props.Length && props[i]) return props[i];
            switch (k)
            {
                case FarmProp.Hoe: return Icon("farm_field");
                case FarmProp.Can: return Icon("drop");
                case FarmProp.Basket: return Icon("farm_orchard");
                case FarmProp.Bread: return Icon("farm_oven");
                case FarmProp.Hammer: return Icon("hammer");
                case FarmProp.Sack: return Icon("seed");
                case FarmProp.Apple: return Icon("farm_orchard");
                case FarmProp.Carrot: return Icon("leaf");
                case FarmProp.Dust: return App.Art ? App.Art.Get("anim_smoke_small") : null;
                case FarmProp.Spark: return App.Art ? App.Art.Get("anim_sparkle") : null;
                case FarmProp.Smoke: return App.Art ? App.Art.Get("anim_smoke_big") : null;
                case FarmProp.Heart: return Icon("heart");
                case FarmProp.Seed: return Icon("seed");
                case FarmProp.Drop: return Icon("drop");
                case FarmProp.Zzz: return Icon("moon");
                default: return Icon("ball");
            }
        }

        public Sprite ProductOf(string kind) =>
            Prop(kind == "veg" ? FarmProp.Carrot : kind == "orchard" ? FarmProp.Apple : kind == "bakery" ? FarmProp.Bread :
                kind == "smithy" ? FarmProp.Hammer : FarmProp.Ball);

        // pos, vel theo toạ độ lớp vật (lớp hạt cùng khung)
        public void Fx(Sprite s, Color c, Vector2 pos, Vector2 vel, float gravity, float life, float size0, float size1, float spin = 0,
            bool pop = false, float drag = 0)
        {
            if (!s || !fxPrefab || !fxLayer) return;
            var fx = fxPool.Find(x => !x.Busy);
            if (!fx)
            {
                if (fxPool.Count >= 60) return;
                fx = Ui.Spawn(fxPrefab, fxLayer);
                fxPool.Add(fx);
            }
            fx.Play(s, c, fxLayer.InverseTransformPoint(objLayer.TransformPoint(pos)), vel, gravity, life, size0, size1, spin, pop, drag);
        }
    }
}
