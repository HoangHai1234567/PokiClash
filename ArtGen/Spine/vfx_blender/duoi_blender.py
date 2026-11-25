# -*- coding: utf-8 -*-
"""Hạt đuôi lửa → khói (28 khung, ~1,15 s) cho vệt đuôi của cầu lửa / thiên thạch: lúc sinh ra là cụm lửa đậm (vàng, cam, đỏ)
nguội rất nhanh (~0,5 s) để lộ cụm khói nâu xám nằm sau; khói phồng, bay lên, thủng, tách cụm rồi tan. AtomSpine thả dày các hạt
này ngay sau quả cầu theo quãng đường bay → đoạn sát cầu là lửa đậm, xa dần thành khói, vệt liền và dính vào cầu.
    blender.exe -b --factory-startup --python duoi_blender.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import math
import os
import sys

import bmesh
import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402
from mathutils import Vector  # noqa: E402

OUT, FRAMES, SAVE = F.args()
N = 28
F.reset(N)
T = (N - 1) / F.FPS
LOBES = [(0.0, 0.0, 0.8), (-0.55, -0.12, 0.55), (0.5, -0.1, 0.55), (-0.1, 0.48, 0.5)]


def lobes_mesh(name):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for lx, lz, r in LOBES:
        part = bmesh.new()
        bmesh.ops.create_icosphere(part, subdivisions=4, radius=r)
        bmesh.ops.delete(part, geom=[v for v in part.verts if v.co.y > 0.04 * r], context="VERTS")
        bmesh.ops.translate(part, verts=part.verts, vec=Vector((lx, 0, lz)))
        tmp = bpy.data.meshes.new("tmp")
        part.to_mesh(tmp)
        part.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    bm.to_mesh(me)
    bm.free()
    return me


goc = F.empty("Goc")
van = F.empty("Van")
vmin = F.empty("VanMin", scale=(0.5, 0.5, 0.5))
doc = F.empty("Doc", loc=(0, 0, 0.2), scale=(1.1, 1, 1), rot=(0, math.radians(-90), 0))   # 1 ở đỉnh → 0 ở đáy
for i in range(3):
    F.keys(goc, "scale", [(0, 0.6), (0.15, 0.85), (0.6, 1.12), (T, 1.38)], i)
F.keys(goc, "location", [(0, 0.0), (0.4, 0.25), (T, 0.95)], 2)
for i in range(3):
    F.keys(van, "scale", [(0, 1.0), (T, 1.4)], i)
F.keys(van, "location", [(0, 0.0), (T, -0.7)], 2)
F.keys(vmin, "location", [(0, 0.0), (T, -0.9)], 2)
tv = F.clouds("Van", 0.42)
tm = F.clouds("VanMin", 0.11, "VORONOI_F1", contrast=3)
tg = F.blend_tex()
NG = F.shatter_group("TachCum", 0.62, speed=0.5, gravity=-1.0, radial=0.8, jitter=(0.5, 0.2, 0.4), bias=(0, 0, 0.35))
DISP = [(0, 0.2), (0.3, 0.3), (T, 0.38)]
LAYERS = [  # lửa đậm phía trước (đẩy ra xa), nguội nhanh; khói nằm sau, lộ ra khi lửa tắt
    ("kem", F.PAL["kem"], [(0, 0.66), (0.06, 0.85), (0.12, 1.05)], 0.26, None),
    ("vang", F.PAL["vang"], [(0, 0.10), (0.08, 0.42), (0.18, 0.68), (0.26, 1.05)], 0.23, None),
    ("cam", F.PAL["cam"], [(0, 0.12), (0.15, 0.45), (0.26, 0.70), (0.34, 1.05)], 0.20, None),
    ("do", F.PAL["do"], [(0, 0.14), (0.22, 0.48), (0.33, 0.72), (0.42, 1.05)], 0.17, None),
    ("than", F.PAL["than"], [(0, 0.16), (0.3, 0.52), (0.4, 0.75), (0.5, 1.05)], 0.14, None),
    ("khoi_nhat", "#B9AAA0", [(0, 0.10), (0.45, 0.30), (0.7, 0.58), (0.92, 0.80), (1.05, 1.05)], 0.06, 0.55),
    ("khoi_vua", "#8C7C74", [(0, 0.12), (0.55, 0.32), (0.8, 0.62), (0.98, 0.82), (1.08, 1.05)], 0.03, 0.3),
    ("khoi_dam", "#5F534D", [(0, 0.14), (0.62, 0.36), (0.88, 0.66), (1.04, 0.86), (1.12, 1.05)], 0.0, None),
]
for name, col, thk, push, gk in LAYERS:
    ob = F.shell(name, lobes_mesh(name), col, goc, ("W", "D", "F", "G"))
    grads = [dict(group="G", tex=tg, empty=doc, w=gk)] if gk else []
    F.standard_stack(ob, van, tv, vmin, tm, grads=grads, disp_keys=DISP, th_keys=thk, push=push, smooth_it=22,
                     shatter=NG if name.startswith("khoi") else None)
F.setup_render((0, -30, 0.75), 4.4, 288, 320)
F.run(OUT, "duoi_bl", (0, -30, 0.75), 4.4, 288, 320, frames=FRAMES, save=SAVE, save_frame=4, anchor_xz=(0, 0))
