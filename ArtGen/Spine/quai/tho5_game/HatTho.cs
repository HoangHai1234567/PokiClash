// Bộ THỔ (2026-11-17): năm tướng đầu đảo Thổ, vẽ lại trên rig Sword x Staff (ArtGen/Spine/<mã>_rig.py; ghi chú
// ArtGen/Spine/inbox/tho5_ghichu.md; bản xem trước Python ArtGen/Spine/tho5_fx.py). Người dùng 2026-11-17: "cho vào game đi".
// Giữ id tướng, thẻ, chỉ số; đổi hình:
//   ải 1  thach_nhan = Thạch Giáp (tatu mai đá hổ phách, rig cong_da_1)
//   ải 5  lung_vuong = Sa Tích    (thằn lằn áo choàng phiến đất nung, rig than_lan_cat_1)
//   ải 10 cao_da     = Tê Thiềm   (cóc tê giác đất nung, rig thu_da_1)
//   ải 15 ho_khoan   = Sa Long    (rồng giáp sa thạch, rig rong_cat_1)
//   ải 20 phu_van    = Sơn Viên   (vượn núi đá bốn tay, rig quy_nui_1)
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip). Mọi mốc dưới đây là mốc của
// rig (giây clip), co giãn theo lead / khung trúng của rig. Lớp hạt không đọc được xương nên chỗ miệng, vuốt, tay, mai đo sẵn trên rig
// (đơn vị chiều cao dáng đứng; x về phía đối thủ, y lên) theo giờ clip.
// Hình hệ Thổ (skill-petclash mục 5): khối đá góc cạnh, trồi lên, rơi nặng, nảy một lần rồi nằm; bụi tròn nâu be; sỏi. Không dùng ảnh
// đá, vết nứt có mạch dung nham của bộ Hỏa (hat_rock_*, hat_crack_*), không dùng chớp nước BurstFlash (bảng W là màu nước): chớp trúng
// là sao gai màu kem. Thân khối lớn (lưỡi cát, lốc cát, cột sa thạch, gai sóng chấn, vết nứt) là mảng liền (MSolid / MFill); hạt chỉ
// làm mép, bụi, dăm. Rung lúc trúng do rig khai (impactShake); ở đây chỉ rung cho nhịp không phải khung trúng (dậm, nện, đáp).
// DẠNG 2 (2026-11-17, rig riêng mỗi dạng; quai/doi_tho5_dang2.py): Thạch Giáp cong_da_2 (3528), Sa Tích than_lan_cat_2 (3530), Tê Thiềm
// thu_da_2 (3526); Sa Long thêm DẠNG 1 rong_cat_non (3529), dạng 2 là rig rong_cat_1 cũ. Mã dạng 2: n_*2 (hàm cũ thêm tham số dang, mốc
// và bảng vị trí đo trên rig dạng 2 ở inbox/<mã>_2_ghichu.md); Sa Long dạng 1: n_long_*1. Thang cỡ dạng 1 < dạng 2 (skill-petclash mục 6).
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color ToBuiC = C(176, 148, 110), ToBuiC2 = C(146, 118, 86);                       // bụi đất: be, nâu
        static readonly Color ToDa = C(150, 136, 118), ToDa2 = C(118, 104, 90), ToDa3 = C(184, 170, 150);  // đá xám nâu: giữa, sẫm, sáng
        static readonly Color ToPhach = C(240, 166, 46), ToPhach2 = C(255, 210, 112);                      // pha lê hổ phách: mặt chính, mặt sáng
        static readonly Color ToGom = C(184, 98, 58), ToGom2 = C(214, 140, 90);                            // đất nung (áo phiến Sa Tích)
        static readonly Color ToCat = C(222, 192, 138), ToCat2 = C(196, 160, 104), ToCat3 = C(240, 222, 182), ToCatSam = C(168, 124, 70);
        static readonly Color ToSaThach = C(230, 206, 156), ToSon = C(196, 134, 70), ToNutC = C(70, 50, 34);
        static readonly Color ToKem = C(255, 246, 214);                                                    // chớp trúng

        // ================= vật liệu chung =================

        // điểm đo trên rig theo giờ clip (bước dt từ t0), nội suy thẳng
        static Vector2 ToDiem(Vector2[] bang, float t0, float dt, float t)
        {
            float f = Mathf.Clamp((t - t0) / dt, 0, bang.Length - 1.001f);
            int i = (int)f;
            return Vector2.Lerp(bang[i], bang[Mathf.Min(bang.Length - 1, i + 1)], f - i);
        }

        // điểm đo (đơn vị chiều cao, x về phía đối thủ, y lên) → toạ độ sân (y xuống)
        static Vector2 ToSan(Vector2 feet, float H, float dir, Vector2 u) => feet + new Vector2(dir * u.x * H, -u.y * H);

        // cụm bụi đất (Bui nhuộm be / nâu)
        P ToBui(Vector2 pos, Vector2 vel, float life = 0, float r0 = 5, float r1 = 14, int group = Front)
        {
            var b = Bui(pos, vel, life, r0, r1, group);
            b.col = (b.seed & 4) != 0 ? ToBuiC2 : ToBuiC;
            return b;
        }

        // hình sỏi: khối tròn méo viền mực, dẹt theo hgt, mờ ở 30% cuối đời
        void DrawSoiP(P q, float k, List<Item> buf)
        {
            float a = 1 - SmoothStep(0.7f, 1, k);
            if (q.sz < 0.8f || a < 0.03f) return;
            int si = q.seed & 3;
            Put(buf, q.group, 45, S("solid_" + si), Ink, q.pos, 2 * q.sz + 3.5f, q.hgt, q.ang, a);
            Put(buf, q.group, 45.1f, S("blob_" + si), q.col, q.pos, 2 * q.sz, q.hgt, q.ang, a);
        }

        // sỏi / dăm đá văng: rơi có trọng lực, chạm đất nảy một lần rồi nằm, mờ dần
        P ToSoi(Vector2 pos, Vector2 vel, float r, Color col, float ground, float life = 0, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life > 0 ? life : U(0.6f, 0.9f), acc = new Vector2(0, 900), drag = 0.6f, spin = U(-800, 800),
                spinDrag = 0.4f, ang = U(0, 360), seed = rng.Next(4), sz = r, col = col, group = group, ground = ground, bounce = 0.35f,
                hgt = U(1.0f, 1.45f)
            };
            p.draw = DrawSoiP;
            return Add(p);
        }

        // chớp trúng: sao gai kem viền mực, lõi hổ phách nhạt, 0,12 s
        void ToChop(Vector2 c, float size, int group = Front, float life = 0.12f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = rng.Next(4), sz = size };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (0.7f + 0.4f * EaseOut(k / 0.5f));
                Put(buf, q.group, 60, S("bursts_" + q.seed), Ink, q.pos, s + 5, 1, q.ang);
                Put(buf, q.group, 60.1f, S("burst_" + q.seed), ToKem, q.pos, s, 1, q.ang);
                Put(buf, q.group, 60.2f, S("burst_" + ((q.seed + 1) & 3)), ToPhach2, q.pos, 0.42f * s, 1, q.ang + 20);
            };
            Add(p);
        }

        // vòng bụi dưới đất (elip ở lớp đất)
        void ToVong(Vector2 feet, float R1, float life = 0.45f) => Ring(feet + new Vector2(0, 2), life, 0.25f * R1, R1, ToCat3, 0.3f, Floor, 30.4f);

        // một cú trúng hệ Thổ: chớp sao kem, dăm văng đều nửa trên quanh tâm rồi rơi nảy, bụi tròn. muc: 1 vừa, 2 nặng; c1, c2: màu dăm
        void ToNo(Vector2 c, float ground, float tH, float muc, Color c1, Color c2)
        {
            float sc = tH / 150f;
            ToChop(c, 0.26f * tH * Mathf.Sqrt(muc));
            int n = Mathf.RoundToInt(6 * muc);
            for (int i = 0; i < n; i++)
            {
                float a = -Mathf.PI / 2 + ((i + 0.5f) / n - 0.5f) * 2.6f + U(-0.2f, 0.2f);
                var v = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * (U(150, 260) * (0.8f + 0.25f * muc) * sc);
                ToSoi(c, v, U(3.5f, 6.5f) * (0.8f + 0.2f * muc) * sc, i % 3 == 0 ? c2 : c1, ground + U(-4, 6) * sc, 0, (i & 1) == 0 ? Front : Back);
            }
            for (int i = 0; i < Mathf.RoundToInt(3 * muc); i++)
                ToBui(c + U2(-10, 10) * sc, new Vector2(U(-60, 60), U(-50, -10)) * sc, 0, 6 * muc * sc, 16 * muc * sc, (i & 1) == 0 ? Front : Back);
        }

        // hạt bị hút vào một điểm đang dời (miệng, vuốt, tảng đá trên tay): sỏi / cục cát nhỏ đi theo f^mu tới đích
        void ToHut(Vector2 p0, Func<float, Vector2> dich, float life, float r, Color col, float mu, float vong = 0)
        {
            var q = new P { pos = p0, home = p0, life = life, group = Front, seed = rng.Next(4), sz = r, col = col, spin = U(-600, 600), hgt = U(1, 1.3f) };
            q.upd = (z, dt, s) =>
            {
                float f = z.age / z.life;
                z.pos = z.home + (dich(s.T) - z.home) * Mathf.Pow(f, mu) + new Vector2(0, -vong * Mathf.Sin(Mathf.PI * f));
                z.vel = Vector2.zero;
            };
            q.draw = DrawSoiP;
            Add(q);
        }

        // mảnh pha lê hổ phách: giọt nhọn chĩa theo hướng bay, một dải mặt sáng. yCham: chạm mức này thì gọi trung rồi tắt
        P ToPhaLe(Vector2 pos, Vector2 vel, float len, float wd, float life, float yCham = float.NaN, Action<Vector2> trung = null)
        {
            var p = new P { pos = pos, vel = vel, life = life, sz = len, wd = wd, group = Front, R0 = yCham };
            p.upd = (q, dt, s) =>
            {
                if (!float.IsNaN(q.R0) && q.pos.y >= q.R0 && !q.dead)
                {
                    q.dead = true;
                    trung?.Invoke(q.pos);
                }
            };
            p.draw = (q, k, buf) => DrawPhaLe(buf, q.group, q.pos, Unit(q.vel), q.sz, q.wd);
            return Add(p);
        }

        void DrawPhaLe(List<Item> buf, int g, Vector2 pos, Vector2 d, float len, float wd)
        {
            float ang = TipAngle(d);
            var n = new Vector2(-d.y, d.x);
            Put(buf, g, 47, S("needles_0"), Ink, pos, len + 5, (wd + 5) / (len + 5), ang);
            Put(buf, g, 47.1f, S("needle_0"), ToPhach, pos, len, wd / len, ang);
            Put(buf, g, 47.2f, S("needle_0"), ToPhach2, pos + n * (0.18f * wd) + d * (0.05f * len), 0.72f * len, 0.32f * wd / (0.72f * len), ang);
        }

        // tảng đá: bốn khối tròn méo chồng nhau viền mực (đá giữa, sẫm, sáng) + mạch hổ phách chéo (crust); ang theo độ
        void DrawTang(P q, float k, List<Item> buf)
        {
            float r = q.sz;
            if (r < 1.2f) return;
            int sd = q.seed & 3, g = q.group;
            float a = q.ang, rad = -a * Mathf.Deg2Rad, cs = Mathf.Cos(rad), sn = Mathf.Sin(rad);
            float ink = Mathf.Min(4.5f, 2.2f + r * 0.08f);
            for (int i = 0; i < 4; i++)
            {
                var u = ThachU[i];
                var c = q.pos + new Vector2(u.x * cs - u.y * sn, u.x * sn + u.y * cs) * r;
                float d = 2 * r * u.z;
                int si = (sd + i) & 3;
                Put(buf, g, q.ph, S("solid_" + si), Ink, c, d + ink, 1, a + i * 50);
                Put(buf, g, q.ph + 0.1f + i * 0.02f, S("blob_" + si), i == 1 ? ToDa2 : i == 3 ? ToDa3 : ToDa, c, d, 1, a + i * 50);
            }
            if (!q.crust || r < 6) return;
            var m = q.pos + new Vector2(0.12f * cs, 0.12f * sn) * r;
            Put(buf, g, q.ph + 0.3f, S("needles_0"), Ink, m, 1.15f * r + ink, (0.24f * r + ink) / (1.15f * r + ink), a + 64);
            Put(buf, g, q.ph + 0.4f, S("needle_0"), ToPhach, m, 1.15f * r, 0.24f / 1.15f, a + 64);
        }

        // tảng đá bay vồng từ a tới b trong tb giây, xoay, kéo vệt bụi; tới nơi gọi trung(b). co1: cỡ lúc tới so với lúc rời
        void ToTangBay(Vector2 a, Vector2 b, float tb, float r, float vong, bool phach, Action<Vector2> trung, float co1 = 1, int seed = -1)
        {
            var n = new Vector2(-(b - a).y, (b - a).x).normalized;
            if (n.y > 0) n = -n;
            float t0 = T;
            var p = new P
            {
                pos = a, life = tb, group = Front, sz = r, seed = seed >= 0 ? seed : rng.Next(4), crust = phach, ph = 44,
                spin = (b.x > a.x ? 1 : -1) * 420
            };
            p.upd = (q, dt, s) =>
            {
                float f = Mathf.Clamp01((s.T - t0) / tb);
                q.pos = Vector2.Lerp(a, b, f) + n * (vong * Mathf.Sin(Mathf.PI * f));
                q.vel = Vector2.zero;
                q.sz = r * Mathf.Lerp(1, co1, f);
                if (s.U(0, 1) < 0.12f) ToBui(q.pos, new Vector2(s.U(-20, 20), s.U(-20, 0)), 0.35f, 0.25f * r, 0.6f * r);
            };
            p.draw = DrawTang;
            p.onDeath = (q, s) => trung?.Invoke(b);
            Add(p);
        }

        // lưỡi cát trăng khuyết (mảng liền viền mực, dải sáng ở mép trước) bay thẳng a → b trong tb giây, bụi rơi lại phía sau
        void ToLuoiCat(Vector2 a, Vector2 b, float tb, float R, Action<Vector2> trung)
        {
            var d = Unit(b - a);
            var ax = new Vector2(-d.y, d.x);
            var p = new P { pos = a, vel = (b - a) / tb, life = tb, group = Front, sz = R };
            p.upd = (q, dt, s) =>
            {
                if (s.U(0, 1) < 0.15f) ToBui(q.pos - d * (q.sz * 0.5f) + s.U2(-6, 6), new Vector2(s.U(-20, 20), -10), 0.3f, 3, 8);
            };
            p.draw = (q, k, buf) =>
            {
                const int n = 11, N = 2 * n - 2;
                MSolid(Front, 26, Crescent(q.pos, d, ax, q.sz, 1f, 0.42f, 1.15f, n), N, ToCat, 1, 2.4f);
                MFill(Front, 26.01f, Crescent(q.pos, d, ax, q.sz, 0.92f, 0.74f, 0.95f, n), N, ToCat3, 1, false);
            };
            p.onDeath = (q, s) => trung?.Invoke(b);
            Add(p);
        }

        // cột sa thạch trồi từ đất (đáy bám đất, đỉnh vỡ xiên, hai vạch son trồi theo), giữ rồi lún; bụi, dăm ở chân
        void ToCot(Vector2 chan, float w, float h, float giu, int group, float sc)
        {
            const float tLen = 0.12f, tLun = 0.25f;
            var p = new P { pos = chan, life = tLen + giu + tLun, group = group, sz = h, wd = w, hgt = U(-0.25f, 0.25f) * w };
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                float hh = q.sz * (t < tLen ? Mathf.Sqrt(t / tLen) : t < tLen + giu ? 1 : Mathf.Max(0, 1 - (t - tLen - giu) / tLun));
                if (hh < 2) return;
                float hw = q.wd / 2, nn = q.hgt;
                int s0 = mp.Count;
                mp.Add(q.pos + new Vector2(-hw, 0));
                mp.Add(q.pos + new Vector2(-hw, -hh + nn * 0.5f));
                mp.Add(q.pos + new Vector2(0, -hh - Mathf.Abs(nn) * 0.4f));
                mp.Add(q.pos + new Vector2(hw, -hh - nn * 0.5f));
                mp.Add(q.pos + new Vector2(hw, 0));
                MSolid(q.group, 24, s0, 5, ToSaThach, 1, 2.6f);
                float bd = Mathf.Max(3, 0.12f * q.wd);
                for (int j = 0; j < 2; j++)
                {
                    float y = -hh + q.sz * (j == 0 ? 0.65f : 0.32f);           // vạch son trồi theo thân cột
                    if (y > -bd - 2) continue;
                    int s1 = mp.Count;
                    mp.Add(q.pos + new Vector2(-hw + 2, y));
                    mp.Add(q.pos + new Vector2(hw - 2, y - bd * 0.5f));
                    mp.Add(q.pos + new Vector2(hw - 2, y + bd * 0.6f));
                    mp.Add(q.pos + new Vector2(-hw + 2, y + bd));
                    MFill(q.group, 24.01f + j * 0.001f, s1, 4, ToSon, 1, false);
                }
            };
            Add(p);
            for (int i = 0; i < 4; i++)
                ToBui(chan + new Vector2(U(-0.6f, 0.6f) * w, -2), new Vector2(U(-70, 70), U(-50, -10)) * sc, 0.6f, 6 * sc, 15 * sc, (i & 1) == 0 ? Front : Back);
            for (int i = 0; i < 5; i++)
                ToSoi(chan + new Vector2(U(-0.4f, 0.4f) * w, -4), new Vector2(U(-160, 160), U(-300, -150)) * sc, U(3, 5) * sc,
                    i % 2 == 0 ? ToCat2 : ToSaThach, chan.y + 2, 0, (i & 1) == 0 ? Front : Back);
        }

        // vết nứt đất: dải nâu sẫm gấp khúc lan từ a tới b trong tLan giây, nằm 0,5 s rồi mờ
        void ToNut(Vector2 a, Vector2 b, float tLan, float sc)
        {
            const int n = 12;
            var pts = new Vector2[n + 1];
            for (int i = 0; i <= n; i++)
                pts[i] = Vector2.Lerp(a, b, (float)i / n) + (i > 0 && i < n ? new Vector2(0, U(-5, 5) * sc) : Vector2.zero);
            var p = new P { pos = a, life = tLan + 0.9f, group = Floor };
            p.draw = (q, k, buf) =>
            {
                int m = Mathf.Min(n, (int)(n * Mathf.Min(1, q.age / tLan)) + 1);
                float al = 1 - Mathf.Max(0, (q.age - tLan - 0.5f) / 0.4f);
                for (int i = 0; i < m; i++)
                {
                    Vector2 p0 = pts[i], p1 = pts[i + 1], e = p1 - p0;
                    var nn = new Vector2(-e.y, e.x).normalized * (2.4f * sc);
                    int s0 = mp.Count;
                    mp.Add(p0 + nn);
                    mp.Add(p1 + nn);
                    mp.Add(p1 - nn);
                    mp.Add(p0 - nn);
                    MFill(Floor, 5, s0, 4, ToNutC, al, true);
                }
            };
            Add(p);
        }

        // lốc cát trùm đối thủ (mảng liền trong mờ, viền mực): thân phễu cát, sáu dải xoáy chéo sẫm / sáng chạy lên, miệng loe; nở 0,25 s
        // đầu, tan 0,35 s cuối; mảnh đất nung bay quanh, bụi tràn miệng và chân phễu. Khối lớn phủ lên đối thủ nên trong mờ 0,82.
        void ToLocCat(Vector2 chan, float cao, float t0, float t1, float sc)
        {
            float dur = t1 - t0;
            Func<float, float, float> bk = (u, mo) => 1.35f * (12 + 28 * u + 30 * u * u * u) * (0.35f + 0.65f * mo) * sc;   // miệng phễu loe; rộng hơn bản xem trước 35 % (2026-11-17, soi trong game: hẹp hơn thân đối thủ to)
            Func<float, float, float> lac = (a, u) => 7 * sc * Mathf.Sin(a * 8 + u * 4.5f) * u;
            At(t0, () =>
            {
                var p = new P { pos = chan, life = dur, group = Front };
                p.draw = (q, k, buf) =>
                {
                    float a = q.age;
                    float mo = Mathf.Min(1, a / 0.25f) * Mathf.Min(1, (dur - a) / 0.35f);
                    if (mo <= 0.01f) return;
                    float h = cao * (0.3f + 0.7f * Mathf.Min(1, a / 0.25f));
                    const int M = 11;
                    const float Al = 0.82f;
                    int s0 = mp.Count;
                    for (int j = 0; j < M; j++)
                    {
                        float u = j / (M - 1f);
                        mp.Add(new Vector2(q.pos.x - bk(u, mo) + lac(a, u), q.pos.y - u * h));
                    }
                    for (int j = M - 1; j >= 0; j--)
                    {
                        float u = j / (M - 1f);
                        mp.Add(new Vector2(q.pos.x + bk(u, mo) + lac(a, u), q.pos.y - u * h));
                    }
                    MSolid(Front, 22, s0, 2 * M, ToCat, Al * mo, 2.2f);
                    for (int i = 0; i < 6; i++)                                   // dải xoáy chéo chạy lên
                    {
                        float v = (a * 1.7f + i / 6f) % 1f;
                        if (v < 0.08f || v > 0.94f) continue;
                        float u0 = Mathf.Max(0.02f, v - 0.05f), u1 = Mathf.Min(0.98f, v + 0.03f);
                        float ra = bk(u0, mo) * 0.92f, rb = bk(u1, mo) * 0.92f;
                        float ya = q.pos.y - u0 * h, yb = q.pos.y - u1 * h, xa = q.pos.x + lac(a, u0), xb = q.pos.x + lac(a, u1);
                        float bd = 5 * sc;
                        int s1 = mp.Count;
                        mp.Add(new Vector2(xa - ra, ya));
                        mp.Add(new Vector2(xb + rb, yb));
                        mp.Add(new Vector2(xb + rb, yb + bd));
                        mp.Add(new Vector2(xa - ra, ya + bd));
                        MFill(Front, 22.01f + i * 0.001f, s1, 4, ToCatSam, Al * mo, false);
                        if ((i & 1) != 0) continue;
                        int s2 = mp.Count;
                        mp.Add(new Vector2(xa - ra * 0.65f, ya - 9 * sc));
                        mp.Add(new Vector2(xb + rb * 0.55f, yb - 9 * sc));
                        mp.Add(new Vector2(xb + rb * 0.55f, yb - 6.5f * sc));
                        mp.Add(new Vector2(xa - ra * 0.65f, ya - 6.5f * sc));
                        MFill(Front, 22.02f + i * 0.001f, s2, 4, ToCat3, Al * mo, false);
                    }
                };
                Add(p);
            });
            // mảnh đất nung + bụi bay quanh lốc, bụi tràn miệng / chân phễu
            Every(t0 + 0.12f, t1 - 0.25f, 50, x =>
            {
                float u = U(0.15f, 0.95f), a0 = U(0, 6.28f), sp = U(9, 14);
                var q = new P { pos = chan, life = U(0.35f, 0.6f), group = Front, seed = rng.Next(4), sz = U(3.5f, 6f) * sc, col = U(0, 1) < 0.5f ? ToGom : ToGom2,
                    hgt = 1.4f, spin = U(-500, 500) };
                q.upd = (z, dt, s) =>
                {
                    float r = (18 + 50 * Mathf.Pow(u, 1.2f)) * sc, th = a0 + z.age * sp;
                    z.pos = new Vector2(chan.x + r * Mathf.Cos(th), chan.y - u * cao - 10 * sc * z.age);
                    z.vel = Vector2.zero;
                    z.group = Mathf.Sin(th) > 0 ? Front : Back;
                };
                q.draw = DrawSoiP;
                Add(q);
                if (U(0, 1) < 0.45f)
                {
                    float d = U(0, 1) < 0.5f ? -1 : 1;
                    ToBui(chan + new Vector2(d * 60 * sc, -cao * 0.95f), new Vector2(d * 70, -10) * sc, 0.5f, 5 * sc, 13 * sc);
                }
                if (U(0, 1) < 0.35f)
                {
                    float d = U(0, 1) < 0.5f ? -1 : 1;
                    ToBui(chan + new Vector2(d * 20 * sc, -2), new Vector2(d * 80, -10) * sc, 0.45f, 4 * sc, 12 * sc, Back);
                }
            });
        }

        // sóng chấn: chín cụm gai đá trồi nối nhau dọc mặt đất từ a tới b trong tb giây (mỗi cụm trồi rồi lún, bụi); tới nơi gọi toi
        void ToSongChan(Vector2 a, Vector2 b, float tb, float sc, Action toi)
        {
            const int n = 9;
            for (int i = 0; i < n; i++)
            {
                float f = (i + 1f) / n;
                bool cuoi = i == n - 1;
                At(tb * f, () =>
                {
                    var c = Vector2.Lerp(a, b, f);
                    for (int m = 0; m < 2; m++)
                    {
                        var q = new P
                        {
                            pos = c + new Vector2(U(-14, 14), U(-3, 3)) * sc, life = 0.32f, group = Front, sz = U(18, 30) * (0.7f + 0.5f * f) * sc,
                            wd = U(8, 13) * sc, hgt = U(-3, 3) * sc, R0 = U(0.6f, 0.9f), seed = rng.Next(3)
                        };
                        q.draw = (z, k, buf) =>
                        {
                            float g = Mathf.Min(1, k / 0.25f) * (1 - Mathf.Max(0, k - 0.6f) / 0.4f);
                            if (g < 0.05f) return;
                            int s0 = mp.Count;
                            mp.Add(z.pos + new Vector2(-z.wd, 0));
                            mp.Add(z.pos + new Vector2(-z.wd * 0.5f, -z.sz * z.R0 * g));
                            mp.Add(z.pos + new Vector2(z.hgt, -z.sz * g));
                            mp.Add(z.pos + new Vector2(z.wd * 0.6f, -z.sz * 0.7f * g));
                            mp.Add(z.pos + new Vector2(z.wd, 0));
                            MSolid(z.group, 24, s0, 5, z.seed == 0 ? ToDa2 : z.seed == 1 ? ToDa : ToDa3, 1, 2.2f);
                        };
                        Add(q);
                    }
                    ToBui(c, new Vector2(U(-40, 40), -30) * sc, 0.5f, 5 * sc, 13 * sc, Back);
                    if (cuoi) toi?.Invoke();
                });
            }
        }

        // vết cắn: hai cung kem (hàm trên, hàm dưới) khép vào nhau trong 0,18 s
        void ToCan(Vector2 c, float tH)
        {
            for (int j = 0; j < 2; j++)
            {
                float sd = j == 0 ? -1 : 1;
                var p = new P { pos = c, life = 0.18f, group = Front, sz = 0.42f * tH, ph = sd };
                p.draw = (q, k, buf) =>
                {
                    float off = q.ph * (0.08f + 0.22f * (1 - EaseOut(k / 0.5f))) * q.sz;
                    float al = 1 - SmoothStep(0.6f, 1, k);
                    float ang = q.ph < 0 ? 180 : 0;
                    Put(buf, Front, 61, S("arcs_0"), Ink, q.pos + new Vector2(0, off), q.sz + 4, 1, ang, al);
                    Put(buf, Front, 61.1f, S("arc_0"), ToKem, q.pos + new Vector2(0, off), q.sz, 1, ang, al);
                };
                Add(p);
            }
        }

        // ba vệt vuốt: ba cung kem chéo, so le 0,02 s, hiện 0,18 s
        void ToVuot(Vector2 c, float dir, float tH)
        {
            float sc = tH / 150f;
            for (int i = 0; i < 3; i++)
            {
                var at = c + new Vector2((-8 + 9 * i) * dir, -6 + 7 * i) * sc;
                At(0.02f * i, () =>
                {
                    var p = new P { pos = at, life = 0.18f, group = Front, sz = 0.42f * tH };
                    p.draw = (q, k, buf) =>
                    {
                        float al = 1 - k * k, ang = dir > 0 ? -40 : 40;
                        Put(buf, Front, 61, S("arcs_0"), Ink, q.pos, q.sz + 4, 1, ang, al);
                        Put(buf, Front, 61.1f, S("arc_0"), ToKem, q.pos, q.sz, 1, ang, al);
                    };
                    Add(p);
                });
            }
        }

        // ================= Thạch Giáp (thach_nhan; rig cong_da_1, ArtGen/Spine/cong_da_rig.py) =================
        const float GiapHuc = 0.40f, GiapCast = 0.66f, GiapSkill = 1.50f;
        static readonly float[] GiapPhong = { 0.46f, 0.52f, 0.58f };   // ba viên sỏi (mảnh của rig, xương fly_*, game lái) rời mai; tới đích sau GiapBay
        const float GiapBay = 0.20f, GiapLac0 = 0.28f, GiapLac1 = 0.60f, GiapDap = 0.66f;
        const float GiapGong0 = 0.30f, GiapGong1 = 0.80f, GiapBan = 0.86f, GiapMua = 1.18f;
        static readonly Vector2[] GiapMai = { new Vector2(0.220f, 0.464f), new Vector2(0.152f, 0.656f), new Vector2(0.188f, 0.655f), new Vector2(0.194f, 0.595f),
            new Vector2(0.209f, 0.436f) };                              // giữa mai lúc lắc, 0,28 → 0,60 bước 0,08
        static readonly Vector2 GiapPhaLe = new Vector2(0.016f, 0.725f); // hốc pha lê trên đỉnh mai lúc bắn lên (0,86)
        // dạng 2 (cong_da_2, rig 3528; inbox/cong_da_2_ghichu.md): đánh thường trúng 0,46; cast lắc 0,26 → 0,60, ba CỤM PHA LÊ của rig rời
        // hốc 0,46 / 0,52 / 0,58, găm 0,66 / 0,72 / 0,78, dậm 0,68; skill gồng 0,30 → 0,84, cụm đỉnh vọt 0,90, mưa 1,22, trúng 1,56
        static readonly Vector2[] GiapMai2 = { new Vector2(-0.011f, 0.636f), new Vector2(-0.015f, 0.644f), new Vector2(-0.016f, 0.648f),
            new Vector2(-0.015f, 0.647f), new Vector2(-0.014f, 0.644f) };      // giữa núi đá lúc lắc, 0,26 → 0,58 bước 0,08
        static readonly Vector2[] GiapRoi2 = { new Vector2(-0.312f, 0.583f), new Vector2(0.281f, 0.694f), new Vector2(-0.297f, 0.838f) }; // hốc cụm rời
        static readonly Vector2 GiapPhaLe2 = new Vector2(0.085f, 0.870f);   // cụm đỉnh lúc vọt (0,90)

        // ĐÒN THƯỜNG: lao húc đầu. Bụi sau gót lúc bật, chỗ đầu chạm: chớp, dăm đá, bụi. dang 2: cú húc nặng hơn, vòng bụi dưới đối thủ
        public float NGiapHuc(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 1)
        {
            float L = Mathf.Max(0.05f, lead), k = L / GiapHuc, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            At(Mathf.Max(0, L - 0.22f * k), () =>
            {
                for (int i = 0; i < 2; i++)
                    ToBui(casterFeet + new Vector2(-dir * U(4, 0.25f * casterH), U(-4, 2)), new Vector2(-dir * U(60, 160), -U(10, 50)) * sH, 0, 4 * sH, 12 * sH, Back);
            });
            At(L, () =>
            {
                ToNo(foeBody + new Vector2(-dir * 0.22f * tH, 0.04f * tH), foeFeet.y, tH, dang == 2 ? 1.3f : 0.9f, ToDa, ToDa2);
                if (dang == 2) ToVong(foeFeet, 70 * sc);
                for (int i = 0; i < 2; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    ToBui(foeFeet + new Vector2(sd * U(6, 0.25f * tH), U(-5, 2)), new Vector2(sd * U(80, 200), -U(10, 50)) * sc, 0, 5 * sc, 14 * sc, Back);
                }
            });
            return L;
        }

        // CHIÊU MANA: lắc mai (bụi, sỏi rơi khỏi mai), ba viên sỏi của rig rời mai bay găm (lớp này lo từng cú găm), đáp phịch.
        // dang 2: ba CỤM PHA LÊ hổ phách của rig rời ba hốc núi đá, mỗi cú găm nặng hơn, dăm hổ phách
        public float NGiapSoi(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 1)
        {
            float L = Mathf.Max(0.05f, lead), k = L / GiapCast, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            bool d2 = dang == 2;
            float lac0 = d2 ? 0.26f : GiapLac0, dap = d2 ? 0.68f : GiapDap;
            Func<float, Vector2> mai = t => ToSan(casterFeet, casterH, dir, ToDiem(d2 ? GiapMai2 : GiapMai, lac0, 0.08f, t / k));
            Every(lac0 * k, GiapLac1 * k, 40, x =>
            {
                var p = mai((lac0 + (GiapLac1 - lac0) * x) * k) + new Vector2(U(-0.2f, 0.2f), U(-0.1f, 0.1f)) * casterH;
                ToBui(p, new Vector2(U(-30, 30), U(-20, 20)) * sH, 0.5f, 3 * sH, 8 * sH);
                if (U(0, 1) < 0.5f) ToSoi(p, new Vector2(U(-90, 90), U(-160, -60)) * sH, 2.4f * sH, ToDa, casterFeet.y + 4 * sH);
            });
            for (int i = 0; i < 3; i++)
            {
                int j = i;
                At(GiapPhong[j] * k, () => ToBui(d2 ? ToSan(casterFeet, casterH, dir, GiapRoi2[j]) : mai(GiapPhong[j] * k), Vector2.zero, 0.45f,
                    (d2 ? 5 : 4) * sH, (d2 ? 13 : 10) * sH));
                At((GiapPhong[j] + GiapBay) * k, () =>
                {
                    if (d2) ToNo(foeBody + U2(-16, 16) * sc, foeFeet.y, tH, j == 2 ? 1.5f : 1.1f, ToPhach, ToDa);
                    else ToNo(foeBody + U2(-14, 14) * sc, foeFeet.y, tH, j == 2 ? 1.1f : 0.8f, ToDa, ToDa2);
                });
            }
            At(dap * k, () =>
            {
                ToVong(casterFeet, 70 * sH);
                for (int d = -1; d <= 1; d += 2)
                    ToBui(casterFeet + new Vector2(d * 40 * sH, -4 * sH), new Vector2(d * 70, -20) * sH, 0, 6 * sH, 16 * sH);
                Shake?.Invoke(0.08f);
            });
            return (GiapPhong[0] + GiapBay) * k;
        }

        // CHIÊU CUỐI: rụt mai gồng (bụi), pha lê vọt lên trời từ hốc mai, mưa pha lê hổ phách: bảy mảnh nhỏ so le, mảnh to cắm xuống đúng
        // khung trúng (cắm đất cạnh đối thủ, rung rồi vỡ). dang 2: mười mảnh, mảnh to hơn, cú cuối nặng hơn
        public float NGiapMua(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 1)
        {
            bool d2 = dang == 2;
            float L = Mathf.Max(0.3f, lead), k = L / (d2 ? 1.56f : GiapSkill), dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            float gong1 = d2 ? 0.84f : GiapGong1, ban = d2 ? 0.90f : GiapBan, mua = d2 ? 1.22f : GiapMua, to = d2 ? 1.25f : 1f;
            Every(GiapGong0 * k, gong1 * k, 22, x =>
                ToBui(casterFeet + new Vector2(U(-0.4f, 0.4f) * casterH, -2), new Vector2(U(-40, 40), -15) * sH, 0.5f, 3.5f * sH, 9 * sH, Back));
            At(GiapGong0 * k, () => Shake?.Invoke(0.05f));
            At(ban * k, () =>
            {
                var goc = ToSan(casterFeet, casterH, dir, d2 ? GiapPhaLe2 : GiapPhaLe);
                for (int i = 0; i < (d2 ? 8 : 6); i++)
                    ToPhaLe(goc + new Vector2(U(-18, 18) * sH, 0), new Vector2(U(-60, 60), -1100 - 120 * i) * sH, 22 * sH, 8 * sH, 0.5f);
                for (int i = 0; i < 4; i++)
                    ToBui(goc + U2(-20, 20) * sH, new Vector2(U(-80, 80), U(-60, -20)) * sH, 0, 5 * sH, 13 * sH);
                ToVong(casterFeet, 80 * sH);
                Shake?.Invoke(0.15f);
            });
            float[] dx = { -34, 22, -10, 36, -26, 8, 30, -44, 16, -2 };
            const float TB = 0.26f;                                      // giây rơi của một mảnh
            var vRoi = new Vector2(dir * 230, 1050) * sc;                 // rơi chéo từ phía mình xuống
            int nm = d2 ? 10 : 7;
            for (int i = 0; i < nm; i++)
            {
                int j = i;
                float tc = Mathf.Min(L - 0.05f, (mua + (d2 ? 0.032f : 0.045f) * j) * k);
                At(Mathf.Max(0, tc - TB), () =>
                {
                    var dich = foeBody + new Vector2(dx[j] * (d2 ? 1.15f : 1f), U(-30, 25)) * sc;
                    ToPhaLe(dich - vRoi * TB, vRoi, 24 * sc * to, 9 * sc * to, TB + 0.1f, dich.y, p => ToNo(p, foeFeet.y, tH, 0.7f * to, ToPhach, ToDa));
                });
            }
            At(Mathf.Max(0, L - TB), () =>
            {
                var dich = foeBody + new Vector2(0, 0.06f * tH);
                var v = new Vector2(dir * 260, 1150) * sc;
                ToPhaLe(dich - v * TB, v, 48 * sc * to, 18 * sc * to, TB + 0.1f, dich.y, p =>
                {
                    ToNo(p, foeFeet.y, tH, 2f * to, ToPhach, ToDa2);
                    ToVong(foeFeet, 95 * sc * to, 0.55f);
                    var cam = new P { pos = new Vector2(p.x + dir * 0.1f * tH, foeFeet.y), life = 0.45f, group = Front, sz = 54 * sc * to, wd = 24 * sc * to };
                    cam.draw = (z, kk, buf) =>
                        DrawPhaLe(buf, Front, z.pos + new Vector2(1.5f * sc * Mathf.Sin(z.age * 70), -0.42f * z.sz), Unit(new Vector2(dir * 0.25f, -1)), z.sz, z.wd);
                    cam.onDeath = (z, s) => ToNo(z.pos + new Vector2(0, -0.4f * z.sz), foeFeet.y, tH, 1.2f, ToPhach, ToPhach2);
                    Add(cam);
                });
            });
            return L;
        }

        // ================= Sa Tích (lung_vuong; rig than_lan_cat_1, ArtGen/Spine/than_lan_cat_rig.py) =================
        const float TichDop = 0.56f, TichCast = 0.6787f, TichSkill = 1.00f;
        static readonly float[] TichPhong = { 14 / 30f, 16 / 30f, 18 / 30f };   // ba phiến áo choàng (mảnh của rig, game lái) rời thân
        const float TichBay = 0.20f, TichDam = 0.62f, TichHet = 1.78f;
        static readonly Vector2[] TichAo = { new Vector2(0.048f, 0.755f), new Vector2(0.059f, 0.749f), new Vector2(0.080f, 0.767f), new Vector2(0.189f, 0.833f) };
                                                                        // giữa áo choàng lúc xoè, 0,12 → 0,45 bước 0,11
        // dạng 2 (than_lan_cat_2, rig 3530): đánh thường bật 0,38, đớp 0,52; cast cát bốc 0,05 → 0,45, NĂM phiến mũ trùm rời 0,46 → 0,62,
        // găm 0,66 → 0,82 (trúng 0,672); skill cát xoáy 0,08, đập đất 0,62 và 1,00 (= trúng, lốc cát), lốc tan 1,78
        static readonly float[] TichPhong2 = { 0.46f, 0.50f, 0.54f, 0.58f, 0.62f };
        static readonly Vector2[] TichAo2 = { new Vector2(0.101f, 0.650f), new Vector2(0.085f, 0.655f), new Vector2(0.065f, 0.660f), new Vector2(0.052f, 0.663f),
            new Vector2(0.140f, 0.618f) };                                // gốc mũ trùm lúc xoè, 0,05 → 0,45 bước 0,1
        static readonly Vector2 TichVuot2 = new Vector2(0.42f, 0.05f);    // vuốt tay xa chạm đất lúc đập (gốc bàn tay 0,42 / 0,29, vuốt thấp hơn ~0,25)

        // ĐÒN THƯỜNG: chồm đớp: vết cắn hai cung kem, dăm cát. dang 2: bụi sau chân lúc bật, cú đớp nặng hơn
        public float NTichDop(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 1)
        {
            float L = Mathf.Max(0.05f, lead), dir = foeFeet.x >= casterFeet.x ? 1 : -1, sH = casterH / 150f;
            if (dang == 2)
                At(L * 0.38f / 0.52f, () =>
                {
                    for (int i = 0; i < 3; i++)
                        ToBui(casterFeet + new Vector2(-dir * U(4, 0.3f * casterH), U(-4, 2)), new Vector2(-dir * U(70, 180), -U(10, 50)) * sH, 0, 5 * sH, 14 * sH, Back);
                });
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.12f * tH, 0.04f * tH);
                ToCan(c, tH * (dang == 2 ? 1.2f : 1f));
                ToNo(c, foeFeet.y, tH, dang == 2 ? 1.05f : 0.7f, ToCat, ToCat2);
            });
            return L;
        }

        // CHIÊU MANA: cát bốc quanh áo choàng lúc xoè; ba phiến đất nung của rig bay găm: mỗi cú găm dăm đất nung. dang 2: năm phiến mũ trùm
        public float NTichPhien(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 1)
        {
            bool d2 = dang == 2;
            float L = Mathf.Max(0.05f, lead), k = L / (d2 ? 0.672f : TichCast), dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            float x0 = d2 ? 0.05f : 0.12f, x1 = 0.45f;
            Every(x0 * k, x1 * k, d2 ? 34 : 26, x =>
            {
                var p = ToSan(casterFeet, casterH, dir, d2 ? ToDiem(TichAo2, 0.05f, 0.1f, x0 + (x1 - x0) * x) : ToDiem(TichAo, 0.12f, 0.11f, x0 + (x1 - x0) * x))
                        + U2(-0.25f, 0.25f) * casterH;
                ToBui(p, new Vector2(U(-40, 40), U(-60, -20)) * sH, 0.5f, 3.5f * sH, 9 * sH);
            });
            var ph = d2 ? TichPhong2 : TichPhong;
            for (int i = 0; i < ph.Length; i++)
            {
                int j = i;
                bool cuoi = j == ph.Length - 1;
                At((ph[j] + TichBay) * k, () => ToNo(foeBody + U2(-16, 16) * sc, foeFeet.y, tH, cuoi ? (d2 ? 1.35f : 1.1f) : 0.85f, ToGom, ToGom2));
            }
            return (ph[0] + TichBay) * k;
        }

        // CHIÊU CUỐI: cát xoáy quanh chân đối thủ, dậm đất, LỐC CÁT trùm đối thủ tới lúc thu áo choàng. dang 2: đập đất hai lần bằng vuốt tay
        // xa (0,62 và 1,00 = trúng), lốc cao và rộng hơn
        public float NTichLoc(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 1)
        {
            bool d2 = dang == 2;
            float L = Mathf.Max(0.3f, lead), k = L / TichSkill, sc = tH / 150f, sH = casterH / 150f, dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var dam = d2 ? ToSan(casterFeet, casterH, dir, TichVuot2) + new Vector2(0, casterH * 0.05f) : casterFeet;
            Every(0.08f * k, L, 18, x =>
            {
                float a = U(0, 6.28f);
                ToBui(foeFeet + new Vector2(50 * Mathf.Cos(a), -4 + 8 * Mathf.Sin(a)) * sc, new Vector2(-60 * Mathf.Sin(a), -20) * sc, 0.5f, 3.5f * sc, 9 * sc, Back);
            });
            foreach (float td in d2 ? new[] { TichDam, TichSkill } : new[] { TichDam })
                At(td * k, () =>
                {
                    ToVong(dam, (d2 ? 95 : 80) * sH);
                    for (int d = -1; d <= 1; d += 2)
                        ToBui(dam + new Vector2(d * 40 * sH, -4 * sH), new Vector2(d * 90, -20) * sH, 0, 7 * sH, 18 * sH);
                    Shake?.Invoke(0.25f);
                });
            float cao = Mathf.Min((d2 ? 1.45f : 1.25f) * tH, foeFeet.y - 30);   // phễu tự hạ khi đối thủ đứng sát mép trên sân
            ToLocCat(foeFeet + new Vector2(0, 4 * sc), cao, Mathf.Max(0, L - 0.06f * k), (TichHet + 0.2f) * k, sc * (d2 ? 1.15f : 1f));
            return L;
        }

        // ================= Tê Thiềm (cao_da; rig thu_da_1, ArtGen/Spine/thu_da_rig.py) =================
        const float ThiemGiang = 0.50f, ThiemCast = 0.92f, ThiemSkill = 1.20f;
        const float ThiemTu = 0.12f, ThiemCuon = 0.32f, ThiemLao = 0.86f, ThiemVe = 1.64f, ThiemBayDa = 0.36f;
        static readonly Vector2[] ThiemMieng = { new Vector2(0.438f, 0.515f), new Vector2(0.388f, 0.477f), new Vector2(0.337f, 0.481f), new Vector2(0.277f, 0.480f),
            new Vector2(0.369f, 0.549f), new Vector2(0.496f, 0.640f), new Vector2(0.535f, 0.563f), new Vector2(0.521f, 0.580f), new Vector2(0.525f, 0.568f) };
                                                                        // miệng lúc há hàm tụ đá, 0,1 → 0,9 bước 0,1
        // dạng 2 (thu_da_2, rig 3526): đánh thường lao 0,34 ĐÂM mũi khối pha lê 0,55; cast tụ 0,30, phun 0,95; skill (rig khai lunge) gồng
        // 0,50, nhảy 0,96, BỔ khối xuống 1,12 (= trúng), chạm đất lúc về 1,62, gầm 1,86
        static readonly Vector2[] ThiemMieng2 = { new Vector2(0.421f, 0.478f), new Vector2(0.356f, 0.541f), new Vector2(0.293f, 0.583f), new Vector2(0.282f, 0.603f),
            new Vector2(0.277f, 0.600f), new Vector2(0.275f, 0.605f), new Vector2(0.272f, 0.621f), new Vector2(0.268f, 0.627f), new Vector2(0.263f, 0.632f),
            new Vector2(0.265f, 0.609f), new Vector2(0.331f, 0.561f), new Vector2(0.399f, 0.521f), new Vector2(0.432f, 0.471f) };   // miệng, 0,1 → 1,3
        const float ThiemDam2 = 0.55f, ThiemLao2 = 0.34f, ThiemGong2 = 0.50f, ThiemNhay2 = 0.96f, ThiemBo2 = 1.12f, ThiemVe2 = 1.62f, ThiemGam2 = 1.86f;

        // ĐÒN THƯỜNG: chồm giáng sừng: vòng bụi chỗ đáp, chớp, dăm đá
        public float NThiemGiang(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead), dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f;
            At(L, () =>
            {
                ToNo(foeBody + new Vector2(-dir * 0.16f * tH, 0.06f * tH), foeFeet.y, tH, 1f, ToDa, ToDa2);
                var g = foeFeet + new Vector2(-dir * 0.2f * tH, 0);
                ToVong(g, 60 * sc);
                for (int d = -1; d <= 1; d += 2)
                    ToBui(g + new Vector2(d * 20 * sc, -4 * sc), new Vector2(d * 60, -30) * sc, 0, 5 * sc, 13 * sc, Back);
            });
            return L;
        }

        // CHIÊU MANA: há hàm, bụi và sỏi xoáy hút vào miệng; nhả: tảng đá (mạch hổ phách) bay vồng tới đối thủ, vỡ. dang 2: ngả ra sau gầm,
        // tụ lâu hơn, tảng to hơn, vỡ nặng hơn
        public float NThiemPhun(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 1)
        {
            bool d2 = dang == 2;
            float L = Mathf.Max(0.1f, lead), k = L / (d2 ? 0.95f : ThiemCast), dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            float t0 = T;
            Func<float, Vector2> mieng = t => ToSan(casterFeet, casterH, dir, ToDiem(d2 ? ThiemMieng2 : ThiemMieng, 0.1f, 0.1f, (t - t0) / k));
            Every((d2 ? 0.30f : ThiemTu) * k, L - 0.04f * k, d2 ? 50 : 40, x =>
            {
                float a = U(0, 6.28f);
                var p0 = mieng(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * (U(45, 70) * sH);
                ToHut(p0, mieng, 0.32f, U(2.5f, 3.8f) * sH, U(0, 1) < 0.5f ? ToDa : ToBuiC, 1.6f);
            });
            At(L, () =>
            {
                var m = mieng(T);
                ToTangBay(m, foeBody + new Vector2(-dir * 0.05f * tH, 0), ThiemBayDa, (d2 ? 21 : 16) * sH, 60 * sc, true, p =>
                {
                    ToNo(p, foeFeet.y, tH, d2 ? 2.1f : 1.6f, ToDa, ToPhach);
                    ToVong(foeFeet, (d2 ? 100 : 80) * sc);
                    Shake?.Invoke(0.2f);
                });
                for (int i = 0; i < 3; i++)
                    ToBui(m + U2(-8, 8) * sH, new Vector2(-dir * U(30, 80), U(-40, 10)) * sH, 0.4f, 4 * sH, 10 * sH);
            });
            return L + ThiemBayDa;
        }

        // CHIÊU CUỐI (rig khai lunge): cuộn tròn xoay tại chỗ (bụi, sỏi toé ra sau), lăn tới (vệt bụi theo đường lăn), nện đúng khung
        // trúng, bật về đáp đất
        public float NThiemLan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / ThiemSkill, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            var toi = Vector2.Lerp(casterFeet, foeFeet, 0.72f);           // đỉnh cú lunge của sân (AolaSticker.Lunge)
            Func<float, Vector2> cho = t =>
            {
                float u = Mathf.Clamp01((t / k - ThiemLao) / (ThiemSkill - ThiemLao));
                return Vector2.Lerp(casterFeet, toi, u * u * (3 - 2 * u));
            };
            Every((ThiemCuon + 0.04f) * k, ThiemLao * k, 34, x =>
            {
                var p = casterFeet + new Vector2(U(-10, 10) * sH, -4 * sH);
                ToBui(p, new Vector2(-dir * U(40, 120), U(-50, -10)) * sH, 0.5f, 4.5f * sH, 12 * sH, Back);
                if (U(0, 1) < 0.4f) ToSoi(p, new Vector2(-dir * U(80, 200), U(-220, -100)) * sH, 2.4f * sH, ToDa, casterFeet.y + 4 * sH);
            });
            float tl0 = ThiemLao * k;
            Every(tl0, L, 45, x => ToBui(cho(tl0 + x * (L - tl0)) + new Vector2(0, -2 * sH), new Vector2(U(-20, 20), U(-30, -5)) * sH, 0.55f, 5 * sH, 13 * sH, Back));
            At(L, () =>
            {
                ToNo(foeBody + new Vector2(-dir * 0.1f * tH, 0.07f * tH), foeFeet.y, tH, 2.2f, ToDa, ToPhach);
                ToVong(foeFeet, 110 * sc, 0.6f);
            });
            At(ThiemVe * k, () =>
            {
                ToVong(casterFeet, 70 * sH);
                Shake?.Invoke(0.1f);
            });
            return L;
        }

        // ================= Sa Long (ho_khoan; rig rong_cat_1, ArtGen/Spine/rong_cat_rig.py) =================
        const float LongVuotT = 0.54f, LongCast = 0.76f, LongSkill = 1.82f;
        static readonly float[] LongChem = { 0.70f, 0.76f, 0.84f };    // ba nhát vuốt quét của cast (sự kiện chem1..3)
        static readonly Vector2[] LongVuotCast = { new Vector2(0.816f, 0.014f), new Vector2(0.937f, 0.141f), new Vector2(0.731f, -0.039f) };
        static readonly Vector2[] LongVuotSkill = { new Vector2(-0.139f, 0.639f), new Vector2(-0.150f, 0.646f), new Vector2(-0.159f, 0.654f),
            new Vector2(-0.145f, 0.643f), new Vector2(-0.146f, 0.644f), new Vector2(-0.164f, 0.657f), new Vector2(-0.166f, 0.658f), new Vector2(-0.155f, 0.650f),
            new Vector2(0.119f, 0.083f), new Vector2(0.093f, 0.012f) };   // vuốt lúc giơ gồng rồi nện, 0,3 → 1,2 bước 0,1
        const float LongGong = 0.36f, LongNen = 1.16f, LongBayLuoi = 0.20f;
        static readonly float[] LongCotT = { 1.34f, 1.56f, 1.82f };     // ba cột trồi (sự kiện cot1..3), cột cuối to = khung trúng
        // DẠNG 1 (rong_cat_non, rig 3529; inbox/rong_cat_non_ghichu.md): đánh thường vồ chém trúng 0,40; cast hai nhát 0,40 (= trúng) / 0,47,
        // lưỡi rời vuốt sát đất trước ngực; skill gồng 0,60 (cát hút về vuốt xa tới ~1,50), nện 1,60, cột nhỏ 1,76, cột vừa 1,96 (= trúng)
        static readonly float[] LongChem1 = { 0.40f, 0.47f };
        static readonly Vector2 LongVuotCast1 = new Vector2(0.09f, 0.0f);
        static readonly Vector2[] LongVuotSkill1 = { new Vector2(0.426f, 0.166f), new Vector2(0.460f, 0.170f), new Vector2(0.469f, 0.211f),
            new Vector2(0.472f, 0.235f), new Vector2(0.472f, 0.256f), new Vector2(0.472f, 0.274f), new Vector2(0.473f, 0.289f), new Vector2(0.476f, 0.295f),
            new Vector2(0.500f, 0.249f) };                                // vuốt xa lúc gồng, 0,60 → 1,40 bước 0,1
        const float LongGong1 = 0.60f, LongNen1 = 1.60f, LongCot1a = 1.76f, LongSkill1 = 1.96f;
        static readonly Vector2 LongNenP1 = new Vector2(0.500f, 0.055f);

        // ĐÒN THƯỜNG: lao chém vuốt: ba vệt vuốt kem, dăm cát. manh < 1: dạng 1 (rồng non, vệt nhỏ hơn)
        public float NLongVuot(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh = 1)
        {
            float L = Mathf.Max(0.05f, lead), dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.1f * tH, 0);
                ToVuot(c, dir, tH * manh);
                ToNo(c, foeFeet.y, tH, manh, ToCat, ToCat2);
            });
            return L;
        }

        // CHIÊU MANA: ba nhát vuốt quét, mỗi nhát phóng một lưỡi cát trăng khuyết bay tới đối thủ. dang 1 (rồng non rong_cat_non): hai nhát
        // 0,40 / 0,47, hai lưỡi nhỏ rời vuốt sát đất trước ngực
        public float NLongLuoi(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 2)
        {
            bool d1 = dang == 1;
            var chem = d1 ? LongChem1 : LongChem;
            float L = Mathf.Max(0.1f, lead), k = L / (d1 ? LongChem1[0] : LongCast), dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            for (int i = 0; i < chem.Length; i++)
            {
                int j = i;
                At(chem[j] * k, () =>
                {
                    var m = ToSan(casterFeet, casterH, dir, d1 ? LongVuotCast1 : LongVuotCast[j]);
                    float R = d1 ? (26 + 4 * j) * sH : (34 + 5 * j) * sH;
                    ToLuoiCat(m, foeBody + new Vector2(0, (d1 ? j - 0.5f : j - 1) * 16 * sc), LongBayLuoi, R,
                        p => ToNo(p, foeFeet.y, tH, d1 ? 0.7f : 0.9f, ToCat, ToCat2));
                });
            }
            return chem[0] * k + LongBayLuoi;
        }

        // CHIÊU CUỐI: giơ vuốt gồng (cát, đá vụn hút về vuốt), nện đất (vết nứt chạy tới đối thủ), CỘT SA THẠCH trồi ba nhịp quanh đối thủ,
        // cột cuối to đúng khung trúng
        public float NLongCot(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / LongSkill, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            float t0 = T;
            Func<float, Vector2> vuot = t => ToSan(casterFeet, casterH, dir, ToDiem(LongVuotSkill, 0.3f, 0.1f, (t - t0) / k));
            Every(LongGong * k, (LongNen - 0.1f) * k, 36, x =>
            {
                float a = U(0, 6.28f);
                var p0 = vuot(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.6f) * (U(50, 80) * sH);
                ToHut(p0, vuot, 0.3f, U(2.5f, 4.5f) * sH, U(0, 1) < 0.5f ? ToCat : ToCat2, 1.5f);
            });
            var nen = casterFeet + new Vector2(dir * 0.2f * casterH, 0);
            At(LongNen * k, () =>
            {
                ToVong(nen, 100 * sH, 0.55f);
                for (int d = -1; d <= 1; d += 2)
                    ToBui(nen + new Vector2(d * 30 * sH, -4 * sH), new Vector2(d * 90, -30) * sH, 0, 7 * sH, 18 * sH);
                Shake?.Invoke(0.3f);
                ToNut(nen, foeFeet + new Vector2(dir * 0.13f * tH, 2), 0.18f * k, sc);
            });
            // soi trong game 2026-11-17: cột cao bằng đối thủ nằm sau nó thì bị che gần hết: hai cột nhỏ dời ra ngoài hai bên thân (±0,62 chiều cao
            // đối thủ), cột cuối cao 1,45 lần đối thủ để trồi hẳn lên trên đầu nó
            float[] dx = { -0.62f, 0.62f, 0 };
            for (int i = 0; i < 3; i++)
            {
                int j = i;
                bool to = j == 2;
                At(LongCotT[j] * k, () =>
                {
                    ToCot(foeFeet + new Vector2(dx[j] * tH, (to ? 2 : 4) * sc), (to ? 0.48f : 0.26f) * tH, (to ? 1.45f : 0.75f) * tH, to ? 0.55f : 0.35f,
                        Back, sc);
                    if (to) ToNo(foeBody + new Vector2(0, 10 * sc), foeFeet.y, tH, 2.2f, ToCat, ToCat2);
                    else
                    {
                        Shake?.Invoke(0.18f);
                        ToNo(foeFeet + new Vector2(dx[j] * tH, -0.5f * tH), foeFeet.y, tH, 0.7f, ToCat2, ToSaThach);
                    }
                });
            }
            return L;
        }

        // ================= DẠNG 2 Tê Thiềm, DẠNG 1 Sa Long (hàm riêng: động tác khác hẳn dạng kia) =================

        // Tê Thiềm dạng 2, ĐÒN THƯỜNG: bụi sau chân lúc lao, mũi khối pha lê ĐÂM vào thân đối thủ: chớp, dăm hổ phách văng theo hướng đâm,
        // hai mảnh pha lê nhỏ bật ra
        public float NThiemDam2(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead), k = L / ThiemDam2, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            At(ThiemLao2 * k, () =>
            {
                for (int i = 0; i < 3; i++)
                    ToBui(casterFeet + new Vector2(-dir * U(4, 0.3f * casterH), U(-4, 2)), new Vector2(-dir * U(80, 200), -U(10, 60)) * sH, 0, 5 * sH, 14 * sH, Back);
            });
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.18f * tH, 0.08f * tH);
                ToNo(c, foeFeet.y, tH, 1.4f, ToPhach, ToDa);
                for (int i = 0; i < 2; i++)
                    ToPhaLe(c, new Vector2(dir * U(150, 260), -U(260, 420)) * sc, 16 * sc, 6 * sc, 0.45f);
                ToVong(foeFeet, 75 * sc);
            });
            return L;
        }

        // Tê Thiềm dạng 2, CHIÊU CUỐI (rig khai lunge): giơ khối pha lê gồng trên đầu (bụi, sỏi rơi), nhảy tới (bụi bật dưới chân), BỔ khối
        // xuống ngay trước đối thủ (khung trúng): chớp lớn, vòng bụi, vết nứt toả, ba cột PHA LÊ hổ phách trồi quanh chỗ bổ, mảnh pha lê văng;
        // về chạm đất: bụi; gầm: rung nhẹ
        public float NThiemBo2(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / ThiemBo2, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            Every(ThiemGong2 * k, ThiemNhay2 * k, 22, x =>
            {
                ToBui(casterFeet + new Vector2(U(-0.4f, 0.4f) * casterH, -2), new Vector2(U(-40, 40), -15) * sH, 0.5f, 4 * sH, 10 * sH, Back);
                if (U(0, 1) < 0.4f)
                    ToSoi(casterFeet + new Vector2(dir * U(-0.1f, 0.3f) * casterH, -U(0.9f, 1.1f) * casterH), new Vector2(U(-60, 60), 60) * sH, 2.6f * sH, ToPhach,
                        casterFeet.y + 4 * sH);
            });
            At(ThiemGong2 * k, () => Shake?.Invoke(0.08f));
            At(ThiemNhay2 * k, () =>
            {
                ToVong(casterFeet, 75 * sH);
                for (int d = -1; d <= 1; d += 2)
                    ToBui(casterFeet + new Vector2(d * 40 * sH, -4 * sH), new Vector2(d * 90, -25) * sH, 0, 7 * sH, 18 * sH);
            });
            At(L, () =>
            {
                var cham = foeFeet + new Vector2(-dir * 0.22f * tH, 0);           // khối cắm đất ngay trước đối thủ
                ToNo(foeBody + new Vector2(-dir * 0.12f * tH, 0.12f * tH), foeFeet.y, tH, 2.4f, ToPhach, ToDa);
                ToVong(cham, 125 * sc, 0.65f);
                ToNut(cham, cham + new Vector2(-dir * 0.9f * tH, 6 * sc), 0.16f, sc);
                ToNut(cham, cham + new Vector2(dir * 0.7f * tH, -4 * sc), 0.16f, sc);
                // soi trong game 2026-11-17: cột cao bằng đối thủ nằm sau nó thì bị đối thủ và thân tướng (vừa nhảy tới) che hết: hai cột bên
                // dời ra ngoài thân (±0,7 × đối thủ quanh chân nó), cột giữa sau lưng đối thủ cao 1,4 × để trồi hẳn lên trên đầu
                for (int i = 0; i < 3; i++)
                {
                    var at = foeFeet + new Vector2((i - 1) * 0.7f * tH, i == 1 ? 2 : 4);
                    float h = (i == 1 ? 1.4f : 0.8f) * tH, w = (i == 1 ? 0.36f : 0.24f) * tH;
                    var q = new P { pos = at, life = 0.55f, group = Back, sz = h, wd = w, ang = (i - 1) * 14 };
                    q.draw = (z, kk, buf) =>
                    {
                        float t = kk * z.life;
                        float g = t < 0.07f ? 1.15f * EaseOut(t / 0.07f) : t < 0.13f ? 1.15f - 0.15f * (t - 0.07f) / 0.06f : 1 - SmoothStep(0.72f, 1, kk);
                        float hh = z.sz * g;
                        if (hh < 2) return;
                        float a = z.ang * Mathf.Deg2Rad;
                        DrawPhaLe(buf, z.group, z.pos + new Vector2(Mathf.Sin(a), -Mathf.Cos(a)) * (hh * 0.5f), new Vector2(Mathf.Sin(a), -Mathf.Cos(a)), hh, z.wd);
                    };
                    q.onDeath = (z, s3) => ToNo(z.pos + new Vector2(0, -0.4f * z.sz), foeFeet.y, tH, 0.8f, ToPhach, ToPhach2);
                    Add(q);
                }
            });
            At(ThiemVe2 * k, () =>
            {
                ToVong(casterFeet, 75 * sH);
                Shake?.Invoke(0.12f);
            });
            At(ThiemGam2 * k, () => Shake?.Invoke(0.1f));
            return L;
        }

        // Sa Long dạng 1, CHIÊU CUỐI: giơ vuốt gồng (cát hút về vuốt), nện đất (vòng bụi, vết nứt chạy tới đối thủ), cột sa thạch nhỏ bên hông
        // đối thủ rồi cột vừa sau lưng nó trồi cao hơn đầu (khung trúng); cả hai lớp sau đối thủ (không che con bị trúng)
        public float NLongCot1(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / LongSkill1, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            float t0 = T;
            Func<float, Vector2> vuot = t => ToSan(casterFeet, casterH, dir, ToDiem(LongVuotSkill1, LongGong1, 0.1f, (t - t0) / k));
            Every(LongGong1 * k, (LongNen1 - 0.1f) * k, 30, x =>
            {
                float a = U(0, 6.28f);
                var p0 = vuot(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.6f) * (U(40, 65) * sH);
                ToHut(p0, vuot, 0.3f, U(2.2f, 3.8f) * sH, U(0, 1) < 0.5f ? ToCat : ToCat2, 1.5f);
            });
            var nen = ToSan(casterFeet, casterH, dir, LongNenP1);
            nen.y = casterFeet.y;
            At(LongNen1 * k, () =>
            {
                ToVong(nen, 80 * sH, 0.5f);
                for (int d = -1; d <= 1; d += 2)
                    ToBui(nen + new Vector2(d * 26 * sH, -4 * sH), new Vector2(d * 80, -25) * sH, 0, 6 * sH, 15 * sH);
                Shake?.Invoke(0.22f);
                ToNut(nen, foeFeet + new Vector2(dir * 0.1f * tH, 2), 0.16f * k, sc);
            });
            // soi trong game 2026-11-17: cột nhỏ phía bên mình và cột vừa 1,2 × bị đối thủ che: cột nhỏ dời ra phía xa (ngoài thân), cột vừa
            // cao 1,35 × (dạng 2: 1,45 ×)
            At(LongCot1a * k, () =>
            {
                ToCot(foeFeet + new Vector2(dir * 0.66f * tH, 4 * sc), 0.24f * tH, 0.78f * tH, 0.3f, Back, sc);
                Shake?.Invoke(0.14f);
                ToNo(foeFeet + new Vector2(dir * 0.66f * tH, -0.5f * tH), foeFeet.y, tH, 0.6f, ToCat2, ToSaThach);
            });
            At(L, () =>
            {
                ToCot(foeFeet + new Vector2(dir * 0.08f * tH, 2 * sc), 0.38f * tH, 1.35f * tH, 0.45f, Back, sc);
                ToNo(foeBody + new Vector2(0, 10 * sc), foeFeet.y, tH, 1.6f, ToCat, ToCat2);
            });
            return L;
        }

        // ================= Sơn Viên (phu_van; rig quy_nui_1, ArtGen/Spine/quy_nui_rig.py) =================
        static readonly float[] VienDam = { 0.28f, 0.54f, 0.94f };      // ba cú đấm, cú cuối = khung trúng
        const float VienCast = 0.72f, VienSkill = 2.02f;
        const float VienTu0 = 0.15f, VienTu1 = 1.15f, VienNen1 = 1.32f, VienNen2 = 1.62f, VienBayChan = 0.36f, VienBayTang = 0.42f;
        static readonly Vector2 VienNen = new Vector2(0.074f, 0.022f);  // hai nắm đấm nện đất (cast 0,72)
        static readonly Vector2[] VienTay = { new Vector2(0.125f, 1.146f), new Vector2(0.125f, 1.159f), new Vector2(0.125f, 1.183f), new Vector2(0.125f, 1.204f),
            new Vector2(0.142f, 1.219f), new Vector2(0.109f, 1.243f), new Vector2(0.109f, 1.257f), new Vector2(0.144f, 1.259f), new Vector2(0.252f, 1.245f),
            new Vector2(-0.055f, 1.374f), new Vector2(-0.119f, 1.363f), new Vector2(-0.123f, 1.356f), new Vector2(-0.048f, 1.328f), new Vector2(0.156f, 1.160f),
            new Vector2(-0.109f, 1.338f), new Vector2(0.134f, 1.183f), new Vector2(0.139f, 1.135f), new Vector2(0.202f, 1.219f), new Vector2(0.264f, 1.255f),
            new Vector2(0.157f, 1.232f), new Vector2(0.104f, 1.227f) };   // giữa tảng đá trên hai tay phụ, 0,1 → 2,1 bước 0,1

        // ĐÒN THƯỜNG: lao tới liên hoàn ba đấm: hai cú nhỏ, cú cuối nặng có vòng bụi
        public float NVienDam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead), k = L / VienDam[2], dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f;
            for (int i = 0; i < 3; i++)
            {
                int j = i;
                At(VienDam[j] * k, () =>
                {
                    bool cuoi = j == 2;
                    ToNo(foeBody + new Vector2(-dir * 0.12f * tH, 0) + U2(-10, 10) * sc, foeFeet.y, tH, cuoi ? 1.4f : 0.6f, ToDa, ToDa2);
                    if (cuoi) ToVong(foeFeet, 80 * sc);
                    else Shake?.Invoke(0.12f);
                });
            }
            return L;
        }

        // CHIÊU MANA: hai nắm đấm nện đất (vòng bụi, bụi hai bên), sóng chấn gai đá chạy dọc đất tới đối thủ, hất trúng
        public float NVienChan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead), dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            At(L, () =>
            {
                var m = ToSan(casterFeet, casterH, dir, VienNen);
                var g = new Vector2(m.x, casterFeet.y);
                ToVong(g, 95 * sH, 0.5f);
                for (int d = -1; d <= 1; d += 2)
                    ToBui(g + new Vector2(d * 30 * sH, -4 * sH), new Vector2(d * 90, -30) * sH, 0, 7 * sH, 18 * sH);
                Shake?.Invoke(0.3f);
                ToSongChan(g + new Vector2(dir * 0.15f * casterH, -2), foeFeet + new Vector2(dir * 0.07f * tH, 2), VienBayChan, sc,
                    () => ToNo(foeBody + new Vector2(0, 14 * sc), foeFeet.y, tH, 1.8f, ToDa, ToDa2));
            });
            return L + VienBayChan;
        }

        // CHIÊU CUỐI: TẢNG ĐÁ KHỔNG LỒ lớn dần trên hai tay phụ (đá từ mặt đất bay lên nhập vào), hai nhịp nện gồng, bốn tay ném: tảng bay
        // vồng xuống đối thủ, vỡ: dăm, vòng bụi lớn, mưa đá nhỏ
        public float NVienTang(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.5f, lead), k = L / VienSkill, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            float t0 = T;
            // bán kính như bản xem trước (tho5_fx.quy_nui_skill: rig 70 → 220 đơn vị × 1,8 "khổng lồ", con cao ~1005): 0,125 → 0,39 chiều cao
            Func<float, float> rLuc = t => (0.125f + 0.27f * Mathf.Pow(Mathf.Clamp01((t / k - VienTu0) / (VienTu1 - VienTu0)), 1.3f)) * casterH;
            Func<float, Vector2> tay = t =>
            {
                var p = ToSan(casterFeet, casterH, dir, ToDiem(VienTay, 0.1f, 0.1f, t / k));
                p.y = Mathf.Max(p.y, rLuc(t) + 6);                          // không vượt mép trên sân
                return p;
            };
            int seed = rng.Next(4);
            At(VienTu0 * k, () =>
            {
                var tang = new P { pos = tay(VienTu0 * k), life = L - VienTu0 * k, group = Front, seed = seed, crust = true, ph = 44 };
                tang.upd = (q, dt, s) =>
                {
                    float t = s.T - t0;
                    q.sz = rLuc(t);
                    q.pos = tay(t);
                    q.vel = Vector2.zero;
                    q.ang = 8 * Mathf.Sin(t * 3);
                };
                tang.draw = DrawTang;
                Add(tang);
            });
            Every((VienTu0 + 0.05f) * k, VienTu1 * k, 30, x =>
            {
                var p0 = casterFeet + new Vector2(dir * U(-0.7f, 0.45f) * casterH, U(-6, 4) * sH);
                ToHut(p0, s => tay(s - t0), 0.38f, U(4, 8) * sH, U(0, 1) < 0.5f ? ToDa : ToDa2, 1.5f, 40 * sH);
                if (U(0, 1) < 0.4f) ToBui(p0, new Vector2(U(-30, 30), -40) * sH, 0.45f, 3 * sH, 7 * sH, Back);
            });
            foreach (float tn in new[] { VienNen1, VienNen2 })
                At(tn * k, () =>
                {
                    ToVong(casterFeet + new Vector2(-dir * 0.13f * casterH, 0), 90 * sH);
                    Shake?.Invoke(0.18f);
                    var m = tay(tn * k);
                    for (int i = 0; i < 4; i++) ToSoi(m + U2(-30, 30) * sH, new Vector2(U(-80, 80), 40) * sH, 4 * sH, ToDa, casterFeet.y + 2);
                });
            At(L, () =>
            {
                ToTangBay(tay(L), foeBody + new Vector2(0, 10 * sc), VienBayTang, rLuc(L), 90 * sc, true, p =>
                {
                    ToNo(p, foeFeet.y, tH, 2.8f, ToDa, ToPhach);
                    ToVong(foeFeet, 130 * sc, 0.7f);
                    Shake?.Invoke(0.3f);
                    for (int i = 0; i < 7; i++)
                        At(0.08f + 0.05f * i, () =>
                        {
                            var dich = foeBody + new Vector2(U(-50, 50), U(0, 30)) * sc;
                            ToTangBay(foeBody + new Vector2(U(-60, 60) * sc, -260 * sc), dich, 0.28f, 6 * sc, 10 * sc, false,
                                q => ToNo(q, foeFeet.y, tH, 0.5f, ToDa, ToDa2));
                        });
                }, 0.85f, seed);
            });
            return L + VienBayTang;
        }
    }
}
