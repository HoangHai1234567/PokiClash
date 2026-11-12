// Bộ CẦU NĂNG LƯỢNG của Lộc Phong (2026-11-12, hươu gỗ lá phong, suất bom_la đảo Mộc; rig ArtGen/Spine/huou_go*.py).
// Người dùng: "mana hơi cúi đầu, tụ 1 quả cầu năng lượng nhỏ ở giữa 2 sừng rồi bắn 1 tia từ quả cầu đó vào đối thủ"; "chiêu cuối đứng
// bằng 2 chân, ngửa đầu há to mồm tụ 1 quả cầu siêu to, khi tụ xong gật đầu nện mạnh vào đối thủ".
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes.
// Dùng lại quả cầu lá và gió hút của Gạc Đá (HatDa.cs: CauLa, GatherLa) và tia của bộ Thủy (NTia, nhuộm theo bảng màu của tướng).
// Mốc của clip (huou_go_clip.py dạng 2 / huou_go_non_clip.py dạng 1):
//   cast : tụ = lead − 0,62 s (đầu đã cúi xong), bắn = lead, tia chảy 0,88 s.
//   skill: tụ = lead − 1,45 s (mồm vừa há), cầu đầy = lead − 0,28, ngả sau lấy đà, rời mõm = lead − 0,06, trúng = lead.
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // CẦU GẠC + TIA (chiêu mana): gió và lá quanh đầu bị hút về điểm giữa hai gạc (mouth = xương `mieng` của rig ở khung bắn), quả
        // cầu nhỏ lớn dần, đập nhanh dần; đầy thì chớp một nhịp rồi nhả tia thẳng vào thân đối thủ; cầu co dần trong lúc tia chảy.
        public float NCauTia(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
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
                return r * (1 + 0.06f * Mathf.Sin(age * (12 + 12 * g)));
            };
            At(tTu, () =>
            {
                CauLa(cFn, L + dur - tTu, rFn);
                GatherLa(cFn, 0, L - tTu - 0.04f, 0.42f * casterH, 22);
            });
            At(L, () =>
            {
                Shake?.Invoke(0.3f);
                BurstFlash(mouth, 0.34f * casterH, Back);
                WExtra(mouth, 4, 200);
            });
            // tia: gọi NTia SÁT khung bắn (lead 0,14 s). NTia tự tụ giọt + cầu nước nhỏ ở miệng suốt từ lúc gọi; gọi từ đầu clip thì đám
            // giọt ấy hiện ở chỗ giữa gạc khi đầu chưa cúi tới và che mất quả cầu (soi ảnh chụp trận 2026-11-12).
            float casterGround = casterFeet.y;
            At(L - 0.14f, () => NTia(mouth, foeBody, foeFeet, casterGround, tH, 0.14f, dur));
            return L + Mathf.Max(0.03f, ((foeBody - mouth).magnitude - 30) / 1150f); // = giờ trúng NTia tự tính (T0 + travel)
        }

        // CẦU RỪNG THU (chiêu cuối): con vật dựng người, ngửa đầu há mồm: gió, lá quanh người bị hút về điểm trước mõm, quả cầu lớn dần
        // tới cỡ một phần ba thân, đập nhanh dần; đầy thì chớp; ngả ra sau một nhịp rồi GẬT đầu: cầu rời mõm lao chéo xuống thân đối thủ,
        // kéo đuôi lá; trúng: nổ lá to, vòng lan, bụi dưới chân, lá rơi lả tả.
        // truoc, len: tâm cầu so với chân, tính bằng chiều cao tướng (ra phía đối thủ, lên trên). Đo trên ảnh chụp trận 2026-11-12: mõm
        // lúc ngửa đầu của dạng 2 ở (−0,05; 0,88), dạng 1 ở (−0,15; 0,75); cầu bán kính 0,36 nằm chếch lên phía trước mõm, mép chạm mõm.
        public float NCauMom(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float truoc = 0.22f,
            float len = 1.15f)
        {
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
                if (tTu + age > hit - 0.02f) return 0;
                float g = Mathf.Clamp01(age / Mathf.Max(0.1f, tDay - tTu));
                float r = rFull * (0.18f + 0.82f * g) * Mathf.Min(1, age / 0.1f);
                return r * (1 + 0.05f * Mathf.Sin(age * (9 + 11 * g)));
            };
            At(tTu, () =>
            {
                CauLa(cFn, hit - tTu, rFn);
                Ripple(casterFeet + new Vector2(0, 2), 0.15f * casterH, 0.7f * casterH, 0.5f);
                GatherLa(cFn, 0, tDay - tTu, 1.25f * casterH, 84);
                Every(0, tDay - tTu, 10, x =>
                    Foam(casterFeet + new Vector2(U(-0.55f, 0.55f) * casterH, U(-4, 2)), new Vector2(U(-30, 30), -U(130, 240)), 0, 2.5f, 7, Back));
            });
            At(tDay, () =>
            {
                Shake?.Invoke(0.3f);
                BurstFlash(c0, 0.74f * casterH, Back);
                WExtra(c0, 6, 240);
            });
            At(tNem, () => Shake?.Invoke(0.35f));
            float goc = T;
            Every(tNem, hit, 80, x =>
            {
                var at = cFn(T - goc - tTu);
                Leaf(at + U2(-8, 8), new Vector2(-dir * U(80, 200), U(-120, 60)), U(0.3f, 0.5f), U(4.5f, 7.5f), 300, 1.5f);
            });
            At(hit, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(FlashW);
                LaNo(foeBody, foeFeet, tH, 1.8f);
                RingN(foeBody, 0.32f, 0.14f * tH, 0.78f * tH, W[3], 1, Front, 36);
                WExtra(foeBody, 11, 360);
                Ripple(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.8f * tH);
                for (int i = 0; i < 9; i++)
                    Foam(foeFeet + new Vector2(U(-0.4f, 0.4f) * tH, U(-6, 2)), new Vector2(U(-130, 130), U(-60, -10)), 0, 4, 14, Back);
            });
            At(hit + 0.12f, () => BurstFlash(foeBody + new Vector2(0, -0.12f * tH), 0.4f * tH));
            Every(hit + 0.05f, hit + 0.5f, 30, x =>
                Leaf(foeBody + new Vector2(U(-0.55f, 0.55f) * tH, -U(0.2f, 0.75f) * tH), new Vector2(U(-40, 40), U(20, 80)), U(0.5f, 0.8f), U(4, 6.5f), 260, 1.2f,
                    U(0, 1) < 0.5f ? Back : Front));
            return hit;
        }
    }
}
