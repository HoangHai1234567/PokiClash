// Gỡ đảo Casino khỏi bản đồ sảnh (người dùng 2026-11-28: "sao lại lộ đảo casino, liên quan gì ở dưới đấy, sao nhỏ thế", chọn gỡ).
// Bản 2026-11-27 (GD_Claude/29 mục C8) đặt nút "casino_dao" (ảnh thu nhỏ sanh_dao_casino.png, rộng 28% bản đồ) ở góc dưới trái, giữa dải
// mây vành đáy, và dời 19 đám mây vành ra khỏi đảo. Menu "PokiClash/Prefab/Sảnh: gỡ đảo Casino" vá Screens/Hub: xoá "casino_dao" trong lớp
// "dao", trả mọi đám mây vành (may_vien_roi) về chỗ gốc theo khoá "ring" của hub_map.json (như HubMapMenu dựng). Vào Casino bằng nút giữa
// thanh dưới hoặc đi tàu. Chạy lại được.
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HubCasinoMenu
    {
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string MapJson = "Assets/03 Art/Islands/hub_map.json";

        [MenuItem("PokiClash/Prefab/Sảnh: gỡ đảo Casino", priority = 62)]
        public static void Remove()
        {
            var contents = PrefabUtility.LoadPrefabContents(HubPath);
            try
            {
                var dao = contents.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == "dao");
                if (!dao)
                {
                    Debug.LogError("[Sảnh] Không thấy lớp dao trong " + HubPath);
                    return;
                }
                var old = dao.Find("casino_dao");
                bool had = old;
                if (old) Object.DestroyImmediate(old.gameObject);

                int restored = 0;
                var ring = dao.Find("may_vien_roi");
                if (ring)
                {
                    var mapRoot = J.Obj(MiniJson.Parse(AssetDatabase.LoadAssetAtPath<TextAsset>(MapJson).text));
                    var view = J.Arr(mapRoot, "view");
                    var homes = J.Arr(mapRoot, "ring");
                    if (view.Count > 1 && homes.Count == ring.childCount)
                    {
                        float vw = System.Convert.ToSingle(view[0]), vh = System.Convert.ToSingle(view[1]);
                        for (int i = 0; i < ring.childCount; i++)
                        {
                            var q = J.Arr(homes[i]);
                            var c = (RectTransform)ring.GetChild(i);
                            var home = new Vector2((System.Convert.ToSingle(q[0]) - 0.5f) * vw, (0.5f - System.Convert.ToSingle(q[1])) * vh);
                            if ((c.anchoredPosition - home).sqrMagnitude > 0.25f || !c.gameObject.activeSelf) restored++;
                            c.anchoredPosition = home;
                            c.gameObject.SetActive(true);
                        }
                    }
                    else
                        Debug.LogWarning($"[Sảnh] Số mây vành ({ring.childCount}) khác khoá ring của {MapJson} ({homes.Count}): không trả mây về chỗ gốc");
                }
                PrefabUtility.SaveAsPrefabAsset(contents, HubPath);
                Debug.Log($"[Sảnh] Gỡ đảo Casino khỏi {HubPath}: {(had ? "đã xoá casino_dao" : "không còn casino_dao")}, trả {restored} đám mây vành về chỗ gốc");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
