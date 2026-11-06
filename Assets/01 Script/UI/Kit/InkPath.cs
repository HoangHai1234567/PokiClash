// Nét mực vẽ dần theo đường gấp khúc (mũi tên kế hoạch, vòng khoanh trên sa bàn màn boot): nét liền hoặc đứt, đầu tròn.
// Reveal: phần độ dài đã vẽ (0..1); Offset: dời pha nét đứt về phía cuối đường (tăng dần thì nét chạy). Điểm theo đơn vị UI,
// gốc ở pivot. Một màu (Graphic.color); viền mực quanh nét màu thì đặt một InkPath mực to hơn nằm dưới.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    [RequireComponent(typeof(CanvasRenderer))]
    public sealed class InkPath : MaskableGraphic
    {
        const int CapSegments = 10;

        [SerializeField] Vector2[] points = new Vector2[0];
        [SerializeField] float width = 8;
        [SerializeField] float dash, gap; // dash = 0: nét liền
        [SerializeField] bool closed;
        [SerializeField, Range(0, 1)] float reveal = 1;
        [SerializeField] float offset;

        float[] cum;
        Vector2[] path;

        public float Reveal
        {
            get => reveal;
            set
            {
                value = Mathf.Clamp01(value);
                if (Mathf.Approximately(value, reveal)) return;
                reveal = value;
                SetVerticesDirty();
            }
        }

        public float Offset
        {
            get => offset;
            set
            {
                if (Mathf.Approximately(value, offset)) return;
                offset = value;
                if (dash > 0) SetVerticesDirty();
            }
        }

        // Dùng khi nướng prefab (Editor).
        public void Setup(Vector2[] pts, float lineWidth, float dashLen = 0, float gapLen = 0, bool isClosed = false)
        {
            points = pts;
            width = lineWidth;
            dash = dashLen;
            gap = gapLen;
            closed = isClosed;
            cum = null;
            SetVerticesDirty();
        }

        protected override void OnValidate()
        {
            base.OnValidate();
            cum = null;
        }

        void Measure()
        {
            int n = points.Length + (closed && points.Length > 2 ? 1 : 0);
            path = new Vector2[n];
            for (int i = 0; i < n; i++) path[i] = points[i % points.Length];
            cum = new float[n];
            for (int i = 1; i < n; i++) cum[i] = cum[i - 1] + Vector2.Distance(path[i - 1], path[i]);
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            if (points == null || points.Length < 2 || reveal <= 0 || width <= 0) return;
            if (cum == null || path == null || path.Length != points.Length + (closed && points.Length > 2 ? 1 : 0)) Measure();
            float total = cum[cum.Length - 1];
            float end = total * reveal;
            Color32 c = color;
            if (dash <= 0)
            {
                Stroke(vh, 0, end, c);
                return;
            }
            float period = dash + Mathf.Max(0, gap);
            for (float s = Mathf.Repeat(offset, period) - period; s < end; s += period)
            {
                float a = Mathf.Max(0, s), b = Mathf.Min(end, s + dash);
                if (b > a) Stroke(vh, a, b, c);
            }
        }

        Vector2 At(float s, out int seg)
        {
            seg = 0;
            while (seg < cum.Length - 2 && cum[seg + 1] < s) seg++;
            float len = cum[seg + 1] - cum[seg];
            float k = len > 1e-4f ? (s - cum[seg]) / len : 0;
            return Vector2.Lerp(path[seg], path[seg + 1], Mathf.Clamp01(k));
        }

        // đoạn từ độ dài a tới b: các đoạn thẳng nối nhau, chỗ nối và hai đầu là đĩa tròn
        void Stroke(VertexHelper vh, float a, float b, Color32 c)
        {
            var p = At(a, out int sa);
            var q = At(b, out int sb);
            var prev = p;
            Cap(vh, p, c);
            for (int i = sa + 1; i <= sb; i++)
            {
                Segment(vh, prev, path[i], c);
                Cap(vh, path[i], c);
                prev = path[i];
            }
            Segment(vh, prev, q, c);
            Cap(vh, q, c);
        }

        void Segment(VertexHelper vh, Vector2 p, Vector2 q, Color32 c)
        {
            var d = q - p;
            float len = d.magnitude;
            if (len < 1e-3f) return;
            var n = new Vector2(-d.y, d.x) / len * (width * 0.5f);
            int i0 = vh.currentVertCount;
            vh.AddVert(p + n, c, Vector2.zero);
            vh.AddVert(p - n, c, Vector2.zero);
            vh.AddVert(q - n, c, Vector2.zero);
            vh.AddVert(q + n, c, Vector2.zero);
            vh.AddTriangle(i0, i0 + 1, i0 + 2);
            vh.AddTriangle(i0, i0 + 2, i0 + 3);
        }

        void Cap(VertexHelper vh, Vector2 at, Color32 c)
        {
            float r = width * 0.5f;
            int i0 = vh.currentVertCount;
            vh.AddVert(at, c, Vector2.zero);
            for (int k = 0; k < CapSegments; k++)
            {
                float t = k * Mathf.PI * 2 / CapSegments;
                vh.AddVert(at + new Vector2(Mathf.Cos(t), Mathf.Sin(t)) * r, c, Vector2.zero);
            }
            for (int k = 0; k < CapSegments; k++) vh.AddTriangle(i0, i0 + 1 + k, i0 + 1 + (k + 1) % CapSegments);
        }
    }
}

