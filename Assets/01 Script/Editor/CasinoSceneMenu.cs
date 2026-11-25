// Màn đảo Casino "Bến Lữ Khách" (GD_Claude/29_DaoCasino.md, mốc C2). Menu "PokiClash/Prefab/Đảo Casino/Đảo: dựng màn" (chạy lại được):
// - hình (C8, gen theo lớp: ArtGen/Casino/lop/xu_ly_2k.py): đảo trống casino_dao.png (2048 x 1360, hiện 1:1) + công trình rời
//   casino_ct_<id>.png đặt đúng khung trong casino_art.json (px ảnh đảo, gốc trên trái); lều sự kiện casino_ct_leu_<lều> thay cọc bãi
//   (casino_ct_bai_*) khi sự kiện mở;
// - prefab mục Items/DiemCasino (CasinoSpot): vùng chạm trong suốt, bảng tên nổi trên đỉnh, khoá, chấm đỏ;
// - Screens/Casino: lần đầu chép từ Screens/Cave (giữ canvas, khung, vùng nội dung), thay CaveScene bằng CasinoScene; nền: ảnh đảo bọc
//   lớp kéo (HubPan), lớp công trình xếp theo đáy, các điểm chạm neo theo khung công trình (bảng Spots); giao diện: dòng
//   tin + hàng nút Bói sao, Lịch lữ khách, Về sảnh;
// - scene Assets/00 Scenes/Casino.unity và Build Settings.
// - bến tàu nam với con tàu của game (chuyến tàu sảnh ↔ đảo đi chếch, ShipVoyage), vành mây rời (CloudRing), sáng tối theo giờ (DayNight);
// - mỗi công trình một vật riêng ct_<mã> có CasinoBuilding (đổi hình từng cái: thay casino_ct_<mã>.png rồi chạy lại menu).
// Menu "Máy bi: nút Ra đảo": thêm nút vào Screens/Machine (MachineScene.toIsland).
// Chạy không cần bấm (Unity dùng chung nhiều phiên): Temp/casino_build.flag → biên dịch xong, không Play thì dựng cả hai rồi xoá cờ;
// Temp/casino_tour.flag → vào Play, chụp màn đảo và màn máy bi vào Temp/PokiShots/casino/, rồi Stop (bản lưu sao lưu, trả lại).
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class CasinoSceneMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/Casino.prefab";
        const string BaseScreenPath = "Assets/04 Prefabs/Screens/Cave.prefab";
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string SpotPath = "Assets/04 Prefabs/Items/DiemCasino.prefab";
        const string ScenePath = "Assets/00 Scenes/Casino.unity";
        const string ArtDir = "Assets/03 Art/Casino/";
        const string BasePath = ArtDir + "casino_dao.png";
        const string ArtJson = ArtDir + "casino_art.json";
        static readonly Color Sea = new Color(8 / 255f, 222 / 255f, 251 / 255f); // màu tấm vân biển chung (tau_bien) của sảnh / chuyến tàu

        // điểm chạm (thứ tự CasinoScene.Ids) → ảnh công trình làm khung chạm ("a|b": gộp khung); bảng lịch: khung riêng (px bản 2k)
        static readonly (string id, string art)[] Spots =
        {
            ("tower", "thap"), ("fishing", "ben_cau"), ("race", "dua"), ("market", "cho"), ("underground", "hang"), ("inn", "quan_tro"),
            ("booth_blackjack", "bai_tren|leu_blackjack"), ("booth_roulette", "bai_phai|leu_roulette"), ("booth_slot", "bai_trai|leu_slot"),
            ("board", null),
        };
        static readonly Vector4 BoardRect = new Vector4(940, 1020, 1110, 1160);
        // bến tàu nam (ảnh casino_ct_ben_tau không vẽ thuyền): con tàu của game đậu ở mặt nước trước đầu trái bến, mũi lên; ra khơi về nam
        // (chuyến tàu sảnh ↔ đảo nhận / giao tàu ở điểm cuối, ngoài mép dưới màn). Toạ độ local khung đảo (gốc tâm ảnh 2048 x 1360, y lên)
        // toạ độ ảnh đảo (px, gốc trên trái), đổi sang local khung (gốc tâm, y lên) lúc dựng: mặt nước ngay trước đầu trái bến
        static readonly Vector2 DockPx = new Vector2(660, 1395);
        static readonly Vector2[] SouthPx = { new Vector2(650, 1540), new Vector2(610, 2000) };
        const float ShipScale = 0.9f, ShipSpeed = 520;
        const string GlowItemPath = "Assets/04 Prefabs/Items/HinhDong.prefab";

        // cọc bãi và lều theo thứ tự CasinoScene.Booths
        static readonly string[] Pads = { "bai_tren", "bai_phai", "bai_trai" };
        static readonly string[] Tents = { "leu_blackjack", "leu_roulette", "leu_slot" };

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        [MenuItem("PokiClash/Prefab/Đảo Casino/Đảo: dựng màn", priority = 70)]
        public static void Build()
        {
            if (!DataImporter.Run(false)) Debug.LogError("[Đảo Casino] Nhập dữ liệu lỗi: đảo sẽ thiếu số liệu.");
            var assets = Load<UiAssets>();
            if (!assets)
            {
                Debug.LogError("[Đảo Casino] Không thấy UiAssets.");
                return;
            }
            Theme.Init(assets);
            var art = ImportArt();
            if (art == null) return;
            var spot = BuildSpot();
            if (!BuildScreen(assets, art, spot)) return;
            MakeScene();
            AssetDatabase.SaveAssets();
            Debug.Log("[Đảo Casino] Đã dựng " + ScreenPath + ", " + ScenePath);
        }

        // ---------- ảnh nền tạm ----------

        sealed class Art
        {
            public Sprite baseSprite;
            public float w, h;
            public Dictionary<string, Vector4> rects = new Dictionary<string, Vector4>(); // x0, y0, x1, y1 px ảnh đảo
            public Dictionary<string, Sprite> sprites = new Dictionary<string, Sprite>();
        }

        static Sprite LoadSprite(string path, int max)
        {
            AssetDatabase.ImportAsset(path);
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (ti && (ti.textureType != TextureImporterType.Sprite || ti.maxTextureSize < max))
            {
                ti.textureType = TextureImporterType.Sprite;
                ti.maxTextureSize = Mathf.Max(ti.maxTextureSize, max);
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        static Art ImportArt()
        {
            if (!File.Exists(ArtJson) || !File.Exists(BasePath))
            {
                Debug.LogError("[Đảo Casino] Thiếu " + ArtJson + " hoặc " + BasePath + " (chạy ArtGen/Casino/lop/xu_ly_2k.py).");
                return null;
            }
            var meta = J.Obj(MiniJson.Parse(File.ReadAllText(ArtJson)));
            var art = new Art { baseSprite = LoadSprite(BasePath, 2048), w = (float)J.Num(meta, "w"), h = (float)J.Num(meta, "h") };
            foreach (var kv in J.Obj(meta, "items"))
            {
                var o = J.Obj(kv.Value);
                art.rects[kv.Key] = new Vector4((float)J.Num(o, "x0"), (float)J.Num(o, "y0"), (float)J.Num(o, "x1"), (float)J.Num(o, "y1"));
                var sp = LoadSprite(ArtDir + "casino_ct_" + kv.Key + ".png", 1024);
                if (sp) art.sprites[kv.Key] = sp;
                else Debug.LogWarning("[Đảo Casino] Thiếu ảnh casino_ct_" + kv.Key + ".png");
            }
            return art;
        }

        static void Anchor(RectTransform rt, Art art, Vector4 r)
        {
            rt.anchorMin = new Vector2(r.x / art.w, 1 - r.w / art.h);
            rt.anchorMax = new Vector2(r.z / art.w, 1 - r.y / art.h);
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            rt.pivot = new Vector2(0.5f, 0.5f);
        }

        // ---------- prefab điểm chạm ----------

        static CasinoSpot BuildSpot()
        {
            var root = HomeSceneMenu.Node(null, "DiemCasino", typeof(CanvasRenderer), typeof(Image), typeof(ClickCatcher), typeof(CasinoSpot));
            HomeSceneMenu.At(root, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(240, 240), new Vector2(0.5f, 0.5f));
            var hitImg = root.GetComponent<Image>();
            hitImg.color = new Color(1, 1, 1, 0); // vùng chạm trong suốt (Image alpha 0 vẫn nhận chạm)
            hitImg.raycastTarget = true;

            // bảng tên nổi trên đỉnh khung công trình
            var plate = HomeSceneMenu.Img(root, "bang", Sketch.Pill, new Color(1f, 0.98f, 0.92f, 0.97f), false, true);
            var prt = plate.rectTransform;
            HomeSceneMenu.At(prt, new Vector2(0.5f, 1), new Vector2(0, 4), new Vector2(260, 86), new Vector2(0.5f, 0));
            var vl = plate.gameObject.AddComponent<VerticalLayoutGroup>();
            vl.padding = new RectOffset(26, 26, 8, 10);
            vl.spacing = -2;
            vl.childAlignment = TextAnchor.MiddleCenter;
            vl.childControlWidth = vl.childControlHeight = true;
            vl.childForceExpandWidth = vl.childForceExpandHeight = false;
            var fit = plate.gameObject.AddComponent<ContentSizeFitter>();
            fit.horizontalFit = fit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            var title = HomeSceneMenu.Text(plate.transform, "ten", 32, Theme.Ink);
            title.textWrappingMode = TextWrappingModes.NoWrap;
            var sub = HomeSceneMenu.Text(plate.transform, "phu", 24, Theme.Ink2);
            sub.textWrappingMode = TextWrappingModes.NoWrap;
            sub.font = Theme.Bold;

            // khoá ở góc trái bảng, chấm đỏ góc phải (không theo bố cục)
            var art = Load<ArtLibrary>();
            var lockImg = HomeSceneMenu.Img(plate.transform, "khoa", art ? art.Icon("lock") : null, Color.white);
            lockImg.preserveAspect = true;
            lockImg.gameObject.AddComponent<LayoutElement>().ignoreLayout = true;
            HomeSceneMenu.At(lockImg.rectTransform, new Vector2(0, 0.5f), new Vector2(-6, 0), new Vector2(46, 46), new Vector2(0.5f, 0.5f));
            var dot = HomeSceneMenu.Img(plate.transform, "cham", Sketch.Dot, Theme.Red);
            dot.gameObject.AddComponent<LayoutElement>().ignoreLayout = true;
            HomeSceneMenu.At(dot.rectTransform, new Vector2(1, 1), new Vector2(-4, -4), new Vector2(30, 30), new Vector2(0.5f, 0.5f));

            var cs = root.GetComponent<CasinoSpot>();
            cs.Setup(root.GetComponent<ClickCatcher>(), plate, lockImg, dot, title, sub);
            try
            {
                return PrefabUtility.SaveAsPrefabAsset(root.gameObject, SpotPath).GetComponent<CasinoSpot>();
            }
            finally
            {
                Object.DestroyImmediate(root.gameObject);
            }
        }

        // ---------- màn hình ----------

        static bool BuildScreen(UiAssets assets, Art art, CasinoSpot spotPrefab)
        {
            if (!File.Exists(ScreenPath))
            {
                if (!AssetDatabase.CopyAsset(BaseScreenPath, ScreenPath))
                {
                    Debug.LogError("[Đảo Casino] Không chép được " + BaseScreenPath + " sang " + ScreenPath);
                    return false;
                }
                AssetDatabase.ImportAsset(ScreenPath);
            }
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                root.name = "Casino";
                RectTransform Find(string n) => root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == n);
                // thay CaveScene bằng CasinoScene, giữ canvas và vùng nội dung của SceneRoot
                var scene = root.GetComponent<CasinoScene>();
                RectTransform content = null;
                if (!scene)
                {
                    var old = root.GetComponent<SceneRoot>();
                    PokiCanvas view = null;
                    if (old)
                    {
                        var so = new SerializedObject(old);
                        view = so.FindProperty("view").objectReferenceValue as PokiCanvas;
                        content = so.FindProperty("content").objectReferenceValue as RectTransform;
                        Object.DestroyImmediate(old);
                    }
                    scene = root.AddComponent<CasinoScene>();
                    scene.SetupView(view ? view : root.GetComponentInChildren<PokiCanvas>(true), content);
                }
                else content = scene.Content;
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var khung = Find("khung_anh");
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !khung || !safe)
                {
                    Debug.LogError("[Đảo Casino] Screens/Casino thiếu Canvas/Nen, khung_anh hoặc Canvas/An toan/Khung.");
                    return false;
                }
                var sea = Sea;
                foreach (Transform c in nen) c.gameObject.SetActive(c == khung || c.name == "nen_hai_ben");
                var sides = Find("nen_hai_ben");
                if (sides && sides.GetComponent<Image>() is Image si)
                {
                    si.sprite = null;
                    si.color = sea;
                    si.raycastTarget = false;
                }
                if (khung.GetComponent<Image>() is Image ki)
                {
                    ki.sprite = null;
                    ki.color = sea;
                }

                // ảnh nền màn cũ (anh_nen_*) thành ảnh đảo, bọc lớp kéo "keo"
                var frame = Find("anh_nen_casino") ?? khung.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name.StartsWith("anh_nen_"));
                if (!frame)
                {
                    frame = HomeSceneMenu.Node(khung, "anh_nen_casino", typeof(CanvasRenderer), typeof(Image), typeof(AspectRatioFitter));
                    HomeSceneMenu.Fill(frame);
                }
                frame.name = "anh_nen_casino";
                var keo = Find("keo");
                if (!keo)
                {
                    keo = HomeSceneMenu.Fill(HomeSceneMenu.Node(khung, "keo"));
                    keo.SetSiblingIndex(frame.GetSiblingIndex());
                }
                if (frame.parent != keo) frame.SetParent(keo, false);
                frame.gameObject.SetActive(true);
                // ảnh đảo cỡ thật 1:1 (2048 x 1360) giữa lớp kéo: vừa chiều cao vùng giữa thanh trên và hàng nút, kéo ngang
                var fitter = frame.GetComponent<AspectRatioFitter>();
                if (fitter) Object.DestroyImmediate(fitter);
                // mép trên ảnh (đường chân trời) nằm sát dưới thanh trên; biển là lớp lát riêng phủ quá khung nên không lộ ranh
                HomeSceneMenu.At(frame, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - art.h / 2), new Vector2(art.w, art.h), new Vector2(0.5f, 0.5f));
                // khung: trong suốt, chỉ nhận kéo; bên trong: lớp biển (tấm vân biển chung của sảnh / chuyến tàu, lát lặp, phủ quá khung, DayNight
                // làm tối về đêm như biển sảnh) rồi lớp đất (ảnh đảo, nước trong suốt; doi_bien.py) — biển hai đảo nối liền cả màu lẫn vân
                var frameImg = frame.GetComponent<Image>();
                Theme.SetSprite(frameImg, null);
                frameImg.color = new Color(1, 1, 1, 0);
                frameImg.raycastTarget = true; // nhận kéo bản đồ
                foreach (Transform c in frame.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject); // lớp cũ, chữ của màn gốc
                var seaImg = HomeSceneMenu.Img(frame, "bien", AssetDatabase.LoadAssetAtPath<Sprite>(ShipBuild.ArtDir + "tau_bien.png"), Color.white);
                seaImg.type = Image.Type.Tiled;
                HomeSceneMenu.Fill(seaImg.rectTransform).offsetMin = new Vector2(-1600, -1600);
                seaImg.rectTransform.offsetMax = new Vector2(1600, 1600);
                var landImg = HomeSceneMenu.Img(frame, "dat", art.baseSprite, Color.white);
                HomeSceneMenu.Fill(landImg.rectTransform);
                var pan = khung.GetComponent<HubPan>() ?? khung.gameObject.AddComponent<HubPan>();
                // kéo ngang đúng tới mép ảnh ((2048 − 1080) / 2 ≈ 0,45 bề ngang màn), dọc không kéo xuống (mép trên đã sát thanh trên):
                // không bao giờ lộ mép ảnh / nền ngoài khung
                pan.Setup(keo, new Vector2((art.w - 1080) / 2f / 1080f, 0f));
                pan.SetPads(0, 80);

                // công trình: mỗi ảnh một Image đúng khung, xếp theo đáy (gần người xem vẽ sau); lều sự kiện tắt sẵn, cọc bãi bật
                var layerArt = HomeSceneMenu.Fill(HomeSceneMenu.Node(frame, "cong_trinh"));
                var images = new Dictionary<string, Image>();
                foreach (var kv in art.rects.OrderBy(kv => kv.Value.w))
                {
                    if (!art.sprites.TryGetValue(kv.Key, out var sp)) continue;
                    var img = HomeSceneMenu.Img(layerArt, "ct_" + kv.Key, sp, Color.white);
                    Anchor(img.rectTransform, art, kv.Value);
                    img.gameObject.AddComponent<CasinoBuilding>().Setup(kv.Key, img); // mỗi công trình một vật riêng, đổi hình riêng
                    img.gameObject.SetActive(!kv.Key.StartsWith("leu_"));
                    images[kv.Key] = img;
                }
                Image Pick(string k) => images.TryGetValue(k, out var i) ? i : null;
                scene.SetupBooths(Pads.Select(Pick).ToArray(), Tents.Select(Pick).ToArray());

                // mây vành rời quanh đảo (dùng chung với Nhà): chuyến tàu qua mây mang theo, toả quanh tàu; chừa lối ở bến tàu
                var clouds = HomeSceneMenu.Fill(HomeSceneMenu.Node(frame, "may", typeof(CanvasGroup)));
                var cg = clouds.GetComponent<CanvasGroup>();
                cg.blocksRaycasts = false;
                cg.interactable = false;
                Vector2 L(Vector2 px) => new Vector2(px.x - art.w / 2, art.h / 2 - px.y);
                var cloudImgs = HomeSceneMenu.BuildClouds(clouds, new Vector2(art.w, art.h), DockPx.x);
                clouds.gameObject.AddComponent<CloudRing>().Setup(cloudImgs, 290);

                // bến tàu: con tàu của game (ShipBuild.Pier), trên lớp mây, dưới lớp sáng tối
                var pier = ShipBuild.Pier(frame, L(DockPx), Vector2.up, SouthPx.Select(L).ToArray(), null, ShipScale, ShipSpeed);

                // sáng tối theo giờ máy (DayNight, DayCycle dùng chung với sảnh, đảo, Nhà): nhuộm, tia nắng; biển ngoài ảnh tối theo đêm
                // lớp nhuộm phủ quá khung ảnh 3000 px mỗi phía (khung_anh có RectMask2D cắt theo màn): mây, nền ngoài khung cũng nhuộm cùng
                // một lớp, không lộ ranh mặt nạ (lỗi người dùng chỉ ra 2026-11-25)
                var dayRoot = HomeSceneMenu.Fill(HomeSceneMenu.Node(frame, "sang_toi"));
                dayRoot.offsetMin = new Vector2(-3000, -3000);
                dayRoot.offsetMax = new Vector2(3000, 3000);
                var mul = AssetDatabase.LoadAssetAtPath<Material>("Assets/03 Art/Islands/day_multiply.mat");
                var raysMat = AssetDatabase.LoadAssetAtPath<Material>("Assets/03 Art/Islands/day_rays.mat");
                var tint = HomeSceneMenu.Img(dayRoot, "nhuom", null, Color.white);
                HomeSceneMenu.Fill(tint.rectTransform);
                tint.material = mul;
                var rays = HomeSceneMenu.Img(dayRoot, "nang", null, new Color(1, 1, 1, 0));
                HomeSceneMenu.Fill(rays.rectTransform);
                rays.material = raysMat;
                var lamps = HomeSceneMenu.Fill(HomeSceneMenu.Node(dayRoot, "den_dao"));
                var dn = dayRoot.gameObject.AddComponent<DayNight>();
                // không truyền "biển ngoài ảnh": lớp nhuộm đã phủ cả nền ngoài khung (truyền thêm thì tối gấp đôi)
                dn.Setup(tint, rays, lamps, AssetDatabase.LoadAssetAtPath<GameObject>(GlowItemPath)?.GetComponent<Image>(),
                    AssetDatabase.LoadAssetAtPath<TextAsset>("Assets/03 Art/Islands/island_anim.json"), "casino", new Graphic[] { seaImg }, null);
                var dso = new SerializedObject(dn);
                var cArr = dso.FindProperty("clouds");
                if (cArr != null)
                {
                    cArr.arraySize = cloudImgs.Length;
                    for (int i = 0; i < cloudImgs.Length; i++) cArr.GetArrayElementAtIndex(i).objectReferenceValue = cloudImgs[i];
                    dso.ApplyModifiedPropertiesWithoutUndo();
                }
                if (!mul || !raysMat) Debug.LogWarning("[Đảo Casino] Chưa có day_multiply.mat / day_rays.mat: đảo chưa nhuộm theo giờ.");

                // điểm chạm: khung = ảnh công trình (bãi lều: gộp khung cọc và khung lều)
                var layer = HomeSceneMenu.Fill(HomeSceneMenu.Node(frame, "diem"));
                layer.SetAsLastSibling();
                var spots = new List<CasinoSpot>();
                foreach (var sp in Spots)
                {
                    var c = ((GameObject)PrefabUtility.InstantiatePrefab(spotPrefab.gameObject, layer)).GetComponent<CasinoSpot>();
                    c.name = "diem_" + sp.id;
                    c.SetId(sp.id);
                    Vector4 r = BoardRect;
                    if (sp.art != null)
                    {
                        bool first = true;
                        foreach (var a in sp.art.Split('|'))
                        {
                            if (!art.rects.TryGetValue(a, out var ar)) continue;
                            r = first ? ar : new Vector4(Mathf.Min(r.x, ar.x), Mathf.Min(r.y, ar.y), Mathf.Max(r.z, ar.z), Mathf.Max(r.w, ar.w));
                            first = false;
                        }
                    }
                    Anchor(c.Rt, art, r);
                    spots.Add(c);
                }

                // giao diện: bỏ giao diện của màn gốc trong khung an toàn (giữ vùng nội dung của SceneRoot, xoá con của nó)
                foreach (Transform c in safe.Cast<Transform>().ToList())
                    if (c != content && c.name != "giao_dien_dao") Object.DestroyImmediate(c.gameObject);
                if (content)
                    foreach (Transform c in content.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject);
                var oldUi = safe.Find("giao_dien_dao");
                if (oldUi) Object.DestroyImmediate(oldUi.gameObject);
                var ui = HomeSceneMenu.Fill(HomeSceneMenu.Node(safe, "giao_dien_dao", typeof(CanvasGroup)));
                var bar = HomeSceneMenu.Node(ui, "hang_nut");
                HomeSceneMenu.At(bar, new Vector2(0.5f, 0), new Vector2(0, 28), new Vector2(1040, 250), new Vector2(0.5f, 0));
                var tip = HomeSceneMenu.Img(bar, "goi_y", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.94f), false, true);
                HomeSceneMenu.At(tip.rectTransform, new Vector2(0.5f, 1), Vector2.zero, new Vector2(1000, 84), new Vector2(0.5f, 1));
                var info = HomeSceneMenu.Text(tip.transform, "chu", 26, Theme.Ink);
                HomeSceneMenu.Fill(info.rectTransform).offsetMin = new Vector2(20, 6);
                info.rectTransform.offsetMax = new Vector2(-20, -6);
                info.enableAutoSizing = true;
                info.fontSizeMin = 18;
                info.fontSizeMax = 26;
                var row = HomeSceneMenu.Node(bar, "nut", typeof(HorizontalLayoutGroup));
                HomeSceneMenu.At(row, new Vector2(0.5f, 0), Vector2.zero, new Vector2(1040, 140), new Vector2(0.5f, 0));
                var hl = row.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 18;
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var lucky = HomeSceneMenu.Button(assets, row, "boi_sao", Loc.T("Bói sao"), BtnColor.Yellow, new Vector2(320, 120));
                var board = HomeSceneMenu.Button(assets, row, "lich", Loc.T("Lịch lữ khách"), BtnColor.Paper, new Vector2(340, 120));
                var home = HomeSceneMenu.Button(assets, row, "ve_sanh", Loc.T("Về sảnh"), BtnColor.Green, new Vector2(320, 120));

                scene.Setup(spots.ToArray(), lucky, board, home, info);
                scene.SetupPier(pier, pan, ui.GetComponent<CanvasGroup>());
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
                return true;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static void MakeScene()
        {
            if (!File.Exists(ScenePath))
            {
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
                var prev = SceneManager.GetActiveScene();
                SceneManager.SetActiveScene(scene);
                var screen = AssetDatabase.LoadAssetAtPath<GameObject>(ScreenPath);
                ((GameObject)PrefabUtility.InstantiatePrefab(screen)).name = SceneIds.Casino;
                SceneManager.SetActiveScene(prev);
                EditorSceneManager.SaveScene(scene, ScenePath);
                EditorSceneManager.CloseScene(scene, true);
            }
            else
            {
                // bản sao prefab trong scene có thể còn giá trị đè cũ (khung từng giãn theo màn): trả về đúng prefab
                var scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Additive);
                foreach (var go in scene.GetRootGameObjects())
                    if (PrefabUtility.IsPartOfPrefabInstance(go))
                        PrefabUtility.RevertPrefabInstance(PrefabUtility.GetOutermostPrefabInstanceRoot(go), InteractionMode.AutomatedAction);
                EditorSceneManager.SaveScene(scene);
                EditorSceneManager.CloseScene(scene, true);
            }
            var list = EditorBuildSettings.scenes.ToList();
            if (list.All(x => x.path != ScenePath))
            {
                list.Add(new EditorBuildSettingsScene(ScenePath, true));
                EditorBuildSettings.scenes = list.ToArray();
            }
        }

        // ---------- nút Ra đảo trong màn máy bi ----------

        [MenuItem("PokiClash/Prefab/Đảo Casino/Máy bi: nút Ra đảo", priority = 71)]
        public static void MachineButton()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var root = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var scene = root.GetComponent<MachineScene>();
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!scene || !safe)
                {
                    Debug.LogError("[Đảo Casino] Screens/Machine thiếu MachineScene hoặc Canvas/An toan/Khung.");
                    return;
                }
                var old = safe.Find("ra_dao");
                if (old) Object.DestroyImmediate(old.gameObject);
                var b = HomeSceneMenu.Button(assets, safe, "ra_dao", Loc.T("Ra đảo"), BtnColor.Paper, new Vector2(220, 96));
                var rt = (RectTransform)b.transform;
                HomeSceneMenu.At(rt, new Vector2(0, 1), new Vector2(18, -SceneRoot.BarHeight - 12), new Vector2(220, 96), new Vector2(0, 1));
                b.gameObject.SetActive(false); // MachineScene bật khi đảo đã mở
                scene.SetupIsland(b);
                PrefabUtility.SaveAsPrefabAsset(root, MachinePath);
                Debug.Log("[Đảo Casino] Đã thêm nút Ra đảo vào " + MachinePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // ---------- chụp thử ----------

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino");

        [MenuItem("PokiClash/Thử/Đảo Casino/Đảo: chụp màn đảo và máy bi (đang Play)", priority = 150)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator WaitRouter(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(ShotDir);
            foreach (var f in Directory.GetFiles(ShotDir, "*.jpg")) File.Delete(f);
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 40); // đủ cấp để thấy các trò mở
                s.casino = null; // như lần đầu ra đảo
                App.Router.Go(SceneIds.Casino);
                yield return WaitRouter(SceneIds.Casino);
                yield return new WaitForSecondsRealtime(1.2f);
                yield return Shot("1_lan_dau_truyen", true);
                {
                    var fr = Object.FindAnyObjectByType<CasinoScene>()?.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(r => r.name == "anh_nen_casino");
                    if (fr)
                    {
                        var c = new Vector3[4];
                        fr.GetWorldCorners(c);
                        Debug.Log($"[Thử] khung đảo: góc {c[0]} {c[2]}, lossy {fr.lossyScale}, rect {fr.rect}, quay {fr.eulerAngles}");
                        for (var p = fr.parent; p; p = p.parent) Debug.Log($"[Thử]   cha {p.name}: scale {p.localScale}, quay {p.localEulerAngles}, rect {(p as RectTransform)?.rect}");
                        foreach (var sp in fr.GetComponentsInChildren<CasinoSpot>(true).Take(3)) Debug.Log($"[Thử]   điểm {sp.Id}: {sp.transform.position}");
                    }
                }
                App.Modals.CloseAll();
                Casino.Of(s).intro = true;
                Object.FindAnyObjectByType<CasinoScene>()?.Refresh();
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("2_dao_giua");
                var pan = Object.FindAnyObjectByType<HubPan>();
                if (pan)
                {
                    foreach (var (tag, o) in new[] { ("trai", new Vector2(3000, 0)), ("phai", new Vector2(-3000, 0)) })
                    {
                        pan.SetOffset(o);
                        yield return new WaitForSecondsRealtime(1.6f);
                        yield return Shot("3_keo_" + tag);
                    }
                    pan.SetOffset(Vector2.zero);
                }
                s.level = 9; // vừa mở đảo: nhiều trò còn khoá
                Object.FindAnyObjectByType<CasinoScene>()?.Refresh();
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot("4_cap_9_khoa");
                App.Router.Go(SceneIds.Machine, SceneIds.Casino);
                yield return WaitRouter(SceneIds.Machine);
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot("5_may_bi_nut_ra_dao");
                Debug.Log("[Thử] Xong đảo Casino: " + Path.GetFullPath(ShotDir));
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        // chuyến tàu sảnh → đảo → sảnh: chụp liên tiếp (Temp/PokiShots/casino_tau/)
        static string VoyDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_tau");

        static IEnumerator Voyage()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(VoyDir);
            foreach (var f in Directory.GetFiles(VoyDir, "*.jpg")) File.Delete(f);
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 40);
                Casino.Of(s).intro = true;
                if (App.Router.Current != SceneIds.Hub)
                {
                    App.Router.Go(SceneIds.Hub);
                    yield return WaitRouter(SceneIds.Hub);
                }
                yield return new WaitForSecondsRealtime(1.5f);
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.5f);
                yield return VShot("0_sanh");
                App.Router.Go(SceneIds.Casino);
                for (int k = 0; k < 26; k++)
                {
                    yield return new WaitForSecondsRealtime(0.32f);
                    yield return VShot($"1_di_{k:00}");
                }
                yield return WaitRouter(SceneIds.Casino);
                yield return new WaitForSecondsRealtime(1.5f);
                App.Modals.CloseAll();
                yield return VShot("2_toi_dao");
                App.Router.Go(SceneIds.Hub);
                for (int k = 0; k < 22; k++)
                {
                    yield return new WaitForSecondsRealtime(0.32f);
                    yield return VShot($"3_ve_{k:00}");
                }
                yield return WaitRouter(SceneIds.Hub);
                Debug.Log("[Thử] Xong chuyến tàu đảo Casino: " + Path.GetFullPath(VoyDir));
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
        }

        static IEnumerator VShot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(VoyDir, name + ".jpg"), tex.EncodeToJPG(80));
            Object.DestroyImmediate(tex);
        }

        static IEnumerator Shot(string name, bool keepModal = false)
        {
            if (!keepModal) App.Modals.CloseAll(); // popup ưu đãi lúc vào game che bản đồ
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(ShotDir, name + ".jpg"), tex.EncodeToJPG(82));
            Object.DestroyImmediate(tex);
        }

        // ---------- chạy không cần bấm menu ----------

        static double nextPoll, tourStart;
        static bool tourRunning;
        static string Flag(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            var build = Flag("casino_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                Build();
                MachineButton();
                return;
            }
            var voy = Flag("casino_voyage_tour.flag");
            if (File.Exists(voy) && !tourRunning)
            {
                if (!EditorApplication.isPlaying)
                {
                    if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true;
                    return;
                }
                Application.runInBackground = true; // game tắt Run In Background: Unity nằm nền thì vòng game đứng, lượt chụp không chạy
                if (App.I == null || App.Router == null || App.Router.Busy || App.Router.Current == null) return;
                File.Delete(voy);
                tourRunning = true;
                tourStart = EditorApplication.timeSinceStartup;
                App.I.StartCoroutine(VoyageThenStop());
                return;
            }
            var tour = Flag("casino_tour.flag");
            if (File.Exists(tour) && !tourRunning)
            {
                if (!EditorApplication.isPlaying)
                {
                    if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true; // scene nào cũng được: SceneRoot tự nạp Boot
                    return;
                }
                Application.runInBackground = true; // game tắt Run In Background: Unity nằm nền thì vòng game đứng, lượt chụp không chạy
                if (App.I == null || App.Router == null || App.Router.Busy || App.Router.Current == null) return;
                File.Delete(tour);
                tourRunning = true;
                tourStart = EditorApplication.timeSinceStartup;
                App.I.StartCoroutine(TourThenStop());
                return;
            }
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 120)
            {
                tourRunning = false;
                EditorApplication.isPlaying = false;
            }
        }

        static IEnumerator VoyageThenStop()
        {
            yield return new WaitForSecondsRealtime(3f);
            yield return Voyage();
            yield return new WaitForSecondsRealtime(1f);
            tourRunning = false;
            EditorApplication.isPlaying = false;
        }

        static IEnumerator TourThenStop()
        {
            yield return new WaitForSecondsRealtime(3f);
            yield return Run();
            yield return new WaitForSecondsRealtime(1f);
            tourRunning = false;
            EditorApplication.isPlaying = false;
        }
    }
}
