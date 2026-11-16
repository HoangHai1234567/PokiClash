// Bộ SÓI GIÁP (2026-11-16, sói chiến binh mặc giáp sắt, khiên sắt + búa sắt, suất chien_than ải 30 đảo Kim; rig ArtGen/Spine/soi_giap_rig.py
// (rig gốc monster_3428): dạng 1 sói con soi_giap_1 (SG_DANG=non), dạng 2 soi_giap_2; ghi chú ArtGen/Spine/inbox/soi_giap_ghichu.md).
// Người dùng: đánh thường "lao lên dùng búa gõ đối thủ" (tướng lao tới); chiêu mana "ném búa vào đối thủ" (búa bay là mảnh của rig trên xương
// fly_0, game lái tới thân đối thủ rồi búa quay về tay); chiêu cuối "vào tư thế che khiên, sau đó charge nhanh xé gió tới đối thủ húc mạnh, tạo
// thêm fx" (rig khai lunge cho skill). Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc), phát lúc clip BẮT ĐẦU; mốc là giây clip của rig, co
// theo `lead` (giờ trúng của clip):
// - n_soi_go (đòn thường): bụi lúc bật đi; vệt búa bổ từ trên đầu xuống; búa nện: chớp sắt, tia, dăm thép, sóng đất, bụi, sỏi.
// - n_soi_nem1 / n_soi_nem (chiêu mana): bụi lúc vung; tia lúc búa rời tay; búa bay XOÁY: vệt gió + cung gió quanh búa theo đúng đường bay
//   (bảng số đo của rig, về cả lượt đi lẫn lượt về); búa trúng: chớp, tia, dăm, vòng sóng, rung; búa nảy ra; búa về tay: chớp nhỏ.
// - n_soi_huc1 / n_soi_huc (chiêu cuối): che khiên: chớp ở khiên, bụi; tụ lực: sợi gió HÚT VÀO tướng, bụi xoáy vào chân, sỏi run nảy, khiên
//   loé, vòng gió co lại; bật lao: bụi tung sau chân, vòng đất; lao: sợi gió xé ngược dọc thân, NÓN GIÓ (cung gió) trước mép khiên, bụi kéo
//   vệt; húc: chớp lớn, tia, dăm, vòng sóng kép, gió toạc ra sau lưng đối thủ, sóng đất, bụi, sỏi, rung mạnh.
// Điểm trên rig (đo bằng ArtGen/Spine/mo_xe/atomik_dang.py, phần của chiều cao KHAI cho game, x về phía trước, y lên): đổi clip thì đo lại.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        const float SgDt = 1f / 30f;
        const float SgALead = 0.467f, SgAVung = 0.17f;
        const float SgCLead = 0.70f, SgCVung = 0.24f, SgCNem = 0.50f, SgCNay = 0.77f, SgCBat = 1.12f;
        const float SgSLead = 1.343f, SgSChe = 0.05f, SgSTu = 0.45f, SgSTu1 = 1.05f, SgSLao = 1.17f, SgSHuc = 1.333f;
        static readonly Color SgThep = C(170, 174, 184), SgBac = C(225, 228, 235), SgGio = C(242, 245, 248);

        // búa bay (cast 0,50 → 1,133 s, mỗi 1/30 s): tâm búa = chân + phần riêng (X, Y) + W × (thân đối thủ − chân) (xương fly_0 mang W phần
        // quãng tới far, game dời far tới thân đối thủ). Góc búa (độ, rig y lên) để cung gió xoay theo búa.
        static readonly float[] SgBuaX = { 0.642f, 0.590f, 0.622f, 0.456f, 0.160f, 0.032f, 0.072f, 0.110f, 0.127f, 0.112f, 0.052f, -0.011f, -0.025f, 0.041f, 0.171f, 0.317f, 0.416f, 0.432f, 0.372f, 0.14f };
        static readonly float[] SgBuaY = { 0.767f, 0.816f, 0.649f, 0.359f, 0.236f, 0.249f, 0.105f, 0.064f, 0.012f, -0.054f, -0.040f, 0.096f, 0.328f, 0.588f, 0.801f, 0.924f, 0.960f, 0.949f, 0.942f, 0.40f };
        static readonly float[] SgBuaW = { 0f, 0.167f, 0.333f, 0.5f, 0.667f, 0.833f, 1f, 1f, 1f, 0.99f, 0.934f, 0.838f, 0.714f, 0.573f, 0.427f, 0.286f, 0.162f, 0.066f, 0.01f, 0f };
        static readonly float[] SgBuaA = { 60, -23, -107, 170, 87, 3, -80, -105, -130, -167, 148, 103, 58, 13, -33, -78, -123, -168, 147, 120 };
        // chiêu cuối: quãng thân đã đi / quãng đỉnh (xương move), 0,90 → 1,50 s mỗi 1/30 s (lùi lấy đà rồi lao, đỉnh ở 1,333)
        static readonly float[] SgLao = { 0f, -0.004f, -0.035f, -0.058f, -0.073f, -0.081f, -0.084f, -0.081f, -0.064f, -0.011f, 0.098f, 0.287f, 0.58f, 1.004f, 1.004f, 0.964f, 0.929f, 0.91f, 0.903f };
        // đầu búa lúc nện (so chân lúc đỉnh lao; sói con 0,57 / 0,12, sói lớn 0,62 / 0,05: đòn thường chỉ có một mã cho cả hai dạng)
        static readonly Vector2 SgDauBua = new Vector2(0.6f, 0.08f);
        // dạng 1 (sói con) / dạng 2: mép trước + tâm khiên lúc lao, tâm khiên lúc che
        static readonly Vector2[] SgKhienLao = { new Vector2(0.55f, 0.16f), new Vector2(0.58f, 0.32f) };
        static readonly Vector2[] SgKhienChe = { new Vector2(0.10f, 0.42f), new Vector2(0.12f, 0.36f) };

        static float SgBang(float[] a, float u)
        {
            u = Mathf.Clamp(u, 0, a.Length - 1.001f);
            int i = (int)u;
            return Mathf.Lerp(a[i], a[i + 1], u - i);
        }

        // cung gió: cung tròn mảnh (hat_arc_0) quay bụng về hướng d, nở rồi tan; màu gió trắng
        void SgCung(Vector2 c, Vector2 d, float R, float life, float alpha = 0.9f, int group = Front)
        {
            var p = new P { pos = c, aim = Unit(d), life = life, sz = R, group = group, col = SgGio, wd = alpha };
            p.draw = (q, k, buf) =>
            {
                float a = (1 - SmoothStep(0.3f, 1, k)) * q.wd;
                if (a < 0.04f) return;
                float r = q.sz * (0.82f + 0.3f * EaseOut(k));
                float ang = VelAng(q.aim) - 284.7f; // giữa cung của ảnh nằm ở góc 284,7 độ
                Put(buf, q.group, 45, S("arcs_0"), Ink, q.pos, 2 * r, 1, ang, a * 0.8f);
                Put(buf, q.group, 45.4f, S("arc_0"), Color.Lerp(q.col, SgBac, k), q.pos, 2 * r, 1, ang, a);
            };
            Add(p);
        }

        // vòng gió mảnh KHÔNG viền mực (vòng mảnh có viền mực thành vòng đen: soi trong trận 2026-11-16), nở / co rồi tan
        void SgVong(Vector2 pos, float life, float R0, float R1, float squash, float alpha = 0.85f, int group = Front)
        {
            var p = new P { pos = pos, life = life, group = group, col = SgGio, R0 = R0, R1 = R1, hgt = squash, wd = alpha };
            p.draw = (q, k, buf) =>
            {
                float R = q.R0 + (q.R1 - q.R0) * EaseOut(k);
                float a = (1 - SmoothStep(0.55f, 1, k)) * q.wd;
                if (a < 0.03f || R < 2) return;
                Put(buf, q.group, 32.5f, S("ring"), q.col, q.pos, 2 * R * q.hgt, 1 / q.hgt, 0, a);
            };
            Add(p);
        }

        // sợi gió trắng (SoiGio của bộ Mộc, màu gió sắt)
        P SgSoi(Vector2 pos, Vector2 vel, float life, float sz, int group = Front)
        {
            var q = SoiGio(pos, vel, life, sz, group);
            q.col = SgGio;
            return q;
        }

        // cú trúng sắt: chớp, tia theo hướng d (nửa vòng), dăm thép
        void SgTrung(Vector2 c, Vector2 d, float tH, float manh, int nTia, int nDam)
        {
            SatChop(c, 0.42f * tH * manh, Front, 0.14f);
            for (int i = 0; i < Mathf.RoundToInt(nTia * manh); i++)
            {
                var dd = (d * U(0.2f, 1f) + new Vector2(U(-0.7f, 0.7f), U(-1f, 0.4f))).normalized;
                Spark(c, dd, U(240, 480), U(0.18f, 0.3f), U(6, 9), 420);
            }
            for (int i = 0; i < Mathf.RoundToInt(nDam * manh); i++)
                GiaoDam(c + U2(-6, 6), (d * U(0.2f, 0.8f) + new Vector2(U(-0.7f, 0.7f), -U(0.3f, 1f))) * U(160, 340) * manh, U(10, 15) * Mathf.Sqrt(manh));
        }

        // sóng đất ở chỗ nện / húc: vòng đất, bụi toả hai bên, sỏi
        void SgDat(Vector2 g, float tH, float manh, int nBui, int nSoi)
        {
            Ring(g, 0.42f, 0.08f * tH, 0.62f * tH * manh, BuiC2, 0.3f, Floor, 31);
            for (int i = 0; i < Mathf.RoundToInt(nBui * manh); i++)
            {
                float sd = (i & 1) == 0 ? 1 : -1;
                Bui(g + new Vector2(sd * U(0.02f, 0.35f) * tH, U(-5, 2)), new Vector2(sd * U(110, 280) * manh, -U(10, 70)), U(0.45f, 0.7f), 4,
                    U(10, 15) * manh, (i & 2) == 0 ? Back : Front);
            }
            for (int i = 0; i < nSoi; i++)
                Rock(g + new Vector2(U(-0.15f, 0.15f) * tH, -6), new Vector2(U(-200, 200), -U(220, 380)), g.y + U(-4, 6), U(9, 14) * Mathf.Sqrt(manh));
        }

        // ĐÒN THƯỜNG: lao tới, búa bổ từ trên đầu xuống nện. lead: giây từ đầu clip attack tới lúc búa nện.
        public float NSoiGo(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.05f, lead), k = t0 / SgALead;
            const float manh = 1f;
            var toi = Vector2.Lerp(casterFeet, foeFeet, 0.72f); // sân kéo đỉnh cú lao tới 72 % quãng tới đối thủ (AolaSticker.Lunge)
            var g = toi + new Vector2(dir * SgDauBua.x * casterH, -SgDauBua.y * casterH);
            At(SgAVung * k, () =>
            {
                for (int i = 0; i < 5; i++)
                    Bui(casterFeet + new Vector2(-dir * U(0, 0.2f) * casterH, U(-5, 2)), new Vector2(-dir * U(100, 240), -U(20, 80)), U(0.35f, 0.55f), 3.5f, U(8, 12), Back);
            });
            // vệt búa bổ: cung từ trên đầu xuống trước mặt (búa đi từ 1,2 lần chiều cao xuống sát đất trong một khung)
            At(t0 - 0.04f * k, () => SgCung(toi + new Vector2(dir * 0.12f * casterH, -0.55f * casterH), new Vector2(dir * 0.75f, 0.66f), 0.66f * casterH, 0.14f));
            At(t0, () =>
            {
                Shake?.Invoke(0.3f * manh);
                SgTrung(g + new Vector2(0, -0.1f * tH), new Vector2(dir * 0.3f, -1), tH, 1.2f * manh, 8, 4);
                SgDat(g + new Vector2(0, 0.02f * tH), tH, 0.9f * manh, 6, 2);
            });
            return t0;
        }

        // tâm búa bay ở giây clip tc (sân)
        Vector2 SgBua(Vector2 feet, float H, float dir, Vector2 foeBody, float tc)
        {
            float u = (tc - SgCNem) / SgDt;
            return feet + new Vector2(dir * SgBang(SgBuaX, u) * H, -SgBang(SgBuaY, u) * H) + SgBang(SgBuaW, u) * (foeBody - feet);
        }

        // CHIÊU MANA: ném búa xoáy (búa là mảnh của rig, game lái tới thân đối thủ), búa nảy ra rồi bay về tay. manh: 0,85 dạng 1, 1 dạng 2.
        public float NSoiNem(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.2f, lead), k = t0 / SgCLead, T0 = T;
            float Tc() => (T - T0) / k;
            At(SgCVung * k, () =>
            {
                for (int i = 0; i < 3; i++)
                    Bui(casterFeet + new Vector2(-dir * U(0, 0.18f) * casterH, U(-5, 2)), new Vector2(-dir * U(70, 160), -U(10, 50)), 0, 3.5f, 9, Back);
            });
            At(SgCNem * k, () =>
            {
                var a = SgBua(casterFeet, casterH, dir, foeBody, SgCNem);
                SatChop(a, 0.14f * casterH * manh, Front, 0.1f);
                for (int i = 0; i < 6; i++) Spark(a, new Vector2(dir * U(0.4f, 1f), U(-0.5f, 0.4f)), U(220, 420), U(0.12f, 0.22f), U(5, 8), 100);
            });
            // búa bay xoáy: sợi gió kéo sau búa, cung gió quay theo búa (cả lượt đi và lượt về)
            void Bay(float a0, float a1)
            {
                Every(a0 * k, a1 * k, 70 * manh, x =>
                {
                    float tc = Tc();
                    var p = SgBua(casterFeet, casterH, dir, foeBody, tc);
                    var v = (SgBua(casterFeet, casterH, dir, foeBody, tc + SgDt) - SgBua(casterFeet, casterH, dir, foeBody, tc - SgDt)) / (2 * SgDt * k);
                    if (v.sqrMagnitude < 400) return;
                    SgSoi(p + U2(-0.08f, 0.08f) * casterH, -v * U(0.08f, 0.2f) + U2(-40, 40), U(0.14f, 0.22f), U(7, 10) * manh, Back);
                });
                Every(a0 * k, a1 * k, 22, x =>
                {
                    float tc = Tc();
                    var p = SgBua(casterFeet, casterH, dir, foeBody, tc);
                    float ga = SgBang(SgBuaA, (tc - SgCNem) / SgDt) * Mathf.Deg2Rad;
                    SgCung(p, new Vector2(dir * Mathf.Cos(ga), -Mathf.Sin(ga)), 0.26f * casterH * manh, 0.12f, 0.75f);
                });
            }
            Bay(SgCNem + 0.02f, SgCLead - 0.01f);
            Bay(SgCNay + 0.03f, SgCBat - 0.03f);
            var c = foeBody + new Vector2(-dir * 0.05f * tH, 0);
            At(t0, () =>
            {
                Shake?.Invoke(0.32f * manh);
                SgTrung(c, new Vector2(dir, 0), tH, 1.15f * manh, 9, 6);
                Ring(c, 0.34f, 0.06f * tH, 0.58f * tH * manh, SgThep, 0.5f, Front, 32);
                for (int i = 0; i < 4; i++) Bui(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, U(-4, 2)), new Vector2(U(-120, 120), -U(10, 60)), 0, 4, 11, Back);
            });
            // búa nảy khỏi thân đối thủ
            At(SgCNay * k, () =>
            {
                for (int i = 0; i < 5; i++) Spark(c, new Vector2(-dir * U(0.3f, 1f), U(-0.7f, 0.3f)), U(180, 340), U(0.12f, 0.2f), U(5, 7), 300);
            });
            At(SgCBat * k, () =>
            {
                var a = SgBua(casterFeet, casterH, dir, foeBody, SgCBat);
                SatChop(a, 0.16f * casterH * manh, Front, 0.12f);
                for (int i = 0; i < 4; i++) Spark(a, new Vector2(U(-1f, 1f), U(-1f, 0.2f)), U(120, 220), U(0.12f, 0.2f), U(5, 7), 150);
                for (int i = 0; i < 2; i++)
                    Bui(casterFeet + new Vector2(-dir * U(0.02f, 0.15f) * casterH, U(-5, 2)), new Vector2(-dir * U(60, 140), -U(10, 40)), 0, 3.5f, 9, Back);
            });
            return t0;
        }

        // CHIÊU CUỐI: che khiên, tụ gió, lùi lấy đà, lao xé gió, húc. dang: 0 sói con, 1 sói lớn. Trả giây tới lúc húc (= lead).
        public float NSoiHuc(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.4f, lead), k = t0 / SgSLead, T0 = T;
            float manh = dang == 0 ? 0.85f : 1f;
            float Tc() => (T - T0) / k;
            var toi = Vector2.Lerp(casterFeet, foeFeet, 0.72f); // đỉnh cú lao (AolaSticker.Lunge)
            var hg = Unit(toi - casterFeet);
            Vector2 Chan(float tc) => tc < 0.9f ? casterFeet : Vector2.LerpUnclamped(casterFeet, toi, SgBang(SgLao, (tc - 0.9f) / SgDt));
            var kc = SgKhienChe[dang];
            var khien = casterFeet + new Vector2(dir * kc.x * casterH, -kc.y * casterH);
            var kl = SgKhienLao[dang];

            // che khiên: chớp ở khiên, bụi hai bên chân
            At(SgSChe * k + 0.12f * k, () =>
            {
                SatChop(khien, 0.2f * casterH * manh, Front, 0.12f);
                for (int i = 0; i < 3; i++) Spark(khien, new Vector2(U(-1f, 1f), U(-1f, 0.2f)), U(140, 260), U(0.12f, 0.2f), U(5, 7), 200);
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(casterFeet + new Vector2(sd * U(0.05f, 0.3f) * casterH, U(-5, 2)), new Vector2(sd * U(60, 150), -U(10, 40)), 0, 3.5f, 10, Back);
                }
            });
            // tụ lực: sợi gió hút vào tướng, nhanh dần; bụi xoáy vào chân; sỏi run nảy; khiên loé hai lần
            Every(SgSTu * k, SgSTu1 * k, x => (34 + 60 * x) * manh, x =>
            {
                float a = U(0, Mathf.PI * 2), R = U(0.75f, 1.15f) * casterH;
                var dich = khien + new Vector2(-dir * 0.1f * casterH, 0);
                var p = dich + new Vector2(Mathf.Cos(a) * R, Mathf.Sin(a) * R * 0.7f);
                var v = dich - p;
                float life = U(0.2f, 0.3f);
                SgSoi(p, v / life * 1.1f, life, U(8, 12) * manh, rng.Next(2) == 0 ? Back : Front);
            });
            Every(SgSTu * k + 0.05f, SgSTu1 * k, 16 * manh, x =>
            {
                float sd = rng.Next(2) == 0 ? 1 : -1;
                Bui(casterFeet + new Vector2(sd * U(0.35f, 0.6f) * casterH, U(-5, 2)), new Vector2(-sd * U(90, 180), -U(10, 50)), U(0.35f, 0.55f), 3.5f, U(8, 12),
                    rng.Next(2) == 0 ? Back : Front);
            });
            for (int i = 0; i < 4; i++)
            {
                float tt = (SgSTu + 0.12f + 0.13f * i) * k;
                At(tt, () => Rock(casterFeet + new Vector2(U(-0.5f, 0.5f) * casterH, -4), new Vector2(U(-30, 30), -U(120, 200)), casterFeet.y + U(-3, 4), U(7, 10)));
            }
            At(0.75f * k, () => SatChop(khien, 0.13f * casterH * manh, Front, 0.1f));
            At(0.98f * k, () => SatChop(khien + new Vector2(dir * 0.05f * casterH, 0.04f * casterH), 0.15f * casterH * manh, Front, 0.1f));
            At(SgSTu1 * k, () => SgVong(khien, 0.24f, 0.95f * casterH, 0.1f * casterH, 0.65f)); // vòng gió co vào khiên
            // bật lao: bụi tung sau chân, vòng đất
            At(SgSLao * k, () =>
            {
                Shake?.Invoke(0.12f);
                Ring(casterFeet, 0.36f, 0.06f * casterH, 0.5f * casterH, BuiC2, 0.3f, Floor, 31);
                for (int i = 0; i < Mathf.RoundToInt(8 * manh); i++)
                    Bui(casterFeet + new Vector2(-dir * U(0, 0.25f) * casterH, U(-5, 2)), -hg * U(140, 320) + new Vector2(0, -U(20, 100)), U(0.4f, 0.65f), 4,
                        U(10, 15) * manh, (i & 1) == 0 ? Back : Front);
            });
            // lao xé gió: sợi gió xé ngược dọc thân, nón gió trước mép khiên, bụi kéo vệt dưới chân
            Every(SgSLao * k, SgSHuc * k, 170 * manh, x =>
            {
                var ch = Chan(Tc());
                var p = ch + new Vector2(dir * U(-0.6f, 0.75f) * casterH, -U(0.05f, 1.05f) * casterH);
                SgSoi(p, -hg * U(520, 900), U(0.14f, 0.22f), U(8, 12) * manh, rng.Next(3) == 0 ? Front : Back);
                if (rng.Next(4) == 0)
                    Bui(ch + new Vector2(-dir * U(0, 0.2f) * casterH, U(-5, 2)), -hg * U(80, 200) + new Vector2(0, -U(10, 50)), U(0.3f, 0.5f), 3.5f, U(8, 12), Back);
            });
            Every(SgSLao * k + 0.03f, SgSHuc * k, 30, x =>
            {
                var ch = Chan(Tc());
                var m = ch + new Vector2(dir * (kl.x + 0.08f) * casterH, -kl.y * casterH);
                SgCung(m, new Vector2(dir, 0), (0.32f + 0.22f * x) * casterH * manh, 0.12f, 0.9f);
            });
            // húc: chớp lớn, tia, dăm, vòng sóng kép, gió toạc ra sau lưng đối thủ, sóng đất, bụi, sỏi, rung mạnh
            var c = toi + new Vector2(dir * kl.x * casterH, -kl.y * casterH);
            At(SgSHuc * k, () =>
            {
                Shake?.Invoke(0.6f * manh);
                SatChop(c, 0.62f * tH * manh, Front, 0.16f);
                SgTrung(c, new Vector2(dir, -0.2f), tH, 1.3f * manh, 12, 8);
                Ring(c, 0.32f, 0.06f * tH, 0.6f * tH * manh, SgThep, 0.55f, Front, 32);
                for (int i = 0; i < Mathf.RoundToInt(18 * manh); i++)
                {
                    float a = U(-1.2f, 1.2f);
                    var d = new Vector2(dir * Mathf.Cos(a), Mathf.Sin(a) * 0.8f);
                    SgSoi(c + d * U(0.05f, 0.25f) * tH, d * U(600, 1000), U(0.18f, 0.3f), U(9, 13) * manh, (i & 1) == 0 ? Front : Back);
                }
                SgDat(foeFeet + new Vector2(-dir * 0.1f * tH, 2), tH, 1.2f * manh, 10, Mathf.RoundToInt(4 * manh));
            });
            At(SgSHuc * k + 0.07f, () =>
            {
                SgVong(c, 0.4f, 0.2f * tH, 1.2f * tH * manh, 0.5f);
                for (int i = 0; i < 5; i++)
                    Bui(foeFeet + new Vector2(dir * U(0.05f, 0.4f) * tH, U(-6, 2)), new Vector2(dir * U(120, 260), -U(20, 90)), U(0.5f, 0.8f), 5, U(12, 18) * manh, Back);
            });
            return t0;
        }
    }
}
