// Phần động của sàn đấu: đọc Resources/arena_fx.json (ArtGen/BattleBG/build_thuy.py --xuat ghi; mỗi nền một danh sách món, toạ độ
// 0..1 theo khung sân, y từ trên, cỡ theo bề ngang khung) và sprite BattleBG/Anim/san_<tên>, Islands/Anim/anim_<tên>. Lớp "PhanDong"
// nằm ngay trên ảnh nền, dưới tướng, trong prefab Screens/Battle (menu "PokiClash/Prefab/Sàn đấu: lớp phần động"); StageView gọi
// Bind(khoá nền) mỗi lần đổi nền (boss tiến hóa đổi sang nền dạng sau). Mỗi hình sinh từ prefab mục Items/HinhDong.
// Món: lấp lánh, bọt, bụi nước, sóng, gợn tròn, quầng sáng, tia đèn hải đăng, mưa, nước thác, sương, cầu vồng, bong bóng, đom đóm,
// vệt trăng, vòng phù văn, đốm hồn, lá rơi, xoáy nước, đinh ba, sét (nền loé theo), mây bão, vòi rồng. Nền dùng chung (đảo Mộc): khoá có
// "use" mượn ảnh nền khác, "tint" phủ màu ảnh nền (StageView). "img" trong json đổi ảnh của
// món (boss 70 dùng xoáy, đinh ba, sóng cỡ lớn san_*). Flare(): quầng sáng, phù văn, tia đèn bừng lên, xoáy quay nhanh
// (khi tướng dùng chiêu, Tuyệt kỹ). Chụp ảnh tĩnh thì đứng yên như IslandAnim.
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ArenaAnim : MonoBehaviour
    {
        abstract class Fx
        {
            public ArenaAnim host;
            public Vector2 at; // 0..1 theo khung, y từ trên
            public float size, w, h; // cỡ theo bề ngang khung; vùng rải (w theo bề ngang, h theo bề cao)
            public int seed;
            public abstract void Tick(float t);
        }

        [SerializeField] Image itemPrefab; // Items/HinhDong: Image không nhận chạm

        static Dictionary<string, object> arenas;
        readonly List<Fx> fx = new List<Fx>();

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)] // Play không reload domain
        static void ResetCache() => arenas = null;
        float clock, flare;

        RectTransform Rt => (RectTransform)transform;
        float Wd => Rt.rect.width;
        float Ht => Rt.rect.height;

        static Dictionary<string, object> Entry(string key)
        {
            if (arenas == null)
            {
                var ta = Resources.Load<TextAsset>("arena_fx");
                arenas = ta ? J.Obj(J.Obj(MiniJson.Parse(ta.text)), "arenas") ?? new Dictionary<string, object>()
                    : new Dictionary<string, object>();
            }
            return J.Obj(arenas, key);
        }

        // màu trời phủ phần dôi trên đầu máy dài; null khi nền không có trong json
        public static string Sky(string key) => J.Str(Entry(key), "sky");

        // nền dùng chung (đảo Mộc, build_moc.py --xuat): khoá mượn ảnh của khoá khác ("use") và phủ màu lên ảnh nền ("tint")
        public static string Use(string key) => J.Str(Entry(key), "use");
        public static string Tint(string key) => J.Str(Entry(key), "tint");

        // Dùng khi dựng prefab (Editor).
        public void Setup(Image item) => itemPrefab = item;

        public void Bind(string key)
        {
            foreach (Transform c in transform) Destroy(c.gameObject);
            fx.Clear();
            if (!itemPrefab) return;
            clock = flare = 0;
            int seed = 0;
            foreach (var o in J.Arr(Entry(key), "fx"))
            {
                var it = J.Obj(o);
                Fx f = Make(J.Str(it, "k"), it);
                if (f == null) continue;
                f.host = this;
                f.at = new Vector2((float)J.Num(it, "x"), (float)J.Num(it, "y"));
                f.size = (float)J.Num(it, "s");
                f.w = (float)J.Num(it, "w");
                f.h = (float)J.Num(it, "h");
                f.seed = seed++;
                fx.Add(f);
            }
        }

        public void Flare() => flare = 1;

        Fx Make(string k, Dictionary<string, object> it)
        {
            int n = J.Int(it, "n", 1);
            string img = J.Str(it, "img");
            switch (k)
            {
                case "sparkle": return new Twinkle { items = Images("anim_sparkle", n) };
                case "foam": return new Pulse { img = Images("anim_foam", 1)[0] };
                case "spray": return new Spray { img = Images("anim_foam", 1)[0] };
                case "wave": return new Drift { items = Images(img ?? "anim_wave", n) };
                case "ripple": return new Ripple { items = Images("san_ripple", n) };
                case "glow": return new Glow { img = Images(img ?? "san_glow", 1, J.Str(it, "c"))[0] };
                case "beam": return new Beam { img = Images("san_beam", 1)[0], angle = (float)J.Num(it, "a"), thin = (float)J.Num(it, "q", 0.4) };
                case "rain": return new Rain { items = Images(null, n, "#e8f0ff") };
                case "fall": return new Fall { items = Images("san_fall", 3), top = (float)J.Num(it, "t"), bottom = (float)J.Num(it, "b", 1) };
                case "mist": return new Mist { items = Images(img ?? "san_mist", n) };
                case "rainbow": return new Rainbow { img = Images("san_rainbow", 1)[0] };
                case "bubbles": return new Bubbles { items = Images("san_bubble", n), many = Sprite("san_bubbles") };
                case "firefly": return new Firefly { items = Images("san_firefly", n) };
                case "shimmer": return new Shimmer { img = Images("san_moonlight", 1)[0] };
                case "rune": return new Rune { img = Images(img ?? "san_rune", 1)[0] };
                case "wisp": return new Wisp { items = Images(img ?? "san_wisp", n) };
                case "leaf": return new Leaf { items = Images(img ?? "anim_leaf", J.Int(it, "n", 2)) };
                case "whirlpool": return MakeWhirl((float)J.Num(it, "q", 0.2), (float)J.Num(it, "v", 1), img ?? "anim_whirlpool");
                case "trident": return new Trident { img = Images(img ?? "anim_trident", 1)[0] };
                case "bolt": return new Bolt { flash = Images(null, 1, "#e6e0ff")[0], img = Images(img ?? "san_bolt", 1)[0] };
                case "cloud": return new Cloud { items = Images(img ?? "san_cloud", n) };
                case "spout": return new Spout { items = Images(img ?? "san_spout", n) };
            }
            return null;
        }

        static Sprite Sprite(string name) => App.Art && App.Art.HasArt(name) ? App.Art.Get(name) : null;

        Image NewImage(string sprite, Transform parent)
        {
            var img = Ui.Spawn(itemPrefab, parent);
            img.name = sprite ?? "vet";
            img.preserveAspect = false; // cỡ tính ở Place (tia đèn ép dẹt, vệt mưa không có ảnh)
            var rt = img.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            Theme.SetSprite(img, sprite == null ? null : Sprite(sprite));
            if (sprite != null && !img.sprite) img.gameObject.SetActive(false); // thiếu ảnh: bỏ món, không hiện ô trắng
            return img;
        }

        Image[] Images(string sprite, int count, string hex = null)
        {
            var arr = new Image[Mathf.Max(1, count)];
            for (int i = 0; i < arr.Length; i++)
            {
                arr[i] = NewImage(sprite, transform);
                if (hex != null) arr[i].color = Theme.Hex(hex);
            }
            return arr;
        }

        // xoáy dẹt: khung cha (một mục ẩn ảnh) ép bề cao, ảnh con xoay
        Fx MakeWhirl(float squash, float speed, string sprite)
        {
            var holder = NewImage(null, transform);
            holder.name = "xoay";
            holder.enabled = false;
            var hr = holder.rectTransform;
            hr.sizeDelta = Vector2.zero;
            hr.localScale = new Vector3(1, squash, 1);
            return new Whirl { holder = hr, img = NewImage(sprite, hr), speed = speed };
        }

        // toạ độ 0..1 (y từ trên) -> anchoredPosition neo góc trên trái
        Vector2 P(Vector2 uv) => new Vector2(uv.x * Wd, -uv.y * Ht);
        Vector2 P(float u, float v) => P(new Vector2(u, v));
        float S(float s) => s * Wd;

        static void Place(Image img, Vector2 pos, float w, float alpha, float rot = 0, Vector3? scale = null, float hOverride = 0)
        {
            var rt = img.rectTransform;
            var sp = img.sprite;
            float h = hOverride > 0 ? hOverride : sp ? w * sp.rect.height / sp.rect.width : w;
            rt.sizeDelta = new Vector2(w, h);
            rt.anchoredPosition = pos;
            rt.localEulerAngles = new Vector3(0, 0, rot);
            rt.localScale = scale ?? Vector3.one;
            var c = img.color;
            c.a = Mathf.Clamp01(alpha);
            img.color = c;
        }

        static float Hash(int seed, int i) => Mathf.Repeat(Mathf.Sin(seed * 12.9898f + i * 78.233f) * 43758.547f, 1f);

        // điểm ngẫu nhiên trong vùng rải của món, đổi mỗi lượt sinh (gen)
        Vector2 Spot(Fx f, int i, int gen) =>
            P(f.at.x + (Hash(f.seed * 31 + i, gen) - 0.5f) * f.w, f.at.y + (Hash(f.seed * 17 + i, gen + 7) - 0.5f) * f.h);

        void Update()
        {
            if (fx.Count == 0) return;
            if (Shader.GetGlobalFloat("_PokiBoil") > 0.5f) clock += Mathf.Min(Time.unscaledDeltaTime, 0.1f);
            flare = Mathf.Max(0, flare - Time.unscaledDeltaTime * 1.4f);
            foreach (var f in fx) f.Tick(clock);
        }

        // ---------- các kiểu chuyển động ----------

        // lấp lánh: hiện, xoay, tắt; mỗi lần hiện một chỗ khác trong vùng
        sealed class Twinkle : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                for (int i = 0; i < items.Length; i++)
                {
                    float period = 2.4f + Hash(seed, i);
                    float tt = t + Hash(seed, i + 3) * period;
                    int gen = Mathf.FloorToInt(tt / period);
                    float ph = Mathf.Repeat(tt, period);
                    float k = ph < 0.7f ? Mathf.Sin(ph / 0.7f * Mathf.PI) : 0;
                    Place(items[i], host.Spot(this, i, gen), host.S(size), k, ph * 120, new Vector3(k, k, 1));
                }
            }
        }

        // bọt mép nước: phập phồng tại chỗ
        sealed class Pulse : Fx
        {
            public Image img;
            public override void Tick(float t)
            {
                float ph = Mathf.Sin(t * 3.2f + seed * 1.7f);
                float k = 1 + ph * 0.1f;
                Place(img, host.P(at), host.S(size), 0.75f + 0.25f * ph, 0, new Vector3(k, k, 1));
            }
        }

        // sóng vỗ đá: bọt bắn lên, nở, tan; nghỉ rồi bắn lại
        sealed class Spray : Fx
        {
            public Image img;
            public override void Tick(float t)
            {
                float period = 2.6f + Hash(seed, 1) * 1.2f;
                float ph = Mathf.Repeat(t + Hash(seed, 2) * period, period);
                float k = Mathf.Clamp01(ph / 0.9f);
                img.rectTransform.pivot = new Vector2(0.5f, 0.1f);
                float sc = 0.4f + k * 0.85f;
                Place(img, host.P(at), host.S(size), ph < 0.9f ? 1 - k * k : 0, 0, new Vector3(sc, sc, 1));
            }
        }

        // sóng ngoài biển: nổi lên, trôi ngang, mờ
        sealed class Drift : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                const float life = 4.5f;
                for (int i = 0; i < items.Length; i++)
                {
                    float tt = t + (float)i / items.Length * life + Hash(seed, i) * 0.5f;
                    int gen = Mathf.FloorToInt(tt / life);
                    float k = Mathf.Repeat(tt, life) / life;
                    float wx = 0.8f + 0.2f * Mathf.Sin(k * Mathf.PI);
                    float w = host.S(size);
                    Place(items[i], host.Spot(this, i, gen) + new Vector2(k * w * 0.5f, 0), w, Mathf.Sin(k * Mathf.PI) * 0.85f, 0,
                        new Vector3(wx, wx, 1));
                }
            }
        }

        // gợn tròn: loang rộng, mờ dần, lần sau một chỗ khác trong vùng
        sealed class Ripple : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                const float life = 3f;
                for (int i = 0; i < items.Length; i++)
                {
                    float tt = t + (float)i / items.Length * life + Hash(seed, i) * life;
                    int gen = Mathf.FloorToInt(tt / life);
                    float k = Mathf.Repeat(tt, life) / life;
                    float sc = 0.35f + k * 0.9f;
                    Place(items[i], host.Spot(this, i, gen), host.S(size), (1 - k) * 0.8f, 0, new Vector3(sc, sc, 1));
                }
            }
        }

        // quầng sáng (ngọc, trăng, cửa đền, đèn): phập phồng; bừng lên theo chiêu
        sealed class Glow : Fx
        {
            public Image img;
            public override void Tick(float t)
            {
                float ph = Mathf.Sin(t * 1.6f + seed);
                float fl = host.flare;
                float k = 1 + ph * 0.06f + fl * 0.25f;
                Place(img, host.P(at), host.S(size), 0.45f + ph * 0.15f + fl * 0.4f, 0, new Vector3(k, k, 1));
            }
        }

        // tia đèn hải đăng: đèn quay tròn nên nhìn ngang thấy tia quét sang phải, ngắn lại, sang trái
        sealed class Beam : Fx
        {
            public Image img;
            public float angle, thin;
            public override void Tick(float t)
            {
                float c = Mathf.Cos(t * 0.9f + seed);
                float w = host.S(size);
                var sp = img.sprite;
                float h = (sp ? w * sp.rect.height / sp.rect.width : w * 0.4f) * thin;
                img.rectTransform.pivot = new Vector2(0.03f, 0.5f);
                Place(img, host.P(at), w, Mathf.Abs(c) * (0.5f + host.flare * 0.4f), c >= 0 ? angle : -angle,
                    new Vector3(c, 1, 1), h);
            }
        }

        // mưa: vệt xiên rơi khắp khung, rơi hết thì quay lại trên đầu
        sealed class Rain : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                float len = host.S(size);
                for (int i = 0; i < items.Length; i++)
                {
                    float u = Hash(seed, i), sp = 0.9f + Hash(seed, i + 50) * 0.4f;
                    float k = Mathf.Repeat(t * sp + Hash(seed, i + 9), 1f);
                    var pos = new Vector2((u + 0.18f * (1 - k)) % 1.1f * host.Wd, -(k * 1.15f - 0.08f) * host.Ht);
                    Place(items[i], pos, 3, 0.35f, -12, null, len);
                }
            }
        }

        // nước thác: vệt trắng trượt từ đỉnh xuống chân thác, mờ ở hai đầu
        sealed class Fall : Fx
        {
            public Image[] items;
            public float top, bottom;
            public override void Tick(float t)
            {
                float w = host.S(size);
                for (int i = 0; i < items.Length; i++)
                {
                    float k = Mathf.Repeat(t / 1.4f + (float)i / items.Length, 1f);
                    float y = Mathf.Lerp(top, bottom, k);
                    Place(items[i], host.P(at.x, y), w, Mathf.Sin(k * Mathf.PI) * 0.7f);
                }
            }
        }

        // sương chân thác: cụm sương trôi ngang trong vùng, nở, mờ
        sealed class Mist : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                const float life = 6f;
                for (int i = 0; i < items.Length; i++)
                {
                    float tt = t + (float)i / items.Length * life;
                    int gen = Mathf.FloorToInt(tt / life);
                    float k = Mathf.Repeat(tt, life) / life;
                    float sc = 0.8f + 0.3f * k;
                    var p = host.Spot(this, i, gen) + new Vector2((k - 0.5f) * host.S(size), 0);
                    Place(items[i], p, host.S(size), Mathf.Sin(k * Mathf.PI) * 0.55f, 0, new Vector3(sc, sc, 1));
                }
            }
        }

        // cầu vồng: hiện dần, đứng, tắt dần, nghỉ (chu kỳ 14 s)
        sealed class Rainbow : Fx
        {
            public Image img;
            public override void Tick(float t)
            {
                float ph = Mathf.Repeat(t + 2, 14f);
                float a = ph < 3 ? ph / 3 : ph < 8 ? 1 : ph < 11 ? (11 - ph) / 3 : 0;
                Place(img, host.P(at), host.S(size), a * 0.55f);
            }
        }

        // bong bóng: nổi lên từ mặt nước, lắc nhẹ, vỡ
        sealed class Bubbles : Fx
        {
            public Image[] items;
            public Sprite many;
            public override void Tick(float t)
            {
                const float life = 3.2f;
                for (int i = 0; i < items.Length; i++)
                {
                    float tt = t + (float)i / items.Length * life;
                    int gen = Mathf.FloorToInt(tt / life);
                    float k = Mathf.Repeat(tt, life) / life;
                    if (many && i % 3 == 2) items[i].sprite = many;
                    float w = host.S(size) * (items[i].sprite == many ? 2.2f : 0.7f + Hash(seed, i + gen) * 0.5f);
                    var p = host.Spot(this, i, gen) + new Vector2(Mathf.Sin(k * 9 + i) * w * 0.3f, k * host.Ht * Mathf.Max(0.05f, h) * 0.6f);
                    Place(items[i], p, w, (k < 0.15f ? k / 0.15f : 1 - (k - 0.15f) / 0.85f) * 0.85f);
                }
            }
        }

        // đom đóm: lượn chậm trong vùng, chớp tắt
        sealed class Firefly : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                for (int i = 0; i < items.Length; i++)
                {
                    float sx = 0.31f + Hash(seed, i) * 0.2f, sy = 0.47f + Hash(seed, i + 5) * 0.2f;
                    var p = host.P(at.x + Mathf.Sin(t * sx + i * 2.1f) * w * 0.5f, at.y + Mathf.Sin(t * sy + i * 1.3f) * h * 0.5f);
                    float a = 0.25f + 0.75f * Mathf.Max(0, Mathf.Sin(t * 1.9f + i * 2.4f));
                    Place(items[i], p, host.S(size), a);
                }
            }
        }

        // vệt trăng trên nước: lung linh
        sealed class Shimmer : Fx
        {
            public Image img;
            public override void Tick(float t)
            {
                float ph = Mathf.Sin(t * 3 + seed * 1.9f);
                Place(img, host.P(at), host.S(size), 0.45f + 0.3f * ph, 0, new Vector3(1 + 0.12f * Mathf.Sin(t * 2.3f + seed), 1, 1));
            }
        }

        // vòng phù văn trên bệ boss: phập phồng, bừng lên theo chiêu
        sealed class Rune : Fx
        {
            public Image img;
            public override void Tick(float t)
            {
                float ph = Mathf.Sin(t * 1.4f);
                float k = 1 + 0.03f * ph + host.flare * 0.08f;
                Place(img, host.P(at), host.S(size), 0.4f + 0.2f * ph + host.flare * 0.5f, 0, new Vector3(k, k, 1));
            }
        }

        // đốm hồn: bay lên, lắc, mờ
        sealed class Wisp : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                const float life = 4f;
                for (int i = 0; i < items.Length; i++)
                {
                    float tt = t + (float)i / items.Length * life;
                    int gen = Mathf.FloorToInt(tt / life);
                    float k = Mathf.Repeat(tt, life) / life;
                    float w = host.S(size);
                    var p = host.Spot(this, i, gen) + new Vector2(Mathf.Sin(k * 6 + i) * w * 0.4f, k * w * 3);
                    float sc = 0.7f + 0.3f * k;
                    Place(items[i], p, w, Mathf.Sin(k * Mathf.PI) * 0.8f, 0, new Vector3(sc, sc, 1));
                }
            }
        }

        // lá rơi từ tán cây: chao qua lại
        sealed class Leaf : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                const float life = 5f;
                float w = host.S(size);
                for (int i = 0; i < items.Length; i++)
                {
                    float tt = t + (float)i / items.Length * life;
                    int gen = Mathf.FloorToInt(tt / life);
                    float age = Mathf.Repeat(tt, life), k = age / life;
                    var start = new Vector2(Hash(seed, gen * 7 + i) - 0.5f, Hash(seed, gen * 13 + i) - 0.5f) * w * 3;
                    Place(items[i], host.P(at) + start + new Vector2(Mathf.Sin(age * 2.4f + i) * w * 0.6f, -age * w * 1.1f), w,
                        k > 0.7f ? (1 - k) / 0.3f : Mathf.Min(1, k * 6), Mathf.Sin(age * 2.4f + i) * 45);
                }
            }
        }

        // xoáy nước dẹt theo mặt hồ, quay (speed: nhân tốc độ, boss dạng sau quay nhanh hơn); chiêu làm quay nhanh
        sealed class Whirl : Fx
        {
            public RectTransform holder;
            public Image img;
            public float speed = 1;
            float ang;
            public override void Tick(float t)
            {
                holder.anchoredPosition = host.P(at);
                ang -= (35 * speed + host.flare * 160) * Mathf.Min(Time.unscaledDeltaTime, 0.1f) * (Shader.GetGlobalFloat("_PokiBoil") > 0.5f ? 1 : 0);
                float w = host.S(size);
                Place(img, Vector2.zero, w, 0.9f, ang, null, w);
            }
        }

        // sét: đánh xuống một chỗ trong vùng mỗi 3,5–6 s, nháy hai lần; cả lớp nền loé sáng theo (dưới tướng)
        sealed class Bolt : Fx
        {
            public Image img, flash;
            public override void Tick(float t)
            {
                float period = 3.5f + Hash(seed, 1) * 2.5f;
                float tt = t + Hash(seed, 2) * period;
                int gen = Mathf.FloorToInt(tt / period);
                float ph = Mathf.Repeat(tt, period);
                float a = ph < 0.08f ? 1 : ph < 0.14f ? 0.25f : ph < 0.3f ? 1 - (ph - 0.14f) / 0.16f : 0;
                img.rectTransform.pivot = new Vector2(0.5f, 1); // đầu sét ở trên
                Place(img, host.Spot(this, 0, gen), host.S(size), a, (Hash(seed, gen + 3) - 0.5f) * 16);
                Place(flash, new Vector2(host.Wd / 2, -host.Ht / 2), host.Wd, a * 0.22f, 0, null, host.Ht);
            }
        }

        // mây bão trôi ngang qua vùng trời, chậm; mỗi đám một cỡ, một độ cao
        sealed class Cloud : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                const float life = 22f;
                for (int i = 0; i < items.Length; i++)
                {
                    float tt = t + (float)i / items.Length * life + Hash(seed, i) * 3;
                    int gen = Mathf.FloorToInt(tt / life);
                    float k = Mathf.Repeat(tt, life) / life;
                    float x = at.x - w / 2 - 0.2f + k * (w + 0.4f), y = at.y + (Hash(seed, i * 7 + gen) - 0.5f) * h;
                    float sc = 0.8f + 0.4f * Hash(seed, i + 11);
                    Place(items[i], host.P(x, y), host.S(size) * sc, Mathf.Min(1, Mathf.Sin(k * Mathf.PI) * 3) * 0.9f);
                }
            }
        }

        // vòi rồng ở chân trời: mọc lên từ mặt biển, lắc, tan; lần sau một chỗ khác trong vùng
        sealed class Spout : Fx
        {
            public Image[] items;
            public override void Tick(float t)
            {
                const float life = 7f;
                for (int i = 0; i < items.Length; i++)
                {
                    float tt = t + (float)i / items.Length * life + Hash(seed, i) * life;
                    int gen = Mathf.FloorToInt(tt / life);
                    float k = Mathf.Repeat(tt, life) / life;
                    float grow = Mathf.SmoothStep(0, 1, Mathf.Clamp01(k / 0.25f)), fade = k > 0.75f ? (1 - k) / 0.25f : 1;
                    items[i].rectTransform.pivot = new Vector2(0.5f, 0);
                    Place(items[i], host.Spot(this, i, gen), host.S(size), fade * 0.95f, Mathf.Sin(t * 1.7f + i) * 6,
                        new Vector3(1, grow, 1));
                }
            }
        }

        // đinh ba nổi giữa xoáy (at là chân đinh ba): nhấp nhô, nghiêng nhẹ
        sealed class Trident : Fx
        {
            public Image img;
            public override void Tick(float t)
            {
                img.rectTransform.pivot = new Vector2(0.5f, 0);
                float w = host.S(size);
                Place(img, host.P(at) + new Vector2(0, Mathf.Sin(t * 2.2f) * w * 0.12f), w, 1, Mathf.Sin(t * 1.3f) * 4);
            }
        }
    }
}
