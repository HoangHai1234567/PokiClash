// Bộ THIẾT VỆ (2026-11-16, chiến binh sắt khiên giáo, suất doc_giac ải 5 đảo Kim; rig ArtGen/Spine/chien_sat_rig.py (rig gốc monster_3348),
// dạng 1 chien_sat_1, dạng 2 chien_sat_2; ghi chú ArtGen/Spine/inbox/chien_sat_ghichu.md).
// Người dùng: đánh thường "dùng giáo đâm đối thủ" (tướng lao tới); chiêu mana "ném giáo vào người đối thủ" (cây giáo là mảnh của rig trên xương
// fly_0, game lái tới đối thủ, farAim xoay theo hướng bay); chiêu cuối "dơ giáo lên triệu hồi các mũi kim sắt sau đó dậm mạnh giáo xuống đất, các
// mũi kim lao vào người đối thủ (làm animation người thôi, các mũi kim code làm)". Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc), phát lúc
// clip BẮT ĐẦU; mốc lấy theo giờ trúng `lead` của clip:
// - n_giao_dam (đòn thường): chỗ mũi giáo chạm thân đối thủ: chớp sắt, tia bạc toé theo hướng đâm, dăm thép, bụi dưới chân đối thủ.
// - n_giao_nem1 / n_giao_nem (chiêu mana): gió + tia lúc giáo rời tay (lead − 0,21 s), giáo găm: chớp, vòng sóng, dăm, rung; giáo mọc lại trong
//   tay (lead + 0,11 s): chớp nhỏ ở tay.
// - n_kim_sat1 / n_kim_sat (chiêu cuối, 7 / 11 kim): lúc giơ giáo (`trieu_hoi`, 0,42 / 1,82 lead) kim sắt hiện lần lượt thành vòng cung trên đầu,
//   mũi chĩa vào đối thủ, lơ lửng run dần; giáo dậm đất (`dam_dat`, lead − 0,30): sóng đất ở mũi giáo trước mặt, bụi, rung; `phong_kim` (lead −
//   0,24) kim lần lượt lùi lấy đà rồi lao găm vào thân đối thủ (kim đầu chạm đúng lead); mỗi kim chớp + dăm; kim cuối nổ to hơn.
// Mốc (giây từ đầu clip skill của rig 1,82 s tới trúng): trieu_hoi 0,42; dam_dat 1,52; phong_kim 1,58. Đổi clip thì sửa KIM_*.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        const float KimLead = 1.82f, KimTrieu = 0.42f, KimDam = 1.52f, KimPhong = 1.58f;
        static readonly Color GiaoThep = C(170, 174, 184), GiaoBac = C(222, 225, 232), GiaoToi = C(94, 98, 108), GiaoDo = C(191, 47, 58);

        // dăm thép: mảnh kim xám có viền mực, văng, rơi, xoay
        void GiaoDam(Vector2 pos, Vector2 vel, float sz, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = U(0.45f, 0.75f), acc = new Vector2(0, 900), drag = 1.5f, sz = sz, group = group, spin = U(-9, 9),
                ang = U(0, 6.28f), col = rng.Next(3) == 0 ? GiaoBac : GiaoThep
            };
            p.draw = (q, k, buf) =>
            {
                float s2 = q.sz * (1 - SmoothStep(0.7f, 1, k));
                Put(buf, q.group, 44, S("needles_0"), Ink, q.pos, s2 + 4, 0.5f, q.ang * Mathf.Rad2Deg);
                Put(buf, q.group, 44.5f, S("needle_0"), q.col, q.pos, s2, 0.5f, q.ang * Mathf.Rad2Deg);
            };
            Add(p);
        }

        // một cú trúng của mũi thép: chớp, tia bạc theo hướng d, dăm thép
        void GiaoTrung(Vector2 c, Vector2 d, float tH, float manh, int nTia = 6, int nDam = 4)
        {
            KmBong(c - d * 0.04f * tH, -d + new Vector2(0, -0.25f), 0.3f * tH * manh, 0.1f, KmBac);   // bông va chạm toé ngược (2026-11-18)
            SatChop(c, 0.36f * tH * manh);
            for (int i = 0; i < Mathf.RoundToInt(nTia * manh); i++)   // tia bạc bắn nhanh rồi khựng
            {
                var dd = (d * U(0.3f, 1f) + new Vector2(U(-0.6f, 0.6f), U(-0.8f, 0.5f))).normalized;
                KmTiaLua(c, dd, U(420, 740), U(6, 9), (i & 1) == 0 ? KmBac[4] : GiaoBac);
            }
            for (int i = 0; i < Mathf.RoundToInt(nDam * manh); i++)
                GiaoDam(c + U2(-6, 6), (d * U(0.2f, 0.8f) + new Vector2(U(-0.7f, 0.7f), -U(0.3f, 1f))) * U(160, 340) * manh, U(10, 16) * Mathf.Sqrt(manh));
        }

        // ĐÒN THƯỜNG: tướng lao tới đâm giáo; lead: giây từ đầu clip attack tới khung đâm trúng.
        public float NGiaoDam(Vector2 casterFeet, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var c = foeBody + new Vector2(-dir * 0.22f * tH, 0.02f * tH);
            At(Mathf.Max(0.02f, lead), () =>
            {
                Shake?.Invoke(0.24f);
                GiaoTrung(c, new Vector2(dir, 0), tH, 1f, 8, 5);
                for (int i = 0; i < 3; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(foeFeet + new Vector2(sd * U(6, 0.25f * tH), U(-5, 2)), new Vector2(sd * U(100, 260), -U(10, 50)), 0, 4, 11, Back);
                }
            });
            return Mathf.Max(0.02f, lead);
        }

        // CHIÊU MANA: ném giáo (cây giáo là mảnh của rig, game lái tới đối thủ). hand: chỗ tay ném (StageView.Muzzle). manh: 0,85 dạng 1, 1 dạng 2.
        public float NGiaoNem(Vector2 casterFeet, float casterH, Vector2 hand, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float tRoi = Mathf.Max(0.02f, lead - 0.21f), tMoc = lead + 0.11f;
            At(tRoi, () =>
            {
                for (int i = 0; i < 6; i++) Spark(hand, new Vector2(dir * U(0.4f, 1f), U(-0.5f, 0.3f)), U(220, 420), U(0.12f, 0.22f), U(5, 8), 100);
                Bui(casterFeet + new Vector2(-dir * U(4, 0.12f * casterH), U(-4, 2)), new Vector2(-dir * U(80, 180), -U(10, 40)), 0, 4, 10, Back);
            });
            var c = foeBody + new Vector2(-dir * 0.05f * tH, 0);
            At(Mathf.Max(0.02f, lead), () =>
            {
                Shake?.Invoke(0.32f * manh);
                GiaoTrung(c, new Vector2(dir, 0), tH, 1.15f * manh, 9, 7);
                Ring(c, 0.34f, 0.06f * tH, 0.58f * tH * manh, GiaoThep, 0.5f, Front, 32);
                for (int i = 0; i < 4; i++) Bui(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, U(-4, 2)), new Vector2(U(-120, 120), -U(10, 60)), 0, 4, 11, Back);
            });
            At(tMoc, () =>
            {
                SatChop(hand, 0.22f * casterH * manh, Front, 0.12f);
                for (int i = 0; i < 4; i++) Spark(hand, new Vector2(U(-1f, 1f), U(-1f, 0.2f)), U(120, 220), U(0.12f, 0.2f), U(5, 7), 150);
            });
            return Mathf.Max(0.02f, lead);
        }

        // MỘT KIM SẮT: hiện ở home (sân) lúc gọi, mũi chĩa theo `toa` (hướng xoè quạt, sân), lơ lửng run dần; tới tL (giây từ lúc hiện) lùi lấy
        // đà và xoay mũi về đích, rồi lao tới tgt, tới nơi lúc tH2 (giây từ lúc hiện) thì găm: chớp + dăm. L, W: dài, rộng kim (sân).
        // nhip: sức nhịp trúng phụ khi kim găm (0: kim đầu, cú trúng chính do StageView lo)
        void KimSat(Vector2 home, Vector2 toa, Vector2 tgt, float L, float W, float tL, float tH2, float tHFoe, float manh, bool cuoi, float nhip = 0.4f)
        {
            var aim = (tgt - home).normalized;
            float ph = U(0, 6.28f);
            var p = new P { pos = home, life = tH2, group = Front, sz = L, wd = W, home = home, aim = aim, drift = toa };
            p.upd = (q, dt, s3) =>
            {
                float t = q.age;
                Vector2 np;
                if (t < tL)
                {
                    float run = 0.02f * L * SmoothStep(0, tL, t);                       // run mạnh dần trong lúc chờ
                    np = q.home + new Vector2(0, Mathf.Sin(t * 5.2f + ph) * 0.04f * L) + run * new Vector2(Mathf.Sin(t * 61 + ph), Mathf.Cos(t * 53 + ph));
                }
                else
                {
                    float u = Mathf.Clamp01((t - tL) / Mathf.Max(0.02f, tH2 - tL));
                    var lui = q.home - q.aim * (0.18f * L);
                    np = u < 0.18f ? Vector2.Lerp(q.home, lui, EaseOut(u / 0.18f)) : Vector2.Lerp(lui, tgt, Mathf.Pow((u - 0.18f) / 0.82f, 1.6f));
                    if ((float)q.rng.NextDouble() < 0.25f)   // vệt tia sau kim (hàm gọi mỗi bước con 120 Hz: 0,25 ≈ 30 tia/giây mỗi kim, trước 0,6 vượt ngân sách)
                        Spark(q.pos - q.aim * (0.45f * L), -q.aim * U(60, 140) + U2(-30, 30), U(40, 100), U(0.1f, 0.2f), U(4, 7), 0);
                }
                q.vel = dt > 1e-5f ? (np - q.pos) / dt : Vector2.zero;
            };
            // ảnh needle_0 là giọt nhọn dựng đứng chỉ chiếm 27 % bề ngang khung ảnh: bề ngang khung = bề ngang kim muốn thấy / 0,27
            float st = W / 0.27f / Mathf.Max(1f, L);
            p.draw = (q, k, buf) =>
            {
                float t = k * q.life;
                float s = EaseOut(Mathf.Clamp01(t / 0.12f));
                float hh = q.sz * s;
                if (hh < 2) return;
                // lúc chờ mũi chĩa theo quạt; lúc lùi lấy đà (18 % đầu quãng bay) xoay dần về đích
                float uq = t < tL ? 0 : Mathf.Clamp01((t - tL) / Mathf.Max(0.02f, tH2 - tL));
                var dv = Vector2.Lerp(q.drift, q.aim, SmoothStep(0, 0.2f, uq)).normalized;
                float ang = VelAng(dv) - 90;
                Put(buf, q.group, 45, S("needles_0"), Ink, q.pos, hh * 1.07f, st * 1.12f, ang);
                Put(buf, q.group, 45.5f, S("needle_0"), GiaoThep, q.pos, hh, st, ang);
                Put(buf, q.group, 45.6f, S("needle_0"), GiaoBac, q.pos + dv * (0.12f * hh), hh * 0.55f, st * 0.45f, ang);
            };
            p.onDeath = (q, s3) =>
            {
                s3.KmNhip(nhip);
                GiaoTrung(tgt, aim, tHFoe, (cuoi ? 1.5f : 0.75f) * manh, cuoi ? 10 : 4, cuoi ? 9 : 3);
            };
            Add(p);
        }

        // CHIÊU CUỐI: n kim (7 dạng 1, 11 dạng 2). lead: giây từ đầu clip skill tới trúng (kim đầu găm). Trả giây tới lúc kim đầu găm.
        public float NKimSat(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int n, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float k = Mathf.Max(0.3f, lead) / KimLead;
            float tTrieu = KimTrieu * k, tDam = KimDam * k, tPhong = KimPhong * k, tTrung = Mathf.Max(0.3f, lead);
            float L = 0.44f * casterH * Mathf.Sqrt(manh), W = 0.064f * casterH * Mathf.Sqrt(manh); // dài, rộng kim THẤY ĐƯỢC (sân): mảnh như kim
            float tCuoi = tTrung;
            for (int i = 0; i < n; i++)
            {
                // QUẠT KIM xoè toả tròn quanh một tâm sau đầu, cao hơn đỉnh mào, mũi chĩa ra ngoài (như hào quang lưỡi kim). Hai bản trước bị chê
                // khi soi trong trận 2026-11-16: xếp ngang trên đầu mà cùng chĩa về đối thủ thì kim chồng dọc thân nhau thành dải xám như khói;
                // xếp cột dọc sau lưng thì đè lên mũ và mào.
                float f = n == 1 ? 0.5f : i / (n - 1f);
                float th = Mathf.Lerp(n > 8 ? 28f : 36f, n > 8 ? 152f : 144f, f) * Mathf.Deg2Rad; // góc quạt (độ UI, 90 = thẳng lên)
                var toa = new Vector2(Mathf.Cos(th), -Mathf.Sin(th));                       // hướng xoè (sân, y xuống)
                var home = casterFeet + new Vector2(-dir * 0.08f * casterH, -1.05f * casterH) + toa * (0.6f * casterH);
                int thu = Mathf.Abs(i - (n - 1) / 2) * 2 - (i < (n - 1) / 2 ? 1 : 0);      // hiện từ giữa quạt ra hai bên
                thu = Mathf.Clamp(thu, 0, n - 1);
                float tHien = tTrieu + 0.055f * thu;
                // chỗ găm: kim càng cao thì găm càng cao trên thân, hai cánh quạt găm hai bên
                var tgt = foeBody + new Vector2(-dir * U(0.0f, 0.08f) * tH + (f - 0.5f) * 0.16f * tH, (0.12f - 0.4f * Mathf.Sin(th)) * tH + U(-0.03f, 0.03f) * tH);
                bool cuoi = i == n / 2;
                float tBay = tPhong + 0.022f * thu;
                float tToi = (tTrung - tPhong) + tBay;                                     // kim đầu chạm đúng lead
                if (cuoi) tToi = tTrung + 0.022f * n + 0.04f;
                tCuoi = Mathf.Max(tCuoi, tToi);
                float tL = tBay - tHien, tH2 = tToi - tHien;
                At(tHien, () =>
                {
                    KimSat(home, toa, tgt, L, W, tL, tH2, tH, manh, cuoi, cuoi ? 0.8f : thu == 0 ? 0 : 0.4f);
                    SatChop(home, 0.16f * casterH * manh, Front, 0.12f);
                    for (int j = 0; j < 2; j++) Spark(home, new Vector2(U(-1f, 1f), U(-1f, 0.3f)), U(80, 180), U(0.12f, 0.2f), U(4, 6), 100);
                });
            }
            // giáo dậm đất: sóng đất ở mũi giáo trước mặt, bụi, rung
            var dat = casterFeet + new Vector2(dir * 0.62f * casterH, 2);
            At(tDam, () =>
            {
                Shake?.Invoke(0.45f * manh);
                KmChop(dat + new Vector2(0, -0.06f * casterH), 0.3f * casterH * manh, 0.07f, KmBac);
                KmCung(dat, 0.08f * casterH, 1.0f * casterH * manh, 0.42f, GiaoBac, 0.3f, Floor, 30.6f, 0.9f);   // vòng cung dẹt không viền (KR5)
                KmCung(dat, 0.04f * casterH, 0.65f * casterH * manh, 0.52f, KmBac[3], 0.3f, Floor, 31, 0.7f);
                for (int i = 0; i < Mathf.RoundToInt(8 * manh); i++)
                {
                    float sd = (i & 1) == 0 ? -1 : 1;
                    Bui(dat + new Vector2(sd * U(0.02f, 0.4f) * casterH, U(-5, 2)), new Vector2(sd * U(120, 300) * manh, -U(10, 80)), U(0.45f, 0.7f), 5,
                        U(10, 16) * manh, (i & 2) == 0 ? Back : Front);
                }
                for (int i = 0; i < Mathf.RoundToInt(4 * manh); i++)
                    Rock(dat + new Vector2(U(-0.2f, 0.2f) * casterH, -6), new Vector2(U(-200, 200), -U(220, 400)), dat.y + U(-4, 6), U(11, 16));
            });
            // kim cuối găm: rung mạnh, vòng sóng ở thân đối thủ, bụi
            At(tCuoi, () =>
            {
                Shake?.Invoke(0.35f * manh);
                Ring(foeBody, 0.38f, 0.06f * tH, 0.7f * tH * manh, GiaoThep, 0.5f, Front, 32);
                for (int i = 0; i < 5; i++) Bui(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, U(-4, 2)), new Vector2(U(-140, 140), -U(10, 70)), 0, 4, 12, Back);
            });
            return tTrung;
        }
    }
}
