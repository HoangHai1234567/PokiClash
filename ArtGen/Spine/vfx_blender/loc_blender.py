# -*- coding: utf-8 -*-
"""Lốc xoáy lửa (một lượt 48 khung = 2 s) theo mẫu "Updated and Simplified Tornado" của CodyWinch (skill mục 10):
- lớp vỏ riêng: tối (đỏ sẫm, trong cùng), thân cam (thủng → lộ dải tối), sáng kem (dồn về đỉnh); tia lửa đỏ; vệt sáng mảnh;
- dáng: eo hẹp, đỉnh loe, chân xoè; texture Voronoi F1 trôi LÊN + Simple Deform Twist 4π → dải xoắn chạy lên; thân lắc;
- mọc lên từ đất (0–0,3 s), cuối đòn ép về trục thành đường mảnh rồi tắt (như Warp "Thin" của mẫu).
    blender.exe -b --factory-startup --python loc_blender.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
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
N = 48
T = (N - 1) / F.FPS
F.reset(N)
H = 3.9


def prof_main(s):
    return 0.27 + 0.2 * math.exp(-(s / 0.12) ** 2) + 1.05 * max(0.0, (s - 0.32) / 0.68) ** 1.7


def funnel(name, prof, k=1.0, extra=0.0):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=5, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co
        s = (z + 1) / 2
        r = prof(s) * k + extra
        c = max(math.sqrt(max(1 - z * z, 0.0)), 0.18)
        v.co = Vector((x / c * r, y / c * r, s * H))
    bm.to_mesh(me)
    bm.free()
    return me


goc = F.empty("Goc")
for i in (0, 1):   # mọc ra rồi ép về trục khi tắt
    F.keys(goc, "scale", [(0, 0.5), (0.3, 1.0), (1.5, 1.05), (1.78, 0.32), (1.94, 0.02)], i)
F.keys(goc, "scale", [(0, 0.06), (0.3, 1.0), (T, 1.06)], 2)   # mọc lên từ đất

van = F.empty("Van", loc=(0, 0, -2.4), scale=(0.5, 0.5, 0.5))          # vân thân trôi lên
vmin = F.empty("VanMin", loc=(0, 0, 0), scale=(0.25, 0.25, 0.25))
vtia = F.empty("VanTia", loc=(0, 0, 0), scale=(0.5, 0.5, 0.4))         # tia lửa trôi lên nhanh hơn
vvet = F.empty("VanVet", loc=(0, 0, 0), scale=(1.0, 1.0, 0.5))         # vệt sáng mảnh
doc = F.empty("Doc", loc=(0, 0, H / 2), scale=(H / 2, 1, 1), rot=(0, math.radians(-90), 0))   # 0 ở chân → 1 ở đỉnh
F.keys(van, "location", [(0, -2.4), (T, 2.8)], 2)
F.keys(vmin, "location", [(0, 0.0), (T, 4.0)], 2)
F.keys(vtia, "location", [(0, 0.0), (T, 6.5)], 2)
F.keys(vvet, "location", [(0, 0.0), (T, 4.5)], 2)

t_main = F.clouds("Van", 2.0, "VORONOI_F1")
t_min = F.clouds("VanMin", 0.1, "VORONOI_F1", contrast=3)
t_vet = F.clouds("VanVet", 1.0, "VORONOI_F2_F1", contrast=3)
t_tia = bpy.data.textures.new("VanTia", "VORONOI")
t_tia.distance_metric, t_tia.contrast = "DISTANCE", 3.0
tg = F.blend_tex()
LAC = [(0, 0.0), (0.45, 0.12), (0.9, -0.1), (1.35, 0.09), (1.8, -0.05), (T, 0.0)]


def lac(ob):
    bd = ob.modifiers.new("Lac", "SIMPLE_DEFORM")
    bd.deform_method, bd.deform_axis = "BEND", "Y"
    F.keys(bd, "angle", LAC)


def twist(ob, ang):
    tw = ob.modifiers.new("Xoan", "SIMPLE_DEFORM")
    tw.deform_method, tw.deform_axis, tw.angle = "TWIST", "Z", ang


# ---------------------------------------------------------------- 3 lớp thân: tối, cam, sáng
BODY = [  # (tên, màu, khoá ngưỡng, đẩy ra, cộng sáng ở đỉnh)
    ("toi", F.PAL["than"], [(0, 0.05), (1.62, 0.05), (1.9, 1.05)], 0.0, None),
    ("cam", F.PAL["cam"], [(0, 0.5), (1.55, 0.5), (1.85, 1.05)], 0.06, None),
    ("sang", F.PAL["kem"], [(0, 0.80), (1.45, 0.80), (1.75, 1.05)], 0.12, 0.1),
]
for name, col, thk, push, top in BODY:
    ob = F.shell(name, funnel(name, prof_main), col, goc, ("W", "D", "F", "G"))
    grads = [dict(group="G", tex=tg, empty=doc, w=top, mode="ADD")] if top else []
    F.vwe(ob, "Van", "W", t_main, van)
    F.vwe(ob, "VanMin", "F", t_min, vmin)
    F.mix(ob, "ChepD", "D", "W", "SET")
    F.mix(ob, "CongMin", "W", "F", "ADD", 0.15)
    for g in grads:
        F.vwe(ob, "GDoc", "G", tg, doc)
        F.mix(ob, "WDoc", "W", "G", "ADD", g["w"])
    F.displace(ob, "Phong", "D", 0.16)
    ob.modifiers.new("Min", "SUBSURF").levels = 1
    F.displace(ob, "Phong2", "D", 0.08)
    mk = F.mask(ob, "AnMon", "W", thk[0][1])
    F.keys(mk, "threshold", thk)
    F.smooth(ob, 40)
    twist(ob, 4 * math.pi)
    lac(ob)
    F.displace(ob, "DayRa", None, push)

# ---------------------------------------------------------------- tia lửa đỏ (đốm nhỏ bay quanh)
ob = F.shell("tia", funnel("tia", prof_main, 1.25, 0.25), F.PAL["do"], goc, ("W",))
F.vwe(ob, "Van", "W", t_tia, vtia)
mk = F.mask(ob, "Dom", "W", 0.62)
F.keys(mk, "threshold", [(0, 0.62), (1.6, 0.62), (1.9, 1.05)])
F.smooth(ob, 6)
twist(ob, math.pi)
lac(ob)

# ---------------------------------------------------------------- vệt sáng mảnh theo viền ô (W = 1 − giá trị F2−F1)
ob = F.shell("vet", funnel("vet", prof_main, 1.04, 0.05), F.PAL["vang"], goc, ())
vg = ob.vertex_groups.new(name="W")
vg.add(list(range(len(ob.data.vertices))), 1.0, "REPLACE")
m = ob.modifiers.new("Van", "VERTEX_WEIGHT_EDIT")
m.vertex_group, m.falloff_type, m.invert_falloff = "W", "LINEAR", True
m.mask_texture, m.mask_tex_use_channel, m.mask_tex_mapping, m.mask_tex_map_object = t_vet, "INT", "OBJECT", vvet
mk = F.mask(ob, "Net", "W", 0.86)
F.keys(mk, "threshold", [(0, 0.86), (1.5, 0.86), (1.75, 1.05)])
F.smooth(ob, 4)
twist(ob, math.pi * 1.2)
lac(ob)

F.setup_render((0, -30, 2.2), 4.9, 320, 448)
F.run(OUT, "loc_bl", (0, -30, 2.2), 4.9, 320, 448, frames=FRAMES, save=SAVE, save_frame=24)
