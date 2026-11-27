// Giao diện sảnh chung (LobbyDock, người dùng 2026-11-27: "các UI này sống qua các màn home/đảo chính/đảo casino, chỉ tắt khi vào các scene
// bên trong"): dời hàng nút đáy (hang_nut), cột công trình (cot_cong_trinh) và cột ưu đãi (cua_hang_san, HubShop) từ Screens/Hub sang
// App.prefab, cùng canvas với thanh trên (Canvas thanh tren, thứ tự 10, trên lớp chuyến tàu):
// - hang_nut, cot_cong_trinh vào nút sanh_chung (LobbyDock, trải kín khung, ngay trước Thanh tren để thanh trên và lớp đồ bay vẽ trên);
// - cua_hang_san vào vùng an toàn của canvas đó (như ở sảnh).
// Hai canvas cùng prefab CanvasManHinh nên giữ nguyên neo, toạ độ. Tham chiếu LobbyDock.bottom / buildings lấy theo HubScene.bottom /
// buildings cũ (cùng vị trí trong cụm chép), nối TopBars.lobby, rồi xoá ba cụm khỏi Hub và để trống hai mảng cũ của HubScene.
// Chạy lại được: App đã có LobbyDock thì chỉ nối lại TopBars. Từ đây các menu dựng hàng nút / cột (HubDockMenu, HubTileMenu, HubBadgeMenu,
// SoPhepMenu, ShopMenu.BuildHub) sửa ở App.prefab.
using System.Collections.Generic;
using System.Linq;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class LobbyDockMenu
    {
        public const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        public const string NodeName = "sanh_chung";

        // Temp/lobby_dock.flag: biên dịch xong và không Play thì dời một lần rồi xoá cờ (Unity dùng chung nhiều phiên)
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            var f = System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../Temp/lobby_dock.flag"));
            if (!System.IO.File.Exists(f)) return;
            System.IO.File.Delete(f);
            Move();
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Sảnh chung: dời hàng nút, cột công trình, cột ưu đãi sang App", priority = 63)]
        public static void Move()
        {
            var app = PrefabUtility.LoadPrefabContents(AppPath);
            GameObject hub = null;
            try
            {
                var bars = app.GetComponentInChildren<TopBars>(true);
                var canvas = bars ? bars.GetComponentInParent<PokiCanvas>(true) : null;
                if (!canvas || !canvas.Frame || !canvas.Safe)
                {
                    Debug.LogError("[Sảnh chung] Không thấy TopBars hoặc canvas của thanh trên trong App.prefab.");
                    return;
                }
                var dock = app.GetComponentInChildren<LobbyDock>(true);
                if (dock)
                {
                    bars.SetLobby(dock);
                    EditorUtility.SetDirty(bars);
                    PrefabUtility.SaveAsPrefabAsset(app, AppPath);
                    Debug.Log("[Sảnh chung] App.prefab đã có " + NodeName + ": chỉ nối lại TopBars.");
                    return;
                }

                hub = PrefabUtility.LoadPrefabContents(HubPath);
                var scene = hub.GetComponentInChildren<HubScene>(true);
                var row = Find(hub, "hang_nut");
                var col = Find(hub, "cot_cong_trinh");
                var shop = hub.GetComponentInChildren<HubShop>(true);
                if (!scene || !row || !col)
                {
                    Debug.LogError("[Sảnh chung] Screens/Hub thiếu HubScene, hang_nut hoặc cot_cong_trinh.");
                    return;
                }

                // nút sanh_chung: trải kín khung, ngay trước Thanh tren
                var node = new GameObject(NodeName, typeof(RectTransform), typeof(CanvasGroup)).GetComponent<RectTransform>();
                node.SetParent(canvas.Frame, false);
                node.anchorMin = Vector2.zero;
                node.anchorMax = Vector2.one;
                node.pivot = new Vector2(0.5f, 0.5f);
                node.offsetMin = node.offsetMax = Vector2.zero;
                node.SetSiblingIndex(bars.transform.GetSiblingIndex());
                dock = node.gameObject.AddComponent<LobbyDock>();

                var rowCopy = Copy(row, node);
                var colCopy = Copy(col, node);
                if (shop) Copy((RectTransform)shop.transform, canvas.Safe).SetAsLastSibling();

                // tham chiếu theo vị trí trong cụm chép
                var so = new SerializedObject(scene);
                var oldBottom = so.FindProperty("bottom");
                var oldBuild = so.FindProperty("buildings");
                var bottom = new LobbyDock.BottomButton[oldBottom != null ? oldBottom.arraySize : 0];
                for (int i = 0; i < bottom.Length; i++)
                {
                    var e = oldBottom.GetArrayElementAtIndex(i);
                    bottom[i] = new LobbyDock.BottomButton
                    {
                        button = Map(e.FindPropertyRelative("button").objectReferenceValue as SketchButton, row, rowCopy),
                        badge = Map(e.FindPropertyRelative("badge").objectReferenceValue as RectTransform, row, rowCopy),
                        badgeText = Map(e.FindPropertyRelative("badgeText").objectReferenceValue as TMPro.TextMeshProUGUI, row, rowCopy),
                    };
                    if (!bottom[i].button) Debug.LogWarning($"[Sảnh chung] Nút đáy {i} không nằm trong hang_nut.");
                }
                var builds = new HubBuilding[oldBuild != null ? oldBuild.arraySize : 0];
                for (int i = 0; i < builds.Length; i++)
                {
                    builds[i] = Map(oldBuild.GetArrayElementAtIndex(i).objectReferenceValue as HubBuilding, col, colCopy);
                    if (!builds[i]) Debug.LogWarning($"[Sảnh chung] Thẻ công trình {i} không nằm trong cot_cong_trinh.");
                }
                dock.Setup(bottom, builds);
                EditorUtility.SetDirty(dock);
                bars.SetLobby(dock);
                EditorUtility.SetDirty(bars);

                // gỡ khỏi Hub, để trống mảng cũ và nhóm giao diện chuyến tàu (trỏ vào hai cụm vừa gỡ)
                Object.DestroyImmediate(row.gameObject);
                Object.DestroyImmediate(col.gameObject);
                if (shop) Object.DestroyImmediate(shop.gameObject);
                if (oldBottom != null) oldBottom.arraySize = 0;
                if (oldBuild != null) oldBuild.arraySize = 0;
                var chrome = so.FindProperty("chrome");
                if (chrome != null) chrome.arraySize = 0;
                so.ApplyModifiedPropertiesWithoutUndo();

                PrefabUtility.SaveAsPrefabAsset(app, AppPath);
                PrefabUtility.SaveAsPrefabAsset(hub, HubPath);
                AssetDatabase.SaveAssets();
                Debug.Log($"[Sảnh chung] Đã dời hang_nut ({bottom.Count(b => b.button)} nút), cot_cong_trinh ({builds.Count(b => b)} thẻ)" +
                          (shop ? ", cua_hang_san" : "") + " sang App.prefab/" + NodeName + "; Screens/Hub đã gỡ.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(app);
                if (hub) PrefabUtility.UnloadPrefabContents(hub);
            }
        }

        static RectTransform Find(GameObject root, string name) =>
            root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == name);

        // chép cụm sang cha mới, giữ neo / toạ độ / tên
        static RectTransform Copy(RectTransform src, Transform parent)
        {
            var go = Object.Instantiate(src.gameObject, parent, false);
            go.name = src.name;
            go.SetActive(src.gameObject.activeSelf);
            return (RectTransform)go.transform;
        }

        // component tương ứng trong cụm chép: cùng đường đi theo thứ tự con từ gốc cụm
        static T Map<T>(T orig, Transform srcRoot, Transform dstRoot) where T : Component
        {
            if (!orig || !orig.transform.IsChildOf(srcRoot)) return null;
            var path = new List<int>();
            for (var t = orig.transform; t != srcRoot; t = t.parent) path.Add(t.GetSiblingIndex());
            var d = dstRoot;
            for (int i = path.Count - 1; i >= 0; i--)
            {
                if (path[i] >= d.childCount) return null;
                d = d.GetChild(path[i]);
            }
            // cùng loại trên cùng đối tượng: lấy theo thứ tự
            int k = System.Array.IndexOf(orig.GetComponents<T>(), orig);
            var all = d.GetComponents<T>();
            return k >= 0 && k < all.Length ? all[k] : null;
        }
    }
}
