// KHUNG HÌNH VẼ SẴN (flipbook, 2026-11-19). Người dùng chọn style VFX theo bốn gói ảnh mẫu (dáng, chuyển động) nhưng chất liệu của game:
// "texture … kiểu chì vẽ, bỏ bóng ánh sáng đi", và "muốn vfx mượt hơn … tăng frame lên". Mỗi hiệu ứng là 24 khung vẽ sẵn (gen GPT rồi
// làm phẳng + phủ vân chì: ArtGen/Spine/vfx_gen/cat_khung.py, chi_phang.py, xuat_fb.py), ảnh Assets/03 Art/Fx/Hat/hat_fb_<tên>_NN.png.
// Chạy 24 khung/giây, CHỒNG MỜ khung kế (khung i đặc + khung i+1 mờ dần lên) cho mượt ở 60 khung/giây; không viền mực, không quầng.
// Khung đã tô màu sẵn: tint mặc định trắng (nhân màu Image), muốn đổi sắc (gai sắt -> tinh thể oải hương, khói -> bụi đất) thì truyền tint.
// Điểm neo theo từng hiệu ứng (bảng Fbs): "chân" = đáy giữa khung đứng trên đất, "tâm" = tâm chớp / tâm cầu. Toạ độ sân như mọi hạt.
// Dùng:
//   Fb("no", chânĐốiThủ, 1.6f * tH);                                   nổ một lần, cao 1,6 lần thân đối thủ
//   Fb("lua_lap", p, 60, life: 1.2f);                                   lửa cháy lặp 1,2 s rồi tắt dần
//   FbFly("cau_lua", miệng, thânĐốiThủ, 70, 520, q => Fb("trung_lua", q.pos, 110));  cầu lửa bay tới, trúng thì bung
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public sealed class FbDef
        {
            public readonly int n;
            public readonly float aspect, px, py, fps, k, cy;
            public readonly bool loop;

            // w, h: cỡ khung (điểm ảnh); px, py: điểm neo trong khung (0..1, py tính từ ĐÁY lên)
            // k (2026-11-24, bộ lửa Blender): khung vẽ cao k × h mà hàm gọi truyền — khung mới lấp đầy khung hơn khung cũ (cầu tròn không đuôi,
            //   nổ tròn) nên thu lại cho đúng cỡ cũ mà không phải sửa từng chỗ gọi
            // cy: tâm cụm (khói) cao hơn điểm neo bao nhiêu phần h, cho vệt khói đuôi đặt tâm cụm lên đường bay
            public FbDef(int n, int w, int h, float px, float py, bool loop, float fps = 24, float k = 1, float cy = 0.42f)
            {
                this.n = n;
                aspect = w / (float)h;
                this.px = px;
                this.py = py;
                this.loop = loop;
                this.fps = fps;
                this.k = k;
                this.cy = cy;
            }
        }

        // khung_chi/ds.json (cat_khung.py) + tâm đo trên khung (cầu lửa: đầu cầu ở 73 % bề ngang, đuôi về trái)
        public static readonly Dictionary<string, FbDef> Fbs = new Dictionary<string, FbDef>
        {
            // BỘ LỬA BLENDER (2026-11-24, người dùng: "thay các fx vừa làm vào game"; ArtGen/Spine/vfx_lua_toon/xuat_game.py, skill vfx-petclash
            // blender_anime_fx.md mục 9–11): nổ, khói, lửa cháy, cầu lửa, lốc lửa thay khung GPT cũ cùng tên; phun, kim_lua, duoi_lua là tên mới
            { "no", new FbDef(26, 296, 300, 0.582f, 0.141f, false, 24, 0.75f) }, // nổ tròn: sao chớp → khối lửa phồng → thủng lỗ → mảnh đỏ sẫm; neo ĐÁY quả nổ
            { "trung_lua", new FbDef(24, 260, 244, 0.545f, 0.49f, false) }, // lửa trúng đích: đòn tới từ TRÁI (lật khi đòn tới từ phải)
            { "lua_lap", new FbDef(24, 206, 277, 0.515f, 0.029f, true) },   // lửa cháy lặp 1 s (shader Voronoi bài Blender Box): chân vàng, thân cam đốm đỏ, ngọn vệt trắng
            { "cau_lua", new FbDef(24, 177, 179, 0.497f, 0.497f, true, 24, 0.6f) }, // cầu lửa TRÒN không đuôi (đuôi = vệt "duoi_lua"), neo tâm; k: cầu cao nửa h như khung cũ
            { "nham", new FbDef(24, 282, 232, 0.5f, 0.01f, false) },        // dung nham phun từ đất, đổ thành vũng, nguội
            { "khoi", new FbDef(25, 272, 280, 0.499f, 0.044f, false, 24, 1, 0.28f) }, // cụm khói nâu xám hai tông phồng, bay lên, vỡ mảnh; neo đáy cụm
            { "phun", new FbDef(47, 512, 295, 0.024f, 0.425f, false) },    // phun lửa: mép đầu vươn từ miệng (0,75 s), giữ, đứt khỏi miệng 1,27 s, vỡ mảnh; neo miệng, phun sang PHẢI
            { "kim_lua", new FbDef(12, 298, 54, 0.691f, 0.5f, true) },     // kim lửa xoắn (lặp), mũi về +x
            { "duoi_lua", new FbDef(27, 228, 240, 0.5f, 0.31f, false, 24, 1, 0) }, // hạt vệt đuôi cầu lửa: cụm lửa đậm → khói; neo tâm cụm lúc sinh
            { "nuoc_toe", new FbDef(24, 272, 226, 0.5f, 0.01f, false) },    // vương miện nước toé từ đất
            { "song_nuoc", new FbDef(24, 248, 205, 0.5f, 0.01f, false) },   // sóng dâng, cuộn, đổ sang PHẢI
            { "trung_nuoc", new FbDef(24, 256, 274, 0.525f, 0.47f, false) },// nước trúng đích: tia tới từ TRÁI
            { "cau_nuoc", new FbDef(24, 242, 246, 0.5f, 0.5f, true) },      // cầu nước có dải bọt xoay (lặp)
            { "loc", new FbDef(24, 248, 238, 0.5f, 0.01f, true) },          // lốc năng lượng xanh (lặp)
            { "gai_la", new FbDef(24, 250, 227, 0.5f, 0.01f, false) },      // gai lá đâm lên: nứt, phóng, giữ, gãy rụng lá
            { "gai_bang", new FbDef(24, 238, 216, 0.5f, 0.01f, false) },    // gai tinh thể lam nhạt đâm lên, vỡ mảnh
            { "gai_sat", new FbDef(24, 238, 216, 0.5f, 0.01f, false) },     // gai sắt xám thép đâm lên, vỡ mảnh (nhuộm được)
            // lốc xoáy LẶP (2026-11-19, người dùng chê vòi rồng mảng cũ "màu hơi trầm và chưa hợp"): phễu hẹp ở đất, nở lên trên, dải xoắn
            { "loc_nuoc", new FbDef(24, 238, 251, 0.5f, 0.01f, true) },     // lốc nước: lam, ngọc lam, bọt trắng
            { "loc_lua", new FbDef(48, 420, 292, 0.5f, 0.03f, false) },    // lốc lửa MỘT LƯỢT 2 s (Blender, từ file mẫu Tornado đã mua): mọc, xoắn, gió cuốn, tàn, ép về trục
            { "loc_cat", new FbDef(24, 242, 250, 0.5f, 0.01f, true) },      // lốc cát: kem, vàng cát, nâu
            // cầu lửa mới (2026-11-19, người dùng chê cầu lửa Hỏa Quy "tĩnh"): lửa cuộn xoáy quanh lõi, LẶP
            { "cau_tu", new FbDef(24, 254, 264, 0.5f, 0.5f, true) },        // cầu lửa đang tụ: phồng to rồi co (cỡ đổi trong vòng lặp), lưỡi lửa cuộn
            { "cau_bay", new FbDef(24, 262, 166, 0.78f, 0.48f, true) },     // cầu lửa bay sang PHẢI: lửa cuộn quanh đầu, đuôi dài quẫy
            // lốc TRÙM (2026-11-19, người dùng: "lốc xoáy làm to lên cho che hết tướng địch"): cột xoáy DÀY, gốc gần rộng bằng miệng (rộng ~0,95
            // cao) — dùng khi lốc bao quanh đối thủ; lốc phễu (loc_nuoc / loc_lua / loc_cat) thon ở gốc nên hở chân
            { "loc_nuoc_bao", new FbDef(24, 240, 249, 0.5f, 0.01f, true) },
            { "loc_lua_bao", new FbDef(24, 244, 246, 0.5f, 0.01f, true) },
            { "loc_cat_bao", new FbDef(24, 248, 252, 0.5f, 0.01f, true) },
            // tia vẽ sẵn (2026-11-19, người dùng: "các tia năng lượng/nước như này nhìn vẫn chưa đã"; HatTiaFb.cs): đoạn thân chảy sang PHẢI,
            // đầu nòng, va chạm (tia tới từ TRÁI). Tất cả LẶP
            { "tia_moc_doan", new FbDef(24, 260, 126, 0.5f, 0.5f, true) },
            { "tia_moc_nong", new FbDef(24, 262, 256, 0.5f, 0.5f, true) },
            { "tia_moc_trung", new FbDef(24, 262, 268, 0.45f, 0.49f, true) },
            { "tia_nuoc_doan", new FbDef(24, 260, 136, 0.5f, 0.5f, true) },
            { "tia_nuoc_trung", new FbDef(24, 300, 260, 0.39f, 0.54f, true) },
            { "tia_lua_doan", new FbDef(24, 260, 138, 0.5f, 0.5f, true) },
            { "tia_lua_nong", new FbDef(24, 284, 252, 0.5f, 0.5f, true) },
            { "tia_lua_trung", new FbDef(24, 262, 272, 0.465f, 0.486f, true) },
            { "tia_vang_doan", new FbDef(24, 260, 142, 0.5f, 0.5f, true) },
            { "tia_vang_nong", new FbDef(24, 276, 256, 0.5f, 0.5f, true) },
            { "tia_vang_trung", new FbDef(24, 260, 268, 0.441f, 0.493f, true) },
            // CẦU NĂNG LƯỢNG kiểu "Energy Ball" (CodyWinch, 2026-11-24, người dùng chọn cho cầu năng lượng Mộc / Kim / Thổ): thân nhiều múi màu
            // phẳng, gân sáng lộ qua khe, xoay một vòng / 1,5 s (ArtGen/Spine/vfx_blender/cau_nl_bl.py → vfx_lua_toon/cat_nl.py → xuat_game.py).
            // Neo tâm, LẶP 36 khung; k 0,6 như cau_lua: quả cầu cao ~0,855 khung → bán kính thấy 0,257 h (vẽ bằng VeCauNl)
            { "cau_moc", new FbDef(36, 248, 256, 0.518f, 0.511f, true, 24, 0.6f) },  // lục ngọc + gân chanh: CauLa (Gạc Đá, Lộc Phong), đầu nòng DaTiaMoc
            { "cau_vang", new FbDef(36, 248, 256, 0.518f, 0.511f, true, 24, 0.6f) }, // cam vàng + gân kem: RbCau (Thần Cơ, Pháo Giáp), đầu nòng DaTiaVang
            { "cau_troi", new FbDef(36, 248, 256, 0.518f, 0.511f, true, 24, 0.6f) }, // cam đỏ + gân vàng: Mặt Trời của Thổ Tinh (TtMatTroi)
        };

        // vẽ CẦU NĂNG LƯỢNG kiểu Energy Ball (khung "cau_moc" / "cau_vang" / "cau_troi") tâm c, bán kính THẤY r (đơn vị sân); t: giây (đổi
        // khung, mỗi cầu nên lệch pha riêng); ang, st: góc (độ, ngược kim đồng hồ trên màn hình) và độ giãn dọc góc đó (cầu bay kéo dài theo
        // hướng bay). Trả false nếu chưa nhập khung (hàm gọi tự vẽ cầu hạt cũ)
        const float CauNlH = 3.9f;   // cao khung / bán kính thấy (k 0,6 × quả cầu 0,855 khung: r = 0,257 h)
        bool VeCauNl(List<Item> buf, string fx, Vector2 c, float r, int g, float layer, float t, float ang = 0, float st = 1, float a = 1)
        {
            var art = FbArt(fx);
            if (art == null) return false;
            var d = Fbs[fx];
            DrawFb(buf, art, d, t * d.fps, c, CauNlH * r, g, layer, ang, false, Color.white, a, st);
            return true;
        }

        readonly Dictionary<string, Sprite[]> fbArt = new Dictionary<string, Sprite[]>();

        Sprite[] FbArt(string fx)
        {
            if (fbArt.TryGetValue(fx, out var a)) return a;
            a = null;
            if (Fbs.TryGetValue(fx, out var d))
            {
                a = new Sprite[d.n];
                for (int i = 0; i < d.n; i++)
                {
                    a[i] = S("fb_" + fx + "_" + i.ToString("00"));
                    if (a[i] == null)
                    {
                        a = null;
                        break;
                    }
                }
            }
            if (a != null) fbArt[fx] = a; // thiếu khung (gói tải sau chưa nạp): không nhớ, lần sau tìm lại
            return a;
        }

        // đã nhập đủ khung chưa (chưa nhập thì hàm gọi tự rơi về hiệu ứng cũ)
        public bool HasFb(string fx) => FbArt(fx) != null;

        // số giây một lượt (tốc độ 1)
        public static float FbDur(string fx) => Fbs.TryGetValue(fx, out var d) ? d.n / d.fps : 0;

        // Phát hiệu ứng khung tại điểm neo pos, khung cao h (đơn vị sân).
        //   speed: nhân tốc độ; start: bắt đầu từ khung thứ mấy (vd. bỏ khung nứt đất của gai)
        //   life > 0: chạy đúng life giây (hiệu ứng lặp thì lặp, một lượt thì dừng ở khung cuối), cuối mờ dần fadeOut giây
        //   flip: lật ngang (đòn tới từ phải, sóng đổ sang trái); ang: góc (độ, ngược kim đồng hồ trên màn hình)
        //   tint: nhân màu (mặc định trắng = giữ màu khung); alpha: độ đặc tối đa
        public P Fb(string fx, Vector2 pos, float h, int group = Front, float layer = 30, float speed = 1, float ang = 0,
            bool flip = false, Color? tint = null, float alpha = 1, float life = -1, float start = 0, float fadeOut = 0.15f)
        {
            var art = FbArt(fx);
            if (art == null) return null;
            var d = Fbs[fx];
            float fps = d.fps * Mathf.Max(0.05f, speed);
            float dur = life > 0 ? life : Mathf.Max(0.05f, (d.n - start) / fps);
            var col = tint ?? Color.white;
            var p = new P { pos = pos, group = group, life = dur };
            p.draw = (q, k, buf) =>
            {
                float a = alpha;
                if (life > 0) a *= Mathf.Clamp01((q.life - q.age) / Mathf.Max(0.01f, fadeOut));
                DrawFb(buf, art, d, start + q.age * fps, q.pos, h, q.group, layer, ang, flip, col, a);
            };
            return Add(p);
        }

        // Vật bay bằng khung (cầu lửa, cầu nước): bay thẳng từ -> tới với v đơn vị sân / giây, khung xoay theo hướng bay (khung vẽ bay
        // sang phải; bay sang trái thì lật thay vì lộn ngược). Tới nơi gọi onHit(p) (p.pos = điểm tới).
        //   khoi > 0: kèm vệt khói đuôi (FbKhoiDuoi) cụm cao khoi
        public P FbFly(string fx, Vector2 tu, Vector2 toi, float h, float v, Action<P> onHit = null, int group = Front, float layer = 34,
            Color? tint = null, float alpha = 1, float khoi = 0)
        {
            var art = FbArt(fx);
            if (art == null) return null;
            var d = Fbs[fx];
            var dir = toi - tu;
            float dist = dir.magnitude;
            dir = Unit(dir);
            bool flip = dir.x < 0;
            // khung vẽ mũi về +x; trên UI (y lên) mũi phải chỉ theo u = (dir.x, -dir.y)
            float ang = flip ? Mathf.Atan2(dir.y, -dir.x) * Mathf.Rad2Deg : Mathf.Atan2(-dir.y, dir.x) * Mathf.Rad2Deg;
            var col = tint ?? Color.white;
            var p = new P { pos = tu, vel = dir * v, group = group, life = Mathf.Max(0.05f, dist / Mathf.Max(1, v)) };
            float ph = U(0, d.n);
            p.draw = (q, k, buf) =>
            {
                float a = alpha * Mathf.Clamp01(q.age / 0.05f);
                DrawFb(buf, art, d, ph + q.age * d.fps, q.pos, h, q.group, layer, ang, flip, col, a);
            };
            if (onHit != null)
                p.onDeath = (q, _) =>
                {
                    q.pos = toi;
                    onHit(q);
                };
            Add(p);
            // cầu lửa tròn (2026-11-24) không còn đuôi vẽ sẵn: luôn kéo vệt "duoi_lua" (lửa đậm → khói) thay vệt khói
            if (fx == "cau_lua" && DuoiLua(p, 0.5f * h * d.k) != null) return p;
            if (khoi > 0) FbKhoiDuoi(p, khoi, -dir * (0.5f * h));
            return p;
        }

        // VỆT ĐUÔI CẦU LỬA (2026-11-24, người dùng: "đuôi lửa đậm và khói làm thành 1 trail gắn vào cầu"): cứ vật đi được ~0,45 bán kính thì thả
        // một hạt khung "duoi_lua" ngay sau nó (cụm lửa đậm nguội dần thành khói, nở ra, trôi ngược hướng bay + bốc lên). r: bán kính quả cầu (đơn
        // vị sân). Soi ảnh chụp trong trận: hạt cao 5 r, sống 0,9 s thành cột khói xám to phủ cả sân sau cú nổ và che tướng mình → hạt 3,6 r, sống
        // ~0,75 s, MẶC ĐỊNH lớp sau tướng (Back: không che hai con, giữa sân vẫn thấy). where(): tâm cầu; alive(): cầu còn bay.
        //   buoc: quãng giữa hai hạt (phần r; tối thiểu 6 đơn vị sân để cầu nhỏ bay xa không đẻ quá nhiều hạt); speed: tốc độ khung (đời ≈ 1,1 / speed s)
        public P DuoiLua(Func<Vector2> where, Func<bool> alive, float r, int group = Back, float layer = 26, float speed = 1.5f, float buoc = 0.45f)
        {
            if (!HasFb("duoi_lua") || where == null || r < 1) return null;
            r = Mathf.Min(r, 30); // cầu chiêu cuối rất to (Hỏa Quy): không chặn thì cụm khói đuôi phủ kín cả đối thủ
            var last = where();
            float con = 0, step = Mathf.Max(6, buoc * r), h = 3.6f * r;
            var e = new P { life = 8, group = group };
            e.upd = (q, dt, s) =>
            {
                if (alive != null && !alive())
                {
                    q.dead = true;
                    return;
                }
                var cur = where();
                var seg = cur - last;
                float len = seg.magnitude;
                var u = len > 1e-4f ? seg / len : Vector2.zero;
                float x = step - con;
                while (x <= len)
                {
                    var pnt = last + seg * (x / Mathf.Max(1e-4f, len)) + U2(-0.08f, 0.08f) * r;
                    var f = Fb("duoi_lua", pnt, h * U(0.9f, 1.1f), group, layer + U(0, 0.5f), speed * U(0.92f, 1.08f), U(-12, 12), U(0, 1) < 0.5f);
                    if (f != null)
                    {
                        f.vel = -u * U(0.4f, 0.7f) * r + new Vector2(U(-0.2f, 0.2f) * r, -U(0.8f, 1.4f) * r);
                        f.drag = 0.8f;
                    }
                    x += step;
                }
                con = len - (x - step);
                last = cur;
            };
            return Add(e);
        }

        // vệt đuôi theo một hạt bay (tâm cầu = p.pos); thôi thả khi hạt chết / hết tuổi
        public P DuoiLua(P host, float r, int group = Back, float layer = 26) =>
            host == null ? null : DuoiLua(() => host.pos, () => !host.dead && host.age < host.life, r, group, layer);

        // VỆT KHÓI ĐUÔI cho vật bay (người dùng 2026-11-19: "fireball, tên lửa,... nên thêm trail smoke vào"): cụm khói khung "khoi" nhỏ nhả
        // đều sau vật bay, rải trên cả đoạn vừa bay qua (bay nhanh vẫn liền), chạy nhanh (speed) nên tan sau ~0,5 s, bỏ mấy khung đầu (múi
        // tí hon), góc / lật ngẫu nhiên cho khỏi lặp. Lớp sau vật bay (Back, hoặc Front layer thấp hơn vật). Cụm cao h đơn vị sân.
        //   where(): điểm đuôi hiện tại; alive(): vật còn bay không (false -> thôi nhả, các cụm đã nhả tự tan)
        public P FbKhoiDuoi(Func<Vector2> where, Func<bool> alive, float h, float rate = 26, Color? tint = null, int group = Front,
            float layer = 27, float speed = 1.9f, float maxDur = 8)
        {
            if (!HasFb("khoi") || where == null) return null;
            var last = where();
            float acc = 0;
            var e = new P { life = maxDur, group = group };
            e.upd = (q, dt, L) =>
            {
                if (alive != null && !alive())
                {
                    q.dead = true;
                    return;
                }
                var cur = where();
                acc += dt * rate;
                while (acc >= 1)
                {
                    acc -= 1;
                    float hh = h * U(0.8f, 1.2f);
                    // neo "chân" của khung khói: dời xuống cy cao (khung cũ 0,38; khói Blender 0,28) để tâm cụm nằm trên đường bay
                    var pnt = Vector2.Lerp(last, cur, U(0, 1)) + new Vector2(U(-0.1f, 0.1f) * h, Fbs["khoi"].cy * hh);
                    Fb("khoi", pnt, hh, group, layer + U(0, 0.5f), speed * U(0.9f, 1.15f), U(-14, 14), U(0, 1) < 0.5f, tint, 0.92f, -1, 3);
                }
                last = cur;
            };
            return Add(e);
        }

        // vệt khói theo một hạt bay (p.pos + lệch off, ví dụ -hướng * nửa thân đạn); thôi nhả khi hạt chết / hết tuổi
        //   speed: tốc độ chạy khung khói (nhỏ hơn = cụm sống lâu hơn = vệt dài hơn; 1,9 ~ 0,45 s, 1,0 ~ 0,9 s)
        public P FbKhoiDuoi(P host, float h, Vector2 off = default, float rate = 26, Color? tint = null, int group = Front, float layer = 27,
            float speed = 1.9f)
        {
            if (host == null) return null;
            return FbKhoiDuoi(() => host.pos + off, () => !host.dead && host.age < host.life, h, rate, tint, group, layer, speed);
        }

        // vẽ khung f (số thực): khung floor(f) đặc, khung kế chồng lên với alpha = phần lẻ (mượt giữa hai khung 24 khung/giây)
        //   sx (2026-11-24): giãn dọc trục ngang của khung (trước khi xoay) — phun lửa giãn cho đủ dài tới đích mà không dày thêm
        void DrawFb(List<Item> buf, Sprite[] art, FbDef d, float f, Vector2 pos, float h, int g, float layer, float ang, bool flip,
            Color col, float a, float sx = 1)
        {
            if (a < 0.02f) return;
            h *= d.k;
            int n = d.n;
            int i;
            float u;
            if (d.loop)
            {
                f %= n;
                if (f < 0) f += n;
                i = (int)f;
                u = f - i;
            }
            else
            {
                if (f >= n - 1)
                {
                    i = n - 1;
                    u = 0;
                }
                else
                {
                    i = Mathf.Max(0, (int)f);
                    u = Mathf.Clamp01(f - i);
                }
            }
            float asp = d.aspect * sx, w = h * asp;
            // điểm neo -> tâm khung (Image xoay quanh tâm): lệch trong khung (y lên), lật, xoay, rồi đổi sang toạ độ sân (y xuống)
            float ox = (0.5f - d.px) * w, oy = (0.5f - d.py) * h;
            if (flip) ox = -ox;
            float r = ang * Mathf.Deg2Rad, c = Mathf.Cos(r), s = Mathf.Sin(r);
            var center = pos + new Vector2(ox * c - oy * s, -(ox * s + oy * c));
            Put(buf, g, layer, art[i], col, center, h, asp, ang, a, 0, flip);
            if (u > 0.02f)
            {
                int j = d.loop ? (i + 1) % n : Mathf.Min(n - 1, i + 1);
                Put(buf, g, layer + 0.001f, art[j], col, center, h, asp, ang, a * u, 0, flip);
            }
        }
    }
}
