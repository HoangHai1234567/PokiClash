// Đóng/mở gói một texture (atlas) hay sprite (chân dung, mặt tướng) để mã hoá (Lớp 1, cách B). Thuần BCL (không đụng UnityEngine)
// để test ngoài Unity: chỉ gói số liệu + bytes thô. PokiArt (phía Game) bóc raw của Texture2D rồi gọi Pack; lúc chạy giải mã rồi
// Unpack để dựng lại Texture2D đúng format (giữ nén ASTC nếu raw là ASTC). Format-agnostic: lưu đúng format editor bóc được, dựng
// lại y hệt — đúng hình dù raw là ASTC hay RGBA (chỉ khác dung lượng).
using System.IO;

namespace PokiClash.Security
{
    public sealed class TexBlob
    {
        public const int KindTexture = 0;
        public const int KindSprite = 1;

        public int kind;
        public int format;      // (int)UnityEngine.TextureFormat
        public int width, height, mipCount;
        public byte filterMode;  // (byte)UnityEngine.FilterMode
        public byte wrapMode;    // (byte)UnityEngine.TextureWrapMode
        public byte linear;      // 1 = không gian tuyến tính, 0 = sRGB

        // chỉ dùng khi kind == KindSprite:
        public float pivotX, pivotY;             // pivot CHUẨN HOÁ (0..1) theo rect
        public float rectX, rectY, rectW, rectH; // vùng sprite trong texture (pixel)
        public float ppu;
        public float borderL, borderB, borderR, borderT; // viền 9-slice (pixel)

        public byte[] raw; // dữ liệu texture thô (theo format)

        static readonly byte[] Magic = { (byte)'P', (byte)'X', (byte)'T', (byte)'1' };

        public byte[] Pack()
        {
            using (var ms = new MemoryStream())
            using (var w = new BinaryWriter(ms))
            {
                w.Write(Magic);
                w.Write((byte)kind);
                w.Write(format);
                w.Write(width);
                w.Write(height);
                w.Write(mipCount);
                w.Write(filterMode);
                w.Write(wrapMode);
                w.Write(linear);
                if (kind == KindSprite)
                {
                    w.Write(pivotX); w.Write(pivotY);
                    w.Write(rectX); w.Write(rectY); w.Write(rectW); w.Write(rectH);
                    w.Write(ppu);
                    w.Write(borderL); w.Write(borderB); w.Write(borderR); w.Write(borderT);
                }
                w.Write(raw != null ? raw.Length : 0);
                if (raw != null) w.Write(raw);
                w.Flush();
                return ms.ToArray();
            }
        }

        // Trả null nếu không đúng định dạng.
        public static TexBlob Unpack(byte[] data)
        {
            if (data == null || data.Length < 4) return null;
            using (var ms = new MemoryStream(data, false))
            using (var r = new BinaryReader(ms))
            {
                for (int i = 0; i < 4; i++) if (r.ReadByte() != Magic[i]) return null;
                var b = new TexBlob
                {
                    kind = r.ReadByte(),
                    format = r.ReadInt32(),
                    width = r.ReadInt32(),
                    height = r.ReadInt32(),
                    mipCount = r.ReadInt32(),
                    filterMode = r.ReadByte(),
                    wrapMode = r.ReadByte(),
                    linear = r.ReadByte(),
                };
                if (b.kind == KindSprite)
                {
                    b.pivotX = r.ReadSingle(); b.pivotY = r.ReadSingle();
                    b.rectX = r.ReadSingle(); b.rectY = r.ReadSingle(); b.rectW = r.ReadSingle(); b.rectH = r.ReadSingle();
                    b.ppu = r.ReadSingle();
                    b.borderL = r.ReadSingle(); b.borderB = r.ReadSingle(); b.borderR = r.ReadSingle(); b.borderT = r.ReadSingle();
                }
                int n = r.ReadInt32();
                b.raw = r.ReadBytes(n);
                return b;
            }
        }
    }
}
