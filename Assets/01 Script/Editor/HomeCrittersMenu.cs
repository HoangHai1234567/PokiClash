// Giao diện màn Nhà kiểu Clash of Critters (người dùng 2026-11-22: "các button / điều khiển chức năng chưa rõ ràng, đục sâu vào Clash
// of Critters"; mổ ở GD_Claude/22_Critters_Home.md mục 7). Menu "PokiClash/Prefab/Nhà và side meta/Nhà: giao diện kiểu Critters" vá prefab có sẵn, không
// dựng lại bản đồ:
// - Items/NutVongNha: nút tròn icon (biến thể Kit/Nut_Tron) có chữ dưới, dòng giá, chấm đỏ (HomeRingButton).
// - Items/TheXayNha: thẻ khay xây (biến thể Kit/Nut_Vua) icon to trên, tên + giá dưới (HomeTrayItem).
// - Items/NhaVat: bong bóng có vòng tiến độ (ảnh vành khuyên vong_tien_do.png, Filled Radial360) và chạm được (ClickCatcher).
// - Screens/Home: dựng lại lớp nha_ui (HomeSceneMenu.BuildUi gọi vào đây): dòng tài nguyên, vòng nút "vong" (HomeRing, 6 nút + nhãn
//   tên), gợi ý một dòng, tấm xây "tam_xay" (tab lọc + khay cuộn ngang 2 hàng), bảng chữ cũ (dự phòng, ẩn), hàng nút dưới: kệ gỗ + 4 thẻ
//   giấy (Xây, Lát ô, Thu hết, Ra đảo) dựng ở HomeDockMenu.BuildBar (2026-11-27).
// Chạy lại được: nút, thẻ dựng lại; vòng bong bóng có rồi thì giữ.
using System.IO;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using M = PokiClash.EditorTools.HomeSceneMenu;

namespace PokiClash.EditorTools
{
    public static class HomeCrittersMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/Home.prefab";
        const string ObjPath = "Assets/04 Prefabs/Items/NhaVat.prefab";
        const string RoundKit = "Assets/04 Prefabs/Kit/Nut_Tron.prefab";
        const string CardKit = "Assets/04 Prefabs/Kit/Nut_Vua.prefab";
        const string RingBtnPath = "Assets/04 Prefabs/Items/NutVongNha.prefab";
        const string CardPath = "Assets/04 Prefabs/Items/TheXayNha.prefab";
        const string RingSpritePath = "Assets/03 Art/Home/vong_tien_do.png";

        // cỡ (px, khung rộng 1080): nút tròn, icon trong nút, tấm xây (cao, đáy: trên kệ gỗ hàng nút dưới cao ~200), thẻ khay
        const float BtnSize = 112, IconSize = 64, SheetH = 520, SheetY = 234;
        static readonly Vector2 CardSize = new Vector2(176, 195);

