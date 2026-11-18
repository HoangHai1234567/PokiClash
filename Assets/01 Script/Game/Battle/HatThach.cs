// THIÊN THẠCH THÚ (suất cu_phu, ải 60 đảo Thổ, mini boss; 2026-11-17): quái thú đá đen mạch hổ phách, lưng rừng tinh thể ngọc lam,
// năm cụm thiên thạch bay quỹ đạo nguyên tử quanh người. Rig tinh_hach_1 (ArtGen/Spine/tinh_hach_rig.py, monster_3806; ghi chú
// ArtGen/Spine/inbox/tho9_ghichu.md; vào game: quai/doi_tinh_hach.py). Đi đường "n_" như bộ Thổ (HatTho.cs): phát lúc clip BẮT ĐẦU kèm
// lead (giờ trúng của clip); mốc dưới đây là giây của rig, co giãn theo k = lead / giờ trúng của rig. Thiên thạch, quả cầu là hình của
// rig (game lái bản sao bay tới đối thủ qua xương far / fly_*); ở đây chỉ tia ma sát, lửa, đá, bụi, nổ.
// DẠNG 1 "Thiên Thạch Thú Non" (2026-11-18): rig riêng tinh_hach_non (ghi chú ArtGen/Spine/inbox/tinh_hach_non_ghichu.md), cùng nhịp clip,
// ba thiên thạch, quả cầu nhỏ hơn: mã n_thach_xoay1 / n_thach_cau1 dùng bộ số ThtD1 (đòn thường n_thach_vo dùng chung hai dạng).
// Người dùng (lượt 3): "chiêu mana vẫn dùng 2 tay xoa nhau, các thiên thạch xung quanh bay nhanh hơn rồi lao vào người đối thủ";
// "chiêu cuối tướng cuộn người lại thành 1 quả bóng thiên thạch đầy gai ... bay lên cao, lao xuống người đối thủ như 1 viên thiên thạch,
// có hiệu ứng xé gió tạo lửa rồi nổ rất lớn".
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color ThtNgoc = C(72, 206, 190), ThtNgoc2 = C(170, 240, 228);   // tinh thể ngọc lam: mặt chính, mặt sáng

        // đánh thường: thu mình 0,28, bật vồ, ĐỚP 0,46 (= trúng), lắc đầu xé 0,59 / 0,72
        const float ThtDop = 0.46f, ThtBat = 0.28f, ThtXe1 = 0.59f, ThtXe2 = 0.72f;
        // chiêu mana: hai tay xoa 0,30 → 1,05; thiên thạch xoáy về trước đôi tay 0,80 → 1,05; phóng 1,05 + 0,08 j, bay 0,22 s; trúng 1,27
        const float ThtXoa0 = 0.30f, ThtXoa1 = 1.05f, ThtTu0 = 0.80f, ThtPhong0 = 1.05f, ThtPhongCach = 0.08f, ThtBay = 0.22f;
        const float ThtXoayT = ThtPhong0 + ThtBay;
        static readonly Vector2 ThtTay = new Vector2(-0.06f, 0.50f);                      // giữa hai bàn tay đang xoa
        static readonly Vector2 ThtTu = new Vector2(0.12f, 0.545f);                       // điểm thiên thạch xoáy về
        static readonly Vector2[] ThtS0 =                                                 // chỗ từng bản sao rời đi (xương fly_j)
        {
            new Vector2(0.171f, 0.548f), new Vector2(0.055f, 0.561f), new Vector2(0.155f, 0.524f), new Vector2(0.086f, 0.581f), new Vector2(0.115f, 0.512f)
        };
        // chiêu cuối: cuộn thành cầu 0,36; quay tại chỗ tới 1,00; vọt lên 1,00 → 1,36; LỬA lao xuống 1,36 → 1,70; NỔ 1,70 (= trúng); nảy về
        // tới 2,05, bung người 2,12, đáp 2,50
        const float ThtCuon = 0.36f, ThtLen = 1.00f, ThtDinh = 1.36f, ThtNo = 1.70f, ThtNay = 2.05f, ThtVe = 2.50f;
        const float ThtRCau = 0.39f;                                                      // bán kính quả cầu (chiều cao tướng)
        // tâm quả cầu theo giờ clip (bước 0,05 s): x = phần cú lao của move (1 = đỉnh lao game nắn vào 72 % quãng tới đối thủ, AolaSticker.
        // Lunge), y, z = tâm so với move (chiều cao tướng; x về phía đối thủ, y lên). Đo bằng ArtGen/Spine sau lần xuất 2026-11-17.
        static readonly Vector3[] ThtCau =
        {
            new Vector3(0.000f, -0.022f, 0.551f), new Vector3(0.000f, -0.022f, 0.551f), new Vector3(0.000f, -0.022f, 0.551f), new Vector3(0.000f, -0.022f, 0.551f),
            new Vector3(0.000f, -0.022f, 0.551f), new Vector3(0.000f, -0.022f, 0.551f), new Vector3(0.000f, -0.022f, 0.551f), new Vector3(0.000f, -0.022f, 0.551f),
            new Vector3(0.000f, -0.022f, 0.553f), new Vector3(0.000f, -0.022f, 0.565f), new Vector3(0.000f, -0.022f, 0.573f), new Vector3(0.000f, -0.022f, 0.582f),
            new Vector3(0.000f, -0.022f, 0.599f), new Vector3(0.000f, -0.022f, 0.609f), new Vector3(0.000f, -0.022f, 0.611f), new Vector3(0.000f, -0.022f, 0.609f),
            new Vector3(0.000f, -0.022f, 0.595f), new Vector3(0.000f, -0.022f, 0.576f), new Vector3(0.000f, -0.022f, 0.567f), new Vector3(0.000f, -0.022f, 0.553f),
            new Vector3(0.000f, -0.022f, 0.551f), new Vector3(-0.068f, -0.022f, 1.171f), new Vector3(-0.093f, -0.022f, 1.392f), new Vector3(-0.126f, -0.022f, 1.692f),
            new Vector3(-0.136f, -0.022f, 1.783f), new Vector3(-0.146f, -0.022f, 1.878f), new Vector3(-0.148f, -0.022f, 1.895f), new Vector3(-0.149f, -0.022f, 1.900f),
            new Vector3(-0.147f, -0.022f, 1.899f), new Vector3(-0.109f, -0.022f, 1.859f), new Vector3(-0.058f, -0.022f, 1.807f), new Vector3(0.024f, -0.022f, 1.722f),
            new Vector3(0.309f, -0.022f, 1.426f), new Vector3(0.807f, -0.022f, 0.910f), new Vector3(1.154f, -0.022f, 0.551f), new Vector3(1.154f, -0.022f, 0.551f),
            new Vector3(0.871f, -0.022f, 0.813f), new Vector3(0.682f, -0.022f, 0.987f), new Vector3(0.626f, -0.022f, 1.039f), new Vector3(0.570f, -0.022f, 1.090f),
            new Vector3(0.561f, -0.022f, 1.099f), new Vector3(0.556f, -0.022f, 1.101f), new Vector3(0.539f, -0.022f, 1.100f), new Vector3(0.508f, -0.022f, 1.098f),
            new Vector3(0.414f, -0.022f, 1.081f), new Vector3(0.295f, -0.022f, 1.040f), new Vector3(0.233f, -0.022f, 1.007f), new Vector3(0.173f, -0.022f, 0.964f),
            new Vector3(0.070f, -0.022f, 0.842f), new Vector3(0.009f, -0.022f, 0.664f), new Vector3(0.000f, -0.022f, 0.551f),
        };

        // Bộ số theo DẠNG: dạng 1 "Thiên Thạch Thú Non" (2026-11-18) là rig riêng tinh_hach_non (đầu to, ba thiên thạch, quả cầu nhỏ hơn,
        // cùng nhịp clip). Đo bằng ArtGen/Spine/tinh_hach_do_hat.py (TH_DANG=non); script đo lại đúng từng số bảng dạng 2 ở trên (Tay, Tu
        // của dạng 2 đã chỉnh tay +0,029 / −0,008 và +0,009 / −0,003 so với số đo: dạng 1 cộng cùng độ lệch). muc: độ mạnh nổ, rung, chớp.
        sealed class ThtDang
        {
            public Vector2 tay, tu;
            public Vector2[] s0;
            public Vector3[] cau;
            public float rCau, muc;
        }
        static readonly ThtDang ThtD2 = new ThtDang { tay = ThtTay, tu = ThtTu, s0 = ThtS0, cau = ThtCau, rCau = ThtRCau, muc = 1f };
        static readonly Vector3[] ThtCau1 =
        {
            new Vector3(0.000f, 0.055f, 0.528f), new Vector3(0.000f, 0.055f, 0.528f), new Vector3(0.000f, 0.055f, 0.528f), new Vector3(0.000f, 0.055f, 0.528f),
            new Vector3(0.000f, 0.055f, 0.528f), new Vector3(0.000f, 0.055f, 0.528f), new Vector3(0.000f, 0.055f, 0.528f), new Vector3(0.000f, 0.055f, 0.528f),
            new Vector3(0.000f, 0.055f, 0.530f), new Vector3(0.000f, 0.055f, 0.542f), new Vector3(0.000f, 0.055f, 0.550f), new Vector3(0.000f, 0.055f, 0.559f),
            new Vector3(0.000f, 0.055f, 0.576f), new Vector3(0.000f, 0.055f, 0.587f), new Vector3(0.000f, 0.055f, 0.588f), new Vector3(0.000f, 0.055f, 0.586f),
            new Vector3(0.000f, 0.055f, 0.573f), new Vector3(0.000f, 0.055f, 0.553f), new Vector3(0.000f, 0.055f, 0.544f), new Vector3(0.000f, 0.055f, 0.530f),
            new Vector3(0.000f, 0.055f, 0.528f), new Vector3(-0.068f, 0.055f, 1.148f), new Vector3(-0.093f, 0.055f, 1.370f), new Vector3(-0.126f, 0.055f, 1.669f),
            new Vector3(-0.136f, 0.055f, 1.760f), new Vector3(-0.146f, 0.055f, 1.855f), new Vector3(-0.148f, 0.055f, 1.872f), new Vector3(-0.149f, 0.055f, 1.878f),
            new Vector3(-0.147f, 0.055f, 1.876f), new Vector3(-0.109f, 0.055f, 1.836f), new Vector3(-0.058f, 0.055f, 1.784f), new Vector3(0.024f, 0.055f, 1.699f),
            new Vector3(0.309f, 0.055f, 1.403f), new Vector3(0.807f, 0.055f, 0.888f), new Vector3(1.154f, 0.055f, 0.528f), new Vector3(1.154f, 0.055f, 0.528f),
            new Vector3(0.871f, 0.055f, 0.790f), new Vector3(0.682f, 0.055f, 0.964f), new Vector3(0.626f, 0.055f, 1.016f), new Vector3(0.570f, 0.055f, 1.067f),
            new Vector3(0.561f, 0.055f, 1.076f), new Vector3(0.556f, 0.055f, 1.078f), new Vector3(0.539f, 0.055f, 1.077f), new Vector3(0.508f, 0.055f, 1.075f),
            new Vector3(0.414f, 0.055f, 1.058f), new Vector3(0.295f, 0.055f, 1.017f), new Vector3(0.233f, 0.055f, 0.984f), new Vector3(0.173f, 0.055f, 0.941f),
            new Vector3(0.070f, 0.055f, 0.819f), new Vector3(0.009f, 0.055f, 0.642f), new Vector3(0.000f, 0.055f, 0.528f),
        };
        static readonly ThtDang ThtD1 = new ThtDang
        {
            tay = new Vector2(-0.111f, 0.487f), tu = new Vector2(0.069f, 0.532f),
            s0 = new[] { new Vector2(0.120f, 0.535f), new Vector2(0.006f, 0.519f), new Vector2(0.096f, 0.564f) },
            cau = ThtCau1, rCau = 0.337f, muc = 0.75f
        };

        // tâm quả cầu trên sân ở giây clip tr (rig): chân + cú lao đã nắn (V = 72 % quãng tới đối thủ) + tâm so với move
        static Vector2 ThtCauSan(Vector3[] cau, Vector2 feet, float H, float dir, Vector2 V, float tr)
        {
            float f = Mathf.Clamp(tr / 0.05f, 0, cau.Length - 1.001f);
            int i = (int)f;
            var v = Vector3.Lerp(cau[i], cau[Mathf.Min(cau.Length - 1, i + 1)], f - i);
            return feet + V * v.x + new Vector2(dir * v.y * H, -v.z * H);
        }

        // mảnh tinh thể văng (ngọc lam hoặc hổ phách): giọt nhọn chĩa theo hướng bay, rơi có trọng lực, lật theo đường bay, mờ ở 30% cuối
        P ThtManh(Vector2 pos, Vector2 vel, float len, bool ngoc, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = U(0.5f, 0.8f), acc = new Vector2(0, 900), drag = 1.2f, sz = len, wd = 0.42f * len, group = group,
                col = ngoc ? ThtNgoc : ToPhach
            };
            p.draw = (q, k, buf) =>
            {
                float a = 1 - SmoothStep(0.7f, 1, k);
                if (a < 0.03f) return;
                var d = Unit(q.vel);
                var n = new Vector2(-d.y, d.x);
                float ang = TipAngle(d);
                bool ng = q.col == ThtNgoc;
                Put(buf, q.group, 47, S("needles_0"), Ink, q.pos, q.sz + 5, (q.wd + 5) / (q.sz + 5), ang, a);
                Put(buf, q.group, 47.1f, S("needle_0"), q.col, q.pos, q.sz, q.wd / q.sz, ang, a);
                Put(buf, q.group, 47.2f, S("needle_0"), ng ? ThtNgoc2 : ToPhach2, q.pos + n * (0.18f * q.wd) + d * (0.05f * q.sz), 0.72f * q.sz,
                    0.32f * q.wd / (0.72f * q.sz), ang, a);
            };
            return Add(p);
        }

        // tia ma sát / vệt gió màu riêng (Spark nhuộm theo chủ đề; ở đây đặt màu)
        P ThtTia(Vector2 pos, Vector2 dir, float speed, Color col, float life, float size, float grav = 400, int group = Front)
        {
            var p = Spark(pos, dir, speed, life, size, grav, group);
            p.col = col;
            return p;
        }

        // một thiên thạch đâm trúng: chớp sao kem, dăm đá + tinh thể văng nửa trên, lửa nhỏ (thẻ gây cháy), bụi
        void ThtTrung(Vector2 c, Vector2 foeFeet, float tH, float muc)
        {
            float sc = tH / 150f;
            ToNo(c, foeFeet.y, tH, muc, ToDa, ToDa2);
            Explode(c, 0.3f * muc, tH);
            int n = Mathf.RoundToInt(4 * muc);
            for (int i = 0; i < n; i++)
            {
                float a = -Mathf.PI / 2 + ((i + 0.5f) / n - 0.5f) * 2.4f + U(-0.2f, 0.2f);
                ThtManh(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(220, 380) * sc, U(10, 15) * sc * (0.8f + 0.2f * muc), (i & 1) == 0,
                    (i & 2) == 0 ? Front : Back);
            }
        }

        // ĐÒN THƯỜNG "Vồ xé" (rig khai đánh thường lao): bụi, sỏi bật lùi lúc phóng; ĐỚP: vết cắn lớn, chớp, dăm đá + tinh thể; hai nhịp xé
        public float NThachVo(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead), k = L / ThtDop, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sH = casterH / 150f, sc = tH / 150f;
            At(ThtBat * k, () =>
            {
                for (int i = 0; i < 4; i++)
                    ToBui(casterFeet + new Vector2(dir * U(-0.25f, 0.2f) * casterH, U(-6, 2)), new Vector2(-dir * U(70, 180), -U(15, 60)) * sH, 0, 6 * sH, 16 * sH, Back);
                for (int i = 0; i < 3; i++)
                    ToSoi(casterFeet + new Vector2(dir * U(-0.1f, 0.2f) * casterH, -4), new Vector2(-dir * U(80, 200), -U(180, 300)) * sH, U(3, 5) * sH, ToDa,
                        casterFeet.y + U(-2, 4));
            });
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.1f * tH, 0.04f * tH);
                ToCan(c, tH * 1.3f);
                ToNo(c, foeFeet.y, tH, 1.4f, ToDa, ToDa2);
                for (int i = 0; i < 4; i++)
                {
                    float a = -Mathf.PI / 2 + (i - 1.5f) * 0.55f;
                    ThtManh(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(220, 340) * sc, U(10, 14) * sc, (i & 1) == 0);
                }
                ToVong(foeFeet, 70 * sc);
            });
            foreach (float tx in new[] { ThtXe1, ThtXe2 })
                At(tx * k, () => ToNo(foeBody + new Vector2(U(-0.12f, 0.12f) * tH, U(-0.1f, 0.1f) * tH), foeFeet.y, tH, 0.5f, ToDa, ToDa2));
            return L;
        }

        // CHIÊU MANA "Thiên thạch xoáy": HAI TAY XOA (tia lửa đá hổ phách / ngọc lam toé giữa hai bàn tay, chớp nhỏ theo nhịp miết); mảnh tinh
        // thể bị hút về trước đôi tay lúc thiên thạch xoáy về; NĂM thiên thạch lần lượt lao vào đối thủ: lửa đuôi, tia, khói mỏng theo đúng
        // đường bay của bản sao trong rig; mỗi viên trúng: dăm đá, tinh thể, lửa nhỏ (viên cuối to hơn)
        public float NThachXoay(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            ThtXoay(ThtD2, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        // dạng 1 (Thiên Thạch Thú Non): ba thiên thạch, nhẹ hơn
        public float NThachXoay1(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            ThtXoay(ThtD1, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        float ThtXoay(ThtDang d, Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / ThtXoayT, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sH = casterH / 150f, sc = tH / 150f;
            var s0 = d.s0;
            var tay = ToSan(casterFeet, casterH, dir, d.tay);
            Every(ThtXoa0 * k, ThtXoa1 * k, 30, x =>
            {
                float a = U(-2.6f, -0.4f);
                var d = new Vector2(dir * Mathf.Cos(a), Mathf.Sin(a));
                ThtTia(tay + U2(-6, 6) * sH, d, U(170, 320) * sH, U(0, 1) < 0.5f ? ToPhach2 : ThtNgoc2, U(0.16f, 0.28f), 7 * sH, 520);
            });
            for (int i = 0; i < 5; i++)
                At((ThtXoa0 + 0.06f + 0.16f * i) * k, () => ToChop(tay + U2(-5, 5) * sH, 0.10f * casterH, Front, 0.08f));
            var tu = ToSan(casterFeet, casterH, dir, d.tu);
            At(ThtTu0 * k, () =>
            {
                for (int i = 0; i < 14; i++)
                {
                    float a = U(0, 6.28f), r = U(0.45f, 0.75f) * casterH;
                    var p0 = tu + new Vector2(Mathf.Cos(a) * r, Mathf.Sin(a) * r * 0.7f);
                    ToHut(p0, _ => tu, U(0.18f, 0.25f) * k, U(2.5f, 4) * sH, (i & 1) == 0 ? ThtNgoc : ToPhach, 2.2f);
                }
            });
            for (int j = 0; j < s0.Length; j++)
            {
                int jj = j;
                float t0 = (ThtPhong0 + ThtPhongCach * j) * k, tb = ThtBay * k;
                var a0 = ToSan(casterFeet, casterH, dir, s0[j]);
                var v = foeBody - a0;
                var nn = dir * new Vector2(v.y, -v.x).normalized;
                float sgn = (j & 1) == 1 ? 1 : -1;
                float tStart = T + t0;
                Vector2 Duong(float tt)
                {
                    float f = Mathf.Clamp01((tt - tStart) / tb);
                    f *= f;
                    return a0 + v * f + nn * (0.05f * casterH * Mathf.Sin(Mathf.PI * f) * sgn);
                }
                var dv = Unit(v);
                Every(t0, t0 + tb, 80, x =>
                {
                    var p = Duong(T);
                    var q = Flame(p + U2(-4, 4) * sH, -dv * U(40, 120) * sH + U2(-30, 30) * sH, U(0.16f, 0.24f), 8 * sH, U(13, 17) * sH, "tron", Th.pal,
                        U(0, 1) < 0.6f ? Back : Front, 3, -120, 1.4f, 0.15f, 0.1f);
                    Tongue(q, 1, 0.1f);
                });
                Every(t0, t0 + tb, 30, x => ThtTia(Duong(T), -dv + U2(-0.5f, 0.5f), U(120, 260) * sH, U(0, 1) < 0.5f ? ToPhach2 : ThtNgoc2, U(0.12f, 0.2f), 7 * sH, 200));
                Every(t0, t0 + tb, 24, x => Smoke(Duong(T) - dv * 10 * sH, -dv * 20 + U2(-10, 10), U(0.5f, 0.8f), 4 * sH, 10 * sH, Back, "dark", 0.15f));
                At(t0 + tb, () =>
                {
                    bool cuoi = jj == s0.Length - 1;
                    ThtTrung(foeBody + new Vector2(U(-0.12f, 0.12f) * tH, U(-0.12f, 0.08f) * tH), foeFeet, tH, (cuoi ? 1.5f : 0.9f) * d.muc);
                    if (jj > 0) Shake?.Invoke((cuoi ? 0.25f : 0.12f) * d.muc);
                });
            }
            At((ThtPhong0 + ThtPhongCach * (s0.Length - 1) + ThtBay) * k + 0.05f, () => ToVong(foeFeet, 85 * sc, 0.5f));
            return L;
        }

        // CHIÊU CUỐI "Quả cầu thiên thạch": cuộn người (bụi bung che lúc đổi hình) → quả cầu quay tại chỗ (bụi, sỏi, tia ma sát hất ra sau) →
        // vọt lên (đất phụt, vòng bụi) → LAO XUỐNG: lửa xé gió bùng quanh mặt trước quả cầu, đuôi sao chổi lửa + khói, vệt gió kem → NỔ RẤT LỚN
        // ngay đối thủ (lõi lửa sau lưng nó, vành lưỡi lửa, cột lửa, hai vòng sóng, đá + tinh thể văng, vết nứt toả, vành khói, nấm khói, hai
        // nổ phụ) → nảy về kéo than, khói → đáp (vòng bụi)
        public float NThachCau(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            ThtCauChieu(ThtD2, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        // dạng 1 (Thiên Thạch Thú Non): quả cầu nhỏ hơn, nổ nhẹ hơn (muc)
        public float NThachCau1(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead) =>
            ThtCauChieu(ThtD1, casterFeet, casterH, foeFeet, foeBody, tH, lead);

        float ThtCauChieu(ThtDang d, Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / ThtNo, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sH = casterH / 150f, sc = tH / 150f;
            var V = (foeFeet - casterFeet) * 0.72f;
            float tGoi = T, rb = d.rCau * casterH, m = d.muc;
            Vector2 Cau(float tt) => ThtCauSan(d.cau, casterFeet, casterH, dir, V, (tt - tGoi) / k);
            // cuộn người: bụi bung che chỗ đổi hình
            At((ThtCuon - 0.05f) * k, () =>
            {
                var c = Cau(T);
                for (int i = 0; i < 10; i++)
                {
                    float a = 6.28f * (i + U(-0.3f, 0.3f)) / 10;
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f);
                    ToBui(c + d * rb * 0.75f, d * U(70, 140) * sH, U(0.45f, 0.6f), 9 * sH, 24 * sH, (i & 1) == 0 ? Front : Back);
                }
                for (int i = 0; i < 6; i++)
                    ThtManh(c, new Vector2(U(-1, 1), -U(0.4f, 1)) * U(160, 260) * sH, U(8, 12) * sH, (i & 1) == 0);
            });
            // quay tại chỗ: bụi, sỏi, tia ma sát hất ra sau từ chân quả cầu
            Every(ThtCuon * k, ThtLen * k, x => 22 + 26 * x, x =>
            {
                var c = Cau(T);
                var chan = new Vector2(c.x - dir * 0.2f * rb, casterFeet.y - 3);
                ToBui(chan + U2(-6, 6) * sH, new Vector2(-dir * U(80, 200), -U(20, 80)) * sH, U(0.4f, 0.6f), 5 * sH, 14 * sH, U(0, 1) < 0.5f ? Back : Front);
                if (U(0, 1) < 0.3f)
                    ToSoi(chan, new Vector2(-dir * U(120, 260), -U(150, 280)) * sH, U(2.5f, 4.5f) * sH, U(0, 1) < 0.5f ? ToDa : ToDa2, casterFeet.y + U(-2, 4));
                if (U(0, 1) < 0.6f)
                    ThtTia(chan, new Vector2(-dir, -U(0.3f, 1)), U(200, 360) * sH, U(0, 1) < 0.6f ? ToPhach2 : ToKem, U(0.14f, 0.24f), 7 * sH, 600);
            });
            // vọt lên
            At(ThtLen * k, () =>
            {
                var chan = new Vector2(Cau(T).x, casterFeet.y);
                ToVong(chan, 110 * sH, 0.55f);
                for (int i = 0; i < 7; i++)
                    ToSoi(chan + new Vector2(U(-0.25f, 0.25f) * casterH, -4), new Vector2(U(-160, 160), -U(300, 520)) * sH, U(3.5f, 6) * sH,
                        i % 3 == 0 ? ToDa2 : ToDa, casterFeet.y + U(-2, 6), 0, (i & 1) == 0 ? Front : Back);
                for (int i = 0; i < 4; i++)
                {
                    float d = (i & 1) == 0 ? -1 : 1;
                    ToBui(chan + new Vector2(d * U(10, 50) * sH, -U(4, 24) * sH), new Vector2(d * U(50, 120), -U(30, 90)) * sH, 0, 7 * sH, 18 * sH,
                        (i & 1) == 0 ? Front : Back);
                }
                Shake?.Invoke(0.18f);
            });
            // LAO XUỐNG: bùng lửa lúc bắt đầu rơi, rồi lửa xé gió dày dần theo tốc độ
            At((ThtDinh + 0.02f) * k, () =>
            {
                var c = Cau(T);
                ToChop(c, 0.22f * casterH, Front, 0.1f);
                for (int i = 0; i < 12; i++)
                {
                    float a = 6.28f * (i + U(-0.3f, 0.3f)) / 12;
                    Tongue(Flame(c + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * rb * 0.8f, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(120, 220) * sH,
                        U(0.24f, 0.34f), 10 * sH, U(18, 24) * sH, "tron", Th.pal, (i & 1) == 0 ? Back : Front, 4, -160, 1.6f, 0.2f), 1, 0.15f);
                }
            });
            Vector2 Huong(float tt) => Unit(Cau(tt + 0.02f) - Cau(tt - 0.02f));
            Every(ThtDinh * k, ThtNo * k, x => 50 + 110 * x, x =>
            {
                var c = Cau(T);
                var dv = Huong(T);
                var bn = new Vector2(-dv.y, dv.x);
                bool truoc = U(0, 1) < 0.35f;
                var p = c + dv * rb * U(0.15f, 0.95f) + bn * rb * U(-0.85f, 0.85f);
                var q = Flame(p, -dv * U(60, 180) * sH + bn * U(-90, 90) * sH, U(0.2f, 0.32f), (truoc ? 9 : 12) * sH, (truoc ? U(16, 21) : U(22, 30)) * sH,
                    "tron", Th.pal, truoc ? Front : Back, 3, -100, 1.7f, 0.25f, 0.15f);
                Tongue(q, 1, 0.08f);
                q.smokeGroup = Back;
            });
            Every(ThtDinh * k, ThtNo * k, 34, x =>
            {
                var dv = Huong(T);
                Smoke(Cau(T) - dv * rb * 0.9f + U2(-8, 8) * sH, -dv * 30 + U2(-15, 15), U(0.8f, 1.2f), 7 * sH, 18 * sH, Back);
            });
            Every(ThtDinh * k, ThtNo * k, 40, x =>
            {
                var dv = Huong(T);
                var bn = new Vector2(-dv.y, dv.x);
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                ThtTia(Cau(T) + bn * sd * rb * U(0.9f, 1.2f), -dv, U(380, 560) * sH, ToKem, U(0.1f, 0.16f), 11 * sH, 0, sd > 0 ? Front : Back);
            });
            Every(ThtDinh * k, ThtNo * k, 22, x => Ember(Cau(T) + U2(-rb, rb) * 0.6f, -Huong(T) * U(60, 140) * sH, U(0.5f, 0.8f), 9 * sH));
            // NỔ RẤT LỚN
            At(L, () =>
            {
                var c = Vector2.Lerp(Cau(T), foeBody, 0.55f);
                var dat = new Vector2(c.x, foeFeet.y);
                Shake?.Invoke(0.9f * m);
                FlashScreen?.Invoke(new Color(1, 0.96f, 0.84f, 0.5f * m));
                Explode(c, 1.4f * m, tH, Back);
                Explode(c + new Vector2(0, 0.05f * tH), 0.55f * m, tH, Front);
                int nVanh = Mathf.RoundToInt(20 * m);
                for (int i = 0; i < nVanh; i++)
                {
                    float a = -180f * (i + U(-0.3f, 0.3f)) / (nVanh - 1) * Mathf.Deg2Rad;      // vành lưỡi lửa nửa trên, rải đều
                    var q = Flame(dat + U2(-10, 10) * sc, new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 1.1f) * U(320, 680) * sc, U(0.45f, 0.7f), 15 * sc, U(28, 40) * sc,
                        "tron", Th.pal, Back, 4, -200, 1.5f, 0.35f);
                    Tongue(q, 1, 0.2f);
                }
                for (int i = 0; i < 12; i++)
                {
                    float a = U(-170, -10) * Mathf.Deg2Rad;
                    Flame(dat, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * 540 * sc, 0.32f, 8 * sc, 20 * sc, "nhon", Th.pal, Back, 5, -150, 1, 0);
                }
                foreach (int sd in new[] { -1, 1 })
                    for (int i = 0; i < 3; i++)
                        Tongue(Flame(dat + new Vector2(sd * U(10, 30), 6) * sc, new Vector2(sd * U(250, 420), -30) * sc, 0.35f, 8 * sc, U(13, 18) * sc, "tron",
                            Th.pal, Front, 4, -200, 1.3f, 0), 0.4f, 0.6f);
                Every(0, 0.45f, x => 110 * (1 - 0.5f * x), x =>                      // cột lửa ôm thân đối thủ
                {
                    float th = U(0, 6.28f);
                    bool fr = Mathf.Sin(th) > 0.4f;
                    var q = Flame(foeFeet + new Vector2(0.4f * tH * Mathf.Cos(th), 12 * sc * Mathf.Sin(th) - 4), new Vector2(Mathf.Cos(th) * 40, -U(420, 680)) * sc,
                        U(0.32f, 0.5f), 9 * sc, U(20, 28) * sc * (fr ? 0.6f : 1), "tron", Th.pal, fr ? Front : Back, 2.2f, -200, 1.7f, 0.1f, 0.15f);
                    Tongue(q, 1, 0.5f);
                    q.smokeGroup = Back;
                });
                Ring(dat + new Vector2(0, 2), 0.42f, 0.2f * tH, 1.8f * m * tH, Th.ring);
                At(0.1f, () => Ring(dat + new Vector2(0, 2), 0.36f, 0.1f * tH, 1.3f * m * tH, Th.ring2));
                ToVong(dat, 140 * m * sc, 0.6f);
                for (int i = 0; i < 12; i++)
                {
                    float a = (-90 + U(-75, 75)) * Mathf.Deg2Rad;
                    ToSoi(c + U2(-10, 10) * sc, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(300, 600) * sc, U(4.5f, 8) * sc, i % 3 == 0 ? ToDa2 : i % 3 == 1 ? ToDa : ToDa3,
                        foeFeet.y + U(-8, 16) * sc, 0, (i & 1) == 0 ? Front : Back);
                }
                for (int i = 0; i < 10; i++)
                {
                    float a = (-90 + U(-80, 80)) * Mathf.Deg2Rad;
                    ThtManh(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(300, 560) * sc, U(12, 18) * sc, (i & 1) == 0, (i & 2) == 0 ? Front : Back);
                }
                for (int i = 0; i < 14; i++) Spark(c + U2(-12, 12), new Vector2(U(-1, 1), -U(0.3f, 1)), U(300, 560) * sc);
                At(0.1f, () =>
                {
                    for (int i = 0; i < 10; i++) Spark(c + U2(-12, 12), new Vector2(U(-1, 1), -U(0.3f, 1)), U(300, 560) * sc);
                });
                for (int i = 0; i < 5; i++)
                {
                    float a = (i - 2) * 0.5f + U(-0.12f, 0.12f);
                    ToNut(dat, dat + new Vector2(Mathf.Sin(a) * U(0.8f, 1.1f) * tH, U(2, 10) * sc), 0.16f, sc);
                }
                for (int i = 0; i < 16; i++)
                {
                    float sd = U(0, 1) < 0.5f ? -1 : 1;
                    Smoke(dat + new Vector2(sd * U(15, 45), U(-6, 4)) * sc, new Vector2(sd * U(90, 260), -U(10, 50)) * sc, U(1.0f, 1.4f), 9 * sc, U(16, 22) * sc, Back);
                }
                for (int i = 0; i < 6; i++)
                    Smoke(c + new Vector2(U(-30, 30), -U(40, 80)) * sc, new Vector2(U(-40, 40), -U(140, 220)) * sc, U(1.2f, 1.5f), 14 * sc, 30 * sc, Back);
                for (int i = 0; i < 14; i++) Ash(c + U2(-40, 40) * sc, new Vector2(U(-80, 80), -U(80, 160)));
                At(0.13f, () =>
                {
                    Shake?.Invoke(0.4f * m);
                    Explode(c + new Vector2(dir * U(0.1f, 0.25f) * tH, -U(0.1f, 0.22f) * tH), 0.75f * m, tH, Back);
                });
                if (m >= 1) At(0.3f, () => Explode(c + new Vector2(-dir * U(0.05f, 0.2f) * tH, -U(0.0f, 0.15f) * tH), 0.55f, tH, Back));
            });
            // nảy về: than, khói mỏng theo quả cầu
            Every((ThtNo + 0.04f) * k, ThtNay * k, 26, x =>
            {
                var c = Cau(T);
                Ember(c + U2(-rb, rb) * 0.5f, new Vector2(U(-40, 40), U(-60, -20)) * sH, U(0.5f, 0.8f), 8 * sH);
                if (U(0, 1) < 0.5f) Smoke(c + U2(-rb, rb) * 0.4f, null, U(0.7f, 1.0f), 5 * sH, 13 * sH, Back);
            });
            // đáp về chỗ cũ
            At(ThtVe * k, () =>
            {
                ToVong(casterFeet, 100 * sH, 0.5f);
                for (int d = -1; d <= 1; d += 2)
                    ToBui(casterFeet + new Vector2(d * 0.3f * casterH, -4 * sH), new Vector2(d * 100, -30) * sH, 0, 7 * sH, 18 * sH);
                Shake?.Invoke(0.15f);
            });
            return L;
        }
    }
}
