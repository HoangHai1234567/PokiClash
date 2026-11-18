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
// Nâng 2026-11-18 (người dùng: "sóng âm chưa đẹp", "khói rải rác chưa thành cụm", "sét vàng tươi lõi kem"): sóng âm là dải cung dày giữa
// thuôn hai đầu, nở và mỏng dần, tới mặt trước thân đối thủ thì bẹt ra rồi tan (SongAmMoc); bụi thành cụm tách dần (BuiCum); vòng cung dẹt
// đứt đoạn trên đất (CungDat); vết đất giữ ~1 s (VetDat); sét của rồng vàng tươi lõi kem rộng (SetTuoi), chớp nổ nhỏ không che mặt.
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
        static readonly Color[] SetTuoi = { C(255, 232, 64), C(255, 252, 226) }; // sét của rồng trúc: vàng tươi, lõi kem (góp ý 2026-11-18)

        public const float RongGamDur = 0.6f; // chiêu gầm: sóng âm phát chừng này giây kể từ lúc há mồm

        // ---------- SÉT: một tia gấp khúc từ trên trời xuống điểm dich; hiện đậm 2–3 khung rồi mảnh dần; đổi dáng một lần giữa chừng ----------
        // q.stops (nếu có): màu thân, màu lõi (lõi rộng hơn); không có thì SetC / SetLoi như cũ (Pháo Giáp HatPhao.cs dùng chung)
        void DrawSet(P q, float k, List<Item> buf)
        {
            Color cThan = q.stops != null ? q.stops[0] : SetC, cLoi = q.stops != null ? q.stops[1] : SetLoi;
            float rLoi = q.stops != null ? 0.55f : 0.42f;
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
                LaLieu(buf, q.group, 47.3f, false, cThan, tam, u, dai, day, a);
                LaLieu(buf, q.group, 47.6f, false, cLoi, tam, u, dai * 0.84f, day * rLoi, a);
                if (q.big && (i == 2 || i == n - 2)) // hai nhánh con rẽ ra
                {
                    var r2 = nrm * ((i == 2 ? 1 : -1) * q.sz * 1.5f) + huong.normalized * q.sz * 1.3f;
                    var t2 = truoc + r2 * 0.5f;
                    LaLieu(buf, q.group, 46.8f, true, Ink, t2, Unit(r2), r2.magnitude + 6, day * 0.55f + 5, a);
                    LaLieu(buf, q.group, 47.1f, false, cThan, t2, Unit(r2), r2.magnitude, day * 0.55f, a);
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

        // sét giáng vào đầu đối thủ: tia chính + hai tia phụ lệch giờ (vàng tươi, lõi kem rộng), chớp nổ nhỏ ở trước + toé sau thân (bản cũ:
        // chớp to ở trước che mặt), vòng va chạm, tia vụn theo cụm, chớp màn
        void SetGiang(Vector2 dau, float tH, float manh)
        {
            var troi = dau + new Vector2(U(-0.25f, 0.25f) * tH, -2.3f * tH);
            Set(troi, dau, 0.085f * tH * manh, 0.2f * tH, 0.26f).stops = SetTuoi;
            At(0.07f, () => Set(troi + new Vector2(0.3f * tH, 0), dau + new Vector2(0.06f * tH, 0.05f * tH), 0.05f * tH * manh, 0.16f * tH, 0.16f, false).stops = SetTuoi);
            At(0.15f, () => Set(troi + new Vector2(-0.34f * tH, 0), dau + new Vector2(-0.07f * tH, 0.08f * tH), 0.042f * tH * manh, 0.15f * tH, 0.14f, false).stops = SetTuoi);
            FlashScreen?.Invoke(FlashSet);
            Shake?.Invoke(1f);
            DanhTrung?.Invoke(dau, 1);
            Chop(dau, 0.4f * tH * Mathf.Min(1.2f, manh), 0.08f);
            BurstFlash(dau, 0.6f * tH * manh, Back, 0.16f);
            VongVa(dau, 0.1f * tH, 0.55f * tH, 0.28f, SetTuoi[0], Front, 0.9f, 36);
            for (int i = 0; i < 4; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / 4;
                TiaVunCum(dau, new Vector2(Mathf.Cos(a), Mathf.Sin(a)), 0.5f, 3, U(380, 600) * manh, U(3.4f, 4.6f), Front, SetTuoi[0], SetTuoi[1]);
            }
        }

        // một chỗ đất nứt bật lên trên đường địa chấn: vòng cung dẹt nhỏ, cụm bụi tách dần, đá vụn
        void DatNut(Vector2 dat, float tH, float sc)
        {
            CungDat(dat + new Vector2(0, 2), 0.04f * tH, 0.3f * tH * sc, 0.36f, CungC, 0.05f * tH * sc, 3);
            for (int i = 0; i < 2; i++)
                BuiCum(dat + new Vector2(U(-12, 12) * sc, U(-4, 2)), new Vector2(U(-70, 70), -U(50, 110)) * sc, U(0.07f, 0.1f) * tH * sc, 0, i == 0 ? Back : Front);
            int n = Mathf.RoundToInt(4 * sc);
            for (int i = 0; i < n; i++)
                DaVun(dat + new Vector2(U(-10, 10) * sc, -4), new Vector2(U(-130, 130), -U(260, 470)) * sc, U(0.4f, 0.65f), U(2.6f, 4.2f), (i & 1) == 0 ? Back : Front);
        }

        // ĐÒN ĐÁNH THƯỜNG: dậm hai chân trước → địa chấn chạy tới đối thủ → SÉT giáng vào đầu nó đúng khung trúng của clip.
        public float NRongDam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.3f, lead);
            float tDam = Mathf.Max(0.05f, L - 0.22f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var truoc = casterFeet + new Vector2(dir * 0.2f * casterH, 0); // chỗ hai chân trước dậm xuống
            // chồm dựng: bụi dưới chân sau
            float tChom = Mathf.Max(0.02f, L - 0.63f);
            Every(tChom, tChom + 0.2f, 7, x =>
                BuiCum(casterFeet + new Vector2(-dir * U(0.05f, 0.3f) * casterH, U(-4, 2)), new Vector2(-dir * U(20, 80), -U(20, 50)), U(0.05f, 0.07f) * casterH, 0, Back));
            // DẬM: vòng cung dẹt hai lớp, cụm bụi lớn tách dần, đá vụn, lá, vết đất
            At(tDam, () =>
            {
                Shake?.Invoke(0.9f);
                CungDat(truoc + new Vector2(0, 2), 0.1f * casterH, 0.85f * casterH, 0.45f, CungC, 0.1f * casterH);
                CungDat(truoc + new Vector2(0, 2), 0.06f * casterH, 0.55f * casterH, 0.4f, W[2], 0.06f * casterH, 5);
                VetDat(truoc + new Vector2(0, 3), 0.5f * casterH, 1f);
                for (int i = 0; i < 6; i++)
                {
                    float sd = i == 5 ? 0 : (i & 1) == 0 ? 1 : -1;
                    BuiCum(truoc + new Vector2(sd * U(0.08f, 0.32f) * casterH, U(-6, 3)), new Vector2(sd * U(90, 220), -U(15, 55)), U(0.1f, 0.15f) * casterH, 0,
                        i < 4 ? Back : Front);
                }
                for (int i = 0; i < 7; i++) DaVun(truoc + new Vector2(U(-24, 24), -4), new Vector2(U(-220, 220), -U(240, 460)), U(0.45f, 0.75f), U(2.6f, 4.4f));
                for (int i = 0; i < 5; i++) Leaf(truoc + new Vector2(U(-20, 20), -U(4, 14)), new Vector2(U(-140, 140), -U(260, 420)), U(0.5f, 0.8f), U(3.6f, 5.6f), 700, 1.2f);
            });
            // địa chấn chạy tới đối thủ: ba chỗ đất nứt, cái sau to hơn
            for (int i = 0; i < 3; i++)
            {
                int j = i;
                At(tDam + 0.055f * (j + 1), () => DatNut(Vector2.Lerp(truoc, foeFeet, 0.26f + 0.3f * j), tH, 0.8f + 0.2f * j));
            }
            // SÉT giáng xuống đầu đối thủ + đất dưới chân nó bật lên
            var dau = foeBody + new Vector2(0, -0.42f * tH);
            At(L - 0.06f, () => CungDat(foeFeet + new Vector2(0, 2), 0.32f * tH, 0.08f * tH, 0.08f, SetTuoi[0], 0.05f * tH, 5)); // vòng co lại báo trước một nhịp
            At(L, () =>
            {
                SetGiang(dau, tH, 1);
                DatNut(foeFeet, tH, 1.25f);
                VetDat(foeFeet + new Vector2(0, 3), 0.48f * tH, 1f);
                WExtra(foeBody, 4, 300);
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

        // SÓNG ÂM bộ Mộc: dải cung dày giữa thuôn nhọn hai đầu (lưỡi liềm lồi về phía bay), lao từ mồm tới MẶT TRƯỚC thân đối thủ, nở rộng và
        // mỏng dần theo quãng; tới nơi thì bẹt ra, mỏng hẳn rồi tan (không trùm lên mặt con bị trúng). Lớp ngoài kem / lớp trong lục tươi, đợt
        // sau đảo màu (kem: q.big). Ảnh kr_songam (lồi về +x, cắt sát) khi đã nhập; chưa có thì mảng liền (MLiem). Bản cũ (SongAm, Bạch Viêm Hổ
        // HatHo.cs còn dùng): cung móng ngựa dày đều, không thuôn, bay xuyên qua đối thủ.
        P SongAmMoc(Vector2 tu, Vector2 den, float r0, float r1, float day0, float v, bool kem, int group = Front)
        {
            var d = den - tu;
            float toi = d.magnitude / v;
            var p = new P { pos = tu, home = tu, aim = Unit(d), vy = v, life = toi + 0.1f, tb = toi, R0 = r0, R1 = r1, wd = day0, big = kem, stops = W, group = group,
                seed = rng.Next(4) };
            p.draw = (q, k, buf) =>
            {
                float t = q.age, toi2 = q.tb;
                float f = Mathf.Clamp01(t / toi2);
                float R = Mathf.Lerp(q.R0, q.R1, EaseOut(f));
                float day = q.wd * (1 - 0.4f * f);
                float span = 1.55f;
                float a = Mathf.Min(1, t / 0.04f);
                if (t > toi2)
                {
                    float u = (t - toi2) / Mathf.Max(0.02f, q.life - toi2);
                    span *= 1 + 0.45f * u;
                    R *= 1 + 0.12f * u;
                    day *= 1 - u;
                    a *= 1 - u;
                }
                day = Mathf.Min(day, 0.7f * R); // lúc mới ra khỏi mồm cung còn nhỏ: không cho dày quá bán kính
                if (a < 0.03f || day < 0.8f) return;
                var dinh = q.home + q.aim * (Mathf.Min(t, toi2) * q.vy);
                Color c1 = q.big ? AmC : q.stops[3], c2 = q.big ? q.stops[3] : AmC;
                var ks = S("kr_songam_" + q.seed);
                if (ks != null)
                {
                    // ảnh: lưỡi liềm lồi về +x, dây cung 90 % chiều cao khung, giữa dày 16 % bề ngang khung, đỉnh lưng ở 58 % bề ngang
                    float chord = 2 * R * Mathf.Sin(span * 0.5f);
                    float h = chord / 0.9f, wk = day / 0.16f;
                    float ang = VelAng(q.aim);
                    var c = dinh - q.aim * (0.08f * wk);
                    Put(buf, q.group, 44, S("kr_songams_" + q.seed) ?? ks, Ink, c, h + 6, (wk + 6) / (h + 6), ang, a);
                    Put(buf, q.group, 44.2f, ks, c1, c, h, wk / h, ang, a);
                    Put(buf, q.group, 44.4f, ks, c2, dinh - q.aim * (0.08f * wk * 0.5f), h * 0.86f, wk * 0.5f / (h * 0.86f), ang, a);
                    return;
                }
                MLiem(q.group, 44, dinh - q.aim * R, q.aim, R, day, span, c1, c2, a, 2.4f);
            };
            return Add(p);
        }

        // CHIÊU MANA: GẦM. Lấy hơi (lá, vệt gió bị hút xoắn vào mồm) → há mồm: các đợt sóng âm (dải cung thuôn hai đầu) nối nhau lao tới mặt
        // trước thân đối thủ, nở và mỏng dần, tới nơi thì bẹt ra tan; màn rung theo từng đợt; bụi cụm và lá bị thổi tạt dọc đất; mỗi đợt tới nơi
        // đối thủ giật một nhịp; đợt đầu chớp nhỏ + lá vỡ, bụi sau lưng nó bị thổi đi.
        public float NRongGam(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead,
            float dur = RongGamDur)
        {
            MocSang();
            float s0 = Mathf.Max(0.1f, lead);
            var dd = Unit(foeBody - mouth);
            var nrm = new Vector2(-dd.y, dd.x);
            var cham = ChamThan(mouth, foeBody, 1.4f * tH); // sóng dừng sớm hơn tia một chút: cung rộng, hai đầu không quàng lên mặt
            float dist = (foeBody - mouth).magnitude;
            const float V = 980;
            float fly = dist / V;                            // giờ trúng giữ như bản trước
            float toi = (cham - mouth).magnitude / V;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            // lấy hơi
            if (s0 > 0.2f) GatherLa(t => mouth, Mathf.Max(0, s0 - 0.42f), s0 - 0.06f, 84, 28);
            // GẦM: đợt sóng nối nhau, đợt đầu to và nhanh nhất
            At(s0, () =>
            {
                Shake?.Invoke(1f);
                VongVa(mouth, 0.05f * casterH, 0.36f * casterH, 0.24f, AmC, Front, 0.9f, 43);
                for (int i = 0; i < 3; i++)
                    BuiCum(casterFeet + new Vector2(dir * U(0.1f, 0.5f) * casterH, U(-4, 2)), new Vector2(dir * U(140, 300), -U(10, 40)), U(0.1f, 0.13f) * casterH, 0, Back);
            });
            int N = Mathf.Max(3, Mathf.RoundToInt(dur / 0.09f));
            for (int i = 0; i < N; i++)
            {
                int j = i;
                At(s0 + 0.09f * j, () =>
                {
                    float m = j == 0 ? 1.15f : 1 - 0.04f * j;
                    SongAmMoc(mouth + dd * 10, cham, 0.12f * casterH, 0.8f * tH * m, 0.2f * tH * m, V * (j == 0 ? 1.08f : 1), (j & 1) == 0);
                    Shake?.Invoke(j == 0 ? 0.6f : 0.3f);
                    float f = U(0.15f, 0.85f); // bụi cụm và lá bị thổi tạt dọc đất
                    var p = Vector2.Lerp(casterFeet, foeFeet, f) + new Vector2(0, U(-5, 2));
                    if ((j & 1) == 0) BuiCum(p, new Vector2(dir * U(200, 360), -U(10, 40)), U(0.06f, 0.09f) * tH, 0, Back);
                    Leaf(p + new Vector2(0, -U(4, 20)), new Vector2(dir * U(420, 700), -U(40, 160)), U(0.3f, 0.5f), U(3.4f, 5.4f), 300, 0.6f, Back);
                });
                At(s0 + 0.09f * j + toi * (j == 0 ? 1 / 1.08f : 1), () => // đợt sóng tới nơi: đối thủ giật, vòng va chạm nhỏ, tia vụn toé ngược
                {
                    DanhTrung?.Invoke(cham, j == 0 ? 0.7f : 0.3f);
                    VongVa(cham, 0.06f * tH, 0.3f * tH, 0.16f, AmC, Front, 1, 42);
                    TiaVunCum(cham, -dd, 1.1f, 2, U(260, 420), U(3f, 4f), Front, AmC, MocChanh);
                });
            }
            // trúng: đợt đầu chớp nhỏ + lá vỡ; bụi sau lưng đối thủ bị thổi đi suốt lúc sóng tới
            float hit = s0 + fly;
            At(hit, () =>
            {
                Shake?.Invoke(0.8f);
                LaNo(foeBody, foeFeet, tH, 1.05f);
                WExtra(foeBody, 5, 320);
            });
            Every(hit, hit + dur, 5, x =>
                BuiCum(foeFeet + new Vector2(dir * U(0, 0.3f) * tH, U(-5, 2)), new Vector2(dir * U(160, 320), -U(20, 60)), U(0.08f, 0.11f) * tH, 0, Back));
            Every(hit, hit + dur, 8, x =>
                Leaf(foeBody + new Vector2(U(-0.25f, 0.25f), U(-0.35f, 0.2f)) * tH, new Vector2(dir * U(240, 420), -U(40, 140)), U(0.35f, 0.55f), U(3.4f, 5f), 380, 1.2f,
                    U(0, 1) < 0.6f ? Back : Front));
            return hit;
        }

        // CHIÊU CUỐI: VẠN DIỆP. Sấp xoè cánh (vòng đất) → dựng cánh gầm (lá cuốn bay lên quanh thân) → khép cánh thành kén (lá bị hút
        // vào thân; măng nhú báo trước quanh chân đối thủ) → kén BUNG (chớp toé, vành lá toả đều) → QUẠT CÁNH: bão lá lao tới chém đối
        // thủ từ nhiều hướng → sập cánh: rừng măng trúc đâm lên dưới chân nó, cột lá, sét kết liễu.
        public float NRongVan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.9f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var nguc = casterFeet + new Vector2(dir * 0.05f * casterH, -0.42f * casterH);
            float tSap = Mathf.Max(0.03f, L - 1.65f), tGam = Mathf.Max(0.06f, L - 1.28f), tKen = Mathf.Max(0.1f, L - 0.82f), tBung = Mathf.Max(0.14f, L - 0.55f);
            // sấp xuống, cánh xoè sát đất: vòng đất và bụi hai bên
            At(tSap, () =>
            {
                Shake?.Invoke(0.4f);
                CungDat(casterFeet + new Vector2(0, 2), 0.16f * casterH, 1.0f * casterH, 0.5f, CungC, 0.09f * casterH);
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    BuiCum(casterFeet + new Vector2(sd * U(0.15f, 0.5f) * casterH, U(-5, 2)), new Vector2(sd * U(90, 200), -U(10, 40)), U(0.1f, 0.13f) * casterH, 0, Back);
                }
            });
            // dựng bốn cánh gầm: lá quanh người cuốn xoáy bay lên
            Every(tGam, tKen, 70, x =>
            {
                float a = U(0, 6.28f);
                float R = U(0.34f, 0.66f) * casterH;
                var from = casterFeet + new Vector2(Mathf.Cos(a) * R, Mathf.Sin(a) * R * 0.26f - U(0, 0.3f) * casterH);
                Leaf(from, new Vector2(-Mathf.Sin(a) * 220, -U(240, 420)), U(0.45f, 0.72f), U(4.5f, 7.5f), -140, 1.1f, Mathf.Sin(a) < 0 ? Back : Front);
            });
            At(tGam, () => Shake?.Invoke(0.5f));
            // khép cánh thành kén: lá và vệt gió bị hút xoắn vào ngực, nhanh dần, nhập vào kén; vòng co lại; măng nhú quanh chân đối thủ (báo trước)
            At(tKen, () => GatherLa(t => nguc, 0, tBung - tKen - 0.04f, 0.95f * casterH, 60));
            At(tKen, () => CungDat(casterFeet + new Vector2(0, 2), 0.9f * casterH, 0.14f * casterH, 0.3f, W[3], 0.06f * casterH, 5));
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
                Chop(nguc, 0.6f * casterH, 0.09f);
                BurstFlash(nguc, 0.7f * casterH, Back, 0.16f);
                VongVa(nguc, 0.14f * casterH, 0.95f * casterH, 0.36f, W[3], Back, 1, 34);
                for (int i = 0; i < 30; i++)
                {
                    float a = 6.28f * (i + U(0, 0.8f)) / 30; // rải đều góc
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Leaf(nguc + d * U(0.1f, 0.24f) * casterH, d * U(260, 560), U(0.5f, 0.85f), U(4.5f, 8f), 420, 1.5f, (i & 1) == 0 ? Back : Front);
                }
                for (int i = 0; i < 3; i++)
                    BuiCum(nguc + new Vector2(U(-0.3f, 0.3f), U(-0.3f, 0.1f)) * casterH, new Vector2(U(-80, 80), -U(40, 90)), U(0.12f, 0.16f) * casterH, 0, Back, CumPhan);
                WExtra(nguc, 7, 340);
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
                var q = Leaf(from, dd * spd + nrm * U(-160, 160), dist / spd + 0.3f, U(6f, 10.5f));
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
            Every(hit, hit + 0.5f, 8, x =>
            {
                Shake?.Invoke(0.2f);
                DanhTrung?.Invoke(foeBody, 0.3f);
            });
            // SẬP CÁNH: rừng măng trúc đâm lên dưới chân đối thủ, cột lá, vòng đất, sét kết liễu
            float tSapCanh = L + 0.5f;
            At(tSapCanh - 0.06f, () => CungDat(foeFeet + new Vector2(0, 2), 0.7f * tH, 0.1f * tH, 0.1f, W[3], 0.06f * tH, 5));
            At(tSapCanh, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(FlashSet);
                CungDat(foeFeet + new Vector2(0, 2), 0.16f * tH, 1.1f * tH, 0.5f, CungC, 0.11f * tH);
                VetDat(foeFeet + new Vector2(0, 3), 0.6f * tH, 1.1f);
                LaNo(foeBody, foeFeet, tH, 1.6f);
                WExtra(foeBody, 8, 360);
                for (int i = 0; i < 5; i++)
                {
                    float sd = i == 4 ? 0 : (i & 1) == 0 ? 1 : -1;
                    BuiCum(foeFeet + new Vector2(sd * U(0.15f, 0.48f) * tH, U(-6, 2)), new Vector2(sd * U(90, 200), -U(15, 50)), U(0.12f, 0.16f) * tH, 0, Back);
                }
                for (int i = 0; i < 7; i++) DaVun(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -4), new Vector2(U(-240, 240), -U(260, 520)), U(0.5f, 0.8f), U(2.8f, 4.6f));
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
