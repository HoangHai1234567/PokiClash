// Bộ Mộc của lớp hạt chồng lớp phẳng (2026-11-12, tướng tinh linh rừng Mầm Ú, id mam_u: "chiêu mana há mồm bắn ra nhiều lá cây vào người
// đối thủ"). Hạt LÁ là ảnh xám có gân (ArtGen/Spine/la.py → hat_leaf_<i>, hat_leafs_<i>) nhuộm bằng Image.color, một lớp mực + một
// lớp màu, lật nghiêng lúc bay. Dùng chung khung của bộ Thủy (HatNuoc.cs): mã chiêu bắt đầu bằng "n_", phát lúc clip BẮT ĐẦU kèm lead,
// bảng màu lấy từ WThemes (mực, lục đậm, lục non, lục nhạt, phấn), nên StageView / HeroViewer không phải thêm đường riêng.
// Nâng 2026-11-18 (người dùng chê tia cụt, nổ / sóng âm chưa đẹp, khói rải rác, hút khí xấu, màu tối, hạt lẻ to): đầu file này có bộ đồ dùng
// chung của mười tướng Mộc (bảng màu tươi, chớp nổ, bụi cụm tách dần, vòng cung dẹt trên đất, vết trên đất, tia vụn theo cụm, lá rơi lượn,
// tia năng lượng có bông va chạm và tắt bằng vỡ vụn). Ảnh hạt mới hat_kr_* dùng khi đã nhập; chưa nhập thì về hình cũ, không lỗi.
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // ================= ĐỒ DÙNG CHUNG BỘ MỘC (2026-11-18) =================
        static readonly Color MocChanh = C(232, 245, 122), MocKem = C(250, 255, 224); // vàng chanh lõi, kem (góp ý 2026-11-18)
        static readonly Color VetC = C(92, 74, 52), VetNut = C(214, 186, 138);         // vết đất: vệt sẫm, màu nhuộm vết nứt
        static readonly Color CungC = C(204, 174, 124);                                 // vòng cung dẹt của cú dậm / nện: be đất đậm hơn nền cát một nấc
        static readonly Color[] CumDat = { C(244, 232, 200), C(216, 194, 152) };      // cụm bụi đất be sáng: đỉnh nhạt, đáy đậm
        static readonly Color[] CumPhan = { C(250, 255, 224), C(206, 232, 118) };     // cụm phấn lá: kem, chanh non

        static Color[] MPal(Color d, Color m, Color l) => new[] { C(43, 33, 24), d, m, l, C(250, 255, 224) };

        // bảng màu TƯƠI theo tướng (mực, đậm sát viền, giữa, tươi, kem). Góp ý 2026-11-18 "màu tươi hơn": lá #7BD34A, lục #3FAE3A, lục đậm sát
        // viền #2A7F2E, lõi vàng chanh #E8F57A, kem #FAFFE0; giữ nét riêng từng tướng (Gạc Đá, Lộc Phong lục ngọc; Giác Mộc hổ phách).
        // Đề xuất chuyển vào WThemes (HatNuoc.cs) rồi bỏ bảng này và MocSang.
        static readonly Dictionary<string, Color[]> MocTuoi = new Dictionary<string, Color[]>
        {
            { "mam_u", MPal(C(42, 127, 46), C(92, 190, 64), C(160, 226, 96)) },
            { "tien_la", MPal(C(42, 127, 46), C(96, 186, 66), C(236, 240, 172)) },
            { "phong_linh", MPal(C(42, 127, 46), C(63, 174, 58), C(123, 211, 74)) },
            { "gio_loc", MPal(C(50, 124, 46), C(88, 184, 60), C(150, 218, 92)) },
            { "hat_de", MPal(C(50, 124, 46), C(88, 184, 60), C(150, 218, 92)) }, // Cổ Vương (hệ Thổ, suất hat_de từ 2026-11-19; chiêu HatCoVuong.cs gọi MocSang)
            { "tho_hoang", MPal(C(40, 120, 50), C(80, 176, 66), C(168, 228, 108)) },
            { "thanh_long", MPal(C(30, 124, 80), C(54, 176, 100), C(150, 228, 140)) },
            { "long_vuot", MPal(C(56, 124, 52), C(104, 170, 64), C(170, 214, 96)) },
            { "gac_da", MPal(C(26, 154, 106), C(58, 210, 144), C(176, 244, 204)) },
            { "bom_la", MPal(C(28, 154, 110), C(62, 210, 150), C(188, 246, 214)) },
            { "moc_tinh", MPal(C(226, 138, 28), C(252, 196, 56), C(255, 236, 140)) },
        };
        static readonly Dictionary<WTheme, WTheme> mocSang = new Dictionary<WTheme, WTheme>();

        // đổi bảng màu của tướng Mộc đang ra chiêu sang bản tươi (gọi đầu mỗi chiêu Mộc, sau UseTheme của StageView / HeroViewer); tướng không
        // có trong MocTuoi giữ nguyên. Mỗi tướng chỉ dựng bảng một lần.
        void MocSang()
        {
            if (wth == null) return;
            if (mocSang.TryGetValue(wth, out var s))
            {
                wth = s;
                return;
            }
            var moi = wth;
            foreach (var kv in WThemes)
                if (kv.Value == wth && MocTuoi.TryGetValue(kv.Key, out var w))
                {
                    moi = new WTheme { w = w, fx = wth.fx };
                    break;
                }
            mocSang[wth] = moi;
            mocSang[moi] = moi;
            wth = moi;
        }

        // StageView gán (đề xuất): con đứng gần điểm này chớp + giật nhẹ, mức 0..1 (tia, luồng lá, sóng âm trúng liên hồi). Null thì bỏ qua.
        public Action<Vector2, float> DanhTrung;

        // CHỚP NỔ phẳng 1–2 khung (đỉnh cú trúng): kem lõi chanh viền mực, nhỏ hơn thân đối thủ. Ảnh kr_chop; chưa có thì sao gai burst.
        P Chop(Vector2 c, float size, float life = 0.07f, int group = Front)
        {
            var p = new P { pos = c, life = life, group = group, sz = size, ang = U(0, 360), seed = rng.Next(4) };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (0.8f + 0.3f * EaseOut(k / 0.5f));
                int i = q.seed & 3;
                var f = S("kr_chop_" + i);
                if (f != null)
                {
                    Put(buf, q.group, 45, S("kr_chops_" + i) ?? f, Ink, q.pos, s + 6, 1, q.ang);
                    Put(buf, q.group, 45.2f, f, MocChanh, q.pos, s, 1, q.ang);
                    Put(buf, q.group, 45.4f, f, MocKem, q.pos, s * 0.6f, 1, q.ang + 15);
                    return;
                }
                Put(buf, q.group, 45, S("bursts_" + i), Ink, q.pos, s + 6, 1, q.ang);
                Put(buf, q.group, 45.2f, S("burst_" + i), MocChanh, q.pos, s, 1, q.ang);
                Put(buf, q.group, 45.4f, S("burst_" + ((i + 1) & 3)), MocKem, q.pos, s * 0.58f, 1, q.ang + 20);
            };
            return Add(p);
        }

        // CỤM BỤI / PHẤN nhiều múi (mẫu Kingdom Rush 5 tower_build_dust): to gần đủ ngay khung đầu, phình nhẹ, rồi TÁCH thành ba cụm nhỏ toả
        // ra, bay lên, nhỏ dần rồi mới mờ (không tắt phụt). Hai tông phẳng: đỉnh nhạt mau[0], đáy đậm mau[1]; viền mực mờ trước ruột. Ảnh
        // kr_khoi + kr_khoiday (bóng nửa dưới) cho cụm mẹ, kr_khoinho cho cụm con; chưa có thì cụm mây sblob vẽ hai lớp (đáy đậm, đỉnh nhạt dời lên).
        static readonly Vector2[] CumTach = { new Vector2(-0.48f, 0.12f), new Vector2(0.5f, 0.06f), new Vector2(0.04f, -0.44f) };

        public P BuiCum(Vector2 pos, Vector2 vel, float r, float life = 0, int group = Back, Color[] mau = null, bool tach = true)
        {
            bool me = tach && r >= 7;
            var p = new P
            {
                pos = pos, vel = vel, life = life > 0 ? life : me ? U(0.28f, 0.4f) : U(0.45f, 0.7f), drag = 3.2f, acc = new Vector2(0, -36), seed = rng.Next(8),
                sz = r, group = group, stops = mau ?? CumDat, big = me, ang = U(-12, 12), spin = U(-20, 20), fade = 0.92f
            };
            p.draw = DrawCum;
            if (me)
                p.onDeath = (q, s) =>
                {
                    float rr = q.sz * 1.06f; // cỡ lúc tách = cuối pha phình
                    for (int i = 0; i < 3; i++)
                    {
                        var o = CumTach[(i + q.seed) % 3];
                        var c = new P
                        {
                            pos = q.pos + o * rr, vel = q.vel * 0.4f + o * s.U(50, 90) + new Vector2(0, -s.U(20, 50)), life = s.U(0.38f, 0.58f), drag = 2.2f,
                            acc = new Vector2(0, -60), seed = s.rng.Next(8), sz = rr * s.U(0.42f, 0.56f), group = q.group, stops = q.stops, ang = s.U(-20, 20),
                            spin = s.U(-30, 30), fade = q.fade
                        };
                        c.draw = s.DrawCum;
                        s.Add(c);
                    }
                };
            return Add(p);
        }

        void DrawCum(P q, float k, List<Item> buf)
        {
            float g, aInk = 1, aFill = 1;
            if (q.big) g = k < 0.2f ? 0.55f + 0.45f * EaseOut(k / 0.2f) : 1 + 0.06f * (k - 0.2f) / 0.8f; // cụm mẹ: không co, tới cuối đời thì tách
            else
            {
                g = k < 0.18f ? 0.8f + 0.2f * EaseOut(k / 0.18f) : 1 - 0.75f * SmoothStep(0.18f, 1, k);
                aInk = 1 - SmoothStep(0.3f, 0.75f, k);
                aFill = 1 - SmoothStep(0.62f, 1, k);
            }
            float r = q.sz * g;
            if (r < 1 || aFill < 0.03f) return;
            aFill *= q.fade;
            aInk *= q.fade;
            int i = q.seed & 3, g0 = q.group;
            Color top = q.stops[0], bot = q.stops[1];
            var sp = q.big ? S("kr_khoi_" + i) : (S("kr_khoinho_" + i) ?? S("kr_khoi_" + i));
            if (sp != null)
            {
                var sd = q.big ? S("kr_khois_" + i) : (S("kr_khoinhos_" + i) ?? S("kr_khois_" + i));
                float d = 2.3f * r;
                if (aInk > 0.03f) Put(buf, g0, 30, sd ?? sp, Ink, q.pos, d + 4, 1, q.ang, aInk);
                Put(buf, g0, 30.5f, sp, top, q.pos, d, 1, q.ang, aFill);
                var day = q.big ? S("kr_khoiday_" + i) : null;
                if (day != null) Put(buf, g0, 30.7f, day, bot, q.pos, d, 1, q.ang, aFill);
                return;
            }
            float d2 = 2.1f * r;
            if (aInk > 0.03f) Put(buf, g0, 30, S("ssolid_" + i), Ink, q.pos, d2 + 4, 1.12f, q.ang, aInk);
            Put(buf, g0, 30.5f, S("sblob_" + i), bot, q.pos, d2, 1.12f, q.ang, aFill);
            Put(buf, g0, 30.7f, S("sblob_" + ((i + 1) & 3)), top, q.pos + new Vector2(0, -0.17f * r), 0.8f * d2, 1.12f, q.ang + 8, aFill);
        }

        // VÒNG CUNG SÓNG DẸT trên đất (mẫu Kingdom Rush 5): elip phẳng không viền, nở nhanh, mỏng dần, đứt thành n cung, mỗi cung dày giữa thuôn
        // hai đầu. Ảnh kr_cung; chưa có thì dựng bằng mảng liền (dải hở).
        P CungDat(Vector2 c, float R0, float R1, float life, Color col, float day, int n = 4, float squash = 0.3f, int group = Floor, float layer = 31)
        {
            var p = new P
            {
                pos = c, life = life, R0 = R0, R1 = R1, col = col, wd = day, span = Mathf.Max(2, n), hgt = squash, group = group, ph = U(0, 6.28f),
                seed = rng.Next(4), tb = layer
            };
            p.draw = (q, k, buf) =>
            {
                float R = Mathf.Lerp(q.R0, q.R1, EaseOut(k));
                float a = 1 - SmoothStep(0.55f, 1, k);
                if (a < 0.03f || R < 2) return;
                var sp = S("kr_cung_" + q.seed);
                if (sp != null) // ảnh vẽ sẵn dẹt (cao ~0,36 bề ngang), vòng chiếm 90 % khung vuông
                {
                    Put(buf, q.group, q.tb, sp, q.col, q.pos, 2 * R / 0.9f, 1, 0, a);
                    return;
                }
                float th = q.wd * (1 - 0.75f * k);
                const int m = 7;
                float span = 6.2832f / q.span;
                for (int j = 0; j < q.span; j++)
                {
                    float tc = q.ph + span * j + 0.3f * Mathf.Sin(j * 2.3f + q.ph), hs = span * (0.3f + 0.08f * Mathf.Sin(j * 1.7f + 2 * q.ph));
                    int a0 = mp.Count;
                    for (int pass = 0; pass < 2; pass++)
                        for (int i = 0; i < m; i++)
                        {
                            float u = i / (m - 1f), ga = tc + hs * (2 * u - 1);
                            float rr = pass == 0 ? R : R - th * Mathf.Pow(Mathf.Sin(Mathf.PI * u), 0.7f);
                            mp.Add(q.pos + new Vector2(Mathf.Cos(ga) * rr, Mathf.Sin(ga) * rr * q.hgt));
                        }
                    MRibbon(q.group, q.tb, a0, a0 + m, m, q.col, a);
                }
            };
            return Add(p);
        }

        // VẾT TRÊN ĐẤT sau cú nện / nổ: vệt sẫm dẹt + vết nứt, hiện ngay, giữ hold giây rồi mờ trong 0,5 s
        P VetDat(Vector2 c, float R, float hold = 1f, Color? nut = null)
        {
            var p = new P { pos = c, life = hold + 0.5f, group = Floor, sz = R, seed = rng.Next(4), col = nut ?? VetNut, tb = hold };
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                float a = Mathf.Min(1, t / 0.05f) * (1 - SmoothStep(q.tb, q.life, t));
                if (a < 0.03f) return;
                float g = 0.75f + 0.25f * EaseOut(t / 0.12f);
                Put(buf, Floor, 1.2f, S("ell"), VetC, q.pos, 0.6f * q.sz * g, 3.2f, 0, 0.3f * a);
                Put(buf, Floor, 1.4f, S("crack_" + (q.seed & 3)), q.col, q.pos, 0.85f * q.sz * g, 2.4f, 0, 0.8f * a);
            };
            return Add(p);
        }

        // vòng va chạm không viền. Vòng đứng (squash ≥ 0,5): vòng mảnh ring; vòng nằm (squash < 0,5): ảnh kr_cung đứt đoạn vẽ sẵn dẹt (chưa có
        // thì ring dẹt)
        void VongVa(Vector2 c, float R0, float R1, float life, Color col, int group = Front, float squash = 1, float layer = 42)
        {
            if (squash >= 0.5f || S("kr_cung_0") == null)
            {
                RingN(c, life, R0, R1, col, squash, group, layer);
                return;
            }
            var p = new P { pos = c, life = life, group = group, col = col, R0 = R0, R1 = R1, tb = layer, seed = rng.Next(4) };
            p.draw = (q, k, buf) =>
            {
                float R = Mathf.Lerp(q.R0, q.R1, EaseOut(k));
                Put(buf, q.group, q.tb, S("kr_cung_" + q.seed), q.col, q.pos, 2 * R / 0.9f, 1, 0, 1 - SmoothStep(0.55f, 1, k));
            };
            Add(p);
        }

        static readonly float[] VetFy = { 0.22f, 0.27f, 0.47f, 0.16f }; // bề dày đầu vệt so với khung của ảnh kr_vet_<i> (dài 90 % khung)

        // VỆT THUÔN: đầu tròn về phía dir, đuôi nhọn ngược lại, dài len, dày day (đơn vị sân). Ảnh kr_vet (đầu ở +x, dài 90 % khung vuông, dày
        // VetFy); chưa có thì giọt kim needle (mũi lên, mũi làm đuôi)
        void VetPut(List<Item> buf, int g, float layer, bool muc, Color col, Vector2 tam, Vector2 dir, float len, float day, float alpha = 1, int i = 0)
        {
            if (len < 2 || day < 0.6f || alpha < 0.03f) return;
            var kv = S((muc ? "kr_vets_" : "kr_vet_") + (i & 3)) ?? (muc ? S("kr_vet_" + (i & 3)) : null);
            if (kv != null)
            {
                float h = day / VetFy[i & 3];
                Put(buf, g, layer, kv, col, tam, h, len / 0.9f / h, VelAng(dir), alpha);
            }
            else
            {
                float h = len / 0.95f;
                Put(buf, g, layer, S(muc ? "needles_0" : "needle_0"), col, tam, h, day / 0.31f / h, TipAngle(-dir), alpha);
            }
        }

        // TIA VỤN đi theo CỤM lệch cỡ (góp ý 2026-11-18: hạt lẻ nhỏ hơn, không đứng đơn lẻ): n vệt nhỏ bắn từ at quanh hướng dir, lệch tối đa
        // lech (radian); vệt đầu to nhất, còn lại nhỏ hơn; bắn mạnh rồi hãm, rơi nhẹ
        void TiaVunCum(Vector2 at, Vector2 dir, float lech, int n, float speed, float sz, int group = Front, Color? c1 = null, Color? c2 = null)
        {
            var d0 = Unit(dir);
            float a0 = Mathf.Atan2(d0.y, d0.x) + U(-0.4f, 0.4f) * lech;
            Color ca = c1 ?? MocChanh, cb = c2 ?? MocKem;
            for (int i = 0; i < n; i++)
            {
                float a = a0 + U(-0.6f, 0.6f) * lech;
                float f = i == 0 ? 1 : U(0.45f, 0.8f);
                var p = new P
                {
                    pos = at + U2(-3, 3), vel = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * speed * U(0.75f, 1.15f) * (0.7f + 0.3f * f), life = U(0.16f, 0.28f),
                    drag = 6, acc = new Vector2(0, 520), seed = rng.Next(4), sz = sz * f, group = group, col = (i & 1) == 0 ? ca : cb
                };
                p.draw = DrawVun;
                Add(p);
            }
        }

        void DrawVun(P q, float k, List<Item> buf)
        {
            float sp = q.vel.magnitude;
            float day = q.sz * (1 - k * k);
            if (day < 0.6f) return;
            float len = day * Mathf.Clamp(sp / 70, 1.8f, 4.2f);
            var d = sp > 1 ? q.vel / sp : Vector2.right;
            VetPut(buf, q.group, 40, true, Ink, q.pos, d, len + 3, day + 2.6f, 1, q.seed);
            VetPut(buf, q.group, 40.2f, false, q.col, q.pos, d, len, day, 1, q.seed);
        }

        // lá rơi LƯỢN: rơi chậm, đưa qua đưa lại, lật; co nhỏ ở cuối đời, không tắt phụt
        P LaRoi(Vector2 pos, Vector2 vel, float life, float r, int group = Front)
        {
            var q = Leaf(pos, vel, life, r, 150, 1.6f, group);
            q.spin = U(-160, 160);
            q.upd = (z, dt, s) => z.vel.x += Mathf.Sin(z.age * 5.2f + z.ph) * 260 * dt;
            return q;
        }

        // mảnh năng lượng vỡ (tia tắt): lá liễu nhọn hai đầu xoay, rơi, co
        void DrawMangVo(P q, float k, List<Item> buf)
        {
            float s = q.sz * (1 - SmoothStep(0.55f, 1, k));
            if (s < 0.8f) return;
            float r = q.ang * Mathf.Deg2Rad;
            var d = new Vector2(Mathf.Cos(r), -Mathf.Sin(r));
            LaLieu(buf, q.group, 41, true, Ink, q.pos, d, 2.6f * s + 5, 0.75f * s + 4, 1);
            LaLieu(buf, q.group, 41.3f, false, q.col, q.pos, d, 2.6f * s, 0.75f * s, 1);
        }

        // bông toé (đầu tia, chỗ va chạm): ảnh kr_tiadau (thân tròn ở ~22 % bề ngang khung, gai toé về +x) hoặc bông nước crown; bốn lớp (mực,
        // giữa, vàng chanh, kem) cùng neo ở THÂN bông = c, gai toé theo dir; hinh: đổi dáng (gọi với số đổi mỗi 2 khung)
        void BongPut(List<Item> buf, int g, Vector2 c, Vector2 dir, float sz, int hinh, float alpha = 1)
        {
            if (sz < 2) return;
            int i = hinh & 3;
            var w = W;
            var td = S("kr_tiadau_" + i);
            if (td != null)
            {
                float ang = VelAng(dir) + ((hinh * 37) % 7 - 3) * 6f;
                const float Than = 0.28f; // tâm khung cách thân bông 0,28 khung theo hướng toé
                Put(buf, g, 43, S("kr_tiadaus_" + i) ?? td, Ink, c + dir * (Than * (sz + 6)), sz + 6, 1, ang, alpha);
                Put(buf, g, 43.2f, td, w[2], c + dir * (Than * sz), sz, 1, ang, alpha);
                Put(buf, g, 43.4f, td, MocChanh, c + dir * (Than * 0.72f * sz), sz * 0.72f, 1, ang, alpha);
                Put(buf, g, 43.6f, td, MocKem, c + dir * (Than * 0.44f * sz), sz * 0.44f, 1, ang, alpha);
                return;
            }
            float a2 = (hinh * 53) % 360;
            int s2 = 2 + (hinh & 1);
            Put(buf, g, 43, S("crowns_" + s2), Ink, c, sz + 6, 1, a2, alpha);
            Put(buf, g, 43.2f, S("crown_" + s2), w[2], c, sz, 1, a2, alpha);
            Put(buf, g, 43.4f, S("crown_" + s2), MocChanh, c, sz * 0.74f, 1, a2 + 12, alpha);
            Put(buf, g, 43.6f, S("crown_" + (5 - s2)), MocKem, c, sz * 0.46f, 1, a2 + 30, alpha);
        }

        // BÔNG VA CHẠM của luồng / tia đập vào thân: hai bông toé xoè chữ V về phía con bắn (lệch ±50° quanh hướng ngược tia, như dòng bị mặt
        // thân hắt sang hai bên), đổi dáng mỗi 2 khung, hai bông lệch dáng nhau
        void BongVa(List<Item> buf, int g, Vector2 c, Vector2 nguoc, float sz, int hinh)
        {
            float lech = 0.87f + 0.1f * ((hinh * 29) % 5 - 2) / 2f;
            float cs = Mathf.Cos(lech), sn = Mathf.Sin(lech);
            BongPut(buf, g, c, new Vector2(nguoc.x * cs - nguoc.y * sn, nguoc.x * sn + nguoc.y * cs), sz * 0.82f, hinh);
            BongPut(buf, g, c, new Vector2(nguoc.x * cs + nguoc.y * sn, -nguoc.x * sn + nguoc.y * cs), sz * 0.74f, hinh + 1);
        }

        // điểm chạm của tia: MẶT TRƯỚC thân đối thủ (đầu tia tới đây là chạm; bản cũ dừng giữa thân hoặc xuyên qua tâm thân)
        static Vector2 ChamThan(Vector2 src, Vector2 foeBody, float tH) => foeBody - Unit(foeBody - src) * (0.16f * tH);

        // TIA NĂNG LƯỢNG bộ Mộc (Lộc Phong, Giác Mộc). src: gốc tia; dst: điểm chạm (ChamThan); travel: giây đầu tia tới dst (= giờ trúng hàm gọi
        // trả về); dur: giây từ lúc nhả tới lúc tia bắt đầu tắt ở ngọn; hw0: nửa bề dày; manh: cỡ bông va chạm (mana 1, chiêu cuối 1,4); datY: mặt
        // đất dưới đối thủ (bụi bốc), NaN thì thôi; mieng: cỡ bông ở gốc tia (0: không).
        // - Thân: mảng liền 5 lớp (mực, đậm sát viền, giữa, vàng chanh, lõi kem rộng), mép gợn chạy dọc theo dòng, đầu tia tròn; vệt kem chảy dọc
        //   trong thân; lá xoắn quanh thân (nửa sau vẽ sau tướng).
        // - Chỗ chạm: chớp, BÔNG VA CHẠM đổi dáng mỗi 2 khung, toé ngược về phía con bắn; vòng va chạm mỗi 0,12 s; tia vụn + mẩu lá toé theo cụm;
        //   đối thủ giật từng nhịp (DanhTrung) và màn rung nhẹ; bụi bốc dưới chân.
        // - Tắt (bản cũ cắt phụt / cả thân tia trượt vào đối thủ như khúc gỗ): thân tia thon dần từ gốc tới ngọn rồi vỡ thành mảnh năng lượng rơi
        //   lả tả; bông va chạm co lại sau cùng.
        void TiaMoc(Vector2 src, Vector2 dst, float travel, float dur, float hw0, float tH, float manh = 1, float datY = float.NaN, float mieng = 0,
            int group = Front)
        {
            var dd = dst - src;
            float dist = Mathf.Max(1, dd.magnitude);
            var u = dd / dist;
            var nrm = new Vector2(-u.y, u.x);
            travel = Mathf.Max(0.02f, travel);
            float tTat = Mathf.Max(travel + 0.1f, dur - 0.18f);
            const float Lan = 0.14f, Mat = 0.08f; // sóng thon chạy từ gốc tới ngọn trong Lan giây; mỗi điểm mất trong Mat giây
            float tHet = tTat + Lan + Mat;         // ngọn tia mất hẳn
            var w = W;
            var core = new P { pos = src, life = tHet + 0.02f, group = group, stops = w };
            core.draw = (q, k, buf) =>
            {
                float a = q.age;
                float head = dist * Mathf.Clamp01(a / travel);
                if (head < 4) return;
                int n = Mathf.Max(3, Mathf.CeilToInt(head / 14) + 1);
                float mo = Mathf.Min(1, a / 0.05f * 0.7f + 0.3f); // bật mở nhanh
                float bt = 1 + 0.07f * Mathf.Sin(a * 38);         // đập
                for (int li = 0; li < 5; li++)
                {
                    float wf = li < 2 ? 1 : li == 2 ? 0.78f : li == 3 ? 0.56f : 0.28f, grow = li == 0 ? 2.6f : 0;
                    int a0 = mp.Count;
                    for (int pass = 0; pass < 2; pass++)
                        for (int i = 0; i < n; i++)
                        {
                            float x = head * i / (n - 1);
                            float f = x / dist;
                            float tat = 1 - SmoothStep(tTat + Lan * f, tTat + Lan * f + Mat, a);
                            float hw = hw0 * mo * bt * tat * (1 + 0.1f * Mathf.Sin(x * 0.06f - a * 36)) * Mathf.Min(1, x / (2.2f * hw0) + 0.55f);
                            float dx = head - x;
                            if (dx < hw0) hw *= Mathf.Sqrt(Mathf.Max(0, dx / hw0 * (2 - dx / hw0))); // đầu tia tròn
                            var c = src + u * x + nrm * (1.2f * Mathf.Sin(x * 0.04f - a * 24));
                            mp.Add(c + nrm * ((pass == 0 ? 1 : -1) * (hw * wf + grow * Mathf.Clamp01(hw * 0.5f))));
                        }
                    MRibbon(q.group, 9 + li * 0.1f, a0, a0 + n, n, li == 0 ? Ink : li == 3 ? MocChanh : li == 4 ? MocKem : q.stops[li]);
                }
            };
            Add(core);
            // đầu tia lúc đang lao: búp toé chĩa về trước
            var bup = new P { pos = src, life = travel + 0.02f, group = group, sz = hw0 * 3.4f, seed = rng.Next(4) };
            bup.draw = (q, k, buf) => BongPut(buf, q.group, src + u * (dist * Mathf.Clamp01(q.age / travel)), u, q.sz * (0.85f + 0.15f * Mathf.Sin(q.age * 60)),
                q.seed + (int)(q.age * 15));
            Add(bup);
            // bông ở gốc tia (miệng, đỉnh sừng, quả tim): chập chờn suốt lúc tia chảy
            if (mieng > 1)
            {
                var gb = new P { pos = src, life = tTat + Lan * 0.3f, group = group, sz = mieng, seed = rng.Next(4) };
                gb.draw = (q, k, buf) => BongPut(buf, q.group, q.pos, u, q.sz * (0.9f + 0.1f * Mathf.Sin(q.age * 50)) * (1 - SmoothStep(0.8f, 1, k)),
                    q.seed + (int)(q.age * 15));
                Add(gb);
            }
            // vệt kem chảy dọc thân tia
            float SP = Mathf.Max(900, dist / travel);
            Every(travel, tTat - 0.04f, 22, x => // sinh từ lúc đầu tia đã chạm: vệt chạy nhanh hơn đầu tia, sinh sớm thì vượt ra trước mũi tia
            {
                var p = new P
                {
                    pos = src + nrm * U(-0.45f, 0.45f) * hw0, vel = u * SP * U(1.1f, 1.4f), group = group, sz = hw0 * U(0.26f, 0.4f),
                    col = U(0, 1) < 0.6f ? MocKem : MocChanh, seed = rng.Next(4)
                };
                p.life = dist / p.vel.magnitude;
                p.draw = (q, k, buf) => VetPut(buf, q.group, 41, false, q.col, q.pos, u, q.sz * 5.5f, q.sz, Mathf.Min(1, k * 6) * (1 - SmoothStep(0.85f, 1, k)), q.seed);
                Add(p);
            });
            // lá xoắn quanh thân tia: nửa trước vẽ trước, nửa sau vẽ sau tướng
            Every(travel * 0.6f, tTat - 0.04f, 12, x =>
            {
                float v = SP * U(0.7f, 0.85f);
                var q = Leaf(src, u * v, dist / v, U(3.6f, 5.2f), 0, 0, group);
                q.R0 = hw0 * U(1.25f, 1.7f);
                q.R1 = v;
                q.upd = (z, dt, s) =>
                {
                    float ga = z.age * 16 + z.ph;
                    var np = src + u * (z.R1 * z.age) + nrm * (z.R0 * Mathf.Sin(ga));
                    z.vel = (np - z.pos) / Mathf.Max(dt, 1e-5f);
                    z.group = Mathf.Cos(ga) >= 0 ? Front : Back;
                };
            });
            // chỗ chạm: chớp + đối thủ giật
            At(travel, () =>
            {
                Chop(dst, 0.4f * tH * manh, 0.08f);
                Shake?.Invoke(0.3f * manh);
                DanhTrung?.Invoke(dst, 0.7f);
                TiaVunCum(dst, -u, 1.2f, 5, 520 * manh, 4.4f);
            });
            var bong = new P { pos = dst, life = tHet - travel, group = group, sz = (0.36f + 0.12f * manh) * tH, seed = rng.Next(4) };
            bong.draw = (q, k, buf) =>
            {
                float t = q.age;
                float g = t < 0.05f ? 0.5f + 0.7f * EaseOut(t / 0.05f) : t < 0.1f ? 1.2f - 0.2f * (t - 0.05f) / 0.05f : 1; // bật quá cỡ rồi về
                g *= (1 - SmoothStep(q.life - 0.12f, q.life, t)) * (0.9f + 0.1f * Mathf.Sin(t * 70));
                BongVa(buf, q.group, q.pos, -u, q.sz * g, q.seed + (int)(t * 15));
            };
            At(travel, () => Add(bong));
            float tNgon = tTat + Lan; // ngọn tia bắt đầu tắt
            int nv = Mathf.Max(1, Mathf.FloorToInt((tNgon - travel) / 0.12f));
            for (int i = 0; i < nv; i++)
                At(travel + 0.06f + 0.12f * i, () =>
                {
                    VongVa(dst, 0.05f * tH, (0.24f + 0.06f * manh) * tH, 0.18f, MocKem, group);
                    DanhTrung?.Invoke(dst, 0.3f);
                    Shake?.Invoke(0.1f * manh);
                });
            // toé ngược theo cụm: tia vụn + mẩu lá
            Every(travel, tNgon, 11 * manh, x =>
            {
                TiaVunCum(dst + nrm * U(-0.5f, 0.5f) * hw0, -u, 1.3f, 3, U(300, 520) * manh, U(3, 4.6f), U(0, 1) < 0.7f ? group : Back, MocChanh, w[3]);
                if (U(0, 1) < 0.5f)
                    Leaf(dst + U2(-6, 6), Unit(-u + nrm * U(-1.2f, 1.2f)) * U(160, 320) + new Vector2(0, -U(40, 120)), U(0.35f, 0.55f), U(3f, 4.8f), 640, 2f,
                        U(0, 1) < 0.5f ? Front : Back);
            });
            if (!float.IsNaN(datY))
                Every(travel, tNgon, 3, x =>
                    BuiCum(new Vector2(dst.x + U(-0.25f, 0.25f) * tH, datY + U(-4, 2)), new Vector2(U(-60, 60), -U(20, 50)), U(0.08f, 0.12f) * tH, 0, Back));
            // tia tắt: vỡ thành mảnh năng lượng rơi lả tả theo sóng thon (gốc trước, ngọn sau)
            for (int j = 0; j < 9; j++)
            {
                float f = (j + U(0.2f, 0.8f)) / 9;
                int jj = j;
                At(tTat + Lan * f + Mat * 0.4f, () =>
                {
                    var at = src + u * dist * f + nrm * U(-0.4f, 0.4f) * hw0;
                    float sd = U(0, 1) < 0.5f ? -1 : 1;
                    var p = new P
                    {
                        pos = at, vel = nrm * sd * U(50, 130) + u * U(-40, 60) + new Vector2(0, -U(20, 80)), life = U(0.3f, 0.48f), drag = 2.4f,
                        acc = new Vector2(0, 380), sz = hw0 * U(0.5f, 0.85f), spin = U(-400, 400), ang = VelAng(u), group = group,
                        col = (jj & 1) == 0 ? MocChanh : w[3]
                    };
                    p.draw = DrawMangVo;
                    Add(p);
                    if (jj % 3 == 1) LaRoi(at, new Vector2(U(-40, 40), -U(20, 60)), U(0.5f, 0.8f), U(3.5f, 5f), U(0, 1) < 0.5f ? Front : Back);
                });
            }
        }

        // LƯỠI LIỀM mảng liền: lưng cong về phía d (đơn vị), tâm vòng ở c, bán kính R, dày giữa day, thuôn nhọn hai đầu, mở góc span (radian).
        // Lớp ngoài màu c1 có viền mực ink; lớp trong c2 mỏng hơn, sát lưng; squash < 1 ép dẹt theo chiều đứng (nằm trên đất). Dùng cho sóng
        // âm, sóng đất, lưỡi liềm của vụ nổ.
        void MLiem(int g, float layer, Vector2 c, Vector2 d, float R, float day, float span, Color c1, Color c2, float alpha = 1, float ink = 2.4f,
            float squash = 1)
        {
            if (R < 2 || day < 0.8f || alpha < 0.03f) return;
            var n = new Vector2(-d.y, d.x);
            const int m = 9;
            for (int lop = 0; lop < 2; lop++)
            {
                float dl = lop == 0 ? day : day * 0.46f, R2 = lop == 0 ? R : R - day * 0.1f;
                int a0 = mp.Count;
                for (int i = 0; i < m; i++) // lưng (cung ngoài) đi xuôi
                {
                    float th = span * (i / (m - 1f) - 0.5f);
                    var v = d * Mathf.Cos(th) + n * Mathf.Sin(th);
                    mp.Add(c + new Vector2(v.x, v.y * squash) * R2);
                }
                for (int i = m - 2; i >= 1; i--) // bụng (cung trong) đi ngược, dày nhất ở giữa
                {
                    float u = i / (m - 1f), th = span * (u - 0.5f);
                    var v = d * Mathf.Cos(th) + n * Mathf.Sin(th);
                    mp.Add(c + new Vector2(v.x, v.y * squash) * (R2 - dl * Mathf.Pow(Mathf.Sin(Mathf.PI * u), 0.75f)));
                }
                int cnt = mp.Count - a0;
                if (lop == 0) MSolid(g, layer, a0, cnt, c1, alpha, ink);
                else MFill(g, layer + 0.01f, a0, cnt, c2, alpha, true);
            }
        }

        // MÚI NĂNG LƯỢNG của vụ nổ cầu: bung đủ cỡ ngay (0,05 s), giữ, rồi teo thành đốm trong lúc trôi ra và bay lên (mẫu Kingdom Rush 5:
        // khối → múi tách → đốm). Ảnh kr_luakhoi (khối phồng nhiều múi); chưa có thì cụm tròn chồng lớp.
        P MuiNang(Vector2 pos, Vector2 vel, float r, float life, int group = Back)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = 3, acc = new Vector2(0, -50), sz = r, group = group, seed = rng.Next(4), ang = U(0, 360),
                spin = U(-60, 60), stops = W
            };
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                float g = t < 0.05f ? 0.6f + 0.4f * EaseOut(t / 0.05f) : 1 - 0.85f * SmoothStep(0.3f, 1, k);
                float r2 = q.sz * g;
                if (r2 < 1) return;
                float lo = 1 - SmoothStep(0.2f, 0.55f, k); // lõi kem nguội trước, rồi tới chanh
                var w = q.stops;
                int i = q.seed & 3, gr = q.group;
                var kl = S("kr_luakhoi_" + i);
                if (kl != null)
                {
                    Put(buf, gr, 25, S("kr_luakhois_" + i) ?? kl, Ink, q.pos, 2.2f * r2 + 5, 1, q.ang);
                    Put(buf, gr, 25.2f, kl, w[2], q.pos, 2.2f * r2, 1, q.ang);
                }
                else
                {
                    Put(buf, gr, 25, S("solid_" + i), Ink, q.pos, 2 * r2 + 5, 1, q.ang);
                    Put(buf, gr, 25.2f, S("blob_" + i), w[2], q.pos, 2 * r2, 1, q.ang);
                }
                float rc = r2 * (0.5f + 0.3f * lo);
                Put(buf, gr, 25.4f, S("blob_" + ((i + 1) & 3)), Color.Lerp(w[3], MocChanh, lo), q.pos + new Vector2(-0.1f, -0.16f) * r2, 2 * rc, 1, q.ang);
                if (lo > 0.05f) Put(buf, gr, 25.6f, S("blob_" + ((i + 2) & 3)), MocKem, q.pos + new Vector2(-0.14f, -0.22f) * r2, 1.1f * r2 * lo, 1, q.ang);
            };
            return Add(p);
        }

        // lưỡi liềm lá của vụ nổ: cong ra ngoài, cắm quanh khối, bật nhanh rồi teo (ảnh kr_liem lưng ở +x; chưa có thì mảng liền)
        P Liem(Vector2 pos, Vector2 d, float R, float life, int group = Front)
        {
            var p = new P { pos = pos, aim = Unit(d), life = life, sz = R, group = group, seed = rng.Next(4), vel = Unit(d) * U(60, 120), drag = 4, stops = W };
            p.draw = (q, k, buf) =>
            {
                float g = k < 0.2f ? 0.6f + 0.4f * EaseOut(k / 0.2f) : 1 - 0.8f * SmoothStep(0.35f, 1, k);
                float R2 = q.sz * g;
                if (R2 < 2) return;
                var w = q.stops;
                var kl = S("kr_liem_" + (q.seed & 3));
                if (kl != null)
                {
                    float ang = VelAng(q.aim);
                    Put(buf, q.group, 34, S("kr_liems_" + (q.seed & 3)) ?? kl, Ink, q.pos, R2 + 5, 1, ang);
                    Put(buf, q.group, 34.2f, kl, k < 0.4f ? MocChanh : w[3], q.pos, R2, 1, ang);
                    return;
                }
                MLiem(q.group, 34, q.pos - q.aim * (R2 * 0.6f), q.aim, R2 * 0.6f, R2 * 0.26f * (1 - 0.4f * k), 1.9f, k < 0.4f ? MocChanh : w[3], MocKem, 1, 2.2f);
            };
            return Add(p);
        }

        // nén cầu 1–2 khung ngay trước lúc nhả rồi bật to (đi kèm chớp): nhân vào bán kính; t, tNha cùng một mốc giờ
        static float NenNha(float t, float tNha) =>
            t < tNha - 0.07f || t > tNha + 0.07f ? 1 : t < tNha ? 1 - 0.3f * SmoothStep(tNha - 0.07f, tNha - 0.025f, t) : 1.25f - 0.25f * (t - tNha) / 0.07f;

        // NỔ CẦU NĂNG LƯỢNG (mẫu Kingdom Rush 5 explosion_KR5_big; không che con bị trúng): chớp 2 khung ở trước → khối năng lượng nhiều múi bung
        // ngay ở SAU thân đối thủ (ôm viền thân) → múi tách ra trôi, teo thành đốm; lưỡi liềm lá cong ra ngoài rồi teo; vành lá + tia vụn văng;
        // cụm phấn và cụm bụi tách dần bay lên; hai vòng cung dẹt đứt đoạn trên đất; vết trên đất giữ 1 s rồi mờ; lá rơi lượn.
        void NoCau(Vector2 c, Vector2 foeFeet, float tH, float sc)
        {
            float s = Mathf.Min(sc, 1.6f);
            Chop(c, 0.46f * tH * Mathf.Min(1.3f, sc), 0.08f);
            DanhTrung?.Invoke(c, 1);
            for (int i = 0; i < 5; i++)
            {
                float a = 6.28f * (i + U(0.1f, 0.9f)) / 5;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.85f - 0.2f);
                MuiNang(c + d * 0.14f * tH * s, d * U(70, 150) * s + new Vector2(0, -30), U(0.14f, 0.2f) * tH * s, U(0.42f, 0.62f), Back);
            }
            for (int i = 0; i < 5; i++)
            {
                float a = 6.28f * (i + U(0.15f, 0.85f)) / 5;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.9f);
                Liem(c + d * 0.24f * tH * s, d, U(0.16f, 0.22f) * tH * s, U(0.22f, 0.32f), d.y > 0.3f ? Front : Back);
            }
            int n = Mathf.RoundToInt(7 * s);
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / n;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                Leaf(c + d * U(6, 14), d * U(200, 420) * s, U(0.5f, 0.8f), U(3.6f, 6f), 620, 2.2f, (i & 1) == 0 ? Front : Back);
            }
            TiaVunCum(c, new Vector2(-1, -0.7f), 0.9f, 3, 460 * s, 4f);
            TiaVunCum(c, new Vector2(1, -0.7f), 0.9f, 3, 460 * s, 4f);
            for (int i = 0; i < 2; i++)
                BuiCum(c + new Vector2(U(-0.3f, 0.3f), U(-0.35f, 0.05f)) * tH * s, new Vector2(U(-70, 70), -U(40, 90)), U(0.11f, 0.15f) * tH * s, 0, Back, CumPhan);
            // khung vẽ sẵn (2026-11-19): bụi dưới chân là hai cụm khói nhuộm đất + một cụm giữa (thay ba cụm BuiCum); phấn lá giữ hạt cũ
            if (!MocBuiHaiBen(foeFeet, 0.14f * tH * s, 0.3f * tH, 130, true))
                for (int i = 0; i < 3; i++)
                {
                    float sd = i == 2 ? 0 : i == 0 ? -1 : 1;
                    BuiCum(foeFeet + new Vector2(sd * U(0.12f, 0.42f) * tH, U(-6, 2)), new Vector2(sd * U(80, 170), -U(15, 45)), U(0.11f, 0.15f) * tH * s, 0, Back);
                }
            CungDat(foeFeet + new Vector2(0, 2), 0.12f * tH, 0.8f * tH * s, 0.42f, MocChanh, 0.09f * tH * s);
            var w2 = W[2];
            At(0.08f, () => CungDat(foeFeet + new Vector2(0, 2), 0.08f * tH, 0.58f * tH * s, 0.42f, w2, 0.06f * tH * s, 5));
            VetDat(foeFeet + new Vector2(0, 3), 0.5f * tH * s, 1f);
            Every(0.12f, 0.6f, 22 * s, x =>
                LaRoi(c + new Vector2(U(-0.55f, 0.55f) * tH, -U(0.25f, 0.8f) * tH), new Vector2(U(-40, 40), U(10, 50)), U(0.6f, 0.9f), U(3.6f, 5.6f),
                    U(0, 1) < 0.5f ? Back : Front));
        }

        // ================= LÁ =================
        public const float LaDur = 0.9f; // chiêu phun lá: luồng lá chảy chừng này giây kể từ lúc nhả (clip cast giữ há mồm 0,94 s)

        Sprite LeafS(int i, bool solid) => S((solid ? "leafs_" : "leaf_") + i) ?? S((solid ? "drops_" : "drop_") + i);

        // lá: xoay theo p.ang (độ), lật nghiêng theo tuổi (bề ngang co giãn), co nhỏ ở cuối đời
        void DrawLeaf(P p, float k, List<Item> buf)
        {
            float s = 2.9f * p.sz * (1 - SmoothStep(0.8f, 1, k));
            if (s < 1) return;
            var w = p.stops ?? W;
            float st = 0.4f + 0.6f * Mathf.Abs(Mathf.Cos(p.age * p.vy + p.ph));
            int i = p.seed & 3;
            Put(buf, p.group, 40, LeafS(i, true), Ink, p.pos, s + 4, (s * st + 4) / (s + 4), p.ang);
            Put(buf, p.group, 40.3f, LeafS(i, false), (p.seed & 4) != 0 ? w[2] : Color.Lerp(w[2], w[3], 0.55f), p.pos, s, st, p.ang); // lá tươi: lục giữa và lục tươi (bản cũ lục đậm, trông tối)
        }

        public P Leaf(Vector2 pos, Vector2 vel, float life, float r, float grav = 0, float drag = 0, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = drag, acc = new Vector2(0, grav), seed = rng.Next(8), sz = r, group = group,
                ang = TipAngle(Unit(vel)), spin = U(-520, 520), spinDrag = 0.6f, ph = U(0, 6.28f), vy = U(9, 15), stops = W
            };
            p.draw = DrawLeaf;
            return Add(p);
        }

        // lá vỡ lúc trúng (mẫu Kingdom Rush 5, không che con bị trúng): chớp nhỏ 2 khung ở trước; khối toé màu lá ôm SAU thân; vành lá rải đều
        // góc văng ra rồi rơi; tia vụn theo cụm; cụm phấn sau lưng tách dần; vòng cung dẹt đứt đoạn dưới chân. Bản cũ: chớp to ở trước che mặt,
        // bọt trắng kiểu nước, vòng mảnh.
        void LaNo(Vector2 c, Vector2 foeFeet, float tH, float sc)
        {
            float s = Mathf.Min(sc, 1.5f);
            Chop(c, 0.36f * tH * Mathf.Min(1.25f, sc), 0.07f);
            BurstFlash(c, 0.52f * tH * s, Back, 0.18f);
            int n = Mathf.RoundToInt(9 * Mathf.Min(sc, 1.5f));
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / n; // rải đều góc (ngẫu nhiên hẳn thì dồn cục)
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.25f);
                Leaf(c + d * U(4, 12), d * U(170, 360) * sc, U(0.55f, 0.85f), U(3.6f, 6.4f), 620, 2.2f, (i & 1) == 0 ? Front : Back);
            }
            TiaVunCum(c, new Vector2(-1, -0.6f), 0.9f, 3, 380 * s, 3.6f);
            TiaVunCum(c, new Vector2(1, -0.6f), 0.9f, 3, 380 * s, 3.6f);
            int nc = sc > 1.2f ? 3 : 2;
            for (int i = 0; i < nc; i++)
                BuiCum(c + new Vector2(U(-0.3f, 0.3f), U(-0.25f, 0.1f)) * tH * s, new Vector2(U(-60, 60), -U(30, 70)), U(0.09f, 0.13f) * tH * s, 0, Back, CumPhan);
            CungDat(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.6f * tH * s, 0.45f, W[2], 0.07f * tH * s);
        }

        // PHUN LÁ: lúc hít (trước khung nhả) lá nhỏ và vệt gió bị hút xoắn vào mồm; từ khung nhả một luồng lá dày bắn tới thân đối thủ, mỗi lá
        // tự lái nhẹ về một điểm trong thân, lượn và lật; ở mặt trước thân đối thủ một bông va chạm toé liên tục, lá chạm thì vỡ thành mẩu lá bật
        // ngược + tia vụn theo cụm; hết luồng nổ một chùm lá.
        public float NLa(Vector2 mouth, Vector2 target, Vector2 foeFeet, float tH, float lead, float dur = LaDur)
        {
            MocSang();
            var dd = Unit(target - mouth);
            var nrm = new Vector2(-dd.y, dd.x);
            float dist = (target - mouth).magnitude;
            float s0 = Mathf.Max(0.05f, lead);
            const float V = 780;
            float fly = dist / V;
            if (s0 > 0.16f) GatherLa(t => mouth, 0, s0 - 0.06f, 72, 30);
            Every(s0, s0 + dur, x => 80 * (x < 0.14f ? 1.5f : x > 0.86f ? 0.6f : 1), x => // "bắn ra NHIỀU lá": bản đầu 40 lá/giây, lá nhỏ, nhìn thưa
            {
                float spd = V * U(0.86f, 1.14f);
                float a = U(-0.16f, 0.16f);
                var v = (dd * Mathf.Cos(a) + nrm * Mathf.Sin(a)) * spd;
                var q = Leaf(mouth + nrm * U(-8, 8), v, dist / spd + 0.3f, U(6f, 10.5f));
                q.aim = target + new Vector2(U(-0.24f, 0.24f), U(-0.3f, 0.3f)) * tH;
                q.R0 = spd;
                q.upd = (z, dt, s) =>
                {
                    var to = z.aim - z.pos;
                    float d = to.magnitude;
                    var want = to / Mathf.Max(d, 1e-5f) * z.R0 + nrm * (Mathf.Sin(z.age * 13 + z.ph) * 120);
                    z.vel += (want - z.vel) * Mathf.Min(1, 6 * dt);
                    if (d < 15)
                    {
                        z.hit = true;
                        z.dead = true;
                    }
                };
                q.onDeath = (z, s) =>
                {
                    if (!z.hit) return;
                    if (s.U(0, 1) < 0.4f) s.Leaf(z.pos, -dd * s.U(60, 150) + s.U2(-120, 120), s.U(0.3f, 0.5f), s.U(3f, 4.6f), 700, 1.5f);
                };
            });
            // phấn lá bay ra ở mồm theo luồng (bản cũ: bọt trắng kiểu nước)
            Every(s0, s0 + dur, 7, x => BuiCum(mouth + U2(-5, 5) + dd * 10, dd * U(70, 120) + U2(-25, 25), U(4, 6), 0, Front, CumPhan, false));
            // chỗ chạm: bông va chạm toé ngược liên tục, tia vụn theo cụm, đối thủ giật từng nhịp
            var cham = ChamThan(mouth, target, tH);
            float tHit = s0 + fly;
            var bong = new P { pos = cham, life = dur + 0.06f, group = Front, sz = 0.36f * tH, seed = rng.Next(4) };
            bong.draw = (q, k, buf) =>
            {
                float t = q.age;
                float g = t < 0.05f ? 0.5f + 0.6f * EaseOut(t / 0.05f) : 1.1f - 0.1f * Mathf.Min(1, (t - 0.05f) / 0.05f);
                g *= (1 - SmoothStep(q.life - 0.12f, q.life, t)) * (0.88f + 0.12f * Mathf.Sin(t * 60));
                BongVa(buf, q.group, q.pos, -dd, q.sz * g, q.seed + (int)(t * 15));
            };
            At(tHit, () =>
            {
                Add(bong);
                Chop(cham, 0.32f * tH, 0.07f);
            });
            Every(tHit, tHit + dur, 9, x => TiaVunCum(cham + nrm * U(-8, 8), -dd, 1.3f, 3, U(260, 420), U(2.8f, 4f), U(0, 1) < 0.7f ? Front : Back, MocChanh, W[3]));
            Every(tHit, tHit + dur, 7, x =>
            {
                Shake?.Invoke(0.1f);
                DanhTrung?.Invoke(cham, 0.25f);
            });
            At(tHit + dur, () =>
            {
                Shake?.Invoke(0.3f);
                LaNo(target, foeFeet, tH, 0.8f);
            });
            return tHit;
        }

        // cú HÚC BỤNG của chiêu lao tới: gọi đúng khung trúng; lá vỡ tung quanh chỗ chạm, sao văng (họa tiết của chủ đề), cụm bụi dưới chân
        public float NLaVa(Vector2 foeBody, Vector2 foeFeet, float tH)
        {
            MocSang();
            Shake?.Invoke(0.6f);
            LaNo(foeBody, foeFeet, tH, 1.3f);
            WExtra(foeBody, 6, 320);
            if (!MocBuiHaiBen(foeFeet, 0.13f * tH, 0.24f * tH, 110)) // khung vẽ sẵn (2026-11-19): hai cụm khói nhuộm đất thay bốn cụm BuiCum
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    BuiCum(foeFeet + new Vector2(sd * U(0.1f, 0.34f) * tH, U(-6, 2)), new Vector2(sd * U(60, 140), -U(15, 40)), U(0.1f, 0.14f) * tH, 0, Back);
                }
            VetDat(foeFeet + new Vector2(0, 3), 0.36f * tH, 0.9f);
            return 0;
        }

        // ================= GAI (2026-11-12, Cầu Gai ở suất tien_la: "gồng rồi phóng dài các gai cơ thể dài hẳn ra đâm tứ tung") =================
        // Rig tự làm gai trên thân dài ra (clip cast); lớp này lo phần tới được đối thủ: gai trồi từ đất chạy tới chân nó rồi đâm tua tủa.
        // Ảnh hat_thorn_<i> (một gai), hat_tuft_<i> (cụm gai trồi), hat_shard_<i> (dăm gai): ArtGen/Spine/gai.py đặt hình theo một quy ước:
        // hình chiếm tối đa 92% khung vuông, canh giữa ngang, ĐÁY hình (thorn, tuft) ở 96% chiều cao khung.
        const float GaiLap = 0.92f, GaiDay = 0.46f; // GaiDay: tâm khung cách đáy hình 0,46 khung
        static readonly Color GaiC = C(255, 238, 164), GaiC2 = C(250, 218, 132); // kem vàng ấm như gai của tướng (ảnh hạt xám vân chì nhân vào còn xỉn đi; kem nhạt thì ra xám be)
        const float GaiInk = 9; // viền mực dày như viền gai của tướng: bản đầu 5, gai kem lẫn vào nền cát

        public bool HasGai => S("thorn_0") && S("tuft_0") && S("shard_0");

        Sprite GaiS(string ten, int i, bool solid) => S(ten + (solid ? "s_" : "_") + i);

        void DrawShard(P p, float k, List<Item> buf)
        {
            float s = 2.6f * p.sz * (1 - SmoothStep(0.75f, 1, k));
            if (s < 1) return;
            int i = p.seed & 3;
            Put(buf, p.group, 41, GaiS("shard", i, true), Ink, p.pos, s + 3.5f, 1, p.ang);
            Put(buf, p.group, 41.3f, GaiS("shard", i, false), p.col, p.pos, s, 1, p.ang);
        }

        // dăm gai: mảnh gãy xoay, rơi có trọng lực
        public P Shard(Vector2 pos, Vector2 vel, float life, float r, float grav = 760, float drag = 1.4f, int group = Front)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = drag, acc = new Vector2(0, grav), seed = rng.Next(8), sz = r, group = group,
                ang = U(0, 360), spin = U(-760, 760), spinDrag = 0.5f
            };
            p.col = (p.seed & 4) != 0 ? GaiC2 : GaiC;
            p.draw = DrawShard;
            return Add(p);
        }

        // nhịp trồi: bật quá cỡ trong 0,07 s, về cỡ, đứng, rồi rút xuống ở 28% cuối đời
        static float GaiGrow(float k, float life)
        {
            float t = k * life;
            if (t < 0.07f) return 1.22f * EaseOut(t / 0.07f);
            if (t < 0.14f) return 1.22f - 0.22f * (t - 0.07f) / 0.07f;
            return 1 - SmoothStep(0.72f, 1, k);
        }

        // cụm gai trồi từ đất: đáy bám đất, wd là bề rộng khung hình trên sân
        P Tuft(Vector2 feet, float wd, float life = 0.6f, int group = Front, int seed = -1)
        {
            var p = new P { pos = feet, life = life, group = group, seed = seed >= 0 ? seed : rng.Next(4), wd = wd, col = GaiC };
            p.draw = (q, k, buf) =>
            {
                float h = q.wd * GaiGrow(k, q.life);
                if (h < 3) return;
                var c = q.pos - new Vector2(0, h * GaiDay);
                Put(buf, q.group, 36, GaiS("tuft", q.seed, true), Ink, c, h + GaiInk, (q.wd + GaiInk) / (h + GaiInk));
                Put(buf, q.group, 36.3f, GaiS("tuft", q.seed, false), q.col, c, h, q.wd / h);
            };
            return Add(p);
        }

        // một cái gai dài đâm lên từ đất theo hướng dir (đơn vị), dài len, mập thick (bề ngang so với bề dài của khung)
        P Spike(Vector2 at, Vector2 dir, float len, float life, int group, int seed, float thick = 0.5f)
        {
            var p = new P { pos = at, life = life, group = group, seed = seed & 3, wd = len / GaiLap, off = Unit(dir), hgt = thick, col = (seed & 4) != 0 ? GaiC2 : GaiC };
            p.draw = (q, k, buf) =>
            {
                float f = q.wd * GaiGrow(k, q.life);
                if (f < 4) return;
                var c = q.pos + q.off * (f * GaiDay);
                float ang = TipAngle(q.off);
                Put(buf, q.group, 35, GaiS("thorn", q.seed, true), Ink, c, f + GaiInk, (f * q.hgt + GaiInk) / (f + GaiInk), ang);
                Put(buf, q.group, 35.3f, GaiS("thorn", q.seed, false), q.col, c, f, q.hgt, ang);
            };
            return Add(p);
        }

        // gai gãy vụn: chớp nhỏ ở trước, khối toé sau thân, dăm gai văng toả rồi rơi, cụm bụi kem
        void GaiNo(Vector2 c, float tH, float sc, int n = 12)
        {
            Chop(c, 0.34f * tH * Mathf.Min(1.3f, sc), 0.07f);
            BurstFlash(c, 0.5f * tH * Mathf.Min(1.4f, sc), Back, 0.16f);
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / n; // rải đều góc
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                Shard(c + d * U(4, 12), d * U(190, 400) * sc, U(0.5f, 0.8f), U(3f, 5.2f));
            }
            for (int i = 0; i < 2; i++)
                BuiCum(c + new Vector2(U(-0.25f, 0.25f), U(-0.2f, 0.1f)) * tH, new Vector2(U(-60, 60), -U(30, 70)), U(0.09f, 0.12f) * tH * Mathf.Min(1.3f, sc), 0, Back,
                    CumPhan);
        }

        // GỒNG GAI: lúc gồng (trước khung nhả) dăm gai bị hút vào thân; khung nhả gai trên thân bật dài (rig), dăm gai văng tứ tung quanh
        // thân; gai trồi từ đất chạy thành hàng tới chân đối thủ, cụm sau to hơn cụm trước; tới nơi một cụm lớn bật lên sau lưng nó, gai
        // dài đâm chéo tua tủa (cao ở sau lưng, thấp ở trước cho khỏi che), dăm gai văng; gai đứng 0,5 s rồi rút xuống.
        public float NGai(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float s0 = Mathf.Max(0.05f, lead);
            var body = casterFeet - new Vector2(0, 0.5f * casterH);
            if (s0 > 0.16f)
                Every(0, s0 - 0.08f, x => 14 + 26 * x, x => // mật độ tăng dần tới lúc nhả; dăm bay xoắn vào thân, nhanh dần
                {
                    float a = U(0, 6.28f), R = U(0.5f, 0.9f) * casterH;
                    var q = Shard(body + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * R, Vector2.zero, 0.3f, U(2.2f, 3.6f), 0, 0);
                    q.ph = a;
                    q.R0 = R;
                    q.upd = (z, dt, s) =>
                    {
                        float kk = Mathf.Min(1, z.age / z.life);
                        float ga = z.ph + 1.8f * kk * kk, rr = z.R0 * (1 - kk * kk);
                        var np = body + new Vector2(Mathf.Cos(ga), Mathf.Sin(ga) * 0.8f) * rr;
                        z.vel = (np - z.pos) / Mathf.Max(dt, 1e-5f);
                    };
                });
            At(s0, () =>
            {
                Shake?.Invoke(0.22f);
                CungDat(casterFeet + new Vector2(0, 2), 0.2f * casterH, 0.8f * casterH, 0.42f, W[2], 0.08f * casterH);
                for (int i = 0; i < 10; i++)
                {
                    float a = 6.28f * (i + U(0, 0.8f)) / 10;
                    var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.2f);
                    Shard(body + d * 0.42f * casterH, d * U(260, 480), U(0.35f, 0.6f), U(2.8f, 4.6f));
                }
                if (!MocBuiHaiBen(casterFeet, 0.12f * casterH, 0.26f * casterH, 90)) // khung vẽ sẵn (2026-11-19): hai cụm khói nhuộm đất thay ba cụm BuiCum
                    for (int i = 0; i < 3; i++)
                    {
                        float sd = i == 1 ? 0 : i == 0 ? -1 : 1;
                        BuiCum(casterFeet + new Vector2(sd * U(0.2f, 0.32f) * casterH, U(-4, 2)), new Vector2(sd * U(60, 120), -U(15, 40)), U(0.1f, 0.13f) * casterH, 0, Back);
                    }
            });
            const int N = 4;
            const float Gap = 0.06f;
            var run = foeFeet - casterFeet;
            // khung vẽ sẵn (2026-11-19, người dùng chê "gai lá đâm lên xấu"): gai lá (gai_la) thay cụm gai Tuft / gai dài Spike. Đỉnh phóng của
            // từng cụm rơi đúng nhịp cụm cũ (gọi + 0,07 s), nên khung nứt đất hiện trước một chút; giờ trúng không đổi
            bool fb = HasFb("gai_la");
            for (int i0 = 0; i0 < N; i0++)
            {
                int i = i0;
                float tGoi = s0 + 0.05f + i * Gap;
                if (fb) // hàng gai so le: cụm chính lớn dần, cụm nhỏ chen giữa lệch sang bên kia, trễ nửa nhịp. Vẽ ở lớp TRƯỚC (người dùng xem trong
                        // game 2026-11-19: gai ở lớp sau bị thân che, không thấy rõ); hàng nằm giữa hai con nên không che mặt ai
                {
                    var at = casterFeet + run * (0.36f + 0.12f * i) + new Vector2(U(-6, 6), (i & 1) == 0 ? -4 : 4);
                    MocGaiFb(at, (0.5f + 0.1f * i) * tH, tGoi + 0.07f, 0.1f, Front, 35 + 0.01f * i, (i & 1) == 1);
                    if (i < N - 1)
                        MocGaiFb(casterFeet + run * (0.42f + 0.12f * i) + new Vector2(U(-6, 6), (i & 1) == 0 ? 6 : -6), (0.32f + 0.06f * i) * tH, tGoi + 0.1f, 0.06f, Front,
                            (i & 1) == 0 ? 35.05f : 34.9f, (i & 1) == 0); // cụm đứng thấp hơn trên màn (gần người xem) vẽ đè lên
                    At(tGoi, () =>
                    {
                        Shake?.Invoke(0.06f);
                        Shard(at + new Vector2(U(-8, 8), -6), new Vector2(U(-110, 110), -U(150, 260)), U(0.35f, 0.5f), U(2.6f, 4)); // dăm gai phụ đi kèm
                    });
                    continue;
                }
                At(tGoi, () =>
                {
                    var at = casterFeet + run * (0.36f + 0.12f * i) + new Vector2(U(-6, 6), U(-3, 3)); // bắt đầu ngoài thân con ra chiêu
                    Tuft(at, (0.44f + 0.09f * i) * tH, 0.5f);
                    Shake?.Invoke(0.06f);
                    for (int j = 0; j < 2; j++) Shard(at + new Vector2(U(-8, 8), -6), new Vector2(U(-110, 110), -U(150, 260)), U(0.35f, 0.5f), U(2.6f, 4));
                    BuiCum(at + new Vector2(U(-6, 6), 0), new Vector2(U(-40, 40), -U(20, 40)), (0.07f + 0.012f * i) * tH, 0, Back);
                });
            }
            float hit = s0 + 0.05f + N * Gap + 0.03f;
            // vòng gai lá quanh chân đối thủ (MocVongGai): bốn cụm cao so le sau lưng, to hơn để ló lên trên vai (đỉnh lệch nhau 0–0,08 s); lớp
            // trước ba cụm thấy rõ: hai cụm to hai bên + một cụm vừa chếch trước chân phía Cầu Gai (bản đầu: hai cụm 0,4 tH, gần như không thấy).
            // Giữ tới ~0,45 s sau trúng rồi gãy rụng lá ngay trong khung, nên bỏ đợt "gai rút" bằng dăm. start 4,5: khung nứt đất ngắn, hiện khi
            // hàng gai chạy gần tới nơi (sớm quá thì mất cảm giác gai chạy tới)
            if (fb)
                MocVongGai(foeFeet, tH, hit, 0.4f, casterFeet.x < foeFeet.x ? -1 : 1,
                    new[] { (-0.42f, 1.3f, 0f), (-0.12f, 1.5f, 0.03f), (0.2f, 1.42f, 0.055f), (0.46f, 1.25f, 0.08f) });
            At(hit, () =>
            {
                Shake?.Invoke(0.5f);
                DanhTrung?.Invoke(foeBody, 0.6f);
                if (!fb)
                {
                    Tuft(foeFeet + new Vector2(0, -3), 1.35f * tH, 0.74f, Back, 2 + rng.Next(2));
                    Tuft(foeFeet + new Vector2(-0.52f * tH, 6), 0.4f * tH, 0.66f, Front, 1); // hai cụm trước đứng hai bên, thấp: không che mặt con bị trúng
                    Tuft(foeFeet + new Vector2(0.52f * tH, 7), 0.4f * tH, 0.66f, Front, 1);
                }
                GaiNo(foeBody, tH, 1);
                WExtra(foeBody, 5, 300);
                CungDat(foeFeet + new Vector2(0, 2), 0.14f * tH, 0.66f * tH, 0.45f, W[2], 0.07f * tH);
                VetDat(foeFeet + new Vector2(0, 3), 0.42f * tH, 1f);
                if (!MocBuiHaiBen(foeFeet, 0.13f * tH, 0.3f * tH, 100)) // khung vẽ sẵn: hai cụm khói nhuộm đất thay bốn cụm BuiCum
                    for (int i = 0; i < 4; i++)
                    {
                        float sd = (i & 1) == 0 ? 1 : -1;
                        BuiCum(foeFeet + new Vector2(sd * U(0.12f, 0.38f) * tH, U(-6, 2)), new Vector2(sd * U(60, 140), -U(15, 45)), U(0.1f, 0.14f) * tH, 0, Back);
                    }
            });
            // gai dài đâm chéo lên: ba cái cao sau lưng, hai cái thấp phía trước (có khung vẽ sẵn thì chỉ còn nhịp rung + dăm gai văng theo)
            for (int j0 = 0; j0 < 5; j0++)
            {
                int j = j0;
                At(hit + 0.02f + j * 0.035f, () =>
                {
                    bool back = j < 3;
                    float x = back ? (j - 1) * 0.3f : (j == 3 ? -0.4f : 0.4f);
                    float tilt = x * (back ? 1.5f : -1.3f) + U(-0.08f, 0.08f); // sau lưng xoè ra ngoài, phía trước chĩa chéo vào trong
                    var d = new Vector2(Mathf.Sin(tilt), -Mathf.Cos(tilt));
                    var at = foeFeet + new Vector2(x * tH, back ? -2 : 7);
                    if (!fb) Spike(at, d, (back ? U(1.2f, 1.45f) : U(0.42f, 0.52f)) * tH, 0.62f - j * 0.02f, back ? Back : Front, j, back ? 0.42f : 0.55f);
                    Shake?.Invoke(0.12f);
                    for (int i = 0; i < 2; i++) Shard(at + d * 10, d * U(160, 300) + U2(-80, 80), U(0.35f, 0.55f), U(2.4f, 3.8f));
                });
            }
            if (!fb)
                At(hit + 0.5f, () => // gai rút: vụn rơi, bụi lún
                {
                    for (int i = 0; i < 6; i++)
                        Shard(foeFeet + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.1f, 0.8f) * tH), new Vector2(U(-50, 50), U(-30, 40)), U(0.4f, 0.6f), U(2.4f, 3.6f));
                    BuiCum(foeFeet + new Vector2(U(-0.2f, 0.2f) * tH, -2), new Vector2(U(-30, 30), -U(15, 35)), 0.12f * tH, 0, Back);
                });
            return hit;
        }

        // tướng đang ra chiêu có phải là id không (wth do UseTheme đặt theo tướng, MocSang có thể đã đổi sang bản tươi)
        bool ThemeLa(string id) => WThemes.TryGetValue(id, out var t) && (wth == t || (mocSang.TryGetValue(t, out var s) && wth == s));

        // CÂY QUẬT của người cây Long Vuốt (mana "n_gai_va", 2026-11-19; người dùng: "cây quật nhìn hơi nhẹ nhàng và hơi ít cây, chưa có impact").
        // Gọi đúng khung trúng (dây gai của rig quật xuống). Khung vẽ sẵn quat_dat (thân dây leo xoắn nện xuống, đất nứt, đá đất + lá văng, bụi;
        // neo chân): bốn cây so le quanh đối thủ, cây chính ở lớp TRƯỚC lệch một bên (bắt đầu ở khung đã gần nện xuống, đúng lúc trúng), cây phụ
        // trước bên kia, hai cây sau lưng (một cây cao ló lên trên vai); mỗi cây ngả RA NGOÀI (không quất ngang mặt đối thủ). Cây chính: rung 0,5 +
        // DanhTrung 1 (sân tự thêm khựng nhún + bông toé trắng); cây sau: rung 0,3 + DanhTrung 0,45. Mỗi gốc cây một cụm bụi đất + đá đất văng; hai
        // cụm gai lá bật quanh chân; dăm gai (GaiNo), cung đất, vết đất giữ. Hàm không biết con ra chiêu ở phía nào nên bên của cây chính bốc ngẫu nhiên.
        // Chưa nhập khung quat_dat thì bản cũ (NGaiVa).
        public float NQuatGai(Vector2 foeBody, Vector2 foeFeet, float tH)
        {
            MocSang();
            float s = U(0, 1) < 0.5f ? -1 : 1;
            var cay = new[] { (0.48f * s, 10f, 1.36f, 0f, Front), (-0.64f * s, 8f, 1.18f, 0.09f, Front), (-0.14f * s, -4f, 1.55f, 0.16f, Back), (0.78f * s, -2f, 1.1f, 0.23f, Back) };
            const float Sp = 1.35f, St = 2;
            float song = (24 - St) / (24 * Sp);
            for (int i = 0; i < cay.Length; i++)
            {
                var (ox, oy, hh, tre, nhom) = cay[i];
                int ii = i;
                At(tre, () =>
                {
                    var goc = foeFeet + new Vector2(ox * tH, oy);
                    Fb("quat_dat", goc, hh * tH, nhom, nhom == Front ? 37 + 0.01f * ii : 33, Sp, 0, ox > 0, null, 1, song, St, 0.22f);
                    Shake?.Invoke(ii == 0 ? 0.5f : 0.3f);
                    DanhTrung?.Invoke(foeBody, ii == 0 ? 1f : 0.45f);
                    if (MocKhoiFb(goc + new Vector2(0, -2), (ii == 0 ? 0.15f : 0.12f) * tH, new Vector2(Mathf.Sign(ox) * U(60, 130), -U(15, 35)), Back, 4, 1.35f) == null)
                        BuiCum(goc, new Vector2(Mathf.Sign(ox) * U(60, 130), -U(15, 35)), 0.12f * tH, 0, Back);
                    for (int j = 0; j < 3; j++)
                        DaVun(goc + new Vector2(U(-10, 10), -4), new Vector2(U(-200, 200), -U(240, 440)), U(0.45f, 0.7f), U(2.8f, 4.4f), nhom);
                });
            }
            Shake?.Invoke(0.2f);
            GaiNo(foeBody, tH, 1.2f, 12);
            WExtra(foeBody, 6, 320);
            if (HasFb("gai_la")) // hai cụm gai lá bật quanh chân: một cụm trước ở ngoài cùng phía cây phụ, một cụm sau lưng
            {
                MocGaiFb(foeFeet + new Vector2(-0.95f * s * tH, 9), 0.6f * tH, 0.06f, 0.2f, Front, 35.3f, s < 0, 1.35f, 4.5f);
                MocGaiFb(foeFeet + new Vector2(0.24f * s * tH, -5), 0.95f * tH, 0.12f, 0.2f, Back, 34, s > 0, 1.35f, 4.5f);
            }
            CungDat(foeFeet + new Vector2(0, 2), 0.16f * tH, 0.95f * tH, 0.45f, CungC, 0.1f * tH);
            VetDat(foeFeet + new Vector2(0, 3), 0.5f * tH, 1.1f);
            if (!MocBuiHaiBen(foeFeet, 0.15f * tH, 0.34f * tH, 140, true))
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    BuiCum(foeFeet + new Vector2(sd * U(0.12f, 0.38f) * tH, U(-6, 2)), new Vector2(sd * U(70, 150), -U(15, 45)), U(0.11f, 0.15f) * tH, 0, Back);
                }
            return 0;
        }

        // cú TÔNG của chiêu cuối "Lăn Gai" (quả cầu gai xoay lao vào): gọi đúng khung chạm; gai gãy văng tung, cụm gai bật lên dưới chân.
        // Mã n_gai_va cũng là chiêu mana của người cây Long Vuốt: có khung quat_dat thì sang NQuatGai (2026-11-19)
        public float NGaiVa(Vector2 foeBody, Vector2 foeFeet, float tH)
        {
            if (HasFb("quat_dat") && ThemeLa("long_vuot")) return NQuatGai(foeBody, foeFeet, tH);
            MocSang();
            Shake?.Invoke(0.7f);
            GaiNo(foeBody, tH, 1.4f, 18);
            WExtra(foeBody, 7, 340);
            // khung vẽ sẵn (2026-11-19): vòng gai lá (MocVongGai) gọi đúng khung chạm nên bỏ khung nứt đất. Sau lưng một cụm cao ló lên trên vai +
            // một cụm vừa; lớp trước hai cụm to hai bên chân (người dùng xem trong game: gai chỉ ở lớp sau thì bị thân che). Hàm này không biết
            // con ra chiêu ở phía nào nên bỏ cụm chếch trước. Không có khung thì cụm gai Tuft cũ
            if (HasFb("gai_la"))
                MocVongGai(foeFeet, tH, 0.05f, 0.24f, 0, new[] { (0.04f, 1.3f, 0f), (-0.36f, 0.95f, 0.05f) }, 0.92f, 2.5f);
            else Tuft(foeFeet + new Vector2(0, -3), 0.9f * tH, 0.5f, Back, 1);
            CungDat(foeFeet + new Vector2(0, 2), 0.14f * tH, 0.74f * tH, 0.45f, W[2], 0.08f * tH);
            VetDat(foeFeet + new Vector2(0, 3), 0.42f * tH, 1f);
            if (!MocBuiHaiBen(foeFeet, 0.14f * tH, 0.3f * tH, 120)) // khung vẽ sẵn: hai cụm khói nhuộm đất thay bốn cụm BuiCum
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    BuiCum(foeFeet + new Vector2(sd * U(0.12f, 0.38f) * tH, U(-6, 2)), new Vector2(sd * U(70, 150), -U(15, 45)), U(0.11f, 0.15f) * tH, 0, Back);
                }
            return 0;
        }
    }
}
