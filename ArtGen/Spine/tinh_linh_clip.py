# -*- coding: utf-8 -*-
"""Tinh linh rừng mập: clip RIÊNG theo ý người dùng (2026-11-12), dựng ở TẦNG ĐIỀU KHIỂN của rig gốc monster_3407 rồi để runtime Spine
thật nướng (cách của xuong_rong_clip.py / rong_vay_clip.py; skill pokiclash-spine-rig mục 00 "CLIP MỚI trên rig gốc").

Người dùng:
- idle: giống họ; thi thoảng mắt nhìn loanh quanh; thi thoảng tay đánh bụng, bụng rung rung.
- đánh thường: lao tới dùng tay tát đối thủ.
- chiêu mana: há mồm (mồm gen thêm) bắn ra nhiều lá cây vào người đối thủ.
- chiêu cuối: phình to cơ thể, dùng bụng lao thẳng vào đối thủ, bật nảy lại, bụng rung rung kiểu béo béo cute.
- thêm walk; die giống họ; appear rơi từ trên trời xuống.

Rig gốc điều khiển bằng:
  bone > bone2 > bone3 (THÂN: dời, xoay, co giãn cả bụng + hai tay + mầm cây trong bụng)
  bone3 > bone5 > bone6 > bone7   tay TRƯỚC (bên trái người xem, vẽ trên thân)
  bone3 > bone8 > bone9 > bone10  tay SAU (bên phải, nấp sau thân)
  bone3 > bone11 / bone12         hai góc đáy bụng, IK (có giãn) tới R / L nằm trên đất (con của bone2)
  bone2 > bone43 > bone44 > bone4 ĐẦU (bone4 chỉ thừa hưởng độ dời): bone43 dời, bone44 xoay, bone4 co giãn
  bone4 > bone13 (mắt: dời = liếc), bone14 (gốc tóc) > các chuỗi lá, dây leo
  mắt đổi ảnh trong slot P_SL_bq1: bq1 thường, bq2 xếch giận (mở to), bq3 xếch hẹp, bq4 "> <", bq5 nhắm (nét lượn), bq6 nửa nhắm có mày (gồng)

Kênh riêng cho rig của MÌNH (rig gốc không có, xem thử không thấy): ex["nguoi"] = (dx, dy) con ngươi, ex["mieng"] = 0..1 há mồm.

    tinh_linh_clip.py dung                 ghép, ghi <scan>/lam_clip/tl_extra.json
    tinh_linh_clip.py xem [clip,..] [n] [view] [t0] [t1]   tờ khung trên rig gốc (có cung bay giả) → <scan>/lam_clip/khung/<clip>.jpg
    tinh_linh_clip.py song                 trang xem SỐNG (runtime Spine thật, 60 khung/giây) → <scan>/lam_clip/xem/xem.html
    tinh_linh_clip.py gif                  GIF từng clip (ít khung, nhìn giật: chỉ để gửi nhanh) → <scan>/lam_clip/xem/xem_gif.html
    tinh_linh_clip.py mau                  lấy mẫu 30 khung/giây → <scan>/sample_moi.json (tinh_linh_rig.py đọc)
Chạy qua quai/khoa.py chrome (xem, gif, mau mở Chrome ngầm)."""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MON = "monster_3407"
FPS = 30.0
F = 1.0 / FPS


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
ix = TEN.index
_S = None

TAY_T = ["bone5", "bone6", "bone7"]             # tay trước (bên trái người xem)
TAY_S = ["bone8", "bone9", "bone10"]            # tay sau
DAU = ["bone43", "bone44", "bone4", "bone13", "bone14"]
S_MAT = "P_SL_bq1"                              # slot mắt (đổi ảnh bq1..bq6)
CAO_THAN = 205.0                                # bone3 cách đáy bụng chừng này (đơn vị con gốc)
CAO_DAU = 212.0                                 # đỉnh bụng (chỗ đầu ngồi lên) cách bone3 chừng này


def nhom(ds):
    m = np.zeros(len(TEN), bool)
    for n in ds:
        m[ix(n)] = True
    return m


def con_chau(goc):
    """mọi xương là con cháu của `goc` (kể cả nó)."""
    g = ix(goc)
    r = []
    for i, b in enumerate(I["bones"]):
        p = i
        while p >= 0 and p != g:
            p = I["bones"][p]["parent"]
        if p == g:
            r.append(TEN[i])
    return r


