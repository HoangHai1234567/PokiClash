// SÓNG ÂM VẼ CHÌ (2026-11-19). Người dùng: "phần sóng âm vẫn chưa ổn đâu, làm đơn giản thôi, bạn có thể dùng shader bẻ cong tạo kiểu
// shockwave hoặc làm 1 vài nét vẽ tay tô chì màu xám nhạt làm sóng âm". Chọn nét chì: hợp nét vẽ tay của sân (trời, cát cũng gạch chì), còn
// shader bẻ cong trên uGUI phải render cả sân ra texture rồi mới bẻ được, nặng trên điện thoại.
// Một cung = 2–3 nét chì song song (ảnh hat_kr_songchi_<i>, ArtGen/Spine/hat_songchi.py: lồi về +x, dây cung 86 % chiều cao khung, đỉnh lưng
// ở 62 % bề ngang khung), KHÔNG viền mực, nhuộm xám nhạt. Bay từ miệng tới đích (mặt trước thân đối thủ), nở to dần, rung nhẹ, nhạt dần
// theo quãng, tới nơi thì mờ hẳn trong khoảng 0,15 s. Mỗi lần gầm chỉ 3–4 cung. Chưa nhập ảnh thì dùng cung mảnh cũ hat_arc_0, cũng không viền.
// Dùng ở: Rồng Trúc (HatRong.NRongGam), Bạch Viêm Hổ (HatHo.NHoGam), Thổ Tinh (HatThoTinh.TtSongGam).
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color SongChiC = new Color32(158, 154, 147, 255); // xám nhạt hơi ấm (vòng 2: đậm hơn một nấc, 188 chìm trên cát / biển)

        // một cung: h0 -> h1 là cỡ khung ảnh (chiều cao) lúc ra khỏi miệng -> lúc tới đích; v đơn vị sân / giây; alpha tối đa
        P SongChi(Vector2 tu, Vector2 den, float h0, float h1, float v, float alpha = 0.92f, int group = Front)
        {
            var d = den - tu;
            float toi = Mathf.Max(0.08f, d.magnitude / v);
            var p = new P
            {
                pos = tu, home = tu, aim = Unit(d), vy = v, life = toi + 0.15f, tb = toi, R0 = h0, R1 = h1, wd = alpha, group = group,
                seed = rng.Next(4)
            };
            p.draw = (q, k, buf) =>
            {
                float t = q.age, f = Mathf.Clamp01(t / q.tb);
                float h = Mathf.Lerp(q.R0, q.R1, EaseOut(f));
                float a = Mathf.Min(1, t / 0.05f) * q.wd * (1 - 0.12f * f);
                if (t > q.tb) // tới đích: nở thêm chút rồi mờ hẳn, không trùm lên mặt con bị trúng
                {
                    float u = Mathf.Clamp01((t - q.tb) / Mathf.Max(0.02f, q.life - q.tb));
                    a *= 1 - u;
                    h *= 1 + 0.08f * u;
                }
                if (a < 0.03f) return;
                var dinh = q.home + q.aim * (Mathf.Min(t, q.tb) * q.vy);
                float ang = VelAng(q.aim) + 2.5f * Mathf.Sin(t * 41 + q.seed * 1.9f); // rung nhẹ như nét vẽ tay
                var sp = S("kr_songchi_" + q.seed);
                if (sp != null)
                {
                    Put(buf, q.group, 44.6f, sp, SongChiC, dinh - q.aim * (0.12f * h), h, 1, ang, a);
                    return;
                }
                float R = 0.5f * h; // dự phòng: giữa cung của ảnh hat_arc_0 nằm ở góc 284,7 độ
                Put(buf, q.group, 44.6f, S("arc_0"), SongChiC, dinh - q.aim * (R * 0.72f), 2 * R, 1, ang - 284.7f, a);
            };
            return Add(p);
        }
    }
}
