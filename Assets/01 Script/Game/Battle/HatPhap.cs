// Bộ VIÊM SƯ (2026-11-14, pháp sư lửa cầm trượng cầu lửa, suất hong_lien đảo Hỏa; rig ArtGen/Spine/phap_lua_rig.py).
// Người dùng: chiêu mana "giơ trượng lên triệu hồi các mũi kim lửa rồi bắn vào người đối thủ"; chiêu cuối "cầu lửa bay lên phình to, còn bay
// đi đâu do code làm". Rig diễn thân và quả cầu lửa TRÊN TRƯỢNG (chiêu cuối: cầu rời trượng, bay lên, phình 2,4 lần rồi BIẾN MẤT đúng mốc
// `ban_cau`); kim lửa, lửa bị hút về cầu, quả cầu bay tới đối thủ và vụ nổ là việc của lớp hạt này.
// Đi đường "n_" (StageView.PreFx → PlayNuoc: phát từ đầu clip, biết `lead` = giờ tới khung trúng của clip) vì kim phải hiện lúc giơ trượng và
// cầu phải rời chỗ TRƯỚC khung trúng. Màu theo Themes["hong_lien"] (bảng "lua").
// - n_kim_phap (chiêu mana): kim lửa hiện dần thành vòng cung quanh đầu trượng đang giơ (mốc `goi_kim`), vụt trượng (`ban_kim`) thì cả loạt
//   phóng đi, mũi đầu chạm đối thủ đúng khung trúng.
// - n_cau_phap (chiêu cuối): lưỡi lửa và than hồng từ quanh sân bị hút vào quả cầu của rig đang phình; cầu đầy thì nháy vòng; mốc `ban_cau`
//   quả cầu hạt (cùng chỗ, cùng cỡ với cầu của rig vừa biến mất) lao tới đối thủ, chạm đúng khung trúng, nổ lớn.
// Vị trí đầu trượng / tâm cầu theo giây là số đo trên rig đã xuất (phần của chiều cao KHAI cho game 662, x về phía trước, y lên): đổi clip cast / skill
// hay hình thì đo lại bằng đoạn mã trong ArtGen/Spine/inbox/phap_lua_ghichu.md mục 8.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // clip cast: giơ trượng `goi_kim` 0,16 s, vụt trượng `ban_kim` 1,05 s, `trung` 1,19 s
        const float PhapGoi = 0.16f, PhapBan = 1.05f, PhapTrung = 1.19f;
        static readonly Vector2 PhapTruong = new Vector2(-0.34f, 1.44f); // đầu trượng lúc giơ (0,16–0,8 s của cast)
        // clip skill: cầu rời trượng 0,66 s, lên tới đỉnh và bắt đầu hút `hut` 1,05 s, đầy 2,05 s, `ban_cau` 2,25 s, `trung` 2,45 s
        const float PhapTach = 0.66f, PhapHut = 1.05f, PhapDay = 2.05f, PhapBanCau = 2.25f, PhapNo = 2.45f;
        const float PhapR0 = 0.124f; // bán kính cầu trên trượng (82 đơn vị rig) theo chiều cao game
        static readonly float[] PhapT = { 0.66f, 1.05f, 2.05f, 2.20f, 2.25f };
        static readonly Vector2[] PhapP =
        {
            new Vector2(0.085f, 0.940f), new Vector2(0.097f, 1.510f), new Vector2(0.096f, 1.501f), new Vector2(0.008f, 1.562f), new Vector2(-0.008f, 1.567f),
        };
        static readonly float[] PhapS = { 1f, 1f, 2.28f, 2.5f, 2.41f }; // tỉ lệ cầu của rig ở các mốc trên
        // DẠNG 1 (Viêm Đồng, pháp sư lửa con; rig phap_lua_non, chiều cao khai 642): trượng ngắn, cầu nhỏ; mốc 0,66 s lệch về sau vì trượng
        // thả rời đứng bên trái mũ. Đo bằng ArtGen/Spine/phap_lua_non.py do
        const float PhapR0Non = 0.095f;
        static readonly Vector2[] PhapPNon =
        {
            new Vector2(-0.629f, 0.755f), new Vector2(0.060f, 1.447f), new Vector2(0.061f, 1.438f), new Vector2(-0.030f, 1.501f), new Vector2(-0.046f, 1.507f),
        };

        static float PhapNoi(float[] v, float tc)
        {
            if (tc <= PhapT[0]) return v[0];
            for (int i = 1; i < PhapT.Length; i++)
                if (tc <= PhapT[i]) return Mathf.Lerp(v[i - 1], v[i], (tc - PhapT[i - 1]) / (PhapT[i] - PhapT[i - 1]));
            return v[v.Length - 1];
        }

        static Vector2 PhapTam(Vector2[] P, float tc)
        {
            if (tc <= PhapT[0]) return P[0];
            for (int i = 1; i < PhapT.Length; i++)
                if (tc <= PhapT[i]) return Vector2.Lerp(P[i - 1], P[i], (tc - PhapT[i - 1]) / (PhapT[i] - PhapT[i - 1]));
            return P[P.Length - 1];
        }

        // KIM LỬA QUANH ĐẦU TRƯỢNG (chiêu mana). lead: giây từ đầu clip cast tới khung trúng. Trả giây tới lúc mũi đầu chạm đối thủ.
        public float NKimPhap(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            const int N = 7;
            float L = Mathf.Max(0.5f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t00 = L - PhapTrung;                                   // giờ (tính từ lúc gọi) của giây 0 clip
            float tGoi = Mathf.Max(0.02f, t00 + PhapGoi), tBan = Mathf.Max(tGoi + 0.2f, t00 + PhapBan);
            float bay = Mathf.Max(0.08f, L - tBan);                      // giây kim bay: mũi đầu chạm đúng khung trúng
            var A = casterFeet + new Vector2(dir * PhapTruong.x, -PhapTruong.y) * casterH;
            float RA = 0.31f * casterH, LEN = 58;
            var pc = Pal[Th.pal];
            Color[] cols = { Ink, pc[0], pc[1], pc[2], pc[3] };
            float[] fr = { 1, 1, 0.82f, 0.6f, 0.34f };
            float[] ext = { 4.5f, 0, 0, 0, 0 };
            float cach = Mathf.Min(0.08f, (tBan - tGoi - 0.25f) / N);    // kim hiện lần lượt, mũi cuối hiện xong trước lúc vụt trượng
            float goc = T;
            for (int i = 0; i < N; i++)
            {
                int ii = i;
                At(tGoi + i * cach, () =>
                {
                    // vòng cung phía trên, ngả về phía đối thủ (đầu trượng ở sau lưng tướng nên kim xoè ra trước mặt)
                    float th = Mathf.PI * (1.08f - 0.9f * (ii + 0.5f) / N);
                    var home = A + new Vector2(dir * (0.25f * RA + RA * Mathf.Cos(th)), -0.75f * RA * Mathf.Sin(th));
                    var aim = foeBody + new Vector2(U(-0.18f, 0.18f) * tH, U(-0.15f, 0.2f) * tH);
                    float launch = goc + tBan + ii * 0.035f;
                    KimLua(home, aim, ii, launch, (aim - home).magnitude / bay, cols, fr, ext, LEN);
                });
            }
            // đầu trượng nhả tia lửa trong lúc gọi kim; lúc vụt trượng thì rung nhẹ
            Every(tGoi, tBan - 0.05f, 14, x => Spark(A + U2(-8, 8), new Vector2(dir * U(0.1f, 1f), -U(0.3f, 1f)), U(120, 220), 0, 6));
            At(tBan, () => Shake?.Invoke(0.12f));
            At(L + N * 0.035f + 0.25f, () =>
            {
                for (int i = 0; i < 2; i++) HoaKhoi(foeBody + new Vector2(U(-25, 25), -U(10, 30)), U(13, 17), Back, null, 0, true, 0.4f); // khói thành cụm
            });
            return L;
        }

        // CẦU LỬA CHIÊU CUỐI. lead: giây từ đầu clip skill tới khung trúng (`trung`). Trả giây tới lúc cầu chạm đối thủ.
        // non: dạng 1 (Viêm Đồng): cầu nhỏ hơn, vụ nổ nhẹ hơn
        public float NCauPhap(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, bool non = false)
        {
            var tamP = non ? PhapPNon : PhapP;
            float r0 = non ? PhapR0Non : PhapR0;
            float L = Mathf.Max(0.8f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t00 = L - PhapNo, goc = T;                              // t00: giờ (tính từ lúc gọi) của giây 0 clip
            Vector2 Rig(Vector2 p) => casterFeet + new Vector2(dir * p.x, -p.y) * casterH;
            Vector2 Tam(float tc) => Rig(PhapTam(tamP, tc));
            float Rt(float tc) => r0 * casterH * PhapNoi(PhapS, tc);
            float tHut = Mathf.Max(0.02f, t00 + PhapHut), tDay = Mathf.Max(tHut + 0.2f, t00 + PhapDay);
            float tBan = Mathf.Max(tDay + 0.05f, t00 + PhapBanCau);
            float bay = Mathf.Max(0.12f, L - tBan);
            float R = Rt(PhapBanCau);                                     // bán kính cầu lúc rời chỗ (cầu của rig biến mất ở mốc này)

            // hút (2026-11-18, người dùng chê pha hút quanh cầu): VỆT lửa thuôn sinh trên vòng rộng quanh cầu của rig, hiện dần, xoắn ốc nhanh dần vào
            // tâm, chạm vành thì nhập vào; thêm một dòng vệt từ phía dưới (lửa từ áo, từ đất bốc lên); hai vòng co; chớp lúc cầu rời chỗ (cầu là mảnh
            // của rig nên không vẽ khối cầu, chỉ vẽ phần hút)
            Vector2 TamT(float t) => Tam(t - goc - t00);
            float RtT(float t) => Rt(t - goc - t00);
            HoaTuCau(TamT, R, tHut, tBan, false, 1.1f, RtT);
            float chieu = -dir;
            Every(tHut, tDay, x => 10 + 14 * x, x =>
            {
                float a = U(0.15f, 2.99f), rr = U(0.75f, 1.2f) * casterH; // nửa dưới cầu (y sân đi xuống)
                HoaHut(TamT, RtT, TamT(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * rr, U(0.4f, 0.52f), U(0, 1) < 0.5f ? Pal[Th.pal][1] : Pal[Th.pal][2], chieu,
                    goc + tBan + 0.02f);
            });
            // lưỡi lửa chữ S liếm ra từ thân cầu của rig trong lúc phình
            Every(tHut + 0.1f, tBan, x => 8 + 14 * x, x =>
            {
                float tc = T - goc - t00, r = Rt(tc), a = U(0, 6.28f);
                var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                HoaLuoi(Flame(Tam(tc) + o * r * 0.8f, o * U(40, 110) + new Vector2(0, -U(40, 120)), U(0.22f, 0.32f), r * 0.26f, r * U(0.36f, 0.5f), "tron",
                    Th.pal, Front, 3, -160, 1.5f, 0, 0), 1, 0.5f, 0);
            });

            // cầu đầy: vòng co sát cầu (không còn vòng nâu to), toé tia; giữ tới lúc bắn thì cụm tàn lửa lách tách
            At(tDay, () =>
            {
                Shake?.Invoke(0.18f);
                var c = Tam(PhapDay);
                float r = Rt(PhapDay);
                HoaVongCo(TamT, r * 2.1f, r * 1.05f, 0.2f, Th.ring2);
                for (int j = 0; j < 6; j++)
                {
                    float a = 6.28f * (j + U(0, 0.7f)) / 6;
                    var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Spark(c + o * r, o, U(220, 380), 0, 6, 120);
                }
            });
            Every(tDay, tBan, 7, x =>
            {
                float tc = T - goc - t00, a = U(0, 6.28f);
                var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                HoaTan(Tam(tc) + o * Rt(tc) * 1.1f, new Vector2(o.x, o.y - 0.6f) * U(50, 130), U(0.3f, 0.5f), 3);
            });

            // bắn: quả cầu hạt nhận chỗ của cầu rig, lấy đà rồi lao thẳng vào đối thủ; đuôi lưỡi lửa, khói, tia
            var from = Tam(PhapBanCau);
            var tgt = foeBody + new Vector2(-dir * 0.06f * tH, 0);
            var d0 = Unit(tgt - from);
            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - goc - tBan) / bay);
                return from + (tgt - from) * (x * (0.35f + 0.65f * x));
            }
            float Rb(float t) => R * (1 - 0.22f * Mathf.Clamp01((t - goc - tBan) / bay)); // co nhẹ lúc lao (nhìn như bị nén)
            At(tBan, () =>
            {
                Shake?.Invoke(0.25f);
                for (int j = 0; j < 6; j++) Spark(from, -d0 + U2(-0.8f, 0.8f), U(240, 420), 0, 6);
                HoaCau(Bay, Rb, bay + 0.01f); // khối cầu lửa nhiều múi nhận chỗ, nhận cỡ của cầu rig vừa biến mất
            });
            Every(tBan, L, 60, x =>
            {
                var q = Flame(Bay(T) - d0 * R * 0.3f + U2(-0.5f, 0.5f) * R, -d0 * U(80, 180) + new Vector2(-d0.y, d0.x) * U(-110, 110) + new Vector2(0, -20),
                    U(0.22f, 0.34f), R * 0.7f, R * 0.7f, "tron", Th.pal, Front, 3, -140, 1.4f, 0, 0);
                HoaLuoi(q, 1, 0.2f, 0);
                q.sizeFn = (z, k) => z.r1 * Mathf.Pow(1 - k, 1.1f);
            });
            HoaDuoiKhoi(t => Bay(t) - d0 * R, tBan + 0.03f, L, 13, 17);
            Every(tBan, L, 16, x => Spark(Bay(T), -d0 + U2(-0.6f, 0.6f), U(180, 320), 0, 6));

            // chạm: nổ lớn KR5, hai vụ nổ phụ, khói cụm và tro
            At(L, () =>
            {
                NuocPulse?.Invoke(1f);
                HoaCauNo(tgt, foeFeet, tH, dir, non ? 1.2f : 1.6f);
            });
            At(L + 0.12f, () =>
            {
                Shake?.Invoke(0.3f);
                HoaNo(tgt + new Vector2(dir * U(4, 22), U(-30, 6)), non ? 0.55f : 0.8f, tH);
            });
            if (!non) At(L + 0.24f, () => HoaNo(tgt + new Vector2(-dir * U(4, 20), U(-12, 14)), 0.55f, tH));
            At(L + 0.36f, () =>
            {
                for (int i = 0; i < 3; i++)
                    HoaKhoi(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.15f, 0.5f) * tH), U(0.14f, 0.18f) * tH, Back, null, 0, true, 0.5f);
                for (int i = 0; i < 4; i++) Ash(foeBody + U2(-30, 30));
            });
            return L;
        }
    }
}
