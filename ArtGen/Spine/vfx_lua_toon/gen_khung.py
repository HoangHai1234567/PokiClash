# -*- coding: utf-8 -*-
"""Khung hiệu ứng lửa toon kiểu "lửa lỏng": phun lửa, luồng nhỏ, cầu lửa, mũi tên lửa, nổ trúng, nổ nấm.

Mẫu style: ba clip người dùng gửi 2026-11-23 (C:/Users/ADMIN/Videos/firebreath.mp4, explosion.mp4,
Screen Recordings/Screen Recording 2026-11-23 225926.mp4 = flamethrower).
- Múi lửa: thân đỏ thẫm, đáy đỏ sẫm, mũ vàng mép chảy giọt, vệt sáng kem, viền cam mảnh.
- Tan: ruột múi rỗng dần (ăn mòn từ trong), còn viền cuộn chữ C rồi viền đứt và mất.
- Luồng nhỏ: lõi kem, ăn mòn theo nhiễu trôi, chia tầng màu cứng.
Không quầng sáng, không gradient: mỗi vùng một màu đều.

    py -3 -I gen_khung.py <fx>|tat [--sheet]

Ra: frames/<fx>/<fx>_NN.png (24 khung/giây), frames/manifest.json, xem/<fx>_sheet.png.
"""
import json
import math
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "frames")
XEM = os.path.join(HERE, "xem")
FPS = 24
SS = 2  # vẽ to gấp đôi rồi thu nhỏ cho mép mượt

PAL = {
    # lửa lỏng
    "do": "#E2283C", "dod": "#A91B35", "vang": "#FFB424", "vangn": "#FFE25E", "kem": "#FFF6D6",
    "vien": "#FFA02E", "cam": "#FF7A2A",
    # luồng nhỏ
    "j_kem": "#FFF9EC", "j_vn": "#FFEBA6", "j_vang": "#FFD24A", "j_cam": "#FFA06A", "j_hong": "#F2647A",
    "j_tim": "#B45CE8",
    # khói, chớp
    "muc": "#2B2118", "khoi": "#3B2D2A", "khoi2": "#5E4A42", "dothan": "#7A1A2C",
}
LIQ = dict(base="do", shadow="dod", cap="vang", hl="vangn", core="kem", rim="vien")
SMOKE = dict(base="khoi", shadow="muc", cap="khoi2", hl=None, core=None, rim=None)


