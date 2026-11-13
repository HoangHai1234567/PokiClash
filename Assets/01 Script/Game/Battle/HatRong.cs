// Bộ của RỒNG TRÚC bốn cánh, boss cuối đảo Mộc (2026-11-13, suất thanh_long; rig ArtGen/Spine/moc_vuong_rig.py, clip trên rig monster_3709).
// Người dùng: đánh thường "dậm 2 chân trước thật mạnh, tạo địa chấn cùng sấm sét vào đầu đối thủ (fx làm riêng)"; chiêu mana "hét mạnh,
// shake cam, tạo ra những đợt sóng âm cực mạnh"; chiêu cuối "animation thật epic, hoành tráng, fx thật đẹp" (Claude tự quyết: VẠN DIỆP).
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes.
// Mốc của clip (moc_vuong_rig.py):
//   attack (skill_04 của họ): chồm dựng lead − 0,63; hai chân trước DẬM lead − 0,22; sét giáng = lead (1,15 s); gầm sau đó.
//   cast (skill_02_1): lấy hơi lead − 0,42; há mồm GẦM = lead (0,62 s), giữ gầm tới lead + 0,63.
//   skill (skill_05 + skill_03): sấp xoè cánh lead − 1,65; dựng cánh gầm lead − 1,28; khép cánh thành kén lead − 0,82; kén BUNG lead − 0,55;
//   QUẠT CÁNH = lead (2,02 s); sập cánh quét xuống lead + 0,50.
// Không quầng sáng, không cộng sáng: sét và sóng âm là hình phẳng có viền mực. Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs
// lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color SetC = C(255, 224, 92), SetLoi = C(255, 250, 222); // sét: vàng, lõi kem
        static readonly Color AmC = C(250, 246, 226); // sóng âm: kem
        static readonly Color FlashSet = new Color(1f, 0.97f, 0.8f, 0.34f);

        public const float RongGamDur = 0.6f; // chiêu gầm: sóng âm phát chừng này giây kể từ lúc há mồm

        // ---------- SÉT: một tia gấp khúc từ trên trời xuống điểm dich; hiện đậm 2–3 khung rồi mảnh dần; đổi dáng một lần giữa chừng ----------
        void DrawSet(P q, float k, List<Item> buf)
        {
            float a = k < 0.3f ? 1 : 1 - SmoothStep(0.3f, 1, k);
            if (a < 0.05f) return;
            float day = q.wd * (k < 0.3f ? 1 : 0.35f + 0.65f * (1 - SmoothStep(0.3f, 1, k)));
            var rnd = new System.Random(q.seed * 7919 + (k > 0.42f ? 17 : 0)); // đổi dáng một lần: sét là chuyển động, không là ảnh tĩnh
            var tu = q.home;
            int n = q.span;
            var truoc = tu;
            var huong = q.pos - tu;
            var nrm = Unit(new Vector2(-huong.y, huong.x));
            for (int i = 1; i <= n; i++)
            {
                float f = i / (float)n;
                var p = Vector2.Lerp(tu, q.pos, f);
                if (i < n) p += nrm * ((float)rnd.NextDouble() * 2 - 1) * q.sz * (0.55f + 0.45f * Mathf.Sin(f * 3.14f));
                var d = p - truoc;
                float dai = d.magnitude * 1.16f;
                var tam = (p + truoc) * 0.5f;
                var u = Unit(d);
                LaLieu(buf, q.group, 47, true, Ink, tam, u, dai + 7, day + 6, a);
                LaLieu(buf, q.group, 47.3f, false, SetC, tam, u, dai, day, a);
                LaLieu(buf, q.group, 47.6f, false, SetLoi, tam, u, dai * 0.84f, day * 0.42f, a);
                if (q.big && (i == 2 || i == n - 2)) // hai nhánh con rẽ ra
                {
                    var r2 = nrm * ((i == 2 ? 1 : -1) * q.sz * 1.5f) + huong.normalized * q.sz * 1.3f;
                    var t2 = truoc + r2 * 0.5f;
                    LaLieu(buf, q.group, 46.8f, true, Ink, t2, Unit(r2), r2.magnitude + 6, day * 0.55f + 5, a);
                    LaLieu(buf, q.group, 47.1f, false, SetC, t2, Unit(r2), r2.magnitude, day * 0.55f, a);
                }
                truoc = p;
            }
        }

        P Set(Vector2 tu, Vector2 dich, float day, float lech, float life = 0.22f, bool nhanh = true, int group = Front)
        {
            var p = new P { pos = dich, home = tu, life = life, wd = day, sz = lech, span = 7, seed = rng.Next(1000), big = nhanh, group = group };
            p.draw = DrawSet;
            return Add(p);
        }

        // sét giáng vào đầu đối thủ: tia chính + hai tia phụ lệch giờ, chớp toé, tia vụn văng, chớp màn
        void SetGiang(Vector2 dau, float tH, float manh)
        {
            var troi = dau + new Vector2(U(-0.25f, 0.25f) * tH, -2.3f * tH);
            Set(troi, dau, 0.085f * tH * manh, 0.2f * tH, 0.26f);
            At(0.07f, () => Set(troi + new Vector2(0.3f * tH, 0), dau + new Vector2(0.06f * tH, 0.05f * tH), 0.05f * tH * manh, 0.16f * tH, 0.16f, false));
            At(0.15f, () => Set(troi + new Vector2(-0.34f * tH, 0), dau + new Vector2(-0.07f * tH, 0.08f * tH), 0.042f * tH * manh, 0.15f * tH, 0.14f, false));
            FlashScreen?.Invoke(FlashSet);
            Shake?.Invoke(1f);
            BurstFlash(dau, 0.62f * tH * manh, Front, 0.16f);
            RingN(dau, 0.3f, 0.1f * tH, 0.62f * tH, SetC, 0.9f, Front, 36);
            for (int i = 0; i < 12; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / 12;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                var q = Spark(dau + d * U(4, 12), d, U(320, 620) * manh, U(0.16f, 0.3f), U(7, 11), 500, Front, 4);
                q.col = (i & 1) == 0 ? SetC : SetLoi;
            }
        }

        // một chỗ đất nứt bật lên trên đường địa chấn: đá vụn, bụi phụt, vòng đất nhỏ
        void DatNut(Vector2 dat, float tH, float sc)
        {
            Ripple(dat + new Vector2(0, 2), 0.04f * tH, 0.3f * tH * sc, 0.38f, BuiC2);
            for (int i = 0; i < 4; i++)
                Bui(dat + new Vector2(U(-12, 12) * sc, U(-4, 2)), new Vector2(U(-90, 90), -U(60, 150)) * sc, 0, 4, 12 * sc, (i & 1) == 0 ? Back : Front);
            int n = Mathf.RoundToInt(5 * sc);
            for (int i = 0; i < n; i++)
                DaVun(dat + new Vector2(U(-10, 10) * sc, -4), new Vector2(U(-130, 130), -U(260, 470)) * sc, U(0.4f, 0.65f), U(2.8f, 4.6f), (i & 1) == 0 ? Back : Front);
        }

        // ĐÒN ĐÁNH THƯỜNG: dậm hai chân trước → địa chấn chạy tới đối thủ → SÉT giáng vào đầu nó đúng khung trúng của clip.
        public float NRongDam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead);
            float tDam = Mathf.Max(0.05f, L - 0.22f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var truoc = casterFeet + new Vector2(dir * 0.2f * casterH, 0); // chỗ hai chân trước dậm xuống
            // chồm dựng: bụi dưới chân sau
            float tChom = Mathf.Max(0.02f, L - 0.63f);
            Every(tChom, tChom + 0.2f, 14, x =>
                Bui(casterFeet + new Vector2(-dir * U(0.05f, 0.3f) * casterH, U(-4, 2)), new Vector2(-dir * U(20, 80), -U(20, 70)), 0, 3, 8, Back));
            // DẬM
            At(tDam, () =>
            {
                Shake?.Invoke(0.9f);
                Ripple(truoc + new Vector2(0, 2), 0.1f * casterH, 0.8f * casterH, 0.5f, BuiC2);
                RingN(truoc + new Vector2(0, 2), 0.34f, 0.08f * casterH, 0.5f * casterH, BuiC, 0.3f, Floor, 30.6f);
                for (int i = 0; i < 12; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(truoc + new Vector2(sd * U(6, 36), U(-6, 3)), new Vector2(sd * U(120, 320), -U(15, 80)), U(0.45f, 0.8f), 5, U(10, 16), i < 8 ? Back : Front);
                }
                for (int i = 0; i < 8; i++) DaVun(truoc + new Vector2(U(-24, 24), -4), new Vector2(U(-220, 220), -U(240, 460)), U(0.45f, 0.75f), U(3f, 4.8f));
                for (int i = 0; i < 6; i++) Leaf(truoc + new Vector2(U(-20, 20), -U(4, 14)), new Vector2(U(-140, 140), -U(260, 420)), U(0.5f, 0.8f), U(4.5f, 7f), 700, 1.2f);
            });
            // địa chấn chạy tới đối thủ: ba chỗ đất nứt, cái sau to hơn
            for (int i = 0; i < 3; i++)
            {
                int j = i;
                At(tDam + 0.055f * (j + 1), () => DatNut(Vector2.Lerp(truoc, foeFeet, 0.26f + 0.3f * j), tH, 0.8f + 0.2f * j));
            }
            // SÉT giáng xuống đầu đối thủ + đất dưới chân nó bật lên
            var dau = foeBody + new Vector2(0, -0.42f * tH);
            At(L - 0.04f, () => Ripple(foeFeet + new Vector2(0, 2), 0.3f * tH, 0.06f * tH, 0.1f, SetC)); // vòng co lại báo trước một nhịp
            At(L, () =>
            {
                SetGiang(dau, tH, 1);
                DatNut(foeFeet, tH, 1.25f);
                WExtra(foeBody, 5, 300);
            });
            return L;
        }

        // ---------- SÓNG ÂM: một cung phẳng viền mực bay từ mồm tới đối thủ, nở to dần, mờ ở cuối ----------
        void DrawSongAm(P q, float k, List<Item> buf)
        {
            float a = Mathf.Min(1, k / 0.12f) * (1 - SmoothStep(0.72f, 1, k));
            if (a < 0.04f) return;
            float r = Mathf.Lerp(q.R0, q.R1, EaseOut(k));
            float ang = VelAng(q.aim) - 284.7f; // giữa cung của ảnh hat_arc_0 nằm ở góc 284,7 độ
            var tam = q.pos - q.aim * (r * 0.72f); // tâm vòng lùi lại để ĐỈNH cung nằm ở q.pos
            // "sóng âm cực mạnh": một DẢI dày chứ không phải một nét (ảnh cung mảnh): ba cung lồng sát nhau thành dải, mực viền hai mép
            Put(buf, q.group, 44, S("arcs_0"), Ink, tam, 2 * r + 7, 1, ang, a);
            Put(buf, q.group, 44, S("arcs_0"), Ink, tam, 2 * r * 0.88f - 7, 1, ang, a);
            for (int i = 0; i < 4; i++) Put(buf, q.group, 44.4f, S("arc_0"), q.col, tam, 2 * r * (1 - 0.04f * i), 1, ang, a);
        }

        P SongAm(Vector2 tu, Vector2 den, float r0, float r1, float v, Color col, int group = Front)
        {
            var d = den - tu;
            float life = d.magnitude / v + 0.12f;
            var p = new P { pos = tu, vel = Unit(d) * v, aim = Unit(d), life = life, R0 = r0, R1 = r1, col = col, group = group };
            p.draw = DrawSongAm;
            return Add(p);
        }

        // CHIÊU MANA: GẦM. Lấy hơi (lá, bụi bị hút vào mồm) → há mồm: các đợt sóng âm nối nhau lao tới đối thủ, màn rung theo từng đợt, bụi
        // đất bị thổi tạt dọc đường; đợt đầu tới nơi thì đối thủ trúng, lá và bụi sau lưng nó bị thổi bay.
        public float NRongGam(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead,
            float dur = RongGamDur)
        {
            float s0 = Mathf.Max(0.1f, lead);
            var dd = Unit(foeBody - mouth);
            var nrm = new Vector2(-dd.y, dd.x);
            float dist = (foeBody - mouth).magnitude;
            const float V = 980;
            float fly = dist / V;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            // lấy hơi
            if (s0 > 0.2f)
                Every(Mathf.Max(0, s0 - 0.42f), s0 - 0.08f, 26, x =>
                {
                    float a = U(0, 6.28f);
                    var from = mouth + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * U(46, 90) + dd * 30;
                    if (U(0, 1) < 0.6f) Leaf(from, (mouth - from) * 3.2f, 0.3f, U(3.5f, 6f));
                    else Foam(from, (mouth - from) * 3f, 0.28f, 2.5f, 6);
                });
            // GẦM: bảy đợt sóng, mỗi đợt hai cung lồng nhau; đợt đầu to và nhanh nhất
            At(s0, () =>
            {
                Shake?.Invoke(1f);
                RingN(mouth, 0.26f, 0.05f * casterH, 0.34f * casterH, AmC, 0.9f, Front, 43);
                for (int i = 0; i < 8; i++)
                    Bui(casterFeet + new Vector2(dir * U(0.1f, 0.5f) * casterH, U(-4, 2)), new Vector2(dir * U(160, 380), -U(10, 60)), 0, 4, 12, Back);
            });
            int N = Mathf.Max(3, Mathf.RoundToInt(dur / 0.09f));
            for (int i = 0; i < N; i++)
            {
                int j = i;
                At(s0 + 0.09f * j, () =>
                {
                    float m = j == 0 ? 1.2f : 1;
                    var den = foeBody + dd * (0.2f * tH);
                    SongAm(mouth, den, 0.14f * casterH, 0.86f * tH * m, V * (j == 0 ? 1.08f : 1), AmC);
                    SongAm(mouth - dd * 22, den - dd * 22, 0.09f * casterH, 0.56f * tH * m, V * (j == 0 ? 1.08f : 1), W[3]);
                    Shake?.Invoke(j == 0 ? 0.7f : 0.38f);
                    for (int q = 0; q < 3; q++) // bụi và lá bị thổi tạt dọc đất
                    {
                        float f = U(0.1f, 0.9f);
                        var p = Vector2.Lerp(casterFeet, foeFeet, f) + new Vector2(0, U(-5, 2));
                        if ((q & 1) == 0) Bui(p, new Vector2(dir * U(240, 460), -U(10, 60)), 0, 3, 9, Back);
                        else Leaf(p + new Vector2(0, -U(4, 20)), new Vector2(dir * U(420, 700), -U(40, 160)), U(0.3f, 0.5f), U(4, 6.5f), 300, 0.6f, Back);
                    }
                });
            }
            // trúng: mỗi đợt tới nơi là một cú giật nhỏ ở đối thủ; đợt đầu chớp toé + lá vỡ, bụi sau lưng nó bị thổi đi
            float hit = s0 + fly;
            At(hit, () =>
            {
                Shake?.Invoke(0.85f);
                BurstFlash(foeBody, 0.5f * tH);
                LaNo(foeBody, foeFeet, tH, 1.1f);
                WExtra(foeBody, 6, 320);
            });
            Every(hit, hit + dur, 11, x =>
            {
                var p = foeBody + new Vector2(U(-0.2f, 0.2f), U(-0.35f, 0.3f)) * tH;
                var q = Spark(p, dd + nrm * U(-0.5f, 0.5f), U(300, 520), U(0.14f, 0.24f), U(6, 9), 0, Front, 3);
                q.col = AmC;
                Bui(foeFeet + new Vector2(dir * U(0, 0.3f) * tH, U(-5, 2)), new Vector2(dir * U(200, 420), -U(20, 90)), 0, 4, 12, Back);
            });
            return hit;
        }

        // CHIÊU CUỐI: VẠN DIỆP. Sấp xoè cánh (vòng đất) → dựng cánh gầm (lá cuốn bay lên quanh thân) → khép cánh thành kén (lá bị hút
        // vào thân; măng nhú báo trước quanh chân đối thủ) → kén BUNG (chớp toé, vành lá toả đều) → QUẠT CÁNH: bão lá lao tới chém đối
        // thủ từ nhiều hướng → sập cánh: rừng măng trúc đâm lên dưới chân nó, cột lá, sét kết liễu.
        public float NRongVan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.9f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var nguc = casterFeet + new Vector2(dir * 0.05f * casterH, -0.42f * casterH);
            float tSap = Mathf.Max(0.03f, L - 1.65f), tGam = Mathf.Max(0.06f, L - 1.28f), tKen = Mathf.Max(0.1f, L - 0.82f), tBung = Mathf.Max(0.14f, L - 0.55f);
            // sấp xuống, cánh xoè sát đất: vòng đất và bụi hai bên
            At(tSap, () =>
            {
                Shake?.Invoke(0.4f);
                Ripple(casterFeet + new Vector2(0, 2), 0.16f * casterH, 0.95f * casterH, 0.55f, BuiC2);
                for (int i = 0; i < 10; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(casterFeet + new Vector2(sd * U(0.1f, 0.5f) * casterH, U(-5, 2)), new Vector2(sd * U(100, 260), -U(10, 60)), 0, 4, 13, Back);
                }
            });
            // dựng bốn cánh gầm: lá quanh người cuốn xoáy bay lên
            Every(tGam, tKen, 70, x =>
            {
                float a = U(0, 6.28f);
                float R = U(0.34f, 0.66f) * casterH;
                var from = casterFeet + new Vector2(Mathf.Cos(a) * R, Mathf.Sin(a) * R * 0.26f - U(0, 0.3f) * casterH);
                Leaf(from, new Vector2(-Mathf.Sin(a) * 220, -U(240, 420)), U(0.45f, 0.72f), U(5.5f, 9f), -140, 1.1f, Mathf.Sin(a) < 0 ? Back : Front);
            });
            At(tGam, () => Shake?.Invoke(0.5f));
            // khép cánh thành kén: lá và phấn bị hút vào ngực; vòng co lại; măng nhú quanh chân đối thủ (báo trước)
            Every(tKen, tBung - 0.04f, 80, x =>
            {
                float a = U(0, 6.28f);
                var from = nguc + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * U(0.5f, 0.95f) * casterH;
                if (U(0, 1) < 0.7f) Leaf(from, (nguc - from) * 3.3f, 0.3f, U(4, 7f), 0, 0, Mathf.Sin(a) < 0 ? Back : Front);
                else Foam(from, (nguc - from) * 3.1f, 0.3f, 2.5f, 6);
            });
            At(tKen, () => Ripple(casterFeet + new Vector2(0, 2), 0.9f * casterH, 0.12f * casterH, 0.3f, W[3]));
            if (HasGai)
                for (int i = 0; i < 4; i++)
                {
                    int j = i;
                    At(tKen + 0.06f * j, () =>
                    {
                        var q = Spike(foeFeet + new Vector2((j - 1.5f) * 0.22f * tH, 2), new Vector2((j - 1.5f) * 0.12f, -1), 0.2f * tH, L + 0.5f - tKen - 0.06f * j,
                            (j & 1) == 0 ? Back : Front, j, 0.5f);
                        q.col = (j & 1) == 0 ? W[2] : W[1];
                    });
                }
            // kén BUNG
            At(tBung, () =>
            {
                Shake?.Invoke(0.85f);
                FlashScreen?.Invoke(FlashW);
                BurstFlash(nguc, 0.7f * casterH, Front, 0.16f);
                RingN(nguc, 0.36f, 0.14f * casterH, 0.95f * casterH, W[3], 1, Back, 34);
                for (int i = 0; i < 34; i++)
                {
                    float a = 6.28f * (i + U(0, 0.8f)) / 34; // rải đều góc
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Leaf(nguc + d * U(0.1f, 0.24f) * casterH, d * U(260, 560), U(0.5f, 0.85f), U(5.5f, 9.5f), 420, 1.5f, (i & 1) == 0 ? Back : Front);
                }
                WExtra(nguc, 8, 340);
            });
            // QUẠT CÁNH: bão lá lao tới (từ quanh thân, mỗi lá tự lái về một điểm trong thân đối thủ), các lưỡi lá lớn chém chéo qua nó
            var dd = Unit(foeBody - nguc);
            var nrm = new Vector2(-dd.y, dd.x);
            float dist = (foeBody - nguc).magnitude;
            const float V = 1150;
            float fly = dist / V;
            float tQuat = L - 0.06f;
            Every(tQuat, tQuat + 0.56f, x => 120 * (x < 0.2f ? 1.4f : 1), x =>
            {
                float spd = V * U(0.85f, 1.15f);
                var from = nguc + nrm * U(-0.55f, 0.55f) * casterH + dd * U(0, 0.2f) * casterH;
                var q = Leaf(from, dd * spd + nrm * U(-160, 160), dist / spd + 0.3f, U(7.5f, 13f));
                q.aim = foeBody + new Vector2(U(-0.26f, 0.26f), U(-0.34f, 0.3f)) * tH;
                q.R0 = spd;
                q.upd = (z, dt, s) =>
                {
                    var to = z.aim - z.pos;
                    float d = to.magnitude;
                    var want = to / Mathf.Max(d, 1e-5f) * z.R0 + nrm * (Mathf.Sin(z.age * 15 + z.ph) * 150);
                    z.vel += (want - z.vel) * Mathf.Min(1, 7 * dt);
                    if (d < 16)
                    {
                        z.hit = true;
                        z.dead = true;
                    }
                };
                q.onDeath = (z, s) =>
                {
                    if (!z.hit) return;
                    if (s.U(0, 1) < 0.4f) s.Leaf(z.pos, -dd * s.U(60, 150) + s.U2(-140, 140), s.U(0.3f, 0.5f), s.U(3.5f, 5.5f), 700, 1.5f);
                };
            });
            float hit = L + fly;
            At(L, () => Shake?.Invoke(0.7f));
            var chem = new[] { (-0.5f, -0.9f, 1.0f), (0.6f, -0.8f, 0.95f), (-0.9f, 0.1f, 1.1f), (0.35f, -1f, 0.9f), (0.9f, 0.3f, 1.05f), (-0.3f, -1f, 1.15f) };
            for (int i = 0; i < chem.Length; i++)
            {
                int j = i;
                At(hit + 0.075f * j, () =>
                {
                    var (cx, cy, m) = chem[j];
                    var d = Unit(new Vector2(cx, cy));
                    var c = foeBody + new Vector2(U(-0.12f, 0.12f), U(-0.16f, 0.12f)) * tH;
                    VetChem(c, d, 1.0f * tH * m, 0.085f * tH * m, 0.2f);
                    ChemToe(c, d, tH, 0.8f, 3);
                    Shake?.Invoke(0.42f);
                });
            }
            Every(hit, hit + 0.5f, 8, x => Shake?.Invoke(0.2f));
            // SẬP CÁNH: rừng măng trúc đâm lên dưới chân đối thủ, cột lá, vòng đất, sét kết liễu
            float tSapCanh = L + 0.5f;
            At(tSapCanh - 0.03f, () => Ripple(foeFeet + new Vector2(0, 2), 0.7f * tH, 0.1f * tH, 0.1f, W[3]));
            At(tSapCanh, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(FlashSet);
                Ripple(foeFeet + new Vector2(0, 2), 0.16f * tH, 1.05f * tH, 0.55f, BuiC2);
                RingN(foeBody, 0.36f, 0.16f * tH, 0.95f * tH, W[3], 1, Front, 36);
                LaNo(foeBody, foeFeet, tH, 1.7f);
                WExtra(foeBody, 10, 360);
                for (int i = 0; i < 10; i++)
                    Bui(foeFeet + new Vector2(U(-0.45f, 0.45f) * tH, U(-6, 2)), new Vector2(U(-160, 160), -U(15, 80)), 0, 4, 15, Back);
                for (int i = 0; i < 8; i++) DaVun(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -4), new Vector2(U(-240, 240), -U(260, 520)), U(0.5f, 0.8f), U(3f, 5f));
                if (HasGai) // măng trúc: bốn cái cao phía sau, ba cái thấp phía trước
                {
                    var goc = new[] { (-0.46f, -0.3f, 1.0f, Back), (-0.16f, -0.08f, 1.22f, Back), (0.16f, 0.1f, 1.16f, Back), (0.46f, 0.32f, 0.96f, Back),
                        (-0.6f, -0.8f, 0.5f, Front), (0.02f, 0.02f, 0.42f, Front), (0.62f, 0.85f, 0.48f, Front) };
                    for (int i = 0; i < goc.Length; i++)
                    {
                        var (ox, nghieng, dai, nhom) = goc[i];
                        var q = Spike(foeFeet + new Vector2(ox * tH, 2), new Vector2(nghieng, -1), dai * tH, 0.8f, nhom, i, 0.46f);
                        q.col = (i & 1) == 0 ? W[2] : W[1];
                    }
                }
                CotLa(foeFeet + new Vector2(-0.2f * tH, 0), tH, 1.2f);
                CotLa(foeFeet + new Vector2(0.22f * tH, 0), tH, 1.1f);
                SetGiang(foeBody + new Vector2(0, -0.42f * tH), tH, 1.25f);
            });
            Every(tSapCanh, tSapCanh + 0.5f, x => 80 * (1 - 0.6f * x), x =>
                Leaf(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -U(0, 0.15f) * tH), new Vector2(U(-80, 80), -U(420, 720)), U(0.55f, 0.85f), U(4.5f, 7.5f), 980, 0.7f,
                    U(0, 1) < 0.72f ? Back : Front));
            return hit;
        }
    }
}
