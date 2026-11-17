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
        static readonly Color[] VmVang = { C(236, 138, 34), C(252, 192, 60), C(255, 232, 140), C(255, 252, 232) };
        static readonly Color VmTrang = C(255, 250, 236), VmToi = new Color(0.05f, 0.03f, 0.1f, 0.85f);
        static readonly Color VmFlash = new Color(1f, 0.95f, 0.72f, 0.4f);
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
        void VmTu(System.Func<float, Vector2> tam, float t0, float t1, float R, float manh)
        {
            Every(t0, t1, x => (14 + 30 * x) * manh, x => RbHutXa(tam, U(1.6f, 2.8f) * R, U(0.32f, 0.5f), U(6, 9) * manh));
            Every(t0 + 0.05f, t1, x => 6 + 10 * x, x => RbLiem(tam(T), R * 0.8f));
        }

        // đường lửa sáng chạy dọc mặt đất từ a tới b trong khoảng [t0, t1]: tia vàng phụt lên, lưỡi lửa nhỏ, bụi
        void VmDuongLua(Vector2 a, Vector2 b, float t0, float t1, float H, float manh)
        {
            float t00 = T;
            Every(t0, t1, 70, x =>
            {
                float u = Mathf.Clamp01((T - t00 - t0) / Mathf.Max(0.05f, t1 - t0));
                var p = Vector2.Lerp(a, b, u) + new Vector2(U(-6, 6), U(-3, 2));
                Spark(p, new Vector2(U(-0.3f, 0.3f), -1), U(160, 320) * manh, 0, 7, 500);
                var q = Flame(p, new Vector2(U(-20, 20), -U(60, 140)), U(0.18f, 0.28f), 0.05f * H * manh, 0.09f * H * manh, "tron", "nang",
                    U(0, 1) < 0.5f ? Back : Front, 2.5f, -200, 1.6f, 0, 0.1f);
                Tongue(q, 1, 0.3f);
                if (U(0, 1) < 0.35f) BuiTro(p, new Vector2(U(-40, 40), -U(10, 40)), U(0.4f, 0.6f), 3, U(7, 10), Back);
            });
        }

        // nổ năng lượng vàng (ấn / tia Mặt Trời trúng); sc: cỡ
        void VmNoVang(Vector2 tgt, Vector2 feet, Vector2 body, float tH, float dir, float sc)
        {
            RbChop(tgt, 1.1f * tH * sc, Front, 0.16f);
            CauNo(tgt, feet, body, tH, dir, sc);
            RbVong(tgt, 0.28f, 0.2f * tH, 0.9f * tH * sc, VmVang[2]);
            RbTia(tgt, 0.12f * tH, 10, 200, 380, 120);
            for (int i = 0; i < 8; i++) Ember(body + new Vector2(U(-0.3f, 0.3f) * tH, -U(0, 0.5f) * tH), new Vector2(U(-60, 60), -U(80, 160)));
        }

        // nổ lửa đỏ cam (thiên thạch nện); sc: cỡ
        void VmNoLua(Vector2 tgt, Vector2 feet, float tH, float sc, int nDa)
        {
            var th0 = Th;
            Th = VmLuaTh;
            RbChop(tgt, 0.8f * tH * sc, Front, 0.14f);
            Explode(tgt, sc, tH);
            Ring(feet + new Vector2(0, 2), 0.42f, 0.14f * tH, 0.95f * tH * sc, VmLuaTh.ring2, 0.3f);
            BuiDap(feet, tH, 1.1f * sc, 10);
            for (int i = 0; i < nDa; i++)
                Rock(feet + new Vector2(U(-0.3f, 0.3f) * tH, -6), new Vector2(U(-300, 300), -U(300, 560)), feet.y + U(-4, 8), U(8, 14) * sc);
            for (int i = 0; i < 6; i++)
            {
                float a = U(0, 6.28f);
                Spark(tgt, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f), U(260, 460));
            }
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
                var q = Flame(c + U2(-0.4f, 0.4f) * R, new Vector2(U(-50, 50), U(-50, 50)), U(0.16f, 0.24f), 0.7f * R, 1.1f * R, "tron", "nang", Front,
                    3, -100, 1.5f, 0, 0.15f);
                Tongue(q, 1, 0.3f);
                if (U(0, 1) < 0.5f) Spark(c, new Vector2(U(-1, 1), U(-1, 1)), U(120, 260));
            });
            // 3. đầu trượng nện đất: chớp, bụi, đá, vòng đất, rung
            var dat = new Vector2(Sun(T0 + tDap).x, casterFeet.y);
            At(tDap, () =>
            {
                var c = new Vector2(Sun(T).x, casterFeet.y);
                Shake?.Invoke(0.22f * manh);
                RbChop(c + new Vector2(0, -0.1f * casterH), 1.6f * R + 0.2f * casterH * manh, Front, 0.12f);
                Ring(c + new Vector2(0, 2), 0.32f, 0.06f * casterH, 0.5f * casterH * manh, VmVang[2], 0.3f);
                BuiDap(c, casterH, 0.8f * manh, 8);
                for (int i = 0; i < 5; i++) Rock(c + new Vector2(U(-20, 20), -4), new Vector2(U(-220, 220), -U(240, 420)), c.y + U(-3, 6), U(6, 10) * manh);
                for (int i = 0; i < 7; i++) Spark(c, new Vector2(U(-1, 1), -U(0.4f, 1)), U(220, 420));
            });
            // 4. đường lửa chạy dọc đất tới chân đối thủ
            VmDuongLua(dat, foeFeet, tDap + 0.02f, tAn, casterH, manh);
            // 5. ấn nở dưới chân đối thủ
            At(tAn, () =>
            {
                Ring(foeFeet + new Vector2(0, 2), 0.36f, 0.1f * tH, 0.75f * tH * manh, VmVang[2], 0.3f);
                Ring(foeFeet + new Vector2(0, 2), 0.3f, 0.6f * tH * manh, 0.3f * tH, VmVang[1], 0.3f);
                RbTia(foeFeet + new Vector2(0, -6), 0.1f * tH, 8, 180, 320, 300);
            });
            // 6. trúng: chớp, cột năng lượng phụt lên, tia lửa, than, rung
            At(L0, () =>
            {
                Shake?.Invoke(0.4f * manh);
                RbChop(foeBody, 0.9f * tH * manh, Front, 0.14f);
                RbCot(foeFeet, tH, 0.36f, manh);
                RbVong(foeBody, 0.26f, 0.15f * tH, 0.8f * tH * manh, VmVang[2]);
                for (int i = 0; i < 9; i++)
                {
                    float a = U(0, 6.28f);
                    Spark(foeBody, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f), U(240, 440));
                }
                Extra(foeBody, Mathf.RoundToInt(4 * manh), 360, Front);
            });
            Every(L0, L0 + 0.5f, 18, x => Ember(foeFeet + new Vector2(U(-0.25f, 0.25f) * tH, -U(0, 0.6f) * tH), new Vector2(U(-30, 30), -U(90, 170))));
            At(L0 + 0.3f, () =>
            {
                for (int i = 0; i < 3; i++) Smoke(foeBody + new Vector2(U(-0.2f, 0.2f) * tH, -U(0.05f, 0.4f) * tH), null, 0, 8, 20, Back);
            });
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
            // 4. TIA giáng xuống: lõi lửa năng lượng dọc cột (đã mọc tới đâu thì tới đó), dày dần sau mỗi hành tinh; tia văng hai bên
            At(tBan, () =>
            {
                Shake?.Invoke(0.2f * manh);
                FlashScreen?.Invoke(VmFlash);
                RbChop(dinh, 3.2f * R, Front, 0.14f);
            });
            Every(tBan, L0 + 0.32f * k, 110, x =>
            {
                float u = Mathf.Clamp01((T - T0 - tBan) / lao);             // phần cột đã có tia (từ đỉnh)
                float v = U(0, u);
                var p = Vector2.Lerp(dinh, foeBody, v);
                int qua = 0;
                foreach (var c in hanh)
                    if (p.y > Cot(c).y) qua++;                               // đã qua mấy hành tinh
                float w = (0.05f + 0.035f * qua) * casterH * manh;
                var q = Flame(p + new Vector2(U(-0.35f, 0.35f) * w, 0), new Vector2(U(-30, 30), U(120, 260)), U(0.14f, 0.22f), 0.7f * w, 1.1f * w, "tron",
                    "nang", Front, 3, 0, 1.7f, 0, 0.08f);
                Tongue(q, 1, 0.2f);
                if (U(0, 1) < 0.3f) Spark(p, new Vector2(U(0, 1) < 0.5f ? -1 : 1, U(-0.4f, 0.3f)), U(160, 320), 0, 7, 300);
            });
            for (int i = 0; i < hanh.Length; i++)
            {
                var p = Cot(hanh[i]);
                At(tBan + lao * Mathf.Clamp01((p.y - dinh.y) / dai), () =>      // lúc đầu tia giáng tới hành tinh này
                {
                    RbChop(p, 2.4f * R, Front, 0.1f);
                    RbVong(p, 0.22f, R, 3f * R, VmVang[2]);
                    RbTia(p, R, 6, 160, 300, 100);
                });
            }
            // 5. trúng: nổ mặt trời lớn, vòng sóng đất, bụi, tia, than, khói
            At(L0, () =>
            {
                Shake?.Invoke(0.55f * manh);
                FlashScreen?.Invoke(VmFlash);
                VmNoVang(foeBody, foeFeet, foeBody, tH, dir, 1.2f * manh);
                Ring(foeFeet + new Vector2(0, 2), 0.5f, 0.15f * tH, 1.25f * tH * manh, VmVang[1], 0.3f);
                BuiDap(foeFeet, tH, 1.2f * manh, 12);
                RbNut(foeFeet + new Vector2(0, 2), tH * manh);
            });
            At(L0 + 0.12f, () => Ring(foeFeet + new Vector2(0, 2), 0.5f, 0.3f * tH, 1.6f * tH * manh, VmVang[2], 0.3f));
            At(L0 + 0.35f, () =>
            {
                for (int i = 0; i < 5; i++) Smoke(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.05f, 0.5f) * tH), null, 0, 9, 24, Back);
                for (int i = 0; i < 6; i++) Ash(foeBody + U2(-26, 26));
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
                Every(tQuy, tThuc - 0.1f * k, 26, x =>
                {
                    float a = wq[jj] * (T - T0) + 2.1f * jj;
                    var p = nguc + new Vector2(Mathf.Cos(a) * rq[jj] * casterH, Mathf.Sin(a) * 0.32f * rq[jj] * casterH);
                    var e = Ember(p, new Vector2(U(-15, 15), U(-15, 15)), U(0.35f, 0.55f), U(7, 10) * manh, Mathf.Sin(a) > 0 ? Front : Back);
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
                RbChop(c, 3.4f * R, Front, 0.16f);
                RbVong(c, 0.35f, 1.2f * R, 4.2f * R, VmTrang);
                RbTia(c, 1.2f * R, 12, 160, 300, 0);
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
                for (int i = 0; i < 3; i++) Spark(c + U2(-R, R), new Vector2(U(-0.2f, 0.2f), -1), U(700, 900), 0.4f, 12, 0, Front, 0.5f);
                RbChop(c, 2f * R, Front, 0.1f);
            });
            // 6. ba thiên thạch (rig vẽ): đuôi lửa hạt bám theo, nện lần lượt; cú cuối (Trái Đất) rất lớn
            for (int j = 0; j < 3; j++)
            {
                int jj = j;
                float th = VmSMHien[j] * k, tn = VmSNo[j] * k;
                float sc = (j == 2 ? 1.5f : 0.85f) * manh;
                Every(th, Mathf.Min(tn, VmSMTat[j] * k + 0.03f), 70, x =>
                {
                    var p = Rot(jj, T);
                    var q = Flame(p + U2(-0.15f, 0.15f) * tH * sc, new Vector2(-dir * U(40, 120), -U(120, 260)), U(0.2f, 0.3f), 0.1f * tH * sc,
                        0.16f * tH * sc, "tron", "lua", Back, 2.5f, -150, 1.4f, 0.2f, 0.15f);
                    Tongue(q, 1, 0.2f);
                    if (U(0, 1) < 0.4f) Spark(p, new Vector2(-dir * U(0.2f, 0.6f), -1), U(200, 360));
                });
                At(tn, () =>
                {
                    var tgt = foeBody + new Vector2(-dir * 0.04f * tH, -0.05f * tH);
                    Shake?.Invoke(jj == 2 ? 1.0f * manh : (0.32f + 0.08f * jj) * manh);
                    VmNoLua(tgt, foeFeet, tH, sc, jj == 2 ? 10 : 4);
                    if (jj == 2)
                    {
                        FlashScreen?.Invoke(FlashSet);
                        RbNut(foeFeet + new Vector2(0, 2), 1.3f * tH * manh);
                        var th0 = Th;
                        Th = VmLuaTh;
                        CauNo(tgt, foeFeet, foeBody, tH, dir, 1.6f * manh);
                        Th = th0;
                        RbCot(foeFeet, tH, 0.45f, 1.1f * manh);
                    }
                });
            }
            // 7. Mặt Trời sáng lại: chớp vàng, tia
            At(tSang, () =>
            {
                var c = Sun(T);
                RbChop(c, 2.8f * R, Front, 0.14f);
                RbVong(c, 0.3f, R, 3.4f * R, VmVang[2]);
                RbTia(c, R, 8, 150, 280, 60);
            });
            At(L0 + 0.15f, () =>
            {
                Shake?.Invoke(0.4f * manh);
                Ring(foeFeet + new Vector2(0, 2), 0.55f, 0.3f * tH, 1.9f * tH * manh, VmLuaTh.ring2, 0.3f);
            });
            Every(L0, L0 + 0.7f, 16, x => Ember(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, -U(0, 0.7f) * tH), new Vector2(U(-40, 40), -U(90, 180))));
            At(L0 + 0.4f, () =>
            {
                for (int i = 0; i < 8; i++) Smoke(foeBody + new Vector2(U(-0.35f, 0.35f) * tH, -U(0.05f, 0.6f) * tH), null, 0, 10, 28, Back);
                for (int i = 0; i < 10; i++) Ash(foeBody + U2(-32, 32));
            });
            return L0;
        }
    }
}
