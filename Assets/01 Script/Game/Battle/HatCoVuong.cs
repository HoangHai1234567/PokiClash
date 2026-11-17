// Bộ của CỔ VƯƠNG (2026-11-17, tượng vua cổ rễ quấn cầm cột đá, suất gio_loc đảo Mộc, thay Linh Điểu; rig ArtGen/Spine/tuong_cot_rig.py
// (dạng 2, rig monster_3608) và tuong_cot_non_rig.py (dạng 1 Cổ Vương Nhi, rig monster_3273); bản xem trước tuong_cot_fx.py).
// Cột đá (cả cột tung lên trời, cột khổng lồ giáng xuống và bay về, cột nhỏ của dạng 1) là mảnh của RIG trên xương fly_cot → cot_bay
// (AolaActor.FarAtomik lái tới đối thủ thật); lớp này lo rễ, bụi, đá vỡ, lá, bóng báo trước.
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lá lấy từ WThemes.
// Mốc của clip:
//   dạng 2  attack: đập cột = lead (0,50) · cast: cột cắm đất lead − 0,36, rễ tới đối thủ = lead (1,12) · skill: tung cột lead − 1,08,
//           gồng lead − 1,02, cột bắt đầu giáng lead − 0,22, cắm = lead (1,64), rễ trồi lead + 0,08, bắt cột lead + 0,98
//   dạng 1  attack: húc = lead (0,46) · cast: nện tay lead − 0,33, rễ tới = lead (0,95) · skill: gồng gọi lead − 0,88, cột nhỏ bắt
//           đầu rơi lead − 0,23, cắm = lead (1,18)
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // rễ trồi khỏi đất: gai dài (ảnh hat_thorn của bộ Mộc) tô màu rễ nâu gỗ của Lâm Tượng
        P Re(Vector2 at, Vector2 dir, float len, float life, int group, int seed, float thick = 0.42f)
        {
            var q = Spike(at, dir, len, life, group, seed, thick);
            q.col = (seed & 1) == 0 ? ReC : ReC2;
            return q;
        }

        // rễ lớn trồi quanh chân đối thủ: ba cái cao phía sau lưng, hai cái thấp hai bên phía trước (không che mặt con bị trúng)
        void ReQuan(Vector2 foeFeet, float tH, float sc, float life)
        {
            var goc = new[] { (-0.34f, -0.3f, 1.1f, Back), (0.02f, 0.05f, 1.28f, Back), (0.36f, 0.32f, 1.0f, Back), (-0.5f, -0.75f, 0.46f, Front),
                (0.52f, 0.8f, 0.44f, Front) };
            for (int i = 0; i < goc.Length; i++)
            {
                var (ox, nghieng, dai, nhom) = goc[i];
                int ii = i;
                At(0.03f * i, () => Re(foeFeet + new Vector2(ox * tH, nhom == Back ? -2 : 7), new Vector2(nghieng, -1), dai * tH * sc, life - 0.03f * ii, nhom, ii,
                    nhom == Back ? 0.42f : 0.55f));
            }
        }

        // ĐẬP TRỤ (đòn thường dạng 2, tướng lao tới): giơ cột (bụi dưới chân), đập cột chúi xuống đầu đối thủ: chớp, tảng đá rêu văng, dăm đá,
        // vòng bụi dưới chân nó, lá rơi
        public float NTruDap(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            At(Mathf.Max(0.02f, L - 0.3f), () =>
            {
                for (int i = 0; i < 5; i++)
                    Bui(casterFeet + new Vector2(U(-14, 14), U(-4, 2)), new Vector2(-dir * U(60, 180), -U(20, 70)), U(0.35f, 0.55f), 3.5f, U(8, 12), Back);
            });
            At(L, () =>
            {
                Shake?.Invoke(0.6f);
                var cham = foeBody + new Vector2(-dir * 0.05f * tH, -0.32f * tH); // đầu đối thủ, nơi đầu cột đập xuống
                BurstFlash(cham, 0.5f * tH);
                for (int i = 0; i < 4; i++)
                {
                    float a = (-90 + (i - 1.5f) * 40 + U(-10, 10)) * Mathf.Deg2Rad;
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Thach(cham + d * U(4, 12), new Vector2(d.x * U(160, 320) + dir * 40, d.y * U(220, 420)), U(0.8f, 1.1f), U(5, 8), foeFeet.y + U(-8, 14),
                        (i & 1) == 0 ? Front : Back, i == 1);
                }
                for (int i = 0; i < 9; i++)
                {
                    float a = 6.28f * (i + U(0, 0.8f)) / 9;
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f);
                    DaVun(cham + d * U(4, 12), d * U(200, 400), U(0.45f, 0.75f), U(3f, 5f));
                }
                WExtra(cham, 3, 260);
            });
            At(L + 0.05f, () =>
            {
                Ripple(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.62f * tH, 0.45f, BuiC2);
                for (int i = 0; i < 6; i++)
                    Bui(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, U(-5, 2)), new Vector2(U(-130, 130), -U(15, 60)), U(0.45f, 0.7f), 4, U(10, 15), Back);
            });
            Every(L + 0.04f, L + 0.4f, 18, x =>
                Leaf(foeBody + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.1f, 0.5f) * tH), new Vector2(U(-50, 50), U(20, 80)), U(0.5f, 0.75f), U(4, 6), 220, 1.2f));
            return L;
        }

        // HÚC VƯƠNG MIỆN (đòn thường dạng 1, lao tới): chóp vương miện húc vào đối thủ: chớp nhỏ, dăm đá, lá bật
        public float NVuongHuc(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            At(Mathf.Max(0.02f, L - 0.18f), () =>
            {
                for (int i = 0; i < 4; i++)
                    Bui(casterFeet + new Vector2(U(-10, 10), U(-4, 2)), new Vector2(-dir * U(80, 200), -U(20, 70)), U(0.3f, 0.5f), 3, U(7, 10), Back);
            });
            At(L, () =>
            {
                Shake?.Invoke(0.3f);
                var cham = foeBody + new Vector2(-dir * 0.14f * tH, -0.05f * tH);
                BurstFlash(cham, 0.38f * tH);
                for (int i = 0; i < 6; i++)
                {
                    float a = -dir * 1.1f + (i - 2.5f) * 0.35f + U(-0.1f, 0.1f); // bật ngược về phía tướng, toả hình quạt
                    var d = new Vector2(Mathf.Sin(a), -Mathf.Cos(a));
                    if ((i & 1) == 0) DaVun(cham + d * U(4, 10), d * U(180, 320), U(0.4f, 0.65f), U(2.8f, 4.4f));
                    else Leaf(cham + d * U(4, 10), d * U(160, 300), U(0.4f, 0.6f), U(3.5f, 5.5f), 500, 1.8f);
                }
                WExtra(cham, 2, 220);
            });
            return L;
        }

        // RỄ TRÓI ĐẤT (chiêu mana, cả hai dạng; thẻ đánh 3 nhát): cột (dạng 2) / hai nắm tay (dạng 1) nện xuống đất: vòng bụi, đất vụn; rễ
        // trồi nối nhau dọc mặt đất chạy tới đối thủ, rễ sau to hơn; tới nơi rễ lớn trồi quanh nó quấn lại, ba nhịp siết (chớp, lá văng)
        public float NReTroi(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.4f, lead);
            float tCam = Mathf.Max(0.04f, L - 0.35f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var goc = casterFeet + new Vector2(dir * 0.3f * casterH, 0); // chỗ cột / nắm tay nện xuống
            At(tCam, () =>
            {
                Shake?.Invoke(0.4f);
                Ripple(goc + new Vector2(0, 2), 0.1f * casterH, 0.7f * casterH, 0.5f, BuiC2);
                for (int i = 0; i < 10; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(goc + new Vector2(sd * U(4, 30), U(-6, 2)), new Vector2(sd * U(100, 260), -U(15, 70)), U(0.45f, 0.75f), 4, U(10, 15), i < 6 ? Back : Front);
                }
                for (int i = 0; i < 6; i++) DaVun(goc + new Vector2(U(-20, 20), -4), new Vector2(U(-200, 200), -U(220, 420)), U(0.45f, 0.7f), U(2.8f, 4.4f));
            });
            // rễ trồi nối nhau dọc đất tới đối thủ
            const int N = 6;
            float gap = Mathf.Max(0.03f, (L - tCam - 0.06f) / N);
            for (int i0 = 0; i0 < N; i0++)
            {
                int i = i0;
                At(tCam + 0.05f + i * gap, () =>
                {
                    var at = Vector2.Lerp(goc, foeFeet, 0.18f + 0.68f * i / (N - 1f)) + new Vector2(U(-6, 6), U(-3, 3));
                    for (int j = 0; j < 2; j++)
                    {
                        float t = U(-0.45f, 0.45f);
                        Re(at + new Vector2(U(-10, 10), j == 0 ? -1 : 4), new Vector2(Mathf.Sin(t), -Mathf.Cos(t)), (0.22f + 0.05f * i) * tH * U(0.85f, 1.1f), 0.42f,
                            j == 0 ? Back : Front, i + j);
                    }
                    Bui(at, new Vector2(U(-50, 50), -U(20, 50)), U(0.35f, 0.5f), 3, U(8, 12), Back);
                    if ((i & 1) == 0) Shake?.Invoke(0.06f);
                });
            }
            // tới nơi: rễ lớn quấn, ba nhịp siết
            At(L, () =>
            {
                Shake?.Invoke(0.5f);
                ReQuan(foeFeet, tH, 1f, 0.8f);
                Ripple(foeFeet + new Vector2(0, 2), 0.12f * tH, 0.62f * tH, 0.45f, BuiC2);
                for (int i = 0; i < 6; i++)
                    Bui(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, U(-6, 2)), new Vector2(U(-110, 110), -U(15, 55)), 0, 4, 12, Back);
            });
            for (int h = 0; h < 3; h++)
            {
                int hh = h;
                At(L + 0.06f + 0.12f * h, () =>
                {
                    Shake?.Invoke(hh == 0 ? 0.35f : 0.2f);
                    var c = foeBody + new Vector2(U(-0.12f, 0.12f) * tH, (hh - 1) * 0.18f * tH);
                    BurstFlash(c, (hh == 0 ? 0.42f : 0.3f) * tH);
                    for (int j = 0; j < 4; j++)
                    {
                        float a = U(0, 6.28f);
                        var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                        Leaf(c + d * U(4, 10), d * U(150, 280), U(0.4f, 0.6f), U(3.5f, 5.5f), 500, 1.8f);
                    }
                    if (hh == 2) WExtra(c, 4, 260);
                });
            }
            return L;
        }

        // THẦN TRỤ GIÁNG THẾ (chiêu cuối dạng 2; manh < 1: TIỂU TRỤ GIÁNG của dạng 1): gồng: lá xung quanh bị hút xoáy vào lõi pha lê, bụi
        // dưới chân; cột (mảnh của rig) giáng xuống chỗ đối thủ: bóng tối loang dưới chân nó báo trước; cắm: rung màn, chớp màn (dạng 2),
        // vòng bụi lớn, tảng đá rêu văng, dăm đá, bụi lan hai bên; dạng 2 thêm rễ trồi quanh cột, lá rơi lả tả, bụi lúc bắt cột về tay.
        public float NTruGiang(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh = 1)
        {
            float L = Mathf.Max(0.9f, lead);
            bool lon = manh >= 1;
            float tTu = Mathf.Max(0.04f, L - (lon ? 1.02f : 0.88f)), tGiang = Mathf.Max(tTu + 0.1f, L - 0.22f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var loi = casterFeet + new Vector2(dir * 0.04f * casterH, -(lon ? 0.42f : 0.3f) * casterH); // lõi pha lê
            var cam = foeFeet + new Vector2(-dir * (lon ? 0.18f : 0.12f) * tH, 0); // chân cột (hơi lệch về phía trước đối thủ, như rig)
            // gồng: lá bị hút xoáy vào lõi
            Every(tTu, tGiang - 0.04f, x => (lon ? 30 : 20) + 24 * x, x =>
            {
                float a = U(0, 6.28f);
                var from = loi + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.7f) * U(0.55f, 0.95f) * casterH;
                var q = Leaf(from, Vector2.zero, U(0.3f, 0.42f), U(3.5f, 6f), 0, 0, Mathf.Sin(a) < 0 ? Back : Front);
                q.vel = (loi - from) / q.life + new Vector2(-Mathf.Sin(a), Mathf.Cos(a)) * 120;
            });
            At(tTu, () => Ripple(casterFeet + new Vector2(0, 2), 0.12f * casterH, 0.62f * casterH, 0.45f));
            Every(tTu, tGiang, 8, x => Bui(casterFeet + new Vector2(U(-0.45f, 0.45f) * casterH, U(-4, 2)), new Vector2(U(-40, 40), -U(50, 120)), 0, 3, 9, Back));
            // bóng báo trước dưới chân đối thủ
            At(tGiang, () =>
            {
                float R = (lon ? 0.7f : 0.45f) * tH;
                var bong = new P { pos = cam + new Vector2(0, 2), life = L - tGiang + 0.1f, group = Floor, sz = R };
                bong.draw = (q, k, buf) => Put(buf, Floor, 1, S("ell"), C(46, 40, 34), q.pos, 1.4f * q.sz * (0.3f + 0.7f * k), 3, 0, 0.18f + 0.32f * k);
                Add(bong);
            });
            // cột cắm
            At(L, () =>
            {
                Shake?.Invoke(lon ? 1f : 0.55f);
                if (lon) FlashScreen?.Invoke(FlashW);
                Ripple(cam + new Vector2(0, 2), 0.18f * tH, (lon ? 1.3f : 0.8f) * tH, 0.55f, BuiC2);
                RingN(cam + new Vector2(0, 2), 0.36f, 0.1f * tH, (lon ? 0.9f : 0.55f) * tH, BuiC, 0.3f, Floor, 30.6f);
                ThachNo(cam + new Vector2(0, -0.12f * tH), foeFeet, tH, (lon ? 0.3f : 0.18f) * tH, dir);
                for (int i = 0; i < (lon ? 16 : 9); i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(cam + new Vector2(sd * U(8, 0.35f * tH), U(-6, 3)), new Vector2(sd * U(140, 380), -U(10, 70)), U(0.55f, 0.9f), 5, U(12, 20), i < 10 ? Back : Front);
                }
                BurstFlash(foeBody + new Vector2(0, -0.05f * tH), 0.45f * tH);
                WExtra(foeBody, lon ? 7 : 4, 320);
            });
            if (lon)
            {
                At(L + 0.08f, () =>
                {
                    Shake?.Invoke(0.35f);
                    ReQuan(foeFeet, tH, 0.9f, 0.6f);
                });
                Every(L + 0.06f, L + 0.6f, 26, x =>
                    Leaf(foeFeet + new Vector2(U(-0.6f, 0.6f) * tH, -U(0.4f, 1.0f) * tH), new Vector2(U(-50, 50), U(20, 90)), U(0.55f, 0.85f), U(4, 6.5f), 240, 1.2f,
                        U(0, 1) < 0.5f ? Back : Front));
                At(L + 0.98f, () => // bắt cột về tay
                {
                    Shake?.Invoke(0.2f);
                    for (int i = 0; i < 6; i++)
                        Bui(casterFeet + new Vector2(U(-0.3f, 0.3f) * casterH, U(-4, 2)), new Vector2(U(-120, 120), -U(20, 60)), U(0.4f, 0.6f), 4, U(9, 13), Back);
                });
            }
            return L;
        }
    }
}
