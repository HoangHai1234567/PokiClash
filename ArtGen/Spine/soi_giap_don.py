# -*- coding: utf-8 -*-
"""Sói giáp sắt: bộ ĐẶT DÁNG cho ba clip tấn công (người dùng 2026-11-16: "animation tấn công cả 3 kiểu còn yếu và hơi xấu").

Bản đầu chỉ xoay FK tay trên dáng có sẵn của họ nên thiếu lực: không nhún lấy đà, không bật người, chân trượt. Ở đây mỗi clip là một
dãy DÁNG KHOÁ (pose to pose) đặt bằng tham số có nghĩa, nội suy có đường cong, rồi giải:
  - thân: hông dời / xoay, ngực, cổ, đầu (cộng lên dáng nền = dáng của họ hoặc dáng nghỉ);
  - CHÂN bám đất bằng IK hai khúc (đùi + ống tới cổ chân, bàn chân giữ góc thế giới): hông nhún, chồm, bật mà bàn chân không trượt;
  - TAY BÚA: hướng vai → nắm tay (góc thế giới) + độ duỗi + góc búa thế giới, IK hai khúc;
  - tay khiên: lệch FK; búa giãn dọc trục ở khung nhanh nhất (smear);
  - lớp phụ (bờm, vạt, đuôi, tai) trễ theo vận tốc thân: `phu`.
Tham số của một dáng (thiếu = như dáng nghỉ):
  mx, my   dời cả con (xương move; game nắn quãng lao theo mx)        hx, hy   dời hông (thế giới)
  hr       xoay hông (+ ngả ra sau, − chúi tới)   nr ngực   cr cổ   dr đầu   vr xương đòn + giáp vai
  ta, tk   tay búa: góc thế giới vai → nắm tay (độ), độ duỗi 0..1     tb  chiều gập khuỷu (±1)     ba  góc búa thế giới (nắm tay → đầu búa)
  bs       búa giãn dọc trục (1 = thường)
  k0..k3   tay khiên: lệch FK xương đòn, bắp, cẳng, khiên      kw  khiên giữ góc thế giới = nghỉ + kw (None: theo tay)
  kx, ky   bàn tay khiên giữ chỗ = chỗ nghỉ + (kx, ky) bằng IK (None: theo FK k0..k2)
  fRx fRy fRr / fLx fLy fLr   cổ chân gần / xa: dời so với chỗ đứng nghỉ, xoay bàn
"""
import math

import numpy as np

REST = dict(mx=0.0, my=0.0, hx=0.0, hy=0.0, hr=0.0, nr=0.0, cr=0.0, dr=0.0, vr=0.0, ta=None, tk=None, tb=-1.0, ba=None, bs=1.0,
            k0=0.0, k1=0.0, k2=0.0, k3=0.0, kw=None, kx=None, ky=0.0, fRx=0.0, fRy=0.0, fRr=0.0, fLx=0.0, fLy=0.0, fLr=0.0)
ZERO = np.array([0, 0, 0, 1, 1.0])


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


EASE = {"em": em, "lin": lambda x: min(1.0, max(0.0, x)), "in": lambda x: min(1.0, max(0.0, x)) ** 2.2,
        "out": lambda x: 1 - (1 - min(1.0, max(0.0, x))) ** 2.2, "in3": lambda x: min(1.0, max(0.0, x)) ** 3.2}


def _ang(v):
    return math.degrees(math.atan2(v[1], v[0]))


def _wrap(a):
    return a - 360.0 * round(a / 360.0)


