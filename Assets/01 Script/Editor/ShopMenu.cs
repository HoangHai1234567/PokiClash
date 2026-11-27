// Cửa hàng (GD_Claude/26_CuaHang_IAP_QuangCao.md), menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết" (chạy lại được):
// Bản 3 (2026-11-27, cùng tông màn cửa hàng, GD_Claude/26 mục 17; sprite Assets/03 Art/Shop/v3, màu ShopHue):
// - Items/OGoi: ô gói (PackCell): nền màu tươi ba lớp, dải tên tối đáy, cột trái mô tả / ô món kem (Items/OMonCuaHang) / ghi chú, nhãn đỏ
//   "Giá trị ×N", đồng hồ viên tối, nút giá xanh lá + nút phụ, chữ "Đã mua";
// - Dialogs/CuaHang: tờ popup / trang con (ShopSheet, biến thể tờ giấy gốc HopThoai, phủ nền tối viền mực): băng tím tên vàng, dòng phụ,
//   hàng tab (ẩn), danh sách cuộn, nút "Hôm nay không hiện nữa"; thêm vào UiKit;
// - App.prefab: component OfferHost (máy hiện popup ưu đãi);
// - Dialogs/TranKetQua: nút quảng cáo riêng "hang_qc" dưới lời khuyên (BattleResultDialog.adButton: Tiếp sức / Nhận ×2);
// - App.prefab (giao diện sảnh chung LobbyDock, 2026-11-27; trước ở Screens/Hub): nhóm "cua_hang_san" mép trái dưới thanh trên (HubShop: Lọ Bi + 3 ưu đãi; bản ô vuông 2026-11-27: ô vuông bo tròn viền
//   trắng như Clash of Critters, lòng ô màu gói, hình gói to tràn mép trên và thở, đồng hồ chữ trắng viền mực đáy ô; cột phải cùng kiểu do
//   Editor/HubTileMenu.cs dựng). Nút Cửa hàng ở hàng nút đáy. Chỉ dựng tờ + ô + cụm sảnh: menu "Cửa hàng: tờ popup + cụm sảnh".
// Menu thử (đang Play): mở cửa hàng, ép từng popup, đặt lại trạng thái cửa hàng, tour chụp (Temp/PokiShots/cua_hang/).
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ShopMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const string ChestPath = "Assets/04 Prefabs/Dialogs/MoRuong.prefab";
        const string ResultPath = "Assets/04 Prefabs/Dialogs/TranKetQua.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string CellPath = "Assets/04 Prefabs/Items/OGoi.prefab";
        const string ShopPath = "Assets/04 Prefabs/Dialogs/CuaHang.prefab";
        const string IconDir = "Assets/03 Art/Fallback/Icons";

        internal static UiKit Kit => AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết", priority = 71)]
        public static void BuildAll()
        {
            // sprite giấy / mực (Sketch.*) tra bảng BakedArt, lúc chạy App gán; dựng trong Editor thì gán tạm từ asset
            if (!BakedArt.Current)
            {
                var guid = AssetDatabase.FindAssets("t:BakedArt").FirstOrDefault();
                if (guid != null) BakedArt.Current = AssetDatabase.LoadAssetAtPath<BakedArt>(AssetDatabase.GUIDToAssetPath(guid));
            }
            // material mã hoá của sprite giấy (Theme.Kit) nằm trong UiAssets, lúc chạy App gọi Theme.Init
            if (!Theme.Kit)
            {
                var ua = AssetDatabase.FindAssets("t:UiAssets").FirstOrDefault();
                if (ua != null) Theme.Init(AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(ua)));
            }
            if (!Sketch.PanelThin) Debug.LogWarning("[Cửa hàng] Không nạp được sprite giấy (BakedArt): ô gói sẽ không có viền");
            var cell = BuildCell();
            BuildSheet(cell);
            ShopPageMenu.Build(); // màn cửa hàng toàn màn hình, ô / thẻ / mục, màn nở trứng (2026-11-23)
            AddHost();
            PatchResult();
            BuildHub();
            AssetDatabase.SaveAssets();
            Debug.Log($"[Cửa hàng] Đã dựng {CellPath}, {ShopPath} (UiKit), OfferHost trong App.prefab, nút quảng cáo hộp kết quả trận, nhóm cua_hang_san ở sảnh.");
        }

        // ---------- mẫu chữ ----------

        internal static (TextMeshProUGUI title, TextMeshProUGUI hint) Templates()
        {
            var prep = AssetDatabase.LoadAssetAtPath<GameObject>(PrepPath).GetComponent<StagePrepDialog>();
            var so = new SerializedObject(prep);
            return ((TextMeshProUGUI)so.FindProperty("p.title").objectReferenceValue, (TextMeshProUGUI)so.FindProperty("p.hint").objectReferenceValue);
        }

        internal static TextMeshProUGUI Text(TextMeshProUGUI tpl, Transform parent, string name, float size, TextAlignmentOptions align, Color color)
        {
            var t = Object.Instantiate(tpl.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = name;
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            foreach (var c in t.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
            t.gameObject.SetActive(true);
            t.enableAutoSizing = false;
            t.fontSize = size;
            t.alignment = align;
            t.color = color;
            t.textWrappingMode = TextWrappingModes.Normal;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }

        internal static RectTransform Rt(string name, Transform parent, params System.Type[] comps)
        {
            var go = new GameObject(name, new[] { typeof(RectTransform) }.Concat(comps).ToArray());
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        internal static Image Img(string name, Transform parent, Sprite s, Color c)
        {
            var img = Rt(name, parent, typeof(CanvasRenderer), typeof(Image)).GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.raycastTarget = false;
            return img;
        }

        internal static Sprite Icon(string name) => AssetDatabase.LoadAllAssetsAtPath($"{IconDir}/{name}.png").OfType<Sprite>().FirstOrDefault();

        internal static void Le(Component c, float h, float w = -1)
        {
            var le = c.GetComponent<LayoutElement>() ?? c.gameObject.AddComponent<LayoutElement>();
            le.preferredHeight = h;
            if (w >= 0) le.preferredWidth = w;
        }

        // ---------- ô gói (bản 3: cùng tông màn cửa hàng, GD_Claude/26 mục 17) ----------

        const string ItemCellPath = "Assets/04 Prefabs/Items/OMonCuaHang.prefab";

        static PackCell BuildCell()
        {
            var (titleTpl, hintTpl) = Templates();
            var tile = AssetDatabase.LoadAssetAtPath<GameObject>(ChestPath).GetComponent<ChestDialog>().TilePrefab;
            var itemCell = AssetDatabase.LoadAssetAtPath<GameObject>(ItemCellPath)?.GetComponent<ShopItemCell>();
            if (!itemCell) Debug.LogError("[Cửa hàng] Chưa có Items/OMonCuaHang: dựng màn cửa hàng (ShopPageMenu) trước");
            var navy = ShopPageMenu.Navy;
            var root = Rt("OGoi", null, typeof(CanvasRenderer), typeof(Image), typeof(LayoutElement)).gameObject;
            try
            {
                var rt = (RectTransform)root.transform;
                rt.sizeDelta = new Vector2(900, 300);
                var card = root.GetComponent<Image>();
                Theme.SetSprite(card, ShopPageMenu.V3Sprite("the_nen", ShopPageMenu.CardBorder));
                card.type = Image.Type.Sliced;
                card.color = ShopHue.Sunset.fill;
                card.raycastTarget = false;
                var panel = ShopPageMenu.Sliced("mang_phai", root.transform, ShopPageMenu.V3Sprite("the_phai", ShopPageMenu.CardBorder), ShopHue.Sunset.panel);
                var rays = ShopPageMenu.Sliced("sao_no", root.transform, ShopPageMenu.V3Sprite("the_tia", ShopPageMenu.CardBorder), ShopHue.Sunset.rays);
                var layout = root.GetComponent<LayoutElement>();
                layout.preferredHeight = 300;
                layout.minHeight = 200;

                // cột trái phía trên dải tên: mô tả, lưới món, ghi chú
                var left = Rt("trai", root.transform, typeof(VerticalLayoutGroup));
                left.anchorMin = new Vector2(0, 0);
                left.anchorMax = new Vector2(0, 1);
                left.pivot = new Vector2(0, 1);
                left.offsetMin = new Vector2(26, PackCell.Strip);
                left.offsetMax = new Vector2(26 + 570, -22);
                var vl = left.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 8;
                vl.childAlignment = TextAnchor.UpperLeft;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = vl.childForceExpandHeight = false;
                var desc = Text(hintTpl, left, "mo_ta", 25, TextAlignmentOptions.TopLeft, Color.white);
                Le(desc, 58);
                desc.enableAutoSizing = true;
                desc.fontSizeMin = 17;
                desc.fontSizeMax = 25;
                ShopPageMenu.Ink(desc, 0.22f);
                var items = Rt("mon", left, typeof(GridLayoutGroup), typeof(LayoutElement));
                items.pivot = new Vector2(0, 1);
                items.localScale = Vector3.one * PackCell.ItemScale;
                var grid = items.GetComponent<GridLayoutGroup>();
                grid.cellSize = new Vector2(ShopItemCell.Size, ShopItemCell.Size);
                grid.spacing = new Vector2(10, 10);
                grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
                grid.constraintCount = 5;
                grid.startCorner = GridLayoutGroup.Corner.UpperLeft;
                grid.childAlignment = TextAnchor.UpperLeft;
                var ile = items.GetComponent<LayoutElement>();
                ile.preferredHeight = ShopItemCell.Size * PackCell.ItemScale;
                ile.preferredWidth = 5 * ShopItemCell.Size + 4 * 10;
                var note = Text(hintTpl, left, "ghi_chu", 25, TextAlignmentOptions.MidlineLeft, Color.white);
                Le(note, 38);
                note.enableAutoSizing = true;
                note.fontSizeMin = 17;
                note.fontSizeMax = 25;
                ShopPageMenu.Ink(note, 0.22f);

                // tên trong dải tối đáy
                var title = Text(titleTpl, root.transform, "ten", 40, TextAlignmentOptions.MidlineLeft, Color.white);
                title.rectTransform.anchorMin = new Vector2(0, 0);
                title.rectTransform.anchorMax = new Vector2(1, 0);
                title.rectTransform.pivot = new Vector2(0, 0);
                title.rectTransform.offsetMin = new Vector2(28, 12);
                title.rectTransform.offsetMax = new Vector2(-310, 88);
                title.enableAutoSizing = true;
                title.fontSizeMin = 24;
                title.fontSizeMax = 40;
                title.textWrappingMode = TextWrappingModes.NoWrap;
                ShopPageMenu.Ink(title, 0.28f);

                // nhãn đỏ "Giá trị ×N" chìa ra mép trên phải
                var value = Img("gia_tri", root.transform, ShopPageMenu.V3Sprite("nhan_gia_tri", new Vector4(34, 10, 14, 10)), Color.white);
                value.type = Image.Type.Sliced;
                value.rectTransform.Place(new Vector2(1, 1), new Vector2(8, 12), new Vector2(300, 70), new Vector2(1, 1));
                var valueText = Text(titleTpl, value.transform, "chu", 34, TextAlignmentOptions.Center, Color.white);
                valueText.rectTransform.Stretch(36, 4, 14, 6);
                valueText.enableAutoSizing = true;
                valueText.fontSizeMin = 20;
                valueText.fontSizeMax = 34;
                valueText.textWrappingMode = TextWrappingModes.NoWrap;
                ShopPageMenu.Ink(valueText, 0.25f);

                // đồng hồ viên tối dưới nhãn
                var pill = Img("dong_ho", root.transform, ShopPageMenu.V3Sprite("vien", ShopPageMenu.PillBorder), new Color(navy.r, navy.g, navy.b, 0.88f));
                pill.type = Image.Type.Sliced;
                pill.rectTransform.Place(new Vector2(1, 1), new Vector2(-20, -74), new Vector2(220, 48), new Vector2(1, 1));
                var timer = Text(hintTpl, pill.transform, "chu", 25, TextAlignmentOptions.Center, Color.white);
                timer.rectTransform.Stretch(8, 2, 8, 2);
                timer.fontStyle = FontStyles.Bold;

                // nút giá xanh lá trong dải tên, nút phụ phía trên
                var buy = ShopPageMenu.PriceButton(root.transform, "nut_mua", 270, 92, 40);
                var br = buy.Rect;
                br.anchorMin = br.anchorMax = br.pivot = new Vector2(1, 0);
                br.anchoredPosition = new Vector2(-20, 12);
                var extra = ShopPageMenu.PriceButton(root.transform, "nut_phu", 270, 80, 30);
                var er = extra.Rect;
                er.anchorMin = er.anchorMax = er.pivot = new Vector2(1, 0);
                er.anchoredPosition = new Vector2(-20, 12 + 92 + 12);
                var done = Text(titleTpl, root.transform, "da_mua", 38, TextAlignmentOptions.Center, ShopPageMenu.DoneGreen);
                done.rectTransform.Place(new Vector2(1, 0), new Vector2(-26, 14), new Vector2(300, 76), new Vector2(1, 0));
                done.rectTransform.localEulerAngles = new Vector3(0, 0, 4);
                done.enableAutoSizing = true;
                done.fontSizeMin = 20;
                done.fontSizeMax = 38;
                ShopPageMenu.Ink(done, 0.25f);

                foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                    if (!gr.transform.IsChildOf(buy.transform) && !gr.transform.IsChildOf(extra.transform)) gr.raycastTarget = false;
                buy.GetComponent<Image>().raycastTarget = extra.GetComponent<Image>().raycastTarget = true;

                root.AddComponent<PackCell>().Setup(new PackCell.Parts
                {
                    card = card, panel = panel, rays = rays, valueBg = value, title = title, desc = desc, timer = timer, note = note, done = done,
                    valueText = valueText, timerBox = pill.gameObject, items = items, buy = buy, extra = extra, layout = layout,
                }, itemCell, tile);
                return PrefabUtility.SaveAsPrefabAsset(root, CellPath).GetComponent<PackCell>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- tờ cửa hàng / popup (bản 3: tờ tối viền mực, băng tím tiêu đề vàng) ----------

        static void BuildSheet(PackCell cell)
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "CuaHang";
                root.GetComponent<ModalSheet>().Configure(1000, false, true);
                var sheet = root.GetComponentsInChildren<Transform>(true).First(t => t.name == "to_giay");
                // nền tối trùm kín tờ giấy (không vào bố cục), bỏ băng keo
                var tape = sheet.Find("bang_keo");
                if (tape) tape.gameObject.SetActive(false);
                var dark = ShopPageMenu.Sliced("nen_to_toi", sheet, ShopPageMenu.V3Sprite("to_toi", new Vector4(44, 44, 44, 44)), Color.white);
                dark.rectTransform.Stretch(-10, -10, -10, -10);
                dark.gameObject.AddComponent<LayoutElement>().ignoreLayout = true;

                // nền tối thêm SAU các lớp trang trí giấy của tờ gốc (luoi: kẻ ô, chi_khau: đường chỉ) nên nằm trên chúng; nội dung thêm sau
                // nên nằm trên nền (đừng đổi thứ tự: bản đặt nền lên đầu bị kẻ ô đè, bản dời nền xuống sau nội dung thì che mất thẻ)
                var content = Rt("noi_dung", sheet, typeof(VerticalLayoutGroup));
                var vl = content.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 12;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = true;
                vl.childForceExpandHeight = false;

                // băng tím, tên vàng viền mực; dòng phụ trắng
                var head = Rt("bang_tieu_de", content, typeof(LayoutElement));
                Le(head, 100);
                var band = ShopPageMenu.Sliced("bang", head, ShopPageMenu.V3Sprite("muc_bang", new Vector4(30, 30, 30, 30)), Color.white);
                var title = Text(titleTpl, band.transform, "tieu_de", 56, TextAlignmentOptions.Center, ShopPageMenu.Gold);
                title.rectTransform.Stretch(80, 4, 80, 12);
                title.enableAutoSizing = true;
                title.fontSizeMin = 30;
                title.fontSizeMax = 56;
                title.textWrappingMode = TextWrappingModes.NoWrap;
                ShopPageMenu.Ink(title, 0.3f);
                var sub = Text(hintTpl, content, "dong_phu", 28, TextAlignmentOptions.Center, Color.white);
                Le(sub, 46);
                sub.enableAutoSizing = true;
                sub.fontSizeMin = 18;
                sub.fontSizeMax = 28;
                ShopPageMenu.Ink(sub, 0.22f);

                // hàng tab (tờ này không còn dùng tab: luôn ẩn; giữ cho ShopSheet.Parts)
                var tabRow = Rt("hang_tab", content, typeof(HorizontalLayoutGroup), typeof(LayoutElement));
                Le(tabRow, 96);
                var hl = tabRow.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 10;
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var tabs = new SketchButton[4];
                var dots = new GameObject[4];
                string[] tabNames = { "Ưu đãi", "Bi", "Tướng", "Đặc quyền" };
                for (int i = 0; i < 4; i++)
                {
                    var b = Ui.Spawn(kit.buttonSmall, tabRow);
                    b.name = "tab_" + ShopSheet.TabIds[i];
                    b.Rect.sizeDelta = new Vector2(220, b.Rect.sizeDelta.y);
                    b.SetText(tabNames[i]);
                    b.SetRole(i == 0 ? BtnColor.Orange : BtnColor.Paper);
                    var dot = Img("cham_do", b.transform, ShopPageMenu.V3Sprite("cham_do", Vector4.zero), Color.white);
                    dot.rectTransform.Place(new Vector2(1, 1), new Vector2(-6, -6), new Vector2(34, 34), new Vector2(0.5f, 0.5f));
                    dot.gameObject.SetActive(false);
                    tabs[i] = b;
                    dots[i] = dot.gameObject;
                }
                tabRow.gameObject.SetActive(false);

                // danh sách cuộn
                var scrollGo = Rt("cuon", content, typeof(CanvasRenderer), typeof(Image), typeof(ScrollRect), typeof(LayoutElement)).gameObject;
                var scrollLe = scrollGo.GetComponent<LayoutElement>();
                scrollLe.preferredHeight = 1000;
                scrollGo.GetComponent<Image>().color = new Color(1, 1, 1, 0);
                var scroll = scrollGo.GetComponent<ScrollRect>();
                scroll.horizontal = false;
                scroll.vertical = true;
                scroll.movementType = ScrollRect.MovementType.Clamped;
                var viewport = Rt("khung", scrollGo.transform, typeof(RectMask2D));
                viewport.Stretch();
                var list = Rt("danh_sach", viewport, typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
                list.anchorMin = new Vector2(0, 1);
                list.anchorMax = new Vector2(1, 1);
                list.pivot = new Vector2(0.5f, 1);
                list.anchoredPosition = Vector2.zero;
                list.sizeDelta = Vector2.zero;
                var lvl = list.GetComponent<VerticalLayoutGroup>();
                lvl.spacing = 22;
                // trên 16 cho nhãn giá trị chìa ra mép ô đầu, phải 12 cho nhãn chìa ra mép phải
                lvl.padding = new RectOffset(4, 12, 16, 16);
                lvl.childControlWidth = lvl.childControlHeight = true;
                lvl.childForceExpandWidth = true;
                lvl.childForceExpandHeight = false;
                list.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                scroll.viewport = viewport;
                scroll.content = list;

                // "Hôm nay không hiện nữa": nút tấm xám hai tông (vai giấy; đã tích thì xanh)
                var muteRow = Rt("hang_tat", content, typeof(LayoutElement));
                Le(muteRow, 92);
                var mute = ShopPageMenu.PriceButton(muteRow, "nut_tat_hom_nay", 560, 80, 30);
                var mr = mute.Rect;
                mr.anchorMin = mr.anchorMax = mr.pivot = new Vector2(0.5f, 0.5f);
                mr.anchoredPosition = Vector2.zero;
                mute.SetRole(BtnColor.Paper);
                mute.SetText("Hôm nay không hiện nữa");

                root.AddComponent<ShopSheet>().Setup(new ShopSheet.Parts
                {
                    title = title, sub = sub, tabRow = tabRow, tabs = tabs, dots = dots, scroll = scroll, list = list, scrollLayout = scrollLe, mute = mute,
                }, cell);
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, ShopPath).GetComponent<ShopSheet>();
                if (!kit.dialogs.Any(x => x is ShopSheet))
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

        // ---------- App.prefab: OfferHost ----------

        static void AddHost()
        {
            var contents = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var app = contents.GetComponentInChildren<App>(true);
                if (contents.GetComponentInChildren<OfferHost>(true)) return;
                app.gameObject.AddComponent<OfferHost>();
                PrefabUtility.SaveAsPrefabAsset(contents, AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // ---------- hộp kết quả trận: nút quảng cáo ----------

        static void PatchResult()
        {
            var kit = Kit;
            var contents = PrefabUtility.LoadPrefabContents(ResultPath);
            try
            {
                var dlg = contents.GetComponent<BattleResultDialog>() ?? contents.GetComponentInChildren<BattleResultDialog>(true);
                var so = new SerializedObject(dlg);
                var prop = so.FindProperty("adButton");
                if (prop.objectReferenceValue) return;
                var tips = (TextMeshProUGUI)so.FindProperty("tips").objectReferenceValue;
                var parent = tips.transform.parent;
                var row = Rt("hang_qc", parent, typeof(LayoutElement));
                row.SetSiblingIndex(tips.transform.GetSiblingIndex() + 1);
                Le(row, 104);
                var b = Ui.Spawn(kit.buttonNormal, row);
                b.name = "nut_qc";
                var r = b.Rect;
                r.anchorMin = r.anchorMax = r.pivot = new Vector2(0.5f, 0.5f);
                r.anchoredPosition = Vector2.zero;
                r.sizeDelta = new Vector2(420, r.sizeDelta.y);
                b.SetRole(BtnColor.Blue);
                b.SetText("Xem quảng cáo");
                b.gameObject.SetActive(false);
                prop.objectReferenceValue = b;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, ResultPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // ---------- sảnh: Lọ Bi, ưu đãi (bản ô vuông 2026-11-27: ô vuông bo tròn viền trắng như cột icon máy bi Clash of Critters,
        // lòng ô màu của gói, hình gói to tràn mép trên và thở, đồng hồ chữ trắng viền mực ở đáy ô) ----------

        // cạnh ô, phần hình tràn trên mép ô, bước dọc giữa hai ô (cột trái 4 ô: Lọ Bi + 3 ưu đãi). Cột phải (HubTileMenu) dùng cùng số.
        // Bước 214 (người dùng 2026-11-27 "giãn khoảng cách các ô ra"; 186 chỉ hở 12 giữa đáy ô và đỉnh hình ô dưới, giờ 40).
        internal const float HubTileSize = 152, HubTileOver = 22, HubStep = 214;
        // chữ tên / đồng hồ đáy ô (người dùng 2026-11-27 "phóng to text lên chút nữa": 23–24 -> 28), cao vùng chữ
        internal const float HubLabelSize = 28, HubLabelH = 56;

        static Sprite ShopArt(string name) => AssetDatabase.LoadAllAssetsAtPath($"Assets/03 Art/Shop/v2/{name}.png").OfType<Sprite>().FirstOrDefault();

        // tâm ngang vòng cấp ở thanh trên (App.prefab, TopBars: Hud 1040 rộng neo giữa màn 1080, hàng ngang căn trái, vong_cap đầu hàng
        // rộng 180 → 110): cột ô trái đặt tâm ô đúng chỗ này (người dùng 2026-11-27: "ô level và các ô dưới không thẳng hàng")
        internal static float LevelCenterX()
        {
            var app = AssetDatabase.LoadAssetAtPath<GameObject>(AppPath);
            var bars = app ? app.GetComponentInChildren<TopBars>(true) : null;
            var hud = bars ? new SerializedObject(bars).FindProperty("hud").objectReferenceValue as RectTransform : null;
            var ring = hud ? hud.Find("vong_cap") as RectTransform : null;
            var hl = hud ? hud.GetComponent<HorizontalLayoutGroup>() : null;
            if (!ring || !hl)
            {
                Debug.LogWarning("[Cửa hàng] Không đọc được vòng cấp ở App.prefab, cột trái đặt tâm x = 110");
                return 110;
            }
            var le = ring.GetComponent<LayoutElement>();
            float w = le && le.preferredWidth > 0 ? le.preferredWidth : ring.sizeDelta.x;
            return (PokiCanvas.RefW - hud.sizeDelta.x) / 2 + hl.padding.left + w / 2;
        }

        // lòng ô (tô màu), viền trắng giấy, lớp đen mờ đáy ô dưới chữ của ô vuông sảnh (ArtGen/Shop/v3/ve_ui.py hub_tile)
        internal static (Sprite nen, Sprite vien, Sprite day) HubTileSprites() =>
            (ShopPageMenu.V3Sprite("o_san_nen", Vector4.zero), ShopPageMenu.V3Sprite("o_san_vien", Vector4.zero),
                ShopPageMenu.V3Sprite("o_san_day", Vector4.zero));

        // lòng ô + viền trắng + hình to (tràn mép trên, thở lệch pha) vào một khung ô T × T có sẵn; trả hình
        internal static (Image nen, Image icon) HubTileFace(RectTransform tile, Sprite art, Color hue, float phase)
        {
            var (nenS, vienS, dayS) = HubTileSprites();
            var nen = Img("nen_o", tile, nenS, hue);
            nen.rectTransform.Stretch();
            var vien = Img("vien_o", tile, vienS, Color.white);
            vien.rectTransform.Stretch();
            var T = HubTileSize;
            var icon = Img("hinh", tile, art, Color.white);
            icon.preserveAspect = true;
            // tâm hình cao hơn giữa ô: chừa đáy cho chữ, đỉnh hình nhô qua mép trên HubTileOver
            icon.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -T * 0.42f + 4), new Vector2(T * 1.02f, T * 0.92f), new Vector2(0.5f, 0.5f));
            var br = icon.gameObject.AddComponent<Breathe>();
            br.amount = 0.06f;
            br.period = 1.8f;
            br.phase = phase;
            // lớp đen mờ đáy ô (người dùng 2026-11-27: "phần text có 1 lớp đen mờ ở dưới để người chơi đọc được"): trên hình, dưới chữ
            var day = Img("day_o", tile, dayS, Color.white);
            day.rectTransform.Stretch();
            return (nen, icon);
        }

        // chữ trắng viền mực ở đáy ô (tên, đồng hồ)
        internal static TextMeshProUGUI HubTileLabel(TextMeshProUGUI tpl, RectTransform tile, string name, float size, float height)
        {
            var t = Text(tpl, tile, name, size, TextAlignmentOptions.Center, Color.white);
            t.rectTransform.anchorMin = new Vector2(0, 0);
            t.rectTransform.anchorMax = new Vector2(1, 0);
            t.rectTransform.pivot = new Vector2(0.5f, 0);
            t.rectTransform.offsetMin = new Vector2(8, 10);
            t.rectTransform.offsetMax = new Vector2(-8, 10 + height);
            t.enableAutoSizing = true;
            t.fontSizeMin = 14;
            t.fontSizeMax = size;
            t.lineSpacing = -18;
            ShopPageMenu.Ink(t, 0.28f);
            return t;
        }

        // một ô ở cột sảnh: vùng chạm là ô (SketchButton: lún, nảy khi chạm), mặt ô HubTileFace
        static (SketchButton button, Image icon, Image nen) HubTile(Transform parent, string name, float y, Sprite art, Color hue, float phase)
        {
            var (outlined, plain) = ShopPageMenu.KitLabelMats();
            var bg = Img(name, parent, null, new Color(1, 1, 1, 0));
            bg.raycastTarget = true;
            bg.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, y), new Vector2(HubTileSize, HubTileSize), new Vector2(0.5f, 1));
            var (nen, icon) = HubTileFace(bg.rectTransform, art, hue, phase);
            var b = bg.gameObject.AddComponent<SketchButton>();
            b.Setup(bg, null, false, null, null, outlined, plain);
            b.SetColor(new Color(1, 1, 1, 0));
            foreach (var g in bg.GetComponentsInChildren<Graphic>(true))
                if (g != bg) g.raycastTarget = false;
            return (b, icon, nen);
        }

        internal static void BuildHub()
        {
            var (titleTpl, _) = Templates();
            var navy = ShopPageMenu.Navy;
            // cột ưu đãi ở App.prefab, vùng an toàn của canvas thanh trên, cạnh hàng nút sảnh chung (LobbyDock, 2026-11-27)
            var contents = PrefabUtility.LoadPrefabContents(LobbyDockMenu.AppPath);
            try
            {
                var dock = contents.GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "hang_nut");
                var canvas = dock ? dock.GetComponentInParent<PokiCanvas>(true) : contents.GetComponentInChildren<PokiCanvas>(true);
                if (!canvas)
                {
                    Debug.LogError("[Cửa hàng] Không thấy canvas của sảnh.");
                    return;
                }
                var old = canvas.Safe.Find("cua_hang_san");
                if (old) Object.DestroyImmediate(old.gameObject);
                var holder = Rt("cua_hang_san", canvas.Safe);
                holder.anchorMin = holder.anchorMax = holder.pivot = new Vector2(0, 1);
                float cx = LevelCenterX();
                holder.anchoredPosition = new Vector2(cx - (HubTileSize + 12) / 2, -216);
                Debug.Log($"[Cửa hàng] Cột ô trái: tâm x = {cx} (theo vòng cấp)");
                holder.sizeDelta = new Vector2(HubTileSize + 12, HubTileOver + HubStep * 4);
                var group = Rt("nhom", holder);
                group.Stretch();

                // Lọ Bi: ô trời, hình lọ, thanh viên tối đầy vàng trong đáy ô, số trắng
                var (piggy, _, _) = HubTile(group, "nut_lo_bi", -HubTileOver, ShopArt("goi2_lo_bi"), ShopHue.Sky.fill, 0);
                var track = Img("thanh", piggy.transform, ShopPageMenu.V3Sprite("vien", ShopPageMenu.PillBorder), new Color(navy.r, navy.g, navy.b, 0.92f));
                track.type = Image.Type.Sliced;
                track.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 12), new Vector2(HubTileSize - 30, 40), new Vector2(0.5f, 0));
                var fill = Img("day", track.transform, ShopPageMenu.V3Sprite("vien", ShopPageMenu.PillBorder), Theme.Yellow);
                fill.type = Image.Type.Filled;
                fill.fillMethod = Image.FillMethod.Horizontal;
                fill.rectTransform.Stretch(6, 6, 6, 6);
                var ptext = Text(titleTpl, track.transform, "so", 27, TextAlignmentOptions.Center, Color.white);
                ptext.rectTransform.Stretch(8, 1, 8, 1);
                ptext.enableAutoSizing = true;
                ptext.fontSizeMin = 14;
                ptext.fontSizeMax = 27;
                ShopPageMenu.Ink(ptext, 0.25f);
                foreach (var g in track.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;

                // 3 ưu đãi đang mở (hình, màu lòng ô đặt lúc chạy theo gói); đồng hồ chữ trắng viền mực đáy ô
                var bubs = new HubShop.Bubble[3];
                for (int i = 0; i < 3; i++)
                {
                    var (b, icon, nen) = HubTile(group, "bong_bong_" + (i + 1), -HubTileOver - (i + 1) * HubStep, ShopArt("goi2_nhap_mon"),
                        ShopHue.Sunset.fill, (i + 1) * 0.27f);
                    var t = HubTileLabel(titleTpl, b.Rect, "gio", HubLabelSize, HubLabelH * 0.75f);
                    t.textWrappingMode = TextWrappingModes.NoWrap;
                    b.gameObject.SetActive(false);
                    bubs[i] = new HubShop.Bubble { button = b, icon = icon, timer = t, timerBg = null, tile = nen };
                }
                holder.gameObject.AddComponent<HubShop>().Setup(group.gameObject, null, null, piggy, fill, ptext, bubs);
                PrefabUtility.SaveAsPrefabAsset(contents, LobbyDockMenu.AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // tờ popup + ô gói + cụm sảnh (bản 3), không dựng lại màn cửa hàng / nở trứng / mở khoá / quà ngày, App.prefab, hộp kết quả trận
        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: tờ popup + cụm sảnh", priority = 71)]
        public static void BuildSheetAndHub()
        {
            if (!BakedArt.Current)
            {
                var guid = AssetDatabase.FindAssets("t:BakedArt").FirstOrDefault();
                if (guid != null) BakedArt.Current = AssetDatabase.LoadAssetAtPath<BakedArt>(AssetDatabase.GUIDToAssetPath(guid));
            }
            if (!Theme.Kit)
            {
                var ua = AssetDatabase.FindAssets("t:UiAssets").FirstOrDefault();
                if (ua != null) Theme.Init(AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(ua)));
            }
            BuildSheet(BuildCell());
            BuildHub();
            AssetDatabase.SaveAssets();
            Debug.Log($"[Cửa hàng] Đã dựng {CellPath}, {ShopPath}, cụm ưu đãi ở sảnh (bản 3).");
        }

        // ---------- menu thử (đang Play) ----------

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();

        static bool Playing()
        {
            if (EditorApplication.isPlaying && App.I != null) return true;
            Debug.LogWarning("[Cửa hàng] Mở Boot.unity và bấm Play trước.");
            return false;
        }

        static void Prep()
        {
            Tutorial.Skip(S);
            Offers.EnsureStarter(S, D, Now);
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/mở (đang Play)", priority = 150)]
        static void OpenShop()
        {
            if (!Playing()) return;
            Prep();
            ShopSheet.OpenShop();
        }

        static void Pop(Popup p)
        {
            if (!Playing()) return;
            App.Modals.CloseAll();
            OfferHost.Push(p);
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/popup Hết bi (đang Play)", priority = 151)]
        static void PopRefill() => Pop(new Popup { kind = "refill", free = true });

        [MenuItem("PokiClash/Thử/Cửa hàng/popup Sắp hết bi (đang Play)", priority = 151)]
        static void PopRefillLow() => Pop(new Popup { kind = "refill", warn = true, key = "refill_low" });

        [MenuItem("PokiClash/Thử/Cửa hàng/popup Ưu Đãi Bất Ngờ (đang Play)", priority = 152)]
        static void PopFlash()
        {
            if (!Playing()) return;
            Prep();
            var o = Offers.Build(S, D, "flash", null, Now, new Rng(Rng.RandomSeed()));
            App.Save.Save();
            Pop(new Popup { kind = "offer", id = o.uid, key = "flash" });
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/popup Gói Tiếp Sức (đang Play)", priority = 153)]
        static void PopRelief()
        {
            if (!Playing()) return;
            Prep();
            var o = Offers.Build(S, D, "relief", null, Now, new Rng(Rng.RandomSeed()));
            App.Save.Save();
            Pop(new Popup { kind = "offer", id = o.uid, key = "relief" });
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/popup Quà Nhập Môn (đang Play)", priority = 154)]
        static void PopStarter()
        {
            if (!Playing()) return;
            Prep();
            var o = S.shop.offers.active.Find(x => x.pack == "starter3");
            if (o == null || o.bought)
            {
                Debug.LogWarning("[Cửa hàng] Quà Nhập Môn đã mua hoặc chưa có (đặt lại trạng thái cửa hàng rồi thử lại).");
                return;
            }
            Pop(new Popup { kind = "offer", id = o.uid, key = "starter3" });
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/popup Lọ Bi đầy (đang Play)", priority = 155)]
        static void PopPiggy()
        {
            if (!Playing()) return;
            Prep();
            Shop.Of(S).piggy = Shop.PiggyCap(S, D.Cfg.shop);
            App.Save.Save();
            Pop(new Popup { kind = "piggy", key = "piggy" });
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/popup Chuỗi Quà (đang Play)", priority = 156)]
        static void PopChain()
        {
            if (!Playing()) return;
            Prep();
            if (!Shop.ChainLive(S, Now)) Shop.ChainStart(S, D.Cfg.shop, Now);
            App.Save.Save();
            Pop(new Popup { kind = "chain", key = "chain" });
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/popup Quà hôm nay (đang Play)", priority = 157)]
        static void PopClaims()
        {
            if (!Playing()) return;
            Prep();
            Shop.Of(S).giftDay = -1;
            App.Save.Save();
            Pop(new Popup { kind = "claims", free = true });
        }

        // màn quà hôm nay (DailyGiftView): lượt 1 có quảng cáo (chụp các nhịp, bấm ×2, quảng cáo giả 3 s, dấu ×2, quà bay), lượt 2 không có
        // quảng cáo (nút Nhận hiện ngay). Ảnh ở Temp/PokiShots/qua_ngay/; sao lưu và trả bản lưu.
        [MenuItem("PokiClash/Thử/Cửa hàng/màn quà hôm nay: chụp (đang Play)", priority = 157)]
        static void GiftTour()
        {
            if (!Playing()) return;
            App.I.StartCoroutine(RunGiftTour());
        }

        static IEnumerator RunGiftTour()
        {
            var dir = Path.Combine(PlayTour.ShotDir, "qua_ngay");
            if (Directory.Exists(dir)) Directory.Delete(dir, true);
            Directory.CreateDirectory(dir);
            int n = 0;
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var ads = Ads.Current;
            IEnumerator At(float t0, float a, string name)
            {
                while (Time.realtimeSinceStartup - t0 < a) yield return null;
                yield return new WaitForEndOfFrame();
                var tex = ScreenCapture.CaptureScreenshotAsTexture();
                File.WriteAllBytes(Path.Combine(dir, $"{n++:00}_{name}_{a:0.0}s.jpg"), tex.EncodeToJPG(85));
                Object.Destroy(tex);
            }
            SketchButton Btn(string name) => Object.FindAnyObjectByType<DailyGiftView>()?.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == name);
            try
            {
                App.Modals.CloseAll();
                Prep();
                Shop.Of(S).giftDay = -1;
                AdGate.Of(S).used.Remove(Ads.DailyGiftAd); // bản lưu đã dùng hết lượt ×2 hôm nay thì không có nút ×2 để chụp (trả lại ở finally)
                if (!DailyGiftView.Open(null))
                {
                    Debug.LogWarning("[Cửa hàng] Không mở được màn quà hôm nay (chưa dựng prefab Items/QuaNgay?).");
                    yield break;
                }
                float t = Time.realtimeSinceStartup;
                foreach (var a in new[] { 0.15f, 0.45f, 0.7f, 1.0f, 1.3f, 1.8f, 2.6f, 3.4f }) yield return At(t, a, "co_qc");
                Btn("nut_x2")?.SimulateClick();
                t = Time.realtimeSinceStartup;
                foreach (var a in new[] { 1.0f, 3.3f, 3.6f, 4.0f, 4.6f, 5.2f }) yield return At(t, a, "bam_x2");
                while (DailyGiftView.Playing) yield return null;
                yield return new WaitForSecondsRealtime(0.4f);

                // không có quảng cáo: nút Nhận xanh hiện ngay
                Ads.Current = null;
                Shop.Of(S).giftDay = -1;
                App.Modals.CloseAll();
                DailyGiftView.Open(null);
                t = Time.realtimeSinceStartup;
                foreach (var a in new[] { 1.2f, 2.0f }) yield return At(t, a, "khong_qc");
                Btn("nut_thuong")?.SimulateClick();
                t = Time.realtimeSinceStartup;
                yield return At(t, 0.3f, "khong_qc_nhan");
                while (DailyGiftView.Playing) yield return null;
                Debug.Log($"[Cửa hàng] Màn quà hôm nay: {n} ảnh ở {dir}");
            }
            finally
            {
                Ads.Current = ads;
                foreach (var v in Object.FindObjectsByType<DailyGiftView>(FindObjectsSortMode.None)) Object.Destroy(v.gameObject);
                App.Modals.CloseAll();
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/vào game lại (hàng popup lúc vào) (đang Play)", priority = 158)]
        static void ReOpen()
        {
            if (!Playing()) return;
            Prep();
            var list = Offers.Open(S, D, Now, new Rng(Rng.RandomSeed()));
            App.Save.Save();
            foreach (var p in list) OfferHost.Push(p);
            Debug.Log("[Cửa hàng] Hàng popup lúc vào game: " + (list.Count == 0 ? "(trống: hết trần hoặc chưa tới mốc)" : string.Join(", ", list)));
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/đặt lại trạng thái cửa hàng (đang Play)", priority = 159)]
        static void ResetShop()
        {
            if (!Playing()) return;
            S.shop = null;
            App.Save.Save();
            Debug.Log("[Cửa hàng] Đã xoá trạng thái cửa hàng của bản lưu (gói đã mua, ưu đãi, Lọ Bi, thẻ, túi rương).");
        }

        // màn mở khoá tướng: mỗi bậc một tướng, chụp các pha (tụ lực, bùng, lộ diện, bảng tin) vào Temp/PokiShots/mo_khoa/
        [MenuItem("PokiClash/Thử/Cửa hàng/màn mở khoá tướng, 5 bậc (đang Play)", priority = 161)]
        static void UnlockTour()
        {
            if (!Playing()) return;
            App.I.StartCoroutine(RunUnlockTour());
        }

        static IEnumerator RunUnlockTour()
        {
            var dir = Path.Combine(PlayTour.ShotDir, "mo_khoa");
            if (Directory.Exists(dir)) Directory.Delete(dir, true);
            Directory.CreateDirectory(dir);
            int n = 0;
            App.Modals.CloseAll();
            for (int r = 0; r < 5; r++)
            {
                var h = D.Heroes.FirstOrDefault(x => (int)x.rarity == r);
                if (h == null) continue;
                HeroUnlockView.Play(new[] { h.id });
                // nhịp bút chì vẽ: trang 0–0,35 s, lần viền ~0,7–1,7 s, gạch chì ~1,7–2,4 s, bút chì màu tô ~2,4–4,1 s (2026-11-25),
                // bật ra + sao ~4,2 s, chữ ~4,5 s, nút ~4,8 s. Chụp dày hơn: HeroUnlockShots (Temp/unlock_shots.flag)
                float[] at = { 0.6f, 1.0f, 1.4f, 1.9f, 2.6f, 3.2f, 3.8f, 4.4f, 6.0f };
                float t0 = Time.realtimeSinceStartup;
                foreach (var a in at)
                {
                    while (Time.realtimeSinceStartup - t0 < a) yield return null;
                    yield return new WaitForEndOfFrame();
                    var tex = ScreenCapture.CaptureScreenshotAsTexture();
                    File.WriteAllBytes(Path.Combine(dir, $"{n++:00}_bac{r}_{a:0.00}s.jpg"), tex.EncodeToJPG(85));
                    Object.Destroy(tex);
                }
                var v = Object.FindAnyObjectByType<HeroUnlockView>();
                if (v) v.GetComponentsInChildren<SketchButton>().FirstOrDefault(b => b.name == "nut_tiep")?.SimulateClick();
                yield return new WaitForSecondsRealtime(0.5f);
            }
            Debug.Log($"[Cửa hàng] Màn mở khoá tướng: {n} ảnh ở {dir}");
        }

        // tour chụp: 4 tab, mua một gói bi (cửa hàng giả lập), mở Rương Tướng, các popup; xong trả trạng thái cửa hàng cũ
        [MenuItem("PokiClash/Thử/Cửa hàng/tour chụp (đang Play)", priority = 160)]
        static void Tour()
        {
            if (!Playing()) return;
            App.I.StartCoroutine(RunTour());
        }

        static string Dir => Path.Combine(PlayTour.ShotDir, "cua_hang");
        static int shot;

        static IEnumerator Shot(string name, float wait = 0.7f)
        {
            yield return new WaitForSecondsRealtime(wait);
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, $"{shot++:00}_{name}.jpg"), tex.EncodeToJPG(85));
            Object.Destroy(tex);
        }

        static IEnumerator RunTour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            shot = 0;
            // nở trứng cộng mảnh tướng vào bản lưu: sao lưu cả file, trả lại trong finally (memory tour-sao-luu-ban-luu)
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            try
            {
                App.Modals.CloseAll();
                S.shop = null;
                Prep();
                Shop.Of(S).AddItem(Eggs.Key(2), 3);
                Shop.Of(S).AddItem(Eggs.Key(4), 1);
                Shop.Grant(S, D, new System.Collections.Generic.List<ShopItem> { new ShopItem { k = Shop.Ticket, n = 1, r = 2 } }, Now, new Rng(1));
                Shop.Of(S).piggy = 900;
                Offers.Build(S, D, "flash", null, Now, new Rng(2));
                Shop.ChainStart(S, D.Cfg.shop, Now);
                App.Modals.CloseAll();
                ShopPage.Open();
                yield return Shot("trang_dau");
                foreach (var t in ShopPage.Sections)
                {
                    App.Modals.CloseAll();
                    ShopPage.Open(t);
                    yield return Shot("muc_" + t);
                }
                // mua Túi bi (cửa hàng giả lập mua ngay)
                App.Modals.CloseAll();
                ShopService.BuyPack("balls_1");
                yield return new WaitForSecondsRealtime(2.2f);
                yield return Shot("mua_tui_bi");
                // nở 1 trứng (chụp từng pha), rồi nở 3 trứng (chạy nhanh, bảng tổng)
                App.Modals.CloseAll();
                ShopService.HatchEggs(4, 1);
                yield return Shot("no_trung_roi", 0.3f);
                yield return Shot("no_trung_lac", 0.5f);
                yield return Shot("no_trung_bat", 0.6f);
                yield return Shot("no_trung_hien", 0.9f);
                while (EggHatchView.Playing)
                {
                    Object.FindAnyObjectByType<EggHatchView>()?.GetComponentInChildren<Button>()?.onClick.Invoke();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                ShopService.HatchEggs(2, 3);
                yield return Shot("no_3_trung_dang_no", 1.0f);
                yield return new WaitForSecondsRealtime(4f);
                yield return Shot("no_3_trung_bang_tong");
                var hv = Object.FindAnyObjectByType<EggHatchView>();
                if (hv) hv.GetComponentsInChildren<SketchButton>().FirstOrDefault(b => b.name == "nut_nhan")?.SimulateClick();
                yield return new WaitForSecondsRealtime(0.6f);
                App.Modals.CloseAll();
                foreach (var p in new[]
                         {
                             new Popup { kind = "refill", free = true }, new Popup { kind = "piggy", free = true }, new Popup { kind = "chain", free = true },
                             new Popup { kind = "offer", id = S.shop.offers.active.Find(o => o.tpl == "flash").uid, key = "flash" },
                             new Popup { kind = "offer", id = Offers.Build(S, D, "relief", null, Now, new Rng(3)).uid, key = "relief" },
                             new Popup { kind = "offer", id = S.shop.offers.active.Find(o => o.pack == "starter3").uid, key = "starter3" },
                             new Popup { kind = "intro", id = "fund", key = "intro_fund" },
                         })
                {
                    App.Modals.CloseAll();
                    ShopSheet.OpenPopup(p, null);
                    yield return Shot("popup_" + p.kind + (p.key != null ? "_" + p.key : ""));
                }
                App.Modals.CloseAll();
                Debug.Log($"[Cửa hàng] Tour chụp xong: {shot} ảnh ở {Dir}");
            }
            finally
            {
                App.Modals.CloseAll();
                foreach (var v in Object.FindObjectsByType<EggHatchView>(FindObjectsSortMode.None)) Object.Destroy(v.gameObject);
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                    Debug.Log(File.ReadAllText(path) == backup ? "[Cửa hàng] Đã trả bản lưu cũ (đọc lại khớp)." : "[Cửa hàng] CẢNH BÁO: bản lưu đọc lại không khớp bản sao lưu.");
                }
            }
        }
    }
}
