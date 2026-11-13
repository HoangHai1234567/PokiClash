// Bộ hiệu ứng của GIÁC MỘC (2026-11-13, thú cổ thụ một sừng, suất moc_tinh đảo Mộc; rig ArtGen/Spine/giac_moc*.py trên rig monster_3804).
// Người dùng: "tấn công thường dậm chân mạnh tạo vết nứt tới đối thủ (fx làm riêng)"; "chiêu cast mana ngẩng lên tụ cầu năng lượng ở
// trên đỉnh sừng rồi cúi xuống phóng tia năng lượng từ cầu"; "chiêu cuối mở phần bụng, trong phần bụng có 1 quả cầu năng lượng kiểu
// trái tim phát sáng (luôn có sẵn), nó sẽ phát sáng cực mạnh rồi bắn ra 1 tia sáng cực mạnh chết chóc vào người đối thủ".
// Đi chung đường bộ Thủy / Mộc (HatNuoc.PlayNuoc, mã "n_"): phát lúc clip BẮT ĐẦU kèm lead (giờ trúng của clip), màu lấy từ WThemes
// ("moc_tinh": hổ phách). Dùng lại quả cầu và gió hút của Gạc Đá (HatDa.cs: CauLa, GatherLa), tia của bộ Thủy (NTia), đất nứt và bụi
// của rồng trúc / Lâm Tượng (HatRong.cs: DatNut; HatVoi.cs: Bui; HatDa.cs: DaVun).
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
        static readonly Color GiacLoi = C(255, 250, 224);

        static Vector2 GiacSungAt(Vector2 feet, float h, float dir, float clipT)
        {
            int n = GiacSung.Length / 2;
            float x = Mathf.Clamp(clipT / 0.1f, 0, n - 1.001f);
            int i = (int)x;
            float w = x - i;
            return feet + new Vector2(dir * Mathf.Lerp(GiacSung[2 * i], GiacSung[2 * i + 2], w) * h, -Mathf.Lerp(GiacSung[2 * i + 1], GiacSung[2 * i + 3], w) * h);
        }

        // tia vụn hổ phách bật lên từ khe đất
        void GiacTiaVun(Vector2 at, int n, float manh, int group = Front)
        {
            for (int i = 0; i < n; i++)
            {
                var d = Unit(new Vector2(U(-0.7f, 0.7f), -1));
                var q = Spark(at + new Vector2(U(-10, 10), U(-4, 0)), d, U(260, 520) * manh, U(0.18f, 0.34f), U(6, 10), 620, group, 4);
                q.col = (i & 1) == 0 ? W[2] : W[3];
            }
        }

        // ĐÒN ĐÁNH THƯỜNG: co chân trước rồi DẬM → đất nứt chạy tới đối thủ, ánh hổ phách lọt qua khe → đất bật dưới chân đối thủ.
        public float NGiacDam(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.3f, lead);
            float tDam = Mathf.Max(0.05f, L - 0.18f);
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var chan = casterFeet + new Vector2(dir * GiacChanX * casterH, 0);
            // co chân: bụi nhẹ dưới chân trụ
            float tCo = Mathf.Max(0.02f, L - 0.60f);
            Every(tCo, tCo + 0.18f, 12, x =>
                Bui(casterFeet + new Vector2(-dir * U(0.05f, 0.35f) * casterH, U(-4, 2)), new Vector2(-dir * U(20, 70), -U(20, 60)), 0, 3, 8, Back));
            // DẬM
            At(tDam, () =>
            {
                Shake?.Invoke(0.85f);
                Ripple(chan + new Vector2(0, 2), 0.1f * casterH, 0.75f * casterH, 0.5f, BuiC2);
                RingN(chan + new Vector2(0, 2), 0.32f, 0.08f * casterH, 0.46f * casterH, BuiC, 0.3f, Floor, 30.6f);
                for (int i = 0; i < 12; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(chan + new Vector2(sd * U(6, 34), U(-6, 3)), new Vector2(sd * U(120, 300), -U(15, 80)), U(0.45f, 0.8f), 5, U(10, 16), i < 8 ? Back : Front);
                }
                for (int i = 0; i < 8; i++) DaVun(chan + new Vector2(U(-22, 22), -4), new Vector2(U(-220, 220), -U(240, 450)), U(0.45f, 0.75f), U(3f, 4.8f));
                for (int i = 0; i < 5; i++) Leaf(chan + new Vector2(U(-20, 20), -U(4, 14)), new Vector2(U(-140, 140), -U(260, 420)), U(0.5f, 0.8f), U(4.5f, 7f), 700, 1.2f);
                GiacTiaVun(chan, 5, 0.8f);
            });
            // vết nứt chạy tới đối thủ: năm chỗ đất bật, cái sau to hơn, ánh hổ phách lọt qua khe
            const int N = 5;
            for (int i = 0; i < N; i++)
            {
                int j = i;
                At(tDam + (L - tDam - 0.02f) * (j + 1) / (N + 1), () =>
                {
                    var at = Vector2.Lerp(chan, foeFeet, (j + 1f) / (N + 1));
                    DatNut(at, tH, 0.65f + 0.13f * j);
                    GiacTiaVun(at, 2 + j / 2, 0.7f + 0.08f * j, Back);
                    Ripple(at + new Vector2(0, 2), 0.03f * tH, 0.16f * tH, 0.22f, W[2]);
                });
            }
            // trúng: đất dưới chân đối thủ bật tung, cột ánh hổ phách phụt lên
            At(L, () =>
            {
                Shake?.Invoke(0.7f);
                DatNut(foeFeet, tH, 1.35f);
                GiacTiaVun(foeFeet, 12, 1.25f);
                BurstFlash(foeFeet + new Vector2(0, -0.18f * tH), 0.62f * tH, Back, 0.16f);
                RingN(foeFeet + new Vector2(0, 2), 0.3f, 0.08f * tH, 0.6f * tH, W[2], 0.3f, Floor, 30.8f);
                WExtra(foeBody, 5, 300);
            });
            return L;
        }

        // CẦU ĐỈNH SỪNG + TIA (chiêu mana): năng lượng từ ngực hé mở chảy lên, gió và lá bị hút về đỉnh sừng, quả cầu lớn dần theo đỉnh
        // sừng đang ngẩng cao; cúi đầu chĩa sừng về trước, cầu chớp một nhịp rồi nhả tia thẳng vào thân đối thủ; cầu cạn dần lúc tia chảy.
        public float NGiacTia(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
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
                float w = SmoothStep(L - 0.10f, L - 0.01f, t) * (1 - SmoothStep(L + dur, L + dur + 0.1f, t));
                return Vector2.Lerp(p, mouth, w) + new Vector2(0, 1.5f * Mathf.Sin(age * 11));
            };
            Func<float, float> rFn = age =>
            {
                float t = tTu + age;
                if (t > L + dur) return 0;
                float g = Mathf.Clamp01(age / Mathf.Max(0.1f, L - tTu - 0.25f));
                float r = rFull * (0.2f + 0.8f * g) * Mathf.Min(1, age / 0.08f);
                if (t > L) r *= 1 - 0.45f * Mathf.Clamp01((t - L) / dur);
                return r * (1 + 0.06f * Mathf.Sin(age * (12 + 12 * g)));
            };
            At(tTu, () =>
            {
                CauLa(cFn, L + dur - tTu, rFn);
                GatherLa(cFn, 0, L - tTu - 0.3f, 0.5f * casterH, 24);
            });
            // năng lượng từ tim (ngực hé mở) bốc lên đỉnh sừng trong lúc ngẩng
            Every(tTu, 1.10f / kT, 26, x =>
            {
                var dich = cFn(T0Giac(x, tTu, 1.10f / kT) - tTu);
                var d = Unit(dich - tim + new Vector2(U(-30, 30), 0));
                var q = Spark(tim + U2(-10, 10), d, U(520, 760), U(0.3f, 0.45f), U(6, 9), 0, Back, 1.2f);
                q.col = U(0, 1) < 0.5f ? W[2] : W[3];
            });
            At(L, () =>
            {
                Shake?.Invoke(0.35f);
                BurstFlash(mouth, 0.4f * casterH, Back);
                WExtra(mouth, 5, 220);
            });
            // tia năng lượng thẳng từ quả cầu (bản đầu dùng tia nước NTia nhuộm hổ phách: có bọt trắng và sóng lượn, trông như phun nước)
            float travel = (foeBody - mouth).magnitude / 2600f;
            float hit = L + travel;
            At(L, () => GiacTiaSang(mouth, foeBody + new Vector2(dir * 0.06f * tH, 0), dur, 0.042f * Mathf.Max(casterH, tH)));
            At(hit, () =>
            {
                BurstFlash(foeBody, 0.6f * tH, Front, 0.14f);
                RingN(foeBody, 0.26f, 0.1f * tH, 0.55f * tH, W[3], 1, Front, 36);
                WExtra(foeBody, 6, 300);
            });
            Every(hit, L + dur + travel, 30, x =>
            {
                float a = U(-1.8f, 1.8f);
                var q = Spark(foeBody + U2(-8, 8), new Vector2(dir * Mathf.Cos(a), Mathf.Sin(a)), U(280, 560), U(0.16f, 0.28f), U(5, 9), 420, Front, 4);
                q.col = U(0, 1) < 0.5f ? W[2] : GiacLoi;
            });
            Every(hit + 0.1f, L + dur + travel - 0.05f, 6, x =>
            {
                Shake?.Invoke(0.18f);
                BurstFlash(foeBody + U2(-0.1f, 0.1f) * tH, U(0.3f, 0.44f) * tH, Front, 0.09f);
            });
            At(L + dur + travel, () =>
            {
                for (int i = 0; i < 8; i++)
                    Leaf(foeBody + U2(-0.2f, 0.2f) * tH, new Vector2(U(-180, 180), -U(120, 320)), U(0.45f, 0.7f), U(4, 6.5f), 600, 1.2f);
            });
            return hit;
        }

        static float T0Giac(float x, float t0, float t1) => t0 + (t1 - t0) * Mathf.Clamp01(x);

        // TIA SÁNG: một dải năng lượng thẳng, dày, viền mực, ba lớp màu (đậm, tươi, lõi sáng), đầu tia lao rất nhanh, thân rung nhẹ.
        P GiacTiaSang(Vector2 src, Vector2 dst, float dur, float hw0, int group = Front)
        {
            var dd = dst - src;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            const float SP = 2600;
            float travel = dist / SP;
            var core = new P { pos = src, life = dur + travel + 0.14f, group = group, stops = W };
            core.draw = (q, k, buf) =>
            {
                float a = q.age;
                float head = Mathf.Min(dist + 26, SP * a), tail = Mathf.Max(0, SP * (a - dur));
                if (head - tail < 24) return;
                int n = Mathf.Max(2, Mathf.CeilToInt((head - tail) / 16) + 1);
                float no = Mathf.Min(1, a / 0.07f + 0.25f) * (1 - 0.55f * SmoothStep(dur - 0.22f, dur, a)); // nở lúc đầu, thon lại lúc tắt
                for (int li = 0; li < 4; li++)
                {
                    float wf = li < 2 ? 1 : li == 2 ? 0.70f : 0.34f, grow = li == 0 ? 2.6f : 0;
                    int a0 = mp.Count;
                    for (int pass = 0; pass < 2; pass++)
                        for (int i = 0; i < n; i++)
                        {
                            float x = tail + (head - tail) * i / (n - 1);
                            float hw = hw0 * no * (1 + 0.09f * Mathf.Sin(x * 0.045f - a * 48)) *
                                       Mathf.Min(1, Mathf.Min((x - tail) / 46 + 0.3f, (head - x) / 30 + 0.6f));
                            mp.Add(src + u * x + nrm * ((pass == 0 ? 1 : -1) * (hw * wf + grow)));
                        }
                    MRibbon(group, 9 + li * 0.1f, a0, a0 + n, n, li == 0 ? Ink : li == 3 ? GiacLoi : q.stops[li]);
                }
            };
            return Add(core);
        }

        // TIM CỔ THỤ KHAI QUANG (chiêu cuối): vỏ ngực mở, quả tim đập nhanh dần, mỗi nhịp một vòng sáng lan, gió và lá quanh người bị hút
        // vào tim; đầy thì loé trắng một nhịp rồi BẮN tia sáng dày từ tim xuyên thân đối thủ, ghìm một giây: thân đối thủ toé tia vụn liên
        // hồi, đất dưới đường tia bốc bụi, màn rung; hết tia: nổ lá, vòng lan, lá rơi lả tả.
        public float NGiacTim(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float L = Mathf.Max(0.8f, lead);
            float kT = 2.05f / L;
            float tMo = 0.15f / kT, tTu = 1.00f / kT;
            const float dur = 1.0f;
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            var tim = casterFeet + new Vector2(dir * GiacTimX * casterH, -GiacTimY * casterH);
            Func<float, Vector2> cFn = age => tim;
            // vỏ ngực mở: bụi và lá bật quanh chân
            At(tMo, () =>
            {
                Ripple(casterFeet + new Vector2(0, 2), 0.15f * casterH, 0.7f * casterH, 0.5f, BuiC2);
                for (int i = 0; i < 8; i++)
                    Bui(casterFeet + new Vector2(U(-0.4f, 0.4f) * casterH, U(-4, 2)), new Vector2(U(-90, 90), -U(30, 100)), 0, 4, 11, Back);
            });
            // tim tụ lực: nhịp đập nhanh dần (0,34 s → 0,12 s), mỗi nhịp một vòng sáng + chớp nhỏ
            float tb = tTu, gap = 0.34f;
            while (tb < L - 0.12f)
            {
                float g = Mathf.Clamp01((tb - tTu) / Mathf.Max(0.2f, L - tTu));
                float tt = tb;
                At(tt, () =>
                {
                    RingN(tim, 0.26f, 0.05f * casterH, (0.22f + 0.2f * g) * casterH, W[2], 1f, Front, 36);
                    BurstFlash(tim, (0.2f + 0.16f * g) * casterH, Front, 0.09f);
                    if (g > 0.5f) Shake?.Invoke(0.12f + 0.2f * g);
                });
                gap = Mathf.Lerp(0.34f, 0.12f, g);
                tb += gap;
            }
            At(tTu, () =>
            {
                GatherLa(cFn, 0, L - tTu - 0.06f, 1.2f * casterH, 78);
                Every(0, L - tTu - 0.06f, 12, x =>
                    Bui(casterFeet + new Vector2(U(-0.55f, 0.55f) * casterH, U(-4, 2)), new Vector2(U(-30, 30), -U(130, 240)), 0, 2.5f, 7, Back));
            });
            // tia vụn hổ phách bị hút vào tim
            Every(tTu, L - 0.08f, x => 20 + 50 * x, x =>
            {
                float a = U(0, 6.283f), rr = U(0.5f, 1.0f) * casterH;
                var from = tim + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.8f) * rr;
                var q = Spark(from, Unit(tim - from), rr / 0.26f, 0.26f, U(5, 8), 0, Front, 0);
                q.col = U(0, 1) < 0.5f ? W[2] : W[3];
            });
            // đầy: loé
            At(L - 0.08f, () =>
            {
                BurstFlash(tim, 1.0f * casterH, Front, 0.12f);
                RingN(tim, 0.22f, 0.1f * casterH, 0.9f * casterH, GiacLoi, 1f, Front, 36.2f);
            });
            // BẮN
            float travel = (foeBody - tim).magnitude / 2600f;
            float hit = L + travel;
            float hw = 0.125f * Mathf.Max(casterH, tH);
            At(L, () =>
            {
                Shake?.Invoke(1f);
                FlashScreen?.Invoke(new Color(1f, 0.93f, 0.66f, 0.42f));
                GiacTiaSang(tim, foeBody + new Vector2(dir * 0.1f * tH, 0), dur, hw);
                BurstFlash(tim, 0.7f * casterH, Front, 0.16f);
                WExtra(tim, 8, 320);
            });
            // gốc tia: tim loé liên hồi, tia vụn văng ngược
            Every(L, L + dur - 0.1f, 22, x =>
            {
                var q = Spark(tim + U2(-8, 8), Unit(new Vector2(-dir * U(0.3f, 1f), U(-1f, 1f))), U(260, 520), U(0.16f, 0.3f), U(5, 9), 200, Front, 3);
                q.col = U(0, 1) < 0.5f ? W[3] : GiacLoi;
            });
            Every(L + 0.1f, L + dur - 0.12f, 7, x => BurstFlash(tim, U(0.34f, 0.5f) * casterH, Front, 0.09f));
            // dọc đường tia: bụi đất bốc, lá bị thổi dạt
            Every(L + 0.03f, L + dur, 34, x =>
            {
                var at = Vector2.Lerp(tim, foeBody, U(0.12f, 0.9f));
                Bui(new Vector2(at.x, casterFeet.y + U(-4, 2)), new Vector2(dir * U(40, 160), -U(40, 130)), 0, 3, 10, Back);
                if (U(0, 1) < 0.35f) Leaf(at + new Vector2(0, U(-hw, hw)), new Vector2(dir * U(120, 320), U(-160, 60)), U(0.35f, 0.6f), U(4, 6.5f), 300, 1.4f);
            });
            // chỗ trúng: toé liên hồi suốt lúc tia chảy, rung màn từng nhịp
            At(hit, () =>
            {
                BurstFlash(foeBody, 0.9f * tH, Front, 0.16f);
                RingN(foeBody, 0.3f, 0.12f * tH, 0.8f * tH, W[3], 1, Front, 36);
                WExtra(foeBody, 10, 380);
                DatNut(foeFeet, tH, 1.2f);
            });
            Every(hit, L + dur + travel, 46, x =>
            {
                float a = U(-1.9f, 1.9f);
                var d = new Vector2(dir * Mathf.Cos(a), Mathf.Sin(a));
                var q = Spark(foeBody + U2(-10, 10), d, U(340, 700), U(0.16f, 0.32f), U(6, 11), 420, Front, 4);
                q.col = U(0, 1) < 0.5f ? W[2] : GiacLoi;
            });
            Every(hit + 0.08f, L + dur + travel - 0.05f, 9, x =>
            {
                Shake?.Invoke(0.35f);
                BurstFlash(foeBody + U2(-0.12f, 0.12f) * tH, U(0.4f, 0.62f) * tH, Front, 0.1f);
            });
            // hết tia: nổ lá, vòng lan, bụi dưới chân, lá rơi lả tả
            float tHet = L + dur + travel;
            At(tHet, () =>
            {
                Shake?.Invoke(0.8f);
                LaNo(foeBody, foeFeet, tH, 1.7f);
                RingN(foeBody, 0.34f, 0.14f * tH, 0.9f * tH, W[3], 1, Front, 36);
                Ripple(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.85f * tH);
                GiacTiaVun(foeFeet, 10, 1.1f);
            });
            Every(tHet + 0.05f, tHet + 0.5f, 26, x =>
                Leaf(foeBody + new Vector2(U(-0.55f, 0.55f) * tH, -U(0.2f, 0.75f) * tH), new Vector2(U(-40, 40), U(20, 80)), U(0.5f, 0.8f), U(4, 6.5f), 260, 1.2f,
                    U(0, 1) < 0.5f ? Back : Front));
            return hit;
        }
    }
}
