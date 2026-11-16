// Bộ THIẾT CƯA (2026-11-16, tinh linh đuôi máy cưa, suất phi_thuong ải 15 đảo Kim; rig ArtGen/Spine/cua_xich_rig.py (rig gốc
// monster_3374), cả hai dạng chung rig cua_xich_1; ghi chú ArtGen/Spine/inbox/cua_xich_ghichu.md).
// Người dùng: đánh thường "lao vào húc đối thủ"; chiêu mana "dùng đuôi cưa quật đối thủ"; chiêu cuối "kéo thêm dây kéo nhiều lần nữa, cưa quay
// nhanh hơn và to ra chút, có hiệu ứng thêm vào kiểu hút khí xung quanh... sau đó dùng đuôi cưa liên tục đối thủ (kiểu đối thủ bị attack liên
// tục), có hiệu ứng tia lửa bắn ra". Cả ba đòn đều do rig lao tới (tướng tự quật, không có đạn): lớp này chỉ thêm hạt đúng các mốc của clip.
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc), phát lúc clip BẮT ĐẦU; mốc là giây clip của rig, co theo `lead` (giờ trúng của clip).
// - n_cua_huc (đòn thường): mai đầu húc vào thân đối thủ: chớp sắt, tia lửa, dăm thép, bụi dưới chân.
// - n_cua_quat (chiêu mana): đĩa cưa quật trúng: chớp, chùm TIA LỬA cưa toé ngược lên, dăm thép, vòng sóng, bụi.
// - n_cua_lien (chiêu cuối): mỗi lần giật dây: khói xám phụt ở đĩa cưa (lần cuối máy nổ: khói to + tia lửa); 1,05–1,5 s vệt gió HÚT VÀO
//   đĩa cưa từ quanh tướng; từ lúc ghì cưa: 11 nhát, mỗi nhát một chùm tia lửa + dăm thép ở chỗ cưa chạm, rung nhẹ; nhát cuối nổ to hơn.
// Chỗ đĩa cưa lúc đứng (phần của chiều cao KHAI cho game, x về phía trước, y lên): đo ở khung 0 idle của rig (xương bone25).
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        const float CuALead = 0.50f, CuCLead = 0.47f, CuSLead = 1.78f;
        static readonly float[] CuSKeo = { 0.30f, 0.66f, 0.98f };
        const float CuSNo = 1.08f, CuSHut0 = 1.05f, CuSHut1 = 1.50f, CuSNha = 3.02f;
        const int CuSNhat = 11;
        static readonly Vector2 CuDia = new Vector2(-0.39f, 0.52f); // tâm đĩa cưa lúc đứng
        // tâm đĩa cưa so với chân lúc QUAY NGƯỜI vươn đuôi tới trước (skill_03_1 của rig: quật lúc trúng cast, giữ lúc ghì cưa). Rig vươn đuôi
        // nằm ngang còn sân nắn cú lao chéo tới 72 % quãng (AolaSticker.Lunge) nên đĩa nằm ngang chân / bụng đối thủ, không ở giữa thân nó:
        // hạt toé ở ĐĨA (đỉnh lao + độ vươn này), không ở thân đối thủ (tour 2026-11-16: tia lửa toé trên đầu tướng).
        static readonly Vector2 CuDiaQuat = new Vector2(0.66f, 0.20f), CuDiaGhi = new Vector2(0.68f, 0.15f);

        static Vector2 CuDinhLao(Vector2 casterFeet, Vector2 foeFeet) => casterFeet + (foeFeet - casterFeet) * 0.72f;
        static readonly Color CuThep = C(170, 174, 184), CuGio = C(236, 238, 244);

        // chùm tia lửa cưa: văng ngược về phía tướng và lên trên, nóng vàng cam (Th.spark), vài viên rơi xa
        void CuTiaLua(Vector2 c, float dir, int n, float manh)
        {
            for (int i = 0; i < n; i++)
                Spark(c + U2(-4, 4), new Vector2(-dir * U(0.15f, 1f), U(-1f, -0.15f)), U(260, 520) * manh, U(0.22f, 0.42f), U(6, 9) * manh, 650, Front, 3);
        }

        // một nhát trúng: chớp + tia lửa + dăm thép (+ bụi chân đối thủ nếu bui)
        void CuTrung(Vector2 c, Vector2 foeFeet, float dir, float tH, float manh, int tia, int dam, bool bui)
        {
            SatChop(c, 0.38f * tH * manh, Front, 0.12f);
            CuTiaLua(c, dir, tia, manh);
            for (int i = 0; i < dam; i++) GiaoDam(c + U2(-5, 5), new Vector2(-dir * U(-0.3f, 1f), -U(0.2f, 1f)) * U(140, 300), U(8, 13) * manh);
            if (!bui) return;
            for (int i = 0; i < 3; i++)
            {
                float sd = (i & 1) == 0 ? 1 : -1;
                Bui(foeFeet + new Vector2(sd * U(6, 0.25f * tH), U(-5, 2)), new Vector2(sd * U(90, 220), -U(10, 50)), 0, 4, 11, Back);
            }
        }

        // ĐÒN THƯỜNG: lao tới húc. lead: giây từ đầu clip attack tới lúc chạm.
        public float NCuaHuc(Vector2 casterFeet, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var c = foeBody + new Vector2(-dir * 0.26f * tH, 0.02f * tH);
            At(Mathf.Max(0.02f, lead), () =>
            {
                Shake?.Invoke(0.26f);
                CuTrung(c, foeFeet, dir, tH, 1f, 6, 5, true);
            });
            return Mathf.Max(0.02f, lead);
        }

        // CHIÊU MANA: lao tới, quay người, đuôi cưa quật ngang trúng thân đối thủ.
        public float NCuaQuat(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.02f, lead);
            var c = CuDinhLao(casterFeet, foeFeet) + new Vector2(dir * CuDiaQuat.x * casterH, -CuDiaQuat.y * casterH);
            At(t0, () =>
            {
                Shake?.Invoke(0.34f);
                CuTrung(c, foeFeet, dir, tH, 1.1f, 14, 7, true);
                Ring(c, 0.3f, 0.06f * tH, 0.5f * tH, CuThep, 0.5f, Front, 32);
            });
            At(t0 + 0.08f, () => CuTiaLua(c, dir, 6, 0.8f)); // đĩa còn quay rà thêm một chút
            return t0;
        }

        // CHIÊU CUỐI: giật dây ba lần (khói, máy nổ), hút khí vào đĩa cưa, lao tới ghì cưa 11 nhát.
        public float NCuaLien(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.3f, lead), k = t0 / CuSLead;
            var dia = casterFeet + new Vector2(dir * CuDia.x * casterH, -CuDia.y * casterH);
            // giật dây: khói xám phụt ở đĩa (máy hắt hơi), lần cuối máy nổ: khói to, tia lửa, rung
            for (int j = 0; j < CuSKeo.Length; j++)
            {
                int jj = j;
                At(CuSKeo[j] * k + 0.1f * k, () =>
                {
                    int n = 2 + jj;
                    for (int i = 0; i < n; i++)
                        Smoke(dia + U2(-6, 6), new Vector2(-dir * U(30, 90), -U(40, 110)), U(0.6f, 0.9f), 6, 14 + 4 * jj, Back, "dark", 0.2f);
                });
            }
            At(CuSNo * k, () =>
            {
                Shake?.Invoke(0.22f);
                for (int i = 0; i < 6; i++)
                    Smoke(dia + U2(-8, 8), new Vector2(-dir * U(40, 140), -U(50, 160)), U(0.8f, 1.2f), 8, 26, Back, "dark", 0.3f);
                for (int i = 0; i < 10; i++)
                    Spark(dia + U2(-6, 6), new Vector2(U(-1f, 1f), U(-1f, 0.2f)), U(200, 380), U(0.2f, 0.34f), U(6, 8), 500, Front, 3);
            });
            // hút khí: vệt gió sinh trên vòng quanh tướng, bay vào tâm đĩa cưa, nhanh dần
            Every(CuSHut0 * k, CuSHut1 * k, 46, x =>
            {
                float a = U(0, Mathf.PI * 2), R = U(0.7f, 1.1f) * casterH;
                var p = dia + new Vector2(Mathf.Cos(a) * R, Mathf.Sin(a) * R * 0.75f);
                var v = dia - p;
                float life = U(0.22f, 0.32f);
                var q = Spark(p, v, v.magnitude / life * 1.15f, life, U(5, 7), 0, Front, 0.3f);
                q.col = CuGio;
            });
            At(CuSHut1 * k, () => Ring(dia, 0.28f, 0.5f * casterH, 0.08f * casterH, CuGio, 0.6f, Front, 32)); // vòng gió co vào đĩa
            // ghì cưa: 11 nhát dồn dập ở chỗ cưa chạm thân đối thủ; nhát cuối mạnh hơn
            var c = CuDinhLao(casterFeet, foeFeet) + new Vector2(dir * CuDiaGhi.x * casterH, -CuDiaGhi.y * casterH);
            float buoc = (CuSNha - CuSLead - 0.08f) / (CuSNhat - 1);
            for (int j = 0; j < CuSNhat; j++)
            {
                bool cuoi = j == CuSNhat - 1;
                At(t0 + j * buoc * k, () =>
                {
                    Shake?.Invoke(cuoi ? 0.42f : 0.14f);
                    CuTrung(c + U2(-0.05f * tH, 0.05f * tH), foeFeet, dir, tH, cuoi ? 1.25f : 0.85f, cuoi ? 18 : 9, cuoi ? 8 : 3, cuoi);
                    if (cuoi) Ring(c, 0.34f, 0.06f * tH, 0.6f * tH, CuThep, 0.5f, Front, 32);
                });
            }
            return t0;
        }
    }
}
