// PNG bảng màu (tối đa 256 màu, giữ alpha) cho ảnh vector tô phẳng (hình tướng aola): điểm trong suốt hẳn gom về một màu;
// ảnh ≤ 256 màu giữ nguyên từng màu; nhiều hơn thì chia hộp theo sai số (median cut, không gian nhân sẵn alpha) rồi tinh chỉnh
// vài vòng k-means. Không hoà màu (dither) để mảng màu phẳng nén tốt. Thuần C# (không dùng UnityEngine) để thử được ngoài
// Unity; bước build AolaDevBuild gọi qua AolaPngPack.
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;

namespace PokiClash.EditorTools
{
    public static class PalettePng
    {
        const int MaxColors = 256;
        const int Refine = 3; // số vòng k-means sau median cut
        const float AlphaWeight = 2f; // sai khác alpha nặng hơn màu (mép mờ)

        // rgba: 4 byte mỗi điểm. bottomUp: hàng dưới trước (như Texture2D.GetPixels32), PNG ghi hàng trên trước.
        // maxMse: dừng chia hộp khi sai số bình phương trung bình mỗi điểm (không gian nhân sẵn alpha) đã dưới mức này;
        // ảnh vector tô phẳng thường chỉ cần vài chục màu, ít màu thì nén tốt hơn.
        public const float DefaultMse = 32f;

        public static byte[] Encode(byte[] rgba, int w, int h, bool bottomUp, float maxMse = DefaultMse)
        {
            int n = w * h;
            var keys = new uint[n];
            var counts = new Dictionary<uint, int>();
            uint run = 0;
            int runLen = 0;
            for (int i = 0; i < n; i++)
            {
                int o = i * 4;
                byte a = rgba[o + 3];
                uint k = a == 0 ? 0u : ((uint)rgba[o] << 24) | ((uint)rgba[o + 1] << 16) | ((uint)rgba[o + 2] << 8) | a;
                keys[i] = k;
                if (k == run && runLen > 0) runLen++;
                else
                {
                    if (runLen > 0) Add(counts, run, runLen);
                    run = k;
                    runLen = 1;
                }
            }
            if (runLen > 0) Add(counts, run, runLen);

            var palette = counts.Count <= MaxColors ? new List<uint>(counts.Keys) : Quantize(counts, maxMse);
            // mục có alpha < 255 lên đầu để tRNS ngắn
            palette.Sort((x, y) => ((x & 0xff) == 255 ? 1 : 0).CompareTo((y & 0xff) == 255 ? 1 : 0));
            var map = Map(counts, palette);

            // ít màu thì ghi 1/2/4 bit mỗi điểm (dồn từ bit cao)
            int bits = palette.Count <= 2 ? 1 : palette.Count <= 4 ? 2 : palette.Count <= 16 ? 4 : 8;
            int stride = (w * bits + 7) / 8 + 1;
            var raw = new byte[h * stride];
            for (int y = 0; y < h; y++)
            {
                int src = (bottomUp ? h - 1 - y : y) * w, dst = y * stride + 1; // byte đầu hàng: bộ lọc 0
                uint lastKey = 1;
                byte lastIdx = 0;
                for (int x = 0; x < w; x++)
                {
                    uint k = keys[src + x];
                    if (k != lastKey)
                    {
                        lastKey = k;
                        lastIdx = map[k];
                    }
                    if (bits == 8) raw[dst + x] = lastIdx;
                    else
                    {
                        int bit = x * bits;
                        raw[dst + (bit >> 3)] |= (byte)(lastIdx << (8 - bits - (bit & 7)));
                    }
                }
            }
            return WritePng(w, h, bits, palette, raw);
        }

        static void Add(Dictionary<uint, int> d, uint k, int c)
        {
            d.TryGetValue(k, out int v);
            d[k] = v + c;
        }

        // ---------- chọn bảng màu ----------

        static List<uint> Quantize(Dictionary<uint, int> counts, float maxMse)
        {
            bool clear = counts.ContainsKey(0);
            int m = counts.Count - (clear ? 1 : 0);
            // màu ở không gian nhân sẵn alpha (r·a, g·a, b·a, a·trọng số), kèm số điểm
            var c = new float[m, 4];
            var wt = new float[m];
            int i = 0;
            foreach (var kv in counts)
            {
                if (kv.Key == 0) continue;
                Pre(kv.Key, c, i);
                wt[i] = kv.Value;
                i++;
            }
            int target = MaxColors - (clear ? 1 : 0);
            var centers = MedianCut(c, wt, m, target, maxMse);
            for (int it = 0; it < Refine; it++) centers = KMeans(c, wt, m, centers);

            var pal = new List<uint>(centers.Count + 1);
            if (clear) pal.Add(0);
            var seen = new HashSet<uint>(pal);
            foreach (var p in centers)
            {
                uint k = Straight(p);
                if (seen.Add(k)) pal.Add(k);
            }
            return pal;
        }

