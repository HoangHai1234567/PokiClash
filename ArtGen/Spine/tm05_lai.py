# -*- coding: utf-8 -*-
"""Cách lai (đặc tả mục 5, chuẩn 2026-11-11): cắt thẳng từ concept các mảnh liền thân, không cần vẽ bù nhiều (hai nửa vỏ, gai, mũ
miện, xúc tu chân, xúc tu khoé hàm, chân mềm, râu); tờ GPT chỉ cho lòng miệng, ngọc, mí. Cần cv2: chạy bằng venv.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm05_lai.py <k>

Gán nhãn: nét mực (nâu đen, ít sắc) tách concept thành các cụm màu; mỗi cụm theo nhãn chiếm đa số trong bản đồ đa giác (ưu tiên:
gai > mũ miện > xúc tu > miệng/ngọc (theo màu) > chân > nửa trên / nửa dưới theo đường chia); nét mực và cụm vụn theo nhãn gần nhất.
Vẽ bù: chân gai lấn vào dưới vỏ, gốc xúc tu lấn vào dưới thân (loang màu chính mảnh), vì các mảnh đó vẽ SAU vỏ nên chỉ lộ khi lắc.
Ra inbox/tm05_<k>/manh_lai/<mảnh>.png, lai.json (khung bao trong concept, đường giữa xúc tu), nhan.png (bản đồ nhãn để soi).
"""
import heapq
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

import tm05  # noqa: E402
from quai import anh  # noqa: E402

# đa giác gán nhãn (px concept), theo thứ tự ưu tiên cao → thấp
VUNG = {
    2: dict(
        gai={"g0": [(355, 282), (400, 245), (470, 238), (525, 280), (540, 340), (470, 345), (400, 318)],
             "g1": [(395, 180), (440, 150), (520, 150), (585, 200), (598, 278), (540, 295), (490, 250), (430, 215)],
             "g2": [(485, 105), (540, 75), (620, 80), (690, 140), (705, 235), (620, 245), (560, 190)],
             "g3": [(620, 35), (680, 15), (760, 30), (840, 100), (855, 195), (760, 210), (700, 140)],
             "g4": [(850, 65), (880, 55), (925, 110), (932, 178), (895, 185), (865, 130)],
             "g5": [(315, 640), (380, 595), (440, 600), (470, 640), (440, 675), (330, 672)],
             "g6": [(350, 715), (410, 668), (470, 670), (490, 710), (455, 745), (360, 735)],
             "g7": [(420, 790), (470, 722), (520, 720), (540, 760), (500, 800), (430, 800)]},
        mien=[(810, 195), (860, 128), (940, 118), (1010, 150), (1055, 198), (1050, 238), (815, 238)],
        xt={"xt_a": [(1050, 440), (1132, 440), (1137, 528), (1050, 528)],
            "xt_b": [(1060, 548), (1142, 548), (1147, 642), (1060, 642)]},
        mieng_hop=(650, 380, 1060, 660), ngoc=((880, 532), 104),
        mat_hop={"mi_a": (883, 280, 965, 345), "mi_b": (980, 283, 1056, 345)},
        chan={"cbs": [(280, 790), (565, 780), (585, 860), (510, 955), (280, 955)],
              "cbt": [(592, 790), (720, 790), (745, 880), (725, 995), (505, 995), (515, 905), (560, 860)],
              "cfs": [(752, 795), (890, 795), (915, 880), (862, 948), (758, 948)],
              "cft": [(880, 770), (1192, 812), (1192, 988), (990, 978), (872, 892)]},
        goc_chan={"cbs": (540, 795), "cbt": (650, 800), "cfs": (815, 802), "cft": (915, 785)},
        goc_xt={"xt_a": (1052, 485), "xt_b": (1062, 600)},
        chia=[(380, 497), (520, 486), (600, 480), (700, 478), (800, 500), (900, 525), (1000, 520), (1250, 520)],
        day_vo=[(380, 760), (550, 790), (700, 815), (850, 812), (1000, 765), (1250, 765)],
    ),
    1: dict(
        gai={"g0": [(400, 350), (445, 335), (505, 360), (508, 445), (450, 448), (400, 395)],
             "g1": [(490, 255), (545, 248), (600, 300), (600, 358), (530, 360), (490, 300)],
             "g2": [(620, 178), (680, 175), (725, 255), (725, 298), (620, 300), (615, 250)],
             "g3": [(752, 160), (820, 158), (858, 240), (858, 280), (755, 280), (750, 230)],
             "g4": [(895, 210), (960, 205), (1002, 270), (1000, 335), (930, 335), (895, 290)],
             "g5": [(490, 702), (575, 700), (580, 772), (495, 780)],
             "g6": [(595, 730), (680, 730), (685, 802), (600, 806)]},
        xt={"xt_a": [(1002, 432), (1165, 432), (1165, 487), (1002, 492)],
            "xt_b": [(1002, 495), (1170, 487), (1170, 545), (1002, 545)],
            "xt_c": [(1002, 548), (1170, 545), (1170, 628), (1002, 628)]},
        mieng_hop=(640, 500, 1010, 650), ngoc=((862, 600), 50),
        mat_hop={"mi_a": (816, 450, 900, 517), "mi_b": (910, 416, 1008, 502)},
        chan={"chan": [(745, 748), (955, 748), (960, 836), (745, 836)]},
        goc_chan={"chan": (790, 752)},
        goc_xt={"xt_a": (1004, 470), "xt_b": (1004, 512), "xt_c": (1004, 560)},
        chia=[(380, 565), (520, 600), (600, 628), (700, 636), (800, 632), (900, 630), (1000, 606), (1250, 600)],
        day_vo=[(380, 760), (600, 780), (745, 760), (760, 748), (950, 748), (1000, 720), (1250, 700)],
    ),
}
TRUOC = {"g": "tren", "xt": "duoi", "chan": "duoi"}   # mũ miện vẽ TRƯỚC vỏ: không vẽ bù   # mảnh nằm sau mảnh nào (vẽ bù lấn vào)


