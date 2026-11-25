# -*- coding: utf-8 -*-
"""Cụm khói (26 khung, ~1,1 s) theo kỹ thuật Cloudy Explosion, đúng luật khói của dự án (skill vfx-petclash mục 1b):
cụm nhiều múi chồng nhau (to, vừa, nhỏ), 3 lớp nâu xám phẳng, đỉnh nhạt đáy đậm (gradient đứng nhân vào trọng số lớp ngoài),
phồng ra + bay lên, rồi thủng lỗ, tách thành mảnh nhỏ (đảo lưới) bay lên, co lại và tan. AtomSpine rải nhiều cụm này quanh lửa.
    blender.exe -b --factory-startup --python khoi_blender.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
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
N = 26
F.reset(N)
goc = F.empty("Goc")
van = F.empty("Van")
vmin = F.empty("VanMin", scale=(0.5, 0.5, 0.5))
doc = F.empty("Doc", loc=(0, 0, 0.3), scale=(1.3, 1, 1), rot=(0, math.radians(-90), 0))  # 1 ở đỉnh → 0 ở đáy
T = (N - 1) / F.FPS
for i in range(3):
    F.keys(goc, "scale", [(0, 0.3), (0.12, 0.7), (0.35, 0.95), (T, 1.25)], i)
F.keys(goc, "location", [(0, 0.0), (0.35, 0.35), (T, 1.25)], 2)
for i in range(3):
    F.keys(van, "scale", [(0, 1.0), (T, 1.4)], i)
F.keys(van, "location", [(0, 0.0), (T, -0.8)], 2)
F.keys(vmin, "location", [(0, 0.0), (T, -1.0)], 2)
tv = F.clouds("Van", 0.45)
tm = F.clouds("VanMin", 0.12, "VORONOI_F1", contrast=3)
tg = F.blend_tex()
NG = F.shatter_group("TachCum", 0.55, speed=0.55, gravity=-1.2, radial=0.8, jitter=(0.6, 0.2, 0.5), bias=(0, 0, 0.4))

LOBES = [(0.0, 0.0, 1.0), (-0.78, -0.22, 0.68), (0.8, -0.18, 0.72), (-0.35, 0.62, 0.62), (0.42, 0.66, 0.55),
         (0.05, -0.55, 0.6)]   # (x, z, bán kính): múi to, vừa, nhỏ chồng nhau


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


DISP = [(0, 0.15), (0.3, 0.32), (T, 0.4)]
LAYERS = [  # (tên, màu, khoá ngưỡng, đẩy ra)
    ("khoi_nhat", "#B9AAA0", [(0, 0.10), (0.3, 0.28), (0.55, 0.55), (0.8, 0.78), (0.95, 1.05)], 0.06),
    ("khoi_vua", "#8C7C74", [(0, 0.12), (0.4, 0.30), (0.65, 0.60), (0.88, 0.80), (1.0, 1.05)], 0.03),
    ("khoi_dam", "#5F534D", [(0, 0.14), (0.5, 0.34), (0.75, 0.64), (0.95, 0.84), (1.06, 1.05)], 0.0),
]
for name, col, thk, push in LAYERS:
    ob = F.shell(name, lobes_mesh(name), col, goc, ("W", "D", "F", "G"))
    # đỉnh nhạt đáy đậm: lớp ngoài (nhạt) bị khoét ở đáy trước → lộ lớp đậm bên dưới
    gk = 0.55 if name == "khoi_nhat" else (0.3 if name == "khoi_vua" else None)
    grads = [dict(group="G", tex=tg, empty=doc, w=gk)] if gk else []
    F.standard_stack(ob, van, tv, vmin, tm, grads=grads, disp_keys=DISP, th_keys=thk, push=push, smooth_it=22,
                     shatter=NG)
F.setup_render((0, -30, 1.35), 5.8, 352, 416)
F.run(OUT, "khoi_bl", (0, -30, 1.35), 5.8, 352, 416, frames=FRAMES, save=SAVE, save_frame=8, anchor_xz=(0, 0))
