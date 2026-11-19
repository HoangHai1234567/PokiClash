// Bộ THIẾT KHOÁNG (2026-11-16, tinh linh quặng sắt chui đất, suất bo_ngua ải 10 đảo Kim; rig ArtGen/Spine/quang_sat_rig.py, hai dạng trên rig
// monster_3371; ghi chú ArtGen/Spine/inbox/quang_sat_ghichu.md). Người dùng: "bạn có thể làm thêm hiệu ứng" (sau khi tướng vào game với hiệu ứng
// mượn của bộ khác).
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip); mọi mốc dưới đây là mốc sự kiện của
// rig (quang_sat_rig.py) tính theo khung trúng, co giãn theo lead / khung trúng của rig nếu clip chạy nhanh chậm khác.
// - n_khoang_huc (đòn thường): dạng 1 húc: chớp, dăm quặng, tia, bụi. Dạng 2 (nhận ra bằng lead > 0,7 s: khung trúng ở nhát giáng 0,92) thêm
//   nhát húc ở 0,46 rồi cú giáng: chớp lớn, vòng sóng đất, bụi hai bên, đá văng.
// - n_khoang_ban1 / n_khoang_ban2 (chiêu mana): rig tự bay mảnh (fly_*, game lái tới đối thủ); lớp này lo từng cú GĂM: dạng 1 hai tay, dạng 2
//   hai tay + năm gai (7 cú đúng giờ từng mảnh tới), cú cuối to hơn có vòng bụi dưới chân.
// - n_khoang_dao1 / n_khoang_dao (chiêu cuối): đất toé lúc mũi tinh thể cắm hố, đất phụt theo lúc chui; đất hất sau gò lúc chạy ngầm (gò đi
//   theo cú lunge của sân: từ chân mình tới 72 % quãng tới đối thủ); sỏi rung trước khi trồi; đất nổ tung lúc trồi; húc: chớp + vòng cột tinh
//   thể quanh đối thủ (NSatDap); dạng 2 thêm nhát húc đầu, rơi lại xuống hố, đất nổ lần hai to hơn; bụi lúc rơi đất và lúc nhảy về.
//   Từ 2026-11-19 vòng cột là khung vẽ sẵn "gai_sat" nhuộm theo dạng (KmGaiVong), bụi đất nổ to là khung "khoi" nhuộm nâu (KmBuiFb).
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // màu: đất nâu của gò / hố (rig), quặng sắt đen (dạng 1), hematit đỏ gỉ (dạng 2)
        // 2026-11-18 ("màu tươi hơn, hợp sân cát biển sáng"): đất nâu ấm, quặng sắt sáng hơn chút (vẫn sẫm hơn nền cát để nổi)
        static readonly Color KhDat = C(156, 108, 64), KhDat2 = C(124, 84, 50);
        static readonly Color KhSat = C(78, 84, 100), KhSat2 = C(114, 122, 140);
        static readonly Color KhDo = C(152, 58, 44), KhDo2 = C(110, 38, 32);

        // mốc rig (giây clip): đòn thường, chiêu mana, chiêu cuối từng dạng
        const float KhHuc = 0.46f, KhGiang = 0.92f;
        static readonly float[] KhBan1 = { 0.600f, 0.667f };
        static readonly float[] KhBan2 = { 0.600f, 0.667f, 0.733f, 0.767f, 0.800f, 0.833f, 0.900f };
        const float KhBanTrung = 0.612f;                           // khung trúng cast của rig (= tay đầu tới + 0,012)
        const float KhDao = 0.62f, KhGo = 0.88f, KhChay0 = 1.02f, KhChay1 = 1.80f, KhTroi = 1.92f;
        static readonly float[] KhHit = { 2.08f, 2.66f };          // khung trúng skill (dạng 1, dạng 2)
        static readonly float[] KhDapT = { 2.40f, 3.00f };          // rơi chạm đất
        static readonly float[] KhLui1 = { 3.02f, 3.62f };         // nhảy về chạm đất
        const float KhHuc1 = 2.08f, KhXuong = 2.36f, KhTroi2 = 2.46f;  // dạng 2: húc lần một, rơi lại hố, đất nổ lần hai

        static readonly Color KhBuiC = C(170, 124, 80), KhBuiC2 = C(138, 98, 62);   // bụi đất nâu ấm (bụi be của bộ khác lẫn vào nền cát)

        // cụm bụi đất nâu
        P KhBui(Vector2 pos, Vector2 vel, float life = 0, float r0 = 5, float r1 = 16, int group = Front)
        {
            var b = Bui(pos, vel, life, r0, r1, group);
            b.col = (b.seed & 4) != 0 ? KhBuiC2 : KhBuiC;
            return b;
        }

        // một cột quặng trồi từ đất (đáy bám đất), bật quá cỡ, đứng, rồi vỡ thành dăm (như SatCot, màu theo dạng)
        void KhCot(Vector2 feet, float hgt, float wd, float delay, int group, int dang)
        {
            Color c1 = dang == 2 ? KhDo : KhSat, c2 = dang == 2 ? KhDo2 : KhSat2;
            At(delay, () =>
            {
                var p = new P { pos = feet, life = 0.6f, group = group, sz = hgt, wd = wd, col = U(0, 1) < 0.35f ? c2 : c1, ang = U(-14, 14) };
                p.draw = (q, k, buf) =>
                {
                    float t = k * q.life;
                    float g = t < 0.07f ? 1.2f * EaseOut(t / 0.07f) : t < 0.13f ? 1.2f - 0.2f * (t - 0.07f) / 0.06f : 1 - SmoothStep(0.75f, 1, k);
                    float hh = q.sz * g;
                    if (hh < 2) return;
                    float a = q.ang * Mathf.Deg2Rad;
                    var c = q.pos + new Vector2(Mathf.Sin(a), -Mathf.Cos(a)) * (hh * 0.5f);
                    Put(buf, q.group, 43, S("needles_0"), Ink, c, hh + 5, (q.wd + 5) / (hh + 5), -q.ang);
                    Put(buf, q.group, 43.5f, S("needle_0"), q.col, c, hh, q.wd / hh, -q.ang);
                };
                p.onDeath = (q, s3) =>
                {
                    for (int i = 0; i < 3; i++)
                        KhDam(q.pos + new Vector2(U(-0.3f, 0.3f) * q.wd, -U(0.2f, 0.8f) * q.sz), new Vector2(U(-200, 200), -U(160, 320)), U(0.4f, 0.6f),
                            U(5, 8), c1, c2, q.group);
                };
                Add(p);
            });
        }

        // HÚC TỪ DƯỚI (khung trúng chiêu cuối): chớp, vòng sóng, VÒNG CỘT QUẶNG trồi quanh đối thủ rồi vỡ, đất toé, đá văng
        void KhDap(Vector2 foeFeet, Vector2 foeBody, float tH, float manh, int dang)
        {
            Shake?.Invoke(0.6f * manh);
            var tam = foeFeet + new Vector2(0, -0.3f * tH);
            // chớp 2 khung nhỏ ở chân (trước: chớp 0,8 thân trùm kín đối thủ), vòng cung dẹt không viền (KR5), vệt đất xới giữ ~1 s
            KmChop(tam + new Vector2(0, 0.12f * tH), 0.4f * tH * manh, 0.07f, KmBac);
            KmCung(foeFeet + new Vector2(0, 2), 0.1f * tH, 1.15f * tH * manh, 0.42f, KhBuiC, 0.3f, Floor, 30.6f, 0.9f);
            KmChay(foeFeet + new Vector2(0, 3), 0.45f * tH * manh, 1f, 0.9f, 0.3f);
            // khung vẽ sẵn (2026-11-19, người dùng chê cột tinh thể cũ "gai sắt đâm lên xấu"): vòng cụm gai quặng đâm lên bằng khung "gai_sat"
            // nhuộm theo dạng (quặng sắt xám / hematit đỏ gỉ; KmGaiVong, HatFbKim.cs). Chưa nhập ảnh: cột quặng cũ
            bool gai = KmGaiVong(foeFeet, tH, manh, dang == 2 ? KhDoFb : KhSatFb, dang == 2 ? KhDoFb2 : KhSatFb2);
            int nc = gai ? 0 : Mathf.RoundToInt(9 * manh);
            for (int i = 0; i < nc; i++)
            {
                float a = 6.28f * (i + U(-0.2f, 0.2f)) / nc;
                var at = foeFeet + new Vector2(Mathf.Cos(a) * 0.62f * tH * manh, Mathf.Sin(a) * 0.16f * tH * manh);
                bool sau = Mathf.Sin(a) < 0;
                KhCot(at, U(0.45f, 0.8f) * tH * manh * (sau ? 1.1f : 0.85f), U(0.13f, 0.19f) * tH * manh, 0.03f + 0.02f * (i % 3), sau ? Back : Front, dang);
            }
            KhDatToe(foeFeet, tH, 1.1f * manh, Mathf.RoundToInt(10 * manh));
        }

        // cục đất / dăm quặng: dăm gai nhuộm màu (máy chưa có ảnh dăm thì tạm dùng lá như DaVun)
        P KhDam(Vector2 pos, Vector2 vel, float life, float r, Color c1, Color c2, int group = Front)
        {
            if (!HasGai) return Leaf(pos, vel, life, r, 700, 1.6f, group);
            var q = Shard(pos, vel, life, r, 860, 1.3f, group);
            q.col = (q.seed & 4) != 0 ? c2 : c1;
            return q;
        }

        // đất toé ở một chỗ: vòng bụi, cụm bụi hai bên, cục đất bắn lên rơi, đá nảy. sc: cỡ; n: số cục đất
        void KhDatToe(Vector2 dat, float H, float sc, int n, bool da = true)
        {
            Ripple(dat + new Vector2(0, 2), 0.05f * H, 0.5f * H * sc, 0.45f, KhBuiC2);
            // khung vẽ sẵn (2026-11-19): đất nổ to (sc ≥ 0,85: cắm hố, trồi lên, húc) thì bụi là hai cụm khung "khoi" nhuộm nâu đất (KmBuiFb,
            // HatFbKim.cs) thay vòng cụm bụi rời; cục đất, đá giữ
            bool fb = sc >= 0.85f && KmBuiFb(dat, H, sc);
            for (int i = 0; i < (fb ? 0 : Mathf.RoundToInt(6 * sc)); i++)
            {
                float sd = (i & 1) == 0 ? 1 : -1;
                KhBui(dat + new Vector2(sd * U(4, 0.24f * H) * sc, U(-5, 2)), new Vector2(sd * U(90, 260) * sc, -U(20, 110)), U(0.5f, 0.85f), 6,
                    U(15, 26) * sc, (i & 2) == 0 ? Back : Front);
            }
            for (int i = 0; i < n; i++)
            {
                float a = Mathf.Lerp(-150, -30, (i + U(0, 0.8f)) / n) * Mathf.Deg2Rad;       // toả đều nửa trên
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                KhDam(dat + new Vector2(U(-0.12f, 0.12f) * H * sc, -4), d * U(260, 500) * sc, U(0.5f, 0.8f), U(6f, 10f) * Mathf.Sqrt(sc), KhDat,
                    KhDat2, (i & 1) == 0 ? Back : Front);
            }
            if (da)
                for (int i = 0; i < Mathf.RoundToInt(2 * sc); i++)
                    Rock(dat + new Vector2(U(-0.15f, 0.15f) * H, -6), new Vector2(U(-200, 200), -U(260, 440)) * sc, dat.y + U(-4, 6), U(16, 24) * sc);
        }

        // một cú găm của mảnh quặng (chiêu mana) / chỗ húc: chớp nhỏ, tia, dăm quặng theo màu dạng
        void KhGam(Vector2 c, Vector2 d, float tH, float sc, int dang)
        {
            Color c1 = dang == 2 ? KhDo : KhSat, c2 = dang == 2 ? KhDo2 : KhSat2;
            KmBong(c - d * 0.04f * tH, -d + new Vector2(0, -0.2f), 0.3f * tH * sc, 0.1f, KmBac);   // bông va chạm toé ngược (2026-11-18)
            BurstFlash(c, 0.3f * tH * sc);
            for (int i = 0; i < Mathf.RoundToInt(4 * sc); i++)   // tia bắn nhanh rồi khựng
            {
                float a = U(0, 6.28f);
                var dd = (new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f) - d * 0.6f).normalized;
                KmTiaLua(c, dd, U(360, 640) * sc, U(6, 9), (i & 1) == 0 ? KmBac[4] : KmBac[3]);
            }
            for (int i = 0; i < Mathf.RoundToInt(5 * sc); i++)
            {
                float a = U(0, 6.28f);
                KhDam(c + U2(-6, 6), (new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.5f) - d * 0.4f) * U(170, 330) * sc, U(0.4f, 0.65f),
                    U(6f, 9f) * Mathf.Sqrt(sc), c1, c2);
            }
        }

        // ĐÒN THƯỜNG. lead: giây tới khung trúng (dạng 1: húc 0,46; dạng 2: giáng 0,92)
        public float NKhoangHuc(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead);
            bool d2 = L > 0.7f;
            int dang = d2 ? 2 : 1;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var d = new Vector2(dir, 0);
            if (!d2)
            {
                var c = foeBody + new Vector2(-dir * 0.24f * tH, 0.06f * tH);
                At(L, () =>
                {
                    Shake?.Invoke(0.3f);
                    KhGam(c, d, tH, 1.1f, 1);
                    for (int i = 0; i < 3; i++)
                    {
                        float sd = (i & 1) == 0 ? 1 : -1;
                        KhBui(foeFeet + new Vector2(sd * U(6, 0.25f * tH), U(-5, 2)), new Vector2(sd * U(100, 240), -U(10, 50)), 0, 5, 17, Back);
                    }
                });
                return L;
            }
            float k = L / KhGiang;
            // nhát húc (không phải khung trúng của game): chớp nhỏ + tia ở mép trước thân đối thủ
            At(KhHuc * k, () =>
            {
                Shake?.Invoke(0.15f);
                KhGam(foeBody + new Vector2(-dir * 0.26f * tH, 0.05f * tH), d, tH, 0.75f, dang);
            });
            // lộn qua đầu: vài hạt bụi bị hất lên lúc bật
            At((KhHuc + 0.08f) * k, () =>
            {
                for (int i = 0; i < 3; i++)
                    KhBui(foeFeet + new Vector2(-dir * U(0.1f, 0.35f) * tH, U(-4, 2)), new Vector2(-dir * U(40, 120), -U(30, 80)), 0, 5, 15, Back);
            });
            // CÚ GIÁNG: đè từ trên xuống đầu đối thủ, sóng đất dưới chân nó
            At(L, () =>
            {
                Shake?.Invoke(0.55f);
                var c = foeBody + new Vector2(-dir * 0.1f * tH, -0.3f * tH);
                SatChop(c, 0.62f * tH);
                KhGam(c, new Vector2(0, -1), tH, 1.25f, dang);
                RingN(foeFeet + new Vector2(0, 2), 0.32f, 0.08f * tH, 0.6f * tH, KhBuiC, 0.3f, Floor, 30.6f);
                KhDatToe(foeFeet, tH, 0.9f, 6);
            });
            return L;
        }

        // CHIÊU MANA: từng mảnh quặng găm vào đối thủ. dang: 1 (hai tay) / 2 (hai tay + năm gai)
        public float NKhoangBan(Vector2 casterFeet, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float L = Mathf.Max(0.05f, lead);
            float k = L / KhBanTrung;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var d = new Vector2(dir, 0);
            var ts = dang == 2 ? KhBan2 : KhBan1;
            for (int i = 0; i < ts.Length; i++)
            {
                int j = i;
                bool cuoi = j == ts.Length - 1;
                // tay găm giữa thân, gai găm cao hơn chút; tản hẹp quanh đích (mảnh của rig cũng găm quanh đó)
                var c = foeBody + new Vector2(-dir * U(0.05f, 0.18f) * tH, (j < 2 ? U(-0.05f, 0.08f) : U(-0.2f, 0.02f)) * tH);
                At(Mathf.Max(0.02f, ts[j] * k), () =>
                {
                    Shake?.Invoke(cuoi ? 0.45f : 0.18f);
                    if (j > 0) KmNhip(cuoi ? 0.8f : 0.4f);   // mảnh đầu là cú trúng chính (StageView)
                    KhGam(c, d, tH, cuoi ? 1.2f : 0.8f, dang);
                    if (cuoi)
                    {
                        Ripple(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.5f * tH, 0.45f, KhBuiC2);
                        for (int q = 0; q < 4; q++)
                        {
                            float sd = (q & 1) == 0 ? 1 : -1;
                            KhBui(foeFeet + new Vector2(sd * U(6, 0.25f * tH), U(-5, 2)), new Vector2(sd * U(100, 240), -U(10, 60)), 0, 5, 17, Back);
                        }
                    }
                });
            }
            return Mathf.Max(0.02f, ts[0] * k);
        }

        // CHIÊU CUỐI: chui đất → gò chạy ngầm → trồi lên húc. lead: giây tới khung trúng (húc cuối). dang: 1 / 2
        public float NKhoangDao(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            int di = dang == 2 ? 1 : 0;
            float L = Mathf.Max(0.3f, lead);
            float k = L / KhHit[di];
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var dich = casterFeet + (foeFeet - casterFeet) * 0.72f;  // chỗ trồi = đỉnh cú lunge của sân (AolaSticker.Lunge)
            float H = casterH;
            // 1. mũi tinh thể cắm đất: đất toé
            At(KhDao * k, () =>
            {
                Shake?.Invoke(0.25f);
                KhDatToe(casterFeet, H, 0.85f, 8, false);
            });
            // thân chui xuống: đất phụt lên hai bên miệng hố
            Every(KhDao * k + 0.04f, 0.84f * k, 22, x =>
            {
                float sd = U(0, 1) < 0.5f ? 1 : -1;
                KhDam(casterFeet + new Vector2(sd * U(0.1f, 0.4f) * H, -4), new Vector2(sd * U(60, 200), -U(220, 380)), U(0.4f, 0.6f), U(5f, 8f),
                    KhDat, KhDat2, U(0, 1) < 0.5f ? Back : Front);
            });
            // gò nhô lên ở miệng hố
            At(KhGo * k, () =>
            {
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    KhBui(casterFeet + new Vector2(sd * U(0.1f, 0.4f) * H, U(-4, 2)), new Vector2(sd * U(60, 160), -U(20, 70)), 0, 5, 17, Back);
                }
            });
            // 2. chạy ngầm: gò đi theo cú lunge (êm vào êm ra); đất bị hất ra sau gò, bụi thấp bò theo
            System.Func<float, Vector2> go = s =>
            {
                float u = Mathf.Clamp01((s / k - KhChay0) / (KhChay1 - KhChay0));
                return Vector2.Lerp(casterFeet, dich, u * u * (3 - 2 * u));
            };
            float tc0 = KhChay0 * k;
            Every(tc0, KhChay1 * k, 26, x =>
            {
                var at = go(tc0 + x * (KhChay1 - KhChay0) * k);
                KhDam(at + new Vector2(-dir * U(0.05f, 0.35f) * H, -U(2, 10)), new Vector2(-dir * U(80, 240), -U(180, 340)), U(0.35f, 0.55f),
                    U(5f, 8f), KhDat, KhDat2, U(0, 1) < 0.5f ? Back : Front);
                if (U(0, 1) < 0.5f)
                    KhBui(at + new Vector2(-dir * U(0.1f, 0.45f) * H, U(-4, 2)), new Vector2(-dir * U(30, 110), -U(10, 40)), U(0.45f, 0.7f), 5, U(13, 20), Back);
            });
            // 3. sắp trồi: sỏi rung, bụi rỉ quanh chỗ gò dừng
            Every((KhTroi - 0.14f) * k, KhTroi * k, 30, x =>
                KhDam(dich + new Vector2(U(-0.3f, 0.3f) * H, -4), new Vector2(U(-40, 40), -U(80, 160)), U(0.25f, 0.4f), U(4f, 6f), KhDat, KhDat2, Back));
            At((KhTroi - 0.12f) * k, () => Shake?.Invoke(0.15f));
            // 4. trồi lên: đất nổ tung
            At(KhTroi * k, () =>
            {
                Shake?.Invoke(0.5f);
                KhDatToe(dich, H, 1.1f, 12);
                RingN(dich + new Vector2(0, 2), 0.3f, 0.08f * H, 0.55f * H, KhBuiC, 0.3f, Floor, 30.6f);
            });
            if (dang == 2)
            {
                // húc lần một (không phải khung trúng của game), rơi lại xuống hố, đất nổ lần hai to hơn
                At(KhHuc1 * k, () =>
                {
                    Shake?.Invoke(0.3f);
                    KmNhip(1);   // húc lần một (trước cú trúng chính)
                    KhGam(foeBody + new Vector2(-dir * 0.22f * tH, 0.12f * tH), new Vector2(0, -1), tH, 0.9f, 2);
                });
                At(KhXuong * k, () => KhDatToe(dich, H, 0.6f, 5, false));
                Every((KhTroi2 - 0.1f) * k, KhTroi2 * k, 30, x =>
                    KhDam(dich + new Vector2(U(-0.3f, 0.3f) * H, -4), new Vector2(U(-40, 40), -U(80, 160)), U(0.25f, 0.4f), U(4f, 6f), KhDat, KhDat2, Back));
                At(KhTroi2 * k, () =>
                {
                    Shake?.Invoke(0.7f);
                    KhDatToe(dich, H, 1.35f, 14);
                    RingN(dich + new Vector2(0, 2), 0.34f, 0.1f * H, 0.7f * H, KhBuiC, 0.3f, Floor, 30.6f);
                });
            }
            // 5. HÚC (khung trúng): chớp ở chỗ chạm + vòng cột tinh thể trồi quanh đối thủ
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.2f * tH, 0.14f * tH);
                KhGam(c, new Vector2(0, -1), tH, dang == 2 ? 1.3f : 1.05f, dang);
                KhDap(foeFeet, foeBody, tH, dang == 2 ? 1f : 0.8f, dang);
            });
            // 6. rơi chạm đất, nhảy về chạm đất: bụi
            At(KhDapT[di] * k, () => KhDatToe(dich, H, 0.55f, 4, false));
            At(KhLui1[di] * k, () =>
            {
                for (int i = 0; i < 6; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    KhBui(casterFeet + new Vector2(sd * U(6, 0.3f * H), U(-5, 2)), new Vector2(sd * U(90, 220), -U(10, 60)), 0, 6, 18, (i & 2) == 0 ? Back : Front);
                }
            });
            return L;
        }
    }
}
