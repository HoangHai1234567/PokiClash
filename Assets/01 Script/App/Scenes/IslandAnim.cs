// Lớp phần động trên ảnh đảo (sảnh: con của ảnh đảo "dao" trong Screens/Hub; đảo hệ: con của ảnh bản đồ trong Screens/Zone):
// đọc island_anim.json (ArtGen/Islands/compose_islands.py ghi; toạ độ tỉ lệ theo ảnh, cỡ tỉ lệ theo bề ngang ảnh) và sprite
// Islands/Anim/anim_<tên>. Mỗi món một kiểu chuyển động: khói bốc nở mờ dần, lửa lật hai hình, bánh răng xoay, chuông lắc rồi
// nghỉ, xoáy nước xoay kèm đinh ba nhấp nhô, bọt phập phồng, lấp lánh, lá rơi, gió cuộn, gợn nước, sóng trôi ngoài biển; sông
// dung nham và suối có đốm lửa / gợn nước chạy dọc. Tắt "nét vẽ rung" (hoặc chụp ảnh tĩnh) thì đứng yên.
// Sảnh tự gắn theo key (world); màn đảo gọi Bind("zone_<hệ>") mỗi lần vào đảo. Mỗi hình động sinh từ prefab mục Items/HinhDong.
// Hạt dọc dòng chảy lấy cỡ theo bề rộng dòng (w trong json); gợn nước nằm dọc theo dòng.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class IslandAnim : MonoBehaviour
    {
        [SerializeField] TextAsset data; // Assets/03 Art/Islands/island_anim.json
        [SerializeField] Image itemPrefab; // Items/HinhDong: Image không nhận chạm, neo góc dưới trái
        [Tooltip("Gắn sẵn khi vào màn (sảnh: world); rỗng thì chờ Bind")]
        [SerializeField] string autoKey;

        // một món đang chạy: cập nhật theo thời gian
        abstract class Fx
        {
            public IslandAnim host;
            public abstract void Tick(float t);
        }

        readonly List<Fx> fx = new List<Fx>();
        Dictionary<string, object> root;
        float clock;

        RectTransform Rt => (RectTransform)transform;

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextAsset json, string key, Image item)
        {
            data = json;
            itemPrefab = item;
            autoKey = key;
        }

        void Start()
        {
            if (!string.IsNullOrEmpty(autoKey)) Bind(autoKey);
        }

        public void Bind(string key)
        {
            foreach (Transform c in transform) Destroy(c.gameObject);
            fx.Clear();
            if (!data || !itemPrefab || !App.Art) return;
            root ??= J.Obj(MiniJson.Parse(data.text));
            var entry = J.Obj(root, key);
            if (entry == null) return;
            int seed = 0;
            foreach (var o in J.Arr(entry, "items"))
            {
                var it = J.Obj(o);
                var p = new Vector2((float)J.Num(it, "x"), (float)J.Num(it, "y"));
                float s = (float)J.Num(it, "s");
                Add(J.Str(it, "k"), p, s, seed++);
            }
            foreach (var o in J.Arr(entry, "rivers"))
            {
                var rv = J.Obj(o);
                var pts = new List<Vector2>();
                foreach (var q in J.Arr(rv, "pts"))
                {
                    var a = J.Arr(q);
                    pts.Add(new Vector2(Convert.ToSingle(a[0]), Convert.ToSingle(a[1])));
                }
                bool lava = J.Str(rv, "k") == "lava";
                float rw = (float)J.Num(rv, "w", lava ? 0.01 : 0.02);
                fx.Add(new Flow { host = this, path = pts, lava = lava, width = rw, items = NewImages(lava ? "embers" : "ripple", lava ? 7 : 6) });
            }
        }

        void Add(string k, Vector2 p, float s, int seed)
        {
            switch (k)
            {
                case "smoke": fx.Add(new Emitter { host = this, at = p, size = s, kind = k, life = 4f, items = NewImages("smoke_big", 4), alt = SpriteOf("smoke_small"), seed = seed }); break;
                case "flame": fx.Add(new Flame { host = this, at = p, size = s, img = NewImage("flame_a"), a = SpriteOf("flame_a"), b = SpriteOf("flame_b"), seed = seed }); break;
                case "gear": fx.Add(new Spin { host = this, at = p, size = s, img = NewImage("gear_big"), speed = -40 }); break;
                case "gear2": fx.Add(new Spin { host = this, at = p, size = s, img = NewImage("gear_small"), speed = 55 }); break;
                case "bell": fx.Add(new Bell { host = this, at = p, size = s, img = NewImage("bell"), seed = seed }); break;
                case "whirlpool":
                    fx.Add(new Spin { host = this, at = p, size = s, img = NewImage("whirlpool"), speed = -35 });
                    fx.Add(new Bob { host = this, at = p, size = s * 0.42f, img = NewImage("trident") });
                    break;
                case "foam": fx.Add(new Pulse { host = this, at = p, size = s, img = NewImage("foam"), seed = seed }); break;
                case "ripple": fx.Add(new Pulse { host = this, at = p, size = s, img = NewImage("ripple"), seed = seed, slow = true }); break;
                case "sparkle": fx.Add(new Twinkle { host = this, at = p, size = s, img = NewImage("sparkle"), seed = seed }); break;
                case "leaf": fx.Add(new Emitter { host = this, at = p, size = s, kind = k, life = 5f, items = NewImages("leaf", 2), seed = seed }); break;
                case "wind": fx.Add(new Emitter { host = this, at = p, size = s, kind = k, life = 3.2f, items = NewImages("wind", 1), seed = seed }); break;
                case "wave": fx.Add(new Emitter { host = this, at = p, size = s, kind = k, life = 4.5f, items = NewImages("wave", 1), seed = seed }); break;
            }
        }

        static Sprite SpriteOf(string n) => App.Art.Get("anim_" + n);

        Image NewImage(string n)
        {
            var img = Ui.Spawn(itemPrefab, transform);
            img.name = n;
            Theme.SetSprite(img, SpriteOf(n));
            return img;
        }

        Image[] NewImages(string n, int count)
        {
            var arr = new Image[count];
            for (int i = 0; i < count; i++) arr[i] = NewImage(n);
            return arr;
        }

        // toạ độ tỉ lệ (u, v từ trên) -> toạ độ trong lớp (neo góc dưới trái); cỡ tỉ lệ -> đơn vị lớp
        Vector2 P(Vector2 uv) => new Vector2(uv.x * Rt.rect.width, (1 - uv.y) * Rt.rect.height);
        float S(float s) => s * Rt.rect.width;

        static void Place(Image img, Vector2 pos, float w, float alpha = 1, float rot = 0, Vector2? scale = null)
        {
            var rt = img.rectTransform;
            var sp = img.sprite;
            float h = sp ? w * sp.rect.height / sp.rect.width : w;
            rt.sizeDelta = new Vector2(w, h);
            rt.anchoredPosition = pos;
            rt.localEulerAngles = new Vector3(0, 0, rot);
            rt.localScale = scale ?? Vector3.one;
            var c = img.color;
            c.a = Mathf.Clamp01(alpha);
            img.color = c;
        }

        void Update()
        {
            if (fx.Count == 0) return;
            // tắt nét rung (cài đặt hoặc chụp ảnh tĩnh): đứng yên
            if (Shader.GetGlobalFloat("_PokiBoil") > 0.5f) clock += Mathf.Min(Time.unscaledDeltaTime, 0.1f);
            foreach (var f in fx) f.Tick(clock);
        }

        static float Hash(int seed, int i) => Mathf.Repeat(Mathf.Sin(seed * 12.9898f + i * 78.233f) * 43758.547f, 1f);

        // ---------- các kiểu chuyển động ----------

        sealed class Spin : Fx
        {
            public Vector2 at;
            public float size, speed;
            public Image img;
            public override void Tick(float t) => Place(img, host.P(at), host.S(size), 1, t * speed);
        }

        // đinh ba giữa xoáy: nhấp nhô, nghiêng nhẹ
        sealed class Bob : Fx
        {
            public Vector2 at;
            public float size;
            public Image img;
            public override void Tick(float t)
            {
                float w = host.S(size);
                Place(img, host.P(at) + new Vector2(0, w * 0.35f + Mathf.Sin(t * 2.2f) * w * 0.08f), w, 1, Mathf.Sin(t * 1.3f) * 5);
            }
        }

        // chuông: lắc quanh móc treo 1,6 s rồi nghỉ, chu kỳ 4 s
        sealed class Bell : Fx
        {
            public Vector2 at;
            public float size;
            public int seed;
            public Image img;
            public override void Tick(float t)
            {
                img.rectTransform.pivot = new Vector2(0.5f, 1f);
                float w = host.S(size);
                float ph = Mathf.Repeat(t + seed * 1.7f, 4f);
                float ang = ph < 1.6f ? Mathf.Sin(ph * Mathf.PI * 2 / 0.55f) * 16 * Mathf.Sin(ph / 1.6f * Mathf.PI) : 0;
                var sp = img.sprite;
                float h = sp ? w * sp.rect.height / sp.rect.width : w;
                Place(img, host.P(at) + new Vector2(0, h * 0.5f), w, 1, ang);
            }
        }

        // lửa: lật giữa hai hình, phồng nhẹ
        sealed class Flame : Fx
        {
            public Vector2 at;
            public float size;
            public int seed;
            public Image img;
            public Sprite a, b;
            public override void Tick(float t)
            {
                int k = Mathf.FloorToInt(t / 0.16f + seed);
                img.sprite = (k & 1) == 0 ? a : b;
                img.rectTransform.pivot = new Vector2(0.5f, 0.15f);
                float sy = 1 + Mathf.Sin(t * 9 + seed) * 0.08f;
                Place(img, host.P(at), host.S(size), 1, 0, new Vector3(1, sy, 1));
            }
        }

        // bọt, gợn nước tại chỗ: phập phồng
        sealed class Pulse : Fx
        {
            public Vector2 at;
            public float size;
            public int seed;
            public bool slow;
            public Image img;
            public override void Tick(float t)
            {
                float ph = Mathf.Sin(t * (slow ? 2.2f : 4f) + seed);
                float k = 1 + ph * (slow ? 0.12f : 0.08f);
                Place(img, host.P(at), host.S(size), slow ? 0.55f + 0.35f * ph : 0.8f + 0.2f * ph, 0, new Vector3(k, k, 1));
            }
        }

        // lấp lánh: hiện, xoay, tắt; mỗi lần hiện lệch chỗ một chút
        sealed class Twinkle : Fx
        {
            public Vector2 at;
            public float size;
            public int seed;
            public Image img;
            public override void Tick(float t)
            {
                float period = 2.2f + Hash(seed, 0);
                float tt = t + Hash(seed, 1) * period;
                int n = Mathf.FloorToInt(tt / period);
                float ph = Mathf.Repeat(tt, period);
                float k = ph < 0.7f ? Mathf.Sin(ph / 0.7f * Mathf.PI) : 0;
                float w = host.S(size);
                var off = new Vector2(Hash(seed, n) - 0.5f, Hash(seed, n + 99) - 0.5f) * w * 0.8f;
                Place(img, host.P(at) + off, w, k, ph * 120, new Vector3(k, k, 1));
            }
        }

        // khói, lá, gió, sóng: hạt sinh lần lượt, sống life giây
        sealed class Emitter : Fx
        {
            public Vector2 at;
            public float size, life;
            public string kind;
            public int seed;
            public Image[] items;
            public Sprite alt;
            public override void Tick(float t)
            {
                float w = host.S(size);
                for (int i = 0; i < items.Length; i++)
                {
                    float age = Mathf.Repeat(t + (float)i / items.Length * life + Hash(seed, i) * 0.3f, life);
                    float k = age / life;
                    int gen = Mathf.FloorToInt((t + (float)i / items.Length * life) / life);
                    var img = items[i];
                    var p0 = host.P(at);
                    switch (kind)
                    {
                        case "smoke":
                            if (alt) img.sprite = (gen + i) % 2 == 0 ? alt : SpriteOf("smoke_big");
                            float sc = 0.45f + k * 1.1f;
                            float al = k < 0.2f ? k / 0.2f : 1 - (k - 0.2f) / 0.8f;
                            Place(img, p0 + new Vector2(Mathf.Sin(age * 1.4f + i) * w * 0.18f + k * w * 0.3f, k * w * 2.2f), w * sc, al * 0.9f);
                            break;
                        case "leaf":
                            var start = new Vector2(Hash(seed, gen * 7 + i) - 0.5f, Hash(seed, gen * 13 + i) - 0.5f) * w * 3;
                            Place(img, p0 + start + new Vector2(Mathf.Sin(age * 2.4f + i) * w * 0.6f, -age * w * 0.9f), w,
                                k > 0.7f ? (1 - k) / 0.3f : Mathf.Min(1, k * 6), Mathf.Sin(age * 2.4f + i) * 45);
                            break;
                        case "wind":
                            Place(img, p0 + new Vector2((k - 0.5f) * w * 1.2f, Mathf.Sin(age * 3) * w * 0.08f), w, Mathf.Sin(k * Mathf.PI) * 0.9f);
                            break;
                        case "wave":
                            var drift = new Vector2(Hash(seed, gen) - 0.5f, Hash(seed, gen + 5) - 0.5f) * w * 1.5f;
                            float wx = 0.8f + 0.2f * Mathf.Sin(k * Mathf.PI);
                            Place(img, p0 + drift + new Vector2(k * w * 0.5f, 0), w, Mathf.Sin(k * Mathf.PI) * 0.85f, 0, new Vector3(wx, wx, 1));
                            break;
                    }
                }
            }
        }

        // dòng chảy: hạt chạy dọc đường từ đầu tới cuối, mờ ở hai đầu; dung nham nhấp nháy, chậm hơn
        sealed class Flow : Fx
        {
            public List<Vector2> path;
            public bool lava;
            public float width; // bề rộng dòng, tỉ lệ theo bề ngang ảnh
            public Image[] items;
            float[] cum;

            public override void Tick(float t)
            {
                if (path.Count < 2) return;
                var pts = new Vector2[path.Count];
                for (int i = 0; i < pts.Length; i++) pts[i] = host.P(path[i]);
                if (cum == null || cum.Length != pts.Length) cum = new float[pts.Length];
                cum[0] = 0;
                for (int i = 1; i < pts.Length; i++) cum[i] = cum[i - 1] + Vector2.Distance(pts[i - 1], pts[i]);
                float len = cum[pts.Length - 1];
                if (len < 1) return;
                // dung nham: json chỉ đo lõi vàng sáng nên nhân rộng; gợn nước dài bằng bề rộng suối
                float w = host.Rt.rect.width * Mathf.Max(0.006f, width) * (lava ? 2.4f : 1.1f);
                float period = len / (host.Rt.rect.width * (lava ? 0.035f : 0.075f)); // tốc độ chảy theo bề ngang ảnh mỗi giây
                for (int i = 0; i < items.Length; i++)
                {
                    float u = Mathf.Repeat(t / period + (float)i / items.Length, 1f);
                    float d = u * len;
                    int j = 1;
                    while (j < pts.Length - 1 && cum[j] < d) j++;
                    float seg = Mathf.Max(0.001f, cum[j] - cum[j - 1]);
                    var pos = Vector2.Lerp(pts[j - 1], pts[j], (d - cum[j - 1]) / seg);
                    var dir = pts[j] - pts[j - 1];
                    float alpha = Mathf.Sin(u * Mathf.PI);
                    if (lava) alpha *= 0.7f + 0.3f * Mathf.Sin(t * 11 + i * 2.3f);
                    float rot = lava ? 0 : Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg; // nét gợn nằm dọc theo dòng
                    Place(items[i], pos, w, lava ? alpha : alpha * 0.85f, rot);
                }
            }
        }
    }
}
