// Dựng màn chọn tướng khởi đầu Dialogs/ChonTuongKhoiDau (StarterDialog, GD_Claude/15_TuongKhoiDau.md). Người dùng 2026-11-24: nền đen
// trải kín màn, 5 tướng xếp vòng tròn 3D theo độ sâu (5 ô xem tướng Items/OXemTuong có animation), vùng vuốt trên vòng; dưới vòng: hệ
// + tên, hệ · vai, danh hiệu, 3 dòng chỉ số (chữ, 5 nấc, số), Lực chiến, nút "Chọn …". Biến thể tờ giấy gốc HopThoai: tờ trải kín màn,
// tắt mọi hình giấy, nền tối thành đen. Chữ chép từ hộp Chuẩn bị trận (phông). Thêm vào danh sách hộp của UiKit
// (App.Modals.Open<StarterDialog>). Chạy lại thì dựng lại; chữ đặt sẵn trong prefab để trống (lúc chạy điền), trừ chữ cố định.
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class StarterDialogMenu
    {
        const string SheetPath = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const string ViewerPath = "Assets/04 Prefabs/Items/OXemTuong.prefab";
        const string OutPath = "Assets/04 Prefabs/Dialogs/ChonTuongKhoiDau.prefab";

        static readonly Color Black = new Color(0.035f, 0.03f, 0.028f, 1);
        static readonly Color Cream = Theme.Paper;
        static readonly Color Muted = new Color(0.72f, 0.67f, 0.58f, 1);
        static readonly Color Gold = new Color(1f, 0.83f, 0.38f, 1);

        // mép trên vòng (chân con đứng trước) và vùng vuốt, so với giữa màn (khung 1080 × 1920)
        const float RingY = 220;

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Hộp chọn tướng khởi đầu (ChonTuongKhoiDau)", priority = 65)]
        static void Build()
        {
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));
            var prep = AssetDatabase.LoadAssetAtPath<GameObject>(PrepPath).GetComponent<StagePrepDialog>();
            var pso = new SerializedObject(prep);
            var titleTpl = (TextMeshProUGUI)pso.FindProperty("p.title").objectReferenceValue;
            var hintTpl = (TextMeshProUGUI)pso.FindProperty("p.hint").objectReferenceValue;
            var viewerPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(ViewerPath);
            if (!viewerPrefab || !viewerPrefab.GetComponent<HeroViewer>())
            {
                Debug.LogError("[Tướng khởi đầu] Không thấy " + ViewerPath + " (HeroViewer).");
                return;
            }

            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetPath));
            try
            {
                root.name = "ChonTuongKhoiDau";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(1080, true, false);
                var sheet = view.Sheet;
                // tờ trải kín màn, không nghiêng; tắt mọi hình giấy (nền giấy, lưới, đường khâu, băng keo), nền tối thành đen
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                sheet.anchorMin = Vector2.zero;
                sheet.anchorMax = Vector2.one;
                sheet.pivot = new Vector2(0.5f, 0.5f);
                sheet.offsetMin = sheet.offsetMax = Vector2.zero;
                view.SetFlat(true);
                foreach (var g in root.GetComponentsInChildren<Graphic>(true))
                {
                    bool keep = g.transform.IsChildOf(view.Close.transform) || g.gameObject == view.Dim.gameObject ||
                                (view.Catcher && g.gameObject == view.Catcher.gameObject);
                    if (!keep) g.enabled = false;
                }
                view.Dim.color = Black;

                var body = Rt("noi_dung", sheet);
                body.Stretch();
                body.SetAsLastSibling();

                // chữ tiêu đề của hộp Chuẩn bị mang vật liệu chữ mực sẫm (trên nền đen không thấy): mọi chữ dùng mẫu chữ gợi ý, tô kem
                var title = Txt(hintTpl, body, "tieu_de", new Vector2(0.5f, 1), new Vector2(0, -140), new Vector2(960, 90), 64, Cream);
                title.fontStyle = FontStyles.Bold;
                title.text = "Chọn bạn đồng hành";
                var hint = Txt(hintTpl, body, "goi_y", new Vector2(0.5f, 1), new Vector2(0, -248), new Vector2(960, 56), 36, Muted);
                hint.text = "Vuốt để xoay, chạm để chọn";

                // vòng: 5 ô gốc ở giữa đáy (chân), mỗi ô một CanvasGroup (tối dần theo độ sâu) và một ô xem tướng trải kín ô
                var ring = Rt("vong", body);
                ring.Place(new Vector2(0.5f, 0.5f), new Vector2(0, RingY), new Vector2(10, 10));
                int n = 5;
                var slots = new RectTransform[n];
                var viewers = new HeroViewer[n];
                var fades = new CanvasGroup[n];
                for (int i = 0; i < n; i++)
                {
                    var slot = Rt("o_tuong_" + i, ring);
                    slot.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(StarterDialog.ViewSize + 20, StarterDialog.ViewSize + 20),
                        new Vector2(0.5f, 0));
                    fades[i] = slot.gameObject.AddComponent<CanvasGroup>();
                    fades[i].blocksRaycasts = false; // vùng vuốt nhận chạm
                    var v = (GameObject)PrefabUtility.InstantiatePrefab(viewerPrefab, slot);
                    v.name = "xem_tuong";
                    // khung cắt của ô xem tướng (RectMask2D) tắt: trên vòng, đòn và chiêu được tràn ra ngoài ô
                    foreach (var m in v.GetComponentsInChildren<RectMask2D>(true)) m.enabled = false;
                    ((RectTransform)v.transform).Stretch();
                    slots[i] = slot;
                    viewers[i] = v.GetComponent<HeroViewer>();
                }

                // vùng vuốt trong suốt phủ dải vòng, nằm trên vòng
                var swipeImg = Img("vung_vuot", body, null, new Color(0, 0, 0, 0));
                swipeImg.raycastTarget = true;
                swipeImg.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, RingY + 170), new Vector2(1080, 680));
                var swipe = swipeImg.gameObject.AddComponent<SwipeArea>();

                // hệ + tên (biểu tượng hệ cạnh tên, căn giữa cả cụm)
                var nameRow = Rt("hang_ten", body);
                nameRow.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -60), new Vector2(960, 96));
                var hl = nameRow.gameObject.AddComponent<HorizontalLayoutGroup>();
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.spacing = 18;
                hl.childControlWidth = hl.childControlHeight = true;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var icon = Img("icon_he", nameRow, null, Color.white);
                icon.preserveAspect = true;
                var ile = icon.gameObject.AddComponent<LayoutElement>();
                ile.preferredWidth = ile.preferredHeight = 76;
                var name = Txt(hintTpl, nameRow, "ten", new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(700, 96), 70, Cream);
                name.fontStyle = FontStyles.Bold;
                name.enableAutoSizing = false;
                name.textWrappingMode = TextWrappingModes.NoWrap;
                name.text = "";

                var elem = Txt(hintTpl, body, "he_vai", new Vector2(0.5f, 0.5f), new Vector2(0, -140), new Vector2(960, 58), 42, Cream);
                elem.text = "";
                var tag = Txt(hintTpl, body, "danh_hieu", new Vector2(0.5f, 0.5f), new Vector2(0, -198), new Vector2(960, 50), 34, Muted);
                tag.fontStyle = FontStyles.Italic;
                tag.text = "";

                // 3 dòng chỉ số: chữ trái, 5 nấc bình hành nền trắng giữa (Máu xanh lá, Công đỏ, Thủ xanh dương), số phải
                var labels = StatPipsBuild.Labels;
                var rows = new StatPips[labels.Length];
                for (int k = 0; k < labels.Length; k++)
                {
                    var row = Rt("chi_so_" + k, body);
                    row.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -300 - 88 * k), new Vector2(820, 64));
                    var lab = Txt(hintTpl, row, "chu", new Vector2(0, 0.5f), new Vector2(0, 0), new Vector2(150, 64), 40, Cream, TextAlignmentOptions.MidlineLeft,
                        new Vector2(0, 0.5f));
                    lab.text = labels[k];
                    var val = Txt(hintTpl, row, "so", new Vector2(1, 0.5f), Vector2.zero, new Vector2(160, 64), 40, Cream, TextAlignmentOptions.MidlineRight,
                        new Vector2(1, 0.5f));
                    val.text = "";
                    rows[k] = StatPipsBuild.Add(row, k, 160, 46, 98, lab, val);
                }
                var power = Txt(hintTpl, body, "luc_chien", new Vector2(0.5f, 0.5f), new Vector2(0, -580), new Vector2(960, 56), 40, Gold);
                power.text = "";

                var pick = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonBig.gameObject, body)).GetComponent<SketchButton>();
                pick.name = "nut_Chon";
                pick.SetText("Chọn");
                pick.SetRole(BtnColor.Green);
                var prt = (RectTransform)pick.transform;
                prt.anchorMin = prt.anchorMax = new Vector2(0.5f, 0);
                prt.pivot = new Vector2(0.5f, 0);
                prt.anchoredPosition = new Vector2(0, 150);

                var dlgComp = root.GetComponent<StarterDialog>();
                if (!dlgComp) dlgComp = root.AddComponent<StarterDialog>();
                dlgComp.Setup(new StarterDialog.Parts
                {
                    ring = ring, slots = slots, viewers = viewers, fades = fades, swipe = swipe,
                    name = name, elem = elem, title = tag, power = power, elemIcon = icon, stats = rows, pick = pick,
                });
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, OutPath).GetComponent<StarterDialog>();
                // danh sách hộp của UiKit: bỏ chỗ trỏ cũ (đã mất hoặc bản cũ), thêm bản mới
                kit.dialogs.RemoveAll(x => !x || (x is StarterDialog && x != dlg));
                if (!kit.dialogs.Contains(dlg)) kit.dialogs.Add(dlg);
                EditorUtility.SetDirty(kit);
                AssetDatabase.SaveAssets();
                Debug.Log($"[Tướng khởi đầu] Đã dựng {OutPath} (vòng 5 tướng, nền đen) và gắn vào UiKit.");
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static RectTransform Rt(string name, Transform parent)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        static Image Img(string name, Transform parent, Sprite s, Color c)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            img.sprite = s;
            img.color = c;
            img.raycastTarget = false;
            return img;
        }

        // chữ chép từ chữ có sẵn (phông), đặt chỗ, cỡ, màu
        static TextMeshProUGUI Txt(TextMeshProUGUI from, Transform parent, string name, Vector2 anchor, Vector2 pos, Vector2 size, float fontSize, Color color,
            TextAlignmentOptions align = TextAlignmentOptions.Center, Vector2? pivot = null)
        {
            var t = Object.Instantiate(from.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = name;
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            foreach (var c in t.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
            t.gameObject.SetActive(true);
            t.rectTransform.Place(anchor, pos, size, pivot);
            t.enableAutoSizing = false;
            t.fontSize = fontSize;
            t.color = color;
            t.alignment = align;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Ellipsis;
            t.richText = true;
            t.raycastTarget = false;
            return t;
        }
    }
}