        static void Pre(uint k, float[,] c, int i)
        {
            float a = k & 0xff;
            c[i, 0] = (k >> 24) * a / 255f;
            c[i, 1] = ((k >> 16) & 0xff) * a / 255f;
            c[i, 2] = ((k >> 8) & 0xff) * a / 255f;
            c[i, 3] = a * AlphaWeight;
        }

        static uint Straight(float[] p)
        {
            float a = Math.Max(1f, Math.Min(255f, p[3] / AlphaWeight));
            byte A = (byte)Math.Round(a);
            byte R = Clamp(p[0] * 255f / a), G = Clamp(p[1] * 255f / a), B = Clamp(p[2] * 255f / a);
            return ((uint)R << 24) | ((uint)G << 16) | ((uint)B << 8) | A;
        }

        static byte Clamp(float v) => (byte)Math.Round(Math.Max(0f, Math.Min(255f, v)));

        sealed class Box
        {
            public int start, end; // [start, end) trong mảng chỉ số
            public double score; // tổng sai số bình phương (có trọng số)
            public int axis;
        }

        static List<float[]> MedianCut(float[,] c, float[] wt, int m, int target, float maxMse)
        {
            var idx = new int[m];
            for (int i = 0; i < m; i++) idx[i] = i;
            var boxes = new List<Box> { Stats(c, wt, idx, 0, m) };
            double totalW = 0;
            for (int i = 0; i < m; i++) totalW += wt[i];
            while (boxes.Count < target)
            {
                double sse = 0;
                foreach (var b in boxes) sse += b.score;
                if (sse / totalW <= maxMse) break;
                Box best = null;
                foreach (var b in boxes)
                    if (b.end - b.start > 1 && (best == null || b.score > best.score)) best = b;
                if (best == null || best.score <= 0) break;
                int ax = best.axis;
                Array.Sort(idx, best.start, best.end - best.start, Comparer<int>.Create((x, y) => c[x, ax].CompareTo(c[y, ax])));
                double total = 0;
                for (int i = best.start; i < best.end; i++) total += wt[idx[i]];
                double acc = 0;
                int cut = best.start + 1;
                for (int i = best.start; i < best.end - 1; i++)
                {
                    acc += wt[idx[i]];
                    cut = i + 1;
                    if (acc >= total / 2) break;
                }
                boxes.Remove(best);
                boxes.Add(Stats(c, wt, idx, best.start, cut));
                boxes.Add(Stats(c, wt, idx, cut, best.end));
            }
            var centers = new List<float[]>(boxes.Count);
            foreach (var b in boxes)
            {
                var p = new float[4];
                double sw = 0;
                for (int i = b.start; i < b.end; i++)
                {
                    int j = idx[i];
                    sw += wt[j];
                    for (int ch = 0; ch < 4; ch++) p[ch] += (float)(c[j, ch] * wt[j]);
                }
                for (int ch = 0; ch < 4; ch++) p[ch] = (float)(p[ch] / sw);
                centers.Add(p);
            }
            return centers;
        }

        static Box Stats(float[,] c, float[] wt, int[] idx, int start, int end)
        {
            double sw = 0;
            var s = new double[4];
            var s2 = new double[4];
            for (int i = start; i < end; i++)
            {
                int j = idx[i];
                double w = wt[j];
                sw += w;
                for (int ch = 0; ch < 4; ch++)
                {
                    double v = c[j, ch];
                    s[ch] += v * w;
                    s2[ch] += v * v * w;
                }
            }
            var box = new Box { start = start, end = end };
            double bestVar = -1;
            for (int ch = 0; ch < 4; ch++)
            {
                double sse = s2[ch] - s[ch] * s[ch] / Math.Max(1e-9, sw);
                box.score += sse;
                if (sse > bestVar)
                {
                    bestVar = sse;
                    box.axis = ch;
                }
            }
            return box;
        }

        static List<float[]> KMeans(float[,] c, float[] wt, int m, List<float[]> centers)
        {
            int k = centers.Count;
            var sum = new double[k, 4];
            var sw = new double[k];
            for (int i = 0; i < m; i++)
            {
                int b = Nearest(c[i, 0], c[i, 1], c[i, 2], c[i, 3], centers);
                sw[b] += wt[i];
                for (int ch = 0; ch < 4; ch++) sum[b, ch] += c[i, ch] * wt[i];
            }
            var next = new List<float[]>(k);
            for (int b = 0; b < k; b++)
            {
                if (sw[b] <= 0) continue; // tâm không còn màu nào: bỏ
                var p = new float[4];
                for (int ch = 0; ch < 4; ch++) p[ch] = (float)(sum[b, ch] / sw[b]);
                next.Add(p);
            }
            return next;
        }

