// TIA NĂNG LƯỢNG kiểu Water Laser (2026-11-25; người dùng: "quét tia water laser mới làm, sau đó dùng base đó làm tia năng lượng bắn ra
// và impact cho các tia năng lượng của các tướng đảo mộc/kim/thổ"). Khung lấy nguyên từ NLaser (HatNuocGoi.cs, mổ gói FX_PF_WaterLaser_*):
//  - THÂN: ống 4 lớp vẽ bằng shader UIWaterFx chế độ 7 (vỏ mỏng rách, vỏ ngoài, lõi sáng, vệt sáng trôi; vân sắc kéo dài dọc thân), pha Cast
//    tia MẢNH phóng tới có mũi gai, chạm thì PHÌNH vượt cỡ rồi "thở" theo đường cong 1 s của gói, gợn ngang, miệng thon;
//  - vòng lưỡi liềm ôm thân gần miệng (ChemVong ép dẹt theo trục), xoắn chạy dọc thân tới đích (Xoan), xen trước / sau ống;
//  - CHỖ TRÚNG lặp 0,2 s (FX_PF_WaterLaser_Impact): chớp tròn + chớp hướng, gai sắc bắn ngược + toả hai bên kéo dài theo hướng bay, toé sao
//    có hướng, tia vụn;
//  - TẮT: ngừng nhả, đuôi rời miệng chạy nốt tới đích, ống mảnh lại và vỡ khúc theo nhiễu, mảnh xoắn rơi.
// Đổi cho năng lượng:
//  - màu: bảng shader theo hệ (HatNuocFx.Pal*: lục ngọc / hổ phách / lửa nhiệt / Kim / Thổ) cho ống và mọi flipbook, không tô lam;
//  - hạt chỉ hợp nước (giọt, bong bóng, lá nước, toé thường, vệt nước trượt, mưa) thay bằng hạt theo hệ: tia vụn có mực (DrawVun) bắn khỏi
//    thân và cưỡi dọc tia, lá xanh + lá phong (Mộc), lá hổ phách (Giác Mộc), than lửa (tia nhiệt);
//  - đầu nòng: cầu năng lượng Energy Ball người dùng đã chọn cho Mộc / Kim / Thổ (khung cau_moc / cau_vang như TiaFb, lớn dần lúc tụ, phập
//    phồng lúc bắn), lưỡi liềm quay quanh, vòng gai nở dọc gốc tia;
//  - nền đất: vòng gợn trên đất ở chân đối thủ (ChamDat, bảng hệ, kiểu nền); bụi, lá rơi, nổ cuối do hàm gọi giữ như cũ.
// Hợp đồng giờ y như TiaFb (HatTiaFb.cs): gọi lúc bắt đầu tụ, tụ tTu giây, đầu tia vươn TiaVuon(quãng) giây, dội tBan giây kể từ lúc chạm,
// rồi đuôi rời miệng bay nốt tới đích (tốc max(380, quãng / 0,32)). Trả giờ chạm. Chỉ chạy khi có lưới shader (CoLaser); không có thì hàm gọi
// tự về TiaFb vẽ sẵn như trước.
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public sealed class LaserHe
        {
            public int pal;               // bảng màu shader (HatNuocFx.Pal*)
            public string nl;             // khung cầu năng lượng đầu nòng (cau_moc / cau_vang); null: không cầu (nguồn do hàm gọi vẽ)
            public float nlR = 0.85f;     // bán kính thấy của cầu / bề dày tia (như TiaSkin.nlR)
            public Color vun1, vun2;      // tia vụn bắn khỏi thân / chỗ trúng (xen hai màu)
            public int hat;               // hạt cưỡi dọc tia: 1 lá xanh + lá phong, 2 lá theo bảng tướng (hổ phách), 3 than lửa
        }

        // Lộc Phong: năng lượng lục ngọc gân chanh (cầu cau_moc), lá phong đỏ cam cuốn theo; Giác Mộc: hổ phách (cầu cau_vang); Thổ Tinh: tia
        // nhiệt từ Mặt Trời (không cầu đầu nòng, Mặt Trời là nguồn)
        public static readonly LaserHe LaserMoc = new LaserHe { pal = HatNuocFx.PalMoc, nl = "cau_moc", vun1 = C(232, 245, 122), vun2 = C(250, 255, 224), hat = 1 };
        public static readonly LaserHe LaserHoPhach = new LaserHe { pal = HatNuocFx.PalHoPhach, nl = "cau_vang", vun1 = C(255, 200, 80), vun2 = C(255, 242, 196), hat = 2 };
        public static readonly LaserHe LaserLua = new LaserHe { pal = HatNuocFx.PalLua, vun1 = C(252, 214, 92), vun2 = C(255, 244, 206), hat = 3 };

        public static bool TiaLaser = true; // tắt: mọi tia năng lượng về TiaFb vẽ sẵn
        bool CoLaser => TiaLaser && NuocShaderOn;

        // tia vụn năng lượng bay tự do: vệt dài theo vận tốc, co dần, KHÔNG viền mực (vfx-petclash 1c: năng lượng không viền mực ngoài; lần
        // chụp đầu dùng DrawVun có mực: vệt nhỏ thành chấm đen lấm tấm dọc tia)
        P LVun(Vector2 pos, Vector2 vel, float life, float sz, Color col, int g, float grav = 520, float drag = 3)
        {
            var p = new P { pos = pos, vel = vel, life = Mathf.Max(0.05f, life), drag = drag, acc = new Vector2(0, grav), seed = rng.Next(4), sz = sz, group = g, col = col };
            p.draw = DrawVunNl;
            return Add(p);
        }

        void DrawVunNl(P q, float k, System.Collections.Generic.List<Item> buf)
        {
            float sp = q.vel.magnitude;
            float day = q.sz * (1 - k * k);
            if (day < 0.6f) return;
            float len = day * Mathf.Clamp(sp / 70, 1.8f, 4.6f);
            var d = sp > 1 ? q.vel / sp : Vector2.right;
            VetPut(buf, q.group, 40.2f, false, q.col, q.pos, d, len, day, 1, q.seed);
        }

        // cụm tia vụn lệch cỡ quanh hướng dir (như TiaVunCum, không mực)
        void LVunCum(Vector2 at, Vector2 dir, float lech, int n, float speed, float sz, int g, Color c1, Color c2)
        {
            var d0 = Unit(dir);
            float a0 = Mathf.Atan2(d0.y, d0.x) + U(-0.4f, 0.4f) * lech;
            for (int i = 0; i < n; i++)
            {
                float a = a0 + U(-0.6f, 0.6f) * lech;
                float f = i == 0 ? 1 : U(0.45f, 0.8f);
                LVun(at + U2(-3, 3), new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * speed * U(0.75f, 1.15f) * (0.7f + 0.3f * f), U(0.16f, 0.28f), sz * f,
                    (i & 1) == 0 ? c1 : c2, g, 520, 6);
            }
        }

        // goc / dich: gốc tia và chỗ chạm (hàm, bám rig); day: bề dày thân tia (sân); nongK / trungK: nhân cỡ cầu đầu nòng / chỗ trúng (0: bỏ);
        // gyDich: mặt đất dưới đối thủ (NaN: tia không chạm đất, vd. tia nhiệt Thổ Tinh đập vào vỏ đá giữa không trung)
        public float ELaser(LaserHe he, Func<Vector2> goc, Func<Vector2> dich, float day, float tTu, float tBan, int g = Front, float nongK = 1,
            float trungK = 1, float gyDich = float.NaN)
        {
            int pal = he.pal;
            var g0 = goc();
            var h0 = dich();
            float dai = Mathf.Max(20, (h0 - g0).magnitude);
            float tVuon = TiaVuon(dai);
            float tHitL = tTu + tVuon, tEnd = tHitL + tBan;
            float vChay = Mathf.Max(380, dai / 0.32f), tDuoi = dai / vChay;
            float sd = NSeed();

            // ---- THÂN ỐNG (4 lớp) + mũi gai ở đầu tia lúc phóng
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
                else if (a < tHitL + 0.11f) sw = 0.32f + 0.86f * EaseOut((a - tHitL) / 0.11f);   // phình vượt cỡ
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
                    float neck = 0.62f + 0.38f * Mathf.Clamp01(s * L / (1.1f * day));
                    float tip = s1 < 1 && s > s1 - 0.06f ? Mathf.Clamp01((s1 - s) / 0.06f) * 0.6f + 0.4f : 1;
                    nHw.Add(0.56f * day * sw * neck * tip);
                }
                NTubePrep();
                NTube(g, 3.82f, 3, 1.22f, 1.4f, Mathf.Max(cut, 0.05f), sd, 1, pal);   // vỏ mỏng rách
                NTube(g, 4.0f, 0, 1f, 1.9f, cut, sd + 3, 1, pal);                      // vỏ ngoài
                NTube(g, 4.12f, 1, 0.56f, 2.6f, cut, sd + 7, 1, pal);                  // lõi sáng
                NTube(g, 4.2f, 2, 0.78f, 3.2f, cut, sd + 11, 1, pal);                  // vệt sáng trôi
                if (a >= tTu && a < tHitL) // mũi gai năng lượng ở đầu tia đang phóng
                {
                    var hp = o + u * (s1 * L);
                    NFbS(g, 4.35f, hp - u * (0.2f * day), 1.3f * day, 0.9f * day, NAng(u), NFb.GaiTrung, 0, 0.3f, 1, sd, 0.2f, 0, false, pal);
                }
            });

            // ---- ĐẦU NÒNG: cầu năng lượng (tụ → phập phồng → mờ), lưỡi liềm quay quanh, vòng gai nở dọc gốc tia
            if (nongK > 0)
            {
                if (he.nl != null && HasFb(he.nl))
                {
                    float rNl = he.nlR * day * nongK, phNl = U(0, 1.5f);
                    var pn = new P { pos = goc(), group = g, life = tEnd + 0.25f };
                    pn.upd = (q, dt, L) => q.pos = goc();
                    pn.draw = (q, kk, buf) =>
                    {
                        float a = q.age;
                        float lon = a < tTu ? Mathf.Lerp(0.35f, 1f, EaseOut(a / Mathf.Max(0.01f, tTu))) : 1 + 0.07f * Mathf.Sin((a - tTu) * 50);
                        float al = Mathf.Clamp01(a / 0.06f) * Mathf.Clamp01((q.life - a) / 0.22f);
                        VeCauNl(buf, he.nl, q.pos, rNl * lon, q.group, 38, a * 1.2f + phNl, 0, 1, al);
                    };
                    Add(pn);
                }
                Every(Mathf.Max(0, tTu - 0.12f), tEnd, 4.5f, x => // lưỡi liềm quay quanh đầu nòng (LaserNoise06: quay ±2,15 rad/s)
                {
                    float sp = (U(0, 1) < 0.5f ? -1 : 1) * U(110, 170);
                    NFbPhat(U(0, 1) < 0.5f ? g : Back, 4.5f, default, Vector2.zero, U(0.4f, 0.55f), NFb.ChemVong, 1.3f * day * nongK, 1.8f * day * nongK,
                        U(0, 360), 0.3f, 0.08f, 0, U(0, 1) < 0.5f, 0, 0, sp, 0, t => goc(), 0.8f, pal);
                });
                Every(tHitL, tEnd, 3.2f, x => // vòng gai nở dọc gốc tia (WaterAOE: dải gai dựng vuông góc thân, chạy ra)
                {
                    var u = (dich() - goc()).normalized;
                    float off = U(0.1f, 0.5f) * day;
                    NFbPhat(g, 4.48f, default, Vector2.zero, U(0.32f, 0.4f), NFb.VongNuoc, 1.3f * day * nongK, 2.3f * day * nongK, NAng(u) - 90, 0.3f,
                        0.08f, 0, U(0, 1) < 0.5f, 0, 0, 0, 0.42f, t => goc() + (dich() - goc()).normalized * (off + 260 * t), 0.8f, pal);
                });
            }

            // ---- VÒNG LƯỠI LIỀM ôm thân gần miệng, chạy ra ~45 % thân rồi tan
            Every(tHitL, tEnd, 9, x =>
            {
                bool truoc = U(0, 1) < 0.6f;
                float dur = U(0.3f, 0.4f), reach = U(0.3f, 0.55f);
                float angT = NAng(dich() - goc());
                float hgt = U(1.5f, 1.9f) * day;
                NFbPhat(g, truoc ? 4.42f : 3.72f, default, Vector2.zero, dur, NFb.ChemVong, hgt * 0.42f, hgt * 0.55f, angT, 0.3f, truoc ? 0.08f : -0.1f, 0,
                    U(0, 1) < 0.5f, 0, 0, 0, 1 / 0.42f, t =>
                    {
                        var o = goc();
                        var dv = dich() - o;
                        float L = dv.magnitude;
                        return o + dv / Mathf.Max(1, L) * (Mathf.Min(1, 0.05f + t / dur) * reach * L);
                    }, 0.8f, pal);
            });
            // ---- XOẮN chạy dọc thân tới đích, xen trước / sau thân
            Every(tHitL, tEnd, 8, x =>
            {
                bool truoc = U(0, 1) < 0.55f;
                float dur = U(0.28f, 0.36f), w = U(2.0f, 2.8f) * day;
                float angT = NAng(dich() - goc());
                float lech = U(-0.12f, 0.12f) * day;
                NFbPhat(g, truoc ? 4.4f : 3.7f, default, Vector2.zero, dur, NFb.Xoan, w, w * 1.08f, angT, 0.28f, truoc ? 0.08f : -0.08f, 0, U(0, 1) < 0.5f,
                    0, 0, 0, U(0.5f, 0.65f), t =>
                    {
                        var o = goc();
                        var dv = dich() - o;
                        float L = dv.magnitude;
                        var u = dv / Mathf.Max(1, L);
                        return o + u * (Mathf.Min(1, 0.08f + t / dur * 0.95f) * L) + new Vector2(-u.y, u.x) * lech;
                    }, 0.8f, pal);
            });

            // ---- HẠT CƯỠI DỌC TIA (thay bong bóng trong lòng tia): vệt sáng chạy nhanh tới đích, lá / than lửa cuốn theo
            int seqR = 0;
            Every(tHitL, tEnd, 16, x =>
            {
                var o = goc();
                var dv = dich() - o;
                float L = Mathf.Max(1, dv.magnitude);
                var u = dv / L;
                var n = new Vector2(-u.y, u.x);
                float v = Mathf.Max(520, L / 0.32f);
                float s = U(0, 0.25f) * L;
                var p0 = o + u * s + n * (U(-0.32f, 0.32f) * day);
                float life = (L - s) / v * U(0.85f, 1f);
                int id = seqR++;
                if (he.hat == 1 && id % 3 == 1)
                {
                    var q = Leaf(p0, u * (v * 0.75f) + n * U(-40, 40), life / 0.75f, U(3.2f, 4.6f), 0, 0, U(0, 1) < 0.65f ? g : Back);
                    if ((id & 1) == 1) q.stops = LaPhong;
                }
                else if (he.hat == 2 && id % 4 == 1) Leaf(p0, u * (v * 0.75f) + n * U(-40, 40), life / 0.75f, U(3.2f, 4.4f), 0, 0, U(0, 1) < 0.65f ? g : Back);
                else if (he.hat == 3 && id % 3 == 1)
                {
                    var q = Ember(p0, u * (v * 0.6f) + n * U(-50, 50), life / 0.6f, U(6, 9), g);
                    q.col = he.vun1;
                }
                else LVun(p0, u * v, life, U(3.0f, 4.2f), (id & 1) == 0 ? he.vun1 : he.vun2, g, 0, 0);
            });
            // ---- TIA VỤN bắn khỏi thân (thay giọt bắn khỏi thân)
            Every(tHitL, tEnd + tDuoi, 14, x =>
            {
                var o = goc();
                var dv = dich() - o;
                float L = dv.magnitude, s = U(0.15f, 0.95f);
                var u = dv / Mathf.Max(1, L);
                var n = new Vector2(-u.y, u.x);
                float side = U(0, 1) < 0.5f ? -1 : 1;
                var vel = u * U(80, 240) + n * side * U(90, 240) + Len * U(0, 80);
                LVun(o + u * (s * L) + n * side * (0.4f * day), vel, U(0.22f, 0.36f), U(2.4f, 3.6f), U(0, 1) < 0.5f ? he.vun1 : he.vun2,
                    side > 0 ? g : Back);
            });

            // ---- VÒNG GỢN TRÊN ĐẤT ở chân đối thủ (năng lượng dội xuống đất)
            if (!float.IsNaN(gyDich))
                Every(tHitL, tEnd + tDuoi, 5, x =>
                {
                    var h = dich();
                    var p = new Vector2(h.x + U(-0.9f, 0.9f) * day, gyDich + U(-3, 8));
                    float w = U(1.2f, 2.0f) * day;
                    NFbPhat(Floor, 2.1f, p, Vector2.zero, U(0.5f, 0.7f), NFb.ChamDat, w * 0.45f, w, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f, null, 0.8f, pal);
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
                        // chớp tròn + chớp hướng (lõi kem của bảng, 0,12–0,2 s)
                        NFbPhat(g, 6.2f, h - u * (0.1f * day), Vector2.zero, U(0.12f, 0.18f), NFb.ChopTron, 1.3f * day * k, 1.9f * day * k, U(0, 360), 0.3f,
                            0.22f, 0, false, 0, 0, 0, 0, null, 0.8f, pal);
                        if ((ii & 1) == 0)
                            NFbPhat(g, 6.1f, h, Vector2.zero, 0.14f, NFb.ChopHuong, 1.6f * day * k, 2.1f * day * k, U(0, 360), 0.3f, 0.15f, 0, false, 0, 0, 0, 0,
                                null, 0.8f, pal);
                        // gai sắc bắn ngược về phía người bắn + toả hai bên, kéo dài theo hướng bay
                        int m = ii == 0 ? 7 : rng.Next(3, 6);
                        for (int j = 0; j < m; j++)
                        {
                            float an = back + (U(0, 1) < 0.5f ? -1 : 1) * U(15, 80);
                            var dir = NHuong(an);
                            float w = U(0.8f, 1.5f) * day * k;
                            NFbPhat(g, 6.0f, h + dir * (0.2f * day), dir * U(160, 420), U(0.2f, 0.26f), NFb.GaiTrung, w, w * 1.25f, an, 0.32f, -0.05f, 0,
                                false, 0, 3, 0, 0.55f, null, 0.8f, pal);
                        }
                        // toé sao có hướng (WaterLateralImpact: bông gai toé về −x → xoay ngược hướng toé)
                        if (ii < 2 || (ii & 1) == 0)
                        {
                            float an = back + U(-30, 30);
                            var dir = NHuong(an);
                            float w = U(1.5f, 2.1f) * day * k;
                            NFbPhat(g, 5.6f, h + dir * (0.3f * w), dir * U(40, 100), U(0.24f, 0.3f), NFb.ToeNgangC, w * 0.8f, w, an + 180, 0.3f, 0.06f, 0, false,
                                0, 0, 0, 0, null, 0.8f, pal);
                        }
                        // tia vụn bắn ngược (cụm lệch cỡ)
                        LVunCum(h + U2(-4, 4), -u, 1.2f, ii == 0 ? 6 : 3, U(320, 520) * Mathf.Sqrt(k), U(3.4f, 4.6f), U(0, 1) < 0.7f ? g : Back, he.vun1, he.vun2);
                    });
                }
            }

            // ---- TẮT: mảnh xoắn rơi dọc thân lúc đuôi chạy (lá rơi lượn cho Mộc)
            At(tEnd, () =>
            {
                var o = goc();
                var h = dich();
                var dv = h - o;
                float L = dv.magnitude;
                var u = dv / Mathf.Max(1, L);
                for (int j = 0; j < 5; j++)
                {
                    float s = U(0.1f, 0.95f);
                    var p = o + u * (s * L);
                    var v = u * U(40, 160) + new Vector2(U(-60, 60), -U(40, 140));
                    float w = U(1.0f, 1.6f) * day;
                    NFbPhat(g, 4.7f, p, v, U(0.4f, 0.55f), NFb.Xoan, w * 0.7f, w, NAng(u) + U(-40, 40), 0.3f, 0.05f, 0, U(0, 1) < 0.5f, 600, 1.5f, U(-120, 120),
                        0.6f, null, 0.8f, pal);
                }
                if (he.hat == 1 || he.hat == 2)
                    for (int j = 0; j < 2; j++)
                    {
                        var q = LaRoi(o + u * (U(0.2f, 0.8f) * L), u * U(60, 140) + new Vector2(0, -U(20, 50)), U(0.5f, 0.8f), U(3.5f, 5f), g);
                        if (he.hat == 1 && j == 0) q.stops = LaPhong;
                    }
            });
            return tHitL;
        }
    }
}
