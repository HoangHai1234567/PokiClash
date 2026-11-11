# -*- coding: utf-8 -*-
"""tm09: dò vị trí, tỉ lệ (ngang, dọc riêng), góc của từng mảnh GPT trên concept đã duyệt (SQDIFF có mặt nạ trên Lab, dò thô
rồi tinh quanh gợi ý đọc trên concept kẻ lưới; mảnh dài trơn như chân, đuôi đặt theo hai đầu khớp). Ra inbox/tm09_<k>/place.json
(toạ độ concept px, s theo tờ GPT gốc) và so_ghep.png (ghép mảnh lên concept, in IoU mặt nạ). Cần cv2:

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm09_place.py 2
    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm09_place.py 1
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import rig as riglib  # noqa: E402  (lab_f, fg_mask)

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm09"

from tm09_cfg_place import DRAW, HINT, TWO  # noqa: E402,F401



def warp2(rgba, sx, sy, r, lat=False):
    im = rgba[:, ::-1] if lat else rgba
    h, w = im.shape[:2]
    nw, nh = max(2, int(round(w * sx))), max(2, int(round(h * sy)))
    im = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA if sx < 1 else cv2.INTER_LINEAR)
    return riglib.warp(im, 1.0, r)


def match(ref_lab, part, lat, sxs, sys_, rots, f, around, win):
    best = None
    R = cv2.resize(ref_lab, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    for sx in sxs:
        for sy0 in sys_:
            sy = sx if sy0 is None else sy0
            for r in rots:
                wp = warp2(part, sx * f, sy * f, r, lat)
                if wp.shape[0] >= R.shape[0] or wp.shape[1] >= R.shape[1] or min(wp.shape[:2]) < 6:
                    continue
                m = (wp[:, :, 3] > 200).astype(np.float32)
                area = m.sum()
                if area < 20:
                    continue
                t = riglib.lab_f(np.ascontiguousarray(wp[:, :, :3]))
                res = cv2.matchTemplate(R, t, cv2.TM_SQDIFF, mask=np.dstack([m, m, m])) / area
                th, tw = wp.shape[:2]
                ys, xs = np.mgrid[0:res.shape[0], 0:res.shape[1]]
                cx, cy = (xs + tw / 2) / f, (ys + th / 2) / f
                bad = (np.abs(cx - around[0]) > win) | (np.abs(cy - around[1]) > win)
                res = np.where(bad, np.inf, res)
                mn, _, loc, _ = cv2.minMaxLoc(res)
                if not np.isfinite(mn):
                    continue
                if best is None or mn < best[0]:
                    best = (mn, sx, sy, r, (loc[0] + tw / 2) / f, (loc[1] + th / 2) / f)
    return best


def do_two(part, lat, q0, q1, he_cung, day):
    """mảnh vẽ duỗi thẳng nằm ngang (gốc trái) hoặc đứng (gốc trên): đặt gốc tại q0, trục chĩa tới q1."""
    m = part[:, :, 3] > 128
    h, w = m.shape
    doc = h > w                       # chân vẽ đứng
    q0, q1 = np.array(q0, float), np.array(q1, float)
    d = q1 - q0
    L = float(np.hypot(*d))
    goc_dich = math.degrees(math.atan2(-d[1], d[0]))      # góc nhìn (y xuống)
    goc_anh = -90.0 if doc else 0.0                       # trục ảnh: đứng xuống hoặc ngang sang phải
    if lat:
        goc_anh = 180.0 - goc_anh
    r = (goc_dich - goc_anh + 180) % 360 - 180
    dai_anh = h if doc else w
    s_truc = he_cung * L / dai_anh
    if day:
        ys, xs = np.nonzero(m)
        if doc:
            cols = xs[ys < 0.25 * h]
            thick = float(cols.max() - cols.min())
        else:
            rows = ys[xs < 0.12 * w]
            thick = float(rows.max() - rows.min())
        s_ngang = day / max(1.0, thick)
    else:
        s_ngang = s_truc
    sx, sy = (s_ngang, s_truc) if doc else (s_truc, s_ngang)
    return {"sx": round(s_truc if not doc else s_ngang, 4), "sy": round(s_ngang if not doc else s_truc, 4), "r": round(r, 2),
            "q0": [float(q0[0]), float(q0[1])], "q1": [float(q1[0]), float(q1[1])], "lat": lat, "two": True, "doc": doc}


def place(k):
    base = os.path.join(HERE, "inbox", f"{CODE}_{k}")
    ref = np.array(Image.open(os.path.join(base, "tai_ve", "L1_duyet.png")).convert("RGB"))
    H, W = ref.shape[:2]
    rfg = riglib.fg_mask(ref)
    ref_lab = riglib.lab_f(ref)
    parts = {}
    for n in set(HINT[k]) | set(TWO[k]):
        p = os.path.join(base, "manh", (n if n != "sung_xa" else "sung") + ".png")
        parts[n] = np.array(Image.open(p).convert("RGBA"))
    out = {}
    for n, (bb, s_est, r_est, lat, cung) in HINT[k].items():
        part = parts[n]
        ph, pw = part.shape[:2]
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        if s_est is None:
            sx0, sy0 = (bb[2] - bb[0]) / pw, (bb[3] - bb[1]) / ph
            if cung:
                sx0 = sy0 = (sx0 + sy0) / 2
        else:
            sx0, sy0 = s_est

        def fine(sx, sy, r, px, py, f, dsx, dr, w, n_s=5):
            sxs = np.linspace(sx * (1 - dsx), sx * (1 + dsx), n_s)
            sys2 = [None] if cung else np.linspace(sy * (1 - dsx), sy * (1 + dsx), n_s)
            return match(ref_lab, part, lat, sxs, sys2, np.arange(r - dr, r + dr + 0.1, max(1.0, dr / 2)), f, (px, py), w)

        c = fine(sx0, sy0, r_est, cx, cy, 0.5, 0.02, 10, 25)   # tỉ lệ tin khung bao (dò rộng là co nhỏ lại), chỉ dò vị trí, góc
        if c is None:
            print(f"  {n}: KHÔNG dò được")
            continue
        _, sx, sy, r, px, py = c
        if cung:
            sy = sx
        c = fine(sx, sy, r, px, py, 1.0, 0.01, 2, 8, 3)
        err, sx, sy, r, px, py = c
        if cung:
            sy = sx
        out[n] = {"sx": round(float(sx), 4), "sy": round(float(sy), 4), "r": round(float(r), 2), "cx": round(float(px), 1),
                  "cy": round(float(py), 1), "lat": lat, "err": round(float(err), 1)}
        print(f"  {n:8s} sx={sx:.3f} sy={sy:.3f} r={r:+.0f} tâm=({px:.0f},{py:.0f}) sai={err:.0f}", flush=True)
    for n, (q0, q1, he, day) in TWO[k].items():
        out[n] = do_two(parts[n], n == "duoi", q0, q1, he, day)
        print(f"  {n:8s} hai đầu {q0}→{q1}: sx={out[n]['sx']:.3f} sy={out[n]['sy']:.3f} r={out[n]['r']:+.0f}")
    # ghép thử theo thứ tự vẽ, IoU mặt nạ với concept
    comp = np.full((H, W, 4), 0, np.uint8)
    for n in DRAW:
        if n not in out:
            continue
        t = out[n]
        part = parts[n]
        if t.get("two"):
            wp = warp2(part, t["sx"], t["sy"], t["r"], t["lat"])
            h, w = part.shape[:2]
            # điểm gốc trên ảnh (giữa mép trái / mép trên) sau biến đổi → đặt tại q0
            g = np.array([0.02 * w, h / 2]) if not t["doc"] else np.array([w / 2, 0.04 * h])
            c0 = np.array([w / 2, h / 2])
            v = (g - c0) * np.array([t["sx"], t["sy"]])
            if t["lat"]:
                v[0] = -v[0]
            th = math.radians(-t["r"])
            v = np.array([v[0] * math.cos(th) - v[1] * math.sin(th), v[0] * math.sin(th) + v[1] * math.cos(th)])
            cx, cy = np.array(t["q0"]) - v
            t["cx"], t["cy"] = round(float(cx), 1), round(float(cy), 1)
        else:
            wp = warp2(part, t["sx"], t["sy"], t["r"], t["lat"])
            cx, cy = t["cx"], t["cy"]
        x0, y0 = int(round(cx - wp.shape[1] / 2)), int(round(cy - wp.shape[0] / 2))
        ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + wp.shape[1]), min(H, y0 + wp.shape[0])
        if ax1 <= ax0 or ay1 <= ay0:
            continue
        src = wp[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0]
        a = src[:, :, 3:4] / 255.0
        dst = comp[ay0:ay1, ax0:ax1]
        dst[:, :, :3] = (src[:, :, :3] * a + dst[:, :, :3] * (1 - a)).astype(np.uint8)
        dst[:, :, 3] = np.maximum(dst[:, :, 3], src[:, :, 3])
    cfg = (comp[:, :, 3] > 128).astype(np.uint8)
    iou = float((cfg & rfg).sum() / max(1, (cfg | rfg).sum()))
    comp_rgb = np.where(comp[:, :, 3:4] > 128, comp[:, :, :3], 255).astype(np.uint8)
    diff = np.full_like(ref, 255)
    diff[(rfg > 0) & (cfg == 0)] = (230, 60, 60)
    diff[(rfg == 0) & (cfg > 0)] = (60, 110, 230)
    diff[(rfg > 0) & (cfg > 0)] = (205, 205, 205)
    Image.fromarray(np.concatenate([ref, comp_rgb, diff], 1)).save(os.path.join(base, "rig", "so_ghep.png"))
    ys, xs = np.nonzero(rfg)
    yg = int(ys.max())
    xg = float(xs[ys > yg - 0.04 * H].mean())
    json.dump({"ref_size": [W, H], "iou": round(iou, 4), "ground": [xg, yg], "parts": out},
              open(os.path.join(base, "place.json"), "w"), indent=1)
    print(f"  IoU ghép mảnh / concept = {iou:.3f}; đất y={yg}, x giữa chân={xg:.0f} → {os.path.join(base, 'rig', 'so_ghep.png')}")


if __name__ == "__main__":
    place(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
