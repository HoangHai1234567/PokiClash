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
                Fb("no", chan, h, NoNhom, 30, 1.15f, 0, huong < 0 || (huong == 0 && U(0, 1) < 0.5f), null, 1, -1, 2.5f);
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
            // 2026-11-19 đêm: cầu BAY dùng khung mới "cau_bay" (lửa cuộn quanh đầu, đuôi dài quẫy; đầu cầu ở 0,78; 0,48, quả cầu cao ≈ 0,52 khung nên
            // khung cao 3,8 bán kính) khi đã nhập; chưa có thì "cau_lua" (khung cao 4 bán kính)
            string fx = bay && HasFb("cau_bay") ? "cau_bay" : "cau_lua";
            float hk = fx == "cau_bay" ? 3.8f : 4f;
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
                        var pnt = last + seg * (x / Mathf.Max(1e-4f, len)) + new Vector2(U(-0.05f, 0.05f) * h, 0.38f * hh); // neo chân: tâm cụm trên đường bay
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

        // bán kính tương đương (căn diện tích phủ / π, phần chiều cao khung) của từng khung "cau_tu": khung tự phồng (khung 0 nhỏ, khung 12 to nhất)
        // trong vòng lặp 1 s; chia cho số này để cỡ cầu do mã điều khiển (lớn dần theo pha tụ, phập phồng nhanh), không theo nhịp 1 Hz của khung
        static readonly float[] CauTuR =
        {
            0.256f, 0.268f, 0.281f, 0.298f, 0.309f, 0.316f, 0.326f, 0.336f, 0.343f, 0.353f, 0.365f, 0.377f,
            0.379f, 0.375f, 0.362f, 0.348f, 0.341f, 0.334f, 0.327f, 0.309f, 0.303f, 0.286f, 0.274f, 0.268f,
        };

        // CẦU LỬA ĐANG TỤ vẽ sẵn "cau_tu" (2026-11-19 đêm; người dùng chê cầu "cau_lua" đứng yên "xấu ... nhìn hơi tĩnh", muốn "làm lại 1 quả cầu
        // lửa mới"): lửa cuộn xoáy quanh lõi, bám điểm chạy tam(giờ sân), bán kính rt(giờ sân) (đã gồm phập phồng ~7 Hz và cú nén của HoaTuCau /
        // HoaNhip). Bù cỡ từng khung theo CauTuR (quả cầu nhìn bằng 2,3 rt), xoay chậm 35–55 độ/giây (chiều ngẫu nhiên), hiện dần 0,06 s.
        P HoaFbCauTu(Func<float, Vector2> tam, Func<float, float> rt, float life, int group = Front)
        {
            var art = FbArt("cau_tu");
            if (art == null) return null;
            var d = Fbs["cau_tu"];
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
                float f = (q.ph + q.age * d.fps) % d.n, a = Mathf.Min(1, q.age / 0.06f), ang = a0 + quay * q.age;
                int i = (int)f, j = (i + 1) % d.n;
                float u = f - i;
                Put(buf, q.group, 34, art[i], Color.white, q.pos, 1.15f * r / CauTuR[i], d.aspect, ang, a);
                if (u > 0.02f) Put(buf, q.group, 34.001f, art[j], Color.white, q.pos, 1.15f * r / CauTuR[j], d.aspect, ang, a * u);
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
    }
}
