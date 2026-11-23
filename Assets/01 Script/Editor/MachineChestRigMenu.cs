// Rig rương AtomSpine cho prefab Kit/Ruong (GD_Claude/23_MayBi_TraiNghiem.md giai đoạn 1). Thêm con "rig" (AtomSpine.AtomikGraphic,
// tắt sẵn, không nhận chạm, chạy theo giờ thật) và gán ba rig ruong_<bậc>.bytes (ArtGen/Pachinko/ruong_rig/build_rig.py) cho
// ChestIcon. Mọi chỗ dùng Kit/Ruong (khay rương chờ, màn mở rương...) nhận theo prefab lồng; rig chỉ bật khi code gọi PlayRig.
// Chạy lại được (thay con "rig" cũ).
using System.IO;
using AtomSpine;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class MachineChestRigMenu
    {
        const string ChestPath = "Assets/04 Prefabs/Kit/Ruong.prefab";
        const string RigDir = "Assets/03 Art/Pachinko/Rig/";

        [MenuItem("PokiClash/Prefab/Máy bi/rig rương (AtomSpine)", priority = 76)]
        public static void Build()
        {
            var go = AssetDatabase.LoadAssetAtPath<TextAsset>(RigDir + "ruong_go.bytes");
            var bac = AssetDatabase.LoadAssetAtPath<TextAsset>(RigDir + "ruong_bac.bytes");
            var vang = AssetDatabase.LoadAssetAtPath<TextAsset>(RigDir + "ruong_vang.bytes");
            if (!go || !bac || !vang)
            {
                Debug.LogError("[Rương] Thiếu " + RigDir + "ruong_<go|bac|vang>.bytes (py -3 -I ArtGen/Pachinko/ruong_rig/build_rig.py).");
                return;
            }
            if (!File.Exists(ChestPath))
            {
                Debug.LogError("[Rương] Thiếu " + ChestPath);
                return;
            }
            var root = PrefabUtility.LoadPrefabContents(ChestPath);
            try
            {
                var icon = root.GetComponent<ChestIcon>();
                if (!icon)
                {
                    Debug.LogError("[Rương] " + ChestPath + " không có ChestIcon.");
                    return;
                }
                var old = root.transform.Find("rig");
                if (old) Object.DestroyImmediate(old.gameObject);
                var node = new GameObject("rig", typeof(RectTransform), typeof(CanvasRenderer), typeof(AtomikGraphic));
                node.layer = LayerMask.NameToLayer("UI");
                var rt = (RectTransform)node.transform;
                rt.SetParent(root.transform, false);
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0);
                rt.anchoredPosition = Vector2.zero;
                rt.sizeDelta = ((RectTransform)root.transform).sizeDelta;
                var g = node.GetComponent<AtomikGraphic>();
                g.raycastTarget = false;
                g.playOnEnable = false;
                g.updateMode = AtomikUpdateMode.Unscaled;
                g.scaleMode = AtomikGraphicScale.RigPixels;
                g.overlayClip = "";
                g.clip = "cho";
                node.SetActive(false);
                icon.SetupRig(g, go, bac, vang);
                PrefabUtility.SaveAsPrefabAsset(root, ChestPath);
                Debug.Log("[Rương] Đã gắn rig AtomSpine vào " + ChestPath + " (go " + go.bytes.Length / 1024 + " KB, bạc " + bac.bytes.Length / 1024 + " KB, vàng " + vang.bytes.Length / 1024 + " KB).");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }
    }
}
