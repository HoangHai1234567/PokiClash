// Lấp lánh nhấp nháy trong một vùng (popup bán bản 4, người dùng 2026-11-27: "thêm fx glow ánh sáng các kiểu vào cho đẹp"): các sao bốn cánh
// (lap_lanh.png) dựng sẵn làm con trong prefab (stars) hiện ở chỗ ngẫu nhiên trong khung RectTransform của chính nó, phồng lên rồi tắt trong
// ~period giây, vừa xoay vừa mờ, xong lại hiện chỗ khác; lệch nhịp nhau. Không sinh đồ vật lúc chạy (PrefabOnlyTests).
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class Twinkle : MonoBehaviour
    {
        public Image[] stars;
        public Vector2 size = new Vector2(26, 52); // cỡ nhỏ nhất / lớn nhất
        public float period = 1.2f;
        public Color color = Color.white;

        float[] t0, dur, rot;

        void OnEnable()
        {
            if (stars == null) return;
            int n = stars.Length;
            t0 = new float[n];
            dur = new float[n];
            rot = new float[n];
            float now = Time.unscaledTime;
            for (int i = 0; i < n; i++) Place(i, now + Random.Range(0f, period));
        }

        void Place(int i, float start)
        {
            var s = stars[i];
            if (!s) return;
            var r = ((RectTransform)transform).rect;
            var rt = s.rectTransform;
            rt.anchoredPosition = new Vector2(Random.Range(r.xMin, r.xMax), Random.Range(r.yMin, r.yMax));
            float sz = Random.Range(size.x, size.y);
            rt.sizeDelta = new Vector2(sz, sz);
            t0[i] = start;
            dur[i] = period * Random.Range(0.75f, 1.3f);
            rot[i] = Random.Range(-25f, 25f);
            rt.localScale = Vector3.zero;
        }

        void Update()
        {
            if (stars == null || t0 == null) return;
            float now = Time.unscaledTime;
            for (int i = 0; i < stars.Length; i++)
            {
                var s = stars[i];
                if (!s) continue;
                float k = (now - t0[i]) / dur[i];
                if (k < 0) continue;
                if (k >= 1)
                {
                    Place(i, now + Random.Range(0.1f, period * 0.6f));
                    continue;
                }
                float e = Mathf.Sin(k * Mathf.PI);
                s.rectTransform.localScale = new Vector3(e, e, 1);
                s.rectTransform.localEulerAngles = new Vector3(0, 0, rot[i] + 70 * k);
                var c = color;
                c.a *= e;
                s.color = c;
            }
        }
    }
}
