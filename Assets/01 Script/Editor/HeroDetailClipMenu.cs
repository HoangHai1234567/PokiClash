// Hộp chi tiết tướng (Dialogs/ChiTietTuong): thêm nút 6, 7 "RA SÂN", "CHẾT" xem clip appear, die của rig .atomik (lô quái Thủy
// 2026-11-11). Chép nút Mana (p.clips[4], menu "Hộp chi tiết tướng: hạt lửa + nút Mana" phải chạy trước), đặt cuối hàng nút clip,
// gán HeroDetailDialog.p.clips[5..6] (ClipIds[5..6] = appear, die). Nút ẩn sẵn trong prefab: HeroDetailDialog bật khi dạng đang xem
// có clip đó. Chạy lại không tạo trùng, chỉ sửa nhãn và thứ tự.
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HeroDetailClipMenu
    {
        const string DetailPath = "Assets/04 Prefabs/Dialogs/ChiTietTuong.prefab";
        static readonly string[] Labels = { "RA SÂN", "CHẾT" };
        static readonly string[] Names = { "nut_RaSan", "nut_Chet" };
        const int First = 5;

        [MenuItem("PokiClash/Prefab/Hộp chi tiết tướng: nút Ra sân + Chết", priority = 64)]
        public static void Build()
        {
            var root = PrefabUtility.LoadPrefabContents(DetailPath);
            try
            {
                var dlg = root.GetComponentInChildren<HeroDetailDialog>(true);
                if (!dlg)
                {
                    Debug.LogError("[Hộp chi tiết] ChiTietTuong thiếu HeroDetailDialog.");
                    return;
                }
                var so = new SerializedObject(dlg);
                var clips = so.FindProperty("p.clips");
                var src = clips.arraySize > 4 ? clips.GetArrayElementAtIndex(4).objectReferenceValue as UI.SketchButton : null;
                if (!src)
                {
                    Debug.LogError("[Hộp chi tiết] Chưa có nút Mana (p.clips[4]): chạy menu \"Hộp chi tiết tướng: hạt lửa + nút Mana\" trước.");
                    return;
                }
                // tăng cỡ mảng thì Unity chép phần tử cuối (nút Mana) vào ô mới: dọn về rỗng, và coi ô trỏ vào nút Mana là rỗng
                int old = clips.arraySize;
                if (old < First + Labels.Length)
                {
                    clips.arraySize = First + Labels.Length;
                    for (int i = old; i < clips.arraySize; i++) clips.GetArrayElementAtIndex(i).objectReferenceValue = null;
                }
                // trả nút Mana về đúng (lần chạy lỗi trước đã đổi tên, nhãn, ẩn nó): tên, nhãn, hiện, đứng ngay sau nút Chiêu
                var row = src.transform.parent;
                src.gameObject.name = "nut_Mana";
                var srcLabel = src.GetComponentInChildren<TMPro.TextMeshProUGUI>(true);
                if (srcLabel) srcLabel.text = "Mana";
                src.gameObject.SetActive(true);
                var skill = clips.GetArrayElementAtIndex(2).objectReferenceValue as UI.SketchButton;
                if (skill && skill.transform.parent == row) src.transform.SetSiblingIndex(skill.transform.GetSiblingIndex() + 1);
                for (int i = 0; i < Labels.Length; i++)
                {
                    var cur = clips.GetArrayElementAtIndex(First + i).objectReferenceValue as UI.SketchButton;
                    if (cur == src) cur = null;
                    if (!cur)
                    {
                        var go = Object.Instantiate(src.gameObject, row);
                        cur = go.GetComponent<UI.SketchButton>();
                        clips.GetArrayElementAtIndex(First + i).objectReferenceValue = cur;
                    }
                    cur.gameObject.name = Names[i];
                    cur.transform.SetAsLastSibling();
                    var label = cur.GetComponentInChildren<TMPro.TextMeshProUGUI>(true);
                    if (label) label.text = Labels[i];
                    cur.gameObject.SetActive(false);
                }
                so.ApplyModifiedPropertiesWithoutUndo();

                // vừa hàng khi đủ 7 nút: thu bề rộng mọi nút theo số nút (kể cả nút đang ẩn)
                var rt = (RectTransform)row;
                var hl = rt.GetComponent<HorizontalLayoutGroup>();
                int n = rt.childCount;
                if (hl && n > 0)
                {
                    float per = (rt.rect.width - hl.padding.horizontal - hl.spacing * (n - 1)) / n;
                    foreach (Transform c in rt)
                    {
                        var le = c.GetComponent<LayoutElement>();
                        if (!le || per <= 0) continue;
                        if (le.preferredWidth > per) le.preferredWidth = per;
                        if (le.minWidth > per) le.minWidth = per;
                    }
                }
                PrefabUtility.SaveAsPrefabAsset(root, DetailPath);
                Debug.Log($"[Hộp chi tiết] {DetailPath}: {rt.childCount} nút clip, thêm RA SÂN, CHẾT (ẩn khi dạng không có clip).");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }
    }
}
