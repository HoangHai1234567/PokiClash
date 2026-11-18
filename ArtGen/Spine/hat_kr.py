# -*- coding: utf-8 -*-
"""hat_kr.py: bộ hình hạt kiểu Kingdom Rush 5 cho hiệu ứng trận PokiClash (2026-11-18).

Người dùng chê (2026-11-18): khói rải rác chưa thành cụm, chưa mềm; lửa, nước chưa được như Kingdom Rush; nổ, sóng âm chưa đẹp;
cụm dung nham là quả cầu tròn; cuối tia cụt lủn; hạt hút quanh cầu tụ xấu; màu chưa tươi; đốm lửa lẻ to quá.
Bộ này vẽ lại hình hạt bằng thuật toán (trường khoảng cách có dấu, SDF): mỗi hình là một khối liền nhiều múi, học DÁNG từ tờ khung
KR5 (ArtGen/ThamKhao/KR5/to_khung), không chép, không cắt ảnh của Ironhide.

Quy ước (như bộ cũ fire.py / xuat_hat.py):
- ảnh 384x384 RGBA. Bản vân hat_<tên>_<i>.png: xám nhạt có vân chì gạch chéo, game nhuộm bằng Image.color (màu x xám).
  Bản đặc hat_<tên>s_<i>.png: trắng đặc, ĐÃ NỞ SẴN DIL (1,6% khung, ~6 px) quanh bản vân, nên mép lõm, mép trong của hình rỗng
  và giọt tách rời đều có viền mực khi vẽ cùng cỡ; game vẫn có thể +2..5 như HatLua.
- Tô phẳng, không quầng, không gradient sáng tối. Riêng khói (kr_khoi, kr_khoinho, kr_khoiday) mép mềm (người dùng cho phép).
- Hình vân giữ "hình sao" quanh điểm co lớp (PIVOT): các lớp màu trong là bản thu nhỏ quanh điểm đó nên nằm gọn trong lớp ngoài.
- Gốc / hướng / điểm co của từng tên: bảng TEN ở dưới.

Chạy:  py -3 -I ArtGen/Spine/hat_kr.py                 -> ArtGen/Spine/hat_kr/*.png + xem.png
       py -3 -I ArtGen/Spine/hat_kr.py kr_lua kr_mao   -> chỉ các tên đó, tờ xem thử hat_kr/xem_thu.png
       py -3 -I ArtGen/Spine/hat_kr.py --xuat          -> chép thêm sang Assets/03 Art/Fx/Hat/ (chỉ file hat_kr_*)
"""
import math
import os
import shutil
import sys
import zlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fire import GRAY, HATCH_LO, INK  # noqa: E402  (màu nền vân, nét chì, mực của bộ cũ)

OUT = os.path.join(HERE, "hat_kr")
UNITY = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx", "Hat"))
N, G = 384, 768          # cỡ ảnh ra; lưới tính SDF (gấp 2 rồi trung bình khối)
MARGIN = 0.055           # lề của bản vân (phần khung)
DIL = 0.016              # bản đặc nở thêm (phần khung)
BIG = 1e3


# ======================================================================================================================
# SDF: lưới, hình cơ bản, phép gộp
# ======================================================================================================================
def rng_of(name, i):
    return np.random.RandomState((zlib.crc32(name.encode()) + 7919 * i) & 0x7FFFFFFF)


def smin(a, b, k):
    """hợp mềm (Inigo Quilez): chỗ nối hai múi lượn tròn bán kính ~k thay vì gãy góc."""
    if k <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def union(ds, k=0.0):
    out = ds[0]
    for d in ds[1:]:
        out = smin(out, d, k)
    return out


def sub(a, b):
    return np.maximum(a, -b)


class Grid:
    """lưới điểm trong toạ độ THIẾT KẾ (khung 0..1, y xuống) ứng với lưới ảnh ra qua co giãn + dời (không xoay):
    điểm thiết kế = anchor + (điểm ra - target) / s."""

    def __init__(self, n, anchor=(0.5, 0.5), target=(0.5, 0.5), s=1.0, lo=0.0, hi=1.0):
        u = lo + (np.arange(n) + 0.5) / n * (hi - lo)
        self.xs = (anchor[0] + (u - target[0]) / s).astype(np.float32)
        self.ys = (anchor[1] + (u - target[1]) / s).astype(np.float32)
        self.n, self.s = n, s
        self.px = float((hi - lo) / n / s)  # một điểm ảnh, đơn vị thiết kế

    def full(self):
        return np.full((self.n, self.n), BIG, np.float32)

    def win(self, x0, x1, y0, y1):
        c0, c1 = np.searchsorted(self.xs, [x0, x1])
        r0, r1 = np.searchsorted(self.ys, [y0, y1])
        if c1 <= c0 or r1 <= r0:
            return None
        return slice(r0, r1), slice(c0, c1)

    def XY(self, w):
        return self.xs[w[1]][None, :], self.ys[w[0]][:, None]


def circle(g, cx, cy, r, pad=0.1):
    d = g.full()
    w = g.win(cx - r - pad, cx + r + pad, cy - r - pad, cy + r + pad)
    if w:
        X, Y = g.XY(w)
        d[w] = np.hypot(X - cx, Y - cy) - r
    return d


def ellipse(g, cx, cy, rx, ry, rot=0.0, pad=0.1):
    d = g.full()
    m = max(rx, ry) + pad
    w = g.win(cx - m, cx + m, cy - m, cy + m)
    if w:
        X, Y = g.XY(w)
        c, s = math.cos(rot), math.sin(rot)
        dx, dy = X - cx, Y - cy
        u, v = dx * c + dy * s, -dx * s + dy * c
        k0 = np.hypot(u / rx, v / ry)
        k1 = np.hypot(u / (rx * rx), v / (ry * ry))
        d[w] = np.where(k0 < 1, (k0 - 1) * min(rx, ry), k0 * (k0 - 1) / np.maximum(k1, 1e-6))
    return d


def stroke(g, pts, rads, pad=0.1):
    """chuỗi đoạn có bán kính đổi dần (nét thon): SDF = khoảng tới đoạn - bán kính nội suy."""
    d = g.full()
    for (x0, y0), (x1, y1), r0, r1 in zip(pts[:-1], pts[1:], rads[:-1], rads[1:]):
        rm = max(r0, r1) + pad
        w = g.win(min(x0, x1) - rm, max(x0, x1) + rm, min(y0, y1) - rm, max(y0, y1) + rm)
        if not w:
            continue
        X, Y = g.XY(w)
        dx, dy = x1 - x0, y1 - y0
        L2 = max(dx * dx + dy * dy, 1e-12)
        t = np.clip(((X - x0) * dx + (Y - y0) * dy) / L2, 0, 1)
        v = np.hypot(X - (x0 + t * dx), Y - (y0 + t * dy)) - (r0 + (r1 - r0) * t)
        d[w] = np.minimum(d[w], v)
    return d


_NOISE = {}


def noise(g, seed, freq):
    """nhiễu trơn (giá trị, nội suy bậc 3) theo toạ độ thiết kế: dùng làm mép gợn / rung tay."""
    if seed not in _NOISE:
        _NOISE[seed] = np.random.RandomState(seed).standard_normal((64, 64)).astype(np.float32)
    yy, xx = np.meshgrid(g.ys * freq, g.xs * freq, indexing="ij")
    return ndimage.map_coordinates(_NOISE[seed], [yy % 64, xx % 64], order=3, mode="grid-wrap").astype(np.float32)


def walk(x, y, ang, length, n, angf=lambda t: 0.0):
    """đường giữa n điểm từ (x, y); ang: 0 = lên (-y), dương = ngả phải; angf(t) cộng thêm vào góc theo tiến độ t."""
    pts = [(x, y)]
    step = length / (n - 1)
    for j in range(1, n):
        a = ang + angf((j - 0.5) / (n - 1))
        x += math.sin(a) * step
        y -= math.cos(a) * step
        pts.append((x, y))
    return pts


def taper(n, r0, p=0.8, bulge=0.0, rmin=0.003):
    return [max(rmin, r0 * (1 - t) ** p * (1 + bulge * math.sin(math.pi * t))) for t in np.linspace(0, 1, n)]


class Spec:
    """build(g) -> {'main': sdf, 'aux': sdf (hình phụ cùng khung), 'holes': sdf (đục lỗ), 'cut': sdf (khe chỉ ở bản vân)}.
    fit: 'c' giữa khung | 'b' chân (ax, đáy hình) ở giữa đáy | 'l' gốc (mép trái, ay) ở giữa mép trái | 'p' điểm (ax, ay) ở tâm."""

    def __init__(self, build, fit="c", ax=0.5, ay=0.5, soft=0.0, cracks=(), crack_w=0.012):
        self.build, self.fit, self.ax, self.ay, self.soft = build, fit, ax, ay, soft
        self.cracks, self.crack_w = cracks, crack_w


def fit_of(spec):
    g = Grid(360, lo=-0.4, hi=1.4)
    sd = spec.build(g)["main"]
    ins = sd < 0
    rr, cc = np.where(ins.any(1))[0], np.where(ins.any(0))[0]
    x0, x1, y0, y1 = g.xs[cc[0]], g.xs[cc[-1]], g.ys[rr[0]], g.ys[rr[-1]]
    lo, hi = MARGIN, 1 - MARGIN
    if spec.fit == "c":
        A, T = ((x0 + x1) / 2, (y0 + y1) / 2), (0.5, 0.5)
    elif spec.fit == "b":
        A, T = (spec.ax, y1), (0.5, hi)
    elif spec.fit == "l":
        A, T = (x0, spec.ay), (lo, 0.5)
    else:
        A, T = (spec.ax, spec.ay), (0.5, 0.5)
    cand = []
    if A[0] - x0 > 1e-6:
        cand.append((T[0] - lo) / (A[0] - x0))
    if x1 - A[0] > 1e-6:
        cand.append((hi - T[0]) / (x1 - A[0]))
    if A[1] - y0 > 1e-6:
        cand.append((T[1] - lo) / (A[1] - y0))
    if y1 - A[1] > 1e-6:
        cand.append((hi - T[1]) / (y1 - A[1]))
    return A, T, float(min(cand))


def inside_dist(sd_fn, lo=-0.1, hi=1.1, n=240):
    """khoảng cách vào trong (đơn vị thiết kế) của một hình, trên lưới thô: để đặt lỗ, đốm sáng, vết nứt cho nằm gọn trong."""
    g = Grid(n, lo=lo, hi=hi)
    sd = sd_fn(g)
    din = ndimage.distance_transform_edt(sd < 0) * ((hi - lo) / n)
    return g, din


def pick_inside(g, din, rng, need, region=None, tries=600):
    for _ in range(tries):
        r, c = rng.randint(0, g.n), rng.randint(0, g.n)
        x, y = float(g.xs[c]), float(g.ys[r])
        if din[r, c] >= need and (region is None or region(x, y)):
            return x, y
    return None


