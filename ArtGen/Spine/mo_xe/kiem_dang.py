# -*- coding: utf-8 -*-
"""Kiểm một .atomik dạng dựng bằng atomik_dang: (1) khung cuối evolve (phần n_) trùng khung 0 idle của rig dạng sau (đơn vị rig dạng
sau); (2) clip không lặp: khung cuối lệch khung 0 idle; clip lặp: khép vòng; (3) bước dời lớn nhất giữa hai khung 30 fps.
    kiem_dang.py <atomik dạng này> [<atomik dạng sau>]"""
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atomik_dang as A  # noqa: E402

J, img, _ = A.load(sys.argv[1])
S = J["slots"]
own = [i for i, s in enumerate(S) if not s["name"].startswith("n_")]
P, Q = A.Pose(J), A.Pose(J)


def pts(P, slots):
    out = {}
    for s, a, V, al in P.items():
        if s in slots and al > 0.5:
            out[s] = V
    return out


def lech(a, b):
    ks = set(a) & set(b)
    return max((float(np.hypot(*(a[k] - b[k]).T).max()) for k in ks), default=0.0), len(set(a) ^ set(b))


ii = A.clip(J, "idle")
P.at(ii, 0)
I0 = pts(P, own)
for an in J["anims"]:
    if an["name"] == "evolve":
        continue
    ci = A.clip(J, an["name"])
    P.at(ci, an["dur"])
    end = pts(P, own)
    d, nd = lech(end, I0)
    step = 0.0
    prev = None
    for t in np.arange(0, an["dur"] + 1e-6, 1 / 30):
        P.at(ci, t)
        cur = pts(P, own)
        if prev is not None:
            step = max(step, lech(cur, prev)[0])
        prev = cur
    print(f"  {an['name']:7s} cuối↔idle0 {d:7.2f} (slot khác {nd:3d})  bước 30fps lớn nhất {step:6.1f}")
if len(sys.argv) > 2 and any(a["name"] == "evolve" for a in J["anims"]):
    JB, _, _ = A.load(sys.argv[2])
    PB = A.Pose(JB).at(A.clip(JB, "idle"), 0)
    ref = {s: V for s, a, V, al in PB.items()}
    nb = [i for i, s in enumerate(S) if s["name"].startswith("n_")]
    off = len(S) - len(JB["slots"])
    P.at(A.clip(J, "evolve"), J["anims"][A.clip(J, "evolve")]["dur"])
    nroot = A.bi(J)["n_" + next(b["name"] for b in JB["bones"] if b["parent"] < 0)]
    a_, b_, c_, d_, x_, y_ = P.w[nroot]
    M = np.linalg.inv(np.array([[a_, b_], [c_, d_]]))
    got = {}
    for s, a, V, al in P.items():
        if s in nb:
            got[s - off] = (M @ (V - [x_, y_]).T).T
    d, nd = lech(got, ref)
    print(f"  evolve: khung cuối dạng sau ↔ idle0 của rig dạng sau {d:.3f} đơn vị (slot khác {nd}); dạng này còn hiện: "
          f"{sum(1 for s, a, V, al in P.items() if s in own and al > 0.01)}")
