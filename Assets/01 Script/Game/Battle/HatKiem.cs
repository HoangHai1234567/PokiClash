// Bộ của VOỌC TƯỚNG (2026-11-12, voọc kiếm sĩ giáp lá, suất tho_hoang đảo Mộc; rig ArtGen/Spine/kiem_si_rig.py, clip kiem_si_clip.py).
// Người dùng: "chiêu cast mana: cúi xuống hold, rút kiếm chém, trong lúc hold có thể move tới đối thủ"; "chiêu cuối: rút ra 2 kiếm rồi
// biến mất cực nhanh, spawn các ảo ảnh chém tướng địch ở nhiều góc, về lại vị trí ban đầu rồi đóng kiếm; khi đóng kiếm tướng địch bị
// chém liên tục từ các vết trước". Ảo ảnh là mảnh của RIG (xương far / ao_*, sân lái tới đúng đối thủ); lớp này lo vệt chém, sẹo
// chém nằm lại trên đối thủ, loạt chém nổ lại lúc tra kiếm, bụi, gió, lá bị cắt.
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes.
// Mốc của clip: cast: cúi lead − 0,73, lướt tới lúc giữ thế tới lead − 0,17, nhát rút kiếm = lead (1,03), nhát bổ thứ hai lead + 0,73.
// skill: rút hai kiếm lead − 2,22, biến mất lead − 1,70, bốn ảo ảnh chém lead − 1,44 / − 1,20 / − 0,96 / − 0,74 (ngang, chéo xuống,
// bổ thẳng, chéo lên), hiện lại lead − 0,50, chuôi chạm miệng vỏ = lead (2,64), sáu vết nổ lại lead + 0,05 … + 0,40.
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color KiemC = C(250, 255, 246); // lõi vệt chém: trắng thép ngả lục

        // chiêu mana mà tướng LƯỚT TỚI đối thủ trong clip cast (rig khai lunge cho cast): sân nắn quãng lướt tới đối thủ (StageView.Place)
        public static bool CastLao(string kind) => kind == "n_kiem_rut";

        // hình lá liễu nhọn hai đầu: hai giọt kim (hat_needle_0, mũi lên) chĩa ngược nhau, bầu chồng lên nhau ở giữa
        void LaLieu(List<Item> buf, int g, float layer, bool muc, Color col, Vector2 tam, Vector2 d, float dai, float day, float alpha)
        {
            if (dai < 3 || day < 0.6f) return;
            float h = dai * 0.5f, hN = h * 1.12f;
            float st = day / (0.24f * hN); // phần hình chiếm ~24 % bề ngang ảnh
            var s = S(muc ? "needles_0" : "needle_0");
            Put(buf, g, layer, s, col, tam + d * (h * 0.5f), hN, st, TipAngle(d), alpha);
            Put(buf, g, layer, s, col, tam - d * (h * 0.5f), hN, st, TipAngle(-d), alpha);
        }

        // VỆT CHÉM: quét dài ra trong 0,05 s (đầu vệt dẫn trước), sáng trắng rồi mảnh dần; seo > 0: hết pha sáng còn lại một SẸO mảnh màu lá
        // nằm trên đối thủ thêm seo giây (chờ loạt chém nổ lại), rồi tắt hẳn
        void DrawVetChem(P q, float k, List<Item> buf)
        {
            float t = k * q.life, sang = q.tb;
            float quet = Mathf.Clamp01(t / 0.05f);
            quet = 1 - (1 - quet) * (1 - quet);
            float dai = q.sz * (0.2f + 0.8f * quet);
            var tam = q.pos - q.aim * (q.sz * 0.5f) + q.aim * (dai * 0.5f);
            float u = Mathf.Clamp01((t - 0.05f) / Mathf.Max(0.02f, sang - 0.05f));
            bool seo = q.life > sang + 0.01f;
            float day, alpha, loi;
            if (t <= sang)
            {
                day = q.wd * (1 - (seo ? 0.74f : 0.8f) * SmoothStep(0.15f, 1, u));
                alpha = seo ? 1 : 1 - SmoothStep(0.55f, 1, u);
                loi = 1 - SmoothStep(0.1f, 0.8f, u);
            }
            else
            {
                float v = (t - sang) / Mathf.Max(0.02f, q.life - sang);
                day = q.wd * (0.26f + 0.05f * Mathf.Sin(q.age * 26 + q.ph)); // sẹo: rung nhẹ như còn âm ỉ
                alpha = 0.92f * (1 - SmoothStep(0.9f, 1, v));
                loi = 0;
            }
            if (alpha < 0.03f) return;
            var w = q.stops ?? W;
            LaLieu(buf, q.group, 46, true, Ink, tam, q.aim, dai + 6, day + 5, alpha);
            LaLieu(buf, q.group, 46.3f, false, Color.Lerp(w[3], w[2], seo && t > sang ? 0.35f : 0), tam, q.aim, dai, day, alpha);
            if (loi > 0.05f) LaLieu(buf, q.group, 46.6f, false, KiemC, tam, q.aim, dai * 0.86f, day * 0.5f * loi + 0.6f, alpha);
        }

        P VetChem(Vector2 c, Vector2 d, float dai, float day, float sang = 0.2f, float seo = 0, int group = Front)
        {
            var p = new P { pos = c, aim = Unit(d), life = sang + seo, tb = sang, sz = dai, wd = day, group = group, stops = W, ph = U(0, 6.28f) };
            p.draw = DrawVetChem;
            return Add(p);
        }

        // vệt kiếm vung: một cung tròn mảnh (hat_arc_0, cung dài ~150 độ) quay bụng về hướng d, nở nhẹ rồi tan
        void CungKiem(Vector2 c, Vector2 d, float R, float life = 0.16f, int group = Front)
        {
            var p = new P { pos = c, aim = Unit(d), life = life, sz = R, group = group, stops = W };
            p.draw = (q, k, buf) =>
            {
                float a = 1 - SmoothStep(0.35f, 1, k);
                if (a < 0.04f) return;
                float r = q.sz * (0.86f + 0.2f * EaseOut(k));
                float ang = VelAng(q.aim) - 284.7f; // giữa cung của ảnh nằm ở góc 284,7 độ
                Put(buf, q.group, 45, S("arcs_0"), Ink, q.pos, 2 * r, 1, ang, a);
                Put(buf, q.group, 45.4f, S("arc_0"), Color.Lerp(KiemC, q.stops[3], k), q.pos, 2 * r, 1, ang, a);
            };
            Add(p);
        }

        // thứ văng ra ở một nhát chém: chớp toé nhỏ ở giữa vệt, tia vụn bắn dọc hai đầu vệt, lá bị cắt bay theo hướng chém
        void ChemToe(Vector2 c, Vector2 d, float tH, float manh, int la)
        {
            d = Unit(d);
            var n = new Vector2(-d.y, d.x);
            BurstFlash(c, 0.3f * tH * manh);
            for (int i = 0; i < 6; i++)
            {
                float sd = (i & 1) == 0 ? 1 : -1;
                var q = Spark(c + d * sd * U(0.1f, 0.4f) * tH * manh, d * sd + n * U(-0.35f, 0.35f), U(300, 520) * manh, U(0.16f, 0.26f), U(6, 9), 0, Front, 4);
                q.col = (i % 3) == 0 ? W[3] : KiemC;
            }
            for (int i = 0; i < la; i++)
            {
                var v = d * U(120, 320) + n * U(-170, 170) + new Vector2(0, -U(20, 120));
                Leaf(c + d * U(-0.3f, 0.3f) * tH + n * U(-6, 6), v * manh, U(0.4f, 0.7f), U(3.5f, 6f), 560, 1.8f, (i & 1) == 0 ? Front : Back);
            }
        }

        // BẠT KIẾM (chiêu mana): cúi giữ thế: vòng bụi dưới chân; lướt tới: bụi và sợi gió tuột lại sau lưng, lá bị cuốn theo; nhát rút kiếm:
        // cung kiếm quét qua đối thủ, vệt chém chéo lên, lá bị cắt; nhát bổ thứ hai: vệt chéo xuống bắt chéo vệt đầu.
        public float NKiemRut(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.4f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var toi = Vector2.Lerp(casterFeet, foeFeet, 0.72f); // sân kéo đỉnh cú lướt tới 72 % quãng tới đối thủ (AolaSticker.Lunge)
            var hg = Unit(toi - casterFeet);
            float t0 = Mathf.Max(0.02f, L - 0.70f), t1 = Mathf.Max(t0 + 0.05f, L - 0.17f);
            At(Mathf.Max(0.01f, L - 0.73f), () => Ripple(casterFeet + new Vector2(0, 2), 0.08f * casterH, 0.42f * casterH, 0.4f, BuiC2));
            float goc = T;
            Every(t0, t1, 46, x =>
            {
                float k = Mathf.Clamp01((T - goc - t0) / (t1 - t0));
                var chan = Vector2.Lerp(casterFeet, toi, k * k * (3 - 2 * k));
                float r = U(0, 1);
                if (r < 0.4f) Bui(chan + new Vector2(-dir * U(0, 0.25f) * casterH, U(-5, 2)), -hg * U(60, 180) + new Vector2(0, -U(10, 60)), U(0.3f, 0.5f), 3.5f, U(8, 13), Back);
                else if (r < 0.75f) SoiGio(chan + new Vector2(-dir * U(0.1f, 0.5f) * casterH, -U(0.15f, 0.6f) * casterH), -hg * U(180, 340), U(0.2f, 0.3f), U(7, 11), Back);
                else Leaf(chan + new Vector2(-dir * U(0, 0.4f) * casterH, -U(0.05f, 0.5f) * casterH), -hg * U(80, 200) + new Vector2(0, -U(30, 110)), U(0.35f, 0.55f), U(3.5f, 5.5f), 360, 1.4f, Back);
            });
            var d1 = Unit(new Vector2(dir * 0.82f, -0.57f)); // nhát rút kiếm: chéo lên về phía sau đối thủ
            var d2 = Unit(new Vector2(dir * 0.78f, 0.62f));  // nhát bổ: chéo xuống
            var tam = foeBody + new Vector2(-dir * 0.06f * tH, 0);
            At(Mathf.Max(0.02f, L - 0.03f), () => CungKiem(Vector2.Lerp(toi + new Vector2(0, -0.45f * casterH), foeBody, 0.45f), d1, 0.62f * Mathf.Max(casterH, tH)));
            At(L, () =>
            {
                Shake?.Invoke(0.5f);
                VetChem(tam, d1, 1.3f * tH, 0.13f * tH, 0.24f);
                ChemToe(tam, d1, tH, 1, 8);
                WExtra(tam, 3, 260);
                Ripple(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.5f * tH);
            });
            At(L + 0.70f, () => CungKiem(Vector2.Lerp(toi + new Vector2(0, -0.6f * casterH), foeBody, 0.5f), d2, 0.6f * Mathf.Max(casterH, tH)));
            At(L + 0.73f, () =>
            {
                Shake?.Invoke(0.4f);
                VetChem(tam, d2, 1.2f * tH, 0.12f * tH, 0.24f);
                ChemToe(tam, d2, tH, 0.9f, 6);
                WExtra(tam, 2, 220);
            });
            return L;
        }

        // hướng bốn nhát của bốn ảo ảnh (x theo phía trước mặt tướng, y xuống), cùng thứ tự với rig (AO trong kiem_si_clip.py), và hai nhát
        // thêm của loạt nổ lại; chỗ tâm vết lệch so với thân đối thủ (theo chiều cao đối thủ)
        static readonly Vector2[] AoHuong = { new Vector2(1, 0), new Vector2(0.73f, 0.69f), new Vector2(0.04f, 1), new Vector2(0.76f, -0.64f), new Vector2(0.9f, 0.42f), new Vector2(0.5f, -0.86f) };
        static readonly Vector2[] AoTam = { new Vector2(0, -0.08f), new Vector2(0.03f, 0.02f), new Vector2(-0.02f, -0.02f), new Vector2(-0.03f, 0.05f), new Vector2(0.02f, -0.16f), new Vector2(0, 0.1f) };
        static readonly float[] AoGio = { 1.44f, 1.20f, 0.96f, 0.74f }; // giây trước lead

        // ẢO ẢNH LOẠN TRẢM (chiêu cuối): rút kiếm: lóe ở tay; biến mất: bụi, lá, sợi gió vút về phía đối thủ; mỗi ảo ảnh chém: vệt chém +
        // SẸO nằm lại trên đối thủ; hiện lại: bụi dưới chân; chuôi chạm miệng vỏ: vòng nhỏ ở hông, rồi các sẹo NỔ LẠI lần lượt thành vệt
        // chém to hơn (thêm hai nhát), lá bị cắt văng, cuối cùng chùm lá vỡ.
        public float NKiemAo(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(1.6f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var hong = casterFeet + new Vector2(dir * 0.1f * casterH, -0.42f * casterH);
            var hg = Unit(foeBody - hong);
            var ng = new Vector2(-hg.y, hg.x);
            Vector2 Huong(int i) => Unit(new Vector2(dir * AoHuong[i].x, AoHuong[i].y));
            Vector2 Tam(int i) => foeBody + new Vector2(dir * AoTam[i].x, AoTam[i].y) * tH;
            const float No0 = 0.05f, NoBuoc = 0.07f;

            // rút hai kiếm: lóe nhỏ ở tay, lá dưới chân bật lên
            At(Mathf.Max(0.02f, L - 2.22f), () =>
            {
                BurstFlash(hong + new Vector2(dir * 0.12f * casterH, -0.1f * casterH), 0.22f * casterH);
                for (int i = 0; i < 5; i++)
                    Leaf(casterFeet + new Vector2(U(-0.35f, 0.35f) * casterH, -U(0, 0.1f) * casterH), new Vector2(U(-60, 60), -U(140, 260)), U(0.35f, 0.5f), U(3.5f, 5.5f), 300, 1.4f, Back);
            });
            // biến mất: bụi bật dưới chân, sợi gió và lá vút theo về phía đối thủ
            float tBien = Mathf.Max(0.04f, L - 1.70f);
            At(tBien, () =>
            {
                Shake?.Invoke(0.2f);
                Ripple(casterFeet + new Vector2(0, 2), 0.1f * casterH, 0.6f * casterH, 0.4f, BuiC2);
                for (int i = 0; i < 8; i++)
                    Bui(casterFeet + new Vector2(U(-0.25f, 0.25f) * casterH, U(-6, 2)), new Vector2(-dir * U(60, 240), -U(10, 80)), U(0.4f, 0.65f), 4, U(10, 16), Back);
            });
            Every(tBien - 0.04f, tBien + 0.2f, 70, x =>
            {
                var at = hong + hg * U(0, 0.5f) * casterH + ng * U(-0.4f, 0.4f) * casterH;
                if (U(0, 1) < 0.65f) SoiGio(at, hg * U(700, 1100), U(0.18f, 0.28f), U(8, 13), U(0, 1) < 0.5f ? Back : Front);
                else Leaf(at, hg * U(380, 620) + ng * U(-60, 60), U(0.3f, 0.45f), U(3.5f, 5.5f), 120, 1.6f, Back);
            });
            // bốn ảo ảnh chém: vệt + sẹo nằm lại tới lúc nổ
            for (int i = 0; i < 4; i++)
            {
                int ii = i;
                float tc = L - AoGio[i];
                if (tc < 0.05f) continue;
                At(tc, () =>
                {
                    Shake?.Invoke(0.28f);
                    var c = Tam(ii);
                    var d = Huong(ii);
                    VetChem(c, d, 1.15f * tH, 0.1f * tH, 0.2f, L + No0 + ii * NoBuoc - tc - 0.2f);
                    ChemToe(c, d, tH, 0.75f, 3);
                    for (int j = 0; j < 4; j++) // gió của cú lướt xuyên qua
                        SoiGio(c + d * U(-0.5f, 0.3f) * tH + new Vector2(-d.y, d.x) * U(-0.25f, 0.25f) * tH, d * U(520, 820), U(0.16f, 0.24f), U(7, 11), Back);
                });
            }
            // hiện lại ở chỗ cũ
            At(Mathf.Max(0.08f, L - 0.50f), () =>
            {
                Ripple(casterFeet + new Vector2(0, 2), 0.08f * casterH, 0.5f * casterH, 0.4f, BuiC2);
                for (int i = 0; i < 6; i++)
                    Bui(casterFeet + new Vector2(U(-0.2f, 0.2f) * casterH, U(-6, 2)), new Vector2(dir * U(40, 200), -U(10, 60)), U(0.35f, 0.6f), 3.5f, U(9, 14), Back);
                for (int i = 0; i < 4; i++)
                    Leaf(hong + U2(-0.3f, 0.3f) * casterH, new Vector2(dir * U(40, 160), -U(40, 140)), U(0.4f, 0.6f), U(3.5f, 5.5f), 420, 1.6f, Back);
            });
            // chuôi chạm miệng vỏ
            At(L, () =>
            {
                Shake?.Invoke(0.25f);
                RingN(hong, 0.24f, 0.05f * casterH, 0.3f * casterH, W[3], 1, Front, 32);
                BurstFlash(hong, 0.16f * casterH);
            });
            // các vết nổ lại lần lượt
            for (int j = 0; j < 6; j++)
            {
                int jj = j;
                At(L + No0 + j * NoBuoc, () =>
                {
                    Shake?.Invoke(jj == 5 ? 0.85f : 0.4f);
                    var c = Tam(jj);
                    var d = Huong(jj);
                    VetChem(c, d, 1.5f * tH, 0.16f * tH, 0.22f);
                    ChemToe(c, d, tH, 1.05f, 4);
                    if ((jj & 1) == 0) WExtra(c, 2, 260);
                });
            }
            // chốt: chùm lá vỡ, vòng, bụi dưới chân đối thủ
            float tChot = L + No0 + 6 * NoBuoc;
            At(tChot, () =>
            {
                LaNo(foeBody, foeFeet, tH, 1.25f);
                RingN(foeBody, 0.3f, 0.12f * tH, 0.75f * tH, W[3], 1, Front, 32);
                WExtra(foeBody, 8, 340);
                for (int i = 0; i < 10; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(foeFeet + new Vector2(sd * U(6, 0.28f * tH), U(-6, 3)), new Vector2(sd * U(120, 320), -U(10, 60)), U(0.5f, 0.8f), 5, U(11, 18), Back);
                }
            });
            Every(tChot, tChot + 0.45f, 22, x =>
                Leaf(foeBody + new Vector2(U(-0.5f, 0.5f) * tH, -U(0, 0.5f) * tH), new Vector2(U(-50, 50), U(20, 90)), U(0.5f, 0.8f), U(3.5f, 6f), 240, 1.2f, U(0, 1) < 0.5f ? Front : Back));
            return L + No0; // sát thương hiện ở vết nổ đầu tiên
        }
    }
}
