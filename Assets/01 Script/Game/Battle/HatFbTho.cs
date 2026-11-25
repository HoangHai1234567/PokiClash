// KHUNG VẼ SẴN cho bộ THỔ (2026-11-19; API ở HatFlip.cs): bụi, khói, gai / cột đá trồi, nổ, lửa trúng, cầu lửa bám vật bay của các tướng
// Thổ (HatTho.cs, HatThach.cs, HatThoTinh.cs, HatBun.cs, HatCoVuong.cs) dùng khung vẽ sẵn 24 khung thay cho cụm hạt. Người dùng 2026-11-18/19:
// "khói rải rác chưa thành cụm, chưa mềm", "gai ... đâm lên xấu", "nổ chưa đẹp"; duyệt bộ khung: "ổn hơn rồi đấy, cho vào game đi".
// Luật chung của các hàm dưới: chưa nhập khung (HasFb false) thì trả null / rơi về hạt cũ như trước.
// NHUỘM: Image nhân màu nên chỉ làm tối / đổi sắc được, không sáng hơn khung gốc. Khung khói xám nâu ~ (124, 109, 102) nhân (200, 170, 130)
// ra nâu sô-cô-la (soi tờ nhuộm thử 2026-11-19), nên bụi đất nhuộm sáng hơn một nấc, ra nâu đất ~ (122, 94, 70). Khung gai sắt xám lam
// ~ (147, 154, 167) nhân cam nhạt ra đá sa thạch / đá nâu be.
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color FbBuiC = C(250, 218, 172);     // khói → bụi đất
        static readonly Color FbCatC = C(255, 228, 176);     // khói → bụi cát (Sa Tích, Sa Long, Sa Trùng)
        static readonly Color FbGomC = C(255, 204, 168);     // khói → bụi đất nung đỏ (phiến Sa Tích)
        static readonly Color FbTrangC = C(244, 228, 240);   // khói → bụi đá trăng (Thổ Tinh)
        static readonly Color FbKhoiDen = C(196, 188, 186);  // khói → khói than của nổ lớn (tối hơn khung gốc một nấc)
        static readonly Color FbSaThach = C(255, 214, 152);  // gai sắt → gai sa thạch (Sa Long, Sa Trùng)
        static readonly Color FbDaNau = C(255, 198, 132);    // gai sắt → gai đá nâu be (sóng chấn Sơn Viên)
        static readonly Color FbPhachC = C(255, 184, 92);    // gai sắt → cột pha lê hổ phách (Tê Thiềm dạng 2)

        // màu bụi vẽ sẵn theo màu dăm của cú trúng (ToNo): cát → bụi cát, đất nung → bụi đỏ, đá trăng → bụi tím nhạt, còn lại bụi đất
        static Color FbTint(Color c1) =>
            c1 == ToCat || c1 == ToCat2 || c1 == ToCat3 || c1 == ToSaThach ? FbCatC : c1 == ToGom || c1 == ToGom2 ? FbGomC : c1 == TtDa || c1 == TtMat ? FbTrangC : FbBuiC;

        // cụm bụi / khói vẽ sẵn: chân (đáy giữa khung) ở chan, cao h; trôi theo vel (có cản), nghiêng nhẹ + lật ngẫu nhiên cho đỡ lặp. speed: khung
        // gốc 1 s một lượt, bụi hạt cũ sống 0,5–0,75 s nên mặc định 1,4. start: bỏ mấy khung đầu (cụm còn nhỏ). life > 0: chạy đúng life giây,
        // mờ dần fadeOut giây cuối (khói phủ đối thủ cần mỏng dần)
        P FbBui(Vector2 chan, Vector2 vel, float h, int group, Color tint, float speed = 1.4f, float alpha = 0.92f, float start = 1, float layer = 31,
            float life = -1, float fadeOut = 0.15f)
        {
            var p = Fb("khoi", chan, h, group, layer, speed, U(-7, 7), U(0, 1) < 0.5f, tint, alpha, life, start, fadeOut);
            if (p != null)
            {
                p.vel = vel;
                p.drag = 2.4f;
            }
            return p;
        }

        // một cụm bụi hạt cũ (ToBui bán kính r1, màu col) → một cụm khói vẽ sẵn cùng tầm (cao 2,4 r1 × to). ti: xác suất sinh (dòng sinh đều:
        // ít cụm mà to). dat: chân cụm ở c (bụi bốc từ đất) hay tâm cụm ở c (bụi giữa không trung). Chưa có khung: cụm hạt cũ y như trước
        P ToBuiFb(Vector2 c, Vector2 vel, float life, float r0, float r1, int group, Color? col, Color tint, float ti = 1, float to = 1, bool dat = false,
            bool tach = false)
        {
            if (!HasFb("khoi"))
            {
                var b = ToBui(c, vel, life, r0, r1, group, tach);
                if (col.HasValue) b.col = col.Value;
                return b;
            }
            if (ti < 1 && U(0, 1) >= ti) return null;
            float h = 2.4f * r1 * to;
            return FbBui(c + new Vector2(0, (dat ? 0.08f : 0.42f) * h), vel * 0.6f, h, group, tint, life > 0 ? Mathf.Clamp(0.85f / life, 0.6f, 2.4f) : 1.4f,
                0.92f, dat ? 1 : 3);                                           // giữa không trung: bỏ ba khung đầu cho cụm bung quanh c
        }

        // một cụm khói than hạt cũ (ToKhoi bán kính r1, đời life) → cụm khói vẽ sẵn nhuộm khói than; ti: xác suất sinh; chưa có khung: hạt cũ
        P ToKhoiFb(Vector2 c, Vector2 vel, float life, float r0, float r1, int group, bool tach = false, float ti = 1, float to = 1)
        {
            if (!HasFb("khoi")) return ToKhoi(c, vel, life, r0, r1, group, tach);
            if (ti < 1 && U(0, 1) >= ti) return null;
            float h = 2.4f * r1 * to;
            return FbBui(c + new Vector2(0, 0.42f * h), vel * 0.6f, h, group, FbKhoiDen, Mathf.Clamp(0.95f / life, 0.4f, 2.4f), 0.95f, 3, 32);
        }

        // khung chạy theo BA PHA (gai / cột trồi): lên (khung f0 → f1 trong t1 giây), giữ (f1 → f2 trong giu giây: khung giữ có lắc nhẹ sẵn), tàn
        // (f2 → khung cuối trong t3 giây). Khớp đúng nhịp trồi / giữ / lún của hiệu ứng cũ thay vì một tốc độ đều
        P FbBaPha(string fx, Vector2 pos, float h, int group, float layer, Color tint, float f0, float f1, float t1, float f2, float giu, float t3,
            bool flip = false, float ang = 0, float alpha = 1)
        {
            var art = FbArt(fx);
            if (art == null) return null;
            var d = Fbs[fx];
            float cuoi = d.n - 1;
            t1 = Mathf.Max(0.02f, t1);
            giu = Mathf.Max(0.02f, giu);
            t3 = Mathf.Max(0.02f, t3);
            var p = new P { pos = pos, group = group, life = t1 + giu + t3 };
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                float f = t < t1 ? Mathf.Lerp(f0, f1, t / t1) : t < t1 + giu ? Mathf.Lerp(f1, f2, (t - t1) / giu) : Mathf.Lerp(f2, cuoi, (t - t1 - giu) / t3);
                DrawFb(buf, art, d, f, q.pos, h, q.group, layer, ang, flip, tint, alpha);
            };
            return Add(p);
        }

        // gai / cột đá trồi (khung gai sắt nhuộm màu đá): chân ở chan, ĐỈNH gai cao ~ cao (khung giữ cao 0,97 khung). Bỏ phần nứt đất dài của
        // khung (khung 0–3; vết nứt, hố do ToNut / ToHo lo): gai phóng lên tới khung 11 trong tLen, giữ tới khung 18 trong giu, vỡ rơi trong tLun
        P FbGai(Vector2 chan, float cao, int group, Color tint, float tLen, float giu, float tLun, bool flip = false, float ang = 0, float layer = 24)
            => FbBaPha("gai_sat", chan, cao / 0.97f, group, layer, tint, 4, 11, tLen, 18, giu, tLun, flip, ang);

        // cầu lửa vẽ sẵn BÁM một vật đang bay (thiên thạch, quả cầu của rig: game lái, lớp hạt không đọc xương nên đi theo đường đo sẵn pos(T)):
        // đầu cầu (tâm khung 73 % / 46 %) ở pos, đuôi lửa ngược hướng bay (huong lúc gọi; khung vẽ bay sang phải, bay sang trái thì lật như
        // FbFly); lặp tới hết life rồi mờ nhanh. Đầu cầu tròn bán kính ~0,25 h: h ≈ 4 × bán kính vật thì lõi vàng nấp sau vật, vành lửa ló ra
        P FbCauBam(Func<float, Vector2> pos, Vector2 huong, float h, float life, int group = Back, float layer = 34, float alpha = 1)
        {
            var dv = Unit(huong);
            bool flip = dv.x < 0;
            float ang = flip ? Mathf.Atan2(dv.y, -dv.x) * Mathf.Rad2Deg : Mathf.Atan2(-dv.y, dv.x) * Mathf.Rad2Deg;
            var p = Fb("cau_lua", pos(T), h, group, layer, 1, ang, flip, null, alpha, Mathf.Max(0.05f, life), U(0, 24), 0.06f);
            if (p != null)
            {
                p.upd = (q, dt, s) =>
                {
                    q.pos = pos(s.T);
                    q.vel = Vector2.zero;
                };
                // cầu tròn Blender (2026-11-24) không còn đuôi vẽ sẵn: vệt "duoi_lua" sau cầu (quả cầu bán kính 0,25 h), lớp dưới cầu
                DuoiLua(() => p.pos, () => !p.dead && p.age < p.life, 0.25f * h, group, layer - 6);
            }
            return p;
        }
    }
}
