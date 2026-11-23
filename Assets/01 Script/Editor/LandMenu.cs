// Đảo kiểu vùng đất (GD_Claude/18_DaoVungDat_Habitat.md, M1 2026-11-18).
// - "PokiClash/Prefab/Sảnh và đảo/Đảo vùng đất: Dựng nước, ảnh (mọi đảo)": với mỗi đảo có ảnh khoảng cách tới bờ Baked/Islands/land_<đảo>_dist.png (thủy,
//   mộc…; ghi bằng ArtGen/Islands/land_<đảo>/m0/build_land.py --xuat): đặt cách nhập (không sRGB, không nén, không mipmap), nhập lại
//   ảnh nền land_<đảo> (4096, luật trong ArtImporter), tạo hoặc cập nhật material sóng Assets/03 Art/Islands/land_water_<đảo>.mat
//   (shader PokiClash/UIInkWater); gán vào Screens/Zone (ZoneScene.landWaters, landWater = của Thủy), dựng lại danh mục ảnh. Chạy lại
//   được nhiều lần.
// - "PokiClash/Thử/Đảo Thủy vùng đất: …" (đang Play): đặt tiến độ đảo Thủy 0, 23, 69 ải, vào đảo, đưa từng habitat vào giữa, chụp
//   liên tục (idle, đòn đánh định kỳ) vào Temp/PokiShots/land/; xong trả lại bản lưu như trước. Chụp bằng ScreenCapture (không gán
//   targetTexture cho camera: canvas tính lại cỡ, UI lệch).
// - "PokiClash/Prefab/Sảnh và đảo/Đảo vùng đất: Dựng cờ ải, vùng boss": prefab Items/CoAi (LandFlag: vùng chạm trong suốt, than có nhịp phồng, ô đá,
//   vải, cán; khung vải Assets/03 Art/Islands/Co/co_vai_*, vẽ bằng ArtGen/Islands/land_thuy/m0/ve_co.py), gán ZoneScene.flagPrefab;
//   vùng boss chưa mở: gán ZoneScene.secPrefab (Items/HinhDong: mây phủ, bút chì), pencilArt (Islands/Co/but_chi.png); đặt cách nhập
//   ảnh trường vùng Baked/Islands/land_<đảo>_vung.png của mọi đảo (không sRGB, không nén, không mipmap; build_land.py --xuat ghi),
//   tạo material Islands/land_sketch_<đảo>.mat (shader PokiClash/UILandSketch) gán vào ZoneScene.landSketches, dựng ảnh phác chì
//   "phac_vung" làm con đầu của ảnh bản đồ (dưới hiệu ứng, sáng tối), gán ZoneScene.landSketch; prefab Items/TrungPhuc (Image + ClickCatcher: mây phủ chọc được, mắt boss, rương bí ẩn),
//   gán ZoneScene.eggPrefab, eggArt (Islands/Co/trung_*, Pachinko/pk_ruong_go); dựng lại danh mục ảnh.
// - "PokiClash/Thử/Đảo Thủy vùng đất: easter egg vùng khoá …" (đang Play): tiến độ 23, chụp cảnh rò qua mây, boss tung tuyệt kỹ,
//   chọc mây hắt xì, rương bí ẩn; xong trả bản lưu.
// - "PokiClash/Thử/Đo hiệu năng đảo vùng đất …" (đang Play): đang ở màn đảo vùng đất, tắt lần lượt từng lớp, ghi batches, tris, SetPass
//   (UnityStats) vào Console.
// - "PokiClash/Thử/Đảo Thủy vùng đất: vùng boss …" (đang Play): vùng tối ở tiến độ 0, 23; vùng vừa mở tan tối (19 → 20); cờ trên
//   đường khúc 50–60 (tiến độ 70), 46; thử nút "Khoá lại hết đảo", ô số đảo Thủy của SRDebugger (gọi qua reflection); trả bản lưu.
// - "PokiClash/Thử/Đảo Mộc vùng đất: …" (đang Play): toàn đảo và từng bệ ở tiến độ 69 (cờ trên đường, tướng trên bệ), vùng khoá ở
//   tiến độ 0, 23 (phác chì, mây, bướm, gió, lá rơi, pha lê, đom đóm), lần đầu vào đảo, mở vùng ải 21–30, boss vùng khoá tung tuyệt
//   kỹ; ảnh vào Temp/PokiShots/land/<đảo>_*.jpg; xong trả bản lưu. Đảo Hỏa cùng tour (kèm cột khói).
// - "PokiClash/Thử/Đảo Thủy vùng đất: cờ ải …" (đang Play): tiến độ 45, chụp cờ khúc 40–60 (hai ảnh cách nhau cho thấy vải bay),
//   khúc đã qua, khúc chưa mở, toàn đảo, đêm; rồi sảnh lúc 10h, 18h20, 22h (mây sảnh); xong trả lại bản lưu và giờ.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.UI;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class LandMenu
    {
        const string BakedDir = "Assets/03 Art/Baked/Islands";
        const string IslandDir = "Assets/03 Art/Islands";
        const string ZonePath = "Assets/04 Prefabs/Screens/Zone.prefab";
        const string FlagPath = "Assets/04 Prefabs/Items/CoAi.prefab";
        const string FlagArt = "Assets/03 Art/Islands/Co";
        const string ItemPath = "Assets/04 Prefabs/Items/HinhDong.prefab";
        const string PencilPath = "Assets/03 Art/Islands/Co/but_chi.png";
        const string EggPath = "Assets/04 Prefabs/Items/TrungPhuc.prefab";
        const string ChestArtPath = "Assets/03 Art/Pachinko/pk_ruong_go.png";
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "land");

        // các đảo vùng đất có ảnh Baked/Islands/land_<đảo><đuôi>.png (đuôi _dist: khoảng cách tới bờ, _vung: trường vùng boss); Thủy đầu
        static List<(string isl, string path)> Islands(string tail)
        {
            var list = new List<(string isl, string path)>();
            if (!Directory.Exists(BakedDir)) return list;
            foreach (var f in Directory.GetFiles(BakedDir, "land_*" + tail + ".png"))
            {
                var n = Path.GetFileNameWithoutExtension(f);
                list.Add((n.Substring(5, n.Length - 5 - tail.Length), BakedDir + "/" + n + ".png"));
            }
            return list.OrderBy(x => x.isl == "thuy" ? 0 : 1).ThenBy(x => x.isl).ToList();
        }

        // ảnh số (khoảng cách, trường vùng): đọc đúng số, không sRGB, không nén, không mipmap, RG16
        static void ImportField(string path)
        {
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (!ti) return;
            ti.textureType = TextureImporterType.Default;
            ti.sRGBTexture = false;
            ti.mipmapEnabled = false;
            ti.alphaSource = TextureImporterAlphaSource.None;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.filterMode = FilterMode.Bilinear;
            ti.npotScale = TextureImporterNPOTScale.None;
            ti.maxTextureSize = 2048;
            ti.textureCompression = TextureImporterCompression.Uncompressed;
            foreach (var pf in new[] { "Standalone", "Android", "iPhone" })
            {
                var ps = ti.GetPlatformTextureSettings(pf);
                ps.overridden = true;
                ps.maxTextureSize = 2048;
                ps.format = TextureImporterFormat.RG16;
                ti.SetPlatformTextureSettings(ps);
            }
            ti.SaveAndReimport();
        }

        // material của đảo: tạo nếu chưa có, đặt shader và một ảnh
        static Material IslandMat(string path, Shader shader, string tex, string texPath)
        {
            var mat = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (!mat)
            {
                mat = new Material(shader) { name = Path.GetFileNameWithoutExtension(path) };
                AssetDatabase.CreateAsset(mat, path);
            }
            else mat.shader = shader;
            mat.SetTexture(tex, AssetDatabase.LoadAssetAtPath<Texture2D>(texPath));
            EditorUtility.SetDirty(mat);
            return mat;
        }

        static void SetArray(SerializedObject so, string prop, IList<Material> mats)
        {
            var a = so.FindProperty(prop);
            a.arraySize = mats.Count;
            for (int i = 0; i < mats.Count; i++) a.GetArrayElementAtIndex(i).objectReferenceValue = mats[i];
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Đảo vùng đất: Dựng cờ ải, vùng boss", priority = 71)]
        static void BuildFlag()
        {
            Sprite S(string n) => AssetDatabase.LoadAssetAtPath<Sprite>($"{FlagArt}/{n}.png");
            var frames = new List<Sprite>();
            for (int i = 0; S("co_vai_" + i); i++) frames.Add(S("co_vai_" + i));
            Sprite pole = S("co_can"), stone = S("co_o");
            if (frames.Count == 0 || !pole || !stone)
            {
                Debug.LogError($"[Vùng đất] Thiếu ảnh cờ trong {FlagArt}: chạy ArtGen/Islands/land_thuy/m0/ve_co.py rồi refresh");
                return;
            }
            LandFlag flag;
            var root = new GameObject("co_ai", typeof(RectTransform), typeof(Image), typeof(ClickCatcher), typeof(LandFlag));
            try
            {
                var hit = root.GetComponent<Image>();
                hit.color = new Color(1, 1, 1, 0);
                hit.raycastTarget = true;
                root.GetComponent<CanvasRenderer>().cullTransparentMesh = true; // vùng chạm trong suốt: không vẽ
                var body = new GameObject("than", typeof(RectTransform), typeof(Pulse));
                body.transform.SetParent(root.transform, false);
                var pulse = body.GetComponent<Pulse>();
                pulse.amount = 0.14f;
                pulse.period = 1.1f;
                pulse.enabled = false;
                Image Img(string n, Sprite sp)
                {
                    var go = new GameObject(n, typeof(RectTransform), typeof(Image));
                    go.transform.SetParent(body.transform, false);
                    var im = go.GetComponent<Image>();
                    im.sprite = sp;
                    im.raycastTarget = false;
                    return im;
                }
                // thứ tự vẽ: ô đá, vải, cán (cán che mép vải)
                var o = Img("o", stone);
                var vai = Img("vai", frames[0]);
                var can = Img("can", pole);
                root.GetComponent<LandFlag>().Setup(root.GetComponent<ClickCatcher>(), (RectTransform)body.transform, o, vai, can, pulse, frames.ToArray());
                ((RectTransform)root.transform).sizeDelta = new Vector2(150, 180);
                flag = PrefabUtility.SaveAsPrefabAsset(root, FlagPath).GetComponent<LandFlag>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
            // ảnh trường vùng (R: vùng × 25, G: đất) cho shader phác chì của từng đảo: đọc đúng số, không nén
            var sketchShader = Shader.Find("PokiClash/UILandSketch");
            var sketches = new List<Material>();
            var fields = Islands("_vung");
            if (fields.Count == 0) Debug.LogError($"[Vùng đất] Chưa có {BakedDir}/land_<đảo>_vung.png: chạy build_land.py --xuat rồi refresh");
            foreach (var (isl, path) in fields)
            {
                ImportField(path);
                if (sketchShader) sketches.Add(IslandMat($"{IslandDir}/land_sketch_{isl}.mat", sketchShader, "_SecTex", path));
            }
            var mat = sketches.Count > 0 ? sketches[0] : null;
            var pencil = AssetDatabase.LoadAssetAtPath<Sprite>(PencilPath);
            // món chạm được: Image (nhận chạm) + ClickCatcher
            Image egg;
            var eroot = new GameObject("trung", typeof(RectTransform), typeof(Image), typeof(ClickCatcher));
            try
            {
                var ei = eroot.GetComponent<Image>();
                ei.raycastTarget = true;
                ei.preserveAspect = true;
                egg = PrefabUtility.SaveAsPrefabAsset(eroot, EggPath).GetComponent<Image>();
            }
            finally
            {
                Object.DestroyImmediate(eroot);
            }
            var eggArt = new List<Sprite>();
            foreach (var g in AssetDatabase.FindAssets("trung_ t:Sprite", new[] { FlagArt }))
            {
                var sp = AssetDatabase.LoadAssetAtPath<Sprite>(AssetDatabase.GUIDToAssetPath(g));
                if (sp && sp.name.StartsWith("trung_")) eggArt.Add(sp);
            }
            var chestSp = AssetDatabase.LoadAssetAtPath<Sprite>(ChestArtPath);
            if (chestSp) eggArt.Add(chestSp);
            else Debug.LogError("[Vùng đất] Thiếu " + ChestArtPath + " (rương bí ẩn)");
            var zone = PrefabUtility.LoadPrefabContents(ZonePath);
            try
            {
                var so = new SerializedObject(zone.GetComponentInChildren<ZoneScene>(true));
                so.FindProperty("flagPrefab").objectReferenceValue = flag;
                var item = AssetDatabase.LoadAssetAtPath<GameObject>(ItemPath);
                so.FindProperty("secPrefab").objectReferenceValue = item ? item.GetComponent<Image>() : null;
                if (!item) Debug.LogError("[Vùng đất] Thiếu " + ItemPath + " (mây phủ, bút chì vùng boss)");
                so.FindProperty("pencilArt").objectReferenceValue = pencil;
                if (!pencil) Debug.LogError("[Vùng đất] Thiếu " + PencilPath + " (ve_co.py)");
                // ảnh phác chì: con đầu của ảnh bản đồ, phủ kín ảnh (ZoneSceneLand gán sprite lúc vào đảo)
                var map = (Image)so.FindProperty("p.map").objectReferenceValue;
                var old = map.transform.Find("phac_vung");
                if (old) Object.DestroyImmediate(old.gameObject);
                var go = new GameObject("phac_vung", typeof(RectTransform), typeof(Image));
                go.transform.SetParent(map.transform, false);
                go.transform.SetAsFirstSibling();
                var rt = (RectTransform)go.transform;
                rt.anchorMin = Vector2.zero;
                rt.anchorMax = Vector2.one;
                rt.offsetMin = rt.offsetMax = Vector2.zero;
                var sk = go.GetComponent<Image>();
                sk.material = mat;
                sk.raycastTarget = false;
                sk.preserveAspect = false;
                go.SetActive(false);
                so.FindProperty("landSketch").objectReferenceValue = sk;
                SetArray(so, "landSketches", sketches);
                so.FindProperty("eggPrefab").objectReferenceValue = egg;
                // canvas con sau lớp nút: mây phủ tĩnh, lớp trên mây (cùng khung toạ độ với lớp nút; GraphicRaycaster: chạm mây, mắt boss)
                var nodes = (RectTransform)so.FindProperty("p.nodeLayer").objectReferenceValue;
                RectTransform Layer(string n, int after)
                {
                    var o = nodes.parent.Find(n);
                    if (o) Object.DestroyImmediate(o.gameObject);
                    var lg = new GameObject(n, typeof(RectTransform), typeof(Canvas), typeof(GraphicRaycaster));
                    var lr = (RectTransform)lg.transform;
                    lr.SetParent(nodes.parent, false);
                    lr.anchorMin = nodes.anchorMin;
                    lr.anchorMax = nodes.anchorMax;
                    lr.pivot = nodes.pivot;
                    lr.anchoredPosition = nodes.anchoredPosition;
                    lr.sizeDelta = nodes.sizeDelta;
                    lr.localScale = nodes.localScale;
                    lr.SetSiblingIndex(after + 1);
                    lg.GetComponent<Canvas>().overrideSorting = false;
                    return lr;
                }
                var cl = Layer("lop_may_vung", nodes.GetSiblingIndex());
                var ol = Layer("lop_tren_may", cl.GetSiblingIndex());
                so.FindProperty("cloudLayer").objectReferenceValue = cl;
                so.FindProperty("overLayer").objectReferenceValue = ol;
                var ea = so.FindProperty("eggArt");
                ea.arraySize = eggArt.Count;
                for (int i = 0; i < eggArt.Count; i++) ea.GetArrayElementAtIndex(i).objectReferenceValue = eggArt[i];
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(zone, ZonePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(zone);
            }
            ArtImporter.BuildLibrary();
            AssetDatabase.SaveAssets();
            Debug.Log($"[Vùng đất] Đã dựng {FlagPath} ({frames.Count} khung vải), gán vào Zone cùng phác chì "
                      + string.Join(", ", sketches.Select(m => m.name)) + $", bút chì, {eggArt.Count} hình easter egg");
        }

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đảo Thủy vùng đất: cờ ải chia đều, nổi bật (đang Play)", priority = 126)]
        static void FlagTour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(RunFlagTour());
        }

        static IEnumerator RunFlagTour()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "co_*.jpg")) File.Delete(f);
            foreach (var f in Directory.GetFiles(Dir, "may_sanh_*.jpg")) File.Delete(f);
            try
            {
                DayCycle.Override = 10f;
                App.Save.Data.zones[(int)Elem.Thuy] = 45;
                App.Router.Go(SceneIds.Hub);
                yield return WaitRouter(SceneIds.Hub);
                App.Router.Go(SceneIds.Zone, Elem.Thuy);
                yield return WaitRouter(SceneIds.Zone);
                var zs = Object.FindAnyObjectByType<ZoneScene>();
                yield return new WaitForSecondsRealtime(2.5f);
                yield return Shot("co_vao_dao");
                foreach (var (idx, zoom, tag) in new[] { (46, 0.8f, "46_gan"), (52, 0.6f, "52_vua"), (15, 0.7f, "15_da_qua"), (63, 0.7f, "63_chua_mo") })
                {
                    zs.LandFocus(idx, zoom);
                    yield return new WaitForSecondsRealtime(1.2f);
                    yield return Shot($"co_{tag}_a");
                    yield return new WaitForSecondsRealtime(0.35f);
                    yield return Shot($"co_{tag}_b");
                }
                zs.LandOverview();
                yield return new WaitForSecondsRealtime(1.2f);
                yield return Shot("co_toan_dao");
                DayCycle.Override = 22f;
                zs.LandFocus(46, 0.8f);
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot("co_46_dem");
                // mây sảnh đồng bộ đảo vùng đất (hình mây vẽ tay, xỉn theo giờ)
                foreach (var (h, tag) in new[] { (10f, "10h"), (18.33f, "18h20"), (22f, "22h") })
                {
                    DayCycle.Override = h;
                    App.Router.Go(SceneIds.Hub);
                    yield return WaitRouter(SceneIds.Hub);
                    yield return new WaitForSecondsRealtime(1.2f);
                    yield return Shot($"may_sanh_{tag}");
                }
                Debug.Log("[Thử] Xong cờ ải, mây sảnh: " + Path.GetFullPath(Dir));
            }
            finally
            {
                DayCycle.Override = null;
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Đảo vùng đất: Dựng nước, ảnh (mọi đảo)", priority = 70)]
        static void Build()
        {
            var dists = Islands("_dist");
            if (dists.Count == 0)
            {
                Debug.LogError($"[Vùng đất] Chưa có {BakedDir}/land_<đảo>_dist.png: chạy build_land.py --xuat rồi refresh");
                return;
            }
            var shader = Shader.Find("PokiClash/UIInkWater");
            if (!shader)
            {
                Debug.LogError("[Vùng đất] Không thấy shader PokiClash/UIInkWater");
                return;
            }
            var mats = new List<Material>();
            var arts = new List<string>();
            foreach (var (isl, path) in dists)
            {
                ImportField(path);
                var artPath = $"{IslandDir}/land_{isl}.png";
                AssetDatabase.ImportAsset(artPath, ImportAssetOptions.ForceUpdate);
                mats.Add(IslandMat($"{IslandDir}/land_water_{isl}.mat", shader, "_DistTex", path));
                var art = AssetDatabase.LoadAssetAtPath<Texture2D>(artPath);
                arts.Add($"land_{isl} {(art ? art.width + "x" + art.height : "THIẾU ẢNH NỀN")}");
            }

            var root = PrefabUtility.LoadPrefabContents(ZonePath);
            try
            {
                var so = new SerializedObject(root.GetComponentInChildren<ZoneScene>(true));
                so.FindProperty("landWater").objectReferenceValue = mats[0];
                SetArray(so, "landWaters", mats);
                // camera kéo, zoom của đảo vùng đất: cùng chỗ ScrollRect (ZoneScene tắt ScrollRect khi vào đảo vùng đất)
                var scroll = (ScrollRect)so.FindProperty("p.scroll").objectReferenceValue;
                var lv = scroll.GetComponent<LandView>();
                if (!lv) lv = scroll.gameObject.AddComponent<LandView>();
                so.FindProperty("landView").objectReferenceValue = lv;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(root, ZonePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            ArtImporter.BuildLibrary();
            AssetDatabase.SaveAssets();
            Debug.Log("[Vùng đất] Đã dựng material sóng " + string.Join(", ", mats.Select(m => m.name)) + " gán vào Zone; ảnh nền: "
                      + string.Join(", ", arts));
        }

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đảo Thủy vùng đất: habitat, tướng idle và đánh, chấm ải, sóng (đang Play)", priority = 125)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(RunTour());
        }

        static IEnumerator WaitRouter(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        static IEnumerator RunTour()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*.jpg")) File.Delete(f);
            try
            {
                // toàn đảo theo giờ (sáng, hoàng hôn, đêm), phần động (hai ảnh cách 3 giây), zoom vừa, gần hải đăng / nấm lúc đêm, sảnh
                App.Save.Data.zones[(int)Elem.Thuy] = 23;
                App.Router.Go(SceneIds.Hub);
                yield return WaitRouter(SceneIds.Hub);
                App.Router.Go(SceneIds.Zone, Elem.Thuy);
                yield return WaitRouter(SceneIds.Zone);
                var z0 = Object.FindAnyObjectByType<ZoneScene>();
                DayCycle.Override = 10f;
                yield return new WaitForSecondsRealtime(1.5f);
                Debug.Log("[Thử] lúc vào đảo: " + z0.LandDebug());
                yield return Shot("vao_dao_10h");
                foreach (var (h, tag) in new[] { (10f, "10h"), (18.33f, "18h20"), (22f, "22h") })
                {
                    DayCycle.Override = h;
                    z0.LandOverview();
                    yield return new WaitForSecondsRealtime(2.5f);
                    yield return Shot($"toan_dao_{tag}_a");
                    yield return new WaitForSecondsRealtime(3f);
                    yield return Shot($"toan_dao_{tag}_b");
                }
                DayCycle.Override = 10f;
                z0.LandFocus(30, 0.55f);
                Debug.Log("[Thử] sau LandFocus(30, 0.55): " + z0.LandDebug());
                yield return new WaitForSecondsRealtime(1.5f);
                Debug.Log("[Thử] trước khi chụp zoom_vua: " + z0.LandDebug());
                yield return Shot("zoom_vua_10h");
                DayCycle.Override = 22f;
                z0.LandFocus(10, 0.8f);
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot("dem_hai_dang_a");
                yield return new WaitForSecondsRealtime(1f);
                yield return Shot("dem_hai_dang_b");
                z0.LandFocus(50, 0.8f);
                Debug.Log("[Thử] sau LandFocus(50, 0.8): " + z0.LandDebug());
                yield return new WaitForSecondsRealtime(1.5f);
                Debug.Log("[Thử] trước khi chụp dem_vuc_hang: " + z0.LandDebug());
                yield return Shot("dem_vuc_hang");
                foreach (var (h, tag) in new[] { (10f, "10h"), (18.33f, "18h20"), (22f, "22h") })
                {
                    DayCycle.Override = h;
                    App.Router.Go(SceneIds.Hub);
                    yield return WaitRouter(SceneIds.Hub);
                    yield return new WaitForSecondsRealtime(1.2f);
                    yield return Shot($"sanh_{tag}");
                }
                DayCycle.Override = null;
            }
            finally
            {
                DayCycle.Override = null;
            }
            // tiến độ đã qua → habitat cần soi (giữa khung)
            var plan = new (int prog, int[] look)[]
            {
                (0, new[] { 1, 5 }),
                (69, new[] { 70 }),
            };
            try
            {
                foreach (var (prog, look) in plan)
                {
                    App.Save.Data.zones[(int)Elem.Thuy] = prog;
                    App.Router.Go(SceneIds.Hub);
                    yield return WaitRouter(SceneIds.Hub);
                    App.Router.Go(SceneIds.Zone, Elem.Thuy);
                    yield return WaitRouter(SceneIds.Zone);
                    yield return new WaitForSecondsRealtime(0.3f);
                    yield return Shot($"p{prog:00}_vao_0");
                    yield return new WaitForSecondsRealtime(2.2f);
                    yield return Shot($"p{prog:00}_vao_1");
                    var zs = Object.FindAnyObjectByType<ZoneScene>();
                    if (!zs)
                    {
                        Debug.LogError("[Thử] Không thấy ZoneScene");
                        yield break;
                    }
                    foreach (int idx in look)
                    {
                        if (!zs.LandFocus(idx))
                        {
                            Debug.LogError("[Thử] Đảo Thủy chưa có vùng đất (zones.json land, Nhập dữ liệu)");
                            yield break;
                        }
                        yield return new WaitForSecondsRealtime(1.5f); // dựng hình tướng (mỗi khung một cái)
                        yield return Shot($"p{prog:00}_ai{idx:00}_0");
                        yield return new WaitForSecondsRealtime(0.5f);
                        yield return Shot($"p{prog:00}_ai{idx:00}_1");
                        if (!zs.LandAttack(idx)) Debug.LogWarning($"[Thử] Ải {idx}: hình tướng chưa dựng hoặc không có clip đánh");
                        for (int k = 2; k < 9; k++) // đòn đánh khoảng 1 giây
                        {
                            yield return new WaitForSecondsRealtime(0.15f);
                            yield return Shot($"p{prog:00}_ai{idx:00}_{k}");
                        }
                    }
                }
                Debug.Log("[Thử] Xong đảo Thủy vùng đất: " + Path.GetFullPath(Dir));
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đảo Thủy vùng đất: vùng boss, cờ trên đường, khoá đảo (đang Play)", priority = 127)]
        static void SectionTour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(RunSectionTour());
        }

        // shown: số vùng boss đã diễn cảnh mở (-1: bằng số vùng đã mở, không diễn)
        static IEnumerator EnterThuy(int prog, int shown = -1) => EnterLand(Elem.Thuy, prog, shown);

        static IEnumerator EnterLand(Elem e, int prog, int shown = -1)
        {
            App.Save.Data.zones[(int)e] = prog;
            var land = App.Data.Zone(e)?.land;
            if (land != null && land.Has) LandShown.Set(App.Save.Data, e, shown >= 0 ? shown : land.OpenSections(prog));
            App.Router.Go(SceneIds.Hub);
            yield return WaitRouter(SceneIds.Hub);
            App.Router.Go(SceneIds.Zone, e);
            yield return WaitRouter(SceneIds.Zone);
        }

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đảo Mộc vùng đất: toàn đảo, vùng boss, easter egg (đang Play)", priority = 130)]
        static void MocTour() => IslandTour(Elem.Moc, "moc");

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đảo Hỏa vùng đất: toàn đảo, khói, vùng boss, easter egg (đang Play)", priority = 131)]
        static void HoaTour() => IslandTour(Elem.Hoa, "hoa");

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đảo Kim vùng đất: toàn đảo, khói, vùng boss, easter egg (đang Play)", priority = 132)]
        static void KimTour() => IslandTour(Elem.Kim, "kim");

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đảo Thổ vùng đất: toàn đảo, khói, vùng boss, easter egg (đang Play)", priority = 133)]
        static void ThoTour() => IslandTour(Elem.Tho, "tho");

        static void IslandTour(Elem e, string tag)
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(RunIslandTour(e, tag));
        }

        // ảnh <tag>_*.jpg: toàn đảo, từng bệ (tiến độ 69), vùng khoá + easter egg (23, 0), lần đầu vào đảo, mở vùng 21–30, tuyệt kỹ
        static IEnumerator RunIslandTour(Elem isl, string pre)
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, pre + "_*.jpg")) File.Delete(f);
            try
            {
                DayCycle.Override = 10f;
                // mở hết: toàn đảo, từng bệ (tướng trên bệ, cờ đúng trên đường, bảng tên)
                yield return EnterLand(isl, 69);
                var zs = Object.FindAnyObjectByType<ZoneScene>();
                yield return new WaitForSecondsRealtime(2f);
                zs.LandOverview();
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot($"{pre}_69_toan");
                foreach (var idx in new[] { 1, 5, 10, 15, 20, 30, 40, 50, 60, 70 })
                {
                    zs.LandFocus(idx, 0.6f);
                    yield return new WaitForSecondsRealtime(1.6f);
                    yield return Shot($"{pre}_69_ai{idx:00}");
                }
                // vùng khoá ở tiến độ 23: phác chì + mây, đom đóm (vùng 7), pha lê (vùng 8), lá rơi (vùng 9), chim (vùng 6)
                yield return EnterLand(isl, 23);
                zs = Object.FindAnyObjectByType<ZoneScene>();
                yield return new WaitForSecondsRealtime(2f);
                zs.LandOverview();
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot($"{pre}_23_toan");
                foreach (var (idx, tag) in new[] { (40, "v6_chim"), (50, "v7_domdom"), (60, "v8_phale"), (70, "v9_laroi") })
                {
                    zs.LandFocus(idx, 0.55f);
                    yield return new WaitForSecondsRealtime(1.2f);
                    for (int k = 0; k < 3; k++)
                    {
                        yield return new WaitForSecondsRealtime(0.6f);
                        yield return Shot($"{pre}_23_{tag}_{k}");
                    }
                }
                // boss vùng khoá tung tuyệt kỹ (vùng 7: ải 50)
                zs.LandFocus(50, 0.6f);
                yield return new WaitForSecondsRealtime(1.8f);
                Debug.Log("[Thử] " + zs.LandEgg("ult", 7));
                for (int k = 0; k < 8; k++)
                {
                    yield return new WaitForSecondsRealtime(0.4f);
                    yield return Shot($"{pre}_ult7_{k}");
                }
                yield return new WaitForSecondsRealtime(1.5f);
                // tiến độ 0 (đã xem vùng 0): bướm (vùng 1), gió hang nanh (vùng 4), lá đỏ (vùng 5)
                yield return EnterLand(isl, 0, 1);
                zs = Object.FindAnyObjectByType<ZoneScene>();
                yield return new WaitForSecondsRealtime(2f);
                zs.LandOverview();
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot($"{pre}_00_toan");
                foreach (var (idx, tag) in new[] { (5, "v1_buom"), (20, "v4_gio"), (30, "v5_laroi") })
                {
                    zs.LandFocus(idx, 0.55f);
                    yield return new WaitForSecondsRealtime(1.2f);
                    for (int k = 0; k < 3; k++)
                    {
                        yield return new WaitForSecondsRealtime(0.6f);
                        yield return Shot($"{pre}_00_{tag}_{k}");
                    }
                }
                // lần đầu vào đảo: diễn mở vùng 0
                yield return EnterLand(isl, 0, 0);
                for (int k = 0; k < 10; k++)
                {
                    yield return new WaitForSecondsRealtime(k == 0 ? 0.4f : 0.6f);
                    yield return Shot($"{pre}_dau_{k:00}");
                }
                // qua ải 20 quay lại: diễn mở vùng ải 21–30 (đường cua tay áo)
                yield return EnterLand(isl, 20, 5);
                for (int k = 0; k < 14; k++)
                {
                    yield return new WaitForSecondsRealtime(k == 0 ? 0.5f : 0.55f);
                    yield return Shot($"{pre}_mo_{k:00}");
                }
                Debug.Log($"[Thử] Xong đảo {isl}: " + Path.GetFullPath(Dir));
            }
            finally
            {
                DayCycle.Override = null;
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        static IEnumerator RunSectionTour()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "vung_*.jpg")) File.Delete(f);
            try
            {
                DayCycle.Override = 10f;
                foreach (var prog in new[] { 0, 23 })
                {
                    yield return EnterThuy(prog);
                    var zs = Object.FindAnyObjectByType<ZoneScene>();
                    yield return new WaitForSecondsRealtime(2f);
                    yield return Shot($"vung_{prog:00}_vao");
                    zs.LandOverview();
                    yield return new WaitForSecondsRealtime(1.5f);
                    yield return Shot($"vung_{prog:00}_toan");
                }
                {
                    var zs = Object.FindAnyObjectByType<ZoneScene>();
                    zs.LandFocus(30, 0.6f); // ranh vùng mở / khoá (ải 30 thuộc vùng đã mở, vùng ải 40 khoá)
                    yield return new WaitForSecondsRealtime(1.5f);
                    yield return Shot("vung_23_ranh");
                }
                // lần đầu vào đảo: diễn mở vùng 0 (bến, ải 1); ghi lớp chắn chạm có bật giữa lúc diễn không
                yield return EnterThuy(0, 0);
                var cover = Object.FindAnyObjectByType<CloudCover>(FindObjectsInactive.Include);
                var blocker = typeof(CloudCover).GetField("blocker", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)?.GetValue(cover) as Image;
                for (int k = 0; k < 14; k++)
                {
                    yield return new WaitForSecondsRealtime(k == 0 ? 0.4f : 0.55f);
                    yield return Shot($"vung_dau_{k:00}");
                    if (k == 3 || k == 13) Debug.Log($"[Thử] khoá chạm lúc {k}: {(blocker ? blocker.gameObject.activeSelf : false)}");
                }
                // vừa mở vùng: đã diễn tới vùng ải 16–20, qua ải 20 (boss) quay lại: diễn mở vùng ải 21–30
                yield return EnterThuy(20, 5);
                for (int k = 0; k < 14; k++) // chờ camera, mây tan (1,1 s), bút chì ngoáy (2,6 s), tô nốt (0,6 s), cờ mọc
                {
                    yield return new WaitForSecondsRealtime(k == 0 ? 0.5f : 0.55f);
                    yield return Shot($"vung_mo_{k:00}");
                }
                // cờ đúng trên đường: khúc 50–60 (như ảnh người dùng gửi), 46
                yield return EnterThuy(70);
                var z7 = Object.FindAnyObjectByType<ZoneScene>();
                z7.LandFocus(55, 0.8f);
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot("vung_70_co_55");
                yield return EnterThuy(45);
                Object.FindAnyObjectByType<ZoneScene>().LandFocus(46, 0.8f);
                yield return new WaitForSecondsRealtime(1.5f);
                yield return Shot("vung_45_co_46");
                // nút SRDebugger (Assembly-CSharp, gọi qua reflection)
                var t = System.Type.GetType("SROptions, Assembly-CSharp");
                var cur = t?.GetProperty("Current")?.GetValue(null);
                if (cur == null) Debug.LogError("[Thử] Không thấy SROptions.Current");
                else
                {
                    t.GetMethod("PokiLockAllIslands").Invoke(cur, null);
                    Debug.Log("[Thử] Sau Khoá lại hết đảo: " + string.Join(", ", App.Save.Data.zones) + " | rương " + string.Join(", ", App.Save.Data.zoneChests));
                    t.GetProperty("PokiIslandThuy").SetValue(cur, 23);
                    Debug.Log("[Thử] Sau đặt đảo Thủy 23: " + string.Join(", ", App.Save.Data.zones));
                    App.Router.Go(SceneIds.Zone, Elem.Thuy);
                    yield return WaitRouter(SceneIds.Zone);
                    yield return new WaitForSecondsRealtime(2f);
                    yield return Shot("vung_sr_thuy_23");
                }
                Debug.Log("[Thử] Xong vùng boss: " + Path.GetFullPath(Dir));
            }
            finally
            {
                DayCycle.Override = null;
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đảo Thủy vùng đất: easter egg vùng khoá (đang Play)", priority = 128)]
        static void EggTour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(RunEggTour());
        }

        static IEnumerator RunEggTour()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "trung_*.jpg")) File.Delete(f);
            try
            {
                DayCycle.Override = 10f;
                yield return EnterThuy(23);
                var zs = Object.FindAnyObjectByType<ZoneScene>();
                yield return new WaitForSecondsRealtime(1.5f);
                // vùng 6 (ải 31–40): cá voi phun nước; vùng 7 nấm; vùng 8 tuyết; vùng 9 xoáy nước
                foreach (var (idx, zoom, sec, tag) in new[] { (40, 0.55f, 6, "v6"), (50, 0.55f, 7, "v7"), (60, 0.55f, 8, "v8"), (70, 0.55f, 9, "v9") })
                {
                    zs.LandFocus(idx, zoom);
                    yield return new WaitForSecondsRealtime(1.2f);
                    for (int k = 0; k < 4; k++)
                    {
                        yield return new WaitForSecondsRealtime(0.7f);
                        yield return Shot($"trung_{tag}_{k}");
                    }
                }
                // boss vùng khoá tung tuyệt kỹ (vùng 6: cá voi ải 40; vùng 9: rồng ải 70)
                foreach (var (idx, sec) in new[] { (40, 6), (70, 9) })
                {
                    zs.LandFocus(idx, 0.6f);
                    yield return new WaitForSecondsRealtime(1.8f);
                    Debug.Log("[Thử] " + zs.LandEgg("ult", sec));
                    for (int k = 0; k < 8; k++)
                    {
                        yield return new WaitForSecondsRealtime(0.4f);
                        yield return Shot($"trung_ult{sec}_{k}");
                    }
                    yield return new WaitForSecondsRealtime(1.5f);
                }
                // chạm liên tục 5 lần (mây lò xo, không giật), chụp dày
                zs.LandFocus(50, 0.6f);
                yield return new WaitForSecondsRealtime(1.2f);
                for (int k = 0; k < 12; k++)
                {
                    if (k < 5 && k % 1 == 0) zs.LandEgg("poke1", 7);
                    yield return new WaitForSecondsRealtime(0.15f);
                    yield return Shot($"trung_cham_{k:00}");
                }
                yield return new WaitForSecondsRealtime(1.5f);
                // chọc mây 7 lần: hắt xì (vùng 7)
                zs.LandFocus(50, 0.55f);
                yield return new WaitForSecondsRealtime(1.2f);
                int balls = App.Save.Data.balls;
                Debug.Log("[Thử] " + zs.LandEgg("poke", 7));
                for (int k = 0; k < 4; k++)
                {
                    yield return new WaitForSecondsRealtime(0.35f);
                    yield return Shot($"trung_hatxi_{k}");
                }
                yield return new WaitForSecondsRealtime(1.5f);
                Debug.Log($"[Thử] bi sau hắt xì: {balls} -> {App.Save.Data.balls}");
                // rương bí ẩn: vùng 3 đã mở (nhận được), vùng 8 còn khoá (chỉ báo)
                zs = Object.FindAnyObjectByType<ZoneScene>();
                zs.LandFocus(15, 0.6f);
                yield return new WaitForSecondsRealtime(1.2f);
                yield return Shot("trung_ruong_mo");
                balls = App.Save.Data.balls;
                Debug.Log("[Thử] " + zs.LandEgg("chest", 3) + $" bi {balls} -> {App.Save.Data.balls}");
                zs = Object.FindAnyObjectByType<ZoneScene>();
                Debug.Log("[Thử] " + zs.LandEgg("chest", 8));
                // đêm: mắt, đom đóm, nấm sáng hơn
                DayCycle.Override = 22f;
                zs.LandFocus(50, 0.55f);
                yield return new WaitForSecondsRealtime(2.2f);
                yield return Shot("trung_dem_v7");
                Debug.Log("[Thử] Xong easter egg: " + Path.GetFullPath(Dir));
            }
            finally
            {
                DayCycle.Override = null;
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Đo hiệu năng đảo vùng đất (đang Play)", priority = 129)]
        static void PerfProbe()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(RunPerfProbe());
        }

        // tắt lần lượt từng lớp của màn đảo vùng đất, ghi số liệu khung hình (UnityStats) để biết lớp nào tốn
        static IEnumerator RunPerfProbe()
        {
            if (App.Router.Current != SceneIds.Zone)
            {
                App.Router.Go(SceneIds.Zone, Elem.Thuy);
                yield return WaitRouter(SceneIds.Zone);
                yield return new WaitForSecondsRealtime(3f); // dựng hình tướng trong khung
            }
            string Stat() => $"batches {UnityStats.batches}, setpass {UnityStats.setPassCalls}, tris {UnityStats.triangles}, verts {UnityStats.vertices}, " +
                             $"draw calls {UnityStats.drawCalls}";
            IEnumerator Settle()
            {
                for (int i = 0; i < 6; i++) yield return new WaitForEndOfFrame();
            }
            var sb = new System.Text.StringBuilder("[Đo] màn đảo vùng đất\n");
            yield return Settle();
            sb.Append("gốc: ").Append(Stat()).Append('\n');
            var groups = new List<(string name, List<GameObject> gos)>();
            List<GameObject> Named(string prefix) => Object.FindObjectsByType<RectTransform>(FindObjectsSortMode.None)
                .Where(t => t.name.StartsWith(prefix)).Select(t => t.gameObject).ToList();
            groups.Add(("mây vùng khoá", Named("may_vung_")));
            groups.Add(("vành mây (IslandAnim)", Object.FindObjectsByType<IslandAnim>(FindObjectsSortMode.None).Select(a => a.gameObject).ToList()));
            groups.Add(("sáng tối (DayNight)", Object.FindObjectsByType<DayNight>(FindObjectsSortMode.None).Select(a => a.gameObject).ToList()));
            groups.Add(("cờ ải", Object.FindObjectsByType<LandFlag>(FindObjectsSortMode.None).Select(a => a.gameObject).ToList()));
            groups.Add(("habitat (ZoneNode)", Object.FindObjectsByType<ZoneNode>(FindObjectsSortMode.None).Select(a => a.gameObject).ToList()));
            groups.Add(("camera hình tướng (RT)", Object.FindObjectsByType<Camera>(FindObjectsSortMode.None).Where(c => c.targetTexture).Select(c => c.gameObject).ToList()));
            groups.Add(("phác chì", Named("phac_vung")));
            groups.Add(("easter egg trên mây", Named("trung_").Concat(Named("mat_")).ToList()));
            foreach (var (name, gos) in groups)
            {
                var was = gos.Select(g => g.activeSelf).ToList();
                foreach (var g in gos) g.SetActive(false);
                yield return Settle();
                sb.Append($"tắt {name} ({gos.Count}): ").Append(Stat()).Append('\n');
                for (int i = 0; i < gos.Count; i++)
                    if (gos[i]) gos[i].SetActive(was[i]);
                yield return Settle();
            }
            File.WriteAllText(Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "do_hieu_nang.txt"), sb.ToString());
            Debug.Log(sb.ToString());
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(82));
            Object.DestroyImmediate(tex);
        }
    }
}
