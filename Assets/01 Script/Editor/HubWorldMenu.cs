// Đưa ảnh đảo ghép (ArtGen/Islands/compose_islands.py: world, sea_tile, zone_<hệ> trong Assets/03 Art/Islands) vào prefab:
// - Screens/Hub: lớp kéo "keo" bọc anh_nen_world (HubPan trên khung_anh); trong anh_nen_world: biển lặp rộng (nhận kéo),
//   ảnh đảo có lề, vành mây quanh rìa (ra rìa mới thấy, che chỗ cho các đảo sau); nền hai bên cũng là biển lặp.
//   Bảng vùng, làng, công trình giữ nguyên chỗ (toạ độ khung 1080 x 1920 trùng với ảnh ghép).
// - Screens/Zone: biển lặp cuộn theo bản đồ (con đầu của noi_dung).
// - Lớp phần động IslandAnim (island_anim.json, sprite Islands/Anim): con của ảnh đảo sảnh (key world) và của ảnh bản đồ đảo hệ;
//   mỗi hình động sinh từ prefab mục Items/HinhDong (dựng ở đây nếu chưa có).
// Chạy lại được: dựng lại các lớp trên. Đổi lề ảnh (MARGIN của script ghép) thì sửa Margin ở đây.
using System.IO;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HubWorldMenu
    {
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string ZonePath = "Assets/04 Prefabs/Screens/Zone.prefab";
        const string ArtDir = "Assets/03 Art/Islands/";
        const string CloudPath = "Assets/03 Art/Baked/Sketch/sk_CloudPuff.png";
        const string AnimJson = ArtDir + "island_anim.json";
        const string AnimItemPath = "Assets/04 Prefabs/Items/HinhDong.prefab";
        const float FW = 1080, FH = 1920, Margin = 200; // khung sảnh và lề ảnh đảo (theo script ghép)
        const float Pan = 340; // giới hạn kéo mỗi phía (đơn vị khung)
        // vùng có đất trong khung (gồm phần lấn ra lề): mây đặt ngoài vùng này
        const float LandL = -160, LandR = 1240, LandT = -70;

        [MenuItem("PokiClash/Prefab/Đảo sảnh: ghép ảnh, kéo, mây viền", priority = 62)]
        static void Build()
        {
            foreach (var f in Directory.GetFiles(ArtDir, "*.png", SearchOption.AllDirectories))
                AssetDatabase.ImportAsset(f.Replace('\\', '/'), ImportAssetOptions.ForceUpdate);
            AssetDatabase.ImportAsset(AnimJson, ImportAssetOptions.ForceUpdate);
            var anim = AssetDatabase.LoadAssetAtPath<TextAsset>(AnimJson);
            var world = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + "world.png");
            var sea = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + "sea_tile.png");
            var cloud = AssetDatabase.LoadAssetAtPath<Sprite>(CloudPath);
            if (!world || !sea || !cloud)
            {
                Debug.LogError("[Sảnh] Thiếu world.png / sea_tile.png trong " + ArtDir + " hoặc sk_CloudPuff: chạy ArtGen/Islands/compose_islands.py trước.");
                return;
            }
            ArtImporter.BuildLibrary();
            AnimItem();
            BuildHub(world, sea, cloud, anim);
            BuildZone(anim);
        }

        static void BuildHub(Sprite world, Sprite sea, Sprite cloud, TextAsset anim)
        {
            var contents = PrefabUtility.LoadPrefabContents(HubPath);
            try
            {
                RectTransform Find(string n)
                {
                    foreach (var t in contents.GetComponentsInChildren<RectTransform>(true))
                        if (t.name == n) return t;
                    return null;
                }
                var khung = Find("khung_anh");
                var frame = Find("anh_nen_world");

                // lớp kéo bọc khung ảnh (AspectRatioFitter của anh_nen_world tự giữ vị trí, nên kéo lớp cha)
                var keo = Find("keo");
                if (!keo)
                {
                    keo = NewRect("keo", khung);
                    Stretch(keo, Vector2.zero, Vector2.one);
                    keo.SetSiblingIndex(frame.GetSiblingIndex());
                    frame.SetParent(keo, false);
                }
                var frameImg = frame.GetComponent<Image>();
                frameImg.sprite = null;
                frameImg.enabled = false;
                frame.GetComponent<AspectRatioFitter>().aspectRatio = FW / FH;
                var sides = Find("nen_hai_ben").GetComponent<Image>();
                Tiled(sides, sea);
                sides.raycastTarget = false;

                foreach (var n in new[] { "bien", "dao", "may_vien" })
                {
                    var old = frame.Find(n);
                    if (old) Object.DestroyImmediate(old.gameObject);
                }
                // biển rộng: phủ cả khi kéo quá giới hạn; nhận kéo cho vùng trống
                var bien = NewRect("bien", frame);
                Stretch(bien, new Vector2(-0.8f, -0.5f), new Vector2(1.8f, 1.5f));
                var bienImg = bien.gameObject.AddComponent<Image>();
                Tiled(bienImg, sea);
                bienImg.raycastTarget = true;
                bien.SetSiblingIndex(0);

                var dao = NewRect("dao", frame);
                Stretch(dao, new Vector2(-Margin / FW, -Margin / FH), new Vector2(1 + Margin / FW, 1 + Margin / FH));
                var daoImg = dao.gameObject.AddComponent<Image>();
                daoImg.sprite = world;
                daoImg.raycastTarget = false;
                dao.SetSiblingIndex(1);
                AnimLayer(dao, anim, "world");

                var ring = NewRect("may_vien", frame);
                Stretch(ring, Vector2.zero, Vector2.one);
                ring.SetSiblingIndex(2);
                Clouds(ring, cloud, Find("may_0").GetComponent<Image>().material); // sprite nướng sẵn cần material của mây có sẵn

                var pan = khung.GetComponent<HubPan>();
                if (!pan) pan = khung.gameObject.AddComponent<HubPan>();
                pan.Setup(keo, new Vector2(Pan / FW, Pan / FH));

                PrefabUtility.SaveAsPrefabAsset(contents, HubPath);
                Debug.Log($"[Sảnh] Đã dựng lớp kéo, biển, đảo ghép, vành mây ({ring.childCount} cụm) trong {HubPath}.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // vành mây: hai hàng so le dọc bốn phía, ngoài vùng có đất
        static void Clouds(RectTransform ring, Sprite cloud, Material mat)
        {
            var r = new System.Random(7);
            int n = 0;
            void Puff(float x, float y, float w)
            {
                var rt = NewRect($"may_{n++}", ring);
                rt.anchorMin = rt.anchorMax = new Vector2(x / FW, 1 - y / FH);
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(w, w * cloud.rect.height / cloud.rect.width);
                rt.localScale = new Vector3(r.NextDouble() < 0.5 ? -1 : 1, 1, 1);
                var img = rt.gameObject.AddComponent<Image>();
                img.sprite = cloud;
                img.material = mat;
                img.raycastTarget = false;
                var b = rt.gameObject.AddComponent<Bob>();
                b.amount = 4 + (float)r.NextDouble() * 6;
                b.period = 3.5f + (float)r.NextDouble() * 3;
            }
            float J(float a) => (float)(r.NextDouble() * 2 - 1) * a;
            for (int row = 0; row < 3; row++)
            {
                float d = row * 150; // hàng ngoài
                float w = 420 + row * 60;
                for (float x = LandL - 300; x <= LandR + 300; x += 230)
                {
                    Puff(x + J(40) + row * 115, LandT - 70 - d + J(25), w + J(60));
                    Puff(x + J(40) + row * 115, FH + 120 + d + J(25), w + J(60)); // dưới đáy khung: hàng nút đã che phần đáy đảo
                }
                for (float y = LandT - 150; y <= FH + 150; y += 200)
                {
                    Puff(LandL - 90 - d + J(25), y + J(40) + row * 100, w + J(60));
                    Puff(LandR + 90 + d + J(25), y + J(40) + row * 100, w + J(60));
                }
            }
        }

        static void BuildZone(TextAsset anim)
        {
            var contents = PrefabUtility.LoadPrefabContents(ZonePath);
            try
            {
                var scene = contents.GetComponent<ZoneScene>();
                var so = new SerializedObject(scene);
                var content = (RectTransform)so.FindProperty("p.content").objectReferenceValue;
                var old = content.Find("bien_cuon");
                if (old) Object.DestroyImmediate(old.gameObject);
                var rt = NewRect("bien_cuon", content);
                Stretch(rt, Vector2.zero, Vector2.one);
                rt.SetSiblingIndex(0);
                var img = rt.gameObject.AddComponent<Image>();
                img.raycastTarget = false;
                so.FindProperty("seaScroll").objectReferenceValue = img;
                var map = (Image)so.FindProperty("p.map").objectReferenceValue;
                so.FindProperty("mapAnim").objectReferenceValue = AnimLayer(map.rectTransform, anim, "");
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, ZonePath);
                Debug.Log($"[Đảo] Đã thêm biển cuộn vào {ZonePath}.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // prefab mục hình động: Image không nhận chạm, giữ tỉ lệ ảnh, neo góc dưới trái (IslandAnim đặt toạ độ từ góc này)
        static Image AnimItem()
        {
            var item = AssetDatabase.LoadAssetAtPath<GameObject>(AnimItemPath);
            if (!item)
            {
                var go = new GameObject("HinhDong", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                var img = go.GetComponent<Image>();
                img.raycastTarget = false;
                img.preserveAspect = true;
                var rt = (RectTransform)go.transform;
                rt.anchorMin = rt.anchorMax = Vector2.zero;
                rt.pivot = new Vector2(0.5f, 0.5f);
                item = PrefabUtility.SaveAsPrefabAsset(go, AnimItemPath);
                Object.DestroyImmediate(go);
            }
            return item.GetComponent<Image>();
        }

        // lớp phần động phủ kín ảnh cha (dựng lại nếu đã có)
        static IslandAnim AnimLayer(RectTransform parent, TextAsset json, string key)
        {
            var old = parent.Find("dong");
            if (old) Object.DestroyImmediate(old.gameObject);
            var rt = NewRect("dong", parent);
            Stretch(rt, Vector2.zero, Vector2.one);
            rt.SetSiblingIndex(0); // ngay trên ảnh, dưới các lớp con khác (đường, ải trên bản đồ đảo hệ)
            var a = rt.gameObject.AddComponent<IslandAnim>();
            a.Setup(json, key, AnimItem());
            return a;
        }

        static void Tiled(Image img, Sprite sea)
        {
            img.sprite = sea;
            img.type = Image.Type.Tiled;
            img.color = Color.white;
            var fit = img.GetComponent<AspectRatioFitter>();
            if (fit) fit.aspectRatio = FW / FH;
        }

        static RectTransform NewRect(string name, Transform parent)
        {
            var rt = new GameObject(name, typeof(RectTransform)).GetComponent<RectTransform>();
            rt.SetParent(parent, false);
            return rt;
        }

        static void Stretch(RectTransform rt, Vector2 min, Vector2 max)
        {
            rt.anchorMin = min;
            rt.anchorMax = max;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = rt.offsetMax = Vector2.zero;
        }
    }
}
