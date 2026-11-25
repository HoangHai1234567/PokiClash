// CHIÊU ĐỔI MÀU từ bộ chiêu nước cho hệ khác (2026-11-25; người dùng: "giờ làm cho cả các hệ khác nữa nhé, phù hợp thì mới làm", chọn bốn
// việc: cầu ma xanh lục cho Mộc, chém lửa cho Viêm Đao, tia lửa năng lượng, cầu ma màu lửa).
//  - cầu ma đổi màu: HatNuocChieu.CauMaTheo (prefab gốc MagicWater_OrbLoop, material theo hệ), gọi từ HatDa (Gạc Đá), HatLoc (Lộc Phong),
//    HatRua (Hỏa Quy);
//  - tia lửa năng lượng: HatNhan.TiaMatFb dùng ELaser bảng lửa (Hỏa Nhãn; Tiểu Quỷ Lava đổi chiêu mana sang "tia_mat" bắn từ mũi giáo);
//  - chém lửa: NDaoLien dưới đây.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // VỠ CẦU MA MÀU LỬA (2026-11-25, người dùng xem chiêu cuối Hỏa Quy: "nổ cũng không đúng lắm": cầu xoáy biến mất rồi chỉ có nổ lửa
        // thường, không ăn với quả cầu): cùng bố cục vụ vỡ cầu ma thủy (MaNo) đổi bảng lửa, bỏ phần nước (toé, giọt, vũng): quầng chớp hai lớp,
        // chớp tròn + chớp hướng, vòng sóng nở, ba lưỡi liềm xoáy văng (như dải bay vòng của cầu bị bung), vòng chạm đất. Nổ lửa cũ gọi ngay sau.
        void HoaCauMaNo(Vector2 c, Vector2 foeFeet, float tH, float sc)
        {
            if (!NuocShaderOn) return;
            const int pal = HatNuocFx.PalLua;
            float sd = NSeed();
            // quầng chớp: cả hai lớp tông cam đỏ (tông sáng kem-hổ phách của MaNo thành đĩa đào nhạt trùm đối thủ, lần chụp đầu), lớp trước nhỏ, ngắn
            NP(Front, 0.3f, (q, a) =>
            {
                float k = a / 0.3f;
                NQuang(Back, 5.0f, c, Mathf.Lerp(0.9f, 1.4f, EaseOut(k)) * tH * sc, 0.5f * (1 - k), 1.5f, 1, 0.2f, sd + 20, pal);
                if (a < 0.2f)
                    NQuang(Front, 6.68f, c, Mathf.Lerp(0.4f, 0.8f, EaseOut(a / 0.2f)) * tH * sc, 0.7f * (1 - a / 0.2f), 1.4f, 1, 0.25f, sd + 21, pal);
            });
            NFbPhat(Front, 6.6f, c, Vector2.zero, 0.15f, NFb.ChopTron, 1.1f * tH * sc, 1.8f * tH * sc, U(0, 360), 0.3f, 0.22f, 0, false, 0, 0, 0, 0, null, 0.8f,
                pal);
            NFbPhat(Front, 6.55f, c, Vector2.zero, 0.16f, NFb.ChopHuong, 1.3f * tH * sc, 1.9f * tH * sc, U(0, 360), 0.3f, 0.15f, 0, false, 0, 0, 0, 0, null,
                0.8f, pal);
            NP(Front, 0.4f, (q, a) =>
            {
                float k = a / 0.4f, rr = Mathf.Lerp(0.4f, 1.5f, EaseOut(k)) * tH * sc;
                NFbS(Front, 6.3f, c, 2 * rr, 1.8f * rr, 0, NFb.ChamDat, 2 + 10 * k, 0.3f, 1, sd + 2, 0.3f, 2, false, pal);
            });
            for (int j = 0; j < 3; j++)
                NFbPhat(Front, 6.4f, c, Vector2.zero, U(0.3f, 0.4f), NFb.ChemVong, 0.8f * tH * sc, 1.9f * tH * sc, U(0, 360), 0.3f, 0.1f, 0, U(0, 1) < 0.5f, 0, 0,
                    (U(0, 1) < 0.5f ? -1 : 1) * U(220, 360), 0, null, 0.8f, pal);
            NFbPhat(Floor, 2.1f, foeFeet + new Vector2(0, 2), Vector2.zero, 0.7f, NFb.ChamDat, 0.6f * tH * sc, 2.3f * tH * sc, 0, 0.3f, 0, 1, false, 0, 0, 0,
                0.32f, null, 0.8f, pal);
        }

        // mốc clip skill của Viêm Đao (ArtGen/Spine/inbox/quy_dao_ghichu.md: skill 2,67 s = skill_04_1 + lao tới 0,10–0,28): bảy nhát chém, bật
        // nhảy vọt khỏi khung, rơi bổ cắm đất ở khung trúng (hitTimes skill 1,87, cả hai dạng)
        static readonly float[] DaoChemT = { 0.30f, 0.42f, 0.60f, 0.74f, 0.86f, 0.98f, 1.24f };
        // góc lưỡi chém theo kiểu nhát (độ; 0 = ngang về phía đối thủ, dương = chúc xuống): quét ngang, xoay chém, hất lên, bổ, quét, xoay, đâm
        static readonly float[] DaoChemGoc = { 4, -28, 34, -62, 12, -36, 70 };
        const float DaoBoT = 1.87f;

        // CHÉM LỬA (chiêu cuối Viêm Đao; trước là mã chung "no_lon" chỉ nổ lớn lúc bổ): Chém nước của Uyên Xà (NXaChem) đổi bảng lửa, mỗi nhát
        // của chuỗi liên hoàn một cung lưỡi liềm lửa (ChemVong) + vệt sáng + chớp hướng + tia lửa toé ngay trên thân đối thủ, đổi chiều xen kẽ
        // theo kiểu nhát; nhát đâm cuối chuỗi có nổ nhỏ. Rơi bổ cắm đất (lead): cung chém dọc rất to + vệt sáng giáng xuống + nổ lớn như mã chung.
        // Không có shader nước thì chỉ nổ lớn như cũ.
        public float NDaoLien(Vector2 casterFeet, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            float side = foeFeet.x < casterFeet.x ? 1 : -1; // phía con ra chiêu so với đối thủ (BigBurst)
            float dir = -side;
            float L = Mathf.Max(0.5f, lead), k = L / DaoBoT; // co giãn mốc theo khung trúng thật của clip
            if (!NuocShaderOn)
            {
                AtW(L, () => BigBurst(foeFeet, foeBody, tH, side));
                return L;
            }
            const int pal = HatNuocFx.PalLua;
            for (int i = 0; i < DaoChemT.Length; i++)
            {
                int ii = i;
                bool cuoi = i == DaoChemT.Length - 1;
                AtW(DaoChemT[i] * k, () =>
                {
                    float an = (dir > 0 ? 0 : 180) + DaoChemGoc[ii] * dir + U(-5, 5);
                    var d = NHuong(an);
                    var c = foeBody + new Vector2(U(-0.08f, 0.08f), U(-0.1f, 0.06f)) * tH;
                    float w = (cuoi ? 1.55f : 1.3f) * tH;
                    NFbDoan(Front, 6.3f, _ => c, 0.22f, NFb.ChemVong, 0, 9, w, w * 1.15f, an + 90 * (ii % 2 == 0 ? 1 : -1), 0.3f, 0.1f, 0, ii % 2 == 1,
                        pal: pal);
                    NFbPhat(Front, 6.35f, c - d * (0.18f * tH), d * 520, 0.15f, NFb.VetSang, 1.3f * tH, 1.6f * tH, an, 0.3f, 0.3f, 2, dir < 0, pal: pal);
                    NFbPhat(Front, 6.1f, c, Vector2.zero, 0.12f, NFb.ChopHuong, 0.7f * tH, 1.0f * tH, an, 0.3f, 0.14f, pal: pal);
                    for (int j = 0; j < 5; j++) Spark(c + U2(-6, 6), d + U2(-0.6f, 0.6f) + new Vector2(0, -0.3f), U(220, 420), 0, 6);
                    if (cuoi) HoaNo(c, 0.5f, tH, null, Front, dir);
                    Shake?.Invoke(cuoi ? 0.4f : 0.2f);
                    HoaTrung?.Invoke(foeBody, cuoi ? 0.5f : 0.3f);
                });
            }
            AtW(L, () =>
            {
                var c = foeBody + new Vector2(0, -0.05f * tH);
                NFbDoan(Front, 6.4f, _ => c, 0.26f, NFb.ChemVong, 0, 9, 1.9f * tH, 2.2f * tH, 180 + U(-6, 6), 0.3f, 0.1f, pal: pal);
                NFbPhat(Front, 6.45f, c + new Vector2(0, -0.45f * tH), new Vector2(0, 900), 0.16f, NFb.VetSang, 1.8f * tH, 2.1f * tH, 90, 0.3f, 0.3f, 2,
                    pal: pal);
                BigBurst(foeFeet, foeBody, tH, side);
            });
            return L;
        }
    }
}
