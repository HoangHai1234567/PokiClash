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
            // khung vẽ sẵn (2026-11-19): đất bật thành một cụm khói nhuộm đất phồng lên (cụm to ngay, bỏ khung cụm bé) thay hai cụm BuiCum
            if (MocKhoiFb(dat + new Vector2(U(-6, 6) * sc, U(-2, 2)), 0.1f * tH * sc, new Vector2(U(-40, 40), -U(40, 80)) * sc, Back, 4.5f, 1.4f) == null)
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
            if (HasFb("khoi")) // khung vẽ sẵn (2026-11-19): một cụm khói nhuộm đất dưới chân sau thay vài cụm BuiCum lấm tấm
                At(tChom, () => MocKhoiFb(casterFeet + new Vector2(-dir * U(0.12f, 0.24f) * casterH, U(-3, 2)), 0.08f * casterH, new Vector2(-dir * U(20, 70), -U(15, 35)),
                    Back, 3, 1.3f, 0.85f));
            else
                Every(tChom, tChom + 0.2f, 7, x =>
                    BuiCum(casterFeet + new Vector2(-dir * U(0.05f, 0.3f) * casterH, U(-4, 2)), new Vector2(-dir * U(20, 80), -U(20, 50)), U(0.05f, 0.07f) * casterH, 0, Back));
            // DẬM: vòng cung dẹt hai lớp, cụm bụi lớn tách dần, đá vụn, lá, vết đất
            At(tDam, () =>
            {
                Shake?.Invoke(0.9f);
                CungDat(truoc + new Vector2(0, 2), 0.1f * casterH, 0.85f * casterH, 0.45f, CungC, 0.1f * casterH);
                CungDat(truoc + new Vector2(0, 2), 0.06f * casterH, 0.55f * casterH, 0.4f, W[2], 0.06f * casterH, 5);
                VetDat(truoc + new Vector2(0, 3), 0.5f * casterH, 1f);
                if (!MocBuiHaiBen(truoc, 0.15f * casterH, 0.26f * casterH, 160, true)) // khung vẽ sẵn: hai cụm khói nhuộm đất + một cụm giữa thay sáu cụm BuiCum
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
            bool kh = HasFb("khoi"); // khung vẽ sẵn (2026-11-19): bụi bị thổi là cụm khói nhuộm đất (ít cụm hơn: cụm to, sống lâu); chưa nhập khung thì BuiCum
            At(s0, () =>
            {
                Shake?.Invoke(1f);
                for (int i = 0; i < (kh ? 2 : 3); i++)
                {
                    var at = casterFeet + new Vector2(dir * U(0.1f, 0.5f) * casterH, U(-4, 2));
                    if (kh) MocKhoiFb(at, U(0.11f, 0.14f) * casterH, new Vector2(dir * U(160, 300), -U(10, 30)), Back, 4, 1.35f);
                    else BuiCum(at, new Vector2(dir * U(140, 300), -U(10, 40)), U(0.1f, 0.13f) * casterH, 0, Back);
                }
            });
            // sóng âm vẽ chì (2026-11-19, người dùng: "làm đơn giản thôi"): 3–4 cung nét chì xám nhạt (SongChi, HatSongChi.cs) thay 7 dải cung
            // viền mực hai màu; bỏ vòng tròn ở miệng và ở chỗ chạm
            int N = Mathf.Clamp(Mathf.RoundToInt(dur / 0.15f), 3, 4);
            for (int i = 0; i < N; i++)
            {
                int j = i;
                float vj = V * (j == 0 ? 1.06f : 1);
                At(s0 + 0.14f * j, () =>
                {
                    float m = j == 0 ? 1.1f : 1 - 0.06f * j;
                    SongChi(mouth + dd * 10, cham, 0.26f * casterH, 1.1f * tH * m, vj, 0.95f - 0.07f * j);
                    Shake?.Invoke(j == 0 ? 0.6f : 0.25f);
                    float f = U(0.15f, 0.85f); // bụi cụm và lá bị thổi tạt dọc đất
                    var p = Vector2.Lerp(casterFeet, foeFeet, f) + new Vector2(0, U(-5, 2));
                    if ((j & 1) == 0)
                    {
                        if (kh) MocKhoiFb(p, U(0.07f, 0.1f) * tH, new Vector2(dir * U(200, 340), -U(10, 30)), Back, 3.5f, 1.4f, 0.85f);
                        else BuiCum(p, new Vector2(dir * U(200, 360), -U(10, 40)), U(0.06f, 0.09f) * tH, 0, Back);
                    }
                    Leaf(p + new Vector2(0, -U(4, 20)), new Vector2(dir * U(420, 700), -U(40, 160)), U(0.3f, 0.5f), U(3.4f, 5.4f), 300, 0.6f, Back);
                });
                At(s0 + 0.14f * j + toi * V / vj, () => DanhTrung?.Invoke(cham, j == 0 ? 0.7f : 0.3f)); // cung tới nơi: đối thủ giật một nhịp
            }
            // trúng: đợt đầu chớp nhỏ + lá vỡ; bụi sau lưng đối thủ bị thổi đi suốt lúc sóng tới
            float hit = s0 + fly;
            At(hit, () =>
            {
                Shake?.Invoke(0.8f);
                LaNo(foeBody, foeFeet, tH, 1.05f);
                WExtra(foeBody, 5, 320);
            });
            Every(hit, hit + dur, kh ? 3.5f : 5, x =>
            {
                var at = foeFeet + new Vector2(dir * U(0, 0.3f) * tH, U(-5, 2));
                if (kh) MocKhoiFb(at, U(0.09f, 0.12f) * tH, new Vector2(dir * U(160, 300), -U(15, 40)), Back, 3.5f, 1.35f, 0.88f);
                else BuiCum(at, new Vector2(dir * U(160, 320), -U(20, 60)), U(0.08f, 0.11f) * tH, 0, Back);
            });
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
                if (!MocBuiHaiBen(casterFeet, 0.13f * casterH, 0.36f * casterH, 140)) // khung vẽ sẵn (2026-11-19): hai cụm khói nhuộm đất thay bốn cụm BuiCum
                    for (int i = 0; i < 4; i++)
                    {
                        float sd = (i & 1) == 0 ? 1 : -1;
                        BuiCum(casterFeet + new Vector2(sd * U(0.15f, 0.5f) * casterH, U(-5, 2)), new Vector2(sd * U(90, 200), -U(10, 40)), U(0.1f, 0.13f) * casterH, 0, Back);
                    }
            });
            // dựng bốn cánh gầm: lá quanh người cuốn xoáy bay lên. Khung vẽ sẵn (2026-11-19): một cột lốc năng lượng (loc) xoáy sau lưng rồng từ lúc
            // dựng cánh tới lúc khép kén (mờ dần vào kén), lá cuốn giữ lại nhưng thưa hơn
            bool loc = HasFb("loc");
            if (loc) At(tGam, () => MocLocFb(casterFeet + new Vector2(0, -2), 1.25f * casterH, tKen - tGam + 0.12f));
            Every(tGam, tKen, loc ? 36 : 70, x =>
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
            float tSapCanh = L + 0.5f;
            bool gaiFb = HasFb("gai_la");
            if (gaiFb) // khung vẽ sẵn (2026-11-19): măng nhú là gai lá nhỏ (gai_la) nhú lên, đứng chờ tới lúc sập cánh thì gãy cùng lúc rừng măng đâm lên;
                       // hai cụm ngoài ở lớp TRƯỚC, lệch ±0,52 tH cho thấy rõ mà không che chân; hai cụm trong sau lưng, cao hơn để ló ra hai bên thân
                for (int i = 0; i < 4; i++)
                {
                    float tNhu = tKen + 0.06f * i + 0.07f;
                    bool ngoai = i == 0 || i == 3;
                    MocGaiFb(foeFeet + new Vector2((ngoai ? 0.52f : 0.24f) * (i < 2 ? -1 : 1) * tH, ngoai ? 7 : -2), (ngoai ? 0.34f : 0.42f) * tH, tNhu, tSapCanh - tNhu,
                        Front, 34, (i & 1) == 1); // lớp TRƯỚC (người dùng 2026-11-19: "gai đất, nổ đang bị lỗi layer hiện đằng sau tướng địch")
                }
            else if (HasGai)
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
            At(tSapCanh - 0.06f, () => CungDat(foeFeet + new Vector2(0, 2), 0.7f * tH, 0.1f * tH, 0.1f, W[3], 0.06f * tH, 5));
            // khung vẽ sẵn (2026-11-19, người dùng chê "măng trúc đâm lên xấu"): rừng gai lá (gai_la, MocVongGai) so le, bốn cụm cao sau lưng đối thủ
            // đủ cao để ló lên trên vai; lớp trước ba cụm thấy rõ (hai cụm to hai bên + một cụm vừa chếch trước chân phía rồng; người dùng xem
            // trong game: bản đầu gai phần lớn ở sau lưng, bị thân che), không cụm cao nào ngay trước mặt; đỉnh phóng lệch nhau 0–0,09 s quanh lúc
            // sập cánh, khung nứt đất hiện trước một nhịp (cùng vòng co báo trước); giữ ~0,4 s rồi gãy rụng lá
            if (gaiFb)
                MocVongGai(foeFeet, tH, tSapCanh, 0.4f, casterFeet.x < foeFeet.x ? -1 : 1,
                    new[] { (-0.46f, 1.3f, 0f), (-0.16f, 1.55f, 0.03f), (0.16f, 1.48f, 0.05f), (0.46f, 1.25f, 0.08f) }, 1.06f, 2.5f);
            At(tSapCanh, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(FlashSet);
                CungDat(foeFeet + new Vector2(0, 2), 0.16f * tH, 1.1f * tH, 0.5f, CungC, 0.11f * tH);
                VetDat(foeFeet + new Vector2(0, 3), 0.6f * tH, 1.1f);
                LaNo(foeBody, foeFeet, tH, 1.6f);
                WExtra(foeBody, 8, 360);
                if (!MocBuiHaiBen(foeFeet, 0.15f * tH, 0.36f * tH, 150, true)) // khung vẽ sẵn: hai cụm khói nhuộm đất + một cụm giữa thay năm cụm BuiCum
                    for (int i = 0; i < 5; i++)
                    {
                        float sd = i == 4 ? 0 : (i & 1) == 0 ? 1 : -1;
                        BuiCum(foeFeet + new Vector2(sd * U(0.15f, 0.48f) * tH, U(-6, 2)), new Vector2(sd * U(90, 200), -U(15, 50)), U(0.12f, 0.16f) * tH, 0, Back);
                    }
                for (int i = 0; i < 7; i++) DaVun(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -4), new Vector2(U(-240, 240), -U(260, 520)), U(0.5f, 0.8f), U(2.8f, 4.6f));
                if (!gaiFb && HasGai) // măng trúc: bốn cái cao phía sau, ba cái thấp phía trước
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
                if (!gaiFb) // có rừng gai lá (khung vẽ sẵn) thì bỏ hai cột lá: trùng việc với rừng gai + lá phun, và đỡ ~20 hạt lúc đông nhất
                {
                    CotLa(foeFeet + new Vector2(-0.2f * tH, 0), tH, 1.2f);
                    CotLa(foeFeet + new Vector2(0.22f * tH, 0), tH, 1.1f);
                }
                SetGiang(foeBody + new Vector2(0, -0.42f * tH), tH, 1.25f);
            });
            Every(tSapCanh, tSapCanh + 0.5f, x => (gaiFb ? 60 : 80) * (1 - 0.6f * x), x => // có rừng gai lá thì bớt lá phun (đỡ đông hạt)
                Leaf(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -U(0, 0.15f) * tH), new Vector2(U(-80, 80), -U(420, 720)), U(0.55f, 0.85f), U(4.5f, 7.5f), 980, 0.7f,
                    U(0, 1) < 0.72f ? Back : Front));
            return hit;
        }
    }
}
