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

        // chùm tia lửa cưa: văng ngược về phía tướng và lên trên, BẮN NHANH RỒI KHỰNG (cản gắt, 2026-11-18), nóng vàng cam, vài viên rơi xa
        void CuTiaLua(Vector2 c, float dir, int n, float manh)
        {
            for (int i = 0; i < n; i++)
            {
                var q = Spark(c + U2(-4, 4), new Vector2(-dir * U(0.15f, 1f), U(-1f, -0.15f)), U(460, 820) * manh, U(0.24f, 0.4f), U(6, 9) * manh, 650, Front,
                    (i & 3) == 0 ? 3.5f : 7.5f);
                q.col = (i & 1) == 0 ? KmLua[4] : KmLua[3];
            }
        }

        // một nhát trúng: bông va chạm toé ngược về tướng + chớp + tia lửa + dăm thép (+ bụi chân đối thủ nếu bui)
        void CuTrung(Vector2 c, Vector2 foeFeet, float dir, float tH, float manh, int tia, int dam, bool bui)
        {
            KmBong(c, new Vector2(-dir, -0.5f), 0.3f * tH * manh, 0.1f, KmLua);
            SatChop(c, 0.3f * tH * manh, Front, 0.1f);
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
            // giật dây (2026-11-18: người dùng chê khói rải rác, chưa thành cụm): CỤM KHÓI THAN nhiều múi hai tông phụt ở đĩa (máy hắt hơi), bay lên,
            // tách cụm rồi mới mờ, có tro; mỗi lần to hơn; lần cuối máy NỔ: chớp nhỏ, khối khói to, tia lửa bắn rồi khựng, rung
            for (int j = 0; j < CuSKeo.Length; j++)
            {
                int jj = j;
                At(CuSKeo[j] * k + 0.1f * k, () =>
                {
                    // khung vẽ sẵn (2026-11-19): có khung "khoi" (KmKhoi đổi sang khung) thì MỘT cụm to dần mỗi lần, vì nhiều khung cùng chỗ chồng
                    // thành bóng đôi
                    bool fb = HasFb("khoi");
                    for (int i = 0; i < (fb ? 1 : 1 + jj); i++)
                        KmKhoi(dia + U2(-6, 6), new Vector2(-dir * U(30, 90), -U(50, 110)), (0.1f + 0.025f * jj) * casterH * U(0.85f, 1.1f) * (fb ? 1 + 0.2f * jj : 1),
                            U(0.8f, 1.1f), Back, 0, jj == 0 ? 1 : 2, null, 0.4f);
                    KmKhoi(dia + new Vector2(-dir * 6, -4), new Vector2(-dir * U(60, 120), -U(20, 50)), 0.06f * casterH, U(0.5f, 0.7f), Back, 0, 0, null, 0, true);
                });
            }
            At(CuSNo * k, () =>
            {
                Shake?.Invoke(0.22f);
                KmChop(dia, 0.22f * casterH, 0.06f, KmLua);
                // khung vẽ sẵn (2026-11-19): có khung "khoi" thì hai cụm (một to ở đĩa, một vừa lệch ra sau, lên trên) thay ba cụm cùng chỗ
                bool fb = HasFb("khoi");
                for (int i = 0; i < (fb ? 2 : 3); i++)
                    KmKhoi(dia + (fb ? new Vector2(-dir * 0.12f * casterH, -0.07f * casterH) * i : U2(-8, 8)), new Vector2(-dir * U(40, 140), -U(60, 150)),
                        U(0.15f, 0.19f) * casterH * (fb ? (i == 0 ? 1.3f : 0.9f) : 1), U(1.0f, 1.3f), Back, 0.6f, 2, null, 0.5f);
                for (int i = 0; i < 8; i++)
                    KmTiaLua(dia + U2(-6, 6), new Vector2(U(-1f, 1f), U(-1f, 0.2f)), U(380, 640), U(6, 8), KmLua[3 + (i & 1)]);
            });
            // hút khí: VỆT GIÓ XOẮN ỐC vào đĩa cưa, nhanh dần, chạm vành đĩa thì nhập; dày dần; hai vòng gió co về đĩa
            float rDia = 0.12f * casterH;
            Every(CuSHut0 * k, CuSHut1 * k, x => 24 + 40 * x, x =>
                KmHut(_ => dia, _ => rDia, U(0.75f, 1.15f) * casterH, U(0.24f, 0.36f), U(6, 8), CuGio, -dir, Front, 0.75f));
            At((CuSHut0 + 0.4f * (CuSHut1 - CuSHut0)) * k, () => KmVong(_ => dia, 0.24f, 0.8f * casterH, rDia, CuGio, 0.75f, 0.75f));
            At(CuSHut1 * k, () => KmVong(_ => dia, 0.26f, 0.55f * casterH, rDia, CuGio, 0.75f, 0.85f)); // vòng gió co vào đĩa
            // ghì cưa: 11 nhát dồn dập ở chỗ cưa chạm thân đối thủ; nhát cuối mạnh hơn
            var c = CuDinhLao(casterFeet, foeFeet) + new Vector2(dir * CuDiaGhi.x * casterH, -CuDiaGhi.y * casterH);
            float buoc = (CuSNha - CuSLead - 0.08f) / (CuSNhat - 1);
            for (int j = 0; j < CuSNhat; j++)
            {
                bool cuoi = j == CuSNhat - 1;
                int jj = j;
                At(t0 + j * buoc * k, () =>
                {
                    Shake?.Invoke(cuoi ? 0.42f : 0.14f);
                    if (jj > 0) KmNhip(cuoi ? 0.8f : 0.4f);   // nhát đầu là cú trúng chính (StageView), các nhát sau: đối thủ chớp + giật theo nhịp cưa
                    CuTrung(c + U2(-0.05f * tH, 0.05f * tH), foeFeet, dir, tH, cuoi ? 1.25f : 0.85f, cuoi ? 18 : 9, cuoi ? 8 : 3, cuoi);
                    if (cuoi) Ring(c, 0.34f, 0.06f * tH, 0.6f * tH, CuThep, 0.5f, Front, 32);
                });
            }
            return t0;
        }
    }
}
