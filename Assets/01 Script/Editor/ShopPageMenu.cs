// Dựng prefab màn cửa hàng toàn màn hình (ShopPage) và màn nở trứng (EggHatchView), gọi từ menu "PokiClash/Prefab/Khác/Hộp thoại và màn∕Cửa hàng: dựng hết"
// (ShopMenu.BuildAll). GD_Claude/26 mục 13. Prefab:
// - Items/MucCuaHang (ShopSection): ruy băng đỏ máy bi (pk_ruy_bang) ghi tên mục, đồng hồ bên phải;
// - Items/LuoiCuaHang (ShopGrid): GridLayoutGroup, cột / cỡ ô đặt lúc chạy;
// - Items/OCuaHang (ShopTile): tờ giấy pha màu, hình to (hoặc chồng 3 quả), số, tên, dòng phụ, nhãn góc, sticker ×N, nút giá, chấm đỏ;
// - Items/TheCuaHang (ShopCard): thẻ ngang to: hình / mặt tướng trái, tên, mô tả, hàng ô thưởng thu nhỏ, đồng hồ, sticker, hai nút;
// - Dialogs/CuaHangLon (ShopPage): biến thể tờ giấy gốc HopThoai trải kín màn: tiêu đề, số bi, hàng 5 nút mục, trang cuộn dọc; vào UiKit;
// - Items/NoTrung (EggHatchView): canvas riêng: nền tối, hai lớp tia, vòng toả, trứng hai nửa (vòm / thân), chớp trắng, 16 sao, chữ,
//   chỗ ô mảnh, lưới bảng tổng, nút Nhận / Bỏ qua; gán UiKit.eggHatch;
// - Items/MoKhoaTuong (HeroUnlockView): canvas riêng: nền mực + vệt tốc độ (pha tụ lực), nền màu bậc + hoa văn sao trôi, đĩa giấy, hai
//   lớp tia, sao lấp lánh, sao băng, chỗ chân dung, chớp, bảng tin giấy (ruy băng TƯỚNG MỚI!, tên, viên bậc, danh hiệu, hệ, huy hiệu hệ),
//   nút Xem tướng / Tiếp; gán UiKit.heroUnlock.
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using static PokiClash.EditorTools.ShopMenu;

namespace PokiClash.EditorTools
{
    public static class ShopPageMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string ChestPath = "Assets/04 Prefabs/Dialogs/MoRuong.prefab";
        const string SectionPath = "Assets/04 Prefabs/Items/MucCuaHang.prefab";
        const string GridPath = "Assets/04 Prefabs/Items/LuoiCuaHang.prefab";
        const string TilePath = "Assets/04 Prefabs/Items/OCuaHang.prefab";
        const string CardPath = "Assets/04 Prefabs/Items/TheCuaHang.prefab";
        const string PagePath = "Assets/04 Prefabs/Dialogs/CuaHangLon.prefab";
        const string HatchPath = "Assets/04 Prefabs/Items/NoTrung.prefab";
        const string UnlockPath = "Assets/04 Prefabs/Items/MoKhoaTuong.prefab";

        public const float HeaderH = 118, NavH = 104;

        static Sprite Art(string path) => AssetDatabase.LoadAllAssetsAtPath(path).OfType<Sprite>().FirstOrDefault();
        static RewardTile TilePrefab => AssetDatabase.LoadAssetAtPath<GameObject>(ChestPath).GetComponent<ChestDialog>().TilePrefab;

        public static void Build()
        {
            var section = BuildSection();
            var grid = BuildGrid();
            var tile = BuildTile();
            var card = BuildCard();
            BuildPage(section, grid, tile, card);
            BuildHatch();
            BuildUnlock();
        }

        static GameObject NewRoot(string name, params System.Type[] comps) => Rt(name, null, comps).gameObject;

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

        static RectTransform Anchors(RectTransform r, Vector2 min, Vector2 max)
        {
            r.anchorMin = min;
            r.anchorMax = max;
            r.offsetMin = r.offsetMax = Vector2.zero;
            r.pivot = new Vector2(0.5f, 0.5f);
            return r;
        }

        static void Outline(TextMeshProUGUI t, float width)
        {
            t.outlineWidth = width;
            t.outlineColor = Theme.Ink;
        }

        // ---------- mục ----------

