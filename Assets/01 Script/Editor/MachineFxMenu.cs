// Dựng hai prefab mục cho mặt máy bi rồi gán vào MachineBoard của Screens/Machine (prefab mục đã có thì chỉ gán lại):
// - Items/HatMayBi (p.particle): một Image trắng neo góc trên trái như các mục khác của mặt máy, không nhận chạm, vật liệu UI
//   mặc định để tô màu được; dùng làm hạt hiệu ứng và nấm động (MachineFx, MachineBoard);
// - Items/VetBiDai (p.trail): TrailGraphic, vệt đuôi một bi; gốc ở góc trên trái lớp vệt.
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class MachineFxMenu
    {
        const string ItemPath = "Assets/04 Prefabs/Items/HatMayBi.prefab";
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string TrailPath = "Assets/04 Prefabs/Items/VetBiDai.prefab";
        const string SpritePath = "Assets/03 Art/Fallback/fx_glow.png";

        [MenuItem("PokiClash/Prefab/Máy bi: hạt hiệu ứng", priority = 62)]
        public static void Build()
        {
            var item = AssetDatabase.LoadAssetAtPath<GameObject>(ItemPath);
            if (!item)
            {
                var go = new GameObject("HatMayBi", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                var img = go.GetComponent<Image>();
                img.raycastTarget = false;
                img.sprite = AssetDatabase.LoadAssetAtPath<Sprite>(SpritePath);
                var rt = (RectTransform)go.transform;
                rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(32, 32);
                item = PrefabUtility.SaveAsPrefabAsset(go, ItemPath);
                Object.DestroyImmediate(go);
                Debug.Log("[Máy bi] Tạo prefab mục " + ItemPath);
            }

            var trail = AssetDatabase.LoadAssetAtPath<GameObject>(TrailPath);
            if (!trail)
            {
                var go = new GameObject("VetBiDai", typeof(RectTransform), typeof(CanvasRenderer), typeof(TrailGraphic));
                go.GetComponent<TrailGraphic>().raycastTarget = false;
                var rt = (RectTransform)go.transform;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0, 1);
                rt.anchoredPosition = Vector2.zero;
                rt.sizeDelta = Vector2.zero;
                trail = PrefabUtility.SaveAsPrefabAsset(go, TrailPath);
                Object.DestroyImmediate(go);
                Debug.Log("[Máy bi] Tạo prefab mục " + TrailPath);
            }

            var contents = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var board = contents.GetComponentInChildren<MachineBoard>(true);
                var so = new SerializedObject(board);
                so.FindProperty("p.particle").objectReferenceValue = item.GetComponent<Image>();
                so.FindProperty("p.trail").objectReferenceValue = trail.GetComponent<TrailGraphic>();
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, MachinePath);
                Debug.Log("[Máy bi] Gán hạt hiệu ứng vào " + MachinePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
