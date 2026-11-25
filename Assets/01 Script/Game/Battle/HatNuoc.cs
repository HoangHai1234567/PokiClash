// Bộ Thủy của lớp hạt chồng lớp phẳng (2026-11-10; chuyển từ ArtGen/Spine/bo_thuy.py, sổ công thức ở skill pokiclash-fx-congthuc
// mục 5b). Hạt nước (lưỡi sóng cuộn, giọt, bọt, vương miện nước) là ảnh xám GPT nhuộm bằng Image.color; khối nước lớn (lõi tia, con
// sóng thần, lưỡi trăng khuyết, cột phun, thân vòi rồng) là mảng đa giác tô phẳng gửi sang HatMang.
// Khác bộ Hỏa: chiêu nước được gọi lúc clip BẮT ĐẦU, kèm lead = thời gian tới khung nhả của clip. Pha tụ nước chạy trong lúc tướng
// lấy đà, nước nhả đúng khung nhả (người dùng 2026-11-10: sửa animation cho khớp hiệu ứng). Hàm trả thời gian tới lúc trúng.
// Biến tĩnh ở file này không được dùng biến tĩnh của HatLua.cs lúc khởi tạo (thứ tự khởi tạo giữa hai file không chắc).
// 2026-11-18 (người dùng chê tia cụt lủn, nước chưa như Kingdom Rush, bọt rải rác, pha tụ xấu, màu tối): bảng màu nước tươi; hình hạt
// kiểu Kingdom Rush hat_kr_* (có hình cũ dự phòng); tia nước chạm tận thân, loe ra ôm thân, bông toé liên tục, đuôi đứt bay nốt rồi vỡ;
// pha tụ bằng vệt xoắn ốc nhập vào cầu nước sóng sánh; toé kiểu Kingdom Rush (mão đục lỗ, khối văng → giọt → chấm, vành giọt, vệt ướt);
// đạn có đuôi liền chia theo quãng bay; bọt thành cụm. Báo cáo: Temp/vfx_thuy/BAO_CAO.md.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // ---------- chủ đề nước theo tướng ----------
        public sealed class WTheme
        {
            public Color[] w; // mực, xanh đậm, xanh giữa, xanh nhạt, bọt
            public Theme fx; // họa tiết thêm (dùng lại Extra của bộ Hỏa): mảnh băng, sao...
            // tia nước CHIÊU CUỐI to theo thân người bắn (2026-11-19): nửa bề dày lõi tia = tiaTo × casterH (chặn 22–29 = 2–2,6 lần tia chiêu
            // cuối thường 11); 0 = tia thường. Dùng cho tướng há mồm rất to phun luồng nước (Thôn Kình)
            // Tia vẽ sẵn (2026-11-19): bề dày tia chiêu cuối = 2,2 × tiaTo × casterH (Thôn Kình ~0,33 casterH)
            public float tiaTo;
        }

        static Color[] WPal(Color d, Color m, Color l) => new[] { C(43, 33, 24), d, m, l, C(244, 252, 255) };

        // bảng nước tươi (người dùng 2026-11-18: "màu tươi hơn", sân bãi cát sáng, trời xanh): lam đậm sát viền #2B7FD0, lam #4EB6F2,
        // lam nhạt #9FE0FF, kem #F2FBFF (bọt). Không lam xám, không xanh đục. Bảng từng tướng Thủy dưới đây giữ sắc của tướng nhưng nâng
        // sáng và độ bão hoà theo bảng này.
        static readonly WTheme WDefault = new WTheme { w = WPal(C(43, 127, 208), C(78, 182, 242), C(159, 224, 255)) };
        static readonly Dictionary<string, WTheme> WThemes = new Dictionary<string, WTheme>
        {
            // lô 10 tướng mới đảo Thủy (2026-11-11), màu theo bảng màu từng dòng (ArtGen/Spine/inbox/tm0*_ghichu.md); mực và bọt chung
            // giọt mưa võ sĩ: lam đại dương #1F5DB5, lam ngọc sáng #35BFE6, bọt nhạt
            { "ti_tach", new WTheme { w = WPal(C(36, 116, 210), C(64, 190, 244), C(166, 232, 255)) } }, // 2026-11-18: nâng sáng
            // cua ẩn sĩ nhà đá: giáp chàm #3D5486, vỏ lam xám #6A8BBB, lam bọt #BFE6E2; mảnh đá bazan văng
            // suất này nay là dòng ếch xanh (2026-11-11): bỏ họa tiết mảnh đá của cua; màu nước tạm giữ, chờ người dùng chọn
            // 2026-11-18: lam xám tạm của cua làm cầu nước của ếch đục, tối (ảnh trước) → bảng nước tươi chung
            { "thach_giai", new WTheme { w = WPal(C(43, 127, 208), C(78, 182, 242), C(159, 224, 255)) } },
            // nòng nọc / ếch xoáy: cô-ban #2457C5, cerulean #3FA9E0, vây nhạt #9FE1F0
            { "ca_den", new WTheme { w = WPal(C(58, 100, 216), C(96, 162, 248), C(178, 214, 255)) } },   // chàm của cá đèn lồng; 2026-11-18: chàm tím sẫm làm tia tối → lam chàm tươi
            // hà mã: hồn nước ba lam #2B7FD6, #4FB6EE, #A6DEF8
            { "ha_ba", new WTheme { w = WPal(C(43, 127, 214), C(79, 184, 244), C(166, 230, 255)) } },
            // sò ngọc: mòng két #1F9AA8, ngọc lam #36C2B4, ngọc lam nhạt #7ED8CB; gai san hô cam văng
            // suất này nay là dòng bạch tuộc quái vật (2026-11-12, mã bach_tuoc): nước là MỰC, đen tím than nhạt dần; bỏ gai san hô
            // 2026-11-18: mực vẫn đen nhưng toé có ánh tím tươi (người dùng: tông tối, xám thì nâng sáng, tăng bão hoà); bọt tím rất nhạt
            { "so_ngoc", new WTheme { w = new[] { C(43, 33, 24), C(34, 28, 50), C(98, 64, 162), C(186, 142, 246), C(240, 230, 255) } } },
            // kỳ giông mưa bão: chàm bão #34477E, xanh đá mưa #6E88BC, lam nhạt #9CC0E8; mây giông xám bay lên
            { "giong_bao", new WTheme { w = WPal(C(46, 96, 204), C(52, 186, 222), C(188, 242, 254)) } },   // pháp sư nước: chàm của mũ, lam ngọc của áo, lam băng (2026-11-18: chàm sáng lên)
            // cá voi biến dị (2026-11-11, thay cá voi sen): lam đá sẫm #2F4A6E, lam biển #4F86B0, trắng băng #BFE3EE; mảnh đá đen văng
            // 2026-11-19 (người dùng: "chiêu cuối tướng này tia nước nhỏ quá"): cá voi há mồm rất to nên tia chiêu cuối dày theo thân (tiaTo)
            { "lien_kinh", new WTheme { w = WPal(C(40, 112, 196), C(84, 164, 232), C(196, 238, 252)), fx = new Theme { extra = "tinh_the", extraCol = C(58, 56, 66) }, tiaTo = 0.15f } },
            // rắn vực sâu: chàm vực #2E2F6E, chàm xám #5058A8, bạc hà #8FE3D0; chấm đèn bạc hà
            { "uyen_xa", new WTheme { w = WPal(C(38, 98, 214), C(70, 162, 246), C(152, 226, 255)) } },   // rắn nước có sừng (2026-11-11): lam cô-ban của thân, nhạt dần về màu đốm bong bóng; bỏ họa tiết sao của rắn đèn cũ
            // cá sấu băng: petrol sẫm #1F5566, petrol #3C8396, cạnh băng #9DBAC6; mảnh băng đục
            // suất này nay là dòng rồng vây (2026-11-12, mã rong_vay): chàm của thân #34408F, lam ngọc của vây #49BFC4, lam nhạt; bỏ mảnh băng
            { "han_ngac", new WTheme { w = WPal(C(44, 106, 208), C(58, 198, 218), C(178, 240, 246)) } }, // 2026-11-18: lốc xám đục (ảnh trước) → lam tươi
            // rồng biển nhiều đầu: ngọc bích sẫm, ngọc bích #2FA79B, bạc hà #A6E6D8; sao vàng như gạc
            { "hai_long", new WTheme { w = WPal(C(26, 140, 152), C(52, 198, 192), C(172, 242, 230)), fx = new Theme { extra = "sao", extraCol = C(233, 184, 74) } } },
            // đảo Mộc, tinh linh rừng mập (2026-11-12, dòng Mầm Ú, id mam_u; chiêu lá ở HatMoc.cs): lục lá đậm của mầm, lục non, lục nhạt của thân;
            // sao vàng văng lúc húc bụng
            { "mam_u", new WTheme { w = WPal(C(62, 140, 88), C(156, 204, 92), C(206, 230, 140)), fx = new Theme { extra = "sao", extraCol = C(255, 226, 120) } } },
            // đảo Mộc, Cầu Gai (2026-11-12, suất tien_la; chiêu gai ở HatMoc.cs): lục sẫm của thân, lục non, kem của gai; sao kem văng lúc trúng
            { "tien_la", new WTheme { w = WPal(C(52, 120, 72), C(132, 186, 96), C(238, 226, 176)), fx = new Theme { extra = "sao", extraCol = C(250, 240, 200) } } },
            // đảo Mộc, Gạc Đá (2026-11-12, suất gac_da; chiêu ở HatDa.cs): lục ngọc của hạt mầm (đậm, tươi, nhạt); đá vụn nâu xám văng lúc trúng
            // đảo Mộc, Lâm Tượng (2026-11-12, ma mút rừng, suất phong_linh; chiêu ở HatVoi.cs): lục sẫm và lục tươi của áo lá, sao màu mật của ngà
            { "phong_linh", new WTheme { w = WPal(C(40, 124, 66), C(100, 176, 74), C(170, 212, 84)), fx = new Theme { extra = "sao", extraCol = C(238, 212, 150) } } },
            { "gac_da", new WTheme { w = WPal(C(30, 150, 104), C(64, 206, 140), C(170, 236, 196)), fx = new Theme { extra = "giap", extraCol = C(128, 120, 104) } } },
            // Thiết Khoáng (bo_ngua, đảo Kim): chiêu mana n_da_va (hai tay quặng găm): bụi đất nâu, mảnh quặng sắt đen
            { "bo_ngua", new WTheme { w = WPal(C(110, 82, 56), C(150, 118, 84), C(206, 186, 160)), fx = new Theme { extra = "giap", extraCol = C(70, 72, 82) } } },
            // đảo Mộc, Lộc Phong (2026-11-12, suất bom_la; chiêu ở HatLoc.cs): lục bảo của pha lê và vân nhựa trên gạc (đậm, tươi, nhạt); sao vàng lá phong văng lúc trúng
            { "bom_la", new WTheme { w = WPal(C(30, 150, 110), C(64, 206, 150), C(184, 240, 212)), fx = new Theme { extra = "sao", extraCol = C(240, 172, 62) } } },
            // đảo Mộc, Linh Điểu (2026-11-12, chim bảo hộ rừng, suất gio_loc; chiêu ở HatChim.cs; 2026-11-17 bị Cổ Vương đè nhầm, trả lại 2026-11-19): lục sẫm của gân lá, lục lá cánh, lục non; cánh hoa hồng của cành cánh văng lúc trúng
            { "gio_loc", new WTheme { w = WPal(C(42, 106, 58), C(76, 154, 82), C(147, 198, 99)), fx = new Theme { extra = "canh_sen", extraCol = C(242, 166, 188) } } },
            // đảo Thổ, Cổ Vương (2026-11-17, tượng vua cổ rễ quấn cầm cột, tướng 6 đảo Thổ, suất hat_de từ 2026-11-19; chiêu ở HatCoVuong.cs): lục sẫm, lục lá, lục non của lá trên rễ; dăm đá xám lục văng lúc trúng
            { "hat_de", new WTheme { w = WPal(C(58, 104, 52), C(109, 190, 69), C(160, 216, 104)), fx = new Theme { extra = "giap", extraCol = C(120, 128, 110) } } },
            // đảo Mộc, Voọc Tướng (2026-11-12, voọc kiếm sĩ giáp lá, suất tho_hoang; chiêu ở HatKiem.cs): lục sẫm của mũ giáp, lục lá, lục non của lá cài mũ; sao vàng của đinh giáp và tua văng lúc trúng
            { "tho_hoang", new WTheme { w = WPal(C(34, 96, 52), C(84, 160, 70), C(176, 222, 120)), fx = new Theme { extra = "sao", extraCol = C(246, 196, 72) } } },
            // đảo Mộc, người cây đầm lầy (2026-11-12, suất long_vuot; dây gai và quả cầu dây leo là mảnh của rig): lục sẫm của dây gai, lục rêu thân, lục rêu vai; kem của gai văng lúc trúng
            // đảo Mộc, rồng trúc bốn cánh (2026-11-13, boss cuối, suất thanh_long; chiêu ở HatRong.cs): lục bảo sẫm, lục bảo, lục non của cánh; sao vàng ngà của giáp
            { "thanh_long", new WTheme { w = WPal(C(30, 84, 62), C(52, 140, 92), C(150, 212, 140)), fx = new Theme { extra = "sao", extraCol = C(236, 196, 80) } } },
            { "long_vuot", new WTheme { w = WPal(C(47, 82, 51), C(78, 122, 62), C(124, 164, 74)), fx = new Theme { extra = "sao", extraCol = C(239, 224, 168) } } },
            // đảo Mộc, Giác Mộc (2026-11-13, thú cổ thụ một sừng, suất moc_tinh; chiêu ở HatGiac.cs): hổ phách sẫm, hổ phách tươi, vàng nhạt của tinh thể sừng và quả tim; sao kem
            { "moc_tinh", new WTheme { w = WPal(C(214, 134, 32), C(250, 190, 60), C(255, 232, 150)), fx = new Theme { extra = "sao", extraCol = C(255, 246, 200) } } },
        };

        WTheme wth = WDefault;
        Color[] W => wth.w;
        static readonly Color FoamC = C(244, 252, 255);
        static readonly float[] WF = { 1, 1, 0.8f, 0.58f, 0.36f };
        // phần hình chiếm trong khung vuông của ảnh hat_crown_<i> (rộng, cao); 0, 1: vương miện nhìn ngang; 2, 3: nước toé nhìn thẳng
        static readonly Vector2[] CrownF = { new Vector2(0.928f, 0.554f), new Vector2(0.928f, 0.554f), new Vector2(0.928f, 0.909f), new Vector2(0.928f, 0.924f) };

        void UseWater(string heroId) => wth = heroId != null && WThemes.TryGetValue(heroId, out var t) ? t : WDefault;

        void WExtra(Vector2 at, int n, float speed, int group = Front)
        {
            if (wth.fx == null) return;
            var old = Th;
            Th = wth.fx;
            Extra(at, n, speed, group);
            Th = old;
        }

        public bool HasWater => S("wave_0") && S("drop_0") && S("foam_0");

        // ---------- mảng nước liền ----------
        static Color32 A32(Color c, float alpha)
        {
            c.a *= alpha;
            return c;
        }

        void MFill(int g, float layer, int a0, int n, Color c, float alpha = 1, bool fringe = true) =>
            ms.Add(new MShape { group = g, layer = layer, kind = HatMang.Fill, a0 = a0, b0 = -1, n = n, col = A32(c, alpha), fringe = fringe });

        void MBand(int g, float layer, int a0, int b0, int n, Color c, float alpha = 1, bool fringe = false) =>
            ms.Add(new MShape { group = g, layer = layer, kind = HatMang.Band, a0 = a0, b0 = b0, n = n, col = A32(c, alpha), fringe = fringe });

        void MRibbon(int g, float layer, int a0, int b0, int n, Color c, float alpha = 1) =>
            ms.Add(new MShape { group = g, layer = layer, kind = HatMang.Ribbon, a0 = a0, b0 = b0, n = n, col = A32(c, alpha), fringe = true });

        // đường viền nở ra ngoài d (toạ độ sân); trả chỉ số đầu của đường mới (cùng số điểm)
        int MGrow(int a0, int n, float d)
        {
            float area = 0;
            for (int i = 0; i < n; i++)
            {
                Vector2 p = mp[a0 + i], q = mp[a0 + (i + 1) % n];
                area += p.x * q.y - p.y * q.x;
            }
            float sign = area > 0 ? 1 : -1;
            int s = mp.Count;
            for (int i = 0; i < n; i++)
            {
                Vector2 p = mp[a0 + i], e1 = p - mp[a0 + (i + n - 1) % n], e2 = mp[a0 + (i + 1) % n] - p;
                Vector2 n1 = new Vector2(e1.y, -e1.x), n2 = new Vector2(e2.y, -e2.x);
                if (n1.sqrMagnitude > 1e-8f) n1.Normalize();
                if (n2.sqrMagnitude > 1e-8f) n2.Normalize();
                var vn = n1 + n2;
                float len = vn.magnitude;
                vn = len > 1e-4f ? vn / len : n2;
                mp.Add(p + vn * (sign * d / Mathf.Max(0.5f, Vector2.Dot(vn, n2))));
            }
            return s;
        }

        // đường thu về mid theo (kx, ky) rồi dời shift
        int MScale(int a0, int n, Vector2 mid, Vector2 k, Vector2 shift)
        {
            int s = mp.Count;
            for (int i = 0; i < n; i++)
            {
                var p = mp[a0 + i] - mid;
                mp.Add(mid + new Vector2(p.x * k.x, p.y * k.y) + shift);
            }
            return s;
        }

        readonly List<Vector2> ctl = new List<Vector2>(32);

        // đường cong kín Catmull-Rom qua các điểm trong ctl; trả chỉ số đầu, số điểm = ctl.Count * seg
        int MSmooth(int seg = 4)
        {
            int m = ctl.Count, s = mp.Count;
            for (int i = 0; i < m; i++)
            {
                Vector2 p0 = ctl[(i + m - 1) % m], p1 = ctl[i], p2 = ctl[(i + 1) % m], p3 = ctl[(i + 2) % m];
                for (int j = 0; j < seg; j++)
                {
                    float t = (float)j / seg;
                    mp.Add(0.5f * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * (t * t) + (3 * p1 - p0 - 3 * p2 + p3) * (t * t * t)));
                }
            }
            return s;
        }

        // một mảng đặc có viền mực
        void MSolid(int g, float layer, int a0, int n, Color c, float alpha = 1, float ink = 2.4f)
        {
            if (ink > 0) MBand(g, layer, MGrow(a0, n, ink), a0, n, Ink, alpha, true);
            MFill(g, layer + 0.001f, a0, n, c, alpha, ink <= 0);
        }

        // mảng nước lồi ba lớp lồng nhau (mực, đậm, giữa, nhạt), các lớp KHÔNG chồng nhau nên làm trong mờ được
        void MNested(int g, float layer, int a0, int n, Color[] w, Vector2 mid, Vector2 k2, Vector2 k3, Vector2 shift, float alpha = 1, float ink = 2.4f)
        {
            int b = MScale(a0, n, mid, k2, shift), c = MScale(a0, n, mid, k3, shift * 2);
            MBand(g, layer, MGrow(a0, n, ink), a0, n, Ink, alpha, true);
            MBand(g, layer + 0.001f, a0, b, n, w[1], alpha);
            MBand(g, layer + 0.002f, b, c, n, w[2], alpha);
            MFill(g, layer + 0.003f, c, n, w[3], alpha, false);
        }

        // ---------- hạt nước ----------
        void DrawWave(P p, float k, List<Item> buf)
        {
            float r = p.r0 + (p.r1 - p.r0) * EaseOut(k / 0.3f);
            r *= 1 - SmoothStep(p.fade, 1, k);
            if (r < 1) return;
            float sp = p.vel.magnitude;
            var d = sp > 30 ? Unit(p.vel / sp * (0.6f * p.tip) + new Vector2(0, -p.tipUp)) : new Vector2(0, -1);
            float ang = TipAngle(d);
            var w = p.stops ?? W;
            for (int i = 0; i < 5; i++)
            {
                float rad = r * WF[i];
                if (rad < 1) continue;
                Put(buf, p.group, 20 + i, S((i == 0 ? "waves_" : "wave_") + (p.seed & 3)), w[i], p.pos + d * (r - rad) * 0.55f,
                    2.7f * rad + (i == 0 ? 5 : 0), 1, ang);
            }
        }

        public P Wave(Vector2 pos, Vector2 vel, float life, float r0, float r1, int group = Front, float tip = 1, float up = 0.25f, float drag = 1,
            float accY = 0, float fade = 0.72f, float foamP = 0)
        {
            if (NS) return NLuoiNuoc(pos, vel, life, r0, r1, group, drag, accY); // bộ nước shader: lưỡi nước thon
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = drag, acc = new Vector2(0, accY), seed = rng.Next(4), r0 = r0, r1 = r1, group = group,
                tip = tip, tipUp = up, fade = fade, ph = U(0, 6.28f), stops = W
            };
            p.draw = DrawWave;
            if (foamP > 0)
                p.onDeath = (q, s) =>
                {
                    if (s.U(0, 1) < foamP) s.Foam(q.pos, null, 0, 4, 11, q.group);
                };
            return Add(p);
        }

        // 2026-11-18: giọt nhỏ hơn (người dùng: giọt lẻ to quá), hình giọt Kingdom Rush hat_kr_giot nếu đã nhập
        void DrawDrop(P p, float k, List<Item> buf)
        {
            float s = 2.3f * p.sz * (1 - SmoothStep(0.8f, 1, k));
            if (s < 1) return;
            float sp = p.vel.magnitude;
            var d = sp > 5 ? p.vel / sp : new Vector2(0, 1);
            PutGiot(buf, p.group, 40, p.pos, d, s, p.stops ?? W, p.seed, sp);
        }

        // một giọt lệ ba lớp (mực, giữa, nhạt lệch về đầu). hat_kr_giot: đầu tròn ở +x, quay đầu ra trước, giọt rơi nhanh (mưa) kéo dài
        // theo tốc độ. Dự phòng hat_drop: ngọn nhọn chĩa lên, quay cho đuôi nhọn ra sau hướng bay
        void PutGiot(List<Item> buf, int g, float layer, Vector2 pos, Vector2 d, float s, Color[] w, int sd, float sp = 0)
        {
            var gi = SK("kr_giot_", sd);
            if (gi != null)
            {
                float ang = VelAng(d), st = 1 + 0.9f * Mathf.Clamp01((sp - 300) / 600);
                Put(buf, g, layer, SK("kr_giots_", sd) ?? gi, Ink, pos, s + 3.5f, (s * st + 3.5f) / (s + 3.5f), ang);
                Put(buf, g, layer + 0.3f, gi, w[2], pos, s, st, ang);
                Put(buf, g, layer + 0.6f, gi, w[3], pos + d * s * 0.12f, s * 0.56f, st, ang);
                return;
            }
            float a2 = TipAngle(-d);
            Put(buf, g, layer, S("drops_" + (sd & 3)), Ink, pos, s + 4, 1, a2);
            Put(buf, g, layer + 0.3f, S("drop_" + (sd & 3)), w[2], pos, s, 1, a2);
            Put(buf, g, layer + 0.6f, S("drop_" + (sd & 3)), w[3], pos + d * s * 0.1f, s * 0.56f, 1, a2);
        }

        public P Drop(Vector2 pos, Vector2 vel, float life = 0, float r = 5, float grav = 900, int group = Front, float ground = float.NaN,
            float drag = 0.6f)
        {
            if (NS) return NGiot(pos, vel, r * 0.8f, group, life > 0 ? life : 0.7f, grav, ground); // bộ nước shader: giọt tròn
            var p = new P
            {
                pos = pos, vel = vel, life = life > 0 ? life : U(0.5f, 0.9f), drag = drag, acc = new Vector2(0, grav), seed = rng.Next(4), sz = r,
                group = group, stops = W
            };
            if (!float.IsNaN(ground))
            {
                p.ground = ground;
                p.life = 2;
                p.onGround = (q, s) =>
                {
                    s.Plop(q.pos);
                    q.dead = true;
                };
            }
            p.draw = DrawDrop;
            return Add(p);
        }

        // vòng không viền mực (vòng mảnh có viền thì thành vòng đen)
        P RingN(Vector2 pos, float life, float R0, float R1, Color col, float squash = 0.3f, int group = Floor, float layer = 30)
        {
            if (NS) return NRipple(pos, R0, R1, life); // bộ nước shader: vành gợn
            var p = new P { pos = pos, life = life, group = group, col = col, R0 = R0, R1 = R1, hgt = squash, ph = layer };
            p.draw = (q, k, buf) =>
            {
                float R = q.R0 + (q.R1 - q.R0) * EaseOut(k);
                Put(buf, q.group, q.ph, S("ring"), q.col, q.pos, 2 * R * q.hgt, 1 / q.hgt, 0, 1 - Mathf.Max(0, (k - 0.7f) / 0.3f));
            };
            return Add(p);
        }

        void Plop(Vector2 pos) => RingN(pos, 0.3f, 2, 11, FoamC, 0.36f);

        public P Foam(Vector2 pos, Vector2? vel = null, float life = 0, float r0 = 4, float r1 = 11, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel ?? new Vector2(U(-20, 20), U(-40, -10)), life = life > 0 ? life : U(0.45f, 0.75f), drag = 2.5f,
                seed = rng.Next(4), r0 = r0, r1 = r1, group = group, ang = U(0, 6.28f), spin = U(-1, 1)
            };
            p.draw = (q, k, buf) =>
            {
                float r = k < 0.25f ? q.r0 + (q.r1 - q.r0) * EaseOut(k / 0.25f) : q.r1 * (1 - 0.9f * SmoothStep(0.25f, 1, k));
                float a = 1 - SmoothStep(0.7f, 1, k);
                if (r < 1 || a < 0.03f) return;
                float g = q.ang * Mathf.Rad2Deg;
                Put(buf, q.group, 30, S("foams_" + (q.seed & 3)), Ink, q.pos, 2 * r + 3.5f, 1, g, a);
                Put(buf, q.group, 31, S("foam_" + (q.seed & 3)), FoamC, q.pos, 2 * r, 1, g, a);
            };
            return Add(p);
        }

        // vòng sóng dưới đất: dải màu có viền + vòng bọt trắng mảnh bên trong
        void Ripple(Vector2 pos, float R0, float R1, float life = 0.5f, Color? col = null)
        {
            RingN(pos, life, R0 * 0.82f, R1 * 0.82f, FoamC, 0.3f, Floor, 30.8f);
            Ring(pos, life, R0, R1, col ?? W[2]);
        }

        // vương miện nước (mão) mọc từ mặt đất (người dùng 2026-11-18: toé như Kingdom Rush): to nhất ngay khung đầu, các lưỡi nhọn chĩa
        // lên; ở 30% đời bị đục lỗ (hat_kr_maolo), từ 50% sụp xuống và vỡ thành giọt văng ra từ các ngọn; trên đất còn vành giọt elip.
        // Ảnh hat_kr_mao: chân giữa đáy khung vuông (đáy hình ở ~96% khung, hình rộng ~92% khung). Chưa nhập: vương miện cũ (CrownCu).
        void Crown(Vector2 feet, float wd, float life = 0.42f, int group = Front)
        {
            if (NS)
            {
                NCrownDat(feet, wd, life, group);
                return;
            }
            // khung vẽ sẵn (2026-11-19): vương miện nước toé từ đất nuoc_toe (dâng, xoè ngọn, vỡ giọt, còn vũng mỏng) thay mão kr_mao + vành
            // giọt + giọt sụp. Bề ngang ngọn lúc xoè nhất ~ 1,05 × cao khung nên cao = 0,95 × wd; mão ngắn đời (mưa) thì chạy nhanh hơn. Lớp
            // trước tướng thì trong mờ 0,92 (mão lớn dưới chân che chân đối thủ)
            if (FbNuoc("nuoc_toe"))
            {
                ToeNuoc(feet, 0.95f * wd, Mathf.Clamp(0.8f / Mathf.Max(0.1f, life), 1.3f, 2.2f), group, 34, group == Front ? 0.92f : 1);
                return;
            }
            if (SK("kr_mao_", 0) == null)
            {
                CrownCu(feet, wd, life, group);
                return;
            }
            life = Mathf.Max(life, 0.5f);
            var p = new P { pos = feet, life = life, group = group, seed = rng.Next(4), wd = wd, stops = W };
            p.draw = (q, k, buf) =>
            {
                float s = q.wd / 0.92f;
                float gx = 1 + 0.14f * SmoothStep(0.45f, 1, k);
                float gy = (k < 0.06f ? 0.86f + 0.14f * k / 0.06f : 1) * (1 - 0.8f * SmoothStep(0.5f, 1, k));
                float a = 1 - SmoothStep(0.78f, 1, k);
                if (gy < 0.05f || a < 0.03f) return;
                bool lo = k > 0.3f && SK("kr_maolo_", q.seed) != null;
                string bv = lo ? "kr_maolo_" : "kr_mao_", bs = lo ? "kr_maolos_" : "kr_maos_";
                var w = q.stops;
                for (int i = 0; i < 4; i++)
                {
                    float f = i < 2 ? 1 : i == 2 ? 0.8f : 0.58f; // lớp trong nhỏ dần, cùng chân: mép đậm, lõi nhạt
                    float hs = s * f * gy, ws = s * f * gx, ext = i == 0 ? 5 : 0;
                    var spr = i == 0 ? SK(bs, q.seed) ?? SK(bv, q.seed) : SK(bv, q.seed);
                    Put(buf, q.group, 34 + i * 0.1f, spr, i == 0 ? w[0] : w[i], q.pos - new Vector2(0, 0.46f * hs), hs + ext, (ws + ext) / (hs + ext), 0, a);
                }
            };
            Add(p);
            VanhGiot(feet + new Vector2(0, 2), 0.6f * wd, life + 0.15f);
            var th = wth;
            int nd = Mathf.Clamp((int)(wd / 13), 3, 9);
            At(life * 0.5f, () => InW(th, () => // mão sụp: các ngọn vỡ thành giọt
            {
                for (int i = 0; i < nd; i++)
                {
                    float x = U(-0.42f, 0.42f);
                    Drop(feet + new Vector2(x * wd, -U(0.45f, 0.8f) * wd), new Vector2(Mathf.Sign(x) * U(50, 150), -U(40, 150)), 0, U(2, 3.4f), 900,
                        U(0, 1) < 0.6f ? group : Back, feet.y + U(-6, 10));
                }
            }));
        }

        // vành giọt elip trên đất sau cú toé (Kingdom Rush): nở nhẹ rồi các giọt nhỏ dần, mờ ở nửa sau. Ảnh hat_kr_vanh (i = 0, 1) đã dẹt
        // sẵn nên vẽ khung vuông; chưa nhập thì vòng nước dẹt không viền.
        void VanhGiot(Vector2 feet, float R, float life = 0.55f)
        {
            var p = new P { pos = feet, life = life, group = Floor, seed = rng.Next(2), sz = R, stops = W };
            p.draw = (q, k, buf) =>
            {
                float R2 = q.sz * (0.7f + 0.3f * EaseOut(k / 0.4f));
                float a = 1 - SmoothStep(0.55f, 1, k);
                var v = SK("kr_vanh_", q.seed & 1);
                if (v != null)
                {
                    Put(buf, Floor, 5, SK("kr_vanhs_", q.seed & 1) ?? v, Ink, q.pos, 2 * R2 + 3, 1, 0, a);
                    Put(buf, Floor, 5.1f, v, q.stops[3], q.pos, 2 * R2, 1, 0, a);
                    return;
                }
                Put(buf, Floor, 5, S("ring"), q.stops[3], q.pos, 2 * R2 * 0.3f, 1 / 0.3f, 0, a);
            };
            Add(p);
        }

        // vương miện nước bản cũ (hat_crown_0, 1): mọc từ mặt đất rồi lún xuống (đáy bám đất)
        void CrownCu(Vector2 feet, float wd, float life = 0.42f, int group = Front)
        {
            var p = new P { pos = feet, life = life, group = group, seed = rng.Next(2), wd = wd, stops = W };
            p.draw = (q, k, buf) =>
            {
                float g = k < 0.28f ? EaseOut(k / 0.28f) : 1 - SmoothStep(0.5f, 1, k);
                var f = CrownF[q.seed];
                for (int i = 0; i < 5; i++)
                {
                    float side = q.wd / f.x * (0.6f + 0.4f * WF[i]);
                    float hgt = side * g * Mathf.Sqrt(WF[i]);
                    if (hgt < 2) continue;
                    float ext = i == 0 ? 5 : 0;
                    Put(buf, q.group, 34 + i * 0.1f, S((i == 0 ? "crowns_" : "crown_") + q.seed), q.stops[i], q.pos - new Vector2(0, f.y * hgt / 2),
                        hgt + ext, (side + ext) / (hgt + ext));
                }
            };
            Add(p);
        }

        static readonly float[] BurstF = { 1, 1, 0.8f, 0.6f, 0.4f };

        // chớp nước toé nhìn thẳng
        void BurstFlash(Vector2 c, float size, int group = Front, float life = 0.14f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = 2 + rng.Next(2), sz = size, stops = W };
            p.draw = (q, k, buf) =>
            {
                for (int i = 0; i < 5; i++)
                    Put(buf, q.group, 33 + i * 0.1f, S((i == 0 ? "crowns_" : "crown_") + q.seed), q.stops[i], q.pos,
                        q.sz * (0.6f + 0.5f * EaseOut(k / 0.6f)) * BurstF[i] + (i == 0 ? 5 : 0), 1, q.ang);
            };
            Add(p);
        }

        // nước toé lúc trúng (2026-11-18 theo Kingdom Rush): đỉnh ngay khung đầu, tan bằng vỡ ra. Ở thân: chớp sao kem 2 khung + các khối
        // nước văng ra (đốm kem, dải đậm ở đáy) → giọt → chấm; dưới chân: mão nước đục lỗ rồi sụp thành giọt, vành giọt elip, vòng sóng;
        // giọt văng theo chùm lệch cỡ, bọt thành cụm
        // dir: hướng nước bay tới (khung vẽ sẵn trung_nuoc có hướng; null = lật ngẫu nhiên)
        void Splash(Vector2 c, float sc, float ground, float tH, int group = Front, Vector2? dir = null)
        {
            if (NS) // bộ nước shader (2026-11-24, HatNuocShader.cs)
            {
                NSplash(c, sc, ground, tH, group, dir);
                return;
            }
            var feet = new Vector2(c.x, ground);
            // khung vẽ sẵn (2026-11-19): nước trúng đích trung_nuoc ở thân + vương miện nước nuoc_toe dưới chân (Crown) thay chớp sao kem, khối
            // nước văng có viền mực, cụm bọt viền mực. Giữ một chùm giọt bắn ra sau (chiều sâu), vòng sóng trên đất, họa tiết thêm của tướng.
            // Cao khung ~ 1 × tH × sc (bông toé đỉnh ~0,9 khung, lõi đặc ~0,5 khung): toé lớn chiêu cuối (sc 1,25) không che mặt quá ~0,2 s
            if (FbNuoc("trung_nuoc"))
            {
                TrungNuoc(c, Mathf.Min(1.3f, sc) * tH, dir, group, 44, 1.25f, 0.92f);
                Crown(feet + new Vector2(0, 4), 0.78f * tH * sc, 0.55f);
                float a0 = (-90 + U(-60, 60)) * Mathf.Deg2Rad;
                for (int i = 0; i < 2; i++)
                {
                    float a = a0 + U(-0.2f, 0.2f);
                    Drop(c + U2(-6, 6), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(260, 420) * sc * (1 - 0.16f * i), 0, U(2.2f, 3.4f), 900, Back,
                        ground + U(-10, 10));
                }
                Ripple(feet, 0.12f * tH, 0.72f * tH * sc);
                WExtra(c, (int)(4 * sc + 1), 300 * sc, group);
                return;
            }
            KrHit(c, 0.6f * tH * sc, group, (int)(5 + 2.4f * sc), 1.1f);
            Crown(feet + new Vector2(0, 4), 0.78f * tH * sc, 0.55f);
            int nc = sc > 1 ? 4 : 3;
            for (int j = 0; j < nc; j++)
            {
                float a0 = (-90 + U(-75, 75)) * Mathf.Deg2Rad;
                int m = U(0, 1) < 0.5f ? 2 : 3;
                bool back = U(0, 1) < 0.4f;
                for (int i = 0; i < m; i++)
                {
                    float a = a0 + U(-0.2f, 0.2f);
                    Drop(c + U2(-6, 6), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(260, 440) * sc * (1 - 0.16f * i), 0, U(2.2f, 3.8f) * (i == 0 ? 1.2f : 0.8f), 900,
                        back ? Back : group, ground + U(-10, 18));
                }
            }
            BotCum(c + U2(-14, 14) * sc, new Vector2(U(-40, 40), U(-50, -20)), U(9, 12) * sc, group);
            if (sc > 0.9f) BotCum(c + U2(-18, 18) * sc, new Vector2(U(-50, 50), U(-40, -10)), U(7, 10) * sc, Back);
            Ripple(feet, 0.12f * tH, 0.72f * tH * sc);
            WExtra(c, (int)(4 * sc + 1), 300 * sc, group);
        }

        // cầu nước: bốn lớp tròn rung nhẹ, hai vòng xoắn quay bên trong, cụm bọt bám mép dưới. cFn, rFn: theo giây từ lúc gọi
        P Orb(Func<float, Vector2> cFn, float tGrow, float tEnd, float rEnd, Func<float, float> rFn = null, int group = Front)
        {
            var p = new P { pos = cFn(0), life = tEnd, group = group, seed = rng.Next(4), stops = W };
            p.upd = (q, dt, s) =>
            {
                var np = cFn(q.age);
                q.drift = np - q.pos;
                q.pos = np;
                q.vel = Vector2.zero;
            };
            p.draw = (q, k, buf) =>
            {
                float age = q.age;
                float r = rFn != null ? rFn(age) : rEnd * EaseOut(age / tGrow) * (1 - SmoothStep(0.93f, 1, k));
                if (r < 1.5f) return;
                float wob = 1 + 0.07f * Mathf.Sin(age * 15);
                float mv = q.drift.magnitude;
                float ang = mv > 0.3f ? -Mathf.Atan2(q.drift.y, q.drift.x) * Mathf.Rad2Deg : 0;
                float st = wob * (1 + Mathf.Min(0.25f, mv / 14));
                var w = q.stops;
                int g = q.group, sd = q.seed;
                Put(buf, g, 20, S("solid_" + sd), Ink, q.pos, 2 * r / wob + 5, st, ang);
                Put(buf, g, 21, S("blob_" + sd), w[1], q.pos, 2 * r / wob, st, ang);
                Put(buf, g, 22, S("blob_" + ((sd + 1) & 3)), w[2], q.pos + new Vector2(0, -r * 0.08f), 1.66f * r / wob, st, ang);
                Put(buf, g, 23, S("blob_" + ((sd + 2) & 3)), w[3], q.pos + new Vector2(-r * 0.12f, -r * 0.2f), 1.1f * r, 1, ang);
                for (int j = 0; j < 2; j++)
                {
                    float a = age * 7 + j * Mathf.PI;
                    Put(buf, g, 24, S("curl_" + j), j == 0 ? w[4] : w[3], q.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.7f) * r * 0.3f, r * 0.7f, 1,
                        -a * Mathf.Rad2Deg);
                }
                var fp = q.pos + new Vector2(r * 0.42f, r * 0.62f);
                Put(buf, g, 25, S("foams_1"), Ink, fp, r * 0.62f + 3);
                Put(buf, g, 25.5f, S("foam_1"), FoamC, fp, r * 0.62f);
            };
            return Add(p);
        }

        // tụ nước về điểm cFn(giây từ lúc gọi) (người dùng 2026-11-18: pha hút quanh cầu xấu): VỆT nước thuôn (đầu đậm đuôi nhạt, dài theo
        // tốc) hiện dần trên một vòng rồi bay xoắn ốc vào tâm, càng gần càng nhanh (ease-in); vẽ dưới cầu nên tới mép cầu là nhập vào, chết
        // đúng lúc chạm tâm và làm cầu phồng (pulse[0]). Mật độ tăng dần tới lúc nhả; hai vòng nước co về tâm ở 0,42 s và 0,2 s trước lúc nhả.
        void Gather(Func<float, Vector2> cFn, float t0, float t1, float reach = 85, float rate = 60, int group = Front, float[] pulse = null)
        {
            if (t1 - t0 < 0.05f) return;
            float start = T;
            float thick = Mathf.Clamp(reach / 22, 2.6f, 4.4f);
            Every(t0, t1, x => rate * (0.3f + 1.2f * x * x), x =>
            {
                var q = new P
                {
                    life = U(0.3f, 0.42f), seed = rng.Next(4), group = group, ph = U(0, 6.28f), R0 = U(0.72f, 1) * reach, sz = thick * U(0.75f, 1.15f),
                    spin = U(0, 1) < 0.5f ? -1 : 1, big = U(0, 1) < 0.3f, stops = W
                };
                q.pos = cFn(T - start) + new Vector2(Mathf.Cos(q.ph), Mathf.Sin(q.ph) * 0.8f) * q.R0;
                q.upd = (z, dt, s) =>
                {
                    float k = Mathf.Min(1, z.age / z.life);
                    float a = z.ph + z.spin * 2.4f * k * k;
                    float rr = z.R0 * (1 - k * k * (0.6f + 0.4f * k));
                    var np = cFn(s.T + dt - start) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * rr;
                    z.vel = (np - z.pos) / Mathf.Max(dt, 1e-5f);
                };
                q.draw = (z, k, buf) =>
                {
                    float sp = z.vel.magnitude;
                    if (sp < 1) return;
                    if (NS) // bộ nước shader: vệt thon xoắn vào đầu nòng
                    {
                        NGatherVe(z, k, sp);
                        return;
                    }
                    float g = Mathf.Min(1, k / 0.25f); // hiện dần, không bật phụt
                    float th = z.sz * (0.55f + 0.45f * g), len = th * Mathf.Clamp(sp / 110, 1.8f, 5);
                    var w = z.stops;
                    PutVet(buf, z.group, 14, z.pos, z.vel / sp, len, th, z.big ? FoamC : w[3], z.big ? w[3] : w[2], g, z.seed);
                };
                if (pulse != null) q.onDeath = (z, s) => pulse[0] = Mathf.Min(0.3f, pulse[0] + 0.07f);
                Add(q);
            });
            var w3 = W[3];
            for (int i = 0; i < 2; i++)
            {
                float tr = t1 - 0.42f + i * 0.22f;
                if (tr < t0) continue;
                At(tr, () => RingCo(cFn(T - start), reach * 1.05f, reach * 0.12f, 0.3f, w3, group));
            }
        }

        // ================= hình hạt kiểu Kingdom Rush (2026-11-18) =================
        // Bộ hình mới hat_kr_<tên>_<i> (bản vân) và hat_kr_<tên>s_<i> (bản đặc), i = 0..3, đang được vẽ. Chỗ nào dùng cũng có hình cũ dự
        // phòng: ảnh mới chưa nhập thì S trả null và vẽ bằng hình cũ, không lỗi.
        static readonly Dictionary<string, string[]> KNames = new Dictionary<string, string[]>();

        static string KN(string b, int i)
        {
            if (!KNames.TryGetValue(b, out var a))
            {
                a = new string[4];
                for (int j = 0; j < 4; j++) a[j] = b + j;
                KNames[b] = a;
            }
            return a[i & 3];
        }

        Sprite SK(string b, int i) => S(KN(b, i));

        static float Hash(int a)
        {
            uint h = (uint)a * 2654435761u;
            h ^= h >> 13;
            h *= 0x5bd1e995;
            h ^= h >> 15;
            return (h & 0xffff) / 65535f;
        }

        static float Sq(float v) => v * v;

        // chạy fn với bảng màu nước th (sự kiện hẹn giờ chạy lúc có thể đã đổi tướng ra chiêu: hai tướng nước đánh nhau không lẫn màu)
        void InW(WTheme th, Action fn)
        {
            var o = wth;
            wth = th;
            fn();
            wth = o;
        }

        void AtW(float t, Action fn)
        {
            var th = wth;
            At(t, () => InW(th, fn));
        }

        void EveryW(float t0, float t1, Func<float, float> rate, Action<float> fn)
        {
            var th = wth;
            Every(t0, t1, rate, x =>
            {
                var o = wth;
                wth = th;
                fn(x);
                wth = o;
            });
        }

        void EveryW(float t0, float t1, float rate, Action<float> fn) => EveryW(t0, t1, _ => rate, fn);

        // nhịp đập của dòng nước đang dội vào đối thủ (tia nước: mỗi 0,24 s; số 0..1 là độ mạnh). StageView CHƯA gắn (đề xuất trong
        // Temp/vfx_thuy/BAO_CAO.md): gắn vào chớp _Flash + giật lùi nhẹ của con bị trúng thì đối thủ "chớp + giật" suốt dòng tia
        public Action<float> NuocPulse;

        // vệt nước thuôn: hat_kr_vet (đầu tròn ở +x, đuôi nhọn về -x); dự phòng ảnh giọt hat_drop_1 (ngọn chĩa lên) quay cho đầu tròn ra
        // trước. Ba lớp: mực, thân màu body, đầu màu head nhỏ lệch về trước (đầu đậm đuôi nhạt). ink = false: không viền (vệt sáng trên tia)
        void PutVet(List<Item> buf, int g, float layer, Vector2 pos, Vector2 dir, float len, float th, Color body, Color head, float alpha, int seed,
            bool ink = true)
        {
            var s = SK("kr_vet_", seed);
            if (s != null)
            {
                float ang = VelAng(dir);
                if (ink) Put(buf, g, layer, SK("kr_vets_", seed) ?? s, Ink, pos, th + 3, (len + 3) / (th + 3), ang, alpha);
                Put(buf, g, layer + 0.1f, s, body, pos, th, len / th, ang, alpha);
                if (ink) Put(buf, g, layer + 0.2f, s, head, pos + dir * len * 0.22f, th * 0.62f, len * 0.5f / (th * 0.62f), ang, alpha);
                return;
            }
            float a2 = TipAngle(-dir);
            if (ink) Put(buf, g, layer, S("drops_1"), Ink, pos, len + 3, (th + 3) / (len + 3), a2, alpha);
            Put(buf, g, layer + 0.1f, S("drop_1"), body, pos, len, th / len, a2, alpha);
            if (ink) Put(buf, g, layer + 0.2f, S("drop_1"), head, pos + dir * len * 0.2f, len * 0.5f, th * 0.62f / (len * 0.5f), a2, alpha);
        }

        // vòng nước co về tâm (không viền mực: vòng mảnh có viền thì thành vòng đen): hiện dần, co nhanh dần
        void RingCo(Vector2 c, float R0, float R1, float life, Color col, int group = Front)
        {
            var p = new P { pos = c, life = life, group = group, col = col, R0 = R0, R1 = R1 };
            p.draw = (q, k, buf) =>
            {
                float R = q.R0 + (q.R1 - q.R0) * k * k;
                float a = Mathf.Min(1, k / 0.25f) * (1 - SmoothStep(0.8f, 1, k));
                Put(buf, q.group, 13, S("ring"), q.col, q.pos, 2 * R * 0.82f, 1 / 0.82f, 0, 0.9f * a);
            };
            Add(p);
        }

        // cầu nước đang tụ / đang bay (người dùng 2026-11-18: cầu là khối nước sóng sánh có đốm sáng, không phải hình tròn trơn): khối
        // hat_kr_khoinuoc đổi hình mỗi 2 khung, lõi cuộn hat_kr_cau quay, đốm kem hat_kr_dom khớp đúng khung khối; lớp đậm lệch xuống thành
        // dải đậm ở đáy. Lớn dần theo nhịp đập, mỗi vệt nhập vào thì phồng (pulse[0], tự xẹp); nén lại 2 khung ngay trước tSqz (lúc nhả).
        // tail > 0: khi bay rải đốt đuôi theo quãng (bán kính đốt = tail × bán kính cầu) nên đuôi liền. cFn, rFn: theo giây từ lúc gọi.
        // Chưa có ảnh mới: khối tròn bốn lớp + hai vòng xoắn như bản cũ.
        P CauNuoc(Func<float, Vector2> cFn, float tEnd, Func<float, float> rFn, float[] pulse = null, float tSqz = -1, int group = Front, float tail = 0)
        {
            if (NS) return NCauShader(cFn, tEnd, rFn, pulse, tSqz, group); // bộ nước shader: đuôi liền thân theo đường bay
            // khung vẽ sẵn (2026-11-19): cầu nước cau_nuoc (khối nước 4 tông lam, dải bọt xoay quanh, lặp 24 khung) thay khối kr_khoinuoc + lõi
            // cuộn + đốm kem có viền mực. Giữ cỡ theo rFn (lớn dần theo nhịp, phồng khi vệt nhập, nén 2 khung trước lúc nhả), giãn theo hướng
            // bay; thân cầu chiếm ~0,78 cao khung nên cao khung = 2,56 r. Đuôi liền vẫn rải đốt, bỏ viền mực cho hợp khung (không viền)
            Sprite[] fbA = FbNuoc("cau_nuoc") ? FbArt("cau_nuoc") : null;
            var fbD = fbA != null ? Fbs["cau_nuoc"] : null;
            var fbT = FbNuocTint();
            var p = new P { pos = cFn(0), life = tEnd, group = group, seed = rng.Next(4), stops = W, ph = U(0, 24) };
            p.upd = (q, dt, s) =>
            {
                var np = cFn(q.age);
                q.drift = np - q.pos;
                q.pos = np;
                q.vel = Vector2.zero;
                if (pulse != null) pulse[0] *= Mathf.Exp(-7 * dt);
                if (tail <= 0) return;
                float mv = q.drift.magnitude;
                if (mv < 0.5f || mv > 200) return;
                float r = rFn(q.age) * tail, step = Mathf.Max(4, r * 0.55f);
                var d = q.drift / mv;
                q.tb += mv;
                int guard = 0;
                while (q.tb >= step && guard++ < 8)
                {
                    q.tb -= step;
                    s.DuoiNuoc(q.pos - d * q.tb, r * s.U(0.85f, 1.05f), 0.2f, q.stops, q.group, 14, fbA == null);
                }
            };
            p.draw = (q, k, buf) =>
            {
                float age = q.age;
                float r = rFn(age);
                if (r < 1.5f) return;
                r *= 1 + 0.06f * Mathf.Sin(age * 15) + (pulse != null ? pulse[0] : 0);
                float sx = 1;
                if (tSqz > 0 && age > tSqz - 0.07f && age < tSqz) // nén lại 2 khung trước lúc nhả
                {
                    r *= 0.8f;
                    sx = 1.14f;
                }
                float mv = q.drift.magnitude;
                float ang = mv > 0.3f ? VelAng(q.drift) : 0;
                float st = sx * (1 + Mathf.Min(0.3f, mv / 12));
                if (fbA != null) // khung vẽ sẵn: cầu cau_nuoc lặp, chồng mờ khung kế (mượt), lệch pha ngẫu nhiên mỗi cầu
                {
                    VeCauNuocFb(buf, fbA, fbD, q.ph + age * fbD.fps, q.pos, 2.56f * r, st, q.group, 20, ang, fbT, Mathf.Min(1, age / 0.05f));
                    return;
                }
                int fr = q.seed + (int)(age / 0.066f); // đổi hình mỗi 2 khung: nước sóng sánh
                var w = q.stops;
                int g = q.group;
                var kn = SK("kr_khoinuoc_", fr);
                if (kn != null)
                {
                    var up = new Vector2(0, -r * 0.1f);
                    Put(buf, g, 20, SK("kr_khoinuocs_", fr) ?? S("solid_" + (fr & 3)), Ink, q.pos, 2 * r + 5, st, ang);
                    Put(buf, g, 21, kn, w[1], q.pos, 2 * r, st, ang);
                    var core = SK("kr_cau_", fr);
                    Put(buf, g, 22, core ?? kn, w[2], q.pos + up * 0.8f, 1.7f * r, st, core != null ? age * 160 : ang);
                    Put(buf, g, 23, core != null ? SK("kr_cau_", fr + 1) : kn, w[3], q.pos + up * 1.8f + new Vector2(-r * 0.1f, 0), 1.06f * r, 1,
                        core != null ? -age * 220 : ang);
                    var dom = SK("kr_dom_", fr);
                    if (dom != null) Put(buf, g, 24, dom, FoamC, q.pos, 2 * r, st, ang);
                    else Put(buf, g, 24, S("foam_" + (fr & 3)), FoamC, q.pos + new Vector2(-r * 0.32f, -r * 0.36f), 0.42f * r);
                    return;
                }
                int sd = q.seed;
                Put(buf, g, 20, S("solid_" + sd), Ink, q.pos, 2 * r + 5, st, ang);
                Put(buf, g, 21, S("blob_" + sd), w[1], q.pos, 2 * r, st, ang);
                Put(buf, g, 22, S("blob_" + ((sd + 1) & 3)), w[2], q.pos + new Vector2(0, -r * 0.08f), 1.66f * r, st, ang);
                Put(buf, g, 23, S("blob_" + ((sd + 2) & 3)), w[3], q.pos + new Vector2(-r * 0.12f, -r * 0.2f), 1.1f * r, 1, ang);
                for (int j = 0; j < 2; j++)
                {
                    float a = age * 7 + j * Mathf.PI;
                    Put(buf, g, 24, S("curl_" + j), j == 0 ? w[4] : w[3], q.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.7f) * r * 0.3f, r * 0.7f, 1,
                        -a * Mathf.Rad2Deg);
                }
                Put(buf, g, 24.5f, S("foam_" + (fr & 3)), FoamC, q.pos + new Vector2(-r * 0.32f, -r * 0.36f), 0.36f * r);
            };
            return Add(p);
        }

        // nước trúng nhỏ kiểu Kingdom Rush (0,33 s): chớp sao kem 2 khung (hat_kr_chop; dự phòng nước toé nhìn thẳng hat_crown_2, 3) →
        // n khối nước văng đều quanh tâm (lệch ngẫu nhiên) → giọt → chấm. bias: vận tốc cộng thêm (toé lệch một phía)
        void KrHit(Vector2 c, float size, int group = Front, int n = 7, float speed = 1, Vector2? bias = null)
        {
            if (NS) // bộ nước shader: toé nhỏ (hướng tới = ngược bias)
            {
                NTrung(c, size * 1.7f, bias.HasValue ? -bias.Value : (Vector2?)null, group);
                return;
            }
            var star = new P { pos = c, life = 0.1f, group = group, seed = rng.Next(4), sz = size, ang = U(0, 360), stops = W };
            star.draw = (q, k, buf) =>
            {
                float s = q.sz * (0.88f + 0.25f * k);
                var w = q.stops;
                var ch = SK("kr_chop_", q.seed);
                if (ch != null)
                {
                    Put(buf, q.group, 44, SK("kr_chops_", q.seed) ?? ch, Ink, q.pos, s + 5, 1, q.ang);
                    Put(buf, q.group, 44.1f, ch, w[3], q.pos, s, 1, q.ang);
                    Put(buf, q.group, 44.2f, ch, FoamC, q.pos, 0.62f * s, 1, q.ang + 18);
                    return;
                }
                int cs = 2 + (q.seed & 1);
                Put(buf, q.group, 44, S("crowns_" + cs), Ink, q.pos, 0.8f * s + 5, 1, q.ang);
                Put(buf, q.group, 44.1f, S("crown_" + cs), w[3], q.pos, 0.8f * s, 1, q.ang);
                Put(buf, q.group, 44.2f, S("crown_" + cs), FoamC, q.pos, 0.5f * s, 1, q.ang + 18);
            };
            Add(star);
            var b = bias ?? Vector2.zero;
            float k0 = Mathf.Clamp(size / 60, 0.6f, 1.5f);
            for (int i = 0; i < n; i++)
            {
                float a = 6.2832f * (i + U(-0.3f, 0.3f)) / n;
                var dir = new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.85f);
                Khoi(c + dir * size * 0.12f, (dir * U(190, 320) * k0 + b) * speed, U(0.28f, 0.36f), size * U(0.08f, 0.13f), group);
            }
        }

        // khối nước văng (Kingdom Rush): bay ra, cản mạnh, rơi nhẹ; 42% đời đầu là khối có đốm kem và dải đậm ở đáy, rồi thành giọt thuôn
        // theo hướng bay, 20% cuối là chấm nhỏ dần rồi mất (tan bằng vỡ nhỏ, không mờ phụt)
        P Khoi(Vector2 pos, Vector2 vel, float life, float r, int group = Front)
        {
            if (NS) return NKhoi(pos, vel, life, r, group); // bộ nước shader: cục nước có khối
            var p = new P { pos = pos, vel = vel, life = life, drag = 5.5f, acc = new Vector2(0, 420), seed = rng.Next(4), sz = r, group = group, stops = W };
            p.draw = (q, k, buf) =>
            {
                var w = q.stops;
                int g = q.group, sd = q.seed;
                float sp = q.vel.magnitude;
                var d = sp > 5 ? q.vel / sp : new Vector2(0, 1);
                if (k < 0.42f)
                {
                    float r = q.sz * (k < 0.08f ? 0.7f + 0.3f * k / 0.08f : 1), ang = VelAng(d), st = 1 + Mathf.Min(0.35f, sp / 900);
                    var kn = SK("kr_khoinuoc_", sd);
                    if (kn != null)
                    {
                        Put(buf, g, 40, SK("kr_khoinuocs_", sd) ?? kn, Ink, q.pos, 2 * r + 3.5f, st, ang);
                        Put(buf, g, 40.2f, kn, w[1], q.pos, 2 * r, st, ang);
                        Put(buf, g, 40.4f, kn, w[2], q.pos + new Vector2(0, -r * 0.14f), 1.72f * r, st, ang);
                        var dom = SK("kr_dom_", sd);
                        if (dom != null) Put(buf, g, 40.6f, dom, FoamC, q.pos, 2 * r, st, ang);
                        else Put(buf, g, 40.6f, S("foam_" + sd), FoamC, q.pos + new Vector2(-r * 0.25f, -r * 0.3f), 0.5f * r);
                        return;
                    }
                    Put(buf, g, 40, S("solid_" + sd), Ink, q.pos, 2 * r + 3.5f, st, ang);
                    Put(buf, g, 40.2f, S("blob_" + sd), w[1], q.pos, 2 * r, st, ang);
                    Put(buf, g, 40.4f, S("blob_" + ((sd + 1) & 3)), w[2], q.pos + new Vector2(0, -r * 0.16f), 1.7f * r, st, ang);
                    Put(buf, g, 40.6f, S("blob_" + ((sd + 2) & 3)), FoamC, q.pos + new Vector2(-r * 0.25f, -r * 0.32f), 0.6f * r);
                    return;
                }
                if (k < 0.8f)
                {
                    PutGiot(buf, g, 40, q.pos, d, q.sz * 2.2f * (1 - 0.45f * (k - 0.42f) / 0.38f), w, sd, sp);
                    return;
                }
                float rd = q.sz * 0.55f * (1 - (k - 0.8f) / 0.2f);
                if (rd < 0.6f) return;
                Put(buf, g, 40, S("solid_" + sd), Ink, q.pos, 2 * rd + 2.5f);
                Put(buf, g, 40.2f, S("solid_" + sd), w[2], q.pos, 2 * rd);
            };
            return Add(p);
        }

        // cụm bọt / hơi nước (người dùng 2026-11-18: bọt, hơi nước thành cụm mềm, không rải rác): ba múi lệch cỡ chồng nhau, chung một
        // viền mực (mực của mọi múi vẽ dưới mọi màu), bay cùng nhau, nở tới đỉnh ở 25% đời rồi co mượt. hoi: hơi nước (hat_kr_khoi,
        // hat_kr_khoinho; dự phòng bọt), không viền, trong mờ 0,62, bay lên
        P BotCum(Vector2 pos, Vector2? vel = null, float r = 9, int group = Front, float life = 0, bool hoi = false)
        {
            if (NS) return NBotCum(pos, vel, r, group, life, hoi); // bộ nước shader: cụm bọt trắng
            var p = new P
            {
                pos = pos, vel = vel ?? new Vector2(U(-20, 20), U(-40, -10)), life = life > 0 ? life : U(0.5f, 0.75f), drag = 2.5f,
                acc = new Vector2(0, hoi ? -40 : 0), seed = rng.Next(4), sz = r, group = group, ang = U(0, 360), big = hoi, stops = W,
                off = new Vector2(U(0.5f, 0.72f), U(0.38f, 0.58f)), ph = U(0, 6.28f)
            };
            p.draw = (q, k, buf) =>
            {
                float r0 = k < 0.25f ? 0.55f + 0.45f * EaseOut(k / 0.25f) : 1 - 0.82f * SmoothStep(0.25f, 1, k);
                float rr0 = q.sz * r0, a = 1 - SmoothStep(0.72f, 1, k);
                if (rr0 < 1 || a < 0.03f) return;
                int g = q.group, sd = q.seed;
                for (int i = 0; i < 3; i++)
                {
                    float rr = i == 0 ? rr0 : rr0 * (i == 1 ? q.off.x : q.off.y);
                    float an = q.ph + i * 2.3f;
                    var pp = q.pos + (i == 0 ? Vector2.zero : new Vector2(Mathf.Cos(an), Mathf.Sin(an) * 0.8f) * rr0 * 0.8f);
                    float ga = q.ang + i * 40;
                    if (q.big)
                    {
                        var hs = SK(i == 0 ? "kr_khoi_" : "kr_khoinho_", sd + i) ?? S("foam_" + ((sd + i) & 3));
                        Put(buf, g, 31, hs, i == 0 ? FoamC : q.stops[4], pp, 2 * rr, 1, ga, 0.62f * a);
                        continue;
                    }
                    Put(buf, g, 30, S("foams_" + ((sd + i) & 3)), Ink, pp, 2 * rr + 3.5f, 1, ga, a);
                    Put(buf, g, 31, S("foam_" + ((sd + i) & 3)), FoamC, pp, 2 * rr, 1, ga, a);
                }
            };
            return Add(p);
        }

        // một đốt đuôi nước đứng yên tại chỗ sinh rồi co dần (đuôi đạn chia theo quãng bay nên liền); các đốt chung lớp nên hoà thành một
        // dải có một viền mực
        // ink = false: không viền mực (đuôi của cầu nước khung vẽ sẵn, khung không viền; khung vẽ sẵn 2026-11-19)
        void DuoiNuoc(Vector2 pos, float r, float life, Color[] w, int group = Front, float layer = 14, bool ink = true)
        {
            var p = new P { pos = pos, life = life, group = group, seed = rng.Next(4), sz = r, stops = w, ph = layer, big = ink };
            p.draw = (q, k, buf) =>
            {
                float rr = q.sz * Mathf.Pow(1 - k, 0.7f);
                if (rr < 0.8f) return;
                int sd = q.seed;
                float L = q.ph;
                if (q.big) Put(buf, q.group, L, S("solid_" + sd), Ink, q.pos, 2 * rr + 4.5f);
                Put(buf, q.group, L + 0.1f, S("blob_" + sd), q.stops[1], q.pos, 2 * rr);
                Put(buf, q.group, L + 0.2f, S("blob_" + ((sd + 1) & 3)), q.stops[2], q.pos, 1.5f * rr);
                if (k < 0.5f) Put(buf, q.group, L + 0.3f, S("blob_" + ((sd + 2) & 3)), q.stops[3], q.pos, 0.85f * rr * (1 - 1.2f * k));
            };
            Add(p);
        }

        // rải đốt đuôi theo quãng đạn đi trong bước này (gọi trong upd của đạn, trước khi đạn dời): đạn nhanh vẫn có đuôi liền
        void RaiDuoi(P z, float dt, float step, float r, float life, int group = Front)
        {
            float sp = z.vel.magnitude, mv = sp * dt;
            if (mv < 1e-3f) return;
            var d = z.vel / sp;
            z.tb += mv;
            int guard = 0;
            while (z.tb >= step && guard++ < 6)
            {
                z.tb -= step;
                DuoiNuoc(z.pos + d * (mv - z.tb), r * U(0.85f, 1.1f), life, z.stops, group);
            }
        }

        // lá nước ôm theo thân ở chỗ tia chạm: cung quanh tâm thân O bán kính R, từ hướng về người bắn (back) quay ±th0 rad; dày A ở giữa,
        // mỏng dần thành sừng nhọn ôm ra sau thân. Trả chỉ số đầu, số điểm = 2n
        int LaOm(Vector2 O, Vector2 back, float R, float A, float th0, float age, int n = 12)
        {
            int s = mp.Count;
            for (int i = 0; i < n; i++)
            {
                float t = -1 + 2f * i / (n - 1), th = t * th0, ca = Mathf.Cos(th), sa = Mathf.Sin(th);
                var d = new Vector2(back.x * ca - back.y * sa, back.x * sa + back.y * ca);
                float prof = Mathf.Pow(Mathf.Max(0, Mathf.Cos(t * 1.5708f)), 0.7f) * (1 + 0.18f * Mathf.Sin(age * 26 + i * 1.7f));
                mp.Add(O + d * (R + A * prof));
            }
            for (int i = n - 1; i >= 0; i--)
            {
                float t = -1 + 2f * i / (n - 1), th = t * th0 * 1.05f, ca = Mathf.Cos(th), sa = Mathf.Sin(th);
                mp.Add(O + new Vector2(back.x * ca - back.y * sa, back.x * sa + back.y * ca) * R);
            }
            return s;
        }

        static readonly Color BubbleHi = C(214, 240, 252);

        P Bubble(Vector2 pos, Vector2 vel, float life, float r, int group = Front)
        {
            var p = new P { pos = pos, vel = vel, life = life, group = group, seed = rng.Next(4), sz = r, ph = U(0, 6.28f), stops = W };
            p.draw = (q, k, buf) =>
            {
                float rr = q.sz * Mathf.Min(1, q.age / 0.12f) * (1 + 0.05f * Mathf.Sin(q.age * 11 + q.ph));
                float st = 1 + 0.06f * Mathf.Sin(q.age * 9 + q.ph);
                int g = q.group, sd = q.seed;
                Put(buf, g, 26, S("solid_" + sd), Ink, q.pos, 2 * rr + 4, st);
                Put(buf, g, 27, S("blob_" + sd), q.stops[2], q.pos, 2 * rr, st);
                Put(buf, g, 28, S("blob_" + ((sd + 1) & 3)), q.stops[3], q.pos + new Vector2(-rr * 0.06f, -rr * 0.08f), 1.68f * rr, st);
                Put(buf, g, 29, S("blob_" + ((sd + 2) & 3)), BubbleHi, q.pos + new Vector2(-rr * 0.14f, -rr * 0.18f), 1.1f * rr);
                Put(buf, g, 29.5f, S("foam_2"), FoamC, q.pos + new Vector2(rr * 0.4f, rr * 0.5f), rr * 0.5f);
            };
            p.onDeath = (q, s) =>
            {
                s.BurstFlash(q.pos, q.sz * 4.2f, q.group, 0.1f);
                for (int i = 0; i < 5; i++)
                {
                    float a = s.U(0, 6.28f);
                    s.Drop(q.pos, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f) * s.U(120, 240), 0.4f, q.sz * 0.3f, 900, q.group);
                }
                s.Foam(q.pos, null, 0, 4, q.sz * 0.8f, q.group);
                q.onPop?.Invoke(q, s);
            };
            return Add(p);
        }

        // vệt ướt trên cát (người dùng 2026-11-18: vệt ướt giữ khoảng 1 s rồi mờ): loang ra trong 0,14 s, giữ nguyên tới 62% đời rồi mờ dần
        // (không co); hai mảng phẳng trong mờ, không viền mực, vài chấm ướt quanh
        void Puddle(Vector2 pos, float R = 22, float life = 1.3f)
        {
            if (NS)
            {
                NVung(pos, R, Mathf.Max(life, 1.2f));
                return;
            }
            life = Mathf.Max(life, 1.5f);
            var p = new P { pos = pos, life = life, group = Floor, sz = R, stops = W, seed = rng.Next(1 << 16) };
            p.draw = (q, k, buf) =>
            {
                float g = EaseOut(q.age / 0.14f), hold = 1 - SmoothStep(0.62f, 1, k), R2 = q.sz * g * (1 + 0.06f * k);
                if (R2 < 0.5f || hold < 0.02f) return;
                Put(buf, Floor, 2, S("ell"), q.stops[1], q.pos, R2, 3.3f, 0, 0.3f * hold);
                Put(buf, Floor, 2.1f, S("ell"), q.stops[2], q.pos + new Vector2(-R2 * 0.3f, -1), R2 * 0.55f, 3.6f, 0, 0.36f * hold);
                for (int i = 0; i < 4; i++) // chấm ướt rải quanh
                {
                    float hx = Hash(q.seed + i * 7) * 2 - 1, hy = Hash(q.seed + i * 13 + 3) - 0.5f;
                    float rs = q.sz * (0.12f + 0.12f * Hash(q.seed + i * 29)) * g;
                    Put(buf, Floor, 2.2f, S("ell"), q.stops[1], q.pos + new Vector2(hx * q.sz * 2.3f, hy * q.sz * 0.9f), rs, 2.2f, 0, 0.32f * hold);
                }
            };
            Add(p);
        }

        // mưa giọt rơi lại quanh c sau khi nước bắn lên
        void RainBack(Vector2 c, float tH, int n = 16, float spread = 0.8f, float t0 = 0.3f, float t1 = 0.75f) =>
            Every(t0, t1, n / (t1 - t0), x => Drop(c + new Vector2(U(-spread, spread) * tH, -U(0.9f, 1.35f) * tH), new Vector2(U(-20, 20), 120), 0,
                U(3, 5), 900, U(0, 1) < 0.5f ? Front : Back, c.y + U(-10, 20)));

        // cột lưỡi sóng dựng lên sau lưng đối thủ (sau cú trúng lớn)
        void BackColumn(Vector2 foeFeet, float tH, float dur = 0.28f, float rate = 80)
        {
            // khung vẽ sẵn (2026-11-19): một vương miện nước lớn nuoc_toe dựng sau lưng đối thủ (lớp sau tướng) thay ~22 lưỡi sóng cuộn có viền
            // mực bắn lên; cao ~1,1 tH như cột lưỡi sóng cũ
            if (FbNuoc("nuoc_toe"))
            {
                ToeNuoc(foeFeet + new Vector2(U(-0.06f, 0.06f) * tH, -3), 1.2f * tH, 1.35f, Back, 20);
                return;
            }
            Every(0, dur, rate, x => Wave(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -4), new Vector2(U(-50, 50), -U(380, 620) * (1 - 0.4f * x)),
                U(0.4f, 0.55f), 8, U(16, 24), Back, 1, 0.5f, 1.6f, 900, 0.72f, 0.5f));
        }

        static readonly Color FlashW = new Color(0.9f, 0.97f, 1f, 0.3f);

        // ================= CHIÊU NƯỚC =================
        // lead: giây từ lúc gọi (đầu clip) tới khung nhả của clip. Mỗi hàm trả giây từ lúc gọi tới lúc trúng đối thủ.

        // bề ngang (nửa) của lõi tia ở quãng x (tính từ gốc): mép gợn chảy tới; gốc ở miệng hẹp; đuôi đã đứt thì tròn; chưa chạm thì mũi tròn
        // mập; đã chạm thân thì loe ra ở 36 đơn vị cuối. kl: nhân các quãng dọc (gốc hẹp, đuôi tròn, đoạn loe, mũi tròn) cho tia to (2026-11-19:
        // tia chiêu cuối Thôn Kình dày 2–2,6 lần thì mũi, đuôi, đoạn loe cũng dài theo, không thành đầu bằng)
        static float TiaHW(float x, float a, float tail, float head, float dist, bool hit, float hw0, float kl = 1)
        {
            float f = 1 + 0.16f * Mathf.Sin(x * 0.085f / kl - a * 34) + 0.08f * Mathf.Sin(x * 0.19f / kl - a * 57);
            if (tail <= 0) f *= 0.6f + 0.4f * SmoothStep(0, 26 * kl, x);
            else f *= Mathf.Sqrt(Mathf.Clamp01((x - tail) / (12 * kl)));
            if (hit) f *= 1 + 0.75f * SmoothStep(dist - 36 * kl, dist, x);
            else f *= Mathf.Sqrt(Mathf.Clamp01((head - x) / (10 * kl) + 0.12f)) * (1 + 0.35f * Mathf.Exp(-Sq((head - x - 10 * kl) / (12 * kl))));
            return hw0 * f;
        }

        // lớp của lõi tia: mực, lam đậm (mép), lam, lam nhạt (lõi rộng), sọc kem lệch về một bên (vệt sáng trên lưng dòng nước)
        static readonly float[] TiaW = { 1, 1, 0.8f, 0.62f, 0.34f };
        static readonly float[] TiaO = { 0, 0, -0.06f, -0.12f, -0.24f };

        // tia nước (người dùng 2026-11-18: "cuối tia nhìn cụt lủn, không có sự va chạm giữa tia đó với địch"):
        // - tụ ở miệng trong lúc lấy đà: vệt nước xoắn ốc nhập vào cầu nước sóng sánh, cầu nén 2 khung rồi toé lúc nhả;
        // - dòng nước liền (mảng): mép lam đậm, lõi lam nhạt rộng, sọc kem gợn chạy theo dòng, mép gợn chảy tới, vệt sáng lướt trên dòng;
        //   đầu dòng tới TẬN mặt trước thân đối thủ (cách tâm thân 0,24 tH), không dừng giữa chừng;
        // - chỗ chạm: dòng loe ra, lá nước trăng khuyết ôm theo thân (trong mờ 0,86 để không che mặt), bông nước toé chĩa ngược về phía
        //   người bắn đổi hình mỗi 2 khung (hat_kr_tiadau; dự phòng vương miện nước nằm nghiêng), khối nước tạt ngang theo thân, chùm giọt
        //   bắn ngược, cụm bọt; mỗi 0,24 s một nhịp đập (vòng sóng, mão nhỏ dưới chân, rung nhẹ, NuocPulse cho chớp + giật đối thủ);
        // - hết tia: đuôi đứt từ gốc (miệng nhỏ giọt), đoạn còn lại bay nốt tới đích, rơi giọt dọc đường, tới nơi thì vỡ toé thành giọt.
        // Trả giây tới lúc đầu dòng chạm đối thủ (hợp đồng thời gian với StageView: HoldNuoc("n_tia") = dur + 0,05 không đổi).
        // hwTo > 0: nửa bề dày lõi tia (tia TO của tướng há mồm rất to, WTheme.tiaTo; 0 = 9,5 thường, 11 chiêu cuối). Tia to thì cầu tụ, toé lúc
        // nhả, gợn, vệt sáng, giọt mép, khối văng to theo bề dày (kt); bông trúng, mão, vòng sóng, toé cuối to thêm 30 % mỗi lần dày gấp đôi
        // (kh). Giờ trúng, nhịp đập, NuocPulse không đổi
        // dayKhung > 0: bề dày tia vẽ sẵn (2026-11-19: mọi tia nước của tướng Thủy bảng lam / ngọc lam, xem PlayNuoc): có đủ khung DaTiaNuoc
        // thì phát NTiaKhung (HatFbThuy.cs), cùng giờ chạm, nhịp đập, giờ trả về; chưa có khung (hoặc bảng mực tím) thì tia mảng liền bên dưới
        public float NTia(Vector2 mouth, Vector2 target, Vector2 foeFeet, float casterGround, float tH, float lead, float dur = 0.88f, float hwTo = 0,
            float dayKhung = 0)
        {
            if (dayKhung > 0 && HasTia(DaTiaNuoc) && FbNuoc("tia_nuoc_doan"))
                return NTiaKhung(mouth, target, foeFeet, casterGround, tH, lead, dur, dayKhung);
            var dd = target - mouth;
            float d0 = dd.magnitude;
            var u = dd / Mathf.Max(1, d0);
            var nrm = new Vector2(-u.y, u.x);
            var back = -u;
            var src = mouth + u * 14;
            float rf = Mathf.Clamp(d0 - 70, 0, 0.24f * tH);
            var hitP = target - u * rf; // mặt trước thân đối thủ
            float dist = Mathf.Max(20, Vector2.Dot(hitP - src, u));
            float T0 = Mathf.Max(0.14f, lead), T1 = T0 + dur;
            const float SP = 1250, SPT = 1450; // tốc đầu dòng, tốc đoạn đuôi đứt bay nốt
            float travel = Mathf.Max(0.03f, dist / SP), tHit = T0 + travel, tCut = T1 + dist / SPT;
            bool big = dur > 1;
            float hwN = big ? 11 : 9.5f, hw0 = hwTo > 0 ? hwTo : hwN;
            // tia to (2026-11-19, Thôn Kình chiêu cuối): kt = bề dày so với tia thường; kc = cầu tụ / toé ở miệng; kh = bông trúng, toé chân
            float kt = hw0 / hwN, kc = Mathf.Max(1, 0.8f * kt), kh = 1 + 0.3f * (kt - 1), sk = Mathf.Sqrt(kt);
            float rc = 16 * kc;
            float start = T;
            var pulse = new float[1];
            Gather(t => src, 0, T0 - 0.03f, 62 * sk, 70, Front, pulse);
            CauNuoc(t => src, T1 + 0.08f, a => a < T0 ? rc * EaseOut(a / T0) : rc * (1 - 0.45f * (a - T0) / dur) * (1 - SmoothStep(T1 - 0.05f, T1 + 0.08f, a)),
                pulse, T0);
            // khung vẽ sẵn (2026-11-19): có khung nước thì bông toé chỗ chạm, toé lúc nhả là trung_nuoc; bớt khối văng / giọt, bỏ cụm bọt viền mực
            bool fb = FbNuoc("trung_nuoc");
            AtW(T0, () =>
            {
                Shake?.Invoke(0.2f);
                if (fb) // khung vẽ sẵn: cầu toé lúc nhả = bông nước nhỏ chĩa theo dòng
                {
                    TrungNuoc(src + u * 10 * kc, 54 * kc, u, Front, 44, 1.7f);
                    return;
                }
                KrHit(src + u * 8, 30 * kc, Front, 5, 0.8f, u * 120); // cầu toé lúc nhả
                BotCum(src + U2(-6, 6), u * 30 + new Vector2(0, -20), 7);
            });
            var core = new P { pos = src, life = tCut - T0 + 0.02f, group = Front, stops = W };
            core.draw = (q, k, buf) =>
            {
                float a = q.age;
                float head = Mathf.Min(dist, SP * a), tail = a > dur ? Mathf.Min(head, SPT * (a - dur)) : 0;
                if (head - tail < 4) return;
                bool hit = head >= dist - 0.5f;
                int n = Mathf.Clamp(Mathf.CeilToInt((head - tail) / 9) + 1, 3, 48);
                for (int li = 0; li < 5; li++)
                {
                    float wf = TiaW[li], off = TiaO[li], grow = li == 0 ? 2.4f : 0;
                    int a0 = mp.Count;
                    for (int pass = 0; pass < 2; pass++)
                        for (int i = 0; i < n; i++)
                        {
                            float x = tail + (head - tail) * i / (n - 1);
                            float hw = TiaHW(x, a, tail, head, dist, hit, hw0, kt);
                            if (li == 4) hw *= 0.7f + 0.3f * Mathf.Sin(x * 0.11f / kt - a * 46); // sọc kem gợn chạy theo dòng
                            var c = src + u * x + nrm * (2.4f * sk * Mathf.Sin(x * 0.045f - a * 20) * Mathf.Min(1, x / 40) + off * hw);
                            mp.Add(c + nrm * ((pass == 0 ? 1 : -1) * (hw * wf + grow)));
                        }
                    MRibbon(Front, 9 + li * 0.1f, a0, a0 + n, n, li == 0 ? Ink : li == 4 ? FoamC : q.stops[li]);
                }
            };
            AtW(T0, () => Add(core));
            // vệt sáng lướt trên dòng (không viền): cho thấy nước đang chảy tới
            EveryW(T0 + 0.02f, T1, 30, x =>
            {
                var q = new P { pos = src + nrm * (U(-0.4f, 0.4f) * hw0), vel = u * SP * U(1, 1.1f), life = Mathf.Max(0.02f, (dist - 18) / SP), group = Front,
                    seed = rng.Next(4), sz = U(2.2f, 3.2f) * sk, stops = W };
                q.draw = (z, k, buf) => PutVet(buf, Front, 15, z.pos, u, z.sz * 7, z.sz, z.stops[4], z.stops[4], Mathf.Min(1, k / 0.15f), z.seed, false);
                Add(q);
            });
            // giọt rơi khỏi dòng: chùm hai giọt lệch cỡ
            EveryW(T0 + 0.05f, T1, 9, x =>
            {
                float sd = U(0, 1) < 0.5f ? -1 : 1, xx = dist * U(0.15f, 0.85f);
                float gy = casterGround + (foeFeet.y - casterGround) * (xx / dist) + U(0, 24);
                for (int i = 0; i < 2; i++)
                    Drop(src + u * (xx + i * 6) + nrm * sd * 9 * kt, u * U(80, 200) + nrm * sd * U(50, 150) + new Vector2(0, -50), 0, U(2, 3.4f) * (i == 0 ? 1.1f : 0.75f),
                        900, Front, gy);
            });
            // chỗ chạm: lá nước ôm thân + bông toé chĩa về phía người bắn (một hạt sống từ lúc chạm tới khi đoạn đuôi tới nơi)
            var O = hitP + u * Mathf.Max(14, rf);
            float R = Mathf.Max(14, rf);
            var hd = new P { pos = hitP, life = tCut - tHit + 0.04f, group = Front, seed = rng.Next(4), stops = W, sz = (big ? 0.56f : 0.5f) * tH * kh };
            hd.draw = (q, k, buf) =>
            {
                float age = q.age;
                int step = (int)(age / 0.066f), fr = q.seed + step; // đổi hình mỗi 2 khung
                float j = Hash(q.seed * 31 + step), endK = SmoothStep(q.life - 0.1f, q.life, age);
                float s = q.sz * (1 + 0.3f * (1 - Mathf.Min(1, age / 0.1f))) * (0.9f + 0.18f * j) * (1 - 0.5f * endK); // to nhất ngay khung đầu
                var w = q.stops;
                float A = 0.1f * tH * (1 - 0.5f * endK) * (big ? 1.15f : 1) * sk;
                MSolid(Front, 30, LaOm(O, back, R, A, 1.2f, age), 24, w[2], 0.86f, 2.2f);
                MFill(Front, 30.2f, LaOm(O, back, R + 0.1f * A, 0.6f * A, 1.0f, age + 0.3f), 24, w[3], 0.86f, false);
                MFill(Front, 30.3f, LaOm(O, back, R + 0.2f * A, 0.28f * A, 0.72f, age + 0.6f), 24, FoamC, 0.86f, false);
                if (fb) return; // khung vẽ sẵn: bông toé là các lượt trung_nuoc theo nhịp đập (dưới), lá nước ôm thân giữ
                var td = SK("kr_tiadau_", fr);
                if (td != null)
                {
                    float ang = VelAng(back) + (j - 0.5f) * 18;
                    var c0 = q.pos + back * s * 0.22f;
                    Put(buf, Front, 46, SK("kr_tiadaus_", fr) ?? td, Ink, c0, s + 5, 1, ang);
                    Put(buf, Front, 46.1f, td, w[2], c0, s, 1, ang);
                    Put(buf, Front, 46.2f, td, w[3], c0 + u * s * 0.06f, 0.8f * s, 1, ang);
                    Put(buf, Front, 46.3f, td, FoamC, c0 + u * s * 0.12f, 0.55f * s, 1, ang);
                    return;
                }
                int cs = fr & 1; // dự phòng: vương miện nước cũ nằm nghiêng, chân ở chỗ chạm, các ngọn chĩa về phía người bắn
                var f = CrownF[cs];
                float a2 = TipAngle(back) + (j - 0.5f) * 18;
                for (int i = 0; i < 5; i++)
                {
                    float side = s * 0.8f / f.x * (0.6f + 0.4f * WF[i]), hg = side * Mathf.Sqrt(WF[i]), ext = i == 0 ? 5 : 0;
                    Put(buf, Front, 46 + i * 0.1f, S((i == 0 ? "crowns_" : "crown_") + cs), w[i], q.pos + back * (f.y * hg / 2), hg + ext, (side + ext) / (hg + ext), a2);
                }
            };
            AtW(tHit, () => Add(hd));
            // khối nước tạt ngang theo thân, chùm giọt bắn ngược về phía người bắn, cụm bọt (khung vẽ sẵn: bông toé đã có giọt, bọt nên bớt
            // khối văng 18 → 7/s, chùm giọt 11 → 6/s, bỏ cụm bọt viền mực)
            EveryW(tHit, tCut, fb ? 7 : 18, x =>
            {
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                Khoi(hitP + nrm * sd * U(4, 14) * kt, nrm * sd * U(170, 290) + back * U(30, 120) + new Vector2(0, -U(20, 90)), U(0.3f, 0.38f), U(4.5f, 7) * sk);
            });
            EveryW(tHit, tCut, fb ? 6 : 11, x =>
            {
                float a = Mathf.Atan2(back.y, back.x) + U(-1.1f, 1.1f);
                int m = U(0, 1) < 0.4f ? 3 : 2;
                bool bk = U(0, 1) < 0.35f;
                for (int i = 0; i < m; i++)
                {
                    float ai = a + U(-0.15f, 0.15f);
                    Drop(hitP + U2(-6, 6), new Vector2(Mathf.Cos(ai), Mathf.Sin(ai) - 0.45f) * U(200, 400) * (1 - 0.18f * i), 0, U(2, 3.6f) * (i == 0 ? 1.15f : 0.8f), 900,
                        bk ? Back : Front, foeFeet.y + U(-10, 18));
                }
            });
            if (!fb) EveryW(tHit, tCut, 5, x => BotCum(hitP + back * 8 + U2(-12, 12), back * U(20, 60) + U2(-30, 30), U(6, 9)));
            int nb = Mathf.Max(1, Mathf.CeilToInt((tCut - tHit) / 0.24f));
            for (int i = 0; i < nb; i++)
            {
                int ii = i;
                AtW(tHit + i * 0.24f, () =>
                {
                    // khung vẽ sẵn (2026-11-19): mỗi nhịp đập một bông nước trung_nuoc ở mặt trước thân (tia tới từ phía người bắn, nghiêng theo
                    // tia), lượt đầu to nhất (thay bông kr_tiadau đổi hình mỗi 2 khung). Mỗi lượt ~0,6 s nên chồng 2–3 lượt: dòng nước dội liên tục
                    if (fb)
                        TrungNuoc(hitP + back * (0.04f * tH) + nrm * U(-4, 4) * kt, (big ? 0.82f : 0.75f) * tH * kh * (ii == 0 ? 1.15f : U(0.9f, 1)), u, Front, 46,
                            ii == 0 ? 1.35f : 1.5f, 0.92f);
                    Ripple(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.62f * tH * kh);
                    if ((ii & 1) == 0) Crown(foeFeet + new Vector2(U(-12, 12), 6), 0.5f * tH * kh, 0.5f);
                    Shake?.Invoke((ii == 0 ? 0.3f : 0.08f) * kh);
                    NuocPulse?.Invoke(ii == 0 ? 1 : 0.45f);
                });
            }
            // hết tia: nước đứt từ gốc, miệng nhỏ giọt; đoạn còn lại bay nốt, rơi giọt dọc đường
            AtW(T1, () =>
            {
                for (int i = 0; i < 4; i++)
                    Drop(src + U2(-5, 5), new Vector2(U(-50, 50), U(-60, 10)) + u * U(20, 80), 0, U(2.2f, 3.4f), 900, Front, casterGround + U(-6, 10));
                if (!fb) BotCum(src + u * 6, u * 40, 7); // khung vẽ sẵn: bỏ cụm bọt viền mực ở miệng, cầu khung đang co lại đã đủ
            });
            EveryW(T1 + 0.02f, tCut, 36, x =>
            {
                float tl = Mathf.Min(dist, SPT * (T - start - T1));
                Drop(src + u * tl + nrm * U(-6, 6), u * U(100, 220) + new Vector2(0, -U(10, 60)), 0, U(2, 3), 900, Front,
                    casterGround + (foeFeet.y - casterGround) * (tl / dist) + U(0, 24));
            });
            AtW(tCut, () => // đoạn cuối tới đích: vỡ toé thành giọt, vệt ướt
            {
                Splash(hitP, (big ? 0.9f : 0.8f) * kh, foeFeet.y, tH, Front, u); // khung vẽ sẵn: bông toé cuối theo hướng tia (tia to: to theo kh)
                Puddle(foeFeet + new Vector2(0, 3), 22 * kh, 1.5f);
            });
            return tHit;
        }

        // cầu nước (2026-11-18): vệt nước xoắn ốc nhập vào cầu sóng sánh lớn dần theo nhịp ở miệng trong lúc lấy đà, cầu nén 2 khung rồi
        // nhả: toé ở miệng, cầu bay vòng cung kéo đuôi liền (đốt đuôi chia theo quãng bay), nhỏ giọt; trúng thì vỡ toé lớn, cột nước sau
        // lưng, mưa giọt, vệt ướt giữ khoảng 1 s
        // co: nhân cỡ cầu (chỉ nhân cỡ); oc = true (2026-11-19, Thạch Giải: "không cần làm animation tụ nước vì nó ợ từ trong bụng ra, khi nào
        // nó ợ thì bắn cầu nước từ mồm ra"): bỏ pha tụ (vệt xoắn ốc, cầu lớn dần ở miệng), đúng khung ợ cầu hiện ở giữa mồm (nở 0,06 s) rồi bay
        // luôn; giờ trúng giữ T0 + 0,55
        public float NCau(Vector2 mouth, Vector2 target, float casterGround, Vector2 foeFeet, float tH, float lead, float co = 1, bool oc = false)
        {
            var src = mouth;
            float T0 = Mathf.Max(0.2f, lead);
            const float TT = 0.55f, ARC = 70;
            Vector2 Path(float t)
            {
                if (t < T0) return src + new Vector2(0, 2.5f * Mathf.Sin(t * 9));
                float x = Mathf.Min(1, (t - T0) / TT);
                return src + (target - src) * x + new Vector2(0, -4 * ARC * x * (1 - x));
            }
            float start = T;
            var pulse = new float[1];
            float tg = Mathf.Max(0.1f, T0 - 0.05f), rc = 30 * co;
            if (oc)
                CauNuoc(Path, T0 + TT, a => a < T0 ? 0 : rc * (0.6f + 0.4f * EaseOut((a - T0) / 0.06f)) * (1 - SmoothStep(T0 + TT - 0.04f, T0 + TT, a)), null, -1,
                    Front, 0.62f);
            else
            {
                Gather(Path, 0, T0 - 0.05f, 90, 80, Front, pulse);
                CauNuoc(Path, T0 + TT, a => rc * EaseOut(a / tg) * (1 - SmoothStep(T0 + TT - 0.04f, T0 + TT, a)), pulse, T0, Front, 0.62f);
            }
            // khung vẽ sẵn (2026-11-19): cầu là cau_nuoc (trong CauNuoc); toé ở miệng lúc nhả là bông trung_nuoc nhỏ chĩa theo hướng ném, bỏ cụm
            // bọt viền mực; trúng: Splash khung (trung_nuoc theo hướng cầu rơi tới + nuoc_toe) và cột nước sau lưng là nuoc_toe lớn (BackColumn)
            var uc = Unit(target - src);
            AtW(T0, () =>
            {
                Shake?.Invoke(0.15f);
                if (FbNuoc("trung_nuoc"))
                {
                    TrungNuoc(src + uc * 8 * co, 66 * Mathf.Sqrt(co), uc, Front, 44, 1.6f);
                    return;
                }
                KrHit(src, 40 * Mathf.Sqrt(co), Front, 5, 0.7f);
                BotCum(src + U2(-8, 8), null, 8);
            });
            EveryW(T0, T0 + TT, 12, x => Drop(Path(T - start) + U2(-10, 10), new Vector2(U(-40, 40), U(-20, 60)), 0, U(2.2f, 3.6f), 900, Front,
                casterGround + (foeFeet.y - casterGround) * x + U(-5, 30)));
            AtW(T0 + TT, () =>
            {
                Shake?.Invoke(0.6f);
                FlashScreen?.Invoke(FlashW);
                Splash(target, 1.25f, foeFeet.y, tH, Front, target - src + new Vector2(0, 4 * ARC)); // hướng cầu lúc rơi tới (cuối vòng cung)
                BackColumn(foeFeet, tH);
                RainBack(foeFeet, tH, 14);
                Puddle(foeFeet + new Vector2(0, 3), 26, 1.5f);
            });
            return T0 + TT;
        }

        // bong bóng: thổi chùm bong bóng tự lái tới đối thủ, lượn, vỡ lần lượt; bong bóng lớn cuối cùng vỡ toé
        public float NBong(Vector2 mouth, Vector2 target, Vector2 foeFeet, float tH, float lead)
        {
            var src = mouth;
            var dd = Unit(target - src);
            var nrm = new Vector2(-dd.y, dd.x);
            float dist = (target - src).magnitude;
            float s0 = Mathf.Max(0.05f, lead - 0.05f);
            void Blow(bool big)
            {
                float r = big ? 26 : U(8, 15);
                var q = Bubble(src + U2(-6, 6), dd * (big ? 250 : U(300, 420)) * 0.4f + nrm * U(-120, 120), 2.2f, r);
                q.aim = target + (big ? Vector2.zero : new Vector2(U(-0.25f, 0.25f), U(-0.25f, 0.25f)) * tH);
                q.vy = big ? 250 : U(300, 420);
                q.big = big;
                q.upd = (z, dt, s) =>
                {
                    var to = z.aim - z.pos;
                    float d = to.magnitude;
                    var want = to / Mathf.Max(d, 1e-5f) * z.vy + nrm * (Mathf.Sin(z.age * 6 + z.ph) * 90);
                    z.vel += (want - z.vel) * Mathf.Min(1, 4 * dt);
                    if (d < 16 + z.sz * 0.4f) z.dead = true;
                };
                q.onPop = (z, s) =>
                {
                    s.Shake?.Invoke(z.big ? 0.5f : 0.1f);
                    if (z.big) s.Splash(z.pos, 0.9f, foeFeet.y, tH);
                    else s.RingN(foeFeet + new Vector2(0, 2), 0.35f, 0.1f * tH, 0.4f * tH, z.stops[3]);
                };
            }
            Gather(t => src, 0, s0 - 0.04f, 50, 40);
            Every(s0, s0 + 0.8f, 12, x => Blow(false));
            Every(s0, s0 + 0.8f, 16, x => Foam(src + U2(-6, 6), dd * 60 + U2(-30, 30), 0, 3, 7));
            At(s0 + 0.85f, () => Blow(true));
            return s0 + Mathf.Clamp(dist / 330, 0.3f, 0.9f);
        }

        // điểm của một lưỡi trăng khuyết (mặt lồi theo d, trục dọc ax); trả chỉ số đầu, số điểm = 2 * n - 2
        int Crescent(Vector2 c, Vector2 d, Vector2 ax, float sc, float a, float a2, float b, int n = 13)
        {
            int s = mp.Count;
            for (int i = 0; i < n; i++)
            {
                float th = -Mathf.PI / 2 + Mathf.PI * i / (n - 1);
                mp.Add(c + (d * (a * Mathf.Cos(th)) + ax * (b * Mathf.Sin(th))) * sc);
            }
            for (int i = n - 2; i >= 1; i--)
            {
                float th = -Mathf.PI / 2 + Mathf.PI * i / (n - 1);
                mp.Add(c + (d * (a2 * Mathf.Cos(th)) + ax * (b * Mathf.Sin(th))) * sc);
            }
            return s;
        }

        // lưỡi nước: hai lưỡi trăng khuyết liền chém liên tiếp, mép trước có dải bọt trắng
        public float NLuoi(Vector2 mouth, Vector2 target, Vector2 foeFeet, float tH, float lead)
        {
            var dd = target - mouth;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            var src = mouth + u * 12;
            float T0 = Mathf.Max(0.12f, lead);
            const float SP = 900;
            const int N = 2 * 13 - 2;
            float travel = Mathf.Max(0.05f, (dist - 20) / SP);
            Gather(t => src, 0, T0 - 0.04f, 55, 50);
            Orb(t => src, T0, T0 + 0.25f, 13);
            void Blade(float tilt)
            {
                Shake?.Invoke(0.15f);
                var ax = nrm * Mathf.Cos(tilt) + u * Mathf.Sin(tilt);
                var d = u * Mathf.Cos(tilt) - nrm * Mathf.Sin(tilt);
                var q = new P { pos = src, vel = u * SP, life = travel, group = Front, stops = W };
                q.draw = (z, k, buf) =>
                {
                    float sc = 0.4f + 0.6f * EaseOut(z.age / 0.07f);
                    var c = z.pos - d * 8 * sc;
                    MSolid(Front, 26, Crescent(c, d, ax, sc, 34, 2, 58), N, z.stops[1]);
                    MFill(Front, 26.2f, Crescent(c, d, ax, sc, 30, 9, 51), N, z.stops[2]);
                    MFill(Front, 26.3f, Crescent(c, d, ax, sc, 22, 12, 42), N, z.stops[3]);
                    MFill(Front, 26.4f, Crescent(c, d, ax, sc, 30.5f, 23, 46), N, FoamC);
                };
                Add(q);
                float start = T;
                Vector2 Pos() => src + u * SP * (T - start);
                var w3 = W[3];
                Every(0.03f, travel, 34, x =>
                {
                    var g = new P { pos = Pos() - u * 16, vel = u * SP * 0.25f, life = 0.13f, group = Front, col = w3 };
                    g.draw = (z, k, buf) => MFill(Front, 25, Crescent(z.pos, d, ax, 1 - 0.25f * k, 26, 14, 50), N, z.col, 0.55f * (1 - k));
                    Add(g);
                });
                Every(0, travel, 44, x => Drop(Pos() + ax * U(-48, 48) - u * 14, -u * U(40, 140) + new Vector2(0, -40), 0.4f, U(2.6f, 4.2f)));
                Every(0, travel, 20, x => Foam(Pos() + ax * ((U(0, 1) < 0.5f ? -1 : 1) * U(34, 52)) - u * 10, Vector2.zero, 0.35f, 3, U(6, 9)));
                At(travel, () =>
                {
                    Shake?.Invoke(0.4f);
                    var cut = new P { pos = target, life = 0.16f, group = Front };
                    cut.draw = (z, k, buf) =>
                        MSolid(Front, 36, Crescent(z.pos - d * 6, d, ax, 1 + 0.35f * k, 14 * (1 - k), 4 * (1 - k), 64), N, FoamC, 1 - k * k, 2);
                    Add(cut);
                    Splash(target, 0.75f, foeFeet.y, tH);
                });
            }
            At(T0, () => Blade(0.35f));
            At(T0 + 0.22f, () => Blade(-0.35f));
            return T0 + travel;
        }

        static readonly float[] SpearF = { 1, 1, 0.8f, 0.58f, 0.34f };

        // thương nước: các mũi thương tụ thành vòng cung trên đầu tướng trong lúc lấy đà, tới khung nhả thì phóng lần lượt
        public float NThuong(Vector2 casterFeet, float casterH, Vector2 target, Vector2 foeFeet, float tH, float lead, int count = 6)
        {
            float dirx = target.x < casterFeet.x ? -1 : 1;
            var A = casterFeet + new Vector2(dirx * 10, -1.08f * casterH);
            float RA = 0.46f * casterH;
            const float LEN = 62;
            float T0 = Mathf.Max(0.25f, lead);
            float gap = Mathf.Min(0.08f, (T0 - 0.12f) / count);
            float dist = (target - A).magnitude;
            var thW = wth;
            Gather(t => A, 0, T0 - 0.06f, 0.55f * casterH, 55); // 2026-11-18: nước bị hút xoắn ốc về vòng cung trên đầu trong lúc giơ gậy
            for (int i0 = 0; i0 < count; i0++)
            {
                int i = i0;
                At(0.04f + i * gap, () =>
                {
                    float th = Mathf.PI + Mathf.PI * (i + 0.5f) / count;
                    var home = A + new Vector2(RA * Mathf.Cos(th), 0.5f * RA * Mathf.Sin(th));
                    var q = new P
                    {
                        pos = home, life = 4, home = home, aim = target + new Vector2(U(-0.18f, 0.18f), U(-0.15f, 0.2f)) * tH, span = i,
                        launch = T + (T0 - 0.04f - i * gap) + i * 0.1f, group = Front, stops = W
                    };
                    BotCum(home, null, 7);
                    for (int j = 0; j < 2; j++) Drop(home + U2(-10, 10), new Vector2(U(-60, 60), -U(20, 90)), 0.35f, 2.4f);
                    q.upd = (z, dt, s) =>
                    {
                        if (!z.fly)
                        {
                            z.pos = z.home + new Vector2(0, 3.5f * Mathf.Sin(z.age * 7 + z.span));
                            z.vel = (z.aim - z.pos) * 0.001f;
                            if (s.U(0, 1) < 0.08f) s.Drop(z.pos + s.U2(-6, 6), new Vector2(0, 40), 0.35f, 2.4f);
                            if (s.T >= z.launch)
                            {
                                z.fly = true;
                                z.vel = Unit(z.aim - z.pos) * 1500;
                                s.Shake?.Invoke(0.05f);
                            }
                            return;
                        }
                        var dv = Unit(z.vel);
                        if (s.U(0, 1) < 0.5f) s.Drop(z.pos - dv * 26, -dv * 80 + s.U2(-50, 50), 0.25f, 2.4f, 200);
                        if (Vector2.Dot(z.aim - z.pos, z.vel) <= 0)
                        {
                            z.dead = true;
                            s.Shake?.Invoke(0.14f);
                            s.InW(thW, () => // 2026-11-18: nước trúng nhỏ kiểu Kingdom Rush thay chớp toé + giọt rời
                            {
                                // khung vẽ sẵn (2026-11-19): mỗi mũi trúng một bông trung_nuoc nghiêng theo hướng mũi lao tới (6–8 mũi nên nhỏ hơn
                                // đòn thường: 0,58 tH, chạy nhanh 1,55)
                                if (s.FbNuoc("trung_nuoc")) s.TrungNuoc(z.aim, 0.58f * tH, dv, Front, 44, 1.55f);
                                else s.KrHit(z.aim, 0.34f * tH, Front, 5, 1, dv * -60);
                                s.WExtra(z.aim, 1, 240);
                            });
                        }
                    };
                    q.draw = (z, k, buf) =>
                    {
                        if (NS) // bộ nước shader: mũi thương là một dải nước nhọn (HatNuocShader.cs)
                        {
                            NMuiThuong(z, LEN);
                            return;
                        }
                        float age = z.age;
                        float sc = age < 0.1f ? 1.25f * EaseOut(age / 0.1f) : 1.25f - 0.25f * Mathf.Min(1, (age - 0.1f) / 0.06f);
                        var d = z.fly ? Unit(z.vel) : Unit(z.aim - z.pos);
                        float ang = TipAngle(d);
                        for (int li = 0; li < 5; li++)
                        {
                            float f = SpearF[li];
                            float L = LEN * sc * f * (z.fly && li < 2 ? 1.25f : 1) + (li == 0 ? 5 : 0);
                            Put(buf, Front, 20 + li, S(li == 0 ? "drops_1" : "drop_1"), z.stops[li], z.pos - d * (LEN * sc * (1 - f) * 0.2f), L, 0.62f, ang);
                        }
                    };
                    Add(q);
                });
            }
            float end = T0 + count * 0.1f + dist / 1500 + 0.05f;
            AtW(end, () => // khung vẽ sẵn (2026-11-19): mão là nuoc_toe (Crown); AtW cho đúng bảng nước
            {
                Crown(foeFeet + new Vector2(0, 6), 0.7f * tH);
                Ripple(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.7f * tH);
                RainBack(foeFeet, tH, 8, 0.5f, 0, 0.3f);
            });
            return T0 + dist / 1500;
        }

        // đạn nước bay từ chỗ nhả tới đối thủ trong chừng này giây (đòn đánh thường của tướng đứng yên bắn)
        public const float DanTravel = 0.13f;

        // đạn nước của đòn đánh thường (pháp sư nước 2026-11-11: chĩa gậy bắn): một viên nước thon rời chỗ nhả DanTravel giây TRƯỚC
        // khung trúng của clip nên chạm đối thủ đúng khung trúng (số sát thương, khựng, rung của sân không phải dời). Không có pha tụ
        // ở chỗ nhả: lúc lấy đà đầu gậy còn ở sau vai. Nhỏ hơn chiêu mana: chớp toé 0,12 s, 6 giọt, 2 bọt.
        public float NDan(Vector2 mouth, Vector2 target, Vector2 foeFeet, float tH, float lead)
        {
            float T0 = Mathf.Max(DanTravel + 0.02f, lead);
            var th = wth;
            AtW(T0 - DanTravel, () =>
            {
                var aim = target + new Vector2(U(-0.1f, 0.1f), U(-0.08f, 0.1f)) * tH;
                var dd = aim - mouth;
                float dist = Mathf.Max(1, dd.magnitude);
                var u = dd / dist;
                // khung vẽ sẵn (2026-11-19): toé nhỏ ở đầu gậy là bông trung_nuoc nhỏ chĩa theo hướng bắn
                if (FbNuoc("trung_nuoc")) TrungNuoc(mouth + u * 6, 42, u, Front, 44, 1.8f);
                else KrHit(mouth + u * 4, 22, Front, 4, 0.6f, u * 60); // 2026-11-18: toé nhỏ ở đầu gậy lúc nhả
                for (int i = 0; i < 2; i++) Drop(mouth + U2(-5, 5), -u * U(40, 120) + new Vector2(U(-70, 70), -U(30, 110)), 0.32f, 2.4f);
                var q = new P { pos = mouth, life = DanTravel + 0.25f, aim = aim, group = Front, stops = W, vel = u * (dist / DanTravel), fly = true };
                q.upd = (z, dt, s) =>
                {
                    var dv = Unit(z.vel);
                    s.RaiDuoi(z, dt, 6, 4.2f, 0.14f); // đuôi liền chia theo quãng bay
                    if (s.U(0, 1) < 0.25f) s.Drop(z.pos - dv * 20, -dv * 70 + s.U2(-45, 45), 0.22f, 2.2f, 240);
                    if (Vector2.Dot(z.aim - z.pos, z.vel) <= 0)
                    {
                        z.dead = true;
                        s.Shake?.Invoke(0.12f);
                        s.InW(th, () =>
                        {
                            // khung vẽ sẵn (2026-11-19): đạn trúng = bông trung_nuoc 0,82 tH (đòn thường 0,7–1 × tH) theo hướng đạn bay, bỏ
                            // chớp sao + khối văng + cụm bọt viền mực
                            if (s.FbNuoc("trung_nuoc")) s.TrungNuoc(z.aim, 0.82f * tH, dv, Front, 44, 1.35f);
                            else
                            {
                                s.KrHit(z.aim, 0.44f * tH, Front, 6, 1, dv * -50);
                                s.BotCum(z.aim + s.U2(-8, 8), null, 8);
                            }
                            s.WExtra(z.aim, 1, 240);
                        });
                    }
                };
                q.draw = (z, k, buf) =>
                {
                    float sc = z.age < 0.05f ? 0.6f + 0.4f * z.age / 0.05f : 1;
                    var d = Unit(z.vel);
                    float ang = TipAngle(d);
                    for (int li = 0; li < 5; li++)
                    {
                        float f = SpearF[li];
                        float L = 50 * sc * f + (li == 0 ? 5 : 0);
                        Put(buf, Front, 20 + li, S(li == 0 ? "drops_1" : "drop_1"), z.stops[li], z.pos - d * (50 * sc * (1 - f) * 0.2f), L, 0.8f, ang);
                    }
                };
                Add(q);
            });
            return T0;
        }

        // viên ngọc trai của dòng sò đột biến (suất ha_ba, 2026-11-11): con sò ngậm miệng phồng lên rồi phụt viên ngọc ở khung nhả của
        // clip cast. Viên ngọc rời miệng đúng khung nhả, bay NgocTravel giây, kéo theo giọt dãi; chạm đối thủ thì toé nước. Ngọc vẽ bằng
        // lớp chồng như bong bóng: viền mực, thân xà cừ, vệt tím nhạt ở mép dưới (tô phẳng, không điểm sáng).
        static readonly Color NgocA = C(241, 228, 236), NgocB = C(201, 182, 218);
        // quả bóng mực của dòng bạch tuộc (suất so_ngoc, 2026-11-12, mã "n_muc"): cùng đường bay với viên ngọc, to hơn, đen mực với vệt
        // tím than ở mép dưới; giọt, vũng và cú toé lấy màu mực từ WTheme của tướng
        static readonly Color MucA = C(40, 35, 52), MucB = C(124, 86, 196); // 2026-11-18: vệt tím than → tím tươi
        public const float NgocTravel = 0.2f;

        public float NNgoc(Vector2 mouth, Vector2 target, Vector2 foeFeet, float tH, float lead, bool muc = false)
        {
            float T0 = Mathf.Max(0.05f, lead);
            float tg = Mathf.Max(0.02f, T0 - 0.55f);
            float sz = (muc ? 0.13f : 0.085f) * tH;
            var th = wth;
            // 2026-11-18 (pha tụ): trong lúc phồng người, vệt nước (mực) xoắn ốc nhập vào cầu nước sóng sánh ở miệng, cầu nén 2 khung rồi
            // toé đúng lúc phụt viên ngọc / bóng mực
            if (T0 - tg > 0.15f)
            {
                var pulse = new float[1];
                float tl = T0 - tg;
                AtW(tg, () =>
                {
                    Gather(t => mouth, 0, tl - 0.03f, muc ? 72 : 60, 60, Front, pulse);
                    CauNuoc(t => mouth, tl + 0.02f, a => 1.05f * sz * EaseOut(a / tl), pulse, tl);
                });
            }
            AtW(T0, () =>
            {
                var aim = target + new Vector2(U(-0.06f, 0.06f), U(-0.06f, 0.08f)) * tH;
                var dd = aim - mouth;
                float dist = Mathf.Max(1, dd.magnitude);
                var u = dd / dist;
                Shake?.Invoke(0.2f);
                // khung vẽ sẵn (2026-11-19): toé ở miệng lúc phụt ngọc là bông trung_nuoc nhỏ theo hướng phụt (bóng mực của bạch tuộc: bảng tím,
                // FbNuoc trả false nên giữ hạt cũ)
                if (FbNuoc("trung_nuoc")) TrungNuoc(mouth + u * 8, 0.46f * tH, u, Front, 44, 1.6f);
                else KrHit(mouth + u * 6, 0.26f * tH, Front, 4, 0.7f, u * 150);
                for (int i = 0; i < 3; i++) Drop(mouth + U2(-6, 6), u * U(60, 260) + new Vector2(U(-120, 120), -U(40, 200)), 0.36f, U(2.2f, 3.2f));
                var q = new P
                {
                    pos = mouth, life = NgocTravel + 0.3f, aim = aim, group = Front, stops = W, vel = u * (dist / NgocTravel), fly = true,
                    seed = rng.Next(4), sz = sz,
                };
                q.upd = (z, dt, s) =>
                {
                    s.RaiDuoi(z, dt, Mathf.Max(5, z.sz * 0.7f), z.sz * 0.62f, 0.14f); // đuôi nước (mực) liền chia theo quãng bay
                    if (Vector2.Dot(z.aim - z.pos, z.vel) <= 0)
                    {
                        z.dead = true;
                        s.InW(th, () =>
                        {
                            s.Shake?.Invoke(0.45f);
                            s.Splash(z.aim, 0.85f, foeFeet.y, tH, Front, z.vel); // khung vẽ sẵn: bông toé theo hướng ngọc bay
                            s.Puddle(foeFeet + new Vector2(0, 3), 22, 1.5f);
                        });
                    }
                };
                q.draw = (z, k, buf) =>
                {
                    float rr = z.sz * (z.age < 0.04f ? 0.55f + 0.45f * z.age / 0.04f : 1);
                    float ang = VelAng(Unit(z.vel)); // dài theo hướng bay
                    Put(buf, Front, 26, S("solid_" + z.seed), Ink, z.pos, 2 * rr + 4, 1.18f, ang);
                    Put(buf, Front, 27, S("blob_" + z.seed), muc ? MucA : NgocA, z.pos, 2 * rr, 1.18f, ang);
                    Put(buf, Front, 28, S("blob_" + ((z.seed + 1) & 3)), muc ? MucB : NgocB, z.pos + new Vector2(-rr * 0.2f, rr * 0.28f), 0.9f * rr);
                };
                Add(q);
            });
            return T0 + NgocTravel;
        }

        // con sóng: lưng, đỉnh, mũi mào, bụng mào, mặt lõm, chân (trục: tới trước, lên cao; theo bề rộng và chiều cao sóng)
        static readonly Vector2[] Song =
        {
            new Vector2(-1.3f, 0), new Vector2(-0.95f, 0.24f), new Vector2(-0.55f, 0.62f), new Vector2(-0.1f, 0.94f), new Vector2(0.35f, 1),
            new Vector2(0.72f, 0.86f), new Vector2(0.9f, 0.6f), new Vector2(0.84f, 0.4f), new Vector2(0.68f, 0.52f), new Vector2(0.48f, 0.6f),
            new Vector2(0.3f, 0.42f), new Vector2(0.32f, 0.18f), new Vector2(0.5f, 0), new Vector2(-0.2f, -0.04f), new Vector2(-0.8f, -0.04f),
        };
        static readonly Vector2[] Song2 =
        {
            new Vector2(-1.02f, 0.05f), new Vector2(-0.8f, 0.24f), new Vector2(-0.45f, 0.55f), new Vector2(-0.05f, 0.8f), new Vector2(0.35f, 0.87f),
            new Vector2(0.64f, 0.77f), new Vector2(0.76f, 0.64f), new Vector2(0.5f, 0.72f), new Vector2(0.18f, 0.56f), new Vector2(0.12f, 0.22f),
            new Vector2(0.3f, 0.04f), new Vector2(-0.4f, 0),
        };
        static readonly Vector2[] Song3 =
        {
            new Vector2(-0.82f, 0.14f), new Vector2(-0.5f, 0.42f), new Vector2(-0.1f, 0.66f), new Vector2(0.22f, 0.74f), new Vector2(0.2f, 0.62f),
            new Vector2(-0.1f, 0.52f), new Vector2(-0.45f, 0.28f), new Vector2(-0.7f, 0.1f),
        };
        static readonly Vector2[] SongMao =
        {
            new Vector2(-0.1f, 0.96f), new Vector2(0.2f, 1.03f), new Vector2(0.5f, 0.99f), new Vector2(0.76f, 0.85f), new Vector2(0.9f, 0.63f),
            new Vector2(0.83f, 0.45f),
        };
        static readonly float[] SongChan = { -1.15f, -0.75f, -0.35f, 0.05f, 0.42f };

        // sóng thần: nước tụ dưới chân tướng lúc lấy đà, tới khung nhả một con sóng liền có mào cuộn lăn tới, đổ ập lên đối thủ
        public float NSong(Vector2 casterFeet, float casterH, Vector2 foeFeet, float tH, float lead, float to = 1)
        {
            float tS = tH * to; // to > 1: sóng thần (Thôn Kình, 2026-11-25): thân sóng, mào, toé đổ to theo
            float sx = foeFeet.x < casterFeet.x ? -1 : 1;
            var A = casterFeet + new Vector2(sx * 0.46f * casterH, -4);
            var B = foeFeet + new Vector2(0, 4);
            var u = Unit(B - A);
            var side = new Vector2(-u.y, u.x * 0.35f);
            const float TT = 0.62f, TC = 0.2f, TR = 0.14f;
            float T0 = Mathf.Max(TR + 0.04f, lead);
            float start = T;
            var stop = B - new Vector2(sx * 0.3f * tH, 0);
            Vector2 Front_(float t, out float x)
            {
                x = Mathf.Clamp01((t - T0) / TT);
                return A + (stop - A) * (x * x * (3 - 2 * x));
            }
            Vector2 Now(out float x) => Front_(T - start, out x);
            Gather(t => A + new Vector2(0, -8), 0, T0, 60, 50);
            At(0.05f, () => Ripple(casterFeet + new Vector2(0, -2), 0.22f * casterH, 0.66f * casterH));
            AtW(T0 - TR, () => // khung vẽ sẵn (2026-11-19): mão lúc sóng dâng là nuoc_toe (Crown); AtW cho đúng bảng nước
            {
                Shake?.Invoke(0.25f);
                Crown(A + new Vector2(0, 4), 0.6f * tH);
            });
            var body = new P { pos = A, life = TR + TT + TC, group = Front, stops = W };
            body.draw = (q, k, buf) =>
            {
                float t = T0 - TR + q.age;
                var c = Front_(t, out float pr);
                float fall = 1 - SmoothStep(T0 + TT, T0 + TT + TC, t);
                float hg = (0.55f + 0.6f * pr) * tS * EaseOut(q.age / 0.22f) * fall;
                float wd = (0.5f + 0.25f * pr) * tS * (1 + 0.6f * (1 - fall));
                if (hg < 4) return;
                if (NS) // bộ nước shader: thân sóng là dải theo mặt cắt + dải bọt mào (HatNuocShader.cs)
                {
                    NSongVe(c, hg, wd, sx, t, fall, 1.7f);
                    return;
                }
                int Shape(Vector2[] ctrl, float wob)
                {
                    ctl.Clear();
                    for (int i = 0; i < ctrl.Length; i++)
                    {
                        float f = ctrl[i].x, v = ctrl[i].y;
                        ctl.Add(new Vector2(c.x + sx * (f + wob * Mathf.Sin(t * 13 + i)) * wd,
                            c.y - (v + (v > 0.08f ? wob * Mathf.Sin(t * 11 + i * 1.7f) : 0)) * hg));
                    }
                    return MSmooth();
                }
                MSolid(Front, 22, Shape(Song, 0.03f), Song.Length * 4, q.stops[1], 1, 2.6f);
                MFill(Front, 22.2f, Shape(Song2, 0.02f), Song2.Length * 4, q.stops[2]);
                MFill(Front, 22.3f, Shape(Song3, 0.02f), Song3.Length * 4, q.stops[3]);
                for (int i = 0; i < SongMao.Length; i++) // bọt trắng phủ mào
                {
                    var pos = new Vector2(c.x + sx * SongMao[i].x * wd, c.y - SongMao[i].y * hg);
                    float r = (0.13f + 0.03f * Mathf.Sin(t * 9 + i * 2)) * hg * (i == 0 || i == 5 ? 0.75f : 1);
                    Put(buf, Front, 23, S("foams_" + (i & 3)), Ink, pos, 2 * r + 4);
                    Put(buf, Front, 23.1f, S("foam_" + (i & 3)), FoamC, pos, 2 * r);
                }
                for (int i = 0; i < SongChan.Length; i++) // bọt sủi dọc chân sóng
                {
                    var pos = new Vector2(c.x + sx * SongChan[i] * wd, c.y - 0.02f * hg);
                    float r = (0.07f + 0.02f * Mathf.Sin(t * 12 + i * 2.3f)) * hg;
                    Put(buf, Front, 23, S("foams_" + ((i + 1) & 3)), Ink, pos, 2 * r + 4);
                    Put(buf, Front, 23.1f, S("foam_" + ((i + 1) & 3)), FoamC, pos, 2 * r);
                }
            };
            At(T0 - TR, () => Add(body));
            if (NS && NuocGoi) GSongThem(() => Now(out _), sx, tS, T0, TT); // bản 3: vệt trượt, sóng trượt, khói bọt, toé mưa của gói
            Every(T0, T0 + TT, 46, x =>
            {
                var c = Now(out float pr);
                float sz = 9 + 8 * pr;
                Wave(c + new Vector2(sx * U(0.1f, 0.5f) * tH * 0.6f, -U(0, 14)), new Vector2(sx * U(160, 300), -U(120, 300)), U(0.26f, 0.36f), sz * 0.6f,
                    sz, Front, 1, 0.5f, 2, 900, 0.72f, 0.3f);
            });
            Every(T0, T0 + TT, 10, x => BotCum(Now(out _) - u * 0.75f * tH + side * U(-30, 30), new Vector2(0, -8), U(9, 13), Back)); // bọt thành cụm
            var w3 = W[3];
            Every(T0, T0 + TT, 7, x => RingN(Now(out _) - u * 0.8f * tH, 0.4f, 8, 44, w3));
            Every(T0, T0 + TT, 26, x =>
            {
                var c = Now(out _);
                Drop(c + new Vector2(sx * U(-0.2f, 0.5f) * tH, -U(0.5f, 1) * tH), new Vector2(U(-120, 120), -U(100, 260)), 0, U(3, 5), 900, Front,
                    c.y + U(-6, 20));
            });
            // khung vẽ sẵn (2026-11-19): con sóng mảng tới nơi thì giao cho khung song_nuoc (từ khung 10: mào cuộn lớn nhất → đổ ập → bọt tràn
            // → vũng mỏng) đổ chồm qua đối thủ theo hướng sóng (khung vẽ đổ sang PHẢI, đổ sang trái thì lật), thay 18 lưỡi sóng cuộn có viền
            // mực bắn qua đầu và 5 cụm bọt viền mực tràn hai bên. Mào cuộn ở ~0,8 bề ngang khung nên neo lùi về phía người ra chiêu 0,36 cao
            // khung cho mào đổ trúng đối thủ; trong mờ 0,86 (khối nước lớn phủ lên con bị trúng). Phát sớm 0,08 s cho chồng lên lúc mảng sụp
            bool fbS = !NS && FbNuoc("song_nuoc");
            if (NS) At(T0 + TT - 0.04f, () => NSongDo(foeFeet, tS, sx)); // bộ nước shader: sóng đổ tới đích
            if (fbS)
            {
                float hs = 1.2f * tH;
                var tint = FbNuocTint();
                At(T0 + TT - 0.04f, () => SongNuoc(foeFeet + new Vector2(-sx * 0.36f * hs, 4), hs, sx < 0, 10, 1.25f, tint));
            }
            AtW(T0 + TT + 0.04f, () =>
            {
                Shake?.Invoke(0.75f);
                FlashScreen?.Invoke(FlashW);
                if (!fbS && !NS)
                    for (int i = 0; i < 18; i++) // nước chồm qua đầu rồi đổ xuống
                    {
                        bool fr = U(0, 1) < 0.25f;
                        Wave(B + new Vector2(U(-50, 50), -10), new Vector2(U(-150, 150) + u.x * 120, -U(380, 640)), U(0.45f, 0.65f), 12,
                            U(20, 30) * (fr ? 0.6f : 1), fr ? Front : Back, 1, 0.4f, 1.5f, 1100, 0.72f, 0.6f);
                    }
                Splash(foeFeet + new Vector2(0, -0.4f * tH), 1.1f * to, foeFeet.y, tH, Front, u);
                if (!fbS)
                    for (int i = 0; i < 5; i++) // bọt tràn hai bên sát đất, thành cụm
                    {
                        float sd = U(0, 1) < 0.5f ? -1 : 1;
                        BotCum(B + new Vector2(sd * U(10, 40), U(-6, 6)), new Vector2(sd * U(120, 260), -U(0, 30)), U(11, 15), U(0, 1) < 0.5f ? Front : Back,
                            U(0.6f, 0.9f));
                    }
                RainBack(foeFeet, tH, 14);
                Puddle(foeFeet + new Vector2(0, 3), 26, 1.4f);
            });
            HaiLongBao(foeFeet, tH, T0 - TR, T0 + TT + 0.5f, T0 + TT + 0.04f, 2, 4); // 2026-11-19: Hải Long dạng 1 thêm lốc phụ + sét (HatFbThuy.cs)
            return T0 + TT;
        }

        static readonly Color CloudA = C(150, 186, 224), CloudB = C(204, 226, 244);

        // mưa rào: mây tụ trên đầu đối thủ trong lúc lấy đà, tới khung nhả thì trút mưa
        public float NMua(Vector2 foeFeet, float tH, float lead, float dur = 1.15f)
        {
            var top = foeFeet + new Vector2(0, -1.2f * tH);
            if (top.y < 44) top.y = 44; // không vượt mép trên sân
            float T0 = Mathf.Max(0.35f, lead), T1 = T0 + dur;
            Gather(t => top, 0, T0, 70, 45);
            if (NS && NuocGoi) GMuaDat(foeFeet, tH, T0, T1); // bản 3: vòng gợn + toé hạt mưa của gói
            for (int i = 0; i < 7; i++)
            {
                bool mid = i >= 2 && i <= 4;
                var p = new P
                {
                    pos = top, life = T1 + 0.5f, seed = i & 3, off = new Vector2((i - 3) * 27 + U(-6, 6), U(-9, 9) - (mid ? 8 : 0)),
                    sz = U(27, 36) * (mid ? 1.15f : 1), ph = U(0, 6.28f), group = Front
                };
                p.draw = (q, k, buf) =>
                {
                    float g = EaseOut(q.age / T0) * (1 - SmoothStep(T1, T1 + 0.5f, q.age));
                    float r = q.sz * g;
                    if (r < 1.5f) return;
                    var pos = top + q.off * g + new Vector2(0, 2.5f * Mathf.Sin(q.age * 4 + q.ph));
                    Put(buf, Front, 30, S("foams_" + q.seed), Ink, pos, 2 * r + 4);
                    Put(buf, Front, 31, S("foam_" + q.seed), CloudA, pos, 2 * r);
                    Put(buf, Front, 31.5f, S("foam_" + ((q.seed + 1) & 3)), CloudB, pos + new Vector2(-r * 0.15f, -r * 0.22f), 1.3f * r);
                };
                Add(p);
            }
            Every(T0, T1, x => 125 * Mathf.Min(1, x * 5), x =>
            {
                float x0 = U(-0.8f, 0.8f) * tH;
                bool onFoe = Mathf.Abs(x0) < 0.38f * tH && U(0, 1) < 0.6f;
                var q = Drop(top + new Vector2(x0, 12), new Vector2(-50, U(760, 940)), 0, U(6.5f, 9.5f), 300,
                    onFoe || U(0, 1) < 0.5f ? Front : Back, onFoe ? foeFeet.y - U(0.45f, 0.85f) * tH : foeFeet.y + U(-12, 22));
                q.seed = 1; // giọt dài thon
                if (onFoe)
                    q.onGround = (z, s) =>
                    {
                        s.Foam(z.pos, null, 0, 4, 7);
                        for (int j = 0; j < 2; j++) s.Drop(z.pos, new Vector2(s.U(-150, 150), -s.U(60, 170)), 0.3f, 2.6f);
                        z.dead = true;
                    };
            });
            // khung vẽ sẵn (2026-11-19): mão nhỏ là nuoc_toe chạy nhanh (Crown); EveryW cho đúng bảng nước của tướng gọi mưa
            EveryW(T0 + 0.15f, T1 + 0.1f, 3.5f, x => Crown(foeFeet + new Vector2(U(-0.6f, 0.6f) * tH, U(0, 14)), U(0.25f, 0.4f) * tH, 0.3f));
            var w3 = W[3];
            for (int i = 0; i < 4; i++)
                At(T0 + 0.15f + i * 0.3f, () => Ripple(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.7f * tH, 0.5f, w3));
            At(T0 + 0.12f, () =>
            {
                Shake?.Invoke(0.2f);
                Puddle(foeFeet + new Vector2(0, 3), 26, dur + 0.55f);
            });
            Every(T0 + 0.3f, T1, 3, x => WExtra(foeFeet + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.3f, 0.8f) * tH), 1, 200));
            return T0 + 0.2f;
        }

        // cột nước: chân loe, thân thon, đầu xoè ba ngọn
        static readonly Vector2[] Cot =
        {
            new Vector2(-1.7f, 0), new Vector2(-0.9f, 0.1f), new Vector2(-0.62f, 0.45f), new Vector2(-0.78f, 0.74f), new Vector2(-1.5f, 0.88f),
            new Vector2(-1.25f, 1.02f), new Vector2(-0.6f, 0.96f), new Vector2(0, 1.1f), new Vector2(0.6f, 0.96f), new Vector2(1.25f, 1.02f),
            new Vector2(1.5f, 0.88f), new Vector2(0.78f, 0.74f), new Vector2(0.62f, 0.45f), new Vector2(0.9f, 0.1f), new Vector2(1.7f, 0),
        };
        static readonly Vector2[] CotBot = { new Vector2(-1.2f, 0.98f), new Vector2(0, 1.1f), new Vector2(1.2f, 0.98f), new Vector2(-0.6f, 1.02f), new Vector2(0.6f, 1.02f) };

        // xoáy nước rồi mạch phun: xoáy sát đất siết vào tâm dưới chân đối thủ trong lúc lấy đà, tới khung nhả cột nước vọt lên
        public float NXoay(Vector2 foeFeet, float tH, float lead)
        {
            if (NS) return NXoayShader(foeFeet, tH, lead); // bộ nước shader: mạch phun (HatNuocShader.cs)
            var Cc = foeFeet + new Vector2(0, 4);
            float T1 = Mathf.Max(0.45f, lead + 0.08f);
            Every(0, T1 + 0.1f, 28, x =>
            {
                var p = new P { pos = Cc, life = 0.5f, ph = U(0, 360), seed = rng.Next(3), stops = W };
                p.draw = (q, k, buf) =>
                {
                    float R = (0.95f - 0.65f * k) * tH;
                    int idx = Mathf.RoundToInt((q.ph + 420 * k) / 30) % 12;
                    float alpha = Mathf.Min(1, Mathf.Min(k / 0.15f, (1 - k) / 0.25f));
                    if (q.seed == 0)
                    {
                        Put(buf, Floor, 31, S("arc_" + idx), FoamC, Cc, 2 * R * 0.3f * 0.9f, 1 / 0.3f, 0, alpha);
                        return;
                    }
                    Put(buf, Floor, 30, S("arcs_" + idx), Ink, Cc, 2 * R * 0.3f, 1 / 0.3f, 0, alpha);
                    Put(buf, Floor, 30.5f, S("arc_" + idx), q.stops[q.seed == 1 ? 2 : 3], Cc, 2 * R * 0.3f, 1 / 0.3f, 0, alpha);
                };
                Add(p);
            });
            Every(0.05f, T1, 36, x =>
            {
                var q = Wave(Cc, Vector2.zero, 0.55f, 6, U(9, 13), Front, 1, 0.08f, 0, 0, 0.75f);
                q.ph = U(0, 6.28f);
                q.upd = (z, dt, s) =>
                {
                    float k = z.age / z.life, a = z.ph + 7.5f * z.age, R = (0.9f - 0.62f * k) * tH;
                    var np = Cc + new Vector2(R * Mathf.Cos(a), 0.3f * R * Mathf.Sin(a) - 3);
                    z.vel = (np - z.pos) / Mathf.Max(dt, 1e-5f);
                    z.group = Mathf.Sin(a) < 0 ? Back : Front;
                };
            });
            Every(0.1f, T1, 6, x => BotCum(Cc + new Vector2(U(-0.25f, 0.25f) * tH, U(-6, 6)), Vector2.zero, U(6, 9), Back, 0.45f));
            At(0.1f, () => Shake?.Invoke(0.15f));
            AtW(T1, () => // khung vẽ sẵn (2026-11-19): AtW để chọn khung / hạt theo đúng bảng nước của tướng ra chiêu
            {
                Shake?.Invoke(0.65f);
                FlashScreen?.Invoke(FlashW);
                Crown(Cc + new Vector2(0, 4), 0.85f * tH, 0.5f); // khung vẽ sẵn: nuoc_toe lớn ở chân cột
                Ripple(Cc, 0.15f * tH, 0.85f * tH);
                // khung vẽ sẵn: cột nước húc từ dưới lên thân = bông trung_nuoc xoay cho tia tới từ DƯỚI (thay chớp sao + khối văng viền mực)
                bool fb = FbNuoc("trung_nuoc");
                if (fb) TrungNuoc(foeFeet + new Vector2(0, -0.45f * tH), 1.0f * tH, new Vector2(0, -1), Front, 44, 1.25f, 0.9f, 90);
                else KrHit(foeFeet + new Vector2(0, -0.45f * tH), 0.6f * tH, Front, 7);
                // khung vẽ sẵn (2026-11-19, người dùng chê lốc / cột nước mảng "màu hơi trầm và chưa hợp"): cột xoáy nước là lốc "loc_nuoc" hai
                // lớp bao quanh đối thủ (sau tướng đặc, trước tướng lật + trong mờ 0,5), vọt lên 1,3 tH trong 0,12 s như cột cũ, xoáy nhanh
                // (tốc 1,7), cuối co 25 % và tắt dần 0,26 s; bỏ cột mảng ba lớp có viền mực + bọt đầu cột. Chưa nhập khung: cột mảng cũ
                // 2026-11-19 ("lốc xoáy làm to lên cho che hết tướng địch"): cao 1,7 tH (chặn mép trên sân), giãn ngang 1,9, chân khung hạ 0,1 cao
                // khung như vòi rồng NVoi; phần chân đối thủ đã có mão nuoc_toe 0,85 tH ở trên
                // 2026-11-19 (khung lốc TRÙM "loc_nuoc_bao": cột xoáy dày, gốc gần rộng bằng miệng): có khung thì dùng nó, cao 1,65 tH (LocBaoCao),
                // giãn ngang chỉ 1,25, chân khung hạ 0,04 cao khung: trùm kín từ chân tới đầu. Chưa có thì lốc phễu loc_nuoc to (giãn 1,9) như trên
                bool loc;
                if (FbNuoc("loc_nuoc_bao"))
                {
                    float HB = LocBaoCao(Cc.y, tH);
                    Func<float, float> caoB = t => HB * EaseOut(t / 0.12f) * (1 - 0.25f * SmoothStep(0.4f, 0.66f, t));
                    loc = LocNuocBao(t => Cc + new Vector2(0, LocBaoHa * caoB(t)), caoB, 0.66f, 0.5f, 1.7f, LocBaoGian, 0.05f, 0.26f, 16, "loc_nuoc_bao");
                }
                else
                {
                    float HX = Mathf.Clamp((Cc.y - 24) / (0.85f * 1.04f), 1.3f * tH, 1.7f * tH);
                    Func<float, float> caoX = t => HX * EaseOut(t / 0.12f) * (1 - 0.25f * SmoothStep(0.4f, 0.66f, t));
                    loc = FbNuoc("loc_nuoc") && LocNuocBao(t => Cc + new Vector2(0, 0.1f * caoX(t)), caoX, 0.66f, 0.5f, 1.7f, 1.9f, 0.05f, 0.26f, 16);
                }
                var pil = new P { pos = Cc, life = 0.66f, group = Front, stops = W };
                pil.draw = (q, k, buf) =>
                {
                    float a = q.age;
                    float g = EaseOut(a / 0.12f) * (1 - SmoothStep(0.4f, 0.66f, a));
                    if (g < 0.05f) return;
                    float ht = 1.3f * tH * g, wd = 0.17f * tH * (0.75f + 0.25f * g);
                    ctl.Clear();
                    for (int i = 0; i < Cot.Length; i++)
                        ctl.Add(new Vector2(Cc.x + (Cot[i].x + 0.07f * Mathf.Sin(a * 22 + i * 1.3f)) * wd, Cc.y - Cot[i].y * ht));
                    MNested(Front, 16, MSmooth(), Cot.Length * 4, q.stops, new Vector2(Cc.x, Cc.y - 0.52f * ht), new Vector2(0.55f, 0.9f),
                        new Vector2(0.2f, 0.78f), new Vector2(-0.12f * wd, 0), 0.82f);
                    for (int i = 0; i < CotBot.Length; i++) // bọt trên đầu cột
                    {
                        var pos = new Vector2(Cc.x + CotBot[i].x * wd, Cc.y - CotBot[i].y * ht);
                        float r = (0.62f + 0.12f * Mathf.Sin(a * 18 + i * 2)) * wd * (i < 3 ? 1 : 0.75f);
                        Put(buf, Front, 17, S("foams_" + (i & 3)), Ink, pos, 2 * r + 4);
                        Put(buf, Front, 17.1f, S("foam_" + (i & 3)), FoamC, pos, 2 * r);
                    }
                };
                if (!loc) Add(pil); // có khung lốc thì không vẽ cột mảng
                // khung vẽ sẵn: vương miện nuoc_toe ở chân đã toé lên nên lưỡi sóng bắn quanh cột bớt 60 → 26/s
                float rate = fb ? 26 : 60;
                Every(0, 0.45f, x => rate * (1 - 0.5f * x), x =>
                {
                    bool fr = U(0, 1) < 0.25f;
                    Wave(Cc + new Vector2(U(-0.2f, 0.2f) * tH, -4), new Vector2(U(-50, 50), -U(520, 800) * (1 - 0.4f * x)), U(0.4f, 0.55f), 9,
                        U(18, 26) * (fr ? 0.6f : 1), fr ? Front : Back, 1, 0.6f, 1.4f, 900, 0.72f, 0.5f);
                });
                if (!loc) // khung lốc đã có bọt ở miệng phễu: bỏ cụm bọt viền mực trên đầu cột
                    Every(0.1f, 0.6f, 8, x => BotCum(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -U(1, 1.3f) * tH), new Vector2(U(-60, 60), -U(0, 40)), U(11, 16), Back));
                RainBack(foeFeet, tH, 18);
                Puddle(foeFeet + new Vector2(0, 3), 24);
                WExtra(foeFeet + new Vector2(0, -0.5f * tH), 5, 320);
            });
            HaiLongBao(foeFeet, tH, Mathf.Max(0.1f, T1 - 0.35f), T1 + 0.6f, T1, 2, 4); // 2026-11-19: Hải Long dạng 2 thêm lốc phụ + sét (HatFbThuy.cs)
            return T1;
        }

        // vòi rồng nước: phễu là 8 vòng nước dẹt xếp chồng, lắc ngang lệch pha theo độ cao; thân trong mờ ở trước đối thủ. Nước bị hút
        // vào chân trong lúc lấy đà, phễu dựng lên trước khung nhả một nhịp
        // tu: LỐC XOÁY NƯỚC (n_loc, rồng vây 2026-11-12: "quạt 1 phát mạnh tạo 1 lốc xoáy nước"): phễu dựng lên ở chỗ tu (trước mặt tướng,
        // đúng khung quạt cánh) rồi lướt tới chân đối thủ trong T_DI giây, quay tại đó tới khi sụp. Không có tu: vòi rồng mọc tại chỗ.
        public float NVoi(Vector2 foeFeet, float tH, float lead, Vector2? tu = null)
        {
            var Cd = foeFeet + new Vector2(0, 4);
            bool di = tu.HasValue;
            var Cs = di ? tu.Value + new Vector2(0, 4) : Cd;
            const float T_DI = 0.5f;
            float sc = tH / 150f;
            float HT = 1.27f * tH;
            if (Cd.y - HT < 24) HT = Mathf.Max(0.8f * tH, Cd.y - 24); // không vượt mép trên sân
            const float T_UP = 0.35f;
            const int N = 8, RN = 20;
            float TA = Mathf.Max(0.12f, lead - 0.1f), T1 = TA + 1.65f, T_END = T1 + 0.4f;
            Vector2 CcT(float t) => di ? Vector2.Lerp(Cs, Cd, SmoothStep(TA + 0.1f, TA + 0.1f + T_DI, t)) : Cd;
            float Grow(float t)
            {
                t -= TA;
                return t <= 0 ? 0 : EaseOut(t / T_UP) * (1 - SmoothStep(T1 - TA, T_END - TA, t));
            }
            float Radius(float hh) => (16 + 72 * Mathf.Pow(hh, 1.15f)) * sc;
            Vector2 Centre(float hh, float t) => CcT(t) + new Vector2((4 + 24 * hh) * sc * Mathf.Sin(t * 7.5f - hh * 5), -hh * HT * Grow(t));
            float start = T;
            // nước quanh chân bị hút vào
            Every(0, T1, 26, x =>
            {
                float a = U(0, 6.28f);
                var Cc = CcT(T - start);
                var pos = Cc + new Vector2(Mathf.Cos(a) * tH, Mathf.Sin(a) * 0.3f * tH);
                Drop(pos, (Cc - pos) * 2.6f + new Vector2(-Mathf.Sin(a), Mathf.Cos(a) * 0.3f) * 150, 0.38f, U(3, 4.5f), 0, Mathf.Sin(a) > 0 ? Front : Back,
                    float.NaN, 0);
            });
            var w3 = W[3];
            int rings = Mathf.Max(2, (int)(T1 / 0.28f));
            for (int i = 0; i < rings; i++) At(0.05f + i * 0.28f, () => RingN(CcT(T - start), 0.4f, 0.9f * tH, 0.2f * tH, w3));
            AtW(TA, () => // khung vẽ sẵn (2026-11-19): AtW cho mão (nuoc_toe) theo đúng bảng nước của tướng ra chiêu
            {
                Shake?.Invoke(0.35f);
                Crown(Cs + new Vector2(0, 4), 0.75f * tH, 0.5f);
            });
            // khung vẽ sẵn (2026-11-19, người dùng xem Hải Long chê "phần lốc xoáy nước ... màu hơi trầm và chưa hợp lắm"): có khung "loc_nuoc"
            // thì thân vòi / lốc là khung lốc nước hai lớp bao quanh đối thủ (LocNuocBao: sau tướng đặc, trước tướng lật + trong mờ 0,5), thay
            // 8 đĩa mảng có viền mực tô bảng nước của tướng. Dâng lên từ TA: cao 15 % → HT trong 0,22 s (hiện dần 0,12 s), chân theo CcT (lốc
            // n_loc lướt từ trước mặt tướng tới chân đối thủ), sụp từ T1: co 30 % và tắt dần trong 0,35 s. Bỏ luôn các hạt bám hình đĩa cũ (sọc
            // bọt trượt quanh mặt phễu, lưỡi sóng viền mực ở hai mép, cụm bọt viền mực ở miệng phễu): khung đã có dải bọt. Giữ nước bị hút vào
            // chân, vòng co, mão nuoc_toe lúc dựng, giọt văng, họa tiết thêm, cú sụp toé; giờ trả về giữ nguyên
            // 2026-11-19 (người dùng: "lốc xoáy làm to lên cho che hết tướng địch"): lốc cao 1,7 tH (chặn mép trên sân, tối thiểu 1,3 tH), giãn
            // ngang 1,9, chân khung hạ 0,1 cao khung dưới chân đối thủ (vòng nước chân lốc ôm quanh chân, đoạn ngang thân nằm ở phần phễu nở). Đo
            // bề ngang khung theo chiều cao: thân phễu ~0,2 bề ngang khung ở 15–30 % cao, 0,45 ở 50 %, 0,65 ở 60–85 %, nên ngang thân đối
            // thủ: chân ~0,7 tH, giữa thân ~1 tH, ngực trở lên ≥ 1,3 tH. Chân (đoạn phễu thon) bù bằng vương miện nuoc_toe toé lặp ở gốc lốc
            // 2026-11-19 (khung lốc TRÙM "loc_nuoc_bao": cột xoáy dày, gốc gần rộng bằng miệng): có khung thì lốc bao quanh đối thủ là nó, cao
            // 1,65 tH (LocBaoCao), giãn ngang 1,25, chân khung hạ 0,04 cao khung: trùm kín từ chân tới đầu, không cần mão bù chân. Lốc n_loc
            // đang lướt tới vẫn là phễu loc_nuoc vừa (1,3 tH, giãn 1,25), tới chân đối thủ thì chuyển sang lốc trùm: phễu tắt dần 0,15 s, lốc
            // trùm hiện dần 0,15 s và nở từ 70 % cao. Chưa có khung trùm: lốc phễu to (giãn 1,9) + mão bù chân như dưới
            bool bao = FbNuoc("loc_nuoc_bao"), pheu = FbNuoc("loc_nuoc");
            bool fbL = bao || pheu;
            if (bao)
            {
                float HB = LocBaoCao(Cd.y, tH), tToi = di ? TA + 0.1f + T_DI : TA;
                bool noi = di && pheu; // lướt bằng phễu rồi nối sang lốc trùm
                if (noi)
                {
                    float HP = 1.3f * tH;
                    AtW(TA, () => LocNuocBao(t => CcT(TA + t), t => HP * (0.15f + 0.85f * EaseOut(t / 0.22f)), tToi - TA + 0.15f, 0.5f, 1.15f, 1.25f, 0.12f,
                        0.15f));
                }
                float t0 = noi ? tToi - 0.02f : TA;
                Func<float, float> caoB = t => HB * (noi ? 0.7f + 0.3f * EaseOut(t / 0.2f) : 0.15f + 0.85f * EaseOut(t / 0.22f)) *
                    (1 - 0.3f * SmoothStep(T1 - t0, T_END - t0, t));
                AtW(t0, () => LocNuocBao(t => CcT(t0 + t) + new Vector2(0, LocBaoHa * caoB(t)), caoB, T_END - t0, 0.5f, 1.15f, LocBaoGian, noi ? 0.15f : 0.12f,
                    0.35f, 18, "loc_nuoc_bao"));
            }
            else if (pheu)
            {
                float HL = Mathf.Clamp((Cd.y - 24) / (0.85f * 1.04f), 1.3f * tH, 1.7f * tH);
                Func<float, float> cao = t => HL * (0.15f + 0.85f * EaseOut(t / 0.22f)) * (1 - 0.3f * SmoothStep(T1 - TA, T_END - TA, t));
                AtW(TA, () => LocNuocBao(t => CcT(TA + t) + new Vector2(0, 0.1f * cao(t)), cao, T_END - TA, 0.5f, 1.15f, 1.9f));
                // gốc lốc: vương miện nước toé lặp phủ phần chân đối thủ (đoạn phễu thon)
                EveryW(TA + 0.18f, T1 - 0.1f, 3.2f, x => ToeNuoc(CcT(T - start) + new Vector2(U(-0.08f, 0.08f) * tH, 2), 0.78f * tH * U(0.9f, 1.1f), 1.6f, Front,
                    17, 0.75f));
            }
            var body = new P { pos = Cd, life = T_END, group = Front, stops = W };
            body.draw = (q, k, buf) =>
            {
                float t = q.age, g = Grow(t);
                if (g < 0.05f) return;
                for (int i = 0; i < N; i++)
                {
                    float hh = (i + 0.5f) / N;
                    var c = Centre(hh, t);
                    float r = Radius(hh) * (0.5f + 0.5f * g), hr = HT * g / N * 0.86f;
                    float tl = 0.16f * Mathf.Sin(t * 7.5f - hh * 5 + 1.3f), ca = Mathf.Cos(tl), sa = Mathf.Sin(tl);
                    int c0 = mp.Count;
                    for (int ly = 0; ly < 3; ly++) // ba đường lồng nhau: vành ngoài, dải xanh giữa, vệt xanh nhạt
                    {
                        float kx = ly == 0 ? 1 : ly == 1 ? 0.92f : 0.36f, ky = ly == 0 ? 1 : ly == 1 ? 0.6f : 0.22f;
                        float dx = ly == 2 ? -0.42f : 0, dy = ly == 0 ? 0 : ly == 1 ? 0.12f : 0.22f;
                        for (int j = 0; j < RN; j++)
                        {
                            float a = 6.2832f * j / RN;
                            float x = dx * r + kx * r * Mathf.Cos(a), y = dy * hr + ky * hr * Mathf.Sin(a);
                            mp.Add(new Vector2(c.x + x * ca - y * sa, c.y + x * sa + y * ca));
                        }
                    }
                    float L = 18 + i * 0.02f;
                    const float Al = 0.86f;
                    MBand(Front, L, MGrow(c0, RN, 2.2f), c0, RN, Ink, Al, true);
                    MBand(Front, L + 0.001f, c0, c0 + RN, RN, q.stops[1], Al);
                    MBand(Front, L + 0.002f, c0 + RN, c0 + 2 * RN, RN, q.stops[2], Al);
                    MFill(Front, L + 0.003f, c0 + 2 * RN, RN, q.stops[3], Al, false);
                }
            };
            if (!fbL) Add(body); // khung vẽ sẵn: có khung lốc thì không vẽ đĩa mảng
            // sọc bọt trượt quanh mặt trước của phễu (từ phải sang trái = phễu đang quay)
            if (!fbL) Every(TA + 0.1f, T1, 16, x =>
            {
                var q = new P { pos = Cd, life = U(0.45f, 0.6f), tb = T - start, hgt = U(0.05f, 0.3f), sz = U(26, 44) * sc, col = U(0, 1) < 0.65f ? FoamC : w3 };
                q.draw = (z, k, buf) =>
                {
                    float t = z.tb + z.age, hh = Mathf.Min(1, z.hgt + 0.75f * k);
                    var c = Centre(hh, t);
                    float R = Radius(hh) * 0.93f, a = (18 + 144 * k) * Mathf.Deg2Rad;
                    var pos = c + new Vector2(R * Mathf.Cos(a), 0.3f * R * Mathf.Sin(a));
                    var tan = new Vector2(-Mathf.Sin(a), 0.3f * Mathf.Cos(a));
                    float alpha = Mathf.Min(1, Mathf.Min(k / 0.15f, (1 - k) / 0.25f)) * 0.95f;
                    float th = (2.5f + 3 * (1 - Mathf.Abs(2 * k - 1))) * sc, len = z.sz * (0.4f + 0.6f * Mathf.Sin(a));
                    Put(buf, Front, 19, S("ell"), z.col, pos, th, Mathf.Max(1, len / th), VelAng(tan), alpha);
                };
                Add(q);
            });
            // mào sóng văng ra ở hai mép phễu (khung vẽ sẵn: bỏ khi có khung lốc)
            if (!fbL) Every(TA + 0.12f, T1, 30, x =>
            {
                float hh = U(0.15f, 1), sd = U(0, 1) < 0.5f ? -1 : 1;
                var c = Centre(hh, T - start);
                Wave(c + new Vector2(sd * Radius(hh) * 0.9f, 0), new Vector2(sd * U(120, 240), -U(60, 200)), U(0.26f, 0.38f), 6,
                    U(11, 17) * (0.6f + 0.4f * hh), Front, 1, 0.35f, 3, 500, 0.72f, 0.25f);
            });
            // miệng phễu: bọt cuộn, giọt văng (khung vẽ sẵn: bọt cuộn bỏ khi có khung lốc, giọt văng giữ)
            if (!fbL) Every(TA + T_UP, T1 + 0.1f, 9, x =>
            {
                float a = U(0, 6.28f);
                var c = Centre(1, T - start);
                float R = Radius(1);
                BotCum(c + new Vector2(R * Mathf.Cos(a), 0.3f * R * Mathf.Sin(a) + 4), new Vector2(Mathf.Cos(a) * 60, -U(10, 50)), U(10, 14),
                    Mathf.Sin(a) > 0 ? Front : Back);
            });
            Every(TA + T_UP, T1, 26, x => Drop(Centre(U(0.5f, 1), T - start) + new Vector2(U(-30, 30), 0),
                new Vector2((U(0, 1) < 0.5f ? -1 : 1) * U(170, 300), -U(40, 160)), 0, U(3, 5), 900, U(0, 1) < 0.5f ? Front : Back, foeFeet.y + U(-10, 24)));
            Every(TA + T_UP, T1, 4, x => WExtra(Centre(U(0.4f, 1), T - start), 1, 220));
            AtW(T1 + 0.15f, () => // vòi sụp: nước đổ xuống toé ra (khung vẽ sẵn 2026-11-19: Splash ra trung_nuoc + nuoc_toe; AtW cho đúng bảng nước)
            {
                Shake?.Invoke(0.4f);
                Splash(foeFeet + new Vector2(0, -0.3f * tH), 0.9f, foeFeet.y, tH, Back);
                RainBack(foeFeet, tH, 16, 0.6f, 0, 0.35f);
                Puddle(foeFeet + new Vector2(0, 3), 20, 1);
            });
            if (!di) HaiLongBao(foeFeet, tH, TA, T1, TA + 0.15f, 3, 6); // 2026-11-19: vòi rồng Hải Long dạng 3 thêm lốc phụ + sét (HatFbThuy.cs)
            return di ? TA + 0.1f + 0.85f * T_DI : TA + 0.15f;
        }

        // cú va nước của chiêu lao tới (trượt, húc, liên hoàn): gọi đúng khung trúng, nước toé lớn ở thân đối thủ, cột nước, mưa giọt
        // dir: hướng cú lao tới (khung vẽ sẵn 2026-11-19: bông trung_nuoc có hướng; null = lật ngẫu nhiên). Có khung nước thì Splash là
        // trung_nuoc + nuoc_toe, cột nước sau lưng là nuoc_toe lớn (BackColumn); cụm hơi nước (không viền), mưa giọt, vệt ướt giữ
        public float NVa(Vector2 foeBody, Vector2 foeFeet, float tH, Vector2? dir = null)
        {
            Shake?.Invoke(0.6f);
            FlashScreen?.Invoke(FlashW);
            Splash(foeBody, 1.25f, foeFeet.y, tH, Front, dir);
            BotCum(foeBody + U2(-20, 20), new Vector2(U(-60, 60), -U(30, 70)), 12, Back, 0, true); // hơi nước bốc thành cụm
            BackColumn(foeFeet, tH);
            RainBack(foeFeet, tH, 14);
            Puddle(foeFeet + new Vector2(0, 3), 26, 1.5f);
            return 0;
        }

        // ================= chọn chiêu nước =================
        public static bool IsNuoc(string kind) => kind != null && kind.StartsWith("n_");

        // chiêu chỉ phát ở khung trúng (không có pha tụ): cú va của chiêu lao tới
        public static bool NuocAtHit(string kind) => kind == "n_va" || kind == "n_la_va" || kind == "n_gai_va" || kind == "n_sat_dap" || kind == "n_sat_dap1"
            || kind == "n_xa_chem";

        // ult: chiêu cuối (tia dài hơn, mưa lâu hơn)
        public float PlayNuoc(string kind, bool ult, Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeFeet, Vector2 foeBody, float tH,
            float lead)
        {
            if (!HasWater) return 0;
            switch (kind)
            {
                case "n_va": return NVa(foeBody, foeFeet, tH, new Vector2(Mathf.Sign(foeFeet.x - casterFeet.x), 0)); // khung vẽ sẵn (2026-11-19): truyền hướng lao tới cho bông toé (trước rơi xuống default)
                case "n_tia": // 2026-11-19: chiêu cuối của tướng có WTheme.tiaTo (Thôn Kình) là tia to theo thân người bắn
                    // 2026-11-19 (người dùng muốn cải thiện "các tia nước" luôn, sau bản thử Tí Tách): MỌI tia nước của tướng Thủy là tia vẽ sẵn
                    // (NTiaKhung; bảng mực tím / chưa có khung thì tia mảng cũ). Bề dày theo thân người bắn: mana 0,22 casterH (26–44), chiêu cuối
                    // 0,28 (34–56), chiêu cuối của tướng há mồm rất to (tiaTo, Thôn Kình) 2,2 × tiaTo = 0,33 casterH (44–68). Riêng từng tướng
                    // (gốc tia đo trên rig: giữa mồm Hải Đăng / Thạch Giải, đầu trượng Giông Bão, giữa hai sừng Uyên Xà; bề dày, cầu đầu nòng, tụ):
                    // NTiaNuoc (HatFbThuy.cs)
                    return NTiaNuoc(ult, casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
                case "n_cau": return NCauNuoc(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // 2026-11-19: Thạch Giải ợ cầu ở giữa mồm, không tụ, cầu × 1,6 (HatFbThuy.cs)
                case "n_bong": return NBong(mouth, foeBody, foeFeet, tH, lead);
                case "n_luoi": return NLuoi(mouth, foeBody, foeFeet, tH, lead);
                case "n_thuong": return NThuong(casterFeet, casterH, foeBody, foeFeet, tH, lead, ult ? 8 : 6);
                case "n_dan": return NDan(mouth, foeBody, foeFeet, tH, lead);
                case "n_ngoc": return NNgoc(mouth, foeBody, foeFeet, tH, lead);
                case "n_muc": return NNgoc(mouth, foeBody, foeFeet, tH, lead, true);
                case "n_song": return NSong(casterFeet, casterH, foeFeet, tH, lead);
                case "n_mua": return NMua(foeFeet, tH, lead, ult ? 1.3f : 1.15f);
                case "n_xoay": return NXoay(foeFeet, tH, lead);
                case "n_voi": return NVoi(foeFeet, tH, lead);
                case "n_loc": return NVoi(foeFeet, tH, lead, casterFeet + new Vector2(Mathf.Sign(foeFeet.x - casterFeet.x) * 0.85f * casterH, 0));
                // chiêu nước mới theo gói mẫu (2026-11-25, HatNuocChieu.cs)
                case "n_lien_dan": return NLienDan(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // Tí Tách: 5 viên đạn nước liên tiếp
                case "n_bong_nay": return NBongNay(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // Thạch Giải: 3 bong bóng nảy
                case "n_cau_nhot": return NCauNhot(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // Thạch Giải: cầu bọc đối thủ rồi vỡ
                case "n_bom": return NBom(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);             // Hải Đăng: bom nước bay vồng nổ cột nước
                case "n_cau_xoay": return NCauXoay(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);   // Giông Bão: cầu xoáy từ đầu trượng
                case "n_mua_giong": return NMuaGiong(casterFeet, casterH, foeBody, foeFeet, tH, lead);        // Giông Bão: mưa giông, cột thác dội, sét
                case "n_song_than": return NSongThan(casterFeet, casterH, mouth, foeFeet, tH, lead);          // Thôn Kình: luồng nước tuôn từ miệng thành sóng thần
                case "n_dao_lien": return NDaoLien(casterFeet, foeBody, foeFeet, tH, lead); // Viêm Đao: chém lửa liên hoàn (Chém nước đổi bảng lửa), nổ lớn ở cú bổ
                case "n_cau_ma": return NCauMa(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);      // Thôn Kình: triệu hồi cầu ma thủy ở thân đối thủ rồi nổ
                case "n_thuy_xa": return NThuyXa(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);    // Uyên Xà: rắn nước trườn từ sừng tới ngoạm
                case "n_xa_chem": return NXaChem(casterFeet, foeBody, foeFeet, tH);                          // Uyên Xà: ba nhát chém nước lúc đuôi quất trúng
                case "n_bao_xoay": return NBaoXoay(foeFeet, tH, lead, false);                                 // Hàn Ngạc Vương: siêu bão xoáy
                case "n_bao_xoay1": return NBaoXoay(foeFeet, tH, lead, true);                                 // Ngạc Nhi: bão xoáy nhẹ
                case "n_loat_cau": return NLoatCau(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);  // Hải Long: mỗi đầu nhả một cầu nước
                case "n_loat_tia": return NLoatTia(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);  // Hải Long: mỗi đầu bắn một tia Water Laser (HatHaiLongTia.cs)
                case "n_la": return NLa(mouth, foeBody, foeFeet, tH, lead); // bộ Mộc (HatMoc.cs): phun lá
                case "n_la_va": return NLaVa(foeBody, foeFeet, tH); // cú húc: lá vỡ tung lúc chạm
                case "n_gai": return HasGai ? NGai(casterFeet, casterH, foeFeet, foeBody, tH, lead) : NLa(mouth, foeBody, foeFeet, tH, lead); // gồng gai: gai trồi từ đất
                case "n_gai_va": return HasGai ? NGaiVa(foeBody, foeFeet, tH) : NLaVa(foeBody, foeFeet, tH); // quả cầu gai tông: gai gãy văng
                case "n_da_va": return NDaVa(foeBody, foeFeet, tH, lead); // Gạc Đá (HatDa.cs): hai tảng tay nện trúng, đá vụn + bụi
                case "n_cau_la": return NCauLa(casterFeet, casterH, foeFeet, foeBody, tH, lead); // tụ cầu năng lượng (gió, lá bị hút vào), ném, nổ lá
                case "n_cau_tia": return NCauTia(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // Lộc Phong (HatLoc.cs): tụ cầu nhỏ giữa hai gạc rồi bắn tia
                case "n_voi_phun": return NVoiPhun(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // Lâm Tượng (HatVoi.cs): vòi phụt luồng hạt cây + lá
                case "n_dam_rung": return NDamRung(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Lâm Tượng: dậm chân, sóng đất chạy tới, rễ và cột lá trồi
                case "n_hat_nga": return NHatNga(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Lâm Tượng, đòn đánh thường: bụi đạp, lá tuột, nện + hất ngà
                case "n_dam_rung1": return NDamRung(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0.7f); // dạng 1 (Tượng Mầm): bản nhẹ, không có rễ trồi
                case "n_cau_mom": return NCauMom(casterFeet, casterH, foeFeet, foeBody, tH, lead);
                case "n_cau_mom1": return NCauMom(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0.10f, 1.02f); // Lộc Phong: tụ cầu to trước mõm, gật đầu nện vào đối thủ
                case "n_mo_dam": return NMoDam(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Linh Điểu (HatChim.cs), đòn đánh thường: lao tới đâm mỏ
                case "n_la_gam": return NLaGam(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Linh Điểu: quạt cánh, lá cánh (mảnh của rig) găm vào đối thủ rồi rút về
                case "n_thach_roi": return NThachRoi(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Linh Điểu: gọi tảng đá phủ rêu rơi từ trời xuống đầu đối thủ
                case "n_thach_roi1": return NThachRoi(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0.78f); // dạng 1 (Điểu Nhi): tảng nhỏ hơn
                case "n_tru_dap": return NTruDap(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Cổ Vương (HatCoVuong.cs, suất hat_de đảo Thổ), đòn đánh thường dạng 2: lao tới đập cột xuống đầu đối thủ
                case "n_vuong_huc": return NVuongHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Cổ Vương Nhi, đòn đánh thường dạng 1: lao húc chóp vương miện
                case "n_re_troi": return HasGai ? NReTroi(casterFeet, casterH, foeFeet, foeBody, tH, lead) : NLa(mouth, foeBody, foeFeet, tH, lead); // Cổ Vương: cắm cột / nện tay, rễ trồi dọc đất tới đối thủ rồi quấn
                case "n_tru_giang": return NTruGiang(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Cổ Vương: lá hút vào lõi, cột khổng lồ (mảnh của rig) giáng xuống đối thủ, rễ trồi
                case "n_tru_giang1": return NTruGiang(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0.6f); // Cổ Vương Nhi: cột nhỏ giáng xuống
                case "n_giac_dam": return NGiacDam(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Giác Mộc (HatGiac.cs), đòn đánh thường: dậm chân, đất nứt chạy tới đối thủ
                case "n_giac_tia": return NGiacTia(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // Giác Mộc: tụ cầu ở đỉnh sừng rồi cúi đầu bắn tia
                case "n_giac_tim": return NGiacTim(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Giác Mộc: mở ngực, tim rực sáng bắn tia lớn
                case "n_rong_dam": return NRongDam(casterFeet, casterH, foeFeet, foeBody, tH, lead); // rồng trúc (HatRong.cs), đòn đánh thường: dậm chân, địa chấn, sét giáng
                case "n_rong_gam": return NRongGam(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // rồng trúc: gầm, sóng âm
                case "n_rong_van": return NRongVan(casterFeet, casterH, foeFeet, foeBody, tH, lead); // rồng trúc: chiêu cuối Vạn Diệp
                case "n_kiem_rut": return NKiemRut(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Voọc Tướng (HatKiem.cs): cúi giữ thế lướt tới, rút kiếm chém, bổ nhát hai
                case "n_kiem_ao": return NKiemAo(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Voọc Tướng: ảo ảnh chém để lại sẹo, tra kiếm thì các vết nổ lại
                case "n_cau_lan": return NCauLan(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Nham Thần (HatNham.cs): chiêu cuối cuộn thành cầu lửa lăn tông, bật về
                case "n_nham_va": return NNhamVa(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Nham Thần, đòn đánh thường: lao tới vả từ trên xuống đầu
                case "n_cau_sung": return NCauSung(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Hỏa Quy (HatRua.cs): chiêu cuối, lửa trên lưng bị hút vào cầu lửa trên mũi sừng, hất sừng phóng cầu
                case "n_cau_sung1": return NCauSung(casterFeet, casterH, foeFeet, foeBody, tH, lead, true); // Hỏa Quy dạng 1 (rùa non): cầu nhỏ, ba dải lửa, mũi sừng ngắn
                case "n_dat_dam": return NDatDam(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Viêm Dũng (HatDat.cs), chiêu mana: lao tới đâm, chém liên hoàn, dung nham trào ở nhát bổ kết
                case "n_nui_huc": return NNuiHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Hỏa Sơn Long (HatNuiLua.cs), đòn đánh thường: lao tới húc
                case "n_nui_cau": return NNuiCau(casterFeet, casterH, mouth, foeFeet, foeBody, tH, lead); // Hỏa Sơn Long: há mồm tụ cầu lửa rồi bắn
                case "n_nui_cau1": return NNuiCau(casterFeet, casterH, mouth, foeFeet, foeBody, tH, lead, 1); // dạng 1 (Hỏa Sơn Nhi)
                case "n_nui_ten": return NNuiTen(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Hỏa Sơn Long: chiêu cuối, 16 đạn tầm nhiệt từ các ống núi lửa
                case "n_nui_ten1": return NNuiTen(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // dạng 1 (Hỏa Sơn Nhi): 8 phát, nổ nhẹ hơn
                case "n_nui_ten2": return NNuiTen(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // dạng 2 (Hỏa Sơn Thú): 12 phát từ năm tháp ống và núi lửa chính
                case "n_nui_cau2": return NNuiCau(casterFeet, casterH, mouth, foeFeet, foeBody, tH, lead, 2); // dạng 2 (Hỏa Sơn Thú)
                case "n_ho_va": return NHoVa(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Bạch Viêm Hổ (HatHo.cs), đòn đánh thường: vả, ba vệt vuốt lửa
                case "n_ho_gam": return NHoGam(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead); // Bạch Viêm Hổ: gầm, sóng xung kích + sóng nhiệt
                case "n_ho_anh": return NHoAnh(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Bạch Viêm Hổ: chiêu cuối, màn âm bản, 12 lượt lướt chém để lại sẹo lửa rồi nổ
                case "n_ho_anh1": return NHoAnh(casterFeet, casterH, foeFeet, foeBody, tH, lead, 6, 0.8f); // dạng 1 (Viêm Hổ Nhi): 6 lượt, nổ nhẹ hơn
                case "n_cau_rua": return NCauMieng(casterFeet, casterH, mouth, foeFeet, foeBody, tH, lead); // Hỏa Quy, chiêu mana: tụ cầu lửa ở mõm rồi bắn
                case "n_kim_phap": return NKimPhap(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Viêm Sư (HatPhap.cs), pháp sư lửa: kim lửa hiện quanh đầu trượng đang giơ, vụt trượng thì phóng
                case "n_cau_phap1": return NCauPhap(casterFeet, casterH, foeFeet, foeBody, tH, lead, true); // Viêm Đồng (dạng 1): trượng ngắn, cầu nhỏ, nổ nhẹ hơn
                case "n_cau_phap": return NCauPhap(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Viêm Sư: chiêu cuối, lửa bị hút vào quả cầu của rig đang phình, mốc ban_cau cầu lao tới đối thủ, nổ lớn
                case "n_sat_tong": return NSatTong(casterFeet, foeFeet, foeBody, tH, lead); // Thiết Tinh (HatSat.cs), đòn đánh thường: lao tới tông, chớp + dăm tinh thể
                case "n_sat_ban1": return NSatBan(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Thiết Tinh Nhi (dạng 1): 8 tinh thể của rig bay găm vào đối thủ
                case "n_sat_ban2": return NSatBan(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thiết Tinh (dạng 2): 10 tinh thể (5 gốc + 5 tách đôi)
                case "n_sat_dap1": return NSatDap(foeFeet, foeBody, tH, 0.8f); // Thiết Tinh Nhi: chiêu cuối dập xuống, vòng cột tinh thể (bản nhẹ)
                case "n_sat_dap": return NSatDap(foeFeet, foeBody, tH, 1f); // Thiết Tinh: chiêu cuối dập xuống, vòng cột tinh thể trồi rồi vỡ
                case "n_giao_dam": return NGiaoDam(casterFeet, foeFeet, foeBody, tH, lead); // Thiết Vệ (HatGiao.cs), đòn đánh thường: lao tới đâm giáo
                case "n_giao_nem1": return NGiaoNem(casterFeet, casterH, mouth, foeFeet, foeBody, tH, lead, 0.85f); // Thiết Vệ Nhi: ném giáo (giáo bay là mảnh của rig), giáo găm nổ, giáo mọc lại trong tay
                case "n_giao_nem": return NGiaoNem(casterFeet, casterH, mouth, foeFeet, foeBody, tH, lead, 1f); // Thiết Vệ: ném giáo
                case "n_kim_sat1": return NKimSat(casterFeet, casterH, foeFeet, foeBody, tH, lead, 7, 0.85f); // Thiết Vệ Nhi: chiêu cuối, 7 kim sắt hiện trên đầu, dậm giáo, kim lao găm
                case "n_kim_sat": return NKimSat(casterFeet, casterH, foeFeet, foeBody, tH, lead, 11, 1f); // Thiết Vệ: chiêu cuối, 11 kim sắt
                case "n_xich_go": return NXichGo(casterFeet, foeFeet, foeBody, tH, lead); // Quỷ Xích (HatXich.cs), đòn đánh thường: bay tới gõ móc lên đầu đối thủ
                case "n_xich_nem1": return NXichNem(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1, 0.85f); // Quỷ Xích Nhi: quay xích, ném móc găm rồi giật về
                case "n_xich_nem": return NXichNem(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2, 1f); // Quỷ Xích: quay xích, ném móc
                case "n_xich_lua1": return NXichLua(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1, 0.8f); // Quỷ Xích Nhi: chiêu cuối xích lửa, trói, cột lửa (bản nhẹ)
                case "n_xich_lua": return NXichLua(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2, 1f); // Quỷ Xích: chiêu cuối xích lửa quay, ném trói, cột lửa rất to
                case "n_soi_go": return NSoiGo(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sói Giáp (HatSoi.cs), đòn đánh thường: lao tới, búa bổ nện
                case "n_soi_nem1": return NSoiNem(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0.85f); // Sói Giáp Con: ném búa xoáy, trúng, búa bay về tay
                case "n_soi_nem": return NSoiNem(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1f); // Sói Giáp: ném búa xoáy
                case "n_soi_huc1": return NSoiHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0); // Sói Giáp Con: chiêu cuối (bản nhẹ)
                case "n_soi_huc": return NSoiHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Sói Giáp: chiêu cuối che khiên, tụ gió, lao xé gió, húc
                case "n_khoang_huc": return NKhoangHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thiết Khoáng (HatKhoang.cs), đòn đánh thường: húc (dạng 2 húc rồi lộn giáng)
                case "n_khoang_ban1": return NKhoangBan(casterFeet, foeFeet, foeBody, tH, lead, 1); // Thiết Khoáng Nhi: hai tay quặng găm
                case "n_khoang_ban2": return NKhoangBan(casterFeet, foeFeet, foeBody, tH, lead, 2); // Thiết Khoáng: hai tay + năm gai găm
                case "n_khoang_dao1": return NKhoangDao(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Thiết Khoáng Nhi: chui đất, gò chạy ngầm, trồi lên húc
                case "n_khoang_dao": return NKhoangDao(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thiết Khoáng: trồi lên húc hai lần
                case "n_cua_huc": return NCuaHuc(casterFeet, foeFeet, foeBody, tH, lead); // Thiết Cưa (HatCua.cs), đòn đánh thường: lao tới húc
                case "n_cua_quat": return NCuaQuat(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thiết Cưa: lao tới, quay người quật đuôi cưa, tia lửa cưa
                case "n_cua_lien": return NCuaLien(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thiết Cưa: chiêu cuối giật dây, hút khí, ghì cưa 11 nhát
                case "n_hon_chem": return NHonChem(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Vong Kỵ (HatHon.cs), đòn đánh thường: lao tới, vung kiếm qua đầu bổ, vệt chém lửa hồn
                case "n_hon_goi1": return NHonGoi(casterFeet, casterH, foeFeet, foeBody, tH, lead, 3, 0.85f); // Vong Kỵ Nhi: giơ kiếm gọi 3 hồn đồng đội lao tới
                case "n_hon_goi": return NHonGoi(casterFeet, casterH, foeFeet, foeBody, tH, lead, 5, 1f); // Vong Kỵ: giơ kiếm gọi 5 hồn đồng đội lao tới
                case "n_hon_kiem1": return NHonKiem(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0.8f); // Vong Kỵ Nhi: chiêu cuối vá kiếm bằng hồn, bổ (bản nhẹ)
                case "n_hon_kiem": return NHonKiem(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1f); // Vong Kỵ: chiêu cuối hút hồn vá kiếm, bổ một nhát cực mạnh
                case "n_robot_ban1": return NRobotBan(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Thần Cơ Nhi (HatRobot.cs), đòn đánh thường: tụ cầu năng lượng ở ổ nắm đấm rồi bắn
                case "n_robot_ban": return NRobotBan(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thần Cơ, đòn đánh thường
                case "n_robot_cau1": return NRobotCau(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Thần Cơ Nhi: tụ cầu năng lượng to giữa hai tay giơ cao, ném xuống đầu đối thủ
                case "n_robot_cau": return NRobotCau(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thần Cơ: cầu to, nổ rất lớn
                case "n_robot_ten1": return NRobotTen(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Thần Cơ Nhi: chiêu cuối mở giáp ngực, 7 tên lửa tầm nhiệt (bản nhẹ)
                case "n_robot_ten": return NRobotTen(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thần Cơ: chiêu cuối 7 tên lửa tầm nhiệt bay cong ngẫu nhiên, nổ lớn
                case "n_phao_ban1": return NPhaoBan(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Pháo Giáp Nhi (HatPhao.cs), đòn thường: nâng nòng bắn một quả đạn sắt vòng cung, nổ lửa
                case "n_phao_ban": return NPhaoBan(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Pháo Giáp, đòn thường
                case "n_phao_mua1": return NPhaoMua(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Pháo Giáp Nhi: 5 quả lên trời, mỗi quả tách 2 tên lửa nhỏ homing lao xuống
                case "n_phao_mua": return NPhaoMua(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Pháo Giáp: 5 quả lên trời, mỗi quả tách 3 tên lửa nhỏ homing lao xuống, nổ lớn
                case "n_phao_cau1": return NPhaoCau(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Pháo Giáp Nhi: chiêu cuối gồng tụ cầu năng lượng ở họng pháo, bắn, giật điện (bản nhẹ)
                case "n_phao_cau": return NPhaoCau(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Pháo Giáp: chiêu cuối gồng tụ cầu năng lượng rất lớn, bắn, nổ rất lớn, giật điện
                case "n_vua_an1": return NVuaAn(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Nhật Hoàng Tử (HatVua.cs), đòn thường "Nhật Ấn": nện trượng, đường lửa dọc đất, ấn + cột năng lượng (bản nhẹ)
                case "n_vua_an": return NVuaAn(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Nhật Vương, đòn thường "Nhật Ấn"
                case "n_vua_tia1": return NVuaTia(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Nhật Hoàng Tử: chiêu mana, ba hành tinh xếp cột trên đầu đối thủ, tia Mặt Trời giáng xuống (bản nhẹ)
                case "n_vua_tia": return NVuaTia(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Nhật Vương: chiêu mana "Tam Tinh Quang Pháo", nổ mặt trời lớn
                case "n_vua_nhat1": return NVuaNhat(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Nhật Hoàng Tử: chiêu cuối nhật thực, ba thiên thạch (bản nhẹ)
                case "n_vua_nhat": return NVuaNhat(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Nhật Vương: chiêu cuối "Nhật Thực Thiên Giáng": màn tối, ba thiên thạch nện, cú cuối rất lớn
                case "n_giap_huc": return NGiapHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thạch Giáp (HatTho.cs), đòn thường: lao húc đầu, dăm đá
                case "n_giap_soi": return NGiapSoi(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thạch Giáp: lắc mai, ba viên sỏi (mảnh của rig) găm
                case "n_giap_mua": return NGiapMua(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thạch Giáp: chiêu cuối pha lê vọt lên trời, mưa pha lê hổ phách
                case "n_tich_dop": return NTichDop(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Tích (HatTho.cs), đòn thường: chồm đớp, vết cắn
                case "n_tich_phien": return NTichPhien(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Tích: ba phiến áo choàng đất nung (mảnh của rig) găm
                case "n_tich_loc": return NTichLoc(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Tích: chiêu cuối dậm đất, lốc cát trùm đối thủ
                case "n_thiem_giang": return NThiemGiang(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm (HatTho.cs), đòn thường: chồm giáng sừng
                case "n_thiem_phun": return NThiemPhun(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm: há hàm hút đá, phun tảng đá
                case "n_thiem_lan": return NThiemLan(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm: chiêu cuối cuộn tròn lăn nện (rig khai lunge)
                case "n_long_vuot": return NLongVuot(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Long (HatTho.cs), đòn thường: lao chém vuốt
                case "n_long_luoi": return NLongLuoi(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Long: ba lưỡi cát trăng khuyết
                case "n_long_cot": return NLongCot(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Long: chiêu cuối nện đất, cột sa thạch trồi ba nhịp
                case "n_vien_dam": return NVienDam(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sơn Viên (HatTho.cs), đòn thường: liên hoàn ba đấm
                case "n_vien_chan": return NVienChan(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sơn Viên: nện đất, sóng chấn gai đá
                case "n_vien_tang": return NVienTang(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sơn Viên: chiêu cuối tụ tảng đá khổng lồ, bốn tay ném
                case "n_giap_huc2": return NGiapHuc(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thạch Giáp dạng 2 (HatTho.cs): lao húc nặng
                case "n_giap_soi2": return NGiapSoi(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thạch Giáp dạng 2: ba cụm pha lê của rig găm
                case "n_giap_mua2": return NGiapMua(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Thạch Giáp dạng 2: mưa pha lê dày, mảnh to
                case "n_tich_dop2": return NTichDop(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Sa Tích dạng 2: chồm đớp nặng
                case "n_tich_phien2": return NTichPhien(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Sa Tích dạng 2: năm phiến mũ trùm găm
                case "n_tich_loc2": return NTichLoc(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Sa Tích dạng 2: đập đất hai lần, lốc cát lớn
                case "n_thiem_dam2": return NThiemDam2(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm dạng 2: lao đâm mũi khối pha lê
                case "n_thiem_phun2": return NThiemPhun(casterFeet, casterH, foeFeet, foeBody, tH, lead, 2); // Tê Thiềm dạng 2: ngả gầm, phun tảng đá lớn
                case "n_thiem_bo2": return NThiemBo2(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tê Thiềm dạng 2: nhảy tới bổ khối pha lê, cột pha lê
                case "n_long_vuot1": return NLongVuot(casterFeet, casterH, foeFeet, foeBody, tH, lead, 0.75f); // Sa Long dạng 1 (rồng non): vồ chém nhẹ
                case "n_long_luoi1": return NLongLuoi(casterFeet, casterH, foeFeet, foeBody, tH, lead, 1); // Sa Long dạng 1: hai lưỡi cát nhỏ
                case "n_long_cot1": return NLongCot1(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Long dạng 1: nện đất, hai cột sa thạch
                case "n_trung_dop": return NTrungDop(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Trùng (HatTho.cs, rig sau_dat_1), đòn thường: đớp nghiền
                case "n_trung_gai": return NTrungGai(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Trùng: giáng đầu xuống đất, ba gai đá đầu ngạnh trồi
                case "n_trung_mieng": return NTrungMieng(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Sa Trùng: chiêu cuối lặn, chạy ngầm, trồi ngoạm
                case "n_thach_vo": return NThachVo(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thiên Thạch Thú (HatThach.cs, suất cu_phu; phiên assets-3c)
                case "n_thach_xoay": return NThachXoay(casterFeet, casterH, foeFeet, foeBody, tH, lead);
                case "n_thach_cau": return NThachCau(casterFeet, casterH, foeFeet, foeBody, tH, lead);
                case "n_thach_xoay1": return NThachXoay1(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thiên Thạch Thú Non (dạng 1, rig tinh_hach_non): ba thiên thạch
                case "n_thach_cau1": return NThachCau1(casterFeet, casterH, foeFeet, foeBody, tH, lead);
                case "n_bun_danh": return NBunDanh(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Bùn Ngoạm (HatBun.cs, rig quai_bun_1), đòn thường: tay bùn co giãn đấm
                case "n_bun_troi": return NBunTroi(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Bùn Ngoạm: cắm tay xuống bùn, nắm đấm bùn khổng lồ trồi
                case "n_bun_ngoam": return NBunNgoam(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Bùn Ngoạm: chiêu cuối lao ngoạm, nuốt, gai đâm, nhổ
                case "n_tinh_nen": return NTinhNen(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thổ Tinh (HatThoTinh.cs, suất giap_nham), đòn thường: nhảy nện hai nắm đấm
                case "n_tinh_gai": return NTinhGai(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thổ Tinh: gầm, mười lưỡi trăng lưng phóng
                case "n_tinh_hang": return NTinhHang(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Thổ Tinh: chiêu cuối thiên thạch bọc, ép, mặt trời, tia nhiệt, nổ nấm
                case "n_tinh_nen1": return NTinhNen1(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tiểu Thổ Tinh (dạng 1, rig thach_de_non)
                case "n_tinh_gai1": return NTinhGai1(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tiểu Thổ Tinh: sáu mảnh vỏ lưng phóng
                case "n_tinh_hang1": return NTinhHang1(casterFeet, casterH, foeFeet, foeBody, tH, lead); // Tiểu Thổ Tinh: chiêu cuối (nhẹ hơn)
                default: return NVa(foeBody, foeFeet, tH);
            }
        }

        // giây tướng giữ dáng nhả (khung trúng của clip) sau lúc nhả: tia tới khi dòng tắt, bong bóng tới khi thổi xong, thương tới khi
        // mũi cuối phóng đi, mưa và vòi rồng gần hết hiệu ứng
        public static float HoldNuoc(string kind, bool ult) =>
            kind switch
            {
                "n_tia" => (ult ? 1.25f : 0.88f) + 0.05f,
                "n_cau" => 0.12f,
                "n_ngoc" => 0.1f,
                "n_muc" => 0.1f,
                "n_bong" => 0.85f,
                "n_luoi" => 0.32f,
                "n_thuong" => (ult ? 8 : 6) * 0.1f,
                "n_song" => 0.3f,
                "n_mua" => ult ? 1.05f : 0.9f,
                "n_xoay" => 0.4f,
                "n_voi" => 1.2f,
                "n_loc" => 0.3f,
                "n_lien_dan" => 4 * 0.11f + 0.1f,
                "n_bong_nay" => 2 * 0.13f + 0.12f,
                "n_cau_nhot" => 0.12f,
                "n_bom" => 0.14f,
                "n_cau_xoay" => 0.16f,
                "n_mua_giong" => 1.05f,
                "n_song_than" => 0.45f,
                "n_thuy_xa" => 0.2f,
                "n_dao_lien" => 0.32f,
                "n_cau_ma" => 0.6f,     // cầu prefab gốc giữ 0,5 s sau khung há rồi mới nổ
                "n_bao_xoay" => 1.2f,
                "n_bao_xoay1" => 1.2f,
                "n_loat_cau" => 0.35f,
                "n_loat_tia" => LoatTiaGiu,
                "n_la" => LaDur + 0.04f,
                "n_cau_tia" => 0.88f + 0.05f,
                "n_giac_tia" => 0.88f + 0.05f,
                "n_giac_tim" => 1.0f + 0.05f,
                "n_rong_gam" => RongGamDur + 0.04f,
                "n_kim_sat" => 0.3f,
                "n_kim_sat1" => 0.25f,
                _ => 0,
            };
    }
}