# ======================================================================================================================
# raster: SDF -> mặt nạ, bản đặc nở sẵn, mép mềm, vân chì, vết nứt
# ======================================================================================================================
def _edt(b):
    return ndimage.distance_transform_edt(b).astype(np.float32)


def _down(a):
    return a.reshape(N, 2, N, 2).mean(axis=(1, 3))


def _ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def _cov(sd, g):
    return np.clip(0.5 - sd / g.px, 0, 1).astype(np.float32)


def _masks(sd, g, soft, fill=True):
    m = _cov(sd, g)
    ins = m >= 0.5
    if fill:  # lấp túi hở nhỏ giữa các múi (không thì mực lộ thành chấm đen)
        filled = ndimage.binary_fill_holes(ins)
        m = np.where(filled & ~ins, 1.0, m).astype(np.float32)
        ins = filled
    sol = np.maximum(m, np.clip(DIL * G + 0.5 - _edt(~ins), 0, 1))
    softa = None
    if soft:
        din = _edt(ins)
        w = float(np.clip(soft * din.max(), 0.02 * G, 0.045 * G))
        softa = _ss(0, w, din)
        m = softa
        sol = _ss(0, w, _edt(sol >= 0.5))
    return m, sol, softa


def van_tex(seed):
    """vân chì sáp: nền xám nhạt (GRAY) + nét gạch chéo sẫm hơn (HATCH_LO), hơi rung; cỡ nét theo khung 384 (khoảng 8 px)."""
    S = 3 * N
    rng = np.random.RandomState(seed)
    im = Image.new("L", (S, S), GRAY[0])
    d = ImageDraw.Draw(im)
    step = 24
    a = math.radians(-38)
    ca, sa = math.cos(a), math.sin(a)
    span = int(math.hypot(S, S)) + step
    for k in range(-span, span, step):
        jit = rng.uniform(-0.35, 0.35) * step
        pts = []
        for j in range(13):
            t = -span + 2 * span * j / 12
            off = k + jit + rng.uniform(-1.5, 1.5)
            pts.append((S / 2 + off * -sa + t * ca, S / 2 + off * ca + t * sa))
        c = int(GRAY[0] + (HATCH_LO[0] - GRAY[0]) * 0.85 * rng.uniform(0.6, 1.0))
        d.line(pts, fill=c, width=int(round(rng.uniform(5, 8))), joint="curve")
    return np.asarray(im.resize((N, N), Image.LANCZOS), np.float32)


def draw_cracks(cracks, tf, crack_w):
    """vết nứt vỏ (dung nham): nét gấp khúc thon dần, vẽ đậm hơn vân. Trả độ phủ 0..1 ở cỡ N."""
    S = 3 * N
    A, T, s = tf
    im = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(im)
    for poly, wm in cracks:
        P = [((T[0] + s * (x - A[0])) * S, (T[1] + s * (y - A[1])) * S) for x, y in poly]
        n = len(P)
        for j in range(n - 1):
            w = crack_w * wm * S * (1 - 0.6 * j / max(1, n - 2))
            d.line([P[j], P[j + 1]], fill=255, width=max(2, int(w)))
            r = w / 2
            d.ellipse([P[j + 1][0] - r, P[j + 1][1] - r, P[j + 1][0] + r, P[j + 1][1] + r], fill=255)
    return np.asarray(im.resize((N, N), Image.LANCZOS), np.float32) / 255


def render(spec, seed):
    A, T, s = fit_of(spec)
    g = Grid(G, A, T, s)
    out = spec.build(g)
    res = {"tf": (A, T, s)}
    m, sol, softa = _masks(out["main"], g, spec.soft)
    res["van"], res["solid"] = _down(m), _down(sol)
    if "holes" in out:
        m2, s2, _ = _masks(sub(out["main"], out["holes"]), g, spec.soft, fill=False)
        res["van_lo"], res["solid_lo"] = _down(m2), _down(s2)
    if "aux" in out:
        a = _cov(np.maximum(out["aux"], out["main"]), g)
        if softa is not None:
            a = a * softa
        res["aux"] = _down(a)
    if "cut" in out:
        res["van"] = res["van"] * (1 - _down(_cov(out["cut"], g)))
    tex = van_tex(seed)
    if spec.cracks:
        din = _edt(res["van"] >= 0.5)
        c = draw_cracks(spec.cracks, res["tf"], spec.crack_w) * _ss(0.015 * N, 0.04 * N, din)
        tex = tex * (1 - 0.92 * c) + 132 * 0.92 * c
    res["tex"] = tex
    return res


# ======================================================================================================================
# HÌNH: mỗi tên một hàm f_<tên>(i) -> Spec
# ======================================================================================================================
# ---------- khói: cụm nhiều múi tròn chồng nhau, to vừa nhỏ không đều, mép mềm; bóng nửa dưới tách riêng (kr_khoiday) ----------
KHOI = [
    [(0.27, 0.60, 0.150), (0.50, 0.38, 0.205), (0.74, 0.50, 0.150), (0.44, 0.66, 0.165), (0.67, 0.70, 0.120)],
    [(0.42, 0.24, 0.165), (0.64, 0.31, 0.135), (0.50, 0.48, 0.175), (0.29, 0.53, 0.125), (0.71, 0.57, 0.130), (0.48, 0.73, 0.130)],
    [(0.50, 0.29, 0.150), (0.29, 0.39, 0.120), (0.73, 0.40, 0.125), (0.42, 0.56, 0.175), (0.67, 0.61, 0.145), (0.24, 0.65, 0.105),
     (0.52, 0.77, 0.105)],
    [(0.62, 0.30, 0.190), (0.35, 0.45, 0.150), (0.57, 0.59, 0.160), (0.30, 0.71, 0.110)],
]
KHOINHO = [
    [(0.42, 0.52, 0.25), (0.71, 0.60, 0.15)],
    [(0.29, 0.42, 0.16), (0.52, 0.53, 0.21), (0.75, 0.63, 0.12)],
    [(0.46, 0.57, 0.24), (0.29, 0.37, 0.13), (0.73, 0.64, 0.12)],
    [(0.39, 0.39, 0.20), (0.63, 0.63, 0.19)],
]


def _lobes(rng, layout, pull=0.86, grow=1.06):
    """múi khói: kéo về trọng tâm (pull) và nở (grow) cho chồng sâu thành một cụm, không rời từng quả."""
    L = []
    mx = sum(t[0] for t in layout) / len(layout)
    my = sum(t[1] for t in layout) / len(layout)
    for x, y, r in sorted(layout, key=lambda t: t[1]):  # trên = sau, dưới = trước (múi dưới che múi trên)
        x = mx + (x - mx) * pull + rng.uniform(-0.012, 0.012)
        y = my + (y - my) * pull + rng.uniform(-0.012, 0.012)
        r *= grow * rng.uniform(0.95, 1.05)
        e = rng.uniform(-0.04, 0.1)
        L.append((x, y, r * (1 + e), r * (1 - e), rng.uniform(-0.5, 0.5), rng.uniform(-1, 1)))
    return L


def f_khoi(i, layout=None, name="kr_khoi"):
    rng = rng_of(name, i)
    lobes = _lobes(rng, layout or KHOI[i])
    seed = rng.randint(1 << 20)

    def build(g):
        nz = 0.004 * noise(g, seed, 6)
        L = [ellipse(g, x, y, rx, ry, rot) + nz for x, y, rx, ry, rot, _ in lobes]
        main = union(L, 0.012)
        sh = g.full()
        y0, y1 = min(t[1] for t in lobes), max(t[1] for t in lobes)
        for j, (x, y, rx, ry, rot, a) in enumerate(lobes):  # bóng: lưỡi liềm dưới trái của mỗi múi, phần không bị múi trước che
            ang = math.radians(-58 + 12 * a)
            r = (rx + ry) / 2
            dep = 0.26 + 0.3 * (y - y0) / max(1e-6, y1 - y0)  # múi dưới bóng dày (đáy cụm đậm), múi trên mỏng
            lit = ellipse(g, x + math.cos(ang) * r * dep, y + math.sin(ang) * r * dep, rx * 1.03, ry * 1.03, rot) + nz
            cres = sub(L[j], lit)
            if j < len(L) - 1:
                cres = sub(cres, union(L[j + 1:]))
            sh = np.minimum(sh, cres)
        return {"main": main, "aux": sh}

    return Spec(build, "c", soft=0.11)


def f_khoinho(i):
    rng = rng_of("kr_khoinho", i)
    lobes = _lobes(rng, KHOINHO[i])
    seed = rng.randint(1 << 20)

    def build(g):
        nz = 0.004 * noise(g, seed, 6)
        return {"main": union([ellipse(g, x, y, rx, ry, rot) + nz for x, y, rx, ry, rot, _ in lobes], 0.012)}

    return Spec(build, "c", soft=0.11)


# ---------- lửa: lưỡi chữ S liền khối, chân tròn mập, ngọn quặp; 2-3 giọt tách bay trên ngọn ----------
LUA = [
    dict(side=1, lean=0.10, sw=0.55, hook=1.35, rb=0.165, L=0.64, branch=[(-1, 0.27, 0.30)],
         drops=[("tongue", 0.10, -0.08, 0.042, 0.35), ("oval", -0.13, 0.03, 0.026, -0.2), ("oval", 0.20, 0.22, 0.020, 0.3)]),
    dict(side=-1, lean=-0.12, sw=0.45, hook=1.5, rb=0.185, L=0.58, branch=[(1, 0.22, 0.24)],
         drops=[("tongue", -0.12, -0.05, 0.040, -0.4), ("oval", 0.12, -0.02, 0.028, 0.2)]),
    dict(side=1, lean=0.03, sw=0.70, hook=1.1, rb=0.15, L=0.70, branch=[(1, 0.30, 0.26)],
         drops=[("oval", -0.09, -0.06, 0.032, -0.3), ("tongue", 0.12, 0.02, 0.034, 0.5)]),
    dict(side=-1, lean=0.0, sw=0.35, hook=1.25, rb=0.175, L=0.56, branch=[(-1, 0.24, 0.30), (1, 0.30, 0.27)],
         drops=[("tongue", 0.09, -0.07, 0.036, 0.3), ("oval", -0.12, -0.03, 0.026, -0.3), ("oval", 0.02, -0.16, 0.019, 0.0)]),
]


def _flame_tongue(x, y, ang, length, w0, side, sw, hook, n=30):
    pts = walk(x, y, ang, length, n,
               lambda t: side * sw * math.sin(math.pi * 1.7 * t) - side * hook * max(0.0, (t - 0.62) / 0.38) ** 1.6)
    return pts, taper(n, w0, 0.8, 0.3)


PIV_LUA = [(0.5, 0.92), (0.5, 0.70)]  # các điểm co lớp phải chịu được (phần khung): chân và giữa dưới


