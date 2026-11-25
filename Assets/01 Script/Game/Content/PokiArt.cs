// Lớp 1 (cách B): nạp ảnh đã mã hoá. Ưu tiên blob mã hoá ở Resources/enc/<key>.bytes (giải mã -> dựng Texture2D/Sprite đúng format,
// giữ nén ASTC). KHÔNG có blob (Editor / bản thử chưa strip) thì LÙI VỀ Resources.Load như cũ: lắp façade này vào không đổi hành vi
// gì cho tới khi bước build sinh blob. Texture/Sprite dựng từ blob được cache mãi theo key (dùng chung, không Destroy -> không có
// tham chiếu treo); bộ nhớ tăng theo số dạng đã nạp — chấp nhận được, tinh chỉnh (prewarm/evict) sau khi kiểm trong Unity.
using System.Collections.Generic;
using PokiClash.Security;
using UnityEngine;

namespace PokiClash.Game
{
    public static class PokiArt
    {
        public const string EncDir = "enc/"; // Resources/enc/<key>.bytes

        static readonly Dictionary<string, Texture2D> texCache = new Dictionary<string, Texture2D>();
        static readonly Dictionary<string, Sprite> sprCache = new Dictionary<string, Sprite>();
        static readonly Dictionary<string, ResourceRequest> warming = new Dictionary<string, ResourceRequest>();

        // Có blob mã hoá cho key này không (bản ship đã strip ảnh gốc thì chỉ còn blob).
        public static bool HasEncrypted(string key) => Resources.Load<TextAsset>(EncDir + key) != null;

        public static Texture2D LoadTexture(string key)
        {
            if (string.IsNullOrEmpty(key)) return null;
            if (texCache.TryGetValue(key, out var cached) && cached) return cached;
            var blob = TakeWarmed(key) ?? Resources.Load<TextAsset>(EncDir + key);
            if (blob != null)
            {
                var tex = BuildTexture(blob.bytes, key);
                if (tex) { texCache[key] = tex; return tex; }
            }
            return Resources.Load<Texture2D>(key); // lùi về bản cũ (Editor/chưa strip)
        }

        public static Sprite LoadSprite(string key)
        {
            if (string.IsNullOrEmpty(key)) return null;
            if (sprCache.TryGetValue(key, out var cached) && cached) return cached;
            var blob = Resources.Load<TextAsset>(EncDir + key);
            if (blob != null)
            {
                var spr = BuildSprite(blob.bytes, key);
                if (spr) { sprCache[key] = spr; return spr; }
            }
            return Resources.Load<Sprite>(key);
        }

        // Nạp trước blob không chặn (atlas tướng sắp dùng): LoadTexture sau đó lấy ngay.
        public static void Prewarm(string key)
        {
            if (string.IsNullOrEmpty(key) || texCache.ContainsKey(key) || warming.ContainsKey(key)) return;
            warming[key] = Resources.LoadAsync<TextAsset>(EncDir + key);
        }

        static TextAsset TakeWarmed(string key)
        {
            if (!warming.TryGetValue(key, out var req)) return null;
            warming.Remove(key);
            return req?.asset as TextAsset; // đọc .asset buộc hoàn tất nếu chưa xong
        }

        // Dựng Texture2D từ blob mã hoá nằm sẵn trong asset (atlas .atomik, AtomikAsset.Atlas). null nếu blob hỏng.
        public static Texture2D TextureFromEncrypted(byte[] enc, string key) => enc == null ? null : BuildTexture(enc, key);

        // Dựng Texture2D từ gói đã mã hoá; dùng chung cho atlas và nền sprite.
        static Texture2D BuildTexture(byte[] enc, string key)
        {
            var plain = PokiCrypt.TryDecrypt(enc, "texture");
            var b = plain == null ? null : TexBlob.Unpack(plain);
            if (b == null) { Debug.LogError("[Bảo mật] Giải mã/đọc ảnh lỗi: " + key); return null; }
            return FromBlob(b, key);
        }

        public static Texture2D FromBlob(TexBlob b, string key)
        {
            var tex = new Texture2D(b.width, b.height, (TextureFormat)b.format, b.mipCount > 1, b.linear == 1)
            {
                filterMode = (FilterMode)b.filterMode,
                wrapMode = (TextureWrapMode)b.wrapMode,
                name = key,
            };
            tex.LoadRawTextureData(b.raw);
            tex.Apply(false, true); // false: không tự dựng mip; true: bỏ bản CPU (nhẹ bộ nhớ)
            return tex;
        }

        static Sprite BuildSprite(byte[] enc, string key)
        {
            var plain = PokiCrypt.TryDecrypt(enc, "texture");
            var b = plain == null ? null : TexBlob.Unpack(plain);
            if (b == null) { Debug.LogError("[Bảo mật] Giải mã/đọc sprite lỗi: " + key); return null; }
            var tex = FromBlob(b, key);
            var rect = new Rect(b.rectX, b.rectY, b.rectW, b.rectH);
            var pivot = new Vector2(b.pivotX, b.pivotY);
            var border = new Vector4(b.borderL, b.borderB, b.borderR, b.borderT);
            return Sprite.Create(tex, rect, pivot, b.ppu, 0, SpriteMeshType.FullRect, border);
        }
    }
}
