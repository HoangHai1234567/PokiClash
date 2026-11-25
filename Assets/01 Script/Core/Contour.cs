// Viền ngoài của hình từ mặt nạ độ phủ (màn mở khoá tướng, người dùng 2026-11-24: "bút chì vẽ lên trang giấy hình tướng", chọn
// cách "đi theo viền thật"): bút chì lần theo các vòng viền này trước rồi mới gạch bên trong và tô màu (HeroUnlockView).
// Mặt nạ: alpha w x h, hàng 0 ở dưới (như texture Unity). Các bước: ngưỡng → đóng khe 1 điểm ảnh (nở rồi co 3x3) → tách mảng liền
// → bỏ mảng vụn (nhỏ hơn 2% mảng lớn nhất) → lần viền ngoài từng mảng (Moore, đỉnh trên cùng bên trái) → bớt điểm (Ramer–Douglas–
// Peucker) → bo một lượt (Chaikin) → quay ngược chiều kim đồng hồ (từ đỉnh đi sang trái trước, như vẽ đầu rồi xuống thân).
// Lỗ bên trong (khe giữa tay và thân) không lần: gạch chì bên trong và tô màu lo phần đó.
// Toạ độ trả về: điểm ảnh của mặt nạ, y lên, mỗi vòng là mảng xen kẽ [x0, y0, x1, y1, ...], vòng kín (điểm cuối ≠ điểm đầu).
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    public static class Contour
    {
        // 8 hướng theo chiều kim đồng hồ trên màn (y lên): Tây, Tây Bắc, Bắc, Đông Bắc, Đông, Đông Nam, Nam, Tây Nam
        static readonly int[] DX = { -1, -1, 0, 1, 1, 1, 0, -1 };
        static readonly int[] DY = { 0, 1, 1, 1, 0, -1, -1, -1 };

        // hộp chứa các điểm có alpha >= thr: [xmin, ymin, xmax, ymax] (bao gồm); không có điểm nào thì null
        public static int[] Bounds(byte[] alpha, int w, int h, byte thr = 24)
        {
            int x0 = w, y0 = h, x1 = -1, y1 = -1;
            for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
            {
                if (alpha[y * w + x] < thr) continue;
                if (x < x0) x0 = x;
                if (x > x1) x1 = x;
                if (y < y0) y0 = y;
                if (y > y1) y1 = y;
            }
            return x1 < 0 ? null : new[] { x0, y0, x1, y1 };
        }

        // các vòng viền ngoài, mảng lớn trước, tối đa maxLoops vòng
        public static List<float[]> Loops(byte[] alpha, int w, int h, byte thr = 110, int maxLoops = 5, float eps = 0.9f)
        {
            var res = new List<float[]>();
            if (alpha == null || alpha.Length < w * h || w < 3 || h < 3) return res;
            var m = new bool[w * h];
            for (int i = 0; i < m.Length; i++) m[i] = alpha[i] >= thr;
            m = Erode(Dilate(m, w, h), w, h);

            // tách mảng liền (8 hướng), nhớ diện tích và điểm đầu (hàng trên cùng, trái nhất)
            var lab = new int[w * h];
            var area = new List<int> { 0 };
            var start = new List<int> { -1 };
            var stack = new Stack<int>();
            for (int y = h - 1; y >= 0; y--)
            for (int x = 0; x < w; x++)
            {
                int i = y * w + x;
                if (!m[i] || lab[i] != 0) continue;
                int id = area.Count, n = 0;
                area.Add(0);
                start.Add(i);
                lab[i] = id;
                stack.Push(i);
                while (stack.Count > 0)
                {
                    int c = stack.Pop();
                    n++;
                    int cx = c % w, cy = c / w;
                    for (int d = 0; d < 8; d++)
                    {
                        int nx = cx + DX[d], ny = cy + DY[d];
                        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
                        int j = ny * w + nx;
                        if (!m[j] || lab[j] != 0) continue;
                        lab[j] = id;
                        stack.Push(j);
                    }
                }
                area[id] = n;
            }
            if (area.Count <= 1) return res;
            int big = 0;
            for (int k = 1; k < area.Count; k++) big = Math.Max(big, area[k]);
            var ids = new List<int>();
            for (int k = 1; k < area.Count; k++)
                if (area[k] >= Math.Max(12, big * 0.02f)) ids.Add(k);
            ids.Sort((a, b) => area[b].CompareTo(area[a]));
            if (ids.Count > maxLoops) ids.RemoveRange(maxLoops, ids.Count - maxLoops);

            foreach (int id in ids)
            {
                var pts = Trace(lab, w, h, id, start[id]);
                if (pts.Count < 8) continue;
                var simp = Rdp(pts, eps);
                if (simp.Count < 3) continue;
                var sm = Chaikin(simp);
                // vòng lần theo chiều kim đồng hồ: đảo lại (giữ điểm đầu ở đỉnh)
                if (Area(sm) < 0)
                {
                    var first = sm[0];
                    sm.RemoveAt(0);
                    sm.Reverse();
                    sm.Insert(0, first);
                }
                var arr = new float[sm.Count * 2];
                for (int k = 0; k < sm.Count; k++)
                {
                    arr[2 * k] = sm[k].x;
                    arr[2 * k + 1] = sm[k].y;
                }
                res.Add(arr);
            }
            return res;
        }

        struct P
        {
            public float x, y;
            public P(float x, float y)
            {
                this.x = x;
                this.y = y;
            }
        }

        static bool[] Dilate(bool[] m, int w, int h)
        {
            var o = new bool[m.Length];
            for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
            {
                bool on = false;
                for (int dy = -1; dy <= 1 && !on; dy++)
                for (int dx = -1; dx <= 1 && !on; dx++)
                {
                    int nx = x + dx, ny = y + dy;
                    if (nx >= 0 && ny >= 0 && nx < w && ny < h && m[ny * w + nx]) on = true;
                }
                o[y * w + x] = on;
            }
            return o;
        }

        static bool[] Erode(bool[] m, int w, int h)
        {
            var o = new bool[m.Length];
            for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
            {
                bool on = true;
                for (int dy = -1; dy <= 1 && on; dy++)
                for (int dx = -1; dx <= 1 && on; dx++)
                {
                    int nx = x + dx, ny = y + dy;
                    if (nx < 0 || ny < 0 || nx >= w || ny >= h || !m[ny * w + nx]) on = false;
                }
                o[y * w + x] = on;
            }
            return o;
        }

        // lần viền ngoài Moore từ điểm đầu s (trên cùng, trái nhất nên ô phía Tây trống); dừng khi về s và bước kế trùng bước đầu
        static List<P> Trace(int[] lab, int w, int h, int id, int s)
        {
            var pts = new List<P>();
            int sx = s % w, sy = s / w;
            int px = sx, py = sy, back = 0; // back: hướng từ điểm đang đứng tới ô vừa rời (bắt đầu: Tây)
            int secondX = -1, secondY = -1, guard = 4 * w * h;
            pts.Add(new P(sx + 0.5f, sy + 0.5f));
            while (guard-- > 0)
            {
                int found = -1;
                for (int k = 1; k <= 8; k++)
                {
                    int d = (back + k) % 8;
                    int nx = px + DX[d], ny = py + DY[d];
                    if (nx < 0 || ny < 0 || nx >= w || ny >= h || lab[ny * w + nx] != id) continue;
                    found = d;
                    break;
                }
                if (found < 0) break; // điểm lẻ
                // ô trống ngay trước hướng tìm thấy thành ô vừa rời của điểm mới
                int bd = (found + 7) % 8;
                int bx = px + DX[bd], by = py + DY[bd];
                int cx = px + DX[found], cy = py + DY[found];
                if (px == sx && py == sy && pts.Count > 1 && cx == secondX && cy == secondY) break;
                if (secondX < 0)
                {
                    secondX = cx;
                    secondY = cy;
                }
                px = cx;
                py = cy;
                back = Dir(bx - px, by - py);
                if (px == sx && py == sy) continue; // về đầu: chưa thêm lại, xét bước kế để dừng
                pts.Add(new P(px + 0.5f, py + 0.5f));
            }
            return pts;
        }

        static int Dir(int dx, int dy)
        {
            for (int d = 0; d < 8; d++)
                if (DX[d] == dx && DY[d] == dy)
                    return d;
            return 0;
        }

        // bớt điểm cho vòng kín: chạy trên đường hở có điểm đầu lặp ở cuối, bỏ điểm cuối
        static List<P> Rdp(List<P> pts, float eps)
        {
            var open = new List<P>(pts) { pts[0] };
            var keep = new bool[open.Count];
            keep[0] = keep[open.Count - 1] = true;
            var st = new Stack<(int a, int b)>();
            st.Push((0, open.Count - 1));
            while (st.Count > 0)
            {
                var (a, b) = st.Pop();
                if (b - a < 2) continue;
                float ax = open[a].x, ay = open[a].y, bx = open[b].x, by = open[b].y;
                float vx = bx - ax, vy = by - ay, len = (float)Math.Sqrt(vx * vx + vy * vy);
                int far = -1;
                float best = eps;
                for (int i = a + 1; i < b; i++)
                {
                    float dx = open[i].x - ax, dy = open[i].y - ay;
                    float dd = len < 1e-4f ? (float)Math.Sqrt(dx * dx + dy * dy) : Math.Abs(dx * vy - dy * vx) / len;
                    if (dd > best)
                    {
                        best = dd;
                        far = i;
                    }
                }
                if (far < 0) continue;
                keep[far] = true;
                st.Push((a, far));
                st.Push((far, b));
            }
            var o = new List<P>();
            for (int i = 0; i < open.Count - 1; i++)
                if (keep[i])
                    o.Add(open[i]);
            return o;
        }

        // bo góc một lượt cho vòng kín, giữ điểm đầu ở chỗ cũ (đỉnh)
        static List<P> Chaikin(List<P> pts)
        {
            var o = new List<P> { pts[0] };
            int n = pts.Count;
            for (int i = 0; i < n; i++)
            {
                var a = pts[i];
                var b = pts[(i + 1) % n];
                o.Add(new P(0.75f * a.x + 0.25f * b.x, 0.75f * a.y + 0.25f * b.y));
                o.Add(new P(0.25f * a.x + 0.75f * b.x, 0.25f * a.y + 0.75f * b.y));
            }
            return o;
        }

        // diện tích có dấu (y lên): dương là ngược chiều kim đồng hồ
        static float Area(List<P> p)
        {
            double s = 0;
            for (int i = 0; i < p.Count; i++)
            {
                var a = p[i];
                var b = p[(i + 1) % p.Count];
                s += (double)a.x * b.y - (double)b.x * a.y;
            }
            return (float)(s / 2);
        }
    }
}