def _drops_inside(rng, body_fn, want, pivots, region, gap=0.025, ks=(0.8, 0.6, 0.38)):
    """đặt giọt tách rời quanh thân sao cho bản thu nhỏ của giọt (lớp màu trong, co quanh từng điểm co) luôn rơi gọn
    vào trong thân: lớp trong không lòi ra ngoài viền mực. want: [(bán kính hiệu dụng, dữ liệu)] theo thứ tự ưu tiên."""
    gl, din = inside_dist(body_fn, lo=-0.2, hi=1.2, n=280)
    dout = ndimage.distance_transform_edt(din <= 0) * (1.4 / 280)
    step = gl.xs[1] - gl.xs[0]

    def at(arr, x, y):
        c, r = int((x - gl.xs[0]) / step), int((y - gl.ys[0]) / step)
        return arr[r, c] if 0 <= r < gl.n and 0 <= c < gl.n else 0.0
    placed = []
    for reff, data in want:
        best, bs = None, -9
        for _ in range(2500):
            x, y = rng.uniform(*region[0]), rng.uniform(*region[1])
            if at(dout, x, y) < reff + gap or any(math.hypot(x - px, y - py) < reff + pr + 0.03 for px, py, pr, _ in placed):
                continue
            ok = True
            for P in pivots:
                for k in ks:
                    if at(din, P[0] + k * (x - P[0]), P[1] + k * (y - P[1])) < k * reff + 0.005:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                sc = -y + rng.uniform(0, 0.08) - 0.3 * abs(at(dout, x, y) - reff - gap)
                if sc > bs:
                    bs, best = sc, (x, y)
        if best:
            placed.append((best[0], best[1], reff, data))
    return placed


def f_lua(i):
    P = LUA[i]
    rng = rng_of("kr_lua", i)
    seed = rng.randint(1 << 20)
    bx, by = 0.5, 0.80
    pts, rads = _flame_tongue(bx, by, P["lean"], P["L"], P["rb"], P["side"], P["sw"], P["hook"])
    parts = []  # (pts, rads) các ngọn phụ ở vai
    for sd, ts, ln in P["branch"]:
        j = int(ts * (len(pts) - 1))
        x, y = pts[j]
        w = rads[j]
        bp = walk(x + sd * w * 0.5, y, sd * 0.95, ln, 18, lambda t, sd=sd: -sd * 0.75 * t - sd * 0.9 * max(0.0, (t - 0.6) / 0.4) ** 1.5)
        parts.append((bp, taper(18, w * 0.62, 0.85, 0.15)))

    def body(g):
        d = smin(ellipse(g, bx, by, P["rb"] * 1.12, P["rb"] * 0.95), stroke(g, pts, rads), 0.04)
        for bp, br in parts:
            d = smin(d, stroke(g, bp, br), 0.03)
        return d

    # điểm co (khung) -> thiết kế: chân hình ở đáy, cao hình ~ từ ngọn tới chân
    ys = [p[1] for p in pts] + [by + P["rb"] * 0.95]
    top, bot = min(ys), max(ys)
    hgt = (bot - top) / 0.83
    pivots = [(bx, bot - (0.945 - py) * hgt) for _, py in PIV_LUA]
    want = [(r * 1.25, (kind, r, rot)) for kind, _, _, r, rot in P["drops"]]
    drops = _drops_inside(rng, body, want, pivots, ((0.18, 0.82), (top - 0.12, top + 0.32)))

    def build(g):
        d = body(g)
        for x, y, _, (kind, r, rot) in drops:
            if kind == "oval":
                dd = ellipse(g, x, y, r * 0.78, r * 1.22, rot)
            else:  # ngọn lửa con: đáy tròn, đầu nhọn chĩa lên, hơi quặp
                dp = walk(x, y + r * 0.9, rot, r * 2.5, 12, lambda t, rot=rot: 0.7 * t * t * (1 if rot > 0 else -1))
                dd = smin(circle(g, x, y + r * 0.9, r * 0.92), stroke(g, dp, taper(12, r * 0.92, 0.9)), 0.01)
            d = np.minimum(d, dd)
        return {"main": d + 0.0035 * noise(g, seed, 7)}

    return Spec(build, "b", ax=bx)


# ---------- chùm đốm lửa (thêm 2026-11-18 theo góp ý "đốm lửa lẻ to quá"): 3-5 ngọn con lệch cỡ trong một hình ----------
LUACHUM = [
    [(0.36, 0.60, 0.075, -0.25), (0.62, 0.46, 0.055, 0.3), (0.50, 0.24, 0.035, 0.1), (0.74, 0.74, 0.03, 0.4)],
    [(0.50, 0.58, 0.07, 0.15), (0.28, 0.40, 0.045, -0.35), (0.70, 0.30, 0.04, 0.35), (0.40, 0.18, 0.026, -0.1), (0.66, 0.72, 0.028, 0.2)],
    [(0.42, 0.50, 0.085, -0.2), (0.70, 0.62, 0.045, 0.3), (0.62, 0.24, 0.03, 0.2)],
    [(0.30, 0.66, 0.05, -0.3), (0.52, 0.44, 0.065, 0.1), (0.74, 0.58, 0.04, 0.35), (0.36, 0.22, 0.03, -0.2), (0.64, 0.18, 0.022, 0.2)],
]


def f_luachum(i):
    rng = rng_of("kr_luachum", i)
    seed = rng.randint(1 << 20)
    items = LUACHUM[i]

    def one(g, x, y, r, rot, k=1.0):
        """ngọn con; k < 1: bản thu nhỏ quanh đáy của chính nó (lõi)."""
        bx, by = x, y + r * 1.2
        dp = walk(bx, by - (1 - k) * r * 0.25, rot, r * 3.0 * k, 12, lambda t: 0.8 * t * t * (1 if rot > 0 else -1))
        return smin(circle(g, bx, by - (1 - k) * r * 0.25, r * k), stroke(g, dp, taper(12, r * k, 0.85)), 0.01 * k)

    def build(g):
        d, core = g.full(), g.full()
        for x, y, r, rot in items:
            d = np.minimum(d, one(g, x, y, r, rot))
            core = np.minimum(core, one(g, x, y, r, rot, 0.58))
        nz = 0.003 * noise(g, seed, 8)
        return {"main": d + nz, "aux": core + nz}

    return Spec(build, "c")


# ---------- khối lửa phồng: cầu lửa vỡ / lõi nổ, nhiều múi, mép gợn ----------
LUAKHOI = [
    dict(n=7, sq=0.70, r0=0.24, cleft=0, tri=False),
    dict(n=6, sq=1.00, r0=0.22, cleft=0, tri=False),
    dict(n=6, sq=0.88, r0=0.23, cleft=1, tri=False),
    dict(n=3, sq=1.00, r0=0.17, cleft=0, tri=True),
]


def f_luakhoi(i):
    P = LUAKHOI[i]
    rng = rng_of("kr_luakhoi", i)
    seed = rng.randint(1 << 20)
    r0, sq = P["r0"], P["sq"]
    lobes = [(0.5, 0.5, r0 * 1.05, r0 * sq)]
    a0 = rng.uniform(0, 2 * math.pi)
    for j in range(P["n"]):
        a = a0 + 2 * math.pi * j / P["n"] + rng.uniform(-0.25, 0.25)
        if P["tri"]:
            dist, r = 0.17, rng.uniform(0.16, 0.19)
        else:
            dist, r = r0 * rng.uniform(0.78, 1.0), rng.uniform(0.10, 0.15)
        lobes.append((0.5 + math.cos(a) * dist, 0.5 + math.sin(a) * dist * sq, r, r * (0.9 + 0.1 * sq)))
    bumps = []
    for x, y, rx, ry in lobes[1:]:
        base = math.atan2(y - 0.5, x - 0.5)
        for _ in range(rng.randint(1, 3)):
            a = base + rng.uniform(-0.8, 0.8)
            br = rng.uniform(0.028, 0.05)
            bumps.append((x + math.cos(a) * rx * 0.93, y + math.sin(a) * ry * 0.93, br))
    cleft = None
    if P["cleft"]:
        a = rng.uniform(-2.0, -1.2)
        p0 = (0.5 + math.cos(a) * 0.42, 0.5 + math.sin(a) * 0.42 * sq)
        cleft = walk(p0[0], p0[1], math.atan2(0.5 - p0[0], -(0.5 - p0[1])), 0.26, 10, lambda t: 0.4 * t)

    def build(g):
        d = union([ellipse(g, x, y, rx, ry) for x, y, rx, ry in lobes], 0.03)
        d = smin(d, union([circle(g, x, y, r) for x, y, r in bumps]), 0.012)
        d = d + 0.005 * noise(g, seed, 9)
        if cleft:
            d = sub(d, stroke(g, cleft, taper(10, 0.03, 1.0)))
        return {"main": d}

    return Spec(build, "c")


# ---------- liềm lửa: mảnh lửa văng trong vụ nổ, lưng (lồi) hướng +x, tâm khung ở chỗ dày nhất ----------
LIEM = [
    dict(R=0.36, span=150, skew=1.0, w=0.085, curl=0.18, asym=0.0),
    dict(R=0.34, span=165, skew=0.75, w=0.078, curl=0.26, asym=0.25),
    dict(R=0.29, span=118, skew=1.0, w=0.112, curl=0.10, asym=-0.1),
    dict(R=0.40, span=150, skew=1.35, w=0.062, curl=0.30, asym=0.15),
]


def f_liem(i):
    P = LIEM[i]
    rng = rng_of("kr_liem", i)
    seed = rng.randint(1 << 20)
    n = 44
    span = math.radians(P["span"])
    a0, a1 = -span / 2 * (1 + P["asym"]), span / 2 * (1 - P["asym"])
    us = np.linspace(0, 1, n)
    rads = [P["w"] * math.sin(math.pi * u ** P["skew"]) ** 0.75 + 0.003 for u in us]
    um = 0.5 ** (1 / P["skew"])
    am = a0 + (a1 - a0) * um
    R = P["R"]
    Ox, Oy = 0.5 - R * math.cos(am), 0.5 - R * math.sin(am)
    pts = []
    for u in us:
        a = a0 + (a1 - a0) * u
        rr = R * (1 - P["curl"] * abs(2 * u - 1) ** 3)
        pts.append((Ox + rr * math.cos(a), Oy + rr * math.sin(a)))

    def build(g):
        return {"main": stroke(g, pts, rads) + 0.003 * noise(g, seed, 7)}

    return Spec(build, "p", 0.5, 0.5)


