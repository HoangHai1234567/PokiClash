# -*- coding: utf-8 -*-
"""Cầu lửa (lặp 16 khung) theo "Procedural Cartoon Flames in Blender" (Blender Box, youtube RDrswNZYiCo), đổi cho cầu tròn:
- 4 cầu lồng nhau (đỏ ngoài cùng thủng nhiều → còn đốm / vệt đỏ ở mép; cam; vàng; lõi kem), Subsurf + Displace Voronoi gắn Empty
  xoay (mép phập phồng);
- vật liệu Emission trộn Transparent: Voronoi 3 cỡ (4 / 8 / 16) → ColorRamp tuyến tính → trộn Soft Light → nhân Gradient (phía
  sau thủng nhiều hơn) → ColorRamp CONSTANT (ngưỡng từng lớp) → Invert → hệ số Mix Shader → lỗ tròn sắc mép;
- lặp liền: mỗi Mapping và Empty xoay số vòng nguyên trong một chu kỳ (thay driver trôi của bài, vốn không lặp được);
- Eevee, Emission cường độ 1, View Standard, nền trong, không bloom (luật dự án: không quầng sáng).
    blender.exe -b --factory-startup --python cau_eevee.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402

OUT, FRAMES, SAVE = F.args()
N = 24   # vòng lặp 1 s (game: 24 khung, trùng tên ảnh cũ)
P = N / F.FPS
sc = F.reset(N)
TAU = 2 * math.pi

ripple = F.empty("Ripple", scale=(1.0, 1.0, 1.0))
F.keys(ripple, "rotation_euler", [(0, 0.0), (P, TAU)], 2)
F.keys(ripple, "rotation_euler", [(0, 0.0), (P, -TAU)], 0)
t_disp = bpy.data.textures.new("FlameRipple", "VORONOI")
t_disp.noise_scale, t_disp.contrast = 1.3, 0.3

SHELLS = [  # (tên, màu, cỡ, ngưỡng ramp constant, độ phồng, góc xoay riêng)
    ("do", F.PAL["do"], 1.06, 0.97, 0.5, 0.4),
    ("cam", "#FF9A26", 0.96, 0.82, 0.45, 1.3),
    ("vang", "#FFD94A", 0.8, 0.64, 0.38, 2.1),
    ("kem", F.PAL["kem"], 0.6, 0.30, 0.3, 3.0),
]


def node(nt, kind, loc, **props):
    n = nt.nodes.new(kind)
    n.location = loc
    for k, v in props.items():
        setattr(n, k, v)
    return n


def flame_material(name, color, th, rot0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    L = nt.links
    out = node(nt, "ShaderNodeOutputMaterial", (1400, 0))
    mix = node(nt, "ShaderNodeMixShader", (1200, 0))
    emi = node(nt, "ShaderNodeEmission", (1000, 100))
    emi.inputs["Color"].default_value = F.lin(color)
    emi.inputs["Strength"].default_value = 1.0
    tra = node(nt, "ShaderNodeBsdfTransparent", (1000, -100))
    inv = node(nt, "ShaderNodeInvert", (850, 0))
    cr2 = node(nt, "ShaderNodeValToRGB", (600, 0))
    cr2.color_ramp.interpolation = "CONSTANT"
    cr2.color_ramp.elements[0].color = (0, 0, 0, 1)
    cr2.color_ramp.elements[1].position = th
    cr2.color_ramp.elements[1].color = (1, 1, 1, 1)
    tc = node(nt, "ShaderNodeTexCoord", (-900, 0))
    layers = []
    for i, (scale, turns) in enumerate([(3.0, 2), (6.0, 3), (1.6, -1)]):   # 24 khung (1 s) cho game
        mp = node(nt, "ShaderNodeMapping", (-700, 300 - 300 * i))
        mp.inputs["Rotation"].default_value = (rot0, rot0 * 0.7, 0)
        for t, ang in ((0, rot0), (P, rot0 + turns * TAU)):
            mp.inputs["Rotation"].default_value[0] = ang
            mp.inputs["Rotation"].keyframe_insert("default_value", index=0, frame=F.fr(t))
        vo = node(nt, "ShaderNodeTexVoronoi", (-500, 300 - 300 * i))
        vo.inputs["Scale"].default_value = scale
        vo.inputs["Randomness"].default_value = 1.0
        cr = node(nt, "ShaderNodeValToRGB", (-300, 300 - 300 * i))
        cr.color_ramp.elements[0].position, cr.color_ramp.elements[1].position = 0.0, 0.76
        L.new(tc.outputs["Object"], mp.inputs["Vector"])
        L.new(mp.outputs["Vector"], vo.inputs["Vector"])
        L.new(vo.outputs["Distance"], cr.inputs["Fac"])
        layers.append(cr.outputs["Color"])
    m1 = node(nt, "ShaderNodeMixRGB", (-50, 200), blend_type="SOFT_LIGHT")
    m1.inputs["Fac"].default_value = 1.0
    L.new(layers[0], m1.inputs["Color1"])
    L.new(layers[1], m1.inputs["Color2"])
    m2 = node(nt, "ShaderNodeMixRGB", (150, 100), blend_type="SOFT_LIGHT")
    m2.inputs["Fac"].default_value = 1.0
    L.new(m1.outputs["Color"], m2.inputs["Color1"])
    L.new(layers[2], m2.inputs["Color2"])
    # gradient: phía trước (+X) giữ đặc, phía sau (−X) mỏng dần (lửa bị gió thổi về sau)
    gm = node(nt, "ShaderNodeMapping", (-300, -600))
    gm.inputs["Location"].default_value = (1.4, 0, 0)
    gm.inputs["Scale"].default_value = (0.36, 1, 1)
    gr = node(nt, "ShaderNodeTexGradient", (-100, -600))
    L.new(tc.outputs["Object"], gm.inputs["Vector"])
    L.new(gm.outputs["Vector"], gr.inputs["Vector"])
    m3 = node(nt, "ShaderNodeMixRGB", (380, 0), blend_type="MULTIPLY")
    m3.inputs["Fac"].default_value = 0.55
    L.new(m2.outputs["Color"], m3.inputs["Color1"])
    L.new(gr.outputs["Color"], m3.inputs["Color2"])
    L.new(m3.outputs["Color"], cr2.inputs["Fac"])
    L.new(cr2.outputs["Color"], inv.inputs["Color"])
    L.new(inv.outputs["Color"], mix.inputs["Fac"])
    L.new(emi.outputs["Emission"], mix.inputs[1])
    L.new(tra.outputs["BSDF"], mix.inputs[2])
    L.new(mix.outputs["Shader"], out.inputs["Surface"])
    return mat


for name, col, scl, th, disp, rot0 in SHELLS:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=1.0)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (scl, scl, scl)
    ob.rotation_euler = (rot0, rot0 * 0.5, rot0 * 0.3)
    bpy.ops.object.shade_smooth()
    ob.modifiers.new("Min", "SUBSURF").levels = 2
    d = ob.modifiers.new("Phong", "DISPLACE")
    d.texture, d.texture_coords, d.texture_coords_object = t_disp, "OBJECT", ripple
    d.strength, d.mid_level = disp, 0.5
    ob.data.materials.append(flame_material(name, col, th, rot0))

F.setup_render((0, -30, 0), 3.4, 256, 256)
r = sc.render
r.engine = "BLENDER_EEVEE"
try:
    sc.eevee.taa_render_samples = 16
except Exception:
    pass
sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"
F.run(OUT, "cau_bl", (0, -30, 0), 3.4, 256, 256, frames=FRAMES, save=SAVE, save_frame=1, loop=True)
