# -*- coding: utf-8 -*-
"""Cắt từng cụm mây khỏi concept cũ của Thanh Long thành ảnh hiệu ứng riêng (inbox/fx/thanh_long_may<k>_<i>.png) để game cho
mây bay vòng quanh rồng (beasts_cfg "orbit"), không còn dính vào lưới thân (người dùng dặn 2026-11-09: mây có animation bay
xung quanh). Mỗi cụm là một mảng liền trên nền trắng: lấy mảng chứa điểm hạt giống, lấp lòng, mép mượt.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/cat_may.py
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, "inbox")
FXD = os.path.join(IN, "fx")

# dạng -> (ảnh nguồn, [điểm trong lòng từng cụm mây])
SRC = {
    1: ("thanh_long_1/L1_duyet.png", [(530, 380), (1010, 745)]),
    2: ("thanh_long_2/tai_ve/L1_lien.png", [(390, 290), (1310, 700), (690, 840)]),
    3: ("thanh_long_3/L1_duyet.png", [(310, 270), (690, 840), (1290, 740)]),
}


def cut(path, seeds, prefix):
    rgb = np.array(Image.open(os.path.join(IN, path)).convert("RGB"))
    ink = (rgb.min(2) < 236).astype(np.uint8)  # nét mực, màu sáp (mây xanh xám nhạt vẫn dưới 236)
    ink = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, cl, st, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    out = []
    for i, (x, y) in enumerate(seeds):
        c = cl[y, x]
        if c == 0:  # hạt rơi vào khe giấy trong lòng mây: lấy mảng gần nhất
            ys, xs = np.nonzero(cl > 0)
            j = int(np.argmin((xs - x) ** 2 + (ys - y) ** 2))
            c = cl[ys[j], xs[j]]
        m = (cl == c).astype(np.uint8)
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        full = np.zeros_like(m)
        cv2.drawContours(full, cs, -1, 1, -1)
        a = cv2.GaussianBlur(full.astype(np.float32), (0, 0), 0.8)
        x0, y0, w, h = cv2.boundingRect(full)
        x0, y0 = max(0, x0 - 3), max(0, y0 - 3)
        x1, y1 = min(rgb.shape[1], x0 + w + 6), min(rgb.shape[0], y0 + h + 6)
        rgba = np.dstack([rgb, np.clip(a * 255, 0, 255).astype(np.uint8)])[y0:y1, x0:x1]
        name = f"{prefix}_{i}"
        Image.fromarray(rgba).save(os.path.join(FXD, name + ".png"))
        out.append((name, x1 - x0, y1 - y0, int(full.sum())))
    return out


def main():
    os.makedirs(FXD, exist_ok=True)
    for k, (p, seeds) in SRC.items():
        for name, w, h, area in cut(p, seeds, f"thanh_long_may{k}"):
            print(f"{name}: {w}x{h}, {area} px")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
