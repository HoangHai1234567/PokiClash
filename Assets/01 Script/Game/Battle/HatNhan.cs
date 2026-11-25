// Bộ HỎA NHÃN (2026-11-13, mắt lửa bọc giáp, suất hoa_nhan đảo Hỏa; rig ArtGen/Spine/mat_lua*.py).
// Người dùng: chiêu mana "giống skill_02, bổ sung thêm bắn tia lửa từ giữa mắt"; chiêu cuối "dơ 2 tay sang ngang, xoay liên tục quanh cơ
// thể như chong chóng rồi lao vào đập liên tục vào đối thủ"; "fx bạn cứ tự bổ sung nếu thiếu".
// Đi đường bộ Hỏa (StageView.FireFx → PlayMana / PlayUlt): phát ở khung nhả của clip, màu theo Themes["hoa_nhan"] (bảng "lua").
// - tia_mat: TIA lửa liền từ con ngươi (mảng liền 5 lớp: mực, đỏ tươi, cam, vàng, lõi kem; mép lượn; đầu PHÌNH tròn dừng ở mặt trước thân
//   đối thủ) + lưỡi lửa chữ S dọc tia + BÔNG VA CHẠM toé ngược và lửa dạt dọc mặt thân suốt dòng; hết dòng đuôi rút tới chỗ chạm, tia mảnh dần,
//   vỡ thành lưỡi lửa + khói cụm, nổ nhỏ kết (2026-11-18); clip giữ dáng bung 0,96 s sau khung nhả (HoldOf 1,0).
// - quyen_xoay: lửa XOÁY quanh đối thủ trong lúc hai nắm tay quay chong chóng đập vào, mỗi nhát một chớp nổ + tia lửa văng (6 nhát cách
//   0,18 s, nhát cuối to nhất), rồi khói tan. Tướng lao tới đối thủ trong clip (lunge), hiệu ứng đặt ở chỗ đối thủ.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public const float TiaMatHold = 1.0f;

        // tia lửa từ con ngươi tới thân đối thủ; trả giây tới lúc đầu tia chạm đối thủ
        // casterH (2026-11-19 khuya): chiều cao người bắn, cho bề dày tia vẽ sẵn (0,22 casterH); 0 = lấy theo tH
        public float TiaMat(Vector2 mouth, Vector2 target, float tH, float dur = 0.9f, float casterH = 0)
        {
            var dd = target - mouth;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            var src = mouth + u * 6;
            const float T0 = 0.04f, SP = 1700, RUT = 2100;
            float T1 = T0 + dur, goc = T;
            // 2026-11-18 (người dùng: "cuối tia cụt lủn, không có va chạm"): đầu tia dừng ở MẶT TRƯỚC thân đối thủ, đầu phình tròn, bông va chạm toé
            // ngược ở đó suốt dòng tia; hết dòng thì đuôi rút tới chỗ chạm, tia mảnh dần và vỡ thành lưỡi lửa + khói, nổ nhỏ kết
            float mat = Mathf.Max(30, dist - 6 - 0.2f * tH);
            var cham = src + u * mat;
            float travel = Mathf.Max(0.03f, mat / SP), tHit = T0 + travel, tHet = T1 + mat / RUT;
            var pc = Pal[Th.pal];
            var lop = new[] { Ink, pc[0], pc[1], pc[2], pc[3] }; // mực, đỏ tươi, cam, vàng, lõi kem (tươi, không ngả nâu)
            float[] wf = { 1, 1, 0.76f, 0.5f, 0.24f };
            float hw0 = Mathf.Clamp(0.12f * tH, 18, 34);             // nửa bề ngang tia theo cỡ đối thủ
            // TIA VẼ SẴN (2026-11-19 khuya; người dùng: tia "nhìn vẫn chưa đã" — ống thẳng đặc, chỗ trúng nhỏ): có bộ da DaTiaLua thì thân tia,
            // cầu đầu nòng, bông trúng là khung vẽ sẵn (HatTiaFb.cs), giữ giờ chạm, nhịp HoaTrung / Shake và giờ trả về
            if (CoLaser || HasTia(DaTiaLua))
            {
                TiaMatFb(src, cham, target, u, nrm, tH, 0.22f * (casterH > 0 ? casterH : tH), T0, T1, tHit, mat);
                return tHit;
            }
            // con ngươi loé: chớp nhỏ + vài tia lửa toé ngược
            At(T0, () =>
            {
                Shake?.Invoke(0.18f);
                HoaChop(src, 0.3f * tH, 0.08f);
                for (int i = 0; i < 4; i++) Spark(src + U2(-4, 4), -u * U(0.4f, 0.9f) + nrm * U(-0.9f, 0.9f), U(200, 340), 0, 6);
            });
            // lõi tia: mảng liền 5 lớp, đầu chạy tới mặt trước thân rồi PHÌNH tròn, mép lượn như lửa; cuối dòng đuôi rút tới đầu, mảnh dần
            var core = new P { pos = src, life = tHet - T0 + 0.04f, group = Front };
            core.draw = (q, k, buf) =>
            {
                float a = q.age;
                float head = Mathf.Min(mat, SP * a), tail = Mathf.Max(0, RUT * (a - dur));
                if (head - tail < 8) return;
                float mong = 1 - 0.7f * SmoothStep(dur - 0.04f, dur + 0.14f, a);
                float hwDau = hw0 * 1.12f * mong * (1 + 0.1f * Mathf.Sin(a * 41));
                int n = Mathf.Max(2, Mathf.CeilToInt((head - tail) / 12) + 1);
                var cd = src + u * head + nrm * (2.2f * Mathf.Sin(head * 0.05f - a * 26));
                for (int li = 0; li < 5; li++)
                {
                    float grow = li == 0 ? 2.6f : 0;
                    int a0 = mp.Count;
                    for (int pass = 0; pass < 2; pass++)
                        for (int i = 0; i < n; i++)
                        {
                            float x = tail + (head - tail) * i / (n - 1);
                            float env = Mathf.Min(1, (x - tail) / 22 + 0.3f);
                            float hw = hw0 * (1 + 0.22f * Mathf.Sin(x * 0.07f - a * 34) + 0.12f * Mathf.Sin(x * 0.19f + a * 21)) * env * mong;
                            var c = src + u * x + nrm * (2.2f * Mathf.Sin(x * 0.05f - a * 26));
                            mp.Add(c + nrm * ((pass == 0 ? 1 : -1) * (hw * wf[li] + grow)));
                        }
                    MRibbon(Front, 9 + li * 0.1f, a0, a0 + n, n, lop[li]);
                    // nắp tròn ở đầu tia (không cắt phẳng): cùng lớp nên gộp chung một viền mực với thân tia
                    float rc = hwDau * wf[li] + grow;
                    int c0 = mp.Count;
                    var ch = cd - u * (hwDau * 0.35f);
                    for (int j = 0; j < 12; j++) mp.Add(ch + new Vector2(Mathf.Cos(j * 0.5236f), Mathf.Sin(j * 0.5236f)) * rc);
                    MFill(Front, 9 + li * 0.1f + 0.01f, c0, 12, lop[li]);
                }
            };
            At(T0, () => Add(core));
            // lưỡi lửa chữ S bám mép đoạn tia đang hiện (không mọc trước đầu tia), ngọn ngả theo hướng bắn
            Every(T0 + 0.02f, T1, x => 40 * Mathf.Min(1, (1 - x) * dur / 0.12f), x =>
            {
                float a = T - goc - T0, head = Mathf.Min(mat, SP * a);
                if (head < 30) return;
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                var q = Flame(src + u * U(0.05f, 0.9f) * head + nrm * sd * hw0 * U(0.3f, 0.9f), u * U(420, 700) + nrm * sd * U(30, 90), U(0.28f, 0.38f), U(8, 10),
                    U(17, 23), "krl", Th.pal, Front, 1.8f, -240, 1f, 0, 0);
                q.smokeGroup = Back;
            });
            // con ngươi phụt lửa liên tục (gốc tia)
            Every(T0, T1, 20, x => HoaLuoi(Flame(src + U2(-3, 3), u * U(60, 120) + nrm * U(-40, 40), U(0.2f, 0.28f), 8, U(16, 22), "tron", Th.pal, Front, 2.4f,
                -200, 1.2f, 0, 0), 1, 0.3f, 0));
            // VA CHẠM: chớp khi đầu tia tới, bông lửa toé ngược ở mặt trước thân suốt dòng, lưỡi lửa dạt dọc mặt thân, khói cụm sau lưng, đối thủ chớp
            At(tHit, () =>
            {
                Shake?.Invoke(0.28f);
                HoaChop(cham, 0.42f * tH, 0.09f);
                HoaBong(cham, -u, 0.55f * tH, tHet - tHit + 0.04f);
                HoaTrung?.Invoke(target, 0.6f);
                Extra(cham, 3, 260);
            });
            Every(tHit + 0.03f, T1, 18, x =>
            {
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                var v = (-u * U(0.15f, 0.55f) + nrm * sd * U(0.7f, 1f) + new Vector2(0, -0.35f)) * U(240, 400);
                HoaLuoi(Flame(cham + nrm * sd * U(4, 14), v, U(0.2f, 0.3f), 7, U(14, 19), "tron", Th.pal, U(0, 1) < 0.5f ? Back : Front, 3.5f, -200, 1.4f, 0, 0),
                    1, 0.3f, 0.06f);
                if (U(0, 1) < 0.5f) Spark(cham + U2(-8, 8), -u * U(0.3f, 0.8f) + nrm * sd * U(0.4f, 1f) + new Vector2(0, -0.4f), U(240, 420), 0, 6);
            });
            Every(tHit + 0.2f, T1, 5, x => HoaTrung?.Invoke(target, 0.3f));
            Every(tHit + 0.1f, T1, 3.5f, x => HoaKhoi(cham + new Vector2(U(-10, 10), -0.22f * tH), U(11, 15), Back));
            // KẾT: đuôi tia rút qua đâu thì tia vỡ ra ở đó thành lưỡi lửa nhỏ bốc lên + cụm khói mảnh; tới chỗ chạm thì nổ nhỏ
            Every(T1, tHet, 34, x =>
            {
                float a = T - goc - T0, tail = Mathf.Min(mat, RUT * (a - dur));
                var p = src + u * tail + nrm * U(-0.8f, 0.8f) * hw0;
                HoaLuoi(Flame(p, new Vector2(U(-30, 30), -U(60, 140)) + u * U(40, 120), U(0.24f, 0.34f), 6, U(12, 17), "tron", Th.pal, Front, 2.5f, -200, 1.3f,
                    0, 0), 1, 0.6f, 0);
                if (U(0, 1) < 0.18f) HoaKhoi(p + new Vector2(0, -6), U(8, 11), Back, null, U(0.7f, 0.9f), false);
            });
            At(tHet, () =>
            {
                Shake?.Invoke(0.2f);
                HoaNo(cham, 0.45f, tH, null, Front, u.x >= 0 ? 1 : -1); // khung vẽ sẵn (2026-11-19): "trung_lua" lật theo hướng tia
                HoaKhoi(cham + new Vector2(0, -0.15f * tH), U(15, 19), Back, null, 0, true, 0.7f);
                for (int i = 0; i < 4; i++) Ash(target + U2(-26, 26));
            });
            return tHit;
        }

        // TIA MẮT bằng khung vẽ sẵn (TiaFb + DaTiaLua): đoạn lửa có sợi xoắn trôi liên tục từ con ngươi tới mặt trước thân đối thủ, cầu lửa xoáy ở
        // con ngươi lớn dần trong pha tụ, lửa toé ngược lặp ở chỗ trúng. Nối giờ như NTiaKhung (HatFbThuy.cs): tTu = giờ chạm cũ − thời gian vươn
        // (quãng / 2600, kẹp 0,07–0,14), tBan = giờ tắt cũ − giờ chạm; đoạn cuối bay nốt vào đích ở tCut thì nổ kết. Bỏ: lõi tia mảng liền, chớp
        // con ngươi, lửa phụt ở con ngươi, lưỡi lửa bám mép tia, chớp + bông HoaBong ở chỗ trúng, lưỡi lửa dạt dọc thân, tia vỡ lúc rút. Giữ: rung,
        // tia văng ngược ở con ngươi, nhịp HoaTrung (lúc chạm 0,6, rồi 0,3 mỗi 0,2 s), mảnh theo chủ đề, tia văng ở chỗ trúng (thưa), khói cụm sau
        // lưng, nổ nhỏ + khói + tro lúc kết.
        void TiaMatFb(Vector2 src, Vector2 cham, Vector2 target, Vector2 u, Vector2 nrm, float tH, float day, float T0, float T1, float tHit, float mat)
        {
            float dai = Mathf.Max(30, mat);
            float tVuon = Mathf.Clamp(dai / 2600f, 0.07f, 0.14f);         // như TiaFb
            float tTu = Mathf.Max(0.03f, tHit - tVuon), tBan = Mathf.Max(0.2f, T1 - tHit);
            float vChay = Mathf.Max(380, dai / 0.32f);                     // như TiaFb: đoạn cuối bay nốt tới đích
            float tCut = T1 + dai / vChay;
            At(T0, () =>
            {
                Shake?.Invoke(0.18f);
                for (int i = 0; i < 4; i++) Spark(src + U2(-4, 4), -u * U(0.4f, 0.9f) + nrm * U(-0.9f, 0.9f), U(200, 340), 0, 6);
            });
            // 2026-11-25 (người dùng chọn "tia lửa năng lượng" khi làm chiêu đổi màu cho hệ khác): có lưới shader thì thân tia, cầu đầu nòng, chỗ
            // trúng là tia năng lượng kiểu Water Laser bảng lửa (ELaser LaserLua, HatTiaLaser.cs), cùng giờ chạm; không thì tia vẽ sẵn
            if (CoLaser) ELaser(LaserLua, () => src, () => cham, day, tTu, tBan, Front, 0.9f, 1);
            else TiaFb(DaTiaLua, src, cham, day, tTu, tBan);
            At(tHit, () =>
            {
                Shake?.Invoke(0.28f);
                HoaTrung?.Invoke(target, 0.6f);
                Extra(cham, 3, 260);
            });
            Every(tHit + 0.03f, T1, 9, x =>
            {
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                Spark(cham + U2(-8, 8), -u * U(0.3f, 0.8f) + nrm * sd * U(0.4f, 1f) + new Vector2(0, -0.4f), U(240, 420), 0, 6);
            });
            Every(tHit + 0.2f, T1, 5, x => HoaTrung?.Invoke(target, 0.3f));
            Every(tHit + 0.1f, T1, 3.5f, x => HoaKhoi(cham + new Vector2(U(-10, 10), -0.22f * tH), U(11, 15), Back));
            At(tCut, () =>
            {
                Shake?.Invoke(0.2f);
                HoaNo(cham, 0.45f, tH, null, Front, u.x >= 0 ? 1 : -1);
                HoaKhoi(cham + new Vector2(0, -0.15f * tH), U(15, 19), Back, null, 0, true, 0.7f);
                for (int i = 0; i < 4; i++) Ash(target + U2(-26, 26));
            });
        }

        // chiêu cuối: lửa xoáy quanh đối thủ + chuỗi chớp nổ theo nhịp đấm; trả 0 (nhát đầu trúng ngay lúc gọi, khớp khung trúng của clip)
        public float QuyenXoay(Vector2 foeFeet, Vector2 foeBody, float tH, int nhat = 6, float cach = 0.18f)
        {
            var Cc = foeFeet + new Vector2(0, 2);
            float T1 = (nhat - 1) * cach + 0.25f, HT = 0.95f * tH, R = 0.62f * tH, OM = 11;
            HoaCung(Cc, 0.2f * tH, 1.0f * tH, 0.5f, Th.ring);
            // vòng lửa xoáy: lưỡi lửa chữ S bay vòng elip quanh đối thủ, dâng dần lên; nửa xa vẽ sau, nửa gần vẽ trước
            void Orbit(P q, float dt, HatLua s)
            {
                float a = q.ph + OM * q.age, y = q.vy * q.age;
                float rr = q.R0 * (1 - 0.25f * Mathf.Min(1, y / HT));
                q.pos = Cc + new Vector2(rr * Mathf.Cos(a), 0.3f * rr * Mathf.Sin(a) - y);
                q.vel = new Vector2(-rr * Mathf.Sin(a) * OM, 0.3f * rr * Mathf.Cos(a) * OM - q.vy);
                q.group = Mathf.Sin(a) < 0 ? Back : Front;
            }
            // khung vẽ sẵn (2026-11-19 tối, người dùng chê lốc cũ "màu hơi trầm và chưa hợp lắm"): thân lốc là "loc_lua" bao quanh đối thủ (lớp sau
            // đặc, lớp trước mờ 0,55 lệch pha), vọt lên 0,2 s, xoáy tới hết chuỗi đấm rồi tắt dần; bỏ lưỡi lửa chữ S bay vòng elip. 2026-11-19 đêm
            // (người dùng: "lốc xoáy làm to lên cho che hết tướng địch"): lốc trùm "loc_lua_bao" cao 1,65 thân, giãn ngang 1,2 (ngang thân ≈ 1,2
            // thân, trùm từ chân tới đầu); chưa nhập thì "loc_lua" cao 1,7 thân, giãn 1,55
            if (!HoaFbLoc(Cc, 1.7f * tH, 0, T1 + 0.1f, true, 0.55f, 1.15f, 1.55f, 1.65f * tH, 1.2f))
                Every(0, T1, x => 70 * Mathf.Min(1, x * 5 + 0.4f) * (1 - 0.6f * Mathf.Max(0, (x - 0.8f) / 0.2f)), x =>
                {
                    var q = Flame(Cc, Vector2.zero, U(0.32f, 0.46f), U(8, 10), U(18, 26), "krl", Th.pal, Front, 0, 0, 1.5f, 0, 0);
                    q.ph = U(0, 6.28f);
                    q.vy = U(0.6f, 1.3f) * HT / q.life;
                    q.R0 = R * U(0.85f, 1.15f);
                    q.upd = Orbit;
                    q.smokeGroup = Back;
                });
            else // tàn lửa phụ bị cuốn quanh lốc (thưa, theo quỹ đạo cũ), cho lốc có hạt bay quanh
                Every(0.15f, T1, 8, x => HoaTan(Cc + new Vector2(U(-0.45f, 0.45f) * tH, -U(0.1f, 0.8f) * tH), new Vector2(U(-160, 160), -U(80, 200)),
                    U(0.35f, 0.5f), 2, U(0, 1) < 0.5f ? Back : Front));
            // nhịp đấm: mỗi nhát một vụ nổ KR5 ở thân (so le trái phải, cao thấp), tia lửa văng; nhát cuối to nhất, có vòng cung + vệt cháy dưới chân
            for (int i = 0; i < nhat; i++)
            {
                bool cuoi = i == nhat - 1;
                float t = i * cach;
                float huong = (i & 1) == 0 ? 1 : -1; // khung vẽ sẵn (2026-11-19): hai nắm tay chong chóng đập so le, "trung_lua" lật xen kẽ
                At(t, () =>
                {
                    var c = foeBody + new Vector2(U(-0.22f, 0.22f) * tH, U(-0.18f, 0.12f) * tH);
                    Shake?.Invoke(cuoi ? 0.45f : 0.16f);
                    HoaTrung?.Invoke(c, cuoi ? 0.8f : 0.4f);
                    HoaNo(c, cuoi ? 1.0f : U(0.42f, 0.55f), tH, cuoi ? Cc : (Vector2?)null, Front, huong);
                    int ns = cuoi ? 6 : 3;
                    for (int j = 0; j < ns; j++)
                    {
                        float a = U(0, 6.28f);
                        Spark(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f), U(260, 480), 0, 7);
                    }
                    if (cuoi) Extra(c, 4, 320);
                });
            }
            At(T1, () =>
            {
                for (int i = 0; i < 3; i++)
                    HoaKhoi(foeBody + new Vector2(U(-0.35f, 0.35f) * tH, -U(0.15f, 0.55f) * tH), U(0.13f, 0.17f) * tH, Back, null, 0, true, 0.5f);
                for (int i = 0; i < 4; i++) Ash(foeBody + U2(-30, 30));
            });
            return 0;
        }
    }
}
