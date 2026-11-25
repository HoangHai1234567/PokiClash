# -*- coding: utf-8 -*-
"""Thương nước (lặp 12 khung = 0,5 s), bộ nước Blender (nuocbl.py): mũi khoan nước thuôn dài mũi về +x — thân nước chảy với vệt lam
xoắn quanh trục (toạ độ xoay quanh x một vòng mỗi chu kỳ), dải nước trắng quấn xoắn ốc, đuôi tia nước toé lại phía sau. Như kim lửa
xoắn (kim_blender.py) nhưng là nước. Dùng cho n_thuong (kim / thương nước của pháp sư nước). Neo ở gốc đầu mũi (x = 0).
    blender.exe -b --factory-startup --python thuong_nuoc_bl.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import math
import os
import sys

import bmesh
import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402
import nuocbl as W  # noqa: E402

OUT, FRAMES, SAVE = F.args()
N = 12
P = N / F.FPS
sc = F.reset(N)
TAU = W.TAU
rnd = W.rnd

# thân: tiện tròn quanh trục x theo mặt cắt (x, bán kính): đuôi mảnh → phình ở 75 % → mũi nhọn
PROF = [(-2.6, 0.015), (-2.0, 0.05), (-1.2, 0.1), (-0.4, 0.15), (0.2, 0.185), (0.6, 0.16), (1.0, 0.085), (1.45, 0.0)]   # thuôn, mũi dài nhọn


def lathe(name, prof, seg=36):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    for x, r in prof:
        rings.append([bm.verts.new((x, r * math.cos(TAU * j / seg), r * math.sin(TAU * j / seg))) for j in range(seg)])
    for i in range(len(rings) - 1):
        for j in range(seg):
            bm.faces.new((rings[i][j], rings[i][(j + 1) % seg], rings[i + 1][(j + 1) % seg], rings[i + 1][j]))
    bm.to_mesh(me)
    bm.free()
    return W.smooth(me)


truc = F.empty("Truc")
MAT = W.flow_mat("Thuong", truc, scale=(0.35, 2.2, 2.2), spin=(P, 0, 1), hi_axis="Z", hi_th=0.8, rim_th=0.8, noise_scale=1.3)
body = W.link(bpy.data.objects.new("Than", lathe("Than", PROF)))
body.data.materials.append(MAT)


def helix(name, x0, x1, R0, R1, pitch, width, n=140):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    a_, b_ = [], []
    for i in range(n + 1):
        u = i / n
        x = x0 + (x1 - x0) * u
        R = R0 + (R1 - R0) * u
        th = TAU * (x - x0) / pitch
        w = width * math.sin(math.pi * u) ** 0.6
        for lst, dv in ((a_, 0.5), (b_, -0.5)):
            lst.append(bm.verts.new((x + dv * w, R * math.cos(th), R * math.sin(th))))
    for i in range(n):
        bm.faces.new((b_[i], b_[i + 1], a_[i + 1], a_[i]))
    bm.to_mesh(me)
    bm.free()
    return me


SANG_M = W.flat("DaiSang", "bot", 0.85)
for k, (ph, w) in enumerate(((0.0, 0.22), (math.pi, 0.14))):
    ob = W.link(bpy.data.objects.new(f"Dai{k}", helix(f"Dai{k}", -2.2, 0.7, 0.07, 0.24, 0.8, w * 0.75)))
    ob.data.materials.append(SANG_M)
    ob.rotation_euler[0] = ph
    for t, a in ((0, ph), (P, ph - TAU)):
        ob.rotation_euler[0] = a
        ob.keyframe_insert("rotation_euler", index=0, frame=F.fr(t))

# đuôi: lá nước nhọn toé lại phía sau quanh thân, đổi dáng mỗi 2 khung (3 bộ)
SANG, CHINH, BOT = W.flat("Sang", "sang"), W.flat("Chinh", "chinh"), W.flat("Bot", "bot")
sets = []
for v in range(3):
    par = F.empty(f"Duoi{v}")
    kids = []
    for k in range(5):
        side = 1 if k % 2 else -1
        x = rnd.uniform(-2.0, -0.2)
        ang = 180 + side * rnd.uniform(8, 26)
        ln = rnd.uniform(0.5, 1.1) * (1 - (x + 2.0) / 3.0 * 0.4)
        b = W.obj(f"La{v}_{k}", W.blade_mesh(f"La{v}_{k}", ln, rnd.uniform(0.1, 0.18), side * 0.1, 0.2), (SANG, CHINH, BOT)[k % 3],
                  (x, -0.4, side * rnd.uniform(0.08, 0.2)), ang)
        b.parent = par
        kids.append(b)
    sets.append(kids)
for v, kids in enumerate(sets):          # ba bộ thay nhau mỗi 2 khung, vòng 12 khung lặp liền
    for f in range(1, N + 1):
        show = ((f - 1) // 2) % 3 == v
        for ob in kids:
            ob.hide_render = not show
            ob.keyframe_insert("hide_render", frame=f)

# giọt bắn lại phía sau theo vòng lặp (mỗi giọt đúng một chu kỳ)
DR = (BOT, SANG, CHINH)
for k in range(10):
    ob = W.drop(f"Giot{k}", DR[k % 3], 1)
    ph = k / 10
    x0 = rnd.uniform(-1.6, 0.2)
    z0 = rnd.choice((-1, 1)) * rnd.uniform(0.1, 0.25)
    sp = rnd.uniform(2.0, 3.2)
    sz = rnd.uniform(0.04, 0.07)
    for i in range(13):
        q = (i / 12 + ph) % 1.0
        ob.location = (x0 - sp * q, -0.3, z0 * (1 + 2.2 * q))
        s = sz * (1 - q) ** 0.6
        ob.scale = (s * 1.6, s, s)
        ob.keyframe_insert("location", frame=F.fr(P * i / 12))
        ob.keyframe_insert("scale", frame=F.fr(P * i / 12))

CAM = (-0.75, -30, 0.0)
W.eevee(CAM, 220, 104, W.UPP)
F.run(OUT, "thuong_nuoc", CAM, W.UPP * 220, 220, 104, frames=FRAMES, save=SAVE, save_frame=1, loop=True, anchor_xz=(0, 0))
