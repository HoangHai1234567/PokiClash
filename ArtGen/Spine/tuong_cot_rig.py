# -*- coding: utf-8 -*-
"""Tượng vua cổ rễ quấn cầm cột đá (tuong_cot; tướng 6 đảo Mộc, ải 30): hình của mình chạy trên ĐÚNG bộ xương của con gốc monster_3608
(golem đá vác cột; game tham khảo). Ghi chú: inbox/tuong_cot_ghichu.md.

- XƯƠNG: mọi xương bộ chính của họ (FK thuần, không IK); bỏ shadow và bộ xương rời (P_*2 ... dùng cho run_01 / die_01 của họ). Thêm:
  `move` (sân đo lao), `m_<mảnh>` (một xương riêng cho mỗi mảnh, con của xương gốc của nó, đặt ở tâm mảnh: clip appear / die tách
  từng mảnh bay riêng mà không kéo theo xương con), `far` (chỗ đối thủ mặc định), `fly_cot` → `cot_bay` (cột bay ở chiêu cuối: game co
  quãng theo đối thủ thật, AolaActor.FarAtomik), `mieng` (chỗ phát VFX).
- MẢNH: mảnh cứng "đúng chỗ, đúng cỡ" trên concept (tuong_cot_manh.py → inbox/tuong_cot_1/manh/), concept căn lên con gốc bằng co + dời
  (mau/can.json); mỗi mảnh bám cứng xương m_ của nó, đặt sao cho ở khung 0 idle trùng chỗ trên concept.
Xương và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tuong_cot_rig.py    → inbox/tuong_cot_1/rig/
    py -3 -I ArtGen/Spine/tuong_cot_rig.py soi <clip> <giây,...|n=12|t0:t1:n> [tỉ lệ]   → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/tuong_cot_rig.py kiem                            đo góc nhảy / bước dời từng clip
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy.optimize import linear_sum_assignment

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, khung, hoat, xuat, soi, luoi  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import tho5  # noqa: E402

tho5.CON["tuong_cot"] = ("monster_3608", 6, 30)
G = tho5.dat("tuong_cot")
TEN_RIG = "tuong_cot_1"
D_PX = float(os.environ.get("TC_DPX", "0.5"))       # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~1250 đơn vị)
MANH = os.path.join(G.BASE, "manh")
RA = os.environ.get("TC_RA") or os.path.join(G.BASE, "rig")
FPS = 30.0
TAN = 0.45
CAO = 1266.0                     # chiều cao game đo ở khung 0 idle

# mảnh của mình (thứ tự vẽ sau → trước) → xương gốc. "pha_le_x*" là pha lê mượn ảnh đặt ở chỗ part gốc (khuất lúc nghỉ).
MANH_XUONG = [
    ("tay_xa", "bone20"), ("pha_le_x4", "bone52"), ("pha_le_x5", "bone51"), ("pha_le_x6", "bone53"), ("hong_x", "bone3"),
    ("vai_xa", "P_jianjiaL03"), ("hong", "bone2"), ("than", "bone3"), ("da_*", None), ("cot", "bone54"), ("nam_xa", "bone21"),
    ("lung", "bone39"), ("dau", "bone4"), ("loi", "bone3"), ("pha_le_x1", "bone48"), ("pha_le_1", "bone50"), ("pha_le_2", "bone49"),
    ("vai_gan", "bone17"), ("nam_gan", "bone8"), ("tay_gan", "bone7"),
]
PHA_LE_MUON = {"pha_le_x1": ("P_jiejing01", "pha_le_1"), "pha_le_x4": ("P_jiejing04", "pha_le_2"), "pha_le_x5": ("P_jiejing05", "pha_le_1"),
               "pha_le_x6": ("P_jiejing06", "pha_le_2")}
DA_GOC = {"P_shitou01": "bone31", "P_shitou02": "bone32", "P_shitou03": "bone33", "P_shitou04": "bone34", "P_shitou05": "bone37",
          "P_shitou06": "bone38", "P_shitou07": "bone35", "P_shitou08": "bone36"}
# xương của các phần (con quay phải; GẦN = nửa trái tranh = R của họ)
TAY_GAN = ("bone6", "bone7", "bone8")          # vai (gốc chung vai + tay gần), cánh tay, nắm tay
TAY_XA = ("bone18", "bone19", "bone20", "bone21")
THAN = ("bone", "bone40", "bone2", "bone3")
DAU = "bone4"


# ---------------------------------------------------------------- nạp
def nap():
    scan = G.scan()
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    S = json.load(open(os.path.join(scan, "sample_goc.json"), encoding="utf-8"))
    return D0, I, S


def mats(Dj):
    return {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in Dj["bones"]}


def tf():
    """px concept → toạ độ rig (qua phép căn co k + dời của mau/can.json rồi phép đổi của goc_ca_con)."""
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    c = json.load(open(os.path.join(G.MAU, "can.json")))
    s, cx, cy, k, tx, ty = j["s"], j["cx"], j["cy"], c["k"], c["tx"], c["ty"]
    to_rig = lambda P: np.stack([cx + (k * P[:, 0] + tx - 768) / s, cy - (k * P[:, 1] + ty - 512) / s], 1)   # noqa: E731
    to_px = lambda V: np.stack([((V[:, 0] - cx) * s + 768 - tx) / k, ((cy - V[:, 1]) * s + 512 - ty) / k], 1)  # noqa: E731
    return s / k, to_rig, to_px


def bo_xuong(I):
    """xương bộ rời (con của `bone` tên P_*, và cháu của chúng) + shadow: bỏ."""
    ten = [b["name"] for b in I["bones"]]
    bo = {"shadow"}
    for b in I["bones"]:
        p = b["parent"]
        cha = ten[p] if p is not None and p >= 0 else None
        if (cha == "bone" and b["name"].startswith("P_")) or cha in bo:
            bo.add(b["name"])
    return bo


def gan_da(D0):
    """ghép 8 viên đá của mình với 8 viên của họ theo tâm (thuật toán Hungary)."""
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    _, to_rig, _ = tf()
    mine = sorted([k for k in DATJ if k.startswith("da_")], key=lambda k: int(k.split("_")[1]))
    by0 = {a["slot"]: a for a in D0["atts"]}
    goc = list(DA_GOC)
    cm = np.array([to_rig(np.array([[(DATJ[k]["hop"][0] + DATJ[k]["hop"][2]) / 2, (DATJ[k]["hop"][1] + DATJ[k]["hop"][3]) / 2]]))[0]
                   for k in mine])
    cg = np.array([np.array(by0[s]["xy"], float).reshape(-1, 2).mean(0) for s in goc])
    C = np.hypot(cm[:, None, 0] - cg[None, :, 0], cm[:, None, 1] - cg[None, :, 1])
    r, c = linear_sum_assignment(C)
    return {mine[i]: DA_GOC[goc[j]] for i, j in zip(r, c)}


def anh_manh(ten):
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    s_px, _, _ = tf()
    g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


# ---------------------------------------------------------------- dựng
def dung(far_xy=None):
    D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    BO = bo_xuong(I)
    Wi = mats(D0)
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    goc0 = {}
    for b in IB:
        nm = b["name"]
        if nm == "root" or nm in BO:
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        goc0[nm] = g
        sk.xuong(nm, "move" if cha == "root" else cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    s_px, to_rig, _ = tf()
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    by0 = {a["slot"]: a for a in D0["atts"]}
    da = gan_da(D0)
    ds = []
    for m, b in MANH_XUONG:
        if m.endswith("*"):
            ds += [(k, da[k]) for k in sorted(da, key=lambda k: int(k.split("_")[1]))]
        else:
            ds.append((m, b))
    tong = [0, 0]
    tam_px = {}
    LOC, WIM = {}, {}
    for m, b in ds:
        if m in PHA_LE_MUON:                                        # pha lê mượn ảnh, đặt theo khung part gốc
            part, src = PHA_LE_MUON[m]
            im0, _, kq = anh_manh(src)
            Q = np.array(by0[part]["xy"], float).reshape(-1, 2)
            q0, q1 = Q.min(0), Q.max(0)
            hcao = q1[1] - q0[1]
            k2 = hcao * D_PX / im0.height
            im = im0.convert("RGBa").resize((max(2, round(im0.width * k2)), max(2, round(im0.height * k2))), Image.LANCZOS).convert("RGBA")
            sk.anh(m, im)
            c = (q0 + q1) / 2
            L = luoi.luoi_vung(im, buoc_vien=6.0, buoc_trong=9.0, vien=2, ten=m, in_tk=False)
            V = np.stack([c[0] + (L.pts[:, 0] - im.width / 2) / D_PX, c[1] - (L.pts[:, 1] - im.height / 2) / D_PX], 1)
        else:
            im, (x0, y0, x1, y1), kq = anh_manh(m)
            sk.anh(m, im)
            bv = max(6.0, min(12.0, 0.06 * min(im.width, im.height)))
            L = luoi.luoi_vung(im, buoc_vien=bv, buoc_trong=bv * 1.5, vien=2, ten=m, in_tk=False)
            V = to_rig(np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1))      # thế giới ở khung 0 idle
        c = V.mean(0) if m not in ("cot",) else (V.min(0) + V.max(0)) / 2
        tam_px[m] = c
        lp = np.linalg.solve(Wi[b], np.array([c[0], c[1], 1.0]))       # tâm mảnh trong hệ xương gốc (khung 0 idle)
        xb = f"m_{m}"
        sk.xuong(xb, b, float(lp[0]), float(lp[1]))
        Wm_i = Wi[b] @ khung.mat(float(lp[0]), float(lp[1]), 0.0)          # ma trận xương m_ ở khung 0 idle
        loc = np.linalg.solve(Wm_i, np.vstack([V.T, np.ones(len(V))]))
        Vs = (sk.W0[xb] @ loc)[:2].T                                        # thế giới ở dáng gốc
        sk.slot(m, "move", m)
        sk.luoi_gan(m, m, L, [{xb: 1.0}] * L.n, the_gioi=Vs)
        LOC[m] = loc[:2]
        WIM[m] = Wm_i
        tong[0] += L.n
        tong[1] += len(L.tris)
    sk.xuong("mieng", "move", 0.0, 0.0)
    # cột bay (chiêu cuối): fly_cot (con của root, x dáng gốc = tâm cột lúc nghỉ) → cot_bay (y, góc, cỡ); hình = bản sao cột, ẩn sẵn
    Wc = WIM["cot"]
    x0, y0, a0 = float(Wc[0, 2]), float(Wc[1, 2]), khung.goc_mat(Wc)
    sk.xuong("far", "root", *(far_xy if far_xy is not None else (1.6 * CAO, 0.45 * CAO)))
    sk.xuong("fly_cot", "root", x0, 0.0)
    sk.xuong("cot_bay", "fly_cot", 0.0, y0, goc=a0)
    Vb = (sk.W0["cot_bay"] @ np.vstack([LOC["cot"], np.ones(LOC["cot"].shape[1])]))[:2].T
    sk.slot("cot_bay", "move", "cot", an=True, truoc="nam_xa")
    sk.luoi_gan("cot_bay", "cot", sk.luoi[("cot", "cot")], [{"cot_bay": 1.0}] * len(Vb), the_gioi=Vb)
    for e, mo in (("trung", "khung trúng"), ("cam_cot", "appear: cột rơi cắm xuống đất (bụi, rung)"),
                  ("loi_sang", "appear: lõi pha lê bừng sáng"), ("dat_dau", "appear / idle: đầu đặt xuống cổ (bụi nhỏ)"),
                  ("nho_cot", "appear: nhổ cột khỏi đất vác lên vai"), ("cam", "cast: cột cắm xuống đất, rễ bắt đầu chạy tới đối thủ"),
                  ("rut", "cast: rút cột lên"), ("nem_cot", "skill: tung cột lên trời"), ("tu", "skill: gồng, lá / rễ hút vào lõi"),
                  ("giang", "skill: cột khổng lồ bắt đầu giáng xuống đối thủ (bóng / vết nứt báo trước)"),
                  ("re", "skill: rễ trồi quanh cột cắm"), ("bat_cot", "skill: cột bay về, bắt lại"), ("tat", "die: lõi tắt"),
                  ("sup", "die: bắt đầu sụp"), ("do", "die: cột đổ chạm đất")):
        sk.su_kien(e, mo)
    info = dict(IB=IB, ten=ten, goc0=goc0, S=S, Wi=Wi, manh=[m for m, _ in ds], xuong_manh=dict(ds), tam=tam_px, loc=LOC, wim=WIM)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác")
    return sk, info


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
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
        out[clip] = (float(v["dur"]), res, len(fr))
    return out


def ease(u, k="io"):
    u = min(1.0, max(0.0, u))
    if k == "io":
        return u * u * (3 - 2 * u)
    if k == "out":
        return 1 - (1 - u) ** 2
    if k == "in":
        return u * u
    if k == "back":                                   # ra quá đà rồi về (đáp mảnh vào chỗ)
        c = 1.7
        return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
    if k == "em":                                     # bậc năm: vận tốc + gia tốc 0 hai đầu
        return u * u * u * (u * (6 * u - 15) + 10)
    return u


def tmap(t, moc):
    """ánh xạ giờ từng đoạn: moc = [(t, tau[, kiểu])...]; kiểu áp cho đoạn KẾT THÚC ở mốc đó."""
    if t <= moc[0][0]:
        return moc[0][1]
    for a, b in zip(moc, moc[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(1e-9, b[0] - a[0])
            return a[1] + (b[1] - a[1]) * ease(u, b[2] if len(b) > 2 else "lin")
    return moc[-1][1]


def _r(i, k):
    """số giả ngẫu nhiên cố định trong [-1, 1] theo (mảnh, khoá)."""
    return math.sin(12.9898 * (i + 1) + 78.233 * (k + 1)) * 0.5 + math.sin(4.1 * (i + 3) * (k + 2)) * 0.5


# mốc giờ
M_ATTACK = [(0.0, 0.0), (1.20, 1.20)]
T_ATK = 0.50
M_CAST = [(0.0, 0.0), (0.76, 0.76, "lin"), (0.82, 0.86, "out"), (1.34, 1.06, "lin"), (1.95, 1.67, "io")]
T_CAM, T_RE, T_RUT, D_CAST = 0.76, 1.12, 1.36, 1.95
T_NEM, T_TU, T_CHI, T_GIANG, T_SKILL, T_RE2, T_LEN, T_BAT, D_SKILL = 0.56, 0.62, 1.22, 1.42, 1.64, 1.72, 2.08, 2.62, 3.05
T_CAMCOT, T_LOI, T_DAU, T_NHO, D_APPEAR = 0.32, 1.06, 1.32, 1.46, 2.85
T_TAT, T_SUP, T_DO, D_DIE = 0.30, 0.34, 0.86, 1.75


def lam_clip(sk, info, cao=CAO):
    CD = chuyen_dong(info)
    manh = info["manh"]
    LOC = info["loc"]
    bones = {b["name"]: b for b in sk.bones}
    far = sk.W0["far"][:2, 2]
    x0c = float(sk.W0["fly_cot"][0, 2])
    yb0, ab0 = float(sk.W0["cot_bay"][1, 2]), khung.goc_mat(sk.W0["cot_bay"])
    half_cot = float(LOC["cot"][0].max())                       # nửa chiều dài cột (trục x của xương cột)
    day_cot = float(LOC["cot"][1].max())

    def dat(P, goc, tau, lap=False, chi=None, bo=None, k=1.0):
        dur, R, n = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if (chi is not None and b not in chi) or (bo is not None and b in bo):
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, k * float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, k * float(v[1]), k * float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, 1 + k * (float(v[3]) - 1), 1 + k * (float(v[4]) - 1))

    def pha(Pa, Pb, w):
        Q = Pa.copy()
        for b in set(Pa.t) | set(Pb.t):
            a_ = Pa.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            dr = (b_[2] - a_[2] + 180.0) % 360.0 - 180.0
            Q.t[b] = [a_[0] + (b_[0] - a_[0]) * w, a_[1] + (b_[1] - a_[1]) * w, a_[2] + dr * w,
                      a_[3] + (b_[3] - a_[3]) * w, a_[4] + (b_[4] - a_[4]) * w]
        for s_ in set(Pa.alpha) | set(Pb.alpha):
            Q.alpha[s_] = Pa.alpha.get(s_, 1.0) + (Pb.alpha.get(s_, 1.0) - Pa.alpha.get(s_, 1.0)) * w
        return Q

    def chep(P, Q):
        P.t.clear()
        P.t.update({k: list(v) for k, v in Q.t.items()})
        P.alpha.clear()
        P.alpha.update(Q.alpha)

    def dat_tg(P, Wc, xb, Wd, them=0.0):
        """đặt xương lá xb sao cho ma trận thế giới = Wd @ R(them) (them: xoay thêm quanh gốc xương, không quấn vòng)."""
        b = bones[xb]
        Lm = np.linalg.solve(Wc[b["parent"]], Wd)
        r = math.degrees(math.atan2(Lm[1, 0], Lm[0, 0]))
        sx = math.hypot(Lm[0, 0], Lm[1, 0])
        sy = (Lm[0, 0] * Lm[1, 1] - Lm[0, 1] * Lm[1, 0]) / max(sx, 1e-9)
        dr = (r - b["rot"] + 180.0) % 360.0 - 180.0 + them
        P.t[xb] = [float(Lm[0, 2] - b["x"]), float(Lm[1, 2] - b["y"]), float(dr), sx / b["sx"], sy / b["sy"]]

    def day_(Wm, da=0.0):
        """độ cao điểm thấp nhất của mảnh (so với tâm) khi xoay thêm da độ."""
        R = khung.mat(0, 0, da)
        A = (Wm[:2, :2] @ R[:2, :2])
        return A, None

    def thap(m, Wm, da):
        A = Wm[:2, :2] @ khung.mat(0, 0, da)[:2, :2]
        return float((A @ LOC[m])[1].min())

    def song_(t, tre, chu=2.0):
        return math.sin(2 * math.pi * (t - tre) / chu)

    RINV = {}
    for b in sk.bones:
        if b["name"].startswith("m_"):
            Wp = info["Wi"][b["parent"]] if b["parent"] in info["Wi"] else sk.W0[b["parent"]]
            RINV[b["name"]] = np.linalg.inv(Wp[:2, :2])

    def mv(P, xb, dx, dy):
        """dời xương m_ theo trục THẾ GIỚI (dx, dy), quy về trục xương cha ở khung 0 idle."""
        d = RINV[xb] @ np.array([dx, dy])
        P.move(xb, float(d[0]), float(d[1]))

    def em(u):
        return ease(u, "em")

    DA = [m for m in manh if m.startswith("da_")]
    PL = [m for m in manh if m.startswith("pha_le")]

    def phu_kien(t, P, k=1.0, chu=2.0):
        """đá lơ lửng nhấp nhô lệch pha, pha lê trôi, lõi phồng xẹp (sóng chu kỳ chu, khép vòng)."""
        for i, m in enumerate(DA):
            mv(P, f"m_{m}", 0.0, k * 7.0 * song_(t, 0.13 * i, chu))
            P.rot(f"m_{m}", k * 3.0 * song_(t, 0.21 * i + 0.3, chu))
        for i, m in enumerate(PL):
            mv(P, f"m_{m}", k * 3.0 * song_(t, 0.17 * i + 0.5, chu), k * 6.0 * song_(t, 0.19 * i, chu))
            P.rot(f"m_{m}", k * 6.0 * song_(t, 0.23 * i, chu))
        s = 1 + k * 0.035 * song_(t, 0.0, chu)
        P.scale("m_loi", s, s)

    # ------------------------------------------------ idle: idle_01 hai vòng + đá nhấp nhô + trò: đầu nhấc lên ngó cột rồi đặt xuống
    D_IDLE = 4.0
    G0, G1 = 2.15, 3.55

    def f_idle(t, P):
        dat(P, "idle_01", t, True)
        phu_kien(t, P)
        if G0 < t < G1:
            u = (t - G0) / (G1 - G0)
            nang = em(min(1.0, u / 0.35)) * (1 - em(max(0.0, (u - 0.62) / 0.38)))
            mv(P, "m_dau", -4.0 * nang, 26.0 * nang)
            P.rot("m_dau", 9.0 * nang * em(min(1.0, max(0.0, (u - 0.15) / 0.3))) - 3.0 * nang * math.sin(math.pi * min(1, max(0, (u - 0.4) / 0.3))))
            # đặt xuống: nảy nhẹ
            tb = t - (G0 + 0.62 * (G1 - G0) + 0.38 * (G1 - G0))
        tb = t - G1
        if 0 < tb < 0.3:
            b_ = math.exp(-tb / 0.07) * math.sin(tb * 2 * math.pi / 0.14)
            mv(P, "m_dau", 0.0, 4.0 * b_)
            P.scale("m_dau", 1 + 0.03 * b_, 1 - 0.03 * b_)

    # ------------------------------------------------ walk: trôi nặng nề, thân nhún hai nhịp, tay gần đưa, đá trễ
    D_WALK = 1.2

    def f_walk(t, P):
        dat(P, "idle_01", 0.0)
        ph = 2 * math.pi * t / D_WALK
        P.move("bone", 0.0, 22.0 * math.sin(2 * ph) - 6.0)
        P.rot("bone2", -3.5 + 1.5 * math.sin(2 * ph + 0.6))
        P.rot("bone4", 2.5 * math.sin(2 * ph + 1.4))
        P.rot("bone7", 9.0 * math.sin(ph))
        P.rot("bone8", 6.0 * math.sin(ph - 0.5))
        P.rot("bone17", 2.0 * math.sin(ph + 0.4))
        P.rot("bone20", -3.0 * math.sin(ph + 0.9))
        for i, m in enumerate(DA):
            mv(P, f"m_{m}", -10.0 * (1 + 0.3 * math.sin(i)), 12.0 * math.sin(2 * ph - 0.9 - 0.25 * i))
        for i, m in enumerate(PL):
            mv(P, f"m_{m}", -6.0, 8.0 * math.sin(2 * ph - 1.2 - 0.3 * i))

    # ------------------------------------------------ hit
    def f_hit(t, P):
        dat(P, "hit_01", t)
        k = math.exp(-((t - 0.08) / 0.07) ** 2)
        P.scale("m_loi", 1 - 0.25 * k, 1 - 0.25 * k)
        for i, m in enumerate(PL):
            mv(P, f"m_{m}", -14.0 * k * (1 + 0.4 * _r(i, 1)), 8.0 * k * _r(i, 2))

    # dáng khoá dùng chung (lấy từ clip của họ)
    P_idle0 = khung.Pose()
    dat(P_idle0, "idle_01", 0.0)
    P_raise = khung.Pose()                          # cột dựng thẳng giơ cao bên phải, tay gần dang ra sau giữ thăng bằng
    dat(P_raise, "skill_01", 0.68)
    P_block = khung.Pose()                          # cột dựng đứng trước mặt, chân cột chạm đất
    dat(P_block, "block_01", 0.0)
    o_bone = sk.W0["bone"][:2, 2]
    tam_than = np.mean([v for k, v in info["tam"].items() if k != "cot"], axis=0)

    def lat(P, theta, c=None):
        """xoay CẢ THÂN quanh tâm thân (thế giới) theta độ (âm = lộn tới trước, theo chiều kim đồng hồ khi quay phải)."""
        g = P.t.get("bone", [0.0, 0.0, 0.0, 1.0, 1.0])
        c = (tam_than if c is None else c) + np.array([g[0], g[1]])        # tâm thân đi theo độ dời hiện có (nhảy)
        o = o_bone + np.array([g[0], g[1]])
        th = math.radians(theta)
        R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        d = c + R @ (o - c) - o
        P.move("bone", float(d[0]), float(d[1]))
        P.rot("bone", theta)

    # ------------------------------------------------ attack: ĐẬP TRỤ (giơ cột thẳng lên trời, khựng, lao tới đập cột xuống đầu đối thủ)
    T_GIO, T_DINH = 0.30, 0.42                      # giơ xong, bắt đầu đập
    P_dap = khung.Pose()                            # dáng đập: skill_01 0,86 (cột ngang tới trước) + ép cột chúi xuống, thân đổ tới
    dat(P_dap, "skill_01", 0.86)
    P_dap.rot("bone21", -34.0)
    P_dap.rot("bone2", -9.0)
    P_dap.rot("bone4", -6.0)

    def f_attack(t, P):
        if t < T_GIO:                                # giơ cột: lấy đà ngả ra sau, nhún
            u = ease(t / T_GIO, "io")
            Q = pha(P_idle0, P_raise, u)
            Q.rot("bone2", 7.0 * u)
            Q.move("bone", 0.0, -22.0 * math.sin(math.pi * u))
        elif t < T_DINH:                             # khựng trên đỉnh (cột rung nhẹ, lõi phồng)
            Q = P_raise.copy()
            Q.rot("bone2", 7.0)
            Q.rot("bone21", 2.0 * math.sin(2 * math.pi * (t - T_GIO) / 0.12))
        elif t < T_ATK:                              # đập
            u = ease((t - T_DINH) / (T_ATK - T_DINH), "in")
            Q = pha(P_raise, P_dap, u)
            Q.rot("bone2", 7.0 * (1 - u))
        elif t < T_ATK + 0.12:                       # khựng lúc trúng
            Q = P_dap.copy()
        else:                                        # về: đường về của họ (cột vòng qua đầu lên vai), bỏ dần phần ép chúi
            u = (t - T_ATK - 0.12) / (M_ATTACK[-1][0] - T_ATK - 0.12 - 0.04)
            Q = khung.Pose()
            dat(Q, "skill_01", 0.86 + (1.50 - 0.86) * ease(u, "io"))
            e = 1 - ease(min(1.0, u / 0.35), "io")
            Q.rot("bone21", -34.0 * e)
            Q.rot("bone2", -9.0 * e)
            Q.rot("bone4", -6.0 * e)
        chep(P, Q)
        lao = ease((t - 0.18) / (T_ATK - 0.18), "in") if t < T_ATK else (1.0 if t < T_ATK + 0.12 else
                                                                         1 - ease((t - T_ATK - 0.12) / 0.6, "io"))
        P.move("move", 0.32 * cao * max(0.0, lao), 0.0)
        k = math.exp(-((t - T_ATK - 0.015) / 0.04) ** 2)
        P.scale("bone", 1 + 0.07 * k, 1 - 0.07 * k)
        g = math.sin(math.pi * min(1.0, max(0.0, (t - 0.15) / (T_ATK - 0.15))))
        P.scale("m_loi", 1 + 0.12 * g, 1 + 0.12 * g)
        phu_kien(t, P, 0.5)

    # ------------------------------------------------ cast: RỄ TRÓI ĐẤT (nhún, bật nhảy giơ cột qua đầu, nện cột cắm xuống đất; gồng
    # cho rễ chạy ngầm tới đối thủ; rút cột). Không dùng skill_02 của họ: nó có hai khoá bậc (bật ngửa → đứng trong một khung, tụt thân
    # 270 đơn vị trong một khung) lộ rõ ở hình to.
    T_NHUN, T_DINH2, T_LAT0, T_LAT1 = 0.22, 0.46, 0.24, 0.69
    H_NHAY = 0.42 * cao

    def f_cast(t, P):
        # dáng tay + cột
        if t < 0.34:
            Q = pha(P_idle0, P_raise, ease(t / 0.34, "io"))
        elif t < 0.58:
            Q = P_raise.copy()
        elif t < T_CAM:
            Q = pha(P_raise, P_block, ease((t - 0.58) / (T_CAM - 0.58), "in"))
        elif t < T_RUT:
            Q = P_block.copy()
            v = math.sin(math.pi * (t - T_CAM) / (T_RUT - T_CAM))
            Q.rot("bone2", -5.0 * v)                                  # tì người vào cột, gồng
            Q.rot("bone4", 4.0 * v)
            Q.move("bone", 0.0, -10.0 * v)
            s_ = 1 + 0.16 * v
            Q.scale("m_loi", s_, s_)
        else:
            Pa = khung.Pose()
            dat(Pa, "block_01", tmap(t, [(T_RUT, 0.0), (T_RUT + 0.14, 0.10, "io"), (T_RUT + 0.44, 0.50, "io")]))
            Q = pha(Pa, P_idle0, ease((t - (T_RUT + 0.34)) / (D_CAST - 0.05 - T_RUT - 0.34), "io"))
        chep(P, Q)
        # nhún → bật → rơi nện
        if t < T_NHUN:
            h = -45.0 * ease(t / T_NHUN, "io")
        elif t < T_DINH2:
            h = -45.0 + (H_NHAY + 45.0) * ease((t - T_NHUN) / (T_DINH2 - T_NHUN), "out")
        elif t < T_CAM:
            h = H_NHAY * (1 - ease((t - T_DINH2) / (T_CAM - T_DINH2), "in"))
        else:
            h = 0.0
        P.move("bone", 0.0, h)
        if t < T_NHUN:
            q = ease(t / T_NHUN)
            P.scale("bone", 1 + 0.05 * q, 1 - 0.07 * q)
        # trên không: ngả ra sau lấy đà (giơ cột cao nhất) rồi chúi tới theo cú nện (không lộn vòng: người dùng thấy lạ)
        if T_NHUN < t < T_CAM + 0.1:
            u1 = math.sin(math.pi * min(1.0, (t - T_NHUN) / (T_DINH2 + 0.06 - T_NHUN)))
            u2 = ease((t - (T_DINH2 + 0.06)) / (T_CAM - T_DINH2 - 0.06), "in") if t > T_DINH2 + 0.06 else 0.0
            u3 = 1 - ease((t - T_CAM) / 0.1) if t > T_CAM else 1.0
            lat(P, (9.0 * u1 * (1 - u2) - 10.0 * u2) * u3)
        k = math.exp(-((t - T_CAM - 0.015) / 0.045) ** 2)
        P.scale("bone", 1 + 0.08 * k, 1 - 0.09 * k)
        phu_kien(t, P, 0.5)
        W = sk.the_gioi(P)
        p = (W["m_cot"] @ np.array([-half_cot, 0.0, 1.0]))[:2]                   # chân cột
        P.move("mieng", float(p[0]), float(max(0.0, p[1])))

    # ------------------------------------------------ skill: THẦN TRỤ GIÁNG THẾ
    def cot_bay(P, C, A, S):
        """cột bay: tâm C (thế giới), góc A (liền, không quấn), cỡ S."""
        P.alpha["cot"] = 0.0
        P.alpha["cot_bay"] = 1.0
        P.move("fly_cot", float(C[0] - x0c), 0.0)
        P.move("cot_bay", 0.0, float(C[1] - yb0))
        P.rot("cot_bay", float(A - ab0))
        P.scale("cot_bay", S, S)

    def than_skill(t, P):
        if t < T_GIANG:
            tau = tmap(t, [(0.0, 0.0), (T_NEM - 0.06, 0.40, "io"), (T_NEM, 0.50, "out"), (T_CHI, 1.05, "io"), (T_GIANG, 1.17, "lin")])
            dat(P, "skill_04", tau)
        elif t < T_LEN:
            dat(P, "skill_04", tmap(t, [(T_GIANG, 1.17), (T_SKILL, 1.30, "in"), (T_LEN, 1.40, "out")]))
            # vung tay chỉ xuống đối thủ: thân chúi tới
            u = ease((t - T_GIANG) / (T_SKILL - T_GIANG), "in")
            P.rot("bone2", -10.0 * u * (1 - ease((t - T_SKILL) / (T_LEN - T_SKILL))))
        else:
            Pa = khung.Pose()
            dat(Pa, "skill_04", 1.40 + (t - T_LEN) * 0.3)
            Pb = khung.Pose()
            dat(Pb, "idle_01", 0.0)
            chep(P, pha(Pa, Pb, ease((t - T_LEN) / (T_BAT - 0.05 - T_LEN), "io")))
        if T_TU < t < T_GIANG:
            r = hoat.rung(t, T_TU, T_GIANG, 2)
            g = ease((t - T_TU) / (T_GIANG - T_TU), "in")
            P.rot("bone3", 1.5 * r * (0.4 + g))
            P.move("bone", 0.0, -14.0 * g)
            s = 1 + 0.18 * g + 0.04 * r
            P.scale("m_loi", s, s)
            for i, m in enumerate(DA):                                        # đá bị hút bay lên quanh thân
                mv(P, f"m_{m}", 10.0 * _r(i, 3) * g, (40.0 + 30.0 * abs(_r(i, 4))) * g + 4.0 * r)
                P.rot(f"m_{m}", 25.0 * _r(i, 5) * g)
        if T_GIANG <= t < T_GIANG + 0.35:                                      # đá rơi về chỗ
            u = ease((t - T_GIANG) / 0.35, "in")
            for i, m in enumerate(DA):
                mv(P, f"m_{m}", 10.0 * _r(i, 3) * (1 - u), (40.0 + 30.0 * abs(_r(i, 4))) * (1 - u))
                P.rot(f"m_{m}", 25.0 * _r(i, 5) * (1 - u))
        if T_SKILL - 0.02 < t < T_SKILL + 0.25:
            k = math.exp(-((t - T_SKILL - 0.02) / 0.06) ** 2)
            P.scale("bone", 1 + 0.06 * k, 1 - 0.07 * k)
        tb = t - T_BAT
        if 0 < tb < 0.35:                                                       # bắt cột: khựng, thân lún
            k = math.exp(-tb / 0.08) * math.cos(tb * 2 * math.pi / 0.22)
            P.move("bone", 0.0, -18.0 * k)
            P.rot("bone20", 4.0 * k)

    def f_skill(t, P):
        than_skill(t, P)
        if t < T_NEM:
            return
        W = sk.the_gioi(P)
        Wn = W["m_cot"]                                    # cột thật ở dáng hiện tại (chỗ tay)
        C_nem, A_nem = Wn[:2, 2].copy(), khung.goc_mat(Wn)
        if t < T_GIANG:                                    # bay vọt lên trời, xoay
            # chỗ rời tay = cột thật ở giây T_NEM (tính lại dáng ở giây đó)
            Q = khung.Pose()
            than_skill(T_NEM, Q)
            Wq = sk.the_gioi(Q)["m_cot"]
            C0, A0 = Wq[:2, 2], khung.goc_mat(Wq)
            u = (t - T_NEM) / 0.42
            C = C0 + np.array([40.0 * min(u, 1), 2.6 * cao * ease(min(u, 1.0), "out") + 1.2 * cao * max(0.0, u - 1.0)])
            cot_bay(P, C, A0 + 540.0 * ease(min(u, 1.0), "out"), 1.0)
            if u > 1.05:                                   # đã ra khỏi khung: ẩn tới lúc giáng
                P.alpha["cot_bay"] = 0.0
            return
        Cg = np.array([far[0] - 0.18 * cao, far[1] - 0.45 * cao])       # mặt đất dưới đối thủ, hơi lệch về phía trước địch
        S = 1.85
        A_dung = 84.0 + 720.0                             # đứng (đầu vỡ lên trên), cùng vòng với góc lúc bay lên (A0 + 540 ≈ 720 + ...)
        if t < T_SKILL:                                   # giáng xuống chỗ đối thủ, khổng lồ
            u = ease((t - T_GIANG) / (T_SKILL - T_GIANG), "in")
            y_dat = Cg[1] + half_cot * S - 30.0           # chân cột chạm đất (lún 30)
            C = np.array([Cg[0], y_dat + 2.4 * cao * (1 - u)])
            cot_bay(P, C, A_dung, S)
            return
        if t < T_LEN:                                     # cắm: rung tắt dần
            tb = t - T_SKILL
            k = math.exp(-tb / 0.12) * math.sin(tb * 2 * math.pi / 0.16)
            C = np.array([Cg[0], Cg[1] + half_cot * S - 30.0 - 10.0 * k])
            cot_bay(P, C, A_dung + 2.5 * k, S)
            return
        if t < T_BAT:                                     # nhổ lên, thu nhỏ, bay vòng cung về tay, xoay một vòng
            u = (t - T_LEN) / (T_BAT - T_LEN)
            Pn = khung.Pose()
            than_skill(T_BAT, Pn)
            Wb = sk.the_gioi(Pn)["m_cot"]
            Cb, Ab = Wb[:2, 2], khung.goc_mat(Wb)
            Ab = Ab + 360.0 * round((A_dung + 360.0 - Ab) / 360.0)          # cùng vòng với A_dung + 1 vòng
            nho = ease(min(1.0, u / 0.3), "out")
            S_ = S + (1.0 - S) * nho
            Cst = np.array([Cg[0], Cg[1] + half_cot * S - 30.0 + 120.0 * nho])
            v = ease(max(0.0, (u - 0.2) / 0.8), "io")
            C = Cst + (Cb - Cst) * v + np.array([0.0, 0.55 * cao * math.sin(math.pi * v)])
            cot_bay(P, C, A_dung + (Ab - A_dung) * v, S_)
            return
        P.alpha["cot"] = 1.0
        P.alpha["cot_bay"] = 0.0

    # ------------------------------------------------ appear: PHẾ TÍCH THỨC TỈNH
    # dáng thân nền: block_01 khung 0 (cột dựng đứng trước mặt); cột rơi từ trời cắm xuống đúng chỗ đó; các mảnh nằm rải trên đất (phế tích)
    # hiện dần rồi lần lượt bay lên ráp vào chỗ; lõi bừng sáng; đầu rơi xuống cổ sau cùng; nhổ cột vác lên lưng (block_01 chạy tiếp).
    LEN = {}                               # mảnh → (giờ nhấc, thời gian bay)
    nhom = [("da_", 0.42, 0.05), ("hong", 0.52, 0.04), ("than", 0.58, 0), ("lung", 0.66, 0), ("tay_xa", 0.70, 0), ("vai_xa", 0.74, 0),
            ("nam_xa", 0.80, 0), ("pha_le", 0.84, 0.03), ("vai_gan", 0.86, 0), ("tay_gan", 0.94, 0), ("nam_gan", 1.00, 0)]
    for m in manh:
        for pre, t0, buoc in nhom:
            if m.startswith(pre):
                j = [x for x in manh if x.startswith(pre)].index(m)
                LEN[m] = (t0 + buoc * j, 0.36)
                break

    def nen_appear(P):
        dat(P, "block_01", 0.0)

    P_nen = khung.Pose()
    nen_appear(P_nen)
    W_nen = sk.the_gioi(P_nen)
    PHE = {}                              # chỗ nằm của mảnh trên đất: (tâm, góc thêm)
    for i, m in enumerate(manh):
        if m in ("cot", "dau", "loi"):
            continue
        Wm = W_nen[f"m_{m}"]
        da = 55.0 * _r(i, 7)
        cx = Wm[0, 2] + 160.0 * _r(i, 8) - 40.0
        cy = -thap(m, Wm, da) + 4.0
        PHE[m] = (np.array([cx, cy]), da)

    def f_appear(t, P):
        nen_appear(P)
        if t < T_NHO:
            P.move("bone", 0.0, 3.0 * math.sin(2 * math.pi * t / 1.4))
        W = sk.the_gioi(P)
        # cột: rơi thẳng đứng từ trời, cắm, rung
        Wc = W_nen["m_cot"]
        if t < T_CAMCOT:
            u = ease(t / T_CAMCOT, "in")
            Wd = Wc.copy()
            Wd[1, 2] += 2.2 * cao * (1 - u)
            dat_tg(P, W, "m_cot", Wd)
            P.alpha["cot"] = min(1.0, t / 0.08)
        elif t < T_CAMCOT + 0.45:
            tb = t - T_CAMCOT
            k = math.exp(-tb / 0.1) * math.sin(tb * 2 * math.pi / 0.15)
            dat_tg(P, W, "m_cot", Wc, them=3.0 * k)
        # mảnh: nằm trên đất (hiện dần) → bay lên ráp vào chỗ
        for m, (t0, dt) in LEN.items():
            xb = f"m_{m}"
            Wm = W[xb]
            c1 = Wm[:2, 2]
            c0, da = PHE[m]
            if t < t0:
                a = min(1.0, max(0.0, (t - 0.05) / 0.25))
                rung_ = 2.5 * math.sin(2 * math.pi * (t - t0) / 0.1) * max(0.0, 1 - (t0 - t) / 0.18)   # rung báo trước khi nhấc
                Wd = Wm.copy()
                Wd[0, 2], Wd[1, 2] = c0[0], c0[1]
                dat_tg(P, W, xb, Wd, them=da + rung_)
                P.alpha[m] = a
            elif t < t0 + dt:
                u = (t - t0) / dt
                v = ease(u, "back")
                c = c0 + (c1 - c0) * v + np.array([0.0, 0.32 * cao * math.sin(math.pi * min(1.0, u))])
                Wd = Wm.copy()
                Wd[0, 2], Wd[1, 2] = c[0], c[1]
                dat_tg(P, W, xb, Wd, them=da * (1 - ease(u, "out")))
        # lõi: tắt tới T_LOI rồi bừng
        if t < T_LOI:
            P.alpha["loi"] = 0.0
        elif t < T_LOI + 0.3:
            u = (t - T_LOI) / 0.3
            s = 0.25 + 0.95 * ease(min(1.0, u / 0.55), "out") - 0.2 * ease(max(0.0, (u - 0.55) / 0.45))
            P.scale("m_loi", s, s)
        # đầu: rơi từ trên xuống cổ
        if t < T_DAU:
            a = min(1.0, max(0.0, (t - (T_DAU - 0.35)) / 0.12))
            u = ease(max(0.0, (t - (T_DAU - 0.30)) / 0.30), "in")
            P.alpha["dau"] = a
            mv(P, "m_dau", 0.0, 520.0 * (1 - u))
            P.rot("m_dau", -12.0 * (1 - u))
        elif t < T_DAU + 0.35:
            tb = t - T_DAU
            k = math.exp(-tb / 0.08) * math.cos(tb * 2 * math.pi / 0.18)
            P.scale("m_dau", 1 + 0.06 * k, 1 - 0.06 * k)
            P.move("bone", 0.0, -10.0 * k)
        # nhổ cột vác lên lưng: block_01 chạy tiếp (chậm lại), rồi về idle 0
        if t >= T_NHO:
            Pa = khung.Pose()
            dat(Pa, "block_01", tmap(t, [(T_NHO, 0.0), (T_NHO + 0.18, 0.10, "io"), (T_NHO + 0.62, 0.50, "io")]))
            Pb = khung.Pose()
            dat(Pb, "idle_01", 0.0)
            w = ease((t - (T_NHO + 0.5)) / 0.3, "io")
            Q = pha(Pa, Pb, w)
            # gầm nhẹ cuối: ngửa đầu, lõi phồng
            g = math.sin(math.pi * min(1.0, max(0.0, (t - 2.15) / 0.55)))
            Q.rot("bone4", 7.0 * g)
            Q.rot("bone3", -2.0 * g)
            s = 1 + 0.12 * g
            Q.scale("m_loi", s, s)
            chep(P, Q)

    # ------------------------------------------------ die: SỤP ĐỔ (lõi chập chờn tắt, các mảnh rơi rã thành đống, cột đổ)
    P_d = khung.Pose()
    dat(P_d, "idle_01", 0.0)
    W_d = sk.the_gioi(P_d)
    ROI = {}
    for i, m in enumerate(manh):
        if m == "cot":
            continue
        Wm = W_d[f"m_{m}"]
        c0 = Wm[:2, 2]
        da = 70.0 * _r(i, 11)
        dx = 140.0 * _r(i, 12) - 30.0
        yf = -thap(m, Wm, da) + 3.0
        t0 = T_SUP + 0.05 * abs(_r(i, 13)) + (0.0 if m.startswith(("da_", "pha_le")) else 0.06) + (0.10 if m == "dau" else 0.0)
        ROI[m] = (t0, c0.copy(), np.array([c0[0] + dx, yf]), da)
    g_ = 5200.0

    def f_die(t, P):
        dat(P, "idle_01", 0.0)
        if t < T_SUP:                                                    # chập chờn
            r = hoat.rung(t, 0.0, T_SUP, 2)
            P.rot("bone3", 1.5 * r)
            fl = 0.5 + 0.5 * math.cos(2 * math.pi * t / 0.09)
            s = 1 + 0.15 * fl * (1 - t / T_SUP)
            P.scale("m_loi", s, s)
        if t >= T_TAT:
            P.alpha["loi"] = max(0.0, 1 - (t - T_TAT) / 0.12)
        W = sk.the_gioi(P)
        for m, (t0, c0, cf, da) in ROI.items():
            if t < t0:
                continue
            xb = f"m_{m}"
            Wm = W[xb]
            hh = max(1.0, c0[1] - cf[1])
            T = math.sqrt(2 * hh / g_)
            u = (t - t0) / T
            if u < 1:
                c = np.array([c0[0] + (cf[0] - c0[0]) * u, c0[1] - hh * u * u])
                a_ = da * u
            else:
                tb = t - t0 - T
                H = min(30.0, 0.08 * hh)
                c = np.array([cf[0], cf[1] + H * abs(math.sin(math.pi * tb / 0.16)) * math.exp(-tb / 0.12)])
                a_ = da + 4.0 * math.exp(-tb / 0.1) * math.sin(tb * 2 * math.pi / 0.2)
            Wd = Wm.copy()
            Wd[0, 2], Wd[1, 2] = c[0], c[1]
            dat_tg(P, W, xb, Wd, them=a_)
        # cột: đổ ra sau quanh chân cột, nằm ngang trên đống đá
        t0c = T_SUP + 0.06
        if t > t0c:
            Wc = W["m_cot"]
            a0 = khung.goc_mat(Wc)
            p0 = (Wc @ np.array([-half_cot, 0.0, 1.0]))[:2]               # chân cột (đầu dưới phải)
            af = 180.0 + 6.0
            u = min(1.0, (t - t0c) / (T_DO - t0c))
            a_ = a0 + (af - a0) * u * u
            if u >= 1:
                tb = t - T_DO
                a_ = af + 3.0 * math.exp(-tb / 0.1) * math.sin(tb * 2 * math.pi / 0.18)
            yp = p0[1] + (day_cot + 6.0 - p0[1]) * u * u
            c = np.array([p0[0], yp]) + half_cot * np.array([math.cos(math.radians(a_)), math.sin(math.radians(a_))])
            if u >= 1:
                c[1] += 14.0 * abs(math.sin(math.pi * (t - T_DO) / 0.15)) * math.exp(-(t - T_DO) / 0.1)
            Wd = Wc.copy()
            Wd[0, 2], Wd[1, 2] = c[0], c[1]
            dat_tg(P, W, "m_cot", Wd, them=a_ - a0)
        if t > D_DIE - TAN:
            a = max(0.0, 1 - (t - (D_DIE - TAN)) / (TAN - 0.05))
            for sl in sk.slots:
                P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], 1.0 if sl["alpha"] > 0 else 0.0)

    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_CAMCOT, "cam_cot", ""), (T_LOI, "loi_sang", ""), (T_DAU, "dat_dau", ""),
                                                (T_NHO, "nho_cot", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True, ev=[(G1, "dat_dau", "")]),
        Clip("walk", D_WALK, f_walk, loop=True),
        Clip("attack", M_ATTACK[-1][0], f_attack, ev=[(T_ATK, "trung", "")], trung=T_ATK),
        Clip("cast", D_CAST, f_cast, ev=[(T_CAM, "cam", ""), (T_RE, "trung", ""), (T_RUT, "rut", "")], trung=T_RE),
        Clip("skill", D_SKILL, f_skill, ev=[(T_NEM, "nem_cot", ""), (T_TU, "tu", ""), (T_GIANG, "giang", ""), (T_SKILL, "trung", ""),
                                            (T_RE2, "re", ""), (T_BAT, "bat_cot", "")], trung=T_SKILL),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", D_DIE, f_die, ev=[(T_TAT, "tat", ""), (T_SUP, "sup", ""), (T_DO, "do", "")]),
    ]
    return clips


# ---------------------------------------------------------------- lệnh
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
    sc = float(a[3]) if len(a) > 3 else 0.25
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
    """cho bản xem trước có đối thủ (tho5_fx.Tuong): rig với xương far đặt ở far_xy → (sk, info, clips, chiều cao)."""
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
    clips = lam_clip(sk, info, cao)
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
            Wl = [sk.the_gioi(P) for P in fr]
            for b in ("m_dau", "m_nam_gan", "m_cot", "m_tay_gan", "m_vai_gan", "m_loi", "cot_bay"):
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if d > 0.10 * cao and not (b == "cot_bay" and c.ten == "skill"):
                        xau.append(f"{i / 60:.2f}s {b} dời {d / cao:.2f} cao/khung60")
            print(f"{c.ten}: {len(fr)} khung60" + ("" if not xau else " | " + "; ".join(xau[:16]) + (" ..." if len(xau) > 16 else "")))
        return
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Tượng vua cổ cầm cột (tuong_cot_1): tướng 6 đảo Mộc", dang=1, so_dang=1,
                  dung_yen=("cast", "skill"), lao=("attack",), far=("cast", "skill"), ma_goc=None, khop_idle=0.2, cao=cao,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.4, tran_mb=0.7, span=3.4)


if __name__ == "__main__":
    main(sys.argv[1:])