TOC = [n for n in con_chau("bone14") if n != "bone14"]


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y CHƯA áp ràng buộc; k độ trộn IK; mat = ảnh mắt;
    ex = kênh riêng của rig mình (con ngươi, mồm)."""

    def __init__(self, u, k, mat="P_SL_bq1", ex=None):
        self.u, self.k, self.mat = u, k, mat
        self.ex = dict(nguoi=(0.0, 0.0), mieng=0.0) if ex is None else dict(ex)

    def chep(self):
        return Dang(self.u.copy(), self.k.copy(), self.mat, self.ex)

    def tron(self, B, w, mat_na=None):
        ww = np.full(len(TEN), float(w)) if mat_na is None else np.where(mat_na, float(w), 0.0)
        return Dang(self.u + (B.u - self.u) * ww[:, None], self.k + (B.k - self.k) * (float(w) if mat_na is None else 0.0), self.mat, self.ex)

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
        _S = {c: (float(v["dur"]), np.array([f["u"] for f in v["frames"]], float), np.array([[q[0] for q in f["k"]] for f in v["frames"]], float),
                  [f["n"][I_MAT] for f in v["frames"]]) for c, v in S.items()}
    return _S


I_MAT = [s["name"] for s in I["slots"]].index(S_MAT)


def dk(clip, t, lap=False):
    dur, U, Kk, M = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    return Dang(U[i0] * (1 - w) + U[i1] * w, Kk[i0] * (1 - w) + Kk[i1] * w, M[i0] or "P_SL_bq1")


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
    """nội suy theo các mốc (t, giá trị); kieu[i] = hàm làm êm của đoạn i (mặc định em)."""
    if t <= moc[0][0]:
        return moc[0][1]
    for i in range(len(moc) - 1):
        (a, x), (b, y) = moc[i], moc[i + 1]
        if t <= b:
            w = (t - a) / (b - a)
            w = (kieu[i] if kieu and kieu[i] else em)(w)
            return x + (y - x) * w
    return moc[-1][1]


def rung(t, t0, bien, tan=0.28, hz=5.5, pha=0.0):
    """dao động tắt dần bắt đầu ở t0 (bụng mỡ rung): bien · e^(−(t−t0)/tan) · sin."""
    if t < t0:
        return 0.0
    x = t - t0
    return bien * math.exp(-x / tan) * math.sin(2 * math.pi * hz * x + pha)


def than(D, s=1.0, doc=1.0, goc=0.0, dx=0.0, dy=0.0, dau=1.0):
    """CẢ khối (thân bone3 + đầu): phồng đều `s` lần, giãn dọc thêm `doc` lần (ngang co 1/√doc cho giữ thể tích), nghiêng `goc` độ
    quanh điểm tì đất, dời (dx, dy). Đáy bụng giữ trên đất (bone3 nâng theo), đầu nâng theo đỉnh bụng và phồng `dau` lần."""
    i = ix("bone3")
    sx, sy = s / math.sqrt(doc), s * doc
    nang = (sy - 1.0) * CAO_THAN                      # đáy bụng không chui xuống đất
    g = math.radians(goc)
    # nghiêng quanh điểm tì đất (dưới bone3 một đoạn CAO_THAN·sy): bone3 đi theo cung tròn
    r = CAO_THAN * sy
    D.u[i, 0] += dx - r * math.sin(g)
    D.u[i, 1] += dy + nang - r * (1 - math.cos(g))
    D.u[i, 2] += goc
    D.u[i, 3] *= sx
    D.u[i, 4] *= sy
    # đầu: ngồi trên đỉnh bụng (cách bone3 CAO_DAU dọc trục thân)
    rd = CAO_DAU
    hx = dx - r * math.sin(g) - rd * sy * math.sin(g)
    hy = dy + nang - r * (1 - math.cos(g)) + rd * (sy * math.cos(g) - 1.0)
    j = ix("bone43")
    D.u[j, 0] += hx
    D.u[j, 1] += hy
    D.u[ix("bone44"), 2] += goc
    D.co("bone4", dau * (1 + (sx - 1) * 0.5), dau * (1 + (sy - 1) * 0.35))
    return D


def lac_bung(D, v):
    """bụng mỡ lắc: v > 0 phình ngang, xẹp dọc; hai góc đáy bụng xoè ra. v cỡ ±0,08."""
    i = ix("bone3")
    D.u[i, 3] *= 1 + v
    D.u[i, 4] *= 1 - 0.8 * v
    D.u[i, 1] += -0.8 * v * CAO_THAN
    D.doi("bone11", -90 * v, 0)
    D.doi("bone12", 90 * v, 0)
    j = ix("bone43")
    D.u[j, 1] += -0.8 * v * (CAO_THAN + CAO_DAU)
    return D


def tay(D, nguon, w, ds=TAY_T + TAY_S):
    m = nhom(ds)
    D.u[m] += (nguon.u[m] - D.u[m]) * w
    return D


def toc_tre(D, goc):
    """tóc ngả theo quán tính: mọi gốc chuỗi lá / dây xoay thêm `goc` (đốt sau một nửa)."""
    for n in TOC:
        p = TEN[I["bones"][ix(n)]["parent"]]
        D.xoay(n, goc if p == "bone14" else 0.5 * goc)
    return D


# ---------------------------------------------------------------- idle 8 s: vòng một như họ + liếc mắt; vòng hai vỗ bụng hai cái
I_VONG, I_DUR = 4.0, 8.0
I_VO = (5.20, 5.56)             # hai cú vỗ bụng
I_LIEC = [(0.0, (0, 0)), (0.9, (0, 0)), (1.08, (-1, 0.1)), (1.9, (-1, 0.1)), (2.1, (0.2, 0.6)), (2.75, (0.2, 0.6)), (2.95, (1, -0.2)),
          (3.45, (1, -0.2)), (3.7, (0, 0)), (8.0, (0, 0))]


def idle(t):
    """IDLE 8 s lặp = hai vòng idle_01 của họ (4 s). Vòng một: nguyên của họ (thở, tay vẫy nhẹ, mắt trượt) + CON NGƯƠI liếc trái → lên
    → phải → về. Vòng hai: 4,95 s tay trước giơ ra lấy đà, VỖ bụng 5,20 và 5,56 (mắt nhắm cong khoái chí), mỗi cú bụng rung tắt dần
    ~0,7 s, đầu và tóc nảy theo trễ một nhịp; 6,3 s tay về, mở mắt."""
    x = t % I_DUR
    D = dk("idle_01", x % I_VONG, lap=True)
    lx = cong([(a, v[0]) for a, v in I_LIEC], x)
    ly = cong([(a, v[1]) for a, v in I_LIEC], x)
    D.ex["nguoi"] = (lx, ly)
    if x >= I_VONG:
        R = dk("idle_01", x % I_VONG, lap=True)
        w = cung(x, 4.75, 5.0, 6.0, 6.4)                  # tay trước thôi theo nhịp vẫy của họ, làm động tác vỗ
        m = nhom(TAY_T)
        N = nghi()
        D.u[m] += (N.u[m] - D.u[m]) * w
        # góc tay: 0 = thõng; âm = giơ ra ngoài (lấy đà); dương = úp vào bụng
        g = cong([(4.75, 0), (5.02, -34), (I_VO[0], 46), (5.36, -20), (I_VO[1], 50), (5.74, 30), (6.05, 36), (6.4, 0)], x,
                 [None, None, vao, ra, vao, ra, None, None])
        D.xoay("bone5", g)
        D.xoay("bone6", 0.45 * g if g > 0 else 0.3 * g)
        D.xoay("bone7", 0.5 * g if g > 0 else 0.4 * g)
        v = sum(rung(x, tv + 0.01, 0.075, 0.24, 5.2, 0.0) for tv in I_VO)
        lac_bung(D, v)
        vd = sum(rung(x, tv + 0.07, 1.0, 0.26, 5.2, 0.0) for tv in I_VO)        # đầu, tóc nảy trễ
        D.doi("bone43", 0, 5.0 * vd)
        D.xoay("bone44", 1.6 * vd)
        toc_tre(D, 5.0 * vd)
        D.xoay("bone8", -9.0 * v / 0.075)                                      # tay sau bật ra theo nhịp rung
        if 5.08 <= x < 6.25:
            D.mat = "P_SL_bq5"
        del R
    return D


# ---------------------------------------------------------------- attack: LAO VÀO rồi TÁT NGANG từ trái sang phải
A_NHUN, A_TOI, A_TAT, A_GIU, A_VE, A_DUR = 0.16, 0.44, 0.56, 0.70, 1.20, 1.34
A_XA, A_CAO = 420.0, 30.0        # cung lao (đơn vị con gốc): chạy tới trước A_XA rồi mới tát (game co giãn cho đỉnh rơi vào đối thủ)
L_TAY = 210.0                    # chiều dài tay trước duỗi thẳng (bone5 + bone6 + bone7)


def tay_thang(D, goc_tg, dai, w, vai=0.0):
    """tay TRƯỚC duỗi thẳng, chĩa theo góc THẾ GIỚI `goc_tg` (0 = sang phải, −90 = xuống, ±180 = sang trái), dài `dai` lần (tay
    thạch co giãn được: co ngắn = đang chĩa về phía người xem); trộn `w` với dáng tay đang có; `vai` = vai đưa ra trước (đơn vị)."""
    i5, i6, i7 = ix("bone5"), ix("bone6"), ix("bone7")
    g3 = D.u[ix("bone3"), 2]
    D.u[i5, 2] += (goc_tg - g3 - D.u[i5, 2]) * w
    D.u[i6, 2] += (0.0 - D.u[i6, 2]) * w
    D.u[i7, 2] += (0.0 - D.u[i7, 2]) * w
    D.u[i5, 3] *= 1 + (dai - 1) * w
    D.u[i5, 4] *= 1 + (min(1.3, 1 / math.sqrt(max(dai, 0.3))) - 1) * w       # co ngắn thì mập ra, duỗi dài thì thon lại
    D.u[i5, 0] += vai * w
    return D


def attack(t):
    """ĐÒN THƯỜNG 1,34 s (người dùng 2026-11-12: "lao vào tát cơ mà"; "tát chứ không phải hất tay lên, tay tát phải đưa từ trái
    sang"). Thân, đầu, tóc, tay sau theo skill_01 của họ (bớt cú nhảy dựng); TAY TRƯỚC tự dựng, KHÔNG dùng cú vung vòng qua đầu của họ.
    Nhún lấy đà 0 → 0,16; LAO 0,16 → 0,44: người chúi tới 13°, nảy hai nhịp, tay trước duỗi ngang ra SAU (bên trái, hơi chếch lên),
    kéo căng thêm ngay trước khi tát; TÁT 0,44 → 0,56: tay quét NGANG từ trái sang phải ngang tầm ngực, đi qua trước bụng (giữa đường
    tay co ngắn vì đang chĩa về phía người xem), vai đưa ra trước, kết thúc duỗi dài gấp đôi sang phải, đầu tay vượt mép thân; sự kiện trung 0,56; đà tay đi
    tiếp, khựng tới 0,70, bụng rung vì phanh gấp; nhảy lùi về chỗ 0,70 → 1,20, tay thu về qua phía trước; nhún về dáng nghỉ."""
    ts = cong([(0, 0), (A_TOI, 0.50), (A_TAT, 0.633), (A_GIU, 0.70), (A_VE, 1.24), (A_DUR, 1.333)], t, [None, vao, None, None, None])
    D = dk("skill_01", ts)
    N = nghi()
    i3 = ix("bone3")
    D.u[i3, 1] = N.u[i3, 1] + (D.u[i3, 1] - N.u[i3, 1]) * 0.45              # bớt cú nhảy dựng của họ: đây là tát ngang, không bổ xuống
    j = ix("bone43")
    D.u[j, 1] = N.u[j, 1] + (D.u[j, 1] - N.u[j, 1]) * 0.45
    m = nhom(TAY_T)
    D.u[m] = N.u[m]                                                         # bỏ cú vung tay qua đầu của họ
    lao = cung(t, A_NHUN - 0.04, A_NHUN + 0.08, A_TOI - 0.04, A_TOI + 0.04)
    nhun = cung(t, 0.0, A_NHUN - 0.05, A_NHUN, A_NHUN + 0.08)
    buoc = abs(math.sin(math.pi * (t - A_NHUN) / 0.14)) if A_NHUN < t < A_TOI else 0.0
    than(D, doc=1.0 - 0.10 * nhun + 0.05 * lao * buoc, goc=5.0 * nhun - 13.0 * lao, dy=14.0 * lao * buoc)
    ve = cung(t, A_GIU, A_GIU + 0.12, A_VE - 0.14, A_VE)                      # đang nhảy lùi: ngả nhẹ ra sau, đáp thì bẹp
    than(D, doc=1.0 + 0.05 * ve - 0.08 * cung(t, A_VE - 0.05, A_VE + 0.02, A_VE + 0.04, A_VE + 0.14), goc=4.0 * ve)
    # tay trước: góc thế giới và độ dài theo thời gian. Dáng nghỉ ~ −120°. Lấy đà = −190° (sang trái, chếch lên). Tát: −190° → −12° (chếch xuống: tay nằm ngang NGỰC, không vắt qua mặt) đi
    # qua −90° (trước bụng) với độ dài 1,15 → 0,42 → 1,62: đầu tay đi gần như NGANG từ trái sang phải
    g = cong([(0, -120), (A_NHUN, -128), (A_TOI - 0.08, -184), (A_TOI, -194), (A_TAT, -12), (A_TAT + 0.05, -5), (A_GIU, -10), (A_VE - 0.1, -112),
              (A_DUR, -120)], t, [None, None, None, vao, ra, None, None, None])
    # độ dài: mốc theo thời gian (đơn giản, trơn): căng 1,2 lúc lấy đà; 0,42 giữa cú quét; 1,62 lúc trúng; chùng 1,45; về 1
    t_giua = A_TOI + 0.55 * (A_TAT - A_TOI)
    dai = cong([(0, 0.96), (A_NHUN, 0.96), (A_TOI - 0.08, 1.10), (A_TOI, 1.22), (t_giua, 0.42), (A_TAT, 2.0), (A_TAT + 0.05, 1.82), (A_GIU, 1.70),
                (A_VE - 0.1, 0.96), (A_DUR, 0.96)], t, [None, None, None, vao, ra, None, None, None, None])
    # ép đầu tay đi trên MỘT ĐƯỜNG NGANG thấp hơn vai 84 đơn vị (ngang ngực) suốt cú quét và lúc thu tay về: độ dài <= 0,40 / |sin góc|
    q = cung(t, A_TOI - 0.02, A_TOI + 0.02, A_GIU + 0.1, A_VE - 0.16)
    tran = 0.40 / max(0.05, abs(math.sin(math.radians(g))))
    dai += (min(dai, tran) - dai) * q
    w = cung(t, 0.02, A_NHUN + 0.06, A_VE - 0.12, A_VE + 0.06)
    vai = cong([(0, 0), (A_TOI, -14), (A_TAT, 85), (A_GIU, 70), (A_VE, 0)], t, [None, vao, None, None])
    tay_thang(D, g, dai, w, vai)
    if 0.08 <= t < A_VE - 0.2:
        D.mat = "P_SL_bq3"
    lac_bung(D, rung(t, A_TAT + 0.02, 0.07, 0.2, 5.5) + rung(t, A_VE + 0.02, 0.05, 0.18, 5.5))
    toc_tre(D, 20.0 * lao - 22.0 * cung(t, A_TOI, A_TAT, A_TAT + 0.03, A_GIU + 0.2) + 10.0 * ve)
    return D


def attack_bay(t):
    """cung lao của đòn thường (xương move): chạy tới trước, tới nơi rồi mới tát (đỉnh giữ suốt cú tát), nhảy lùi về."""
    if t <= A_NHUN:
        return -18.0 * em(t / A_NHUN), 0.0
    if t <= A_TOI:
        u = (t - A_NHUN) / (A_TOI - A_NHUN)
        return -18.0 + (A_XA * 0.94 + 18.0) * em(u), 0.0
    if t <= A_TAT:
        return A_XA * (0.94 + 0.06 * (t - A_TOI) / (A_TAT - A_TOI)), 0.0
    if t <= A_GIU:
        return A_XA, 0.0
    u = min(1.0, (t - A_GIU) / (A_VE - A_GIU))
    return A_XA * (1 - em(u)), A_CAO * 3.0 * 4 * u * (1 - u)


# ---------------------------------------------------------------- cast: hít căng, há mồm phun lá
C_HIT, C_PHUN, C_HET, C_DUR = 0.46, 0.56, 1.50, 2.0


def cast(t):
    """CHIÊU MANA 2,0 s, đứng tại chỗ. Hít 0 → 0,46: phồng dần hai nấc (1,06 rồi 1,14), ngả ra sau 9°, hai tay giơ lên, mắt lim dim;
    0,46 → 0,56 gập người tới 11°, HÁ MỒM (ex mieng), mắt trợn; sự kiện phun 0,56; giữ há 0,56 → 1,50: người rung nhẹ, giật lùi từng
    nhịp 0,13 s theo từng loạt lá, xẹp dần về cỡ thường; sự kiện het_phun 1,50; ngậm mồm, thở phào, bụng rung, về dáng nghỉ."""
    D = nghi()
    giu = cung(t, C_HIT, C_PHUN, C_HET, C_HET + 0.14)
    s = cong([(0, 1), (0.16, 1.06), (0.24, 1.04), (C_HIT - 0.04, 1.15), (C_PHUN, 1.10), (C_HET, 1.0), (C_DUR, 1.0)], t)
    doc = cong([(0, 1), (C_HIT - 0.04, 1.07), (C_PHUN, 0.93), (C_PHUN + 0.12, 0.97), (C_HET, 0.99), (C_HET + 0.12, 1.04), (C_DUR - 0.2, 1)], t)
    g = cong([(0, 0), (C_HIT - 0.04, 9), (C_PHUN, -11), (C_HET, -8), (C_HET + 0.2, 3), (C_DUR, 0)], t, [None, vao, None, None, None])
    nhip = math.sin(2 * math.pi * (t - C_PHUN) / 0.13) if t > C_PHUN else 0.0          # nhân với giu: tắt dần, không cắt cụt
    than(D, s=s, doc=doc, goc=g + 1.3 * nhip * giu, dx=-5.0 * max(0.0, nhip) * giu + 14 * cung(t, C_HIT, C_PHUN, C_HET, C_HET + 0.2),
         dau=1 + 0.05 * giu)
    D.xoay("bone44", cong([(0, 0), (C_HIT - 0.04, 10), (C_PHUN, -7), (C_HET, -5), (C_HET + 0.2, 0)], t))       # đầu ngửa hít, cúi phun
    gio = dk("skill_03", 0.33)                               # dáng hai tay giơ cao của họ
    tay(D, gio, 0.75 * cung(t, 0.04, C_HIT - 0.06, C_HIT, C_PHUN) + 0.42 * giu)
    D.xoay("bone5", -10 * nhip * giu)
    D.xoay("bone8", 10 * nhip * giu)
    toc_tre(D, cong([(0, 0), (C_HIT - 0.04, -8), (C_PHUN, 18), (C_PHUN + 0.2, 10), (C_HET, 8), (C_HET + 0.25, -3), (C_DUR, 0)], t) + 3 * nhip * giu)
    lac_bung(D, rung(t, C_HET + 0.12, 0.05, 0.22, 5.0))
    D.ex["mieng"] = cung(t, C_HIT + 0.03, C_PHUN - 0.02, C_HET + 0.02, C_HET + 0.12)
    D.mat = ("P_SL_bq1" if t < 0.10 else "P_SL_bq6" if t < C_HIT else "P_SL_bq2" if t < C_HET + 0.1 else "P_SL_bq5" if t < C_HET + 0.34
             else "P_SL_bq1")
    return D


# ---------------------------------------------------------------- skill: BỤNG phình béo, lấy bụng húc, bật về nảy tưng tưng
S_PHINH, S_LAO, S_HUC, S_NAY, S_DAP, S_DAP2, S_DAP3, S_DUR = 0.60, 0.74, 0.90, 0.98, 1.46, 1.80, 2.02, 2.70
S_TO = 1.40                      # bụng to chừng này lần lúc phình
S_BEO = 0.86                     # lúc phình bụng bè NGANG hơn là cao (giãn dọc × S_BEO): ngang ~1,5 lần, cao ~1,2 lần
S_XA, S_CAO = 200.0, 96.0        # cung lao: húc tới trước S_XA; lúc bật về nảy cao S_CAO
S_NAY2, S_NAY3 = 48.0, 20.0      # về tới chỗ còn nảy thêm hai cái, cao chừng này
S_BOM = (0.10, 0.28, 0.46)       # ba nấc bơm


def skill(t):
    """CHIÊU CUỐI 2,7 s (người dùng 2026-11-12: "phình phần bụng ra cho béo là chủ yếu, tăng sự nảy nảy của bụng lên cho cute").
    PHÌNH 0 → 0,60: ba nấc bơm, mỗi nấc bụng vọt quá rồi lún lại và rung; chỉ BỤNG to ra (ngang 1,5 lần, cao 1,2 lần), đầu gần như
    giữ cỡ, hai tay giữ cỡ và bị bụng đẩy xoè ngang; mắt giận. 0,60 → 0,74 ngả ra sau lấy đà, bụng lắc lư. LAO 0,74 → 0,90 ưỡn bụng
    đi đầu. HÚC 0,90 (sự kiện trung): bụng ép bẹp ngang vào đối thủ, khựng tới 0,98, rung. BẬT VỀ 0,98 → 1,46 theo cung cao, bụng vẫn
    béo và lắc trong lúc bay, mắt "> <", tay chới với. Về tới chỗ NẢY TƯNG TƯNG ba lần như quả bóng nước: đáp 1,46 (sự kiện dap, bẹp
    dí), nảy cao 48, đáp 1,80, nảy 20, đáp 2,02; mỗi lần đáp bụng rung mạnh rồi tắt dần, hai tay vỗ theo, mắt nhắm khoái chí. Từ 2,07
    xì hơi về cỡ thường, bụng còn rung dư; về dáng nghỉ."""
    D = nghi()
    N = nghi()
    s_ = cong([(0, 1), (0.10, 1.17), (0.17, 1.10), (0.28, 1.30), (0.35, 1.22), (0.46, S_TO + 0.07), (0.53, S_TO - 0.03), (S_PHINH, S_TO),
               (S_DAP3 + 0.05, S_TO), (S_DAP3 + 0.20, 1.12), (S_DAP3 + 0.30, 1.16), (S_DAP3 + 0.46, 1.0)], t)
    pp = min(1.0, max(0.0, (s_ - 1.0) / (S_TO - 1.0)))                       # 0..1: đang phình tới đâu
    nhip = cong([(0, 1), (S_PHINH, 1), (S_LAO, 0.94), (S_HUC - 0.03, 1.04), (S_HUC + 0.02, 1.26), (S_NAY, 1.18), (S_NAY + 0.12, 0.95),
                 (S_DAP - 0.05, 1.10), (S_DAP + 0.05, 0.70), (S_DAP + 0.17, 1.14), (S_DAP2 - 0.04, 1.07), (S_DAP2 + 0.04, 0.80),
                 (S_DAP2 + 0.13, 1.08), (S_DAP3 - 0.03, 1.03), (S_DAP3 + 0.04, 0.88), (S_DAP3 + 0.14, 1.04), (S_DAP3 + 0.30, 1.0)], t)
    g = cong([(0, 0), (S_PHINH, 0), (S_LAO, 13), (S_HUC - 0.02, 15), (S_HUC + 0.02, 4), (S_NAY, 3), (S_NAY + 0.2, -16), (S_DAP - 0.04, -6),
              (S_DAP + 0.08, 4), (S_DAP2, -2), (S_DAP2 + 0.1, 2), (S_DAP3 + 0.1, 0)], t)
    than(D, s=s_, doc=(1.0 - (1.0 - S_BEO) * pp) * nhip, goc=g)
    # đầu gần như giữ cỡ (chỉ to 8%), hai tay giữ cỡ: chỉ bụng béo ra
    i4, i3 = ix("bone4"), ix("bone3")
    D.u[i4, 3], D.u[i4, 4] = N.u[i4, 3] * (1 + 0.08 * pp), N.u[i4, 4] * (1 + 0.08 * pp)
    xoe = dk("skill_02", 0.62)                               # dáng hai tay xoè ngang của họ
    gio = dk("skill_03", 0.33)
    tay(D, xoe, cong([(0, 0), (0.30, 0.55), (S_PHINH, 0.95), (S_HUC, 1.0), (S_DAP, 0.62), (S_DAP3, 0.5), (S_DAP3 + 0.45, 0)], t))
    choi = cung(t, S_NAY, S_NAY + 0.1, S_DAP - 0.1, S_DAP + 0.05)           # đang bay về: tay chới với
    tay(D, gio, 0.5 * choi)
    D.xoay("bone5", 18 * choi * math.sin(2 * math.pi * 4.0 * (t - S_NAY)))
    D.xoay("bone8", -18 * choi * math.sin(2 * math.pi * 4.0 * (t - S_NAY) + 1.0))
    # BỤNG NẢY: mỗi nấc bơm một nhịp rung; lúc gồng giữ và lúc bay lắc đều; húc và ba lần đáp rung mạnh tắt dần
    v = sum(rung(t, a + 0.02, 0.07, 0.13, 6.0) for a in S_BOM)
    v += 0.035 * cung(t, S_PHINH - 0.05, S_PHINH + 0.03, S_LAO, S_LAO + 0.06) * math.sin(2 * math.pi * 5.0 * t)
    v += rung(t, S_HUC + 0.01, 0.10, 0.16, 6.0)
    v += 0.05 * cung(t, S_NAY + 0.08, S_NAY + 0.18, S_DAP - 0.12, S_DAP - 0.02) * math.sin(2 * math.pi * 4.4 * (t - S_NAY))
    dap = rung(t, S_DAP + 0.04, 0.17, 0.26, 4.6) + rung(t, S_DAP2 + 0.03, 0.12, 0.24, 4.8) + rung(t, S_DAP3 + 0.03, 0.09, 0.30, 5.0)
    v = max(-0.2, min(0.2, v + dap))
    lac_bung(D, v)
    kx, ky = D.u[i3, 3] / N.u[i3, 3], D.u[i3, 4] / N.u[i3, 4]             # hai tay giữ cỡ (tính sau cả nhịp rung của bụng)
    for n in ("bone5", "bone8"):
        D.co(n, kx ** -0.85, ky ** -0.85)
    vd = rung(t, S_DAP + 0.10, 1.0, 0.26, 4.6) + 0.7 * rung(t, S_DAP2 + 0.09, 1.0, 0.24, 4.8) + 0.5 * rung(t, S_DAP3 + 0.09, 1.0, 0.30, 5.0)
    D.doi("bone43", 0, 8.0 * vd)                                           # đầu nảy trễ sau bụng một nhịp
    D.xoay("bone44", 2.4 * vd + cong([(S_HUC - 0.02, 0), (S_HUC + 0.03, -14), (S_NAY, -10), (S_NAY + 0.2, 8), (S_DAP, 0)], t))
    D.xoay("bone5", 60.0 * dap)                                            # hai tay vỗ theo nhịp bụng lúc đáp
    D.xoay("bone8", -60.0 * dap)
    toc_tre(D, cong([(0, 0), (S_PHINH, 0), (S_LAO, -6), (S_HUC - 0.03, -22), (S_HUC + 0.04, 26), (S_NAY + 0.1, 14), (S_DAP - 0.05, -12),
                     (S_DAP + 0.06, 16), (S_DAP2 - 0.04, -8), (S_DAP2 + 0.05, 12), (S_DAP3 + 0.05, 8), (S_DAP3 + 0.3, 0)], t) + 6.0 * vd)
    D.mat = ("P_SL_bq1" if t < 0.05 else "P_SL_bq2" if t < S_HUC else "P_SL_bq4" if t < S_DAP + 0.12 else "P_SL_bq5" if t < S_DUR - 0.32
             else "P_SL_bq1")
    return D


def skill_bay(t):
    if t <= S_PHINH:
        return 0.0, 0.0
    if t <= S_LAO:
        return -22.0 * em((t - S_PHINH) / (S_LAO - S_PHINH)), 0.0
    if t <= S_HUC:
        u = vao((t - S_LAO) / (S_HUC - S_LAO), 1.6)
        return -22.0 + (S_XA + 22.0) * u, 10.0 * math.sin(math.pi * u)
    if t <= S_NAY:
        return S_XA, 0.0
    if t <= S_DAP:
        u = (t - S_NAY) / (S_DAP - S_NAY)
        return S_XA * (1 - ra(u, 1.5)), S_CAO * 4 * u * (1 - u)
    for t0, t1, cao in ((S_DAP + 0.07, S_DAP2, S_NAY2), (S_DAP2 + 0.05, S_DAP3, S_NAY3)):
        if t0 < t < t1:
            u = (t - t0) / (t1 - t0)
            return 0.0, cao * 4 * u * (1 - u)
    return 0.0, 0.0


# ---------------------------------------------------------------- appear: rơi từ trên trời xuống
P_ROI, P_NAY, P_DAP2, P_DUR = 0.40, 0.76, 0.98, 1.80
P_CAO = 640.0                    # rơi từ cao chừng này (đơn vị con gốc; cả con cao ~740). Rig mình hiện dần 0,2 s đầu


def appear(t):
    """APPEAR 1,8 s. Rơi 0 → 0,40 từ trên trời (cung dời ở appear_bay): thân giãn dọc 1,16, hai tay bị gió thốc lên, tóc dựng ngược,
    mắt "> <"; CHẠM ĐẤT 0,40 (sự kiện cham_dat): bẹp dí còn 0,58 chiều cao, bè ngang; nảy lên 0,50 → 0,76 (cao 70, giãn dọc), tay
    xoè giữ thăng bằng; đáp lần hai 0,98 bẹp nhẹ, bụng rung tắt dần; 1,15 mở mắt, lắc người một cái, liếc hai bên; về dáng nghỉ."""
    D = nghi()
    doc = cong([(0, 1.16), (P_ROI - 0.03, 1.2), (P_ROI + 0.05, 0.58), (P_ROI + 0.12, 0.66), (0.62, 1.14), (P_NAY, 1.04), (P_DAP2 - 0.04, 1.08),
                (P_DAP2 + 0.05, 0.84), (P_DAP2 + 0.2, 1.05), (P_DAP2 + 0.36, 1.0)], t)
    g = cong([(0, -5), (P_ROI, -2), (P_ROI + 0.08, 0), (0.62, 4), (P_DAP2, -2), (P_DAP2 + 0.25, 0)], t)
    than(D, doc=doc, goc=g)
    gio = dk("skill_03", 0.33)
    xoe = dk("skill_02", 0.62)
    tay(D, gio, cong([(0, 1.0), (P_ROI, 1.0), (P_ROI + 0.08, 0.0)], t))
    tay(D, xoe, cong([(0, 0), (P_ROI, 0), (P_ROI + 0.07, 1.0), (0.62, 0.55), (P_DAP2, 0.75), (P_DAP2 + 0.4, 0)], t))
    v = rung(t, P_ROI + 0.05, 0.10, 0.2, 5.0) * (1 if t < P_NAY else 0) + rung(t, P_DAP2 + 0.04, 0.085, 0.3, 4.8)
    lac_bung(D, v)
    vd = rung(t, P_DAP2 + 0.10, 1.0, 0.3, 4.8)
    D.doi("bone43", 0, 6.0 * vd)
    lac = rung(t, 1.2, 5.0, 0.22, 3.6)                       # lắc người rũ bụi
    D.xoay("bone44", 1.8 * vd + lac)
    D.xoay("bone3", 0.5 * lac)
    toc_tre(D, cong([(0, -30), (P_ROI - 0.02, -34), (P_ROI + 0.07, 30), (P_ROI + 0.2, 8), (0.62, -14), (P_NAY, 0), (P_DAP2 - 0.03, -16),
                     (P_DAP2 + 0.07, 18), (P_DAP2 + 0.3, 0)], t) + 5.0 * vd + 2.0 * lac)
    D.mat = "P_SL_bq4" if t < P_DAP2 + 0.14 else ("P_SL_bq5" if t < 1.2 else "P_SL_bq1")
    D.ex["nguoi"] = (cong([(1.2, 0), (1.3, -1), (1.45, -1), (1.55, 1), (1.66, 1), (1.76, 0)], t), 0.0)
    return D


def appear_bay(t):
    if t < P_ROI:
        return 0.0, P_CAO * (1 - (t / P_ROI) ** 1.8)
    if P_ROI + 0.10 < t < P_DAP2:
        u = (t - P_ROI - 0.10) / (P_DAP2 - P_ROI - 0.10)
        return 0.0, 70.0 * 4 * u * (1 - u)
    return 0.0, 0.0


# ---------------------------------------------------------------- walk: NHÚN xuống rồi BẬT lên, mỗi vòng một cú nhảy
W_DUR = 0.9
W_NHUN, W_BAT, W_DINH, W_DAP = 0.24, 0.32, 0.49, 0.68
W_CAO = 92.0                     # nhảy cao chừng này (đơn vị con gốc; cả con cao ~740)


def walk(t):
    """WALK 0,9 s lặp (người dùng 2026-11-12: "walk làm thành nhún xuống bật lên đi"): mỗi vòng MỘT cú nhảy tại chỗ (game lo dời
    ngang). Nhún 0,10 → 0,24: bẹp còn 0,78 chiều cao, bụng bè ra, hai tay bị đẩy xoè; BẬT 0,24 → 0,32: giãn dọc 1,18, rời đất; trên
    không tới 0,66 (đỉnh 0,49, cao 92): hai tay hất lên, tóc trễ xuống rồi dựng lên lúc rơi; ĐÁP 0,68: bẹp 0,76, bụng nảy lại 1,06 rồi
    lún vào cú nhún của vòng sau (khung 0 = khung cuối)."""
    x = t % W_DUR
    D = nghi()
    doc = cong([(0, 0.94), (0.10, 1.0), (W_NHUN, 0.78), (W_BAT + 0.01, 1.18), (W_DINH, 1.04), (W_DAP - 0.06, 1.14), (W_DAP + 0.02, 0.76),
                (0.80, 1.06), (W_DUR, 0.94)], x, [None, None, vao, None, None, vao, ra, None])
    u = (x - W_BAT + 0.02) / (W_DAP - W_BAT)
    cao = W_CAO * 4 * u * (1 - u) if 0.0 < u < 1.0 else 0.0
    g = cong([(0, 0), (W_NHUN, 3), (W_BAT + 0.02, -5), (W_DINH, -2), (W_DAP, 2), (0.80, 0), (W_DUR, 0)], x)
    than(D, doc=doc, goc=g)
    D.doi("bone2", 0.0, cao)                                 # nhấc cả con (đáy bụng, hai mục tiêu IK, đầu) khỏi mặt đất
    tg = cong([(0, 6), (0.10, 0), (W_NHUN, 12), (W_BAT + 0.03, -30), (W_DINH, -44), (W_DAP - 0.04, -52), (W_DAP + 0.04, 14), (0.80, 2),
               (W_DUR, 6)], x)                               # âm = tay hất ra ngoài, lên trên
    D.xoay("bone5", tg)
    D.xoay("bone6", 0.45 * tg)
    D.xoay("bone7", 0.35 * tg)
    D.xoay("bone8", -0.9 * tg)
    D.xoay("bone9", -0.4 * tg)
    D.xoay("bone10", -0.3 * tg)
    toc_tre(D, cong([(0, 8), (0.10, 0), (W_NHUN, -8), (W_BAT + 0.04, 16), (W_DINH, 0), (W_DAP - 0.04, -22), (W_DAP + 0.05, 22), (0.80, -4),
                     (W_DUR, 8)], x))
    D.xoay("bone44", cong([(0, -2), (0.10, 0), (W_NHUN, 4), (W_BAT + 0.03, -5), (W_DINH, 0), (W_DAP - 0.03, 4), (W_DAP + 0.04, -6),
                           (0.80, 1), (W_DUR, -2)], x))
    lac_bung(D, cong([(0, -0.03), (0.10, 0), (W_NHUN, 0.03), (W_BAT + 0.02, -0.03), (W_DINH, 0), (W_DAP, 0), (W_DAP + 0.04, 0.05),
                      (0.80, -0.035), (W_DUR, -0.03)], x))
    return D


def hit(t):
    return dk("hit_01", t)


def die(t):
    return dk("die_01", t)


CLIP = {"tl_idle": (I_DUR, idle), "tl_walk": (W_DUR, walk), "tl_attack": (A_DUR, attack), "tl_cast": (C_DUR, cast), "tl_skill": (S_DUR, skill),
        "tl_appear": (P_DUR, appear), "tl_hit": (nap()["hit_01"][0], hit), "tl_die": (nap()["die_01"][0], die)}
LAP = ("tl_idle", "tl_walk")
BAY = {"tl_attack": attack_bay, "tl_skill": skill_bay, "tl_appear": appear_bay}        # cung dời của xương move (đơn vị con gốc)
SU_KIEN = {"tl_idle": [(I_VO[0], "vo_bung", ""), (I_VO[1], "vo_bung", "")], "tl_walk": [], "tl_hit": [], "tl_die": [],
           "tl_attack": [(A_TAT, "trung", "")], "tl_cast": [(C_PHUN, "phun", ""), (C_HET, "het_phun", "")],
           "tl_skill": [(S_PHINH, "phinh", ""), (S_HUC, "trung", ""), (S_DAP, "dap", ""), (S_DAP2, "dap", ""), (S_DAP3, "dap", "")], "tl_appear": [(P_ROI, "cham_dat", ""), (P_DAP2, "dap", "")]}


def dung(xem=False):
    out = []
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        Ds = [fn(t) for t in ts]
        U = np.array([d.u for d in Ds])
        if xem and ten in BAY:
            for j, t in enumerate(ts):
                U[j, ix("bone"), :2] += BAY[ten](t)
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
        ks = []
        for t, d in zip(ts, Ds):
            if not ks or ks[-1][1] != d.mat:
                ks.append([round(t, 4), d.mat])
        slots = {S_MAT: {"attachment": ks}}
        out.append({"name": ten, "dur": dur, "bones": bones, "iks": iks, "slots": slots})
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, mắt {[k[1][-3:] for k in ks]}")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "tl_extra.json"), "w", encoding="utf-8"))
    # kênh riêng của rig mình (con ngươi, mồm) + cung bay: rig của mình đọc
    rieng = {}
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        rieng[ten] = {"dur": dur, "nguoi": [list(fn(t).ex["nguoi"]) for t in ts], "mieng": [float(fn(t).ex["mieng"]) for t in ts],
                      "bay": [list(BAY[ten](t)) if ten in BAY else [0.0, 0.0] for t in ts], "su_kien": SU_KIEN.get(ten, []), "lap": ten in LAP}
    json.dump(rieng, open(os.path.join(SCAN, "kenh_rieng.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "tl_extra.json"))


def _chay(*a):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "chay.py"), *a], capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace")[-900:])
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)


VIEW = "40,400,1500,1060"
VIEW_RIENG = {"tl_appear": "0,640,1500,1500", "tl_attack": "230,400,1900,1060", "tl_skill": "120,430,1700,1140"}


def gif(n=46):
    """GIF từng clip trên RIG GỐC (hình của game tham khảo: chỉ để xem nội bộ) + trang xem → <scan>/lam_clip/xem/."""
    from PIL import Image
    dung(xem=True)
    ra_ = os.path.join(LAM, "xem")
    os.makedirs(ra_, exist_ok=True)
    cols = 8
    the = []
    for c in CLIP:
        dur = CLIP[c][0]
        view = VIEW_RIENG.get(c, VIEW)
        vw, vh = [float(x) for x in view.split(",")[2:]]
        tw = 460
        th = int(round(tw * vh / vw))
        nn = 96 if c == "tl_idle" else n
        _chay("sheet", LAM, MON, os.path.join(LAM, "khung_gif"), f"anims={c}&extra=tl_extra.json&n={nn}&tw={tw}&th={th}&cols={cols}&view={view}")
        im = Image.open(os.path.join(LAM, "khung_gif", c + ".jpg")).convert("RGB")
        fr = [im.crop(((i % cols) * tw, (i // cols) * th, (i % cols) * tw + tw, (i // cols) * th + th)) for i in range(nn)]
        lap = c in LAP
        if lap:
            fr = fr[:-1]
        fr = [f.quantize(96, method=Image.FASTOCTREE) for f in fr]
        d = max(20, int(round(dur / (nn - 1) * 1000 / 10.0)) * 10)
        fr[0].save(os.path.join(ra_, c + ".gif"), save_all=True, append_images=fr[1:] + ([] if lap else [fr[-1]] * 6), duration=d, loop=0)
        ev = ", ".join(f"{e} {x:.2f} s" for x, e, _ in SU_KIEN.get(c, []))
        the.append(f'<figure><img src="{c}.gif"><figcaption><b>{c}</b> · {dur:.2f} s' + (f" · sự kiện: {ev}" if ev else "") + "</figcaption></figure>")
    html_ = ("<!doctype html><meta charset=utf-8><title>tinh_linh: clip trên rig gốc</title><style>body{background:#22252b;color:#ddd;"
             "font:14px sans-serif;margin:16px}figure{display:inline-block;margin:6px;vertical-align:top}img{display:block;border-radius:6px}"
             "figcaption{padding:4px 2px}</style><p>Clip dựng ở tầng điều khiển, chạy trên RIG GỐC (hình của game tham khảo, chỉ xem nội "
             "bộ). Cung lao của đòn thường / chiêu cuối / appear ở đây là giả lập phần code game lo. Con ngươi liếc và mồm há là kênh "
             "riêng của rig mình: ở đây chưa thấy.</p>" + "".join(the))
    open(os.path.join(ra_, "xem_gif.html"), "w", encoding="utf-8").write(html_)
    print(os.path.join(ra_, "xem_gif.html"))


TRANG = r"""<!doctype html><html><head><meta charset="utf-8"><title>tinh_linh: clip trên rig gốc</title>
<style>body{background:#22252b;color:#ddd;font:14px sans-serif;margin:14px}button{background:#333842;color:#ddd;border:1px solid #555;
border-radius:6px;padding:6px 12px;margin:3px;font:14px sans-serif;cursor:pointer}button.on{background:#e8a33c;color:#111;border-color:#e8a33c}
canvas{display:block;margin-top:10px;border-radius:8px;background:#6b7079}#st{color:#9ab}#mo{margin:6px 2px;max-width:1000px;line-height:1.45}
</style></head><body>
<div><b>tinh_linh</b>: clip dựng ở tầng điều khiển, chạy bằng runtime Spine thật trên RIG GỐC (hình của game tham khảo, chỉ xem nội bộ).
Cung lao / rơi là giả lập phần code game lo. Mồm há là kênh riêng của rig mình: ở đây chưa thấy. <span id="st">đang nạp</span></div>
<div id="nut"></div><div>tốc độ: <span id="td"></span> &nbsp; <label><input type="checkbox" id="lap" checked> phát lại liên tục</label></div>
<div id="mo"></div><canvas id="cv" width="1100" height="700"></canvas>
<script src="__LIB__"></script>
<script>
const NAME="__MON__", SKEL="__SKEL__", ATLAS=__ATLAS__, PNG="__PNG__", EXTRA=__EXTRA__, INFO=__INFO__;
__ADDEXTRA__
function b64(s){const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u;}
const st=document.getElementById("st"), cv=document.getElementById("cv");
let cur=null, t=0, speed=1, last=0, hold=0;
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
  for(const c of Object.keys(INFO)){const b=document.createElement("button");b.textContent=c.replace("tl_","");b.dataset.clip=c;b.onclick=()=>chon(c);nut.appendChild(b);}
  const td=document.getElementById("td");
  for(const v of [1,0.5,0.25]){const b=document.createElement("button");b.textContent=v+"×";b.onclick=()=>{speed=v;[...td.children].forEach(x=>x.classList.toggle("on",x===b));};td.appendChild(b);if(v===1)b.classList.add("on");}
  chon(Object.keys(INFO)[0]);
  st.textContent="sẵn sàng";
  function ve(now){
    const dt=Math.min(0.05,(now-last)/1000||0);last=now;
    const i=INFO[cur], a=sd.findAnimation(cur);
    if(i.lap){t=(t+dt*speed)%i.dur;}
    else if(t<i.dur){t=Math.min(i.dur,t+dt*speed);}
    else{hold+=dt;if(hold>0.7&&document.getElementById("lap").checked){t=0;hold=0;}}
    sk.setToSetupPose();
    a.apply(sk,t,t,false,[],1,spine.MixBlend.setup,spine.MixDirection.mixIn);
    sk.updateWorldTransform(spine.Physics.update);
    const [vx,vy,vw,vh]=i.view;
    ctx.gl.clearColor(0.42,0.44,0.48,1);ctx.gl.clear(ctx.gl.COLOR_BUFFER_BIT);
    renderer.camera.position.x=vx;renderer.camera.position.y=vy;renderer.camera.zoom=Math.max(vw/cv.width,vh/cv.height);
    ctx.gl.viewport(0,0,cv.width,cv.height);renderer.camera.setViewport(cv.width,cv.height);renderer.camera.update();
    renderer.begin();renderer.drawSkeleton(sk,false);renderer.end();
    requestAnimationFrame(ve);
  }
  requestAnimationFrame(ve);
}
main().catch(e=>{st.textContent="LOI "+e+" "+(e.stack||"");});
</script></body></html>"""

MO_TA = {"tl_idle": "vòng một như họ (mắt liếc); vòng hai tay vỗ bụng 5,20 và 5,56 s, bụng rung", "tl_walk": "mỗi vòng một cú nhảy tại chỗ: nhún bẹp xuống, bật lên, hai tay hất lên, đáp bẹp, bụng nảy (game lo dời ngang)",
         "tl_attack": "nhún, LAO tới (chúi người, tay duỗi ngang ra sau), tới nơi TÁT NGANG từ trái sang phải qua trước bụng, khựng, nhảy lùi về",
         "tl_cast": "hít phồng hai nấc, gập tới há mồm phun lá (mồm chưa có trên rig gốc), giữ rung giật, thở phào",
         "tl_skill": "bơm ba nấc cho BỤNG béo ra (đầu, tay giữ cỡ), ngả lấy đà, ưỡn bụng lao húc, bẹp, bật về theo cung cao, về chỗ nảy tưng tưng ba lần, bụng rung, xì hơi",
         "tl_appear": "rơi từ trên trời, bẹp dí, nảy, đáp lần hai, rung, mở mắt lắc người", "tl_hit": "nguyên hit_01 của họ",
         "tl_die": "nguyên die_01 của họ"}


def song():
    """trang xem SỐNG (runtime Spine thật, 60 khung/giây, mở bằng file://) trên rig gốc → <scan>/lam_clip/xem/xem.html.
    GIF ít khung nhìn giật (người dùng 2026-11-12: "sao nhìn animation demo giật thế")."""
    import base64
    dung(xem=True)
    extra = open(os.path.join(LAM, "tl_extra.json"), encoding="utf-8").read()
    dung()
    mo_xe = open(os.path.join(HERE, "mo_xe", "mo_xe.html"), encoding="utf-8").read()
    a = mo_xe.index("function addExtra(data, list) {")
    b = mo_xe.index("// lấy mẫu 30 khung/giây")
    b64 = lambda f: base64.b64encode(open(os.path.join(RIG, f), "rb").read()).decode()
    info = {c: {"dur": CLIP[c][0], "lap": c in LAP, "view": [float(x) for x in VIEW_RIENG.get(c, VIEW).split(",")], "mo": MO_TA.get(c, ""),
                "ev": ", ".join(f"{e} {x:.2f} s" for x, e, _ in SU_KIEN.get(c, []))} for c in CLIP}
    lib = "file:///" + os.path.join(HERE, "lib", "spine-player.js").replace(os.sep, "/")
    h = (TRANG.replace("__LIB__", lib).replace("__MON__", MON).replace("__SKEL__", b64(MON + ".skel"))
         .replace("__ATLAS__", json.dumps(open(os.path.join(RIG, MON + ".atlas"), encoding="utf-8").read()))
         .replace("__PNG__", "data:image/png;base64," + b64(MON + ".png")).replace("__EXTRA__", extra)
         .replace("__INFO__", json.dumps(info, ensure_ascii=False)).replace("__ADDEXTRA__", mo_xe[a:b]))
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
            _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={c}&extra=tl_extra.json&n={n}&tw=380&th={int(round(380 * vh / vw))}&cols=8&view={view}{tt}")
    elif lenh == "gif":
        gif()
    elif lenh == "song":
        song()
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "tl_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