        static int Nearest(float r, float g, float b, float a, List<float[]> centers)
        {
            int best = 0;
            float bd = float.MaxValue;
            for (int i = 0; i < centers.Count; i++)
            {
                var p = centers[i];
                float dr = r - p[0], dg = g - p[1], db = b - p[2], da = a - p[3];
                float d = dr * dr + dg * dg + db * db + da * da;
                if (d < bd)
                {
                    bd = d;
                    best = i;
                }
            }
            return best;
        }

        // màu gốc → chỉ số bảng màu gần nhất (màu trong suốt hẳn → mục trong suốt)
        static Dictionary<uint, byte> Map(Dictionary<uint, int> counts, List<uint> palette)
        {
            var map = new Dictionary<uint, byte>(counts.Count);
            var pc = new List<float[]>(palette.Count);
            var tmp = new float[1, 4];
            foreach (var p in palette)
            {
                Pre(p, tmp, 0);
                pc.Add(new[] { tmp[0, 0], tmp[0, 1], tmp[0, 2], tmp[0, 3] });
            }
            int exactClear = palette.IndexOf(0);
            foreach (var k in counts.Keys)
            {
                int at = palette.IndexOf(k);
                if (at < 0 && k == 0) at = exactClear;
                if (at < 0)
                {
                    Pre(k, tmp, 0);
                    at = Nearest(tmp[0, 0], tmp[0, 1], tmp[0, 2], tmp[0, 3], pc);
                }
                map[k] = (byte)at;
            }
            return map;
        }

        // ---------- ghi PNG ----------

        static byte[] WritePng(int w, int h, int bits, List<uint> palette, byte[] raw)
        {
            using (var ms = new MemoryStream())
            {
                ms.Write(new byte[] { 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A }, 0, 8);
                var ihdr = new byte[13];
                BigEndian(ihdr, 0, (uint)w);
                BigEndian(ihdr, 4, (uint)h);
                ihdr[8] = (byte)bits; // số bit mỗi chỉ số
                ihdr[9] = 3; // bảng màu
                Chunk(ms, "IHDR", ihdr);
                var plte = new byte[palette.Count * 3];
                int trns = 0;
                for (int i = 0; i < palette.Count; i++)
                {
                    uint k = palette[i];
                    plte[i * 3] = (byte)(k >> 24);
                    plte[i * 3 + 1] = (byte)(k >> 16);
                    plte[i * 3 + 2] = (byte)(k >> 8);
                    if ((k & 0xff) != 255) trns = i + 1;
                }
                Chunk(ms, "PLTE", plte);
                if (trns > 0)
                {
                    var t = new byte[trns];
                    for (int i = 0; i < trns; i++) t[i] = (byte)(palette[i] & 0xff);
                    Chunk(ms, "tRNS", t);
                }
                Chunk(ms, "IDAT", Zlib(raw));
                Chunk(ms, "IEND", Array.Empty<byte>());
                return ms.ToArray();
            }
        }

        static byte[] Zlib(byte[] data)
        {
            using (var ms = new MemoryStream())
            {
                ms.WriteByte(0x78);
                ms.WriteByte(0xDA);
                using (var d = new DeflateStream(ms, CompressionLevel.Optimal, true)) d.Write(data, 0, data.Length);
                uint a = 1, b = 0;
                foreach (var v in data)
                {
                    a = (a + v) % 65521;
                    b = (b + a) % 65521;
                }
                var ad = new byte[4];
                BigEndian(ad, 0, (b << 16) | a);
                ms.Write(ad, 0, 4);
                return ms.ToArray();
            }
        }

        static void Chunk(Stream s, string type, byte[] data)
        {
            var len = new byte[4];
            BigEndian(len, 0, (uint)data.Length);
            s.Write(len, 0, 4);
            var t = new byte[] { (byte)type[0], (byte)type[1], (byte)type[2], (byte)type[3] };
            s.Write(t, 0, 4);
            s.Write(data, 0, data.Length);
            uint crc = Crc(Crc(0xffffffffu, t), data) ^ 0xffffffffu;
            var cb = new byte[4];
            BigEndian(cb, 0, crc);
            s.Write(cb, 0, 4);
        }

        static uint[] crcTable;

        static uint Crc(uint crc, byte[] data)
        {
            if (crcTable == null)
            {
                crcTable = new uint[256];
                for (uint n = 0; n < 256; n++)
                {
                    uint c = n;
                    for (int k = 0; k < 8; k++) c = (c & 1) != 0 ? 0xedb88320u ^ (c >> 1) : c >> 1;
                    crcTable[n] = c;
                }
            }
            foreach (var v in data) crc = crcTable[(crc ^ v) & 0xff] ^ (crc >> 8);
            return crc;
        }

        static void BigEndian(byte[] b, int at, uint v)
        {
            b[at] = (byte)(v >> 24);
            b[at + 1] = (byte)(v >> 16);
            b[at + 2] = (byte)(v >> 8);
            b[at + 3] = (byte)v;
        }
    }
}