# ---------- dung nham: khối chảy mềm, giọt kéo, mép gợn, khe nứt vỏ ----------
NHAM = [  # C: múi tròn (x, y, r): khối lõi gọn + bọt nổi trên đỉnh; D: giọt kéo ngắn cổ mập (gốc x, y, hướng, dài), rủ lệch nhau
    dict(C=[(0.48, 0.47, 0.24), (0.29, 0.52, 0.15), (0.67, 0.51, 0.15), (0.37, 0.29, 0.09), (0.57, 0.26, 0.10), (0.72, 0.36, 0.07)],
         D=[(0.35, 0.64, 1.85, 0.17), (0.63, 0.65, 1.42, 0.11)]),
    dict(C=[(0.50, 0.43, 0.22), (0.41, 0.58, 0.16), (0.61, 0.57, 0.15), (0.35, 0.28, 0.08), (0.60, 0.25, 0.09)],
         D=[(0.50, 0.70, 1.62, 0.19), (0.70, 0.50, 0.25, 0.12)]),
    dict(C=[(0.50, 0.49, 0.20), (0.32, 0.51, 0.16), (0.68, 0.48, 0.16), (0.19, 0.56, 0.09), (0.81, 0.51, 0.08), (0.44, 0.32, 0.08),
            (0.62, 0.32, 0.07)],
         D=[(0.29, 0.63, 1.85, 0.13), (0.55, 0.66, 1.52, 0.17), (0.77, 0.59, 1.3, 0.10)]),
    dict(C=[(0.55, 0.44, 0.21), (0.40, 0.56, 0.16), (0.69, 0.35, 0.12), (0.29, 0.65, 0.10), (0.60, 0.25, 0.08), (0.77, 0.49, 0.07)],
         D=[(0.25, 0.71, 2.4, 0.15), (0.51, 0.65, 1.6, 0.12)]),
]


def _drip(x, y, ang, length, r0=0.07, neck=0.022, bulb=0.046, n=22):
    """giọt kéo: gốc dày trong khối, cổ thắt, bầu tròn ở đầu; hướng ang (0 = sang phải, pi/2 = xuống), cong dần xuống."""
    pts, rads = [], []
    for j in range(n):
        t = j / (n - 1)
        a = ang + (math.pi / 2 - ang) * 0.18 * t
        if j:
            x += math.cos(a) * length / (n - 1)
            y += math.sin(a) * length / (n - 1)
        pts.append((x, y))
        if t < 0.62:
            rads.append(r0 + (neck - r0) * (t / 0.62) ** 0.8)
        else:
            rads.append(neck + (bulb - neck) * math.sin((t - 0.62) / 0.38 * math.pi / 2))
    return pts, rads


