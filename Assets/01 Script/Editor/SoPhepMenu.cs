// Dựng prefab Sổ Phép (Core/SoPhep.cs, GD_Claude/28_SoPhep.md, người dùng duyệt 2026-11-24), menu "PokiClash/Prefab/Hộp thoại và màn/Sổ Phép":
// - Items/OSoPhep (SoPhepTile): viền chọn (mực, sau khung), khung giấy, icon, tên, cấp, giá, dấu tích; ClickCatcher cả ô;
// - Dialogs/SoPhep (SoPhepDialog): biến thể tờ giấy gốc HopThoai trải kín màn như cửa hàng (tràn quá mép giấu viền, bỏ băng keo, chữ
//   và nút trong khung an_toan SafeArea): đầu màn (tên, nét, đá, đã vẽ), trang cuộn dọc 4 chương × 5 ô đặt sẵn (hai ô, hai ô, ô chốt,
//   nối bằng nét mực), bảng đáy cố định (tên ô, hiệu ứng, 5 nút mặt, giá, Gợi ý / Vẽ / Tẩy sổ); gắn vào UiKit.dialogs;
// - vá Screens/Battle: nút "Lật trang" ở đầu hàng thẻ, bên trái chip "Chọn" (BattleView.p.reroll);
// - vá Screens/Hub: icon "pencil" cho thẻ công trình thứ 4 (Sổ Phép, thay chỗ Cây bi đã ẩn).
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using static PokiClash.EditorTools.ShopMenu;

namespace PokiClash.EditorTools
{
    public static class SoPhepMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string TilePath = "Assets/04 Prefabs/Items/OSoPhep.prefab";
        const string DialogPath = "Assets/04 Prefabs/Dialogs/SoPhep.prefab";
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const float TileW = 420, TileH = 168, RowGap = 206, ColX = 236;
        const float HeaderH = 118, InfoH = 70, PanelH = 500, Bleed = 30;
        const float ChapterTop = 118, ChapterH = ChapterTop + 2 * RowGap + TileH + 70;

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Sổ Phép", priority = 72)]
        public static void BuildAll()
        {
            var tile = BuildTile();
            BuildDialog(tile);
            PatchBattle();
            PatchHub();
            AssetDatabase.SaveAssets();
            Debug.Log("[Sổ Phép] Đã dựng " + TilePath + ", " + DialogPath + ", vá nút Lật trang (Battle), icon Sổ Phép (Hub)");
        }

