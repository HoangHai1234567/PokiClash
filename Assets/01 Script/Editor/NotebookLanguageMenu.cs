// Thêm dòng "Ngôn ngữ" vào prefab Screens/Notebook, ngay dưới dòng "Giảm nhấp nháy" (không có thì "Rung", rồi "Âm thanh"): nhân bản
// dòng đó (chữ giữ nguyên kiểu), nút trong dòng dựng lại từ đúng prefab kit với cùng các chỉnh sửa (giữ liên kết kit), rồi gán
// NotebookScene.p.language. Nút ghi "Tiếng Việt" / "English", bấm thì đổi ngôn ngữ (2026-11-21). Đã có thì không làm gì.
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class NotebookLanguageMenu
    {
        const string NotebookPath = "Assets/04 Prefabs/Screens/Notebook.prefab";
        public const string RowName = "hang_NgonNgu", Label = "Ngôn ngữ";

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Sổ tay: thêm dòng Ngôn ngữ", priority = 63)]
        public static void Add()
        {
            var contents = PrefabUtility.LoadPrefabContents(NotebookPath);
            try
            {
                var scene = contents.GetComponentInChildren<NotebookScene>(true);
                var so = new SerializedObject(scene);
                var lang = so.FindProperty("p.language");
                if (lang.objectReferenceValue)
                {
                    Debug.Log("[Sổ tay] Đã có dòng Ngôn ngữ");
                    return;
                }
                var src = (SketchButton)so.FindProperty("p.lowFlash").objectReferenceValue
                          ?? (SketchButton)so.FindProperty("p.haptics").objectReferenceValue
                          ?? (SketchButton)so.FindProperty("p.sound").objectReferenceValue;
                if (!src)
                {
                    Debug.LogError("[Sổ tay] Không thấy nút Giảm nhấp nháy / Rung / Âm thanh để nhân bản.");
                    return;
                }
                var row = src.transform.parent;
                var copy = Object.Instantiate(row.gameObject, row.parent, false);
                copy.name = RowName;
                copy.transform.SetSiblingIndex(row.GetSiblingIndex() + 1);

                // con là prefab kit: thay bản sao (đã mất liên kết) bằng bản dựng từ prefab nguồn với cùng chỉnh sửa
                for (int i = 0; i < row.childCount; i++)
                {
                    var orig = row.GetChild(i).gameObject;
                    if (!PrefabUtility.IsAnyPrefabInstanceRoot(orig)) continue;
                    var source = PrefabUtility.GetCorrespondingObjectFromSource(orig);
                    var cloned = copy.transform.GetChild(i).gameObject;
                    var fresh = (GameObject)PrefabUtility.InstantiatePrefab(source, copy.transform);
                    PrefabUtility.SetPropertyModifications(fresh, PrefabUtility.GetPropertyModifications(orig));
                    fresh.transform.SetSiblingIndex(i);
                    fresh.name = cloned.name;
                    Object.DestroyImmediate(cloned);
                }

                foreach (var t in copy.GetComponentsInChildren<TextMeshProUGUI>(true))
                    if (!t.GetComponentInParent<SketchButton>()) t.text = Label;
                var btn = copy.GetComponentInChildren<SketchButton>(true);
                btn.SetText("Tiếng Việt");
                lang.objectReferenceValue = btn;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, NotebookPath);
                Debug.Log($"[Sổ tay] Thêm dòng Ngôn ngữ ({btn.name}) dưới dòng {row.name}");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
