# -*- coding: utf-8 -*-
"""Sinh Assets/01 Script/Game/Battle/HatXich.cs (lớp hạt của quỷ xích, suất khien_bac đảo Kim) = khung C# dưới đây + bảng số đo trên rig hai
dạng (quy_xich_do_hat.py chạy cho QX_DANG=non và dạng 2). Đổi clip, tỉ lệ hay hình rig thì xuất rig lại rồi chạy file này.

    py -3 -I ArtGen/Spine/quy_xich_hat_cs.py
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RA = os.path.join(ROOT, "Assets", "01 Script", "Game", "Battle", "HatXich.cs")

KHUNG = r'''// Bộ QUỶ XÍCH (2026-11-16, quỷ béo mặc giáp, móc nối xích sắt, suất khien_bac ải 20 đảo Kim; rig ArtGen/Spine/quy_xich_rig.py (rig gốc
// monster_3408): dạng 1 non quy_xich_1 (QX_DANG=non), dạng 2 quy_xich_2; ghi chú ArtGen/Spine/inbox/quy_xich_ghichu.md).
// Người dùng: đánh thường "bay tới dùng móc gõ vào đầu đối thủ" (tướng lao tới); chiêu mana "quay xích ném đối thủ" (móc + xích là mảnh của
// rig trên xương fly_*, game lái tới đối thủ); chiêu cuối "xích sắt bốc lửa, xoay xích tạo ra trail lửa và khói, ném trói đối thủ sau đó thiêu
// đốt; thêm 1 cột lửa rất to thiêu cháy đối thủ". Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc), phát lúc clip BẮT ĐẦU; mốc là giây clip
// của rig, co theo `lead` (giờ trúng của clip):
// - n_xich_go (đòn thường): móc gõ đỉnh đầu đối thủ: chớp sắt, tia toé, dăm thép; móc đập xuống: bụi dưới chân đối thủ.
// - n_xich_nem1 / n_xich_nem (chiêu mana): vệt gió kim loại theo đúng đường móc quay, tia + bụi lúc ném, móc găm: chớp, vòng sóng, dăm, rung;
//   móc giật ra: tia, dăm; móc về tay: chớp nhỏ.
// - n_xich_lua1 / n_xich_lua (chiêu cuối): `lua_xich` móc bốc lửa; lúc quay: vệt lửa + khói theo đúng đường móc quay, lửa liếm dọc xích; ném:
//   lửa chạy dọc xích từ tay tới đối thủ; `troi`: VÒNG XÍCH quấn quanh thân đối thủ (ảnh mắt xích của rig: Resources/quy_xich_2/
//   quy_xich_2_tt_xich_<1|2>.png), nóng đỏ dần, lửa liếm vòng xích, xích căng cháy; `cot_lua`: CỘT LỬA rất to bốc từ chân đối thủ (cao tới gần
//   mép trên màn, tối đa 2,4 lần thân), vòng lửa + khe nứt dưới đất, khói đen ở đỉnh, than; bốn nhịp `chay`: nổ lửa trên thân; `tha`: vòng
//   xích rơi, lửa dọc xích tắt dần theo xích rút về, khói.
// Điểm trên rig (đầu móc khi quay, ba điểm giữa xích dài, chỗ xích nối tay) là bảng số đo theo khung 30 / giây (phần của chiều cao KHAI cho
// game, x về phía trước, y lên): đổi clip hay tỉ lệ rig thì đo lại và sinh lại file này (ArtGen/Spine/quy_xich_hat_cs.py). FILE SINH TỰ ĐỘNG.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // mốc clip (giây) của rig: attack / cast / skill
        const float XqDt = 1f / 30f;
        const float XqALead = 0.775f;
        const float XqCLead = 0.895f, XqCQuay = 0.20f, XqCNem = 0.733f, XqCRut = 1.07f, XqCVe = 1.267f;
        const float XqSLead = 1.732f, XqSLua = 0.10f, XqSNem = 1.022f, XqSTroi = 1.182f, XqSCot = 1.582f, XqSTha = 2.682f, XqSRut = 2.882f;
        static readonly Color XqThep = C(170, 174, 184), XqNong = C(255, 150, 70), XqGio = C(236, 238, 244);

/*BANG*/

        sealed class XqBang
        {
            public float[] mx, my, ax, ay, bx, by, cx, cy, tx, ty;
            public byte[] mh;
        }

/*LAY*/

        static Vector2 XqMau(float[] xs, float[] ys, float t)
        {
            float f = Mathf.Max(0, t) / XqDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            float w = Mathf.Clamp01(f - i);
            return new Vector2(Mathf.Lerp(xs[i], xs[j], w), Mathf.Lerp(ys[i], ys[j], w));
        }

        static bool XqHien(byte[] h, float t) => h[Mathf.Clamp(Mathf.RoundToInt(Mathf.Max(0, t) / XqDt), 0, h.Length - 1)] != 0;

        // ảnh mắt xích của rig (AolaImport nhập tên có "_tt_" thành sprite: Resources/quy_xich_2/quy_xich_2_tt_xich_<i>.png), nạp một lần
        static readonly Dictionary<string, Sprite> xqAnh = new Dictionary<string, Sprite>();

        static Sprite XqXich(int i)
        {
            string key = "quy_xich_2_tt_xich_" + i;
            if (xqAnh.TryGetValue(key, out var s) && s) return s;
            s = Resources.Load<Sprite>("quy_xich_2/" + key);
            xqAnh[key] = s;
            return s;
        }

        // một lưỡi lửa của vệt móc quay: bay chậm theo móc rồi tụt lại, ngọn ngả ngược hướng bay
        void XqVet(Vector2 p, Vector2 v, float manh, int g)
        {
            var q = Flame(p + U2(-4, 4), v * 0.12f + new Vector2(U(-30, 30), -U(40, 120)), U(0.22f, 0.34f), U(8, 11) * manh, U(18, 26) * manh, "tron",
                Th.pal, g, 3f, -260, 1.7f, 0.04f, 0.05f);   // khói của vệt nay là cụm liền riêng (NXichLua), lưỡi lửa ít nhả khói lẻ
            Tongue(q, -1, 0.45f);
            q.smokeGroup = Back;
        }

        // lưỡi lửa nhỏ liếm lên (dọc xích, quanh vòng trói)
        void XqLiem(Vector2 p, float manh, int g, float r = 1)
        {
            var q = Flame(p + U2(-3, 3), new Vector2(U(-25, 25), -U(70, 150)), U(0.18f, 0.28f), 5 * manh * r, U(10, 15) * manh * r, "tron", Th.pal, g, 3f,
                -300, 1.6f, 0.06f, 0.06f);
            Tongue(q, 1, 0.6f);
            q.smokeGroup = Back;
        }

        // ĐÒN THƯỜNG: tướng bay tới, móc gõ đỉnh đầu đối thủ rồi đập xuống. lead: giây từ đầu clip attack tới lúc móc chạm đầu.
        public float NXichGo(Vector2 casterFeet, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.02f, lead), k = t0 / XqALead;
            var dau = foeBody + new Vector2(-dir * 0.06f * tH, -0.34f * tH);
            At(t0, () =>
            {
                Shake?.Invoke(0.3f);
                SatChop(dau, 0.42f * tH, Front, 0.14f);
                for (int i = 0; i < 8; i++)
                    Spark(dau, new Vector2(dir * U(-0.3f, 0.9f), U(-0.9f, 0.6f)), U(240, 440), U(0.16f, 0.28f), U(6, 9), 500);
                for (int i = 0; i < 4; i++)
                    GiaoDam(dau + U2(-5, 5), new Vector2(dir * U(-0.2f, 0.9f), -U(0.2f, 1f)) * U(160, 320), U(10, 15));
            });
            At(t0 + 0.05f * k, () =>
            {
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(foeFeet + new Vector2(sd * U(6, 0.3f * tH), U(-5, 2)), new Vector2(sd * U(100, 240), -U(10, 50)), 0, 4, 11, Back);
                }
            });
            return t0;
        }

        // CHIÊU MANA: quay xích qua đầu rồi ném móc (móc + xích là mảnh của rig, game lái). dang: 1 / 2; manh: 0,85 dạng 1, 1 dạng 2.
        public float NXichNem(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.3f, lead), k = t0 / XqCLead, T0 = T;
            var B = XqLay(dang, false);
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            float Tc() => (T - T0) / k;
            Vector2 Moc(float tc) => San(XqMau(B.mx, B.my, tc));
            // vệt gió kim loại theo đúng đường móc quay
            Every(XqCQuay * k, XqCNem * k, 34, x =>
            {
                float tc = Tc();
                if (!XqHien(B.mh, tc)) return;
                var v = (Moc(tc + XqDt) - Moc(tc - XqDt)) / (2 * XqDt * k);
                if (v.sqrMagnitude < 100) return;
                var p = Spark(Moc(tc), -v, U(60, 140), U(0.1f, 0.16f), U(6, 9) * manh, 0, Back, 6);
                p.col = XqGio;
            });
            At(XqCNem * k, () =>
            {
                var a = San(XqMau(B.tx, B.ty, XqCNem));
                for (int i = 0; i < 6; i++) Spark(a, new Vector2(dir * U(0.4f, 1f), U(-0.5f, 0.3f)), U(220, 420), U(0.12f, 0.22f), U(5, 8), 100);
                Bui(casterFeet + new Vector2(-dir * U(4, 0.12f * casterH), U(-4, 2)), new Vector2(-dir * U(80, 180), -U(10, 40)), 0, 4, 10, Back);
            });
            var c = foeBody + new Vector2(-dir * 0.05f * tH, 0);
            At(t0, () =>
            {
                Shake?.Invoke(0.3f * manh);
                GiaoTrung(c, new Vector2(dir, 0), tH, 1.1f * manh, 9, 6);
                Ring(c, 0.34f, 0.06f * tH, 0.55f * tH * manh, XqThep, 0.5f, Front, 32);
                for (int i = 0; i < 3; i++) Bui(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, U(-4, 2)), new Vector2(U(-120, 120), -U(10, 60)), 0, 4, 11, Back);
            });
            At(XqCRut * k, () =>
            {
                for (int i = 0; i < 6; i++) Spark(c, new Vector2(-dir * U(0.3f, 1f), U(-0.6f, 0.3f)), U(200, 380), U(0.12f, 0.22f), U(5, 8), 300);
                for (int i = 0; i < 3; i++) GiaoDam(c + U2(-5, 5), new Vector2(-dir * U(0.2f, 0.8f), -U(0.3f, 1f)) * U(140, 280), U(9, 13));
            });
            At(XqCVe * k, () =>
            {
                var a = San(XqMau(B.tx, B.ty, XqCVe));
                SatChop(a, 0.16f * casterH * manh, Front, 0.12f);
            });
            return t0;
        }

        // CHIÊU CUỐI: xích lửa quay, ném, trói, cột lửa thiêu. dang: 1 / 2; manh: 0,8 dạng 1, 1 dạng 2. Trả giây tới nhịp đốt đầu (= lead).
        public float NXichLua(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.3f, lead), k = t0 / XqSLead, T0 = T;
            var B = XqLay(dang, true);
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            float Tc() => (T - T0) / k;
            Vector2 Moc(float tc) => San(XqMau(B.mx, B.my, tc));
            Vector2 Tay(float tc) => San(XqMau(B.tx, B.ty, tc));
            Vector2 VMoc(float tc) => (Moc(tc + XqDt) - Moc(tc - XqDt)) / (2 * XqDt * k);
            var dich = foeBody;

            // 1. móc bốc lửa: chớp nhỏ, lưỡi lửa bùng
            At(XqSLua * k, () =>
            {
                var m = Moc(XqSLua);
                KmChop(m, 0.16f * casterH * manh, 0.06f, KmLua, Back);
                for (int i = 0; i < 6; i++) XqLiem(m, manh, Back, 1.4f);
            });
            // 2. quay (2026-11-18: người dùng chê khói, lửa rải rác, chưa thành cụm): vệt lửa + KHÓI CỤM LIỀN chia theo QUÃNG đường móc quay (KR5),
            // không theo giờ nữa nên vệt liền dù móc quay nhanh; khói than đáy còn ánh lửa, bay lên, ngả xám rồi mờ
            float dQuay = (XqSNem - XqSLua) * k;
            int demQ = 0;
            // khung vẽ sẵn (2026-11-19, người dùng: "các fireball ... nên thêm trail smoke vào"): có khung "khoi" thì vệt khói đuôi theo móc lửa
            // (KmDuoiKhoi, HatFbKim.cs; cụm 0,24 thân, 22 cụm/giây, sau tướng dưới lưỡi lửa) thay chuỗi khói một múi, không để cả hai
            bool fbKhoi = HasFb("khoi");
            if (fbKhoi) At(XqSLua * k, () => KmDuoiKhoi(t => Moc((t - T0) / k), dQuay, 0.24f * casterH * manh, 0.04f * casterH, 22, Back));
            At(XqSLua * k, () => KmDuoi(t => Moc((t - T0) / k), dQuay, 0.12f * casterH, (pt, ud) =>
            {
                float tc = Tc();
                if (!XqHien(B.mh, tc)) return;
                float x = Mathf.Clamp01((tc - XqSLua) / (XqSNem - XqSLua));
                XqVet(pt, VMoc(tc), manh * (0.85f + 0.3f * x), Back);
                if (!fbKhoi && demQ++ % 2 == 0)
                    KmKhoi(pt + U2(-3, 3), new Vector2(U(-15, 15), -U(40, 80)), U(0.1f, 0.12f) * casterH * manh, U(0.55f, 0.8f), Back, 0.8f, 0, null, 0.2f,
                        demQ % 8 != 1);
            }));
            Every(XqSLua * k, XqSNem * k, 40 * manh, x =>
            {
                float tc = Tc();
                if (!XqHien(B.mh, tc)) return;
                int j = rng.Next(3);
                var v = j == 0 ? XqMau(B.ax, B.ay, tc) : j == 1 ? XqMau(B.bx, B.by, tc) : XqMau(B.cx, B.cy, tc);
                XqLiem(San(v), manh, Back);
            });
            // 3. ném: lửa chạy dọc xích từ tay tới đối thủ, đầu xích (móc) cháy to
            Every(XqSNem * k, XqSTroi * k, 90 * manh, x =>
            {
                float tc = Tc();
                float q = EaseOut(Mathf.Clamp01((tc - XqSNem) / (XqSTroi - XqSNem)));
                var a = Tay(tc);
                var dau = Vector2.Lerp(a, dich, q);
                if (U(0, 1) < 0.4f) XqVet(dau, (dich - a) * 4f, manh, Front);
                else XqLiem(Vector2.Lerp(a, dau, U(0.05f, 1f)), manh, Front);
            });
            // 4. trói: vòng xích quấn thân đối thủ, lửa liếm vòng, xích căng cháy
            At(XqSTroi * k, () =>
            {
                Shake?.Invoke(0.4f * manh);
                KmNhip(0.8f);   // trói: nhịp trúng phụ trước cú đốt chính
                KmNo(dich, foeFeet, tH, 0.45f * manh, "luat", dir);
                XqVongXich(dich, foeFeet.y, tH, manh, (XqSTha - XqSTroi) * k, (XqSCot - XqSTroi) * k);
            });
            float rx = 0.44f * tH * Mathf.Sqrt(manh), ry = 0.12f * tH;
            // lửa liếm vòng xích: lưỡi chữ S liền khối có giọt tách (KmLuaS; ảnh chưa nhập thì lưỡi cũ)
            Every(XqSTroi * k, XqSTha * k, 24 * manh, x =>
            {
                float th = U(0, 6.2832f);
                float cy = dich.y + (rng.Next(2) == 0 ? -0.1f : 0.12f) * tH;
                var p = new Vector2(dich.x + rx * Mathf.Cos(th), cy + ry * Mathf.Sin(th));
                int g = Mathf.Sin(th) > 0 ? Front : Back;
                if (KmLuaS(p, U(0.12f, 0.17f) * tH * manh, U(0.3f, 0.42f), KmLua, Th.pal, g, new Vector2(U(-10, 10), -U(20, 50)), 0.35f) == null)
                    XqLiem(p, manh, g, 1.1f);
            });
            Every(XqSTroi * k, XqSTha * k, 26 * manh, x => XqLiem(Vector2.Lerp(Tay(Tc()), dich, U(0.05f, 0.92f)), manh, Front, 0.85f));
            // 5. CỘT LỬA rất to + bốn nhịp đốt (nổ KR5 nhỏ, lõi sau lưng đối thủ)
            At(XqSCot * k, () =>
            {
                KmNhip(0.6f);
                XqCotLua(foeFeet, tH, manh, (XqSTha - XqSCot) * k);
            });
            for (int i = 0; i < 4; i++)
            {
                int ii = i;
                At((XqSCot + 0.15f + 0.25f * i) * k, () =>
                {
                    Shake?.Invoke(0.18f * manh);
                    if (ii > 0) KmNhip(0.4f);   // nhịp đốt đầu là cú trúng chính (StageView)
                    KmNo(dich + new Vector2(U(-0.15f, 0.15f) * tH, U(-0.2f, 0.1f) * tH), foeFeet, tH, 0.4f * manh, "luat", dir);
                });
            }
            // 6. thả: khói cụm bay lên tách dần, lửa dọc xích tắt dần theo xích rút về
            At(XqSTha * k, () =>
            {
                for (int i = 0; i < 3; i++)
                    KmKhoi(dich + new Vector2(U(-0.25f, 0.25f) * tH, -U(0.2f, 0.5f) * tH), new Vector2(U(-20, 20), -U(40, 80)), U(0.14f, 0.18f) * tH,
                        U(1.0f, 1.3f), Back, 0.5f, 2, null, 0.4f);
            });
            Every(XqSTha * k, XqSRut * k, x => 70 * manh * (1 - x), x =>
            {
                float tc = Tc();
                float q = 1 - EaseOut(Mathf.Clamp01((tc - XqSTha) / (XqSRut - XqSTha)));
                var a = Tay(tc);
                XqLiem(Vector2.Lerp(a, Vector2.Lerp(a, dich, q), U(0.05f, 1f)), manh, Front, 0.8f);
            });
            return t0;
        }

        // VÒNG XÍCH quấn thân đối thủ: hai vòng elip mắt xích của rig (nửa sau vẽ sau tướng, nửa trước vẽ trước), quấn dần từng mắt, nóng đỏ
        // dần khi cột lửa bốc (tCot giây sau lúc trói), giữ tới tTha rồi rơi xuống mặt đất dưới chân đối thủ (dat), nảy nhẹ, nằm yên, mờ
        void XqVongXich(Vector2 body, float dat, float tH, float manh, float tTha, float tCot)
        {
            var s1 = XqXich(1);
            var s2 = XqXich(2);
            if (s1 == null || s2 == null) return;
            float rx = 0.44f * tH * Mathf.Sqrt(manh), ry = 0.12f * tH, L = 0.15f * tH;
            const int n = 14;
            for (int vong = 0; vong < 2; vong++)
            {
                float cy = body.y + (vong == 0 ? -0.1f : 0.12f) * tH;
                for (int i = 0; i < n; i++)
                {
                    float th = 6.2832f * i / n + vong * 0.22f;
                    var sp = (i & 1) == 0 ? s2 : s1;
                    var p = new P
                    {
                        pos = new Vector2(body.x + rx * Mathf.Cos(th), cy + ry * Mathf.Sin(th)), life = tTha + 0.7f,
                        group = Mathf.Sin(th) > 0 ? Front : Back, ph = 0.012f * (i + vong * n), sz = L,
                        ground = dat + ry * Mathf.Sin(th) * 0.6f, bounce = 0.25f
                    };
                    p.onGround = (q, s3) => q.spin = 0;
                    var d = new Vector2(-rx * Mathf.Sin(th), ry * Mathf.Cos(th));
                    float goc = VelAng(d) - 90;
                    float asp = sp.rect.width / Mathf.Max(1f, sp.rect.height);
                    float quay = U(-6, 6);
                    p.upd = (q, dt, s3) =>
                    {
                        if (q.age > tTha && q.acc.y == 0 && q.vel.y >= 0 && q.pos.y < q.ground - 0.5f)
                        {
                            q.acc = new Vector2(0, 1400);                      // bắt đầu rơi (một lần)
                            q.vel = new Vector2(U(-40, 40), -U(40, 120));
                            q.spin = quay;
                        }
                    };
                    p.draw = (q, k, buf) =>
                    {
                        float t = q.age;
                        if (t < q.ph) return;
                        float hien = EaseOut(Mathf.Clamp01((t - q.ph) / 0.08f));
                        float nong = SmoothStep(tCot, tCot + 0.45f, t) * (1 - SmoothStep(tTha, tTha + 0.4f, t));
                        float a = 1 - SmoothStep(tTha + 0.35f, tTha + 0.7f, t);
                        var col = Color.Lerp(Color.white, XqNong, 0.75f * nong);
                        Put(buf, q.group, 38, sp, col, q.pos, q.sz * hien, asp, goc + q.ang * Mathf.Rad2Deg, a);
                    };
                    Add(p);
                }
            }
        }

        // CỘT LỬA rất to dưới chân đối thủ: vòng lửa + khe nứt dưới đất, nổ ở chân, cột lưỡi lửa bốc thẳng lên (lõi sau lưng đối thủ, hai mép
        // trước nhỏ hơn để không che mặt), lõi nóng giữa cột, khói đen ở đỉnh, than bay. Cao tới gần mép trên màn, tối đa 2,4 lần thân.
        void XqCotLua(Vector2 feet, float tH, float manh, float dur)
        {
            float rx = 0.36f * tH;
            float cao = Mathf.Clamp(feet.y - 24, 1.2f * tH, 2.4f * tH) * Mathf.Sqrt(manh);
            float v0 = Mathf.Max(380, (cao - 60) / 0.425f);
            Shake?.Invoke(0.7f * manh);
            // hai vòng cung dẹt KHÔNG viền nở trên đất (KR5; vòng có viền mực dày nhìn nặng, soi tờ khung 2026-11-18)
            KmCung(feet + new Vector2(0, 2), 0.15f * tH, 1.1f * tH * manh, 0.45f, Th.ring2, 0.3f, Floor, 30.6f, 0.9f);
            KmCung(feet + new Vector2(0, 2), 0.1f * tH, 0.75f * tH * manh, 0.6f, Th.ember, 0.3f, Floor, 31, 0.75f);
            var cr = new P { pos = feet + new Vector2(0, 2), life = dur + 0.5f, group = Floor, seed = rng.Next(4), sz = tH };
            cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_" + q.seed), Color.white, q.pos, 1.4f * q.sz * 0.42f * Mathf.Min(1, q.age / 0.15f),
                1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.3f));
            Add(cr);
            KmChay(feet + new Vector2(0, 3), 0.5f * tH, dur, 0.8f, 0.42f);
            KmNo(feet + new Vector2(0, -0.15f * tH), feet, tH, 0.9f * manh, "luat", 0);
            // 2026-11-18 (người dùng: lửa rải rác, chưa liền, chưa mềm): thân cột là các lưỡi lửa TO chồng sát nhau sau lưng đối thủ (một khối, một
            // viền mực), ít hơn mà to hơn; mép trước chỉ vài lưỡi chữ S nhỏ ở chân (không che mặt); giọt lửa tách khỏi ngọn; đỉnh cột là khói CỤM
            // than đáy ánh lửa (tách cụm rồi mới mờ); cụm đốm nhỏ thay đốm lẻ to
            // khung vẽ sẵn (2026-11-19): thân cột là ba khung lửa lặp "lua_lap" chồng nhau sau lưng (KmCotLuaFb, HatFbKim.cs) thay ~90 lưỡi rời;
            // mép trước (KmLuaS), nổ chân (KmNo), khói đỉnh (KmKhoi) cũng ra khung; chưa nhập ảnh thì lưỡi lửa dưới
            if (!KmCotLuaFb(feet, cao, dur))
            {
                Every(0, dur, x => 64 * manh * (1 - 0.3f * x), x =>
                {
                    float th = U(0, 6.2832f);
                    float c = Mathf.Cos(th), s = Mathf.Sin(th);
                    var q = Flame(feet + new Vector2(rx * c * U(0.5f, 0.95f), 10 * s - 6), new Vector2(-c * U(10, 50), -U(0.85f, 1.15f) * v0), U(0.5f, 0.72f),
                        U(13, 17) * manh, U(38, 50) * manh, "tron", Th.pal, Back, 1.3f, -380, 1.75f, 0.03f, 0.04f);
                    Tongue(q, 1, 0.65f);
                    q.smokeGroup = Back;
                });
                Every(0, dur * 0.85f, 24 * manh, x =>
                {
                    var q = Flame(feet + new Vector2(U(-0.12f, 0.12f) * tH, -4), new Vector2(U(-20, 20), -U(1.05f, 1.3f) * v0), U(0.4f, 0.55f), 10 * manh,
                        U(26, 34) * manh, "tron", Th.pal, Back, 1.2f, -420, 2.1f, 0, 0.04f);
                    Tongue(q, 1, 0.75f);
                });
            }
            Every(0.04f, dur, 9 * manh, x =>
            {
                float sd = rng.Next(2) == 0 ? -1 : 1;
                var chan = feet + new Vector2(sd * rx * U(0.55f, 0.95f), U(2, 8));
                if (KmLuaS(chan, U(0.2f, 0.28f) * tH * manh, U(0.34f, 0.48f), KmLua, Th.pal, Front, new Vector2(-sd * U(0, 20), -U(10, 40)), 0.6f) == null)
                {
                    var q = Flame(chan + new Vector2(0, -6), new Vector2(-sd * U(0, 30), -U(0.5f, 0.7f) * v0), U(0.3f, 0.42f), 8 * manh, U(16, 22) * manh, "tron",
                        Th.pal, Front, 1.6f, -380, 1.7f, 0, 0);
                    Tongue(q, 1, 0.7f);
                }
            });
            Every(0.1f, dur, 10 * manh, x => KmGiot(feet + new Vector2(U(-0.25f, 0.25f) * tH, -cao * U(0.55f, 0.95f)), new Vector2(U(-40, 40), -U(160, 260)),
                U(6, 9) * manh, KmLua, Back));
            Every(0.15f, dur + 0.3f, 6 * manh, x => KmKhoi(feet + new Vector2(U(-0.25f, 0.25f) * tH, -cao * U(0.85f, 1.05f)),
                new Vector2(U(-30, 30), -U(60, 110)), U(0.16f, 0.21f) * tH * manh, U(1.0f, 1.3f), Back, 0.8f, 2, null, 0.45f));
            Every(0, dur, 2 * manh, x => KmDomCum(feet + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.2f, 0.9f) * cao), new Vector2(U(-50, 50), -U(140, 240)),
                Th.ember, U(0, 1) < 0.5f ? Front : Back));
        }
    }
}
'''


def do(dang):
    env = dict(os.environ)
    env.pop("QX_DANG", None)
    if dang == 1:
        env["QX_DANG"] = "non"
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "quy_xich_do_hat.py")], env=env, capture_output=True, text=True,
                       encoding="utf-8", check=True)
    # rig in thêm dòng thông báo ra stdout: chỉ giữ dòng mảng C# và dòng chú thích của bảng
    return "".join(ln + "\n" for ln in r.stdout.splitlines() if ln.startswith("        static readonly") or ln.startswith("        // quy_xich"))


def lay():
    o = ["        static XqBang XqLay(int dang, bool chieu) =>"]
    cs = []
    for d in (1, 2):
        for c, k in ((True, "S"), (False, "C")):
            p = f"Xq{d}{k}"
            cs.append((d, c, f"new XqBang {{ mx = {p}MocX, my = {p}MocY, mh = {p}MocHien, ax = {p}Xich0X, ay = {p}Xich0Y, bx = {p}Xich1X, "
                             f"by = {p}Xich1Y, cx = {p}Xich2X, cy = {p}Xich2Y, tx = {p}TayX, ty = {p}TayY }}"))
    o.append(f"            dang == 1 ? (chieu ? {cs[0][2]}")
    o.append(f"                              : {cs[1][2]})")
    o.append(f"                      : (chieu ? {cs[2][2]}")
    o.append(f"                              : {cs[3][2]});")
    return "\n".join(o)


def main():
    bang = do(1) + do(2)
    s = KHUNG.replace("/*BANG*/", bang.rstrip("\n")).replace("/*LAY*/", lay())
    open(RA, "w", encoding="utf-8", newline="\n").write(s)
    print(RA, f"{len(s) // 1024} KB")


if __name__ == "__main__":
    main()