def ve_da_giac(shape, pts, val, lab):
    m = np.zeros(shape, np.uint8)
    cv2.fillPoly(m, [np.array(pts, np.int32)], 1)
    lab[m > 0] = val


def duoi_duong(shape, line):
    """mặt nạ phía DƯỚI đường gấp khúc (y lớn hơn)."""
    H, W = shape
    xs = np.arange(W)
    L = np.array(line, float)
    yl = np.interp(xs, L[:, 0], L[:, 1])
    return np.arange(H)[:, None] > yl[None, :]


def duong_giua(mask, goc):
    """đường giữa của dải cong: gốc = điểm mặt nạ gần `goc` nhất, ngọn = điểm xa nhất theo đường đi trong hình; đường đi ngắn
    nhất có trọng số (ưu tiên đi giữa hình theo biến đổi khoảng cách). Trả list điểm (x, y)."""
    dt = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 5)
    H, W = mask.shape
    ys, xs = np.nonzero(mask)
    j = int(np.argmin((xs - goc[0]) ** 2 + (ys - goc[1]) ** 2))
    src = (ys[j], xs[j])

    def dijk(s, cost):
        D = np.full((H, W), np.inf)
        prev = {}
        D[s] = 0
        h = [(0.0, s)]
        nb = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1), (-1, -1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (1, 1, 1.414)]
        while h:
            d, (y, x) = heapq.heappop(h)
            if d > D[y, x]:
                continue
            for dy, dx, l in nb:
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and mask[yy, xx]:
                    nd = d + l * cost[yy, xx]
                    if nd < D[yy, xx]:
                        D[yy, xx] = nd
                        prev[(yy, xx)] = (y, x)
                        heapq.heappush(h, (nd, (yy, xx)))
        return D, prev

    D, _ = dijk(src, np.ones((H, W)))
    D2 = np.where(np.isfinite(D), D, -1)
    tip = np.unravel_index(int(np.argmax(D2)), D2.shape)
    cost = 1.0 / (0.5 + dt)
    _, prev = dijk(src, cost)
    path = [tip]
    while path[-1] != src and path[-1] in prev:
        path.append(prev[path[-1]])
    path = path[::-1]
    return [(float(x), float(y)) for y, x in path], float(dt.max())


