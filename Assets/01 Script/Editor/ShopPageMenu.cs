// Dựng prefab màn cửa hàng toàn màn hình (ShopPage) và màn nở trứng (EggHatchView), gọi từ menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết"
// (ShopMenu.BuildAll). GD_Claude/26 mục 13. Prefab:
// Bản 3 (2026-11-27, học cửa hàng Clash of Critters, mục 15): sprite Assets/03 Art/Shop/v3 (ArtGen/Shop/v3/ve_ui.py --assets), màu ShopHue.
// - Items/MucCuaHang (ShopSection): băng tím caro thoi viền mực, tên mục vàng, đồng hồ bên phải;
// - Items/LuoiCuaHang (ShopGrid): GridLayoutGroup, cột / cỡ ô đặt lúc chạy;
// - Items/OMonCuaHang (ShopItemCell): ô món kem viền mực, hình, vạch tối ghi số;
// - Items/OCuaHang (ShopTile): nền màu tươi caro + sao nổ, tên trên đầu, hình to (hoặc chồng 3 quả), số, dòng phụ, nhãn góc, nhãn đỏ ×N,
//   dải tối đáy có nút giá xanh lá, chấm đỏ;
// - Items/TheCuaHang (ShopCard): thẻ ngang: nền ba lớp (màu chính + mảng phải cắt chéo + sao nổ), dải tên tối, hình / mặt tướng trái,
//   ô món canh phải, mô tả, đồng hồ, nhãn đỏ "Giá trị ×N", nút giá xanh lá và nút phụ;
// - Dialogs/CuaHangLon (ShopPage): biến thể tờ giấy gốc HopThoai trải kín màn, phủ nền tối: thanh trên (số bi, tiêu đề vàng, nút đóng), cột
//   5 mục bên trái (hình gói + tên, ô chọn tím → lam), trang cuộn dọc bên phải; vào UiKit;
// - Items/NoTrung (EggHatchView): canvas riêng: nền tối, hai lớp tia, vòng toả, trứng hai nửa (vòm / thân), chớp trắng, 16 sao, chữ,
//   chỗ ô mảnh, lưới bảng tổng, nút Nhận / Bỏ qua; gán UiKit.eggHatch;
// - Items/MoKhoaTuong (HeroUnlockView): canvas riêng: nền gradient màu bậc, trang sổ (dòng kẻ, lề đỏ, ruy băng TƯỚNG MỚI!), chỗ
//   tướng, tranh chì (material PencilDraw), nét viền (InkStroke), khối chữ (tên, viên bậc, hệ, danh hiệu, 3 dòng chỉ số, nút Xem
//   tướng / Tiếp), sao trắng, bút chì (2026-11-24: bút chì vẽ tướng lên trang sổ rồi tướng bật ra); gán UiKit.heroUnlock.
// - Items/QuaNgay (DailyGiftView, 2026-11-27): canvas riêng: nền đen, hai lớp tia + quầng + lõi quầng + vòng + vệt loé (ảnh sáng mềm pk_g_*
//   cộng sáng, material Resources/UIAdditive), hình quà, dấu ×2, số, tên món, hàng quà kèm, sao vẽ tay, chớp trắng, chữ "Quà hôm nay",
//   nút "Nhận ×2" to (TV, viền sáng bám mép nút: material Resources/UIEdgeGlow, 2026-11-27) và nút "Nhận thường" nhỏ (nhóm mờ dần);
//   gán UiKit.dailyGift.
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
        const string ItemCellPath = "Assets/04 Prefabs/Items/OMonCuaHang.prefab";
        const string PagePath = "Assets/04 Prefabs/Dialogs/CuaHangLon.prefab";
        const string HatchPath = "Assets/04 Prefabs/Items/NoTrung.prefab";
        const string UnlockPath = "Assets/04 Prefabs/Items/MoKhoaTuong.prefab";
        const string GiftPath = "Assets/04 Prefabs/Items/QuaNgay.prefab";

        public const float HeaderH = 118, NavH = 104;

        static Sprite Art(string path) => AssetDatabase.LoadAllAssetsAtPath(path).OfType<Sprite>().FirstOrDefault();
        static RewardTile TilePrefab => AssetDatabase.LoadAssetAtPath<GameObject>(ChestPath).GetComponent<ChestDialog>().TilePrefab;

        public static void Build()
        {
            var section = BuildSection();
            var grid = BuildGrid();
            var tile = BuildTile();
            var card = BuildCard(BuildItemCell());
            BuildPage(section, grid, tile, card);
            BuildHatch();
            BuildUnlock();
            BuildGift();
        }

        // chỉ màn cửa hàng (bản 3): mục, lưới, ô món, ô, thẻ, màn; không dựng lại màn nở trứng / mở khoá / quà ngày, không đụng App.prefab
        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: chỉ màn cửa hàng (CuaHangLon)", priority = 71)]
        public static void BuildShopOnly()
        {
            var section = BuildSection();
            var grid = BuildGrid();
            var tile = BuildTile();
            var card = BuildCard(BuildItemCell());
            BuildPage(section, grid, tile, card);
            AssetDatabase.SaveAssets();
            Debug.Log("[Cửa hàng] Đã dựng màn cửa hàng bản 3: MucCuaHang, LuoiCuaHang, OMonCuaHang, OCuaHang, TheCuaHang, CuaHangLon.");
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

        // ---------- bản 3: sprite, màu, nút (GD_Claude/26 mục 17) ----------

        const string V3 = "Assets/03 Art/Shop/v3/";
        internal static readonly Color Navy = Theme.Hex("#16142a"), Gold = Theme.Hex("#ffd84a"), TopBg = Theme.Hex("#1f1f2b"), SideBg = Theme.Hex("#1b163e"),
            DoneGreen = Theme.Hex("#a6ff6e");
        internal static readonly Vector4 CardBorder = new Vector4(40, 110, 40, 40), TileBorder = new Vector4(34, 104, 34, 34), Round30 = new Vector4(30, 30, 30, 30),
            BtnBorder = new Vector4(36, 36, 36, 36);
        internal static readonly Vector4 PillBorder = new Vector4(24, 24, 24, 24); // vien.png: viên thuốc trơn của bộ v3 (Sketch.Pill rỗng khi dựng ngoài "dựng hết")

        // sprite bản 3 (ArtGen/Shop/v3/ve_ui.py --assets), đặt viền 9 mảnh (trái, dưới, phải, trên)
        internal static Sprite V3Sprite(string name, Vector4 border)
        {
            string path = V3 + name + ".png";
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (!ti)
            {
                Debug.LogError($"[Cửa hàng] Thiếu {path}: chạy ArtGen/Shop/v3/ve_ui.py --assets");
                return null;
            }
            if (ti.spriteBorder != border)
            {
                ti.spriteBorder = border;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        // chữ trắng / vàng viền mực xanh thẫm (trên nền màu tươi)
        internal static void Ink(TextMeshProUGUI t, float width)
        {
            t.outlineWidth = width;
            t.outlineColor = Navy;
        }

        internal static Image Sliced(string name, Transform parent, Sprite s, Color c)
        {
            var img = Img(name, parent, s, c);
            img.type = Image.Type.Sliced;
            img.rectTransform.Stretch();
            return img;
        }

        // chữ nút: chép chữ của nút kit (đúng phông + material viền chữ mà SketchButton đổi theo vai trò)
        internal static TextMeshProUGUI KitLabel(Transform parent, float size)
        {
            var src = Kit.buttonNormal.Label;
            var t = Object.Instantiate(src.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = "chu";
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            foreach (var c in t.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
            for (int i = t.transform.childCount - 1; i >= 0; i--) Object.DestroyImmediate(t.transform.GetChild(i).gameObject);
            t.enableAutoSizing = true;
            t.fontSizeMax = size;
            t.fontSizeMin = 16;
            t.fontSize = size;
            t.alignment = TextAlignmentOptions.Center;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.raycastTarget = false;
            return t;
        }

        internal static (Material outlined, Material plain) KitLabelMats()
        {
            var so = new SerializedObject(Kit.buttonNormal);
            return ((Material)so.FindProperty("labelOutlined").objectReferenceValue, (Material)so.FindProperty("labelPlain").objectReferenceValue);
        }

        // nút giá: tấm xám hai tông viền mực (nut_gia) tô xanh lá; đè đổi tấm tối (nut_gia_an)
        internal static SketchButton PriceButton(Transform parent, string name, float w, float h, float font)
        {
            var (outlined, plain) = KitLabelMats();
            var img = Img(name, parent, V3Sprite("nut_gia", BtnBorder), ShopHue.Lime);
            img.type = Image.Type.Sliced;
            img.raycastTarget = true;
            img.rectTransform.sizeDelta = new Vector2(w, h);
            var label = KitLabel(img.transform, font);
            label.rectTransform.Stretch(22, 8, 22, 18); // chừa môi tối dưới
            var b = img.gameObject.AddComponent<SketchButton>();
            b.Setup(img, label, false, img.sprite, V3Sprite("nut_gia_an", BtnBorder), outlined, plain);
            b.SetRole(BtnColor.Green);
            b.SetColor(ShopHue.Lime);
            b.SetText("Mua");
            return b;
        }

        // ---------- mục ----------

        static ShopSection BuildSection()
        {
            var (titleTpl, hintTpl) = Templates();
            var root = NewRoot("MucCuaHang", typeof(LayoutElement));
            Le(root.GetComponent<RectTransform>(), 100);
            ((RectTransform)root.transform).sizeDelta = new Vector2(ShopPage.ContentW, 100);
            var band = Sliced("bang", root.transform, V3Sprite("muc_bang", Round30), Color.white);
            var title = Text(titleTpl, band.transform, "ten", 54, TextAlignmentOptions.Center, Gold);
            title.rectTransform.Stretch(150, 4, 150, 12);
            title.enableAutoSizing = true;
            title.fontSizeMin = 30;
            title.fontSizeMax = 54;
            title.textWrappingMode = TextWrappingModes.NoWrap;
            Ink(title, 0.3f);
            var pill = Img("dong_ho", band.transform, V3Sprite("vien", PillBorder), Navy);
            pill.type = Image.Type.Sliced;
            pill.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-16, 0), new Vector2(190, 54), new Vector2(1, 0.5f));
            var timer = Text(hintTpl, pill.transform, "chu", 26, TextAlignmentOptions.Center, Color.white);
            timer.rectTransform.Stretch(6, 2, 6, 2);
            timer.fontStyle = FontStyles.Bold;
            root.AddComponent<ShopSection>().Setup(title, timer, pill.gameObject);
            return Save<ShopSection>(root, SectionPath);
        }

        // ---------- lưới ----------

        static ShopGrid BuildGrid()
        {
            var root = NewRoot("LuoiCuaHang", typeof(GridLayoutGroup), typeof(ContentSizeFitter));
            var g = root.GetComponent<GridLayoutGroup>();
            g.spacing = new Vector2(16, 20);
            g.cellSize = new Vector2(275, 430);
            g.childAlignment = TextAnchor.UpperCenter;
            g.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            g.constraintCount = 3;
            root.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            root.AddComponent<ShopGrid>().Setup(g);
            return Save<ShopGrid>(root, GridPath);
        }

        // ---------- ô món trong thẻ ----------

        static ShopItemCell BuildItemCell()
        {
            var root = NewRoot("OMonCuaHang", typeof(CanvasRenderer), typeof(Image));
            ((RectTransform)root.transform).sizeDelta = new Vector2(ShopItemCell.Size, ShopItemCell.Size);
            var frame = root.GetComponent<Image>();
            Theme.SetSprite(frame, V3Sprite("o_mon", Vector4.zero));
            frame.raycastTarget = false;
            var icon = Img("hinh", root.transform, null, Color.white);
            Anchors(icon.rectTransform, new Vector2(0.1f, 0.35f), new Vector2(0.9f, 0.94f));
            icon.preserveAspect = true;
            var heroBox = Anchors(Rt("khung_tuong", root.transform, typeof(RectMask2D)), new Vector2(0.06f, 0.33f), new Vector2(0.94f, 0.96f));
            // số trắng to trong vạch tối (bản đầu chữ tự co còn ~13 px, không đọc được)
            var (titleTpl, _) = Templates();
            var count = Text(titleTpl, root.transform, "so", 38, TextAlignmentOptions.Center, Color.white);
            Anchors(count.rectTransform, new Vector2(0.02f, 0.0f), new Vector2(0.98f, 0.33f));
            count.textWrappingMode = TextWrappingModes.NoWrap;
            count.overflowMode = TextOverflowModes.Overflow;
            count.transform.SetAsLastSibling();
            root.AddComponent<ShopItemCell>().Setup(frame, icon, count, heroBox);
            return Save<ShopItemCell>(root, ItemCellPath);
        }

        // ---------- ô ----------

        static ShopTile BuildTile()
        {
            var (titleTpl, hintTpl) = Templates();
            var root = NewRoot("OCuaHang", typeof(CanvasRenderer), typeof(Image));
            ((RectTransform)root.transform).sizeDelta = new Vector2(276, 420);
            var bg = root.GetComponent<Image>();
            Theme.SetSprite(bg, V3Sprite("o_nen", TileBorder));
            bg.type = Image.Type.Sliced;
            bg.color = ShopHue.Sky.fill;
            bg.raycastTarget = false;
            var rays = Sliced("tia", root.transform, V3Sprite("o_tia", TileBorder), Color.white);

            var art = Img("hinh", root.transform, null, Color.white);
            Anchors(art.rectTransform, new Vector2(0.08f, 0.34f), new Vector2(0.92f, 0.83f));
            art.preserveAspect = true;
            var stackRt = Anchors(Rt("chong", root.transform), new Vector2(0.06f, 0.34f), new Vector2(0.94f, 0.83f));
            var stack = new Image[3];
            Vector2[,] box = { { new Vector2(0, 0.02f), new Vector2(0.6f, 0.8f) }, { new Vector2(0.4f, 0.02f), new Vector2(1, 0.8f) }, { new Vector2(0.18f, 0.16f), new Vector2(0.82f, 1) } };
            for (int i = 0; i < 3; i++)
            {
                stack[i] = Img("qua_" + (i + 1), stackRt, null, Color.white);
                Anchors(stack[i].rectTransform, box[i, 0], box[i, 1]);
                stack[i].preserveAspect = true;
            }
            var count = Text(titleTpl, root.transform, "so", 46, TextAlignmentOptions.BottomRight, Color.white);
            Anchors(count.rectTransform, new Vector2(0.45f, 0.33f), new Vector2(0.95f, 0.48f));
            Ink(count, 0.3f);
            var title = Text(titleTpl, root.transform, "ten", 34, TextAlignmentOptions.Center, Color.white);
            Anchors(title.rectTransform, new Vector2(0.05f, 0.83f), new Vector2(0.95f, 0.95f));
            title.enableAutoSizing = true;
            title.fontSizeMin = 20;
            title.fontSizeMax = 34;
            title.textWrappingMode = TextWrappingModes.NoWrap;
            Ink(title, 0.28f);
            var sub = Text(hintTpl, root.transform, "phu", 22, TextAlignmentOptions.Center, Color.white);
            Anchors(sub.rectTransform, new Vector2(0.04f, 0.245f), new Vector2(0.96f, 0.33f));
            sub.enableAutoSizing = true;
            sub.fontSizeMin = 15;
            sub.fontSizeMax = 22;
            Ink(sub, 0.24f);

            // nút giá trong dải tối đáy
            var buy = PriceButton(root.transform, "nut_mua", 0, 80, 34);
            var br = buy.Rect;
            br.anchorMin = new Vector2(0.07f, 0);
            br.anchorMax = new Vector2(0.93f, 0);
            br.pivot = new Vector2(0.5f, 0);
            br.anchoredPosition = new Vector2(0, 11);
            br.sizeDelta = new Vector2(0, 80);

            // nhãn góc trái (Lần đầu ×2, Bán chạy): chìa ra mép trên
            var ribbon = Img("nhan", root.transform, V3Sprite("vien", PillBorder), Theme.Red);
            ribbon.type = Image.Type.Sliced;
            ribbon.rectTransform.Place(new Vector2(0, 1), new Vector2(-8, 18), new Vector2(176, 46), new Vector2(0, 1));
            ribbon.rectTransform.localEulerAngles = new Vector3(0, 0, 6);
            var ribbonText = Text(hintTpl, ribbon.transform, "chu", 22, TextAlignmentOptions.Center, Color.white);
            ribbonText.rectTransform.Stretch(8, 2, 8, 2);
            ribbonText.enableAutoSizing = true;
            ribbonText.fontSizeMin = 14;
            ribbonText.fontSizeMax = 22;
            ribbonText.fontStyle = FontStyles.Bold;

            // nhãn giá trị "×N" góc phải
            var value = Img("gia_tri", root.transform, V3Sprite("nhan_gia_tri", new Vector4(34, 10, 14, 10)), Color.white);
            value.type = Image.Type.Sliced;
            value.rectTransform.Place(new Vector2(1, 1), new Vector2(10, 18), new Vector2(124, 52), new Vector2(1, 1));
            var valueText = Text(titleTpl, value.transform, "chu", 32, TextAlignmentOptions.Center, Color.white);
            valueText.rectTransform.Stretch(26, 2, 8, 4);
            valueText.enableAutoSizing = true;
            valueText.fontSizeMin = 18;
            valueText.fontSizeMax = 32;
            Ink(valueText, 0.25f);

            var done = Text(titleTpl, root.transform, "da_mua", 30, TextAlignmentOptions.Center, DoneGreen);
            Anchors(done.rectTransform, new Vector2(0.04f, 0.01f), new Vector2(0.96f, 0.22f));
            done.enableAutoSizing = true;
            done.fontSizeMin = 18;
            done.fontSizeMax = 30;
            Ink(done, 0.25f);

            var dot = Img("cham_do", root.transform, V3Sprite("cham_do", Vector4.zero), Color.white);
            dot.rectTransform.Place(new Vector2(1, 1), new Vector2(-10, -10), new Vector2(40, 40), new Vector2(0.5f, 0.5f));

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (!gr.transform.IsChildOf(buy.transform)) gr.raycastTarget = false;
            buy.GetComponent<Image>().raycastTarget = true;
            root.AddComponent<ShopTile>().Setup(new ShopTile.Parts
            {
                bg = bg, rays = rays, art = art, ribbon = ribbon, dot = dot, valueBg = value, stack = stack, title = title, sub = sub, count = count,
                ribbonText = ribbonText, done = done, valueText = valueText, buy = buy,
            });
            return Save<ShopTile>(root, TilePath);
        }

        // ---------- thẻ ngang ----------

        static ShopCard BuildCard(ShopItemCell cell)
        {
            var (titleTpl, hintTpl) = Templates();
            const float W = ShopPage.ContentW, H = ShopCard.Tall;
            var root = NewRoot("TheCuaHang", typeof(CanvasRenderer), typeof(Image), typeof(LayoutElement));
            ((RectTransform)root.transform).sizeDelta = new Vector2(W, H);
            Le(root.GetComponent<RectTransform>(), H);
            var bg = root.GetComponent<Image>();
            Theme.SetSprite(bg, V3Sprite("the_nen", CardBorder));
            bg.type = Image.Type.Sliced;
            bg.color = ShopHue.Gold.fill;
            bg.raycastTarget = false;
            var panel = Sliced("mang_phai", root.transform, V3Sprite("the_phai", CardBorder), ShopHue.Gold.panel);
            var rays = Sliced("sao_no", root.transform, V3Sprite("the_tia", CardBorder), ShopHue.Gold.rays);

            // hình gói / mặt tướng bên trái, đè một phần dải tên như thẻ mẫu
            var art = Img("hinh", root.transform, null, Color.white);
            art.rectTransform.anchorMin = new Vector2(0, 0);
            art.rectTransform.anchorMax = new Vector2(0, 1);
            art.rectTransform.pivot = new Vector2(0, 0.5f);
            art.rectTransform.offsetMin = new Vector2(20, 66);
            art.rectTransform.offsetMax = new Vector2(20 + 340, -14);
            art.preserveAspect = true;
            var hero = Img("mat_tuong", root.transform, null, Color.white);
            hero.rectTransform.anchorMin = art.rectTransform.anchorMin;
            hero.rectTransform.anchorMax = art.rectTransform.anchorMax;
            hero.rectTransform.pivot = art.rectTransform.pivot;
            hero.rectTransform.offsetMin = art.rectTransform.offsetMin;
            hero.rectTransform.offsetMax = art.rectTransform.offsetMax;
            hero.preserveAspect = true;

            // tên trong dải tối đáy
            var title = Text(titleTpl, root.transform, "ten", 44, TextAlignmentOptions.MidlineLeft, Color.white);
            title.rectTransform.anchorMin = new Vector2(0, 0);
            title.rectTransform.anchorMax = new Vector2(1, 0);
            title.rectTransform.pivot = new Vector2(0, 0);
            title.rectTransform.offsetMin = new Vector2(30, 12);
            title.rectTransform.offsetMax = new Vector2(-340, 86);
            title.enableAutoSizing = true;
            title.fontSizeMin = 26;
            title.fontSizeMax = 44;
            title.textWrappingMode = TextWrappingModes.NoWrap;
            Ink(title, 0.28f);

            // mô tả ngắn bên phải trên hàng món
            var desc = Text(hintTpl, root.transform, "mo_ta", 27, TextAlignmentOptions.TopRight, Color.white);
            desc.rectTransform.anchorMin = new Vector2(0, 1);
            desc.rectTransform.anchorMax = new Vector2(1, 1);
            desc.rectTransform.pivot = new Vector2(1, 1);
            desc.rectTransform.offsetMin = new Vector2(380, -128);
            desc.rectTransform.offsetMax = new Vector2(-26, -70);
            desc.enableAutoSizing = true;
            desc.fontSizeMin = 18;
            desc.fontSizeMax = 27;
            Ink(desc, 0.24f);

            // hàng ô món canh phải
            var items = Rt("mon", root.transform, typeof(GridLayoutGroup));
            items.anchorMin = items.anchorMax = items.pivot = new Vector2(1, 1);
            items.anchoredPosition = new Vector2(-26, -132);
            items.sizeDelta = new Vector2(5 * ShopItemCell.Size + 4 * 8, ShopItemCell.Size);
            items.localScale = Vector3.one * ShopCard.ItemScale;
            var g = items.GetComponent<GridLayoutGroup>();
            g.cellSize = new Vector2(ShopItemCell.Size, ShopItemCell.Size);
            g.spacing = new Vector2(8, 8);
            g.constraint = GridLayoutGroup.Constraint.FixedRowCount;
            g.constraintCount = 1;
            g.childAlignment = TextAnchor.UpperRight; // canh phải, giữ thứ tự món (bi trước)

            // đồng hồ góc trên trái
            var pill = Img("dong_ho", root.transform, V3Sprite("vien", PillBorder), new Color(Navy.r, Navy.g, Navy.b, 0.88f));
            pill.type = Image.Type.Sliced;
            pill.rectTransform.Place(new Vector2(0, 1), new Vector2(16, -16), new Vector2(214, 50), new Vector2(0, 1));
            var timer = Text(hintTpl, pill.transform, "chu", 26, TextAlignmentOptions.Center, Color.white);
            timer.rectTransform.Stretch(8, 2, 8, 2);
            timer.fontStyle = FontStyles.Bold;

            // nhãn đỏ "Giá trị ×N": chìa ra mép trên, sát mép phải
            var value = Img("gia_tri", root.transform, V3Sprite("nhan_gia_tri", new Vector4(34, 10, 14, 10)), Color.white);
            value.type = Image.Type.Sliced;
            value.rectTransform.Place(new Vector2(1, 1), new Vector2(8, 14), new Vector2(320, 74), new Vector2(1, 1));
            var valueText = Text(titleTpl, value.transform, "chu", 36, TextAlignmentOptions.Center, Color.white);
            valueText.rectTransform.Stretch(38, 4, 14, 6);
            valueText.enableAutoSizing = true;
            valueText.fontSizeMin = 20;
            valueText.fontSizeMax = 36;
            valueText.textWrappingMode = TextWrappingModes.NoWrap;
            Ink(valueText, 0.25f);

            var buy = PriceButton(root.transform, "nut_mua", 300, 104, 46);
            var br = buy.Rect;
            br.anchorMin = br.anchorMax = br.pivot = new Vector2(1, 0);
            br.anchoredPosition = new Vector2(-20, 16);
            var extra = PriceButton(root.transform, "nut_phu", 230, 88, 32);
            var er = extra.Rect;
            er.anchorMin = er.anchorMax = er.pivot = new Vector2(1, 0);
            er.anchoredPosition = new Vector2(-20 - 300 - 14, 24);

            var note = Text(hintTpl, root.transform, "ghi_chu", 24, TextAlignmentOptions.MidlineRight, Color.white);
            note.rectTransform.Place(new Vector2(1, 0), new Vector2(-26, 14), new Vector2(470, 84), new Vector2(1, 0));
            note.enableAutoSizing = true;
            note.fontSizeMin = 16;
            note.fontSizeMax = 24;
            Ink(note, 0.24f);
            var done = Text(titleTpl, root.transform, "da_mua", 40, TextAlignmentOptions.Center, DoneGreen);
            done.rectTransform.Place(new Vector2(1, 0), new Vector2(-30, 18), new Vector2(330, 80), new Vector2(1, 0));
            done.rectTransform.localEulerAngles = new Vector3(0, 0, 4);
            done.enableAutoSizing = true;
            done.fontSizeMin = 22;
            done.fontSizeMax = 40;
            Ink(done, 0.25f);

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (!gr.transform.IsChildOf(buy.transform) && !gr.transform.IsChildOf(extra.transform)) gr.raycastTarget = false;
            buy.GetComponent<Image>().raycastTarget = extra.GetComponent<Image>().raycastTarget = true;
            root.AddComponent<ShopCard>().Setup(new ShopCard.Parts
            {
                bg = bg, panel = panel, rays = rays, art = art, heroArt = hero, valueBg = value, title = title, desc = desc, timer = timer, done = done,
                note = note, valueText = valueText, items = items, buy = buy, extra = extra,
            }, cell, pill.gameObject);
            return Save<ShopCard>(root, CardPath);
        }

        // ---------- màn cửa hàng ----------

        // hình nút cột mục (theo ShopPage.Sections): khinh khí cầu, hộp quà, trứng Sử Thi, thùng bi, sổ phiêu lưu
        static readonly string[] NavArt = { "v2/goi2_khoi_hanh_3", "v2/goi2_nhap_mon", "v2/trung2_3", "v2/goi2_bi_4", "v2/goi2_the_phieu_luu" };
        public const float NavItemH = 214;

        static void BuildPage(ShopSection section, ShopGrid grid, ShopTile tile, ShopCard card)
        {
            var kit = Kit;
            var (titleTpl, _) = Templates();
            var (outlined, plain) = KitLabelMats();
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "CuaHangLon";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(1080, false, true);
                var sheet = view.Sheet;
                // tờ giấy trải KÍN màn (người dùng 2026-11-24: "shop nên full màn"): tràn quá mép màn Bleed điểm, bỏ băng keo; lớp hộp thoại phủ
                // cả tai thỏ nên nội dung (noi_dung) thu lại đúng bằng màn, chữ và nút nằm trong khung an_toan (SafeArea). Bản 3: nền tối phủ
                // kín tờ giấy (2026-11-27: "nền màu tối chút, các gói IAP màu tươi nổi")
                const float Bleed = 30;
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                sheet.anchorMin = Vector2.zero;
                sheet.anchorMax = Vector2.one;
                sheet.pivot = new Vector2(0.5f, 0.5f);
                sheet.offsetMin = new Vector2(-Bleed, -Bleed);
                sheet.offsetMax = new Vector2(Bleed, Bleed);
                view.SetFlat(true);
                var tape = sheet.Find("bang_keo");
                if (tape) tape.gameObject.SetActive(false);

                var page = Rt("noi_dung", sheet);
                page.Stretch(Bleed, Bleed, Bleed, Bleed);
                page.SetAsLastSibling();
                // nền: tối cả màn, caro chàm ở vùng trang, cột mục chàm thẫm bên trái (kéo hết chiều cao, dưới thanh trên)
                Sliced("nen_toi", page, null, TopBg).type = Image.Type.Simple;
                var pattern = Img("nen_caro", page, V3Sprite("nen_trang", Vector4.zero), Color.white);
                pattern.type = Image.Type.Tiled;
                pattern.rectTransform.Stretch(ShopPage.SideW, 0, 0, 0);
                // cột trái: ảnh vẽ tay lát dọc (cot_trai 190 x 768: sao, lấp lánh, quái nhỏ; vien_cot: nét mực dọc rộng 8; assets-31 vẽ,
                // người dùng 2026-11-27: "cột bên trái màu trơn nhìn đơn điệu") nếu có, không thì màu trơn
                var sideArt = System.IO.File.Exists(V3 + "cot_trai.png") ? V3Sprite("cot_trai", Vector4.zero) : null;
                var side = Img("nen_cot", page, sideArt, sideArt ? Color.white : SideBg);
                if (sideArt) side.type = Image.Type.Tiled;
                side.rectTransform.anchorMin = new Vector2(0, 0);
                side.rectTransform.anchorMax = new Vector2(0, 1);
                side.rectTransform.pivot = new Vector2(0, 0.5f);
                side.rectTransform.offsetMin = Vector2.zero;
                side.rectTransform.offsetMax = new Vector2(ShopPage.SideW, 0);
                var edgeArt = System.IO.File.Exists(V3 + "vien_cot.png") ? V3Sprite("vien_cot", Vector4.zero) : null;
                var edge = Img("vien_cot", side.transform, edgeArt, edgeArt ? Color.white : Navy);
                if (edgeArt) edge.type = Image.Type.Tiled;
                edge.rectTransform.anchorMin = new Vector2(1, 0);
                edge.rectTransform.anchorMax = new Vector2(1, 1);
                edge.rectTransform.pivot = new Vector2(1, 0.5f);
                edge.rectTransform.offsetMin = new Vector2(edgeArt ? -8 : -5, 0);
                edge.rectTransform.offsetMax = Vector2.zero;

                var body = Rt("an_toan", page, typeof(SafeArea));
                body.Stretch();
                // thanh trên tối, kéo lên che vùng tai thỏ
                var top = Img("thanh_tren", body, null, TopBg);
                top.rectTransform.anchorMin = new Vector2(0, 1);
                top.rectTransform.anchorMax = new Vector2(1, 1);
                top.rectTransform.pivot = new Vector2(0.5f, 1);
                top.rectTransform.offsetMin = new Vector2(0, -HeaderH);
                top.rectTransform.offsetMax = new Vector2(0, 400);
                // nút đóng (con của tờ giấy, ModalService gắn): góc phải thanh trên; ShopPage dời xuống theo tai thỏ lúc mở
                var cr = (RectTransform)view.Close.transform;
                cr.anchorMin = cr.anchorMax = new Vector2(1, 1);
                cr.pivot = new Vector2(0.5f, 0.5f);
                cr.anchoredPosition = new Vector2(-Bleed - 64, -Bleed - HeaderH / 2);
                // số bi góc trái, tiêu đề vàng giữa
                var chip = Img("so_bi", body, V3Sprite("vien", PillBorder), SideBg);
                chip.type = Image.Type.Sliced;
                chip.rectTransform.Place(new Vector2(0, 1), new Vector2(20, -22), new Vector2(250, 74), new Vector2(0, 1));
                var ball = Img("icon", chip.transform, Icon("ball"), Color.white);
                ball.preserveAspect = true;
                ball.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(4, 0), new Vector2(70, 70), new Vector2(0, 0.5f));
                var balls = Text(titleTpl, chip.transform, "so", 40, TextAlignmentOptions.MidlineRight, Color.white);
                balls.rectTransform.Stretch(80, 4, 22, 4);
                Ink(balls, 0.22f);
                var title = Text(titleTpl, body, "tieu_de", 56, TextAlignmentOptions.Center, Gold);
                title.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(40, -14), new Vector2(460, HeaderH - 24), new Vector2(0.5f, 1));
                title.enableAutoSizing = true;
                title.fontSizeMin = 32;
                title.fontSizeMax = 56;
                title.textWrappingMode = TextWrappingModes.NoWrap;
                Ink(title, 0.3f);

                // cột mục: hình gói + tên; nền nút là ô chọn tím → lam, chỉ hiện ở mục đang xem (ShopPage.LateUpdate)
                var col = Rt("cot_muc", body, typeof(VerticalLayoutGroup));
                col.anchorMin = new Vector2(0, 0);
                col.anchorMax = new Vector2(0, 1);
                col.pivot = new Vector2(0, 1);
                col.offsetMin = new Vector2(0, 0);
                col.offsetMax = new Vector2(ShopPage.SideW - 5, -HeaderH - 12);
                var vlg = col.GetComponent<VerticalLayoutGroup>();
                vlg.spacing = 8;
                vlg.childAlignment = TextAnchor.UpperCenter;
                vlg.childControlWidth = vlg.childControlHeight = false;
                vlg.childForceExpandWidth = vlg.childForceExpandHeight = false;
                var pick = V3Sprite("muc_chon", Round30);
                var nav = new SketchButton[ShopPage.Sections.Length];
                var dots = new GameObject[nav.Length];
                for (int i = 0; i < nav.Length; i++)
                {
                    var bgi = Img("muc_" + ShopPage.Sections[i], col, pick, i == 0 ? Color.white : new Color(1, 1, 1, 0));
                    bgi.type = Image.Type.Sliced;
                    bgi.raycastTarget = true;
                    bgi.rectTransform.sizeDelta = new Vector2(ShopPage.SideW - 16, NavItemH);
                    var icon = Img("hinh", bgi.transform, Art("Assets/03 Art/Shop/" + NavArt[i] + ".png"), Color.white);
                    icon.preserveAspect = true;
                    icon.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -10), new Vector2(150, 134), new Vector2(0.5f, 1));
                    var label = KitLabel(bgi.transform, 32);
                    label.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 12), new Vector2(ShopPage.SideW - 20, 60), new Vector2(0.5f, 0));
                    var b = bgi.gameObject.AddComponent<SketchButton>();
                    b.Setup(bgi, label, false, pick, pick, outlined, plain);
                    b.SetRole(BtnColor.Green); // chữ trắng viền mực
                    b.SetColor(i == 0 ? Color.white : new Color(1, 1, 1, 0));
                    label.text = ShopPage.NavNames[i];
                    var dot = Img("cham_do", bgi.transform, V3Sprite("cham_do", Vector4.zero), Color.white);
                    dot.rectTransform.Place(new Vector2(1, 1), new Vector2(-16, -16), new Vector2(40, 40), new Vector2(0.5f, 0.5f));
                    dot.gameObject.SetActive(false);
                    nav[i] = b;
                    dots[i] = dot.gameObject;
                }

                // trang cuộn bên phải cột mục
                var scrollGo = Rt("cuon", body, typeof(CanvasRenderer), typeof(Image), typeof(ScrollRect)).gameObject;
                var srt = (RectTransform)scrollGo.transform;
                srt.Stretch(ShopPage.SideW, HeaderH, 0, 0);
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
                vl.spacing = 24;
                // trái 14 + 858 + phải 18 = 1080 - cột 190; trên 22 cho nhãn giá trị chìa ra mép thẻ đầu
                vl.padding = new RectOffset(14, 18, 22, 60);
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
                    title = title, balls = balls, nav = nav, navDots = dots, scroll = scroll, content = content, safe = body,
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
        // ---------- màn quà hôm nay ----------

        // dựng riêng màn quà hôm nay (không dựng lại các prefab khác của cửa hàng)
        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: chỉ màn quà ngày (QuaNgay)", priority = 71)]
        static void BuildGiftOnly()
        {
            BuildGift();
            AssetDatabase.SaveAssets();
            Debug.Log("[Cửa hàng] Đã dựng " + GiftPath);
        }

        static void BuildGift()
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var add = AssetDatabase.LoadAssetAtPath<Material>("Assets/Resources/UIAdditive.mat");
            var root = NewRoot("QuaNgay", typeof(Canvas), typeof(GraphicRaycaster), typeof(CanvasGroup));
            var rt = (RectTransform)root.transform;
            rt.sizeDelta = new Vector2(1080, 1920);
            var cv = root.GetComponent<Canvas>();
            cv.overrideSorting = true;
            cv.sortingOrder = 450;

            // nền đen (người dùng: "nền đen thôi"); nhận chạm để chặn màn dưới
            var dim = Img("nen_den", root.transform, null, new Color(0, 0, 0, 0));
            dim.rectTransform.Stretch();
            dim.raycastTarget = true;

            var gold = new Color(1f, 0.8f, 0.4f, 0);
            var cream = new Color(1f, 0.95f, 0.8f, 0);
            var center = new Vector2(0, 150);
            Image Glow(string n, string file, Vector2 size, Color c)
            {
                var img = Img(n, root.transform, Art($"Assets/03 Art/Pachinko/{file}.png"), c);
                img.rectTransform.Place(new Vector2(0.5f, 0.5f), center, size);
                if (add) img.material = add;
                return img;
            }
            var rays = Glow("tia", "pk_g_tia", new Vector2(1250, 1250), gold);
            var rays2 = Glow("tia_2", "pk_g_tia", new Vector2(820, 820), cream);
            rays2.rectTransform.localEulerAngles = new Vector3(0, 0, 15);
            var halo = Glow("quang", "pk_g_quang", new Vector2(860, 860), gold);
            var core = Glow("loi_quang", "pk_g_quang", new Vector2(460, 460), cream);
            var ring = Glow("vong", "pk_g_vong", new Vector2(380, 380), cream);
            var flare = Glow("loe", "pk_g_loe", new Vector2(1200, 300), new Color(1f, 0.92f, 0.7f, 0));

            // hình quà (con: ảnh giữ tỉ lệ, dấu ×2 góc phải trên)
            var item = Rt("qua", root.transform);
            item.Place(new Vector2(0.5f, 0.5f), center, new Vector2(470, 470));
            var art = Img("hinh", item, null, Color.white);
            art.rectTransform.Stretch();
            art.preserveAspect = true;
            var stamp = Ui.Spawn(kit.stamp, item);
            stamp.name = "dau_x2";
            var srt = (RectTransform)stamp.transform;
            srt.anchorMin = srt.anchorMax = new Vector2(1, 1);
            srt.anchoredPosition = new Vector2(-40, -50);
            srt.localEulerAngles = new Vector3(0, 0, -12);
            stamp.gameObject.SetActive(false);

            var count = Text(titleTpl, root.transform, "so", 104, TextAlignmentOptions.Center, Color.white);
            count.rectTransform.Place(new Vector2(0.5f, 0.5f), center + new Vector2(0, -320), new Vector2(700, 130));
            Outline(count, 0.24f);
            var itemName = Text(hintTpl, root.transform, "ten_mon", 40, TextAlignmentOptions.Center, Theme.Paper);
            itemName.rectTransform.Place(new Vector2(0.5f, 0.5f), center + new Vector2(0, -405), new Vector2(800, 60));
            var extrasTitle = Text(hintTpl, root.transform, "kem_tieu_de", 32, TextAlignmentOptions.Center, Theme.Paper);
            extrasTitle.rectTransform.Place(new Vector2(0.5f, 0.5f), center + new Vector2(0, -480), new Vector2(800, 50));
            var extras = Rt("kem", root.transform, typeof(HorizontalLayoutGroup));
            extras.Place(new Vector2(0.5f, 0.5f), center + new Vector2(0, -620), new Vector2(5 * RewardTile.W + 4 * 18, RewardTile.H));
            var hl = extras.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = 18;
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;

            // sao vẽ tay (phẳng, không cộng sáng) bắn ra / lấp lánh quanh quà
            var star = Art("Assets/03 Art/Pachinko/fx2_sao4.png");
            var stars = new Image[10];
            for (int i = 0; i < stars.Length; i++)
            {
                stars[i] = Img("sao_" + i, root.transform, star, Color.white);
                stars[i].rectTransform.Place(new Vector2(0.5f, 0.5f), center, new Vector2(70, 70));
                stars[i].gameObject.SetActive(false);
            }

            var flash = Img("chop", root.transform, null, new Color(1, 1, 1, 0));
            flash.rectTransform.Stretch();

            var title = Text(titleTpl, root.transform, "tieu_de", 86, TextAlignmentOptions.Center, Theme.Yellow);
            title.rectTransform.Place(new Vector2(0.5f, 0.5f), center + new Vector2(0, 480), new Vector2(980, 120));
            Outline(title, 0.28f);

            // nút ×2 to (bọc trong khung thở, viền sáng bám mép nút) neo đáy; nút thường nhỏ bên dưới, nhóm mờ dần.
            // Viền sáng: Image không ảnh, cỡ và số shader do DailyGiftView.FitGlow đặt theo cỡ nút lúc chạy (người dùng 2026-11-27 bỏ quầng to)
            var wrap = Rt("nut_x2_khung", root.transform);
            wrap.Place(new Vector2(0.5f, 0), new Vector2(0, 440), new Vector2(640, 160));
            var btnGlow = Img("vien_sang_nut", wrap, null, gold);
            btnGlow.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(660, 200));
            var edgeGlow = AssetDatabase.LoadAssetAtPath<Material>("Assets/Resources/UIEdgeGlow.mat");
            if (edgeGlow) btnGlow.material = edgeGlow;
            var x2 = Ui.Spawn(kit.buttonBig, wrap);
            x2.name = "nut_x2";
            x2.Rect.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(600, Mathf.Max(x2.Rect.sizeDelta.y, 140)));
            x2.SetRole(BtnColor.Orange);
            x2.SetText("Nhận ×2");
            var tv = Img("tv", x2.transform, Icon("tv"), Color.white);
            tv.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(86, 4), new Vector2(84, 84));
            var lr = x2.Label.rectTransform;
            lr.offsetMin = new Vector2(lr.offsetMin.x + 120, lr.offsetMin.y);

            var plainGroup = Rt("nut_thuong_nhom", root.transform, typeof(CanvasGroup));
            plainGroup.Place(new Vector2(0.5f, 0), new Vector2(0, 250), new Vector2(420, 120));
            var plain = Ui.Spawn(kit.buttonSmall, plainGroup);
            plain.name = "nut_thuong";
            plain.Rect.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(360, plain.Rect.sizeDelta.y));
            plain.SetRole(BtnColor.Paper);
            plain.SetText("Nhận thường");

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (gr != dim && !gr.transform.IsChildOf(x2.transform) && !gr.transform.IsChildOf(plain.transform)) gr.raycastTarget = false;
            tv.raycastTarget = false;
            root.AddComponent<DailyGiftView>().Setup(new DailyGiftView.Parts
            {
                dim = dim, rays = rays, rays2 = rays2, halo = halo, haloCore = core, flare = flare, ring = ring, flash = flash, art = art, btnGlow = btnGlow,
                item = item, x2Wrap = wrap, extras = extras, stars = stars, title = title, count = count, itemName = itemName, extrasTitle = extrasTitle,
                stamp = stamp, x2 = x2, plain = plain, plainGroup = plainGroup.GetComponent<CanvasGroup>(),
            }, TilePrefab);
            var view = Save<DailyGiftView>(root, GiftPath);
            kit.dailyGift = view;
            EditorUtility.SetDirty(kit);
        }

        // ---------- màn mở khoá tướng ----------

        // dựng riêng màn mở khoá (không dựng lại các prefab khác của cửa hàng)
        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: chỉ màn mở khoá tướng (MoKhoaTuong)", priority = 71)]
        static void BuildUnlockOnly()
        {
            BuildUnlock();
            AssetDatabase.SaveAssets();
            Debug.Log("[Cửa hàng] Đã dựng " + UnlockPath);
        }

        // Temp/unlock_build.flag: biên dịch xong và không Play thì dựng màn mở khoá một lần rồi xoá cờ (Unity dùng chung nhiều phiên)
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void HookUnlockFlag() => EditorApplication.update += PollUnlockFlag;

        static void PollUnlockFlag()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            var flag = System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../Temp/unlock_build.flag"));
            if (!System.IO.File.Exists(flag)) return;
            System.IO.File.Delete(flag);
            BuildUnlockOnly();
        }

        // Màn mở khoá tướng kiểu bút chì vẽ lên trang sổ (người dùng 2026-11-24, thay màn cột sáng kiểu Brawl Stars): xem HeroUnlockView
        const string PencilMat = "Assets/03 Art/Shaders/PencilDraw.mat";

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

            // nền màu bậc: gradient tròn (ảnh xám, nhân màu bậc lúc chạy), lộ quanh mép trang sổ
            var rarityBg = Img("nen_bac", root.transform, Art("Assets/03 Art/Shop/nen_gradient_tron.png"), Theme.Blue);
            rarityBg.rectTransform.Stretch();

            // trang sổ phép: giấy viền mực, dòng kẻ, lề đỏ; tướng và khối chữ nằm trên trang (trượt cùng trang)
            var page = Img("trang_so", root.transform, Sketch.Panel, Theme.Paper);
            page.type = Image.Type.Sliced;
            page.rectTransform.Stretch(34, 120, 34, 110);
            var lines = Img("dong_ke", page.transform, Sketch.LinedPaper, Theme.Paper); // ảnh dòng kẻ nền trắng: nhân màu giấy
            lines.type = Image.Type.Tiled;
            lines.rectTransform.Stretch(24, 170, 24, 36);
            var margin = Img("le_do", page.transform, null, new Color(Theme.Red.r, Theme.Red.g, Theme.Red.b, 0.4f));
            var mr = margin.rectTransform;
            mr.anchorMin = Vector2.zero;
            mr.anchorMax = new Vector2(0, 1);
            mr.offsetMin = new Vector2(104, 36);
            mr.offsetMax = new Vector2(108, -40);

            var ribbon = Img("ruy_bang", page.transform, Art(P + "pk_ruy_bang.png"), Color.white);
            ribbon.preserveAspect = true;
            ribbon.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, 46), new Vector2(640, 136), new Vector2(0.5f, 1));
            var ribbonText = Text(titleTpl, ribbon.transform, "chu", 44, TextAlignmentOptions.Center, Color.white);
            ribbonText.rectTransform.Stretch(90, 22, 90, 40);
            Outline(ribbonText, 0.22f);

            // chỗ tướng: gốc ở chân; khung hình (rig / chân dung dựng lúc chạy), tranh chì, nét viền (dời vào khung hình lúc chạy)
            var hero = Rt("tuong", page.transform);
            hero.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -105), new Vector2(800, 1000), new Vector2(0.5f, 0));
            var art = Rt("hinh", hero);
            art.Place(new Vector2(0.5f, 0), Vector2.zero, new Vector2(800, 1000), new Vector2(0.5f, 0));
            var mat = AssetDatabase.LoadAssetAtPath<Material>(PencilMat);
            if (!mat)
            {
                mat = new Material(Shader.Find("PokiClash/UIPencilDraw"));
                AssetDatabase.CreateAsset(mat, PencilMat);
            }
            mat.SetFloat("_Rows", HeroUnlockView.Rows);
            EditorUtility.SetDirty(mat);
            var drawing = Rt("tranh_chi", hero, typeof(CanvasRenderer), typeof(RawImage)).GetComponent<RawImage>();
            drawing.material = mat;
            drawing.raycastTarget = false;
            drawing.rectTransform.Stretch();
            drawing.gameObject.SetActive(false);
            var ink = Rt("net_vien", hero, typeof(CanvasRenderer), typeof(InkStroke)).GetComponent<InkStroke>();
            ink.color = new Color(0.24f, 0.2f, 0.17f, 1);
            ink.width = 6;
            ink.raycastTarget = false;
            ink.rectTransform.Stretch();
            ink.gameObject.SetActive(false);

            // khối chữ dưới tướng: tên; viên bậc + biểu tượng hệ, "Hệ …"; danh hiệu; 3 dòng chỉ số; nút
            var info = Rt("chu_tuong", page.transform);
            info.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -535), new Vector2(920, 560));
            var heroName = Text(titleTpl, info, "ten", 66, TextAlignmentOptions.Center, Theme.Ink);
            heroName.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 232), new Vector2(820, 86));
            heroName.enableAutoSizing = true;
            heroName.fontSizeMin = 36;
            heroName.fontSizeMax = 66;
            heroName.textWrappingMode = TextWrappingModes.NoWrap;
            var pill = Img("vien_bac", info, Sketch.Pill, Theme.Orange);
            pill.type = Image.Type.Sliced;
            pill.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(-140, 152), new Vector2(270, 56));
            var rarity = Text(titleTpl, pill.transform, "bac", 32, TextAlignmentOptions.Center, Color.white);
            rarity.rectTransform.Stretch(10, 2, 10, 2);
            var badgeIcon = Img("icon_he", info, null, Color.white);
            badgeIcon.preserveAspect = true;
            badgeIcon.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(40, 152), new Vector2(56, 56));
            var elem = Text(hintTpl, info, "he", 34, TextAlignmentOptions.MidlineLeft, Theme.Ink2);
            elem.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(78, 152), new Vector2(240, 56), new Vector2(0, 0.5f));
            elem.textWrappingMode = TextWrappingModes.NoWrap;
            var title = Text(hintTpl, info, "danh_hieu", 30, TextAlignmentOptions.Center, Theme.Ink2);
            title.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 88), new Vector2(860, 48));
            title.fontStyle = FontStyles.Italic;
            title.enableAutoSizing = true;
            title.fontSizeMin = 20;
            title.fontSizeMax = 30;
            // 3 dòng chỉ số như màn chọn tướng khởi đầu: chữ trái, 5 nấc bình hành nền trắng, số phải
            var labels = StatPipsBuild.Labels;
            var stats = new StatPips[labels.Length];
            for (int k = 0; k < labels.Length; k++)
            {
                var row = Rt("chi_so_" + k, info);
                row.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 10 - 60 * k), new Vector2(680, 52));
                var lab = Text(hintTpl, row, "chu", 34, TextAlignmentOptions.MidlineLeft, Theme.Ink2);
                lab.rectTransform.Place(new Vector2(0, 0.5f), Vector2.zero, new Vector2(140, 52), new Vector2(0, 0.5f));
                lab.textWrappingMode = TextWrappingModes.NoWrap;
                lab.text = labels[k];
                var val = Text(titleTpl, row, "so", 34, TextAlignmentOptions.MidlineRight, Theme.Ink);
                val.rectTransform.Place(new Vector2(1, 0.5f), Vector2.zero, new Vector2(160, 52), new Vector2(1, 0.5f));
                val.textWrappingMode = TextWrappingModes.NoWrap;
                stats[k] = StatPipsBuild.Add(row, k, 140, 34, 74, lab, val);
            }
            var view = Ui.Spawn(kit.buttonNormal, info);
            view.name = "nut_xem_tuong";
            view.Rect.Place(new Vector2(0.5f, 0.5f), new Vector2(-220, -215), new Vector2(360, view.Rect.sizeDelta.y));
            view.SetRole(BtnColor.Paper);
            view.SetText("Xem tướng");
            var next = Ui.Spawn(kit.buttonNormal, info);
            next.name = "nut_tiep";
            next.Rect.Place(new Vector2(0.5f, 0.5f), new Vector2(220, -215), new Vector2(360, next.Rect.sizeDelta.y));
            next.SetRole(BtnColor.Green);
            next.SetText("Tiếp");

            // sao trắng viền mực: 8 sao bay ra, 12 lấp lánh nháy tại chỗ (ArtGen/UI/mo_khoa_tuong/sao.py)
            var fx = Rt("sao", root.transform);
            fx.Stretch();
            var starSp = Art("Assets/03 Art/Shop/sao_trang.png");
            var sparkSp = Art("Assets/03 Art/Shop/lap_lanh.png");
            const int big = 8, sparks = 12;
            var stars = new Image[big + sparks];
            for (int i = 0; i < stars.Length; i++)
            {
                bool b = i < big;
                stars[i] = Img((b ? "sao_" : "lap_lanh_") + i, fx, b ? starSp : sparkSp, Color.white);
                stars[i].rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, b ? new Vector2(132, 132) : new Vector2(86, 86));
                stars[i].gameObject.SetActive(false);
            }

            // bút chì (vẽ cho bản đồ đảo Cỏ), gốc ở ngòi
            var pencil = Img("but_chi", root.transform, Art("Assets/03 Art/Islands/Co/but_chi.png"), Color.white);
            pencil.preserveAspect = true;
            pencil.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(300, 257), new Vector2(0.105f, 0.143f));
            pencil.gameObject.SetActive(false);

            // bút chì màu (2026-11-25: nhiều bút chì màu tô các vùng cùng lúc; ArtGen/UI/mo_khoa_tuong/but_mau.py tách từ bút chì trên):
            // ảnh thân xám (nhuộm màu nhóm lúc chạy), con là vỏ chồng khít; cùng cỡ, cùng gốc ở ngòi như bút chì
            var crayonBody = Art("Assets/03 Art/Shop/but_mau_than.png");
            var crayonShell = Art("Assets/03 Art/Shop/but_mau_vo.png");
            var crayons = new Image[crayonBody && crayonShell ? 6 : 0];
            for (int i = 0; i < crayons.Length; i++)
            {
                var c = Img("but_mau_" + i, root.transform, crayonBody, Color.white);
                c.preserveAspect = true;
                c.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(300, 257), new Vector2(0.105f, 0.143f));
                var shell = Img("vo", c.transform, crayonShell, Color.white);
                shell.preserveAspect = true;
                shell.rectTransform.Stretch();
                c.gameObject.SetActive(false);
                crayons[i] = c;
            }

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (gr != ci && !gr.transform.IsChildOf(view.transform) && !gr.transform.IsChildOf(next.transform)) gr.raycastTarget = false;
            root.AddComponent<HeroUnlockView>().Setup(new HeroUnlockView.Parts
            {
                rarityBg = rarityBg, page = page, pencil = pencil, hero = hero, art = art, info = info, fx = fx, drawing = drawing, ink = ink,
                stars = stars, bigStars = big, badgeIcon = badgeIcon, ribbon = ribbon, ribbonText = ribbonText, heroName = heroName,
                rarity = rarity, title = title, elem = elem, rarityPill = pill, next = next, view = view, catcher = btn, stats = stats,
                crayons = crayons,
            });
            var v = Save<HeroUnlockView>(root, UnlockPath);
            kit.heroUnlock = v;
            EditorUtility.SetDirty(kit);
        }
    }
}
