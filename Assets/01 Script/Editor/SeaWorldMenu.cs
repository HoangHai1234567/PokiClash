// Biển chung của sảnh, Nhà, đảo Casino (người dùng 2026-11-27: "nước của 3 đảo phải liền mạch nhau, move đi phải mượt"; App/SeaAnchor.cs):
// - vật liệu Resources/SeaWorld.mat (shader PokiClash/UISeaWorld, _SeaTile = Islands/sanh_bien): chuyến tàu (ShipVoyage) nạp lúc chạy,
//   lớp biển mở của ba màn dùng chung;
// - mỗi màn: SeaAnchor trên lớp kéo (Hub: dao, Nhà: the_gioi, Casino: anh_nen_casino); lớp biển mở (Hub bien_lat, Nhà bien_ngoai,
//   Casino bien) đổi sang SeaWorld.mat, kiểu Simple (shader bỏ uv), ảnh vẫn là sanh_bien (ShoreWaveMenu đọc ảnh này);
// - vật liệu UIHomeSea của biển trong ảnh nền Nhà (home_sea.mat) và sóng bờ (sanh_bo.mat, casino_bo.mat): _TileWorld = 1, _TileTex =
//   sanh_bien (Casino trước dùng tau_bien), nên biển trong ảnh, sóng bờ, biển mở, chuyến tàu là một mặt nước ghim theo thế giới;
// - Nhà: LandView.hardEdge = (150, 150, 150, 0): rừng rìa cắt thẳng ở mép trái, phải, trên; kéo quá tay không lộ đường cắt.
// Menu "PokiClash/Prefab/Sảnh và đảo/Biển chung: sảnh, Nhà, Casino" hoặc cờ Temp/sea_world.flag (nội dung: hub, home, casino, cách bởi
// dấu phẩy; trống là cả ba; chạy khi Unity không Play, không biên dịch). HomeSeaOutMenu (Nhà) và ShoreWaveMenu (sảnh, Casino) gọi lại
// sau khi vá xong. Chạy lại được.
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class SeaWorldMenu
    {
        const string MatPath = "Assets/Resources/SeaWorld.mat";
        const string TilePath = "Assets/03 Art/Islands/sanh_bien.png";
        const string ShaderName = "PokiClash/UISeaWorld";

        sealed class Spec
        {
            public string key, prefab, anchor, sea, shore;
            public Vector4 hard;
        }

        static readonly Spec[] Screens =
        {
            new Spec { key = "hub", prefab = "Assets/04 Prefabs/Screens/Hub.prefab", anchor = "dao", sea = "bien_lat", shore = "Assets/03 Art/Baked/Shore/sanh_bo.mat" },
            new Spec
            {
                key = "home", prefab = "Assets/04 Prefabs/Screens/Home.prefab", anchor = "the_gioi", sea = "bien_ngoai", shore = "Assets/03 Art/Home/home_sea.mat",
                hard = new Vector4(150, 150, 150, 0),
            },
            new Spec { key = "casino", prefab = "Assets/04 Prefabs/Screens/Casino.prefab", anchor = "anh_nen_casino", sea = "bien", shore = "Assets/03 Art/Baked/Shore/casino_bo.mat" },
        };

        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/sea_world.flag"));
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            if (!File.Exists(Flag)) return;
            string text = File.ReadAllText(Flag).Trim();
            File.Delete(Flag);
            var keys = text.Length == 0 ? Screens.Select(s => s.key).ToArray() : text.Split(',', ' ', '\n', '\r').Where(k => k.Length > 0).ToArray();
            Apply(keys);
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Biển chung: sảnh, Nhà, Casino")]
        static void All() => Apply("hub", "home", "casino");

        public static void Apply(params string[] keys)
        {
            var mat = Mat();
            if (!mat) return;
            var tile = AssetDatabase.LoadAssetAtPath<Texture2D>(TilePath);
            var sprite = AssetDatabase.LoadAssetAtPath<Sprite>(TilePath);
            foreach (var s in Screens)
                if (keys.Contains(s.key))
                    Patch(s, mat, tile, sprite);
            AssetDatabase.SaveAssets();
            Debug.Log("[Biển chung] Xong: " + string.Join(", ", keys));
        }

        static Material Mat()
        {
            var shader = Shader.Find(ShaderName);
            var tile = AssetDatabase.LoadAssetAtPath<Texture2D>(TilePath);
            if (!shader || !tile)
            {
                Debug.LogError($"[Biển chung] Thiếu shader {ShaderName} hoặc {TilePath}");
                return null;
            }
            var mat = AssetDatabase.LoadAssetAtPath<Material>(MatPath);
            if (!mat)
            {
                mat = new Material(shader) { name = "SeaWorld" };
                AssetDatabase.CreateAsset(mat, MatPath);
            }
            mat.shader = shader;
            mat.SetTexture("_SeaTile", tile);
            mat.SetColor("_Color", Color.white);
            EditorUtility.SetDirty(mat);
            return mat;
        }

        static void Patch(Spec s, Material mat, Texture2D tile, Sprite sprite)
        {
            var root = PrefabUtility.LoadPrefabContents(s.prefab);
            string note;
            try
            {
                var anchor = root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == s.anchor);
                if (!anchor)
                {
                    Debug.LogError($"[Biển chung] {s.prefab} thiếu lớp kéo {s.anchor}");
                    return;
                }
                if (!anchor.GetComponent<SeaAnchor>()) anchor.gameObject.AddComponent<SeaAnchor>();
                var sea = anchor.GetComponentsInChildren<Image>(true).FirstOrDefault(i => i.name == s.sea);
                if (sea)
                {
                    sea.material = mat;
                    sea.type = Image.Type.Simple;
                    if (sprite) sea.sprite = sprite;
                    sea.raycastTarget = false;
                }
                note = $"SeaAnchor trên {s.anchor}, lớp biển {(sea ? s.sea + " " + sea.rectTransform.rect.size : "KHÔNG THẤY " + s.sea)}";
                if (s.hard != Vector4.zero)
                {
                    var lv = root.GetComponentInChildren<LandView>(true);
                    if (lv)
                    {
                        var so = new SerializedObject(lv);
                        var p = so.FindProperty("hardEdge");
                        if (p != null)
                        {
                            p.vector4Value = s.hard;
                            so.ApplyModifiedPropertiesWithoutUndo();
                            note += $", LandView.hardEdge {s.hard}";
                        }
                    }
                    else note += ", không thấy LandView";
                }
                PrefabUtility.SaveAsPrefabAsset(root, s.prefab);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            var shore = AssetDatabase.LoadAssetAtPath<Material>(s.shore);
            if (shore)
            {
                shore.SetFloat("_TileWorld", 1);
                shore.SetTexture("_TileTex", tile);
                EditorUtility.SetDirty(shore);
                AssetDatabase.SaveAssetIfDirty(shore); // lần chạy đầu 2026-11-27 SetFloat không xuống file nếu chỉ chờ SaveAssets cuối
                // vẫn chưa xuống file thì sửa thẳng YAML (vật liệu là văn bản)
                string full = Path.GetFullPath(s.shore), text = File.ReadAllText(full);
                if (text.Contains("_TileWorld: 0"))
                {
                    File.WriteAllText(full, text.Replace("_TileWorld: 0", "_TileWorld: 1"));
                    AssetDatabase.ImportAsset(s.shore, ImportAssetOptions.ForceUpdate);
                }
                note += $", {Path.GetFileName(s.shore)} _TileWorld {AssetDatabase.LoadAssetAtPath<Material>(s.shore).GetFloat("_TileWorld")}";
            }
            else note += $", thiếu {s.shore}";
            Debug.Log($"[Biển chung] {s.prefab}: {note}");
        }
    }
}
