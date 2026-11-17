// Bùn Ngoạm (2026-11-17): quái bùn, suất ho_kim_cuong (ải 50 "Vách Kim Cương" đảo Thổ, thay hình Hổ Kim Cương; giữ id, thẻ, chỉ số).
// Rig quai_bun_1 (ArtGen/Spine/quai_bun_rig.py; ghi chú ArtGen/Spine/inbox/quai_bun_ghichu.md mục 11 "Vào game"; script đưa vào game
// ArtGen/Spine/quai/doi_quai_bun.py). Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc): phát lúc clip BẮT ĐẦU kèm lead = giờ trúng của
// clip; mọi mốc dưới đây là giây của rig, co giãn theo k = lead / khung trúng của rig. Lớp hạt không đọc xương nên vai, chỗ tay cắm, đáy nắm
// đấm, tâm quả bóng, miệng, mũi 22 gai và quãng xương move đo sẵn trên rig (đơn vị chiều cao dáng đứng; x về phía đối thủ, y lên).
// - Đòn thường "Đấm bùn" (rig khai stay + far, tay co giãn tới đúng đối thủ): giọt bùn rơi theo cánh tay vươn / giữ / rút; trúng: toé bùn,
//   cục bùn văng, chớp sao kem nhỏ.
// - Chiêu mana "Đấm Bùn Trồi": tay cắm xuống bùn (toé, vương miện bùn, vòng bụi); gò bùn + vết nứt chạy ngầm tới chỗ nắm đấm; NẮM ĐẤM BÙN
//   KHỔNG LỒ của rig trồi (bùn đá văng, ba vết nứt, rung); trúng; nắm đấm lún (toé nhỏ).
// - Chiêu cuối "Nuốt Chửng" (rig khai lunge): bụi + bùn lúc bật nhảy; giọt bùn rớt khỏi hàm khổng lồ giữa không trung; NGOẠM: toé bùn lớn che
//   lúc đối thủ biến mất (StageView giấu nó tới lúc nhổ, StageViewNuot.cs); phụt bùn đổi thành quả bóng, bụi chỗ bóng rơi; bóng quẫy (bùn bắn
//   khỏi chỗ bụng lồi); 22 gai đâm xuyên (bụi đá ở mũi từng gai; khung trúng ở đợt một); rút gai; phụt bùn hiện lại; ọe; NHỔ: bùn phun khỏi
//   hàm (vệt bùn bám theo đối thủ bay về chỗ: StageView gọi BunNhoBay); bùn rớt lúc bay lùi; đáp.
// - Ra sân (StageViewNuot.RaSanFx): cục đất chạm đất hai lần (toé đất), bung thành tướng (phụt bùn).
// Hình hệ Thổ (skill-petclash mục 5) + chất bùn: cục bùn tròn méo, giọt bùn kéo theo hướng bay, chạm đất bẹp thành vết bùn rồi mờ (không nảy
// như sỏi); đá xám (gai, nắm đấm) văng thì nảy một lần rồi nằm; bụi tròn be. Màu bùn lấy theo chân dung (sô-cô-la, bụng nâu sáng).
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // ---- mốc rig (giây clip) ----
        const float BunDanhT = 0.50f, BunVuon = 0.42f, BunRut = 0.78f, BunRutXong = 0.92f;                  // attack 1,30
        const float BunTroiT = 0.84f, BunCam = 0.60f, BunTroi = 0.74f, BunLun = 1.04f;                       // cast 1,70
        const float BunNgoamT = 1.94f, BunLao = 0.42f, BunHa = 0.56f, BunCap = 0.92f, BunPhong = 0.99f,      // skill 4,30
            BunGiay = 1.24f, BunGiay2 = 1.72f, BunDam = 1.78f, BunDam2 = 2.16f, BunRutGai = 2.72f, BunHien = 3.00f, BunOe = 3.12f,
            BunNho = 3.47f, BunVe = 3.54f, BunDap = 3.90f;

        // ---- điểm đo trên rig ----
        static readonly Vector2 BunVai = new Vector2(0.27f, 0.52f);        // gốc tay co giãn (attack)
        static readonly Vector2 BunCamP = new Vector2(0.60f, 0f);          // chỗ tay cắm xuống bùn (cast 0,60)
        const float BunDayNam = 0.583f;                                    // đáy nắm đấm khổng lồ (xương nam_ngam) dưới xương far
        static readonly Vector2 BunBong = new Vector2(0.133f, 0.45f);      // tâm quả bóng so với xương move
        const float BunR = 0.47f;                                          // bán kính quả bóng
        static readonly Vector2 BunMiengTo = new Vector2(0.217f, 0.634f);  // lòng hàm khổng lồ lúc nhổ (so với move)
        static readonly Vector2 BunHam = new Vector2(0.26f, 0.66f);        // lòng hàm khổng lồ lúc lao, há (so với move)
        static readonly Vector2 BunMieng = new Vector2(0.18f, 0.28f);      // miệng thường lúc ọe (so với move)
        // xương move của skill (giây, x, y): bật nhảy 0,42, tới đích 0,80–0,99, đứng ở đích tới 3,44, bay lùi 3,54 → 3,90
        static readonly float[] BunMoveB =
        {
            0f, 0f, 0f, 0.20f, -0.023f, 0f, 0.42f, -0.047f, 0.011f, 0.50f, 0.062f, 0.113f, 0.56f, 0.257f, 0.183f, 0.66f, 0.675f, 0.238f,
            0.74f, 0.991f, 0.212f, 0.80f, 1.161f, 0.156f, 0.86f, 1.223f, 0.086f, 0.92f, 1.226f, 0.060f, 0.99f, 1.226f, 0.008f, 1.10f, 1.226f, 0f,
            3.44f, 1.221f, 0.006f, 3.47f, 1.201f, 0.034f, 3.50f, 1.184f, 0.058f, 3.54f, 1.143f, 0.073f, 3.65f, 0.570f, 0.151f,
            3.75f, 0.207f, 0.150f, 3.90f, 0f, 0f,
        };
        const float BunMoveMax = 1.226f;                                   // đỉnh lao của rig (sân nắn về 72 % quãng tới đối thủ)
        // 22 gai đâm từ tâm bóng (giây trồi, góc độ, độ dài tới mũi): đợt một 10 gai dài, đợt hai 12 gai ngắn xen giữa; rút cùng lúc 2,72
        static readonly float[] BunGaiB =
        {
            1.80f, 61, 0.85f, 1.84f, 15, 0.74f, 1.87f, 126, 0.85f, 1.90f, 107, 0.64f, 1.94f, 31, 0.85f, 1.97f, 174, 0.74f, 2.00f, -11, 0.63f,
            2.04f, 48, 0.74f, 2.07f, 141, 0.84f, 2.11f, 111, 0.62f,
            2.18f, -22, 0.50f, 2.20f, 14, 0.63f, 2.24f, 153, 0.48f, 2.24f, 75, 0.70f, 2.27f, 166, 0.61f, 2.30f, 38, 0.52f, 2.31f, 118, 0.66f,
            2.34f, -14, 0.62f, 2.37f, 165, 0.55f, 2.37f, 69, 0.58f, 2.40f, -154, 0.45f, 2.44f, 132, 0.66f,
        };

        // ---- màu bùn (theo chân dung: sô-cô-la, bụng nâu sáng) ----
        static readonly Color BunSam = C(96, 52, 30), BunC = C(140, 82, 50), BunSang = C(186, 128, 82), BunKem = C(222, 180, 128);
        static readonly Color[] BunW = { Ink, BunSam, BunC, BunSang, BunKem };

        // ================= vật liệu bùn =================

        static Vector2 BunMoveAt(float t)
        {
            var b = BunMoveB;
            int n = b.Length / 3;
            if (t <= b[0]) return new Vector2(b[1], b[2]);
            for (int i = 1; i < n; i++)
                if (t <= b[3 * i])
                {
                    float f = (t - b[3 * i - 3]) / Mathf.Max(1e-4f, b[3 * i] - b[3 * i - 3]);
                    return Vector2.Lerp(new Vector2(b[3 * i - 2], b[3 * i - 1]), new Vector2(b[3 * i + 1], b[3 * i + 2]), f);
                }
            return new Vector2(b[3 * n - 2], b[3 * n - 1]);
        }

        // chỗ xương move của chiêu cuối trên sân ở giây clip t (chép AolaSticker.Lunge: quãng lao của rig xoay + co cho đỉnh rơi vào 72 % quãng)
        static Vector2 BunThan(Vector2 feet, Vector2 foeFeet, float H, float dir, float t)
        {
            var m = BunMoveAt(t);
            var T = (foeFeet - feet) * 0.72f;
            float M = BunMoveMax * H;
            if (M < 1 || T.sqrMagnitude < 1) return feet;
            float k = T.magnitude / M, ang = Mathf.Atan2(T.y, T.x) - Mathf.Atan2(0, dir * M);
            float cs = Mathf.Cos(ang) * k, sn = Mathf.Sin(ang) * k, mx = dir * m.x * H, my = -m.y * H;
            return feet + new Vector2(mx * cs - my * sn, mx * sn + my * cs);
        }

        // vết bùn bẹt trên đất: nở nhanh, nằm, mờ (lớp đất)
        void BunVet(Vector2 pos, float r, Color col)
        {
            var p = new P { pos = pos + new Vector2(0, 1), life = U(0.5f, 0.75f), group = Floor, seed = rng.Next(4), sz = r, col = col, ang = U(-10, 10) };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (0.55f + 0.45f * Mathf.Min(1, q.age / 0.06f)) * (1 - 0.25f * SmoothStep(0.6f, 1, k));
                float a = 1 - SmoothStep(0.55f, 1, k);
                if (s < 1 || a < 0.03f) return;
                int si = q.seed & 3;
                float h = 0.8f * s, w = 2.3f * s;
                Put(buf, Floor, 6, S("solid_" + si), Ink, q.pos, h + 3, (w + 3) / (h + 3), q.ang, a);
                Put(buf, Floor, 6.1f, S("blob_" + si), q.col, q.pos, h, w / h, q.ang, a);
            };
            Add(p);
        }

        // giọt bùn: giọt lệ kéo theo hướng bay (ảnh giọt nhuộm bùn), rơi, chạm đất bẹp thành vết bùn
        void DrawBunGiot(P p, float k, List<Item> buf)
        {
            float s = 2.4f * p.sz * (1 - SmoothStep(0.85f, 1, k));
            if (s < 1) return;
            float sp = p.vel.magnitude;
            var d = sp > 5 ? p.vel / sp : new Vector2(0, 1);
            float ang = TipAngle(-d);
            int i = p.seed & 3;
            Put(buf, p.group, 40, S("drops_" + i), Ink, p.pos, s + 4, 1, ang);
            Put(buf, p.group, 40.3f, S("drop_" + i), BunC, p.pos, s, 1, ang);
            Put(buf, p.group, 40.6f, S("drop_" + i), BunSang, p.pos + d * s * 0.12f, s * 0.48f, 1, ang);
        }

        P BunGiot(Vector2 pos, Vector2 vel, float r, float ground, int group = Front, float grav = 900)
        {
            var p = new P { pos = pos, vel = vel, life = 1.6f, drag = 0.6f, acc = new Vector2(0, grav), seed = rng.Next(4), sz = r, group = group, ground = ground };
            p.draw = DrawBunGiot;
            p.onGround = (q, s) =>
            {
                s.BunVet(q.pos, q.sz * 1.5f, BunSam);
                q.dead = true;
            };
            return Add(p);
        }

        // cục bùn: khối tròn méo viền mực (như sỏi), xoay, rơi; chạm đất bẹp thành vết bùn (không nảy)
        P BunCuc(Vector2 pos, Vector2 vel, float r, float ground, int group = Front, Color? col = null)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = 1.6f, acc = new Vector2(0, 950), drag = 0.5f, spin = U(-500, 500), spinDrag = 0.4f, ang = U(0, 360),
                seed = rng.Next(4), sz = r, col = col ?? (rng.Next(3) == 0 ? BunSam : BunC), group = group, ground = ground, hgt = U(1.0f, 1.35f)
            };
            p.draw = DrawSoiP;
            p.onGround = (q, s) =>
            {
                s.BunVet(q.pos, q.sz * 1.35f, q.col);
                q.dead = true;
            };
            return Add(p);
        }

        // toé bùn nhìn thẳng (ảnh nước toé nhuộm bùn, 5 lớp từ mực vào lõi), nở 0,6 đời rồi giữ, 0,16 s
        void BunToe(Vector2 c, float size, int group = Front, float life = 0.16f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = 2 + rng.Next(2), sz = size };
            p.draw = (q, k, buf) =>
            {
                float a = 1 - SmoothStep(0.75f, 1, k);
                for (int i = 0; i < 5; i++)
                    Put(buf, q.group, 33 + i * 0.1f, S((i == 0 ? "crowns_" : "crown_") + q.seed), BunW[i], q.pos,
                        q.sz * (0.6f + 0.5f * EaseOut(k / 0.6f)) * BurstF[i] + (i == 0 ? 5 : 0), 1, q.ang, a);
            };
            Add(p);
        }

        // vương miện bùn mọc từ đất rồi lún (đáy bám đất; ảnh vương miện nước nhuộm bùn)
        void BunVuong(Vector2 feet, float wd, float life = 0.42f, int group = Front)
        {
            var p = new P { pos = feet, life = life, group = group, seed = rng.Next(2), wd = wd };
            p.draw = (q, k, buf) =>
            {
                float g = k < 0.28f ? EaseOut(k / 0.28f) : 1 - SmoothStep(0.5f, 1, k);
                var f = CrownF[q.seed];
                for (int i = 0; i < 5; i++)
                {
                    float side = q.wd / f.x * (0.6f + 0.4f * WF[i]);
                    float hgt = side * g * Mathf.Sqrt(WF[i]);
                    if (hgt < 2) continue;
                    float ext = i == 0 ? 5 : 0;
                    Put(buf, q.group, 34 + i * 0.1f, S((i == 0 ? "crowns_" : "crown_") + q.seed), BunW[i], q.pos - new Vector2(0, f.y * hgt / 2),
                        hgt + ext, (side + ext) / (hgt + ext));
                }
            };
            Add(p);
        }

        // cú bùn trúng: toé bùn, cục bùn văng đều nửa trên quanh tâm rồi bẹp xuống đất, giọt bùn, chớp sao kem nhỏ. muc: 1 vừa, 2 nặng
        void BunNo(Vector2 c, float ground, float tH, float muc, bool chop = true)
        {
            float sc = tH / 150f;
            if (chop) ToChop(c, 0.2f * tH * Mathf.Sqrt(muc));
            BunToe(c, 0.42f * tH * Mathf.Sqrt(muc));
            int n = Mathf.RoundToInt(6 * muc);
            for (int i = 0; i < n; i++)
            {
                float a = -Mathf.PI / 2 + ((i + 0.5f) / n - 0.5f) * 2.8f + U(-0.18f, 0.18f);
                var v = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * (U(160, 280) * (0.8f + 0.25f * muc) * sc);
                BunCuc(c, v, U(3.5f, 6f) * (0.8f + 0.2f * muc) * sc, ground + U(-4, 8) * sc, (i & 1) == 0 ? Front : Back);
            }
            for (int i = 0; i < Mathf.RoundToInt(5 * muc); i++)
                BunGiot(c + U2(-6, 6) * sc, new Vector2(U(-230, 230), -U(120, 330)) * sc, U(2.6f, 4f) * sc, ground + U(-4, 8) * sc, (i & 1) == 0 ? Front : Back);
        }

        // phụt bùn quanh một khối tròn (đổi hình bóng ↔ tướng): cục bùn + giọt toả đều từ mép, bụi ở chân
        void BunPhut(Vector2 c, float R, float ground, float sH, float muc)
        {
            int n = Mathf.RoundToInt(9 * muc);
            for (int i = 0; i < n; i++)
            {
                float a = (i + U(-0.3f, 0.3f)) / n * 2 * Mathf.PI;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                if (d.y > 0.55f) d.y *= 0.4f;                                   // nửa dưới bẹt: ít bùn chui xuống đất
                var p0 = c + d * (R * 0.85f);
                BunCuc(p0, (d * U(170, 300) + new Vector2(0, -U(60, 140))) * sH, U(4, 7) * sH, ground + U(-4, 8) * sH, d.y < -0.2f ? Back : Front);
                if ((i & 1) == 0) BunGiot(p0, (d * U(220, 360) + new Vector2(0, -U(80, 180))) * sH, U(2.6f, 4f) * sH, ground + U(-4, 8) * sH);
            }
            for (int i = 0; i < 4; i++)
            {
                float s = (i & 1) == 0 ? -1 : 1;
                ToBui(new Vector2(c.x + s * U(0.4f, 0.9f) * R, ground - U(2, 10) * sH), new Vector2(s * U(50, 120), -U(20, 60)) * sH, 0, 7 * sH * muc,
                    17 * sH * muc, (i & 1) == 0 ? Back : Front);
            }
        }

        // bụi khi đáp / bật nhảy: vòng bụi dưới đất, cụm bụi lăn hai bên (hoặc về một phía), vài cục bùn
        void BunBui(Vector2 feet, float sH, float muc, float huong = 0)
        {
            ToVong(feet, 100 * sH * Mathf.Sqrt(muc), 0.5f);
            for (int i = 0; i < Mathf.RoundToInt(5 * muc); i++)
            {
                float s = huong != 0 ? huong : (i & 1) == 0 ? -1 : 1;
                ToBui(feet + new Vector2(s * U(0.05f, 0.4f) * 150 * sH, -U(2, 10) * sH), new Vector2(s * U(60, 160), -U(15, 60)) * sH, 0,
                    7 * sH * muc, 16 * sH * muc, (i & 1) == 0 ? Back : Front);
            }
            for (int i = 0; i < Mathf.RoundToInt(3 * muc); i++)
            {
                float s = huong != 0 ? huong : (i & 1) == 0 ? -1 : 1;
                BunCuc(feet + new Vector2(s * U(0, 0.25f) * 150 * sH, -6 * sH), new Vector2(s * U(80, 200), -U(160, 300)) * sH, U(3, 5) * sH,
                    feet.y + U(-2, 8) * sH, (i & 1) == 0 ? Back : Front);
            }
        }

        // gò bùn chạy ngầm từ a tới b trong (t0, t1): ụ bùn nâu (mảng liền viền mực) trượt dọc mặt đất, bụi + giọt bùn phía sau, vết nứt theo
        void BunGo(Vector2 a, Vector2 b, float t0, float t1, float sc)
        {
            float dur = Mathf.Max(0.05f, t1 - t0);
            At(t0, () =>
            {
                var p = new P { pos = a, life = dur, group = Front, sz = 1 };
                p.upd = (q, dt, s) =>
                {
                    float f = Mathf.Clamp01(q.age / dur);
                    q.pos = Vector2.Lerp(a, b, f * f * (3 - 2 * f));
                    q.vel = Vector2.zero;
                    if (s.U(0, 1) < 0.4f)
                        ToBui(q.pos + new Vector2(s.U(-14, 14) * sc, -4 * sc), new Vector2(-Mathf.Sign(b.x - a.x) * s.U(30, 90), -s.U(30, 80)) * sc, 0.45f,
                            5 * sc, 12 * sc, s.U(0, 1) < 0.5f ? Front : Back);
                    if (s.U(0, 1) < 0.3f)
                        BunGiot(q.pos + new Vector2(0, -8 * sc), new Vector2(s.U(-110, 110), -s.U(160, 300)) * sc, s.U(2.4f, 3.6f) * sc, q.pos.y + 3 * sc);
                };
                p.draw = (q, k, buf) =>
                {
                    float w = 34 * sc, h = 15 * sc * (0.6f + 0.4f * Mathf.Sin(q.age * 38));
                    const int n = 9;
                    int s0 = mp.Count;
                    for (int i = 0; i < n; i++)
                    {
                        float u = i / (n - 1f), ang = Mathf.PI * u;
                        mp.Add(q.pos + new Vector2(-Mathf.Cos(ang) * w, -Mathf.Sin(ang) * h - 2 * sc * Mathf.Sin(ang * 3 + q.age * 30)));
                    }
                    MSolid(Front, 23, s0, n, BunC, 1, 2.2f);
                };
                Add(p);
                ToNut(a, b, dur, sc);
            });
        }

        // ================= ĐÒN THƯỜNG "Đấm bùn" =================
        // tay bùn co giãn phóng 0,42 → 0,50 (game lái nắm đấm tới thân đối thủ = foeBody), giữ tới 0,78, rút về 0,92
        public float NBunDanh(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead), k = L / BunDanhT, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            var vai = ToSan(casterFeet, casterH, dir, BunVai);
            // phần cánh tay đã vươn (0..1 của quãng vai → nắm đấm) theo giờ rig
            Func<float, float> du = t => t < BunVuon ? 0 : t < BunDanhT ? Mathf.Lerp(0.45f, 1f, (t - BunVuon) / (BunDanhT - BunVuon)) :
                t < BunRut ? 1 : Mathf.Max(0, 1 - (t - BunRut) / (BunRutXong - BunRut));
            float t0 = BunVuon * k, t1 = BunRutXong * k;
            Every(t0, t1, x =>
            {
                float t = BunVuon + x * (BunRutXong - BunVuon);
                return t < BunDanhT + 0.03f ? 120 : t < BunRut ? 16 : 50;
            }, x =>
            {
                float t = BunVuon + x * (BunRutXong - BunVuon);
                float u = U(0.15f, Mathf.Max(0.2f, du(t)));
                var p = Vector2.Lerp(vai, foeBody, u) + new Vector2(0, U(-6, 6) * sH);
                BunGiot(p, new Vector2(U(-60, 60), -U(0, 90)) * sH, U(2.4f, 3.8f) * sH, Mathf.Lerp(casterFeet.y, foeFeet.y, u) + U(-3, 6) * sH);
            });
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.08f * tH, 0.02f * tH);
                BunNo(c, foeFeet.y, tH, 1.2f);
                ToVong(foeFeet, 65 * sc, 0.4f);
            });
            return L;
        }

        // ================= CHIÊU MANA "Đấm Bùn Trồi" =================
        // cắm tay 0,60; gò bùn chạy ngầm 0,60 → 0,74; nắm đấm khổng lồ (xương nam_ngam, con của far = thân đối thủ) trồi 0,74; trúng 0,84;
        // lún 1,04. Đáy nắm đấm = foeBody + 0,583 chiều cao tướng (dưới xương far).
        public float NBunTroi(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / BunTroiT, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            var cam = ToSan(casterFeet, casterH, dir, BunCamP);
            var day = foeBody + new Vector2(0, BunDayNam * casterH);
            At(BunCam * k, () =>
            {
                BunToe(cam + new Vector2(0, -0.08f * casterH), 0.42f * casterH, Front, 0.14f);
                BunVuong(cam, 0.55f * casterH, 0.36f);
                for (int i = 0; i < 6; i++)
                    BunGiot(cam + new Vector2(U(-10, 10), -6) * sH, new Vector2(U(-200, 200), -U(180, 340)) * sH, U(2.6f, 4f) * sH, cam.y + U(-3, 8) * sH);
                ToVong(cam, 80 * sH, 0.45f);
                Shake?.Invoke(0.15f);
            });
            BunGo(cam + new Vector2(dir * 0.1f * casterH, 0), day + new Vector2(-dir * 0.12f * tH, 0), BunCam * k, BunTroi * k, sH);
            At(BunTroi * k, () =>
            {
                BunVuong(day, 0.9f * casterH, 0.4f, Back);
                for (int i = 0; i < 8; i++)
                {
                    float a = -Mathf.PI / 2 + U(-1.1f, 1.1f);
                    var v = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(260, 460) * sH;
                    if ((i & 1) == 0) BunCuc(day + new Vector2(U(-0.2f, 0.2f) * casterH, -6 * sH), v, U(4, 7) * sH, day.y + U(-3, 8) * sH, (i & 2) == 0 ? Front : Back);
                    else ToSoi(day + new Vector2(U(-0.2f, 0.2f) * casterH, -6 * sH), v, U(4, 6.5f) * sH, i % 3 == 0 ? ToDa2 : ToDa, day.y + U(-3, 8) * sH, 0,
                        (i & 2) == 0 ? Front : Back);
                }
                for (int i = 0; i < 3; i++)
                {
                    float a = (i - 1) * 0.6f;
                    ToNut(day, day + new Vector2(Mathf.Sin(a) * 0.55f * casterH, 3 * sH), 0.12f, sH);
                }
                BunBui(day, sH, 1.1f);
                Shake?.Invoke(0.22f);
            });
            At(L, () =>
            {
                var c = foeBody + new Vector2(0, 0.08f * tH);
                ToChop(c, 0.26f * tH);
                ToNo(c, foeFeet.y, tH, 1.2f, ToDa, BunC);
            });
            At(BunLun * k, () =>
            {
                BunToe(day + new Vector2(0, -0.06f * casterH), 0.32f * casterH, Back, 0.14f);
                for (int i = 0; i < 4; i++)
                    BunGiot(day + new Vector2(U(-0.15f, 0.15f) * casterH, -8 * sH), new Vector2(U(-150, 150), -U(140, 260)) * sH, U(2.6f, 3.8f) * sH,
                        day.y + U(-3, 8) * sH);
            });
            return L;
        }

        // ================= CHIÊU CUỐI "Nuốt Chửng" =================
        public float NBunNgoam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / BunNgoamT, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            Func<float, Vector2> than = t => BunThan(casterFeet, foeFeet, casterH, dir, t);        // chân (xương move) trên sân
            var dich = than(1.5f);                                                                // chỗ bóng đứng
            var bong = ToSan(dich, casterH, dir, BunBong);
            float R = BunR * casterH, dat = dich.y;
            // bật nhảy: bụi + bùn hất ra sau
            At(BunLao * k, () =>
            {
                BunBui(casterFeet, sH, 1f, -dir);
                Shake?.Invoke(0.1f);
            });
            // giọt bùn rớt khỏi hàm khổng lồ đang há giữa không trung
            Every(BunHa * k, (BunCap - 0.02f) * k, 30, x =>
            {
                float t = BunHa + x * (BunCap - 0.02f - BunHa);
                var m = than(t);
                float f = Mathf.Clamp01(BunMoveAt(t).x / BunMoveMax);
                var p = ToSan(m, casterH, dir, BunHam) + U2(-0.13f, 0.13f) * casterH;
                BunGiot(p, new Vector2(U(-50, 50), U(-40, 60)) * sH, U(2.6f, 4.2f) * sH, Mathf.Lerp(casterFeet.y, dat, f) + U(-3, 8) * sH);
            });
            // NGOẠM: hàm sập lên đối thủ (StageView giấu nó từ đây): toé bùn lớn che chỗ nó biến mất, chớp cắn
            At(BunCap * k, () =>
            {
                ToChop(foeBody, 0.3f * tH);
                BunToe(foeBody, 0.85f * tH, Front, 0.2f);
                BunNo(foeBody, foeFeet.y, tH, 1.6f, false);
                Shake?.Invoke(0.22f);
            });
            // phụt bùn đổi thành quả bóng; bóng rơi chạm đất
            At(BunPhong * k, () =>
            {
                BunPhut(bong, R, dat, sH, 1f);
                BunBui(new Vector2(bong.x, dat), sH, 1.2f);
                Shake?.Invoke(0.18f);
            });
            // quẫy trong bụng: bùn bắn khỏi chỗ bụng lồi
            Every(BunGiay * k, BunGiay2 * k, 9, _ =>
            {
                float a = U(-200, 20) * Mathf.Deg2Rad;
                var d = new Vector2(dir * Mathf.Cos(a), -Mathf.Sin(a));
                var p0 = bong + d * R * 0.92f;
                for (int i = 0; i < 2; i++)
                    BunGiot(p0, (d * U(120, 220) + new Vector2(0, -U(60, 150))) * sH, U(2.4f, 3.6f) * sH, dat + U(-3, 8) * sH, d.y < -0.3f ? Back : Front);
            });
            // 22 gai đâm xuyên: bụi đá + sỏi bắn ở mũi mỗi gai, dăm bùn ở chân gai (mặt bóng)
            for (int g = 0; g < BunGaiB.Length / 3; g++)
            {
                float tg = BunGaiB[3 * g], deg = BunGaiB[3 * g + 1], rg = BunGaiB[3 * g + 2];
                At(tg * k, () =>
                {
                    float a = deg * Mathf.Deg2Rad;
                    var d = new Vector2(dir * Mathf.Cos(a), -Mathf.Sin(a));
                    var mui = bong + d * rg * casterH;
                    int grp = d.y < -0.25f ? Back : Front;
                    ToBui(mui, d * 60 * sH + new Vector2(0, -20 * sH), 0.45f, 4 * sH, 11 * sH, grp);
                    ToSoi(mui, (d * U(160, 260) + new Vector2(0, -U(40, 120))) * sH, U(2.6f, 4f) * sH, (g & 1) == 0 ? ToDa : ToDa3, dat + U(-3, 8) * sH, 0, grp);
                    if ((g & 1) == 0) BunGiot(bong + d * R, (d * U(120, 200) + new Vector2(0, -60)) * sH, U(2.2f, 3.2f) * sH, dat + U(-3, 8) * sH, grp);
                });
            }
            At(BunDam * k, () => Shake?.Invoke(0.16f));
            At(BunDam2 * k, () => Shake?.Invoke(0.16f));
            // khung trúng (đợt gai một): chớp sao kem + dăm đá nổ ngay giữa bóng (đối thủ trong bụng bị đâm)
            At(L, () =>
            {
                ToChop(bong + new Vector2(0, -0.1f * casterH), 0.34f * tH);
                ToNo(bong, dat, tH, 1.4f, ToDa, ToDa3);
            });
            // rút gai: bụi nhỏ chỗ chân gai
            At(BunRutGai * k, () =>
            {
                for (int i = 0; i < 7; i++)
                {
                    float a = U(-200, 20) * Mathf.Deg2Rad;
                    var d = new Vector2(dir * Mathf.Cos(a), -Mathf.Sin(a));
                    ToBui(bong + d * R, d * 40 * sH, 0.4f, 4 * sH, 10 * sH, d.y < -0.25f ? Back : Front);
                }
            });
            // thôi làm bóng, hiện lại còn ngậm: phụt bùn
            At(BunHien * k, () =>
            {
                BunPhut(bong, R, dat, sH, 0.9f);
                Shake?.Invoke(0.12f);
            });
            // ọe hai cơn: giọt bùn rớt khỏi miệng
            for (int j = 0; j < 2; j++)
                At((BunOe + 0.13f * j) * k, () =>
                {
                    var mi = ToSan(than(BunOe), casterH, dir, BunMieng);
                    for (int i = 0; i < 4; i++)
                        BunGiot(mi, new Vector2(dir * U(40, 140), -U(40, 140)) * sH, U(2.4f, 3.4f) * sH, dat + U(-3, 8) * sH);
                });
            // NHỔ: bùn phun khỏi hàm khổng lồ về phía đối thủ bị nhổ (vệt bùn theo nó: BunNhoBay)
            At(BunNho * k, () =>
            {
                var mi = ToSan(than(BunNho), casterH, dir, BunMiengTo);
                BunToe(mi, 0.5f * casterH, Front, 0.16f);
                for (int i = 0; i < 12; i++)
                {
                    float a = U(-0.9f, 0.35f);                                                     // từ ngang tới chếch lên, về phía trước
                    var v = new Vector2(dir * Mathf.Cos(a), Mathf.Sin(a)) * U(220, 420) * sH;
                    BunGiot(mi, v, U(2.6f, 4.2f) * sH, dat + U(-3, 10) * sH);
                }
                for (int i = 0; i < 4; i++)
                    BunCuc(mi, new Vector2(dir * U(120, 300), -U(80, 220)) * sH, U(3.5f, 5.5f) * sH, dat + U(-3, 10) * sH);
                Shake?.Invoke(0.2f);
            });
            // bay lùi: bùn rớt khỏi thân
            Every(BunVe * k, (BunDap - 0.04f) * k, 22, x =>
            {
                float t = BunVe + x * (BunDap - 0.04f - BunVe);
                var m = than(t);
                float f = Mathf.Clamp01(BunMoveAt(t).x / BunMoveMax);
                BunGiot(m + new Vector2(U(-0.3f, 0.3f), -U(0.15f, 0.5f)) * casterH, new Vector2(-dir * U(20, 80), U(-60, 20)) * sH, U(2.4f, 3.6f) * sH,
                    Mathf.Lerp(casterFeet.y, dat, f) + U(-3, 8) * sH);
            });
            // đáp về chỗ
            At(BunDap * k, () =>
            {
                BunBui(casterFeet, sH, 1.1f);
                Shake?.Invoke(0.14f);
            });
            return L;
        }

        // Đối thủ bị NHỔ bay theo cung (StageView lái, StageViewNuot.cs): vệt giọt bùn rớt theo thân nó suốt quãng bay, tới chân thì đáp:
        // vết bùn, vòng bụi, bụi, cục bùn. than(u): giữa thân đối thủ ở phần quãng u (0..1); dur: giây bay; feet: chỗ đáp.
        public void BunNhoBay(Func<float, Vector2> than, float dur, Vector2 feet, float tH)
        {
            if (!Ready) return;
            float sc = tH / 150f, d0 = Mathf.Max(0.1f, dur);
            float t0 = T;
            Every(0, d0 * 0.92f, 34, _ =>
            {
                float u = Mathf.Clamp01((T - t0) / d0);
                var p = than(u) + U2(-0.18f, 0.18f) * tH;
                BunGiot(p, new Vector2(U(-60, 60), U(-80, 20)) * sc, U(2.4f, 3.8f) * sc, feet.y + U(-3, 8) * sc, U(0, 1) < 0.6f ? Front : Back);
            });
            At(d0, () =>
            {
                BunVet(feet, 26 * sc, BunSam);
                BunBui(feet, sc, 1f);
                for (int i = 0; i < 4; i++)
                    BunGiot(feet + new Vector2(U(-0.2f, 0.2f) * tH, -0.1f * tH), new Vector2(U(-160, 160), -U(120, 240)) * sc, U(2.4f, 3.4f) * sc,
                        feet.y + U(-2, 8) * sc);
                Shake?.Invoke(0.12f);
            });
        }

        // RA SÂN (clip appear của rig quai_bun_1; StageViewNuot.RaSanFx gọi đúng lúc sự kiện qua): "nay" cục đất chạm đất (toé đất, bụi), "bung"
        // cục đất bung thành tướng (phụt bùn quanh thân). feet: chân tướng; H: chiều cao tướng trên sân; dir: hướng mặt (+1 phải)
        public void BunRaSan(string ev, Vector2 feet, float H, float dir)
        {
            if (!Ready) return;
            float sH = H / 150f;
            var cuc = ToSan(feet, H, dir, new Vector2(0.133f, 0.27f));                          // tâm cục đất lúc chạm đất (xương cuc)
            if (ev == "nay")
            {
                BunVet(feet + new Vector2(dir * 0.13f * H, 0), 30 * sH, BunSam);
                ToVong(feet + new Vector2(dir * 0.13f * H, 0), 85 * sH, 0.45f);
                for (int i = 0; i < 5; i++)
                {
                    float s = (i & 1) == 0 ? -1 : 1;
                    ToSoi(feet + new Vector2(dir * 0.13f * H + s * U(0.05f, 0.25f) * H, -4 * sH), new Vector2(s * U(80, 200), -U(140, 300)) * sH,
                        U(2.6f, 4.2f) * sH, i % 3 == 0 ? ToCatSam : BunC, feet.y + U(-2, 8) * sH, 0, (i & 1) == 0 ? Front : Back);
                }
                for (int i = 0; i < 3; i++)
                {
                    float s = (i & 1) == 0 ? -1 : 1;
                    ToBui(feet + new Vector2(dir * 0.13f * H + s * U(0.1f, 0.3f) * H, -4 * sH), new Vector2(s * U(50, 120), -U(15, 50)) * sH, 0, 6 * sH,
                        15 * sH, (i & 1) == 0 ? Back : Front);
                }
            }
            else if (ev == "bung")
            {
                BunToe(cuc, 0.7f * H, Front, 0.14f);
                BunPhut(cuc, 0.3f * H, feet.y, sH, 1.1f);
            }
        }
    }
}
