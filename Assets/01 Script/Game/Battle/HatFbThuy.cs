// KHUNG VẼ SẴN cho bộ Thủy (2026-11-19). Người dùng duyệt bộ khung 24 khung ("ổn hơn rồi đấy, cho vào game đi"): nước toé từ đất
// (nuoc_toe), sóng cuộn đổ (song_nuoc), nước trúng đích (trung_nuoc), cầu nước có dải bọt xoay (cau_nuoc). File này gom các hàm dùng
// chung của bộ Thủy để thay phần thân chính của toé / trúng / cầu / sóng (dựng bằng hạt có viền mực) bằng khung vẽ sẵn (HatFlip.cs).
// Thân tia nước liền, lá nước ôm thân, vòi rồng, con sóng thần, cột phun (mảng HatMang có va chạm) giữ nguyên.
// Chưa nhập khung, hoặc bảng nước của tướng không phải lam / ngọc lam (mực tím của bạch tuộc so_ngoc, lục của tướng Mộc lỡ rơi vào hàm
// nước): giữ hạt cũ, vì nhân màu (Image.color) không đổi được khung lam ra tím / lục.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // khung nước dùng được cho bảng nước đang phát (wth): đã nhập khung và màu giữa của bảng là lam / ngọc lam (lục > đỏ, lam > đỏ)
        bool FbNuoc(string fx)
        {
            var m = W[2];
            return m.g > m.r && m.b > m.r && HasFb(fx);
        }

        // màu nhân cho khung nước: khung đã tô bảng lam chung (lam đậm #1D5FD2 → ngọc lam #45DFD0, bọt trắng). Tướng có sắc nước lệch hẳn
        // bảng chung (sắc màu giữa lệch > 15 độ, ví dụ ngọc bích của Hải Long) thì nhân nhẹ về sắc đó; còn lại giữ nguyên màu khung đã duyệt
        Color FbNuocTint()
        {
            var m = W[2];
            var d = WDefault.w[2];
            Color.RGBToHSV(m, out float h1, out _, out _);
            Color.RGBToHSV(d, out float h0, out _, out _);
            float dh = Mathf.Abs(h1 - h0);
            if (Mathf.Min(dh, 1 - dh) * 360 <= 15) return Color.white;
            var r = new Color(Mathf.Min(1, m.r / Mathf.Max(0.01f, d.r)), Mathf.Min(1, m.g / Mathf.Max(0.01f, d.g)), Mathf.Min(1, m.b / Mathf.Max(0.01f, d.b)), 1);
            return Color.Lerp(Color.white, r, 0.5f);
        }

        // góc và lật cho khung vẽ hướng sang PHẢI (trung_nuoc: tia tới từ TRÁI) khi nước bay theo dir (toạ độ sân, y xuống): bay sang trái
        // thì lật thay vì lộn ngược (như FbFly); nghiêng tối đa maxAng độ cho nước rơi chéo (mũi thương, cột phun) không dựng đứng cả bông
        static float FbAngThuy(Vector2 dir, float maxAng, out bool flip)
        {
            dir = Unit(dir);
            flip = dir.x < 0;
            float ang = flip ? Mathf.Atan2(dir.y, -dir.x) * Mathf.Rad2Deg : Mathf.Atan2(-dir.y, dir.x) * Mathf.Rad2Deg;
            return Mathf.Clamp(ang, -maxAng, maxAng);
        }

        // nước trúng đích bằng khung vẽ sẵn (khung vẽ sẵn 2026-11-19, thay chớp sao kem + khối nước có viền mực của KrHit): tâm c ở thân
        // (không ở đầu), khung cao h; dir: hướng nước bay tới (null: lật ngẫu nhiên). start 2 = vào ngay khung chớp sao (khung 0, 1 còn bé).
        // Tốc 1,3: một lượt ~0,7 s, đỉnh bông toé ở ~0,2 s rồi vỡ thành giọt, tan
        P TrungNuoc(Vector2 c, float h, Vector2? dir, int group = Front, float layer = 44, float speed = 1.3f, float alpha = 0.94f, float maxAng = 35)
        {
            if (NS) return NTrung(c, h, dir, group); // bộ nước shader (2026-11-24)
            bool flip;
            float ang = 0;
            if (dir.HasValue) ang = FbAngThuy(dir.Value, maxAng, out flip);
            else flip = U(0, 1) < 0.5f;
            return Fb("trung_nuoc", c, h, group, layer, speed, ang, flip, FbNuocTint(), alpha, -1, 2);
        }

        // vương miện nước toé từ đất bằng khung vẽ sẵn (thay mão kr_mao + vành giọt + giọt sụp): chân ở feet, khung cao h. start 2: bỏ hai
        // khung đầu còn bé tí cho cú toé bật ngay
        P ToeNuoc(Vector2 feet, float h, float speed = 1.5f, int group = Front, float layer = 34, float alpha = 1)
        {
            if (NS) return NToe(feet, h, group); // bộ nước shader (2026-11-24)
            const float st = 2;
            var p = Fb("nuoc_toe", feet, h, group, layer, speed, 0, U(0, 1) < 0.5f, FbNuocTint(), alpha, -1, st);
            if (p == null) return null;
            // đáy hình trong khung nhích lên dần (đo trên ảnh: khung 0–5 đáy ở 0,99 cao khung, 6–11 ở 0,94, 12–17 ở ~0,91, 18–23 ở 0,86): dời
            // điểm neo xuống theo khung để chân vũng nước luôn bám mặt đất, không lơ lửng
            float fps = Fbs["nuoc_toe"].fps * speed;
            p.upd = (q, dt, s) =>
            {
                float f = st + q.age * fps;
                q.pos = feet + new Vector2(0, h * (0.05f * SmoothStep(5, 7, f) + 0.035f * SmoothStep(11, 13, f) + 0.045f * SmoothStep(16.5f, 18.5f, f)));
            };
            return p;
        }

        // sóng cuộn đổ bằng khung vẽ sẵn song_nuoc (khung vẽ đổ sang PHẢI; flip = đổ sang trái): chân ở feet, khung cao h, bắt đầu từ khung
        // start. Đáy bọt tràn ở 4 khung cuối nhích lên 0,07 cao khung nên dời neo xuống theo khung (chân sóng bám đất)
        P SongNuoc(Vector2 feet, float h, bool flip, float start, float speed, Color tint, float alpha = 0.86f, int group = Front, float layer = 23.5f)
        {
            var p = Fb("song_nuoc", feet, h, group, layer, speed, 0, flip, tint, alpha, -1, start);
            if (p == null) return null;
            float fps = Fbs["song_nuoc"].fps * speed;
            p.upd = (q, dt, s) => q.pos = feet + new Vector2(0, h * 0.07f * SmoothStep(17, 18.5f, start + q.age * fps));
            return p;
        }

        // vẽ khung cầu nước (điểm neo ở tâm) có giãn theo hướng bay: khung floor(f) đặc, khung kế chồng mờ theo phần lẻ (như DrawFb); stretch
        // giãn bề ngang khung theo góc ang (cầu đang bay dài ra, nén trước lúc nhả)
        void VeCauNuocFb(List<Item> buf, Sprite[] art, FbDef d, float f, Vector2 c, float h, float stretch, int g, float layer, float ang, Color col,
            float a)
        {
            if (a < 0.02f) return;
            int n = d.n;
            f %= n;
            if (f < 0) f += n;
            int i = (int)f;
            float u = f - i;
            Put(buf, g, layer, art[i], col, c, h, d.aspect * stretch, ang, a);
            if (u > 0.02f) Put(buf, g, layer + 0.001f, art[(i + 1) % n], col, c, h, d.aspect * stretch, ang, a * u);
        }

        // LỐC NƯỚC bằng khung vẽ sẵn "loc_nuoc" (lặp; khung vẽ sẵn 2026-11-19, người dùng chê vòi rồng mảng cũ "màu hơi trầm và chưa hợp"):
        // phễu hẹp ở đất nở lên trên, dải xoắn lam / ngọc lam / bọt trắng. Chân và cao đổi theo tuổi: chan(t), cao(t), t = giây từ lúc phát
        // (lốc lướt tới, phễu dâng lên). gian: giãn ngang (phễu khung thon hơn vòi mảng cũ, giãn để ôm được thân đối thủ); hiện dần fadeIn,
        // tắt dần fadeOut cuối đời; lắc nghiêng nhẹ ±lac độ quanh chân. Giữ màu khung đã duyệt (không nhân màu: bản cũ bị chê trầm).
        // Trả null khi chưa nhập khung (hàm gọi về đường cũ). fx: "loc_nuoc" (phễu thon ở gốc, cho lốc đang lướt tới) hoặc "loc_nuoc_bao"
        // (2026-11-19: lốc TRÙM, cột xoáy dày, gốc gần rộng bằng miệng, cho lốc bao quanh đối thủ)
        P LocNuocFb(Func<float, Vector2> chan, Func<float, float> cao, float life, int group, float layer, float alpha = 1, bool flip = false,
            float phase = 0, float speed = 1.15f, float gian = 1.25f, float fadeIn = 0.12f, float fadeOut = 0.35f, float lac = 3, string fx = "loc_nuoc")
        {
            var art = FbArt(fx);
            if (art == null) return null;
            var d = Fbs[fx];
            float fps = d.fps * Mathf.Max(0.05f, speed), ph0 = U(0, 6.28f);
            var p = new P { pos = chan(0), group = group, life = Mathf.Max(0.05f, life) };
            p.upd = (q, dt, s) => q.pos = chan(q.age);
            p.draw = (q, k, buf) =>
            {
                float h = cao(q.age);
                if (h < 2) return;
                float a = alpha * Mathf.Min(1, q.age / Mathf.Max(0.01f, fadeIn)) * Mathf.Clamp01((q.life - q.age) / Mathf.Max(0.01f, fadeOut));
                VeFbGian(buf, art, d, phase + q.age * fps, q.pos, h, gian, q.group, layer, lac * Mathf.Sin(q.age * 3.1f + ph0), flip, Color.white, a);
            };
            return Add(p);
        }

        // lốc nước bao quanh đối thủ: hai lớp lệch pha, lớp SAU tướng đặc (mặt sau phễu), lớp TRƯỚC tướng lật ngang (mặt trước xoáy ngược
        // chiều mặt sau khi nhìn chiếu) và trong mờ aTruoc nên vẫn thấy con bị trúng ở trong; lớp trước to hơn 4 % cho ôm ra ngoài lớp sau
        bool LocNuocBao(Func<float, Vector2> chan, Func<float, float> cao, float life, float aTruoc = 0.5f, float speed = 1.15f, float gian = 1.25f,
            float fadeIn = 0.12f, float fadeOut = 0.35f, float layer = 18, string fx = "loc_nuoc")
        {
            if (LocNuocFb(chan, cao, life, Back, layer, 1, false, 0, speed, gian, fadeIn, fadeOut, 3, fx) == null) return false;
            LocNuocFb(chan, t => 1.04f * cao(t), life, Front, layer, aTruoc, true, 12, speed, gian, fadeIn, fadeOut, 3, fx);
            return true;
        }

        // lốc TRÙM "loc_nuoc_bao" (2026-11-19, người dùng: "lốc xoáy làm to lên cho che hết tướng địch"): đo bề ngang khung theo chiều cao:
        // vòng chân 0,82–0,9 bề ngang khung ở 5–10 % cao, cột 0,65–0,69 ở 20–50 %, miệng 0,8–0,87 ở 55–85 %. Cao 1,65 tH, giãn ngang 1,25
        // nên ngang thân ≥ 1,3 tH, miệng ~1,7 tH; chân khung hạ 0,04 cao khung (vòng nước ngang / dưới chân đối thủ một chút). Cao chặn để
        // phần đặc (90 % khung, lớp trước to hơn 4 %) không vượt mép trên sân (y 24), tối thiểu 1,3 tH
        const float LocBaoGian = 1.25f, LocBaoHa = 0.04f;

        static float LocBaoCao(float feetY, float tH, float muc = 1.65f) => Mathf.Clamp((feetY - 24) / ((0.9f - LocBaoHa) * 1.04f), 1.3f * tH, muc * tH);

        // vẽ khung f (số thực) có giãn ngang gian quanh điểm neo (như DrawFb: neo theo FbDef, lật, xoay ang quanh neo, khung kế chồng mờ)
        void VeFbGian(List<Item> buf, Sprite[] art, FbDef d, float f, Vector2 pos, float h, float gian, int g, float layer, float ang, bool flip,
            Color col, float a)
        {
            if (a < 0.02f) return;
            int n = d.n, i;
            float u;
            if (d.loop)
            {
                f %= n;
                if (f < 0) f += n;
                i = (int)f;
                u = f - i;
            }
            else if (f >= n - 1)
            {
                i = n - 1;
                u = 0;
            }
            else
            {
                i = Mathf.Max(0, (int)f);
                u = Mathf.Clamp01(f - i);
            }
            float asp = d.aspect * gian, w = h * asp;
            float ox = (0.5f - d.px) * w, oy = (0.5f - d.py) * h;
            if (flip) ox = -ox;
            float r = ang * Mathf.Deg2Rad, c = Mathf.Cos(r), s = Mathf.Sin(r);
            var center = pos + new Vector2(ox * c - oy * s, -(ox * s + oy * c));
            Put(buf, g, layer, art[i], col, center, h, asp, ang, a, 0, flip);
            if (u > 0.02f)
            {
                int j = d.loop ? (i + 1) % n : Mathf.Min(n - 1, i + 1);
                Put(buf, g, layer + 0.001f, art[j], col, center, h, asp, ang, a * u, 0, flip);
            }
        }

        // TIA NƯỚC VẼ SẴN (2026-11-19, thử ở Tí Tách rồi áp cho mọi tia nước n_tia của tướng Thủy bảng lam / ngọc lam, mana và chiêu cuối;
        // người dùng: "các tia năng lượng/nước như này nhìn vẫn chưa đã"):
        // thân tia mảng liền + cầu tụ + lá ôm thân + bông trúng của NTia thay bằng TiaFb(DaTiaNuoc): đoạn tia nước lam / ngọc lam có sợi bọt
        // xoắn trôi liên tục, đầu nòng là cầu nước cau_nuoc, bông va chạm tia_nuoc_trung lặp (vương miện nước toé ngược). day: bề dày thân tia.
        // Hợp đồng thời gian giữ như NTia: chạm lúc tHit = T0 + quãng / 1250 (tTu = tHit − thời gian đầu tia vươn của TiaFb), nhả tới T1 =
        // T0 + dur (tBan = T1 − tHit; HoldNuoc("n_tia") không đổi), nhịp đập mỗi 0,24 s (NuocPulse, rung, vòng sóng, mão nuoc_toe dưới chân
        // ở nhịp chẵn). Giữ vệt xoắn ốc tụ vào đầu nòng, giọt rơi khỏi dòng, khối văng + chùm giọt bắn ngược ở chỗ trúng (bớt: 4 + 4/s vì bông
        // khung đã lớn), giọt ở miệng lúc tắt, toé cuối Splash khi đoạn tia cuối tới đích, vệt ướt.
        // Riêng tướng (2026-11-19, NTiaNuoc): goc(t) = gốc tia theo giây từ lúc gọi (điểm rig đo sẵn: giữa mồm, đầu trượng, giữa hai sừng;
        // null = chỗ bắn của rig + 14 theo hướng tia như cũ), tia và cầu đầu nòng bám theo nó từng khung; nongK / trungK nhân cỡ cầu đầu nòng /
        // bông trúng (nongK = 0: không cầu); ngay = true: không tụ, tia phóng NGAY ở khung nhả của clip (T0), chạm sau thời gian đầu tia vươn
        // (0,07–0,14 s) và trả giờ chạm mới, các nhịp đập dời theo
        float NTiaKhung(Vector2 mouth, Vector2 target, Vector2 foeFeet, float casterGround, float tH, float lead, float dur, float day,
            Func<float, Vector2> goc = null, float nongK = 1, float trungK = 1, bool ngay = false)
        {
            float T0c = Mathf.Max(0.14f, lead);
            var g0 = goc != null ? goc(T0c) : mouth; // gốc tia lúc nhả
            var dd = target - g0;
            float d0 = dd.magnitude;
            var u = dd / Mathf.Max(1, d0);
            var nrm = new Vector2(-u.y, u.x);
            var back = -u;
            var src = goc != null ? g0 : mouth + u * 14;
            float rf = Mathf.Clamp(d0 - 70, 0, 0.24f * tH);
            var hitP = target - u * rf; // mặt trước thân đối thủ (như NTia)
            float dist = Mathf.Max(20, Vector2.Dot(hitP - src, u));
            float T0 = Mathf.Max(0.14f, lead), T1 = T0 + dur;
            // 2026-11-19 (mọi tia nước dùng tia vẽ sẵn): tia chiêu cuối (dur > 1) toé cuối 0,9 thay 0,8; tia dày hơn tia mana chuẩn (~36) thì mão,
            // vòng sóng, toé cuối, vệt ướt, rung đầu to theo kh (chiêu cuối 0,28 casterH ~1,2; Thôn Kình 0,33 casterH ~1,35)
            bool big = dur > 1;
            float kh = Mathf.Clamp(1 + 0.6f * (day / 36 - 1), 1, 1.5f);
            float tHit = T0 + Mathf.Max(0.03f, dist / 1250);
            float dai = (hitP - src).magnitude;
            float tVuon = Mathf.Clamp(dai / 2600f, 0.07f, 0.14f); // như TiaFb
            float tTu = Mathf.Max(0.05f, tHit - tVuon);
            if (ngay) // không tụ: phóng ngay ở khung nhả, chạm sau tVuon
            {
                tTu = T0;
                tHit = T0 + tVuon;
            }
            float tBan = Mathf.Max(0.2f, T1 - tHit);
            float vChay = Mathf.Max(380, dai / 0.32f);           // như TiaFb: đoạn cuối bay nốt tới đích
            float tCut = T1 + dai / vChay;
            float start = T;
            Func<float, Vector2> gocT = goc ?? (t => src);
            if (!ngay) Gather(gocT, 0, tTu - 0.03f, 62 * Mathf.Sqrt(day / 19), 70);
            if (NS) // bộ nước shader, bản 3 (2026-11-25, HatNuocGoi.cs): tia kiểu Water Laser của gói mẫu, cùng hợp đồng giờ (bản 2: NTiaShader)
                NLaser(goc != null ? (Func<Vector2>)(() => goc(T - start)) : () => src, () => hitP, day, tTu, tBan, Front, nongK, trungK, casterGround,
                    foeFeet.y);
            else if (goc != null) TiaFb(DaTiaNuoc, () => goc(T - start), () => hitP, day, tTu, tBan, Front, 36, null, nongK, trungK);
            else TiaFb(DaTiaNuoc, src, hitP, day, tTu, tBan, Front, 36, null, nongK, trungK);
            AtW(tTu, () => Shake?.Invoke(0.2f));
            // giọt rơi khỏi mép dòng: chùm hai giọt lệch cỡ (bản 3 shader: tia Water Laser tự bắn giọt + toé, bỏ các lớp cũ trùng việc)
            if (!NS) EveryW(tTu + 0.05f, T1, 6, x =>
            {
                float sd = U(0, 1) < 0.5f ? -1 : 1, xx = dist * U(0.15f, 0.85f);
                float gy = casterGround + (foeFeet.y - casterGround) * (xx / dist) + U(0, 24);
                for (int i = 0; i < 2; i++)
                    Drop(src + u * (xx + i * 6) + nrm * sd * 0.45f * day, u * U(80, 200) + nrm * sd * U(50, 150) + new Vector2(0, -50), 0,
                        U(2, 3.4f) * (i == 0 ? 1.1f : 0.75f), 900, Front, gy);
            });
            // chỗ trúng: khối nước tạt ngang theo thân, chùm giọt bắn ngược về phía người bắn
            if (!NS) EveryW(tHit, tCut, 4, x =>
            {
                float sd = U(0, 1) < 0.5f ? -1 : 1;
                Khoi(hitP + nrm * sd * U(0.2f, 0.5f) * day, nrm * sd * U(170, 290) + back * U(30, 120) + new Vector2(0, -U(20, 90)), U(0.3f, 0.38f),
                    U(5, 7.5f));
            });
            if (!NS) EveryW(tHit, tCut, 4, x =>
            {
                float a = Mathf.Atan2(back.y, back.x) + U(-1.1f, 1.1f);
                int m = U(0, 1) < 0.4f ? 3 : 2;
                bool bk = U(0, 1) < 0.35f;
                for (int i = 0; i < m; i++)
                {
                    float ai = a + U(-0.15f, 0.15f);
                    Drop(hitP + U2(-6, 6), new Vector2(Mathf.Cos(ai), Mathf.Sin(ai) - 0.45f) * U(200, 400) * (1 - 0.18f * i), 0, U(2, 3.6f) * (i == 0 ? 1.15f : 0.8f),
                        900, bk ? Back : Front, foeFeet.y + U(-10, 18));
                }
            });
            // nhịp đập của dòng nước dội vào thân (như NTia): rung, NuocPulse (chớp + giật đối thủ), vòng sóng, mão nuoc_toe ở nhịp chẵn
            int nb = Mathf.Max(1, Mathf.CeilToInt((tCut - tHit) / 0.24f));
            for (int i = 0; i < nb; i++)
            {
                int ii = i;
                AtW(tHit + i * 0.24f, () =>
                {
                    Ripple(foeFeet + new Vector2(0, 2), 0.15f * tH, 0.62f * tH * kh);
                    if ((ii & 1) == 0) Crown(foeFeet + new Vector2(U(-12, 12), 6), 0.5f * tH * kh, 0.5f);
                    Shake?.Invoke((ii == 0 ? 0.3f : 0.08f) * kh);
                    NuocPulse?.Invoke(ii == 0 ? 1 : 0.45f);
                });
            }
            // hết tia: miệng nhỏ giọt; đoạn cuối bay nốt (theo tốc trôi của đoạn TiaFb), rơi giọt dọc đường
            AtW(T1, () =>
            {
                for (int i = 0; i < 4; i++)
                    Drop(gocT(T - start) + U2(-5, 5), new Vector2(U(-50, 50), U(-60, 10)) + u * U(20, 80), 0, U(2.2f, 3.4f), 900, Front, casterGround + U(-6, 10));
            });
            EveryW(T1 + 0.02f, tCut, 14, x =>
            {
                float tl = Mathf.Min(dist, vChay * (T - start - T1));
                Drop(src + u * tl + nrm * U(-0.3f, 0.3f) * day, u * U(100, 220) + new Vector2(0, -U(10, 60)), 0, U(2, 3), 900, Front,
                    casterGround + (foeFeet.y - casterGround) * (tl / dist) + U(0, 24));
            });
            AtW(tCut, () => // đoạn cuối tới đích: vỡ toé, vệt ướt
            {
                Splash(hitP, (big ? 0.9f : 0.8f) * kh, foeFeet.y, tH, Front, u);
                Puddle(foeFeet + new Vector2(0, 3), 22 * kh, 1.5f);
            });
            return tHit;
        }

        // ================= tia / cầu nước riêng từng tướng (2026-11-19) =================
        // Điểm rig đo sẵn trên .atomik (scratchpad fb_thuy_do_rig.py / fb_thuy_bang.py, bộ tính tư thế ArtGen/Spine/mo_xe/atomik_dang.py),
        // phần của chiều cao game, x tới trước, y lên, gốc ở chân. Ra toạ độ sân lấy LỆCH so với chỗ bắn của rig (game.muzzle, StageView truyền
        // vào là `mouth`) nên lệch neo của hình không ảnh hưởng. Dạng (1, 2) phân bằng độ cao chỗ bắn / casterH khi hai dạng khác hẳn.
        //  - Hải Đăng (ca_den): tâm vùng lòng miệng (điểm ảnh đỏ / hồng) ở dáng há: cast (0,12; 0,334) / (0,097; 0,323), skill (0,155; 0,323) /
        //    (0,12; 0,30) cho dạng 1 / 2 → lấy trung bình; chỗ bắn rig (0,347; 0,305) nằm ở mép phải miệng (gốc tia cũ lệch ~0,23 H ra trước).
        //  - Thạch Giải (thach_giai): tâm vùng lòng miệng đỏ: cast dạng 1 (0,16; 0,62), dạng 2 (0,27; 0,895); khung ợ của skill: dạng 1 (−0,02;
        //    0,59), dạng 2 (−0,01; 0,88). Độ há ~0,45 H (môi trên tới mép hàm dưới).
        //  - Giông Bão (giong_bao): xương "cau" (quả cầu đầu trượng) mỗi 0,05 s của clip cast (GbTruong1 / 2; trượng vung từ sau đầu ra trước ở
        //    khung nhả, rung nhẹ lúc giữ).
        //  - Uyên Xà (uyen_xa): trung điểm tâm hai sừng (hình P_ear01, P_ear02) mỗi 0,05 s của clip cast (UxSung, trung bình hai dạng: lệch nhau
        //    ≤ 0,03 H).
        static readonly Vector2 CdMzR = new Vector2(0.347f, 0.305f), CdMieng = new Vector2(0.11f, 0.33f), CdMiengUlt = new Vector2(0.14f, 0.31f);
        static readonly Vector2 TgMzR1 = new Vector2(0.366f, 0.676f), TgMzR2 = new Vector2(0.558f, 0.986f);
        static readonly Vector2 TgMieng1 = new Vector2(0.16f, 0.62f), TgMieng2 = new Vector2(0.27f, 0.895f);
        static readonly Vector2 TgO1 = new Vector2(-0.02f, 0.59f), TgO2 = new Vector2(-0.01f, 0.88f);
        static readonly Vector2 GbMzR1 = new Vector2(0.957f, 0.349f), GbMzR2 = new Vector2(0.821f, 0.553f);
        static readonly Vector2 UxMzR = new Vector2(0.053f, 0.586f);
        static readonly Vector2[] GbTruong1 =
        {
            new Vector2(0.463f, 0.865f), new Vector2(0.122f, 0.962f), new Vector2(-0.108f, 0.956f), new Vector2(-0.192f, 0.913f), new Vector2(-0.219f, 0.910f),
            new Vector2(-0.193f, 0.942f), new Vector2(-0.139f, 0.977f), new Vector2(-0.102f, 0.996f), new Vector2(-0.115f, 0.995f), new Vector2(-0.197f, 0.960f),
            new Vector2(0.516f, 0.964f), new Vector2(0.950f, 0.345f), new Vector2(0.930f, 0.347f), new Vector2(0.928f, 0.364f), new Vector2(0.931f, 0.377f),
            new Vector2(0.933f, 0.409f), new Vector2(0.933f, 0.376f), new Vector2(0.934f, 0.392f), new Vector2(0.935f, 0.409f), new Vector2(0.935f, 0.376f),
            new Vector2(0.936f, 0.409f), new Vector2(0.936f, 0.393f), new Vector2(0.936f, 0.378f), new Vector2(0.936f, 0.411f), new Vector2(0.936f, 0.379f),
            new Vector2(0.937f, 0.395f), new Vector2(0.937f, 0.412f), new Vector2(0.937f, 0.379f), new Vector2(0.938f, 0.412f), new Vector2(0.938f, 0.395f),
            new Vector2(0.938f, 0.379f), new Vector2(0.929f, 0.451f), new Vector2(0.875f, 0.615f), new Vector2(0.793f, 0.750f), new Vector2(0.694f, 0.826f),
            new Vector2(0.602f, 0.862f), new Vector2(0.522f, 0.872f), new Vector2(0.475f, 0.869f), new Vector2(0.463f, 0.865f), new Vector2(0.463f, 0.865f),
        };
        static readonly Vector2[] GbTruong2 =
        {
            new Vector2(0.287f, 0.865f), new Vector2(0.069f, 0.977f), new Vector2(-0.175f, 1.011f), new Vector2(-0.238f, 0.987f), new Vector2(-0.282f, 0.974f),
            new Vector2(-0.286f, 0.989f), new Vector2(-0.262f, 1.015f), new Vector2(-0.225f, 1.040f), new Vector2(-0.202f, 1.055f), new Vector2(-0.222f, 1.055f),
            new Vector2(-0.292f, 1.028f), new Vector2(0.153f, 1.119f), new Vector2(0.821f, 0.553f), new Vector2(0.793f, 0.543f), new Vector2(0.783f, 0.569f),
            new Vector2(0.790f, 0.561f), new Vector2(0.795f, 0.608f), new Vector2(0.797f, 0.591f), new Vector2(0.798f, 0.575f), new Vector2(0.799f, 0.606f),
            new Vector2(0.801f, 0.573f), new Vector2(0.802f, 0.589f), new Vector2(0.803f, 0.605f), new Vector2(0.804f, 0.572f), new Vector2(0.805f, 0.604f),
            new Vector2(0.806f, 0.588f), new Vector2(0.806f, 0.572f), new Vector2(0.807f, 0.604f), new Vector2(0.807f, 0.571f), new Vector2(0.808f, 0.587f),
            new Vector2(0.809f, 0.602f), new Vector2(0.809f, 0.570f), new Vector2(0.810f, 0.601f), new Vector2(0.748f, 0.706f), new Vector2(0.660f, 0.819f),
            new Vector2(0.568f, 0.893f), new Vector2(0.479f, 0.926f), new Vector2(0.404f, 0.930f), new Vector2(0.346f, 0.917f), new Vector2(0.306f, 0.892f),
            new Vector2(0.289f, 0.869f), new Vector2(0.287f, 0.865f),
        };
        static readonly Vector2[] UxSung =
        {
            new Vector2(0.028f, 0.839f), new Vector2(0.013f, 0.837f), new Vector2(-0.021f, 0.833f), new Vector2(-0.063f, 0.825f), new Vector2(-0.103f, 0.817f),
            new Vector2(-0.128f, 0.811f), new Vector2(-0.139f, 0.808f), new Vector2(-0.151f, 0.803f), new Vector2(-0.060f, 0.812f), new Vector2(0.136f, 0.824f),
            new Vector2(0.208f, 0.820f), new Vector2(0.219f, 0.817f), new Vector2(0.215f, 0.818f), new Vector2(0.211f, 0.819f), new Vector2(0.209f, 0.819f),
            new Vector2(0.206f, 0.819f), new Vector2(0.203f, 0.821f), new Vector2(0.197f, 0.822f), new Vector2(0.194f, 0.822f), new Vector2(0.190f, 0.823f),
            new Vector2(0.178f, 0.825f), new Vector2(0.183f, 0.823f), new Vector2(0.174f, 0.826f), new Vector2(0.166f, 0.827f), new Vector2(0.175f, 0.825f),
            new Vector2(0.160f, 0.828f), new Vector2(0.156f, 0.829f), new Vector2(0.164f, 0.827f), new Vector2(0.152f, 0.829f), new Vector2(0.151f, 0.829f),
            new Vector2(0.140f, 0.830f), new Vector2(0.121f, 0.832f), new Vector2(0.100f, 0.833f), new Vector2(0.077f, 0.836f), new Vector2(0.087f, 0.839f),
            new Vector2(0.054f, 0.841f), new Vector2(0.031f, 0.841f),
        };

        // điểm bảng (mỗi 0,05 s từ đầu clip) ở giây t, nội suy thẳng; quá cuối bảng giữ điểm cuối
        static Vector2 DiemBang(Vector2[] b, float t)
        {
            float f = Mathf.Max(0, t) / 0.05f;
            int i = Mathf.Min(b.Length - 1, (int)f);
            return i >= b.Length - 1 ? b[b.Length - 1] : Vector2.Lerp(b[i], b[i + 1], f - i);
        }

        // id tướng của bảng nước đang phát (WThemes là bảng theo id; null: bảng chung)
        string WId()
        {
            foreach (var kv in WThemes)
                if (kv.Value == wth) return kv.Key;
            return null;
        }

        // tia nước n_tia theo tướng: bề dày theo thân người bắn (mana 0,22 casterH, chiêu cuối 0,28, chiêu cuối Thôn Kình 2,2 × tiaTo), tia vẽ sẵn
        // (NTiaKhung) khi có khung; riêng từng tướng:
        //  - Hải Đăng (người dùng: "không cần tụ cầu nước ở trước mặt, khi nào há mồm thì bắn tia nước, chỉnh lại tia nước cho đúng giữa mồm và
        //    scale tia nước to lên"): gốc = tâm lòng miệng đo trên rig, không cầu đầu nòng, không tụ, phóng ngay ở khung há; bề dày 0,3 casterH
        //    (mana) / 0,36 (chiêu cuối)
        //  - Thạch Giải mana ("làm tia nước to lên nữa ... cho to bằng mồm luôn"): gốc = tâm lòng miệng theo dạng, bề dày 0,48 casterH (≈ độ há
        //    ~0,45 H), cầu đầu nòng 0,55 lần (≈ cỡ miệng), bông trúng 0,6 lần (không trùm kín con bị trúng suốt lúc tia dội)
        //  - Giông Bão mana ("cầu nước phải đi theo phần trượng của phù thủy chứ không đứng im 1 chỗ"): gốc + cầu đầu nòng bám quả cầu đầu
        //    trượng theo bảng rig từng khung (cầu đầu nòng 0,75 lần)
        //  - Uyên Xà mana ("cầu nước tụ phải ở giữa 2 sừng không phải ở mồm"): gốc + cầu đầu nòng ở trung điểm hai sừng theo bảng rig từng khung
        //    (cầu đầu nòng 0,8 lần)
        float NTiaNuoc(bool ult, Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            float dur = ult ? 1.25f : 0.88f;
            float hwTo = ult && wth.tiaTo > 0 ? Mathf.Clamp(wth.tiaTo * casterH, 22, 29) : 0;
            float day = !ult ? Mathf.Clamp(0.22f * casterH, 26, 44) : wth.tiaTo > 0 ? Mathf.Clamp(2.2f * wth.tiaTo * casterH, 44, 68) : Mathf.Clamp(0.28f * casterH, 34, 56);
            if (!(HasTia(DaTiaNuoc) && FbNuoc("tia_nuoc_doan"))) return NTia(mouth, foeBody, foeFeet, casterFeet.y, tH, lead, dur, hwTo);
            float dir = foeFeet.x < casterFeet.x ? -1 : 1, H = Mathf.Max(1, casterH);
            float mzY = (casterFeet.y - mouth.y) / H; // độ cao chỗ bắn của rig / thân: phân dạng
            Vector2 Lech(Vector2 diem, Vector2 mz) => mouth + new Vector2(dir * (diem.x - mz.x) * H, -(diem.y - mz.y) * H);
            switch (WId())
            {
                case "ca_den":
                {
                    var g = Lech(ult ? CdMiengUlt : CdMieng, CdMzR);
                    return NTiaKhung(mouth, foeBody, foeFeet, casterFeet.y, tH, lead, dur, Mathf.Clamp((ult ? 0.36f : 0.3f) * casterH, 40, 80), t => g, 0, 1, true);
                }
                case "thach_giai" when !ult:
                {
                    bool d2 = mzY > 0.83f;
                    var g = Lech(d2 ? TgMieng2 : TgMieng1, d2 ? TgMzR2 : TgMzR1);
                    return NTiaKhung(mouth, foeBody, foeFeet, casterFeet.y, tH, lead, dur, Mathf.Clamp(0.48f * casterH, 60, 110), t => g, 0.55f, 0.6f);
                }
                case "giong_bao" when !ult:
                {
                    bool d2 = mzY > 0.45f;
                    var b = d2 ? GbTruong2 : GbTruong1;
                    var mz = d2 ? GbMzR2 : GbMzR1;
                    return NTiaKhung(mouth, foeBody, foeFeet, casterFeet.y, tH, lead, dur, day, t => Lech(DiemBang(b, t), mz), 0.75f);
                }
                case "uyen_xa" when !ult:
                    return NTiaKhung(mouth, foeBody, foeFeet, casterFeet.y, tH, lead, dur, day, t => Lech(DiemBang(UxSung, t), UxMzR), 0.8f);
            }
            return NTiaKhung(mouth, foeBody, foeFeet, casterFeet.y, tH, lead, dur, day);
        }

        // cầu nước n_cau theo tướng: Thạch Giải ("không cần làm animation tụ nước vì nó ợ từ trong bụng ra, khi nào nó ợ thì bắn cầu nước từ mồm
        // ra, làm cầu nước to hơn"): không tụ, đúng khung ợ cầu hiện ở giữa mồm (tâm lòng miệng đo trên rig ở khung ợ, theo dạng) rồi bay luôn,
        // cầu × 1,6. Tướng khác như cũ
        float NCauNuoc(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (WId() == "thach_giai")
            {
                float dir = foeFeet.x < casterFeet.x ? -1 : 1, H = Mathf.Max(1, casterH);
                bool d2 = (casterFeet.y - mouth.y) / H > 0.83f;
                var o = d2 ? TgO2 : TgO1;
                var mz = d2 ? TgMzR2 : TgMzR1;
                var g = mouth + new Vector2(dir * (o.x - mz.x) * H, -(o.y - mz.y) * H);
                return NCau(g, foeBody, casterFeet.y, foeFeet, tH, lead, 1.6f, true);
            }
            return NCau(mouth, foeBody, casterFeet.y, foeFeet, tH, lead);
        }

        // ================= bão của chiêu cuối Hải Long (2026-11-19) =================
        // Người dùng: "chiêu cuối con này chưa epic, thêm nhiều lốc xoáy và sét đánh vào". Gọi thêm trong NVoi (dạng 3), NXoay (dạng 2), NSong
        // (dạng 1) khi bảng nước là của hai_long, không đổi giờ chạm / nhịp / giờ trả về của chiêu:
        //  - soLoc cột lốc nước phụ (loc_nuoc, cao 1,1–1,4 tH) mọc lệch giờ 0,12 s quanh đối thủ (hai bên, sau lưng, chếch trước), mỗi cột kèm
        //    nuoc_toe ở chân, trôi lắc nhẹ, dâng 0,22 s và tắt dần cuối bão; cột sau lưng đối thủ ở lớp sau tướng, cột chếch trước mờ 0,8;
        //  - soSet phát sét set_danh (neo chỗ chạm đất, một lượt ~0,7 s): phát CHÍNH đánh xuyên đầu đối thủ đúng nhịp trúng lớn tChinh, một phát
        //    nữa cũng vào đối thủ, còn lại quanh sân / chân các cột lốc; mỗi phát chớp màn trắng nhạt, rung 0,3–0,5, bông trung_trang ở chỗ
        //    trúng; phát vào đối thủ thêm NuocPulse (chớp + giật).
        void HaiLongBao(Vector2 foeFeet, float tH, float t0, float t1, float tChinh, int soLoc, int soSet)
        {
            if (WId() != "hai_long") return;
            Vector2[] cho = { new Vector2(-1.05f, -0.12f), new Vector2(1.0f, -0.1f), new Vector2(0.35f, -0.36f), new Vector2(-0.55f, 0.28f) };
            Vector2 Cho(int i)
            {
                var p = foeFeet + cho[i % cho.Length] * tH;
                p.x = Mathf.Clamp(p.x, 24, 536);
                return p;
            }
            if (FbNuoc("loc_nuoc"))
                for (int i = 0; i < Mathf.Min(soLoc, cho.Length); i++)
                {
                    float ti = t0 + 0.12f * i + U(0, 0.06f), life = Mathf.Max(0.5f, t1 - ti), h = U(1.1f, 1.4f) * tH, A = 0.08f * tH, ph = U(0, 6.28f);
                    var p0 = Cho(i);
                    bool sau = cho[i].y < 0;
                    AtW(ti, () =>
                    {
                        LocNuocFb(t => p0 + new Vector2(A * Mathf.Sin(t * 1.6f + ph), 0.25f * A * Mathf.Cos(t * 1.3f + ph)),
                            t => h * (0.15f + 0.85f * EaseOut(t / 0.22f)) * (1 - 0.3f * SmoothStep(life - 0.35f, life, t)), life, sau ? Back : Front,
                            sau ? 16 : 19, sau ? 1 : 0.8f, U(0, 1) < 0.5f, U(0, 24), 1.3f, 1.15f, 0.15f, 0.35f, 4);
                        ToeNuoc(p0 + new Vector2(0, 2), 0.7f * tH, 1.5f, sau ? Back : Front, sau ? 17 : 20, 0.85f);
                    });
                }
            if (!HasFb("set_danh")) return;
            for (int k = 0; k < soSet; k++)
            {
                bool chinh = k == 0, vaoDich = k <= 1;
                // phát chính đúng nhịp trúng lớn; các phát khác rải đều trong bão, tránh trùng phát chính
                float tk = chinh ? tChinh : Mathf.Lerp(t0 + 0.12f, t1 - 0.25f, (k - 1 + 0.5f + U(-0.25f, 0.25f)) / Mathf.Max(1, soSet - 1));
                if (!chinh && Mathf.Abs(tk - tChinh) < 0.12f) tk += 0.14f;
                Vector2 cham;
                if (vaoDich) cham = foeFeet + new Vector2(chinh ? 0 : U(-0.12f, 0.12f) * tH, 3);
                else if (k - 2 < soLoc && U(0, 1) < 0.6f) cham = Cho(k - 2) + new Vector2(U(-0.1f, 0.1f) * tH, 2); // chân một cột lốc
                else cham = foeFeet + new Vector2((U(0, 1) < 0.5f ? -1 : 1) * U(0.45f, 1.25f) * tH, U(-0.3f, 0.3f) * tH);
                cham.x = Mathf.Clamp(cham.x, 24, 536);
                float hs = (chinh ? 1.9f : U(1.45f, 1.75f)) * tH;
                int g = vaoDich || cham.y >= foeFeet.y ? Front : Back;
                AtW(Mathf.Max(0.02f, tk), () =>
                {
                    Fb("set_danh", cham, hs, g, 42, 1.4f, 0, U(0, 1) < 0.5f, null, 0.95f, -1, 1);
                    FlashScreen?.Invoke(new Color(1, 1, 0.93f, vaoDich ? 0.22f : 0.12f));
                    Shake?.Invoke(chinh ? 0.5f : vaoDich ? 0.4f : 0.3f);
                    if (HasFb("trung_trang"))
                        Fb("trung_trang", vaoDich ? foeFeet + new Vector2(0, -0.55f * tH) : cham + new Vector2(0, -0.08f * hs), (vaoDich ? 0.9f : 0.45f) * tH,
                            g, 44, 1.4f, U(-20, 20), U(0, 1) < 0.5f, null, 0.95f, -1, 1);
                    if (vaoDich) NuocPulse?.Invoke(chinh ? 0.8f : 0.45f);
                });
            }
        }
    }
}
