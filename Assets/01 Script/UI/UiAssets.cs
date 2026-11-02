// Tài nguyên dùng chung của bộ UI: phông TMP, material nét rung, ảnh thay thế (đặt qua menu "PokiClash/Dựng scene").
using TMPro;
using UnityEngine;

namespace PokiClash.UI
{
    [CreateAssetMenu(menuName = "PokiClash/UiAssets", fileName = "UiAssets")]
    public sealed class UiAssets : ScriptableObject
    {
        [Header("Phông (Baloo 2 cho tiêu đề và số, Pangolin cho chữ thường)")]
        public TMP_FontAsset title; // Baloo 2 ExtraBold (800)
        public TMP_FontAsset bold; // Baloo 2 Bold (700)
        public TMP_FontAsset body; // Pangolin

        [Header("Material shader PokiClash/UIInkBoil")]
        public Material kit; // _Encoded = 1, cho sprite vẽ bằng code
        public Material plain; // _Encoded = 0, cho ảnh thường (icon, ảnh gen)
        public Material sticker; // shader PokiClash/StickerOutline: viền sticker cho tướng aola (bản dev)
        public Material petPart; // shader PokiClash/PetPart của hình bộ phận tướng aola; có material thì shader vào bản build

        [Header("Nướng sẵn (menu PokiClash/Prefab/1. Nướng ảnh và âm thanh)")]
        public BakedArt baked;

        [Header("Bộ kit prefab (menu PokiClash/Prefab/2. Nướng bộ kit)")]
        public UiKit prefabs;
    }
}
