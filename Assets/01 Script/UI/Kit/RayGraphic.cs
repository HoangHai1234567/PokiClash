// Tia tập trung kiểu truyện tranh: các nêm mảnh tỏa từ một tâm ra xa, cách tâm một khoảng trống (chỗ nhân vật). Một màu (color),
// độ rộng và khoảng hở của nêm ngẫu nhiên theo hạt giống cố định. Dùng làm nền khung truyện của màn VS khi chưa có ảnh nền vẽ tay.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    [RequireComponent(typeof(CanvasRenderer))]
    public sealed class RayGraphic : MaskableGraphic
    {
        [SerializeField] int count = 46;
        [SerializeField] float inner = 260, outer = 1800; // bán kính đầu trong (vùng trống giữa), đầu ngoài
        [SerializeField] float width = 0.5f; // độ rộng nêm so với khoảng góc của nó (0..1)
        [SerializeField] int seed = 7;

        public void Set(float innerRadius, float outerRadius)
        {
            inner = innerRadius;
            outer = outerRadius;
            SetVerticesDirty();
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            if (count < 3) return;
            Color32 c = color;
            var state = Random.state;
            Random.InitState(seed);
            float step = Mathf.PI * 2 / count;
            for (int i = 0; i < count; i++)
            {
                float a = i * step + Random.Range(-0.3f, 0.3f) * step;
                float w = step * width * Random.Range(0.35f, 1f) * 0.5f;
                float r0 = inner * Random.Range(0.85f, 1.35f);
                var tip = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * r0;
                var l = new Vector2(Mathf.Cos(a - w), Mathf.Sin(a - w)) * outer;
                var r = new Vector2(Mathf.Cos(a + w), Mathf.Sin(a + w)) * outer;
                int k = vh.currentVertCount;
                vh.AddVert(tip, c, Vector2.zero);
                vh.AddVert(l, c, Vector2.zero);
                vh.AddVert(r, c, Vector2.zero);
                vh.AddTriangle(k, k + 1, k + 2);
            }
            Random.state = state;
        }
    }
}