class Bo:
    """bộ giải dáng trên một rig (sk): đo độ dài, dáng nghỉ một lần."""

    def __init__(self, sk):
        self.sk = sk
        W = sk.the_gioi()
        o = lambda b: W[b][:2, 2].copy()
        self.W0 = W
        self.vai, self.khuyu, self.nam, self.dau = o("P_shouR1"), o("P_shouR2"), o("P_shouR31"), o("dau_bua")
        self.L1, self.L2 = float(np.hypot(*(self.khuyu - self.vai))), float(np.hypot(*(self.nam - self.khuyu)))
        d = self.nam - self.vai
        self.ta0, self.tk0, self.ba0 = _ang(d), float(np.hypot(*d)) / (self.L1 + self.L2), _ang(self.dau - self.nam)
        self.kh0 = _ang(W["W_dunpai3"][:2, 0])
        h, g, m = o("P_shouL1"), o("P_shouL2"), o("P_shouL3")
        self.kh = dict(l1=float(np.hypot(*(g - h))), l2=float(np.hypot(*(m - g))), co=m, dau=1.0 if _wrap(_ang(g - h) - _ang(m - h)) > 0 else -1.0)
        self.chan = {}
        for k, (a, b, c) in dict(R=("P_tuiR1", "P_tuiR2", "P_tuiR3"), L=("P_tuiL1", "P_tuiL2", "P_tuiL3")).items():
            h, g, m = o(a), o(b), o(c)
            dau_ = 1.0 if _wrap(_ang(g - h) - _ang(m - h)) > 0 else -1.0
            self.chan[k] = dict(x=(a, b, c), l1=float(np.hypot(*(g - h))), l2=float(np.hypot(*(m - g))), co=m, goc=_ang(W[c][:2, 0]), dau=dau_)

    # ---- công cụ
    def _W(self, P):
        return self.sk.the_gioi(P)

    def xoay_tg(self, P, b, goc):
        """xoay xương b cho trục x của nó chĩa góc thế giới `goc`."""
        W = self._W(P)
        P.rot(b, _wrap(goc - _ang(W[b][:2, 0])))

    def doi_tg(self, P, b, dx, dy):
        """dời xương b một quãng THẾ GIỚI (dx, dy) (đổi sang hệ xương cha)."""
        W = self._W(P)
        cha = self.sk.bones[self.sk.bi[b]]["parent"]
        d = np.linalg.solve(W[cha][:2, :2], np.array([dx, dy], float))
        P.move(b, float(d[0]), float(d[1]))

    def ik2(self, P, b1, b2, dich, l1, l2, dau):
        W = self._W(P)
        g = W[b1][:2, 2]
        d = np.asarray(dich, float) - g
        L = float(np.hypot(*d))
        L = min(max(L, abs(l1 - l2) + 1.0), l1 + l2 - 0.5)
        a0 = _ang(d)
        c1 = (l1 * l1 + L * L - l2 * l2) / (2 * l1 * L)
        a1 = a0 + dau * math.degrees(math.acos(min(1.0, max(-1.0, c1))))
        self.xoay_tg(P, b1, a1)
        W = self._W(P)
        k = W[b2][:2, 2]
        dich2 = g + L * np.array([math.cos(math.radians(a0)), math.sin(math.radians(a0))])
        self.xoay_tg(P, b2, _ang(dich2 - k))

    # ---- đặt một dáng (tham số q) lên tư thế P (đã đặt dáng nền nếu có)
    def dat(self, P, q, chan="nghi", tay=True):
        """chan: "nghi" = cổ chân đặt theo chỗ đứng của dáng nghỉ (+ dời f*), "nen" = giữ cổ chân của dáng NỀN đang có trong P (dáng của
        họ: thế che khiên...) rồi mới chỉnh thân, False = để chân theo hông (chạy, bay)."""
        q = dict(REST, **q)
        giu = None
        if chan == "nen":
            W = self._W(P)
            giu = {k: (W[c["x"][2]][:2, 2].copy(), _ang(W[c["x"][2]][:2, 0])) for k, c in self.chan.items()}
        P.move("move", q["mx"], q["my"])
        P.move("bone2", q["hx"], q["hy"])
        for b, k in (("P_shenti1", "hr"), ("P_shenti3", "nr"), ("P_shenti8", "cr"), ("P_tou2", "dr"), ("P_shenti9", "vr"),
                     ("P_shenti10", "k0"), ("P_shouL1", "k1"), ("P_shouL2", "k2"), ("W_dunpai3", "k3")):
            if abs(q[k]) > 1e-6:
                P.rot(b, q[k])
        if q["kx"] is not None:                                      # bàn tay khiên giữ chỗ (so với xương move) = chỗ nghỉ + (kx, ky): IK hai khúc
            c = self.kh
            self.ik2(P, "P_shouL1", "P_shouL2", c["co"] + np.array([q["mx"] + q["kx"], q["my"] + q["ky"]]), c["l1"], c["l2"], c["dau"])
        if q["kw"] is not None:                                      # khiên giữ góc THẾ GIỚI = góc nghỉ + kw (thân chúi, ngả thì khiên vẫn dựng)
            W = self._W(P)
            P.rot("W_dunpai3", _wrap(self.kh0 + q["kw"] - _ang(W["W_dunpai3"][:2, 0])))
        if chan:
            mv = np.array([q["mx"], q["my"]])                        # cổ chân đi theo xương move; nhấc chân bằng f*y
            for k, c in self.chan.items():
                a, b, m = c["x"]
                co, goc = (giu[k][0] + mv, giu[k][1]) if giu else (c["co"] + mv, c["goc"])
                self.ik2(P, a, b, co + np.array([q[f"f{k}x"], q[f"f{k}y"]]), c["l1"], c["l2"], c["dau"])
                self.xoay_tg(P, m, goc + q[f"f{k}r"])
        if tay and q["ta"] is not None:
            W = self._W(P)
            s = W["P_shouR1"][:2, 2]
            tk = self.tk0 if q["tk"] is None else q["tk"]
            L = tk * (self.L1 + self.L2)
            f = s + L * np.array([math.cos(math.radians(q["ta"])), math.sin(math.radians(q["ta"]))])
            self.ik2(P, "P_shouR1", "P_shouR2", f, self.L1, self.L2, q["tb"])
            if q["ba"] is not None:
                W = self._W(P)
                P.rot("P_shouR31", _wrap(q["ba"] - _ang(W["dau_bua"][:2, 2] - W["P_shouR31"][:2, 2])))
        if abs(q["bs"] - 1.0) > 1e-4:
            P.scale("W_futou", q["bs"], 1.0 / math.sqrt(q["bs"]))
        return P

    def nghi(self):
        return dict(REST, ta=self.ta0, tk=self.tk0, ba=self.ba0, kw=0.0, kx=0.0, ky=0.0)


