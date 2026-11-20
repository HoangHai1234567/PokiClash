// Nút khay Xây có icon công trình (người dùng 2026-11-20: "gen thêm icon các building trong đó nữa"; icon gen ở ArtGen/Home/icons,
// cắt vào Assets/03 Art/Home/icons/icon_home_<mã>.png). Prefab Items/NutKhayNha là biến thể của Kit/Nut_Nho: thêm ảnh "icon" bên trái,
// chữ dời sang phải và tự co cỡ. HomeSceneMenu gọi TrayItem() khi dựng lại cả màn; menu dưới dựng lại nút rồi chỉ vá trường
// trayIconPrefab của Screens/Home.prefab, không dựng lại cả màn.
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HomeTrayMenu
    {
        const string KitPath = "Assets/04 Prefabs/Kit/Nut_Nho.prefab";
        const string ItemPath = "Assets/04 Prefabs/Items/NutKhayNha.prefab";
        const string HomePath = "Assets/04 Prefabs/Screens/Home.prefab";

        // prefab nút khay có icon; có rồi thì dùng lại (rebuild: dựng lại)
        public static HomeTrayItem TrayItem(bool rebuild = false)
        {
            var have = AssetDatabase.LoadAssetAtPath<HomeTrayItem>(ItemPath);
            if (have && !rebuild) return have;
            var kit = AssetDatabase.LoadAssetAtPath<GameObject>(KitPath);
            var go = (GameObject)PrefabUtility.InstantiatePrefab(kit);
            try
            {
                go.name = "NutKhayNha";
                var btn = go.GetComponent<SketchButton>();
                var icon = new GameObject("icon", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image)).GetComponent<Image>();
                var ir = icon.rectTransform;
                ir.SetParent(go.transform, false);
                ir.anchorMin = ir.anchorMax = ir.pivot = new Vector2(0, 0.5f);
                ir.anchoredPosition = new Vector2(10, 3);
                ir.sizeDelta = new Vector2(80, 80);
                icon.preserveAspect = true;
                icon.raycastTarget = false;
                icon.enabled = false;
                var label = btn.Label;
                var lr = label.rectTransform;
                lr.offsetMin = new Vector2(94, lr.offsetMin.y);
                label.enableAutoSizing = true;
                label.fontSizeMax = label.fontSize;
                label.fontSizeMin = 14;
                go.AddComponent<HomeTrayItem>().Setup(btn, icon);
                return PrefabUtility.SaveAsPrefabAsset(go, ItemPath).GetComponent<HomeTrayItem>();
            }
            finally
            {
                Object.DestroyImmediate(go);
            }
        }

        [MenuItem("PokiClash/Prefab/Nhà: nút khay có icon công trình", priority = 64)]
        static void Patch()
        {
            var item = TrayItem(true);
            var root = PrefabUtility.LoadPrefabContents(HomePath);
            try
            {
                var scene = root.GetComponentInChildren<HomeScene>(true);
                if (!scene)
                {
                    Debug.LogError("[Nhà] Không thấy HomeScene trong " + HomePath);
                    return;
                }
                scene.SetupTrayIcon(item);
                PrefabUtility.SaveAsPrefabAsset(root, HomePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            Debug.Log("[Nhà] Khay Xây dùng nút có icon: " + ItemPath);
        }
    }
}
