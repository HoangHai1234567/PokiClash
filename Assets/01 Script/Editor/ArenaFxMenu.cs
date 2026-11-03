// Dựng lớp phần động của sàn đấu trong Screens/Battle: "PhanDong" (ArenaAnim) phủ đúng khung ảnh nền của StageView, ngay trên ảnh
// nền, dưới tướng; mỗi hình động sinh từ prefab mục Items/HinhDong (HubWorldMenu dựng). Có rồi thì dựng lại. Gán vào StageView.arena.
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ArenaFxMenu
    {
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";
        const string ItemPath = "Assets/04 Prefabs/Items/HinhDong.prefab";

        [MenuItem("PokiClash/Prefab/Sàn đấu: lớp phần động (Screens/Battle)", priority = 63)]
        public static void Build()
        {
            var item = AssetDatabase.LoadAssetAtPath<GameObject>(ItemPath);
            if (!item)
            {
                Debug.LogError("[Sàn đấu] Chưa có " + ItemPath + " (menu PokiClash/Prefab của đảo sảnh dựng)");
                return;
            }
            var contents = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var stage = contents.GetComponentInChildren<StageView>(true);
                var so = new SerializedObject(stage);
                var bg = (Image)so.FindProperty("bg").objectReferenceValue;
                var old = bg.transform.parent.Find("PhanDong");
                if (old) Object.DestroyImmediate(old.gameObject);
                var go = new GameObject("PhanDong", typeof(RectTransform));
                var rt = (RectTransform)go.transform;
                var b = bg.rectTransform;
                rt.SetParent(b.parent, false);
                rt.SetSiblingIndex(b.GetSiblingIndex() + 1);
                rt.anchorMin = b.anchorMin;
                rt.anchorMax = b.anchorMax;
                rt.pivot = b.pivot;
                rt.anchoredPosition = b.anchoredPosition;
                rt.sizeDelta = b.sizeDelta;
                var anim = go.AddComponent<ArenaAnim>();
                anim.Setup(item.GetComponent<Image>());
                so.FindProperty("arena").objectReferenceValue = anim;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, BattlePath);
                Debug.Log("[Sàn đấu] Dựng lớp phần động PhanDong trong " + BattlePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
