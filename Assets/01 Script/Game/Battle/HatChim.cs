// Đồ dùng chung tách ra từ bộ Linh Điểu cũ (chim bảo hộ rừng, suất gio_loc 2026-11-12; suất nay là Cổ Vương, chiêu ở HatCoVuong.cs):
// tảng đá rừng phủ rêu (Thach, DrawThach, ThachNo: Cổ Vương), sợi gió (SoiGio: Voọc Tướng HatKiem.cs, Sói Giáp HatSoi.cs), khung tảng
// ThachU (bộ Thổ HatTho.cs). Ba chiêu riêng của chim (đâm mỏ, lá găm, thiên thạch) đã bỏ cùng tướng.
// Biến tĩnh ở file này không dùng biến tĩnh của HatLua.cs lúc khởi tạo.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        static readonly Color ThachC = C(154, 150, 138), ThachC2 = C(102, 98, 90), ThachC3 = C(190, 186, 172); // xám đá của đuôi chim: giữa, sẫm, mặt sáng
        static readonly Color GioC = C(246, 250, 240); // sợi gió trắng ngà

        // tảng đá rừng: bốn khối tròn lệch nhau chung một viền mực (mọi viền nằm dưới mọi khối nên hình bóng gồ ghề liền một nét): thân
        // xám, một khối sẫm phía dưới, một khối nhạt phía trên; reu: mảng rêu lục trùm đỉnh. Xoay; có ground thì nảy một lần rồi nằm lại
        static readonly Vector3[] ThachU = { new Vector3(0, 0, 1f), new Vector3(0.5f, 0.24f, 0.66f), new Vector3(-0.52f, 0.28f, 0.6f), new Vector3(0.08f, -0.4f, 0.62f) };

        void DrawThach(P q, float k, List<Item> buf)
        {
            float r = q.sz * (1 - SmoothStep(0.72f, 1, k));
            if (r < 1.2f) return;
            int sd = q.seed & 3, g = q.group;
            float a = q.ang;
            float rad = -a * Mathf.Deg2Rad;
            Vector2 Rot(float x, float y) => new Vector2(x * Mathf.Cos(rad) - y * Mathf.Sin(rad), x * Mathf.Sin(rad) + y * Mathf.Cos(rad)) * r;
            float ink = Mathf.Min(4.5f, 2.2f + r * 0.1f);
            int n = r < 6 ? 2 : 4;
            for (int i = 0; i < n; i++)
            {
                var u = ThachU[i];
                var c = q.pos + Rot(u.x, u.y);
                float d = 2 * r * u.z;
                int si = (sd + i) & 3;
                Put(buf, g, q.ph, S("solid_" + si), Ink, c, d + ink, 1, a + i * 50);
                Put(buf, g, q.ph + 0.1f + i * 0.02f, S("blob_" + si), i == 1 ? ThachC2 : i == 3 ? ThachC3 : ThachC, c, d, 1, a + i * 50);
            }
            if (!q.crust || r < 5) return;
            var cr = q.pos + Rot(-0.04f, -0.66f);
            Put(buf, g, q.ph, S("solid_" + ((sd + 2) & 3)), Ink, cr, 0.92f * r + ink, 1.7f, a);
            Put(buf, g, q.ph + 0.3f, S("blob_" + ((sd + 2) & 3)), q.stops[1], cr, 0.92f * r, 1.7f, a);
            Put(buf, g, q.ph + 0.4f, S("blob_" + ((sd + 3) & 3)), q.stops[2], q.pos + Rot(-0.12f, -0.76f), 0.46f * r, 1.8f, a);
        }

        P Thach(Vector2 pos, Vector2 vel, float life, float r, float ground = float.NaN, int group = Front, bool reu = false)
        {
            var p = new P
            {
                pos = pos, vel = vel, life = life, acc = new Vector2(0, 1300), spin = U(-420, 420), spinDrag = 0.6f, ang = U(0, 360), seed = rng.Next(8),
                sz = r, group = group, ground = ground, bounce = 0.34f, crust = reu, stops = W, ph = 44
            };
            p.draw = DrawThach;
            return Add(p);
        }

        // sợi gió: vệt trắng mảnh bay thẳng, hiện rồi tan
        P SoiGio(Vector2 pos, Vector2 vel, float life, float sz, int group = Front)
        {
            var p = new P { pos = pos, vel = vel, life = life, seed = rng.Next(2), sz = sz, group = group, col = GioC, drag = 1.2f };
            p.draw = (q, k, buf) =>
            {
                float a = 1 - Mathf.Abs(2 * k - 1);
                if (a < 0.05f) return;
                Put(buf, q.group, 38, S("streakg_" + (q.seed & 1)), q.col, q.pos, q.sz, Mathf.Clamp(q.vel.magnitude / 80, 2.4f, 5f), VelAng(q.vel),
                    Mathf.Min(1, a * 1.7f));
            };
            return Add(p);
        }

        // đá vỡ to: chớp toé, tảng con văng rồi nảy trên đất, dăm đá, bụi
        void ThachNo(Vector2 c, Vector2 foeFeet, float tH, float R, float dir)
        {
            BurstFlash(c, 0.7f * tH);
            for (int i = 0; i < 7; i++)
            {
                float a = (-90 + (i - 3) * 34 + U(-10, 10)) * Mathf.Deg2Rad; // nửa trên, rải đều
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                Thach(c + d * U(4, 0.4f * R), new Vector2(d.x * U(200, 420) + dir * 60, d.y * U(260, 520)), U(1.0f, 1.4f), R * U(0.22f, 0.4f), foeFeet.y + U(-10, 18),
                    (i & 1) == 0 ? Front : Back, (i % 3) == 0);
            }
            for (int i = 0; i < 12; i++)
            {
                float a = 6.28f * (i + U(0, 0.8f)) / 12;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.35f);
                DaVun(c + d * U(4, 14), d * U(220, 460), U(0.45f, 0.8f), U(3.2f, 5.6f));
            }
            for (int i = 0; i < 6; i++) Bui(c + U2(-0.5f, 0.5f) * R, U2(-90, 90) + new Vector2(0, -50), U(0.5f, 0.8f), 6, U(14, 22), i < 4 ? Back : Front);
        }
    }
}
