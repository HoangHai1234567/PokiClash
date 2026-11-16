# -*- coding: utf-8 -*-
"""Sinh `Assets/01 Script/Game/Battle/HatHon.cs` (hiệu ứng hồn xanh của kỵ sĩ bị nguyền, suất tam_kiem): khung C# + bảng số đo từ rig
(ky_nguyen_rig.py) theo khung 30 / giây, phần của chiều cao KHAI cho game (x về phía trước, y lên, gốc ở chân):
    cast : mũi kiếm gãy (xương mieng)
    skill: mũi kiếm gãy, chỗ gãy (hon_goc), mép đang hiện của phần vá (hon_dau), mũi phần vá (mui_hon), độ đậm phần vá
Mốc (giây clip) đọc từ sự kiện của clip trong rig. Đổi clip / tỉ lệ rig thì chạy lại script này (đừng sửa tay HatHon.cs).

    py -3 -I ArtGen/Spine/ky_nguyen_hat_cs.py [dạng ...]     (mặc định: 2; dạng 1 thêm khi có rig dạng 1)
"""
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RA = os.path.join(ROOT, "Assets", "01 Script", "Game", "Battle", "HatHon.cs")


def do(dang):
    """{tên bảng: mảng} + mốc cho một dạng."""
    import importlib
    if dang == 1:
        os.environ["KN_DANG"] = "non"
    import ky_nguyen_rig as R
    importlib.reload(R)
    sk, info = R.dung()
    cao = float(info["cao"])
    clips = {c.ten: c for c in R.lam_clip(sk, info)}
    out, moc = {}, {}

    def bang(ten_clip, diem, them_hon=False):
        c = clips[ten_clip]
        fr = R.nuong(sk, c)
        cols = {k: ([], []) for k in diem}
        hon = []
        for P in fr:
            W = sk.the_gioi(P)
            for k, b in diem.items():
                p = W[b][:2, 2]
                cols[k][0].append(p[0] / cao)
                cols[k][1].append(p[1] / cao)
            if them_hon:
                hon.append(max((P.alpha.get(s["name"], 0.0) for s in sk.slots if s["name"].startswith("P_jian_hon")), default=0.0))
        for k, (xs, ys) in cols.items():
            out[f"{ten_clip}_{k}_x"] = np.array(xs)
            out[f"{ten_clip}_{k}_y"] = np.array(ys)
        if them_hon:
            out[f"{ten_clip}_hon"] = np.array(hon)
        moc[ten_clip] = {"dur": c.dur, "trung": c.trung, **{e[1]: e[0] for e in c.ev}}

    bang("cast", {"tip": "mieng"})
    bang("skill", {"tip": "mieng", "goc": "hon_goc", "dau": "hon_dau", "mui": "mui_hon"}, them_hon=True)
    moc["attack"] = {"dur": clips["attack"].dur, "trung": clips["attack"].trung}
    return out, moc, cao


def fa(a):
    return "{ " + ", ".join(f"{v:.3f}f" for v in a) + " }"


def sinh(dangs):
    bangs, mocs = {}, {}
    for d in dangs:
        b, m, cao = do(d)
        bangs[d], mocs[d] = (b, cao), m
    d0 = dangs[-1]
    m = mocs[d0]
    S, C, A = m["skill"], m["cast"], m["attack"]
    dong = []
    for d in dangs:
        b, cao = bangs[d]
        dong.append(f"        // dạng {d}: chiều cao khai {cao:.1f}; skill {mocs[d]['skill']['dur']:.3f} s, trúng {mocs[d]['skill']['trung']:.3f}; "
                    f"cast {mocs[d]['cast']['dur']:.3f} s, trúng {mocs[d]['cast']['trung']:.3f}")
        for k, v in b.items():
            ten = "Kn" + str(d) + "".join(x.capitalize() for x in k.split("_"))
            dong.append(f"        static readonly float[] {ten} = {fa(v)};")
    the = "\n".join(dong)
    cs = KHUNG.replace("@BANG@", the)
    rep = {"@A_LEAD@": A["trung"], "@C_LEAD@": C["trung"], "@C_GOI@": C["goi"], "@S_LEAD@": S["trung"], "@S_HUT@": S["hut"], "@S_HAT@": S["hat"],
           "@S_HOI@": S["hoi_phuc"], "@S_GONG@": S["gong"], "@S_CHEM@": S["chem"] - 0.05, "@S_TAT@": S["tat"]}
    for k, v in rep.items():
        cs = cs.replace(k, f"{v:.3f}")
    cs = cs.replace("@DANG2@", str(d0)).replace("@DANG1@", str(dangs[0]))
    open(RA, "w", encoding="utf-8", newline="\n").write(cs)
    print(RA, f"{len(cs) // 1024} KB; mốc skill {S}; cast {C}; attack {A}")


