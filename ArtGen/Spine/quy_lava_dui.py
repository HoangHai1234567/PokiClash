# -*- coding: utf-8 -*-
"""Tiểu quỷ lava: vẽ bằng mã tờ M_G (đùi chân gần) khi Codex treo: khúc chân ngắn màu da nối đáy thân với cụm đá chân gần. Vân sáp lấy
thẳng từ mảnh thân (manh/than.png, vùng da không có mực), viền mực nâu hơi rung như nét bút. Khúc này gần như luôn khuất (dưới thân, trong
cụm đá chân), chỉ lộ khi giơ găng tay lên.

    quy_lava_dui.py     → inbox/quy_lava_1/tai_ve/M_G.png (1536 × 1024, nền trắng, đúng chỗ trên concept)"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "inbox", "quy_lava_1")
P0, P1, DAY = np.array([700.0, 745.0]), np.array([622.0, 830.0]), 78.0
INK = (43, 33, 24)


def main():
    th = np.asarray(Image.open(os.path.join(B, "manh", "than.png")).convert("RGBA")).astype(np.int32)
    # ô vân sạch: vùng da đặc, cách mực, lấy ô vuông lớn nhất có thể ở giữa thân
    dac = (th[..., 3] > 250) & (th[..., :3].max(2) > 90)
    med = np.median(th[..., :3][dac], 0)                                  # màu da trung vị thật của mảnh thân
    da = dac & (np.abs(th[..., :3] - med).max(2) < 34)
    da = cv2.morphologyEx(da.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)).astype(bool)
    d = cv2.distanceTransform(da.astype(np.uint8), cv2.DIST_L2, 5)
    cy, cx = np.unravel_index(d.argmax(), d.shape)
    r = int(min(d.max() * 0.7, 90))
    o = th[cy - r:cy + r, cx - r:cx + r, :3].astype(np.uint8)
    can = np.full((1024, 1536, 3), 255, np.uint8)
    # viên nhộng (hai đầu tròn), hơi rung mép
    m = np.zeros((1024, 1536), np.uint8)
    u = (P1 - P0) / np.hypot(*(P1 - P0))
    n_ = np.array([-u[1], u[0]])
    rng = np.random.default_rng(5)
    pts = []
    L = np.hypot(*(P1 - P0))
    for k in range(72):
        a = 2 * np.pi * k / 72
        c = P1 if np.cos(a) >= 0 else P0
        rr = DAY / 2 * (1 + 0.025 * np.sin(5 * a + 1.3)) + rng.normal(0, 0.6)
        pts.append(c + u * np.cos(a) * rr + n_ * np.sin(a) * rr)
    cv2.fillPoly(m, [np.round(pts).astype(np.int32)], 1)
    ys, xs = np.nonzero(m)
    tile = np.tile(o, (int(np.ceil(1024 / o.shape[0])) + 1, int(np.ceil(1536 / o.shape[1])) + 1, 1))
    can[ys, xs] = tile[ys % (2 * r), xs % (2 * r)]
    # nét mực ~5 px quanh viền
    vien = m.astype(bool) & ~cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))).astype(bool)
    can[vien] = INK
    Image.fromarray(can).save(os.path.join(B, "tai_ve", "M_G.png"))
    print(os.path.join(B, "tai_ve", "M_G.png"), "ô vân", 2 * r, "px")


if __name__ == "__main__":
    main()
