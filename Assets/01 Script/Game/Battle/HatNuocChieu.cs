// CHIÊU NƯỚC MỚI theo bộ nước gói mẫu (2026-11-25). Người dùng: "dựa trên bộ fx các skill nước, làm thêm các chiêu thức cho các tướng, không
// chỉ xoay quanh kiểu cầu/tia ... có thêm các projectile, mưa, lốc xoáy nước, các kiểu cầu nước"; duyệt bảng đề xuất (mỗi chiêu bám động tác
// clip đang có của tướng, mạnh dần theo ải). Vẽ bằng shader bộ nước bản 3 (HatNuocGoi.cs: NFbPhat, NBall, dải liền) và khối dùng chung
// (GSplash, GTrung, GToe, GCotPhun, CauNuoc → NCauShader); không có lưới shader / bảng nước không lam (NS false) thì về chiêu cũ của tướng.
//  - n_lien_dan  Tí Tách mana "Liên châu thủy đạn": há miệng bắn 5 viên đạn nước liên tiếp (gói: SimpleProjectile + Projectile_Cast), mỗi viên
//                một nhịp trúng nhỏ, viên cuối to toé lớn.
//  - n_bong_nay  Thạch Giải mana "Bong bóng nảy": thổi 3 bong bóng (BongDon) bay vồng, nảy một lần trên đất rồi vỡ ở thân đối thủ (BongVo).
//  - n_cau_nhot  Thạch Giải chiêu cuối "Cầu nhốt": ợ cầu nước bay tới, bung thành bong bóng lớn TRONG MỜ bọc lấy đối thủ (vành + ruột mờ +
//                vệt bọt xoay, thấy đối thủ bên trong), rung hai nhịp rồi vỡ toé.
//  - n_bom       Hải Đăng mana "Bom nước": há miệng phụt cầu nước nặng bay vồng cao (gói: Water_Grenade), vòng gợn co trên đất báo chỗ rơi,
//                chạm chân đối thủ nổ thành toé đất lớn + ba cột nước + mưa giọt.
// Hợp đồng với StageView như mọi chiêu "n_": phát lúc clip bắt đầu kèm lead (giờ trúng của clip), trả giây tới cú trúng chính; nhịp trúng
// phụ gọi NuocPulse (đối thủ chớp + giật); giờ giữ dáng ở HoldNuoc.
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // điểm đo trên rig (phần chiều cao, x tới trước, y lên, gốc ở chân) → toạ độ sân, lệch so với chỗ bắn của rig (như NTiaNuoc)
        static Vector2 LechRig(Vector2 mouth, Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 diem, Vector2 mz)
        {
            float dir = foeFeet.x < casterFeet.x ? -1 : 1, H = Mathf.Max(1, casterH);
            return mouth + new Vector2(dir * (diem.x - mz.x) * H, -(diem.y - mz.y) * H);
        }

        // flipbook phát một ĐOẠN khung f0 → f1 theo đời hạt (lap: lặp qua lại f0 ↔ f1 với fps); at: vị trí theo tuổi; cỡ w0 → w1, hk: cao / rộng
        P NFbDoan(int g, float layer, Func<float, Vector2> at, float life, NFb fb, float f0, float f1, float w0, float w1, float angUi, float cut = 0.3f,
            float lift = 0, int kind = 0, bool flip = false, float hk = 0, bool lap = false, float fps = 14, Func<float, float> wFn = null,
            int pal = 0)
        {
            float sd = NSeed();
            var p = new P { pos = at(0), life = Mathf.Max(0.04f, life), group = g };
            p.draw = (q, k, buf) =>
            {
                q.pos = at(q.age);
                float fr;
                if (lap)
                {
                    float span = Mathf.Max(0.5f, f1 - f0), x = q.age * fps % (2 * span);
                    fr = f0 + (x < span ? x : 2 * span - x);
                }
                else fr = Mathf.Lerp(f0, f1, k);
                float w = wFn != null ? wFn(q.age) : Mathf.Lerp(w0, w1, EaseOut(k));
                float a = k < 0.85f ? 1 : 1 - (k - 0.85f) / 0.15f;
                NFbS(q.group, layer + k * 0.01f, q.pos, w, hk > 0 ? w * hk : 0, angUi, fb, fr, cut, a, sd, lift, kind, flip, pal);
            };
            return Add(p);
        }

        // viên đạn nước bay từ a tới b trong fly giây (vồng nhẹ lên trên theo vong): cầu shader giãn theo hướng bay, đuôi dải thon liền thân,
        // giọt rớt lại phía sau; tới đích gọi onHit
        P NVienDan(Vector2 a, Vector2 b, float fly, float r, float vong, int g, Action onHit)
        {
            float sd = NSeed();
            Vector2 Path(float t)
            {
                float x = Mathf.Clamp01(t / fly);
                return Vector2.Lerp(a, b, x) + new Vector2(0, -4 * vong * x * (1 - x));
            }
            var p = new P { pos = a, life = Mathf.Max(0.04f, fly), group = g };
            float lastDrop = 0;
            p.upd = (q, dt, s) =>
            {
                q.pos = Path(q.age);
                if (q.age - lastDrop > 0.035f)
                {
                    lastDrop = q.age;
                    var d = Unit(Path(q.age) - Path(Mathf.Max(0, q.age - 0.03f)));
                    s.NGiot(q.pos - d * r + s.U2(-2, 2), -d * s.U(40, 110) + new Vector2(0, -s.U(0, 40)), s.U(0.22f, 0.36f) * r, q.group, s.U(0.25f, 0.4f), 650);
                }
            };
            p.draw = (q, k, buf) =>
            {
                var now = Path(q.age);
                float tl = Mathf.Min(q.age, 0.075f);
                var past = Path(q.age - tl);
                var dv = now - past;
                float rr = r * Mathf.Min(1, 0.5f + q.age / 0.05f);
                if (dv.magnitude > 0.5f * rr)
                {
                    nPts.Clear();
                    nHw.Clear();
                    const int M = 8;
                    for (int j = M; j >= 0; j--)
                    {
                        nPts.Add(Path(q.age - tl * j / M));
                        nHw.Add(rr * 0.72f * Mathf.Pow(1 - j / (float)M, 0.85f) + 0.5f);
                    }
                    NStripFlush(q.group, 5.9f, 1.3f, 0.07f, sd);
                }
                NBall(q.group, 6, now, rr, 1, 0, 0.06f, 0.4f, sd, dv.sqrMagnitude > 0.01f ? dv : (Vector2?)null, 1.3f);
            };
            p.onDeath = (q, s) => onHit?.Invoke();
            return Add(p);
        }

        // ================= Tí Tách: Liên châu thủy đạn =================
        public float NLienDan(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NTiaNuoc(false, casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
            float T0 = Mathf.Max(0.12f, lead);
            const int N = 5;
            const float Gap = 0.11f;
            float dir = foeFeet.x < casterFeet.x ? -1 : 1;
            float fly = Mathf.Clamp((foeBody - mouth).magnitude / 1600f, 0.12f, 0.22f);
            float r0 = Mathf.Clamp(0.06f * casterH, 6, 11);
            Gather(t => mouth, 0, T0 - 0.03f, 46, 40);                 // nước tụ nhỏ ở miệng lúc lấy đà
            for (int i = 0; i < N; i++)
            {
                int ii = i;
                bool cuoi = i == N - 1;
                float r = cuoi ? 1.7f * r0 : r0 * U(0.9f, 1.1f);
                var aim = foeBody + new Vector2(-dir * 0.1f * tH + U(-0.1f, 0.1f) * tH, U(-0.16f, 0.1f) * tH);
                AtW(T0 + Gap * i, () =>
                {
                    var u = Unit(aim - mouth);
                    Shake?.Invoke(cuoi ? 0.16f : 0.05f);
                    // phụt ở miệng: toé nhỏ bung chĩa theo hướng bắn (texture dựng lên → xoay theo hướng)
                    NFbPhat(Front, 5.2f, mouth + u * (0.8f * r), u * 30, 0.2f, NFb.ToeGiuaNho, 2.4f * r, 3.4f * r, NAng(u) - 90, 0.3f, 0.12f);
                    NVienDan(mouth + u * (0.6f * r), aim, fly * (cuoi ? 1.1f : 1), r, 0.04f * tH, Front, () =>
                    {
                        if (cuoi)
                        {
                            GSplash(aim, 0.8f, foeFeet.y, tH, Front, u);
                            Puddle(foeFeet + new Vector2(0, 3), 22, 1.3f);
                            Shake?.Invoke(0.32f);
                        }
                        else
                        {
                            GTrung(aim, 0.48f * tH, u, Front);
                            Shake?.Invoke(0.1f);
                        }
                        if (ii > 0) NuocPulse?.Invoke(cuoi ? 0.7f : 0.35f);
                    });
                });
            }
            return T0 + fly;
        }

        // ================= Thạch Giải: Bong bóng nảy / Cầu nhốt =================
        Vector2 TgDiem(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeFeet, bool o)
        {
            bool d2 = (casterFeet.y - mouth.y) / Mathf.Max(1, casterH) > 0.83f;
            var diem = o ? (d2 ? TgO2 : TgO1) : (d2 ? TgMieng2 : TgMieng1);
            return LechRig(mouth, casterFeet, casterH, foeFeet, diem, d2 ? TgMzR2 : TgMzR1);
        }

        public float NBongNay(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NTiaNuoc(false, casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
            float dir = foeFeet.x < casterFeet.x ? -1 : 1;
            var src = TgDiem(casterFeet, casterH, mouth, foeFeet, false);
            float T0 = Mathf.Max(0.15f, lead);
            const float T1 = 0.3f, T2 = 0.24f, Gap = 0.13f;
            // lần chụp đầu 0,1 casterH (12–24) nhỏ như hạt đậu so với cái miệng ~0,45 H của Thạch Giải: bong bóng ~1/3 độ há
            float rB = Mathf.Clamp(0.16f * casterH, 18, 40);
            Gather(t => src, 0, T0 - 0.04f, 60, 45);
            for (int i = 0; i < 3; i++)
            {
                int ii = i;
                float r = rB * (i == 1 ? 1.15f : U(0.82f, 0.95f));
                float f = U(0.48f, 0.6f);
                var nay = new Vector2(Mathf.Lerp(src.x, foeFeet.x, f), Mathf.Lerp(casterFeet.y, foeFeet.y, f) - 0.85f * r);
                var dich = foeBody + new Vector2(-dir * 0.1f * tH + U(-0.1f, 0.1f) * tH, U(-0.15f, 0.08f) * tH);
                AtW(T0 + Gap * i, () =>
                {
                    var u = Unit(nay - src);
                    NFbPhat(Front, 5.2f, src + u * r, u * 30, 0.2f, NFb.ToeGiuaNho, 2f * r, 2.8f * r, NAng(u) - 90, 0.3f, 0.12f);
                    BongBay(src, nay, dich, T1, T2, r, 0.42f * tH, 0.28f * tH, foeFeet.y, () =>
                    {
                        GTrung(dich, 0.45f * tH, new Vector2(dir, 0), Front);
                        Shake?.Invoke(ii == 2 ? 0.25f : 0.1f);
                        if (ii > 0) NuocPulse?.Invoke(ii == 2 ? 0.6f : 0.35f);
                    });
                });
            }
            return T0 + T1 + T2;
        }

        // bong bóng bay vồng a → nay (chạm đất, bẹp + gợn + toé nhỏ) → dich, rồi vỡ (khung vỡ của BongDon + BongVo)
        void BongBay(Vector2 a, Vector2 nay, Vector2 dich, float T1, float T2, float r, float cao1, float cao2, float ground, Action onHit)
        {
            float sd = NSeed();
            Vector2 Pos(float t)
            {
                if (t < T1)
                {
                    float x = t / T1;
                    return Vector2.Lerp(a, nay, x) + new Vector2(0, -4 * cao1 * x * (1 - x));
                }
                float y = Mathf.Clamp01((t - T1) / T2);
                return Vector2.Lerp(nay, dich, y) + new Vector2(0, -4 * cao2 * y * (1 - y));
            }
            var p = new P { pos = a, life = T1 + T2, group = Front };
            p.draw = (q, k, buf) =>
            {
                float t = q.age;
                var c = Pos(t);
                q.pos = c;
                float w = 2.3f * r * Mathf.Min(1, 0.45f + t / 0.08f), h = w;
                float bep = 1 - Mathf.Clamp01(Mathf.Abs(t - T1) / 0.07f);   // bẹp lúc chạm đất
                w *= 1 + 0.28f * bep;
                h *= 1 - 0.25f * bep;
                float fr = t < 0.08f ? Mathf.Lerp(1, 4, t / 0.08f) : 4 + Mathf.PingPong(t * 9, 2);
                var cc = c + new Vector2(0, 0.2f * r * bep);
                // ruột khung có alpha thấp → ngưỡng mép thấp hơn (0,22) cho vành dày; thêm vệt bọt trắng cong quay chậm (ánh bong bóng, không chấm sáng)
                NFbS(Front, 6, cc, w, h, 8 * Mathf.Sin(t * 7 + sd), NFb.BongDon, fr, 0.22f, 1, sd, 0.06f);
                NFbS(Front, 6.05f, cc, 0.92f * w, 0.92f * h, 130 + 60 * t + sd * 10, NFb.ChemVong, 2, 0.36f, 1, sd + 5, 0.3f, 2);
            };
            p.onDeath = (q, s) =>
            {
                var c = q.pos;
                s.NFbDoan(Front, 6.1f, _ => c, 0.32f, NFb.BongDon, 7, 15, 2.4f * r, 2.9f * r, 0, 0.3f, 0.1f);
                s.NFbPhat(Front, 6.05f, c, Vector2.zero, 0.3f, NFb.BongVo, 2.6f * r, 3.3f * r, s.U(0, 360), 0.3f, 0.06f);
                onHit?.Invoke();
            };
            Add(p);
            At(T1, () =>
            {
                var gp = new Vector2(nay.x, ground + (nay.y + 0.85f * r - ground) * 0.5f);
                NFbPhat(Floor, 2.1f, new Vector2(nay.x, nay.y + 0.85f * r), Vector2.zero, 0.5f, NFb.ChamDat, 1.2f * r, 3.2f * r, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f);
                NFbPhat(Front, 5.1f, new Vector2(nay.x, nay.y + 0.85f * r) + Len * (0.9f * r), Vector2.zero, 0.3f, NFb.ToeGiuaNho, 2.2f * r, 3f * r, 0, 0.3f, 0.08f);
                for (int j = 0; j < 4; j++)
                    NGiot(new Vector2(nay.x, nay.y + 0.8f * r), new Vector2(U(-140, 140), -U(120, 240)), U(1.6f, 2.6f), Front, U(0.3f, 0.45f), 900, gp.y + 6);
            });
        }

        public float NCauNhot(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NCauNuoc(casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
            var g = TgDiem(casterFeet, casterH, mouth, foeFeet, true);
            float T0 = Mathf.Max(0.2f, lead);
            const float TT = 0.42f;
            float rc = Mathf.Clamp(0.22f * casterH, 28, 48);
            var dich = foeBody + new Vector2(0, -0.04f * tH);
            Vector2 Path(float t)
            {
                if (t < T0) return g;
                float x = Mathf.Min(1, (t - T0) / TT);
                return Vector2.Lerp(g, dich, x) + new Vector2(0, -4 * 45 * x * (1 - x));
            }
            CauNuoc(Path, T0 + TT, a => a < T0 ? 0 : rc * (0.6f + 0.4f * EaseOut((a - T0) / 0.06f)) * (1 - SmoothStep(T0 + TT - 0.04f, T0 + TT, a)), null, -1,
                Front, 0.62f);
            AtW(T0, () =>
            {
                var u = Unit(dich - g);
                NFbPhat(Front, 5.4f, g + u * (0.5f * rc), u * 40, 0.24f, NFb.ToeNgangC, 1.6f * rc, 2.1f * rc, NAng(u) + 180, 0.3f, 0.06f); // ToeNgangC toé về −x
                Shake?.Invoke(0.2f);
            });
            AtW(T0 + TT, () => BongNhot(dich, rc, tH, foeFeet));
            return T0 + TT;
        }

        // bong bóng lớn bọc lấy đối thủ (trong mờ: vành nước + ruột mờ 0,3 + vệt bọt xoay; đối thủ thấy rõ bên trong), rung hai nhịp, vỡ
        void BongNhot(Vector2 c, float r0, float tH, Vector2 foeFeet)
        {
            const float Dur = 0.82f;
            float Rf = 0.8f * tH, sd = NSeed();
            float R(float t)
            {
                float x = Mathf.Clamp01(t / 0.14f);
                float back = 1 + 0.12f * Mathf.Sin(Mathf.PI * x);          // phồng vượt cỡ rồi về
                return Mathf.Lerp(r0, Rf, EaseOut(x)) * back;
            }
            Shake?.Invoke(0.35f);
            NFbPhat(Front, 6.2f, c, Vector2.zero, 0.14f, NFb.ChopTron, 0.9f * Rf, 1.4f * Rf, U(0, 360), 0.3f, 0.2f);
            NP(Front, Dur, (q, t) =>
            {
                float rr = R(t), wob = 0.05f * Mathf.Sin(t * 15);
                float rx = rr * (1 + wob), ry = rr * (1 - wob);
                // ruột mờ: cầu shader alpha 0,26 (mặt nạ "đặc" của NSprite là ô vuông: lần chụp đầu thành khung vuông mờ quanh bong bóng)
                NBall(Front, 3.0f, c, ry, 0.26f, 0, 0.03f, 0.18f, sd, Vector2.right, rx / Mathf.Max(1, ry));
                NRing(Front, 3.2f, c, rx, ry, 0.86f, MLoang, 3.1f, 0.04f, 0, 1, sd);                          // vành nước
                NFbS(Front, 3.4f, c, 2.05f * rx, 2.05f * ry, t * 140 + sd * 20, NFb.ChemVong, 2, 0.32f, 1, sd, 0.3f, 2); // vệt bọt trắng xoay
                NFbS(Front, 3.4f, c, 1.7f * rx, 1.7f * ry, 200 - t * 110 + sd * 20, NFb.ChemVong, 3, 0.36f, 0.9f, sd + 3, 0.3f, 2);
            });
            Every(0.05f, Dur - 0.1f, 12, x =>
            {
                var p = c + new Vector2(U(-0.55f, 0.55f) * Rf, U(-0.1f, 0.6f) * Rf);
                NFbPhat(Front, 3.3f, p, new Vector2(U(-15, 15), -U(60, 120)), U(0.4f, 0.6f), NFb.BongNho, 0.08f * Rf, 0.14f * Rf, 0, 0.35f, 0.15f);
            });
            for (int i = 1; i <= 2; i++)
                At(0.26f * i + 0.04f, () =>
                {
                    NuocPulse?.Invoke(0.35f);
                    Shake?.Invoke(0.12f);
                });
            AtW(Dur, () =>
            {
                Shake?.Invoke(0.6f);
                FlashScreen?.Invoke(FlashW);
                NuocPulse?.Invoke(0.8f);
                NFbDoan(Front, 6.1f, _ => c, 0.36f, NFb.BongDon, 8, 15, 2.1f * Rf, 2.5f * Rf, 0, 0.3f, 0.1f);
                NFbPhat(Front, 6.05f, c, Vector2.zero, 0.36f, NFb.BongVo, 2.2f * Rf, 2.8f * Rf, U(0, 360), 0.3f, 0.06f);
                GSplash(c, 1.2f, foeFeet.y, tH, Front, null);
                for (int j = 0; j < 18; j++)
                {
                    float an = 6.283f * (j + U(0, 0.7f)) / 18;
                    var v = new Vector2(Mathf.Cos(an), Mathf.Sin(an) - 0.3f) * U(220, 420);
                    float rd = U(2.4f, 4.2f);
                    NFbPhat(Front, 5.9f, c + new Vector2(Mathf.Cos(an), Mathf.Sin(an)) * (0.8f * Rf), v, U(0.4f, 0.6f), NFb.Giot, rd * 1.8f, rd, NAng(v), 0.35f, 0.1f,
                        0, false, 900, 0, 0, 0.6f);
                }
                Puddle(foeFeet + new Vector2(0, 3), 32, 1.6f);
            });
        }

        // ================= Hải Đăng: Bom nước =================
        public float NBom(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NTiaNuoc(false, casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
            float dir = foeFeet.x < casterFeet.x ? -1 : 1;
            var g = LechRig(mouth, casterFeet, casterH, foeFeet, CdMieng, CdMzR);
            float T0 = Mathf.Max(0.15f, lead);
            const float TT = 0.5f;
            float rc = Mathf.Clamp(0.14f * casterH, 16, 30);
            var land = foeFeet + new Vector2(-dir * 0.06f * tH, -rc);
            float apex = Mathf.Max(0.95f * tH, 70);
            Vector2 Path(float t)
            {
                if (t < T0) return g + new Vector2(0, 2 * Mathf.Sin(t * 9));
                float x = Mathf.Min(1, (t - T0) / TT);
                return Vector2.Lerp(g, land, x) + new Vector2(0, -4 * apex * x * (1 - x));
            }
            float tg = Mathf.Max(0.1f, T0 - 0.05f);
            Gather(Path, 0, T0 - 0.05f, 70, 60);
            CauNuoc(Path, T0 + TT, a => rc * EaseOut(Mathf.Min(1, a / tg)) * (1 - SmoothStep(T0 + TT - 0.03f, T0 + TT, a)), null, T0, Front, 0.62f);
            AtW(T0, () =>
            {
                var u = Unit(Path(T0 + 0.05f) - g);
                NFbPhat(Front, 5.4f, g + u * (0.6f * rc), u * 40, 0.24f, NFb.ToeNgangC, 1.5f * rc, 2f * rc, NAng(u) + 180, 0.3f, 0.06f);
                Shake?.Invoke(0.2f);
            });
            // báo trước chỗ rơi (KR5: đòn xuống đất báo trước trên đất): vòng gợn CO về tâm dưới chân đối thủ trong lúc cầu bay
            for (int k = 0; k < 3; k++)
                AtW(T0 + 0.13f * k, () => NFbPhat(Floor, 2.1f, foeFeet + new Vector2(0, 2), Vector2.zero, 0.42f, NFb.ChamDat, 1.1f * tH, 0.45f * tH, 0, 0.3f, 0, 1,
                    false, 0, 0, 0, 0.32f));
            // nổ: lần chụp đầu (toé đất 1,35 tH + ba cột 1,05 tH) nhỏ so với chữ "bom": to lên, thêm toé thân, vành gợn rộng, vòng giọt toả đều
            AtW(T0 + TT, () =>
            {
                Shake?.Invoke(0.7f);
                FlashScreen?.Invoke(FlashW);
                NFbPhat(Front, 6.2f, foeFeet + new Vector2(0, -0.25f * tH), Vector2.zero, 0.15f, NFb.ChopTron, 1.1f * tH, 1.7f * tH, U(0, 360), 0.3f, 0.2f);
                GToe(foeFeet, 1.85f * tH, Front);
                GCotPhun(foeFeet, 1.45f * tH);
                GSplash(foeFeet + new Vector2(0, -0.45f * tH), 1.15f, foeFeet.y, tH, Front, new Vector2(0, -1));
                NFbPhat(Front, 6.0f, foeFeet + new Vector2(0, -0.4f * tH), Vector2.zero, 0.36f, NFb.BongVo, 1.3f * tH, 1.7f * tH, U(0, 360), 0.3f, 0.05f);
                NFbPhat(Floor, 2.1f, foeFeet + new Vector2(0, 2), Vector2.zero, 0.7f, NFb.ChamDat, 0.6f * tH, 2.4f * tH, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f);
                for (int j = 0; j < 16; j++)
                {
                    float an = Mathf.PI * (0.05f + 0.9f * (j + U(0, 0.8f)) / 16);       // nửa trên, rải đều
                    var v = new Vector2(Mathf.Cos(an), -Mathf.Sin(an)) * U(260, 520);
                    float rd = U(2.6f, 4.6f);
                    NFbPhat(Front, 5.9f, foeFeet + new Vector2(0, -0.3f * tH), v, U(0.45f, 0.65f), NFb.Giot, rd * 1.8f, rd, NAng(v), 0.35f, 0.1f, 0, false, 900, 0,
                        0, 0.6f);
                }
                RainBack(foeFeet, tH, 16, 0.8f, 0.25f, 0.75f);
                Puddle(foeFeet + new Vector2(0, 3), 38, 1.7f);
            });
            return T0 + TT;
        }

        // ================= Giông Bão: Cầu xoáy / Mưa giông =================
        // đầu trượng theo clip cast (bảng GbTruong của tia cũ, HatFbThuy.cs); clip chiêu cuối không có bảng nên dùng chỗ bắn của rig
        Func<float, Vector2> GbDauTruong(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeFeet)
        {
            bool d2 = (casterFeet.y - mouth.y) / Mathf.Max(1, casterH) > 0.45f;
            var b = d2 ? GbTruong2 : GbTruong1;
            var mz = d2 ? GbMzR2 : GbMzR1;
            return t => LechRig(mouth, casterFeet, casterH, foeFeet, DiemBang(b, t), mz);
        }

        // CẦU XOÁY (gói: StrongProjectile_Cast / Traveling / Impact): nước bị hút xoắn về quả cầu ở đầu trượng, cầu lớn dần theo trượng vung; khung
        // nhả: cầu phóng thẳng (khối nước cuộn kéo sau + lưỡi liềm quay của NCauShader), ba cầu nhỏ quay quanh như vệ tinh, vệt xoắn rơi dọc
        // đường; trúng: chớp tròn + chớp hướng, gai sắc, toé sao, toé lớn
        public float NCauXoay(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NTiaNuoc(false, casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
            float dir = foeFeet.x < casterFeet.x ? -1 : 1;
            var dau = GbDauTruong(casterFeet, casterH, mouth, foeFeet);
            float T0 = Mathf.Max(0.2f, lead);
            var g0 = dau(T0);
            var dich = foeBody + new Vector2(-dir * 0.08f * tH, -0.04f * tH);
            float TT = Mathf.Clamp((dich - g0).magnitude / 1300f, 0.22f, 0.36f);
            float rc = Mathf.Clamp(0.13f * casterH, 16, 30);
            Vector2 Path(float t)
            {
                if (t < T0) return dau(t);
                float x = Mathf.Min(1, (t - T0) / TT);
                return Vector2.Lerp(g0, dich, x) + new Vector2(0, -4 * 22 * x * (1 - x));
            }
            float tg = Mathf.Max(0.12f, T0 - 0.05f);
            var pulse = new float[1];
            Gather(Path, 0, T0 - 0.05f, 85, 70, Front, pulse);
            // đuôi chỉ tính từ lúc rời trượng (tDuoi0 = T0): lần chụp đầu đuôi 0,2 s gồm cả cú vung trượng thành dải nước gập khuỷu
            NCauShader(Path, T0 + TT, a => rc * (0.25f + 0.75f * EaseOut(Mathf.Min(1, a / tg))) * (1 - SmoothStep(T0 + TT - 0.03f, T0 + TT, a)), pulse, T0, Front,
                T0);
            // ba cầu nhỏ quay quanh (nghiêng theo hướng bay; nửa vòng sau vẽ ở lớp sau)
            float sd = NSeed(), start = T;
            NP(Front, T0 + TT, (q, a) =>
            {
                if (a < 0.15f) return;
                var c = Path(a);
                var u = Unit(Path(a + 0.02f) - Path(Mathf.Max(0, a - 0.02f)));
                if (a < T0) u = new Vector2(dir, 0);
                var n = new Vector2(-u.y, u.x);
                float lon = Mathf.Min(1, (a - 0.15f) / 0.2f) * (1 - SmoothStep(T0 + TT - 0.05f, T0 + TT, a));
                for (int i = 0; i < 3; i++)
                {
                    float th = a * 15 + i * 2.094f;
                    float cs = Mathf.Cos(th), sn = Mathf.Sin(th);
                    var p = c + n * (sn * 1.75f * rc) + u * (cs * 0.55f * rc);
                    NBall(cs > 0 ? Front : Back, cs > 0 ? 6.4f : 3.6f, p, 0.3f * rc * lon * (0.85f + 0.15f * cs), 1, 0, 0.05f, 0.4f, sd + i);
                }
            });
            // vệt xoắn rơi lại dọc đường bay
            Every(T0, T0 + TT, 26, x =>
            {
                var c = Path(T - start);
                var u = Unit(dich - g0);
                float w = U(1.6f, 2.2f) * rc;
                NFbPhat(U(0, 1) < 0.6f ? Front : Back, 5.0f, c - u * (0.8f * rc), -u * U(30, 80) + new Vector2(0, -U(0, 30)), U(0.28f, 0.36f), NFb.Xoan, w, w * 1.1f,
                    NAng(u) + U(-20, 20), 0.28f, 0.05f, 0, U(0, 1) < 0.5f, 120, 1, 0, 0.55f);
            });
            AtW(T0, () =>
            {
                Shake?.Invoke(0.25f);
                var u = Unit(dich - g0);
                NFbPhat(Front, 5.6f, g0 + u * rc, u * 50, 0.2f, NFb.ChopHuong, 1.6f * rc, 2.2f * rc, NAng(u), 0.3f, 0.12f);
            });
            AtW(T0 + TT, () =>
            {
                var u = Unit(dich - g0);
                float back = NAng(-u);
                Shake?.Invoke(0.45f);
                NFbPhat(Front, 6.2f, dich - u * (0.15f * rc), Vector2.zero, 0.16f, NFb.ChopTron, 2.6f * rc, 3.8f * rc, U(0, 360), 0.3f, 0.2f);
                NFbPhat(Front, 6.1f, dich, Vector2.zero, 0.15f, NFb.ChopHuong, 3f * rc, 4f * rc, NAng(u), 0.3f, 0.12f);
                for (int j = 0; j < 7; j++)
                {
                    float an = back + (U(0, 1) < 0.5f ? -1 : 1) * U(15, 85);
                    var d = NHuong(an);
                    float w = U(1.6f, 2.8f) * rc;
                    NFbPhat(Front, 6.0f, dich + d * (0.4f * rc), d * U(180, 420), U(0.2f, 0.27f), NFb.GaiTrung, w, w * 1.25f, an, 0.32f, -0.1f, 0, false, 0, 3, 0, 0.55f);
                }
                for (int j = 0; j < 2; j++)
                {
                    float an = back + (j == 0 ? 1 : -1) * U(20, 45);
                    var d = NHuong(an);
                    float w = U(3.2f, 4.2f) * rc;
                    NFbPhat(Front, 5.6f, dich + d * (0.3f * w), d * U(50, 110), U(0.26f, 0.32f), NFb.ToeNgangC, w * 0.8f, w, an + 180, 0.3f, 0.05f);
                }
                GSplash(dich, 0.95f, foeFeet.y, tH, Front, u);
                Puddle(foeFeet + new Vector2(0, 3), 24, 1.3f);
            });
            return T0 + TT;
        }

        // cột thác dội từ trên xuống (ống nước dựng đứng, cùng lớp ống của tia Water Laser): đầu nước rơi xuống đất trong TR, giữ giu giây (thân
        // gợn, loe dần về chân), rồi đuôi rời mây rơi nốt; chạm đất gọi onCham
        void ThacDoi(Vector2 top, float yDat, float hw, float giu, int g, Action onCham)
        {
            float sd = NSeed(), L = Mathf.Max(20, yDat - top.y);
            const float TR = 0.09f, TD = 0.16f;
            NP(g, TR + giu + TD + 0.04f, (q, a) =>
            {
                float head = EaseOut(Mathf.Clamp01(a / TR));
                float tail = a < TR + giu ? 0 : Mathf.Clamp01((a - TR - giu) / TD);
                if (head <= tail + 0.01f) return;
                float cut = tail > 0 ? 0.1f + 0.6f * tail : 0;
                nPts.Clear();
                nHw.Clear();
                const int N = 18;
                for (int i = 0; i <= N; i++)
                {
                    float s = Mathf.Lerp(tail, head, i / (float)N);
                    float wob = Mathf.Sin(s * 7 - a * 12 + sd) * 0.12f * hw;
                    nPts.Add(new Vector2(top.x + wob, top.y + s * L));
                    float w = hw * (0.55f + 0.5f * s) * (1 + 0.08f * Mathf.Sin(s * 13 - a * 17));
                    if (head < 1 && s > head - 0.08f) w *= 0.6f + 0.4f * Mathf.Clamp01((head - s) / 0.08f);
                    nHw.Add(w);
                }
                NTubePrep();
                NTube(g, 3.82f, 3, 1.2f, 1.5f, Mathf.Max(cut, 0.05f), sd);
                NTube(g, 4.0f, 0, 1f, 2.2f, cut, sd + 3);
                NTube(g, 4.12f, 1, 0.55f, 2.8f, cut, sd + 7);
                NTube(g, 4.2f, 2, 0.78f, 3.4f, cut, sd + 11);
            });
            At(TR, () => onCham?.Invoke());
        }

        // MƯA GIÔNG (chiêu cuối; gói: RainExample + WaterGround + FallingWater): giơ gậy thì mây tụ trên đầu đối thủ (NMua), dậm gậy thì mưa trút,
        // ba cột thác dội lần lượt (giữa trúng đối thủ, rồi hai bên), hai tia sét trong mây giông đánh xuống
        public float NMuaGiong(Vector2 casterFeet, float casterH, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NThuong(casterFeet, casterH, foeBody, foeFeet, tH, lead, 8);
            float T0 = Mathf.Max(0.35f, lead);
            NMua(foeFeet, tH, lead, 1.3f);
            var top = foeFeet + new Vector2(0, -1.2f * tH);
            if (top.y < 44) top.y = 44;
            float hw = 0.2f * tH;
            float[] lech = { 0, -0.5f, 0.48f };
            float[] gio = { 0, 0.28f, 0.52f };
            for (int i = 0; i < 3; i++)
            {
                int ii = i;
                var p = new Vector2(foeFeet.x + lech[i] * tH, top.y + 14);
                p.x = Mathf.Clamp(p.x, 24, 536);
                // cột giữa đổ ngay trên đối thủ: vẽ ở lớp SAU tướng (lần chụp đầu ở lớp trước: ống nước đặc che kín con bị trúng), toé ở lớp trước
                AtW(T0 + gio[i] - 0.09f, () => ThacDoi(p, foeFeet.y + (ii == 0 ? 2 : U(-4, 8)), hw * (ii == 0 ? 1.15f : 0.9f), ii == 0 ? 0.32f : 0.22f,
                    ii == 0 ? Back : (U(0, 1) < 0.5f ? Front : Back), () =>
                    {
                        var chan = new Vector2(p.x, foeFeet.y + 2);
                        Shake?.Invoke(ii == 0 ? 0.5f : 0.3f);
                        GToe(chan, (ii == 0 ? 1.3f : 0.95f) * tH, Front);
                        NFbPhat(Front, 3.15f, chan + Len * (0.5f * tH), Vector2.zero, 0.5f, NFb.CotDung, 0.55f * tH, 0.62f * tH, 0, 0.3f, 0.04f, 0, U(0, 1) < 0.5f);
                        if (ii == 0) GSplash(foeBody, 0.9f, foeFeet.y, tH, Front, new Vector2(0, 1));
                        else NuocPulse?.Invoke(0.45f);
                    }));
            }
            // vệt mưa xiên rơi nhanh từ đáy mây (mưa của NMua mảnh, lần chụp đầu gần như không thấy): giọt kéo dài theo vận tốc, toé ở đất
            float gio0 = T0 - 0.05f, gio1 = T0 + 1.3f;
            EveryW(gio0, gio1, 46, x =>
            {
                var p = new Vector2(foeFeet.x + U(-1.2f, 1.1f) * tH, top.y + U(0, 22));
                var v = new Vector2(-110, U(900, 1150));
                float rd = U(2.2f, 3.4f);
                NFbPhat(U(0, 1) < 0.55f ? Front : Back, 5.8f, p, v, (foeFeet.y + U(-6, 10) - p.y) / v.y, NFb.Giot, rd * 5.5f, rd * 4.5f, NAng(v), 0.35f, 0.12f, 0,
                    false, 0, 0, 0, 0.32f, null, 0.9f);
            });
            // sét trong mây giông (khung set_danh nếu đã nhập): một phát vào đối thủ, một phát cạnh bên; chớp màn nhạt
            if (HasFb("set_danh"))
                for (int k = 0; k < 2; k++)
                {
                    bool vao = k == 0;
                    float tk = T0 + (vao ? 0.16f : 0.68f);
                    AtW(tk, () =>
                    {
                        var cham = vao ? foeFeet + new Vector2(U(-0.08f, 0.08f) * tH, 3) : foeFeet + new Vector2((U(0, 1) < 0.5f ? -1 : 1) * U(0.6f, 0.9f) * tH, U(-6, 6));
                        cham.x = Mathf.Clamp(cham.x, 24, 536);
                        Fb("set_danh", cham, (vao ? 1.55f : 1.35f) * tH, Front, 42, 1.4f, 0, U(0, 1) < 0.5f, null, 0.95f, -1, 1);
                        FlashScreen?.Invoke(new Color(1, 1, 0.93f, vao ? 0.2f : 0.12f));
                        Shake?.Invoke(vao ? 0.4f : 0.25f);
                        if (vao) NuocPulse?.Invoke(0.55f);
                    });
                }
            return T0;
        }

        // ================= Thôn Kình: Sóng thần =================
        // há to: một luồng nước dày tuôn từ miệng đổ xuống đất trước mặt (ống nước cong), dựng thành con sóng lớn (NSong × 1,45) cuộn tới đổ ập
        public float NSongThan(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NTiaNuoc(true, casterFeet, casterH, mouth, foeFeet + new Vector2(0, -0.5f * tH), foeFeet, tH, lead);
            float sx = foeFeet.x < casterFeet.x ? -1 : 1;
            float T0 = Mathf.Max(0.18f, lead);
            var A = casterFeet + new Vector2(sx * 0.46f * casterH, -4);   // chân sóng (như NSong)
            float day = Mathf.Clamp(0.24f * casterH, 30, 64), sd = NSeed();
            const float TU = 0.12f, GIU = 0.36f, TD = 0.18f;
            AtW(T0 - 0.06f, () =>
            {
                Shake?.Invoke(0.35f);
                NP(Front, TU + GIU + TD + 0.04f, (q, a) =>
                {
                    float head = EaseOut(Mathf.Clamp01(a / TU));
                    float tail = a < TU + GIU ? 0 : Mathf.Clamp01((a - TU - GIU) / TD);
                    if (head <= tail + 0.01f) return;
                    var m = mouth + new Vector2(sx * 0.04f * casterH, 0);
                    var cv = new Vector2(Mathf.Lerp(m.x, A.x, 0.7f) + sx * 0.12f * casterH, m.y - 0.05f * casterH); // cong ra trước rồi đổ xuống
                    nPts.Clear();
                    nHw.Clear();
                    const int N = 18;
                    for (int i = 0; i <= N; i++)
                    {
                        float s = Mathf.Lerp(tail, head, i / (float)N);
                        float u1 = 1 - s;
                        nPts.Add(u1 * u1 * m + 2 * u1 * s * cv + s * s * A + new Vector2(0, Mathf.Sin(s * 9 - a * 14) * 0.05f * day));
                        nHw.Add(0.5f * day * (0.7f + 0.5f * s) * (1 + 0.08f * Mathf.Sin(s * 11 - a * 16)));
                    }
                    float cut = tail > 0 ? 0.1f + 0.6f * tail : 0;
                    NTubePrep();
                    NTube(Front, 3.82f, 3, 1.2f, 1.5f, Mathf.Max(cut, 0.05f), sd);
                    NTube(Front, 4.0f, 0, 1f, 2.3f, cut, sd + 3);
                    NTube(Front, 4.12f, 1, 0.55f, 2.9f, cut, sd + 7);
                    NTube(Front, 4.2f, 2, 0.78f, 3.5f, cut, sd + 11);
                });
            });
            Every(T0, T0 + GIU, 14, x =>
            {
                var v = new Vector2(sx * U(60, 200), -U(80, 220));
                float rd = U(2.6f, 4.4f);
                NFbPhat(Front, 5.9f, A + new Vector2(U(-0.1f, 0.1f) * casterH, -U(0, 20)), v, U(0.4f, 0.6f), NFb.Giot, rd * 1.8f, rd, NAng(v), 0.35f, 0.1f, 0,
                    false, 900, 0, 0, 0.6f);
            });
            AtW(T0 + 0.04f, () => GToe(A + new Vector2(0, 2), 0.9f * casterH, Front));
            return NSong(casterFeet, casterH, foeFeet, tH, T0 + 0.12f, 1.45f);
        }

        // ================= Thôn Kình: Cầu ma thủy (thay Sóng thần) =================
        // Người dùng 2026-11-25: "chiêu này đổi sang magic orb này rồi cho nó nổ ở vị trí địch"; xem bản đầu (cầu đặc tô dải, bắn từ miệng)
        // thì "sao nhìn không giống với demo", rồi "cho ngoại lệ quầng sáng, làm lại giống demo, làm thêm phần xung quanh của nó nữa" và
        // "chiêu của con đấy là triệu hồi quả cầu đấy ở chỗ địch luôn rồi nổ chứ không cần bắn".
        // Dựng theo từng lớp của prefab FX_PF_MagicWater_OrbLoop (ArtGen/XemVfx/vfx_goi/PHAN_TICH.md), cỡ theo bán kính vỏ cầu r (vỏ gói size
        // 2,1), cầu TRIỆU HỒI ngay ở thân đối thủ (đối thủ nằm trong cầu):
        //  - Glow / Mask: quầng TỐI lớn (2,4 r, 2 r) — NGOẠI LỆ quầng (NQuang tông tối, shader UIWaterFx chế độ 8);
        //  - DarkBack / DarkSphere: vỏ cầu gần trong suốt (cầu shader alpha 0,3) + mảng xoáy TwirlingWater tối; LightSphere: mảng xoáy sáng
        //    quay ngược chiều (Xoan);
        //  - HeartCircle: vòng mảnh màu kem quanh lõi; Heartlight: LÕI QUẦNG SÁNG (NQuang tông sáng, chập chờn) + chấm lõi kem;
        //  - Around / AroundDark: bốn vệt nước dài bay vòng trên quỹ đạo elip nghiêng rộng 2–2,35 r (ống nước bảng xanh ngọc, thon hai đầu);
        //  - SparksLoop: hạt sáng li ti toả chập chờn 26 / giây; Dots / ExtraDots: giọt nước trôi 12 / giây;
        //  - Cast lúc triệu hồi: chớp quầng lớn tắt dần (Heartlight_Burst), chớp tia toả (RadialImpact), hai vỏ xoáy nở (CircleBurst 0 / 0,2 s),
        //    vòng sóng chấn nở (ShockWave khúc xạ → vành bọt phẳng), chùm hạt sáng toả (LightBurst); nước + hạt hút xoắn vào suốt pha tụ;
        //  - phần xung quanh: quầng tối dẹt trên đất dưới chân đối thủ + vòng gợn xanh ngọc lan đều.
        // Lớp: quầng, vỏ, xoáy tối, lõi, vòng tim, nửa SAU các vệt bay vòng vẽ ở lớp SAU tướng (đối thủ đứng trước lõi sáng, vẫn thấy rõ); xoáy
        // sáng, nửa TRƯỚC các vệt, hạt sáng, giọt ở lớp trước.
        // Nhịp (clip há to miệng): cầu hiện + lớn dần từ đầu clip, tới khung há (lead) bừng sáng, giữ 0,3 s rồi NỔ tại chỗ (MaNo).
        public float NCauMa(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NSongThan(casterFeet, casterH, mouth, foeFeet, tH, lead);
            const int pal = HatNuocFx.PalMa;
            var hien = CauMaHienTruoc();
            // prefab gốc: cầu chỉ THÀNH HÌNH (lõi sáng, dải xoáy bay vòng, hạt sáng) ở giây 0,8 của gói (Cast cuộn kín lõi 0,25–0,8 s, rồi
            // Heartlight_Impact / RadialImpact / LightBurst bừng) → tua phần tụ cho giây 0,8 của gói rơi đúng khung há (T0), giữ cầu đã thành hình
            // 0,5 s rồi mới nổ (bản đầu nổ ở ~0,75 s gói, đúng trước lúc thành hình, nên không thấy lõi sáng như demo)
            float T0 = hien ? Mathf.Max(0.5f, lead) : Mathf.Max(0.45f, lead), tN = T0 + (hien ? 0.5f : 0.3f);
            var c = foeBody + new Vector2(0, -0.04f * tH);
            float R = 0.75f * tH;   // to hơn thân đối thủ một chút: các lớp cầu tràn ra ngoài viền đối thủ (0,55 thì bị che gần hết)
            float sd = NSeed();
            float Lon(float t)
            {
                float k = 0.25f + 0.75f * EaseOut(Mathf.Min(1, t / Mathf.Max(0.15f, T0 - 0.05f)));
                if (t >= T0) k = 1 + 0.06f * Mathf.Sin((t - T0) * 30);                // bừng ở khung há, rung tới lúc nổ
                return k * (t > tN - 0.06f ? 0.88f : 1);                            // nén 1 khung trước khi nổ
            }
            Vector2 Tam(float t) => c + new Vector2(0, 2.5f * Mathf.Sin(t * 6));
            // HƯỚNG A (người dùng 2026-11-25: "dùng thẳng prefab của gói, nhưng nên sửa lại 1 chút để nó có chất vẽ tay hơn"): sân có CauMaRT (menu
            // CauMaRigMenu) thì thân cầu là prefab gốc FX_PF_MagicWater_OrbLoop chạy trong rig, chụp RenderTexture, hiện qua shader UIVeTayRT (dải
            // phẳng + vân chì + quầng). Vỏ gói bán kính 1,05 đơn vị ↔ R; khung camera 8,04 đơn vị (FOV 30, cách 15). Hệ hạt đẩy theo giờ sân.
            // Phần Cast / lõi bừng của gói tự có, nên bỏ các lớp shader tự vẽ (VeCauMa, VeVongMa, hạt sáng, hút xoắn, chớp triệu hồi).
            if (hien)
            {
                const float GoiThanh = 0.8f;                         // giây gói lúc cầu thành hình
                float last = 0, co = 8.04f * (0.5f * tH / 1.05f);   // vỏ gói (bán kính 1,05) ↔ 0,5 thân đối thủ (0,75: vỏ xoáy to che kín đối thủ)
                float Goi(float t) => t < T0 ? t * GoiThanh / T0 : GoiThanh + (t - T0);
                hien.Bat();
                NP(Front, tN + 0.14f, (q, a) =>
                {
                    float dt = Mathf.Max(0, Goi(a) - Goi(last));
                    last = a;
                    float an = Mathf.Min(1, a / 0.06f) * (a < tN ? 1 : Mathf.Max(0, 1 - (a - tN) / 0.12f));
                    float nen = a > tN - 0.07f && a < tN ? 0.86f : 1;  // nén 1–2 khung trước khi nổ
                    hien.Ve(StageView.P(Tam(a)), co * NK * nen, an, dt);
                });
                At(tN + 0.15f, () => hien.Tat());
                AtW(0.02f, () => Shake?.Invoke(0.3f));
                AtW(T0, () => Shake?.Invoke(0.35f));
            }
            else
            {
                NP(Front, tN, (q, a) => VeCauMa(Tam(a), R * Lon(a), a, sd, a >= T0 ? 1.25f : 1));
                NP(Front, tN, (q, a) => VeVongMa(Tam(a), R * Lon(a), a, sd));
                EveryW(0.05f, tN, 26, x => HatMa(c, R));
                EveryW(0.05f, tN, 12, x => GiotMa(c, R));
            }
            // phần xung quanh dưới chân đối thủ: quầng tối dẹt + vòng gợn xanh ngọc lan đều
            var dat = foeFeet + new Vector2(0, 2);
            NP(Floor, tN + 0.05f, (q, a) =>
            {
                float k = Mathf.Min(1, a / 0.3f) * (1 - SmoothStep(tN - 0.05f, tN + 0.05f, a));
                NQuang(Floor, 2.0f, dat, 0.42f * tH * k, 0.5f, 1.4f, 1, 0.15f, sd + 9, pal, 2.8f);
            });
            EveryW(0.05f, tN, 3.5f, x => NFbPhat(Floor, 2.1f, dat, Vector2.zero, 0.7f, NFb.ChamDat, 0.5f * tH, 2f * tH, 0, 0.3f, 0.1f, 1, false, 0, 0, 0, 0.32f, null,
                0.8f, pal));
            if (hien)
            {
                AtW(tN, () => MaNo(c, 0.3f * R, tH, foeFeet));
                return tN;
            }
            // Cast lúc triệu hồi
            AtW(0.02f, () =>
            {
                Shake?.Invoke(0.3f);
                NP(Front, 0.55f, (q, a) => NQuang(Front, 6.5f, c, Mathf.Lerp(0.5f, 1.6f, EaseOut(a / 0.55f)) * R, 0.75f * (1 - a / 0.55f), 1.4f, 0, 0.2f, sd + 11, pal));
                NFbPhat(Front, 6.4f, c, Vector2.zero, 0.18f, NFb.ChopTron, 0.9f * R, 1.6f * R, U(0, 360), 0.3f, 0.25f, 0, false, 0, 0, 0, 0, null, 0.8f, pal);
                NP(Front, 0.35f, (q, a) =>
                {
                    float k = a / 0.35f, rr = Mathf.Lerp(0.6f, 2.2f, EaseOut(k)) * R;
                    NFbS(Front, 6.05f, c, 2 * rr, 1.8f * rr, 0, NFb.ChamDat, 2 + 9 * k, 0.3f, 1, sd + 13, 0.3f, 2, false, pal);
                });
                for (int k = 0; k < 2; k++)
                    AtW(0.2f * k, () => NFbPhat(Front, 6.15f, c, Vector2.zero, 0.5f, NFb.Xoan, 0.8f * R, 2.2f * R, U(0, 360), 0.3f, 0.12f, 0, U(0, 1) < 0.5f, 0, 0,
                        (U(0, 1) < 0.5f ? -1 : 1) * U(120, 220), 0.5f, null, 0.8f, pal));
                for (int j = 0; j < 20; j++) HatMa(c, 0.4f * R, 1);
            });
            // nước + hạt bị hút xoắn vào cầu suốt pha tụ
            EveryW(0.05f, tN - 0.05f, x => 10 + 26 * x, x =>
            {
                float an = U(0, 6.283f), rr = U(1.7f, 2.6f) * R, life = U(0.3f, 0.42f), sz = U(0.05f, 0.09f) * R;
                bool to = U(0, 1) < 0.25f;
                var p = new P { pos = c, life = life, group = Front };
                p.draw = (z, k, buf) =>
                {
                    float kk = k * k;
                    var o = new Vector2(Mathf.Cos(an + 3.2f * kk), Mathf.Sin(an + 3.2f * kk) * 0.8f) * (rr * (1 - kk));
                    z.pos = c + o;
                    if (to) NFbS(Front, 6.5f, z.pos, 0.9f * R * (1 - 0.5f * k), 0.28f * R, NAng(new Vector2(-o.y, o.x)), NFb.Xoan, k * 15, 0.3f, 1, sd + an, 0.1f, 0, false, pal);
                    else NDot(Front, 6.5f, z.pos, sz * (1 - 0.4f * k), 2, 1, -o, pal);
                };
                Add(p);
            });
            // khung há: lõi bừng sáng
            AtW(T0, () =>
            {
                Shake?.Invoke(0.35f);
                NP(Front, 0.28f, (q, a) => NQuang(Back, 6.55f, c, Mathf.Lerp(0.8f, 1.4f, a / 0.28f) * R, 0.9f * (1 - a / 0.28f), 1.2f, 0, 0.2f, sd + 12, pal));
            });
            AtW(tN, () => MaNo(c, 0.3f * R, tH, foeFeet));
            return tN;
        }

        // material của cầu prefab gốc theo hệ (CauMaHien.matHe, menu CauMaRigMenu)
        public const int CauMaThuy = 0, CauMaMoc = 1, CauMaHoa = 2;

        // CẦU MA ĐỔI MÀU cho hệ khác (2026-11-25, người dùng: "giờ làm cho cả các hệ khác nữa nhé, phù hợp thì mới làm"; chọn cầu ma xanh lục cho
        // Gạc Đá / Lộc Phong, cầu ma màu lửa cho Hỏa): vẽ cầu prefab gốc bám đường cFn (toạ độ sân) với bán kính rFn của quả cầu cũ (vỏ gói bán
        // kính 1,05 ↔ r), tuổi a tính từ lúc gọi, tới tEnd; tua gói cho giây 0,8 (cầu thành hình: lõi sáng, dải bay vòng) rơi đúng tThanh (lúc
        // cầu đầy của chiêu cũ). r ≤ 0,5 thì ẩn. Trả false nếu sân / ô xem chưa gắn CauMaRT (chiêu tự vẽ cầu cũ).
        // k: phóng cầu so với cầu cũ (Hỏa Quy 1,8: cầu lửa cũ nhỏ, cầu gói thưa hơn nên phải to hơn mới đọc được giữa lưỡi lửa)
        bool CauMaTheo(int he, Func<float, Vector2> cFn, Func<float, float> rFn, float tEnd, float tThanh, float k = 1)
        {
            var hien = CauMaHienTruoc();
            if (!hien) return false;
            const float GoiThanh = 0.8f;
            float th = Mathf.Max(0.1f, tThanh), last = 0;
            float Goi(float t) => t < th ? t * GoiThanh / th : GoiThanh + (t - th);
            hien.Bat(he);
            NP(Front, tEnd + 0.02f, (q, a) =>
            {
                float dt = Mathf.Max(0, Goi(a) - Goi(last));
                last = a;
                float r = a < tEnd ? rFn(a) : 0;
                float an = r > 0.5f ? Mathf.Min(1, a / 0.06f) : 0;
                hien.Ve(StageView.P(cFn(a)), 8.04f * (Mathf.Max(1, r) * k / 1.05f) * NK, an, dt);
            });
            At(tEnd + 0.03f, () => hien.Tat());
            return true;
        }

        // RawImage hiện prefab gốc ở lớp hạt trước (CauMaRT, CauMaRigMenu); null nếu sân / ô xem chưa gắn
        CauMaHien cauMaHien;
        bool cauMaTim;

        CauMaHien CauMaHienTruoc()
        {
            if (!cauMaTim)
            {
                cauMaTim = true;
                if (groups[Front]) cauMaHien = groups[Front].GetComponentInChildren<CauMaHien>(true);
            }
            return cauMaHien && cauMaHien.San ? cauMaHien : null;
        }

        // thân cầu ma thủy (tâm c, bán kính vỏ r, a giây; sang: nhân cỡ lõi sáng): lớp sau tướng (quầng, vỏ, xoáy tối, lõi, vòng tim) / lớp trước
        // (xoáy sáng)
        void VeCauMa(Vector2 c, float r, float a, float sd, float sang = 1)
        {
            const int pal = HatNuocFx.PalMa;
            if (r < 2) return;
            // lần chụp thứ hai (cầu triệu hồi tại đối thủ) quá nhạt: đối thủ che gần hết các lớp sau → quầng tối đậm + loang rộng hơn, vỏ sau đậm
            // hơn, thêm vỏ mờ + vành + lõi sáng mờ ở lớp TRƯỚC (đối thủ vẫn thấy qua)
            NQuang(Back, 5.0f, c, 2.3f * r, 0.62f, 1.0f, 1, 0.25f, sd, pal);                                    // Glow (tối)
            NQuang(Back, 5.05f, c, 1.7f * r, 0.5f, 1.6f, 1, 0.2f, sd + 1, pal);                                 // Mask (tối)
            NBall(Back, 5.5f, c, r, 0.55f, 0, 0.06f, 0.4f, sd + 2, null, 1, pal);                               // DarkBack
            NFbS(Back, 5.6f, c, 2.1f * r, 1.1f * r, a * 140 + sd * 40, NFb.Xoan, (a * 16) % 16, 0.3f, 1, sd + 3, -0.08f, 0, false, pal);           // DarkSphere
            NFbS(Back, 6.2f, c, 0.62f * r * sang, 0.62f * r * sang, a * 60, NFb.ChamDat, 2.5f + Mathf.Sin(a * 9), 0.32f, 1, sd + 5, 0.3f, 2, false, pal); // HeartCircle
            NQuang(Back, 6.3f, c, 1.0f * r * sang * (1 + 0.08f * Mathf.Sin(a * 13 + sd)), 1, 1.2f, 0, 0.25f, sd + 6, pal);                          // Heartlight
            NDot(Back, 6.35f, c, 0.15f * r * sang, 2, 1, null, pal);
            NBall(Front, 5.4f, c, r, 0.16f, 0, 0.06f, 0.4f, sd + 7, null, 1, pal);                               // mặt trước vỏ: mờ, nhuộm nhẹ đối thủ
            NFbS(Front, 5.45f, c, 2.06f * r, 2.06f * r, a * 40, NFb.ChamDat, 3, 0.36f, 1, sd + 8, 0.25f, 0, false, pal); // vành vỏ
            NQuang(Front, 5.5f, c, 0.55f * r * sang, 0.55f, 1.6f, 0, 0.2f, sd + 10, pal);                       // lõi sáng lọt qua thân đối thủ
            NFbS(Front, 5.65f, c, 1.9f * r, 1.0f * r, -a * 110 + sd * 40 + 90, NFb.Xoan, (a * 16 + 7) % 16, 0.3f, 1, sd + 4, 0.2f, 0, true, pal); // LightSphere
        }

        // vệt nước bay vòng (Around / AroundDark): bốn vệt dài trên quỹ đạo elip nghiêng; đoạn nửa sau (sin < 0) ở lớp SAU tướng, nửa trước ở lớp
        // trước
        void VeVongMa(Vector2 c, float r, float a, float sd)
        {
            const int pal = HatNuocFx.PalMa;
            if (r < 3) return;
            for (int i = 0; i < 4; i++)
            {
                float Rx = (1.6f + 0.3f * (i % 2)) * r, Ry = (0.45f + 0.08f * i) * r;
                float tilt = (i % 2 == 0 ? -18 : 14) * Mathf.Deg2Rad, ct = Mathf.Cos(tilt), st = Mathf.Sin(tilt);
                float phi = sd + i * 1.57f + a * (i < 2 ? 1.6f : -1.3f);
                float span = i % 2 == 0 ? 1.25f : 0.95f;
                bool toi = i >= 2;
                for (int pass = 0; pass < 2; pass++)
                {
                    nPts.Clear();
                    nHw.Clear();
                    const int M = 22;
                    for (int j = 0; j <= M; j++)
                    {
                        float u = j / (float)M, th = phi - span + 2 * span * u, sn = Mathf.Sin(th);
                        if ((sn > 0) != (pass == 1))
                        {
                            if (nPts.Count >= 2) break;
                            nPts.Clear();
                            nHw.Clear();
                            continue;
                        }
                        float ex = Mathf.Cos(th) * Rx, ey = sn * Ry;
                        nPts.Add(c + new Vector2(ex * ct - ey * st, ex * st + ey * ct));
                        nHw.Add(Mathf.Max(0.3f, 0.15f * r * Mathf.Sin(Mathf.PI * u) * (0.8f + 0.2f * sn)));
                    }
                    if (nPts.Count < 2) continue;
                    NTubePrep();
                    int g = pass == 1 ? Front : Back;
                    float layer = pass == 1 ? 6.45f : 5.55f;
                    if (toi)
                    {
                        NTube(g, layer, 3, 1.1f, 2.2f, 0.05f, sd + i, 1, pal);
                        NTube(g, layer + 0.01f, 0, 0.9f, 2.6f, 0, sd + i + 3, 1, pal);
                    }
                    else
                    {
                        NTube(g, layer, 0, 1f, 2.4f, 0, sd + i, 1, pal);
                        NTube(g, layer + 0.01f, 1, 0.6f, 3f, 0, sd + i + 3, 1, pal);
                        NTube(g, layer + 0.02f, 2, 0.8f, 3.4f, 0, sd + i + 5, 1, pal);
                    }
                }
            }
        }

        // hạt sáng li ti (SparksLoop / LightBurst): quầng nhỏ + chấm kem, bay toả chập chờn rồi tắt dần; manh > 0: toả nhanh (bung)
        void HatMa(Vector2 c, float R, float manh = 0)
        {
            const int pal = HatNuocFx.PalMa;
            float an = U(0, 6.283f), sp = manh > 0 ? U(300, 600) : U(40, 110);
            var d = new Vector2(Mathf.Cos(an), Mathf.Sin(an));
            var p = new P { pos = c + d * (U(0.4f, 1.1f) * R), vel = d * sp, life = manh > 0 ? U(0.3f, 0.5f) : U(0.4f, 1.0f), drag = manh > 0 ? 3 : 1.2f, group = Front };
            float sz = Mathf.Clamp(U(0.05f, 0.1f) * R, 3.5f, 9), ph = U(0, 6.28f), sdd = NSeed();
            p.upd = (q, dt, s) => q.vel += new Vector2(Mathf.Sin(q.age * 9 + ph), Mathf.Cos(q.age * 7 + ph)) * (160 * dt);
            p.draw = (q, k, buf) =>
            {
                float a = 1 - k * k;
                NQuang(Front, 6.6f, q.pos, 2.4f * sz * a, 0.8f * a, 1.4f, 0, 0, sdd, pal);
                NDot(Front, 6.62f, q.pos, sz * a, 2, 1, null, pal);
            };
            Add(p);
        }

        // giọt nước trôi quanh cầu (Dots / ExtraDots)
        void GiotMa(Vector2 c, float R)
        {
            float an = U(0, 6.283f);
            var d = new Vector2(Mathf.Cos(an), Mathf.Sin(an));
            var v = d * U(30, 80);
            float rd = Mathf.Clamp(U(0.04f, 0.07f) * R, 2, 5);
            NFbPhat(Front, 6.0f, c + d * (U(0.6f, 1.2f) * R), v, U(0.5f, 1.0f), NFb.Giot, rd * 1.6f, rd, NAng(v), 0.35f, 0.1f, 0, false, 60, 0.5f, 0, 0.6f, null, 0.8f,
                HatNuocFx.PalMa);
        }

        // NỔ cầu ma thủy tại thân đối thủ: quầng sáng bừng + quầng tối, chớp kem + chớp hướng; cầu nước xanh ngọc phồng đủ cỡ ~0,08 s rồi vỡ lấm
        // tấm (mờ 0,55: thấy đối thủ; mẫu KR5 đỉnh ở khung 1–3); toé lớn + gai sắc + toé sao bắn đều; vành sóng chấn; lưỡi liềm xoáy văng; chùm
        // giọt và hạt sáng toả; vệt xoáy văng; toé đất, vòng gợn, vũng; nhịp trúng phụ 0,16 s sau
        void MaNo(Vector2 c, float R, float tH, Vector2 foeFeet)
        {
            const int pal = HatNuocFx.PalMa;
            float sd = NSeed();
            Shake?.Invoke(0.8f);
            FlashScreen?.Invoke(FlashW);
            NP(Front, 0.3f, (q, a) =>
            {
                float k = a / 0.3f;
                NQuang(Back, 5.0f, c, Mathf.Lerp(1.0f, 1.6f, EaseOut(k)) * tH, 0.5f * (1 - k), 1.5f, 1, 0.2f, sd + 20, pal);
                NQuang(Front, 6.68f, c, Mathf.Lerp(0.6f, 1.25f, EaseOut(k)) * tH, 0.95f * (1 - k * k), 1.2f, 0, 0.25f, sd + 21, pal);
            });
            NFbPhat(Front, 6.6f, c, Vector2.zero, 0.15f, NFb.ChopTron, 1.2f * tH, 1.9f * tH, U(0, 360), 0.3f, 0.22f, 0, false, 0, 0, 0, 0, null, 0.8f, pal);
            NFbPhat(Front, 6.55f, c, Vector2.zero, 0.16f, NFb.ChopHuong, 1.4f * tH, 2.0f * tH, U(0, 360), 0.3f, 0.15f, 0, false, 0, 0, 0, 0, null, 0.8f, pal);
            NP(Front, 0.3f, (q, a) =>
            {
                float k = a / 0.3f;
                float r = Mathf.Lerp(R, 0.9f * tH, EaseOut(Mathf.Min(1, a / 0.08f)));
                NBall(Front, 6.2f, c, r, 0.55f, 0.02f + 0.95f * SmoothStep(0.15f, 1, k), 0.12f, 0.6f, sd, null, 1, pal);
            });
            GSplash(c, 1.15f, foeFeet.y, tH, Front, null);
            for (int j = 0; j < 8; j++)
            {
                float an = 360f * (j + U(0, 0.6f)) / 8;
                var d = NHuong(an);
                float w = U(0.55f, 0.85f) * tH;
                NFbPhat(Front, 6.45f, c + d * (0.3f * tH), d * U(260, 480), U(0.22f, 0.3f), NFb.GaiTrung, w, w * 1.2f, an, 0.32f, 0.05f, 0, false, 0, 3, 0, 0.55f,
                    null, 0.8f, pal);
            }
            for (int j = 0; j < 3; j++)
            {
                float an = 120f * j + U(-20, 20);
                var d = NHuong(an);
                float w = U(0.9f, 1.2f) * tH;
                NFbPhat(Front, 6.42f, c + d * (0.3f * w), d * U(60, 120), U(0.26f, 0.32f), NFb.ToeNgangC, 0.8f * w, w, an + 180, 0.3f, 0.06f, 0, false, 0, 0, 0, 0,
                    null, 0.8f, pal);
            }
            NP(Front, 0.4f, (q, a) =>
            {
                float k = a / 0.4f, rr = Mathf.Lerp(0.4f, 1.5f, EaseOut(k)) * tH;
                NFbS(Front, 6.3f, c, 2 * rr, 1.8f * rr, 0, NFb.ChamDat, 2 + 10 * k, 0.3f, 1, sd + 2, 0.3f, 2, false, pal);
            });
            for (int j = 0; j < 3; j++)
                NFbPhat(Front, 6.4f, c, Vector2.zero, U(0.3f, 0.4f), NFb.ChemVong, 0.8f * tH, 1.9f * tH, U(0, 360), 0.3f, 0.1f, 0, U(0, 1) < 0.5f, 0, 0,
                    (U(0, 1) < 0.5f ? -1 : 1) * U(220, 360), 0, null, 0.8f, pal);
            for (int j = 0; j < 20; j++)
            {
                float an = 6.283f * (j + U(0, 0.7f)) / 20;
                var v = new Vector2(Mathf.Cos(an), Mathf.Sin(an) - 0.15f) * U(300, 600);
                float rd = U(2.8f, 4.8f);
                NFbPhat(Front, 6.0f, c + v.normalized * (0.25f * tH), v, U(0.4f, 0.6f), NFb.Giot, rd * 1.8f, rd, NAng(v), 0.35f, 0.12f, 0, false, 700, 0, 0, 0.6f,
                    null, 0.8f, pal);
            }
            for (int j = 0; j < 16; j++) HatMa(c, 0.3f * tH, 1);
            for (int j = 0; j < 5; j++)
            {
                var v = new Vector2(U(-1, 1), U(-1, 0.2f)).normalized * U(200, 380);
                float w = U(0.5f, 0.8f) * tH;
                NFbPhat(Front, 6.1f, c + v.normalized * (0.2f * tH), v, U(0.4f, 0.55f), NFb.Xoan, w, w * 1.1f, NAng(v), 0.3f, 0.08f, 0, U(0, 1) < 0.5f, 500, 1.5f,
                    U(-200, 200), 0.4f, null, 0.8f, pal);
            }
            GToe(foeFeet, 1.3f * tH, Front);
            NFbPhat(Floor, 2.1f, foeFeet + new Vector2(0, 2), Vector2.zero, 0.7f, NFb.ChamDat, 0.6f * tH, 2.3f * tH, 0, 0.3f, 0, 1, false, 0, 0, 0, 0.32f, null, 0.8f, pal);
            Puddle(foeFeet + new Vector2(0, 3), 34, 1.6f);
            At(0.16f, () =>
            {
                NuocPulse?.Invoke(0.6f);
                Shake?.Invoke(0.3f);
            });
        }

        // ================= Uyên Xà: Thủy xà / Chém nước =================
        // THỦY XÀ (mana): nước tụ giữa hai sừng (bảng UxSung của tia cũ); khung nhả: một con rắn nước (ống nước 4 lớp như tia Water Laser, dày ở
        // đầu thon về đuôi) trườn uốn lượn từ sừng tới đối thủ, đầu tròn có hai hàm lưỡi liềm há ra; tới nơi hai hàm NGOẠM khép vào thân đối
        // thủ, toé lớn; thân rắn trôi nốt vào rồi tan
        public float NThuyXa(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NTiaNuoc(false, casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
            float dir = foeFeet.x < casterFeet.x ? -1 : 1;
            Func<float, Vector2> sung = t => LechRig(mouth, casterFeet, casterH, foeFeet, DiemBang(UxSung, t), UxMzR);
            float T0 = Mathf.Max(0.2f, lead);
            var g0 = sung(T0);
            var dich = foeBody + new Vector2(-dir * 0.12f * tH, -0.05f * tH);
            float dist = (dich - g0).magnitude;
            float TT = Mathf.Clamp(dist / 1100f, 0.3f, 0.45f);
            float day = Mathf.Clamp(0.2f * casterH, 22, 44), amp = Mathf.Min(0.3f * tH, 0.16f * dist), sd = NSeed();
            const float TAN = 0.32f;
            Gather(sung, 0, T0 - 0.04f, 70, 55);
            var u = (dich - g0) / Mathf.Max(1, dist);
            var n = new Vector2(-u.y, u.x);
            Vector2 Than(float s, float a) => Vector2.Lerp(g0, dich, s) + n * (Mathf.Sin(s * Mathf.PI * 2.4f - a * 11) * amp * Mathf.Sin(Mathf.PI * Mathf.Clamp01(s)));
            NP(Front, T0 + TT + TAN + 0.05f, (q, a) =>
            {
                if (a < T0) return;
                float x = (a - T0) / TT;
                float s1 = Mathf.Min(1, EaseOut(Mathf.Min(1, x)) * 1.02f);
                float s0 = x < 0.55f ? 0 : Mathf.Min(1, (x - 0.55f) / 0.75f);
                if (a > T0 + TT) s0 = Mathf.Max(s0, Mathf.Clamp01((a - T0 - TT) / TAN));
                if (s1 - s0 < 0.02f) return;
                float cut = a > T0 + TT ? 0.1f + 0.7f * Mathf.Clamp01((a - T0 - TT) / TAN) : 0;
                nPts.Clear();
                nHw.Clear();
                const int N = 28;
                for (int i = 0; i <= N; i++)
                {
                    float s = Mathf.Lerp(s0, s1, i / (float)N), f = i / (float)N;      // f: 0 đuôi → 1 đầu
                    nPts.Add(Than(s, a));
                    float w = 0.5f * day * (0.28f + 0.72f * Mathf.Pow(f, 0.7f));
                    if (f > 0.9f) w *= 0.55f + 0.45f * (1 - f) / 0.1f;                  // cổ thon trước đầu tròn
                    nHw.Add(w * (1 + 0.07f * Mathf.Sin(s * 19 - a * 15)));
                }
                NTubePrep();
                NTube(Front, 3.82f, 3, 1.2f, 1.4f, Mathf.Max(cut, 0.05f), sd);
                NTube(Front, 4.0f, 0, 1f, 2.0f, cut, sd + 3);
                NTube(Front, 4.12f, 1, 0.55f, 2.6f, cut, sd + 7);
                NTube(Front, 4.2f, 2, 0.78f, 3.2f, cut, sd + 11);
                if (a < T0 + TT + 0.02f) // đầu rắn: khối nước tròn + hai hàm lưỡi liềm há
                {
                    var h = Than(s1, a);
                    var tg = Unit(Than(s1, a) - Than(Mathf.Max(0, s1 - 0.04f), a));
                    NBall(Front, 6, h, 0.62f * day, 1, 0, 0.06f, 0.4f, sd, tg, 1.3f);
                    float ha = 28 + 14 * Mathf.Sin(a * 22);
                    for (int j = -1; j <= 1; j += 2)
                        NFbS(Front, 6.2f, h + tg * (0.35f * day) + new Vector2(-tg.y, tg.x) * (j * 0.28f * day), 1.15f * day, 1.15f * day,
                            NAng(tg) + j * ha + (j > 0 ? 0 : 180), NFb.ChemVong, 2, 0.32f, 1, sd + j, 0.18f, 0, j < 0);
                }
            });
            AtW(T0, () =>
            {
                Shake?.Invoke(0.22f);
                NFbPhat(Front, 5.6f, g0 + u * (0.4f * day), u * 40, 0.2f, NFb.ChopHuong, 1.4f * day, 1.9f * day, NAng(u), 0.3f, 0.12f);
            });
            AtW(T0 + TT, () => // NGOẠM: hai hàm lưỡi liềm khép vào thân đối thủ
            {
                Shake?.Invoke(0.45f);
                for (int j = -1; j <= 1; j += 2)
                {
                    int jj = j;
                    var c0 = dich + n * (jj * 0.75f * day);
                    NFbDoan(Front, 6.3f, t => Vector2.Lerp(c0, dich + n * (jj * 0.12f * day), EaseOut(Mathf.Min(1, t / 0.09f))), 0.22f, NFb.ChemVong, 1, 6,
                        2.2f * day, 2.6f * day, NAng(u) + jj * 70 + (jj > 0 ? 0 : 180), 0.3f, 0.15f, 0, jj < 0);
                }
                NFbPhat(Front, 6.2f, dich, Vector2.zero, 0.15f, NFb.ChopTron, 2.2f * day, 3.2f * day, U(0, 360), 0.3f, 0.2f);
                GSplash(dich, 0.95f, foeFeet.y, tH, Front, u);
                Puddle(foeFeet + new Vector2(0, 3), 24, 1.3f);
            });
            return T0 + TT;
        }

        // CHÉM NƯỚC (chiêu cuối, lúc chạm: đuôi sừng quất liên tiếp, "vệt chém riêng chưa làm"): ba lưỡi chém nước (MainSlash + vệt sáng
        // HighlightSlash) xéo đổi chiều cách nhau 0,09 s ngay trên thân đối thủ, mỗi nhát chớp hướng + toé nhỏ + giọt; nhát cuối toé lớn
        public float NXaChem(Vector2 casterFeet, Vector2 foeBody, Vector2 foeFeet, float tH)
        {
            if (!NS) return NVa(foeBody, foeFeet, tH, new Vector2(Mathf.Sign(foeFeet.x - casterFeet.x), 0));
            float dir = foeFeet.x < casterFeet.x ? -1 : 1;
            float[] goc = { 28, -34, 8 };
            for (int i = 0; i < 3; i++)
            {
                int ii = i;
                bool cuoi = i == 2;
                AtW(0.09f * i, () =>
                {
                    float an = (dir > 0 ? 0 : 180) + goc[ii] * dir + U(-6, 6);
                    var d = NHuong(an);
                    var c = foeBody + new Vector2(U(-0.08f, 0.08f), U(-0.12f, 0.08f)) * tH;
                    // lưỡi chém là cung lưỡi liềm quét (ChemVong khung 0 → 9) — lần chụp đầu dùng dải Chem mảnh, bị thân Uyên Xà đang lao sát
                    // che gần hết, chỉ còn mảnh toé; cung to 1,6 tH + vệt sáng trắng dọc lưỡi
                    NFbDoan(Front, 6.3f, _ => c, 0.24f, NFb.ChemVong, 0, 9, 1.45f * tH, 1.7f * tH, an + 90 * (ii % 2 == 0 ? 1 : -1), 0.3f, 0.1f, 0, ii % 2 == 1);
                    NFbPhat(Front, 6.35f, c - d * (0.2f * tH), d * 560, 0.16f, NFb.VetSang, 1.5f * tH, 1.8f * tH, an, 0.3f, 0.3f, 2, dir < 0);
                    NFbPhat(Front, 6.1f, c, Vector2.zero, 0.13f, NFb.ChopHuong, 0.8f * tH, 1.1f * tH, an, 0.3f, 0.14f);
                    if (cuoi)
                    {
                        GSplash(c, 1.15f, foeFeet.y, tH, Front, new Vector2(dir, 0));
                        Puddle(foeFeet + new Vector2(0, 3), 26, 1.4f);
                    }
                    else GTrung(c, 0.5f * tH, new Vector2(dir, 0), Front);
                    for (int j = 0; j < 6; j++)
                    {
                        var v = (d * U(160, 360) + new Vector2(U(-80, 80), -U(40, 160)));
                        float rd = U(2.4f, 4f);
                        NFbPhat(Front, 5.9f, c + U2(-8, 8), v, U(0.35f, 0.5f), NFb.Giot, rd * 1.8f, rd, NAng(v), 0.35f, 0.1f, 0, false, 900, 0, 0, 0.6f);
                    }
                    Shake?.Invoke(cuoi ? 0.6f : 0.25f);
                    if (ii > 0) NuocPulse?.Invoke(cuoi ? 0.75f : 0.4f);
                });
            }
            BackColumn(foeFeet, tH);
            return 0;
        }

        // ================= Hàn Ngạc: Siêu bão xoáy =================
        // vòi rồng nước dựng dưới chân đối thủ (NVoi) + vòng xoáy lớn quanh thân (XoayO ở ba độ cao, nửa sau ở lớp sau), mảnh băng trắng bay
        // vòng quanh phễu, vệt nước bị hút xoắn từ hai bên vào chân phễu, mưa gió quất ngang; dạng 1 (nhe) ít lớp hơn
        public float NBaoXoay(Vector2 foeFeet, float tH, float lead, bool nhe)
        {
            float t = NVoi(foeFeet, tH, lead);
            if (!NS) return t;
            float TA = Mathf.Max(0.12f, lead - 0.1f), T1 = TA + 1.65f;
            float sd = NSeed(), HT = Mathf.Min(1.27f * tH, foeFeet.y - 24);
            int nTang = nhe ? 2 : 3;
            for (int k = 0; k < nTang; k++) // vòng xoáy lớn quanh phễu: mỗi tầng hai nửa (sau / trước)
            {
                float hh = 0.25f + 0.3f * k;
                for (int side = 0; side < 2; side++)
                {
                    int sdd = side;
                    float kk = k;
                    AtW(TA + 0.12f + 0.06f * k, () => NP(sdd == 0 ? Back : Front, T1 - TA - 0.1f, (q, a) =>
                    {
                        float grow = EaseOut(Mathf.Min(1, a / 0.25f)) * (1 - SmoothStep(T1 - TA - 0.45f, T1 - TA - 0.12f, a));
                        float w = (1.25f + 0.6f * hh) * tH * grow * (nhe ? 0.82f : 1);   // lần chụp đầu 0,95 + 0,5 hh: lẫn vào phễu
                        if (w < 4) return;
                        var c = foeFeet + new Vector2(0.06f * tH * Mathf.Sin(a * 6 + kk), -hh * HT);
                        float fr = (a * 22 + kk * 5) % NuocFbBang.Get(NFb.XoayO).frames;
                        NFbS(sdd == 0 ? Back : Front, sdd == 0 ? 3.4f : 4.6f, c, w, w * 0.34f, sdd == 0 ? 180 : 0, NFb.XoayO, fr, 0.3f, 1, sd + kk * 3 + sdd, 0.06f, 0,
                            sdd == 0);
                    }));
                }
            }
            // mảnh băng trắng bay vòng quanh phễu (gai sắc tô toàn bọt trắng), vòng nghiêng: nửa sau ở lớp sau
            int nBang = nhe ? 5 : 9;
            for (int i0 = 0; i0 < nBang; i0++)
            {
                int i = i0;
                float ph = 6.283f * i / nBang, hh = U(0.15f, 0.95f), sp = U(5, 7.5f);
                AtW(TA + 0.2f + 0.03f * i, () =>
                {
                    float life = T1 - TA - 0.25f;
                    for (int side = 0; side < 2; side++)
                    {
                        int sdd = side;
                        NP(sdd == 0 ? Back : Front, life, (q, a) =>
                        {
                            float th = ph + a * sp, cs = Mathf.Cos(th), sn = Mathf.Sin(th);
                            if ((sn > 0) != (sdd == 1)) return;
                            float r = (0.35f + 0.55f * hh) * tH * EaseOut(Mathf.Min(1, a / 0.3f));
                            var c = foeFeet + new Vector2(cs * r, -hh * HT + sn * 0.22f * r);
                            // mảnh băng: gai sắc tô bảng Kim (thép → bạc → kem, dải cel) cho tách khỏi nước lam; lần chụp đầu tô toàn bọt trắng
                            // 0,2 tH thì lẫn vào vệt gió
                            float w = 0.3f * tH * (0.8f + 0.3f * sn) * (1 - SmoothStep(life - 0.25f, life, a));
                            NFbS(sdd == 0 ? Back : Front, sdd == 0 ? 3.5f : 4.7f, c, w, w * 1.1f, th * 57.3f + 90, NFb.GaiTrung, (i % 4), 0.3f, 1, sd + i, 0.1f, 0,
                                false, HatNuocFx.PalKim);
                        });
                    }
                });
            }
            // xoáy dẹt trên đỉnh phễu (mắt bão): lưỡi liềm chém vòng ép dẹt quay chậm, hai lớp lệch pha
            AtW(TA + 0.2f, () => NP(Front, T1 - TA - 0.3f, (q, a) =>
            {
                float grow = EaseOut(Mathf.Min(1, a / 0.3f)) * (1 - SmoothStep(T1 - TA - 0.6f, T1 - TA - 0.3f, a));
                float w = 1.7f * tH * grow * (nhe ? 0.8f : 1);
                if (w < 4) return;
                var c = foeFeet + new Vector2(0, -1.02f * HT);
                NFbS(Front, 4.65f, c, w, w * 0.3f, a * 210, NFb.ChemVong, 2, 0.3f, 1, sd + 31, 0.08f);
                NFbS(Back, 3.45f, c + new Vector2(0, -0.04f * tH), 0.8f * w, 0.24f * w, 140 - a * 170, NFb.ChemVong, 3, 0.32f, 1, sd + 37, 0.02f);
            }));
            // nước bị hút xoắn từ hai bên vào chân phễu
            EveryW(TA, T1 - 0.2f, nhe ? 6 : 10, x =>
            {
                float s = U(0, 1) < 0.5f ? -1 : 1;
                var p0 = foeFeet + new Vector2(s * U(0.9f, 1.3f) * tH, U(-0.1f, 0.05f) * tH);
                float w = U(0.5f, 0.75f) * tH;
                NFbPhat(U(0, 1) < 0.5f ? Front : Back, 3.0f, p0, new Vector2(-s * U(260, 380), -U(10, 60)), U(0.35f, 0.45f), NFb.SongTruot, w * 0.9f, w * 0.6f, 0, 0.3f,
                    0.04f, 0, s > 0);
            });
            // mưa gió quất ngang
            EveryW(TA + 0.1f, T1, nhe ? 22 : 36, x =>
            {
                var p = foeFeet + new Vector2(U(-1.4f, 1.4f) * tH, -U(0.1f, 1.3f) * tH);
                var v = new Vector2(U(520, 720) * (U(0, 1) < 0.5f ? 1 : -1) * 0.2f + 600, U(280, 420));
                float rd = U(2f, 3.2f);
                NFbPhat(U(0, 1) < 0.5f ? Front : Back, 5.8f, p, v, U(0.22f, 0.32f), NFb.Giot, rd * 5f, rd * 4f, NAng(v), 0.35f, 0.12f, 0, false, 0, 0, 0, 0.32f, null, 0.85f);
            });
            return t;
        }

        // ================= Hải Long: Loạt thủy cầu =================
        // Mỗi đầu nhả một cầu nước đúng lúc đầu đó vươn ra trong clip cast (đo trên .atomik bằng ArtGen/Spine/mo_xe/atomik_dang.py, xương
        // mieng_<k>, phần chiều cao game, x tới trước, y lên, gốc chân; giờ vươn tính theo giây clip, trúng khai 1,0 s): dạng 1 một đầu, dạng 2
        // ba đầu, dạng 3 năm đầu. Dạng phân bằng chỗ bắn của rig (game.muzzle): dạng 3 x ≈ 0,21; dạng 1 / 2 x ≈ 0,42, y 0,576 / 0,625.
        static readonly Vector2 HlMz1 = new Vector2(0.424f, 0.576f), HlMz2 = new Vector2(0.413f, 0.625f), HlMz3 = new Vector2(0.207f, 0.626f);
        static readonly Vector2[] HlDau1 = { new Vector2(0.49f, 0.545f) };
        static readonly float[] HlGio1 = { 1.0f };
        static readonly Vector2[] HlDau2 = { new Vector2(0.475f, 0.62f), new Vector2(0.777f, 0.462f), new Vector2(0.004f, 0.566f) };
        static readonly float[] HlGio2 = { 1.0f, 1.15f, 1.2f };
        static readonly Vector2[] HlDau3 =
            { new Vector2(0.208f, 0.63f), new Vector2(0.457f, 0.457f), new Vector2(0.56f, 0.307f), new Vector2(-0.134f, 0.594f), new Vector2(-0.197f, 0.374f) };
        static readonly float[] HlGio3 = { 1.0f, 1.05f, 1.15f, 1.2f, 1.25f };

        public float NLoatCau(Vector2 casterFeet, float casterH, Vector2 mouth, Vector2 foeBody, Vector2 foeFeet, float tH, float lead)
        {
            if (!NS) return NTiaNuoc(false, casterFeet, casterH, mouth, foeBody, foeFeet, tH, lead);
            float dir = foeFeet.x < casterFeet.x ? -1 : 1, H = Mathf.Max(1, casterH);
            float mzX = (mouth.x - casterFeet.x) * dir / H, mzY = (casterFeet.y - mouth.y) / H;
            int dang = mzX < 0.31f ? 3 : mzY > 0.6f ? 2 : 1;
            var dau = dang == 3 ? HlDau3 : dang == 2 ? HlDau2 : HlDau1;
            var gio = dang == 3 ? HlGio3 : dang == 2 ? HlGio2 : HlGio1;
            var mz = dang == 3 ? HlMz3 : dang == 2 ? HlMz2 : HlMz1;
            float k = Mathf.Max(0.3f, lead) / 1.0f;
            float tHit0 = 0;
            for (int i = 0; i < dau.Length; i++)
            {
                int ii = i;
                bool chinh = i == 0;
                var g = LechRig(mouth, casterFeet, casterH, foeFeet, dau[i], mz);
                var aim = foeBody + new Vector2(-dir * 0.08f * tH + U(-0.12f, 0.12f) * tH, U(-0.16f, 0.1f) * tH);
                float T0 = gio[i] * k, TT = Mathf.Clamp((aim - g).magnitude / 1300f, 0.24f, 0.4f);
                float rc = Mathf.Clamp((chinh ? 0.085f : 0.065f) * casterH, 12, chinh ? 26 : 20);
                float arc = U(20, 55);
                Vector2 Path(float t)
                {
                    if (t < T0) return g;
                    float x = Mathf.Min(1, (t - T0) / TT);
                    return Vector2.Lerp(g, aim, x) + new Vector2(0, -4 * arc * x * (1 - x));
                }
                if (chinh) tHit0 = T0 + TT;
                // cầu hiện ở miệng ngay trước lúc đầu vươn (0,12 s), phóng theo cú vươn
                NCauShader(Path, T0 + TT, a => a < T0 - 0.12f ? 0 : rc * EaseOut(Mathf.Clamp01((a - T0 + 0.12f) / 0.1f)) * (1 - SmoothStep(T0 + TT - 0.03f, T0 + TT, a)),
                    null, T0, Front, T0);
                AtW(T0, () =>
                {
                    var u = Unit(aim - g);
                    NFbPhat(Front, 5.4f, g + u * (0.6f * rc), u * 40, 0.2f, NFb.ToeNgangC, 1.4f * rc, 1.9f * rc, NAng(u) + 180, 0.3f, 0.06f);
                    Shake?.Invoke(chinh ? 0.22f : 0.1f);
                });
                AtW(T0 + TT, () =>
                {
                    var u = Unit(aim - g);
                    if (chinh || ii == dau.Length - 1) GSplash(aim, chinh ? 0.85f : 0.75f, foeFeet.y, tH, Front, u);
                    else GTrung(aim, 0.5f * tH, u, Front);
                    Shake?.Invoke(chinh ? 0.35f : 0.18f);
                    if (!chinh) NuocPulse?.Invoke(ii == dau.Length - 1 ? 0.6f : 0.35f);
                    if (ii == dau.Length - 1) Puddle(foeFeet + new Vector2(0, 3), 26, 1.4f);
                });
            }
            return tHit0;
        }
    }
}
