// Bộ hiệu ứng của GIÁC MỘC (2026-11-13, thú cổ thụ một sừng, suất moc_tinh đảo Mộc; rig ArtGen/Spine/giac_moc*.py trên rig monster_3804).
// Người dùng: "tấn công thường dậm chân mạnh tạo vết nứt tới đối thủ (fx làm riêng)"; "chiêu cast mana ngẩng lên tụ cầu năng lượng ở
// trên đỉnh sừng rồi cúi xuống phóng tia năng lượng từ cầu"; "chiêu cuối mở phần bụng, trong phần bụng có 1 quả cầu năng lượng kiểu
// trái tim phát sáng (luôn có sẵn), nó sẽ phát sáng cực mạnh rồi bắn ra 1 tia sáng cực mạnh chết chóc vào người đối thủ".
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes
// ("moc_tinh": hổ phách, bản tươi MocTuoi của HatMoc.cs). Dùng lại quả cầu và gió hút của Gạc Đá (HatDa.cs: CauLa, GatherLa), tia năng
// lượng chung của bộ Mộc (HatMoc.cs: TiaMoc), đất nứt của rồng trúc (HatRong.cs: DatNut), dăm đá (HatDa.cs: DaVun).
// Nâng 2026-11-18 (người dùng: tia cuối cụt lủn, không va chạm; tia màu tối như khúc gỗ; hút khí quanh cầu xấu): tia TiaMoc lõi chanh kem
// rộng, đầu tia tới mặt trước thân đối thủ, bông va chạm toé liên tục, tắt bằng thon dần rồi vỡ vụn; năng lượng hút nhập vào cầu / tim;
// cầu nén 1–2 khung rồi chớp; vết nứt hổ phách nằm lại trên đất; bụi thành cụm.
// Mốc của clip (giac_moc_clip.py):
//   attack: dậm = lead − 0,18 s (0,74), trúng = lead (0,92).
//   cast  : tụ = 0,40 s, ngẩng cao tới 1,10, cúi 1,11 → 1,33, bắn = lead (1,36), tia chảy 0,88 s (clip ghìm tới 2,30).
//   skill : vỏ ngực mở 0,15 → 0,95, tim tụ từ 1,00, bắn = lead (2,05), ghìm tia tới 3,05, đóng ngực 3,55.
// Sân không theo dõi xương của rig, nên đường đi của đỉnh sừng (xương `mieng`) và chỗ quả tim (xương `tim`) chép sẵn từ rig
// (`giac_moc_rig.py duong`): x ra phía đối thủ, y lên, chia cho chiều cao tướng.
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // đỉnh sừng trong clip cast, mỗi 0,1 s từ 0 tới 2,7 s
        static readonly float[] GiacSung =
        {
            0.542f, 1.059f, 0.593f, 1.050f, 0.594f, 1.094f, 0.491f, 1.240f, 0.414f, 1.307f, 0.359f, 1.342f, 0.377f, 1.331f, 0.387f, 1.324f,
            0.392f, 1.323f, 0.392f, 1.325f, 0.399f, 1.323f, 0.405f, 1.321f, 0.430f, 1.247f, 0.573f, 0.753f, 0.571f, 0.742f, 0.587f, 0.729f,
            0.599f, 0.732f, 0.616f, 0.740f, 0.625f, 0.756f, 0.630f, 0.775f, 0.630f, 0.800f, 0.626f, 0.825f, 0.613f, 0.867f, 0.599f, 0.917f,
            0.568f, 0.982f, 0.558f, 1.019f, 0.543f, 1.057f, 0.542f, 1.059f,
        };
        const float GiacTimX = 0.23f, GiacTimY = 0.49f; // quả tim lúc ngực đã mở (clip skill 0,4 → 3,2 s gần như đứng yên)
        const float GiacChanX = 0.057f;                 // bàn chân trước gần (chân dậm) so với gốc

        static Vector2 GiacSungAt(Vector2 feet, float h, float dir, float clipT)
        {
            int n = GiacSung.Length / 2;
            float x = Mathf.Clamp(clipT / 0.1f, 0, n - 1.001f);
            int i = (int)x;
            float w = x - i;
            return feet + new Vector2(dir * Mathf.Lerp(GiacSung[2 * i], GiacSung[2 * i + 2], w) * h, -Mathf.Lerp(GiacSung[2 * i + 1], GiacSung[2 * i + 3], w) * h);
        }

        // tia vụn hổ phách bật lên từ khe đất: theo cụm nhỏ lệch cỡ (bản cũ: vệt lẻ to)
        void GiacTiaVun(Vector2 at, int n, float manh, int group = Front)
        {
            var w = W;
            for (int i = 0; i < n; i += 3)
                TiaVunCum(at + new Vector2(U(-10, 10), U(-4, 0)), new Vector2(U(-0.3f, 0.3f), -1), 0.6f, Mathf.Min(3, n - i), U(280, 520) * manh, U(3f, 4.4f), group,
                    w[2], MocChanh);
        }

        // năng lượng bị hút về tâm cFn(giây từ lúc gọi): vệt thuôn không viền bay lái dần về tâm, nhanh dần, hiện dần lúc sinh, chạm tâm thì nhập
        // vào cầu (bản cũ: vệt trắng viền mực bay thẳng, tắt giữa đường)
        void NangHut(Func<float, Vector2> cFn, float start, Vector2 from, float speed, float sz, int group)
        {
            var q = new P { pos = from, life = 0.6f, group = group, sz = sz, stops = W, seed = rng.Next(4), R0 = speed, tb = start };
            var d0 = Unit(cFn(T - start) - from);
            q.vel = (d0 + new Vector2(-d0.y, d0.x) * U(-0.6f, 0.6f)) * speed * 0.4f;
            q.upd = (z, dt, s) =>
            {
                var to = cFn(s.T - z.tb) - z.pos;
                float d = to.magnitude;
                float v = z.R0 * (0.4f + 1.4f * Mathf.Min(1, z.age / 0.25f)); // nhanh dần
                z.vel += (to / Mathf.Max(d, 1e-5f) * v - z.vel) * Mathf.Min(1, 9 * dt);
                if (d < 8 || d < z.vel.magnitude * dt) z.dead = true;
            };
            q.draw = DrawGioHut;
            Add(q);
        }

        // ĐÒN ĐÁNH THƯỜNG: co chân trước rồi DẬM → vết nứt hổ phách chạy tới đối thủ (vết nằm lại trên đất ~1 s), ánh hổ phách lọt qua khe →
        // đất bật dưới chân đối thủ, vòng cung dẹt, vết nứt lớn.
        public float NGiacDam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.3f, lead);
            float tDam = Mathf.Max(0.05f, L - 0.18f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var chan = casterFeet + new Vector2(dir * GiacChanX * casterH, 0);
            var w = W;
            // co chân: bụi nhẹ dưới chân trụ
            float tCo = Mathf.Max(0.02f, L - 0.60f);
            if (HasFb("khoi")) // khung vẽ sẵn (2026-11-19): một cụm khói nhuộm đất nhỏ dưới chân trụ thay vài cụm BuiCum lấm tấm
                At(tCo, () => MocKhoiFb(casterFeet + new Vector2(-dir * U(0.12f, 0.28f) * casterH, U(-3, 2)), 0.07f * casterH, new Vector2(-dir * U(20, 60), -U(15, 35)),
                    Back, 3, 1.3f, 0.85f));
            else
                Every(tCo, tCo + 0.18f, 6, x =>
                    BuiCum(casterFeet + new Vector2(-dir * U(0.05f, 0.35f) * casterH, U(-4, 2)), new Vector2(-dir * U(20, 70), -U(20, 50)), U(0.05f, 0.07f) * casterH, 0, Back));
            // DẬM
            At(tDam, () =>
            {
                Shake?.Invoke(0.85f);
                CungDat(chan + new Vector2(0, 2), 0.1f * casterH, 0.8f * casterH, 0.45f, CungC, 0.09f * casterH);
                VetDat(chan + new Vector2(0, 3), 0.42f * casterH, 0.9f, w[3]);
                if (!MocBuiHaiBen(chan, 0.14f * casterH, 0.24f * casterH, 140, true)) // khung vẽ sẵn: hai cụm khói nhuộm đất + một cụm giữa thay năm cụm BuiCum
                    for (int i = 0; i < 5; i++)
                    {
                        float sd = i == 2 ? 0 : (i & 1) == 0 ? 1 : -1;
                        BuiCum(chan + new Vector2(sd * U(0.1f, 0.3f) * casterH, U(-6, 2)), new Vector2(sd * U(80, 200), -U(15, 50)), U(0.1f, 0.14f) * casterH, 0,
                            i < 3 ? Back : Front);
                    }
                for (int i = 0; i < 7; i++) DaVun(chan + new Vector2(U(-22, 22), -4), new Vector2(U(-220, 220), -U(240, 450)), U(0.45f, 0.75f), U(2.6f, 4.2f));
                for (int i = 0; i < 4; i++) Leaf(chan + new Vector2(U(-20, 20), -U(4, 14)), new Vector2(U(-140, 140), -U(260, 420)), U(0.5f, 0.8f), U(3.6f, 5.6f), 700, 1.2f);
                GiacTiaVun(chan, 6, 0.8f);
            });
            // vết nứt chạy tới đối thủ: năm chỗ đất bật, cái sau to hơn; vết nứt hổ phách nằm lại trên đất
            const int N = 5;
            for (int i = 0; i < N; i++)
            {
                int j = i;
                At(tDam + (L - tDam - 0.02f) * (j + 1) / (N + 1), () =>
                {
                    var at = Vector2.Lerp(chan, foeFeet, (j + 1f) / (N + 1));
                    DatNut(at, tH, 0.65f + 0.13f * j);
                    VetDat(at + new Vector2(0, 2), (0.2f + 0.04f * j) * tH, 0.8f + 0.04f * (N - j), w[3]);
                    GiacTiaVun(at, 3, 0.7f + 0.08f * j, Back);
                });
            }
            // trúng: đất dưới chân đối thủ bật tung, cột ánh hổ phách phụt lên
            At(L, () =>
            {
                Shake?.Invoke(0.7f);
                DanhTrung?.Invoke(foeBody, 0.7f);
                DatNut(foeFeet, tH, 1.35f);
                VetDat(foeFeet + new Vector2(0, 3), 0.5f * tH, 1f, w[3]);
                GiacTiaVun(foeFeet, 12, 1.25f);
                Chop(foeFeet + new Vector2(0, -0.12f * tH), 0.36f * tH, 0.07f);
                BurstFlash(foeFeet + new Vector2(0, -0.18f * tH), 0.62f * tH, Back, 0.16f);
                CungDat(foeFeet + new Vector2(0, 2), 0.08f * tH, 0.66f * tH, 0.42f, w[2], 0.08f * tH);
                WExtra(foeBody, 4, 300);
            });
            return L;
        }

        // CẦU ĐỈNH SỪNG + TIA (chiêu mana): năng lượng từ ngực hé mở chảy lên đỉnh sừng (vệt thuôn nhanh dần, nhập vào cầu), gió và lá bị hút
        // xoắn về đỉnh sừng, quả cầu lớn dần theo đỉnh sừng đang ngẩng cao, đập nhanh dần; cúi đầu chĩa sừng về trước, cầu nén 1–2 khung rồi chớp,
        // nhả tia năng lượng (TiaMoc: lõi chanh kem rộng) tới MẶT TRƯỚC thân đối thủ, bông va chạm toé liên tục, đối thủ giật từng nhịp; cầu cạn
        // dần lúc tia chảy; hết tia thì tia thon từ gốc tới ngọn rồi vỡ vụn, lá nổ nhỏ.
        public float NGiacTia(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.4f, lead);
            float kT = 1.36f / L;                          // giây của clip cho mỗi giây thật (sân có thể chạy clip nhanh / chậm hơn)
            float tTu = 0.40f / kT;
            const float dur = 0.88f;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float rFull = 0.125f * casterH;
            var tim = casterFeet + new Vector2(dir * (GiacTimX - 0.02f) * casterH, -(GiacTimY + 0.03f) * casterH);
            // đỉnh sừng theo clip; sát khung bắn thì hoà về `mouth` (chỗ bắn game tính từ rig) để cầu và gốc tia trùng nhau
            Func<float, Vector2> cFn = age =>
            {
                float t = tTu + age;
                var p = GiacSungAt(casterFeet, casterH, dir, t * kT);
                float wl = SmoothStep(L - 0.10f, L - 0.01f, t) * (1 - SmoothStep(L + dur, L + dur + 0.1f, t));
                return Vector2.Lerp(p, mouth, wl) + new Vector2(0, 1.5f * Mathf.Sin(age * 11));
            };
            Func<float, float> rFn = age =>
            {
                float t = tTu + age;
                if (t > L + dur) return 0;
                float g = Mathf.Clamp01(age / Mathf.Max(0.1f, L - tTu - 0.25f));
                float r = rFull * (0.2f + 0.8f * g) * Mathf.Min(1, age / 0.08f);
                if (t > L) r *= 1 - 0.45f * Mathf.Clamp01((t - L) / dur);
                return r * NenNha(t, L);
            };
            float goc = T;
            // tia vẽ sẵn (2026-11-19, da vàng DaTiaVang gần màu hổ phách): cầu xoáy đầu nòng thay quả cầu CauLa, bám đỉnh sừng như cũ;
            // 2026-11-25: có lưới shader thì là tia năng lượng kiểu Water Laser bảng hổ phách (GiacTiaFb → ELaser)
            bool fb = CoLaser || HasTia(DaTiaVang);
            At(tTu, () =>
            {
                if (!fb) CauLa(cFn, L + dur - tTu, rFn, Front, L - tTu);
                GatherLa(cFn, 0, L - tTu - 0.3f, (fb ? 0.6f : 0.5f) * casterH, 24); // cầu vẽ sẵn to hơn cầu cũ: gió, lá hút từ xa hơn
            });
            // năng lượng từ tim (ngực hé mở) bốc lên đỉnh sừng trong lúc ngẩng: mật độ tăng dần
            Every(tTu, 1.10f / kT, x => 10 + 24 * x, x =>
                NangHut(cFn, goc + tTu, tim + U2(-10, 10), U(420, 620), U(3f, 4.4f), Back));
            // tia năng lượng thẳng từ quả cầu: giờ trúng giữ như bản trước (quãng / 2600)
            float travel = (foeBody - mouth).magnitude / 2600f;
            float hit = L + travel;
            float hw = 0.05f * Mathf.Max(casterH, tH);
            float datY = foeFeet.y;
            float tPhong = L;
            if (fb) // gốc tia: đỉnh sừng theo clip tới khung bắn, rồi đứng ở `mouth`
                tPhong = GiacTiaFb(() => T - goc < L ? cFn(T - goc - tTu) : mouth, mouth, ChamThan(mouth, foeBody, tH), tTu, hit, L + dur, L + 0.84f,
                    0.22f * casterH, 1, tH, datY);
            At(tPhong, () => // chớp nòng đúng lúc tia phóng (tia hạt cũ: khung bắn của clip)
            {
                Shake?.Invoke(0.35f);
                Chop(mouth, 0.34f * casterH, 0.08f);
                WExtra(mouth, 4, 220);
            });
            if (!fb) At(L, () => TiaMoc(mouth, ChamThan(mouth, foeBody, tH), travel, dur, hw, tH, 1, datY));
            At(hit, () => WExtra(foeBody, 4, 300));
            At(L + dur, () => LaNo(foeBody, foeFeet, tH, 0.75f));
            return hit;
        }

        // TIA VẼ SẴN của Giác Mộc (2026-11-19; người dùng: "các tia năng lượng/nước như này nhìn vẫn chưa đã"): TiaFb da vàng DaTiaVang (năng lượng
        // vàng cam lõi kem, dải xoắn, sao lấp lánh; gần hổ phách của tướng) thay thân tia TiaMoc + bông gốc + bông trúng, GIỮ hợp đồng thời gian
        // của TiaMoc. Gọi lúc đầu chiêu (giây 0).
        //   tu: gốc tia (hàm, bám rig); src: gốc tia lúc bắn; cham: điểm chạm (ChamThan); tNong: lúc cầu đầu nòng bắt đầu hiện, lớn dần tới lúc phóng;
        //   hit: giờ chạm cũ (đầu tia chạm đúng lúc này: lúc phóng lùi lại tVuon giây của TiaFb); tHet: lúc tia hạt cũ mất hẳn, đuôi tia vẽ sẵn bay
        //   tới đích đúng lúc này (nên ngừng nhả sớm hơn quãng đuôi bay); tNgon: lúc nhịp trúng cuối (ngọn TiaMoc bắt đầu tắt); manh: như TiaMoc
        //   (mana 1, chiêu cuối 1,4).
        // Nhịp trúng như TiaMoc: chạm: rung 0,3·manh + DanhTrung 0,7 + chùm tia vụn; rồi mỗi 0,12 s tới tNgon: DanhTrung 0,3 + rung 0,1·manh (xen sao
        // lấp lánh / lá hổ phách bật ngược). Tia vụn hổ phách toé ngược suốt lúc dội, bụi dưới chân đối thủ; lúc ngừng nhả vài mảnh năng lượng bay
        // theo hướng tia rồi rơi. Trả lúc phóng (giây kể từ lúc gọi) để hàm gọi đặt chớp nòng.
        float GiacTiaFb(Func<Vector2> tu, Vector2 src, Vector2 cham, float tNong, float hit, float tHet, float tNgon, float day, float manh, float tH, float datY)
        {
            float dai = (cham - src).magnitude;
            var u = Unit(cham - src);
            var nrm = new Vector2(-u.y, u.x);
            float tVuon = Mathf.Clamp(dai / 2600f, 0.07f, 0.14f);    // như TiaFb
            float tPhong = Mathf.Max(tNong + 0.05f, hit - tVuon);
            float tDuoi = dai / Mathf.Max(380, dai / 0.32f);          // đuôi bay nốt vào đích (tốc trôi đoạn của TiaFb)
            float tNgung = Mathf.Max(hit + 0.3f, tHet - tDuoi);       // ngừng nhả
            var w = W;
            // 2026-11-25: tia năng lượng kiểu Water Laser (ELaser, bảng hổ phách, cầu cau_vang), cùng giờ chạm; tia vụn toé ngược thưa hơn vì
            // chỗ trúng của ELaser đã tự bắn gai + tia vụn
            bool laser = CoLaser;
            At(tNong, () =>
            {
                if (laser) ELaser(LaserHoPhach, tu, () => cham, day, tPhong - tNong, tNgung - hit, Front, 1, manh > 1 ? 1.15f : 1, datY);
                else TiaFb(DaTiaVang, tu, () => cham, day, tPhong - tNong, tNgung - hit);
            });
            // tia vụn / mảnh vỡ: tia Water Laser hổ phách thì cùng tông hổ phách (vàng chanh MocChanh lệch tông trên tia cam, ảnh chụp 2026-11-25)
            Color cVun = laser ? LaserHoPhach.vun1 : MocChanh;
            At(hit, () =>
            {
                Shake?.Invoke(0.3f * manh);
                DanhTrung?.Invoke(cham, 0.7f);
                TiaVunCum(cham, -u, 1.2f, 5, 520 * manh, 4.4f, Front, w[2], cVun);
            });
            int nv = Mathf.Max(1, Mathf.FloorToInt((tNgon - hit) / 0.12f));
            for (int i = 0; i < nv; i++)
            {
                int ii = i;
                At(hit + 0.06f + 0.12f * i, () =>
                {
                    DanhTrung?.Invoke(cham, 0.3f);
                    Shake?.Invoke(0.1f * manh);
                    if ((ii & 1) == 0) WExtra(cham, 1, 220); // sao lấp lánh (họa tiết của tướng) bật ra theo nhịp, hợp sao trên da tia vàng
                    else Leaf(cham + U2(-6, 6), Unit(-u + nrm * U(-1.1f, 1.1f)) * U(180, 340) + new Vector2(0, -U(40, 120)), U(0.4f, 0.6f), U(3.6f, 5.4f), 620, 2f,
                        U(0, 1) < 0.6f ? Front : Back);
                });
            }
            Every(hit, tNgung, (laser ? 3 : 7) * manh, x =>
                TiaVunCum(cham + nrm * U(-0.4f, 0.4f) * day, -u, 1.3f, 3, U(300, 480) * manh, U(3f, 4.4f), U(0, 1) < 0.7f ? Front : Back, cVun, w[3]));
            bool kh = HasFb("khoi");
            Every(hit, tNgung, kh ? 2 : 3, x =>
            {
                var at = new Vector2(cham.x + U(-0.25f, 0.25f) * tH, datY + U(-4, 2));
                if (kh) MocKhoiFb(at, U(0.08f, 0.11f) * tH, new Vector2(u.x * U(40, 100), -U(20, 40)), Back, 3.5f, 1.3f, 0.85f);
                else BuiCum(at, new Vector2(U(-60, 60), -U(20, 50)), U(0.08f, 0.12f) * tH, 0, Back);
            });
            for (int j = 0; j < 6; j++)
            {
                int jj = j;
                At(tNgung + 0.03f * j, () =>
                {
                    var at = src + u * dai * U(0.1f, 0.6f) + nrm * U(-0.5f, 0.5f) * day;
                    var p = new P
                    {
                        pos = at, vel = u * U(260, 460) + nrm * U(-60, 60) + new Vector2(0, -U(10, 50)), life = U(0.32f, 0.5f), drag = 2.2f,
                        acc = new Vector2(0, 360), sz = day * U(0.18f, 0.3f), spin = U(-400, 400), ang = VelAng(u), group = Front,
                        col = (jj & 1) == 0 ? cVun : w[3]
                    };
                    p.draw = DrawMangVo;
                    Add(p);
                });
            }
            return tPhong;
        }

        // TIM CỔ THỤ KHAI QUANG (chiêu cuối): vỏ ngực mở, quả tim đập nhanh dần, mỗi nhịp một vòng lan, gió và lá quanh người bị hút xoắn vào tim,
        // năng lượng hổ phách nhập vào tim nhanh dần; ngay trước lúc bắn một vòng co sát vào tim rồi CHỚP; BẮN tia năng lượng dày từ tim tới mặt
        // trước thân đối thủ, ghìm một giây: bông va chạm toé liên tục, đối thủ giật từng nhịp, đất dưới chân nó nứt, dọc đường tia bụi cụm bốc và
        // lá bị thổi dạt, màn rung; hết tia: tia thon từ gốc rồi vỡ vụn, nổ cầu (NoCau), tia vụn hổ phách phụt từ đất.
        public float NGiacTim(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            MocSang();
            float L = Mathf.Max(0.8f, lead);
            float kT = 2.05f / L;
            float tMo = 0.15f / kT, tTu = 1.00f / kT;
            const float dur = 1.0f;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var tim = casterFeet + new Vector2(dir * GiacTimX * casterH, -GiacTimY * casterH);
            Func<float, Vector2> cFn = age => tim;
            var w = W;
            // vỏ ngực mở: bụi cụm quanh chân, vòng cung dẹt
            At(tMo, () =>
            {
                CungDat(casterFeet + new Vector2(0, 2), 0.15f * casterH, 0.7f * casterH, 0.5f, CungC, 0.07f * casterH);
                if (!MocBuiHaiBen(casterFeet, 0.1f * casterH, 0.3f * casterH, 70)) // khung vẽ sẵn (2026-11-19): hai cụm khói nhuộm đất thay bốn cụm BuiCum
                    for (int i = 0; i < 4; i++)
                    {
                        float sd = (i & 1) == 0 ? 1 : -1;
                        BuiCum(casterFeet + new Vector2(sd * U(0.12f, 0.4f) * casterH, U(-4, 2)), new Vector2(sd * U(40, 100), -U(30, 70)), U(0.08f, 0.11f) * casterH, 0, Back);
                    }
            });
            // tim tụ lực: nhịp đập nhanh dần (0,34 s → 0,12 s), mỗi nhịp một vòng lan; nhịp sau mạnh thì chớp nhỏ + rung
            float tb = tTu, gap = 0.34f;
            while (tb < L - 0.12f)
            {
                float g = Mathf.Clamp01((tb - tTu) / Mathf.Max(0.2f, L - tTu));
                float tt = tb;
                At(tt, () =>
                {
                    VongVa(tim, 0.05f * casterH, (0.22f + 0.2f * g) * casterH, 0.26f, w[3], Front, 1, 36);
                    if (g > 0.45f)
                    {
                        Chop(tim, (0.16f + 0.14f * g) * casterH, 0.06f);
                        Shake?.Invoke(0.12f + 0.2f * g);
                    }
                });
                gap = Mathf.Lerp(0.34f, 0.12f, g);
                tb += gap;
            }
            float goc = T;
            At(tTu, () =>
            {
                GatherLa(cFn, 0, L - tTu - 0.06f, 1.2f * casterH, 58);
                // bụi dưới chân bị cuốn lên (khung vẽ sẵn 2026-11-19: cụm khói nhuộm đất bay lên, thưa hơn; chưa nhập khung thì BuiCum cũ)
                bool kh = HasFb("khoi");
                Every(0, L - tTu - 0.06f, kh ? 3.5f : 5, x =>
                {
                    var at = casterFeet + new Vector2(U(-0.55f, 0.55f) * casterH, U(-4, 2));
                    if (kh) MocKhoiFb(at, U(0.07f, 0.1f) * casterH, new Vector2(U(-30, 30), -U(80, 130)), Back, 2.5f, 1.1f, 0.85f);
                    else BuiCum(at, new Vector2(U(-30, 30), -U(100, 170)), U(0.06f, 0.09f) * casterH, 0, Back);
                });
            });
            // năng lượng hổ phách bị hút vào tim: xoắn vào, nhanh dần, mật độ tăng tới lúc bắn
            Every(tTu, L - 0.08f, x => 14 + 34 * x, x =>
            {
                float a = U(0, 6.283f), rr = U(0.55f, 1.0f) * casterH;
                NangHut(cFn, goc, tim + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * rr, U(520, 760), U(3.2f, 4.8f), Mathf.Sin(a) < 0 ? Back : Front);
            });
            // ngay trước lúc bắn: vòng co sát vào tim
            At(L - 0.3f, () => VongCo(cFn, goc, 0.95f * casterH, MocKem, Front));
            // BẮN: giờ trúng giữ như bản trước (quãng / 2600)
            float travel = (foeBody - tim).magnitude / 2600f;
            float hit = L + travel;
            float hw = 0.11f * Mathf.Max(casterH, tH);
            float datY = foeFeet.y;
            // tia vẽ sẵn (2026-11-19, da vàng DaTiaVang, GiacTiaFb): tim là quả cầu của rig nên cầu xoáy đầu nòng chỉ hiện ~0,3 s ngay trước lúc bắn
            // (tim "rực sáng cực mạnh rồi bắn"), không che tim suốt pha tụ; bề dày 0,28 casterH; đuôi tia tới đích đúng lúc nổ cầu (tHet) như cũ;
            // 2026-11-25: có lưới shader thì là tia năng lượng kiểu Water Laser bảng hổ phách (ELaser)
            bool fb = CoLaser || HasTia(DaTiaVang);
            float tPhong = L;
            if (fb) tPhong = GiacTiaFb(() => tim, tim, ChamThan(tim, foeBody, tH), Mathf.Max(tTu, hit - 0.42f), hit, L + dur + 0.02f, L + 0.96f, 0.28f * casterH, 1.4f, tH, datY);
            At(tPhong, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(new Color(1f, 0.96f, 0.72f, 0.4f));
                Chop(tim, 0.8f * casterH, 0.09f);
                if (!fb) TiaMoc(tim, ChamThan(tim, foeBody, tH), travel, dur, hw, tH, 1.4f, datY, 0.5f * casterH);
                WExtra(tim, 6, 320);
            });
            // gốc tia: tia vụn văng ngược theo cụm
            Every(L, L + dur - 0.1f, 8, x =>
                TiaVunCum(tim + U2(-8, 8), new Vector2(-dir, U(-0.6f, 0.4f)), 0.8f, 3, U(260, 480), U(3f, 4.4f), Front, CoLaser ? LaserHoPhach.vun1 : MocChanh, w[3]));
            // dọc đường tia: bụi cụm bốc từ đất, lá bị thổi dạt
            bool khTia = HasFb("khoi");
            Every(L + 0.03f, L + dur, 10, x =>
            {
                float f = U(0.15f, 0.85f);
                var at = Vector2.Lerp(tim, foeBody, f);
                var dat = new Vector2(at.x, Mathf.Lerp(casterFeet.y, foeFeet.y, f) + U(-4, 2));
                if (!khTia) BuiCum(dat, new Vector2(dir * U(40, 140), -U(40, 100)), U(0.06f, 0.09f) * tH, 0, Back);
                else if (U(0, 1) < 0.55f) // khung vẽ sẵn (2026-11-19): bụi bốc là cụm khói nhuộm đất dạt theo hướng tia, thưa hơn (cụm to, sống lâu)
                    MocKhoiFb(dat, U(0.07f, 0.1f) * tH, new Vector2(dir * U(60, 150), -U(30, 70)), Back, 3, 1.3f, 0.85f);
                Leaf(at + new Vector2(0, U(-hw, hw)), new Vector2(dir * U(120, 320), U(-160, 60)), U(0.35f, 0.6f), U(3.4f, 5.2f), 300, 1.4f);
            });
            // chỗ trúng: đất dưới chân đối thủ nứt, họa tiết
            At(hit, () =>
            {
                WExtra(foeBody, 8, 380);
                DatNut(foeFeet, tH, 1.2f);
                VetDat(foeFeet + new Vector2(0, 3), 0.55f * tH, 1.2f, w[3]);
            });
            Every(hit + 0.08f, L + dur + travel - 0.05f, 6, x => Shake?.Invoke(0.3f));
            // hết tia: nổ cầu ở chỗ chạm, tia vụn hổ phách phụt từ đất
            float tHet = L + dur + 0.02f;
            At(tHet, () =>
            {
                Shake?.Invoke(0.8f);
                NoCau(foeBody, foeFeet, tH, 1.35f);
                GiacTiaVun(foeFeet, 9, 1.1f);
            });
            return hit;
        }
    }
}
