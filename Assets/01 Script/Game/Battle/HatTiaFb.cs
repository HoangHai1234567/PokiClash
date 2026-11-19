// TIA VẼ SẴN (2026-11-19). Người dùng: "các tia năng lượng/nước như này nhìn vẫn chưa đã" (thân tia là ống đặc thẳng, hai đầu nhỏ). Nâng lên:
//  - thân tia = nhiều ĐOẠN vẽ sẵn (khung lặp 24, đoạn năng lượng / nước đầu đuôi thon, sợi xoắn quấn quanh) chồng lên nhau và TRÔI liên tục từ
//    miệng tới đích: tia liền mà chảy, mép gợn; không cần ảnh nối liền mạch (GPT vẽ không khớp mép);
//  - đầu nòng: khung cầu xoáy có tia lóe, lớn dần trong pha tụ, phập phồng lúc bắn;
//  - chỗ trúng: khung va chạm lặp suốt lúc tia dội (bông toé ngược, vòng loang), lật theo hướng tia;
//  - nhịp: tụ (tTu) → phóng (đầu tia vươn tới đích ~0,1 s, đoạn đầu phình) → dội (bề dày phập phồng ~8 lần / giây, gợn ngang)
//    → tắt (ngừng nhả: đuôi tia rời miệng, bay nốt vào đích; đầu nòng, bông trúng mờ dần).
// Khung: ArtGen/Spine/vfx_gen (cat_khung.py, chi_phang.py, xuat_fb.py), bảng HatFlip.Fbs. Nhịp trúng (FoePulse / NuocPulse...) do hàm gọi giữ.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        public sealed class TiaSkin
        {
            public string doan, nong, trung;
            public float doanDay = 0.42f;  // bề dày thân tia / cao khung đoạn (đo trên khung)
            public float nongCo = 2.3f;    // cao khung đầu nòng / bề dày tia
            public float trungCo = 2.9f;   // cao khung va chạm / bề dày tia
            public Color tint = Color.white;
        }

        // Lộc Phong: năng lượng lá xanh, lá phong đỏ cam cuốn theo; tia nước: lam / ngọc lam, sợi bọt xoắn (đầu nòng dùng cầu nước có sẵn)
        public static readonly TiaSkin DaTiaMoc = new TiaSkin { doan = "tia_moc_doan", nong = "tia_moc_nong", trung = "tia_moc_trung", doanDay = 0.38f };
        public static readonly TiaSkin DaTiaNuoc = new TiaSkin { doan = "tia_nuoc_doan", nong = "cau_nuoc", trung = "tia_nuoc_trung", nongCo = 1.9f, doanDay = 0.53f };
        // lửa: đoạn lửa có sợi lửa xoắn, cầu lửa xoáy, lửa toé ngược (tia mắt Hỏa Nhãn, tia nhiệt Thổ Tinh...); vàng: năng lượng Mặt Trời, dải
        // vàng xoắn + sao (tia Mặt Trời Nhật Vương, tia năng lượng Thần Cơ, tia hổ phách Giác Mộc...)
        public static readonly TiaSkin DaTiaLua = new TiaSkin { doan = "tia_lua_doan", nong = "tia_lua_nong", trung = "tia_lua_trung", doanDay = 0.51f };
        public static readonly TiaSkin DaTiaVang = new TiaSkin { doan = "tia_vang_doan", nong = "tia_vang_nong", trung = "tia_vang_trung", doanDay = 0.5f };

        public bool HasTia(TiaSkin k) => k != null && HasFb(k.doan) && HasFb(k.nong) && HasFb(k.trung);

        // thời gian đầu tia vươn từ miệng tới đích (quãng đơn vị sân); hàm tự vẽ thân tia dùng để khớp nhịp với TiaFb
        public static float TiaVuon(float quang) => Mathf.Clamp(quang / 2600f, 0.07f, 0.14f);

        public float TiaFb(TiaSkin k, Vector2 tu, Vector2 toi, float day, float tTu, float tBan, int group = Front, float layer = 36,
            Action onCham = null, float nongK = 1, float trungK = 1, bool coDoan = true) =>
            TiaFb(k, () => tu, () => toi, day, tTu, tBan, group, layer, onCham, nongK, trungK, coDoan);

        // Phát tia từ miệng tu() tới chỗ trúng toi() (hàm để bám theo rig đang động); day: bề dày thân tia (đơn vị sân);
        // tTu: giây tụ ở miệng trước khi bắn; tBan: giây tia dội (tính từ lúc chạm). Trả giờ chạm (giây kể từ lúc gọi). onCham gọi lúc chạm.
        // nongK / trungK: nhân cỡ cầu đầu nòng / bông va chạm cho riêng chiêu (vd. đầu nòng nhỏ hơn khi tia bắn ra từ một vật nhỏ)
        // coDoan = false: KHÔNG thả đoạn thân vẽ sẵn (hàm gọi tự vẽ thân tia liền bằng mảng, vd. tia nước 2026-11-19: "tia nước scale to lên
        // xấu quá, làm lại nhìn mềm mại hơn và 3D hơn"); đầu nòng, bông va chạm, giờ chạm vẫn như cũ. Thời gian vươn = TiaVuon(quãng)
        public float TiaFb(TiaSkin k, Func<Vector2> tu, Func<Vector2> toi, float day, float tTu, float tBan, int group = Front, float layer = 36,
            Action onCham = null, float nongK = 1, float trungK = 1, bool coDoan = true)
        {
            if (!HasTia(k)) return -1;
            var dDoan = Fbs[k.doan];
            float hDoan = day / Mathf.Max(0.1f, k.doanDay);       // cao khung đoạn
            float lDoan = hDoan * dDoan.aspect;                    // dài một đoạn
            float buoc = 0.34f * lDoan;                            // đoạn chồng ~2/3 lên nhau
            float dai0 = (toi() - tu()).magnitude;
            float vChay = Mathf.Max(380, dai0 / 0.32f);           // tốc trôi của đoạn (đơn vị sân / giây)
            float tVuon = TiaVuon(dai0);                           // đầu tia vươn tới đích
            float tCham = tTu + tVuon;
            float t0 = T;

            // đầu nòng: lớn dần trong pha tụ, phập phồng lúc bắn, mờ dần sau khi tắt
            var aN = FbArt(k.nong);
            var dN = Fbs[k.nong];
            float hN = k.nongCo * day * nongK;
            var pn = new P { pos = tu(), group = group, life = tCham + tBan + 0.25f };
            pn.upd = (q, dt, L) => q.pos = tu();
            pn.draw = (q, kk, buf) =>
            {
                float a = q.age;
                float lon = a < tTu ? Mathf.Lerp(0.35f, 1f, EaseOut(a / Mathf.Max(0.01f, tTu))) : 1 + 0.07f * Mathf.Sin((a - tTu) * 50);
                float al = Mathf.Clamp01(a / 0.06f) * Mathf.Clamp01((q.life - a) / 0.22f);
                var dir = Unit(toi() - q.pos);
                bool flip = dir.x < 0;
                float ang = flip ? Mathf.Atan2(dir.y, -dir.x) * Mathf.Rad2Deg : Mathf.Atan2(-dir.y, dir.x) * Mathf.Rad2Deg;
                DrawFb(buf, aN, dN, a * dN.fps * 1.2f, q.pos, hN * lon, q.group, layer + 2, ang, flip, k.tint, al);
            };
            Add(pn);

            // bông trúng lặp ở đích suốt lúc tia dội
            At(tCham, () =>
            {
                onCham?.Invoke();
                var aT = FbArt(k.trung);
                var dT = Fbs[k.trung];
                float hT = k.trungCo * day * trungK;
                var pt = new P { pos = toi(), group = group, life = tBan + 0.3f };
                pt.upd = (q, dt, L) => q.pos = toi();
                pt.draw = (q, kk, buf) =>
                {
                    float a = q.age;
                    float lon = Mathf.Lerp(0.55f, 1f, EaseOut(Mathf.Clamp01(a / 0.12f))) * (1 + 0.06f * Mathf.Sin(a * 47));
                    float al = Mathf.Clamp01((q.life - a) / 0.25f);
                    var dir = Unit(q.pos - tu());
                    // khung va chạm vẽ cho tia tới từ TRÁI: tia bay sang trái thì lật; xoay theo độ dốc của tia
                    bool flip = dir.x < 0;
                    float ang = flip ? Mathf.Atan2(dir.y, -dir.x) * Mathf.Rad2Deg : Mathf.Atan2(-dir.y, dir.x) * Mathf.Rad2Deg;
                    DrawFb(buf, aT, dT, a * dT.fps, q.pos, hT * lon, q.group, layer + 3, ang * 0.5f, flip, k.tint, al);
                };
                Add(pt);
            });

            // thân tia: các đoạn trôi từ miệng tới đích. Lúc phóng, đoạn rải dọc từ miệng tới đầu tia đang vươn (đầu tia phình 1,25 lần).
            var aD = FbArt(k.doan);
            int seq = 0;
            void ThaDoan(float s0, bool dauTia)
            {
                int id = seq++;
                float ph = U(0, dDoan.n);
                float lech = U(0, 6.2832f);
                var p = new P { group = group, life = 3 };
                float s = s0;
                p.upd = (q, dt, L) =>
                {
                    s += vChay * dt;
                    var a = tu();
                    var d = toi() - a;
                    float len = d.magnitude;
                    if (s >= len + 0.1f * lDoan) q.dead = true;
                    q.pos = a + Unit(d) * Mathf.Min(s, len);
                    q.ph = len;
                };
                p.draw = (q, kk, buf) =>
                {
                    var a = tu();
                    var dir = Unit(toi() - a);
                    float len = q.ph > 0 ? q.ph : (toi() - a).magnitude;
                    // gần miệng nhỏ lại (nối êm vào cầu đầu nòng), gần đích mờ dần (chui vào bông trúng)
                    float f = Mathf.Clamp01(s / Mathf.Max(1, len));
                    float tuoiT = T - t0 - tTu;
                    float dayNhip = 1 + 0.09f * Mathf.Sin(tuoiT * 50 + s * 0.02f);   // phập phồng ~8 lần / giây, sóng chạy dọc tia
                    // gốc tia THON rồi phình (người dùng 2026-11-19: "đầu tia nước kiểu như cắt ngang cụt … sửa thành từ 1 tia nhỏ phình ra to"):
                    // trong 2,4 bề dày đầu tính từ miệng, đoạn nhỏ từ 0,2 lên đủ cỡ
                    float goc = Mathf.Lerp(0.2f, 1f, SmoothStep(0, 1, s / Mathf.Max(1, 2.4f * day)));
                    float co = goc * dayNhip * (dauTia ? 1.25f : 1f);
                    float al = Mathf.Clamp01((1 - f) / 0.1f + 0.15f) * Mathf.Clamp01(q.age / 0.03f);
                    var n = new Vector2(-dir.y, dir.x);
                    // đoạn gần miệng đẩy tới trước nửa chiều dài (theo cỡ đang thu) để đuôi thon nằm đúng ở miệng, không thò ngược ra sau
                    float lui = Mathf.Max(0, 0.45f * lDoan * co - s);
                    var pos = q.pos + dir * lui + n * (0.07f * day * goc * Mathf.Sin(tuoiT * 23 + lech + s * 0.03f));     // gợn ngang
                    bool flip = dir.x < 0;
                    float ang = flip ? Mathf.Atan2(dir.y, -dir.x) * Mathf.Rad2Deg : Mathf.Atan2(-dir.y, dir.x) * Mathf.Rad2Deg;
                    DrawFb(buf, aD, dDoan, ph + q.age * dDoan.fps * 1.3f, pos, hDoan * co, q.group, layer + 0.0005f * (id % 400), ang,
                        flip, k.tint, al);
                };
                Add(p);
            }

            if (!coDoan) return tCham;
            // phóng: đầu tia vươn tới đích, rải đoạn dọc đường đã vươn
            At(tTu, () =>
            {
                float daiNay = (toi() - tu()).magnitude;
                int nVuon = Mathf.Max(2, Mathf.CeilToInt(daiNay / buoc));
                for (int i = 0; i < nVuon; i++)
                {
                    float sI = i * buoc;
                    At(tVuon * i / nVuon, () => ThaDoan(sI, false));
                }
                At(0, () => ThaDoan(0, true));
            });
            // dội: nhả đoạn đều từ miệng theo quãng (đoạn chồng 2/3)
            Every(tTu, tCham + tBan, vChay / buoc, x => ThaDoan(0, false));
            return tCham;
        }
    }
}
