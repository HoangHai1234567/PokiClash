# -*- coding: utf-8 -*-
"""kiểm góc nhảy giữa hai khung liền nhau của mọi xương, mọi clip (góc nhảy lớn = runtime quay ngược một vòng trong một khung)."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
import nguoi_cay_rig as R
from quai import hoat
with contextlib.redirect_stdout(io.StringIO()):
    sk, info = R.dung()
    clips = R.lam_clip(sk, info)
for c in clips:
    fr = hoat.nuong(sk, c)
    xau = {}
    for a, b in zip(fr, fr[1:]):
        for bn in set(a.t) | set(b.t):
            d = abs(b.t.get(bn, [0, 0, 0, 1, 1])[2] - a.t.get(bn, [0, 0, 0, 1, 1])[2])
            if d > xau.get(bn, 0):
                xau[bn] = d
    lon = sorted(((v, k) for k, v in xau.items() if v > 40), reverse=True)[:6]
    cuoi = {k: round(v[2]) for k, v in fr[-1].t.items() if abs(v[2]) > 170}
    print(f"{c.ten:7s} bước xoay lớn nhất mỗi khung: " + (", ".join(f"{k} {v:.0f}°" for v, k in lon) or "không xương nào quá 40°") +
          (f" | khung cuối lệch vòng: {cuoi}" if cuoi and c.ten != "die" else ""))
