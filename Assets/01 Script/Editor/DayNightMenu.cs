// Sáng tối theo giờ máy (người dùng dặn 2026-11-18: mọi đảo và sảnh lấy thời gian sáng, tối).
// - "PokiClash/Prefab/Sảnh và đảo/Sáng tối: Dựng lớp sáng tối (Zone, Hub)": tạo material nhân màu (UIMultiply), tia nắng (UISunRays); dựng lớp "sang_toi"
//   (DayNight: nhuom, nang, den) trong Screens/Zone ngay sau lớp phần động của ảnh bản đồ (dưới đường, chấm ải, tướng; gán
//   ZoneScene.dayNight) và trong Screens/Hub trên biển, đảo, mây của anh_nen_world, dưới lop_tren (autoKey world). Chạy lại thì dựng lại.
//   Cả hai màn: lớp nhuộm, nắng tràn 20000 ra ngoài ảnh (khung cắt RectMask2D cắt lại), đèn trùng khung ảnh.
// - "PokiClash/Prefab/Sảnh và đảo/Sáng tối: Mây sảnh đồng bộ đảo vùng đất": mây sảnh (vành mây may_vien, mây trôi may_0..) đổi sang hình mây vẽ tay của đảo
//   vùng đất (land_thuy_may_1/2, xen kẽ; giữ bề ngang, cao theo tỉ lệ hình, bỏ material của mây nướng cũ) và gán vào DayNight.clouds
//   để xỉn theo giờ như mây đảo (người dùng dặn 2026-11-18: "mây ở phần đảo chính cũng phải đổi đồng bộ"). Dựng lại lớp sáng tối
//   cũng gán lại mây.
// - "PokiClash/Thử/Giờ trong game: …" (đang Play): ép giờ (DayCycle.Override) để soi; "theo máy" bỏ ép.
// - "PokiClash/Thử/Sáng tối: chụp mép bản đồ sảnh" (đang Play): kéo sảnh tới hai góc giới hạn, chụp lúc 10h, 18h20, 22h vào
//   Temp/PokiShots/sanh_mep_*.png (không xoá ảnh khác), trả giờ theo máy và về giữa.
using System.Linq;
using System.Text;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class DayNightMenu
    {
        const string ZonePath = "Assets/04 Prefabs/Screens/Zone.prefab";
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string MulPath = "Assets/03 Art/Islands/day_multiply.mat";
        const string RaysPath = "Assets/03 Art/Islands/day_rays.mat";
        const string JsonPath = "Assets/03 Art/Islands/island_anim.json";
        static readonly string[] CloudArt = { "Assets/03 Art/Islands/land_thuy_may_1.png", "Assets/03 Art/Islands/land_thuy_may_2.png" };

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Sáng tối: Mây sảnh đồng bộ đảo vùng đất", priority = 72)]
        static void HubCloudsMenu()
        {
            var art = CloudArt.Select(AssetDatabase.LoadAssetAtPath<Sprite>).ToArray();
            if (art.Any(a => !a))
            {
                Debug.LogError("[Sáng tối] Thiếu hình mây land_thuy_may_1/2 (ArtGen/Islands/land_thuy/m0/build_land.py --xuat)");
                return;
            }
            Edit(HubPath, root =>
            {
                var world = root.GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "anh_nen_world");
                var dn = world ? world.GetComponentInChildren<DayNight>(true) : null;
                if (!dn)
                {
                    Debug.LogError("[Sáng tối] Hub: không thấy anh_nen_world / lớp sang_toi (chạy Dựng lớp sáng tối trước)");
                    return;
                }
                var list = HubClouds(world);
                for (int i = 0; i < list.Length; i++)
                {
                    var img = list[i];
                    var sp = art[i % art.Length];
                    float w = img.rectTransform.sizeDelta.x;
                    img.sprite = sp;
                    img.material = null; // mây nướng cũ (sk_CloudPuff) cần material giải mã kênh; hình mới là sprite thường
                    img.type = Image.Type.Simple;
                    img.color = Color.white;
                    img.rectTransform.sizeDelta = new Vector2(w, w * sp.rect.height / sp.rect.width);
                }
                SetClouds(dn, list);
                Debug.Log($"[Sáng tối] Hub: đổi {list.Length} đám mây sang hình mây đảo vùng đất, gán DayNight.clouds");
            });
            AssetDatabase.SaveAssets();
        }

        // mây sảnh: các con của vành mây may_vien và mây trôi may_* nằm thẳng dưới anh_nen_world
        static Image[] HubClouds(Transform world)
        {
            var list = new System.Collections.Generic.List<Image>();
            var ring = world.Find("may_vien");
            if (ring)
                foreach (Transform c in ring)
                    if (c.TryGetComponent<Image>(out var im)) list.Add(im);
            foreach (Transform c in world)
                if (c.name.StartsWith("may_") && c.name != "may_vien" && c.TryGetComponent<Image>(out var im)) list.Add(im);
            return list.ToArray();
        }

        static void SetClouds(DayNight dn, Image[] list)
        {
            var so = new SerializedObject(dn);
            var arr = so.FindProperty("clouds");
            arr.arraySize = list.Length;
            for (int i = 0; i < list.Length; i++) arr.GetArrayElementAtIndex(i).objectReferenceValue = list[i];
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Sáng tối: Dựng lớp sáng tối (Zone, Hub)", priority = 71)]
        static void Build()
        {
            var mul = Mat(MulPath, "PokiClash/UIMultiply");
            var rays = Mat(RaysPath, "PokiClash/UISunRays");
            var json = AssetDatabase.LoadAssetAtPath<TextAsset>(JsonPath);
            if (!mul || !rays || !json)
            {
                Debug.LogError("[Sáng tối] Thiếu shader UIMultiply / UISunRays hoặc island_anim.json");
                return;
            }
            Edit(ZonePath, root =>
            {
                var zs = root.GetComponentInChildren<ZoneScene>(true);
                var anim = (IslandAnim)new SerializedObject(zs).FindProperty("mapAnim").objectReferenceValue;
                if (!anim)
                {
                    Debug.LogError("[Sáng tối] Zone: ZoneScene.mapAnim trống");
                    return;
                }
                var dn = Overlay(anim.transform.parent, anim.transform.GetSiblingIndex() + 1, anim, mul, rays, json, "", 20000);
                var so = new SerializedObject(zs);
                so.FindProperty("dayNight").objectReferenceValue = dn;
                so.ApplyModifiedPropertiesWithoutUndo();
                Debug.Log("[Sáng tối] Zone: " + Children(anim.transform.parent));
            });
            Edit(HubPath, root =>
            {
                var anim = root.GetComponentsInChildren<IslandAnim>(true)
                    .FirstOrDefault(a => new SerializedObject(a).FindProperty("autoKey").stringValue == "world");
                if (!anim)
                {
                    Debug.LogError("[Sáng tối] Hub: không thấy lớp phần động autoKey world");
                    return;
                }
                // nhuộm cả biển, đảo, mây của lớp ảnh nền sảnh (anh_nen_world), dưới lop_tren (bảng vùng, nút giữ sáng cho dễ đọc).
                // Nhuộm tràn ra ngoài anh_nen_world (RectMask2D của khung_anh cắt lại): kéo ra rìa thấy biển lặp, lề ảnh đảo, vành mây
                // ngoài khung ảnh, phải tối theo (người dùng báo 2026-11-18: lộ mép chữ nhật). nen_hai_ben nằm ngoài khung cắt: seaOutside.
                var island = anim.transform.parent;
                var stray = island.Find("sang_toi");
                if (stray) Object.DestroyImmediate(stray.gameObject);
                var world = island.parent;
                var top = world.Find("lop_tren");
                var dn = Overlay(world, top ? top.GetSiblingIndex() : world.childCount, anim, mul, rays, json, "world", 20000);
                var sea = world.Find("bien") ? world.Find("bien").GetComponent<Graphic>() : null;
                var sides = root.GetComponentsInChildren<Graphic>(true).FirstOrDefault(g => g.name == "nen_hai_ben");
                var so = new SerializedObject(dn);
                var arr = so.FindProperty("seaDark");
                arr.arraySize = sea ? 1 : 0;
                if (sea) arr.GetArrayElementAtIndex(0).objectReferenceValue = sea;
                var outArr = so.FindProperty("seaOutside");
                outArr.arraySize = sides ? 1 : 0;
                if (sides) outArr.GetArrayElementAtIndex(0).objectReferenceValue = sides;
                if (!sides) Debug.LogWarning("[Sáng tối] Hub: không thấy nen_hai_ben");
                so.ApplyModifiedPropertiesWithoutUndo();
                SetClouds(dn, HubClouds(world));
                Debug.Log("[Sáng tối] Hub: " + Children(world));
            });
            AssetDatabase.SaveAssets();
            Debug.Log("[Sáng tối] Đã dựng lớp sáng tối cho Zone và Hub");
        }

        static string Children(Transform t)
        {
            if (!t) return "-";
            var sb = new StringBuilder(t.name + " [");
            for (int i = 0; i < t.childCount; i++) sb.Append(i == 0 ? "" : ", ").Append(t.GetChild(i).name);
            return sb.Append("]").ToString();
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

        static void Edit(string path, System.Action<GameObject> patch)
        {
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                patch(root);
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static RectTransform Stretch(GameObject go, Transform parent)
        {
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent, false);
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            rt.pivot = new Vector2(0.5f, 0.5f);
            return rt;
        }

        static Image Img(Transform parent, string name, Material m)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
            Stretch(go, parent);
            var img = go.GetComponent<Image>();
            img.material = m;
            img.raycastTarget = false;
            img.color = Color.white;
            img.enabled = false; // DayNight bật khi có tác dụng
            return img;
        }

        // bleed: lớp nhuộm, nắng tràn ra ngoài khung cha bao nhiêu (màn đảo zoom ra, sảnh kéo ra rìa thấy biển ngoài ảnh: phải tối, nắng
        // theo); lớp đèn co lại cho trùng khung cha (toạ độ đèn theo ảnh, DayNight lấy khung này quy uv của nắng)
        static DayNight Overlay(Transform parent, int index, IslandAnim anim, Material mul, Material rays, TextAsset json, string key, float bleed)
        {
            var old = parent.Find("sang_toi");
            if (old)
            {
                if (old.GetSiblingIndex() < index) index--;
                Object.DestroyImmediate(old.gameObject);
            }
            var go = new GameObject("sang_toi", typeof(RectTransform));
            var ort = Stretch(go, parent);
            ort.offsetMin = -Vector2.one * bleed;
            ort.offsetMax = Vector2.one * bleed;
            go.transform.SetSiblingIndex(Mathf.Clamp(index, 0, parent.childCount - 1));
            var tint = Img(go.transform, "nhuom", mul);
            // nắng tràn như nhuộm; RawImage để DayNight đặt uvRect theo khung ảnh (shader tính dải theo uv: uv 0..1 = khung ảnh, phần
            // tràn có uv ngoài 0..1 nên dải chạy tiếp, không to quá cỡ, không lộ mép ở rìa khung)
            var rayGo = new GameObject("nang", typeof(RectTransform), typeof(CanvasRenderer), typeof(RawImage));
            Stretch(rayGo, go.transform);
            var ray = rayGo.GetComponent<RawImage>();
            ray.material = rays;
            ray.raycastTarget = false;
            ray.color = Color.white;
            ray.enabled = false; // DayNight bật khi có tác dụng
            var lights = Stretch(new GameObject("den", typeof(RectTransform)), go.transform);
            lights.offsetMin = Vector2.one * bleed;
            lights.offsetMax = -Vector2.one * bleed;
            var dn = go.AddComponent<DayNight>();
            var item = (Image)new SerializedObject(anim).FindProperty("itemPrefab").objectReferenceValue;
            dn.Setup(tint, ray, lights, item, json, key);
            return dn;
        }

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Giờ trong game: 10h sáng (đang Play)", priority = 126)]
        static void Morning() => DayCycle.Override = 10f;

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Giờ trong game: 18h20 hoàng hôn (đang Play)", priority = 126)]
        static void Dusk() => DayCycle.Override = 18.33f;

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Giờ trong game: 22h đêm (đang Play)", priority = 126)]
        static void Night() => DayCycle.Override = 22f;

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Giờ trong game: theo giờ máy (đang Play)", priority = 126)]
        static void Real() => DayCycle.Override = null;

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Sáng tối: chụp mép bản đồ sảnh (đang Play)", priority = 127)]
        static void HubEdges()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Sáng tối] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(HubEdgesRun());
        }

        static System.Collections.IEnumerator HubEdgesRun()
        {
            BootTitle.Dismiss();
            App.Modals.CloseAll();
            if (App.Router.Current != SceneIds.Hub) App.Router.Go(SceneIds.Hub);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != SceneIds.Hub) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(1f);
            var pan = Object.FindAnyObjectByType<HubPan>();
            if (!pan)
            {
                Debug.LogError("[Sáng tối] Không thấy HubPan trên sảnh");
                yield break;
            }
            var max = (Vector2)typeof(HubPan).GetProperty("Max", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance).GetValue(pan);
            System.IO.Directory.CreateDirectory(PlayTour.ShotDir);
            try
            {
                // trai_duoi: thấy mép trái, mép dưới khung ảnh (như ảnh người dùng báo); phai_tren: mép phải, mép trên
                foreach (var (h, tag) in new[] { (10f, "10h"), (18.33f, "18h20"), (22f, "22h") })
                    foreach (var (o, side) in new[] { (new Vector2(max.x, max.y), "trai_duoi"), (new Vector2(-max.x, -max.y), "phai_tren") })
                    {
                        DayCycle.Override = h;
                        for (int i = 0; i < 20; i++)
                        {
                            pan.SetOffset(o);
                            yield return null;
                        }
                        pan.SetOffset(o);
                        yield return new WaitForEndOfFrame();
                        var tex = ScreenCapture.CaptureScreenshotAsTexture();
                        System.IO.File.WriteAllBytes(System.IO.Path.Combine(PlayTour.ShotDir, $"sanh_mep_{tag}_{side}.png"), tex.EncodeToPNG());
                        Object.Destroy(tex);
                    }
                pan.Recenter();
                // màn đảo Thủy zoom ra hết lúc 10h: nắng, nhuộm tràn ra biển ngoài ảnh cũng không lộ mép
                DayCycle.Override = 10f;
                App.Router.Go(SceneIds.Zone, PokiClash.Core.Elem.Thuy);
                t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Zone) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(1f);
                var zone = Object.FindAnyObjectByType<ZoneScene>();
                if (zone) zone.LandOverview();
                yield return new WaitForSecondsRealtime(2.5f);
                yield return new WaitForEndOfFrame();
                var zt = ScreenCapture.CaptureScreenshotAsTexture();
                System.IO.File.WriteAllBytes(System.IO.Path.Combine(PlayTour.ShotDir, "sanh_mep_dao_thuy_10h.png"), zt.EncodeToPNG());
                Object.Destroy(zt);
                App.Router.Go(SceneIds.Hub);
                Debug.Log("[Sáng tối] Đã chụp mép bản đồ sảnh: " + PlayTour.ShotDir);
            }
            finally
            {
                DayCycle.Override = null;
                pan.Recenter();
            }
        }
    }
}
