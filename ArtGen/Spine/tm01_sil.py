# -*- coding: utf-8 -*-
"""Dò bố trí cả con theo BÓNG DÁNG concept (dòng tm01): mỗi mảnh có tham số (vị trí, góc, tỉ lệ dọc / ngang), tay chân hai đoạn
gập theo dáng đứng; mặt nạ cả con dựng nhanh bằng phép biến hình affine từng mảnh (từng đoạn chi) lên lưới điểm của concept.
Hàm mục tiêu = IoU(mặt nạ cả con, mặt nạ concept) − hệ số × chi phí màu trung bình của các mảnh (giữ mảnh nằm đúng màu, không
trượt sang chỗ khác). Xuống dốc từng tham số, bước co dần, giới hạn quanh chỗ ban đầu (dời ±40 px rig, góc ±25°, tỉ lệ 0,75–1,4).

Dùng: bo = bo_tri(ts) (hàm của từng dạng, trả danh sách (ảnh, Dat, mặt nạ cắt ảnh hoặc None, tên)); toi_uu(ts, bo_tri, conc, ...)."""
import json
import math
import os

import numpy as np
from PIL import Image

import tm01_khop as KH


def _affine_ra_raster(dat, w, h, conc):
    """ma trận 3x3: px ảnh mảnh -> px lưới concept (cột, hàng)."""
    P = np.array([[0, 0], [w, 0], [0, h]], float)
    V = dat.ra(P, w, h)
    R = np.stack([V[:, 0] + conc.ox, conc.oy - V[:, 1]], 1)
    A = np.array([[R[1, 0] - R[0, 0], R[2, 0] - R[0, 0], R[0, 0]], [R[1, 1] - R[0, 1], R[2, 1] - R[0, 1], R[0, 1]], [0, 0, 1.0]])
    A[0, 0] /= w
    A[1, 0] /= w
    A[0, 1] /= h
    A[1, 1] /= h
    return A


def mat_na(bo, conc):
    H, W = conc.mask.shape
    out = np.zeros((H, W), bool)
    for im, dat, cat, _ in bo:
        a = im.getchannel("A")
        if cat is not None:
            a = Image.fromarray((np.asarray(a) * cat).astype(np.uint8))
        A = _affine_ra_raster(dat, im.width, im.height, conc)
        inv = np.linalg.inv(A)
        r = a.transform((W, H), Image.AFFINE, (inv[0, 0], inv[0, 1], inv[0, 2], inv[1, 0], inv[1, 1], inv[1, 2]), resample=Image.BILINEAR)
        out |= np.asarray(r) > 110
    return out


def iou(m, conc):
    return float((m & conc.mask).sum()) / max(1, float((m | conc.mask).sum()))


class Mau:
    """chi phí màu từng mảnh (cache điểm mẫu)."""

    def __init__(self):
        self.c = {}

    def __call__(self, bo, conc):
        tot, n = 0.0, 0
        for im, dat, cat, ten in bo:
            if ten is None:
                continue
            key = (ten, id(im))
            if key not in self.c:
                self.c[key] = KH._diem(im, 3, None if cat is None else cat > 0.5)
            P, col = self.c[key]
            tot += KH.chi_phi(P, col, conc, dat, im.width, im.height)
            n += 1
        return tot / max(1, n)


def toi_uu(ts, bo_tri, conc, gioi, mau_he=0.0012, vong=6, in_ra=True):
    """ts: dict tham số {khoá: số}; gioi: {khoá: (thấp, cao, bước)}. Sửa ts tại chỗ, trả (iou đầu, iou cuối)."""
    mau = Mau()

    def J(t):
        bo = bo_tri(t)
        return iou(mat_na(bo, conc), conc) - mau_he * mau(bo, conc)

    best = J(ts)
    i0 = iou(mat_na(bo_tri(ts), conc), conc)
    steps = {k: g[2] for k, g in gioi.items()}
    for v in range(vong):
        moved = 0
        for k, (lo, hi, _) in gioi.items():
            for sgn in (1, -1):
                t2 = dict(ts)
                t2[k] = min(hi, max(lo, ts[k] + sgn * steps[k]))
                if t2[k] == ts[k]:
                    continue
                j = J(t2)
                if j > best + 1e-5:
                    best, ts[k], moved = j, t2[k], moved + 1
                    break
        if in_ra:
            print(f"  vòng {v}: mục tiêu {best:.4f}, IoU {iou(mat_na(bo_tri(ts), conc), conc):.4f}, đổi {moved}")
        if not moved:
            steps = {k: s * 0.5 for k, s in steps.items()}
    return i0, iou(mat_na(bo_tri(ts), conc), conc)


def luu(ts, path):
    json.dump({k: round(float(v), 4) for k, v in ts.items()}, open(path, "w", encoding="utf-8"), indent=1)


def doc(path):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
