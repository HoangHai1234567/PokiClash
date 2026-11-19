// Gộp lệnh vẽ (batches) bằng Sprite Atlas (người dùng 2026-11-18: "tris nhiều quá, batches cũng nhiều so với game 2D", "làm nốt tối
// ưu batches đi"). Đo trên màn đảo vùng đất: hình lẻ mỗi thứ một texture xen kẽ nhau làm vỡ lệnh vẽ (cờ ải 8 hình: ô đá, cán, 6 khung
// vải; hiệu ứng đảo anim_*; mây, chim, thuyền; easter egg, rương, bút chì).
// - "PokiClash/Tối ưu/Sprite Atlas đảo (dựng lại)": bật Sprite Atlas V2 cho project (EditorSettings), dựng
//   Assets/03 Art/Islands/dao_hinh_roi.spriteatlasv2 gồm thư mục Islands/Co, Islands/Anim, rương
//   Pachinko/pk_ruong_go, icon bảng tên bệ (khoá, dấu qua, vương miện, boss; cả 75 icon thì cần texture 4096, không gom); không xoay, không gói sát (Image vẽ cả khung chữ nhật của hình), lề 4, không mipmap, 2048, điện thoại ASTC 6x6;
//   mỗi đảo vùng đất một atlas riêng dao_hinh_roi_<đảo>.spriteatlasv2 cho mây, chim, thuyền cắt từ ảnh nền (land_<đảo>_may_*, chim_*,
//   thuyen; mỗi lúc chỉ mở một đảo, gom chung thì tràn 2048); gói ngay. Chỉ hình trong atlas đổi cách vẽ, các màn khác giữ nguyên.
//   Ảnh nền lớn, biển lặp (Tiled) không đưa vào. Hình nguồn trong atlas nhập không nén (ArtImporter hỏi InAtlas; nguồn nén sẵn thì
//   gói lại mờ, Unity báo lỗi), menu nhập lại các hình nguồn trước khi gói.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.U2D;
using UnityEngine;
using UnityEngine.U2D;

namespace PokiClash.EditorTools
{
    public static class AtlasMenu
    {
        const string AtlasPath = "Assets/03 Art/Islands/dao_hinh_roi.spriteatlasv2";
        static readonly string[] Folders = { "Assets/03 Art/Islands/Co", "Assets/03 Art/Islands/Anim" };
        const string IslandDir = "Assets/03 Art/Islands";
        static readonly string[] Files =
        {
            "Assets/03 Art/Pachinko/pk_ruong_go.png",
            // icon trên bảng tên bệ ải (ZoneNode): khoá, dấu qua, vương miện mini boss, boss
            "Assets/03 Art/Fallback/Icons/lock.png", "Assets/03 Art/Fallback/Icons/check.png",
            "Assets/03 Art/Fallback/Icons/crownSm.png", "Assets/03 Art/Fallback/Icons/boss.png",
        };

        // hình thuộc atlas đảo: trong thư mục Co, Anim; danh sách Files; mây, chim, thuyền cắt từ ảnh nền đảo vùng đất
        public static bool InAtlas(string path)
        {
            path = path.Replace('\\', '/');
            if (Folders.Any(f => path.StartsWith(f + "/")) || Files.Contains(path)) return true;
            if (!path.StartsWith(IslandDir + "/land_") || !path.EndsWith(".png") || path.IndexOf('/', IslandDir.Length + 1) >= 0) return false;
            var n = Path.GetFileNameWithoutExtension(path);
            return n.Contains("_may_") || n.Contains("_chim_") || n.EndsWith("_thuyen");
        }

