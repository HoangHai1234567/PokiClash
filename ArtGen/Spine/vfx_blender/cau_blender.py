# -*- coding: utf-8 -*-
"""Cầu lửa (lặp 16 khung): một quả cầu lửa tròn đang cháy, KHÔNG đuôi (đuôi lửa + khói là vệt riêng trong AtomSpine, xem
duoi_blender.py). Lõi kem sáng → vàng → cam ở viền, quanh viền 9 lưỡi lửa ngắn liếm ra (hơi ngả lên); vân sôi xoay một vòng
mỗi chu kỳ (lặp liền). Gradient tròn (Blend SPHERICAL) làm lõi nóng, viền nguội.
    blender.exe -b --factory-startup --python cau_blender.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
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
RC = 1.0
LICKS = 7


def part(fn, subdiv=4):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.06], context="VERTS")
    for v in bm.verts:
        v.co = fn(*v.co)
    tmp = bpy.data.meshes.new("tmp")
    bm.to_mesh(tmp)
    bm.free()
    return tmp


def lick_fn(theta, L, w):
    th = math.radians(theta)
    dx, dz = math.cos(th), math.sin(th)
    dz += 0.35                                            # ngả lên (lửa bốc)
    n = math.hypot(dx, dz)
    dx, dz = dx / n, dz / n
    nx, nz = -dz, dx
    bx, bz = 0.7 * math.cos(th), 0.7 * math.sin(th)

    def fn(x, y, z):
        s = (x + 1) / 2
        r = w * (1 - s) ** 0.75 * (1 + 0.5 * s)
        c = max(math.sqrt(max(1 - x * x, 0.0)), 1e-3)
        yl, zl = y / c * r, z / c * r
        return Vector((bx + dx * s * L + nx * zl, yl, bz + dz * s * L + nz * zl))
    return fn


def ball_mesh(name):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    parts = [part(lambda x, y, z: Vector((x * RC, y * RC, z * RC)), 5)]
    for i in range(LICKS):
        th = i * 360 / LICKS + 12 * math.sin(i * 2.3)
        parts.append(part(lick_fn(th, 0.42 + 0.3 * math.sin(i * 1.7) ** 2, 0.44)))
    for tmp in parts:
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    bm.to_mesh(me)
    bm.free()
    return me


goc = F.empty("Goc")
van = F.empty("Van")
vmin = F.empty("VanMin", scale=(0.5, 0.5, 0.5))
tron = F.empty("Tron", scale=(1.9, 1.9, 1.9))          # gradient tròn: 1 ở tâm → 0 ở bán kính 1,9
loi = F.empty("Loi", scale=(1.15, 1.15, 1.15))         # lõi nóng
F.keys(van, "rotation_euler", [(0, 0.0), (P, 2 * math.pi)], 2)
F.keys(vmin, "rotation_euler", [(0, 0.0), (P, -2 * math.pi)], 0)
for i in range(3):
    F.keys(goc, "scale", [(0, 1.0), (P / 2, 1.04), (P, 1.0)], i)
tv = F.clouds("Van", 0.4)
tm = F.clouds("VanMin", 0.1, "VORONOI_F1", contrast=3)
tg = bpy.data.textures.new("Tron", "BLEND")
tg.progression = "SPHERICAL"
LAYERS = [("kem", 0.60, 0.07), ("vang", 0.40, 0.05), ("cam", 0.30, 0.035), ("do", 0.22, 0.02), ("than", 0.15, 0.0)]
for name, th, push in LAYERS:
    ob = F.shell(name, ball_mesh(name), F.PAL[name], goc, ("W", "D", "F", "G", "J"))
    F.standard_stack(ob, van, tv, vmin, tm, fine_k=0.24,
                     grads=[dict(group="J", tex=tg, empty=loi, w=0.5, mode="ADD"),
                            dict(group="G", tex=tg, empty=tron, w=0.6, d=0.4)],
                     disp=0.24, th=th, push=push, smooth_it=20)
F.setup_render((0, -30, 0.15), 4.2, 288, 288)
F.run(OUT, "cau_bl", (0, -30, 0.15), 4.2, 288, 288, frames=FRAMES, save=SAVE, save_frame=1, loop=True)
