# -*- coding: utf-8 -*-
"""Ảnh hiệu ứng vẽ tay riêng của nhím thép (quái đảo Kim): vệt cào thép lưỡi liềm -> quai_kim/atom/images/chem_k.png.

    py -3 -I ArtGen/Spine/quai_kim_fx.py

Ảnh `slash` của vfx.art bị cắt mép (lưỡi liềm tràn khung), nên tự vẽ: ba vệt cào song song (ba vuốt), mỗi vệt một lưỡi liềm thon
hai đầu, lõi trắng bạc + viền thép nhạt + nét mực nâu sẫm, tô phẳng (không quầng, không chuyển màu). Chĩa theo trục +x của xương.
"""
import math
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "quai_kim", "atom", "images", "chem_k.png")
INK = (24, 33, 43)          # BGR của #2B2118
CORE = (251, 247, 244)      # trắng bạc
EDGE = (222, 210, 201)      # thép nhạt
S = 360


def crescent(img, cx, cy, r, w, a0, a1):
    """lưỡi liềm: vành cung tâm (cx, cy) bán kính r, dày w ở giữa, thon về hai đầu (góc a0 -> a1, độ)"""
    n = 60
    outer, inner = [], []
    for i in range(n + 1):
        u = i / n
        a = math.radians(a0 + (a1 - a0) * u)
        th = w * math.sin(math.pi * u) ** 0.8
        outer.append((cx + (r + th / 2) * math.cos(a), cy - (r + th / 2) * math.sin(a)))
        inner.append((cx + (r - th / 2) * math.cos(a), cy - (r - th / 2) * math.sin(a)))
    poly = np.array(outer + inner[::-1], np.float32)
    k = 4
    pts = np.round(poly * k).astype(np.int32)
    cv2.fillPoly(img, [pts], (*EDGE, 255), cv2.LINE_AA, shift=2)
    # lõi: dải mảnh hơn ở giữa vành
    outer2, inner2 = [], []
    for i in range(n + 1):
        u = i / n
        a = math.radians(a0 + (a1 - a0) * u)
        th = 0.45 * w * math.sin(math.pi * u) ** 1.2
        outer2.append((cx + (r + th / 2) * math.cos(a), cy - (r + th / 2) * math.sin(a)))
        inner2.append((cx + (r - th / 2) * math.cos(a), cy - (r - th / 2) * math.sin(a)))
    p2 = np.round(np.array(outer2 + inner2[::-1], np.float32) * k).astype(np.int32)
    cv2.fillPoly(img, [p2], (*CORE, 255), cv2.LINE_AA, shift=2)
    cv2.polylines(img, [pts], True, (*INK, 255), 3, cv2.LINE_AA, shift=2)


def main():
    img = np.zeros((S, S, 4), np.uint8)
    # ba vệt cào (ba vuốt) xếp so le, cung cong ra trước (+x), đầu dưới trái -> đầu trên phải
    r = 150
    for dx, w in ((-52, 26), (0, 34), (52, 26)):          # ba vệt song song, lệch ngang (vuông góc nét cào)
        crescent(img, S * 0.56 - r + dx, S * 0.5, r, w, -42, 42)
    cv2.imwrite(OUT, img)
    a = img[..., 3] > 0
    ys, xs = np.nonzero(a)
    print(f"{OUT}: {S}x{S}, nét {xs.min()}..{xs.max()} x {ys.min()}..{ys.max()}")


if __name__ == "__main__":
    main()