def _cracks(rng, centres, n):
    out = []
    for k in range(n):
        cx, cy, rx, ry = centres[k % len(centres)]
        x, y = cx + rng.uniform(-0.5, 0.5) * rx, cy + rng.uniform(-0.5, 0.5) * ry
        a = rng.uniform(0, 2 * math.pi)
        poly = [(x, y)]
        for _ in range(rng.randint(4, 7)):
            a += rng.uniform(-0.75, 0.75)
            st = rng.uniform(0.035, 0.06)
            x, y = x + math.cos(a) * st, y + math.sin(a) * st
            poly.append((x, y))
        out.append((poly, 1.0))
        bx, by = poly[len(poly) // 2]
        ba = a + rng.choice([-1, 1]) * rng.uniform(0.8, 1.4)
        br = [(bx, by)]
        for _ in range(rng.randint(2, 4)):
            ba += rng.uniform(-0.5, 0.5)
            bx, by = bx + math.cos(ba) * 0.04, by + math.sin(ba) * 0.04
            br.append((bx, by))
        out.append((br, 0.7))
    return out


def f_nham(i):
    P = NHAM[i]
    rng = rng_of("kr_nham", i)
    seed = rng.randint(1 << 20)
    drips = [_drip(x, y, a, ln, r0=0.085, neck=0.038, bulb=0.054) for x, y, a, ln in P["D"]]
    cracks = _cracks(rng, [(x, y, r * 0.8, r * 0.8) for x, y, r in P["C"][:3]], 3)

    def build(g):
        d = union([circle(g, x, y, r) for x, y, r in P["C"]], 0.04)
        for pts, rads in drips:
            d = smin(d, stroke(g, pts, rads), 0.035)
        d = d + 0.008 * noise(g, seed, 5) + 0.006 * noise(g, seed + 1, 14)
        return {"main": d}

    return Spec(build, "c", cracks=cracks, crack_w=0.016)


# ---------- giọt (nước, dung nham): đầu tròn bên PHẢI, đuôi thuôn sang trái ----------
def _tear(hx, R, tx, curve=0.0, p=1.0, n=26, bead=None, wob=0.0):
    pts, rads = [], []
    for j in range(n):
        t = j / (n - 1)
        x = hx + (tx - hx) * t
        y = 0.5 + curve * t * t + wob * math.sin(t * math.pi * 2.2) * t
        pts.append((x, y))
        r = R * (1 - t) ** p
        if bead:
            r += bead[1] * math.exp(-((t - bead[0]) / 0.09) ** 2)
        rads.append(max(0.003, r))
    return pts, rads


NHAMGIOT = [dict(hx=0.70, R=0.17, tx=0.08, curve=0.0, p=1.25),
            dict(hx=0.68, R=0.165, tx=0.10, curve=-0.14, p=1.1),
            dict(hx=0.70, R=0.16, tx=0.07, curve=0.04, p=1.35, bead=(0.6, 0.05)),
            dict(hx=0.63, R=0.21, tx=0.20, curve=0.0, p=1.0, wob=0.035)]
GIOT = [dict(hx=0.66, R=0.20, tx=0.08, curve=0.0, p=1.0),
        dict(hx=0.72, R=0.14, tx=0.06, curve=-0.09, p=1.3),
        dict(hx=0.62, R=0.24, tx=0.22, curve=0.0, p=0.9),
        dict(hx=0.68, R=0.17, tx=0.08, curve=0.0, p=1.15, wob=0.04)]


def f_nhamgiot(i):
    P = dict(NHAMGIOT[i])
    rng = rng_of("kr_nhamgiot", i)
    seed = rng.randint(1 << 20)
    hx, R = P.pop("hx"), P.pop("R")
    pts, rads = _tear(hx, R, **P)
    cracks = []
    if i in (0, 2):
        cracks = [([(hx + 0.06, 0.44), (hx + 0.01, 0.47), (hx - 0.03, 0.46), (hx - 0.08, 0.5)], 0.8)]

    def build(g):
        d = smin(circle(g, hx, 0.5, R), stroke(g, pts, rads), 0.02)
        return {"main": d + 0.005 * noise(g, seed, 7)}

    return Spec(build, "c", cracks=cracks)


def f_giot(i):
    P = dict(GIOT[i])
    hx, R = P.pop("hx"), P.pop("R")
    pts, rads = _tear(hx, R, **P)

    def build(g):
        return {"main": smin(circle(g, hx, 0.5, R), stroke(g, pts, rads), 0.015)}

    return Spec(build, "c")


# ---------- chùm giọt nước (thêm 2026-11-18): 3-5 giọt lệ lệch cỡ, cùng bay về +x ----------
GIOTCHUM = [
    [(0.66, 0.50, 0.075, 0.0), (0.38, 0.30, 0.05, -0.15), (0.34, 0.70, 0.04, 0.2), (0.82, 0.24, 0.028, -0.1)],
    [(0.70, 0.44, 0.065, -0.1), (0.46, 0.62, 0.055, 0.1), (0.30, 0.34, 0.035, -0.2), (0.80, 0.72, 0.03, 0.15), (0.20, 0.60, 0.022, 0.0)],
    [(0.60, 0.56, 0.085, 0.05), (0.36, 0.32, 0.04, -0.2), (0.84, 0.30, 0.03, -0.1)],
    [(0.74, 0.36, 0.055, -0.15), (0.52, 0.58, 0.065, 0.0), (0.30, 0.40, 0.04, -0.1), (0.76, 0.74, 0.035, 0.2), (0.24, 0.72, 0.025, 0.1)],
]


def f_giotchum(i):
    items = GIOTCHUM[i]

    def one(g, x, y, r, a, k=1.0):
        """giọt lệ; k < 1: bản thu nhỏ dồn về đầu tròn (lõi)."""
        x, y = x + math.cos(a) * r * (1 - k) * 0.3, y + math.sin(a) * r * (1 - k) * 0.3
        tail = (x - math.cos(a) * r * 3.4 * k, y - math.sin(a) * r * 3.4 * k)
        pts = [(x + (tail[0] - x) * t, y + (tail[1] - y) * t) for t in np.linspace(0, 1, 12)]
        return smin(circle(g, x, y, r * k), stroke(g, pts, taper(12, r * k, 1.05)), 0.008 * k)

    def build(g):
        d, core = g.full(), g.full()
        for x, y, r, a in items:
            d = np.minimum(d, one(g, x, y, r, a))
            core = np.minimum(core, one(g, x, y, r, a, 0.55))
        return {"main": d, "aux": core}

    return Spec(build, "c")


# ---------- mão nước toé: 5-9 lưỡi nhọn chĩa lên, chân rộng; bản đục lỗ (kr_maolo) cùng khung ----------
MAO = [
    dict(n=7, amax=72, Lmax=0.66, spread=0.50, w=0.085, hook=1.2, holes=7),
    dict(n=5, amax=64, Lmax=0.80, spread=0.40, w=0.10, hook=1.0, holes=6),
    dict(n=9, amax=78, Lmax=0.52, spread=0.60, w=0.068, hook=1.4, holes=9),
    dict(n=6, amax=70, Lmax=0.70, spread=0.48, w=0.09, hook=1.3, holes=7, asym=0.25),
]


def _mao_parts(i):
    P = MAO[i]
    rng = rng_of("kr_mao", i)
    tongues = []
    n = P["n"]
    for j in range(n):
        u = j / (n - 1)
        c = 2 * u - 1 + P.get("asym", 0) * 0.5
        a = math.radians(P["amax"]) * (2 * u - 1) + rng.uniform(-0.08, 0.08)
        L = P["Lmax"] * (0.28 + 0.72 * (1 - min(1, abs(c)) ** 1.6)) * rng.uniform(0.85, 1.1)
        x = 0.5 + (u - 0.5) * P["spread"] + rng.uniform(-0.015, 0.015)
        sgn = 1 if a >= 0 else -1
        bend = 0.35 * abs(2 * u - 1) + rng.uniform(0.0, 0.15)
        hk = P["hook"] * rng.uniform(0.5, 1.1) * (sgn if rng.uniform() < 0.75 else -sgn)
        pts = walk(x, 0.86, a, L, 24, lambda t, s=sgn, b=bend, h=hk: s * b * t ** 1.4 + h * max(0.0, (t - 0.7) / 0.3) ** 2)
        w0 = P["w"] * (0.7 + 0.5 * L / P["Lmax"])
        tongues.append((pts, taper(24, w0, 1.15, 0.2)))
    return P, rng, tongues


def f_mao(i):
    P, rng, tongues = _mao_parts(i)
    seed = rng.randint(1 << 20)

    def mao_sd(g):
        d = smin(ellipse(g, 0.5, 0.87, 0.37, 0.075), ellipse(g, 0.5, 0.79, 0.24, 0.13), 0.06)
        for pts, rads in tongues:
            d = smin(d, stroke(g, pts, rads), 0.035)
        return d + 0.003 * noise(g, seed, 7)

    gl, din = inside_dist(mao_sd)
    holes = []
    for _ in range(600):
        if len(holes) >= P["holes"]:
            break
        big = len(holes) < P["holes"] // 2
        r = rng.uniform(0.05, 0.085) if big else rng.uniform(0.022, 0.04)
        p = pick_inside(gl, din, rng, r * (0.75 if big else 1.0) + 0.01, lambda x, y: 0.3 < y < 0.9, tries=60)
        if p and all(math.hypot(p[0] - hx, p[1] - hy) > r + hr + 0.022 for hx, hy, hr, *_ in holes):
            holes.append((p[0], p[1], r, rng.uniform(0.75, 1.35), rng.uniform(0, math.pi)))

    def build(g):
        d = mao_sd(g)
        hs = g.full()
        for x, y, r, e, rot in holes:
            hs = np.minimum(hs, ellipse(g, x, y, r * e, r / e, rot))
        return {"main": d, "holes": hs + 0.003 * noise(g, seed + 3, 11)}

    return Spec(build, "b", ax=0.5)


# ---------- khối nước văng: tròn méo, mép phẳng; đốm sáng (kr_dom) cùng khung ----------
def f_khoinuoc(i):
    rng = rng_of("kr_khoinuoc", i)
    seed = rng.randint(1 << 20)

    def shape(g):
        if i == 0:  # hạt đậu cong
            d = smin(ellipse(g, 0.40, 0.52, 0.25, 0.17, -0.35), ellipse(g, 0.63, 0.44, 0.20, 0.15, 0.45), 0.08)
        elif i == 1:  # cục nước có đuôi văng
            tail = [(0.52 - 0.40 * t, 0.50 + 0.12 * t * t) for t in np.linspace(0, 1, 16)]
            d = smin(ellipse(g, 0.60, 0.48, 0.25, 0.20, 0.15), stroke(g, tail, taper(16, 0.17, 0.9, 0.0, 0.035)), 0.05)
            d = smin(d, circle(g, 0.12, 0.63, 0.045), 0.03)
        elif i == 2:  # tròn méo có bướu
            d = smin(circle(g, 0.48, 0.54, 0.27), circle(g, 0.71, 0.31, 0.10), 0.07)
        else:  # hai múi
            d = smin(ellipse(g, 0.35, 0.57, 0.19, 0.17, 0.0), ellipse(g, 0.64, 0.42, 0.21, 0.18, 0.3), 0.05)
            d = smin(d, circle(g, 0.22, 0.38, 0.06), 0.04)
        return d + 0.009 * noise(g, seed, 3.5)

    gl, din = inside_dist(shape)
    best, bv = None, -1
    for r in range(0, gl.n, 3):  # chỗ sâu trong khối, lệch lên trên phải
        for c in range(0, gl.n, 3):
            if din[r, c] > 0.09:
                v = din[r, c] + 0.35 * (gl.xs[c] - gl.ys[r])
                if v > bv:
                    bv, best = v, (float(gl.xs[c]), float(gl.ys[r]))
    dots = []
    if best:
        rot = -0.55 + rng.uniform(-0.2, 0.2)
        dots.append((best[0], best[1], 0.072, 0.034, rot))
        for k in range(30):
            a = rng.uniform(0, 2 * math.pi)
            q = (best[0] + math.cos(a) * 0.11, best[1] + math.sin(a) * 0.11)
            rr = int((q[1] - gl.ys[0]) / (gl.ys[1] - gl.ys[0]))
            cc = int((q[0] - gl.xs[0]) / (gl.xs[1] - gl.xs[0]))
            if 0 <= rr < gl.n and 0 <= cc < gl.n and din[rr, cc] > 0.05 and (i != 2 or k > 3):
                dots.append((q[0], q[1], 0.024, 0.022, 0.0))
                break

    def build(g):
        aux = g.full()
        for x, y, rx, ry, rot in dots:
            aux = np.minimum(aux, ellipse(g, x, y, rx, ry, rot))
        return {"main": shape(g), "aux": aux}

    return Spec(build, "c")


# ---------- vành giọt nước elip trên đất (2 biến thể) ----------
def _ring_segs(segs, rx, ry, thick, n=18):
    """các đoạn cung trên elip tâm (0.5, 0.5); thick(theta) bề dày; mỗi đoạn thuôn nhọn hai đầu."""
    out = []
    for a0, a1, k in segs:
        pts, rads = [], []
        for t in np.linspace(0, 1, n):
            a = a0 + (a1 - a0) * t
            pts.append((0.5 + math.cos(a) * rx, 0.5 + math.sin(a) * ry))
            rads.append(max(0.003, thick(a) * k * math.sin(math.pi * t) ** 0.6))
        out.append((pts, rads))
    return out


def f_vanh(i):
    rng = rng_of("kr_vanh", i)
    th = lambda a: 0.013 + 0.04 * max(0.0, math.sin(a)) ** 1.2  # dày phía trước (dưới), mỏng phía sau
    segs = []
    if i == 0:
        cuts = sorted([math.radians(v) for v in (-150, -95, -40, 15, 168)])
        for a0, a1 in zip(cuts, cuts[1:] + [cuts[0] + 2 * math.pi]):
            segs.append((a0 + 0.06, a1 - 0.06, rng.uniform(0.85, 1.1)))
    else:
        a = rng.uniform(0, 0.3)
        while a < 2 * math.pi - 0.2:
            ln = rng.uniform(0.25, 0.55)
            segs.append((a, a + ln, rng.uniform(0.75, 1.15)))
            a += ln + rng.uniform(0.08, 0.2)
    parts = _ring_segs(segs, 0.43, 0.15, th)
    dots = [(0.5 + math.cos(a) * 0.43 * k, 0.5 + math.sin(a) * 0.15 * k, r) for a, k, r in
            [(rng.uniform(0.2, 2.9), rng.uniform(1.12, 1.25), rng.uniform(0.012, 0.022)) for _ in range(5 + 3 * i)]]

    def build(g):
        d = g.full()
        for pts, rads in parts:
            d = np.minimum(d, stroke(g, pts, rads))
        for x, y, r in dots:
            d = np.minimum(d, ellipse(g, x, y, r * 1.5, r))
        return {"main": d}

    return Spec(build, "c")


# ---------- vòng cung sóng xung kích dẹt trên đất, đứt 3-5 đoạn ----------
CUNG = [(3, 0.0), (4, 0.4), (5, 0.15), (4, 1.1)]


def f_cung(i):
    rng = rng_of("kr_cung", i)
    n, off = CUNG[i]
    th = lambda a: 0.012 + 0.048 * max(0.0, math.sin(a)) ** 1.3
    segs = []
    base = [off + 2 * math.pi * j / n + rng.uniform(-0.25, 0.25) for j in range(n)]
    for j in range(n):
        a0 = base[j]
        a1 = base[(j + 1) % n] + (2 * math.pi if j == n - 1 else 0)
        gap = rng.uniform(0.2, 0.45)
        segs.append((a0 + gap / 2, a1 - gap / 2, rng.uniform(0.85, 1.15)))
    parts = _ring_segs(segs, 0.45, 0.15, th, n=24)

    def build(g):
        d = g.full()
        for pts, rads in parts:
            d = np.minimum(d, stroke(g, pts, rads))
        return {"main": d}

    return Spec(build, "c")


# ---------- sóng âm: dải cung dày thuôn nhọn hai đầu; lõm về TRÁI, lồi về PHẢI ----------
SONGAM = [dict(Rc=0.42, span=58, w=0.068, asym=0.0, rip=0),
          dict(Rc=0.30, span=74, w=0.048, asym=0.0, rip=0),
          dict(Rc=0.62, span=38, w=0.090, asym=0.35, rip=0),
          dict(Rc=0.44, span=56, w=0.062, asym=0.0, rip=3)]


def f_songam(i):
    P = SONGAM[i]
    rng = rng_of("kr_songam", i)
    seed = rng.randint(1 << 20)
    n = 40
    sp = math.radians(P["span"])
    Ox = 0.5 - P["Rc"]
    pts, rads = [], []
    for t in np.linspace(0, 1, n):
        a = -sp + 2 * sp * t
        pts.append((Ox + P["Rc"] * math.cos(a), 0.5 + P["Rc"] * math.sin(a)))
        tt = t ** (1 + P["asym"])
        w = P["w"] * math.sin(math.pi * tt) ** 0.8
        if P["rip"]:
            w *= 1 + 0.22 * math.sin(math.pi * 2 * P["rip"] * t) ** 2
        rads.append(max(0.003, w))

    def build(g):
        return {"main": stroke(g, pts, rads) + 0.002 * noise(g, seed, 6)}

    return Spec(build, "p", 0.5, 0.5)


# ---------- chớp nổ: cục chớp xoáy (0, 1) và sao gai (2, 3) ----------
def f_chop(i):
    rng = rng_of("kr_chop", i)
    seed = rng.randint(1 << 20)
    if i < 2:
        side = 1 if i == 0 else -1
        lobes = [(0.38, 0.40, 0.19), (0.64, 0.40, 0.17), (0.50, 0.63, 0.21), (0.74, 0.60, 0.09)] if i == 0 else                 [(0.37, 0.56, 0.21), (0.58, 0.33, 0.18), (0.67, 0.63, 0.15), (0.30, 0.30, 0.1), (0.50, 0.78, 0.08)]
        sp = []
        th0 = rng.uniform(0, 2 * math.pi)
        for t in np.linspace(0, 1, 50):
            th = th0 + side * t * 2.1 * math.pi
            r = 0.03 + 0.17 * t
            sp.append((0.5 + math.cos(th) * r, 0.5 + math.sin(th) * r))
        cw = [0.005 + 0.021 * math.sin(math.pi * t) ** 0.7 for t in np.linspace(0, 1, 50)]

        def build(g):
            d = union([circle(g, x, y, r) for x, y, r in lobes], 0.03) + 0.008 * noise(g, seed, 5)
            return {"main": d, "cut": stroke(g, sp, cw)}

        return Spec(build, "c")
    # sao gai: gai thon cong nhẹ kiểu chong chóng, dài ngắn lệch
    n = 10 if i == 2 else 7
    a0 = rng.uniform(0, 2 * math.pi)
    spikes = []
    for j in range(n):
        a = a0 + 2 * math.pi * j / n + rng.uniform(-0.12, 0.12)
        L = (0.44 if j % 2 == 0 else 0.29) * rng.uniform(0.9, 1.05) if i == 2 else rng.uniform(0.27, 0.45)
        pts = [(0.5 + math.cos(a + 0.22 * t * t) * L * t, 0.5 + math.sin(a + 0.22 * t * t) * L * t) for t in np.linspace(0, 1, 14)]
        spikes.append((pts, taper(14, 0.085 if i == 2 else 0.1, 1.0)))

    def build(g):
        d = circle(g, 0.5, 0.5, 0.17 if i == 2 else 0.15) + 0.006 * noise(g, seed, 7)
        for pts, rads in spikes:
            d = smin(d, stroke(g, pts, rads), 0.02)
        return {"main": d}

    return Spec(build, "c")


# ---------- đầu tia / bông va chạm cuối tia: gốc trái giữa khung, toé loe nhiều nhánh ra PHẢI ----------
TIADAU = [dict(n=5, amax=62, L=0.62, w=0.075, hook=0.0),
          dict(n=7, amax=70, L=0.66, w=0.055, hook=0.0),
          dict(n=6, amax=66, L=0.60, w=0.065, hook=1.0),
          dict(n=6, amax=60, L=0.64, w=0.07, hook=0.3, asym=0.35)]


def f_tiadau(i):
    P = TIADAU[i]
    rng = rng_of("kr_tiadau", i)
    seed = rng.randint(1 << 20)
    br = []
    n = P["n"]
    for j in range(n):
        u = j / (n - 1)
        c = 2 * u - 1
        a = math.radians(P["amax"]) * c + P.get("asym", 0) * 0.35 + rng.uniform(-0.07, 0.07)
        L = P["L"] * (0.42 + 0.58 * (1 - abs(c) ** 1.5)) * rng.uniform(0.85, 1.1)
        sgn = 1 if a >= 0 else -1
        x0, y0 = 0.30, 0.5 + 0.13 * math.sin(a)
        hk = P["hook"] * sgn * rng.uniform(0.6, 1.1)
        # đường giữa đi sang PHẢI: ang tính từ trục +x (y xuống), loe ra ngoài dần
        pts = []
        x, y = x0, y0
        for t in np.linspace(0, 1, 22):
            aa = a + sgn * 0.35 * t ** 1.3 * abs(c) + hk * max(0.0, (t - 0.65) / 0.35) ** 2
            pts.append((x, y))
            x += math.cos(aa) * L / 21
            y += math.sin(aa) * L / 21
        br.append((pts, taper(22, P["w"] * (0.75 + 0.4 * (1 - abs(c))), 0.95, 0.15)))
    bell = [(0.10 + 0.24 * t, 0.5) for t in np.linspace(0, 1, 12)]
    bell_r = [0.085 + 0.08 * t ** 1.5 for t in np.linspace(0, 1, 12)]

    def build(g):
        d = smin(circle(g, 0.12, 0.5, 0.095), stroke(g, bell, bell_r), 0.03)
        for pts, rads in br:
            d = smin(d, stroke(g, pts, rads), 0.035)
        return {"main": d + 0.003 * noise(g, seed, 7)}

    return Spec(build, "l", ay=0.5)


# ---------- vệt hút / tia văng: đầu tròn đậm ở +x, đuôi nhọn về -x, hơi cong ----------
VET = [dict(R=0.095, L=0.80, curve=0.06, p=1.15, wob=0.0),
       dict(R=0.085, L=0.78, curve=0.20, p=1.0, wob=0.0),
       dict(R=0.14, L=0.55, curve=0.05, p=0.85, wob=0.0),
       dict(R=0.07, L=0.86, curve=0.0, p=1.3, wob=0.05)]


def f_vet(i):
    P = VET[i]
    n = 30
    hx = 0.5 + P["L"] / 2 - P["R"]
    pts, rads = [], []
    for t in np.linspace(0, 1, n):
        x = hx - (P["L"] - P["R"]) * t
        y = 0.5 - P["curve"] * (t * t - t * 0.3) + P["wob"] * math.sin(t * math.pi * 2) * t
        pts.append((x, y))
        rads.append(max(0.003, P["R"] * (1 - t) ** P["p"]))

    def build(g):
        return {"main": smin(circle(g, hx, pts[0][1], P["R"]), stroke(g, pts, rads), 0.015)}

    return Spec(build, "c")


# ---------- cầu năng lượng cuộn: lõi tròn méo + vỏ nhiều múi cuộn cùng chiều, mép gợn ----------
CAU = [dict(n=6, curl=1.0, r=0.27, cut=False), dict(n=5, curl=1.4, r=0.26, cut=True),
       dict(n=8, curl=0.8, r=0.28, cut=False), dict(n=7, curl=1.2, r=0.25, cut=True)]


def f_cau(i):
    P = CAU[i]
    rng = rng_of("kr_cau", i)
    seed = rng.randint(1 << 20)
    side = 1 if i % 2 == 0 else -1
    a0 = rng.uniform(0, 2 * math.pi)
    arms = []
    for j in range(P["n"]):
        a = a0 + 2 * math.pi * j / P["n"] + rng.uniform(-0.15, 0.15)
        sx, sy = 0.5 + math.cos(a) * P["r"] * 0.75, 0.5 + math.sin(a) * P["r"] * 0.75
        L = rng.uniform(0.17, 0.24)
        pts = []
        x, y = sx, sy
        for t in np.linspace(0, 1, 18):
            aa = a + side * (0.55 + P["curl"] * t ** 1.2)  # hướng tiếp tuyến, quặp dần vào
            pts.append((x, y))
            x += math.cos(aa) * L / 17
            y += math.sin(aa) * L / 17
        arms.append((pts, taper(18, rng.uniform(0.07, 0.095), 1.0, 0.1)))
    sp = []
    if P["cut"]:
        th0 = rng.uniform(0, 2 * math.pi)
        for t in np.linspace(0, 1, 40):
            th = th0 + side * t * 1.6 * math.pi
            r = 0.05 + 0.15 * t
            sp.append((0.5 + math.cos(th) * r, 0.5 + math.sin(th) * r))
    cw = [0.004 + 0.014 * math.sin(math.pi * t) ** 0.7 for t in np.linspace(0, 1, 40)]

    def build(g):
        d = circle(g, 0.5, 0.5, P["r"]) + 0.012 * noise(g, seed, 4)
        for pts, rads in arms:
            d = smin(d, stroke(g, pts, rads), 0.03)
        d = d + 0.004 * noise(g, seed + 1, 11)
        out = {"main": d}
        if sp:
            out["cut"] = stroke(g, sp, cw)
        return out

    return Spec(build, "c")


# ======================================================================================================================
# bảng tên (hợp đồng): tên, hàm, số biến thể, có bản đặc không, gốc / hướng, điểm co lớp gợi ý (phần khung, trước khi xoay)
# ======================================================================================================================
TEN = [
    ("kr_khoi", f_khoi, 4, True, "giữa", (0.5, 0.5)),
    ("kr_khoinho", f_khoinho, 4, True, "giữa", (0.5, 0.5)),
    ("kr_khoiday", None, 4, False, "khớp kr_khoi_<i>", (0.5, 0.5)),
    ("kr_lua", f_lua, 4, True, "chân giữa đáy, ngọn lên", (0.5, 0.9)),
    ("kr_luakhoi", f_luakhoi, 4, True, "giữa", (0.5, 0.5)),
    ("kr_liem", f_liem, 4, True, "lưng +x, tâm ở chỗ dày", (0.5, 0.5)),
    ("kr_nham", f_nham, 4, True, "giữa", (0.5, 0.5)),
    ("kr_nhamgiot", f_nhamgiot, 4, True, "đầu tròn +x", (0.66, 0.5)),
    ("kr_mao", f_mao, 4, True, "chân giữa đáy, lưỡi lên", (0.5, 0.72)),
    ("kr_maolo", None, 4, True, "khớp kr_mao_<i>", (0.5, 0.72)),
    ("kr_khoinuoc", f_khoinuoc, 4, True, "giữa", (0.5, 0.45)),
    ("kr_dom", None, 4, False, "khớp kr_khoinuoc_<i>", (0.5, 0.5)),
    ("kr_giot", f_giot, 4, True, "đầu tròn +x", (0.64, 0.5)),
    ("kr_vanh", f_vanh, 2, True, "giữa (elip trên đất)", (0.5, 0.5)),
    ("kr_cung", f_cung, 4, True, "giữa (elip 3:1)", (0.5, 0.5)),
    ("kr_songam", f_songam, 4, True, "lõm trái, lồi phải", (0.5, 0.5)),
    ("kr_chop", f_chop, 4, True, "giữa", (0.5, 0.5)),
    ("kr_tiadau", f_tiadau, 4, True, "gốc trái giữa, toé +x", (0.055, 0.5)),
    ("kr_vet", f_vet, 4, True, "đầu tròn +x", (0.8, 0.5)),
    ("kr_cau", f_cau, 4, True, "giữa", (0.5, 0.5)),
    ("kr_luachum", f_luachum, 4, True, "giữa, ngọn lên", (0.5, 0.5)),
    ("kr_giotchum", f_giotchum, 4, True, "giữa, đầu giọt +x", (0.5, 0.5)),
]


def _save(path, rgb_gray, alpha, solid=False):
    a = np.clip(np.round(alpha * 255), 0, 255).astype(np.uint8)
    if solid:
        rgb = np.full(a.shape, 255, np.uint8)
    else:  # ngoài hình để xám phẳng (nén nhẹ, mép không viền tối khi lọc song tuyến)
        rgb = np.where(alpha > 0.002, rgb_gray, GRAY[0]).astype(np.uint8)
    Image.fromarray(np.dstack([rgb, rgb, rgb, a]), "RGBA").save(path, optimize=True)


def generate(only=None):
    os.makedirs(OUT, exist_ok=True)
    made = {}
    for name, fn, nv, has_solid, _, _ in TEN:
        if fn is None:
            continue
        need = {name, "kr_khoiday"} if name == "kr_khoi" else {name, "kr_maolo"} if name == "kr_mao" else \
            {name, "kr_dom"} if name == "kr_khoinuoc" else {name}
        if only and not (need & set(only)):
            continue
        for i in range(nv):
            seed = zlib.crc32(f"{name}_{i}".encode()) & 0xFFFF
            r = render(fn(i), seed)
            tex = r["tex"]
            _save(os.path.join(OUT, f"hat_{name}_{i}.png"), tex, r["van"])
            _save(os.path.join(OUT, f"hat_{name}s_{i}.png"), tex, r["solid"], solid=True)
            made[(name, i)] = True
            if name == "kr_khoi":
                _save(os.path.join(OUT, f"hat_kr_khoiday_{i}.png"), van_tex(seed + 11), r["aux"])
                made[("kr_khoiday", i)] = True
            if name == "kr_mao":
                _save(os.path.join(OUT, f"hat_kr_maolo_{i}.png"), tex, r["van_lo"])
                _save(os.path.join(OUT, f"hat_kr_maolos_{i}.png"), tex, r["solid_lo"], solid=True)
                made[("kr_maolo", i)] = True
            if name in ("kr_luachum", "kr_giotchum"):
                _save(os.path.join(OUT, f"hat_{name}l_{i}.png"), van_tex(seed + 17), r["aux"])
            if name == "kr_khoinuoc":
                _save(os.path.join(OUT, f"hat_kr_dom_{i}.png"), van_tex(seed + 13), r["aux"])
                made[("kr_dom", i)] = True
            print(f"  {name}_{i}", flush=True)
    return made


# ======================================================================================================================
# tờ xem: vẽ như game (bản đặc tô mực nở thêm vài px dưới, rồi bản vân nhuộm nhiều lớp thu nhỏ quanh điểm co)
# ======================================================================================================================
def hx(s):
    s = s.lstrip("#")
    return tuple(int(s[k:k + 2], 16) for k in (0, 2, 4))


# bảng tươi (người dùng 2026-11-18: màu phải tươi, hợp sân cát sáng, trời xanh, chì sáp tươi); ngoài -> lõi
FIRE = [hx("F0702A"), hx("FFA43A"), hx("FFD94A"), hx("FFF6D6")]
WATER = [hx("2B7FD0"), hx("4EB6F2"), hx("9FE0FF"), hx("F2FBFF")]
LAVA = [hx("8A3A22"), hx("F0702A"), hx("FFA43A"), hx("FFD94A")]
SMOKE = [hx("3A3532"), hx("6E6862"), hx("A39C94")]
SAND, DARK = hx("F3E2B8"), hx("2C3036")
KF = (1.0, 0.8, 0.6, 0.38)  # cỡ các lớp màu so với lớp ngoài (như LobeF của HatLua)

_SPR = {}


def spr(name, i, solid=False):
    key = (name, i, solid)
    if key not in _SPR:
        f = os.path.join(OUT, f"hat_{name}{'s' if solid else ''}_{i}.png")
        _SPR[key] = Image.open(f).convert("RGBA") if os.path.exists(f) else None
    return _SPR[key]


_RS = {}


def _sized(im, size):
    key = (id(im), size)
    if key not in _RS:
        _RS[key] = np.asarray(im.resize((size, size), Image.LANCZOS), np.float32) / 255
    return _RS[key]


def _composite(dst, src, x, y):
    """dán src (mảng float HxWx4, màu chưa nhân alpha) lên dst (float HxWx3) tại góc (x, y), cắt phần ngoài khung."""
    H, W = dst.shape[:2]
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4]
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + s[..., :3] * a


