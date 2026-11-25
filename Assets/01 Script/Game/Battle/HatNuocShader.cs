// BỘ NƯỚC BẰNG SHADER trong trận (người dùng 2026-11-24 chọn "c": toàn bộ hiệu ứng nước chạy bằng shader thay khung vẽ sẵn, lốc nước
// giữ khung). Học shader repo abitofgamedev/water_vfx; chất nước là bộ nước v2 đã duyệt trong Blender (lam nhạt + bọt trắng, khối cel,
// mép lam sâu, cầu đuôi liền thân, vương miện ngón nước, dải hai ngưỡng) — skill vfx-petclash/blender_anime_fx.md mục 13c.
// Hình vẽ bằng HatNuocFx (một lưới / lớp hạt, shader PokiClash/UIWaterFx); hạt P bình thường của HatLua, hàm draw gọi các hàm N…
// (toạ độ sân, giây sân) thay vì trả Item. Thay ở mức KHỐI DÙNG CHUNG để mọi chiêu nước (và mọi chi tiết riêng từng tướng: gốc tia đo
// trên rig, bề dày theo thân, giờ trúng, nhịp đập) giữ nguyên:
//   thân tia của NTiaKhung (TiaFb DaTiaNuoc) → NTiaShader; Splash → NSplash; Crown → NCrownDat; Puddle → NVung; CauNuoc → NCauShader;
//   Drop → NGiot; Ripple → NRipple.
// Bật khi: NuocShader (tĩnh) + cả ba lớp hạt có HatNuocFx (đã chạy menu NuocFxMenu) + bảng nước đang phát là lam / ngọc lam (mực tím,
// nước lục: hạt cũ). Không có thì các khối tự về bản cũ.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public static bool NuocShader = true;

        readonly HatNuocFx[] nfx = new HatNuocFx[3];
        bool nfxTim;
        static readonly Vector2 SangXY = new Vector2(-0.45f, 0.55f); // phần ngang của hướng sáng trong toạ độ UI (y lên), khớp _Light của shader
        readonly List<Vector2> nPts = new List<Vector2>(128);
        readonly List<float> nHw = new List<float>(128);
        const float NK = StageView.K;
        // ô atlas mặt nạ (ArtGen/Spine/nuoc_shader/tao_texture.py): ngón 0–2, đặc 3/7/11, chấm 4–6, vũng 8–10, loang 12–13, bọt mép 14–15
        const int MNgon = 0, MCham = 4, MVung = 8, MLoang = 12;

        bool NuocShaderOn
        {
            get
            {
                if (!NuocShader) return false;
                if (!nfxTim)
                {
                    nfxTim = true;
                    for (int g = 0; g < 3; g++)
                        if (groups[g]) nfx[g] = groups[g].GetComponentInChildren<HatNuocFx>(true);
                }
                return nfx[0] && nfx[1] && nfx[2];
            }
        }

        // bảng nước đang phát là lam / ngọc lam (shader tô một bảng lam nhạt cố định)
        bool NuocXanh
        {
            get
            {
                var m = W[2];
                return m.g > m.r && m.b > m.r;
            }
        }

        bool NS => NuocShaderOn && NuocXanh;

        void BeginNuocFx()
        {
            if (!nfxTim) return;
            for (int g = 0; g < 3; g++)
                if (nfx[g]) nfx[g].Begin();
        }

        void EndNuocFx()
        {
            if (!nfxTim) return;
            for (int g = 0; g < 3; g++)
                if (nfx[g]) nfx[g].End();
        }

        void ClearNuocFx()
        {
            if (!nfxTim) return;
            for (int g = 0; g < 3; g++)
                if (nfx[g])
                {
                    nfx[g].Begin();
                    nfx[g].End();
                }
        }

        // ================= hình (toạ độ sân, y xuống) =================
        static Color32 NA(float a) => new Color32(255, 255, 255, (byte)Mathf.RoundToInt(Mathf.Clamp01(a) * 255));
        static float NAng(Vector2 dir) => Mathf.Atan2(-dir.y, dir.x) * Mathf.Rad2Deg; // hướng trên sân → độ UI (y lên)
        float NSeed() => U(0, 64);

        void NBall(int g, float layer, Vector2 c, float r, float a = 1, float thr = 0, float wob = 0.07f, float spin = 0.22f, float seed = 0,
            Vector2? dir = null, float sx = 1)
        {
            var f = nfx[g];
            if (!f || r < 0.5f) return;
            f.Ball(layer, StageView.P(c), r * NK, NA(a), thr, wob, spin, T, seed, dir.HasValue ? NAng(dir.Value) : 0, sx);
        }

        void NSprite(int g, float layer, Vector2 c, float w, float h, float angField, int mask, float thr, float band, bool flat, float ns, float a,
            float seed)
        {
            var f = nfx[g];
            if (!f || w < 0.5f) return;
            f.Sprite(layer, StageView.P(c), w * NK, h * NK, -angField, mask, thr, band, flat, ns, NA(a), T, seed);
        }

        void NFan(int g, float layer, Vector2 o, Vector2 axis, float R, float half, float r0, int mask, float tiles, float thr, float a, float seed,
            float squash = 1)
        {
            var f = nfx[g];
            if (!f || R < 0.5f) return;
            f.Fan(layer, StageView.P(o), NAng(axis), R * NK, half, r0, mask, tiles, thr, NA(a), T, seed, squash);
        }

        void NRing(int g, float layer, Vector2 c, float rx, float ry, float r0, int mask, float tiles, float thr, int half, float a, float seed)
        {
            var f = nfx[g];
            if (!f || rx < 0.5f) return;
            f.Ring(layer, StageView.P(c), rx * NK, ry * NK, r0, mask, tiles, thr, half, NA(a), T, seed);
        }

        void NDot(int g, float layer, Vector2 c, float r, int tone, float a = 1, Vector2? vel = null)
        {
            var f = nfx[g];
            if (!f || r < 0.3f) return;
            float sx = 1, ang = 0;
            if (vel.HasValue)
            {
                float sp = vel.Value.magnitude;
                sx = 1 + Mathf.Min(1.3f, sp / 500f);
                if (sp > 1) ang = NAng(vel.Value);
            }
            f.Dot(layer, StageView.P(c), r * NK, tone, NA(a), sx, ang);
        }

        // dải theo nPts (toạ độ sân) với nửa bề rộng nHw (đơn vị sân) đã điền; đổi sang UI tại chỗ
        void NStripFlush(int g, float layer, float head, float tail, float seed, float a = 1, float foam = 0)
        {
            var f = nfx[g];
            if (!f || nPts.Count < 2) return;
            for (int i = 0; i < nPts.Count; i++)
            {
                nPts[i] = StageView.P(nPts[i]);
                nHw[i] *= NK;
            }
            f.Strip(layer, nPts, nHw, NA(a), head, tail, T, seed, SangXY, foam);
        }

        P NP(int g, float life, Action<P, float> draw, Vector2 pos = default)
        {
            var p = new P { pos = pos, life = Mathf.Max(0.02f, life), group = g, seed = rng.Next(1000) };
            p.draw = (q, k, buf) => draw(q, q.age);
            return Add(p);
        }

        // ================= mảnh =================
        // giọt nước tròn (giãn theo vận tốc), rơi theo trọng lực, co dần
        P NGiot(Vector2 pos, Vector2 vel, float r, int g, float life, float grav = 900, float ground = float.NaN, int tone = -1)
        {
            int tn = tone >= 0 ? tone : rng.Next(3) == 0 ? 0 : rng.Next(1, 3);
            var p = new P { pos = pos, vel = vel, acc = new Vector2(0, grav), life = Mathf.Max(0.05f, life), group = g, ground = ground };
            p.draw = (q, k, buf) => NDot(q.group, 6 + k * 0.01f, q.pos, r * (1 - k * k), tn, 1, q.vel);
            return Add(p);
        }

        // chấm toé (sprite cụm chấm mềm): nở 0,6 → 1,1, trôi, tan theo ngưỡng 0,14 → 1 (repo Splash: 0,5 s)
        void NCham(Vector2 c, float s, int g, float life, Vector2 drift, float delay = 0, float layer = 4)
        {
            float sd = NSeed(), ang = U(0, 360);
            int mk = MCham + rng.Next(3);
            Action go = () => NP(g, life, (q, a) =>
            {
                float k = a / life;
                float sc = 0.6f + 0.5f * EaseOut(Mathf.Min(1, k / 0.4f));
                NSprite(g, layer + k * 0.01f, c + drift * EaseOut(k), s * sc, s * sc, ang, mk, 0.14f + 0.86f * k, 0.06f, false, 4, 1, sd);
            });
            if (delay > 0) At(delay, go);
            else go();
        }

        // vương miện ngón nước (quạt): nở 0,3 → 1 trong 0,2 s, ngón mảnh dần rồi đứt thành giọt theo ngưỡng 0,02 → 0,95, viền bọt
        P NVuong(Vector2 o, Vector2 axis, float R, float life, int g, float delay = 0, float half = 0.8f, float layer = 3.5f, float squash = 1)
        {
            float sd = NSeed();
            int mk = MNgon + rng.Next(3);
            axis = axis.sqrMagnitude > 1e-6f ? axis.normalized : new Vector2(0, -1);
            Func<P> go = () => NP(g, life, (q, a) =>
            {
                float k = a / life, rest = Mathf.Max(0.01f, life - 0.2f);
                float grow = a < 0.2f ? 0.3f + 0.7f * EaseOut(a / 0.2f) : 1 + 0.1f * (a - 0.2f) / rest;
                float thr = a < 0.2f ? 0.02f + 0.06f * (a / 0.2f) : 0.08f + 0.87f * (a - 0.2f) / rest;
                NFan(g, layer + k * 0.01f, o, axis, R * grow, half, 0.12f, mk, 2, thr, 1, sd, squash);
            });
            if (delay > 0)
            {
                At(delay, () => go());
                return null;
            }
            return go();
        }

        // vành loang trên đất (elip): nửa sau lớp Sau tướng, nửa trước lớp Trước; mặt nạ mây loang lặp 4,14 quanh vành (số của repo)
        void NVanhDat(Vector2 c, float R, float life, float delay = 0, float r0 = 0.45f, float t0 = 0.11f)
        {
            float sd = NSeed();
            int mk = MLoang + rng.Next(2);
            Action go = () =>
            {
                for (int h = -1; h <= 1; h += 2)
                {
                    int hh = h;
                    NP(hh > 0 ? Front : Back, life, (q, a) =>
                    {
                        float k = a / life;
                        float grow = a < 0.25f ? 0.33f + 0.67f * EaseOut(a / 0.25f) : 1 + 0.12f * k;
                        NRing(q.group, 2 + k * 0.01f, c, R * grow, R * grow * 0.36f, r0, mk, 4.14f, t0 + (1 - t0) * k, hh, 1, sd);
                    });
                }
            };
            if (delay > 0) At(delay, go);
            else go();
        }

        // vũng nước nằm đất (lớp Đất): nở đủ cỡ ở 0,16 s, giữ rồi tan theo ngưỡng (repo Puddle)
        void NVung(Vector2 pos, float R, float life)
        {
            float sd = NSeed(), ang = U(-10, 10);
            int mk = MVung + rng.Next(3);
            NP(Floor, life, (q, a) =>
            {
                float k = a / life;
                float sc = a < 0.16f ? 0.2f + 0.8f * EaseOut(a / 0.16f) : 1 + 0.05f * k;
                float thr = k < 0.35f ? 0.02f + 0.08f * k / 0.35f : 0.1f + 0.9f * (k - 0.35f) / 0.65f;
                NSprite(Floor, 1, pos, 2.6f * R * sc, 1.05f * R * sc, ang, mk, thr, 0.05f, true, 3.5f, 0.92f, sd);
            });
        }

        // gợn vòng trên đất (thay Ripple): vành mảnh nở R0 → R1, tan dần
        P NRipple(Vector2 pos, float R0, float R1, float life)
        {
            float sd = NSeed();
            int mk = MLoang + rng.Next(2);
            P front = null;
            for (int h = -1; h <= 1; h += 2)
            {
                int hh = h;
                var q0 = NP(hh > 0 ? Front : Back, life, (q, a) =>
                {
                    float k = a / life, R = Mathf.Lerp(R0, R1, EaseOut(k));
                    NRing(q.group, 1.5f, pos, R, R * 0.36f, 0.78f, mk, 6, 0.1f + 0.9f * k, hh, 1, sd);
                });
                if (hh > 0) front = q0;
            }
            return front;
        }

        // ================= khối dùng chung =================
        // toé lớn ở thân (thay Splash): chớp kem, 2 vương miện ngửa ngược về phía đòn tới, chấm toé, giọt
        void NSplash(Vector2 c, float sc, float ground, float tH, int g, Vector2? dir)
        {
            if (NuocGoi) // bản 3: flipbook gói mẫu (HatNuocGoi.cs)
            {
                GSplash(c, sc, ground, tH, g, dir);
                return;
            }
            float d = dir.HasValue && Mathf.Abs(dir.Value.x) > 0.01f ? Mathf.Sign(dir.Value.x) : U(0, 1) < 0.5f ? -1 : 1;
            var back = new Vector2(-d, -0.8f).normalized;
            float R = 0.62f * tH * sc;
            float sdc = NSeed();
            NP(g, 0.13f, (q, a) =>
            {
                float s = R * 1.25f * (0.7f + 2.4f * a);
                NSprite(g, 5, c, s, s, 0, MCham, 0.05f + 6 * a, 1, true, 3, 1, sdc); // dải mép = 1: cả chấm tô màu bọt (chớp kem)
            });
            NVuong(c + back * (0.1f * R), back, R, 0.7f, g);
            NVuong(c + new Vector2(0, 0.05f * R), (back + new Vector2(0.35f * d, -0.2f)).normalized, 0.68f * R, 0.62f, g, 0.03f, 0.7f, 3.4f);
            for (int i = 0; i < 6; i++)
            {
                var off = back * (U(0.2f, 0.9f) * R) + new Vector2(U(-0.35f, 0.35f), U(-0.3f, 0.2f)) * R;
                NCham(c + off, U(0.5f, 0.85f) * R, g, U(0.4f, 0.55f), back * (U(0.2f, 0.5f) * R), U(0, 0.12f));
            }
            float sq = Mathf.Sqrt(Mathf.Max(0.2f, sc));
            for (int i = 0; i < 16; i++)
            {
                float an = Mathf.Atan2(back.y, back.x) + U(-1.1f, 1.1f);
                var v = new Vector2(Mathf.Cos(an), Mathf.Sin(an)) * (U(220, 480) * sq);
                NGiot(c + U2(-6, 6), v, U(2.2f, 4.2f) * sq, g, U(0.45f, 0.7f), 900, ground + U(-8, 14));
            }
        }

        // vương miện dưới chân (thay Crown): quạt ngửa lên rộng + vành loang trên đất
        void NCrownDat(Vector2 feet, float wd, float life, int g)
        {
            if (NuocGoi) // bản 3: flipbook gói mẫu
            {
                GCrownDat(feet, wd, life, g);
                return;
            }
            NVuong(feet, new Vector2(0, -1), 0.55f * wd, Mathf.Max(0.35f, life), g, 0, 0.95f, 3.2f, 1.25f);
            NVanhDat(feet, 0.5f * wd, Mathf.Max(0.4f, life));
        }

        // thân tia nước (thay TiaFb DaTiaNuoc trong NTiaKhung, cùng hợp đồng giờ): đầu tia vươn tới đích trong tVuon rồi PHÌNH (vượt cỡ,
        // phập phồng), vệt nước chảy dọc, miệng thon; giữ tBan; đuôi rời miệng tan rách theo ngưỡng đuôi, chạy tới đích với tốc vChay như
        // TiaFb; cầu nước đầu nòng (nongK); đích nở vương miện ngửa ngược + chấm toé mỗi 0,24 s (trungK)
        void NTiaShader(Func<Vector2> goc, Func<Vector2> dich, float day, float tTu, float tBan, int g, float nongK, float trungK)
        {
            var g0 = goc();
            var h0 = dich();
            float dai = Mathf.Max(20, (h0 - g0).magnitude);
            float tVuon = Mathf.Clamp(dai / 2600f, 0.07f, 0.14f);
            float tHitL = tTu + tVuon, tEnd = tHitL + tBan;
            float vChay = Mathf.Max(380, dai / 0.32f), tDuoi = dai / vChay;
            float sd = NSeed();
            NP(g, tEnd + tDuoi + 0.06f, (q, a) =>
            {
                var o = goc();
                var h = dich();
                var dv = h - o;
                float L = Mathf.Max(1, dv.magnitude);
                var u = dv / L;
                var n = new Vector2(-u.y, u.x);
                float head = a < tTu ? -0.1f : Mathf.Min(1.2f, 1.2f * EaseOut((a - tTu) / tVuon));
                float tail = a < tEnd ? -0.3f : -0.06f + 1.25f * Mathf.Clamp01((a - tEnd) / tDuoi);
                float sw = a < tHitL ? 0.35f
                    : a < tHitL + 0.12f ? 0.35f + 0.85f * EaseOut((a - tHitL) / 0.12f)
                    : 1.2f - 0.2f * EaseOut((a - tHitL - 0.12f) / 0.1f);
                sw *= 1 + 0.06f * Mathf.Sin(a * 14);
                if (a > tEnd) sw *= Mathf.Lerp(1, 0.55f, Mathf.Clamp01((a - tEnd) / tDuoi));
                if (head > 0)
                {
                    nPts.Clear();
                    nHw.Clear();
                    int N = Mathf.Clamp(Mathf.RoundToInt(L / 10), 12, 56);
                    for (int i = 0; i <= N; i++)
                    {
                        float s = i / (float)N;
                        float wave = Mathf.Sin(s * Mathf.PI * 3 - a * 10) * 0.2f * day * s * (1 - s);
                        nPts.Add(o + u * (s * L) + n * wave);
                        float neck = 0.55f + 0.45f * Mathf.Clamp01(s * L / (1.2f * day));
                        float puls = 1 + 0.08f * Mathf.Sin(18 * s - 14 * a);
                        nHw.Add(0.5f * day * sw * neck * puls);
                    }
                    NStripFlush(g, 4, head, tail, sd);
                }
                if (nongK > 0 && a < tEnd + 0.06f)
                {
                    float rb = 0.62f * day * nongK * (a < tTu ? 0.25f + 0.75f * EaseOut(a / Mathf.Max(0.01f, tTu)) : 1 + 0.05f * Mathf.Sin(a * 17));
                    if (a > tEnd) rb *= Mathf.Max(0, 1 - (a - tEnd) / 0.06f);
                    NBall(g, 5, o, rb, 1, 0, 0.08f, 0.35f, sd, u);
                }
            });
            if (trungK <= 0) return;
            int nb = Mathf.Max(1, Mathf.CeilToInt((tEnd + tDuoi - tHitL) / 0.24f));
            for (int i = 0; i < nb; i++)
            {
                int ii = i;
                At(tHitL + i * 0.24f, () =>
                {
                    var o = goc();
                    var h = dich();
                    var u = (h - o).normalized;
                    var back = new Vector2(-u.x, -0.85f).normalized;
                    float R = 1.15f * day * trungK * (ii == 0 ? 1.15f : 0.85f);
                    NVuong(h - u * (0.1f * R), back, R, 0.5f, g, 0, 0.75f, 4.5f);
                    for (int j = 0; j < 2; j++)
                        NCham(h + back * (U(0.2f, 0.7f) * R) + U2(-0.25f, 0.25f) * R, U(0.45f, 0.75f) * R, g, U(0.35f, 0.5f), back * (U(0.2f, 0.4f) * R));
                });
            }
        }

        // cầu nước (thay khung cau_nuoc trong CauNuoc, cùng hợp đồng: cFn, rFn theo giây từ lúc gọi, pulse phồng, nén trước tSqz): vòm cầu giả
        // có vệt xoay, rung thạch, mép lam sâu; ĐUÔI LIỀN THÂN là dải theo chính đường bay đã qua (cFn lùi giờ 0,2 s) thon dần, chót rách
        // theo ngưỡng + nhỏ giọt; hết đời cầu vỡ lấm tấm (ngưỡng trên nhiễu mịn)
        P NCauShader(Func<float, Vector2> cFn, float tEnd, Func<float, float> rFn, float[] pulse, float tSqz, int g)
        {
            float sd = NSeed();
            var p = new P { pos = cFn(0), life = tEnd, group = g, seed = rng.Next(1000) };
            float lastDrop = 0;
            p.upd = (q, dt, s) =>
            {
                var np = cFn(q.age);
                q.drift = np - q.pos;
                q.pos = np;
                q.vel = Vector2.zero;
                if (pulse != null) pulse[0] *= Mathf.Exp(-7 * dt);
                float sp = q.drift.magnitude / Mathf.Max(dt, 1e-4f);
                if (sp > 60 && q.age - lastDrop > 0.05f)
                {
                    lastDrop = q.age;
                    var tp = cFn(Mathf.Max(0, q.age - 0.2f));
                    s.NGiot(tp + s.U2(-3, 3), -q.drift.normalized * s.U(30, 90) + new Vector2(0, -s.U(0, 40)), s.U(1.6f, 2.8f), q.group, s.U(0.3f, 0.5f), 500);
                }
            };
            p.draw = (q, k, buf) =>
            {
                float age = q.age, r = rFn(age);
                if (r < 1.5f) return;
                r *= 1 + (pulse != null ? pulse[0] : 0);
                float sx = 1;
                if (tSqz > 0 && age > tSqz - 0.07f && age < tSqz)
                {
                    r *= 0.8f;
                    sx = 1.14f;
                }
                var now = cFn(age);
                var past = cFn(Mathf.Max(0, age - 0.2f));
                float len = (now - past).magnitude;
                Vector2? dir = null;
                if (len > 0.6f * r)
                {
                    nPts.Clear();
                    nHw.Clear();
                    const int M = 12;
                    for (int j = M; j >= 0; j--)
                    {
                        nPts.Add(cFn(Mathf.Max(0, age - 0.2f * j / M)));
                        nHw.Add(r * 0.78f * Mathf.Pow(1 - j / (float)M, 0.9f) + 0.6f);
                    }
                    NStripFlush(q.group, 5.9f, 1.3f, 0.07f, sd);
                    dir = now - past;
                    sx = Mathf.Max(sx, 1 + Mathf.Min(0.18f, len / (6 * r)));
                }
                if (NuocGoi) GCauThem(q, now, past, r, sd); // bản 3: khối nước cuộn kéo sau + lưỡi liềm quay quanh (gói mẫu)
                NBall(q.group, 6, now, r, 1, 0, 0.07f, 0.28f, sd, dir, sx);
            };
            p.onDeath = (q, s) =>
            {
                var c = q.pos;
                float r = rFn(Mathf.Max(0, q.life - 0.01f));
                s.NP(q.group, 0.18f, (z, a) => s.NBall(z.group, 6, c, r * (1 + 0.6f * a), 1, 0.02f + 5.4f * a, 0.1f, 0.3f, sd, null, 1 + a));
            };
            return Add(p);
        }
        // nước trúng nhỏ ở thân (thay khung trung_nuoc): vương miện ngửa ngược theo hướng tới + 2 chấm toé + giọt; trả hạt vương miện
        P NTrung(Vector2 c, float h, Vector2? dir, int g)
        {
            if (NuocGoi) return GTrung(c, h, dir, g); // bản 3: flipbook gói mẫu
            float d = dir.HasValue && Mathf.Abs(dir.Value.x) > 0.01f ? Mathf.Sign(dir.Value.x) : U(0, 1) < 0.5f ? -1 : 1;
            var back = new Vector2(-d, -0.85f).normalized;
            float R = 0.55f * h;
            var p = NVuong(c + back * (0.1f * R), back, R, 0.5f, g);
            for (int i = 0; i < 2; i++)
                NCham(c + back * (U(0.2f, 0.6f) * R) + U2(-0.25f, 0.25f) * R, U(0.4f, 0.65f) * R, g, U(0.35f, 0.5f), back * (U(0.15f, 0.35f) * R));
            for (int i = 0; i < 8; i++)
            {
                float an = Mathf.Atan2(back.y, back.x) + U(-1, 1);
                NGiot(c + U2(-4, 4), new Vector2(Mathf.Cos(an), Mathf.Sin(an)) * U(180, 380), U(1.8f, 3.2f), g, U(0.35f, 0.55f));
            }
            return p;
        }

        // vương miện nước toé từ đất (thay khung nuoc_toe): quạt ngửa lên + vành loang; trả hạt vương miện
        P NToe(Vector2 feet, float h, int g)
        {
            if (NuocGoi) return GToe(feet, h, g); // bản 3: flipbook gói mẫu
            NVanhDat(feet, 0.45f * h, 0.6f);
            return NVuong(feet, new Vector2(0, -1), 0.6f * h, 0.55f, g, 0, 0.95f, 3.2f, 1.2f);
        }

        // mũi thương nước (thay 5 lớp giọt chồng trong NThuong): một dải thon đuôi → phình ở 70 % → mũi nhọn, vệt nước chảy dọc, khi bay đuôi
        // rách theo ngưỡng; giữ nhịp phồng lúc mọc như bản cũ
        void NMuiThuong(P z, float LEN)
        {
            float age = z.age;
            float sc = age < 0.1f ? 1.25f * EaseOut(age / 0.1f) : 1.25f - 0.25f * Mathf.Min(1, (age - 0.1f) / 0.06f);
            var dv = z.fly ? z.vel : z.aim - z.pos;
            var d = dv.sqrMagnitude > 1e-6f ? dv.normalized : Vector2.right;
            float L = LEN * sc * (z.fly ? 1.5f : 1.1f);
            var tip = z.pos + d * (0.35f * L);
            var tl = z.pos - d * (0.75f * L);
            float w0 = 0.16f * LEN * sc;
            nPts.Clear();
            nHw.Clear();
            const int M = 14;
            for (int i = 0; i <= M; i++)
            {
                float s = i / (float)M;
                nPts.Add(Vector2.Lerp(tl, tip, s));
                float w = s < 0.7f ? Mathf.Pow(s / 0.7f, 0.8f) : Mathf.Pow((1 - s) / 0.3f, 0.75f);
                nHw.Add(w0 * Mathf.Max(0.04f, w));
            }
            NStripFlush(z.group, 20, 1.3f, z.fly ? 0.06f : -0.2f, z.span * 7.3f);
        }
        // ================= giai đoạn 2: mạch phun, sóng =================
        // mạch phun bằng shader (thay toàn bộ NXoay, cùng giờ: xoáy dưới đất trong lúc tụ, phụt ở T1, trả T1): vành gợn co về tâm + giọt sủi;
        // tới T1 cột nước dựng từ chân đối thủ (đầu cột lên đỉnh 0,12 s, phình, phập phồng, 0,42–0,66 s sụp từ trên xuống), vương miện ngửa
        // ở đỉnh và chân, giọt rơi quanh cột, nước húc từ dưới lên thân, vành loang + vũng
        float NXoayShader(Vector2 foeFeet, float tH, float lead)
        {
            var Cc = foeFeet + new Vector2(0, 4);
            float T1 = Mathf.Max(0.45f, lead + 0.08f);
            for (int i = 0; i < 3; i++)
            {
                float d0 = i * Mathf.Max(0.05f, T1 / 3.2f);
                At(d0, () => NRipple(Cc, 0.95f * tH, 0.3f * tH, Mathf.Max(0.25f, T1 - d0)));
            }
            Every(0.05f, T1, 14, x => NGiot(Cc + new Vector2(U(-0.5f, 0.5f) * tH, U(-4, 4)), new Vector2(U(-40, 40), -U(60, 160)), U(1.6f, 2.6f), Front,
                U(0.3f, 0.5f), 600, Cc.y + U(-4, 6)));
            At(0.1f, () => Shake?.Invoke(0.15f));
            At(T1, () =>
            {
                Shake?.Invoke(0.65f);
                FlashScreen?.Invoke(FlashW);
                NVanhDat(Cc, 0.75f * tH, 0.7f);
                NVung(Cc + new Vector2(0, 2), 0.42f * tH, 1.4f);
                float sd = NSeed(), H = 1.55f * tH, W0 = 0.22f * tH;
                NP(Front, 0.7f, (q, a) =>
                {
                    float head = a < 0.12f ? 1.2f * EaseOut(a / 0.12f) : a < 0.42f ? 1.2f : 1.2f - 1.3f * Mathf.Clamp01((a - 0.42f) / 0.24f);
                    if (head < 0.02f) return;
                    float sw = a < 0.15f ? 0.5f + 0.7f * EaseOut(a / 0.15f) : 1.2f - 0.2f * EaseOut((a - 0.15f) / 0.1f);
                    sw *= 1 + 0.07f * Mathf.Sin(a * 20);
                    nPts.Clear();
                    nHw.Clear();
                    const int M = 24;
                    for (int i = 0; i <= M; i++)
                    {
                        float s = i / (float)M;
                        nPts.Add(Cc + new Vector2(0.06f * tH * Mathf.Sin(s * 5 - a * 9) * s, -H * s));
                        nHw.Add(W0 * sw * (1 - 0.3f * s) * (0.8f + 0.2f * Mathf.Clamp01(s / 0.06f)));
                    }
                    NStripFlush(Front, 3, head, -0.3f, sd);
                });
                NVuong(Cc + new Vector2(0, -H * 0.95f), new Vector2(0, -1), 0.75f * tH, 0.5f, Front, 0.08f, 1.0f, 4, 1.15f);
                NVuong(Cc + new Vector2(0, -H * 0.9f), new Vector2(0, -1), 0.55f * tH, 0.45f, Front, 0.3f, 0.9f, 4.1f);
                NVuong(Cc, new Vector2(0, -1), 0.6f * tH, 0.5f, Front, 0, 0.95f, 3.2f, 1.3f);
                Every(0.08f, 0.6f, 40, x =>
                {
                    float an = U(-2.6f, -0.5f);
                    NGiot(Cc + new Vector2(U(-0.15f, 0.15f) * tH, -H * U(0.75f, 1f)), new Vector2(Mathf.Cos(an), Mathf.Sin(an)) * U(120, 320), U(2, 3.6f),
                        U(0, 1) < 0.3f ? Back : Front, U(0.5f, 0.8f), 900, Cc.y + U(-6, 10));
                });
                NTrung(foeFeet + new Vector2(0, -0.45f * tH), 0.9f * tH, new Vector2(0, -1), Front);
                if (NuocGoi) GCotPhun(Cc, tH); // bản 3: cột nước dựng flipbook của gói
            });
            return T1;
        }

        static readonly Vector2[] NSongK = // mặt cắt sóng (x theo hướng sóng × bề ngang, y lên × cao): chân sau → lưng → đỉnh → mào → mũi quặp
            { new Vector2(-1.05f, 0.18f), new Vector2(-0.55f, 0.42f), new Vector2(-0.12f, 0.8f), new Vector2(0.12f, 1.0f), new Vector2(0.38f, 0.94f),
                new Vector2(0.5f, 0.74f), new Vector2(0.42f, 0.56f) };

        static Vector2 NCR(Vector2 p0, Vector2 p1, Vector2 p2, Vector2 p3, float u) =>
            0.5f * (2 * p1 + (p2 - p0) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * (u * u) + (3 * p1 - p0 - 3 * p2 + p3) * (u * u * u));

        // thân sóng bằng shader (thay đa giác HatMang + bọt viền mực trong NSong): dải dày theo mặt cắt NSongK, thon dần về mũi mào, vệt nước
        // chảy dọc; dải BỌT rách phủ phần mào; khi đổ (fall 1 → 0) tan từ chân lên. c: chân trước của sóng, sx: hướng sóng (±1)
        void NSongVe(Vector2 c, float hg, float wd, float sx, float t, float fall, float seed)
        {
            nPts.Clear();
            nHw.Clear();
            int nk = NSongK.Length;
            Vector2 K(int i)
            {
                i = Mathf.Clamp(i, 0, nk - 1);
                var p = NSongK[i];
                if (i >= 2) p.y += 0.03f * Mathf.Sin(t * 11 + i * 1.7f);
                return c + new Vector2(sx * p.x * wd, -p.y * hg);
            }
            const int per = 7;
            int tot = (nk - 1) * per;
            for (int j = 0; j <= tot; j++)
            {
                int seg = Mathf.Min(nk - 2, j / per);
                float u = j / (float)per - seg;
                nPts.Add(NCR(K(seg - 1), K(seg), K(seg + 1), K(seg + 2), u));
                float s = j / (float)tot;
                nHw.Add(hg * (0.24f * Mathf.Pow(1 - s, 0.6f) + 0.03f));
            }
            float tail = (1 - fall) * 1.15f - 0.05f;
            // bọt: phần mào (s ≥ 0,55), hẹp hơn thân — sao chép trước khi NStripFlush đổi toạ độ
            int f0 = Mathf.RoundToInt(tot * 0.55f);
            var fp = new List<Vector2>(tot - f0 + 1);
            var fw = new List<float>(tot - f0 + 1);
            for (int j = f0; j <= tot; j++)
            {
                fp.Add(nPts[j]);
                fw.Add(nHw[j] * 0.62f);
            }
            NStripFlush(Front, 22, 1.25f, tail, seed);
            nPts.Clear();
            nHw.Clear();
            nPts.AddRange(fp);
            nHw.AddRange(fw);
            NStripFlush(Front, 22.5f, 1.25f, tail, seed + 3.1f, 1, 0.78f);
        }

        // sóng đổ tới đích (thay khung song_nuoc): toé lớn ở thân theo hướng sóng, vương miện lớn dưới chân, vành loang, vũng
        void NSongDo(Vector2 foeFeet, float tH, float sx)
        {
            if (NuocGoi) GSongDo(foeFeet, tH, sx); // bản 3: gai + chớp + vệt trượt của gói
            var body = foeFeet + new Vector2(0, -0.5f * tH);
            NSplash(body, 1.45f, foeFeet.y, tH, Front, new Vector2(sx, 0));
            NVuong(foeFeet + new Vector2(sx * 0.1f * tH, 0), new Vector2(sx * 0.5f, -1), 0.95f * tH, 0.6f, Front, 0.02f, 1.0f, 3.6f, 1.2f);
            NVanhDat(foeFeet, 0.85f * tH, 0.8f);
            NVung(foeFeet + new Vector2(0, 3), 0.5f * tH, 1.5f);
        }
        // ================= giai đoạn 3 (người dùng 2026-11-25: "update nốt các vfx thủy mới vào đi"): khối cũ còn viền mực → shader =================
        // lưỡi nước bay (thay Wave): dải thon theo hướng bay (đầu dày, đuôi nhọn), dài theo tốc, tan từ đuôi theo tuổi; giữ vật lý của Wave
        P NLuoiNuoc(Vector2 pos, Vector2 vel, float life, float r0, float r1, int g, float drag, float accY)
        {
            var p = new P { pos = pos, vel = vel, life = Mathf.Max(0.05f, life), drag = drag, acc = new Vector2(0, accY), group = g, seed = rng.Next(1000) };
            float sd = NSeed();
            p.draw = (q, k, buf) =>
            {
                float sp = q.vel.magnitude;
                var d = sp > 5 ? q.vel / sp : new Vector2(0, -1);
                float r = Mathf.Lerp(r0, r1, k) * (1 - k * k * k);
                if (r < 0.8f) return;
                float len = r * 2.2f + Mathf.Min(60, sp * 0.03f);
                var head = q.pos + d * (0.3f * len);
                var tl = q.pos - d * len;
                nPts.Clear();
                nHw.Clear();
                const int M = 8;
                for (int i = 0; i <= M; i++)
                {
                    float s = i / (float)M;
                    nPts.Add(Vector2.Lerp(tl, head, s));
                    float w = s < 0.75f ? Mathf.Pow(s / 0.75f, 0.7f) : Mathf.Pow((1 - s) / 0.25f, 0.5f);
                    nHw.Add(0.55f * r * Mathf.Max(0.05f, w));
                }
                NStripFlush(q.group, 5 + k * 0.01f, 1.3f, -0.2f + 1.1f * k * k, sd);
            };
            return Add(p);
        }

        // cụm bọt (thay BotCum): 3 chấm bọt trắng chồng lệch cỡ, trôi theo vận tốc (hơi nước: bay lên), co dần
        P NBotCum(Vector2 pos, Vector2? vel, float r, int g, float life, bool hoi)
        {
            var p = new P
            {
                pos = pos, vel = vel ?? new Vector2(U(-20, 20), -U(10, 40)), life = life > 0 ? life : U(0.45f, 0.65f), drag = 2.5f,
                acc = new Vector2(0, hoi ? -60 : 120), group = g, seed = rng.Next(1000)
            };
            var off = new[] { new Vector2(0, 0), new Vector2(U(0.45f, 0.7f), U(-0.3f, 0.1f)), new Vector2(-U(0.4f, 0.65f), U(-0.15f, 0.2f)) };
            var rs = new[] { 1f, U(0.55f, 0.75f), U(0.5f, 0.7f) };
            p.draw = (q, k, buf) =>
            {
                float sc = (k < 0.2f ? 0.5f + 0.5f * EaseOut(k / 0.2f) : 1) * (1 - k * k);
                for (int i = 0; i < 3; i++) NDot(q.group, 5.5f + i * 0.001f, q.pos + off[i] * (r * sc), r * rs[i] * sc, 2);
            };
            return Add(p);
        }

        // khối nước văng (thay Khoi): cục nước nhỏ có khối, rơi, cuối đời tan lấm tấm; giữ vật lý của Khoi
        P NKhoi(Vector2 pos, Vector2 vel, float life, float r, int g)
        {
            var p = new P { pos = pos, vel = vel, life = Mathf.Max(0.05f, life), drag = 5.5f, acc = new Vector2(0, 420), group = g, seed = rng.Next(1000) };
            float sd = NSeed();
            p.draw = (q, k, buf) =>
            {
                float rr = r * 1.15f * (1 - 0.5f * k * k);
                NBall(q.group, 5.5f, q.pos, rr, 1, k > 0.55f ? (k - 0.55f) / 0.45f : 0, 0.1f, 0.4f, sd, q.vel.sqrMagnitude > 1 ? q.vel : (Vector2?)null,
                    1 + Mathf.Min(0.25f, q.vel.magnitude / 1600));
            };
            return Add(p);
        }

        // vệt nước bị hút xoắn vào đầu nòng (thay nét PutVet trong Gather): dải thon theo vận tốc, hiện dần
        void NGatherVe(P z, float k, float sp)
        {
            float g = Mathf.Min(1, k / 0.25f);
            float th = z.sz * (0.55f + 0.45f * g), len = th * Mathf.Clamp(sp / 110, 1.8f, 5);
            var d = z.vel / sp;
            nPts.Clear();
            nHw.Clear();
            const int M = 6;
            for (int i = 0; i <= M; i++)
            {
                float s = i / (float)M;
                nPts.Add(z.pos - d * (len * (1 - s)));
                nHw.Add(0.5f * th * Mathf.Max(0.08f, Mathf.Pow(s, 0.8f)) * (s > 0.85f ? (1 - s) / 0.15f * 0.6f + 0.4f : 1));
            }
            NStripFlush(z.group, 4.5f, 1.3f, -0.2f, z.seed * 3.3f, g, z.big ? 0.62f : 0);
        }
    }
}
