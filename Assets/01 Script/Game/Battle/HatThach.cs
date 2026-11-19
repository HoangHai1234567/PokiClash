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
// KHUNG VẼ SẴN (2026-11-19, HatFlip.cs + HatFbTho.cs; chưa nhập ảnh hat_fb_* thì hạt cũ): đuôi thiên thạch mana và áo lửa quả cầu chiêu cuối là
// cầu lửa vẽ sẵn bám đường bay; viên trúng có lửa trúng vẽ sẵn sau thân; nổ chiêu cuối là nổ nấm vẽ sẵn + dung nham phun ở lớp đất; bụi, khói
// là cụm khói vẽ sẵn. Giữ: tia ma sát, mảnh tinh thể, dăm, chớp, sóng đất, hố, vết nứt, than, tro, mọi mốc và giờ trúng.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color ThtNgoc = C(79, 214, 200), ThtNgoc2 = C(186, 248, 238);   // tinh thể ngọc lam tươi #4FD6C8: mặt chính, mặt sáng

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

        // một thiên thạch đâm trúng: chớp sao kem, bông va chạm ngược hướng bay, dăm đá + tinh thể văng nửa trên, lửa nhỏ SAU thân (thẻ gây cháy;
        // không che con bị trúng), bụi cụm
        void ThtTrung(Vector2 c, Vector2 foeFeet, float tH, float muc, Vector2 huong = default)
        {
            float sc = tH / 150f;
            ToNo(c, foeFeet.y, tH, muc, ToDa, ToDa2, huong);
            // khung vẽ sẵn (2026-11-19): lửa trúng đích vẽ sẵn (khung vẽ đòn tới từ trái: thiên thạch bay sang trái thì lật), 0,7 tH viên thường,
            // 0,95 tH viên cuối; thay nổ lửa nhỏ / ba lưỡi lửa. Lớp TRƯỚC (người dùng xem trong game: "vài vụ nổ layer nằm dưới địch nên không thấy
            // rõ"), neo dời 0,14 tH về phía kẻ đánh cho bông lửa nằm ở mặt trước thân, đỡ che mặt
            if (HasFb("trung_lua"))
                Fb("trung_lua", huong.sqrMagnitude > 1e-4f ? c - Unit(huong) * (0.14f * tH) : c, (muc >= 1.1f ? 0.95f : 0.7f) * tH, Front, 30, 1.3f, 0, huong.x < 0);
            else if (muc >= 1.1f) Explode(c + new Vector2(0, -0.04f * tH), 0.24f * muc, tH, Back);   // viên cuối: nổ lửa nhỏ sau thân
            else
                for (int i = 0; i < 3; i++)                                      // viên thường: ba lưỡi lửa nhỏ sau thân (giữ ngân sách hạt)
                {
                    float a = -Mathf.PI * (0.25f + 0.25f * i) + U(-0.2f, 0.2f);
                    Tongue(Flame(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(140, 220) * sc, U(0.22f, 0.3f), 5 * sc, U(10, 13) * sc, "tron", Th.pal, Back, 4,
                        -160, 1.5f, 0.3f, 0.05f), 1, 0.2f);
                }
            int n = Mathf.RoundToInt(2 * muc);
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
                for (int d = 0; d < 2; d++)
                    ToCum(casterFeet + new Vector2(dir * (d == 0 ? -0.18f : 0.1f) * casterH, -4 * sH), new Vector2(-dir * U(80, 150), -U(20, 45)) * sH, 12 * sH, 3, Back);
                ToSoiCum(casterFeet + new Vector2(dir * 0.05f * casterH, -4), new Vector2(-dir * U(100, 180), -U(200, 280)) * sH, 3.4f * sH, ToDa, ToDa2,
                    casterFeet.y + U(-2, 4));
            });
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.1f * tH, 0.04f * tH);
                ToCan(c, tH * 1.3f);
                ToNo(c, foeFeet.y, tH, 1.4f, ToDa, ToDa2, new Vector2(dir, 0));
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
            // tụ: mảnh tinh thể + bụi bay xoắn ốc về trước đôi tay thành vệt, nhanh dần, dày dần tới lúc phóng; hai vòng co (ngọc lam, hổ phách)
            Every((ThtTu0 - 0.12f) * k, (ThtPhong0 - 0.03f) * k, x => 20 + 50 * x, x =>
            {
                float a = U(0, 6.28f), r = U(0.45f, 0.72f) * casterH;
                var p0 = tu + new Vector2(Mathf.Cos(a) * r, Mathf.Sin(a) * r * 0.7f);
                ToHut(p0, _ => tu, U(0.18f, 0.25f) * k, U(2f, 3.2f) * sH, U(0, 1) < 0.4f ? ThtNgoc : U(0, 1) < 0.6f ? ToPhach : ToBuiC, 2.2f);
            });
            At((ThtTu0 - 0.1f) * k, () => ToVongCo(_ => tu, 0.6f * casterH, 0.28f * k, ThtNgoc2));
            At((ThtTu0 + 0.08f) * k, () => ToVongCo(_ => tu, 0.5f * casterH, 0.22f * k, ToPhach2));
            At(ThtPhong0 * k, () => ToChop(tu, 0.3f * casterH, Front, 0.1f));
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
                // khung vẽ sẵn (2026-11-19): đuôi sao chổi là CẦU LỬA vẽ sẵn bám đúng đường bay của bản sao (lớp sau: lõi nấp sau thiên thạch của rig,
                // vành lửa + đuôi ló ra), thay dòng 95 cụm lửa / giây
                if (HasFb("cau_lua")) At(t0, () => FbCauBam(Duong, v, 0.4f * casterH, tb, Back, 34));
                else
                    // đuôi sao chổi: nhiều cụm lửa NHỎ dày bám đường bay hoà thành một dải liền (một viền mực), không lưỡi lửa to rời
                    Every(t0, t0 + tb, 95, x =>
                    {
                        var p = Duong(T);
                        var q = Flame(p + U2(-3, 3) * sH, -dv * U(40, 110) * sH + U2(-20, 20) * sH, U(0.12f, 0.18f), 5 * sH, U(8, 11) * sH, "tron", Th.pal,
                            U(0, 1) < 0.65f ? Back : Front, 3, -100, 1.5f, 0.1f, 0.04f);
                        if (U(0, 1) < 0.25f) Tongue(q, 1, 0.1f);
                    });
                Every(t0, t0 + tb, 26, x => ThtTia(Duong(T), -dv + U2(-0.5f, 0.5f), U(120, 260) * sH, U(0, 1) < 0.5f ? ToPhach2 : ThtNgoc2, U(0.12f, 0.2f), 6 * sH, 200));
                // VỆT KHÓI ĐUÔI (người dùng xem trong game 2026-11-19: "fireball, tên lửa,... nên thêm trail smoke vào"): FbKhoiDuoi nhả cụm khói
                // 0,24 tH ở giữa đuôi cầu lửa (lớp sau, dưới cầu lửa), thôi nhả lúc viên trúng; thay dòng khói than thưa cũ (không chồng hai vệt)
                if (HasFb("khoi")) At(t0, () => FbKhoiDuoi(() => Duong(T) - dv * (0.3f * casterH), () => T < tStart + tb, 0.24f * tH, 30, null, Back, 27));
                else Every(t0, t0 + tb, 24, x => ToKhoi(Duong(T) - dv * 10 * sH + U2(-3, 3) * sH, -dv * 15 + new Vector2(0, -10), U(0.5f, 0.7f), 4 * sH, U(8, 10) * sH, Back,
                    false));
                At(t0 + tb, () =>
                {
                    bool cuoi = jj == s0.Length - 1;
                    ThtTrung(foeBody + new Vector2(-dir * 0.08f * tH, 0) + U2(-6, 6) * sc, foeFeet, tH, (cuoi ? 1.5f : 0.9f) * d.muc, v);
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
                bool fb = HasFb("khoi");
                for (int i = 0; i < 5; i++)                                       // bụi bung che chỗ đổi hình: năm cụm to quanh quả cầu, tách dần
                {
                    if (fb && (i == 1 || i == 3)) continue;                      // khung vẽ sẵn (2026-11-19): ba cụm khói vẽ sẵn to hơn thay năm cụm hạt
                    float a = 6.28f * (i + U(-0.25f, 0.25f)) / 5;
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f);
                    ToBuiFb(c + d * rb * 0.7f, d * U(60, 120) * sH, U(0.5f, 0.65f), 10 * sH, 20 * sH, (i & 1) == 0 ? Front : Back, null, FbBuiC, 1, 1.25f, false, true);
                }
                for (int i = 0; i < 5; i++)
                    ThtManh(c, new Vector2(U(-1, 1), -U(0.4f, 1)) * U(160, 260) * sH, U(7, 10) * sH, (i & 1) == 0);
            });
            // quay tại chỗ: bụi cụm liền, sỏi nhỏ, tia ma sát hất ra sau từ chân quả cầu (mật độ tăng dần tới lúc vọt)
            Every(ThtCuon * k, ThtLen * k, x => 10 + 16 * x, x =>
            {
                var c = Cau(T);
                var chan = new Vector2(c.x - dir * 0.2f * rb, casterFeet.y - 3);
                // khung vẽ sẵn (2026-11-19): bụi hất ra sau là cụm khói vẽ sẵn nhuộm bụi, chân ở mặt đất, 40 % số cụm, to × 1,3
                ToBuiFb(chan + U2(-6, 6) * sH, new Vector2(-dir * U(80, 180), -U(20, 70)) * sH, U(0.45f, 0.6f), 7 * sH, U(12, 15) * sH, U(0, 1) < 0.5f ? Back : Front,
                    null, FbBuiC, 0.4f, 1.3f, true);
                if (U(0, 1) < 0.3f)
                    ToSoi(chan, new Vector2(-dir * U(120, 260), -U(150, 280)) * sH, U(1.8f, 3f) * sH, U(0, 1) < 0.5f ? ToDa : ToDa2, casterFeet.y + U(-2, 4));
                if (U(0, 1) < 0.8f)
                    ThtTia(chan, new Vector2(-dir, -U(0.3f, 1)), U(200, 360) * sH, U(0, 1) < 0.6f ? ToPhach2 : ToKem, U(0.14f, 0.24f), 6 * sH, 600);
            });
            // vọt lên
            At(ThtLen * k, () =>
            {
                var chan = new Vector2(Cau(T).x, casterFeet.y);
                ToVong(chan, 110 * sH, 0.55f);
                ToHo(chan, 32 * sH, 0.8f);
                for (int i = 0; i < 3; i++)
                    ToSoiCum(chan + new Vector2(U(-0.2f, 0.2f) * casterH, -4), new Vector2(U(-160, 160), -U(320, 500)) * sH, U(3f, 4.4f) * sH,
                        i == 1 ? ToDa2 : ToDa, ToDa3, casterFeet.y + U(-2, 6), (i & 1) == 0 ? Front : Back);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(chan + new Vector2(d * U(16, 40) * sH, -U(4, 16) * sH), new Vector2(d * U(50, 110), -U(30, 70)) * sH, 13 * sH, 3, d < 0 ? Front : Back);
                Shake?.Invoke(0.18f);
            });
            // LAO XUỐNG (người dùng: "xé gió tạo lửa"): bùng lửa lúc bắt đầu rơi, rồi ÁO LỬA dày dần theo tốc độ: nhiều cụm lửa NHỎ dồn ở mặt trước
            // quả cầu hoà thành một khối liền (một viền mực), đuôi sao chổi kéo theo vận tốc; lưỡi lửa chỉ ở mép (người dùng 2026-11-18: "các đốm lửa
            // nhìn hơi đơn lẻ và to quá")
            // khung vẽ sẵn (2026-11-19): có khung "cau_lua" thì áo lửa + đuôi sao chổi là MỘT cầu lửa vẽ sẵn bám tâm quả cầu (lớp sau: lõi vàng bán
            // kính ~ quả cầu nấp sau nó, vành lửa ló quanh, đuôi kéo ngược hướng lao), thay mười lưỡi lửa bùng và dòng 70–190 cụm lửa / giây
            bool cauFb = HasFb("cau_lua");
            At((ThtDinh + 0.02f) * k, () =>
            {
                var c = Cau(T);
                ToChop(c, 0.3f * casterH, Front, 0.1f);
                ToVongVa(c, 0.9f * rb, 0.22f, 0.9f);
                if (cauFb)
                {
                    FbCauBam(Cau, Cau(tGoi + ThtNo * k) - Cau(tGoi + ThtDinh * k), 4f * rb, (ThtNo - ThtDinh - 0.02f) * k, Back, 34);
                    return;
                }
                for (int i = 0; i < 10; i++)
                {
                    float a = 6.28f * (i + U(-0.3f, 0.3f)) / 10;
                    var q = Flame(c + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * rb * 0.8f, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(110, 200) * sH,
                        U(0.2f, 0.28f), 7 * sH, U(11, 15) * sH, "tron", Th.pal, (i & 1) == 0 ? Back : Front, 4, -160, 1.6f, 0.15f, 0.05f);
                    if ((i & 1) == 0) Tongue(q, 1, 0.15f);
                }
            });
            Vector2 Huong(float tt) => Unit(Cau(tt + 0.02f) - Cau(tt - 0.02f));
            if (!cauFb)
                Every(ThtDinh * k, ThtNo * k, x => 70 + 120 * x, x =>
                {
                    var c = Cau(T);
                    var dv = Huong(T);
                    var bn = new Vector2(-dv.y, dv.x);
                    bool truoc = U(0, 1) < 0.3f;
                    var p = c + dv * rb * U(0.2f, 0.95f) + bn * rb * U(-0.85f, 0.85f);
                    var q = Flame(p, -dv * U(80, 200) * sH + bn * U(-60, 60) * sH, U(0.16f, 0.24f), (truoc ? 6 : 8) * sH, (truoc ? U(9, 12) : U(12, 16)) * sH,
                        "tron", Th.pal, truoc ? Front : Back, 3, -80, 1.8f, 0.12f, 0.05f);
                    if (U(0, 1) < 0.22f) Tongue(q, 1, 0.08f);
                    q.smokeGroup = Back;
                });
            // VỆT KHÓI ĐUÔI (người dùng 2026-11-19: "fireball ... nên thêm trail smoke vào"): FbKhoiDuoi nhả cụm khói 0,32 tH trên đuôi sao chổi
            // (1,8 bán kính sau tâm quả cầu, lớp sau dưới cầu lửa) suốt lúc lao, thôi nhả lúc nổ; thay dòng khói than thưa cũ (không chồng hai vệt)
            if (HasFb("khoi"))
                At(ThtDinh * k, () => FbKhoiDuoi(() => Cau(T) - Huong(T) * (1.8f * rb), () => T < tGoi + ThtNo * k, 0.32f * tH, 26, null, Back, 27));
            else
                Every(ThtDinh * k, ThtNo * k, 26, x =>
                {
                    var dv = Huong(T);
                    ToKhoi(Cau(T) - dv * rb * 1.0f + U2(-6, 6) * sH, -dv * 25 + new Vector2(0, -10), U(0.6f, 0.85f), 7 * sH, U(13, 16) * sH, Back, false);
                });
            Every(ThtDinh * k, ThtNo * k, 34, x =>
            {
                var dv = Huong(T);
                var bn = new Vector2(-dv.y, dv.x);
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                ThtTia(Cau(T) + bn * sd * rb * U(0.9f, 1.2f), -dv, U(380, 560) * sH, ToKem, U(0.1f, 0.16f), 10 * sH, 0, sd > 0 ? Front : Back);
            });
            Every(ThtDinh * k, ThtNo * k, 10, x => Ember(Cau(T) + U2(-rb, rb) * 0.6f, -Huong(T) * U(60, 140) * sH, U(0.45f, 0.7f), 6 * sH));
            // NỔ RẤT LỚN (KR5): chớp kem 2 khung → khối lửa đã to gần đủ ngay SAU lưng đối thủ (không che nó) + đá, tinh thể văng → sóng đất cung dẹt,
            // hố, vết nứt giữ ~1 s → khói than CỤM nhiều múi bốc lên, tách dần, tan. Một tiếng nổ phụ lệch sau 0,13 s
            At(L, () =>
            {
                var c = Vector2.Lerp(Cau(T), foeBody, 0.55f);
                var dat = new Vector2(c.x, foeFeet.y);
                Shake?.Invoke(0.9f * m);
                FlashScreen?.Invoke(new Color(1, 0.96f, 0.84f, 0.5f * m));
                ToChop(c, 0.62f * tH * m, Front, 0.08f);
                // khung vẽ sẵn (2026-11-19; "nổ chưa đẹp"): NỔ NẤM vẽ sẵn (chân ở mặt đất: phồng, chớp sao, nấm có thân, nguội, khói, mảnh khuyết) +
                // dung nham hổ phách phun ở lớp đất lệch về phía mình (nứt, phun dẻo, đổ thành vũng, nguội); thay nổ lưỡi lửa, sáu lưỡi nhọn, lửa tạt
                // sát đất và cột lửa. Nổ ở lớp TRƯỚC (người dùng xem trong game: nổ sau lưng đối thủ "nằm dưới địch nên không thấy rõ"): neo dời
                // 0,2 tH về phía mình, cao 1,6 tH, chạy nhanh hơn một chút (~0,8 s) cho khỏi trùm đối thủ lâu
                bool noFb = HasFb("no");
                if (noFb)
                {
                    Fb("no", dat + new Vector2(-dir * 0.2f * tH, 2), 1.6f * tH * m, Front, 30, 1.25f, 0, dir < 0);
                    Fb("nham", dat + new Vector2(-dir * 0.4f * tH, 3), 0.9f * tH * m, Front, 29, 1.2f, 0, dir < 0); // dung nham: lớp TRƯỚC (người dùng 2026-11-19: "gai đất, nổ đang bị lỗi layer hiện đằng sau tướng địch")
                }
                else
                {
                    Explode(c + new Vector2(0, -0.06f * tH), 1.05f * m, tH, Back);
                    for (int i = 0; i < 6; i++)
                    {
                        float a = U(-160, -20) * Mathf.Deg2Rad;
                        Flame(dat, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * 500 * sc, 0.28f, 6 * sc, 14 * sc, "nhon", Th.pal, Back, 5, -150, 1, 0);
                    }
                    foreach (int sd in new[] { -1, 1 })
                        for (int i = 0; i < 2; i++)                               // lửa tạt sát đất phía trước: nhỏ, thấp
                            Tongue(Flame(dat + new Vector2(sd * U(14, 34), 6) * sc, new Vector2(sd * U(250, 400), -20) * sc, 0.3f, 6 * sc, U(10, 13) * sc, "tron",
                                Th.pal, Front, 4, -200, 1.3f, 0), 0.4f, 0.6f);
                    Every(0, 0.35f, x => 60 * (1 - 0.5f * x), x =>                   // cột lửa sau lưng đối thủ, vài lưỡi nhỏ ở mép trước
                    {
                        float th = U(0, 6.28f);
                        bool fr = Mathf.Sin(th) > 0.55f;
                        var q = Flame(foeFeet + new Vector2(0.4f * tH * Mathf.Cos(th), 12 * sc * Mathf.Sin(th) - 4), new Vector2(Mathf.Cos(th) * 40, -U(420, 640)) * sc,
                            U(0.3f, 0.45f), 7 * sc, U(14, 19) * sc * (fr ? 0.6f : 1), "tron", Th.pal, fr ? Front : Back, 2.2f, -200, 1.7f, 0.08f, 0.06f);
                        Tongue(q, 1, 0.5f);
                        q.smokeGroup = Back;
                    });
                }
                ToVong(dat, 1.5f * m * tH, 0.5f);
                At(0.08f, () => ToVong(dat, 1.0f * m * tH, 0.55f));
                ToHo(dat, 0.42f * tH * m, 1.0f);
                for (int i = 0; i < 4; i++)
                {
                    float a = (-90 + (i - 1.5f) * 38 + U(-10, 10)) * Mathf.Deg2Rad;
                    ToSoiCum(c + U2(-10, 10) * sc, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(320, 560) * sc, U(4f, 5.5f) * sc, i % 2 == 0 ? ToDa2 : ToDa, ToDa3,
                        foeFeet.y + U(-8, 16) * sc, (i & 1) == 0 ? Front : Back);
                }
                for (int i = 0; i < 6; i++)
                {
                    float a = (-90 + U(-80, 80)) * Mathf.Deg2Rad;
                    ThtManh(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(300, 520) * sc, U(10, 15) * sc, (i & 1) == 0, (i & 2) == 0 ? Front : Back);
                }
                At(0.1f, () =>
                {
                    for (int i = 0; i < 8; i++) Spark(c + U2(-12, 12), new Vector2(U(-1, 1), -U(0.3f, 1)), U(300, 520) * sc);
                });
                for (int i = 0; i < 5; i++)
                {
                    float a = (i - 2) * 0.5f + U(-0.12f, 0.12f);
                    ToNut(dat, dat + new Vector2(Mathf.Sin(a) * U(0.8f, 1.1f) * tH, U(2, 10) * sc), 0.16f, sc);
                }
                At(0.14f, () =>                                                   // khói than: cụm thấp lan ngang + cụm cao bốc lên, tách dần
                {
                    for (int d = -1; d <= 1; d += 2)
                        ToKhoiCum(dat + new Vector2(d * U(20, 40), -8) * sc, new Vector2(d * U(110, 200), -U(15, 40)) * sc, 20 * sc * m, 3, U(1.2f, 1.5f));
                    if (noFb) return;                                             // khung vẽ sẵn: khung nổ đã có nấm khói, chỉ giữ hai cụm thấp lan ngang
                    ToKhoiCum(c + new Vector2(0, -0.35f * tH), new Vector2(U(-20, 20), -U(110, 160)) * sc, 26 * sc * m, 4, 1.5f);
                    ToKhoiCum(c + new Vector2(-dir * 0.3f * tH, -0.15f * tH), new Vector2(-dir * 60, -U(60, 100)) * sc, 18 * sc * m, 3, 1.3f);
                });
                for (int i = 0; i < 6; i++) Ash(c + U2(-40, 40) * sc, new Vector2(U(-80, 80), -U(80, 160)));
                At(0.13f, () =>
                {
                    Shake?.Invoke(0.4f * m);
                    // khung vẽ sẵn: tiếng nổ phụ là lửa trúng vẽ sẵn ở lớp TRƯỚC (người dùng: nổ sau lưng "không thấy rõ"), lệch về phía mình và thấp
                    // hơn chỗ nổ phụ cũ (cũ: phía xa, cao ngang đầu) để khỏi đè mặt đối thủ; thay nổ lưỡi lửa
                    if (HasFb("trung_lua"))
                        Fb("trung_lua", c + new Vector2(-dir * U(0.15f, 0.25f) * tH, -U(0.02f, 0.12f) * tH), 0.75f * tH * m, Front, 31, 1.3f, U(-20, 20), dir < 0);
                    else Explode(c + new Vector2(dir * U(0.1f, 0.25f) * tH, -U(0.12f, 0.24f) * tH), 0.5f * m, tH, Back);
                });
            });
            // nảy về: than, khói mỏng theo quả cầu
            Every((ThtNo + 0.04f) * k, ThtNay * k, 12, x =>
            {
                var c = Cau(T);
                if (U(0, 1) < 0.5f) Ember(c + U2(-rb, rb) * 0.5f, new Vector2(U(-40, 40), U(-60, -20)) * sH, U(0.45f, 0.7f), 6 * sH);
                else ToKhoiFb(c + U2(-rb, rb) * 0.4f, new Vector2(U(-20, 20), -40), U(0.7f, 0.9f), 5 * sH, 12 * sH, Back, false, 0.5f, 1.2f);   // khung vẽ sẵn
            });
            // đáp về chỗ cũ
            At(ThtVe * k, () =>
            {
                ToVong(casterFeet, 100 * sH, 0.5f);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(casterFeet + new Vector2(d * 0.3f * casterH, -4 * sH), new Vector2(d * 100, -30) * sH, 12 * sH, 3);
                Shake?.Invoke(0.15f);
            });
            return L;
        }
    }
}
