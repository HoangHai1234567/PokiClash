# -*- coding: utf-8 -*-
"""Cắt cầu NĂNG LƯỢNG kiểu Energy Ball (vfx_blender/cau_nl_bl.py, 2026-11-24) từ vfx_blender/render/g_cau_nl_<bộ> thành frames/cau_nl_<bộ>
(cat_gen.save: hộp gộp mọi khung, neo tâm cầu, ghi manifest.json). Bộ: moc (lục ngọc + gân chanh), vang (cam vàng + gân kem), troi (Mặt Trời).
    py -3 -I cat_nl.py [moc vang troi]
"""
import glob
import json
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cat_gen  # noqa: E402

R = os.path.normpath(os.path.join(HERE, "..", "vfx_blender", "render"))
for bo in sys.argv[1:] or ["moc", "vang", "troi"]:
    src = os.path.join(R, "g_cau_nl_" + bo)
    info = json.load(open(os.path.join(src, "info.json"), encoding="utf-8"))
    fr = [cv2.imread(f, cv2.IMREAD_UNCHANGED) for f in sorted(glob.glob(os.path.join(src, "cau_nl_*.png")))]
    al = np.max(np.stack([f[..., 3] for f in fr]), 0)
    edge = [(al[:, 0] > 8).any(), (al[:, -1] > 8).any(), (al[0] > 8).any(), (al[-1] > 8).any()]
    if any(edge):
        print(bo, "CHAM MEP trai/phai/tren/duoi:", edge)
    cat_gen.save("cau_nl_" + bo, fr, info["anchor"], loop=True)
