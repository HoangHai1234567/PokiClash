# -*- coding: utf-8 -*-
"""Hươu gỗ DẠNG 1 (khúc gỗ non): clip dựng ở TẦNG ĐIỀU KHIỂN của rig gốc monster_3304 rồi để runtime Spine thật nướng. Cùng bộ ý với
dạng 2 (huou_go_clip.py) ở mức nhỏ hơn; người dùng chưa dặn riêng clip dạng 1 (đề xuất của Claude, 2026-11-12). File này sinh từ khung
chung của huou_go_clip.py bằng scratchpad/tao_non_clip.py rồi sửa tay tiếp ở đây.

- idle / walk / hit / die: nguyên idle_01, run_01, hit_01, die_01 của họ.
- đánh thường: chạy lao tới, rạp người HÚC gạc (skill_01 của họ).
- chiêu mana: hơi cúi, tụ cầu nhỏ giữa hai cành gạc, bắn tia.
- chiêu cuối: ngả người ra sau, há mồm tụ cầu trước mồm, gật đầu nện tới.
- appear: cổng rừng mở, con vật chạy nước kiệu qua.

Rig gốc (con nhìn sang PHẢI): root > bone40 (dời cả con) > `bone` (mông; chân sau bone2-3, bone4-5: IK tuiR_H, tuiL_H; đuôi bone14 >
ba chuỗi lá) và bone6 (ngực; chân trước bone27 > bone7-8, bone28 > bone9-10: IK tuiR_Q, tuiL_Q thường tắt) > bone11 > bone12 > bone13
(khúc gỗ) > mồm bone24, ụ mắt bone25 > bone26, bone39, hai cành gạc bone29, bone30. Thứ tự IK trong mẫu: tuiL_H, tuiL_Q, tuiR_H, tuiR_Q.

Kênh riêng (ghi <scan>/kenh_rieng.json): ham 0..1 (mồm há), cau = (bán kính, x, y thế giới), bay (xương move), cong 0..1 (cổng mở).

    huou_go_non_clip.py dung | xem [clip,..|het] [n] [view|het] [t0] [t1] | song | mau       (xem, mau chạy qua quai/khoa.py chrome)"""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MON = "monster_3304"
FPS = 30.0


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


SCAN = os.path.join(sxs(), "scan", MON)
RIG = os.path.join(sxs(), "web", "assets", "Monster", MON)
LAM = os.path.join(SCAN, "lam_clip")
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
TEN = [b["name"] for b in I["bones"]]
PA = [b["parent"] for b in I["bones"]]
B0 = np.array([[b["x"], b["y"], b["rot"], b["sx"], b["sy"]] for b in I["bones"]], float)
IKS = [k["name"] for k in I["ik"]]                 # tuiL_H, tuiL_Q, tuiR_H, tuiR_Q
ix = TEN.index
_S = None

CHUOI_DAU = ["root", "bone40", "bone6", "bone11", "bone12", "bone13"]      # FK thuần tới khúc gỗ
# điểm thế giới ở dáng gốc: khúc gỗ x −68..96, y 23..259; mồm x −1..70, y 150..212; hai cành gạc mọc từ đỉnh khúc gỗ
TAM_SO = (35.0, 181.0)                             # tâm mồm
GIUA_SUNG = (12.0, 308.0)                          # giữa hai cành gạc, trên đỉnh khúc gỗ: chỗ tụ cầu của chiêu mana
HUONG_MOM = (0.94, 0.34)                           # hướng mồm (ra trước, hơi lên)
CAU_NHO, CAU_TO = 26.0, 82.0                       # bán kính cầu mana / cầu chiêu cuối (đơn vị rig)


def nhom(ds):
    m = np.zeros(len(TEN), bool)
    for n in ds:
        m[ix(n)] = True
    return m


