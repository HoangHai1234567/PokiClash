// BỘ NƯỚC THEO GÓI MẪU (bản 3, người dùng 2026-11-25: "làm lại vfx nước của game theo asset này, thêm texture vẽ tay nhẹ nhàng của mình
// vào, quét thật kĩ và lấy cái nào phù hợp, nó có gì mình cũng phải có như vậy"; "đặc biệt là tia nước ở water laser rất đẹp"; texture
// "dùng thẳng nhưng nên thay đổi đi chút"). Gói: SrRubfish "Water - Assets for VFX 02" + NamuFX "Stylized Water Effect Pack" (đã mổ từng
// prefab: ArtGen/XemVfx/vfx_goi/PHAN_TICH.md, ảnh động xem.html). Flipbook của gói đóng vào atlas giá trị + alpha (ArtGen/Spine/nuoc_goi/
// dong_goi.py → nuoc_fb.png, bảng NuocFbBang.cs), shader UIWaterFx chế độ 6 tô lại bằng dải cel lam nhạt / bọt trắng + vân chì của game,
// chế độ 7 là ống tia nhiều lớp. Giữ dáng + nhịp + cách ghép lớp của gói; hợp đồng giờ / điểm rig / bề dày của từng tướng giữ nguyên.
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        readonly System.Collections.Generic.List<Vector2> nUi = new System.Collections.Generic.List<Vector2>(128);
        readonly System.Collections.Generic.List<float> nW = new System.Collections.Generic.List<float>(128);
        static readonly Vector2 Len = new Vector2(0, -1); // hướng lên trên sân (y xuống)

        // ================= vẽ flipbook =================
        // tâm c (sân), cỡ w × h (sân; h ≤ 0 → theo tỉ lệ khung gốc), angUi: độ UI (y lên; NAng(hướng sân))
        void NFbS(int g, float layer, Vector2 c, float w, float h, float angUi, NFb fb, float frame, float cut, float a, float seed, float lift = 0,
            int kind = 0, bool flip = false, int pal = 0)
        {
            var f = nfx[g];
            if (!f || w < 0.5f || a <= 0.003f) return;
            f.Fb(layer, StageView.P(c), w * NK, h > 0 ? h * NK : 0, angUi, fb, frame, cut, NA(a), T, seed, lift, kind, flip, pal);
        }

        // phát trọn một flipbook theo đời hạt (khung 0 → cuối, như UV module "frameOverTime 0→1" của gói); cỡ w0 → w1 (EaseOut), tỉ lệ cao /
        // rộng hk (0: theo khung gốc), xoay angUi + spin·tuổi; vật lý theo vel / grav / drag; at: hàm vị trí bám (null: theo vật lý)
        P NFbPhat(int g, float layer, Vector2 pos, Vector2 vel, float life, NFb fb, float w0, float w1, float angUi, float cut, float lift = 0,
            int kind = 0, bool flip = false, float grav = 0, float drag = 0, float spin = 0, float hk = 0, Func<float, Vector2> at = null,
            float fade0 = 0.8f, int pal = 0)
        {
            var d = NuocFbBang.Get(fb);
            float sd = NSeed();
            var p = new P { pos = at != null ? at(0) : pos, vel = vel, acc = new Vector2(0, grav), drag = drag, life = Mathf.Max(0.04f, life), group = g };
            p.draw = (q, k, buf) =>
            {
                if (at != null) q.pos = at(q.age);
                float w = Mathf.Lerp(w0, w1, EaseOut(k));
                float a = k < fade0 ? 1 : 1 - (k - fade0) / Mathf.Max(0.01f, 1 - fade0);
                NFbS(q.group, layer + k * 0.01f, q.pos, w, hk > 0 ? w * hk : 0, angUi + spin * q.age, fb, k * (d.frames - 1), cut, a, sd, lift, kind, flip,
                    pal);
            };
            return Add(p);
        }

        // ống tia: nPts / nHw (sân) đã điền → đổi UI một lần; Tube nhiều lớp dùng chung (wk: nhân bề rộng)
        void NTubePrep()
        {
            nUi.Clear();
            for (int i = 0; i < nPts.Count; i++) nUi.Add(StageView.P(nPts[i]));
        }

        void NTube(int g, float layer, int kind, float wk, float scroll, float cut, float seed, float a = 1, int pal = 0)
        {
            var f = nfx[g];
            if (!f || nUi.Count < 2) return;
            nW.Clear();
            for (int i = 0; i < nHw.Count; i++) nW.Add(nHw[i] * NK * wk);
            f.Tube(layer, nUi, nW, NA(a), kind, scroll, cut, T, seed, SangXY, pal);
        }

        // nhịp "thở" bề dày tia của gói (Size over lifetime của LaserCore / LaserNoise, hạt sinh lại mỗi 1 s): 0,6 → 1 → 0,85 → 0,91 → 0,76
        // → 0,90 → 0,79 → 0,6; ở đây kéo về 0,8–1 cho tia không thắt quá
        static readonly float[] ThoT = { 0, 0.11f, 0.26f, 0.41f, 0.59f, 0.71f, 0.83f, 1 };
        static readonly float[] ThoV = { 0.6f, 1, 0.85f, 0.91f, 0.76f, 0.9f, 0.79f, 0.6f };

        static float Tho(float t)
        {
            t -= Mathf.Floor(t);
            for (int i = 1; i < ThoT.Length; i++)
                if (t <= ThoT[i])
                {
                    float k = (t - ThoT[i - 1]) / (ThoT[i] - ThoT[i - 1]);
                    float v = Mathf.Lerp(ThoV[i - 1], ThoV[i], k * k * (3 - 2 * k));
                    return 0.8f + 0.2f * (v - 0.6f) / 0.4f;
                }
            return 0.8f;
        }

        // ================= TIA NƯỚC kiểu Water Laser =================
        // Mổ gói (FX_PF_WaterLaser_Cast / MainLaser / Impact / Burst / Dissolve):
        //  - Cast: tia MẢNH phóng tới (LaserCore 0,4 s) + mũ lưỡi liềm ở đầu (TwirlingWater 2x8) + bọt văng (Dots), toé ở đích.
        //  - MainLaser: ống nhiều lớp (LaserCore 01/02 Fresnel lõi sáng mép đậm; LaserNoise 01–04 vân nước sắc trôi nhanh dọc thân), bề dày
        //    "thở" theo đường cong 1 s; đầu tia (Head) có lá nước xoay (LateralWater 3x4, quay 2,15 rad/s) + khối xoắn (TwirlingWater) + vòng
        //    nước nở (WaterAOE TiledWater 3x4, sinh 2–4 / s); bong bóng trôi trong lòng tia (bubbles 2x2), giọt bắn khỏi thân (FlipbookDots
        //    kéo dài, 20–45 / s); dưới đất vệt nước trượt cuộn (LateralWaterSlide 4x4, 23 / s), vòng gợn chấm (WaterDots), toé mưa (RainSplash).
        //  - Impact (lặp 0,2 s): chớp tròn (Animeimpact) + chớp hướng (DirectionalImpact) + gai sắc bắn ra (ImpactShapes 2x2, 3–8 cái, kéo
        //    dài) + toé ngang có hướng (LateralSplash 2x5) + giọt (15–20 + 20 / s) + nền đất như trên.
        //  - Dissolve: tia mảnh lại, vỡ khúc (tan theo nhiễu), mảnh xoắn rơi, toé + nền đất đọng lại.
        // Ở đây: cùng hợp đồng giờ của NTiaShader / TiaFb (đầu tia vươn tVuon từ tTu, giữ tBan, đuôi rời miệng chạy tới đích với vChay);
        // gyGoc / gyDich: mặt đất dưới người bắn / dưới đối thủ (vệt nước trượt nằm trên đường đất nối hai chân).
        void NLaser(Func<Vector2> goc, Func<Vector2> dich, float day, float tTu, float tBan, int g, float nongK, float trungK, float gyGoc, float gyDich)
        {
            var g0 = goc();
            var h0 = dich();
            float dai = Mathf.Max(20, (h0 - g0).magnitude);
            float tVuon = Mathf.Clamp(dai / 2600f, 0.07f, 0.14f);
            float tHitL = tTu + tVuon, tEnd = tHitL + tBan;
            float vChay = Mathf.Max(380, dai / 0.32f), tDuoi = dai / vChay;
            float sd = NSeed();

            // ---- THÂN ỐNG (4 lớp) + mũ đầu tia lúc phóng
            NP(g, tEnd + tDuoi + 0.08f, (q, a) =>
            {
                var o = goc();
                var h = dich();
                var dv = h - o;
                float L = Mathf.Max(1, dv.magnitude);
                var u = dv / L;
                var n = new Vector2(-u.y, u.x);
                float head = a < tTu ? 0 : Mathf.Min(1, EaseOut((a - tTu) / tVuon));
                float tail = a < tEnd ? 0 : Mathf.Clamp01((a - tEnd) / tDuoi);
                if (head <= tail + 0.002f) return;
                float sw;
                if (a < tHitL) sw = 0.32f;                                                       // Cast: tia mảnh
                else if (a < tHitL + 0.11f) sw = 0.32f + 0.86f * EaseOut((a - tHitL) / 0.11f);   // phình vượt cỡ (đường cong gói: 0,6 → 1 ở 0,11)
                else sw = Mathf.Lerp(1.18f, 1, Mathf.Clamp01((a - tHitL - 0.11f) / 0.15f)) * Tho(a - tHitL);
                if (a > tEnd) sw *= Mathf.Lerp(1, 0.45f, tail);
                float cut = a > tEnd ? 0.12f + 0.75f * tail : 0;
                nPts.Clear();
                nHw.Clear();
                int N = Mathf.Clamp(Mathf.RoundToInt(L / 9), 12, 64);
                float s0 = tail, s1 = head;
                for (int i = 0; i <= N; i++)
                {
                    float s = Mathf.Lerp(s0, s1, i / (float)N);
                    float wave = Mathf.Sin(s * Mathf.PI * 2.2f - a * 9) * 0.1f * day * s * (1 - s);
                    nPts.Add(o + u * (s * L) + n * wave);
                    float neck = 0.62f + 0.38f * Mathf.Clamp01(s * L / (1.1f * day));            // miệng thon hơn chút
                    float tip = s1 < 1 && s > s1 - 0.06f ? Mathf.Clamp01((s1 - s) / 0.06f) * 0.6f + 0.4f : 1; // đầu đang vươn: mũi thuôn
                    nHw.Add(0.56f * day * sw * neck * tip); // gói: ống dày, đọc rõ khối
                }
                NTubePrep();
                NTube(g, 3.82f, 3, 1.22f, 1.25f, Mathf.Max(cut, 0.05f), sd);       // vỏ mỏng rách (xoắn ngoài)
                NTube(g, 4.0f, 0, 1f, 1.7f, cut, sd + 3);                           // vỏ ngoài
                NTube(g, 4.12f, 1, 0.56f, 2.3f, cut, sd + 7);                       // lõi sáng
                NTube(g, 4.2f, 2, 0.78f, 2.9f, cut, sd + 11);                       // vệt bọt trôi
                if (a >= tTu && a < tHitL) // mũ lưỡi liềm ở đầu tia đang phóng (Cast: TwirlingWater trên mũ)
                {
                    var hp = o + u * (s1 * L);
                    float k = (a - tTu) / tVuon;
                    NFbS(g, 4.35f, hp - u * (0.25f * day), 1.15f * day, 0.95f * day, NAng(u) + 90, NFb.NuocNgang, 2 + 3 * k, 0.32f, 1, sd, 0.15f);
                }
            });

            // ---- ĐẦU NÒNG: khối nước cuộn (tụ → nhả), lá nước xoay, vòng nước nở
            if (nongK > 0)
            {
                var dN = NuocFbBang.Get(NFb.CauVong);
                NP(g, tEnd + 0.12f, (q, a) =>
                {
                    var o = goc();
                    var u = (dich() - o).normalized;
                    float grow = a < tTu ? 0.3f + 0.7f * EaseOut(a / Mathf.Max(0.02f, tTu)) : 1 + 0.06f * Mathf.Sin(a * 15);
                    if (a > tEnd) grow *= Mathf.Max(0, 1 - (a - tEnd) / 0.12f);
                    float w = 1.25f * day * nongK * grow;
                    float fr = (a * 24) % dN.frames;
                    NFbS(g, 4.6f, o + u * (0.12f * w), w, w * 0.92f, NAng(u), NFb.CauVong, fr, 0.34f, 1, sd + 1, 0.08f, 0, true); // mặt trắng gốc ở −x → lật
                });
                Every(tTu, tEnd, 4.2f, x => // lá nước xoay quanh đầu tia (LaserNoise06: quay ngẫu nhiên ±2,15 rad/s)
                {
                    float sp = (U(0, 1) < 0.5f ? -1 : 1) * U(90, 150);
                    float ang0 = U(0, 360);
                    NFbPhat(U(0, 1) < 0.5f ? g : Back, 4.5f, default, Vector2.zero, U(0.45f, 0.6f), NFb.NuocNgang, 1.2f * day * nongK,
                        1.6f * day * nongK, ang0, 0.3f, 0.05f, 0, false, 0, 0, sp, 0, t => goc());
                });
                Every(tTu, tEnd, 3.2f, x => // vòng nước nở quanh gốc tia (WaterAOE: dải gai nước dựng vuông góc thân)
                {
                    var u = (dich() - goc()).normalized;
                    float off = U(0.1f, 0.5f) * day;
                    NFbPhat(g, 4.48f, default, Vector2.zero, U(0.32f, 0.4f), NFb.VongNuoc, 1.3f * day * nongK, 2.3f * day * nongK, NAng(u) - 90, 0.3f,
                        0.05f, 0, U(0, 1) < 0.5f, 0, 0, 0, 0.42f, t => goc() + (dich() - goc()).normalized * (off + 260 * t));
                });
            }

            // ---- VÒNG LƯỠI LIỀM ôm thân gần miệng (mũ lưỡi liềm / khối xoắn ở Head của gói: TwirlingWater trên khối xoắn, 6 / s): lưỡi liềm
            // chém vòng (CicularSlash) ép dẹt theo trục tia → vòng nước ôm ống nhìn ngang, chạy ra ~45 % thân rồi tan
            Every(tHitL, tEnd, 9, x =>
            {
                bool truoc = U(0, 1) < 0.6f;
                float dur = U(0.3f, 0.4f), reach = U(0.3f, 0.55f);
                float angT = NAng(dich() - goc());
                float hgt = U(1.5f, 1.9f) * day;
                NFbPhat(g, truoc ? 4.42f : 3.72f, default, Vector2.zero, dur, NFb.ChemVong, hgt * 0.42f, hgt * 0.55f, angT, 0.3f, truoc ? 0.05f : -0.12f, 0,
                    U(0, 1) < 0.5f, 0, 0, 0, 1 / 0.42f, t =>
                    {
                        var o = goc();
                        var dv = dich() - o;
                        float L = dv.magnitude;
                        return o + dv / Mathf.Max(1, L) * (Mathf.Min(1, 0.05f + t / dur) * reach * L);
                    });
            });
            // ---- XOẮN chạy dọc thân tới đích (LaserNoise05: TwirlingWater), xen trước / sau thân
            Every(tHitL, tEnd, 8, x =>
            {
                bool truoc = U(0, 1) < 0.55f;
                float dur = U(0.28f, 0.36f), w = U(2.0f, 2.8f) * day;
                float angT = NAng(dich() - goc());
                float lech = U(-0.12f, 0.12f) * day;
                NFbPhat(g, truoc ? 4.4f : 3.7f, default, Vector2.zero, dur, NFb.Xoan, w, w * 1.08f, angT, 0.28f, truoc ? 0.05f : -0.1f, 0, U(0, 1) < 0.5f,
                    0, 0, 0, U(0.5f, 0.65f), t =>
                    {
                        var o = goc();
                        var dv = dich() - o;
                        float L = dv.magnitude;
                        var u = dv / Mathf.Max(1, L);
                        return o + u * (Mathf.Min(1, 0.08f + t / dur * 0.95f) * L) + new Vector2(-u.y, u.x) * lech;
                    });
            });

            // ---- BONG BÓNG trôi trong lòng tia + GIỌT bắn khỏi thân
            Every(tHitL, tEnd, 22, x =>
            {
                float dur = U(0.32f, 0.45f), lech = U(-0.3f, 0.3f) * day, r = U(0.13f, 0.24f) * day;
                NFbPhat(g, 4.3f, default, Vector2.zero, dur, NFb.BongNho, r, r * 0.8f, U(0, 360), 0.35f, 0.25f, 0, false, 0, 0, 0, 0, t =>
                {
                    var o = goc();
                    var dv = dich() - o;
                    float L = dv.magnitude;
                    var u = dv / Mathf.Max(1, L);
                    return o + u * (Mathf.Min(1, t / dur) * L * 0.96f) + new Vector2(-u.y, u.x) * lech;
                });
            });
            Every(tHitL, tEnd + tDuoi, 30, x =>
            {
                var o = goc();
                var dv = dich() - o;
                float L = dv.magnitude, s = U(0.12f, 0.95f);
                var u = dv / Mathf.Max(1, L);
                var n = new Vector2(-u.y, u.x);
                float side = U(0, 1) < 0.5f ? -1 : 1;
                var v = u * U(60, 220) + n * side * U(80, 230) + Len * U(0, 90);
                float r = U(0.1f, 0.22f) * day;
                NFbPhat(g, 4.55f, o + u * (s * L) + n * side * (0.4f * day), v, U(0.38f, 0.55f), NFb.Giot, r * 1.6f, r * 0.9f, NAng(v), 0.35f, 0.1f,
                    0, false, 900, 0, 0, 0.62f);
            });

            // ---- NỀN ĐẤT dọc đường tia: vệt nước trượt cuộn theo hướng tia, vòng gợn chấm, toé mưa
            bool lat = (h0 - g0).x < 0; // texture TruotDat cuộn về +x
            Every(tHitL, tEnd + tDuoi * 0.6f, 15, x =>
            {
                var o = goc();
                var h = dich();
                float s = U(0.25f, 1.02f);
                var p = new Vector2(Mathf.Lerp(o.x, h.x, s), Mathf.Lerp(gyGoc, gyDich, s) + U(-2, 8));
                float w = U(1.4f, 2.4f) * day;
                NFbPhat(Floor, 2.2f, p + Len * (0.25f * w), new Vector2(Mathf.Sign(h.x - o.x) * U(20, 60), 0), U(0.45f, 0.6f), NFb.TruotDat, w * 0.8f, w, 0, 0.3f, -0.02f, 1,
                    lat, 0, 2);
            });
            Every(tHitL, tEnd + tDuoi, 11, x =>
            {
                var h = dich();
                var p = new Vector2(h.x + U(-1.4f, 1.4f) * day, gyDich + U(-4, 10));
                float w = U(0.9f, 1.7f) * day;
                NFbPhat(Floor, 2.1f, p, Vector2.zero, U(0.6f, 0.8f), NFb.ChamDat, w * 0.45f, w, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f);
            });
            Every(tHitL, tEnd + tDuoi, 9, x =>
            {
                var o = goc();
                var h = dich();
                float s = U(0.5f, 1.05f);
                var p = new Vector2(Mathf.Lerp(o.x, h.x, s) + U(-0.5f, 0.5f) * day, Mathf.Lerp(gyGoc, gyDich, s) + U(0, 8));
                NFb m = (NFb)((int)NFb.MuaA + rng.Next(4));
                float w = U(0.6f, 1.05f) * day;
                NFbPhat(Front, 2.3f, p + Len * (0.3f * w), Vector2.zero, U(0.55f, 0.75f), m, w, w * 1.08f, 0, 0.3f, 0.05f, 0, U(0, 1) < 0.5f);
            });

            // ---- CHỖ TRÚNG (lặp 0,2 s như FX_PF_WaterLaser_Impact)
            if (trungK > 0)
            {
                int nb = Mathf.Max(1, Mathf.CeilToInt((tEnd + tDuoi * 0.5f - tHitL) / 0.2f));
                for (int i = 0; i < nb; i++)
                {
                    int ii = i;
                    At(tHitL + i * 0.2f, () =>
                    {
                        var o = goc();
                        var h = dich();
                        var u = (h - o).normalized;
                        float k = trungK * (ii == 0 ? 1.2f : 1);
                        float back = NAng(-u);
                        // chớp tròn + chớp hướng (bọt trắng sáng, 0,12–0,2 s)
                        NFbPhat(g, 6.2f, h - u * (0.1f * day), Vector2.zero, U(0.12f, 0.18f), NFb.ChopTron, 1.3f * day * k, 1.9f * day * k, U(0, 360), 0.3f,
                            0.18f);
                        if ((ii & 1) == 0)
                            NFbPhat(g, 6.1f, h, Vector2.zero, 0.14f, NFb.ChopHuong, 1.6f * day * k, 2.1f * day * k, U(0, 360), 0.3f, 0.12f);
                        // gai sắc bắn ra: ngược về phía người bắn + toả hai bên (nước dội thân bật lại), kéo dài theo hướng bay
                        int m = ii == 0 ? 7 : rng.Next(3, 6);
                        for (int j = 0; j < m; j++)
                        {
                            float an = back + (U(0, 1) < 0.5f ? -1 : 1) * U(15, 80);
                            var dir = new Vector2(Mathf.Cos(an * Mathf.Deg2Rad), -Mathf.Sin(an * Mathf.Deg2Rad));
                            float w = U(0.8f, 1.5f) * day * k;
                            NFbPhat(g, 6.0f, h + dir * (0.2f * day), dir * U(160, 420), U(0.2f, 0.26f), NFb.GaiTrung, w, w * 1.25f, an, 0.32f, -0.12f, 0,
                                false, 0, 3, 0, 0.55f);
                        }
                        // toé ngang có hướng (LateralSplash 2x5): ngược + lên / xuống theo thân
                        for (int j = 0; j < (ii == 0 ? 2 : 1); j++)
                        {
                            float an = back + (U(0, 1) < 0.5f ? 1 : -1) * U(20, 55);
                            var dir = new Vector2(Mathf.Cos(an * Mathf.Deg2Rad), -Mathf.Sin(an * Mathf.Deg2Rad));
                            float w = U(1.8f, 2.6f) * day * k;
                            NFbPhat(g, 5.6f, h + dir * (0.45f * w), dir * U(60, 140), U(0.22f, 0.3f), U(0, 1) < 0.5f ? NFb.ToeNgangA : NFb.ToeNgangB, w * 0.8f,
                                w, an, 0.3f, 0.05f);
                        }
                        // toé thường bay ngược / lên (Splashes)
                        for (int j = 0; j < 2; j++)
                        {
                            var v = new Vector2(-u.x * U(80, 260), -U(60, 260));
                            float w = U(0.9f, 1.4f) * day * k;
                            NFbPhat(g, 5.4f, h + U2(-0.3f, 0.3f) * day, v, U(0.45f, 0.6f), NFb.Toe, w * 0.6f, w, U(0, 360), 0.3f, 0, 0, false, 500, 2);
                        }
                        // giọt toả nửa sau
                        for (int j = 0; j < (ii == 0 ? 14 : 5); j++)
                        {
                            float an = back + U(-95, 95);
                            var v = new Vector2(Mathf.Cos(an * Mathf.Deg2Rad), -Mathf.Sin(an * Mathf.Deg2Rad)) * U(180, 520);
                            float r = U(0.1f, 0.2f) * day;
                            NFbPhat(g, 5.9f, h + U2(-5, 5), v, U(0.4f, 0.6f), NFb.Giot, r * 1.7f, r, NAng(v), 0.35f, 0.1f, 0, false, 900, 0, 0, 0.6f);
                        }
                    });
                }
            }

            // ---- TẮT (Dissolve): mảnh xoắn + toé rơi dọc thân lúc đuôi chạy
            At(tEnd, () =>
            {
                var o = goc();
                var h = dich();
                var dv = h - o;
                float L = dv.magnitude;
                var u = dv / Mathf.Max(1, L);
                for (int j = 0; j < 7; j++)
                {
                    float s = U(0.1f, 0.95f);
                    var p = o + u * (s * L);
                    var v = u * U(40, 160) + new Vector2(U(-60, 60), -U(40, 160));
                    float w = U(0.9f, 1.5f) * day;
                    NFbPhat(g, 4.7f, p, v, U(0.4f, 0.55f), j % 2 == 0 ? NFb.NuocNgang : NFb.Toe, w * 0.7f, w, U(0, 360), 0.32f, 0, 0, false, 700, 1.5f,
                        U(-120, 120));
                }
            });
        }
        // ================= KHỐI DÙNG CHUNG theo gói (toé, trúng, toé đất, vương miện chân) =================
        // Gói: Water_Impact_01 / SimpleWaterImpact / Water_SimpleSplash_01 / ImpactGround (Rubfish), Hit_01 / 02, Water_Splash_A / B,
        // Water_Impact (NamuFX): chớp tròn 0,1–0,15 s → toé bung giữa flipbook 4x4 (0,4–0,6 s) + toé ngang có hướng + 2–3 khối toé bay
        // (Size 0 → 1, rơi) + giọt kéo dài 10–20 + nền đất (toé đất, vòng gợn chấm, toé mưa nhỏ).
        public static bool NuocGoi = true; // tắt: về khối shader bản 2

        static Vector2 NHuong(float angUi) => new Vector2(Mathf.Cos(angUi * Mathf.Deg2Rad), -Mathf.Sin(angUi * Mathf.Deg2Rad));

        // toé lớn ở thân (NSplash): R = 0,62 tH × sc; back = về phía đòn tới
        void GSplash(Vector2 c, float sc, float ground, float tH, int g, Vector2? dir)
        {
            float d = dir.HasValue && Mathf.Abs(dir.Value.x) > 0.01f ? Mathf.Sign(dir.Value.x) : U(0, 1) < 0.5f ? -1 : 1;
            var back = new Vector2(-d, -0.8f).normalized;
            float R = 0.62f * tH * sc, ab = NAng(back);
            NFbPhat(g, 6.2f, c, Vector2.zero, 0.13f, NFb.ChopTron, 0.9f * R, 1.4f * R, U(0, 360), 0.3f, 0.2f);
            NFbPhat(g, 5.2f, c + Len * (0.15f * R), Vector2.zero, 0.5f, NFb.ToeGiua, 1.5f * R, 1.9f * R, 0, 0.3f, 0.02f, 0, d > 0);
            for (int i = 0; i < 2; i++)
            {
                float an = ab + (i == 0 ? 1 : -1) * U(10, 35);
                var h = NHuong(an);
                NFbPhat(g, 5.6f, c + h * (0.5f * R), h * U(60, 140), U(0.28f, 0.36f), i == 0 ? NFb.ToeNgangA : NFb.ToeNgangB, 1.3f * R, 1.7f * R, an,
                    0.3f, 0.04f);
            }
            for (int i = 0; i < 3; i++)
            {
                var v = new Vector2(-d * U(80, 280), -U(120, 320));
                NFbPhat(g, 5.4f, c + U2(-0.2f, 0.2f) * R, v, U(0.5f, 0.62f), NFb.Toe, 0.35f * R, 0.75f * R, U(0, 360), 0.3f, 0, 0, false, 700, 1.5f);
            }
            float sq = Mathf.Sqrt(Mathf.Max(0.2f, sc));
            for (int i = 0; i < 14; i++)
            {
                float an = ab + U(-70, 70);
                var v = NHuong(an) * (U(220, 480) * sq);
                float r = U(2.6f, 4.6f) * sq;
                NFbPhat(g, 5.9f, c + U2(-6, 6), v, U(0.42f, 0.62f), NFb.Giot, r * 1.8f, r, NAng(v), 0.35f, 0.1f, 0, false, 900, 0, 0, 0.6f);
            }
            var gp = new Vector2(c.x, ground);
            NFbPhat(Front, 3.3f, gp + Len * (0.32f * R), Vector2.zero, 0.55f, NFb.ToeDat, 1.5f * R, 1.8f * R, 0, 0.3f, 0, 0, d < 0);
            NFbPhat(Floor, 2.1f, gp, Vector2.zero, 0.75f, NFb.ChamDat, 0.6f * R, 1.6f * R, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f);
        }

        // trúng nhỏ ở thân (NTrung): toé trúng flipbook + toé ngang ngược hướng tới + giọt
        P GTrung(Vector2 c, float h, Vector2? dir, int g)
        {
            float d = dir.HasValue && Mathf.Abs(dir.Value.x) > 0.01f ? Mathf.Sign(dir.Value.x) : U(0, 1) < 0.5f ? -1 : 1;
            var back = new Vector2(-d, -0.85f).normalized;
            float R = 0.55f * h, ab = NAng(back);
            var p = NFbPhat(g, 5.3f, c + back * (0.1f * R), Vector2.zero, 0.42f, NFb.ToeTrung, 1.3f * R, 1.7f * R, 0, 0.3f, 0.02f, 0, d > 0); // texture toé chéo lên phải
            NFbPhat(g, 6.1f, c, Vector2.zero, 0.11f, NFb.ChopTron, 0.7f * R, 1.1f * R, U(0, 360), 0.3f, 0.2f);
            float an0 = ab + U(-15, 15);
            var h0 = NHuong(an0);
            NFbPhat(g, 5.5f, c + h0 * (0.4f * R), h0 * U(50, 110), 0.3f, NFb.ToeNgangC, 1.1f * R, 1.5f * R, an0 + 180, 0.3f, 0.03f); // ToeNgangC toé về −x
            for (int i = 0; i < 8; i++)
            {
                float an = ab + U(-60, 60);
                var v = NHuong(an) * U(180, 380);
                float r = U(2.2f, 3.6f);
                NFbPhat(g, 5.9f, c + U2(-4, 4), v, U(0.35f, 0.55f), NFb.Giot, r * 1.7f, r, NAng(v), 0.35f, 0.1f, 0, false, 900, 0, 0, 0.6f);
            }
            return p;
        }

        // vương miện nước toé từ đất (NToe): toé đất lớn (GroundSplash 5x5) + vòng gợn chấm; trả hạt toé
        P GToe(Vector2 feet, float h, int g)
        {
            var p = NFbPhat(g, 3.3f, feet + Len * (0.4f * h), Vector2.zero, 0.6f, NFb.ToeDatLon, 1.1f * h, 1.35f * h, 0, 0.3f, 0.02f, 0, U(0, 1) < 0.5f);
            NFbPhat(Floor, 2.1f, feet, Vector2.zero, 0.7f, NFb.ChamDat, 0.4f * h, 1.1f * h, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f);
            return p;
        }

        // vương miện dưới chân (NCrownDat): hàng gai nước dựng (TiledWater, như vòng WaterAOE) + toé đất + vòng gợn
        void GCrownDat(Vector2 feet, float wd, float life, int g)
        {
            float l = Mathf.Max(0.35f, life);
            NFbPhat(g, 3.25f, feet + Len * (0.2f * wd), Vector2.zero, l, NFb.VongNuoc, 0.8f * wd, 1.15f * wd, 0, 0.3f, 0.02f, 0, U(0, 1) < 0.5f, 0, 0, 0, 0.42f);
            NFbPhat(Back, 3.1f, feet + Len * (0.24f * wd), Vector2.zero, l * 0.9f, NFb.VongNuoc, 0.7f * wd, 1.0f * wd, 0, 0.3f, -0.08f, 0, U(0, 1) < 0.5f, 0, 0, 0,
                0.4f);
            NFbPhat(Floor, 2.1f, feet, Vector2.zero, l + 0.15f, NFb.ChamDat, 0.4f * wd, 1.2f * wd, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f);
        }

        // phần thêm cho cầu nước đang bay (NCauShader): khối nước cuộn kéo sau cầu (WaterLoop như StrongProjectile_Traveling), lưỡi liềm
        // quay quanh (WaterOrb_Loop / Charge), bong bóng rơi theo đuôi
        void GCauThem(P q, Vector2 now, Vector2 past, float r, float sd)
        {
            var dv = now - past;
            float sp = dv.magnitude;
            var dN = NuocFbBang.Get(NFb.CauVong);
            if (sp > 0.5f * r)
            {
                var u = dv / sp;
                float len = Mathf.Min(2.6f * r, 1.2f * r + sp * 0.6f);
                NFbS(q.group, 5.8f, now - u * (0.45f * len), len, 1.55f * r, NAng(u), NFb.CauVong, (q.age * 24) % dN.frames, 0.34f, 1, sd, 0.05f, 0, true);
            }
            var dC = NuocFbBang.Get(NFb.ChemVong);
            float fr = (q.age * 20) % dC.frames;
            NFbS(q.group, 6.2f, now, 2.3f * r, 2.3f * r, q.age * 260 + sd * 40, NFb.ChemVong, fr, 0.32f, 1, sd + 2, 0.12f);
        }
        // ================= SÓNG, MẠCH PHUN, MƯA theo gói =================
        // sóng đang chạy (WaveAttack_Projectile / Cast): vệt nước trượt cuộn ở chân (LateralWaterSlide, 0,8–1,5 / s mỗi bên → dày hơn cho
        // nhìn ngang), sóng trượt ở mào, khói bọt + toé mưa đọng lại phía sau (Lingering: FoamSmoke 12–20 / s, RainSplash 12 / s)
        void GSongThem(Func<Vector2> now, float sx, float tH, float T0, float TT)
        {
            bool lat = sx < 0; // texture trượt / sóng trượt cuộn về +x
            Every(T0, T0 + TT, 9, x =>
            {
                var c = now();
                float w = U(0.6f, 1.0f) * tH;
                NFbPhat(Front, 23.6f, c + new Vector2(sx * U(-0.1f, 0.35f) * tH, 0) + Len * (0.27f * w), new Vector2(sx * U(120, 240), 0), U(0.42f, 0.55f),
                    NFb.TruotDat, w * 0.8f, w, 0, 0.3f, 0.02f, 0, lat, 0, 1.5f);
            });
            Every(T0 + 0.05f, T0 + TT, 6, x =>
            {
                var c = now();
                float w = U(0.7f, 1.0f) * tH;
                NFbPhat(Front, 23.8f, c + new Vector2(sx * 0.15f * tH, -U(0.45f, 0.75f) * tH), new Vector2(sx * U(150, 300), -U(0, 60)), U(0.4f, 0.5f),
                    NFb.SongTruot, w * 0.8f, w, 0, 0.3f, 0.06f, 0, lat, 300, 1);
            });
            Every(T0, T0 + TT, 13, x =>
            {
                var c = now();
                float w = U(0.45f, 0.75f) * tH;
                NFbPhat(Back, 3.6f, c - new Vector2(sx * U(0.35f, 0.95f) * tH, U(0.05f, 0.3f) * tH), new Vector2(0, -U(5, 25)), U(0.8f, 1.2f), NFb.BotKhoi,
                    w * 0.7f, w, U(-20, 20), 0.3f, 0.3f, 0, U(0, 1) < 0.5f, 0, 0, 0, 0, null, 0.55f);
            });
            Every(T0, T0 + TT + 0.2f, 10, x =>
            {
                var c = now();
                NFb m = (NFb)((int)NFb.MuaA + rng.Next(4));
                float w = U(0.35f, 0.6f) * tH;
                NFbPhat(Front, 2.4f, c - new Vector2(sx * U(0.2f, 1.1f) * tH, -U(0, 8)) + Len * (0.3f * w), Vector2.zero, U(0.6f, 0.8f), m, w, w * 1.08f, 0,
                    0.3f, 0.05f, 0, U(0, 1) < 0.5f);
            });
        }

        // sóng đổ tới đích (thêm vào NSongDo): chớp hướng + gai sắc bắn tung theo hướng sóng (WaveAttack_Impact), vệt trượt hai bên chân
        void GSongDo(Vector2 foeFeet, float tH, float sx)
        {
            var body = foeFeet + new Vector2(0, -0.5f * tH);
            float fw = sx > 0 ? 0 : 180;
            NFbPhat(Front, 6.1f, body, Vector2.zero, 0.14f, NFb.ChopHuong, 0.9f * tH, 1.2f * tH, U(0, 360), 0.3f, 0.12f);
            for (int j = 0; j < 6; j++)
            {
                float an = fw + U(-70, 70);
                var dir = NHuong(an);
                float w = U(0.35f, 0.6f) * tH;
                NFbPhat(Front, 6.0f, body + dir * (0.15f * tH), dir * U(180, 420), U(0.2f, 0.26f), NFb.GaiTrung, w, w * 1.25f, an, 0.32f, -0.12f, 0, false, 0,
                    3, 0, 0.55f);
            }
            for (int s = -1; s <= 1; s += 2)
            {
                float w = U(0.8f, 1.1f) * tH;
                NFbPhat(Front, 3.4f, foeFeet + new Vector2(s * 0.35f * tH, 0) + Len * (0.27f * w), new Vector2(s * U(80, 160), 0), U(0.45f, 0.6f), NFb.TruotDat,
                    w * 0.8f, w, 0, 0.3f, 0.02f, 0, s < 0, 0, 2);
            }
        }

        // cột nước mạch phun (thêm vào NXoayShader lúc phụt): 2–3 cột nước dựng flipbook (VerticalSplash 4x4) quanh cột shader, toé đất lớn
        // ở chân, toé thường bay từ đỉnh
        void GCotPhun(Vector2 Cc, float tH)
        {
            for (int i = 0; i < 3; i++)
            {
                float w = (i == 0 ? 0.75f : U(0.45f, 0.6f)) * tH;
                var p = Cc + new Vector2(i == 0 ? 0 : (i == 1 ? -1 : 1) * U(0.18f, 0.3f) * tH, 0);
                NFbPhat(i == 0 ? Front : Back, 3.15f, p + Len * (0.8f * w), Vector2.zero, U(0.55f, 0.7f), NFb.CotDung, w, w * 1.05f, 0, 0.3f, 0.04f, 0,
                    U(0, 1) < 0.5f);
            }
            NFbPhat(Front, 3.3f, Cc + Len * (0.38f * tH), Vector2.zero, 0.6f, NFb.ToeDatLon, 1.0f * tH, 1.25f * tH, 0, 0.3f, 0.02f, 0, U(0, 1) < 0.5f);
            for (int i = 0; i < 4; i++)
            {
                var v = new Vector2(U(-200, 200), -U(250, 420));
                NFbPhat(Front, 5.4f, Cc + Len * (1.3f * tH), v, U(0.55f, 0.7f), NFb.Toe, 0.2f * tH, 0.42f * tH, U(0, 360), 0.3f, 0, 0, false, 800, 1);
            }
        }

        // mưa (thêm vào NMua): vòng gợn mưa + toé hạt mưa trên đất quanh chân đối thủ (RainExample + WaterGround của gói)
        void GMuaDat(Vector2 foeFeet, float tH, float T0, float T1)
        {
            Every(T0 + 0.15f, T1 + 0.3f, 16, x =>
            {
                var p = foeFeet + new Vector2(U(-1.1f, 1.1f) * tH, U(-6, 14));
                float w = U(0.3f, 0.6f) * tH;
                NFbPhat(Floor, 2.15f, p, Vector2.zero, U(0.5f, 0.75f), NFb.GonMua, w * 0.5f, w, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f);
            });
            Every(T0 + 0.15f, T1 + 0.2f, 14, x =>
            {
                var p = foeFeet + new Vector2(U(-1.0f, 1.0f) * tH, U(-4, 12));
                NFb m = (NFb)((int)NFb.MuaA + rng.Next(4));
                float w = U(0.25f, 0.45f) * tH;
                NFbPhat(Front, 2.4f, p + Len * (0.3f * w), Vector2.zero, U(0.5f, 0.7f), m, w, w * 1.08f, 0, 0.3f, 0.05f, 0, U(0, 1) < 0.5f);
            });
        }
    }
}
