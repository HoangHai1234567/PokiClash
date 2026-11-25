// Lõi mã hoá dùng chung của PokiClash (bảo mật bản build: ảnh, chỉ số, save...). Thuần BCL (không đụng UnityEngine) để test
// được ngoài Unity bằng mcs/mono. Chống đọc (AES-256-CBC) và chống sửa (HMAC-SHA256, encrypt-then-MAC): sửa một byte là hỏng MAC,
// không giải ra. Khoá dẫn xuất theo "nhãn" bằng HKDF (texture, balance, save... khác khoá nhau); khoá chủ cất dạng hai mảng XOR,
// không có literal khoá nào để grep. Đây là mã đối xứng chạy trên máy người chơi: cao thủ dump bộ nhớ vẫn moi được — mục tiêu là
// nâng rào đủ cao để không đáng công, chứ không phải bất khả xâm phạm. Lớp 2 (mã hoá global-metadata) giấu tên hàm ở đây.
using System;
using System.Security.Cryptography;
using System.Text;

namespace PokiClash.Security
{
    public static class PokiCrypt
    {
        // Khoá chủ 32 byte cất dạng A xor B (không có mảng khoá thật trong mã). A xor B = khoá.
        static readonly byte[] A =
        {
            0x3F,0xA1,0x08,0xD2,0x5C,0x7E,0x90,0x14, 0xBB,0x46,0xE3,0x29,0x71,0xCA,0x0D,0x58,
            0x9A,0x33,0x6F,0xB4,0x02,0xEE,0x87,0x1D, 0x4C,0xF0,0x65,0xA8,0xDB,0x39,0x7A,0x11,
        };
        static readonly byte[] B =
        {
            0x8C,0x2D,0x51,0x6A,0xF7,0x19,0x44,0xCE, 0x03,0x9F,0x70,0xB2,0x5D,0xE6,0x28,0x81,
            0x47,0xDA,0x16,0x63,0xAB,0x35,0xC9,0x7C, 0xE0,0x12,0x8E,0x5B,0x30,0xF4,0x6D,0xA9,
        };

        static byte[] Master()
        {
            var k = new byte[32];
            for (int i = 0; i < 32; i++) k[i] = (byte)(A[i] ^ B[i] ^ 0x5A);
            return k;
        }

        // Salt cố định của HKDF (không phải bí mật; chỉ để tách miền khoá).
        static readonly byte[] Salt = Encoding.ASCII.GetBytes("PokiClash/v1/kdf");

        const byte Ver = 1;
        static readonly byte[] Magic = { (byte)'P', (byte)'K', (byte)'C', 0x31 }; // "PKC1"

        // Bộ nhớ đệm khoá theo nhãn (dẫn xuất một lần): nhãn -> (khoá AES 32, khoá MAC 32).
        static readonly System.Collections.Generic.Dictionary<string, (byte[] enc, byte[] mac)> Keys
            = new System.Collections.Generic.Dictionary<string, (byte[], byte[])>();

        // HKDF (RFC 5869) rút gọn: Extract bằng HMAC(salt, master), Expand ra 64 byte -> 32 enc + 32 mac.
        // info = label (+ context nếu có, như id máy cho save). Tự viết để khỏi dính Rfc2898 (khác hành vi giữa các runtime).
        static (byte[] enc, byte[] mac) DeriveKeys(string label, byte[] context)
        {
            string ck = context == null ? label : label + "\0" + Convert.ToBase64String(context);
            lock (Keys)
            {
                if (Keys.TryGetValue(ck, out var got)) return got;
                byte[] master = Master();
                byte[] prk;
                using (var h = new HMACSHA256(Salt)) prk = h.ComputeHash(master);
                Array.Clear(master, 0, master.Length);

                var info = new System.Collections.Generic.List<byte>();
                info.AddRange(Encoding.UTF8.GetBytes("PokiClash:" + label));
                if (context != null) { info.Add(0); info.AddRange(context); }

                byte[] okm = HkdfExpand(prk, info.ToArray(), 64);
                Array.Clear(prk, 0, prk.Length);
                var enc = new byte[32]; var mac = new byte[32];
                Buffer.BlockCopy(okm, 0, enc, 0, 32);
                Buffer.BlockCopy(okm, 32, mac, 0, 32);
                Array.Clear(okm, 0, okm.Length);
                var pair = (enc, mac);
                Keys[ck] = pair;
                return pair;
            }
        }

