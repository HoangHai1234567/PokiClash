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

        // một nhát kiếm lửa trúng đối thủ: vệt lửa theo hướng d, chớp, tia lửa văng, than hồng, bụi dưới chân
        void DatChem(Vector2 tam, Vector2 d, float tH, float manh, Vector2 foeFeet)
        {
            var pc = Pal[Th.pal];
            var n = new Vector2(-d.y, d.x);
            Shake?.Invoke(0.3f * manh);
            VetLua(tam, d, 1.15f * manh * tH, 0.1f * manh * tH, 0.2f, 0, Ink, pc[1], pc[3], pc[1]);
            BurstFlash(tam + d * (0.1f * tH), 0.3f * manh * tH);
            int tia = Mathf.RoundToInt(7 * manh);
            for (int i = 0; i < tia; i++)
                Spark(tam + n * U(-0.14f, 0.14f) * tH, d + n * U(-0.7f, 0.7f), U(260, 480), U(0.18f, 0.3f), U(6, 9), 300);
            for (int i = 0; i < 3; i++) Ember(tam + U2(-0.15f, 0.15f) * tH, new Vector2(U(-80, 80), -U(60, 200)), U(0.4f, 0.7f), 8);
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
            At(Mathf.Max(0.05f, L - DatTu), () => Eruption(foeFeet, tH));                                                              // nứt đất 0,42 s rồi trào
            At(L, () => DatChem(tam, Unit(new Vector2(dir * 0.35f, 0.94f)), tH, 1.25f, foeFeet));                                      // bổ kết
            return L;
        }
    }
}
