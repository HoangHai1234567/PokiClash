// Đèn đêm các đảo trên bản đồ sảnh (người dùng 2026-11-20: "buổi đêm các đảo sáng lên và người chơi cần phải biết là click được vào đảo,
// ban ngày thì không cần sáng, chiều tối thì cần; không dùng mũi tên"; chọn cách 3 + 4: mặt nạ phát sáng + đuốc thắp bằng shader).
// Menu "PokiClash/Prefab/Sảnh: đèn đêm các đảo (đuốc, chỗ phát sáng)" sửa Screens/Hub (HubMapMenu cũng gọi Apply khi dựng lại bản đồ):
// - lớp "den_dao" phủ đúng ảnh bản đồ "dao", nằm NGAY TRÊN lớp nhuộm "sang_toi" (nên lửa, chỗ phát sáng không bị nhuộm tối), dưới lop_tren;
// - mỗi đảo một nhóm "dem_<hệ>" trùng khung ảnh đảo (gốc ở chân đảo như "dao_<hệ>"), HubIslandArt nhún nhóm cùng đảo và ẩn khi đảo chưa mở;
//   trong nhóm: "phat" (sanh_phat_<hệ>, shader UIIslandEmit, màu Image = màu hệ pha trắng: phần sáng thêm), "duoc_<i>" / "den_<i>" (Image
//   không ảnh, shader UITorch; màu Image: r = hạt giống lệch nhịp, g = 1 đuốc / 0 đốm đèn trong tranh);
// - lớp "bang_dao" ngay trên den_dao (cùng khung "dao"): năm bảng tên đảo (HubZone) và mây che "suong_mu" chuyển lên đây để lửa, chỗ phát
//   sáng không đè bảng tên, mây che vẫn phủ cả đèn của đảo chưa mở; bảng tên nay không bị nhuộm (đêm dễ đọc), mây che nhuộm qua
//   DayNight.cloudsAbove (CloudTint x màu nhuộm, tối như mây dưới lớp nhuộm);
// - xoá quầng "sang" cũ (2026-11-19) trong các "dao_<hệ>".
// Số liệu: Assets/03 Art/Islands/hub_night.json (ArtGen/Islands/sanh_moi/den_dem.py: chỗ phát sáng, chỗ đặt đuốc). Chạy lại được.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class HubNightMenu
    {
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string ArtDir = "Assets/03 Art/Islands/";
        const string NightJson = ArtDir + "hub_night.json";
        const string MapJson = ArtDir + "hub_map.json";
        const string EmitMat = ArtDir + "hub_emit.mat";
        const string TorchMat = ArtDir + "hub_torch.mat";
        const float Aspect = 1.4f;                          // cao / ngang ô đuốc (UITorch._Aspect)
        const float TorchW = 0.12f, LampW = 0.085f;         // bề ngang ô đuốc, ô đốm đèn: tỉ lệ bề ngang bản đồ
        const float TorchFoot = 0.22f, LampCenter = 0.62f;  // chân đuốc, tâm đốm đèn (đơn vị bề ngang ô, UITorch)
        const float HaloA = 0.36f;                          // độ sáng vùng sáng quanh lửa (UITorch._HaloA; người dùng 2026-11-20: sáng hơn nữa)
        // độ sáng thêm của chỗ phát sáng theo đảo (nhân màu hệ); thân cây thần Mộc rộng, sáng đủ thì chói
        static readonly Dictionary<Elem, float> EmitBoost = new Dictionary<Elem, float> { { Elem.Moc, 0.45f } };

        [MenuItem("PokiClash/Prefab/Sảnh: đèn đêm các đảo (đuốc, chỗ phát sáng)", priority = 64)]
        static void Build()
        {
            var contents = PrefabUtility.LoadPrefabContents(HubPath);
            try
            {
                if (Apply(contents)) PrefabUtility.SaveAsPrefabAsset(contents, HubPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
            AssetDatabase.SaveAssets();
        }

        public static bool Apply(GameObject contents)
        {
            AssetDatabase.ImportAsset(NightJson, ImportAssetOptions.ForceUpdate);
            var json = AssetDatabase.LoadAssetAtPath<TextAsset>(NightJson);
            var mapJson = AssetDatabase.LoadAssetAtPath<TextAsset>(MapJson);
            if (!json || !mapJson)
            {
                Debug.LogError("[Đèn đêm] Thiếu hub_night.json / hub_map.json: chạy ArtGen/Islands/sanh_moi/den_dem.py");
                return false;
            }
            RectTransform Find(string n) => contents.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == n);
            var dao = Find("dao");
            var tint = Find("sang_toi");
            if (!dao || !tint || tint.parent != dao.parent)
            {
                Debug.LogError("[Đèn đêm] Không thấy dao / sang_toi cùng cha trong Hub: chạy menu Sáng tối và Sảnh bản đồ thế giới trước");
                return false;
            }
            var emit = Mat(EmitMat, "PokiClash/UIIslandEmit");
            var torch = Mat(TorchMat, "PokiClash/UITorch");
            if (!emit || !torch)
            {
                Debug.LogError("[Đèn đêm] Thiếu shader PokiClash/UIIslandEmit hoặc PokiClash/UITorch");
                return false;
            }
            var world = (RectTransform)dao.parent;
            var old = world.Find("den_dao");
            if (old) Object.DestroyImmediate(old.gameObject);
            foreach (var t in dao.GetComponentsInChildren<RectTransform>(true)
                         .Where(t => t.name == "sang" && t.parent && t.parent.name.StartsWith("dao_")).ToArray())
                Object.DestroyImmediate(t.gameObject);

            torch.SetFloat("_HaloA", HaloA);
            var layer = new GameObject("den_dao", typeof(RectTransform)).GetComponent<RectTransform>();
            layer.SetParent(world, false);
            Copy(dao, layer);
            layer.SetSiblingIndex(tint.GetSiblingIndex() + 1);

            // bảng tên đảo, mây che lên trên đèn đêm (chạy lại: dùng lại lớp cũ, đừng xoá vì đang chứa bảng tên, mây che)
            var top = world.Find("bang_dao") as RectTransform;
            if (!top)
            {
                top = new GameObject("bang_dao", typeof(RectTransform)).GetComponent<RectTransform>();
                top.SetParent(world, false);
            }
            Copy(dao, top);
            top.SetSiblingIndex(layer.GetSiblingIndex() + 1);
            var scene = contents.GetComponentInChildren<HubScene>(true);
            var zones = scene ? new SerializedObject(scene).FindProperty("zones") : null;
            int nPlate = 0;
            for (int i = 0; zones != null && i < zones.arraySize; i++)
                if (zones.GetArrayElementAtIndex(i).objectReferenceValue is HubZone z)
                {
                    if (z.transform.parent == dao) z.transform.SetParent(top, false);
                    if (z.transform.parent == top) nPlate++;
                }
            var fogRt = dao.Find("suong_mu") ?? top.Find("suong_mu");
            if (fogRt)
            {
                fogRt.SetParent(top, false);
                fogRt.SetAsLastSibling();
            }
            var dn = contents.GetComponentsInChildren<DayNight>(true).FirstOrDefault(x => x.transform.parent == world || x.transform == tint);
            if (dn)
            {
                var fogImgs = fogRt ? fogRt.GetComponentsInChildren<Image>(true).Where(im => im.sprite).ToArray() : new Image[0];
                var so = new SerializedObject(dn);
                var arr = so.FindProperty("cloudsAbove");
                arr.arraySize = fogImgs.Length;
                for (int i = 0; i < fogImgs.Length; i++) arr.GetArrayElementAtIndex(i).objectReferenceValue = fogImgs[i];
                so.ApplyModifiedPropertiesWithoutUndo();
            }
            else Debug.LogWarning("[Đèn đêm] Không thấy DayNight của sảnh: mây che sẽ không tối theo giờ");

            var map = J.Obj(MiniJson.Parse(mapJson.text));
            var view = J.Arr(map, "view");
            float mapAspect = Convert.ToSingle(view[0]) / Convert.ToSingle(view[1]); // ngang / cao của ảnh bản đồ
            var rects = new Dictionary<string, float[]>();
            foreach (var o in J.Arr(map, "islands"))
            {
                var it = J.Obj(o);
                rects[J.Str(it, "zone")] = J.Arr(it, "rect").Select(Convert.ToSingle).ToArray();
            }
            var arts = contents.GetComponentsInChildren<HubIslandArt>(true);
            int nIsl = 0, nTorch = 0, seed = 0;
            foreach (var o in J.Arr(J.Obj(MiniJson.Parse(json.text)), "islands"))
            {
                var it = J.Obj(o);
                string zs = J.Str(it, "zone");
                var e = Keys.ToElem(zs);
                var art = arts.FirstOrDefault(a => a.Zone == e);
                if (!art || !rects.TryGetValue(zs, out var rc))
                {
                    Debug.LogWarning("[Đèn đêm] Không thấy ảnh đảo " + zs);
                    continue;
                }
                var box = (RectTransform)art.transform.parent;
                var g = new GameObject("dem_" + zs, typeof(RectTransform)).GetComponent<RectTransform>();
                g.SetParent(layer, false);
                Copy(box, g);
                art.SetNight(g);
                nIsl++;

                // chỗ phát sáng: giữ màu gốc trên lớp nhuộm, sáng thêm theo màu hệ
                var spr = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + J.Str(it, "emit") + ".png");
                var er = J.Arr(it, "emitRect");
                if (spr && er.Count == 4)
                {
                    float x0 = Convert.ToSingle(er[0]), y0 = Convert.ToSingle(er[1]), x1 = Convert.ToSingle(er[2]), y1 = Convert.ToSingle(er[3]);
                    var img = NewImage("phat", g);
                    img.rectTransform.anchorMin = new Vector2(x0, 1 - y1);
                    img.rectTransform.anchorMax = new Vector2(x1, 1 - y0);
                    img.rectTransform.offsetMin = img.rectTransform.offsetMax = Vector2.zero;
                    img.sprite = spr;
                    img.material = emit;
                    var bc = Color.Lerp(Theme.Of(e), Color.white, 0.35f) * (EmitBoost.TryGetValue(e, out var kb) ? kb : 1f);
                    img.color = new Color(bc.r, bc.g, bc.b, 1);
                }
                else Debug.LogWarning("[Đèn đêm] Thiếu ảnh phát sáng của đảo " + zs);

                // đuốc, đốm đèn: khung tính theo tỉ lệ khung đảo (khỏi phụ thuộc cỡ px của prefab)
                float bw = rc[2] - rc[0], bh = rc[3] - rc[1];
                int k = 0;
                foreach (var to in J.Arr(it, "torches"))
                {
                    var t = J.Obj(to);
                    bool isTorch = J.Str(t, "k") == "torch";
                    float x = (float)J.Num(t, "x"), y = (float)J.Num(t, "y");
                    float wq = isTorch ? TorchW : LampW;
                    float w = wq / bw, h = wq * Aspect * mapAspect / bh;
                    float piv = (isTorch ? TorchFoot : LampCenter) / Aspect;
                    var img = NewImage((isTorch ? "duoc_" : "den_") + k++, g);
                    var rt = img.rectTransform;
                    rt.anchorMin = new Vector2(x - w / 2, 1 - y - piv * h);
                    rt.anchorMax = new Vector2(x + w / 2, 1 - y - piv * h + h);
                    rt.offsetMin = rt.offsetMax = Vector2.zero;
                    img.material = torch;
                    img.color = new Color(Mathf.Repeat(seed++ * 0.618f, 1f), isTorch ? 1 : 0, 1, 1);
                    nTorch++;
                }
            }
            Debug.Log($"[Đèn đêm] Hub: lớp den_dao trên sang_toi, {nIsl} đảo, {nTorch} đuốc / đốm đèn; bang_dao: {nPlate} bảng tên, " +
                      (fogRt ? "mây che" : "không thấy mây che suong_mu"));
            return true;
        }

        static Image NewImage(string name, RectTransform parent)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            img.raycastTarget = false;
            return img;
        }

        static void Copy(RectTransform src, RectTransform dst)
        {
            dst.anchorMin = src.anchorMin;
            dst.anchorMax = src.anchorMax;
            dst.pivot = src.pivot;
            dst.offsetMin = src.offsetMin;
            dst.offsetMax = src.offsetMax;
            dst.localScale = Vector3.one;
        }

        static Material Mat(string path, string shaderName)
        {
            var sh = Shader.Find(shaderName);
            if (!sh) return null;
            var m = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (!m)
            {
                m = new Material(sh) { name = System.IO.Path.GetFileNameWithoutExtension(path) };
                AssetDatabase.CreateAsset(m, path);
            }
            else m.shader = sh;
            EditorUtility.SetDirty(m);
            return m;
        }
    }
}
