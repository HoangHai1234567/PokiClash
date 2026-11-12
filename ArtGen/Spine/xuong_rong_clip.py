# -*- coding: utf-8 -*-
"""Xương rồng tròn: clip RIÊNG theo ý người dùng (2026-11-12), dựng ở TẦNG ĐIỀU KHIỂN của rig gốc monster_3229 rồi để runtime Spine
thật nướng (cách của rong_vay_clip.py / bach_tuoc_clip.py; skill pokiclash-spine-rig mục 00 "CLIP MỚI trên rig gốc").

Người dùng:
- idle: giống họ, sửa đi một chút.
- đánh thường: nhảy tới đối thủ (rig làm bật nhún, code lo phần bay) rồi há thật to mồm cắn.
- chiêu mana: gồng rồi phóng dài các gai trên cơ thể, đâm tứ tung (họ làm gai dài ra bằng tỉ lệ dọc xương của từng gai: skill_02).
- chiêu cuối: thu chân tay vào trong, nhảy lên nhẹ, phồng to, gai dài và nhọn hơn, xoay liên tục rồi tông vào đối thủ, bị bật ngược
  về chỗ cũ (rig làm phồng, nhảy, đáp; code lo bay, bật ngược). Hai clip như Tí Tách: skill (hết clip là dáng đang xoay bay) +
  skill_land (tông, bật về, đáp, xẹp), cung bay do AolaSticker.Jump tính.

Rig gốc điều khiển bằng:
  bone3 (hông: nhún, lắc cả con) → bone4 (chậu: hai chân IK bone5-7 / bone8-10, mục tiêu R2 > R1, L2 > L1 đứng yên trên đất)
  bone4 → bone11 (đế quả cầu) → bone12 (quả cầu: thân, hàm trên bone19, năm gai bone22-25 (+ bone21 dưới bone11), hoa bone29-31)
  bone12 → rotate_02 → bone13 > 14 > 15 (tay TRƯỚC, bên trái người xem; gai nắm tay bone26-28)
  bone12 → rotate_01 → bone16 > 17 > 18 (tay SAU, bên phải; gai nắm tay bone32-34)
  miệng: hàm trên bone19 (con bone12) và hàm dưới bone20 (con bone11) DỜI lại gần nhau là ngậm (dáng gốc = há).

    xuong_rong_clip.py dung                 ghép, ghi <scan>/lam_clip/xr_extra.json
    xuong_rong_clip.py xem [clip,..] [n] [view] [t0] [t1]   tờ khung trên rig gốc (có cung bay giả) → <scan>/lam_clip/khung/<clip>.jpg
    xuong_rong_clip.py gif                  GIF từng clip + trang xem → <scan>/lam_clip/xem/xem.html
    xuong_rong_clip.py mau                  lấy mẫu 30 khung/giây → <scan>/sample_moi.json (xuong_rong_rig.py đọc)
Chạy qua quai/khoa.py chrome (xem, mau mở Chrome ngầm)."""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MON = "monster_3229"
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
B0 = np.array([[b["x"], b["y"], b["rot"], b["sx"], b["sy"]] for b in I["bones"]], float)
IKS = [k["name"] for k in I["ik"]]
SLOT = [s["name"] for s in I["slots"]]
ix = TEN.index
_S = None

TAY_T = ["rotate_02", "bone13", "bone14", "bone15"]            # tay trước (bên trái người xem)
TAY_S = ["rotate_01", "bone16", "bone17", "bone18"]            # tay sau
GAI_THAN = ["bone21", "bone22", "bone23", "bone24", "bone25"]
GAI_TAY_T = ["bone26", "bone27", "bone28"]
GAI_TAY_S = ["bone32", "bone33", "bone34"]
GAI = GAI_THAN + GAI_TAY_T + GAI_TAY_S
HOA = ["bone29", "bone30", "bone31"]
CHAN = ["bone5", "bone6", "bone7", "bone8", "bone9", "bone10"]
S_CHAN = ["P_tuiL1", "P_tuiL2", "P_tuiR1", "P_tuiR2"]
S_TAY = ["P_shouL1", "P_shouL2", "P_shouR1", "P_shouR2", "P_shouR3"]
HAM_T, HAM_D = (-23.7, 3.65), (23.6, -4.27)                    # độ dời hàm trên / hàm dưới lúc NGẬM của idle_01 (dáng gốc = há)


