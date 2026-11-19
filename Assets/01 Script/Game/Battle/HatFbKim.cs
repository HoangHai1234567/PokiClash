// KHUNG VẼ SẴN CHO HỆ KIM (2026-11-19): hàm dùng chung đưa bộ khung vẽ sẵn 24 khung (HatFlip.cs: Fb, FbDur, DrawFb) vào hiệu ứng 10 tướng
// Kim. Người dùng chê (2026-11-18/19): gai sắt đâm lên xấu, nổ chưa đẹp, khói rải rác chưa cụm chưa mềm, lửa rời rạc; duyệt bộ khung mới ("ổn
// hơn rồi đấy, cho vào game đi"). Mỗi hàm trả false / null khi chưa nhập ảnh khung: hàm gọi tự rơi về hạt cũ.
// - KmNoFb: nổ to → khung "no" neo ở đất; nổ nhỏ (đạn, tên lửa, nhịp đốt) → khung "trung_lua" ở tâm; cả hai TRƯỚC tướng (KmNo gọi).
// - KmDuoiKhoi: vệt khói đuôi khung "khoi" (FbKhoiDuoi của HatFlip.cs) cho vật bay theo đường hàm giờ sân (đạn, cầu năng lượng, móc lửa).
// - KmKhoiFb: cụm khói than / khói hồn → khung "khoi" (KmKhoi gọi). Đuôi đạn, hơi xì, khói xám nhạt giữ hạt cũ (khung nâu xám chỉ nhân màu
//   được, không sáng lên thành xám nhạt).
// - KmLuaFb: lưỡi lửa chữ S đỏ cam → khung "lua_lap" mọc, cháy, co (KmLuaS gọi). Lửa hồn xanh giữ hạt cũ (nhuộm khung cam ra xanh xỉn).
// - KmGaiVong: vòng gai đâm lên quanh chân đối thủ → khung "gai_sat" nhuộm màu (Thiết Tinh, Thiết Khoáng).
// - KmCotLuaFb: thân cột lửa → ba khung "lua_lap" chồng nhau sau lưng đối thủ (Quỷ Xích).
// - KmCauBam: lửa bọc thiên thạch của rig → khung "cau_lua" bám theo (Nhật Vương).
// - KmBuiFb: cụm bụi đất lúc đất nổ tung → khung "khoi" nhuộm nâu đất (Thiết Khoáng).
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // màu nhuộm khung (nhân màu: chỉ tối đi, không sáng lên). Khung "gai_sat" xám thép ~ (160, 165, 180); khung "khoi" nâu xám ~ (140, 124, 116)
        static readonly Color KmKhoiHonFb = C(170, 225, 205);                     // khói hồn xám xanh (Vong Kỵ) ~ (93, 109, 93)
        static readonly Color KmBuiFbC = C(255, 226, 178);                        // bụi đất nâu ấm (Thiết Khoáng) ~ (140, 110, 80)
        static readonly Color SatTimFb = C(228, 212, 255), SatThepFb = C(212, 224, 255);   // tinh thể oải hương ~ (143, 137, 180), thép lam ~ (133, 145, 180)
        static readonly Color KhSatFb = C(196, 200, 214), KhSatFb2 = C(220, 224, 236);     // quặng sắt (Thiết Khoáng dạng 1)
        static readonly Color KhDoFb = C(245, 140, 112), KhDoFb2 = C(226, 118, 100);       // hematit đỏ gỉ (Thiết Khoáng dạng 2)
        bool kmNoLat;

        // NỔ bằng khung vẽ sẵn (KmNo gọi, bảng lửa đỏ cam "luat" và năng lượng vàng "vtuoi"; lửa hồn giữ hạt cũ vì khung lửa cam nhuộm xanh ra
        // xỉn). Cỡ và nhịp như bản hạt: D = 0,68 tH · sc^0,6. Nổ to (sc ≥ 0,8): khung "no" neo ở ĐẤT dưới tâm, cao 1,6 D (chiêu cuối sc 1,5–1,8
        // ra 1,4–1,55 lần thân); lật xen kẽ cho các đợt nổ chồng nhau khỏi thành bóng đôi. Nổ nhỏ (đạn, tên lửa, nhịp đốt): khung "trung_lua"
        // ở tâm, cao 1,5 D (0,5–0,75 lần thân), nhanh 1,3 lần cho khỏi che lâu. Cả hai vẽ TRƯỚC tướng (bản đầu vẽ sau: người dùng chê nằm dưới
        // địch không thấy rõ), neo dời về phía người ra chiêu. Bỏ khối khói múi tròn và lưỡi liềm của bản hạt (khung đã có lửa, khói nâu, mảnh
        // khuyết); giữ chớp 2 khung, vòng cung dẹt, vệt cháy, tia bắn rồi khựng, đá, mảnh theo chủ đề. Trả false nếu chưa nhập ảnh.
        bool KmNoFb(Vector2 c, Vector2 dat, float tH, float sc, string pal, float huong)
        {
            bool nho = sc < 0.8f, lon = sc >= 1.1f;
            if (!HasFb(nho ? "trung_lua" : "no")) return false;
            KmPal();
            var cols = KmBang(pal);
            float D = 0.68f * tH * Mathf.Pow(sc, 0.6f);
            // 2026-11-19 (người dùng xem trong game: "có vài vụ nổ layer nằm dưới địch nên không thấy rõ"): mọi khung nổ vẽ TRƯỚC tướng, neo
            // dời 0,1 thân (nổ nhỏ) / 0,2 thân (nổ to) về phía người ra chiêu cho bớt che mặt mà vẫn thấy rõ (huong: hướng đòn, +1 = sang phải)
            float lui = -huong * (nho ? 0.1f : 0.2f) * tH;
            if (nho)
            {
                // khung vẽ cho đòn tới từ TRÁI: đòn bay sang trái (huong < 0) thì lật
                Fb("trung_lua", c + new Vector2(lui, 0), 1.5f * D, Front, 31, 1.3f, U(-8, 8), huong < 0);
                KmChop(c, 0.34f * D, 0.06f, cols);
            }
            else
            {
                kmNoLat = !kmNoLat;   // lật xen kẽ + lệch ngang nhẹ: hai đợt nổ sát nhau (thiên thạch, đợt nổ phụ) không thành bóng đôi
                Fb("no", new Vector2(c.x + lui + (kmNoLat ? 0.08f : -0.08f) * D, dat.y + 2), 1.6f * D, Front, 30, lon ? 1f : 1.15f, 0, kmNoLat);
                KmChop(c, (lon ? 0.3f : 0.38f) * D, lon ? 0.07f : 0.06f, cols);   // nổ lớn: cục chớp nhỏ lấy đà 2 khung
            }
            At(lon ? 0.06f : 0.035f, () =>
            {
                KmCung(dat + new Vector2(0, 2), 0.12f * D, (0.9f + 0.3f * sc) * D, 0.34f, cols[4]);
                if (sc >= 0.5f) KmChay(dat + new Vector2(0, 3), 0.42f * D, 0.9f + 0.2f * sc, 0.9f);
                int ns = Mathf.Clamp(Mathf.RoundToInt(1 + 3 * sc), 2, 7);
                for (int i = 0; i < ns; i++)
                {
                    float a = U(0, 6.28f);
                    KmTiaLua(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f), U(520, 820) * Mathf.Sqrt(sc), U(6, 9), (i & 1) == 0 ? cols[4] : cols[3]);
                }
                if (lon)
                    for (int i = 0; i < 3; i++)
                        Rock(dat + new Vector2(huong * U(0, 0.25f) * tH, -8), new Vector2(huong * U(80, 320), -U(260, 480)), dat.y + U(-4, 6), U(9, 13));
                if (sc >= 0.5f) Extra(c, Mathf.RoundToInt(2 * sc), 300 * Mathf.Sqrt(sc), Front);
            });
            return true;
        }

        // CỤM KHÓI bằng khung "khoi" (phồng, bay lên, tan thành mảnh), cùng chỗ, cỡ, đời với cụm hạt cũ (KmKhoi gọi). Khung lúc đầy rộng ~0,98,
        // cao ~0,9 khung, cụm hạt cũ rộng ~2,2 r rồi tách cụm toả ra: khung cao 3 r, neo chân dưới tâm cụm 0,42 khung; tốc độ theo đời. Trôi
        // chậm theo vel, lớp 11 (dưới lửa, tia). hon: nhuộm khói hồn xám xanh. Trả null nếu chưa nhập ảnh.
        P KmKhoiFb(Vector2 pos, Vector2 vel, float r, float life, int group, bool hon, float tro)
        {
            if (!HasFb("khoi")) return null;
            float h = 3f * r;
            var p = Fb("khoi", pos + new Vector2(0, 0.42f * h), h, group, 11, Mathf.Clamp(FbDur("khoi") / Mathf.Max(0.3f, life), 0.7f, 1.6f), U(-6, 6),
                rng.Next(2) == 0, hon ? KmKhoiHonFb : (Color?)null);
            p.vel = vel * 0.5f;
            p.drag = 2;
            if (tro > 0 && U(0, 1) < tro) p.onDeath = (q, s) => s.Ash(q.pos + new Vector2(s.U(-0.3f, 0.3f) * h, -0.6f * h), null, q.group);
            return p;
        }

        // VỆT KHÓI ĐUÔI cho vật bay theo đường bay(giờ sân) trong dur giây (người dùng 2026-11-19: "các fireball, tên lửa,... nên thêm trail
        // smoke vào"): FbKhoiDuoi (HatFlip.cs) nhả cụm khung "khoi" ở điểm lùi `lui` sau vật theo hướng bay, thôi nhả khi hết dur, các cụm đã
        // nhả tự tan. Lớp 18: dưới lưỡi lửa đuôi (20+) và thân đạn / cầu (24+). Trả false nếu chưa nhập ảnh khung "khoi".
        bool KmDuoiKhoi(Func<float, Vector2> bay, float dur, float h, float lui, float rate, int group = Front, float layer = 18)
        {
            if (!HasFb("khoi")) return false;
            float het = T + dur;
            FbKhoiDuoi(() =>
            {
                // hướng bay lấy về phía trước (lúc mới hiện, điểm trước đó của bảng rig là chỗ ẩn); hết đường thì lấy về sau
                var p = bay(T);
                var d = bay(T + 0.02f) - p;
                if (d.sqrMagnitude < 1e-4f) d = p - bay(T - 0.02f);
                return p - Unit(d) * lui;
            }, () => T < het, h, rate, null, group, layer);
            return true;
        }

        // khung (lặp hoặc một lượt) đứng ở chân `chan`: mọc từ 0,35 lên đủ cỡ trong `moc` giây, cuối co về `co` lần cỡ và mờ trong `tat` giây;
        // pha đầu ngẫu nhiên (start < 0) để nhiều cụm cùng lúc không nháy đồng loạt
        P KmFbMoc(string fx, Vector2 chan, float h, float life, int group, float layer, float moc, float tat, float co, bool lat, float speed = 1,
            Vector2 vel = default, float start = -1)
        {
            var art = FbArt(fx);
            if (art == null) return null;
            var d = Fbs[fx];
            float ph = start >= 0 ? start : U(0, d.n), fps = d.fps * speed;
            var p = new P { pos = chan, vel = vel, drag = 2.2f, life = Mathf.Max(0.05f, life), group = group, sz = h };
            p.draw = (q, k, buf) =>
            {
                float con = q.life - q.age;
                float g = (moc > 0 ? Mathf.Lerp(0.35f, 1, EaseOut(q.age / moc)) : 1) * Mathf.Lerp(co, 1, Mathf.Clamp01(con / Mathf.Max(0.01f, tat)));
                float a = Mathf.Clamp01(con / Mathf.Max(0.01f, 0.6f * tat));
                DrawFb(buf, art, d, ph + q.age * fps, q.pos, q.sz * g, q.group, layer, 0, lat, Color.white, a);
            };
            return Add(p);
        }

        // LƯỠI LỬA ĐỎ CAM bằng khung "lua_lap" (KmLuaS gọi): cụm lửa liền khối có lưỡi chữ S, giọt tách, mọc nhanh, cháy, co rồi tắt như lưỡi
        // hạt cũ; chân đứng yên (trôi chậm theo vel), không bay lên. Khung lửa cao ~0,9 khung, ảnh kr_lua cũ ~0,85 ô: cao 1,05 h.
        P KmLuaFb(Vector2 chan, float h, float life, int group, Vector2 vel) =>
            KmFbMoc("lua_lap", chan, 1.05f * h, life, group, 22, 0.2f * life, 0.5f * life, 0.35f, rng.Next(2) == 0, 1, vel * 0.5f);

        // VÒNG GAI ĐÂM LÊN quanh chân đối thủ (chiêu cuối Thiết Tinh, Thiết Khoáng) bằng khung "gai_sat" (đất nứt, gai phóng, giữ, vỡ vụn), thay
        // các cột kim rời bị chê "gai sắt đâm lên xấu": ba cụm sau lưng (cụm giữa cao 1,35 thân, hai cụm ±0,42 cao 1,1 ló trên vai), hai cụm
        // trước 0,9 thân lệch ±0,6 thân hai bên chân, một cụm thấp 0,5 chếch phía trước. Bỏ 5 khung nứt đất đầu (cú dập đã chạm), chạy 1,5 lần:
        // đủ cao sau ~0,17 s, vỡ hết ~0,53 s như cột cũ; lần lượt 0–0,08 s. chinh / phu: màu nhuộm khung xám thép (cụm giữa + hai cụm trước / hai cụm sau bên). Trả false nếu chưa nhập ảnh.
        bool KmGaiVong(Vector2 feet, float tH, float manh, Color chinh, Color phu)
        {
            if (!HasFb("gai_sat")) return false;
            float s = tH * manh;
            // 2026-11-19 (soi ảnh chụp trong game: thân đối thủ che gần hết ba cụm sau, hai cụm trước 0,62 nhỏ): cụm sau to hơn, ló trên đầu và
            // trên vai; hai cụm trước 0,9 thân lệch ±0,6 thân ra hai bên chân; thêm một cụm thấp 0,5 chếch phía trước (bên ngẫu nhiên). Không
            // đặt cụm cao ngay trước mặt
            float ben = rng.Next(2) == 0 ? -1 : 1;
            Gai(new Vector2(0, -0.1f), 1.35f, Front, 0, false, chinh); // lớp TRƯỚC (người dùng 2026-11-19: "gai đất, nổ đang bị lỗi layer hiện đằng sau tướng địch")
            Gai(new Vector2(-0.42f, -0.08f), 1.1f, Front, 0.03f, true, phu);
            Gai(new Vector2(0.42f, -0.08f), 1.1f, Front, 0.04f, false, phu);
            Gai(new Vector2(-0.6f, 0.12f), 0.9f, Front, 0.05f, false, chinh);
            Gai(new Vector2(0.6f, 0.12f), 0.9f, Front, 0.06f, true, chinh);
            Gai(new Vector2(ben * 0.22f, 0.2f), 0.5f, Front, 0.08f, ben > 0, phu);
            return true;

            // o: lệch so với chân (phần thân, y sân đi xuống: âm = lùi ra sau); cao: phần thân
            void Gai(Vector2 o, float cao, int g, float tre, bool lat, Color tint)
            {
                var at = feet + o * s;
                float hh = cao * s * U(0.92f, 1.08f), sp = 1.5f * U(0.94f, 1.06f), ang = U(-7, 7);
                At(tre, () => Fb("gai_sat", at, hh, g, 43, sp, ang, lat, tint, 1, -1, 5));
            }
        }

        // THÂN CỘT LỬA (Quỷ Xích) bằng khung "lua_lap": ba cụm lửa lặp chồng nhau sau lưng đối thủ (dưới to, lên trên nhỏ dần: chân ở 0 / 0,27 /
        // 0,5 chiều cao cột, cao 0,6 / 0,52 / 0,46 cột, ngọn trên cùng ~0,95 cột), mọc lần lượt từ dưới lên trong ~0,3 s, cháy suốt `dur`, cuối co
        // và mờ; thay ~90 lưỡi lửa rời của bản hạt. Trả false nếu chưa nhập ảnh.
        bool KmCotLuaFb(Vector2 feet, float cao, float dur)
        {
            if (!HasFb("lua_lap")) return false;
            float[] y = { 0, 0.27f, 0.5f }, h = { 0.6f, 0.52f, 0.46f };   // chồng sâu (soi bản ghép thử: chồng nông thì thành ba cục rời)
            for (int i = 0; i < 3; i++)
            {
                int ii = i;
                At(0.07f * i, () => KmFbMoc("lua_lap", feet + new Vector2(U(-4, 4), 4 - y[ii] * cao), h[ii] * cao, dur + 0.15f - 0.07f * ii, Back,
                    21 - 0.1f * ii, 0.16f, 0.35f, 0.5f, ii == 1, 1 + 0.12f * ii));
            }
            return true;
        }

        // LỬA BỌC THIÊN THẠCH của rig (Nhật Vương) bằng khung "cau_lua" (cầu lửa, đuôi lửa sau, lặp): bám vat(giờ sân) trong dur giây, đầu cầu
        // theo hướng bay `huong` (sân; khung vẽ bay sang phải, bay sang trái thì lật như FbFly), vẽ SAU tướng nên đá của rig vẫn nằm trên; thay
        // chuỗi lưỡi lửa của đuôi. Trả false nếu chưa nhập ảnh.
        bool KmCauBam(Func<float, Vector2> vat, float dur, float h, Vector2 huong)
        {
            var art = FbArt("cau_lua");
            if (art == null) return false;
            var d = Fbs["cau_lua"];
            var u = Unit(huong);
            bool lat = u.x < 0;
            float ang = lat ? Mathf.Atan2(u.y, -u.x) * Mathf.Rad2Deg : Mathf.Atan2(-u.y, u.x) * Mathf.Rad2Deg;
            float ph = U(0, d.n);
            var p = new P { pos = vat(T), life = Mathf.Max(0.05f, dur), group = Back };
            p.upd = (q, dt, s) =>
            {
                q.pos = vat(s.T);
                q.vel = Vector2.zero;
            };
            p.draw = (q, k, buf) => DrawFb(buf, art, d, ph + q.age * d.fps, q.pos, h, q.group, 24, ang, lat, Color.white, Mathf.Clamp01(q.age / 0.04f));
            Add(p);
            return true;
        }

        // BỤI ĐẤT NỔ TUNG (Thiết Khoáng cắm hố, trồi lên, húc từ dưới) bằng khung "khoi" nhuộm nâu đất: hai cụm hai bên chỗ nổ, SAU tướng, lật
        // đối xứng, thay vòng cụm bụi rời. H: chiều cao thân tham chiếu; sc: cỡ. Trả false nếu chưa nhập ảnh.
        bool KmBuiFb(Vector2 dat, float H, float sc)
        {
            if (!HasFb("khoi")) return false;
            for (int i = 0; i < 2; i++)
            {
                float sd = i == 0 ? -1 : 1;
                var p = Fb("khoi", dat + new Vector2(sd * U(0.16f, 0.24f) * H * sc, U(-3, 2)), 0.5f * H * sc * U(0.9f, 1.1f), Back, 11, 1.25f * U(0.92f, 1.08f),
                    -sd * U(4, 10), sd > 0, KmBuiFbC);   // ngả ra ngoài (góc dương = ngược kim đồng hồ)
                p.vel = new Vector2(sd * U(40, 90) * sc, -U(10, 30));
                p.drag = 2.5f;
            }
            return true;
        }
    }
}
