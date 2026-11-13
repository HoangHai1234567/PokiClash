// Bộ Thủy của lớp hạt chồng lớp phẳng (2026-11-10; chuyển từ ArtGen/Spine/bo_thuy.py, sổ công thức ở skill pokiclash-fx-congthuc
// mục 5b). Hạt nước (lưỡi sóng cuộn, giọt, bọt, vương miện nước) là ảnh xám GPT nhuộm bằng Image.color; khối nước lớn (lõi tia, con
// sóng thần, lưỡi trăng khuyết, cột phun, thân vòi rồng) là mảng đa giác tô phẳng gửi sang HatMang.
// Khác bộ Hỏa: chiêu nước được gọi lúc clip BẮT ĐẦU, kèm lead = thời gian tới khung nhả của clip. Pha tụ nước chạy trong lúc tướng
// lấy đà, nước nhả đúng khung nhả (người dùng 2026-11-10: sửa animation cho khớp hiệu ứng). Hàm trả thời gian tới lúc trúng.
// Biến tĩnh ở file này không được dùng biến tĩnh của HatLua.cs lúc khởi tạo (thứ tự khởi tạo giữa hai file không chắc).
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
        }

        static Color[] WPal(Color d, Color m, Color l) => new[] { C(43, 33, 24), d, m, l, C(244, 252, 255) };

        static readonly WTheme WDefault = new WTheme { w = WPal(C(30, 104, 190), C(58, 150, 226), C(140, 208, 246)) };
        static readonly Dictionary<string, WTheme> WThemes = new Dictionary<string, WTheme>
        {
            // cáo nước xanh ngọc, đuôi sóng
            { "tieu_y", new WTheme { w = WPal(C(28, 118, 190), C(64, 170, 226), C(156, 222, 244)) } },
            // chim cánh cụt băng: nước xanh băng, mảnh băng văng
            { "canh_cut", new WTheme { w = WPal(C(36, 122, 150), C(104, 194, 222), C(190, 232, 244)), fx = new Theme { extra = "tinh_the", extraCol = C(196, 234, 248) } } },
            // chim đàn tím: nước tím lam, sao lấp lánh
            { "mi_nhi", new WTheme { w = WPal(C(92, 84, 198), C(134, 148, 236), C(192, 212, 250)), fx = new Theme { extra = "sao", extraCol = C(232, 214, 255) } } },
            // dê biển vảy xanh ngọc
            { "ma_ket", new WTheme { w = WPal(C(16, 138, 160), C(44, 200, 212), C(160, 238, 236)) } },
            // cá mập xanh thẫm
            { "vay_lam", new WTheme { w = WPal(C(26, 62, 162), C(50, 112, 216), C(132, 190, 244)) } },
            // cua pha lê: nước xanh pha lê nhạt, mảnh pha lê
            { "kuba", new WTheme { w = WPal(C(52, 146, 200), C(116, 204, 236), C(202, 238, 250)), fx = new Theme { extra = "tinh_the", extraCol = C(222, 244, 252) } } },
            // rồng băng: mảnh băng
            { "thuong_lam", new WTheme { w = WPal(C(30, 104, 190), C(58, 150, 226), C(140, 208, 246)), fx = new Theme { extra = "tinh_the", extraCol = C(190, 232, 250) } } },
            // rùa xanh lục
            { "huyen_vu", new WTheme { w = WPal(C(20, 128, 132), C(52, 188, 178), C(168, 234, 216)) } },
            // lân chuông: sao vàng
            { "lam_quan", new WTheme { w = WPal(C(34, 96, 196), C(70, 146, 232), C(150, 204, 248)), fx = new Theme { extra = "sao", extraCol = C(255, 224, 110) } } },
            { "giot_suong", new WTheme { w = WPal(C(20, 120, 150), C(50, 176, 200), C(150, 226, 234)) } },
            // lô 10 tướng mới đảo Thủy (2026-11-11), màu theo bảng màu từng dòng (ArtGen/Spine/inbox/tm0*_ghichu.md); mực và bọt chung
            // giọt mưa võ sĩ: lam đại dương #1F5DB5, lam ngọc sáng #35BFE6, bọt nhạt
            { "ti_tach", new WTheme { w = WPal(C(31, 93, 181), C(53, 191, 230), C(158, 223, 243)) } },
            // cua ẩn sĩ nhà đá: giáp chàm #3D5486, vỏ lam xám #6A8BBB, lam bọt #BFE6E2; mảnh đá bazan văng
            // suất này nay là dòng ếch xanh (2026-11-11): bỏ họa tiết mảnh đá của cua; màu nước tạm giữ, chờ người dùng chọn
            { "thach_giai", new WTheme { w = WPal(C(61, 84, 134), C(106, 139, 187), C(191, 230, 226)) } },
            // nòng nọc / ếch xoáy: cô-ban #2457C5, cerulean #3FA9E0, vây nhạt #9FE1F0
            { "ca_den", new WTheme { w = WPal(C(52, 66, 143), C(76, 95, 196), C(155, 168, 242)) } },   // chàm của cá đèn lồng
            // hà mã: hồn nước ba lam #2B7FD6, #4FB6EE, #A6DEF8
            { "ha_ba", new WTheme { w = WPal(C(43, 127, 214), C(79, 182, 238), C(166, 222, 248)) } },
            // sò ngọc: mòng két #1F9AA8, ngọc lam #36C2B4, ngọc lam nhạt #7ED8CB; gai san hô cam văng
            // suất này nay là dòng bạch tuộc quái vật (2026-11-12, mã bach_tuoc): nước là MỰC, đen tím than nhạt dần; bỏ gai san hô
            { "so_ngoc", new WTheme { w = WPal(C(40, 35, 52), C(74, 66, 96), C(140, 130, 166)) } },
            // kỳ giông mưa bão: chàm bão #34477E, xanh đá mưa #6E88BC, lam nhạt #9CC0E8; mây giông xám bay lên
            { "giong_bao", new WTheme { w = WPal(C(42, 53, 128), C(47, 159, 179), C(190, 232, 244)) } },   // pháp sư nước: chàm của mũ, lam ngọc của áo, lam băng
            // cá voi biến dị (2026-11-11, thay cá voi sen): lam đá sẫm #2F4A6E, lam biển #4F86B0, trắng băng #BFE3EE; mảnh đá đen văng
            { "lien_kinh", new WTheme { w = WPal(C(47, 74, 110), C(79, 134, 176), C(191, 227, 238)), fx = new Theme { extra = "tinh_the", extraCol = C(58, 56, 66) } } },
            // rắn vực sâu: chàm vực #2E2F6E, chàm xám #5058A8, bạc hà #8FE3D0; chấm đèn bạc hà
            { "uyen_xa", new WTheme { w = WPal(C(34, 78, 190), C(64, 140, 232), C(134, 214, 240)) } },   // rắn nước có sừng (2026-11-11): lam cô-ban của thân, nhạt dần về màu đốm bong bóng; bỏ họa tiết sao của rắn đèn cũ
            // cá sấu băng: petrol sẫm #1F5566, petrol #3C8396, cạnh băng #9DBAC6; mảnh băng đục
            // suất này nay là dòng rồng vây (2026-11-12, mã rong_vay): chàm của thân #34408F, lam ngọc của vây #49BFC4, lam nhạt; bỏ mảnh băng
            { "han_ngac", new WTheme { w = WPal(C(52, 64, 143), C(73, 191, 196), C(178, 226, 230)) } },
            // rồng biển nhiều đầu: ngọc bích sẫm, ngọc bích #2FA79B, bạc hà #A6E6D8; sao vàng như gạc
            { "hai_long", new WTheme { w = WPal(C(31, 127, 120), C(47, 167, 155), C(166, 230, 216)), fx = new Theme { extra = "sao", extraCol = C(233, 184, 74) } } },
            // đảo Mộc, tinh linh rừng mập (2026-11-12, dòng Mầm Ú, id mam_u; chiêu lá ở HatMoc.cs): lục lá đậm của mầm, lục non, lục nhạt của thân;
            // sao vàng văng lúc húc bụng
            { "mam_u", new WTheme { w = WPal(C(62, 140, 88), C(156, 204, 92), C(206, 230, 140)), fx = new Theme { extra = "sao", extraCol = C(255, 226, 120) } } },
            // đảo Mộc, Cầu Gai (2026-11-12, suất tien_la; chiêu gai ở HatMoc.cs): lục sẫm của thân, lục non, kem của gai; sao kem văng lúc trúng
            { "tien_la", new WTheme { w = WPal(C(52, 120, 72), C(132, 186, 96), C(238, 226, 176)), fx = new Theme { extra = "sao", extraCol = C(250, 240, 200) } } },
            // đảo Mộc, Gạc Đá (2026-11-12, suất gac_da; chiêu ở HatDa.cs): lục ngọc của hạt mầm (đậm, tươi, nhạt); đá vụn nâu xám văng lúc trúng
            // đảo Mộc, Lâm Tượng (2026-11-12, ma mút rừng, suất phong_linh; chiêu ở HatVoi.cs): lục sẫm và lục tươi của áo lá, sao màu mật của ngà
            { "phong_linh", new WTheme { w = WPal(C(40, 124, 66), C(100, 176, 74), C(170, 212, 84)), fx = new Theme { extra = "sao", extraCol = C(238, 212, 150) } } },
            { "gac_da", new WTheme { w = WPal(C(30, 150, 104), C(64, 206, 140), C(170, 236, 196)), fx = new Theme { extra = "giap", extraCol = C(128, 120, 104) } } },
            // đảo Mộc, Lộc Phong (2026-11-12, suất bom_la; chiêu ở HatLoc.cs): lục bảo của pha lê và vân nhựa trên gạc (đậm, tươi, nhạt); sao vàng lá phong văng lúc trúng
            { "bom_la", new WTheme { w = WPal(C(30, 150, 110), C(64, 206, 150), C(184, 240, 212)), fx = new Theme { extra = "sao", extraCol = C(240, 172, 62) } } },
            // đảo Mộc, Linh Điểu (2026-11-12, chim bảo hộ rừng, suất gio_loc; chiêu ở HatChim.cs): lục sẫm của gân lá, lục lá cánh, lục non; cánh hoa hồng của cành cánh văng lúc trúng
            { "gio_loc", new WTheme { w = WPal(C(42, 106, 58), C(76, 154, 82), C(147, 198, 99)), fx = new Theme { extra = "canh_sen", extraCol = C(242, 166, 188) } } },
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

        void DrawDrop(P p, float k, List<Item> buf)
        {
            float s = 2.6f * p.sz * (1 - SmoothStep(0.8f, 1, k));
            if (s < 1) return;
            float sp = p.vel.magnitude;
            var d = sp > 5 ? p.vel / sp : new Vector2(0, 1);
            float ang = TipAngle(-d); // đuôi nhọn ở phía sau hướng bay
            var w = p.stops ?? W;
            Put(buf, p.group, 40, S("drops_" + (p.seed & 3)), Ink, p.pos, s + 4, 1, ang);
            Put(buf, p.group, 40.3f, S("drop_" + (p.seed & 3)), w[2], p.pos, s, 1, ang);
            Put(buf, p.group, 40.6f, S("drop_" + (p.seed & 3)), w[3], p.pos + d * s * 0.1f, s * 0.56f, 1, ang);
        }

        public P Drop(Vector2 pos, Vector2 vel, float life = 0, float r = 5, float grav = 900, int group = Front, float ground = float.NaN,
            float drag = 0.6f)
        {
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

        // vương miện nước mọc từ mặt đất rồi lún xuống (đáy bám đất)
        void Crown(Vector2 feet, float wd, float life = 0.42f, int group = Front)
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

        // nước toé lúc trúng: chớp toé, vành lưỡi sóng toả đều, giọt văng vòng cung, bọt, vương miện nước, vòng sóng
        void Splash(Vector2 c, float sc, float ground, float tH, int group = Front)
        {
            BurstFlash(c, 0.72f * tH * sc, group);
            int n = (int)(8 * sc + 1);
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(-0.3f, 0.3f)) / n;
                Wave(c + U2(-4, 4), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(200, 330) * sc, U(0.3f, 0.42f), 8 * sc, U(14, 19) * sc, group, 1, 0.15f,
                    4.5f, 300);
            }
            for (int i = 0; i < (int)(14 * sc); i++)
            {
                float a = (-90 + U(-85, 85)) * Mathf.Deg2Rad;
                Drop(c + U2(-6, 6), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(240, 460) * sc, 0, U(3, 6), 900, U(0, 1) < 0.6f ? group : Back,
                    ground + U(-10, 18));
            }
            for (int i = 0; i < (int)(5 * sc); i++) Foam(c + U2(-18, 18) * sc, null, 0, 4, U(9, 14) * sc, group);
            var feet = new Vector2(c.x, ground);
            Crown(feet + new Vector2(0, 4), 0.78f * tH * sc);
            Ripple(feet, 0.12f * tH, 0.75f * tH * sc);
            var w3 = W[3];
            At(0.12f, () => Ripple(feet, 0.08f * tH, 0.5f * tH * sc, 0.5f, w3));
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

        // tụ nước về điểm cFn(giây từ lúc gọi): giọt và lưỡi sóng nhỏ bay trôn ốc vào tâm, vòng nước co lại dần
        void Gather(Func<float, Vector2> cFn, float t0, float t1, float reach = 85, float rate = 60, int group = Front)
        {
            if (t1 - t0 < 0.05f) return;
            float start = T;
            Every(t0, t1, rate, x =>
            {
                float R = U(0.7f, 1) * reach;
                bool big = U(0, 1) < 0.3f;
                var q = new P
                {
                    life = U(0.3f, 0.42f), seed = rng.Next(4), group = group, sz = U(3, 5.5f), r0 = 5, r1 = U(7, 10), tip = 1, tipUp = 0,
                    fade = 0.75f, ph = U(0, 6.28f), R0 = R, stops = W
                };
                q.pos = cFn(T - start) + new Vector2(Mathf.Cos(q.ph), Mathf.Sin(q.ph) * 0.8f) * R;
                q.upd = (z, dt, s) =>
                {
                    float k = Mathf.Min(1, z.age / z.life);
                    float a = z.ph + 4.5f * k * k;
                    float rr = z.R0 * Mathf.Pow(1 - k, 1.3f);
                    var np = cFn(s.T - start) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * rr;
                    z.vel = (np - z.pos) / Mathf.Max(dt, 1e-5f);
                };
                if (big) q.draw = DrawWave;
                else q.draw = DrawDrop;
                Add(q);
            });
            int n = Mathf.Max(1, (int)((t1 - t0) / 0.22f));
            var w3 = W[3];
            for (int i = 0; i < n; i++)
                At(t0 + i * 0.22f, () => RingN(cFn(T - start), 0.34f, reach * 0.9f, reach * 0.16f, w3, 1, group, 18));
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

        void Puddle(Vector2 pos, float R = 22, float life = 1.3f)
        {
            var p = new P { pos = pos, life = life, group = Floor, sz = R, stops = W };
            p.draw = (q, k, buf) =>
            {
                float a = Mathf.Min(1, k / 0.12f), f = 1 - k * k * k;
                Put(buf, Floor, 2, S("ell"), Ink, q.pos, (q.sz + 4) * a * f, 3.3f, 0, 0.9f);
                Put(buf, Floor, 3, S("ell"), q.stops[2], q.pos, q.sz * a * f, 3.4f);
                Put(buf, Floor, 4, S("ell"), q.stops[3], q.pos + new Vector2(-6, -1), q.sz * 0.55f * a * (1 - k * k), 3.8f);
            };
            Add(p);
        }

        // mưa giọt rơi lại quanh c sau khi nước bắn lên
        void RainBack(Vector2 c, float tH, int n = 16, float spread = 0.8f, float t0 = 0.3f, float t1 = 0.75f) =>
            Every(t0, t1, n / (t1 - t0), x => Drop(c + new Vector2(U(-spread, spread) * tH, -U(0.9f, 1.35f) * tH), new Vector2(U(-20, 20), 120), 0,
                U(3, 5), 900, U(0, 1) < 0.5f ? Front : Back, c.y + U(-10, 20)));

        // cột lưỡi sóng dựng lên sau lưng đối thủ (sau cú trúng lớn)
        void BackColumn(Vector2 foeFeet, float tH, float dur = 0.28f, float rate = 80) =>
            Every(0, dur, rate, x => Wave(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -4), new Vector2(U(-50, 50), -U(380, 620) * (1 - 0.4f * x)),
                U(0.4f, 0.55f), 8, U(16, 24), Back, 1, 0.5f, 1.6f, 900, 0.72f, 0.5f));

        static readonly Color FlashW = new Color(0.9f, 0.97f, 1f, 0.3f);

        // ================= CHIÊU NƯỚC =================
        // lead: giây từ lúc gọi (đầu clip) tới khung nhả của clip. Mỗi hàm trả giây từ lúc gọi tới lúc trúng đối thủ.

        // tia nước: tụ ở miệng trong lúc lấy đà, tới khung nhả thì bắn dòng nước liền (lõi mảng + lưỡi sóng cuộn chạy đè lên)
        public float NTia(Vector2 mouth, Vector2 target, Vector2 foeFeet, float casterGround, float tH, float lead, float dur = 0.88f)
        {
            var dd = target - mouth;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            var src = mouth + u * 14;
            float T0 = Mathf.Max(0.14f, lead), T1 = T0 + dur;
            const float SP = 1150;
            float travel = Mathf.Max(0.03f, (dist - 30) / SP);
            Gather(t => src, 0, T0 - 0.04f, 60, 55);
            Orb(t => src, T0, T1 + 0.05f, 17,
                a => a < T0 ? 17 * EaseOut(a / T0) : 17 * (1 - 0.6f * (a - T0) / (T1 - T0)) * (1 - SmoothStep(T1 - 0.1f, T1 + 0.05f, a)));
            At(T0, () =>
            {
                Shake?.Invoke(0.2f);
                for (int i = 0; i < 4; i++) Foam(src + U2(-8, 8), null, 0, 4, 10);
            });
            var core = new P { pos = src, life = dur + travel + 0.1f, group = Front, stops = W };
            core.draw = (q, k, buf) =>
            {
                float a = q.age;
                float head = Mathf.Min(dist - 18, SP * a), tail = Mathf.Max(0, SP * (a - dur));
                if (head - tail < 30) return;
                int n = Mathf.Max(2, Mathf.CeilToInt((head - tail) / 12) + 1);
                for (int li = 0; li < 4; li++)
                {
                    float wf = li < 2 ? 1 : li == 2 ? 0.66f : 0.28f, off = li < 2 ? 0 : li == 2 ? -0.12f : -0.3f, grow = li == 0 ? 2.4f : 0;
                    int a0 = mp.Count;
                    for (int pass = 0; pass < 2; pass++)
                        for (int i = 0; i < n; i++)
                        {
                            float x = tail + (head - tail) * i / (n - 1);
                            float hw = (7.5f + 1.6f * Mathf.Sin(x * 0.07f - a * 30)) * Mathf.Min(1, Mathf.Min((x - tail) / 26 + 0.25f, (head - x) / 16 + 0.45f));
                            var c = src + u * x + nrm * (3 * Mathf.Sin(x * 0.045f - a * 22) + off * hw);
                            mp.Add(c + nrm * ((pass == 0 ? 1 : -1) * (hw * wf + grow)));
                        }
                    MRibbon(Front, 9 + li * 0.1f, a0, a0 + n, n, li == 0 ? Ink : q.stops[li]);
                }
            };
            At(T0, () => Add(core));
            Every(T0, T1, x => 90 * (x < 0.1f ? 1.4f : 1) * Mathf.Min(1, (1 - x) * dur / 0.14f), x =>
            {
                float a = U(-1, 1) * 2.5f * Mathf.Deg2Rad;
                var dv = u * Mathf.Cos(a) + nrm * Mathf.Sin(a);
                var q = Wave(src + dv * U(0, 10) + nrm * U(-3, 3), dv * SP * U(0.95f, 1.05f), travel * U(0.95f, 1.08f), 14, U(17, 22), Front, 1, 0.12f, 0,
                    0, 0.9f, 0.35f);
                q.upd = (z, dt, s) => z.vel += nrm * (Mathf.Sin(z.age * 24 + z.ph) * 700 * dt); // dòng nước lượn
            });
            Every(T0 + 0.05f, T1, 26, x =>
            {
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                Drop(src + u * dist * U(0.15f, 0.85f) + nrm * sd * 10, u * U(120, 260) + nrm * sd * U(90, 200) + new Vector2(0, -60), 0, U(2.5f, 4.5f),
                    900, Front, casterGround + (foeFeet.y - casterGround) * U(0.2f, 0.9f) + U(0, 30));
            });
            float tHit = T0 + travel;
            Every(tHit, T1 + travel, 38, x =>
            {
                float a = Mathf.Atan2(-u.y, -u.x) + U(-1.3f, 1.3f);
                Drop(target + U2(-10, 10), new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.5f) * U(200, 420), 0, U(3, 5.5f), 900,
                    U(0, 1) < 0.6f ? Front : Back, foeFeet.y + U(-10, 18));
            });
            Every(tHit, T1 + travel, 22, x => Foam(target + U2(-16, 16), U2(-60, 60), 0, 4, U(9, 14)));
            Every(tHit, T1 + travel, 9, x => Wave(target + U2(-8, 8), new Vector2((U(0, 1) < 0.5f ? -1 : 1) * U(120, 240), -U(60, 200)), 0.34f, 7,
                U(12, 16), Front, 1, 0.3f, 4, 500));
            int rip = Mathf.Max(1, Mathf.CeilToInt(dur / 0.24f));
            for (int i = 0; i < rip; i++)
                At(tHit + i * 0.24f, () =>
                {
                    Ripple(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.7f * tH);
                    Crown(foeFeet + new Vector2(U(-10, 10), 6), 0.7f * tH, 0.36f);
                });
            At(tHit, () => Shake?.Invoke(0.3f));
            At(T1 + travel, () => Splash(target, 0.8f, foeFeet.y, tH));
            return tHit;
        }

        // cầu nước: cầu lớn dần ở miệng trong lúc lấy đà, tới khung nhả thì ném vòng cung, vỡ thành nước toé, cột nước, mưa giọt
        public float NCau(Vector2 mouth, Vector2 target, float casterGround, Vector2 foeFeet, float tH, float lead)
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
            Gather(Path, 0, T0 - 0.05f, 90, 75);
            Orb(Path, T0 - 0.05f, T0 + TT, 30);
            At(T0, () =>
            {
                Shake?.Invoke(0.15f);
                for (int i = 0; i < 4; i++) Foam(src + U2(-10, 10), null, 0, 4, 11);
            });
            Every(T0, T0 + TT, 34, x => Drop(Path(T - start) + U2(-14, 14), new Vector2(U(-50, 50), U(-40, 60)), 0, U(3, 5), 900, Front,
                casterGround + (foeFeet.y - casterGround) * x + U(-5, 30)));
            Every(T0, T0 + TT, 24, x => Foam(Path(T - start) + U2(-10, 10), new Vector2(0, -15), 0, 4, U(8, 12)));
            Every(T0, T0 + TT, 30, x =>
            {
                float t = T - start;
                Wave(Path(t), -Unit(Path(t + 0.02f) - Path(t)) * U(40, 120) + U2(-40, 40), 0.22f, 9, 13, Front, 1, 0.1f, 3);
            });
            At(T0 + TT, () =>
            {
                Shake?.Invoke(0.6f);
                FlashScreen?.Invoke(FlashW);
                Splash(target, 1.25f, foeFeet.y, tH);
                BackColumn(foeFeet, tH);
                RainBack(foeFeet, tH, 18);
                Puddle(foeFeet + new Vector2(0, 3));
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
                    Foam(home, null, 0, 4, 10);
                    for (int j = 0; j < 3; j++) Drop(home + U2(-10, 10), new Vector2(U(-60, 60), -U(20, 90)), 0.35f, 2.8f);
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
                        if (s.U(0, 1) < 0.5f) s.Drop(z.pos - dv * 26, -dv * 80 + s.U2(-50, 50), 0.25f, 3, 200);
                        if (s.U(0, 1) < 0.25f) s.Foam(z.pos - dv * 28, Vector2.zero, 0.3f, 3, 6);
                        if (Vector2.Dot(z.aim - z.pos, z.vel) <= 0)
                        {
                            z.dead = true;
                            s.Shake?.Invoke(0.14f);
                            s.BurstFlash(z.aim, 0.34f * tH, Front, 0.1f);
                            for (int j = 0; j < 5; j++)
                            {
                                float a = s.U(0, 6.28f);
                                s.Drop(z.aim, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f) * s.U(140, 300), 0.4f, 3.2f);
                            }
                            s.Foam(z.aim + s.U2(-8, 8), null, 0, 4, 9);
                            s.WExtra(z.aim, 1, 240);
                        }
                    };
                    q.draw = (z, k, buf) =>
                    {
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
            At(end, () =>
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
            At(T0 - DanTravel, () =>
            {
                var aim = target + new Vector2(U(-0.1f, 0.1f), U(-0.08f, 0.1f)) * tH;
                var dd = aim - mouth;
                float dist = Mathf.Max(1, dd.magnitude);
                var u = dd / dist;
                for (int i = 0; i < 3; i++) Foam(mouth + U2(-6, 6), -u * U(20, 70) + U2(-30, 30), 0.24f, 3, 9);
                for (int i = 0; i < 4; i++) Drop(mouth + U2(-5, 5), -u * U(40, 120) + new Vector2(U(-70, 70), -U(30, 110)), 0.32f, 2.6f);
                var q = new P { pos = mouth, life = DanTravel + 0.25f, aim = aim, group = Front, stops = W, vel = u * (dist / DanTravel), fly = true };
                q.upd = (z, dt, s) =>
                {
                    var dv = Unit(z.vel);
                    if (s.U(0, 1) < 0.7f) s.Drop(z.pos - dv * 20, -dv * 70 + s.U2(-45, 45), 0.22f, 2.8f, 240);
                    if (s.U(0, 1) < 0.3f) s.Foam(z.pos - dv * 22, Vector2.zero, 0.26f, 3, 7);
                    if (Vector2.Dot(z.aim - z.pos, z.vel) <= 0)
                    {
                        z.dead = true;
                        s.Shake?.Invoke(0.12f);
                        s.BurstFlash(z.aim, 0.44f * tH, Front, 0.12f);
                        for (int j = 0; j < 6; j++)
                        {
                            float a = s.U(0, 6.28f);
                            s.Drop(z.aim, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f) * s.U(150, 320), 0.4f, 3.2f);
                        }
                        for (int j = 0; j < 2; j++) s.Foam(z.aim + s.U2(-9, 9), null, 0, 4, 10);
                        s.WExtra(z.aim, 1, 240);
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
        static readonly Color MucA = C(40, 35, 52), MucB = C(92, 82, 116);
        public const float NgocTravel = 0.2f;

        public float NNgoc(Vector2 mouth, Vector2 target, Vector2 foeFeet, float tH, float lead, bool muc = false)
        {
            float T0 = Mathf.Max(0.05f, lead);
            At(T0, () =>
            {
                var aim = target + new Vector2(U(-0.06f, 0.06f), U(-0.06f, 0.08f)) * tH;
                var dd = aim - mouth;
                float dist = Mathf.Max(1, dd.magnitude);
                var u = dd / dist;
                Shake?.Invoke(0.2f);
                BurstFlash(mouth, 0.3f * tH, Front, 0.1f);
                for (int i = 0; i < 4; i++) Foam(mouth + U2(-8, 8), -u * U(20, 80) + U2(-30, 30), 0.26f, 3, 10);
                for (int i = 0; i < 7; i++) Drop(mouth + U2(-6, 6), u * U(60, 260) + new Vector2(U(-120, 120), -U(40, 200)), 0.36f, U(2.4f, 3.6f));
                var q = new P
                {
                    pos = mouth, life = NgocTravel + 0.3f, aim = aim, group = Front, stops = W, vel = u * (dist / NgocTravel), fly = true,
                    seed = rng.Next(4), sz = (muc ? 0.13f : 0.085f) * tH,
                };
                q.upd = (z, dt, s) =>
                {
                    var dv = Unit(z.vel);
                    if (s.U(0, 1) < 0.8f) s.Drop(z.pos - dv * z.sz, -dv * 60 + s.U2(-55, 55), 0.24f, 2.8f, 300);
                    if (s.U(0, 1) < 0.25f) s.Foam(z.pos - dv * z.sz, Vector2.zero, 0.24f, 3, 7);
                    if (Vector2.Dot(z.aim - z.pos, z.vel) <= 0)
                    {
                        z.dead = true;
                        s.Shake?.Invoke(0.45f);
                        s.BurstFlash(z.aim, 0.6f * tH, Front, 0.13f);
                        s.Splash(z.aim, 0.85f, foeFeet.y, tH);
                        for (int j = 0; j < 9; j++)
                        {
                            float a = s.U(0, 6.28f);
                            s.Drop(z.aim, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.5f) * s.U(160, 380), 0.42f, 3.4f);
                        }
                        for (int j = 0; j < 3; j++) s.Foam(z.aim + s.U2(-10, 10), null, 0, 4, 11);
                        s.Puddle(foeFeet + new Vector2(0, 3));
                    }
                };
                q.draw = (z, k, buf) =>
                {
                    float rr = z.sz * (z.age < 0.04f ? 0.55f + 0.45f * z.age / 0.04f : 1);
                    float ang = TipAngle(Unit(z.vel));
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
        public float NSong(Vector2 casterFeet, float casterH, Vector2 foeFeet, float tH, float lead)
        {
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
            At(T0 - TR, () =>
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
                float hg = (0.55f + 0.6f * pr) * tH * EaseOut(q.age / 0.22f) * fall;
                float wd = (0.5f + 0.25f * pr) * tH * (1 + 0.6f * (1 - fall));
                if (hg < 4) return;
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
            Every(T0, T0 + TT, 46, x =>
            {
                var c = Now(out float pr);
                float sz = 9 + 8 * pr;
                Wave(c + new Vector2(sx * U(0.1f, 0.5f) * tH * 0.6f, -U(0, 14)), new Vector2(sx * U(160, 300), -U(120, 300)), U(0.26f, 0.36f), sz * 0.6f,
                    sz, Front, 1, 0.5f, 2, 900, 0.72f, 0.3f);
            });
            Every(T0, T0 + TT, 30, x => Foam(Now(out _) - u * 0.75f * tH + side * U(-30, 30), new Vector2(0, -8), 0, 5, U(9, 13), Back));
            var w3 = W[3];
            Every(T0, T0 + TT, 7, x => RingN(Now(out _) - u * 0.8f * tH, 0.4f, 8, 44, w3));
            Every(T0, T0 + TT, 26, x =>
            {
                var c = Now(out _);
                Drop(c + new Vector2(sx * U(-0.2f, 0.5f) * tH, -U(0.5f, 1) * tH), new Vector2(U(-120, 120), -U(100, 260)), 0, U(3, 5), 900, Front,
                    c.y + U(-6, 20));
            });
            At(T0 + TT + 0.04f, () =>
            {
                Shake?.Invoke(0.75f);
                FlashScreen?.Invoke(FlashW);
                for (int i = 0; i < 18; i++) // nước chồm qua đầu rồi đổ xuống
                {
                    bool fr = U(0, 1) < 0.25f;
                    Wave(B + new Vector2(U(-50, 50), -10), new Vector2(U(-150, 150) + u.x * 120, -U(380, 640)), U(0.45f, 0.65f), 12,
                        U(20, 30) * (fr ? 0.6f : 1), fr ? Front : Back, 1, 0.4f, 1.5f, 1100, 0.72f, 0.6f);
                }
                Splash(foeFeet + new Vector2(0, -0.4f * tH), 1.1f, foeFeet.y, tH);
                for (int i = 0; i < 12; i++) // bọt tràn hai bên sát đất
                {
                    float sd = U(0, 1) < 0.5f ? -1 : 1;
                    Foam(B + new Vector2(sd * U(10, 40), U(-6, 6)), new Vector2(sd * U(120, 260), -U(0, 30)), U(0.6f, 0.9f), 6, U(11, 16),
                        U(0, 1) < 0.5f ? Front : Back);
                }
                RainBack(foeFeet, tH, 18);
                Puddle(foeFeet + new Vector2(0, 3), 26, 1.4f);
            });
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
            Every(T0 + 0.15f, T1 + 0.1f, 5, x => Crown(foeFeet + new Vector2(U(-0.6f, 0.6f) * tH, U(0, 14)), U(0.25f, 0.4f) * tH, 0.3f));
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
            Every(0.1f, T1, 16, x => Foam(Cc + new Vector2(U(-0.25f, 0.25f) * tH, U(-6, 6)), Vector2.zero, 0.4f, 3, U(6, 9), Back));
            At(0.1f, () => Shake?.Invoke(0.15f));
            At(T1, () =>
            {
                Shake?.Invoke(0.65f);
                FlashScreen?.Invoke(FlashW);
                Crown(Cc + new Vector2(0, 4), 0.85f * tH, 0.5f);
                Ripple(Cc, 0.15f * tH, 0.85f * tH);
                BurstFlash(foeFeet + new Vector2(0, -0.45f * tH), 0.6f * tH);
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
                Add(pil);
                Every(0, 0.45f, x => 60 * (1 - 0.5f * x), x =>
                {
                    bool fr = U(0, 1) < 0.25f;
                    Wave(Cc + new Vector2(U(-0.2f, 0.2f) * tH, -4), new Vector2(U(-50, 50), -U(520, 800) * (1 - 0.4f * x)), U(0.4f, 0.55f), 9,
                        U(18, 26) * (fr ? 0.6f : 1), fr ? Front : Back, 1, 0.6f, 1.4f, 900, 0.72f, 0.5f);
                });
                Every(0.1f, 0.6f, 20, x => Foam(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -U(1, 1.3f) * tH), new Vector2(U(-60, 60), -U(0, 40)), 0, 6,
                    U(11, 16), Back));
                RainBack(foeFeet, tH, 18);
                Puddle(foeFeet + new Vector2(0, 3), 24);
                WExtra(foeFeet + new Vector2(0, -0.5f * tH), 5, 320);
            });
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
            At(TA, () =>
            {
                Shake?.Invoke(0.35f);
                Crown(Cs + new Vector2(0, 4), 0.75f * tH, 0.5f);
            });
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
            Add(body);
            // sọc bọt trượt quanh mặt trước của phễu (từ phải sang trái = phễu đang quay)
            Every(TA + 0.1f, T1, 16, x =>
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
            // mào sóng văng ra ở hai mép phễu
            Every(TA + 0.12f, T1, 30, x =>
            {
                float hh = U(0.15f, 1), sd = U(0, 1) < 0.5f ? -1 : 1;
                var c = Centre(hh, T - start);
                Wave(c + new Vector2(sd * Radius(hh) * 0.9f, 0), new Vector2(sd * U(120, 240), -U(60, 200)), U(0.26f, 0.38f), 6,
                    U(11, 17) * (0.6f + 0.4f * hh), Front, 1, 0.35f, 3, 500, 0.72f, 0.25f);
            });
            // miệng phễu: bọt cuộn, giọt văng
            Every(TA + T_UP, T1 + 0.1f, 26, x =>
            {
                float a = U(0, 6.28f);
                var c = Centre(1, T - start);
                float R = Radius(1);
                Foam(c + new Vector2(R * Mathf.Cos(a), 0.3f * R * Mathf.Sin(a) + 4), new Vector2(Mathf.Cos(a) * 60, -U(10, 50)), 0, 6, U(10, 15),
                    Mathf.Sin(a) > 0 ? Front : Back);
            });
            Every(TA + T_UP, T1, 26, x => Drop(Centre(U(0.5f, 1), T - start) + new Vector2(U(-30, 30), 0),
                new Vector2((U(0, 1) < 0.5f ? -1 : 1) * U(170, 300), -U(40, 160)), 0, U(3, 5), 900, U(0, 1) < 0.5f ? Front : Back, foeFeet.y + U(-10, 24)));
            Every(TA + T_UP, T1, 4, x => WExtra(Centre(U(0.4f, 1), T - start), 1, 220));
            At(T1 + 0.15f, () => // vòi sụp: nước đổ xuống toé ra
            {
                Shake?.Invoke(0.4f);
                Splash(foeFeet + new Vector2(0, -0.3f * tH), 0.9f, foeFeet.y, tH, Back);
                RainBack(foeFeet, tH, 16, 0.6f, 0, 0.35f);
                Puddle(foeFeet + new Vector2(0, 3), 20, 1);
            });
            return di ? TA + 0.1f + 0.85f * T_DI : TA + 0.15f;
        }

        // cú va nước của chiêu lao tới (trượt, húc, liên hoàn): gọi đúng khung trúng, nước toé lớn ở thân đối thủ, cột nước, mưa giọt
        public float NVa(Vector2 foeBody, Vector2 foeFeet, float tH)
        {
            Shake?.Invoke(0.6f);
            FlashScreen?.Invoke(FlashW);
            Splash(foeBody, 1.25f, foeFeet.y, tH);
            BackColumn(foeFeet, tH);
            RainBack(foeFeet, tH, 18);
            Puddle(foeFeet + new Vector2(0, 3));
            return 0;
        }

        // ================= chọn chiêu nước =================
        public static bool IsNuoc(string kind) => kind != null && kind.StartsWith("n_");

        // chiêu chỉ phát ở khung trúng (không có pha tụ): cú va của chiêu lao tới
        public static bool NuocAtHit(string kind) => kind == "n_va" || kind == "n_la_va" || kind == "n_gai_va";

        // ult: chiêu cuối (tia dài hơn, mưa lâu hơn)
        public float PlayNuoc(string kind, bool ult, Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeFeet, Vector2 foeBody, float tH,
            float lead)
        {
            if (!HasWater) return 0;
            switch (kind)
            {
                case "n_tia": return NTia(mouth, foeBody, foeFeet, casterFeet.y, tH, lead, ult ? 1.25f : 0.88f);
                case "n_cau": return NCau(mouth, foeBody, casterFeet.y, foeFeet, tH, lead);
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
                case "n_cau_rua": return NCauMieng(casterFeet, casterH, mouth, foeFeet, foeBody, tH, lead); // Hỏa Quy, chiêu mana: tụ cầu lửa ở mõm rồi bắn
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
                "n_la" => LaDur + 0.04f,
                "n_cau_tia" => 0.88f + 0.05f,
                "n_giac_tia" => 0.88f + 0.05f,
                "n_giac_tim" => 1.0f + 0.05f,
                "n_rong_gam" => RongGamDur + 0.04f,
                _ => 0,
            };
    }
}
