// Đảo Casino trên bản đồ sảnh (GD_Claude/29 mục C8, 2026-11-27; người dùng chọn thu nhỏ hình đảo có sẵn): menu
// "PokiClash/Prefab/Sảnh: đảo Casino" vá Screens/Hub: nút "casino_dao" trong lớp "dao" của bản đồ (cùng cha với các đảo hệ), góc dưới trái
// (biển trống dưới đảo Thủy, xa bến tàu về Nhà ở góc dưới phải), con "hinh" ảnh sanh_dao_casino.png (ArtGen/Casino/hub/dao_sanh.py) có
// HubIslandArt để chạm đúng theo hình đảo; HubScene.SetupCasino gán, chạm như nút giữa thanh dưới (đi tàu ra đảo).
// Tên nút không bắt đầu bằng "dao_" nên menu dựng lại bản đồ (HubMapMenu, xoá mọi "dao_*") không xoá mất. Chạy lại được.
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HubCasinoMenu
    {
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string ArtPath = "Assets/03 Art/Islands/sanh_dao_casino.png";
        // khung trên bản đồ (tỉ lệ ảnh bản đồ, y từ trên): rộng 0,28; cao theo ảnh 760 x 459 trên bản đồ 1024 x 1796
        const float U0 = 0.04f, U1 = 0.32f, V1 = 0.982f;

        [MenuItem("PokiClash/Prefab/Sảnh: đảo Casino", priority = 62)]
        public static void Build()
        {
            var spr = AssetDatabase.LoadAssetAtPath<Sprite>(ArtPath);
            if (!spr)
            {
                Debug.LogError("[Sảnh] Thiếu " + ArtPath + ": chạy ArtGen/Casino/hub/dao_sanh.py");
                return;
            }
            var contents = PrefabUtility.LoadPrefabContents(HubPath);
            try
            {
                var scene = contents.GetComponentInChildren<HubScene>(true);
                var dao = contents.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == "dao");
                if (!scene || !dao)
                {
                    Debug.LogError("[Sảnh] Không thấy HubScene / lớp dao trong " + HubPath);
                    return;
                }
                var old = dao.Find("casino_dao");
                if (old) Object.DestroyImmediate(old.gameObject);
                float v0 = V1 - (U1 - U0) * (1024f / 1796f) * spr.rect.height / spr.rect.width;
                var box = new GameObject("casino_dao", typeof(RectTransform)) { layer = dao.gameObject.layer }.GetComponent<RectTransform>();
                box.SetParent(dao, false);
                box.anchorMin = new Vector2(U0, 1 - V1);
                box.anchorMax = new Vector2(U1, 1 - v0);
                box.pivot = new Vector2(0.5f, 0.18f);
                box.offsetMin = box.offsetMax = Vector2.zero;
                // ngay sau các đảo hệ (dưới lớp đèn đêm, mây, hình động của bản đồ)
                int last = Enumerable.Range(0, dao.childCount).Where(i => dao.GetChild(i).name.StartsWith("dao_")).DefaultIfEmpty(0).Max();
                box.SetSiblingIndex(Mathf.Min(last + 1, dao.childCount - 1));

                var go = new GameObject("hinh", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image)) { layer = dao.gameObject.layer };
                var rt = (RectTransform)go.transform;
                rt.SetParent(box, false);
                rt.anchorMin = Vector2.zero;
                rt.anchorMax = Vector2.one;
                rt.offsetMin = rt.offsetMax = Vector2.zero;
                var img = go.GetComponent<Image>();
                img.sprite = spr;
                img.raycastTarget = true; // bấm theo hình đảo (HubIslandArt lọc bằng mặt nạ)

                // mặt nạ bấm thô từ ảnh (như HubMapMenu)
                const int MW = 96;
                int mh = Mathf.Max(1, Mathf.RoundToInt(MW * spr.rect.height / spr.rect.width));
                var bits = new byte[MW * mh];
                var tex = new Texture2D(2, 2);
                tex.LoadImage(System.IO.File.ReadAllBytes(System.IO.Path.Combine(Application.dataPath, "..", ArtPath)));
                for (int y = 0; y < mh; y++)
                    for (int x = 0; x < MW; x++)
                        bits[y * MW + x] = (byte)(tex.GetPixelBilinear((x + 0.5f) / MW, 1 - (y + 0.5f) / mh).a > 0.5f ? 1 : 0);
                Object.DestroyImmediate(tex);
                var art = go.AddComponent<HubIslandArt>();
                art.Setup(Elem.Thuy, box, MW, mh, bits); // hệ không dùng: đảo Casino không nằm trong SetupIslands
                scene.SetupCasino(art);

                // mây vành rời ở mép bản đồ (may_vien_roi, HubMapMenu) đè lên đảo: đẩy từng đám ra xa tâm đảo 20 px một tới khi hết đè
                // (như KeepClear của màn đảo Casino), đẩy quá 900 px thì tắt. Dựng lại bản đồ (HubMapMenu) thì chạy lại menu này.
                var ring = dao.Find("may_vien_roi");
                int moved = 0, hidden = 0;
                if (ring)
                {
                    var dr = dao.rect;
                    var isl = Rect.MinMaxRect((U0 - 0.5f) * dr.width - 30, (0.5f - V1) * dr.height - 30, (U1 - 0.5f) * dr.width + 30,
                        (0.5f - v0) * dr.height + 30);
                    foreach (RectTransform c in ring)
                    {
                        Rect R(Vector2 p) => new Rect(p - c.sizeDelta / 2, c.sizeDelta);
                        var pos = c.anchoredPosition;
                        if (!R(pos).Overlaps(isl)) continue;
                        var dir = (pos - isl.center).sqrMagnitude > 1 ? (pos - isl.center).normalized : Vector2.down;
                        float push = 0;
                        while (R(pos).Overlaps(isl) && push < 900)
                        {
                            pos += dir * 20;
                            push += 20;
                        }
                        if (R(pos).Overlaps(isl))
                        {
                            c.gameObject.SetActive(false);
                            hidden++;
                        }
                        else
                        {
                            c.anchoredPosition = pos;
                            moved++;
                        }
                    }
                }
                Debug.Log($"[Sảnh] Mây vành quanh đảo Casino: đẩy ra {moved}, tắt {hidden}");
                PrefabUtility.SaveAsPrefabAsset(contents, HubPath);
                Debug.Log($"[Sảnh] Đã đặt đảo Casino vào {HubPath} (khung {U0:0.00}–{U1:0.00} x {v0:0.000}–{V1:0.000})");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
