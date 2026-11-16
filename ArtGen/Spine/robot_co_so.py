# -*- coding: utf-8 -*-
"""Robot cổ (robot_co): so hình bóng concept với con gốc SAU KHI co / dời concept cho khớp nhất (GPT hay vẽ to hơn ảnh mẫu ~10–20 %).

    robot_co_so.py [ABC]   → in tỉ lệ, độ dời, IoU từng hướng; tờ inbox/robot_co_1/mau/_so_goc_co.png (viền đỏ = con gốc trên concept đã co)
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import robot_co as G  # noqa: E402
import robot_co_da as D  # noqa: E402

W, H = 1536, 1024


def khop(m, g):
    """tìm tỉ lệ a và dời (dx, dy) để a·concept + d phủ con gốc khít nhất (IoU). Tâm co = trọng tâm concept."""
    ys, xs = np.nonzero(m)
    cx, cy = xs.mean(), ys.mean()
    gy, gx = np.nonzero(g)
    best = (0, 1.0, 0, 0)
    for a in np.arange(0.80, 1.06, 0.01):
        M = np.array([[a, 0, (1 - a) * cx], [0, a, (1 - a) * cy]], np.float32)
        mm = cv2.warpAffine(m.astype(np.uint8), M, (W, H), flags=cv2.INTER_NEAREST).astype(bool)
        yy, xx = np.nonzero(mm)
        dx0, dy0 = gx.mean() - xx.mean(), gy.mean() - yy.mean()
        for dx in np.arange(dx0 - 12, dx0 + 13, 4):
            for dy in np.arange(dy0 - 12, dy0 + 13, 4):
                T = np.float32([[1, 0, dx], [0, 1, dy]])
                m2 = cv2.warpAffine(mm.astype(np.uint8), T, (W, H), flags=cv2.INTER_NEAREST).astype(bool)
                iou = (m2 & g).sum() / max(1, (m2 | g).sum())
                if iou > best[0]:
                    best = (iou, a, dx + (1 - a) * cx, dy + (1 - a) * cy)
    return best


def main(ks="ABC"):
    g = D._mat_na(os.path.join(G.MAU, "goc_ca_con.png"))
    cs, _ = cv2.findContours(g.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    o = []
    for k in ks:
        p = os.path.join(G.TAI, f"L1_{k}.png")
        if not os.path.exists(p):
            continue
        m = D._mat_na(p)
        iou, a, tx, ty = khop(m, g)
        im = np.asarray(Image.open(p).convert("RGB").resize((W, H)))
        M = np.float32([[a, 0, tx], [0, a, ty]])
        im2 = cv2.warpAffine(im, M, (W, H), borderValue=(255, 255, 255))
        cv2.drawContours(im2, cs, -1, (230, 30, 30), 3)
        cv2.putText(im2, f"{k}  x{a:.2f}  IoU {iou:.3f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (230, 30, 30), 4)
        o.append(Image.fromarray(im2).resize((W // 2, H // 2), Image.LANCZOS))
        print(f"{k}: co ×{a:.2f}, dời ({tx:.0f}, {ty:.0f}) px → IoU {iou:.3f}")
    if o:
        c = Image.new("RGB", (W // 2 * len(o), H // 2), "white")
        for i, im in enumerate(o):
            c.paste(im, (i * W // 2, 0))
        c.save(os.path.join(G.MAU, "_so_goc_co.png"))


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["ABC"]))
