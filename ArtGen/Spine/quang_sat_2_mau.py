# -*- coding: utf-8 -*-
"""Dạng 2 quặng sắt: (1) cân màu đỏ các mảnh tinh thể tờ M2 về đúng concept (Codex tô sáng hơn ~30 kênh đỏ); (2) cắt hai gai trong
(longdan_3, longdan_2) THẲNG từ concept khi Codex hết hạn mức: gai vẽ đè lên vòm, viền mực kín nên tách được bằng màu.

    quang_sat_2_mau.py can      cân màu longdan_4, gai_t, gai_p, longdan_1, longdan_0 (giữ bản gốc ở manh/_goc_<tên>.png)
    quang_sat_2_mau.py gai      cắt longdan_3, longdan_2 từ concept → manh/ + dat.json
"""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quang_sat_2_manh as Q  # noqa: E402

M = Q.M
CON = np.asarray(Image.open(M.CONCEPT).convert("RGB")).astype(np.int32)


def la_do(a):
    return (a[..., 0] > 100) & (a[..., 0] > a[..., 1] * 1.6) & (a[..., 0] > a[..., 2] * 1.6)


def can():
    D = M.nap_dat()
    for k in ("longdan_4", "gai_t", "gai_p", "longdan_1", "longdan_0"):
        p = os.path.join(M.MANH, k + ".png")
        g = os.path.join(M.MANH, f"_goc_{k}.png")
        if not os.path.exists(g):
            shutil.copy(p, g)
        A = np.asarray(Image.open(g).convert("RGBA")).astype(np.int32)
        x0, y0, x1, y1 = D[k]["hop"]
        m, mc = la_do(A[..., :3]) & (A[..., 3] > 128), la_do(CON[y0:y1, x0:x1])
        d = np.median(CON[y0:y1, x0:x1][mc], 0) - np.median(A[..., :3][m], 0)
        B = A.copy()
        B[..., :3][m] = np.clip(A[..., :3][m] + d, 0, 255)
        Image.fromarray(B.astype(np.uint8), "RGBA").save(p)
        print(k, "lệch", d.astype(int).tolist())


def gai():
    D = M.nap_dat()
    for k in ("longdan_3", "longdan_2"):
        x0, y0, x1, y1 = Q.HOP2[k]
        x0, y0, x1, y1 = x0 - 30, y0 - 30, x1 + 30, y1 + 30
        sub = CON[y0:y1, x0:x1].copy()
        do = (la_do(sub) & (sub[..., 1] < 90)).astype(np.uint8)                     # bỏ mạch cam của vòm bên dưới
        n, lab, st, _ = cv2.connectedComponentsWithStats(do, 8)
        gop = np.isin(lab, [i for i in range(1, n) if st[i, 4] > 200]).astype(np.uint8)     # mọi mặt đỏ (nét gờ xám chia gai thành nhiều mảng)
        gop = cv2.morphologyEx(gop, cv2.MORPH_CLOSE, M.el(7))                             # khép qua nét gờ
        n2, lab2, st2, _ = cv2.connectedComponentsWithStats(gop, 8)
        kk = 1 + int(np.argmax(st2[1:, 4]))
        cs, _ = cv2.findContours((lab2 == kk).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        fill = cv2.drawContours(np.zeros(do.shape, np.uint8), cs, -1, 1, -1)      # gồm cả nét gờ xám bên trong
        vanh = cv2.dilate(fill, M.el(6)).astype(bool) & ~fill.astype(bool)       # viền mực mới, kín quanh gai
        muc = sub.max(2) < 70
        sub[vanh & ~muc] = (43, 33, 24)                                            # chỗ mực gốc sứt / là vòm: tô mực
        m = fill.astype(bool) | vanh
        full = np.zeros(CON.shape[:2], bool)
        full[y0:y1, x0:x1] = m
        A = CON.copy()
        A[y0:y1, x0:x1] = sub
        b = M.luu_manh(A, full, k, D, "L1_duyet.png (cắt thẳng, Codex hết hạn mức)")
        print(k, "hộp", b)
    M.ghi_dat(D)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "gai":
        gai()
    else:
        print(__doc__)
