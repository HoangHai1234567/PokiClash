// Dựng hộp chọn đội Dialogs/ChonDoi (biến thể tờ giấy gốc HopThoai, TeamPickerDialog): tiêu đề, lưới kho tướng (Items/OKho),
// dòng gợi ý (khắc hệ, ô đội còn khoá), nút "Xong". Chữ chép từ hộp Chuẩn bị trận. Gán vào ChuanBiTran (pickerPrefab) cùng hai chữ
// đầu mục đội hình (teamTitle, teamHint). Chạy lại thì dựng lại.
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class TeamPickerMenu
    {
        const string SheetPath = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonDoi.prefab";

        [MenuItem("PokiClash/Prefab/Hộp chọn đội (ChonDoi)", priority = 64)]
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
                root.name = "ChonDoi";
                root.GetComponent<ModalSheet>().Configure(940, false, false);
                // khung nội dung dưới tờ giấy (như ChuanBiTran): cột dọc, giãn ngang
                var sheet = Find(root.transform, "to_giay");
                if (!sheet)
                {
                    Debug.LogError("[Đội] HopThoai không có to_giay.");
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
                title.text = "Chọn đội";

                var gridGo = new GameObject("kho", typeof(RectTransform), typeof(GridLayoutGroup), typeof(LayoutElement));
                gridGo.transform.SetParent(content, false);
                var grid = gridGo.GetComponent<GridLayoutGroup>();
                grid.cellSize = new Vector2(136, 160);
                grid.spacing = new Vector2(14, 16);
                grid.childAlignment = TextAnchor.UpperCenter;
                var gridLe = gridGo.GetComponent<LayoutElement>();
                gridLe.preferredHeight = 176;

                var hint = Text(hintTpl, content, "goi_y", 80);
                hint.alignment = TextAlignmentOptions.Center;
                hint.textWrappingMode = TextWrappingModes.Normal;
                hint.text = "Mũi tên xanh: khắc hệ của địch. Mũi tên đỏ: bị khắc.";

                var row = new GameObject("hang", typeof(RectTransform), typeof(HorizontalLayoutGroup), typeof(LayoutElement));
                row.transform.SetParent(content, false);
                var hl = row.GetComponent<HorizontalLayoutGroup>();
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                row.GetComponent<LayoutElement>().preferredHeight = 120;
                var done = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonBig.gameObject, row.transform)).GetComponent<SketchButton>();
                done.name = "nut_Xong";
                done.SetText("Xong");
                done.SetRole(BtnColor.Green);

                root.AddComponent<TeamPickerDialog>().Setup(title, hint, (RectTransform)gridGo.transform, gridLe, done, cell);
                var picker = PrefabUtility.SaveAsPrefabAsset(root, PickerPath).GetComponent<TeamPickerDialog>();

                // gán vào hộp Chuẩn bị trận
                var contents = PrefabUtility.LoadPrefabContents(PrepPath);
                try
                {
                    var so = new SerializedObject(contents.GetComponent<StagePrepDialog>());
                    so.FindProperty("pickerPrefab").objectReferenceValue = picker;
                    var head = Find(contents.transform, "dau_doi");
                    var texts = head.GetComponentsInChildren<TextMeshProUGUI>(true);
                    so.FindProperty("teamTitle").objectReferenceValue = texts[0];
                    so.FindProperty("teamHint").objectReferenceValue = texts.Length > 1 ? texts[1] : null;
                    so.ApplyModifiedPropertiesWithoutUndo();
                    PrefabUtility.SaveAsPrefabAsset(contents, PrepPath);
                }
                finally
                {
                    PrefabUtility.UnloadPrefabContents(contents);
                }
                Debug.Log($"[Đội] Đã dựng {PickerPath} và gán vào {PrepPath}.");
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
