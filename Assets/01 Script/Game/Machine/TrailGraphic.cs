// Vệt đuôi một bi (prefab mục Items/VetBiDai): dải liền qua các điểm mẫu, như TrailRenderer nhưng trong uGUI. Mỗi điểm có
// độ mờ riêng (mới đậm, cũ nhạt); ngang dải ba làn đỉnh, hai mép nhạt hơn giữa nên mép mềm. Toạ độ điểm là toạ độ máy
// (MachineBoard.Local), gốc của Graphic đặt ở góc trên trái lớp vệt.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class TrailGraphic : MaskableGraphic
    {
        public const float EdgeAlpha = 0.25f; // độ mờ mép so với giữa dải

        readonly List<Vector2> pts = new List<Vector2>();
        readonly List<float> alphas = new List<float>();
        float width;

        // điểm từ đầu (bi) về đuôi, alpha 0..1 theo từng điểm
        public void Set(List<Vector2> points, List<float> alpha, float w, Color c)
        {
            pts.Clear();
            pts.AddRange(points);
            alphas.Clear();
            alphas.AddRange(alpha);
            width = w;
            color = c;
            SetVerticesDirty();
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            int n = pts.Count;
            if (n < 2) return;
            var c = color;
            for (int i = 0; i < n; i++)
            {
                // pháp tuyến theo hướng trung bình của hai đoạn kề
                var d = pts[Mathf.Min(i + 1, n - 1)] - pts[Mathf.Max(i - 1, 0)];
                if (d.sqrMagnitude < 1e-6f) d = Vector2.right;
                d.Normalize();
                var nrm = new Vector2(-d.y, d.x) * (width / 2);
                float a = c.a * alphas[i];
                var mid = new Color(c.r, c.g, c.b, a);
                var edge = new Color(c.r, c.g, c.b, a * EdgeAlpha);
                vh.AddVert(pts[i] + nrm, edge, Vector4.zero);
                vh.AddVert(pts[i], mid, Vector4.zero);
                vh.AddVert(pts[i] - nrm, edge, Vector4.zero);
            }
            for (int i = 0; i < n - 1; i++)
            {
                int k = i * 3, m = k + 3;
                vh.AddTriangle(k, k + 1, m + 1);
                vh.AddTriangle(k, m + 1, m);
                vh.AddTriangle(k + 1, k + 2, m + 2);
                vh.AddTriangle(k + 1, m + 2, m + 1);
            }
        }
    }
}
