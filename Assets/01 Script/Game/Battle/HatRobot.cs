// Bộ ROBOT CỔ (2026-11-16, robot hủy diệt cổ đại, suất thiet_phu ải 40 đảo Kim; rig ArtGen/Spine/robot_co_rig.py trên rig gốc monster_3613):
// dạng 1 robot_co_1 (RC_DANG=non: robot con thép mới), dạng 2 robot_co_2 (robot cổ sắt gỉ); ghi chú ArtGen/Spine/inbox/robot_co_ghichu.md.
// Người dùng: đánh thường "giơ tay phải lên, tụ 1 quả cầu năng lượng kiểu dragonball rồi bắn, tay bị giật lại"; chiêu mana "đưa 2 tay lên trời,
// xoay lòng bàn tay liên tục, tụ 1 quả cầu năng lượng to hơn rồi ném xuống đầu đối thủ, impact lớn, nặng"; chiêu cuối "mở mặt ra có lõi tên lửa
// lục giác, phóng các tên lửa bay random theo đường cong bezier kiểu homing missile vào đối thủ, impact nặng, nổ lớn"; lúc ghép vào game "làm
// thêm các fx cần thiết vì tôi chưa thấy tên lửa nào".
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc: phát lúc clip BẮT ĐẦU, `lead` = giờ trúng của clip); mốc là giây clip của rig co theo
// lead; chỗ trên rig (ổ nắm đấm, cầu to giữa hai bàn tay, hai lòng bàn tay, tâm lõi, miệng 7 ống) là bảng đo ở HatRobotBang.cs (sinh bằng
// ArtGen/Spine/robot_co_do_hat.py: đổi clip hay tỉ lệ rig thì chạy lại).
// - n_robot_ban1 / n_robot_ban (đòn thường): hạt năng lượng bị hút vào ổ nắm đấm, cầu năng lượng vàng lớn dần có hai cung điện quay, lưỡi
//   năng lượng liếm quanh, đầy thì nháy vòng; bắn: chớp ở ổ, vòng, tia văng, hơi xì ở ổ lúc tay giật lùi; cầu bay có đuôi; trúng: chớp, nổ vàng.
// - n_robot_cau1 / n_robot_cau (chiêu mana): cầu to giữa hai bàn tay giơ cao, xoáy năng lượng ở hai lòng bàn tay (bàn tay xoay) và dải hạt
//   từ lòng bàn tay cuốn vào cầu, hạt hút từ xa, sỏi dưới chân bay lên, bụi xoáy, ba nhịp vòng nạp (nhịp cuối chớp + rung); vung đập: cầu vọt
//   lên rồi cắm xuống đỉnh đầu đối thủ; nổ rất lớn: chớp, nổ vàng, cột năng lượng phụt lên, hai vòng sóng đất, nứt đất, đá văng, bụi, khói.
// - n_robot_ten1 / n_robot_ten (chiêu cuối): giáp ngực mở xì hơi hai bên, lõi nóng (than vàng bốc lên, vòng nháy); 7 TÊN LỬA vẽ rõ hình (vỏ
//   thép, mũi đỏ, đai sẫm, hai vây đuôi, lửa phụt đuôi, vệt khói xám) rời đúng ống, đúng giờ `phong` của clip, phụt lửa khói ở miệng ống, bay
//   đường cong Bézier bậc ba NGẪU NHIÊN kiểu homing (điểm lái 1 theo hướng phóng, điểm lái 2 lệch quanh đích, lắc ngang tắt dần, tăng tốc lao
//   vào) tới chỗ chạm riêng trên thân đối thủ; mỗi quả nổ lửa; sau quả cuối nổ rất lớn ba đợt, sóng đất, đá, khói; khép ngực xì hơi.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // màu: KHÔNG dùng biến tĩnh của file khác trong khởi tạo tĩnh (thứ tự khởi tạo giữa các phần partial không cố định)
        static readonly Color RbMuc = C(43, 33, 24);
        static readonly Color[] RbNang = { C(240, 112, 42), C(255, 164, 58), C(255, 217, 74), C(255, 246, 214) }; // năng lượng tươi (2026-11-18; trước = Pal["nang"] ngả nâu)
        static readonly Color[] RbChopC = { C(43, 33, 24), C(240, 112, 42), C(255, 164, 58), C(255, 217, 74), C(255, 246, 214) };
        static readonly float[] RbChopF = { 1, 1, 0.8f, 0.6f, 0.4f };
        static readonly Color RbThep = C(168, 176, 190), RbThepSam = C(78, 82, 96), RbMui = C(214, 62, 42);
        static readonly Color RbLuaNgoai = C(248, 150, 48), RbLuaTrong = C(254, 226, 120);
        static readonly Color[] RbKhoiTen = { C(250, 204, 130), C(150, 146, 146), C(184, 181, 180), C(212, 209, 206) };   // vệt khói tên lửa
        static readonly Color[] RbHoi = { C(200, 204, 210), C(220, 223, 226), C(234, 236, 238), C(246, 246, 246) };        // hơi xì
        // nổ của tên lửa: lửa đỏ cam thường (chủ đề của tướng là năng lượng vàng)
        static readonly Theme RbLuaTh = new Theme
        {
            pal = "lua", spark = C(255, 214, 120), ember = C(248, 140, 44), ring = C(240, 110, 40), ring2 = C(252, 236, 180), extra = "giap",
            extraCol = C(92, 92, 100)
        };

        sealed class RbBang
        {
            public float[] ax, ay, cx, cy, tx, ty, ux, uy, lx, ly, ox, oy, hx, hy;
        }

        static RbBang rb1, rb2;

        static RbBang RbLay(int dang) =>
            dang == 1
                ? (rb1 ??= new RbBang
                {
                    ax = Rb1ACauX, ay = Rb1ACauY, cx = Rb1CCauX, cy = Rb1CCauY, tx = Rb1CTayX, ty = Rb1CTayY, ux = Rb1CTayTX, uy = Rb1CTayTY,
                    lx = Rb1SLoiX, ly = Rb1SLoiY, ox = Rb1SOngX, oy = Rb1SOngY, hx = Rb1SHuongX, hy = Rb1SHuongY
                })
                : (rb2 ??= new RbBang
                {
                    ax = Rb2ACauX, ay = Rb2ACauY, cx = Rb2CCauX, cy = Rb2CCauY, tx = Rb2CTayX, ty = Rb2CTayY, ux = Rb2CTayTX, uy = Rb2CTayTY,
                    lx = Rb2SLoiX, ly = Rb2SLoiY, ox = Rb2SOngX, oy = Rb2SOngY, hx = Rb2SHuongX, hy = Rb2SHuongY
                });

        static Vector2 RbMau(float[] xs, float[] ys, float t)
        {
            float f = Mathf.Max(0, t) / RbDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            float w = Mathf.Clamp01(f - i);
            return new Vector2(Mathf.Lerp(xs[i], xs[j], w), Mathf.Lerp(ys[i], ys[j], w));
        }

        // ================================================================ BỘ HẠT KR5 CỦA HỆ KIM (2026-11-18)
        // Người dùng chê (2026-11-18): đầu tia cụt lủn, không va chạm với địch; nổ, sóng âm chưa đẹp như Kingdom Rush 5; khói rải rác chưa thành
        // cụm, chưa mềm; pha hút / tụ cầu xấu; Mặt Trời và tia màu tối, đốm lửa đơn lẻ và to; màu phải tươi hợp sân cát biển sáng. Các hạt dưới
        // đây dùng chung cho 10 tướng Kim (HatSat … HatPhao), số theo vfx-petclash/hoc_kr5_vfx.md và pokiclash-fx-congthuc mục 2b. Hình mới
        // (bộ hat_kr_* trong Assets/03 Art/Fx/Hat) đang được vẽ: chưa nhập thì mọi hàm dùng hình cũ, không lỗi.
        // Khung vẽ sẵn (2026-11-19, HatFbKim.cs): KmNo, KmKhoi, KmLuaS chuyển sang khung "no" / "trung_lua", "khoi", "lua_lap" khi đã nhập ảnh,
        // nên cả 10 tướng Kim gọi các hàm này đều đổi theo; chưa nhập thì giữ bản hạt.

        static readonly Color KmKem = C(255, 246, 214), KmVangT = C(255, 217, 74), KmCamT = C(255, 164, 58), KmDoCam = C(240, 112, 42);
        // năng lượng / Mặt Trời tươi (người dùng 2026-11-18): mực, dải đậm sát viền cam đỏ (không nâu, không xám), cam tươi, vàng tươi, lõi kem
        static readonly Color[] KmNang = { C(43, 33, 24), C(240, 112, 42), C(255, 164, 58), C(255, 217, 74), C(255, 246, 214) };
        // lửa đỏ cam (nổ tên lửa, đạn sắt, thiên thạch, xích lửa): mực, đỏ cam, cam, vàng, kem
        static readonly Color[] KmLua = { C(43, 33, 24), C(234, 82, 40), C(250, 150, 46), C(255, 212, 76), C(255, 244, 208) };
        // lửa hồn xanh (Vong Kỵ): mực, lục đậm, lục tươi, lục nhạt, kem lục
        // va chạm thép (Kim): mực, thép lam, bạc, vàng kem, trắng kem (bông va chạm, tia của đòn sắt)
        static readonly Color[] KmBac = { C(43, 33, 24), C(126, 142, 182), C(198, 210, 234), C(252, 238, 186), C(255, 252, 238) };
        static readonly Color[] KmHon = { C(43, 33, 24), C(64, 156, 60), C(126, 210, 66), C(190, 242, 112), C(242, 255, 214) };
        // khói hai tông: đỉnh lúc đầu, đỉnh lúc cuối, đáy lúc đầu, đáy lúc cuối. Than: đen than ngả xám (luật khói của dự án)
        static readonly Color[] KmThan = { C(92, 86, 84), C(180, 176, 172), C(44, 38, 36), C(128, 124, 120) };
        static readonly Color[] KmKhoiHon = { C(78, 98, 84), C(174, 194, 176), C(36, 50, 42), C(112, 134, 116) };   // khói hồn: đen ngả xanh xám
        static readonly Color[] KmXam = { C(186, 184, 182), C(232, 230, 228), C(126, 124, 124), C(190, 188, 186) };  // khói máy, khói pháo, hơi xì
        static readonly Color KmDayNong = C(232, 108, 46);  // đáy khói còn ánh lửa lúc vừa bung
        static readonly Color KmChayC = C(86, 66, 52);      // vệt cháy trên đất
        static readonly float[] KmCauF = { 1, 1, 0.86f, 0.68f, 0.46f };

        readonly Dictionary<string, Sprite[]> kmAnh = new Dictionary<string, Sprite[]>();

        // bộ bốn ảnh hat_<ten>_0..3; null nếu chưa nhập (ảnh thiếu trong bộ thì lấy ảnh có sẵn)
        Sprite[] KmBo(string ten)
        {
            if (kmAnh.TryGetValue(ten, out var a)) return a;
            a = new Sprite[4];
            Sprite co = null;
            for (int i = 0; i < 4; i++)
            {
                a[i] = S(ten + "_" + i);
                if (co == null && a[i] != null) co = a[i];
            }
            if (co == null) a = null;
            else
                for (int i = 0; i < 4; i++)
                    if (a[i] == null) a[i] = co;
            kmAnh[ten] = a;
            return a;
        }

        Sprite Km(string ten, int i)
        {
            var a = KmBo(ten);
            return a == null ? null : a[i & 3];
        }

        // bảng lửa tươi cho Flame (Pal của HatLua.cs): thêm lúc chạy, không trong khởi tạo tĩnh (thứ tự khởi tạo giữa các phần partial không cố định)
        void KmPal()
        {
            if (!Pal.ContainsKey("vtuoi")) Pal["vtuoi"] = new[] { KmNang[1], KmNang[2], KmNang[3], KmNang[4] };
            if (!Pal.ContainsKey("luat")) Pal["luat"] = new[] { KmLua[1], KmLua[2], KmLua[3], KmLua[4] };
        }

        static Color[] KmBang(string pal) => pal == "hon" ? KmHon : pal == "lua" || pal == "luat" ? KmLua : KmNang;

        // NHỊP TRÚNG PHỤ (2026-11-18): chớp trắng + đẩy lùi con bị trúng của lần PlayNuoc gần nhất (HatNuoc.NuocPulse, StageView gắn: chớp
        // 0,05 + 0,09k, lùi 2 + 3,5k). k: 1 nhịp đầu / cú mạnh, ~0,4 nhịp sau. Cú trúng chính (giờ trả về) do StageView lo: không gọi trùng.
        // Chặn dày: hai nhịp nhẹ cách nhau dưới 0,08 s thì bỏ nhịp sau (loạt tên lửa, giật điện không thành nhấp nháy liên hồi).
        float kmNhipT = -9;

        void KmNhip(float k)
        {
            if (k <= 0) return;
            if (k < 0.9f && T - kmNhipT < 0.08f) return;
            kmNhipT = T;
            NuocPulse?.Invoke(Mathf.Clamp01(k));
        }

        // ---------- khói cụm ----------
        static readonly Vector2[] KmMui = { new Vector2(-0.42f, 0.14f), new Vector2(0.4f, 0.1f), new Vector2(0.02f, -0.27f) };
        static readonly float[] KmMuiR = { 0.66f, 0.62f, 0.8f };

        // CỤM KHÓI KR5: nhiều múi, hai tông phẳng (đỉnh nhạt, đáy đậm), một viền mực chung với mọi cụm cùng lớp; to gần đủ ngay (22 % đời), bay
        // lên, tới 45 % đời TÁCH thành `tach` cụm con nhỏ toả ra rồi tự co; mờ ở 35 % cuối, không vụt tắt. Tông than đen ngả xám theo tuổi; nong:
        // đáy còn ánh lửa lúc đầu (khói nổ vừa bung); mot: một múi (đuôi đạn, rẻ). Ảnh kr_khoi + kr_khoiday; chưa nhập thì ghép ba múi sblob, đáy
        // mỗi múi tô đậm bằng nửa dưới ảnh.
        P KmKhoi(Vector2 pos, Vector2 vel, float r, float life, int group = Back, float nong = 0, int tach = 2, Color[] tong = null, float tro = 0.3f,
            bool mot = false, float den0 = 0)
        {
            // khung vẽ sẵn (2026-11-19): cụm khói than / khói hồn nhiều múi → khung "khoi" (KmKhoiFb, HatFbKim.cs). Cụm một múi (đuôi đạn, hơi
            // xì), cụm con lúc tách và khói xám nhạt (KmXam: khung nâu xám không sáng lên được) giữ hạt dưới
            if (!mot && tach > 0 && (tong == null || tong == KmThan || tong == KmKhoiHon))
            {
                var f = KmKhoiFb(pos, vel, r, life, group, tong == KmKhoiHon, tro);
                if (f != null) return f;
            }
            var p = new P
            {
                pos = pos, vel = vel, life = life, drag = 1.5f, acc = new Vector2(0, -50), seed = rng.Next(4), r0 = 0.7f * r, r1 = r, group = group,
                ang = U(-0.12f, 0.12f), spin = U(-0.25f, 0.25f), spinDrag = 0.5f, ph = U(0, 6.28f), heat = nong, span = tach, tb = -1, sz = tro,
                big = mot, hgt = den0
            };
            p.stops = tong ?? KmThan;
            p.upd = (q, dt, s) =>
            {
                q.vel.x += Mathf.Sin(q.age * 3.1f + q.ph) * 24 * dt;
                if (q.span <= 0 || q.tb >= 0 || q.age < 0.45f * q.life) return;
                q.tb = q.age;
                float k = q.age / q.life, rr = KmKhoiR(q, k), den = Mathf.Lerp(q.hgt, 1, Mathf.Pow(k, 0.8f));
                for (int j = 0; j < q.span; j++)
                {
                    float a = q.ph + 6.28f * j / q.span + s.U(-0.5f, 0.5f);
                    var d = new Vector2(Mathf.Cos(a), 0.7f * Mathf.Sin(a) - 0.35f);
                    s.KmKhoi(q.pos + d * (0.42f * rr), q.vel * 0.6f + d * s.U(28, 60), rr * s.U(0.5f, 0.62f), (q.life - q.age) * s.U(0.9f, 1.2f), q.group, 0,
                        0, q.stops, q.sz, q.big, den);
                }
            };
            p.draw = DrawKmKhoi;
            if (tro > 0 && U(0, 1) < tro) p.onDeath = (q, s) => s.Ash(q.pos + s.U2(-0.3f, 0.3f) * q.r1, null, q.group);
            return Add(p);
        }

        static float KmKhoiR(P q, float k)
        {
            float r = k < 0.22f ? q.r0 + (q.r1 - q.r0) * EaseOut(k / 0.22f) : q.r1 * (1 - 0.18f * SmoothStep(0.22f, 1, k));
            if (q.tb >= 0) r *= 1 - 0.5f * SmoothStep(q.tb, q.tb + 0.3f * q.life, q.age); // đã tách: cụm mẹ co nhanh, cụm con thay chỗ
            return r * (1 - 0.35f * SmoothStep(0.75f, 1, k));
        }

        void DrawKmKhoi(P q, float k, List<Item> buf)
        {
            float r = KmKhoiR(q, k);
            float aInk = 1 - SmoothStep(0.55f, 0.9f, k), aFill = 1 - SmoothStep(0.62f, 1, k);
            if (r < 1 || aFill < 0.03f) return;
            float den = Mathf.Lerp(q.hgt, 1, Mathf.Pow(k, 0.8f));
            var t = q.stops;
            Color tren = Color.Lerp(t[0], t[1], den), duoi = Color.Lerp(t[2], t[3], den);
            if (q.heat > 0) duoi = Color.Lerp(duoi, KmDayNong, q.heat * (1 - SmoothStep(0.05f, 0.4f, k)));
            int g = q.group;
            var mot = Km("kr_khoi", q.seed);
            if (mot != null)
            {
                float ang = q.ang * Mathf.Rad2Deg;
                var day = Km("kr_khoiday", q.seed);
                if (aInk > 0.03f) Put(buf, g, 10, Km("kr_khois", q.seed) ?? S("ssolid_" + q.seed), Ink, q.pos, 2 * r + 5, 1, ang, aInk);
                Put(buf, g, 11, mot, tren, q.pos, 2 * r, 1, ang, aFill);
                if (day != null) Put(buf, g, 11.4f, day, duoi, q.pos, 2 * r, 1, ang, aFill);
                else Put(buf, g, 11.4f, mot, duoi, q.pos, 2 * r, 1, 0, aFill, 2);
                return;
            }
            if (q.big)
            {
                if (aInk > 0.03f) Put(buf, g, 10, S("ssolid_" + q.seed), Ink, q.pos, 2 * r + 4, 1, 0, aInk);
                Put(buf, g, 11, S("sblob_" + q.seed), tren, q.pos, 2 * r, 1, 0, aFill);
                Put(buf, g, 11.4f, S("sblob_" + q.seed), duoi, q.pos + new Vector2(0, 0.06f * r), 1.88f * r, 1, 0, aFill, 2);
                return;
            }
            float ca = Mathf.Cos(q.ang), sa = Mathf.Sin(q.ang);
            for (int j = 0; j < 3; j++)
            {
                var o = KmMui[j];
                var c = q.pos + new Vector2(o.x * ca - o.y * sa, o.x * sa + o.y * ca) * r;
                float d = 2 * r * KmMuiR[j];
                int sd = (q.seed + j) & 3;
                if (aInk > 0.03f) Put(buf, g, 10, S("ssolid_" + sd), Ink, c, d + 5, 1, 0, aInk);
                Put(buf, g, 11, S("sblob_" + sd), tren, c, d, 1, 0, aFill);
                Put(buf, g, 11.4f, S("sblob_" + sd), duoi, c + new Vector2(0, 0.05f * d), 0.94f * d, 1, 0, aFill, 2);
            }
        }

        // ---------- lửa, đốm ----------

        // đốm lửa nhỏ (lưỡi liềm teo lại): trôi lên chậm theo khói, nguội vàng → cam, co rồi tắt
        P KmDom(Vector2 pos, float sz, Color[] cols, int group = Front, Vector2? vel = null)
        {
            var p = new P
            {
                pos = pos, vel = vel ?? new Vector2(U(-20, 20), -U(40, 80)), life = U(0.35f, 0.6f), drag = 2, seed = rng.Next(2), sz = sz, group = group,
                stops = cols
            };
            p.draw = (q, k, buf) => Put(buf, q.group, 41, S("emberg_" + (q.seed & 1)), Color.Lerp(q.stops[3], q.stops[2], k), q.pos, q.sz * (1 - k * k));
            return Add(p);
        }

        // CỤM ĐỐM LỬA (người dùng 2026-11-18: "các đốm lửa nhìn hơi đơn lẻ và to quá"): 3–6 đốm nhỏ lệch cỡ (0,35–0,7 lần đốm cũ) đi cùng nhau
        void KmDomCum(Vector2 pos, Vector2 vel, Color col, int group = Front, int n = 0)
        {
            if (n <= 0) n = rng.Next(3, 7);
            for (int i = 0; i < n; i++)
            {
                var e = Ember(pos + U2(-7, 7), vel + U2(-16, 16), U(0.55f, 0.95f), i == 0 ? U(5.2f, 6.4f) : U(3f, 4.8f), group);
                e.col = col;
            }
        }

        // LƯỠI LIỀM LỬA của vụ nổ (KR5): bật ra từ tâm, hãm gắt, lưng cong ra ngoài cắm trong khối khói; lõi nguội từ trong ra (kem → vàng → cam)
        // rồi teo thành đốm, đốm trôi lên theo khói. Ảnh kr_liem (lưng +x), đổi hình mỗi 2 khung; chưa nhập thì lưỡi lửa vẽ tay cũ (Flame "luoi").
        void KmLiem(Vector2 c, Vector2 d, float sz, float sp, float life, Color[] cols, string pal, int group)
        {
            if (KmBo("kr_liem") == null)
            {
                var f = Flame(c, d * sp, life, 0.42f * sz, 0.6f * sz, "tron", pal, group, 7, -120, 1.5f, 0, 0);
                Tongue(f, 1, 0.12f);
                f.onDeath = (q, s) => s.KmDom(q.pos, s.U(3, 4.5f), cols, q.group);
                return;
            }
            var p = new P { pos = c, vel = d * sp, life = life, drag = 7, acc = new Vector2(0, -90), seed = rng.Next(4), sz = sz, group = group, aim = d, stops = cols };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (k < 0.15f ? 0.75f + 0.25f * EaseOut(k / 0.15f) : 1 - 0.7f * SmoothStep(0.45f, 1, k));
                if (s < 1.5f) return;
                float ang = VelAng(q.aim);
                int sd = (q.seed + (int)(q.age * 15)) & 3;
                Sprite a = Km("kr_liem", sd), b = Km("kr_liems", sd) ?? a;
                Put(buf, q.group, 20, b, Ink, q.pos, s + 5, 1, ang);
                for (int i = 1; i < 5; i++)
                {
                    float f = i == 1 ? 1 : i == 2 ? 0.84f * (1 - 0.4f * SmoothStep(0.3f, 0.95f, k)) : i == 3 ? 0.66f * (1 - SmoothStep(0.15f, 0.7f, k))
                        : 0.44f * (1 - SmoothStep(0.05f, 0.4f, k));
                    if (f * s < 1.5f) continue;
                    Put(buf, q.group, 20 + i, a, q.stops[i], q.pos + q.aim * (s * (1 - f) * 0.22f), s * f, 1, ang);
                }
            };
            p.onDeath = (q, s) => s.KmDom(q.pos, s.U(3, 4.5f), q.stops, q.group);
            Add(p);
        }

        // LƯỠI LỬA CHỮ S (KR5 "lửa lặp"): liền khối, ngọn uốn, 1–2 giọt tách bay khỏi ngọn; ảnh kr_lua (chân giữa đáy, ngọn lên); chưa nhập thì
        // lưỡi lửa vẽ tay cũ. Cháy tại chỗ, phồng lên rồi teo, lõi nguội dần. Trả hạt (null nếu dùng lưỡi cũ).
        P KmLuaS(Vector2 chan, float h, float life, Color[] cols, string pal, int group, Vector2 vel, float giot = 0.5f)
        {
            // khung vẽ sẵn (2026-11-19): lửa đỏ cam → khung "lua_lap" mọc, cháy, co (KmLuaFb, HatFbKim.cs); lửa hồn xanh giữ hạt (khung cam nhuộm
            // xanh ra xỉn)
            if (cols == KmLua)
            {
                var f = KmLuaFb(chan, h, life, group, vel);
                if (f != null) return f;
            }
            if (KmBo("kr_lua") == null)
            {
                var f = Flame(chan + new Vector2(0, -0.3f * h), vel + new Vector2(0, -U(60, 120)), life, 0.3f * h, 0.5f * h, "tron", pal, group, 2.5f, -260, 1.6f,
                    0.1f, 0);
                Tongue(f, 1, 0.7f);
                f.smokeGroup = Back;
                return null;
            }
            var p = new P
            {
                pos = chan, vel = vel, life = life, drag = 2.2f, acc = new Vector2(0, -120), seed = rng.Next(4), sz = h, group = group, stops = cols,
                ang = U(-10, 10), ph = U(0, 6.28f)
            };
            p.draw = (q, k, buf) =>
            {
                float g = k < 0.2f ? 0.55f + 0.45f * EaseOut(k / 0.2f) : 1 - 0.75f * SmoothStep(0.5f, 1, k);
                float s = q.sz * g;
                if (s < 2) return;
                int sd = (q.seed + (int)(q.age * 15)) & 3;   // đổi dáng mỗi 2 khung (KR5 giữ 2 khung)
                Sprite a = Km("kr_lua", sd), b = Km("kr_luas", sd) ?? a;
                float lac = q.ang + 6 * Mathf.Sin(q.age * 9 + q.ph);
                var tam = q.pos + new Vector2(0, -0.5f * s);   // chân ở giữa đáy ảnh
                Put(buf, q.group, 20, b, Ink, tam, s + 5, 1, lac);
                for (int i = 1; i < 5; i++)
                {
                    float f = i == 1 ? 1 : i == 2 ? 0.82f : i == 3 ? 0.62f * (1 - 0.6f * SmoothStep(0.3f, 0.9f, k)) : 0.4f * (1 - SmoothStep(0.15f, 0.6f, k));
                    if (f * s < 2) continue;
                    Put(buf, q.group, 20 + i, a, q.stops[i], q.pos + new Vector2(0, -0.5f * s * f), s * f, 1, lac);
                }
            };
            if (U(0, 1) < giot)
                p.onDeath = (q, s) => s.KmGiot(q.pos + new Vector2(0, -0.8f * q.sz), new Vector2(s.U(-30, 30), -s.U(90, 160)), 0.16f * q.sz, q.stops, q.group);
            return Add(p);
        }

        // giọt lửa tách khỏi ngọn: bay lên, co lại (ảnh kr_giot, chưa nhập thì lưỡi nhỏ)
        void KmGiot(Vector2 pos, Vector2 vel, float sz, Color[] cols, int group)
        {
            var p = new P { pos = pos, vel = vel, life = U(0.22f, 0.34f), drag = 3, acc = new Vector2(0, -60), seed = rng.Next(4), sz = Mathf.Max(4, sz), group = group, stops = cols };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (1 - k * k);
                if (s < 1.2f) return;
                var a = Km("kr_giot", q.seed);
                if (a == null)
                {
                    Put(buf, q.group, 40, S("emberg_" + (q.seed & 1)), q.stops[3], q.pos, s);
                    return;
                }
                float ang = q.vel.sqrMagnitude > 1 ? VelAng(q.vel) : -90;   // đầu tròn của giọt (+x ảnh) theo hướng bay
                Put(buf, q.group, 39, Km("kr_giots", q.seed) ?? a, Ink, q.pos, 2.2f * s + 3, 1, ang);
                Put(buf, q.group, 39.1f, a, Color.Lerp(q.stops[3], q.stops[2], k), q.pos, 2.2f * s, 1, ang);
            };
            Add(p);
        }

        // ---------- nổ ----------

        // CHỚP NỔ 1–2 khung (KR5): sao gai kem lõi vàng, nhỏ (khoảng 1/3 vụ nổ); ảnh kr_chop hoặc burst cũ
        void KmChop(Vector2 c, float size, float life, Color[] cols, int group = Front)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = rng.Next(4), sz = size, stops = cols };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (0.8f + 0.35f * EaseOut(k / 0.5f));
                var a = Km("kr_chop", q.seed);
                Sprite v = a != null ? Km("kr_chops", q.seed) ?? a : S("bursts_" + q.seed), f = a ?? S("burst_" + q.seed);
                Put(buf, q.group, 33, v, Ink, q.pos, s + 4, 1, q.ang);
                Put(buf, q.group, 33.1f, f, q.stops[3], q.pos, s, 1, q.ang);
                Put(buf, q.group, 33.2f, f, q.stops[4], q.pos, s * 0.62f, 1, q.ang);
            };
            Add(p);
        }

        // VÒNG CUNG DẸT trên đất (KR5): elip phẳng KHÔNG viền, nở nhanh rồi hãm, nhạt dần; ảnh kr_cung (cung đứt đoạn) hoặc vòng ring cũ
        void KmCung(Vector2 pos, float R0, float R1, float life, Color col, float squash = 0.3f, int group = Floor, float layer = 30.5f, float alpha = 0.9f)
        {
            var p = new P { pos = pos, life = life, group = group, col = col, R0 = R0, R1 = R1, hgt = squash, ph = layer, seed = rng.Next(4), wd = alpha };
            p.draw = (q, k, buf) =>
            {
                float R = q.R0 + (q.R1 - q.R0) * EaseOut(k);
                float a = q.wd * (1 - SmoothStep(0.35f, 1, k));
                if (a < 0.03f || R < 2) return;
                var cung = Km("kr_cung", q.seed);
                if (cung != null)   // ảnh đã vẽ dẹt sẵn trong khung vuông: nét chiếm 0,9 bề ngang, 0,36 bề cao
                {
                    float hh = 2 * R * q.hgt / 0.36f;
                    Put(buf, q.group, q.ph, cung, q.col, q.pos, hh, 2 * R / 0.9f / hh, 0, a);
                }
                else Put(buf, q.group, q.ph, S("ring"), q.col, q.pos, 2 * R * q.hgt, 1 / q.hgt, 0, a);
            };
            Add(p);
        }

        // VỆT CHÁY trên đất dưới vụ nổ: elip đậm phẳng alpha thấp, giữ `giu` giây rồi mờ trong `mo` giây (KR5: decal giữ 1–2 s)
        void KmChay(Vector2 pos, float R, float giu = 1f, float mo = 0.9f, float alpha = 0.38f)
        {
            var p = new P { pos = pos, life = giu + mo, group = Floor, sz = R, wd = alpha, tb = giu, col = KmChayC };
            p.draw = (q, k, buf) =>
            {
                float a = q.wd * Mathf.Min(1, q.age / 0.08f) * (1 - SmoothStep(q.tb, q.life, q.age));
                if (a < 0.02f) return;
                Put(buf, Floor, 1.5f, S("ell") ?? S("solid_0"), q.col, q.pos, 2 * q.sz * 0.3f * Mathf.Min(1, 0.6f + q.age / 0.15f), 1 / 0.3f, 0, a);
            };
            Add(p);
        }

        // tia kim loại bắn nhanh rồi KHỰNG (cản gắt), kéo dài theo tốc độ
        P KmTiaLua(Vector2 c, Vector2 d, float sp, float sz, Color col, int group = Front)
        {
            var q = Spark(c, d, sp, U(0.24f, 0.36f), sz, 520, group, 8.5f);
            q.col = col;
            return q;
        }

        // VỤ NỔ KR5 (2026-11-18): chớp 1–2 khung → lưỡi liềm lửa cắm trong khối khói hai tông đã to gần đủ → khói tách cụm bay lên rồi mờ; vòng
        // cung dẹt trên đất, tia bắn rồi khựng, mảnh văng một phía, vệt cháy giữ ~1 s. Lõi (khói, phần lớn lưỡi liềm) ở Sau tướng, phía trước chỉ
        // vài lưỡi nhỏ + tia: không che con bị trúng. c: tâm; dat: đất dưới tâm; tH: chiều cao đối thủ; sc: cỡ (0,4 trúng nhỏ … 1,8 chiêu cuối);
        // pal: "luat" lửa đỏ cam, "vtuoi" năng lượng vàng tươi, "hon" lửa hồn; huong: phía mảnh văng (+1 / −1); khoi: tông khói (null: than)
        void KmNo(Vector2 c, Vector2 dat, float tH, float sc, string pal, float huong, Color[] khoi = null)
        {
            // khung vẽ sẵn (2026-11-19): lửa đỏ cam / năng lượng vàng → khung "no" (nổ to, neo ở đất, sau tướng) hoặc "trung_lua" (nổ nhỏ trên
            // thân), KmNoFb ở HatFbKim.cs; lửa hồn và máy chưa nhập ảnh đi bản hạt dưới
            if (pal != "hon" && KmNoFb(c, dat, tH, sc, pal, huong)) return;
            KmPal();
            var cols = KmBang(pal);
            float D = 0.68f * tH * Mathf.Pow(sc, 0.6f);
            bool lon = sc >= 1.1f, nho = sc < 0.8f;
            KmChop(c, (lon ? 0.3f : 0.38f) * D, lon ? 0.07f : 0.06f, cols);   // nổ lớn: cục chớp nhỏ lấy đà 2 khung rồi mới bung
            At(lon ? 0.06f : 0.035f, () =>
            {
                // khối khói hai tông sau tướng, to gần đủ ngay, đáy còn ánh lửa
                int nk = Mathf.Clamp(Mathf.RoundToInt(0.8f + 2.6f * sc), 1, 6);   // nổ nhỏ (loạt tên lửa) ít cụm: ngân sách hạt
                // khung vẽ sẵn (2026-11-19): khói than / khói hồn ra khung "khoi" (KmKhoi): ít cụm hơn mà to hơn (nhiều khung sát nhau thành bóng đôi)
                bool fbKhoi = HasFb("khoi") && (khoi == null || khoi == KmThan || khoi == KmKhoiHon);
                if (fbKhoi) nk = Mathf.Clamp(Mathf.RoundToInt(0.5f + 1.2f * sc), 1, 3);
                for (int i = 0; i < nk; i++)
                {
                    float a = 6.28f * (i + U(-0.25f, 0.25f)) / nk;
                    // khối lõi sau lưng đối thủ nhưng LÒI ra hai bên và trên đầu (soi tờ khung 2026-11-18: đặt sát tâm thì thân che hết)
                    var o = new Vector2(Mathf.Cos(a) * (nho ? 0.3f : 0.44f), Mathf.Sin(a) * 0.26f - (nho ? 0.12f : 0.2f)) * D;
                    KmKhoi(c + o, Unit(o) * U(30, 70) * Mathf.Sqrt(sc) + new Vector2(0, -U(30, 60)), U(0.21f, 0.29f) * D * (fbKhoi ? 1.35f : 1),
                        U(0.85f, 1.2f) * (0.8f + 0.2f * sc), Back, 1, sc < 0.6f ? 1 : 2, khoi, 0.35f);
                }
                // lưỡi liềm lửa toả đều như cánh hoa, phần lớn sau tướng
                int nl = Mathf.Clamp(Mathf.RoundToInt(1.5f + 3.6f * sc), 3, 9);
                for (int i = 0; i < nl; i++)
                {
                    float a = 6.28f * (i + U(-0.3f, 0.3f)) / nl;
                    var d = Unit(new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.85f - 0.15f));
                    bool truoc = nho ? i % 3 != 2 : i % 3 == 1;   // nổ trúng nhỏ: lửa phía trước (nhỏ hơn thân); nổ lớn: lõi sau, vài lưỡi nhỏ phía trước
                    KmLiem(c + d * 0.06f * D, d, (truoc ? 0.2f : 0.28f) * D, U(320, 520) * Mathf.Sqrt(sc), U(0.2f, 0.3f), cols, pal, truoc ? Front : Back);
                }
                // vòng cung dẹt + vệt cháy trên đất
                KmCung(dat + new Vector2(0, 2), 0.12f * D, (0.9f + 0.3f * sc) * D, 0.34f, cols[4]);
                if (sc >= 0.5f) KmChay(dat + new Vector2(0, 3), 0.42f * D, 0.9f + 0.2f * sc, 0.9f);
                // tia bắn rồi khựng, mảnh văng một phía
                int ns = Mathf.Clamp(Mathf.RoundToInt(1 + 4 * sc), 2, 9);
                for (int i = 0; i < ns; i++)
                {
                    float a = U(0, 6.28f);
                    KmTiaLua(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f), U(520, 820) * Mathf.Sqrt(sc), U(6, 9), (i & 1) == 0 ? cols[4] : cols[3]);
                }
                if (lon)
                    for (int i = 0; i < 3; i++)
                        Rock(dat + new Vector2(huong * U(0, 0.25f) * tH, -8), new Vector2(huong * U(80, 320), -U(260, 480)), dat.y + U(-4, 6), U(9, 13));
                if (sc >= 0.5f) Extra(c, Mathf.RoundToInt(2 * sc), 300 * Mathf.Sqrt(sc), Front);
            });
        }

        // ---------- tia, va chạm ----------

        // BÔNG VA CHẠM ở chỗ tia / đạn chạm thân: toé về hướng d (ảnh kr_tiadau toé +x; chưa nhập thì sao nổ burst), đổi hình mỗi 2 khung
        void KmBong(Vector2 c, Vector2 d, float size, float life, Color[] cols, int group = Front)
        {
            var p = new P { pos = c, life = life, group = group, seed = rng.Next(4), sz = size, aim = Unit(d), stops = cols, ang = U(0, 360) };
            p.draw = (q, k, buf) =>
            {
                float s = q.sz * (k < 0.3f ? 0.7f + 0.45f * EaseOut(k / 0.3f) : 1.15f - 0.5f * SmoothStep(0.4f, 1, k));
                int sd = (q.seed + (int)(q.age * 15)) & 3;
                var a = Km("kr_tiadau", sd);
                float ang = a != null ? VelAng(q.aim) : q.ang;
                Sprite v = a != null ? Km("kr_tiadaus", sd) ?? a : S("bursts_" + sd), f = a ?? S("burst_" + sd);
                Put(buf, q.group, 34, v, Ink, q.pos, s + 4, 1, ang);
                Put(buf, q.group, 34.1f, f, q.stops[2], q.pos, s, 1, ang);
                Put(buf, q.group, 34.2f, f, q.stops[3], q.pos + q.aim * (0.06f * s), s * 0.76f, 1, ang);
                Put(buf, q.group, 34.3f, f, q.stops[4], q.pos + q.aim * (0.1f * s), s * 0.48f, 1, ang);
            };
            Add(p);
        }

        // vòng mảnh KHÔNG viền mực quanh một tâm đang chạy: R1 < R0 thì co về tâm nhanh dần (pha tụ), ngược lại bung rồi hãm (va chạm)
        void KmVong(Func<float, Vector2> tam, float life, float R0, float R1, Color col, float squash = 1, float alpha = 0.85f, int group = Front)
        {
            var p = new P { pos = tam(T), life = life, group = group, col = col, R0 = R0, R1 = R1, hgt = squash, wd = alpha };
            p.upd = (q, dt, s) =>
            {
                q.pos = tam(s.T);
                q.vel = Vector2.zero;
            };
            p.draw = (q, k, buf) =>
            {
                bool co = q.R1 < q.R0;
                float R = q.R0 + (q.R1 - q.R0) * (co ? k * k : EaseOut(k));
                float a = q.wd * (co ? SmoothStep(0, 0.25f, k) * (1 - SmoothStep(0.85f, 1, k)) : 1 - SmoothStep(0.5f, 1, k));
                if (a < 0.03f || R < 2) return;
                Put(buf, q.group, 32.5f, S("ring"), q.col, q.pos, 2 * R * q.hgt, 1 / q.hgt, 0, a);
            };
            Add(p);
        }

        // TIA NĂNG LƯỢNG LIỀN KHỐI (mảng liền, không ghép hạt rời): src → dst. Đầu tia lao tới đúng dst (thân đối thủ) rồi DỪNG ở đó; thân rung
        // nhẹ; hết dur thì đuôi RÚT về chỗ chạm trong `rut` giây và thon lại (không cắt phụt). Năm lớp: mực mảnh, dải cam đỏ sát viền, cam, vàng,
        // lõi kem rộng. hw: nửa bề rộng (sân); gán sizeFn(hạt, phần quãng 0..1) của hạt trả về để tia dày mỏng theo chiều dài.
        P KmTia(Vector2 src, Vector2 dst, float dur, float hw0, Color[] cols, int group = Front, float sp = 2400, float rut = 0.14f)
        {
            var dd = dst - src;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            var core = new P { pos = src, life = dur + rut + 0.02f, group = group, stops = cols };
            core.draw = (q, k, buf) =>
            {
                float a = q.age;
                float head = Mathf.Min(dist, sp * a), tail = dist * SmoothStep(dur, dur + rut, a);
                if (head - tail < 6) return;
                int n = Mathf.Max(2, Mathf.CeilToInt((head - tail) / 14) + 1);
                float no = Mathf.Min(1, 0.35f + a / 0.06f) * (1 - 0.55f * SmoothStep(dur - 0.06f, dur + rut, a));
                for (int li = 0; li < 5; li++)
                {
                    float wf = li < 2 ? 1 : li == 2 ? 0.9f : li == 3 ? 0.74f : 0.5f, grow = li == 0 ? 1.7f : 0;
                    int a0 = mp.Count;
                    for (int pass = 0; pass < 2; pass++)
                        for (int i = 0; i < n; i++)
                        {
                            float x = tail + (head - tail) * i / (n - 1);
                            float hw = hw0 * no * (1 + 0.08f * Mathf.Sin(x * 0.05f - a * 52)) * (q.sizeFn != null ? q.sizeFn(q, x / Mathf.Max(1, dist)) : 1) *
                                       Mathf.Min(1, Mathf.Min((x - tail) / 26 + 0.4f, (head - x) / 18 + 0.75f));
                            var c = src + u * x + nrm * (1.2f * Mathf.Sin(x * 0.07f - a * 38));
                            mp.Add(c + nrm * ((pass == 0 ? 1 : -1) * (hw * wf + grow)));
                        }
                    MRibbon(q.group, 9 + li * 0.1f, a0, a0 + n, n, q.stops[li]);
                }
            };
            return Add(core);
        }

        // VA CHẠM LIÊN TỤC ở chỗ tia chạm thân (t0 → t1, giây từ lúc gọi): bông toé đổi hình mỗi 2 khung, tia kim loại bắn ngược rồi khựng, vòng va
        // chạm nở, chớp, màn rung nhỏ dồn dập; hết tia thì bông vỡ to một lần. u: hướng tia; hw: nửa bề rộng tia
        // dau: sức nhịp đầu lúc đầu tia chạm (0: bỏ, khi cú trúng chính của StageView trùng lúc này); các nhịp sau 0,4
        void KmCham(Vector2 c, Vector2 u, float t0, float t1, float hw, Color[] cols, float manh, float dau = 1)
        {
            At(t0, () => KmNhip(dau));
            var nrm = new Vector2(-u.y, u.x);
            Every(t0, t1, 15, x => KmBong(c + U2(-0.2f, 0.2f) * hw, -u + nrm * U(-0.6f, 0.6f), U(2.4f, 3.2f) * hw * manh, 0.1f, cols));
            Every(t0, t1, 34 * manh, x =>
            {
                float sd = rng.Next(2) == 0 ? -1 : 1;
                KmTiaLua(c, -u * U(0.2f, 0.9f) + nrm * sd * U(0.5f, 1.2f), U(380, 720), U(5, 8), (rng.Next(2) == 0) ? cols[4] : cols[3]);
            });
            Every(t0, t1, 7, x =>
            {
                KmVong(_ => c, 0.2f, 0.6f * hw, 2.8f * hw * manh, cols[4], 0.55f, 0.8f);
                Shake?.Invoke(0.05f * manh);
                KmNhip(0.4f);   // đối thủ chớp + giật theo nhịp tia
            });
            At(t1, () =>
            {
                KmNhip(0.6f);
                KmBong(c, -u, 4.2f * hw * manh, 0.16f, cols);
                KmVong(_ => c, 0.26f, hw, 3.6f * hw * manh, cols[4], 0.55f, 0.85f);
                for (int i = 0; i < 6; i++) KmTiaLua(c, -u * U(0, 0.8f) + nrm * U(-1.2f, 1.2f), U(420, 760), U(6, 9), cols[3 + (i & 1)]);
            });
        }

        // ---------- pha tụ ----------

        // HẠT BỊ HÚT (người dùng 2026-11-18: hạt hút quanh cầu đang xấu): VỆT thuôn kéo dài theo vận tốc (đầu đậm, đuôi nhọn; ảnh kr_vet hoặc
        // streakg cũ), bay XOẮN ỐC vào tâm, nhanh dần (ease-in), hiện dần lúc sinh, chạm vỏ cầu (bán kính rt) thì nhập vào cầu, không tắt giữa
        // đường. tam / rt: tâm, bán kính cầu theo giờ sân; xa: bán kính lúc sinh; chieu: +1 / −1 chiều xoáy; dep: độ dẹt quỹ đạo
        void KmHut(Func<float, Vector2> tam, Func<float, float> rt, float xa, float life, float sz, Color col, float chieu, int group = Front, float dep = 0.8f)
        {
            float a0 = U(0, 6.28f);
            var p = new P
            {
                life = life, group = group, sz = sz, seed = rng.Next(4), col = col, ph = a0, wd = chieu * U(1.5f, 2.5f), R0 = xa, hgt = dep
            };
            p.pos = tam(T) + new Vector2(Mathf.Cos(a0), dep * Mathf.Sin(a0)) * xa;
            p.upd = (z, dt, s) =>
            {
                float k = Mathf.Clamp01((z.age + dt) / z.life);
                float e = k * k * (0.3f + 0.7f * k);                         // chậm lúc đầu, lao nhanh dần khi tới gần
                float rc = Mathf.Max(1, rt(s.T));
                float R = Mathf.Lerp(z.R0, 0.85f * rc, e);
                float a = z.ph + z.wd * e;
                var np = tam(s.T) + new Vector2(Mathf.Cos(a), z.hgt * Mathf.Sin(a)) * R;
                z.vel = dt > 1e-5f ? (np - z.pos) / dt : Vector2.zero;
                if (k >= 0.999f || R <= 0.9f * rc) z.dead = true;               // tới vỏ cầu: nhập vào cầu
            };
            p.draw = (z, k, buf) =>
            {
                float sp = z.vel.magnitude;
                float hien = SmoothStep(0, 0.3f, k);
                float st = Mathf.Clamp(sp / 70, 1.5f, 4.6f), ang = sp > 1 ? VelAng(z.vel) : 0;
                var vet = Km("kr_vet", z.seed);
                if (vet == null)
                {
                    Put(buf, z.group, 40, S("streakg_" + (z.seed & 1)), z.col, z.pos, z.sz * (0.6f + 0.4f * hien), st, ang, hien);
                    return;
                }
                float dai = z.sz * st * 1.1f, cao = Mathf.Min(dai, 2.6f * z.sz);   // ảnh vuông, nét vệt mảnh nằm ngang giữa khung
                Put(buf, z.group, 39.5f, Km("kr_vets", z.seed) ?? vet, Ink, z.pos, cao + 3, (dai + 3) / (cao + 3), ang, hien);
                Put(buf, z.group, 39.6f, vet, z.col, z.pos, cao, dai / cao, ang, hien);
            };
            Add(p);
        }

        // cầu NÉN lại 1–2 khung ngay trước lúc nhả rồi bung (nhân vào bán kính): t, tBan tính cùng một gốc giờ
        static float KmNen(float t, float tBan) => t >= tBan - 0.075f && t < tBan ? 1 - 0.24f * SmoothStep(tBan - 0.075f, tBan - 0.02f, t) : 1;

        // ĐUÔI THEO QUÃNG BAY (KR5: hạt đuôi chia đều theo quãng đạn vừa đi, nên đuôi liền dù đạn nhanh): hạt dẫn vô hình bám vat(giờ sân) trong
        // dur giây, mỗi `buoc` đơn vị sân đường đi gọi sinh(điểm, hướng bay) một lần (nội suy trong khung)
        void KmDuoi(Func<float, Vector2> vat, float dur, float buoc, Action<Vector2, Vector2> sinh)
        {
            var p = new P { pos = vat(T), life = dur, group = Front, wd = 0 };
            p.upd = (z, dt, s) =>
            {
                var np = vat(s.T);
                var d = np - z.pos;
                float m = d.magnitude;
                if (m > 1e-3f)
                {
                    var u = d / m;
                    float x = buoc - z.wd;
                    int dem = 0;
                    while (x <= m && dem++ < 12)
                    {
                        sinh(z.pos + u * x, u);
                        x += buoc;
                    }
                    z.wd = m - (x - buoc);
                }
                z.pos = np;
                z.vel = Vector2.zero;
            };
            Add(p);
        }

        // ---------------------------------------------------------------- hạt dùng chung

        // QUẢ CẦU NĂNG LƯỢNG: một hạt (viền mực + bốn lớp vàng → trắng lệch nhau, xoay; hai cung điện quay ngược chiều nhau), bám tam(giờ sân), bán
        // kính rt(giờ sân); lúc bay thì kéo dài theo hướng bay
        P RbCau(Func<float, Vector2> tam, Func<float, float> rt, float life, int group = Front)
        {
            var p = new P { pos = tam(T), life = life, group = group, seed = rng.Next(4), ph = U(0, 6.28f), r0 = rt(T) };
            p.upd = (z, dt, s) =>
            {
                var np = tam(s.T);
                z.aim = (np - z.pos) / Mathf.Max(1e-4f, dt);
                z.pos = np;
                z.vel = Vector2.zero;
                z.r0 = rt(s.T);
            };
            // 2026-11-18 (người dùng: cầu tụ xấu, màu tối): vỏ NHIỀU MÚI (ba múi lệch tâm quay ngược nhau, hình bóng không tròn trơn) + lõi kem lệch
            // nhẹ, bảng năng lượng tươi; lớn theo NHỊP ĐẬP (giật ngắn, nghỉ dài, dồn dần khi đầy). Ảnh kr_cau (khối cuộn nhiều múi) nếu đã nhập.
            p.draw = (z, k, buf) =>
            {
                float nhip = Mathf.Pow(Mathf.Max(0, Mathf.Sin(z.age * (8 + 5 * Mathf.Min(1, z.age)) + z.ph)), 8);
                float r = z.r0 * (1 + 0.1f * nhip + 0.025f * Mathf.Sin(z.age * 41 + z.ph));
                if (r < 1) return;
                float sp = z.aim.magnitude, st = 1 + Mathf.Min(0.55f, sp / 1500), va = sp > 40 ? VelAng(z.aim) : 0;
                var cau = Km("kr_cau", z.seed);
                // kiểu ENERGY BALL vẽ sẵn bằng Blender (2026-11-24, người dùng chọn): thân múi cam vàng + gân kem lộ qua khe thay viền mực và bốn
                // lớp kr_cau; bán kính thấy = r như lớp ngoài cũ (2 r). Hai cung điện quay quanh giữ nguyên
                if (VeCauNl(buf, "cau_vang", z.pos, r, z.group, 26, z.age + z.ph * 0.24f, va, st)) { /* thân cầu đã vẽ bằng khung */ }
                else if (cau != null)
                {
                    float quay = z.age * 150;
                    Put(buf, z.group, 26, Km("kr_caus", z.seed) ?? cau, RbMuc, z.pos, 2 * r + 5, st, va + quay);
                    for (int i = 1; i < 5; i++)
                        Put(buf, z.group, 26 + 0.2f * i, Km("kr_cau", z.seed + (i >> 1)), KmNang[i], z.pos, 2 * r * KmCauF[i], st,
                            va + quay * ((i & 1) == 0 ? -1.3f : 1) + 40 * i);
                }
                else
                {
                    for (int l = 0; l < 2; l++)
                        for (int j = 0; j < 3; j++)
                        {
                            float a = z.age * 3.4f * ((j & 1) == 0 ? 1 : -1) + j * 2.09f + z.ph;
                            var c = z.pos + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * (0.2f * r);
                            Put(buf, z.group, 26 + 0.2f * l, S((l == 0 ? "solid_" : "blob_") + ((z.seed + j) & 3)), l == 0 ? RbMuc : KmNang[1], c,
                                1.64f * r + (l == 0 ? 5 : 0), st, va + 50 * j);
                        }
                    float b = z.age * 5.1f + z.ph;
                    Put(buf, z.group, 26.5f, S("blob_" + ((z.seed + 1) & 3)), KmNang[2], z.pos + new Vector2(Mathf.Cos(b), Mathf.Sin(b)) * (0.05f * r),
                        2 * r * 0.86f, st, va + 23);
                    Put(buf, z.group, 26.7f, S("blob_" + ((z.seed + 2) & 3)), KmNang[3], z.pos + new Vector2(Mathf.Cos(b), Mathf.Sin(b)) * (0.09f * r),
                        2 * r * 0.66f, st, va + 61);
                    Put(buf, z.group, 26.9f, S("blob_" + ((z.seed + 3) & 3)), KmNang[4], z.pos + new Vector2(Mathf.Cos(-b), Mathf.Sin(-b)) * (0.1f * r),
                        2 * r * 0.42f, st, va + 97);
                }
                for (int j = 0; j < 2; j++)   // hai cung điện quay ngược nhau: vẽ KHÔNG viền (cung mảnh có viền thành vòng đen quanh cầu)
                {
                    float a = (j == 0 ? 1 : -1) * z.age * 520 + j * 140 + z.ph * Mathf.Rad2Deg;
                    Put(buf, z.group, 27.25f + 0.1f * j, S("arc_" + ((z.seed + 5 * j) % 12)), KmNang[4 - j], z.pos, 2.5f * r, 1, a);
                }
            };
            return Add(p);
        }

        // hạt năng lượng bị hút từ `tu` vào tâm đang chạy: vệt thuôn theo hướng bay, hiện dần, nhanh dần (ease-in), chạm vỏ cầu (rt) thì nhập vào
        // cầu (2026-11-18: trước đây bay tới TÂM mới tắt, hiện phụt)
        void RbHut(Func<float, Vector2> tam, Vector2 tu, float life, float sz, int group = Front, Func<float, float> rt = null)
        {
            float xa = Mathf.Max(10, (tam(T) - tu).magnitude);
            var p = new P { pos = tu, life = life, group = group, sz = sz, seed = rng.Next(4), col = U(0, 1) < 0.5f ? KmNang[3] : KmNang[4], R0 = xa };
            p.upd = (z, dt, s) =>
            {
                var d = tam(s.T) - z.pos;
                float m = d.magnitude, v = z.R0 * (0.5f + 6f * Mathf.Pow(z.age / z.life, 2));
                float rc = rt != null ? 0.85f * rt(s.T) : 1.5f;
                if (m < v * dt + rc)
                {
                    z.dead = true;
                    return;
                }
                z.vel = d / m * v;
            };
            p.draw = (z, k, buf) =>
            {
                float hien = SmoothStep(0, 0.3f, k), st = Mathf.Clamp(z.vel.magnitude / 70, 1.5f, 4.4f), ang = VelAng(z.vel);
                var vet = Km("kr_vet", z.seed);
                if (vet == null)
                {
                    Put(buf, z.group, 40, S("streakg_" + (z.seed & 1)), z.col, z.pos, z.sz * (0.6f + 0.4f * hien), st, ang, hien);
                    return;
                }
                float dai = z.sz * st * 1.1f, cao = Mathf.Min(dai, 2.6f * z.sz);   // ảnh vuông, nét vệt mảnh nằm ngang giữa khung
                Put(buf, z.group, 39.5f, Km("kr_vets", z.seed) ?? vet, RbMuc, z.pos, cao + 3, (dai + 3) / (cao + 3), ang, hien);
                Put(buf, z.group, 39.6f, vet, z.col, z.pos, cao, dai / cao, ang, hien);
            };
            Add(p);
        }

        // hạt hút từ xa: XOẮN ỐC vào cầu (KmHut), cùng một chiều xoáy cho cả luồng; rt: bán kính cầu (null: tụ vào một điểm)
        void RbHutXa(Func<float, Vector2> tam, float xa, float life, float sz, int group = Front, Func<float, float> rt = null) =>
            KmHut(tam, rt ?? (_ => 3), xa, life, sz, U(0, 1) < 0.5f ? KmNang[3] : KmNang[4], 1, group, 0.8f);

        // lưỡi năng lượng liếm quanh cầu (tâm c, bán kính r): bảng năng lượng tươi
        void RbLiem(Vector2 c, float r, int group = Front)
        {
            KmPal();
            float a = U(0, 6.28f);
            var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
            var q = Flame(c + o * r * 0.62f, o * U(30, 80) + new Vector2(0, -U(30, 70)), U(0.16f, 0.26f), r * 0.26f, r * 0.42f, "tron", "vtuoi", group, 3, -150,
                1.5f, 0, 0);
            Tongue(q, 1, 0.4f);
        }

        // xoáy năng lượng ở một lòng bàn tay đang xoay: ba cung điện quay nhanh quanh tâm; chieu: +1 / −1
        void RbXoay(Func<float, Vector2> tam, float r, float life, float chieu, int group = Front)
        {
            var p = new P { pos = tam(T), life = life, group = group, seed = rng.Next(12), sz = r, ph = chieu };
            p.upd = (z, dt, s) =>
            {
                z.pos = tam(s.T);
                z.vel = Vector2.zero;
            };
            p.draw = (z, k, buf) =>
            {
                float rr = z.sz * Mathf.Min(1, z.age / 0.15f) * (1 - SmoothStep(0.88f, 1, k)) * (1 + 0.08f * Mathf.Sin(z.age * 31));
                if (rr < 1) return;
                for (int j = 0; j < 3; j++)
                {
                    float a = z.ph * z.age * 900 + 120 * j;
                    Put(buf, z.group, 38 + 0.1f * j, S("arcs_" + ((z.seed + 4 * j) % 12)), RbMuc, z.pos, 2.4f * rr, 1, a);
                    Put(buf, z.group, 38.05f + 0.1f * j, S("arc_" + ((z.seed + 4 * j) % 12)), RbNang[2 + (j & 1)], z.pos, 2.4f * rr, 1, a);
                }
            };
            Add(p);
        }

        // chớp toé vàng (năm lớp sao nổ lồng nhau)
        void RbChop(Vector2 c, float size, int group = Front, float life = 0.14f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = rng.Next(4), sz = size };
            p.draw = (q, k, buf) =>
            {
                for (int i = 0; i < 5; i++)
                    Put(buf, q.group, 33 + 0.1f * i, S((i == 0 ? "bursts_" : "burst_") + q.seed), RbChopC[i], q.pos,
                        q.sz * (0.6f + 0.5f * EaseOut(k / 0.6f)) * RbChopF[i] + (i == 0 ? 5 : 0), 1, q.ang);
            };
            Add(p);
        }

        // vòng tròn (nhìn thẳng) quanh một điểm: vòng mảnh KHÔNG viền mực (2026-11-18; vòng mảnh có viền mực thành vòng đen, vfx-petclash mục 4)
        void RbVong(Vector2 c, float life, float R0, float R1, Color col) => KmVong(_ => c, life, R0, R1, col, 1, 0.9f);

        // tia văng toả đều quanh tâm
        void RbTia(Vector2 c, float r, int n, float v0, float v1, float grav = 200)
        {
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.7f)) / n;
                var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                var q = Spark(c + o * r, o, U(v0, v1) * 1.25f, U(0.22f, 0.34f), 7, grav, Front, 7);   // bắn nhanh rồi khựng
                q.col = (i & 1) == 0 ? KmNang[4] : KmNang[3];
            }
        }

        // hơi xì (giáp ngực mở / khép, ổ nắm đấm sau phát bắn): cụm hơi trắng xám phụt theo dir rồi tan
        void RbHoiXi(Vector2 pos, Vector2 dir, float sc, int n = 3, int group = Front)
        {
            for (int i = 0; i < n; i++)   // cụm hơi xám nhạt hai tông một múi (2026-11-18)
                KmKhoi(pos + dir * U(0, 6), dir * U(90, 170) * sc + new Vector2(U(-15, 15), -U(10, 30)), U(8, 12) * sc, U(0.45f, 0.7f), group, 0, 0, KmXam, 0,
                    true, 0.3f);
        }

        // sỏi dưới chân bị năng lượng nhấc lên, lắc lư rồi tan
        void RbSoi(Vector2 pos, float sz)
        {
            var p = new P
            {
                pos = pos, vel = new Vector2(U(-15, 15), -U(50, 110)), life = U(0.7f, 1.1f), drag = 0.6f, spin = U(-4, 4), seed = rng.Next(4), sz = sz,
                group = U(0, 1) < 0.5f ? Back : Front, ph = U(0, 6.28f)
            };
            p.upd = (z, dt, s) => z.vel.x += Mathf.Sin(z.age * 6 + z.ph) * 40 * dt;
            p.draw = (z, k, buf) => Put(buf, z.group, 45, S("rock_" + (z.seed & 3)), Color.white, z.pos,
                z.sz * Mathf.Min(1, z.age / 0.1f) * (1 - SmoothStep(0.7f, 1, k)), 1, z.ang * Mathf.Rad2Deg);
            Add(p);
        }

        // vết nứt đất sáng dưới chân đối thủ (không có vũng dung nham như Crater)
        void RbNut(Vector2 pos, float H, float life = 1.4f)
        {
            var cr = new P { pos = pos, life = life, group = Floor, seed = rng.Next(4), sz = H };
            cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_" + q.seed), Color.white, q.pos, 1.7f * q.sz * 0.42f * Mathf.Min(1, q.age / 0.12f),
                1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.3f));
            Add(cr);
        }

        // cột năng lượng phụt thẳng lên từ chân đối thủ (dur giây), bọc quanh thân: nửa sau, nửa trước
        void RbCot(Vector2 feet, float H, float dur, float manh)
        {
            KmPal();
            Every(0, dur, 60, x =>
            {
                float w = 0.2f * H * manh * (1 - 0.5f * x);
                bool truoc = U(0, 1) < 0.25f;  // phần lớn cột sau lưng đối thủ, vài lưỡi nhỏ phía trước: không che thân
                var q = Flame(feet + new Vector2(U(-w, w), -U(0, 0.1f) * H), new Vector2(U(-40, 40), -U(520, 900) * manh), U(0.24f, 0.38f), 0.08f * H * manh,
                    (truoc ? 0.1f : 0.15f) * H * manh, "tron", "vtuoi", truoc ? Front : Back, 1.4f, -200, 1.6f, 0.05f, 0.05f);
                Tongue(q, 1, 0.1f);
                q.smokeGroup = Back;
            });
        }

        // ---------------------------------------------------------------- tên lửa

        // thân tên lửa vẽ theo hướng bay (aim): lửa phụt sát đuôi, hai vây đuôi sẫm, vỏ thép viền mực, đai sẫm giữa thân, mũi đỏ
        void RbVeTen(P z, float k, List<Item> buf)
        {
            float L = z.sz * Mathf.Min(1, 0.55f + z.age / 0.08f), W = 0.34f * L;
            var d = z.aim;
            var n = new Vector2(-d.y, d.x);
            float va = VelAng(d);
            int g = z.group;
            float fl = 0.8f + 0.35f * Mathf.Sin(z.age * 70 + z.seed * 1.7f), ta = TipAngle(-d);
            var duoi = z.pos - d * (0.5f * L);
            Put(buf, g, 24.6f, S("lobes_" + (z.seed & 3)), RbMuc, duoi - d * (0.45f * W * fl), 1.5f * W * fl + 4, 0.75f, ta);
            Put(buf, g, 24.7f, S("lobe_" + (z.seed & 3)), RbLuaNgoai, duoi - d * (0.45f * W * fl), 1.5f * W * fl, 0.75f, ta);
            Put(buf, g, 24.8f, S("lobe_" + ((z.seed + 1) & 3)), RbLuaTrong, duoi - d * (0.3f * W * fl), 0.9f * W * fl, 0.7f, ta);
            for (int s = -1; s <= 1; s += 2)
            {
                var fd = Unit(-d * 0.6f + n * (0.8f * s));
                var fp = z.pos - d * (0.3f * L) + n * (0.42f * W * s);
                float fa = TipAngle(fd);
                Put(buf, g, 25f, S("needles_0"), RbMuc, fp, 0.95f * W + 4, 0.6f, fa);
                Put(buf, g, 25.1f, S("needle_0"), RbThepSam, fp, 0.95f * W, 0.6f, fa);
            }
            Put(buf, g, 26f, S("solid_" + (z.seed & 3)), RbMuc, z.pos, W + 4, (L + 4) / (W + 4), va);
            Put(buf, g, 26.2f, S("blob_" + (z.seed & 3)), RbThep, z.pos, W, L / W, va);
            Put(buf, g, 26.3f, S("solid_" + ((z.seed + 2) & 3)), RbThepSam, z.pos - d * (0.12f * L), 0.95f * W, 0.32f, va);
            Put(buf, g, 26.4f, S("blob_" + ((z.seed + 1) & 3)), RbMui, z.pos + d * (0.3f * L), 0.86f * W, 1.35f, va);
        }

        // MỘT TÊN LỬA TẦM NHIỆT: rời `from` theo hướng `ax`, bay D giây theo đường cong ngẫu nhiên (Bézier bậc ba như TenNhiet), luôn tới đúng
        // `tgt`. L: dài thân (px sân)
        // 2026-11-18: đuôi là KHÓI CỤM LIỀN chia theo quãng bay (KR5), không còn chuỗi bóng; thua: bước giữa hai cụm khói (phần dài thân); doi: hệ
        // số đời khói (loạt tên lửa đông thì khói ngắn đời hơn cho đủ ngân sách hạt; 0: không khói, chỉ lửa phụt); to: hệ số cỡ cụm khói
        // khung vẽ sẵn (2026-11-19): có khung "khoi" thì doi nhân tần suất vệt khói (22 cụm/giây × doi), tan: tốc độ khung khói (cao = tan nhanh)
        void RbTen(Vector2 from, Vector2 ax, Vector2 tgt, float D, float L, float thua = 0.7f, float doi = 1f, float to = 1f, float tan = 2.4f)
        {
            float dist = Mathf.Max(60, (tgt - from).magnitude);
            // tầm vòng: không nhỏ hơn ~6 lần thân tên lửa, kể cả khi đối thủ đứng sát (vòng cung phải thấy rõ)
            float vong = Mathf.Max(dist, 6.5f * L);
            var p1 = from + ax * vong * U(0.55f, 0.95f);
            // điểm lái 2: lệch quanh đích, phần lớn phía trên (vòng lên rồi bổ xuống), đôi khi quặt ngang
            float a = U(0, 1) < 0.75f ? U(-2.8f, -0.35f) : U(-0.35f, 0.45f) + (U(0, 1) < 0.5f ? Mathf.PI : 0);
            var p2 = tgt + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * vong * U(0.35f, 0.7f);
            float ph = U(0, 6.28f), amp = U(5, 13), f = U(1.4f, 2.8f);

            Vector2 Pos(float x)
            {
                float s = x * (0.3f + 0.7f * x * x); // rời ống có tốc độ, hãm nhẹ lúc vòng, tăng tốc mạnh lúc lao vào đích
                float u = 1 - s;
                var b = u * u * u * from + 3 * u * u * s * p1 + 3 * u * s * s * p2 + s * s * s * tgt;
                var tg = Unit(3 * u * u * (p1 - from) + 6 * u * s * (p2 - p1) + 3 * s * s * (tgt - p2));
                return b + new Vector2(-tg.y, tg.x) * (amp * Mathf.Sin(ph + f * 6.28f * x) * (1 - x) * Mathf.Min(1, x * 6));
            }

            var h = new P { pos = from, life = D, group = Front, seed = rng.Next(4), sz = L, aim = ax };
            float dong = 0, quang = 0, buoc = thua * L;
            // khung vẽ sẵn (2026-11-19, người dùng: "tên lửa ... nên thêm trail smoke vào"): có khung "khoi" thì vệt khói đuôi FbKhoiDuoi (dưới)
            // thay chuỗi khói một múi, không để cả hai
            bool fbKhoi = doi > 0 && HasFb("khoi");
            var truoc = from;
            h.upd = (z, dt, s) =>
            {
                float x = Mathf.Clamp01(z.age / z.life);
                var now = Pos(x);
                z.aim = Unit(Pos(Mathf.Min(1, x + 0.015f)) - now);
                z.vel = Vector2.zero;
                z.pos = now;
                var duoi = now - z.aim * (0.55f * z.sz);
                // lửa phụt: lưỡi nhỏ, tắt nhanh (chỉ nối lửa đuôi với vệt khói)
                dong += dt * 30;
                while (dong >= 1)
                {
                    dong -= 1;
                    var q = s.Flame(duoi + s.U2(-1f, 1f), -z.aim * s.U(90, 170), s.U(0.06f, 0.1f), 0.16f * z.sz, 0.19f * z.sz, "tron", "lua", Front, 3, -40,
                        1.5f, 0, 0.01f);
                    q.sizeFn = (w, kk) => w.r1 * Mathf.Pow(1 - kk, 1.4f);
                }
                // khói cụm liền: mỗi `buoc` đường bay một cụm, đáy còn ánh lửa lúc mới sinh, tự nở, ngả xám, mờ
                var d0 = now - truoc;
                float m = d0.magnitude;
                if (m > 1e-3f && doi > 0 && !fbKhoi)
                {
                    var u = d0 / m;
                    float xq = buoc - quang;
                    int dem = 0;
                    while (xq <= m && dem++ < 10)
                    {
                        var at = truoc + u * xq - u * (0.55f * z.sz);
                        s.KmKhoi(at + s.U2(-1.5f, 1.5f), new Vector2(s.U(-8, 8), s.U(-22, -6)), s.U(0.3f, 0.38f) * z.sz * to, s.U(0.42f, 0.6f) * doi, Back, 0.7f, 0,
                            KmXam, 0, true);
                        xq += buoc;
                    }
                    quang = m - (xq - buoc);
                }
                truoc = now;
            };
            h.draw = RbVeTen;
            Add(h);
            // vệt khói đuôi: nhả ở đuôi lửa phụt (sau thân 0,6 dài), cụm cao 1,4 dài thân (~0,25 thân tướng; tên lửa nhỏ của Pháo Giáp nhỏ hơn),
            // 22 cụm/giây × doi cho liền (tên lửa bay ~700 đơn vị/giây), tan nhanh (tan) cho đủ ngân sách hạt; lớp 18 dưới lửa phụt và thân
            if (fbKhoi)
                FbKhoiDuoi(() => h.pos - h.aim * (0.6f * h.sz), () => !h.dead && h.age < h.life, 1.4f * L * to, 22 * doi, null, Front, 18, tan);
        }

        // phụt ở miệng ống lúc phóng: lửa, khói xám, tia (lửa đỏ cam thường)
        void RbPhut(Vector2 m, Vector2 ax, float manh)
        {
            var th0 = Th;
            Th = RbLuaTh;
            for (int i = 0; i < 3; i++)
            {
                var f = Flame(m + ax * U(2, 6), ax * U(160, 300) + U2(-40, 40), U(0.12f, 0.2f), 4 * manh, U(8, 11) * manh, "tron", "lua", Front, 4.5f, -100,
                    1.5f, 0, 0.05f);
                Tongue(f, 1, 0.1f);
            }
            for (int i = 0; i < 2; i++)
                KmKhoi(m - ax * U(0, 4), -ax * U(40, 90) + new Vector2(U(-30, 30), U(-10, 10)), U(12, 16) * manh, U(0.5f, 0.8f), Front, 0.6f, 0, KmXam, 0,
                    i == 0);
            for (int i = 0; i < 3; i++) KmTiaLua(m, ax + U2(-0.6f, 0.6f), U(320, 520), U(5, 7), KmLua[4]);
            Th = th0;
        }

        // nổ của một tên lửa ở chỗ chạm (cứ ba quả một quả nổ to hơn): nổ KR5 nhỏ lửa đỏ cam, lõi sau tướng (2026-11-18)
        void RbNoTen(Vector2 tgt, Vector2 feet, float tH, int j, float manh, float huong)
        {
            var th0 = Th;
            Th = RbLuaTh;
            bool to = j % 3 == 2;
            if (j > 0) KmNhip(to ? 0.6f : 0.4f);   // quả đầu là cú trúng chính (StageView), các quả sau: nhịp phụ
            Shake?.Invoke(to ? 0.24f : 0.13f);
            KmNo(tgt, new Vector2(tgt.x, feet.y), tH, (to ? 0.62f : 0.42f) * manh, "luat", huong);
            Th = th0;
        }

        // ---------------------------------------------------------------- ba đòn

        // ĐÒN THƯỜNG: tụ cầu năng lượng ở ổ nắm đấm tay phải hình rồi bắn. dang: 1 / 2. Trả giây tới lúc cầu chạm (= lead).
        public float NRobotBan(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.3f, lead), k = L0 / RbALead, T0 = T;
            var B = RbLay(dang);
            float manh = dang == 1 ? 0.85f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 O(float tc) => San(RbMau(B.ax, B.ay, tc));
            float R = Mathf.Clamp(0.1f * casterH, 9, 20) * manh;
            float tTu = RbATu * k, tBan = RbABan * k;
            float Rt(float tc) => R * (0.2f + 0.8f * Mathf.Sqrt(Mathf.Clamp01((tc - RbATu) / (RbABan - 0.08f - RbATu))));
            var tgt = foeBody + new Vector2(-dir * 0.06f * tH, -0.04f * tH);
            var S0 = O(RbABan);
            var d0 = Unit(tgt - S0);

            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - T0 - tBan) / Mathf.Max(0.04f, L0 - tBan));
                return Vector2.Lerp(S0, tgt, x * (0.75f + 0.25f * x)) + new Vector2(0, -0.05f * casterH) * Mathf.Sin(Mathf.PI * x);
            }

            Vector2 Tam(float t) => t - T0 < tBan ? O((t - T0) / k) : Bay(t);
            float Rr(float t) => t - T0 < tBan ? Rt((t - T0) / k) * KmNen(t - T0, tBan) : R;
            KmPal();

            // tụ (2026-11-18): cầu nhiều múi lớn dần theo nhịp đập trước ổ nắm đấm; vệt năng lượng XOẮN ỐC vào, nhanh dần, chạm vỏ cầu thì nhập
            // (dày dần tới lúc nhả); hai vòng co về cầu; lưỡi năng lượng liếm quanh; nén 1–2 khung rồi chớp lúc nhả
            At(tTu, () => RbCau(Tam, Rr, L0 - tTu));
            Every(tTu, tBan - 0.05f * k, x => 16 + 34 * x, x => RbHutXa(Tam, U(2.6f, 4.2f) * R, U(0.32f, 0.46f), U(6, 8), Front, Rr));
            Every(tTu + 0.08f * k, L0, x => 8 + 12 * x, x => RbLiem(Tam(T), Rr(T)));
            At(tTu + 0.3f * (tBan - tTu), () => KmVong(Tam, 0.26f, 3.2f * R, 0.9f * R, KmNang[3], 1, 0.75f));
            At(tTu + 0.65f * (tBan - tTu), () => KmVong(Tam, 0.22f, 2.8f * R, 0.9f * R, KmNang[4], 1, 0.8f));
            // đầy: tia toé quanh cầu
            At(Mathf.Max(tTu + 0.05f, tBan - 0.1f * k), () => RbTia(Tam(T), R, 6, 160, 280, 60));
            // bắn: chớp ở ổ, vòng bung, tia văng ngược bắn rồi khựng, rung nhẹ; tay giật lùi: hơi xì ở ổ
            At(tBan, () =>
            {
                Shake?.Invoke(0.12f);
                KmChop(S0, 2.6f * R, 0.07f, KmNang);
                RbVong(S0, 0.2f, R, 2.6f * R, RbNang[2]);
                for (int i = 0; i < 6; i++) KmTiaLua(S0, -d0 + U2(-0.8f, 0.8f), U(360, 600), U(5, 8), KmNang[4]);
            });
            At(tBan + 0.05f * k, () => RbHoiXi(O(RbABan + 0.05f), new Vector2(-dir, -0.3f).normalized, 0.8f * manh, 3));
            // bay: đuôi năng lượng LIỀN chia theo quãng bay (lưỡi co dần), tia
            At(tBan, () => KmDuoi(Bay, L0 - tBan, 0.45f * R, (p, u) =>
            {
                var q = Flame(p - u * R * 0.3f + U2(-0.25f, 0.25f) * R, -u * U(60, 140) + U2(-30, 30), U(0.14f, 0.22f), 0.7f * R, 0.8f * R, "tron", "vtuoi",
                    Front, 3, -60, 1.4f, 0, 0);
                q.sizeFn = (z, kk) => z.r1 * Mathf.Pow(1 - kk, 1.1f);
            }));
            Every(tBan, L0, 24, x => KmTiaLua(Bay(T), -d0 + U2(-0.6f, 0.6f), U(220, 380), U(5, 7), KmNang[3]));
            // khung vẽ sẵn (2026-11-19, người dùng: "các fireball ... nên thêm trail smoke vào"): vệt khói đuôi sau cầu (KmDuoiKhoi, HatFbKim.cs)
            At(tBan, () => KmDuoiKhoi(Bay, L0 - tBan, 2.4f * R, R, 18));
            // trúng: nổ KR5 năng lượng vàng tươi (chớp, lưỡi liềm trong khói, vòng cung, vệt cháy), bông va chạm theo hướng bay
            At(L0, () =>
            {
                Shake?.Invoke(0.25f * manh);
                KmBong(tgt - d0 * 0.06f * tH, -d0, 0.34f * tH * manh, 0.12f, KmNang);
                KmNo(tgt, new Vector2(tgt.x, foeFeet.y), tH, 0.55f * manh, "vtuoi", dir);
            });
            return L0;
        }

        // CHIÊU MANA: tụ cầu to giữa hai bàn tay giơ cao (lòng bàn tay xoay), vung đập ném xuống đỉnh đầu đối thủ. Trả giây tới lúc chạm (= lead).
        public float NRobotCau(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.5f, lead), k = L0 / RbCLead, T0 = T;
            var B = RbLay(dang);
            float manh = dang == 1 ? 0.85f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            float Tc(float t) => (t - T0) / k;
            Vector2 Giu(float tc) => San(RbMau(B.cx, B.cy, tc));
            Vector2 Tay(float tc) => San(RbMau(B.tx, B.ty, tc));
            Vector2 TayT(float tc) => San(RbMau(B.ux, B.uy, tc));
            float R = Mathf.Clamp(0.21f * casterH, 18, 42) * manh;
            const float tuC = 0.30f, dayC = 1.45f;
            float roiC = RbCNem - 0.08f; // đầu cú vung đập (T_NEM của rig): cầu rời tay ở dáng cao nhất
            float Rt(float tc) => R * (0.15f + 0.85f * Mathf.Sqrt(Mathf.Clamp01((tc - tuC) / (dayC - tuC))));
            float tRoi = roiC * k, tNo = L0;
            var dau = foeBody + new Vector2(-dir * 0.04f * tH, -0.3f * tH); // đỉnh đầu đối thủ
            var S0 = Giu(roiC);
            var Cc = new Vector2(S0.x + (dau.x - S0.x) * 0.4f, Mathf.Min(S0.y, dau.y) - 0.45f * casterH);

            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - T0 - tRoi) / Mathf.Max(0.05f, tNo - tRoi));
                float s = x * (0.4f + 0.6f * x), u = 1 - s;
                return u * u * S0 + 2 * u * s * Cc + s * s * dau;
            }

            Vector2 TamCau(float t) => t - T0 < tRoi ? Giu(Tc(t)) : Bay(t);
            float RCau(float t) => t - T0 < tRoi ? Rt(Tc(t)) * KmNen(t - T0, tRoi) : R;
            KmPal();

            // 1. tụ (2026-11-18): cầu nhiều múi lớn dần theo nhịp đập giữa hai bàn tay; vệt năng lượng XOẮN ỐC vào từ xa, nhanh dần, chạm vỏ cầu
            // thì nhập (dày dần tới lúc ném); lưỡi năng lượng liếm quanh; vòng co về cầu ở từng nhịp nạp; nén 1–2 khung rồi chớp lúc rời tay
            At(tuC * k, () => RbCau(TamCau, RCau, tNo - tuC * k));
            Every(tuC * k, tRoi - 0.05f * k, x => 14 + 40 * x, x => RbHutXa(TamCau, U(1.7f, 2.8f) * R, U(0.4f, 0.6f), U(7, 9), Front, RCau));
            Every((tuC + 0.15f) * k, tNo, x => 12 + 14 * x, x => RbLiem(TamCau(T), RCau(T)));
            // 2. hai lòng bàn tay xoay liên tục: xoáy cung điện ở mỗi lòng bàn tay + dải hạt từ lòng bàn tay cuốn vào cầu
            At(0.45f * k, () =>
            {
                RbXoay(t => Tay(Tc(t)), 0.34f * R, (roiC - 0.45f) * k, 1);
                RbXoay(t => TayT(Tc(t)), 0.34f * R, (roiC - 0.45f) * k, -1);
            });
            Every(0.5f * k, tRoi - 0.04f * k, x => 18 + 22 * x, x => RbHut(TamCau, (rng.Next(2) == 0 ? Tay(Tc(T)) : TayT(Tc(T))) + U2(-4, 4), U(0.3f, 0.45f),
                U(6, 8), Front, RCau));
            // 3. năng lượng nén xuống đất: sỏi bay lên, bụi xoáy quanh chân
            Every(0.55f * k, tRoi, 7, x => RbSoi(casterFeet + new Vector2(U(-0.5f, 0.5f) * casterH, U(-4, 2)), U(5, 9) * manh));
            Every(0.6f * k, tRoi, 6, x =>
            {
                float sd = rng.Next(2) == 0 ? -1 : 1;
                BuiTro(casterFeet + new Vector2(sd * U(0.1f, 0.45f) * casterH, U(-4, 2)), new Vector2(sd * U(40, 110), -U(5, 30)), U(0.5f, 0.8f), 4, U(8, 12),
                    Back);
            });
            // 4. ba nhịp nạp: vòng nở quanh cầu, tia toé; nhịp cuối (cầu đầy) chớp + rung
            float[] nhip = { 0.85f, 1.15f, dayC - 0.03f };
            for (int i = 0; i < nhip.Length; i++)
            {
                int ii = i;
                At(nhip[i] * k, () =>
                {
                    var c = TamCau(T);
                    float r = RCau(T);
                    KmVong(TamCau, 0.24f, (2.6f + 0.3f * ii) * r, 0.95f * r, KmNang[3 + (ii & 1)], 1, 0.8f);   // vòng co về cầu
                    RbTia(c, r, 4 + 2 * ii, 160, 300, 60);
                    if (ii == nhip.Length - 1)
                    {
                        Shake?.Invoke(0.15f);
                        KmChop(c, 1.6f * r, 0.07f, KmNang);
                    }
                });
            }
            // 5. vung đập: cầu rời tay (vòng, tia), vọt lên rồi cắm xuống đầu đối thủ; đuôi năng lượng, tia
            At(tRoi, () =>
            {
                Shake?.Invoke(0.2f);
                KmChop(S0, 1.5f * R, 0.07f, KmNang);
                RbVong(S0, 0.22f, R, 2.2f * R, RbNang[2]);
                RbTia(S0, R, 8, 220, 380);
            });
            // đuôi năng lượng LIỀN chia theo quãng bay (KR5), tia bắn rồi khựng
            At(tRoi, () => KmDuoi(Bay, tNo - tRoi, 0.4f * R, (pt, ud) =>
            {
                var q = Flame(pt - ud * R * 0.3f + U2(-0.35f, 0.35f) * R, -ud * U(60, 140) + U2(-40, 40), U(0.18f, 0.28f), 0.7f * R, 0.8f * R, "tron", "vtuoi",
                    Front, 3, -100, 1.4f, 0, 0);
                q.sizeFn = (z, kk) => z.r1 * Mathf.Pow(1 - kk, 1.1f);
            }));
            Every(tRoi, tNo, 26, x =>
            {
                var c = Bay(T);
                KmTiaLua(c, -Unit(Bay(T + 0.02f) - c) + U2(-0.7f, 0.7f), U(240, 420), U(5, 7), KmNang[3]);
            });
            // khung vẽ sẵn (2026-11-19): vệt khói đuôi sau cầu to (KmDuoiKhoi), cụm tối đa 0,3 thân đối thủ
            At(tRoi, () => KmDuoiKhoi(Bay, tNo - tRoi, Mathf.Min(1.4f * R, 0.3f * tH), 0.9f * R, 22));
            // 6. chạm: chớp, nổ vàng rất lớn, cột năng lượng phụt lên, sóng đất hai đợt, nứt đất, đá văng, bụi, khói
            var tam = foeBody + new Vector2(-dir * 0.04f * tH, -0.12f * tH);
            // 2026-11-18: nổ KR5 (chớp 2 khung → lưỡi liềm vàng trong khối khói hai tông → khói tách cụm bay lên), lõi sau lưng đối thủ, bông va
            // chạm ở đỉnh đầu theo hướng cầu cắm xuống; trước đây chớp 1,3 thân + cầu lửa CauNo trùm kín đối thủ
            At(tNo, () =>
            {
                Shake?.Invoke(0.6f * manh);
                KmBong(dau, Unit(dau - Cc), 0.5f * tH * manh, 0.14f, KmNang);
                KmNo(tam, foeFeet, tH, 1.6f * manh, "vtuoi", dir);
                RbCot(foeFeet, tH, 0.3f, manh);
                KmCung(foeFeet + new Vector2(0, 2), 0.15f * tH, 1.3f * tH * manh, 0.5f, KmNang[3], 0.3f, Floor, 30.6f, 0.8f);
                RbNut(foeFeet + new Vector2(0, 2), tH * manh);
                BuiDap(foeFeet, tH, 1.3f * manh, 10);
                for (int i = 0; i < 4; i++)
                    Rock(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, -6), new Vector2(U(-300, 300), -U(320, 600)), foeFeet.y + U(-4, 8), U(9, 15) * manh);
            });
            At(tNo + 0.14f, () =>
            {
                Shake?.Invoke(0.3f * manh);
                KmNhip(0.4f);
                KmCung(foeFeet + new Vector2(0, 2), 0.3f * tH, 1.7f * tH * manh, 0.55f, KmNang[4], 0.3f, Floor, 30.6f, 0.7f);
                KmNo(tam + new Vector2(dir * U(4, 18), U(-24, 4)), foeFeet, tH, 0.7f * manh, "vtuoi", dir);
            });
            At(tNo + 0.36f, () =>
            {
                for (int i = 0; i < 2; i++)
                    KmKhoi(foeBody + new Vector2(U(-0.25f, 0.25f) * tH, -U(0.15f, 0.45f) * tH), new Vector2(U(-20, 20), -U(40, 70)), U(0.13f, 0.17f) * tH,
                        U(1.0f, 1.3f), Back, 0, 2);
                for (int i = 0; i < 4; i++) Ash(foeBody + U2(-28, 28));
            });
            return L0;
        }

        // CHIÊU CUỐI: mở giáp ngực, phóng 7 tên lửa tầm nhiệt từ lõi lục giác. Trả giây tới lúc quả đầu chạm đối thủ (= lead).
        public float NRobotTen(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.3f, lead), k = L0 / RbSLead, T0 = T;
            var B = RbLay(dang);
            float manh = dang == 1 ? 0.8f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 Loi(float tc) => San(RbMau(B.lx, B.ly, tc));
            float Lt = Mathf.Clamp(0.2f * casterH, 20, 40) * manh; // dài thân tên lửa
            int n = Mathf.Min(RbSPhong.Length, B.ox.Length);

            // 1. giáp ngực mở: hơi xì hai bên khe ngực; mở hết: vòng nháy ở lõi; lõi nóng: than vàng bốc lên tới hết loạt phóng
            At(Mathf.Max(0.02f, (RbSMo + 0.03f) * k), () =>
            {
                var c = Loi(RbSMo + 0.03f);
                Shake?.Invoke(0.08f);
                for (int s = -1; s <= 1; s += 2)
                    RbHoiXi(c + new Vector2(s * 0.07f * casterH, -0.02f * casterH), new Vector2(s, -0.25f).normalized, manh);
            });
            At(0.45f * k, () =>
            {
                var c = Loi(0.45f);
                RbVong(c, 0.22f, 0.03f * casterH, 0.13f * casterH * manh, RbNang[1]);
                RbTia(c, 0.04f * casterH, 6, 140, 260, 100);
            });
            Every(0.45f * k, (RbSPhong[n - 1] + 0.1f) * k, 4, x =>
            {
                var c = Loi((T - T0) / k);
                KmDomCum(c + U2(-0.04f, 0.04f) * casterH, new Vector2(U(-20, 20), -U(60, 110)), KmNang[3], Front, rng.Next(3, 5));   // cụm đốm nhỏ
            });

            // 2. loạt phóng: mỗi quả rời đúng ống, đúng giờ `phong` của clip; quả đầu chạm đúng khung trúng
            float tCuoi = 0, bay0 = (RbSLead - RbSPhong[0]) * k;
            for (int i = 0; i < n; i++)
            {
                int j = i;
                float ts = RbSPhong[j] * k;
                var o = new Vector2(B.ox[j], B.oy[j]);
                var hh = new Vector2(B.hx[j], B.hy[j]);
                // hướng phóng: chủ yếu lên trời, toả theo chỗ ống trên lõi, hơi về phía đối thủ (y sân đi xuống)
                var ax = Unit(new Vector2(dir * (0.85f * hh.x + 0.3f), -(0.55f * hh.y + 1.1f)));
                float D = j == 0 ? bay0 : bay0 + U(0.02f, 0.24f);
                var tgt = j == n - 1 ? foeBody + new Vector2(-dir * 0.05f * tH, 0) : foeBody + new Vector2(-dir * U(0f, 0.16f) * tH, U(-0.3f, 0.2f) * tH);
                At(ts, () =>
                {
                    var m = San(o);
                    Shake?.Invoke(0.06f);
                    RbPhut(m, ax, manh);
                    RbTen(m, ax, tgt, D, Lt);
                });
                float tNo = ts + D;
                tCuoi = Mathf.Max(tCuoi, tNo);
                At(tNo, () => RbNoTen(tgt, foeFeet, tH, j, manh, dir));
            }

            // 3. sau quả cuối: nổ rất lớn ba đợt (lửa đỏ cam), sóng đất, bụi, đá, khói và tro
            float tKet = tCuoi + 0.07f;
            var giua = foeBody + new Vector2(-dir * 0.05f * tH, 0);
            // 2026-11-18: ba đợt nổ KR5 lửa đỏ cam (lõi sau lưng đối thủ, khói hai tông tách cụm bay lên, vòng cung dẹt, vệt cháy)
            At(tKet, () =>
            {
                var th0 = Th;
                Th = RbLuaTh;
                Shake?.Invoke(0.55f * manh);
                KmNhip(0.9f);
                KmNo(giua, foeFeet, tH, 1.55f * manh, "luat", dir);
                KmCung(foeFeet + new Vector2(0, 2), 0.2f * tH, 1.2f * tH * manh, 0.5f, KmLua[4], 0.3f, Floor, 30.6f, 0.75f);
                BuiDap(foeFeet, tH, 1.2f * manh, 10);
                for (int i = 0; i < 3; i++)
                    Rock(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, -6), new Vector2(U(-260, 260), -U(300, 560)), foeFeet.y + U(-4, 6), U(9, 14) * manh);
                Th = th0;
            });
            At(tKet + 0.12f, () =>
            {
                var th0 = Th;
                Th = RbLuaTh;
                Shake?.Invoke(0.35f * manh);
                KmNhip(0.4f);
                KmNo(giua + new Vector2(dir * U(6, 22), U(-30, -6)), foeFeet, tH, 0.8f * manh, "luat", dir);
                Th = th0;
            });
            At(tKet + 0.24f, () =>
            {
                var th0 = Th;
                Th = RbLuaTh;
                KmNo(giua + new Vector2(-dir * U(4, 18), U(4, 20)), foeFeet, tH, 0.6f * manh, "luat", dir);
                Th = th0;
            });
            At(tKet + 0.4f, () =>
            {
                for (int i = 0; i < 2; i++)
                    KmKhoi(foeBody + new Vector2(U(-0.25f, 0.25f) * tH, -U(0.2f, 0.5f) * tH), new Vector2(U(-20, 20), -U(40, 70)), U(0.14f, 0.18f) * tH,
                        U(1.0f, 1.3f), Back, 0, 2);
                for (int i = 0; i < 5; i++) Ash(foeBody + U2(-30, 30));
            });

            // 4. khép ngực: hơi xì
            At(RbSDong * k, () =>
            {
                var c = Loi(RbSDong);
                for (int s = -1; s <= 1; s += 2)
                    RbHoiXi(c + new Vector2(s * 0.06f * casterH, -0.02f * casterH), new Vector2(s, -0.4f).normalized, 0.8f * manh, 2);
            });
            return L0;
        }
    }
}
