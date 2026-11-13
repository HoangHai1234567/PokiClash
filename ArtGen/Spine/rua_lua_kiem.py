# -*- coding: utf-8 -*-
"""kiểm góc nhảy giữa hai khung liền nhau của mọi xương, mọi clip (góc nhảy lớn = runtime quay ngược một vòng trong một khung)."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
import rua_lua_rig as R
from quai import hoat
with contextlib.redirect_stdout(io.StringIO()):
    sk, info = R.dung()
    clips = R.lam_clip(sk, info)
for c in clips:
    fr = hoat.nuong(sk, c)
    xau, luc = {}, {}
    for i, (a, b) in enumerate(zip(fr, fr[1:])):
        for bn in set(a.t) | set(b.t):
            d = abs(b.t.get(bn, [0, 0, 0, 1, 1])[2] - a.t.get(bn, [0, 0, 0, 1, 1])[2])
            if d > xau.get(bn, 0):
                xau[bn] = d
                luc[bn] = i / 30.0
    lon = sorted(((v, f"{k}@{luc[k]:.2f}") for k, v in xau.items() if v > 40), reverse=True)[:6]
    cuoi = {k: round(v[2]) for k, v in fr[-1].t.items() if abs(v[2]) > 170}
    print(f"{c.ten:7s} bước xoay lớn nhất mỗi khung: " + (", ".join(f"{k} {v:.0f}°" for v, k in lon) or "không xương nào quá 40°") +
          (f" | khung cuối lệch vòng: {cuoi}" if cuoi and c.ten != "die" else ""))
    # bước dời lớn nhất mỗi khung của gốc từng xương (đơn vị rig / khung ở 30 khung/giây), trừ phần cả con dời (move)
    import numpy as np
    buoc = {}
    Ws = [sk.the_gioi(P) for P in fr]
    luc2 = {}
    for i, (Wa, Wb) in enumerate(zip(Ws, Ws[1:])):
        dm = Wb["move"][:2, 2] - Wa["move"][:2, 2]
        for bn in Wa:
            d = float(np.hypot(*(Wb[bn][:2, 2] - Wa[bn][:2, 2] - dm)))
            if d > buoc.get(bn, 0):
                buoc[bn] = d
                luc2[bn] = i / 30.0
    lon = sorted(((v, f"{k}@{luc2[k]:.2f}") for k, v in buoc.items()), reverse=True)[:5]
    print("          bước dời lớn nhất mỗi khung: " + ", ".join(f"{k} {v:.0f}" for v, k in lon))
