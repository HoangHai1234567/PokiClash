# -*- coding: utf-8 -*-
"""Dò tự động chỗ đặt từng mảnh của dòng tm01 vào concept đã duyệt (như rig.place / thuy_long.place, viết lại không cần cv2):
mỗi mảnh (ảnh đã co về cỡ rig) đặt bằng Dat (x, y, góc, tỉ lệ sx, sy); chi phí = khoảng cách màu RGB giữa điểm mảnh và điểm concept
cùng chỗ (chặn trên 250), điểm rơi ra nền trắng của concept phạt 300. Dò kiểu xuống dốc từng tham số, bước co dần, giới hạn quanh
chỗ đặt ban đầu. Kết quả ghi inbox/tm01_<k>/khop.json để lần dựng sau dùng lại (lệnh `tm01.py khop <k>`)."""
import json
import math
import os

import numpy as np
from PIL import Image

from quai import anh
from quai.khung import Dat


class Concept:
    """concept đổi về lưới điểm 1 px = 1 đơn vị rig: (x, y) rig -> (cột, hàng) = (x + x0·S, y0·S − y)."""

    def __init__(self, path, doi):
        im = Image.open(path).convert("RGB")
        self.doi = doi
        w, h = im.size
        S = doi.S
        self.rgb = np.asarray(im.resize((max(2, int(round(w * S))), max(2, int(round(h * S)))), Image.LANCZOS)).astype(np.float32)
        full = ~anh.nen_tu_mep(np.asarray(im).min(axis=2) > 236)
        self.mask = np.asarray(Image.fromarray((full * 255).astype(np.uint8)).resize((self.rgb.shape[1], self.rgb.shape[0]),
                                                                                       Image.BILINEAR)) > 127
        self.ox, self.oy = doi.x0 * S, doi.y0 * S

    def sample(self, X, Y):
        c = np.round(X + self.ox).astype(int)
        r = np.round(self.oy - Y).astype(int)
        H, W = self.mask.shape
        ok = (c >= 0) & (r >= 0) & (c < W) & (r < H)
        col = np.zeros((len(X), 3), np.float32)
        m = np.zeros(len(X), bool)
        col[ok] = self.rgb[r[ok], c[ok]]
        m[ok] = self.mask[r[ok], c[ok]]
        return col, m


def _diem(im, buoc=2, vung=None):
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    ys, xs = np.mgrid[0:a.shape[0]:buoc, 0:a.shape[1]:buoc]
    ys, xs = ys.ravel(), xs.ravel()
    keep = a[ys, xs, 3] > 160
    if vung is not None:
        keep &= vung[ys, xs]
    xs, ys = xs[keep], ys[keep]
    return np.stack([xs + 0.5, ys + 0.5], 1), a[ys, xs, :3]


def chi_phi(P, col, conc, dat, w, h):
    V = dat.ra(P, w, h)
    cc, m = conc.sample(V[:, 0], V[:, 1])
    d = np.minimum(np.sqrt(((cc - col) ** 2).sum(1)), 250.0)
    d[~m] = 300.0
    return float(d.mean())


def _mk(dat, x, y, g, sx, sy):
    return Dat(x, y, goc=g, ti=(sx, sy), neo=dat.neo, lat=dat.lat, neo_px=dat.neo_px)


def do(im, dat0, conc, ten="", di=40.0, goc=25.0, ti=(0.7, 1.45), kieu="deu", vung=None, co_dinh=False, in_ra=True):
    """dò Dat cho ảnh im quanh dat0. kieu: 'deu' (tỉ lệ đều), 'hai' (sx, sy riêng), 'goc_ti' (giữ gốc neo, chỉ góc + tỉ lệ).
    vung: mặt nạ bool trên ảnh (chỉ dò theo phần này, vd phần cẳng tay). Trả (Dat, chi phí đầu, chi phí cuối)."""
    P, col = _diem(im, 2 if im.width * im.height > 6000 else 1, vung)
    w, h = im.size
    x0, y0, g0, sx0, sy0 = dat0.x, dat0.y, dat0.goc, dat0.sx, dat0.sy
    cur = [x0, y0, g0, sx0, sy0]
    f = lambda p: chi_phi(P, col, conc, _mk(dat0, *p), w, h)  # noqa: E731
    c0 = best = f(cur)
    steps = [8.0, 8.0, 4.0, 0.06, 0.06]
    free = [0, 1, 2, 3, 4] if kieu == "hai" else ([2, 3] if kieu == "goc_ti" else [0, 1, 2, 3])
    for _ in range(60):
        moved = False
        for i in free:
            for sgn in (1, -1):
                p = list(cur)
                if i == 3 and kieu != "hai":
                    p[3] = cur[3] * (1 + sgn * steps[3])
                    p[4] = cur[4] * (1 + sgn * steps[3])
                elif i in (3, 4):
                    p[i] = cur[i] * (1 + sgn * steps[i])
                else:
                    p[i] = cur[i] + sgn * steps[i]
                if math.hypot(p[0] - x0, p[1] - y0) > di or abs(p[2] - g0) > goc:
                    continue
                if not (ti[0] * sx0 <= p[3] <= ti[1] * sx0 and ti[0] * sy0 <= p[4] <= ti[1] * sy0):
                    continue
                c = f(p)
                if c < best - 1e-4:
                    best, cur, moved = c, p, True
        if not moved:
            steps = [s * 0.5 for s in steps]
            if steps[0] < 0.5 and steps[2] < 0.25:
                break
    if in_ra:
        print(f"  dò {ten}: chi phí {c0:.1f} → {best:.1f}; dời ({cur[0] - x0:+.1f}, {cur[1] - y0:+.1f}) góc {cur[2] - g0:+.1f}° "
              f"tỉ lệ {cur[3] / sx0:.3f}×{cur[4] / sy0:.3f}")
    return _mk(dat0, *cur), c0, best


class Khop:
    """giữ kết quả dò: che_do 'do' (dò và ghi), 'doc' (đọc khop.json), 'tat' (dùng chỗ đặt ban đầu)."""

    def __init__(self, path, che_do, conc=None):
        self.path, self.che_do, self.conc = path, che_do, conc
        self.kq = {}
        if che_do == "doc" and os.path.exists(path):
            self.kq = json.load(open(path, encoding="utf-8"))

    def dat(self, ten, im, dat0, **kw):
        if self.che_do == "do":
            d, c0, c1 = do(im, dat0, self.conc, ten=ten, **kw)
            self.kq[ten] = {"x": d.x, "y": d.y, "goc": d.goc, "sx": d.sx, "sy": d.sy, "cp0": round(c0, 2), "cp": round(c1, 2)}
            return d
        if ten in self.kq:
            r = self.kq[ten]
            return Dat(r["x"], r["y"], goc=r["goc"], ti=(r["sx"], r["sy"]), neo=dat0.neo, lat=dat0.lat, neo_px=dat0.neo_px)
        return dat0

    def luu(self):
        if self.che_do == "do":
            json.dump(self.kq, open(self.path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("  ghi", self.path)