def hexc(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


# ---------------------------------------------------------------- nhiễu
class Perlin:
    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        p = rng.permutation(256)
        self.p = np.concatenate([p, p]).astype(np.int32)
        ang = rng.random(256) * 2 * np.pi
        self.g = np.stack([np.cos(ang), np.sin(ang)], 1).astype(np.float32)

    def __call__(self, x, y):
        x = np.asarray(x, np.float32)
        y = np.asarray(y, np.float32)
        xi = np.floor(x).astype(np.int32)
        yi = np.floor(y).astype(np.int32)
        xf = x - xi
        yf = y - yi
        xi &= 255
        yi &= 255
        x1 = (xi + 1) & 255
        y1 = (yi + 1) & 255
        p, g = self.p, self.g

        def dot(ix, iy, dx, dy):
            gg = g[p[p[ix] + iy]]
            return gg[..., 0] * dx + gg[..., 1] * dy

        u = xf * xf * xf * (xf * (xf * 6 - 15) + 10)
        v = yf * yf * yf * (yf * (yf * 6 - 15) + 10)
        n00 = dot(xi, yi, xf, yf)
        n10 = dot(x1, yi, xf - 1, yf)
        n01 = dot(xi, y1, xf, yf - 1)
        n11 = dot(x1, y1, xf - 1, yf - 1)
        a = n00 + u * (n10 - n00)
        b = n01 + u * (n11 - n01)
        return (a + v * (b - a)) * 1.41


def fbm(P, x, y, octaves=4, gain=0.5, lac=2.03):
    s = 0.0
    amp, f, norm = 1.0, 1.0, 0.0
    for i in range(octaves):
        s = s + amp * P(x * f + i * 17.3, y * f - i * 9.1)
        norm += amp
        amp *= gain
        f *= lac
    return s / norm * 1.6


def clamp01(x):
    return np.clip(x, 0.0, 1.0)


def c01(x):
    return min(max(x, 0.0), 1.0)


def sstep(a, b, x):
    t = c01((x - a) / (b - a))
    return t * t * (3 - 2 * t)


def ease_out(x, p=3):
    return 1 - (1 - c01(x)) ** p


def ease_in(x, p=2):
    return c01(x) ** p


def ease_out_back(x, s=1.7):
    x = c01(x) - 1
    return x * x * ((s + 1) * x + s) + 1


def relu(x):
    return np.maximum(x, 0.0)


PN = Perlin(7)  # nhiễu dùng chung cho mọi múi


# ---------------------------------------------------------------- vải vẽ
class Canvas:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.w, self.h = W * SS, H * SS
        self.rgb = np.zeros((self.h, self.w, 3), np.float32)
        self.a = np.zeros((self.h, self.w), np.float32)
        self.fire = np.zeros((self.h, self.w), np.float32)

    def rim_edge(self, col="vien", width=1.5):
        """Viền mảnh ở mép ngoài của cả khối lửa (và mép lỗ khi rỗng ruột)."""
        m = (self.fire > 0.5).astype(np.uint8)
        k = 2 * int(round(width * SS / 2 + 0.5)) + 1
        er = cv2.erode(m, np.ones((k, k), np.uint8)) > 0
        self.put(0, 0, (m > 0) & ~er, col)

    def box(self, cx, cy, rx, ry):
        x0 = int(max(0, math.floor(cx - rx)))
        x1 = int(min(self.w, math.ceil(cx + rx) + 1))
        y0 = int(max(0, math.floor(cy - ry)))
        y1 = int(min(self.h, math.ceil(cy + ry) + 1))
        if x1 <= x0 or y1 <= y0:
            return None
        Y, X = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        return y0, x0, X - cx, Y - cy

    def put(self, y0, x0, mask, col, al=1.0, fire=False):
        if col is None:
            return
        if isinstance(col, str):
            col = hexc(PAL[col])
        hh, ww = mask.shape
        m = mask.astype(np.float32) * al
        sr = self.rgb[y0:y0 + hh, x0:x0 + ww]
        sa = self.a[y0:y0 + hh, x0:x0 + ww]
        sr *= (1 - m[..., None])
        sr += col * m[..., None]
        sa *= (1 - m)
        sa += m
        sf = self.fire[y0:y0 + hh, x0:x0 + ww]
        sf *= (1 - m)
        if fire:
            sf += m

    def poly(self, pts, col, al=1.0):
        """pts: list (x, y) toạ độ 1x."""
        m = np.zeros((self.h, self.w), np.uint8)
        arr = np.round(np.array(pts, np.float32) * SS * 4).astype(np.int32)
        cv2.fillPoly(m, [arr], 1, lineType=cv2.LINE_8, shift=2)
        self.put(0, 0, m > 0, col, al)

    def out(self):
        pre = np.dstack([self.rgb * self.a[..., None], self.a]).astype(np.float32)
        small = cv2.resize(pre, (self.W, self.H), interpolation=cv2.INTER_AREA)
        al = small[..., 3]
        col = np.where(al[..., None] > 1e-4, small[..., :3] / np.maximum(al[..., None], 1e-4), 0)
        img = np.dstack([col[..., 2], col[..., 1], col[..., 0], al * 255])  # BGRA
        return np.clip(img + 0.5, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- múi lửa
def blob(cv, x, y, r, seed=0, hot=0.3, hollow=0.0, rimcut=0.0, alpha=1.0, sx=1.0, sy=1.0, rot=0.0,
         ph=0.0, pal=LIQ, rimw=None, drips=3, rimon=None):
    """Một múi. hot: 1 = gần như kem/vàng hết, 0 = đỏ có mũ vàng nhỏ. hollow: 0..1 rỗng ruột.
    rimcut: 0..1 viền đứt dần. ph: pha nhiễu (radian) cho múi sôi; vòng lặp dùng 2*pi*t/P."""
    if alpha <= 0.01 or r < 0.6:
        return
    P = PN
    R = r * SS
    cx, cy = x * SS, y * SS
    ext = R * 1.3 * max(sx, sy)
    b = cv.box(cx, cy, ext, ext)
    if b is None:
        return
    y0, x0, dx, dy = b
    c, s = math.cos(rot), math.sin(rot)
    lx = (c * dx + s * dy) / sx
    ly = (-s * dx + c * dy) / sy
    d = np.hypot(lx, ly)
    th = np.arctan2(ly, lx)
    ct, st = np.cos(th), np.sin(th)
    ox, oy = 0.55 * math.cos(ph), 0.55 * math.sin(ph)
    wob = 1 + 0.12 * P(ct * 1.25 + seed * 3.7 + ox, st * 1.25 + seed * 1.3 + oy)
    rr = R * wob
    inside = d < rr
    if not inside.any():
        return
    dn = d / rr
    nf = P(lx / R * 1.7 + seed * 5.1 + ox, ly / R * 1.7 - seed * 2.3 + oy)
    keep = (nf * 0.5 + dn) > (hollow * 1.65 - 0.55)
    fill = inside & keep
    # mũ vàng theo hướng lên của thế giới
    xn = dx / (R * max(sx, sy))
    yn = dy / (R * max(sx, sy))
    rng = np.random.default_rng(seed * 7919 + 13)
    drip = 0.0
    for _ in range(drips):
        cxk = rng.uniform(-0.7, 0.7)
        wk = rng.uniform(0.13, 0.26)
        ak = rng.uniform(0.14, 0.3)
        drip = drip + ak * np.exp(-((xn - cxk) / wk) ** 2)
    lvl = -0.42 + 0.9 * hot
    yb = lvl + drip + 0.06 * P(xn * 3.1 + seed + ox, 4.2 + oy)
    rw = (rimw if rimw is not None else max(1.25, r * 0.065)) * SS
    rim = inside & (d > rr - rw)
    nr = P(ct * 1.7 + seed * 2.9 + 11 + ox * 0.6, st * 1.7 + seed * 0.7 + oy * 0.6)
    rimkeep = nr > (rimcut * 2.3 - 1.25)
    isf = pal is LIQ
    cv.put(y0, x0, fill, pal["base"], alpha, isf)
    if pal.get("shadow"):
        sh = fill & (yn > 0.58 + 0.08 * nf) & (dn > 0.35)
        cv.put(y0, x0, sh, pal["shadow"], alpha, isf)
    cap = fill & (yn < yb)
    cv.put(y0, x0, cap, pal["cap"], alpha, isf)
    if isf:
        # giọt vàng nhỏ lơ lửng trong phần đỏ (như clip)
        for _ in range(2):
            bxn, byn = rng.uniform(-0.45, 0.45), lvl + rng.uniform(0.3, 0.55)
            br = rng.uniform(0.07, 0.11)
            bub = fill & (((xn - bxn) / (br * 1.4)) ** 2 + ((yn - byn) / br) ** 2 < 1)
            cv.put(y0, x0, bub, pal["cap"], alpha, isf)
    if pal.get("hl"):
        hl = cap & (yn < -0.68 + 0.45 * hot + 0.1 * nf) & (np.abs(xn) < 0.55)
        cv.put(y0, x0, hl, pal["hl"], alpha, isf)
        if hot > 0.7 and pal.get("core"):
            core = cap & (yn < -1.1 + 0.9 * hot + 0.1 * nf) & (np.abs(xn) < 0.45)
            cv.put(y0, x0, core, pal["core"], alpha, isf)
    # viền riêng từng múi chỉ hiện khi múi đã rỗng ruột (còn viền cuộn như clip)
    show_rim = rimon if rimon is not None else hollow > 0.02
    if pal.get("rim") and show_rim:
        ra = alpha * (1.0 if rimon else c01(hollow * 8))
        cv.put(y0, x0, rim & rimkeep, pal["rim"], ra, isf)


def dot(cv, x, y, r, col="vangn", alpha=1.0, sx=1.0, sy=1.0, rot=0.0):
    R = r * SS
    b = cv.box(x * SS, y * SS, R * max(sx, sy) + 1, R * max(sx, sy) + 1)
    if b is None or alpha <= 0.01:
        return
    y0, x0, dx, dy = b
    c, s = math.cos(rot), math.sin(rot)
    lx = (c * dx + s * dy) / sx
    ly = (-s * dx + c * dy) / sy
    cv.put(y0, x0, lx * lx + ly * ly < R * R, col, alpha)


def star(cv, x, y, ro, ri, n=8, rot=0.0, col="kem", alpha=1.0, jitter=0.0, seed=0):
    rng = np.random.default_rng(seed)
    pts = []
    for i in range(2 * n):
        a = rot + i * math.pi / n
        rr = ro * (1 + jitter * rng.uniform(-1, 1)) if i % 2 == 0 else ri
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    cv.poly(pts, col, alpha)


def ring(cv, x, y, r, w, col="vien", alpha=1.0, sy=1.0):
    R, Wd = r * SS, w * SS
    b = cv.box(x * SS, y * SS, R + Wd, R * sy + Wd)
    if b is None or alpha <= 0.01:
        return
    y0, x0, dx, dy = b
    d = np.hypot(dx, dy / sy)
    cv.put(y0, x0, (d < R) & (d > R - Wd), col, alpha)


def tube(cv, pts, rads, seed=0, hot=0.6, ph=0.0, pal=LIQ, alpha=1.0):
    """Luồng liền: hợp các vòng tròn, mũ vàng phía trên, viền ở mép ngoài."""
    if len(pts) == 0 or alpha <= 0.01:
        return
    P = PN
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    rm = max(rads) + 2
    cx = (min(xs) + max(xs)) / 2 * SS
    cy = (min(ys) + max(ys)) / 2 * SS
    b = cv.box(cx, cy, ((max(xs) - min(xs)) / 2 + rm) * SS, ((max(ys) - min(ys)) / 2 + rm) * SS)
    if b is None:
        return
    y0, x0, dx, dy = b
    X = dx + cx
    Y = dy + cy
    ox, oy = 0.5 * math.cos(ph), 0.5 * math.sin(ph)
    fill = np.zeros(dx.shape, bool)
    cap = np.zeros(dx.shape, bool)
    hl = np.zeros(dx.shape, bool)
    for i, ((px, py), r) in enumerate(zip(pts, rads)):
        R = r * SS
        ddx = X - px * SS
        ddy = Y - py * SS
        inside = ddx * ddx + ddy * ddy < R * R
        fill |= inside
        yn = ddy / max(R, 1)
        n = P(X / (SS * 22) - ph * 0.3 + seed, Y / (SS * 14) + oy)
        cap |= inside & (yn < -0.15 + 0.9 * hot + 0.35 * n)
        hl |= inside & (yn < -0.75 + 0.75 * hot + 0.3 * n)
    cv.put(y0, x0, fill, pal["base"], alpha, True)
    if hot <= 0:  # thân nấm: một màu đỏ, không mũ
        return
    cv.put(y0, x0, cap, pal["cap"], alpha, True)
    if pal.get("hl"):
        cv.put(y0, x0, hl & cap, pal["hl"], alpha, True)


def ribbon(cv, pts, widths, col, alpha=1.0):
    """Dải thuôn: pts đường giữa, widths nửa bề rộng tại từng điểm."""
    pts = np.array(pts, np.float32)
    if len(pts) < 2:
        return
    tang = np.gradient(pts, axis=0)
    tang /= np.maximum(np.linalg.norm(tang, axis=1, keepdims=True), 1e-6)
    nrm = np.stack([-tang[:, 1], tang[:, 0]], 1)
    w = np.array(widths, np.float32)[:, None]
    left = pts + nrm * w
    right = pts - nrm * w
    poly = np.concatenate([left, right[::-1]], 0)
    cv.poly(poly.tolist(), col, alpha)


def rnd(seed):
    return np.random.default_rng(seed * 1009 + 7)


# ---------------------------------------------------------------- 1. phun lửa lớn (kiểu flamethrower)
PHUN_W, PHUN_H, PHUN_X0, PHUN_Y0 = 640, 330, 26, 190
T_EMIT = 0.7


def phun_path(age, a, D, ph, sw):
    """Vị trí một múi theo tuổi: phóng nhanh rồi hãm, lan theo góc a, ngóc lên, cuộn sóng."""
    s = D * ease_out(age / 0.6, 2.4) + 40 * max(age - 0.6, 0)
    x = PHUN_X0 + s * math.cos(a)
    y = PHUN_Y0 + s * math.sin(a) - 70 * age * age - 26 * math.sin(age * 6.5 + ph) * min(1, s / 240) * sw
    return x, y, s


def phun_lua(t):
    cv = Canvas(PHUN_W, PHUN_H)
    dt = 1 / 34
    items = []
    j = 0
    while j * dt <= T_EMIT:
        tb = j * dt
        age = t - tb
        R = rnd(j)
        life = R.uniform(0.7, 0.86)
        if 0 <= age <= life:
            a = R.normal(0, 0.15) - 0.05
            D = R.uniform(0.62, 0.92) * (PHUN_W - 120)
            ph = R.uniform(0, 6.28)
            r1 = R.uniform(40, 70)
            x, y, s = phun_path(age, a, D, ph, R.uniform(0.6, 1.2))
            r = (5 + (r1 - 5) * ease_out(age / 0.42, 2)) * (1 + 0.18 * c01((age - 0.4) / 0.5))
            a01 = age / life
            hot = 0.28 + 0.72 * (1 - c01(age / 0.26))
            items.append((tb, dict(x=x, y=y, r=r, seed=j, hot=hot, hollow=sstep(0.45, 0.8, a01),
                                   rimcut=sstep(0.68, 1.0, a01), alpha=1 - sstep(0.94, 1.0, a01),
                                   ph=age * 5 + ph, sy=0.92, rot=a * 0.6)))
        j += 1
    # múi mới vẽ sau (nằm trên), như clip: múi gần miệng đè múi xa
    for _, kw in sorted(items, key=lambda it: it[0]):
        blob(cv, **kw)
    # luồng liền sát miệng
    pts, rads = [], []
    for k in range(26):
        age = k * 0.011
        tb = t - age
        if tb < 0 or tb > T_EMIT:
            continue
        x, y, s = phun_path(age, -0.05, 0.77 * (PHUN_W - 120), 0.0, 0.0)
        pts.append((x, y))
        rads.append(4 + 30 * ease_out(age / 0.3, 1.6))
    tube(cv, pts, rads, hot=0.5, ph=t * 8)
    cv.rim_edge()
    # nòng: chấm kem sáng
    if t < T_EMIT + 0.12:
        k = 1 - sstep(T_EMIT - 0.02, T_EMIT + 0.12, t)
        rr = (9 + 1.5 * math.sin(t * 40)) * k * ease_out(t / 0.05)
        dot(cv, PHUN_X0, PHUN_Y0, rr + 3, "vang")
        dot(cv, PHUN_X0, PHUN_Y0, rr, "kem")
    return cv.out()


# ---------------------------------------------------------------- 2. luồng phun nhỏ, lặp (đòn thường, giữ tia)
def phun_nho(t, P_LOOP=0.5, W=300, H=120):
    w, h = W * SS, H * SS
    Y, X = np.mgrid[0:h, 0:w].astype(np.float32)
    x0, yc, L = 10 * SS, h * 0.55, (W - 22) * SS
    u = (X - x0) / L
    uc = np.clip(u, 0, 1.2)
    hw = h * (0.012 + 0.34 * uc ** 0.75)
    v = (Y - yc + h * 0.06 * uc ** 2) / hw
    p = (t % P_LOOP) / P_LOOP

    def field(off):
        nx = uc * 5.5 - off
        ny = v * 1.1
        qx = fbm(PN, nx * 0.6, ny * 0.6 + 3.1, 3)
        return fbm(PN, nx + 0.9 * qx, ny + 0.6, 4)

    S = 5.0
    n = ((1 - p) * field(p * S) + p * field((p - 1) * S)) / math.sqrt((1 - p) ** 2 + p ** 2)
    lump = 1 + 0.25 * n
    ve = v / lump
    base = 1 - ve * ve - relu(u - 0.92) * 9
    val = 0.62 * base + 0.42 * n
    heat = 1 - 0.55 * uc
    s = val - (0.06 + 0.6 * (1 - heat))
    score = s * 1.2 + heat * 0.75
    names = ["j_kem", "j_vn", "j_vang", "j_cam", "j_hong"]
    idx = np.full(s.shape, len(names), np.int32)
    for i, lv in reversed(list(enumerate([1.02, 0.84, 0.64, 0.42]))):
        idx = np.where(score > lv, i + 1, idx)
    lut = np.zeros((len(names) + 1, 3), np.float32)
    for i, nm in enumerate(names):
        lut[i + 1] = hexc(PAL[nm])
    rgb = lut[idx]
    a = (s > 0).astype(np.float32)
    # vệt tím sát nòng
    tim = (s > 0) & (u < 0.07) & (np.abs(v) < 0.35)
    rgb[tim] = hexc(PAL["j_tim"])
    cv = Canvas(W, H)
    cv.rgb, cv.a = rgb, a
    return cv.out()


# ---------------------------------------------------------------- 3. cầu lửa bay, lặp
def cau_lua(t, P_LOOP=0.5, W=300, H=170):
    cv = Canvas(W, H)
    bx, by, br = 212, 88, 38
    phl = 2 * math.pi * (t % P_LOOP) / P_LOOP
    # đuôi lửa thuôn sau quả cầu: 3 lưỡi vẫy theo pha, đỏ ngoài, vàng trong
    xs = np.linspace(bx - 10, bx - 190, 36)
    q = (bx - 10 - xs) / 180
    for col, amp, wmax, ph0 in [("vien", 0, 30, 0.0), ("do", 0, 27, 0.0), ("vang", 2, 15, 0.8), ("vangn", 3, 7, 1.6)]:
        for sgn in (-1, 0, 1):
            ys = by - 4 + sgn * 15 * q + 9 * np.sin(xs * 0.05 + phl * 2 + ph0 + sgn * 1.3) * q - 18 * q * q
            wd = (wmax if sgn == 0 else wmax * 0.6) * (1 - q) ** 1.1 + 0.4
            ribbon(cv, list(zip(xs, ys)), wd, col)
    N = 12
    dt = P_LOOP / N
    life = 0.4
    items = []
    j0 = int(math.floor((t - life) / dt)) - 1
    for j in range(j0, int(math.floor(t / dt)) + 1):
        tb = j * dt
        age = t - tb
        if age < 0 or age > life:
            continue
        R = rnd(j % N + 100)
        a01 = age / life
        if j % 3:
            continue
        x = bx - 150 - 110 * ease_out(a01, 1.5)
        y = by - 20 + R.uniform(-22, 18) * ease_out(a01, 1.3) - 40 * age
        r = R.uniform(9, 14) * (1 - 0.3 * a01)
        items.append((tb, dict(x=x, y=y, r=r, seed=j % N + 100, hot=0.4,
                               hollow=sstep(0.0, 0.45, a01) * 0.9 + 0.1, rimcut=sstep(0.4, 1.0, a01), rimw=1.1,
                               alpha=1 - sstep(0.93, 1, a01), ph=phl + j)))
    for _, kw in sorted(items, key=lambda it: it[0]):
        blob(cv, **kw)
    # than văng ra sau
    for k in range(5):
        R = rnd(k + 300)
        ph0 = R.uniform(0, 1)
        q = ((t / P_LOOP) + ph0) % 1.0
        x = bx - 30 - 190 * q
        y = by + R.uniform(-40, 40) * q - 20 * q
        dot(cv, x, y, 3.2 * (1 - q) + 0.8, "vangn", 1 - sstep(0.75, 1, q))
    # quả cầu chính: sôi theo pha vòng lặp
    pulse = 1 + 0.05 * math.sin(phl * 2)
    blob(cv, bx - 22, by + 4, br * 0.62 * pulse, seed=9, hot=0.35, ph=phl + 1)
    blob(cv, bx, by, br * pulse, seed=3, hot=0.5, ph=phl, sx=1.08, sy=0.96)
    cv.rim_edge()
    return cv.out()


# ---------------------------------------------------------------- 4. mũi tên lửa bay, lặp
def muiten(t, P_LOOP=0.5, W=340, H=120):
    cv = Canvas(W, H)
    tipx, yc = 318, 60
    phl = 2 * math.pi * (t % P_LOOP) / P_LOOP
    # đuôi múi nhỏ rỗng dần
    N = 10
    dt = P_LOOP / N
    life = 0.34
    items = []
    j0 = int(math.floor((t - life) / dt)) - 1
    for j in range(j0, int(math.floor(t / dt)) + 1):
        tb = j * dt
        age = t - tb
        if age < 0 or age > life:
            continue
        R = rnd(j % N + 500)
        a01 = age / life
        if j % 2:
            continue
        x = tipx - 215 - 90 * ease_out(a01, 1.4)
        y = yc + R.uniform(-16, 16) * a01 + 5 * math.sin(age * 20 + j)
        r = R.uniform(7, 11) * (1 - 0.3 * a01)
        items.append((tb, dict(x=x, y=y, r=r, seed=j % N + 500, hot=0.4,
                               hollow=0.15 + 0.85 * sstep(0.0, 0.5, a01), rimcut=sstep(0.4, 1, a01),
                               alpha=1 - sstep(0.9, 1, a01), ph=phl + j, rimw=1.1, drips=3)))
    for _, kw in sorted(items, key=lambda it: it[0]):
        blob(cv, **kw)
    # ba lưỡi lửa vẫy theo pha, từ ngoài vào trong
    xs = np.linspace(tipx - 44, tipx - 230, 40)
    for lay, (col, amp, wmax, k, ph0) in enumerate([("do", 15, 15, 0.055, 0.0), ("vang", 10, 9, 0.06, 0.9),
                                                    ("kem", 5, 4, 0.065, 1.7)]):
        for sgn in (-1, 1):
            q = (tipx - 44 - xs) / 186
            env = np.sin(np.clip(q, 0, 1) * math.pi * 0.9 + 0.25)
            ys = yc + sgn * (4 + amp * q) + amp * 0.6 * np.sin(xs * k + phl * 2 + ph0 + sgn) * q
            wd = wmax * (1 - q) ** 1.2 * env + 0.5
            ribbon(cv, list(zip(xs, ys)), wd, col)
    # thân giữa
    ribbon(cv, [(tipx - 40, yc), (tipx - 140, yc + 1)], [7, 2], "vang")
    ribbon(cv, [(tipx - 40, yc), (tipx - 120, yc + 1)], [3.5, 1], "kem")
    # đầu mũi tên: viền cam, vàng, lõi kem
    fl = 1 + 0.04 * math.sin(phl * 3)

    def head(sc, col):
        L, Hh, notch = 58 * sc * fl, 24 * sc, 16 * sc
        cv.poly([(tipx - (1 - sc) * 8, yc), (tipx - L, yc - Hh), (tipx - L + notch, yc), (tipx - L, yc + Hh)], col)

    head(1.0, "vien")
    head(0.9, "do")
    head(0.72, "vang")
    head(0.45, "kem")
    return cv.out()


# ---------------------------------------------------------------- 5. nổ trúng (cầu lửa, tên lửa chạm)
def no_trung(t, W=320, H=320):
    cv = Canvas(W, H)
    cx, cy = 160, 170
    # vòng va chạm mảnh
    if 0.03 < t < 0.3:
        q = (t - 0.03) / 0.27
        ring(cv, cx, cy, 30 + 110 * ease_out(q, 2.5), 3.0 * (1 - q) + 0.8, "vien", 1 - sstep(0.6, 1, q), sy=0.8)
    # than văng
    for k in range(12):
        R = rnd(k + 900)
        a = R.uniform(0, 2 * math.pi)
        sp = R.uniform(150, 300)
        q = c01((t - 0.03) / 0.6)
        if q <= 0 or q >= 1:
            continue
        dist = sp * (1 - (1 - q) ** 2) * 0.55
        x = cx + dist * math.cos(a)
        y = cy + dist * math.sin(a) * 0.85 + 160 * q * q
        dot(cv, x, y, R.uniform(2.5, 4.5) * (1 - q * 0.7), "vangn", 1 - sstep(0.7, 1, q))
    # múi bung toả tròn
    n = 9
    items = []
    for k in range(n):
        R = rnd(k + 700)
        a = k * 2 * math.pi / n + R.uniform(-0.3, 0.3)
        dl = R.uniform(0.0, 0.05)
        age = t - 0.025 - dl
        if age < 0:
            continue
        life = R.uniform(0.6, 0.72)
        a01 = age / life
        if a01 > 1:
            continue
        dist = R.uniform(46, 76) * ease_out(age / 0.3, 2.6)
        x = cx + dist * math.cos(a)
        y = cy + dist * math.sin(a) * 0.82 - 40 * age
        r = R.uniform(26, 40) * ease_out_back(age / 0.16) * (1 + 0.12 * a01)
        items.append((-dist, dict(x=x, y=y, r=r, seed=k + 700, hot=0.3 + 0.7 * (1 - c01(age / 0.22)),
                                  hollow=sstep(0.42, 0.82, a01), rimcut=sstep(0.66, 1.0, a01),
                                  alpha=1 - sstep(0.93, 1, a01), ph=age * 6 + k)))
    for _, kw in sorted(items, key=lambda it: it[0]):
        blob(cv, **kw)
    # lõi giữa
    age = t - 0.02
    if 0 <= age <= 0.62:
        a01 = age / 0.62
        blob(cv, cx, cy - 30 * age, 52 * ease_out_back(age / 0.14) * (1 + 0.1 * a01), seed=777,
             hot=0.35 + 0.65 * (1 - c01(age / 0.25)), hollow=sstep(0.35, 0.8, a01), rimcut=sstep(0.6, 1, a01),
             alpha=1 - sstep(0.92, 1, a01), ph=age * 6)
    cv.rim_edge()
    # chớp sao 3 khung đầu
    if t < 0.13:
        k = [0.55, 1.0, 0.7, 0.35][min(3, int(t * FPS))]
        star(cv, cx, cy, 95 * k, 26 * k, n=8, rot=0.2, col="vang", jitter=0.25, seed=4)
        star(cv, cx, cy, 70 * k, 18 * k, n=8, rot=0.2, col="kem", jitter=0.25, seed=4)
    return cv.out()


# ---------------------------------------------------------------- 6. nổ nấm (chiêu cuối)
def no_nam(t, W=420, H=460):
    cv = Canvas(W, H)
    gx, gy = 210, 420
    f = int(round(t * FPS))
    # khung 0: sao chữ thập báo trước
    if f == 0:
        ribbon(cv, [(gx, gy - 150), (gx, gy), (gx, gy + 20)], [0.5, 6, 0.5], "vang")
        ribbon(cv, [(gx - 120, gy - 6), (gx, gy - 6), (gx + 120, gy - 6)], [0.5, 5, 0.5], "vang")
        ribbon(cv, [(gx, gy - 110), (gx, gy), (gx, gy + 12)], [0.4, 2.5, 0.4], "kem")
        ribbon(cv, [(gx - 90, gy - 6), (gx, gy - 6), (gx + 90, gy - 6)], [0.4, 2.2, 0.4], "kem")
        star(cv, gx, gy - 6, 18, 5, n=4, col="kem")
        return cv.out()
    # khung 1: khung đảo, đĩa tối tia đỏ
    if f == 1:
        cxx, cyy = gx, gy - 150
        dot(cv, cxx, cyy, 190, "muc")
        R = rnd(42)
        for k in range(14):
            a = k * 2 * math.pi / 14 + R.uniform(-0.15, 0.15)
            L = R.uniform(120, 185)
            w = R.uniform(5, 11)
            p0 = (cxx + 30 * math.cos(a), cyy + 30 * math.sin(a))
            p1 = (cxx + L * math.cos(a), cyy + L * math.sin(a))
            ribbon(cv, [p0, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2), p1], [0.5, w, 0.5],
                   "do" if k % 3 else "cam")
        ring(cv, cxx, cyy, 120, 4, "do", 1.0, sy=0.55)
        dot(cv, cxx, cyy, 26, "do")
        return cv.out()
    # khung 2: đĩa kem, gai đỏ sẫm cắm từ mép vào
    if f == 2:
        cxx, cyy = gx, gy - 150
        dot(cv, cxx, cyy, 186, "kem")
        R = rnd(43)
        for k in range(16):
            a = k * 2 * math.pi / 16 + R.uniform(-0.12, 0.12)
            L = R.uniform(70, 125)
            w = R.uniform(9, 18)
            p0 = (cxx + 186 * math.cos(a), cyy + 186 * math.sin(a))
            p1 = (cxx + (186 - L) * math.cos(a), cyy + (186 - L) * math.sin(a))
            ribbon(cv, [p0, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2), p1], [w, w * 0.6, 0.5],
                   "dothan" if k % 2 else "do")
        return cv.out()
    # khung 3: đĩa kem viền vàng
    if f == 3:
        dot(cv, gx, gy - 150, 178, "vang")
        dot(cv, gx, gy - 150, 168, "kem")
        return cv.out()

    # từ khung 4: khói chân, thân nấm, mũ nấm
    end = 1.75
    fade = 1 - sstep(end - 0.12, end, t)
    # cột phụt (0.17 – 0.45)
    if t < 0.5:
        q = ease_out((t - 0.13) / 0.1, 2)
        dq = 1 - sstep(0.3, 0.5, t)
        R = rnd(1300)
        for k in range(7):
            xo = (k - 3) * 15 + R.uniform(-6, 6)
            hgt = (150 + R.uniform(0, 120)) * q * dq
            lean = R.uniform(-18, 18)
            if hgt < 4:
                continue
            base_w = R.uniform(10, 18)
            pts = [(gx + xo + lean * s_, gy - hgt * s_) for s_ in np.linspace(0, 1, 8)]
            wds = [base_w * (1 - s_) ** 0.8 + 0.6 for s_ in np.linspace(0, 1, 8)]
            ribbon(cv, pts, [w_ + 2.5 for w_ in wds], "vien")
            ribbon(cv, pts, wds, "vang")
            ribbon(cv, pts[:6], [w_ * 0.45 for w_ in wds[:6]], "kem")
    # thân nấm
    cap_y0 = 215
    rise = cap_y0 - 45 * ease_out((t - 0.4) / 1.3, 1.6)
    if t > 0.32:
        q = ease_out((t - 0.32) / 0.25, 2)
        top = gy - (gy - rise - 30) * q
        shrink = 1 - sstep(1.1, 1.6, t)
        pts, rads = [], []
        for s_ in np.linspace(0, 1, 14):
            y = gy - 10 - (gy - 10 - top) * s_
            wv = (24 - 12 * math.sin(s_ * math.pi * 0.9) + 8 * s_) * shrink
            pts.append((gx + 4 * math.sin(s_ * 5 + t * 3), y))
            rads.append(wv)
        if shrink > 0.05:
            tube(cv, pts, rads, hot=-0.3, ph=t * 4, alpha=fade)
        # gân vàng chạy dọc thân
        R = rnd(1400)
        for k in range(3 if shrink > 0.3 else 0):
            xo = (k - 1) * 9 + R.uniform(-3, 3)
            ys = np.linspace(gy - 14, top + 20, 10)
            xs = gx + xo * (0.6 + 0.4 * np.abs(np.linspace(-1, 1, 10))) + 3 * np.sin(ys * 0.06 + t * 9 + k)
            ribbon(cv, list(zip(xs, ys)), [0.6] + [1.6] * 8 + [0.6], "vangn", fade * (0.6 + 0.4 * math.sin(t * 30 + k)))
    # mũ nấm: các múi bay từ chân lên vị trí, rồi sôi, nguội, rỗng
    layout = [(-105, 18, 40), (-60, 30, 44), (-12, 34, 46), (38, 30, 44), (88, 22, 42), (122, -2, 32),
              (-128, -2, 32), (-82, -18, 42), (-30, -14, 46), (24, -16, 46), (74, -20, 42),
              (-50, -54, 38), (2, -58, 42), (52, -52, 38), (-14, -88, 30), (30, -84, 28)]
    items = []
    for k, (ox, oy, rr) in enumerate(layout):
        R = rnd(k + 1500)
        dl = 0.24 + 0.012 * k + R.uniform(0, 0.03)
        age = t - dl
        if age < 0:
            continue
        q = ease_out(age / 0.34, 2.2)
        sc = 1 + 0.12 * ease_out((t - 0.5) / 1.2, 1.5)
        tx, ty = gx + ox * sc, rise + oy * sc
        x = gx + ox * 0.25 + (tx - gx - ox * 0.25) * q
        y = gy - 30 + (ty - gy + 30) * q
        r = rr * (0.35 + 0.65 * ease_out_back(age / 0.3)) * sc * (1 + 0.04 * math.sin(t * 7 + k))
        lowk = c01((oy + 10) / 45)  # múi dưới nguội đỏ sớm
        hot = 1 - c01(age / 0.5) * (0.6 + 0.3 * lowk)
        a01 = c01((t - 0.95 - 0.02 * (15 - k)) / 0.5)
        items.append((oy, dict(x=x, y=y, r=r, seed=k + 1500, hot=hot, hollow=sstep(0.0, 0.7, a01),
                               rimcut=sstep(0.45, 1.0, a01), alpha=fade, ph=t * 4 + k, sy=0.9)))
    # múi trên vẽ trước, múi dưới đè lên (như ảnh mẫu: tầng dưới phía trước)
    for _, kw in sorted(items, key=lambda it: it[0]):
        blob(cv, **kw)
    cv.rim_edge()
    # khói đen chân lan ra
    for k in range(14):
        R = rnd(k + 1200)
        side = -1 if k % 2 else 1
        q = ease_out((t - 0.17 - 0.02 * k) / 0.7, 2.2)
        if q <= 0:
            continue
        x = gx + side * (12 + (10 + 11 * (k // 2) + R.uniform(0, 20)) * q)
        y = gy - R.uniform(0, 18) - 8 * q
        r = R.uniform(18, 34) * (0.4 + 0.6 * q)
        blob(cv, x, y, r, seed=k + 1200, hot=0.15, pal=SMOKE, alpha=fade,
             hollow=sstep(1.25, 1.7, t + R.uniform(0, 0.1)), ph=t * 3 + k, drips=2)
    # than bay lên
    for k in range(10):
        R = rnd(k + 1600)
        q = c01((t - 0.3 - R.uniform(0, 0.6)) / 0.9)
        if q <= 0 or q >= 1:
            continue
        x = gx + R.uniform(-150, 150) + 20 * math.sin(q * 6 + k)
        y = rise + R.uniform(-20, 80) - 170 * q
        dot(cv, x, y, R.uniform(2.5, 4.5) * (1 - q * 0.6), "vangn", (1 - sstep(0.7, 1, q)) * fade)
    return cv.out()


# ---------------------------------------------------------------- xuất
JOBS = {
    # tên: (hàm, giây, lặp?, điểm neo (x, y) trong khung, tỉ lệ tờ xem)
    "phun_lua": (phun_lua, 1.6, False, (PHUN_X0, PHUN_Y0), 0.42),
    "phun_nho": (phun_nho, 0.5, True, (10, 66), 0.8),
    "cau_lua": (cau_lua, 0.5, True, (212, 88), 0.8),
    "muiten": (muiten, 0.5, True, (318, 60), 0.8),
    "no_trung": (no_trung, 0.75, False, (160, 170), 0.6),
    "no_nam": (no_nam, 1.75, False, (210, 420), 0.42),
}


def render(name):
    fn, dur, loop, anchor, _ = JOBS[name]
    n = int(round(dur * FPS))
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith(".png"):
            os.remove(os.path.join(d, f))
    frames = []
    for i in range(n):
        img = fn(i / FPS)
        cv2.imwrite(os.path.join(d, f"{name}_{i:02d}.png"), img)
        frames.append(img)
    h, w = frames[0].shape[:2]
    print(name, n, "khung", w, "x", h)
    return frames, dict(count=n, w=w, h=h, fps=FPS, loop=loop, anchor=list(anchor))


def sheet(name, frames, cols=6, bg="#E8DCC0", scale=1.0):
    os.makedirs(XEM, exist_ok=True)
    h, w = frames[0].shape[:2]
    tw, th = int(w * scale), int(h * scale)
    rows = (len(frames) + cols - 1) // cols
    out = np.full((rows * (th + 4), cols * (tw + 4), 3), 255, np.uint8)
    bgc = hexc(bg)[::-1]
    for i, f in enumerate(frames):
        r, c = divmod(i, cols)
        fr = cv2.resize(f, (tw, th), interpolation=cv2.INTER_AREA) if scale != 1 else f
        al = fr[..., 3:4].astype(np.float32) / 255
        tile = (fr[..., :3].astype(np.float32) * al + bgc * (1 - al)).astype(np.uint8)
        cv2.putText(tile, f"{i / FPS:.2f}", (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (40, 40, 40), 1)
        out[r * (th + 4):r * (th + 4) + th, c * (tw + 4):c * (tw + 4) + tw] = tile
    p = os.path.join(XEM, f"{name}_sheet.png")
    cv2.imwrite(p, out)
    print(p)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "tat"
    names = list(JOBS) if which == "tat" else which.split(",")
    mpath = os.path.join(OUT, "manifest.json")
    man = json.load(open(mpath, encoding="utf-8")) if os.path.exists(mpath) else {}
    for nm in names:
        fr, info = render(nm)
        man[nm] = info
        if "--sheet" in sys.argv:
            sheet(nm, fr, scale=JOBS[nm][4])
    os.makedirs(OUT, exist_ok=True)
    json.dump(man, open(mpath, "w", encoding="utf-8"), indent=1)
