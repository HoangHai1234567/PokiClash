// Thêm dòng "Rung" vào prefab Screens/Notebook, ngay dưới dòng "Âm thanh": nhân bản dòng đó (chữ giữ nguyên kiểu), nút trong dòng
// dựng lại từ đúng prefab kit với cùng các chỉnh sửa (giữ liên kết kit), rồi gán NotebookScene.p.haptics. Đã có thì không làm gì.
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class NotebookHapticsMenu
    {
        const string NotebookPath = "Assets/04 Prefabs/Screens/Notebook.prefab";
        public const string RowName = "hang_Rung", Label = "Rung";

        [MenuItem("PokiClash/Prefab/Sổ tay: thêm dòng Rung", priority = 61)]
        public static void Add()
        {
            var contents = PrefabUtility.LoadPrefabContents(NotebookPath);
            try
            {
                var scene = contents.GetComponentInChildren<NotebookScene>(true);
                var so = new SerializedObject(scene);
                var haptics = so.FindProperty("p.haptics");
                if (haptics.objectReferenceValue)
                {
                    Debug.Log("[Sổ tay] Đã có dòng Rung");
                    return;
                }
                var sound = (SketchButton)so.FindProperty("p.sound").objectReferenceValue;
                if (!sound)
                {
                    Debug.LogError("[Sổ tay] Không thấy nút Âm thanh để nhân bản.");
                    return;
                }
                var row = sound.transform.parent;
                var copy = Object.Instantiate(row.gameObject, row.parent, false);
                copy.name = RowName;
                copy.transform.SetSiblingIndex(row.GetSiblingIndex() + 1);

                // con là prefab kit: thay bản sao (đã mất liên kết) bằng bản dựng từ prefab nguồn với cùng chỉnh sửa
                for (int i = 0; i < row.childCount; i++)
                {
                    var orig = row.GetChild(i).gameObject;
                    if (!PrefabUtility.IsAnyPrefabInstanceRoot(orig)) continue;
                    var src = PrefabUtility.GetCorrespondingObjectFromSource(orig);
                    var cloned = copy.transform.GetChild(i).gameObject;
                    var fresh = (GameObject)PrefabUtility.InstantiatePrefab(src, copy.transform);
                    PrefabUtility.SetPropertyModifications(fresh, PrefabUtility.GetPropertyModifications(orig));
                    fresh.transform.SetSiblingIndex(i);
                    fresh.name = cloned.name;
                    Object.DestroyImmediate(cloned);
                }

                foreach (var t in copy.GetComponentsInChildren<TextMeshProUGUI>(true))
                    if (!t.GetComponentInParent<SketchButton>()) t.text = Label;
                var btn = copy.GetComponentInChildren<SketchButton>(true);
                haptics.objectReferenceValue = btn;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, NotebookPath);
                Debug.Log($"[Sổ tay] Thêm dòng Rung ({btn.name}) dưới dòng Âm thanh");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
