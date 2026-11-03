// Đa giác lồi tô một màu (khung truyện tranh chéo của màn VS và viền mực của nó). Đỉnh tính theo đơn vị UI, gốc là pivot của khung,
// xếp theo thứ tự quanh viền. Làm hình cho Mask được: Mask cắt đúng theo đa giác. Inset: co đa giác vào trong một khoảng đều.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    [RequireComponent(typeof(CanvasRenderer))]
    public sealed class PolyGraphic : MaskableGraphic
    {
        [SerializeField] Vector2[] points = new Vector2[0];

        public Vector2[] Points
        {
            get => points;
            set
            {
                points = value;
                SetVerticesDirty();
            }
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            if (points == null || points.Length < 3) return;
            Color32 c = color;
            foreach (var p in points) vh.AddVert(p, c, Vector2.zero);
            for (int i = 1; i < points.Length - 1; i++) vh.AddTriangle(0, i, i + 1);
        }

        // co đa giác lồi vào trong d (mỗi cạnh dời vào d theo pháp tuyến, đỉnh mới là giao hai cạnh kề); chiều đỉnh nào cũng được
        public static Vector2[] Inset(Vector2[] pts, float d)
        {
            int n = pts.Length;
            float area = 0;
            for (int i = 0; i < n; i++) area += pts[i].x * pts[(i + 1) % n].y - pts[(i + 1) % n].x * pts[i].y;
            float side = area > 0 ? 1 : -1; // ngược chiều kim đồng hồ: pháp tuyến trong là bên trái cạnh
            var res = new Vector2[n];
            for (int i = 0; i < n; i++)
            {
                Vector2 a0 = pts[(i + n - 1) % n], a1 = pts[i], b1 = pts[(i + 1) % n];
                Vector2 da = (a1 - a0).normalized, db = (b1 - a1).normalized;
                Vector2 na = new Vector2(-da.y, da.x) * side, nb = new Vector2(-db.y, db.x) * side;
                Vector2 pa = a1 + na * d, pb = a1 + nb * d;
                float cross = da.x * db.y - da.y * db.x;
                if (Mathf.Abs(cross) < 1e-5f)
                {
                    res[i] = pa;
                    continue;
                }
                float t = ((pb.x - pa.x) * db.y - (pb.y - pa.y) * db.x) / cross;
                res[i] = pa + da * t;
            }
            return res;
        }
    }
}
