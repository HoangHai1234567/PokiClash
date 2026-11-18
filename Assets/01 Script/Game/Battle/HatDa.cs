// Bộ ĐÁ RỪNG của Gạc Đá (2026-11-12, tượng đá cổ giữ rừng, suất gac_da đảo Mộc; rig ArtGen/Spine/tuong_da*.py).
// Người dùng: "chiêu mana đưa 2 tay lên trước bắn 2 bàn tay vào đối thủ" (rig tự bắn hai tảng cẳng tay trên xương fly_*; lớp này chỉ lo
// cú TRÚNG: đá vụn, bụi); "chiêu cuối đưa 2 tay lên trời xoè bàn tay tụ 1 quả cầu năng lượng (làm thêm fx, khi tụ làm kiểu hiệu ứng
// gió / lá bị hút xung quanh vào cầu), sau đó 2 tay đổ về phía trước kiểu ném vào đối thủ".
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes
// (bản tươi MocTuoi của HatMoc.cs).
// Mốc của clip skill (tuong_da_clip.py): tụ = lead − 1,56 s, cầu đầy = lead − 0,48, ngả sau = lead − 0,32, rời tay = lead − 0,18.
// Nâng 2026-11-18 (người dùng: "các skill hút khí ... xung quanh tụ cầu đang xấu"; "khói rải rác chưa thành cụm"): quả cầu nhiều múi đập
// theo nhịp tim, hạt hút bay xoắn ốc nhanh dần và nhập vào cầu, cầu nén 1–2 khung rồi chớp lúc rời tay, nổ cầu kiểu Kingdom Rush 5 (NoCau).
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color DaC = C(146, 136, 116), DaC2 = C(118, 108, 92); // nâu xám của tảng tay (nâng sáng 2026-11-18: bản cũ xám tối)

        // đá vụn: dăm đá xoay, rơi có trọng lực (dùng ảnh dăm gai nhuộm màu đá; máy chưa có ảnh đó thì tạm dùng lá)
        P DaVun(Vector2 pos, Vector2 vel, float life, float r, int group = Front)
        {
            if (!HasGai) return Leaf(pos, vel, life, r, 700, 1.6f, group);
            var q = Shard(pos, vel, life, r, 820, 1.4f, group);
            q.col = (q.seed & 4) != 0 ? DaC2 : DaC;
            return q;
        }

        // đá vỡ lúc tảng tay nện trúng: chớp nhỏ 2 khung ở trước, khối toé sau thân, dăm đá văng toả đều rồi rơi, cụm bụi đá tách dần
        void DaNo(Vector2 c, float tH, float sc)
        {
            Chop(c, 0.34f * tH * sc, 0.07f);
            BurstFlash(c, 0.48f * tH * sc, Back, 0.16f);
            int n = Mathf.RoundToInt(9 * sc);
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / n; // rải đều góc (ngẫu nhiên hẳn thì dồn cục)
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                DaVun(c + d * U(4, 12), d * U(180, 380) * sc, U(0.45f, 0.75f), U(2.8f, 4.8f));
            }
            for (int i = 0; i < 2; i++)
                BuiCum(c + new Vector2(U(-0.25f, 0.25f), U(-0.2f, 0.1f)) * tH, new Vector2(U(-70, 70), -U(30, 70)), U(0.1f, 0.13f) * tH * sc, 0, Back);
        }

        // HAI TẢNG TAY NỆN TRÚNG (chiêu mana): tảng gần chạm ở khung trúng của clip, tảng xa sau đó 0,10 s; mỗi cú đá vụn + bụi, cú sau
        // thêm họa tiết của chủ đề, cụm bụi và vòng cung dẹt dưới chân, vết trên đất
        public float NDaVa(Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            MocSang();
            float s0 = Mathf.Max(0.02f, lead);
            var c1 = foeBody + new Vector2(0, 0.10f * tH);
            var c2 = foeBody + new Vector2(0, -0.14f * tH);
            At(s0, () =>
            {
                Shake?.Invoke(0.5f);
                DanhTrung?.Invoke(c1, 0.6f);
                DaNo(c1, tH, 1);
                CungDat(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.55f * tH, 0.4f, CungC, 0.07f * tH);
            });
            At(s0 + 0.10f, () =>
            {
                Shake?.Invoke(0.55f);
                DanhTrung?.Invoke(c2, 0.7f);
                DaNo(c2, tH, 1.1f);
                WExtra(c2, 4, 300);
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    BuiCum(foeFeet + new Vector2(sd * U(0.12f, 0.36f) * tH, U(-6, 2)), new Vector2(sd * U(60, 140), -U(15, 45)), U(0.1f, 0.14f) * tH, 0, Back);
                }
                VetDat(foeFeet + new Vector2(0, 3), 0.38f * tH, 0.9f);
            });
            return s0;
        }

        // QUẢ CẦU NĂNG LƯỢNG RỪNG (Gạc Đá, Lộc Phong, Giác Mộc): khối nhiều múi cuộn (bốn múi đậm quay quanh tâm thành mép gồ ghề, không phải
        // hình tròn trơn), lớp giữa, lõi vàng chanh rộng, tâm kem, hai vòng xoắn quay, ba chiếc lá bay vòng quanh (nửa sau vẽ sau cầu); ĐẬP theo
        // nhịp tim nhanh dần (mỗi nhịp phồng 12 % rồi xẹp). Ảnh kr_cau thay bốn múi khi đã nhập. cFn, rFn: theo giây từ lúc gọi; nhanh: giây
        // tới lúc nhịp đập nhanh nhất (0: ba phần tư đời).
        P CauLa(Func<float, Vector2> cFn, float tEnd, Func<float, float> rFn, int group = Front, float nhanh = 0)
        {
            var p = new P { pos = cFn(0), life = tEnd, group = group, seed = rng.Next(4), stops = W, wd = nhanh > 0 ? nhanh : tEnd * 0.75f };
            p.upd = (q, dt, s) =>
            {
                var np = cFn(q.age);
                q.drift = np - q.pos;
                q.pos = np;
                q.vel = Vector2.zero;
                q.vy += dt * (2.2f + 6.5f * Mathf.Clamp01(q.age / q.wd)); // pha nhịp đập: 2,2 → 8,7 nhịp/giây
            };
            p.draw = (q, k, buf) =>
            {
                float age = q.age;
                float r = rFn(age);
                if (r < 1.5f) return;
                r *= 1 + 0.12f * Mathf.Exp(-9 * (q.vy - Mathf.Floor(q.vy))); // nhịp tim: phồng ngay đầu nhịp rồi xẹp
                float mv = q.drift.magnitude;
                float ang = mv > 0.3f ? -Mathf.Atan2(q.drift.y, q.drift.x) * Mathf.Rad2Deg : 0;
                float st = 1 + Mathf.Min(0.3f, mv / 12);
                var w = q.stops;
                int g = q.group, sd = q.seed;
                var kc = S("kr_cau_" + sd);
                if (kc != null)
                {
                    float rot = age * 50;
                    Put(buf, g, 20, S("kr_caus_" + sd) ?? kc, Ink, q.pos, 2.3f * r + 5, st, ang + rot);
                    Put(buf, g, 21, kc, w[1], q.pos, 2.3f * r, st, ang + rot);
                    Put(buf, g, 21.5f, kc, w[2], q.pos, 1.8f * r, st, ang - rot * 0.7f);
                }
                else
                {
                    for (int j = 0; j < 4; j++) // bốn múi quay quanh tâm: mép gồ ghề như khối năng lượng cuộn
                    {
                        float a = age * 2.4f + j * 1.571f;
                        var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * (0.3f * r);
                        Put(buf, g, 20, S("solid_" + ((sd + j) & 3)), Ink, q.pos + o, 1.45f * r + 5, st, ang + j * 40);
                        Put(buf, g, 21, S("blob_" + ((sd + j) & 3)), w[1], q.pos + o, 1.45f * r, st, ang + j * 40);
                    }
                    Put(buf, g, 21.5f, S("blob_" + ((sd + 1) & 3)), w[2], q.pos, 1.62f * r, st, ang);
                }
                Put(buf, g, 22, S("blob_" + ((sd + 2) & 3)), MocChanh, q.pos + new Vector2(-r * 0.06f, -r * 0.08f), 1.18f * r, 1, ang);
                Put(buf, g, 23, S("blob_" + ((sd + 3) & 3)), MocKem, q.pos + new Vector2(-r * 0.12f, -r * 0.16f), 0.62f * r, 1, ang);
                for (int j = 0; j < 2; j++)
                {
                    float a = age * 8 + j * Mathf.PI;
                    Put(buf, g, 24, S("curl_" + j), j == 0 ? MocKem : w[2], q.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.75f) * r * 0.3f, r * 0.72f, 1,
                        -a * Mathf.Rad2Deg);
                }
                if (r < 9) return;
                for (int j = 0; j < 3; j++)
                {
                    float a = age * 5.5f + j * 2.094f;
                    bool sau = Mathf.Sin(a) < 0;
                    var lp = q.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.5f) * r * 1.2f;
                    float ls = Mathf.Max(7, r * 0.46f);
                    float la = -a * Mathf.Rad2Deg;
                    Put(buf, g, sau ? 19.2f : 26, LeafS(j, true), Ink, lp, ls + 3.5f, 0.62f, la);
                    Put(buf, g, sau ? 19.5f : 26.3f, LeafS(j, false), w[2], lp, ls, 0.58f, la);
                }
            };
            return Add(p);
        }

        // HÚT về tâm cFn (giây từ lúc gọi): vệt gió thuôn (đầu đậm đuôi nhạt, dài theo vận tốc, không viền) và lá (mũi theo hướng bay) bay XOẮN ỐC
        // vào tâm, cùng một chiều xoáy, NHANH DẦN khi tới gần (ease-in); sinh ra thì hiện dần, tới tâm thì co lại nhập vào cầu đúng lúc chạm; mật
        // độ tăng dần tới lúc nhả; hai vòng co về tâm. Bản cũ: vệt trắng viền mực dày như que xương, bay gần thẳng, bật phụt, vòng nở to mảnh.
        void GatherLa(Func<float, Vector2> cFn, float t0, float t1, float reach, float rate, int group = Front)
        {
            if (t1 - t0 < 0.05f) return;
            float start = T;
            float chieu = U(0, 1) < 0.5f ? 1 : -1; // một chiều xoáy cho cả đám
            Every(t0, t1, x => rate * (0.35f + 1.3f * x), x =>
            {
                float R = U(0.6f, 1) * reach;
                bool gio = U(0, 1) < 0.5f;
                var q = new P
                {
                    life = U(0.34f, 0.5f), seed = rng.Next(8), group = U(0, 1) < 0.35f ? Back : group, sz = gio ? U(3f, 4.6f) : U(4.2f, 6.6f), ph = U(0, 6.28f),
                    R0 = R, vy = U(9, 15), stops = W, hgt = chieu * U(1.6f, 2.4f)
                };
                q.pos = cFn(T - start) + new Vector2(Mathf.Cos(q.ph), Mathf.Sin(q.ph) * 0.8f) * R;
                q.upd = (z, dt, s) =>
                {
                    float k = Mathf.Min(1, z.age / z.life), e = k * k;
                    float a = z.ph + z.hgt * e;
                    var np = cFn(s.T - start) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * (z.R0 * (1 - e));
                    z.vel = (np - z.pos) / Mathf.Max(dt, 1e-5f);
                    float sp = z.vel.magnitude;
                    if (sp > 1) z.ang = TipAngle(z.vel / sp); // lá: mũi theo hướng bay
                };
                if (gio) q.draw = DrawGioHut;
                else q.draw = DrawLaHut;
                Add(q);
            });
            var w3 = W[3];
            At(t0 + (t1 - t0) * 0.3f, () => VongCo(cFn, start, reach * 0.95f, w3, group));
            At(Mathf.Max(t0, t1 - 0.3f), () => VongCo(cFn, start, reach * 0.8f, w3, group));
        }

        // vệt gió bị hút: thân nhạt, nửa đầu đậm hơn; hiện dần lúc sinh, mảnh dần, tới tâm thì co lại nhập vào cầu
        void DrawGioHut(P z, float k, List<Item> buf)
        {
            float a = Mathf.Min(1, k / 0.22f) * (1 - SmoothStep(0.88f, 1, k));
            if (a < 0.04f) return;
            float sp = z.vel.magnitude;
            var d = sp > 1 ? z.vel / sp : Vector2.right;
            float day = z.sz * (1 - 0.45f * k);
            float len = Mathf.Clamp(sp * 0.07f, day * 2.2f, day * 7);
            var w = z.stops;
            VetPut(buf, z.group, 38, false, MocKem, z.pos, d, len, day, 0.8f * a, z.seed);
            VetPut(buf, z.group, 38.2f, false, w[3], z.pos + d * (len * 0.24f), d, len * 0.5f, day * 0.92f, a, z.seed);
        }

        // lá bị hút: hiện dần (nở từ 60 %), lật, mũi theo hướng bay, co lại lúc nhập vào cầu
        void DrawLaHut(P z, float k, List<Item> buf)
        {
            float a = Mathf.Min(1, k / 0.2f);
            float s = 2.9f * z.sz * (1 - SmoothStep(0.82f, 1, k)) * (0.6f + 0.4f * a);
            if (s < 1) return;
            var w = z.stops;
            float st = 0.45f + 0.55f * Mathf.Abs(Mathf.Cos(z.age * z.vy + z.ph));
            int i = z.seed & 3;
            Put(buf, z.group, 40, LeafS(i, true), Ink, z.pos, s + 4, (s * st + 4) / (s + 4), z.ang, a);
            Put(buf, z.group, 40.3f, LeafS(i, false), (z.seed & 4) != 0 ? w[2] : Color.Lerp(w[2], w[3], 0.55f), z.pos, s, st, z.ang, a);
        }

        // vòng CO về tâm (lấy đà tụ cầu): vòng không viền từ ngoài co vào nhanh dần, đậm dần, chạm tâm thì tắt (ảnh kr_cung: vòng dẹt đứt đoạn
        // nằm ngang quanh cầu như một đĩa năng lượng; chưa có thì vòng tròn ring)
        void VongCo(Func<float, Vector2> cFn, float start, float R, Color col, int group)
        {
            var p = new P { pos = cFn(T - start), life = 0.3f, group = group, col = col, R0 = R, tb = start, seed = rng.Next(4), ang = U(0, 360) };
            p.upd = (q, dt, s) =>
            {
                q.pos = cFn(s.T - q.tb);
                q.vel = Vector2.zero;
            };
            p.draw = (q, k, buf) =>
            {
                float Rr = q.R0 * (1 - 0.86f * k * k);
                float a = Mathf.Min(1, k / 0.3f) * (1 - SmoothStep(0.85f, 1, k));
                var kc = S("kr_cung_" + q.seed);
                if (kc != null) Put(buf, q.group, 18, kc, q.col, q.pos, 2 * Rr / 0.9f, 1, 0, a);
                else Put(buf, q.group, 18, S("ring"), q.col, q.pos, 2 * Rr, 1, 0, a);
            };
            Add(p);
        }

        // CẦU TIM RỪNG (chiêu cuối): lúc hai tay giơ lên, gió và lá quanh người bị hút xoắn về điểm giữa hai bàn tay phía trên đầu, quả cầu lớn
        // dần và đập nhanh dần; đầy thì một vòng sáng lan; con ra chiêu ngả ra sau rồi đổ tay: ngay trước lúc rời tay cầu NÉN lại 1–2 khung rồi
        // chớp và bật to, bay thẳng tới thân đối thủ, kéo đuôi lá; trúng: nổ cầu (NoCau: chớp, khối nhiều múi sau thân, lưỡi liềm, lá, bụi cụm,
        // vòng cung dẹt, vết đất), lá rơi lượn.
        public float NCauLa(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.7f, lead);
            float tTu = Mathf.Max(0.05f, L - 1.56f), tDay = L - 0.48f, tNga = L - 0.32f, tNem = L - 0.18f;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var c0 = casterFeet + new Vector2(0.03f * dir * casterH, -1.33f * casterH);
            var cNga = c0 + new Vector2(-0.07f * dir * casterH, -0.02f * casterH);
            var cNem = casterFeet + new Vector2(0.52f * dir * casterH, -0.70f * casterH);
            float fly = Mathf.Clamp((foeBody - cNem).magnitude / 1500f, 0.12f, 0.3f);
            float hit = tNem + fly;
            float rFull = 0.25f * casterH;
            // age: giây kể từ lúc tụ (tTu)
            Func<float, Vector2> cFn = age =>
            {
                float t = tTu + age;
                if (t < tDay) return c0 + new Vector2(0, 2.5f * Mathf.Sin(age * 9));
                if (t < tNga) return Vector2.Lerp(c0, cNga, SmoothStep(tDay, tNga, t));
                if (t < tNem)
                {
                    float k = (t - tNga) / (tNem - tNga);
                    k *= k;
                    return Vector2.Lerp(cNga, cNem, k) + new Vector2(0, -0.12f * casterH * Mathf.Sin(Mathf.PI * k));
                }
                return Vector2.Lerp(cNem, foeBody, Mathf.Clamp01((t - tNem) / fly));
            };
            Func<float, float> rFn = age =>
            {
                float t = tTu + age;
                if (t > hit - 0.02f) return 0;
                float g = Mathf.Clamp01(age / Mathf.Max(0.1f, tDay - tTu));
                float r = rFull * (0.25f + 0.75f * g) * Mathf.Min(1, age / 0.1f);
                return r * NenNha(t, tNem);
            };
            At(tTu, () =>
            {
                CauLa(cFn, hit - tTu, rFn, Front, tNem - tTu);
                CungDat(casterFeet + new Vector2(0, 2), 0.15f * casterH, 0.6f * casterH, 0.45f, W[2], 0.06f * casterH);
                GatherLa(cFn, 0, tNem - tTu - 0.04f, 1.1f * casterH, 56);
                // bụi và lá dưới chân bị cuốn lên: cụm nhỏ, bay lên rồi tách
                Every(0, tDay - tTu, 5, x =>
                    BuiCum(casterFeet + new Vector2(U(-0.5f, 0.5f) * casterH, U(-4, 2)), new Vector2(U(-30, 30), -U(90, 160)), U(0.06f, 0.09f) * casterH, 0, Back));
            });
            At(tDay, () =>
            {
                Shake?.Invoke(0.2f);
                VongVa(c0, 0.2f * casterH, 0.62f * casterH, 0.3f, MocKem, Back);
            });
            At(tNem, () => // rời tay: chớp đúng lúc cầu bật ra sau 1–2 khung nén
            {
                Shake?.Invoke(0.3f);
                Chop(cNem, 0.42f * casterH, 0.08f);
                WExtra(cNem, 4, 220);
            });
            // đuôi lá + vệt năng lượng sau quả cầu lúc bay
            float goc = T;
            Every(tNem, hit, 56, x =>
            {
                var at = cFn(T - goc - tTu);
                if (U(0, 1) < 0.65f) Leaf(at + U2(-6, 6), new Vector2(-dir * U(60, 160), U(-90, 90)), U(0.3f, 0.5f), U(3.4f, 5.4f), 300, 1.5f);
                else TiaVunCum(at, new Vector2(-dir, U(-0.4f, 0.4f)), 0.5f, 2, U(120, 220), U(2.8f, 4f));
            });
            At(hit, () =>
            {
                Shake?.Invoke(0.9f);
                NoCau(foeBody, foeFeet, tH, 1.4f);
                WExtra(foeBody, 7, 340);
            });
            return hit;
        }
    }
}
