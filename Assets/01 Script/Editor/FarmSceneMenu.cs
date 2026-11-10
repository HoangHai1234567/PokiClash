// Trang trại thành cảnh thật (người dùng dặn 2026-11-10). Menu "PokiClash/Prefab/Trang trại: cảnh thật" (chạy lại được, dựng lại các lớp):
// - nhập ảnh Assets/03 Art/Farm (farm_bg.png và props/farm_*.png, đưa vào bằng ArtGen/SideMeta/import_farm.py) thành sprite;
// - prefab mục Items/ThuTrangTrai (FarmPet), Items/ChoLamTrangTrai (FarmSlot), Items/HatTrangTrai (FarmFx);
// - Screens/Farm: Canvas/Nen: tắt mặt bàn gỗ, bật khung_anh; anh_nen_farm_bg là ảnh nền (bọc lớp kéo "keo", HubPan trên khung_anh);
//   trong ảnh nền: bang_khu (bảng tên 5 khu), cho_lam (8 chỗ làm), vung (bãi cỏ, ổ rơm: chỉ là khung toạ độ), thu (lớp thú), hat (lớp hạt);
//   Canvas/An toan/Khung: tắt trang giấy và khung cuộn lưới cũ, thêm hang_nut ở đáy (gợi ý, năng suất ×2, Thu hoạch, Tự xếp, ×2).
// Toạ độ theo ảnh 1024 x 1536 (gốc trên trái), trùng ArtGen/SideMeta/build_farm.py (SPOTS) và balance.json farm.spots. Sau khi dựng,
// chỉnh chỗ đứng, bảng, bãi cỏ thẳng trong prefab (chạy lại menu thì về toạ độ này).
using System.IO;
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class FarmSceneMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/Farm.prefab";
        const string PetPath = "Assets/04 Prefabs/Items/ThuTrangTrai.prefab";
        const string SlotPath = "Assets/04 Prefabs/Items/ChoLamTrangTrai.prefab";
        const string FxPath = "Assets/04 Prefabs/Items/HatTrangTrai.prefab";
        const string ArtDir = "Assets/03 Art/Farm/";
        const float W = 1024, H = 1536;

        // chỗ đứng (thứ tự balance.json farm.spots: duck1, veg1, orchard1, bakery, smithy, duck2, veg2, orchard2) và hướng nhìn khi làm
        static readonly (float x, float y, float face)[] Spots =
        {
            (640, 700, 1), (200, 1200, 1), (190, 700, 1), (800, 1250, -1), (850, 960, -1), (820, 690, -1), (380, 1200, -1), (360, 700, -1),
        };

        // bảng tên khu: loại, tên, hình đồ nghề (props/farm_<tên>), icon hệ, toạ độ
        static readonly (string kind, string name, string icon, string elem, float x, float y)[] Signs =
        {
            ("duck", "Ao vịt", "sack", "e_thuy", 735, 455),
            ("orchard", "Vườn cây", "apple", "e_moc", 275, 425),
            ("veg", "Ruộng rau", "carrot", "e_tho", 290, 1272),
            ("bakery", "Lò bánh", "bread", "e_hoa", 625, 1150),
            ("smithy", "Xưởng nông cụ", "hammer", "e_kim", 870, 728),
        };

        // bãi cỏ (bầu dục nội tiếp) và ổ rơm: x0, y0, x1, y1 trên ảnh
        static readonly Vector4 Meadow = new Vector4(300, 845, 700, 1025), Bed = new Vector4(80, 950, 250, 1020);
        static readonly string[] PropNames = { "hoe", "can", "basket", "bread", "hammer", "sack", "apple", "carrot", "dust", "spark", "smoke", "heart" };

        static ArtLibrary art;
        static Sprite Icon(string n) => art ? art.Icon(n) : null;

        [MenuItem("PokiClash/Prefab/Trang trại: cảnh thật", priority = 63)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            art = Load<ArtLibrary>();
            Theme.Init(assets);
            var bg = ImportSprite(ArtDir + "farm_bg.png", 2048);
            var props = new Sprite[System.Enum.GetValues(typeof(FarmProp)).Length];
            for (int i = 0; i < PropNames.Length; i++) props[i] = ImportSprite(ArtDir + "props/farm_" + PropNames[i] + ".png", 256);
            if (!bg) Debug.LogWarning("[Trang trại] Chưa có " + ArtDir + "farm_bg.png (chạy ArtGen/SideMeta/import_farm.py): nền để màu cỏ.");

            var fx = BuildFx();
            var slot = BuildSlot();
            var pet = BuildPet(assets.prefabs);
            BuildScreen(bg, props, pet, slot, fx);
            AssetDatabase.SaveAssets();
            Debug.Log($"[Trang trại] Đã dựng {PetPath}, {SlotPath}, {FxPath} và cảnh trong {ScreenPath}.");
        }

        // ---------- chạy không cần bấm menu (Unity dùng chung nhiều session) ----------
        // Temp/farm_build.flag: biên dịch xong và không Play thì dựng prefab một lần rồi xoá cờ.
        // Temp/farm_tour.flag: vào Play, chạy tour "Trang trại" của PlayTour (ảnh Temp/PokiShots 180+), xong tour thì Stop.
        const string TourMenu = "PokiClash/Thử/Trang trại: tự xếp, tua giờ, thu hoạch, đổi ca (đang Play)";
        static double nextPoll, tourStart; // tourStart: lúc gọi tour (quá 150 giây chưa xong thì Stop)

        static string Flag(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            if (!EditorApplication.isPlayingOrWillChangePlaymode)
            {
                if (File.Exists(Flag("farm_build.flag")))
                {
                    File.Delete(Flag("farm_build.flag"));
                    Build();
                }
                else if (File.Exists(Flag("farm_tour.flag")))
                {
                    File.Delete(Flag("farm_tour.flag"));
                    SessionState.SetBool("FarmTour", true);
                    tourStart = EditorApplication.timeSinceStartup; // tính giờ từ lúc vào Play
                    EditorApplication.isPlaying = true;
                }
                if (!SessionState.GetBool("FarmTour", false)) tourStart = 0;
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                Debug.LogWarning("[Trang trại] Tour quá 150 giây chưa xong: dừng Play.");
                tourStart = 0;
                Application.logMessageReceived -= TourLog;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("FarmTour", false) && App.I != null && App.Router != null &&
                App.Router.CurrentRoot != null)
            {
                // màn mở game chỉ tắt khi chạm hoặc chuyển scene: tắt luôn để tour chạy
                SessionState.SetBool("FarmTour", false);
                BootTitle.Dismiss();
                tourStart = EditorApplication.timeSinceStartup;
                Application.logMessageReceived += TourLog;
                EditorApplication.ExecuteMenuItem(TourMenu);
            }
        }

        static void TourLog(string msg, string stack, LogType type)
        {
            if (!msg.StartsWith("[Thử] Xong trang trại")) return;
            Application.logMessageReceived -= TourLog;
            tourStart = 0;
            EditorApplication.delayCall += () => EditorApplication.isPlaying = false;
        }

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));

        static Sprite ImportSprite(string path, int max)
        {
            if (!File.Exists(path)) return null;
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (ti && (ti.textureType != TextureImporterType.Sprite || ti.maxTextureSize != max || ti.mipmapEnabled))
            {
                ti.textureType = TextureImporterType.Sprite;
                ti.spriteImportMode = SpriteImportMode.Single;
                ti.mipmapEnabled = false;
                ti.alphaIsTransparency = true;
                ti.maxTextureSize = max;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        // ---------- dựng nút ----------

        static RectTransform Node(Transform parent, string name, params System.Type[] types)
        {
            var go = new GameObject(name, new[] { typeof(RectTransform) }.Concat(types).ToArray());
            go.layer = LayerMask.NameToLayer("UI");
            var rt = (RectTransform)go.transform;
            if (parent) rt.SetParent(parent, false);
            return rt;
        }

        static RectTransform At(RectTransform rt, Vector2 anchor, Vector2 pos, Vector2 size, Vector2 pivot)
        {
            rt.anchorMin = rt.anchorMax = anchor;
            rt.pivot = pivot;
            rt.anchoredPosition = pos;
            rt.sizeDelta = size;
            return rt;
        }

        static RectTransform Fill(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return rt;
        }

        static Image Img(Transform parent, string name, Sprite s, Color c, bool raycast = false, bool sliced = false)
        {
            var img = Node(parent, name, typeof(CanvasRenderer), typeof(Image)).GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.preserveAspect = !sliced;
            img.raycastTarget = raycast;
            return img;
        }

        static Image Hit(GameObject go)
        {
            var img = go.GetComponent<Image>();
            if (!img) img = go.AddComponent<Image>();
            img.sprite = null;
            img.color = new Color(1, 1, 1, 0);
            img.raycastTarget = true;
            return img;
        }

        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, float outline = 0)
        {
            var t = Node(parent, name, typeof(CanvasRenderer), typeof(TextMeshProUGUI)).GetComponent<TextMeshProUGUI>();
            t.font = font;
            if (outline > 0)
            {
                var m = Theme.Outlined(font, outline);
                if (m) t.fontSharedMaterial = m;
            }
            t.fontSize = size;
            t.color = color;
            t.alignment = TextAlignmentOptions.Center;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }

        static T Save<T>(GameObject root, string path) where T : Component
        {
            try
            {
                return PrefabUtility.SaveAsPrefabAsset(root, path).GetComponent<T>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- prefab mục ----------

        static FarmFx BuildFx()
        {
            var rt = Node(null, "HatTrangTrai", typeof(CanvasRenderer), typeof(Image), typeof(FarmFx));
            At(rt, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(48, 48), new Vector2(0.5f, 0.5f));
            var img = rt.GetComponent<Image>();
            img.preserveAspect = true;
            img.raycastTarget = false;
            rt.GetComponent<FarmFx>().Setup(img);
            return Save<FarmFx>(rt.gameObject, FxPath);
        }

        static FarmSlot BuildSlot()
        {
            var root = Node(null, "ChoLamTrangTrai", typeof(CanvasRenderer), typeof(Image), typeof(ClickCatcher), typeof(FarmSlot));
            At(root, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(170, 90), new Vector2(0.5f, 0.5f));
            Hit(root.gameObject);
            var p = new FarmSlot.Parts { click = root.GetComponent<ClickCatcher>() };

            p.ground = Img(root, "dat", Sketch.DashRing, Color.white);
            p.ground.preserveAspect = false;
            At(p.ground.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(150, 60), new Vector2(0.5f, 0.5f));

            p.plus = Img(root, "cong", Sketch.Round, Theme.CardFill);
            At(p.plus.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 54), new Vector2(66, 66), new Vector2(0.5f, 0.5f));
            var plusText = Text(p.plus.transform, "chu", Theme.Title, 54, Theme.GreenD);
            Fill(plusText.rectTransform);
            plusText.text = "+";

            p.lockIcon = Img(root, "khoa", Icon("lock"), Color.white);
            At(p.lockIcon.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 46), new Vector2(60, 60), new Vector2(0.5f, 0.5f));
            p.lockText = Text(root, "khoa_chu", Theme.Bold, 26, Theme.Paper, 0.25f);
            At(p.lockText.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, -2), new Vector2(160, 34), new Vector2(0.5f, 0.5f));

            // bong bóng bi tích trên đầu tướng
            var bubble = Img(root, "bong_bong", Sketch.Round, Theme.CardFill, true);
            At(bubble.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 215), new Vector2(84, 84), new Vector2(0.5f, 0.5f));
            p.bubble = bubble.gameObject;
            p.bubbleClick = bubble.gameObject.AddComponent<ClickCatcher>();
            var ball = Img(bubble.transform, "bi", Icon("ball"), Color.white);
            At(ball.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 4), new Vector2(54, 54), new Vector2(0.5f, 0.5f));
            p.stock = Text(bubble.transform, "so", Theme.Title, 30, Theme.Paper, 0.3f);
            At(p.stock.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(30, -30), new Vector2(80, 36), new Vector2(0.5f, 0.5f));

            // vòng sức còn cạnh đầu
            var ring = Node(root, "vong");
            At(ring, new Vector2(0.5f, 0.5f), new Vector2(84, 100), new Vector2(58, 58), new Vector2(0.5f, 0.5f));
            p.ringRoot = ring.gameObject;
            var ringBg = Img(ring, "nen", Sketch.Round, Theme.Paper);
            Fill(ringBg.rectTransform);
            p.ring = Img(ring, "suc", Sketch.Ring360, Theme.Green);
            Fill(p.ring.rectTransform);
            p.ring.type = Image.Type.Filled;
            p.ring.fillMethod = Image.FillMethod.Radial360;
            p.ring.fillOrigin = (int)Image.Origin360.Top;
            p.ring.fillClockwise = false;
            p.ringText = Text(ring, "gio", Theme.Bold, 22, Theme.Ink, 0.22f);
            At(p.ringText.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, -42), new Vector2(100, 28), new Vector2(0.5f, 0.5f));

            root.GetComponent<FarmSlot>().Setup(p);
            return Save<FarmSlot>(root.gameObject, SlotPath);
        }

        static FarmPet BuildPet(UiKit kit)
        {
            var root = Node(null, "ThuTrangTrai", typeof(CanvasRenderer), typeof(Image), typeof(FarmPet));
            At(root, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(130, 165), new Vector2(0.5f, 0f));
            Hit(root.gameObject);
            var p = new FarmPet.Parts();
            var bottom = new Vector2(0.5f, 0);

            p.shadow = Img(root, "bong", Sketch.Dot, new Color(0.17f, 0.13f, 0.09f, 0.26f));
            p.shadow.preserveAspect = false;
            At(p.shadow.rectTransform, bottom, new Vector2(0, 2), new Vector2(118, 28), new Vector2(0.5f, 0.5f));

            p.body = At(Node(root, "than"), bottom, Vector2.zero, new Vector2(160, 180), bottom);
            p.flip = At(Node(p.body, "lat"), bottom, Vector2.zero, new Vector2(160, 180), bottom);
            p.portrait = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, p.flip)).GetComponent<HeroPortrait>();
            p.portrait.name = "chan_dung";
            // ảnh chân dung: chân ở 6% đáy khung (HeroArt.FootY) → hạ xuống cho chân trùng gốc
            At(p.portrait.Rect, bottom, new Vector2(0, -FarmPet.Height * HeroArt.FootY), new Vector2(FarmPet.Height * HeroArt.W / HeroArt.H, FarmPet.Height), bottom);
            foreach (var g in p.portrait.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
            p.tool = Img(p.flip, "do", null, Color.white);
            At(p.tool.rectTransform, bottom, new Vector2(46, 46), new Vector2(84, 84), new Vector2(0.25f, 0.25f));
            p.tool.gameObject.SetActive(false);

            p.emote = Img(root, "cam_xuc", null, Color.white);
            At(p.emote.rectTransform, bottom, new Vector2(46, FarmPet.Height + 10), new Vector2(56, 56), new Vector2(0.5f, 0.5f));
            p.emote.gameObject.SetActive(false);
            p.tag = Text(root, "ten", Theme.Bold, 26, Theme.Ink, 0.25f);
            At(p.tag.rectTransform, bottom, new Vector2(0, FarmPet.Height + 18), new Vector2(320, 36), bottom);
            p.tag.color = Theme.Paper;
            p.tag.gameObject.SetActive(false);

            root.GetComponent<FarmPet>().Setup(p);
            return Save<FarmPet>(root.gameObject, PetPath);
        }

        // ---------- màn hình ----------

        static void BuildScreen(Sprite bg, Sprite[] props, FarmPet pet, FarmSlot slotPrefab, FarmFx fx)
        {
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                RectTransform Find(string n) =>
                    root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == n);
                var scene = root.GetComponent<FarmScene>();
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var khung = Find("khung_anh");
                var frame = Find("anh_nen_farm_bg");
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!scene || !nen || !khung || !frame || !safe)
                {
                    Debug.LogError("[Trang trại] Screens/Farm thiếu FarmScene, Canvas/Nen, khung_anh, anh_nen_farm_bg hoặc Canvas/An toan/Khung.");
                    return;
                }

                // nền: tắt mặt bàn gỗ (menu Giao diện), bật khung ảnh; hai bên màu cỏ
                foreach (Transform c in nen) c.gameObject.SetActive(c == khung || c.name == "nen_hai_ben");
                var sides = Find("nen_hai_ben");
                if (sides)
                {
                    var si = sides.GetComponent<Image>();
                    if (si)
                    {
                        si.sprite = null;
                        si.color = Theme.Hex("#8cc96a");
                        si.raycastTarget = false;
                    }
                }

                // lớp kéo bọc ảnh nền
                var keo = Find("keo");
                if (!keo)
                {
                    keo = Fill(Node(khung, "keo"));
                    keo.SetSiblingIndex(frame.GetSiblingIndex());
                    frame.SetParent(keo, false);
                }
                var fit = frame.GetComponent<AspectRatioFitter>();
                fit.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
                fit.aspectRatio = W / H;
                var frameImg = frame.GetComponent<Image>();
                Theme.SetSprite(frameImg, bg);
                frameImg.color = bg ? Color.white : Theme.Hex("#9fd27c");
                frameImg.preserveAspect = false;
                frameImg.raycastTarget = true; // nhận kéo bản đồ
                var pan = khung.GetComponent<HubPan>();
                if (!pan) pan = khung.gameObject.AddComponent<HubPan>();
                pan.Setup(keo, new Vector2(110 / 1080f, 70 / 1920f));

                foreach (var n in new[] { "bang_khu", "cho_lam", "vung", "thu", "hat" })
                {
                    var old = frame.Find(n);
                    if (old) Object.DestroyImmediate(old.gameObject);
                }
                Vector2 A(float x, float y) => new Vector2(x / W, 1 - y / H);

                // bảng tên khu
                var signs = Fill(Node(frame, "bang_khu"));
                foreach (var s in Signs) Sign(signs, s.kind, s.name, s.icon, s.elem, A(s.x, s.y));

                // chỗ làm
                var slotLayer = Fill(Node(frame, "cho_lam"));
                var slots = new FarmSlot[Spots.Length];
                var face = new float[Spots.Length];
                for (int i = 0; i < Spots.Length; i++)
                {
                    var sl = ((GameObject)PrefabUtility.InstantiatePrefab(slotPrefab.gameObject, slotLayer)).GetComponent<FarmSlot>();
                    sl.name = "cho_" + i;
                    var rt = sl.Rt;
                    rt.anchorMin = rt.anchorMax = A(Spots[i].x, Spots[i].y);
                    rt.anchoredPosition = Vector2.zero;
                    slots[i] = sl;
                    face[i] = Spots[i].face;
                }

                // bãi cỏ, ổ rơm (khung toạ độ, không vẽ)
                var zones = Fill(Node(frame, "vung"));
                RectTransform Area(string n, Vector4 r)
                {
                    var rt = Node(zones, n);
                    rt.anchorMin = A(r.x, r.w);
                    rt.anchorMax = A(r.z, r.y);
                    rt.offsetMin = rt.offsetMax = Vector2.zero;
                    return rt;
                }
                var meadow = Area("bai_co", Meadow);
                var bed = Area("o_rom", Bed);

                var pets = Fill(Node(frame, "thu"));
                var fxLayer = Fill(Node(frame, "hat"));

                scene.SetupScene(pets, fxLayer, meadow, bed, slots, face, pet, fx, props);

                // giao diện cũ: trang giấy, khung cuộn lưới → tắt; nút và chữ dời xuống hàng đáy
                var so = new SerializedObject(scene);
                var info = (TextMeshProUGUI)so.FindProperty("info").objectReferenceValue;
                var boostLeft = (TextMeshProUGUI)so.FindProperty("boostLeft").objectReferenceValue;
                var buttons = new[] { "harvest", "auto", "boost" }.Select(k => (Component)so.FindProperty(k).objectReferenceValue).ToArray();
                BottomBar(safe, info, boostLeft, buttons);
                foreach (var n in new[] { "cuon", "trang" })
                {
                    var t = Find(n);
                    if (t) t.gameObject.SetActive(false);
                }

                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // bảng gỗ giấy: icon khu, tên, chấm hệ; neo ở toạ độ ảnh, không nhận chạm
        static void Sign(RectTransform parent, string kind, string name, string icon, string elem, Vector2 anchor)
        {
            var plate = Img(parent, "bang_" + kind, Sketch.Pill, new Color(1f, 0.98f, 0.92f, 0.94f), false, true);
            var rt = plate.rectTransform;
            rt.anchorMin = rt.anchorMax = anchor;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = Vector2.zero;
            var hl = plate.gameObject.AddComponent<HorizontalLayoutGroup>();
            hl.padding = new RectOffset(14, 20, 6, 6);
            hl.spacing = 8;
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = true;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var fit = plate.gameObject.AddComponent<ContentSizeFitter>();
            fit.horizontalFit = fit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            void Ic(string n, Sprite s, float size)
            {
                var i = Img(plate.transform, n, s, Color.white);
                var le = i.gameObject.AddComponent<LayoutElement>();
                le.preferredWidth = le.preferredHeight = size;
            }
            Ic("icon", AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + "props/farm_" + icon + ".png") ?? Icon("seed"), 48);
            var t = Text(plate.transform, "ten", Theme.Bold, 30, Theme.Ink);
            t.text = name;
            Ic("he", Icon(elem), 34);
        }

        static void BottomBar(RectTransform safe, TextMeshProUGUI info, TextMeshProUGUI boostLeft, Component[] buttons)
        {
            var old = safe.Find("hang_nut");
            var bar = old as RectTransform;
            if (!bar)
            {
                bar = Node(safe, "hang_nut");
            }
            bar.anchorMin = new Vector2(0, 0);
            bar.anchorMax = new Vector2(1, 0);
            bar.pivot = new Vector2(0.5f, 0);
            bar.anchoredPosition = new Vector2(0, 24);
            bar.sizeDelta = new Vector2(-32, 250);
            bar.SetAsLastSibling();

            var hint = bar.Find("goi_y") as RectTransform;
            if (!hint) hint = Img(bar, "goi_y", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.93f), false, true).rectTransform;
            hint.anchorMin = new Vector2(0, 1);
            hint.anchorMax = new Vector2(1, 1);
            hint.pivot = new Vector2(0.5f, 1);
            hint.anchoredPosition = Vector2.zero;
            hint.sizeDelta = new Vector2(0, 72);
            if (info)
            {
                foreach (var le in info.GetComponents<LayoutElement>()) Object.DestroyImmediate(le);
                info.transform.SetParent(hint, false);
                Fill(info.rectTransform).offsetMin = new Vector2(16, 4);
                info.rectTransform.offsetMax = new Vector2(-16, -4);
                info.fontSize = 26;
                info.enableAutoSizing = true;
                info.fontSizeMin = 18;
                info.fontSizeMax = 26;
                info.textWrappingMode = TextWrappingModes.Normal;
                info.alignment = TextAlignmentOptions.Center;
                info.color = Theme.Ink;
            }
            if (boostLeft)
            {
                foreach (var le in boostLeft.GetComponents<LayoutElement>()) Object.DestroyImmediate(le);
                boostLeft.transform.SetParent(bar, false);
                At(boostLeft.rectTransform, new Vector2(0.5f, 1), new Vector2(0, 40), new Vector2(700, 40), new Vector2(0.5f, 0));
                boostLeft.alignment = TextAlignmentOptions.Center;
            }

            var row = bar.Find("nut") as RectTransform;
            if (!row) row = Node(bar, "nut", typeof(HorizontalLayoutGroup));
            row.anchorMin = new Vector2(0, 0);
            row.anchorMax = new Vector2(1, 0);
            row.pivot = new Vector2(0.5f, 0);
            row.anchoredPosition = Vector2.zero;
            row.sizeDelta = new Vector2(0, 150);
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = 16;
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            foreach (var b in buttons)
            {
                if (!b) continue;
                foreach (var le in b.GetComponents<LayoutElement>()) le.ignoreLayout = false;
                b.transform.SetParent(row, false);
                var rt = (RectTransform)b.transform;
                rt.sizeDelta = new Vector2(330, Mathf.Max(110, rt.sizeDelta.y));
            }
        }
    }
}
