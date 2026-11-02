// Tìm ảnh theo tên ("world", "zone_thuy", "btn_red", icon "ball"...): ảnh gen trong Assets/03 Art trước,
// không có thì ảnh thay thế (Assets/03 Art/Fallback, xuất từ code vẽ của bản web), không có nữa thì null.
// Thiếu ảnh chỉ ghi cảnh báo một lần cho mỗi tên, không gây lỗi. Danh mục dựng bằng menu "PokiClash/Nhập ảnh".
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    [CreateAssetMenu(menuName = "PokiClash/ArtLibrary", fileName = "ArtLibrary")]
    public sealed class ArtLibrary : ScriptableObject
    {
        [Serializable]
        public struct Entry
        {
            public string name;
            public Sprite sprite;
        }

        public List<Entry> art = new List<Entry>(); // ảnh gen (đã xử lý từ ArtGen/*/inbox)
        public List<Entry> fallback = new List<Entry>(); // ảnh thay thế
        public List<Entry> icons = new List<Entry>(); // icon thay thế (Fallback/Icons)

        Dictionary<string, Sprite> artMap, fallbackMap, iconMap;
        readonly HashSet<string> warned = new HashSet<string>();

        public static ArtLibrary Current;

        void Index()
        {
            if (artMap != null) return;
            artMap = Map(art);
            fallbackMap = Map(fallback);
            iconMap = Map(icons);
        }

        static Dictionary<string, Sprite> Map(List<Entry> list)
        {
            var d = new Dictionary<string, Sprite>();
            foreach (var e in list)
                if (e.sprite != null && !string.IsNullOrEmpty(e.name))
                    d[e.name] = e.sprite;
            return d;
        }

        public bool HasArt(string name)
        {
            Index();
            return artMap.ContainsKey(name);
        }

        // Ảnh nền, đảo, khung...: ảnh gen nếu có, không thì ảnh thay thế.
        public Sprite Get(string name)
        {
            Index();
            if (artMap.TryGetValue(name, out var s)) return s;
            if (fallbackMap.TryGetValue(name, out s))
            {
                Warn(name, "dùng ảnh thay thế");
                return s;
            }
            Warn(name, "không có cả ảnh thay thế");
            return null;
        }

        // Icon: ảnh gen "icon_<tên>" nếu có (gói ArtGen/Icons), không thì icon SVG của bản web.
        public Sprite Icon(string name)
        {
            Index();
            if (string.IsNullOrEmpty(name)) return null;
            if (artMap.TryGetValue("icon_" + name, out var s)) return s;
            if (iconMap.TryGetValue(name, out s)) return s;
            Warn("icon_" + name, "không có icon");
            return iconMap.TryGetValue("star", out s) ? s : null;
        }

        void Warn(string name, string what)
        {
            if (warned.Add(name)) Debug.LogWarning($"[Ảnh] Chưa có ảnh '{name}': {what}.");
        }

        public void Invalidate() => artMap = null;
    }
}
