// Bộ chiêu của LÂM TƯỢNG (2026-11-12, ma mút rừng, suất phong_linh đảo Mộc; rig ArtGen/Spine/voi_rung.py).
// Chiêu mana "Vòi Phun": hít hơi (lá, bụi phấn bị hút vào chóp vòi), duỗi vòi phụt một luồng HẠT CÂY kèm lá vào thân đối thủ, hai nhịp
// phụt mạnh. Chiêu cuối "Dậm Rừng": chồm hai chân trước (lá quanh người cuốn xoáy bay lên), DẬM xuống: bụi, đất vụn, lá trên lưng
// bung ra, một làn sóng đất chạy tới đối thủ (từng cột lá phụt lên dọc đường), tới nơi rễ trồi và cột lá phun dưới chân nó.
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lá lấy từ WThemes.
// Mốc của clip (voi_rung.py): cast: hít từ 0,20 s, nhả = lead (0,62), giữ ngắm tới 1,56 (clip tự giữ, không cần HoldNuoc);
//   skill: chồm rống = lead − 0,87 s, dậm = lead (1,42).
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public const float VoiDur = 0.9f; // luồng hạt chảy chừng này giây kể từ lúc nhả
        static readonly Color HatC = C(238, 212, 150), HatC2 = C(196, 158, 96); // hạt cây màu mật như ngà của tướng (lõi, vỏ)
        static readonly Color BuiC = C(226, 208, 172), BuiC2 = C(198, 176, 138); // bụi đất be
        static readonly Color ReC = C(156, 116, 74), ReC2 = C(128, 94, 60); // rễ nâu gỗ

        // hạt cây: giọt thon hai lớp màu (vỏ sẫm, lõi sáng), mũi theo hướng bay; mẩu vỡ thì xoay tự do
        void DrawSeed(P p, float k, List<Item> buf)
        {
            float s = 2.5f * p.sz * (1 - SmoothStep(0.8f, 1, k));
            if (s < 1) return;
            float sp = p.vel.magnitude;
            var d = sp > 5 ? p.vel / sp : new Vector2(0, 1);
            float ang = p.fly ? TipAngle(-d) : p.ang;
            int i = p.seed & 3;
            Put(buf, p.group, 41, S("drops_" + i), Ink, p.pos, s + 4, 1, ang);
            Put(buf, p.group, 41.3f, S("drop_" + i), HatC2, p.pos, s, 1, ang);
            Put(buf, p.group, 41.6f, S("drop_" + i), HatC, p.pos + (p.fly ? d * s * 0.08f : Vector2.zero), s * 0.56f, 1, ang);
        }

        public P Seed(Vector2 pos, Vector2 vel, float life, float r, float grav = 0, float drag = 0, int group = Front, bool fly = true)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = drag, acc = new Vector2(0, grav), seed = rng.Next(4), sz = r, group = group, fly = fly,
                ang = U(0, 360), spin = fly ? 0 : U(-700, 700), spinDrag = 0.5f, ph = U(0, 6.28f)
            };
            p.draw = DrawSeed;
            return Add(p);
        }

        // cụm bụi đất: như bọt nhưng nhuộm be, nở rồi tan
        public P Bui(Vector2 pos, Vector2 vel, float life = 0, float r0 = 4, float r1 = 11, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life > 0 ? life : U(0.45f, 0.75f), drag = 2.6f, seed = rng.Next(8), r0 = r0, r1 = r1, group = group,
                ang = U(0, 6.28f), spin = U(-1, 1)
            };
            p.col = (p.seed & 4) != 0 ? BuiC2 : BuiC;
            p.draw = (q, k, buf) =>
            {
                float r = k < 0.25f ? q.r0 + (q.r1 - q.r0) * EaseOut(k / 0.25f) : q.r1 * (1 - 0.9f * SmoothStep(0.25f, 1, k));
                float a = 1 - SmoothStep(0.7f, 1, k);
                if (r < 1 || a < 0.03f) return;
                float g = q.ang * Mathf.Rad2Deg;
                Put(buf, q.group, 30, S("foams_" + (q.seed & 3)), Ink, q.pos, 2 * r + 3.5f, 1, g, a);
                Put(buf, q.group, 31, S("foam_" + (q.seed & 3)), q.col, q.pos, 2 * r, 1, g, a);
            };
            return Add(p);
        }

        // hạt vỡ lúc trúng: mẩu hạt bật ngược rồi rơi
        void HatVo(Vector2 at, Vector2 dd, int n)
        {
            for (int i = 0; i < n; i++)
                Seed(at, -dd * U(70, 190) + U2(-150, 150) + new Vector2(0, -U(40, 140)), U(0.32f, 0.5f), U(2.6f, 3.8f), 900, 1.2f, Front, false);
        }

        // VÒI PHUN (chiêu mana): hít → hai nhịp phụt; luồng hạt cây hẹp và nhanh, lá cuốn theo quanh luồng; hạt chạm thì vỡ bật ngược,
        // lá chạm thì rách; hết luồng nổ một chùm lá + hạt. Trả giờ tới lúc hạt đầu tiên chạm.
        public float NVoiPhun(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 target, Vector2 foeFeet, float tH, float lead,
            float dur = VoiDur)
        {
            var dd = Unit(target - mouth);
            var nrm = new Vector2(-dd.y, dd.x);
            float dist = (target - mouth).magnitude;
            float s0 = Mathf.Max(0.05f, lead);
            const float V = 980;
            float fly = Mathf.Max(0.03f, (dist - 14) / V);
            // hít: lúc này vòi còn cuộn lên, chóp vòi ở phía trên chỗ nhả một chút
            var hut = mouth + new Vector2(-dd.x * 0.05f * casterH, -0.15f * casterH);
            if (s0 > 0.2f)
                Every(Mathf.Max(0, s0 - 0.44f), s0 - 0.1f, 34, x =>
                {
                    float a = U(0, 6.28f);
                    var from = hut + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * U(46, 86) + dd * 30;
                    if (U(0, 1) < 0.6f) Leaf(from, (hut - from) * 3.6f, 0.26f, U(3.5f, 6f));
                    else Bui(from, (hut - from) * 3.2f, 0.26f, 2.5f, 6);
                });
            // hai nhịp phụt mạnh (thẻ đánh 2 lần): đầu luồng và giữa luồng
            Func<float, float> nhip = x => x < 0.14f || (x > 0.48f && x < 0.62f) ? 1.7f : x > 0.9f ? 0.55f : 1;
            foreach (float t in new[] { 0f, 0.44f })
                At(s0 + t, () =>
                {
                    Shake?.Invoke(0.28f);
                    BurstFlash(mouth + dd * 12, 0.2f * casterH);
                    for (int i = 0; i < 5; i++) Bui(mouth + U2(-5, 5), -dd * U(30, 90) + U2(-50, 50), 0, 3, 9);
                });
            // hạt cây
            Every(s0, s0 + dur, x => 48 * nhip(x), x =>
            {
                float spd = V * U(0.9f, 1.1f);
                float a = U(-0.06f, 0.06f);
                var q = Seed(mouth + nrm * U(-5, 5), (dd * Mathf.Cos(a) + nrm * Mathf.Sin(a)) * spd, dist / spd + 0.3f, U(5.2f, 7f));
                q.aim = target + new Vector2(U(-0.16f, 0.16f), U(-0.22f, 0.22f)) * tH;
                q.R0 = spd;
                q.upd = (z, dt, s) =>
                {
                    var to = z.aim - z.pos;
                    float d = to.magnitude;
                    z.vel += (to / Mathf.Max(d, 1e-5f) * z.R0 - z.vel) * Mathf.Min(1, 7 * dt);
                    if (d < 15)
                    {
                        z.hit = true;
                        z.dead = true;
                    }
                };
                q.onDeath = (z, s) =>
                {
                    if (!z.hit) return;
                    s.HatVo(z.pos, dd, 2);
                    if (s.U(0, 1) < 0.22f) s.BurstFlash(z.pos, 0.16f * tH);
                    if (s.U(0, 1) < 0.2f) s.Bui(z.pos, s.U2(-40, 40), 0, 3, 8);
                };
            });
            // lá cuốn theo luồng: toả rộng hơn hạt, lượn và lật
            Every(s0, s0 + dur, x => 54 * nhip(x), x =>
            {
                float spd = V * U(0.72f, 0.92f);
                float a = U(-0.2f, 0.2f);
                var q = Leaf(mouth + nrm * U(-9, 9), (dd * Mathf.Cos(a) + nrm * Mathf.Sin(a)) * spd, dist / spd + 0.35f, U(6f, 10f));
                q.aim = target + new Vector2(U(-0.26f, 0.26f), U(-0.32f, 0.32f)) * tH;
                q.R0 = spd;
                q.upd = (z, dt, s) =>
                {
                    var to = z.aim - z.pos;
                    float d = to.magnitude;
                    var want = to / Mathf.Max(d, 1e-5f) * z.R0 + nrm * (Mathf.Sin(z.age * 12 + z.ph) * 150);
                    z.vel += (want - z.vel) * Mathf.Min(1, 5.5f * dt);
                    if (d < 16)
                    {
                        z.hit = true;
                        z.dead = true;
                    }
                };
                q.onDeath = (z, s) =>
                {
                    if (z.hit && s.U(0, 1) < 0.4f)
                        s.Leaf(z.pos, -dd * s.U(60, 150) + s.U2(-120, 120), s.U(0.3f, 0.5f), s.U(3.5f, 5.5f), 700, 1.5f);
                };
            });
            Every(s0, s0 + dur, 12, x => Bui(mouth + U2(-5, 5) + dd * 8, dd * 90 + U2(-30, 30), 0, 2.5f, 6));
            Every(s0 + fly, s0 + fly + dur, 7, x => Shake?.Invoke(0.1f));
            At(s0 + fly + 0.44f, () => Shake?.Invoke(0.3f)); // nhịp phụt thứ hai tới nơi
            At(s0 + fly + dur, () =>
            {
                Shake?.Invoke(0.35f);
                LaNo(target, foeFeet, tH, 0.85f);
                HatVo(target, dd, 8);
            });
            return s0 + fly;
        }

        // một cột lá phụt lên từ mặt đất (sóng đất chạy qua): vòng nhỏ, bụi, đất vụn, lá bắn lên rồi rơi
        void CotLa(Vector2 dat, float tH, float sc)
        {
            Ripple(dat + new Vector2(0, 2), 0.05f * tH, 0.3f * tH * sc, 0.4f, BuiC2);
            for (int i = 0; i < 3; i++) Bui(dat + new Vector2(U(-10, 10) * sc, U(-4, 2)), new Vector2(U(-80, 80), -U(30, 90)) * sc, 0, 4, 11 * sc, Back);
            int n = Mathf.RoundToInt(12 * sc);
            for (int i = 0; i < n; i++)
                Leaf(dat + new Vector2(U(-9, 9) * sc, -U(2, 10)), new Vector2(U(-95, 95), -U(300, 520)) * sc, U(0.5f, 0.8f), U(4.5f, 7.5f), 900, 0.8f,
                    (i & 1) == 0 ? Back : Front);
            for (int i = 0; i < 2; i++) DaVun(dat + new Vector2(U(-8, 8), -4), new Vector2(U(-120, 120), -U(200, 340)) * sc, U(0.4f, 0.6f), U(2.6f, 3.8f));
        }

        // DẬM RỪNG (chiêu cuối): xem đầu file. Trả giờ tới lúc rễ và cột lá trồi dưới chân đối thủ.
        // manh: độ mạnh theo dạng (dạng cuối 1; dạng đầu 0,7: ít lá hơn, ba cột, không có rễ trồi).
        public float NDamRung(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh = 1)
        {
            float L = Mathf.Max(0.5f, lead);
            float tG = Mathf.Max(0.05f, L - 0.87f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var truoc = casterFeet + new Vector2(dir * 0.36f * casterH, 0); // chỗ hai chân trước dậm xuống
            var lung = casterFeet + new Vector2(-dir * 0.08f * casterH, -0.62f * casterH); // giữa khối lá trên lưng
            // gồng: vòng dưới chân, lá quanh người cuốn xoáy bay lên, bụi chân sau
            At(tG, () => Ripple(casterFeet + new Vector2(0, 2), 0.15f * casterH, 0.72f * casterH, 0.5f));
            Every(tG, L - 0.12f, 84 * manh, x =>
            {
                float a = U(0, 6.28f);
                float R = U(0.34f, 0.62f) * casterH;
                var from = casterFeet + new Vector2(Mathf.Cos(a) * R, Mathf.Sin(a) * R * 0.26f - U(0, 0.3f) * casterH);
                Leaf(from, new Vector2(-Mathf.Sin(a) * 200, -U(230, 400)), U(0.45f, 0.72f), U(5.5f, 9f), -140, 1.1f, Mathf.Sin(a) < 0 ? Back : Front);
            });
            Every(tG, L - 0.2f, 9, x =>
                Bui(casterFeet + new Vector2(-dir * U(0.1f, 0.4f) * casterH, U(-4, 2)), new Vector2(-dir * U(20, 70), -U(30, 80)), 0, 3, 8, Back));
            // DẬM
            At(L, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(FlashW);
                Ripple(truoc + new Vector2(0, 2), 0.14f * casterH, 1.0f * casterH, 0.5f, BuiC2);
                RingN(truoc + new Vector2(0, 2), 0.36f, 0.1f * casterH, 0.62f * casterH, BuiC, 0.3f, Floor, 30.6f);
                for (int i = 0; i < 14; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(truoc + new Vector2(sd * U(6, 40), U(-6, 3)), new Vector2(sd * U(120, 330), -U(15, 80)), U(0.5f, 0.85f), 5, U(11, 17),
                        i < 9 ? Back : Front);
                }
                for (int i = 0; i < 8; i++) DaVun(truoc + new Vector2(U(-26, 26), -4), new Vector2(U(-230, 230), -U(240, 460)), U(0.5f, 0.8f), U(3f, 4.8f));
                for (int i = 0; i < 22; i++) // lá trên lưng bung ra theo cú dậm
                {
                    float a = 3.14f + 3.14f * (i + U(0, 0.8f)) / 22; // nửa trên
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Leaf(lung + d * U(0.18f, 0.34f) * casterH, d * U(190, 420) + new Vector2(dir * 60, 0), U(0.55f, 0.9f), U(5f, 8.5f), 560, 1.6f,
                        (i & 1) == 0 ? Back : Front);
                }
            });
            // sóng đất chạy tới đối thủ: bốn cột lá phụt lên dọc đường, cột sau to hơn
            int N = manh >= 1 ? 4 : 3;
            const float buoc = 0.07f;
            for (int i = 0; i < N; i++)
            {
                int j = i;
                float f = 0.28f + 0.62f * j / (N - 1f);
                At(L + buoc * (j + 1), () => CotLa(Vector2.Lerp(truoc, foeFeet, f), tH, (0.9f + 0.2f * j) * manh));
            }
            float hit = L + buoc * (N + 1);
            At(hit, () =>
            {
                Shake?.Invoke(0.9f);
                LaNo(foeBody, foeFeet, tH, 1.5f * manh);
                RingN(foeBody, 0.32f, 0.14f * tH, 0.8f * tH, W[3], 1, Front, 36);
                WExtra(foeBody, 9, 340);
                Ripple(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.85f * tH, 0.5f, BuiC2);
                for (int i = 0; i < 9; i++)
                    Bui(foeFeet + new Vector2(U(-0.4f, 0.4f) * tH, U(-6, 2)), new Vector2(U(-140, 140), -U(15, 70)), 0, 4, 14, Back);
                if (HasGai && manh >= 1) // rễ trồi quanh chân đối thủ: ba cái cao phía sau, hai cái thấp hai bên phía trước
                {
                    var goc = new[] { (-0.34f, -0.25f, 0.92f, Back), (0.02f, 0.0f, 1.06f, Back), (0.36f, 0.28f, 0.86f, Back), (-0.5f, -0.75f, 0.46f, Front),
                        (0.52f, 0.8f, 0.44f, Front) };
                    for (int i = 0; i < goc.Length; i++)
                    {
                        var (ox, nghieng, dai, nhom) = goc[i];
                        var q = Spike(foeFeet + new Vector2(ox * tH, 2), new Vector2(nghieng, -1), dai * tH, 0.75f, nhom, i, 0.42f);
                        q.col = (i & 1) == 0 ? ReC : ReC2;
                    }
                }
            });
            // cột lá phun dưới chân đối thủ (phần lớn sau lưng nó, không che mặt)
            Every(hit, hit + 0.5f, x => 84 * manh * (1 - 0.6f * x), x =>
                Leaf(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -U(0, 0.15f) * tH), new Vector2(U(-80, 80), -U(420, 720)), U(0.55f, 0.85f), U(4.5f, 7.5f), 980,
                    0.7f, U(0, 1) < 0.72f ? Back : Front));
            At(hit + 0.12f, () => BurstFlash(foeBody + new Vector2(0, -0.1f * tH), 0.42f * tH));
            return hit;
        }

        // đòn đánh thường có hiệu ứng dù tướng LAO tới (không đứng bắn): StageView.AtkFx phát lúc clip attack bắt đầu
        public static bool AtkLao(string kind) => kind == "n_hat_nga" || kind == "n_mo_dam";

        // HẤT NGÀ (đòn đánh thường, clip attack của voi_rung.py: cào đất lead − 0,40; chân sau đạp bật lead − 0,14; nện + hất ngà = lead):
        // bụi cào đất dưới chân trước, bụi và đất vụn bắn ra sau lúc chân sau đạp, lá trên lưng tuột lại phía sau lúc bay, tới nơi
        // chân trước nện: vòng bụi + bụi hai bên; chỗ ngà chạm thân đối thủ: chớp toé nhỏ, lá vỡ, bụi. Nhỏ hơn chiêu mana.
        public float NHatNga(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            // sân kéo đỉnh cú lao tới 72 % quãng tới đối thủ (AolaSticker.Lunge): thân đáp ở đó, hai chân trước nện xuống phía trước nó
            var toi = Vector2.Lerp(casterFeet, foeFeet, 0.72f);
            var truoc = toi + (foeFeet - casterFeet).normalized * 0.2f * casterH;
            var sau = casterFeet + new Vector2(-dir * 0.3f * casterH, 0); // chân sau
            // cào đất
            if (L > 0.42f)
                Every(L - 0.42f, L - 0.3f, 26, x =>
                    Bui(casterFeet + new Vector2(dir * U(0.22f, 0.34f) * casterH, U(-4, 2)), new Vector2(-dir * U(90, 190), -U(20, 70)), 0, 2.5f, 7, Back));
            // chân sau đạp bật
            At(Mathf.Max(0.02f, L - 0.14f), () =>
            {
                Shake?.Invoke(0.25f);
                Ripple(sau + new Vector2(0, 2), 0.06f * casterH, 0.4f * casterH, 0.35f, BuiC2);
                for (int i = 0; i < 9; i++)
                    Bui(sau + new Vector2(U(-14, 14), U(-5, 2)), new Vector2(-dir * U(120, 320), -U(30, 130)), U(0.4f, 0.7f), 4, U(9, 15), i < 6 ? Back : Front);
                for (int i = 0; i < 4; i++) DaVun(sau + new Vector2(U(-10, 10), -4), new Vector2(-dir * U(120, 260), -U(180, 320)), U(0.4f, 0.6f), U(2.6f, 3.8f), Back);
            });
            // đang bay: lá tuột lại phía sau
            float t0 = Mathf.Max(0.02f, L - 0.12f);
            float goc = T;
            Every(t0, L, 60, x =>
            {
                float k = Mathf.Clamp01((T - goc - t0) / Mathf.Max(0.02f, L - t0));
                var at = Vector2.Lerp(casterFeet, toi, k) + new Vector2(-dir * U(0, 0.3f) * casterH, -U(0.45f, 0.95f) * casterH);
                Leaf(at, new Vector2(-dir * U(60, 180), U(-90, 30)), U(0.35f, 0.6f), U(4.5f, 7.5f), 420, 1.4f, U(0, 1) < 0.6f ? Back : Front);
            });
            // nện + hất ngà
            At(L, () =>
            {
                Shake?.Invoke(0.35f);
                Ripple(toi + new Vector2(0, 2), 0.1f * casterH, 0.52f * casterH, 0.4f, BuiC2);
                for (int i = 0; i < 12; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    var goc2 = i < 6 ? truoc : toi;
                    Bui(goc2 + new Vector2(sd * U(6, 0.3f * casterH), U(-5, 3)), new Vector2(sd * U(110, 280), -U(15, 70)), U(0.4f, 0.7f), 4, U(9, 14), Back);
                }
                for (int i = 0; i < 4; i++) DaVun(truoc + new Vector2(U(-12, 12), -4), new Vector2(U(-150, 150), -U(190, 330)), U(0.4f, 0.6f), U(2.6f, 3.8f), Back);
                // chỗ ngà hất: chớp toé + lá bật khỏi đối thủ theo hướng hất (lên và ra xa con đánh). Không đặt bụi ở đây: con đánh
                // đang đè lên đối thủ, bụi sẽ dính lên mặt nó
                var cham = foeBody + new Vector2(dir * 0.15f * tH, -0.1f * tH); // phía mũi ngà, qua khỏi mặt con đánh
                BurstFlash(cham, 0.5f * tH);
                for (int i = 0; i < 10; i++)
                {
                    float a = dir * 0.55f + (i - 4.5f) * 0.3f + U(-0.12f, 0.12f); // góc tính từ phương thẳng lên, ngả theo hướng hất
                    var d = new Vector2(Mathf.Sin(a), -Mathf.Cos(a));
                    Leaf(cham + d * U(6, 14), d * U(200, 380), U(0.45f, 0.75f), U(4.5f, 7f), 640, 2f);
                }
            });
            return L;
        }
    }
}
