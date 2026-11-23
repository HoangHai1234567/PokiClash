// Lá, cánh hoa bay theo gió trên bản đồ Nhà (GD_Claude/22_Critters_Home.md mốc A4; học hạt gió pbvx_camp_wind của Clash of Critters:
// hạt sống 9–12 giây, bay chậm khắp map). Các Image dựng sẵn trong prefab (menu "PokiClash/Prefab/Nhà và side meta/Nhà: dựng màn", nút "hat/gio"), component
// này chỉ dời: trôi theo gió, lắc lư, lật (co giãn ngang theo sin), ra khỏi bản đồ thì vào lại ở mép đối diện; mờ dần ở mép. Lớp "hat"
// nằm dưới lớp nhuộm nên đêm lá tối theo cảnh.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HomeWind : MonoBehaviour
    {
        [SerializeField] Image[] leaves;
        [SerializeField] Vector2 wind = new Vector2(-46f, 16f); // px bản đồ mỗi giây (y xuống)
        [SerializeField] float edge = 260f; // dải mép mờ dần (px bản đồ)

        Vector2[] pos;
        float[] phase, speed, spin;
        Vector2 size;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Image[] items) => leaves = items;

        // ảnh lá thứ i theo thứ tự prefab dựng (home_leaf_1..4 xoay vòng: 0–2 lá, 3 cánh hoa): lá văng khi cây bay, lá rụng khi cây lắc
        public Sprite Leaf(int i) => leaves != null && leaves.Length > 0 && leaves[i % leaves.Length] ? leaves[i % leaves.Length].sprite : null;

        void OnEnable()
        {
            if (leaves == null || leaves.Length == 0) return;
            size = ((RectTransform)transform).rect.size;
            if (size.x <= 0 || size.y <= 0) return;
            int n = leaves.Length;
            pos = new Vector2[n];
            phase = new float[n];
            speed = new float[n];
            spin = new float[n];
            var rnd = new System.Random(5);
            for (int i = 0; i < n; i++)
            {
                pos[i] = new Vector2((float)rnd.NextDouble() * size.x, (float)rnd.NextDouble() * size.y);
                phase[i] = (float)rnd.NextDouble() * 10f;
                speed[i] = 0.7f + (float)rnd.NextDouble() * 0.6f;
                spin[i] = 1.2f + (float)rnd.NextDouble() * 1.6f;
            }
        }

        void Update()
        {
            if (pos == null) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.1f), t = Time.unscaledTime;
            for (int i = 0; i < leaves.Length; i++)
            {
                var img = leaves[i];
                if (!img) continue;
                var p = pos[i] + (wind * speed[i] + new Vector2(0, Mathf.Sin(t * 1.3f + phase[i]) * 22f)) * dt;
                // ra khỏi bản đồ: vào lại ở mép đối diện
                if (p.x < -40) p.x += size.x + 80;
                if (p.x > size.x + 40) p.x -= size.x + 80;
                if (p.y < -40) p.y += size.y + 80;
                if (p.y > size.y + 40) p.y -= size.y + 80;
                pos[i] = p;
                var rt = img.rectTransform;
                rt.anchoredPosition = new Vector2(p.x, -p.y);
                float flip = Mathf.Sin(t * spin[i] + phase[i]);
                rt.localScale = new Vector3(Mathf.Lerp(0.25f, 1f, Mathf.Abs(flip)) * Mathf.Sign(flip + 0.0001f), 1, 1);
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * 0.9f + phase[i] * 2f) * 35f);
                float d = Mathf.Min(Mathf.Min(p.x, size.x - p.x), Mathf.Min(p.y, size.y - p.y));
                var c = img.color;
                c.a = Mathf.Clamp01(d / edge);
                img.color = c;
            }
        }
    }
}
