// Bộ ROBOT CỔ (2026-11-16, robot hủy diệt cổ đại, suất thiet_phu ải 40 đảo Kim; rig ArtGen/Spine/robot_co_rig.py trên rig gốc monster_3613):
// dạng 1 robot_co_1 (RC_DANG=non: robot con thép mới), dạng 2 robot_co_2 (robot cổ sắt gỉ); ghi chú ArtGen/Spine/inbox/robot_co_ghichu.md.
// Người dùng: đánh thường "giơ tay phải lên, tụ 1 quả cầu năng lượng kiểu dragonball rồi bắn, tay bị giật lại"; chiêu mana "đưa 2 tay lên trời,
// xoay lòng bàn tay liên tục, tụ 1 quả cầu năng lượng to hơn rồi ném xuống đầu đối thủ, impact lớn, nặng"; chiêu cuối "mở mặt ra có lõi tên lửa
// lục giác, phóng các tên lửa bay random theo đường cong bezier kiểu homing missile vào đối thủ, impact nặng, nổ lớn"; lúc ghép vào game "làm
// thêm các fx cần thiết vì tôi chưa thấy tên lửa nào".
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc: phát lúc clip BẮT ĐẦU, `lead` = giờ trúng của clip); mốc là giây clip của rig co theo
// lead; chỗ trên rig (ổ nắm đấm, cầu to giữa hai bàn tay, hai lòng bàn tay, tâm lõi, miệng 7 ống) là bảng đo ở HatRobotBang.cs (sinh bằng
// ArtGen/Spine/robot_co_do_hat.py: đổi clip hay tỉ lệ rig thì chạy lại).
// - n_robot_ban1 / n_robot_ban (đòn thường): hạt năng lượng bị hút vào ổ nắm đấm, cầu năng lượng vàng lớn dần có hai cung điện quay, lưỡi
//   năng lượng liếm quanh, đầy thì nháy vòng; bắn: chớp ở ổ, vòng, tia văng, hơi xì ở ổ lúc tay giật lùi; cầu bay có đuôi; trúng: chớp, nổ vàng.
// - n_robot_cau1 / n_robot_cau (chiêu mana): cầu to giữa hai bàn tay giơ cao, xoáy năng lượng ở hai lòng bàn tay (bàn tay xoay) và dải hạt
//   từ lòng bàn tay cuốn vào cầu, hạt hút từ xa, sỏi dưới chân bay lên, bụi xoáy, ba nhịp vòng nạp (nhịp cuối chớp + rung); vung đập: cầu vọt
//   lên rồi cắm xuống đỉnh đầu đối thủ; nổ rất lớn: chớp, nổ vàng, cột năng lượng phụt lên, hai vòng sóng đất, nứt đất, đá văng, bụi, khói.
// - n_robot_ten1 / n_robot_ten (chiêu cuối): giáp ngực mở xì hơi hai bên, lõi nóng (than vàng bốc lên, vòng nháy); 7 TÊN LỬA vẽ rõ hình (vỏ
//   thép, mũi đỏ, đai sẫm, hai vây đuôi, lửa phụt đuôi, vệt khói xám) rời đúng ống, đúng giờ `phong` của clip, phụt lửa khói ở miệng ống, bay
//   đường cong Bézier bậc ba NGẪU NHIÊN kiểu homing (điểm lái 1 theo hướng phóng, điểm lái 2 lệch quanh đích, lắc ngang tắt dần, tăng tốc lao
//   vào) tới chỗ chạm riêng trên thân đối thủ; mỗi quả nổ lửa; sau quả cuối nổ rất lớn ba đợt, sóng đất, đá, khói; khép ngực xì hơi.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // màu: KHÔNG dùng biến tĩnh của file khác trong khởi tạo tĩnh (thứ tự khởi tạo giữa các phần partial không cố định)
        static readonly Color RbMuc = C(43, 33, 24);
        static readonly Color[] RbNang = { C(236, 138, 34), C(252, 192, 60), C(255, 232, 140), C(255, 252, 232) }; // = Pal["nang"] (HatLua.cs)
        static readonly Color[] RbChopC = { C(43, 33, 24), C(236, 138, 34), C(252, 192, 60), C(255, 232, 140), C(255, 252, 232) };
        static readonly float[] RbChopF = { 1, 1, 0.8f, 0.6f, 0.4f };
        static readonly Color RbThep = C(168, 176, 190), RbThepSam = C(78, 82, 96), RbMui = C(214, 62, 42);
        static readonly Color RbLuaNgoai = C(248, 150, 48), RbLuaTrong = C(254, 226, 120);
        static readonly Color[] RbKhoiTen = { C(250, 204, 130), C(150, 146, 146), C(184, 181, 180), C(212, 209, 206) };   // vệt khói tên lửa
        static readonly Color[] RbHoi = { C(200, 204, 210), C(220, 223, 226), C(234, 236, 238), C(246, 246, 246) };        // hơi xì
        // nổ của tên lửa: lửa đỏ cam thường (chủ đề của tướng là năng lượng vàng)
        static readonly Theme RbLuaTh = new Theme
        {
            pal = "lua", spark = C(255, 214, 120), ember = C(248, 140, 44), ring = C(240, 110, 40), ring2 = C(252, 236, 180), extra = "giap",
            extraCol = C(92, 92, 100)
        };

        sealed class RbBang
        {
            public float[] ax, ay, cx, cy, tx, ty, ux, uy, lx, ly, ox, oy, hx, hy;
        }

        static RbBang rb1, rb2;

        static RbBang RbLay(int dang) =>
            dang == 1
                ? (rb1 ??= new RbBang
                {
                    ax = Rb1ACauX, ay = Rb1ACauY, cx = Rb1CCauX, cy = Rb1CCauY, tx = Rb1CTayX, ty = Rb1CTayY, ux = Rb1CTayTX, uy = Rb1CTayTY,
                    lx = Rb1SLoiX, ly = Rb1SLoiY, ox = Rb1SOngX, oy = Rb1SOngY, hx = Rb1SHuongX, hy = Rb1SHuongY
                })
                : (rb2 ??= new RbBang
                {
                    ax = Rb2ACauX, ay = Rb2ACauY, cx = Rb2CCauX, cy = Rb2CCauY, tx = Rb2CTayX, ty = Rb2CTayY, ux = Rb2CTayTX, uy = Rb2CTayTY,
                    lx = Rb2SLoiX, ly = Rb2SLoiY, ox = Rb2SOngX, oy = Rb2SOngY, hx = Rb2SHuongX, hy = Rb2SHuongY
                });

        static Vector2 RbMau(float[] xs, float[] ys, float t)
        {
            float f = Mathf.Max(0, t) / RbDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            float w = Mathf.Clamp01(f - i);
            return new Vector2(Mathf.Lerp(xs[i], xs[j], w), Mathf.Lerp(ys[i], ys[j], w));
        }

        // ---------------------------------------------------------------- hạt dùng chung

        // QUẢ CẦU NĂNG LƯỢNG: một hạt (viền mực + bốn lớp vàng → trắng lệch nhau, xoay; hai cung điện quay ngược chiều nhau), bám tam(giờ sân), bán
        // kính rt(giờ sân); lúc bay thì kéo dài theo hướng bay
        P RbCau(Func<float, Vector2> tam, Func<float, float> rt, float life, int group = Front)
        {
            var p = new P { pos = tam(T), life = life, group = group, seed = rng.Next(4), ph = U(0, 6.28f), r0 = rt(T) };
            p.upd = (z, dt, s) =>
            {
                var np = tam(s.T);
                z.aim = (np - z.pos) / Mathf.Max(1e-4f, dt);
                z.pos = np;
                z.vel = Vector2.zero;
                z.r0 = rt(s.T);
            };
            p.draw = (z, k, buf) =>
            {
                float r = z.r0 * (1 + 0.07f * Mathf.Sin(z.age * 38 + z.ph));
                if (r < 1) return;
                float sp = z.aim.magnitude, st = 1 + Mathf.Min(0.55f, sp / 1500), va = sp > 40 ? VelAng(z.aim) : z.age * 260;
                Put(buf, z.group, 26, S("solid_" + (z.seed & 3)), RbMuc, z.pos, 2 * r + 5, st, va);
                for (int i = 0; i < 4; i++)
                {
                    float a = z.age * 9 + i * 2.1f;
                    Put(buf, z.group, 26.2f + 0.2f * i, S("blob_" + ((z.seed + i) & 3)), RbNang[i], z.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * (r * 0.06f * i),
                        2 * r * LobeF[i + 1], st, va + 31 * i);
                }
                for (int j = 0; j < 2; j++)
                {
                    float a = (j == 0 ? 1 : -1) * z.age * 520 + j * 140 + z.ph * Mathf.Rad2Deg;
                    Put(buf, z.group, 27.2f + 0.1f * j, S("arcs_" + ((z.seed + 5 * j) % 12)), RbMuc, z.pos, 2.7f * r, 1, a);
                    Put(buf, z.group, 27.25f + 0.1f * j, S("arc_" + ((z.seed + 5 * j) % 12)), RbNang[3], z.pos, 2.7f * r, 1, a);
                }
            };
            return Add(p);
        }

        // hạt năng lượng bị hút từ `tu` vào tâm đang chạy (nhanh dần), vệt sáng theo hướng bay; tới tâm thì tắt
        void RbHut(Func<float, Vector2> tam, Vector2 tu, float life, float sz, int group = Front)
        {
            float xa = Mathf.Max(10, (tam(T) - tu).magnitude);
            var p = new P { pos = tu, life = life, group = group, sz = sz, seed = rng.Next(2), col = U(0, 1) < 0.5f ? RbNang[2] : RbNang[3] };
            p.upd = (z, dt, s) =>
            {
                var d = tam(s.T) - z.pos;
                float m = d.magnitude, v = xa * (1.1f + 5f * z.age / z.life);
                if (m < v * dt + 1.5f)
                {
                    z.dead = true;
                    return;
                }
                z.vel = d / m * v;
            };
            p.draw = (z, k, buf) => Put(buf, z.group, 40, S("streakg_" + (z.seed & 1)), z.col, z.pos, z.sz * Mathf.Min(1, z.age / 0.06f),
                Mathf.Clamp(z.vel.magnitude / 90, 1.6f, 3.6f), VelAng(z.vel));
            Add(p);
        }

        void RbHutXa(Func<float, Vector2> tam, float xa, float life, float sz, int group = Front)
        {
            float a = U(0, 6.28f);
            RbHut(tam, tam(T) + new Vector2(Mathf.Cos(a), 0.85f * Mathf.Sin(a)) * xa, life, sz, group);
        }

        // lưỡi năng lượng liếm quanh cầu (tâm c, bán kính r)
        void RbLiem(Vector2 c, float r, int group = Front)
        {
            float a = U(0, 6.28f);
            var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
            var q = Flame(c + o * r * 0.55f, o * U(30, 80) + new Vector2(0, -U(30, 70)), U(0.16f, 0.26f), r * 0.3f, r * 0.5f, "tron", "nang", group, 3, -150,
                1.5f, 0, 0);
            Tongue(q, 1, 0.4f);
        }

        // xoáy năng lượng ở một lòng bàn tay đang xoay: ba cung điện quay nhanh quanh tâm; chieu: +1 / −1
        void RbXoay(Func<float, Vector2> tam, float r, float life, float chieu, int group = Front)
        {
            var p = new P { pos = tam(T), life = life, group = group, seed = rng.Next(12), sz = r, ph = chieu };
            p.upd = (z, dt, s) =>
            {
                z.pos = tam(s.T);
                z.vel = Vector2.zero;
            };
            p.draw = (z, k, buf) =>
            {
                float rr = z.sz * Mathf.Min(1, z.age / 0.15f) * (1 - SmoothStep(0.88f, 1, k)) * (1 + 0.08f * Mathf.Sin(z.age * 31));
                if (rr < 1) return;
                for (int j = 0; j < 3; j++)
                {
                    float a = z.ph * z.age * 900 + 120 * j;
                    Put(buf, z.group, 38 + 0.1f * j, S("arcs_" + ((z.seed + 4 * j) % 12)), RbMuc, z.pos, 2.4f * rr, 1, a);
                    Put(buf, z.group, 38.05f + 0.1f * j, S("arc_" + ((z.seed + 4 * j) % 12)), RbNang[2 + (j & 1)], z.pos, 2.4f * rr, 1, a);
                }
            };
            Add(p);
        }

        // chớp toé vàng (năm lớp sao nổ lồng nhau)
        void RbChop(Vector2 c, float size, int group = Front, float life = 0.14f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = rng.Next(4), sz = size };
            p.draw = (q, k, buf) =>
            {
                for (int i = 0; i < 5; i++)
                    Put(buf, q.group, 33 + 0.1f * i, S((i == 0 ? "bursts_" : "burst_") + q.seed), RbChopC[i], q.pos,
                        q.sz * (0.6f + 0.5f * EaseOut(k / 0.6f)) * RbChopF[i] + (i == 0 ? 5 : 0), 1, q.ang);
            };
            Add(p);
        }

        // vòng tròn (nhìn thẳng) quanh một điểm
        void RbVong(Vector2 c, float life, float R0, float R1, Color col) => Ring(c, life, R0, R1, col, 1f, Front, 36);

        // tia văng toả đều quanh tâm
        void RbTia(Vector2 c, float r, int n, float v0, float v1, float grav = 200)
        {
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.7f)) / n;
                var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                Spark(c + o * r, o, U(v0, v1), 0, 8, grav);
            }
        }

        // hơi xì (giáp ngực mở / khép, ổ nắm đấm sau phát bắn): cụm hơi trắng xám phụt theo dir rồi tan
        void RbHoiXi(Vector2 pos, Vector2 dir, float sc, int n = 3, int group = Front)
        {
            for (int i = 0; i < n; i++)
            {
                var q = Smoke(pos + dir * U(0, 6), dir * U(90, 170) * sc + new Vector2(U(-15, 15), -U(10, 30)), U(0.4f, 0.65f), 3 * sc, U(8, 12) * sc, group,
                    "dark", 0);
                q.stops = RbHoi;
            }
        }

        // sỏi dưới chân bị năng lượng nhấc lên, lắc lư rồi tan
        void RbSoi(Vector2 pos, float sz)
        {
            var p = new P
            {
                pos = pos, vel = new Vector2(U(-15, 15), -U(50, 110)), life = U(0.7f, 1.1f), drag = 0.6f, spin = U(-4, 4), seed = rng.Next(4), sz = sz,
                group = U(0, 1) < 0.5f ? Back : Front, ph = U(0, 6.28f)
            };
            p.upd = (z, dt, s) => z.vel.x += Mathf.Sin(z.age * 6 + z.ph) * 40 * dt;
            p.draw = (z, k, buf) => Put(buf, z.group, 45, S("rock_" + (z.seed & 3)), Color.white, z.pos,
                z.sz * Mathf.Min(1, z.age / 0.1f) * (1 - SmoothStep(0.7f, 1, k)), 1, z.ang * Mathf.Rad2Deg);
            Add(p);
        }

        // vết nứt đất sáng dưới chân đối thủ (không có vũng dung nham như Crater)
        void RbNut(Vector2 pos, float H, float life = 1.4f)
        {
            var cr = new P { pos = pos, life = life, group = Floor, seed = rng.Next(4), sz = H };
            cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_" + q.seed), Color.white, q.pos, 1.7f * q.sz * 0.42f * Mathf.Min(1, q.age / 0.12f),
                1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.3f));
            Add(cr);
        }

        // cột năng lượng phụt thẳng lên từ chân đối thủ (dur giây), bọc quanh thân: nửa sau, nửa trước
        void RbCot(Vector2 feet, float H, float dur, float manh)
        {
            Every(0, dur, 80, x =>
            {
                float w = 0.2f * H * manh * (1 - 0.5f * x);
                var q = Flame(feet + new Vector2(U(-w, w), -U(0, 0.1f) * H), new Vector2(U(-40, 40), -U(520, 900) * manh), U(0.24f, 0.38f), 0.08f * H * manh,
                    0.15f * H * manh, "tron", "nang", U(0, 1) < 0.5f ? Back : Front, 1.4f, -200, 1.6f, 0.05f, 0.05f);
                Tongue(q, 1, 0.1f);
                q.smokeGroup = Back;
            });
        }

        // ---------------------------------------------------------------- tên lửa

        // thân tên lửa vẽ theo hướng bay (aim): lửa phụt sát đuôi, hai vây đuôi sẫm, vỏ thép viền mực, đai sẫm giữa thân, mũi đỏ
        void RbVeTen(P z, float k, List<Item> buf)
        {
            float L = z.sz * Mathf.Min(1, 0.55f + z.age / 0.08f), W = 0.34f * L;
            var d = z.aim;
            var n = new Vector2(-d.y, d.x);
            float va = VelAng(d);
            int g = z.group;
            float fl = 0.8f + 0.35f * Mathf.Sin(z.age * 70 + z.seed * 1.7f), ta = TipAngle(-d);
            var duoi = z.pos - d * (0.5f * L);
            Put(buf, g, 24.6f, S("lobes_" + (z.seed & 3)), RbMuc, duoi - d * (0.45f * W * fl), 1.5f * W * fl + 4, 0.75f, ta);
            Put(buf, g, 24.7f, S("lobe_" + (z.seed & 3)), RbLuaNgoai, duoi - d * (0.45f * W * fl), 1.5f * W * fl, 0.75f, ta);
            Put(buf, g, 24.8f, S("lobe_" + ((z.seed + 1) & 3)), RbLuaTrong, duoi - d * (0.3f * W * fl), 0.9f * W * fl, 0.7f, ta);
            for (int s = -1; s <= 1; s += 2)
            {
                var fd = Unit(-d * 0.6f + n * (0.8f * s));
                var fp = z.pos - d * (0.3f * L) + n * (0.42f * W * s);
                float fa = TipAngle(fd);
                Put(buf, g, 25f, S("needles_0"), RbMuc, fp, 0.95f * W + 4, 0.6f, fa);
                Put(buf, g, 25.1f, S("needle_0"), RbThepSam, fp, 0.95f * W, 0.6f, fa);
            }
            Put(buf, g, 26f, S("solid_" + (z.seed & 3)), RbMuc, z.pos, W + 4, (L + 4) / (W + 4), va);
            Put(buf, g, 26.2f, S("blob_" + (z.seed & 3)), RbThep, z.pos, W, L / W, va);
            Put(buf, g, 26.3f, S("solid_" + ((z.seed + 2) & 3)), RbThepSam, z.pos - d * (0.12f * L), 0.95f * W, 0.32f, va);
            Put(buf, g, 26.4f, S("blob_" + ((z.seed + 1) & 3)), RbMui, z.pos + d * (0.3f * L), 0.86f * W, 1.35f, va);
        }

        // MỘT TÊN LỬA TẦM NHIỆT: rời `from` theo hướng `ax`, bay D giây theo đường cong ngẫu nhiên (Bézier bậc ba như TenNhiet), luôn tới đúng
        // `tgt`. L: dài thân (px sân)
        void RbTen(Vector2 from, Vector2 ax, Vector2 tgt, float D, float L)
        {
            float dist = Mathf.Max(60, (tgt - from).magnitude);
            // tầm vòng: không nhỏ hơn ~6 lần thân tên lửa, kể cả khi đối thủ đứng sát (vòng cung phải thấy rõ)
            float vong = Mathf.Max(dist, 6.5f * L);
            var p1 = from + ax * vong * U(0.55f, 0.95f);
            // điểm lái 2: lệch quanh đích, phần lớn phía trên (vòng lên rồi bổ xuống), đôi khi quặt ngang
            float a = U(0, 1) < 0.75f ? U(-2.8f, -0.35f) : U(-0.35f, 0.45f) + (U(0, 1) < 0.5f ? Mathf.PI : 0);
            var p2 = tgt + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * vong * U(0.35f, 0.7f);
            float ph = U(0, 6.28f), amp = U(5, 13), f = U(1.4f, 2.8f);

            Vector2 Pos(float x)
            {
                float s = x * (0.3f + 0.7f * x * x); // rời ống có tốc độ, hãm nhẹ lúc vòng, tăng tốc mạnh lúc lao vào đích
                float u = 1 - s;
                var b = u * u * u * from + 3 * u * u * s * p1 + 3 * u * s * s * p2 + s * s * s * tgt;
                var tg = Unit(3 * u * u * (p1 - from) + 6 * u * s * (p2 - p1) + 3 * s * s * (tgt - p2));
                return b + new Vector2(-tg.y, tg.x) * (amp * Mathf.Sin(ph + f * 6.28f * x) * (1 - x) * Mathf.Min(1, x * 6));
            }

            var h = new P { pos = from, life = D, group = Front, seed = rng.Next(4), sz = L, aim = ax };
            float dong = 0, khoi = 0;
            h.upd = (z, dt, s) =>
            {
                float x = Mathf.Clamp01(z.age / z.life);
                var now = Pos(x);
                z.aim = Unit(Pos(Mathf.Min(1, x + 0.015f)) - now);
                z.vel = Vector2.zero;
                z.pos = now;
                var duoi = now - z.aim * (0.55f * z.sz);
                // lửa phụt: lưỡi nhỏ, tắt nhanh (chỉ nối lửa đuôi với vệt khói, không thành chuỗi hạt)
                dong += dt * 46;
                while (dong >= 1)
                {
                    dong -= 1;
                    var q = s.Flame(duoi + s.U2(-1f, 1f), -z.aim * s.U(90, 170), s.U(0.06f, 0.1f), 0.16f * z.sz, 0.19f * z.sz, "tron", "lua", Front, 3, -40,
                        1.5f, 0, 0.01f);
                    q.sizeFn = (w, kk) => w.r1 * Mathf.Pow(1 - kk, 1.4f);
                }
                khoi += dt * 34;
                while (khoi >= 1)
                {
                    khoi -= 1;
                    var sm = s.Smoke(duoi - z.aim * (0.3f * z.sz), new Vector2(s.U(-10, 10), s.U(-24, -6)), s.U(0.55f, 0.85f), 0.16f * z.sz, s.U(0.42f, 0.55f) * z.sz,
                        Back, "dark", 0);
                    sm.stops = RbKhoiTen;
                }
            };
            h.draw = RbVeTen;
            Add(h);
        }

        // phụt ở miệng ống lúc phóng: lửa, khói xám, tia (lửa đỏ cam thường)
        void RbPhut(Vector2 m, Vector2 ax, float manh)
        {
            var th0 = Th;
            Th = RbLuaTh;
            for (int i = 0; i < 3; i++)
            {
                var f = Flame(m + ax * U(2, 6), ax * U(160, 300) + U2(-40, 40), U(0.12f, 0.2f), 4 * manh, U(8, 11) * manh, "tron", "lua", Front, 4.5f, -100,
                    1.5f, 0, 0.05f);
                Tongue(f, 1, 0.1f);
            }
            for (int i = 0; i < 2; i++)
            {
                var sm = Smoke(m - ax * U(0, 4), -ax * U(40, 90) + new Vector2(U(-30, 30), U(-10, 10)), U(0.5f, 0.8f), 5 * manh, U(12, 16) * manh, Front, "dark",
                    0);
                sm.stops = RbKhoiTen;
            }
            for (int i = 0; i < 3; i++) Spark(m, ax + U2(-0.6f, 0.6f), U(200, 340));
            Th = th0;
        }

        // nổ của một tên lửa ở chỗ chạm (cứ ba quả một quả nổ to hơn)
        void RbNoTen(Vector2 tgt, float tH, int j, float manh)
        {
            var th0 = Th;
            Th = RbLuaTh;
            bool to = j % 3 == 2;
            Shake?.Invoke(to ? 0.24f : 0.13f);
            Explode(tgt, (to ? 0.62f : 0.45f) * manh, tH);
            for (int i = 0; i < 4; i++)
            {
                float a = U(0, 6.28f);
                Spark(tgt, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f), U(240, 420));
            }
            Th = th0;
        }

        // ---------------------------------------------------------------- ba đòn

        // ĐÒN THƯỜNG: tụ cầu năng lượng ở ổ nắm đấm tay phải hình rồi bắn. dang: 1 / 2. Trả giây tới lúc cầu chạm (= lead).
        public float NRobotBan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.3f, lead), k = L0 / RbALead, T0 = T;
            var B = RbLay(dang);
            float manh = dang == 1 ? 0.85f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 O(float tc) => San(RbMau(B.ax, B.ay, tc));
            float R = Mathf.Clamp(0.1f * casterH, 9, 20) * manh;
            float tTu = RbATu * k, tBan = RbABan * k;
            float Rt(float tc) => R * (0.2f + 0.8f * Mathf.Sqrt(Mathf.Clamp01((tc - RbATu) / (RbABan - 0.08f - RbATu))));
            var tgt = foeBody + new Vector2(-dir * 0.06f * tH, -0.04f * tH);
            var S0 = O(RbABan);
            var d0 = Unit(tgt - S0);

            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - T0 - tBan) / Mathf.Max(0.04f, L0 - tBan));
                return Vector2.Lerp(S0, tgt, x * (0.75f + 0.25f * x)) + new Vector2(0, -0.05f * casterH) * Mathf.Sin(Mathf.PI * x);
            }

            Vector2 Tam(float t) => t - T0 < tBan ? O((t - T0) / k) : Bay(t);
            float Rr(float t) => t - T0 < tBan ? Rt((t - T0) / k) : R;

            // tụ: cầu lớn dần trước ổ nắm đấm, hạt năng lượng bị hút vào (dày dần), lưỡi năng lượng liếm quanh
            At(tTu, () => RbCau(Tam, Rr, L0 - tTu));
            Every(tTu, tBan - 0.05f * k, x => 22 + 30 * x, x => RbHutXa(Tam, U(2.6f, 4.6f) * R, U(0.35f, 0.5f), U(6, 8)));
            Every(tTu + 0.08f * k, L0, x => 10 + 12 * x, x => RbLiem(Tam(T), Rr(T)));
            // đầy: nháy vòng sát cầu, tia toé
            At(Mathf.Max(tTu + 0.05f, tBan - 0.1f * k), () =>
            {
                var c = Tam(T);
                RbVong(c, 0.16f, R * 0.8f, R * 1.7f, RbNang[1]);
                RbTia(c, R, 6, 160, 280, 60);
            });
            // bắn: chớp ở ổ, vòng, tia văng ngược, rung nhẹ; tay giật lùi: hơi xì ở ổ
            At(tBan, () =>
            {
                Shake?.Invoke(0.12f);
                RbChop(S0, 3.2f * R, Front, 0.1f);
                RbVong(S0, 0.18f, R, 2.4f * R, RbNang[2]);
                for (int i = 0; i < 6; i++) Spark(S0, -d0 + U2(-0.8f, 0.8f), U(200, 360));
            });
            At(tBan + 0.05f * k, () => RbHoiXi(O(RbABan + 0.05f), new Vector2(-dir, -0.3f).normalized, 0.8f * manh, 3));
            // bay: đuôi năng lượng co dần, tia
            Every(tBan, L0, 70, x =>
            {
                var q = Flame(Bay(T) - d0 * R * 0.3f + U2(-0.3f, 0.3f) * R, -d0 * U(60, 140) + U2(-30, 30), U(0.14f, 0.22f), 0.7f * R, 0.8f * R, "tron", "nang",
                    Front, 3, -60, 1.4f, 0, 0);
                q.sizeFn = (z, kk) => z.r1 * Mathf.Pow(1 - kk, 1.1f);
            });
            Every(tBan, L0, 30, x => Spark(Bay(T), -d0 + U2(-0.6f, 0.6f), U(140, 260)));
            // trúng: chớp, nổ vàng, vòng, tia
            At(L0, () =>
            {
                Shake?.Invoke(0.25f * manh);
                RbChop(tgt, 0.5f * tH * manh, Front, 0.12f);
                Explode(tgt, 0.5f * manh, tH);
                RbVong(tgt, 0.22f, 0.06f * tH, 0.42f * tH * manh, RbNang[1]);
            });
            return L0;
        }

        // CHIÊU MANA: tụ cầu to giữa hai bàn tay giơ cao (lòng bàn tay xoay), vung đập ném xuống đỉnh đầu đối thủ. Trả giây tới lúc chạm (= lead).
        public float NRobotCau(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.5f, lead), k = L0 / RbCLead, T0 = T;
            var B = RbLay(dang);
            float manh = dang == 1 ? 0.85f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            float Tc(float t) => (t - T0) / k;
            Vector2 Giu(float tc) => San(RbMau(B.cx, B.cy, tc));
            Vector2 Tay(float tc) => San(RbMau(B.tx, B.ty, tc));
            Vector2 TayT(float tc) => San(RbMau(B.ux, B.uy, tc));
            float R = Mathf.Clamp(0.21f * casterH, 18, 42) * manh;
            const float tuC = 0.30f, dayC = 1.45f;
            float roiC = RbCNem - 0.08f; // đầu cú vung đập (T_NEM của rig): cầu rời tay ở dáng cao nhất
            float Rt(float tc) => R * (0.15f + 0.85f * Mathf.Sqrt(Mathf.Clamp01((tc - tuC) / (dayC - tuC))));
            float tRoi = roiC * k, tNo = L0;
            var dau = foeBody + new Vector2(-dir * 0.04f * tH, -0.3f * tH); // đỉnh đầu đối thủ
            var S0 = Giu(roiC);
            var Cc = new Vector2(S0.x + (dau.x - S0.x) * 0.4f, Mathf.Min(S0.y, dau.y) - 0.45f * casterH);

            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - T0 - tRoi) / Mathf.Max(0.05f, tNo - tRoi));
                float s = x * (0.4f + 0.6f * x), u = 1 - s;
                return u * u * S0 + 2 * u * s * Cc + s * s * dau;
            }

            Vector2 TamCau(float t) => t - T0 < tRoi ? Giu(Tc(t)) : Bay(t);
            float RCau(float t) => t - T0 < tRoi ? Rt(Tc(t)) : R;

            // 1. tụ: cầu lớn dần giữa hai bàn tay, hạt hút từ xa (dày dần), lưỡi năng lượng liếm quanh
            At(tuC * k, () => RbCau(TamCau, RCau, tNo - tuC * k));
            Every(tuC * k, tRoi - 0.05f * k, x => 18 + 40 * x, x => RbHutXa(TamCau, U(1.7f, 2.8f) * R, U(0.4f, 0.6f), U(7, 9)));
            Every((tuC + 0.15f) * k, tNo, x => 16 + 14 * x, x => RbLiem(TamCau(T), RCau(T)));
            // 2. hai lòng bàn tay xoay liên tục: xoáy cung điện ở mỗi lòng bàn tay + dải hạt từ lòng bàn tay cuốn vào cầu
            At(0.45f * k, () =>
            {
                RbXoay(t => Tay(Tc(t)), 0.34f * R, (roiC - 0.45f) * k, 1);
                RbXoay(t => TayT(Tc(t)), 0.34f * R, (roiC - 0.45f) * k, -1);
            });
            Every(0.5f * k, tRoi - 0.04f * k, 32, x => RbHut(TamCau, (rng.Next(2) == 0 ? Tay(Tc(T)) : TayT(Tc(T))) + U2(-4, 4), U(0.3f, 0.45f), U(6, 8)));
            // 3. năng lượng nén xuống đất: sỏi bay lên, bụi xoáy quanh chân
            Every(0.55f * k, tRoi, 7, x => RbSoi(casterFeet + new Vector2(U(-0.5f, 0.5f) * casterH, U(-4, 2)), U(5, 9) * manh));
            Every(0.6f * k, tRoi, 6, x =>
            {
                float sd = rng.Next(2) == 0 ? -1 : 1;
                BuiTro(casterFeet + new Vector2(sd * U(0.1f, 0.45f) * casterH, U(-4, 2)), new Vector2(sd * U(40, 110), -U(5, 30)), U(0.5f, 0.8f), 4, U(8, 12),
                    Back);
            });
            // 4. ba nhịp nạp: vòng nở quanh cầu, tia toé; nhịp cuối (cầu đầy) chớp + rung
            float[] nhip = { 0.85f, 1.15f, dayC - 0.03f };
            for (int i = 0; i < nhip.Length; i++)
            {
                int ii = i;
                At(nhip[i] * k, () =>
                {
                    var c = TamCau(T);
                    float r = RCau(T);
                    RbVong(c, 0.2f, 0.9f * r, (1.6f + 0.25f * ii) * r, RbNang[1]);
                    RbTia(c, r, 4 + 2 * ii, 160, 300, 60);
                    if (ii == nhip.Length - 1)
                    {
                        Shake?.Invoke(0.15f);
                        RbChop(c, 2.4f * r, Front, 0.12f);
                    }
                });
            }
            // 5. vung đập: cầu rời tay (vòng, tia), vọt lên rồi cắm xuống đầu đối thủ; đuôi năng lượng, tia
            At(tRoi, () =>
            {
                Shake?.Invoke(0.2f);
                RbVong(S0, 0.22f, R, 2.2f * R, RbNang[2]);
                RbTia(S0, R, 8, 220, 380);
            });
            Every(tRoi, tNo, 70, x =>
            {
                var c = Bay(T);
                var d = Unit(Bay(T + 0.02f) - c);
                var q = Flame(c - d * R * 0.3f + U2(-0.4f, 0.4f) * R, -d * U(60, 140) + U2(-40, 40), U(0.18f, 0.28f), 0.7f * R, 0.8f * R, "tron", "nang", Front, 3,
                    -100, 1.4f, 0, 0);
                q.sizeFn = (z, kk) => z.r1 * Mathf.Pow(1 - kk, 1.1f);
            });
            Every(tRoi, tNo, 34, x =>
            {
                var c = Bay(T);
                Spark(c, -Unit(Bay(T + 0.02f) - c) + U2(-0.7f, 0.7f), U(160, 300));
            });
            // 6. chạm: chớp, nổ vàng rất lớn, cột năng lượng phụt lên, sóng đất hai đợt, nứt đất, đá văng, bụi, khói
            var tam = foeBody + new Vector2(-dir * 0.04f * tH, -0.12f * tH);
            At(tNo, () =>
            {
                Shake?.Invoke(0.6f * manh);
                RbChop(dau, 1.3f * tH * manh, Front, 0.16f);
                CauNo(tam, foeFeet, foeBody, tH, dir, 1.6f * manh);
                RbCot(foeFeet, tH, 0.35f, manh);
                Ring(foeFeet + new Vector2(0, 2), 0.5f, 0.15f * tH, 1.25f * tH * manh, RbNang[1], 0.3f);
                RbNut(foeFeet + new Vector2(0, 2), tH * manh);
                BuiDap(foeFeet, tH, 1.4f * manh, 14);
                for (int i = 0; i < 8; i++)
                    Rock(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, -6), new Vector2(U(-300, 300), -U(320, 600)), foeFeet.y + U(-4, 8), U(9, 15) * manh);
            });
            At(tNo + 0.14f, () =>
            {
                Shake?.Invoke(0.3f * manh);
                Ring(foeFeet + new Vector2(0, 2), 0.55f, 0.3f * tH, 1.7f * tH * manh, RbNang[2], 0.3f);
                Explode(tam + new Vector2(dir * U(4, 18), U(-24, 4)), 0.7f * manh, tH);
            });
            At(tNo + 0.36f, () =>
            {
                for (int i = 0; i < 6; i++) Smoke(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.05f, 0.5f) * tH), null, 0, 9, 24, Back);
                for (int i = 0; i < 8; i++) Ash(foeBody + U2(-28, 28));
            });
            return L0;
        }

        // CHIÊU CUỐI: mở giáp ngực, phóng 7 tên lửa tầm nhiệt từ lõi lục giác. Trả giây tới lúc quả đầu chạm đối thủ (= lead).
        public float NRobotTen(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.3f, lead), k = L0 / RbSLead, T0 = T;
            var B = RbLay(dang);
            float manh = dang == 1 ? 0.8f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 Loi(float tc) => San(RbMau(B.lx, B.ly, tc));
            float Lt = Mathf.Clamp(0.2f * casterH, 20, 40) * manh; // dài thân tên lửa
            int n = Mathf.Min(RbSPhong.Length, B.ox.Length);

            // 1. giáp ngực mở: hơi xì hai bên khe ngực; mở hết: vòng nháy ở lõi; lõi nóng: than vàng bốc lên tới hết loạt phóng
            At(Mathf.Max(0.02f, (RbSMo + 0.03f) * k), () =>
            {
                var c = Loi(RbSMo + 0.03f);
                Shake?.Invoke(0.08f);
                for (int s = -1; s <= 1; s += 2)
                    RbHoiXi(c + new Vector2(s * 0.07f * casterH, -0.02f * casterH), new Vector2(s, -0.25f).normalized, manh);
            });
            At(0.45f * k, () =>
            {
                var c = Loi(0.45f);
                RbVong(c, 0.22f, 0.03f * casterH, 0.13f * casterH * manh, RbNang[1]);
                RbTia(c, 0.04f * casterH, 6, 140, 260, 100);
            });
            Every(0.45f * k, (RbSPhong[n - 1] + 0.1f) * k, 14, x =>
            {
                var c = Loi((T - T0) / k);
                Ember(c + U2(-0.05f, 0.05f) * casterH, new Vector2(U(-30, 30), -U(60, 120)), U(0.4f, 0.7f), U(6, 9));
            });

            // 2. loạt phóng: mỗi quả rời đúng ống, đúng giờ `phong` của clip; quả đầu chạm đúng khung trúng
            float tCuoi = 0, bay0 = (RbSLead - RbSPhong[0]) * k;
            for (int i = 0; i < n; i++)
            {
                int j = i;
                float ts = RbSPhong[j] * k;
                var o = new Vector2(B.ox[j], B.oy[j]);
                var hh = new Vector2(B.hx[j], B.hy[j]);
                // hướng phóng: chủ yếu lên trời, toả theo chỗ ống trên lõi, hơi về phía đối thủ (y sân đi xuống)
                var ax = Unit(new Vector2(dir * (0.85f * hh.x + 0.3f), -(0.55f * hh.y + 1.1f)));
                float D = j == 0 ? bay0 : bay0 + U(0.02f, 0.24f);
                var tgt = j == n - 1 ? foeBody + new Vector2(-dir * 0.05f * tH, 0) : foeBody + new Vector2(-dir * U(0f, 0.16f) * tH, U(-0.3f, 0.2f) * tH);
                At(ts, () =>
                {
                    var m = San(o);
                    Shake?.Invoke(0.06f);
                    RbPhut(m, ax, manh);
                    RbTen(m, ax, tgt, D, Lt);
                });
                float tNo = ts + D;
                tCuoi = Mathf.Max(tCuoi, tNo);
                At(tNo, () => RbNoTen(tgt, tH, j, manh));
            }

            // 3. sau quả cuối: nổ rất lớn ba đợt (lửa đỏ cam), sóng đất, bụi, đá, khói và tro
            float tKet = tCuoi + 0.07f;
            var giua = foeBody + new Vector2(-dir * 0.05f * tH, 0);
            At(tKet, () =>
            {
                var th0 = Th;
                Th = RbLuaTh;
                CauNo(giua, foeFeet, foeBody, tH, dir, 1.55f * manh);
                Ring(foeFeet + new Vector2(0, 2), 0.5f, 0.2f * tH, 1.1f * tH * manh, RbLuaTh.ring2, 0.3f);
                BuiDap(foeFeet, tH, 1.3f * manh, 12);
                for (int i = 0; i < 6; i++)
                    Rock(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -6), new Vector2(U(-260, 260), -U(300, 560)), foeFeet.y + U(-4, 6), U(9, 14) * manh);
                Th = th0;
            });
            At(tKet + 0.12f, () =>
            {
                var th0 = Th;
                Th = RbLuaTh;
                Shake?.Invoke(0.35f * manh);
                Explode(giua + new Vector2(dir * U(6, 22), U(-30, -6)), 0.8f * manh, tH);
                Th = th0;
            });
            At(tKet + 0.24f, () =>
            {
                var th0 = Th;
                Th = RbLuaTh;
                Explode(giua + new Vector2(-dir * U(4, 18), U(4, 20)), 0.6f * manh, tH);
                Th = th0;
            });
            At(tKet + 0.4f, () =>
            {
                for (int i = 0; i < 7; i++) Smoke(foeBody + new Vector2(U(-0.32f, 0.32f) * tH, -U(0.05f, 0.55f) * tH), null, 0, 9, 26, Back);
                for (int i = 0; i < 9; i++) Ash(foeBody + U2(-30, 30));
            });

            // 4. khép ngực: hơi xì
            At(RbSDong * k, () =>
            {
                var c = Loi(RbSDong);
                for (int s = -1; s <= 1; s += 2)
                    RbHoiXi(c + new Vector2(s * 0.06f * casterH, -0.02f * casterH), new Vector2(s, -0.4f).normalized, 0.8f * manh, 2);
            });
            return L0;
        }
    }
}
