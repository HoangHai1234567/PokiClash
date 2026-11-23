// Cửa hàng (GD_Claude/26_CuaHang_IAP_QuangCao.md), menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết" (chạy lại được):
// - Items/OGoi: ô gói (PackCell): tờ giấy mỏng, cột trái tên / mô tả / lưới món (ô thưởng Items/OThuong thu nhỏ) / ghi chú, góc phải nhãn
//   giá trị (dấu đỏ kit), đồng hồ, hai nút (kit), dấu "Đã mua";
// - Dialogs/CuaHang: tờ cửa hàng / popup (ShopSheet, biến thể tờ giấy gốc HopThoai dính mép trên): tiêu đề, dòng phụ, hàng 4 tab có chấm
//   đỏ, danh sách cuộn, nút "Hôm nay không hiện nữa"; thêm vào UiKit;
// - App.prefab: component OfferHost (máy hiện popup ưu đãi);
// - Dialogs/TranKetQua: nút quảng cáo riêng "hang_qc" dưới lời khuyên (BattleResultDialog.adButton: Tiếp sức / Nhận ×2);
// - Screens/Hub: nhóm "cua_hang_san" mép trái dưới thanh trên (HubShop: nút Lọ Bi, 3 bong bóng ưu đãi). Nút Cửa hàng ở hàng nút đáy.
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

        // ---------- ô gói ----------

        static PackCell BuildCell()
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var tile = AssetDatabase.LoadAssetAtPath<GameObject>(ChestPath).GetComponent<ChestDialog>().TilePrefab;
            var root = Rt("OGoi", null, typeof(CanvasRenderer), typeof(Image), typeof(LayoutElement)).gameObject;
            try
            {
                var rt = (RectTransform)root.transform;
                rt.sizeDelta = new Vector2(920, 220);
                var card = root.GetComponent<Image>();
                Theme.SetSprite(card, Sketch.PanelThin);
                card.type = Image.Type.Sliced;
                card.color = Theme.Paper;
                card.raycastTarget = false;
                var layout = root.GetComponent<LayoutElement>();
                layout.preferredHeight = 220;
                layout.minHeight = 200;

                // cột trái: tên, mô tả, lưới món, ghi chú
                var left = Rt("trai", root.transform, typeof(VerticalLayoutGroup));
                left.anchorMin = new Vector2(0, 0);
                left.anchorMax = new Vector2(0, 1);
                left.pivot = new Vector2(0, 1);
                left.offsetMin = new Vector2(26, 14);
                left.offsetMax = new Vector2(26 + 600, -16);
                var vl = left.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 6;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = vl.childForceExpandHeight = false;
                var title = Text(titleTpl, left, "ten", 34, TextAlignmentOptions.MidlineLeft, Theme.Ink);
                Le(title, 46);
                var desc = Text(hintTpl, left, "mo_ta", 23, TextAlignmentOptions.TopLeft, Theme.Ink2);
                Le(desc, 58);
                var items = Rt("mon", left, typeof(GridLayoutGroup), typeof(LayoutElement));
                items.pivot = new Vector2(0, 1);
                items.localScale = Vector3.one * PackCell.ItemScale;
                var grid = items.GetComponent<GridLayoutGroup>();
                grid.cellSize = new Vector2(RewardTile.W, RewardTile.H);
                grid.spacing = new Vector2(12, 24);
                grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
                grid.constraintCount = 5;
                grid.startCorner = GridLayoutGroup.Corner.UpperLeft;
                grid.childAlignment = TextAnchor.UpperLeft;
                var ile = items.GetComponent<LayoutElement>();
                ile.preferredHeight = (RewardTile.H + 24) * PackCell.ItemScale;
                ile.preferredWidth = (5 * RewardTile.W + 4 * 12);
                var note = Text(hintTpl, left, "ghi_chu", 24, TextAlignmentOptions.MidlineLeft, Theme.Ink2);
                Le(note, 34);

                // góc phải: nhãn giá trị, đồng hồ, hai nút, dấu đã mua
                var value = Ui.Spawn(kit.stamp, root.transform);
                value.name = "gia_tri";
                var vr = (RectTransform)value.transform;
                vr.anchorMin = vr.anchorMax = vr.pivot = new Vector2(1, 1);
                vr.anchoredPosition = new Vector2(-14, -10);
                vr.localEulerAngles = new Vector3(0, 0, 5);
                vr.localScale = Vector3.one * 0.4f; // dấu kit cỡ con dấu hộp kết quả trận: thu nhỏ thành nhãn góc ô
                var timer = Text(hintTpl, root.transform, "dong_ho", 26, TextAlignmentOptions.MidlineRight, Theme.Ink2);
                timer.rectTransform.Place(new Vector2(1, 1), new Vector2(-26, -82), new Vector2(270, 36));
                var buy = Ui.Spawn(kit.buttonNormal, root.transform);
                buy.name = "nut_mua";
                var br = buy.Rect;
                br.anchorMin = br.anchorMax = br.pivot = new Vector2(1, 0);
                br.anchoredPosition = new Vector2(-22, 18);
                br.sizeDelta = new Vector2(250, br.sizeDelta.y);
                var extra = Ui.Spawn(kit.buttonSmall, root.transform);
                extra.name = "nut_phu";
                var er = extra.Rect;
                er.anchorMin = er.anchorMax = er.pivot = new Vector2(1, 0);
                er.anchoredPosition = new Vector2(-22, 18 + br.sizeDelta.y + 12);
                er.sizeDelta = new Vector2(250, er.sizeDelta.y);
                var done = Text(titleTpl, root.transform, "da_mua", 38, TextAlignmentOptions.Center, Theme.GreenD);
                done.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-30, -10), new Vector2(280, 70), new Vector2(1, 0.5f));
                done.rectTransform.localEulerAngles = new Vector3(0, 0, 8);

                foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                    if (!gr.transform.IsChildOf(buy.transform) && !gr.transform.IsChildOf(extra.transform)) gr.raycastTarget = false;

                root.AddComponent<PackCell>().Setup(new PackCell.Parts
                {
                    card = card, title = title, desc = desc, timer = timer, note = note, done = done, items = items, value = value, buy = buy, extra = extra,
                    layout = layout,
                }, tile);
                return PrefabUtility.SaveAsPrefabAsset(root, CellPath).GetComponent<PackCell>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- tờ cửa hàng / popup ----------

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
                var content = Rt("noi_dung", sheet, typeof(VerticalLayoutGroup));
                var vl = content.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 10;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = true;
                vl.childForceExpandHeight = false;

                var title = Text(titleTpl, content, "tieu_de", 60, TextAlignmentOptions.Center, Theme.Ink);
                Le(title, 74);
                var sub = Text(hintTpl, content, "dong_phu", 28, TextAlignmentOptions.Center, Theme.Ink2);
                Le(sub, 42);

                // hàng tab
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
                    var dot = Img("cham_do", b.transform, Sketch.Dot, Theme.Red);
                    dot.rectTransform.Place(new Vector2(1, 1), new Vector2(-6, -6), new Vector2(26, 26), new Vector2(0.5f, 0.5f));
                    dot.gameObject.SetActive(false);
                    tabs[i] = b;
                    dots[i] = dot.gameObject;
                }

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
                lvl.spacing = 14;
                lvl.padding = new RectOffset(6, 6, 4, 16);
                lvl.childControlWidth = lvl.childControlHeight = true;
                lvl.childForceExpandWidth = true;
                lvl.childForceExpandHeight = false;
                list.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                scroll.viewport = viewport;
                scroll.content = list;

                // "Hôm nay không hiện nữa"
                var muteRow = Rt("hang_tat", content, typeof(LayoutElement));
                Le(muteRow, 84);
                var mute = Ui.Spawn(kit.buttonSmall, muteRow);
                mute.name = "nut_tat_hom_nay";
                var mr = mute.Rect;
                mr.anchorMin = mr.anchorMax = mr.pivot = new Vector2(0.5f, 0.5f);
                mr.anchoredPosition = Vector2.zero;
                mr.sizeDelta = new Vector2(560, mr.sizeDelta.y);
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

        // ---------- sảnh: Lọ Bi, bong bóng ưu đãi ----------

        static void BuildHub()
        {
            var kit = Kit;
            var (_, hintTpl) = Templates();
            var contents = PrefabUtility.LoadPrefabContents(HubPath);
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
                holder.anchoredPosition = new Vector2(18, -240);
                holder.sizeDelta = new Vector2(170, 640);
                var group = Rt("nhom", holder);
                group.Stretch();

                // Lọ Bi: nút tròn icon bi, thanh dưới
                var piggy = Ui.Spawn(kit.buttonRound, group);
                piggy.name = "nut_lo_bi";
                piggy.SetText("");
                var pr = piggy.Rect;
                pr.anchorMin = pr.anchorMax = pr.pivot = new Vector2(0.5f, 1);
                pr.anchoredPosition = new Vector2(0, 0);
                pr.sizeDelta = new Vector2(132, 132);
                var picon = Img("icon", piggy.transform, Icon("ball"), Color.white);
                picon.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 6), new Vector2(76, 76));
                picon.preserveAspect = true;
                var track = Img("thanh", group, Sketch.BarTrack, Theme.Paper3);
                track.type = Image.Type.Sliced;
                track.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -136), new Vector2(140, 34), new Vector2(0.5f, 1));
                var fill = Img("day", track.transform, Sketch.BarFill, Theme.Yellow);
                fill.type = Image.Type.Filled;
                fill.fillMethod = Image.FillMethod.Horizontal;
                fill.rectTransform.Stretch(4, 4, 4, 4);
                var ptext = Text(hintTpl, track.transform, "so", 22, TextAlignmentOptions.Center, Theme.Ink);
                ptext.rectTransform.Stretch();
                var plabel = Text(hintTpl, group, "nhan_lo_bi", 22, TextAlignmentOptions.Center, Theme.Ink);
                plabel.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -172), new Vector2(170, 30), new Vector2(0.5f, 1));
                plabel.text = "Lọ Bi";

                // 3 bong bóng ưu đãi
                var bubs = new HubShop.Bubble[3];
                for (int i = 0; i < 3; i++)
                {
                    var b = Ui.Spawn(kit.buttonRound, group);
                    b.name = "bong_bong_" + (i + 1);
                    b.SetText("");
                    b.SetRole(BtnColor.Yellow);
                    var r = b.Rect;
                    r.anchorMin = r.anchorMax = r.pivot = new Vector2(0.5f, 1);
                    r.anchoredPosition = new Vector2(0, -220 - i * 140);
                    r.sizeDelta = new Vector2(112, 112);
                    var ic = Img("icon", b.transform, Icon("coin"), Color.white);
                    ic.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 8), new Vector2(60, 60));
                    ic.preserveAspect = true;
                    var pill = Img("nen_gio", b.transform, Sketch.Pill, Theme.Paper);
                    pill.type = Image.Type.Sliced;
                    pill.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, -14), new Vector2(124, 36), new Vector2(0.5f, 0));
                    var t = Text(hintTpl, pill.transform, "gio", 22, TextAlignmentOptions.Center, Theme.Ink);
                    t.rectTransform.Stretch();
                    b.gameObject.SetActive(false);
                    bubs[i] = new HubShop.Bubble { button = b, icon = ic, timer = t };
                }
                holder.gameObject.AddComponent<HubShop>().Setup(group.gameObject, null, null, piggy, fill, ptext, bubs);
                PrefabUtility.SaveAsPrefabAsset(contents, HubPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
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
                float[] at = { 0.45f, 0.9f, 1.25f, 1.33f, 1.6f, 2.6f, 4.2f };
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
