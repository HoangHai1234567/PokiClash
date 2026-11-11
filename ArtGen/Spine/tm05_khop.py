# -*- coding: utf-8 -*-
"""Khớp mảnh tm05 vào concept bằng dò tự động (như rig.place / thuy_long.place): mỗi mảnh dò tỉ lệ, góc, vị trí cực tiểu SQDIFF có
mặt nạ trên Lab, ba tầng (thô → vừa → mịn). Cần cv2: chạy bằng venv.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm05_khop.py <k>     ra inbox/tm05_<k>/rig/khop.json + khop_ghep.png (+ IoU)

khop.json: {mảnh: {s, r, cx, cy, err}}: ảnh mảnh (đã cắt sát theo alpha) phóng s, xoay r độ (ngược kim như mắt nhìn) quanh tâm,
tâm đặt ở (cx, cy) px concept. Mảnh vẽ thẳng rồi uốn theo đường cong (chân, xúc tu, lưỡi) và màng lòng miệng không dò ở đây.
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")


def lab_f(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)


def warp(rgba, s, r):
    h, w = rgba.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), r, s)
    c, si = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * si + w * c) + 2, int(h * c + w * si) + 2
    M[0, 2] += nw / 2 - w / 2
    M[1, 2] += nh / 2 - h / 2
    return cv2.warpAffine(rgba, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def match(R_lab, part, scales, rots, f, around=None, win=None):
    best = None
    R = cv2.resize(R_lab, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    for s in scales:
        for r in rots:
            wp = warp(part, s * f, r)
            if wp.shape[0] >= R.shape[0] or wp.shape[1] >= R.shape[1] or min(wp.shape[:2]) < 6:
                continue
            m = (wp[:, :, 3] > 200).astype(np.float32)
            area = m.sum()
            if area < 20:
                continue
            t = lab_f(np.ascontiguousarray(wp[:, :, :3]))
            res = cv2.matchTemplate(R, t, cv2.TM_SQDIFF, mask=np.dstack([m, m, m])) / area
            th, tw = wp.shape[:2]
            if around is not None:
                ys, xs = np.mgrid[0:res.shape[0], 0:res.shape[1]]
                cx, cy = (xs + tw / 2) / f, (ys + th / 2) / f
                res = np.where((np.abs(cx - around[0]) > win) | (np.abs(cy - around[1]) > win), np.inf, res)
            mn, _, loc, _ = cv2.minMaxLoc(res)
            if not np.isfinite(mn):
                continue
            if best is None or mn < best[0]:
                best = (float(mn), float(s), float(r), (loc[0] + tw / 2) / f, (loc[1] + th / 2) / f)
    return best


def tang(R_lab, part, c, around_win=(60, 14)):
    c = match(R_lab, part, np.arange(c[1] * 0.95, c[1] * 1.051, c[1] * 0.0125), np.arange(c[2] - 6, c[2] + 6.1, 2), 0.5, (c[3], c[4]), around_win[0])
    return match(R_lab, part, np.arange(c[1] * 0.985, c[1] * 1.016, c[1] * 0.005), np.arange(c[2] - 2, c[2] + 2.1, 1), 1.0, (c[3], c[4]), around_win[1])


def nap(path):
    im = Image.open(path).convert("RGBA")
    bb = im.getbbox()
    return np.array(im.crop(bb))


def khop(k):
    import tm05
    c = tm05.CFG[k]
    man = tm05.thu_muc(k, "manh")
    ref = np.array(Image.open(tm05.thu_muc(k, "tai_ve", "L1_chon.png")).convert("RGB"))
    R_lab = lab_f(ref)
    out = {}
    # hai nửa vỏ: dò thô cả ảnh quanh khung bao dự kiến
    for nm, box in (("tren", c["tren_box"]), ("duoi", c["duoi_box"])):
        p = os.path.join(man, nm + ".png")
        if not os.path.exists(p):
            continue
        part = nap(p)
        s0 = (box[2] - box[0]) / part.shape[1]
        ctr = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
        cc = match(R_lab, part, s0 * np.arange(0.8, 1.21, 0.04), range(-12, 13, 4), 0.25, ctr, 140)
        cc = tang(R_lab, part, cc)
        out[nm] = dict(zip(("err", "s", "r", "cx", "cy"), cc))
        print(f"  {nm:6s} s={cc[1]:.3f} r={cc[2]:+.0f} tâm=({cc[3]:.0f},{cc[4]:.0f}) sai={cc[0]:.0f}")
    # ngọc, mũ miện
    small = [("ngoc", c["ngoc"][0], c["ngoc"][1], 0)]
    if "mien" in c:
        small.append(("mien", (c["mien"][0][0], c["mien"][0][1] - 40), c["mien"][1], 0))
    for nm, ctr, wdt, r0 in small:
        p = os.path.join(man, nm + ".png")
        if not os.path.exists(p):
            continue
        part = nap(p)
        s0 = wdt / part.shape[1]
        cc = match(R_lab, part, s0 * np.arange(0.75, 1.26, 0.05), range(r0 - 12, r0 + 13, 4), 0.5, ctr, 80)
        cc = tang(R_lab, part, cc, (40, 10))
        out[nm] = dict(zip(("err", "s", "r", "cx", "cy"), cc))
        print(f"  {nm:6s} s={cc[1]:.3f} r={cc[2]:+.0f} tâm=({cc[3]:.0f},{cc[4]:.0f}) sai={cc[0]:.0f}")
    # gai: ảnh đứng (chân dưới); góc dự kiến theo chân → ngọn trong CFG
    for (nm, par, b, t), gim in zip(c["gai"], tm05.GAI_ANH[k]):
        p = os.path.join(man, gim + ".png")
        if not os.path.exists(p):
            continue
        part = nap(p)
        B, T = np.array(b, float), np.array(t, float)
        L = float(np.hypot(*(T - B)))
        a = math.degrees(math.atan2(-(T - B)[1], (T - B)[0]))   # góc màn hình (y lên)
        r0 = a - 90
        s0 = L * 1.12 / part.shape[0]
        ctr = (B + T) / 2
        cc = match(R_lab, part, s0 * np.arange(0.7, 1.31, 0.05), np.arange(r0 - 30, r0 + 31, 6), 0.5, ctr, 70)
        if cc is None:
            continue
        cc = tang(R_lab, part, cc, (30, 8))
        out[nm] = dict(zip(("err", "s", "r", "cx", "cy"), cc), anh=gim)
        print(f"  {nm:6s} ({gim}) s={cc[1]:.3f} r={cc[2]:+.0f} tâm=({cc[3]:.0f},{cc[4]:.0f}) sai={cc[0]:.0f}")
    ra = tm05.thu_muc(k, "rig")
    os.makedirs(ra, exist_ok=True)
    json.dump(out, open(os.path.join(ra, "khop.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # ghép thử các mảnh đã dò lên nền trắng, IoU với concept (chỉ phần mảnh đã dò)
    H, W = ref.shape[:2]
    comp = np.full((H, W, 3), 255, np.float32)
    mk = np.zeros((H, W), bool)
    order = [n for n in out if n.startswith("g")] + [n for n in ("ngoc", "duoi", "tren", "mien") if n in out]
    for nm in order:
        o = out[nm]
        part = nap(os.path.join(man, o.get("anh", nm) + ".png"))
        wp = warp(part, o["s"], o["r"])
        x0, y0 = int(round(o["cx"] - wp.shape[1] / 2)), int(round(o["cy"] - wp.shape[0] / 2))
        ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + wp.shape[1]), min(H, y0 + wp.shape[0])
        sub = wp[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0].astype(np.float32)
        al = sub[:, :, 3:4] / 255.0
        comp[ay0:ay1, ax0:ax1] = comp[ay0:ay1, ax0:ax1] * (1 - al) + sub[:, :, :3] * al
        mk[ay0:ay1, ax0:ax1] |= sub[:, :, 3] > 128
    Image.fromarray(np.hstack([ref, comp.astype(np.uint8)])).save(os.path.join(ra, "khop_ghep.png"))
    print(os.path.join(ra, "khop.json"))


if __name__ == "__main__":
    khop(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
