# -*- coding: utf-8 -*-
"""tm06 dạng 2: khớp hàm dưới GPT vào vùng hàm cắt từ concept bằng IoU mặt nạ (dò tỉ lệ ngang, dọc, góc, vị trí), ghi lại
place.json["parts"]["ham"]. Cần cv2:

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm06_khop_ham.py
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tm06_lai as A  # noqa: E402
import tm06_place as PL  # noqa: E402


def main():
    rgb = np.array(Image.open(A.inbox("tai_ve", "L1_duyet.png")).convert("RGB"))
    fg = PL.fg_mask(rgb) > 0
    lab = A.labels(rgb, fg)
    tgt = lab == A.NAMES.index("ham")
    ys, xs = np.nonzero(tgt)
    cx0, cy0 = xs.mean(), ys.mean()
    pj = json.load(open(A.inbox("place.json"), encoding="utf-8"))
    p0 = pj["parts"]["ham"]
    part = PL.nap(2, "ham")
    best = None
    for sx in np.linspace(p0["sx"] * 0.9, p0["sx"] * 1.25, 8):
        for sy in np.linspace(p0["sy"] * 0.9, p0["sy"] * 1.45, 9):
            for r in np.arange(p0["r"] - 8, p0["r"] + 8.1, 2):
                wp = PL.bien_doi(part, sx, sy, r, False)
                m = wp[:, :, 3] > 128
                my, mx = np.nonzero(m)
                for dx in range(-16, 17, 4):
                    for dy in range(-16, 17, 4):
                        ox = int(round(cx0 + dx - mx.mean()))
                        oy = int(round(cy0 + dy - my.mean()))
                        M = np.zeros(fg.shape, bool)
                        y1, x1 = min(fg.shape[0], oy + m.shape[0]), min(fg.shape[1], ox + m.shape[1])
                        M[max(0, oy):y1, max(0, ox):x1] = m[max(0, -oy):y1 - oy, max(0, -ox):x1 - ox]
                        iou = (M & tgt).sum() / max(1, (M | tgt).sum())
                        if best is None or iou > best[0]:
                            best = (iou, sx, sy, r, ox + m.shape[1] / 2, oy + m.shape[0] / 2)
    iou, sx, sy, r, cx, cy = best
    pj["parts"]["ham"].update(sx=round(float(sx), 4), sy=round(float(sy), 4), r=round(float(r), 2), cx=round(float(cx), 1),
                              cy=round(float(cy), 1), khop="IoU mặt nạ hàm concept %.3f" % iou)
    json.dump(pj, open(A.inbox("place.json"), "w", encoding="utf-8"), indent=1)
    print(f"  ham: IoU với vùng hàm concept {iou:.3f}; sx={sx:.3f} sy={sy:.3f} r={r:+.1f} tâm=({cx:.0f},{cy:.0f})")


if __name__ == "__main__":
    main()
