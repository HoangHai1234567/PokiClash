// Bộ HỎA NHÃN (2026-11-13, mắt lửa bọc giáp, suất hoa_nhan đảo Hỏa; rig ArtGen/Spine/mat_lua*.py).
// Người dùng: chiêu mana "giống skill_02, bổ sung thêm bắn tia lửa từ giữa mắt"; chiêu cuối "dơ 2 tay sang ngang, xoay liên tục quanh cơ
// thể như chong chóng rồi lao vào đập liên tục vào đối thủ"; "fx bạn cứ tự bổ sung nếu thiếu".
// Đi đường bộ Hỏa (StageView.FireFx → PlayMana / PlayUlt): phát ở khung nhả của clip, màu theo Themes["hoa_nhan"] (bảng "lua").
// - tia_mat: TIA lửa liền từ con ngươi (mảng liền 4 lớp: mực, đỏ, cam, lõi kem; mép lượn) + lưỡi lửa chạy dọc tia + toé lửa liên tục ở chỗ
//   trúng; clip giữ dáng bung 0,96 s sau khung nhả (HoldOf 1,0).
// - quyen_xoay: lửa XOÁY quanh đối thủ trong lúc hai nắm tay quay chong chóng đập vào, mỗi nhát một chớp nổ + tia lửa văng (6 nhát cách
//   0,18 s, nhát cuối to nhất), rồi khói tan. Tướng lao tới đối thủ trong clip (lunge), hiệu ứng đặt ở chỗ đối thủ.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public const float TiaMatHold = 1.0f;

        // tia lửa từ con ngươi tới thân đối thủ; trả giây tới lúc đầu tia chạm đối thủ
        public float TiaMat(Vector2 mouth, Vector2 target, float tH, float dur = 0.9f)
        {
            var dd = target - mouth;
            float dist = dd.magnitude;
            var u = dd / Mathf.Max(1, dist);
            var nrm = new Vector2(-u.y, u.x);
            var up = nrm.y < 0 ? nrm : -nrm;
            var src = mouth + u * 6;
            const float T0 = 0.04f, SP = 1700;
            float T1 = T0 + dur;
            float travel = Mathf.Max(0.03f, (dist - 30) / SP);
            var pc = Pal[Th.pal];
            var lop = new[] { Ink, pc[1], pc[2], pc[3] };                 // mực, cam, vàng cam, lõi kem (tươi, không ngả nâu)
            float hw0 = Mathf.Clamp(0.11f * tH, 17, 32);                   // nửa bề ngang tia theo cỡ đối thủ
            // con ngươi loé: chớp nhỏ + vài tia lửa toé ngược
            At(T0, () =>
            {
                Shake?.Invoke(0.18f);
                Explode(src, 0.26f, tH);
                for (int i = 0; i < 4; i++) Spark(src + U2(-4, 4), -u * U(0.4f, 0.9f) + nrm * U(-0.9f, 0.9f), U(200, 340));
            });
            // lõi tia: mảng liền, đầu tia chạy tới đích, cuối tia rút về; mép lượn nhẹ như lửa
            var core = new P { pos = src, life = dur + travel + 0.12f, group = Front };
            core.draw = (q, k, buf) =>
            {
                float a = q.age;
                float head = Mathf.Min(dist - 16, SP * a), tail = Mathf.Max(0, SP * (a - dur));
                if (head - tail < 24) return;
                int n = Mathf.Max(2, Mathf.CeilToInt((head - tail) / 12) + 1);
                for (int li = 0; li < 4; li++)
                {
                    float wf = li < 2 ? 1 : li == 2 ? 0.64f : 0.3f, grow = li == 0 ? 2.6f : 0;
                    int a0 = mp.Count;
                    for (int pass = 0; pass < 2; pass++)
                        for (int i = 0; i < n; i++)
                        {
                            float x = tail + (head - tail) * i / (n - 1);
                            float env = Mathf.Min(1, Mathf.Min((x - tail) / 22 + 0.3f, (head - x) / 14 + 0.5f));
                            float hw = hw0 * (1 + 0.22f * Mathf.Sin(x * 0.07f - a * 34) + 0.12f * Mathf.Sin(x * 0.19f + a * 21)) * env;
                            var c = src + u * x + nrm * (2.2f * Mathf.Sin(x * 0.05f - a * 26));
                            mp.Add(c + nrm * ((pass == 0 ? 1 : -1) * (hw * wf + grow)));
                        }
                    MRibbon(Front, 9 + li * 0.1f, a0, a0 + n, n, lop[li]);
                }
            };
            At(T0, () => Add(core));
            // lưỡi lửa chạy dọc tia, ngọn ngả ngược hướng bắn (vân vẽ tay cho lõi trơn)
            // lưỡi lửa bám dọc tia (sinh ở mép tia, bay theo hướng bắn, to và sống đủ lâu để giữ màu lửa tươi như luồng phun)
            Every(T0 + 0.02f, T1, x => 60 * Mathf.Min(1, (1 - x) * dur / 0.12f), x =>
            {
                float f = U(0.0f, 0.8f), sd = U(0, 1) < 0.5f ? -1 : 1;
                var q = Flame(src + u * dist * f + nrm * sd * hw0 * U(0.3f, 0.9f), u * U(520, 820) + nrm * sd * U(30, 90), U(0.3f, 0.42f), U(9, 12),
                    U(20, 28), "luoi", Th.pal, Front, 1.8f, -240, 1f, 0.06f, 0.05f);
                q.smokeGroup = Back;
            });
            // con ngươi phụt lửa liên tục (gốc tia)
            Every(T0, T1, 22, x => Flame(src + U2(-3, 3), u * U(60, 120) + nrm * U(-40, 40), U(0.2f, 0.28f), 8, U(18, 24), "tron", Th.pal, Front, 2.4f,
                -200, 1.2f, 0, 0));
            float tHit = T0 + travel;
            // chỗ trúng: chớp nổ khi đầu tia tới, rồi toé lửa + tia lửa liên tục tới khi tia rút
            At(tHit, () =>
            {
                Shake?.Invoke(0.28f);
                Explode(target, 0.55f, tH);
                Extra(target, 3, 260);
            });
            Every(tHit + 0.05f, T1, 11, x =>
            {
                float side = U(0, 1) < 0.5f ? -1 : 1;
                var q = Flame(target - u * 14 + U2(-8, 8), -u * U(120, 220) + nrm * side * U(140, 260) + new Vector2(0, -U(60, 140)), U(0.22f, 0.32f),
                    7, U(15, 21), "luoi", Th.pal, Front, 3.5f, -200, 1.4f, 0.2f, 0.1f);
                q.smokeGroup = Back;
                for (int i = 0; i < 2; i++) Spark(target + U2(-10, 10), -u * U(0.3f, 0.8f) + nrm * side * U(0.4f, 1f) + new Vector2(0, -0.4f), U(240, 420));
            });
            At(T1 - 0.04f, () =>
            {
                for (int i = 0; i < 4; i++) Smoke(src + u * dist * U(0.3f, 0.85f) + up * U(6, 18), new Vector2(U(-20, 20), -U(40, 70)), 0, 7, 20, Back);
                for (int i = 0; i < 6; i++) Ash(target + U2(-26, 26));
            });
            return tHit;
        }

        // chiêu cuối: lửa xoáy quanh đối thủ + chuỗi chớp nổ theo nhịp đấm; trả 0 (nhát đầu trúng ngay lúc gọi, khớp khung trúng của clip)
        public float QuyenXoay(Vector2 foeFeet, Vector2 foeBody, float tH, int nhat = 6, float cach = 0.18f)
        {
            var Cc = foeFeet + new Vector2(0, 2);
            float T1 = (nhat - 1) * cach + 0.25f, HT = 0.95f * tH, R = 0.62f * tH, OM = 11;
            Ring(Cc, 0.5f, 0.2f * tH, 1.0f * tH, Th.ring);
            // vòng lửa xoáy: lưỡi lửa bay vòng elip quanh đối thủ, dâng dần lên; nửa xa vẽ sau, nửa gần vẽ trước
            void Orbit(P q, float dt, HatLua s)
            {
                float a = q.ph + OM * q.age, y = q.vy * q.age;
                float rr = q.R0 * (1 - 0.25f * Mathf.Min(1, y / HT));
                q.pos = Cc + new Vector2(rr * Mathf.Cos(a), 0.3f * rr * Mathf.Sin(a) - y);
                q.vel = new Vector2(-rr * Mathf.Sin(a) * OM, 0.3f * rr * Mathf.Cos(a) * OM - q.vy);
                q.group = Mathf.Sin(a) < 0 ? Back : Front;
            }
            Every(0, T1, x => 70 * Mathf.Min(1, x * 5 + 0.4f) * (1 - 0.6f * Mathf.Max(0, (x - 0.8f) / 0.2f)), x =>
            {
                var q = Flame(Cc, Vector2.zero, U(0.32f, 0.46f), U(8, 10), U(18, 26), "luoi", Th.pal, Front, 0, 0, 1.5f, 0.15f, 0.12f);
                q.ph = U(0, 6.28f);
                q.vy = U(0.6f, 1.3f) * HT / q.life;
                q.R0 = R * U(0.85f, 1.15f);
                q.upd = Orbit;
                q.smokeGroup = Back;
            });
            // nhịp đấm: mỗi nhát một chớp nổ ở thân (so le trái phải, cao thấp), tia lửa văng; nhát cuối to nhất
            for (int i = 0; i < nhat; i++)
            {
                bool cuoi = i == nhat - 1;
                float t = i * cach;
                At(t, () =>
                {
                    var c = foeBody + new Vector2(U(-0.22f, 0.22f) * tH, U(-0.18f, 0.12f) * tH);
                    Shake?.Invoke(cuoi ? 0.45f : 0.16f);
                    Explode(c, cuoi ? 1.0f : U(0.45f, 0.6f), tH);
                    int ns = cuoi ? 8 : 4;
                    for (int j = 0; j < ns; j++)
                    {
                        float a = U(0, 6.28f);
                        Spark(c, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.3f), U(260, 480));
                    }
                    if (cuoi)
                    {
                        Ring(Cc, 0.45f, 0.3f * tH, 1.2f * tH, Th.ring);
                        Extra(c, 5, 320);
                    }
                });
            }
            At(T1, () =>
            {
                for (int i = 0; i < 6; i++) Smoke(foeBody + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.1f, 0.6f) * tH), null, 0, 9, 24, Back, "fire");
                for (int i = 0; i < 8; i++) Ash(foeBody + U2(-30, 30));
            });
            return 0;
        }
    }
}
