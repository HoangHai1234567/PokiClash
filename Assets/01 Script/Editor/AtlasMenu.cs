// Gộp lệnh vẽ (batches) bằng Sprite Atlas (người dùng 2026-11-18: "tris nhiều quá, batches cũng nhiều so với game 2D", "làm nốt tối
// ưu batches đi"). Đo trên màn đảo vùng đất: hình lẻ mỗi thứ một texture xen kẽ nhau làm vỡ lệnh vẽ (cờ ải 8 hình: ô đá, cán, 6 khung
// vải; hiệu ứng đảo anim_*; mây, chim, thuyền; easter egg, rương, bút chì).
// - "PokiClash/Tối ưu/Sprite Atlas đảo (dựng lại)": bật Sprite Atlas V2 cho project (EditorSettings), dựng
//   Assets/03 Art/Islands/dao_hinh_roi.spriteatlasv2 gồm thư mục Islands/Co, Islands/Anim, mây land_thuy_may_*, chim, thuyền, rương
//   Pachinko/pk_ruong_go, icon bảng tên bệ (khoá, dấu qua, vương miện, boss; cả 75 icon thì cần texture 4096, không gom); không xoay, không gói sát (Image vẽ cả khung chữ nhật của hình), lề 4, không mipmap, 2048, điện thoại ASTC 6x6;
//   gói ngay. Chỉ hình trong atlas đổi cách vẽ, các màn khác giữ nguyên. Ảnh nền lớn, biển lặp (Tiled) không đưa vào.
using System.Collections.Generic;
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
        static readonly string[] Files =
        {
            "Assets/03 Art/Islands/land_thuy_may_1.png", "Assets/03 Art/Islands/land_thuy_may_2.png",
            "Assets/03 Art/Islands/land_thuy_chim_1.png", "Assets/03 Art/Islands/land_thuy_chim_2.png", "Assets/03 Art/Islands/land_thuy_chim_3.png",
            "Assets/03 Art/Islands/land_thuy_thuyen.png", "Assets/03 Art/Pachinko/pk_ruong_go.png",
            // icon trên bảng tên bệ ải (ZoneNode): khoá, dấu qua, vương miện mini boss, boss
            "Assets/03 Art/Fallback/Icons/lock.png", "Assets/03 Art/Fallback/Icons/check.png",
            "Assets/03 Art/Fallback/Icons/crownSm.png", "Assets/03 Art/Fallback/Icons/boss.png",
        };

        [MenuItem("PokiClash/Tối ưu/Sprite Atlas đảo (dựng lại)", priority = 200)]
        static void Build()
        {
            if (EditorSettings.spritePackerMode != SpritePackerMode.SpriteAtlasV2)
            {
                EditorSettings.spritePackerMode = SpritePackerMode.SpriteAtlasV2;
                Debug.Log("[Atlas] Bật Sprite Atlas V2 cho project");
            }
            if (AssetDatabase.LoadMainAssetAtPath(AtlasPath)) AssetDatabase.DeleteAsset(AtlasPath);
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
            var atlas = new SpriteAtlasAsset();
            atlas.Add(objs.ToArray());
            SpriteAtlasAsset.Save(atlas, AtlasPath);
            AssetDatabase.ImportAsset(AtlasPath, ImportAssetOptions.ForceUpdate);
            var imp = AssetImporter.GetAtPath(AtlasPath) as SpriteAtlasImporter;
            if (!imp)
            {
                Debug.LogError("[Atlas] Không đọc được importer của " + AtlasPath);
                return;
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
            SpriteAtlasUtility.PackAllAtlases(EditorUserBuildSettings.activeBuildTarget);
            var packed = AssetDatabase.LoadAssetAtPath<SpriteAtlas>(AtlasPath);
            Debug.Log($"[Atlas] Đã dựng {AtlasPath}: {(packed ? packed.spriteCount : 0)} hình ({objs.Count} mục)");
        }
    }
}
