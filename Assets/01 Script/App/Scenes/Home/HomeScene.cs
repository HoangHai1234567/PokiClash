// Màn Nhà (GD_Claude/21_Nha_Home.md, mốc H2), thay Trang trại. Luật ở Core/Home. Prefab Assets/04 Prefabs/Screens/Home dựng bằng menu
// "PokiClash/Prefab/Nhà và side meta/Nhà: dựng màn" (Editor/HomeSceneMenu.cs).
// - Bản đồ: ảnh nền đảo (home_base: đồng cỏ hình thoi, cao nguyên, hồ, suối, mạch quặng, bãi cát, biển, rừng rìa trên) kéo, phóng to thu nhỏ nhẹ (LandView của màn Đảo, chế độ phủ kín màn);
//   lưới thoi 72 x 72 (người dùng dặn 2026-11-19: đảo to cho quái đi khắp nơi, máy không cần thấy hết đảo), ô 96 x 48 px; gốc lưới
//   (góc trên ô 0,0) đo trên ảnh nền (home_art.json, ảnh ghép bằng ArtGen/Home/base/compose_base72.py).
// - Quái (FarmPet của Trang trại, cảnh chủ là màn này; bật UseRig: rig .atomik chạy walk / idle, đêm sáng nhẹ, người dùng 2026-11-20):
//   tướng rảnh đi lang thang trên đất đã mở (tối đa MaxRoam con), tướng đang làm
//   đứng trước công trình cử động theo việc, tướng đang nghỉ ngủ cạnh Nhà chính. Quái chỉ vào làm khi người chơi kéo thả nó vào công
//   trình hoặc chọn trong bảng công trình (hộp chọn tướng); không có Tự xếp.
// - Bến tàu ở mũi dưới (PierShip, dựng bằng ShipBuild.Pier của phiên sảnh): chuyến tàu qua mây sảnh ↔ Nhà cập bến / rời bến ở đây; tàu
//   cập bến xong thì máy lướt lên Nhà chính; chạm tàu là về đảo.
// - Lớp theo render queue kiểu Clash of Critters (bảng Layers, GD_Claude/22_Critters_Home.md): nền + biển (shader UIHomeSea) → cát →
//   cỏ rải → ô lát → lưới → vách → môi cỏ → cây rìa → vật (cây ô chưa mở, công trình, trang trí, quái; vẽ xa trước gần sau theo góc dưới
//   chân thoi) → hạt → mây che rìa (từng đám rời dựng sẵn trong prefab, CloudRing toả quanh tàu) → tàu → sáng tối (DayNight dùng chung
//   với các đảo: nhuộm theo giờ máy, tia nắng) → tự sáng (mặt nạ cửa sổ, lò của công trình khi tối, không quầng).
// - Chạm: công trình → vòng nút quanh nó (HomeRing, kiểu Clash of Critters 2026-11-22: Thu, Giao tướng, Lên cấp + giá, Dời, Chi tiết;
//   nhãn tên + trạng thái dưới chân); ô rừng → Dọn; bong bóng trên công trình (vòng tiến độ kho) chạm là thu. Chế độ xây: tấm dưới có
//   tab lọc + khay cuộn thẻ icon, chạm / kéo đất để dời bóng ma, nút ✓ ✗ cạnh bóng ma; chế độ lát: chọn loại ô, chạm đất để lát.
//   Hàng nút dưới: nút tròn icon có chữ (Xây, Lát ô, Thu hết có chấm đỏ khi có đồ chờ thu, Ra đảo).
// - Vật vừa chọn (người dùng 2026-11-22): nhún (HomeObject.Bounce) và sáng nhẹ bằng shader PokiClash/UIHomeSelect (vật liệu selectMat,
//   độ sáng _HomeSel toàn cục: loé lúc chọn rồi thở nhẹ khi bảng còn mở); ô rừng thì cây trong ô nhún lần lượt, sáng cùng.
// - Cây bi (Core/Trees; từ 2026-11-23 chỉ còn ở Nhà, mở cùng Nhà): bong bóng trên đầu ghi số bi cây đang có (kiểu Clash of Critters);
//   chạm một cây (thân hay tán lá, HitAt) là hái hết mọi cây, bi bay từ từng cây lên chip bi của thanh trên (hạt FarmFx.Fly trên lớp
//   giao diện cố định), chip đếm chạy. Cây đã mở mà chưa có chỗ nằm đầu khay Xây, đặt miễn phí; lần đầu có hướng dẫn (Tutor): Xây →
//   chọn Cây bi → kéo, Đặt → chạm cây hái bi.
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
    // phần rừng (bong bóng bi, cây bay khi dọn xong, gió) ở HomeScene.Forest.cs; chim, bướm, ong ở HomeScene.Life.cs
    public sealed partial class HomeScene : SceneRoot, IFarmPetHost
    {
        public override string Title => Loc.T("Nhà");

        const float CW = 96, CH = 48; // một ô lưới: ngang, dọc (px)
        const float TreeScale = 192f / 150f * 0.85f; // cây rời: chân cỏ 150 px ở ảnh gen = 2 ô lưới; thu 0,85 cho cân với nhà
        const float TopInset = SceneRoot.BarHeight + 70, BottomInset = 230; // khung trên (thanh, dòng tài nguyên), dưới (hàng nút, gợi ý)

        // Lớp của bản đồ Nhà theo render queue kiểu Clash of Critters (GD_Claude/22_Critters_Home.md mục 6): bộ dựng prefab tạo các nút con
        // của lớp kéo đúng thứ tự số này (uGUI: thứ tự anh em là thứ tự vẽ); code chạy chỉ đặt vật vào đúng nút, không đổi thứ tự lớp.
        // Môi trường (cát, cỏ rải, vách, cây rìa) cố định theo queue, không xếp mỗi khung; chỉ lớp "vat" xếp theo chân.
        public static readonly (string name, int queue)[] Layers =
        {
            ("nen", 100),       // ảnh nền + biển (shader UIHomeSea)
            ("cat", 200),       // bãi cát, đồ ven biển
            ("co_rai", 300),    // cụm cỏ, hoa rải lặp
            ("o_lat", 400),     // ô lát
            ("luoi", 500),      // lưới sáng khi xây
            ("vach", 600),      // vách cao nguyên
            ("moi_co", 650),    // môi cỏ phủ mép vách
            ("rung_nen", 700),  // cây rìa (không mở được)
            ("vat", 800),       // công trình, cây ô rừng chưa mở, quái
            ("hat", 850),       // hạt quái, gió
            ("may", 900),       // mây rìa
            ("ben_tau", 950),   // tàu ở bến (ShipBuild.Pier)
            ("sang_toi", 1000), // nhuộm theo giờ, tia nắng
            ("tu_sang", 1100),  // mặt nạ tự sáng của công trình (đêm), không quầng
        };

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
        [SerializeField] RectTransform rimLayer; // lớp "rung_nen": cây rìa, vẽ dưới lớp vật, không xếp mỗi khung
        [SerializeField] Material emitMat; // mặt nạ tự sáng của công trình (shader PokiClash/UIIslandEmit, tự đọc _PokiNight)
        [SerializeField] float terraceH; // vách cao nguyên dọc hai cạnh trên (px): cây rìa đứng trên bậc cao, nâng lên chừng ấy
        [SerializeField] Material selectMat; // vật đang chọn sáng nhẹ (shader PokiClash/UIHomeSelect, home_select.mat); trống thì chỉ nhún

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
        [SerializeField] HomeTrayItem trayIconPrefab; // khay Xây: nút có icon công trình (Items/NutKhayNha); trống thì nút chữ như cũ
        [SerializeField] RectTransform panel; // bảng chữ cũ: chỉ dùng khi prefab chưa có vòng nút (ring)
        [SerializeField] TextMeshProUGUI panelTitle, panelBody;
        [SerializeField] SketchButton panelA, panelB, panelC, panelD;

        // Giao diện kiểu Clash of Critters (người dùng 2026-11-22, GD_Claude/22_Critters_Home.md mục 7): vòng nút quanh vật đang chọn thay
        // bảng chữ, hàng nút dưới là nút tròn icon có chữ dưới (chấm đỏ khi có đồ chờ thu), chế độ xây là tấm dưới có tab lọc và khay cuộn
        // thẻ icon, đặt / dời bằng nút ✓ ✗ bên cạnh bóng ma. Menu "PokiClash/Prefab/Nhà và side meta/Nhà: giao diện kiểu Critters".
        [SerializeField] HomeRing ring;
        [SerializeField] HomeRingButton hudBuild, hudPaint, hudHarvest, hudSail;
        [SerializeField] RectTransform sheet; // tấm xây: nền, tab, khay cuộn (khay là nội dung cuộn bên trong)
        [SerializeField] SketchButton[] tabs; // Tất cả, Sản xuất, Hỗ trợ, Trang trí
        int tab;
        bool selPop; // vật vừa chọn: vòng nút nảy ra (đếm giờ mỗi giây thì không)

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

        // Dùng khi nướng prefab (Editor): phần giao diện kiểu Critters
        public void SetupCritters(HomeRing ringComp, HomeRingButton build, HomeRingButton paint, HomeRingButton harvest, HomeRingButton sail,
            RectTransform sheetRt, SketchButton[] tabButtons)
        {
            ring = ringComp;
            hudBuild = build;
            hudPaint = paint;
            hudHarvest = harvest;
            hudSail = sail;
            sheet = sheetRt;
            tabs = tabButtons;
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

        // Dùng khi nướng prefab (Editor): nút khay Xây có icon công trình (HomeTrayMenu)
        public void SetupTrayIcon(HomeTrayItem item) => trayIconPrefab = item;

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

        // Dùng khi nướng prefab (Editor): lớp cây rìa, vật liệu mặt nạ tự sáng, chiều cao vách cao nguyên (bộ mảnh home_kit.json).
        public void SetupEnv(RectTransform rim, Material emit, float terrace)
        {
            rimLayer = rim;
            emitMat = emit;
            terraceH = terrace;
        }

        // Dùng khi nướng prefab (Editor).
        public void SetupGrid(Image grid) => gridImg = grid;

        // Dùng khi nướng prefab (Editor): vật liệu sáng nhẹ của vật đang chọn
        public void SetupSelect(Material m) => selectMat = m;

        // ---------- vật đang chọn: nhún + sáng nhẹ ----------

        static readonly int HomeSelId = Shader.PropertyToID("_HomeSel");
        HomeObject selObj; // vật đang sáng (công trình, cây bi vừa hái)
        int selTreesLot = -1; // ô rừng đang sáng (cây trong ô)
        readonly List<(Image img, float sx, float delay)> selTrees = new List<(Image, float, float)>();
        bool selHold; // giữ sáng tới khi bảng đóng; không giữ (cây bi vừa hái) thì loé rồi tắt
        float selT;
        const float SelFlash = 0.08f;

        // chọn vật o (null = bỏ): sáng + nhún; chạm lại vật đang chọn thì nhún lại. hold: giữ sáng theo bảng
        void Pick(HomeObject o, bool hold)
        {
            ClearTreeSel();
            if (selObj != o)
            {
                if (selObj) selObj.Select(null);
                selObj = o;
                if (o) o.Select(selectMat);
            }
            selHold = hold;
            selT = 0;
            if (!o) return;
            o.Bounce();
            Haptics.Play(Haptic.Peg);
        }

        // chọn ô rừng: cây trong ô sáng cùng vật liệu, nhún lần lượt từ gần tâm ra
        void PickLot(int lot)
        {
            if (selObj) selObj.Select(null);
            selObj = null;
            if (selTreesLot != lot)
            {
                ClearTreeSel();
                selTreesLot = lot;
                if (forestTrees.TryGetValue(lot, out var list) && list.Count > 0)
                {
                    var c = C;
                    var (i, j) = Home.LotIJ(c, lot);
                    var mid = CellTop(i * c.lot + c.lot / 2f, j * c.lot + c.lot / 2f);
                    foreach (var (img, _) in list)
                    {
                        if (!img) continue;
                        var p = img.rectTransform.anchoredPosition;
                        float dist = (new Vector2(p.x, -p.y) - mid).magnitude;
                        if (selectMat) img.material = selectMat;
                        selTrees.Add((img, img.rectTransform.localScale.x, Mathf.Min(0.25f, dist / 2400f)));
                    }
                }
            }
            selHold = true;
            selT = 0;
            Haptics.Play(Haptic.Peg);
        }

        void ClearTreeSel()
        {
            foreach (var (img, sx, _) in selTrees)
            {
                if (!img) continue;
                Theme.SetSprite(img, img.sprite); // trả vật liệu thường
                img.rectTransform.localScale = new Vector3(sx, 1, 1);
            }
            selTrees.Clear();
            selTreesLot = -1;
        }

        // mỗi khung: hết chọn (bảng đóng, đổi chế độ, vật bị dời / xoá) thì trả về thường; đặt độ sáng toàn cục, nhún cây ô rừng
        void SyncSelect(float dt)
        {
            bool panelOn = SelOn && mode == Mode.Normal;
            if (selObj)
            {
                bool keep = selObj.gameObject.activeInHierarchy && (selHold ? panelOn && selBuilding == selObj.Id : selT < 0.6f);
                if (!keep)
                {
                    selObj.Select(null);
                    selObj = null;
                }
            }
            if (selTreesLot >= 0 && !(panelOn && selLot == selTreesLot)) ClearTreeSel();
            float g = 0;
            if (selObj || selTreesLot >= 0)
            {
                selT += dt;
                // loé lên trong SelFlash giây rồi lặn; còn giữ thì thở quanh 0,5 (0,36–0,64) cho thấy rõ vật đang chọn
                float flash = selT < SelFlash ? selT / SelFlash : Mathf.Exp(-(selT - SelFlash) * 5f);
                float steady = selHold ? Mathf.Clamp01(selT / SelFlash) * (0.5f + 0.14f * Mathf.Sin((selT - SelFlash) * 3.4f)) : 0;
                g = Mathf.Max(flash, steady);
                for (int i = 0; i < selTrees.Count; i++)
                {
                    var (img, sx, delay) = selTrees[i];
                    if (!img) continue;
                    float t = selT - delay;
                    var sq = t > 0 && t < 0.8f ? HomeObject.Squash(t, 0.7f) : Vector3.one;
                    img.rectTransform.localScale = new Vector3(sx * sq.x, sq.y, 1);
                }
            }
            Shader.SetGlobalFloat(HomeSelId, g);
        }

        // ---------- Cây bi: số bi trên đầu, chạm là hái hết, bi bay lên chip ----------

        readonly List<FarmFx> flyPool = new List<FarmFx>();

        // bi đang có (phần nguyên) của cây b; st = Trees.Of(...).stock đã tính tới giờ
        static int TreeBalls(HomeBuilding b, List<double> st) => b.tree >= 0 && b.tree < st.Count ? (int)Math.Floor(st[b.tree] + 1e-9) : 0;

        bool IsTree(HomeBuilding b) => Home.Def(D.Cfg, b.def)?.kind == "tree";

        // khung bắt chạm của hình cây (px bản đồ, y xuống): khung ảnh bỏ bớt lề trong suốt hai bên và trên
        static Rect TreeRect(HomeObject o)
        {
            var r = ViewRect(o.Rt);
            float mx = r.width * 0.12f, my = r.height * 0.06f;
            return Rect.MinMaxRect(r.xMin + mx, r.yMin + my, r.xMax - mx, r.yMax);
        }

        // công trình ở điểm chạm p (px bản đồ), cell = ô của p: Cây bi bắt chạm theo hình, cả tán lá (người dùng 2026-11-23: chạm thân
        // mới hái được, chạm lá thì không); công trình khác theo ô dưới chân; trùng nhau thì cái vẽ sau (gần người xem) thắng
        HomeBuilding HitAt(Vector2 p, Vector2Int cell)
        {
            var foot = Home.InMap(C, cell.x, cell.y) ? Home.At(S.home, D.Cfg, cell.x, cell.y) : null;
            HomeBuilding tree = null;
            float treeDepth = float.MinValue;
            foreach (var b in S.home.buildings)
            {
                if (b.id == moveId || !IsTree(b) || !objs.TryGetValue(b.id, out var o) || !o || !o.gameObject.activeSelf) continue;
                if (!TreeRect(o).Contains(p) || o.Depth < treeDepth) continue;
                tree = b;
                treeDepth = o.Depth;
            }
            if (tree == null || foot == null || foot == tree) return tree ?? foot;
            return objs.TryGetValue(foot.id, out var fo) && fo && fo.Depth > treeDepth ? foot : tree;
        }

        // hái mọi cây (Trees.Harvest như nút Hái của hộp Cây bi sảnh); cây vừa chạm loé + nhún, cây khác nhún nhẹ, bi bay từ từng cây
        void HarvestTrees(HomeBuilding tapped)
        {
            var s = S;
            var cfg = D.Cfg;
            double now = Now;
            Trees.Tick(s, cfg, now);
            var st = Trees.Of(s, now).stock;
            var from = new List<(HomeObject o, Vector3 at, int n)>();
            foreach (var tb in s.home.buildings)
            {
                if (!IsTree(tb) || !objs.TryGetValue(tb.id, out var o)) continue;
                int k = TreeBalls(tb, st);
                if (k > 0) from.Add((o, o.BubbleWorld(), k));
            }
            int n = Trees.Harvest(s, cfg, now);
            if (n <= 0) return;
            if (App.Bars) App.Bars.HoldBalls(n); // chip giữ số cũ tới khi bi bay tới (lưu xong thanh trên tự làm mới)
            App.Save.Save();
            selBuilding = selLot = -1;
            HideSel();
            objs.TryGetValue(tapped.id, out var hit);
            Pick(hit, false);
            // cây chưa có chỗ trong nhà (hết chỗ đặt) vẫn được hái: bi của nó bay ra từ cây vừa chạm
            int rest = n - from.Sum(f => f.n);
            if (rest > 0 && hit) from.Add((hit, hit.BubbleWorld(), rest));
            foreach (var f in from)
            {
                f.o.PopBubble();
                if (f.o != hit) f.o.Bounce(0.6f);
            }
            App.Audio.Play("coin");
            FlyBalls(from, n);
            Labels();
        }

        // bi bay từ các cây lên chip bi: mỗi cây 3–6 viên (theo số bi, tổng tối đa 24), các cây bật cùng lúc, trên lớp bay của thanh trên
        // (trên mọi thứ của màn, không mờ theo giao diện cố định); mỗi viên tới thì chip đếm thêm phần của nó (HoldBalls / ReleaseBalls)
        // và nảy nhẹ
        void FlyBalls(List<(HomeObject o, Vector3 at, int n)> from, int total)
        {
            var bars = App.Bars;
            var chip = bars ? bars.BallChip : null;
            var parent = bars ? bars.FlyLayer : null;
            var sp = Icon("ball");
            if (!chip || !parent || !fxPrefab || !sp || from.Count == 0)
            {
                if (bars) bars.ReleaseBalls(total);
                return;
            }
            // số viên mỗi cây: 3–6 theo số bi, tổng tối đa 24 (nhiều cây thì mỗi cây bớt, ít nhất 2)
            var ks = from.Select(f => Mathf.Clamp(Mathf.CeilToInt(f.n / 5f), 3, 6)).ToArray();
            int sum = ks.Sum();
            if (sum > 24)
                for (int t = 0; t < ks.Length; t++)
                    ks[t] = Mathf.Max(2, Mathf.RoundToInt(ks[t] * 24f / sum));
            int count = ks.Sum(), maxK = ks.Max();
            float step = Mathf.Min(0.06f, 0.6f / maxK); // các cây bật cùng lúc, mỗi cây bật lần lượt: cả loạt bật trong khoảng 0,7 giây
            int every = Mathf.Max(1, count / 10); // tiếng "pick": nhiều viên thì cách viên mới kêu, khỏi dồn tiếng
            int left = total, landed = 0;
            var cam = PokiCanvas.UiCamera;
            Vector2 Local(Vector3 world)
            {
                var scr = RectTransformUtility.WorldToScreenPoint(cam, world);
                RectTransformUtility.ScreenPointToLocalPointInRectangle(parent, scr, cam, out var l);
                return l;
            }
            var to = Local(chip.TransformPoint(chip.rect.center));
            for (int t = 0; t < from.Count; t++)
            {
                var a = Local(from[t].at);
                for (int i = 0; i < ks[t]; i++)
                {
                    var fx = flyPool.Find(x => x && !x.Busy);
                    if (!fx)
                    {
                        fx = Ui.Spawn(fxPrefab, parent);
                        flyPool.Add(fx);
                    }
                    float delay = i * step + t * 0.03f;
                    fx.Fly(sp, a + UnityEngine.Random.insideUnitCircle * 14f, to, delay, UnityEngine.Random.Range(0.62f, 0.74f), 54, () =>
                    {
                        // phần của viên này (viên cuối nhả nốt phần lẻ)
                        int part = ++landed >= count ? left : Mathf.Min(left, Mathf.CeilToInt(total / (float)count));
                        left -= part;
                        if (!bars) return;
                        bars.ReleaseBalls(part);
                        bars.PunchBalls();
                        if ((landed - 1) % every == 0) App.Audio.Play("pick", 0.45f, 1.05f + Mathf.Min(landed / every, 12) * 0.04f);
                    });
                }
            }
        }

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
            spreadR = 1000;
            gridMat.SetVector("_Spread", new Vector4(0, 0, 1000, 0));
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

        // lưới lan ra từ ô giữa khung nhìn khi vào chế độ xây (học Critters: IsometricGridRenderer.spreadSpeed); 1000 = đã lan hết, tắt vệt sáng
        float spreadR = 1000;
        Vector2 spreadC;

        void StartSpread()
        {
            if (!gridMat || !world) return;
            var vrt = landView ? (RectTransform)landView.transform : null;
            var lp = vrt ? (Vector2)world.InverseTransformPoint(vrt.TransformPoint(vrt.rect.center)) : Vector2.zero;
            spreadC = CellF(new Vector2(lp.x, -lp.y)); // lớp kéo neo trên trái: y local âm đi xuống
            spreadR = 0;
        }

        void FadeGrid(float dt)
        {
            if (!gridMat) return;
            if (spreadR < 1000)
            {
                // 36 ô/giây: khung nhìn rộng khoảng 20 ô nên lan qua màn trong khoảng nửa giây (Critters 100 ô/giây nhưng máy họ chỉ thấy vài ô)
                spreadR = spreadR > C.grid * 1.5f ? 1000 : spreadR + dt * 36f;
                gridMat.SetVector("_Spread", new Vector4(spreadC.x, spreadC.y, spreadR, 0));
            }
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
            Tutorial.SeedTree(s, D.Cfg, Now); // cây bi đầu có sẵn 10 bi (cây mở cùng Nhà)
            if (!Tutorial.CoreDone(s)) Tutorial.Mark(s, Tutorial.HomeGo); // hướng dẫn C21 (ép chạm tàu ở sảnh) xong khi đã về tới Nhà
            App.Save.Save();
            btnBuild.SetOnClick(() => SetMode(mode == Mode.Build ? Mode.Normal : Mode.Build));
            btnPaint.SetOnClick(() => SetMode(mode == Mode.Paint ? Mode.Normal : Mode.Paint));
            btnHarvest.SetOnClick(HarvestAll);
            btnSail.SetOnClick(() => App.Router.Go(SceneIds.Hub));
            Guide.Mark("home.build", hudBuild ? (Component)hudBuild : btnBuild);
            Guide.Mark("home.sail", hudSail ? (Component)hudSail : btnSail);
            if (ring) ring.Insets(TopInset, BottomInset);
            if (tabs != null)
                for (int i = 0; i < tabs.Length; i++)
                {
                    int k = i;
                    if (tabs[i]) tabs[i].SetOnClick(() =>
                    {
                        tab = k;
                        BuildTray();
                    });
                }
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
            LifeEnter(); // chim, bướm, ong (HomeScene.Life.cs)
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
            Pick(null, false);
            Shader.SetGlobalFloat(HomeSelId, 0);
            LifeExit(); // cây đang bay, chim, bướm, ong
            // bi bay nằm ở lớp bay của thanh trên (khung app, không gỡ theo màn): dọn đi, viên đang bay báo tới nơi (nhả số bi đang giữ)
            foreach (var fx in flyPool)
                if (fx)
                    Destroy(fx.gameObject);
            flyPool.Clear();
        }

        public override void Refresh() => Render();

        void FocusOn(HomeBuilding b, float dur = 0)
        {
            if (b == null || !landView) return;
            var n = Home.Def(D.Cfg, b.def).size;
            landView.Show(CellTop(b.gx + n / 2f, b.gy + n / 2f), 1f, dur);
        }

        void Update()
        {
            if (!world || App.I == null || App.Save?.Data == null || App.Data == null) return; // chưa khởi động xong hoặc đang dừng Play
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.1f);
            clock += dt;
            FadeGrid(dt);
            SyncSelect(dt);
            LifeTick(dt); // gió lay cây, cây bay khi dọn xong, chim, bướm, ong
            if ((tutorT += dt) > 0.5f)
            {
                tutorT = 0;
                Tutor();
            }
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

        // ô rừng dọn xong (lúc đang xem hoặc lúc vắng): cây bay lên trời (RenderForests → LaunchForest), bi thưởng bay từ trên đầu ô rừng
        // lên chip bi như Cây bi (ô đang trong khung nhìn), báo bi để thả (bi, gỗ đã cộng trong bản lưu). Phải chạy TRƯỚC lần lưu đầu sau khi
        // dọn xong (lưu là thanh trên làm mới số bi): SpeedUp, ClearLot gọi thẳng vào đây
        void ReportCleared()
        {
            var h = S.home;
            var lots = h.cleared.ToList();
            int balls = lots.Sum(lot => Home.RingOf(C, lot)?.balls ?? 0);
            int n = lots.Count;
            h.cleared.Clear();
            var from = ClearedRewardFrom(lots); // chỗ bi bay ra: lấy trước Render (Render gỡ mốc ô rừng)
            int fly = from.Sum(f => f.n);
            if (fly > 0 && App.Bars) App.Bars.HoldBalls(fly);
            if (selLot >= 0 && lots.Contains(selLot))
            {
                selLot = -1;
                HideSel();
            }
            App.Save.Save();
            Render();
            App.Bars.Refresh();
            if (fly > 0) FlyBalls(from, fly);
            else App.Audio.Play("coin");
            string what = n > 1 ? Loc.F("Đã dọn {0} ô rừng", n) : Loc.T("Đã dọn rừng");
            App.Toasts.Show(balls > 0 ? Loc.F("{0}: +{1} bi để thả", what, balls) : what, Icon("ball"));
        }

        // ---------- dựng ----------

        void Render()
        {
            var s = S;
            var d = D;
            var h = Home.Of(s, d, Now);
            res.text = Loc.F("Gỗ {0}/{1:0}   Quặng {2}/{3:0}   ", Mathf.FloorToInt((float)h.wood), Home.WoodCap(h, d.Cfg), Mathf.FloorToInt((float)h.ore), Home.OreCap(h, d.Cfg)) +
                       Loc.F("Bánh {0}   Nhà cấp {1}   Tướng {2}/{3}", h.bread, Home.Level(h), Home.UsedSlots(h), Home.TotalSlots(h, C));
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
                        if (selTreesLot == lot) ClearTreeSel(); // trả vật liệu, cỡ của cây đang sáng
                        LaunchForest(lot, old); // vừa dọn xong: cây trong khung nhìn bay lên trời, cây ngoài khung gỡ luôn
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
            mk.BubbleTapped = _ => TapLot(lot); // chạm bong bóng bi = chạm ô rừng
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
            FitMarker(lot); // mốc cao tới ngọn cây giữa ô: bong bóng bi nổi trên tán
        }

        const int RimKey = -1000; // khoá của rìa rừng trong forestTrees (ô rừng là 0..35)

        // rìa rừng ngoài hai cạnh trên của lưới: một dải cây rời sâu 6 ô nối ô rừng với rừng vẽ sẵn trên ảnh nền, không mở được.
        // Nằm ở lớp "rung_nen" (queue 700, như cây nền queue 2998 của Critters): xếp xa trước gần sau một lần lúc dựng, không xếp lại mỗi khung
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
            var parent = rimLayer ? rimLayer : objLayer;
            for (float gx = -Depth + 1; gx < c.grid; gx += 2.2f)
            for (float gy = -Depth + 1; gy < c.grid; gy += 2.2f)
            {
                if (gx >= 0 && gy >= 0) continue; // trong lưới
                float x = gx + R(-0.7f, 0.7f), y = gy + R(-0.7f, 0.7f);
                var p = CellTop(x, y);
                if (p.x < -80 || p.x > size.x + 80 || p.y < 30) continue;
                AddTree(tall[rnd.Next(tall.Length)], x, y, R(0.9f, 1.15f), rnd.Next(2) == 0, list, parent);
            }
            // bậc cao sau vách (bộ mảnh A5): cây đứng trên mặt bậc, cao hơn đồng cỏ terraceH px
            if (terraceH > 0)
                foreach (var (img, _) in list)
                    img.rectTransform.anchoredPosition += new Vector2(0, terraceH);
            foreach (var (img, _) in list) img.color = LockedTint;
            if (rimLayer)
            {
                var sorted = list.OrderBy(e => e.Item2).ToList();
                for (int i = 0; i < sorted.Count; i++) sorted[i].Item1.transform.SetSiblingIndex(i);
            }
        }

        void AddTree(TreeArt t, float gx, float gy, float sc, bool flip, List<(Image, float)> list, RectTransform parent = null)
        {
            if (gx > C.grid - 4 && gy > C.grid - 4) return; // bến ở mũi dưới: không cho cây mọc đè
            var img = Ui.Spawn(treePrefab, parent ? parent : objLayer);
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
                    o.BubbleTapped = OnBubble;
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
            SortObjectsAndPets();
            foreach (var kv in forestTrees)
            {
                if (kv.Key == RimKey && rimLayer) continue; // cây rìa ở lớp riêng, đã xếp lúc dựng
                foreach (var (img, d) in kv.Value) order.Add((img.transform, d));
            }
            foreach (var m in forests.Values) order.Add((m.transform, float.MaxValue / 2));
            if (ghost) order.Add((ghost.transform, float.MaxValue));
            order.Sort((a, b) => a.d.CompareTo(b.d));
            for (int i = 0; i < order.Count; i++)
                if (i >= objLayer.childCount || objLayer.GetChild(i) != order[i].t) order[i].t.SetSiblingIndex(i);
        }

        // Công trình và quái (người dùng 2026-11-20: "vẽ lỗi, lúc ở trên lúc ở dưới"). Y góc dưới chỉ đúng khi hai vật cùng cỡ: cây bi 2x2
        // đứng trước tường nhà 6x6 có y góc dưới nhỏ hơn nhà nên bị nhà đè; mẹo cũ đẩy quái lên sau công trình theo một dải ngang bật tắt
        // khi quái đi, kéo theo quái nhảy cả lên trước cây đứng trước nó. Luật mới: hai vật mà hình chồng nhau, vật nằm hẳn phía trước vật
        // kia theo một trục lưới (x0 >= x1 hoặc y0 >= y1 của vật kia, phía kia không như vậy) vẽ sau; không phân được thì theo y góc dưới.
        // Khoá vẽ = y góc dưới, chỉ nâng tới khi mọi cặp đã phân đúng, nên cây rừng (giữ y góc dưới) gần như không bị xáo.
        struct SortItem
        {
            public Transform t;
            public Rect box;  // ô lưới (x, y, rộng, sâu); quái: một điểm
            public Rect view; // hình trên bản đồ (px, y xuống)
            public float key;
        }

        readonly List<SortItem> sortItems = new List<SortItem>();
        readonly Dictionary<int, HomeBuilding> sortBuildings = new Dictionary<int, HomeBuilding>();

        void SortObjectsAndPets()
        {
            sortItems.Clear();
            sortBuildings.Clear();
            if (S.home != null)
                foreach (var b in S.home.buildings) sortBuildings[b.id] = b;
            foreach (var kv in objs)
            {
                var o = kv.Value;
                if (!sortBuildings.TryGetValue(kv.Key, out var b) || !o.gameObject.activeSelf)
                {
                    order.Add((o.transform, o.Depth));
                    continue;
                }
                int n = Home.Def(D.Cfg, b.def).size;
                sortItems.Add(new SortItem { t = o.transform, box = new Rect(b.gx, b.gy, n, n), view = ViewRect(o.Rt), key = o.Depth });
            }
            foreach (var p in pets.Values)
            {
                if (p.State == FarmPet.Mode.Drag)
                {
                    order.Add((p.transform, float.MaxValue / 4));
                    continue;
                }
                var m = ToMap(p.Pos);
                var c = CellF(m);
                float hh = p.ViewHeight, hw = hh * 0.6f;
                sortItems.Add(new SortItem { t = p.transform, box = new Rect(c.x, c.y, 0, 0), view = new Rect(m.x - hw, m.y - hh, 2 * hw, hh + 8), key = m.y });
            }
            int cnt = sortItems.Count;
            for (int pass = 0; pass < cnt; pass++)
            {
                bool moved = false;
                for (int i = 0; i < cnt; i++)
                for (int j = 0; j < cnt; j++)
                {
                    if (i == j) continue;
                    var a = sortItems[i];
                    var f = sortItems[j];
                    if (f.key > a.key || !a.view.Overlaps(f.view) || !DrawAfter(f.box, a.box)) continue;
                    f.key = a.key + 0.01f;
                    sortItems[j] = f;
                    moved = true;
                }
                if (!moved) break;
            }
            foreach (var it in sortItems) order.Add((it.t, it.key));
        }

        // a nằm trước mặt tường nhìn thấy được của b (mặt gx = x1 hoặc gy = y1: gần người xem)
        static bool InFront(Rect a, Rect b) => a.x >= b.xMax - 1e-3f || a.y >= b.yMax - 1e-3f;

        static bool IsPoint(Rect r) => r.width <= 0 && r.height <= 0;

        // f phải vẽ sau a? Quái (điểm) với công trình: quái ở trước một mặt tường nhìn thấy được thì vẽ sau, không thì vẽ trước (đứng trong
        // chân công trình lúc đi xuyên: không phân, theo y). Hai công trình: một cái trước mặt tường cái kia mà điều ngược lại không đúng.
        // Hai quái: theo y chân.
        static bool DrawAfter(Rect f, Rect a)
        {
            bool fp = IsPoint(f), ap = IsPoint(a);
            if (fp && ap) return false;
            if (fp) return InFront(f, a);
            if (ap) return !InFront(a, f) && !a.Overlaps(f);
            return InFront(f, a) && !InFront(a, f);
        }

        // khung hình của vật trên bản đồ (px, y xuống): neo góc trên trái lớp, pivot ở góc dưới chân thoi
        static Rect ViewRect(RectTransform rt)
        {
            var s = rt.sizeDelta;
            var pv = rt.pivot;
            var a = rt.anchoredPosition;
            return new Rect(a.x - pv.x * s.x, -a.y - (1 - pv.y) * s.y, s.x, s.y);
        }

        // nhãn trên đầu: đang xây / nâng cấp (giờ còn), đồ đầy kho; ô rừng đang dọn
        void Labels()
        {
            var s = S;
            var h = s.home;
            if (h == null) return;
            double now = Now;
            Trees.Tick(s, D.Cfg, now);
            var st = Trees.Of(s, now).stock;
            bool any = false; // có đồ chờ thu: chấm đỏ trên nút Thu hết
            foreach (var b in h.buildings)
            {
                if (!objs.TryGetValue(b.id, out var o)) continue;
                string text = b.job != 0 ? $"{(b.job == 1 ? Loc.T("Xây") : Loc.T("Lên cấp"))} {Clock((b.until - now) / 60000)}" : null;
                o.Label(text);
                if (IsTree(b))
                {
                    // Cây bi: bong bóng ghi số bi đang có (từ 1 bi), chạm cây là hái
                    int k = TreeBalls(b, st);
                    o.Bubble(k > 0 ? Icon("ball") : null, k > 0 ? TopBars.Fmt(k) : null);
                    o.Fill(-1);
                    continue;
                }
                // công trình làm ra: bong bóng icon sản phẩm, vòng xanh chạy theo lượng chờ thu so với sức chứa, đầy thì cam + phập phồng
                var df = Home.Def(D.Cfg, b.def);
                bool has = Home.Stock(b) > 0;
                any |= has;
                o.Bubble(has ? Icon(OutIcon(df.output)) : null);
                o.Fill(has ? StockFill(b, df) : -1);
            }
            if (hudHarvest) hudHarvest.Dot(any);
            ForestBubbles(now); // đang dọn: giờ còn; dọn được: bong bóng bi thưởng (HomeScene.Forest.cs)
            if (ghost) return; // đang đặt / dời: vòng ✓ ✗ do UpdateGhost lo
            if (selBuilding >= 0 || selLot >= 0) RefreshPanel();
        }

        // phần kho đã đầy: tổng đồ chờ thu / tổng sức chứa của các ô có tướng (tướng rút hết mà còn đồ thì coi là đầy)
        float StockFill(HomeBuilding b, HomeBuildingDef df)
        {
            double have = 0, cap = 0, capH = Home.CapHours(D.Cfg, df, b.level);
            foreach (var sl in b.slots)
            {
                have += sl.stock;
                if (sl.hero != null) cap += Home.Rate(S, D, sl.hero, b) * capH;
            }
            return cap <= 0 ? 1 : Mathf.Clamp01((float)(have / cap));
        }

        // chạm bong bóng (kiểu Critters): Cây bi thì hái hết, công trình thì thu luôn
        void OnBubble(HomeObject o)
        {
            if (mode != Mode.Normal || !o) return;
            var b = Home.Find(S.home, o.Id);
            if (b == null) return;
            if (IsTree(b))
            {
                HarvestTrees(b);
                return;
            }
            if (Home.Stock(b) <= 0) return;
            o.PopBubble();
            Harvest(b.id);
            o.Bounce(0.6f);
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

        // đèn công trình khi trời tối, theo cách Critters (GD_Claude/22 mục 5) nhưng không quầng (người dùng 2026-11-20): mỗi công trình có
        // mặt nạ tự sáng home_e_<def> cùng khung ảnh công trình (cửa sổ kính đổi màu đèn, lò, đèn lồng, pha lê: ArtGen/Home/night/home_emit.py),
        // vẽ ở lớp "tu_sang" trên lớp nhuộm nên không bị tối; shader UIIslandEmit tự đọc độ đêm _PokiNight (ban ngày tắt hẳn) và chập chờn.
        void NightLights()
        {
            if (!glowPrefab || !emitMat || S.home == null) return;
            var h = S.home;
            // khớp đèn với công trình có mặt nạ (đang xây thì chưa sáng)
            var want = h.buildings.Where(b => b.job != 1 && objs.ContainsKey(b.id) && Meta("home_e_" + b.def).sprite).ToList();
            if (want.Count != lights.Count || want.Where((b, i) => lights[i].id != b.id).Any())
            {
                foreach (var l in lights) Destroy(l.img.gameObject);
                lights.Clear();
                foreach (var b in want)
                {
                    var img = Ui.Spawn(glowPrefab, lightLayer);
                    Theme.SetSprite(img, Meta("home_e_" + b.def).sprite);
                    img.material = emitMat;
                    img.preserveAspect = false;
                    img.raycastTarget = false;
                    img.color = new Color(1f, 0.86f, 0.58f, 1f); // màu sáng cộng thêm (UIIslandEmit)
                    lights.Add((img, b.id));
                }
            }
            for (int i = 0; i < lights.Count; i++)
            {
                var (img, id) = lights[i];
                var o = objs[id];
                var rt = img.rectTransform;
                var ort = o.Rt;
                rt.anchorMin = ort.anchorMin;
                rt.anchorMax = ort.anchorMax;
                rt.pivot = ort.pivot;
                rt.sizeDelta = ort.sizeDelta;
                rt.anchoredPosition = ort.anchoredPosition;
                rt.localScale = ort.localScale; // công trình đang nhún (vừa chọn): đèn nhún theo
                img.enabled = o.gameObject.activeSelf; // đang dời: công trình ẩn, đèn ẩn theo
            }
        }

        // ---------- hướng dẫn đặt Cây bi (GD_Claude/25_FTUE.md chặng G, G3a–G3d) ----------

        float tutorT;

        // Cây bi đến cùng Nhà, người chơi tự đặt (người dùng 2026-11-23). Lần đầu: Xây → chọn Cây bi trong khay → kéo bóng ma, Đặt
        // (ba bước lặp: bấm Thôi / Xong giữa chừng thì lần sau dẫn lại; xong hẳn khi đã đặt cây, cờ TreePlaced), rồi chạm cây hái 10 bi
        // có sẵn (TreeTap). Cây sau (cấp 30, 50...) không dẫn: thẻ đầu khay, chấm "!" trên nút Nhà của sảnh. Update gọi nửa giây một lần.
        void Tutor()
        {
            var s = S;
            if (s?.home == null || shipArriving || (pier && pier.Busy) || App.Router == null || App.Router.Busy || !Guide.Idle) return;
            if (App.Modals != null && App.Modals.Count > 0) return;
            // C22–C24 (người dùng 2026-11-24): lần đầu về Nhà trong chuỗi bắt buộc, giới thiệu qua (không chi tiết) Nhà chính, ruộng
            // vườn, xưởng gỗ và kho, rồi mới tới Cây bi. Bản lưu đã xong chuỗi thì bỏ qua cả ba
            if (!Tutorial.Done(s, Tutorial.HomeWood))
            {
                if (Tutorial.CoreDone(s)) Guide.Skip(Tutorial.HomeMain, Tutorial.HomeFarm, Tutorial.HomeWood);
                else
                {
                    if (mode != Mode.Normal || ghost) return;
                    if (Intro(Tutorial.HomeMain, Loc.T("Đây là Nhà của bạn. Tướng làm việc ở đây, cả khi bạn vắng."), "main") ||
                        Intro(Tutorial.HomeFarm, Loc.T("Ruộng và vườn: tướng làm ở đây ra bi."), "field", "orchard") ||
                        Intro(Tutorial.HomeWood, Loc.T("Xưởng gỗ ra gỗ, Kho giữ gỗ. Gỗ dùng để xây và nâng cấp."), "sawmill", "storage"))
                        return;
                }
            }
            if (!Tutorial.Done(s, Tutorial.TreePlaced))
            {
                if (Home.TreesWaiting(s, D) <= 0)
                {
                    if (Home.CountOf(s.home, "tree") > 0) Guide.Skip(Tutorial.TreePlaced); // cây đã có chỗ (đặt sẵn, hoặc tự đặt)
                    return;
                }
                if (mode == Mode.Normal) Guide.Force(Tutorial.TreeBuild, "home.build", Loc.T("Cây bi đã về Nhà! Bấm Xây để đặt cây."), null, true);
                else if (mode == Mode.Build && !ghost) Guide.Force(Tutorial.TreeTray, "home.tray.tree", Loc.T("Chọn Cây bi. Đặt cây không tốn gì."), null, true);
                else if (ghost && ghostDef == "tree" && moveId < 0 && !(tap && tap.Grabbing))
                    Guide.Show(Tutorial.TreeSpot, Guide.Mode.Hint, "home.ghost", Loc.T("Kéo cây tới chỗ bạn thích, rồi bấm Đặt."), null, true, null, 30);
                return;
            }
            if (mode != Mode.Normal || ghost) return;
            if (!Tutorial.Done(s, Tutorial.TreeTap))
            {
                // cây đã hái hết trước khi kịp dẫn (10 bi có sẵn đã lấy): coi như xong, không để chuỗi bắt buộc chờ mãi
                if (Trees.Stock(s, D.Cfg, Now) <= 0)
                {
                    if (Tutorial.Done(s, Tutorial.TreeSeed)) Guide.Skip(Tutorial.TreeTap);
                    return;
                }
                var tb = s.home.buildings.FirstOrDefault(IsTree);
                if (tb == null || !objs.TryGetValue(tb.id, out var o) || !o) return;
                Guide.Mark("home.tree", o);
                Guide.Force(Tutorial.TreeTap, "home.tree", Loc.F("Chạm cây để hái bi. Mỗi cây ra {0} bi mỗi giờ, chứa được {1}.",
                    D.Cfg.trees.perHour.ToString("0.#"), D.Cfg.trees.cap.ToString("0")));
                return;
            }
            // C25: đi hết Nhà trong chuỗi bắt buộc thì gợi ý về sảnh (Cửa hàng mở ở đó), không chặn
            if (!Tutorial.CoreDone(s)) Guide.Hint(Tutorial.HomeBack, "home.sail", Loc.T("Về sảnh xem có gì mới!"), 10);
        }

        // giới thiệu qua một công trình (C22–C24): lướt máy tới, khoanh sáng, lời tướng đồng hành, chạm đâu cũng qua (Guide.SayAt).
        // Nhà chưa có công trình nào trong defs thì bỏ bước. true = đã xin hiện
        bool Intro(string id, string text, params string[] defs)
        {
            var s = S;
            if (Tutorial.Done(s, id)) return false;
            HomeBuilding b = null;
            foreach (var df in defs)
            {
                b = s.home.buildings.FirstOrDefault(x => x.def == df && objs.TryGetValue(x.id, out var ob) && ob);
                if (b != null) break;
            }
            if (b == null)
            {
                Guide.Skip(id);
                return false;
            }
            FocusOn(b, 0.45f);
            Guide.Mark("home.intro", objs[b.id]);
            return Guide.SayAt(id, "home.intro", text);
        }

        // ---------- chế độ ----------

        void SetMode(Mode m)
        {
            if (m == Mode.Build && mode != Mode.Build) StartSpread();
            mode = m;
            if (m != Mode.Build) EndGhost();
            selBuilding = selLot = -1;
            HideSel();
            if (hudBuild)
            {
                // hàng nút icon: đang xây / lát thì nút đó thành "Xong" (tích), các nút khác ẩn như chế độ xây của Critters
                hudBuild.SetCaption(m == Mode.Build ? Loc.T("Xong") : Loc.T("Xây"));
                hudBuild.SetIcon(Icon(m == Mode.Build ? "check" : "hammer"));
                hudBuild.gameObject.SetActive(m != Mode.Paint);
                if (hudPaint)
                {
                    hudPaint.SetCaption(m == Mode.Paint ? Loc.T("Xong") : Loc.T("Lát ô"));
                    hudPaint.SetIcon(Icon(m == Mode.Paint ? "check" : "pencil"));
                    hudPaint.gameObject.SetActive(m != Mode.Build);
                }
                if (hudHarvest) hudHarvest.gameObject.SetActive(m == Mode.Normal);
                if (hudSail) hudSail.gameObject.SetActive(m == Mode.Normal);
            }
            else
            {
                btnBuild.SetText(m == Mode.Build ? "Xong" : Loc.T("Xây"));
                btnPaint.SetText(m == Mode.Paint ? "Xong" : Loc.T("Lát ô"));
            }
            // gợi ý chỉ còn một dòng ngắn khi xây / lát; chế độ thường không gợi ý (người dùng 2026-11-22: bỏ dòng gợi ý dài)
            hint.text = m == Mode.Build ? Loc.T("Chọn thẻ để xây · chạm công trình để dời")
                : m == Mode.Paint ? Loc.T("Chọn loại ô rồi chạm đất · Cỏ để xoá")
                : "";
            if (ring && hint.transform.parent) hint.transform.parent.gameObject.SetActive(m != Mode.Normal);
            BuildTray();
        }

        // tấm xây (khay + tab) bật / tắt; prefab cũ chỉ có khay
        void SheetOn(bool on)
        {
            if (sheet) sheet.gameObject.SetActive(on);
            else if (tray) tray.gameObject.SetActive(on);
            if (ring && hint && hint.transform.parent) hint.transform.parent.gameObject.SetActive(on);
        }

        // bỏ chọn: tắt vòng nút (và bảng cũ nếu prefab chưa có vòng)
        void HideSel()
        {
            if (ring) ring.Hide();
            if (panel) panel.gameObject.SetActive(false);
        }

        bool SelOn => ring ? ring.On : panel && panel.gameObject.activeSelf;

        void BuildTray()
        {
            for (int i = tray.childCount - 1; i >= 0; i--) Destroy(tray.GetChild(i).gameObject);
            SheetOn(mode != Mode.Normal);
            // tab lọc (chỉ chế độ xây): Tất cả, Sản xuất, Hỗ trợ, Trang trí; tab đang chọn tô xanh
            if (tabs != null)
                for (int i = 0; i < tabs.Length; i++)
                {
                    if (!tabs[i]) continue;
                    tabs[i].gameObject.SetActive(mode == Mode.Build);
                    tabs[i].SetRole(i == tab ? BtnColor.Green : BtnColor.Paper);
                }
            if (sheet) tray.anchoredPosition = new Vector2(0, tray.anchoredPosition.y); // khay là nội dung cuộn ngang: về đầu
            if (mode == Mode.Build)
            {
                TreeTrayItem();
                foreach (var df in C.buildings.Where(b => b.kind != "main" && b.kind != "tree" && InTab(b)))
                {
                    var e = Home.CanBuild(S, D, df.id);
                    if (e == HomeErr.NotFound) continue;
                    if (df.reward && e == HomeErr.Locked) continue; // trang trí thưởng chưa có
                    var (w, o, _, _) = Home.BuildCost(df);
                    SketchButton btn;
                    if (trayIconPrefab)
                    {
                        var it = Ui.Spawn(trayIconPrefab, tray);
                        it.SetIcon(Icon("home_" + df.id), e == HomeErr.Ok); // icon_home_<mã> (ArtGen/Home/icons)
                        btn = it.Button;
                    }
                    else btn = Ui.Spawn(trayPrefab, tray);
                    string cost = (w > 0 ? Loc.F("{0} gỗ", w) : "") + (o > 0 ? Loc.F(" {0} quặng", o) : "");
                    btn.SetText($"{df.Name}\n{(e == HomeErr.Ok ? cost : Why(e, df))}");
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
                    btn.SetText($"{t.Name}\n{(t.wood > 0 ? t.wood + Loc.T(" gỗ") : "")}{(t.ore > 0 ? Loc.F(" {0} quặng", t.ore) : "")}");
                    if (t.id == paintTile) btn.SetRole(BtnColor.Green); // ô đang chọn tô xanh (phông không có dấu ✓, soát UI 2026-11-23)
                    var id = t.id;
                    btn.SetOnClick(() =>
                    {
                        paintTile = id;
                        BuildTray();
                    });
                }
            }
        }

        // Cây bi chờ đặt (mở cùng Nhà, 2026-11-23): thẻ đầu khay ở mọi tab, ghi số cây chờ, đặt miễn phí
        void TreeTrayItem()
        {
            int n = Home.TreesWaiting(S, D);
            if (n <= 0) return;
            var df = Home.Def(D.Cfg, "tree");
            SketchButton btn;
            if (trayIconPrefab)
            {
                var it = Ui.Spawn(trayIconPrefab, tray);
                it.SetIcon(Icon("home_tree"), true);
                btn = it.Button;
            }
            else btn = Ui.Spawn(trayPrefab, tray);
            btn.SetText($"{df.Name}{(n > 1 ? $" ×{n}" : "")}\n{Loc.T("Miễn phí")}");
            btn.SetOnClick(() => StartGhost("tree"));
            Guide.Mark("home.tray.tree", btn);
        }

        bool InTab(HomeBuildingDef df) => tabs == null || tabs.Length == 0 || tab switch
        {
            1 => df.kind == "prod",
            2 => df.kind == "support",
            3 => Home.IsDeco(df),
            _ => true,
        };

        static string Why(HomeErr e, HomeBuildingDef df) => e switch
        {
            HomeErr.HomeLevel => Loc.F("Nhà cấp {0}", df.home),
            HomeErr.Count => Loc.T("Đủ số"),
            HomeErr.Cost => Loc.T("Thiếu gỗ"),
            HomeErr.Builder => Loc.T("Thợ bận"),
            HomeErr.Locked => Loc.T("Chưa có"),
            _ => "",
        };

        void StartGhost(string def)
        {
            var pos = Home.FindSpot(S, D, def);
            if (pos == null)
            {
                App.Toasts.Show(Loc.T("Hết chỗ trống: dọn thêm rừng"), Icon("lock"));
                return;
            }
            EndGhost();
            ghost = Ui.Spawn(objPrefab, objLayer);
            ghostDef = def;
            ghostAt = new Vector2Int(pos.Value.gx, pos.Value.gy);
            UpdateGhost();
            ghost.Bounce();
            Guide.Mark("home.ghost", ghost);
            var df = Home.Def(D.Cfg, def);
            SheetOn(false);
            KeepVisible(CellTop(ghostAt.x + df.size / 2f, ghostAt.y + df.size / 2f));
            selPop = true;
            GhostRing();
        }

        // bóng ma đang đặt / dời: hai nút cạnh bóng ma như Critters (✗ Thôi, ✓ Đặt kèm giá); chỗ chưa đặt được thì ✓ khoá, nhãn ghi lý do
        void GhostRing()
        {
            if (!ghost) return;
            var df = Home.Def(D.Cfg, ghostDef);
            var e = Home.CanPlace(S, D, ghostDef, ghostAt.x, ghostAt.y, moveId);
            var (w, o, _, _) = Home.BuildCost(df);
            string cost = moveId >= 0 ? null : Cost(w, o);
            string title = moveId >= 0 ? Loc.F("Dời {0}", df.Name) : df.Name;
            string sub = e == HomeErr.Ok ? (moveId >= 0 ? Loc.T("Kéo hoặc chạm đất để đổi chỗ") : Loc.F("Cỡ {0}x{1} · kéo để đổi chỗ", df.size, df.size))
                : ErrText(e);
            if (!ring)
            {
                ShowPanel(title, sub, (Loc.T("Đặt"), PlaceGhost), (Loc.T("Thôi"), CancelGhost), (null, null));
                return;
            }
            var items = new List<RingItem>
            {
                new RingItem(Icon("close"), Loc.T("Thôi"), BtnColor.Red, CancelGhost),
                new RingItem(Icon("check"), Loc.T("Đặt"), BtnColor.Green, PlaceGhost, cost, e == HomeErr.Ok, () => App.Toasts.Show(ErrText(e), Icon("lock"))),
            };
            ring.Show(ghost.Rt, title, sub, items, selPop);
            selPop = false;
        }

        static string Cost(int wood, int ore) => wood <= 0 && ore <= 0 ? null
            : (wood > 0 ? Loc.F("{0} gỗ", wood) : "") + (wood > 0 && ore > 0 ? " · " : "") + (ore > 0 ? Loc.F("{0} quặng", ore) : "");

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
            ghost.Bounce(); // nhấc lên: nhún
            var df = Home.Def(D.Cfg, b.def);
            SheetOn(false); // khay che nửa màn: ẩn khi đang dời
            if (pan) KeepVisible(CellTop(b.gx + df.size / 2f, b.gy + df.size / 2f));
            App.Audio.Play("click");
            selPop = true;
            GhostRing();
        }

        // điểm bản đồ đang bị bảng chọn (nửa dưới) hoặc thanh trên che thì kéo máy cho nó ra giữa khung
        void KeepVisible(Vector2 mapPt)
        {
            if (!landView || !landView.On) return;
            var v = landView.ToView(mapPt);
            var size = landView.ViewSize;
            // vòng nút: trên đầu vật cần chỗ cho quạt nút (~300 px), dưới chỉ có hàng nút; prefab cũ: bảng chữ che nửa dưới
            float low = ring ? size.y - BottomInset - 140 : size.y * 0.58f, high = TopInset + (ring ? 300 : 80);
            if (v.y > low || v.y < high || v.x < 60 || v.x > size.x - 60) landView.Show(mapPt, landView.Zoom, 0.3f);
        }

        const string MoveText = "Nhấn giữ rồi kéo công trình, hoặc chạm đất để chọn chỗ mới (xanh là đặt được), rồi bấm Đặt.";

        // ---------- nhấn giữ, kéo (HomeTap) ----------

        // nhấn xuống trúng bóng ma đang xây / dời: cầm lên kéo luôn
        bool OnPress(Vector2 p)
        {
            if (!ghost || mode != Mode.Build) return false;
            var cell = CellAt(p);
            int n = Home.Def(D.Cfg, ghostDef).size;
            bool foot = cell.x >= ghostAt.x && cell.y >= ghostAt.y && cell.x < ghostAt.x + n && cell.y < ghostAt.y + n;
            // bóng ma Cây bi: nhấn trúng tán lá cũng cầm được
            if (!foot && !(ghostDef == "tree" && TreeRect(ghost).Contains(p))) return false;
            grabOffset = cell - ghostAt;
            UpdateGhost();
            return true;
        }

        // giữ yên trên công trình (chế độ thường hoặc xây): nhấc lên, cùng ngón kéo đi
        bool OnHold(Vector2 p)
        {
            if (mode == Mode.Paint) return false;
            var cell = CellAt(p);
            var b = HitAt(p, cell);
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
            UpdateGhost(); // hạ xuống (UpdateGhost dựng lại vòng ✓ ✗ theo chỗ mới)
            ghost.Bounce(0.6f);
        }

        void CancelGhost()
        {
            EndGhost();
            HideSel();
        }

        // bỏ bóng ma; đang dời thì hiện lại công trình ở chỗ cũ
        void EndGhost()
        {
            if (ghost) Destroy(ghost.gameObject);
            ghost = null;
            ghostDef = null;
            Guide.Mark("home.ghost", null);
            GridGhost(false);
            if (moveId >= 0 && objs.TryGetValue(moveId, out var o) && o) o.gameObject.SetActive(true);
            moveId = -1;
            if (tray) SheetOn(mode != Mode.Normal);
        }

        string BuildText(HomeBuildingDef df)
        {
            var (w, o, _, min) = Home.BuildCost(df);
            string what = df.kind == "prod" ? Loc.F("Làm ra: {0}. Hợp hệ {1}.", OutName(df.output), Elements.Name(df.elem)) : df.kind == "support" ? Support(df) : Loc.F("Điểm đẹp +{0}.", df.beauty);
            return Loc.F("{0}\nGiá: {1} gỗ{2}{3}. Cỡ {4}x{5}.", what, w, (o > 0 ? Loc.F(", {0} quặng", o) : ""), (min > 0 ? $", {Clock(min)}" : ""), df.size, df.size);
        }

        static string Support(HomeBuildingDef df) => df.id switch
        {
            "storage" => Loc.T("Thêm sức chứa gỗ, quặng."),
            "well" => Loc.T("Tưới ruộng, vườn quanh giếng."),
            "waterwheel" => Loc.T("Tưới rộng; phải sát suối."),
            "hotspring" => Loc.T("Tướng nghỉ nhanh hơn."),
            _ => "",
        };

        static string OutName(string o) => o switch
        {
            "balls" => "bi",
            "wood" => Loc.T("gỗ"),
            "ore" => Loc.T("quặng, ít đá tiến hóa"),
            "fish" => Loc.T("câu cá: bi, thẻ, cúp"),
            "stones" => Loc.T("đá tiềm năng (ăn quặng)"),
            "bread" => Loc.T("bánh (tướng ăn thì hết nghỉ)"),
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
            GhostRing(); // ✓ khoá / mở, lý do theo chỗ mới
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
            var at = ghostAt;
            // cây bi đầu tiên đặt xong: hướng dẫn đặt cây xong, về chế độ thường để chạm cây hái bi (bước TreeTap)
            bool firstTree = moveId < 0 && ghostDef == "tree" && !Tutorial.Done(S, Tutorial.TreePlaced);
            if (moveId < 0 && ghostDef == "tree") Guide.Skip(Tutorial.TreePlaced, Tutorial.TreeBuild, Tutorial.TreeTray, Tutorial.TreeSpot);
            EndGhost();
            HideSel();
            App.Save.Save();
            if (firstTree) SetMode(Mode.Normal);
            Render();
            BuildTray();
            // đặt xuống: công trình nhún một cái
            var placed = Home.At(S.home, D.Cfg, at.x, at.y);
            if (placed != null && objs.TryGetValue(placed.id, out var po)) po.Bounce(0.8f);
        }

        static string ErrText(HomeErr e) => e switch
        {
            HomeErr.Overlap => Loc.T("Chồng lên công trình khác"),
            HomeErr.Locked => Loc.T("Ô rừng chưa dọn"),
            HomeErr.Blocked => Loc.T("Chỗ này không xây được"),
            HomeErr.NeedOre => Loc.T("Mỏ phải đặt trên mạch quặng"),
            HomeErr.NeedStream => Loc.T("Cối nước phải sát suối"),
            HomeErr.OutOfMap => Loc.T("Ra ngoài đảo"),
            HomeErr.Cost => Loc.T("Thiếu gỗ hoặc quặng"),
            HomeErr.Builder => Loc.T("Đội thợ đang bận"),
            HomeErr.HomeLevel => Loc.T("Cần nâng Nhà chính"),
            HomeErr.PlayerLevel => Loc.T("Cần lên cấp"),
            HomeErr.Count => Loc.T("Đã đủ số công trình loại này"),
            HomeErr.MaxLevel => Loc.T("Đã tối đa"),
            HomeErr.NotAdjacent => Loc.T("Phải kề đất đã mở"),
            HomeErr.Busy => Loc.T("Đang bận"),
            HomeErr.TotalSlots => Loc.T("Hết chỗ tướng (nâng Nhà chính)"),
            HomeErr.BallSlots => Loc.T("Hết chỗ ra bi (lên cấp)"),
            HomeErr.HeroBusy => Loc.T("Tướng đang bận"),
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
                    var hit = HitAt(p, cell);
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
            // chạm trúng tán lá cây bi cũng tính (HitAt), không chỉ ô dưới chân (người dùng 2026-11-23)
            var b = HitAt(p, cell);
            if (b == null && !Home.InMap(C, cell.x, cell.y))
            {
                HideSel();
                return;
            }
            if (b != null)
            {
                // Cây bi có bi: chạm là hái hết mọi cây (không mở bảng)
                if (IsTree(b) && Trees.Stock(s, d.Cfg, Now) > 0)
                {
                    HarvestTrees(b);
                    return;
                }
                selBuilding = b.id;
                selLot = -1;
                App.Audio.Play("click");
                selPop = true;
                Pick(objs.TryGetValue(b.id, out var bo) ? bo : null, true);
                RefreshPanel();
                return;
            }
            int lot = Home.LotOfCell(C, cell.x, cell.y);
            if (!s.home.lots.Contains(lot) && Home.LotKind(C, lot) != "hill" && LotTappable(lot))
            {
                selLot = lot;
                selBuilding = -1;
                App.Audio.Play("click");
                selPop = true;
                PickLot(lot);
                RefreshPanel();
                return;
            }
            selBuilding = selLot = -1;
            HideSel();
        }

        // ô rừng chạm vào có hiện bảng không (người dùng 2026-11-20: "click vào mấy ô rừng chưa mở được thì đừng hiện gì"): đang dọn hoặc
        // mở được thì hiện; còn khoá (chưa liền đất đã mở, chưa đủ cấp người chơi) thì không hiện gì, chạm như đất trống. Mở ô miễn phí
        // (2026-11-25) nên không còn trường hợp thiếu gỗ, thợ.
        bool LotTappable(int lot)
        {
            if (S.home.clearing.ContainsKey(lot)) return true;
            return Home.CanClear(S, D, lot) == HomeErr.Ok;
        }

        // vật đang chọn → vòng nút quanh nó (Critters): nhãn tên + một dòng trạng thái dưới chân, nút tròn icon trên đầu; chữ dài (sản lượng
        // từng ô tướng, điều kiện lên cấp) vào nút "Chi tiết". Gọi lại mỗi giây (đếm giờ) thì chỉ thay chữ, không nảy lại.
        void RefreshPanel()
        {
            var s = S;
            var d = D;
            var h = s.home;
            double now = Now;
            if (selLot >= 0)
            {
                forests.TryGetValue(selLot, out var mk);
                if (h.clearing.TryGetValue(selLot, out var until))
                {
                    int lotC = selLot;
                    ShowSel(mk, Loc.T("Đang dọn rừng"), Loc.F("Còn {0}", Clock((until - now) / 60000)), null,
                        new RingItem(Icon("tv"), Loc.T("Nhanh 30'"), BtnColor.Purple, () => SpeedUp(-1, lotC)));
                    return;
                }
                var e = Home.CanClear(s, d, selLot);
                var ring = Home.RingOf(C, selLot);
                int reward = ring?.reward ?? 0, balls = ring?.balls ?? 0;
                string detail = Loc.F("Mở từ cấp {0}. Miễn phí, mở ngay. Mở xong rơi {1} gỗ, {2} bi để thả.", Home.LotPlayer(C, selLot), reward, balls) +
                                (e == HomeErr.Ok ? "" : $"\n{ErrText(e)}.");
                int lot = selLot;
                ShowSel(mk, Loc.T("Ô rừng"), e == HomeErr.Ok ? Loc.F("Mở miễn phí · rơi {0} gỗ", reward) : ErrText(e), detail,
                    new RingItem(Icon("hammer"), Loc.T("Dọn"), BtnColor.Green, () => ClearLot(lot), Loc.T("Miễn phí"), e == HomeErr.Ok,
                        () => App.Toasts.Show(ErrText(e), Icon("lock"))));
                return;
            }
            var b = Home.Find(h, selBuilding);
            if (b == null)
            {
                HideSel();
                return;
            }
            var df = Home.Def(d.Cfg, b.def);
            string title = $"{df.Name}{(Home.IsDeco(df) ? "" : Loc.F(" cấp {0}", b.level))}";
            var lines = new List<string>();
            string sub = null;
            if (b.job != 0)
            {
                lines.Add(Loc.F("{0}: còn {1}.", (b.job == 1 ? Loc.T("Đang xây") : Loc.T("Đang lên cấp")), Clock((b.until - now) / 60000)));
                sub = Loc.F("{0} · còn {1}", (b.job == 1 ? Loc.T("Đang xây") : Loc.T("Đang lên cấp")), Clock((b.until - now) / 60000));
            }
            int stock = Home.Stock(b);
            if (df.kind == "prod")
            {
                lines.Add(Loc.F("Làm ra {0}. Có {1} chờ thu.", OutName(df.output), stock));
                int working = 0;
                for (int i = 0; i < b.slots.Count; i++)
                {
                    var sl = b.slots[i];
                    if (sl.hero != null) working++;
                    lines.Add(sl.hero == null ? Loc.F("Ô {0}: trống", i + 1)
                        : Loc.F("Ô {0}: {1}, {2:0.#}/giờ, còn {3}", i + 1, d.Hero(sl.hero)?.name, Home.Rate(s, d, sl.hero, b), Clock(sl.energy * 60)));
                }
                sub ??= stock > 0 ? Loc.F("Có {0} chờ thu · {1}/{2} tướng", stock, working, b.slots.Count)
                    : Loc.F("{0}/{1} tướng đang làm", working, b.slots.Count);
            }
            else if (df.kind == "support")
            {
                lines.Add(Support(df));
                sub ??= Support(df);
            }
            else if (df.kind == "tree")
            {
                // chạm cây có bi thì hái luôn, nên vòng chỉ hiện khi cây chưa có bi nào chín
                var cfg = d.Cfg;
                double cap = Trees.Cap(s, cfg, now), rate = Trees.Rate(s, cfg, now);
                var st = Trees.Of(s, now).stock;
                double have = b.tree >= 0 && b.tree < st.Count ? st[b.tree] : 0;
                lines.Add(Loc.F("Mỗi cây {0} bi mỗi giờ, chứa tối đa {1:0} bi; đầy thì ngừng.", FarmScene.Dec(rate), cap));
                if (have < cap && rate > 0)
                {
                    string next = Clock((Math.Floor(have) + 1 - have) / rate * 60);
                    lines.Add(Loc.F("Bi kế tiếp sau {0}. Có bi thì chạm cây để hái hết.", next));
                    sub ??= Loc.F("Bi kế tiếp sau {0}", next);
                }
            }
            else if (df.kind == "main")
            {
                lines.Add(Loc.F("Gỗ {0:0}/{1:0}, quặng {2:0}/{3:0}. Thợ {4}/{5}.", h.wood, Home.WoodCap(h, d.Cfg), h.ore, Home.OreCap(h, d.Cfg), Home.Busy(h), Home.Builders(h, C)));
                sub ??= Loc.F("Thợ {0}/{1}", Home.Busy(h), Home.Builders(h, C));
            }
            else if (Home.IsDeco(df)) sub ??= Loc.F("Điểm đẹp +{0}", df.beauty);
            var up = Home.UpgradeCost(d.Cfg, b);
            var ue = Home.CanUpgrade(s, d, b.id);
            if (up != null && ue != HomeErr.Ok) lines.Add(Loc.F("Lên cấp: {0}.", ErrText(ue)));
            bool prod = df.kind == "prod" && b.job != 1;
            int bid = b.id;
            var items = new List<RingItem>();
            // thu (có đồ chờ thu), giao tướng / đổi ca, nhanh 30' (đang xây) hoặc lên cấp / cất, dời, chi tiết
            if (prod && stock > 0) items.Add(new RingItem(Icon(OutIcon(df.output)), Loc.T("Thu"), BtnColor.Orange, () => Harvest(bid)));
            if (prod)
            {
                // chỗ trống thì chọn tướng vào chỗ đó; đủ người thì đổi ca ô mệt nhất (hộp chọn tướng có nút rút ra)
                int empty = b.slots.FindIndex(sl => sl.hero == null);
                int tired = b.slots.Count == 0 ? -1 : b.slots.Select((sl, i) => (sl, i)).OrderBy(x => x.sl.energy).First().i;
                if (empty >= 0) items.Add(new RingItem(Icon("team"), Loc.T("Giao tướng"), BtnColor.Blue, () => Picker(bid, empty)));
                else if (tired >= 0) items.Add(new RingItem(Icon("team"), Loc.T("Đổi ca"), BtnColor.Blue, () => Picker(bid, tired)));
            }
            if (b.job != 0) items.Add(new RingItem(Icon("tv"), Loc.T("Nhanh 30'"), BtnColor.Purple, () => SpeedUp(bid, -1)));
            else if (Home.IsDeco(df)) items.Add(new RingItem(Icon("down"), Loc.T("Cất"), BtnColor.Yellow, () => StoreDeco(bid)));
            else if (up != null)
            {
                var upErr = ue;
                items.Add(new RingItem(Icon("up"), Loc.T("Lên cấp"), BtnColor.Green, () => Upgrade(bid), Cost(up.Value.wood, up.Value.ore),
                    ue == HomeErr.Ok, () => App.Toasts.Show(ErrText(upErr), Icon("lock"))));
            }
            items.Add(new RingItem(Icon("swap"), Loc.T("Dời"), BtnColor.Yellow, () =>
            {
                var mb = Home.Find(S.home, bid);
                if (mb != null) StartMove(mb);
            }));
            objs.TryGetValue(b.id, out var target);
            ShowSel(target, title, sub, string.Join("\n", lines), items.ToArray());
        }

        // hiện vòng nút quanh target; detail khác rỗng thì thêm nút "Chi tiết" (hộp chữ đầy đủ). Prefab chưa có vòng thì về bảng chữ cũ.
        void ShowSel(Component target, string title, string sub, string detail, params RingItem[] items)
        {
            var list = new List<RingItem>(items);
            if (!string.IsNullOrEmpty(detail))
            {
                string t = title, body = detail;
                list.Add(new RingItem(Icon("info"), Loc.T("Chi tiết"), BtnColor.Paper, () => App.Modals.Alert(t, body, "OK", null, false)));
            }
            if (!ring || !target)
            {
                (string, Action) At(int i) => i < list.Count ? (list[i].label, list[i].act) : (null, null);
                ShowPanel(title, string.IsNullOrEmpty(detail) ? sub : detail, At(0), At(1), At(2), At(3));
                return;
            }
            ring.Show((RectTransform)target.transform, title, sub, list, selPop);
            selPop = false;
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

        void ClearLot(int lot)
        {
            var e = Home.ClearLot(S, D, Now, lot);
            if (e == HomeErr.Ok && S.home.cleared.Count > 0) ReportCleared(); // dọn tức thì (0 phút): cây bay, bi bay trước lần lưu
            else Done(e);
        }
        void Upgrade(int id) => Done(Home.Upgrade(S, D, Now, id));

        void StoreDeco(int id)
        {
            if (!Home.Store(S, D, id)) return;
            selBuilding = -1;
            HideSel();
            Done(HomeErr.Ok);
        }

        void SpeedUp(int id, int lot)
        {
            Ads.Show(AdGate.HomeSpeed, ok =>
            {
                if (!ok) return;
                Home.SpeedUp(S, D, Now, id, lot);
                // quảng cáo rút giờ làm ô rừng xong ngay: cây bay, bi bay (ReportCleared phải chạy trước lần lưu)
                if (S.home.cleared.Count > 0)
                {
                    App.Audio.Play("click");
                    ReportCleared();
                }
                else Done(HomeErr.Ok);
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
                App.Toasts.Show(Loc.T("Chưa có gì để thu"), Icon("info"));
                return;
            }
            var parts = new List<string>();
            if (y.balls > 0) parts.Add(Loc.F("+{0} bi", y.balls));
            if (y.wood > 0) parts.Add(Loc.F("+{0} gỗ", y.wood));
            if (y.ore > 0) parts.Add(Loc.F("+{0} quặng", y.ore));
            if (y.evo > 0) parts.Add(Loc.F("+{0} đá tiến hóa", y.evo));
            if (y.stones > 0) parts.Add(Loc.F("+{0} đá tiềm năng", y.stones));
            if (y.bread > 0) parts.Add(Loc.F("+{0} bánh", y.bread));
            if (y.other.Count > 0) parts.Add(Loc.F("+{0} thưởng câu", y.other.Count));
            if (y.deco.Count > 0) parts.Add(Loc.T("+cúp câu cá"));
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
                    pet.UseRig(true); // rig chạy walk / idle, đêm sáng nhẹ (người dùng 2026-11-20)
                    pet.PassPan = false; // kéo trên tướng đang làm / nghỉ không dời máy (FarmPet.OnBeginDrag)
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
                selPop = true;
                ShowSel(pet, Loc.F("{0} đang nghỉ", hd.name), Loc.F("Còn {0:0} phút · có {1} bánh", Math.Ceiling(left), h.bread),
                    Loc.F("Còn {0:0} phút. Có {1} bánh (Bếp làm ra): cho ăn thì hết nghỉ ngay.", Math.Ceiling(left), h.bread),
                    new RingItem(Icon("bun"), Loc.T("Cho ăn"), BtnColor.Orange, () =>
                    {
                        var e = Home.Feed(S, D, Now, id);
                        HideSel();
                        if (e == HomeErr.Ok) App.Toasts.Show(Loc.F("{0} hết nghỉ", hd.name), Icon("flame"));
                        Done(e);
                    }, null, h.bread > 0, () => App.Toasts.Show(Loc.T("Chưa có bánh: Bếp làm ra bánh"), Icon("bun"))));
                return;
            }
            if (pet.Spot < 0) return;
            selBuilding = pet.Spot / 8;
            selLot = -1;
            selPop = true;
            RefreshPanel();
            if (objs.TryGetValue(selBuilding, out var wo)) Pick(wo, true); // công trình tướng đang làm sáng lên
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
            // cầm tướng thì máy đứng yên (người dùng 2026-11-20 và 2026-11-23: "tap và hold tướng thì cam tự di chuyển"): bỏ hẳn tự trôi khi
            // ngón tới mép (dải mép nằm sát thanh trên, hàng nút dưới nên cầm tướng gần đó là máy chạy). Công trình ngoài khung: ngón thứ hai
            // kéo đất (HomeTap chuyển cho LandView), tướng vẫn bám ngón đang cầm (FarmPet.Update đặt lại theo ngón mỗi khung)
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
                App.Toasts.Show(Loc.F("{0} đủ người: chạm công trình để đổi ca", df.Name), Icon("team"));
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
            App.Toasts.Show(Loc.F("{0} vào {1}: {2} {3}/giờ{4}", hd.name, df.Name, FarmScene.Dec(Home.Rate(s, d, pet.Hero, b)), FarmHeroRow.Unit(df.output), (match ? Loc.T(" (hợp hệ)") : "")), Icon(OutIcon(df.output)));
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
                if (fxPool.Count >= 120) return; // ô rừng dọn xong: mỗi cây bay lên một cụm bụi (HomeScene.Forest.cs)
                fx = Ui.Spawn(fxPrefab, fxLayer);
                fxPool.Add(fx);
            }
            fx.Play(s, c, fxLayer.InverseTransformPoint(objLayer.TransformPoint(pos)), vel, gravity, life, size0, size1, spin, pop, drag);
        }
    }
}
