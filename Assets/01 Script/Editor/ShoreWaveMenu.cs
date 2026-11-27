// Sóng gần bờ cho sảnh và đảo Casino như biển Nhà (người dùng 2026-11-27: "làm thêm shader sóng gần bờ như của home cho đảo chính và
// đảo casino"). Mặt nạ bờ: ArtGen/Islands/bo_song/make_shore.py -> 03 Art/Baked/Shore/sanh_bo.png, casino_bo.png (R rộng, G vừa, B sắc
// sát bờ, A = 1; khung ảnh đảo nới Pad đơn vị mỗi bên).
// Menu "PokiClash/Prefab/Sảnh và đảo/Sóng bờ: sảnh, Casino" hoặc cờ Temp/shore_wave.flag (chạy khi Unity không Play, không biên dịch):
// - lớp "bien_bo" (Image không ảnh, vật liệu PokiClash/UIHomeSea kiểu biển lát) ngay trên lớp biển lát của màn, dưới các đảo: sảnh
//   (Screens/Hub, trong "dao", trên bien_lat), Casino (Screens/Casino, trong anh_nen_casino, trên bien, dưới dat); khung = khung cha nới Pad;
// - vật liệu Baked/Shore/<tên>.mat: ảnh biển lát lấy từ lớp biển của màn, số lặp và độ lệch ô (_TileST) tính theo vị trí thật của lớp
//   biển để ô lát khớp liền; dải mép, vạch bọt mảnh, nhạt như Nhà (home_sea.mat); nhiễu lắc quy theo đơn vị màn cho cùng nhịp với Nhà.
//   Đêm: shader tối biển xa bờ theo _PokiNight (cùng màu DayCycle.SeaNight như lớp biển lát tối qua DayNight.seaDark).
// Chạy lại được.
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ShoreWaveMenu
    {
        const float Pad = 640; // phải khớp PAD của make_shore.py
        const string Dir = "Assets/03 Art/Baked/Shore/";
        // Nhà: ảnh nền 6975 x 4198 đơn vị; nhiễu của home_sea.mat tính trên khung đó (quy ra đơn vị màn cho sảnh, Casino cùng nhịp)
        const float HomeW = 6975, HomeH = 4198;

        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/shore_wave.flag"));
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            if (!File.Exists(Flag)) return;
            File.Delete(Flag);
            Build();
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Sóng bờ: sảnh, Casino")]
        static void Build()
        {
            Patch("Assets/04 Prefabs/Screens/Hub.prefab", "sanh_bo", "dao", "bien_lat", null);
            Patch("Assets/04 Prefabs/Screens/Casino.prefab", "casino_bo", "anh_nen_casino", "bien", "dat");
            AssetDatabase.SaveAssets();
            SeaWorldMenu.Apply("hub", "casino"); // biển chung: ô lát theo thế giới (_TileWorld), gốc biển của màn (2026-11-27)
            Debug.Log("[Sóng bờ] Xong");
        }

        // parentName: khung ảnh đảo (mặt nạ phủ khung này nới Pad); seaName: lớp biển lát của màn (con của parent); below: con đặt lớp
        // sóng ngay trước (null: ngay sau lớp biển)
        static void Patch(string prefab, string name, string parentName, string seaName, string below)
        {
            var mask = DataTex(Dir + name + ".png", false, 2048);
            var flow = DataTex("Assets/03 Art/Baked/Home/home_sea_flow.png", true, 256);
            var caustic = DataTex("Assets/03 Art/Baked/Home/home_sea_caustic.png", true, 512);
            var shader = Shader.Find("PokiClash/UIHomeSea");
            if (!mask || !flow || !shader)
            {
                Debug.LogError($"[Sóng bờ] Thiếu mặt nạ {Dir}{name}.png (chạy ArtGen/Islands/bo_song/make_shore.py), ảnh nhiễu của Nhà hoặc shader UIHomeSea");
                return;
            }
            var root = PrefabUtility.LoadPrefabContents(prefab);
            try
            {
                var parent = root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == parentName);
                var seaRt = parent ? parent.Find(seaName) as RectTransform : null;
                var sea = seaRt ? seaRt.GetComponent<Image>() : null;
                if (!parent || !sea || !sea.sprite)
                {
                    Debug.LogError($"[Sóng bờ] {prefab} thiếu {parentName}/{seaName} (lớp biển lát)");
                    return;
                }
                var rt = parent.Find("bien_bo") as RectTransform;
                if (!rt)
                {
                    var go = new GameObject("bien_bo", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                    go.layer = seaRt.gameObject.layer;
                    rt = (RectTransform)go.transform;
                    rt.SetParent(parent, false);
                }
                // thứ tự vẽ: ngay trước `below` (đảo), không thì ngay sau lớp biển
                var under = below != null ? parent.Find(below) : null;
                rt.SetAsLastSibling();
                rt.SetSiblingIndex(under ? under.GetSiblingIndex() : seaRt.GetSiblingIndex() + 1);
                rt.anchorMin = Vector2.zero;
                rt.anchorMax = Vector2.one;
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.offsetMin = -Vector2.one * Pad;
                rt.offsetMax = Vector2.one * Pad;
                rt.localScale = Vector3.one;
                rt.localRotation = Quaternion.identity;

                // ô lát của lớp biển: cỡ (đơn vị local của lớp biển) và gốc ở góc dưới trái khung lớp biển
                var canvas = seaRt.GetComponentInParent<Canvas>(true);
                float refPpu = canvas ? canvas.referencePixelsPerUnit : 100;
                float ppu = sea.sprite.pixelsPerUnit / refPpu * Mathf.Max(0.01f, sea.pixelsPerUnitMultiplier);
                var tile = sea.sprite.rect.size / ppu;
                Vector3 seaBL = seaRt.TransformPoint(seaRt.rect.min), boBL = rt.TransformPoint(rt.rect.min);
                Vector2 off = seaRt.InverseTransformVector(boBL - seaBL);
                Vector2 size = seaRt.InverseTransformVector(rt.TransformVector(rt.rect.size));
                var st = new Vector4(size.x / tile.x, size.y / tile.y, Frac(off.x / tile.x), Frac(off.y / tile.y));

                var matPath = Dir + name + ".mat";
                var mat = AssetDatabase.LoadAssetAtPath<Material>(matPath);
                if (!mat)
                {
                    mat = new Material(shader);
                    AssetDatabase.CreateAsset(mat, matPath);
                }
                mat.shader = shader;
                mat.SetTexture("_SeaTex", mask);
                mat.SetTexture("_FlowTex", flow);
                if (caustic) mat.SetTexture("_CausticTex", caustic);
                mat.SetTexture("_TileTex", sea.sprite.texture);
                mat.SetVector("_TileST", st);
                mat.SetFloat("_TileMix", 1);
                mat.SetFloat("_FoamAlpha", 0.55f);
                mat.SetFloat("_FoamCut", 0.72f);
                mat.SetFloat("_EdgeCut", 0.45f);
                mat.SetColor("_EdgeCol", new Color(0.624f, 0.89f, 0.949f, 0.35f));
                mat.SetFloat("_Grain", 0);
                mat.SetFloat("_Crisp", 1);
                mat.SetFloat("_Steps", 0);
                mat.SetFloat("_RiverFoam", 0);
                // nhiễu lắc dải, bọt: home_sea.mat tính trên khung 6975 x 4198; quy theo cỡ khung lớp này (đơn vị màn) cho cùng nhịp
                Vector2 box = rt.rect.size;
                float k = (HomeW + HomeH) / Mathf.Max(1, box.x + box.y);
                mat.SetFloat("_FlowScale", 2 * Mathf.Min(box.x, box.y) / HomeH);
                mat.SetVector("_FlowFine", new Vector4(6 * box.x / HomeW, 3 * box.y / HomeH, 0, 0));
                mat.SetFloat("_Move", 0.055f * k);
                mat.SetFloat("_FoamMove", 0.01f * k);
                EditorUtility.SetDirty(mat);

                var img = rt.GetComponent<Image>();
                img.sprite = null;
                img.color = Color.white;
                img.material = mat;
                img.raycastTarget = false;
                PrefabUtility.SaveAsPrefabAsset(root, prefab);
                Debug.Log($"[Sóng bờ] {prefab}: bien_bo {box} (khung {parent.rect.size} nới {Pad}), ô lát {tile}, _TileST {st}");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static float Frac(float x) => x - Mathf.Floor(x);

        // ảnh dữ liệu: không sRGB, không mipmap, không nén (như HomeSceneMenu.DataTex)
        static Texture2D DataTex(string path, bool repeat, int max)
        {
            if (!File.Exists(path)) return null;
            AssetDatabase.ImportAsset(path);
            var ti = (TextureImporter)AssetImporter.GetAtPath(path);
            if (!ti) return null;
            var wrap = repeat ? TextureWrapMode.Repeat : TextureWrapMode.Clamp;
            if (ti.sRGBTexture || ti.mipmapEnabled || ti.textureCompression != TextureImporterCompression.Uncompressed ||
                ti.textureType != TextureImporterType.Default || ti.wrapMode != wrap || ti.maxTextureSize != max)
            {
                ti.textureType = TextureImporterType.Default;
                ti.sRGBTexture = false;
                ti.mipmapEnabled = false;
                ti.alphaSource = TextureImporterAlphaSource.FromInput;
                ti.wrapMode = wrap;
                ti.filterMode = FilterMode.Bilinear;
                ti.textureCompression = TextureImporterCompression.Uncompressed;
                ti.maxTextureSize = max;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(path);
        }
    }
}
