// Bộ BẠCH VIÊM HỔ (2026-11-14, bạch hổ mây lửa, suất hoa_tinh đảo Hỏa; rig ArtGen/Spine/hoa_ho_rig.py, dạng 1 hổ con HH_DANG=non).
// Người dùng: đòn thường "vả đối thủ"; chiêu mana "gồng người, ngửa đầu nhẹ hét to, impact cực lớn, tạo sóng xung kích cùng sóng nhiệt"; chiêu
// cuối "bật nhanh rồi biến mất, làm hiệu ứng âm bản màn chơi, hổ đánh liên tục (kiểu bay qua gây dam như chém) tầm 10-15 chiêu sau đó về vị
// trí ban đầu, các nhát đánh để lại lửa cháy tạo thành vụ nổ ở đối thủ". Rig diễn thân hổ (các lượt lướt là chính con hổ hiện 1 khung mỗi
// lượt); lớp này lo vệt vuốt, sóng gầm, sóng nhiệt, màn âm bản, vệt chém + sẹo lửa nằm lại trên đối thủ và vụ nổ.
// Đi đường "n_" (StageView.PreFx → PlayNuoc: phát từ đầu clip, biết `lead` = giờ tới khung trúng của clip). Màu theo Themes["hoa_tinh"].
// Mốc clip (giây): attack vả 0,50. cast: gồng 0,20, gầm 0,70 (= lead), hết gầm 1,45. skill: bật 0,36, tan hẳn 0,533, lượt k hiện ở
// 0,667 + 0,1 k (12 lượt; dạng 1: 6 lượt), hiện lại 0,633 + 0,1 n + 0,167, nổ sau đó 0,30 (= lead). Đổi clip thì sửa các hằng Ho*.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // màn chơi âm bản trong chừng ấy giây (StageView gắn; ô xem tướng không gắn thì bỏ qua)
        public Action<float> NegScreen;

        const float HoTu = 0.20f, HoGam = 0.70f, HoHetGam = 1.45f;
        const float HoBat = 0.36f, HoBien = 0.5333f, HoLuot0 = 0.6667f, HoBuoc = 0.1f;
        // độ dốc từng nhát chém của chiêu cuối (y xuống; x theo chiều lướt của lượt đó)
        static readonly float[] HoDoc = { -0.25f, 0.35f, -0.55f, 0.15f, 0.6f, -0.4f, 0.05f, -0.7f, 0.45f, -0.15f, 0.7f, -0.05f };

        static Color Dao(Color c) => new Color(1 - c.r, 1 - c.g, 1 - c.b, c.a);

        // VỆT LỬA: như vệt chém của Voọc Tướng (lá liễu quét dài ra trong 0,05 s rồi mảnh dần) nhưng màu tự chọn; stops = [viền, thân, lõi, sẹo].
        // life > tb: hết pha sáng còn lại một SẸO mảnh màu stops[3] viền mực nằm trên đối thủ tới hết life.
        void DrawVetLua(P q, float k, List<Item> buf)
        {
            float t = k * q.life, sang = q.tb;
            float quet = Mathf.Clamp01(t / 0.05f);
            quet = 1 - (1 - quet) * (1 - quet);
            float dai = q.sz * (0.2f + 0.8f * quet);
            var tam = q.pos - q.aim * (q.sz * 0.5f) + q.aim * (dai * 0.5f);
            float u = Mathf.Clamp01((t - 0.05f) / Mathf.Max(0.02f, sang - 0.05f));
            bool coSeo = q.life > sang + 0.01f, laSeo = t > sang;
            float day, alpha, loi;
            if (!laSeo)
            {
                day = q.wd * (1 - (coSeo ? 0.7f : 0.8f) * SmoothStep(0.15f, 1, u));
                alpha = coSeo ? 1 : 1 - SmoothStep(0.55f, 1, u);
                loi = 1 - SmoothStep(0.1f, 0.8f, u);
            }
            else
            {
                float v = (t - sang) / Mathf.Max(0.02f, q.life - sang);
                day = q.wd * (0.3f + 0.06f * Mathf.Sin(q.age * 26 + q.ph));
                alpha = 0.95f * (1 - SmoothStep(0.92f, 1, v));
                loi = 0;
            }
            if (alpha < 0.03f) return;
            var s = q.stops;
            LaLieu(buf, q.group, 46, true, laSeo ? Ink : s[0], tam, q.aim, dai + 6, day + 5, alpha);
            LaLieu(buf, q.group, 46.3f, false, laSeo ? s[3] : s[1], tam, q.aim, dai, day, alpha);
            if (loi > 0.05f) LaLieu(buf, q.group, 46.6f, false, s[2], tam, q.aim, dai * 0.86f, day * 0.5f * loi + 0.6f, alpha);
        }

        P VetLua(Vector2 c, Vector2 d, float dai, float day, float sang, float seo, Color vien, Color than, Color loi, Color seoC, int group = Front)
        {
            var p = new P
            {
                pos = c, aim = Unit(d), life = sang + Mathf.Max(0, seo), tb = sang, sz = dai, wd = day, group = group, ph = U(0, 6.28f),
                stops = new[] { vien, than, loi, seoC }
            };
            p.draw = DrawVetLua;
            return Add(p);
        }

        // ĐÒN THƯỜNG: VẢ. Ba vệt vuốt lửa song song bổ chéo xuống thân đối thủ đúng khung vả, chớp toé, tia lửa, bụi dưới chân nó.
        public float NHoVa(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.05f, lead);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var pc = Pal[Th.pal];
            var tam = foeBody + new Vector2(-dir * 0.05f * tH, -0.06f * tH);
            var d = Unit(new Vector2(dir * 0.5f, 0.86f));
            var n = new Vector2(-d.y, d.x);
            At(L, () =>
            {
                Shake?.Invoke(0.45f);
                for (int i = -1; i <= 1; i++)
                    VetLua(tam + n * (i * 0.14f * tH) - d * (Mathf.Abs(i) * 0.06f * tH), d, (i == 0 ? 0.95f : 0.78f) * tH, 0.085f * tH, 0.2f, 0, Ink, pc[1], pc[3], pc[1]);
                // khung vẽ sẵn (2026-11-19): lửa trúng đích "trung_lua" 0,8 thân xoay theo hướng vả (lửa tạt ngược về phía vuốt), thay chớp sao gai
                if (HoaFbTrung(tam + d * (0.08f * tH), 0.8f * tH, d) == null)
                    HoaChop(tam + d * (0.18f * tH), 0.34f * tH, 0.09f); // chớp lửa (BurstFlash là chớp nước, lấy bảng màu nước)
                for (int i = 0; i < 6; i++)
                    Spark(tam + n * U(-0.16f, 0.16f) * tH, d + n * U(-0.7f, 0.7f), U(260, 480), U(0.18f, 0.3f), U(5, 7), 300);
                HoaTan(tam, new Vector2(U(-40, 40), -U(100, 170)), U(0.45f, 0.65f), 4);
                for (int i = 0; i < 5; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(foeFeet + new Vector2(sd * U(6, 0.25f * tH), U(-5, 2)), new Vector2(sd * U(100, 260), -U(10, 50)), 0, 4, 11, Back);
                }
            });
            At(L + 0.08f, () =>
            {
                // khung vẽ sẵn (2026-11-19): ba cụm lửa lặp nhỏ "lua_lap" cháy trên ba vết vuốt 0,45 s, thay ba lưỡi lửa chữ S
                if (HasFb("lua_lap"))
                {
                    for (int i = 0; i < 3; i++)
                        HoaFbLua(tam + n * ((i - 1) * 0.14f * tH) + d * U(-0.1f, 0.25f) * tH, U(0.18f, 0.24f) * tH, U(0.38f, 0.5f), Front, 24, 0.06f, 0.6f);
                    return;
                }
                for (int i = 0; i < 3; i++)
                    HoaLuoi(Flame(tam + n * ((i - 1) * 0.14f * tH) + d * U(-0.2f, 0.3f) * tH, new Vector2(U(-30, 30), -U(60, 140)), U(0.3f, 0.45f), 6, U(10, 14),
                        "tron", Th.pal, Front, 2, -200, 1.4f, 0, 0), 1, 0.5f, 0.1f);
            });
            return L;
        }

        // SÓNG ÂM RÕ (2026-11-19 khuya; người dùng: "phần sóng âm chiêu mana tướng này chưa rõ"): như SongChi (HatSongChi.cs, cung 2–3 nét chì xám
        // nhạt, không viền mực) nhưng nét DÀY gấp đôi (hai lớp ảnh cung lệch nhau 3 % dọc hướng bay) và đặc hơn; nở h0 → h1 trên đường bay, rung nhẹ,
        // tới đích (mặt trước thân đối thủ) nở thêm chút rồi mờ hẳn trong 0,12 s. Chưa có ảnh cung thì về SongChi.
        P SongChiDay(Vector2 tu, Vector2 den, float h0, float h1, float v, float alpha)
        {
            if (S("kr_songchi_0") == null) return SongChi(tu, den, h0, h1, v, alpha);
            var d = den - tu;
            float toi = Mathf.Max(0.08f, d.magnitude / v);
            var p = new P { pos = tu, home = tu, aim = Unit(d), vy = v, life = toi + 0.12f, tb = toi, R0 = h0, R1 = h1, wd = alpha, seed = rng.Next(4) };
            p.draw = (q, k, buf) =>
            {
                float t = q.age, f = Mathf.Clamp01(t / q.tb);
                float h = Mathf.Lerp(q.R0, q.R1, EaseOut(f));
                float a = Mathf.Min(1, t / 0.04f) * q.wd;
                if (t > q.tb)
                {
                    float u = Mathf.Clamp01((t - q.tb) / Mathf.Max(0.02f, q.life - q.tb));
                    a *= 1 - u;
                    h *= 1 + 0.1f * u;
                }
                if (a < 0.03f) return;
                var dinh = q.home + q.aim * (Mathf.Min(t, q.tb) * q.vy);
                float ang = VelAng(q.aim) + 2f * Mathf.Sin(t * 41 + q.seed * 1.9f);
                var sp = S("kr_songchi_" + q.seed);
                Put(buf, Front, 44.6f, sp, SongChiC, dinh - q.aim * (0.12f * h), h, 1, ang, a);
                Put(buf, Front, 44.61f, sp, SongChiC, dinh - q.aim * (0.15f * h), h * 0.98f, 1, ang, a * 0.85f); // lớp thứ hai: nét dày gấp đôi
            };
            return Add(p);
        }

        // CHIÊU MANA: HỔ GẦM. Gồng: vòng cung co về chân, vệt lửa xoắn ốc hút vào ngực. Gầm: chớp ở mồm, SÓNG XUNG KÍCH (vòng mảnh quanh mồm, hai vòng
        // cung dẹt loang trên đất tới quá chỗ đối thủ, màn chớp) rồi các đợt sóng âm mảnh nối nhau lao tới, tan ở mặt trước đối thủ; SÓNG NHIỆT: lưỡi
        // lửa thấp và cụm tàn lửa bị thổi tạt dọc mặt đất. Đợt đầu tới nơi: nổ ở đối thủ, rồi nó cháy lách tách tới hết tiếng gầm. manh: dạng 1 nhỏ hơn.
        public float NHoGam(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead, float manh = 1)
        {
            float L = Mathf.Max(0.12f, lead);
            float t00 = L - HoGam, goc = T;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var pc = Pal[Th.pal];
            var dd = Unit(foeBody - mouth);
            var nrm = new Vector2(-dd.y, dd.x);
            float dist = (foeBody - mouth).magnitude;
            const float V = 1000;
            float fly = dist / V;
            float dur = HoHetGam - HoGam;
            var nguc = casterFeet + new Vector2(dir * 0.12f * casterH, -0.45f * casterH);

            // gồng
            float tTu = Mathf.Max(0.02f, t00 + HoTu);
            At(tTu, () => HoaCung(casterFeet + new Vector2(0, 2), 0.75f * casterH, 0.12f * casterH, 0.42f, Th.ring));
            if (L - tTu > 0.15f)
            {
                float chieu = U(0, 1) < 0.5f ? 1 : -1;
                Every(tTu, L - 0.06f, x => 18 + 22 * x, x =>
                {
                    float a = U(0, 6.28f);
                    var from = nguc + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.7f) * U(0.5f, 0.85f) * casterH;
                    HoaHut(t => nguc, t => 8, from, U(0.26f, 0.34f), U(0, 1) < 0.5f ? pc[1] : pc[2], chieu, goc + L, Back);
                });
            }

            // GẦM: sóng xung kích
            At(L, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(new Color(1, 0.9f, 0.7f, 0.3f));
                HoaChop(mouth, 0.36f * casterH, 0.09f);
                HoaCung(casterFeet + new Vector2(0, 2), 0.2f * casterH, Mathf.Max(0.9f * casterH, dist * 1.15f) * manh, 0.5f, Th.ring);
                for (int i = 0; i < 8; i++)
                    Bui(casterFeet + new Vector2(dir * U(0.1f, 0.5f) * casterH, U(-4, 2)), new Vector2(dir * U(200, 460), -U(10, 60)), 0, 4, 12, Back);
            });
            // các đợt sóng âm: dải cung thuôn hai đầu (kem ngoài / cam trong, đợt sau đảo màu) lao tới MẶT TRƯỚC thân đối thủ rồi bẹt ra tan; mỗi đợt
            // tới nơi đối thủ chớp + giật một nhịp (NuocPulse: mã "n_" đi qua PlayNuoc)
            // sóng âm vẽ chì (2026-11-19, người dùng: "làm đơn giản thôi"): 3–4 cung nét chì xám nhạt (SongChi, HatSongChi.cs) thay dải cung kem /
            // cam viền mực; bỏ vòng tròn ở miệng và vòng cung đất thứ hai
            // 2026-11-19 khuya (người dùng: "phần sóng âm chiêu mana tướng này chưa rõ"): 6 cung cách 0,1 s (dạng nhỏ 5), to hơn (0,3 → 1,35 thân;
            // cung đầu 1,2 lần), nét dày gấp đôi (SongChiDay), bay tới TẬN mặt trước thân đối thủ (0,12 thân trước tâm); mỗi cung tới nơi: bông toé
            // trắng "trung_trang" nhỏ ở chỗ chạm, rung nhẹ, nhịp trúng HoaTrung. Lúc gầm thêm ba gợn "méo không khí": cung chì nhỏ nhạt nở đồng tâm ở
            // miệng.
            int N = manh < 0.95f ? 5 : 6;
            var den = foeBody - dd * (0.12f * tH);
            float toi = (den - mouth).magnitude / V;
            for (int i = 0; i < N; i++)
            {
                int j = i;
                float vj = V * (j == 0 ? 1.08f : 1);
                At(L + 0.1f * j, () =>
                {
                    float m = (j == 0 ? 1.2f : 1) * manh;
                    SongChiDay(mouth + dd * 10, den, 0.3f * casterH, 1.35f * tH * m, vj, 1f - 0.05f * j);
                    Shake?.Invoke(j == 0 ? 0.7f : 0.25f);
                });
                if (j > 0)
                    At(L + 0.1f * j + toi * V / vj, () =>
                    {
                        var cham = den + nrm * U(-0.12f, 0.12f) * tH;
                        Fb("trung_trang", cham, 0.42f * tH, Front, 33, 1.6f, U(-15, 15), dir < 0, null, 0.9f);
                        Shake?.Invoke(0.12f);
                        HoaTrung?.Invoke(cham, 0.3f);
                    });
            }
            for (int i = 0; i < 3; i++)
            {
                int j = i;
                At(L + 0.04f * j, () => SongChi(mouth + dd * 4, mouth + dd * (0.3f * casterH), (0.1f + 0.04f * j) * casterH, (0.45f + 0.08f * j) * casterH, 700,
                    0.55f));
            }
            // SÓNG NHIỆT dọc mặt đất: bỏ (2026-11-19 khuya; người dùng: "tự nhiên thấy mấy đốm lửa spawn ra ở dưới nhìn không đẹp")

            // trúng
            float hit = L + fly;
            At(hit, () =>
            {
                Shake?.Invoke(0.9f);
                NuocPulse?.Invoke(0.8f);
                HoaNo(foeBody, 1.05f * manh, tH, foeFeet, Front, dir); // khung vẽ sẵn (2026-11-19): "no" sau lưng + "trung_lua" lật theo hướng sóng
                HoaTan(foeBody, new Vector2(dir * U(160, 320), -U(80, 200)), U(0.45f, 0.65f), 5);
                // 2026-11-19 khuya: bỏ hai cụm lửa "lua_lap" cháy ở chân đối thủ và lửa / tia rải trên thân suốt tiếng gầm (người dùng: "mấy đốm lửa
                // spawn ra ở dưới nhìn không đẹp"); chỉ giữ lửa của cú nổ chính
            });

            At(hit + dur, () =>
            {
                for (int i = 0; i < 2; i++)
                    HoaKhoi(foeBody + new Vector2(U(-0.25f, 0.25f) * tH, -U(0.15f, 0.4f) * tH), U(0.12f, 0.16f) * tH, Back, null, 0, true, 0.5f);
            });
            return hit;
        }

        // CHIÊU CUỐI: ẢNH TRẢO LIÊN HOÀN. Bật tới: bụi và tia lửa ở chân; tan biến: MÀN ÂM BẢN tới lúc hiện lại; mỗi lượt hổ lướt qua: một
        // vệt lướt mảnh xuyên ngang + một VỆT CHÉM chéo trên đối thủ (trong màn âm bản vẽ bằng màu đảo để hiện ra màu lửa), vệt để lại SẸO LỬA
        // cháy âm ỉ; hiện lại ở chỗ cũ; rồi các sẹo NỔ lần lượt thành vụ nổ lớn. n: số lượt (12; dạng 1: 6). Trả giây tới vụ nổ đầu.
        public float NHoAnh(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int n = 12, float manh = 1)
        {
            float tHien = HoLuot0 - 1 / 30f + n * HoBuoc + 5 / 30f, tNo = tHien + 0.30f;
            float L = Mathf.Max(tNo * 0.6f, lead);
            float t00 = L - tNo;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var pc = Pal[Th.pal];
            Color kem = C(255, 246, 214);

            // bật tới
            At(Mathf.Max(0.02f, t00 + HoBat), () =>
            {
                Shake?.Invoke(0.3f);
                HoaCung(casterFeet + new Vector2(0, 2), 0.1f * casterH, 0.7f * casterH, 0.4f, Th.ring);
                for (int i = 0; i < 8; i++)
                    Bui(casterFeet + new Vector2(U(-0.25f, 0.25f) * casterH, U(-6, 2)), new Vector2(-dir * U(80, 280), -U(10, 80)), U(0.4f, 0.65f), 4, U(10, 16), Back);
                for (int i = 0; i < 6; i++) Spark(casterFeet + new Vector2(U(-0.2f, 0.2f) * casterH, -4), new Vector2(-dir * U(0.3f, 1f), -U(0.2f, 0.8f)), U(260, 440), 0, 6);
            });
            // màn âm bản từ lúc tan hẳn tới lúc hiện lại
            float tAm = Mathf.Max(0.03f, t00 + HoBien);
            At(tAm, () => NegScreen?.Invoke(Mathf.Max(0.2f, t00 + tHien - tAm + 0.04f)));

            // các lượt lướt
            var tamSeo = new Vector2[n];
            var huongSeo = new Vector2[n];
            for (int i = 0; i < n; i++)
            {
                int k = i;
                float tk = t00 + HoLuot0 + k * HoBuoc;
                float sg = (k & 1) == 0 ? dir : -dir;
                huongSeo[k] = Unit(new Vector2(sg, HoDoc[k % HoDoc.Length]));
                tamSeo[k] = foeBody + new Vector2(U(-0.1f, 0.1f), U(-0.16f, 0.12f)) * tH;
                if (tk < 0.02f) continue;
                At(tk, () =>
                {
                    Shake?.Invoke(0.3f);
                    NuocPulse?.Invoke(0.35f);
                    var c = tamSeo[k];
                    var d = huongSeo[k];
                    var nn = new Vector2(-d.y, d.x);
                    // vệt lướt của thân hổ: mảnh, dài, ngang qua đối thủ
                    VetLua(new Vector2(c.x, foeBody.y - 0.05f * tH), new Vector2(sg, 0), 3.4f * tH, 0.05f * tH, 0.12f, 0, Dao(kem), Dao(pc[2]), Dao(kem), pc[1], Back);
                    // nhát chém + sẹo lửa nằm lại tới lúc nổ
                    VetLua(c, d, 1.5f * tH * manh, 0.12f * tH, 0.16f, L - tk - 0.16f, Dao(kem), Dao(pc[1]), Dao(pc[3]), pc[1]);
                    for (int j = 0; j < 4; j++)
                    {
                        float sd = (j & 1) == 0 ? 1 : -1;
                        var q = Spark(c + d * sd * U(0.1f, 0.5f) * tH, d * sd + nn * U(-0.4f, 0.4f), U(320, 560), U(0.14f, 0.24f), U(5, 7), 0, Front, 4);
                        q.col = Dao(Th.spark);
                    }
                });
                // lửa chữ S cháy dọc sẹo; khung vẽ sẵn (2026-11-19): một cụm lửa lặp nhỏ "lua_lap" cháy giữa mỗi sẹo tới lúc nổ (dạng 1 ít lượt: thêm
                // một cụm lệch dọc sẹo)
                if (HasFb("lua_lap"))
                {
                    float sTu = tk + 0.1f;
                    if (L - sTu > 0.08f)
                        At(sTu, () =>
                        {
                            int nc = n <= 6 ? 2 : 1;
                            for (int c = 0; c < nc; c++)
                                HoaFbLua(tamSeo[k] + huongSeo[k] * (nc == 1 ? U(-0.15f, 0.15f) : (c == 0 ? -0.3f : 0.3f)) * tH * manh, U(0.18f, 0.24f) * tH * manh,
                                    L - sTu + 0.05f, Front, 24, 0.08f, 0.2f);
                        });
                }
                else
                    Every(tk + 0.1f, L, 6, x =>
                    {
                        var p = tamSeo[k] + huongSeo[k] * U(-0.55f, 0.55f) * tH * manh;
                        HoaLuoi(Flame(p, new Vector2(U(-20, 20), -U(50, 120)), U(0.28f, 0.42f), 5, U(8, 12), "tron", Th.pal, Front, 2, -220, 1.4f, 0, 0), 1, 0.5f,
                            0);
                    });
            }
            // hiện lại ở chỗ cũ
            At(Mathf.Max(0.05f, t00 + tHien), () =>
            {
                HoaCung(casterFeet + new Vector2(0, 2), 0.08f * casterH, 0.55f * casterH, 0.4f, Th.ring);
                for (int i = 0; i < 6; i++)
                    Bui(casterFeet + new Vector2(U(-0.2f, 0.2f) * casterH, U(-6, 2)), new Vector2(dir * U(40, 200), -U(10, 60)), U(0.35f, 0.6f), 3.5f, U(9, 14), Back);
            });
            // các sẹo nổ lần lượt, rồi vụ nổ lớn
            int buoc = Mathf.Max(1, n / 4);
            int soNo = 0;
            for (int i = 0; i < n; i += buoc)
            {
                int k = i;
                At(L + 0.05f * soNo, () =>
                {
                    Shake?.Invoke(0.4f);
                    HoaNo(tamSeo[k] + huongSeo[k] * U(-0.3f, 0.3f) * tH, U(0.5f, 0.7f) * manh, tH, null, Front, huongSeo[k].x >= 0 ? 1 : -1); // khung vẽ sẵn: lật theo sẹo
                    VetLua(tamSeo[k], huongSeo[k], 1.7f * tH * manh, 0.15f * tH, 0.2f, 0, Ink, pc[1], pc[3], pc[1]);
                });
                soNo++;
            }
            float tLon = L + 0.05f * soNo + 0.04f;
            At(tLon, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(new Color(1, 0.95f, 0.8f, 0.22f)); // rig đã khai chớp ở khung trúng: ở đây chỉ nháy nhẹ
                NuocPulse?.Invoke(1f);
                HoaCauNo(foeBody, foeFeet, tH, dir, 1.5f * manh);
            });
            At(tLon + 0.14f, () => HoaNo(foeBody + new Vector2(dir * U(4, 22), U(-30, 6)), 0.7f * manh, tH, null, Front, dir));
            At(tLon + 0.4f, () =>
            {
                for (int i = 0; i < 3; i++)
                    HoaKhoi(foeBody + new Vector2(U(-0.3f, 0.3f) * tH, -U(0.15f, 0.5f) * tH), U(0.13f, 0.17f) * tH, Back, null, 0, true, 0.5f);
                for (int i = 0; i < 4; i++) Ash(foeBody + U2(-30, 30));
            });
            return L;
        }
    }
}
