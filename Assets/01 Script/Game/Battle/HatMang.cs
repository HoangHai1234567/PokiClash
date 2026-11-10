// Mảng nước liền tô phẳng (bộ Thủy 2026-11-10): thân vòi rồng, con sóng thần, lưỡi nước, cột nước phun, lõi tia nước. Hạt rời không
// tạo được khối nước lớn nên lớp hạt HatLua gửi các đa giác của khung hình sang đây, thành phần này vẽ thành một lưới uGUI:
// - Fill: đa giác kín (cắt tai, đa giác lõm được);
// - Band: dải kín giữa hai đường viền cùng số điểm (viền mực, các lớp màu lồng nhau: không chồng nhau nên làm trong mờ được);
// - Ribbon: dải hở giữa hai đường (lõi tia nước).
// Mép ngoài có một viền mờ dần 1,5 px cho khỏi răng cưa. Màu là màu đỉnh nhân với ô vân chì lặp (Assets/03 Art/Fx/Hat/van_chi.png).
// Đặt sẵn trong prefab làm con ĐẦU của mỗi lớp hạt (menu "PokiClash/Prefab/Sàn đấu: hạt lửa"): mọi mảng nằm dưới các hạt cùng lớp.
// Khung của thành phần đặt rộng 8000 quanh gốc (pivot giữa) để RectMask2D của ô xem tướng không loại cả lưới; gốc toạ độ vẫn là
// góc trên trái của lớp hạt như các Image hạt.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    [RequireComponent(typeof(CanvasRenderer))]
    public sealed class HatMang : MaskableGraphic
    {
        public const byte Fill = 0, Band = 1, Ribbon = 2;

        public struct Shape
        {
            public byte kind;
            public int a0, b0, n; // điểm đường ngoài, đường trong (Band, Ribbon), số điểm mỗi đường
            public Color32 col;
            public bool fringe;
        }

        [SerializeField] Texture2D van; // ô vân chì lặp
        [SerializeField] float tile = 72; // cạnh một ô vân (đơn vị UI)
        const float Soft = 1.5f; // bề rộng viền mờ (đơn vị UI)

        readonly List<Vector2> pts = new List<Vector2>(2048);
        readonly List<Shape> shapes = new List<Shape>(128);
        static readonly List<int> ring = new List<int>(256);
        bool had;

        public override Texture mainTexture => van ? van : s_WhiteTexture;

        public void Begin()
        {
            pts.Clear();
            shapes.Clear();
        }

        public int PointCount => pts.Count;
        public void Point(Vector2 ui) => pts.Add(ui);
        public void Add(Shape s) => shapes.Add(s);

        public void End()
        {
            if (shapes.Count > 0 || had) SetVerticesDirty();
            had = shapes.Count > 0;
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            for (int i = 0; i < shapes.Count; i++)
            {
                var s = shapes[i];
                if (s.n < 2) continue;
                if (s.kind == Fill) DoFill(vh, s);
                else DoBand(vh, s, s.kind == Ribbon);
            }
        }

        int Vert(VertexHelper vh, Vector2 p, Color32 c)
        {
            vh.AddVert(new Vector3(p.x, p.y, 0), c, new Vector4(p.x / tile, p.y / tile, 0, 0));
            return vh.currentVertCount - 1;
        }

        static float Cross(Vector2 a, Vector2 b) => a.x * b.y - a.y * b.x;

        float Area(int a0, int n)
        {
            float s = 0;
            for (int i = 0; i < n; i++) s += Cross(pts[a0 + i], pts[a0 + (i + 1) % n]);
            return s;
        }

        static bool InTri(Vector2 p, Vector2 a, Vector2 b, Vector2 c)
        {
            float d1 = Cross(b - a, p - a), d2 = Cross(c - b, p - b), d3 = Cross(a - c, p - c);
            bool neg = d1 < 0 || d2 < 0 || d3 < 0, pos = d1 > 0 || d2 > 0 || d3 > 0;
            return !(neg && pos);
        }

        void DoFill(VertexHelper vh, Shape s)
        {
            int n = s.n, a0 = s.a0;
            if (n < 3) return;
            int v0 = vh.currentVertCount;
            for (int i = 0; i < n; i++) Vert(vh, pts[a0 + i], s.col);
            bool ccw = Area(a0, n) > 0;
            ring.Clear();
            for (int i = 0; i < n; i++) ring.Add(i);
            int guard = n * n + 8;
            while (ring.Count > 3 && guard-- > 0)
            {
                bool cut = false;
                int m = ring.Count;
                for (int i = 0; i < m; i++)
                {
                    int ia = ring[(i + m - 1) % m], ib = ring[i], ic = ring[(i + 1) % m];
                    Vector2 A = pts[a0 + ia], B = pts[a0 + ib], C = pts[a0 + ic];
                    float cr = Cross(B - A, C - B);
                    if (Mathf.Abs(cr) < 1e-5f) // ba điểm thẳng hàng: bỏ điểm giữa
                    {
                        ring.RemoveAt(i);
                        cut = true;
                        break;
                    }
                    if (ccw ? cr < 0 : cr > 0) continue; // góc lõm
                    bool inside = false;
                    for (int j = 0; j < m; j++)
                    {
                        int ij = ring[j];
                        if (ij == ia || ij == ib || ij == ic) continue;
                        if (InTri(pts[a0 + ij], A, B, C))
                        {
                            inside = true;
                            break;
                        }
                    }
                    if (inside) continue;
                    vh.AddTriangle(v0 + ia, v0 + ib, v0 + ic);
                    ring.RemoveAt(i);
                    cut = true;
                    break;
                }
                if (!cut) break;
            }
            for (int i = 1; i + 1 < ring.Count; i++) vh.AddTriangle(v0 + ring[0], v0 + ring[i], v0 + ring[i + 1]);
            if (s.fringe) Fringe(vh, a0, n, v0, s.col, ccw ? 1 : -1, true);
        }

        void DoBand(VertexHelper vh, Shape s, bool open)
        {
            int n = s.n;
            int va = vh.currentVertCount;
            for (int i = 0; i < n; i++) Vert(vh, pts[s.a0 + i], s.col);
            int vb = vh.currentVertCount;
            for (int i = 0; i < n; i++) Vert(vh, pts[s.b0 + i], s.col);
            int last = open ? n - 1 : n;
            for (int i = 0; i < last; i++)
            {
                int j = (i + 1) % n;
                vh.AddTriangle(va + i, va + j, vb + j);
                vh.AddTriangle(va + i, vb + j, vb + i);
            }
            if (!s.fringe) return;
            if (open)
            {
                // dải hở: phía ngoài của đường a là phía xa đường b, và ngược lại
                var mid = pts[s.a0 + n / 2] - pts[s.b0 + n / 2];
                var dir = pts[s.a0 + Mathf.Min(n - 1, n / 2 + 1)] - pts[s.a0 + Mathf.Max(0, n / 2 - 1)];
                float sign = Cross(dir, mid) > 0 ? -1 : 1; // pháp tuyến (dy, -dx) * sign chĩa về phía mid
                Fringe(vh, s.a0, n, va, s.col, sign, false);
                Fringe(vh, s.b0, n, vb, s.col, -sign, false);
            }
            else Fringe(vh, s.a0, n, va, s.col, Area(s.a0, n) > 0 ? 1 : -1, true);
        }

        // viền mờ dần ra ngoài đường a0..a0+n (đỉnh đã có từ v0); sign: 1 nếu đường đi ngược chiều kim đồng hồ (pháp tuyến ngoài là
        // (dy, -dx)), -1 nếu ngược lại
        void Fringe(VertexHelper vh, int a0, int n, int v0, Color32 col, float sign, bool closed)
        {
            var clear = col;
            clear.a = 0;
            int f0 = vh.currentVertCount;
            for (int i = 0; i < n; i++)
            {
                int ip = closed ? (i + n - 1) % n : Mathf.Max(0, i - 1), inx = closed ? (i + 1) % n : Mathf.Min(n - 1, i + 1);
                Vector2 p = pts[a0 + i], e1 = p - pts[a0 + ip], e2 = pts[a0 + inx] - p;
                Vector2 n1 = new Vector2(e1.y, -e1.x), n2 = new Vector2(e2.y, -e2.x);
                if (n1.sqrMagnitude > 1e-8f) n1.Normalize();
                if (n2.sqrMagnitude > 1e-8f) n2.Normalize();
                var vn = n1 + n2;
                float len = vn.magnitude;
                vn = len > 1e-4f ? vn / len : (n2.sqrMagnitude > 0 ? n2 : n1);
                float k = Soft / Mathf.Max(0.5f, Vector2.Dot(vn, n2.sqrMagnitude > 0 ? n2 : n1));
                Vert(vh, p + vn * (sign * k), clear);
            }
            int last = closed ? n : n - 1;
            for (int i = 0; i < last; i++)
            {
                int j = (i + 1) % n;
                vh.AddTriangle(v0 + i, v0 + j, f0 + j);
                vh.AddTriangle(v0 + i, f0 + j, f0 + i);
            }
        }
    }
}
