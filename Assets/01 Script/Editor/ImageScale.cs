// Thu nhỏ ảnh RGBA bằng lọc hộp (trung bình theo diện tích phủ), trộn ở không gian nhân sẵn alpha để mép trong suốt không
// ám màu tối. Tách hai lượt ngang rồi dọc. Thuần C# (không dùng UnityEngine); bước build AolaDevBuild gọi qua AolaPngPack.
using System;

namespace PokiClash.EditorTools
{
    public static class ImageScale
    {
        // rgba: 4 byte mỗi điểm, w × h; trả nw × nh (nw ≤ w, nh ≤ h), cùng chiều hàng với ảnh vào
        public static byte[] Down(byte[] rgba, int w, int h, int nw, int nh)
        {
            if (nw >= w && nh >= h) return rgba;
            // lượt ngang: w × h → nw × h, kênh nhân sẵn alpha (float)
            var mid = new float[nw * h * 4];
            double fx = (double)w / nw;
            for (int x = 0; x < nw; x++)
            {
                double s0 = x * fx, s1 = (x + 1) * fx;
                int i0 = (int)Math.Floor(s0), i1 = Math.Min(w, (int)Math.Ceiling(s1));
                for (int y = 0; y < h; y++)
                {
                    float r = 0, g = 0, b = 0, a = 0;
                    for (int i = i0; i < i1; i++)
                    {
                        float wt = (float)(Math.Min(s1, i + 1) - Math.Max(s0, i));
                        int o = (y * w + i) * 4;
                        float al = rgba[o + 3] * wt;
                        r += rgba[o] * al;
                        g += rgba[o + 1] * al;
                        b += rgba[o + 2] * al;
                        a += al;
                    }
                    int m = (y * nw + x) * 4;
                    mid[m] = r;
                    mid[m + 1] = g;
                    mid[m + 2] = b;
                    mid[m + 3] = a;
                }
            }
            // lượt dọc: nw × h → nw × nh, rồi bỏ nhân alpha
            var outp = new byte[nw * nh * 4];
            double fy = (double)h / nh;
            float area = (float)(fx * fy);
            for (int y = 0; y < nh; y++)
            {
                double s0 = y * fy, s1 = (y + 1) * fy;
                int j0 = (int)Math.Floor(s0), j1 = Math.Min(h, (int)Math.Ceiling(s1));
                for (int x = 0; x < nw; x++)
                {
                    float r = 0, g = 0, b = 0, a = 0;
                    for (int j = j0; j < j1; j++)
                    {
                        float wt = (float)(Math.Min(s1, j + 1) - Math.Max(s0, j));
                        int m = (j * nw + x) * 4;
                        r += mid[m] * wt;
                        g += mid[m + 1] * wt;
                        b += mid[m + 2] * wt;
                        a += mid[m + 3] * wt;
                    }
                    int o = (y * nw + x) * 4;
                    if (a > 0)
                    {
                        outp[o] = Byte(r / a);
                        outp[o + 1] = Byte(g / a);
                        outp[o + 2] = Byte(b / a);
                    }
                    outp[o + 3] = Byte(a / area);
                }
            }
            return outp;
        }

        // đổi cỡ bất kỳ: chiều nào cũng thu nhỏ thì như Down; có chiều phóng to thì nội suy song tuyến (nhân sẵn alpha),
        // chiều thu nhỏ còn lại lấy trung bình hộp (chân dung 384x480 kéo thành 512x512, AolaImport)
        public static byte[] Resize(byte[] rgba, int w, int h, int nw, int nh)
        {
            if (nw <= w && nh <= h) return nw == w && nh == h ? rgba : Down(rgba, w, h, nw, nh);
            var pre = new float[w * h * 4];
            for (int i = 0; i < w * h; i++)
            {
                float a = rgba[i * 4 + 3] / 255f;
                pre[i * 4] = rgba[i * 4] * a;
                pre[i * 4 + 1] = rgba[i * 4 + 1] * a;
                pre[i * 4 + 2] = rgba[i * 4 + 2] * a;
                pre[i * 4 + 3] = rgba[i * 4 + 3];
            }
            var mid = Axis(pre, w, h, nw, true);
            var res = Axis(mid, nw, h, nh, false);
            var outp = new byte[nw * nh * 4];
            for (int i = 0; i < nw * nh; i++)
            {
                float a = res[i * 4 + 3];
                if (a > 0.5f)
                {
                    outp[i * 4] = Byte(res[i * 4] * 255f / a);
                    outp[i * 4 + 1] = Byte(res[i * 4 + 1] * 255f / a);
                    outp[i * 4 + 2] = Byte(res[i * 4 + 2] * 255f / a);
                }
                outp[i * 4 + 3] = Byte(a);
            }
            return outp;
        }

        // một lượt theo một chiều (ngang: horiz) của ảnh float nhân sẵn alpha w × h: phóng to song tuyến, thu nhỏ trung bình hộp
        static float[] Axis(float[] src, int w, int h, int n, bool horiz)
        {
            int len = horiz ? w : h, other = horiz ? h : w;
            var dst = new float[(horiz ? n * h : w * n) * 4];
            double f = (double)len / n;
            for (int k = 0; k < n; k++)
            {
                for (int o = 0; o < other; o++)
                {
                    float r = 0, g = 0, b = 0, a = 0;
                    if (n >= len)
                    {
                        double c = (k + 0.5) * f - 0.5;
                        int i0 = (int)Math.Floor(c);
                        float t = (float)(c - i0);
                        int ia = Math.Max(0, Math.Min(len - 1, i0)), ib = Math.Max(0, Math.Min(len - 1, i0 + 1));
                        int pa = (horiz ? o * w + ia : ia * w + o) * 4, pb = (horiz ? o * w + ib : ib * w + o) * 4;
                        r = src[pa] + (src[pb] - src[pa]) * t;
                        g = src[pa + 1] + (src[pb + 1] - src[pa + 1]) * t;
                        b = src[pa + 2] + (src[pb + 2] - src[pa + 2]) * t;
                        a = src[pa + 3] + (src[pb + 3] - src[pa + 3]) * t;
                    }
                    else
                    {
                        double s0 = k * f, s1 = (k + 1) * f;
                        int i0 = (int)Math.Floor(s0), i1 = Math.Min(len, (int)Math.Ceiling(s1));
                        for (int i = i0; i < i1; i++)
                        {
                            float wt = (float)((Math.Min(s1, i + 1) - Math.Max(s0, i)) / f);
                            int p = (horiz ? o * w + i : i * w + o) * 4;
                            r += src[p] * wt;
                            g += src[p + 1] * wt;
                            b += src[p + 2] * wt;
                            a += src[p + 3] * wt;
                        }
                    }
                    int q = (horiz ? o * n + k : k * w + o) * 4;
                    dst[q] = r;
                    dst[q + 1] = g;
                    dst[q + 2] = b;
                    dst[q + 3] = a;
                }
            }
            return dst;
        }

        static byte Byte(float v) => (byte)Math.Max(0, Math.Min(255, (int)Math.Round(v)));
    }
}
