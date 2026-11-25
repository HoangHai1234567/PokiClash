# -*- coding: utf-8 -*-
"""Mũi kim lửa kiểu "Twisting Effect" (mẫu CodyWinch): mũi khoan xoắn, dải xoắn ốc hai màu (vàng / đỏ cam) xen kẽ, mũi kem,
mặt gãy cạnh (Decimate), đuôi xé ngọn; xoay quanh trục bay một vòng mỗi chu kỳ (lặp 12 khung) như mũi khoan đang khoan.
Dải màu gán theo từng mặt lưới (pha xoắn ốc = góc quanh trục + k·x), vân ăn mòn gắn vào chính mũi kim nên xoay theo.
    blender.exe -b --factory-startup --python kim_blender.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
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
N = 12
P = N / F.FPS
F.reset(N)
TIP, TAIL = 1.0, -2.8          # mũi ở +X, đuôi ở −X
STRIPES, TURNS = 2, 0.75       # số cặp dải; số vòng xoắn trên một đơn vị dài

me = bpy.data.meshes.new("kim")
bm = bmesh.new()
bmesh.ops.create_icosphere(bm, subdivisions=5, radius=1.0)
for v in bm.verts:
    x, y, z = v.co
    s = (x + 1) / 2                                    # 0 ở đuôi → 1 ở mũi
    if s < 0.25:                                       # chân gai (đuôi) bo tròn rồi xé ngọn
        r = 0.24 * (s / 0.25) ** 0.6
    else:                                              # thân nón thẳng nhọn về mũi
        r = 0.24 * ((1 - s) / 0.75) ** 1.05 + 0.003
    c = max(math.sqrt(max(1 - x * x, 0.0)), 1e-3)
    v.co = Vector((TAIL + s * (TIP - TAIL), y / c * r, z / c * r * 0.62))   # mặt cắt dẹt → xoắn thấy viền uốn
bm.to_mesh(me)
bm.free()
ob = bpy.data.objects.new("kim", me)
bpy.context.scene.collection.objects.link(ob)
for nm in ("vang", "camdo", "kem"):
    mat = bpy.data.materials.new(nm)
    mat.diffuse_color = F.lin({"vang": "#FFD94A", "camdo": "#F0602A", "kem": "#FFF6D6"}[nm])
    me.materials.append(mat)
for p in me.polygons:
    cx, cy, cz = p.center
    if cx > TIP - 0.32:
        p.material_index = 2                            # mũi nóng màu kem
    else:
        ph = math.atan2(cz, cy) / (2 * math.pi) * STRIPES + cx * TURNS
        p.material_index = int(math.floor(ph * 2)) % 2  # dải xoắn ốc vàng / đỏ cam xen kẽ

# vân ăn mòn + gradient đuôi, gắn làm con của mũi kim (xoay theo → lặp khớp)
van = F.empty("Van", scale=(1.4, 0.5, 0.5))
van.parent = ob
duoi = F.empty("Duoi", loc=(TAIL + 0.9, 0, 0), scale=(0.9, 1, 1))     # 0 ở chót đuôi → 1 cách đuôi 1,8
duoi.parent = ob
tv = F.clouds("Van", 0.25)
tg = F.blend_tex()
allv = list(range(len(me.vertices)))
for g in ("W", "G"):
    ob.vertex_groups.new(name=g).add(allv, 0.0, "REPLACE")
F.vwe(ob, "Van", "W", tv, van)
F.vwe(ob, "GDuoi", "G", tg, duoi)
F.mix(ob, "WDuoi", "W", "G", "MUL", 0.92)
F.mask(ob, "Duoi", "W", 0.2)
F.smooth(ob, 3)
F.angular(ob, 0.45)
tw = ob.modifiers.new("Xoan", "SIMPLE_DEFORM"); tw.deform_method, tw.deform_axis, tw.angle = "TWIST", "X", 5.0
F.keys(ob, "rotation_euler", [(0, 0.0), (P, 2 * math.pi)], 0)   # xoay một vòng mỗi chu kỳ
F.setup_render((-0.8, -30, 0.0), 4.6, 400, 128)
F.run(OUT, "kim_bl", (-0.8, -30, 0.0), 4.6, 400, 128, frames=FRAMES, save=SAVE, loop=True, anchor_xz=(0, 0))
