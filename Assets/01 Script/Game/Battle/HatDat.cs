// Bộ VIÊM DŨNG (2026-11-14, chiến binh đất nung lõi dung nham, suất huyen_viem đảo Hỏa; rig ArtGen/Spine/dat_nung_rig.py).
// Người dùng: "chiêu mana làm giống skill_04_1, đâm kiếm vào đối thủ rồi thực hiện nhiều động tác chém". Rig diễn thân và kiếm (clip cast
// khai lunge: sân nắn quãng lướt tới đối thủ vì mã này thuộc CastLao); lớp này lo vệt đâm, vệt chém, tia lửa và dung nham trào ở nhát bổ kết.
// Chiêu cuối (năm kiếm bay tới) là mảnh của rig (xương far), hiệu ứng dùng mã chung "no_lon". Bản tối thiểu để vào game, chưa phải VFX riêng đủ.
// Đi đường "n_" (StageView.PreFx → PlayNuoc: phát từ đầu clip, biết `lead` = giờ tới khung trúng của clip). Màu theo Themes["huyen_viem"].
// Mốc clip cast (giây): lao 0,20, đâm 0,42, hất lên 0,74, chém ngược 1,00, tụ 1,30, bổ kết 1,72 (= lead). Đổi clip thì sửa các hằng Dat*.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // quãng (giây) từ từng mốc tới nhát bổ kết
        const float DatDam = 1.30f, DatLen = 0.98f, DatNguoc = 0.72f, DatTu = 0.42f;

        // một nhát kiếm lửa trúng đối thủ: vệt lửa theo hướng d, chớp lửa (2026-11-18: trước dùng BurstFlash là chớp NƯỚC), tia lửa văng, cụm tàn
        // lửa, lưỡi lửa chữ S toé theo hướng chém, bụi dưới chân
        void DatChem(Vector2 tam, Vector2 d, float tH, float manh, Vector2 foeFeet)
        {
            var pc = Pal[Th.pal];
            var n = new Vector2(-d.y, d.x);
            Shake?.Invoke(0.3f * manh);
            NuocPulse?.Invoke(0.4f * manh);
            VetLua(tam, d, 1.15f * manh * tH, 0.1f * manh * tH, 0.2f, 0, Ink, pc[1], pc[3], pc[1]);
            // khung vẽ sẵn (2026-11-19): mỗi nhát một "trung_lua" xoay theo hướng chém (0,6–0,9 thân), thay chớp sao gai + hai lưỡi lửa toé
            bool fb = HoaFbTrung(tam + d * (0.06f * tH), Mathf.Clamp(0.68f * manh, 0.55f, 0.9f) * tH, d) != null;
            if (!fb) HoaChop(tam + d * (0.1f * tH), 0.3f * manh * tH, 0.09f);
            int tia = Mathf.RoundToInt(5 * manh);
            for (int i = 0; i < tia; i++)
                Spark(tam + n * U(-0.14f, 0.14f) * tH, d + n * U(-0.7f, 0.7f), U(260, 480), U(0.18f, 0.3f), U(5, 7), 300);
            for (int i = 0; i < (fb ? 0 : 2); i++)
                HoaLuoi(Flame(tam + d * U(0.05f, 0.2f) * tH, (d + n * U(-0.4f, 0.4f)) * U(160, 280) + new Vector2(0, -60), U(0.24f, 0.32f), 6, U(12, 16) * manh,
                    "tron", Th.pal, i == 0 ? Front : Back, 3.5f, -180, 1.5f, 0, 0), 1, 0.3f, 0);
            HoaTan(tam, new Vector2(U(-50, 50), -U(90, 170)), U(0.45f, 0.65f), 3);
            for (int i = 0; i < 3; i++)
            {
                float sd = (i & 1) == 0 ? 1 : -1;
                Bui(foeFeet + new Vector2(sd * U(6, 0.25f * tH), U(-5, 2)), new Vector2(sd * U(100, 260), -U(10, 50)), 0, 4, 11, Back);
            }
        }

        // chiêu mana: lao tới ĐÂM, hất lên, chém ngược về, tụ lực rồi BỔ kết (dung nham trào dưới chân đối thủ đúng lúc bổ)
        public float NDatDam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var tam = foeBody + new Vector2(-dir * 0.05f * tH, 0);
            At(Mathf.Max(0.02f, L - DatDam), () => DatChem(tam, new Vector2(dir, 0), tH, 0.8f, foeFeet));                              // đâm thẳng
            At(Mathf.Max(0.03f, L - DatLen), () => DatChem(tam, Unit(new Vector2(dir * 0.55f, -0.84f)), tH, 0.85f, foeFeet));          // hất lên
            At(Mathf.Max(0.04f, L - DatNguoc), () => DatChem(tam, Unit(new Vector2(-dir * 0.8f, 0.6f)), tH, 0.85f, foeFeet));          // chém ngược về
            At(Mathf.Max(0.05f, L - DatTu), () => Eruption(foeFeet, tH, 1.45f, dir));                                                  // nứt đất 0,42 s rồi trào (cột "nham" dời về phía người chém)
            At(L, () => DatChem(tam, Unit(new Vector2(dir * 0.35f, 0.94f)), tH, 1.25f, foeFeet));                                      // bổ kết
            return L;
        }
    }
}
