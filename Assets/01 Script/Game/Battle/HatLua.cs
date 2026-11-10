// Hạt chồng lớp phẳng trên sân đấu (bộ Hỏa 2026-11-10; chuyển từ ArtGen/Spine/fxlib.py + bo_hoa.py, sổ công thức ở skill
// pokiclash-fx-congthuc). Mỗi hạt mỗi khung trả các "nét vẽ" (nhóm Đất / Sau tướng / Trước tướng, lớp, ảnh, màu, vị trí, cỡ, góc,
// alpha); gom lại, xếp theo (nhóm, lớp) rồi gán lần lượt cho các Image trong hàng chờ của nhóm đó (thứ tự anh em = thứ tự vẽ).
// Ảnh hạt xám vân chì (Assets/03 Art/Fx/Hat, ArtGen/Spine/xuat_hat.py) nhuộm bằng Image.color; không glow, không cộng sáng.
// Toạ độ theo khung sân web (540 x 464, y xuống) như StageView, đổi ra UI bằng StageView.P; thời gian là giây sân.
// Không tạo GameObject lúc chạy (PrefabOnlyTests): Image sinh bằng Ui.Spawn từ prefab Items/HatLua, giữ trong hàng chờ.
using System;
using System.Collections.Generic;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public const int Floor = 0, Back = 1, Front = 2;

        // ---------- hạt ----------
        public sealed class P
        {
            public Vector2 pos, vel, acc;
            public float age, life = 1, drag, ang, spin, spinDrag, r0, r1, heat = 1, sz, ph, vy, R0, R1, hgt, launch;
            public int seed, group = Front, smokeGroup = -1, span;
            public string style = "tron", pal = "lua";
            public Color col = Color.white;
            public Action<P, float, HatLua> upd;
            public Action<P, HatLua> onDeath, onGround;
            public Action<P, float, List<Item>> draw;
            public Func<P, float, float> sizeFn;
            public float ground = float.NaN, bounce, stretchK = 1100;
            public bool bounced, dead, hit, fly, crust;
            public float tip = -1, tipUp = 0.5f; // lưỡi lửa "luoi": ngọn theo hướng bay (+1) hay ngả ngược lại (-1), và phần ngả lên
            public Vector2 aim, home, off, drift;
            public System.Random rng;
            public Color[] stops; // dải màu khói theo chủ đề lúc sinh (hạt nước: bảng màu nước lúc sinh)
            public float fade = 0.72f, wd, tb; // hạt nước (HatNuoc.cs): lúc bắt đầu co, bề rộng, giờ sinh
            public bool big;
            public Action<P, HatLua> onPop;
        }

        public struct Item
        {
            public int group;
            public float layer, w, h, ang, alpha;
            public Sprite sprite;
            public Color color;
            public Vector2 pos;
            public int fill; // 0 thường; 1 nửa trên (Vertical, gốc trên); 2 nửa dưới
        }

        sealed class Stream
        {
            public float t0, t1, acc;
            public Func<float, float> rate;
            public Action<float> fn;
        }

        // ---------- chủ đề theo tướng (người dùng 2026-11-10: hiệu ứng hợp hình từng tướng) ----------
        public sealed class Theme
        {
            public string pal = "lua"; // bảng màu lửa (Pal)
            public Color spark = C(250, 210, 90), ember = C(244, 170, 56), ring = C(248, 178, 64), ring2 = C(252, 236, 180);
            public Color[] smoke; // null = khói đen thường (SmokeDark); không gán mặc định ở đây: biến tĩnh SmokeDark khởi tạo sau bảng Themes
            public string extra; // họa tiết thêm: tinh_the, canh_sen, may, sao, giap
            public Color extraCol = Color.white;
        }

        static readonly Theme Default = new Theme();
        static readonly Dictionary<string, Theme> Themes = new Dictionary<string, Theme>
        {
            // sói đỏ, tinh thể đỏ trên giáp: lửa đỏ thẫm, mảnh tinh thể đỏ văng
            { "hoa_tinh", new Theme { pal = "tinh", spark = C(255, 150, 120), ember = C(236, 70, 60), ring = C(232, 70, 60), extra = "tinh_the", extraCol = C(206, 30, 56) } },
            // cáo đuôi tím hồng, trăng khuyết: hồ hỏa tím hồng, khói tím xám, sao lấp lánh
            { "huyen_viem", new Theme { pal = "tim", spark = C(240, 160, 255), ember = C(220, 110, 230), ring = C(214, 110, 220), ring2 = C(250, 214, 250),
                smoke = new[] { C(72, 52, 84), C(122, 104, 134), C(170, 160, 182), C(210, 204, 216) }, extra = "sao", extraCol = C(250, 200, 250) } },
            // lân đỏ vàng kim, mây xoắn
            { "lan_hoa", new Theme { pal = "vang", smoke = new[] { C(92, 66, 50), C(142, 122, 106), C(188, 176, 164), C(216, 210, 202) }, spark = C(255, 222, 110), ember = C(250, 190, 60), ring = C(250, 196, 60), extra = "may", extraCol = C(250, 200, 70) } },
            // sư tử vàng bờm đỏ: lửa vàng kim, sao vàng
            { "kim_su", new Theme { pal = "vang", smoke = new[] { C(92, 66, 50), C(142, 122, 106), C(188, 176, 164), C(216, 210, 202) }, spark = C(255, 230, 120), ember = C(250, 200, 70), ring = C(252, 206, 70), extra = "sao", extraCol = C(255, 224, 100) } },
            // rồng sen hồng: lửa hồng sen, cánh sen bay
            { "hong_lien", new Theme { pal = "sen", spark = C(255, 190, 200), ember = C(240, 120, 150), ring = C(236, 110, 150), ring2 = C(252, 222, 228),
                smoke = new[] { C(84, 52, 62), C(130, 104, 112), C(176, 160, 166), C(212, 204, 206) }, extra = "canh_sen", extraCol = C(244, 120, 160) } },
            // rồng đỏ giáp xám: lửa đỏ, mảnh giáp sắt văng
            { "giap_long", new Theme { extra = "giap", extraCol = C(110, 112, 122) } },
            // bò võ sĩ, mây vàng
            { "nguu_quyen", new Theme { pal = "nguu", smoke = new[] { C(92, 66, 50), C(142, 122, 106), C(188, 176, 164), C(216, 210, 202) }, ring = C(250, 170, 60), extra = "may", extraCol = C(250, 196, 70) } },
            // người đá than / nham: lửa dung nham, đá
            { "khong_lo", new Theme { pal = "nham", spark = C(255, 190, 90), ember = C(240, 120, 40), ring = C(236, 104, 34), extra = "giap", extraCol = C(80, 66, 72) } },
            { "nham_than", new Theme { pal = "nham", spark = C(255, 190, 90), ember = C(240, 120, 40), ring = C(236, 104, 34), extra = "giap", extraCol = C(120, 84, 62) } },
        };

        public Theme Th = Default;

        // đặt chủ đề trước khi phát chiêu (tướng không có trong bảng: lửa thường)
        public void UseTheme(string heroId)
        {
            Th = heroId != null && Themes.TryGetValue(heroId, out var t) ? t : Default;
            UseWater(heroId);
        }

        Color[] FireStops()
        {
            var pc = Pal[Th.pal];
            var sm = Th.smoke ?? SmokeDark;
            return new[] { pc[1], Color.Lerp(pc[0], sm[1], 0.55f), sm[1], sm[2], sm[3] };
        }

        // họa tiết thêm theo chủ đề, văng ra quanh at
        public void Extra(Vector2 at, int n, float speed, int group = Front)
        {
            string kind = Th.extra;
            if (kind == null) return;
            var col = Th.extraCol;
            for (int i = 0; i < n; i++)
            {
                float a = U(0, 6.28f);
                var dir = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f);
                var p = new P { pos = at + U2(-8, 8), seed = rng.Next(4), group = group, col = col, spin = U(-8, 8), ph = U(0, 6.28f) };
                switch (kind)
                {
                    case "tinh_the": // mảnh tinh thể: kim nhỏ đỏ thẫm, văng xa, rơi, xoay
                    case "giap": // mảnh giáp sắt
                        p.vel = dir * U(0.6f, 1.1f) * speed;
                        p.life = U(0.5f, 0.8f);
                        p.acc = new Vector2(0, 900);
                        p.drag = 1.5f;
                        p.sz = U(11, 17);
                        p.draw = (q, k, buf) =>
                        {
                            float s2 = q.sz * (1 - SmoothStep(0.7f, 1, k));
                            Put(buf, q.group, 44, S("needles_0"), Ink, q.pos, s2 + 4, 0.55f, q.ang * Mathf.Rad2Deg);
                            Put(buf, q.group, 44.5f, S("needle_0"), q.col, q.pos, s2, 0.55f, q.ang * Mathf.Rad2Deg);
                        };
                        break;
                    case "canh_sen": // cánh sen: bay ra rồi lượn rơi chậm
                        p.vel = dir * U(0.4f, 0.8f) * speed;
                        p.life = U(1.0f, 1.5f);
                        p.acc = new Vector2(0, 60);
                        p.drag = 2.4f;
                        p.sz = U(12, 17);
                        p.spin = U(-3, 3);
                        p.upd = (q, dt, s3) => q.vel.x += Mathf.Sin(q.age * 4 + q.ph) * 70 * dt;
                        p.draw = (q, k, buf) =>
                        {
                            float s2 = q.sz * (1 - SmoothStep(0.75f, 1, k));
                            Put(buf, q.group, 44, S("hooks_" + (q.seed & 3)), Ink, q.pos, s2 + 4, 1, q.ang * Mathf.Rad2Deg);
                            Put(buf, q.group, 44.5f, S("hook_" + (q.seed & 3)), q.col, q.pos, s2, 1, q.ang * Mathf.Rad2Deg);
                        };
                        break;
                    case "may": // mây xoắn vàng: bay lên chậm, xoay
                        p.vel = dir * U(0.3f, 0.6f) * speed + new Vector2(0, -40);
                        p.life = U(0.8f, 1.2f);
                        p.drag = 2;
                        p.sz = U(18, 26);
                        p.spin = U(-2, 2);
                        p.draw = (q, k, buf) => Put(buf, q.group, 44, S("curl_" + (q.seed % 3)), q.col, q.pos,
                            q.sz * Mathf.Min(1, k / 0.15f) * (1 - SmoothStep(0.7f, 1, k)), 1, q.ang * Mathf.Rad2Deg);
                        break;
                    default: // "sao": sao lấp lánh nhấp nháy
                        p.vel = dir * U(0.3f, 0.7f) * speed;
                        p.life = U(0.6f, 1.0f);
                        p.drag = 2.5f;
                        p.sz = U(9, 14);
                        p.draw = (q, k, buf) => Put(buf, q.group, 44, S("starg_0"), q.col, q.pos,
                            q.sz * Mathf.Min(1, k / 0.12f) * (1 - k * k) * (0.6f + 0.4f * Mathf.Abs(Mathf.Sin(q.age * 14 + q.ph))), 1, q.ang * Mathf.Rad2Deg);
                        break;
                }
                Add(p);
            }
        }

        // ---------- trạng thái ----------
        readonly Image prefab;
        readonly RectTransform[] groups;
        readonly Dictionary<string, Sprite> art = new Dictionary<string, Sprite>();
        readonly List<Image>[] pool = { new List<Image>(), new List<Image>(), new List<Image>() };
        readonly List<P> ps = new List<P>();
        readonly List<P> born = new List<P>();
        readonly List<(float t, Action fn)> events = new List<(float, Action)>();
        readonly List<Stream> streams = new List<Stream>();
        readonly List<Item> items = new List<Item>(1024);
        public float T { get; private set; }
        public readonly System.Random rng = new System.Random(7);
        public Action<float> Shake;
        public Action<Color> FlashScreen;
        public int Live => ps.Count;

        public HatLua(Image prefab, RectTransform floor, RectTransform back, RectTransform front, Sprite[] sprites)
        {
            this.prefab = prefab;
            groups = new[] { floor, back, front };
            for (int g = 0; g < 3; g++)
                if (groups[g]) mang[g] = groups[g].GetComponentInChildren<HatMang>(true);
            if (sprites != null)
                foreach (var s in sprites)
                    if (s) art[s.name] = s;
        }

        public bool Ready => prefab && groups[0] && groups[1] && groups[2] && art.Count > 0;

        Sprite S(string name) => art.TryGetValue("hat_" + name, out var s) ? s : null;

        public float U(float a, float b) => a + (float)rng.NextDouble() * (b - a);
        static float U(System.Random r, float a, float b) => a + (float)r.NextDouble() * (b - a);
        public Vector2 U2(float a, float b) => new Vector2(U(a, b), U(a, b));

        public P Add(P p)
        {
            if (p.rng == null) p.rng = rng;
            born.Add(p);
            return p;
        }

        public void At(float t, Action fn) => events.Add((T + t, fn));

        public void Every(float t0, float t1, float rate, Action<float> fn) => Every(t0, t1, _ => rate, fn);

        public void Every(float t0, float t1, Func<float, float> rate, Action<float> fn) =>
            streams.Add(new Stream { t0 = T + t0, t1 = T + t1, rate = rate, fn = fn });

        public void Clear()
        {
            ps.Clear();
            born.Clear();
            events.Clear();
            streams.Clear();
            for (int g = 0; g < 3; g++)
                foreach (var im in pool[g])
                    if (im) im.enabled = false;
            ClearMang();
        }

        // ---------- cập nhật (giây sân) ----------
        public void Update(float dt)
        {
            if (!Ready) return;
            if (ps.Count == 0 && born.Count == 0 && events.Count == 0 && streams.Count == 0)
            {
                HideFrom(0, 0);
                HideFrom(1, 0);
                HideFrom(2, 0);
                ClearMang();
                return;
            }
            int sub = Mathf.Clamp(Mathf.CeilToInt(dt * 120), 1, 6);
            float h = dt / sub;
            for (int i = 0; i < sub; i++) Step(h);
            Render();
        }

        void Step(float dt)
        {
            for (int i = events.Count - 1; i >= 0; i--)
                if (T >= events[i].t)
                {
                    var fn = events[i].fn;
                    events.RemoveAt(i);
                    fn();
                }
            for (int i = streams.Count - 1; i >= 0; i--)
            {
                var st = streams[i];
                if (T >= st.t1)
                {
                    streams.RemoveAt(i);
                    continue;
                }
                if (T < st.t0) continue;
                float x = (T - st.t0) / Mathf.Max(1e-4f, st.t1 - st.t0);
                st.acc += dt * st.rate(x);
                while (st.acc >= 1)
                {
                    st.acc -= 1;
                    st.fn(x);
                }
            }
            if (born.Count > 0)
            {
                ps.AddRange(born);
                born.Clear();
            }
            for (int i = ps.Count - 1; i >= 0; i--)
            {
                var p = ps[i];
                p.age += dt;
                if (p.age >= p.life || p.dead)
                {
                    ps.RemoveAt(i);
                    p.onDeath?.Invoke(p, this);
                    continue;
                }
                if (p.drag > 0) p.vel *= Mathf.Exp(-p.drag * dt);
                p.vel += p.acc * dt;
                if (p.spinDrag > 0) p.spin *= Mathf.Exp(-p.spinDrag * dt);
                p.ang += p.spin * dt;
                p.upd?.Invoke(p, dt, this);
                p.pos += p.vel * dt;
                if (!float.IsNaN(p.ground) && p.pos.y > p.ground && p.vel.y > 0)
                {
                    p.pos.y = p.ground;
                    if (p.bounce > 0 && !p.bounced)
                    {
                        p.bounced = true;
                        p.vel = new Vector2(p.vel.x * 0.65f, -p.vel.y * p.bounce);
                        p.spin *= 0.5f;
                    }
                    else
                    {
                        p.onGround?.Invoke(p, this);
                        p.vel = Vector2.zero;
                        p.acc = Vector2.zero;
                    }
                }
            }
            T += dt;
        }

        static readonly Comparison<Item> Order = (a, b) => a.group != b.group ? a.group.CompareTo(b.group) : a.layer.CompareTo(b.layer);

        void Render()
        {
            items.Clear();
            mp.Clear();
            ms.Clear();
            foreach (var p in ps)
                p.draw?.Invoke(p, Mathf.Min(0.999f, p.age / p.life), items);
            // xếp ổn định theo (nhóm, lớp): List.Sort không ổn định nên thêm chỉ số làm khoá phụ
            for (int i = 0; i < items.Count; i++)
            {
                var it = items[i];
                it.layer += i * 1e-6f;
                items[i] = it;
            }
            items.Sort(Order);
            int[] n = { 0, 0, 0 };
            const float K = StageView.K;
            foreach (var it in items)
            {
                if (!it.sprite || it.w < 0.3f || it.h < 0.3f || it.alpha < 0.02f) continue;
                int g = it.group;
                var list = pool[g];
                Image img;
                if (n[g] < list.Count) img = list[n[g]];
                else
                {
                    img = Ui.Spawn(prefab, groups[g]);
                    img.name = "hat";
                    img.raycastTarget = false;
                    list.Add(img);
                }
                n[g]++;
                if (img.sprite != it.sprite) img.sprite = it.sprite;
                var c = it.color;
                c.a *= it.alpha;
                img.color = c;
                if (it.fill == 0)
                {
                    if (img.type != Image.Type.Simple) img.type = Image.Type.Simple;
                }
                else
                {
                    if (img.type != Image.Type.Filled) img.type = Image.Type.Filled;
                    img.fillMethod = Image.FillMethod.Vertical;
                    img.fillOrigin = it.fill == 1 ? (int)Image.OriginVertical.Top : (int)Image.OriginVertical.Bottom;
                    img.fillAmount = 0.5f;
                }
                img.enabled = true;
                var rt = img.rectTransform;
                rt.anchoredPosition = StageView.P(it.pos);
                rt.sizeDelta = new Vector2(it.w * K, it.h * K);
                rt.localEulerAngles = new Vector3(0, 0, it.ang);
            }
            for (int g = 0; g < 3; g++) HideFrom(g, n[g]);
            FlushMang();
        }

        // ---------- mảng nước liền (HatMang, con đầu của mỗi lớp hạt): hạt gọi MFill / MBand / MRibbon lúc vẽ (HatNuoc.cs) ----------
        struct MShape
        {
            public int group, a0, b0, n;
            public float layer;
            public byte kind;
            public Color32 col;
            public bool fringe;
        }

        readonly HatMang[] mang = new HatMang[3];
        readonly List<Vector2> mp = new List<Vector2>(4096); // điểm của khung hình (toạ độ sân)
        readonly List<MShape> ms = new List<MShape>(256);
        static readonly Comparison<MShape> MOrder = (a, b) => a.layer.CompareTo(b.layer);

        void FlushMang()
        {
            for (int i = 0; i < ms.Count; i++)
            {
                var s = ms[i];
                s.layer += i * 1e-5f;
                ms[i] = s;
            }
            ms.Sort(MOrder);
            for (int g = 0; g < 3; g++)
            {
                var m = mang[g];
                if (!m) continue;
                m.Begin();
                foreach (var s in ms)
                {
                    if (s.group != g) continue;
                    int a = m.PointCount, b = -1;
                    for (int i = 0; i < s.n; i++) m.Point(StageView.P(mp[s.a0 + i]));
                    if (s.kind != HatMang.Fill)
                    {
                        b = m.PointCount;
                        for (int i = 0; i < s.n; i++) m.Point(StageView.P(mp[s.b0 + i]));
                    }
                    m.Add(new HatMang.Shape { kind = s.kind, a0 = a, b0 = b, n = s.n, col = s.col, fringe = s.fringe });
                }
                m.End();
            }
        }

        void ClearMang()
        {
            mp.Clear();
            ms.Clear();
            for (int g = 0; g < 3; g++)
            {
                var m = mang[g];
                if (!m) continue;
                m.Begin();
                m.End();
            }
        }

        void HideFrom(int g, int k)
        {
            var list = pool[g];
            for (int i = k; i < list.Count; i++)
                if (list[i] && list[i].enabled) list[i].enabled = false;
        }

        // ---------- toán ----------
        static float EaseOut(float x)
        {
            x = Mathf.Clamp01(x);
            return 1 - (1 - x) * (1 - x) * (1 - x);
        }

        public static float SmoothStep(float a, float b, float x)
        {
            float t = Mathf.Clamp01((x - a) / (b - a));
            return t * t * (3 - 2 * t);
        }

        static Vector2 Unit(Vector2 v) => v.sqrMagnitude > 1e-8f ? v.normalized : new Vector2(0, -1);
        static float VelAng(Vector2 v) => -Mathf.Atan2(v.y, v.x) * Mathf.Rad2Deg;
        static float TipAngle(Vector2 d) => -Mathf.Atan2(d.x, -d.y) * Mathf.Rad2Deg;

        static Color C(int r, int g, int b) => new Color(r / 255f, g / 255f, b / 255f, 1);
        static readonly Color Ink = C(43, 33, 24);
        static readonly Dictionary<string, Color[]> Pal = new Dictionary<string, Color[]>
        {
            { "lua", new[] { C(234, 80, 42), C(248, 150, 48), C(252, 210, 78), C(254, 244, 206) } },
            { "xoan", new[] { C(206, 58, 38), C(240, 128, 44), C(249, 192, 68), C(253, 236, 176) } },
            { "nham", new[] { C(186, 46, 30), C(236, 104, 34), C(250, 170, 50), C(254, 230, 132) } },
            { "tinh", new[] { C(196, 30, 42), C(236, 80, 52), C(250, 156, 64), C(255, 232, 196) } },
            { "tim", new[] { C(128, 52, 172), C(208, 84, 192), C(246, 152, 216), C(255, 234, 250) } },
            { "vang", new[] { C(214, 52, 34), C(244, 150, 36), C(255, 212, 70), C(255, 246, 205) } },
            { "sen", new[] { C(194, 40, 82), C(236, 102, 142), C(250, 182, 172), C(255, 238, 232) } },
            { "nguu", new[] { C(220, 70, 30), C(246, 140, 40), C(255, 200, 70), C(255, 240, 200) } },
        };
        static readonly Color[] SmokeDark = { C(50, 42, 40), C(98, 92, 90), C(152, 148, 146), C(198, 194, 190) };
        static readonly Color[] SmokeFire = { C(240, 140, 50), C(168, 86, 50), C(112, 98, 94), C(160, 156, 152), C(204, 200, 196) };
        static readonly Color[] Lava = { Ink, C(204, 52, 28), C(242, 112, 34), C(252, 182, 56), C(255, 234, 150) };
        static readonly float[] LavaF = { 1, 1, 0.8f, 0.6f, 0.34f };

        static Color Ramp(Color[] stops, float k)
        {
            k = Mathf.Clamp01(k) * (stops.Length - 1);
            int i = Mathf.Min(stops.Length - 2, (int)k);
            return Color.Lerp(stops[i], stops[i + 1], k - i);
        }

        void Put(List<Item> buf, int g, float layer, Sprite s, Color c, Vector2 pos, float size, float stretch = 1, float ang = 0,
            float alpha = 1, int fill = 0) =>
            buf.Add(new Item { group = g, layer = layer, sprite = s, color = c, pos = pos, w = size * stretch, h = size, ang = ang, alpha = alpha, fill = fill });

        // ---------- vật liệu ----------
        static void Radii(float k, float r, float heat, float[] o)
        {
            o[0] = r;
            o[1] = r;
            o[2] = r * 0.88f * Mathf.Pow(Mathf.Max(0, 1 - k / Mathf.Min(1.4f, 0.95f * heat)), 0.6f);
            o[3] = r * 0.74f * Mathf.Pow(Mathf.Max(0, 1 - k / (0.68f * heat)), 0.7f);
            o[4] = r * 0.55f * Mathf.Pow(Mathf.Max(0, 1 - k / (0.4f * heat)), 0.7f);
        }

        readonly float[] rr = new float[5];
        static readonly float[] HookF = { 1, 1, 0.9f, 0.78f, 0.6f };
        static readonly float[] LobeF = { 1, 1, 0.8f, 0.6f, 0.38f };

        void DrawFlame(P p, float k, List<Item> buf)
        {
            float r;
            if (p.sizeFn != null) r = p.sizeFn(p, k);
            else
            {
                r = p.r0 + (p.r1 - p.r0) * Mathf.Pow(EaseOut(k / 0.75f), 0.8f);
                r *= 1 - 0.88f * Mathf.Pow(Mathf.Max(0, (k - 0.66f) / 0.34f), 1.3f);
            }
            if (r < 0.8f) return;
            Radii(k, r, p.heat, rr);
            var cols = Pal.TryGetValue(p.pal, out var pc) ? pc : Pal["lua"];
            float sp = p.vel.magnitude;
            int g = p.group;
            if (p.style == "luoi") // lưỡi lửa kiểu tranh tướng: ngọn ngả ngược hướng bay và lên, sọc màu to theo dáng lưỡi
            {
                var d = sp > 30 ? Unit(Unit(p.vel) * (0.5f * p.tip) + new Vector2(0, -p.tipUp)) : new Vector2(0, -1);
                float ang = TipAngle(d);
                for (int i = 0; i < 5; i++)
                {
                    float rad = i < 2 ? rr[i] : Mathf.Min(rr[1] * LobeF[i], rr[i] * 1.3f);
                    if (rad < 1) continue;
                    Put(buf, g, 20 + i, S((i == 0 ? "lobes_" : "lobe_") + (p.seed & 3)), i == 0 ? Ink : cols[i - 1],
                        p.pos - d * (r - rad) * 0.45f, 2.7f * rad + (i == 0 ? 5 : 0), 1, ang);
                }
                return;
            }
            if (p.style == "nhon")
            {
                var d = sp > 30 ? Unit(Unit(p.vel) * 0.55f + new Vector2(0, -0.45f)) : new Vector2(0, -1);
                float ang = TipAngle(d);
                for (int i = 0; i < 5; i++)
                {
                    float rad = i < 2 ? rr[i] : Mathf.Min(rr[1] * HookF[i], rr[i] * 1.25f);
                    if (rad < 1) continue;
                    Put(buf, g, 20 + i, S((i == 0 ? "hooks_" : "hook_") + (p.seed & 3)), i == 0 ? Ink : cols[i - 1],
                        p.pos - d * (r - rad) * 0.4f, 2.8f * rad + (i == 0 ? 5 : 0), 1, ang);
                }
                return;
            }
            float stretch = 1 + Mathf.Min(p.pal == "nham" ? 1.6f : 0.7f, sp / p.stretchK);
            float va = sp > 5 ? VelAng(p.vel) : p.ang * Mathf.Rad2Deg;
            for (int i = 0; i < 5; i++)
            {
                float rad = rr[i];
                if (rad < 1) continue;
                if (p.style == "xoan" && i >= 2)
                {
                    var d = Unit(new Vector2(Mathf.Cos(p.ang), -Mathf.Abs(Mathf.Sin(p.ang)) - 0.6f));
                    Put(buf, g, 20 + i, S("hook_" + ((p.seed + i) & 3)), cols[i - 1], p.pos - d * (r - rad) * 0.25f, 2.9f * rad, 1, TipAngle(d));
                    continue;
                }
                Put(buf, g, 20 + i, S((i == 0 ? "solid_" : "blob_") + (p.seed & 3)), i == 0 ? Ink : cols[i - 1], p.pos,
                    2 * rad + (i == 0 ? 5 : 0), stretch, va);
            }
            if (p.style == "xoan" && (p.seed & 1) == 0 && r > 6)
                Put(buf, g, 21.5f, S("curl_" + (p.seed % 3)), C(240, 128, 44), p.pos + new Vector2(r * 0.25f, 0), 1.3f * r, 1, p.ang * Mathf.Rad2Deg);
        }

        void DrawSmoke(P p, float k, List<Item> buf)
        {
            const float grow = 0.27f;
            float r = k < grow ? p.r0 + (p.r1 - p.r0) * EaseOut(k / grow) : p.r1 * (1 - 0.85f * SmoothStep(grow, 1, k));
            float aInk = 1 - SmoothStep(0.45f, 0.85f, k), aFill = 1 - SmoothStep(0.6f, 1, k);
            if (aFill < 0.03f || r < 0.8f) return;
            var stops = p.stops ?? (p.pal == "fire" ? SmokeFire : SmokeDark);
            float ang = p.ang * Mathf.Rad2Deg;
            if (aInk > 0.03f) Put(buf, p.group, 10, S("ssolid_" + (p.seed & 3)), Ink, p.pos, 2 * r + 4, 1, ang, aInk);
            Put(buf, p.group, 11, S("sblob_" + (p.seed & 3)), Ramp(stops, Mathf.Pow(k, 0.8f)), p.pos, 2 * r, 1, ang, aFill);
        }

        // đổi một hạt lửa sang lưỡi lửa vẽ tay kiểu tranh tướng (quét 2026-11-10: mọi chiêu bỏ cụm tròn "bong bóng"); tip: ngọn theo
        // hướng bay (+1: nổ, đuôi đạn) hay ngả ngược (-1: luồng phun, lốc), up: phần ngả lên
        static P Tongue(P q, float tip = 1, float up = 0.2f)
        {
            q.style = "luoi";
            q.tip = tip;
            q.tipUp = up;
            return q;
        }

        // ---------- hạt dựng sẵn ----------
        public P Flame(Vector2 pos, Vector2 vel, float life, float r0, float r1, string style = "tron", string pal = "lua", int group = Front,
            float drag = 1.8f, float accY = -320, float heat = 1, float smokeP = 0.25f, float emberP = 0.12f)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, r0 = r0, r1 = r1, style = style, pal = pal, group = group, drag = drag,
                acc = new Vector2(0, accY), heat = heat, seed = rng.Next(4), ang = U(0, 6.28f), spin = U(-3, 3)
            };
            p.draw = DrawFlame;
            p.onDeath = (q, s) =>
            {
                if ((float)q.rng.NextDouble() < smokeP)
                    Smoke(q.pos, null, 0, q.r1 * 0.22f, q.r1 * 0.55f, q.smokeGroup >= 0 ? q.smokeGroup : q.group);
                if ((float)q.rng.NextDouble() < emberP) Ember(q.pos, null, 0, 9, q.group);
            };
            return Add(p);
        }

        public P Smoke(Vector2 pos, Vector2? vel = null, float life = 0, float r0 = 8, float r1 = 24, int group = Front, string pal = "dark",
            float ashP = 0.35f)
        {
            var p = new P
            {
                pos = pos + U2(-4, 4), vel = vel ?? new Vector2(U(-30, 30), U(-70, -40)), life = life > 0 ? life : U(1.0f, 1.5f),
                drag = 1.4f, acc = new Vector2(0, -30), seed = rng.Next(4), spin = U(-0.8f, 0.8f), spinDrag = 1.2f, ang = U(0, 6.28f),
                r0 = r0, r1 = r1, group = group, ph = U(0, 6.28f), pal = pal
            };
            p.upd = (q, dt, s) =>
            {
                q.vel.x += Mathf.Sin(q.age * 5 + q.ph) * 30 * dt;
                q.vel.y -= 70 * (q.age / q.life) * dt;
            };
            p.stops = pal == "fire" ? FireStops() : Th.smoke;
            p.draw = DrawSmoke;
            if (U(0, 1) < ashP)
                p.onDeath = (q, s) =>
                {
                    int n = q.rng.Next(1, 3);
                    for (int i = 0; i < n; i++) Ash(q.pos + new Vector2(U(-q.r1, q.r1) * 0.4f, U(-q.r1, q.r1) * 0.4f), null, q.group);
                };
            return Add(p);
        }

        public P Ash(Vector2 pos, Vector2? vel = null, int group = Front, bool? dark = null)
        {
            bool dk = dark ?? U(0, 1) < 0.55f;
            var col = dk ? Color.Lerp(C(34, 30, 30), C(70, 64, 62), U(0, 1)) : Color.Lerp(C(140, 136, 132), C(196, 192, 188), U(0, 1));
            var p = new P
            {
                pos = pos, vel = vel ?? new Vector2(U(-35, 35), U(-70, -30)), life = U(1.0f, 1.8f), drag = 1.4f, acc = new Vector2(0, 26),
                seed = rng.Next(4), spin = U(-5, 5), group = group, col = col, ph = U(0, 6.28f), sz = U(4.5f, 8)
            };
            p.upd = (q, dt, s) => q.vel.x += Mathf.Sin(q.age * 3.2f + q.ph) * 55 * dt;
            p.draw = (q, k, buf) => Put(buf, q.group, 42, S("ash_" + (q.seed & 3)), q.col, q.pos, q.sz * (1 - k * k * k * k),
                1f / Mathf.Max(0.25f, Mathf.Abs(Mathf.Cos(q.age * 6 + q.ph))) * 0.5f + 0.5f, q.ang * Mathf.Rad2Deg);
            return Add(p);
        }

        public P Ember(Vector2 pos, Vector2? vel = null, float life = 0, float size = 9, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel ?? new Vector2(U(-40, 40), U(-90, -50)), life = life > 0 ? life : U(0.7f, 1.2f), drag = 1.6f,
                seed = rng.Next(2), spin = U(0, 6.28f), group = group, sz = size
            };
            p.upd = (q, dt, s) => q.vel.x += Mathf.Sin(q.age * 7 + q.spin) * 80 * dt;
            p.col = Th.ember;
            p.draw = (q, k, buf) => Put(buf, q.group, 41, S("emberg_" + (q.seed & 1)), q.col, q.pos, q.sz * (1 - k * k * k));
            return Add(p);
        }

        public P Spark(Vector2 pos, Vector2 dir, float speed, float life = 0, float size = 8, float grav = 400, int group = Front, float drag = 5)
        {
            var p = new P
            {
                pos = pos, vel = Unit(dir) * speed, life = life > 0 ? life : U(0.3f, 0.5f), drag = drag, acc = new Vector2(0, grav),
                seed = rng.Next(2), group = group, sz = size
            };
            p.col = Th.spark;
            p.draw = (q, k, buf) => Put(buf, q.group, 40, S("streakg_" + (q.seed & 1)), q.col, q.pos, q.sz * (1 - k * k),
                Mathf.Clamp(q.vel.magnitude / 90, 1.6f, 3.6f), VelAng(q.vel));
            return Add(p);
        }

        public P Ring(Vector2 pos, float life, float R0, float R1, Color col, float squash = 0.3f, int group = Floor, float layer = 30)
        {
            var p = new P { pos = pos, life = life, group = group, col = col, R0 = R0, R1 = R1, hgt = squash, ph = layer };
            p.draw = (q, k, buf) =>
            {
                float R = q.R0 + (q.R1 - q.R0) * EaseOut(k);
                float a = 1 - Mathf.Max(0, (k - 0.7f) / 0.3f);
                Put(buf, q.group, q.ph, S("rings"), Ink, q.pos, 2 * R * q.hgt, 1 / q.hgt, 0, a);
                Put(buf, q.group, q.ph + 0.5f, S("ring"), q.col, q.pos, 2 * R * q.hgt, 1 / q.hgt, 0, a);
            };
            return Add(p);
        }

        public P Rock(Vector2 pos, Vector2 vel, float ground, float sz = 0, int group = -1)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = 1.6f, acc = new Vector2(0, 1300), spin = U(-10, 10), seed = rng.Next(4), bounce = 0.32f,
                ground = ground, sz = sz > 0 ? sz : U(16, 24), group = group >= 0 ? group : (U(0, 1) < 0.5f ? Front : Back)
            };
            p.draw = (q, k, buf) => Put(buf, q.group, 45, S("rock_" + (q.seed & 3)), Color.white, q.pos, q.sz * (1 - SmoothStep(0.6f, 1, k)), 1,
                q.ang * Mathf.Rad2Deg);
            return Add(p);
        }

        // ---------- dung nham ----------
        void DrawLavaDrop(P z, float k, List<Item> buf)
        {
            float r = z.r1, sp = z.vel.magnitude;
            var d = sp > 1 ? z.vel / sp : new Vector2(0, 1);
            float tail = Mathf.Min(1, sp / 400);
            for (int li = 0; li < 5; li++)
            {
                for (int pi = 0; pi < 3; pi++)
                {
                    float ps = pi == 0 ? 1 : pi == 1 ? 0.66f : 0.38f;
                    var pos = z.pos - d * r * (pi == 0 ? 0 : pi == 1 ? 1.0f : 1.8f) * tail;
                    float rad = r * LavaF[li] * ps;
                    if (rad < 0.8f) continue;
                    Put(buf, z.group, 20 + li, S((li == 0 ? "solid_" : "blob_") + (z.seed & 3)), Lava[li], pos, 2 * rad + (li == 0 ? 4.5f : 0));
                }
            }
            if (z.crust) Put(buf, z.group, 25, S("rock_" + (z.seed & 3)), Color.white, z.pos + new Vector2(r * 0.25f, -r * 0.2f), r * 0.9f, 1,
                z.ang * Mathf.Rad2Deg);
        }

        void LavaSplat(P q)
        {
            var p = new P { pos = q.pos, life = U(0.45f, 0.65f), group = Floor, sz = q.r1 * 1.4f };
            p.draw = (z, k, buf) =>
            {
                float f = 1 - k * k;
                if (z.sz * f < 1) return;
                Put(buf, Floor, 5, S("ell"), Ink, z.pos, (z.sz * 0.75f + 2.5f) * f, 2.6f);
                Put(buf, Floor, 6, S("ell"), Color.Lerp(C(226, 92, 32), C(104, 46, 40), Mathf.Min(1, k * 1.4f)), z.pos, z.sz * 0.75f * f, 2.6f);
                Put(buf, Floor, 6.5f, S("ell"), C(252, 182, 56), z.pos, z.sz * 0.4f * Mathf.Max(0, 1 - k / 0.45f), 2.8f);
            };
            Add(p);
            if (q.r1 > 4.5f)
            {
                int n = rng.Next(2, 4);
                for (int i = 0; i < n; i++)
                {
                    float a = (-90 + U(-55, 55)) * Mathf.Deg2Rad;
                    var c = new P
                    {
                        pos = q.pos, vel = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(70, 150), life = 0.6f, acc = new Vector2(0, 900),
                        r1 = U(2.2f, 3.2f), seed = rng.Next(4), group = q.group, ground = q.pos.y + 1
                    };
                    c.draw = DrawLavaDrop;
                    c.onGround = (z, s) => z.dead = true;
                    Add(c);
                }
            }
        }

        public P LavaDrop(Vector2 pos, Vector2 vel, float r, float ground, int group = Front)
        {
            var q = new P
            {
                pos = pos, vel = vel, life = 2, drag = 0.3f, acc = new Vector2(0, 1400), r1 = r, seed = rng.Next(4), group = group,
                ang = U(0, 6.28f), spin = U(-4, 4), crust = U(0, 1) < 0.3f, ground = ground
            };
            q.draw = DrawLavaDrop;
            q.onGround = (z, s) =>
            {
                LavaSplat(z);
                z.dead = true;
            };
            return Add(q);
        }

        void LavaPool(Vector2 pos, float life, float R)
        {
            var pool = new P { pos = pos, life = life, group = Floor };
            pool.draw = (q, k, buf) =>
            {
                if (k > 0.98f) return;
                float a = Mathf.Min(1, k / 0.1f), f = 1 - k * k * k;
                Put(buf, Floor, 2, S("ell"), Ink, q.pos, (R + 5) * f * a, 3.2f);
                Put(buf, Floor, 3, S("ell"), Color.Lerp(C(186, 46, 30), C(96, 44, 40), k), q.pos, R * f * a, 3.3f);
                Put(buf, Floor, 4, S("ell"), C(236, 104, 34), q.pos, R * 0.65f * Mathf.Max(0, 1 - k / 0.75f) * a, 3.8f);
                Put(buf, Floor, 4.5f, S("ell"), C(250, 170, 50), q.pos, R * 0.35f * Mathf.Max(0, 1 - k / 0.5f) * a, 4.4f);
            };
            Add(pool);
        }

        public void Crater(Vector2 pos, float R, float life, float H)
        {
            var cr = new P { pos = pos, life = life, group = Floor, seed = rng.Next(4), sz = H };
            cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_" + q.seed), Color.white, q.pos, 1.7f * q.sz * 0.42f * Mathf.Min(1, q.age / 0.2f),
                1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.25f));
            Add(cr);
            LavaPool(pos, life, R);
            float ax = 1.55f * R, ay = 0.5f * R;
            const int n = 13;
            for (int j = 0; j < n; j++)
            {
                float th = 2 * Mathf.PI * j / n + U(-0.15f, 0.15f);
                var rp = new P
                {
                    pos = pos + new Vector2(ax * Mathf.Cos(th), ay * Mathf.Sin(th)), life = life, group = Floor, seed = rng.Next(4),
                    ang = U(0, 6.28f), sz = U(9, 15) * (Mathf.Sin(th) > 0 ? 1.15f : 0.9f), ph = th
                };
                rp.draw = (q, k, buf) => Put(buf, Floor, Mathf.Sin(q.ph) > 0 ? 9 : 1.5f, S("rock_" + (q.seed & 3)), Color.white, q.pos,
                    q.sz * Mathf.Min(1, EaseOut(q.age / 0.15f)) * (1 - SmoothStep(0.8f, 1, k)), 1, q.ang * Mathf.Rad2Deg);
                Add(rp);
            }
            for (int j = 0; j < 4; j++)
            {
                var cp = new P
                {
                    pos = pos + new Vector2(U(-0.9f, 0.9f) * ax * 0.6f, U(-0.5f, 0.5f) * ay * 0.6f), vel = new Vector2(U(-6, 6), U(-2, 2)),
                    life = life, group = Floor, seed = rng.Next(4), ang = U(0, 6.28f), spin = U(-0.6f, 0.6f), sz = U(8, 12)
                };
                cp.draw = (q, k, buf) => Put(buf, Floor, 7, S("rock_" + (q.seed & 3)), Color.white, q.pos,
                    q.sz * Mathf.Min(1, k / 0.15f) * (1 - SmoothStep(0.75f, 1, k)), 1.6f, q.ang * Mathf.Rad2Deg);
                Add(cp);
            }
            Every(0.1f, life * 0.75f, 7, x =>
            {
                var bp = new P
                {
                    pos = pos + new Vector2(U(-0.8f, 0.8f) * ax * 0.7f, U(-0.6f, 0.6f) * ay * 0.7f), life = U(0.25f, 0.4f), group = Floor,
                    sz = U(4, 7)
                };
                bp.draw = (q, k, buf) =>
                {
                    Put(buf, Floor, 8, S("ell"), Ink, q.pos, q.sz * EaseOut(k) * 2 + 3, 1.2f);
                    Put(buf, Floor, 8.5f, S("ell"), C(252, 182, 56), q.pos, q.sz * EaseOut(k) * 2, 1.2f);
                };
                bp.onDeath = (q, s) =>
                {
                    for (int i = 0; i < 2; i++)
                    {
                        float a = (-90 + U(-40, 40)) * Mathf.Deg2Rad;
                        var c = new P
                        {
                            pos = q.pos, vel = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(80, 140), life = 0.5f, acc = new Vector2(0, 900),
                            r1 = 2.6f, seed = rng.Next(4), group = Front, ground = q.pos.y + 1
                        };
                        c.draw = DrawLavaDrop;
                        c.onGround = (z, s2) => z.dead = true;
                        Add(c);
                    }
                };
                Add(bp);
            });
            Every(0.1f, life * 0.8f, 6, x => Smoke(pos + new Vector2(U(-ax, ax) * 0.6f, -4), null, 0, 4, 11, Back, "dark", 0.2f));
        }

        // ---------- nổ ----------
        public void Explode(Vector2 c, float sc, float H, int group = Front)
        {
            var f = new P { pos = c, life = 0.13f, group = group, seed = rng.Next(4), ang = U(0, 6.28f), col = Pal[Th.pal][2] };
            f.draw = (q, k, buf) =>
            {
                float s = 0.66f * H * sc * (0.7f + 0.45f * EaseOut(k / 0.5f)), a = q.ang * Mathf.Rad2Deg;
                Put(buf, q.group, 30, S("bursts_" + q.seed), Ink, q.pos, s + 6, 1, a);
                Put(buf, q.group, 31, S("burst_" + q.seed), q.col, q.pos, s, 1, a);
                Put(buf, q.group, 32, S("burst_" + q.seed), C(254, 244, 214), q.pos, s * 0.6f, 1, a);
            };
            Add(f);
            int n1 = (int)(9 * sc + 2);
            for (int i = 0; i < n1; i++)
            {
                float a = 6.28f * (i + U(-0.3f, 0.3f)) / n1; // rải đều quanh tâm: vành lưỡi lửa như cánh hoa, không dồn cục
                var q = Flame(c + U2(-5, 5), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(160, 280) * sc, U(0.34f, 0.48f), 10 * sc,
                    U(17, 23) * sc, "tron", Th.pal, group, 4.5f, -160, 1.6f, 0.3f);
                Tongue(q, 1, 0.12f);
                q.smokeGroup = Back;
            }
            int n2 = (int)(5 * sc + 1);
            for (int i = 0; i < n2; i++)
            {
                float a = U(0, 6.28f);
                Flame(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * 360 * sc, 0.24f, 5 * sc, 12 * sc, "nhon", Th.pal, group, 5.5f, -100, 1.6f, 0);
            }
            var rg = new P { pos = c, life = 0.24f, group = group, sz = H * sc, col = Th.ring2 };
            rg.draw = (q, k, buf) =>
            {
                float R = (0.12f + 0.22f * EaseOut(k)) * q.sz, a = 1 - Mathf.Max(0, (k - 0.7f) / 0.3f);
                Put(buf, q.group, 35, S("rings"), Ink, q.pos, 2 * R, 1, 0, a);
                Put(buf, q.group, 35.5f, S("ring"), q.col, q.pos, 2 * R, 1, 0, a);
            };
            Add(rg);
            int s1 = (int)(10 * sc), s2 = (int)(6 * sc);
            for (int i = 0; i < s1; i++) Spark(c + U2(-6, 6), U2(-1, 1), U(280, 480) * sc);
            At(0.1f, () =>
            {
                for (int i = 0; i < s2; i++) Spark(c + U2(-6, 6), U2(-1, 1), U(280, 480) * sc);
            });
            At(0.14f, () =>
            {
                int n = (int)(3 * sc + 1);
                for (int i = 0; i < n; i++) Smoke(c + U2(-16, 16) - new Vector2(0, 18), null, 0, 7 * sc, 18 * sc, Back);
            });
            for (int i = 0; i < (int)(6 * sc); i++) Ash(c + U2(-20, 20), new Vector2(U(-80, 80), U(-130, -60)));
            Extra(c, (int)(6 * sc + 2), 320 * sc, group);
        }

        // ================= CHIÊU MANA (thay tia nước) =================
        // trả thời gian tới lúc trúng (giây sân)

        // thời gian tướng phải giữ dáng phun từ lúc gọi Breath tới khi luồng lửa tắt (T1 + đuôi)
        public const float BreathHold = 1.22f;

        public float Breath(Vector2 mouth, Vector2 target, float tH, bool swirl)
        {
            // người dùng 2026-11-10: lửa phun phải hợp nét tranh tướng -> lưỡi lửa vẽ tay (ngọn quặp, sọc màu, vân chì đậm)
            string style = "luoi", pal = Th.pal;
            var dd = target - mouth;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            var up = nrm.y < 0 ? nrm : -nrm;
            const float T0 = 0.28f, T1 = 1.18f, Hit = 34;
            Every(0, 0.2f, 40, x =>
            {
                float a = U(0, 6.28f);
                var pos = mouth + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(55, 80);
                var e = Ember(pos, (mouth - pos) * 2.2f, 0.24f, 8);
                e.upd = (q, dt, s) => q.vel *= 1 + 3 * dt;
            });
            Every(0.06f, T0, 30, x => Flame(mouth + U2(-4, 4), u * 25, 0.22f, 4, 10 + 26 * x, style, pal, Front, 1.8f, -320, 1, 0));
            Every(T0, T1, x => 95 * (x < 0.11f ? 1.5f : 1f) * Mathf.Min(1, (1 - x) * (T1 - T0) / 0.16f), x =>
            {
                float a = U(-1, 1) * 12 * Mathf.Deg2Rad;
                var dv = u * Mathf.Cos(a) + nrm * Mathf.Sin(a);
                float ramp = Mathf.Min(1, x * (T1 - T0) / 0.08f);
                var p = Flame(mouth + dv * U(0, 8), dv * U(1200, 1400), U(0.4f, 0.52f), U(13, 16), U(28, 36) * (0.8f + 0.2f * ramp), style, pal,
                    Front, 1.8f, -320, 1, 0.3f);
                p.smokeGroup = Back;
                p.upd = (q, dt, s) =>
                {
                    float k = q.age / q.life;
                    q.vel += nrm * Mathf.Sin(q.age * 17 + q.spin) * 260 * k * dt;
                    if (!q.hit && Vector2.Dot(q.pos - mouth, u) > dist - Hit)
                    {
                        q.hit = true;
                        float vu = Vector2.Dot(q.vel, u);
                        float side = Vector2.Dot(q.pos - mouth, nrm) >= 0 ? 1 : -1;
                        q.vel += -u * vu * 0.92f + nrm * side * Mathf.Abs(vu) * U((System.Random)q.rng, 0.15f, 0.32f);
                        float rNow = q.r0 + (q.r1 - q.r0) * Mathf.Pow(EaseOut(k / 0.75f), 0.8f);
                        q.life = Mathf.Min(q.life, q.age + U((System.Random)q.rng, 0.1f, 0.16f));
                        q.r1 = Mathf.Min(q.r1, rNow * 1.05f);
                        q.r0 = Mathf.Min(q.r0, q.r1);
                        q.acc = Vector2.zero;
                    }
                };
            });
            Every(T0, T1, 14, x =>
            {
                if (x < 0.12f) return;
                float f = U(0.45f, 0.95f);
                Smoke(mouth + u * dist * f + up * U(14, 26) * (0.6f + f), new Vector2(U(-30, 30), U(-70, -40)) - u * 20, 0,
                    6 * (0.8f + 0.5f * f), 18 * (0.8f + 0.5f * f), Back);
            });
            Every(T0, T1, 14, x =>
            {
                float f = U(0.25f, 0.8f), sd = U(0, 1) < 0.5f ? -1 : 1;
                var pos = mouth + u * dist * f + nrm * sd * U(18, 30) * (0.5f + f);
                Spark(pos, u * U(0.5f, 1) + nrm * sd * U(0.4f, 0.9f) + new Vector2(0, -0.3f), U(260, 420));
            });
            if (swirl || Th.extra == "may") // Lân Hỏa, Ngưu Quyền: mây xoắn vàng bay dọc luồng
                Every(T0 + 0.1f, T1, 10, x => Extra(mouth + u * dist * U(0.3f, 0.9f) + up * U(10, 30), 1, 120));
            float tHit = T0 + 0.24f;
            At(tHit, () =>
            {
                Shake?.Invoke(0.25f);
                for (int i = 0; i < 5; i++)
                {
                    float a = Mathf.Atan2(-u.y, -u.x) + U(-1.4f, 1.4f);
                    Spark(target + U2(-10, 10), new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.5f), U(250, 460));
                }
                Extra(target, 4, 300);
            });
            At(T1 - 0.05f, () =>
            {
                for (int i = 0; i < 4; i++) Smoke(mouth + u * dist * U(0.45f, 0.8f) + U2(-18, 18), null, 0, 8, 22, Back);
                for (int i = 0; i < 8; i++) Ash(target + U2(-30, 30));
            });
            return tHit;
        }

        public float Fireball(Vector2 mouth, Vector2 tgt, float tH)
        {
            const float T0 = 0.3f, TT = 0.45f;
            var d = Unit(tgt - mouth);
            Vector2 Path(float t)
            {
                float x = Mathf.Clamp01((t - T0) / TT);
                return mouth + (tgt - mouth) * x + new Vector2(0, -40) * Mathf.Sin(Mathf.PI * x);
            }
            float t0 = T;
            Every(0, T0 - 0.05f, 45, x =>
            {
                float a = U(0, 6.28f);
                var pos = mouth + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(45, 70);
                var e = Ember(pos, (mouth - pos) * 2.4f, 0.22f, 8);
                e.upd = (q, dt, s) => q.vel *= 1 + 3 * dt;
            });
            Every(0.04f, T0, 50, x => Flame(mouth + U2(-3, 3), d * 20, 0.14f, 6, 8 + 14 * x, "tron", Th.pal, Front, 1.8f, -320, 1.8f, 0));
            Every(T0, T0 + TT, 150, x =>
            {
                var q = Flame(Path(T - t0), Vector2.zero, U(0.12f, 0.18f), 13, U(17, 21), "tron", Th.pal, Front, 0, 0, 1.9f, 0, 0);
                q.off = U2(-6, 6);
                q.drift = U2(-40, 40);
                q.upd = (z, dt, s) =>
                {
                    z.off += z.drift * dt;
                    var now = Path(s.T - t0);
                    z.vel = (Path(s.T - t0 + 0.01f) - now) / 0.01f * 0.15f;
                    z.pos = now + z.off - z.vel * dt;
                };
            });
            Every(T0, T0 + TT, 60, x =>
            {
                var q = Flame(Path(T - t0) - d * 4 + U2(-7, 7), -d * U(60, 130) + new Vector2(-d.y, d.x) * U(-70, 70) + new Vector2(0, -20),
                    U(0.18f, 0.26f), 17, 17, "tron", Th.pal, Front, 3, -140, 1.4f, 0, 0.04f);
                Tongue(q, 1, 0.2f);
                q.sizeFn = (z, k) => z.r1 * Mathf.Pow(1 - k, 1.1f);
            });
            Every(T0 + 0.03f, T0 + TT, 55, x => Smoke(Path(T - t0) - d * 22 + U2(-4, 4), new Vector2(U(-12, 12), U(-30, -10)), U(0.7f, 1.0f), 9,
                U(15, 19), Front, "fire", 0.1f));
            Every(T0, T0 + TT, 25, x => Spark(Path(T - t0), -d + U2(-0.6f, 0.6f), U(140, 260)));
            At(T0 + TT, () =>
            {
                Shake?.Invoke(0.45f);
                Explode(tgt, 0.85f, tH);
            });
            return T0 + TT;
        }

        public float Needles(Vector2 casterFeet, float casterH, float casterW, Vector2 tgt, float tH)
        {
            var A = casterFeet + new Vector2(0, -1.08f * casterH);
            const int N = 7;
            float RA = 0.42f * casterW, LEN = 58;
            var pc = Pal[Th.pal];
            Color[] cols = { Ink, pc[0], pc[1], pc[2], pc[3] };
            float[] fr = { 1, 1, 0.82f, 0.6f, 0.34f };
            float[] ext = { 4.5f, 0, 0, 0, 0 };
            for (int i = 0; i < N; i++)
            {
                int ii = i;
                At(0.06f + i * 0.07f, () =>
                {
                    float th = Mathf.PI + Mathf.PI * (ii + 0.5f) / N;
                    var home = A + new Vector2(RA * Mathf.Cos(th), 0.5f * RA * Mathf.Sin(th));
                    var aim = tgt + new Vector2(U(-0.18f, 0.18f) * tH, U(-0.15f, 0.2f) * tH);
                    var q = new P { pos = home, life = 3, seed = 0, home = home, aim = aim, span = ii, launch = T + 0.72f - ii * 0.07f + ii * 0.09f };
                    for (int k = 0; k < 3; k++)
                        Flame(home + U2(-6, 6), new Vector2(U(-30, 30), U(-70, -30)), 0.22f, 5, 11, "tron", Th.pal, Front, 1.8f, -320, 1.6f, 0);
                    Ember(home, null, 0, 7);
                    q.upd = (z, dt, s) =>
                    {
                        if (!z.fly)
                        {
                            z.pos = z.home + new Vector2(0, 3.5f * Mathf.Sin(z.age * 7 + z.span));
                            z.vel = (z.aim - z.pos) * 0.001f;
                            if (s.U(0, 1) < 0.12f)
                                s.Flame(z.pos + s.U2(-8, 8), new Vector2(s.U(-15, 15), s.U(-80, -40)), 0.25f, 4, 9, "nhon", Th.pal, Front, 1.8f, -320, 1.7f, 0, 0.1f);
                            if (s.T >= z.launch)
                            {
                                z.fly = true;
                                z.vel = Unit(z.aim - z.pos) * 1500;
                                s.Shake?.Invoke(0.05f);
                            }
                        }
                        else
                        {
                            if (s.U(0, 1) < 0.35f)
                                s.Spark(z.pos - Unit(z.vel) * 22, -Unit(z.vel) + s.U2(-0.15f, 0.15f), s.U(250, 380), 0.14f, 11, 0, Front, 6);
                            if (s.U(0, 1) < 0.12f)
                                s.Flame(z.pos - Unit(z.vel) * 24, -Unit(z.vel) * 40, 0.12f, 6, 9, "tron", Th.pal, Front, 1.8f, -320, 1.6f, 0, 0);
                            if (Vector2.Dot(z.aim - z.pos, z.vel) <= 0)
                            {
                                z.dead = true;
                                s.NeedleHit(z.aim, Unit(z.vel));
                            }
                        }
                    };
                    q.draw = (z, k, buf) =>
                    {
                        float age = z.age;
                        float sc = age < 0.08f ? 1.25f * EaseOut(age / 0.08f) : 1.25f - 0.25f * Mathf.Min(1, (age - 0.08f) / 0.06f);
                        var d = z.fly ? Unit(z.vel) : Unit(z.aim - z.pos);
                        float ang = TipAngle(d), st = z.fly ? 1.3f : 1;
                        for (int li = 0; li < 5; li++)
                        {
                            float L = LEN * sc * fr[li] * (li < 2 ? st : 1) + ext[li];
                            Put(buf, Front, 20 + li, S(li == 0 ? "needles_0" : "needle_0"), cols[li], z.pos - d * (LEN * sc * (1 - fr[li]) * 0.25f), L, 1, ang);
                        }
                    };
                    Add(q);
                });
            }
            float first = 0.06f + 0.72f + 0.1f;
            At(0.78f + N * 0.09f + 0.2f, () =>
            {
                for (int i = 0; i < 4; i++) Smoke(tgt + U2(-25, 25), null, 0, 7, 18, Back);
            });
            return first;
        }

        void NeedleHit(Vector2 p, Vector2 d)
        {
            Shake?.Invoke(0.14f);
            var f = new P { pos = p, life = 0.06f };
            f.draw = (q, k, buf) =>
            {
                Put(buf, Front, 30, S("solid_0"), Ink, q.pos, 31);
                Put(buf, Front, 31, S("blob_0"), C(254, 244, 214), q.pos, 26);
            };
            Add(f);
            for (int i = 0; i < 3; i++)
            {
                float a = U(0, 6.28f);
                Tongue(Flame(p, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * 150, 0.26f, 7, 13, "tron", Th.pal, Front, 4, -320, 1.6f, 0.25f), 1, 0.2f);
            }
            for (int i = 0; i < 5; i++) Spark(p, -d + U2(-0.9f, 0.9f), U(200, 380), 0, 7);
            Extra(p, 2, 260);
        }

        public float LavaBall(Vector2 mouth, Vector2 foeFeet, float tH, float casterGround)
        {
            var land = foeFeet + new Vector2(0, -0.3f * tH);
            const float T0 = 0.3f, TT = 0.6f, ARC = 115;
            float t0 = T;
            Vector2 Path(float t)
            {
                float x = Mathf.Clamp01((t - T0) / TT);
                return mouth + (land - mouth) * x + new Vector2(0, -4 * ARC * x * (1 - x));
            }
            Vector2 Vel(float t) => (Path(t + 0.01f) - Path(t - 0.01f)) / 0.02f;
            Every(0, T0, 60, x => Flame(mouth + U2(-4, 4), new Vector2(U(-30, 30), U(-90, -40)), 0.2f, 5, 6 + 10 * x, "tron", "nham", Front, 1.8f, -320, 1.8f, 0));
            At(T0, () =>
            {
                var ball = new P { pos = Path(T0), life = TT, spin = -6 };
                ball.upd = (q, dt, s) =>
                {
                    q.pos = Path(s.T - t0);
                    q.vel = Vel(s.T - t0);
                };
                ball.draw = (q, k, buf) =>
                {
                    const float r = 22;
                    float sp = q.vel.magnitude, st = 1 + Mathf.Min(0.25f, sp / 3000), ang = VelAng(q.vel);
                    Put(buf, Front, 20, S("solid_2"), Ink, q.pos, 2 * r + 5, st, ang);
                    Put(buf, Front, 21, S("blob_2"), C(186, 46, 30), q.pos, 2 * r, st, ang);
                    Put(buf, Front, 22, S("blob_3"), C(236, 104, 34), q.pos, 1.64f * r, st, ang);
                    Put(buf, Front, 23, S("blob_0"), C(250, 170, 50), q.pos, 1.15f * r, st, ang);
                    Put(buf, Front, 24, S("blob_1"), C(254, 230, 132), q.pos, 0.6f * r, st, ang);
                    for (int i = 0; i < 3; i++)
                    {
                        float a = q.ang + i * 2.1f;
                        Put(buf, Front, 25, S("rock_" + i), Color.white, q.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * r * 0.62f, r * 0.55f, 1,
                            a * Mathf.Rad2Deg);
                    }
                };
                Add(ball);
            });
            Every(T0, T0 + TT, 50, x => Flame(Path(T - t0) + U2(-12, 12), new Vector2(U(-20, 20), -60), 0.22f, 5, 9, "tron", "nham", Front, 1.8f, -320, 1.8f, 0));
            Every(T0 + 0.05f, T0 + TT, 16, x => LavaDrop(Path(T - t0) + U2(-8, 8), Vel(T - t0) * 0.25f + new Vector2(U(-40, 40), 0), U(4, 7),
                Mathf.Lerp(casterGround, foeFeet.y, x) + U(-10, 20)));
            Every(T0 + 0.05f, T0 + TT, 100, x => Smoke(Path(T - t0) - Unit(Vel(T - t0)) * 22 + U2(-4, 4), new Vector2(0, -20), U(0.7f, 0.95f), 9,
                U(15, 19), Front, "fire", 0.08f));
            At(T0 + TT, () =>
            {
                Shake?.Invoke(0.6f);
                for (int i = 0; i < 22; i++)
                {
                    float a = (-90 + U(-60, 60)) * Mathf.Deg2Rad;
                    LavaDrop(land + U2(-10, 10), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(180, 380), U(4, 8), foeFeet.y + U(-12, 18),
                        U(0, 1) < 0.45f ? Front : Back);
                }
                for (int i = 0; i < 16; i++)
                {
                    float a = U(0, 6.28f);
                    Flame(land + U2(-6, 6), new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.7f) * U(100, 220), 0.4f, 12, U(18, 26), "tron", "nham", Back,
                        4, 200, 1.6f, 0.3f);
                }
                for (int i = 0; i < 5; i++)
                {
                    float a = (-90 + U(-60, 60)) * Mathf.Deg2Rad;
                    Rock(land, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(300, 560), foeFeet.y + U(-14, 22));
                }
                Crater(foeFeet + new Vector2(0, 2), 20, 1.4f, tH);
                Extra(land, 5, 360);
                for (int i = 0; i < 6; i++) Smoke(land + U2(-20, 20) - new Vector2(0, 20), null, 0, 10, 24, Back);
            });
            return T0 + TT;
        }

        // ================= CHIÊU CUỐI (thêm vào clip CHIÊU, lúc trúng) =================

        public float Meteor(Vector2 foeFeet, float tH, float fromSide)
        {
            var imp = foeFeet + new Vector2(0, -6);
            var s0 = foeFeet + new Vector2(fromSide * 310, -480);
            const float TI = 0.75f;
            float t0 = T;
            Vector2 Path(float t) => s0 + (imp - s0) * Mathf.Pow(Mathf.Clamp01(t / TI), 1.6f);
            var dv = Unit(imp - s0);
            var shadow = new P { pos = foeFeet, life = TI, group = Floor };
            shadow.draw = (q, k, buf) => Put(buf, Floor, 1, S("ell"), C(40, 24, 20), q.pos, 0.3f * tH * (0.25f + 0.75f * k), 3, 0, 0.2f + 0.3f * k);
            Add(shadow);
            var met = new P { pos = s0, life = TI, spin = -7, seed = 1 };
            met.upd = (q, dt, s) => q.pos = Path(s.T - t0);
            met.draw = (q, k, buf) => Put(buf, Front, 45, S("rock_1"), Color.white, q.pos, 58, 1, q.ang * Mathf.Rad2Deg);
            Add(met);
            var side = new Vector2(-dv.y, dv.x);
            Every(0.02f, TI, 48, x => Tongue(Flame(Path(T - t0) + U2(-9, 9), -dv * U(140, 280) + side * U(-120, 120), U(0.22f, 0.34f), 17, U(22, 28),
                "tron", Th.pal, Front, 3, -120, 1.3f, 0.3f), 1, 0.1f));
            // lửa trùm quanh đá: lưỡi lửa ngả về sau (cụm tròn ở đây kéo thành chuỗi hạt dọc đường bay)
            Every(0.02f, TI, 30, x => Tongue(Flame(Path(T - t0) - dv * 6 + U2(-8, 8), dv * 60, 0.14f, 16, 22, "tron", Th.pal, Back, 1.8f, -320, 1.5f, 0), -1, 0.1f));
            Every(0.05f, TI, 40, x => Smoke(Path(T - t0) - dv * 44 + U2(-8, 8), -dv * 30 + U2(-15, 15), U(0.8f, 1.2f), 6, 17, Back));
            Every(0.05f, TI, 18, x => Spark(Path(T - t0), -dv + U2(-0.6f, 0.6f), U(150, 300)));
            At(TI, () =>
            {
                Shake?.Invoke(0.9f);
                FlashScreen?.Invoke(new Color(1, 0.96f, 0.84f, 0.45f));
                Explode(foeFeet + new Vector2(0, -0.45f * tH), 0.9f, tH);
                for (int i = 0; i < 18; i++)
                {
                    float a = -180f * (i + U(-0.3f, 0.3f)) / 17 * Mathf.Deg2Rad; // vành lưỡi lửa nửa trên, rải đều
                    Tongue(Flame(imp + U2(-10, 10), new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 1.1f) * U(300, 650), U(0.45f, 0.7f), 15, U(28, 38), "tron", Th.pal,
                        Back, 4, -200, 1.4f, 0.35f), 1, 0.2f);
                }
                for (int i = 0; i < 12; i++)
                {
                    float a = U(-170, -10) * Mathf.Deg2Rad;
                    Flame(imp, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * 520, 0.32f, 8, 20, "nhon", Th.pal, Back, 5, -150, 1, 0);
                }
                foreach (int sd in new[] { -1, 1 })
                    for (int i = 0; i < 3; i++)
                        Tongue(Flame(foeFeet + new Vector2(sd * U(10, 30), 6), new Vector2(sd * U(250, 420), -30), 0.35f, 8, U(13, 18), "tron", Th.pal, Front, 4, -200, 1.3f, 0),
                            0.4f, 0.6f);
                Ring(foeFeet + new Vector2(0, 2), 0.4f, 0.2f * tH, 1.6f * tH, Th.ring);
                At(0.1f, () => Ring(foeFeet + new Vector2(0, 2), 0.35f, 0.1f * tH, 1.2f * tH, Th.ring2));
                for (int i = 0; i < 8; i++)
                {
                    float a = (-90 + U(-70, 70)) * Mathf.Deg2Rad;
                    Rock(imp, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(350, 650), foeFeet.y + U(-15, 25));
                }
                for (int i = 0; i < 14; i++) Spark(imp + U2(-12, 12), new Vector2(U(-1, 1), -U(0.3f, 1)), U(300, 560));
                At(0.1f, () =>
                {
                    for (int i = 0; i < 10; i++) Spark(imp + U2(-12, 12), new Vector2(U(-1, 1), -U(0.3f, 1)), U(300, 560));
                });
                for (int i = 0; i < 16; i++)
                {
                    float sd = U(0, 1) < 0.5f ? -1 : 1;
                    Smoke(foeFeet + new Vector2(sd * U(15, 45), U(-6, 4)), new Vector2(sd * U(90, 260), -U(10, 50)), U(1.0f, 1.4f), 9, U(16, 22), Back);
                }
                for (int i = 0; i < 6; i++)
                    Smoke(imp + new Vector2(U(-30, 30), -U(40, 80)), new Vector2(U(-40, 40), -U(140, 220)), U(1.2f, 1.5f), 14, 30, Back);
                for (int i = 0; i < 14; i++) Ash(imp + U2(-40, 40), new Vector2(U(-80, 80), -U(80, 160)));
                Extra(imp + new Vector2(0, -20), 10, 420);
                var cr = new P { pos = foeFeet + new Vector2(0, 2), life = 1.5f, group = Floor, sz = tH };
                cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_1"), Color.white, q.pos, 1.6f * q.sz * 0.42f, 1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.3f));
                Add(cr);
            });
            return TI;
        }

        public float Eruption(Vector2 foeFeet, float tH)
        {
            float gy = foeFeet.y;
            var pre = new P { pos = foeFeet + new Vector2(0, 2), life = 0.45f, group = Floor, sz = tH };
            pre.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_0"), Color.white, q.pos, 1.5f * q.sz * 0.42f * (0.3f + 0.7f * EaseOut(q.age / 0.3f)), 1 / 0.42f);
            Add(pre);
            Shake?.Invoke(0.15f);
            Every(0.05f, 0.42f, 22, x => LavaDrop(foeFeet + new Vector2(U(-0.45f, 0.45f) * tH, U(-6, 6)), new Vector2(U(-30, 30), -U(100, 180)), U(3, 5),
                gy + U(-6, 8)));
            At(0.42f, () =>
            {
                Shake?.Invoke(0.6f);
                FlashScreen?.Invoke(new Color(1, 0.9f, 0.7f, 0.18f));
                Crater(foeFeet + new Vector2(0, 6), 30, 1.65f, tH);
                Extra(foeFeet + new Vector2(0, -20), 6, 380);
                for (int w = 0; w < 2; w++)
                {
                    int n = w == 0 ? 14 : 8;
                    At(w * 0.1f, () =>
                    {
                        for (int i = 0; i < n; i++)
                        {
                            float a = (-90 + U(-32, 32)) * Mathf.Deg2Rad;
                            LavaDrop(foeFeet + new Vector2(U(-0.2f, 0.2f) * tH, -4), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(320, 560), U(8, 12),
                                gy + U(-10, 18), U(0, 1) < 0.5f ? Front : Back);
                        }
                    });
                }
                for (int i = 0; i < 6; i++)
                {
                    float a = (-90 + U(-55, 55)) * Mathf.Deg2Rad;
                    Rock(foeFeet + new Vector2(0, -6), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(380, 680), gy + U(-14, 22));
                }
            });
            Every(0.42f, 0.82f, 90, x =>
            {
                var v = new Vector2(U(-60, 60), -U(640, 880) * (1 - 0.4f * x));
                float r = U(20, 28) * (1 - 0.3f * x);
                var q = Flame(foeFeet + new Vector2(U(-0.14f, 0.14f) * tH, -2), v, U(0.7f, 0.85f), r * 0.6f, r, "tron", "nham", Back, 0.6f, 1500, 1.5f, 0.15f);
                q.stretchK = 700;
                q.sizeFn = (z, k) => (z.r0 + (z.r1 - z.r0) * Mathf.Min(1, k / 0.3f)) * (1 - Mathf.Max(0, (k - 0.75f) / 0.25f));
            });
            Every(0.5f, 1.3f, 7, x => Smoke(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.3f, 1.0f) * tH), new Vector2(U(-40, 40), -U(60, 110)), 0, 10, 26, Back));
            return 0.42f;
        }

        public float Tornado(Vector2 foeFeet, float tH)
        {
            var Cc = foeFeet + new Vector2(0, 2);
            float HT = 1.22f * tH, R0 = 16, R1 = 74, OM = 9, T1 = 1.9f;
            Every(0, T1, 40, x =>
            {
                float a = U(0, 6.28f);
                var pos = Cc + new Vector2(Mathf.Cos(a) * 1.1f * tH, Mathf.Sin(a) * 0.3f * tH);
                var tang = new Vector2(-Mathf.Sin(a), Mathf.Cos(a) * 0.3f);
                var e = Ember(pos, (Cc - pos) * 2.2f + tang * 160, 0.42f, 7, Mathf.Sin(a) > 0 ? Front : Back);
                e.upd = (q, dt, s) => q.vel *= 1 + 1.5f * dt;
            });
            At(0.15f, () => Shake?.Invoke(0.15f));
            var cr = new P { pos = Cc, life = 2.4f, group = Floor, sz = tH };
            cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_2"), Color.white, q.pos, 1.2f * q.sz * 0.42f * Mathf.Min(1, q.age / 0.4f), 1 / 0.42f, 0,
                Mathf.Min(1, (1 - k) / 0.25f));
            Add(cr);
            Ring(Cc, 2.3f, R0 * 2.2f, R0 * 1.6f, Th.ring);
            void Orbit(P q, float dt, HatLua s)
            {
                float a = q.ph + OM * q.age, y = q.vy * q.age, h = Mathf.Min(1, y / HT);
                float R = q.R0 + (q.R1 - q.R0) * Mathf.Pow(h, 0.9f);
                q.pos = Cc + new Vector2(R * Mathf.Cos(a), 0.3f * R * Mathf.Sin(a) - y);
                q.vel = new Vector2(-R * Mathf.Sin(a) * OM, 0.3f * R * Mathf.Cos(a) * OM - q.vy);
                q.group = Mathf.Sin(a) < 0 ? Back : Front;
                q.hgt = h;
            }
            Every(0.25f, T1, x => 62 * Mathf.Min(1, x * 6) * (1 - 0.5f * Mathf.Max(0, (x - 0.85f) / 0.15f)), x =>
            {
                var q = Flame(Cc, Vector2.zero, U(0.6f, 0.8f), 8, 22, "tron", Th.pal, Front, 0, 0, 1.6f, 0.12f, 0.08f);
                Tongue(q, -0.8f, 0.6f);
                q.ph = U(0, 6.28f);
                q.vy = U(230, 300);
                q.R0 = R0;
                q.R1 = R1 * U(0.85f, 1.05f);
                q.upd = Orbit;
                q.smokeGroup = Back;
                q.stretchK = 700;
                q.sizeFn = (z, k) => (8 + 18 * z.hgt) * (z.group == Front ? 0.75f : 1) * (1 - SmoothStep(0.7f, 1, k));
            });
            Every(0.3f, T1, 26, x =>
            {
                var p = new P
                {
                    pos = Cc, life = U(0.55f, 0.7f), ph = U(0, 360), vy = U(220, 280),
                    col = new[] { Pal[Th.pal][1], Pal[Th.pal][2], Pal[Th.pal][0] }[rng.Next(3)]
                };
                p.draw = (q, k, buf) =>
                {
                    float y = q.vy * q.age, h = Mathf.Min(1, y / HT);
                    float R = (R0 + (R1 - R0) * Mathf.Pow(h, 0.9f)) * 1.05f;
                    var c = Cc + new Vector2(0, -y);
                    float a0 = (q.ph + OM * Mathf.Rad2Deg * q.age) % 360;
                    int idx = Mathf.RoundToInt(a0 / 30) % 12;
                    float alpha = Mathf.Min(1, Mathf.Min(k / 0.15f, (1 - k) / 0.25f));
                    // nửa trên elip (phía xa) vẽ sau tướng, nửa dưới vẽ trước
                    Put(buf, Back, 26, S("arcs_" + idx), Ink, c, 2 * R * 0.3f, 1 / 0.3f, 0, alpha, 1);
                    Put(buf, Back, 26.5f, S("arc_" + idx), q.col, c, 2 * R * 0.3f, 1 / 0.3f, 0, alpha, 1);
                    Put(buf, Front, 26, S("arcs_" + idx), Ink, c, 2 * R * 0.3f, 1 / 0.3f, 0, alpha, 2);
                    Put(buf, Front, 26.5f, S("arc_" + idx), q.col, c, 2 * R * 0.3f, 1 / 0.3f, 0, alpha, 2);
                };
                Add(p);
            });
            Every(0.3f, T1, 45, x =>
            {
                var p = new P { pos = Cc, life = U(0.35f, 0.5f), seed = rng.Next(2), ph = U(0, 6.28f), vy = U(200, 320), R0 = R0 * 1.2f, R1 = R1 * 1.1f };
                p.upd = Orbit;
                p.col = Th.spark;
                p.draw = (q, k, buf) => Put(buf, q.group, 40, S("streakg_" + (q.seed & 1)), q.col, q.pos, 9 * (1 - k * k), 3, VelAng(q.vel));
                Add(p);
            });
            Every(0.35f, T1, 7, x =>
            {
                var p = new P
                {
                    pos = Cc, life = U(0.7f, 1.0f), seed = rng.Next(4), ph = U(0, 6.28f), vy = U(120, 200), R0 = R0 * 2, R1 = R1 * 1.25f,
                    sz = U(9, 14), spin = U(-9, 9)
                };
                p.upd = Orbit;
                p.draw = (q, k, buf) => Put(buf, q.group, 45, S("rock_" + (q.seed & 3)), Color.white, q.pos, q.sz * (1 - SmoothStep(0.75f, 1, k)), 1,
                    q.ang * Mathf.Rad2Deg);
                Add(p);
            });
            Every(0.45f, T1 + 0.2f, 20, x => Smoke(Cc + new Vector2(U(-0.8f, 0.8f) * R1, -HT + U(0, 20)), new Vector2(U(-50, 50), -U(40, 80)), 0, 11,
                U(19, 25), Back, "fire"));
            Every(0.35f, T1, 7, x => Extra(Cc + new Vector2(U(-R1, R1) * 0.7f, -U(0.2f, 1.0f) * HT), 1, 160, U(0, 1) < 0.5f ? Front : Back));
            At(0.3f, () => Shake?.Invoke(0.35f));
            return 0.35f;
        }

        // ================= chọn chiêu (dùng chung cho sân đấu và ô xem tướng) =================
        // chiêu mana theo mã ("cau", "kim", "phun", "phun_xoan", "nham"); trả thời gian tới lúc trúng
        public float PlayMana(string kind, Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeFeet, Vector2 foeBody, float tH) =>
            kind switch
            {
                "phun" => Breath(mouth, foeBody, tH, false),
                "phun_xoan" => Breath(mouth, foeBody, tH, true),
                "kim" => Needles(casterFeet, casterH, casterH * 1.1f, foeBody, tH),
                "nham" => LavaBall(mouth, foeFeet, tH, casterFeet.y),
                _ => Fireball(mouth, foeBody, tH),
            };

        // chiêu cuối theo mã ("thien_thach", "phun_nham", "loc_xoay", "no_lon"); fromSide: phía con ra chiêu so với đối thủ (-1 trái, 1 phải)
        public float PlayUlt(string kind, Vector2 foeFeet, Vector2 foeBody, float tH, float fromSide) =>
            kind switch
            {
                "thien_thach" => Meteor(foeFeet, tH, fromSide == 0 ? 1 : fromSide),
                "phun_nham" => Eruption(foeFeet, tH),
                "loc_xoay" => Tornado(foeFeet, tH),
                _ => BigBurst(foeFeet, foeBody, tH),
            };

        // nổ lớn: vòng lửa loang dưới chân, cột lưỡi lửa vọt lên ôm thân (phần lớn sau lưng), rồi chớp sao gai nổ ở thân, nổ phụ
        public float BigBurst(Vector2 feet, Vector2 body, float tH)
        {
            float rx = 0.34f * tH;
            Shake?.Invoke(0.3f);
            Ring(feet + new Vector2(0, 2), 0.4f, 0.15f * tH, 0.95f * tH, Th.ring);
            var cr = new P { pos = feet + new Vector2(0, 2), life = 1.3f, group = Floor, seed = rng.Next(4), sz = tH };
            cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_" + q.seed), Color.white, q.pos, 1.3f * q.sz * 0.42f * Mathf.Min(1, q.age / 0.15f),
                1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.3f));
            Add(cr);
            Every(0, 0.5f, x => 120 * (1 - 0.5f * x), x =>
            {
                float th = U(0, 6.28f);
                bool front = Mathf.Sin(th) > 0.35f;
                var q = Flame(feet + new Vector2(rx * Mathf.Cos(th), 12 * Mathf.Sin(th) - 4), new Vector2(Mathf.Cos(th) * 40, -U(420, 640)), U(0.32f, 0.5f), 9,
                    U(20, 28) * (front ? 0.6f : 1), "tron", Th.pal, front ? Front : Back, 2.2f, -200, 1.7f, 0.1f, 0.15f);
                Tongue(q, 1, 0.5f);
                q.smokeGroup = Back;
            });
            At(0.18f, () =>
            {
                Shake?.Invoke(0.5f);
                Explode(body, 1.15f, tH);
            });
            At(0.34f, () => Explode(body + new Vector2(U(-22, 22), U(-28, 0)), 0.7f, tH));
            At(0.5f, () =>
            {
                for (int i = 0; i < 5; i++) Smoke(body + new Vector2(U(-30, 30), -U(30, 70)), null, 0, 10, 24, Back);
            });
            return 0.18f;
        }

        // thời gian tướng giữ dáng ra chiêu (khung bắn của clip) sau lúc gọi PlayMana: phun tới khi luồng tắt, kim tới khi kim cuối
        // phóng đi, cầu tới khi cầu tụ xong rời miệng
        public static float HoldOf(string kind) =>
            kind != null && kind.StartsWith("phun") ? BreathHold : kind == "kim" ? 1.35f : 0.32f;
    }
}
