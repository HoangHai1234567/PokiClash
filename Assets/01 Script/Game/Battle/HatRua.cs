// Bộ HỎA QUY (2026-11-13, rùa golem lửa, suất nguu_quyen đảo Hỏa; rig ArtGen/Spine/rua_lua_rig.py).
// Người dùng: chiêu mana "đứng lên nhẹ há mồm, tụ cầu lửa rồi bắn"; chiêu cuối "tụ cầu lửa trên sừng của tướng, lửa sẽ được hút từ lửa trên
// lưng tướng, khi hút hết lửa phóng cầu năng lượng vào địch". Rig chỉ diễn thân (lửa trên lưng co tắt từng ngọn, hất sừng); cầu lửa và dải
// lửa bị hút là việc của lớp hạt này.
// Đi đường "n_" (StageView.PreFx → PlayNuoc: phát từ đầu clip, biết `lead` = giờ tới khung trúng của clip) vì cầu phải tụ TRƯỚC khung nhả.
// Màu theo Themes["nguu_quyen"] (bảng "lua", mảnh văng đá xám lam).
// - n_cau_sung (chiêu cuối): từng ngọn lửa trên lưng (thứ tự và giờ như clip) nhả một dải lưỡi lửa nhỏ bay vòng lên rồi bị hút vào CẦU LỬA
//   đang lớn dần trên mũi sừng gần; cầu đầy thì nháy vòng, toé tia; khung hất sừng cầu rời sừng bay tới đối thủ, nổ lớn.
// - n_cau_rua (chiêu mana): than hồng hút vào mõm, cầu lửa lớn dần ở mõm trong lúc tướng há mồm; khung nhả thì cầu bay tới đối thủ, nổ.
// Vị trí mũi sừng theo giây của clip và chỗ từng ngọn lửa đo trên rig đã xuất (phần của chiều cao game, x về phía trước, y lên): đổi clip
// skill hay hình thì đo lại bằng đoạn mã trong ArtGen/Spine/inbox/rua_lua_ghichu.md mục 7.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // mốc giờ của clip skill (rua_lua_rig.py): hút ngọn đầu 0,32 s, mỗi ngọn cách 0,125 s và co trong 0,30 s; cầu đầy 1,37 s; hất sừng
        // (khung trúng của clip) 1,63 s
        const float RuaHut0 = 0.32f, RuaHutCach = 0.125f, RuaHutDai = 0.30f, RuaDay = 1.37f, RuaNem = 1.63f;
        public const float CauSungBay = 0.30f;  // giây cầu bay từ mũi sừng tới đối thủ
        public const float CauMiengBay = 0.36f; // giây cầu bay từ mõm tới đối thủ
        const float RuaTu = 0.54f;              // chiêu mana: cầu tụ ở mõm chừng ấy giây trước khung nhả (clip cast: tu 0,36 → phun 0,90)

        static readonly float[] SungT = { 0f, 0.30f, 1.37f, 1.50f, 1.57f, 1.60f, 1.63f, 1.80f };
        static readonly Vector2[] SungP =
        {
            new Vector2(0.434f, 0.706f), new Vector2(0.512f, 0.621f), new Vector2(0.456f, 0.619f), new Vector2(0.368f, 0.642f),
            new Vector2(0.338f, 0.670f), new Vector2(0.498f, 0.617f), new Vector2(0.539f, 0.505f), new Vector2(0.564f, 0.504f),
        };
        // giữa từng ngọn lửa trên lưng lúc nó bắt đầu bị hút, theo thứ tự hút: trên đuôi, trái, giữa trái, cao nhất, phải, nhỏ, sau sừng
        static readonly Vector2[] LuaLung =
        {
            new Vector2(-0.19f, 0.53f), new Vector2(-0.05f, 0.53f), new Vector2(0.11f, 0.51f), new Vector2(0.23f, 0.49f),
            new Vector2(0.32f, 0.35f), new Vector2(0.31f, 0.24f), new Vector2(0.38f, 0.19f),
        };

        // DẠNG 1 (rùa non chibi vẽ riêng, hướng "ve" của rua_lua_non_ve.py, 2026-11-14; trước là bản ghép "chibi_1"): sừng là mầm ngắn nên mũi
        // sừng thấp và lùi hơn. Đo bằng ArtGen/Spine/inbox/rua_lua_non/_do_hat.py
        static readonly Vector2[] SungPNon =
        {
            new Vector2(0.310f, 0.633f), new Vector2(0.398f, 0.544f), new Vector2(0.352f, 0.528f), new Vector2(0.286f, 0.531f),
            new Vector2(0.254f, 0.557f), new Vector2(0.337f, 0.576f), new Vector2(0.359f, 0.526f), new Vector2(0.384f, 0.525f),
        };
        // chỉ MỘT ngọn lửa giữa lưng, co chậm suốt quãng tụ (rig: HC_DAI = RuaDay − RuaHut0 − 0,08)
        static readonly Vector2[] LuaNon = { new Vector2(0.24f, 0.54f) };

        static Vector2 SungMui(Vector2[] P, float tc)
        {
            if (tc <= SungT[0]) return P[0];
            for (int i = 1; i < SungT.Length; i++)
                if (tc <= SungT[i]) return Vector2.Lerp(P[i - 1], P[i], (tc - SungT[i - 1]) / (SungT[i] - SungT[i - 1]));
            return P[P.Length - 1];
        }

        // lõi cầu lửa bám theo một điểm chạy (như lõi của Fireball): tam(giờ sân) trả tâm, r bán kính lúc sinh
        void LoiCau(System.Func<float, Vector2> tam, float r)
        {
            var q = Flame(tam(T), Vector2.zero, U(0.12f, 0.18f), r * 0.62f, r * U(0.9f, 1.08f), "tron", Th.pal, Front, 0, 0, 1.9f, 0, 0);
            q.off = U2(-0.2f, 0.2f) * r;
            q.upd = (z, dt, s) =>
            {
                z.vel = Vector2.zero;
                z.pos = tam(s.T) + z.off;
            };
        }

        // vụ nổ lớn ở đối thủ lúc cầu chạm; sc: cỡ (chiêu cuối 1,4; chiêu mana 0,9)
        void CauNo(Vector2 tgt, Vector2 foeFeet, Vector2 foeBody, float tH, float dir, float sc)
        {
            Shake?.Invoke(0.5f * sc);
            Explode(tgt, sc, tH);
            Ring(foeFeet + new Vector2(0, 2), 0.42f, 0.16f * tH, 0.8f * tH * sc, Th.ring);
            int n = Mathf.RoundToInt(8 * sc);
            for (int i = 0; i < n; i++)
            {
                float a = 6.28f * (i + U(0, 0.7f)) / n; // rải đều góc
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f);
                var q = Flame(tgt + d * U(6, 14), d * U(260, 460) * Mathf.Sqrt(sc), U(0.3f, 0.44f), 9, U(18, 25) * Mathf.Sqrt(sc), "tron", Th.pal,
                    i % 3 == 0 ? Front : Back, 4.2f, -160, 1.5f, 0.3f);
                Tongue(q, 1, 0.15f);
                q.smokeGroup = Back;
            }
            Extra(tgt, Mathf.RoundToInt(5 * sc), 400, Front);
            for (int i = 0; i < 8; i++)
            {
                float a = U(0, 6.28f);
                Spark(tgt, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f), U(260, 460));
            }
        }

        // CẦU LỬA TRÊN SỪNG (chiêu cuối). lead: giây từ đầu clip skill tới khung hất sừng. Trả giây tới lúc cầu chạm đối thủ.
        // non: dạng 1 (rùa non): cầu nhỏ hơn, một dải lửa dài, mũi sừng ngắn; vụ nổ nhẹ hơn
        public float NCauSung(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, bool non = false)
        {
            var sung = non ? SungPNon : SungP;
            var nguon = non ? LuaNon : LuaLung;
            float L = Mathf.Max(0.6f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t00 = L - RuaNem, goc = T;                     // t00: giờ (tính từ lúc gọi) của giây 0 clip
            float R = Mathf.Clamp((non ? 0.155f : 0.2f) * casterH, 13, 36); // bán kính cầu lúc đầy
            Vector2 Rig(Vector2 p) => casterFeet + new Vector2(dir * p.x, -p.y) * casterH;
            float Nap(float tc) => Mathf.Clamp01((tc - RuaHut0 - 0.14f) / (RuaDay - RuaHut0 - 0.14f));
            float Rt(float tc) => R * (0.2f + 0.8f * Mathf.Sqrt(Nap(tc)));
            // tâm cầu: ngay trên mũi sừng, hơi chếch ra trước (cầu ngồi trên mũi sừng chứ không nuốt mũi sừng)
            Vector2 Tam(float tc) => Rig(SungMui(sung, tc)) + new Vector2(dir * 0.2f, -0.8f) * Rt(tc);
            float tA = Mathf.Max(0.02f, t00 + RuaHut0 + 0.12f);
            float tDay = Mathf.Max(tA + 0.05f, t00 + RuaDay);
            Vector2 TamT(float t) => Tam(t - goc - t00);
            float RtT(float t) => HoaNhip(Rt(t - goc - t00), t, goc + L);

            // cầu lửa nhiều múi lớn dần trên mũi sừng (nhịp đập, nén trước lúc hất, chớp lúc hất) + hai vòng co; vệt quanh vòng thưa (lửa chính từ lưng)
            // khung vẽ sẵn (2026-11-19): cầu là "cau_lua" (HatFbHoa.cs: đứng yên thì đuôi lửa bốc lên, ngả về phía đối thủ) nên bỏ lưỡi lửa liếm quanh
            // cầu và chuỗi lưỡi đuôi lúc bay
            bool fb = HasFb("cau_lua");
            HoaTuCau(TamT, R, tA - 0.02f, L, true, 0.35f, RtT, dir);
            // từng ngọn lửa trên lưng (thứ tự, giờ như clip): nháy tia ở gốc, lưỡi lửa nhỏ co lại tại gốc, nhả VỆT lửa xoắn ốc nhanh dần vào cầu
            float chieu = dir;
            for (int i = 0; i < nguon.Length; i++)
            {
                var src = Rig(nguon[i]);
                float ts = Mathf.Max(0.02f, t00 + RuaHut0 + (non ? 0 : RuaHutCach * i));
                float dai = non ? RuaDay - RuaHut0 - 0.08f : RuaHutDai; // một ngọn: nhả dải lửa thưa hơn nhưng suốt quãng tụ
                At(ts, () =>
                {
                    for (int j = 0; j < 3; j++) Spark(src + U2(-6, 6), new Vector2(dir * U(0.1f, 0.9f), -U(0.5f, 1f)), U(160, 280), 0, 6);
                });
                Every(ts, ts + dai, non ? 24 : 34, x =>
                {
                    var p0 = src + new Vector2(U(-0.05f, 0.05f), -U(0, 0.07f)) * casterH;
                    HoaHut(TamT, RtT, p0, U(0.34f, 0.46f), U(0, 1) < 0.5f ? Pal[Th.pal][1] : Pal[Th.pal][2], chieu, goc + L + 0.02f);
                });
                Every(ts, ts + dai, 9, x => HoaLuoi(Flame(src + U2(-5, 5), new Vector2(U(-15, 15), -U(60, 120)), U(0.18f, 0.24f), 5, U(9, 12) * (1 - 0.5f * x), "tron",
                    Th.pal, Front, 2, -200, 1.4f, 0, 0), 1, 0.7f, 0));
            }
            // lưỡi lửa liếm ra từ thân cầu
            if (!fb)
                Every(tA + 0.1f, L, x => 8 + 16 * x, x =>
                {
                    float r = RtT(T), a = U(0, 6.28f);
                    var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    HoaLuoi(Flame(TamT(T) + o * r * 0.55f, o * U(30, 90) + new Vector2(-dir * U(10, 50), -U(40, 110)), U(0.2f, 0.3f), r * 0.34f,
                        r * U(0.46f, 0.6f), "tron", Th.pal, Front, 3, -160, 1.5f, 0, 0), 1, 0.5f, 0);
                });
            // cầu đầy: vòng co sát cầu, toé tia; giữ tới lúc hất sừng thì cụm tàn lửa lách tách quanh cầu
            At(tDay, () =>
            {
                Shake?.Invoke(0.12f);
                var c = Tam(RuaDay);
                HoaVongCo(TamT, R * 2.2f, R * 1.05f, 0.2f, Th.ring2);
                for (int j = 0; j < 5; j++)
                {
                    float a = 6.28f * (j + U(0, 0.7f)) / 5;
                    var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    Spark(c + o * R, o, U(200, 340), 0, 6, 120);
                }
            });
            Every(tDay, L, 6, x =>
            {
                float a = U(0, 6.28f);
                var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                HoaTan(TamT(T) + o * R * 1.1f, new Vector2(o.x, o.y - 0.6f) * U(40, 110), U(0.3f, 0.5f), 3);
            });

            // hất sừng: cầu rời mũi sừng bay tới đối thủ (bắn nhanh rồi vào đích); đuôi lưỡi lửa đứng tại chỗ nguội dần, khói đuôi thành cụm, tia
            var from = Tam(RuaNem);
            var tgt = foeBody + new Vector2(-dir * 0.08f * tH, 0);
            var d0 = Unit(tgt - from);
            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - goc - L) / CauSungBay);
                return from + (tgt - from) * (x * (0.45f + 0.55f * x)) + new Vector2(0, -0.1f * casterH) * Mathf.Sin(Mathf.PI * x);
            }
            At(L, () =>
            {
                Shake?.Invoke(0.2f);
                for (int j = 0; j < 5; j++) Spark(from, -d0 + U2(-0.7f, 0.7f), U(220, 380), 0, 6);
                System.Func<float, float> rb = t => R * (1 + 0.06f * Mathf.Sin(t * 40));
                // vệt khói đuôi (2026-11-19 chiều): cụm 0,22–0,35 thân theo cỡ cầu
                if (!fb || HoaFbCau(Bay, rb, CauSungBay + 0.01f, Front, true, 0, KhoiCo(R, tH)) == null) HoaCau(Bay, rb, CauSungBay + 0.01f);
            });
            if (!fb)
                Every(L, L + CauSungBay, 50, x =>
                {
                    var q = Flame(Bay(T) - d0 * R * 0.3f + U2(-0.4f, 0.4f) * R, -d0 * U(60, 140) + new Vector2(-d0.y, d0.x) * U(-80, 80) + new Vector2(0, -20),
                        U(0.2f, 0.3f), R * 0.8f, R * 0.8f, "tron", Th.pal, Front, 3, -140, 1.4f, 0, 0);
                    HoaLuoi(q, 1, 0.2f, 0);
                    q.sizeFn = (z, k) => z.r1 * Mathf.Pow(1 - k, 1.1f);
                });
            HoaDuoiKhoi(t => Bay(t) - d0 * R, L + 0.03f, L + CauSungBay, 11, 14);
            Every(L, L + CauSungBay, 14, x => Spark(Bay(T), -d0 + U2(-0.6f, 0.6f), U(160, 280), 0, 6));

            // chạm: nổ lớn KR5, nổ phụ, khói cụm và tro
            float tNo = L + CauSungBay;
            At(tNo, () =>
            {
                NuocPulse?.Invoke(non ? 0.8f : 1f);
                HoaCauNo(tgt, foeFeet, tH, dir, non ? 1.1f : 1.4f);
            });
            At(tNo + 0.13f, () =>
            {
                Shake?.Invoke(non ? 0.2f : 0.3f);
                HoaNo(tgt + new Vector2(dir * U(4, 20), U(-26, 6)), non ? 0.5f : 0.7f, tH, null, Front, dir); // khung vẽ sẵn: lật theo hướng cầu bay
            });
            At(tNo + 0.34f, () =>
            {
                for (int i = 0; i < 3; i++)
                    HoaKhoi(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.15f, 0.5f) * tH), U(0.13f, 0.17f) * tH, Back, null, 0, true, 0.5f);
                for (int i = 0; i < 4; i++) Ash(foeBody + U2(-28, 28));
            });
            return tNo;
        }

        // bán kính cầu đang tụ (đo theo rig) thêm nhịp đập 7 nhịp/giây ±6 % (2026-11-19 đêm, người dùng: cầu "nhìn hơi tĩnh"; trước ~4 nhịp ±7 %) và cú
        // nén còn 0,78 trong 0,07 s trước giờ nhả `nha` (giờ sân tuyệt đối)
        static float HoaNhip(float r, float t, float nha)
        {
            r *= 1 + 0.06f * Mathf.Sin(t * 44);
            float con = nha - t;
            return con >= 0 && con < 0.07f ? r * Mathf.Lerp(0.78f, 1, con / 0.07f) : r;
        }

        // CẦU LỬA Ở MÕM (chiêu mana). mouth: chỗ nhả ở khung trúng của clip cast (game.muzzle = xương `mieng`). Trả giây tới lúc chạm.
        public float NCauMieng(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.02f, L - RuaTu), goc = T;
            float R = Mathf.Clamp(0.125f * casterH, 11, 22);
            var tam = mouth + new Vector2(dir * 0.3f, 0.1f) * R;

            // tụ (2026-11-18): vệt lửa xoắn ốc hút vào mõm, hai vòng co, cầu nhiều múi lớn dần theo nhịp đập, nén rồi chớp lúc nhả; khung vẽ sẵn
            // (2026-11-19): cầu là "cau_lua" (đã có lửa) nên bỏ lưỡi lửa liếm quanh cầu và chuỗi lưỡi đuôi lúc bay
            bool fb = HasFb("cau_lua");
            var rt = HoaTuCau(t => tam, R, t0, L, true, 1, null, dir);
            if (!fb)
                Every(t0 + 0.14f, L, 12, x =>
                {
                    float r = rt(T), a = U(0, 6.28f);
                    var o = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    HoaLuoi(Flame(tam + o * r * 0.5f, o * U(20, 70) + new Vector2(0, -U(40, 90)), U(0.18f, 0.26f), r * 0.34f, r * 0.55f, "tron", Th.pal, Front,
                        3, -160, 1.5f, 0, 0), 1, 0.5f, 0);
                });

            // nhả: cầu bay vòng cung nhẹ tới đối thủ
            var tgt = foeBody + new Vector2(-dir * 0.06f * tH, 0);
            var d0 = Unit(tgt - tam);
            Vector2 Bay(float t)
            {
                float x = Mathf.Clamp01((t - goc - L) / CauMiengBay);
                return tam + (tgt - tam) * x + new Vector2(0, -34) * Mathf.Sin(Mathf.PI * x);
            }
            At(L, () =>
            {
                Shake?.Invoke(0.14f);
                for (int j = 0; j < 4; j++) Spark(tam, -d0 + U2(-0.7f, 0.7f), U(180, 320), 0, 6);
                System.Func<float, float> rb = t => R * (1 + 0.06f * Mathf.Sin(t * 40));
                // vệt khói đuôi (2026-11-19 chiều): cụm 0,22–0,35 thân theo cỡ cầu
                if (!fb || HoaFbCau(Bay, rb, CauMiengBay + 0.01f, Front, true, 0, KhoiCo(R, tH)) == null) HoaCau(Bay, rb, CauMiengBay + 0.01f);
            });
            if (!fb)
                Every(L, L + CauMiengBay, 40, x =>
                {
                    var q = Flame(Bay(T) - d0 * 4 + U2(-7, 7), -d0 * U(60, 130) + new Vector2(-d0.y, d0.x) * U(-70, 70) + new Vector2(0, -20), U(0.18f, 0.26f),
                        R * 0.85f, R * 0.85f, "tron", Th.pal, Front, 3, -140, 1.4f, 0, 0);
                    HoaLuoi(q, 1, 0.2f, 0);
                    q.sizeFn = (z, k) => z.r1 * Mathf.Pow(1 - k, 1.1f);
                });
            HoaDuoiKhoi(t => Bay(t) - d0 * 22, L + 0.03f, L + CauMiengBay, 10, 13);
            Every(L, L + CauMiengBay, 12, x => Spark(Bay(T), -d0 + U2(-0.6f, 0.6f), U(140, 260), 0, 6));
            float tNo = L + CauMiengBay;
            At(tNo, () => HoaCauNo(tgt, foeFeet, tH, dir, 0.9f));
            return tNo;
        }
    }
}