        [MenuItem("PokiClash/Prefab/Nhà và side meta/Nhà: giao diện kiểu Critters", priority = 66)]
        public static void Patch()
        {
            var assets = M.Load<UiAssets>();
            Theme.Init(assets);
            PatchObj();
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                var scene = root.GetComponentInChildren<HomeScene>(true);
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!scene || !safe)
                {
                    Debug.LogError("[Nhà] " + ScreenPath + " thiếu HomeScene hoặc Canvas/An toan/Khung.");
                    return;
                }
                BuildUi(assets, scene, safe);
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            AssetDatabase.SaveAssets();
            Debug.Log($"[Nhà] Giao diện kiểu Critters: {RingBtnPath}, {CardPath}, vòng bong bóng {ObjPath}, nha_ui của {ScreenPath}.");
        }

        // ---------- bong bóng có vòng tiến độ ----------

        static void PatchObj()
        {
            var obj = PrefabUtility.LoadPrefabContents(ObjPath);
            try
            {
                var ho = obj.GetComponent<HomeObject>();
                var bong = obj.transform.Find("bong");
                if (!ho || !bong)
                {
                    Debug.LogError("[Nhà] " + ObjPath + " thiếu HomeObject hoặc nút \"bong\".");
                    return;
                }
                AddBubbleRing(bong, ho);
                PrefabUtility.SaveAsPrefabAsset(obj, ObjPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(obj);
            }
        }

        // nền vòng mờ + vòng đầy dần dưới icon, bong bóng nhận chạm (HomeObject.SetupRing); dùng cả khi dựng mới NhaVat
        public static void AddBubbleRing(Transform bong, HomeObject ho)
        {
            var sp = RingSprite();
            var track = bong.Find("vong_nen")?.GetComponent<Image>() ?? M.Img(bong, "vong_nen", sp, new Color(0.16f, 0.12f, 0.1f, 0.18f));
            var fill = bong.Find("vong")?.GetComponent<Image>() ?? M.Img(bong, "vong", sp, Theme.Green);
            foreach (var im in new[] { track, fill })
            {
                M.Fill(im.rectTransform).offsetMin = new Vector2(3, 3);
                im.rectTransform.offsetMax = new Vector2(-3, -3);
                im.raycastTarget = false;
                im.gameObject.SetActive(false);
            }
            track.transform.SetSiblingIndex(0); // dưới icon, số
            fill.transform.SetSiblingIndex(1);
            fill.type = Image.Type.Filled;
            fill.fillMethod = Image.FillMethod.Radial360;
            fill.fillOrigin = (int)Image.Origin360.Top;
            fill.fillClockwise = true;
            fill.fillAmount = 1;
            var bubbleImg = bong.GetComponent<Image>();
            if (bubbleImg) bubbleImg.raycastTarget = true;
            var catcher = bong.GetComponent<ClickCatcher>();
            if (!catcher) catcher = bong.gameObject.AddComponent<ClickCatcher>();
            ho.SetupRing(track, fill, catcher);
        }

        // vành khuyên trắng 128 px (tô màu lúc chạy), mép mịn
        static Sprite RingSprite()
        {
            if (!File.Exists(RingSpritePath))
            {
                const int N = 128;
                const float Ro = 62f, Ri = 50f, C = (N - 1) / 2f;
                var tex = new Texture2D(N, N, TextureFormat.RGBA32, false);
                var px = new Color32[N * N];
                for (int y = 0; y < N; y++)
                for (int x = 0; x < N; x++)
                {
                    float d = Mathf.Sqrt((x - C) * (x - C) + (y - C) * (y - C));
                    float a = Mathf.Clamp01(Ro - d + 0.5f) * Mathf.Clamp01(d - Ri + 0.5f);
                    px[y * N + x] = new Color32(255, 255, 255, (byte)Mathf.RoundToInt(a * 255));
                }
                tex.SetPixels32(px);
                File.WriteAllBytes(RingSpritePath, tex.EncodeToPNG());
                Object.DestroyImmediate(tex);
            }
            return M.ImportSprite(RingSpritePath, 128);
        }

        // ---------- prefab nút, thẻ ----------

        // nút tròn icon: lõi màu (Nut_Tron), icon giữa, chữ trắng viền mực dưới nút, dòng giá (viên tối) dưới chữ, chấm đỏ góc trên phải
        public static HomeRingButton RingButton()
        {
            var kit = AssetDatabase.LoadAssetAtPath<GameObject>(RoundKit);
            var go = (GameObject)PrefabUtility.InstantiatePrefab(kit);
            try
            {
                go.name = "NutVongNha";
                ((RectTransform)go.transform).sizeDelta = new Vector2(BtnSize, BtnSize);
                var btn = go.GetComponent<SketchButton>();
                btn.SetText("");
                var center = new Vector2(0.5f, 0.5f);
                var icon = M.Img(go.transform, "icon", null, Color.white);
                M.At(icon.rectTransform, center, new Vector2(0, 2), new Vector2(IconSize, IconSize), center);
                icon.preserveAspect = true;
                icon.enabled = false;
                // chữ mực trong viên giấy tự co theo chữ (chữ trắng viền mảnh khó đọc trên cỏ sáng, soi ảnh 2026-11-22)
                var capBg = M.Img(go.transform, "chu_nen", Sketch.Pill, new Color(1f, 0.98f, 0.92f, 0.96f), false, true);
                M.At(capBg.rectTransform, new Vector2(0.5f, 0), new Vector2(0, -2), new Vector2(120, 32), new Vector2(0.5f, 1));
                var hl = capBg.gameObject.AddComponent<HorizontalLayoutGroup>();
                hl.padding = new RectOffset(14, 14, 1, 3);
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = true;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var capFit = capBg.gameObject.AddComponent<ContentSizeFitter>();
                capFit.horizontalFit = capFit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                var cap = M.Text(capBg.transform, "chu", 22, Theme.Ink);
                cap.textWrappingMode = TextWrappingModes.NoWrap;
                var costBg = M.Img(go.transform, "gia", Sketch.Pill, new Color(0.16f, 0.13f, 0.11f, 0.9f), false, true);
                M.At(costBg.rectTransform, new Vector2(0.5f, 0), new Vector2(0, -42), new Vector2(180, 32), new Vector2(0.5f, 1)); // dưới viên chữ (cao ~34)
                var cost = M.Text(costBg.transform, "so", 20, Color.white);
                M.Fill(cost.rectTransform).offsetMin = new Vector2(10, 0);
                cost.rectTransform.offsetMax = new Vector2(-10, 0);
                cost.textWrappingMode = TextWrappingModes.NoWrap;
                cost.enableAutoSizing = true;
                cost.fontSizeMin = 13;
                cost.fontSizeMax = 20;
                costBg.gameObject.SetActive(false);
                var dot = M.Img(go.transform, "cham", Sketch.Dot, Theme.Red);
                M.At(dot.rectTransform, new Vector2(1, 1), new Vector2(-4, -4), new Vector2(30, 30), new Vector2(1, 1));
                dot.gameObject.SetActive(false);
                go.AddComponent<HomeRingButton>().Setup(btn, icon, cap, costBg.rectTransform, cost, dot.gameObject);
                return PrefabUtility.SaveAsPrefabAsset(go, RingBtnPath).GetComponent<HomeRingButton>();
            }
            finally
            {
                Object.DestroyImmediate(go);
            }
        }

        // thẻ khay xây (kiểu thẻ pbui_build_item của Critters): nền giấy, icon công trình to ở trên, tên + giá (hoặc lý do khoá) ở dưới
        public static HomeTrayItem Card()
        {
            var kit = AssetDatabase.LoadAssetAtPath<GameObject>(CardKit);
            var go = (GameObject)PrefabUtility.InstantiatePrefab(kit);
            try
            {
                go.name = "TheXayNha";
                ((RectTransform)go.transform).sizeDelta = CardSize;
                var btn = go.GetComponent<SketchButton>();
                btn.SetRole(BtnColor.Paper);
                var icon = M.Img(go.transform, "icon", null, Color.white);
                M.At(icon.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -8), new Vector2(124, 120), new Vector2(0.5f, 1));
                icon.preserveAspect = true;
                icon.enabled = false;
                var label = btn.Label;
                var lr = label.rectTransform;
                lr.anchorMin = new Vector2(0, 0);
                lr.anchorMax = new Vector2(1, 0);
                lr.pivot = new Vector2(0.5f, 0);
                lr.sizeDelta = new Vector2(-14, 64);
                lr.anchoredPosition = new Vector2(0, 6);
                label.alignment = TextAlignmentOptions.Center;
                label.textWrappingMode = TextWrappingModes.Normal;
                label.enableAutoSizing = true;
                label.fontSizeMax = 20;
                label.fontSizeMin = 12;
                go.AddComponent<HomeTrayItem>().Setup(btn, icon);
                return PrefabUtility.SaveAsPrefabAsset(go, CardPath).GetComponent<HomeTrayItem>();
            }
            finally
            {
                Object.DestroyImmediate(go);
            }
        }

        static HomeRingButton SpawnRing(HomeRingButton prefab, Transform parent, string name)
        {
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(prefab.gameObject, parent)).GetComponent<HomeRingButton>();
            b.name = name;
            return b;
        }

        // ---------- lớp giao diện nha_ui ----------

        public static void BuildUi(UiAssets assets, HomeScene scene, RectTransform safe)
        {
            foreach (var n in new[] { "hang_nut", "nha_ui", "cuon", "trang" })
            {
                var old = safe.Find(n);
                if (!old) continue;
                if (n == "hang_nut" || n == "nha_ui") Object.DestroyImmediate(old.gameObject);
                else old.gameObject.SetActive(false);
            }
            var art = M.Load<ArtLibrary>();
            var ringBtn = RingButton();
            var card = Card();
            var ui = M.Fill(M.Node(safe, "nha_ui", typeof(CanvasGroup))); // CanvasGroup: chuyến tàu qua mây ẩn / hiện giao diện (HomeScene.Chrome)
            ui.SetAsLastSibling();
            var paper = new Color(1f, 0.98f, 0.92f, 0.95f);
            var center = new Vector2(0.5f, 0.5f);

            // dòng tài nguyên dưới thanh trên
            var resBg = M.Img(ui, "tai_nguyen", Sketch.Pill, paper, false, true);
            M.At(resBg.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 4), new Vector2(1020, 60), new Vector2(0.5f, 1));
            var res = M.Text(resBg.transform, "chu", 26, Theme.Ink);
            M.Fill(res.rectTransform).offsetMin = new Vector2(16, 0);
            res.rectTransform.offsetMax = new Vector2(-16, 0);
            res.enableAutoSizing = true;
            res.fontSizeMin = 18;
            res.fontSizeMax = 26;

            // vòng nút quanh vật đang chọn: 6 nút tròn + nhãn tên (dưới tấm xây, hàng nút)
            var ringRt = M.Fill(M.Node(ui, "vong", typeof(HomeRing)));
            var slots = new HomeRingButton[6];
            for (int i = 0; i < slots.Length; i++)
            {
                slots[i] = SpawnRing(ringBtn, ringRt, "nut_" + (i + 1));
                M.At(slots[i].Rt, center, Vector2.zero, new Vector2(BtnSize, BtnSize), center);
                slots[i].gameObject.SetActive(false);
            }
            var tag = M.Img(ringRt, "nhan_ten", Sketch.Pill, paper, false, true);
            M.At(tag.rectTransform, center, Vector2.zero, new Vector2(300, 80), new Vector2(0.5f, 1));
            var vl = tag.gameObject.AddComponent<VerticalLayoutGroup>();
            vl.padding = new RectOffset(26, 26, 10, 12);
            vl.childAlignment = TextAnchor.UpperCenter;
            vl.childControlWidth = vl.childControlHeight = true;
            vl.childForceExpandWidth = vl.childForceExpandHeight = false;
            var fit = tag.gameObject.AddComponent<ContentSizeFitter>();
            fit.horizontalFit = fit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            var tagTitle = M.Text(tag.transform, "ten", 28, Theme.Ink);
            tagTitle.textWrappingMode = TextWrappingModes.NoWrap;
            var tagSub = M.Text(tag.transform, "trang_thai", 22, Theme.Ink2);
            tagSub.textWrappingMode = TextWrappingModes.NoWrap;
            tag.gameObject.SetActive(false);
            ringRt.GetComponent<HomeRing>().Setup(slots, tag.rectTransform, tagTitle, tagSub);
            ringRt.gameObject.SetActive(false);

            // gợi ý một dòng trên tấm xây (chỉ khi xây / lát)
            var hintBg = M.Img(ui, "goi_y", Sketch.PanelThin, paper, false, true);
            M.At(hintBg.rectTransform, new Vector2(0.5f, 0), new Vector2(0, SheetY + SheetH + 6), new Vector2(1020, 56), new Vector2(0.5f, 0));
            var hint = M.Text(hintBg.transform, "chu", 22, Theme.Ink);
            M.Fill(hint.rectTransform).offsetMin = new Vector2(16, 4);
            hint.rectTransform.offsetMax = new Vector2(-16, -4);
            hint.enableAutoSizing = true;
            hint.fontSizeMin = 16;
            hint.fontSizeMax = 22;
            hintBg.gameObject.SetActive(false);

            // tấm xây: nền giấy, hàng tab lọc, khay cuộn ngang 2 hàng thẻ
            var sheet = M.Img(ui, "tam_xay", Sketch.Panel, paper, true, true);
            M.At(sheet.rectTransform, new Vector2(0.5f, 0), new Vector2(0, SheetY), new Vector2(1040, SheetH), new Vector2(0.5f, 0));
            var tabRow = M.Node(sheet.transform, "tab", typeof(HorizontalLayoutGroup));
            M.At(tabRow, new Vector2(0.5f, 1), new Vector2(0, -14), new Vector2(1000, 74), new Vector2(0.5f, 1));
            var tl = tabRow.GetComponent<HorizontalLayoutGroup>();
            tl.spacing = 10;
            tl.childAlignment = TextAnchor.MiddleCenter;
            tl.childControlWidth = tl.childControlHeight = false;
            tl.childForceExpandWidth = tl.childForceExpandHeight = false;
            var tabSize = new Vector2(232, 70);
            var tabs = new[]
            {
                M.Button(assets, tabRow, "tab_tat_ca", "Tất cả", BtnColor.Green, tabSize),
                M.Button(assets, tabRow, "tab_san_xuat", "Sản xuất", BtnColor.Paper, tabSize),
                M.Button(assets, tabRow, "tab_ho_tro", "Hỗ trợ", BtnColor.Paper, tabSize),
                M.Button(assets, tabRow, "tab_trang_tri", "Trang trí", BtnColor.Paper, tabSize),
            };
            var view = M.Node(sheet.transform, "cuon", typeof(CanvasRenderer), typeof(Image), typeof(RectMask2D), typeof(ScrollRect));
            M.Fill(view).offsetMin = new Vector2(18, 18);
            view.offsetMax = new Vector2(-18, -100);
            var viewImg = view.GetComponent<Image>();
            viewImg.color = new Color(1, 1, 1, 0); // nhận kéo cho khay cuộn
            viewImg.raycastTarget = true;
            var tray = M.Node(view, "khay", typeof(GridLayoutGroup), typeof(ContentSizeFitter));
            tray.anchorMin = new Vector2(0, 0);
            tray.anchorMax = new Vector2(0, 1);
            tray.pivot = new Vector2(0, 0.5f);
            tray.offsetMin = tray.offsetMax = Vector2.zero;
            var gl = tray.GetComponent<GridLayoutGroup>();
            gl.cellSize = CardSize;
            gl.spacing = new Vector2(12, 12);
            gl.startCorner = GridLayoutGroup.Corner.UpperLeft;
            gl.startAxis = GridLayoutGroup.Axis.Vertical;
            gl.childAlignment = TextAnchor.MiddleLeft;
            gl.constraint = GridLayoutGroup.Constraint.FixedRowCount;
            gl.constraintCount = 2;
            tray.GetComponent<ContentSizeFitter>().horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
            var sr = view.GetComponent<ScrollRect>();
            sr.content = tray;
            sr.viewport = view;
            sr.horizontal = true;
            sr.vertical = false;
            sr.movementType = ScrollRect.MovementType.Elastic;
            sr.inertia = true;
            sr.scrollSensitivity = 30;
            sheet.gameObject.SetActive(false);

            // bảng chữ cũ: chỉ để dự phòng (HomeScene về bảng khi thiếu vòng), ẩn
            var panel = M.Img(ui, "bang", Sketch.Panel, paper, true, true);
            M.At(panel.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 228), new Vector2(1020, 420), new Vector2(0.5f, 0));
            var title = M.Text(panel.transform, "tieu_de", 36, Theme.Ink, TextAlignmentOptions.Left);
            M.At(title.rectTransform, new Vector2(0, 1), new Vector2(32, -20), new Vector2(950, 50), new Vector2(0, 1));
            var body = M.Text(panel.transform, "noi_dung", 26, Theme.Ink2, TextAlignmentOptions.TopLeft);
            M.At(body.rectTransform, new Vector2(0, 1), new Vector2(32, -78), new Vector2(950, 200), new Vector2(0, 1));
            body.enableAutoSizing = true;
            body.fontSizeMin = 18;
            body.fontSizeMax = 26;
            var row = M.Node(panel.transform, "nut", typeof(HorizontalLayoutGroup));
            M.At(row, new Vector2(0.5f, 0), new Vector2(0, 22), new Vector2(980, 110), new Vector2(0.5f, 0));
            var rl = row.GetComponent<HorizontalLayoutGroup>();
            rl.spacing = 14;
            rl.childAlignment = TextAnchor.MiddleCenter;
            rl.childControlWidth = rl.childControlHeight = false;
            rl.childForceExpandWidth = rl.childForceExpandHeight = false;
            var bsz = new Vector2(230, 100);
            var a = M.Button(assets, row, "a", "Thu", BtnColor.Orange, bsz);
            var b = M.Button(assets, row, "b", "Giao tướng", BtnColor.Blue, bsz);
            var c = M.Button(assets, row, "c", "Lên cấp", BtnColor.Green, bsz);
            var d = M.Button(assets, row, "d", "Dời", BtnColor.Purple, bsz);
            panel.gameObject.SetActive(false);

            // hàng nút dưới: kệ gỗ + 4 thẻ giấy như hàng nút đáy sảnh (HomeDockMenu, người dùng 2026-11-27: "phải có 1 nền đằng sau, có thể
            // làm giống phần đảo chính, icon quá nhỏ"); chấm đỏ trên Thu hết khi có đồ chờ thu
            var hud = HomeDockMenu.BuildBar(ui);
            var hBuild = hud[0];
            var hPaint = hud[1];
            var hHarvest = hud[2];
            var hSail = hud[3];

            scene.SetupUi(res, hint, hBuild.Button, hPaint.Button, hHarvest.Button, hSail.Button, tray, assets.prefabs.buttonSmall, panel.rectTransform,
                title, body, a, b, c, d);
            scene.SetupTrayIcon(card);
            scene.SetupChrome(ui.GetComponent<CanvasGroup>());
            scene.SetupCritters(ringRt.GetComponent<HomeRing>(), hBuild, hPaint, hHarvest, hSail, sheet.rectTransform, tabs);
        }
    }
}
