// Dựng hộp chọn tướng khởi đầu Dialogs/ChonTuongKhoiDau (biến thể tờ giấy gốc HopThoai, StarterDialog, GD_Claude/15_TuongKhoiDau.md):
// tiêu đề, dòng giới thiệu, hàng 5 ô tướng (Items/OKho của hộp chọn đội), khung chữ hệ và 3 thẻ của tướng đang chọn, nút "Chọn …".
// Chữ chép từ hộp Chuẩn bị trận. Thêm vào danh sách hộp của UiKit (App.Modals.Open<StarterDialog>). Chạy lại thì dựng lại.
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
        const string OutPath = "Assets/04 Prefabs/Dialogs/ChonTuongKhoiDau.prefab";

        [MenuItem("PokiClash/Prefab/Hộp chọn tướng khởi đầu (ChonTuongKhoiDau)", priority = 65)]
        static void Build()
        {
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));
            var prep = AssetDatabase.LoadAssetAtPath<GameObject>(PrepPath).GetComponent<StagePrepDialog>();
            var pso = new SerializedObject(prep);
            var titleTpl = (TextMeshProUGUI)pso.FindProperty("p.title").objectReferenceValue;
            var hintTpl = (TextMeshProUGUI)pso.FindProperty("p.hint").objectReferenceValue;
            var cell = (PrepRosterCell)pso.FindProperty("cellPrefab").objectReferenceValue;

            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetPath));
            try
            {
                root.name = "ChonTuongKhoiDau";
                root.GetComponent<ModalSheet>().Configure(980, true, false);
                var sheet = Find(root.transform, "to_giay");
                if (!sheet)
                {
                    Debug.LogError("[Tướng khởi đầu] HopThoai không có to_giay.");
                    return;
                }
                var content = new GameObject("noi_dung", typeof(RectTransform), typeof(VerticalLayoutGroup)).transform;
                content.SetParent(sheet, false);
                var vl = content.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 14;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = true;
                vl.childForceExpandHeight = false;

                var title = Text(titleTpl, content, "tieu_de", 64);
                title.alignment = TextAlignmentOptions.Center;
                title.text = "Chọn bạn đồng hành";

                var intro = Text(hintTpl, content, "gioi_thieu", 60);
                intro.alignment = TextAlignmentOptions.Center;
                intro.textWrappingMode = TextWrappingModes.Normal;
                intro.text = "Mỗi hệ một tướng, sức ngang nhau. Bạn đồng hành không sợ bị khắc hệ.";

                var gridGo = new GameObject("hang_tuong", typeof(RectTransform), typeof(GridLayoutGroup), typeof(LayoutElement));
                gridGo.transform.SetParent(content, false);
                var grid = gridGo.GetComponent<GridLayoutGroup>();
                grid.cellSize = new Vector2(136, 160);
                grid.spacing = new Vector2(16, 0);
                grid.childAlignment = TextAnchor.UpperCenter;
                gridGo.GetComponent<LayoutElement>().preferredHeight = 170;

                var info = Text(hintTpl, content, "thong_tin", 440);
                info.alignment = TextAlignmentOptions.TopLeft;
                info.textWrappingMode = TextWrappingModes.Normal;
                info.richText = true;
                info.enableAutoSizing = false;
                info.fontSize = 32;
                info.lineSpacing = 8;
                info.text = "Giọt Sương · hệ Thủy";

                var row = new GameObject("hang", typeof(RectTransform), typeof(HorizontalLayoutGroup), typeof(LayoutElement));
                row.transform.SetParent(content, false);
                var hl = row.GetComponent<HorizontalLayoutGroup>();
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                row.GetComponent<LayoutElement>().preferredHeight = 120;
                var pick = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonBig.gameObject, row.transform)).GetComponent<SketchButton>();
                pick.name = "nut_Chon";
                pick.SetText("Chọn");
                pick.SetRole(BtnColor.Green);

                root.AddComponent<StarterDialog>().Setup(info, (RectTransform)gridGo.transform, pick, cell);
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, OutPath).GetComponent<StarterDialog>();
                if (!kit.dialogs.Any(x => x is StarterDialog))
                {
                    kit.dialogs.Add(dlg);
                    EditorUtility.SetDirty(kit);
                    AssetDatabase.SaveAssets();
                }
                Debug.Log($"[Tướng khởi đầu] Đã dựng {OutPath} và thêm vào UiKit.");
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static Transform Find(Transform t, string name)
        {
            foreach (var c in t.GetComponentsInChildren<Transform>(true))
                if (c.name == name) return c;
            return null;
        }

        // chữ chép từ chữ có sẵn (phông, viền), giãn ngang theo cột, cao h
        static TextMeshProUGUI Text(TextMeshProUGUI from, Transform parent, string name, float h)
        {
            var t = Object.Instantiate(from.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = name;
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            var le = t.GetComponent<LayoutElement>();
            if (!le) le = t.gameObject.AddComponent<LayoutElement>();
            le.preferredHeight = h;
            t.gameObject.SetActive(true);
            return t;
        }
    }
}
