// Nét chì vẽ dần theo các vòng viền của tướng (màn mở khoá tướng, HeroUnlockView; người dùng 2026-11-24: bút chì đi theo viền thật).
// Graphic tự dựng lưới (không sinh đồ vật): mỗi đoạn một dải, nối đầu đè lên nhau cho kín khớp, bề dày đổi nhẹ theo nhịp tay.
// Toạ độ điểm là toạ độ cục bộ của khung này. Drawn: độ dài đã vẽ (điểm UI), cộng dồn qua các vòng theo thứ tự.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class InkStroke : MaskableGraphic
    {
        public float width = 6;

        readonly List<Vector2[]> loops = new List<Vector2[]>();
        readonly List<float> lens = new List<float>();
        float drawn;

        public float Total { get; private set; }
        public int Count => loops.Count;
        public float LoopLength(int i) => lens[i];
        public Vector2 LoopStart(int i) => loops[i][0];

        public float Drawn
        {
            get => drawn;
            set
            {
                if (Mathf.Approximately(drawn, value)) return;
                drawn = value;
                SetVerticesDirty();
            }
        }

        // các vòng kín (điểm cuối nối về điểm đầu)
        public void SetLoops(List<Vector2[]> l)
        {
            loops.Clear();
            lens.Clear();
            Total = 0;
            foreach (var p in l)
            {
                if (p == null || p.Length < 2) continue;
                float s = 0;
                for (int i = 0; i < p.Length; i++) s += Vector2.Distance(p[i], p[(i + 1) % p.Length]);
                loops.Add(p);
                lens.Add(s);
                Total += s;
            }
            drawn = 0;
            SetVerticesDirty();
        }

        // điểm trên vòng i ở độ dài d tính từ đầu vòng
        public Vector2 PointOn(int i, float d)
        {
            var p = loops[i];
            d = Mathf.Repeat(d, Mathf.Max(lens[i], 1e-3f));
            for (int k = 0; k < p.Length; k++)
            {
                var a = p[k];
                var b = p[(k + 1) % p.Length];
                float L = Vector2.Distance(a, b);
                if (d <= L) return L < 1e-4f ? a : Vector2.Lerp(a, b, d / L);
                d -= L;
            }
            return p[0];
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            float left = drawn;
            Color32 c = color;
            int seg = 0;
            for (int li = 0; li < loops.Count && left > 0; li++)
            {
                var p = loops[li];
                for (int k = 0; k < p.Length && left > 0; k++, seg++)
                {
                    var a = p[k];
                    var b = p[(k + 1) % p.Length];
                    float L = Vector2.Distance(a, b);
                    if (L < 1e-4f) continue;
                    if (left < L) b = Vector2.Lerp(a, b, left / L);
                    left -= L;
                    // nhịp tay: dày mỏng theo nhiễu chậm dọc nét
                    float w = width * (0.75f + 0.5f * Mathf.PerlinNoise(seg * 0.11f, li * 3.7f));
                    Seg(vh, a, b, w, c);
                }
            }
        }

        static void Seg(VertexHelper vh, Vector2 a, Vector2 b, float w, Color32 c)
        {
            var d = (b - a).normalized;
            var n = new Vector2(-d.y, d.x) * (w * 0.5f);
            a -= d * (w * 0.35f); // đè lên đoạn trước cho kín khớp
            b += d * (w * 0.35f);
            int i = vh.currentVertCount;
            vh.AddVert(a - n, c, Vector2.zero);
            vh.AddVert(a + n, c, Vector2.zero);
            vh.AddVert(b + n, c, Vector2.zero);
            vh.AddVert(b - n, c, Vector2.zero);
            vh.AddTriangle(i, i + 1, i + 2);
            vh.AddTriangle(i, i + 2, i + 3);
        }
    }
}
