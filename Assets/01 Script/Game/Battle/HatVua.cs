// Bộ VUA ROBOT (2026-11-17, suất kim_nghe ải 70 đảo Kim, boss cuối; rig ArtGen/Spine/vua_may_rig.py trên rig gốc monster_3637): dạng 1 vua_may_1
// (VM_DANG=non + vua_may_non.py: hoàng tử robot), dạng 2 vua_may_2 (vua robot giáp vàng bốn cánh, hào quang nguyệt quế, quyền trượng Mặt Trời +
// ba hành tinh); ghi chú ArtGen/Spine/inbox/vua_may_ghichu.md. Người dùng: "các fx tia sáng và vụ nổ cần cải thiện thêm trong unity".
// Rig tự vẽ phần hình (vệt cung lửa, ấn mặt trời, cột sáng, hành tinh xếp cột, đoạn tia, nhật thực, thiên thạch đuôi lửa); vụ nổ trong rig
// (ảnh Mặt Trời phóng to) ĐÃ TẮT khi vào game (quai/doi_vua_may.py an_no): nổ, chớp, tia lửa, bụi, khói, rung, màn tối là việc của lớp này.
// Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc: phát lúc clip BẮT ĐẦU, `lead` = giờ trúng của clip); mốc là giây clip của rig co theo
// lead; chỗ Mặt Trời từng khung và đường rơi ba thiên thạch là bảng đo ở HatVuaBang.cs (sinh bằng ArtGen/Spine/vua_may_do_hat.py).
// - n_vua_an1 / n_vua_an (đòn thường "Nhật Ấn"): Mặt Trời hút năng lượng; cú vụt kéo lưỡi lửa; đầu trượng nện đất (chớp, bụi, đá, vòng đất);
//   một đường lửa sáng chạy dọc đất tới đối thủ; ấn nở dưới chân đối thủ (vòng, tia); trúng: chớp, cột năng lượng phụt lên, tia lửa, than.
// - n_vua_tia1 / n_vua_tia (chiêu mana "Tam Tinh Quang Pháo"): Mặt Trời trên trượng hút năng lượng; ba hành tinh xếp cột trên đầu đối thủ (chớp
//   nhỏ từng hành tinh); Mặt Trời lên đỉnh cột (chớp, tụ); TIA giáng thẳng xuống: lõi lửa năng lượng dọc cột, dày dần sau mỗi hành tinh, tia
//   lửa văng hai bên, chớp màn; trúng: nổ mặt trời lớn, vòng sóng đất, bụi, tia, than, khói.
// - n_vua_nhat1 / n_vua_nhat (chiêu cuối "Nhật Thực Thiên Giáng"): vỗ cánh bay lên (gió bụi); ba vệt quỹ đạo lấp lánh quanh vua; Mặt Trời
//   hút năng lượng; NHẬT THỰC: màn tối ~1 s, vành nhật hoa trắng nháy, tia trắng; ba thiên thạch (rig vẽ) kéo đuôi lửa hạt, nện lần lượt: nổ
//   lửa đỏ cam, mỗi cú một nhịp rung, cú cuối (Trái Đất) nổ rất lớn, chớp màn, nứt đất, đá văng, cột lửa; Mặt Trời sáng lại.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // màu: KHÔNG dùng biến tĩnh của file khác trong khởi tạo tĩnh
        // năng lượng Mặt Trời TƯƠI (người dùng 2026-11-18: "hình mặt trời, các tia beam bắn xuống nhìn màu hơi tối ... màu tươi hơn"): cam đỏ sát
        // viền #F0702A, cam #FFA43A, vàng #FFD94A, lõi kem #FFF6D6 (trước: cam ngả nâu)
        static readonly Color[] VmVang = { C(240, 112, 42), C(255, 164, 58), C(255, 217, 74), C(255, 246, 214) };
        static readonly Color VmTrang = C(255, 250, 236), VmToi = new Color(0.05f, 0.03f, 0.1f, 0.85f);
        static readonly Color VmFlash = new Color(1f, 0.97f, 0.8f, 0.24f);   // chớp màn kem nhẹ (alpha 0,4 làm cả màn bạc màu)
        static readonly Theme VmLuaTh = new Theme
        {
            pal = "lua", spark = C(255, 214, 120), ember = C(248, 140, 44), ring = C(240, 110, 40), ring2 = C(252, 236, 180), extra = "giap",
            extraCol = C(90, 84, 78)
        };

        sealed class VmBang
        {
            public float[] amx, amy, cmx, cmy, smx, smy;
            public float[][] tx, ty;
            public float far;
        }

        static VmBang vm1, vm2;

        static VmBang VmLay(int dang) =>
            dang == 1
                ? (vm1 ??= new VmBang
                {
                    amx = Vm1AMX, amy = Vm1AMY, cmx = Vm1CMX, cmy = Vm1CMY, smx = Vm1SMX, smy = Vm1SMY, tx = new[] { Vm1T0X, Vm1T1X, Vm1T2X },
                    ty = new[] { Vm1T0Y, Vm1T1Y, Vm1T2Y }, far = VmFar1
                })
                : (vm2 ??= new VmBang
                {
                    amx = Vm2AMX, amy = Vm2AMY, cmx = Vm2CMX, cmy = Vm2CMY, smx = Vm2SMX, smy = Vm2SMY, tx = new[] { Vm2T0X, Vm2T1X, Vm2T2X },
                    ty = new[] { Vm2T0Y, Vm2T1Y, Vm2T2Y }, far = VmFar2
                });

        static Vector2 VmMau(float[] xs, float[] ys, float t)
        {
            float f = Mathf.Max(0, t) / VmDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            float w = Mathf.Clamp01(f - i);
            return new Vector2(Mathf.Lerp(xs[i], xs[j], w), Mathf.Lerp(ys[i], ys[j], w));
        }

        // ---------------------------------------------------------------- hạt riêng

        // tụ năng lượng vào Mặt Trời: hạt vàng bị hút từ một vòng quanh tâm (tâm đi theo bảng), thỉnh thoảng một lưỡi năng lượng liếm
        // 2026-11-18: vệt XOẮN ỐC vào Mặt Trời, nhanh dần, chạm vỏ thì nhập; dày dần tới lúc nhả; một vòng co về tâm giữa chừng
        void VmTu(System.Func<float, Vector2> tam, float t0, float t1, float R, float manh)
        {
            Every(t0, t1, x => (12 + 32 * x) * manh, x => RbHutXa(tam, U(1.8f, 3f) * R, U(0.32f, 0.5f), U(5, 7.5f) * manh, Front, _ => 0.9f * R));
            Every(t0 + 0.05f, t1, x => 5 + 9 * x, x => RbLiem(tam(T), R * 0.8f));
            At(t0 + 0.55f * (t1 - t0), () => KmVong(tam, 0.24f, 3.2f * R, 1.0f * R, KmNang[4], 1, 0.8f));
        }

        // đường lửa sáng chạy dọc mặt đất từ a tới b trong khoảng [t0, t1]: tia vàng phụt lên, lưỡi lửa nhỏ, bụi
        void VmDuongLua(Vector2 a, Vector2 b, float t0, float t1, float H, float manh)
        {
            float t00 = T;
            // khung vẽ sẵn (2026-11-19): cứ ba nhịp một cụm lửa lặp "lua_lap" nhỏ mọc, cháy, co tại chỗ (đường lửa liền khối, KmFbMoc ở
            // HatFbKim.cs) thay lưỡi lửa rời; tia, bụi giữ. Chưa nhập ảnh: lưỡi lửa cũ
            bool fb = HasFb("lua_lap");
            int dem = 0;
            Every(t0, t1, 70, x =>
            {
                float u = Mathf.Clamp01((T - t00 - t0) / Mathf.Max(0.05f, t1 - t0));
                var p = Vector2.Lerp(a, b, u) + new Vector2(U(-6, 6), U(-3, 2));
                if (U(0, 1) < 0.45f) KmTiaLua(p, new Vector2(U(-0.3f, 0.3f), -1), U(260, 460) * manh, U(5, 7), KmNang[3 + rng.Next(2)]);
                if (fb)
                {
                    if (dem++ % 3 == 0)
                        KmFbMoc("lua_lap", p + new Vector2(0, 2), 0.2f * H * manh * U(0.85f, 1.15f), U(0.3f, 0.42f), U(0, 1) < 0.5f ? Back : Front, 22, 0.06f,
                            0.16f, 0.4f, rng.Next(2) == 0);
                }
                else
                {
                    var q = Flame(p, new Vector2(U(-20, 20), -U(60, 140)), U(0.18f, 0.28f), 0.05f * H * manh, 0.09f * H * manh, "tron", "vtuoi",
                        U(0, 1) < 0.5f ? Back : Front, 2.5f, -200, 1.6f, 0, 0.1f);
                    Tongue(q, 1, 0.3f);
                }
                if (U(0, 1) < 0.35f) BuiTro(p, new Vector2(U(-40, 40), -U(10, 40)), U(0.4f, 0.6f), 3, U(7, 10), Back);
            });
        }

        // nổ năng lượng vàng tươi (ấn / tia Mặt Trời trúng), kiểu KR5: chớp 2 khung nhỏ, lưỡi liềm vàng cắm trong khối khói hai tông sau lưng đối
        // thủ, vòng cung dẹt, vệt cháy, tia bắn rồi khựng, cụm đốm nhỏ (2026-11-18; trước: chớp 1,1 thân + cầu lửa CauNo trùm kín đối thủ)
        void VmNoVang(Vector2 tgt, Vector2 feet, Vector2 body, float tH, float dir, float sc)
        {
            KmNo(tgt, feet, tH, sc, "vtuoi", dir);
            KmVong(_ => tgt, 0.22f, 0.15f * tH, 0.5f * tH * sc, VmVang[3], 1, 0.6f);   // vòng va chạm nhỏ, nhạt (vòng 0,8 thân thành cái vòng vàng to trùm đối thủ)
            for (int i = 0; i < 2; i++)
                KmDomCum(body + new Vector2(U(-0.25f, 0.25f) * tH, -U(0.1f, 0.45f) * tH), new Vector2(U(-50, 50), -U(80, 150)), VmVang[2 + (i & 1)]);
        }

        // nổ lửa đỏ cam (thiên thạch nện), kiểu KR5; sc: cỡ; huong: phía đá văng
        void VmNoLua(Vector2 tgt, Vector2 feet, float tH, float sc, int nDa, float huong)
        {
            var th0 = Th;
            Th = VmLuaTh;
            KmNo(tgt, feet, tH, sc, "luat", huong);
            KmCung(feet + new Vector2(0, 2), 0.14f * tH, 0.95f * tH * sc, 0.42f, KmLua[4], 0.3f, Floor, 30.6f, 0.8f);
            BuiDap(feet, tH, 1.1f * sc, 8);
            for (int i = 0; i < nDa / 2; i++)
                Rock(feet + new Vector2(U(-0.3f, 0.3f) * tH, -6), new Vector2(U(-300, 300), -U(300, 560)), feet.y + U(-4, 8), U(8, 14) * sc);
            Th = th0;
        }

        // ---------------------------------------------------------------- ba đòn

        // ĐÒN THƯỜNG "Nhật Ấn". dang: 1 / 2. Trả giây tới lúc trúng (= lead).
        public float NVuaAn(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.3f, lead), k = L0 / VmALead, T0 = T;
            var B = VmLay(dang);
            float manh = dang == 1 ? 0.8f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 Sun(float t) => San(VmMau(B.amx, B.amy, (t - T0) / k));
            float R = Mathf.Clamp(0.07f * casterH, 8, 18) * manh;
            float tTu = VmATu * k, tDap = VmADap * k, tAn = VmAAn * k;
            KmPal();

            // 1. Mặt Trời hút năng lượng trong lúc lấy đà
            At(tTu, () =>
            {
                RbVong(Sun(T), 0.2f, 0.4f * R, 1.8f * R, VmVang[2]);
                RbTia(Sun(T), 0.5f * R, 5, 90, 160, 60);
            });
            VmTu(Sun, tTu, tDap - 0.12f * k, R, manh);
            // 2. cú vụt: lưỡi lửa, tia vàng kéo theo Mặt Trời
            Every(tDap - 0.14f * k, tDap, 90, x =>
            {
                var c = Sun(T);
                var q = Flame(c + U2(-0.4f, 0.4f) * R, new Vector2(U(-50, 50), U(-50, 50)), U(0.16f, 0.24f), 0.7f * R, 1.1f * R, "tron", "vtuoi", Front,
                    3, -100, 1.5f, 0, 0.15f);
                Tongue(q, 1, 0.3f);
                if (U(0, 1) < 0.5f) KmTiaLua(c, new Vector2(U(-1, 1), U(-1, 1)), U(220, 400), U(5, 7), VmVang[3]);
            });
            // 3. đầu trượng nện đất: chớp, bụi, đá, vòng đất, rung
            var dat = new Vector2(Sun(T0 + tDap).x, casterFeet.y);
            At(tDap, () =>
            {
                var c = new Vector2(Sun(T).x, casterFeet.y);
                Shake?.Invoke(0.22f * manh);
                KmChop(c + new Vector2(0, -0.08f * casterH), 1.4f * R + 0.12f * casterH * manh, 0.07f, KmNang);
                KmCung(c + new Vector2(0, 2), 0.06f * casterH, 0.55f * casterH * manh, 0.34f, VmVang[3]);
                BuiDap(c, casterH, 0.8f * manh, 6);
                for (int i = 0; i < 3; i++) Rock(c + new Vector2(U(-20, 20), -4), new Vector2(U(-220, 220), -U(240, 420)), c.y + U(-3, 6), U(6, 10) * manh);
                for (int i = 0; i < 6; i++) KmTiaLua(c, new Vector2(U(-1, 1), -U(0.4f, 1)), U(380, 640), U(5, 8), VmVang[2 + (i & 1)]);
            });
            // 4. đường lửa chạy dọc đất tới chân đối thủ
            VmDuongLua(dat, foeFeet, tDap + 0.02f, tAn, casterH, manh);
            // 5. ấn nở dưới chân đối thủ
            At(tAn, () =>
            {
                KmCung(foeFeet + new Vector2(0, 2), 0.1f * tH, 0.75f * tH * manh, 0.36f, VmVang[3]);
                Ring(foeFeet + new Vector2(0, 2), 0.3f, 0.6f * tH * manh, 0.3f * tH, VmVang[1], 0.3f);
                RbTia(foeFeet + new Vector2(0, -6), 0.1f * tH, 7, 180, 320, 300);
            });
            // 6. trúng: chớp, cột năng lượng phụt lên, tia lửa, than, rung
            At(L0, () =>
            {
                Shake?.Invoke(0.4f * manh);
                KmChop(foeFeet + new Vector2(0, -0.12f * tH), 0.36f * tH * manh, 0.07f, KmNang);   // chớp nhỏ ở chân (trước: 0,9 thân che đối thủ)
                KmBong(foeFeet + new Vector2(0, -0.2f * tH), new Vector2(0, -1), 0.36f * tH * manh, 0.14f, KmNang);
                RbCot(foeFeet, tH, 0.36f, manh);
                RbVong(foeBody, 0.26f, 0.15f * tH, 0.8f * tH * manh, VmVang[2]);
                for (int i = 0; i < 8; i++)
                {
                    float a = U(0, 6.28f);
                    KmTiaLua(foeBody, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f), U(420, 700), U(6, 8), VmVang[2 + (i & 1)]);
                }
                Extra(foeBody, Mathf.RoundToInt(3 * manh), 360, Front);
            });
            Every(L0, L0 + 0.5f, 5, x => KmDomCum(foeFeet + new Vector2(U(-0.25f, 0.25f) * tH, -U(0, 0.6f) * tH), new Vector2(U(-30, 30), -U(90, 160)),
                VmVang[2 + rng.Next(2)]));
            At(L0 + 0.3f, () => KmKhoi(foeBody + new Vector2(U(-0.15f, 0.15f) * tH, -U(0.25f, 0.4f) * tH), new Vector2(U(-15, 15), -U(40, 70)),
                0.12f * tH, U(0.9f, 1.2f), Back, 0, 2));
            return L0;
        }

        // CHIÊU MANA "Tam Tinh Quang Pháo": ba hành tinh xếp cột trên đầu đối thủ, Mặt Trời lên đỉnh, tia giáng thẳng xuống. Trả giây tới lúc trúng.
        public float NVuaTia(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.5f, lead), k = L0 / VmCLead, T0 = T;
            var B = VmLay(dang);
            float manh = dang == 1 ? 0.8f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 Sun(float t) => San(VmMau(B.cmx, B.cmy, (t - T0) / k));
            Vector2 Cot(float c) => foeBody + new Vector2(0, -c * B.far * casterH);          // điểm trên cột (bội 1130 đơn vị rig trên far)
            float R = Mathf.Clamp(0.07f * casterH, 8, 18) * manh;
            float tTu = VmCTu * k, tHang = VmCHang * k, tDinh = VmCDinh * k, tBan = VmCBan * k;
            var dinh = Cot(1.42f);
            float[] hanh = { 1.02f, 0.73f, 0.50f };                        // Trái Đất, Sao Hỏa, Sao Thủy (từ trên xuống)
            float lao = 0.12f * k;                                          // tia mọc từ đỉnh xuống tới đối thủ
            float dai = Mathf.Max(1, foeBody.y - dinh.y);                   // y sân đi xuống: đỉnh cột ở trên (y nhỏ hơn)
            KmPal();

            // 1. Mặt Trời trên trượng tụ năng lượng trong lúc giơ trượng
            At(tTu, () => RbVong(Sun(T), 0.2f, 0.4f * R, 1.8f * R, VmVang[2]));
            VmTu(Sun, tTu, 0.55f * k, R, manh);
            // 2. ba hành tinh xếp cột: chớp nhỏ, vòng ở từng hành tinh
            for (int i = 0; i < hanh.Length; i++)
            {
                var p = Cot(hanh[i]);
                At(tHang + 0.04f * k * (2 - i), () =>
                {
                    RbChop(p, 1.6f * R, Front, 0.1f);
                    RbVong(p, 0.22f, 0.5f * R, 2.0f * R, VmVang[2]);
                });
            }
            // 3. Mặt Trời lên đỉnh cột: chớp, tụ
            At(tDinh, () =>
            {
                RbChop(dinh, 2.6f * R, Front, 0.12f);
                RbVong(dinh, 0.24f, 0.6f * R, 2.6f * R, VmVang[3]);
                RbTia(dinh, R, 7, 140, 260, 40);
            });
            VmTu(_ => dinh, tDinh, tBan, 1.2f * R, manh);
            // 4. TIA giáng xuống (2026-11-18: người dùng chê "đầu tia cụt lủn, không có va chạm với địch", "màu hơi tối"): TIA LIỀN KHỐI (mảng
            // liền, không còn ghép lưỡi lửa rời) năm lớp tươi: mực mảnh, dải cam đỏ sát viền, cam, vàng, lõi kem rộng; dày dần sau mỗi hành tinh;
            // vẽ SAU tướng nên đi xuyên qua các hành tinh của rig; đầu tia tới tận đỉnh đầu đối thủ và đứng đó, BÔNG VA CHẠM liên tục ở chỗ chạm
            // (toé, tia kim loại bắn rồi khựng, vòng va chạm, rung nhỏ dồn dập); hết tia thì đuôi rút vào chỗ chạm và bông vỡ to, không cắt phụt
            var cham = foeBody + new Vector2(0, -0.28f * tH);   // chỗ chạm: phần trên thân (tia đi SAU thân nên đoạn dưới khuất, không hở)
            float daiCham = Mathf.Max(1, cham.y - dinh.y);
            float hw = 0.09f * casterH * manh;   // lõi kem rộng (người dùng 2026-11-18)
            float tTat = L0 + 0.32f * k, rut = 0.14f;
            float[] fh = new float[hanh.Length];
            for (int i = 0; i < hanh.Length; i++) fh[i] = Mathf.Clamp01((Cot(hanh[i]).y - dinh.y) / daiCham);
            float Rong(float f)
            {
                float w = 0.55f;
                foreach (var h in fh) w += 0.2f * SmoothStep(h - 0.03f, h + 0.05f, f);   // qua mỗi hành tinh tia dày thêm
                return w;
            }
            // TIA VẼ SẴN (2026-11-19, người dùng: "tia năng lượng ... nhìn vẫn chưa đã": ống thẳng đặc, chỗ trúng nhỏ): có bộ DaTiaVang thì
            // TiaFb (HatTiaFb.cs): đoạn năng lượng Mặt Trời vàng tươi xoắn có sao trôi liên tục từ Mặt Trời đỉnh cột xuống, cầu đầu nòng lớn dần
            // từ lúc Mặt Trời lên đỉnh (tDinh), bông va chạm lặp; vẽ TRƯỚC tướng (thấy rõ chỗ trúng; tia đè lên đoạn tia tối màu của rig), dày
            // 0,22 thân người ra chiêu, chỗ trúng ở đỉnh đầu đối thủ (tia không xuyên mặt). Giữ giờ chạm (tBan + lao), giờ tắt (tTat), nhịp
            // NuocPulse + rung theo nhịp tia, chớp ở hành tinh, tia lửa văng hai bên; bỏ thân tia liền khối và bông va chạm cũ. Chưa nhập ảnh:
            // đường cũ
            bool tiaFb = HasTia(DaTiaVang);
            float tCham = tBan + lao, dayTia = 0.22f * casterH * manh, tVuon = lao;
            if (tiaFb)
            {
                cham = foeBody + new Vector2(0, -0.42f * tH);
                daiCham = Mathf.Max(1, cham.y - dinh.y);
                for (int i = 0; i < hanh.Length; i++) fh[i] = Mathf.Clamp01((Cot(hanh[i]).y - dinh.y) / daiCham);
                tVuon =Mathf.Clamp((cham - dinh).magnitude / 2600f, 0.07f, 0.14f);   // như TiaFb: đầu tia vươn tới đích
                float tTuTia = Mathf.Max(0.05f, tCham - tDinh - tVuon), tBanTia = Mathf.Max(0.2f, tTat - tCham);
                At(tDinh, () => TiaFb(DaTiaVang, dinh, cham, dayTia, tTuTia, tBanTia));
                // nhịp trúng theo tia (thay KmCham): đầu tia chạm 0,02 s trước cú trúng chính của StageView nên bỏ nhịp đầu; rung nhỏ dồn dập, tia
                // kim loại bắn ngược rồi khựng (ít hơn: bông khung đã lớn), nhịp mạnh lúc tắt
                Every(tCham, tTat, 7, x =>
                {
                    Shake?.Invoke(0.05f * manh);
                    KmNhip(0.4f);
                });
                Every(tCham, tTat, 16, x =>
                {
                    float sd = rng.Next(2) == 0 ? -1 : 1;
                    KmTiaLua(cham, new Vector2(sd * U(0.5f, 1.2f), -U(0.2f, 0.9f)), U(380, 720), U(5, 8), KmNang[3 + rng.Next(2)]);
                });
                At(tTat, () => KmNhip(0.6f));
            }
            At(tBan, () =>
            {
                Shake?.Invoke(0.2f * manh);
                FlashScreen?.Invoke(VmFlash);
                KmChop(dinh, 2.4f * R, 0.07f, KmNang);
                KmVong(_ => dinh, 0.24f, R, 3.4f * R, VmVang[3], 1, 0.85f);
                if (!tiaFb) KmTia(dinh, cham, tTat - tBan, hw, KmNang, Back, daiCham / Mathf.Max(0.04f, lao), rut).sizeFn = (z, f) => Rong(f);
            });
            // va chạm liên tục + đối thủ chớp, giật theo nhịp tia (NuocPulse); đầu tia chạm 0,02 s trước cú trúng chính của StageView nên bỏ nhịp đầu
            if (!tiaFb) KmCham(cham, new Vector2(0, 1), tBan + lao, tTat + 0.5f * rut, 1.15f * hw, KmNang, manh, 0);
            // tia lửa văng hai bên thân tia (tia vẽ sẵn: theo bề dày khung, đầu tia vươn từ tCham − tVuon)
            float tMoc = tCham - tVuon;
            Every(tMoc + 0.03f, tTat, 22, x =>
            {
                float v = U(0.1f, 0.95f) * Mathf.Clamp01((T - T0 - tMoc) / tVuon);
                var p = Vector2.Lerp(dinh, cham, v);
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                KmTiaLua(p + new Vector2(sd * (tiaFb ? 0.5f * dayTia : hw * Rong(v)), 0), new Vector2(sd, U(-0.4f, 0.3f)), U(260, 460), U(5, 7),
                    VmVang[2 + rng.Next(2)]);
            });
            for (int i = 0; i < hanh.Length; i++)
            {
                var p = Cot(hanh[i]);
                At(tMoc + tVuon * fh[i], () =>      // lúc đầu tia giáng tới hành tinh này: chớp nhỏ, vòng bung, tia
                {
                    KmChop(p, 1.8f * R, 0.06f, KmNang);
                    RbVong(p, 0.22f, R, 3f * R, VmVang[2]);
                    RbTia(p, R, 5, 160, 300, 100);
                });
            }
            // 5. trúng: nổ mặt trời KR5 (lõi sau lưng đối thủ), vòng cung dẹt hai đợt, bụi, nứt đất, khói cụm
            At(L0, () =>
            {
                Shake?.Invoke(0.55f * manh);
                FlashScreen?.Invoke(VmFlash);
                VmNoVang(foeBody + new Vector2(0, -0.1f * tH), foeFeet, foeBody, tH, dir, 1.25f * manh);
                KmCung(foeFeet + new Vector2(0, 2), 0.15f * tH, 1.25f * tH * manh, 0.5f, VmVang[3], 0.3f, Floor, 30.6f, 0.85f);
                BuiDap(foeFeet, tH, 1.2f * manh, 8);
                RbNut(foeFeet + new Vector2(0, 2), tH * manh);
            });
            At(L0 + 0.12f, () => KmCung(foeFeet + new Vector2(0, 2), 0.3f * tH, 1.6f * tH * manh, 0.5f, VmVang[2], 0.3f, Floor, 30.6f, 0.7f));
            At(L0 + 0.35f, () =>
            {
                for (int i = 0; i < 2; i++)
                    KmKhoi(foeBody + new Vector2(U(-0.25f, 0.25f) * tH, -U(0.2f, 0.45f) * tH), new Vector2(U(-20, 20), -U(40, 70)), U(0.13f, 0.16f) * tH,
                        U(1.0f, 1.3f), Back, 0, 2);
                for (int i = 0; i < 4; i++) Ash(foeBody + U2(-26, 26));
            });
            return L0;
        }

        // CHIÊU CUỐI "Nhật Thực Thiên Giáng": bay lên, quỹ đạo, nhật thực (màn tối), ba thiên thạch nện. Trả giây tới lúc trúng (= lead).
        public float NVuaNhat(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float L0 = Mathf.Max(0.8f, lead), k = L0 / VmSLead, T0 = T;
            var B = VmLay(dang);
            float manh = dang == 1 ? 0.8f : 1f;
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            Vector2 Sun(float t) => San(VmMau(B.smx, B.smy, (t - T0) / k));
            Vector2 Rot(int j, float t) => foeBody + new Vector2(dir * VmMau(B.tx[j], B.ty[j], (t - T0) / k).x * casterH,
                -VmMau(B.tx[j], B.ty[j], (t - T0) / k).y * casterH);
            float R = Mathf.Clamp(0.08f * casterH, 9, 20) * manh;
            float tBay = VmSBay * k, tQuy = VmSQuy * k, tThuc = VmSThuc * k, tPhong = VmSPhong * k, tSang = VmSSang * k;
            var nguc = casterFeet + new Vector2(0, -0.72f * casterH);
            KmPal();

            // 1. vỗ cánh bay lên: gió cuốn bụi hai bên chân, vòng gió
            At(tBay, () =>
            {
                Shake?.Invoke(0.12f * manh);
                Ring(casterFeet + new Vector2(0, 2), 0.4f, 0.1f * casterH, 0.7f * casterH, C(236, 230, 214), 0.3f);
                for (int i = 0; i < 10; i++)
                {
                    float sd = i % 2 == 0 ? -1 : 1;
                    BuiTro(casterFeet + new Vector2(sd * U(0.05f, 0.4f) * casterH, U(-4, 2)), new Vector2(sd * U(90, 220), -U(10, 50)), U(0.5f, 0.8f), 4,
                        U(9, 14), Back);
                }
            });
            // 2. quỹ đạo: ba vệt lấp lánh quay quanh vua (Sao Thủy nhanh, Sao Hỏa chậm)
            float[] rq = { 0.45f, 0.62f, 0.8f }, wq = { 7.5f, 5f, 3.4f };
            for (int j = 0; j < 3; j++)
            {
                int jj = j;
                Every(tQuy, tThuc - 0.1f * k, 16, x =>
                {
                    float a = wq[jj] * (T - T0) + 2.1f * jj;
                    var p = nguc + new Vector2(Mathf.Cos(a) * rq[jj] * casterH, Mathf.Sin(a) * 0.32f * rq[jj] * casterH);
                    var e = Ember(p, new Vector2(U(-15, 15), U(-15, 15)), U(0.35f, 0.55f), U(4, 6.5f) * manh, Mathf.Sin(a) > 0 ? Front : Back);   // đốm nhỏ
                    e.col = VmVang[2 + (jj & 1)];
                });
            }
            // 3. Mặt Trời hút năng lượng khi trượng giơ lên trời
            VmTu(Sun, tThuc - 0.7f * k, tThuc, R, manh);
            // 4. NHẬT THỰC: màn tối ~1 s, vành nhật hoa trắng, tia trắng
            At(tThuc, () =>
            {
                Shake?.Invoke(0.18f * manh);
                var c = Sun(T);
                KmChop(c, 2.6f * R, 0.08f, KmNang);
                RbVong(c, 0.35f, 1.2f * R, 4.2f * R, VmTrang);
                RbTia(c, 1.2f * R, 10, 160, 300, 0);
            });
            Every(tThuc, tSang, 16, x => FlashScreen?.Invoke(VmToi));
            Every(tThuc + 0.08f, tSang, 10, x =>
            {
                var c = Sun(T);
                RbVong(c, 0.3f, 1.4f * R, 2.6f * R, VmTrang);
            });
            // 5. ba hành tinh vọt lên trời
            At(tPhong, () =>
            {
                var c = Sun(T);
                for (int i = 0; i < 3; i++)
                {
                    var q = Spark(c + U2(-R, R), new Vector2(U(-0.2f, 0.2f), -1), U(700, 900), 0.4f, 12, 0, Front, 0.5f);
                    q.col = VmVang[3];
                }
                KmChop(c, 1.6f * R, 0.07f, KmNang);
            });
            // 6. ba thiên thạch (rig vẽ): đuôi lửa hạt bám theo, nện lần lượt; cú cuối (Trái Đất) rất lớn
            for (int j = 0; j < 3; j++)
            {
                int jj = j;
                float th = VmSMHien[j] * k, tn = VmSNo[j] * k;
                float sc = (j == 2 ? 1.5f : 0.85f) * manh;
                // đuôi thiên thạch (2026-11-18): lưỡi lửa + KHÓI CỤM LIỀN chia theo quãng bay (KR5), không còn chuỗi lưỡi lửa rời theo giờ
                float tDuoi = Mathf.Min(tn, VmSMTat[j] * k + 0.03f) - th;
                int demD = 0;
                if (tDuoi > 0.02f)
                    At(th, () =>
                    {
                        // khung vẽ sẵn (2026-11-19): lửa bọc + đuôi lửa là khung "cau_lua" bám theo thiên thạch của rig, SAU tướng (đá của rig vẫn nằm
                        // trên), chỉ trong lúc thiên thạch hiện; hướng = từ giữa quãng rơi tới tâm đối thủ (rig rơi thẳng); thay chuỗi lưỡi lửa rời.
                        // Khói cụm, tia giữ. Chưa nhập ảnh: lưỡi lửa cũ
                        float tm = 0.5f * (VmSMHien[jj] + VmSMTat[jj]) * k, hien = (VmSMTat[jj] - VmSMHien[jj]) * k;
                        bool fb = KmCauBam(t => Rot(jj, t), hien, 0.7f * tH * sc, foeBody - Rot(jj, T0 + tm));
                        // vệt khói đuôi (2026-11-19, người dùng: "các fireball ... nên thêm trail smoke vào"): FbKhoiDuoi nhả giữa đuôi lửa của
                        // cau_lua (lùi 0,6 cao khung), dày (40 cụm/giây vì thiên thạch chỉ hiện ~0,17–0,27 s), cụm 0,22 thân × cỡ (tối đa 0,3), sau tướng
                        // dưới cau_lua; thay chuỗi khói một múi
                        bool fbKhoi = KmDuoiKhoi(t => Rot(jj, t), hien, Mathf.Min(0.22f * sc, 0.3f) * tH, 0.6f * 0.7f * tH * sc, 40, Back, 18);
                        KmDuoi(t => Rot(jj, t), tDuoi, 0.11f * tH * sc, (pt, ud) =>
                        {
                            if (!fb)
                            {
                                var q = Flame(pt + U2(-0.08f, 0.08f) * tH * sc, -ud * U(60, 140) + new Vector2(0, -U(40, 90)), U(0.18f, 0.26f), 0.08f * tH * sc,
                                    0.13f * tH * sc, "tron", "luat", Back, 2.5f, -150, 1.4f, 0, 0.1f);
                                Tongue(q, -1, 0.3f);
                            }
                            if (!fbKhoi && demD++ % 2 == 0)
                                KmKhoi(pt - ud * 0.1f * tH * sc + U2(-3, 3), new Vector2(U(-10, 10), -U(20, 40)), U(0.09f, 0.11f) * tH * sc, U(0.45f, 0.65f), Back,
                                    0.8f, 0, null, 0.15f, true);
                            if (U(0, 1) < 0.2f) KmTiaLua(pt, -ud + U2(-0.4f, 0.4f), U(260, 420), U(5, 7), KmLua[4]);
                        });
                    });
                At(tn, () =>
                {
                    var tgt = foeBody + new Vector2(-dir * 0.04f * tH, -0.05f * tH);
                    Shake?.Invoke(jj == 2 ? 1.0f * manh : (0.32f + 0.08f * jj) * manh);
                    if (jj < 2) KmNhip(jj == 0 ? 1 : 0.5f);   // thiên thạch thứ ba là cú trúng chính (StageView)
                    VmNoLua(tgt, foeFeet, tH, sc, jj == 2 ? 10 : 4, dir);
                    if (jj == 2)
                    {
                        FlashScreen?.Invoke(FlashSet);
                        RbNut(foeFeet + new Vector2(0, 2), 1.3f * tH * manh);
                        RbCot(foeFeet, tH, 0.45f, 1.1f * manh);
                    }
                });
                if (j == 2)
                    At(tn + 0.1f, () =>   // cú cuối: đợt nổ thứ hai sau lưng (lửa đỏ cam), thay cầu lửa CauNo trùm kín đối thủ
                    {
                        var th0 = Th;
                        Th = VmLuaTh;
                        KmNhip(0.4f);
                        KmNo(foeBody + new Vector2(dir * 0.08f * tH, -0.12f * tH), foeFeet, tH, 1.1f * manh, "luat", dir);
                        Th = th0;
                    });
            }
            // 7. Mặt Trời sáng lại: chớp vàng, tia
            At(tSang, () =>
            {
                var c = Sun(T);
                KmChop(c, 2.2f * R, 0.07f, KmNang);
                RbVong(c, 0.3f, R, 3.4f * R, VmVang[2]);
                RbTia(c, R, 8, 150, 280, 60);
            });
            At(L0 + 0.15f, () =>
            {
                Shake?.Invoke(0.4f * manh);
                KmCung(foeFeet + new Vector2(0, 2), 0.3f * tH, 1.9f * tH * manh, 0.55f, KmLua[4], 0.3f, Floor, 30.6f, 0.75f);
            });
            Every(L0, L0 + 0.7f, 5, x => KmDomCum(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, -U(0, 0.7f) * tH), new Vector2(U(-40, 40), -U(90, 170)),
                KmLua[3 + rng.Next(2)]));
            At(L0 + 0.4f, () =>
            {
                for (int i = 0; i < 3; i++)
                    KmKhoi(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.2f, 0.55f) * tH), new Vector2(U(-20, 20), -U(40, 70)), U(0.14f, 0.18f) * tH,
                        U(1.0f, 1.4f), Back, 0, 2);
                for (int i = 0; i < 5; i++) Ash(foeBody + U2(-32, 32));
            });
            return L0;
        }
    }
}