def nhom(ds):
    m = np.zeros(len(TEN), bool)
    for n in ds:
        m[ix(n)] = True
    return m


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y CHƯA áp ràng buộc; k độ trộn IK; an = slot đang ẩn;
    truoc = tay SAU được vẽ ra TRƯỚC thân (lúc gồng hai nắm tay chụm vào giữa)."""

    def __init__(self, u, k, an=(), truoc=False):
        self.u, self.k, self.an, self.truoc = u, k, set(an), truoc

    def chep(self):
        return Dang(self.u.copy(), self.k.copy(), self.an, self.truoc)

    def tron(self, B, w, mat_na=None):
        ww = np.full(len(TEN), float(w)) if mat_na is None else np.where(mat_na, float(w), 0.0)
        return Dang(self.u + (B.u - self.u) * ww[:, None], self.k + (B.k - self.k) * (float(w) if mat_na is None else 0.0), self.an, self.truoc)

    def xoay(self, ten, do):
        self.u[ix(ten), 2] += do
        return self

    def doi(self, ten, dx, dy):
        self.u[ix(ten), 0] += dx
        self.u[ix(ten), 1] += dy
        return self

    def co(self, ten, sx, sy=None):
        self.u[ix(ten), 3] *= sx
        self.u[ix(ten), 4] *= sx if sy is None else sy
        return self


def nap():
    global _S
    if _S is None:
        S = json.load(open(os.path.join(SCAN, "sample_dk.json"), encoding="utf-8"))
        _S = {c: (float(v["dur"]), np.array([f["u"] for f in v["frames"]], float), np.array([[q[0] for q in f["k"]] for f in v["frames"]], float))
              for c, v in S.items()}
    return _S


# A POSE (người dùng 2026-11-12: "tay bên phải có thể làm thõng xuống tức là A pose, không nhất thiết giống con gốc là giơ tay lên"):
# tay SAU (bên phải người xem) của con gốc giơ chếch lên (khúc trên 10°, khúc dưới 31° so với phương ngang); của mình thõng xuống đối
# xứng với tay trước (khúc trên −25°, khúc dưới −63°). Là độ lệch góc cộng vào MỌI dáng lấy từ clip của họ (idle, hit, die...), nên
# nhịp vẫy tay của họ vẫn giữ. Dáng nguồn dùng riêng cho tay (thu, vung) thì lấy nguyên (apose=False).
A_POSE = {"bone16": -36.0, "bone17": -58.0}


def dk(clip, t, lap=False, apose=True):
    dur, U, Kk = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    D = Dang(U[i0] * (1 - w) + U[i1] * w, Kk[i0] * (1 - w) + Kk[i1] * w)
    if apose:
        for n, g in A_POSE.items():
            D.u[ix(n), 2] += g
    return D


def dang_goc():
    """dáng gốc của rig + A pose: dáng để vẽ concept và nướng concept vào khung part."""
    D = Dang(B0.copy(), np.ones(len(IKS)))
    for n, g in A_POSE.items():
        D.u[ix(n), 2] += g
    return D


def goc_tg(D, ten):
    """góc thế giới (xấp xỉ FK: tổng góc riêng dọc chuỗi cha; các xương thân, tay không dính IK) của xương ten."""
    g, p = 0.0, ix(ten)
    while p >= 0:
        g += D.u[p, 2]
        p = I["bones"][p]["parent"]
    return g


def dat_tg(D, ten, goc):
    """đặt góc THẾ GIỚI của xương ten (đặt từ gốc chuỗi ra ngọn)."""
    i = ix(ten)
    D.u[i, 2] += goc - goc_tg(D, ten)
    return D


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


def ham(D, c):
    """miệng: c = 0 há như dáng gốc, 1 ngậm khít như idle, > 1 nghiến, < 0 há to hơn dáng gốc."""
    i, j = ix("bone19"), ix("bone20")
    D.u[i, 0], D.u[i, 1] = B0[i, 0] + HAM_T[0] * c, B0[i, 1] + HAM_T[1] * c
    D.u[j, 0], D.u[j, 1] = B0[j, 0] + HAM_D[0] * c, B0[j, 1] + HAM_D[1] * c
    return D


def gai(D, ds, sx, sy=1.0, k=1.0):
    """gai dài ra: tỉ lệ dọc xương của từng gai (cách của skill_02). sx, sy là số hoặc hàm theo thứ tự gai; k: hệ số bù khi xương
    cha (tay) đang bị thu nhỏ."""
    for q, n in enumerate(ds):
        i = ix(n)
        D.u[i, 3] = B0[i, 3] * (sx(q) if callable(sx) else sx) * k
        D.u[i, 4] = B0[i, 4] * (sy(q) if callable(sy) else sy) * k
    return D


def gai_nghi(D):
    """gai nắm tay về dáng nghỉ (các dáng nguồn của skill_02 gập / thu nhỏ chúng)."""
    R = nghi()
    m = nhom(GAI)
    D.u[m] = R.u[m]
    return D


# tâm và bán kính quả cầu trong hệ xương bone4 ở dáng gốc (bone4 không xoay ở dáng gốc); HO = quả cầu cách mặt đất bao nhiêu
def _tam():
    A = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
    P = np.array(next(x for x in A["atts"] if x["att"] == "P_shenti")["xy"], float).reshape(-1, 2)
    c = (P.min(axis=0) + P.max(axis=0)) / 2
    r = float(P[:, 1].max() - P[:, 1].min()) / 2
    dat = min(float(np.array(x["xy"], float).reshape(-1, 2)[:, 1].min()) for x in A["atts"] if x["att"] in ("P_tuiL2", "P_tuiR2"))
    b4 = next(b for b in A["bones"] if b["name"] == "bone4")
    return c - np.array([b4["x"], b4["y"]]), r, float(c[1] - r - dat)


TAM, RB, HO = _tam()


def cau(D, goc=0.0, s=1.0, dx=0.0, dy=0.0, doc=1.0):
    """CẢ quả cầu (bone4: thân, miệng, tay, gai, hoa; lưới thân bám cả bone4 lẫn bone12 nên phải xoay từ bone4 mới cứng): xoay thêm
    `goc` độ và phồng đều `s` lần QUANH TÂM, giãn thêm `doc` lần theo trục dọc của chính nó; tâm dời (dx, dy) trong hệ bone3."""
    i = ix("bone4")
    r0, sx0, sy0 = math.radians(D.u[i, 2]), D.u[i, 3] / B0[i, 3], D.u[i, 4] / B0[i, 4]
    cx = D.u[i, 0] + sx0 * TAM[0] * math.cos(r0) - sy0 * TAM[1] * math.sin(r0)
    cy = D.u[i, 1] + sx0 * TAM[0] * math.sin(r0) + sy0 * TAM[1] * math.cos(r0)
    r1, sx1, sy1 = r0 + math.radians(goc), sx0 * s, sy0 * s * doc
    D.u[i, 0] = cx + dx - (sx1 * TAM[0] * math.cos(r1) - sy1 * TAM[1] * math.sin(r1))
    D.u[i, 1] = cy + dy - (sx1 * TAM[0] * math.sin(r1) + sy1 * TAM[1] * math.cos(r1))
    D.u[i, 2] += goc
    D.u[i, 3] *= s
    D.u[i, 4] *= s * doc
    return D


def nen(D, doc=1.0, ngang=1.0):
    """nén giãn quả cầu theo trục dọc thân (bone11, trục x chạy lên trên), giữ tâm tại chỗ. Chỉ dùng mức nhẹ (đáy lưới thân bám bone4)."""
    i = ix("bone11")
    g = math.radians(D.u[i, 2])
    v = TAM - B0[i, :2]
    g0 = math.radians(B0[i, 2])
    lx = v[0] * math.cos(g0) + v[1] * math.sin(g0)
    ly = -v[0] * math.sin(g0) + v[1] * math.cos(g0)
    wx, wy = lx * doc, ly * ngang
    D.u[i, 0] = TAM[0] - (wx * math.cos(g) - wy * math.sin(g))
    D.u[i, 1] = TAM[1] - (wx * math.sin(g) + wy * math.cos(g))
    D.u[i, 3] *= doc
    D.u[i, 4] *= ngang
    return D


def chan_treo(D, w, nhac=26.0, khep=10.0):
    """chân rời đất: kéo hai mục tiêu IK lên sát thân và khép vào (lúc đang bay)."""
    D.doi("R2", khep * w, nhac * w)
    D.doi("L2", -khep * w, nhac * w)
    return D


def tay(D, nguon, w):
    """hai tay lấy dáng của `nguon` (chỉ chuỗi xương tay, không lấy gai nắm tay) với trọng số w."""
    m = nhom(TAY_T + TAY_S)
    D.u[m] += (nguon.u[m] - D.u[m]) * w
    return D


# ---------------------------------------------------------------- idle: như họ, chậm hơn một chút, vòng hai nghiến răng xù gai
I_VONG, I_DUR = 1.2, 2.4
I_XU = 1.92          # giây: nghiến răng "tách tách" + xù gai (điểm phá nhịp, 80% vòng lặp)


def idle(t):
    """IDLE 2,4 s lặp = hai vòng nhún của idle_01 (mỗi vòng 1,2 s thay vì 1,0 s). Vòng một nhai một nhịp như họ; vòng hai giữ miệng
    cười há, tới 1,92 s nghiến răng hai cái nhanh, cùng lúc mọi gai xù dài ra rồi rút (lệch pha từng gai)."""
    u = (t % I_DUR) / I_VONG
    D = dk("idle_01", (u % 1.0) * 1.0, lap=True)
    i19, i20 = ix("bone19"), ix("bone20")
    if u >= 1.0:
        c0 = (D.u[i19, 0] - B0[i19, 0]) / HAM_T[0]           # độ ngậm của họ ở giờ này
        x = t % I_DUR
        tach = max(cung(x, I_XU - 0.05, I_XU, I_XU + 0.02, I_XU + 0.09), cung(x, I_XU + 0.11, I_XU + 0.16, I_XU + 0.18, I_XU + 0.27))
        ham(D, 0.22 * c0 + 1.08 * tach)
        for q, n in enumerate(GAI):
            s = cung(x, I_XU - 0.04 + 0.012 * q, I_XU + 0.05 + 0.012 * q, I_XU + 0.16 + 0.012 * q, I_XU + 0.42 + 0.012 * q)
            D.co(n, 1.0 + (0.42 if n in GAI_THAN else 0.30) * s, 1.0)
        D.doi("bone3", 0.0, 3.5 * tach)
    return D


# ---------------------------------------------------------------- attack: nhún, bật tới, há LỐ, đớp mạnh
F = 1.0 / FPS
A_NHUN, A_BAT, A_HA, A_CAN, A_NHA, A_VE, A_DUR = 0.28, 0.36, 15 * F, 20 * F, 26 * F, 34 * F, 1.40
A_HA_TO = 0.12                   # hai hàm dời xa hơn dáng gốc chừng này. Quá ~0,2 thì hai dải răng (cứng, bám hàm) thò ra ngoài vành
#                                  môi (vành môi bám cả bốn xương nên đi ít hơn): lộ dải kem trên thân. Phần "lố" là do cả
#                                  quả cầu phồng 1,25 lần và giãn dọc 1,44 lần quanh tâm
A_XA, A_CAO = 150.0, 62.0        # cung bay (đơn vị con gốc): tới trước A_XA, đỉnh cao A_CAO (game co giãn cho đỉnh rơi vào đối thủ)


def attack(t):
    """ĐÒN THƯỜNG 1,4 s (người dùng 2026-11-12: "há to hơn, lố một chút rồi đớp mạnh"). Nhún lấy đà 0 → 0,28 (ngồi thụp, nghiến
    răng, tay thu); bật 0,36; đang bay: ngửa người, miệng há dần tới 0,50 và VỌT QUÁ (cả quả cầu phồng 1,28 lần, giãn dọc 1,4 lần:
    miệng to gần gấp đôi lúc nghỉ), giữ há rung 0,50 → 0,60, hít thêm một nấc; ĐỚP trong đúng MỘT khung (0,633 → 0,667): sập hàm,
    chúi tới 26°, quả cầu bẹp dọc còn 0,78, gai xù; sự kiện trung 0,667; ngoạm giữ, lắc tắt dần tới 0,87; nhả, bật về tới 1,13;
    đáp, nhún, về dáng nghỉ."""
    R = nghi()
    D = R.chep()
    thu = dk("skill_02", 0.60, apose=False)         # dáng hai tay thu sát thân
    vung = dk("skill_02", 0.47, apose=False)        # dáng hai tay vung cao
    n = cung(t, 0.0, A_NHUN - 0.08, A_NHUN, A_BAT)                      # nhún
    b = cung(t, A_NHUN, A_BAT, A_BAT + 0.02, A_BAT + 0.10)              # giãn lúc bật
    bay = cung(t, A_BAT - 0.03, A_BAT + 0.05, A_VE - 0.06, A_VE + 0.02)  # rời đất
    ha_ = cung(t, A_BAT, A_HA - 0.03, A_CAN - F + 0.001, A_CAN - 0.001)  # há (tắt trong đúng một khung)
    vot = cung(t, A_HA - 0.10, A_HA - 0.02, A_HA, A_HA + 0.09)           # vọt quá lúc vừa há hết
    hit_ = cung(t, A_CAN - 4 * F, A_CAN - 2 * F, A_CAN - F + 0.001, A_CAN - 0.001)   # hít thêm một nấc ngay trước khi đớp
    can = cung(t, A_CAN - F + 0.001, A_CAN - 0.001, A_NHA - 0.04, A_NHA + 0.10)      # ngậm
    ep = cung(t, A_CAN - F + 0.001, A_CAN - 0.001, A_CAN + F, A_CAN + 5 * F)         # bẹp lúc đớp
    dap = cung(t, A_VE - 0.02, A_VE + 0.05, A_VE + 0.07, A_VE + 0.22)   # bẹp lúc đáp
    giu = cung(t, A_HA, A_HA + 0.02, A_CAN - F, A_CAN - 0.001)          # rung lúc giữ há
    rung = 1.0 if int(t * FPS + 0.5) % 2 else -1.0
    r = max(0.0, t - A_CAN)
    lac = math.exp(-r * 6.5) * math.sin(r * 46.0) if A_CAN <= t < A_NHA + 0.06 else 0.0
    D.doi("bone3", 0.0, -30.0 * n - 20.0 * dap + 10.0 * b)
    D.xoay("bone3", 9.09 * max(n, bay) * (1 - dap))                     # idle giây 0 nghiêng −9°: dựng thẳng lại khi đánh
    nen(D, 1.0 - 0.11 * n + 0.12 * b - 0.12 * dap, 1.0 + 0.05 * n + 0.05 * dap)
    cau(D, goc=-6.0 * n + 22.0 * ha_ + 5.0 * hit_ - 26.0 * can + 7.0 * lac + 1.4 * rung * giu,
        s=1.0 + 0.04 * n + (0.25 + 0.08 * vot + 0.04 * hit_) * ha_ - 0.02 * can + 0.05 * ep + 0.04 * dap,
        doc=1.0 + (0.44 + 0.10 * vot + 0.07 * hit_) * ha_ - 0.22 * ep - 0.04 * can + 0.05 * lac)
    ham(D, 1.25 * n * (1 - ha_) - (A_HA_TO + 0.04 * vot + 0.04 * hit_) * ha_ + 1.45 * can + (0.22 * abs(lac) if can > 0.5 else 0.0))
    tay(D, thu, max(n, can))
    tay(D, vung, ha_ * (1 - can))
    chan_treo(D, 0.55 * bay)
    gai(D, GAI_THAN, 1.0 + 0.25 * ha_ + 0.55 * ep + 0.15 * can)
    for q, nm in enumerate(HOA):
        D.xoay(nm, -16.0 * ha_ + 22.0 * ep + 9.0 * lac)
    return D


def attack_bay(t):
    """cung bay của đòn thường (đơn vị con gốc, x tới trước): đặt lên xương `move` ở rig của mình; tới nơi lúc vừa há hết, đớp tại chỗ."""
    t0, t1 = A_BAT - 0.02, A_CAN - 2 * F
    if t < t0:
        return 0.0, 0.0
    if t <= t1:
        u = (t - t0) / (t1 - t0)
        return A_XA * ra(u, 1.5) * 0.94, A_CAO * 4 * u * (1 - u) + 14.0 * u
    if t <= A_CAN:
        return A_XA * (0.94 + 0.06 * (t - t1) / (A_CAN - t1)), 14.0          # đớp: chồm thêm một chút
    if t <= A_NHA:
        return A_XA, 14.0
    if t <= A_VE:
        u = (t - A_NHA) / (A_VE - A_NHA)
        return A_XA * (1 - em(u)), 14.0 * (1 - u) + 38.0 * 4 * u * (1 - u)
    return 0.0, 0.0


# ---------------------------------------------------------------- cast: giơ hai tay lên trời, vòng xuống chụm vào giữa GỒNG, gai phóng dài
C_GIO, C_GIU, C_GONG, C_PHUN, C_HET, C_DUR = 0.22, 0.30, 0.44, 15 * F, 1.30, 1.90
C_GAI = 4.6                      # gai thân dài chừng này lần (người dùng: "gai dài ra vẫn ít" ở bản 2,6–3,4 lần)
C_GAI_TAY = 1.9
# góc THẾ GIỚI của khúc tay (độ; 0 = sang phải, 90 = lên): (giơ lên trời, gồng chụm vào giữa)
C_TAY = {"bone13": (-250.0, -125.0), "bone14": (-265.0, -40.0),      # tay trước (bên trái): lên qua phía ngoài, vòng xuống, quặp vào
         "bone16": (70.0, -55.0), "bone17": (85.0, -140.0)}          # tay sau (bên phải): đối xứng


def cast(t):
    """CHIÊU MANA 1,9 s (người dùng 2026-11-12: "gồng là đứng bằng hai chân, hai tay giơ lên trời rồi lập tức đưa vòng xuống dưới vào
    giữa kiểu gồng cơ thể lên, gai dài ra hẳn"). Đứng hai chân, hai tay giơ thẳng lên trời 0 → 0,22 (thân vươn, há miệng hít), giữ
    tới 0,30; hai tay quật VÒNG ra ngoài – xuống – chụm vào giữa trước bụng 0,30 → 0,44 (dáng gồng của lực sĩ: thụp nhẹ, nghiến răng,
    quả cầu căng, rung); 0,50 BUNG: mọi gai phóng dài 4,6–5,6 lần trong hai khung (vọt quá rồi về), quả cầu phồng 1,1 lần, há gầm,
    sự kiện phun; giữ gồng tới 1,30: từng gai thụt ra thụt vào lệch pha (đâm tứ tung), thân rung; het_phun; gai rút, tay buông về."""
    R = nghi()
    D = R.chep()
    gio = cung(t, 0.0, C_GIO, C_GIU, C_GONG)
    g = cung(t, C_GIU, C_GONG, C_HET, C_HET + 0.30)
    bu = cung(t, C_PHUN - F + 0.001, C_PHUN + F, C_HET, C_HET + 0.20)
    vot = cung(t, C_PHUN - F + 0.001, C_PHUN + F, C_PHUN + 2 * F, C_PHUN + 0.22)
    rung = (1.0 if int(t * FPS + 0.5) % 2 else -1.0) * g
    D.xoay("bone3", 9.09 * max(gio, g))
    D.doi("bone3", 0.0, 11.0 * gio - 17.0 * g)
    nen(D, 1.0 + 0.06 * gio - 0.07 * g, 1.0 - 0.02 * gio + 0.04 * g)
    cau(D, goc=4.0 * gio - 6.0 * g + 1.4 * rung, s=1.0 + 0.02 * gio + 0.03 * g + (0.10 + 0.07 * vot) * bu + 0.010 * rung)
    ham(D, -0.25 * gio * (1 - g) + 1.38 * g * (1 - bu) + (-0.15 + 0.10 * abs(rung)) * bu)
    # hai tay theo góc thế giới: nghỉ → giơ → gồng → nghỉ
    for ten, (len_, gong) in C_TAY.items():
        w0 = goc_tg(R, ten) + 9.09 * 0.0
        a = cong([(0.0, w0), (C_GIO, len_), (C_GIU, len_ + (4.0 if gong > len_ else -4.0)), (C_GONG, gong), (C_HET, gong), (C_HET + 0.34, w0)], t,
                 [lambda x: ra(x, 2.0), None, lambda x: vao(x, 1.8), None, em])
        dat_tg(D, ten, a + (2.2 * rung if ten in ("bone14", "bone17") else 0.0))
    D.xoay("bone15", 26.0 * g)
    D.xoay("bone18", -26.0 * g)
    D.doi("rotate_02", 0.0, -22.0 * g)              # hai vai xích vào giữa lúc gồng (hệ bone12: y dương là bên trái người xem)
    D.doi("rotate_01", 0.0, 26.0 * g)
    D.truoc = C_GIU - 0.04 < t < C_HET + 0.22

    def dai(q, lon):
        s_ = ((t - C_PHUN) * 4.3 + 0.31 * q) % 1.0
        dam = 0.72 + 0.32 * (1 - s_) ** 1.6                        # đâm: thọc ra nhanh, rút về chậm, mỗi gai một pha
        k_ = 1.16 * vot + (1 - vot) * dam
        return (1.0 - 0.28 * g * (1 - bu)) * (1 - bu) + bu * (1.0 + (lon + 0.5 * (q % 3) - 1.0) * k_)

    gai(D, GAI_THAN, lambda q: dai(q, C_GAI), lambda q: 1.0 - 0.10 * bu)
    gai(D, GAI_TAY_T, lambda q: dai(q + 5, C_GAI_TAY), 1.0)
    gai(D, GAI_TAY_S, lambda q: dai(q + 8, C_GAI_TAY), 1.0)
    for q, nm in enumerate(HOA):
        D.xoay(nm, 12.0 * gio - 8.0 * g + 14.0 * bu * math.sin(2 * math.pi * 6.0 * t + 0.9 * q))
    return D


# ---------------------------------------------------------------- skill + skill_land: thu chân tay, nhảy lên không, phồng, xoay, lao, bật về
# Người dùng 2026-11-12 (sau khi xem trong trận: "impact hơi nhẹ"): "kịch bản là nhảy lên không trung, xoay rất nhanh tại chỗ 1–1,5
# giây rồi lao vào đối thủ, sau đó như kiểu bị bật theo hướng vòng cung trở lại, shake cam". Rig: cuộn, nhảy LÊN CAO và ở trên không,
# phồng + gai dài, xoay rất nhanh tại chỗ 1,25 s (lơ lửng, hơi nhấp nhô), ghìm lùi một nhịp rồi lao (code cho bay: hạ từ trên không
# xuống ngang thân đối thủ); chạm, ghì, bị bật về theo vòng cung (code), đáp, xẹp, bung chân tay.
S_THU, S_NHUN, S_DINH = 0.30, 0.42, 0.66
S_XOAY = 1.25                     # xoay tại chỗ trên không chừng này giây
S_BAT = S_DINH + S_XOAY           # 1,91: rời chỗ (sự kiện bat: code cho bay)
S_DUR = S_BAT + 0.15              # 2,06: hết clip, vẫn đang lao
S_CAO = 150.0                     # nhảy lên cao chừng này (quả cầu cao ~236)
S_PHONG = 1.24                    # quả cầu phồng to chừng này lần
S_GAI = 2.5                       # gai dài chừng này lần
L_CHAM, L_GHI, L_VE, L_DUR = 0.14, 0.30, 0.72, 1.50      # skill_land: chạm đối thủ, hết ghì (JumpStay 0,16), về tới chỗ (JumpBack 0,42)
W_MAX = -1800.0                   # độ/giây lúc xoay nhanh nhất (âm = lăn về phía trước, bên phải): 5 vòng/giây
S_TANG = 0.30                     # xoay nhanh dần chừng này giây rồi đều


def _goc_skill(t):
    """góc xoay của quả cầu trong clip skill: bắt đầu xoay ở đỉnh cú nhảy, nhanh dần trong S_TANG giây tới W_MAX, rồi đều."""
    if t <= S_DINH:
        return 0.0
    r = t - S_DINH
    if r <= S_TANG:
        return W_MAX * r * r / (2.0 * S_TANG)
    return W_MAX * S_TANG / 2.0 + W_MAX * (r - S_TANG)


G_HET = _goc_skill(S_DUR)


def _goc_land(t):
    """góc trong skill_land: nối tiếp G_HET, xoay đều tới lúc chạm; ghì: chậm dần; bật về: xoay NGƯỢC chậm dần, dừng đúng bội 360."""
    if t <= L_CHAM:
        return G_HET + W_MAX * t
    g1 = G_HET + W_MAX * L_CHAM
    if t <= L_GHI:
        u = (t - L_CHAM) / (L_GHI - L_CHAM)
        return g1 + W_MAX * 0.45 * (L_GHI - L_CHAM) * (u - u * u / 2.0)
    g2 = g1 + W_MAX * 0.45 * (L_GHI - L_CHAM) / 2.0
    dich = math.ceil((g2 + 620.0) / 360.0) * 360.0            # xoay ngược ít nhất ~620° rồi dừng ở bội 360
    T = L_VE + 0.10
    if t >= T:
        return dich
    u = (t - L_GHI) / (T - L_GHI)
    return g2 + (dich - g2) * (1 - (1 - u) ** 2)


def _tren_khong(tg):
    """độ cao của quả cầu so với lúc nằm đất, theo giờ tính từ đầu clip skill (skill_land = S_DUR + t): nhảy lên S_CAO, lơ lửng nhấp
    nhô lúc xoay, ghìm lên một chút trước khi lao, rồi hạ dần về 0 đúng lúc chạm đối thủ (phần bay ngang do code)."""
    if tg <= S_NHUN:
        return 0.0
    if tg <= S_DINH:
        return S_CAO * ra((tg - S_NHUN) / (S_DINH - S_NHUN), 2.2)
    if tg <= S_BAT:
        r = tg - S_DINH
        ghim = cung(tg, S_BAT - 0.22, S_BAT - 0.06, S_BAT - 0.02, S_BAT + 0.04)
        return S_CAO + 7.0 * math.sin(2 * math.pi * 1.6 * r) * min(1.0, r / 0.3) + 16.0 * ghim
    u = (tg - S_BAT) / (S_DUR + L_CHAM - S_BAT)
    return S_CAO * (1.0 - vao(u, 1.5)) if u < 1.0 else 0.0


def _cuon(D, w):
    """thu chân tay vào trong (w: 0 → 1): tay co ngắn rút sát quả cầu, chân rút lên; w = 1 thì ẩn hẳn khúc tay, nắm tay, chân, chỉ
    còn GAI nắm tay ló ra ở mép quả cầu như gai thân."""
    for goc_ in ("rotate_02", "rotate_01"):
        D.co(goc_, 1.0 - 0.55 * w)
    for n in GAI_TAY_T + GAI_TAY_S:
        D.co(n, 1.0 / (1.0 - 0.55 * w))                        # gai nắm tay giữ cỡ
    D.doi("R2", 30.0 * w, 46.0 * w)
    D.doi("L2", -30.0 * w, 46.0 * w)
    for n in ("bone5", "bone8"):
        D.co(n, 1.0 - 0.6 * w)
    if w > 0.985:
        D.an = set(D.an) | set(S_CHAN) | set(S_TAY)
    return D


def _cau_gai(D, p, x, t, w):
    """gai của quả cầu lúc phồng (p: 0 → 1 phồng, x: rung theo giờ, w: độ thu tay, để bù cỡ gai nắm tay)."""
    def dai(q):
        return 1.0 + (S_GAI - 1.0 + 0.16 * (q % 3) + 0.10 * math.sin(2 * math.pi * 5.0 * t + 1.3 * q) * x) * p
    k = 1.0 / (1.0 - 0.55 * w)
    gai(D, GAI_THAN, dai, lambda q: 1.0 - 0.14 * p)
    gai(D, GAI_TAY_T, lambda q: dai(q + 5), lambda q: 1.0 - 0.10 * p, k=k)
    gai(D, GAI_TAY_S, lambda q: dai(q + 8), lambda q: 1.0 - 0.10 * p, k=k)
    return D


def skill(t):
    """CHIÊU CUỐI nửa đầu 2,06 s. Thu chân tay vào trong 0 → 0,30 (quả cầu hạ xuống đất, nghiến răng); nhún 0,42; NHẢY LÊN KHÔNG, tới
    đỉnh 0,66 (cao 150): PHỒNG 1,24 lần (vọt quá rồi về), gai phóng dài 2,5 lần; XOAY RẤT NHANH tại chỗ trên không 1,25 s (nhanh dần
    0,3 s tới 5 vòng/giây, lơ lửng nhấp nhô); ghìm lên một nhịp 1,7 → 1,9; sự kiện bat 1,91 (rời chỗ: code cho lao); hết clip vẫn
    đang xoay, đang hạ dần về phía đối thủ."""
    R = nghi()
    thu = dk("skill_02", 0.60, apose=False)
    D = R.chep()
    w = em(t / S_THU)
    tay(D, thu, w)
    _cuon(D, w)
    nh = cung(t, S_THU - 0.06, S_NHUN - 0.03, S_NHUN, S_NHUN + 0.08)
    p = cung(t, S_DINH - 0.16, S_DINH - 0.03, 99, 100)
    vot = cung(t, S_DINH - 0.12, S_DINH - 0.03, S_DINH, S_DINH + 0.16)
    ghim = cung(t, S_BAT - 0.22, S_BAT - 0.06, S_BAT - 0.02, S_BAT + 0.04)
    xoay = _goc_skill(t)
    D.xoay("bone3", 9.09 * w)
    s = 1.0 + (S_PHONG - 1.0) * p + 0.10 * vot + 0.05 * ghim
    gian = cung(t, S_NHUN, S_NHUN + 0.07, S_NHUN + 0.10, S_DINH - 0.1)
    nen(D, 1.0 - 0.13 * nh + 0.08 * gian, 1.0 + 0.06 * nh - 0.03 * gian)
    cau(D, goc=xoay, s=s, dx=-14.0 * ghim, dy=-HO * w - 10.0 * nh + _tren_khong(t) + (s - 1.0) * RB)
    ham(D, 1.3 * w * (1 - p) + 0.15 * p)
    _cau_gai(D, p, p, t, w)
    for q, n in enumerate(HOA):
        D.xoay(n, -14.0 * p * min(1.0, abs(xoay) / 360.0) + 10.0 * nh)
    return D


def skill_land(t):
    """CHIÊU CUỐI nửa sau 1,5 s. Đang lao, xoay đều, hạ từ trên không xuống ngang thân đối thủ 0 → 0,14; CHẠM 0,14 (sự kiện cham_dat;
    ép một khung), ghì xoay chậm dần tới 0,30; bị bật ngược về theo vòng cung (code), xoay ngược chậm dần, về tới chỗ 0,72 (sự kiện
    dap): bẹp nặng, xẹp về cỡ thường, gai rút, chân tay bung ra (vọt quá), nhún hai nhịp, về dáng nghỉ."""
    R = nghi()
    thu = dk("skill_02", 0.60, apose=False)
    D = R.chep()
    ve = cung(t, L_VE - 0.02, L_VE + 0.16, 99, 100)                  # 0 = còn là quả cầu, 1 = đã bung ra
    w = 1.0 - ve
    tay(D, thu, w)
    _cuon(D, w)
    p = 1.0 - cung(t, L_VE - 0.03, L_VE + 0.14, 99, 100)
    xoay = _goc_land(t)
    bep = cung(t, L_CHAM - 0.02, L_CHAM + 0.02, L_CHAM + 0.05, L_CHAM + 0.16)
    dap = cung(t, L_VE - 0.03, L_VE + 0.03, L_VE + 0.06, L_VE + 0.26)
    r = max(0.0, t - L_VE)
    nay = math.exp(-r * 6.0) * math.sin(r * 21.0) if t > L_VE else 0.0
    D.xoay("bone3", 9.09 * w)
    D.doi("bone3", 0.0, (-22.0 * dap + 8.0 * nay) * (1 - w))
    s = (1.0 + (S_PHONG - 1.0) * p) * (1.0 - 0.10 * bep)          # chạm: quả cầu đang xoay nên chỉ ép đều
    nen(D, 1.0 - 0.17 * dap + 0.05 * nay, 1.0 + 0.09 * dap)
    cau(D, goc=xoay, s=s, dy=-HO * w + (s - 1.0) * RB + _tren_khong(S_DUR + t) + (10.0 * w if L_CHAM < t < L_VE else 0.0))
    ham(D, 0.15 * p + 0.9 * dap * (1 - p))
    _cau_gai(D, p, p, t + S_DUR, w)
    bung = cung(t, L_VE + 0.02, L_VE + 0.12, L_VE + 0.14, L_VE + 0.34)
    for goc_ in ("rotate_02", "rotate_01"):
        D.co(goc_, 1.0 + 0.16 * bung)
    return D


# ---------------------------------------------------------------- appear: trồi từ đất lên (người dùng dặn 2026-11-12)
P_SAU = 335.0                     # cả con nằm sâu chừng này dưới mặt đất lúc đầu (cao cả con ~315)
P_NHU = 150.0                      # vành hoa nhú lên khỏi mặt đất chừng này
P_HOA, P_LAY, P_THUT, P_TROI, P_DINH, P_CHAM, P_DUR = 0.26, 0.74, 0.86, 0.90, 1.06, 1.22, 2.2
P_VOT = 46.0                      # vọt lên khỏi mặt đất chừng này rồi rơi về


def appear(t):
    """APPEAR 2,2 s, TRỒI TỪ ĐẤT LÊN (mặt nạ cắt ở mặt đất và ụ đất nằm ở rig của mình; đất văng là VFX, rig bắn sự kiện).
    Đất nứt, vành hoa nhú lên 0 → 0,26 (sự kiện nut_dat 0); hoa ngó nghiêng, lắc lư tới 0,74; thụt xuống lấy đà 0,86; VỌT lên
    0,90 → 1,06 (sự kiện troi 0,90: đất văng), còn cuộn tròn lúc chui ra, lên tới nơi thì chân tay bung ra; rơi chạm đất 1,22 (sự
    kiện cham_dat): bẹp, lắc người rũ đất, há miệng gầm một cái xù gai, về dáng nghỉ."""
    R = nghi()
    thu = dk("skill_02", 0.60, apose=False)
    D = R.chep()
    w = 1.0 - cung(t, P_DINH - 0.10, P_DINH + 0.06, 99, 100)            # 1 = cuộn tròn (dưới đất), 0 = đã bung
    tay(D, thu, w)
    _cuon(D, min(w, 0.97))
    dap = cung(t, P_CHAM - 0.02, P_CHAM + 0.03, P_CHAM + 0.06, P_CHAM + 0.28)
    r = max(0.0, t - P_CHAM)
    nay = math.exp(-r * 5.5) * math.sin(r * 19.0) if t > P_CHAM else 0.0
    ru = math.exp(-max(0.0, r - 0.10) * 4.2) * math.sin((r - 0.10) * 2 * math.pi * 5.2) if r > 0.10 else 0.0   # rũ đất
    gam = cung(t, 1.52, 1.64, 1.84, 2.06)
    lay = cung(t, P_HOA - 0.06, P_HOA + 0.06, P_LAY - 0.04, P_THUT)     # hoa ngó nghiêng
    D.xoay("bone3", 9.09 * max(w, dap, abs(ru), gam * 0.6))
    D.doi("bone3", 0.0, (-24.0 * dap + 10.0 * nay) * (1 - w))
    nen(D, 1.0 + 0.10 * cung(t, P_TROI, P_TROI + 0.05, P_DINH - 0.06, P_DINH + 0.05) - 0.18 * dap + 0.06 * nay + 0.05 * gam, 1.0 + 0.08 * dap)
    cau(D, goc=7.0 * lay * math.sin(2 * math.pi * 2.1 * (t - P_HOA)) + 8.0 * ru + 9.0 * gam, s=1.0 + 0.12 * gam, dy=-HO * w + 0.12 * gam * RB)
    ham(D, 1.2 * w + 1.0 * dap * (1 - w) - 0.15 * gam + 0.5 * cung(t, 1.36, 1.46, 1.50, 1.58))
    gai(D, GAI_THAN, 1.0 + 0.5 * gam + 0.25 * abs(ru))
    for q, n in enumerate(HOA):
        D.xoay(n, 22.0 * lay * math.sin(2 * math.pi * 3.0 * (t - P_HOA) - 0.9 * q) + 14.0 * abs(ru) * math.sin(40.0 * t + q))
    return D


def appear_bay(t):
    """độ dời dọc của cả con trong appear (đơn vị con gốc; 0 = đứng trên mặt đất)."""
    day = -(P_SAU - P_NHU)
    if t <= P_HOA:
        return 0.0, -P_SAU + P_NHU * ra(t / P_HOA, 2.2)
    if t <= P_LAY:
        return 0.0, day + 7.0 * math.sin(2 * math.pi * 2.1 * (t - P_HOA))
    if t <= P_THUT:
        return 0.0, day - 12.0 * em((t - P_LAY) / (P_THUT - P_LAY))
    if t <= P_TROI:
        return 0.0, day - 12.0
    if t <= P_DINH:
        return 0.0, (day - 12.0) + (P_VOT - (day - 12.0)) * ra((t - P_TROI) / (P_DINH - P_TROI), 2.0)
    if t <= P_CHAM:
        return 0.0, P_VOT * (1 - vao((t - P_DINH) / (P_CHAM - P_DINH), 2.0))
    return 0.0, 0.0


# ---------------------------------------------------------------- walk: lạch bạch tại chỗ (game tự dời)
W_DUR = 0.8
W_BUOC, W_NHAC = 40.0, 22.0


def walk(t):
    """WALK 0,8 s lặp: hai chân ngắn bước so le (mục tiêu IK: nhấc, đưa tới, đặt, kéo về sau), quả cầu lắc lư sang hai bên và nhún
    hai nhịp mỗi vòng, hơi chúi tới, hai tay vung ngược nhau, miệng nhóp nhép theo bước, hoa lắc trễ pha. Đi về bên phải."""
    D = nghi()
    u = (t / W_DUR) % 1.0
    a = 2 * math.pi * u

    def buoc(pha):
        x = (u + pha) % 1.0
        if x < 0.42:
            s_ = x / 0.42
            return W_BUOC * (em(s_) - 0.5), W_NHAC * math.sin(math.pi * s_)
        s_ = (x - 0.42) / 0.58
        return W_BUOC * (0.5 - s_), 0.0

    for muc, pha in (("R2", 0.0), ("L2", 0.5)):
        dx, dy = buoc(pha)
        D.doi(muc, dx, dy)
    D.xoay("bone3", 9.09 - 4.0 + 5.5 * math.sin(a + 0.5))
    D.doi("bone3", 3.0 * math.sin(a), -5.0 + 6.5 * math.sin(2 * a + 1.1))
    nen(D, 1.0 + 0.035 * math.sin(2 * a + 2.4), 1.0 - 0.02 * math.sin(2 * a + 2.4))
    D.xoay("bone13", 15.0 * math.sin(a + 0.3))
    D.xoay("bone14", 9.0 * math.sin(a - 0.3))
    D.xoay("bone16", -15.0 * math.sin(a + 0.3))
    D.xoay("bone17", -9.0 * math.sin(a - 0.3))
    ham(D, 0.45 + 0.35 * math.sin(2 * a + 0.4))
    for q, n in enumerate(HOA):
        D.xoay(n, 11.0 * math.sin(2 * a - 0.8 * q - 0.6))
    return D


def hit(t):
    return dk("hit_01", t)


def die(t):
    return dk("die_01", t)


CLIP = {"xr_dang": (0.0334, lambda t: dang_goc()), "xr_hit": (nap()["hit_01"][0], hit), "xr_die": (nap()["die_01"][0], die),
        "xr_idle": (I_DUR, idle), "xr_attack": (A_DUR, attack), "xr_cast": (C_DUR, cast), "xr_skill": (S_DUR, skill),
        "xr_skill_land": (L_DUR, skill_land), "xr_appear": (P_DUR, appear), "xr_walk": (W_DUR, walk)}
BAY = {"xr_attack": attack_bay, "xr_appear": appear_bay}        # cung dời của xương move (đơn vị con gốc), rig của mình đọc
SU_KIEN = {"xr_dang": [], "xr_hit": [], "xr_die": [], "xr_idle": [], "xr_attack": [(A_CAN, "trung", "")], "xr_cast": [(C_PHUN, "phun", ""), (C_HET, "het_phun", "")],
           "xr_skill": [(S_DINH - 0.06, "phong", ""), (S_BAT, "bat", "")], "xr_skill_land": [(0.0, "tong", ""), (L_CHAM, "cham_dat", ""), (L_VE, "dap", "")],
           "xr_appear": [(0.0, "nut_dat", ""), (P_TROI, "troi", ""), (P_CHAM, "cham_dat", "")], "xr_walk": []}


def _bay_gia(ten, t):
    """cung bay GIẢ để xem thử trên rig gốc (thay phần code game lo): đòn thường và appear dùng BAY; chiêu cuối bay thẳng tới rồi bật về."""
    if ten in BAY:
        return BAY[ten](t)
    def lao(u):                                   # như AolaSticker.Jump nhánh Rams: nhanh dần
        return u * u * (0.4 + 0.6 * u)
    if ten == "xr_skill" and t > S_BAT:
        return 340.0 * lao((t - S_BAT) / (S_DUR - S_BAT + L_CHAM)), 0.0
    if ten == "xr_skill_land":
        if t <= L_CHAM:
            return 340.0 * lao((S_DUR - S_BAT + t) / (S_DUR - S_BAT + L_CHAM)), 0.0
        if t <= L_GHI:
            return 340.0, 0.0
        if t <= L_VE:
            u = (t - L_GHI) / (L_VE - L_GHI)
            return 340.0 * (1 - em(u)), 230.0 * 4 * u * (1 - u)
    return 0.0, 0.0


S_TAY_SAU = ["P_shouL1", "P_shouL2", "P_shouL33", "P_shouL32", "P_shouL31"]
TRUOC = [x for x in SLOT if x not in S_TAY_SAU] + S_TAY_SAU          # thứ tự vẽ khi tay sau ra trước thân


def dung(xem=False):
    out = []
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        Ds = [fn(t) for t in ts]
        U = np.array([d.u for d in Ds])
        if xem:
            for j, t in enumerate(ts):
                U[j, ix("bone"), :2] += _bay_gia(ten, t)
        Kk = np.array([d.k for d in Ds])
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
        iks = {kn: [[round(t, 4), round(float(v), 4), I["ik"][j]["bend"]] for t, v in zip(ts, Kk[:, j])] for j, kn in enumerate(IKS)
               if np.abs(Kk[:, j] - 1).max() > 1e-4}
        slots = {}
        for sl in sorted(set().union(*[d.an for d in Ds])):
            ks = []
            for t, d in zip(ts, Ds):
                v = None if sl in d.an else sl
                if not ks or ks[-1][1] != v:
                    ks.append([round(t, 4), v])
            slots[sl] = {"attachment": ks}
        thu_tu = []
        for t, d in zip(ts, Ds):
            v = TRUOC if d.truoc else None
            if (not thu_tu and v) or (thu_tu and thu_tu[-1][1] != v):
                thu_tu.append([round(t, 4), v])
        o_ = {"name": ten, "dur": dur, "bones": bones, "iks": iks, "slots": slots}
        if thu_tu:
            o_["draworder"] = thu_tu
        out.append(o_)
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, IK {list(iks)}, ẩn {len(slots)} slot")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "xr_extra.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "xr_extra.json"))


def _chay(*a):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "chay.py"), *a], capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace")[-900:])
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)


VIEW = "150,150,900,520"
VIEW_RIENG = {"xr_appear": "20,218,900,520"}        # đáy khung = mặt đất (thay cho mặt nạ cắt của rig mình)


def gif(n=46):
    """GIF từng clip trên RIG GỐC (hình của game tham khảo: chỉ để xem nội bộ) + trang xem → <scan>/lam_clip/xem/."""
    from PIL import Image
    dung(xem=True)
    ra_ = os.path.join(LAM, "xem")
    os.makedirs(ra_, exist_ok=True)
    tw, th, cols = 450, 300, 8
    nhom_ = {}
    ds = [c for c in CLIP if c != "xr_dang"]
    for c in ds:
        nhom_.setdefault(VIEW_RIENG.get(c, VIEW), []).append(c)
    for view, cs in nhom_.items():
        _chay("sheet", LAM, MON, os.path.join(LAM, "khung_gif"), f"anims={','.join(cs)}&extra=xr_extra.json&n={n}&tw={tw}&th={th}&cols={cols}&view={view}")
    the = []
    for c in ds:
        dur = CLIP[c][0]
        im = Image.open(os.path.join(LAM, "khung_gif", c + ".jpg")).convert("RGB")
        fr = [im.crop(((i % cols) * tw, (i // cols) * th, (i % cols) * tw + tw, (i // cols) * th + th)) for i in range(n)]
        lap = c in ("xr_idle", "xr_walk")
        if lap:
            fr = fr[:-1]
        fr = [f.quantize(96, method=Image.FASTOCTREE) for f in fr]
        d = max(20, int(round(dur / (n - 1) * 1000 / 10.0)) * 10)
        fr[0].save(os.path.join(ra_, c + ".gif"), save_all=True, append_images=fr[1:] + ([] if lap else [fr[-1]] * 6), duration=d, loop=0)
        ev = ", ".join(f"{e} {x:.2f} s" for x, e, _ in SU_KIEN.get(c, []))
        the.append(f'<figure><img src="{c}.gif"><figcaption><b>{c}</b> · {dur:.2f} s' + (f" · sự kiện: {ev}" if ev else "") + "</figcaption></figure>")
    html_ = ("<!doctype html><meta charset=utf-8><title>xuong_rong: clip trên rig gốc</title><style>body{background:#22252b;color:#ddd;"
             "font:14px sans-serif;margin:16px}figure{display:inline-block;margin:6px}img{display:block;border-radius:6px}"
             "figcaption{padding:4px 2px}</style><p>Clip dựng ở tầng điều khiển, chạy trên RIG GỐC (hình của game tham khảo, chỉ xem nội "
             "bộ). Cung bay của đòn thường / chiêu cuối ở đây là giả lập phần code game lo. Appear: đáy khung là mặt đất.</p>" + "".join(the))
    open(os.path.join(ra_, "xem.html"), "w", encoding="utf-8").write(html_)
    print(os.path.join(ra_, "xem.html"))


def main(a):
    sys.stdout.reconfigure(encoding="utf-8")
    lenh = a[0] if a else "dung"
    if lenh == "dung":
        dung()
    elif lenh == "xem":
        dung(xem=True)
        cl = a[1] if len(a) > 1 and a[1] else ",".join(CLIP)
        n = a[2] if len(a) > 2 else "16"
        view = f"&view={a[3]}" if len(a) > 3 and a[3] else "&view=" + VIEW
        tt = (f"&t0={a[4]}" if len(a) > 4 else "") + (f"&t1={a[5]}" if len(a) > 5 else "")
        _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={cl}&extra=xr_extra.json&n={n}&tw=450&th=260&cols=4{view}{tt}")
    elif lenh == "gif":
        gif()
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "xr_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
