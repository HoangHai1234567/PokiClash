// Hạt chồng lớp phẳng trên sân đấu (bộ Hỏa 2026-11-10; chuyển từ ArtGen/Spine/fxlib.py + bo_hoa.py, sổ công thức ở skill
// pokiclash-fx-congthuc). Mỗi hạt mỗi khung trả các "nét vẽ" (nhóm Đất / Sau tướng / Trước tướng, lớp, ảnh, màu, vị trí, cỡ, góc,
// alpha); gom lại, xếp theo (nhóm, lớp) rồi gán lần lượt cho các Image trong hàng chờ của nhóm đó (thứ tự anh em = thứ tự vẽ).
// Ảnh hạt xám vân chì (Assets/03 Art/Fx/Hat, ArtGen/Spine/xuat_hat.py) nhuộm bằng Image.color; không glow, không cộng sáng.
// Toạ độ theo khung sân web (540 x 464, y xuống) như StageView, đổi ra UI bằng StageView.P; thời gian là giây sân.
// Không tạo GameObject lúc chạy (PrefabOnlyTests): Image sinh bằng Ui.Spawn từ prefab Items/HatLua, giữ trong hàng chờ.
// 2026-11-18 (người dùng chê tia cụt, khói rải rác, lửa / dung nham là cầu tròn, nổ chưa đẹp, màu tối): tướng Hỏa dùng các hàm Hoa… (khối "BỘ HỎA
// 2026-11-18" bên dưới: cụm khói tách cụm, nổ kiểu Kingdom Rush 5, cầu lửa nhiều múi, pha tụ xoắn ốc, bông va chạm) và bảng màu tươi "hoa".
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
            public bool flip; // lật ngang ảnh (HatSat.cs: tinh thể của rig khi tướng quay trái)
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
            // suất này nay là Bạch Viêm Hổ (bạch hổ mây lửa, 2026-11-14; HatHo.cs): lửa đỏ cam thường, không mảnh tinh thể (trước: bảng "tinh" + "tinh_the")
            { "hoa_tinh", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42) } },
            // Viêm Dũng (2026-11-14): chiến binh đất nung lõi dung nham, lửa cam, mảnh đá than (trước: cáo đuôi tím hồng, bảng "tim", sao lấp lánh)
            { "huyen_viem", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42), extra = "giap", extraCol = C(74, 62, 60) } },
            // lân đỏ vàng kim, mây xoắn
            { "lan_hoa", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42) } }, // Hỏa Sơn Long (2026-11-15): dung nham cam lõi vàng (trước là Lân Hỏa, bảng vàng + mây)
            // sư tử vàng bờm đỏ: lửa vàng kim, sao vàng
            { "kim_su", new Theme { pal = "vang", smoke = new[] { C(70, 58, 50), C(118, 106, 98), C(170, 162, 154), C(212, 206, 198), C(232, 228, 222) }, spark = C(255, 232, 120), ember = C(255, 206, 70), ring = C(255, 206, 70), extra = "sao", extraCol = C(255, 226, 100) } },
            // suất này nay là pháp sư lửa (Viêm Sư, 2026-11-14): lửa đỏ cam lõi vàng như cầu lửa trên trượng, không mảnh văng (trước là Hồng Liên:
            // rồng sen hồng, pal "sen", cánh sen bay)
            { "hong_lien", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42) } },
            // suất này nay là quỷ lửa cầm đao (Viêm Đao, 2026-11-13): lửa đỏ cam lõi vàng như bờm lửa trên rig, mảnh giáp sắt đen văng ra (trước là
            // Giáp Long: rồng đỏ giáp xám, mảnh giáp xám)
            { "giap_long", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42), extra = "giap", extraCol = C(58, 56, 64) } },
            // bò võ sĩ, mây vàng
            // suất này nay là rùa golem lửa (Hỏa Quy, 2026-11-13): lửa cam thường, mảnh đá bazan xám lam văng ra lúc trúng (trước là Ngưu Quyền: pal "nguu", mây xoắn vàng)
            { "nguu_quyen", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42), extra = "giap", extraCol = C(95, 108, 125) } },
            // người đá than / nham: lửa dung nham, đá
            // mắt lửa bọc giáp (Hỏa Nhãn): lửa đỏ cam lõi vàng như lửa trên rig, mảnh giáp đá vỏ chai đen tím văng ra
            { "hoa_nhan", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42), extra = "giap", extraCol = C(58, 50, 66) } },
            // golem lõi lửa (Nham Thần, 2026-11-13): lửa đỏ cam lõi vàng như lưỡi lửa trên rig (bảng "nham" ra nâu sẫm, lệch màu thân), mảnh đá tro văng ra
            { "nham_than", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42), extra = "giap", extraCol = C(178, 167, 154) } },
            // quỷ lava cầm khiên (Tiểu Quỷ Lava, su_tu_lua; chưa có dòng FireFx: chiêu mana cầu lửa mặc định): lửa tươi, mảnh đá lava sẫm văng ra
            { "su_tu_lua", new Theme { pal = "hoa", spark = C(255, 217, 110), ember = C(255, 164, 58), ring = C(240, 112, 42), extra = "giap", extraCol = C(92, 50, 44) } },
            // tinh linh tinh thể sắt (Thiết Tinh, suất bo_cap đảo Kim, 2026-11-16; HatSat.cs): tia bạc lam, dăm tinh thể tím oải hương
            { "bo_cap", new Theme { pal = "lua", spark = C(226, 232, 248), ember = C(196, 188, 236), ring = C(142, 163, 203), ring2 = C(214, 220, 236), extra = "tinh_the", extraCol = C(167, 159, 211) } },
            // chiến binh sắt khiên giáo (Thiết Vệ, suất doc_giac đảo Kim, 2026-11-16; HatGiao.cs): tia bạc trắng, mảnh giáp thép xám văng ra
            { "doc_giac", new Theme { pal = "lua", spark = C(232, 234, 240), ember = C(200, 204, 214), ring = C(170, 174, 184), ring2 = C(225, 228, 235), extra = "giap", extraCol = C(110, 114, 124) } },
            // tinh linh quặng sắt chui đất (Thiết Khoáng, suất bo_ngua đảo Kim, 2026-11-16; rig ArtGen/Spine/quang_sat_rig.py): tia bạc, than gỉ cam, mảnh quặng sắt đen văng ra
            { "bo_ngua", new Theme { pal = "lua", spark = C(228, 230, 236), ember = C(224, 122, 46), ring = C(150, 140, 132), ring2 = C(214, 208, 200), extra = "giap", extraCol = C(70, 72, 82) } },
            // quỷ béo móc xích lửa (Quỷ Xích, suất khien_bac đảo Kim, 2026-11-16; HatXich.cs): lửa đỏ cam lõi vàng thường (xích lửa, cột lửa), tia lửa vàng, mảnh gang sẫm văng ra
            { "khien_bac", new Theme { pal = "lua", spark = C(255, 214, 120), ember = C(248, 140, 44), ring = C(240, 110, 40), ring2 = C(252, 236, 180), extra = "giap", extraCol = C(86, 90, 100) } },
            // sói chiến binh khiên búa (Sói Giáp, suất chien_than đảo Kim, 2026-11-16; HatSoi.cs): tia trắng ngà, vòng thép, mảnh sắt đen văng ra
            { "chien_than", new Theme { pal = "lua", spark = C(250, 238, 196), ember = C(214, 170, 90), ring = C(170, 174, 184), ring2 = C(225, 228, 235), extra = "giap", extraCol = C(74, 72, 80) } },
            // tinh linh đuôi máy cưa (Thiết Cưa, suất phi_thuong đảo Kim, 2026-11-16; HatCua.cs): tia lửa cưa vàng cam nóng, vòng thép, mảnh đá xám đá phiến văng ra
            { "phi_thuong", new Theme { pal = "lua", spark = C(255, 210, 110), ember = C(248, 140, 44), ring = C(170, 174, 184), ring2 = C(225, 228, 235), extra = "giap", extraCol = C(105, 104, 104) } },
            // kỵ sĩ cổ đại bị nguyền (Vong Kỵ, suất tam_kiem đảo Kim, 2026-11-16; HatHon.cs): lửa linh hồn xanh, khói hồn đen ngả xanh xám, tia xanh nhạt, mảnh giáp sắt rỉ văng ra
            { "tam_kiem", new Theme { pal = "hon", smoke = new[] { C(38, 46, 40), C(84, 102, 86), C(140, 158, 140), C(196, 210, 196) }, spark = C(214, 255, 160), ember = C(150, 230, 90), ring = C(132, 205, 57), ring2 = C(214, 250, 180), extra = "giap", extraCol = C(112, 96, 88) } },
            // robot hủy diệt cổ đại (Thần Cơ, suất thiet_phu đảo Kim, 2026-11-16; HatRobot.cs): năng lượng vàng lõi trắng (cầu, nổ cầu), tia vàng nhạt, mảnh thép sẫm văng ra; nổ tên lửa đổi sang lửa đỏ cam (RbLuaTh)
            { "thiet_phu", new Theme { pal = "nang", spark = C(255, 236, 160), ember = C(255, 196, 80), ring = C(250, 186, 60), ring2 = C(255, 244, 205), extra = "giap", extraCol = C(92, 92, 100) } },
            // thú giáp pháo (Pháo Giáp, suất ung_thep đảo Kim, 2026-11-17; HatPhao.cs): năng lượng vàng (cầu chiêu cuối, nổ cầu), tia vàng, mảnh thép bạc văng ra; đạn sắt và tên lửa nổ lửa đỏ cam (RbLuaTh)
            { "ung_thep", new Theme { pal = "nang", spark = C(255, 236, 160), ember = C(255, 196, 80), ring = C(250, 186, 60), ring2 = C(255, 244, 205), extra = "giap", extraCol = C(170, 176, 188) } },
            // vua robot quyền trượng Mặt Trời (Nhật Vương, suất kim_nghe đảo Kim, 2026-11-17; HatVua.cs): năng lượng Mặt Trời vàng lõi trắng, tia vàng, mảnh giáp vàng văng ra; thiên thạch nổ lửa đỏ cam (VmLuaTh)
            { "kim_nghe", new Theme { pal = "nang", spark = C(255, 238, 170), ember = C(255, 200, 90), ring = C(250, 186, 60), ring2 = C(255, 246, 214), extra = "giap", extraCol = C(232, 178, 58) } },
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

        // Ảnh hạt: trong mảng của bản cài, không có thì lấy từ gói tải sau đã nạp (GD_Claude/27: ảnh chỉ một hệ dùng nằm trong gói của hệ
        // đó). Used (Editor, ContentPack HatScanTour): ghi tên ảnh được dùng để chia gói.
        public static Action<string> Used;

        Sprite S(string name)
        {
            string k = "hat_" + name;
            Used?.Invoke(k);
            if (art.TryGetValue(k, out var s)) return s;
            s = PokiClash.Game.ContentPacks.Get<Sprite>(k);
            if (s) art[k] = s;
            return s;
        }

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
            BeginNuocFx(); // bộ nước shader (HatNuocShader.cs): hạt vẽ hình nước trong lúc draw
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
                rt.localScale = it.flip ? new Vector3(-1, 1, 1) : Vector3.one;
            }
            for (int g = 0; g < 3; g++) HideFrom(g, n[g]);
            FlushMang();
            EndNuocFx();
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
            ClearNuocFx();
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
            { "nham", new[] { C(138, 58, 34), C(240, 112, 42), C(255, 170, 58), C(255, 222, 90) } }, // dung nham (2026-11-18): vỏ nâu đỏ ấm, lõi cam vàng tươi
            { "tinh", new[] { C(196, 30, 42), C(236, 80, 52), C(250, 156, 64), C(255, 232, 196) } },
            { "tim", new[] { C(128, 52, 172), C(208, 84, 192), C(246, 152, 216), C(255, 234, 250) } },
            { "vang", new[] { C(232, 69, 46), C(255, 170, 40), C(255, 222, 80), C(255, 246, 214) } }, // Hỏa Cung (2026-11-18: tươi hơn)
            { "sen", new[] { C(194, 40, 82), C(236, 102, 142), C(250, 182, 172), C(255, 238, 232) } },
            { "nguu", new[] { C(220, 70, 30), C(246, 140, 40), C(255, 200, 70), C(255, 240, 200) } },
            { "hon", new[] { C(70, 150, 50), C(120, 202, 58), C(178, 234, 100), C(236, 255, 200) } }, // lửa linh hồn xanh (Vong Kỵ, HatHon.cs)
            // bộ Hỏa tươi (người dùng 2026-11-18: "màu tươi hơn", sân bãi cát sáng): đỏ tươi E8452E, cam FFA43A, vàng FFD94A, kem FFF6D6 (cam đỏ
            // F0702A dùng cho vòng, tàn lửa); "lua" giữ nguyên cho tướng hệ khác đang mượn lửa
            { "hoa", new[] { C(232, 69, 46), C(255, 164, 58), C(255, 217, 74), C(255, 246, 214) } },
            { "nang", new[] { C(236, 138, 34), C(252, 192, 60), C(255, 232, 140), C(255, 252, 232) } }, // năng lượng vàng lõi trắng (Thần Cơ, HatRobot.cs: RbNang)
        };
        static readonly Color[] SmokeDark = { C(50, 42, 40), C(98, 92, 90), C(152, 148, 146), C(198, 194, 190) };
        static readonly Color[] SmokeFire = { C(240, 140, 50), C(168, 86, 50), C(112, 98, 94), C(160, 156, 152), C(204, 200, 196) };
        static readonly Color[] Lava = { Ink, C(138, 58, 34), C(240, 112, 42), C(255, 170, 58), C(255, 222, 90) }; // vỏ nâu đỏ ấm 8A3A22, lõi cam vàng tươi
        static readonly float[] LavaF = { 1, 1, 0.8f, 0.6f, 0.34f };

        static Color Ramp(Color[] stops, float k)
        {
            k = Mathf.Clamp01(k) * (stops.Length - 1);
            int i = Mathf.Min(stops.Length - 2, (int)k);
            return Color.Lerp(stops[i], stops[i + 1], k - i);
        }

        void Put(List<Item> buf, int g, float layer, Sprite s, Color c, Vector2 pos, float size, float stretch = 1, float ang = 0,
            float alpha = 1, int fill = 0, bool flip = false) =>
            buf.Add(new Item { group = g, layer = layer, sprite = s, color = c, pos = pos, w = size * stretch, h = size, ang = ang, alpha = alpha, fill = fill,
                flip = flip });

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
            if (p.style == "luoi" || p.style == "krl") // lưỡi lửa kiểu tranh tướng: ngọn ngả ngược hướng bay và lên, sọc màu to theo dáng lưỡi
            {
                var d = sp > 30 ? Unit(Unit(p.vel) * (0.5f * p.tip) + new Vector2(0, -p.tipUp)) : new Vector2(0, -1);
                float ang = TipAngle(d);
                // "krl" (bộ Hỏa 2026-11-18): lưỡi chữ S của bộ ảnh mới kr_lua (chân giữa đáy, ngọn chĩa lên); chưa nhập thì lưỡi lobe như cũ
                bool kr = p.style == "krl" && S("kr_lua_0");
                string b = kr ? "kr_lua" : "lobe";
                float s0 = 2.7f * rr[1];
                for (int i = 0; i < 5; i++)
                {
                    float rad = i < 2 ? rr[i] : Mathf.Min(rr[1] * LobeF[i], rr[i] * 1.3f);
                    if (rad < 1) continue;
                    float sz = 2.7f * rad;
                    // kr_lua co lớp quanh CHÂN (điểm neo 0,5; 0,9 của khung): lớp trong lùi về chân cho chân các lớp trùng nhau; bản đặc đã nở sẵn viền
                    var pos = kr ? p.pos - d * 0.4f * (s0 - sz) : p.pos - d * (r - rad) * 0.45f;
                    Put(buf, g, 20 + i, S((i == 0 ? b + "s_" : b + "_") + (p.seed & 3)), i == 0 ? Ink : cols[i - 1], pos, sz + (i == 0 ? (kr ? 3 : 5) : 0), 1, ang);
                }
                return;
            }
            if (p.style == "liem") // lưỡi liềm lửa của vụ nổ (bộ Hỏa 2026-11-18): lưng cong ra ngoài theo p.aim (ảnh kr_liem lưng +x; thay: lưỡi lobe chĩa ra)
            {
                var d = Unit(p.aim);
                bool kr = S("kr_liem_0");
                string b = kr ? "kr_liem" : "lobe";
                float ang = kr ? VelAng(d) : TipAngle(d);
                for (int i = 0; i < 5; i++)
                {
                    float rad = i < 2 ? rr[i] : Mathf.Min(rr[1] * LobeF[i], rr[i] * 1.3f);
                    if (rad < 1) continue;
                    Put(buf, g, 20 + i, S((i == 0 ? b + "s_" : b + "_") + (p.seed & 3)), i == 0 ? Ink : cols[i - 1],
                        kr ? p.pos : p.pos + d * (r - rad) * 0.3f, 2.6f * rad + (i == 0 ? (kr ? 3 : 5) : 0), 1, ang); // kr_liem co lớp quanh tâm
                }
                return;
            }
            if (p.style == "krn") // cụm dung nham mềm (bộ Hỏa 2026-11-18; người dùng chê cầu tròn): ảnh kr_nham, thay bằng giọt kéo đuôi về sau
            {
                bool kr = S("kr_nham_0");
                string b = kr ? "kr_nham" : "drop";
                var d = sp > 5 ? p.vel / sp : new Vector2(0, -1);
                float st = 1 + Mathf.Min(0.8f, sp / p.stretchK);
                float ang = kr ? TipAngle(d) : TipAngle(-d); // kr_nham: đỉnh khung theo hướng bay, giọt kéo (đáy khung) tuột lại sau; drop: đuôi nhọn ra sau
                for (int i = 0; i < 5; i++)
                {
                    float rad = rr[i];
                    if (rad < 1) continue;
                    var c = i == 0 ? Ink : Color.Lerp(Lava[i], Lava[Mathf.Max(1, i - 1)], SmoothStep(0.55f, 1, k)); // nguội dần về vỏ
                    float sz = 2.3f * rad + (i == 0 ? (kr ? 3 : 5) : 0);
                    var pos = kr ? p.pos : p.pos + d * (r - rad) * 0.35f; // kr_nham co lớp quanh tâm
                    Put(buf, g, 20 + i, S((i == 0 ? b + "s_" : b + "_") + (p.seed & 3)), c, pos, sz * st, 1 / st, ang); // kéo dài dọc hướng bay
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
            // giọt dung nham (2026-11-18, người dùng chê "quả cầu tròn"): một GIỌT LỆ kéo dài theo tốc độ, đầu tròn đi trước (ảnh kr_nhamgiot đầu +x;
            // thay: giọt drop đuôi nhọn ra sau), không còn chuỗi ba hạt cườm
            float r = z.r1, sp = z.vel.magnitude;
            var d = sp > 1 ? z.vel / sp : new Vector2(0, 1);
            bool kr = S("kr_nhamgiot_0");
            string b = kr ? "kr_nhamgiot" : "drop";
            float st = 1 + Mathf.Min(0.75f, sp / 600);
            float ang = kr ? VelAng(d) : TipAngle(-d);
            for (int li = 0; li < 5; li++)
            {
                float rad = r * LavaF[li];
                if (rad < 0.8f) continue;
                // kr_nhamgiot co lớp quanh điểm neo (0,66; 0,5) lệch về đầu giọt: lớp trong dồn về đầu tròn
                // ảnh kr_nhamgiot nằm ngang, dày 40 % khung: khung cao 4,6 bán kính cho thân giọt dày gần bằng đường kính
                float fk = kr ? 4.6f : 2.5f;
                var pos = kr ? z.pos + d * 0.16f * st * fk * (r - rad) : z.pos + d * r * (1 - LavaF[li]) * 0.45f;
                float sz = fk * rad + (li == 0 ? (kr ? 3 : 4.5f) : 0);
                var sv = S((li == 0 ? b + "s_" : b + "_") + (z.seed & 3));
                if (kr) Put(buf, z.group, 20 + li, sv, Lava[li], pos, sz, st, ang);
                else Put(buf, z.group, 20 + li, sv, Lava[li], pos, sz * st, 1 / st, ang);
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
                Put(buf, Floor, 6, S("ell"), Color.Lerp(C(240, 112, 42), C(138, 58, 34), Mathf.Min(1, k * 1.4f)), z.pos, z.sz * 0.75f * f, 2.6f);
                Put(buf, Floor, 6.5f, S("ell"), C(255, 217, 74), z.pos, z.sz * 0.4f * Mathf.Max(0, 1 - k / 0.45f), 2.8f);
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
                Put(buf, Floor, 3, S("ell"), Color.Lerp(C(240, 112, 42), C(138, 58, 34), k), q.pos, R * f * a, 3.3f);
                Put(buf, Floor, 4, S("ell"), C(255, 164, 58), q.pos, R * 0.65f * Mathf.Max(0, 1 - k / 0.75f) * a, 3.8f);
                Put(buf, Floor, 4.5f, S("ell"), C(255, 217, 74), q.pos, R * 0.35f * Mathf.Max(0, 1 - k / 0.5f) * a, 4.4f);
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
            Every(0.1f, life * 0.8f, 2.5f, x => HoaKhoi(pos + new Vector2(U(-ax, ax) * 0.6f, -4), U(6, 9), Back, null, U(0.7f, 0.9f), false)); // khói mảnh thành cụm
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

        // =================== BỘ HỎA 2026-11-18: hình và nhịp học Kingdom Rush 5 ===================
        // Người dùng chê (2026-11-18): tia cụt lủn, không va chạm; khói rải rác, chưa thành cụm, chưa mềm; lửa, dung nham là cầu tròn; nổ, sóng âm
        // chưa đẹp; pha hút quanh cầu xấu; màu tối, đốm lửa đơn lẻ, to. Các hàm dưới đây chỉ tướng Hỏa dùng (tên Hoa…) để KHÔNG đổi hiệu ứng của
        // hệ khác đang mượn Explode / Smoke / Ember / CauNo. Ảnh hạt mới tiền tố kr_ (đang vẽ) có thì dùng, chưa nhập thì về hình cũ (không lỗi).

        // điểm trúng (toạ độ sân) và độ mạnh 0..1 mỗi nhịp tia / luồng lửa đang chạm đối thủ: StageView gắn để chớp + giật con đứng ở đó (chưa gắn
        // thì bỏ qua; đề xuất ở Temp/vfx_hoa/BAO_CAO.md)
        public Action<Vector2, float> HoaTrung;

        static readonly Color HoaKem = C(255, 246, 214), HoaVang = C(255, 217, 74), HoaCam = C(255, 164, 58), HoaCamDo = C(240, 112, 42);
        // khói than: đen than ngả xám (người dùng dặn), 5 nấc; tông đáy = Ramp(k), tông đỉnh = Ramp(k + 0,24)
        static readonly Color[] HoaKhoiC = { C(52, 46, 44), C(92, 86, 84), C(142, 138, 136), C(196, 192, 188), C(228, 226, 222) };
        // múi của cụm khói khi chưa có ảnh kr_khoi: chỗ múi (phần bán kính cụm) và cỡ múi
        static readonly Vector2[] HoaMui = { new Vector2(-0.42f, 0.14f), new Vector2(0.42f, 0.18f), new Vector2(0.02f, -0.3f), new Vector2(-0.08f, 0.36f) };
        static readonly float[] HoaMuiR = { 0.6f, 0.56f, 0.68f, 0.5f };

        // ảnh mới nếu đã nhập, không thì ảnh cũ
        Sprite HoaS(string moi, string cu)
        {
            var s = S(moi);
            return s ? s : S(cu);
        }

        static Vector2 HoaXoay(Vector2 v, float a)
        {
            float c = Mathf.Cos(a), s = Mathf.Sin(a);
            return new Vector2(v.x * c - v.y * s, v.x * s + v.y * c);
        }

        // ---------- CỤM KHÓI ----------
        // Một khối nhiều múi (ảnh kr_khoi + bóng đáy kr_khoiday; thay: 3–4 múi sblob chồng nhau), hai tông phẳng: đáy đậm, đỉnh nhạt, một viền mực
        // chung (mọi mực vẽ trước mọi màu). To gần đủ ngay (0,12 đời), bay lên, nhanh dần; ở 48 % đời TÁCH thành 3 cụm nhỏ (kr_khoinho) toả ra, nhỏ
        // dần, có tro, rồi mới mờ (không vụt tắt). lua > 0: đáy cụm còn lõi lửa cam đỏ nguội dần trong 0,2 đời (khói nổ).
        public P HoaKhoi(Vector2 pos, float R, int group = Back, Vector2? vel = null, float life = 0, bool tach = true, float lua = 0)
        {
            if (HasFb("khoi"))
            {
                // khung vẽ sẵn (2026-11-19): cụm khói "khoi" (phồng, bay lên, tan thành mảnh khuyết, một tông nâu xám, nét chì trong) thay khối múi
                // kr_khoi / sblob + ba cụm con. Khung cao 2,3 R (cụm rộng ≈ 0,95 khung), neo chân dưới tâm cụm; chạy hết 24 khung trong đúng `life`
                // (bỏ 2 khung đầu gần như trống); trôi chậm hơn bản hạt vì khung tự bốc lên
                // 2026-11-24 khói Blender: tâm cụm cao cy (0,28) h trên neo (khung GPT cũ 0,45), số khung lấy theo bảng
                var kd = Fbs["khoi"];
                float L = life > 0 ? life : U(1.0f, 1.3f), h = 2.3f * R;
                var f = Fb("khoi", pos + U2(-3, 3) + new Vector2(0, (kd.cy + 0.04f) * h), h, group, 12, (kd.n - 2f) / (kd.fps * Mathf.Max(0.2f, L)), U(-8, 8),
                    U(0, 1) < 0.5f, null, 1, -1, 2);
                if (f != null)
                {
                    f.vel = (vel ?? new Vector2(U(-22, 22), U(-62, -36))) * 0.6f;
                    f.drag = 1.3f;
                    f.acc = new Vector2(0, -16);
                    return f;
                }
            }
            var p = new P
            {
                pos = pos + U2(-3, 3), vel = vel ?? new Vector2(U(-22, 22), U(-62, -36)), life = life > 0 ? life : U(1.0f, 1.3f), drag = 1.3f,
                acc = new Vector2(0, -26), seed = rng.Next(4), ang = U(-0.25f, 0.25f), spin = U(-0.25f, 0.25f), spinDrag = 1.5f, R0 = R, group = group,
                ph = U(0, 6.28f), big = tach, heat = lua, stops = Th.smoke ?? HoaKhoiC
            };
            p.upd = HoaKhoiBay;
            p.draw = HoaVeKhoi;
            return Add(p);
        }

        static float HoaKhoiR(P q, float k)
        {
            if (q.span == 1) return q.R0 * (1 - 0.75f * SmoothStep(0.1f, 1, k));                                       // cụm con: nhỏ dần
            float g = k < 0.12f ? 0.4f + 0.48f * EaseOut(k / 0.12f) : 0.88f + 0.12f * SmoothStep(0.12f, 0.45f, k); // to gần đủ ngay
            g *= q.big ? 1 - 0.7f * SmoothStep(0.46f, 0.74f, k) : 1 - 0.72f * SmoothStep(0.45f, 1, k);              // tách xong cụm mẹ co nhường cụm con
            return q.R0 * g;
        }

        static float HoaKhoiK(P q, float k) => q.span == 1 ? Mathf.Lerp(q.hgt, 1, k) : 0.1f + 0.42f * k; // than đen → xám

        void HoaKhoiBay(P q, float dt, HatLua s)
        {
            float k = q.age / q.life;
            q.vel.x += Mathf.Sin(q.age * 3.4f + q.ph) * 24 * dt;
            q.vel.y -= 55 * k * dt; // càng về cuối càng bay nhanh lên
            if (!q.big || q.hit || k < 0.48f) return;
            q.hit = true;
            float rNow = HoaKhoiR(q, k), con = Mathf.Max(0.45f, q.life - q.age) * 1.2f;
            for (int j = 0; j < 3; j++)
            {
                var o = HoaXoay(HoaMui[j], q.ang);
                var c = new P
                {
                    pos = q.pos + o * rNow, vel = q.vel * 0.6f + Unit(o) * s.U(26, 52) + new Vector2(0, -s.U(14, 34)), life = con * s.U(0.85f, 1.1f),
                    drag = 1.3f, acc = new Vector2(0, -30), seed = (q.seed + j + 1) & 3, ang = q.ang, spin = s.U(-0.4f, 0.4f), spinDrag = 1.2f,
                    R0 = rNow * HoaMuiR[j] * 0.95f, group = q.group, ph = s.U(0, 6.28f), hgt = HoaKhoiK(q, k), span = 1, stops = q.stops, rng = q.rng
                };
                c.upd = s.HoaKhoiBay;
                c.draw = s.HoaVeKhoi;
                if (j == 0) c.onDeath = (z, s2) => s2.Ash(z.pos + s2.U2(-0.4f, 0.4f) * z.R0, null, z.group); // tro tán
                s.Add(c);
            }
        }

        void HoaVeKhoi(P q, float k, List<Item> buf)
        {
            float r = HoaKhoiR(q, k);
            if (r < 1) return;
            float aF, aI;
            if (q.span == 1)
            {
                aF = 1 - SmoothStep(0.6f, 1, k);
                aI = 0.7f * (1 - SmoothStep(0.25f, 0.7f, k));
            }
            else if (q.big)
            {
                aF = 1 - SmoothStep(0.56f, 0.76f, k);
                aI = 0.85f * (1 - SmoothStep(0.4f, 0.66f, k));
            }
            else
            {
                aF = 1 - SmoothStep(0.62f, 1, k);
                aI = 0.85f * (1 - SmoothStep(0.4f, 0.8f, k));
            }
            if (aF < 0.03f) return;
            float kc = HoaKhoiK(q, k);
            Color toi = Ramp(q.stops, kc), sang = Ramp(q.stops, kc + 0.24f);
            if (q.heat > 0 && q.span == 0) toi = Color.Lerp(HoaCamDo, toi, 1 - q.heat * (1 - SmoothStep(0.02f, 0.2f, k))); // lõi lửa nguội trong khói
            int g = q.group;
            float ang = q.ang * Mathf.Rad2Deg;
            string kb = q.span == 1 ? "kr_khoinho" : "kr_khoi";
            var sv = S(kb + "_" + q.seed);
            if (sv)
            {
                if (aI > 0.03f) Put(buf, g, 10, S(kb + "s_" + q.seed), Ink, q.pos, 2 * r + 3, 1, ang, aI); // bản đặc đã nở sẵn viền
                var day = q.span == 0 ? S("kr_khoiday_" + q.seed) : null;
                if (day)
                {
                    Put(buf, g, 11, sv, sang, q.pos, 2 * r, 1, ang, aF);
                    Put(buf, g, 11.5f, day, toi, q.pos, 2 * r, 1, ang, aF);
                }
                else
                {
                    Put(buf, g, 11, sv, toi, q.pos, 2 * r, 1, ang, aF);
                    Put(buf, g, 11.5f, sv, sang, q.pos + new Vector2(0, -0.16f * r), 1.6f * r, 1, ang, aF);
                }
                return;
            }
            int n = q.span == 1 ? 2 : q.R0 < 16 ? 3 : 4;
            float mr = q.span == 1 ? 1.25f : 1;
            for (int pass = 0; pass < (q.span == 1 ? 2 : 3); pass++) // cụm con chỉ một tông (bớt ảnh chồng)
                for (int j = 0; j < n; j++)
                {
                    var o = HoaXoay(HoaMui[j], q.ang) * r;
                    float rl = HoaMuiR[j] * r * mr;
                    int sd = (q.seed + j) & 3;
                    if (pass == 0)
                    {
                        if (aI > 0.03f) Put(buf, g, 10, S("ssolid_" + sd), Ink, q.pos + o, 2 * rl + 4, 1, ang, aI);
                    }
                    else if (pass == 1) Put(buf, g, 11, S("sblob_" + sd), q.span == 1 ? Color.Lerp(toi, sang, 0.5f) : toi, q.pos + o, 2 * rl, 1, ang, aF);
                    else Put(buf, g, 11.5f, S("sblob_" + sd), sang, q.pos + o + new Vector2(0, -0.22f * rl), 1.56f * rl, 1, ang, aF);
                }
        }

        // CỤM TÀN LỬA: 3–6 đốm nhỏ lệch cỡ bay cùng hướng (người dùng: đốm lửa đơn lẻ, to quá; nay cỡ 0,5–0,7 cũ, đi theo cụm)
        public void HoaTan(Vector2 pos, Vector2 vel, float life = 0, int n = 4, int group = Front)
        {
            for (int i = 0; i < n; i++)
                Ember(pos + U2(-6, 6), vel * U(0.82f, 1.15f) + U2(-22, 22), life > 0 ? life * U(0.8f, 1.15f) : 0, i == 0 ? U(6, 7) : U(3.5f, 5.5f), group);
        }

        // CHỚP NỔ phẳng 1–2 khung (tướng Hỏa thay BurstFlash: chớp nước lấy bảng màu NƯỚC): sao gai (kr_chop / burst) viền mực, vàng, lõi kem
        P HoaChop(Vector2 c, float size, float life = 0.09f, int group = Front)
        {
            // khung vẽ sẵn (2026-11-19): chớp = 4–5 khung đầu của "trung_lua" (sao lửa bung, tô phẳng vân chì, không viền mực), cắt ở ~0,15 s rồi mờ
            // nhanh; khung cao 1,6 × size cho sao (≈ 0,6 khung) bằng cỡ sao gai cũ
            if (HasFb("trung_lua"))
                return Fb("trung_lua", c, 1.6f * size, group, 31, 1.3f, U(-20, 20), U(0, 1) < 0.5f, null, 1, Mathf.Max(0.14f, life + 0.06f), 0, 0.07f);
            var f = new P { pos = c, life = life, group = group, seed = rng.Next(4), ang = U(0, 360), sz = size };
            f.draw = (q, k, buf) =>
            {
                float s = q.sz * (0.78f + 0.3f * EaseOut(k / 0.5f));
                Put(buf, q.group, 30, HoaS("kr_chops_" + q.seed, "bursts_" + q.seed), Ink, q.pos, s + (S("kr_chop_0") ? 3 : 6), 1, q.ang);
                Put(buf, q.group, 31, HoaS("kr_chop_" + q.seed, "burst_" + q.seed), HoaVang, q.pos, s, 1, q.ang);
                Put(buf, q.group, 32, HoaS("kr_chop_" + q.seed, "burst_" + q.seed), HoaKem, q.pos, s * 0.58f, 1, q.ang);
            };
            return Add(f);
        }

        // VÒNG CUNG SÓNG DẸT trên đất (KR5; không viền mực: vòng mảnh có viền thì thành vòng đen): nở nhanh rồi chậm, nhạt dần, đứt đoạn
        // (ảnh kr_cung; thay: hai cung đối nhau của hat_arc, hở hai khe)
        P HoaCung(Vector2 feet, float R0, float R1, float life, Color col, float squash = 0.3f, int group = Floor)
        {
            var p = new P { pos = feet, life = life, group = group, col = col, R0 = R0, R1 = R1, hgt = squash, seed = rng.Next(4), span = rng.Next(12) };
            p.draw = (q, k, buf) =>
            {
                float R = q.R0 + (q.R1 - q.R0) * EaseOut(k);
                float a = 0.95f * (1 - SmoothStep(0.4f, 1, k));
                if (a < 0.03f || R < 2) return;
                var kc = S("kr_cung_" + (q.seed & 3));
                if (kc) Put(buf, q.group, 29, kc, q.col, q.pos, 2 * R * q.hgt / 0.36f, 0.36f / q.hgt, 0, a); // ảnh đã dẹt sẵn (cao 36 % khung)
                else
                {
                    Put(buf, q.group, 29, S("arc_" + q.span), q.col, q.pos, 2 * R * q.hgt, 1 / q.hgt, 0, a);
                    Put(buf, q.group, 29, S("arc_" + ((q.span + 6) % 12)), q.col, q.pos, 2 * R * 0.94f * q.hgt, 1 / q.hgt, 0, a);
                }
            };
            return Add(p);
        }

        // VỆT CHÁY trên đất dưới vụ nổ lớn (KR5 decal): elip sẫm phẳng alpha 0,38, giữ khoảng 1 s rồi mờ
        void HoaVetChay(Vector2 feet, float w, float life = 1.9f)
        {
            var p = new P { pos = feet, life = life, group = Floor, sz = w };
            p.draw = (q, k, buf) => Put(buf, Floor, 0.5f, S("ell"), C(74, 52, 44), q.pos, q.sz * 0.3f * Mathf.Min(1, 0.6f + q.age / 0.2f), 1 / 0.3f, 0,
                0.38f * Mathf.Min(1, q.age / 0.06f) * (1 - SmoothStep(0.5f, 1, k)));
            Add(p);
        }

        // đổi hạt lửa sang lưỡi lửa chữ S (style "krl": kr_lua, thay lobe) và bỏ khói lẻ, tàn lẻ khi chết (người dùng: khói rải rác, đốm đơn lẻ):
        // thỉnh thoảng nhả một cụm khói nhỏ sau tướng
        P HoaLuoi(P q, float tip = 1, float up = 0.2f, float khoiP = 0.08f)
        {
            q.style = "krl";
            q.tip = tip;
            q.tipUp = up;
            q.onDeath = khoiP <= 0 ? null : (Action<P, HatLua>)((z, s) =>
            {
                if (z.r1 > 11 && (float)z.rng.NextDouble() < khoiP) s.HoaKhoi(z.pos + new Vector2(0, -4), z.r1 * 0.55f, Back, null, s.U(0.6f, 0.85f), false);
            });
            return q;
        }

        // cỡ lưỡi liềm: bật to trong 0,1 đời rồi teo dần thành đốm (KR5: lưỡi liềm → đốm)
        static float HoaLiemCo(P z, float k) => z.r1 * (k < 0.1f ? 0.55f + 0.45f * EaseOut(k / 0.1f) : 1 - 0.78f * SmoothStep(0.25f, 1, k));

        // ---------- NỔ (học KR5 `explosion_big`) ----------
        // cục chớp nhỏ 2 khung → chớp sao gai; KHỐI KHÓI hai tông to gần đủ ngay (sau tướng, đáy còn lõi lửa nguội) rồi tách cụm bay lên; LƯỠI LIỀM
        // lửa cong ra ngoài cắm trong khói, teo thành đốm; vài lưỡi lửa chữ S bốc lên; tia văng hai đợt cách 0,1 s; cụm tàn lửa; biết chân `dat` thì
        // thêm vòng cung dẹt trên đất (+ vệt cháy khi to). sc 1 ≈ nổ cầu lửa chiêu mana; chớp 0,5·H·sc, nhỏ hơn thân con bị trúng.
        // huong (2026-11-19): hướng đòn bay tới (+1 sang phải, −1 sang trái, 0 chưa biết) để lật khung "trung_lua"
        public void HoaNo(Vector2 c, float sc, float H, Vector2? dat = null, int group = Front, float huong = 0)
        {
            // khung vẽ sẵn (2026-11-19): nổ = "trung_lua" ở thân + (to) quả nổ "no" neo chân sau lưng con bị trúng, thay chớp sao gai + khối khói múi +
            // lưỡi liềm + lưỡi chữ S + vòng cung (HatFbHoa.cs, HoaNoFb)
            if (HasFb("trung_lua"))
            {
                HoaNoFb(c, sc, H, dat, group, huong);
                return;
            }
            float sq = Mathf.Sqrt(sc);
            HoaChop(c, 0.18f * H * sc, 0.07f, group);
            At(0.05f, () => HoaChop(c, 0.5f * H * sc, 0.09f, group));
            // khối khói sau lưng con bị trúng: xoè hình quạt lên trên và sang hai bên để ló ra quanh viền thân ngay (đặt giữa tâm thì bị thân che hết)
            int nk = sc < 0.5f ? 1 : sc < 0.9f ? 2 : 3;
            for (int i = 0; i < nk; i++)
            {
                float a = nk == 1 ? -1.5708f + U(-0.3f, 0.3f) : -2.6f + 2.06f * i / (nk - 1) + U(-0.15f, 0.15f);
                var ve = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                HoaKhoi(c + ve * 0.3f * H * Mathf.Max(0.6f, sc), U(0.14f, 0.18f) * H * Mathf.Max(0.45f, sc), Back, ve * U(45, 75) + new Vector2(0, -U(25, 45)),
                    U(0.95f, 1.25f), sc >= 0.6f, 1);
            }
            int nl = Mathf.Clamp(Mathf.RoundToInt(3 + 3 * sc), 3, 8);
            for (int i = 0; i < nl; i++)
            {
                float a = 6.28f * (i + U(-0.25f, 0.25f)) / nl; // rải đều quanh tâm như cánh hoa, không dồn cục
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.85f);
                var q = Flame(c + d * 0.04f * H * sc, d * U(240, 360) * sq, U(0.24f, 0.32f), 8 * sc, U(14, 19) * sc, "liem", Th.pal,
                    sc >= 1 && (i & 1) == 1 ? Back : group, 8, -50, 1.5f, 0, 0);
                q.aim = d;
                q.sizeFn = HoaLiemCo;
            }
            int nt = sc < 0.5f ? 1 : 2;
            for (int i = 0; i < nt; i++)
                HoaLuoi(Flame(c + U2(-6, 6) * sc, new Vector2(U(-60, 60), -U(160, 260)) * sq, U(0.28f, 0.38f), 7 * sc, U(14, 18) * sc, "tron", Th.pal,
                    group, 3, -200, 1.6f, 0, 0), 1, 0.5f, 0);
            int s1 = Mathf.RoundToInt(2 + 2 * sc), s2 = Mathf.RoundToInt(1 + 2 * sc);
            for (int i = 0; i < s1; i++) Spark(c + U2(-6, 6), U2(-1, 1), U(300, 480) * sq, 0, 7);
            At(0.1f, () =>
            {
                for (int i = 0; i < s2; i++) Spark(c + U2(-6, 6), U2(-1, 1), U(260, 420) * sq, 0, 6);
            });
            HoaTan(c, new Vector2(U(-60, 60), -U(90, 150)), 0, sc < 0.6f ? 3 : 4);
            if (dat.HasValue)
            {
                HoaCung(dat.Value + new Vector2(0, 2), 0.12f * H * sc, 0.75f * H * sc, 0.42f, Th.ring);
                if (sc >= 0.8f) HoaVetChay(dat.Value + new Vector2(0, 2), 0.55f * H * sc);
            }
            if (sc >= 0.6f) Ash(c + U2(-18, 18), new Vector2(U(-70, 70), -U(110, 160)));
            Extra(c, Mathf.RoundToInt(1 + 2 * sc), 300 * sc, group);
        }

        // vụ nổ lớn lúc cầu lửa chạm (tướng Hỏa thay CauNo; CauNo giữ nguyên cho hệ Kim đang dùng): HoaNo + quạt lưỡi lửa theo hướng bay
        // (phần lớn sau lưng đối thủ, không che nó)
        void HoaCauNo(Vector2 tgt, Vector2 foeFeet, float tH, float dir, float sc)
        {
            Shake?.Invoke(0.5f * sc);
            HoaNo(tgt, sc, tH, foeFeet, Front, dir);
            if (HasFb("trung_lua")) return; // khung vẽ sẵn (2026-11-19): "trung_lua" đã toé lửa theo hướng bay, bỏ quạt lưỡi lửa
            int n = Mathf.RoundToInt(3 + 2 * sc);
            for (int i = 0; i < n; i++)
            {
                float a = (i - (n - 1) * 0.5f) * 0.32f + U(-0.08f, 0.08f);
                var d = new Vector2(dir * Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                HoaLuoi(Flame(tgt + d * U(4, 10), d * U(240, 400) * Mathf.Sqrt(sc), U(0.26f, 0.36f), 8, U(15, 21) * Mathf.Sqrt(sc), "tron", Th.pal,
                    i % 3 == 1 ? Front : Back, 4.2f, -160, 1.5f, 0, 0), 1, 0.15f, 0.12f);
            }
        }

        // ---------- CẦU LỬA và PHA TỤ ----------
        // KHỐI CẦU LỬA nhiều múi cuộn bám điểm chạy tam(giờ sân), bán kính rt(giờ sân) (đã gồm nhịp đập, cú nén): MỘT hạt thay chùm LoiCau (≈13 hạt
        // tròn × 5 lớp). Ảnh kr_luakhoi / kr_cau; thay: lõi tròn + sáu múi lửa quanh vành ngọn chĩa ra ngoài, quay chậm, đổi dáng 15 hình/giây.
        P HoaCau(Func<float, Vector2> tam, Func<float, float> rt, float life, int group = Front)
        {
            var p = new P
            {
                pos = tam(T), life = life, group = group, seed = rng.Next(4), ang = U(0, 6.28f), spin = U(0, 1) < 0.5f ? -3.2f : 3.2f, stops = Pal[Th.pal]
            };
            p.upd = (q, dt, s) =>
            {
                q.pos = tam(s.T);
                q.vel = Vector2.zero;
            };
            p.draw = (q, k, buf) => HoaVeCau(q, rt(T), buf);
            return Add(p);
        }

        void HoaVeCau(P q, float r, List<Item> buf)
        {
            if (r < 1.5f) return;
            var cols = q.stops;
            int g = q.group, fr = (q.seed + (int)(q.age * 15)) & 3; // đổi dáng mỗi 2 khung
            float ang = q.ang * Mathf.Rad2Deg;
            string kb = S("kr_luakhoi_0") ? "kr_luakhoi" : S("kr_cau_0") ? "kr_cau" : null;
            if (kb != null)
            {
                Put(buf, g, 20, S(kb + "s_" + fr), Ink, q.pos, 2 * r + 3, 1, ang);
                Put(buf, g, 21, S(kb + "_" + fr), cols[0], q.pos, 2 * r, 1, ang);
                Put(buf, g, 22, S(kb + "_" + ((fr + 1) & 3)), cols[1], q.pos, 1.64f * r, 1, -ang);
                Put(buf, g, 23, S(kb + "_" + ((fr + 2) & 3)), cols[2], q.pos, 1.16f * r, 1, ang * 1.4f);
                Put(buf, g, 24, S(kb + "_" + ((fr + 3) & 3)), cols[3], q.pos, 0.66f * r, 1, 0);
                return;
            }
            for (int pass = 0; pass < 2; pass++)
            {
                var c = pass == 0 ? Ink : cols[0];
                float ext = pass == 0 ? 5 : 0;
                Put(buf, g, 20 + pass, S((pass == 0 ? "solid_" : "blob_") + fr), c, q.pos, 1.72f * r + ext, 1, ang);
                for (int j = 0; j < 6; j++)
                {
                    float th = q.ang + j * 1.047f + 0.25f * Mathf.Sin(q.age * 7 + j * 2.1f);
                    var o = new Vector2(Mathf.Cos(th), Mathf.Sin(th));
                    var d = Unit(o + new Vector2(0, -0.55f)); // ngọn chĩa ra ngoài, ngả lên
                    float s = r * (1.05f + 0.18f * Mathf.Sin(q.age * 11 + j * 1.7f));
                    Put(buf, g, 20 + pass, S((pass == 0 ? "lobes_" : "lobe_") + ((fr + j) & 3)), c, q.pos + o * r * 0.5f, s + ext, 1, TipAngle(d));
                }
            }
            Put(buf, g, 22, S("blob_" + ((fr + 1) & 3)), cols[1], q.pos, 1.5f * r, 1, -ang);
            Put(buf, g, 23, S("blob_" + ((fr + 2) & 3)), cols[2], q.pos, 1.04f * r, 1, ang);
            Put(buf, g, 24, S("blob_" + ((fr + 3) & 3)), cols[3], q.pos + new Vector2(0, 0.1f * r), 0.56f * r, 1, 0);
        }

        // VỆT BỊ HÚT vào cầu: vệt thuôn (kr_vet đầu tròn +x; thay: streakg) sinh ở `tu`, hiện dần từ trong suốt, bay XOẮN ỐC vào tâm và nhanh dần
        // (ease-in), chạm vành cầu thì nhập vào (không tắt giữa đường); quá `het` (giờ sân tuyệt đối: cầu đã rời chỗ) thì tắt
        P HoaHut(Func<float, Vector2> tam, Func<float, float> rt, Vector2 tu, float life, Color col, float chieu, float het, int group = Front)
        {
            var o = tu - tam(T);
            var p = new P
            {
                pos = tu, life = life, group = group, seed = rng.Next(2), col = col, R0 = Mathf.Max(8, o.magnitude), ph = Mathf.Atan2(o.y, o.x),
                tip = chieu * U(1.5f, 2.4f), sz = U(5, 7.5f), launch = het, aim = new Vector2(-o.y, o.x) * chieu
            };
            p.upd = (q, dt, s) =>
            {
                if (s.T > q.launch)
                {
                    q.dead = true;
                    return;
                }
                float k = Mathf.Clamp01(q.age / q.life);
                float e = k * k * (0.35f + 0.65f * k); // nhanh dần
                float rho = q.R0 * (1 - e), a = q.ph + q.tip * e;
                var np = tam(s.T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * rho;
                var mv = np - q.pos;
                if (mv.sqrMagnitude > 1e-4f)
                {
                    q.aim = mv;
                    q.hgt = mv.magnitude / Mathf.Max(1e-4f, dt);
                }
                q.pos = np;
                q.vel = Vector2.zero;
                if (rho <= rt(s.T) * 0.9f) q.dead = true; // nhập vào cầu
            };
            p.draw = (q, k, buf) =>
            {
                float a = Mathf.Min(1, k / 0.25f);
                float len = Mathf.Clamp(q.hgt / 70, 1.3f, 4.2f), ang = VelAng(q.aim);
                var kv = S("kr_vet_" + (q.seed & 1));
                if (kv)
                {
                    // ảnh kr_vet nằm ngang dài 90 % khung, dày 22 %: khung cao sz / 0,22 cho vệt dày sz, dài sz · len
                    float h = q.sz / 0.22f, st = 0.244f * len;
                    Put(buf, q.group, 40, S("kr_vets_" + (q.seed & 1)), Ink, q.pos, h + 3, st * h / (h + 3), ang, a * 0.9f);
                    Put(buf, q.group, 40.5f, kv, q.col, q.pos, h, st, ang, a);
                }
                else
                {
                    Put(buf, q.group, 40, S("streakg_" + (q.seed & 1)), q.col, q.pos, q.sz, len, ang, a);
                    Put(buf, q.group, 40.5f, S("streakg_" + (q.seed & 1)), HoaKem, q.pos + Unit(q.aim) * q.sz * len * 0.18f, q.sz * 0.5f, len * 0.6f, ang, a);
                }
            };
            return Add(p);
        }

        // VÒNG CO về tâm cầu (không viền mực), hiện dần, co nhanh dần tới vành cầu
        P HoaVongCo(Func<float, Vector2> tam, float R0, float R1, float life, Color col, int group = Front)
        {
            var p = new P { pos = tam(T), life = life, group = group, col = col, R0 = R0, R1 = R1 };
            p.upd = (q, dt, s) =>
            {
                q.pos = tam(s.T);
                q.vel = Vector2.zero;
            };
            p.draw = (q, k, buf) => Put(buf, q.group, 36, S("ring"), q.col, q.pos, 2 * Mathf.Lerp(q.R0, q.R1, k * k), 1, 0, 0.9f * Mathf.Min(1, k / 0.3f));
            return Add(p);
        }

        // PHA TỤ CẦU dùng chung (người dùng 2026-11-18: "các skill hút khí / lửa xung quanh tụ cầu xấu"), từ t0 tới tNha (giây từ lúc gọi):
        // - vệt thuôn xoắn ốc vào tâm, nhanh dần, hiện dần, nhập vào cầu; mật độ tăng dần tới lúc nhả;
        // - hai vòng co về tâm; cầu (HoaCau) lớn dần theo căn tiến độ, đập ~4 nhịp/giây; 0,07 s trước lúc nhả nén còn 0,78; lúc nhả chớp.
        // veCau false: cầu là mảnh của rig (Viêm Sư), chỉ vẽ phần hút, rtRig = bán kính cầu của rig; hut: hệ số mật độ vệt (0 = không sinh vệt).
        // Trả bán kính cầu theo giờ sân tuyệt đối (lưỡi lửa liếm bám vành, cầu bay nhận cỡ).
        // huong (2026-11-19): phía đối thủ (±1) để đuôi lửa của cầu vẽ sẵn ngả về trước, khỏi trùm mặt tướng
        Func<float, float> HoaTuCau(Func<float, Vector2> tam, float R, float t0, float tNha, bool veCau = true, float hut = 1, Func<float, float> rtRig = null,
            float huong = 0)
        {
            float a0 = T + t0, a1 = T + tNha;
            Func<float, float> rt = rtRig ?? (t =>
            {
                float nap = Mathf.Clamp01((t - a0) / Mathf.Max(0.05f, a1 - a0));
                // phập phồng 7 Hz ±6 % (2026-11-19 đêm, người dùng: cầu "nhìn hơi tĩnh"; trước 4 Hz ±7 %)
                float r = R * (0.25f + 0.75f * Mathf.Sqrt(nap)) * (1 + 0.06f * Mathf.Sin((t - a0) * 44));
                float con = a1 - t;
                if (con >= 0 && con < 0.07f) r *= Mathf.Lerp(0.78f, 1, con / 0.07f); // nén 1–2 khung trước lúc nhả
                return r;
            });
            // khung vẽ sẵn: cầu đang tụ là "cau_tu" (2026-11-19 đêm: lửa cuộn xoáy quanh lõi, bù cỡ từng khung, xoay chậm, lớn dần theo rt) + tàn lửa
            // xoắn vào; chưa nhập "cau_tu" thì "cau_lua" đứng yên (mũi chúc xuống, đuôi lửa bốc lên); lúc nhả có chớp che chỗ đổi sang cầu bay
            bool cauTu = veCau && HasFb("cau_tu");
            if (veCau)
                At(t0, () =>
                {
                    if (HoaFbCauTu(tam, rt, tNha - t0 + 0.01f) == null && HoaFbCau(tam, rt, tNha - t0 + 0.01f, Front, false, huong) == null)
                        HoaCau(tam, rt, tNha - t0 + 0.01f);
                });
            var pc = Pal[Th.pal];
            float chieu = U(0, 1) < 0.5f ? 1 : -1;
            if (cauTu)
                Every(t0, tNha - 0.05f, x => 8 + 12 * x, x =>
                {
                    float a = U(0, 6.28f), rho = rt(T) * U(2.4f, 3.4f) + U(16, 34);
                    HoaTanXoan(tam, rt, tam(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * rho, U(0.3f, 0.42f), chieu, a1 + 0.02f);
                });
            if (hut > 0)
                Every(t0, tNha - 0.05f, x => (22 + 60 * x * x) * hut, x =>
                {
                    float a = U(0, 6.28f), rho = rt(T) * U(2.2f, 3.2f) + U(14, 30);
                    HoaHut(tam, rt, tam(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * rho, U(0.24f, 0.34f), U(0, 1) < 0.5f ? pc[2] : pc[1], chieu, a1 + 0.02f);
                });
            for (int i = 0; i < 2; i++)
                At(t0 + (tNha - t0) * (0.3f + 0.42f * i), () => HoaVongCo(tam, rt(T) * 2.6f + 16, rt(T) * 1.05f, 0.22f, Th.ring2));
            At(tNha, () => HoaChop(tam(T), 2.4f * (rtRig != null ? rtRig(T) : R), 0.08f));
            return rt;
        }

        // ---------- VA CHẠM của tia / luồng lửa ----------
        // BÔNG VA CHẠM ở chỗ tia chạm thân đối thủ: toé ngược về phía người bắn (ảnh kr_tiadau toé về +x; thay: sao gai nhỏ + ba lưỡi lửa xoè quanh
        // hướng toé), đổi dáng mỗi 2 khung, cỡ đập; mở 0,06 s, khép 0,1 s cuối đời
        P HoaBong(Vector2 at, Vector2 ve, float size, float life, int group = Front)
        {
            var p = new P { pos = at, aim = Unit(ve), life = life, group = group, sz = size, seed = rng.Next(4), stops = Pal[Th.pal] };
            p.draw = (q, k, buf) =>
            {
                float mo = EaseOut(q.age / 0.06f) * (1 - SmoothStep(Mathf.Max(0, 1 - 0.1f / q.life), 1, k));
                int fr = (q.seed + (int)(q.age * 15)) & 3;
                float s = q.sz * mo * (0.88f + 0.16f * Mathf.Sin(q.age * 38));
                if (s < 2) return;
                var c = q.stops;
                int g = q.group;
                if (S("kr_tiadau_0"))
                {
                    // kr_tiadau: gốc toé ở mép trái khung (điểm neo 0,055; 0,5) đặt đúng chỗ chạm, toé ngược về phía người bắn (+x theo q.aim)
                    float ang = VelAng(q.aim) + 14 * Mathf.Sin(q.age * 23);
                    var ve = HoaXoay(q.aim, -14 * Mathf.Sin(q.age * 23) * Mathf.Deg2Rad);
                    Put(buf, g, 33, S("kr_tiadaus_" + fr), Ink, q.pos + ve * 0.445f * (s + 3), s + 3, 1, ang);
                    for (int i = 0; i < 4; i++)
                    {
                        float w = s * LobeF[i + 1];
                        Put(buf, g, 33.1f + 0.1f * i, S("kr_tiadau_" + fr), c[i], q.pos + ve * 0.445f * w, w, 1, ang);
                    }
                    return;
                }
                for (int i = 0; i < 4; i++) // ba lưỡi lửa xoè (giữa dài, hai bên ngắn), mực trước, màu từ ngoài vào lõi
                    for (int j = -1; j <= 1; j++)
                    {
                        var d = HoaXoay(q.aim, j * (0.85f + 0.12f * Mathf.Sin(q.age * 31 + j)));
                        float L = s * (j == 0 ? 0.7f : 0.52f) * (i == 0 ? 1 : LobeF[i]);
                        Put(buf, g, 33 + 0.1f * i, S((i == 0 ? "lobes_" : "lobe_") + ((fr + j + 1) & 3)), i == 0 ? Ink : c[i - 1], q.pos + d * s * 0.22f,
                            L + (i == 0 ? 5 : 0), 1, TipAngle(d));
                    }
                Put(buf, g, 33.5f, S("bursts_" + fr), Ink, q.pos, s * 0.5f + 5, 1, q.age * 300);
                Put(buf, g, 33.6f, S("burst_" + fr), c[2], q.pos, s * 0.5f, 1, q.age * 300);
                Put(buf, g, 33.7f, S("burst_" + fr), c[3], q.pos, s * 0.3f, 1, q.age * 300);
            };
            return Add(p);
        }

        // KHÓI ĐUÔI theo QUÃNG đạn đã đi (KR5: số hạt theo quãng đường nên đuôi liền dù đạn nhanh): cứ khoảng 1,4 bán kính một cụm khói nhỏ đứng
        // tại chỗ (sau tướng, đáy còn lõi lửa nguội), các cụm chồng mép nhau thành một vệt; pos(giờ sân tuyệt đối) là chỗ sinh
        void HoaDuoiKhoi(Func<float, Vector2> pos, float t0, float t1, float R0, float R1)
        {
            // khung vẽ sẵn (2026-11-19 chiều): cầu bay "cau_lua" tự nhả vệt khói đuôi (HoaFbCau → FbKhoiDuoi của HatFlip.cs), nên ở đây thôi
            if (HasFb("khoi") && HasFb("cau_lua")) return;
            var truoc = new Vector2(float.NaN, 0);
            float buoc = 0.7f * (R0 + R1); // cụm sau chồng nửa cụm trước
            Every(t0, t1, 120, x =>
            {
                var p = pos(T);
                if (!float.IsNaN(truoc.x) && (p - truoc).sqrMagnitude < buoc * buoc) return;
                truoc = p;
                HoaKhoi(p + U2(-3, 3), U(R0, R1), Back, new Vector2(U(-12, 12), U(-34, -14)), U(0.5f, 0.7f), false, 0.7f);
            });
        }

        // LỬA BÁM trên thân đối thủ sau cú trúng (KR5 "mod"): ảnh chùm 3–5 ngọn lửa con kr_luachum (mực + cam, rồi lớp vàng kr_luachuml cùng khung),
        // đổi khung 15 hình/giây, phập phồng, nhỏ dần rồi tắt, vài giọt lửa tách bay lên; chưa có ảnh thì lưỡi lửa chữ S sinh liên tục tại chỗ
        void HoaLuaBam(Vector2 at, float r, float dai, int group = Front)
        {
            // khung vẽ sẵn (2026-11-19): cụm lửa cháy lặp "lua_lap" chân ở `at` (cao 2,8 r như chùm cũ), nhỏ dần nửa sau rồi tắt; bỏ lưỡi lửa tách
            if (HoaFbLua(at, 2.8f * r, dai, group, 22, 0.08f, 0.5f) != null) return;
            if (S("kr_luachum_0"))
            {
                var p = new P { pos = at, life = dai, group = group, seed = rng.Next(4), sz = r * 2.6f, stops = Pal[Th.pal] };
                p.draw = (q, k, buf) =>
                {
                    int fr = (q.seed + (int)(q.age * 15)) & 3;
                    float s = q.sz * Mathf.Min(1, q.age / 0.08f) * (1 - 0.55f * SmoothStep(0.5f, 1, k)) * (1 + 0.06f * Mathf.Sin(q.age * 30));
                    float a = 1 - SmoothStep(0.85f, 1, k);
                    if (s < 2 || a < 0.03f) return;
                    var pos = q.pos - new Vector2(0, s * 0.42f); // chân chùm ở `at`
                    Put(buf, q.group, 22, S("kr_luachums_" + fr), Ink, pos, s + 3, 1, 0, a);
                    Put(buf, q.group, 22.3f, S("kr_luachum_" + fr), q.stops[1], pos, s, 1, 0, a);
                    Put(buf, q.group, 22.6f, S("kr_luachuml_" + fr), q.stops[2], pos, s, 1, 0, a);
                };
                Add(p);
                Every(0.1f, dai * 0.8f, 4, x => HoaLuoi(Flame(at + new Vector2(U(-0.3f, 0.3f) * r, -U(0.6f, 1f) * r), new Vector2(U(-15, 15), -U(60, 110)),
                    U(0.2f, 0.3f), r * 0.2f, r * 0.35f, "tron", Th.pal, group, 2, -200, 1.5f, 0, 0), 1, 0.8f, 0));
                return;
            }
            Every(0, dai, x => 9 * (1 - 0.6f * x), x =>
                HoaLuoi(Flame(at + U2(-4, 4), new Vector2(U(-14, 14), -U(40, 90)), U(0.24f, 0.34f), r * 0.45f, r * (1 - 0.4f * x), "tron", Th.pal, group, 2,
                    -200, 1.5f, 0, 0), 1, 0.7f, 0));
        }

        // Hỏa Cung (cung_lua, suất kim_su): chiêu mana bắn ba mũi tên CỦA RIG (xương far / fly_*), gọi đúng khung tên tới nên chỉ làm ba
        // chớp nổ nhỏ so le ở thân đối thủ (giữa, trên, dưới: đúng chỗ ba mũi tên găm); trả 0 vì đã trúng.
        public float TenNo(Vector2 body, float tH, Vector2? tu = null, Vector2? dat = null)
        {
            float dir = tu.HasValue && tu.Value.x > body.x ? -1 : 1; // hướng tên bay (từ người bắn tới đối thủ)
            Shake?.Invoke(0.2f);
            var cho = new[] { body, body + new Vector2(0, -0.1f * tH), body + new Vector2(-dir * 0.04f * tH, 0.1f * tH) };
            for (int i = 0; i < 3; i++)
            {
                var c = cho[i];
                bool dau = i == 0;
                At(0.05f * i, () =>
                {
                    HoaTrung?.Invoke(c, dau ? 0.5f : 0.3f);
                    HoaNo(c, dau ? 0.5f : 0.36f, tH, dau ? dat : null, Front, dir); // khung vẽ sẵn (2026-11-19): "trung_lua" lật theo hướng tên
                    // lửa toé tiếp theo hướng tên (quạt ba lưỡi, hai lưỡi bên sau lưng đối thủ), tia văng ngược về phía người bắn; có khung vẽ sẵn
                    // thì "trung_lua" đã toé theo hướng tên, bỏ quạt
                    for (int j = 0; j < (HasFb("trung_lua") ? 0 : 3); j++)
                    {
                        var d = new Vector2(dir * Mathf.Cos((j - 1) * 0.45f), Mathf.Sin((j - 1) * 0.45f) - 0.25f);
                        HoaLuoi(Flame(c + d * 4, d * U(200, 320), U(0.22f, 0.3f), 6, U(12, 16), "tron", Th.pal, j == 1 ? Front : Back, 4, -160, 1.5f, 0, 0), 1,
                            0.2f, 0);
                    }
                    if (dau)
                        for (int j = 0; j < 3; j++) Spark(c, new Vector2(-dir * U(0.4f, 1f), U(-0.8f, 0.4f)), U(220, 380), 0, 6);
                    HoaLuaBam(c + new Vector2(0, -4), dau ? 13 : 10, 0.7f); // lửa còn bám chỗ tên găm (KR5 "mod")
                });
            }
            At(0.32f, () => HoaKhoi(body + new Vector2(0, -0.2f * tH), 0.14f * tH, Back, null, 1.1f));
            return 0;
        }

        // ================= CHIÊU MANA (thay tia nước) =================
        // trả thời gian tới lúc trúng (giây sân)

        // thời gian tướng phải giữ dáng phun từ lúc gọi Breath tới khi luồng lửa tắt (T1 + đuôi)
        public const float BreathHold = 1.22f;

        public float Breath(Vector2 mouth, Vector2 target, float tH, bool swirl)
        {
            if (HasFb("phun")) return BreathFb(mouth, target, tH, swirl); // bộ lửa Blender 2026-11-24 (HatFbHoa.cs); dưới đây là bản hạt cũ
            // người dùng 2026-11-10: lửa phun phải hợp nét tranh tướng -> lưỡi lửa vẽ tay; 2026-11-18: lưỡi chữ S (krl), luồng dừng ở MẶT TRƯỚC thân
            // đối thủ và toé dạt quanh thân (bông va chạm), khói thành cụm
            string style = "krl", pal = Th.pal;
            var dd = target - mouth;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            var up = nrm.y < 0 ? nrm : -nrm;
            const float T0 = 0.28f, T1 = 1.18f;
            float Hit = Mathf.Max(34, 0.26f * tH);
            var cham = mouth + u * (dist - Hit);
            float chieu = U(0, 1) < 0.5f ? 1 : -1;
            // lấy hơi: vệt thuôn xoắn ốc vào miệng, nhanh dần
            Every(0, 0.22f, 36, x =>
            {
                float a = U(0, 6.28f);
                HoaHut(t => mouth, t => 7, mouth + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(50, 82), U(0.18f, 0.24f), Pal[pal][U(0, 1) < 0.5f ? 1 : 2], chieu,
                    T + 0.3f);
            });
            Every(0.06f, T0, 30, x => Flame(mouth + U2(-4, 4), u * 25, 0.22f, 4, 10 + 26 * x, style, pal, Front, 1.8f, -320, 1, 0, 0));
            Every(T0, T1, x => 95 * (x < 0.11f ? 1.5f : 1f) * Mathf.Min(1, (1 - x) * (T1 - T0) / 0.16f), x =>
            {
                float a = U(-1, 1) * 12 * Mathf.Deg2Rad;
                var dv = u * Mathf.Cos(a) + nrm * Mathf.Sin(a);
                float ramp = Mathf.Min(1, x * (T1 - T0) / 0.08f);
                var p = Flame(mouth + dv * U(0, 8), dv * U(1200, 1400), U(0.4f, 0.52f), U(13, 16), U(28, 36) * (0.8f + 0.2f * ramp), style, pal,
                    Front, 1.8f, -320, 1, 0, 0);
                p.upd = (q, dt, s) =>
                {
                    float k = q.age / q.life;
                    q.vel += nrm * Mathf.Sin(q.age * 17 + q.spin) * 260 * k * dt;
                    if (!q.hit && Vector2.Dot(q.pos - mouth, u) > dist - Hit)
                    {
                        q.hit = true;
                        float vu = Vector2.Dot(q.vel, u);
                        float side = Vector2.Dot(q.pos - mouth, nrm) >= 0 ? 1 : -1;
                        q.vel += -u * vu * 0.92f + nrm * side * Mathf.Abs(vu) * U((System.Random)q.rng, 0.18f, 0.36f);
                        float rNow = q.r0 + (q.r1 - q.r0) * Mathf.Pow(EaseOut(k / 0.75f), 0.8f);
                        q.life = Mathf.Min(q.life, q.age + U((System.Random)q.rng, 0.1f, 0.16f));
                        q.r1 = Mathf.Min(q.r1, rNow * 1.05f);
                        q.r0 = Mathf.Min(q.r0, q.r1);
                        q.acc = Vector2.zero;
                        q.group = q.rng.NextDouble() < 0.55 ? Back : Front; // dạt quanh viền thân, không trùm mặt đối thủ
                    }
                };
            });
            // khói thành cụm từ mép trên luồng (sau tướng)
            Every(T0, T1, 4.5f, x =>
            {
                if (x < 0.12f) return;
                float f = U(0.45f, 0.95f);
                HoaKhoi(mouth + u * dist * f + up * U(18, 30) * (0.6f + f), U(11, 15) * (0.8f + 0.4f * f), Back, new Vector2(U(-20, 20), U(-60, -36)) - u * 16);
            });
            Every(T0, T1, 8, x =>
            {
                float f = U(0.25f, 0.8f), sd = U(0, 1) < 0.5f ? -1 : 1;
                var pos = mouth + u * dist * f + nrm * sd * U(18, 30) * (0.5f + f);
                Spark(pos, u * U(0.5f, 1) + nrm * sd * U(0.4f, 0.9f) + new Vector2(0, -0.3f), U(260, 420), 0, 7);
            });
            if (swirl || Th.extra == "may") // Lân Hỏa, Ngưu Quyền: mây xoắn vàng bay dọc luồng
                Every(T0 + 0.1f, T1, 10, x => Extra(mouth + u * dist * U(0.3f, 0.9f) + up * U(10, 30), 1, 120));
            float tHit = T0 + 0.24f;
            // VA CHẠM: chớp + bông lửa toé ngược ở mặt trước thân suốt luồng, lửa dạt dọc mặt thân, đối thủ chớp theo nhịp
            At(tHit, () =>
            {
                Shake?.Invoke(0.25f);
                HoaChop(cham, 0.36f * tH, 0.09f);
                HoaBong(cham, -u, 0.5f * tH, T1 - tHit + 0.06f);
                for (int i = 0; i < 4; i++)
                {
                    float a = Mathf.Atan2(-u.y, -u.x) + U(-1.4f, 1.4f);
                    Spark(target + U2(-10, 10), new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.5f), U(250, 460), 0, 7);
                }
                Extra(target, 3, 300);
            });
            Every(tHit, T1, 20, x =>
            {
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                var v = (-u * U(0.15f, 0.55f) + nrm * sd * U(0.7f, 1f) + new Vector2(0, -0.35f)) * U(260, 420);
                HoaLuoi(Flame(cham + nrm * sd * U(4, 14), v, U(0.2f, 0.28f), 7, U(14, 19), "tron", pal, U(0, 1) < 0.5f ? Back : Front, 3.5f, -200, 1.4f, 0, 0), 1,
                    0.3f, 0.06f);
            });
            Every(tHit, T1, 5, x => HoaTrung?.Invoke(target, 0.3f));
            At(T1 - 0.05f, () =>
            {
                for (int i = 0; i < 2; i++) HoaKhoi(mouth + u * dist * U(0.5f, 0.85f) + up * U(10, 22), U(14, 18), Back);
                HoaKhoi(cham + new Vector2(0, -0.2f * tH), U(15, 19), Back, null, 0, true, 0.6f);
                for (int i = 0; i < 4; i++) Ash(target + U2(-30, 30));
            });
            return tHit;
        }

        public float Fireball(Vector2 mouth, Vector2 tgt, float tH, Vector2? dat = null)
        {
            const float T0 = 0.3f, TT = 0.45f, R = 19;
            var d = Unit(tgt - mouth);
            var nd = new Vector2(-d.y, d.x);
            float dir = tgt.x >= mouth.x ? 1 : -1;
            Vector2 Path(float t)
            {
                float x = Mathf.Clamp01((t - T0) / TT);
                return mouth + (tgt - mouth) * x + new Vector2(0, -40) * Mathf.Sin(Mathf.PI * x);
            }
            float t0 = T;
            bool fb = HasFb("cau_lua");
            // tụ (2026-11-18): vệt xoắn ốc hút vào, hai vòng co, cầu nhiều múi lớn dần theo nhịp đập, nén rồi chớp lúc nhả; khung vẽ sẵn (2026-11-19):
            // cầu đang tụ là "cau_lua" (đã có lửa), bỏ lưỡi lửa liếm quanh cầu
            var rt = HoaTuCau(t => mouth, R, 0.02f, T0, true, 1, null, dir);
            if (!fb)
                Every(0.1f, T0 - 0.03f, x => 8 + 16 * x, x =>
                {
                    float r = rt(T), a = U(0, 6.28f);
                    var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    HoaLuoi(Flame(mouth + o * r * 0.6f, o * U(20, 60) + new Vector2(0, -U(40, 90)), U(0.16f, 0.24f), r * 0.3f, r * 0.5f, "tron", Th.pal, Front, 3,
                        -160, 1.5f, 0, 0), 1, 0.5f, 0);
                });
            // bay: khối cầu bám đường bay; đuôi lưỡi lửa đứng tại chỗ nguội dần (KR5); khói đuôi thành cụm. Khung vẽ sẵn (2026-11-19): cầu bay là
            // "cau_lua" (mũi theo đường cong, đuôi lửa vẽ sẵn) nên bỏ chuỗi lưỡi lửa đuôi
            At(T0, () =>
            {
                Func<float, Vector2> bay = t => Path(t - t0);
                Func<float, float> rb = t => R * (1 + 0.06f * Mathf.Sin(t * 40));
                // vệt khói đuôi (2026-11-19 chiều): cụm 0,22–0,35 thân theo cỡ cầu
                if (!fb || HoaFbCau(bay, rb, TT + 0.01f, Front, true, 0, KhoiCo(R, tH)) == null) HoaCau(bay, rb, TT + 0.01f);
            });
            if (!fb)
                Every(T0, T0 + TT, 50, x =>
                {
                    var q = Flame(Path(T - t0) - d * 6 + U2(-6, 6), -d * U(50, 120) + nd * U(-60, 60) + new Vector2(0, -20), U(0.2f, 0.27f), 15, 15, "tron",
                        Th.pal, Front, 3, -140, 1.4f, 0, 0);
                    HoaLuoi(q, 1, 0.2f, 0);
                    q.sizeFn = (z, k) => z.r1 * Mathf.Pow(1 - k, 1.1f);
                });
            HoaDuoiKhoi(t => Path(t - t0) - d * 22, T0 + 0.03f, T0 + TT, 11, 14); // khói đuôi theo quãng bay: liền dù cầu bay nhanh
            Every(T0, T0 + TT, 12, x => Spark(Path(T - t0), -d + U2(-0.6f, 0.6f), U(140, 260), 0, 6));
            At(T0 + TT, () =>
            {
                Shake?.Invoke(0.45f);
                HoaCauNo(tgt, dat ?? tgt + new Vector2(0, 0.42f * tH), tH, dir, 0.85f);
            });
            return T0 + TT;
        }

        // một mũi kim lửa: hiện ở `home`, lơ lửng chĩa về `aim`, tới giờ sân `launch` thì phóng đi với tốc độ `speed` (điểm sân / giây), chạm `aim` thì nổ kim
        // (dùng chung: Needles = kim quanh đầu tướng; NKimPhap ở HatPhap.cs = kim quanh đầu trượng của pháp sư lửa, phóng theo giờ của clip)
        // khoi > 0 (2026-11-19 chiều, người dùng: "fireball, tên lửa,... nên thêm trail smoke vào"): lúc phóng, kim nhả vệt khói đuôi (FbKhoiDuoi)
        // cụm cao khoi từ chuôi kim, thưa (18/s) vì kim bay rất nhanh
        void KimLua(Vector2 home, Vector2 aim, int span, float launch, float speed, Color[] cols, float[] fr, float[] ext, float LEN, float khoi = 0)
        {
            var q = new P { pos = home, life = 3, seed = 0, home = home, aim = aim, span = span, launch = launch };
            bool fbKim = HasFb("kim_lua"); // kim xoắn vẽ sẵn đã có lửa: bỏ lưỡi lửa nhỏ quanh kim lúc chờ và sau đuôi lúc bay (soi ảnh chụp 2026-11-24: rối)
            for (int k = 0; k < 2; k++)
                HoaLuoi(Flame(home + U2(-6, 6), new Vector2(U(-30, 30), U(-70, -30)), 0.22f, 5, 11, "tron", Th.pal, Front, 1.8f, -320, 1.6f, 0, 0), 1, 0.6f, 0);
            HoaTan(home, new Vector2(0, -70), 0, 2);
            q.upd = (z, dt, s) =>
            {
                if (!z.fly)
                {
                    z.pos = z.home + new Vector2(0, 3.5f * Mathf.Sin(z.age * 7 + z.span));
                    z.vel = (z.aim - z.pos) * 0.001f;
                    if (!fbKim && s.U(0, 1) < 0.12f)
                        s.Flame(z.pos + s.U2(-8, 8), new Vector2(s.U(-15, 15), s.U(-80, -40)), 0.25f, 4, 9, "nhon", Th.pal, Front, 1.8f, -320, 1.7f, 0, 0);
                    if (s.T >= z.launch)
                    {
                        z.fly = true;
                        z.vel = Unit(z.aim - z.pos) * speed;
                        s.Shake?.Invoke(0.05f);
                        if (khoi > 0) s.FbKhoiDuoi(() => z.pos - Unit(z.vel) * (0.5f * LEN), () => !z.dead && z.age < z.life, khoi, 18);
                    }
                }
                else
                {
                    if (s.U(0, 1) < 0.35f)
                        s.Spark(z.pos - Unit(z.vel) * 22, -Unit(z.vel) + s.U2(-0.15f, 0.15f), s.U(250, 380), 0.14f, 11, 0, Front, 6);
                    if (!fbKim && s.U(0, 1) < 0.12f)
                        s.Flame(z.pos - Unit(z.vel) * 24, -Unit(z.vel) * 40, 0.12f, 6, 9, "tron", Th.pal, Front, 1.8f, -320, 1.6f, 0, 0);
                    if (Vector2.Dot(z.aim - z.pos, z.vel) <= 0)
                    {
                        z.dead = true;
                        s.NeedleHit(z.aim, Unit(z.vel));
                    }
                }
            };
            // kim xoắn vẽ sẵn "kim_lua" (bộ lửa Blender 2026-11-24, như "Twisting Effect" người dùng đưa): mũi về +x, lặp; dài ≈ 1,5 LEN (gồm đuôi lửa
            // xoắn), lúc bay giãn dài 1,3; chưa nhập thì năm lớp ảnh kim cũ
            var kimArt = FbArt("kim_lua");
            if (kimArt != null)
            {
                var kd = Fbs["kim_lua"];
                float ph = U(0, kd.n);
                q.draw = (z, k, buf) =>
                {
                    float age = z.age;
                    float sc = age < 0.08f ? 1.25f * EaseOut(age / 0.08f) : 1.25f - 0.25f * Mathf.Min(1, (age - 0.08f) / 0.06f);
                    FbHuong(z.fly ? Unit(z.vel) : Unit(z.aim - z.pos), out float a, out bool lat);
                    DrawFb(buf, kimArt, kd, ph + age * kd.fps, z.pos, 1.5f * LEN * sc / kd.aspect, Front, 22, a, lat, Color.white, Mathf.Min(1, age / 0.05f),
                        z.fly ? 1.3f : 1);
                };
                Add(q);
                return;
            }
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
                    KimLua(home, aim, ii, T + 0.72f - ii * 0.07f + ii * 0.09f, 1500, cols, fr, ext, LEN);
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
            HoaTrung?.Invoke(p, 0.25f);
            // khung vẽ sẵn (2026-11-19): mỗi kim găm một "trung_lua" nhỏ lật / xoay theo hướng kim (thay chớp sao gai + ba lưỡi lửa toé ngược)
            if (HoaFbTrung(p, 50, d, Front, 1.25f) != null)
            {
                for (int i = 0; i < 3; i++) Spark(p, -d + U2(-0.9f, 0.9f), U(200, 380), 0, 6);
                if (U(0, 1) < 0.35f) HoaKhoi(p + new Vector2(0, -6), U(8, 11), Back, null, U(0.7f, 0.9f), false);
                Extra(p, 1, 260);
                return;
            }
            HoaChop(p, 30, 0.08f);
            float a0 = Mathf.Atan2(-d.y, -d.x);
            for (int i = 0; i < 3; i++)
            {
                float a = a0 + U(-1.2f, 1.2f); // toé ngược về phía kim tới
                HoaLuoi(Flame(p, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * 150, 0.26f, 7, 13, "tron", Th.pal, Front, 4, -320, 1.6f, 0, 0), 1, 0.2f, 0);
            }
            for (int i = 0; i < 4; i++) Spark(p, -d + U2(-0.9f, 0.9f), U(200, 380), 0, 6);
            if (U(0, 1) < 0.5f) HoaKhoi(p + new Vector2(0, -6), U(8, 11), Back, null, U(0.7f, 0.9f), false);
            Extra(p, 1, 260);
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
            if (HasFb("cau_lua") && HasFb("no") && HasFb("duoi_lua")) return MeteorFb(foeFeet, tH, fromSide); // bộ lửa Blender 2026-11-24 (HatFbHoa.cs)
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

        // co (2026-11-19): chiều cao khung "nham" theo thân đối thủ (chiêu mana 1,45; chiêu cuối 1,65); huong: hướng đòn (+1 sang phải, −1 sang
        // trái, 0 chưa biết) để dời cột "nham" về phía người ra chiêu
        public float Eruption(Vector2 foeFeet, float tH, float co = 1.45f, float huong = 0)
        {
            // 2026-11-18 (người dùng chê dung nham là cầu tròn): cột là cụm dung nham mềm kéo đuôi (krn) sau lưng đối thủ, giọt văng là giọt lệ, phần lớn
            // rơi phía sau; báo trước 0,42 s bằng vết nứt + khói mảnh; trào: chớp sát đất, vòng cung dẹt, vệt cháy, khói tách cụm bay lên
            float gy = foeFeet.y;
            var pre = new P { pos = foeFeet + new Vector2(0, 2), life = 0.45f, group = Floor, sz = tH };
            pre.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_0"), Color.white, q.pos, 1.5f * q.sz * 0.42f * (0.3f + 0.7f * EaseOut(q.age / 0.3f)), 1 / 0.42f);
            Add(pre);
            Shake?.Invoke(0.15f);
            if (HasFb("nham"))
            {
                EruptionFb(foeFeet, tH, co, huong);
                return 0.42f;
            }
            Every(0.05f, 0.42f, 14, x => LavaDrop(foeFeet + new Vector2(U(-0.45f, 0.45f) * tH, U(-6, 6)), new Vector2(U(-30, 30), -U(100, 180)), U(2.5f, 4),
                gy + U(-6, 8)));
            Every(0.12f, 0.42f, 5, x => HoaKhoi(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -4), U(6, 9), Back, new Vector2(U(-10, 10), -U(40, 70)),
                U(0.5f, 0.7f), false));
            At(0.42f, () =>
            {
                Shake?.Invoke(0.6f);
                FlashScreen?.Invoke(new Color(1, 0.9f, 0.7f, 0.18f));
                HoaTrung?.Invoke(foeFeet + new Vector2(0, -0.4f * tH), 0.6f);
                Crater(foeFeet + new Vector2(0, 6), 30, 1.65f, tH);
                HoaChop(foeFeet + new Vector2(0, -0.08f * tH), 0.42f * tH, 0.09f);
                HoaCung(foeFeet + new Vector2(0, 2), 0.15f * tH, 1.0f * tH, 0.5f, Th.ring);
                HoaVetChay(foeFeet + new Vector2(0, 2), 0.9f * tH);
                Extra(foeFeet + new Vector2(0, -20), 4, 380);
                for (int w = 0; w < 2; w++)
                {
                    int n = w == 0 ? 10 : 6;
                    At(w * 0.1f, () =>
                    {
                        for (int i = 0; i < n; i++)
                        {
                            float a = (-90 + U(-34, 34)) * Mathf.Deg2Rad;
                            LavaDrop(foeFeet + new Vector2(U(-0.2f, 0.2f) * tH, -4), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(320, 560), U(6, 9),
                                gy + U(-10, 18), U(0, 1) < 0.3f ? Front : Back);
                        }
                    });
                }
                for (int i = 0; i < 4; i++)
                {
                    float a = (-90 + U(-55, 55)) * Mathf.Deg2Rad;
                    Rock(foeFeet + new Vector2(0, -6), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(380, 680), gy + U(-14, 22));
                }
            });
            Every(0.42f, 0.82f, 55, x =>
            {
                var v = new Vector2(U(-60, 60), -U(640, 880) * (1 - 0.4f * x));
                float r = U(19, 27) * (1 - 0.3f * x);
                var q = Flame(foeFeet + new Vector2(U(-0.14f, 0.14f) * tH, -2), v, U(0.6f, 0.72f), r * 0.6f, r, "krn", "nham", Back, 0.6f, 1500, 1.5f, 0, 0);
                q.stretchK = 700;
                q.sizeFn = (z, k) => (z.r0 + (z.r1 - z.r0) * Mathf.Min(1, k / 0.3f)) * (1 - Mathf.Max(0, (k - 0.75f) / 0.25f));
            });
            Every(0.5f, 1.3f, 3.5f, x => HoaKhoi(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.5f, 1.0f) * tH), U(14, 19), Back,
                new Vector2(U(-30, 30), -U(60, 100)), U(1.0f, 1.3f)));
            return 0.42f;
        }

        // khung vẽ sẵn (2026-11-19): dung nham trào = "nham" (nứt, phun dẻo, đổ thành vũng, nguội, khói) neo dưới chân đối thủ, SAU lưng nó (cột
        // trào lên quanh viền thân, vũng loang hai bên chân), cao co × thân; phát sớm 0,15 s để khung phun (khung 4) trùng lúc trúng 0,42 s. Thay
        // cột cụm "krn", hố dung nham Crater, hai đợt giọt lệ, chớp đất, khói cụm. Giữ vết nứt báo trước (đã vẽ ở Eruption), vài giọt sủi báo trước,
        // vòng cung dẹt, vệt cháy, vài giọt lệ + đá văng ra ngoài khung.
        // 2026-11-19 chiều (người dùng: "vụ nổ layer nằm dưới địch nên không thấy rõ"): cột "nham" lên lớp TRƯỚC tướng (NoNhom), dời NoLech thân
        // về phía người ra chiêu
        void EruptionFb(Vector2 foeFeet, float tH, float co, float huong)
        {
            float gy = foeFeet.y;
            Every(0.05f, 0.4f, 8, x => LavaDrop(foeFeet + new Vector2(U(-0.4f, 0.4f) * tH, U(-6, 6)), new Vector2(U(-30, 30), -U(100, 170)), U(2.5f, 3.6f),
                gy + U(-6, 8)));
            Every(0.12f, 0.36f, 4, x => HoaKhoi(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -4), U(6, 9), Back, new Vector2(U(-10, 10), -U(40, 70)),
                U(0.5f, 0.7f), false));
            At(0.27f, () => Fb("nham", foeFeet + new Vector2(-huong * NoLech * tH, 3), co * tH, NoNhom, 28, 1.1f, 0, U(0, 1) < 0.5f));
            At(0.42f, () =>
            {
                Shake?.Invoke(0.6f);
                FlashScreen?.Invoke(new Color(1, 0.9f, 0.7f, 0.18f));
                HoaTrung?.Invoke(foeFeet + new Vector2(0, -0.4f * tH), 0.6f);
                HoaCung(foeFeet + new Vector2(0, 2), 0.15f * tH, 1.0f * tH, 0.5f, Th.ring);
                HoaVetChay(foeFeet + new Vector2(0, 2), 0.9f * tH);
                Extra(foeFeet + new Vector2(0, -20), 4, 380);
                for (int i = 0; i < 4; i++)
                {
                    float a = (-90 + (i < 2 ? -1 : 1) * U(28, 50)) * Mathf.Deg2Rad; // văng ra hai bên, ra ngoài khung
                    LavaDrop(foeFeet + new Vector2(U(-0.2f, 0.2f) * tH, -0.3f * tH), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(300, 480), U(5, 7.5f),
                        gy + U(-10, 18), i == 0 ? Front : Back);
                }
                for (int i = 0; i < 3; i++)
                {
                    float a = (-90 + U(-55, 55)) * Mathf.Deg2Rad;
                    Rock(foeFeet + new Vector2(0, -6), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(380, 620), gy + U(-14, 22));
                }
            });
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
            void Orbit(P q, float dt, HatLua s)
            {
                float a = q.ph + OM * q.age, y = q.vy * q.age, h = Mathf.Min(1, y / HT);
                float R = q.R0 + (q.R1 - q.R0) * Mathf.Pow(h, 0.9f);
                q.pos = Cc + new Vector2(R * Mathf.Cos(a), 0.3f * R * Mathf.Sin(a) - y);
                q.vel = new Vector2(-R * Mathf.Sin(a) * OM, 0.3f * R * Mathf.Cos(a) * OM - q.vy);
                q.group = Mathf.Sin(a) < 0 ? Back : Front;
                q.hgt = h;
            }
            // khung vẽ sẵn (2026-11-19 tối, người dùng chê lốc cũ "màu hơi trầm và chưa hợp lắm"): thân lốc là "loc_lua" bao quanh đối thủ (lớp sau
            // đặc, lớp trước mờ lệch pha), vọt lên 0,2 s từ 0,2 s (lúc lưỡi lửa cũ bắt đầu dâng), xoáy tới T1 rồi tắt dần. Bỏ vòng viền
            // mực ở chân, lưỡi lửa bay vòng, dải cung hai nửa, khói hạt cũ; giữ than bị hút (ở trên), vết nứt, tia lửa bay quanh (thưa hơn), đá cuốn,
            // mảnh theo chủ đề; khói là "khoi" ở miệng phễu. Rung và giờ trả về như cũ.
            // 2026-11-19 đêm (người dùng: "lốc xoáy làm to lên cho che hết tướng địch"): lốc trùm "loc_lua_bao" cao 1,65 thân, giãn ngang 1,2 (ngang
            // thân ≈ 1,2 thân, trùm từ chân tới đầu); chưa nhập thì "loc_lua" cao 1,7 thân, giãn 1,55
            if (HoaFbLoc(Cc, 1.7f * tH, 0.2f, T1 + 0.15f, true, 0.55f, 1.15f, 1.55f, 1.65f * tH, 1.2f))
            {
                Every(0.3f, T1, 18, x =>
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
                // khói bốc từ miệng phễu: lốc Blender (2026-11-24) cao 1,8 thân, miệng ở ≈ 1,6 thân, cụm to hơn (như dự án AtomSpine atom_bl)
                Every(0.4f, T1 - 0.2f, 5, x => HoaKhoi(Cc + new Vector2(U(-0.35f, 0.35f) * tH, -1.6f * tH + U(0, 16)), U(0.2f, 0.27f) * tH, Back,
                    new Vector2(U(-30, 30), -U(50, 90)), U(0.9f, 1.1f), false));
                Every(0.35f, T1, 4, x => Extra(Cc + new Vector2(U(-R1, R1) * 0.7f, -U(0.2f, 1.0f) * HT), 1, 160, U(0, 1) < 0.5f ? Front : Back));
                At(0.3f, () => Shake?.Invoke(0.35f));
                return 0.35f;
            }
            Ring(Cc, 2.3f, R0 * 2.2f, R0 * 1.6f, Th.ring);
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
                "tia_mat" => TiaMat(mouth, foeBody, tH, 0.9f, casterH), // Hỏa Nhãn (HatNhan.cs): tia lửa từ con ngươi (tia vẽ sẵn dày 0,22 casterH)
                "ten" => TenNo(foeBody, tH, casterFeet, foeFeet), // Hỏa Cung: ba mũi tên là mảnh của rig (game lái tới đối thủ), ở đây chỉ nổ lúc tên tới
                "dat_trao" => Eruption(foeFeet, tH, 1.45f, foeFeet.x >= casterFeet.x ? 1 : -1), // Viêm Đao: bổ đao cắm xuống đất, dung nham trào lên dưới chân đối thủ
                _ => Fireball(mouth, foeBody, tH, foeFeet),
            };

        // chiêu cuối theo mã ("thien_thach", "phun_nham", "loc_xoay", "no_lon"); fromSide: phía con ra chiêu so với đối thủ (-1 trái, 1 phải)
        public float PlayUlt(string kind, Vector2 foeFeet, Vector2 foeBody, float tH, float fromSide) =>
            kind switch
            {
                "thien_thach" => Meteor(foeFeet, tH, fromSide == 0 ? 1 : fromSide),
                "phun_nham" => Eruption(foeFeet, tH, 1.65f, -fromSide), // khung vẽ sẵn (2026-11-19): chiêu cuối cột dung nham cao hơn chiêu mana
                "loc_xoay" => Tornado(foeFeet, tH),
                "quyen_xoay" => QuyenXoay(foeFeet, foeBody, tH), // Hỏa Nhãn: lửa xoáy + chuỗi chớp nổ theo nhịp đấm
                _ => BigBurst(foeFeet, foeBody, tH, fromSide),
            };

        // nổ lớn: vòng lửa loang dưới chân, cột lưỡi lửa vọt lên ôm thân (phần lớn sau lưng), rồi chớp sao gai nổ ở thân, nổ phụ
        // fromSide (2026-11-19): phía con ra chiêu so với đối thủ (−1 trái, 1 phải, 0 chưa biết) để lật khung "trung_lua" theo hướng đòn
        public float BigBurst(Vector2 feet, Vector2 body, float tH, float fromSide = 0)
        {
            // 2026-11-18: vòng cung dẹt + vết nứt báo trên đất, cột lưỡi lửa chữ S ôm thân (phần lớn sau lưng), nổ KR5 (khói hai tông tách cụm, lưỡi
            // liềm, vệt cháy) ở 0,18 s, nổ phụ 0,34 s, khói thành cụm bay lên
            float rx = 0.34f * tH, huong = -fromSide;
            Shake?.Invoke(0.3f);
            HoaCung(feet + new Vector2(0, 2), 0.15f * tH, 0.95f * tH, 0.45f, Th.ring);
            var cr = new P { pos = feet + new Vector2(0, 2), life = 1.3f, group = Floor, seed = rng.Next(4), sz = tH };
            cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_" + q.seed), Color.white, q.pos, 1.3f * q.sz * 0.42f * Mathf.Min(1, q.age / 0.15f),
                1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.3f));
            Add(cr);
            if (HasFb("lua_lap"))
            {
                // khung vẽ sẵn (2026-11-19): cột lửa ôm thân = ba cụm lửa lặp "lua_lap" vọt lên ở chân (hai cụm cao sau lưng hai bên, một cụm thấp
                // trước chân), thay ~40 lưỡi lửa chữ S bay lên
                HoaFbLua(feet + new Vector2(-0.2f * tH, -1), 1.1f * tH, 0.62f, Back, 26, 0.1f, 0.5f, 1.2f);
                HoaFbLua(feet + new Vector2(0.22f * tH, -1), 0.95f * tH, 0.58f, Back, 26, 0.12f, 0.5f, 1.2f);
                HoaFbLua(feet + new Vector2(U(-0.08f, 0.08f) * tH, 4), 0.38f * tH, 0.5f, Front, 26, 0.1f, 0.5f, 1.2f);
            }
            else
                Every(0, 0.5f, x => 80 * (1 - 0.5f * x), x =>
                {
                    float th = U(0, 6.28f);
                    bool front = Mathf.Sin(th) > 0.35f;
                    var q = Flame(feet + new Vector2(rx * Mathf.Cos(th), 12 * Mathf.Sin(th) - 4), new Vector2(Mathf.Cos(th) * 40, -U(420, 640)), U(0.32f, 0.5f), 9,
                        U(20, 28) * (front ? 0.6f : 1), "tron", Th.pal, front ? Front : Back, 2.2f, -200, 1.7f, 0, 0);
                    HoaLuoi(q, 1, 0.5f, 0.06f);
                });
            At(0.18f, () =>
            {
                Shake?.Invoke(0.5f);
                HoaTrung?.Invoke(body, 0.8f);
                HoaNo(body, 1.15f, tH, feet, Front, huong);
            });
            At(0.34f, () => HoaNo(body + new Vector2(U(-22, 22), U(-28, 0)), 0.65f, tH, null, Front, huong));
            At(0.5f, () =>
            {
                for (int i = 0; i < 2; i++)
                    HoaKhoi(body + new Vector2(U(-30, 30), -U(40, 70)), U(0.16f, 0.2f) * tH, Back, new Vector2(U(-25, 25), -U(50, 80)), U(1.1f, 1.4f));
            });
            return 0.18f;
        }

        // thời gian tướng giữ dáng ra chiêu (khung bắn của clip) sau lúc gọi PlayMana: phun tới khi luồng tắt, kim tới khi kim cuối
        // phóng đi, cầu tới khi cầu tụ xong rời miệng
        public static float HoldOf(string kind) =>
            kind != null && kind.StartsWith("phun") ? BreathHold : kind == "kim" ? 1.35f : kind == "tia_mat" ? TiaMatHold : 0.32f;
    }
}
