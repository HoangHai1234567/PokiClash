// Ghi gọn hình lưới (atts) và animation (anims) của AtomikAsset thành một khối byte nén (dung lượng build, 2026-11-23). Trước đó
// Unity lưu thẳng mảng float 32 bit: 106 dạng tướng mang ~42 MB vào gói dữ liệu, nén LZ4HC còn ~18 MB. Khối gọn còn ~9 MB.
// Cách ghi: số lượng tử hoá rồi lấy hiệu với số trước cùng làn (zigzag + varint), cả khối nén Deflate. Bước lượng tử rất nhỏ so
// với một điểm ảnh trên màn: giờ 1/100000 s, góc 1/10000 độ, toạ độ 1/1024 px rig, tỉ lệ 1/2^20, độ đậm 1/65536, UV và trọng số 1/2^20.
// Góc và tỉ lệ cần mịn vì cánh tay đòn có thể rất dài: clip appear của nham_than_1 dời xương 19000 px, phóng x18 rồi xương con kéo
// mảnh về gần gốc; góc 1/1000 độ ở đó lệch 0,07 px. Bước lượng tử ghi ngay trong khối (khối tự mô tả, đổi bước không giải sai khối cũ).
// Số không hữu hạn hay quá lớn thì ghi nguyên float (không mất gì). Khoá cũ (keys sải 7/12), điểm điều khiển, giờ sự kiện: ghi nguyên.
// AtomikAsset giải khối này lúc nạp (OnAfterDeserialize), nên mọi nơi dùng atts / anims như cũ.
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Text;

namespace PokiClash.Game
{
    public static class AtomikPack
    {
        public const byte Version = 2;
        // bước lượng tử khi GHI (khi đọc dùng bước ghi trong khối)
        public const double QTime = 100000, QRot = 10000, QPos = 1024, QScale = 1 << 20, QAlpha = 65536, QUv = 1 << 20, QWeight = 1 << 20;

        sealed class Steps
        {
            public double time = QTime, rot = QRot, pos = QPos, scale = QScale, alpha = QAlpha, uv = QUv, weight = QWeight;
        }

        const byte MEmpty = 0, MQuant = 1, MRaw = 2, MWeights = 3;

        // ---------- ghi ----------

        sealed class W
        {
            byte[] buf = new byte[1 << 16];
            public int n;

            void Need(int k)
            {
                if (n + k <= buf.Length) return;
                Array.Resize(ref buf, Math.Max(buf.Length * 2, n + k));
            }

            public void B(byte b) { Need(1); buf[n++] = b; }

            public void U(ulong v)
            {
                Need(10);
                while (v >= 0x80) { buf[n++] = (byte)(v | 0x80); v >>= 7; }
                buf[n++] = (byte)v;
            }

            public void S(long v) => U((ulong)((v << 1) ^ (v >> 63)));

            public void F(float f)
            {
                Need(4);
                var b = BitConverter.GetBytes(f);
                if (!BitConverter.IsLittleEndian) Array.Reverse(b);
                Buffer.BlockCopy(b, 0, buf, n, 4);
                n += 4;
            }

            public void D(double d)
            {
                Need(8);
                var b = BitConverter.GetBytes(d);
                if (!BitConverter.IsLittleEndian) Array.Reverse(b);
                Buffer.BlockCopy(b, 0, buf, n, 8);
                n += 8;
            }

            public void Str(string s)
            {
                var b = Encoding.UTF8.GetBytes(s ?? "");
                U((ulong)b.Length);
                Need(b.Length);
                Buffer.BlockCopy(b, 0, buf, n, b.Length);
                n += b.Length;
            }

            public byte[] Bytes()
            {
                var r = new byte[n];
                Buffer.BlockCopy(buf, 0, r, 0, n);
                return r;
            }
        }

        static bool Quantizable(float[] a, double q, int stride)
        {
            if (q <= 0 || stride <= 0 || a.Length % stride != 0) return false;
            foreach (var x in a)
                if (float.IsNaN(x) || float.IsInfinity(x) || Math.Abs(x * q) > 1e15) return false;
            return true;
        }

