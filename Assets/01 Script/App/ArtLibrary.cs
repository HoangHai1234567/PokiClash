// Tìm ảnh theo tên ("world", "zone_thuy", "btn_red", icon "ball"...): ảnh gen trong Assets/03 Art trước,
// không có thì ảnh thay thế (Assets/03 Art/Fallback, xuất từ code vẽ của bản web), không có nữa thì null.
// Thiếu ảnh chỉ ghi cảnh báo một lần cho mỗi tên, không gây lỗi. Danh mục dựng bằng menu "PokiClash/Nhập ảnh".
using System;
using System.Collections.Generic;
using UnityEngine;
using PokiClash.Core;

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
            // hệ của gói tải sau chứa ảnh (GD_Claude/27): sprite để trống, nạp qua ContentPacks theo tên; rỗng = ảnh bản cài
            public string pack;
        }

        public List<Entry> art = new List<Entry>(); // ảnh gen (đã xử lý từ ArtGen/*/inbox)
        public List<Entry> fallback = new List<Entry>(); // ảnh thay thế
        public List<Entry> icons = new List<Entry>(); // icon thay thế (Fallback/Icons)

        Dictionary<string, Sprite> artMap, fallbackMap, iconMap;
        Dictionary<string, string> packMap; // tên ảnh trong gói tải sau → hệ
        readonly HashSet<string> warned = new HashSet<string>();

        public static ArtLibrary Current;

        void Index()
        {
            if (artMap != null) return;
            artMap = Map(art);
            fallbackMap = Map(fallback);
            iconMap = Map(icons);
            packMap = new Dictionary<string, string>();
            foreach (var e in art)
                if (!string.IsNullOrEmpty(e.pack) && !string.IsNullOrEmpty(e.name)) packMap[e.name] = e.pack;
            MipBias();
        }

        // Trang atlas có mipmap (Shop/anh_mip: hình cửa hàng, icon; 2026-11-27): lệch mip -0,5 như ảnh nguồn (ArtImporter) cho icon thu nhỏ
        // còn nét. Atlas không có ô cài đặt độ lệch, nên đặt lúc chạy; một trang chung cho mọi Image dùng hình trên trang đó.
        void MipBias()
        {
            if (!Application.isPlaying) return;
            var done = new HashSet<Texture>();
            foreach (var e in art)
            {
                var s = e.sprite;
                if (s == null || !s.packed) continue;
                var t = s.texture;
                if (t != null && t.mipmapCount > 1 && done.Add(t)) t.mipMapBias = -0.5f;
            }
        }

        // hệ của gói tải sau chứa ảnh, null nếu ảnh nằm trong bản cài (hoặc không có)
        public string PackOf(string name)
        {
            Index();
            return name != null && packMap.TryGetValue(name, out var e) ? e : null;
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
            return artMap.ContainsKey(name) || packMap.ContainsKey(name);
        }

        // Ảnh nền, đảo, khung...: ảnh gen nếu có, không thì ảnh thay thế.
        public Sprite Get(string name)
        {
            Index();
            if (artMap.TryGetValue(name, out var s)) return s;
            // ảnh trong gói tải sau: lấy từ gói đã nạp; chưa nạp thì xin nạp và tạm dùng ảnh thay thế (nơi gọi nên ContentPacks.Request
            // trước khi dựng màn, như ZoneScene, StageView)
            if (packMap.TryGetValue(name, out var elem))
            {
                s = PokiClash.Game.ContentPacks.Get<Sprite>(name);
                if (s) return s;
                PokiClash.Game.ContentPacks.Request(elem);
                return fallbackMap.TryGetValue(name, out s) ? s : null;
            }
            if (fallbackMap.TryGetValue(name, out s))
            {
                Warn(name, Loc.T("dùng ảnh thay thế"));
                return s;
            }
            Warn(name, Loc.T("không có cả ảnh thay thế"));
            return null;
        }

        // Icon: ảnh gen "icon_<tên>" nếu có (gói ArtGen/Icons), không thì icon SVG của bản web.
        public Sprite Icon(string name)
        {
            Index();
            if (string.IsNullOrEmpty(name)) return null;
            if (artMap.TryGetValue("icon_" + name, out var s)) return s;
            if (iconMap.TryGetValue(name, out s)) return s;
            Warn("icon_" + name, Loc.T("không có icon"));
            return iconMap.TryGetValue("star", out s) ? s : null;
        }

        // Tranh thẻ chung (ArtGen/Cards, GD_Claude/36): ảnh gen "tranh_<mã thẻ>" (03 Art/Cards) nếu có, không thì null để thẻ giữ ô tròn
        // + icon (thẻ riêng tướng, boss, quái chưa có tranh). Không cảnh báo: thiếu tranh là chuyện thường.
        public Sprite CardArt(string cardId)
        {
            Index();
            if (string.IsNullOrEmpty(cardId)) return null;
            return artMap.TryGetValue("tranh_" + cardId, out var s) ? s : null;
        }

        void Warn(string name, string what)
        {
            if (warned.Add(name)) Debug.LogWarning($"[Ảnh] Chưa có ảnh '{name}': {what}.");
        }

        public void Invalidate() => artMap = null;
    }
}
