// Bộ KHỦNG LONG NÚI LỬA (Hỏa Sơn Long, 2026-11-14/15, final boss đảo Hỏa, suất lan_hoa; rig ArtGen/Spine/nui_lua_rig.py trên rig
// monster_3654; ba dạng: 1 = con non chibi nui_lua_non, 2 = thiếu niên (tạm dùng rig dạng 3), 3 = boss hai sừng nui_lua_1).
// Người dùng: đánh thường "lao vào húc đối thủ"; chiêu mana "há mồm ra tụ 1 quả cầu lửa rồi bắn"; chiêu cuối "bẻ các đỉnh núi lửa trên lưng
// theo các hướng khác nhau, bắn ra các viên đạn lửa bay kiểu vòng cung random nhưng vẫn lao vào người đối thủ kiểu homing missile (đạn bay
// thế nào là làm bằng code)"; "final boss, thật đẹp, hoành tráng, impact, thêm fx khói ở đỉnh các núi lửa" (khói đứng nằm trong rig, clip aura).
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc: phát từ đầu clip, biết `lead` = giờ tới khung trúng của clip).
// - n_nui_huc (đòn thường, tướng lao tới): bụi đá lúc bật khỏi chỗ; đầu húc trúng: chớp toé, tia lửa và dăm đá bazan văng hai bên, giọt dung
//   nham văng, bụi dưới chân đối thủ bị ép ra, rung mạnh.
// - n_nui_cau (chiêu mana): than hồng hút vào mồm từ xa, cầu lửa lớn dần giữa hai hàm trong lúc tướng ngẩng đầu há mồm (clip cast: tu 0,30 →
//   nha 1,05); cầu đầy thì nháy vòng; khung nhả: chớp ở mõm, các ống trên lưng phụt khói theo cú giật; cầu bay có đuôi lửa, khói; nổ lớn,
//   giọt dung nham văng ra rơi xuống đất.
// - n_nui_ten (chiêu cuối): lúc gồng than hồng bốc lên từ các ống dày dần; khung dộng xuống (be 1,52): vòng bụi, dăm đá, rung; rồi 16 phát
//   bắn theo đúng thứ tự và giờ của clip (sự kiện `ban`, cách 0,07 s): mỗi phát miệng ống đó phụt lửa + khói, một ĐẠN TẦM NHIỆT rời miệng ống
//   theo hướng ống, bay đường cong NGẪU NHIÊN (Bézier bậc ba: điểm lái 1 dọc trục ống, điểm lái 2 lệch ngẫu nhiên quanh đích, thêm lắc ngang
//   tắt dần) và tăng tốc lao vào đối thủ; mỗi viên nổ nhỏ, viên cuối nổ lớn. Đường bay là mã, đích cố định lúc phát chiêu.
// Chỗ miệng ống lúc bắn và hướng ống đo trên rig đã xuất (phần của chiều cao game, x về phía trước, y lên; độ, 0 = phía trước, 90 = lên):
// đổi clip skill hay hình thì đo lại bằng ArtGen/Spine/inbox/nui_lua_1/_do_hat.py (dạng 1: NL_DANG=chibi).
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // mốc giờ của clip (nui_lua_rig.py): skill bẻ ống 1,52 s, phát đầu 1,62 s (khung trúng của clip), mỗi phát cách 0,07 s; cast tụ 0,75 s
        const float NuiBe = 1.52f, NuiBan0 = 1.62f, NuiBanCach = 0.07f, NuiTu = 0.75f;
        public const float NuiCauBay = 0.34f; // giây cầu lửa bay từ mồm tới đối thủ
        const float NuiTenBay = 0.62f;        // giây bay ngắn nhất của một đạn tầm nhiệt (mỗi viên cộng thêm 0..0,2 s)

        // miệng ống ở từng phát, theo thứ tự bắn (BAN trong nui_lua_rig.py: 09 14 02 10 13 15 03 09 04 02 14 10 01 13 06 09)
        static readonly Vector2[] NuiOngP =
        {
            new Vector2(-0.534f, 0.609f), new Vector2(0.568f, 0.437f), new Vector2(-0.320f, 0.546f), new Vector2(-0.726f, 0.543f),
            new Vector2(0.608f, 0.141f), new Vector2(0.146f, 0.704f), new Vector2(-0.319f, 0.544f), new Vector2(-0.566f, 0.644f),
            new Vector2(-0.450f, 0.485f), new Vector2(-0.300f, 0.579f), new Vector2(0.588f, 0.435f), new Vector2(-0.716f, 0.571f),
            new Vector2(0.019f, 0.330f), new Vector2(0.614f, 0.214f), new Vector2(-0.469f, 0.503f), new Vector2(-0.500f, 0.711f),
        };
        static readonly float[] NuiOngG = { 140, 27, 126, 153, 1, 80, 120, 143, 116, 122, 18, 152, 38, 3, 109, 134 };
        // miệng tám ống lớn ở dáng đứng (09 10 02 14 15 13 01 03): chỗ than hồng bốc lên lúc gồng, chỗ phụt khói lúc nhả cầu
        static readonly Vector2[] NuiOngDung =
        {
            new Vector2(-0.279f, 0.986f), new Vector2(-0.442f, 0.931f), new Vector2(-0.018f, 0.773f), new Vector2(0.372f, 0.920f),
            new Vector2(0.161f, 0.975f), new Vector2(0.434f, 0.759f), new Vector2(0.012f, 0.448f), new Vector2(-0.315f, 0.664f),
            new Vector2(0.005f, 0.893f),   // miệng núi lửa CHÍNH trên đỉnh lưng (xương ong_cc; thiết kế "sừng", đo trên rig da mình 2026-11-14 17:35)
        };

        // DẠNG 1 (con non chibi, nui_lua_non): 8 phát từ núi lửa chính và ba ống nhỏ (cc 09 14 02 cc 09 14 02); đo lại 2026-11-15 sau khi
        // mỗi tháp ống quay quanh chân của chính nó
        static readonly Vector2[] NuiOngP1 =
        {
            new Vector2(-0.119f, 0.661f), new Vector2(-0.645f, 0.544f), new Vector2(0.235f, 0.708f), new Vector2(-0.477f, 0.332f),
            new Vector2(-0.114f, 0.711f), new Vector2(-0.659f, 0.552f), new Vector2(0.259f, 0.728f), new Vector2(-0.446f, 0.376f),
        };
        static readonly float[] NuiOngG1 = { 87, 145, 62, 162, 86, 151, 57, 155 };
        static readonly Vector2[] NuiOngDung1 =
        {
            new Vector2(-0.115f, 0.966f), new Vector2(-0.444f, 0.774f), new Vector2(-0.260f, 0.622f), new Vector2(0.196f, 0.885f),
        };

        // DẠNG 2 (thiếu niên, nui_lua_2): 12 phát từ núi lửa chính và năm tháp ống (cc 10 14 09 13 02, hai vòng); đo 2026-11-15
        static readonly Vector2[] NuiOngP2 =
        {
            new Vector2(0.061f, 0.629f), new Vector2(-0.753f, 0.682f), new Vector2(0.413f, 0.653f), new Vector2(-0.477f, 0.656f),
            new Vector2(0.630f, 0.509f), new Vector2(-0.397f, 0.393f), new Vector2(0.061f, 0.678f), new Vector2(-0.749f, 0.705f),
            new Vector2(0.463f, 0.653f), new Vector2(-0.495f, 0.685f), new Vector2(0.631f, 0.545f), new Vector2(-0.364f, 0.438f),
        };
        static readonly float[] NuiOngG2 = { 86, 146, 69, 139, 42, 162, 86, 147, 59, 141, 52, 151 };
        static readonly Vector2[] NuiOngDung2 =
        {
            new Vector2(0.059f, 0.908f), new Vector2(-0.455f, 0.954f), new Vector2(-0.249f, 0.890f), new Vector2(-0.216f, 0.648f),
            new Vector2(0.367f, 0.814f), new Vector2(0.530f, 0.703f),
        };

        static readonly Color BazanC = C(112, 93, 104), BazanC2 = C(54, 50, 60); // dăm đá bazan: màu đá của da mình sau khi cân màu (bản "sừng")

        void DaBazan(Vector2 pos, Vector2 vel, float life, float r, int group = Front)
        {
            if (!HasGai)
            {
                Extra(pos, 1, vel.magnitude, group);
                return;
            }
            var q = Shard(pos, vel, life, r, 860, 1.4f, group);
            q.col = (q.seed & 4) != 0 ? BazanC2 : BazanC;
        }

        // lửa phụt ở miệng một ống theo hướng ống + một cụm khói nhỏ (y sân đi xuống); sc: cỡ. 2026-11-18: bớt hạt (16 phát × 6 ống), khói thành cụm
        void OngPhut(Vector2 mieng, Vector2 ax, float sc)
        {
            for (int j = 0; j < 2; j++)
                HoaLuoi(Flame(mieng + ax * U(2, 8), ax * U(220, 380) * sc + U2(-40, 40), U(0.16f, 0.24f), 5 * sc, U(10, 14) * sc, "tron", Th.pal, Front,
                    4.5f, -120, 1.5f, 0, 0), 1, 0.1f, 0);
            HoaKhoi(mieng + ax * U(4, 12), U(9, 12) * sc, Back, ax * U(60, 120) * sc + new Vector2(U(-15, 15), -U(20, 40)), U(0.55f, 0.8f), false, 0.6f);
            Spark(mieng, ax + U2(-0.5f, 0.5f), U(220, 360), 0, 6);
        }

        // MỘT ĐẠN TẦM NHIỆT: rời `from` theo hướng `ax`, bay D giây theo đường cong ngẫu nhiên, luôn tới đúng `tgt`. r: bán kính đầu đạn.
        void TenNhiet(Vector2 from, Vector2 ax, Vector2 tgt, float D, float r)
        {
            float dist = Mathf.Max(40, (tgt - from).magnitude);
            // điểm lái 1: dọc trục ống (đạn phóng ra theo hướng ống, kể cả khi ống chĩa ngược phía đối thủ)
            var p1 = from + ax * dist * U(0.32f, 0.58f);
            // điểm lái 2: lệch quanh đích, phần lớn ở phía trên (đạn vòng lên rồi cắm xuống), đôi khi quặt ngang
            float a = U(0, 1) < 0.8f ? U(-2.75f, -0.4f) : U(-0.4f, 0.5f) + (U(0, 1) < 0.5f ? Mathf.PI : 0);
            var p2 = tgt + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * dist * U(0.22f, 0.5f);
            float ph = U(0, 6.28f), amp = U(4, 11), f = U(1.6f, 3.2f);

            Vector2 Pos(float x)
            {
                float s = x * (0.3f + 0.7f * x * x); // rời ống có tốc độ, hãm nhẹ lúc vòng, tăng tốc mạnh lúc lao vào đích
                float u = 1 - s;
                var b = u * u * u * from + 3 * u * u * s * p1 + 3 * u * s * s * p2 + s * s * s * tgt;
                var tg = Unit(3 * u * u * (p1 - from) + 6 * u * s * (p2 - p1) + 3 * s * s * (tgt - p2));
                return b + new Vector2(-tg.y, tg.x) * (amp * Mathf.Sin(ph + f * 6.28f * x) * (1 - x) * Mathf.Min(1, x * 6));
            }

            var h = new P { pos = from, life = D, group = Front, seed = rng.Next(4), r0 = r, pal = Th.pal, aim = ax };
            float dong = 0;
            int dem = 0;
            h.upd = (z, dt, s) =>
            {
                float x = Mathf.Clamp01(z.age / z.life);
                var now = Pos(x);
                z.aim = Unit(Pos(Mathf.Min(1, x + 0.02f)) - now);
                z.vel = Vector2.zero;
                z.pos = now;
                // đuôi: lưỡi lửa chữ S co dần (đứng tại chỗ, nguội dần), cứ năm lưỡi một cụm khói nhỏ, thỉnh thoảng tia văng (2026-11-18: bớt hạt, 16 viên)
                dong += dt * 22;
                while (dong >= 1)
                {
                    dong -= 1;
                    dem++;
                    var q = s.Flame(now - z.aim * z.r0 * 0.5f + s.U2(-0.3f, 0.3f) * z.r0, -z.aim * s.U(40, 110) + new Vector2(0, -20), s.U(0.16f, 0.24f),
                        z.r0 * 0.95f, z.r0 * 0.95f, "tron", z.pal, (dem & 1) == 0 ? Front : Back, 3, -140, 1.4f, 0, 0);
                    s.HoaLuoi(q, 1, 0.2f, 0);
                    q.sizeFn = (w, k) => w.r1 * Mathf.Pow(1 - k, 1.1f);
                    if (dem % 6 == 0)
                        s.HoaKhoi(now - z.aim * z.r0 * 1.4f, z.r0 * 1.3f, Back, new Vector2(s.U(-12, 12), s.U(-34, -14)), s.U(0.45f, 0.65f), false, 0.7f);
                    if (dem % 7 == 0) s.Spark(now, -z.aim + s.U2(-0.6f, 0.6f), s.U(140, 240), 0, 6);
                }
            };
            // đầu đạn: một khối lửa dẹt theo hướng bay, viền mực + bốn lớp màu từ ngoài vào lõi (một hạt); ảnh khối lửa nhiều múi kr_luakhoi đổi dáng mỗi
            // 2 khung khi đã nhập, chưa có thì khối tròn cũ
            h.draw = (z, k, buf) =>
            {
                var cols = Pal.TryGetValue(z.pal, out var pc) ? pc : Pal["lua"];
                float va = VelAng(z.aim), rad = z.r0 * (0.55f + 0.45f * Mathf.Min(1, k / 0.1f));
                int fr = (z.seed + (int)(z.age * 15)) & 3;
                bool kr = S("kr_luakhoi_0");
                Put(buf, z.group, 26, kr ? S("kr_luakhois_" + fr) : S("solid_" + (z.seed & 3)), Ink, z.pos, 2 * rad + (kr ? 3 : 5), 1.5f, va);
                for (int i = 0; i < 4; i++)
                    Put(buf, z.group, 27 + i, kr ? S("kr_luakhoi_" + fr) : S("blob_" + (z.seed & 3)), cols[i], z.pos + z.aim * (rad * 0.14f * i), 2 * rad * LobeF[i + 1],
                        1.5f - 0.12f * i, va);
            };
            Add(h);
        }

        // nổ nhỏ gọn cho loạt đạn tầm nhiệt (16 viên trong khoảng 1 s, giữ ngân sách hạt): chớp, ba lưỡi liềm, hai tia, cụm tàn lửa nhỏ
        void HoaNoNho(Vector2 c, float tH, float manh)
        {
            HoaChop(c, 0.24f * tH * manh, 0.08f);
            for (int i = 0; i < 3; i++)
            {
                float a = 6.28f * (i + U(-0.25f, 0.25f)) / 3;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.85f);
                var q = Flame(c + d * 3, d * U(200, 300), U(0.2f, 0.28f), 5, U(10, 13) * manh, "liem", Th.pal, Front, 8, -50, 1.5f, 0, 0);
                q.aim = d;
                q.sizeFn = HoaLiemCo;
            }
            for (int i = 0; i < 2; i++) Spark(c, U2(-1, 1), U(260, 400), 0, 6);
            HoaTan(c, new Vector2(U(-40, 40), -U(80, 130)), 0, 2);
        }

        // ĐẠN TẦM NHIỆT TỪ CÁC ỐNG NÚI LỬA (chiêu cuối). lead: giây từ đầu clip skill tới phát bắn đầu. Trả giây tới lúc viên đầu chạm đối thủ.
        // dang: 1 = con non (8 phát, nổ nhẹ hơn), 2 = thiếu niên (12 phát), còn lại = dạng lớn (16 phát)
        public float NNuiTen(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 3)
        {
            var NuiOngP = dang == 1 ? NuiOngP1 : dang == 2 ? NuiOngP2 : HatLua.NuiOngP;
            var NuiOngG = dang == 1 ? NuiOngG1 : dang == 2 ? NuiOngG2 : HatLua.NuiOngG;
            var NuiOngDung = dang == 1 ? NuiOngDung1 : dang == 2 ? NuiOngDung2 : HatLua.NuiOngDung;
            float manh = dang == 1 ? 0.78f : dang == 2 ? 0.9f : 1f;
            float L = Mathf.Max(0.5f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t00 = L - NuiBan0; // giờ (tính từ lúc gọi) của giây 0 clip
            Vector2 Rig(Vector2 p) => casterFeet + new Vector2(dir * p.x, -p.y) * casterH;
            int n = NuiOngP.Length;
            float r = Mathf.Clamp(0.05f * casterH, 6, 11);

            // gồng: than hồng bốc lên từ miệng các ống, dày dần; khói đậm hơn ở nhịp gồng thứ hai
            float tG0 = Mathf.Max(0.02f, t00 + 0.1f), tBe = Mathf.Max(tG0 + 0.1f, t00 + NuiBe);
            Every(tG0, tBe, x => 4 + 12 * x * x, x =>
            {
                var o = Rig(NuiOngDung[rng.Next(NuiOngDung.Length)]) + new Vector2(0, 0.06f * casterH * x); // thân rạp dần
                HoaTan(o + U2(-6, 6), new Vector2(U(-30, 30), -U(90, 190) * (0.6f + x)), U(0.5f, 0.9f), 3, U(0, 1) < 0.5f ? Back : Front); // cụm tàn lửa
            });
            Every(Mathf.Max(tG0, t00 + 0.75f), tBe, 4, x =>
                HoaKhoi(Rig(NuiOngDung[rng.Next(NuiOngDung.Length)]) + new Vector2(0, 0.08f * casterH), U(11, 15), Back, new Vector2(U(-20, 20), -U(60, 110)),
                    U(0.7f, 1.0f), false, 0.5f));

            // dộng xuống, bẻ ống: vòng bụi, bụi đá hai bên, dăm đá bật lên, rung
            At(tBe, () =>
            {
                Shake?.Invoke(0.5f);
                BuiDap(casterFeet, casterH, 1.35f * manh, 12);
                for (int i = 0; i < 7; i++)
                    DaBazan(casterFeet + new Vector2(U(-0.45f, 0.45f) * casterH, -4), new Vector2(U(-220, 220), -U(200, 380)), U(0.45f, 0.7f), U(3.4f, 5.4f));
            });

            // loạt bắn
            float tDau = 0, tCuoi = 0;
            for (int i = 0; i < n; i++)
            {
                int k = i;
                float ts = L + k * NuiBanCach;
                float D = NuiTenBay + U(0, 0.2f);
                float g = NuiOngG[k] * Mathf.Deg2Rad;
                var ax = new Vector2(dir * Mathf.Cos(g), -Mathf.Sin(g));
                // mỗi viên một chỗ chạm riêng trên thân đối thủ; viên cuối vào giữa thân
                var tgt = k == n - 1 ? foeBody + new Vector2(-dir * 0.06f * tH, 0)
                    : foeBody + new Vector2(-dir * U(0.02f, 0.14f) * tH, U(-0.3f, 0.22f) * tH);
                At(ts, () =>
                {
                    var m = Rig(NuiOngP[k]);
                    Shake?.Invoke(0.07f);
                    OngPhut(m, ax, 1f);
                    TenNhiet(m + ax * r, ax, tgt, D, r);
                });
                float tNo = ts + D;
                if (k == 0) tDau = tNo;
                tCuoi = Mathf.Max(tCuoi, tNo);
                if (k < n - 1)
                    At(tNo, () =>
                    {
                        Shake?.Invoke(k % 4 == 3 ? 0.26f : 0.12f);
                        NuocPulse?.Invoke(k % 4 == 3 ? 0.5f : 0.25f);
                        if (k % 4 == 3) HoaNo(tgt, 0.55f * manh, tH);
                        else HoaNoNho(tgt, tH, manh);
                        if (k % 2 == 0) LavaDrop(tgt, new Vector2(U(-200, 200), -U(160, 320)), U(3.5f, 5), foeFeet.y, U(0, 1) < 0.5f ? Back : Front);
                    });
            }

            // viên cuối cùng tới sau mọi viên khác: nổ lớn, vòng lửa, giọt dung nham, khói và tro
            float tKet = tCuoi + 0.06f;
            var giua = foeBody + new Vector2(-dir * 0.06f * tH, 0);
            At(tKet, () =>
            {
                NuocPulse?.Invoke(1f);
                HoaCauNo(giua, foeFeet, tH, dir, 1.5f * manh);
                for (int j = 0; j < 6; j++) LavaDrop(giua + U2(-8, 8), new Vector2(U(-280, 280), -U(220, 420)), U(4, 6), foeFeet.y, Front);
                for (int j = 0; j < 6; j++)
                {
                    float a = 6.28f * (j + U(0, 0.8f)) / 6;
                    DaBazan(giua, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f) * U(240, 440), U(0.5f, 0.8f), U(3.4f, 5.4f));
                }
            });
            At(tKet + 0.13f, () =>
            {
                Shake?.Invoke(0.35f);
                HoaNo(giua + new Vector2(dir * U(4, 20), U(-26, 6)), 0.75f, tH);
            });
            At(tKet + 0.34f, () =>
            {
                for (int i = 0; i < 3; i++)
                    HoaKhoi(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.15f, 0.5f) * tH), U(0.14f, 0.18f) * tH, Back, null, 0, true, 0.5f);
                for (int i = 0; i < 4; i++) Ash(foeBody + U2(-28, 28));
            });
            return tDau;
        }

        // CẦU LỬA Ở MỒM (chiêu mana). mouth: chỗ nhả ở khung trúng của clip cast (game.muzzle = xương `mieng`). Trả giây tới lúc chạm.
        public float NNuiCau(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang = 3)
        {
            var NuiOngDung = dang == 1 ? NuiOngDung1 : dang == 2 ? NuiOngDung2 : HatLua.NuiOngDung;
            float L = Mathf.Max(0.3f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.02f, L - NuiTu), goc = T;
            float R = Mathf.Clamp(0.16f * casterH, 14, 30);
            Vector2 Rig(Vector2 p) => casterFeet + new Vector2(dir * p.x, -p.y) * casterH;
            var tam = mouth + new Vector2(dir * 0.35f, 0.05f) * R;

            // tụ (2026-11-18, người dùng chê pha hút quanh cầu): vệt lửa xoắn ốc hút vào mồm nhanh dần, hai vòng co, cầu nhiều múi lớn dần giữa hai hàm
            // theo nhịp đập, nén rồi chớp lúc nhả; lưỡi lửa liếm quanh cầu
            var rt = HoaTuCau(t => tam, R, t0 + 0.04f, L, true, 1.2f);
            Every(t0 + 0.14f, L, x => 10 + 12 * x, x =>
            {
                float r = rt(T), a = U(0, 6.28f);
                var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                HoaLuoi(Flame(tam + o * r * 0.5f, o * U(20, 70) + new Vector2(0, -U(40, 90)), U(0.18f, 0.28f), r * 0.34f, r * 0.56f, "tron", Th.pal, Front,
                    3, -160, 1.5f, 0, 0), 1, 0.5f, 0);
            });
            // cầu đầy (0,12 s trước khi nhả): toé tia
            At(Mathf.Max(t0 + 0.1f, L - 0.12f), () =>
            {
                Shake?.Invoke(0.1f);
                for (int j = 0; j < 5; j++)
                {
                    float a = 6.28f * (j + U(0, 0.7f)) / 5;
                    var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Spark(tam + o * R, o, U(200, 340), 0, 6, 120);
                }
            });

            // nhả: chớp ở mõm (HoaTuCau), các ống trên lưng phụt lửa + khói theo cú giật, bụi dưới chân trượt lùi
            var tgt = foeBody + new Vector2(-dir * 0.06f * tH, 0);
            var d0 = Unit(tgt - tam);
            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - goc - L) / NuiCauBay);
                return tam + (tgt - tam) * (x * (0.5f + 0.5f * x)) + new Vector2(0, -0.08f * casterH) * Mathf.Sin(Mathf.PI * x);
            }
            At(L, () =>
            {
                Shake?.Invoke(0.3f);
                for (int j = 0; j < 5; j++) Spark(tam, -d0 + U2(-0.8f, 0.8f), U(220, 380), 0, 6);
                for (int i = 0; i < Mathf.Min(6, NuiOngDung.Length); i++)
                    OngPhut(Rig(NuiOngDung[i]), new Vector2(-dir * U(0.05f, 0.35f), -1).normalized, 0.8f);
                for (int i = 0; i < 6; i++)
                    BuiTro(casterFeet + new Vector2(dir * U(-0.1f, 0.4f) * casterH, U(-5, 2)), new Vector2(dir * U(90, 220), -U(10, 60)), U(0.35f, 0.6f), 4,
                        U(8, 12), Back);
                HoaCau(Bay, t => R * (1 + 0.06f * Mathf.Sin(t * 40)), NuiCauBay + 0.01f);
            });
            Every(L, L + NuiCauBay, 50, x =>
            {
                var q = Flame(Bay(T) - d0 * R * 0.3f + U2(-0.4f, 0.4f) * R, -d0 * U(60, 140) + new Vector2(-d0.y, d0.x) * U(-80, 80) + new Vector2(0, -20),
                    U(0.2f, 0.3f), R * 0.8f, R * 0.8f, "tron", Th.pal, Front, 3, -140, 1.4f, 0, 0);
                HoaLuoi(q, 1, 0.2f, 0);
                q.sizeFn = (z, k) => z.r1 * Mathf.Pow(1 - k, 1.1f);
            });
            HoaDuoiKhoi(t => Bay(t) - d0 * R, L + 0.03f, L + NuiCauBay, 12, 15);
            Every(L, L + NuiCauBay, 14, x => Spark(Bay(T), -d0 + U2(-0.6f, 0.6f), U(160, 280), 0, 6));

            // chạm: nổ lớn KR5, giọt dung nham văng ra rơi xuống đất, nổ phụ, khói cụm và tro
            float tNo = L + NuiCauBay;
            At(tNo, () =>
            {
                NuocPulse?.Invoke(0.9f);
                HoaCauNo(tgt, foeFeet, tH, dir, 1.2f);
                for (int j = 0; j < 5; j++) LavaDrop(tgt + U2(-8, 8), new Vector2(U(-240, 240), -U(200, 380)), U(3.5f, 5.5f), foeFeet.y, U(0, 1) < 0.5f ? Back : Front);
            });
            At(tNo + 0.13f, () =>
            {
                Shake?.Invoke(0.25f);
                HoaNo(tgt + new Vector2(dir * U(4, 20), U(-26, 6)), 0.6f, tH);
            });
            At(tNo + 0.34f, () =>
            {
                for (int i = 0; i < 2; i++)
                    HoaKhoi(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.15f, 0.5f) * tH), U(0.13f, 0.17f) * tH, Back, null, 0, true, 0.5f);
                for (int i = 0; i < 3; i++) Ash(foeBody + U2(-28, 28));
            });
            return tNo;
        }

        // HÚC (đòn đánh thường, tướng lao tới; lead = khung trúng của clip attack)
        public float NNuiHuc(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.2f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            // bật khỏi chỗ (hết ghìm, 0,10 s trước khi chạm): vòng cung bụi, bụi đá bắn ra sau
            At(Mathf.Max(0.02f, L - 0.12f), () =>
            {
                HoaCung(casterFeet + new Vector2(0, 2), 0.08f * casterH, 0.5f * casterH, 0.35f, TroC2);
                for (int i = 0; i < 7; i++)
                    BuiTro(casterFeet + new Vector2(U(-0.2f, 0.2f) * casterH, U(-5, 2)), new Vector2(-dir * U(130, 300), -U(20, 90)), U(0.35f, 0.6f), 4,
                        U(9, 14), Back);
            });
            // đầu húc vào mặt trước thân đối thủ, ngang ngực
            var cham = foeBody + new Vector2(-dir * 0.12f * tH, 0.08f * tH);
            At(L, () =>
            {
                Shake?.Invoke(0.45f);
                HoaNo(cham, 0.55f, tH);
                for (int i = 0; i < 6; i++)
                {
                    float a = (i - 2.5f) * 0.4f + U(-0.1f, 0.1f); // quạt quanh hướng húc, hơi hất lên
                    Spark(cham, new Vector2(dir * Mathf.Cos(a), Mathf.Sin(a) - 0.2f), U(280, 460), 0, 7);
                }
                for (int i = 0; i < 6; i++)
                {
                    float sd = (i & 1) == 0 ? -1 : 1;
                    DaBazan(cham + new Vector2(U(-4, 4), sd * U(4, 14)), new Vector2(dir * U(60, 260), sd * U(60, 200) - U(120, 240)), U(0.45f, 0.7f),
                        U(3.2f, 5));
                }
                for (int i = 0; i < 3; i++) LavaDrop(cham, new Vector2(dir * U(40, 220), -U(160, 300)), U(3, 4.5f), foeFeet.y, i == 0 ? Front : Back);
                HoaCung(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.6f * tH, 0.4f, TroC2);
                for (int i = 0; i < 6; i++)
                    BuiTro(foeFeet + new Vector2(dir * U(0.05f, 0.3f) * tH, U(-5, 2)), new Vector2(dir * U(120, 280), -U(10, 60)), U(0.4f, 0.65f), 4,
                        U(9, 13), Back);
            });
            return L;
        }
    }
}