def to_phang(rgb, mau, vung, hat=3):
    """tô phẳng vùng `vung` bằng màu `mau` kèm vân chì nhẹ (nhiễu kéo xiên), không loang vệt."""
    H, W = vung.shape
    rng = np.random.RandomState(hat)
    n = rng.normal(0, 1, (H, W)).astype(np.float32)
    k = np.zeros((7, 7), np.float32)
    for i in range(7):
        k[6 - i, i] = 1.0 / 7
    n = cv2.filter2D(n, -1, k) * 9.0
    out = rgb.copy()
    v = np.clip(np.asarray(mau, np.float32)[None, None, :] + n[..., None], 0, 255).astype(np.uint8)
    out[vung] = v[vung]
    return out


def mau_chinh(rgb, m):
    """màu chủ đạo của vùng (trung vị theo cụm màu đông nhất)."""
    px = rgb[m].reshape(-1, 3).astype(int)
    if not len(px):
        return np.array([128, 128, 128])
    q = (px // 24)
    key = q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2]
    vals, cnt = np.unique(key, return_counts=True)
    top = vals[np.argmax(cnt)]
    return np.median(px[key == top], axis=0)


def loang(rgb, base, vung, lan=40):
    """màu của vùng `vung` lấy theo điểm `base` gần nhất (loang dần bằng làm mờ hộp)."""
    c3 = rgb.astype(np.float32) * base[..., None]
    cur = base.astype(np.float32).copy()
    need = vung & ~base
    for _ in range(lan):
        if not (need & (cur == 0)).any():
            break
        c3b = cv2.blur(c3, (5, 5))
        wb = cv2.blur(cur, (5, 5))
        add = (wb > 1e-3) & (cur == 0)
        c3[add] = (c3b[add] / wb[add][:, None])
        cur[add] = 1.0
    out = rgb.copy()
    ok = need & (cur > 0)
    out[ok] = np.clip(c3[ok], 0, 255).astype(np.uint8)
    return out


def luu(ra, n, col, alpha, out, extra=None, pad=3):
    H, W = alpha.shape
    ys, xs = np.nonzero(alpha > 0)
    bx0, by0, bx1, by1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W, xs.max() + 1 + pad), min(H, ys.max() + 1 + pad)
    im = np.dstack([col[by0:by1, bx0:bx1], (np.clip(alpha[by0:by1, bx0:bx1], 0, 1) * 255).astype(np.uint8)])
    Image.fromarray(im, "RGBA").save(os.path.join(ra, n + ".png"))
    e = {"x0": int(bx0), "y0": int(by0), "x1": int(bx1), "y1": int(by1)}
    e.update(extra or {})
    out[n] = e
    return e


