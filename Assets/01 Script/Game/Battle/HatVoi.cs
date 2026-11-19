// Bộ chiêu của LÂM TƯỢNG (2026-11-12, ma mút rừng, suất phong_linh đảo Mộc; rig ArtGen/Spine/voi_rung.py).
// Chiêu mana "Vòi Phun": hít hơi (lá, bụi phấn bị hút vào chóp vòi), duỗi vòi phụt một luồng HẠT CÂY kèm lá vào thân đối thủ, hai nhịp
// phụt mạnh. Chiêu cuối "Dậm Rừng": chồm hai chân trước (lá quanh người cuốn xoáy bay lên), DẬM xuống: bụi, đất vụn, lá trên lưng
// bung ra, một làn sóng đất chạy tới đối thủ (từng cột lá phụt lên dọc đường), tới nơi rễ trồi và cột lá phun dưới chân nó.
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lá lấy từ WThemes.
// Mốc của clip (voi_rung.py): cast: hít từ 0,20 s, nhả = lead (0,62), giữ ngắm tới 1,56 (clip tự giữ, không cần HoldNuoc);
//   skill: chồm rống = lead − 0,87 s, dậm = lead (1,42).
// Nâng 2026-11-18 (người dùng: "khói rải rác chưa thành cụm, chưa mềm", "sóng đất chưa đẹp", "hút khí xấu", "màu tươi hơn"): hít bằng vệt gió
// và lá xoắn ốc nhanh dần (GatherLa); bông va chạm toé liên tục ở mặt trước thân đối thủ; bụi thành cụm tách dần (BuiCum); sóng đất là lưỡi
// liềm dẹt chạy trên đất, nở và mỏng dần (SongDat), vòng cung dẹt đứt đoạn (CungDat), vết đất giữ ~1 s (VetDat). Bui giữ nguyên cho các
// file hệ khác đang dùng.
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
            MocSang();
            var dd = Unit(target - mouth);
            var nrm = new Vector2(-dd.y, dd.x);
            float dist = (target - mouth).magnitude;
            float s0 = Mathf.Max(0.05f, lead);
            const float V = 980;
            float fly = Mathf.Max(0.03f, (dist - 14) / V);
            // hít: lúc này vòi còn cuộn lên, chóp vòi ở phía trên chỗ nhả một chút
            var hut = mouth + new Vector2(-dd.x * 0.05f * casterH, -0.15f * casterH);
            if (s0 > 0.2f) GatherLa(t => hut, Mathf.Max(0, s0 - 0.44f), s0 - 0.08f, 86, 30);
            // hai nhịp phụt mạnh (thẻ đánh 2 lần): đầu luồng và giữa luồng
            Func<float, float> nhip = x => x < 0.14f || (x > 0.48f && x < 0.62f) ? 1.7f : x > 0.9f ? 0.55f : 1;
            foreach (float t in new[] { 0f, 0.44f })
                At(s0 + t, () =>
                {
                    Shake?.Invoke(0.28f);
                    Chop(mouth + dd * 12, 0.22f * casterH, 0.07f);
                    for (int i = 0; i < 2; i++) BuiCum(mouth + U2(-5, 5), -dd * U(30, 90) + U2(-50, 50), U(5, 7), 0, Front, CumPhan, false);
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
                };
            });
            // lá cuốn theo luồng: toả rộng hơn hạt, lượn và lật
            Every(s0, s0 + dur, x => 54 * nhip(x), x =>
            {
                float spd = V * U(0.72f, 0.92f);
                float a = U(-0.2f, 0.2f);
                var q = Leaf(mouth + nrm * U(-9, 9), (dd * Mathf.Cos(a) + nrm * Mathf.Sin(a)) * spd, dist / spd + 0.35f, U(5f, 8.5f));
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
            Every(s0, s0 + dur, 6, x => BuiCum(mouth + U2(-5, 5) + dd * 8, dd * U(70, 110) + U2(-30, 30), U(4, 6), 0, Front, CumPhan, false));
            // chỗ chạm: bông va chạm toé ngược liên tục ở mặt trước thân đối thủ, tia vụn theo cụm, đối thủ giật từng nhịp
            var cham = ChamThan(mouth, target, tH);
            var bong = new P { pos = cham, life = dur + 0.06f, group = Front, sz = 0.34f * tH, seed = rng.Next(4) };
            bong.draw = (q, k, buf) =>
            {
                float t = q.age;
                float g = t < 0.05f ? 0.5f + 0.6f * EaseOut(t / 0.05f) : 1.1f - 0.1f * Mathf.Min(1, (t - 0.05f) / 0.05f);
                g *= (1 - SmoothStep(q.life - 0.12f, q.life, t)) * (0.88f + 0.12f * Mathf.Sin(t * 60));
                BongVa(buf, q.group, q.pos, -dd, q.sz * g, q.seed + (int)(t * 15));
            };
            At(s0 + fly, () =>
            {
                Add(bong);
                Chop(cham, 0.3f * tH, 0.07f);
            });
            Every(s0 + fly, s0 + fly + dur, 8, x => TiaVunCum(cham + nrm * U(-8, 8), -dd, 1.2f, 3, U(240, 400), U(2.8f, 4f), U(0, 1) < 0.7f ? Front : Back, HatC, MocKem));
            Every(s0 + fly, s0 + fly + dur, 7, x =>
            {
                Shake?.Invoke(0.1f);
                DanhTrung?.Invoke(cham, 0.25f);
            });
            At(s0 + fly + 0.44f, () => Shake?.Invoke(0.3f)); // nhịp phụt thứ hai tới nơi
            At(s0 + fly + dur, () =>
            {
                Shake?.Invoke(0.35f);
                LaNo(target, foeFeet, tH, 0.85f);
                HatVo(target, dd, 8);
            });
            return s0 + fly;
        }

        // một cột lá phụt lên từ mặt đất (sóng đất chạy qua): vòng cung dẹt nhỏ, cụm bụi, đất vụn, lá bắn lên rồi rơi.
        // Khung vẽ sẵn (2026-11-19): một cụm gai lá (gai_la) phóng lên ngay chỗ cột (bỏ gần hết khung nứt đất, gọi đúng lúc sóng đất chạy qua) nên
        // lá bắn lên bớt còn ~40 %; bụi là một cụm khói nhuộm đất thay hai cụm BuiCum. Chưa nhập khung thì như cũ. nhomGai: lớp vẽ cụm gai.
        void CotLa(Vector2 dat, float tH, float sc, int nhomGai = Back)
        {
            CungDat(dat + new Vector2(0, 2), 0.05f * tH, 0.32f * tH * sc, 0.38f, CungC, 0.05f * tH * sc, 3);
            bool coGai = MocGaiFb(dat + new Vector2(U(-4, 4), -1), U(0.5f, 0.58f) * tH * sc, 0.07f, 0.08f, nhomGai, 35, U(0, 1) < 0.5f, 1.35f, 3.5f);
            if (MocKhoiFb(dat + new Vector2(U(-8, 8) * sc, U(-2, 2)), 0.1f * tH * sc, new Vector2(U(-40, 40), -U(30, 60)) * sc, Back, 4.5f, 1.4f, 0.88f) == null)
                for (int i = 0; i < 2; i++)
                    BuiCum(dat + new Vector2(U(-10, 10) * sc, U(-4, 2)), new Vector2(U(-70, 70), -U(30, 70)) * sc, U(0.07f, 0.1f) * tH * sc, 0, i == 0 ? Back : Front);
            int n = Mathf.RoundToInt((coGai ? 4.5f : 11) * sc);
            for (int i = 0; i < n; i++)
                Leaf(dat + new Vector2(U(-9, 9) * sc, -U(2, 10)), new Vector2(U(-95, 95), -U(300, 520)) * sc, U(0.5f, 0.8f), U(3.6f, 6f), 900, 0.8f,
                    (i & 1) == 0 ? Back : Front);
            for (int i = 0; i < 2; i++) DaVun(dat + new Vector2(U(-8, 8), -4), new Vector2(U(-120, 120), -U(200, 340)) * sc, U(0.4f, 0.6f), U(2.4f, 3.6f));
        }

        // SÓNG ĐẤT chạy trên mặt đất: một cung của vòng elip nằm trên đất, tâm ở chỗ dậm, phần cung hướng về đối thủ (dày giữa thuôn hai đầu), bán
        // kính lớn dần tới chân đối thủ đúng lúc toi nên cung nở rộng theo quãng, mỏng dần; tới nơi thì bẹt ra tan. Lớp đất, không viền mực (không
        // che ai). Hai màu: lục giữa (thân), vàng chanh (sát mép trước).
        const float SongDatDet = 0.34f; // độ dẹt của mặt đất
        P SongDat(Vector2 tu, Vector2 den, float toi, float day0)
        {
            var d = den - tu;
            var dk = new Vector2(d.x, d.y / SongDatDet); // hướng và quãng trên mặt đất "trải phẳng"
            var p = new P { pos = tu, home = tu, aim = Unit(dk), R1 = dk.magnitude, life = toi + 0.12f, tb = toi, wd = day0, stops = W, group = Floor };
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                float f = Mathf.Clamp01(t / q.tb);
                float R = Mathf.Max(8, q.R1 * f), day = q.wd * (1 - 0.4f * f), span = 0.9f + 0.25f * f, a = Mathf.Min(1, t / 0.04f);
                if (t > q.tb)
                {
                    float u = (t - q.tb) / Mathf.Max(0.02f, q.life - q.tb);
                    span *= 1 + 0.4f * u;
                    day *= 1 - u;
                    a *= 1 - u;
                }
                if (a < 0.03f || day < 0.8f) return;
                MLiem(Floor, 32, q.home, q.aim, R, Mathf.Min(day, 0.8f * R), span, q.stops[2], MocChanh, 0.92f * a, 0, SongDatDet);
            };
            return Add(p);
        }

        // DẬM RỪNG (chiêu cuối): xem đầu file. Trả giờ tới lúc rễ và cột lá trồi dưới chân đối thủ.
        // manh: độ mạnh theo dạng (dạng cuối 1; dạng đầu 0,7: ít lá hơn, ba cột, không có rễ trồi).
        public float NDamRung(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh = 1)
        {
            MocSang();
            float L = Mathf.Max(0.5f, lead);
            float tG = Mathf.Max(0.05f, L - 0.87f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var truoc = casterFeet + new Vector2(dir * 0.36f * casterH, 0); // chỗ hai chân trước dậm xuống
            var lung = casterFeet + new Vector2(-dir * 0.08f * casterH, -0.62f * casterH); // giữa khối lá trên lưng
            // gồng: vòng dưới chân, lá quanh người cuốn xoáy bay lên, bụi chân sau. Khung vẽ sẵn (2026-11-19): một cột lốc năng lượng (loc) xoáy sau
            // lưng voi suốt lúc gồng, tắt dần ngay trước cú dậm; lá cuốn giữ lại nhưng thưa hơn; bụi chân sau là cụm khói nhuộm đất
            bool loc = HasFb("loc"), kh = HasFb("khoi");
            At(tG, () => CungDat(casterFeet + new Vector2(0, 2), 0.15f * casterH, 0.75f * casterH, 0.5f, W[2], 0.07f * casterH));
            if (loc) At(tG, () => MocLocFb(casterFeet + new Vector2(0, -2), (0.95f + 0.2f * manh) * casterH, L - 0.06f - tG));
            Every(tG, L - 0.12f, (loc ? 40 : 76) * manh, x =>
            {
                float a = U(0, 6.28f);
                float R = U(0.34f, 0.62f) * casterH;
                var from = casterFeet + new Vector2(Mathf.Cos(a) * R, Mathf.Sin(a) * R * 0.26f - U(0, 0.3f) * casterH);
                Leaf(from, new Vector2(-Mathf.Sin(a) * 200, -U(230, 400)), U(0.45f, 0.72f), U(4.5f, 7.5f), -140, 1.1f, Mathf.Sin(a) < 0 ? Back : Front);
            });
            Every(tG, L - 0.2f, kh ? 3 : 5, x =>
            {
                var at = casterFeet + new Vector2(-dir * U(0.1f, 0.4f) * casterH, U(-4, 2));
                if (kh) MocKhoiFb(at, U(0.07f, 0.09f) * casterH, new Vector2(-dir * U(20, 60), -U(30, 50)), Back, 3, 1.2f, 0.85f);
                else BuiCum(at, new Vector2(-dir * U(20, 70), -U(30, 60)), U(0.06f, 0.08f) * casterH, 0, Back);
            });
            // DẬM: vòng cung dẹt hai lớp, cụm bụi lớn tách dần, đất vụn, vết đất; lá trên lưng bung ra
            At(L, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(FlashW);
                CungDat(truoc + new Vector2(0, 2), 0.14f * casterH, 1.05f * casterH, 0.5f, CungC, 0.11f * casterH);
                CungDat(truoc + new Vector2(0, 2), 0.08f * casterH, 0.66f * casterH, 0.42f, W[2], 0.07f * casterH, 5);
                VetDat(truoc + new Vector2(0, 3), 0.55f * casterH, 1f);
                if (!MocBuiHaiBen(truoc, 0.16f * casterH, 0.28f * casterH, 170, true)) // khung vẽ sẵn: hai cụm khói nhuộm đất + một cụm giữa thay sáu cụm BuiCum
                    for (int i = 0; i < 6; i++)
                    {
                        float sd = i == 5 ? 0 : (i & 1) == 0 ? 1 : -1;
                        BuiCum(truoc + new Vector2(sd * U(0.08f, 0.34f) * casterH, U(-6, 3)), new Vector2(sd * U(90, 230), -U(15, 55)), U(0.11f, 0.16f) * casterH, 0,
                            i < 4 ? Back : Front);
                    }
                for (int i = 0; i < 7; i++) DaVun(truoc + new Vector2(U(-26, 26), -4), new Vector2(U(-230, 230), -U(240, 460)), U(0.5f, 0.8f), U(2.6f, 4.4f));
                for (int i = 0; i < 22; i++) // lá trên lưng bung ra theo cú dậm
                {
                    float a = 3.14f + 3.14f * (i + U(0, 0.8f)) / 22; // nửa trên
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Leaf(lung + d * U(0.18f, 0.34f) * casterH, d * U(190, 420) + new Vector2(dir * 60, 0), U(0.55f, 0.9f), U(4.2f, 7f), 560, 1.6f,
                        (i & 1) == 0 ? Back : Front);
                }
            });
            // sóng đất chạy tới đối thủ: bốn cột lá phụt lên dọc đường, cột sau to hơn
            int N = manh >= 1 ? 4 : 3;
            const float buoc = 0.07f;
            At(L + 0.02f, () => SongDat(truoc, foeFeet, buoc * (N + 1) - 0.02f, (0.16f + 0.06f * manh) * tH));
            for (int i = 0; i < N; i++)
            {
                int j = i;
                float f = 0.28f + 0.62f * j / (N - 1f);
                // gai của cột vẽ ở lớp TRƯỚC (thấy rõ, như hàng gai Cầu Gai); cột cuối sát chân đối thủ để lớp sau cho khỏi che thân nó
                At(L + buoc * (j + 1), () => CotLa(Vector2.Lerp(truoc, foeFeet, f), tH, (0.9f + 0.2f * j) * manh, Front)); // lớp TRƯỚC (người dùng 2026-11-19: "gai đất, nổ đang bị lỗi layer hiện đằng sau tướng địch")
            }
            float hit = L + buoc * (N + 1);
            // rễ trồi quanh chân đối thủ (dạng cuối). Khung vẽ sẵn (2026-11-19, người dùng chê "gai đâm lên xấu"): rễ nhọn nâu (Spike) thành gai lá có
            // thớ gỗ (gai_la, MocVongGai): ba cụm cao so le sau lưng, đủ cao để ló lên trên vai; lớp trước ba cụm thấy rõ (hai cụm to hai bên + một
            // cụm vừa chếch trước chân phía voi; người dùng xem trong game: bản đầu gai phần lớn ở sau lưng, bị thân che), không cụm cao nào ngay
            // trước mặt; đỉnh phóng lệch nhau quanh giờ trúng; start 4,5: khung nứt đất ngắn, hiện khi sóng đất gần tới nơi; giữ ~0,45 s rồi gãy
            bool gaiFb = manh >= 1 && HasFb("gai_la");
            if (gaiFb)
                MocVongGai(foeFeet, tH, hit, 0.44f, casterFeet.x < foeFeet.x ? -1 : 1, new[] { (-0.36f, 1.2f, 0.01f), (0.02f, 1.4f, 0.04f), (0.38f, 1.15f, 0.07f) });
            At(hit, () =>
            {
                Shake?.Invoke(0.9f);
                DanhTrung?.Invoke(foeBody, 0.8f);
                LaNo(foeBody, foeFeet, tH, 1.4f * manh);
                WExtra(foeBody, 7, 340);
                CungDat(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.9f * tH, 0.5f, CungC, 0.1f * tH);
                VetDat(foeFeet + new Vector2(0, 3), 0.5f * tH, 1f);
                if (!MocBuiHaiBen(foeFeet, 0.14f * tH, 0.32f * tH, 130)) // khung vẽ sẵn: hai cụm khói nhuộm đất thay bốn cụm BuiCum
                    for (int i = 0; i < 4; i++)
                    {
                        float sd = (i & 1) == 0 ? 1 : -1;
                        BuiCum(foeFeet + new Vector2(sd * U(0.12f, 0.42f) * tH, U(-6, 2)), new Vector2(sd * U(80, 170), -U(15, 45)), U(0.11f, 0.15f) * tH, 0, Back);
                    }
                if (!gaiFb && HasGai && manh >= 1) // rễ trồi quanh chân đối thủ: ba cái cao phía sau, hai cái thấp hai bên phía trước
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
            At(hit + 0.12f, () => BurstFlash(foeBody + new Vector2(0, -0.1f * tH), 0.48f * tH, Back, 0.16f));
            return hit;
        }

        // đòn đánh thường có hiệu ứng dù tướng LAO tới (không đứng bắn): StageView.AtkFx phát lúc clip attack bắt đầu
        public static bool AtkLao(string kind) => kind == "n_hat_nga" || kind == "n_tru_dap" || kind == "n_vuong_huc" || kind == "n_nham_va" || kind == "n_ho_va" || kind == "n_nui_huc" ||
            kind == "n_sat_tong" || kind == "n_giao_dam" || kind == "n_xich_go" || kind == "n_khoang_huc" || kind == "n_cua_huc" || kind == "n_hon_chem" || kind == "n_soi_go" ||
            kind == "n_giap_huc" || kind == "n_tich_dop" || kind == "n_thiem_giang" || kind == "n_long_vuot" || kind == "n_vien_dam" ||
            kind == "n_giap_huc2" || kind == "n_tich_dop2" || kind == "n_thiem_dam2" || kind == "n_long_vuot1" || // bộ Thổ (HatTho.cs; dạng 2, dạng 1 Sa Long)
            kind == "n_trung_dop" || // Sa Trùng (rig sau_dat_1)
            kind == "n_thach_vo" || // Thiên Thạch Thú (HatThach.cs, suất cu_phu)
            kind == "n_tinh_nen" || kind == "n_tinh_nen1"; // Thổ Tinh / Tiểu Thổ Tinh (HatThoTinh.cs, suất giap_nham)

        // HẤT NGÀ (đòn đánh thường, clip attack của voi_rung.py: cào đất lead − 0,40; chân sau đạp bật lead − 0,14; nện + hất ngà = lead):
        // bụi cào đất dưới chân trước, bụi và đất vụn bắn ra sau lúc chân sau đạp, lá trên lưng tuột lại phía sau lúc bay, tới nơi
        // chân trước nện: vòng bụi + bụi hai bên; chỗ ngà chạm thân đối thủ: chớp toé nhỏ, lá vỡ, bụi. Nhỏ hơn chiêu mana.
        public float NHatNga(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            // sân kéo đỉnh cú lao tới 72 % quãng tới đối thủ (AolaSticker.Lunge): thân đáp ở đó, hai chân trước nện xuống phía trước nó
            var toi = Vector2.Lerp(casterFeet, foeFeet, 0.72f);
            var truoc = toi + (foeFeet - casterFeet).normalized * 0.2f * casterH;
            var sau = casterFeet + new Vector2(-dir * 0.3f * casterH, 0); // chân sau
            // cào đất (khung vẽ sẵn 2026-11-19: một cụm khói nhuộm đất bị cào hất ra sau thay vài cụm BuiCum lấm tấm)
            bool kh = HasFb("khoi");
            if (L > 0.42f)
            {
                if (kh)
                    At(L - 0.4f, () => MocKhoiFb(casterFeet + new Vector2(dir * U(0.2f, 0.3f) * casterH, U(-3, 2)), 0.07f * casterH, new Vector2(-dir * U(90, 160), -U(15, 35)),
                        Back, 3, 1.35f, 0.85f));
                else
                    Every(L - 0.42f, L - 0.3f, 12, x =>
                        BuiCum(casterFeet + new Vector2(dir * U(0.22f, 0.34f) * casterH, U(-4, 2)), new Vector2(-dir * U(90, 190), -U(20, 50)), U(0.05f, 0.07f) * casterH, 0, Back));
            }
            // chân sau đạp bật
            At(Mathf.Max(0.02f, L - 0.14f), () =>
            {
                Shake?.Invoke(0.25f);
                CungDat(sau + new Vector2(0, 2), 0.06f * casterH, 0.42f * casterH, 0.36f, CungC, 0.06f * casterH, 3);
                if (kh) // khung vẽ sẵn: hai cụm khói nhuộm đất bắn ra sau thay ba cụm BuiCum
                    for (int i = 0; i < 2; i++)
                        MocKhoiFb(sau + new Vector2(-dir * U(4, 18), U(-4, 2)), U(0.11f, 0.14f) * casterH, new Vector2(-dir * U(120, 240), -U(20, 60)), Back, U(3.5f, 4.5f));
                else
                    for (int i = 0; i < 3; i++)
                        BuiCum(sau + new Vector2(U(-14, 14), U(-5, 2)), new Vector2(-dir * U(120, 260), -U(30, 90)), U(0.09f, 0.13f) * casterH, 0, i < 2 ? Back : Front);
                for (int i = 0; i < 4; i++) DaVun(sau + new Vector2(U(-10, 10), -4), new Vector2(-dir * U(120, 260), -U(180, 320)), U(0.4f, 0.6f), U(2.6f, 3.8f), Back);
            });
            // đang bay: lá tuột lại phía sau
            float t0 = Mathf.Max(0.02f, L - 0.12f);
            float goc = T;
            Every(t0, L, 60, x =>
            {
                float k = Mathf.Clamp01((T - goc - t0) / Mathf.Max(0.02f, L - t0));
                var at = Vector2.Lerp(casterFeet, toi, k) + new Vector2(-dir * U(0, 0.3f) * casterH, -U(0.45f, 0.95f) * casterH);
                Leaf(at, new Vector2(-dir * U(60, 180), U(-90, 30)), U(0.35f, 0.6f), U(3.8f, 6.2f), 420, 1.4f, U(0, 1) < 0.6f ? Back : Front);
            });
            // nện + hất ngà
            At(L, () =>
            {
                Shake?.Invoke(0.35f);
                CungDat(toi + new Vector2(0, 2), 0.1f * casterH, 0.56f * casterH, 0.4f, CungC, 0.07f * casterH);
                if (!MocBuiHaiBen(Vector2.Lerp(toi, truoc, 0.5f), 0.12f * casterH, 0.26f * casterH, 150)) // khung vẽ sẵn: hai cụm khói nhuộm đất thay bốn cụm BuiCum
                    for (int i = 0; i < 4; i++)
                    {
                        float sd = (i & 1) == 0 ? 1 : -1;
                        var goc2 = i < 2 ? truoc : toi;
                        BuiCum(goc2 + new Vector2(sd * U(6, 0.3f * casterH), U(-5, 3)), new Vector2(sd * U(100, 220), -U(15, 45)), U(0.09f, 0.13f) * casterH, 0, Back);
                    }
                for (int i = 0; i < 4; i++) DaVun(truoc + new Vector2(U(-12, 12), -4), new Vector2(U(-150, 150), -U(190, 330)), U(0.4f, 0.6f), U(2.6f, 3.8f), Back);
                // chỗ ngà hất: chớp toé + lá bật khỏi đối thủ theo hướng hất (lên và ra xa con đánh). Không đặt bụi ở đây: con đánh
                // đang đè lên đối thủ, bụi sẽ dính lên mặt nó
                var cham = foeBody + new Vector2(dir * 0.15f * tH, -0.1f * tH); // phía mũi ngà, qua khỏi mặt con đánh
                DanhTrung?.Invoke(cham, 0.6f);
                Chop(cham, 0.34f * tH, 0.07f);
                BurstFlash(cham, 0.46f * tH, Back, 0.16f);
                for (int i = 0; i < 10; i++)
                {
                    float a = dir * 0.55f + (i - 4.5f) * 0.3f + U(-0.12f, 0.12f); // góc tính từ phương thẳng lên, ngả theo hướng hất
                    var d = new Vector2(Mathf.Sin(a), -Mathf.Cos(a));
                    Leaf(cham + d * U(6, 14), d * U(200, 380), U(0.45f, 0.75f), U(3.6f, 5.8f), 640, 2f);
                }
            });
            return L;
        }
    }
}