        static void Raw(W w, float[] a)
        {
            if (a == null || a.Length == 0) { w.B(MEmpty); return; }
            w.B(MRaw);
            w.U((ulong)a.Length);
            foreach (var x in a) w.F(x);
        }

        // q <= 0: ghi nguyên
        static void Q(W w, float[] a, double q, int stride)
        {
            if (a == null || a.Length == 0) { w.B(MEmpty); return; }
            if (!Quantizable(a, q, stride)) { Raw(w, a); return; }
            w.B(MQuant);
            w.U((ulong)a.Length);
            for (int s = 0; s < stride; s++)
            {
                long prev = 0;
                for (int i = s; i < a.Length; i += stride)
                {
                    long v = (long)Math.Round(a[i] * q);
                    w.S(v - prev);
                    prev = v;
                }
            }
        }

        static void I(W w, int[] a)
        {
            if (a == null || a.Length == 0) { w.B(MEmpty); return; }
            w.B(MQuant);
            w.U((ulong)a.Length);
            long prev = 0;
            foreach (var x in a) { w.S(x - prev); prev = x; }
        }

        // wInfo: mỗi đỉnh n, rồi n lần (xương, x, y, trọng số). Tách thành từng làn cho dễ nén; dạng lạ thì ghi nguyên.
        static void Weights(W w, float[] a)
        {
            if (a == null || a.Length == 0) { w.B(MEmpty); return; }
            var cnt = new List<int>();
            var bone = new List<int>();
            var xs = new List<float>();
            var ys = new List<float>();
            var ws = new List<float>();
            bool ok = Quantizable(a, QWeight, 1);
            for (int k = 0; ok && k < a.Length;)
            {
                float c = a[k++];
                if (c < 0 || c != Math.Floor(c) || k + 4 * (int)c > a.Length) { ok = false; break; }
                cnt.Add((int)c);
                for (int j = 0; j < (int)c; j++, k += 4)
                {
                    float b = a[k];
                    if (b < 0 || b != Math.Floor(b)) { ok = false; break; }
                    bone.Add((int)b);
                    xs.Add(a[k + 1]);
                    ys.Add(a[k + 2]);
                    ws.Add(a[k + 3]);
                }
            }
            if (!ok) { Raw(w, a); return; }
            w.B(MWeights);
            I(w, cnt.ToArray());
            I(w, bone.ToArray());
            Q(w, xs.ToArray(), QPos, 1);
            Q(w, ys.ToArray(), QPos, 1);
            Q(w, ws.ToArray(), QWeight, 1);
        }

        static void TimelineQ(int type, Steps s, out double q, out int dim)
        {
            switch (type)
            {
                case 0: q = s.rot; dim = 1; return;
                case 1: q = s.pos; dim = 2; return;
                case 2: q = s.scale; dim = 2; return;
                default: q = 0; dim = 1; return; // kiểu lạ: ghi nguyên
            }
        }

        static void Curve(W w, AtomikCurve c, double q, int dim)
        {
            Q(w, c?.t, QTime, 1);
            Q(w, c?.v, q, dim);
            I(w, c?.ck);
            Raw(w, c?.cp);
        }

