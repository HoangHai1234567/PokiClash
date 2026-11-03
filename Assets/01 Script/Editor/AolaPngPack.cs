// Nén hình tướng aola cho bản build (AolaDevBuild): thu nhỏ về cỡ đích (ImageScale) rồi ghi PNG 256 màu (PalettePng). Bản nén
// lưu sẵn trong Library/PokiAolaPng (khoá theo đường dẫn, cỡ, giờ sửa của file gốc, cỡ đích và phiên bản bộ nén), nên chỉ lần
// build đầu (hoặc khi hình đổi) mới tốn thời gian. Mỗi bản nén được Unity tự giải mã lại để chắc máy đọc được; không đọc được
// thì ghi PNG thường (vẫn đúng cỡ đích). Không thu nhỏ mà bản 256 màu không nhỏ hơn thì giữ file gốc.
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class AolaPngPack
    {
        const int Version = 2; // đổi khi bộ nén đổi cách ghi, để bỏ cache cũ

        static string CacheDir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Library/PokiAolaPng"));

        // byte PNG đưa vào bản build cho file gốc (đường dẫn đầy đủ), thu nhỏ về nw × nh (≤ 0: giữ cỡ); hit: lấy từ cache
        public static byte[] Get(string file, int nw, int nh, out bool hit)
        {
            var fi = new FileInfo(file);
            var key = Hash($"{Version}|{PalettePng.DefaultMse}|{fi.FullName.ToLowerInvariant()}|{fi.Length}|{fi.LastWriteTimeUtc.Ticks}|{nw}x{nh}");
            var cached = Path.Combine(CacheDir, key + ".png");
            hit = File.Exists(cached);
            if (hit) return File.ReadAllBytes(cached);
            var bytes = Compress(File.ReadAllBytes(file), nw, nh);
            Directory.CreateDirectory(CacheDir);
            File.WriteAllBytes(cached, bytes);
            return bytes;
        }

        // cỡ ảnh đọc từ đầu file PNG (IHDR); không phải PNG thì false
        public static bool Size(byte[] png, out int w, out int h)
        {
            w = h = 0;
            if (png == null || png.Length < 24 || png[0] != 0x89 || png[1] != 0x50) return false;
            w = (png[16] << 24) | (png[17] << 16) | (png[18] << 8) | png[19];
            h = (png[20] << 24) | (png[21] << 16) | (png[22] << 8) | png[23];
            return true;
        }

        public static bool Size(string file, out int w, out int h)
        {
            var head = new byte[24];
            using (var f = File.OpenRead(file))
                if (f.Read(head, 0, 24) < 24)
                {
                    w = h = 0;
                    return false;
                }
            return Size(head, out w, out h);
        }

        static byte[] Compress(byte[] src, int nw, int nh)
        {
            var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
            var check = new Texture2D(2, 2, TextureFormat.RGBA32, false);
            try
            {
                if (!tex.LoadImage(src)) return src;
                int w = tex.width, h = tex.height;
                var px = tex.GetPixels32(); // hàng dưới trước
                var rgba = new byte[px.Length * 4];
                for (int i = 0; i < px.Length; i++)
                {
                    var c = px[i];
                    rgba[i * 4] = c.r;
                    rgba[i * 4 + 1] = c.g;
                    rgba[i * 4 + 2] = c.b;
                    rgba[i * 4 + 3] = c.a;
                }
                bool scaled = nw > 0 && nh > 0 && (nw < w || nh < h);
                if (scaled)
                {
                    nw = Math.Min(nw, w);
                    nh = Math.Min(nh, h);
                    rgba = ImageScale.Down(rgba, w, h, nw, nh);
                    w = nw;
                    h = nh;
                }
                var png = PalettePng.Encode(rgba, w, h, true);
                if (!scaled && png.Length >= src.Length) return src;
                if (check.LoadImage(png) && check.width == w && check.height == h) return png;
                if (!scaled) return src;
                // Unity không đọc được bản 256 màu: ghi PNG thường cùng cỡ đích (ma trận anim.json đã tính theo cỡ này)
                var plain = new Texture2D(w, h, TextureFormat.RGBA32, false);
                try
                {
                    var cols = new Color32[w * h];
                    for (int i = 0; i < cols.Length; i++) cols[i] = new Color32(rgba[i * 4], rgba[i * 4 + 1], rgba[i * 4 + 2], rgba[i * 4 + 3]);
                    plain.SetPixels32(cols);
                    return plain.EncodeToPNG();
                }
                finally
                {
                    Object.DestroyImmediate(plain);
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning("[Tướng aola] Không nén được một hình, giữ bản gốc: " + e.Message);
                return src;
            }
            finally
            {
                Object.DestroyImmediate(tex);
                Object.DestroyImmediate(check);
            }
        }

        static string Hash(string s)
        {
            using (var sha = SHA1.Create())
            {
                var b = sha.ComputeHash(Encoding.UTF8.GetBytes(s));
                var sb = new StringBuilder(b.Length * 2);
                foreach (var x in b) sb.Append(x.ToString("x2"));
                return sb.ToString();
            }
        }
    }
}
