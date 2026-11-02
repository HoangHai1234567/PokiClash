// Tài nguyên nướng sẵn từ code vẽ cũ (menu "PokiClash/Prefab/1. Nướng ảnh và âm thanh"): sprite giấy và mực của bộ UI,
// nhiễu nét rung, material chữ viền, tiếng tổng hợp. Lúc chạy chỉ tra bảng, không vẽ hay tổng hợp gì. (Hình tướng giữ chỗ
// vẽ tay đã bỏ 2026-11-02.)
using System;
using System.Collections.Generic;
using PokiClash.Core;
using TMPro;
using UnityEngine;

namespace PokiClash.UI
{
    [CreateAssetMenu(menuName = "PokiClash/BakedArt", fileName = "BakedArt")]
    public sealed class BakedArt : ScriptableObject
    {
        [Serializable]
        public struct SpriteItem
        {
            public string name;
            public Sprite sprite;
        }

        [Serializable]
        public struct OutlineItem
        {
            public TMP_FontAsset font;
            public int key; // độ dày viền × 100
            public Material material;
        }

        [Serializable]
        public struct ClipItem
        {
            public string name;
            public AudioClip clip;
        }

        public List<SpriteItem> sketch = new List<SpriteItem>();
        public Texture2D noise;
        public List<OutlineItem> outlines = new List<OutlineItem>();
        public List<ClipItem> sfx = new List<ClipItem>();

        public static BakedArt Current;

        Dictionary<string, Sprite> sketchMap;
        readonly HashSet<string> warned = new HashSet<string>();

        public Sprite Sketch(string name)
        {
            if (sketchMap == null)
            {
                sketchMap = new Dictionary<string, Sprite>();
                foreach (var s in sketch)
                    if (s.sprite) sketchMap[s.name] = s.sprite;
            }
            if (sketchMap.TryGetValue(name, out var sp)) return sp;
            Warn("sprite " + name);
            return null;
        }

        // chữ viền: đúng độ dày nếu có, không thì độ dày gần nhất của cùng phông
        public Material Outline(TMP_FontAsset font, int key)
        {
            Material best = null;
            int bestDiff = int.MaxValue;
            foreach (var o in outlines)
            {
                if (o.font != font || !o.material) continue;
                int diff = Mathf.Abs(o.key - key);
                if (diff < bestDiff)
                {
                    best = o.material;
                    bestDiff = diff;
                }
            }
            if (bestDiff != 0) Warn($"viền {font?.name} {key}");
            return best;
        }

        void Warn(string what)
        {
            if (warned.Add(what)) Debug.LogWarning($"[Nướng] Thiếu {what}: chạy menu PokiClash/Prefab/1. Nướng ảnh và âm thanh.");
        }
    }
}
