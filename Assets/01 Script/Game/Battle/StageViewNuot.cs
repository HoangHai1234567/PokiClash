// Chiêu cuối NUỐT đối thủ rồi NHỔ ra (Bùn Ngoạm, suất ho_kim_cuong, 2026-11-17; ghi chú ArtGen/Spine/inbox/quai_bun_ghichu.md mục 11).
// Phần riêng của StageView (partial) để file chính chỉ đổi vài dòng (Update: giữ clip chết; Place: ẩn / bay).
// - Rig khai trong clip skill sự kiện "ngoam" (hàm sập: đối thủ bị nuốt) và "nho" (nhổ ra), cùng xương "mieng_to" (lòng hàm khổng lồ).
//   Từ ngoam tới nho đối thủ ẩn hẳn (ảnh, bóng, dấu trạng thái). Ở nho nó hiện ra ngay miệng (bé NhoCo0 lần, lớn dần), bay theo cung về CHỖ
//   CŨ (code lái, rig chỉ diễn cú nhổ), đáp nảy một nhịp, rồi về clip của nó. Lúc bay hiện clip trúng đòn, nghiêng ngả ra sau.
// - Khung trúng (gai đâm) vẫn trừ máu, hiện số lúc đối thủ đang trong bụng (số nổi trên quả bóng). Đòn làm nó gục: clip chết đứng ở khung
//   đầu tới khi đáp xong (StageView.Update không tăng a.dead lúc bị nuốt) nên nó chết sau khi đáp.
// - Trạng thái suy thẳng từ giờ clip của kẻ đánh, không lưu cờ: clip bị cắt (tua, bỏ qua, hết trận, đổi tướng, kẻ đánh gục) thì đối thủ hiện
//   lại đúng chỗ ngay khung sau. Chỉ nhớ đối thủ đang bay (để phát vệt bùn một lần, đưa nó lên trên kẻ đánh, trả lại cỡ ảnh khi xong).
// - Hiệu ứng ra sân của rig có lớp hạt riêng (RaSanFx): bảng RaSanHat (id tướng → hàm của HatLua), gọi đúng lúc sự kiện của clip appear qua.
using PokiClash.Core;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class StageView
    {
        const float NhoBay = 0.42f, NhoNay = 0.2f, NhoCo0 = 0.5f; // giây bay, giây nảy (giờ animation), cỡ lúc vừa ra khỏi miệng
        Actor nhoV;                                               // đối thủ đang bay
        Actor nhoK;                                               // kẻ đánh đã tính chỗ miệng lúc nhổ
        Vector2 nhoMieng;                                         // chỗ miệng lúc nhổ so với chân kẻ đánh (đơn vị sân, gồm cú lao)

        // pha bị nuốt của v: 0 không, 1 trong bụng, 2 đang bay / nảy (tf: giây animation kể từ lúc nhổ)
        int NuotPha(Actor v, out Actor k, out float tf)
        {
            tf = 0;
            k = v != null ? actors[1 - v.side] : null;
            if (v == null || k == null || k.aola == null || k.loop || k.clip != Skill || k.dead > 0 || v.exit > 0 || Entering(v)) return 0;
            float t0 = k.aola.EventTime(Skill, "ngoam"), t1 = k.aola.EventTime(Skill, "nho");
            if (t0 < 0 || t1 <= t0 || k.t < t0) return 0;
            if (k.t < t1) return 1;
            tf = k.t - t1;
            return tf < NhoBay + NhoNay ? 2 : 0;
        }

        // chỗ miệng (xương mieng_to) của kẻ đánh lúc nhổ, toạ độ sân: chân + cú lao của sân (AolaSticker.Lunge) + xương của rig ở giờ đó
        Vector2 NhoMieng(Actor k)
        {
            var p = Pos[k.side];
            if (nhoK == k) return p + nhoMieng;
            float t1 = k.aola.EventTime(Skill, "nho");
            var other = Pos[1 - k.side];
            if (!k.aola.Lunge(Skill, t1, (other.x - p.x) * 0.72f, (other.y - p.y) * 0.72f, out var o)) o = Vector2.zero;
            if (!k.aola.BoneAt(Skill, "mieng_to", t1, out var b)) b = new Vector2((other.x - p.x) * 0.72f, -0.65f * k.H);
            nhoK = k;
            nhoMieng = o + b;
            return p + nhoMieng;
        }

        // giữa thân đối thủ bay ở phần quãng u (0..1): từ miệng theo cung về giữa thân lúc đứng ở chỗ cũ
        Vector2 NhoThan(Actor v, Actor k, float u)
        {
            var mieng = NhoMieng(k);
            var dich = Pos[v.side] + new Vector2(0, -0.45f * v.H);
            return Vector2.Lerp(mieng, dich, u) + new Vector2(0, -4 * u * (1 - u) * 0.62f * v.H);
        }

        // đối thủ đang bay / nảy (pha 2): dời ảnh (ox, oy so với chỗ đứng x, y), nghiêng, cỡ ảnh; lúc vừa bị nhổ thì phát vệt bùn và đưa lên trên
        void NhoDat(Actor v, Actor k, float tf, float x, float y, ref float ox, ref float oy, ref float rot)
        {
            if (nhoV != v)
            {
                nhoV = v;
                v.rt.SetAsLastSibling(); // vừa ra khỏi miệng: vẽ trên kẻ đánh
                var h = Hat;
                string kind = FireUlt(k.hero, k.form);
                if (h != null && kind != null && kind.StartsWith("n_bun")) h.BunNhoBay(u => NhoThan(v, k, u), NhoBay, Pos[v.side], v.H);
            }
            float back = v.side == 0 ? 1 : -1; // nghiêng ra sau (xa kẻ đánh), như bật lùi
            float sx = 1, sy = 1;
            Vector2 feet;
            if (tf < NhoBay)
            {
                float u = tf / NhoBay;
                float co = u < 0.3f ? Mathf.Lerp(NhoCo0, 1.06f, Out01(u / 0.3f)) : Mathf.Lerp(1.06f, 1f, Mathf.Clamp01((u - 0.3f) / 0.25f));
                sx = sy = co;
                feet = NhoThan(v, k, u) + new Vector2(0, 0.45f * v.H * co);
                rot += back * 0.55f * Mathf.Sin(Mathf.PI * Mathf.Min(1, u * 1.15f));
            }
            else
            {
                float w = Mathf.Clamp01((tf - NhoBay) / NhoNay);
                feet = Pos[v.side] + new Vector2(0, -4 * w * (1 - w) * 0.09f * v.H);
                float sq = (1 - w) * Mathf.Sin(w * Mathf.PI * 2.2f + 0.3f) * 0.1f; // bẹp lúc chạm, nảy, tắt dần
                sx = 1 + sq;
                sy = 1 - sq;
            }
            ox = feet.x - x;
            oy = feet.y - y;
            if (v.aola != null) v.body.localScale = new Vector3(sx, sy, 1);
        }

        // hết bay (hoặc clip của kẻ đánh bị cắt): trả cỡ ảnh
        void NhoXong(Actor v)
        {
            if (nhoV != v) return;
            nhoV = null;
            if (v.aola != null && v.body) v.body.localScale = Vector3.one;
        }

        // ---------- hiệu ứng ra sân bằng lớp hạt ----------

        // id tướng → hàm hạt của HatLua nhận (tên sự kiện của clip appear, chân, chiều cao, hướng mặt); sự kiện không có trong rig thì bỏ qua
        static readonly System.Collections.Generic.Dictionary<string, string[]> RaSanSuKien = new System.Collections.Generic.Dictionary<string, string[]>
        {
            { "ho_kim_cuong", new[] { "nay", "bung" } }, // Bùn Ngoạm (HatBun.cs BunRaSan): cục đất chạm đất hai lần, bung thành tướng
        };

        // gọi từ Update sau EnterBeats (e0: a.enter trước khung này). Clip appear có thể khai một sự kiện nhiều lần (cục đất nảy hai lần)
        void RaSanFx(Actor a, float e0)
        {
            if (a.aola == null || a.dead > 0 || !RaSanSuKien.TryGetValue(a.hero.id, out var evs) || !HasAppear(a) || e0 > EnterLen(a)) return;
            var h = Hat;
            if (h == null) return;
            float dir = Pos[1 - a.side].x >= Pos[a.side].x ? 1 : -1;
            foreach (var n in evs)
                for (int i = 0; i < 4; i++)
                {
                    float tl = a.aola.EventTime(Game.AolaActor.Appear, n, i);
                    if (tl < 0) break;
                    if (e0 >= tl || a.enter < tl) continue;
                    if (a.hero.id == "ho_kim_cuong") h.BunRaSan(n, Pos[a.side], a.H, dir);
                    AddTrauma(n == "bung" ? 0.2f : 0.16f);
                }
        }
    }
}
