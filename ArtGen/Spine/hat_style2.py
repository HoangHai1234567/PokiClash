"""Bản mẫu bộ hình VFX theo style mới (người dùng chọn 2026-11-19, skill vfx-petclash mục 1c).

Người dùng: "đổi kiểu lửa/nước/nổ trong game ... theo link ảnh tôi gửi, rút ra kiểu style này, và tôi muốn vfx mượt hơn nữa
nghĩa là có thể tăng frame lên". Bổ sung: "mấy ảnh gai lá/gai sắt đâm lên ... xấu quá, cần sửa lại hoặc đổi sang kiểu khác".

Style (học từ 4 tờ mẫu ở ArtGen/StyleRefs/vfx_mau, KHÔNG chép hình của họ):
- không viền mực; mép là tông đậm nhất của chính khối;
- 3–4 tông phẳng xếp lớp + mảng sáng bầu dục lệch lên trên;
- nước tô chuyển màu lam đậm -> ngọc lam, bọt trắng ở mào, đốm trắng nhỏ, vân sáng mảnh;
- lửa lưỡi nhọn quặp vàng -> cam -> đỏ cam, quầng mềm đỏ cam alpha 0,25–0,4;
- khói xám nâu hơi trong, tối ở đáy múi; màu tươi;
- mượt: mọi thông số là hàm liên tục theo thời gian, nội suy PCHIP, khung nào cũng đổi hình một chút.

Mọi hình 256 x 256 RGBA, nền trong, tô sẵn màu (game nhuộm trắng). Vẽ ở 512 rồi thu 2 lần (khử răng cưa).
Ra ArtGen/Spine/hat_style2/:
    <bo>_<i>.png, <bo>_to.png (lưới 4 cột, đọc trái->phải, trên->dưới)   bo = no, nuoctoe, lua, khoi, loc, gaila, gaisat
    h_luoilua_0..3, h_quang, h_giot_0..3, h_khoi_0..3, h_tiachop_0..1, h_vetlua_0..3
    xem_<bo>.gif (30 khung/giây, nền sân), xem_tong.png (ảnh mẫu | bản này)

    py -3 -I ArtGen/Spine/hat_style2.py              # sinh tất cả
    py -3 -I ArtGen/Spine/hat_style2.py no lua hat   # chỉ sinh vài bộ (xem_tong vẫn dựng lại từ file đã có)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.interpolate import PchipInterpolator

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "hat_style2")
REFS = os.path.normpath(os.path.join(HERE, "..", "StyleRefs", "vfx_mau"))
N = 256
SS = 2
S = N * SS
f32 = np.float32
YY, XX = np.mgrid[0:S, 0:S].astype(f32) + 0.5
TAU = math.tau


# ----------------------------------------------------------------------------------------------------------- công cụ chung
def C(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], f32)


def mix(a, b, t):
    return a + (b - a) * t


def ramp(stops, v):
    """stops = [(v0, màu), ...] tăng dần; v mảng -> (..., 3)"""
    v = np.asarray(v, f32)
    out = np.zeros(v.shape + (3,), f32)
    vs = [s[0] for s in stops]
    cs = [C(s[1]) if isinstance(s[1], str) else s[1] for s in stops]
    for ch in range(3):
        out[..., ch] = np.interp(v, vs, [c[ch] for c in cs])
    return out


def kf(keys):
    ts, vs = zip(*keys)
    f = PchipInterpolator(ts, vs)
    lo, hi = ts[0], ts[-1]
    return lambda t: float(f(min(max(t, lo), hi)))


def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


class Cv:
    """tấm vẽ S x S, màu nhân sẵn alpha"""

    def __init__(self):
        self.p = np.zeros((S, S, 4), f32)

    def paint(self, cov, col, a=1.0):
        k = np.clip(cov * a, 0, 1)
        if not np.any(k > 0):
            return
        k = k[..., None]
        col = np.broadcast_to(np.asarray(col, f32), (S, S, 3)) if np.ndim(col) == 1 else col
        self.p[..., :3] = col * k + self.p[..., :3] * (1 - k)
        self.p[..., 3:] = k + self.p[..., 3:] * (1 - k)

    def over(self, other, a=1.0):
        q = other.p * a
        self.p = q + self.p * (1 - q[..., 3:4])

    def mul_alpha(self, a):
        self.p *= a

    def img(self):
        p = self.p.reshape(N, SS, N, SS, 4).mean((1, 3))
        a = p[..., 3:4]
        rgb = np.where(a > 1e-5, p[..., :3] / np.maximum(a, 1e-5), 0)
        out = np.concatenate([rgb, a], -1)
        return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


def cov(d, aa=1.0):
    return np.clip(0.5 - d / aa, 0, 1)


def sd_ell(cx, cy, rx, ry, ang=0.0):
    x = XX - cx
    y = YY - cy
    if ang:
        c, s = math.cos(ang), math.sin(ang)
        x, y = c * x + s * y, -s * x + c * y
    rx = max(rx, 1e-3)
    ry = max(ry, 1e-3)
    k0 = np.sqrt((x / rx) ** 2 + (y / ry) ** 2)
    k1 = np.sqrt((x / (rx * rx)) ** 2 + (y / (ry * ry)) ** 2)
    return k0 * (k0 - 1) / np.maximum(k1, 1e-6)


def sd_circ(cx, cy, r):
    return np.hypot(XX - cx, YY - cy) - r


def smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


Q = 2  # vẽ đa giác ở 2*S rồi thu


def polys_cov(polys):
    """hợp nhiều đa giác (toạ độ S) -> độ phủ S x S"""
    big = Image.new("L", (S * Q, S * Q), 0)
    dr = ImageDraw.Draw(big)
    for pts in polys:
        if len(pts) >= 3:
            dr.polygon([(x * Q, y * Q) for x, y in pts], fill=255)
    a = np.asarray(big, f32) / 255
    return a.reshape(S, Q, S, Q).mean((1, 3))


def lines_cov(lines, width):
    big = Image.new("L", (S * Q, S * Q), 0)
    dr = ImageDraw.Draw(big)
    for pts in lines:
        if len(pts) >= 2:
            dr.line([(x * Q, y * Q) for x, y in pts], fill=255, width=max(1, int(round(width * Q))), joint="curve")
    a = np.asarray(big, f32) / 255
    return a.reshape(S, Q, S, Q).mean((1, 3))


def inner_dist(c):
    """khoảng cách vào trong (px ở S) tính từ mép của vùng phủ c"""
    m = c >= 0.5
    d = ndimage.distance_transform_edt(m).astype(f32) - 0.5
    edge = (c > 0) & (c < 1)
    d[edge] = np.minimum(d[edge], c[edge] - 0.5)
    return d


def ribbon(center, widths):
    """đường giữa (n,2) + bề rộng (n) -> đa giác dải"""
    p = np.asarray(center, f32)
    t = np.gradient(p, axis=0)
    t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-6)
    nrm = np.stack([-t[:, 1], t[:, 0]], 1)
    w = np.asarray(widths, f32)[:, None] * 0.5
    left = p - nrm * w
    right = p + nrm * w
    return [tuple(v) for v in left] + [tuple(v) for v in right[::-1]]


def polyline_frame(pts):
    """khoảng cách tới đường gấp khúc, tham số u (0..1 theo độ dài), lệch ngang q có dấu (dương = bên phải hướng đi)"""
    p = np.asarray(pts, f32)
    seg = p[1:] - p[:-1]
    ln = np.linalg.norm(seg, axis=1)
    cum = np.concatenate([[0], np.cumsum(ln)])
    tot = max(cum[-1], 1e-6)
    best = np.full((S, S), 1e9, f32)
    U = np.zeros((S, S), f32)
    Qd = np.zeros((S, S), f32)
    for i in range(len(seg)):
        ax, ay = p[i]
        bx, by = seg[i]
        l2 = max(bx * bx + by * by, 1e-6)
        h = np.clip(((XX - ax) * bx + (YY - ay) * by) / l2, 0, 1)
        dx = XX - ax - h * bx
        dy = YY - ay - h * by
        d = np.hypot(dx, dy)
        m = d < best
        best = np.where(m, d, best)
        U = np.where(m, (cum[i] + h * ln[i]) / tot, U)
        Qd = np.where(m, (bx * dy - by * dx) / math.sqrt(l2), Qd)
    return best, U, Qd


def angle_curve(x0, y0, length, ang_fn, n=48):
    """đường cong từ (x0,y0), góc (độ, toạ độ màn hình: -90 = lên) theo s∈[0,1]"""
    pts = [(x0, y0)]
    ds = length / (n - 1)
    x, y = x0, y0
    for k in range(1, n):
        s = (k - 0.5) / (n - 1)
        a = math.radians(ang_fn(s))
        x += math.cos(a) * ds
        y += math.sin(a) * ds
        pts.append((x, y))
    return np.array(pts, f32)


def tnoise(h, w, sy, sx, seed):
    """nhiễu lặp liền (tuần hoàn cả hai chiều), độ lệch chuẩn 1"""
    r = np.random.default_rng(seed).standard_normal((h, w))
    ky = np.fft.fftfreq(h)[:, None]
    kx = np.fft.fftfreq(w)[None, :]
    g = np.exp(-2 * np.pi ** 2 * ((sy * ky) ** 2 + (sx * kx) ** 2))
    n = np.real(np.fft.ifft2(np.fft.fft2(r) * g))
    return ((n - n.mean()) / (n.std() + 1e-9)).astype(f32)


def nsamp(nz, x, y):
    return ndimage.map_coordinates(nz, [y, x], order=1, mode="grid-wrap").astype(f32)


def star_pts(cx, cy, R, n, inner, rot, rng, jit=0.25):
    pts = []
    lens = [R * (1 - jit * rng.random()) for _ in range(n)]
    for k in range(2 * n):
        a = rot + math.pi * k / n
        r = lens[k // 2] if k % 2 == 0 else R * inner
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def clip_half(pts, a, b, c):
    """giữ phần a*x + b*y + c <= 0 của đa giác"""
    out = []
    n = len(pts)
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        fp = a * p[0] + b * p[1] + c
        fq = a * q[0] + b * q[1] + c
        if fp <= 0:
            out.append(p)
        if (fp <= 0) != (fq <= 0):
            t = fp / (fp - fq)
            out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return out


# ---------------------------------------------------------------------------------------------------- múi (nổ, khói, bụi)
def paint_lobe(cv, cx, cy, rx, ry, cols, rot=0.0, clip=None, bite=None, hi=(0.0, 0.0, 1.0), a=1.0, mid=(0.03, 0.13, 0.90, 0.76)):
    """một múi 3 tông: nền (tông đậm, cũng là mép) -> tông giữa lệch lên -> mảng sáng bầu dục lệch lên trái.
    bite = (bx, by, br): khoét lõm thành mảnh khuyết."""
    d0 = sd_ell(cx, cy, rx, ry, rot)
    if bite is not None and bite[2] > 0.5:
        d0 = np.maximum(d0, -sd_ell(bite[0], bite[1], bite[2], bite[2] * 0.92))
    c0 = cov(d0)
    if clip is not None:
        c0 = c0 * clip
    cv.paint(c0, cols[0], a)
    hx, hy, hs = hi
    d1 = np.maximum(sd_ell(cx - mid[0] * rx, cy - mid[1] * ry, mid[2] * rx, mid[3] * ry, rot), d0)
    cv.paint(cov(d1) * (1 if clip is None else clip), cols[1], a)
    # mảng sáng hình hạt đậu: bầu dục trừ một bầu dục lệch xuống phải
    ex, ey = cx + (hx - 0.14) * rx, cy + (hy - 0.30) * ry
    ea, eb = 0.56 * rx * hs, 0.34 * ry * hs
    d2 = sd_ell(ex, ey, ea, eb, rot - 0.18)
    d2 = np.maximum(d2, -sd_ell(ex + 0.30 * ea, ey + 0.75 * eb, ea * 0.85, eb * 0.75, rot - 0.18))
    d2 = np.maximum(d2, d0)
    cv.paint(cov(d2) * (1 if clip is None else clip), cols[2], a)


def ground_clip(yg):
    return np.clip(yg - YY + 0.5, 0, 1)


# =========================================================================================================== 1. NỔ 16 khung
HEAT = [(0.00, ["#3E2C31", "#5B4041", "#7D5A50"]),
        (0.33, ["#533A3D", "#7A4B40", "#EA4A1F"]),
        (0.66, ["#7A4B40", "#EE4C1F", "#FF9E1F"]),
        (1.00, ["#EE4A1E", "#FF9E1F", "#FFE13A"])]


def heat_cols(h):
    h = min(max(h, 0.0), 1.0)
    for (h0, c0), (h1, c1) in zip(HEAT[:-1], HEAT[1:]):
        if h <= h1:
            t = (h - h0) / (h1 - h0)
            return [mix(C(a), C(b), t) for a, b in zip(c0, c1)]
    return [C(x) for x in HEAT[-1][1]]


NO_LOBES = [  # (lx, ly, rx, ry) theo bán kính nấm; vẽ từ sau ra trước (trên -> dưới)
    (0.08, -0.80, 0.34, 0.25), (-0.32, -0.66, 0.36, 0.26), (0.46, -0.58, 0.31, 0.23),
    (-0.66, -0.30, 0.32, 0.25), (-0.22, -0.36, 0.38, 0.27), (0.24, -0.32, 0.37, 0.27), (0.66, -0.24, 0.31, 0.24),
    (-0.80, 0.04, 0.26, 0.20), (-0.44, 0.02, 0.34, 0.24), (0.02, 0.05, 0.37, 0.25), (0.46, 0.06, 0.34, 0.23),
    (0.84, 0.09, 0.25, 0.18)]


def no_frames(n=16):
    YG = 0.86 * S
    cx = 0.5 * S
    T = lambda i: i / (n - 1)
    f = 1 / (n - 1)
    R = kf([(0, .07), (1 * f, .12), (2 * f, .175), (3 * f, .215), (4 * f, .24), (5 * f, .25), (6 * f, .255), (8 * f, .262),
            (10 * f, .272), (12 * f, .29), (14 * f, .30), (1, .305)])
    CY = kf([(0, .855), (2 * f, .85), (3 * f, .835), (4 * f, .80), (5 * f, .70), (6 * f, .61), (7 * f, .555), (8 * f, .53),
             (10 * f, .52), (11 * f, .55), (12 * f, .585), (14 * f, .60), (1, .60)])
    HT = kf([(0, 1), (5 * f, 1), (6 * f, .86), (7 * f, .64), (8 * f, .44), (9 * f, .27), (10 * f, .12), (11 * f, .02), (1, 0)])
    SX = kf([(0, 1.12), (4 * f, 1.05), (6 * f, .93), (8 * f, .97), (10 * f, 1.02), (12 * f, 1.08), (1, 1.12)])
    SY = kf([(0, .88), (4 * f, .95), (6 * f, 1.05), (9 * f, 1.0), (12 * f, .82), (1, .78)])
    SP = kf([(0, 0), (9 * f, 0), (11 * f, .07), (13 * f, .18), (1, .30)])
    BT = kf([(0, 0), (10 * f, 0), (11 * f, .28), (12 * f, .6), (13 * f, .92), (14 * f, 1.25), (1, 1.6)])
    AL = kf([(0, 1), (12 * f, 1), (13 * f, .92), (14 * f, .78), (1, .55)])
    STAR = kf([(0, .045), (1 * f, .09), (2 * f, .145), (3 * f, .165), (4 * f, .1), (5 * f, .0), (1, 0)])
    GW = kf([(0, 0), (1 * f, 0), (2 * f, .16), (3 * f, .30), (4 * f, .36), (5 * f, .30), (6 * f, 0), (1, 0)])   # nêm đất kem
    GD = kf([(0, .2), (4 * f, .22), (5 * f, .30), (6 * f, .355), (7 * f, .39), (8 * f, .415), (9 * f, .43), (10 * f, .44), (1, .44)])
    GR = kf([(0, 0), (3 * f, 0), (4 * f, .034), (5 * f, .042), (6 * f, .040), (7 * f, .034), (8 * f, .026), (9 * f, .017),
             (10 * f, .008), (11 * f, 0), (1, 0)])
    GL = kf([(0, 0), (6 * f, 0), (7 * f, .3), (8 * f, .7), (9 * f, 1.0), (10 * f, 1.2), (1, 1.2)])             # đốm đất bay cong
    STEM = kf([(0, 0), (3 * f, 0), (4 * f, .5), (5 * f, 1), (8 * f, 1), (9 * f, .75), (10 * f, .45), (11 * f, .15), (12 * f, 0), (1, 0)])
    SPD = kf([(0, 0), (3 * f, 0), (4 * f, .6), (5 * f, 1), (6 * f, .8), (7 * f, .45), (8 * f, 0), (1, 0)])

    rng = np.random.default_rng(7)
    ph = rng.random(len(NO_LOBES)) * TAU
    drift = [(math.copysign(0.6 + 0.6 * rng.random(), lx if abs(lx) > 0.05 else rng.random() - .5),
              -0.2 - 0.5 * rng.random()) for lx, ly, rx, ry in NO_LOBES]
    bite_dir = rng.random(len(NO_LOBES)) * TAU
    lag = rng.uniform(-0.03, 0.03, len(NO_LOBES))
    szj = rng.uniform(0.88, 1.12, len(NO_LOBES))
    rotj = rng.uniform(-0.28, 0.28, len(NO_LOBES))
    hi_j = [(rng.uniform(-.08, .08), rng.uniform(-.06, .06), rng.uniform(.85, 1.15)) for _ in NO_LOBES]
    spd_ang = [-math.pi / 2 + a for a in (-1.25, -0.75, -0.25, 0.3, 0.8, 1.3, 1.85, -1.85)]
    frames = []
    for i in range(n):
        t = T(i)
        cv = Cv()
        r = R(t) * S
        cy = CY(t) * S
        sx, sy = SX(t), SY(t)
        gclip = ground_clip(YG)
        # --- thân nấm (sau mũ)
        st = STEM(t)
        if st > 0.01:
            top = cy + 0.15 * r
            bot = YG - (1 - min(st, 1)) * (YG - top) * 0.9
            wb = 0.20 * S * min(st * 1.4, 1) * (0.55 + 0.45 * st)
            wn = 0.085 * S * (0.4 + 0.6 * st)
            wt = 0.15 * S * (0.6 + 0.4 * st)
            if st < 0.999 and t > 8 * f:
                wb = 0.012 * S
            ys = np.linspace(bot, top, 20)
            v = (bot - ys) / max(bot - top, 1)
            wv = wb + (wn - wb) * np.sin(np.clip(v / 0.75, 0, 1) * math.pi / 2) ** 0.8
            wv = np.where(v > 0.6, wn + (wt - wn) * ((v - 0.6) / 0.4) ** 2, wv)
            sway = 0.012 * S * np.sin(v * 2.5 + t * 4)
            left = [(cx + sway[k] - wv[k] / 2, ys[k]) for k in range(20)]
            right = [(cx + sway[k] + wv[k] / 2, ys[k]) for k in range(20)][::-1]
            cs = polys_cov([left + right]) * gclip
            cv.paint(cs, C("#7A4B40"))
            shade = [(cx + sway[k] - wv[k] / 2, ys[k]) for k in range(20)] + \
                    [(cx + sway[k] - wv[k] * (0.05 + 0.25 * (1 - v[k])), ys[k]) for k in range(20)][::-1]
            cv.paint(polys_cov([shade]) * cs, C("#553B3D"))
            cv.paint(cov(sd_ell(cx, top + 0.02 * S, wt * 0.62, 0.05 * S)) * cs, C("#553B3D"))
        # --- múi
        h0 = HT(t)
        sp = SP(t)
        bt = BT(t)
        for k, (lx, ly, lrx, lry) in enumerate(NO_LOBES):
            w1 = 0.035 * math.sin(TAU * 1.1 * t + ph[k])
            w2 = 0.03 * math.cos(TAU * 0.9 * t + ph[k] * 1.3)
            px = (lx + w1) * (1 + sp * 0.9) + drift[k][0] * sp * 0.35
            py = (ly + w2) * (1 + sp * 0.5) + drift[k][1] * sp * 0.5
            rr = 1 + 0.06 * math.sin(TAU * 1.3 * t + ph[k] * 0.7) - 0.2 * sp
            lcx = cx + px * r * sx
            lcy = cy + py * r * sy
            lrxp = lrx * r * sx * rr * 1.24 * szj[k]
            lryp = lry * r * sy * rr * 1.24 * szj[k]
            bite = None
            if bt > 0:
                rad = max(lrxp, lryp)
                bb = bt
                bd = rad * (1.25 - 0.55 * bb)
                bite = (lcx + bd * math.cos(bite_dir[k]), lcy + bd * math.sin(bite_dir[k]), rad * 0.62 * bb)
            cols = heat_cols(h0 + lag[k] * (1 if 0.02 < h0 < 0.98 else 0))
            paint_lobe(cv, lcx, lcy, lrxp, lryp, cols, rot=rotj[k], clip=gclip, bite=bite, hi=hi_j[k])
        # --- chớp sao kem
        sr = STAR(t) * S
        if sr > 1:
            rs = np.random.default_rng(100 + i // 2)
            pts = star_pts(cx, YG - 0.035 * S - sr * 0.1, sr, 10, 0.26, -0.3 + t * 0.6, np.random.default_rng(5))
            cs = polys_cov([pts]) * gclip
            cv.paint(cs, C("#FFF2C2"))
            pts2 = star_pts(cx, YG - 0.035 * S - sr * 0.1, sr * 0.45, 8, 0.4, 0.2 - t, np.random.default_rng(6))
            cv.paint(polys_cov([pts2]) * gclip, C("#FFE13A"))
            del rs
        # --- nêm đất màu kem (bung)
        gw = GW(t) * S
        if gw > 1:
            hh = 0.022 * S * min(gw / (0.2 * S), 1)
            wedge = [(cx - gw - 0.05 * S, YG), (cx - 0.07 * S, YG - hh), (cx + 0.07 * S, YG - hh), (cx + gw + 0.05 * S, YG),
                     (cx, YG + 0.004 * S)]
            cv.paint(polys_cov([wedge]) * gclip, C("#FFF0BE"))
        # --- hai cục đất văng (cam -> cong móc -> nhỏ)
        gr = GR(t) * S
        if gr > 0.8:
            gd = GD(t) * S
            gl = GL(t)
            hc = heat_cols(min(1, HT(t) + 0.25))
            for sgn in (-1, 1):
                bx = cx + sgn * gd
                by = YG - gr * 0.75 - gl * 0.07 * S
                # vệt kéo trên đất
                if gl < 0.5:
                    trail = [(cx + sgn * 0.06 * S, YG), (bx - sgn * gr * 0.4, YG - gr * 0.55), (bx, YG)]
                    cv.paint(polys_cov([trail]) * gclip, hc[0], 1 - gl * 2)
                bite = None
                if gl > 0.05:
                    bite = (bx - sgn * gr * (1.0 - 0.5 * min(gl, 1)), by - gr * 0.35, gr * 0.95 * min(gl, 1))
                paint_lobe(cv, bx, by, gr * 1.25, gr * 0.85, hc, clip=gclip, bite=bite, hi=(0, 0, 1.1))
        # --- vạch tốc độ màu kem
        spd = SPD(t)
        if spd > 0.02:
            ps = []
            for k, a in enumerate(spd_ang):
                r0 = r * (1.05 + 0.5 * (1 - spd) + 0.08 * (k % 3))
                ln = 0.06 * S * spd * (0.7 + 0.3 * (k % 2))
                ccx, ccy = cx, cy - 0.25 * r
                p0 = (ccx + math.cos(a) * r0 * sx, ccy + math.sin(a) * r0 * sy)
                p1 = (ccx + math.cos(a) * (r0 * sx + ln), ccy + math.sin(a) * (r0 * sy + ln))
                nx, ny = -math.sin(a) * 0.006 * S, math.cos(a) * 0.006 * S
                ps.append([p0, ((p0[0] + p1[0]) / 2 + nx, (p0[1] + p1[1]) / 2 + ny), p1,
                           ((p0[0] + p1[0]) / 2 - nx, (p0[1] + p1[1]) / 2 - ny)])
            cv.paint(polys_cov(ps), C("#FFF1C4"), min(1, spd * 1.5))
        cv.mul_alpha(AL(t))
        frames.append(cv.img())
    return frames


# ===================================================================================================== 2. NƯỚC TOÉ 16 khung
W_GRAD = [(0.0, "#1C5ED6"), (0.38, "#2386DA"), (0.72, "#2EC4D7"), (1.0, "#46EAD2")]


def water_paint(cv, discs, kblend, ytop, yg, foam_amt, extras=(), alpha=1.0):
    """discs: list dict(x,y,rx,ry,th,u,r,foam). extras: hình phụ (cũng gộp vào khối) dạng (x,y,rx,ry).
    Tô chuyển màu theo độ cao, bọt trắng ở mặt trong mào, vân sáng mảnh, mép đậm, đốm trắng."""
    if not discs and not extras:
        return
    big = np.full((S, S), 1e9, f32)
    near = np.full((S, S), 1e9, f32)
    idx = np.full((S, S), -1, np.int32)
    for k, d in enumerate(discs):
        sd = sd_ell(d["x"], d["y"], d["rx"], d["ry"], d.get("ang", 0.0)) if abs(d["rx"] - d["ry"]) > 0.3 else \
            sd_circ(d["x"], d["y"], d["rx"])
        big = smin(big, sd, kblend)
        m = sd < near
        near = np.where(m, sd, near)
        idx = np.where(m, k, idx)
    for (x, y, rx, ry) in extras:
        sd = sd_ell(x, y, rx, ry)
        big = smin(big, sd, kblend * 0.6)
        m = sd < near
        near = np.where(m, sd, near)
        idx = np.where(m, -1, idx)
    body = cov(big)
    v = np.clip((YY - ytop) / (yg - ytop), 0, 1)
    col = ramp(W_GRAD, v)
    # khung toạ độ theo đĩa gần nhất
    if discs:
        K = len(discs)
        ax = np.array([d["x"] for d in discs] + [0], f32)
        ay = np.array([d["y"] for d in discs] + [0], f32)
        th = np.array([d["th"] for d in discs] + [0], f32)
        uu = np.array([d["u"] for d in discs] + [-1], f32)
        rr = np.array([d["r"] for d in discs] + [1], f32)
        fo = np.array([d["foam"] for d in discs] + [0], f32)
        ii = np.where(idx < 0, K, idx)
        dx = XX - ax[ii]
        dy = YY - ay[ii]
        tx, ty = np.cos(th[ii]), np.sin(th[ii])
        qn = (-ty * dx + tx * dy) / rr[ii]
        un = uu[ii] + (tx * dx + ty * dy) / (rr[ii] * 22)
        valid = ii < K
    else:
        qn = np.zeros((S, S), f32)
        un = np.full((S, S), -1, f32)
        fo = np.zeros(1, f32)
        ii = np.zeros((S, S), np.int32)
        valid = np.zeros((S, S), bool)
    # vân sáng mảnh dọc thân
    streak = np.zeros((S, S), f32)
    for c0, w0, ph in ((-0.55, 0.07, 0.0), (-0.12, 0.05, 1.7), (0.38, 0.06, 3.1)):
        cq = c0 + 0.09 * np.sin(un * 13 + ph)
        streak = np.maximum(streak, np.clip(1 - np.abs(qn - cq) / w0, 0, 1) * (un > 0.08) * (un < 0.97))
    streak = np.clip(streak * 2.2, 0, 1) * valid * (np.clip((rr[ii] - 0.035 * S) / (0.03 * S), 0, 1) if discs else 0)
    # bọt ở mặt trong mào
    fa = fo[ii] * foam_amt * valid
    uf = 1 - 0.55 * fa
    qf = 0.95 - 1.55 * fa * sstep(0.45, 0.85, un) + 0.16 * np.sin(un * 31 + 2.0) + 0.08 * np.sin(un * 57)
    foam = cov((qf - qn) * 40) * (un > uf) * (fa > 0.02)
    fs = np.clip((qn - qf) / 0.55, 0, 1)
    foam_col = ramp([(0, "#BDEFF7"), (1, "#F7FEFF")], fs)
    # mép: tông đậm nhất của chính khối
    rim_f = np.clip(1 - (-big) / 2.6, 0, 1)
    colr = col * (1 - 0.22 * rim_f[..., None])
    cv.paint(body, colr, alpha)
    lite = mix(col, C("#B8F2FF"), 0.55)
    cv.paint(body * streak * (1 - foam) * (rim_f < 0.5), lite, 0.38 * alpha)
    cv.paint(body * foam, foam_col, alpha)
    return big, qn, un, valid, ii


def nuoctoe_frames(n=16):
    YG = 0.88 * S
    YTOP = YG - 0.70 * S
    B = (0.37 * S, YG - 0.012 * S)
    f = 1 / (n - 1)
    TB = 10 * f
    L = kf([(0, .0), (1 * f, .04), (2 * f, .11), (3 * f, .21), (4 * f, .31), (5 * f, .43), (6 * f, .56), (7 * f, .69),
            (8 * f, .81), (9 * f, .91), (10 * f, .97)])
    TH = kf([(0, 8), (2 * f, 12), (3 * f, 22), (4 * f, 42), (5 * f, 78), (6 * f, 122), (7 * f, 160), (8 * f, 190),
             (9 * f, 208), (10 * f, 218)])
    T0 = kf([(0, -150), (2 * f, -134), (4 * f, -116), (7 * f, -110), (10 * f, -112)])
    SZ = kf([(0, .35), (2 * f, .52), (4 * f, .72), (6 * f, .9), (8 * f, 1.0), (10 * f, 1.0)])
    FOAM = kf([(0, 0), (5 * f, 0), (6 * f, .3), (7 * f, .62), (8 * f, .86), (9 * f, 1), (10 * f, 1), (11 * f, .72),
               (12 * f, .42), (13 * f, .16), (14 * f, 0), (1, 0)])
    RP = PchipInterpolator([0, .15, .4, .65, .82, .93, 1], [.10, .082, .07, .088, .108, .092, .042])
    K = 44
    us = np.linspace(0, 1, K)

    def spine(t):
        Ls = L(t) * S
        if Ls < 1:
            return []
        th0 = math.radians(T0(t))
        Th = math.radians(TH(t))
        m = 240
        s = np.linspace(0, 1, m)
        th = th0 + Th * s ** 1.25
        ds = Ls / (m - 1)
        x = B[0] + np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * ds)])
        y = B[1] + np.concatenate([[0], np.cumsum(np.sin(th[:-1]) * ds)])
        xi = np.interp(us, s, x)
        yi = np.interp(us, s, y)
        ti = np.interp(us, s, th)
        r = RP(us) * S * SZ(t)
        return [dict(x=float(xi[k]), y=float(yi[k]), rx=float(r[k]), ry=float(r[k]), r=float(r[k]), th=float(ti[k]),
                     u=float(us[k]), foam=1.0) for k in range(K)]

    base = spine(TB)
    rng = np.random.default_rng(11)
    cxm = np.mean([d["x"] for d in base])
    cym = np.mean([d["y"] for d in base])
    # vỡ thành mảng: chia thân theo u thành 6 cụm, mỗi cụm bay + lộn riêng, cuối mới tơi thành giọt
    bounds = [0, 0.18, 0.38, 0.55, 0.72, 0.86, 1.01]
    grp = np.array([max(j for j in range(6) if u >= bounds[j]) for u in us])
    gv = [(0.10 * S, 0.04 * S), (0.06 * S, -0.04 * S), (-0.30 * S, -0.34 * S), (-0.04 * S, -0.46 * S),
          (0.30 * S, -0.16 * S), (0.46 * S, 0.18 * S)]
    gw = [0.4, -1.2, 2.2, -1.6, 2.4, 3.0]
    gc = []
    for g in range(6):
        sel = [d for d, gg in zip(base, grp) if gg == g]
        gc.append((np.mean([d["x"] for d in sel]), np.mean([d["y"] for d in sel])))
    dv = rng.normal(0, 0.36, (K, 2)) * S
    shrink = rng.uniform(0.45, 0.85, K)
    spin = rng.normal(0, 2.0, K)
    GRAV = 3.0 * S
    # giọt bắn khi vỡ
    drops = []
    for j in range(10):
        k = int(rng.integers(int(K * 0.45), K))
        d = base[k]
        nx, ny = -math.sin(d["th"]), math.cos(d["th"])
        side = -1 if j % 3 else 1
        ang = math.atan2(d["y"] - cym, d["x"] - cxm) + rng.normal(0, 0.4)
        sp = rng.uniform(0.5, 0.9) * S
        drops.append(dict(x0=d["x"] + nx * side * d["r"], y0=d["y"] + ny * side * d["r"],
                          vx=math.cos(ang) * sp + 0.15 * S, vy=math.sin(ang) * sp * 0.5 - 0.12 * S,
                          r=rng.uniform(0.007, 0.015) * S, t0=TB + rng.uniform(0, 1.5 * f)))
    # giọt sớm bay khỏi mào
    early = [dict(t0=6.5 * f, u=0.93, vx=-0.30 * S, vy=-0.70 * S, r=0.016 * S),
             dict(t0=7.2 * f, u=0.85, vx=-0.40 * S, vy=-0.45 * S, r=0.012 * S),
             dict(t0=8.0 * f, u=0.98, vx=0.35 * S, vy=-0.30 * S, r=0.01 * S)]

    frames = []
    for i in range(n):
        t = i * f
        cv = Cv()
        if t <= TB + 1e-6:
            discs = spine(t)
            kb = 0.032 * S
        else:
            tau = t - TB
            discs = []
            for k, d in enumerate(base):
                g = grp[k]
                a = gw[g] * tau
                ox, oy = d["x"] - gc[g][0], d["y"] - gc[g][1]
                rx_, ry_ = ox * math.cos(a) - oy * math.sin(a), ox * math.sin(a) + oy * math.cos(a)
                x = gc[g][0] + rx_ + gv[g][0] * tau + dv[k, 0] * tau * tau * 4
                y = gc[g][1] + ry_ + gv[g][1] * tau + dv[k, 1] * tau * tau * 4 + 0.5 * GRAV * tau * tau
                r = d["r"] * max(0.0, 1 - shrink[k] * (tau / (1 - TB)) ** 1.3)
                if r < 0.8:
                    continue
                pen = np.clip((y + r - YG) / max(r, 1e-3), 0, 1)
                ry = r * (1 - 0.65 * pen)
                rx = r * (1 + 0.7 * pen)
                y = min(y, YG - ry)
                discs.append(dict(x=x, y=y, rx=rx, ry=ry, r=r, th=d["th"] + gw[g] * tau, u=d["u"], foam=1.0))
            kb = S * (0.008 + 0.024 * (1 - sstep(0.05, 0.2, tau)))
        # giọt phụ
        for dd in drops:
            if t > dd["t0"]:
                tau = t - dd["t0"]
                x = dd["x0"] + dd["vx"] * tau
                y = dd["y0"] + dd["vy"] * tau + 0.5 * GRAV * tau * tau
                r = dd["r"] * max(0, 1 - tau / 0.36)
                if r > 0.8 and y < YG:
                    discs.append(dict(x=x, y=y, rx=r, ry=r * 1.12, r=r, th=0.0, u=-1.0, foam=0.0))
        if i >= 1:
            sp_now = spine(min(t, TB)) if t <= TB else base
            for e in early:
                if t > e["t0"] and sp_now:
                    tau = t - e["t0"]
                    k = int(e["u"] * (K - 1))
                    d0 = spine(e["t0"])[k]
                    x = d0["x"] + e["vx"] * tau
                    y = d0["y"] - d0["r"] + e["vy"] * tau + 0.5 * GRAV * tau * tau
                    r = e["r"] * max(0, 1 - tau / 0.3)
                    if r > 0.8:
                        discs.append(dict(x=x, y=y, rx=r, ry=r * 1.15, r=r, th=0.0, u=-1.0, foam=0.0))
        # vũng dưới chân
        grow = min(1.0, L(min(t, TB)) / 0.6)
        extras = []
        if t <= TB:
            extras.append((B[0] + 0.17 * S * grow, YG - 0.010 * S, 0.05 * S + 0.26 * S * grow, 0.014 * S + 0.006 * S * grow))
            if t < 3 * f:
                e = 1 - t / (3 * f)
                extras += [(0.20 * S, YG - 0.006 * S, 0.035 * S * e + 1, 0.008 * S * e + 1),
                           (0.62 * S, YG - 0.006 * S, 0.05 * S * e + 1, 0.009 * S * e + 1)]
        else:
            tau = (t - TB) / (1 - TB)
            sh = 1 - 0.5 * tau
            extras += [(B[0] + 0.12 * S - 0.06 * S * tau, YG - 0.010 * S, 0.16 * S * sh, (0.019 - 0.008 * tau) * S),
                       (B[0] + 0.36 * S + 0.04 * S * tau, YG - 0.009 * S, 0.11 * S * sh, (0.016 - 0.007 * tau) * S)]
        res = water_paint(cv, discs, kb, YTOP, YG, FOAM(t), extras)
        # ô ngọc lam trong bọt + đốm trắng (gắn theo đĩa)
        fa = FOAM(t)
        if res is not None and fa > 0.05 and discs:
            big, qn, un, valid, ii = res
            mains = [d for d in discs if d["u"] >= 0]
            Km = len(mains)
            foam_on = (un > 1 - 0.55 * fa) & valid
            for (uu, qq, ra, rb) in ((0.80, 0.55, 0.42, 0.32), (0.88, 0.35, 0.30, 0.24), (0.72, 0.62, 0.22, 0.18)):
                k = min(Km - 1, int(uu * (Km - 1)))
                if k < 0:
                    continue
                d = mains[k]
                tx, ty = math.cos(d["th"]), math.sin(d["th"])
                ex = d["x"] - ty * qq * d["r"]
                ey = d["y"] + tx * qq * d["r"]
                ce = cov(sd_ell(ex, ey, ra * d["r"] * fa, rb * d["r"] * fa, d["th"])) * cov(big) * foam_on
                cv.paint(ce, C("#46D2D8"))
            spk = []
            rs = np.random.default_rng(3)
            for j in range(16):
                uu = 0.55 + 0.45 * rs.random()
                qq = rs.choice([rs.uniform(0.2, 0.7), rs.uniform(1.12, 1.5), rs.uniform(-0.6, 0.0)])
                k = min(Km - 1, int(uu * (Km - 1)))
                d = mains[k]
                tx, ty = math.cos(d["th"]), math.sin(d["th"])
                ex = d["x"] - ty * qq * d["r"] + tx * rs.uniform(-.3, .3) * d["r"]
                ey = d["y"] + tx * qq * d["r"] + ty * rs.uniform(-.3, .3) * d["r"]
                rr = rs.uniform(0.004, 0.009) * S * min(1, fa * 1.5)
                spk.append((ex, ey, rr * 1.3, rr * 0.8, d["th"]))
            cs = np.zeros((S, S), f32)
            for (ex, ey, a, b, an) in spk:
                cs = np.maximum(cs, cov(sd_ell(ex, ey, a, b, an)))
            cv.paint(cs, C("#FFFFFF"))
        if i == n - 1:
            cv.mul_alpha(0.75)
        frames.append(cv.img())
    return frames


# ======================================================================================================= 3. LỬA lặp 12 khung
FIRE = ["#F0461E", "#FF9A1F", "#FFE24A", "#FFF6B8"]


def fire_tones(cv, c, base_y, height, noise=None, nscroll=0.0, glow=0.0, hot_x=None, a=1.0, rim=4.0, yel=10.0):
    """silhouette c -> quầng mềm + 4 tông lửa (mép đỏ cam, cam, vàng, lõi kem) theo khoảng cách vào trong + nhiễu"""
    if glow > 0:
        g = ndimage.gaussian_filter(c, 0.05 * S)
        cv.paint(np.clip(g * 1.7, 0, 1), C("#F0461E"), glow * a)
    D = inner_dist(c)
    hf = np.clip((base_y - YY) / max(height, 1), 0, 1) if hot_x is None else hot_x
    if noise is not None:
        n1 = nsamp(noise[0], XX, YY + nscroll)
        n2 = nsamp(noise[1], XX, YY + nscroll)
    else:
        n1 = n2 = np.zeros((S, S), f32)
    cv.paint(c, C(FIRE[0]), a)
    cv.paint(cov(rim + 1.5 * n1 - D, 1.0) * c, C(FIRE[1]), a)
    cv.paint(cov(yel + 16 * hf + 5 * n2 - D, 1.0) * c, C(FIRE[2]), a)
    cv.paint(cov(26 + 46 * hf + 5 * n1 - D, 1.0) * c, C(FIRE[3]), a)


def tongue_poly(bx, by, h, w, ang_fn, wprof=None, n=40):
    cl = angle_curve(bx, by, h, ang_fn, n)
    s = np.linspace(0, 1, n)
    if wprof is None:
        wv = w * (1 - s) ** 0.9 * (0.75 + 0.5 * np.sin(np.pi * np.minimum(s / 0.5, 1)) * (s < 0.5) + 0.5 * (s >= 0.5) * 0)
    else:
        wv = wprof(s) * w
    return ribbon(cl, wv), cl


LUA_T = [  # x lệch, cao, rộng, nghiêng(độ), uốn(độ), móc(độ), pha, tần số(nguyên)
    (-0.100, 0.46, 0.18, -10, 12, -52, 0.00, 1),
    (0.110, 0.52, 0.19, 9, -10, 56, 0.37, 1),
    (0.000, 0.74, 0.25, -2, 14, 46, 0.62, 1),
    (-0.175, 0.30, 0.12, -22, 8, -62, 0.15, 2),
    (0.185, 0.33, 0.12, 20, -8, 66, 0.81, 2),
    (-0.040, 0.58, 0.14, -8, -16, -56, 0.48, 2),
]


def lua_shape(t, cx, base_y, scale=1.0, tongues=LUA_T, flakes=True):
    """trả về (vùng ngoài, vùng vàng, vùng lõi): mỗi vùng là hợp các lưỡi cùng đường giữa nhưng thấp, hẹp dần"""
    outer, yel, core = [], [], []
    tips = []
    wp = lambda s: (1 - s) ** 0.85 * (0.8 + 0.35 * np.sin(np.pi * np.clip(s / 0.45, 0, 1)))
    for (x0, h0, w0, lean, bend, hook, ph, fr) in tongues:
        p = TAU * (fr * t + ph)
        h = h0 * S * scale * (1 + 0.13 * math.sin(p))
        lean_t = lean + 6 * math.sin(p + 1.1)
        bend_t = bend * (1 + 0.5 * math.sin(p + 2.0))
        hook_t = hook * (0.8 + 0.35 * math.sin(p + 0.6))
        fn = lambda s, a=lean_t, b=bend_t, c=hook_t, q=p: -90 + a + b * math.sin(math.pi * s * 1.3 + q * 0.5) + c * s ** 3
        bx = cx + x0 * S * scale + 0.012 * S * scale * math.sin(p + 0.3)
        by = base_y - 0.05 * S * scale
        poly, cl = tongue_poly(bx, by, h, w0 * S * scale, fn, wp)
        outer.append(poly)
        tips.append((cl[-1], fn(1.0)))
        # lưỡi vàng bên trong: cùng hướng, thấp 60 %, hẹp 52 %, móc mạnh hơn chút
        fn_y = lambda s, a=lean_t, b=bend_t, c=hook_t, q=p: -90 + a * 0.8 + b * math.sin(math.pi * s * 1.3 + q * 0.5 + 0.4) + c * 1.1 * s ** 3
        py_, _ = tongue_poly(bx + 0.006 * S * math.sin(p * 2), by + 0.01 * S, h * 0.60, w0 * S * scale * 0.52, fn_y, wp)
        yel.append(py_)
        if h0 > 0.4:
            pc, _ = tongue_poly(bx, by + 0.02 * S, h * 0.30, w0 * S * scale * 0.30, fn_y, wp)
            core.append(pc)
    if flakes:
        for j, (tip, ang) in enumerate(tips):
            for m_, off in (((2, 0.0), (2, 0.5)) if j in (2, 1) else ((2, 0.25),)):
                pf = (m_ * t + off + 0.13 * j) % 1.0
                sz = math.sin(math.pi * pf) ** 0.9
                if sz < 0.05:
                    continue
                sgn = 1 if j % 2 else -1
                fx = tip[0] + sgn * 0.035 * S * scale * pf + 0.01 * S * math.sin(TAU * pf + j)
                fy = tip[1] - 0.20 * S * scale * pf + 0.03 * S * scale
                hk = 75 * sgn
                fn2 = lambda s, hk=hk, j=j: -90 + 12 * math.sin(j) + hk * s ** 2
                poly, _ = tongue_poly(fx, fy, 0.09 * S * scale * sz, 0.032 * S * scale * sz, fn2,
                                      lambda s: np.sin(np.pi * np.clip(s * 1.15, 0, 1)) ** 0.6 * (1 - s) ** 0.8)
                outer.append(poly)
    c_out = polys_cov(outer)
    c_out = np.maximum(c_out, cov(sd_ell(cx, base_y - 0.085 * S * scale, 0.19 * S * scale, 0.085 * S * scale)))
    c_yel = polys_cov(yel)
    c_yel = np.maximum(c_yel, cov(sd_ell(cx, base_y - 0.08 * S * scale, 0.13 * S * scale, 0.055 * S * scale)))
    c_core = polys_cov(core)
    c_core = np.maximum(c_core, cov(sd_ell(cx, base_y - 0.065 * S * scale, 0.07 * S * scale, 0.03 * S * scale)))
    return c_out, c_yel, c_core


def paint_fire(cv, c_out, c_yel, c_core, glow=0.34, noise=None, nscroll=0.0, a=1.0):
    if glow > 0:
        g = ndimage.gaussian_filter(c_out, 0.05 * S)
        cv.paint(np.clip(g * 1.7, 0, 1), C("#F0461E"), glow * a)
    D = inner_dist(c_out)
    n1 = nsamp(noise, XX, YY + nscroll) if noise is not None else 0
    cv.paint(c_out, C(FIRE[0]), a)
    cv.paint(cov(4.0 + 1.6 * n1 - D, 1.0) * c_out, C(FIRE[1]), a)
    cv.paint(cov(8.0 - D, 1.0) * c_out * c_yel, C(FIRE[2]), a)
    cv.paint(cov(12.0 - D, 1.0) * c_out * c_core, C(FIRE[3]), a)


def lua_frames(n=12):
    base_y = 0.95 * S
    cx = 0.5 * S
    nz = tnoise(S // 2, S, 22, 9, 31)
    frames = []
    for i in range(n):
        t = i / n
        c_out, c_yel, c_core = lua_shape(t, cx, base_y)
        cv = Cv()
        paint_fire(cv, c_out, c_yel, c_core, 0.34, nz, t * (S // 2))
        frames.append(cv.img())
    return frames



# ================================================================================================= 4. KHÓI tan 12 khung
SMOKE = ["#675852", "#8B7B73", "#AE9F95"]
KHOI_LOBES = [(0.02, -0.52, 0.56, 0.42, 0), (-0.56, -0.24, 0.46, 0.34, 1), (0.56, -0.20, 0.47, 0.35, 2),
              (-0.24, 0.06, 0.54, 0.37, 1), (0.36, 0.09, 0.52, 0.35, 2), (-0.86, 0.16, 0.33, 0.24, 1),
              (0.88, 0.19, 0.31, 0.22, 2)]


def smoke_cluster(cv, cx, cy, R, lobes, t_phase, spread, bite, rng_seed, cols=SMOKE, a=0.88, wob=0.035):
    rng = np.random.default_rng(rng_seed)
    lay = Cv()
    gdir = [(0.1, -1.0), (-0.9, -0.5), (0.9, -0.4)]
    for k, (lx, ly, rx, ry, g) in enumerate(lobes):
        ph = rng.random() * TAU
        bd = rng.random() * TAU
        hj = (rng.uniform(-.08, .08), rng.uniform(-.06, .06), rng.uniform(.85, 1.15))
        px = lx + wob * math.sin(TAU * t_phase + ph) + gdir[g][0] * spread * (0.6 + 0.4 * rng.random())
        py = ly + wob * math.cos(TAU * t_phase * 0.8 + ph) + gdir[g][1] * spread * (0.5 + 0.4 * rng.random())
        sc = 1 - 0.18 * spread
        lcx, lcy = cx + px * R, cy + py * R
        lrx, lry = rx * R * sc, ry * R * sc
        bt = None
        if bite > 0:
            rad = max(lrx, lry)
            bdd = rad * (1.25 - 0.55 * bite)
            bt = (lcx + bdd * math.cos(bd), lcy + bdd * math.sin(bd), rad * 0.62 * bite)
        paint_lobe(lay, lcx, lcy, lrx, lry, [C(x) for x in cols], rot=0.16 * math.sin(ph), bite=bt, hi=hj,
                   mid=(0.02, 0.09, 0.93, 0.80))
    cv.over(lay, a)


def khoi_frames(n=12):
    T = lambda i: i / (n - 1)
    R = kf([(0, .13), (.2, .175), (.5, .215), (1, .25)])
    CY = kf([(0, .66), (1, .47)])
    SPR = kf([(0, 0), (.25, .06), (.6, .32), (1, .62)])
    BT = kf([(0, 0), (.4, 0), (.65, .6), (.85, 1.15), (1, 1.6)])
    AL = kf([(0, .88), (.5, .86), (.75, .62), (.9, .36), (1, .14)])
    frames = []
    for i in range(n):
        t = T(i)
        cv = Cv()
        smoke_cluster(cv, 0.5 * S, CY(t) * S, R(t) * S, KHOI_LOBES, t * 0.9, SPR(t), BT(t), 21, a=AL(t))
        frames.append(cv.img())
    return frames


# ================================================================================================ 5. LỐC năng lượng 12 khung
LOC_PAL = [["#0B2630", "#0F5E5A", "#17B48E", "#2EF0B4", "#C6FFEA"],   # lục ngọc
           ["#0A2A24", "#1A6E3A", "#36C25A", "#8CF56A", "#E6FFC0"]]   # lục chanh


def loc_frames(n=12):
    Q4 = 4
    W = N * Q4
    yb, yt = 0.86, 0.14
    H = yb - yt
    e = 0.30
    rng = np.random.default_rng(41)
    strips = []
    # (lớp, số bản sao, v0, dv, th0, dth, rộng, bảng)
    layer_defs = [(3, 0.02, 0.30, 0.55), (2, 0.18, 0.34, 0.62), (3, 0.38, 0.32, 0.50), (4, 0.58, 0.30, 0.42),
                  (3, 0.72, 0.26, 0.40), (2, 0.08, 0.80, 0.30), (3, 0.30, 0.66, 0.34)]
    for li, (nc, v0, dv, wfac) in enumerate(layer_defs):
        th0 = rng.random() * TAU
        dth = rng.uniform(1.6, 2.6)
        w = (0.030 + 0.03 * wfac) * 1.0
        pal = li % 2
        for j in range(nc):
            strips.append(dict(n=nc, v0=v0 + rng.uniform(-0.03, 0.03), dv=dv, th0=th0 + TAU * j / nc, dth=dth,
                               w=w * rng.uniform(0.8, 1.2), pal=pal if (j + li) % 3 else 1 - pal))
    specks = [dict(v=rng.uniform(0.15, 0.95), th=rng.random() * TAU, m=int(rng.integers(1, 3)), r=rng.uniform(0.006, 0.012))
              for _ in range(16)]

    def rad(v):
        return 0.05 + 0.25 * v ** 1.25

    frames = []
    for i in range(n):
        t = i / n
        img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        glow = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        dr = ImageDraw.Draw(img)

        def axis_x(v):
            return 0.5 + 0.035 * math.sin(TAU * t + 2.2 * v) * v

        def P(v, th):
            r = rad(v)
            return ((axis_x(v) + r * math.cos(th)) * W, (yb - H * v + r * e * math.sin(th)) * W)

        # quầng mềm quanh lốc + nền vũng tối
        ga = np.zeros((W, W), f32)
        gy, gx = np.mgrid[0:W, 0:W].astype(f32) / W
        ga = 0.30 * np.exp(-(((gx - 0.5) / 0.26) ** 2 + ((gy - 0.50) / 0.40) ** 2))
        gl = np.zeros((W, W, 4), np.uint8)
        gl[..., 0], gl[..., 1], gl[..., 2] = 60, 255, 190
        gl[..., 3] = (np.clip(ga, 0, 1) * 255).astype(np.uint8)
        img = Image.alpha_composite(img, Image.fromarray(gl, "RGBA"))
        dr = ImageDraw.Draw(img)
        bx = 0.5 * W
        by = yb * W + 0.01 * W
        dr.ellipse([bx - 0.27 * W, by - 0.055 * W, bx + 0.27 * W, by + 0.055 * W], fill="#0C2A30")
        dr.ellipse([bx - 0.22 * W, by - 0.040 * W, bx + 0.22 * W, by + 0.032 * W], fill="#0F5E5A")
        dr.ellipse([bx - 0.17 * W, by - 0.036 * W, bx + 0.17 * W, by + 0.018 * W], fill="#0B2630")
        # vòng sáng chạy quanh vũng
        for k in range(3):
            a0 = TAU * (t + k / 3)
            pts = []
            for s in np.linspace(0, 1, 16):
                a = a0 + 1.4 * s
                pts.append((bx + 0.20 * W * math.cos(a), by + 0.035 * W * math.sin(a)))
            if math.sin(a0 + 0.7) > -0.2:
                dr.line(pts, fill="#2EF0B4", width=int(0.010 * W), joint="curve")
        # đoạn dải -> sắp theo độ sâu
        segs = []
        for st in strips:
            m = 26
            rot = TAU * t / st["n"]
            pts = []
            for k in range(m):
                s = k / (m - 1)
                v = st["v0"] + st["dv"] * s
                th = st["th0"] + st["dth"] * s + rot
                pts.append((P(v, th), th, s))
            for k in range(m - 1):
                (p0, th0, s0), (p1, th1, s1) = pts[k], pts[k + 1]
                dx, dy = p1[0] - p0[0], p1[1] - p0[1]
                ln = math.hypot(dx, dy) + 1e-6
                nx, ny = -dy / ln, dx / ln
                w0 = st["w"] * W * math.sin(math.pi * s0) ** 0.7 * 0.5
                w1 = st["w"] * W * math.sin(math.pi * s1) ** 0.7 * 0.5
                depth = math.sin((th0 + th1) / 2)
                segs.append((depth, p0, p1, nx, ny, w0, w1, st["pal"]))
        # đốm sáng quay theo
        for sp in specks:
            th = sp["th"] + TAU * t * sp["m"]
            p = P(sp["v"], th)
            segs.append((math.sin(th), p, None, 0, 0, sp["r"] * W, 0, -1))
        segs.sort(key=lambda z: z[0])
        core_drawn = False
        for depth, p0, p1, nx, ny, w0, w1, pal in segs:
            if not core_drawn and depth > -0.05:
                core_drawn = True
                # lõi sáng: quầng + bầu dục kem lệch lên trên
                cl = Image.new("RGBA", (W, W), (0, 0, 0, 0))
                ca = 0.75 * np.exp(-(((gx - axis_x(0.5)) / 0.11) ** 2 + ((gy - 0.47) / 0.20) ** 2))
                cc = np.zeros((W, W, 4), np.uint8)
                cc[..., 0], cc[..., 1], cc[..., 2] = 150, 255, 225
                cc[..., 3] = (np.clip(ca, 0, 1) * 255).astype(np.uint8)
                img = Image.alpha_composite(img, Image.fromarray(cc, "RGBA"))
                dr = ImageDraw.Draw(img)
                ax_ = axis_x(0.55) * W
                dr.ellipse([ax_ - 0.05 * W, 0.36 * W, ax_ + 0.045 * W, 0.50 * W], fill="#C6FFEA")
                dr.ellipse([ax_ - 0.03 * W, 0.38 * W, ax_ + 0.02 * W, 0.44 * W], fill="#F4FFFB")
            if pal < 0:
                col = "#C6FFEA" if depth > 0 else "#17B48E"
                r = w0
                dr.ellipse([p0[0] - r, p0[1] - r * 1.3, p0[0] + r, p0[1] + r * 1.3], fill=col)
                continue
            P5 = LOC_PAL[pal]
            if depth < -0.35:
                col = P5[0]
            elif depth < 0.1:
                col = P5[1]
            elif depth < 0.55:
                col = P5[2]
            elif depth < 0.85:
                col = P5[3]
            else:
                col = P5[4]
            ex = 1.0
            q = [(p0[0] - nx * w0 * 1.35, p0[1] - ny * w0 * 1.35), (p1[0] - nx * w1 * 1.35, p1[1] - ny * w1 * 1.35),
                 (p1[0] + nx * w1 * 1.35, p1[1] + ny * w1 * 1.35), (p0[0] + nx * w0 * 1.35, p0[1] + ny * w0 * 1.35)]
            if depth > -0.35:
                dr.polygon(q, fill=P5[0])
            q = [(p0[0] - nx * w0, p0[1] - ny * w0), (p1[0] - nx * w1 * ex, p1[1] - ny * w1 * ex),
                 (p1[0] + nx * w1 * ex, p1[1] + ny * w1 * ex), (p0[0] + nx * w0, p0[1] + ny * w0)]
            dr.polygon(q, fill=col)
        # khói tím mờ bay theo đỉnh
        wl = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        wd = ImageDraw.Draw(wl)
        for k in range(3):
            a0 = TAU * (t / 3 + k / 3) + 0.5
            pts_l, pts_r = [], []
            for s in np.linspace(0, 1, 20):
                a = a0 + 1.3 * s
                v = 0.82 + 0.12 * s
                r = rad(v) * 1.18
                x = (axis_x(v) + r * math.cos(a)) * W
                y = (yb - H * v + r * e * math.sin(a)) * W - 0.04 * W
                ww = 0.03 * W * math.sin(math.pi * s) ** 0.8
                pts_l.append((x, y - ww))
                pts_r.append((x, y + ww))
            if math.sin(a0 + 0.65) < 0.3:
                wd.polygon(pts_l + pts_r[::-1], fill=(110, 92, 160, 120))
        img = Image.alpha_composite(img, wl)
        frames.append(down_img(img, Q4))
    return frames


def down_img(img, q):
    a = np.asarray(img, f32) / 255
    pm = np.concatenate([a[..., :3] * a[..., 3:], a[..., 3:]], -1)
    h, w = pm.shape[0] // q, pm.shape[1] // q
    pm = pm.reshape(h, q, w, q, 4).mean((1, 3))
    al = pm[..., 3:]
    rgb = np.where(al > 1e-5, pm[..., :3] / np.maximum(al, 1e-5), 0)
    return Image.fromarray((np.clip(np.concatenate([rgb, al], -1), 0, 1) * 255 + .5).astype(np.uint8), "RGBA")


# ========================================================================================== 6–7. GAI LÁ / GAI SẮT 12 khung
LEAF = dict(edge="#1F7A38", shade="#3BAA45", lit="#6FD150", hi="#B4EE72", vein="#D2F78E", vein2="#5CC856")
WOOD = dict(edge="#5A3A22", shade="#8A5A34", lit="#B47C48", hi="#D8A468", vein="#E2B47A", vein2="#A06A3C")
DIRT = dict(top="#B88250", base="#8E5E38", crack="#5E3B22", rock="#7A4E2E", rock_hi="#A87446")
DUST = ["#CDB083", "#E3CC9C", "#F6E8C4"]
STEEL = dict(edge="#3E4A62", f0="#A9B8D0", f1="#7F90AE", f2="#5B6B86", t0="#DCE5F0", t1="#A2B2CA", t2="#6E7E9A", sheen="#F4F1E4")
CRYS = dict(edge="#0E5560", f0="#7FF2E2", f1="#2CC7C4", f2="#13868E", t0="#D8FFF8", t1="#7FE6E0", t2="#1FA3A6", sheen="#F4FFFC")


def paint_blade(cv, base_x, base_y, H, W, lean, bend, pal, clip, sway=0.0, stretch=1.0, sink=0.0):
    """gai lá: lưỡi cong thuôn nhọn; nửa trái sáng, nửa phải tối, mép đậm, gân giữa + gân phụ, mảng sáng bầu dục"""
    Hs = H * stretch
    Ws = W / math.sqrt(max(stretch, 0.3))
    fn = lambda s: -90 + lean + sway + bend * s ** 1.6
    cl = angle_curve(base_x, base_y + sink + 0.03 * S, Hs + 0.03 * S, fn, 44)
    s = np.linspace(0, 1, len(cl))
    wv = Ws * (1 - s) ** 1.15 * (0.62 + 1.5 * s * (1 - s) + 0.4 * s)
    poly = ribbon(cl, wv)
    c = polys_cov([poly]) * clip
    if c.max() <= 0:
        return
    D = inner_dist(c)
    _, U, Qd = polyline_frame(cl)
    cv.paint(c, C(pal["edge"]))
    inner = cov(2.6 - D, 1.0) * c
    lit = cov(Qd + 0.6, 1.0)
    cv.paint(inner * (1 - lit), C(pal["shade"]))
    cv.paint(inner * lit, C(pal["lit"]))
    # mảng sáng bầu dục trên nửa sáng, lệch lên
    k = int(0.5 * (len(cl) - 1))
    tx, ty = cl[k + 1] - cl[k - 1]
    an = math.atan2(ty, tx)
    wk = wv[k]
    hx = cl[k][0] + math.sin(an) * wk * 0.24
    hy = cl[k][1] - math.cos(an) * wk * 0.24
    cv.paint(cov(sd_ell(hx, hy, 0.17 * Hs, 0.11 * Ws, an)) * inner * lit, C(pal["hi"]))
    # gân giữa + gân phụ
    vein = [tuple(p) for p in cl[2:int(len(cl) * 0.86)]]
    cv.paint(lines_cov([vein], 0.010 * S) * inner, C(pal["vein"]))
    side = []
    for sj in (0.18, 0.32, 0.46, 0.60, 0.72):
        k = int(sj * (len(cl) - 1))
        tx, ty = cl[k + 1] - cl[k - 1]
        an = math.atan2(ty, tx)
        for sgn in (-1, 1):
            a2 = an + sgn * 0.0
            ln = wv[k] * 0.42
            ex = cl[k][0] + (math.cos(an) * 0.55 - sgn * math.sin(an)) * ln
            ey = cl[k][1] + (math.sin(an) * 0.55 + sgn * math.cos(an)) * ln
            side.append([tuple(cl[k]), (ex, ey)])
    sc = lines_cov(side, 0.006 * S) * inner
    cv.paint(sc * lit, C(pal["vein"]), 0.85)
    cv.paint(sc * (1 - lit), C(pal["vein2"]))


def crystal_faces(w, h):
    """mặt của một cột tinh thể, toạ độ cục bộ (x phải, y lên)"""
    L, R1, R2, R = -0.5 * w, -0.14 * w, 0.20 * w, 0.5 * w
    SL, M1, M2, SR, TIP = (-0.47 * w, 0.70 * h), (-0.13 * w, 0.75 * h), (0.19 * w, 0.73 * h), (0.47 * w, 0.68 * h), (0.03 * w, h)
    return [([(L, 0), SL, M1, (R1, 0)], "f0"), ([(R1, 0), M1, M2, (R2, 0)], "f1"), ([(R2, 0), M2, SR, (R, 0)], "f2"),
            ([SL, TIP, M1], "t0"), ([M1, TIP, M2], "t1"), ([M2, TIP, SR], "t2")]


def xf(pts, bx, by, ang, sy=1.0, sx=1.0, piv=(0, 0)):
    c, s = math.cos(ang), math.sin(ang)
    out = []
    for x, y in pts:
        x, y = (x - piv[0]) * sx, (y - piv[1]) * sy
        X = x * c + y * s
        Y = -x * s + y * c
        out.append((bx + X + piv[0], by - (Y + piv[1])))
    return out


def paint_faceted(cv, faces, pal, clip, alpha=1.0, sheen=None):
    """faces = [(pts toạ độ S, khoá màu)]; mép đậm (tông tối nhất), mặt sáng / giữa / tối, vệt sáng chéo"""
    c = polys_cov([f[0] for f in faces]) * clip
    if c.max() <= 0:
        return
    D = inner_dist(c)
    lay = Cv()
    lay.paint(c, C(pal["edge"]))
    inner = cov(2.4 - D, 1.0) * c
    for pts, key in faces:
        lay.paint(polys_cov([pts]) * inner, C(pal[key]))
    if sheen:
        lay.paint(polys_cov(sheen) * inner * polys_cov([f[0] for f in faces if f[1] in ("f0", "f1", "t0")]),
                  C(pal["sheen"]), 0.9)
    cv.over(lay, alpha)


def ground_fx(cv, t, f, cx, YG, crack_k, mound_k, chunks, dust, rock_cols, front=False):
    """vết nứt, mô đất, đất văng, bụi"""
    if not front:
        if mound_k > 0.01:
            rx = 0.20 * S * (0.6 + 0.4 * mound_k)
            ry = 0.038 * S * (0.7 + 0.5 * mound_k)
            cv.paint(cov(sd_ell(cx, YG, rx, ry)), C(DIRT["base"]), min(1, mound_k * 1.5))
            cv.paint(cov(sd_ell(cx, YG - ry * 0.25, rx * 0.86, ry * 0.62)), C(DIRT["top"]), min(1, mound_k * 1.5))
        if crack_k > 0.01:
            rng = np.random.default_rng(5)
            lines = []
            for k in range(7):
                a = TAU * k / 7 + rng.uniform(-.3, .3)
                ln = 0.24 * S * crack_k * rng.uniform(0.6, 1.0)
                pts = [(cx, YG)]
                for j in range(1, 5):
                    rr = ln * j / 4
                    aj = a + rng.uniform(-.25, .25)
                    pts.append((cx + rr * math.cos(aj), YG + rr * 0.24 * math.sin(aj)))
                lines.append(pts)
            cv.paint(lines_cov(lines, 0.009 * S), C(DIRT["crack"]), min(1, crack_k * 1.3))
        return
    # phía trước: đất văng + bụi
    for ch in chunks:
        tr = t - ch["t0"]
        if tr <= 0:
            continue
        x = ch["x0"] + ch["vx"] * tr
        y = ch["y0"] + ch["vy"] * tr + 0.5 * 4.6 * S * tr * tr
        if y > YG + 0.01 * S:
            continue
        a = 1 - sstep(0.4, 0.62, tr)
        ang = ch["rot"] + ch["w"] * tr
        pts = [(x + ch["r"] * ch["sh"][k] * math.cos(ang + TAU * k / 5), y + ch["r"] * ch["sh"][k] * math.sin(ang + TAU * k / 5))
               for k in range(5)]
        cpoly = polys_cov([pts])
        cv.paint(cpoly, C(rock_cols[0]), a)
        cv.paint(cpoly * cov(sd_circ(x - ch["r"] * 0.25, y - ch["r"] * 0.35, ch["r"] * 0.6)), C(rock_cols[1]), a)
    for du in dust:
        tr = t - du["t0"]
        if tr <= 0:
            continue
        pr = tr / du["life"]
        if pr >= 1:
            continue
        R = du["r"] * (0.5 + 0.8 * math.sqrt(pr))
        a = 0.95 * (1 - sstep(0.45, 1.0, pr))
        smoke_cluster(cv, du["x"] + du["vx"] * tr, du["y"] - 0.05 * S * pr, R, KHOI_LOBES[3:], pr * 0.5, pr * 0.3,
                      max(0, pr - 0.5) * 2.4, du["seed"], cols=DUST, a=a, wob=0.02)


def make_chunks(rng, cx, YG, t0, nch=9):
    out = []
    for k in range(nch):
        sgn = -1 if k % 2 else 1
        out.append(dict(x0=cx + sgn * rng.uniform(0.01, 0.06) * S, y0=YG - 0.01 * S, vx=sgn * rng.uniform(0.25, 0.7) * S,
                        vy=-rng.uniform(0.7, 1.35) * S, r=rng.uniform(0.010, 0.022) * S, rot=rng.random() * TAU,
                        w=rng.normal(0, 9), sh=rng.uniform(0.7, 1.2, 5), t0=t0 + rng.uniform(0, 0.03)))
    return out


def make_dust(rng, cx, YG, t0):
    out = []
    for k, sgn in enumerate((-1, 1, -1, 1)):
        out.append(dict(x=cx + sgn * rng.uniform(0.08, 0.16) * S, y=YG - 0.02 * S, vx=sgn * rng.uniform(0.06, 0.16) * S,
                        r=rng.uniform(0.07, 0.10) * S, t0=t0 + 0.02 * k, life=rng.uniform(0.45, 0.6), seed=50 + k))
    return out


GAI_KEYS = None


def gai_timeline(n):
    f = 1 / (n - 1)
    G = kf([(0, 0), (1 * f, .10), (2 * f, .58), (3 * f, 1.16), (4 * f, .95), (5 * f, 1.03), (6 * f, 1.0), (8 * f, 1.0),
            (9 * f, .70), (10 * f, .34), (1, .04)])
    CR = kf([(0, .45), (1 * f, .85), (2 * f, 1), (8 * f, 1), (10 * f, .7), (1, .3)])
    MD = kf([(0, .35), (1 * f, 1.0), (2 * f, .75), (3 * f, .6), (8 * f, .6), (10 * f, .45), (1, .25)])
    return f, G, CR, MD


def gaila_frames(n=12):
    YG = 0.90 * S
    cx = 0.5 * S
    f, G, CR, MD = gai_timeline(n)
    rng = np.random.default_rng(61)
    chunks = make_chunks(rng, cx, YG, 2 * f - 0.02)
    dust = make_dust(rng, cx, YG, 2 * f - 0.03)
    blades = [  # x, H, W, lean, bend, pal, sway pha
        (-0.115, 0.42, 0.13, -22, -16, LEAF, 0.4),
        (0.125, 0.36, 0.12, 24, 18, LEAF, 1.9),
        (0.00, 0.66, 0.17, 4, 26, LEAF, 0.0),
        (-0.05, 0.20, 0.07, -38, -10, WOOD, 2.6),
        (0.065, 0.17, 0.065, 40, 12, WOOD, 3.3)]
    leaves = []
    for k in range(9):
        leaves.append(dict(x=cx + rng.uniform(-0.18, 0.2) * S, y=YG - rng.uniform(0.25, 0.62) * S, ph=rng.random() * TAU,
                           vx=rng.uniform(-0.2, 0.2) * S, r=rng.uniform(0.022, 0.034) * S, t0=8.4 * f + rng.uniform(0, 1.2 * f)))
    frames = []
    for i in range(n):
        t = i * f
        cv = Cv()
        ground_fx(cv, t, f, cx, YG, CR(t), MD(t), chunks, dust, (DIRT["rock"], DIRT["rock_hi"]))
        g = G(t)
        clip = np.clip(YG + 0.006 * S - YY, 0, 1)
        for k, (x0, H, Wd, lean, bend, pal, ph) in enumerate(blades):
            delay = 0.0 if k < 3 else 0.35 * f
            gk = G(max(0, t - delay)) * (1 if k != 2 else 1)
            if gk <= 0.005:
                continue
            stretch = max(1.0, gk)
            sink = (1 - min(gk, 1)) * (H * S + 0.04 * S)
            hold = sstep(3.5 * f, 4.5 * f, t) * (1 - sstep(8 * f, 9 * f, t))
            sway = 3.5 * math.sin(TAU * 1.6 * (t - 4 * f) + ph) * hold
            paint_blade(cv, cx + x0 * S, YG, H * S, Wd * S, lean, bend, pal, clip, sway=sway, stretch=stretch, sink=sink)
        # mép trước của mô đất che gốc
        md = MD(t)
        rx = 0.20 * S * (0.6 + 0.4 * md)
        ry = 0.038 * S * (0.7 + 0.5 * md)
        lip = cov(sd_ell(cx, YG, rx * 0.9, ry)) * np.clip(YY - YG + 0.2 * ry, 0, 1)
        cv.paint(lip, C(DIRT["base"]), min(1, md * 1.5))
        ground_fx(cv, t, f, cx, YG, 0, 0, chunks, dust, (DIRT["rock"], DIRT["rock_hi"]), front=True)
        # vụn lá rơi
        lp = []
        for lf in leaves:
            tr = t - lf["t0"]
            if tr <= 0:
                continue
            a = 1 - sstep(0.12, 0.26, tr)
            x = lf["x"] + lf["vx"] * tr + 0.02 * S * math.sin(lf["ph"] + tr * 30)
            y = lf["y"] + 0.9 * S * tr
            an = lf["ph"] + 2.5 * math.sin(tr * 25 + lf["ph"])
            r = lf["r"]
            pts = [(x + r * math.cos(an), y + r * math.sin(an)), (x + 0.4 * r * math.cos(an + 1.6), y + 0.4 * r * math.sin(an + 1.6)),
                   (x - r * math.cos(an), y - r * math.sin(an)), (x + 0.4 * r * math.cos(an - 1.6), y + 0.4 * r * math.sin(an - 1.6))]
            cl_ = polys_cov([pts])
            cv.paint(cl_, C(LEAF["edge"]), a)
            cv.paint(cl_ * cov(sd_circ(x - 0.2 * r, y - 0.2 * r, 0.55 * r)), C(LEAF["lit"]), a)
        frames.append(cv.img())
    return frames


def gaisat_frames(n=12, pal=STEEL):
    YG = 0.90 * S
    cx = 0.5 * S
    f, G, CR, MD = gai_timeline(n)
    rng = np.random.default_rng(71)
    chunks = make_chunks(rng, cx, YG, 2 * f - 0.02)
    dust = make_dust(rng, cx, YG, 2 * f - 0.03)
    spikes = [  # x, h, w, nghiêng (độ, dương = sang phải), trễ
        (-0.20, 0.24, 0.085, 32, 0.4), (0.21, 0.22, 0.08, -30, 0.5), (0.0, 0.62, 0.15, 0, 0.0),
        (-0.105, 0.42, 0.115, 15, 0.15), (0.11, 0.46, 0.12, -13, 0.25)]
    # mảnh vỡ: mỗi cột cắt 3 đường chéo
    cuts = [[(0.30 + rng.uniform(-.04, .04), rng.uniform(-.35, .35)), (0.52 + rng.uniform(-.04, .04), rng.uniform(-.35, .35)),
             (0.76 + rng.uniform(-.03, .03), rng.uniform(-.35, .35))] for _ in spikes]
    shard_v = [[(rng.uniform(-0.5, 0.5) * S + (x0 * 2.2 * S), -rng.uniform(0.5, 1.1) * S, rng.normal(0, 7)) for _ in range(4)]
               for (x0, *_r) in spikes]
    TS = 8.6 * f
    frames = []
    for i in range(n):
        t = i * f
        cv = Cv()
        ground_fx(cv, t, f, cx, YG, CR(t), MD(t), chunks, dust, ("#6E6A72", "#9C99A4"))
        clip = np.clip(YG + 0.006 * S - YY, 0, 1)
        tip_main = None
        for k, (x0, h, w, lean, dl) in enumerate(spikes):
            gk = G(max(0, t - dl * f))
            hh, ww = h * S, w * S
            ang = math.radians(-lean)
            if t < TS:
                if gk <= 0.005:
                    continue
                stretch = max(1.0, gk)
                sink = (1 - min(gk, 1)) * (hh + 0.03 * S)
                hold = sstep(3.5 * f, 4.5 * f, t) * (1 - sstep(8 * f, 9 * f, t))
                wob = math.radians(1.6 * math.sin(TAU * 1.7 * (t - 4 * f) + k)) * hold
                faces = crystal_faces(ww / math.sqrt(stretch), hh * stretch)
                by = YG + sink + 0.02 * S
                fc = [(xf(p, cx + x0 * S, by, ang + wob), key) for p, key in faces]
                sh = [xf([(-0.5 * ww, 0.30 * hh * stretch), (0.2 * ww, 0.44 * hh * stretch), (0.2 * ww, 0.52 * hh * stretch),
                          (-0.5 * ww, 0.38 * hh * stretch)], cx + x0 * S, by, ang + wob),
                      xf([(-0.5 * ww, 0.50 * hh * stretch), (0.2 * ww, 0.62 * hh * stretch), (0.2 * ww, 0.645 * hh * stretch),
                          (-0.5 * ww, 0.525 * hh * stretch)], cx + x0 * S, by, ang + wob)]
                paint_faceted(cv, fc, pal, clip, sheen=sh)
                if k == 2:
                    tip_main = xf([(0.03 * ww, hh * stretch)], cx + x0 * S, by, ang + wob)[0]
            else:
                tau = t - TS
                faces = crystal_faces(ww, hh)
                ys = [0.0] + [c for c, _ in cuts[k]] + [1.2]
                for j in range(4):
                    lo_c, lo_s = (cuts[k][j - 1] if j > 0 else (-0.5, 0.0))
                    hi_c, hi_s = (cuts[k][j] if j < 3 else (1.5, 0.0))
                    piece = []
                    for p, key in faces:
                        q = p
                        # giữ y >= lo + s*x  và  y <= hi + s*x  (toạ độ cục bộ đã chuẩn hoá theo h, w)
                        q = clip_half(q, lo_s * hh / ww * 0.25, -1, lo_c * hh)
                        q = clip_half(q, -hi_s * hh / ww * 0.25, 1, -hi_c * hh)
                        if len(q) >= 3:
                            piece.append((q, key))
                    if not piece:
                        continue
                    allp = [pt for q, _ in piece for pt in q]
                    pcx = sum(p[0] for p in allp) / len(allp)
                    pcy = sum(p[1] for p in allp) / len(allp)
                    if j == 0:
                        sink = (hh * 0.35) * sstep(0, 0.25, tau)
                        fc = [(xf(q, cx + x0 * S, YG + 0.02 * S + sink, ang), key) for q, key in piece]
                        paint_faceted(cv, fc, pal, clip, alpha=1 - sstep(0.12, 0.27, tau))
                        continue
                    vx, vy, wv = shard_v[k][j]
                    base_pt = xf([(pcx, pcy)], cx + x0 * S, YG + 0.02 * S, ang)[0]
                    dx = vx * tau
                    dy = vy * tau + 0.5 * 4.0 * S * tau * tau
                    sc = 1 - 0.35 * sstep(0, 0.27, tau)
                    rot = wv * tau
                    fc = []
                    for q, key in piece:
                        qq = xf(q, cx + x0 * S, YG + 0.02 * S, ang)
                        qq = [((x - base_pt[0]) * sc, (y - base_pt[1]) * sc) for x, y in qq]
                        cr, sr = math.cos(rot), math.sin(rot)
                        qq = [(base_pt[0] + dx + x * cr - y * sr, base_pt[1] + dy + x * sr + y * cr) for x, y in qq]
                        fc.append((qq, key))
                    paint_faceted(cv, fc, pal, np.ones((S, S), f32), alpha=1 - sstep(0.14, 0.28, tau))
        # chớp sáng nhỏ ở đỉnh lúc bung
        fl = kf([(0, 0), (2 * f, 0), (2.6 * f, .6), (3 * f, 1), (4 * f, .45), (5 * f, 0), (1, 0)])(t)
        if fl > 0.02 and tip_main is not None:
            r = 0.085 * S * fl
            pts = star_pts(tip_main[0], tip_main[1], r, 4, 0.18, -math.pi / 2, np.random.default_rng(1), jit=0.0)
            cv.paint(polys_cov([pts]), C("#FFFBEA"))
            pts = star_pts(tip_main[0], tip_main[1], r * 0.55, 4, 0.22, -math.pi / 4, np.random.default_rng(1), jit=0.0)
            cv.paint(polys_cov([pts]), C(pal["t0"]), 0.9)
        md = MD(t)
        rx = 0.20 * S * (0.6 + 0.4 * md)
        ry = 0.038 * S * (0.7 + 0.5 * md)
        lip = cov(sd_ell(cx, YG, rx * 0.9, ry)) * np.clip(YY - YG + 0.2 * ry, 0, 1)
        cv.paint(lip, C(DIRT["base"]), min(1, md * 1.5))
        ground_fx(cv, t, f, cx, YG, 0, 0, chunks, dust, ("#6E6A72", "#9C99A4"), front=True)
        frames.append(cv.img())
    return frames


# ================================================================================================================ 8. HẠT RỜI
def h_luoilua(k):
    rng = np.random.default_rng(80 + k)
    cv = Cv()
    by = 0.95 * S
    cx = 0.5 * S
    specs = [(-4, 12, 40, 0.80, 0.30), (6, -18, -62, 0.82, 0.34), (-8, 22, 70, 0.74, 0.28), (3, -8, 35, 0.86, 0.36)][k]
    lean, bend, hook, hgt, wid = specs
    polys = []
    fn = lambda s: -90 + lean + bend * math.sin(math.pi * s * 1.25) + hook * s ** 3
    wp = lambda s: (1 - s) ** 0.85 * (0.8 + 0.35 * np.sin(np.pi * np.clip(s / 0.45, 0, 1)))
    p, cl = tongue_poly(cx, by, hgt * S, wid * S, fn, wp)
    polys.append(p)
    # lưỡi phụ nhỏ bên hông
    fn2 = lambda s: -90 + lean - 35 * (1 if hook > 0 else -1) + (-hook * 0.8) * s ** 2
    p2, _ = tongue_poly(cx - (0.05 if hook > 0 else -0.05) * S, by - 0.05 * S, hgt * S * 0.42, wid * S * 0.45, fn2, wp)
    polys.append(p2)
    if k in (1, 3):
        tip = cl[-1]
        fn3 = lambda s: -90 + hook * 0.8 * s ** 2
        p3, _ = tongue_poly(tip[0] + 0.02 * S, tip[1] - 0.025 * S, 0.08 * S, 0.035 * S, fn3,
                            lambda s: np.sin(np.pi * s) ** 0.7 * (1 - s) ** 0.6)
        polys.append(p3)
    c = polys_cov(polys)
    c = np.maximum(c, cov(sd_ell(cx, by - 0.08 * S, wid * S * 0.42, 0.08 * S)))
    c *= (YY < by)
    nz = [tnoise(S, S, 20, 9, 90 + k), tnoise(S, S, 26, 12, 95 + k)]
    fire_tones(cv, c, by, hgt * S, nz, 0, glow=0.0)
    return cv.img()


def h_quang():
    r = np.hypot(XX - S / 2, YY - S / 2) / (S / 2)
    a = 0.40 * (1 - sstep(0.0, 1.0, r)) ** 1.6
    cv = Cv()
    cv.paint(a, C("#F2521E"))
    return cv.img()


def h_giot(k):
    cv = Cv()
    cx, cy = 0.5 * S, 0.52 * S
    if k == 0:
        d = sd_circ(cx, cy, 0.36 * S)
    elif k == 1:   # giọt kéo đuôi, đầu tròn ở +x
        d = smin(sd_circ(cx + 0.12 * S, cy, 0.27 * S), sd_ell(cx - 0.16 * S, cy, 0.30 * S, 0.07 * S), 0.12 * S)
        d = np.maximum(d, -(XX - 0.06 * S))
    elif k == 2:   # mảng dẹt bay
        d = sd_ell(cx, cy, 0.40 * S, 0.22 * S, -0.35)
        d = smin(d, sd_circ(cx + 0.24 * S, cy - 0.16 * S, 0.12 * S), 0.08 * S)
    else:          # mảng vỡ nhiều múi
        d = sd_circ(cx - 0.06 * S, cy + 0.02 * S, 0.24 * S)
        for (ox, oy, rr) in ((0.20, -0.10, 0.15), (0.12, 0.18, 0.13), (-0.24, -0.16, 0.11), (-0.30, 0.16, 0.08)):
            d = smin(d, sd_circ(cx + ox * S, cy + oy * S, rr * S), 0.07 * S)
    c = cov(d)
    ys = np.where(c > 0.01, YY, np.nan)
    y0, y1 = np.nanmin(ys), np.nanmax(ys)
    v = np.clip((YY - y0) / max(y1 - y0, 1), 0, 1)
    col = ramp(W_GRAD, v)
    rim = np.clip(1 + d / 5.0, 0, 1)
    cv.paint(c, col * (1 - 0.22 * rim[..., None]))
    # ánh nhạt ở đáy trong khối
    xs = np.where(c > 0.01, XX, np.nan)
    x0, x1 = np.nanmin(xs), np.nanmax(xs)
    w = x1 - x0
    h = y1 - y0
    bc = cov(sd_ell((x0 + x1) / 2 + 0.05 * w, y1 - 0.22 * h, 0.34 * w, 0.14 * h, -0.1)) * cov(d + 0.06 * S)
    cv.paint(bc, C("#8FF5E6"), 0.65)
    # mảng sáng bầu dục lệch lên trái + đốm trắng
    cv.paint(cov(sd_ell(x0 + 0.33 * w, y0 + 0.28 * h, 0.17 * w, 0.10 * h, -0.6)) * c, C("#F2FDFF"))
    cv.paint(cov(sd_circ(x0 + 0.56 * w, y0 + 0.20 * h, 0.035 * min(w, h) + 2)) * c, C("#FFFFFF"))
    return cv.img()


def h_khoi(k):
    cv = Cv()
    rng = np.random.default_rng(300 + k)
    lobes = [(lx + rng.uniform(-.08, .08), ly + rng.uniform(-.08, .08), rx * rng.uniform(.85, 1.15),
              ry * rng.uniform(.85, 1.15), g) for (lx, ly, rx, ry, g) in KHOI_LOBES]
    if k == 3:
        lobes = lobes[3:]
    smoke_cluster(cv, 0.5 * S, 0.60 * S, 0.40 * S if k != 3 else 0.46 * S, lobes, 0.1 * k, 0.0, 0.0, 400 + k)
    return cv.img()


def h_tiachop(k):
    rng = np.random.default_rng(500 + k)
    cv = Cv()
    cx = cy = 0.5 * S
    g = 0.42 * np.exp(-(np.hypot(XX - cx, YY - cy) / (0.13 * S)) ** 2)
    cv.paint(g, C("#FF3A1E"))
    polys = []
    nr = 8 if k == 0 else 11
    for j in range(nr):
        a = TAU * j / nr + rng.uniform(-0.2, 0.2)
        ln = rng.uniform(0.30, 0.47) * S
        kink = rng.uniform(-14, 14)
        fn = lambda s, a=a, kk=kink: math.degrees(a) + kk * (s > 0.55)
        cl = angle_curve(cx, cy, ln, fn, 30)
        s = np.linspace(0, 1, 30)
        wv = rng.uniform(0.030, 0.045) * S * (1 - s) ** 1.3 * (1 + 0.6 * np.exp(-((s - 0.55) / 0.05) ** 2))
        polys.append(ribbon(cl, wv))
        if rng.random() < 0.5:   # nhánh phụ
            k2 = int(rng.integers(10, 20))
            b0 = cl[k2]
            fb = lambda s, a=a: math.degrees(a) + rng.choice([-1, 1]) * 30
            clb = angle_curve(b0[0], b0[1], ln * 0.25, fb, 12)
            sb = np.linspace(0, 1, 12)
            polys.append(ribbon(clb, 0.016 * S * (1 - sb) ** 1.2))
    polys.append(star_pts(cx, cy, 0.075 * S, 7, 0.55, rng.random(), rng, 0.3))
    c = polys_cov(polys)
    r = np.hypot(XX - cx, YY - cy)
    hot = 1 - np.clip(r / (0.32 * S), 0, 1)
    D = inner_dist(c)
    cv.paint(c, C(FIRE[0]))
    cv.paint(cov(3.0 - D) * c * (hot > 0.15), C(FIRE[1]))
    cv.paint(cov(5.0 + 10 * (1 - hot) - D) * c * (hot > 0.35), C(FIRE[2]))
    cv.paint(cov(sd_circ(cx, cy, 0.035 * S)) * c, C(FIRE[3]))
    return cv.img()


def h_vetlua(k):
    rng = np.random.default_rng(600 + k)
    cv = Cv()
    hx, hy = 0.93 * S, 0.52 * S
    polys = []
    nst = [5, 6, 4, 7][k]
    for j in range(nst):
        main = j == 0
        ln = (0.80 if main else rng.uniform(0.42, 0.78)) * S
        a0 = 180 + (0 if main else rng.uniform(-14, 14))
        curl = (rng.uniform(10, 26) if not main else 8) * (-1 if rng.random() < 0.7 else 1)
        fn = lambda s, a0=a0, c=curl: a0 + c * s ** 1.6
        cl = angle_curve(hx - (0 if main else rng.uniform(0.0, 0.10) * S), hy + (0 if main else rng.uniform(-0.03, 0.03) * S),
                         ln, fn, 40)
        s = np.linspace(0, 1, 40)
        W0 = (0.20 if main else rng.uniform(0.05, 0.09)) * S
        wv = W0 * np.clip(s / 0.22, 0, 1) ** 0.55 * (1 - s) ** 1.1
        polys.append(ribbon(cl, wv))
    c = polys_cov(polys)
    hot = np.clip((XX - 0.25 * S) / (0.65 * S), 0, 1)
    nz = [tnoise(S, S, 9, 26, 700 + k), tnoise(S, S, 11, 30, 710 + k)]
    D = inner_dist(c)
    n1 = nz[0]
    g = ndimage.gaussian_filter(c, 0.04 * S)
    cv.paint(np.clip(g * 1.6, 0, 1), C("#F0461E"), 0.30)
    cv.paint(c, C(FIRE[0]))
    cv.paint(cov(3.5 + 1.5 * n1 - D) * c, C(FIRE[1]))
    cv.paint(cov(16 - 12 * hot + 4 * nz[1] - D) * c, C(FIRE[2]))
    cv.paint(cov(36 - 26 * hot + 4 * n1 - D) * c, C(FIRE[3]))
    return cv.img()


# ============================================================================================================== ghi, xem
BG_SKY = (0x9F, 0xD3, 0xF0)
BG_SAND = (0xF3, 0xE2, 0xB8)


def bg(w, h, horizon):
    im = Image.new("RGB", (w, h), BG_SAND)
    ImageDraw.Draw(im).rectangle([0, 0, w, horizon], fill=BG_SKY)
    return im


def save_seq(name, frames):
    for i, fr in enumerate(frames):
        fr.save(os.path.join(OUT, f"{name}_{i}.png"))
    cols = 4
    rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGBA", (cols * N, rows * N), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        sheet.paste(fr, ((i % cols) * N, (i // cols) * N))
    sheet.save(os.path.join(OUT, f"{name}_to.png"))


def save_gif(name, frames, loop, scale=1.5, pause=9):
    sz = int(N * scale)
    w, h = sz + 40, sz + 30
    horizon = int(h * 0.52)
    out = []
    seq = list(frames) + ([] if loop else [None] * pause)
    for fr in seq:
        im = bg(w, h, horizon).convert("RGBA")
        if fr is not None:
            im.alpha_composite(fr.resize((sz, sz), Image.LANCZOS), (20, 10))
        out.append(im.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
    out[0].save(os.path.join(OUT, f"xem_{name}.gif"), save_all=True, append_images=out[1:], duration=33, loop=0,
                disposal=1, optimize=False)


def smooth_report(name, frames):
    al = [np.asarray(f, f32)[..., 3] / 255 for f in frames]
    rows = []
    for a, b in zip(al[:-1], al[1:]):
        inter = np.minimum(a, b).sum()
        uni = np.maximum(a, b).sum() + 1e-6
        rows.append(1 - inter / uni)
    ss = " ".join(f"{x:.2f}" for x in rows)
    print(f"  {name}: đổi hình giữa hai khung liền (1-IoU): {ss}")
    return rows


def font(sz):
    for p in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def load_seq(name):
    out = []
    i = 0
    while os.path.exists(os.path.join(OUT, f"{name}_{i}.png")):
        out.append(Image.open(os.path.join(OUT, f"{name}_{i}.png")).convert("RGBA"))
        i += 1
    return out


def ref_thumb(fname, box=None, h=200):
    p = os.path.join(REFS, fname)
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGB")
    if box:
        W, H = im.size
        im = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    w = int(im.size[0] * h / im.size[1])
    return im.resize((w, h), Image.LANCZOS)


def build_tong():
    rows = [("no", "Nổ 16 khung", ref_thumb("no_9khung.jpg")),
            ("nuoctoe", "Nước toé 16 khung", ref_thumb("nuoc_toe_16khung.jpg", (0, 0, 1, 0.72))),
            ("lua", "Lửa lặp 12 khung", ref_thumb("lua_khoi_comic.jpg", (0.27, 0.6, 0.67, 0.95))),
            ("khoi", "Khói tan 12 khung", ref_thumb("lua_khoi_comic.jpg", (0.34, 0.05, 0.63, 0.52))),
            ("loc", "Lốc năng lượng 12 khung", ref_thumb("loc_nang_luong.jpg", (0, 0, 0.52, 1))),
            ("gaila", "Gai lá 12 khung (không có mẫu)", None),
            ("gaisat", "Gai sắt 12 khung (không có mẫu)", None)]
    T = 118
    RW = 330
    fh = font(18)
    fs = font(14)
    hat = [f"h_luoilua_{i}" for i in range(4)] + ["h_quang"] + [f"h_giot_{i}" for i in range(4)] + \
          [f"h_khoi_{i}" for i in range(4)] + [f"h_tiachop_{i}" for i in range(2)] + [f"h_vetlua_{i}" for i in range(4)]
    width = RW + 16 * (T + 2) + 20
    rowh = T * 1 + 50
    height = 60 + rowh * (len(rows) + 1) + 40
    sheet = Image.new("RGB", (width, height), (40, 38, 44))
    dr = ImageDraw.Draw(sheet)
    dr.text((14, 14), "Bản mẫu VFX style mới (trái: ảnh mẫu thu nhỏ, chỉ để so; phải: từng khung bản của mình trên nền sân)",
            fill=(240, 240, 240), font=fh)
    y = 60
    for name, label, ref in rows:
        frames = load_seq(name)
        dr.text((14, y), label, fill=(255, 230, 160), font=fs)
        if ref is not None:
            r = ref.copy()
            r.thumbnail((RW - 20, T + 10))
            sheet.paste(r, (10, y + 22))
        else:
            dr.text((14, y + 60), "suy từ style 4 tờ mẫu", fill=(180, 180, 180), font=fs)
        for k, fr in enumerate(frames):
            tile = bg(T, T, int(T * 0.55)).convert("RGBA")
            tile.alpha_composite(fr.resize((T, T), Image.LANCZOS))
            sheet.paste(tile.convert("RGB"), (RW + k * (T + 2), y + 22))
            dr.text((RW + k * (T + 2) + 3, y + 24), str(k), fill=(60, 60, 60), font=fs)
        y += rowh
    dr.text((14, y), "Hạt rời: lưỡi lửa ×4, quầng, giọt ×4, khói ×4, tia chớp ×2, vệt lửa ×4", fill=(255, 230, 160), font=fs)
    for k, nm in enumerate(hat):
        p = os.path.join(OUT, nm + ".png")
        if not os.path.exists(p):
            continue
        fr = Image.open(p).convert("RGBA")
        tile = bg(T - 20, T - 20, int((T - 20) * 0.55)).convert("RGBA")
        tile.alpha_composite(fr.resize((T - 20, T - 20), Image.LANCZOS))
        sheet.paste(tile.convert("RGB"), (10 + k * (T - 18), y + 22))
    sheet.save(os.path.join(OUT, "xem_tong.png"))


SEQS = {
    "no": (no_frames, False),
    "nuoctoe": (nuoctoe_frames, False),
    "lua": (lua_frames, True),
    "khoi": (khoi_frames, False),
    "loc": (loc_frames, True),
    "gaila": (gaila_frames, False),
    "gaisat": (gaisat_frames, False),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    want = set(sys.argv[1:]) or set(SEQS) | {"hat"}
    for name, (fn, loop) in SEQS.items():
        if name not in want:
            continue
        print(f"{name} ...")
        fr = fn()
        save_seq(name, fr)
        save_gif(name, fr, loop)
        smooth_report(name, fr + ([fr[0]] if loop else []))
    if "hat" in want:
        print("hạt rời ...")
        for k in range(4):
            h_luoilua(k).save(os.path.join(OUT, f"h_luoilua_{k}.png"))
            h_giot(k).save(os.path.join(OUT, f"h_giot_{k}.png"))
            h_khoi(k).save(os.path.join(OUT, f"h_khoi_{k}.png"))
            h_vetlua(k).save(os.path.join(OUT, f"h_vetlua_{k}.png"))
        for k in range(2):
            h_tiachop(k).save(os.path.join(OUT, f"h_tiachop_{k}.png"))
        h_quang().save(os.path.join(OUT, "h_quang.png"))
    build_tong()
    print("xong:", OUT)


if __name__ == "__main__":
    main()
