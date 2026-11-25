# -*- coding: utf-8 -*-
"""Lửa cháy tại chỗ (lặp 16 khung) kiểu ngọn lửa toon LỒNG NHAU: lớp đỏ cam ngoài cùng là cả cụm lưỡi lửa; lớp cam, vàng, kem
bên trong là chính cụm đó thu nhỏ dần từ gốc (lõi kem nhỏ nhất ở chân) → hình ngọn lửa nhiều tầng rõ. Vân kéo dọc (vệt bốc lên),
đỉnh lưỡi xé ngọn (gradient đứng), cả cụm lắc lư (Simple Deform Bend). Lặp: vân xoay một vòng quanh trục ngang X, góc lắc về 0.
    blender.exe -b --factory-startup --python lua_blender.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
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
N = 16
P = N / F.FPS
F.reset(N)
H = 3.0
TONGUES = [  # (lệch x, cao, rộng, nghiêng, uốn S)
    (0.0, H, 0.55, 0.10, 0.30),
    (-0.42, 0.72 * H, 0.42, -0.38, -0.22),
    (0.44, 0.8 * H, 0.42, 0.34, 0.24),
    (-0.78, 0.42 * H, 0.3, -0.5, -0.1),
    (0.8, 0.48 * H, 0.3, 0.5, 0.12),
]


def tongue(ox, h, w, lean, sk, k):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.06], context="VERTS")
    for v in bm.verts:
        x, y, z = v.co
        s = (z + 1) / 2                                  # 0 ở chân → 1 ở đỉnh
        f = (s / 0.28) ** 0.55 if s < 0.28 else ((1 - s) / 0.72) ** 0.9
        c = max(math.sqrt(max(1 - z * z, 0.0)), 1e-3)
        cx = ox + lean * s * s + sk * math.sin(2 * math.pi * 0.8 * s) * s * 0.6
        v.co = Vector((cx * k + x / c * w * f * k, y / c * w * f * k, s * h * k))   # thu nhỏ từ gốc (0,0,0)
    tmp = bpy.data.meshes.new("tmp")
    bm.to_mesh(tmp)
    bm.free()
    return tmp


def flames_mesh(name, k):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for t in TONGUES:
        tmp = tongue(*t, k)
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    bm.to_mesh(me)
    bm.free()
    return me


goc = F.empty("Goc")
van = F.empty("Van", loc=(0, 0, 1.0), scale=(0.45, 1, 1.7))        # vân kéo dọc → vệt lửa bốc lên
vmin = F.empty("VanMin", loc=(0, 0, 1.0), scale=(0.25, 0.4, 0.55))
doc = F.empty("Doc", loc=(0, 0, H / 2), scale=(H / 2, 1, 1), rot=(0, math.radians(90), 0))  # 1 ở chân → 0 ở đỉnh
F.keys(van, "rotation_euler", [(0, 0.0), (P, -2 * math.pi)], 0)
F.keys(vmin, "rotation_euler", [(0, 0.0), (P, -2 * math.pi)], 0)
F.keys(goc, "scale", [(0, 1.0), (P / 2, 0.97), (P, 1.0)], 0)
F.keys(goc, "scale", [(0, 1.0), (P / 2, 1.04), (P, 1.0)], 2)
tv = F.clouds("Van", 0.3)
tm = F.clouds("VanMin", 0.09, "VORONOI_F1", contrast=3)
tg = F.blend_tex()
LAYERS = [  # (tên, cỡ lồng, ngưỡng, đẩy ra): ngoài → trong
    ("do", 1.0, 0.30, 0.0), ("cam", 0.82, 0.30, 0.08), ("vang", 0.62, 0.30, 0.16), ("kem", 0.4, 0.32, 0.24),
]
for name, k, th, push in LAYERS:
    ob = F.shell(name, flames_mesh(name, k), F.PAL[name], goc, ("W", "D", "F", "G"))
    F.standard_stack(ob, van, tv, vmin, tm, fine_k=0.24, grads=[dict(group="G", tex=tg, empty=doc, w=0.8, d=0.5)],
                     disp=0.1, th=th, push=push, smooth_it=16)
    bd = ob.modifiers.new("Lac", "SIMPLE_DEFORM")
    bd.deform_method, bd.deform_axis = "BEND", "Y"
    F.keys(bd, "angle", [(0, 0.0), (P / 4, 0.18), (3 * P / 4, -0.18), (P, 0.0)])
F.setup_render((0, -30, 1.5), 3.9, 320, 352)
F.run(OUT, "lua_bl", (0, -30, 1.5), 3.9, 320, 352, frames=FRAMES, save=SAVE, loop=True)