def mieng_ngoc_mi(k, V, rgb, full, idx, ink, fg, ra, out):
    """lòng miệng, ngọc, mí lấy từ concept: lòng miệng = vùng đỏ mâm xôi + chỗ ngọc, loang màu lấn vào dưới hai nửa vỏ (khuất,
    đủ cho lúc há to); ngọc = vòng tròn khép lại chỗ răng che (loang màu + vẽ nốt viền mực); mí = mảng da phủ kín cả con mắt
    (bao lồi tròng trắng + mống + con ngươi, nới 5 px) có nét mắt nhắm."""
    H, W = full.shape
    ker = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))  # noqa: E731
    mi_ = full == idx["mieng"]
    ng = full == idx["ngoc"]
    host = (full == idx["tren"]) | (full == idx["duoi"])
    lift = 58 if k == 2 else 40
    reg = mi_ | ng | ((cv2.dilate((mi_ | ng).astype(np.uint8), ker(lift)) > 0) & host)
    # dải dọc đường môi từ bản lề tới miệng (khe hai vỏ khi há), khuất sau hai nửa vỏ
    cfg = tm05.CFG[k]
    band = np.zeros((H, W), np.uint8)
    for line in (cfg["U"], cfg["D"]):
        cv2.polylines(band, [np.array(line, np.int32)], False, 1, thickness=int(lift * 1.4))
    hx, hy = cfg["H"]
    cv2.circle(band, (int(hx), int(hy)), int(lift * 0.5), 1, -1)
    reg |= (band > 0) & host
    r_, g_, b_ = [rgb[..., i].astype(int) for i in range(3)]
    rasp = mi_ & ~ink & (r_ - g_ > 60)
    mc = mau_chinh(rgb, rasp)
    col = to_phang(rgb, mc, reg & ~rasp, hat=11)
    a = cv2.GaussianBlur(reg.astype(np.float32), (0, 0), 0.7)
    luu(ra, "long", col, np.where(reg, 1.0, a * 0), out)
    print(f"  long   lòng miệng từ concept: {int(mi_.sum())} px đỏ + {int(reg.sum() - mi_.sum())} px loang (chỗ ngọc, lấn dưới vỏ)")
    # ngọc: khớp vòng tròn theo viền mực quanh vùng ngọc
    (cx0, cy0), r0 = V["ngoc"]
    ring = (cv2.dilate(ng.astype(np.uint8), ker(7)) > 0) & ink
    ys, xs = np.nonzero(ring)
    A = np.stack([xs, ys, np.ones_like(xs)], 1).astype(float)
    bb = -(xs.astype(float) ** 2 + ys.astype(float) ** 2)
    sol = np.linalg.lstsq(A, bb, rcond=None)[0]
    cx, cy = -sol[0] / 2, -sol[1] / 2
    rr = float(np.sqrt(cx * cx + cy * cy - sol[2]))
    # ink thickness ~ median distance spread
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx - cx, yy - cy)
    th = 3.5 if k == 1 else 4.5
    inside = d < rr - th
    rimz = (d >= rr - th) & (d <= rr + th)
    keep = ng & inside & ~ink
    colp = to_phang(rgb, mau_chinh(rgb, keep), inside & ~keep, hat=13)
    inkc = np.median(rgb[ink & (d < rr + 30)], axis=0).astype(np.uint8)
    colp[rimz] = inkc
    vis = ring & rimz
    colp[vis] = rgb[vis]
    ap = np.clip(rr + th + 0.5 - d, 0, 1)
    luu(ra, "ngoc", colp, ap, out, {"cx": float(cx), "cy": float(cy), "r": rr})
    print(f"  ngoc   vòng tròn tâm ({cx:.0f},{cy:.0f}) bán kính {rr:.0f}, khép {int((inside & ~keep).sum())} px chỗ bị che")
    # mí
    for n, (x0, y0, x1, y1) in V["mat_hop"].items():
        box = np.zeros((H, W), bool)
        box[y0:y1, x0:x1] = True
        r_, g_, b_ = [rgb[..., i].astype(int) for i in range(3)]
        light = np.minimum(np.minimum(r_, g_), b_) > 190
        warm = (r_ > 170) & (r_ - b_ > 70) & (g_ > 80)
        pupil = (b_ > r_ + 25) & (np.maximum(np.maximum(r_, g_), b_) < 140) & (g_ < 90)
        # lõi mắt theo màu: tròng trắng (sáng, ít sắc, chịu vân sáp), mống ấm, con ngươi sẫm xanh; bao lồi rồi nới bằng viền mực
        whit = (np.minimum(np.minimum(r_, g_), b_) > 160) & ((np.maximum(np.maximum(r_, g_), b_) - np.minimum(np.minimum(r_, g_), b_)) < 45)
        cand = box & (full == idx["tren"]) & (whit | warm | pupil)
        nc3, cc3, st3, _ = cv2.connectedComponentsWithStats(cand.astype(np.uint8), connectivity=8)
        if nc3 > 1:   # bỏ vụn (giữ cụm >= 4% cụm lớn nhất)
            mx = st3[1:, cv2.CC_STAT_AREA].max()
            keep3 = [q for q in range(1, nc3) if st3[q, cv2.CC_STAT_AREA] >= 0.04 * mx]
            cand = np.isin(cc3, keep3)
        ys, xs = np.nonzero(cand)
        pts = np.stack([xs, ys], 1).astype(np.int32)
        hull = cv2.convexHull(pts)
        eye = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(eye, hull, 1)
        eye = eye > 0
        lid = cv2.dilate(eye.astype(np.uint8), ker(10 if k == 1 else 8)) > 0
        # màu mí = màu điểm da gần nhất quanh mắt (không lấy mực, tròng trắng, mống): mép mí liền màu với mặt
        bad = cv2.dilate((ink | light | warm | pupil).astype(np.uint8), ker(2)) > 0
        src = (cv2.dilate(lid.astype(np.uint8), ker(18)) > 0) & ~lid & (full == idx["tren"]) & ~bad
        if k == 1:   # dạng 1: chỉ lấy màu da ngọc lam (không kéo mảng xanh vỏ vào mí)
            sk0 = mau_chinh(rgb, src)
            src &= np.abs(rgb.astype(int) - sk0[None, None, :].astype(int)).sum(2) < 110
        _, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys2, xs2 = np.nonzero(src)
        tab = np.zeros((li.max() + 1, 3), np.uint8)
        tab[li[ys2, xs2]] = rgb[ys2, xs2]
        near = tab[li]
        colm = rgb.copy()
        colm[lid] = near[lid]
        sm = cv2.GaussianBlur(colm, (0, 0), 1.6)
        colm[lid] = sm[lid]
        rng = np.random.RandomState(7)
        noise = rng.normal(0, 4, (H, W, 1))
        colm = np.clip(colm.astype(float) + noise, 0, 255).astype(np.uint8)
        # nét mắt nhắm: cung võng xuống qua 58% chiều cao mắt, dày như nét mực
        ey, ex = np.nonzero(eye)
        ax0, ax1, ay0, ay1 = ex.min(), ex.max(), ey.min(), ey.max()
        im = Image.fromarray(colm)
        from PIL import ImageDraw
        dr = ImageDraw.Draw(im)
        w_ = ax1 - ax0
        h_ = ay1 - ay0
        yc = ay0 + 0.52 * h_
        sag = 0.22 * h_
        pts2 = [(ax0 + 0.08 * w_ + t * 0.84 * w_, yc + sag * 4 * t * (1 - t)) for t in np.linspace(0, 1, 24)]
        dr.line(pts2, fill=tuple(int(v) for v in inkc), width=6 if k == 2 else 7, joint="curve")
        colm = np.array(im)
        al = cv2.GaussianBlur(lid.astype(np.float32), (0, 0), 0.8)
        al = np.where(lid, 1.0, al)
        cover = bool(np.all(lid[eye]))
        luu(ra, n, colm, al, out, {"phu": int((eye & ~lid).sum())})
        print(f"  {n}   mí từ concept: mắt {int(eye.sum())} px, còn hở {int((eye & ~lid).sum())} px" + (" (phủ kín)" if cover else ""))


