// Bộ THÚ GIÁP PHÁO (2026-11-17, suất ung_thep ải 60 đảo Kim; rig ArtGen/Spine/thu_phao_rig.py trên rig gốc monster_3629): dạng 1 thu_phao_1
// (TP_DANG=non: thú non mũ hiệp sĩ tròn), dạng 2 thu_phao_2 (thú giáp bạc viền vàng mũ hiệp sĩ); ghi chú ArtGen/Spine/inbox/thu_phao_ghichu.md.
// Người dùng: đánh thường "giống skill_01, bắn 1 quả đạn sắt gây nổ"; chiêu mana "giống skill_03, bắn nhiều quả đạn pháo lên trời, các quả đó
// tách ra thành các tên lửa nhỏ homing missile tấn công mục tiêu"; chiêu cuối "gồng người, tụ 1 quả cầu năng lượng rất lớn ở họng súng rồi bắn
// vào địch, gây giật, giống skill_04_1 nhưng epic hơn và impact hơn".
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc: phát lúc clip BẮT ĐẦU, `lead` = giờ trúng của clip); mốc là giây clip của rig co theo
// lead; chỗ họng pháo + hướng nòng từng khung là bảng đo ở HatPhaoBang.cs (sinh bằng ArtGen/Spine/thu_phao_do_hat.py: đổi clip hay tỉ lệ rig
// thì chạy lại). Dùng lại hạt chung của HatRobot.cs (cầu năng lượng, hạt hút, chớp, vòng, tia, hơi xì, tên lửa Bézier, phụt miệng ống, nổ tên
// lửa) và tia sét Set() của HatRong.cs.
// - n_phao_ban1 / n_phao_ban (đòn thường): họng nháy sáng một nhịp; BẮN: chớp lửa + phụt lửa khói ở họng theo hướng nòng, vòng, tia, rung;
//   ĐẠN SẮT (quả cầu sắt sẫm viền mực, xoay) bay vòng cung từ họng xuống đối thủ, vệt khói xám; trúng: nổ lửa đỏ cam, chớp, mảnh, khói.
// - n_phao_mua1 / n_phao_mua (chiêu mana): nòng chĩa trời, xì hơi nạp; 5 phát đúng giờ `ban` của clip: mỗi quả đạn vọt lên khỏi màn (vệt
//   khói), rồi trên đầu đối thủ TÁCH thành 2 / 3 tên lửa nhỏ (chớp + vòng ở chỗ tách) bay đường cong Bézier ngẫu nhiên kiểu homing lao xuống,
//   mỗi quả nổ lửa; sau loạt cuối nổ lớn, sóng đất, khói.
// - n_phao_cau1 / n_phao_cau (chiêu cuối): GỒNG: cầu năng lượng vàng lớn dần ở họng pháo, hạt hút từ xa, lưỡi năng lượng liếm, cung điện xoáy,
//   tia sét lách tách quanh cầu, sỏi dưới chân bay lên, bụi xoáy, ba nhịp nạp (nhịp cuối chớp + rung); BẮN: chớp lớn, hai vòng sóng ở họng,
//   hơi xì giật lùi, bụi trượt dưới chân, chớp màn; cầu lao thẳng tới đối thủ (đuôi năng lượng, tia sét); trúng: chớp màn, nổ năng lượng rất
//   lớn, cột năng lượng, sóng đất, nứt đất, đá, khói; GIẬT ĐIỆN: sét đánh lách tách quanh đối thủ ~0,9 s.
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color PfSat = C(70, 72, 82), PfSatSang = C(128, 132, 144);
        static readonly Color[] PfKhoi = { C(150, 146, 146), C(170, 167, 166), C(196, 193, 190), C(222, 219, 216) };

        sealed class PfBang
        {
            public float[] amx, amy, ahx, ahy, cmx, cmy, chx, chy, smx, smy, shx, shy;
        }

        static PfBang pf1, pf2;

        static PfBang PfLay(int dang) =>
            dang == 1
                ? (pf1 ??= new PfBang
                {
                    amx = Pf1AMX, amy = Pf1AMY, ahx = Pf1AHX, ahy = Pf1AHY, cmx = Pf1CMX, cmy = Pf1CMY, chx = Pf1CHX, chy = Pf1CHY, smx = Pf1SMX,
                    smy = Pf1SMY, shx = Pf1SHX, shy = Pf1SHY
                })
                : (pf2 ??= new PfBang
                {
                    amx = Pf2AMX, amy = Pf2AMY, ahx = Pf2AHX, ahy = Pf2AHY, cmx = Pf2CMX, cmy = Pf2CMY, chx = Pf2CHX, chy = Pf2CHY, smx = Pf2SMX,
                    smy = Pf2SMY, shx = Pf2SHX, shy = Pf2SHY
                });

        static Vector2 PfMau(float[] xs, float[] ys, float t)
        {
            float f = Mathf.Max(0, t) / PfDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            float w = Mathf.Clamp01(f - i);
            return new Vector2(Mathf.Lerp(xs[i], xs[j], w), Mathf.Lerp(ys[i], ys[j], w));
        }

        // ---------------------------------------------------------------- hạt riêng

        // ĐẠN SẮT: quả cầu sắt sẫm viền mực, một mảng sắt sáng hơn lệch trên (tô phẳng, không bóng loáng), xoay; bám tam(giờ sân)
        P PfDan(Func<float, Vector2> tam, float r, float life, int group = Front)
        {
            var p = new P { pos = tam(T), life = life, group = group, seed = rng.Next(4), sz = r, ph = U(0, 360) };
            p.upd = (z, dt, s) =>
            {
                z.pos = tam(s.T);
                z.vel = Vector2.zero;
            };
            p.draw = (z, k, buf) =>
            {
                float a = z.ph + z.age * 420;
                Put(buf, z.group, 26, S("solid_" + (z.seed & 3)), RbMuc, z.pos, 2 * z.sz + 5, 1, a);
                Put(buf, z.group, 26.2f, S("blob_" + (z.seed & 3)), PfSat, z.pos, 2 * z.sz, 1, a);
                Put(buf, z.group, 26.4f, S("blob_" + ((z.seed + 1) & 3)), PfSatSang, z.pos + new Vector2(-0.28f, -0.3f) * z.sz, 0.75f * z.sz, 1, a);
            };
            return Add(p);
        }

        // vệt khói xám sau đạn / quả pháo
        void PfVet(Vector2 c, float sz)
        {
            var sm = Smoke(c + U2(-2, 2), new Vector2(U(-12, 12), U(-20, -4)), U(0.45f, 0.75f), 0.4f * sz, U(1.0f, 1.4f) * sz, Back, "dark", 0);
            sm.stops = PfKhoi;
        }

        // khói phụt ở họng pháo theo hướng nòng (đậm, to): mây khói xám nở ra rồi tan
        void PfKhoiHong(Vector2 m, Vector2 ax, float sc, int n)
        {
            for (int i = 0; i < n; i++)
            {
                var sm = Smoke(m + ax * U(2, 14) * sc, ax * U(60, 160) * sc + new Vector2(U(-40, 40), -U(20, 60)) * sc, U(0.6f, 1.0f), 6 * sc,
                    U(16, 24) * sc, Front, "dark", 0);
                sm.stops = PfKhoi;
            }
        }

        // tia sét ngắn lách tách quanh tâm c, bán kính r0 → r1
        void PfSetQuanh(Vector2 c, float r0, float r1, float day, float life = 0.12f)
        {
            float a = U(0, 6.28f);
            var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
            Set(c + o * r0, c + o * r1 + U2(-0.2f, 0.2f) * r1, day, 0.25f * (r1 - r0), life, false);
        }

        // ---------------------------------------------------------------- ba đòn

        // ĐÒN THƯỜNG: bắn một quả đạn sắt vòng cung từ họng pháo, nổ ở đối thủ. dang: 1 / 2. Trả giây tới lúc chạm (= lead).
        public float NPhaoBan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.3f, lead), k = L0 / PfALead, T0 = T;
            var B = PfLay(dang);
            float manh = dang == 1 ? 0.85f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 Huong(Vector2 v) => Unit(new Vector2(dir * v.x, -v.y));
            float tBan = PfABan * k;
            float R = Mathf.Clamp(0.07f * casterH, 7, 16) * manh;
            var S0 = San(PfMau(B.amx, B.amy, PfABan));
            var d0 = Huong(PfMau(B.ahx, B.ahy, PfABan));
            var tgt = foeBody + new Vector2(-dir * 0.05f * tH, -0.04f * tH);
            float xa = Mathf.Max(60, (tgt - S0).magnitude);
            var Cc = S0 + d0 * xa * 0.55f;                     // rời họng theo hướng nòng rồi vòng xuống đối thủ

            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - T0 - tBan) / Mathf.Max(0.05f, L0 - tBan));
                float u = 1 - x;
                return u * u * S0 + 2 * u * x * Cc + x * x * tgt;
            }

            // nạp: họng nháy sáng một nhịp, khói mỏng
            At(Mathf.Max(0.02f, tBan - 0.14f * k), () =>
            {
                var m = San(PfMau(B.amx, B.amy, PfABan - 0.14f));
                RbVong(m, 0.14f, 0.3f * R, 1.3f * R, RbNang[2]);
                RbTia(m, 0.4f * R, 4, 90, 160, 60);
            });
            // BẮN: chớp, phụt lửa + khói ở họng theo nòng, vòng, tia, rung
            At(tBan, () =>
            {
                Shake?.Invoke(0.16f * manh);
                RbChop(S0 + d0 * R, 2.8f * R, Front, 0.1f);
                RbPhut(S0, d0, 2.2f * manh);
                PfKhoiHong(S0, d0, manh, 4);
                RbVong(S0, 0.2f, R, 2.8f * R, RbNang[2]);
                for (int i = 0; i < 6; i++) Spark(S0, d0 + U2(-0.6f, 0.6f), U(220, 380));
            });
            // bay: đạn sắt xoay, vệt khói
            At(tBan, () => PfDan(Bay, R, L0 - tBan + 0.02f));
            Every(tBan + 0.02f, L0, 40, x => PfVet(Bay(T), R));
            // trúng: nổ lửa đỏ cam, chớp, mảnh sắt, khói
            At(L0, () =>
            {
                var th0 = Th;
                Th = RbLuaTh;
                Shake?.Invoke(0.3f * manh);
                RbChop(tgt, 0.5f * tH * manh, Front, 0.12f);
                Explode(tgt, 0.6f * manh, tH);
                Ring(tgt, 0.22f, 0.06f * tH, 0.45f * tH * manh, RbLuaTh.ring2, 0.6f);
                for (int i = 0; i < 6; i++)
                {
                    float a = U(0, 6.28f);
                    Spark(tgt, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f), U(240, 420));
                }
                Th = th0;
            });
            At(L0 + 0.16f, () =>
            {
                for (int i = 0; i < 3; i++) Smoke(foeBody + new Vector2(U(-0.2f, 0.2f) * tH, -U(0.05f, 0.4f) * tH), null, 0, 8, 20, Back);
            });
            return L0;
        }

        // CHIÊU MANA: nòng chĩa trời bắn liền 5 quả lên khỏi màn; trên đầu đối thủ mỗi quả tách thành tên lửa nhỏ homing lao xuống. Trả giây tới lúc
        // tên lửa đầu tiên chạm (= lead).
        public float NPhaoMua(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.6f, lead), k = L0 / PfCLead, T0 = T;
            var B = PfLay(dang);
            float manh = dang == 1 ? 0.85f : 1f;
            int tach = dang == 1 ? 2 : 3;                       // số tên lửa nhỏ mỗi quả
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 Huong(Vector2 v) => Unit(new Vector2(dir * v.x, -v.y));
            float R = Mathf.Clamp(0.055f * casterH, 6, 13) * manh;
            float Lt = Mathf.Clamp(0.12f * casterH, 12, 26) * manh; // dài thân tên lửa nhỏ
            float day = Mathf.Min(casterFeet.y, foeFeet.y) - 2.2f * Mathf.Max(casterH, tH); // trên khỏi mép trên màn
            int n = PfCBan.Length;

            // nạp: xì hơi ở họng
            At(PfCNap * k, () =>
            {
                var m = San(PfMau(B.cmx, B.cmy, PfCNap));
                RbHoiXi(m, Huong(PfMau(B.chx, B.chy, PfCNap)), 0.9f * manh, 3);
            });

            float tCuoi = L0;
            for (int i = 0; i < n; i++)
            {
                int ii = i;
                float tc = PfCBan[i], ts = tc * k;
                var S0 = San(PfMau(B.cmx, B.cmy, tc));
                var d0 = Huong(PfMau(B.chx, B.chy, tc));
                // quả pháo vọt lên: rời họng theo nòng, cong dần thẳng lên trời, ra khỏi màn
                var top = new Vector2(S0.x + dir * U(0.15f, 0.35f) * casterH, day);
                var Cc = S0 + d0 * 0.9f * casterH;
                float bayLen = 0.42f * k;

                Vector2 Len(float t)
                {
                    float x = Mathf.Clamp01((t - T0 - ts) / bayLen);
                    float s = x * (0.5f + 0.5f * x), u = 1 - s;
                    return u * u * S0 + 2 * u * s * Cc + s * s * top;
                }

                At(ts, () =>
                {
                    Shake?.Invoke(0.09f * manh);
                    RbChop(S0 + d0 * R, 2.4f * R, Front, 0.09f);
                    RbPhut(S0, d0, 1.6f * manh);
                    PfKhoiHong(S0, d0, 0.75f * manh, 2);
                    RbVong(S0, 0.16f, R, 2.4f * R, RbNang[2]);
                    PfDan(Len, R, bayLen + 0.02f);
                });
                Every(ts + 0.02f, ts + bayLen, 34, x => PfVet(Len(T), R));

                // tách trên đầu đối thủ (rơi vào mép trên màn); tên lửa nhỏ lao xuống, quả đầu chạm đúng lead, các loạt sau dồn dập
                float tTach = ts + bayLen + 0.12f * k;
                var Pt = new Vector2(foeBody.x + U(-0.55f, 0.35f) * tH - dir * 0.15f * tH * (ii - 2), foeFeet.y - U(1.7f, 2.0f) * tH);
                At(tTach, () =>
                {
                    RbChop(Pt, 2.6f * R, Front, 0.1f);
                    RbVong(Pt, 0.18f, R, 2.6f * R, RbNang[1]);
                    RbTia(Pt, R, 5, 140, 260, 200);
                });
                for (int j = 0; j < tach; j++)
                {
                    int jj = j;
                    float tNo = L0 + 0.13f * ii + 0.05f * jj + (ii == 0 && jj == 0 ? 0 : U(0, 0.04f));
                    float D = Mathf.Max(0.3f, tNo - tTach);
                    var ax = Unit(new Vector2((jj - (tach - 1) * 0.5f) * 1.1f + U(-0.3f, 0.3f), U(0.35f, 0.8f)));  // toả ra, chúc xuống (y sân đi xuống)
                    var tgt = foeBody + new Vector2(-dir * U(0f, 0.18f) * tH, U(-0.32f, 0.22f) * tH);
                    At(tTach, () => RbTen(Pt, ax, tgt, D, Lt));
                    At(tTach + D, () => RbNoTen(tgt, tH, ii * tach + jj, 0.75f * manh));
                    tCuoi = Mathf.Max(tCuoi, tTach + D);
                }
            }
            // sau loạt cuối: nổ lớn (lửa đỏ cam), sóng đất, bụi, khói
            float tKet = tCuoi + 0.06f;
            var giua = foeBody + new Vector2(-dir * 0.05f * tH, 0);
            At(tKet, () =>
            {
                var th0 = Th;
                Th = RbLuaTh;
                Shake?.Invoke(0.35f * manh);
                Explode(giua, 0.85f * manh, tH);
                Ring(foeFeet + new Vector2(0, 2), 0.45f, 0.15f * tH, 0.95f * tH * manh, RbLuaTh.ring2, 0.3f);
                BuiDap(foeFeet, tH, 1.1f * manh, 10);
                Th = th0;
            });
            At(tKet + 0.3f, () =>
            {
                for (int i = 0; i < 5; i++) Smoke(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.05f, 0.5f) * tH), null, 0, 9, 24, Back);
                for (int i = 0; i < 6; i++) Ash(foeBody + U2(-26, 26));
            });
            return L0;
        }

        // CHIÊU CUỐI: gồng tụ cầu năng lượng rất lớn ở họng pháo, bắn thẳng vào đối thủ, nổ lớn, GIẬT ĐIỆN. Trả giây tới lúc chạm (= lead).
        public float NPhaoCau(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.5f, lead), k = L0 / PfSLead, T0 = T;
            var B = PfLay(dang);
            float manh = dang == 1 ? 0.78f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 Huong(Vector2 v) => Unit(new Vector2(dir * v.x, -v.y));
            float Tc(float t) => (t - T0) / k;
            Vector2 Hong(float tc) => San(PfMau(B.smx, B.smy, tc));
            Vector2 Nong(float tc) => Huong(PfMau(B.shx, B.shy, tc));
            float R = Mathf.Clamp(0.26f * casterH, 22, 60) * manh;
            float tGong = PfSGong * k, tDay = PfSDay * k, tBan = PfSBan * k;
            float Rt(float tc) => R * (0.12f + 0.88f * Mathf.Sqrt(Mathf.Clamp01((tc - PfSGong) / (PfSDay - PfSGong))));
            var S0 = Hong(PfSBan) + Nong(PfSBan) * R * 0.85f;
            var tgt = foeBody + new Vector2(-dir * 0.04f * tH, -0.06f * tH);
            var d0 = Unit(tgt - S0);

            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - T0 - tBan) / Mathf.Max(0.05f, L0 - tBan));
                return Vector2.Lerp(S0, tgt, x * (0.55f + 0.45f * x));
            }

            Vector2 Tam(float t) => t - T0 < tBan ? Hong(Tc(t)) + Nong(Tc(t)) * Rt(Tc(t)) * 0.85f : Bay(t);
            float Rr(float t) => t - T0 < tBan ? Rt(Tc(t)) * (1 + 0.04f * Mathf.Sin((t - T0) * 40)) : R;

            // 1. gồng: cầu lớn dần ở họng, hạt hút từ xa (dày dần), lưỡi năng lượng liếm, hai xoáy cung điện quay ngược nhau quanh cầu
            At(tGong, () => RbCau(Tam, Rr, L0 - tGong));
            Every(tGong, tBan - 0.04f * k, x => 20 + 50 * x, x => RbHutXa(Tam, U(1.8f, 3.2f) * Mathf.Max(R * 0.5f, Rr(T)), U(0.4f, 0.6f), U(7, 10)));
            Every(tGong + 0.1f * k, L0, x => 14 + 18 * x, x => RbLiem(Tam(T), Rr(T)));
            At(tGong + 0.15f * k, () =>
            {
                RbXoay(t => Tam(t), 0.9f * R, tBan - tGong - 0.15f * k, 1);
                RbXoay(t => Tam(t), 0.7f * R, tBan - tGong - 0.15f * k, -1);
            });
            // tia sét lách tách quanh cầu, dày dần
            Every(tGong + 0.2f * k, tBan, x => 5 + 16 * x, x =>
            {
                float r = Rr(T);
                PfSetQuanh(Tam(T), 0.8f * r, U(1.5f, 2.3f) * r, Mathf.Clamp(0.05f * r, 2, 5), U(0.08f, 0.14f));
            });
            // năng lượng nén xuống đất: sỏi bay lên, bụi xoáy quanh chân
            Every(tGong + 0.1f * k, tBan, 8, x => RbSoi(casterFeet + new Vector2(U(-0.6f, 0.6f) * casterH, U(-4, 2)), U(5, 9) * manh));
            Every(tGong + 0.2f * k, tBan, 7, x =>
            {
                float sd = rng.Next(2) == 0 ? -1 : 1;
                BuiTro(casterFeet + new Vector2(sd * U(0.1f, 0.55f) * casterH, U(-4, 2)), new Vector2(sd * U(40, 110), -U(5, 30)), U(0.5f, 0.8f), 4,
                    U(8, 12), Back);
            });
            // ba nhịp nạp; nhịp cuối (đầy) chớp + rung + chớp màn
            float[] nhip = { PfSGong + 0.45f * (PfSDay - PfSGong), PfSGong + 0.75f * (PfSDay - PfSGong), PfSDay };
            for (int i = 0; i < nhip.Length; i++)
            {
                int ii = i;
                At(nhip[i] * k, () =>
                {
                    var c = Tam(T);
                    float r = Rr(T);
                    RbVong(c, 0.22f, 0.9f * r, (1.6f + 0.3f * ii) * r, RbNang[1]);
                    RbTia(c, r, 5 + 3 * ii, 160, 320, 60);
                    Shake?.Invoke(0.06f + 0.06f * ii);
                    if (ii == nhip.Length - 1)
                    {
                        RbChop(c, 2.2f * r, Front, 0.14f);
                        for (int j = 0; j < 4; j++) PfSetQuanh(c, 0.9f * r, U(2.0f, 2.8f) * r, Mathf.Clamp(0.06f * r, 2.5f, 6), 0.16f);
                    }
                });
            }
            // 2. BẮN: chớp lớn, hai vòng sóng ở họng, hơi xì giật lùi, bụi trượt dưới chân, chớp màn, rung
            At(tBan, () =>
            {
                var m = Hong(PfSBan);
                var ax = Nong(PfSBan);
                Shake?.Invoke(0.5f * manh);
                FlashScreen?.Invoke(FlashSet);
                RbChop(S0, 3.2f * R, Front, 0.14f);
                RbVong(S0, 0.24f, 0.8f * R, 2.6f * R, RbNang[2]);
                PfKhoiHong(m, ax, 1.3f * manh, 5);
                RbHoiXi(m, -ax, 1.4f * manh, 4);
                for (int i = 0; i < 8; i++) Spark(S0, d0 + U2(-0.9f, 0.9f), U(260, 460));
                for (int i = 0; i < 6; i++)
                    BuiTro(casterFeet + new Vector2(U(-0.4f, 0.4f) * casterH, U(-3, 2)), new Vector2(-dir * U(80, 200), -U(10, 40)), U(0.5f, 0.8f), 4,
                        U(10, 15), Back);
            });
            At(tBan + 0.08f * k, () => RbVong(S0, 0.3f, 1.2f * R, 3.6f * R, RbNang[1]));
            // bay: đuôi năng lượng to, tia, sét quấn cầu
            Every(tBan, L0, 80, x =>
            {
                var q = Flame(Bay(T) - d0 * R * 0.35f + U2(-0.35f, 0.35f) * R, -d0 * U(80, 180) + U2(-40, 40), U(0.16f, 0.26f), 0.75f * R, 0.85f * R, "tron",
                    "nang", Front, 3, -60, 1.4f, 0, 0);
                q.sizeFn = (z, kk) => z.r1 * Mathf.Pow(1 - kk, 1.1f);
            });
            Every(tBan, L0, 36, x => Spark(Bay(T), -d0 + U2(-0.7f, 0.7f), U(160, 300)));
            Every(tBan, L0, 22, x => PfSetQuanh(Bay(T), 0.8f * R, U(1.4f, 2.0f) * R, Mathf.Clamp(0.05f * R, 2, 5), 0.1f));
            // 3. trúng: chớp màn, nổ năng lượng rất lớn, cột năng lượng, sóng đất hai đợt, nứt đất, đá, khói
            At(L0, () =>
            {
                Shake?.Invoke(0.95f * manh);
                FlashScreen?.Invoke(FlashSet);
                RbChop(tgt, 1.4f * tH * manh, Front, 0.18f);
                CauNo(tgt, foeFeet, foeBody, tH, dir, 1.8f * manh);
                RbCot(foeFeet, tH, 0.4f, manh);
                Ring(foeFeet + new Vector2(0, 2), 0.5f, 0.15f * tH, 1.35f * tH * manh, RbNang[1], 0.3f);
                RbNut(foeFeet + new Vector2(0, 2), tH * manh);
                BuiDap(foeFeet, tH, 1.5f * manh, 14);
                for (int i = 0; i < 9; i++)
                    Rock(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, -6), new Vector2(U(-320, 320), -U(320, 620)), foeFeet.y + U(-4, 8), U(9, 15) * manh);
                // sét giáng thẳng vào đối thủ ngay khoảnh khắc trúng
                Set(tgt + new Vector2(U(-0.2f, 0.2f) * tH, -1.6f * tH), tgt, 0.07f * tH * manh, 0.18f * tH, 0.24f);
            });
            At(L0 + 0.14f, () =>
            {
                Shake?.Invoke(0.35f * manh);
                Ring(foeFeet + new Vector2(0, 2), 0.55f, 0.3f * tH, 1.8f * tH * manh, RbNang[2], 0.3f);
                Explode(tgt + new Vector2(dir * U(4, 18), U(-24, 4)), 0.75f * manh, tH);
            });
            // GIẬT ĐIỆN: sét đánh lách tách quanh đối thủ, tia văng, rung nhỏ dồn dập
            Every(L0 + 0.05f, L0 + 0.95f, x => 22 - 10 * x, x =>
            {
                var c = foeBody + new Vector2(U(-0.12f, 0.12f) * tH, U(-0.25f, 0.15f) * tH);
                float a = U(0, 6.28f);
                var tu = c + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(0.4f, 0.65f) * tH;
                Set(tu, c, Mathf.Clamp(0.03f * tH, 2, 6) * manh, 0.12f * tH, U(0.08f, 0.14f), false);
                if (rng.Next(3) == 0) Spark(c, new Vector2(U(-1, 1), U(-1, 0.3f)), U(160, 300));
            });
            Every(L0 + 0.1f, L0 + 0.9f, 8, x => Shake?.Invoke(0.08f));
            At(L0 + 0.4f, () =>
            {
                for (int i = 0; i < 7; i++) Smoke(foeBody + new Vector2(U(-0.32f, 0.32f) * tH, -U(0.05f, 0.55f) * tH), null, 0, 9, 26, Back);
                for (int i = 0; i < 9; i++) Ash(foeBody + U2(-30, 30));
            });
            return L0;
        }
    }
}
