// Nước chảy bản đồ sảnh (ArtGen/Islands/sanh_moi/nuoc_dong.py; người dùng 2026-11-23 "nước suối vẫn hơi tĩnh, học Kingdom Rush 5").
// - Cách nhập trường dòng chảy Baked/Islands/Resources/sanh_nuoc_<đảo>_hc.png: số, không sRGB, không nén, không mipmap, bilinear, kẹp
//   mép (ArtPostprocessor bỏ qua thư mục Baked).
// - Menu "PokiClash/Prefab/Sảnh và đảo/Sảnh: nước chảy (material, danh mục ảnh)": mỗi trường một material Islands/Resources/sanh_nuoc_<đảo>.mat (shader
//   PokiClash/UIFlowWater, _FlowTex), dựng lại danh mục ảnh (ảnh phủ sanh_nuoc_<đảo>, bọt anim_bot_*, vòng gợn, lấp lánh). IslandAnim
//   (khoá world_map, "flows") nạp material bằng Resources.Load khi vào sảnh: không phải sửa prefab.
// Chạy lại sau mỗi lần chạy nuoc_dong.py.
using System.IO;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public sealed class HubWaterImport : AssetPostprocessor
    {
        void OnPreprocessTexture()
        {
            if (!HubWaterMenu.IsFlowTex(assetPath)) return;
            var ti = (TextureImporter)assetImporter;
            ti.textureType = TextureImporterType.Default;
            ti.sRGBTexture = false;
            ti.mipmapEnabled = false;
            ti.alphaSource = TextureImporterAlphaSource.None;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.filterMode = FilterMode.Bilinear;
            ti.npotScale = TextureImporterNPOTScale.None;
            ti.textureCompression = TextureImporterCompression.Uncompressed;
            ti.maxTextureSize = 2048;
            foreach (var pf in new[] { "Android", "iPhone" })
            {
                var ps = ti.GetPlatformTextureSettings(pf);
                ps.overridden = true;
                ps.maxTextureSize = 2048;
                ps.format = TextureImporterFormat.RGB24;
                ti.SetPlatformTextureSettings(ps);
            }
        }
    }

    public static class HubWaterMenu
    {
        public const string FlowDir = "Assets/03 Art/Baked/Islands/Resources";
        const string MatDir = "Assets/03 Art/Islands/Resources";

        public static bool IsFlowTex(string path)
        {
            path = path.Replace('\\', '/');
            return path.StartsWith(FlowDir + "/sanh_nuoc_") && path.EndsWith("_hc.png");
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Sảnh: nước chảy (material, danh mục ảnh)", priority = 64)]
        public static void Build()
        {
            var shader = Shader.Find("PokiClash/UIFlowWater");
            if (!shader)
            {
                Debug.LogError("[Sảnh nước] Không thấy shader PokiClash/UIFlowWater (Assets/03 Art/Shaders/UIFlowWater.shader)");
                return;
            }
            if (!AssetDatabase.IsValidFolder(MatDir)) AssetDatabase.CreateFolder("Assets/03 Art/Islands", "Resources");
            int n = 0;
            foreach (var f in Directory.GetFiles(FlowDir, "sanh_nuoc_*_hc.png"))
            {
                var path = f.Replace('\\', '/');
                AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
                var tex = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
                string zone = Path.GetFileNameWithoutExtension(path).Replace("sanh_nuoc_", "").Replace("_hc", "");
                AssetDatabase.ImportAsset($"Assets/03 Art/Islands/sanh_nuoc_{zone}.png", ImportAssetOptions.ForceUpdate);
                string mp = $"{MatDir}/sanh_nuoc_{zone}.mat";
                var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
                if (!mat)
                {
                    mat = new Material(shader) { name = "sanh_nuoc_" + zone };
                    AssetDatabase.CreateAsset(mat, mp);
                }
                mat.shader = shader;
                mat.SetTexture("_FlowTex", tex);
                EditorUtility.SetDirty(mat);
                n++;
            }
            foreach (var a in new[] { "bot_1", "bot_2", "bot_3", "vong", "lap_1", "lap_2", "lap_3", // nước
                         "ca", "ca_vang", "cua", "ca_voi", "duoi_ca_voi", "voi_phun", "chai", "da_lua", "rua" }) // easter egg (IslandAnimTrung)
                AssetDatabase.ImportAsset($"Assets/03 Art/Islands/Anim/anim_{a}.png", ImportAssetOptions.ForceUpdate);
            AssetDatabase.ImportAsset("Assets/03 Art/Islands/island_anim.json", ImportAssetOptions.ForceUpdate);
            AssetDatabase.SaveAssets();
            ArtImporter.BuildLibrary();
            Debug.Log($"[Sảnh nước] {n} material nước chảy, đã dựng lại danh mục ảnh");
        }
    }
}