        static byte[] HkdfExpand(byte[] prk, byte[] info, int len)
        {
            var outp = new byte[len];
            byte[] t = Array.Empty<byte>();
            int pos = 0; byte ctr = 1;
            using (var h = new HMACSHA256(prk))
            {
                while (pos < len)
                {
                    h.Initialize();
                    var buf = new byte[t.Length + info.Length + 1];
                    Buffer.BlockCopy(t, 0, buf, 0, t.Length);
                    Buffer.BlockCopy(info, 0, buf, t.Length, info.Length);
                    buf[buf.Length - 1] = ctr++;
                    t = h.ComputeHash(buf);
                    int take = Math.Min(t.Length, len - pos);
                    Buffer.BlockCopy(t, 0, outp, pos, take);
                    pos += take;
                }
            }
            return outp;
        }

        // ===== API chính =====

        public static byte[] Encrypt(byte[] plain, string label, byte[] context = null)
        {
            if (plain == null) throw new ArgumentNullException(nameof(plain));
            var (encKey, macKey) = DeriveKeys(label, context);
            byte[] iv = new byte[16];
            using (var rng = RandomNumberGenerator.Create()) rng.GetBytes(iv);

            byte[] cipher;
            using (var aes = Aes.Create())
            {
                aes.KeySize = 256; aes.Mode = CipherMode.CBC; aes.Padding = PaddingMode.PKCS7;
                aes.Key = encKey; aes.IV = iv;
                using (var enc = aes.CreateEncryptor())
                    cipher = enc.TransformFinalBlock(plain, 0, plain.Length);
            }

            // blob = Magic(4) | Ver(1) | iv(16) | cipher | mac(32); mac trùm mọi thứ trước mac.
            int head = 4 + 1 + 16;
            var blob = new byte[head + cipher.Length + 32];
            Buffer.BlockCopy(Magic, 0, blob, 0, 4);
            blob[4] = Ver;
            Buffer.BlockCopy(iv, 0, blob, 5, 16);
            Buffer.BlockCopy(cipher, 0, blob, head, cipher.Length);
            byte[] mac;
            using (var h = new HMACSHA256(macKey)) mac = h.ComputeHash(blob, 0, head + cipher.Length);
            Buffer.BlockCopy(mac, 0, blob, head + cipher.Length, 32);
            return blob;
        }

        // Trả về null nếu blob hỏng/bị sửa/sai nhãn (không ném để chỗ gọi xử gọn).
        public static byte[] TryDecrypt(byte[] blob, string label, byte[] context = null)
        {
            try { return Decrypt(blob, label, context); }
            catch { return null; }
        }

        public static byte[] Decrypt(byte[] blob, string label, byte[] context = null)
        {
            if (blob == null || blob.Length < 4 + 1 + 16 + 32) throw new CryptographicException("blob ngắn");
            for (int i = 0; i < 4; i++) if (blob[i] != Magic[i]) throw new CryptographicException("sai magic");
            if (blob[4] != Ver) throw new CryptographicException("sai version");
            var (encKey, macKey) = DeriveKeys(label, context);

            int head = 4 + 1 + 16;
            int cipherLen = blob.Length - head - 32;
            byte[] want;
            using (var h = new HMACSHA256(macKey)) want = h.ComputeHash(blob, 0, head + cipherLen);
            if (!FixedEquals(want, 0, blob, head + cipherLen, 32)) throw new CryptographicException("MAC sai (bị sửa?)");

            var iv = new byte[16];
            Buffer.BlockCopy(blob, 5, iv, 0, 16);
            using (var aes = Aes.Create())
            {
                aes.KeySize = 256; aes.Mode = CipherMode.CBC; aes.Padding = PaddingMode.PKCS7;
                aes.Key = encKey; aes.IV = iv;
                using (var dec = aes.CreateDecryptor())
                    return dec.TransformFinalBlock(blob, head, cipherLen);
            }
        }

        public static byte[] EncryptString(string s, string label, byte[] context = null)
            => Encrypt(Encoding.UTF8.GetBytes(s ?? ""), label, context);

        public static string DecryptString(byte[] blob, string label, byte[] context = null)
        {
            var b = TryDecrypt(blob, label, context);
            return b == null ? null : Encoding.UTF8.GetString(b);
        }

        // So sánh hằng thời gian (chống dò MAC qua thời gian).
        static bool FixedEquals(byte[] a, int ao, byte[] b, int bo, int n)
        {
            int diff = 0;
            for (int i = 0; i < n; i++) diff |= a[ao + i] ^ b[bo + i];
            return diff == 0;
        }
    }
}
