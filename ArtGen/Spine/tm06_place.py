# -*- coding: utf-8 -*-
"""tm06: dò vị trí, tỉ lệ (ngang, dọc), góc của từng mảnh GPT trên concept đã chọn (SQDIFF có mặt nạ trên Lab: dò thô quanh gợi ý
đọc trên concept kẻ lưới rồi dò tinh). Mảnh dài vẽ duỗi thẳng (lá mang) đặt theo hai đầu khớp đọc trên concept. Ra
inbox/tm06_<k>/place.json (toạ độ concept px; tâm ảnh mảnh đã cắt sát) và rig/so_ghep.png (concept | ghép mảnh | khác biệt) + IoU.
Cần cv2:

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm06_place.py 1 [mảnh ...]
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm06"

from tm06_cfg import DRAW, HINT, NOI, TWO  # noqa: E402


def inbox(k, *p):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", *p)


def fg_mask(rgb, light=222, sat=32):
    mn = rgb.min(2).astype(np.int16)
    mx = rgb.max(2).astype(np.int16)
    lite = ((mn > light) & (mx - mn < sat)).astype(np.uint8)
    n, lab = cv2.connectedComponents(lite, connectivity=4)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0]) & (lite > 0)
    fg = (~bg).astype(np.uint8)
    return cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))


def lab_f(rgb):
    return cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2LAB).astype(np.float32)


def nap(k, img):
    im = Image.open(inbox(k, "manh", img + ".png")).convert("RGBA")
    bb = im.getbbox()
    return np.array(im.crop(bb))


def bien_doi(rgba, sx, sy, r, lat):
    """lật (nếu cần), co (sx, sy), xoay r độ quanh tâm; trả ảnh vừa khít và ma trận 2x3 (toạ độ ảnh gốc → ảnh ra)."""
    im = rgba[:, ::-1] if lat else rgba
    h, w = im.shape[:2]
    S = np.array([[sx, 0, 0], [0, sy, 0]], float)
    c, s = math.cos(math.radians(r)), math.sin(math.radians(r))
    R = np.array([[c, s], [-s, c]])                      # xoay ngược kim như mắt nhìn (trục y xuống)
    corners = np.array([[0, 0], [w, 0], [w, h], [0, h]], float) * [sx, sy]
    ctr = np.array([w * sx / 2, h * sy / 2])
    rc = (corners - ctr) @ R.T
    nw, nh = int(np.ceil(np.ptp(rc[:, 0]))) + 2, int(np.ceil(np.ptp(rc[:, 1]))) + 2
    M = np.zeros((2, 3))
    M[:, :2] = R @ S[:, :2]
    M[:, 2] = np.array([nw / 2, nh / 2]) - R @ ctr
    out = cv2.warpAffine(im, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return out


def do(ref_lab, part, lat, sxs, sys_, rots, f, quanh, win, gamma=1.0):
    best = None
    R = cv2.resize(ref_lab, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    for sx in sxs:
        for sy0 in sys_:
            sy = sx if sy0 is None else sy0
            for r in rots:
                wp = bien_doi(part, sx * f, sy * f, r, lat)
                if wp.shape[0] >= R.shape[0] or wp.shape[1] >= R.shape[1] or min(wp.shape[:2]) < 6:
                    continue
                m = (wp[:, :, 3] > 200).astype(np.float32)
                area = m.sum()
                if area < 20:
                    continue
                t = lab_f(wp[:, :, :3])
                res = cv2.matchTemplate(R, t, cv2.TM_SQDIFF, mask=np.dstack([m, m, m])) / area ** gamma
                th, tw = wp.shape[:2]
                ys, xs = np.mgrid[0:res.shape[0], 0:res.shape[1]]
                cx, cy = (xs + tw / 2) / f, (ys + th / 2) / f
                bad = (np.abs(cx - quanh[0]) > win) | (np.abs(cy - quanh[1]) > win)
                res = np.where(bad, np.inf, res)
                mn, _, loc, _ = cv2.minMaxLoc(res)
                if not np.isfinite(mn):
                    continue
                if best is None or mn < best[0]:
                    best = (mn, sx, sy, r, (loc[0] + tw / 2) / f, (loc[1] + th / 2) / f)
    return best


def dat_hai_dau(part, q0, q1, day):
    """mảnh vẽ ngang gốc trái: gốc (mép trái giữa) tới q0, trục chĩa tới q1."""
    m = part[:, :, 3] > 128
    h, w = m.shape
    q0, q1 = np.array(q0, float), np.array(q1, float)
    d = q1 - q0
    L = float(np.hypot(*d))
    r = math.degrees(math.atan2(-d[1], d[0]))          # góc như mắt nhìn
    ys, xs = np.nonzero(m)
    s_truc = L / max(1.0, float(xs.max() - xs.min()))
    s_ngang = day / max(1.0, float(ys.max() - ys.min())) if day else s_truc
    # tâm ảnh: gốc ở (x_min, giữa hàng của cột gốc) → đặt ở q0
    col = ys[xs < xs.min() + 0.06 * w]
    g = np.array([float(xs.min()), float(col.mean()) if len(col) else h / 2])
    v = (g - np.array([w / 2, h / 2])) * [s_truc, s_ngang]
    c, s = math.cos(math.radians(r)), math.sin(math.radians(r))
    v = np.array([c * v[0] + s * v[1], -s * v[0] + c * v[1]])
    ctr = q0 - v
    return {"sx": round(s_truc, 4), "sy": round(s_ngang, 4), "r": round(r, 2), "cx": round(float(ctr[0]), 1),
            "cy": round(float(ctr[1]), 1), "lat": False, "two": True, "q0": q0.tolist(), "q1": q1.tolist()}


def ghep(ref_shape, parts, out, order):
    H, W = ref_shape[:2]
    comp = np.zeros((H, W, 4), np.uint8)
    for n in order:
        if n not in out or n not in parts:
            continue
        t = out[n]
        wp = bien_doi(parts[n], t["sx"], t["sy"], t["r"], t["lat"])
        x0, y0 = int(round(t["cx"] - wp.shape[1] / 2)), int(round(t["cy"] - wp.shape[0] / 2))
        ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + wp.shape[1]), min(H, y0 + wp.shape[0])
        if ax1 <= ax0 or ay1 <= ay0:
            continue
        src = wp[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0].astype(np.float32)
        a = src[:, :, 3:4] / 255.0
        dst = comp[ay0:ay1, ax0:ax1].astype(np.float32)
        dst[:, :, :3] = src[:, :, :3] * a + dst[:, :, :3] * (1 - a)
        dst[:, :, 3] = np.maximum(dst[:, :, 3], src[:, :, 3])
        comp[ay0:ay1, ax0:ax1] = dst.astype(np.uint8)
    return comp


def place(k, chi=None):
    base = inbox(k)
    ref = np.array(Image.open(inbox(k, "tai_ve", "L1_duyet.png")).convert("RGB"))
    H, W = ref.shape[:2]
    rfg = fg_mask(ref)
    ref_lab = lab_f(ref)
    pj = inbox(k, "place.json")
    old = json.load(open(pj, encoding="utf-8"))["parts"] if os.path.exists(pj) else {}
    out = dict(old)
    parts = {}
    for n, hn in HINT[k].items():
        img = hn.get("img", n)
        if os.path.exists(inbox(k, "manh", img + ".png")):
            parts[n] = nap(k, img)
    for n, v in TWO[k].items():
        if os.path.exists(inbox(k, "manh", v[0] + ".png")):
            parts[n] = nap(k, v[0])
    for n, hn in HINT[k].items():
        if n not in parts or (chi and n not in chi):
            continue
        part = parts[n]
        ph, pw = part.shape[:2]
        bb = hn["bb"]
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        r0 = hn.get("r", 0)
        lat = hn.get("lat", False)
        deu = hn.get("deu", True)
        # tỉ lệ ước theo khung bao sau khi xoay (xoay nhỏ: bỏ qua)
        sx0, sy0 = (bb[2] - bb[0]) / pw, (bb[3] - bb[1]) / ph
        if deu:
            sx0 = sy0 = math.sqrt(sx0 * sy0)
        if hn.get("s"):
            sx0, sy0 = hn["s"] if not np.isscalar(hn["s"]) else (hn["s"], hn["s"])
        gm = hn.get("gamma", 1.1)
        ds, dr, win = hn.get("ds", 0.12), hn.get("dr", 10), hn.get("win", 40)
        sxs = np.linspace(sx0 * (1 - ds), sx0 * (1 + ds), 7)
        sys2 = [None] if deu else np.linspace(sy0 * (1 - ds), sy0 * (1 + ds), 5)
        c = do(ref_lab, part, lat, sxs, sys2, np.arange(r0 - dr, r0 + dr + 0.1, max(1.0, dr / 4)), 0.5, (cx, cy), win, gm)
        if c is None:
            print(f"  {n}: KHÔNG dò được")
            continue
        _, sx, sy, r, px, py = c
        sxs = np.linspace(sx * 0.97, sx * 1.03, 5)
        sys2 = [None] if deu else np.linspace(sy * 0.97, sy * 1.03, 5)
        err, sx, sy, r, px, py = do(ref_lab, part, lat, sxs, sys2, np.arange(r - 2, r + 2.1, 1.0), 1.0, (px, py), 10, gm)
        if deu:
            sy = sx
        out[n] = {"sx": round(float(sx), 4), "sy": round(float(sy), 4), "r": round(float(r), 2), "cx": round(float(px), 1),
                  "cy": round(float(py), 1), "lat": lat, "err": round(float(err), 1)}
        print(f"  {n:8s} sx={sx:.3f} sy={sy:.3f} r={r:+.1f} tâm=({px:.0f},{py:.0f}) sai={err:.0f} (ước sx {sx0:.3f})", flush=True)
    for n, v in TWO[k].items():
        img, q0, q1, day = v[:4]
        tinh = v[4] if len(v) > 4 else True
        if n not in parts or (chi and n not in chi):
            continue
        t0 = dat_hai_dau(parts[n], q0, q1, day)
        sx, sy, r = t0["sx"], t0["sy"], t0["r"]
        c = None if not tinh else do(ref_lab, parts[n], False, np.linspace(sx * 0.88, sx * 1.12, 5), np.linspace(sy * 0.85, sy * 1.15, 4),
               np.arange(r - 10, r + 10.1, 2.5), 0.5, (t0["cx"], t0["cy"]), 24)
        if c is not None:
            _, sx, sy, r, px, py = c
            err, sx, sy, r, px, py = do(ref_lab, parts[n], False, np.linspace(sx * 0.97, sx * 1.03, 3),
                                        np.linspace(sy * 0.96, sy * 1.04, 3), np.arange(r - 2, r + 2.1, 1.0), 1.0, (px, py), 8)
            t0.update(sx=round(float(sx), 4), sy=round(float(sy), 4), r=round(float(r), 2), cx=round(float(px), 1),
                      cy=round(float(py), 1), err=round(float(err), 1))
        out[n] = dict(t0, img=img)
        print(f"  {n:8s} hai đầu {q0}→{q1} rồi dò: sx={out[n]['sx']:.3f} sy={out[n]['sy']:.3f} r={out[n]['r']:+.0f} "
              f"tâm=({out[n]['cx']:.0f},{out[n]['cy']:.0f})")
    for n, hn in HINT[k].items():
        if n in out:
            out[n]["img"] = hn.get("img", n)
    for a, ma, b, mb, nn in NOI.get(k, []):
        if a not in out or b not in out:
            continue
        ta, tb = out[a], out[b]
        wa = parts[a].shape[1] * ta["sx"]
        wb = parts[b].shape[1] * tb["sx"]
        if ma == "phai" and mb == "trai":
            ra_, lb = ta["cx"] + wa / 2, tb["cx"] - wb / 2
            need = lb + nn - ra_
            if need > 0:
                la = ta["cx"] - wa / 2
                k2 = (wa + need) / wa
                ta["sx"] = round(ta["sx"] * k2, 4)
                ta["cx"] = round(la + (wa + need) / 2, 1)
                print(f"  nối {a} -> {b}: kéo {a} thêm {need:.0f} px (sx x{k2:.3f})")
    comp = ghep(ref.shape, parts, out, DRAW[k])
    cfg = (comp[:, :, 3] > 128).astype(np.uint8)
    iou = float((cfg & rfg).sum() / max(1, (cfg | rfg).sum()))
    comp_rgb = np.where(comp[:, :, 3:4] > 128, comp[:, :, :3], 255).astype(np.uint8)
    diff = np.full_like(ref, 255)
    diff[(rfg > 0) & (cfg == 0)] = (230, 60, 60)
    diff[(rfg == 0) & (cfg > 0)] = (60, 110, 230)
    diff[(rfg > 0) & (cfg > 0)] = (205, 205, 205)
    os.makedirs(inbox(k, "rig"), exist_ok=True)
    Image.fromarray(np.concatenate([ref, comp_rgb, diff], 1)).save(inbox(k, "rig", "so_ghep.png"))
    ys, xs = np.nonzero(rfg)
    yg = int(ys.max())
    xg = float(xs[ys > yg - 0.04 * H].mean())
    json.dump({"ref_size": [W, H], "iou": round(iou, 4), "ground": [xg, yg], "parts": out}, open(pj, "w", encoding="utf-8"), indent=1)
    print(f"  IoU ghép mảnh / concept = {iou:.3f} (đỏ: concept có mà ghép thiếu; xanh: ghép thừa); đất y={yg}, x giữa={xg:.0f}")


if __name__ == "__main__":
    a = sys.argv[1:]
    place(int(a[0]) if a else 1, a[1:] or None)
