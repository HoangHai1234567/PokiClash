// Bộ THIẾT TINH (2026-11-16, tinh linh tinh thể sắt, suất bo_cap ải 1 đảo Kim; rig ArtGen/Spine/tinh_sat_rig.py (dạng 1, monster_3346) và
// tinh_sat_2_rig.py (dạng 2, monster_3347); ghi chú ArtGen/Spine/inbox/tinh_sat_ghichu.md).
// Người dùng: đánh thường "lao vào tông vào đối thủ"; chiêu mana "gọi tất cả các tinh thể sắt quanh người đâm vào đối thủ, làm các tinh thể
// bay lên trên đầu, sau đó dùng code điều khiển"; chiêu cuối "phình to cơ thể nhảy dập lên đầu đối thủ" (rung squash stretch trong rig).
// Đi đường "n_" (StageView.PreFx / AtkFx / UltFx → PlayNuoc). Màu theo Themes["bo_cap"].
// - n_sat_ban1 / n_sat_ban2 (chiêu mana, dạng 1: 8 phát / dạng 2: 10 phát): rig xếp tinh thể thành vòng cung trên đầu rồi ẨN từng viên đúng
//   mốc `ban`; lớp này sinh lại ĐÚNG ẢNH tinh thể đó (Resources/<dạng>/<dạng>_tt_<vùng>.png, cùng chỗ, cùng cỡ, cùng góc của khung ngay trước
//   lúc ẩn), cho bay đường cong tăng tốc găm vào thân đối thủ, mũi xoay theo hướng bay, vệt tia bạc; mỗi viên chạm thì chớp + dăm tinh thể;
//   viên cuối nổ to hơn. Đường bay là mã, đích cố định lúc phát chiêu.
// - n_sat_dap1 / n_sat_dap (chiêu cuối, phát lúc chạm `cham_dat`): chớp lớn, hai vòng sóng đất, VÒNG CỘT TINH THỂ trồi lên quanh đối thủ rồi
//   vỡ thành dăm, bụi, đá vụn, rung mạnh (dạng 1 bản nhẹ).
// - n_sat_tong (đòn thường, tướng lao tới): chỗ vỏ tinh thể tông vào thân đối thủ: chớp, tia bạc, dăm tinh thể, bụi dưới chân.
// Chỗ, cỡ, góc ảnh và hướng mũi từng viên lúc ẩn là số đo trên rig đã xuất (phần của chiều cao KHAI cho game, x về phía trước, y lên; độ,
// 0 = phía trước, 90 = lên): đổi clip cast hay hình thì đo lại bằng ArtGen/Spine/tinh_sat_do_hat.py 1 / 2.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // dạng 1 (tinh_sat_1, chiều cao khai 400,8): khung trúng cast = phát đầu 0,98 s
        static readonly float[] Tt1T = { 0.980f, 1.055f, 1.130f, 1.205f, 1.280f, 1.355f, 1.430f, 1.505f };
        static readonly Vector2[] Tt1P =
        {
            new Vector2(0.551f, 1.045f), new Vector2(-0.320f, 1.039f), new Vector2(-0.140f, 1.167f), new Vector2(0.609f, 0.777f),
            new Vector2(-0.407f, 0.850f), new Vector2(0.294f, 1.036f), new Vector2(-0.266f, 1.022f), new Vector2(0.107f, 1.088f),
        };
        static readonly Vector2[] Tt1S =
        {
            new Vector2(0.240f, 0.421f), new Vector2(0.315f, 0.410f), new Vector2(0.199f, 0.261f), new Vector2(0.519f, 0.310f),
            new Vector2(0.553f, 0.265f), new Vector2(0.296f, 0.101f), new Vector2(0.299f, 0.132f), new Vector2(0.398f, 0.171f),
        };
        static readonly float[] Tt1A = { -87f, -135f, -108f, -43f, -160f, 4f, 143f, -30f };
        static readonly float[] Tt1G = { -19f, -12f, -16f, -9f, -7f, -16f, -12f, -16f };
        static readonly int[] Tt1K = { 6, 2, 0, 3, 1, 5, 4, 7 };
        static readonly string[] Tt1Anh = { "bin1", "bin2", "bin3", "bin6", "bin7", "bin8", "bin9", "tail3" };

        // dạng 2 (tinh_sat_2, chiều cao khai 363,8): khung trúng cast = phát đầu 1,05 s
        static readonly float[] Tt2T = { 1.050f, 1.110f, 1.170f, 1.230f, 1.290f, 1.350f, 1.410f, 1.470f, 1.530f, 1.590f };
        static readonly Vector2[] Tt2P =
        {
            new Vector2(0.141f, 1.266f), new Vector2(-0.125f, 1.255f), new Vector2(-0.447f, 1.192f), new Vector2(0.412f, 1.333f),
            new Vector2(-0.665f, 1.068f), new Vector2(0.628f, 1.192f), new Vector2(-0.776f, 0.908f), new Vector2(0.809f, 1.000f),
            new Vector2(-0.857f, 0.712f), new Vector2(0.876f, 0.831f),
        };
        static readonly Vector2[] Tt2S =
        {
            new Vector2(0.374f, 0.222f), new Vector2(0.374f, 0.222f), new Vector2(0.275f, 0.197f), new Vector2(0.260f, 0.213f),
            new Vector2(0.281f, 0.194f), new Vector2(0.272f, 0.204f), new Vector2(0.374f, 0.151f), new Vector2(0.175f, 0.140f),
            new Vector2(0.375f, 0.152f), new Vector2(0.173f, 0.143f),
        };
        static readonly float[] Tt2A = { 11f, 13f, -155f, 15f, -156f, 14f, 178f, 27f, -179f, 35f };
        static readonly float[] Tt2G = { -18f, -16f, -12f, -23f, -9f, -21f, -5f, -16f, -2f, -9f };
        static readonly int[] Tt2K = { 2, 2, 1, 3, 1, 3, 0, 4, 0, 4 };
        static readonly string[] Tt2Anh = { "P_bc_01", "P_bc_02", "P_bc_03", "P_bc_04", "P_bc_05" };

        const float SatBay = 0.24f; // giây bay ngắn nhất của một tinh thể (mỗi viên cộng thêm 0..0,08 s)
        static readonly Color SatTim = C(167, 159, 211), SatThep = C(142, 163, 203), SatBac = C(214, 220, 236);
        static readonly Color[] SatChopC = { C(44, 42, 92), C(94, 111, 156), C(142, 163, 203), C(208, 216, 238), C(250, 250, 255) };

        // ảnh tinh thể của rig: sprite gốc ở giữa (AolaImport nhập ảnh <dạng>_tt_<vùng>.png thành sprite), nạp một lần, giữ lại
        static readonly Dictionary<string, Sprite> satAnh = new Dictionary<string, Sprite>();

        static Sprite SatSprite(string dang, string vung)
        {
            string key = dang + "_tt_" + vung;
            if (satAnh.TryGetValue(key, out var s) && s) return s;
            s = Resources.Load<Sprite>(dang + "/" + key);
            satAnh[key] = s;
            return s;
        }

        // chớp sắt nhìn thẳng (vương miện toé, viền chàm đậm, lõi trắng)
        void SatChop(Vector2 c, float size, int group = Front, float life = 0.14f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = 2 + rng.Next(2), sz = size };
            p.draw = (q, k, buf) =>
            {
                for (int i = 0; i < 5; i++)
                    Put(buf, q.group, 33 + i * 0.1f, S((i == 0 ? "crowns_" : "crown_") + q.seed), SatChopC[i], q.pos,
                        q.sz * (0.6f + 0.5f * EaseOut(k / 0.6f)) * BurstF[i] + (i == 0 ? 5 : 0), 1, q.ang);
            };
            Add(p);
        }

        // dăm tinh thể: kim tím / thép có viền mực, văng xa, rơi, xoay
        void SatDam(Vector2 pos, Vector2 vel, float sz, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = U(0.45f, 0.75f), acc = new Vector2(0, 900), drag = 1.5f, sz = sz, group = group, spin = U(-9, 9),
                ang = U(0, 6.28f), col = (rng.Next(3) == 0) ? SatThep : SatTim
            };
            p.draw = (q, k, buf) =>
            {
                float s2 = q.sz * (1 - SmoothStep(0.7f, 1, k));
                Put(buf, q.group, 44, S("needles_0"), Ink, q.pos, s2 + 4, 0.5f, q.ang * Mathf.Rad2Deg);
                Put(buf, q.group, 44.5f, S("needle_0"), q.col, q.pos, s2, 0.5f, q.ang * Mathf.Rad2Deg);
            };
            Add(p);
        }

        // một viên trúng: chớp, tia bạc, dăm tinh thể; manh: cỡ
        void SatTrung(Vector2 c, Vector2 d, float tH, float manh)
        {
            Shake?.Invoke(0.1f * manh);
            SatChop(c, 0.42f * tH * manh);
            int n = Mathf.RoundToInt(5 * manh);
            for (int i = 0; i < n; i++)
            {
                float a = U(0, 6.28f);
                var dd = (new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f) - d * 0.6f).normalized;
                Spark(c, dd, U(220, 420), U(0.18f, 0.3f), U(6, 9), 300);
            }
            for (int i = 0; i < Mathf.RoundToInt(4 * manh); i++)
            {
                float a = U(0, 6.28f);
                SatDam(c + U2(-6, 6), new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.5f) * U(160, 320) * manh, U(10, 16) * Mathf.Sqrt(manh));
            }
        }

        // MỘT TINH THỂ BAY. p0: tâm lúc rời (sân), w, h: cỡ ảnh (sân), ang0: góc ảnh lúc rời (độ UI), tip0: hướng mũi lúc rời (độ UI), flip: ảnh
        // lật ngang (tướng quay trái), tgt: chỗ găm, D: giây bay, lech: độ cong (±, phần quãng)
        void SatTinh(Sprite sp, Vector2 p0, float w, float h, float ang0, float tip0, bool flip, Vector2 tgt, float D, float lech)
        {
            float delta = ang0 - tip0;                                   // góc ảnh so với hướng mũi: giữ suốt đường bay
            var tipV = new Vector2(Mathf.Cos(tip0 * Mathf.Deg2Rad), -Mathf.Sin(tip0 * Mathf.Deg2Rad)); // hướng mũi (y sân đi xuống)
            float dist = (tgt - p0).magnitude;
            var n = new Vector2(-(tgt - p0).y, (tgt - p0).x) / Mathf.Max(1, dist);
            var c1 = p0 + tipV * (0.3f * dist) + n * (lech * dist);       // điểm lái: đi theo mũi trước rồi bẻ cong về đích
            Vector2 B(float u) => (1 - u) * (1 - u) * p0 + 2 * (1 - u) * u * c1 + u * u * tgt;
            Vector2 dB(float u) => 2 * (1 - u) * (c1 - p0) + 2 * u * (tgt - c1);
            var p = new P { pos = p0, life = D, group = Front, sz = h };
            p.upd = (q, dt, s3) =>
            {
                float k = Mathf.Clamp01(q.age / q.life);
                float u = k * k * (0.35f + 0.65f * k);                    // chậm lúc rời, lao nhanh dần
                var np = B(u);
                q.vel = dt > 1e-5f ? (np - q.pos) / dt : Vector2.zero; // Step cộng pos += vel·dt ngay sau upd: tới đúng điểm trên đường cong
                // vệt tia bạc phía sau
                if ((float)q.rng.NextDouble() < 0.55f)
                {
                    var v = dB(Mathf.Max(0.02f, u));
                    Spark(q.pos - v.normalized * (0.3f * w), -v + U2(-40, 40), U(40, 110), U(0.12f, 0.22f), U(5, 8), 0);
                }
            };
            p.draw = (q, k, buf) =>
            {
                float u = k * k * (0.35f + 0.65f * k);
                var v = dB(Mathf.Max(0.02f, u));
                float th = VelAng(v);
                float f = SmoothStep(0, 1, k / 0.3f);                    // mũi xoay dần từ hướng lúc rời sang hướng bay
                float tip = tip0 + Mathf.DeltaAngle(tip0, th) * f;
                Put(buf, q.group, 46, sp, Color.white, q.pos, h, w / Mathf.Max(1e-3f, h), tip + delta, 1, 0, flip);
            };
            Add(p);
        }

        // CHIÊU MANA: dang 1 (8 phát) / 2 (10 phát). lead: giây từ đầu clip cast tới khung trúng (= phát đầu). Trả giây tới lúc viên đầu găm.
        public float NSatBan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            bool d1 = dang == 1;
            var T = d1 ? Tt1T : Tt2T;
            var Pp = d1 ? Tt1P : Tt2P;
            var Sz = d1 ? Tt1S : Tt2S;
            var A = d1 ? Tt1A : Tt2A;
            var G = d1 ? Tt1G : Tt2G;
            var K = d1 ? Tt1K : Tt2K;
            var Anh = d1 ? Tt1Anh : Tt2Anh;
            string ma = d1 ? "tinh_sat_1" : "tinh_sat_2";
            float manh = d1 ? 0.8f : 1f;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            bool flip = dir < 0;
            float t00 = Mathf.Max(0.3f, lead) - T[0]; // giờ (tính từ lúc gọi) của giây 0 clip
            int nn = T.Length;
            float tDau = 0, tCuoi = 0;
            var giua = foeBody + new Vector2(-dir * 0.04f * tH, 0);
            for (int i = 0; i < nn; i++)
            {
                int k = i;
                float ts = Mathf.Max(0.02f, t00 + T[k]);
                float D = SatBay + U(0, 0.08f);
                // mỗi viên một chỗ găm riêng trên thân đối thủ; viên cuối vào giữa thân
                var tgt = k == nn - 1 ? giua : foeBody + new Vector2(-dir * U(0.0f, 0.12f) * tH, U(-0.26f, 0.2f) * tH);
                float lech = U(0.05f, 0.16f) * (k % 2 == 0 ? 1 : -1);
                At(ts, () =>
                {
                    var sp = SatSprite(ma, Anh[K[k]]);
                    var p0 = casterFeet + new Vector2(dir * Pp[k].x, -Pp[k].y) * casterH;
                    float w = Sz[k].x * casterH, h = Sz[k].y * casterH;
                    float ang0 = flip ? -A[k] : A[k];
                    float tip0 = flip ? 180 - G[k] : G[k];
                    if (sp) SatTinh(sp, p0, w, h, ang0, tip0, flip, tgt, D, lech);
                    // chỗ tinh thể rời: tia bạc toé nhẹ
                    for (int j = 0; j < 3; j++) Spark(p0, new Vector2(dir * U(-0.2f, 1f), U(-1f, 0.4f)), U(120, 240), U(0.15f, 0.25f), U(5, 7), 200);
                });
                float tNo = ts + D;
                if (k == 0) tDau = tNo;
                tCuoi = Mathf.Max(tCuoi, tNo);
                if (k < nn - 1)
                    At(tNo, () => SatTrung(tgt, new Vector2(dir, 0), tH, (k % 3 == 2 ? 0.95f : 0.7f) * manh));
            }
            // viên cuối tới sau mọi viên khác: nổ lớn, vòng sóng, nhiều dăm
            float tKet = tCuoi + 0.04f;
            At(tKet, () =>
            {
                SatTrung(giua, new Vector2(dir, 0), tH, 1.5f * manh);
                Shake?.Invoke(0.3f * manh);
                Ring(giua, 0.36f, 0.06f * tH, 0.62f * tH * manh, SatThep, 0.5f, Front, 32);
                for (int j = 0; j < 8; j++)
                {
                    float a = 6.28f * (j + U(0, 0.7f)) / 8;
                    SatDam(giua, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f) * U(260, 460) * manh, U(13, 20));
                }
            });
            At(tKet + 0.12f, () =>
            {
                for (int i = 0; i < 4; i++) Bui(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, U(-4, 2)), new Vector2(U(-120, 120), -U(10, 60)), 0, 4, 11, Back);
            });
            return tDau;
        }

        // một cột tinh thể trồi từ đất (đáy bám đất), bật quá cỡ, đứng, rồi vỡ thành dăm
        void SatCot(Vector2 feet, float hgt, float wd, float delay, int group)
        {
            At(delay, () =>
            {
                var p = new P { pos = feet, life = 0.55f, group = group, sz = hgt, wd = wd, col = U(0, 1) < 0.35f ? SatThep : SatTim, ang = U(-14, 14) };
                p.draw = (q, k, buf) =>
                {
                    float t = k * q.life;
                    float g = t < 0.07f ? 1.2f * EaseOut(t / 0.07f) : t < 0.13f ? 1.2f - 0.2f * (t - 0.07f) / 0.06f : 1 - SmoothStep(0.75f, 1, k);
                    float hh = q.sz * g;
                    if (hh < 2) return;
                    float a = q.ang * Mathf.Deg2Rad;
                    var c = q.pos + new Vector2(Mathf.Sin(a), -Mathf.Cos(a)) * (hh * 0.5f);
                    Put(buf, q.group, 43, S("needles_0"), Ink, c, hh + 5, (q.wd + 5) / (hh + 5), -q.ang);
                    Put(buf, q.group, 43.5f, S("needle_0"), q.col, c, hh, q.wd / hh, -q.ang);
                };
                p.onDeath = (q, s3) =>
                {
                    for (int i = 0; i < 3; i++)
                        SatDam(q.pos + new Vector2(U(-0.3f, 0.3f) * q.wd, -U(0.2f, 0.8f) * q.sz), new Vector2(U(-200, 200), -U(160, 320)), U(10, 15), q.group);
                };
                Add(p);
            });
        }

        // CHIÊU CUỐI: phát lúc chạm (`cham_dat` của skill_land). manh: 0,8 dạng 1, 1 dạng 2.
        public float NSatDap(Vector2 foeFeet, Vector2 foeBody, float tH, float manh)
        {
            Shake?.Invoke(0.6f * manh); // chớp trắng màn đã có ở impactFlash của clip skill (rig): không chớp thêm, màn bị trắng bệch
            var tam = foeFeet + new Vector2(0, -0.3f * tH);
            SatChop(tam, 0.95f * tH * manh, Front, 0.18f);
            Ring(foeFeet + new Vector2(0, 2), 0.42f, 0.1f * tH, 1.05f * tH * manh, SatThep);
            Ring(foeFeet + new Vector2(0, 2), 0.55f, 0.05f * tH, 0.7f * tH * manh, SatBac, 0.3f, Floor, 31);
            // vòng cột tinh thể quanh đối thủ: sau lưng (nhóm Sau) cao hơn, phía trước thấp hơn
            int nc = Mathf.RoundToInt(9 * manh);
            for (int i = 0; i < nc; i++)
            {
                float a = 6.28f * (i + U(-0.2f, 0.2f)) / nc;
                float rx = 0.62f * tH * manh, ry = 0.16f * tH * manh;
                var at = foeFeet + new Vector2(Mathf.Cos(a) * rx, Mathf.Sin(a) * ry);
                bool sau = Mathf.Sin(a) < 0;
                SatCot(at, U(0.45f, 0.8f) * tH * manh * (sau ? 1.1f : 0.85f), U(0.12f, 0.18f) * tH * manh, 0.03f + 0.02f * (i % 3), sau ? Back : Front);
            }
            for (int i = 0; i < Mathf.RoundToInt(12 * manh); i++)
            {
                float a = U(0, 6.28f);
                SatDam(tam + U2(-10, 10), new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.5f) * U(260, 520) * manh, U(13, 21));
            }
            for (int i = 0; i < Mathf.RoundToInt(10 * manh); i++)
            {
                float sd = (i & 1) == 0 ? -1 : 1;
                Bui(foeFeet + new Vector2(sd * U(0.05f, 0.5f) * tH * manh, U(-5, 2)), new Vector2(sd * U(160, 380) * manh, -U(10, 90)), U(0.5f, 0.8f), 5,
                    U(11, 18) * manh, (i & 2) == 0 ? Back : Front);
            }
            for (int i = 0; i < Mathf.RoundToInt(5 * manh); i++)
                Rock(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, -6), new Vector2(U(-240, 240), -U(260, 460)), foeFeet.y + U(-4, 6), U(13, 19));
            At(0.18f, () =>
            {
                Shake?.Invoke(0.25f * manh);
                SatChop(tam + new Vector2(U(-0.1f, 0.1f) * tH, -0.12f * tH), 0.5f * tH * manh);
            });
            return 0;
        }

        // ĐÒN THƯỜNG (tướng lao tới tông). lead: giây từ đầu clip attack tới khung tông.
        public float NSatTong(Vector2 casterFeet, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var c = foeBody + new Vector2(-dir * 0.26f * tH, 0.04f * tH);
            At(Mathf.Max(0.02f, lead), () =>
            {
                Shake?.Invoke(0.28f);
                SatChop(c, 0.55f * tH);
                for (int i = 0; i < 8; i++) Spark(c, new Vector2(dir * U(0.2f, 1f), U(-0.9f, 0.6f)), U(240, 460), U(0.18f, 0.3f), U(6, 9), 300);
                for (int i = 0; i < 6; i++) SatDam(c + U2(-6, 6), new Vector2(dir * U(80, 300), -U(80, 300)), U(10, 16));
                for (int i = 0; i < 3; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(foeFeet + new Vector2(sd * U(6, 0.25f * tH), U(-5, 2)), new Vector2(sd * U(100, 260), -U(10, 50)), 0, 4, 11, Back);
                }
            });
            return Mathf.Max(0.02f, lead);
        }
    }
}
