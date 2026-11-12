// Bộ Mộc của lớp hạt chồng lớp phẳng (2026-11-12, tướng tinh linh rừng Mầm Ú, id mam_u: "chiêu mana há mồm bắn ra nhiều lá cây vào người
// đối thủ"). Hạt LÁ là ảnh xám có gân (ArtGen/Spine/la.py → hat_leaf_<i>, hat_leafs_<i>) nhuộm bằng Image.color, một lớp mực + một
// lớp màu, lật nghiêng lúc bay. Dùng chung khung của bộ Thủy (HatNuoc.cs): mã chiêu bắt đầu bằng "n_", phát lúc clip BẮT ĐẦU kèm lead,
// bảng màu lấy từ WThemes (mực, lục đậm, lục non, lục nhạt, phấn), nên StageView / HeroViewer không phải thêm đường riêng.
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public const float LaDur = 0.9f; // chiêu phun lá: luồng lá chảy chừng này giây kể từ lúc nhả (clip cast giữ há mồm 0,94 s)

        Sprite LeafS(int i, bool solid) => S((solid ? "leafs_" : "leaf_") + i) ?? S((solid ? "drops_" : "drop_") + i);

        // lá: xoay theo p.ang (độ), lật nghiêng theo tuổi (bề ngang co giãn), co nhỏ ở cuối đời
        void DrawLeaf(P p, float k, List<Item> buf)
        {
            float s = 2.9f * p.sz * (1 - SmoothStep(0.8f, 1, k));
            if (s < 1) return;
            var w = p.stops ?? W;
            float st = 0.4f + 0.6f * Mathf.Abs(Mathf.Cos(p.age * p.vy + p.ph));
            int i = p.seed & 3;
            Put(buf, p.group, 40, LeafS(i, true), Ink, p.pos, s + 4, (s * st + 4) / (s + 4), p.ang);
            Put(buf, p.group, 40.3f, LeafS(i, false), (p.seed & 4) != 0 ? w[2] : w[1], p.pos, s, st, p.ang);
        }

        public P Leaf(Vector2 pos, Vector2 vel, float life, float r, float grav = 0, float drag = 0, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = drag, acc = new Vector2(0, grav), seed = rng.Next(8), sz = r, group = group,
                ang = TipAngle(Unit(vel)), spin = U(-520, 520), spinDrag = 0.6f, ph = U(0, 6.28f), vy = U(9, 15), stops = W
            };
            p.draw = DrawLeaf;
            return Add(p);
        }

        // lá vỡ lúc trúng: chớp toé nhỏ màu lá, lá văng toả rồi rơi, phấn, vòng dưới chân
        void LaNo(Vector2 c, Vector2 foeFeet, float tH, float sc)
        {
            BurstFlash(c, 0.46f * tH * sc);
            int n = Mathf.RoundToInt(12 * sc);
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / n; // rải đều góc (ngẫu nhiên hẳn thì dồn cục)
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.25f);
                Leaf(c + d * U(4, 12), d * U(170, 360) * sc, U(0.55f, 0.85f), U(4.5f, 7.5f), 620, 2.2f);
            }
            for (int i = 0; i < 5; i++) Foam(c + U2(-14, 14) * sc, U2(-60, 60) + new Vector2(0, -40), 0, 3, 9 * sc);
            Ripple(foeFeet + new Vector2(0, 2), 0.12f * tH, 0.5f * tH * sc);
        }

        // PHUN LÁ: lúc hít (trước khung nhả) lá nhỏ và phấn bị hút vào mồm; từ khung nhả một luồng lá dày bắn tới thân đối thủ, mỗi lá
        // tự lái nhẹ về một điểm trong thân, lượn và lật; lá chạm thì vỡ thành mẩu lá bật ngược + phấn; hết luồng nổ một chùm lá.
        public float NLa(Vector2 mouth, Vector2 target, Vector2 foeFeet, float tH, float lead, float dur = LaDur)
        {
            var dd = Unit(target - mouth);
            var nrm = new Vector2(-dd.y, dd.x);
            float dist = (target - mouth).magnitude;
            float s0 = Mathf.Max(0.05f, lead);
            const float V = 780;
            float fly = dist / V;
            if (s0 > 0.16f)
                Every(0, s0 - 0.08f, 24, x =>
                {
                    float a = U(0, 6.28f);
                    var from = mouth + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * U(42, 78) + dd * 26;
                    Leaf(from, (mouth - from) * 3.4f, 0.28f, U(3.5f, 6f));
                });
            Every(s0, s0 + dur, x => 72 * (x < 0.14f ? 1.5f : x > 0.86f ? 0.6f : 1), x => // "bắn ra NHIỀU lá": bản đầu 40 lá/giây, lá nhỏ, nhìn thưa
            {
                float spd = V * U(0.86f, 1.14f);
                float a = U(-0.16f, 0.16f);
                var v = (dd * Mathf.Cos(a) + nrm * Mathf.Sin(a)) * spd;
                var q = Leaf(mouth + nrm * U(-8, 8), v, dist / spd + 0.3f, U(7.5f, 12.5f));
                q.aim = target + new Vector2(U(-0.24f, 0.24f), U(-0.3f, 0.3f)) * tH;
                q.R0 = spd;
                q.upd = (z, dt, s) =>
                {
                    var to = z.aim - z.pos;
                    float d = to.magnitude;
                    var want = to / Mathf.Max(d, 1e-5f) * z.R0 + nrm * (Mathf.Sin(z.age * 13 + z.ph) * 120);
                    z.vel += (want - z.vel) * Mathf.Min(1, 6 * dt);
                    if (d < 15)
                    {
                        z.hit = true;
                        z.dead = true;
                    }
                };
                q.onDeath = (z, s) =>
                {
                    if (!z.hit) return;
                    if (s.U(0, 1) < 0.45f) s.Leaf(z.pos, -dd * s.U(60, 150) + s.U2(-120, 120), s.U(0.3f, 0.5f), s.U(3.5f, 5.5f), 700, 1.5f);
                    if (s.U(0, 1) < 0.14f) s.Foam(z.pos, s.U2(-40, 40), 0, 3, 8);
                };
            });
            Every(s0, s0 + dur, 14, x => Foam(mouth + U2(-5, 5) + dd * 8, dd * 90 + U2(-30, 30), 0, 2.5f, 6));
            Every(s0 + fly, s0 + fly + dur, 7, x => Shake?.Invoke(0.1f));
            At(s0 + fly + dur, () =>
            {
                Shake?.Invoke(0.3f);
                LaNo(target, foeFeet, tH, 0.8f);
            });
            return s0 + fly;
        }

        // cú HÚC BỤNG của chiêu lao tới: gọi đúng khung trúng; lá vỡ tung quanh chỗ chạm, sao văng (họa tiết của chủ đề), bụi dưới chân
        public float NLaVa(Vector2 foeBody, Vector2 foeFeet, float tH)
        {
            Shake?.Invoke(0.6f);
            LaNo(foeBody, foeFeet, tH, 1.3f);
            WExtra(foeBody, 9, 320);
            for (int i = 0; i < 6; i++) Foam(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, U(-6, 2)), new Vector2(U(-90, 90), U(-50, -10)), 0, 4, 12, Back);
            return 0;
        }

        // ================= GAI (2026-11-12, Cầu Gai ở suất tien_la: "gồng rồi phóng dài các gai cơ thể dài hẳn ra đâm tứ tung") =================
        // Rig tự làm gai trên thân dài ra (clip cast); lớp này lo phần tới được đối thủ: gai trồi từ đất chạy tới chân nó rồi đâm tua tủa.
        // Ảnh hat_thorn_<i> (một gai), hat_tuft_<i> (cụm gai trồi), hat_shard_<i> (dăm gai): ArtGen/Spine/gai.py đặt hình theo một quy ước:
        // hình chiếm tối đa 92% khung vuông, canh giữa ngang, ĐÁY hình (thorn, tuft) ở 96% chiều cao khung.
        const float GaiLap = 0.92f, GaiDay = 0.46f; // GaiDay: tâm khung cách đáy hình 0,46 khung
        static readonly Color GaiC = C(255, 238, 164), GaiC2 = C(250, 218, 132); // kem vàng ấm như gai của tướng (ảnh hạt xám vân chì nhân vào còn xỉn đi; kem nhạt thì ra xám be)
        const float GaiInk = 9; // viền mực dày như viền gai của tướng: bản đầu 5, gai kem lẫn vào nền cát

        public bool HasGai => S("thorn_0") && S("tuft_0") && S("shard_0");

        Sprite GaiS(string ten, int i, bool solid) => S(ten + (solid ? "s_" : "_") + i);

        void DrawShard(P p, float k, List<Item> buf)
        {
            float s = 2.6f * p.sz * (1 - SmoothStep(0.75f, 1, k));
            if (s < 1) return;
            int i = p.seed & 3;
            Put(buf, p.group, 41, GaiS("shard", i, true), Ink, p.pos, s + 3.5f, 1, p.ang);
            Put(buf, p.group, 41.3f, GaiS("shard", i, false), p.col, p.pos, s, 1, p.ang);
        }

        // dăm gai: mảnh gãy xoay, rơi có trọng lực
        public P Shard(Vector2 pos, Vector2 vel, float life, float r, float grav = 760, float drag = 1.4f, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = drag, acc = new Vector2(0, grav), seed = rng.Next(8), sz = r, group = group,
                ang = U(0, 360), spin = U(-760, 760), spinDrag = 0.5f
            };
            p.col = (p.seed & 4) != 0 ? GaiC2 : GaiC;
            p.draw = DrawShard;
            return Add(p);
        }

        // nhịp trồi: bật quá cỡ trong 0,07 s, về cỡ, đứng, rồi rút xuống ở 28% cuối đời
        static float GaiGrow(float k, float life)
        {
            float t = k * life;
            if (t < 0.07f) return 1.22f * EaseOut(t / 0.07f);
            if (t < 0.14f) return 1.22f - 0.22f * (t - 0.07f) / 0.07f;
            return 1 - SmoothStep(0.72f, 1, k);
        }

        // cụm gai trồi từ đất: đáy bám đất, wd là bề rộng khung hình trên sân
        P Tuft(Vector2 feet, float wd, float life = 0.6f, int group = Front, int seed = -1)
        {
            var p = new P { pos = feet, life = life, group = group, seed = seed >= 0 ? seed : rng.Next(4), wd = wd, col = GaiC };
            p.draw = (q, k, buf) =>
            {
                float h = q.wd * GaiGrow(k, q.life);
                if (h < 3) return;
                var c = q.pos - new Vector2(0, h * GaiDay);
                Put(buf, q.group, 36, GaiS("tuft", q.seed, true), Ink, c, h + GaiInk, (q.wd + GaiInk) / (h + GaiInk));
                Put(buf, q.group, 36.3f, GaiS("tuft", q.seed, false), q.col, c, h, q.wd / h);
            };
            return Add(p);
        }

        // một cái gai dài đâm lên từ đất theo hướng dir (đơn vị), dài len, mập thick (bề ngang so với bề dài của khung)
        P Spike(Vector2 at, Vector2 dir, float len, float life, int group, int seed, float thick = 0.5f)
        {
            var p = new P { pos = at, life = life, group = group, seed = seed & 3, wd = len / GaiLap, off = Unit(dir), hgt = thick, col = (seed & 4) != 0 ? GaiC2 : GaiC };
            p.draw = (q, k, buf) =>
            {
                float f = q.wd * GaiGrow(k, q.life);
                if (f < 4) return;
                var c = q.pos + q.off * (f * GaiDay);
                float ang = TipAngle(q.off);
                Put(buf, q.group, 35, GaiS("thorn", q.seed, true), Ink, c, f + GaiInk, (f * q.hgt + GaiInk) / (f + GaiInk), ang);
                Put(buf, q.group, 35.3f, GaiS("thorn", q.seed, false), q.col, c, f, q.hgt, ang);
            };
            return Add(p);
        }

        // gai gãy vụn: chớp toé, dăm gai văng toả rồi rơi, bụi
        void GaiNo(Vector2 c, float tH, float sc, int n = 12)
        {
            BurstFlash(c, 0.48f * tH * sc);
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / n; // rải đều góc
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                Shard(c + d * U(4, 12), d * U(190, 400) * sc, U(0.5f, 0.8f), U(3.2f, 5.6f));
            }
            for (int i = 0; i < 4; i++) Foam(c + U2(-14, 14) * sc, U2(-60, 60) + new Vector2(0, -40), 0, 3, 9 * sc);
        }

        // GỒNG GAI: lúc gồng (trước khung nhả) dăm gai bị hút vào thân; khung nhả gai trên thân bật dài (rig), dăm gai văng tứ tung quanh
        // thân; gai trồi từ đất chạy thành hàng tới chân đối thủ, cụm sau to hơn cụm trước; tới nơi một cụm lớn bật lên sau lưng nó, gai
        // dài đâm chéo tua tủa (cao ở sau lưng, thấp ở trước cho khỏi che), dăm gai văng; gai đứng 0,5 s rồi rút xuống.
        public float NGai(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float s0 = Mathf.Max(0.05f, lead);
            var body = casterFeet - new Vector2(0, 0.5f * casterH);
            if (s0 > 0.16f)
                Every(0, s0 - 0.08f, 26, x =>
                {
                    float a = U(0, 6.28f);
                    var from = body + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * U(0.5f, 0.9f) * casterH;
                    Shard(from, (body - from) * 3.6f, 0.26f, U(2.4f, 4.2f), 0, 0);
                });
            At(s0, () =>
            {
                Shake?.Invoke(0.22f);
                Ripple(casterFeet + new Vector2(0, 2), 0.2f * casterH, 0.78f * casterH, 0.4f);
                for (int i = 0; i < 10; i++)
                {
                    float a = 6.28f * (i + U(0, 0.8f)) / 10;
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.2f);
                    Shard(body + d * 0.42f * casterH, d * U(260, 480), U(0.35f, 0.6f), U(3, 5));
                }
                for (int i = 0; i < 5; i++)
                    Foam(casterFeet + new Vector2(U(-0.3f, 0.3f) * casterH, U(-4, 2)), new Vector2(U(-110, 110), U(-40, -10)), 0, 4, 11, Back);
            });
            const int N = 4;
            const float Gap = 0.06f;
            var run = foeFeet - casterFeet;
            for (int i0 = 0; i0 < N; i0++)
            {
                int i = i0;
                At(s0 + 0.05f + i * Gap, () =>
                {
                    var at = casterFeet + run * (0.36f + 0.12f * i) + new Vector2(U(-6, 6), U(-3, 3)); // bắt đầu ngoài thân con ra chiêu
                    Tuft(at, (0.44f + 0.09f * i) * tH, 0.5f);
                    Shake?.Invoke(0.06f);
                    for (int j = 0; j < 2; j++) Shard(at + new Vector2(U(-8, 8), -6), new Vector2(U(-110, 110), -U(150, 260)), U(0.35f, 0.5f), U(2.6f, 4));
                    Foam(at + new Vector2(U(-8, 8), 0), new Vector2(U(-50, 50), -U(20, 50)), 0, 3, 9, Back);
                });
            }
            float hit = s0 + 0.05f + N * Gap + 0.03f;
            At(hit, () =>
            {
                Shake?.Invoke(0.5f);
                Tuft(foeFeet + new Vector2(0, -3), 1.35f * tH, 0.74f, Back, 2 + rng.Next(2));
                Tuft(foeFeet + new Vector2(-0.52f * tH, 6), 0.4f * tH, 0.66f, Front, 1); // hai cụm trước đứng hai bên, thấp: không che mặt con bị trúng
                Tuft(foeFeet + new Vector2(0.52f * tH, 7), 0.4f * tH, 0.66f, Front, 1);
                GaiNo(foeBody, tH, 1);
                WExtra(foeBody, 6, 300);
                Ripple(foeFeet + new Vector2(0, 2), 0.14f * tH, 0.62f * tH);
                for (int i = 0; i < 6; i++)
                    Foam(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, U(-6, 2)), new Vector2(U(-100, 100), U(-50, -10)), 0, 4, 12, Back);
            });
            // gai dài đâm chéo lên: ba cái cao sau lưng, hai cái thấp phía trước
            for (int j0 = 0; j0 < 5; j0++)
            {
                int j = j0;
                At(hit + 0.02f + j * 0.035f, () =>
                {
                    bool back = j < 3;
                    float x = back ? (j - 1) * 0.3f : (j == 3 ? -0.4f : 0.4f);
                    float tilt = x * (back ? 1.5f : -1.3f) + U(-0.08f, 0.08f); // sau lưng xoè ra ngoài, phía trước chĩa chéo vào trong
                    var d = new Vector2(Mathf.Sin(tilt), -Mathf.Cos(tilt));
                    var at = foeFeet + new Vector2(x * tH, back ? -2 : 7);
                    Spike(at, d, (back ? U(1.2f, 1.45f) : U(0.42f, 0.52f)) * tH, 0.62f - j * 0.02f, back ? Back : Front, j, back ? 0.42f : 0.55f);
                    Shake?.Invoke(0.12f);
                    for (int i = 0; i < 2; i++) Shard(at + d * 10, d * U(160, 300) + U2(-80, 80), U(0.35f, 0.55f), U(2.6f, 4.2f));
                });
            }
            At(hit + 0.5f, () => // gai rút: vụn rơi
            {
                for (int i = 0; i < 7; i++)
                    Shard(foeFeet + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.1f, 0.8f) * tH), new Vector2(U(-50, 50), U(-30, 40)), U(0.4f, 0.6f), U(2.4f, 3.8f));
            });
            return hit;
        }

        // cú TÔNG của chiêu cuối "Lăn Gai" (quả cầu gai xoay lao vào): gọi đúng khung chạm; gai gãy văng tung, cụm gai bật lên dưới chân
        public float NGaiVa(Vector2 foeBody, Vector2 foeFeet, float tH)
        {
            Shake?.Invoke(0.7f);
            GaiNo(foeBody, tH, 1.4f, 18);
            WExtra(foeBody, 9, 340);
            Tuft(foeFeet + new Vector2(0, -3), 0.9f * tH, 0.5f, Back, 1);
            Ripple(foeFeet + new Vector2(0, 2), 0.14f * tH, 0.7f * tH);
            for (int i = 0; i < 7; i++) Foam(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, U(-6, 2)), new Vector2(U(-110, 110), U(-55, -10)), 0, 4, 13, Back);
            return 0;
        }
    }
}