        public static byte[] Write(AtomikAtt[] atts, AtomikClip[] anims)
        {
            var w = new W();
            var st = new Steps();
            foreach (var q in new[] { st.time, st.rot, st.pos, st.scale, st.alpha, st.uv, st.weight }) w.D(q);
            w.U((ulong)(atts?.Length ?? 0));
            if (atts != null)
                foreach (var a in atts)
                {
                    w.S(a.slot);
                    w.Str(a.name);
                    Q(w, a.uvs, QUv, 2);
                    I(w, a.tris);
                    Weights(w, a.wInfo);
                }
            w.U((ulong)(anims?.Length ?? 0));
            if (anims != null)
                foreach (var c in anims)
                {
                    w.Str(c.name);
                    w.F(c.dur);
                    w.U((ulong)(c.tls?.Length ?? 0));
                    if (c.tls != null)
                        foreach (var tl in c.tls)
                        {
                            w.S(tl.bone);
                            w.S(tl.type);
                            Raw(w, tl.keys);
                            TimelineQ(tl.type, st, out double q, out int dim);
                            Curve(w, tl.c, q, dim);
                        }
                    w.U((ulong)(c.sk?.Length ?? 0));
                    if (c.sk != null)
                        foreach (var k in c.sk)
                        {
                            w.S(k.slot);
                            Q(w, k.times, QTime, 1);
                            I(w, k.atts);
                        }
                    w.U((ulong)(c.sa?.Length ?? 0));
                    if (c.sa != null)
                        foreach (var k in c.sa)
                        {
                            w.S(k.slot);
                            Raw(w, k.keys);
                            Curve(w, k.c, QAlpha, 1);
                        }
                    w.U((ulong)(c.ev?.Length ?? 0));
                    if (c.ev != null)
                        foreach (var e in c.ev)
                        {
                            w.F(e.t);
                            w.Str(e.name);
                            w.Str(e.s);
                        }
                }
            var body = w.Bytes();
            using var ms = new MemoryStream();
            ms.WriteByte(Version);
            using (var ds = new DeflateStream(ms, CompressionLevel.Optimal, true)) ds.Write(body, 0, body.Length);
            return ms.ToArray();
        }

        // ---------- đọc ----------

        sealed class R
        {
            readonly byte[] b;
            int p;

            public R(byte[] b) { this.b = b; }

            public byte B() => b[p++];

            public ulong U()
            {
                ulong v = 0;
                int sh = 0;
                while (true)
                {
                    byte x = b[p++];
                    v |= (ulong)(x & 0x7F) << sh;
                    if (x < 0x80) return v;
                    sh += 7;
                    if (sh > 63) throw new InvalidDataException("varint quá dài");
                }
            }

            public int N() => checked((int)U());

            public long S()
            {
                ulong u = U();
                return (long)(u >> 1) ^ -(long)(u & 1);
            }

            public float F()
            {
                float f;
                if (BitConverter.IsLittleEndian) f = BitConverter.ToSingle(b, p);
                else
                {
                    var t = new byte[4];
                    Buffer.BlockCopy(b, p, t, 0, 4);
                    Array.Reverse(t);
                    f = BitConverter.ToSingle(t, 0);
                }
                p += 4;
                return f;
            }

            public double D()
            {
                double d;
                if (BitConverter.IsLittleEndian) d = BitConverter.ToDouble(b, p);
                else
                {
                    var t = new byte[8];
                    Buffer.BlockCopy(b, p, t, 0, 8);
                    Array.Reverse(t);
                    d = BitConverter.ToDouble(t, 0);
                }
                p += 8;
                if (!(d > 0) || double.IsInfinity(d)) throw new InvalidDataException("bước lượng tử hỏng " + d);
                return d;
            }

            public string Str()
            {
                int n = N();
                var s = Encoding.UTF8.GetString(b, p, n);
                p += n;
                return s;
            }

            public bool End => p == b.Length;
        }

        static float[] RawOrQ(R r, byte m, double q, int stride)
        {
            if (m == MEmpty) return new float[0];
            int n = r.N();
            var a = new float[n];
            if (m == MRaw)
            {
                for (int i = 0; i < n; i++) a[i] = r.F();
                return a;
            }
            if (m != MQuant) throw new InvalidDataException("kiểu mảng lạ " + m);
            for (int s = 0; s < stride; s++)
            {
                long v = 0;
                for (int i = s; i < n; i += stride)
                {
                    v += r.S();
                    a[i] = (float)(v / q);
                }
            }
            return a;
        }

        static float[] Q(R r, double q, int stride) => RawOrQ(r, r.B(), q, stride);

