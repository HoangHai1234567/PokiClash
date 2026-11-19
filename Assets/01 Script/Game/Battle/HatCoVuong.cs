// Bộ của CỔ VƯƠNG (2026-11-17, tượng vua cổ rễ quấn cầm cột đá, tướng 6 đảo THỔ, suất hat_de ải 30; rig ArtGen/Spine/tuong_cot_rig.py
// (dạng 2, rig monster_3608) và tuong_cot_non_rig.py (dạng 1 Cổ Vương Nhi, rig monster_3273); bản xem trước tuong_cot_fx.py).
// 2026-11-17 bị ghép nhầm vào suất gio_loc đảo Mộc (đè Linh Điểu); 2026-11-19 chuyển về hat_de (ArtGen/Spine/quai/doi_suat6_tho.py), thẻ
// giữ hiệu ứng của suất hat_de (chiêu mana 2 nhát, chiêu cuối 3 nhát). Hệ Thổ nhưng chiêu vẫn gọi MocSang (bảng MocTuoi có "hat_de").
// Cột đá (cả cột tung lên trời, cột khổng lồ giáng xuống và bay về, cột nhỏ của dạng 1) là mảnh của RIG trên xương fly_cot → cot_bay
// (AolaActor.FarAtomik lái tới đối thủ thật); lớp này lo rễ, bụi, đá vỡ, lá, bóng báo trước.
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lá lấy từ WThemes.
// Mốc của clip:
//   dạng 2  attack: đập cột = lead (0,50) · cast: cột cắm đất lead − 0,36, rễ tới đối thủ = lead (1,12) · skill: tung cột lead − 1,08,
//           gồng lead − 1,02, cột bắt đầu giáng lead − 0,22, cắm = lead (1,64), rễ trồi lead + 0,08, bắt cột lead + 0,98
//   dạng 1  attack: húc = lead (0,46) · cast: nện tay lead − 0,33, rễ tới = lead (0,95) · skill: gồng gọi lead − 0,88, cột nhỏ bắt
//           đầu rơi lead − 0,23, cắm = lead (1,18)
// Nâng 2026-11-18 (người dùng: "khói rải rác chưa thành cụm, chưa mềm", "nổ chưa đẹp", "màu tươi hơn"): bụi thành cụm tách dần (BuiCum), vòng
// cung dẹt đứt đoạn (CungDat), vết đất giữ ~1 s (VetDat), chớp nổ nhỏ ở trước + toé sau thân (không che mặt), vệt hút xoắn vào lõi.
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
// KHUNG VẼ SẴN (2026-11-19, HatFlip.cs + HatFbTho.cs; chưa nhập ảnh hat_fb_* thì hạt cũ): mọi cụm bụi (BuiCum) là cụm khói vẽ sẵn nhuộm bụi đất,
// ít cụm mà to (CvBui); đá vỡ to dùng bản riêng CvDaNo (như ThachNo của HatChim.cs nhưng bụi là khung vẽ sẵn). Giữ: rễ (Re / ReQuan: khung gai
// lá là lá xanh, không phải rễ gỗ), lá, tảng đá rêu, dăm, chớp, vòng cung đất, vết đất, bóng báo trước, mọi mốc và DanhTrung.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // khung vẽ sẵn (2026-11-19): một cụm bụi (BuiCum bán kính r) → cụm khói vẽ sẵn nhuộm bụi đất cao 2,8 r × to, chân ở pos (sát đất);
        // chưa có khung thì BuiCum cũ
        void CvBui(Vector2 pos, Vector2 vel, float r, int group = Back, bool tach = true, float to = 1)
        {
            if (!HasFb("khoi"))
            {
                BuiCum(pos, vel, r, 0, group, null, tach);
                return;
            }
            float h = 2.8f * r * to;
            FbBui(pos + new Vector2(0, 0.06f * h), vel * 0.5f, h, group, FbBuiC, 1.4f);
        }

        // số cụm bụi: có khung vẽ sẵn thì ít hơn (cụm to hơn × 1,2 bù lại)
        int CvSo(int cu) => HasFb("khoi") ? Mathf.Max(1, Mathf.RoundToInt(cu * 0.67f)) : cu;

        // đá vỡ to (bản của Cổ Vương, như ThachNo ở HatChim.cs): chớp nhỏ ở trước + toé sau thân, tảng con văng rồi nảy, dăm đá; bụi là MỘT cụm
        // khói vẽ sẵn to sau thân (khung vẽ sẵn 2026-11-19). Chưa có khung thì gọi ThachNo cũ
        void CvDaNo(Vector2 c, Vector2 foeFeet, float tH, float R, float dir)
        {
            if (!HasFb("khoi"))
            {
                ThachNo(c, foeFeet, tH, R, dir);
                return;
            }
            Chop(c, 0.4f * tH, 0.08f);
            BurstFlash(c, 0.7f * tH, Back, 0.16f);
            for (int i = 0; i < 7; i++)
            {
                float a = (-90 + (i - 3) * 34 + U(-10, 10)) * Mathf.Deg2Rad; // nửa trên, rải đều
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                Thach(c + d * U(4, 0.4f * R), new Vector2(d.x * U(200, 420) + dir * 60, d.y * U(260, 520)), U(1.0f, 1.4f), R * U(0.22f, 0.4f), foeFeet.y + U(-10, 18),
                    (i & 1) == 0 ? Front : Back, (i % 3) == 0);
            }
            for (int i = 0; i < 12; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / 12;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f);
                DaVun(c + d * U(4, 14), d * U(220, 460), U(0.45f, 0.8f), U(3.2f, 5.6f));
            }
            float h = 0.5f * tH;
            FbBui(new Vector2(c.x, Mathf.Min(foeFeet.y, c.y + 0.1f * h)), new Vector2(U(-30, 30), -40), h, Back, FbBuiC, 1.25f, 0.92f, 2);
        }

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
            MocSang();
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            At(Mathf.Max(0.02f, L - 0.3f), () =>
            {
                for (int i = 0; i < 2; i++)                                     // khung vẽ sẵn (2026-11-19): CvBui
                    CvBui(casterFeet + new Vector2(U(-14, 14), U(-4, 2)), new Vector2(-dir * U(60, 160), -U(20, 50)), U(0.07f, 0.1f) * casterH, Back);
            });
            At(L, () =>
            {
                Shake?.Invoke(0.6f);
                var cham = foeBody + new Vector2(-dir * 0.05f * tH, -0.32f * tH); // đầu đối thủ, nơi đầu cột đập xuống
                DanhTrung?.Invoke(cham, 0.8f);
                Chop(cham, 0.36f * tH, 0.07f);
                BurstFlash(cham, 0.5f * tH, Back, 0.16f);
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
                CungDat(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.66f * tH, 0.45f, CungC, 0.08f * tH);
                VetDat(foeFeet + new Vector2(0, 3), 0.42f * tH, 0.9f);
                for (int i = 0, nb = CvSo(3); i < nb; i++)                      // khung vẽ sẵn (2026-11-19): hai cụm vẽ sẵn to hơn thay ba cụm hạt
                {
                    float sd = i == 2 ? 0 : i == 0 ? -1 : 1;
                    CvBui(foeFeet + new Vector2(sd * U(0.12f, 0.34f) * tH, U(-5, 2)), new Vector2(sd * U(70, 150), -U(15, 45)), U(0.1f, 0.14f) * tH, Back, true, 1.2f);
                }
            });
            Every(L + 0.04f, L + 0.4f, 16, x =>
                LaRoi(foeBody + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.1f, 0.5f) * tH), new Vector2(U(-50, 50), U(10, 50)), U(0.55f, 0.8f), U(3.4f, 5.2f)));
            return L;
        }

        // HÚC VƯƠNG MIỆN (đòn thường dạng 1, lao tới): chóp vương miện húc vào đối thủ: chớp nhỏ, dăm đá, lá bật
        public float NVuongHuc(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            At(Mathf.Max(0.02f, L - 0.18f), () =>
            {
                for (int i = 0; i < 2; i++)                                     // khung vẽ sẵn (2026-11-19): CvBui
                    CvBui(casterFeet + new Vector2(U(-10, 10), U(-4, 2)), new Vector2(-dir * U(80, 180), -U(20, 50)), U(0.06f, 0.09f) * casterH, Back);
            });
            At(L, () =>
            {
                Shake?.Invoke(0.3f);
                var cham = foeBody + new Vector2(-dir * 0.14f * tH, -0.05f * tH);
                DanhTrung?.Invoke(cham, 0.5f);
                Chop(cham, 0.3f * tH, 0.07f);
                BurstFlash(cham, 0.36f * tH, Back, 0.14f);
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

        // RỄ TRÓI ĐẤT (chiêu mana, cả hai dạng; ba nhịp siết dựng cho thẻ 3 nhát của suất cũ, thẻ hat_de đánh 2 nhát): cột (dạng 2) / hai nắm tay (dạng 1) nện xuống đất: vòng bụi, đất vụn; rễ
        // trồi nối nhau dọc mặt đất chạy tới đối thủ, rễ sau to hơn; tới nơi rễ lớn trồi quanh nó quấn lại, ba nhịp siết (chớp, lá văng)
        public float NReTroi(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.4f, lead);
            float tCam = Mathf.Max(0.04f, L - 0.35f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var goc = casterFeet + new Vector2(dir * 0.3f * casterH, 0); // chỗ cột / nắm tay nện xuống
            At(tCam, () =>
            {
                Shake?.Invoke(0.4f);
                CungDat(goc + new Vector2(0, 2), 0.1f * casterH, 0.75f * casterH, 0.45f, CungC, 0.08f * casterH);
                VetDat(goc + new Vector2(0, 3), 0.4f * casterH, 0.9f);
                for (int i = 0, nb = CvSo(4); i < nb; i++)                      // khung vẽ sẵn (2026-11-19): ba cụm vẽ sẵn to hơn thay bốn cụm hạt
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    CvBui(goc + new Vector2(sd * U(0.05f, 0.25f) * casterH, U(-6, 2)), new Vector2(sd * U(90, 200), -U(15, 45)), U(0.1f, 0.13f) * casterH,
                        i < 3 ? Back : Front, true, 1.2f);
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
                    if (!HasFb("khoi") || (i & 1) == 0)                          // khung vẽ sẵn (2026-11-19): cụm vẽ sẵn ở nhịp chẵn, to × 1,3
                        CvBui(at, new Vector2(U(-50, 50), -U(20, 40)), U(0.06f, 0.08f) * tH, Back, (i & 1) == 0, 1.3f);
                    if ((i & 1) == 0) Shake?.Invoke(0.06f);
                });
            }
            // tới nơi: rễ lớn quấn, ba nhịp siết
            At(L, () =>
            {
                Shake?.Invoke(0.5f);
                DanhTrung?.Invoke(foeBody, 0.6f);
                ReQuan(foeFeet, tH, 1f, 0.8f);
                CungDat(foeFeet + new Vector2(0, 2), 0.12f * tH, 0.66f * tH, 0.45f, W[2], 0.07f * tH);
                VetDat(foeFeet + new Vector2(0, 3), 0.42f * tH, 1f);
                for (int i = 0, nb = CvSo(3); i < nb; i++)                      // khung vẽ sẵn (2026-11-19): hai cụm vẽ sẵn to hơn thay ba cụm hạt
                {
                    float sd = i == 2 ? 0 : i == 0 ? -1 : 1;
                    CvBui(foeFeet + new Vector2(sd * U(0.12f, 0.36f) * tH, U(-6, 2)), new Vector2(sd * U(60, 130), -U(15, 40)), U(0.1f, 0.13f) * tH, Back, true, 1.2f);
                }
            });
            for (int h = 0; h < 3; h++)
            {
                int hh = h;
                At(L + 0.06f + 0.12f * h, () =>
                {
                    Shake?.Invoke(hh == 0 ? 0.35f : 0.2f);
                    var c = foeBody + new Vector2(U(-0.12f, 0.12f) * tH, (hh - 1) * 0.18f * tH);
                    DanhTrung?.Invoke(c, hh == 0 ? 0.5f : 0.3f);
                    Chop(c, (hh == 0 ? 0.3f : 0.22f) * tH, 0.06f);
                    BurstFlash(c, (hh == 0 ? 0.42f : 0.3f) * tH, Back, 0.14f);
                    for (int j = 0; j < 4; j++)
                    {
                        float a = U(0, 6.28f);
                        var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                        Leaf(c + d * U(4, 10), d * U(150, 280), U(0.4f, 0.6f), U(3.2f, 5f), 500, 1.8f);
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
            MocSang();
            float L = Mathf.Max(0.9f, lead);
            bool lon = manh >= 1;
            float tTu = Mathf.Max(0.04f, L - (lon ? 1.02f : 0.88f)), tGiang = Mathf.Max(tTu + 0.1f, L - 0.22f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var loi = casterFeet + new Vector2(dir * 0.04f * casterH, -(lon ? 0.42f : 0.3f) * casterH); // lõi pha lê
            var cam = foeFeet + new Vector2(-dir * (lon ? 0.18f : 0.12f) * tH, 0); // chân cột (hơi lệch về phía trước đối thủ, như rig)
            // gồng: lá và vệt gió bị hút xoắn vào lõi, nhanh dần, nhập vào lõi; mật độ tăng dần
            At(tTu, () => GatherLa(t => loi, 0, tGiang - tTu - 0.04f, 0.9f * casterH, lon ? 40 : 28));
            At(tTu, () => CungDat(casterFeet + new Vector2(0, 2), 0.12f * casterH, 0.66f * casterH, 0.45f, W[2], 0.06f * casterH));
            Every(tTu, tGiang, 4, x =>                                          // khung vẽ sẵn (2026-11-19): CvBui
                CvBui(casterFeet + new Vector2(U(-0.45f, 0.45f) * casterH, U(-4, 2)), new Vector2(U(-40, 40), -U(50, 100)), U(0.06f, 0.08f) * casterH, Back));
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
                DanhTrung?.Invoke(foeBody, lon ? 1 : 0.6f);
                CungDat(cam + new Vector2(0, 2), 0.18f * tH, (lon ? 1.35f : 0.85f) * tH, 0.55f, CungC, (lon ? 0.13f : 0.09f) * tH);
                CungDat(cam + new Vector2(0, 2), 0.1f * tH, (lon ? 0.9f : 0.55f) * tH, 0.45f, W[2], (lon ? 0.08f : 0.06f) * tH, 5);
                VetDat(cam + new Vector2(0, 3), (lon ? 0.7f : 0.45f) * tH, 1.1f);
                CvDaNo(cam + new Vector2(0, -0.12f * tH), foeFeet, tH, (lon ? 0.3f : 0.18f) * tH, dir);   // khung vẽ sẵn (2026-11-19): bản bụi vẽ sẵn
                for (int i = 0, nb = CvSo(lon ? 6 : 4); i < nb; i++)            // khung vẽ sẵn: bốn / ba cụm vẽ sẵn to hơn thay sáu / bốn cụm hạt
                {
                    float sd = i == 5 ? 0 : (i & 1) == 0 ? 1 : -1;
                    CvBui(cam + new Vector2(sd * U(0.1f, 0.42f) * tH, U(-6, 3)), new Vector2(sd * U(110, 260), -U(10, 45)), U(0.12f, 0.17f) * tH * (lon ? 1 : 0.8f),
                        i < 4 ? Back : Front, true, 1.2f);
                }
                Chop(foeBody + new Vector2(0, -0.05f * tH), 0.36f * tH, 0.07f);
                WExtra(foeBody, lon ? 6 : 3, 320);
            });
            if (lon)
            {
                At(L + 0.08f, () =>
                {
                    Shake?.Invoke(0.35f);
                    ReQuan(foeFeet, tH, 0.9f, 0.6f);
                });
                Every(L + 0.06f, L + 0.6f, 22, x =>
                    LaRoi(foeFeet + new Vector2(U(-0.6f, 0.6f) * tH, -U(0.4f, 1.0f) * tH), new Vector2(U(-50, 50), U(10, 50)), U(0.6f, 0.9f), U(3.6f, 5.6f),
                        U(0, 1) < 0.5f ? Back : Front));
                At(L + 0.98f, () => // bắt cột về tay
                {
                    Shake?.Invoke(0.2f);
                    for (int i = 0, nb = CvSo(3); i < nb; i++)                  // khung vẽ sẵn (2026-11-19): hai cụm vẽ sẵn to hơn thay ba cụm hạt
                    {
                        float sd = i == 2 ? 0 : i == 0 ? -1 : 1;
                        CvBui(casterFeet + new Vector2(sd * U(0.1f, 0.3f) * casterH, U(-4, 2)), new Vector2(sd * U(60, 140), -U(20, 45)), U(0.08f, 0.11f) * casterH, Back,
                            true, 1.2f);
                    }
                });
            }
            return L;
        }
    }
}
