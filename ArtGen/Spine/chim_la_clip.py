# -*- coding: utf-8 -*-
"""Chim bảo hộ rừng cánh lá (chim_la): clip dựng ở TẦNG ĐIỀU KHIỂN của rig gốc monster_3630 rồi để runtime Spine thật nướng.
Khung chung lấy từ huou_go_non_clip.py. Rig gốc là FK thuần (hai IK L1, L2 mặc định tắt), nhưng clip của họ ĐỔI HÌNH theo khung:
cánh gần đổi bộ chibangR1 ↔ chibangR3 (mặt kia của cánh), hai chân đổi bộ slot khi co chân lúc bay, mắt nhắm lúc trúng đòn; die còn
đổi thứ tự vẽ. Vì vậy mỗi dáng mang theo cả tên hình từng slot (n) và thứ tự vẽ (o) của khung nguồn.

Người dùng dặn 2026-11-12:
- appear: chim bay vào.
- tấn công thường: lao tới đâm mỏ vào đối thủ (tận dụng run của nó, tăng tốc lên).
- run: giống họ.
- chiêu mana: na ná skill_03: chim đứng dọc, dùng cánh quạt mạnh MỘT phát, các lá lông trên cánh bay ra găm vào người đối thủ rồi
  quay về cánh.
- chiêu cuối: giống skill_04, gọi một thiên thạch đá rơi từ trên trời xuống đầu đối thủ.
idle / hit / die: nguyên của họ.

Kênh riêng (ghi <scan>/kenh_rieng.json): bay = (x, y) xương move; mo = độ đậm cả con (appear hiện dần); la = (quãng 0..1 từ cánh tới
đối thủ, độ đậm) của các lá bay; da = (quãng rơi 0..1, độ đậm) của thiên thạch (VFX; rig chỉ đặt sự kiện).

    chim_la_clip.py dung | xem [clip,..|het] [n] [view|het] [t0] [t1] | song | mau       (xem, mau chạy qua quai/khoa.py chrome)"""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MON = "monster_3630"
FPS = 30.0
TT = "ca_"


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
IKS = [k["name"] for k in I["ik"]]
SLOT = [s["name"] for s in I["slots"]]
N0 = [s["att"] for s in I["slots"]]
O0 = list(range(len(SLOT)))
ix = TEN.index
_S = None
GOC = "bone"                                       # xương dời cả con (cha của hông bone3; bóng và đích IK không theo)
XA_DICH = 1050.0                                   # chỗ đối thủ đứng trên trang xem thử (đơn vị rig, bên phải)
CAO_DICH = 560.0


def con_chau(goc):
    m = np.zeros(len(TEN), bool)
    m[ix(goc)] = True
    for i, p in enumerate(PA):
        if p >= 0 and m[p]:
            m[i] = True
    return m


