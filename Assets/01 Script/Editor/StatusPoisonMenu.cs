// Dựng nhóm dấu trạng thái ĐỘC trên đầu tướng trong prefab Items/TranTuong (2026-11-17, agent D): chép nhóm dấu bỏng (st_Burn, ba hình
// lửa nhỏ) thành "st_Poison", đổi hình sang bọt (icon tạm có sẵn Assets/03 Art/Fallback/Icons/bubble.png, thiếu thì giữ hình lửa), tô xanh
// độc, gán vào StageActor.poison. StageView.UpdateStatusIcons cho bọt nổi lên lệch pha. Chạy lại nhiều lần được (xoá nhóm cũ rồi dựng lại).
// Chưa chạy menu này thì sân bỏ qua dấu độc trên đầu (bảng vẫn có chip "Độc ×lớp · lượt").
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class StatusPoisonMenu
    {
        const string ActorPath = "Assets/04 Prefabs/Items/TranTuong.prefab";
        const string BubblePath = "Assets/03 Art/Fallback/Icons/bubble.png";

        [MenuItem("PokiClash/Prefab/Trận/Sàn đấu: dấu trạng thái độc", priority = 64)]
        public static void Build()
        {
            var root = PrefabUtility.LoadPrefabContents(ActorPath);
            try
            {
                var actor = root.GetComponent<StageActor>();
                if (!actor)
                {
                    Debug.LogError("[Dấu độc] TranTuong không có StageActor.");
                    return;
                }
                var so = new SerializedObject(actor);
                var burn = so.FindProperty("burn").objectReferenceValue as RectTransform;
                if (!burn)
                {
                    Debug.LogError("[Dấu độc] StageActor chưa có nhóm dấu bỏng để chép.");
                    return;
                }
                var old = so.FindProperty("poison").objectReferenceValue as RectTransform;
                if (old) Object.DestroyImmediate(old.gameObject);
                var stale = burn.parent.Find("st_Poison");
                if (stale) Object.DestroyImmediate(stale.gameObject);

                var go = Object.Instantiate(burn.gameObject, burn.parent);
                go.name = "st_Poison";
                var rt = (RectTransform)go.transform;
                rt.SetSiblingIndex(burn.GetSiblingIndex() + 1);
                var bubble = AssetDatabase.LoadAssetAtPath<Sprite>(BubblePath);
                foreach (var img in go.GetComponentsInChildren<Image>(true))
                {
                    if (bubble)
                    {
                        img.sprite = bubble;
                        img.preserveAspect = true;
                    }
                    img.color = Theme.Hex("#8fd14f");
                    img.raycastTarget = false;
                    var r = img.rectTransform;
                    r.sizeDelta *= 0.8f;
                }
                go.SetActive(false);
                so.FindProperty("poison").objectReferenceValue = rt;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(root, ActorPath);
                Debug.Log($"[Dấu độc] Dựng st_Poison trong {ActorPath} ({(bubble ? "hình bọt" : "giữ hình lửa, thiếu " + BubblePath)}).");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }
    }
}
