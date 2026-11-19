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
// Hình hệ Thổ (vfx-petclash mục 5): khối đá góc cạnh, trồi lên, rơi nặng, nảy một lần rồi nằm; bụi tròn nâu be; sỏi. Không dùng ảnh
// đá, vết nứt có mạch dung nham của bộ Hỏa (hat_rock_*, hat_crack_*), không dùng chớp nước BurstFlash (bảng W là màu nước): chớp trúng
// là sao gai màu kem. Thân khối lớn (lưỡi cát, lốc cát, cột sa thạch, gai sóng chấn, vết nứt) là mảng liền (MSolid / MFill); hạt chỉ
// làm mép, bụi, dăm. Rung lúc trúng do rig khai (impactShake); ở đây chỉ rung cho nhịp không phải khung trúng (dậm, nện, đáp).
// DẠNG 2 (2026-11-17, rig riêng mỗi dạng; quai/doi_tho5_dang2.py): Thạch Giáp cong_da_2 (3528), Sa Tích than_lan_cat_2 (3530), Tê Thiềm
// thu_da_2 (3526); Sa Long thêm DẠNG 1 rong_cat_non (3529), dạng 2 là rig rong_cat_1 cũ. Mã dạng 2: n_*2 (hàm cũ thêm tham số dang, mốc
// và bảng vị trí đo trên rig dạng 2 ở inbox/<mã>_2_ghichu.md); Sa Long dạng 1: n_long_*1. Thang cỡ dạng 1 < dạng 2 (vfx-petclash mục 6).
// KHUNG VẼ SẴN (2026-11-19, HatFlip.cs + HatFbTho.cs): bụi (ToCum, ToNo, đuôi bụi, dòng bụi), khói than (ToKhoiCum), gai / cột đá trồi (ToCot,
// ToSongChan, TrungGaiDa, cột pha lê Tê Thiềm dạng 2) dùng khung vẽ sẵn khi đã nhập ảnh hat_fb_*; chưa nhập thì hạt cũ y như trước. Nhịp, chỗ,
// cỡ, giờ trúng giữ nguyên; sỏi, dăm, chớp, vòng va chạm, hố, vết nứt, lưỡi cát, lốc cát, tảng đá, mảnh pha lê vẫn là hạt / mảng liền cũ.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // bảng màu TƯƠI (người dùng 2026-11-18: "màu hơi tối, không hợp theme ... màu tươi hơn"): bụi be sáng #E8C99A, cát #D9A866, nâu đất
        // #A86B3C, viền đậm #7A4A26; hổ phách #FFB23A. Ảnh hạt xám ~236 nhân màu còn ~0,93 nên màu hạt ảnh đặt sáng hơn màu đích một nấc.
        static readonly Color ToBuiC = C(244, 214, 166), ToBuiC2 = C(228, 180, 112);                      // bụi đất: be sáng, cát
        static readonly Color ToNau = C(168, 107, 60), ToVien = C(122, 74, 38);                           // nâu đất (đáy cụm bụi), viền đậm
        static readonly Color ToDa = C(206, 172, 128), ToDa2 = C(164, 114, 70), ToDa3 = C(240, 220, 182);  // đá be ấm: giữa, nâu, mặt sáng
        static readonly Color ToPhach = C(255, 178, 58), ToPhach2 = C(255, 228, 150);                      // pha lê hổ phách: mặt chính, mặt sáng
        static readonly Color ToGom = C(214, 112, 60), ToGom2 = C(242, 160, 98);                           // đất nung (áo phiến Sa Tích)
        static readonly Color ToCat = C(238, 204, 142), ToCat2 = C(217, 168, 102), ToCat3 = C(252, 238, 204), ToCatSam = C(168, 107, 60);
        static readonly Color ToSaThach = C(244, 218, 166), ToSon = C(220, 138, 64), ToNutC = C(96, 60, 36);
        static readonly Color ToKem = C(255, 246, 214);                                                    // chớp trúng
        static readonly Color ToKhoi0 = C(58, 50, 46), ToKhoi1 = C(110, 102, 98), ToKhoi2 = C(168, 162, 158), ToKhoi3 = C(212, 208, 204); // khói than → xám

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

        // ảnh hạt mới (bộ kr_ đang vẽ, Assets/03 Art/Fx/Hat, tiền tố hat_): chưa nhập thì dùng ảnh cũ, không lỗi
        Sprite SK(string moi, string cu) => S(moi) ?? S(cu);

        // ---------- bụi, khói: CỤM mềm nhiều múi (người dùng 2026-11-18: "khói nhìn rải rác chưa thành cụm, chưa mềm") ----------
        // Một hạt = một cụm nhiều múi (ảnh kr_khoi, dự phòng foam); hai tông phẳng: đỉnh sáng, đáy đậm (ảnh kr_khoiday đè lên; dự phòng: lớp
        // đậm lót dưới, lớp sáng nhỏ hơn lệch lên). Mọi hạt cùng lớp chung một viền mực nên các cụm chồng nhau hoà thành một khối. Nhịp KR5: to gần
        // đủ ngay (18 % đời), bay lên, cụm to TÁCH thành ba cụm nhỏ ở ~42 % đời, co dần, chỉ mờ ở 35 % cuối.
        void DrawCumTo(P q, float k, List<Item> buf, Color day, float aMax)
        {
            const float grow = 0.18f;
            float r = k < grow ? q.r0 + (q.r1 - q.r0) * EaseOut(k / grow) : q.r1 * (1 - 0.58f * SmoothStep(grow, 1, k));
            float a = aMax * (1 - SmoothStep(0.65f, 1, k));
            if (r < 1 || a < 0.03f) return;
            int i = q.seed & 3;
            float d = 2 * r;
            Sprite van = SK("kr_khoi_" + i, "foam_" + i), dd = S("kr_khoiday_" + i);
            Put(buf, q.group, 30, SK("kr_khois_" + i, "foams_" + i), Ink, q.pos, d + 3.5f, 1, q.ang, a * Mathf.Min(1, 1.6f - 1.6f * SmoothStep(0.5f, 1, k)));
            if (dd != null)
            {
                Put(buf, q.group, 31, van, q.col, q.pos, d, 1, q.ang, a);
                Put(buf, q.group, 31.5f, dd, day, q.pos, d, 1, q.ang, a);
            }
            else
            {
                Put(buf, q.group, 31, van, day, q.pos, d, 1, q.ang, a);
                Put(buf, q.group, 31.5f, van, q.col, q.pos + new Vector2(0, -0.13f * r), 0.82f * d, 1, q.ang, a);
            }
        }

        // cụm bụi đất be sáng (đáy cát đậm). tach: cụm to (r1 ≥ 11) vỡ thành ba cụm nhỏ giữa đời
        P ToBui(Vector2 pos, Vector2 vel, float life = 0, float r0 = 5, float r1 = 14, int group = Front, bool tach = true)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life > 0 ? life : U(0.5f, 0.75f), drag = 2.6f, acc = new Vector2(0, -55), seed = rng.Next(8), r0 = r0, r1 = r1,
                group = group, ang = U(-22, 22), spin = U(-16, 16), spinDrag = 1.2f, ph = U(0, 6.28f), crust = tach && r1 >= 11
            };
            p.col = (p.seed & 4) != 0 ? ToBuiC : ToCat3;
            p.upd = (q, dt, s) =>
            {
                q.vel.x += Mathf.Sin(q.age * 4 + q.ph) * 14 * dt;
                if (!q.crust || q.age < 0.42f * q.life) return;
                q.crust = false;                                                 // tách cụm: ba cụm con phủ đúng hình cụm mẹ rồi toả ra
                float k = q.age / q.life, rc = q.r1 * (1 - 0.58f * SmoothStep(0.18f, 1, k)), a0 = s.U(0, 6.28f);
                for (int j = 0; j < 3; j++)
                {
                    float a = a0 + 2.094f * j;
                    var d = new Vector2(Mathf.Cos(a), 0.75f * Mathf.Sin(a));
                    var c = s.ToBui(q.pos + d * (0.42f * rc), q.vel * 0.5f + d * (0.9f * rc + 8) + new Vector2(0, -12), (q.life - q.age) * s.U(1.0f, 1.25f),
                        0.6f * rc, 0.62f * rc, q.group, false);
                    c.col = q.col;
                    c.seed = (q.seed + j + 1) & 7;
                }
                q.dead = true;
            };
            p.draw = (q, k, buf) => DrawCumTo(q, k, buf, Color.Lerp(q.col, ToNau, 0.4f), 1);
            return Add(p);
        }

        // khói than của nổ lớn (đen ngả xám, có tro), cùng dáng cụm: đỉnh nhạt, đáy đậm; bay lên, tách cụm, tan dần không vụt tắt
        P ToKhoi(Vector2 pos, Vector2 vel, float life, float r0, float r1, int group = Back, bool tach = true, float tuoi0 = 0)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = 1.5f, acc = new Vector2(0, -70), seed = rng.Next(8), r0 = r0, r1 = r1, group = group,
                ang = U(-20, 20), spin = U(-12, 12), spinDrag = 1, ph = U(0, 6.28f), crust = tach && r1 >= 14, R1 = tuoi0
            };
            p.upd = (q, dt, s) =>
            {
                q.vel.x += Mathf.Sin(q.age * 3 + q.ph) * 18 * dt;
                q.vel.y -= 50 * (q.age / q.life) * dt;
                if (!q.crust || q.age < 0.45f * q.life) return;
                q.crust = false;
                float k = q.age / q.life, rc = q.r1 * (1 - 0.58f * SmoothStep(0.18f, 1, k)), a0 = s.U(0, 6.28f);
                for (int j = 0; j < 3; j++)
                {
                    float a = a0 + 2.094f * j;
                    var d = new Vector2(Mathf.Cos(a), 0.75f * Mathf.Sin(a));
                    s.ToKhoi(q.pos + d * (0.42f * rc), q.vel * 0.6f + d * (0.7f * rc + 6), (q.life - q.age) * s.U(1.0f, 1.2f), 0.6f * rc, 0.62f * rc,
                        q.group, false, q.R1 + 0.45f * 0.7f);                    // con nối tiếp màu của mẹ
                }
                if (s.U(0, 1) < 0.5f) s.Ash(q.pos, null, q.group);
                q.dead = true;
            };
            p.draw = (q, k, buf) =>
            {
                float tu = Mathf.Clamp01(q.R1 + k * 0.7f);                      // than đen → xám → xám nhạt theo tuổi
                var col = tu < 0.3f ? Color.Lerp(ToKhoi0, ToKhoi1, tu / 0.3f) : tu < 0.65f ? Color.Lerp(ToKhoi1, ToKhoi2, (tu - 0.3f) / 0.35f)
                    : Color.Lerp(ToKhoi2, ToKhoi3, (tu - 0.65f) / 0.35f);
                q.col = col;
                DrawCumTo(q, k, buf, Color.Lerp(col, ToKhoi0, 0.5f), 0.92f);
            };
            return Add(p);
        }

        // cụm bụi chồng nhiều múi (to, vừa, nhỏ dính nhau, một viền mực ngoài): múi giữa + n−1 múi quanh, toả nhẹ rồi tách dần.
        // khung vẽ sẵn (2026-11-19): có khung "khoi" thì MỘT cụm khói vẽ sẵn nhuộm bụi (tint, mặc định bụi đất) cao (2,6 + 0,4 n) R (rộng ~ cao,
        // tức ~3,6 R với n = 3: rộng hơn cụm múi cũ) thay n múi hạt (ít cụm mà to, mềm, tự tách mảnh rồi tan); dat: c ở sát đất (chân cụm ở mặt
        // đất) hay giữa không trung (tâm cụm ở c)
        void ToCum(Vector2 c, Vector2 vel, float R, int n, int group = Front, float life = 0, Color? tint = null, bool dat = true)
        {
            if (HasFb("khoi"))
            {
                float h = R * (2.6f + 0.4f * n);
                FbBui(c + new Vector2(0, (dat ? 0.1f : 0.42f) * h), vel * 0.6f, h, group, tint ?? FbBuiC, life > 0 ? Mathf.Clamp(0.85f / life, 0.6f, 2.4f) : 1.4f,
                    0.92f, dat ? 1 : 3);                                       // giữa không trung: bỏ ba khung đầu (cụm nhỏ ở chân) cho cụm bung quanh c
                return;
            }
            float a0 = U(0, 6.28f);
            ToBui(c, vel, life, 0.6f * R, R, group);
            for (int i = 1; i < n; i++)
            {
                float a = a0 + 6.283f * i / Mathf.Max(1, n - 1) + U(-0.4f, 0.4f);
                var d = new Vector2(Mathf.Cos(a), 0.7f * Mathf.Sin(a));
                float rr = R * U(0.5f, 0.75f);
                ToBui(c + d * (0.55f * R), vel * U(0.8f, 1.1f) + d * (U(16, 34) * R / 14f), life > 0 ? life * U(0.85f, 1.05f) : 0, 0.55f * rr, rr, group, false);
            }
        }

        // cụm khói than chồng nhiều múi (nổ lớn). khung vẽ sẵn (2026-11-19): một cụm khói vẽ sẵn nhuộm khói than, tâm cụm ở c
        void ToKhoiCum(Vector2 c, Vector2 vel, float R, int n, float life, int group = Back)
        {
            if (HasFb("khoi"))
            {
                float h = R * (2.6f + 0.4f * n);
                FbBui(c + new Vector2(0, 0.4f * h), vel * 0.6f, h, group, FbKhoiDen, Mathf.Clamp(0.95f / life, 0.4f, 1.6f), 0.95f, 2, 32);
                return;
            }
            float a0 = U(0, 6.28f);
            ToKhoi(c, vel, life, 0.6f * R, R, group);
            for (int i = 1; i < n; i++)
            {
                float a = a0 + 6.283f * i / Mathf.Max(1, n - 1) + U(-0.4f, 0.4f);
                var d = new Vector2(Mathf.Cos(a), 0.7f * Mathf.Sin(a));
                float rr = R * U(0.55f, 0.8f);
                ToKhoi(c + d * (0.55f * R), vel * U(0.8f, 1.1f) + d * (U(14, 30) * R / 16f), life * U(0.85f, 1.05f), 0.55f * rr, rr, group, false);
            }
        }

        // ---------- sỏi, dăm: nhỏ, đi theo CHÙM lệch cỡ (người dùng 2026-11-18: "đốm ... đơn lẻ và to quá") ----------
        // hình sỏi: khối tròn méo viền mực dẹt theo hgt, mặt sáng nhỏ lệch lên (đọc ra khối đá), mờ ở 30 % cuối đời
        void DrawSoiP(P q, float k, List<Item> buf)
        {
            float a = 1 - SmoothStep(0.7f, 1, k);
            if (q.sz < 0.8f || a < 0.03f) return;
            int si = q.seed & 3;
            Put(buf, q.group, 45, S("solid_" + si), Ink, q.pos, 2 * q.sz + 3, q.hgt, q.ang, a);
            Put(buf, q.group, 45.1f, S("blob_" + si), q.col, q.pos, 2 * q.sz, q.hgt, q.ang, a);
            if (q.sz >= 3.2f)
                Put(buf, q.group, 45.2f, S("blob_" + ((si + 1) & 3)), Color.Lerp(q.col, ToKem, 0.5f), q.pos + new Vector2(-0.22f, -0.28f) * q.sz, 0.95f * q.sz,
                    q.hgt, q.ang, a);
        }

        // sỏi / dăm đá văng: rơi nặng, chạm đất nảy MỘT lần rồi nằm, mờ dần
        P ToSoi(Vector2 pos, Vector2 vel, float r, Color col, float ground, float life = 0, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life > 0 ? life : U(0.65f, 0.95f), acc = new Vector2(0, 1050), drag = 0.6f, spin = U(-800, 800),
                spinDrag = 0.4f, ang = U(0, 360), seed = rng.Next(4), sz = r, col = col, group = group, ground = ground, bounce = 0.3f,
                hgt = U(1.0f, 1.45f)
            };
            p.draw = DrawSoiP;
            return Add(p);
        }

        // chùm dăm lệch cỡ bay cùng nhau (to / vừa / nhỏ, vận tốc gần nhau) thay cho hạt lẻ
        void ToSoiCum(Vector2 pos, Vector2 vel, float r, Color col, Color col2, float ground, int group = Front)
        {
            var n = Unit(new Vector2(-vel.y, vel.x));
            ToSoi(pos, vel, r, col, ground, 0, group);
            ToSoi(pos + n * (0.9f * r), vel * U(0.84f, 0.94f) + n * U(-22, 22), 0.62f * r, col2, ground + U(-2, 3), 0, group);
            ToSoi(pos - n * (0.7f * r), vel * U(1.04f, 1.14f) + n * U(-22, 22), 0.42f * r, col, ground + U(-2, 3), 0, group);
        }

        // ---------- va chạm ----------
        // chớp trúng (ảnh kr_chop, dự phòng sao gai): kem viền mực, lõi hổ phách nhạt; GIỮ đủ cỡ 2 khung đầu (KR5: chớp 1–2 khung) rồi co nhanh
        void ToChop(Vector2 c, float size, int group = Front, float life = 0.12f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = rng.Next(4), sz = size };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (q.age < 0.045f ? 1.08f : 1.08f - 0.5f * SmoothStep(0.045f, q.life, q.age));
                float a = 1 - SmoothStep(0.75f, 1, k);
                int i = q.seed, j = (q.seed + 1) & 3;
                Put(buf, q.group, 60, SK("kr_chops_" + i, "bursts_" + i), Ink, q.pos, s + 5, 1, q.ang, a);
                Put(buf, q.group, 60.1f, SK("kr_chop_" + i, "burst_" + i), ToKem, q.pos, s, 1, q.ang, a);
                Put(buf, q.group, 60.2f, SK("kr_chop_" + j, "burst_" + j), ToPhach2, q.pos, 0.46f * s, 1, q.ang + 20, a);
            };
            Add(p);
        }

        // dải vòng elip (mảng liền, KHÔNG viền: vòng mảnh có viền mực thì thành vòng đen) bán kính r, dày 2w, dẹt sq, từ góc a0 dài span
        void VongMesh(int g, float layer, Vector2 c, float r, float w, float sq, Color col, float a, float a0, float span, int n = 24)
        {
            int s0 = mp.Count;
            for (int i = 0; i <= n; i++)
            {
                float t = a0 + span * i / n;
                mp.Add(c + new Vector2(Mathf.Cos(t) * (r + w), Mathf.Sin(t) * (r + w) * sq));
            }
            int s1 = mp.Count;
            for (int i = 0; i <= n; i++)
            {
                float t = a0 + span * i / n;
                mp.Add(c + new Vector2(Mathf.Cos(t) * Mathf.Max(0, r - w), Mathf.Sin(t) * Mathf.Max(0, r - w) * sq));
            }
            MRibbon(g, layer, s0, s1, n + 1, col, a);
        }

        // elip phẳng mép gợn (vệt, hố trên đất)
        void ElipMesh(int g, float layer, Vector2 c, float r, float sq, Color col, float a, float ph, int n = 18)
        {
            int s0 = mp.Count;
            for (int i = 0; i < n; i++)
            {
                float t = 6.2832f * i / n, rr = r * (1 + 0.08f * Mathf.Sin(t * 3 + ph) + 0.04f * Mathf.Sin(t * 5 + 2 * ph));
                mp.Add(c + new Vector2(Mathf.Cos(t) * rr, Mathf.Sin(t) * rr * sq));
            }
            MFill(g, layer, s0, n, col, a, true);
        }

        // vòng va chạm quanh chỗ chạm: vòng mảnh kem không viền, nở nhanh, mỏng dần, tan (0,2 s)
        void ToVongVa(Vector2 c, float R, float life = 0.2f, float squash = 0.9f, int group = Front)
        {
            var p = new P { pos = c, life = life, group = group, sz = R, hgt = squash, ph = U(0, 6.28f) };
            p.draw = (q, k, buf) =>
            {
                float r = q.sz * (0.3f + 0.7f * EaseOut(k)), w = Mathf.Max(0.7f, 0.07f * q.sz * (1 - k)), a = 1 - SmoothStep(0.45f, 1, k);
                if (a < 0.03f) return;
                VongMesh(q.group, 59, q.pos, r, w, q.hgt, ToKem, a, q.ph, 6.2832f * (0.86f - 0.3f * k), 20);   // đứt một khe, rộng dần
            };
            Add(p);
        }

        // bông va chạm ở chỗ đạn / tia chạm thân (ảnh kr_tiadau toé về +x; dự phòng chùm gai tuft chĩa lên): toé NGƯỢC hướng bay chếch lên,
        // ba lớp mực / màu / lõi kem, bật đủ cỡ trong 2 khung rồi vỡ (co, mờ) trong ~0,16 s
        void ToBong(Vector2 c, Vector2 huong, float size, Color col, int group = Front, float life = 0.16f)
        {
            var ra = Unit(-Unit(huong) + new Vector2(0, -0.5f));
            var p = new P { pos = c, life = life, group = group, sz = size, aim = ra, col = col, seed = rng.Next(4) };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (q.age < 0.04f ? 0.75f + 6f * q.age : 0.99f + 0.12f * k) * (1 - 0.35f * SmoothStep(0.6f, 1, k));
                float a = 1 - SmoothStep(0.55f, 1, k);
                int i = q.seed;
                bool moi = S("kr_tiadau_" + i) != null;
                float ang = moi ? VelAng(q.aim) : TipAngle(q.aim);
                Sprite den = moi ? SK("kr_tiadaus_" + i, "kr_tiadau_" + i) : S("tufts_" + i), van = moi ? S("kr_tiadau_" + i) : S("tuft_" + i);
                var o = q.aim * (0.32f * s);                                      // gốc bông ở chỗ chạm, thân toé ra ngoài
                Put(buf, q.group, 58, den, Ink, q.pos + o, s + 5, 1, ang, a);
                Put(buf, q.group, 58.1f, van, q.col, q.pos + o, s, 1, ang, a);
                Put(buf, q.group, 58.2f, van, ToKem, q.pos + o * 0.75f, 0.58f * s, 1, ang, a);
            };
            Add(p);
        }

        // sóng đất (KR5): 3–4 cung elip dẹt KHÔNG viền trên lớp đất, nở nhanh, mỏng dần, khe rộng dần (đứt đoạn), tan; dải cát đậm hơn bên trong
        // để nổi trên nền cát sáng
        void ToVong(Vector2 feet, float R1, float life = 0.45f)
        {
            var p = new P { pos = feet + new Vector2(0, 2), life = life, group = Floor, sz = R1, ph = U(0, 6.28f), seed = 3 + rng.Next(2) };
            p.draw = (q, k, buf) =>
            {
                float r = q.sz * (0.22f + 0.78f * EaseOut(k / 0.85f)), w = Mathf.Max(0.7f, q.sz * 0.05f * (1 - 0.8f * k)), a = 1 - SmoothStep(0.5f, 1, k);
                if (a < 0.03f) return;
                int n = q.seed;
                for (int j = 0; j < n; j++)
                {
                    float a0 = q.ph + 6.2832f * j / n, span = 6.2832f / n * (0.8f - 0.3f * k);
                    VongMesh(Floor, 30.4f + j * 0.001f, q.pos, r, w, 0.3f, ToCat3, a, a0, span, 10);
                    VongMesh(Floor, 30.3f + j * 0.001f, q.pos, r * 0.86f, w * 1.5f, 0.3f, ToCat2, 0.55f * a, a0 + 0.2f, span * 0.8f, 10);
                }
            };
            Add(p);
        }

        // hố / vệt nện trên đất (decal KR5): elip nâu đất mờ trong vành be sáng, nằm ~giu giây rồi mờ 0,6 s
        void ToHo(Vector2 feet, float R, float giu = 0.9f)
        {
            var p = new P { pos = feet + new Vector2(0, 2), life = 0.1f + giu + 0.6f, group = Floor, sz = R, ph = U(0, 6.28f) };
            p.draw = (q, k, buf) =>
            {
                float g = EaseOut(q.age / 0.1f), a = 1 - SmoothStep(0.1f + giu, q.life, q.age);
                if (a < 0.03f) return;
                ElipMesh(Floor, 4, q.pos, q.sz * g * 1.15f, 0.32f, ToBuiC, 0.7f * a, q.ph);
                ElipMesh(Floor, 4.01f, q.pos + new Vector2(0, 1), q.sz * g * 0.9f, 0.28f, ToNau, 0.45f * a, q.ph + 1);
            };
            Add(p);
        }

        // một cú trúng hệ Thổ (KR5: chớp 1–2 khung → khối + đá văng → bụi cụm tách dần): chớp kem ở chỗ chạm, vòng va chạm mảnh, bông va chạm
        // toé ngược hướng đòn (khi biết huong), chùm dăm lệch cỡ văng nửa trên chếch về phía kẻ đánh rồi rơi nảy một lần, một cụm bụi nhiều múi sau
        // thân (không che con bị trúng), sát đất thì thêm cụm thấp. muc: 1 vừa, 2 nặng; c1, c2: màu dăm; huong: hướng đòn (từ kẻ đánh tới)
        void ToNo(Vector2 c, float ground, float tH, float muc, Color c1, Color c2, Vector2 huong = default)
        {
            float sc = tH / 150f, m = Mathf.Sqrt(muc);
            bool coHuong = huong.sqrMagnitude > 1e-4f;
            ToChop(c, 0.3f * tH * m);
            ToVongVa(c, 0.34f * tH * m);
            if (coHuong) ToBong(c, huong, 0.4f * tH * Mathf.Min(1.35f, m), Color.Lerp(c1, ToKem, 0.35f));
            var ve = Unit((coHuong ? -Unit(huong) * 0.6f : Vector2.zero) + new Vector2(0, -1));
            float a0 = Mathf.Atan2(ve.y, ve.x);
            int n = Mathf.Clamp(Mathf.RoundToInt(2 * muc), 1, 5);
            for (int i = 0; i < n; i++)
            {
                float a = a0 + ((i + 0.5f) / n - 0.5f) * 2.3f + U(-0.18f, 0.18f);
                var v = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * (U(170, 280) * (0.8f + 0.2f * muc) * sc);
                ToSoiCum(c, v, U(3f, 4.4f) * (0.85f + 0.15f * muc) * sc, (i & 1) == 0 ? c1 : c2, (i & 1) == 0 ? c2 : c1, ground + U(-4, 6) * sc,
                    (i & 1) == 0 ? Front : Back);
            }
            // khung vẽ sẵn (2026-11-19): bụi của cú trúng là MỘT cụm khói vẽ sẵn sau thân (cao 0,36 tH × √muc, màu theo dăm), thay hai cụm múi hạt;
            // dời 0,16 tH về phía kẻ đánh (ghép thử: cụm ngay sau giữa thân bị thân che gần hết) và trôi theo hướng đó; cú sát đất thì chân cụm ở
            // mặt đất
            if (HasFb("khoi"))
            {
                float h = 0.36f * tH * m;
                bool satDat = ground - c.y < 0.42f * tH;
                var lui = coHuong ? -Unit(huong) : Vector2.zero;
                var at = c + new Vector2(lui.x * 0.16f * tH, 0);
                FbBui(satDat ? new Vector2(at.x, ground - 2 * sc) : at + new Vector2(0, 0.42f * h), new Vector2(lui.x * U(20, 50) + U(-15, 15), -U(20, 40)) * sc, h,
                    Back, FbTint(c1), muc >= 1.5f ? 1.25f : 1.45f, 0.92f, satDat ? 1 : 3);
                return;
            }
            ToCum(c + new Vector2(0, -4 * sc), new Vector2(U(-20, 20), -U(30, 60)) * sc, 11 * m * sc, muc >= 1.2f ? 4 : 3, Back);
            if (ground - c.y < 0.42f * tH && muc >= 1) ToCum(new Vector2(c.x, ground - 4 * sc), new Vector2(U(-30, 30), -12) * sc, 9 * m * sc, 3, Back);
        }

        // ---------- tụ, hút (người dùng 2026-11-18: "các skill hút khí ... xung quanh tụ cầu cũng đang xấu") ----------
        // hạt bị hút vào một điểm đang dời (miệng, vuốt, tảng đá trên tay): VỆT bụi kéo dài theo vận tốc (ảnh kr_vet đầu tròn +x, dự phòng streakg)
        // hoặc sỏi xoay (35 %); bay XOẮN ỐC vào tâm, nhanh dần (ease-in f^mu, mu ≥ 1,7), hiện dần lúc sinh, co lại NHẬP vào tâm lúc tới.
        // vong: vồng lên giữa đường (đá từ đất bay lên tảng)
        void ToHut(Vector2 p0, Func<float, Vector2> dich, float life, float r, Color col, float mu, float vong = 0)
        {
            var rel = p0 - dich(T);
            float xoay = (U(0, 1) < 0.5f ? -1 : 1) * U(1.1f, 1.9f), mm = Mathf.Max(1.7f, mu);
            var q = new P
            {
                pos = p0, life = life, group = Front, seed = rng.Next(4), sz = r, col = col, spin = U(-600, 600), hgt = U(1, 1.3f), crust = U(0, 1) < 0.35f,
                aim = Unit(-rel)
            };
            q.upd = (z, dt, s) =>
            {
                float f = Mathf.Clamp01(z.age / z.life), g = Mathf.Pow(f, mm), th = xoay * g, cs = Mathf.Cos(th), sn = Mathf.Sin(th);
                var v = rel * (1 - g);
                var cu = z.pos;
                z.pos = dich(s.T) + new Vector2(v.x * cs - v.y * sn, v.x * sn + v.y * cs) + new Vector2(0, -vong * Mathf.Sin(Mathf.PI * f));
                var dv = z.pos - cu;
                if (dt > 0 && dv.sqrMagnitude > 1e-6f)
                {
                    z.aim = dv.normalized;
                    z.vy = Mathf.Lerp(z.vy, dv.magnitude / dt, 0.5f);
                }
                z.vel = Vector2.zero;
            };
            q.draw = (z, k, buf) =>
            {
                float a = Mathf.Min(1, k / 0.18f), co = 1 - SmoothStep(0.82f, 1, k);
                if (a * co < 0.03f) return;
                if (z.crust)
                {
                    int si = z.seed & 3;
                    float rs = z.sz * co;
                    Put(buf, Front, 45, S("solid_" + si), Ink, z.pos, 2 * rs + 3, z.hgt, z.ang, a);
                    Put(buf, Front, 45.1f, S("blob_" + si), z.col, z.pos, 2 * rs, z.hgt, z.ang, a);
                }
                float st = Mathf.Clamp(z.vy / 60f, 1.4f, 4.4f), s2 = (z.crust ? 1.3f : 2.2f) * z.sz * co, ang = VelAng(z.aim);
                var mid = z.pos - z.aim * (0.4f * s2 * st);                        // đầu vệt ở chỗ hạt, thân kéo về sau
                string ten = "kr_vet_" + z.seed, tenS = "kr_vets_" + z.seed, cu = "streakg_" + (z.seed & 1);
                Put(buf, Front, 43, SK(tenS, cu), Ink, mid, s2 + 2.5f, (s2 * st + 2.5f) / (s2 + 2.5f), ang, a * (z.crust ? 0.6f : 1));
                Put(buf, Front, 43.1f, SK(ten, cu), z.col, mid, s2, st, ang, a * (z.crust ? 0.6f : 1));
            };
            Add(q);
        }

        // vòng co về tâm lúc tụ (mảng mảnh không viền): hiện dần, co nhanh dần (ease-in) từ R0 về tâm, dày lên khi khép, tắt ở tâm
        void ToVongCo(Func<float, Vector2> c, float R0, float life, Color col, float squash = 0.85f)
        {
            var p = new P { pos = c(T), life = life, group = Front, sz = R0, hgt = squash, col = col, ph = U(0, 6.28f) };
            p.upd = (z, dt, s) =>
            {
                z.pos = c(s.T);
                z.vel = Vector2.zero;
            };
            p.draw = (z, k, buf) =>
            {
                float g = k * k, r = z.sz * (1 - 0.85f * g), w = Mathf.Max(0.8f, z.sz * (0.018f + 0.05f * g));
                float a = Mathf.Min(1, k / 0.3f) * (1 - SmoothStep(0.86f, 1, k));
                if (a < 0.03f || r < 1.5f) return;
                VongMesh(Front, 42, z.pos, r, w, z.hgt, z.col, 0.9f * a, z.ph - 2 * k, 6.2832f * 0.82f, 22);
            };
            Add(p);
        }

        // đuôi bụi liền cho mảnh của rig bay thẳng từ a tới b trong tb giây (game lái, lớp hạt không đọc được xương): rải cụm đứng tại chỗ theo
        // quãng (KR5: đuôi chia theo quãng nên liền). Rig có thể nhanh dần nên đuôi theo u² của giờ: luôn ở SAU mảnh, không vượt lên trước
        // khung vẽ sẵn (2026-11-19): có khung "khoi" thì đuôi là các cụm khói vẽ sẵn nhuộm theo col, bước gấp đôi, cụm to hơn (chồng nhau thành dải)
        void ToDuoiThang(Vector2 a, Vector2 b, float tb, float r, Color col)
        {
            var dv = Unit(b - a);
            bool fb = HasFb("khoi");
            float len = (b - a).magnitude, buoc = fb ? Mathf.Max(12, 1.8f * r) : Mathf.Max(6, 0.9f * r);
            var tint = FbTint(col == ToCat3 ? ToCat : col);
            var p = new P { pos = a, life = tb, group = Front };
            p.upd = (z, dt, s) =>
            {
                float u = Mathf.Clamp01(z.age / tb), f = u * u * 0.92f;
                while (z.R0 + buoc <= f * len)
                {
                    z.R0 += buoc;
                    var at = a + dv * z.R0 + new Vector2(-dv.y, dv.x) * s.U(-0.25f, 0.25f) * r;
                    if (fb)
                    {
                        float h = 2.6f * r;
                        s.FbBui(at + new Vector2(0, 0.42f * h), new Vector2(s.U(-8, 8), -s.U(6, 18)), h, Front, tint, 2f, 0.85f, 4);
                        continue;
                    }
                    var c = s.ToBui(at, new Vector2(s.U(-12, 12), -s.U(10, 30)), s.U(0.34f, 0.46f), 0.45f * r, 0.8f * r, Front, false);
                    c.col = col;
                }
            };
            Add(p);
        }

        // mảnh pha lê hổ phách: khối nhọn mập chĩa theo hướng bay, một dải mặt sáng, hai bóng mờ phía sau (vệt tốc độ). yCham: chạm mức này thì
        // gọi trung, vỡ thành ba mảnh nhỏ (không tắt phụt)
        P ToPhaLe(Vector2 pos, Vector2 vel, float len, float wd, float life, float yCham = float.NaN, Action<Vector2> trung = null, float dat = float.NaN)
        {
            var p = new P { pos = pos, vel = vel, life = life, sz = len, wd = wd, group = Front, R0 = yCham };
            p.upd = (q, dt, s) =>
            {
                if (!float.IsNaN(q.R0) && q.pos.y >= q.R0 && !q.dead)
                {
                    q.dead = true;
                    trung?.Invoke(q.pos);
                    var d = Unit(q.vel);
                    int nv = q.sz > 40 ? 3 : 2;                                      // mảnh nhỏ (mưa pha lê) vỡ hai, mảnh to vỡ ba: giữ ngân sách hạt
                    for (int i = 0; i < nv; i++)
                    {
                        float a = Mathf.Atan2(-d.y, -d.x) + (i - 0.5f * (nv - 1)) * 0.7f + s.U(-0.2f, 0.2f);
                        s.ToManhPhach(q.pos, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.6f) * s.U(140, 240), 0.42f * q.sz, 0.5f * q.wd, float.IsNaN(dat) ? float.NaN : dat + s.U(-4, 10));   // mảnh vỡ rơi xuống mặt đất chỗ đối thủ
                    }
                }
            };
            p.draw = (q, k, buf) =>
            {
                var d = Unit(q.vel);
                float sp = q.vel.magnitude * 0.016f;
                if (sp > 2)
                    for (int j = 2; j >= 1; j--) DrawPhaLe(buf, q.group, q.pos - d * (sp * j * 1.3f), d, q.sz * (1 - 0.12f * j), q.wd * (1 - 0.2f * j), j == 1 ? 0.45f : 0.22f, false);
                DrawPhaLe(buf, q.group, q.pos, d, q.sz, q.wd);
            };
            return Add(p);
        }

        // mảnh pha lê vỡ nhỏ: văng, xoay, rơi, chạm đất nảy một lần rồi mờ
        void ToManhPhach(Vector2 pos, Vector2 vel, float len, float wd, float ground)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = U(0.5f, 0.75f), acc = new Vector2(0, 1050), drag = 0.8f, sz = len, wd = wd, ground = ground, bounce = 0.3f,
                spin = U(-700, 700), ang = U(0, 360), group = U(0, 1) < 0.5f ? Front : Back
            };
            p.draw = (q, k, buf) =>
            {
                float a = 1 - SmoothStep(0.7f, 1, k), r = q.ang * Mathf.Deg2Rad;
                DrawPhaLe(buf, q.group, q.pos, new Vector2(Mathf.Cos(r), Mathf.Sin(r)), q.sz, q.wd, a);
            };
            Add(p);
        }

        // full = false: bóng mờ một màu (vệt tốc độ), không lớp chồng nên mờ được
        void DrawPhaLe(List<Item> buf, int g, Vector2 pos, Vector2 d, float len, float wd, float al = 1, bool full = true)
        {
            if (al < 0.03f || len < 1) return;
            float ang = TipAngle(d);
            var n = new Vector2(-d.y, d.x);
            if (!full)
            {
                Put(buf, g, 46.5f, S("needle_0"), ToPhach2, pos, len, wd / len, ang, al);
                return;
            }
            Put(buf, g, 47, S("needles_0"), Ink, pos, len + 5, (wd + 5) / (len + 5), ang, al);
            Put(buf, g, 47.1f, S("needle_0"), ToPhach, pos, len, wd / len, ang, al);
            Put(buf, g, 47.2f, S("needle_0"), ToPhach2, pos + n * (0.18f * wd) + d * (0.05f * len), 0.72f * len, 0.36f * wd / (0.72f * len), ang, al);
        }

        // tảng đá: bốn khối tròn méo chồng nhau viền mực (đá giữa, sẫm, sáng) + mạch hổ phách chéo (crust); ang theo độ
        void DrawTang(P q, float k, List<Item> buf) => DrawTangA(q, buf, 1);

        void DrawTangA(P q, List<Item> buf, float al)
        {
            float r = q.sz;
            if (r < 1.2f || al < 0.03f) return;
            int sd = q.seed & 3, g = q.group;
            float a = q.ang, rad = -a * Mathf.Deg2Rad, cs = Mathf.Cos(rad), sn = Mathf.Sin(rad);
            float ink = Mathf.Min(4.5f, 2.2f + r * 0.08f);
            for (int i = 0; i < 4; i++)
            {
                var u = ThachU[i];
                var c = q.pos + new Vector2(u.x * cs - u.y * sn, u.x * sn + u.y * cs) * r;
                float d = 2 * r * u.z;
                int si = (sd + i) & 3;
                Put(buf, g, q.ph, S("solid_" + si), Ink, c, d + ink, 1, a + i * 50, al);
                Put(buf, g, q.ph + 0.1f + i * 0.02f, S("blob_" + si), i == 1 ? ToDa2 : i == 3 ? ToDa3 : ToDa, c, d, 1, a + i * 50, al);
            }
            if (!q.crust || r < 6) return;
            var m = q.pos + new Vector2(0.12f * cs, 0.12f * sn) * r;
            Put(buf, g, q.ph + 0.3f, S("needles_0"), Ink, m, 1.15f * r + ink, (0.24f * r + ink) / (1.15f * r + ink), a + 64, al);
            Put(buf, g, q.ph + 0.4f, S("needle_0"), ToPhach, m, 1.15f * r, 0.24f / 1.15f, a + 64, al);
        }

        // tảng đá vỡ khi chạm: 3–5 khối nhỏ văng NGƯỢC hướng bay chếch lên, xoay, rơi nặng, nảy một lần rồi nằm, mờ dần (không cắt phụt)
        void ToTangVo(Vector2 c, float r, Vector2 huong, float ground, int seed, bool phach, int n = 4)
        {
            var ve = Unit(-Unit(huong) * 0.5f + new Vector2(0, -1));
            float a0 = Mathf.Atan2(ve.y, ve.x);
            for (int i = 0; i < n; i++)
            {
                float a = a0 + ((i + 0.5f) / n - 0.5f) * 2.6f + U(-0.2f, 0.2f);
                var q = new P
                {
                    pos = c + U2(-0.3f, 0.3f) * r, vel = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * U(160, 300) * Mathf.Sqrt(r / 14f), life = U(0.75f, 1.0f),
                    acc = new Vector2(0, 1150), ground = ground + U(-4, 8), bounce = 0.28f, spin = U(-420, 420), spinDrag = 0.6f, ang = U(0, 360),
                    group = (i & 1) == 0 ? Front : Back, sz = r * U(0.3f, 0.44f), seed = (seed + i) & 3, crust = phach && i == 0, ph = 44
                };
                q.draw = (z, k, buf) => DrawTangA(z, buf, 1 - SmoothStep(0.7f, 1, k));
                Add(q);
            }
        }

        // tảng đá bay vồng từ a tới b trong tb giây, xoay, kéo ĐUÔI BỤI LIỀN (cụm đứng tại chỗ rải theo quãng vừa bay, KR5); tới nơi gọi trung(b) rồi
        // VỠ thành khối nhỏ. co1: cỡ lúc tới so với lúc rời; vo: số khối vỡ (0 = không vỡ); ground: mặt đất chỗ đích (khối vỡ nằm lại)
        void ToTangBay(Vector2 a, Vector2 b, float tb, float r, float vong, bool phach, Action<Vector2> trung, float co1 = 1, int seed = -1, int vo = 4,
            float ground = float.NaN)
        {
            var n = new Vector2(-(b - a).y, (b - a).x).normalized;
            if (n.y > 0) n = -n;
            float t0 = T, dat = float.IsNaN(ground) ? b.y + 0.6f * r + 40 : ground;
            var p = new P
            {
                pos = a, life = tb, group = Front, sz = r, seed = seed >= 0 ? seed : rng.Next(4), crust = phach, ph = 44,
                spin = (b.x > a.x ? 1 : -1) * 420
            };
            p.upd = (q, dt, s) =>
            {
                float f = Mathf.Clamp01((s.T - t0) / tb);
                var cu = q.pos;
                q.pos = Vector2.Lerp(a, b, f) + n * (vong * Mathf.Sin(Mathf.PI * f));
                q.vel = Vector2.zero;
                q.sz = r * Mathf.Lerp(1, co1, f);
                var dv = q.pos - cu;
                q.R0 += dv.magnitude;
                bool fb = s.HasFb("khoi");                                       // khung vẽ sẵn (2026-11-19): cụm khói vẽ sẵn, bước gấp đôi
                float buoc = fb ? Mathf.Max(14, 1.7f * q.sz) : Mathf.Max(7, 0.85f * q.sz);
                if (q.R0 < buoc || dv.sqrMagnitude < 1e-6f) return;
                q.R0 -= buoc;
                var u = dv.normalized;
                var at = q.pos - u * (0.75f * q.sz) + new Vector2(-u.y, u.x) * s.U(-0.3f, 0.3f) * q.sz;
                if (fb)
                {
                    float h = 1.7f * q.sz;
                    s.FbBui(at + new Vector2(0, 0.42f * h), -u * s.U(8, 20) + new Vector2(0, -s.U(6, 16)), h, Front, FbBuiC, 1.9f, 0.88f, 3);
                }
                else s.ToBui(at, -u * s.U(10, 30) + new Vector2(0, -s.U(8, 24)), s.U(0.36f, 0.5f), 0.35f * q.sz, 0.62f * q.sz, Front, false);
                if (s.U(0, 1) < 0.18f) s.ToSoi(q.pos, -u * s.U(30, 80) + new Vector2(s.U(-40, 40), -s.U(20, 60)), s.U(0.12f, 0.2f) * q.sz, ToDa2, dat + s.U(-4, 8));
            };
            p.draw = DrawTang;
            p.onDeath = (q, s) =>
            {
                trung?.Invoke(b);
                if (vo > 0) s.ToTangVo(b, q.sz, b - a, dat, q.seed, phach, vo);
            };
            Add(p);
        }

        // lưỡi cát trăng khuyết (mảng liền viền mực, dải sáng ở mép trước) bay thẳng a → b trong tb giây, ĐUÔI CÁT liền phía sau; tới nơi gọi
        // trung(b) rồi lưỡi ÉP DẸT vào thân, loe ngang, vỡ thành cát (0,12 s) thay vì tắt phụt
        void ToLuoiCat(Vector2 a, Vector2 b, float tb, float R, Action<Vector2> trung)
        {
            var d = Unit(b - a);
            var ax = new Vector2(-d.y, d.x);
            var p = new P { pos = a, vel = (b - a) / tb, life = tb, group = Front, sz = R };
            bool fb = HasFb("khoi");                                             // khung vẽ sẵn (2026-11-19): đuôi cát là cụm khói vẽ sẵn nhuộm cát
            p.upd = (q, dt, s) =>
            {
                q.R0 += q.vel.magnitude * dt;
                float buoc = fb ? Mathf.Max(12, 0.6f * q.sz) : Mathf.Max(6, 0.3f * q.sz);
                while (q.R0 >= buoc)
                {
                    q.R0 -= buoc;
                    var at = q.pos - d * (q.sz * 0.42f) + ax * s.U(-0.4f, 0.4f) * q.sz;
                    if (fb)
                    {
                        float h = 0.62f * q.sz;
                        s.FbBui(at + new Vector2(0, 0.42f * h), -d * s.U(8, 20) + new Vector2(0, -s.U(4, 14)), h, Front, FbCatC, 2.1f, 0.85f, 4);
                        continue;
                    }
                    var c = s.ToBui(at, -d * s.U(10, 30) + new Vector2(0, -s.U(5, 20)), s.U(0.3f, 0.42f), 0.12f * q.sz, 0.24f * q.sz, Front, false);
                    c.col = s.U(0, 1) < 0.5f ? ToCat : ToCat3;
                }
            };
            p.draw = (q, k, buf) =>
            {
                const int n = 11, N = 2 * n - 2;
                MSolid(Front, 26, Crescent(q.pos, d, ax, q.sz, 1f, 0.42f, 1.15f, n), N, ToCat, 1, 2.4f);
                MFill(Front, 26.01f, Crescent(q.pos, d, ax, q.sz, 0.92f, 0.74f, 0.95f, n), N, ToCat3, 1, false);
            };
            p.onDeath = (q, s) =>
            {
                trung?.Invoke(b);
                var v = new P { pos = b, life = 0.12f, group = Front, sz = R };
                v.draw = (z, k, buf) =>
                {
                    const int n = 11, N = 2 * n - 2;
                    float ep = 1 - 0.65f * EaseOut(k), loe = 1 + 0.45f * EaseOut(k), al = 1 - SmoothStep(0.4f, 1, k);
                    MSolid(Front, 26, Crescent(z.pos - d * (0.2f * z.sz * k), d, ax, z.sz, ep, 0.42f * ep, 1.15f * loe, n), N, ToCat, al, 2.4f);
                };
                s.Add(v);
                if (fb)                                                          // khung vẽ sẵn: lưỡi vỡ thành hai cụm cát vẽ sẵn hai đầu lưỡi
                    for (int i = -1; i <= 1; i += 2)
                    {
                        float h = 0.9f * R;
                        s.FbBui(b + ax * (i * 0.4f * R) + new Vector2(0, 0.42f * h), ax * (i * 36) - d * 24 + new Vector2(0, -18), h, Front, FbCatC, 1.8f, 0.9f, 3);
                    }
                else
                    for (int i = 0; i < 3; i++)
                    {
                        float sd = i - 1;
                        var c = s.ToBui(b + ax * (sd * 0.5f * R), ax * (sd * 60) - d * 40 + new Vector2(0, -30), s.U(0.4f, 0.55f), 0.25f * R, 0.42f * R, Front, false);
                        c.col = ToCat3;
                    }
            };
            Add(p);
        }

        // cột sa thạch trồi từ đất (đáy bám đất, đỉnh vỡ xiên, hai vạch son trồi theo), giữ rồi lún; bụi, dăm ở chân
        void ToCot(Vector2 chan, float w, float h, float giu, int group, float sc)
        {
            const float tLen = 0.12f, tLun = 0.25f;
            // khung vẽ sẵn (2026-11-19; người dùng: "gai ... đâm lên xấu"): cụm cột sa thạch vẽ sẵn (khung gai sắt nhuộm sa thạch) trồi đúng nhịp cũ
            // (lên 0,12 s, giữ, vỡ rơi 0,25 s), đỉnh cao bằng cột cũ; bụi + vụn ở chân có sẵn trong khung nên bỏ hai cụm bụi hạt; giữ dăm, hố
            if (HasFb("gai_sat"))
            {
                FbGai(chan, h, group, FbSaThach, tLen, giu, tLun, U(0, 1) < 0.5f);
                for (int i = 0; i < 2; i++)
                    ToSoiCum(chan + new Vector2(U(-0.3f, 0.3f) * w, -4), new Vector2(U(-160, 160), U(-300, -170)) * sc, U(2.8f, 4f) * sc,
                        i == 0 ? ToCat2 : ToSaThach, ToCatSam, chan.y + 2, (i & 1) == 0 ? Front : Back);
                ToHo(chan, 0.65f * w, giu);
                return;
            }
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
            for (int d = -1; d <= 1; d += 2)                                     // bụi trồi ở chân cột: hai cụm nhiều múi lan ra hai bên
                ToCum(chan + new Vector2(d * 0.45f * w, -3), new Vector2(d * U(50, 90), -U(20, 40)) * sc, 0.32f * w + 4 * sc, 3, d < 0 ? Back : Front);
            for (int i = 0; i < 2; i++)
                ToSoiCum(chan + new Vector2(U(-0.3f, 0.3f) * w, -4), new Vector2(U(-160, 160), U(-300, -170)) * sc, U(2.8f, 4f) * sc,
                    i == 0 ? ToCat2 : ToSaThach, ToCatSam, chan.y + 2, (i & 1) == 0 ? Front : Back);
            ToHo(chan, 0.65f * w, giu);
        }

        // vết nứt đất: dải nâu sẫm gấp khúc THON dần lan từ a tới b trong tLan giây, hai nhánh nhỏ rẽ ra, mép be sáng bị hất bên dưới; nằm ~1 s
        // rồi mờ 0,5 s (KR5: vết trên đất giữ 1–2 s)
        void ToNut(Vector2 a, Vector2 b, float tLan, float sc)
        {
            const int n = 12, nb = 4;
            var pts = new Vector2[n + 1];
            for (int i = 0; i <= n; i++)
                pts[i] = Vector2.Lerp(a, b, (float)i / n) + (i > 0 && i < n ? new Vector2(0, U(-5, 5) * sc) : Vector2.zero);
            var nh = new Vector2[2 * (nb + 1)];                                 // hai nhánh rẽ ở 1/3 và 2/3 quãng
            for (int j = 0; j < 2; j++)
            {
                var g = pts[j == 0 ? 4 : 8];
                var e = Unit(b - a);
                float rad = (j == 0 ? 0.6f : -0.55f) + U(-0.15f, 0.15f);
                var dn = new Vector2(e.x * Mathf.Cos(rad) - e.y * Mathf.Sin(rad), (e.x * Mathf.Sin(rad) + e.y * Mathf.Cos(rad)) * 0.45f);
                float L = (b - a).magnitude * U(0.18f, 0.26f);
                for (int i = 0; i <= nb; i++) nh[j * (nb + 1) + i] = g + dn * (L * i / nb) + (i > 0 ? new Vector2(0, U(-2, 2) * sc) : Vector2.zero);
            }
            const float giu = 0.95f, tan = 0.5f;
            var p = new P { pos = a, life = tLan + giu + tan, group = Floor };
            p.draw = (q, k, buf) =>
            {
                float lan = Mathf.Min(1, q.age / tLan), al = 1 - SmoothStep(tLan + giu, tLan + giu + tan, q.age);
                if (al < 0.03f) return;
                int m = Mathf.Min(n, (int)(n * lan) + 1);
                for (int i = 0; i < m; i++) NutDoan(pts[i], pts[i + 1], (2.8f - 1.8f * i / n) * sc, al);
                for (int j = 0; j < 2; j++)
                {
                    float f0 = j == 0 ? 0.33f : 0.67f;
                    if (lan < f0) continue;
                    int mb = Mathf.Min(nb, (int)(nb * Mathf.Min(1, (lan - f0) / 0.3f)) + 1);
                    for (int i = 0; i < mb; i++) NutDoan(nh[j * (nb + 1) + i], nh[j * (nb + 1) + i + 1], (1.6f - 1.1f * i / nb) * sc, al);
                }
            };
            Add(p);
        }

        void NutDoan(Vector2 p0, Vector2 p1, float w, float al)
        {
            var e = p1 - p0;
            var nn = new Vector2(-e.y, e.x).normalized;
            int s0 = mp.Count;                                                   // mép be sáng lệch xuống (đất bị hất)
            mp.Add(p0 + nn * w + new Vector2(0, 1.2f * w));
            mp.Add(p1 + nn * w + new Vector2(0, 1.2f * w));
            mp.Add(p1 - nn * w + new Vector2(0, 1.2f * w));
            mp.Add(p0 - nn * w + new Vector2(0, 1.2f * w));
            MFill(Floor, 4.9f, s0, 4, ToBuiC, 0.8f * al, true);
            int s1 = mp.Count;
            mp.Add(p0 + nn * w);
            mp.Add(p1 + nn * w);
            mp.Add(p1 - nn * w);
            mp.Add(p0 - nn * w);
            MFill(Floor, 5, s1, 4, ToNutC, al, true);
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
            Every(t0 + 0.12f, t1 - 0.25f, 36, x =>
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
                // khung vẽ sẵn (2026-11-19): bụi tràn miệng / chân phễu là cụm cát vẽ sẵn, ít mà to (xác suất × 0,4, cụm × 1,3)
                if (U(0, 1) < 0.45f)
                {
                    float d = U(0, 1) < 0.5f ? -1 : 1;
                    ToBuiFb(chan + new Vector2(d * 60 * sc, -cao * 0.95f), new Vector2(d * 70, -10) * sc, 0.5f, 5 * sc, 13 * sc, Front, null, FbCatC, 0.4f, 1.3f,
                        false, true);
                }
                if (U(0, 1) < 0.35f)
                {
                    float d = U(0, 1) < 0.5f ? -1 : 1;
                    ToBuiFb(chan + new Vector2(d * 20 * sc, -2), new Vector2(d * 80, -10) * sc, 0.45f, 4 * sc, 12 * sc, Back, null, FbCatC, 0.4f, 1.3f, true, true);
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
                    // khung vẽ sẵn (2026-11-19; "gai ... đâm lên xấu"): mỗi nhịp MỘT cụm gai đá vẽ sẵn (khung gai sắt nhuộm đá nâu be), lớn dần về
                    // phía đối thủ, xếp so le hai bên đường chạy, lật xen kẽ; trồi 0,08 s, giữ 0,1 s, vỡ 0,16 s (như gai cũ 0,32 s); bụi, vụn ở chân có
                    // sẵn trong khung nên bỏ cụm bụi hạt, giữ sỏi bắn
                    if (HasFb("gai_sat"))
                    {
                        int ii = Mathf.RoundToInt(f * n);
                        float so = (ii & 1) == 0 ? -1 : 1;
                        FbGai(c + new Vector2(U(-6, 6), so * 4) * sc, U(30, 40) * (0.7f + 0.6f * f) * sc, so < 0 ? Back : Front, FbDaNau, 0.08f, 0.1f, 0.16f,
                            (ii & 2) == 0, U(-6, 6));
                        if ((ii & 1) == 1) ToSoi(c, new Vector2(U(-120, 120), -U(180, 280)) * sc, U(2.2f, 3.2f) * sc, ToDa2, c.y + 3 * sc);
                        if (cuoi) toi?.Invoke();
                        return;
                    }
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
                    ToCum(c + new Vector2(0, -3 * sc), new Vector2(U(-30, 30), -30) * sc, 8 * sc, 2, Back);
                    if (((int)(f * n + 0.5f) & 1) == 1) ToSoi(c, new Vector2(U(-120, 120), -U(180, 280)) * sc, U(2.2f, 3.2f) * sc, ToDa2, c.y + 3 * sc);
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
                ToCum(casterFeet + new Vector2(-dir * 0.15f * casterH, -4 * sH), new Vector2(-dir * U(80, 140), -U(20, 40)) * sH, 11 * sH, 3, Back));
            At(L, () =>
            {
                ToNo(foeBody + new Vector2(-dir * 0.22f * tH, 0.04f * tH), foeFeet.y, tH, dang == 2 ? 1.3f : 0.9f, ToDa, ToDa2, new Vector2(dir, 0));
                if (dang == 2) ToVong(foeFeet, 70 * sc);
                ToCum(foeFeet + new Vector2(-dir * 0.15f * tH, -4 * sc), new Vector2(dir * U(40, 90), -U(15, 35)) * sc, 10 * sc, 3, Back);
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
            // lắc mai: bụi bốc thành cụm liền quanh mai (ít mà to, không rải rác), sỏi nhỏ rơi. khung vẽ sẵn (2026-11-19): cụm khói vẽ sẵn nhuộm
            // bụi, 40 % số cụm, to × 1,3
            Every(lac0 * k, GiapLac1 * k, 13, x =>
            {
                var p = mai((lac0 + (GiapLac1 - lac0) * x) * k) + new Vector2(U(-0.16f, 0.16f), U(-0.08f, 0.08f)) * casterH;
                ToBuiFb(p, new Vector2(U(-30, 30), -U(20, 50)) * sH, U(0.5f, 0.65f), 5 * sH, U(9, 12) * sH, Front, null, FbBuiC, 0.4f, 1.3f);
                if (U(0, 1) < 0.4f) ToSoi(p, new Vector2(U(-90, 90), U(-160, -60)) * sH, 1.8f * sH, ToDa, casterFeet.y + 4 * sH);
            });
            for (int i = 0; i < 3; i++)
            {
                int j = i;
                var tu = d2 ? ToSan(casterFeet, casterH, dir, GiapRoi2[j]) : ToSan(casterFeet, casterH, dir, ToDiem(GiapMai, lac0, 0.08f, GiapPhong[j]));
                var cham = foeBody + new Vector2(-dir * 0.1f * tH, 0);           // mảnh của rig tới đúng giữa thân đối thủ (xương far): bông ở mặt trước
                At(GiapPhong[j] * k, () =>
                {
                    ToCum(tu, new Vector2(-dir * 30, -30) * sH, (d2 ? 9 : 7) * sH, 3, Front, 0, null, false);   // khung vẽ sẵn: cụm giữa không trung (hốc mai)
                    ToDuoiThang(tu, cham, GiapBay * k, (d2 ? 8 : 6) * sH, d2 ? ToCat3 : ToBuiC);
                });
                At((GiapPhong[j] + GiapBay) * k, () =>
                {
                    var c = cham + U2(-5, 5) * sc;
                    if (d2) ToNo(c, foeFeet.y, tH, j == 2 ? 1.5f : 1.1f, ToPhach, ToDa, cham - tu);
                    else ToNo(c, foeFeet.y, tH, j == 2 ? 1.1f : 0.8f, ToDa, ToDa2, cham - tu);
                });
            }
            At(dap * k, () =>
            {
                ToVong(casterFeet, 70 * sH);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(casterFeet + new Vector2(d * 40 * sH, -4 * sH), new Vector2(d * 70, -20) * sH, 9 * sH, 2);
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
            Every(GiapGong0 * k, gong1 * k, 10, x =>                         // khung vẽ sẵn (2026-11-19): bụi gồng là cụm vẽ sẵn, 40 % số cụm, to × 1,3
                ToBuiFb(casterFeet + new Vector2(U(-0.4f, 0.4f) * casterH, -2), new Vector2(U(-40, 40), -20) * sH, 0.55f, 5 * sH, 11 * sH, Back, null, FbBuiC, 0.4f,
                    1.3f, true));
            At(GiapGong0 * k, () => Shake?.Invoke(0.05f));
            At(ban * k, () =>
            {
                var goc = ToSan(casterFeet, casterH, dir, d2 ? GiapPhaLe2 : GiapPhaLe);
                ToChop(goc, 0.3f * casterH, Front, 0.1f);
                for (int i = 0; i < (d2 ? 8 : 6); i++)
                    ToPhaLe(goc + new Vector2(U(-18, 18) * sH, 0), new Vector2(U(-60, 60), -1100 - 120 * i) * sH, 30 * sH, 12 * sH, 0.5f);
                ToCum(goc, new Vector2(0, -40) * sH, 12 * sH, 4, Front, 0, null, false);   // khung vẽ sẵn: cụm giữa không trung (hốc pha lê)
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
                    ToPhaLe(dich - vRoi * TB, vRoi, 30 * sc * to, 13 * sc * to, TB + 0.1f, dich.y, p => ToNo(p, foeFeet.y, tH, 0.7f * to, ToPhach, ToDa, vRoi), foeFeet.y);
                });
            }
            At(Mathf.Max(0, L - TB), () =>
            {
                var dich = foeBody + new Vector2(0, 0.06f * tH);
                var v = new Vector2(dir * 260, 1150) * sc;
                ToPhaLe(dich - v * TB, v, 56 * sc * to, 24 * sc * to, TB + 0.1f, dich.y, p =>
                {
                    ToNo(p, foeFeet.y, tH, 2f * to, ToPhach, ToDa2, v);
                    ToVong(foeFeet, 95 * sc * to, 0.55f);
                    ToHo(foeFeet + new Vector2(dir * 0.1f * tH, 0), 34 * sc * to);
                    var cam = new P { pos = new Vector2(p.x + dir * 0.1f * tH, foeFeet.y), life = 0.45f, group = Front, sz = 54 * sc * to, wd = 24 * sc * to };
                    cam.draw = (z, kk, buf) =>
                        DrawPhaLe(buf, Front, z.pos + new Vector2(1.5f * sc * Mathf.Sin(z.age * 70), -0.42f * z.sz), Unit(new Vector2(dir * 0.25f, -1)), z.sz, z.wd);
                    cam.onDeath = (z, s) => ToNo(z.pos + new Vector2(0, -0.4f * z.sz), foeFeet.y, tH, 1.2f, ToPhach, ToPhach2);
                    Add(cam);
                }, foeFeet.y);
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
                    ToCum(casterFeet + new Vector2(-dir * 0.15f * casterH, -4 * sH), new Vector2(-dir * U(90, 150), -U(20, 40)) * sH, 12 * sH, 3, Back, 0, FbCatC));
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.12f * tH, 0.04f * tH);
                ToCan(c, tH * (dang == 2 ? 1.2f : 1f));
                ToNo(c, foeFeet.y, tH, dang == 2 ? 1.05f : 0.7f, ToCat, ToCat2, new Vector2(dir, 0));
            });
            return L;
        }

        // CHIÊU MANA: cát bốc quanh áo choàng lúc xoè; ba phiến đất nung của rig bay găm: mỗi cú găm dăm đất nung. dang 2: năm phiến mũ trùm
        public float NTichPhien(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 1)
        {
            bool d2 = dang == 2;
            float L = Mathf.Max(0.05f, lead), k = L / (d2 ? 0.672f : TichCast), dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            float x0 = d2 ? 0.05f : 0.12f, x1 = 0.45f;
            // cát bốc quanh áo choàng: cụm liền nở dần theo nhịp xoè (mật độ tăng tới lúc phóng), không chấm rải rác. khung vẽ sẵn (2026-11-19):
            // cụm khói vẽ sẵn nhuộm cát, 40 % số cụm, to × 1,3
            Every(x0 * k, x1 * k, x => (d2 ? 10 : 8) + 10 * x, x =>
            {
                var p = ToSan(casterFeet, casterH, dir, d2 ? ToDiem(TichAo2, 0.05f, 0.1f, x0 + (x1 - x0) * x) : ToDiem(TichAo, 0.12f, 0.11f, x0 + (x1 - x0) * x))
                        + U2(-0.2f, 0.2f) * casterH;
                ToBuiFb(p, new Vector2(U(-40, 40), U(-60, -20)) * sH, U(0.5f, 0.65f), 5 * sH, U(9, 12) * sH, Front, U(0, 1) < 0.5f ? ToCat : ToCat3, FbCatC, 0.4f, 1.3f);
            });
            var ph = d2 ? TichPhong2 : TichPhong;
            var cham = foeBody + new Vector2(-dir * 0.1f * tH, 0);
            for (int i = 0; i < ph.Length; i++)
            {
                int j = i;
                bool cuoi = j == ph.Length - 1;
                var tu = ToSan(casterFeet, casterH, dir, d2 ? ToDiem(TichAo2, 0.05f, 0.1f, 0.45f) : ToDiem(TichAo, 0.12f, 0.11f, 0.45f));
                At(ph[j] * k, () => ToDuoiThang(tu, cham, TichBay * k, 6 * sH, ToCat3));
                At((ph[j] + TichBay) * k, () => ToNo(cham + U2(-8, 8) * sc, foeFeet.y, tH, cuoi ? (d2 ? 1.35f : 1.1f) : 0.85f, ToGom, ToGom2, cham - tu));
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
            // cát xoáy quanh chân đối thủ: cụm liền chạy vòng (mật độ tăng dần tới lúc lốc trùm). khung vẽ sẵn (2026-11-19): cụm khói vẽ sẵn nhuộm
            // cát, chân ở mặt đất, 40 % số cụm, to × 1,3
            Every(0.08f * k, L, x => 8 + 12 * x, x =>
            {
                float a = U(0, 6.28f);
                ToBuiFb(foeFeet + new Vector2(50 * Mathf.Cos(a), -4 + 8 * Mathf.Sin(a)) * sc, new Vector2(-70 * Mathf.Sin(a), -20) * sc, 0.55f, 5 * sc,
                    11 * sc, Mathf.Sin(a) > 0 ? Front : Back, U(0, 1) < 0.5f ? ToCat : ToCat3, FbCatC, 0.4f, 1.3f, true);
            });
            foreach (float td in d2 ? new[] { TichDam, TichSkill } : new[] { TichDam })
                At(td * k, () =>
                {
                    ToVong(dam, (d2 ? 95 : 80) * sH);
                    ToHo(dam, (d2 ? 30 : 24) * sH, 0.7f);
                    for (int d = -1; d <= 1; d += 2)
                        ToCum(dam + new Vector2(d * 40 * sH, -4 * sH), new Vector2(d * 90, -20) * sH, 12 * sH, 3, Front, 0, FbCatC);
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
                ToNo(foeBody + new Vector2(-dir * 0.16f * tH, 0.06f * tH), foeFeet.y, tH, 1f, ToDa, ToDa2, new Vector2(dir, 0.5f));
                var g = foeFeet + new Vector2(-dir * 0.2f * tH, 0);
                ToVong(g, 60 * sc);
                ToCum(g + new Vector2(0, -4 * sc), new Vector2(-dir * 40, -30) * sc, 11 * sc, 3, Back);
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
            float tu0 = (d2 ? 0.30f : ThiemTu) * k, rDa = (d2 ? 21 : 16) * sH;
            // TỤ: bụi, sỏi bay xoắn ốc vào miệng thành vệt, nhanh dần; mật độ tăng tới lúc nhả; hai vòng co về miệng
            Every(tu0, L - 0.04f * k, x => (d2 ? 22 : 18) + (d2 ? 46 : 36) * x, x =>
            {
                float a = U(0, 6.28f);
                var p0 = mieng(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * (U(50, 78) * sH);
                ToHut(p0, mieng, U(0.28f, 0.36f), U(2.2f, 3.4f) * sH, U(0, 1) < 0.45f ? ToDa : U(0, 1) < 0.5f ? ToBuiC : ToCat2, 2f);
            });
            foreach (float f in new[] { 0.25f, 0.62f })
                At(tu0 + (L - tu0) * f, () => ToVongCo(mieng, 2.4f * rDa, 0.3f * k, ToCat3));
            // TẢNG ĐÁ thành hình trong miệng: lớn dần theo nhịp đập (nhanh dần), mạch hổ phách; 0,06 s cuối NÉN lại rồi nhả
            At(tu0 + 0.1f * (L - tu0), () =>
            {
                float tA = T, dur = L - tu0 - 0.1f * (L - tu0);
                var cau = new P { pos = mieng(T), life = dur, group = Front, seed = rng.Next(4), crust = true, ph = 44, spin = dir * 160 };
                cau.upd = (q, dt, s) =>
                {
                    float u = Mathf.Clamp01((s.T - tA) / dur), nen = u > 1 - 0.06f / Mathf.Max(0.07f, dur) ? 0.82f : 1;
                    q.sz = rDa * (0.25f + 0.75f * u * u) * (1 + 0.08f * Mathf.Sin(u * u * 26)) * nen;
                    q.pos = mieng(s.T);
                    q.vel = Vector2.zero;
                };
                cau.draw = DrawTang;
                Add(cau);
            });
            At(L, () =>
            {
                var m = mieng(T);
                var dich = foeBody + new Vector2(-dir * 0.12f * tH, 0);
                ToChop(m, 0.42f * casterH, Front, 0.1f);
                ToTangBay(m, dich, ThiemBayDa, rDa, 60 * sc, true, p =>
                {
                    ToNo(p, foeFeet.y, tH, d2 ? 2.1f : 1.6f, ToDa, ToPhach, dich - m);
                    ToVong(foeFeet, (d2 ? 100 : 80) * sc);
                    Shake?.Invoke(0.2f);
                }, 1, -1, d2 ? 5 : 4, foeFeet.y);
                ToCum(m, new Vector2(-dir * 50, -20) * sH, 9 * sH, 3, Front, 0, null, false);   // khung vẽ sẵn: cụm giữa không trung (miệng)
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
            // khung vẽ sẵn (2026-11-19): bụi toé lúc xoay và vệt bụi đường lăn là cụm khói vẽ sẵn nhuộm bụi, chân ở mặt đất, 40 % số cụm, to × 1,3
            Every((ThiemCuon + 0.04f) * k, ThiemLao * k, 15, x =>
            {
                var p = casterFeet + new Vector2(U(-10, 10) * sH, -4 * sH);
                ToBuiFb(p, new Vector2(-dir * U(60, 140), U(-50, -10)) * sH, 0.55f, 6 * sH, 13 * sH, Back, null, FbBuiC, 0.4f, 1.3f, true);
                if (U(0, 1) < 0.35f) ToSoiCum(p, new Vector2(-dir * U(80, 200), U(-220, -100)) * sH, 2.4f * sH, ToDa, ToDa2, casterFeet.y + 4 * sH, Back);
            });
            float tl0 = ThiemLao * k;
            Every(tl0, L, 20, x => ToBuiFb(cho(tl0 + x * (L - tl0)) + new Vector2(0, -2 * sH), new Vector2(U(-20, 20), U(-30, -5)) * sH, 0.6f, 7 * sH, 14 * sH, Back,
                null, FbBuiC, 0.4f, 1.3f, true));
            At(L, () =>
            {
                ToNo(foeBody + new Vector2(-dir * 0.1f * tH, 0.07f * tH), foeFeet.y, tH, 2.2f, ToDa, ToPhach, new Vector2(dir, 0));
                ToVong(foeFeet, 110 * sc, 0.6f);
                ToHo(foeFeet + new Vector2(-dir * 0.12f * tH, 0), 30 * sc);
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
                ToNo(c, foeFeet.y, tH, manh, ToCat, ToCat2, new Vector2(dir, 0.3f));
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
                    var dich = foeBody + new Vector2(-dir * 0.1f * tH, (d1 ? j - 0.5f : j - 1) * 16 * sc);   // lưỡi tới mặt trước thân, không xuyên qua
                    ToCum(m, new Vector2(-dir * 40, -30) * sH, 7 * sH, 2, Front, 0, FbCatC);
                    ToLuoiCat(m, dich, LongBayLuoi, R, p => ToNo(p, foeFeet.y, tH, d1 ? 0.7f : 0.9f, ToCat, ToCat2, dich - m));
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
            // gồng: cát hút xoắn ốc vào vuốt thành vệt, dày dần tới lúc nện; ba vòng co về vuốt
            Every(LongGong * k, (LongNen - 0.1f) * k, x => 18 + 34 * x, x =>
            {
                float a = U(0, 6.28f);
                var p0 = vuot(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.6f) * (U(50, 80) * sH);
                ToHut(p0, vuot, U(0.26f, 0.34f), U(2.2f, 3.6f) * sH, U(0, 1) < 0.5f ? ToCat : ToCat2, 2f);
            });
            foreach (float f in new[] { 0.15f, 0.45f, 0.75f })
                At((LongGong + (LongNen - 0.1f - LongGong) * f) * k, () => ToVongCo(vuot, 55 * sH, 0.32f * k, ToCat3));
            var nen = casterFeet + new Vector2(dir * 0.2f * casterH, 0);
            At(LongNen * k, () =>
            {
                ToVong(nen, 100 * sH, 0.55f);
                ToHo(nen, 30 * sH);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(nen + new Vector2(d * 30 * sH, -4 * sH), new Vector2(d * 90, -30) * sH, 12 * sH, 3, Front, 0, FbCatC);
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
                ToCum(casterFeet + new Vector2(-dir * 0.15f * casterH, -4 * sH), new Vector2(-dir * U(90, 160), -U(20, 40)) * sH, 12 * sH, 3, Back));
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.18f * tH, 0.08f * tH);
                ToNo(c, foeFeet.y, tH, 1.4f, ToPhach, ToDa, new Vector2(dir, 0));
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
            Every(ThiemGong2 * k, ThiemNhay2 * k, 10, x =>                   // khung vẽ sẵn (2026-11-19): bụi gồng là cụm vẽ sẵn, 40 % số cụm, to × 1,3
            {
                ToBuiFb(casterFeet + new Vector2(U(-0.4f, 0.4f) * casterH, -2), new Vector2(U(-40, 40), -20) * sH, 0.55f, 6 * sH, 12 * sH, Back, null, FbBuiC, 0.4f,
                    1.3f, true);
                if (U(0, 1) < 0.4f)
                    ToSoi(casterFeet + new Vector2(dir * U(-0.1f, 0.3f) * casterH, -U(0.9f, 1.1f) * casterH), new Vector2(U(-60, 60), 60) * sH, 2.6f * sH, ToPhach,
                        casterFeet.y + 4 * sH);
            });
            At(ThiemGong2 * k, () => Shake?.Invoke(0.08f));
            At(ThiemNhay2 * k, () =>
            {
                ToVong(casterFeet, 75 * sH);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(casterFeet + new Vector2(d * 40 * sH, -4 * sH), new Vector2(d * 90, -25) * sH, 12 * sH, 3);
            });
            At(L, () =>
            {
                var cham = foeFeet + new Vector2(-dir * 0.22f * tH, 0);           // khối cắm đất ngay trước đối thủ
                ToNo(foeBody + new Vector2(-dir * 0.12f * tH, 0.12f * tH), foeFeet.y, tH, 2.4f, ToPhach, ToDa, new Vector2(dir * 0.5f, 1));
                ToVong(cham, 125 * sc, 0.65f);
                ToHo(cham, 36 * sc);
                ToNut(cham, cham + new Vector2(-dir * 0.9f * tH, 6 * sc), 0.16f, sc);
                ToNut(cham, cham + new Vector2(dir * 0.7f * tH, -4 * sc), 0.16f, sc);
                // soi trong game 2026-11-17: cột cao bằng đối thủ nằm sau nó thì bị đối thủ và thân tướng (vừa nhảy tới) che hết: hai cột bên
                // dời ra ngoài thân (±0,7 × đối thủ quanh chân nó), cột giữa sau lưng đối thủ cao 1,4 × để trồi hẳn lên trên đầu
                for (int i = 0; i < 3; i++)
                {
                    var at = foeFeet + new Vector2((i - 1) * 0.7f * tH, i == 1 ? 2 : 4);
                    float h = (i == 1 ? 1.4f : 0.8f) * tH, w = (i == 1 ? 0.36f : 0.24f) * tH;
                    // khung vẽ sẵn (2026-11-19; "gai ... đâm lên xấu"): cụm cột pha lê vẽ sẵn (khung gai sắt nhuộm hổ phách), nghiêng như cột cũ, trồi
                    // 0,07 s, giữ 0,3 s, vỡ rơi 0,18 s (đời 0,55 s như cũ); khung tự vỡ thành mảnh nên bỏ cú nổ dăm lúc tan
                    if (HasFb("gai_sat"))
                    {
                        FbGai(at, h, Back, FbPhachC, 0.07f, 0.3f, 0.18f, i == 0, -(i - 1) * 14);
                        continue;
                    }
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
            Every(LongGong1 * k, (LongNen1 - 0.1f) * k, x => 14 + 28 * x, x =>
            {
                float a = U(0, 6.28f);
                var p0 = vuot(T) + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.6f) * (U(40, 65) * sH);
                ToHut(p0, vuot, U(0.26f, 0.34f), U(2f, 3.2f) * sH, U(0, 1) < 0.5f ? ToCat : ToCat2, 2f);
            });
            foreach (float f in new[] { 0.2f, 0.6f })
                At((LongGong1 + (LongNen1 - 0.1f - LongGong1) * f) * k, () => ToVongCo(vuot, 45 * sH, 0.32f * k, ToCat3));
            var nen = ToSan(casterFeet, casterH, dir, LongNenP1);
            nen.y = casterFeet.y;
            At(LongNen1 * k, () =>
            {
                ToVong(nen, 80 * sH, 0.5f);
                ToHo(nen, 24 * sH, 0.7f);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(nen + new Vector2(d * 26 * sH, -4 * sH), new Vector2(d * 80, -25) * sH, 10 * sH, 3, Front, 0, FbCatC);
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
                    ToNo(foeBody + new Vector2(-dir * 0.12f * tH, 0) + U2(-10, 10) * sc, foeFeet.y, tH, cuoi ? 1.4f : 0.6f, ToDa, ToDa2, new Vector2(dir, 0));
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
                ToChop(new Vector2(m.x, casterFeet.y - 0.08f * casterH), 0.34f * casterH, Front, 0.1f);
                ToVong(g, 95 * sH, 0.5f);
                ToHo(g, 32 * sH);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(g + new Vector2(d * 30 * sH, -4 * sH), new Vector2(d * 90, -30) * sH, 12 * sH, 3);
                Shake?.Invoke(0.3f);
                ToSongChan(g + new Vector2(dir * 0.15f * casterH, -2), foeFeet + new Vector2(dir * 0.07f * tH, 2), VienBayChan, sc,
                    () => ToNo(foeBody + new Vector2(-dir * 0.1f * tH, 14 * sc), foeFeet.y, tH, 1.8f, ToDa, ToDa2, new Vector2(dir, 0)));
            });
            return L + VienBayChan;
        }

        // CHIÊU CUỐI: TẢNG ĐÁ KHỔNG LỒ lớn dần trên hai tay phụ (đá từ mặt đất bay lên nhập vào), hai nhịp nện gồng, bốn tay ném: tảng bay
        // vồng xuống đối thủ, vỡ: dăm, vòng bụi lớn, mưa đá nhỏ
        public float NVienTang(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.5f, lead), k = L / VienSkill, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            float t0 = T;
            // bán kính như bản xem trước (tho5_fx.quy_nui_skill: rig 70 → 220 đơn vị × 1,8 "khổng lồ", con cao ~1005): 0,125 → 0,39 chiều cao.
            // Lớn dần theo NHỊP ĐẬP (nhanh dần), 0,06 s trước lúc ném NÉN lại (người dùng 2026-11-18: tụ cầu theo nhịp, nén 1–2 khung rồi chớp)
            Func<float, float> rLuc = t =>
            {
                float u = Mathf.Clamp01((t / k - VienTu0) / (VienTu1 - VienTu0)), nen = t > L - 0.06f && t < L ? 0.86f : 1;
                return (0.125f + 0.27f * Mathf.Pow(u, 1.3f)) * (1 + 0.06f * Mathf.Sin(u * u * 30) * (1 - u * 0.3f)) * nen * casterH;
            };
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
            // đá từ mặt đất bay lên nhập vào tảng: vệt bụi + sỏi xoay theo đường vồng, nhanh dần, dày dần tới lúc ném; vòng co về tảng
            Every((VienTu0 + 0.05f) * k, VienTu1 * k, x => 14 + 26 * x, x =>
            {
                var p0 = casterFeet + new Vector2(dir * U(-0.7f, 0.45f) * casterH, U(-6, 4) * sH);
                ToHut(p0, s => tay(s - t0), U(0.34f, 0.42f), U(3.2f, 6f) * sH, U(0, 1) < 0.5f ? ToDa : ToDa2, 2f, 40 * sH);
                if (U(0, 1) < 0.3f)                                              // khung vẽ sẵn (2026-11-19): bụi chỗ đá bứt khỏi đất, 40 % số cụm, to × 1,3
                    ToBuiFb(p0, new Vector2(U(-30, 30), -40) * sH, 0.5f, 5 * sH, 10 * sH, Back, null, FbBuiC, 0.4f, 1.3f, true);
            });
            foreach (float f in new[] { 0.3f, 0.6f, 0.9f })
                At((VienTu0 + (VienTu1 - VienTu0) * f) * k, () => ToVongCo(s => tay(s - t0), 1.9f * rLuc(T - t0), 0.34f * k, ToCat3, 0.8f));
            foreach (float tn in new[] { VienNen1, VienNen2 })
                At(tn * k, () =>
                {
                    ToVong(casterFeet + new Vector2(-dir * 0.13f * casterH, 0), 90 * sH);
                    Shake?.Invoke(0.18f);
                    var m = tay(tn * k);
                    for (int i = 0; i < 2; i++) ToSoiCum(m + U2(-30, 30) * sH, new Vector2(U(-80, 80), 40) * sH, 3.2f * sH, ToDa, ToDa2, casterFeet.y + 2);
                });
            At(L, () =>
            {
                var dich0 = foeBody + new Vector2(-dir * 0.06f * tH, 10 * sc);
                ToChop(tay(L), 0.5f * casterH, Front, 0.1f);
                ToTangBay(tay(L), dich0, VienBayTang, rLuc(L - 0.07f), 90 * sc, true, p =>
                {
                    ToNo(p, foeFeet.y, tH, 2.8f, ToDa, ToPhach, dich0 - tay(L));
                    // khung vẽ sẵn (2026-11-19): tảng khổng lồ vỡ thì bụi đất cuộn lên to sau lưng đối thủ (chân ở mặt đất, cao 0,95 tH)
                    if (HasFb("khoi"))
                        FbBui(foeFeet + new Vector2(-dir * 0.12f * tH, 0), new Vector2(-dir * 20, -20) * sc, 0.95f * tH, Back, FbBuiC, 1.1f, 0.92f, 3);
                    ToVong(foeFeet, 130 * sc, 0.7f);
                    ToHo(foeFeet, 42 * sc);
                    Shake?.Invoke(0.3f);
                    for (int i = 0; i < 6; i++)
                        At(0.08f + 0.06f * i, () =>
                        {
                            var dich = foeBody + new Vector2(U(-50, 50), U(0, 30)) * sc;
                            ToTangBay(foeBody + new Vector2(U(-60, 60) * sc, -260 * sc), dich, 0.28f, 6 * sc, 10 * sc, false,
                                q => ToNo(q, foeFeet.y, tH, 0.5f, ToDa, ToDa2, new Vector2(0, 1)), 1, -1, 0, foeFeet.y);
                        });
                }, 0.85f, seed, 6, foeFeet.y);
            });
            return L + VienBayTang;
        }

        // ================= Sa Trùng (rua_nui, ải 40; rig sau_dat_1, ArtGen/Spine/sau_dat_rig.py; inbox/sau_dat_ghichu.md) =================
        // Sâu cát khổng lồ trồi giữa tổ phiến đá. Mốc rig: đánh thường lao 0,54, ĐỚP 0,65 (= trúng), nghiến 0,75; chiêu mana vươn 0,20, giáng
        // đầu 1,06, gai 1,14, trúng 1,20; chiêu cuối gầm 0,32, lặn 0,50, chạy ngầm 0,80 → 1,25 (trồi lùi về phía mình ~0,3 chiều cao so với
        // đích), ngoạm 1,62 (= trúng), nghiến 1,72, lặn 1,98, trồi ở nhà 2,35, gầm 2,72. Con sâu tự đi tới đối thủ (xương fly_sau, game lái):
        // ở đây chỉ đất, đá, bụi, gai, vết cắn.
        const float TrungDop = 0.65f, TrungLao = 0.54f, TrungNghien = 0.75f;
        const float TrungGaiT = 1.20f, TrungVuon = 0.20f, TrungNen = 1.06f, TrungGai = 1.14f;
        const float TrungMieng = 1.62f, TrungGam = 0.32f, TrungLan = 0.50f, TrungNgam = 0.80f, TrungTroi = 1.25f, TrungNghien2 = 1.72f,
            TrungLan2 = 1.98f, TrungVe = 2.35f, TrungGam2 = 2.72f;
        static readonly Vector2 TrungNenP = new Vector2(0.48f, 0f);     // chỗ đầu giáng xuống đất trước tổ (cast 1,06)
        const float TrungLechXa = 0.30f;                                // chiêu cuối: chỗ trồi lùi về phía mình (chiều cao tướng)

        // đất phụt (sâu chui lên / lặn xuống): vòng bụi, sỏi bắn cao rồi rơi nảy, bụi cuộn hai bên. muc: 1 vừa, 2 lớn
        void TrungPhut(Vector2 chan, float sH, float muc)
        {
            ToVong(chan, 95 * sH * Mathf.Sqrt(muc), 0.55f);
            ToHo(chan, 30 * sH * Mathf.Sqrt(muc), 0.8f);
            ToChop(chan + new Vector2(0, -0.1f * 150 * sH), 0.24f * 150 * sH * Mathf.Sqrt(muc), Back, 0.1f);
            int n = Mathf.RoundToInt(2.4f * muc);
            for (int i = 0; i < n; i++)
            {
                var v = new Vector2(U(-200, 200), -U(320, 560) * (0.8f + 0.2f * muc)) * sH;
                ToSoiCum(chan + new Vector2(U(-0.25f, 0.25f) * 150 * sH, -4 * sH), v, U(3f, 4.6f) * sH * (0.85f + 0.15f * muc),
                    i % 2 == 0 ? ToCat2 : ToDa, ToCatSam, chan.y + U(-2, 6) * sH, (i & 1) == 0 ? Front : Back);
            }
            for (int d = -1; d <= 1; d += 2)                                     // đất phụt: hai cụm bụi nhiều múi bốc lên, lan hai bên
                ToCum(chan + new Vector2(d * U(20, 40) * sH, -U(8, 20) * sH), new Vector2(d * U(40, 90), -U(40, 80)) * sH, 11 * sH * Mathf.Sqrt(muc),
                    muc >= 1.5f ? 4 : 3, d < 0 ? Back : Front, 0, FbCatC);
        }

        // gò đất chạy ngầm từ a tới b trong (t0, t1): một ụ đất nâu (mảng liền viền mực) trượt dọc mặt đất, bụi + sỏi văng phía sau, vết nứt
        // theo sau
        void TrungGo(Vector2 a, Vector2 b, float t0, float t1, float sc)
        {
            float dur = Mathf.Max(0.05f, t1 - t0);
            At(t0, () =>
            {
                var p = new P { pos = a, life = dur, group = Front, sz = 1 };
                p.upd = (q, dt, s) =>
                {
                    float f = Mathf.Clamp01(q.age / dur);
                    var cu = q.pos;
                    q.pos = Vector2.Lerp(a, b, f * f * (3 - 2 * f));
                    q.vel = Vector2.zero;
                    q.R0 += (q.pos - cu).magnitude;                              // bụi rải theo quãng gò vừa chạy: vệt liền, không lấm tấm
                    bool fb = s.HasFb("khoi");                                   // khung vẽ sẵn (2026-11-19): cụm cát vẽ sẵn, bước gấp đôi, to × 1,3
                    if (q.R0 < (fb ? 18 : 9) * sc) return;
                    q.R0 -= (fb ? 18 : 9) * sc;
                    if (fb)
                        s.ToBuiFb(q.pos + new Vector2(s.U(-12, 12) * sc, -5 * sc), new Vector2(-Mathf.Sign(b.x - a.x) * s.U(30, 80), -s.U(30, 70)) * sc, 0.5f,
                            6 * sc, 13 * sc, s.U(0, 1) < 0.5f ? Front : Back, null, FbCatC, 1, 1.3f, true);
                    else
                        ToBui(q.pos + new Vector2(s.U(-12, 12) * sc, -5 * sc), new Vector2(-Mathf.Sign(b.x - a.x) * s.U(30, 80), -s.U(30, 70)) * sc, 0.5f,
                            6 * sc, 13 * sc, s.U(0, 1) < 0.5f ? Front : Back, false);
                    if (s.U(0, 1) < 0.3f)
                        ToSoi(q.pos + new Vector2(0, -6 * sc), new Vector2(s.U(-120, 120), -s.U(180, 320)) * sc, s.U(2f, 3.4f) * sc,
                            s.U(0, 1) < 0.5f ? ToCat2 : ToCatSam, q.pos.y + 2 * sc);
                };
                p.draw = (q, k, buf) =>
                {
                    float w = 36 * sc, h = 16 * sc * (0.6f + 0.4f * Mathf.Sin(q.age * 40));
                    const int n = 9;
                    int s0 = mp.Count;
                    for (int i = 0; i < n; i++)
                    {
                        float u = i / (n - 1f), ang = Mathf.PI * u;
                        mp.Add(q.pos + new Vector2(-Mathf.Cos(ang) * w, -Mathf.Sin(ang) * h - 2 * sc * Mathf.Sin(ang * 3 + q.age * 30)));
                    }
                    MSolid(Front, 23, s0, n, ToCatSam, 1, 2.2f);
                };
                Add(p);
                ToNut(a, b, dur, sc);
            });
        }

        // gai đá đầu ngạnh trồi từ đất (thân sa thạch, mặt bên sẫm, ngạnh hổ phách ở mũi), nghiêng ang độ; trồi 0,08 s, giữ, lún 0,2 s
        void TrungGaiDa(Vector2 chan, float w, float h, float ang, float giu, int group)
        {
            const float tLen = 0.08f, tLun = 0.2f;
            // khung vẽ sẵn (2026-11-19; "gai ... đâm lên xấu"): cụm gai sa thạch vẽ sẵn (khung gai sắt nhuộm sa thạch), nghiêng theo ang (khung
            // xoay ngược kim nên đổi dấu), lật theo phía nghiêng; đúng nhịp cũ trồi 0,08 s, giữ, lún 0,2 s; đỉnh cao bằng gai cũ
            if (HasFb("gai_sat"))
            {
                FbGai(chan, h, group, FbSaThach, tLen, giu, tLun, ang < 0, -ang);
                return;
            }
            var p = new P { pos = chan, life = tLen + giu + tLun, group = group, sz = h, wd = w, ang = ang };
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                float g = t < tLen ? 1.12f * EaseOut(t / tLen) : t < tLen + 0.05f ? 1.12f - 0.12f * (t - tLen) / 0.05f :
                    t < tLen + giu ? 1 : Mathf.Max(0, 1 - (t - tLen - giu) / tLun);
                float hh = q.sz * g;
                if (hh < 3) return;
                float a = q.ang * Mathf.Deg2Rad, hw = q.wd / 2;
                var up = new Vector2(Mathf.Sin(a), -Mathf.Cos(a));
                var nn = new Vector2(-up.y, up.x);
                var dinh = q.pos + up * hh;
                int s0 = mp.Count;                                                   // thân gai
                mp.Add(q.pos - nn * hw);
                mp.Add(q.pos - nn * (hw * 0.55f) + up * (hh * 0.55f));
                mp.Add(dinh);
                mp.Add(q.pos + nn * (hw * 0.6f) + up * (hh * 0.5f));
                mp.Add(q.pos + nn * hw);
                MSolid(q.group, 24, s0, 5, ToSaThach, 1, 2.4f);
                int s1 = mp.Count;                                                   // mặt bên sẫm
                mp.Add(q.pos + nn * (hw * 0.15f));
                mp.Add(dinh - up * (hh * 0.12f));
                mp.Add(q.pos + nn * (hw * 0.6f) + up * (hh * 0.5f));
                mp.Add(q.pos + nn * (hw * 0.95f));
                MFill(q.group, 24.01f, s1, 4, ToCat2, 1, false);
                int s2 = mp.Count;                                                   // ngạnh hổ phách ở mũi
                float bh = Mathf.Min(0.24f * hh, 1.1f * q.wd);
                mp.Add(dinh);
                mp.Add(dinh - up * bh - nn * (hw * 0.42f));
                mp.Add(dinh - up * (bh * 0.7f));
                mp.Add(dinh - up * bh + nn * (hw * 0.42f));
                MSolid(q.group, 24.02f, s2, 4, ToPhach, 1, 2f);
            };
            Add(p);
        }

        // ĐÒN THƯỜNG "Đớp nghiền" (rig khai đánh thường lao): bụi dưới tổ lúc phóng; ĐỚP: vết cắn lớn, chớp, dăm đá + cát; nghiến: hai nhịp dăm
        public float NTrungDop(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead), k = L / TrungDop, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sH = casterH / 150f;
            At(TrungLao * k, () =>
            {
                for (int d = 0; d < 2; d++)
                    ToCum(casterFeet + new Vector2(dir * (d == 0 ? -0.15f : 0.15f) * casterH, -4 * sH), new Vector2(-dir * U(70, 140), -U(20, 45)) * sH, 12 * sH, 3, Back,
                        0, FbCatC);
            });
            At(L, () =>
            {
                var c = foeBody + new Vector2(-dir * 0.1f * tH, 0.04f * tH);
                ToCan(c, tH * 1.35f);
                ToNo(c, foeFeet.y, tH, 1.5f, ToCat, ToDa, new Vector2(dir, 0));
                ToVong(foeFeet, 70 * tH / 150f);
            });
            for (int i = 0; i < 2; i++)
            {
                float tt = (TrungNghien + 0.09f * i) * k;
                At(tt, () => ToNo(foeBody + new Vector2(U(-0.12f, 0.12f) * tH, U(-0.1f, 0.1f) * tH), foeFeet.y, tH, 0.5f, ToCat2, ToDa));
            }
            return L;
        }

        // CHIÊU MANA "Gai ngầm": bụi rơi khỏi tổ lúc vươn; GIÁNG đầu xuống đất trước tổ (vòng bụi, rung, vết nứt lan tới đối thủ); BA GAI ĐÁ
        // đầu ngạnh trồi quanh chân đối thủ (gai giữa sau lưng nó cao 1,3 lần, hai gai bên nghiêng ra ngoài), trúng: dăm đá lớn
        public float NTrungGai(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / TrungGaiT, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            At(TrungVuon * k, () =>
                ToCum(casterFeet + new Vector2(0, -0.1f * casterH), new Vector2(0, -30) * sH, 12 * sH, 4, Back, 0.7f, FbCatC));
            var nen = ToSan(casterFeet, casterH, dir, TrungNenP);
            At(TrungNen * k, () =>
            {
                ToChop(nen + new Vector2(0, -0.08f * casterH), 0.3f * casterH, Front, 0.1f);
                ToVong(nen, 110 * sH, 0.55f);
                ToHo(nen, 34 * sH);
                for (int d = -1; d <= 1; d += 2)
                    ToCum(nen + new Vector2(d * 30 * sH, -4 * sH), new Vector2(d * 100, -35) * sH, 13 * sH, 3, Front, 0, FbCatC);
                Shake?.Invoke(0.28f);
                ToNut(nen, foeFeet + new Vector2(-dir * 0.1f * tH, 2), (TrungGai - TrungNen) * k, sc);
            });
            At(TrungGai * k, () =>
            {
                float ra = HasFb("gai_sat") ? 0.68f : 0.55f;                     // khung vẽ sẵn: cụm gai rộng ~ cao nên hai gai bên dời ra ngoài thân thêm
                TrungGaiDa(foeFeet + new Vector2(dir * 0.12f * tH, 2 * sc), 0.30f * tH, 1.30f * tH, dir * 6, 0.42f, Back);
                TrungGaiDa(foeFeet + new Vector2(-ra * tH, 4 * sc), 0.22f * tH, 0.80f * tH, -18, 0.34f, Back);
                TrungGaiDa(foeFeet + new Vector2(ra * tH, 4 * sc), 0.22f * tH, 0.80f * tH, 18, 0.34f, Front);
                ToVong(foeFeet, 95 * sc, 0.5f);
            });
            At(L, () => ToNo(foeBody + new Vector2(0, 0.06f * tH), foeFeet.y, tH, 1.9f, ToSaThach, ToDa));
            return L;
        }

        // CHIÊU CUỐI "Miệng sa mạc": gầm (rung); LẶN: đất phụt ở tổ; gò đất chạy ngầm tới trước mặt đối thủ; TRỒI: đất phụt lớn, rung; NGOẠM
        // (khung trúng): vết cắn rất lớn, chớp, dăm, ba vết nứt toả; nghiến: dăm; lặn lại: đất phụt chỗ trồi; trồi về tổ: đất phụt; gầm
        public float NTrungMieng(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead), k = L / TrungMieng, dir = foeFeet.x >= casterFeet.x ? 1 : -1, sc = tH / 150f, sH = casterH / 150f;
            var troi = foeFeet + new Vector2(-dir * TrungLechXa * casterH, 0);
            At(TrungGam * k, () => Shake?.Invoke(0.12f));
            At(TrungLan * k, () => TrungPhut(casterFeet + new Vector2(dir * 0.2f * casterH, 0), sH, 1.2f));
            TrungGo(casterFeet + new Vector2(dir * 0.35f * casterH, 0), troi, TrungNgam * k, TrungTroi * k, sH);
            At(TrungTroi * k, () =>
            {
                TrungPhut(troi, sH, 2f);
                Shake?.Invoke(0.25f);
            });
            At(L, () =>
            {
                var c = foeBody + new Vector2(0, 0.02f * tH);
                ToCan(c, tH * 1.7f);
                ToNo(c, foeFeet.y, tH, 2.4f, ToCat, ToDa, new Vector2(dir, 0.6f));
                ToHo(foeFeet, 40 * sc);
                for (int i = 0; i < 3; i++)
                {
                    float a = (i - 1) * 0.55f;
                    ToNut(foeFeet, foeFeet + new Vector2(Mathf.Sin(a) * 0.9f * tH * (i == 1 ? 0.4f : 1), 4 * sc), 0.14f, sc);
                }
                ToVong(foeFeet, 120 * sc, 0.6f);
            });
            for (int i = 0; i < 2; i++)
            {
                float tt = (TrungNghien2 + 0.1f * i) * k;
                At(tt, () => ToNo(foeBody + new Vector2(U(-0.15f, 0.15f) * tH, U(-0.1f, 0.1f) * tH), foeFeet.y, tH, 0.7f, ToCat2, ToDa));
            }
            At(TrungLan2 * k, () => TrungPhut(troi, sH, 1.2f));
            At(TrungVe * k, () => TrungPhut(casterFeet + new Vector2(dir * 0.2f * casterH, 0), sH, 1.6f));
            At(TrungGam2 * k, () => Shake?.Invoke(0.12f));
            return L;
        }

        // ================= nhịp trúng PHỤ của chiêu nhiều cú (người dùng 2026-11-18: "không có sự va chạm giữa tia đó với địch") =================
        // StageViewThoTinh.cs đọc hàm này để đối thủ CHỚP + GIẬT nhẹ ở từng cú đạn / mảnh / cột chạm tới; cú chính (giờ trúng hàm hiệu ứng trả về)
        // do StageView.Hurt lo nên bỏ qua. Mốc cùng công thức với hàm hiệu ứng ở trên / HatThach.cs. kind: mã chiêu; t: giây clip của kẻ đánh;
        // lead: giờ trúng clip game dùng. since: giây từ cú gần nhất; muc: độ mạnh (cú cuối mạnh hơn). Chạy trên luồng chính (bộ đệm tĩnh).
        static readonly float[] thoNhipT = new float[12];
        public static bool ThoNhip(string kind, float t, float lead, out float since, out float muc)
        {
            since = muc = 0;
            if (kind == null || !kind.StartsWith("n_")) return false;
            var a = thoNhipT;
            int n = 0;
            float L = Mathf.Max(0.05f, lead), chinh = L, m = 0.8f, mCuoi = 1.25f, k;
            switch (kind)
            {
                case "n_giap_soi":
                case "n_giap_soi2":
                    k = L / GiapCast;
                    for (int j = 0; j < 3; j++) a[n++] = (GiapPhong[j] + GiapBay) * k;
                    chinh = a[0];
                    break;
                case "n_tich_phien":
                case "n_tich_phien2":
                    var ph = kind == "n_tich_phien" ? TichPhong : TichPhong2;
                    k = L / (kind == "n_tich_phien" ? TichCast : 0.672f);
                    foreach (float p in ph) a[n++] = (p + TichBay) * k;
                    chinh = a[0];
                    break;
                case "n_long_luoi":
                case "n_long_luoi1":
                    var ch = kind == "n_long_luoi" ? LongChem : LongChem1;
                    k = L / (kind == "n_long_luoi" ? LongCast : LongChem1[0]);
                    foreach (float c in ch) a[n++] = c * k + LongBayLuoi;
                    chinh = a[0];
                    break;
                case "n_thach_xoay":
                case "n_thach_xoay1":
                    k = L / ThtXoayT;
                    int ns = kind == "n_thach_xoay" ? ThtD2.s0.Length : ThtD1.s0.Length;
                    for (int j = 0; j < ns; j++) a[n++] = (ThtPhong0 + ThtPhongCach * j + ThtBay) * k;
                    break;
                case "n_giap_mua":
                case "n_giap_mua2":
                    bool d2 = kind == "n_giap_mua2";
                    k = Mathf.Max(0.3f, lead) / (d2 ? 1.56f : GiapSkill);
                    L = Mathf.Max(0.3f, lead);
                    chinh = L;
                    for (int j = 0, nm = d2 ? 10 : 7; j < nm && n < a.Length - 1; j++)
                        a[n++] = Mathf.Min(L - 0.05f, ((d2 ? 1.22f : GiapMua) + (d2 ? 0.032f : 0.045f) * j) * k);
                    a[n++] = L;
                    m = 0.45f;
                    break;
                case "n_vien_dam":
                    k = L / VienDam[2];
                    foreach (float d in VienDam) a[n++] = d * k;
                    m = 0.7f;
                    break;
                case "n_trung_dop":
                    k = L / TrungDop;
                    a[n++] = L;
                    for (int i = 0; i < 2; i++) a[n++] = (TrungNghien + 0.09f * i) * k;
                    m = mCuoi = 0.55f;
                    break;
                case "n_trung_mieng":
                    L = chinh = Mathf.Max(0.3f, lead);
                    k = L / TrungMieng;
                    a[n++] = L;
                    for (int i = 0; i < 2; i++) a[n++] = (TrungNghien2 + 0.1f * i) * k;
                    m = mCuoi = 0.65f;
                    break;
                case "n_thach_vo":
                    k = L / ThtDop;
                    a[n++] = L;
                    a[n++] = ThtXe1 * k;
                    a[n++] = ThtXe2 * k;
                    m = mCuoi = 0.55f;
                    break;
                case "n_long_cot":
                    L = chinh = Mathf.Max(0.3f, lead);
                    k = L / LongSkill;
                    a[n++] = LongCotT[0] * k;
                    a[n++] = LongCotT[1] * k;
                    a[n++] = L;
                    m = 0.7f;
                    break;
                case "n_long_cot1":
                    L = chinh = Mathf.Max(0.3f, lead);
                    k = L / LongSkill1;
                    a[n++] = LongCot1a * k;
                    a[n++] = L;
                    m = 0.65f;
                    break;
                default:
                    return false;
            }
            for (int i = n - 1; i >= 0; i--)
            {
                if (t < a[i]) continue;
                if (Mathf.Abs(a[i] - chinh) < 0.03f) return false;              // cú chính: sân đã chớp, bật lùi (StageView.Hurt)
                since = t - a[i];
                muc = i == n - 1 ? mCuoi : m;
                return since < 0.2f;
            }
            return false;
        }
    }
}