        static int[] I(R r)
        {
            byte m = r.B();
            if (m == MEmpty) return new int[0];
            if (m != MQuant) throw new InvalidDataException("kiểu mảng nguyên lạ " + m);
            int n = r.N();
            var a = new int[n];
            long v = 0;
            for (int i = 0; i < n; i++) { v += r.S(); a[i] = checked((int)v); }
            return a;
        }

        static float[] Weights(R r, Steps st)
        {
            byte m = r.B();
            if (m != MWeights) return RawOrQ(r, m, st.weight, 1);
            var cnt = I(r);
            var bone = I(r);
            var xs = Q(r, st.pos, 1);
            var ys = Q(r, st.pos, 1);
            var ws = Q(r, st.weight, 1);
            var a = new float[cnt.Length + 4 * bone.Length];
            int k = 0, g = 0;
            foreach (int c in cnt)
            {
                a[k++] = c;
                for (int j = 0; j < c; j++, g++)
                {
                    a[k++] = bone[g];
                    a[k++] = xs[g];
                    a[k++] = ys[g];
                    a[k++] = ws[g];
                }
            }
            return a;
        }

        static AtomikCurve Curve(R r, Steps st, double q, int dim) => new AtomikCurve
        {
            t = Q(r, st.time, 1),
            v = Q(r, q, dim),
            ck = I(r),
            cp = Q(r, 0, 1),
        };

        public static void Read(byte[] packed, out AtomikAtt[] atts, out AtomikClip[] anims)
        {
            if (packed == null || packed.Length < 2) throw new InvalidDataException("khối rỗng");
            if (packed[0] != Version) throw new InvalidDataException("phiên bản khối " + packed[0]);
            byte[] body;
            using (var src = new MemoryStream(packed, 1, packed.Length - 1))
            using (var ds = new DeflateStream(src, CompressionMode.Decompress))
            using (var dst = new MemoryStream(packed.Length * 4))
            {
                ds.CopyTo(dst);
                body = dst.ToArray();
            }
            var r = new R(body);
            var st = new Steps { time = r.D(), rot = r.D(), pos = r.D(), scale = r.D(), alpha = r.D(), uv = r.D(), weight = r.D() };
            atts = new AtomikAtt[r.N()];
            for (int i = 0; i < atts.Length; i++)
                atts[i] = new AtomikAtt
                {
                    slot = (int)r.S(),
                    name = r.Str(),
                    uvs = Q(r, st.uv, 2),
                    tris = I(r),
                    wInfo = Weights(r, st),
                };
            anims = new AtomikClip[r.N()];
            for (int ci = 0; ci < anims.Length; ci++)
            {
                var c = new AtomikClip { name = r.Str(), dur = r.F() };
                c.tls = new AtomikTimeline[r.N()];
                for (int i = 0; i < c.tls.Length; i++)
                {
                    var tl = new AtomikTimeline { bone = (int)r.S(), type = (int)r.S() };
                    tl.keys = Q(r, 0, 1);
                    TimelineQ(tl.type, st, out double q, out int dim);
                    tl.c = Curve(r, st, q, dim);
                    c.tls[i] = tl;
                }
                c.sk = new AtomikSlotKeys[r.N()];
                for (int i = 0; i < c.sk.Length; i++)
                    c.sk[i] = new AtomikSlotKeys { slot = (int)r.S(), times = Q(r, st.time, 1), atts = I(r) };
                c.sa = new AtomikAlphaKeys[r.N()];
                for (int i = 0; i < c.sa.Length; i++)
                {
                    var k = new AtomikAlphaKeys { slot = (int)r.S() };
                    k.keys = Q(r, 0, 1);
                    k.c = Curve(r, st, st.alpha, 1);
                    c.sa[i] = k;
                }
                c.ev = new AtomikEvent[r.N()];
                for (int i = 0; i < c.ev.Length; i++)
                    c.ev[i] = new AtomikEvent { t = r.F(), name = r.Str(), s = r.Str() };
                anims[ci] = c;
            }
            if (!r.End) throw new InvalidDataException("khối còn thừa byte");
        }
    }
}