def noi(keys, t):
    """nội suy dãy dáng khoá [(giây, dict tham số, kiểu cong tới khoá này)] ở giây t → dict tham số (khoá thiếu tham số: lấy khoá trước)."""
    day = []
    cur = {}
    for tt, q, e in keys:
        cur = dict(cur, **q)
        day.append((tt, dict(cur), e))
    if t <= day[0][0]:
        return day[0][1]
    for (t0, a, _), (t1, b, e) in zip(day, day[1:]):
        if t <= t1:
            w = EASE[e]((t - t0) / max(1e-6, t1 - t0))
            out = {}
            for k in b:
                va = a.get(k, REST.get(k))
                out[k] = (va + (b[k] - va) * w) if isinstance(va, (int, float)) and isinstance(b[k], (int, float)) else b[k]
            return out
    return day[-1][1]


CHUOI = {  # lớp phụ: (xương, hệ số theo vận tốc xoay thân, theo vận tốc ngang, theo vận tốc dọc, trễ khung, chặn độ)
    "P_shenti4": (0.035, 0.012, 0.010, 1, 16), "P_shenti5": (0.045, 0.016, 0.012, 2, 20),
    "P_shenti6": (0.035, 0.012, 0.010, 1, 16), "P_shenti7": (0.050, 0.018, 0.014, 3, 22),
    "P_yaodai": (0.030, 0.020, -0.004, 1, 22), "P_yaodai2": (0.040, 0.026, -0.006, 2, 28), "P_yaodai3": (0.045, 0.030, -0.008, 3, 30),
    "P_weiba": (0.030, 0.014, 0.012, 1, 20), "P_weiba2": (0.040, 0.018, 0.016, 2, 24), "P_weiba3": (0.050, 0.02, 0.02, 3, 28),
    "P_erduoR": (0.030, 0.008, 0.012, 1, 14), "P_erduoR2": (0.040, 0.010, 0.016, 2, 18),
    "P_erduoL": (0.030, 0.008, 0.012, 1, 14), "P_erduoL2": (0.040, 0.010, 0.016, 2, 18),
    "P_xianglian1": (0.015, 0.006, 0.006, 2, 8), "P_diaozhui1": (0.050, 0.02, 0.01, 2, 24), "P_diaozhui2": (0.06, 0.024, 0.012, 3, 28),
    "P_diaozhui4": (0.04, 0.02, 0.01, 2, 20),
}


def phu(sk, frames, fps=30.0, manh=1.0, t0=0.0, t1=1e9):
    """lớp phụ trễ theo thân (bờm, vạt, đuôi, tai, mặt dây): cộng góc theo vận tốc xoay của ngực và vận tốc dời của hông ở vài khung
    TRƯỚC (trễ), làm trơn, chặn biên. Chỉ áp trong [t0, t1] (ngoài đó để nguyên chuyển động của họ)."""
    n = len(frames)
    th, px, py = np.zeros(n), np.zeros(n), np.zeros(n)
    for i, P in enumerate(frames):
        W = sk.the_gioi(P)
        th[i] = _ang(W["P_shenti3"][:2, 0])
        px[i], py[i] = W["P_shenti1"][0, 2], W["P_shenti1"][1, 2]
    th = np.degrees(np.unwrap(np.radians(th)))
    dth, dx, dy = np.gradient(th) * fps, np.gradient(px) * fps, np.gradient(py) * fps

    def tron(a, k=2):
        ker = np.array([1, 2, 3, 2, 1], float) if k == 2 else np.array([1, 2, 1], float)
        return np.convolve(np.pad(a, (len(ker) // 2,) * 2, mode="edge"), ker / ker.sum(), mode="valid")
    dth, dx, dy = tron(dth), tron(dx), tron(dy)
    for b, (kr, kx, ky, tre, chan_) in CHUOI.items():
        if b not in sk.bi:
            continue
        for i, P in enumerate(frames):
            t = i / fps
            if not (t0 <= t <= t1):
                continue
            j = max(0, i - tre)
            w = min(1.0, (t - t0) / 0.1) * min(1.0, max(0.0, (t1 - t) / 0.15))
            a = -(kr * dth[j]) + kx * dx[j] - ky * dy[j]
            a = chan_ * math.tanh(a * manh / chan_)
            P.rot(b, float(a * w))
    return frames