        static SoPhepTile BuildTile()
        {
            var (titleTpl, hintTpl) = Templates();
            var root = Rt("OSoPhep", null, typeof(CanvasRenderer), typeof(Image), typeof(ClickCatcher)).gameObject;
            try
            {
                var rt = (RectTransform)root.transform;
                rt.sizeDelta = new Vector2(TileW, TileH);
                var hit = root.GetComponent<Image>();
                hit.color = new Color(1, 1, 1, 0); // nhận chạm cả ô
                var frame = Img("vien_chon", rt, Sketch.Panel, Theme.Ink);
                frame.type = Image.Type.Sliced;
                frame.rectTransform.Stretch(-9, -9, -9, -9);
                var bg = Img("nen", rt, Sketch.Panel, Theme.CardFill);
                bg.type = Image.Type.Sliced;
                bg.rectTransform.Stretch();
                var icon = Img("icon", rt, Icon("pencil"), Color.white);
                icon.preserveAspect = true;
                icon.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(22, 0), new Vector2(104, 104), new Vector2(0, 0.5f));
                var title = Text(titleTpl, rt, "ten", 36, TextAlignmentOptions.MidlineLeft, Theme.Ink);
                title.rectTransform.Place(new Vector2(0, 1), new Vector2(140, -20), new Vector2(TileW - 160, 56), new Vector2(0, 1));
                title.enableAutoSizing = true;
                title.fontSizeMin = 24;
                title.fontSizeMax = 36;
                title.textWrappingMode = TextWrappingModes.NoWrap;
                var level = Text(hintTpl, rt, "cap", 28, TextAlignmentOptions.MidlineRight, Theme.Ink2);
                level.rectTransform.Place(new Vector2(1, 0), new Vector2(-20, 18), new Vector2(90, 40), new Vector2(1, 0));
                var price = Text(hintTpl, rt, "gia", 30, TextAlignmentOptions.MidlineLeft, Theme.Ink);
                price.rectTransform.Place(new Vector2(0, 0), new Vector2(140, 18), new Vector2(TileW - 250, 44), new Vector2(0, 0));
                price.textWrappingMode = TextWrappingModes.NoWrap;
                var tick = Img("da_ve", rt, Icon("check"), Color.white);
                tick.preserveAspect = true;
                tick.rectTransform.Place(new Vector2(1, 1), new Vector2(10, 14), new Vector2(64, 64), new Vector2(1, 1));
                foreach (var g in root.GetComponentsInChildren<Graphic>(true))
                    if (g != hit) g.raycastTarget = false;
                var t = root.AddComponent<SoPhepTile>();
                t.Setup(bg, icon, tick, frame, title, level, price, root.GetComponent<ClickCatcher>());
                return PrefabUtility.SaveAsPrefabAsset(root, TilePath).GetComponent<SoPhepTile>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static void BuildDialog(SoPhepTile tilePrefab)
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "SoPhep";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(1080, false, true);
                var sheet = view.Sheet;
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
                var body = Rt("an_toan", page, typeof(SafeArea));
                body.Stretch();
                var cr = (RectTransform)view.Close.transform;
                cr.anchorMin = cr.anchorMax = new Vector2(1, 1);
                cr.pivot = new Vector2(0.5f, 0.5f);
                cr.anchoredPosition = new Vector2(-Bleed - 64, -Bleed - HeaderH / 2);

                // đầu màn
                var title = Text(titleTpl, body, "tieu_de", 62, TextAlignmentOptions.MidlineLeft, Theme.Ink);
                title.rectTransform.Place(new Vector2(0, 1), new Vector2(44, -14), new Vector2(560, HeaderH - 20), new Vector2(0, 1));
                title.text = "Sổ Phép";
                var points = Chip(body, titleTpl, "net", new Vector2(44, -HeaderH - 4), 250, Icon("pencil"));
                var stones = Chip(body, titleTpl, "da", new Vector2(310, -HeaderH - 4), 330, Icon("shard"));
                var progress = Text(hintTpl, body, "da_ve", 30, TextAlignmentOptions.MidlineRight, Theme.Ink2);
                progress.rectTransform.Place(new Vector2(1, 1), new Vector2(-40, -HeaderH - 4), new Vector2(360, 60), new Vector2(1, 1));
                progress.textWrappingMode = TextWrappingModes.NoWrap;

                // trang cuộn
                var scrollGo = Rt("cuon", body, typeof(CanvasRenderer), typeof(Image), typeof(ScrollRect)).gameObject;
                var srt = (RectTransform)scrollGo.transform;
                srt.Stretch(0, HeaderH + InfoH + 10, 0, PanelH);
                scrollGo.GetComponent<Image>().color = new Color(1, 1, 1, 0);
                var scroll = scrollGo.GetComponent<ScrollRect>();
                scroll.horizontal = false;
                scroll.vertical = true;
                scroll.movementType = ScrollRect.MovementType.Elastic;
                scroll.scrollSensitivity = 30;
                var viewport = Rt("khung", scrollGo.transform, typeof(RectMask2D));
                viewport.Stretch();
                var content = Rt("trang", viewport);
                content.anchorMin = new Vector2(0, 1);
                content.anchorMax = new Vector2(1, 1);
                content.pivot = new Vector2(0.5f, 1);
                content.anchoredPosition = Vector2.zero;
                content.sizeDelta = new Vector2(0, SoPhepDialog.Chapters * ChapterH + 40);
                scroll.viewport = viewport;
                scroll.content = content;

                int n = SoPhepDialog.Chapters;
                var chTitles = new TextMeshProUGUI[n];
                var chNeeds = new TextMeshProUGUI[n];
                var chGroups = new CanvasGroup[n];
                var tiles = new SoPhepTile[n * SoPhepDialog.PerChapter];
                for (int ch = 0; ch < n; ch++)
                {
                    var block = Rt("chuong_" + (ch + 1), content);
                    block.anchorMin = new Vector2(0, 1);
                    block.anchorMax = new Vector2(1, 1);
                    block.pivot = new Vector2(0.5f, 1);
                    block.anchoredPosition = new Vector2(0, -20 - ch * ChapterH);
                    block.sizeDelta = new Vector2(0, ChapterH);
                    var ct = Text(titleTpl, block, "ten_chuong", 44, TextAlignmentOptions.MidlineLeft, Theme.Ink);
                    ct.rectTransform.Place(new Vector2(0, 1), new Vector2(44, -6), new Vector2(980, 60), new Vector2(0, 1));
                    ct.textWrappingMode = TextWrappingModes.NoWrap;
                    var need = Text(hintTpl, block, "dieu_kien", 30, TextAlignmentOptions.MidlineLeft, Theme.RedD);
                    need.rectTransform.Place(new Vector2(0, 1), new Vector2(46, -64), new Vector2(980, 44), new Vector2(0, 1));
                    need.fontStyle = FontStyles.Italic;
                    var group = Rt("o_chuong", block, typeof(CanvasGroup));
                    group.Stretch(0, ChapterTop, 0, 0);
                    // nét mực nối: hai ô hàng 1 → hai ô hàng 2 → ô chốt
                    for (int k = 0; k < 2; k++)
                    {
                        float x = k == 0 ? -ColX : ColX;
                        Line(group, new Vector2(x, -TileH), new Vector2(x, -RowGap));
                        Line(group, new Vector2(x, -RowGap - TileH), new Vector2(0, -2 * RowGap));
                    }
                    var pos = new[]
                    {
                        new Vector2(-ColX, 0), new Vector2(ColX, 0), new Vector2(-ColX, -RowGap), new Vector2(ColX, -RowGap), new Vector2(0, -2 * RowGap),
                    };
                    for (int j = 0; j < SoPhepDialog.PerChapter; j++)
                    {
                        var t = ((GameObject)PrefabUtility.InstantiatePrefab(tilePrefab.gameObject, group)).GetComponent<SoPhepTile>();
                        t.name = "o_" + (j + 1);
                        t.Rect.Place(new Vector2(0.5f, 1), pos[j], new Vector2(TileW, TileH), new Vector2(0.5f, 1));
                        tiles[ch * SoPhepDialog.PerChapter + j] = t;
                    }
                    chTitles[ch] = ct;
                    chNeeds[ch] = need;
                    chGroups[ch] = group.GetComponent<CanvasGroup>();
                }

                // bảng đáy cố định
                var panel = Img("bang_day", body, Sketch.Panel, Theme.Paper2);
                panel.type = Image.Type.Sliced;
                var prt = panel.rectTransform;
                prt.anchorMin = new Vector2(0, 0);
                prt.anchorMax = new Vector2(1, 0);
                prt.pivot = new Vector2(0.5f, 0);
                prt.offsetMin = new Vector2(16, 10);
                prt.offsetMax = new Vector2(-16, PanelH - 10);
                var selName = Text(titleTpl, prt, "ten_o", 48, TextAlignmentOptions.MidlineLeft, Theme.Ink);
                selName.rectTransform.Place(new Vector2(0, 1), new Vector2(34, -18), new Vector2(980, 66), new Vector2(0, 1));
                selName.textWrappingMode = TextWrappingModes.NoWrap;
                var selDesc = Text(hintTpl, prt, "hieu_ung", 32, TextAlignmentOptions.TopLeft, Theme.Ink2);
                selDesc.rectTransform.Place(new Vector2(0, 1), new Vector2(34, -88), new Vector2(980, 110), new Vector2(0, 1));
                selDesc.enableAutoSizing = true;
                selDesc.fontSizeMin = 22;
                selDesc.fontSizeMax = 32;
                var facesRow = Rt("mat", prt, typeof(HorizontalLayoutGroup));
                facesRow.Place(new Vector2(0.5f, 1), new Vector2(0, -206), new Vector2(1000, 76), new Vector2(0.5f, 1));
                var hl = facesRow.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 10;
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var faces = new SketchButton[SoPhepDialog.MaxFaces];
                for (int i = 0; i < faces.Length; i++)
                {
                    var b = Ui.Spawn(kit.buttonSmall, facesRow);
                    b.name = "mat_" + i;
                    b.Rect.sizeDelta = new Vector2(186, b.Rect.sizeDelta.y);
                    b.SetText("");
                    b.SetRole(BtnColor.Paper);
                    faces[i] = b;
                }
                var selCost = Text(hintTpl, prt, "gia", 32, TextAlignmentOptions.Center, Theme.Ink);
                selCost.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -292), new Vector2(980, 48), new Vector2(0.5f, 1));
                selCost.enableAutoSizing = true;
                selCost.fontSizeMin = 22;
                selCost.fontSizeMax = 32;
                var suggest = Ui.Spawn(kit.buttonSmall, prt);
                suggest.name = "nut_goi_y";
                suggest.Rect.Place(new Vector2(0, 0), new Vector2(34, 30), new Vector2(220, suggest.Rect.sizeDelta.y), new Vector2(0, 0));
                suggest.SetRole(BtnColor.Paper);
                suggest.SetText("Gợi ý");
                var draw = Ui.Spawn(kit.buttonNormal, prt);
                draw.name = "nut_ve";
                draw.Rect.Place(new Vector2(0.5f, 0), new Vector2(0, 24), new Vector2(340, draw.Rect.sizeDelta.y), new Vector2(0.5f, 0));
                draw.SetRole(BtnColor.Green);
                draw.SetText("Vẽ");
                var reset = Ui.Spawn(kit.buttonSmall, prt);
                reset.name = "nut_tay_so";
                reset.Rect.Place(new Vector2(1, 0), new Vector2(-34, 30), new Vector2(220, reset.Rect.sizeDelta.y), new Vector2(1, 0));
                reset.SetRole(BtnColor.Red);
                reset.SetText("Tẩy sổ");

                view.Close.transform.SetAsLastSibling();
                var dlgComp = root.AddComponent<SoPhepDialog>();
                dlgComp.Setup(new SoPhepDialog.Parts
                {
                    points = points, stones = stones, progress = progress, scroll = scroll, chapterTitles = chTitles, chapterNeeds = chNeeds,
                    chapterGroups = chGroups, tiles = tiles, selName = selName, selDesc = selDesc, selCost = selCost, faces = faces,
                    draw = draw, suggest = suggest, reset = reset, icons = NodeIcons(),
                });
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, DialogPath).GetComponent<SoPhepDialog>();
                kit.dialogs.RemoveAll(x => !x || (x is SoPhepDialog && x != dlg));
                if (!kit.dialogs.Contains(dlg)) kit.dialogs.Add(dlg);
                EditorUtility.SetDirty(kit);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // icon vẽ riêng của từng ô theo thứ tự ô trong balance.json (03 Art/SoPhep/<id>.png, gen bằng GPT qua Magnific: ArtGen/UI/so_phep)
        static Sprite[] NodeIcons()
        {
            var json = System.IO.File.ReadAllText(System.IO.Path.Combine(Application.dataPath, "02 Data/Json/balance.json"));
            var cfg = PokiClash.Core.BalanceConfig.FromJson(PokiClash.Core.J.Obj(PokiClash.Core.MiniJson.Parse(json)));
            return cfg.sophep.nodes.Select(n => AssetDatabase.LoadAllAssetsAtPath($"Assets/03 Art/SoPhep/{n.id}.png").OfType<Sprite>().FirstOrDefault()).ToArray();
        }

        // ô số liệu nhỏ ở đầu màn: viên giấy, icon, chữ
        static TextMeshProUGUI Chip(RectTransform parent, TextMeshProUGUI tpl, string name, Vector2 pos, float w, Sprite icon)
        {
            var chip = Img(name, parent, Sketch.Pill, Theme.Paper2);
            chip.type = Image.Type.Sliced;
            chip.rectTransform.Place(new Vector2(0, 1), pos, new Vector2(w, 60), new Vector2(0, 1));
            var ic = Img("icon", chip.transform, icon, Color.white);
            ic.preserveAspect = true;
            ic.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(8, 0), new Vector2(50, 50), new Vector2(0, 0.5f));
            var t = Text(tpl, chip.transform, "so", 30, TextAlignmentOptions.MidlineLeft, Theme.Ink);
            t.rectTransform.Stretch(64, 2, 14, 2);
            t.textWrappingMode = TextWrappingModes.NoWrap;
            return t;
        }

        // nét mực nối hai điểm (toạ độ trong khối ô, gốc giữa trên)
        static void Line(RectTransform parent, Vector2 a, Vector2 b)
        {
            var img = Img("net", parent, null, new Color(Theme.Ink.r, Theme.Ink.g, Theme.Ink.b, 0.55f));
            var rt = img.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            var d = b - a;
            rt.anchoredPosition = (a + b) / 2;
            rt.sizeDelta = new Vector2(d.magnitude, 5);
            rt.localEulerAngles = new Vector3(0, 0, Mathf.Atan2(d.y, d.x) * Mathf.Rad2Deg);
        }

        static void PatchBattle()
        {
            var kit = Kit;
            var contents = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var view = contents.GetComponentInChildren<BattleView>(true);
                var so = new SerializedObject(view);
                var qCount = (TextMeshProUGUI)so.FindProperty("p.qCount").objectReferenceValue;
                var qHead = (RectTransform)so.FindProperty("p.qHead").objectReferenceValue;
                if (!qCount || !qHead)
                {
                    Debug.LogError("[Sổ Phép] Không thấy p.qCount / p.qHead trong " + BattlePath);
                    return;
                }
                var old = qHead.Find("nut_lat_trang");
                if (old) Object.DestroyImmediate(old.gameObject);
                // chip "Chọn" có thể là chữ trong một viên: lấy khung ngoài cùng nằm trong qHead
                RectTransform chip = qCount.rectTransform;
                while (chip.parent && chip.parent != qHead) chip = (RectTransform)chip.parent;
                var btn = Ui.Spawn(kit.buttonSmall, qHead);
                btn.name = "nut_lat_trang";
                var brt = btn.Rect;
                brt.anchorMin = chip.anchorMin;
                brt.anchorMax = chip.anchorMax;
                brt.pivot = new Vector2(1, 0.5f);
                float left = chip.anchoredPosition.x - chip.rect.width * chip.pivot.x;
                float midY = chip.anchoredPosition.y + chip.rect.height * (0.5f - chip.pivot.y);
                brt.sizeDelta = new Vector2(250, Mathf.Max(56, chip.rect.height + 4));
                brt.anchoredPosition = new Vector2(left - 14, midY);
                btn.SetRole(BtnColor.Orange);
                btn.SetText("Lật trang ×1");
                btn.gameObject.SetActive(false);
                so.FindProperty("p.reroll").objectReferenceValue = btn;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, BattlePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        static void PatchHub()
        {
            var contents = PrefabUtility.LoadPrefabContents(HubPath);
            try
            {
                var hub = contents.GetComponentInChildren<HubScene>(true);
                var so = new SerializedObject(hub);
                var arr = so.FindProperty("buildings");
                if (arr == null || arr.arraySize < 4)
                {
                    Debug.LogError("[Sổ Phép] Hub không có đủ 4 thẻ công trình");
                    return;
                }
                var b = (HubBuilding)arr.GetArrayElementAtIndex(3).objectReferenceValue;
                if (!b) return;
                b.SetIcon(Icon("pencil"));
                EditorUtility.SetDirty(b);
                PrefabUtility.SaveAsPrefabAsset(contents, HubPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