def con_chau(goc):
    m = np.zeros(len(TEN), bool)
    m[ix(goc)] = True
    for i, p in enumerate(PA):                     # xương xếp cha trước con
        if p >= 0 and m[p]:
            m[i] = True
    return m


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y CHƯA áp ràng buộc; k (6) độ trộn IK; ex = kênh riêng."""

    def __init__(self, u, k, ex=None):
        self.u, self.k = u, k
        self.ex = ex or dict(ham=0.0, cau=(0.0, 0.0, 0.0), cong=0.0)

    def chep(self):
        return Dang(self.u.copy(), self.k.copy(), dict(self.ex))

    def tron(self, B, w, mat_na=None):
        ww = np.full(len(TEN), float(w)) if mat_na is None else np.where(mat_na, float(w), 0.0)
        return Dang(self.u + (B.u - self.u) * ww[:, None], self.k + (B.k - self.k) * (float(w) if mat_na is None else 0.0), dict(self.ex))

    def xoay(self, ten, do):
        self.u[ix(ten), 2] += do
        return self

    def doi(self, ten, dx, dy):
        self.u[ix(ten), 0] += dx
        self.u[ix(ten), 1] += dy
        return self


def nap():
    global _S
    if _S is None:
        S = json.load(open(os.path.join(SCAN, "sample_dk.json"), encoding="utf-8"))
        _S = {}
        for c, v in S.items():
            U = np.array([f["u"] for f in v["frames"]], float)
            U[:, :, 2] = np.degrees(np.unwrap(np.radians(U[:, :, 2]), axis=0))          # bỏ bước nhảy 360 giữa hai khung
            U[:, :, 2] += 360.0 * np.round((B0[None, :, 2] - U[:1, :, 2]) / 360.0)      # khung đầu gần dáng gốc
            _S[c] = (float(v["dur"]), U, np.array([[q[0] for q in f["k"]] for f in v["frames"]], float))
    return _S


def dk(clip, t, lap=False):
    dur, U, Kk = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    return Dang(U[i0] * (1 - w) + U[i1] * w, Kk[i0] * (1 - w) + Kk[i1] * w)


def nghi():
    return dk("idle_01", 0.0)


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return x ** k


def cung(t, t0, t1, t2, t3):
    if t <= t0 or t >= t3:
        return 0.0
    if t < t1:
        return em((t - t0) / (t1 - t0))
    if t <= t2:
        return 1.0
    return 1.0 - em((t - t2) / (t3 - t2))


def cong(moc, t, kieu=None):
    if t <= moc[0][0]:
        return moc[0][1]
    for i in range(len(moc) - 1):
        (a, x), (b, y) = moc[i], moc[i + 1]
        if t <= b:
            w = (t - a) / (b - a)
            if kieu and kieu[i]:
                w = kieu[i](w)
            return x + (y - x) * w
    return moc[-1][1]


def rung(t, t0, bien, tan=6.0, hz=5.0, pha=0.0):
    r = t - t0
    return bien * math.exp(-r * tan) * math.sin(2 * math.pi * hz * r + pha) if r > 0 else 0.0


def giat(t, bien, hz=19.0, pha=0.0):
    return bien * (math.sin(2 * math.pi * hz * t + pha) * 0.6 + math.sin(2 * math.pi * hz * 1.73 * t + 1.3 + pha) * 0.4)


def ma(x, y, rot, sx=1.0, sy=1.0):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return np.array([[c * sx, -s * sy, x], [s * sx, c * sy, y], [0, 0, 1.0]])


def dau_tg(u):
    """ma trận thế giới của xương đầu (bone7): FK thuần dọc chuỗi (chuỗi này không có ràng buộc)."""
    M = np.eye(3)
    for n in CHUOI_DAU:
        M = M @ ma(*u[ix(n)])
    return M


_M0 = np.linalg.inv(dau_tg(B0))
L_SO = _M0 @ np.array([TAM_SO[0], TAM_SO[1], 1.0])
L_SUNG = _M0 @ np.array([GIUA_SUNG[0], GIUA_SUNG[1], 1.0])
L_MOM = _M0[:2, :2] @ np.array(HUONG_MOM)


def cui(D, c):
    """cúi khúc gỗ về trước (c > 0) hoặc ngả ra sau (c < 0). Con nhìn +x nên cúi = quay thuận kim (âm)."""
    D.xoay("bone6", -5.0 * c)
    D.xoay("bone11", -14.0 * c)
    D.xoay("bone12", -7.0 * c)
    D.xoay("bone13", -7.0 * c)
    return D


def cau_sung(D, r):
    p = dau_tg(D.u) @ L_SUNG
    D.ex["cau"] = (r, float(p[0]), float(p[1]))


def cau_mom(D, r, xa=1.0):
    """cầu trước mồm: tâm cách tâm mồm (26 + bán kính) theo hướng mồm."""
    M = dau_tg(D.u)
    h = M[:2, :2] @ L_MOM
    h = h / np.hypot(*h)
    p = (M @ L_SO)[:2] + h * (26.0 * xa + r)
    D.ex["cau"] = (r, float(p[0]), float(p[1]))


# ---------------------------------------------------------------- idle, walk, hit, die: nguyên của họ
def idle(t):
    return dk("idle_01", t, True)


def walk(t):
    return dk("run_01", t, True)


def hit(t):
    return dk("hit_01", t)


def die(t):
    return dk("die_01", t)


# ---------------------------------------------------------------- attack: chạy lao tới, rạp người húc gạc
A_CHAY, A_TRUNG, A_GIU, A_DUR = 0.30, 0.46, 0.62, 1.15
A_XA = 300.0


def attack_bay(t):
    x = cong([(0.0, 0.0), (0.05, 0.0), (A_CHAY, 0.62 * A_XA), (A_TRUNG, A_XA), (A_GIU, A_XA), (1.0, 0.0)], t,
             [None, lambda w: vao(w, 1.5), None, None, em])
    y = 46.0 * math.sin(math.pi * (t - A_GIU) / (1.0 - A_GIU)) if A_GIU < t < 1.0 else 0.0
    return x - 9.0 * rung(t, A_TRUNG, 1.0, 9.0, 5.5), y


def attack(t):
    """ĐÒN THƯỜNG 1,15 s. Chạy lao tới 0,05 → 0,30 (run_01, người chúi dần); rạp người HÚC gạc 0,30 → 0,46 (skill_01 0 → 0,30 s),
    sự kiện trung 0,46; khựng tới 0,62; bật dậy, nhảy lùi về 1,00; hoà về nghỉ."""
    R = nghi()
    tau = cong([(A_CHAY - 0.05, 0.0), (A_TRUNG - 0.06, 0.19), (A_TRUNG, 0.30), (A_GIU, 0.37), (0.98, 0.8333)], t,
               [em, lambda w: vao(w, 1.5), None, em])
    D = dk("skill_01", tau)
    if t < A_CHAY + 0.05:
        Rn = dk("run_01", (t - 0.03) * 1.1, True)
        cui(Rn, 0.5 * em(t / 0.18))
        Rn = R.tron(Rn, em(t / 0.09))
        D = Rn.tron(D, em((t - (A_CHAY - 0.05)) / 0.10))
    D.xoay("bone13", rung(t, A_TRUNG, 6.0, 8.0, 6.0))
    D.doi("bone6", 0.0, -rung(t, A_TRUNG, 6.0, 8.0, 6.0, 1.2))
    return D.tron(R, em((t - 0.98) / 0.17)) if t > 0.98 else D


# ---------------------------------------------------------------- cast: hơi cúi, tụ cầu nhỏ giữa hai cành gạc, bắn tia
C_CUI, C_PHUN, C_HET, C_DUR = 0.32, 0.90, 1.84, 2.20
C_MUC = 0.60


def cast(t):
    """CHIÊU MANA 2,20 s, đứng tại chỗ. Cúi 0 → 0,32; tụ cầu nhỏ giữa hai cành gạc tới 0,90 (rung mạnh dần); BẮN tia 0,90 (phun):
    khúc gỗ giật ngược, thân giật lùi, ghìm tới 1,84 (tia của game chảy 0,88 s sau phun); cầu tắt, ngẩng lên, lắc đầu, về nghỉ."""
    D = dk("idle_01", t, True)
    c = cong([(0.0, 0.0), (C_CUI, 1.0), (C_PHUN - 0.06, 1.15), (C_PHUN + 0.05, 0.62), (C_PHUN + 0.22, 0.88), (C_HET, 0.88), (C_DUR - 0.05, 0.0)], t,
             [em, em, lambda w: ra(w, 2.2), em, None, em])
    tu = cung(t, C_CUI, C_PHUN - 0.05, C_PHUN - 0.05, C_PHUN)
    giu = cung(t, C_PHUN, C_PHUN + 0.05, C_HET - 0.1, C_HET + 0.05)
    cui(D, C_MUC * c + 0.05 * giat(t, 1.0, 17.0) * (0.3 + 0.7 * tu) * (tu > 0) + 0.03 * giat(t, 1.0, 23.0, 0.8) * giu)
    lui = -9.0 * em(t / C_CUI) * (1 - em((t - C_HET) / 0.3)) - 18.0 * cung(t, C_PHUN - 0.01, C_PHUN + 0.05, C_PHUN + 0.12, C_PHUN + 0.5)
    for b in ("bone", "bone6"):
        D.doi(b, lui, -5.0 * cung(t, 0.0, C_CUI, C_HET, C_DUR - 0.05) + giat(t, 1.0, 21.0, 2.0) * giu)
    D.xoay("bone13", rung(t, C_HET + 0.12, 6.0, 5.0, 4.0))
    r = CAU_NHO * (cong([(C_CUI - 0.04, 0.0), (C_PHUN - 0.06, 0.92), (C_PHUN, 1.25), (C_PHUN + 0.1, 1.0), (C_HET - 0.08, 0.9), (C_HET + 0.06, 0.0)], t,
                        [lambda w: ra(w, 1.6), None, None, None, em]) + 0.05 * giat(t, 1.0, 13.0) * (tu > 0 or giu > 0))
    cau_sung(D, max(0.0, r))
    return D


# ---------------------------------------------------------------- skill: ngả ra sau, há mồm tụ cầu, gật đầu nện tới
S_NGA, S_HA, S_DAY, S_NEN, S_TRUNG, S_GIU, S_DUR = 0.36, 0.52, 1.55, 1.70, 1.82, 2.22, 2.80


def skill(t):
    """CHIÊU CUỐI 2,80 s, đứng tại chỗ. Nhún rồi NGẢ người ra sau, hai chân trước nhấc khỏi đất 0 → 0,36; HÁ to mồm 0,36 → 0,52; tụ cầu
    trước mồm tới 1,55 (cầu lớn dần, cả người rung mạnh dần, ngả dần thêm); 1,55 → 1,70 ngả hẳn lấy đà; GẬT đầu NỆN tới 1,70 → 1,82
    (về dáng rạp húc của skill_01 0,28 s), cầu rời mồm (nem 1,76, trung 1,82); khựng, rung tới 2,22; ngậm mồm, đứng dậy, về nghỉ."""
    R = nghi()
    Bo = dk("skill_01", 0.28)
    if t < S_NEN:
        D = dk("idle_01", 0.0)
        D.doi("bone6", 0.0, -10.0 * cung(t, 0.0, 0.10, 0.12, 0.26))
    elif t < S_GIU:
        D = R.tron(Bo, cong([(S_NEN, 0.0), (S_TRUNG, 1.0)], t, [lambda w: vao(w, 2.2)]))
    else:
        D = dk("skill_01", cong([(S_GIU, 0.30), (S_DUR - 0.12, 0.8333)], t, [em]))
        D = D.tron(R, em((t - (S_DUR - 0.25)) / 0.25))
    tu = cung(t, S_HA, S_DAY, S_DAY, S_NEN)
    nga = cong([(0.10, 0.0), (S_NGA, 0.8), (S_DAY, 1.15), (S_NEN, 1.6), (S_NEN + 0.07, 0.0)], t, [em, None, em, lambda w: vao(w, 2.0)])
    cui(D, -nga * 0.52)
    D.xoay("bone6", 9.0 * nga)                                                       # ngực chồm lên: hai chân trước rời đất
    D.doi("bone6", -8.0 * nga, 10.0 * nga)
    D.doi("bone", -5.0 * nga, -4.0 * nga)
    lac = (0.25 + 0.75 * vao(tu, 1.5)) * (S_HA < t < S_NEN)
    D.xoay("bone13", giat(t, 1.6, 16.0) * lac)
    D.xoay("bone11", giat(t, 1.1, 14.0, 1.0) * lac)
    for b in ("bone", "bone6"):
        D.doi(b, giat(t, 1.4, 15.0, 2.0) * lac, giat(t, 1.2, 18.0, 0.5) * lac)
    D.xoay("bone13", rung(t, S_TRUNG, 8.0, 7.0, 6.0))
    D.doi("bone6", rung(t, S_TRUNG, 7.0, 8.0, 6.5), -rung(t, S_TRUNG, 7.0, 8.0, 6.5, 1.3))
    D.ex["ham"] = cong([(S_NGA - 0.02, 0.0), (S_HA, 1.0), (S_GIU - 0.1, 1.0), (S_GIU + 0.16, 0.0)], t, [lambda w: ra(w, 2.0), None, em])
    r = CAU_TO * cong([(S_HA - 0.02, 0.0), (S_DAY, 1.0), (S_NEN + 0.06, 1.08), (S_NEN + 0.10, 0.0)], t, [lambda w: ra(w, 1.5), None, None])
    cau_mom(D, max(0.0, r * (1.0 + 0.03 * giat(t, 1.0, 11.0) * lac)))
    return D


# ---------------------------------------------------------------- appear: cổng rừng mở, con vật chạy nước kiệu qua
P_MO, P_RA, P_TOI, P_DONG, P_DUR = 0.36, 0.40, 1.40, 1.86, 2.15
P_XA = 420.0
P_CONG = -215.0


def appear_bay(t):
    return -P_XA * (1.0 - cong([(P_RA, 0.0), (P_TOI, 1.0)], t, [lambda w: ra(w, 1.35)])), 0.0


def appear(t):
    """APPEAR 2,15 s. Cổng rừng mở 0 → 0,36 (cong_mo); con vật chạy nước kiệu ra khỏi mặt cổng 0,40 → 1,40 (run_01 chậm 0,7 lần, chậm
    dần; phần chưa qua cổng bị mặt nạ cắt giấu); tới chỗ: dừng, ngẩng lên lắc đầu; cổng khép 1,44 → 1,86 (cong_dong); hoà về nghỉ."""
    R = nghi()
    di = dk("run_01", (t - P_RA) * 0.7, True)
    w = 1.0 - em((t - (P_TOI - 0.2)) / 0.28)
    D = R.tron(di, w if t > P_RA - 0.05 else 0.0)
    ng = cung(t, P_TOI - 0.05, P_TOI + 0.18, P_TOI + 0.3, P_DUR - 0.08)
    cui(D, -0.5 * ng)
    D.xoay("bone13", rung(t, P_TOI + 0.2, 8.0, 4.0, 3.6))
    D.ex["cong"] = cong([(0.0, 0.0), (P_MO, 1.0), (P_TOI + 0.04, 1.0), (P_DONG, 0.0)], t, [lambda w: ra(w, 2.2), None, lambda w: vao(w, 1.8)])
    return D


CLIP = {"hn_idle": (2.0, idle), "hn_walk": (0.5333, walk), "hn_attack": (A_DUR, attack), "hn_cast": (C_DUR, cast),
        "hn_skill": (S_DUR, skill), "hn_appear": (P_DUR, appear), "hn_hit": (0.5, hit), "hn_die": (1.0, die)}
LAP = {"hn_idle", "hn_walk"}
BAY = {"hn_attack": attack_bay, "hn_appear": appear_bay}
SU_KIEN = {"hn_attack": [(A_TRUNG, "trung", "")],
           "hn_cast": [(C_CUI, "tu", ""), (C_PHUN, "phun", ""), (C_HET, "het_phun", "")],
           "hn_skill": [(S_HA, "tu", ""), (S_DAY, "day", ""), (S_NEN + 0.06, "nem", ""), (S_TRUNG, "trung", "")],
           "hn_appear": [(0.0, "cong_mo", ""), (P_RA, "buoc_ra", ""), (P_TOI + 0.04, "cong_dong", "")]}


def dung(xem=False):
    out = []
    rieng = {}
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        Ds = [fn(t) for t in ts]
        U = np.array([d.u for d in Ds])
        Kk = np.array([d.k for d in Ds])
        bay = [list(BAY[ten](t)) if ten in BAY else [0.0, 0.0] for t in ts]
        if xem and ten in BAY:                     # giả lập ngay trên rig gốc phần xương move của rig mình lo
            U[:, ix("bone40"), :2] += np.array(bay)
        bones = {}
        for i, nm in enumerate(TEN):
            d = U[:, i] - B0[i]
            o = {}
            if np.abs(d[:, 2]).max() > 1e-3:
                o["rotate"] = [[round(t, 4), round(float(v), 3)] for t, v in zip(ts, d[:, 2])]
            if np.abs(d[:, :2]).max() > 1e-3:
                o["translate"] = [[round(t, 4), round(float(x), 3), round(float(y), 3)] for t, (x, y) in zip(ts, d[:, :2])]
            sc = U[:, i, 3:] / np.where(np.abs(B0[i, 3:]) < 1e-6, 1.0, B0[i, 3:])
            if np.abs(sc - 1).max() > 1e-4:
                o["scale"] = [[round(t, 4), round(float(x), 4), round(float(y), 4)] for t, (x, y) in zip(ts, sc)]
            if o:
                bones[nm] = o
        iks = {kn: [[round(t, 4), round(float(v), 4), -1] for t, v in zip(ts, Kk[:, j])] for j, kn in enumerate(IKS)
               if np.abs(Kk[:, j] - 1).max() > 1e-4}
        out.append({"name": ten, "dur": dur, "bones": bones, "iks": iks, "slots": {}})
        rieng[ten] = {"dur": dur, "ham": [float(d.ex["ham"]) for d in Ds], "cau": [list(d.ex["cau"]) for d in Ds],
                      "cong": [float(d.ex["cong"]) for d in Ds], "bay": bay, "su_kien": SU_KIEN.get(ten, []), "lap": ten in LAP}
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, IK {list(iks)}")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "hn_extra.json"), "w", encoding="utf-8"))
    if not xem:
        json.dump(rieng, open(os.path.join(SCAN, "kenh_rieng.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "hn_extra.json"))
    return rieng


def _chay(*a):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "chay.py"), *a], capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace")[-900:])
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)


VIEW = "0,170,820,560"
VIEW_RIENG = {"hn_attack": "150,170,1050,580", "hn_skill": "40,200,900,640", "hn_appear": "-170,170,1050,560"}

TRANG = r"""<!doctype html><html><head><meta charset="utf-8"><title>huou_go dạng 1: clip trên rig gốc</title>
<style>body{background:#22252b;color:#ddd;font:14px sans-serif;margin:14px}button{background:#333842;color:#ddd;border:1px solid #555;
border-radius:6px;padding:6px 12px;margin:3px;font:14px sans-serif;cursor:pointer}button.on{background:#e8a33c;color:#111;border-color:#e8a33c}
#khung{position:relative;width:1100px;height:700px;margin-top:10px}canvas{position:absolute;left:0;top:0;border-radius:8px}#cv{background:#6b7079}
#st{color:#9ab}#mo{margin:6px 2px;max-width:1080px;line-height:1.45}</style></head><body>
<div><b>huou_go dạng 1</b>: clip dựng ở tầng điều khiển, chạy bằng runtime Spine thật trên RIG GỐC (hình của game tham khảo, chỉ xem nội bộ).
Quãng lao của đòn thường và quãng đi vào của appear là giả lập phần xương move lo. Vòng tròn = chỗ và cỡ quả cầu năng lượng (VFX làm
sau); "mồm" = độ há (rig gốc không có hàm, rig của mình mới há được); vòng bầu dục + mảng che = cánh cổng và phần bị mặt nạ giấu.
<span id="st">đang nạp</span></div>
<div id="nut"></div><div>tốc độ: <span id="td"></span> &nbsp; <label><input type="checkbox" id="lap" checked> phát lại liên tục</label></div>
<div id="mo"></div><div id="khung"><canvas id="cv" width="1100" height="700"></canvas><canvas id="ov" width="1100" height="700"></canvas></div>
<script src="__LIB__"></script>
<script>
const NAME="__MON__", SKEL="__SKEL__", ATLAS=__ATLAS__, PNG="__PNG__", EXTRA=__EXTRA__, INFO=__INFO__, KENH=__KENH__, XCONG=__XCONG__;
__ADDEXTRA__
function b64(s){const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u;}
const st=document.getElementById("st"), cv=document.getElementById("cv"), ov=document.getElementById("ov").getContext("2d");
let cur=null, t=0, speed=1, last=0, hold=0;
function kenh(c,ten,t){const k=KENH[c][ten];const x=Math.min(k.length-1,t*30),i=Math.floor(x),j=Math.min(k.length-1,i+1),w=x-i;
  return Array.isArray(k[i])?k[i].map((v,q)=>v*(1-w)+k[j][q]*w):k[i]*(1-w)+k[j]*w;}
async function main(){
  const ctx=new spine.ManagedWebGLRenderingContext(cv,{alpha:false});
  const am=new spine.AssetManager(ctx,"");
  am.setRawDataURI(NAME+".atlas","data:text/plain;base64,"+btoa(unescape(encodeURIComponent(ATLAS))));
  am.setRawDataURI(NAME+".png",PNG);
  am.loadTextureAtlas(NAME+".atlas");
  await new Promise(res=>{const w=()=>am.isLoadingComplete()?res():setTimeout(w,50);w();});
  if(am.hasErrors()){st.textContent="LOI "+JSON.stringify(am.getErrors());return;}
  const atlas=am.require(NAME+".atlas");
  const sd=new spine.SkeletonBinary(new spine.AtlasAttachmentLoader(atlas)).readSkeletonData(b64(SKEL));
  addExtra(sd,EXTRA);
  const renderer=new spine.SceneRenderer(cv,ctx);
  const sk=new spine.Skeleton(sd);
  const nut=document.getElementById("nut"), mo=document.getElementById("mo");
  function chon(c){cur=c;t=0;hold=0;[...nut.children].forEach(b=>b.classList.toggle("on",b.dataset.clip===c));
    const i=INFO[c];mo.textContent=c+" · "+i.dur.toFixed(2)+" s"+(i.lap?" · lặp":"")+(i.ev?" · sự kiện: "+i.ev:"")+" — "+i.mo;}
  for(const c of Object.keys(INFO)){const b=document.createElement("button");b.textContent=c.replace("hn_","");b.dataset.clip=c;b.onclick=()=>chon(c);nut.appendChild(b);}
  const td=document.getElementById("td");
  for(const v of [1,0.5,0.25]){const b=document.createElement("button");b.textContent=v+"×";b.onclick=()=>{speed=v;[...td.children].forEach(x=>x.classList.toggle("on",x===b));};td.appendChild(b);if(v===1)b.classList.add("on");}
  chon(Object.keys(INFO)[0]);
  st.textContent="sẵn sàng";
  function ve(now){
    const dt=Math.min(0.05,(now-last)/1000||0);last=now;
    const i=INFO[cur], a=sd.findAnimation(cur);
    if(i.lap){t=(t+dt*speed)%i.dur;}
    else if(t<i.dur){t=Math.min(i.dur,t+dt*speed);}
    else{hold+=dt;if(hold>0.8&&document.getElementById("lap").checked){t=0;hold=0;}}
    sk.setToSetupPose();
    a.apply(sk,t,t,false,[],1,spine.MixBlend.setup,spine.MixDirection.mixIn);
    sk.updateWorldTransform(spine.Physics.update);
    const [vx,vy,vw,vh]=i.view, z=Math.max(vw/cv.width,vh/cv.height);
    ctx.gl.clearColor(0.42,0.44,0.48,1);ctx.gl.clear(ctx.gl.COLOR_BUFFER_BIT);
    renderer.camera.position.x=vx;renderer.camera.position.y=vy;renderer.camera.zoom=z;
    ctx.gl.viewport(0,0,cv.width,cv.height);renderer.camera.setViewport(cv.width,cv.height);renderer.camera.update();
    renderer.begin();renderer.drawSkeleton(sk,false);renderer.end();
    ov.clearRect(0,0,1100,700);
    const X=x=>550+(x-vx)/z, Y=y=>350-(y-vy)/z;
    const ham=kenh(cur,"ham",t), cau=kenh(cur,"cau",t), bay=kenh(cur,"bay",t), cg=kenh(cur,"cong",t);
    ov.strokeStyle="rgba(40,30,20,.35)";ov.lineWidth=1;ov.beginPath();ov.moveTo(0,Y(0));ov.lineTo(1100,Y(0));ov.stroke();
    if(cur==="hn_appear"){ov.fillStyle="rgb(107,112,121)";ov.fillRect(0,0,X(XCONG),Y(0));
      if(cg>0.01){ov.strokeStyle="rgba(120,220,120,.95)";ov.fillStyle="rgba(60,150,90,.35)";ov.lineWidth=7;ov.beginPath();
        ov.ellipse(X(XCONG),Y(180),80*cg/z,200*cg/z,0,0,6.2832);ov.fill();ov.stroke();}}
    if(cau[0]>0.5){const x=X(cau[1]+bay[0]), y=Y(cau[2]+bay[1]), r=cau[0]/z;
      ov.fillStyle="rgba(110,230,150,.55)";ov.strokeStyle="rgba(30,110,60,.9)";ov.lineWidth=3;ov.beginPath();ov.arc(x,y,r,0,6.2832);ov.fill();ov.stroke();}
    ov.fillStyle=ham>0.05?"#fd8":"#bcd";ov.font="15px sans-serif";ov.fillText("mồm há "+Math.round(ham*100)+"%   t = "+t.toFixed(2)+" s",14,24);
    requestAnimationFrame(ve);
  }
  requestAnimationFrame(ve);
}
main().catch(e=>{st.textContent="LOI "+e+" "+(e.stack||"");});
</script></body></html>"""

MO_TA = {"hn_idle": "nguyên idle_01 của họ", "hn_walk": "nguyên run_01 của họ (nước kiệu); game lo dời ngang",
         "hn_attack": "chạy lao tới, rạp người HÚC gạc vào đối thủ; khựng; bật dậy, nhảy lùi về",
         "hn_cast": "hơi cúi, tụ cầu nhỏ giữa hai cành gạc (rung mạnh dần); BẮN tia: khúc gỗ giật ngược, ghìm giữ tia; ngẩng lên, lắc đầu",
         "hn_skill": "nhún, NGẢ người ra sau (chân trước rời đất), HÁ mồm tụ cầu trước mồm (rung mạnh dần); ngả hẳn lấy đà; GẬT đầu NỆN tới; khựng; ngậm mồm, về nghỉ",
         "hn_appear": "cổng rừng mở phía sau, con vật chạy nước kiệu ra khỏi cổng (phần chưa qua cổng bị giấu), tới chỗ thì ngẩng lên lắc đầu; cổng khép",
         "hn_hit": "nguyên hit_01 của họ", "hn_die": "nguyên die_01 của họ: bị hất tung lên rồi rơi nằm bẹp"}


def song():
    """trang xem SỐNG (runtime Spine thật, 60 khung/giây, mở bằng file://) trên rig gốc → <scan>/lam_clip/xem/xem.html."""
    import base64
    dung(xem=True)
    extra = open(os.path.join(LAM, "hn_extra.json"), encoding="utf-8").read()
    rieng = dung()
    mo_xe = open(os.path.join(HERE, "mo_xe", "mo_xe.html"), encoding="utf-8").read()
    a = mo_xe.index("function addExtra(data, list) {")
    b = mo_xe.index("// lấy mẫu 30 khung/giây")
    b64 = lambda f: base64.b64encode(open(os.path.join(RIG, f), "rb").read()).decode()
    info = {c: {"dur": CLIP[c][0], "lap": c in LAP, "view": [float(x) for x in VIEW_RIENG.get(c, VIEW).split(",")], "mo": MO_TA.get(c, ""),
                "ev": ", ".join(f"{e}{' ' + s if s else ''} {x:.2f} s" for x, e, s in SU_KIEN.get(c, []))} for c in CLIP}
    kenh = {c: {k: rieng[c][k] for k in ("ham", "cau", "bay", "cong")} for c in CLIP}
    lib = "file:///" + os.path.join(HERE, "lib", "spine-player.js").replace(os.sep, "/")
    h = (TRANG.replace("__LIB__", lib).replace("__MON__", MON).replace("__SKEL__", b64(MON + ".skel"))
         .replace("__ATLAS__", json.dumps(open(os.path.join(RIG, MON + ".atlas"), encoding="utf-8").read()))
         .replace("__PNG__", "data:image/png;base64," + b64(MON + ".png")).replace("__EXTRA__", extra).replace("__XCONG__", str(P_CONG))
         .replace("__INFO__", json.dumps(info, ensure_ascii=False)).replace("__KENH__", json.dumps(kenh)).replace("__ADDEXTRA__", mo_xe[a:b]))
    ra_ = os.path.join(LAM, "xem")
    os.makedirs(ra_, exist_ok=True)
    open(os.path.join(ra_, "xem.html"), "w", encoding="utf-8").write(h)
    print(os.path.join(ra_, "xem.html"))


def main(a):
    sys.stdout.reconfigure(encoding="utf-8")
    lenh = a[0] if a else "dung"
    if lenh == "dung":
        dung()
    elif lenh == "xem":
        dung(xem=True)
        cl = a[1] if len(a) > 1 and a[1] not in ("", "het") else ",".join(CLIP)       # PowerShell bỏ đối số rỗng: dùng "het"
        n = a[2] if len(a) > 2 else "16"
        tt = (f"&t0={a[4]}" if len(a) > 4 else "") + (f"&t1={a[5]}" if len(a) > 5 else "")
        for c in cl.split(","):
            view = a[3] if len(a) > 3 and a[3] not in ("", "het") else VIEW_RIENG.get(c, VIEW)
            vw, vh = [float(x) for x in view.split(",")[2:]]
            _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={c}&extra=hn_extra.json&n={n}&tw=380&th={int(round(380 * vh / vw))}&cols=8&view={view}{tt}")
        dung()
    elif lenh == "song":
        song()
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "hn_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
