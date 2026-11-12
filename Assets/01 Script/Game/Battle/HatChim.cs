// Bộ của LINH ĐIỂU (2026-11-12, chim bảo hộ rừng cánh lá đuôi đá, suất gio_loc đảo Mộc; rig ArtGen/Spine/chim_la_rig.py).
// Người dùng: "tấn công thường lao tới đâm mỏ vào đối thủ"; "chiêu mana chim đứng dọc dùng cánh quạt mạnh 1 phát, các lá lông trên
// cánh bay ra găm vào người đối thủ rồi lại quay về cánh" (lá là mảnh của RIG bay trên xương fly_*, code lái tới đúng đối thủ; lớp này
// chỉ lo luồng gió lúc quạt, chỗ lá găm, lúc lá rút ra, lúc lá về cánh); "chiêu cuối gọi ra 1 thiên thạch đá rơi từ trên trời xuống
// vào đầu đối thủ".
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes.
// Mốc của clip (chim_la_clip.py): attack: mổ = lead (0,50). cast: giơ cánh lead − 0,69, quạt + lá rời cánh lead − 0,25, lá găm = lead
// (0,95), lá rút ra lead + 0,35, lá về tới cánh lead + 0,69. skill: gồng lead − 1,68, ngửa cổ gọi lead − 0,86, đá bắt đầu rơi
// lead − 0,60, trúng đầu = lead (1,94).
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color ThachC = C(154, 150, 138), ThachC2 = C(102, 98, 90), ThachC3 = C(190, 186, 172); // xám đá của đuôi chim: giữa, sẫm, mặt sáng
        static readonly Color GioC = C(246, 250, 240); // sợi gió trắng ngà

        // tảng đá rừng: bốn khối tròn lệch nhau chung một viền mực (mọi viền nằm dưới mọi khối nên hình bóng gồ ghề liền một nét): thân
        // xám, một khối sẫm phía dưới, một khối nhạt phía trên; reu: mảng rêu lục trùm đỉnh. Xoay; có ground thì nảy một lần rồi nằm lại
        static readonly Vector3[] ThachU = { new Vector3(0, 0, 1f), new Vector3(0.5f, 0.24f, 0.66f), new Vector3(-0.52f, 0.28f, 0.6f), new Vector3(0.08f, -0.4f, 0.62f) };

        void DrawThach(P q, float k, List<Item> buf)
        {
            float r = q.sz * (1 - SmoothStep(0.72f, 1, k));
            if (r < 1.2f) return;
            int sd = q.seed & 3, g = q.group;
            float a = q.ang;
            float rad = -a * Mathf.Deg2Rad;
            Vector2 Rot(float x, float y) => new Vector2(x * Mathf.Cos(rad) - y * Mathf.Sin(rad), x * Mathf.Sin(rad) + y * Mathf.Cos(rad)) * r;
            float ink = Mathf.Min(4.5f, 2.2f + r * 0.1f);
            int n = r < 6 ? 2 : 4;
            for (int i = 0; i < n; i++)
            {
                var u = ThachU[i];
                var c = q.pos + Rot(u.x, u.y);
                float d = 2 * r * u.z;
                int si = (sd + i) & 3;
                Put(buf, g, q.ph, S("solid_" + si), Ink, c, d + ink, 1, a + i * 50);
                Put(buf, g, q.ph + 0.1f + i * 0.02f, S("blob_" + si), i == 1 ? ThachC2 : i == 3 ? ThachC3 : ThachC, c, d, 1, a + i * 50);
            }
            if (!q.crust || r < 5) return;
            var cr = q.pos + Rot(-0.04f, -0.66f);
            Put(buf, g, q.ph, S("solid_" + ((sd + 2) & 3)), Ink, cr, 0.92f * r + ink, 1.7f, a);
            Put(buf, g, q.ph + 0.3f, S("blob_" + ((sd + 2) & 3)), q.stops[1], cr, 0.92f * r, 1.7f, a);
            Put(buf, g, q.ph + 0.4f, S("blob_" + ((sd + 3) & 3)), q.stops[2], q.pos + Rot(-0.12f, -0.76f), 0.46f * r, 1.8f, a);
        }

        P Thach(Vector2 pos, Vector2 vel, float life, float r, float ground = float.NaN, int group = Front, bool reu = false)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, acc = new Vector2(0, 1300), spin = U(-420, 420), spinDrag = 0.6f, ang = U(0, 360), seed = rng.Next(8),
                sz = r, group = group, ground = ground, bounce = 0.34f, crust = reu, stops = W, ph = 44
            };
            p.draw = DrawThach;
            return Add(p);
        }

        // sợi gió: vệt trắng mảnh bay thẳng, hiện rồi tan
        P SoiGio(Vector2 pos, Vector2 vel, float life, float sz, int group = Front)
        {
            var p = new P { pos = pos, vel = vel, life = life, seed = rng.Next(2), sz = sz, group = group, col = GioC, drag = 1.2f };
            p.draw = (q, k, buf) =>
            {
                float a = 1 - Mathf.Abs(2 * k - 1);
                if (a < 0.05f) return;
                Put(buf, q.group, 38, S("streakg_" + (q.seed & 1)), q.col, q.pos, q.sz, Mathf.Clamp(q.vel.magnitude / 80, 2.4f, 5f), VelAng(q.vel),
                    Mathf.Min(1, a * 1.7f));
            };
            return Add(p);
        }

        // ĐÂM MỎ (đòn đánh thường, tướng lao tới): bụi lúc bật khỏi chỗ, sợi gió và vài chiếc lá tuột lại lúc lao, mỏ chạm: chớp toé nhỏ,
        // lá bật theo hướng đâm. Nhỏ hơn chiêu mana.
        public float NMoDam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var toi = Vector2.Lerp(casterFeet, foeFeet, 0.72f); // sân kéo đỉnh cú lao tới 72 % quãng tới đối thủ (AolaSticker.Lunge)
            float t0 = Mathf.Max(0.02f, L - 0.22f);
            At(t0, () =>
            {
                Ripple(casterFeet + new Vector2(0, 2), 0.06f * casterH, 0.36f * casterH, 0.35f, BuiC2);
                for (int i = 0; i < 6; i++)
                    Bui(casterFeet + new Vector2(U(-12, 12), U(-5, 2)), new Vector2(-dir * U(110, 260), -U(20, 90)), U(0.35f, 0.6f), 3.5f, U(8, 12), Back);
            });
            float goc = T;
            Every(t0, L, 54, x =>
            {
                float k = Mathf.Clamp01((T - goc - t0) / Mathf.Max(0.02f, L - t0));
                var at = Vector2.Lerp(casterFeet, toi, k) + new Vector2(-dir * U(0.05f, 0.4f) * casterH, -U(0.3f, 0.85f) * casterH);
                if (U(0, 1) < 0.5f) SoiGio(at, new Vector2(-dir * U(160, 300), U(-20, 20)), U(0.2f, 0.32f), U(7, 11), Back);
                else Leaf(at, new Vector2(-dir * U(70, 190), U(-80, 40)), U(0.35f, 0.55f), U(4, 6.5f), 380, 1.5f, U(0, 1) < 0.6f ? Back : Front);
            });
            At(L, () =>
            {
                Shake?.Invoke(0.3f);
                var cham = foeBody + new Vector2(-dir * 0.12f * tH, -0.12f * tH); // mũi mỏ: mặt trước của đối thủ, hơi cao
                BurstFlash(cham, 0.4f * tH);
                for (int i = 0; i < 7; i++)
                {
                    float a = dir * 1.1f + (i - 3) * 0.3f + U(-0.12f, 0.12f); // toả quanh hướng đâm (tính từ phương thẳng lên)
                    var d = new Vector2(Mathf.Sin(a), -Mathf.Cos(a));
                    Leaf(cham + d * U(5, 12), d * U(190, 340), U(0.4f, 0.65f), U(4, 6.5f), 620, 2f);
                }
                WExtra(cham, 2, 240);
            });
            return L;
        }

        // LÁ GĂM (chiêu mana): cánh quạt một phát: luồng gió và bụi thổi về phía đối thủ đúng lúc lá rời cánh; lá (mảnh của rig) găm vào
        // người đối thủ: mỗi chỗ một chớp toé nhỏ, mẩu lá và cánh hoa bật ra; lá rút ra: vụn lá bay theo về phía chim; lá về tới cánh:
        // vòng nhỏ và vài mẩu lá ở cánh.
        public float NLaGam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float tQuat = Mathf.Max(0.02f, L - 0.3f), tNem = Mathf.Max(0.04f, L - 0.25f);
            var canh = casterFeet + new Vector2(dir * 0.12f * casterH, -0.72f * casterH); // quanh hai cánh
            float xa = (foeBody - canh).magnitude;
            var hg = Unit(foeBody - canh); // hướng bắn: từ cánh tới thân đối thủ
            var ng = new Vector2(-hg.y, hg.x);
            // lấy đà: lá và bụi dưới chân bị hút lên theo cánh giơ
            if (L > 0.5f)
                Every(Mathf.Max(0.02f, L - 0.69f), tQuat, 22, x =>
                    Leaf(casterFeet + new Vector2(U(-0.4f, 0.4f) * casterH, -U(0, 0.2f) * casterH), new Vector2(U(-30, 30), -U(160, 300)), U(0.3f, 0.45f),
                        U(3.5f, 5.5f), 0, 1.2f, Back));
            // cú quạt
            At(tQuat, () =>
            {
                Shake?.Invoke(0.2f);
                Ripple(casterFeet + new Vector2(dir * 0.1f * casterH, 2), 0.1f * casterH, 0.6f * casterH, 0.4f, BuiC2);
                for (int i = 0; i < 9; i++)
                    Bui(casterFeet + new Vector2(dir * U(0, 0.35f) * casterH, U(-6, 2)), new Vector2(dir * U(160, 420), -U(10, 70)), U(0.4f, 0.7f), 4, U(9, 15),
                        Back);
            });
            Every(tQuat, tNem + 0.16f, 80, x =>
            {
                // gió và lá vụn thổi theo đúng hướng lá bay: từ cánh tới thân đối thủ (đối thủ đứng chéo lên hoặc chéo xuống)
                var at = canh + hg * U(-0.1f, 0.35f) * casterH + ng * U(-0.45f, 0.45f) * casterH;
                float v = Mathf.Max(520, xa / 0.3f) * U(0.8f, 1.25f);
                if (U(0, 1) < 0.6f) SoiGio(at, hg * v + ng * U(-30, 30), U(0.24f, 0.36f), U(8, 13), U(0, 1) < 0.5f ? Back : Front);
                else Leaf(at, hg * v * 0.7f + ng * U(-70, 70), U(0.35f, 0.55f), U(3.5f, 5.5f), 160, 1.6f, Back);
            });
            // lá găm: ba nhịp sát nhau quanh thân đối thủ
            for (int i = 0; i < 3; i++)
            {
                int ii = i;
                At(L + i * 0.045f, () =>
                {
                    if (ii == 0) Shake?.Invoke(0.45f);
                    var c = foeBody + new Vector2(-dir * U(0.02f, 0.14f) * tH, (ii - 1) * 0.2f * tH + U(-0.05f, 0.05f) * tH);
                    BurstFlash(c, (ii == 0 ? 0.42f : 0.3f) * tH);
                    for (int j = 0; j < 5; j++)
                    {
                        float a = -dir * 1.2f + (j - 2) * 0.42f + U(-0.15f, 0.15f); // bật ngược về phía chim, toả hình quạt
                        var d = new Vector2(Mathf.Sin(a), -Mathf.Cos(a));
                        Leaf(c + d * U(4, 10), d * U(160, 320), U(0.4f, 0.65f), U(3.5f, 6f), 620, 2f);
                    }
                    if (ii == 1) WExtra(c, 5, 280);
                });
            }
            At(L + 0.04f, () => Ripple(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.5f * tH));
            // lá rút ra: vụn lá và cánh hoa bị kéo theo về phía chim
            At(L + 0.35f, () =>
            {
                Shake?.Invoke(0.15f);
                for (int i = 0; i < 8; i++)
                    Leaf(foeBody + new Vector2(-dir * U(0, 0.15f) * tH, U(-0.25f, 0.25f) * tH), new Vector2(-dir * U(180, 380), U(-120, 60)), U(0.35f, 0.6f),
                        U(3f, 5f), 300, 1.6f);
                WExtra(foeBody, 2, 200);
            });
            // lá về tới cánh
            At(L + 0.69f, () =>
            {
                RingN(canh, 0.26f, 0.08f * casterH, 0.3f * casterH, W[3], 1, Front, 32);
                for (int i = 0; i < 6; i++)
                {
                    float a = U(0, 6.28f);
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Leaf(canh + d * U(8, 0.2f * casterH), d * U(60, 150) + new Vector2(0, -40), U(0.35f, 0.55f), U(3.5f, 5.5f), 320, 1.8f);
                }
            });
            return L;
        }

        // đá vỡ to: chớp toé, tảng con văng rồi nảy trên đất, dăm đá, bụi
        void ThachNo(Vector2 c, Vector2 foeFeet, float tH, float R, float dir)
        {
            BurstFlash(c, 0.7f * tH);
            for (int i = 0; i < 7; i++)
            {
                float a = (-90 + (i - 3) * 34 + U(-10, 10)) * Mathf.Deg2Rad; // nửa trên, rải đều
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                Thach(c + d * U(4, 0.4f * R), new Vector2(d.x * U(200, 420) + dir * 60, d.y * U(260, 520)), U(1.0f, 1.4f), R * U(0.22f, 0.4f), foeFeet.y + U(-10, 18),
                    (i & 1) == 0 ? Front : Back, (i % 3) == 0);
            }
            for (int i = 0; i < 12; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / 12;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f);
                DaVun(c + d * U(4, 14), d * U(220, 460), U(0.45f, 0.8f), U(3.2f, 5.6f));
            }
            for (int i = 0; i < 6; i++) Bui(c + U2(-0.5f, 0.5f) * R, U2(-90, 90) + new Vector2(0, -50), U(0.5f, 0.8f), 6, U(14, 22), i < 4 ? Back : Front);
        }

        // THIÊN THẠCH ĐÁ (chiêu cuối): chim gồng: lá và gió quanh người cuốn lên; ngửa cổ gọi: chớp ở mỏ, một chùm lá bay vút lên trời;
        // trên cao phía đối thủ lá xoáy tụ lại; tảng đá phủ rêu rơi chéo xuống, kéo đuôi bụi, dăm đá, lá, sợi gió, bóng báo trước lớn dần
        // dưới chân đối thủ; trúng ĐẦU: đá vỡ thành tảng con nảy trên đất, bụi lan hai bên, lá và cánh hoa rơi lả tả. manh: dạng 1 nhỏ hơn.
        public float NThachRoi(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh = 1)
        {
            float L = Mathf.Max(0.8f, lead);
            float tTu = Mathf.Max(0.02f, L - 1.68f), tGoi = Mathf.Max(0.06f, L - 0.86f), tRoi = L - 0.60f;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float R = Mathf.Clamp(0.25f * tH, 24, 44) * manh; // bán kính khối chính của tảng đá (cả tảng rộng chừng 2,6 R)
            var dau = foeFeet + new Vector2(0, -0.9f * tH); // đỉnh đầu đối thủ
            var dich = dau + new Vector2(0, -0.5f * R);
            // Sân chỉ cao vài trăm đơn vị và đối thủ phía trên đứng sát mép trên (đầu cách mép ~100): không có chỗ cho đá rơi một quãng
            // dài. Đá hiện NHỎ ở trên cao trong sân (như còn rất xa), vừa rơi chéo xuống đầu vừa LỚN dần tới cỡ thật: nhìn ra đá từ trời
            // lao xuống mà cả đường rơi nằm trong sân, không lẩn sau bảng tên.
            float roi = Mathf.Clamp(dich.y - 30, 40, 300); // quãng rơi theo chiều đứng, điểm hiện không cao quá mép trên sân
            var nguon = dich + new Vector2(-dir * (110 + 0.25f * roi), -roi);
            var mo = casterFeet + new Vector2(dir * 0.2f * casterH, -0.95f * casterH); // mỏ lúc ngửa cổ
            float TI = L - tRoi;
            Vector2 Path(float t) => Vector2.Lerp(nguon, dich, Mathf.Pow(Mathf.Clamp01(t / TI), 1.5f));
            float Co(float t) => 0.2f + 0.8f * Mathf.Pow(Mathf.Clamp01(t / TI), 1.7f); // cỡ so với cỡ thật
            var hb = Unit(dich - nguon); // hướng bay

            // gồng: lá và sợi gió cuốn lên quanh người, bụi dưới chân
            At(tTu, () => Ripple(casterFeet + new Vector2(0, 2), 0.12f * casterH, 0.6f * casterH, 0.45f));
            Every(tTu, tGoi, x => 26 + 30 * x, x =>
            {
                float a = U(0, 6.28f);
                var at = casterFeet + new Vector2(Mathf.Cos(a) * U(0.25f, 0.6f) * casterH, -U(0, 0.25f) * casterH);
                if (U(0, 1) < 0.4f) SoiGio(at, new Vector2(-Mathf.Sin(a) * 60, -U(260, 420)), U(0.3f, 0.45f), U(7, 11), Mathf.Sin(a) < 0 ? Back : Front);
                else Leaf(at, new Vector2(-Mathf.Sin(a) * 90, -U(200, 360)), U(0.4f, 0.6f), U(4, 6.5f), -60, 1.2f, Mathf.Sin(a) < 0 ? Back : Front);
            });
            Every(tTu, tGoi, 8, x => Bui(casterFeet + new Vector2(U(-0.45f, 0.45f) * casterH, U(-4, 2)), new Vector2(U(-40, 40), -U(60, 140)), 0, 3, 9, Back));
            // gọi: chớp ở mỏ, chùm lá vút lên trời
            At(tGoi, () =>
            {
                Shake?.Invoke(0.25f);
                BurstFlash(mo, 0.36f * casterH, Back);
                RingN(mo, 0.3f, 0.06f * casterH, 0.42f * casterH, W[3], 1, Front, 32);
                for (int i = 0; i < 12; i++)
                    Leaf(mo + U2(-10, 10), new Vector2(dir * U(40, 200) + U(-60, 60), -U(620, 980)), U(0.4f, 0.6f), U(4, 6.5f), 0, 0.4f, i < 6 ? Back : Front);
                WExtra(mo, 3, 220);
            });
            // trên trời phía đối thủ: lá xoáy tụ về chỗ đá sắp hiện (ngay mép trên sân)
            if (tRoi - tGoi > 0.08f)
            {
                var tren = nguon; // chỗ đá hiện
                Every(tGoi + 0.05f, tRoi + 0.08f, 44, x =>
                {
                    float a = U(0, 6.28f);
                    var q = Leaf(tren + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.6f) * U(40, 80), Vector2.zero, U(0.22f, 0.3f), U(3, 4.5f), 0, 0, Back);
                    q.vel = (tren - q.pos) / q.life + new Vector2(-Mathf.Sin(a), Mathf.Cos(a)) * 160;
                });
            }
            // bóng báo trước dưới chân đối thủ
            At(tRoi, () =>
            {
                var bong = new P { pos = foeFeet + new Vector2(0, 2), life = TI, group = Floor, sz = R };
                bong.draw = (q, k, buf) => Put(buf, Floor, 1, S("ell"), C(52, 62, 48), q.pos, 1.5f * q.sz * (0.3f + 0.7f * k), 3, 0, 0.16f + 0.3f * k);
                Add(bong);
                // tảng đá
                float t0 = T;
                var da = new P { pos = nguon, life = TI, seed = rng.Next(4), sz = R, group = Front, crust = true, stops = W, spin = -dir * 150, ph = 44 };
                da.upd = (q, dt, s) =>
                {
                    q.pos = Path(s.T - t0);
                    q.vel = Vector2.zero;
                };
                da.draw = (q, k, buf) =>
                {
                    float co = Co(k * TI);
                    q.sz = R * co;
                    DrawThach(q, 0, buf); // k = 0: tảng chính không thu nhỏ theo tuổi
                    // ba chiếc lá dính trên rêu, ngả về sau theo gió
                    for (int j = 0; j < 3; j++)
                    {
                        float rad = -(q.ang + j * 46 - 46) * Mathf.Deg2Rad;
                        var lp = q.pos + new Vector2(Mathf.Sin(rad), -Mathf.Cos(rad)) * q.sz * 1.15f - hb * q.sz * 0.3f;
                        float la = VelAng(-hb) + Mathf.Sin(k * 40 + j * 2) * 14;
                        float ls = Mathf.Max(6, q.sz * 0.7f);
                        Put(buf, q.group, 43.2f, LeafS(j, true), Ink, lp, ls + 3.5f, 0.6f, la);
                        Put(buf, q.group, 43.5f, LeafS(j, false), q.stops[j == 1 ? 2 : 1], lp, ls, 0.56f, la);
                    }
                };
                Add(da);
                // đuôi: bụi, dăm đá, lá tuột, sợi gió; lớn dần theo tảng đá
                Every(0.02f, TI, 46, x =>
                {
                    float r = R * Co(T - t0);
                    Bui(Path(T - t0) - hb * r * 0.8f + U2(-0.5f, 0.5f) * r, -hb * U(40, 120) + U2(-40, 40), U(0.4f, 0.6f), 0.3f * r, U(0.55f, 0.8f) * r, Back);
                });
                Every(0.04f, TI, 26, x =>
                {
                    float co = Co(T - t0);
                    Leaf(Path(T - t0) + U2(-0.8f, 0.8f) * R * co, -hb * U(60, 200) + U2(-110, 110), U(0.4f, 0.65f), U(4, 7) * (0.4f + 0.6f * co), 200, 1.2f, Back);
                });
                Every(0.04f, TI, 14, x =>
                {
                    float co = Co(T - t0);
                    DaVun(Path(T - t0) + U2(-0.7f, 0.7f) * R * co, -hb * U(40, 160) + U2(-130, 130), U(0.35f, 0.55f), U(2.6f, 4.2f) * (0.4f + 0.6f * co), Back);
                });
                Every(0.02f, TI, 30, x =>
                {
                    float co = Co(T - t0);
                    SoiGio(Path(T - t0) - hb * R * co + U2(-0.9f, 0.9f) * R * co, -hb * U(220, 380), U(0.2f, 0.3f), U(8, 13) * (0.4f + 0.6f * co), Back);
                });
            });
            // trúng đầu
            At(L, () =>
            {
                Shake?.Invoke(1f);
                ThachNo(dau, foeFeet, tH, R, dir);
                LaNo(dau + new Vector2(0, 0.1f * tH), foeFeet, tH, 1.3f);
                WExtra(dau, 9, 360);
                RingN(dau + new Vector2(0, 0.15f * tH), 0.3f, 0.14f * tH, 0.7f * tH, W[3], 1, Front, 32);
            });
            // sóng dội xuống đất: vòng bụi, bụi lan hai bên
            At(L + 0.07f, () =>
            {
                Ripple(foeFeet + new Vector2(0, 2), 0.2f * tH, 1.1f * tH, 0.5f, BuiC2);
                for (int i = 0; i < 14; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(foeFeet + new Vector2(sd * U(8, 0.3f * tH), U(-6, 3)), new Vector2(sd * U(140, 380), -U(10, 70)), U(0.55f, 0.9f), 5, U(12, 20), Back);
                }
                BurstFlash(foeBody + new Vector2(0, -0.1f * tH), 0.4f * tH);
            });
            // lá và cánh hoa rơi lả tả sau cú nổ
            Every(L + 0.06f, L + 0.6f, 30, x =>
                Leaf(dau + new Vector2(U(-0.6f, 0.6f) * tH, -U(-0.1f, 0.5f) * tH), new Vector2(U(-50, 50), U(20, 90)), U(0.55f, 0.85f), U(4, 6.5f), 240, 1.2f,
                    U(0, 1) < 0.5f ? Back : Front));
            Every(L + 0.1f, L + 0.5f, 6, x => WExtra(dau + new Vector2(U(-0.4f, 0.4f) * tH, U(-0.1f, 0.3f) * tH), 1, 120));
            return L;
        }
    }
}
