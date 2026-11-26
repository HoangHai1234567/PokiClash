// Dây câu của Bến câu (GD_Claude/32 mục 4): đường gấp khúc dày đều trong hệ toạ độ của RectTransform này, FishingPanel đặt điểm mỗi
// khung (đường cong bậc hai từ đầu cần tới phao, võng theo độ chùng). Tô một màu, không quầng sáng.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    [RequireComponent(typeof(CanvasRenderer))]
    public sealed class FishingLine : MaskableGraphic
    {
        [SerializeField] float width = 3f;
        readonly List<Vector2> pts = new List<Vector2>();

        public float Width { get => width; set { width = value; SetVerticesDirty(); } }

        /// <summary>Đường cong bậc hai a → b, điểm điều khiển ở giữa dời xuống `sag` (đơn vị cục bộ) và lệch ngang `side`.</summary>
        public void SetCurve(Vector2 a, Vector2 b, float sag, float side = 0f, int n = 22)
        {
            pts.Clear();
            var c = (a + b) * 0.5f + new Vector2(side, -sag);
            for (int i = 0; i <= n; i++)
            {
                float t = i / (float)n, u = 1 - t;
                pts.Add(u * u * a + 2 * u * t * c + t * t * b);
            }
            SetVerticesDirty();
        }

        public void Clear()
        {
            pts.Clear();
            SetVerticesDirty();
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            if (pts.Count < 2) return;
            float hw = width * 0.5f;
            Color32 c = color;
            for (int i = 0; i < pts.Count; i++)
            {
                Vector2 dir = i == 0 ? pts[1] - pts[0] : i == pts.Count - 1 ? pts[i] - pts[i - 1] : pts[i + 1] - pts[i - 1];
                if (dir.sqrMagnitude < 1e-6f) dir = Vector2.up;
                var nrm = new Vector2(-dir.y, dir.x).normalized * hw;
                vh.AddVert(pts[i] + nrm, c, Vector2.zero);
                vh.AddVert(pts[i] - nrm, c, Vector2.zero);
                if (i > 0)
                {
                    int k = i * 2;
                    vh.AddTriangle(k - 2, k - 1, k);
                    vh.AddTriangle(k - 1, k + 1, k);
                }
            }
        }
    }
}
