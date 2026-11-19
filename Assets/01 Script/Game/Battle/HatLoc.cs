// Bộ CẦU NĂNG LƯỢNG của Lộc Phong (2026-11-12, hươu gỗ lá phong, suất bom_la đảo Mộc; rig ArtGen/Spine/huou_go*.py).
// Người dùng: "mana hơi cúi đầu, tụ 1 quả cầu năng lượng nhỏ ở giữa 2 sừng rồi bắn 1 tia từ quả cầu đó vào đối thủ"; "chiêu cuối đứng
// bằng 2 chân, ngửa đầu há to mồm tụ 1 quả cầu siêu to, khi tụ xong gật đầu nện mạnh vào đối thủ".
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes.
// Dùng lại quả cầu lá và gió hút của Gạc Đá (HatDa.cs: CauLa, GatherLa).
// Nâng 2026-11-18 (người dùng: tia cuối cụt lủn, không va chạm; tia trông như nước; hút khí quanh cầu xấu): tia riêng của bộ Mộc (TiaMoc ở
// HatMoc.cs: lõi chanh kem rộng, đầu tia tới mặt trước thân đối thủ, bông va chạm toé liên tục, tắt bằng vỡ vụn) thay tia nước NTia; cầu
// nén 1–2 khung rồi chớp lúc nhả; nổ cầu chiêu cuối kiểu Kingdom Rush 5 (NoCau).
// Mốc của clip (huou_go_clip.py dạng 2 / huou_go_non_clip.py dạng 1):
//   cast : tụ = lead − 0,62 s (đầu đã cúi xong), bắn = lead, tia chảy 0,88 s.
//   skill: tụ = lead − 1,45 s (mồm vừa há), cầu đầy = lead − 0,28, ngả sau lấy đà, rời mõm = lead − 0,06, trúng = lead.
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // CẦU GẠC + TIA (chiêu mana): gió và lá quanh đầu bị hút xoắn về điểm giữa hai gạc (mouth = xương `mieng` của rig ở khung bắn), quả cầu
        // nhỏ lớn dần, đập nhanh dần; ngay trước khung bắn cầu nén 1–2 khung rồi chớp, nhả tia năng lượng thẳng vào MẶT TRƯỚC thân đối thủ (bông
        // va chạm toé ngược liên tục, đối thủ giật từng nhịp); cầu co dần trong lúc tia chảy; hết tia thì tia thon từ gốc tới ngọn, vỡ vụn, lá nổ
        // nhỏ ở chỗ chạm.
        public float NCauTia(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (HasTia(DaTiaMoc)) return NCauTiaFb(casterH, mouth, foeBody, foeFeet, tH, lead); // tia vẽ sẵn (2026-11-19); chưa đủ ảnh thì tia hạt cũ
            MocSang();
            float L = Mathf.Max(0.3f, lead);
            float tTu = Mathf.Max(0.02f, L - 0.62f);
            const float dur = 0.88f;
            float rFull = 0.11f * casterH;
            Func<float, Vector2> cFn = age => mouth + new Vector2(0, 1.5f * Mathf.Sin(age * 11));
            Func<float, float> rFn = age =>
            {
                float t = tTu + age;
                if (t > L + dur) return 0;
                float g = Mathf.Clamp01(age / Mathf.Max(0.1f, L - tTu));
                float r = rFull * (0.2f + 0.8f * g) * Mathf.Min(1, age / 0.08f);
                if (t > L) r *= 1 - 0.45f * Mathf.Clamp01((t - L) / dur); // nhả tia: cầu cạn dần
                return r * NenNha(t, L);
            };
            At(tTu, () =>
            {
                CauLa(cFn, L + dur - tTu, rFn, Front, L - tTu);
                GatherLa(cFn, 0, L - tTu - 0.04f, 0.42f * casterH, 24);
            });
            At(L, () =>
            {
                Shake?.Invoke(0.3f);
                Chop(mouth, 0.3f * casterH, 0.08f);
                WExtra(mouth, 3, 200);
            });
            // giờ trúng giữ như bản tia nước cũ (NTia: T0 + travel) để khựng / số sát thương không lệch
            float travel = Mathf.Max(0.03f, ((foeBody - mouth).magnitude - 30) / 1150f);
            float hw = 0.055f * Mathf.Max(casterH, tH);
            float datY = foeFeet.y;
            At(L, () => TiaMoc(mouth, ChamThan(mouth, foeBody, tH), travel, dur, hw, tH, 1, datY));
            At(L + dur, () => LaNo(foeBody, foeFeet, tH, 0.7f));
            return L + travel;
        }

        // lá phong đỏ cam cuốn theo tia vẽ sẵn (mực, đậm, giữa, tươi, kem: DrawLeaf dùng ô 2 và 3)
        static readonly Color[] LaPhong = { C(43, 33, 24), C(176, 62, 26), C(232, 98, 36), C(250, 150, 58), C(255, 236, 200) };

        // CẦU GẠC + TIA bằng TIA VẼ SẴN (2026-11-19, người dùng: "các tia năng lượng/nước như này nhìn vẫn chưa đã": thân tia là ống xanh thẳng
        // đặc, chỗ trúng nhỏ). TiaFb (HatTiaFb.cs, da DaTiaMoc) thay thân tia TiaMoc + quả cầu nhỏ CauLa + bông trúng:
        //  - tụ: cầu xoáy đầu nòng lớn dần ở điểm giữa hai gạc từ mốc tụ cũ (lead − 0,62); gió và lá vẫn bị hút xoắn vào (GatherLa, với rộng hơn
        //    vì cầu mới to hơn cầu cũ);
        //  - giờ chạm GIỮ như cũ (lead + quãng/1150): TiaFb vươn đầu tia mất tVuon giây, nên lúc phóng lùi lại cho đầu tia chạm đúng giờ cũ;
        //    chớp nòng dời theo lúc phóng; bề dày 0,22 casterH (tia cũ 0,11 lần chiều cao lớn hơn giữa hai con);
        //  - dội: tia nhả tới mốc tắt cũ (lead + 0,68), nhịp trúng như TiaMoc (chạm: rung 0,3 + DanhTrung 0,7; rồi mỗi 0,12 s DanhTrung 0,3 +
        //    rung 0,1 tới lead + 0,84); tia vụn và lá xanh / lá phong toé ngược theo nhịp, bụi dưới chân đối thủ;
        //  - tắt: đuôi tia rời nòng bay nốt vào đích (TiaFb); vài mảnh năng lượng bay theo hướng tia rồi rơi; đuôi tới đích thì lá nổ nhỏ.
        float NCauTiaFb(float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.3f, lead);
            float tTu = Mathf.Max(0.02f, L - 0.62f);
            float travel = Mathf.Max(0.03f, ((foeBody - mouth).magnitude - 30) / 1150f); // giờ trúng như bản cũ
            float hit = L + travel;
            var cham = ChamThan(mouth, foeBody, tH);
            var u = Unit(cham - mouth);
            var nrm = new Vector2(-u.y, u.x);
            float dai = (cham - mouth).magnitude;
            float tVuon = Mathf.Clamp(dai / 2600f, 0.07f, 0.14f); // như TiaFb: đầu tia vươn tới đích
            float tPhong = Mathf.Max(tTu + 0.05f, hit - tVuon);   // lúc phóng để đầu tia chạm đúng giờ cũ
            float tBan = Mathf.Max(0.3f, L + 0.68f - hit);         // dội tới mốc tắt cũ của TiaMoc
            float tNgung = hit + tBan;                              // ngừng nhả: đuôi rời nòng
            float tDuoi = dai / Mathf.Max(380, dai / 0.32f);        // đuôi bay nốt vào đích (tốc trôi đoạn của TiaFb)
            float day = 0.22f * casterH;
            var w = W;
            At(tTu, () =>
            {
                TiaFb(DaTiaMoc, () => mouth, () => cham, day, tPhong - tTu, tBan);
                GatherLa(t => mouth, 0, tPhong - tTu - 0.04f, 0.6f * casterH, 24);
            });
            At(tPhong, () => // chớp nòng đúng lúc tia phóng
            {
                Shake?.Invoke(0.3f);
                Chop(mouth, 0.3f * casterH, 0.08f);
                WExtra(mouth, 3, 200);
            });
            // chạm: rung + đối thủ giật, chùm tia vụn toé ngược; rồi nhịp trúng mỗi 0,12 s như TiaMoc
            At(hit, () =>
            {
                Shake?.Invoke(0.3f);
                DanhTrung?.Invoke(cham, 0.7f);
                TiaVunCum(cham, -u, 1.2f, 5, 520, 4.4f);
            });
            int nv = Mathf.Max(1, Mathf.FloorToInt((L + 0.84f - hit) / 0.12f));
            for (int i = 0; i < nv; i++)
            {
                int ii = i;
                At(hit + 0.06f + 0.12f * i, () =>
                {
                    DanhTrung?.Invoke(cham, 0.3f);
                    Shake?.Invoke(0.1f);
                    // mỗi nhịp một chiếc lá (xen lá phong đỏ cam / lá xanh) bật ngược khỏi chỗ trúng
                    var q = Leaf(cham + U2(-6, 6), Unit(-u + nrm * U(-1.1f, 1.1f)) * U(180, 340) + new Vector2(0, -U(40, 120)), U(0.4f, 0.6f), U(3.6f, 5.4f), 620, 2f,
                        U(0, 1) < 0.6f ? Front : Back);
                    if ((ii & 1) == 0) q.stops = LaPhong;
                });
            }
            // tia vụn toé ngược theo cụm suốt lúc dội (thưa hơn TiaMoc: bông trúng vẽ sẵn đã toé)
            Every(hit, tNgung, 7, x =>
                TiaVunCum(cham + nrm * U(-0.4f, 0.4f) * day, -u, 1.3f, 3, U(300, 480), U(3f, 4.4f), U(0, 1) < 0.7f ? Front : Back, MocChanh, w[3]));
            // bụi dưới chân đối thủ (cụm khói nhuộm đất; chưa nhập khung thì BuiCum)
            bool kh = HasFb("khoi");
            Every(hit, tNgung, kh ? 2 : 3, x =>
            {
                var at = new Vector2(cham.x + U(-0.25f, 0.25f) * tH, foeFeet.y + U(-4, 2));
                if (kh) MocKhoiFb(at, U(0.08f, 0.11f) * tH, new Vector2(u.x * U(40, 100), -U(20, 40)), Back, 3.5f, 1.3f, 0.85f);
                else BuiCum(at, new Vector2(U(-60, 60), -U(20, 50)), U(0.08f, 0.12f) * tH, 0, Back);
            });
            // tắt: vài mảnh năng lượng bay theo hướng tia rồi rơi (đuôi tia đang bay nốt vào đích)
            for (int j = 0; j < 6; j++)
            {
                int jj = j;
                At(tNgung + 0.03f * j, () =>
                {
                    var at = mouth + u * dai * U(0.1f, 0.6f) + nrm * U(-0.5f, 0.5f) * day;
                    var p = new P
                    {
                        pos = at, vel = u * U(260, 460) + nrm * U(-60, 60) + new Vector2(0, -U(10, 50)), life = U(0.32f, 0.5f), drag = 2.2f,
                        acc = new Vector2(0, 360), sz = day * U(0.18f, 0.3f), spin = U(-400, 400), ang = VelAng(u), group = Front,
                        col = (jj & 1) == 0 ? MocChanh : w[3]
                    };
                    p.draw = DrawMangVo;
                    Add(p);
                    if (jj % 3 == 1) LaRoi(at, u * U(60, 140) + new Vector2(0, -U(20, 50)), U(0.5f, 0.8f), U(3.5f, 5f), Front).stops = LaPhong;
                });
            }
            At(tNgung + tDuoi, () => LaNo(foeBody, foeFeet, tH, 0.7f)); // đuôi tia tới đích: lá nổ nhỏ
            return hit;
        }

        // CẦU RỪNG THU (chiêu cuối): con vật dựng người, ngửa đầu há mồm: gió, lá quanh người bị hút về điểm trước mõm, quả cầu lớn dần
        // tới cỡ một phần ba thân, đập nhanh dần; đầy thì một vòng sáng lan; ngả ra sau một nhịp, cầu nén 1–2 khung rồi chớp lúc GẬT đầu: cầu
        // rời mõm lao chéo xuống thân đối thủ, kéo đuôi lá; trúng: nổ cầu (NoCau: chớp, khối nhiều múi sau thân, lưỡi liềm, lá, bụi cụm tách
        // dần, vòng cung dẹt, vết đất), lá rơi lượn.
        // truoc, len: tâm cầu so với chân, tính bằng chiều cao tướng (ra phía đối thủ, lên trên). Đo trên ảnh chụp trận 2026-11-12: mõm
        // lúc ngửa đầu của dạng 2 ở (−0,05; 0,88), dạng 1 ở (−0,15; 0,75); cầu bán kính 0,36 nằm chếch lên phía trước mõm, mép chạm mõm.
        public float NCauMom(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float truoc = 0.22f,
            float len = 1.15f)
        {
            MocSang();
            float L = Mathf.Max(0.7f, lead);
            float tTu = Mathf.Max(0.05f, L - 1.45f), tDay = L - 0.28f, tNem = L - 0.06f;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var c0 = casterFeet + new Vector2(truoc * dir * casterH, -len * casterH);       // chếch lên trước mõm lúc đang ngửa đầu
            var cNga = c0 + new Vector2(-0.10f * dir * casterH, -0.06f * casterH);          // ngả ra sau lấy đà
            float fly = Mathf.Clamp((foeBody - c0).magnitude / 1700f, 0.10f, 0.24f);
            float hit = tNem + fly;
            float rFull = 0.36f * casterH;
            Func<float, Vector2> cFn = age =>
            {
                float t = tTu + age;
                if (t < tDay) return c0 + new Vector2(0, 3f * Mathf.Sin(age * 8));
                if (t < tNem) return Vector2.Lerp(c0, cNga, SmoothStep(tDay, tNem - 0.04f, t));
                float k = Mathf.Clamp01((t - tNem) / fly);
                return Vector2.Lerp(cNga, foeBody, k * k);                                 // nện: càng gần càng nhanh
            };
            Func<float, float> rFn = age =>
            {
                float t = tTu + age;
                if (t > hit - 0.02f) return 0;
                float g = Mathf.Clamp01(age / Mathf.Max(0.1f, tDay - tTu));
                float r = rFull * (0.18f + 0.82f * g) * Mathf.Min(1, age / 0.1f);
                return r * NenNha(t, tNem);
            };
            At(tTu, () =>
            {
                CauLa(cFn, hit - tTu, rFn, Front, tNem - tTu);
                CungDat(casterFeet + new Vector2(0, 2), 0.15f * casterH, 0.7f * casterH, 0.5f, W[2], 0.07f * casterH);
                GatherLa(cFn, 0, tNem - tTu - 0.04f, 1.25f * casterH, 60);
                // bụi dưới chân bị cuốn lên (khung vẽ sẵn 2026-11-19: cụm khói nhuộm đất bay lên, thưa hơn vì mỗi cụm to và sống lâu hơn; chưa nhập
                // khung thì BuiCum cũ)
                bool kh = HasFb("khoi");
                Every(0, tDay - tTu, kh ? 4 : 6, x =>
                {
                    var at = casterFeet + new Vector2(U(-0.55f, 0.55f) * casterH, U(-4, 2));
                    if (kh) MocKhoiFb(at, U(0.07f, 0.1f) * casterH, new Vector2(U(-30, 30), -U(80, 130)), Back, 2.5f, 1.1f, 0.85f);
                    else BuiCum(at, new Vector2(U(-30, 30), -U(100, 180)), U(0.06f, 0.09f) * casterH, 0, Back);
                });
            });
            At(tDay, () =>
            {
                Shake?.Invoke(0.25f);
                VongVa(c0, 0.25f * casterH, 0.85f * casterH, 0.3f, MocKem, Back);
            });
            At(tNem, () => // gật đầu: chớp đúng lúc cầu bật ra sau 1–2 khung nén
            {
                Shake?.Invoke(0.35f);
                Chop(cNga, 0.6f * casterH, 0.08f);
                WExtra(cNga, 5, 240);
            });
            float goc = T;
            Every(tNem, hit, 70, x =>
            {
                var at = cFn(T - goc - tTu);
                if (U(0, 1) < 0.7f) Leaf(at + U2(-8, 8), new Vector2(-dir * U(80, 200), U(-120, 60)), U(0.3f, 0.5f), U(3.6f, 6f), 300, 1.5f);
                else TiaVunCum(at, new Vector2(-dir, U(-0.5f, 0.3f)), 0.5f, 2, U(140, 240), U(3f, 4.4f));
            });
            At(hit, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(FlashW);
                NoCau(foeBody, foeFeet, tH, 1.7f);
                WExtra(foeBody, 8, 360);
            });
            At(hit + 0.1f, () => BurstFlash(foeBody + new Vector2(0, -0.12f * tH), 0.5f * tH, Back, 0.16f)); // nhịp toé thứ hai ở sau thân
            return hit;
        }
    }
}