class Scene:
    def __init__(self, w, h, bg):
        self.a = np.ones((h, w, 3), np.float32) * (np.array(bg, np.float32) / 255)
        self.items = []

    def add(self, im, col, cx, cy, size, ang=0.0, alpha=1.0, layer=0.0):
        if im is not None and size >= 2:
            self.items.append((layer, len(self.items), im, col, cx, cy, size, ang, alpha))

    def particle(self, name, i, cx, cy, size, pal, k=KF, pivot=(0.5, 0.5), ang=0.0, ink=5, layer=0.0, alpha=1.0,
                 ink_layer=None, step=1.0):
        """một hạt như HatLua: bản đặc tô mực (cỡ + ink) ở ink_layer, rồi từng lớp màu (layer + j*step) thu nhỏ quanh pivot."""
        if ink is not None:
            self.add(spr(name, i, True), INK, cx, cy, size + ink, ang, alpha, layer if ink_layer is None else ink_layer)
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        for j, (col, kk) in enumerate(zip(pal, k)):
            ox, oy = (pivot[0] - 0.5) * size * (1 - kk), (pivot[1] - 0.5) * size * (1 - kk)
            rx, ry = ox * c + oy * s, -ox * s + oy * c
            self.add(spr(name, i), col, cx + rx, cy + ry, size * kk, ang, alpha, layer + 1 + j * step)

    def render(self):
        for layer, _, im, col, cx, cy, size, ang, alpha in sorted(self.items, key=lambda t: (t[0], t[1])):
            a = _sized(im, int(round(size))).copy()
            a[..., :3] *= np.array(col, np.float32) / 255
            a[..., 3] *= alpha
            if ang:
                pim = Image.fromarray((a * 255).astype(np.uint8), "RGBA").rotate(ang, resample=Image.BICUBIC, expand=True)
                a = np.asarray(pim, np.float32) / 255
            h, w = a.shape[:2]
            _composite(self.a, a, int(round(cx - w / 2)), int(round(cy - h / 2)))
        return Image.fromarray(np.clip(self.a * 255, 0, 255).astype(np.uint8), "RGB")


