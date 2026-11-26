// Scene Bến câu của đảo Casino (GD_Claude/29_DaoCasino.md, mốc C3; mỗi trò một scene, người dùng 2026-11-25). Menu
// "PokiClash/Prefab/Đảo Casino/Bến câu: dựng scene" (chạy lại được): Screens/CasinoFishing (lần đầu chép từ Screens/Cave, thay bằng
// FishingScene; scene chung cũ CasinoPlay đổi tên thành CasinoFishing, giữ GUID), scene CasinoFishing + Build Settings, tấm Bến câu
// (FishingPanel, màn chơi kiểu Clash of Critters từ 2026-11-26): nền tạm, mặt nước nhận chạm, bóng cá, cần, phao, dây, nút CÂU to giữa đáy
// (Sổ Cá + Bán cá bên trái, Mua mồi bên phải), tấm kéo tím (nhịp, đồng hồ, thanh vùng vàng + kim), chỗ câu, mồi, cần câu, tấm kết quả
// (băng kỷ lục, huy chương hạng cân), Sổ Cá 30 ô. Cờ Temp/casino_fishing_build.flag (dựng), Temp/casino_fish_tour.flag (chụp thử,
// Temp/PokiShots/casino_cau/).
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using AtomSpine;
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
        // scene vẽ tay (GD_Claude/32): ArtGen/Casino/ben_cau/nuoc/lam_nuoc.py, lam_do.py, rig/atom/export/cau_ca.atomik
        const string ArtDir = "Assets/03 Art/Casino/BenCau/";
        const string PlatePath = ArtDir + "ben_cau_nen.png";
        const string WaterTexPath = ArtDir + "ben_cau_nuoc.png";
        const string WaterCpuPath = ArtDir + "ben_cau_nuoc_cpu.bytes";
        const string WaterMatPath = ArtDir + "ben_cau_nuoc.mat";
        const string RigPath = ArtDir + "cau_ca.bytes";
        const string BobberPath = ArtDir + "ben_cau_phao.png";
        const string DropPath = ArtDir + "ben_cau_giot.png";
        const string FishPath = ArtDir + "ben_cau_ca.png";
        const string FishArtDir = "Assets/03 Art/Casino/BenCau/Ca";

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
            if (!PrepareArt()) return;
            MoveOld();
            if (!BuildScreen(assets)) return;
            MakeScene();
            AssetDatabase.SaveAssets();
            Debug.Log("[Đảo Casino] Đã dựng " + ScreenPath + ", " + ScenePath);
        }

        // chế độ nhập: nền và đồ nhỏ là Sprite; mặt nạ nước tuyến tính, không nén, kẹp mép; material nước dùng mặt nạ
        static bool PrepareArt()
        {
            foreach (var path in new[] { PlatePath, BobberPath, DropPath, FishPath })
            {
                AssetDatabase.ImportAsset(path);
                if (AssetImporter.GetAtPath(path) is TextureImporter ti)
                {
                    bool dirty = ti.textureType != TextureImporterType.Sprite || ti.spriteImportMode != SpriteImportMode.Single || ti.mipmapEnabled;
                    ti.textureType = TextureImporterType.Sprite;
                    ti.spriteImportMode = SpriteImportMode.Single;
                    ti.mipmapEnabled = false;
                    ti.alphaIsTransparency = true;
                    if (ti.maxTextureSize < 2048) { ti.maxTextureSize = 2048; dirty = true; }
                    if (dirty) ti.SaveAndReimport();
                }
                else
                {
                    Debug.LogError("[Đảo Casino] Thiếu ảnh " + path);
                    return false;
                }
            }
            AssetDatabase.ImportAsset(WaterTexPath);
            if (AssetImporter.GetAtPath(WaterTexPath) is TextureImporter wi)
            {
                wi.textureType = TextureImporterType.Default;
                wi.sRGBTexture = false;
                wi.mipmapEnabled = false;
                wi.textureCompression = TextureImporterCompression.Uncompressed;
                wi.wrapMode = TextureWrapMode.Clamp;
                wi.filterMode = FilterMode.Bilinear;
                wi.maxTextureSize = 2048;
                wi.alphaSource = TextureImporterAlphaSource.None;
                wi.npotScale = TextureImporterNPOTScale.None;   // giữ 1024 x 1536 (code, shader tính theo px ảnh nền)
                wi.SaveAndReimport();
            }
            // hình cá: Sprite nhỏ (cạnh dài 256, Cá Vua 320), không mipmap
            foreach (var g in AssetDatabase.FindAssets("t:Texture2D", new[] { FishArtDir }))
            {
                var path = AssetDatabase.GUIDToAssetPath(g);
                if (AssetImporter.GetAtPath(path) is TextureImporter fi)
                {
                    int cap = Path.GetFileNameWithoutExtension(path).StartsWith("vua_") ? 512 : 256;
                    if (fi.textureType != TextureImporterType.Sprite || fi.mipmapEnabled || fi.maxTextureSize != cap || fi.spriteImportMode != SpriteImportMode.Single)
                    {
                        fi.textureType = TextureImporterType.Sprite;
                        fi.spriteImportMode = SpriteImportMode.Single;
                        fi.mipmapEnabled = false;
                        fi.alphaIsTransparency = true;
                        fi.maxTextureSize = cap;
                        fi.SaveAndReimport();
                    }
                }
            }
            AssetDatabase.ImportAsset(WaterCpuPath);
            AssetDatabase.ImportAsset(RigPath);
            var sh = Shader.Find("PokiClash/UIPondWater");
            if (!sh)
            {
                Debug.LogError("[Đảo Casino] Không thấy shader PokiClash/UIPondWater.");
                return false;
            }
            var m = AssetDatabase.LoadAssetAtPath<Material>(WaterMatPath);
            if (!m)
            {
                m = new Material(sh);
                AssetDatabase.CreateAsset(m, WaterMatPath);
            }
            m.shader = sh;
            m.SetTexture("_WaterTex", AssetDatabase.LoadAssetAtPath<Texture2D>(WaterTexPath));
            EditorUtility.SetDirty(m);
            return true;
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
            // cảnh vẽ tay 2:3 phủ kín khung (EnvelopeParent): nền + shader nước, người câu, dây, phao, đồ ngắm, giọt nước, cá vọt
            var hold = Fill(N(panel, "canh"));
            var world = N(hold, "the_gioi");
            world.anchorMin = world.anchorMax = world.pivot = new Vector2(0.5f, 0.5f);
            world.sizeDelta = new Vector2(1024, 1536);
            var fit = world.gameObject.AddComponent<AspectRatioFitter>();
            fit.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
            fit.aspectRatio = 2 / 3f;
            var plate = Img(world, "nen", AssetDatabase.LoadAssetAtPath<Sprite>(PlatePath), Color.white, true);
            Fill(plate.rectTransform);
            plate.material = AssetDatabase.LoadAssetAtPath<Material>(WaterMatPath);
            var aim = plate.gameObject.AddComponent<AimArea>();

            // người câu: gốc rig (giữa hai ủng) ở chỗ đứng trên bến (px 512, 1405 của nền 1024 x 1536)
            var fisherRt = N(world, "nguoi", typeof(CanvasRenderer), typeof(AtomikGraphic));
            fisherRt.anchorMin = fisherRt.anchorMax = new Vector2(0.5f, 1f - 1405f / 1536f);
            fisherRt.pivot = new Vector2(0.5f, 0f);
            fisherRt.anchoredPosition = Vector2.zero;
            fisherRt.sizeDelta = new Vector2(320, 640);
            var fisher = fisherRt.GetComponent<AtomikGraphic>();
            fisher.scaleMode = AtomikGraphicScale.RigPixels;
            fisher.overlayClip = "";
            fisher.clip = "idle";
            fisher.raycastTarget = false;

            var line = N(world, "day", typeof(CanvasRenderer), typeof(FishingLine)).GetComponent<FishingLine>();
            Fill(line.rectTransform);
            line.color = new Color(1f, 1f, 0.97f, 0.92f);
            line.raycastTarget = false;
            // phao 3D: gốc ở chỗ chạm mặt nước; lớp trên (RectMask2D từ mặt nước trở lên) hình rõ, lớp dưới (từ mặt nước trở xuống)
            // cùng hình tô xanh mờ như nhìn qua nước. FishingPanel dời, nghiêng hai hình như nhau theo lò xo.
            var bob = N(world, "phao");
            bob.anchorMin = bob.anchorMax = new Vector2(0.5f, 0.5f);
            bob.sizeDelta = Vector2.zero;
            var bobSprite = AssetDatabase.LoadAssetAtPath<Sprite>(BobberPath);
            var topMask = N(bob, "tren", typeof(RectMask2D));
            topMask.anchorMin = topMask.anchorMax = new Vector2(0.5f, 0.5f);
            topMask.pivot = new Vector2(0.5f, 0f);
            topMask.anchoredPosition = Vector2.zero;
            topMask.sizeDelta = new Vector2(200, 240);
            var bobTop = Img(topMask, "hinh", bobSprite, Color.white);
            bobTop.rectTransform.anchorMin = bobTop.rectTransform.anchorMax = new Vector2(0.5f, 0f);
            bobTop.rectTransform.pivot = new Vector2(0.5f, 0.3f);
            bobTop.rectTransform.sizeDelta = new Vector2(44, 64);
            var underMask = N(bob, "duoi", typeof(RectMask2D));
            underMask.anchorMin = underMask.anchorMax = new Vector2(0.5f, 0.5f);
            underMask.pivot = new Vector2(0.5f, 1f);
            underMask.anchoredPosition = Vector2.zero;
            underMask.sizeDelta = new Vector2(200, 200);
            var bobUnder = Img(underMask, "bong", bobSprite, new Color(0.55f, 0.78f, 0.95f, 0.42f));
            bobUnder.rectTransform.anchorMin = bobUnder.rectTransform.anchorMax = new Vector2(0.5f, 1f);
            bobUnder.rectTransform.pivot = new Vector2(0.5f, 0.3f);
            bobUnder.rectTransform.sizeDelta = new Vector2(44, 64);
            var bang = Img(world, "cham_than", Sketch.Pill, Theme.Yellow, false, true);
            bang.rectTransform.anchorMin = bang.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            bang.rectTransform.sizeDelta = new Vector2(84, 84);
            var bangT = Txt(bang.transform, "chu", 60, Theme.Ink);
            Fill(bangT.rectTransform);
            bangT.text = "!";

            var outline = Theme.Outlined(Theme.Bold, 0.3f);

            var drops = new RectTransform[10];
            var dropSprite = AssetDatabase.LoadAssetAtPath<Sprite>(DropPath);
            for (int i = 0; i < drops.Length; i++)
            {
                var d = Img(world, "giot_" + i, dropSprite, Color.white);
                d.rectTransform.anchorMin = d.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
                d.rectTransform.sizeDelta = new Vector2(20, 26);
                drops[i] = d.rectTransform;
                d.gameObject.SetActive(false);
            }
            var leap = Img(world, "ca_vot", AssetDatabase.LoadAssetAtPath<Sprite>(FishPath), Color.white);
            leap.rectTransform.anchorMin = leap.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            leap.rectTransform.sizeDelta = new Vector2(120, 64);
            leap.gameObject.SetActive(false);

            // trên: số mồi (bản 3, người dùng 2026-11-26: bỏ nâng cấp cần, phao rơi ngẫu nhiên trên hồ nên không còn nút chỗ câu)
            var top = N(panel, "tren");
            At(top, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 6), new Vector2(1040, 100), new Vector2(0.5f, 1));
            var info = Img(top, "the", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.95f), false, true);
            At(info.rectTransform, new Vector2(0.5f, 1), Vector2.zero, new Vector2(640, 80), new Vector2(0.5f, 1));
            var bait = Txt(info.transform, "moi", 30, Theme.Ink);
            Fill(bait.rectTransform);
            var hint = Txt(panel, "goi_y", 32, Color.white);
            At(hint.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 104), new Vector2(980, 60), new Vector2(0.5f, 1));
            if (outline) hint.fontSharedMaterial = outline;

            // dưới (kiểu Critters): nút to giữa đáy; trái Sổ Cá + Bán cá; phải Mua mồi
            var act = HomeSceneMenu.Button(assets, panel, "nut_cau", Loc.T("Câu"), BtnColor.Green, new Vector2(440, 160));
            At((RectTransform)act.transform, new Vector2(0.5f, 0), new Vector2(0, 36), new Vector2(440, 160), new Vector2(0.5f, 0));
            act.ClickSound = ""; // tiếng theo bước (FishingPanel)
            var actTap = act.gameObject.AddComponent<HoldArea>(); // bắt lúc nhấn xuống cho đúng nhịp
            if (act.Label)
            {
                act.Label.enableAutoSizing = true;
                act.Label.fontSizeMin = 36;
                act.Label.fontSizeMax = 64;
                act.Label.fontSize = 64;
            }
            var dexBtn = HomeSceneMenu.Button(assets, panel, "so_ca", Loc.T("Sổ Cá"), BtnColor.Paper, new Vector2(270, 110));
            At((RectTransform)dexBtn.transform, new Vector2(0, 0), new Vector2(24, 40), new Vector2(270, 110), new Vector2(0, 0));
            var sellBtn = HomeSceneMenu.Button(assets, panel, "ban_ca", Loc.T("Bán cá"), BtnColor.Yellow, new Vector2(270, 110));
            At((RectTransform)sellBtn.transform, new Vector2(0, 0), new Vector2(24, 164), new Vector2(270, 110), new Vector2(0, 0));
            var baitBtn = HomeSceneMenu.Button(assets, panel, "mua_moi", Loc.T("Mua mồi"), BtnColor.Green, new Vector2(270, 110));
            At((RectTransform)baitBtn.transform, new Vector2(1, 0), new Vector2(-24, 40), new Vector2(270, 110), new Vector2(1, 0));
            foreach (var b in new[] { dexBtn, sellBtn, baitBtn })
                if (b.Label)
                {
                    b.Label.enableAutoSizing = true;
                    b.Label.fontSizeMin = 18;
                    b.Label.fontSizeMax = 30;
                }

            // thanh kéo (Critters: tấm tím ở phần ba dưới): hàng nhịp + đồng hồ, thanh ngang có vùng vàng và kim, dòng gợi ý
            var rp = Img(panel, "keo", Sketch.PanelThin, new Color(0.29f, 0.18f, 0.47f, 0.94f), false, true);
            var reelRt = rp.rectTransform;
            At(reelRt, new Vector2(0.5f, 0), new Vector2(0, 300), new Vector2(940, 300), new Vector2(0.5f, 0));
            var pipRow = N(reelRt, "nhip", typeof(HorizontalLayoutGroup));
            At(pipRow, new Vector2(0, 1), new Vector2(40, -26), new Vector2(560, 50), new Vector2(0, 1));
            var ph = pipRow.GetComponent<HorizontalLayoutGroup>();
            ph.spacing = 14;
            ph.childAlignment = TextAnchor.MiddleLeft;
            ph.childControlWidth = ph.childControlHeight = false;
            ph.childForceExpandWidth = ph.childForceExpandHeight = false;
            var pips = new Image[Fishing.MaxTicks];
            for (int i = 0; i < pips.Length; i++)
            {
                pips[i] = Img(pipRow, "nhip_" + i, Sketch.Dot, new Color(1, 1, 1, 0.35f));
                pips[i].rectTransform.sizeDelta = new Vector2(46, 46);
            }
            var clock = Img(reelRt, "dong_ho_nen", Sketch.Dot, new Color(0, 0, 0, 0.35f));
            At(clock.rectTransform, new Vector2(1, 1), new Vector2(-30, -14), new Vector2(96, 96), new Vector2(1, 1));
            var ring = Img(clock.transform, "dong_ho", Sketch.Dot, Theme.Yellow);
            Fill(ring.rectTransform);
            ring.type = Image.Type.Filled;
            ring.fillMethod = Image.FillMethod.Radial360;
            ring.fillOrigin = (int)Image.Origin360.Top;
            ring.fillClockwise = false;
            var inner = Img(clock.transform, "trong", Sketch.Dot, new Color(0.29f, 0.18f, 0.47f, 1));
            Fill(inner.rectTransform).offsetMin = new Vector2(12, 12);
            inner.rectTransform.offsetMax = new Vector2(-12, -12);
            var timer = Txt(clock.transform, "giay", 40, Color.white);
            Fill(timer.rectTransform);
            timer.text = "30";
            var bar = Img(reelRt, "thanh", Sketch.Pill, new Color(1, 1, 1, 0.92f), false, true);
            At(bar.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -150), new Vector2(820, 74), new Vector2(0.5f, 0.5f));
            var zone = Img(bar.transform, "vung_vang", Sketch.Pill, Theme.Yellow, false, true);
            At(zone.rectTransform, new Vector2(0, 0.5f), Vector2.zero, new Vector2(160, 74), new Vector2(0.5f, 0.5f));
            var needle = Img(bar.transform, "kim", null, Theme.Red);
            At(needle.rectTransform, new Vector2(0, 0.5f), Vector2.zero, new Vector2(16, 116), new Vector2(0.5f, 0.5f));
            var cap = Img(needle.transform, "dau_kim", Sketch.Dot, Theme.Red);
            At(cap.rectTransform, new Vector2(0.5f, 1), new Vector2(0, 14), new Vector2(38, 38), new Vector2(0.5f, 1));
            var penalty = Txt(bar.transform, "phat", 44, Theme.Hex("#ff8a7a"));
            At(penalty.rectTransform, new Vector2(1, 0.5f), new Vector2(-40, 70), new Vector2(300, 60), new Vector2(1, 0.5f));
            var penOutline = Theme.Outlined(Theme.Bold, 0.3f);
            if (penOutline) penalty.fontSharedMaterial = penOutline;
            penalty.alpha = 0;
            var reelHint = Txt(reelRt, "goi_y", 28, Color.white);
            At(reelHint.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 22), new Vector2(880, 46), new Vector2(0.5f, 0));
            rp.gameObject.SetActive(false);
            var reelUi = new FishingPanel.ReelUi
            {
                panel = reelRt, bar = bar.rectTransform, zone = zone.rectTransform, needle = needle.rectTransform, zoneImg = zone, timerRing = ring,
                pips = pips, timer = timer, penalty = penalty, hint = reelHint,
            };

            // tấm kết quả: thẻ cá, băng LOÀI MỚI / KỶ LỤC MỚI, huy chương hạng cân
            var res = Img(panel, "ket_qua", null, new Color(0.1f, 0.08f, 0.06f, 0.55f), true);
            Fill(res.rectTransform);
            var card = Img(res.transform, "giay", Sketch.PanelThin, Theme.Paper, true, true);
            At(card.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 40), new Vector2(880, 800), new Vector2(0.5f, 0.5f));
            var rRingImg = Img(card.transform, "vien", Sketch.Dot, Theme.Yellow);
            At(rRingImg.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -90), new Vector2(210, 210), new Vector2(0.5f, 1));
            var dot = Img(rRingImg.transform, "ca", Sketch.Dot, Theme.Blue);
            Fill(dot.rectTransform).offsetMin = new Vector2(-46, -6);   // hình cá to hơn vòng màu độ hiếm phía sau
            dot.rectTransform.offsetMax = new Vector2(46, 6);
            dot.preserveAspect = true;
            var medal = Img(rRingImg.transform, "huy_chuong", Sketch.Medal, Theme.Yellow);
            At(medal.rectTransform, new Vector2(1, 1), new Vector2(30, 20), new Vector2(104, 104), new Vector2(0.5f, 0.5f));
            var banner = Img(card.transform, "bang", Sketch.Pill, Theme.Yellow, false, true);
            At(banner.rectTransform, new Vector2(0.5f, 1), new Vector2(0, 10), new Vector2(560, 104), new Vector2(0.5f, 0.5f));
            var bannerT = Txt(banner.transform, "chu", 50, Theme.Ink);
            Fill(bannerT.rectTransform);
            var rName = Txt(card.transform, "ten", 52, Theme.Ink);
            At(rName.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -320), new Vector2(820, 70), new Vector2(0.5f, 1));
            var rInfo = Txt(card.transform, "nhan", 30, Theme.Ink2);
            At(rInfo.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -395), new Vector2(820, 50), new Vector2(0.5f, 1));
            var rRew = Txt(card.transform, "thuong", 30, Theme.Ink);
            At(rRew.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -460), new Vector2(800, 170), new Vector2(0.5f, 1));
            var ok = HomeSceneMenu.Button(assets, card.transform, "cau_tiep", Loc.T("Câu tiếp"), BtnColor.Green, new Vector2(360, 116));
            At((RectTransform)ok.transform, new Vector2(0.5f, 0), new Vector2(0, 40), new Vector2(360, 116), new Vector2(0.5f, 0));
            res.gameObject.SetActive(false);
            var resUi = new FishingPanel.ResultUi
            {
                root = res.gameObject, card = card.rectTransform, dot = dot, ring = rRingImg, medal = medal, name = rName, info = rInfo, rewards = rRew,
                banner = banner.rectTransform, bannerText = bannerT, ok = ok,
            };
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
                Fill(cd.rectTransform).offsetMin = new Vector2(-18, 4);
                cd.rectTransform.offsetMax = new Vector2(18, -4);
                cd.preserveAspect = true;
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
            var sceneUi = new FishingPanel.SceneUi
            {
                world = world, plate = plate, aim = aim, fisher = fisher, line = line, bobber = bob, bang = bang.rectTransform,
                bobTop = bobTop.rectTransform, bobUnder = bobUnder.rectTransform, drops = drops, hint = hint, leapFish = leap,
                rig = AssetDatabase.LoadAssetAtPath<TextAsset>(RigPath), water = AssetDatabase.LoadAssetAtPath<TextAsset>(WaterCpuPath),
            };
            fp.Setup(sceneUi, act, actTap, reelUi, bait, dexBtn, sellBtn, baitBtn, resUi, dex.gameObject, dHead, cells, close);
            fp.SetFishArt(AssetDatabase.FindAssets("t:Sprite", new[] { FishArtDir }).Select(g => AssetDatabase.LoadAssetAtPath<Sprite>(AssetDatabase.GUIDToAssetPath(g)))
                .Where(x => x).OrderBy(x => x.name).ToArray());
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

        [MenuItem("PokiClash/Thử/Đảo Casino/Bến câu: thả, thanh chạy, Sổ Cá (đang Play)", priority = 151)]
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
                foreach (int zone in new[] { 1, 3, 2 }) // Gần bờ (thường cá nhỏ), Rạn đá, Xa bờ (thường cá lớn: thanh vùng vàng)
                {
                    k++;
                    int kk = k;
                    yield return panel.AutoCast(zone, n => App.I.StartCoroutine(Shot($"2_luot{kk}_{n}")));
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
