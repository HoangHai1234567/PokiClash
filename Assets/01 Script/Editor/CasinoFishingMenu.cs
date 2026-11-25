// Scene Bến câu của đảo Casino (GD_Claude/29_DaoCasino.md, mốc C3; mỗi trò một scene, người dùng 2026-11-25). Menu
// "PokiClash/Prefab/Đảo Casino/Bến câu: dựng scene" (chạy lại được): Screens/CasinoFishing (lần đầu chép từ Screens/Cave, thay bằng
// FishingScene; scene chung cũ CasinoPlay đổi tên thành CasinoFishing, giữ GUID), scene CasinoFishing + Build Settings, tấm Bến câu
// (FishingPanel): nền tạm, mặt nước nhận vuốt và giữ, cần, phao, dây, thanh lực, thanh kéo, chỗ câu, mồi, cần câu, hàng nút đáy,
// tấm kết quả, Sổ Cá 30 ô. Cờ Temp/casino_fishing_build.flag (dựng), Temp/casino_fish_tour.flag (chụp thử, Temp/PokiShots/casino_cau/).
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
    public static class CasinoFishingMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/CasinoFishing.prefab";
        const string OldScreenPath = "Assets/04 Prefabs/Screens/CasinoPlay.prefab"; // scene chung cũ (trước 2026-11-25)
        const string OldScenePath = "Assets/00 Scenes/CasinoPlay.unity";
        const string BaseScreenPath = "Assets/04 Prefabs/Screens/Cave.prefab";
        const string ScenePath = "Assets/00 Scenes/CasinoFishing.unity";
        const string FishBgPath = "Assets/03 Art/Casino/casino_ben_cau_tam.png";

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static RectTransform N(Transform p, string n, params System.Type[] t) => HomeSceneMenu.Node(p, n, t);
        static RectTransform At(RectTransform rt, Vector2 a, Vector2 pos, Vector2 size, Vector2 pivot) => HomeSceneMenu.At(rt, a, pos, size, pivot);
        static RectTransform Fill(RectTransform rt) => HomeSceneMenu.Fill(rt);
        static Image Img(Transform p, string n, Sprite s, Color c, bool ray = false, bool sliced = false) => HomeSceneMenu.Img(p, n, s, c, ray, sliced);
        static TextMeshProUGUI Txt(Transform p, string n, float size, Color c) => HomeSceneMenu.Text(p, n, size, c);

        [MenuItem("PokiClash/Prefab/Đảo Casino/Bến câu: dựng scene", priority = 72)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets)
            {
                Debug.LogError("[Đảo Casino] Không thấy UiAssets.");
                return;
            }
            Theme.Init(assets);
            AssetDatabase.ImportAsset(FishBgPath);
            var ti = AssetImporter.GetAtPath(FishBgPath) as TextureImporter;
            if (ti && ti.textureType != TextureImporterType.Sprite)
            {
                ti.textureType = TextureImporterType.Sprite;
                ti.SaveAndReimport();
            }
            MoveOld();
            if (!BuildScreen(assets)) return;
            MakeScene();
            AssetDatabase.SaveAssets();
            Debug.Log("[Đảo Casino] Đã dựng " + ScreenPath + ", " + ScenePath);
        }

        // scene chung cũ CasinoPlay → scene riêng CasinoFishing (đổi tên giữ GUID, sửa Build Settings)
        static void MoveOld()
        {
            if (File.Exists(OldScreenPath) && !File.Exists(ScreenPath)) AssetDatabase.MoveAsset(OldScreenPath, ScreenPath);
            if (File.Exists(OldScenePath) && !File.Exists(ScenePath)) AssetDatabase.MoveAsset(OldScenePath, ScenePath);
            var list = EditorBuildSettings.scenes.Where(x => x.path != OldScenePath).ToList();
            if (list.Count != EditorBuildSettings.scenes.Length) EditorBuildSettings.scenes = list.ToArray();
        }

        static bool BuildScreen(UiAssets assets)
        {
            if (!File.Exists(ScreenPath))
            {
                if (!AssetDatabase.CopyAsset(BaseScreenPath, ScreenPath))
                {
                    Debug.LogError("[Đảo Casino] Không chép được " + BaseScreenPath);
                    return false;
                }
                AssetDatabase.ImportAsset(ScreenPath);
            }
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                root.name = "CasinoFishing";
                var scene = root.GetComponent<FishingScene>();
                RectTransform content;
                if (!scene)
                {
                    var old = root.GetComponent<SceneRoot>();
                    PokiCanvas view = null;
                    content = null;
                    if (old)
                    {
                        var so = new SerializedObject(old);
                        view = so.FindProperty("view").objectReferenceValue as PokiCanvas;
                        content = so.FindProperty("content").objectReferenceValue as RectTransform;
                        Object.DestroyImmediate(old);
                    }
                    scene = root.AddComponent<FishingScene>();
                    scene.SetupView(view ? view : root.GetComponentInChildren<PokiCanvas>(true), content);
                }
                else content = scene.Content;
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !safe)
                {
                    Debug.LogError("[Đảo Casino] Screens/CasinoFishing thiếu Canvas/Nen hoặc Canvas/An toan/Khung.");
                    return false;
                }
                // nền: tắt lớp của màn gốc, để màu nước (mỗi tấm trò tự có ảnh nền)
                foreach (Transform c in nen) c.gameObject.SetActive(c.name == "nen_hai_ben");
                if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image si)
                {
                    si.sprite = null;
                    si.color = Theme.Hex("#4fb6e6");
                }
                foreach (Transform c in safe.Cast<Transform>().ToList())
                    if (c != content) Object.DestroyImmediate(c.gameObject);
                if (content)
                    foreach (Transform c in content.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject);
                var fishing = BuildFishing(assets, safe);
                scene.Setup(fishing);
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
                return true;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // ---------- Bến câu ----------

        static FishingPanel BuildFishing(UiAssets assets, RectTransform safe)
        {
            var panel = Fill(N(safe, "cau_ca", typeof(FishingPanel)));
            // nền tạm phủ cả tấm (EnvelopeParent 2:3)
            var bgHold = Fill(N(panel, "nen", typeof(RectMask2D)));
            var bg = Img(bgHold, "anh", AssetDatabase.LoadAssetAtPath<Sprite>(FishBgPath), Color.white);
            Fill(bg.rectTransform);
            var fit = bg.gameObject.AddComponent<AspectRatioFitter>();
            fit.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
            fit.aspectRatio = 2 / 3f;

            // trên: mồi, cần câu, chỗ câu
            var top = N(panel, "tren");
            At(top, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 6), new Vector2(1040, 210), new Vector2(0.5f, 1));
            var info = Img(top, "the", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.95f), false, true);
            At(info.rectTransform, new Vector2(0.5f, 1), Vector2.zero, new Vector2(1040, 90), new Vector2(0.5f, 1));
            var bait = Txt(info.transform, "moi", 28, Theme.Ink);
            bait.alignment = TextAlignmentOptions.Left;
            At(bait.rectTransform, new Vector2(0, 0.5f), new Vector2(24, 0), new Vector2(520, 70), new Vector2(0, 0.5f));
            var rod = Txt(info.transform, "can", 28, Theme.Ink);
            rod.alignment = TextAlignmentOptions.Right;
            At(rod.rectTransform, new Vector2(1, 0.5f), new Vector2(-290, 0), new Vector2(230, 70), new Vector2(1, 0.5f));
            var rodBtn = HomeSceneMenu.Button(assets, info.transform, "nang_can", Loc.T("Nâng"), BtnColor.Green, new Vector2(260, 76));
            At((RectTransform)rodBtn.transform, new Vector2(1, 0.5f), new Vector2(-12, 0), new Vector2(260, 76), new Vector2(1, 0.5f));
            var spotsRow = N(top, "cho_cau", typeof(HorizontalLayoutGroup));
            At(spotsRow, new Vector2(0.5f, 1), new Vector2(0, -104), new Vector2(1040, 96), new Vector2(0.5f, 1));
            var hl = spotsRow.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = 14;
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var spots = new SketchButton[3];
            for (int i = 0; i < 3; i++) spots[i] = HomeSceneMenu.Button(assets, spotsRow, "cho_" + i, "?", BtnColor.Paper, new Vector2(320, 90));

            // mặt nước: nhận vuốt (quăng), giữ (giật, kéo)
            var water = Img(panel, "mat_nuoc", null, new Color(1, 1, 1, 0), true);
            var wrt = water.rectTransform;
            wrt.anchorMin = new Vector2(0, 0);
            wrt.anchorMax = new Vector2(1, 1);
            wrt.offsetMin = new Vector2(0, 190);
            wrt.offsetMax = new Vector2(0, -(SceneRoot.BarHeight + 230));
            wrt.pivot = new Vector2(0.5f, 0.5f);
            var swipe = water.gameObject.AddComponent<SwipeArea>();
            var hold = water.gameObject.AddComponent<HoldArea>();

            // cần câu: thanh gỗ chéo ở đáy giữa, đầu cần là gốc dây
            var rodImg = Img(wrt, "can_cau", null, Theme.Hex("#8a5a2b"));
            At(rodImg.rectTransform, new Vector2(0.5f, 0), new Vector2(150, -40), new Vector2(18, 420), new Vector2(0.5f, 0));
            rodImg.rectTransform.localEulerAngles = new Vector3(0, 0, 18);
            var tip = N(wrt, "dau_can");
            // đầu cần: toạ độ theo tâm mặt nước (giống phao, dây)
            tip.anchorMin = tip.anchorMax = new Vector2(0.5f, 0.5f);
            tip.pivot = new Vector2(0.5f, 0.5f);
            tip.sizeDelta = new Vector2(10, 10);
            var line = Img(wrt, "day", null, new Color(1f, 1f, 1f, 0.85f));
            line.rectTransform.anchorMin = line.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            line.rectTransform.pivot = new Vector2(0.5f, 0.5f);
            var bob = Img(wrt, "phao", Sketch.Dot, Theme.Red);
            bob.rectTransform.anchorMin = bob.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            bob.rectTransform.sizeDelta = new Vector2(50, 50);
            var bobTop = Img(bob.transform, "trang", Sketch.Dot, Color.white);
            At(bobTop.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -2), new Vector2(30, 22), new Vector2(0.5f, 1));
            var bang = Img(wrt, "cham_than", Sketch.Pill, Theme.Yellow, false, true);
            bang.rectTransform.anchorMin = bang.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            bang.rectTransform.sizeDelta = new Vector2(84, 84);
            var bangT = Txt(bang.transform, "chu", 60, Theme.Ink);
            Fill(bangT.rectTransform);
            bangT.text = "!";
            var hint = Txt(wrt, "goi_y", 34, Color.white);
            At(hint.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -20), new Vector2(900, 60), new Vector2(0.5f, 1));
            var hintOutline = Theme.Outlined(Theme.Bold, 0.3f);
            if (hintOutline) hint.fontSharedMaterial = hintOutline;

            // thanh lực (trái)
            var powBg = Img(wrt, "luc_nen", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.9f), false, true);
            At(powBg.rectTransform, new Vector2(0, 0.5f), new Vector2(36, 0), new Vector2(54, 460), new Vector2(0, 0.5f));
            var pow = Img(powBg.transform, "luc", null, Theme.Orange);
            Fill(pow.rectTransform).offsetMin = new Vector2(10, 10);
            pow.rectTransform.offsetMax = new Vector2(-10, -10);
            pow.type = Image.Type.Filled;
            pow.fillMethod = Image.FillMethod.Vertical;
            pow.fillOrigin = (int)Image.OriginVertical.Bottom;
            pow.fillAmount = 0;

            // thanh kéo (phải): vùng xanh, cá, vòng kéo
            var reelBg = Img(wrt, "keo", Sketch.PanelThin, new Color(0.15f, 0.3f, 0.45f, 0.75f), false, true);
            var reel = reelBg.rectTransform;
            At(reel, new Vector2(1, 0.5f), new Vector2(-40, 0), new Vector2(120, 760), new Vector2(1, 0.5f));
            var zone = Img(reel, "vung_xanh", Sketch.PanelThin, new Color(0.42f, 0.85f, 0.4f, 0.75f), false, true);
            At(zone.rectTransform, new Vector2(0.5f, 0), Vector2.zero, new Vector2(100, 200), new Vector2(0.5f, 0.5f));
            var fishDot = Img(reel, "ca", Sketch.Dot, Theme.Blue);
            At(fishDot.rectTransform, new Vector2(0.5f, 0), Vector2.zero, new Vector2(70, 70), new Vector2(0.5f, 0.5f));
            var progBg = Img(reel, "vong_keo_nen", null, new Color(0, 0, 0, 0.35f));
            At(progBg.rectTransform, new Vector2(0, 0), new Vector2(-14, 0), new Vector2(26, 760), new Vector2(1, 0));
            var prog = Img(progBg.transform, "vong_keo", null, Theme.Green);
            Fill(prog.rectTransform);
            prog.type = Image.Type.Filled;
            prog.fillMethod = Image.FillMethod.Vertical;
            prog.fillOrigin = (int)Image.OriginVertical.Bottom;

            // dưới: Sổ Cá, Bán cá, Mua mồi
            var bottom = N(panel, "hang_nut", typeof(HorizontalLayoutGroup));
            At(bottom, new Vector2(0.5f, 0), new Vector2(0, 40), new Vector2(1040, 120), new Vector2(0.5f, 0));
            var bh = bottom.GetComponent<HorizontalLayoutGroup>();
            bh.spacing = 14;
            bh.childAlignment = TextAnchor.MiddleCenter;
            bh.childControlWidth = bh.childControlHeight = false;
            bh.childForceExpandWidth = bh.childForceExpandHeight = false;
            var dexBtn = HomeSceneMenu.Button(assets, bottom, "so_ca", Loc.T("Sổ Cá"), BtnColor.Paper, new Vector2(320, 110));
            var sellBtn = HomeSceneMenu.Button(assets, bottom, "ban_ca", Loc.T("Bán cá"), BtnColor.Yellow, new Vector2(340, 110));
            var baitBtn = HomeSceneMenu.Button(assets, bottom, "mua_moi", Loc.T("Mua mồi"), BtnColor.Green, new Vector2(340, 110));

            // tấm kết quả
            var res = Img(panel, "ket_qua", null, new Color(0.1f, 0.08f, 0.06f, 0.55f), true);
            Fill(res.rectTransform);
            var card = Img(res.transform, "giay", Sketch.PanelThin, Theme.Paper, true, true);
            At(card.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 40), new Vector2(880, 760), new Vector2(0.5f, 0.5f));
            var ring = Img(card.transform, "vien", Sketch.Dot, Theme.Yellow);
            At(ring.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -60), new Vector2(210, 210), new Vector2(0.5f, 1));
            var dot = Img(ring.transform, "ca", Sketch.Dot, Theme.Blue);
            Fill(dot.rectTransform).offsetMin = new Vector2(18, 18);
            dot.rectTransform.offsetMax = new Vector2(-18, -18);
            var rName = Txt(card.transform, "ten", 52, Theme.Ink);
            At(rName.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -290), new Vector2(820, 70), new Vector2(0.5f, 1));
            var rInfo = Txt(card.transform, "nhan", 30, Theme.Ink2);
            At(rInfo.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -365), new Vector2(820, 50), new Vector2(0.5f, 1));
            var rRew = Txt(card.transform, "thuong", 30, Theme.Ink);
            At(rRew.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -430), new Vector2(800, 170), new Vector2(0.5f, 1));
            var ok = HomeSceneMenu.Button(assets, card.transform, "cau_tiep", Loc.T("Câu tiếp"), BtnColor.Green, new Vector2(360, 116));
            At((RectTransform)ok.transform, new Vector2(0.5f, 0), new Vector2(0, 40), new Vector2(360, 116), new Vector2(0.5f, 0));
            res.gameObject.SetActive(false);

            // Sổ Cá: 30 ô (5 hệ × 6 loài, thứ tự trong dữ liệu)
            var dex = Img(panel, "so_ca_tam", null, new Color(0.1f, 0.08f, 0.06f, 0.55f), true);
            Fill(dex.rectTransform);
            var page = Img(dex.transform, "giay", Sketch.PanelThin, Theme.Paper, true, true);
            At(page.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, -20), new Vector2(1020, 1500), new Vector2(0.5f, 0.5f));
            var dTitle = Txt(page.transform, "tieu_de", 46, Theme.Ink);
            At(dTitle.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -26), new Vector2(900, 64), new Vector2(0.5f, 1));
            dTitle.text = Loc.T("Sổ Cá");
            var dHead = Txt(page.transform, "dau", 24, Theme.Ink2);
            At(dHead.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -92), new Vector2(940, 80), new Vector2(0.5f, 1));
            var grid = N(page.transform, "luoi", typeof(GridLayoutGroup));
            At(grid, new Vector2(0.5f, 1), new Vector2(0, -186), new Vector2(960, 1110), new Vector2(0.5f, 1));
            var gl = grid.GetComponent<GridLayoutGroup>();
            gl.cellSize = new Vector2(152, 214);
            gl.spacing = new Vector2(8, 8);
            gl.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            gl.constraintCount = 6;
            gl.childAlignment = TextAnchor.UpperCenter;
            var cells = new FishingPanel.DexCell[30];
            for (int i = 0; i < cells.Length; i++)
            {
                var cell = N(grid, "o_" + i);
                var cr = Img(cell, "vien", Sketch.Dot, Color.gray);
                At(cr.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -6), new Vector2(104, 104), new Vector2(0.5f, 1));
                var cd = Img(cr.transform, "ca", Sketch.Dot, Color.gray);
                Fill(cd.rectTransform).offsetMin = new Vector2(10, 10);
                cd.rectTransform.offsetMax = new Vector2(-10, -10);
                var cn = Txt(cell, "ten", 22, Theme.Ink);
                At(cn.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -114), new Vector2(150, 56), new Vector2(0.5f, 1));
                cn.enableAutoSizing = true;
                cn.fontSizeMin = 14;
                cn.fontSizeMax = 22;
                var ci = Txt(cell, "so", 18, Theme.Ink2);
                At(ci.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -170), new Vector2(150, 40), new Vector2(0.5f, 1));
                ci.enableAutoSizing = true;
                ci.fontSizeMin = 12;
                ci.fontSizeMax = 18;
                cells[i] = new FishingPanel.DexCell { dot = cd, ring = cr, name = cn, info = ci };
            }
            var close = HomeSceneMenu.Button(assets, page.transform, "dong", Loc.T("Đóng"), BtnColor.Paper, new Vector2(300, 110));
            At((RectTransform)close.transform, new Vector2(0.5f, 0), new Vector2(0, 40), new Vector2(300, 110), new Vector2(0.5f, 0));
            dex.gameObject.SetActive(false);

            var fp = panel.GetComponent<FishingPanel>();
            fp.Setup(swipe, hold, wrt, tip, bob.rectTransform, line.rectTransform, bang.rectTransform, pow, hint, reel, zone.rectTransform,
                fishDot.rectTransform, fishDot, prog, spots, bait, rod, rodBtn, dexBtn, sellBtn, baitBtn, res.gameObject, dot, ring, rName, rInfo, rRew, ok,
                dex.gameObject, dHead, cells, close);
            // đầu cần: FishingPanel đặt theo đỉnh thanh cần mỗi khung (toạ độ tâm mặt nước)
            panel.gameObject.SetActive(false);
            return fp;
        }

        static void MakeScene()
        {
            if (!File.Exists(ScenePath))
            {
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
                var prev = SceneManager.GetActiveScene();
                SceneManager.SetActiveScene(scene);
                var screen = AssetDatabase.LoadAssetAtPath<GameObject>(ScreenPath);
                ((GameObject)PrefabUtility.InstantiatePrefab(screen)).name = SceneIds.CasinoFishing;
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

        // ---------- chụp thử Bến câu ----------

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_cau");

        [MenuItem("PokiClash/Thử/Đảo Casino/Bến câu: quăng, kéo, Sổ Cá (đang Play)", priority = 151)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
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
                s.level = Mathf.Max(s.level, 20);
                s.balls = Mathf.Max(s.balls, 2000);
                var st = Casino.Of(s);
                st.intro = true;
                st.rod = 4; // mở cả ba chỗ câu
                App.Router.Go(SceneIds.CasinoFishing, Casino.Fishing);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.CasinoFishing) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(1.2f);
                yield return Shot("1_ben_cau");
                var panel = Object.FindAnyObjectByType<FishingPanel>();
                if (!panel)
                {
                    Debug.LogError("[Thử] Không thấy FishingPanel");
                    yield break;
                }
                int k = 0;
                foreach (float pw in new[] { 0.35f, 0.9f })
                {
                    k++;
                    int kk = k;
                    yield return panel.AutoCast(pw, n => App.I.StartCoroutine(Shot($"2_luot{kk}_{n}")));
                    yield return new WaitForSecondsRealtime(0.5f); // ảnh tấm kết quả chụp xong rồi mới bấm Câu tiếp
                    App.Modals.CloseAll();
                    var okBtn = panel.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "cau_tiep");
                    okBtn?.SimulateClick();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                panel.ShowDexForTest();
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Shot("3_so_ca");
                Debug.Log("[Thử] Xong Bến câu: " + Path.GetFullPath(ShotDir));
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

        // chụp giữa lượt (gọi trong AutoCast qua coroutine riêng)
        public static IEnumerator Shot(string name)
        {
            App.Modals.CloseAll();
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(ShotDir, name + ".jpg"), tex.EncodeToJPG(82));
            Object.DestroyImmediate(tex);
        }

        // ---------- cờ ----------

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
            var build = Flag("casino_fishing_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                Build();
                return;
            }
            var tour = Flag("casino_fish_tour.flag");
            if (File.Exists(tour) && !tourRunning)
            {
                if (!EditorApplication.isPlaying)
                {
                    if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true;
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
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                tourRunning = false;
                EditorApplication.isPlaying = false;
            }
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