CANH = con_chau("bone123") | con_chau("bone178")   # hai cánh (gần: bone123, xa: bone178)
DAU = con_chau("bone6")                            # cổ trên + đầu + mào + mỏ


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y; k độ trộn IK; n tên hình từng slot; o thứ tự vẽ."""

    def __init__(self, u, k, n, o, ex=None):
        self.u, self.k, self.n, self.o = u, k, n, o
        self.ex = ex or dict(mo=1.0, la=(0.0, 0.0), da=(0.0, 0.0))

    def chep(self):
        return Dang(self.u.copy(), self.k.copy(), self.n, self.o, dict(self.ex))

    def tron(self, B, w, mat_na=None):
        w = min(1.0, max(0.0, float(w)))
        ww = np.full(len(TEN), w) if mat_na is None else np.where(mat_na, w, 0.0)
        lay_b = w > 0.5 and mat_na is None
        return Dang(self.u + (B.u - self.u) * ww[:, None], self.k + (B.k - self.k) * (w if mat_na is None else 0.0),
                    B.n if lay_b else self.n, B.o if lay_b else self.o, dict(self.ex))

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
            U[:, :, 2] = np.degrees(np.unwrap(np.radians(U[:, :, 2]), axis=0))
            U[:, :, 2] += 360.0 * np.round((B0[None, :, 2] - U[:1, :, 2]) / 360.0)
            _S[c] = (float(v["dur"]), U, np.array([[q[0] for q in f["k"]] for f in v["frames"]], float),
                     [f["n"] for f in v["frames"]], [f["o"] for f in v["frames"]])
    return _S


def dk(clip, t, lap=False):
    dur, U, Kk, Nn, Oo = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    j = i0 if w < 0.5 else i1
    return Dang(U[i0] * (1 - w) + U[i1] * w, Kk[i0] * (1 - w) + Kk[i1] * w, Nn[j], Oo[j])


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


# ---------------------------------------------------------------- idle, walk, hit, die: nguyên của họ
def idle(t):
    return dk("idle_01", t, True)


def walk(t):
    return dk("run_01", t, True)


def hit(t):
    D = dk("hit_01", t)
    return D.tron(nghi(), em((t - 0.40) / 0.10)) if t > 0.40 else D


def die(t):
    return dk("die_01", t)


# ---------------------------------------------------------------- attack: bay lao tới, đâm mỏ
A_DA, A_LAO, A_TRUNG, A_GIU, A_VE, A_DUR = 0.16, 0.42, 0.50, 0.66, 1.12, 1.30
A_XA = 560.0
A_NGUON = 0.63                                     # dáng đâm mỏ: skill_01 của họ ở giây này (thân ngang, đầu chúi tới, mỏ đi trước)


def attack_bay(t):
    x = cong([(0.0, 0.0), (A_DA, -46.0), (A_LAO, 0.80 * A_XA), (A_TRUNG, A_XA), (A_GIU, A_XA - 14.0), (A_VE, 0.0)], t,
             [em, lambda w: vao(w, 1.7), lambda w: ra(w, 1.4), None, em])
    y = cong([(0.0, 0.0), (A_DA, 26.0), (A_LAO, 40.0), (A_TRUNG, 0.0), (A_GIU, 0.0), ((A_GIU + A_VE) / 2, 70.0), (A_VE, 0.0)], t,
             [em, None, lambda w: vao(w, 1.5), None, lambda w: ra(w, 1.6), lambda w: vao(w, 1.6)])
    return x - 12.0 * rung(t, A_TRUNG, 1.0, 9.0, 5.5), y


def attack(t):
    """ĐÒN THƯỜNG 1,30 s. Lấy đà 0 → 0,16 (ngả lùi, cánh giơ lên: dáng đầu run_01); BAY LAO tới 0,16 → 0,42 (run_01 phát nhanh 1,9
    lần: một nhịp vỗ rưỡi, tăng tốc); ĐÂM MỎ 0,42 → 0,50 (về dáng lao của skill_01 0,63 s, cổ vươn thêm), trung 0,50; khựng, rung tới
    0,66; bật lùi bay về 0,66 → 1,12 (đoạn hồi của skill_01); hoà về nghỉ."""
    R = nghi()
    Mo = dk("skill_01", A_NGUON)
    if t < A_LAO:
        Rn = dk("run_01", max(0.0, t - A_DA) * 1.9, True)
        D = R.tron(Rn, em(t / (A_DA * 0.9)))
        D.doi(GOC, 0.0, 0.0)
        D = D.tron(Mo, vao((t - (A_LAO - 0.10)) / 0.18, 1.6))
    elif t < A_GIU:
        Rn = dk("run_01", (A_LAO - A_DA) * 1.9, True)
        D = Rn.tron(Mo, 0.55 + 0.45 * ra((t - A_LAO) / (A_TRUNG - A_LAO), 2.0))
        D.n, D.o = Mo.n, Mo.o
    else:
        D = dk("skill_01", cong([(A_GIU, A_NGUON), (A_VE, 1.20), (A_DUR, 1.3333)], t, [em, None]))
        D = D.tron(R, em((t - (A_DUR - 0.2)) / 0.2))
    # cú mổ: cổ, đầu vươn tới rồi giật lại
    mo_ = cung(t, A_LAO - 0.02, A_TRUNG, A_TRUNG + 0.03, A_GIU + 0.1)
    D.xoay("bone6", -7.0 * mo_).xoay("bone7", -6.0 * mo_).xoay("bone8", -5.0 * mo_)
    D.doi("bone6", 10.0 * mo_, 0.0)
    D.xoay("bone8", rung(t, A_TRUNG, 7.0, 9.0, 7.0))
    D.xoay("bone5", rung(t, A_TRUNG, 3.0, 8.0, 6.0, 1.0))
    return D


# ---------------------------------------------------------------- cast: đứng dọc, quạt cánh mạnh một phát, lá bay ra găm rồi quay về
C_LEN, C_GIU, C_QUAT, C_NEM, C_TRUNG, C_VE, C_TOI, C_DUR = 0.26, 0.58, 0.72, 0.70, 0.95, 1.30, 1.64, 2.20   # nem 0,70: bộ cánh R1 vừa bật lại (khung 21)


def cast(t):
    """CHIÊU MANA 2,20 s, đứng tại chỗ. Người dùng 2026-11-12 (sau bản đầu dùng nhịp quạt thứ nhất của skill_03): "skill_03 sau 2 lần
    đập cánh đầu thì sang lần đập cánh thứ 3 chính là kiểu đập cánh tôi muốn" → CHỈ lấy nhịp thứ ba của họ (1,16 → 2,17 s): dựng
    người xoè cánh 0 → 0,26 (hoà từ nghỉ sang dáng 1,16 s); giơ hai cánh ra sau lưng lấy đà, giữ đỉnh 0,26 → 0,58 (1,16 → 1,39 s);
    VẶN NGƯỜI QUÉT cánh ra trước 0,58 → 0,72 (1,39 → 1,56 s), lá rời cánh giữa cú quét (nem 0,65); lá găm vào đối thủ (trung 0,92);
    giữ hai cánh khép chéo phía trước tới 1,30 (ve: lá rút ra bay về); mở cánh đón 1,30 → 1,64 (toi: lá về tới, cánh giật nhẹ); về."""
    R = nghi()
    tau = cong([(0.0, 1.08), (C_LEN, 1.16), (C_GIU - 0.12, 1.36), (C_GIU, 1.39), (C_QUAT, 1.56), (C_VE, 1.74), (C_TOI, 2.00), (C_DUR - 0.1, 2.1667)], t,
               [None, em, None, lambda w: vao(w, 1.3), lambda w: ra(w, 1.5), em, None])
    D = dk("skill_03", tau)
    if t < C_LEN:
        D = R.tron(D, em(t / (C_LEN - 0.04)))
    # rướn thêm lúc giữ đỉnh, chúi theo cú quét
    ruon = cung(t, C_LEN, C_GIU - 0.10, C_GIU, C_QUAT - 0.04)
    D.doi(GOC, -12.0 * ruon, 18.0 * ruon)
    chui = cung(t, C_GIU + 0.02, C_QUAT, C_VE - 0.1, C_TOI)
    D.doi(GOC, 22.0 * chui, -14.0 * chui)
    D.xoay("bone5", rung(t, C_QUAT, 4.0, 7.0, 6.0))
    D.doi(GOC, -rung(t, C_QUAT, 14.0, 7.0, 5.0), 0.0)
    giu = cung(t, C_QUAT, C_QUAT + 0.05, C_VE - 0.05, C_VE + 0.05)
    D.xoay("bone5", giat(t, 0.5, 15.0) * giu)
    D.xoay("bone5", rung(t, C_TOI, 3.0, 8.0, 6.0, 2.0))       # lá về tới: cánh, ngực giật nhẹ
    D.doi(GOC, -rung(t, C_TOI, 9.0, 8.0, 5.5), 0.0)
    if t > C_DUR - 0.2:
        D = D.tron(R, em((t - (C_DUR - 0.2)) / 0.2))
    q = cong([(C_NEM, 0.0), (C_TRUNG, 1.0), (C_VE, 1.0), (C_TOI, 0.0)], t, [lambda w: ra(w, 1.3), None, lambda w: vao(w, 1.7)])
    D.ex["la"] = (q, 1.0 if C_NEM <= t <= C_TOI else 0.0)
    return D


# ---------------------------------------------------------------- skill: thu cánh tụ lực, bung cánh ngửa mặt gọi thiên thạch
S_THU, S_TU, S_BUNG, S_ROI, S_GIU, S_TRUNG, S_DUR = 0.26, 0.90, 1.08, 1.34, 1.80, 1.94, 2.60


def skill(t):
    """CHIÊU CUỐI 2,60 s, đứng tại chỗ (skill_04 của họ). Thu hai cánh ôm lấy thân 0 → 0,26; tụ lực tới 0,90 (rung mạnh dần, co người);
    BUNG cánh, vươn thẳng, ngửa mặt lên trời 0,90 → 1,08 (goi); giữ dáng gọi, cánh rung tới 1,80 (roi 1,34: thiên thạch hiện trên cao,
    rơi 0,6 s); ĐẬP hai cánh xuống đúng lúc thiên thạch nện (1,80 → 1,94, trung 1,94); khựng, rung; hoà về nghỉ."""
    R = nghi()
    tau = cong([(0.0, 0.0), (S_THU, 0.26), (S_TU, 0.66), (S_BUNG, 0.93), (S_GIU, 1.52), (S_TRUNG, 1.80), (S_DUR - 0.2, 2.0)], t,
               [em, None, lambda w: ra(w, 1.8), None, lambda w: vao(w, 1.6), em])
    D = dk("skill_04", tau)
    tu = cung(t, S_THU - 0.04, S_TU - 0.05, S_TU - 0.02, S_BUNG - 0.08)
    lac = vao(tu, 1.4)
    D.doi(GOC, giat(t, 5.0, 16.0) * lac, -16.0 * tu + giat(t, 4.0, 19.0, 1.0) * lac)
    D.xoay("bone5", giat(t, 1.2, 17.0, 0.5) * lac)
    goi = cung(t, S_BUNG - 0.02, S_BUNG + 0.08, S_GIU - 0.04, S_GIU + 0.06)
    D.doi(GOC, 0.0, 26.0 * goi)
    D.xoay("bone8", giat(t, 1.0, 11.0) * goi)                 # đầu rung như đang hét
    D.xoay("bone5", giat(t, 0.5, 13.0, 0.7) * goi)
    D.doi(GOC, rung(t, S_TRUNG, 12.0, 7.0, 6.0), -rung(t, S_TRUNG, 18.0, 7.0, 6.0, 1.2))
    D.xoay("bone5", rung(t, S_TRUNG, 4.0, 7.0, 6.0))
    if t > S_DUR - 0.25:
        D = D.tron(R, em((t - (S_DUR - 0.25)) / 0.25))
    q = cong([(S_ROI, 0.0), (S_TRUNG, 1.0)], t, [lambda w: vao(w, 1.8)])
    D.ex["da"] = (q, 1.0 if S_ROI <= t <= S_TRUNG + 0.03 else 0.0)
    return D


# ---------------------------------------------------------------- appear: bay từ ngoài vào, xoè cánh hãm, đậu vào dáng nghỉ
P_TOI, P_HAM, P_DUR = 0.95, 1.22, 1.75
P_XA, P_CAO = 760.0, 380.0


def appear_bay(t):
    w = 1.0 - cong([(0.0, 0.0), (P_TOI + 0.12, 1.0)], t, [lambda w_: ra(w_, 2.0)])
    return -P_XA * w, P_CAO * w ** 1.25 + 34.0 * cung(t, P_TOI - 0.1, P_HAM - 0.04, P_HAM, P_DUR - 0.1)


def appear(t):
    """APPEAR 1,75 s. Bay vào từ phía sau, trên cao (run_01 vỗ cánh, chậm dần) 0 → 0,95, hiện dần 0,2 s đầu; tới nơi DỰNG người, xoè
    hai cánh lên cao để hãm (dáng skill_03 0,30 s) 0,95 → 1,22, khựng nhẹ trên không; hạ cánh, hoà về nghỉ."""
    R = nghi()
    Ham = dk("skill_03", 0.30)
    Bay = dk("run_01", t * 1.05, True)
    D = Bay.tron(Ham, em((t - (P_TOI - 0.20)) / 0.30))
    if t > P_HAM:
        D = Ham.tron(R, em((t - P_HAM) / (P_DUR - P_HAM - 0.05)))
    D.xoay("bone5", rung(t, P_HAM, 3.0, 6.0, 4.0))
    D.ex["mo"] = em(t / 0.2)
    return D


CLIP = {TT + "idle": (1.3333, idle), TT + "walk": (0.8, walk), TT + "attack": (A_DUR, attack), TT + "cast": (C_DUR, cast),
        TT + "skill": (S_DUR, skill), TT + "appear": (P_DUR, appear), TT + "hit": (0.5, hit), TT + "die": (1.0, die)}
LAP = {TT + "idle", TT + "walk"}
BAY = {TT + "attack": attack_bay, TT + "appear": appear_bay}
SU_KIEN = {TT + "attack": [(A_TRUNG, "trung", "")],
           TT + "cast": [(C_LEN, "tu", ""), (C_NEM, "nem", ""), (C_TRUNG, "trung", ""), (C_VE, "ve", ""), (C_TOI, "toi", "")],
           TT + "skill": [(S_THU, "tu", ""), (S_BUNG, "goi", ""), (S_ROI, "roi", ""), (S_TRUNG, "trung", "")],
           TT + "appear": [(P_TOI, "toi", "")]}


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
            U[:, ix(GOC), :2] += np.array(bay)
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
        slots = {}
        for si, sn in enumerate(SLOT):
            names = [d.n[si] for d in Ds]
            o = {}
            if any(x != N0[si] for x in names):
                o["attachment"] = [[round(ts[j], 4), names[j]] for j in range(n) if j == 0 or names[j] != names[j - 1]]
            if xem and any(d.ex["mo"] < 0.999 for d in Ds):
                o["alpha"] = [[round(t, 4), round(float(d.ex["mo"]), 3)] for t, d in zip(ts, Ds)]
            if o:
                slots[sn] = o
        A = {"name": ten, "dur": dur, "bones": bones, "iks": {}, "slots": slots}
        if any(d.o != O0 for d in Ds):
            A["draworder"] = [[round(ts[j], 4), None if Ds[j].o == O0 else [SLOT[q] for q in Ds[j].o]] for j in range(n)
                              if j == 0 or Ds[j].o != Ds[j - 1].o]
        iks = {kn: [[round(t, 4), round(float(v), 4), 1] for t, v in zip(ts, Kk[:, j])] for j, kn in enumerate(IKS) if np.abs(Kk[:, j]).max() > 1e-4}
        A["iks"] = iks
        out.append(A)
        rieng[ten] = {"dur": dur, "bay": bay, "mo": [float(d.ex["mo"]) for d in Ds], "la": [list(d.ex["la"]) for d in Ds],
                      "da": [list(d.ex["da"]) for d in Ds], "su_kien": SU_KIEN.get(ten, []), "lap": ten in LAP}
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, {len(slots)} slot đổi hình, IK {list(iks)}"
              f"{', đổi thứ tự vẽ' if 'draworder' in A else ''}")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "ca_extra.json"), "w", encoding="utf-8"))
    if not xem:
        json.dump(rieng, open(os.path.join(SCAN, "kenh_rieng.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "ca_extra.json"))
    return rieng


def _chay(*a):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "chay.py"), *a], capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace")[-900:])
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)


VIEW = "0,520,2000,1400"
VIEW_RIENG = {TT + "attack": "300,520,2600,1400", TT + "appear": "-300,640,2600,1640", TT + "cast": "0,560,2100,1500",
              TT + "skill": "0,600,2100,1560"}
VIEW_SONG = "330,640,2900,1800"                    # trang sống: một khung nhìn chung, thấy cả chỗ đối thủ

# lá bay của chiêu mana trên trang xem thử: mút vài xương lông cánh (lông dài ngoài cùng của hai cánh)
LA_XUONG = ["bone130", "bone131", "bone137", "bone138", "bone143", "bone189", "bone213", "bone188", "bone191", "bone194"]

TRANG = r"""<!doctype html><html><head><meta charset="utf-8"><title>chim_la: clip trên rig gốc</title>
<style>body{background:#22252b;color:#ddd;font:14px sans-serif;margin:14px}button{background:#333842;color:#ddd;border:1px solid #555;
border-radius:6px;padding:6px 12px;margin:3px;font:14px sans-serif;cursor:pointer}button.on{background:#e8a33c;color:#111;border-color:#e8a33c}
#khung{position:relative;width:1160px;height:720px;margin-top:10px}canvas{position:absolute;left:0;top:0;border-radius:8px}#cv{background:#6b7079}
#st{color:#9ab}#mo{margin:6px 2px;max-width:1140px;line-height:1.45}</style></head><body>
<div><b>chim_la</b>: clip dựng ở tầng điều khiển, chạy bằng runtime Spine thật trên RIG GỐC (hình của game tham khảo, chỉ xem nội bộ).
Quãng lao của đòn thường và quãng bay vào của appear là giả lập phần xương move lo. Hình người que bên phải = chỗ đối thủ; các lá lục =
lá cánh bay ra găm rồi quay về (rig của mình sẽ là lá thật của cánh); khối xám = thiên thạch đá (VFX làm sau). <span id="st">đang nạp</span></div>
<div id="nut"></div><div>tốc độ: <span id="td"></span> &nbsp; <label><input type="checkbox" id="lap" checked> phát lại liên tục</label></div>
<div id="mo"></div><div id="khung"><canvas id="cv" width="1160" height="720"></canvas><canvas id="ov" width="1160" height="720"></canvas></div>
<script src="__LIB__"></script>
<script>
const NAME="__MON__", SKEL="__SKEL__", ATLAS=__ATLAS__, PNG="__PNG__", EXTRA=__EXTRA__, INFO=__INFO__, KENH=__KENH__, VIEW=__VIEW__,
  LA=__LA__, XD=__XD__, YD=__YD__;
__ADDEXTRA__
function b64(s){const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u;}
const st=document.getElementById("st"), cv=document.getElementById("cv"), ov=document.getElementById("ov").getContext("2d");
let cur=null, t=0, speed=1, last=0, hold=0, goc=null;
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
  function chon(c){cur=c;t=0;hold=0;goc=null;[...nut.children].forEach(b=>b.classList.toggle("on",b.dataset.clip===c));
    const i=INFO[c];mo.textContent=c+" · "+i.dur.toFixed(2)+" s"+(i.lap?" · lặp":"")+(i.ev?" · sự kiện: "+i.ev:"")+" — "+i.mo;}
  for(const c of Object.keys(INFO)){const b=document.createElement("button");b.textContent=c.replace("ca_","");b.dataset.clip=c;b.onclick=()=>chon(c);nut.appendChild(b);}
  const td=document.getElementById("td");
  for(const v of [1,0.5,0.25]){const b=document.createElement("button");b.textContent=v+"×";b.onclick=()=>{speed=v;[...td.children].forEach(x=>x.classList.toggle("on",x===b));};td.appendChild(b);if(v===1)b.classList.add("on");}
  chon(Object.keys(INFO)[0]);
  st.textContent="sẵn sàng";
  const [vx,vy,vw,vh]=VIEW, z=Math.max(vw/cv.width,vh/cv.height);
  const X=x=>cv.width/2+(x-vx)/z, Y=y=>cv.height/2-(y-vy)/z;
  function la(x,y,g,a){ov.save();ov.translate(X(x),Y(y));ov.rotate(-g);ov.globalAlpha=a;ov.fillStyle="#7cc85a";ov.strokeStyle="#22401c";ov.lineWidth=2;
    ov.beginPath();ov.ellipse(0,0,70/z,17/z,0,0,6.2832);ov.fill();ov.stroke();ov.restore();}
  function ve(now){
    const dt=Math.min(0.05,(now-last)/1000||0);last=now;
    const i=INFO[cur], a=sd.findAnimation(cur);
    if(i.lap){t=(t+dt*speed)%i.dur;}
    else if(t<i.dur){t=Math.min(i.dur,t+dt*speed);}
    else{hold+=dt;if(hold>0.8&&document.getElementById("lap").checked){t=0;hold=0;goc=null;}}
    sk.setToSetupPose();
    a.apply(sk,t,t,false,[],1,spine.MixBlend.setup,spine.MixDirection.mixIn);
    sk.updateWorldTransform(spine.Physics.update);
    ctx.gl.clearColor(0.42,0.44,0.48,1);ctx.gl.clear(ctx.gl.COLOR_BUFFER_BIT);
    renderer.camera.position.x=vx;renderer.camera.position.y=vy;renderer.camera.zoom=z;
    ctx.gl.viewport(0,0,cv.width,cv.height);renderer.camera.setViewport(cv.width,cv.height);renderer.camera.update();
    renderer.begin();renderer.drawSkeleton(sk,false);renderer.end();
    ov.clearRect(0,0,cv.width,cv.height);
    // đối thủ (người que)
    ov.strokeStyle="rgba(250,235,200,.75)";ov.lineWidth=5;ov.beginPath();ov.arc(X(XD),Y(YD+210),70/z,0,6.2832);
    ov.moveTo(X(XD),Y(YD+140));ov.lineTo(X(XD),Y(YD-160));ov.moveTo(X(XD-120),Y(YD+40));ov.lineTo(X(XD+120),Y(YD+40));
    ov.moveTo(X(XD),Y(YD-160));ov.lineTo(X(XD-90),Y(YD-420));ov.moveTo(X(XD),Y(YD-160));ov.lineTo(X(XD+90),Y(YD-420));ov.stroke();
    const lk=kenh(cur,"la",t), dk_=kenh(cur,"da",t);
    const P=LA.map(n=>{const b=sk.findBone(n);return [b.worldX+b.a*b.data.length*0.6,b.worldY+b.c*b.data.length*0.6,Math.atan2(b.c,b.a)];});
    if(lk[1]>0.5){ if(!goc) goc=P.map(p=>p.slice());
      P.forEach((p,j)=>{const q=lk[0], tx=XD-60+((j*37)%120), ty=YD-150+((j*71)%330);
        const sx=goc[j][0]+(p[0]-goc[j][0])*(1-q), sy=goc[j][1]+(p[1]-goc[j][1])*(1-q);
        const x=sx+(tx-sx)*q, y=sy+(ty-sy)*q+Math.sin(q*3.1416)*(60+j*14);
        la(x,y,q>0.02?Math.atan2(ty-sy,tx-sx)*(q<0.999?1:1):p[2],1);});
    } else goc=null;
    if(dk_[1]>0.5){const q=dk_[0], x=XD-260*(1-q), y=YD+260+1500*(1-q), r=150/z;
      ov.fillStyle="#8c8a7e";ov.strokeStyle="#2b2118";ov.lineWidth=5;ov.beginPath();
      for(let k=0;k<7;k++){const g=k*0.8976+q*2.2, rr=r*(0.82+0.18*((k*53)%7)/6);k?ov.lineTo(X(x)+rr*Math.cos(g),Y(y)+rr*Math.sin(g)):ov.moveTo(X(x)+rr*Math.cos(g),Y(y)+rr*Math.sin(g));}
      ov.closePath();ov.fill();ov.stroke();}
    ov.fillStyle="#bcd";ov.font="15px sans-serif";ov.fillText("t = "+t.toFixed(2)+" s",14,24);
    requestAnimationFrame(ve);
  }
  requestAnimationFrame(ve);
}
main().catch(e=>{st.textContent="LOI "+e+" "+(e.stack||"");});
</script></body></html>"""

MO_TA = {TT + "idle": "nguyên idle_01 của họ", TT + "walk": "nguyên run_01 của họ (bay ngang, vỗ cánh); game lo dời ngang",
         TT + "attack": "ngả lùi lấy đà, BAY LAO tới (run của họ phát nhanh 1,9 lần), ĐÂM MỎ vào đối thủ; khựng; bật lùi bay về",
         TT + "cast": "nhịp đập cánh THỨ BA của skill_03: dựng người xoè cánh, giơ hai cánh ra sau lấy đà, VẶN NGƯỜI QUÉT cánh ra trước: lá "
                      "cánh bay ra găm vào đối thủ; giữ cánh khép chéo; lá rút ra bay về, mở cánh đón, cánh giật nhẹ khi lá về tới",
         TT + "skill": "thu hai cánh ôm thân tụ lực (rung mạnh dần); BUNG cánh ngửa mặt lên trời gọi; thiên thạch đá rơi từ trên cao; đập "
                       "cánh xuống đúng lúc thiên thạch nện vào đầu đối thủ",
         TT + "appear": "bay vào từ phía sau, trên cao (hiện dần), tới nơi dựng người xoè cánh hãm, rồi hạ về dáng nghỉ",
         TT + "hit": "nguyên hit_01 của họ", TT + "die": "nguyên die_01 của họ: lộn nhào rồi rơi nằm sấp"}


def song():
    """trang xem SỐNG (runtime Spine thật, 60 khung/giây, mở bằng file://) trên rig gốc → <scan>/lam_clip/xem/xem.html."""
    import base64
    dung(xem=True)
    extra = open(os.path.join(LAM, "ca_extra.json"), encoding="utf-8").read()
    rieng = dung()
    mo_xe = open(os.path.join(HERE, "mo_xe", "mo_xe.html"), encoding="utf-8").read()
    a = mo_xe.index("function addExtra(data, list) {")
    b = mo_xe.index("// lấy mẫu 30 khung/giây")
    b64 = lambda f: base64.b64encode(open(os.path.join(RIG, f), "rb").read()).decode()
    info = {c: {"dur": CLIP[c][0], "lap": c in LAP, "mo": MO_TA.get(c, ""),
                "ev": ", ".join(f"{e}{' ' + s if s else ''} {x:.2f} s" for x, e, s in SU_KIEN.get(c, []))} for c in CLIP}
    kenh = {c: {k: rieng[c][k] for k in ("bay", "mo", "la", "da")} for c in CLIP}
    lib = "file:///" + os.path.join(HERE, "lib", "spine-player.js").replace(os.sep, "/")
    h = (TRANG.replace("__LIB__", lib).replace("__MON__", MON).replace("__SKEL__", b64(MON + ".skel"))
         .replace("__ATLAS__", json.dumps(open(os.path.join(RIG, MON + ".atlas"), encoding="utf-8").read()))
         .replace("__PNG__", "data:image/png;base64," + b64(MON + ".png")).replace("__EXTRA__", extra)
         .replace("__VIEW__", "[" + VIEW_SONG + "]").replace("__LA__", json.dumps(LA_XUONG)).replace("__XD__", str(XA_DICH))
         .replace("__YD__", str(CAO_DICH))
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
        cl = a[1] if len(a) > 1 and a[1] not in ("", "het") else ",".join(CLIP)
        n = a[2] if len(a) > 2 else "16"
        tt = (f"&t0={a[4]}" if len(a) > 4 else "") + (f"&t1={a[5]}" if len(a) > 5 else "")
        for c in cl.split(","):
            view = a[3] if len(a) > 3 and a[3] not in ("", "het") else VIEW_RIENG.get(c, VIEW)
            vw, vh = [float(x) for x in view.split(",")[2:]]
            _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={c}&extra=ca_extra.json&n={n}&tw=380&th={int(round(380 * vh / vw))}&cols=8&view={view}{tt}")
        dung()
    elif lenh == "song":
        song()
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "ca_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
