// Thêm dòng "Giảm nhấp nháy" vào prefab Screens/Notebook, ngay dưới dòng "Rung" (không có thì dưới "Âm thanh"): nhân bản dòng đó (chữ
// giữ nguyên kiểu), nút trong dòng dựng lại từ đúng prefab kit với cùng các chỉnh sửa (giữ liên kết kit), rồi gán NotebookScene.p.lowFlash.
// Bật thì máy bi không chớp mạnh, không phóng to khi jackpot, đèn dịu (GD_Claude/23). Đã có thì không làm gì.
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class NotebookFlashMenu
    {
        const string NotebookPath = "Assets/04 Prefabs/Screens/Notebook.prefab";
        public const string RowName = "hang_GiamNhapNhay", Label = "Giảm nhấp nháy";

        [MenuItem("PokiClash/Prefab/Sổ tay: thêm dòng Giảm nhấp nháy", priority = 62)]
        public static void Add()
        {
            var contents = PrefabUtility.LoadPrefabContents(NotebookPath);
            try
            {
                var scene = contents.GetComponentInChildren<NotebookScene>(true);
                var so = new SerializedObject(scene);
                var flash = so.FindProperty("p.lowFlash");
                if (flash.objectReferenceValue)
                {
                    Debug.Log("[Sổ tay] Đã có dòng Giảm nhấp nháy");
                    return;
                }
                var src = (SketchButton)so.FindProperty("p.haptics").objectReferenceValue ?? (SketchButton)so.FindProperty("p.sound").objectReferenceValue;
                if (!src)
                {
                    Debug.LogError("[Sổ tay] Không thấy nút Rung / Âm thanh để nhân bản.");
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
                flash.objectReferenceValue = btn;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, NotebookPath);
                Debug.Log($"[Sổ tay] Thêm dòng Giảm nhấp nháy ({btn.name}) dưới dòng {row.name}");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