        static ShopSection BuildSection()
        {
            var (titleTpl, hintTpl) = Templates();
            var root = NewRoot("MucCuaHang", typeof(LayoutElement));
            Le(root.GetComponent<RectTransform>(), 120);
            ((RectTransform)root.transform).sizeDelta = new Vector2(1000, 120);
            var ribbon = Img("ruy_bang", root.transform, Art("Assets/03 Art/Pachinko/pk_ruy_bang.png"), Color.white);
            ribbon.preserveAspect = true;
            ribbon.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 0), new Vector2(600, 128));
            var title = Text(titleTpl, ribbon.transform, "ten", 40, TextAlignmentOptions.Center, Color.white);
            title.rectTransform.Stretch(90, 22, 90, 40);
            Outline(title, 0.22f);
            var pill = Img("dong_ho", root.transform, Sketch.Pill, Theme.Paper);
            pill.type = Image.Type.Sliced;
            pill.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-6, 0), new Vector2(200, 48), new Vector2(1, 0.5f));
            var timer = Text(hintTpl, pill.transform, "chu", 26, TextAlignmentOptions.Center, Theme.RedD);
            timer.rectTransform.Stretch();
            root.AddComponent<ShopSection>().Setup(title, timer, pill.gameObject);
            return Save<ShopSection>(root, SectionPath);
        }

        // ---------- lưới ----------

        static ShopGrid BuildGrid()
        {
            var root = NewRoot("LuoiCuaHang", typeof(GridLayoutGroup), typeof(ContentSizeFitter));
            var g = root.GetComponent<GridLayoutGroup>();
            g.spacing = new Vector2(20, 22);
            g.cellSize = new Vector2(320, 430);
            g.childAlignment = TextAnchor.UpperCenter;
            g.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            g.constraintCount = 3;
            root.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            root.AddComponent<ShopGrid>().Setup(g);
            return Save<ShopGrid>(root, GridPath);
        }

        // ---------- ô ----------

        static ShopTile BuildTile()
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var root = NewRoot("OCuaHang", typeof(CanvasRenderer), typeof(Image));
            ((RectTransform)root.transform).sizeDelta = new Vector2(320, 430);
            var bg = root.GetComponent<Image>();
            Theme.SetSprite(bg, Sketch.Panel);
            bg.type = Image.Type.Sliced;
            bg.color = Theme.Paper;
            bg.raycastTarget = false;

            var art = Img("hinh", root.transform, null, Color.white);
            Anchors(art.rectTransform, new Vector2(0.08f, 0.37f), new Vector2(0.92f, 0.93f));
            art.preserveAspect = true;
            var stackRt = Anchors(Rt("chong", root.transform), new Vector2(0.06f, 0.37f), new Vector2(0.94f, 0.93f));
            var stack = new Image[3];
            Vector2[,] box = { { new Vector2(0, 0.02f), new Vector2(0.6f, 0.8f) }, { new Vector2(0.4f, 0.02f), new Vector2(1, 0.8f) }, { new Vector2(0.18f, 0.16f), new Vector2(0.82f, 1) } };
            for (int i = 0; i < 3; i++)
            {
                stack[i] = Img("qua_" + (i + 1), stackRt, null, Color.white);
                Anchors(stack[i].rectTransform, box[i, 0], box[i, 1]);
                stack[i].preserveAspect = true;
            }
            var count = Text(titleTpl, root.transform, "so", 44, TextAlignmentOptions.BottomRight, Color.white);
            Anchors(count.rectTransform, new Vector2(0.45f, 0.36f), new Vector2(0.95f, 0.52f));
            Outline(count, 0.3f);
            var title = Text(titleTpl, root.transform, "ten", 32, TextAlignmentOptions.Center, Theme.Ink);
            Anchors(title.rectTransform, new Vector2(0.04f, 0.255f), new Vector2(0.96f, 0.36f));
            title.enableAutoSizing = true;
            title.fontSizeMin = 20;
            title.fontSizeMax = 32;
            title.textWrappingMode = TextWrappingModes.NoWrap;
            var sub = Text(hintTpl, root.transform, "phu", 22, TextAlignmentOptions.Center, Theme.Ink2);
            Anchors(sub.rectTransform, new Vector2(0.04f, 0.19f), new Vector2(0.96f, 0.265f));
            sub.enableAutoSizing = true;
            sub.fontSizeMin = 16;
            sub.fontSizeMax = 22;

            var buy = Ui.Spawn(kit.buttonSmall, root.transform);
            buy.name = "nut_mua";
            var br = buy.Rect;
            br.anchorMin = new Vector2(0.06f, 0);
            br.anchorMax = new Vector2(0.94f, 0);
            br.pivot = new Vector2(0.5f, 0);
            br.anchoredPosition = new Vector2(0, 16);
            br.sizeDelta = new Vector2(0, br.sizeDelta.y);
            buy.SetRole(BtnColor.Orange);
            buy.SetText("Mua");

            var ribbon = Img("nhan", root.transform, Sketch.Pill, Theme.Red);
            ribbon.type = Image.Type.Sliced;
            ribbon.rectTransform.Place(new Vector2(0, 1), new Vector2(4, -6), new Vector2(190, 46), new Vector2(0, 1));
            ribbon.rectTransform.localEulerAngles = new Vector3(0, 0, 5);
            var ribbonText = Text(hintTpl, ribbon.transform, "chu", 22, TextAlignmentOptions.Center, Color.white);
            ribbonText.rectTransform.Stretch(8, 2, 8, 2);
            ribbonText.enableAutoSizing = true;
            ribbonText.fontSizeMin = 14;
            ribbonText.fontSizeMax = 22;
            ribbonText.fontStyle = FontStyles.Bold;

            var value = Ui.Spawn(kit.stamp, root.transform);
            value.name = "gia_tri";
            var vr = (RectTransform)value.transform;
            vr.anchorMin = vr.anchorMax = vr.pivot = new Vector2(1, 1);
            vr.anchoredPosition = new Vector2(-2, -4);
            vr.localEulerAngles = new Vector3(0, 0, -8);
            vr.localScale = Vector3.one * 0.3f;

            var done = Text(titleTpl, root.transform, "da_mua", 30, TextAlignmentOptions.Center, Theme.GreenD);
            Anchors(done.rectTransform, new Vector2(0.04f, 0.02f), new Vector2(0.96f, 0.18f));
            done.rectTransform.localEulerAngles = new Vector3(0, 0, 4);

            var dot = Img("cham_do", root.transform, Sketch.Dot, Theme.Red);
            dot.rectTransform.Place(new Vector2(1, 1), new Vector2(-8, -8), new Vector2(32, 32), new Vector2(0.5f, 0.5f));

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (!gr.transform.IsChildOf(buy.transform)) gr.raycastTarget = false;
            root.AddComponent<ShopTile>().Setup(new ShopTile.Parts
            {
                bg = bg, art = art, ribbon = ribbon, dot = dot, stack = stack, title = title, sub = sub, count = count, ribbonText = ribbonText, done = done,
                value = value, buy = buy,
            });
            return Save<ShopTile>(root, TilePath);
        }

        // ---------- thẻ ngang ----------

        static ShopCard BuildCard()
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var root = NewRoot("TheCuaHang", typeof(CanvasRenderer), typeof(Image), typeof(LayoutElement));
            ((RectTransform)root.transform).sizeDelta = new Vector2(1000, 380);
            Le(root.GetComponent<RectTransform>(), 380);
            var bg = root.GetComponent<Image>();
            Theme.SetSprite(bg, Sketch.Panel);
            bg.type = Image.Type.Sliced;
            bg.color = Theme.Paper;
            bg.raycastTarget = false;

            var art = Img("hinh", root.transform, null, Color.white);
            art.rectTransform.anchorMin = new Vector2(0, 0);
            art.rectTransform.anchorMax = new Vector2(0, 1);
            art.rectTransform.pivot = new Vector2(0, 0.5f);
            art.rectTransform.offsetMin = new Vector2(24, 30);
            art.rectTransform.offsetMax = new Vector2(24 + 270, -40);
            art.preserveAspect = true;
            var hero = Img("mat_tuong", root.transform, null, Color.white);
            hero.rectTransform.anchorMin = art.rectTransform.anchorMin;
            hero.rectTransform.anchorMax = art.rectTransform.anchorMax;
            hero.rectTransform.pivot = art.rectTransform.pivot;
            hero.rectTransform.offsetMin = art.rectTransform.offsetMin;
            hero.rectTransform.offsetMax = art.rectTransform.offsetMax;
            hero.preserveAspect = true;

            const float X = 316;
            var title = Text(titleTpl, root.transform, "ten", 38, TextAlignmentOptions.MidlineLeft, Theme.Ink);
            title.rectTransform.anchorMin = new Vector2(0, 1);
            title.rectTransform.anchorMax = new Vector2(1, 1);
            title.rectTransform.pivot = new Vector2(0, 1);
            title.rectTransform.offsetMin = new Vector2(X, -70);
            title.rectTransform.offsetMax = new Vector2(-150, -18);
            title.enableAutoSizing = true;
            title.fontSizeMin = 24;
            title.fontSizeMax = 38;
            title.textWrappingMode = TextWrappingModes.NoWrap;
            var desc = Text(hintTpl, root.transform, "mo_ta", 23, TextAlignmentOptions.TopLeft, Theme.Ink2);
            desc.rectTransform.anchorMin = new Vector2(0, 1);
            desc.rectTransform.anchorMax = new Vector2(1, 1);
            desc.rectTransform.pivot = new Vector2(0, 1);
            desc.rectTransform.offsetMin = new Vector2(X, -130);
            desc.rectTransform.offsetMax = new Vector2(-24, -72);
            desc.enableAutoSizing = true;
            desc.fontSizeMin = 16;
            desc.fontSizeMax = 23;

            const float S = 0.72f;
            var items = Rt("mon", root.transform, typeof(GridLayoutGroup));
            items.anchorMin = items.anchorMax = items.pivot = new Vector2(0, 1);
            items.anchoredPosition = new Vector2(X, -134);
            items.sizeDelta = new Vector2(5 * RewardTile.W + 4 * 10, RewardTile.H);
            items.localScale = Vector3.one * S;
            var g = items.GetComponent<GridLayoutGroup>();
            g.cellSize = new Vector2(RewardTile.W, RewardTile.H);
            g.spacing = new Vector2(10, 10);
            g.constraint = GridLayoutGroup.Constraint.FixedRowCount;
            g.constraintCount = 1;
            g.childAlignment = TextAnchor.UpperLeft;

            var pill = Img("dong_ho", root.transform, Sketch.Pill, Theme.Paper);
            pill.type = Image.Type.Sliced;
            pill.rectTransform.Place(new Vector2(0, 1), new Vector2(14, 14), new Vector2(200, 46), new Vector2(0, 1));
            var timer = Text(hintTpl, pill.transform, "chu", 24, TextAlignmentOptions.Center, Theme.RedD);
            timer.rectTransform.Stretch(6, 2, 6, 2);
            timer.fontStyle = FontStyles.Bold;

            var value = Ui.Spawn(kit.stamp, root.transform);
            value.name = "gia_tri";
            var vr = (RectTransform)value.transform;
            vr.anchorMin = vr.anchorMax = vr.pivot = new Vector2(1, 1);
            vr.anchoredPosition = new Vector2(-6, -4);
            vr.localEulerAngles = new Vector3(0, 0, -7);
            vr.localScale = Vector3.one * 0.36f;

            var buy = Ui.Spawn(kit.buttonNormal, root.transform);
            buy.name = "nut_mua";
            var br = buy.Rect;
            br.anchorMin = br.anchorMax = br.pivot = new Vector2(1, 0);
            br.anchoredPosition = new Vector2(-22, 20);
            br.sizeDelta = new Vector2(270, br.sizeDelta.y);
            buy.SetRole(BtnColor.Orange);
            var extra = Ui.Spawn(kit.buttonSmall, root.transform);
            extra.name = "nut_phu";
            var er = extra.Rect;
            er.anchorMin = er.anchorMax = er.pivot = new Vector2(1, 0);
            er.anchoredPosition = new Vector2(-22 - 270 - 16, 24);
            er.sizeDelta = new Vector2(230, er.sizeDelta.y);

            var note = Text(hintTpl, root.transform, "ghi_chu", 22, TextAlignmentOptions.MidlineLeft, Theme.Ink2);
            note.rectTransform.Place(new Vector2(0, 0), new Vector2(X, 22), new Vector2(380, 40), new Vector2(0, 0));
            var done = Text(titleTpl, root.transform, "da_mua", 36, TextAlignmentOptions.Center, Theme.GreenD);
            done.rectTransform.Place(new Vector2(1, 0), new Vector2(-30, 26), new Vector2(300, 64), new Vector2(1, 0));
            done.rectTransform.localEulerAngles = new Vector3(0, 0, 6);

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (!gr.transform.IsChildOf(buy.transform) && !gr.transform.IsChildOf(extra.transform)) gr.raycastTarget = false;
            root.AddComponent<ShopCard>().Setup(new ShopCard.Parts
            {
                bg = bg, art = art, heroArt = hero, title = title, desc = desc, timer = timer, done = done, note = note, items = items, value = value,
                buy = buy, extra = extra,
            }, TilePrefab, pill.gameObject);
            return Save<ShopCard>(root, CardPath);
        }

        // ---------- màn cửa hàng ----------

        static void BuildPage(ShopSection section, ShopGrid grid, ShopTile tile, ShopCard card)
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "CuaHangLon";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(1080, false, true);
                var sheet = view.Sheet;
                // tờ giấy trải kín màn (bỏ tự giãn theo nội dung)
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                sheet.anchorMin = Vector2.zero;
                sheet.anchorMax = Vector2.one;
                sheet.pivot = new Vector2(0.5f, 0.5f);
                sheet.offsetMin = new Vector2(0, 0);
                sheet.offsetMax = new Vector2(0, -40);
                view.SetFlat(true);

                var body = Rt("noi_dung", sheet);
                body.Stretch(0, 0, 0, 0);
                body.SetAsLastSibling();
                // tiêu đề, số bi (chừa nút đóng góc phải của tờ giấy)
                var title = Text(titleTpl, body, "tieu_de", 62, TextAlignmentOptions.MidlineLeft, Theme.Ink);
                title.rectTransform.Place(new Vector2(0, 1), new Vector2(44, -14), new Vector2(520, HeaderH - 20), new Vector2(0, 1));
                var chip = Img("so_bi", body, Sketch.Pill, Theme.Paper2);
                chip.type = Image.Type.Sliced;
                chip.rectTransform.Place(new Vector2(1, 1), new Vector2(-150, -30), new Vector2(240, 64), new Vector2(1, 1));
                var ball = Img("icon", chip.transform, Icon("ball"), Color.white);
                ball.preserveAspect = true;
                ball.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(8, 0), new Vector2(60, 60), new Vector2(0, 0.5f));
                var balls = Text(titleTpl, chip.transform, "so", 36, TextAlignmentOptions.MidlineRight, Theme.Ink);
                balls.rectTransform.Stretch(70, 4, 18, 4);

                // hàng nút mục
                var navRow = Rt("hang_muc", body, typeof(HorizontalLayoutGroup));
                navRow.anchorMin = new Vector2(0, 1);
                navRow.anchorMax = new Vector2(1, 1);
                navRow.pivot = new Vector2(0.5f, 1);
                navRow.offsetMin = new Vector2(24, -HeaderH - NavH);
                navRow.offsetMax = new Vector2(-24, -HeaderH);
                var hl = navRow.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 10;
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var nav = new SketchButton[ShopPage.Sections.Length];
                var dots = new GameObject[nav.Length];
                string[] names = { "Ưu đãi", "Miễn phí", "Trứng", "Bi", "Đặc quyền" };
                for (int i = 0; i < nav.Length; i++)
                {
                    var b = Ui.Spawn(kit.buttonSmall, navRow);
                    b.name = "muc_" + ShopPage.Sections[i];
                    b.Rect.sizeDelta = new Vector2(i == 4 ? 220 : 186, b.Rect.sizeDelta.y);
                    b.SetText(names[i]);
                    b.SetRole(i == 0 ? BtnColor.Orange : BtnColor.Paper);
                    var dot = Img("cham_do", b.transform, Sketch.Dot, Theme.Red);
                    dot.rectTransform.Place(new Vector2(1, 1), new Vector2(-6, -6), new Vector2(26, 26), new Vector2(0.5f, 0.5f));
                    dot.gameObject.SetActive(false);
                    nav[i] = b;
                    dots[i] = dot.gameObject;
                }

                // trang cuộn
                var scrollGo = Rt("cuon", body, typeof(CanvasRenderer), typeof(Image), typeof(ScrollRect)).gameObject;
                var srt = (RectTransform)scrollGo.transform;
                srt.Stretch(0, HeaderH + NavH + 6, 0, 18);
                scrollGo.GetComponent<Image>().color = new Color(1, 1, 1, 0);
                var scroll = scrollGo.GetComponent<ScrollRect>();
                scroll.horizontal = false;
                scroll.vertical = true;
                scroll.movementType = ScrollRect.MovementType.Elastic;
                scroll.scrollSensitivity = 30;
                var viewport = Rt("khung", scrollGo.transform, typeof(RectMask2D));
                viewport.Stretch();
                var content = Rt("trang", viewport, typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
                content.anchorMin = new Vector2(0, 1);
                content.anchorMax = new Vector2(1, 1);
                content.pivot = new Vector2(0.5f, 1);
                content.anchoredPosition = Vector2.zero;
                content.sizeDelta = Vector2.zero;
                var vl = content.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 18;
                vl.padding = new RectOffset(40, 40, 8, 60);
                vl.childAlignment = TextAnchor.UpperCenter;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = true;
                vl.childForceExpandHeight = false;
                content.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                scroll.viewport = viewport;
                scroll.content = content;

                // nút đóng của tờ giấy lên trên cùng
                view.Close.transform.SetAsLastSibling();

                root.AddComponent<ShopPage>().Setup(new ShopPage.Parts
                {
                    title = title, balls = balls, nav = nav, navDots = dots, scroll = scroll, content = content,
                }, section, grid, tile, card);
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, PagePath).GetComponent<ShopPage>();
                if (!kit.dialogs.Any(x => x is ShopPage))
                {
                    kit.dialogs.Add(dlg);
                    EditorUtility.SetDirty(kit);
                }
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- màn nở trứng ----------

        static void BuildHatch()
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var root = NewRoot("NoTrung", typeof(Canvas), typeof(GraphicRaycaster), typeof(CanvasGroup));
            var rt = (RectTransform)root.transform;
            rt.sizeDelta = new Vector2(1080, 1920);
            var cv = root.GetComponent<Canvas>();
            cv.overrideSorting = true;
            cv.sortingOrder = 450;

            // nền tối (khoảng màu Linear: alpha cao mới tối thật, memory ui-phu-toi-linear)
            var dim = Img("nen_toi", root.transform, null, new Color(Theme.Ink.r, Theme.Ink.g, Theme.Ink.b, 0.985f));
            dim.rectTransform.Stretch();
            var catcher = Rt("cham", root.transform, typeof(CanvasRenderer), typeof(Image), typeof(Button));
            catcher.Stretch();
            var ci = catcher.GetComponent<Image>();
            ci.color = new Color(0, 0, 0, 0);
            var btn = catcher.GetComponent<Button>();
            btn.transition = Selectable.Transition.None;
            btn.targetGraphic = ci;

            var center = new Vector2(0, 90);
            var rays = Img("tia", root.transform, Art("Assets/03 Art/Pachinko/pk_fx_tia_toa.png"), new Color(1, 1, 1, 0));
            rays.rectTransform.Place(new Vector2(0.5f, 0.5f), center, new Vector2(1100, 1100));
            var rays2 = Img("tia_2", root.transform, Art("Assets/03 Art/Pachinko/pk_fx_tia_toa.png"), new Color(1, 1, 1, 0));
            rays2.rectTransform.Place(new Vector2(0.5f, 0.5f), center, new Vector2(760, 760));
            rays2.rectTransform.localEulerAngles = new Vector3(0, 0, 15);
            var ring = Img("vong", root.transform, Art("Assets/03 Art/Pachinko/pk_fx_vong_day.png"), new Color(1, 1, 1, 0));
            ring.rectTransform.Place(new Vector2(0.5f, 0.5f), center, new Vector2(320, 320));

            var egg = Rt("trung", root.transform);
            egg.Place(new Vector2(0.5f, 0.5f), center, new Vector2(320, 430));
            Image Half(string n, Image.OriginVertical origin)
            {
                var img = Img(n, egg, null, Color.white);
                img.type = Image.Type.Filled;
                img.fillMethod = Image.FillMethod.Vertical;
                img.fillOrigin = (int)origin;
                img.preserveAspect = false;
                img.rectTransform.Stretch();
                return img;
            }
            var bottom = Half("than", Image.OriginVertical.Bottom);
            var top = Half("vom", Image.OriginVertical.Top);

            var holder = Rt("o_manh", root.transform);
            holder.Place(new Vector2(0.5f, 0.5f), center, new Vector2(RewardTile.W, RewardTile.H));
            holder.localScale = Vector3.one * 1.9f;

            var star = Art("Assets/03 Art/Pachinko/fx2_sao4.png");
            var sparks = new Image[16];
            for (int i = 0; i < sparks.Length; i++)
            {
                sparks[i] = Img("sao_" + i, root.transform, star, Color.white);
                sparks[i].rectTransform.Place(new Vector2(0.5f, 0.5f), center, new Vector2(56, 56));
                sparks[i].gameObject.SetActive(false);
            }
            var flash = Img("chop", root.transform, null, new Color(1, 1, 1, 0));
            flash.rectTransform.Stretch();

            var title = Text(titleTpl, root.transform, "ten_trung", 60, TextAlignmentOptions.Center, Color.white);
            title.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -230), new Vector2(980, 90), new Vector2(0.5f, 1));
            Outline(title, 0.2f);
            var up = Text(titleTpl, root.transform, "nang_bac", 76, TextAlignmentOptions.Center, Theme.Yellow);
            up.rectTransform.Place(new Vector2(0.5f, 0.5f), center + new Vector2(0, 420), new Vector2(900, 110));
            up.rectTransform.localEulerAngles = new Vector3(0, 0, 4);
            Outline(up, 0.28f);
            var heroName = Text(titleTpl, root.transform, "ten_tuong", 56, TextAlignmentOptions.Center, Color.white);
            heroName.rectTransform.Place(new Vector2(0.5f, 0.5f), center + new Vector2(0, -330), new Vector2(980, 170));
            Outline(heroName, 0.2f);
            var hint = Text(hintTpl, root.transform, "cham_tiep", 32, TextAlignmentOptions.Center, Theme.Paper);
            hint.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 230), new Vector2(900, 60), new Vector2(0.5f, 0));

            var grid = Rt("bang_tong", root.transform, typeof(GridLayoutGroup));
            grid.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 60), new Vector2(5 * RewardTile.W + 4 * 18, 2 * RewardTile.H + 30));
            grid.localScale = Vector3.one * 1.18f;
            var gg = grid.GetComponent<GridLayoutGroup>();
            gg.cellSize = new Vector2(RewardTile.W, RewardTile.H);
            gg.spacing = new Vector2(18, 30);
            gg.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            gg.constraintCount = 5;
            gg.childAlignment = TextAnchor.MiddleCenter;

            var ok = Ui.Spawn(kit.buttonNormal, root.transform);
            ok.name = "nut_nhan";
            ok.Rect.Place(new Vector2(0.5f, 0), new Vector2(0, 200), new Vector2(360, ok.Rect.sizeDelta.y), new Vector2(0.5f, 0));
            ok.SetRole(BtnColor.Green);
            ok.SetText("Nhận");
            var skip = Ui.Spawn(kit.buttonSmall, root.transform);
            skip.name = "nut_bo_qua";
            skip.Rect.Place(new Vector2(1, 1), new Vector2(-30, -60), new Vector2(200, skip.Rect.sizeDelta.y), new Vector2(1, 1));
            skip.SetRole(BtnColor.Paper);
            skip.SetText("Bỏ qua");

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (gr != ci && !gr.transform.IsChildOf(ok.transform) && !gr.transform.IsChildOf(skip.transform)) gr.raycastTarget = false;
            root.AddComponent<EggHatchView>().Setup(new EggHatchView.Parts
            {
                dim = dim, rays = rays, rays2 = rays2, ring = ring, flash = flash, eggTop = top, eggBottom = bottom, egg = egg, tileHolder = holder, grid = grid,
                sparks = sparks, title = title, hint = hint, up = up, heroName = heroName, catcher = btn, ok = ok, skip = skip,
            }, TilePrefab);
            var view = Save<EggHatchView>(root, HatchPath);
            kit.eggHatch = view;
            EditorUtility.SetDirty(kit);
        }
        // ---------- màn mở khoá tướng ----------

        static void BuildUnlock()
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var root = NewRoot("MoKhoaTuong", typeof(Canvas), typeof(GraphicRaycaster), typeof(CanvasGroup));
            ((RectTransform)root.transform).sizeDelta = new Vector2(1080, 1920);
            var cv = root.GetComponent<Canvas>();
            cv.overrideSorting = true;
            cv.sortingOrder = 460;
            const string P = "Assets/03 Art/Pachinko/";

            var catcher = Rt("cham", root.transform, typeof(CanvasRenderer), typeof(Image), typeof(Button));
            catcher.Stretch();
            var ci = catcher.GetComponent<Image>();
            ci.color = new Color(0, 0, 0, 0);
            var btn = catcher.GetComponent<Button>();
            btn.transition = Selectable.Transition.None;
            btn.targetGraphic = ci;

            // nền pha tụ lực: mực xanh thẫm, vệt tốc độ dọc
            var dark = Img("nen_muc", root.transform, null, Theme.Hex("#17244a"));
            dark.rectTransform.Stretch();
            var speed = Rt("vet_toc_do", root.transform);
            speed.Stretch();
            var streakSprite = Art(P + "pk_fx_vach_toc.png");
            var streaks = new Image[9];
            for (int i = 0; i < streaks.Length; i++)
            {
                streaks[i] = Img("vet_" + i, speed, streakSprite, new Color(0.75f, 0.85f, 1, 0.35f));
                streaks[i].rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(-480 + i * 120 + (i % 2) * 30, 0), new Vector2(420, 150));
                streaks[i].rectTransform.localEulerAngles = new Vector3(0, 0, -90);
            }

            // nền lộ diện: màu bậc + hoa văn sao trôi (ô lặp)
            var rarityBg = Img("nen_bac", root.transform, null, Theme.Blue);
            rarityBg.rectTransform.Stretch();
            var pattern = Img("hoa_van", root.transform, Art(P + "pk_fx_sao_rong.png"), new Color(1, 1, 1, 0.16f));
            pattern.type = Image.Type.Tiled;
            pattern.pixelsPerUnitMultiplier = 1.4f;
            pattern.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(2600, 3000));
            pattern.rectTransform.localEulerAngles = new Vector3(0, 0, 10);
            pattern.gameObject.SetActive(false); // nền trơn (người dùng 2026-11-23), giữ lớp cho bản sau

            var heroPos = new Vector2(0, -330);
            var discPos = heroPos + new Vector2(0, 380);
            var rays = Img("tia", root.transform, Art(P + "pk_fx_tia_toa.png"), Color.white);
            rays.rectTransform.Place(new Vector2(0.5f, 0.5f), discPos, new Vector2(1400, 1400));
            var rays2 = Img("tia_2", root.transform, Art(P + "pk_fx_tia_toa.png"), Color.white);
            rays2.rectTransform.Place(new Vector2(0.5f, 0.5f), discPos, new Vector2(950, 950));
            rays2.rectTransform.localEulerAngles = new Vector3(0, 0, 15);
            var disc = Img("dia", root.transform, Sketch.Burst, Color.white);
            disc.rectTransform.Place(new Vector2(0.5f, 0.5f), discPos, new Vector2(760, 760));

            var hero = Rt("tuong", root.transform);
            hero.Place(new Vector2(0.5f, 0.5f), heroPos, new Vector2(660, 820), new Vector2(0.5f, 0));
            var spin = Rt("quay", hero);
            spin.Place(new Vector2(0.5f, 0), Vector2.zero, new Vector2(660, 820), new Vector2(0.5f, 0));

            var star = Art(P + "fx2_sao4.png");
            var sparks = new Image[10];
            for (int i = 0; i < sparks.Length; i++)
            {
                sparks[i] = Img("sao_" + i, root.transform, star, Color.white);
                sparks[i].rectTransform.Place(new Vector2(0.5f, 0.5f), discPos, new Vector2(70, 70));
                sparks[i].gameObject.SetActive(false);
            }
            var shootSprite = Art(P + "pk_sao_bang.png");
            var shooting = new Image[6];
            for (int i = 0; i < shooting.Length; i++)
            {
                shooting[i] = Img("sao_bang_" + i, root.transform, shootSprite, Color.white);
                shooting[i].preserveAspect = true;
                shooting[i].rectTransform.Place(new Vector2(0.5f, 0.5f), discPos, new Vector2(150, 150));
                shooting[i].gameObject.SetActive(false);
            }

            var flash = Img("chop", root.transform, null, new Color(1, 1, 1, 0));
            flash.rectTransform.Stretch();

            // bảng tin giấy (dưới tướng), trượt từ phải vào
            var panelImg = Img("bang_tin", root.transform, Sketch.Panel, Theme.Paper);
            panelImg.type = Image.Type.Sliced;
            var panel = panelImg.rectTransform;
            panel.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -560), new Vector2(940, 560));
            var ribbon = Img("ruy_bang", panel, Art(P + "pk_ruy_bang.png"), Color.white);
            ribbon.preserveAspect = true;
            ribbon.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, 46), new Vector2(620, 132), new Vector2(0.5f, 1));
            var ribbonText = Text(titleTpl, ribbon.transform, "chu", 44, TextAlignmentOptions.Center, Color.white);
            ribbonText.rectTransform.Stretch(90, 22, 90, 40);
            Outline(ribbonText, 0.22f);
            var heroName = Text(titleTpl, panel, "ten", 66, TextAlignmentOptions.Center, Theme.Ink);
            heroName.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(40, -96), new Vector2(700, 86), new Vector2(0.5f, 1));
            heroName.enableAutoSizing = true;
            heroName.fontSizeMin = 36;
            heroName.fontSizeMax = 66;
            var pill = Img("vien_bac", panel, Sketch.Pill, Theme.Orange);
            pill.type = Image.Type.Sliced;
            pill.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(40, -190), new Vector2(300, 56), new Vector2(0.5f, 1));
            var rarity = Text(titleTpl, pill.transform, "bac", 32, TextAlignmentOptions.Center, Color.white);
            rarity.rectTransform.Stretch(10, 2, 10, 2);
            var elem = Text(hintTpl, panel, "he", 30, TextAlignmentOptions.Center, Theme.Ink2);
            elem.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(40, -256), new Vector2(700, 44), new Vector2(0.5f, 1));
            var title = Text(hintTpl, panel, "danh_hieu", 30, TextAlignmentOptions.Center, Theme.Ink2);
            title.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(40, -302), new Vector2(760, 90), new Vector2(0.5f, 1));
            title.fontStyle = FontStyles.Italic;
            var badge = Rt("huy_hieu", panel);
            badge.Place(new Vector2(0, 1), new Vector2(110, -170), new Vector2(150, 150));
            var badgeBg = Img("nen", badge, Sketch.Round, Theme.Paper2);
            badgeBg.rectTransform.Stretch();
            var badgeIcon = Img("icon", badge, null, Color.white);
            badgeIcon.preserveAspect = true;
            badgeIcon.rectTransform.Stretch(22, 22, 22, 22);

            var view = Ui.Spawn(kit.buttonNormal, panel);
            view.name = "nut_xem_tuong";
            view.Rect.Place(new Vector2(0.5f, 0), new Vector2(-220, 40), new Vector2(360, view.Rect.sizeDelta.y), new Vector2(0.5f, 0));
            view.SetRole(BtnColor.Paper);
            view.SetText("Xem tướng");
            var next = Ui.Spawn(kit.buttonNormal, panel);
            next.name = "nut_tiep";
            next.Rect.Place(new Vector2(0.5f, 0), new Vector2(220, 40), new Vector2(360, next.Rect.sizeDelta.y), new Vector2(0.5f, 0));
            next.SetRole(BtnColor.Green);
            next.SetText("Tiếp");

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (gr != ci && !gr.transform.IsChildOf(view.transform) && !gr.transform.IsChildOf(next.transform)) gr.raycastTarget = false;
            root.AddComponent<HeroUnlockView>().Setup(new HeroUnlockView.Parts
            {
                dark = dark, rarityBg = rarityBg, pattern = pattern, disc = disc, rays = rays, rays2 = rays2, flash = flash, speed = speed, hero = hero, spin = spin,
                panel = panel, badge = badge, streaks = streaks, sparks = sparks, shooting = shooting, badgeIcon = badgeIcon, ribbon = ribbon,
                ribbonText = ribbonText, heroName = heroName, rarity = rarity, title = title, elem = elem, rarityPill = pill, next = next, view = view,
                catcher = btn,
            });
            var v = Save<HeroUnlockView>(root, UnlockPath);
            kit.heroUnlock = v;
            EditorUtility.SetDirty(kit);
        }
    }
}