KHUNG = r'''// Bộ VONG KỴ (2026-11-16, kỵ sĩ cổ đại bị nguyền, giáp sắt đen rỉ giữ hồn bằng lửa linh hồn xanh, suất tam_kiem ải 50 đảo Kim; rig
// ArtGen/Spine/ky_nguyen_rig.py (rig gốc monster_3642): dạng 2 ky_nguyen_2; ghi chú ArtGen/Spine/inbox/ky_nguyen_ghichu.md).
// Người dùng: đánh thường "lao tới dùng kiếm chém"; chiêu mana "giơ kiếm lên trời, gọi những linh hồn đồng đội từ thời xưa dạng linh hồn xanh
// lao tới đánh kẻ thù"; chiêu cuối "tay kia vuốt lên, thanh kiếm cùn hút những khí xanh xung quanh, được khôi phục bằng vật chất linh hồn xanh
// lá thành kiếm hoàn chỉnh, tỏa aura linh hồn xanh; chém một phát thật mạnh xuống đối thủ, epic, impact". Đi đường "n_" (StageView.PreFx /
// AtkFx → PlayNuoc), phát lúc clip BẮT ĐẦU; mốc là giây clip của rig, co theo `lead` (giờ trúng của clip):
// - n_hon_chem (đòn thường): vệt chém lửa hồn quét chéo qua đối thủ ngay trước khung trúng; trúng: chớp hồn, lưỡi lửa hồn toé, tia, mảnh giáp.
// - n_hon_goi1 / n_hon_goi (chiêu mana): `goi` mũi kiếm giơ trên trời bùng lửa hồn, lửa liếm quanh mũi kiếm; HỒN ĐỒNG ĐỘI (hình mũ vương miện
//   xanh hồn: Resources/ky_nguyen_2/ky_nguyen_2_tt_hon.png) bay ra từ mũi kiếm, xếp quạt trên đầu, lần lượt lao theo cung xuống đối thủ để lại
//   đuôi lửa hồn; mỗi hồn trúng: chớp, lưỡi lửa toé; hồn cuối nổ to (3 / 5 hồn).
// - n_hon_kiem1 / n_hon_kiem (chiêu cuối): `hut` → `hoi_phuc` khí hồn xanh từ quanh người bị hút vào MÉP ĐANG HIỆN của phần vá (đúng mép mặt nạ
//   cắt của rig, bảng số đo), tia lấp lánh ở mép; `hat` lửa hồn chạy dọc lưỡi tới mũi; `hoi_phuc` lưỡi bùng sáng dọc kiếm; `gong` aura hồn bùng
//   quanh người (vòng sàn, lưỡi lửa bốc); nhát bổ: vệt lửa hồn theo đúng đường mũi kiếm; trúng: chớp lớn, hai vòng sóng, cột lưỡi lửa hồn toé
//   lên, khói hồn, mảnh giáp, đá văng, rung mạnh; `tat` phần vá tan thành khí hồn bay lên.
// FILE SINH TỰ ĐỘNG từ ArtGen/Spine/ky_nguyen_hat_cs.py (bảng số đo của rig): đổi clip hay tỉ lệ rig thì chạy lại script, đừng sửa tay.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        const float KnDt = 1f / 30f;
        const float KnALead = @A_LEAD@f;
        const float KnCLead = @C_LEAD@f, KnCGoi = @C_GOI@f;
        const float KnSLead = @S_LEAD@f, KnSHut = @S_HUT@f, KnSHat = @S_HAT@f, KnSHoi = @S_HOI@f, KnSGong = @S_GONG@f, KnSChem = @S_CHEM@f, KnSTat = @S_TAT@f;
        static readonly Color KnXanh = C(132, 205, 57), KnNhat = C(214, 250, 170), KnDam = C(56, 132, 54);
        static readonly Color[] KnChopC = { Ink, C(56, 132, 54), C(132, 205, 57), C(196, 244, 140), C(246, 255, 226) };

@BANG@

        static Vector2 KnMau(float[] xs, float[] ys, float t)
        {
            float f = Mathf.Max(0, t) / KnDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            float w = Mathf.Clamp01(f - i);
            return new Vector2(Mathf.Lerp(xs[i], xs[j], w), Mathf.Lerp(ys[i], ys[j], w));
        }

        static float KnMau1(float[] xs, float t)
        {
            float f = Mathf.Max(0, t) / KnDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            return Mathf.Lerp(xs[i], xs[j], Mathf.Clamp01(f - i));
        }

        // điểm bảng (phần chiều cao, x tới trước, y lên) → sân (y xuống)
        static Vector2 KnO(Vector2 feet, float H, float dir, Vector2 n) => feet + new Vector2(dir * n.x * H, -n.y * H);

        // ảnh hồn đồng đội (AolaImport nhập tên có "_tt_" thành sprite), nạp một lần
        static readonly Dictionary<string, Sprite> knAnh = new Dictionary<string, Sprite>();

        static Sprite KnHonAnh()
        {
            const string key = "ky_nguyen_2_tt_hon";
            if (knAnh.TryGetValue(key, out var s) && s) return s;
            s = Resources.Load<Sprite>("ky_nguyen_2/" + key);
            knAnh[key] = s;
            return s;
        }

        // chớp hồn: vương miện toé xanh (khuôn SatChop)
        void HonChop(Vector2 c, float size, int group = Front, float life = 0.16f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = 2 + rng.Next(2), sz = size };
            p.draw = (q, k, buf) =>
            {
                for (int i = 0; i < 5; i++)
                    Put(buf, q.group, 33 + i * 0.1f, S((i == 0 ? "crowns_" : "crown_") + q.seed), KnChopC[i], q.pos,
                        q.sz * (0.6f + 0.5f * EaseOut(k / 0.6f)) * BurstF[i] + (i == 0 ? 5 : 0), 1, q.ang);
            };
            Add(p);
        }

        // lưỡi lửa hồn: tip +1 ngọn theo hướng bay (toé), −1 ngả ngược (đuôi, vệt)
        P HonLuoi(Vector2 p, Vector2 v, float r0, float r1, float life, int g, float tip = 1, float up = 0.5f)
        {
            var q = Flame(p, v, life, r0, r1, "tron", "hon", g, 2.6f, -280, 1.6f, 0.12f, 0.08f);
            Tongue(q, tip, up);
            q.smokeGroup = Back;
            return q;
        }

        // một cú trúng của hồn: chớp, lưỡi lửa hồn toé theo hướng d, tia, mảnh giáp rỉ
        void HonTrung(Vector2 c, Vector2 d, float tH, float manh, int nLua, int nTia)
        {
            HonChop(c, 0.46f * tH * manh);
            for (int i = 0; i < Mathf.RoundToInt(nLua * manh); i++)
            {
                var dd = (d * U(0.2f, 1f) + new Vector2(U(-0.8f, 0.8f), U(-1f, 0.3f))).normalized;
                HonLuoi(c + U2(-6, 6), dd * U(160, 360) * manh, U(6, 9) * manh, U(16, 26) * manh, U(0.22f, 0.36f), Front, 1, 0.3f);
            }
            for (int i = 0; i < Mathf.RoundToInt(nTia * manh); i++)
                Spark(c, (d * U(0.3f, 1f) + new Vector2(U(-0.7f, 0.7f), U(-0.9f, 0.4f))).normalized, U(220, 440), U(0.16f, 0.3f), U(6, 9), 280);
            Extra(c, Mathf.RoundToInt(3 * manh), 260 * manh);
        }

        // ĐÒN THƯỜNG: lao tới, vung kiếm qua đầu, bổ. lead: giây từ đầu clip attack tới khung trúng.
        public float NHonChem(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.08f, lead);
            var c = foeBody + new Vector2(-dir * 0.1f * tH, -0.02f * tH);
            float R = 0.46f * tH;
            // vệt chém: cung lưỡi lửa hồn quét từ trên sau qua đỉnh xuống dưới trước đối thủ trong 0,07 s trước khung trúng
            for (int i = 0; i < 10; i++)
            {
                float f = i / 9f;
                float ph = Mathf.Lerp(140f, -35f, f) * Mathf.Deg2Rad;
                var pt = c + new Vector2(dir * Mathf.Cos(ph), -Mathf.Sin(ph)) * R;
                var tg = new Vector2(dir * Mathf.Sin(ph), Mathf.Cos(ph));                 // tiếp tuyến theo chiều quét
                At(t0 - 0.075f + 0.075f * f, () => HonLuoi(pt, tg * U(120, 220), U(7, 9), U(17, 24), U(0.16f, 0.24f), Front, -1, 0.15f));
            }
            At(t0, () =>
            {
                Shake?.Invoke(0.26f);
                HonTrung(c, new Vector2(dir, 0.4f).normalized, tH, 1f, 8, 8);
                Ring(c, 0.3f, 0.05f * tH, 0.5f * tH, KnXanh, 0.5f, Front, 32);
            });
            return t0;
        }

        // MỘT HỒN ĐỒNG ĐỘI: bay ra từ mũi kiếm tới chỗ lơ lửng (quạt trên đầu) trong 0,18 s, lơ lửng nhấp nhô, tới tBay lao theo cung xuống tgt
        // (tới nơi đúng hết đời hạt) để lại đuôi lửa hồn; trúng: chớp + lưỡi lửa toé. H: chiều cao hình hồn (sân).
        void HonDongDoi(Vector2 tip, Vector2 home, Vector2 tgt, float H, float tBay, float life, float dir, float tHFoe, float manh, bool cuoi)
        {
            float ph = U(0, 6.28f);
            var ctrl = (home + tgt) * 0.5f + new Vector2(0, -0.6f * H);
            var p = new P { pos = tip, life = life, group = Front, sz = H, home = home, aim = tgt, off = ctrl };
            p.upd = (q, dt, s3) =>
            {
                float t = q.age;
                Vector2 np;
                if (t < 0.24f) np = Vector2.Lerp(tip, q.home, EaseOut(t / 0.24f));
                else if (t < tBay) np = q.home + new Vector2(0, Mathf.Sin((t - 0.24f) * 6.3f + ph) * 0.06f * H);
                else
                {
                    float u = Mathf.Pow(Mathf.Clamp01((t - tBay) / Mathf.Max(0.05f, q.life - tBay)), 1.35f);
                    np = (1 - u) * (1 - u) * q.home + 2 * u * (1 - u) * q.off + u * u * q.aim;
                }
                q.vel = dt > 1e-5f ? (np - q.pos) / dt : Vector2.zero;
                if (t > 0.05f && (float)q.rng.NextDouble() < (t < tBay ? 0.25f : 0.9f))
                    HonLuoi(q.pos + new Vector2(0, 0.25f * H) + U2(-0.12f, 0.12f) * H, -q.vel * 0.08f + new Vector2(U(-20, 20), -U(30, 80)),
                        U(4, 6) * manh, U(10, 16) * manh, U(0.18f, 0.28f), Back, -1, 0.5f);
            };
            var anh = KnHonAnh();
            float st = anh ? anh.rect.width / Mathf.Max(1f, anh.rect.height) : 0.8f;
            p.draw = (q, k, buf) =>
            {
                float t = k * q.life;
                float s = EaseOut(Mathf.Clamp01(t / 0.16f));
                float lean = Mathf.Clamp(q.vel.x * dir / 900f, -1, 1) * 22f;
                if (anh) Put(buf, q.group, 46, anh, Color.white, q.pos, q.sz * s, st, -dir * lean, 0.95f, 0, dir < 0);
                else Put(buf, q.group, 46, S("blob_0"), KnXanh, q.pos, q.sz * 0.6f * s, 1, 0, 0.9f);
            };
            p.onDeath = (q, s3) =>
            {
                HonTrung(tgt, new Vector2(dir, 0.3f).normalized, tHFoe, (cuoi ? 1.45f : 0.8f) * manh, cuoi ? 12 : 5, cuoi ? 10 : 4);
                if (cuoi)
                {
                    Shake?.Invoke(0.4f * manh);
                    Ring(tgt, 0.38f, 0.06f * tHFoe, 0.72f * tHFoe * manh, KnXanh, 0.5f, Front, 32);
                }
                else Shake?.Invoke(0.16f);
            };
            Add(p);
        }

        // CHIÊU MANA: n hồn (3 dạng 1, 5 dạng 2). lead: giây từ đầu clip cast tới trúng (hồn đầu chạm). Trả giây tới lúc hồn đầu trúng.
        public float NHonGoi(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int n, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float k = Mathf.Max(0.3f, lead) / KnCLead;
            float tGoi = KnCGoi * k, tTrung = Mathf.Max(0.3f, lead);
            var tip = KnO(casterFeet, casterH, dir, KnMau(Kn@DANG2@CastTipX, Kn@DANG2@CastTipY, KnCGoi));
            At(tGoi, () =>
            {
                HonChop(tip, 0.32f * casterH * manh, Front, 0.2f);
                Ring(tip, 0.4f, 0.04f * casterH, 0.42f * casterH * manh, KnXanh, 1f, Front, 32);
                for (int i = 0; i < 7; i++) HonLuoi(tip + U2(-8, 8), new Vector2(U(-160, 160), -U(140, 320)), 6, U(14, 22) * manh, U(0.24f, 0.36f), Front, 1, 0.5f);
                for (int i = 0; i < 6; i++) Spark(tip, new Vector2(U(-1f, 1f), U(-1f, 0.1f)), U(160, 320), U(0.16f, 0.26f), U(5, 8), 120);
            });
            Every(tGoi, tGoi + 0.72f * k, 26, _ => HonLuoi(tip + U2(-0.05f, 0.05f) * casterH, new Vector2(U(-40, 40), -U(60, 140)), 4, U(10, 16) * manh,
                U(0.2f, 0.3f), Front, 1, 0.6f));
            float H = 0.46f * casterH * Mathf.Sqrt(manh);
            for (int i = 0; i < n; i++)
            {
                float f = n == 1 ? 0.5f : i / (n - 1f);
                float tHien = tGoi + 0.05f * i;
                float tToi = tTrung + 0.075f * i;
                // chỗ lơ lửng: VÒNG CUNG quanh vai, từ sau lưng sang phía đối thủ (mũi kiếm giơ sát mép trên màn: xếp quạt trên mũi kiếm thì hồn
                // lọt khỏi màn, nấp sau bảng máu đối thủ — soi trong trận 2026-11-16)
                float cao = Mathf.Lerp(1.05f, 1.3f, 1f - Mathf.Abs(f - 0.5f) * 2f);
                var home = casterFeet + new Vector2(dir * Mathf.Lerp(-0.3f, 0.62f, f) * casterH, -cao * casterH);
                var tgt = foeBody + new Vector2(-dir * U(0f, 0.08f) * tH, (f - 0.5f) * 0.32f * tH);
                bool cuoi = i == n - 1;
                float life = tToi - tHien, tBay = Mathf.Max(0.22f, life - 0.34f);
                At(tHien, () => HonDongDoi(tip, home, tgt, H, tBay, life, dir, tH, manh, cuoi));
            }
            return tTrung;
        }

        // CHIÊU CUỐI: lead: giây từ đầu clip skill tới nhát bổ trúng. manh: 0,8 dạng 1, 1 dạng 2. Trả giây tới lúc trúng.
        public float NHonKiem(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float k = Mathf.Max(0.3f, lead) / KnSLead;
            float tTrung = Mathf.Max(0.3f, lead);
            Vector2 Dau(float tc) => KnO(casterFeet, casterH, dir, KnMau(Kn@DANG2@SkillDauX, Kn@DANG2@SkillDauY, tc));
            Vector2 Goc(float tc) => KnO(casterFeet, casterH, dir, KnMau(Kn@DANG2@SkillGocX, Kn@DANG2@SkillGocY, tc));
            Vector2 Mui(float tc) => KnO(casterFeet, casterH, dir, KnMau(Kn@DANG2@SkillMuiX, Kn@DANG2@SkillMuiY, tc));
            float r = 0.012f * casterH;                                                   // cỡ hạt nhỏ theo thân
            // khí hồn bị hút vào mép đang hiện của phần vá + tia lấp lánh ở mép
            Every(KnSHut * k, KnSHoi * k, 40, x =>
            {
                float tc = Mathf.Lerp(KnSHut, KnSHoi, x);
                if (KnMau1(Kn@DANG2@SkillHon, tc) < 0.5f && tc > KnSHut + 0.12f) return;
                var dau = Dau(tc);
                float a = U(0, 6.28f), d = U(0.5f, 0.95f) * casterH;
                var from = dau + new Vector2(Mathf.Cos(a) * d, Mathf.Sin(a) * d * 0.7f + 0.15f * casterH);
                var q = HonLuoi(from, (dau - from) / 0.32f, U(4, 6) * manh, U(9, 14) * manh, 0.32f, (rng.Next(2) == 0) ? Back : Front, -1, 0.1f);
                q.drag = 0;
                q.acc = Vector2.zero;
            });
            Every(KnSHut * k + 0.1f, KnSHoi * k, 30, x =>
            {
                float tc = Mathf.Lerp(KnSHut + 0.1f / k, KnSHoi, x);
                if (KnMau1(Kn@DANG2@SkillHon, tc) < 0.5f) return;
                Spark(Dau(tc), new Vector2(U(-1f, 1f), U(-1f, 0.2f)), U(80, 200), U(0.12f, 0.22f), U(5, 8) * manh, 60);
            });
            // tay hất: lửa hồn chạy dọc lưỡi tới mũi
            Every(KnSHat * k, KnSHoi * k, 50, x =>
            {
                float tc = Mathf.Lerp(KnSHat, KnSHoi, x);
                HonLuoi(Dau(tc) + U2(-0.02f, 0.02f) * casterH, new Vector2(U(-50, 50), -U(80, 180)), 5, U(12, 18) * manh, U(0.2f, 0.3f), Front, 1, 0.6f);
            });
            // kiếm lành: bùng sáng dọc lưỡi
            At(KnSHoi * k, () =>
            {
                var g = Goc(KnSHoi);
                var m = Mui(KnSHoi);
                HonChop(m, 0.3f * casterH * manh, Front, 0.18f);
                for (int i = 0; i < 10; i++)
                {
                    var pt = Vector2.Lerp(g, m, i / 9f);
                    HonLuoi(pt + U2(-6, 6), new Vector2(U(-120, 120), -U(60, 200)), 6, U(14, 22) * manh, U(0.24f, 0.34f), Front, 1, 0.5f);
                }
                Ring(Vector2.Lerp(g, m, 0.5f), 0.36f, 0.05f * casterH, 0.5f * casterH * manh, KnXanh, 0.9f, Front, 32);
            });
            // giơ qua đầu: aura hồn bùng quanh người
            At(KnSGong * k, () =>
            {
                Shake?.Invoke(0.22f * manh);
                Ring(casterFeet, 0.5f, 0.1f * casterH, 0.9f * casterH * manh, KnXanh);
                Ring(casterFeet, 0.6f, 0.06f * casterH, 0.62f * casterH * manh, KnNhat, 0.3f, Floor, 31);
                for (int i = 0; i < Mathf.RoundToInt(14 * manh); i++)
                {
                    var pt = casterFeet + new Vector2(U(-0.42f, 0.42f) * casterH, -U(0.05f, 0.9f) * casterH);
                    HonLuoi(pt, new Vector2(U(-60, 60), -U(160, 320)), 6, U(16, 26) * manh, U(0.3f, 0.45f), (i & 1) == 0 ? Back : Front, 1, 0.8f);
                }
                var m = Mui(KnSGong);
                for (int i = 0; i < 6; i++) Spark(m, new Vector2(U(-1f, 1f), U(-1f, 0.3f)), U(160, 300), U(0.16f, 0.26f), U(5, 8), 120);
            });
            // lửa hồn liếm dọc lưỡi trong lúc giơ qua đầu
            Every(KnSHoi * k, KnSChem * k, 22, x =>
            {
                float tc = Mathf.Lerp(KnSHoi, KnSChem, x);
                var pt = Vector2.Lerp(Goc(tc), Mui(tc), U(0.05f, 0.95f));
                HonLuoi(pt, new Vector2(U(-30, 30), -U(60, 140)), 4, U(9, 14) * manh, U(0.18f, 0.26f), Front, 1, 0.6f);
            });
            // nhát bổ: vệt lửa hồn theo đúng đường mũi kiếm
            Every(KnSChem * k, tTrung + 0.02f, 160, x =>
            {
                float tc = Mathf.Lerp(KnSChem, KnSLead + 0.02f / k, x);
                var a0 = Mui(tc);
                var a1 = Mui(tc - 0.02f);
                HonLuoi(a0 + U2(-6, 6), (a0 - a1) / 0.02f * 0.08f, U(8, 11) * manh, U(20, 30) * manh, U(0.16f, 0.24f), Front, -1, 0.1f);
                if ((rng.Next(3)) == 0) HonLuoi(Vector2.Lerp(Goc(tc), a0, U(0.4f, 0.9f)), (a0 - a1) / 0.02f * 0.05f, 6, U(14, 20) * manh, 0.18f, Front, -1, 0.1f);
            });
            // TRÚNG: chớp lớn, hai vòng sóng, cột lưỡi lửa hồn toé lên, khói hồn, mảnh giáp, đá
            At(tTrung, () =>
            {
                Shake?.Invoke(0.7f * manh);
                var c = foeBody + new Vector2(-dir * 0.06f * tH, 0.06f * tH);
                HonTrung(c, new Vector2(dir, 0.5f).normalized, tH, 1.6f * manh, 14, 14);
                HonChop(c + new Vector2(0, -0.1f * tH), 0.9f * tH * manh, Front, 0.22f);
                Ring(foeFeet, 0.5f, 0.1f * tH, 1.25f * tH * manh, KnXanh);
                Ring(foeFeet, 0.62f, 0.06f * tH, 0.85f * tH * manh, KnNhat, 0.3f, Floor, 31);
                Ring(c, 0.4f, 0.08f * tH, 0.9f * tH * manh, KnXanh, 0.6f, Front, 32);
                for (int i = 0; i < Mathf.RoundToInt(16 * manh); i++)
                {
                    var pt = foeFeet + new Vector2(U(-0.45f, 0.45f) * tH, -U(0f, 0.25f) * tH);
                    HonLuoi(pt, new Vector2(U(-120, 120), -U(260, 620) * manh), 8, U(20, 34) * manh, U(0.34f, 0.5f), (i & 1) == 0 ? Back : Front, 1, 0.85f);
                }
                for (int i = 0; i < Mathf.RoundToInt(5 * manh); i++)
                    Smoke(foeFeet + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.1f, 0.5f) * tH), new Vector2(U(-40, 40), -U(60, 120)), U(1.0f, 1.4f),
                        0.06f * tH, 0.18f * tH, Back, "dark", 0.4f);
                for (int i = 0; i < Mathf.RoundToInt(5 * manh); i++)
                    Rock(foeFeet + new Vector2(U(-0.25f, 0.25f) * tH, -6), new Vector2(U(-260, 260), -U(260, 480)), foeFeet.y + U(-4, 6), U(11, 16));
            });
            // phần vá tan: khí hồn bay lên dọc lưỡi
            Every(KnSTat * k, KnSTat * k + 0.24f * k, 60, x =>
            {
                float tc = KnSTat + 0.24f * x;
                var pt = Vector2.Lerp(Goc(tc), Mui(tc), U(0f, 1f));
                HonLuoi(pt, new Vector2(U(-40, 40), -U(80, 200)), 4, U(10, 16) * manh, U(0.24f, 0.36f), Front, 1, 0.7f);
            });
            return tTrung;
        }
    }
}
'''

if __name__ == "__main__":
    ds = [int(x) for x in sys.argv[1:]] or [2]
    sinh(ds)
