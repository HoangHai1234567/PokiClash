# -*- coding: utf-8 -*-
"""Cổ Vương Nhi (tuong_cot_non; DẠNG 1 của Cổ Vương, tướng 6 đảo Mộc): hình của mình trên ĐÚNG bộ xương con gốc monster_3273 (cổ vật đá
chạm tròn; game tham khảo; người dùng chọn 2026-11-17). Ghi chú: inbox/tuong_cot_ghichu.md mục 8.

- XƯƠNG: 12 xương của họ (FK thuần; bỏ shadow) + `move` (sân đo lao) + `m_<mảnh>` (một xương riêng mỗi mảnh, con của xương gốc, ở tâm
  mảnh: thu / bung / văng riêng từng mảnh) + `far`, `fly_cot` → `cot_bay` (cột nhỏ giáng xuống đối thủ ở chiêu cuối) + `mieng`.
- MẢNH: mảnh cứng "đúng chỗ, đúng cỡ" trên concept (tuong_cot_non_manh.py), concept căn lên con gốc (mau/can.json). Mắt hai hình: `mat` /
  `mat_nham` (nhắm khi con gốc hiện mắt chữ X `P_hit`, và chớp ở idle). Cột ở chiêu cuối mượn ảnh `cot` của dạng 2.
Xương và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tuong_cot_non_rig.py      → inbox/tuong_cot_non_1/rig/
    py -3 -I ArtGen/Spine/tuong_cot_non_rig.py soi <clip> <giây,...|n=12|t0:t1:n> [tỉ lệ]
    py -3 -I ArtGen/Spine/tuong_cot_non_rig.py kiem
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, khung, hoat, xuat, soi, luoi  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import tho5  # noqa: E402

tho5.CON["tuong_cot_non"] = ("monster_3273", 6, 30)
G = tho5.dat("tuong_cot_non")
TEN_RIG = "tuong_cot_non"
D_PX = float(os.environ.get("TCN_DPX", "1.6"))      # pixel atlas mỗi đơn vị rig (con cao ~360 đơn vị)
MANH = os.path.join(G.BASE, "manh")
RA = os.environ.get("TCN_RA") or os.path.join(G.BASE, "rig")
COT_ANH = os.path.join(HERE, "inbox", "tuong_cot_1", "manh", "cot.png")
FPS = 30.0
TAN = 0.45
CAO = 380.0

# mảnh (thứ tự vẽ sau → trước) → xương gốc
MANH_XUONG = [("chan_phai", "bone4"), ("chan_trai", "bone3"), ("tay_phai", "bone7"), ("than", "shenti"), ("loi", "shenti"),
              ("mu", "bone8"), ("mat", "shenti"), ("mat_nham", "shenti"), ("tay_trai", "bone6")]


def ease(u, k="io"):
    u = min(1.0, max(0.0, u))
    if k == "io":
        return u * u * (3 - 2 * u)
    if k == "out":
        return 1 - (1 - u) ** 2
    if k == "in":
        return u * u
    if k == "back":
        c = 1.7
        return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
    return u


def nap():
    scan = G.scan()
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    S = json.load(open(os.path.join(scan, "sample_goc.json"), encoding="utf-8"))
    return D0, I, S


def mats(Dj):
    return {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in Dj["bones"]}


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    c = json.load(open(os.path.join(G.MAU, "can.json")))
    s, cx, cy, k, tx, ty = j["s"], j["cx"], j["cy"], c["k"], c["tx"], c["ty"]
    to_rig = lambda P: np.stack([cx + (k * P[:, 0] + tx - 768) / s, cy - (k * P[:, 1] + ty - 512) / s], 1)   # noqa: E731
    return s / k, to_rig


def anh_manh(ten):
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    s_px, _ = tf()
    g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


def dung(far_xy=None):
    D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wi = mats(D0)
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    goc0 = {}
    for b in IB:
        nm = b["name"]
        if nm in ("root", "shadow"):
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        goc0[nm] = g
        sk.xuong(nm, "move" if cha == "root" else cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    _, to_rig = tf()
    LOC, WIM, TAM = {}, {}, {}
    for m, b in MANH_XUONG:
        im, (x0, y0, x1, y1), kq = anh_manh(m)
        sk.anh(m, im)
        bv = max(4.0, min(10.0, 0.06 * min(im.width, im.height)))
        L = luoi.luoi_vung(im, buoc_vien=bv, buoc_trong=bv * 1.5, vien=2, ten=m, in_tk=False)
        V = to_rig(np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1))
        c = V.mean(0)
        TAM[m] = c
        lp = np.linalg.solve(Wi[b], np.array([c[0], c[1], 1.0]))
        xb = f"m_{m}"
        sk.xuong(xb, b, float(lp[0]), float(lp[1]))
        Wm_i = Wi[b] @ khung.mat(float(lp[0]), float(lp[1]), 0.0)
        loc = np.linalg.solve(Wm_i, np.vstack([V.T, np.ones(len(V))]))
        Vs = (sk.W0[xb] @ loc)[:2].T
        sk.slot(m, "move", m, an=(m == "mat_nham"))
        sk.luoi_gan(m, m, L, [{xb: 1.0}] * L.n, the_gioi=Vs)
        LOC[m], WIM[m] = loc[:2], Wm_i
    sk.xuong("mieng", "move", 0.0, 0.0)
    # cột nhỏ (chiêu cuối): mượn ảnh cột của dạng 2, dựng ĐỨNG (đầu vỡ lên trên), dài ~1,05 chiều cao con
    g = Image.open(COT_ANH).convert("RGBA")
    A = np.asarray(g)[..., 3] > 60
    ys, xs = np.nonzero(A)
    P = np.stack([xs, ys], 1).astype(float)
    P -= P.mean(0)
    w_, v_ = np.linalg.eigh(np.cov(P.T))
    ax = v_[:, np.argmax(w_)]
    if ax[0] + ax[1] > 0:                                     # chiều từ chân cột (dưới phải) tới đầu vỡ (trên trái)
        ax = -ax
    dai_px = float(np.ptp(P @ ax))
    dai = 1.05 * CAO
    kq = dai * D_PX / dai_px
    g2 = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    sk.anh("cot", anh.loang_mau(g2))
    goc_ = 90.0 - math.degrees(math.atan2(-ax[1], ax[0]))
    sk.xuong("far", "root", *(far_xy if far_xy is not None else (1.6 * CAO, 0.45 * CAO)))
    sk.xuong("fly_cot", "root", 0.0, 0.0)
    sk.xuong("cot_bay", "fly_cot", 0.0, dai / 2)
    sk.slot("cot_bay", "cot_bay", "cot", an=True)          # hình cứng trong Spine bám xương của SLOT
    sk.manh("cot_bay", "cot", khung.Dat(0.0, dai / 2, goc=goc_, ti=1.0 / D_PX), xuong="cot_bay")
    for e, mo in (("trung", "khung trúng"), ("lan_dung", "appear: lăn tới, dừng (bụi)"), ("bung", "appear: bung tay chân, vương miện"),
                  ("loi_sang", "appear: lõi pha lê sáng"), ("cam", "cast: nện hai nắm tay xuống đất, rễ con chạy tới đối thủ"),
                  ("goi", "skill: gồng gọi cột (lá hút vào lõi)"), ("giang", "skill: cột nhỏ bắt đầu rơi xuống đối thủ"),
                  ("tat", "die: lõi tắt")):
        sk.su_kien(e, mo)
    info = dict(IB=IB, ten=ten, goc0=goc0, S=S, I=I, loc=LOC, wim=WIM, tam=TAM, dai_cot=dai)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot")
    return sk, info


def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
    sl = [s["name"] for s in info["I"]["slots"]]
    jh = sl.index("P_hit")
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        L = np.array([F["l"] for F in fr], float)
        res = {}
        for i, n in enumerate(ten):
            if n not in goc0:
                continue
            g = goc0[n]
            A = np.stack([L[:, i, 2] - g[2], L[:, i, 0] - g[0], L[:, i, 1] - g[1], L[:, i, 3] / (g[3] or 1.0), L[:, i, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            if np.abs(A - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[n] = A
        nham = np.array([1.0 if (F["n"][jh] and F["a"][jh] > 0.01) else 0.0 for F in fr])
        out[clip] = (float(v["dur"]), res, len(fr), nham)
    return out


def lam_clip(sk, info, cao=CAO):
    CD = chuyen_dong(info)
    bones = {b["name"]: b for b in sk.bones}
    far = sk.W0["far"][:2, 2]
    dai_cot = info["dai_cot"]
    o_xy = sk.W0["xy"][:2, 2]
    tam_than = info["tam"]["than"]

    def dat(P, goc, tau, lap=False, bo=None):
        dur, R, n, nham = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if bo is not None and b in bo:
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        return nham[min(int(round(x)), n - 1)] > 0.5

    def nham_mat(P, k=True):
        P.alpha["mat"] = 0.0 if k else 1.0
        P.alpha["mat_nham"] = 1.0 if k else 0.0

    def pha(Pa, Pb, w):
        Q = Pa.copy()
        for b in set(Pa.t) | set(Pb.t):
            a_ = Pa.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            dr = (b_[2] - a_[2] + 180.0) % 360.0 - 180.0
            Q.t[b] = [a_[0] + (b_[0] - a_[0]) * w, a_[1] + (b_[1] - a_[1]) * w, a_[2] + dr * w,
                      a_[3] + (b_[3] - a_[3]) * w, a_[4] + (b_[4] - a_[4]) * w]
        return Q

    def chep(P, Q):
        al = dict(P.alpha)
        P.t.clear()
        P.t.update({k: list(v) for k, v in Q.t.items()})
        P.alpha.update(al)

    def lat(P, theta):
        """xoay cả thân quanh tâm thân (lăn) theta độ; xương xoay là `xy` (cha của thân và tay chân)."""
        g = P.t.get("xy", [0.0, 0.0, 0.0, 1.0, 1.0])
        c = tam_than + np.array([g[0], g[1]])
        o = o_xy + np.array([g[0], g[1]])
        th = math.radians(theta)
        R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        d = c + R @ (o - c) - o
        P.move("xy", float(d[0]), float(d[1]))
        P.rot("xy", theta)

    def song_(t, tre, chu=2.0):
        return math.sin(2 * math.pi * (t - tre) / chu)

    P_idle0 = khung.Pose()
    dat(P_idle0, "idle_01", 0.0)

    # ------------------------------------------------ idle: idle_01 + lõi phồng xẹp, vương miện lắc nhẹ, chớp mắt
    D_IDLE = 4.0

    def f_idle(t, P):
        dat(P, "idle_01", t, True)
        s = 1 + 0.05 * song_(t, 0.0)
        P.scale("m_loi", s, s)
        P.rot("m_mu", 2.0 * song_(t, 0.25))
        nham_mat(P, 2.60 < t < 2.72 or 2.86 < t < 2.96)

    # ------------------------------------------------ walk: chạy nhảy cóc của họ
    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        nham_mat(P, dat(P, "hit_01", t))
        k = math.exp(-((t - 0.06) / 0.06) ** 2)
        P.scale("m_loi", 1 - 0.3 * k, 1 - 0.3 * k)

    # ------------------------------------------------ appear: LĂN TỚI (cuộn tròn lăn vào, dừng, bung tay chân + vương miện, lõi sáng, vung tay)
    T_DUNG, T_BUNG, T_LOI, D_APPEAR = 0.72, 0.80, 1.06, 2.0
    THU = ("m_tay_trai", "m_tay_phai", "m_chan_trai", "m_chan_phai", "m_mu")

    def f_appear(t, P):
        dat(P, "idle_01", 0.0)
        a = min(1.0, t / 0.15)
        nham_mat(P, t < T_LOI)
        for s_ in ("than", "loi", "mu", "mat", "mat_nham", "tay_trai", "tay_phai", "chan_trai", "chan_phai"):
            P.alpha[s_] = a * P.alpha.get(s_, 1.0)
        for j, s_ in enumerate(("tay_trai", "tay_phai", "chan_trai", "chan_phai", "mu")):      # thu hẳn vào trong lúc lăn
            P.alpha[s_] = P.alpha[s_] * (1.0 if t >= T_BUNG + 0.05 * j else 0.0)
        if t < T_DUNG:                                 # lăn từ trái vào: một vòng tròn
            u = ease(t / T_DUNG, "out")
            P.move("move", -1.5 * cao * (1 - u), 0.0)
            lat(P, -360.0 * u)
        else:
            lat(P, -360.0)
            tb = t - T_DUNG
            k = math.exp(-tb / 0.07) * math.cos(tb * 2 * math.pi / 0.16)
            P.scale("bone2", 1 + 0.10 * k, 1 - 0.10 * k)
        # tay chân, vương miện thu vào rồi bung (so le)
        for j, xb in enumerate(THU):
            t0 = T_BUNG + 0.05 * j
            s = 0.12 if t < t0 else 0.12 + 0.88 * ease((t - t0) / 0.22, "back")
            P.scale(xb, s, s)
        if t < T_LOI:
            P.scale("m_loi", 0.2, 0.2)
        elif t < T_LOI + 0.3:
            u = (t - T_LOI) / 0.3
            s = 0.2 + 1.0 * ease(min(1.0, u / 0.55), "out") - 0.2 * ease(max(0.0, (u - 0.55) / 0.45))
            P.scale("m_loi", s, s)
        # vung hai nắm tay lên (quả quyết) rồi về
        if t > 1.15:
            g = math.sin(math.pi * min(1.0, (t - 1.15) / 0.6))
            P.rot("bone6", 40.0 * g)
            P.rot("bone7", -40.0 * g)
            P.move("xy", 0.0, 22.0 * g)
            P.rot("m_mu", 4.0 * math.sin(2 * math.pi * (t - 1.15) / 0.3) * g)

    # ------------------------------------------------ attack: HÚC VƯƠNG MIỆN (ngả ra sau lấy đà, lao tới húc chóp vương miện, bật lại)
    T_ATK, D_ATK = 0.46, 1.0

    def f_attack(t, P):
        dat(P, "idle_01", 0.0)
        if t < 0.30:                                   # lấy đà: ngả ra sau, nén
            u = ease(t / 0.30)
            rot, dx, sq = 18.0 * u, -0.10 * cao * u, 0.08 * u
        elif t < T_ATK:                                # lao: chúi đầu tới
            u = ease((t - 0.30) / (T_ATK - 0.30), "in")
            rot, dx, sq = 18.0 - 46.0 * u, (-0.10 + 0.62 * u) * cao, 0.08 - 0.16 * u
        elif t < T_ATK + 0.10:
            rot, dx, sq = -28.0, 0.52 * cao, -0.08
        else:                                          # bật lại về chỗ
            u = ease((t - T_ATK - 0.10) / (D_ATK - T_ATK - 0.14))
            rot, dx, sq = -28.0 * (1 - u) + 6.0 * math.sin(math.pi * u), 0.52 * cao * (1 - u), -0.08 * (1 - u)
        P.move("move", float(dx), 0.0)
        P.rot("bone2", rot)
        P.scale("bone2", 1 - sq, 1 + sq)
        P.rot("bone6", 0.8 * rot)
        P.rot("bone7", 0.8 * rot)
        k = math.exp(-((t - T_ATK - 0.015) / 0.04) ** 2)
        P.scale("bone2", 1 + 0.08 * k, 1 - 0.06 * k)
        nham_mat(P, T_ATK - 0.02 < t < T_ATK + 0.10)

    # ------------------------------------------------ cast: RỄ CON (nén người, giơ hai nắm tay, nện xuống đất; rễ con chạy ngầm tới đối thủ)
    T_CAM, T_RE, D_CAST = 0.62, 0.95, 1.5

    def f_cast(t, P):
        dat(P, "idle_01", 0.0)
        if t < 0.44:                                   # giơ hai tay lên, nhón người
            u = ease(t / 0.44)
            tay, y, sq = 70.0 * u, 26.0 * u, -0.06 * u
        elif t < T_CAM:                                # nện
            u = ease((t - 0.44) / (T_CAM - 0.44), "in")
            tay, y, sq = 70.0 - 110.0 * u, 26.0 - 38.0 * u, -0.06 + 0.18 * u
        elif t < 1.10:                                 # giữ, gồng
            v = math.sin(math.pi * (t - T_CAM) / (1.10 - T_CAM))
            tay, y, sq = -40.0, -12.0 + 3.0 * v, 0.12 - 0.04 * v
            s = 1 + 0.18 * v
            P.scale("m_loi", s, s)
        else:
            u = ease((t - 1.10) / (D_CAST - 0.05 - 1.10))
            tay, y, sq = -40.0 * (1 - u), -12.0 * (1 - u), 0.12 * (1 - u)
        P.rot("bone6", tay)
        P.rot("bone7", -tay)
        P.move("xy", 0.0, y)
        P.scale("bone2", 1 + sq, 1 - sq)
        nham_mat(P, T_CAM - 0.02 < t < T_CAM + 0.12)
        P.move("mieng", float(tam_than[0] + 0.3 * cao), 0.0)

    # ------------------------------------------------ skill: TIỂU TRỤ GIÁNG (giơ hai tay gồng gọi; cột đá nhỏ từ trời giáng xuống đối thủ,
    # cắm rung rồi lún mờ; nhảy cẫng lên)
    T_GOI, T_GIANG, T_SKILL, T_TAN, D_SKILL = 0.30, 0.95, 1.18, 1.70, 2.2

    def f_skill(t, P):
        dat(P, "idle_01", 0.0)
        up = ease(t / 0.30) if t < T_GIANG else 1 - ease((t - T_GIANG) / 0.2)
        P.rot("bone6", 95.0 * up)
        P.rot("bone7", -95.0 * up)
        P.move("xy", 0.0, 18.0 * up)
        if T_GOI < t < T_GIANG:
            g = ease((t - T_GOI) / (T_GIANG - T_GOI), "in")
            s = 1 + 0.30 * g
            P.scale("m_loi", s, s)
            P.rot("bone2", 2.5 * math.sin(2 * math.pi * (t - T_GOI) / 0.18) * g)
        if T_GIANG <= t < T_GIANG + 0.25:              # chỉ tay xuống đối thủ
            u = math.sin(math.pi * (t - T_GIANG) / 0.25)
            P.rot("bone2", -12.0 * u)
        tb = t - T_SKILL
        if 0.0 < tb < 0.6:                             # nhảy cẫng
            u = tb / 0.6
            P.move("xy", 0.0, 0.25 * cao * math.sin(math.pi * u) * (1 - u))
            P.rot("bone6", 50.0 * math.sin(math.pi * u))
            P.rot("bone7", -50.0 * math.sin(math.pi * u))
        # cột nhỏ
        if T_GIANG <= t < T_TAN + 0.3:
            P.alpha["cot_bay"] = 1.0
            P.move("fly_cot", float(far[0] - 0.12 * cao), float(far[1] - 0.45 * cao))     # mặt đất dưới đối thủ, hơi lệch về phía trước
            if t < T_SKILL:
                u = ease((t - T_GIANG) / (T_SKILL - T_GIANG), "in")
                P.move("cot_bay", 0.0, 2.2 * cao * (1 - u) - 14.0)
            else:
                tb = t - T_SKILL
                k = math.exp(-tb / 0.1) * math.sin(tb * 2 * math.pi / 0.14)
                lun = ease((t - T_TAN) / 0.3) if t > T_TAN else 0.0
                P.move("cot_bay", 0.0, -14.0 - 6.0 * k - 0.35 * dai_cot * lun)
                P.rot("cot_bay", 2.0 * k)
                P.alpha["cot_bay"] = 1.0 - lun

    # ------------------------------------------------ die: die_01 của họ + mắt nhắm + lõi tắt + mờ
    def f_die(t, P):
        d = CD["die_01"][0]
        nham_mat(P, dat(P, "die_01", t) or t > 0.07)
        if t > 0.25:
            P.alpha["loi"] = max(0.0, 1 - (t - 0.25) / 0.2)
        if t > d:
            a = max(0.0, 1 - (t - d) / (TAN - 0.05))
            for sl in sk.slots:
                P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], 1.0 if sl["alpha"] > 0 else 0.0)

    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_DUNG, "lan_dung", ""), (T_BUNG, "bung", ""), (T_LOI, "loi_sang", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", D_ATK, f_attack, ev=[(T_ATK, "trung", "")], trung=T_ATK),
        Clip("cast", D_CAST, f_cast, ev=[(T_CAM, "cam", ""), (T_RE, "trung", "")], trung=T_RE),
        Clip("skill", D_SKILL, f_skill, ev=[(T_GOI, "goi", ""), (T_GIANG, "giang", ""), (T_SKILL, "trung", "")], trung=T_SKILL),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die, ev=[(0.25, "tat", "")]),
    ]
    return clips


def soi_clip(sk, clips, a):
    ve0 = soi.Ve(sk)
    c = [x for x in clips if x.ten == a[1]][0]
    fr = hoat.nuong(sk, c)
    if ":" in a[2]:
        t0, t1, n = a[2].split(":")
        ts = list(np.linspace(float(t0), float(t1), int(n)))
    elif a[2].startswith("n="):
        ts = list(np.linspace(0, c.dur, int(a[2][2:])))
    else:
        ts = [float(x) for x in a[2].split(",")]
    Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
    Bx = soi._union([ve0.bao(P) for P in Ps], 0.04)
    sc = float(a[3]) if len(a) > 3 else 0.6
    cot = min(len(Ps), 6)
    hang = (len(Ps) + cot - 1) // cot
    out = None
    for i, P in enumerate(Ps):
        im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
        ImageDraw.Draw(im).text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
        if out is None:
            out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    os.makedirs(RA, exist_ok=True)
    pth = os.path.join(RA, f"soi_{a[1]}.png")
    out.save(pth)
    print(pth, out.size)


def dung_het(far_xy=None):
    """cho bản xem trước có đối thủ (tho5_fx.Tuong)."""
    sk, info = dung(far_xy)
    clips = lam_clip(sk, info)
    cao = soi.chieu_cao(soi.Ve(sk), hoat.nuong(sk, clips[1])[0])
    return sk, info, lam_clip(sk, info, cao), cao


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    ve0 = soi.Ve(sk)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    print(f"chiều cao {cao:.0f}")
    if a and a[0] == "soi":
        soi_clip(sk, clips, a)
        return
    if a and a[0] == "kiem":
        for c in clips:
            fr = hoat.nuong(sk, c, fps=60)
            xau = []
            for i in range(1, len(fr)):
                A, B = fr[i - 1], fr[i]
                for b in set(A.t) | set(B.t):
                    da = abs(B.t.get(b, khung.ZERO)[2] - A.t.get(b, khung.ZERO)[2])
                    if da > 25.0:
                        xau.append(f"{i / 60:.2f}s {b} xoay {da:.0f}°")
            print(f"{c.ten}: {len(fr)} khung60" + ("" if not xau else " | " + "; ".join(xau[:12])))
        return
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Cổ Vương Nhi (tuong_cot_non): dạng 1 tướng 6 đảo Mộc", dang=1, so_dang=2,
                  dung_yen=("cast", "skill"), lao=("attack",), far=("cast", "skill"), ma_goc=None, khop_idle=0.2, cao=cao,
                  tol={"rotate": 0.08, "translate": 0.06, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5)


if __name__ == "__main__":
    main(sys.argv[1:])