        [MenuItem("PokiClash/Tối ưu/Sprite Atlas đảo (dựng lại)", priority = 200)]
        static void Build()
        {
            if (EditorSettings.spritePackerMode != SpritePackerMode.SpriteAtlasV2)
            {
                EditorSettings.spritePackerMode = SpritePackerMode.SpriteAtlasV2;
                Debug.Log("[Atlas] Bật Sprite Atlas V2 cho project");
            }
            // hình nguồn nhập lại theo luật không nén (ArtImporter → InAtlas) trước khi gói
            var srcs = AssetDatabase.FindAssets("t:Texture2D", Folders).Select(AssetDatabase.GUIDToAssetPath)
                .Concat(Files).Concat(Directory.GetFiles(IslandDir, "land_*.png").Select(f => f.Replace('\\', '/')))
                .Where(InAtlas).Distinct()
                .Where(x => AssetImporter.GetAtPath(x) is TextureImporter t && t.textureCompression != TextureImporterCompression.Uncompressed)
                .ToList();
            AssetDatabase.StartAssetEditing();
            try
            {
                foreach (var x in srcs) AssetDatabase.ImportAsset(x, ImportAssetOptions.ForceUpdate);
            }
            finally
            {
                AssetDatabase.StopAssetEditing();
            }
            if (srcs.Count > 0) Debug.Log($"[Atlas] Nhập lại {srcs.Count} hình nguồn không nén");
            var objs = new List<Object>();
            foreach (var f in Folders)
            {
                var o = AssetDatabase.LoadAssetAtPath<DefaultAsset>(f);
                if (o) objs.Add(o);
                else Debug.LogWarning("[Atlas] Thiếu thư mục " + f);
            }
            foreach (var f in Files)
            {
                var o = AssetDatabase.LoadAssetAtPath<Texture2D>(f);
                if (o) objs.Add(o);
                else Debug.LogWarning("[Atlas] Thiếu " + f);
            }
            var made = new List<string> { Pack(AtlasPath, objs) };
            // hình rời cắt từ ảnh nền từng đảo vùng đất (land_<đảo>_may_*, chim_*, thuyen)
            var islands = Directory.GetFiles(IslandDir, "land_*_may_1.png").Select(f => Path.GetFileNameWithoutExtension(f))
                .Select(n => n.Substring(5, n.Length - 5 - "_may_1".Length));
            foreach (var isl in islands)
            {
                var list = new List<Object>();
                foreach (var f in Directory.GetFiles(IslandDir, $"land_{isl}_*.png"))
                {
                    var n = Path.GetFileNameWithoutExtension(f);
                    if (!(n.Contains("_may_") || n.Contains("_chim_") || n.EndsWith("_thuyen"))) continue;
                    var o = AssetDatabase.LoadAssetAtPath<Texture2D>(IslandDir + "/" + n + ".png");
                    if (o) list.Add(o);
                }
                if (list.Count > 0) made.Add(Pack($"{IslandDir}/dao_hinh_roi_{isl}.spriteatlasv2", list));
            }
            SpriteAtlasUtility.PackAllAtlases(EditorUserBuildSettings.activeBuildTarget);
            foreach (var path in made.Where(x => x != null))
            {
                var packed = AssetDatabase.LoadAssetAtPath<SpriteAtlas>(path);
                Debug.Log($"[Atlas] Đã dựng {path}: {(packed ? packed.spriteCount : 0)} hình");
            }
        }

        // dựng lại một atlas (xoá bản cũ), trả đường dẫn; gói sau
        static string Pack(string path, List<Object> objs)
        {
            if (AssetDatabase.LoadMainAssetAtPath(path)) AssetDatabase.DeleteAsset(path);
            var atlas = new SpriteAtlasAsset();
            atlas.Add(objs.ToArray());
            SpriteAtlasAsset.Save(atlas, path);
            AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
            var imp = AssetImporter.GetAtPath(path) as SpriteAtlasImporter;
            if (!imp)
            {
                Debug.LogError("[Atlas] Không đọc được importer của " + path);
                return null;
            }
            imp.includeInBuild = true;
            imp.packingSettings = new SpriteAtlasPackingSettings
            {
                enableRotation = false, // UI không vẽ hình xoay trong atlas
                enableTightPacking = false, // Image vẽ cả khung chữ nhật: gói sát làm lẹm hình bên cạnh
                padding = 4,
            };
            imp.textureSettings = new SpriteAtlasTextureSettings
            {
                readable = false, generateMipMaps = false, sRGB = true, filterMode = FilterMode.Bilinear,
            };
            var def = imp.GetPlatformSettings("DefaultTexturePlatform");
            def.maxTextureSize = 2048;
            def.textureCompression = TextureImporterCompression.Compressed;
            imp.SetPlatformSettings(def);
            foreach (var pf in new[] { "Android", "iPhone" })
            {
                var ps = imp.GetPlatformSettings(pf);
                ps.overridden = true;
                ps.maxTextureSize = 2048;
                ps.format = TextureImporterFormat.ASTC_6x6;
                imp.SetPlatformSettings(ps);
            }
            imp.SaveAndReimport();
            return path;
        }
    }
}
