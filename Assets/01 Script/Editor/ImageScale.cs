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

        static byte Byte(float v) => (byte)Math.Max(0, Math.Min(255, (int)Math.Round(v)));
    }
}
