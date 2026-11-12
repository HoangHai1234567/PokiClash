// Bộ ĐÁ RỪNG của Gạc Đá (2026-11-12, tượng đá cổ giữ rừng, suất gac_da đảo Mộc; rig ArtGen/Spine/tuong_da*.py).
// Người dùng: "chiêu mana đưa 2 tay lên trước bắn 2 bàn tay vào đối thủ" (rig tự bắn hai tảng cẳng tay trên xương fly_*; lớp này chỉ lo
// cú TRÚNG: đá vụn, bụi); "chiêu cuối đưa 2 tay lên trời xoè bàn tay tụ 1 quả cầu năng lượng (làm thêm fx, khi tụ làm kiểu hiệu ứng
// gió / lá bị hút xung quanh vào cầu), sau đó 2 tay đổ về phía trước kiểu ném vào đối thủ".
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes.
// Mốc của clip skill (tuong_da_clip.py): tụ = lead − 1,56 s, cầu đầy = lead − 0,48, ngả sau = lead − 0,32, rời tay = lead − 0,18.
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color DaC = C(128, 120, 104), DaC2 = C(104, 97, 84); // nâu xám của tảng tay

        // đá vụn: dăm đá xoay, rơi có trọng lực (dùng ảnh dăm gai nhuộm màu đá; máy chưa có ảnh đó thì tạm dùng lá)
        P DaVun(Vector2 pos, Vector2 vel, float life, float r, int group = Front)
        {
            if (!HasGai) return Leaf(pos, vel, life, r, 700, 1.6f, group);
            var q = Shard(pos, vel, life, r, 820, 1.4f, group);
            q.col = (q.seed & 4) != 0 ? DaC2 : DaC;
            return q;
        }

        // đá vỡ lúc tảng tay nện trúng: chớp toé nhỏ, dăm đá văng toả đều rồi rơi, bụi
        void DaNo(Vector2 c, float tH, float sc)
        {
            BurstFlash(c, 0.44f * tH * sc);
            int n = Mathf.RoundToInt(9 * sc);
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / n; // rải đều góc (ngẫu nhiên hẳn thì dồn cục)
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                DaVun(c + d * U(4, 12), d * U(180, 380) * sc, U(0.45f, 0.75f), U(3.2f, 5.4f));
            }
            for (int i = 0; i < 4; i++) Foam(c + U2(-14, 14) * sc, U2(-60, 60) + new Vector2(0, -40), 0, 3, 9 * sc);
        }

        // HAI TẢNG TAY NỆN TRÚNG (chiêu mana): tảng gần chạm ở khung trúng của clip, tảng xa sau đó 0,10 s; mỗi cú đá vụn + bụi, cú sau
        // thêm họa tiết của chủ đề và vòng bụi dưới chân
        public float NDaVa(Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            float s0 = Mathf.Max(0.02f, lead);
            var c1 = foeBody + new Vector2(0, 0.10f * tH);
            var c2 = foeBody + new Vector2(0, -0.14f * tH);
            At(s0, () =>
            {
                Shake?.Invoke(0.5f);
                DaNo(c1, tH, 1);
                Ripple(foeFeet + new Vector2(0, 2), 0.12f * tH, 0.55f * tH);
            });
            At(s0 + 0.10f, () =>
            {
                Shake?.Invoke(0.55f);
                DaNo(c2, tH, 1.1f);
                WExtra(c2, 5, 300);
                for (int i = 0; i < 5; i++)
                    Foam(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, U(-6, 2)), new Vector2(U(-90, 90), U(-50, -10)), 0, 4, 12, Back);
            });
            return s0;
        }

        // quả cầu năng lượng rừng: ba lớp tròn (lục đậm, lục giữa, lõi nhạt), hai vòng xoắn quay bên trong, ba chiếc lá bay vòng quanh
        // (nửa sau vẽ sau cầu). cFn, rFn: theo giây từ lúc gọi
        P CauLa(Func<float, Vector2> cFn, float tEnd, Func<float, float> rFn, int group = Front)
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
                float r = rFn(age);
                if (r < 1.5f) return;
                float mv = q.drift.magnitude;
                float ang = mv > 0.3f ? -Mathf.Atan2(q.drift.y, q.drift.x) * Mathf.Rad2Deg : 0;
                float st = 1 + Mathf.Min(0.3f, mv / 12);
                var w = q.stops;
                int g = q.group, sd = q.seed;
                Put(buf, g, 20, S("solid_" + sd), Ink, q.pos, 2 * r + 5, st, ang);
                Put(buf, g, 21, S("blob_" + sd), w[1], q.pos, 2 * r, st, ang);
                Put(buf, g, 22, S("blob_" + ((sd + 1) & 3)), w[2], q.pos, 1.62f * r, st, ang);
                Put(buf, g, 23, S("blob_" + ((sd + 2) & 3)), w[3], q.pos + new Vector2(-r * 0.1f, -r * 0.14f), r, 1, ang);
                for (int j = 0; j < 2; j++)
                {
                    float a = age * 8 + j * Mathf.PI;
                    Put(buf, g, 24, S("curl_" + j), j == 0 ? w[4] : w[1], q.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.75f) * r * 0.3f, r * 0.72f, 1,
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

        // gió và lá bị HÚT về điểm cFn(giây từ lúc gọi): lá xoay bay trôn ốc vào tâm, sợi gió trắng mảnh cuốn theo, vòng năng lượng co lại
        // dần; càng về cuối càng dày
        void GatherLa(Func<float, Vector2> cFn, float t0, float t1, float reach, float rate, int group = Front)
        {
            if (t1 - t0 < 0.05f) return;
            float start = T;
            Every(t0, t1, x => rate * (0.5f + 0.8f * x), x =>
            {
                float R = U(0.55f, 1) * reach;
                bool gio = U(0, 1) < 0.34f;
                var q = new P
                {
                    life = U(0.36f, 0.52f), seed = rng.Next(8), group = U(0, 1) < 0.35f ? Back : group, sz = U(6, 10.5f), ph = U(0, 6.28f), R0 = R,
                    vy = U(9, 15), stops = W, spin = U(-500, 500), ang = U(0, 360)
                };
                q.pos = cFn(T - start) + new Vector2(Mathf.Cos(q.ph), Mathf.Sin(q.ph) * 0.8f) * R;
                q.upd = (z, dt, s) =>
                {
                    float k = Mathf.Min(1, z.age / z.life);
                    float a = z.ph + 5f * k * k;
                    float rr = z.R0 * Mathf.Pow(1 - k, 1.25f);
                    var np = cFn(s.T - start) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * rr;
                    z.vel = (np - z.pos) / Mathf.Max(dt, 1e-5f);
                };
                if (gio)
                {
                    q.col = W[4];
                    q.draw = (z, k, buf) =>
                    {
                        float a = 1 - Mathf.Abs(2 * k - 1);
                        if (a < 0.05f) return;
                        Put(buf, z.group, 38, S("streakg_" + (z.seed & 1)), z.col, z.pos, z.sz * 1.6f, Mathf.Clamp(z.vel.magnitude / 70, 2.2f, 4.5f),
                            VelAng(z.vel), Mathf.Min(1, a * 1.6f));
                    };
                }
                else q.draw = DrawLeaf;
                Add(q);
            });
            int n = Mathf.Max(1, (int)((t1 - t0) / 0.24f));
            var w3 = W[3];
            for (int i = 0; i < n; i++)
                At(t0 + i * 0.24f, () => RingN(cFn(T - start), 0.36f, reach * 0.85f, reach * 0.14f, w3, 1, group, 18));
        }

        // CẦU TIM RỪNG (chiêu cuối): lúc hai tay giơ lên, gió và lá quanh người bị hút về điểm giữa hai bàn tay phía trên đầu, quả cầu lớn
        // dần và đập nhanh dần; đầy thì chớp một nhịp; con ra chiêu ngả ra sau rồi đổ tay: cầu theo tay vòng qua đỉnh đầu ra trước, rời tay
        // bay thẳng tới thân đối thủ, kéo đuôi lá; trúng: nổ lá (nhỏ hơn thân), vòng lan dưới chân, lá rơi lả tả.
        public float NCauLa(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
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
                if (tTu + age > hit - 0.02f) return 0;
                float g = Mathf.Clamp01(age / Mathf.Max(0.1f, tDay - tTu));
                float r = rFull * (0.25f + 0.75f * g) * Mathf.Min(1, age / 0.1f);
                return r * (1 + 0.05f * Mathf.Sin(age * (10 + 10 * g)));
            };
            At(tTu, () =>
            {
                CauLa(cFn, hit - tTu, rFn);
                Ripple(casterFeet + new Vector2(0, 2), 0.15f * casterH, 0.6f * casterH, 0.45f);
                GatherLa(cFn, 0, tNga - tTu, 1.1f * casterH, 70);
                // bụi và lá dưới chân bị cuốn lên
                Every(0, tDay - tTu, 9, x =>
                    Foam(casterFeet + new Vector2(U(-0.5f, 0.5f) * casterH, U(-4, 2)), new Vector2(U(-30, 30), -U(120, 220)), 0, 2.5f, 7, Back));
            });
            At(tDay, () =>
            {
                Shake?.Invoke(0.25f);
                BurstFlash(c0, 0.5f * casterH, Back);
                WExtra(c0, 5, 220);
            });
            At(tNem, () => Shake?.Invoke(0.3f));
            // đuôi lá sau quả cầu lúc bay
            float goc = T;
            Every(tNem, hit, 70, x =>
            {
                var at = cFn(T - goc - tTu);
                Leaf(at + U2(-6, 6), new Vector2(-dir * U(60, 160), U(-90, 90)), U(0.3f, 0.5f), U(4, 7), 300, 1.5f);
            });
            At(hit, () =>
            {
                Shake?.Invoke(0.9f);
                LaNo(foeBody, foeFeet, tH, 1.5f);
                RingN(foeBody, 0.3f, 0.12f * tH, 0.62f * tH, W[3], 1, Front, 32);
                WExtra(foeBody, 9, 340);
                for (int i = 0; i < 7; i++)
                    Foam(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, U(-6, 2)), new Vector2(U(-110, 110), U(-55, -10)), 0, 4, 13, Back);
            });
            At(hit + 0.12f, () => BurstFlash(foeBody + new Vector2(0, -0.12f * tH), 0.34f * tH));
            // lá rơi lả tả sau cú nổ
            Every(hit + 0.05f, hit + 0.45f, 26, x =>
                Leaf(foeBody + new Vector2(U(-0.5f, 0.5f) * tH, -U(0.2f, 0.7f) * tH), new Vector2(U(-40, 40), U(20, 80)), U(0.5f, 0.8f), U(4, 6.5f), 260, 1.2f,
                    U(0, 1) < 0.5f ? Back : Front));
            return hit;
        }
    }
}
