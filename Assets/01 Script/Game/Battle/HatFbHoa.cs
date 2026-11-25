// BỘ HỎA bằng KHUNG VẼ SẴN (flipbook, 2026-11-19). Người dùng duyệt bộ khung 24 khung ("ổn hơn rồi đấy, cho vào game đi"): các hàm Hoa… dùng
// chung của HatLua.cs (nổ, chớp, cụm khói, cầu lửa, lửa bám, cột lửa, dung nham phun) đổi phần thân chính sang khung vẽ sẵn của HatFlip.cs:
//   nổ lớn = "no" (neo chân, trước tướng, dời về phía người ra chiêu) + "trung_lua" ở thân (trước tướng);
//   nổ nhỏ, trúng đích = "trung_lua" (lật theo hướng đòn); chớp = vài khung đầu của "trung_lua" (sao lửa bung, không viền mực);
//   cụm khói = "khoi"; cầu lửa bay / cầu đang tụ = "cau_lua"; lửa bám, cột lửa, sẹo lửa = "lua_lap"; dung nham trào = "nham".
// Chưa nhập ảnh khung (HasFb false) thì mọi hàm gọi rơi về hạt cũ. Hạt phụ còn giữ ít: tia văng, cụm tàn lửa, mảnh theo chủ đề, dăm đá.
// Chỉ tướng Hỏa gọi các hàm này (hệ khác chỉ mượn Flame / Spark / Explode / BuiDap… không đổi).
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // nhóm vẽ của quả nổ lớn "no" và cột dung nham "nham": TRƯỚC tướng (người dùng xem trong game 2026-11-19: "có vài vụ nổ layer nằm dưới
        // địch nên không thấy rõ"; trước đó đặt sau lưng để khỏi che con bị trúng). Neo dời 0,15 thân về phía người ra chiêu (NoLech) cho
        // quả nổ ngả về phía đòn tới, bớt trùm mặt con bị trúng mà vẫn rõ.
        const int NoNhom = Front;
        const float NoLech = 0.15f;

        // cỡ cụm khói đuôi của vật bay lửa bán kính R: 1,5 R, kẹp trong 0,22–0,35 thân đối thủ
        static float KhoiCo(float R, float tH) => Mathf.Clamp(1.5f * R, 0.22f * tH, 0.35f * tH);
        // khói đuôi sẫm của Hỏa Sơn Long (final boss đảo Hỏa; người dùng 2026-11-19 đêm: "trail smoke sẫm màu hơn chút và trail để lại vệt dài
        // hơn chút nữa"; khuya: "phải là khói chứ không phải tô đen"): nhân màu khung khói thành xám nâu sẫm hơn khói thường một nấc, KHÔNG đen
        // (trước 0,6; 0,57; 0,55, rồi 0,72; 0,68; 0,66); soi ảnh chụp khuya: sáng thêm chút nữa (0,8; 0,76; 0,74), độ đặc do vệt đặt (0,8)
        static readonly Color KhoiSam = new Color(0.8f, 0.76f, 0.74f, 1);
        // HoaNo từ cỡ này trở lên mới có quả nổ "no"; nhỏ hơn chỉ là lửa trúng đích "trung_lua" (tên, vả, húc, nổ phụ, đạn nhỏ)
        const float NoLon = 0.85f;

        // góc + lật cho khung vẽ mũi về +x (cầu lửa bay sang phải, "trung_lua" đòn tới từ trái) để mũi chỉ theo d (toạ độ sân, y xuống), như FbFly
        static void FbHuong(Vector2 d, out float ang, out bool flip)
        {
            d = Unit(d);
            flip = d.x < 0;
            ang = flip ? Mathf.Atan2(d.y, -d.x) * Mathf.Rad2Deg : Mathf.Atan2(-d.y, d.x) * Mathf.Rad2Deg;
        }

        // khung vẽ sẵn có CỠ ĐỔI THEO TUỔI (Fb của HatFlip.cs giữ cỡ cố định): hk(k) = chiều cao khung (đơn vị sân), k = tuổi / đời; chạy đúng
        // `life` giây (lặp thì lặp, một lượt thì dừng ở khung cuối), hiện dần fadeIn, mờ dần fadeOut cuối đời
        //   alpha (2026-11-19 tối): độ đặc tối đa (lớp trước của lốc bao quanh đối thủ vẽ mờ); sx: giãn ngang (lốc trùm kín đối thủ)
        P FbH(string fx, Vector2 pos, Func<float, float> hk, int group, float layer, float life, float speed = 1, float start = 0, bool flip = false,
            float ang = 0, float fadeIn = 0.04f, float fadeOut = 0.15f, float alpha = 1, float sx = 1, Color? tint = null)
        {
            var art = FbArt(fx);
            if (art == null) return null;
            var d = Fbs[fx];
            float fps = d.fps * Mathf.Max(0.05f, speed);
            var col = tint ?? Color.white; // nhân màu (2026-11-19 khuya: khói đuôi xám nâu)
            var p = new P { pos = pos, group = group, life = Mathf.Max(0.05f, life) };
            p.draw = (q, k, buf) =>
            {
                float h = hk(k);
                if (h < 1) return;
                float a = alpha * Mathf.Min(1, q.age / Mathf.Max(0.01f, fadeIn)) * Mathf.Clamp01((q.life - q.age) / Mathf.Max(0.01f, fadeOut));
                if (Mathf.Abs(sx - 1) < 0.001f) DrawFb(buf, art, d, start + q.age * fps, q.pos, h, q.group, layer, ang, flip, col, a);
                else DrawFbW(buf, art, d, start + q.age * fps, q.pos, h, sx, q.group, layer, flip, col, a);
            };
            return Add(p);
        }

        // như DrawFb của HatFlip.cs (khung floor(f) đặc + khung kế chồng mờ theo phần lẻ) nhưng GIÃN NGANG sx lần quanh điểm neo, không xoay
        // (2026-11-19 tối: lốc lửa "loc_lua" trùm kín đối thủ; khung phễu hẹp ở 0,3 cao nên phải giãn ngang mới phủ được ngang thân)
        void DrawFbW(List<Item> buf, Sprite[] art, FbDef d, float f, Vector2 pos, float h, float sx, int g, float layer, bool flip, Color col, float a)
        {
            if (a < 0.02f) return;
            h *= d.k;
            int n = d.n, i;
            float u;
            if (d.loop)
            {
                f %= n;
                if (f < 0) f += n;
                i = (int)f;
                u = f - i;
            }
            else if (f >= n - 1)
            {
                i = n - 1;
                u = 0;
            }
            else
            {
                i = Mathf.Max(0, (int)f);
                u = Mathf.Clamp01(f - i);
            }
            float st = d.aspect * sx, w = h * st;
            float ox = (0.5f - d.px) * w, oy = (0.5f - d.py) * h;
            if (flip) ox = -ox;
            var center = pos + new Vector2(ox, -oy);
            Put(buf, g, layer, art[i], col, center, h, st, 0, a, 0, flip);
            if (u > 0.02f) Put(buf, g, layer + 0.001f, art[d.loop ? (i + 1) % n : Mathf.Min(n - 1, i + 1)], col, center, h, st, 0, a * u, 0, flip);
        }

        // LỬA TRÚNG ĐÍCH "trung_lua" tâm ở c (đặt ở thân, không ở đầu), khung cao h; d: hướng đòn bay tới (toạ độ sân), d = 0 thì lật ngẫu nhiên
        P HoaFbTrung(Vector2 c, float h, Vector2 d, int group = Front, float speed = 1.1f)
        {
            float ang = 0;
            bool flip;
            if (d.sqrMagnitude < 1e-6f) flip = U(0, 1) < 0.5f;
            else FbHuong(d, out ang, out flip);
            return Fb("trung_lua", c, h, group, 34, speed, ang, flip);
        }

        // NỔ bằng khung vẽ sẵn (thay HoaNo hạt): "trung_lua" ở tâm c (trước tướng, lật theo hướng đòn huong: +1 đòn bay sang phải, −1 sang trái,
        // 0 chưa biết); sc ≥ NoLon thêm quả nổ "no" neo ở chân `dat` (hoặc dưới tâm), TRƯỚC tướng (NoNhom; 2026-11-19 chiều: trước là sau lưng),
        // dời NoLech thân về phía người ra chiêu, phồng nhanh (bỏ 2,5 khung đầu), vệt cháy dưới chân khi to; sc nhỏ thì một cụm khói nhỏ muộn một
        // nhịp. Hạt phụ: vài tia văng, cụm tàn lửa, mảnh theo chủ đề.
        // Cỡ: "trung_lua" 0,6–1,1 thân (sc 0,36 → 0,69; 1 → 0,88); "no" 1,1–2,1 thân (sc 1 → 1,3; 1,5 → 1,7).
        void HoaNoFb(Vector2 c, float sc, float H, Vector2? dat, int group, float huong)
        {
            var d = huong == 0 ? Vector2.zero : new Vector2(huong, U(-0.15f, 0.15f));
            HoaFbTrung(c, Mathf.Clamp(0.58f + 0.3f * sc, 0.6f, 1.1f) * H, d, group);
            if (sc >= NoLon && HasFb("no"))
            {
                float h = Mathf.Clamp(0.45f + 0.85f * sc, 1.1f, 2.1f) * H;
                var chan = (dat.HasValue ? dat.Value + new Vector2(0, 1) : c + new Vector2(0, 0.45f * h)) + new Vector2(-huong * NoLech * H, 0);
                // nổ Blender (2026-11-24): khung 0 là sao chớp nhỏ, khối lửa phồng từ khung 1 → chỉ bỏ nửa khung đầu (khung GPT cũ bỏ 2,5)
                Fb("no", chan, h, NoNhom, 30, 1.15f, 0, huong < 0 || (huong == 0 && U(0, 1) < 0.5f), null, 1, -1, 0.5f);
                if (dat.HasValue && sc >= 0.8f) HoaVetChay(dat.Value + new Vector2(0, 2), 0.55f * H * sc);
            }
            else if (sc >= 0.45f) At(0.12f, () => HoaKhoi(c + new Vector2(0, -0.04f * H), (0.06f + 0.1f * sc) * H, Back, null, U(0.8f, 1f), false)); // khói đọng 0,25–0,3 thân
            float sq = Mathf.Sqrt(sc);
            int s1 = Mathf.RoundToInt(1 + 2 * sc);
            for (int i = 0; i < s1; i++) Spark(c + U2(-6, 6), U2(-1, 1), U(300, 480) * sq, 0, 7);
            HoaTan(c, new Vector2(U(-60, 60), -U(90, 150)), 0, sc < 0.6f ? 2 : 3);
            Extra(c, Mathf.RoundToInt(1 + 2 * sc), 300 * sc, group);
        }

        // CẦU LỬA VẼ SẴN ("cau_lua", lặp) bám điểm chạy tam(giờ sân), bán kính quả cầu rt(giờ sân): khung cao 4 bán kính (quả cầu cao nửa khung, tâm
        // cầu ở điểm neo 0,73; 0,46 của khung). bay true: mũi theo hướng đi đo trên đường tam, đuôi lửa sau; bay false (cầu đang tụ, đứng yên): mũi
        // chúc xuống, đuôi lửa BỐC LÊN, ngả về phía trước `huong` (±1) cho khỏi trùm mặt tướng. Thay khối cầu nhiều múi HoaCau.
        // khoi > 0 (2026-11-19, người dùng: "các fireball, tên lửa,... nên thêm trail smoke vào"): cầu đang bay nhả vệt khói đuôi FbKhoiDuoi cụm cao
        // khoi, điểm nhả sau tâm cầu nửa khung (gốc đuôi lửa), lớp dưới cầu; cầu đứng tụ không nhả
        // khoiTint, khoiSpeed (2026-11-19 đêm): màu nhân và tốc độ khung của vệt khói (Hỏa Sơn Long: sẫm hơn, chậm hơn = vệt dài hơn)
        P HoaFbCau(Func<float, Vector2> tam, Func<float, float> rt, float life, int group = Front, bool bay = true, float huong = 0, float khoi = 0,
            Color? khoiTint = null, float khoiSpeed = 1.9f)
        {
            // 2026-11-24 (bộ lửa Blender): cả cầu bay lẫn cầu đứng là "cau_lua" TRÒN (quả cầu cao nửa h nhờ FbDef.k → h = 4 bán kính); đuôi là vệt
            // "duoi_lua" thả theo quãng bay (DuoiLua). Bỏ "cau_bay" (đuôi dài vẽ sẵn, khung GPT 2026-11-19).
            const string fx = "cau_lua";
            const float hk = 4f;
            var art = FbArt(fx);
            if (art == null) return null;
            var d = Fbs[fx];
            var p = new P { pos = tam(T), life = Mathf.Max(0.05f, life), group = group, ph = U(0, d.n) };
            // hướng mũi (toạ độ sân): đang tụ = chúc xuống, ngả về sau (đuôi ngả về trước); đang bay = theo đường
            p.aim = bay ? Unit(tam(T + 0.02f) - tam(T)) : Unit(new Vector2(-0.35f * huong, 1));
            if (bay && p.aim.sqrMagnitude < 0.5f) p.aim = new Vector2(1, 0);
            p.upd = (q, dt, s) =>
            {
                var np = tam(s.T);
                if (bay)
                {
                    var mv = tam(s.T + 0.012f) - tam(s.T - 0.012f);
                    if (mv.sqrMagnitude > 0.01f) q.aim = Unit(mv);
                }
                q.pos = np;
                q.vel = Vector2.zero;
            };
            p.draw = (q, k, buf) =>
            {
                float r = rt(T);
                if (r < 1.5f) return;
                FbHuong(q.aim, out float ang, out bool flip);
                DrawFb(buf, art, d, q.ph + q.age * d.fps, q.pos, hk * r, q.group, 34, ang, flip, Color.white, Mathf.Min(1, q.age / 0.05f));
            };
            Add(p);
            if (bay && DuoiLua(() => p.pos, () => !p.dead && p.age < p.life, rt(T)) != null) return p;
            if (bay && khoi > 0) FbKhoiDuoi(() => p.pos - p.aim * (2f * rt(T)), () => !p.dead && p.age < p.life, khoi, 26, khoiTint, group, 27, khoiSpeed);
            return p;
        }

        // VỆT KHÓI BÔNG cho vật bay (2026-11-19 khuya; người dùng chê dải liền màu than: "trail khói của final boss đảo hỏa phải là khói chứ không
        // phải tô đen như vậy"; soi ảnh chụp: nhả theo giây thì đạn nhanh để các cụm cách quãng gần bằng cỡ cụm, thành cụm rời): nhả cụm khung "khoi"
        // theo QUÃNG ĐƯỜNG: cứ vật đi được `buoc` × cỡ cụm (0,33: các cụm chồng 2/3 lên nhau) thì đặt một cụm ở đúng chỗ trên đoạn vừa đi, nên vệt
        // bông liền dù vật bay nhanh hay chậm. Mỗi cụm sống `song` giây (chạy hết khung từ khung 3), nở thêm 15 % về cuối (cụm già), trôi lên chậm,
        // góc / lật ngẫu nhiên, cỡ chênh ít (0,92–1,08: không có cụm nhỏ rời ở mép). nha() chọn quãng nhả. tint nhân màu, alpha độ đặc.
        P HoaKhoiDuoi(Func<Vector2> where, Func<bool> alive, Func<bool> nha, float h, Color tint, float alpha = 0.8f, float buoc = 0.33f,
            float song = 0.6f, int group = Front, float layer = 26)
        {
            if (!HasFb("khoi") || where == null) return null;
            var last = where();
            float con = 0, step = Mathf.Max(2, buoc * h);
            float speed = (Fbs["khoi"].n - 3) / (Fbs["khoi"].fps * Mathf.Max(0.1f, song));
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
                if (nha == null || nha())
                {
                    // đặt cụm cách đều `step` dọc đoạn last → cur (con: phần quãng còn dư từ bước trước)
                    float x = step - con;
                    while (x <= len)
                    {
                        float hh = h * U(0.92f, 1.08f);
                        var pnt = last + seg * (x / Mathf.Max(1e-4f, len)) + new Vector2(U(-0.05f, 0.05f) * h, Fbs["khoi"].cy * hh); // neo chân: tâm cụm trên đường bay (cy: khung cũ 0,38, khói Blender 0,28)
                        var f = FbH("khoi", pnt, k => hh * (1 + 0.15f * k), group, layer + U(0, 0.5f), song * U(0.92f, 1.08f), speed, 3, U(0, 1) < 0.5f,
                            U(-14, 14), 0.01f, 0.06f, alpha, 1, tint);
                        if (f != null)
                        {
                            f.vel = new Vector2(U(-8, 8), -U(14, 24));
                            f.drag = 0.6f;
                        }
                        x += step;
                    }
                    con = len - (x - step);
                }
                else con = 0;
                last = cur;
            };
            return Add(e);
        }

        // CẦU LỬA ĐANG TỤ vẽ sẵn "cau_tu" (2026-11-19 đêm; người dùng chê cầu "cau_lua" đứng yên "xấu ... nhìn hơi tĩnh", muốn "làm lại 1 quả cầu
        // lửa mới"): lửa cuộn xoáy quanh lõi, bám điểm chạy tam(giờ sân), bán kính rt(giờ sân) (đã gồm phập phồng ~7 Hz và cú nén của HoaTuCau /
        // HoaNhip). Bù cỡ từng khung theo CauTuR (quả cầu nhìn bằng 2,3 rt), xoay chậm 35–55 độ/giây (chiều ngẫu nhiên), hiện dần 0,06 s.
        // 2026-11-24 (bộ lửa Blender): cầu đang tụ cũng là quả cầu tròn "cau_lua" (cùng hình với cầu bay, khỏi đổi kiểu lúc nhả), quả cầu nhìn bằng
        // 2,3 rt (h = 4,6 rt vì quả cầu cao nửa h), xoay chậm; khung "cau_tu" cũ (cỡ đổi trong vòng lặp, bù bằng CauTuR) không dùng nữa
        P HoaFbCauTu(Func<float, Vector2> tam, Func<float, float> rt, float life, int group = Front)
        {
            var art = FbArt("cau_lua");
            if (art == null) return null;
            var d = Fbs["cau_lua"];
            float quay = (U(0, 1) < 0.5f ? -1 : 1) * U(35, 55), a0 = U(0, 360);
            var p = new P { pos = tam(T), life = Mathf.Max(0.05f, life), group = group, ph = U(0, d.n) };
            p.upd = (q, dt, s) =>
            {
                q.pos = tam(s.T);
                q.vel = Vector2.zero;
            };
            p.draw = (q, k, buf) =>
            {
                float r = rt(T);
                if (r < 1.5f) return;
                DrawFb(buf, art, d, q.ph + q.age * d.fps, q.pos, 4.6f * r, q.group, 34, a0 + quay * q.age, false, Color.white, Mathf.Min(1, q.age / 0.06f));
            };
            return Add(p);
        }

        // TÀN LỬA XOẮN VÀO cầu đang tụ: đốm than nhỏ (emberg nhuộm màu than của chủ đề) sinh ở `tu`, hiện dần, bay xoắn ốc nhanh dần vào tâm (cùng
        // đường với vệt hút HoaHut), chạm vành cầu thì nhập vào; quá `het` (giờ sân tuyệt đối: cầu đã rời chỗ) thì tắt
        P HoaTanXoan(Func<float, Vector2> tam, Func<float, float> rt, Vector2 tu, float life, float chieu, float het, int group = Front)
        {
            var o = tu - tam(T);
            var p = new P
            {
                pos = tu, life = life, group = group, seed = rng.Next(2), col = Th.ember, R0 = Mathf.Max(8, o.magnitude), ph = Mathf.Atan2(o.y, o.x),
                tip = chieu * U(2f, 3f), sz = U(4, 6.5f), launch = het
            };
            p.upd = (q, dt, s) =>
            {
                if (s.T > q.launch)
                {
                    q.dead = true;
                    return;
                }
                float k = Mathf.Clamp01(q.age / q.life), e = k * k * (0.35f + 0.65f * k);
                float rho = q.R0 * (1 - e), an = q.ph + q.tip * e;
                q.pos = tam(s.T) + new Vector2(Mathf.Cos(an), Mathf.Sin(an)) * rho;
                q.vel = Vector2.zero;
                if (rho <= rt(s.T) * 0.85f) q.dead = true;
            };
            p.draw = (q, k, buf) => Put(buf, q.group, 41, S("emberg_" + (q.seed & 1)), q.col, q.pos, q.sz * (1 - 0.4f * k), 1, 0, Mathf.Min(1, k / 0.2f));
            return Add(p);
        }

        // LỐC LỬA VẼ SẴN "loc_lua" (2026-11-19 tối; người dùng chê lốc cũ "màu hơi trầm và chưa hợp lắm"): phễu lửa lặp, chân ở `chan`, khung cao h
        // (rộng ≈ 0,95 h), xoáy từ t0 tới t1 (giây từ lúc gọi): cao vọt lên trong 0,2 s đầu, hiện dần, tắt dần 0,25 s cuối. boc (lốc bao quanh đối
        // thủ): thêm lớp TRƯỚC lệch pha nửa vòng, lật ngang, nhỏ hơn 5 %, mờ `mo` (phía gần của lốc đi qua trước thân mà vẫn thấy con bị trúng);
        // lớp sau đặc (Back). Trả false khi chưa nhập ảnh (hàm gọi về hạt cũ).
        // sx (2026-11-19 đêm, người dùng: "lốc xoáy làm to lên cho che hết tướng địch"): giãn ngang. Phễu trong khung rộng ≈ 0,3 khung ở cổ (0,3 cao),
        // 0,54 ở giữa, 0,8 ở miệng; cao 1,7 thân + giãn 1,55 thì ngang giữa ≈ 1,4 thân, cổ ≈ 0,8 thân, miệng ≈ 2,1 thân, chân rộng ≈ 1,2 thân.
        // hBao > 0 (2026-11-19 khuya; lốc BAO QUANH đối thủ): có khung "loc_lua_bao" (lốc trùm, cột xoáy dày, gốc gần rộng bằng miệng: rộng ≈ 0,6 khung
        // ở 0,2–0,4 cao, 0,86 ở 0,7 cao) thì dùng nó, cao hBao, giãn ngang sxBao (1,65 thân × 1,2: ngang thân ≈ 1,2 thân, miệng ≈ 1,7 thân, trùm
        // từ chân tới đầu, hết hở cổ phễu); chưa nhập thì về "loc_lua" cao h, giãn sx
        bool HoaFbLoc(Vector2 chan, float h, float t0, float t1, bool boc = true, float mo = 0.55f, float speed = 1.15f, float sx = 1, float hBao = 0,
            float sxBao = 1.2f)
        {
            string fx = "loc_lua";
            // 2026-11-24 (bộ lửa Blender): "loc_lua" là MỘT LƯỢT 2 s (tự mọc từ đất, xoắn, gió cuốn, tàn bay vòng, ép về trục) → phát co giãn
            // đúng t0..t1, không lặp, không tự phóng to; phễu mảnh (cổ ≈ 0,3 khung cao, miệng ≈ 0,6) nên cao 1,8 thân (lấy theo hBao nếu có), giãn
            // ngang 1,45 → ngang giữa ≈ 0,8 thân, miệng ≈ 1,6 thân; lớp trước cùng khung, cùng pha, mờ `mo` (lật thì dải xoắn bắt chéo nhau)
            if (HasFb(fx) && !Fbs[fx].loop)
            {
                float lf = Mathf.Max(0.3f, t1 - t0), hh = 1.06f * Mathf.Max(h, hBao);
                float sp = FbDur(fx) / lf;
                At(Mathf.Max(0, t0), () =>
                {
                    FbH(fx, chan, _ => hh, Back, 26, lf, sp, 0, false, 0, 0.04f, 0.12f, 1, 1.45f);
                    if (boc) FbH(fx, chan + new Vector2(0, 2), _ => hh, Front, 26, lf, sp, 0, false, 0, 0.04f, 0.12f, mo, 1.45f);
                });
                return true;
            }
            if (hBao > 0 && HasFb("loc_lua_bao"))
            {
                fx = "loc_lua_bao";
                h = hBao;
                sx = sxBao;
            }
            else if (!HasFb("loc_lua")) return false;
            float life = Mathf.Max(0.3f, t1 - t0), k0 = Mathf.Min(0.6f, 0.2f / life), ph = U(0, 24);
            Func<float, float> co = k => h * (0.25f + 0.75f * EaseOut(k / k0));
            At(Mathf.Max(0, t0), () =>
            {
                FbH(fx, chan, co, Back, 26, life, speed, ph, false, 0, 0.12f, 0.25f, 1, sx);
                if (boc) FbH(fx, chan + new Vector2(0, 2), k => 0.95f * co(k), Front, 26, life, speed, ph + 12, true, 0, 0.12f, 0.25f, mo, sx);
            });
            return true;
        }

        // CỤM LỬA CHÁY "lua_lap" chân ở `chan`: vọt lên trong `len` giây đầu (cỡ hMax), giữ, hạ còn (1 − ha) ở cuối đời rồi tắt dần; lệch pha ngẫu
        // nhiên để các cụm không đập cùng nhịp
        P HoaFbLua(Vector2 chan, float hMax, float life, int group = Front, float layer = 24, float len = 0.08f, float ha = 0.45f, float speed = 1)
        {
            float k0 = Mathf.Clamp01(len / Mathf.Max(0.05f, life));
            return FbH("lua_lap", chan, k => hMax * (k0 > 0 ? EaseOut(k / k0) : 1) * (1 - ha * SmoothStep(0.5f, 1, k)), group, layer, life, speed,
                U(0, 24), U(0, 1) < 0.5f, 0, 0.03f, Mathf.Min(0.18f, 0.3f * life));
        }

        // PHUN LỬA vẽ sẵn "phun" (bộ lửa Blender 2026-11-24; người dùng duyệt nhịp 2026-11-24: "ngọn lửa phải bùng từ từ lên mới to dần và tan biến",
        // khói "thêm vào phần zone gần cuối chứ không phải cuối"): một khung dài neo ở miệng, xoay theo hướng miệng → đích, giãn dọc (sx) cho mép đầu
        // lúc dài nhất (0,93 bề ngang khung) tới mặt trước thân đối thủ mà không dày quá ~1 thân. Nhịp khung gốc: mép đầu vươn 0–0,75 s, giữ, đứt khỏi
        // miệng ở 1,27 s, vỡ mảnh tới 1,92 s → bắt đầu ở 0,1 s (sau nhịp lấy hơi), chạy nhanh hơn chút để đứt đúng lúc tướng thôi giữ dáng (BreathHold).
        // Khói: 5 cụm "khoi" ở mép trên, 62–78 % chiều dài, 1,02–1,4 s khung gốc (như dự án AtomSpine atom_bl). Giữ: lấy hơi xoắn vào miệng, tia văng
        // dọc luồng, chớp + rung + đối thủ chớp lúc chạm, mây xoắn (swirl). Trả giờ chạm.
        float BreathFb(Vector2 mouth, Vector2 target, float tH, bool swirl)
        {
            var art = FbArt("phun");
            var d = Fbs["phun"];
            string pal = Th.pal;
            var dd = target - mouth;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            var up = nrm.y < 0 ? nrm : -nrm;
            float Hit = Mathf.Max(34, 0.26f * tH);
            var cham = mouth + u * (dist - Hit);
            float L = Mathf.Max(60, dist - 0.35f * Hit);                // mép đầu lúc dài nhất
            float hNat = L / (0.932f * d.aspect), hT = Mathf.Min(hNat, 0.95f * tH), sx = hNat / hT;
            const float tS = 0.1f, TachGoc = 1.27f;                  // giờ bắt đầu; giờ (khung gốc) luồng đứt khỏi miệng
            float sp = TachGoc / Mathf.Max(0.5f, BreathHold - tS - 0.02f);
            float G(float tg) => tS + tg / sp;                         // giờ khung gốc → giờ từ lúc gọi
            float tHit = G(0.58f), tEnd = G(TachGoc);
            float chieu = U(0, 1) < 0.5f ? 1 : -1;
            Every(0, 0.22f, 36, x =>
            {
                float a = U(0, 6.28f);
                HoaHut(t => mouth, t => 7, mouth + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(50, 82), U(0.18f, 0.24f), Pal[pal][U(0, 1) < 0.5f ? 1 : 2], chieu,
                    T + 0.3f);
            });
            FbHuong(u, out float ang, out bool flip);
            float dur = d.n / (d.fps * sp);
            At(tS, () =>
            {
                var p = new P { pos = mouth, group = Front, life = dur };
                p.draw = (q, k, buf) => DrawFb(buf, art, d, q.age * d.fps * sp, mouth, hT, Front, 36, ang, flip, Color.white, 1, sx);
                Add(p);
            });
            // khói vùng gần cuối luồng: (giờ khung gốc, phần chiều dài, cao trên trục theo px khung gốc 313, cỡ khung khói / khung lửa)
            float px = hT / 313f;
            foreach (var (tg, fl, dy, sc) in new[] { (1.02f, 0.61f, 85f, 0.55f), (1.1f, 0.71f, 100f, 0.65f), (1.18f, 0.66f, 70f, 0.6f), (1.28f, 0.78f, 95f, 0.62f),
                         (1.4f, 0.69f, 80f, 0.55f) })
            {
                float f = fl, y = dy, s = sc;
                At(G(tg), () =>
                {
                    float hk = 361f * s * px;
                    var c = mouth + u * (L * f) + up * (y * px);
                    var k = Fb("khoi", c + new Vector2(0, Fbs["khoi"].cy * hk), hk, Back, 12, 1, U(-8, 8), U(0, 1) < 0.5f);
                    if (k != null)
                    {
                        k.vel = new Vector2(U(10, 30) * px * (u.x >= 0 ? 1 : -1), -U(90, 130) * px);
                        k.drag = 0.4f;
                    }
                });
            }
            // tia văng dọc luồng (thay chùm đốm than vfx.burst của bản AtomSpine)
            Every(G(0.3f), tEnd, 8, x =>
            {
                float f = U(0.25f, 0.8f), sd = U(0, 1) < 0.5f ? -1 : 1;
                Spark(mouth + u * L * f + nrm * sd * U(0.1f, 0.3f) * hT, u * U(0.5f, 1) + nrm * sd * U(0.4f, 0.9f) + new Vector2(0, -0.3f), U(260, 420), 0, 7);
            });
            if (swirl || Th.extra == "may") // Lân Hỏa, Ngưu Quyền: mây xoắn vàng bay dọc luồng
                Every(G(0.4f), tEnd, 10, x => Extra(mouth + u * L * U(0.3f, 0.9f) + up * U(10, 30), 1, 120));
            At(tHit, () =>
            {
                Shake?.Invoke(0.25f);
                HoaChop(cham, 0.36f * tH, 0.09f);
                for (int i = 0; i < 4; i++)
                {
                    float a = Mathf.Atan2(-u.y, -u.x) + U(-1.4f, 1.4f);
                    Spark(target + U2(-10, 10), new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.5f), U(250, 460), 0, 7);
                }
                Extra(target, 3, 300);
            });
            Every(tHit, tEnd, 5, x => HoaTrung?.Invoke(target, 0.3f));
            At(tEnd + 0.1f, () =>
            {
                for (int i = 0; i < 4; i++) Ash(target + U2(-30, 30));
            });
            return tHit;
        }

        // THIÊN THẠCH vẽ sẵn (bộ lửa Blender 2026-11-24, như clip thien_thach của dự án AtomSpine atom_bl): quả cầu lửa tròn "cau_lua" lao chéo xuống
        // (đường cong nhanh dần như bản cũ) kéo vệt "duoi_lua" dày, chạm đất thì nổ "no" lớn + "trung_lua" (HoaNoFb), cụm khói "khoi" toả quanh, vòng
        // sóng, đá văng, vết nứt. Thay hòn đá + chuỗi lưỡi lửa + khói hạt + vành lưỡi lửa của bản cũ. Giờ trúng như cũ (0,75 s).
        float MeteorFb(Vector2 foeFeet, float tH, float fromSide)
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
            float r = Mathf.Max(26, 0.17f * tH);
            HoaFbCau(t => Path(t - t0), t => r * (1 + 0.05f * Mathf.Sin(t * 38)), TI, Front, true);
            Every(0.05f, TI, 18, x => Spark(Path(T - t0), -dv + U2(-0.6f, 0.6f), U(150, 300)));
            At(TI, () =>
            {
                Shake?.Invoke(0.9f);
                FlashScreen?.Invoke(new Color(1, 0.96f, 0.84f, 0.45f));
                HoaNoFb(foeFeet + new Vector2(0, -0.4f * tH), 1.6f, tH, foeFeet, Front, -fromSide);
                Ring(foeFeet + new Vector2(0, 2), 0.4f, 0.2f * tH, 1.6f * tH, Th.ring);
                At(0.1f, () => Ring(foeFeet + new Vector2(0, 2), 0.35f, 0.1f * tH, 1.2f * tH, Th.ring2));
                for (int i = 0; i < 8; i++)
                {
                    float a = (-90 + U(-70, 70)) * Mathf.Deg2Rad;
                    Rock(imp, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(350, 650), foeFeet.y + U(-15, 25));
                }
                for (int i = 0; i < 12; i++) Spark(imp + U2(-12, 12), new Vector2(U(-1, 1), -U(0.3f, 1)), U(300, 560));
                // cụm khói toả quanh chỗ nổ, muộn một nhịp (boom_smoke của atom_bl: 6 cụm quanh tâm, bay lên, toả ra)
                At(0.25f, () =>
                {
                    for (int i = 0; i < 6; i++)
                    {
                        float a = i / 6f * 6.28f + U(-0.4f, 0.4f);
                        var o = new Vector2(Mathf.Cos(a), 0.5f * Mathf.Sin(a));
                        HoaKhoi(imp + o * 0.35f * tH + new Vector2(0, -0.45f * tH), U(0.17f, 0.24f) * tH, Back, o * U(30, 60) + new Vector2(0, -U(60, 100)),
                            U(1.1f, 1.4f), false);
                    }
                });
                for (int i = 0; i < 10; i++) Ash(imp + U2(-40, 40), new Vector2(U(-80, 80), -U(80, 160)));
                Extra(imp + new Vector2(0, -20), 8, 420);
                var cr = new P { pos = foeFeet + new Vector2(0, 2), life = 1.5f, group = Floor, sz = tH };
                cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_1"), Color.white, q.pos, 1.6f * q.sz * 0.42f, 1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.3f));
                Add(cr);
            });
            return TI;
        }
    }
}
