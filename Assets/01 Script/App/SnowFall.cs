// Tuyết rơi (mùa Noel ở sảnh và màn tải, HubSeason / VoyageSeason; dùng lại được ở màn khác). Một Graphic vẽ cả đám bông tuyết bằng một
// lưới (mỗi bông một ô vuông) và có Canvas riêng để dựng lại lưới mỗi khung không làm bẩn canvas của màn. Hai lớp: xa (nhỏ, chậm, nhạt) và
// gần (to, nhanh, ít bông); mỗi bông lắc ngang theo sóng riêng, gió đẩy nhẹ sang phải.
// Gắn với thế giới, không đứng yên như giao diện (người dùng 2026-11-27: "khi drag cam thì vị trí cũng phải thay đổi"): scroll là độ dời
// của thế giới trên màn (sảnh: độ dời lớp bản đồ HubPan; màn tải: camera chuyến tàu); mỗi bông dời theo scroll × thị sai riêng (lớp gần
// 1,15–1,3: gần mắt hơn mặt đất nên trôi nhanh hơn; lớp xa 0,8–0,95). Bông nằm trong một ô lặp vô hạn (khung + lề 40 điểm), ra khỏi một mép
// thì vào lại mép đối diện ngoài tầm nhìn: kéo tới đâu cũng có tuyết.
// Hình bông: đĩa trắng mép hơi méo, viền xanh xám nhạt, vẽ bằng mã (tô phẳng, không quầng sáng, không bóng). Không nhận chạm.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class SnowFall : MaskableGraphic
    {
        // số bông, cỡ chỉnh theo ảnh chụp sảnh 2026-11-27 (80 bông 6–13 điểm thì gần như không thấy trên đảo sáng)
        public int count = 130;
        public float wind = 14; // điểm / giây sang phải (bông to trôi nhanh hơn)
        [Range(0, 1)] public float nearShare = 0.25f; // phần bông lớp gần
        public Vector2 scroll; // độ dời của thế giới trên màn (điểm canvas)
        const float Margin = 40;

        struct Flake
        {
            public float x, y, size, speed, amp, freq, phase, a, par;
        }

        Flake[] flakes;
        float t;
        static Texture2D tex;

        public static Texture2D FlakeTexture
        {
            get
            {
                if (!tex) tex = MakeTex();
                return tex;
            }
        }

        public override Texture mainTexture => FlakeTexture;

        protected override void Awake()
        {
            base.Awake();
            raycastTarget = false;
        }

        void Init()
        {
            var r = rectTransform.rect;
            flakes = new Flake[Mathf.Max(1, count)];
            for (int i = 0; i < flakes.Length; i++)
            {
                ref var f = ref flakes[i];
                bool near = Random.value < nearShare;
                f.size = near ? Random.Range(20f, 32f) : Random.Range(10f, 18f);
                f.speed = near ? Random.Range(120f, 180f) : Random.Range(50f, 100f);
                f.amp = Random.Range(8f, 26f);
                f.freq = Random.Range(0.25f, 0.6f); // lần lắc / giây
                f.phase = Random.Range(0f, 6.283f);
                f.a = near ? Random.Range(0.9f, 1f) : Random.Range(0.7f, 0.9f);
                f.par = near ? Random.Range(1.15f, 1.3f) : Random.Range(0.8f, 0.95f);
                f.x = Random.Range(r.xMin - Margin, r.xMax + Margin);
                f.y = Random.Range(r.yMin - Margin, r.yMax + Margin);
            }
        }

        void Update()
        {
            var r = rectTransform.rect;
            if (r.width <= 0) return;
            if (flakes == null || flakes.Length != count) Init();
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            t += dt;
            float w = r.width + 2 * Margin, h = r.height + 2 * Margin;
            for (int i = 0; i < flakes.Length; i++)
            {
                ref var f = ref flakes[i];
                f.y = r.yMin - Margin + Mathf.Repeat(f.y - f.speed * dt - (r.yMin - Margin), h);
                f.x = r.xMin - Margin + Mathf.Repeat(f.x + wind * dt * (f.size / 12f) - (r.xMin - Margin), w);
            }
            SetVerticesDirty();
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            if (flakes == null) return;
            var r = rectTransform.rect;
            float x0 = r.xMin - Margin, y0 = r.yMin - Margin, w = r.width + 2 * Margin, h = r.height + 2 * Margin;
            var c = color;
            for (int i = 0; i < flakes.Length; i++)
            {
                var f = flakes[i];
                float x = x0 + Mathf.Repeat(f.x + Mathf.Sin(t * f.freq * 6.283f + f.phase) * f.amp + scroll.x * f.par - x0, w);
                float y = y0 + Mathf.Repeat(f.y + scroll.y * f.par - y0, h);
                float s = f.size * 0.5f;
                var col = new Color(c.r, c.g, c.b, c.a * f.a);
                int v = vh.currentVertCount;
                vh.AddVert(new Vector3(x - s, y - s), col, new Vector2(0, 0));
                vh.AddVert(new Vector3(x - s, y + s), col, new Vector2(0, 1));
                vh.AddVert(new Vector3(x + s, y + s), col, new Vector2(1, 1));
                vh.AddVert(new Vector3(x + s, y - s), col, new Vector2(1, 0));
                vh.AddTriangle(v, v + 1, v + 2);
                vh.AddTriangle(v + 2, v + 3, v);
            }
        }

        // đĩa trắng mép hơi méo (nét tay), viền xanh xám nhạt 4 điểm; mép khử răng cưa 1 điểm; có mipmap cho bông nhỏ khỏi lấm tấm
        static Texture2D MakeTex()
        {
            const int N = 64;
            var t = new Texture2D(N, N, TextureFormat.RGBA32, true) { name = "bong_tuyet", wrapMode = TextureWrapMode.Clamp, filterMode = FilterMode.Trilinear };
            var px = new Color32[N * N];
            var white = new Color(1f, 1f, 1f);
            var rim = new Color(0.80f, 0.86f, 0.93f);
            for (int y = 0; y < N; y++)
                for (int x = 0; x < N; x++)
                {
                    float dx = x + 0.5f - N / 2f, dy = y + 0.5f - N / 2f;
                    float d = Mathf.Sqrt(dx * dx + dy * dy), ang = Mathf.Atan2(dy, dx);
                    float R = 27f + 1.6f * Mathf.Sin(3 * ang + 0.7f) + 1.0f * Mathf.Sin(5 * ang + 2.1f);
                    float a = Mathf.Clamp01(R + 0.5f - d);
                    var col = Color.Lerp(rim, white, Mathf.Clamp01(R - 5f + 0.5f - d));
                    px[y * N + x] = new Color(col.r, col.g, col.b, a);
                }
            t.SetPixels32(px);
            t.Apply(true, true);
            return t;
        }
    }
}