def _font(sz):
    for f in ("arial.ttf", "segoeui.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def tile(name, i, T, bg):
    """một ô: hình vẽ như game theo kiểu của từng tên."""
    sc = Scene(T, T, bg)
    c = T / 2
    D = T * 0.92
    if name == "kr_khoi":
        sc.particle(name, i, c, c, D, [SMOKE[1]], k=(1,), layer=0)
        sc.add(spr("kr_khoiday", i), SMOKE[0], c, c, D, layer=5)
    elif name == "kr_khoiday":
        sc.add(spr("kr_khoi", i), SMOKE[2], c, c, D, layer=0)
        sc.add(spr("kr_khoiday", i), SMOKE[0], c, c, D, layer=1)
    elif name == "kr_khoinho":
        sc.particle(name, i, c, c, D, [SMOKE[1]], k=(1,))
    elif name == "kr_lua":
        sc.particle(name, i, c, c, D, FIRE, pivot=(0.5, 0.9))
    elif name == "kr_luachum":
        sc.particle(name, i, c, c, D, [FIRE[1]], k=(1,))
        sc.add(spr("kr_luachuml", i), FIRE[2], c, c, D, layer=5)
    elif name in ("kr_luakhoi", "kr_cau"):
        sc.particle(name, i, c, c, D, FIRE)
    elif name == "kr_liem":
        sc.particle(name, i, c, c, D, FIRE[1:], k=(1, 0.74, 0.46))
    elif name == "kr_chop":
        sc.particle(name, i, c, c, D, FIRE[1:], k=(1, 0.72, 0.42) if i < 2 else (1, 0.62, 0.3))
    elif name == "kr_tiadau":
        sc.particle(name, i, c, c, D, FIRE, pivot=(0.055, 0.5))
    elif name in ("kr_nham", "kr_nhamgiot"):
        sc.particle(name, i, c, c, D, LAVA, k=(1, 0.8, 0.56, 0.32), pivot=dict((t[0], t[5]) for t in TEN)[name])
    elif name in ("kr_mao", "kr_maolo"):
        sc.particle(name, i, c, c, D, WATER, k=(1, 0.82, 0.6, 0.36), pivot=(0.5, 0.72))
    elif name == "kr_khoinuoc":
        sc.particle(name, i, c, c, D, WATER[:3], k=(1, 0.8, 0.55), pivot=(0.5, 0.45))
        sc.add(spr("kr_dom", i), WATER[3], c, c, D, layer=9)
    elif name == "kr_dom":
        sc.add(spr("kr_khoinuoc", i), WATER[1], c, c, D, layer=0)
        sc.add(spr("kr_dom", i), WATER[3], c, c, D, layer=1)
    elif name == "kr_giot":
        sc.particle(name, i, c, c, D, WATER[:3], k=(1, 0.75, 0.48), pivot=(0.64, 0.5))
    elif name == "kr_giotchum":
        sc.particle(name, i, c, c, D, [WATER[1]], k=(1,))
        sc.add(spr("kr_giotchuml", i), WATER[2], c, c, D, layer=5)
    elif name == "kr_vanh":
        sc.particle(name, i, c, c, D, [WATER[1]], k=(1,))
    elif name == "kr_cung":
        sc.particle(name, i, c, c, D, [FIRE[1]], k=(1,), ink=None)
    elif name == "kr_songam":
        sc.particle(name, i, c, c, D, [WATER[1], WATER[2], WATER[3]], k=(1, 0.72, 0.42))
    elif name == "kr_vet":
        sc.particle(name, i, c, c, D, FIRE[1:], k=(1, 0.7, 0.42), pivot=(0.8, 0.5))
    return sc.render()


# ---------- cảnh ghép thử (toạ độ 400 x 400, vẽ ra cỡ S) ----------
def scene_khoi(S, bg):
    f = S / 400
    sc = Scene(S, S, bg)
    P = [("kr_khoi", 3, 215, 125, 150, 0.9), ("kr_khoinho", 0, 152, 122, 110, 0.95), ("kr_khoi", 1, 125, 190, 160, 0.6),
         ("kr_khoi", 2, 275, 175, 165, 0.6), ("kr_khoi", 0, 195, 235, 235, 0.25), ("kr_khoinho", 2, 290, 270, 105, 0.15),
         ("kr_khoinho", 1, 95, 280, 95, 0.1)]
    for j, (n, i, x, y, s, age) in enumerate(P):  # mực của mọi hạt dưới cùng; rồi từng hạt (sau -> trước): màu nền, bóng dưới
        fill = tuple(int(SMOKE[1][k] + (SMOKE[2][k] - SMOKE[1][k]) * age) for k in range(3))
        shade = tuple(int(SMOKE[0][k] + (SMOKE[1][k] - SMOKE[0][k]) * age) for k in range(3))
        sc.add(spr(n, i, True), INK, x * f, y * f, s * f + 5, layer=0)
        sc.add(spr(n, i), fill, x * f, y * f, s * f, layer=1 + j * 0.01)
        if n == "kr_khoi":
            sc.add(spr("kr_khoiday", i), shade, x * f, y * f, s * f, layer=1 + j * 0.01 + 0.005)
    return sc.render()


def scene_lua(S, bg):
    f = S / 400
    sc = Scene(S, S, bg)
    base = 345
    for n, i, x, s, ang in [("kr_lua", 0, 200, 300, 0), ("kr_lua", 1, 140, 215, 9), ("kr_lua", 2, 262, 235, -7),
                            ("kr_lua", 3, 105, 150, 14), ("kr_lua", 1, 300, 160, -12)]:
        sc.particle(n, i, x * f, (base - s * 0.445) * f, s * f, FIRE, pivot=(0.5, 0.9), ang=ang, ink_layer=0, layer=0)
    # chùm đốm lửa bay trên ngọn: mực + một màu + bản lõi (không co lớp quanh tâm)
    sc.particle("kr_luachum", 1, 215 * f, 62 * f, 95 * f, [FIRE[1]], k=(1,), layer=10)
    sc.add(spr("kr_luachuml", 1), FIRE[2], 215 * f, 62 * f, 95 * f, layer=12)
    return sc.render()


def scene_no(S, bg):
    f = S / 400
    sc = Scene(S, S, bg)
    sc.particle("kr_cung", 1, 200 * f, 322 * f, 380 * f, [FIRE[1]], k=(1,), ink=None, layer=0)
    for j, (i, x, y, s) in enumerate([(1, 125, 165, 165), (3, 278, 150, 175), (2, 200, 92, 195), (0, 118, 248, 140), (2, 288, 245, 140)]):
        sc.add(spr("kr_khoi", i, True), INK, x * f, y * f, s * f + 5, layer=2)
        sc.add(spr("kr_khoi", i), SMOKE[1], x * f, y * f, s * f, layer=3 + j * 0.01)
        sc.add(spr("kr_khoiday", i), SMOKE[0], x * f, y * f, s * f, layer=3 + j * 0.01 + 0.005)
    for j, (phi, d, s, i, lay) in enumerate([(-145, 118, 92, 0, 6), (-80, 128, 100, 1, 6), (-25, 120, 86, 3, 6), (30, 112, 70, 2, 20),
                                             (150, 110, 74, 3, 20), (95, 92, 62, 0, 20)]):
        x, y = 200 + math.cos(math.radians(phi)) * d, 222 + math.sin(math.radians(phi)) * d * 0.8
        sc.particle("kr_liem", i, x * f, y * f, s * f, FIRE[1:], k=(1, 0.74, 0.46), ang=-phi, layer=lay)
    sc.particle("kr_luakhoi", 0, 200 * f, 220 * f, 215 * f, FIRE, layer=10)
    sc.particle("kr_chop", 1, 196 * f, 212 * f, 92 * f, FIRE[2:], k=(1, 0.55), layer=30)
    sc.particle("kr_chop", 3, 250 * f, 176 * f, 52 * f, [FIRE[3]], k=(1,), layer=34)
    return sc.render()


def scene_nuoc(S, bg):
    f = S / 400
    sc = Scene(S, S, bg)
    sc.particle("kr_vanh", 0, 200 * f, 330 * f, 360 * f, [WATER[1]], k=(1,), layer=0)
    sc.particle("kr_mao", 0, 200 * f, (338 - 300 * 0.445) * f, 300 * f, WATER, k=(1, 0.82, 0.6, 0.36), pivot=(0.5, 0.72), layer=5)
    for i, x, y, s, ang in [(0, 75, 150, 80, 25), (1, 330, 120, 74, -150), (3, 280, 55, 56, 0), (2, 110, 60, 50, 0)]:
        sc.particle("kr_khoinuoc", i, x * f, y * f, s * f, WATER[:3], k=(1, 0.8, 0.55), pivot=(0.5, 0.45), ang=ang, layer=10)
        sc.add(spr("kr_dom", i), WATER[3], x * f, y * f, s * f, ang, layer=14)
    for i, x, y, s, ang in [(0, 40, 235, 62, 150), (1, 360, 220, 60, 35), (2, 200, 25, 46, 90), (3, 335, 175, 50, 60),
                            (0, 60, 100, 40, 130)]:
        sc.particle("kr_giot", i, x * f, y * f, s * f, WATER[:3], k=(1, 0.75, 0.48), pivot=(0.64, 0.5), ang=ang, layer=15)
    sc.particle("kr_giotchum", 1, 365 * f, 290 * f, 70 * f, [WATER[1]], k=(1,), ang=20, layer=15)
    sc.add(spr("kr_giotchuml", 1), WATER[2], 365 * f, 290 * f, 70 * f, 20, layer=17)
    return sc.render()


def scene_tia(S, bg):
    f = S / 400
    sc = Scene(S, S, bg)
    for y, pal, i in [(115, FIRE, 0), (290, WATER, 2)]:
        # thân tia: dải phẳng nhiều lớp (thay cho mảng liền MBand của game), đầu tia ở cuối
        ex = 235
        for col, w in [(INK, 46), (pal[0], 38), (pal[1], 28), (pal[2], 17), (pal[3], 7)]:
            band = np.ones((int(w * f), int(ex * f), 4), np.float32)
            band[..., :3] *= np.array(col, np.float32) / 255
            _composite(sc.a, band, 0, int((y - w / 2) * f))
        sc.particle("kr_tiadau", i, (ex - 10 + 190 * (0.5 - 0.055)) * f, y * f, 190 * f, pal, pivot=(0.055, 0.5), layer=5)
        for j, (dx, dy, s, ang) in enumerate([(95, -70, 55, 40), (120, 60, 50, -35), (150, -10, 45, 0), (60, 75, 40, -60)]):
            sc.particle("kr_vet", j, (ex + dx) * f, (y + dy) * f, s * f, pal[1:], k=(1, 0.7, 0.42), pivot=(0.8, 0.5), ang=ang, layer=8)
    return sc.render()


def scene_hut(S, bg):
    """14 hạt kr_vet trên ba nhánh xoắn ốc hút vào một kr_cau (tụ cầu): xa thì to, gần lõi thì nhỏ, đầu tròn chĩa theo hướng bay."""
    f = S / 400
    sc = Scene(S, S, bg)
    cx, cy = 200, 200
    for arm in range(3):
        for k in range(5 if arm else 4):
            th = arm * 2 * math.pi / 3 + k * 0.62
            r = 182 - k * 27
            x, y = cx + math.cos(th) * r, cy + math.sin(th) * r * 0.9
            # tiếp tuyến đường xoắn r = a - b*theta (đi vào): hướng = -dr/dtheta * e_r + r * e_theta
            er, et = (math.cos(th), math.sin(th)), (-math.sin(th), math.cos(th))
            vx, vy = -er[0] * 1.0 - et[0] * 0.95, -er[1] * 1.0 - et[1] * 0.95
            ang = -math.degrees(math.atan2(vy, vx))
            s = 44 + 0.3 * (r - 70)
            sc.particle("kr_vet", (arm + k) % 4, x * f, y * f, s * f, FIRE[:3] if k < 2 else FIRE[1:], k=(1, 0.7, 0.42), pivot=(0.8, 0.5),
                        ang=ang, layer=0, ink_layer=-1)
    sc.particle("kr_cau", 0, cx * f, cy * f, 150 * f, FIRE, layer=10)
    return sc.render()


def scene_nham_songam(S, bg):
    f = S / 400
    sc = Scene(S, S, bg)
    for j, (x, s) in enumerate([(95, 120), (165, 170), (245, 220)]):
        sc.particle("kr_songam", j % 4, x * f, 120 * f, s * f, [WATER[1], WATER[2], WATER[3]], k=(1, 0.72, 0.42), alpha=1 - 0.22 * j,
                    layer=j * 5)
    sc.particle("kr_nham", 0, 170 * f, 300 * f, 190 * f, LAVA, k=(1, 0.8, 0.56, 0.32), layer=20)
    sc.particle("kr_nham", 2, 280 * f, 315 * f, 130 * f, LAVA, k=(1, 0.8, 0.56, 0.32), layer=20, ink_layer=20)
    for i, x, y, s, ang in [(0, 300, 230, 80, 30), (1, 70, 245, 70, 160), (3, 360, 290, 55, -20)]:
        sc.particle("kr_nhamgiot", i, x * f, y * f, s * f, LAVA, k=(1, 0.8, 0.56, 0.32), pivot=(0.66, 0.5), ang=ang, layer=30)
    return sc.render()


SCENES = [("Cụm khói (7 hạt + bóng dưới)", scene_khoi), ("Ngọn lửa (5 hạt kr_lua chồng)", scene_lua),
          ("Vụ nổ (chớp, khối lửa, liềm, cung, khói)", scene_no), ("Nước toé (mão, khối, đốm, giọt, vành)", scene_nuoc),
          ("Cuối tia: kr_tiadau + kr_vet", scene_tia), ("Hút xoắn: 14 kr_vet vào kr_cau", scene_hut),
          ("Sóng âm lan + dung nham", scene_nham_songam)]


def sheet(names, path):
    T, gap, per_row = 150, 6, 3
    lab = _font(15)
    big = _font(22)
    rows = []
    groups = [t for t in TEN if t[0] in names]
    for k in range(0, len(groups), per_row):
        rows.append(groups[k:k + per_row])
    W = per_row * (4 * (T + gap) + 18) + 20
    blocks = []
    for bg, title in ((SAND, "Nền sân sáng"), (DARK, "Nền tối")):
        H = 34 + len(rows) * (T + 26)
        im = Image.new("RGB", (W, H), bg)
        d = ImageDraw.Draw(im)
        tc = (40, 30, 20) if bg == SAND else (230, 230, 230)
        d.text((12, 6), title, font=big, fill=tc)
        for r, row in enumerate(rows):
            y = 34 + r * (T + 26)
            for c, (name, _, nv, _, how, _) in enumerate(row):
                x = 12 + c * (4 * (T + gap) + 18)
                d.text((x, y), f"{name}  ({how})", font=lab, fill=tc)
                for i in range(nv):
                    if spr(name, i) is None and name not in ("kr_khoiday", "kr_dom"):
                        continue
                    im.paste(tile(name, i, T, bg), (x + i * (T + gap), y + 20))
        blocks.append(im)
    S = 300
    scn = [(t, fn) for t, fn in SCENES]
    if set(names) != {t[0] for t in TEN}:
        scn = []
    for bg in (SAND, DARK):
        if not scn:
            break
        cols = max(1, (W - 20) // (S + 10))
        nrow = (len(scn) + cols - 1) // cols
        im = Image.new("RGB", (W, 34 + nrow * (S + 30)), bg)
        d = ImageDraw.Draw(im)
        tc = (40, 30, 20) if bg == SAND else (230, 230, 230)
        d.text((12, 6), "Ghép thử (lớp vẽ như game)", font=big, fill=tc)
        for k, (title, fn) in enumerate(scn):
            x, y = 12 + (k % cols) * (S + 10), 34 + (k // cols) * (S + 30)
            d.text((x, y), title, font=lab, fill=tc)
            im.paste(fn(S, bg), (x, y + 20))
        blocks.append(im)
    # phép thử hình bóng: tô đen cả hình
    sil = []
    for name, _, nv, _, _, _ in groups:
        for i in range(nv):
            im = spr(name, i)
            if im is not None:
                sil.append(im)
    s = 56
    cols = (W - 20) // (s + 4)
    im = Image.new("RGB", (W, 34 + ((len(sil) + cols - 1) // cols) * (s + 4)), SAND)
    d = ImageDraw.Draw(im)
    d.text((12, 6), "Hình bóng (tô đen cả hình)", font=big, fill=(40, 30, 20))
    for k, sp_ in enumerate(sil):
        a = np.asarray(sp_.resize((s, s), Image.LANCZOS), np.float32)[..., 3:4] / 255
        bgv = np.array(SAND, np.float32)
        tilea = bgv * (1 - a) + np.array(INK, np.float32) * a
        im.paste(Image.fromarray(tilea.astype(np.uint8), "RGB"), (12 + (k % cols) * (s + 4), 34 + (k // cols) * (s + 4)))
    blocks.append(im)
    H = sum(b.height for b in blocks)
    out = Image.new("RGB", (W, H), SAND)
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    out.save(path, optimize=True)
    print("tờ xem ->", path, out.size)


def xuat():
    os.makedirs(UNITY, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(OUT)):
        if f.startswith("hat_kr_") and f.endswith(".png"):
            shutil.copyfile(os.path.join(OUT, f), os.path.join(UNITY, f))
            n += 1
    print(n, "ảnh hat_kr_* ->", UNITY)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    only = args or None
    if "--chi-xuat" not in flags:
        generate(only)
        names = only or [t[0] for t in TEN]
        if only:
            names = list(dict.fromkeys(names + [x for n in names for x in
                                                {"kr_khoi": ["kr_khoiday"], "kr_mao": ["kr_maolo"], "kr_khoinuoc": ["kr_dom"]}.get(n, [])]))
        sheet(names, os.path.join(OUT, "xem_thu.png" if only else "xem.png"))
    if "--xuat" in flags or "--chi-xuat" in flags:
        xuat()


if __name__ == "__main__":
    main()