def cat(k):
    V = VUNG[k]
    src = tm05.thu_muc(k, "tai_ve", "L1_chon.png")
    rgb = np.array(Image.open(src).convert("RGB"))
    H, W = rgb.shape[:2]
    r, g, b = [rgb[..., i].astype(int) for i in range(3)]
    bg = anh.nen_tu_mep(rgb.min(axis=2) > 236)
    fg = ~bg
    ink = fg & (np.maximum(np.maximum(r, g), b) < 80) & ((b - r) < 30)
    # bản đồ nhãn đa giác (ưu tiên thấp vẽ trước)
    names = ["tren", "duoi"] + list(V["chan"]) + ["mieng", "ngoc"] + list(V["xt"]) + (["mien"] if "mien" in V else []) + list(V["gai"])
    idx = {n: i + 1 for i, n in enumerate(names)}
    P = np.full((H, W), idx["tren"], np.int32)
    P[duoi_duong((H, W), V["chia"])] = idx["duoi"]
    for n, pg in V["chan"].items():
        m = np.zeros((H, W), np.uint8)
        cv2.fillPoly(m, [np.array(pg, np.int32)], 1)
        P[(m > 0) & duoi_duong((H, W), V["day_vo"])] = idx[n]
    x0, y0, x1, y1 = V["mieng_hop"]
    box = np.zeros((H, W), bool)
    box[y0:y1, x0:x1] = True
    rasp = box & (r > 105) & (g < 80) & (r - b > 35)
    P[rasp] = idx["mieng"]
    (cx, cy), rr = V["ngoc"]
    yy, xx = np.mgrid[0:H, 0:W]
    pearl = ((xx - cx) ** 2 + (yy - cy) ** 2 < rr * rr) & (np.minimum(np.minimum(r, g), b) > 165)
    P[pearl] = idx["ngoc"]
    for n, pg in V["xt"].items():
        ve_da_giac((H, W), pg, idx[n], P)
    if "mien" in V:
        ve_da_giac((H, W), V["mien"], idx["mien"], P)
    for n, pg in V["gai"].items():
        ve_da_giac((H, W), pg, idx[n], P)
    # cụm màu giữa các nét mực, mỗi cụm theo nhãn đa số
    reg = (fg & ~ink).astype(np.uint8)
    nc, comp, st, _ = cv2.connectedComponentsWithStats(reg, connectivity=4)
    lab = np.zeros((H, W), np.int32)
    giay = []
    for i in range(1, nc):
        area = st[i, cv2.CC_STAT_AREA]
        if area < 25:
            continue
        m = comp == i
        v = np.bincount(P[m], minlength=len(names) + 1)
        best = int(np.argmax(v))
        lab[m] = best
        # giấy trắng khép kín sát chân gai (vòng trắng): bỏ, chân gai vẽ bù phía sau sẽ lấp
        nm_b = names[best - 1]
        in_eye = any(st[i, cv2.CC_STAT_LEFT] >= bx[0] - 5 and st[i, cv2.CC_STAT_TOP] >= bx[1] - 5 and
                     st[i, cv2.CC_STAT_LEFT] + st[i, cv2.CC_STAT_WIDTH] <= bx[2] + 5 and st[i, cv2.CC_STAT_TOP] + st[i, cv2.CC_STAT_HEIGHT] <= bx[3] + 5
                     for bx in V["mat_hop"].values())
        if (nm_b.startswith("g") or nm_b in ("tren", "duoi")) and not in_eye and area < 8000 and                 np.minimum(np.minimum(r[m], g[m]), b[m]).mean() > 222:
            lab[m] = 0
            giay.append(i)
    # nét mực, cụm vụn: theo nhãn gần nhất (chỉ trong fg)
    have = lab > 0
    _, li = cv2.distanceTransformWithLabels((~have).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(have)
    table = np.zeros(li.max() + 1, np.int32)
    table[li[ys, xs]] = lab[ys, xs]
    full = np.where(fg, table[li], 0)
    # vòng giấy trắng quanh chân gai: về vỏ chủ (nửa trên / dưới), tô phẳng màu vỏ (không còn khe trắng ở chân gai)
    giay_m = np.zeros((H, W), bool)
    for i in giay:
        gm = comp == i
        near = cv2.dilate(gm.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))) > 0
        v = np.bincount(full[near & ~gm & ((full == idx["tren"]) | (full == idx["duoi"]))], minlength=len(names) + 1)
        host_i = idx["tren"] if v[idx["tren"]] >= v[idx["duoi"]] else idx["duoi"]
        full[gm] = host_i
        giay_m |= gm
    # điểm giấy trắng trong vỏ sát chân gai (vòng trắng liền cụm với màu vỏ): tô màu vỏ
    spm = np.isin(full, [idx[n] for n in V["gai"]]).astype(np.uint8)
    near_sp = cv2.dilate(spm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) > 0
    eyeb = np.zeros((H, W), bool)
    for bx in V["mat_hop"].values():
        eyeb[bx[1]:bx[3], bx[0]:bx[2]] = True
    wpx = near_sp & ~eyeb & (np.minimum(np.minimum(r, g), b) > 205) & ((full == idx["tren"]) | (full == idx["duoi"]))
    wpx = cv2.dilate(wpx.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    giay_m |= wpx & ((full == idx["tren"]) | (full == idx["duoi"])) & ~ink
    print(f"  giấy trắng sát chân gai tô màu vỏ: {int(giay_m.sum())} px")
    # ảnh nhãn để soi
    rng = np.random.RandomState(5)
    pal = rng.randint(40, 255, (len(names) + 1, 3))
    pal[0] = 255
    vis = (pal[full] * 0.55 + rgb * 0.45).astype(np.uint8)
    ra = tm05.thu_muc(k, "manh_lai")
    os.makedirs(ra, exist_ok=True)
    rig = tm05.thu_muc(k, "rig")
    os.makedirs(rig, exist_ok=True)
    Image.fromarray(vis).save(os.path.join(rig, "nhan.png"))
    out = {}
    keep = [n for n in names if n not in ("mieng", "ngoc")]
    for n in keep:
        m = full == idx[n]
        nc2, cc2, st2, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
        if nc2 > 2:   # bỏ mẩu vụn rời (giữ cụm >= 3% cụm lớn nhất)
            big = st2[1:, cv2.CC_STAT_AREA].max()
            for q in range(1, nc2):
                if st2[q, cv2.CC_STAT_AREA] < 0.06 * big:
                    m[cc2 == q] = False
        if m.sum() < 50:
            print("  thiếu mảnh", n)
            continue
        host = TRUOC.get("g" if n.startswith("g") else ("xt" if n.startswith("xt") else ("chan" if n in V["chan"] else n)))
        grow = None
        if host:
            if n in ("g5", "g6", "g7"):
                host = "duoi"
            hm = full == idx[host]
            if n.startswith("xt"):
                hm = (full == idx["tren"]) | (full == idx["duoi"])
            rad = 9 if n.startswith("g") else 26
            if n.startswith("g"):   # chân gai: vòng giấy đã bỏ cũng lấp
                hm = hm | (fg & (full == 0))
            grow = (cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rad + 1, 2 * rad + 1))) > 0) & hm & ~m
        alpha = m.astype(np.float32)
        col = rgb.copy()
        if n in ("tren", "duoi") and (giay_m & m).any():
            gm = giay_m & m
            near = (cv2.dilate(gm.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) > 0) & m & ~gm & ~ink
            dark = np.maximum(np.maximum(r, g), b) < 60
            col = to_phang(col, mau_chinh(rgb, near & ~dark), gm, hat=21)
        if grow is not None and grow.any():
            dark = np.maximum(np.maximum(r, g), b) < 110
            light = np.minimum(np.minimum(r, g), b) > 215
            mc = mau_chinh(rgb, m & ~ink & ~dark & ~light)
            col = to_phang(rgb, mc, grow, hat=len(out) + 3)
            alpha[grow] = 1.0
        a = cv2.GaussianBlur(alpha, (0, 0), 0.7)
        a = np.where(alpha > 0, np.maximum(a, alpha * 0.999), a)
        ys2, xs2 = np.nonzero(alpha > 0)
        bx0, by0, bx1, by1 = xs2.min(), ys2.min(), xs2.max() + 1, ys2.max() + 1
        pad = 3
        bx0, by0, bx1, by1 = max(0, bx0 - pad), max(0, by0 - pad), min(W, bx1 + pad), min(H, by1 + pad)
        im = np.dstack([col[by0:by1, bx0:bx1], (np.clip(a[by0:by1, bx0:bx1], 0, 1) * 255).astype(np.uint8)])
        Image.fromarray(im, "RGBA").save(os.path.join(ra, n + ".png"))
        e = {"x0": int(bx0), "y0": int(by0), "x1": int(bx1), "y1": int(by1)}
        # nhãn đúng (không gồm vùng vẽ bù) cũng lưu để soi
        if n in V["chan"] or n.startswith("xt"):
            goc = (V["goc_chan"].get(n) if n in V["chan"] else V["goc_xt"][n])
            path, th = duong_giua(m | (grow if grow is not None else False), goc)
            e["duong"] = path[::max(1, len(path) // 40)] + [path[-1]]
            e["day"] = th
        out[n] = e
        print(f"  {n:6s} {bx1 - bx0}x{by1 - by0} tại ({bx0},{by0})" + (f", vẽ bù {int(grow.sum())} px" if grow is not None else "")
              + (f", đường giữa {len(e['duong'])} điểm, dày tối đa {2 * e['day']:.0f}" if "duong" in e else ""))
    mieng_ngoc_mi(k, V, rgb, full, idx, ink, fg, ra, out)
    json.dump(out, open(os.path.join(ra, "lai.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(os.path.join(rig, "nhan.png"))


if __name__ == "__main__":
    cat(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
