# -*- coding: utf-8 -*-
"""Nổ trúng (30 khung, 1,25 s) theo mẫu Cloudy Explosion: sao chớp kem 3 khung → khối cầu phồng nhanh rồi chậm, kem vàng →
lột lớp cam → đỏ → đỏ sẫm, thủng lỗ → vỡ mảnh toả tròn từ tâm, rơi, cháy hết.
    blender.exe -b --factory-startup --python no_blender.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402
from mathutils import Vector  # noqa: E402

OUT, FRAMES, SAVE = F.args()
N = 30
F.reset(N)
T_VO = 0.55
goc = F.empty("Goc")
van = F.empty("Van")
vmin = F.empty("VanMin", scale=(0.5, 0.5, 0.5))
F.keys(goc, "scale", [(0, 0.18), (0.05, 0.55), (0.12, 0.82), (0.25, 1.0), (0.7, 1.14), (1.2, 1.2)], 0)
F.keys(goc, "scale", [(0, 0.18), (0.05, 0.55), (0.12, 0.82), (0.25, 1.0), (0.7, 1.14), (1.2, 1.2)], 1)
F.keys(goc, "scale", [(0, 0.18), (0.05, 0.55), (0.12, 0.82), (0.25, 1.0), (0.7, 1.14), (1.2, 1.2)], 2)
F.keys(goc, "location", [(0, 0.0), (1.2, 0.35)], 2)
for i in range(3):
    F.keys(van, "scale", [(0, 1.0), (1.2, 1.5)], i)
F.keys(van, "location", [(0, 0.0), (1.2, -0.6)], 2)
F.keys(vmin, "location", [(0, 0.0), (1.2, -1.2)], 0)
tv = F.clouds("Van", 0.5)
tm = F.clouds("VanMin", 0.12, "VORONOI_F1", contrast=3)
NG = F.shatter_group("VoManh", T_VO, speed=1.6, gravity=4.0, radial=1.0, jitter=(0.8, 0.3, 0.8), bias=(0, 0, 0.25))
DISP = [(0, 0.25), (0.15, 0.55), (0.6, 0.72), (1.2, 0.85)]
LAYERS = [
    ("kem", [(0, 0.55), (0.1, 0.66), (0.22, 0.82), (0.32, 1.05)], 0.10),
    ("vang", [(0, 0.30), (0.2, 0.45), (0.35, 0.60), (0.5, 0.74), (0.6, 1.05)], 0.075),
    ("cam", [(0, 0.34), (0.3, 0.46), (0.45, 0.62), (0.6, 0.76), (0.72, 1.05)], 0.05),
    ("do", [(0, 0.38), (0.4, 0.48), (0.55, 0.64), (0.7, 0.77), (0.85, 1.05)], 0.025),
    ("than", [(0, 0.42), (0.5, 0.50), (0.65, 0.66), (0.8, 0.79), (0.95, 0.90), (1.05, 1.05)], 0.0),
]
for name, thk, push in LAYERS:
    ob = F.shell(name, F.half_sphere(name, lambda x, y, z: Vector((x, y, z))), F.PAL[name], goc, ("W", "D", "F"))
    ang = name in ("do", "than")
    F.standard_stack(ob, van, tv, vmin, tm, disp_keys=DISP, th_keys=thk, push=push, smooth_it=8 if ang else 25,
                     angular_ratio=0.3 if ang else None, shatter=NG)
# sao chớp 3 khung (vàng ngoài, kem trong)
for nm, col, ro, ri, y in (("SaoVang", F.PAL["vang"], 2.3, 0.6, -3.1), ("SaoKem", F.PAL["kem"], 1.7, 0.42, -3.2)):
    st = F.flat_star(nm, 8, ro, ri, col, y=y, rot=0.2)
    for i in range(3):
        F.keys(st, "scale", [(0, 0.35), (0.04, 1.0), (0.085, 0.75), (0.125, 0.0)], i)
    F.keys(st, "rotation_euler", [(0, 0.0), (0.125, 0.35)], 1)
F.setup_render((0, -30, 0.35), 6.6, 448, 448)
F.run(OUT, "no_bl", (0, -30, 0.35), 6.6, 448, 448, frames=FRAMES, save=SAVE, save_frame=8)
