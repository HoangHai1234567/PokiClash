// Kế hoạch tô sáp màu của màn mở khoá tướng (người dùng 2026-11-25: "phần tô màu nhìn hơi phèn và không thật, làm nhiều bút chì màu
// khác nhau tô các phần cùng lúc cho thật hơn"; HeroUnlockView, shader UIPencilDraw).
// Vào: ảnh hộp quanh tướng w x h RGBA, hàng 0 ở dưới, byte theo gamma (như AsyncGPUReadback của RenderTexture sRGB trả về).
//   1. Màu: lấy điểm ảnh đục, bỏ nét mực mảnh (tối hơn DarkL, dày dưới 5 điểm ảnh). Gom màu bằng k-means trên lưới 16 mức mỗi kênh:
//      khởi đầu bằng ô nhiều điểm nhất, rồi lần lượt ô xa nhất có trọng số. Ra tối đa 4 nhóm (4 kênh RGBA của ảnh phủ); nhóm dưới 3%
//      gộp vào nhóm gần nhất.
//   2. Bút: mỗi nhóm một bút. Nhóm lớn được thêm bút (tối đa 6 bút), các bút cùng nhóm chia nhau các hàng.
//   3. Đường bút: hàng ngang từ trên xuống, cách nhau Spacing. Mỗi hàng lấy các đoạn có điểm của nhóm (khe hẹp hơn một hàng thì nối).
//      Bút gạch zích zắc dọc theo đoạn, hàng sau đi ngược chiều, sang đoạn khác thì nhấc bút.
// Shader nhận màu nhóm (Colors). Mỗi bút tô vào kênh của nhóm mình trên ảnh phủ (Stamp); mỗi điểm ảnh lấy kênh của nhóm có màu gần
// nhất, nên màu không lem sang vùng khác. Nét mực và mảng tối (dưới DarkL) thì bút nào đi qua cũng tô.
// Toạ độ đường bút: điểm ảnh của ảnh vào, y lên.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    public sealed class CrayonPlan
    {
        public const float DarkL = 0.27f; // độ sáng (gamma) dưới mức này: nét mực, mảng tối; shader dùng cùng số (_DarkL)
        public const int MaxGroups = 4, MaxPens = 6;
        public const float AirWeight = 0.35f; // đoạn nhấc bút tính 35% quãng (bút bay nhanh hơn lúc gạch)

        public int W, H;
        public float Spacing; // khoảng hàng (điểm ảnh)
        public float Brush;   // bán kính vệt sáp (điểm ảnh)
        public readonly List<float[]> Colors = new List<float[]>(); // màu nhóm (r, g, b theo gamma 0–1), nhóm lớn trước
        public readonly List<Pen> Pens = new List<Pen>();

        public sealed class Pen
        {
            public int Group;
            public float[] X, Y;
            public bool[] Down;  // Down[i]: đoạn từ điểm i − 1 tới i là nét gạch (false: nhấc bút)
            public float[] Cum;  // quãng có trọng số tới điểm i
            public float Length => Cum.Length > 0 ? Cum[Cum.Length - 1] : 0;

            // chỗ bút ở quãng d; seg: số thứ tự đoạn (đổi lực tay theo nét)
            public void At(float d, out float x, out float y, out bool down, out int seg)
            {
                int n = Cum.Length;
                if (n == 0)
                {
                    x = y = 0;
                    down = false;
                    seg = 0;
                    return;
                }
                if (d <= 0 || n == 1)
                {
                    x = X[0];
                    y = Y[0];
                    down = false;
                    seg = 0;
                    return;
                }
                if (d >= Cum[n - 1])
                {
                    x = X[n - 1];
                    y = Y[n - 1];
                    down = Down[n - 1];
                    seg = n - 1;
                    return;
                }
                int lo = 1, hi = n - 1;
                while (lo < hi)
                {
                    int m = (lo + hi) >> 1;
                    if (Cum[m] < d) lo = m + 1;
                    else hi = m;
                }
                float a = Cum[lo - 1], b = Cum[lo];
                float t = b > a ? (d - a) / (b - a) : 1;
                x = X[lo - 1] + (X[lo] - X[lo - 1]) * t;
                y = Y[lo - 1] + (Y[lo] - Y[lo - 1]) * t;
                down = Down[lo];
                seg = lo;
            }

            // các điểm chấm sáp trên nét gạch trong quãng (d0, d1], cách đều step theo quãng (khung sau nối tiếp khung trước)
            public void Strokes(float d0, float d1, float step, Action<float, float, int> stamp)
            {
                if (step <= 0 || d1 <= d0) return;
                for (double d = Math.Floor(d0 / step + 1) * step; d <= d1; d += step)
                {
                    At((float)d, out float x, out float y, out bool down, out int seg);
                    if (down) stamp(x, y, seg);
                }
            }
        }

        static float Dec(float c) => c <= 0.04045f ? c / 12.92f : (float)Math.Pow((c + 0.055f) / 1.055f, 2.4f);
        static float Enc(float l) => l <= 0.0031308f ? l * 12.92f : 1.055f * (float)Math.Pow(l, 1 / 2.4f) - 0.055f;
        public static float Lum(float r, float g, float b) => 0.299f * r + 0.587f * g + 0.114f * b;

        static float D2(float[] c, float r, float g, float b)
        {
            float dr = c[0] - r, dg = c[1] - g, db = c[2] - b;
            return dr * dr + dg * dg + db * db;
        }

        // nhóm gần nhất theo khoảng cách RGB (gamma), như shader
        public int Nearest(float r, float g, float b)
        {
            int best = 0;
            float bd = float.MaxValue;
            for (int k = 0; k < Colors.Count; k++)
            {
                float d = D2(Colors[k], r, g, b);
                if (d < bd)
                {
                    bd = d;
                    best = k;
                }
            }
            return best;
        }

        // premul: màu đã nhân alpha (RenderTexture của rig); linear: dự án ở không gian tuyến tính (nhân alpha trước khi mã gamma).
        // null: ảnh rỗng hoặc không đủ điểm.
        public static CrayonPlan Make(byte[] rgba, int w, int h, bool premul, bool linear, int seed = 1)
        {
            if (rgba == null || w < 4 || h < 4 || rgba.Length < w * h * 4) return null;
            int n = w * h;
            var col = new float[n * 3];
            var opaque = new bool[n];
            var dark = new bool[n];
            for (int i = 0; i < n; i++)
            {
                int a = rgba[i * 4 + 3];
                if (a < 128) continue;
                opaque[i] = true;
                float af = a / 255f;
                for (int c = 0; c < 3; c++)
                {
                    float v = rgba[i * 4 + c] / 255f;
                    if (premul && a < 255) v = linear ? Enc(Math.Min(1, Dec(v) / af)) : Math.Min(1, v / af);
                    col[i * 3 + c] = v;
                }
                dark[i] = Lum(col[i * 3], col[i * 3 + 1], col[i * 3 + 2]) < DarkL;
            }
            // nét mảnh: điểm tối có điểm không tối (hoặc trong suốt, ngoài ảnh) trong ô 5 x 5 quanh nó
            var thin = new bool[n];
            for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
            {
                int i = y * w + x;
                if (!opaque[i] || !dark[i]) continue;
                bool t = false;
                for (int dy = -2; dy <= 2 && !t; dy++)
                for (int dx = -2; dx <= 2 && !t; dx++)
                {
                    int xx = x + dx, yy = y + dy;
                    if (xx < 0 || yy < 0 || xx >= w || yy >= h) t = true;
                    else
                    {
                        int j = yy * w + xx;
                        if (!opaque[j] || !dark[j]) t = true;
                    }
                }
                thin[i] = t;
            }

            // lưới 16 mức mỗi kênh
            var cnt = new int[4096];
            var sum = new double[4096 * 3];
            int total = 0;
            for (int i = 0; i < n; i++)
            {
                if (!opaque[i] || thin[i]) continue;
                float r = col[i * 3], g = col[i * 3 + 1], b = col[i * 3 + 2];
                int bin = (Math.Min(15, (int)(r * 16)) * 16 + Math.Min(15, (int)(g * 16))) * 16 + Math.Min(15, (int)(b * 16));
                cnt[bin]++;
                sum[bin * 3] += r;
                sum[bin * 3 + 1] += g;
                sum[bin * 3 + 2] += b;
                total++;
            }
            if (total < 20) return null;
            var bins = new List<int>();
            for (int k = 0; k < 4096; k++)
                if (cnt[k] > 0) bins.Add(k);
            var mean = new float[4096][];
            foreach (int k in bins) mean[k] = new[] { (float)(sum[k * 3] / cnt[k]), (float)(sum[k * 3 + 1] / cnt[k]), (float)(sum[k * 3 + 2] / cnt[k]) };

            var plan = new CrayonPlan { W = w, H = h };
            var centers = plan.Colors;
            int first = bins[0];
            foreach (int k in bins)
                if (cnt[k] > cnt[first]) first = k;
            centers.Add((float[])mean[first].Clone());
            while (centers.Count < MaxGroups)
            {
                int best = -1;
                float bs = 0, bd = 0;
                foreach (int k in bins)
                {
                    float md = float.MaxValue;
                    foreach (var c in centers) md = Math.Min(md, D2(c, mean[k][0], mean[k][1], mean[k][2]));
                    float s = cnt[k] * md;
                    if (s > bs)
                    {
                        bs = s;
                        best = k;
                        bd = md;
                    }
                }
                if (best < 0 || bd < 0.02f) break; // còn lại đều gần một nhóm đã có (khác nhau dưới ~0,14)
                centers.Add((float[])mean[best].Clone());
            }
            var weight = new int[MaxGroups];
            void Iterate(int times)
            {
                for (int it = 0; it < times; it++)
                {
                    var acc = new double[centers.Count * 3];
                    Array.Clear(weight, 0, weight.Length);
                    foreach (int k in bins)
                    {
                        int g = plan.Nearest(mean[k][0], mean[k][1], mean[k][2]);
                        weight[g] += cnt[k];
                        for (int c = 0; c < 3; c++) acc[g * 3 + c] += sum[k * 3 + c];
                    }
                    for (int g = 0; g < centers.Count; g++)
                        if (weight[g] > 0)
                            for (int c = 0; c < 3; c++) centers[g][c] = (float)(acc[g * 3 + c] / weight[g]);
                }
            }
            Iterate(10);
            // bỏ nhóm nhỏ (dưới 3%) và nhóm trùng màu (khác dưới ~0,1), chạy lại cho các nhóm còn lại
            for (bool changed = true; changed && centers.Count > 1;)
            {
                changed = false;
                int small = -1;
                for (int g = 0; g < centers.Count; g++)
                    if (weight[g] < total * 0.03f && (small < 0 || weight[g] < weight[small])) small = g;
                if (small < 0)
                    for (int a = 0; a < centers.Count && small < 0; a++)
                    for (int b = a + 1; b < centers.Count && small < 0; b++)
                        if (D2(centers[a], centers[b][0], centers[b][1], centers[b][2]) < 0.01f) small = weight[a] < weight[b] ? a : b;
                if (small >= 0)
                {
                    centers.RemoveAt(small);
                    Iterate(4);
                    changed = true;
                }
            }
            // nhóm lớn trước
            var order = new List<int>();
            for (int g = 0; g < centers.Count; g++) order.Add(g);
            order.Sort((a, b) => weight[b].CompareTo(weight[a]));
            var sorted = new List<float[]>();
            foreach (int g in order) sorted.Add(centers[g]);
            centers.Clear();
            centers.AddRange(sorted);

            // nhãn từng điểm: −1 trong suốt, −2 nét mảnh (không lên kế hoạch), còn lại nhóm gần nhất
            int G = centers.Count;
            var lab = new int[n];
            var area = new int[G];
            for (int i = 0; i < n; i++)
            {
                if (!opaque[i])
                {
                    lab[i] = -1;
                    continue;
                }
                if (thin[i])
                {
                    lab[i] = -2;
                    continue;
                }
                int g = plan.Nearest(col[i * 3], col[i * 3 + 1], col[i * 3 + 2]);
                lab[i] = g;
                area[g]++;
            }

            // số bút mỗi nhóm
            var pens = new int[G];
            int used = 0;
            for (int g = 0; g < G; g++)
                if (area[g] > 0)
                {
                    pens[g] = 1;
                    used++;
                }
            while (used < MaxPens)
            {
                int best = -1;
                for (int g = 0; g < G; g++)
                    if (pens[g] > 0 && (best < 0 || area[g] * pens[best] > area[best] * pens[g])) best = g;
                if (best < 0 || area[best] / (float)pens[best] < total * 0.2f) break;
                pens[best]++;
                used++;
            }

            float sp = plan.Spacing = Math.Max(5, Math.Min(24, (float)Math.Round(Math.Max(w, h) / 16f)));
            plan.Brush = 0.62f * sp;
            int nb = (int)Math.Ceiling(h / sp);
            var rnd = new Random(seed);
            var has = new bool[w];
            for (int g = 0; g < G; g++)
            {
                if (pens[g] == 0) continue;
                // các đoạn của từng hàng (trên xuống) và số điểm của nhóm trong hàng
                var bandRuns = new List<List<float[]>>();
                var bandY = new List<float>();
                var bandArea = new List<int>();
                for (int bi = 0; bi < nb; bi++)
                {
                    int y1 = h - 1 - (int)(bi * sp), y0 = Math.Max(0, h - (int)((bi + 1) * sp));
                    if (y1 < 0) break;
                    Array.Clear(has, 0, w);
                    int cntBand = 0;
                    for (int y = y0; y <= y1; y++)
                    for (int x = 0; x < w; x++)
                        if (lab[y * w + x] == g)
                        {
                            has[x] = true;
                            cntBand++;
                        }
                    if (cntBand == 0) continue;
                    var runs = new List<float[]>();
                    int xs = -1, last = -1000;
                    for (int x = 0; x <= w; x++)
                    {
                        bool on = x < w && has[x];
                        if (on)
                        {
                            if (xs < 0) xs = x;
                            else if (x - last > sp) // khe rộng hơn một hàng: cắt đoạn
                            {
                                runs.Add(new float[] { xs, last + 1 });
                                xs = x;
                            }
                            last = x;
                        }
                    }
                    if (xs >= 0) runs.Add(new float[] { xs, last + 1 });
                    foreach (var r in runs)
                    {
                        r[0] = Math.Max(0, r[0] - 0.3f * sp);
                        r[1] = Math.Min(w, r[1] + 0.3f * sp);
                    }
                    bandRuns.Add(runs);
                    bandY.Add((y0 + y1 + 1) * 0.5f);
                    bandArea.Add(cntBand);
                }
                // chia hàng cho các bút của nhóm, mỗi bút một khúc hàng liền nhau, số điểm gần bằng nhau
                int pc = Math.Min(pens[g], bandRuns.Count);
                int bstart = 0, acc = 0;
                for (int pi = 0; pi < pc; pi++)
                {
                    int bend = bstart;
                    float target = area[g] * (pi + 1f) / pc;
                    int room = bandRuns.Count - (pc - 1 - pi); // chừa mỗi bút sau ít nhất một hàng
                    while (bend < room && (pi == pc - 1 || acc + bandArea[bend] * 0.5f < target || bend == bstart))
                        acc += bandArea[bend++];
                    var pen = BuildPen(g, bandRuns, bandY, bstart, bend, sp, h, rnd);
                    if (pen.Cum.Length > 1) plan.Pens.Add(pen);
                    bstart = bend;
                }
            }
            return plan.Pens.Count > 0 ? plan : null;
        }

        static Pen BuildPen(int g, List<List<float[]>> bandRuns, List<float> bandY, int b0, int b1, float sp, int h, Random rnd)
        {
            var xs = new List<float>();
            var ys = new List<float>();
            var down = new List<bool>();
            float amp = 0.6f * sp, adv = 0.55f * sp;
            int dir = -1; // hàng đầu đi từ phải sang trái (bút bay vào từ góc trên phải)
            for (int b = b0; b < b1; b++, dir = -dir)
            {
                var runs = bandRuns[b];
                float yc = bandY[b];
                for (int ri = 0; ri < runs.Count; ri++)
                {
                    var r = runs[dir > 0 ? ri : runs.Count - 1 - ri];
                    float xa = dir > 0 ? r[0] : r[1], xb = dir > 0 ? r[1] : r[0];
                    int m = Math.Max(1, (int)Math.Ceiling(Math.Abs(xb - xa) / adv));
                    for (int j = 0; j <= m; j++)
                    {
                        float x = xa + (xb - xa) * j / m + (j > 0 && j < m ? (float)(rnd.NextDouble() - 0.5) * 0.2f * adv : 0);
                        float y = yc + (j % 2 == 0 ? amp : -amp) + (float)(rnd.NextDouble() - 0.5) * 0.24f * sp;
                        xs.Add(x);
                        ys.Add(Math.Max(0, Math.Min(h, y)));
                        down.Add(j > 0);
                    }
                }
            }
            var p = new Pen { Group = g, X = xs.ToArray(), Y = ys.ToArray(), Down = down.ToArray(), Cum = new float[xs.Count] };
            for (int i = 1; i < xs.Count; i++)
            {
                float dx = xs[i] - xs[i - 1], dy = ys[i] - ys[i - 1];
                float len = (float)Math.Sqrt(dx * dx + dy * dy);
                p.Cum[i] = p.Cum[i - 1] + (p.Down[i] ? len : len * AirWeight);
            }
            return p;
        }

        // chấm một vệt sáp tròn vào kênh ch của ảnh phủ RGBA32 cw x ch (hàng 0 ở dưới): lõi đặc, mép mềm; giữ giá trị lớn hơn
        public static void Stamp(byte[] cov, int cw, int chh, int channel, float cx, float cy, float r, float pressure)
        {
            if (r <= 0) return;
            int x0 = Math.Max(0, (int)Math.Floor(cx - r)), x1 = Math.Min(cw - 1, (int)Math.Ceiling(cx + r));
            int y0 = Math.Max(0, (int)Math.Floor(cy - r)), y1 = Math.Min(chh - 1, (int)Math.Ceiling(cy + r));
            for (int y = y0; y <= y1; y++)
            for (int x = x0; x <= x1; x++)
            {
                float dx = x + 0.5f - cx, dy = y + 0.5f - cy;
                float d = (float)Math.Sqrt(dx * dx + dy * dy) / r;
                if (d >= 1) continue;
                float v = pressure * Math.Min(1, (1 - d) * 2.2f);
                int idx = (y * cw + x) * 4 + channel;
                byte bv = (byte)Math.Min(255, (int)(v * 255 + 0.5f));
                if (bv > cov[idx]) cov[idx] = bv;
            }
        }
    }
}
