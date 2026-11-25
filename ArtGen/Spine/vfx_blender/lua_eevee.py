# -*- coding: utf-8 -*-
"""Lửa cháy (lặp 16 khung) theo "Procedural Cartoon Flames in Blender" (Blender Box, youtube RDrswNZYiCo), skill mục 11:
4 giọt lửa lồng nhau, mỗi giọt xoay một góc: kem ngoài cùng (thủng gần hết → vệt ở mép trên), đỏ (đốm), cam (thân), vàng (lõi, chân).
Vật liệu: Voronoi 3 cỡ → ColorRamp tuyến tính → Soft Light → nhân gradient đứng (đặc ở chân, mỏng lên đỉnh) → ColorRamp CONSTANT →
Invert → Mix Shader Emission / Transparent. Vân trôi lên: xoay Mapping quanh trục X số vòng nguyên mỗi chu kỳ (lặp liền).
Displace Voronoi gắn Empty xoay (mép phập phồng), Simple Deform Bend lắc nhẹ. Eevee, Emission 1, View Standard, nền trong, không bloom.
    blender.exe -b --factory-startup --python lua_eevee.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import math
import os
import sys

import bmesh
import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402

OUT, FRAMES, SAVE = F.args()
N = 24   # vòng lặp 1 s (game: 24 khung, trùng tên ảnh cũ)
P = N / F.FPS
sc = F.reset(N)
TAU = 2 * math.pi

ripple = F.empty("Ripple")
F.keys(ripple, "rotation_euler", [(0, 0.0), (P, TAU)], 2)
t_disp = bpy.data.textures.new("FlameRipple", "CLOUDS")   # mềm: Voronoi của bài tạo nếp gãy → lớp ngoài chui vào trong thành đường chia thẳng
t_disp.noise_scale, t_disp.noise_depth = 0.75, 1

# (tên, màu, cỡ, ngưỡng constant, phồng, xoay riêng (độ), dải đặc theo cao (từ z, tới z, giá trị ở dưới, ở trên), hệ số nhân)
# ngoài → trong (lớp to hơn nằm trước): kem đặc ở ngọn (vệt trắng), vàng đặc ở chân, cam tới giữa, đỏ đốm sau cam, lõi vàng lấp chân
LAYERS = [   # (tên, màu, cỡ, ngưỡng, phồng, xoay riêng, dải (z0, z1, dưới, trên), hệ số dải, kéo cao)
    ("kem", F.PAL["kem"], 1.24, 0.66, 0.75, 25, (0.6, 2.1, 0.0, 1.0), 0.85, 1.18),
    ("vang", "#FFE14D", 1.10, 0.46, 0.42, -60, (0.25, 1.35, 1.0, 0.0), 0.8, 1.0),
    ("do", "#F0702A", 1.05, 0.73, 0.42, 70, (0.4, 2.2, 0.5, 1.0), 0.35, 1.03),
    ("cam", "#FFA43A", 1.0, 0.40, 0.42, -120, (0.0, 2.4, 1.0, 0.25), 0.6, 1.02),
    ("loi", "#FFE14D", 0.84, 0.30, 0.42, 160, (0.0, 1.6, 1.0, 0.0), 0.7, 0.9),
]
TONGUES = [(0.0, 0.0, 1.0)]   # một khối giọt lửa bầu như bài


def teardrop(name):
    """Mỗi lớp = 3 giọt lửa (icosphere kéo phần trên thành ngọn như bài), nhân bản, thu nhỏ, nghiêng ra hai bên; gốc ở chân."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for ox, lean, ks in TONGUES:
        part = bmesh.new()
        bmesh.ops.create_icosphere(part, subdivisions=4, radius=1.0)
        cl, sl = math.cos(lean), math.sin(lean)
        for v in part.verts:
            x, y, z = v.co
            up = max(z, 0.0)
            k = 1 - 0.42 * up ** 1.6
            x, y, z = x * k * ks, y * k * ks, (z * (1 + 0.6 * up) + 1.0) * ks
            v.co = (ox + x * cl + z * sl, y, -x * sl + z * cl)    # nghiêng quanh trục Y tại chân
        tmp = bpy.data.meshes.new("tmp")
        part.to_mesh(tmp)
        part.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    bm.to_mesh(me)
    bm.free()
    return me


def node(nt, kind, loc, **props):
    n = nt.nodes.new(kind)
    n.location = loc
    for k_, v_ in props.items():
        setattr(n, k_, v_)
    return n


def flame_material(name, color, th, rot0, band, gk):
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
    for i, (scale, turns) in enumerate([(3.0, -2), (6.0, -3), (1.6, -1)]):   # 24 khung (1 s) cho game   # quay âm quanh X → mặt trước vân chạy lên
        mp = node(nt, "ShaderNodeMapping", (-700, 300 - 300 * i))
        mp.inputs["Rotation"].default_value = (rot0, 0, rot0 * 0.6)
        mp.inputs["Scale"].default_value = (1.0, 1.0, 0.6)   # co trước khi xoay → ô Voronoi kéo dọc theo trục Z vật
        for t, ang in ((0, rot0), (P, rot0 + turns * TAU)):
            mp.inputs["Rotation"].default_value[0] = ang
            mp.inputs["Rotation"].keyframe_insert("default_value", index=0, frame=F.fr(t))
        vo = node(nt, "ShaderNodeTexVoronoi", (-500, 300 - 300 * i))
        vo.inputs["Scale"].default_value = scale
        vo.inputs["Randomness"].default_value = 1.0
        if scale < 2:                      # ô to: ranh giới mềm (F1 thường cho mặt phân giới phẳng → đường cắt thẳng)
            vo.feature = "SMOOTH_F1"
            vo.inputs["Smoothness"].default_value = 1.0
        cr = node(nt, "ShaderNodeValToRGB", (-300, 300 - 300 * i))
        cr.color_ramp.elements[0].position, cr.color_ramp.elements[1].position = 0.0, 0.76
        L.new(tc.outputs["Object"], mp.inputs["Vector"])
        L.new(mp.outputs["Vector"], vo.inputs["Vector"])
        L.new(vo.outputs["Distance"], cr.inputs["Fac"])
        layers.append(cr.outputs["Color"])
        if i == 0:
            mp_first = mp                  # nhiễu mép dải trôi theo vân (lặp liền)
    m1 = node(nt, "ShaderNodeMixRGB", (-50, 200), blend_type="MIX")
    m1.inputs["Fac"].default_value = 0.35
    L.new(layers[0], m1.inputs["Color1"])
    L.new(layers[1], m1.inputs["Color2"])
    m2 = node(nt, "ShaderNodeMixRGB", (150, 100), blend_type="MIX")
    m2.inputs["Fac"].default_value = 0.15
    L.new(m1.outputs["Color"], m2.inputs["Color1"])
    L.new(layers[2], m2.inputs["Color2"])
    st = node(nt, "ShaderNodeValToRGB", (260, 100))                      # kéo giãn tương phản: mép cắt đi theo vân
    st.color_ramp.elements[0].position, st.color_ramp.elements[1].position = 0.22, 0.9
    L.new(m2.outputs["Color"], st.inputs["Fac"])
    # gradient đứng: đặc ở chân (z −1) → mỏng ở đỉnh (z 2,5)
    sp = node(nt, "ShaderNodeSeparateXYZ", (-300, -600))
    mr = node(nt, "ShaderNodeMapRange", (-100, -600))
    mr.clamp = True
    mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = band[0], band[1]
    mr.inputs["To Min"].default_value, mr.inputs["To Max"].default_value = band[2], band[3]
    L.new(tc.outputs["Object"], sp.inputs["Vector"])
    # nhiễu vào trục cao: chỗ vân bão hoà, ranh giới chỉ còn do gradient quyết định → thành đường ngang; nhiễu làm mép rách
    nz = node(nt, "ShaderNodeTexNoise", (-500, -800))
    nz.inputs["Scale"].default_value = 2.2
    nz.inputs["Detail"].default_value = 3.0
    nz.inputs["Roughness"].default_value = 0.6
    L.new(mp_first.outputs["Vector"], nz.inputs["Vector"])
    nb = node(nt, "ShaderNodeMath", (-300, -800), operation="MULTIPLY_ADD")
    nb.inputs[1].default_value = 1.1
    nb.inputs[2].default_value = -0.55
    L.new(nz.outputs["Fac"], nb.inputs[0])
    za = node(nt, "ShaderNodeMath", (-200, -650), operation="ADD")
    L.new(sp.outputs["Z"], za.inputs[0])
    L.new(nb.outputs["Value"], za.inputs[1])
    L.new(za.outputs["Value"], mr.inputs["Value"])
    m3 = node(nt, "ShaderNodeMixRGB", (380, 0), blend_type="MULTIPLY")
    m3.inputs["Fac"].default_value = gk
    L.new(st.outputs["Color"], m3.inputs["Color1"])
    L.new(mr.outputs["Result"], m3.inputs["Color2"])
    L.new(m3.outputs["Color"], cr2.inputs["Fac"])
    L.new(cr2.outputs["Color"], inv.inputs["Color"])
    L.new(inv.outputs["Color"], mix.inputs["Fac"])
    L.new(emi.outputs["Emission"], mix.inputs[1])
    L.new(tra.outputs["BSDF"], mix.inputs[2])
    L.new(mix.outputs["Shader"], out.inputs["Surface"])
    return mat


for name, col, scl, th, disp, rz, band, gk, zk in LAYERS:
    ob = bpy.data.objects.new(name, teardrop(name))
    sc.collection.objects.link(ob)
    ob.scale = (scl, scl, scl * zk)
    ob.rotation_euler = (0, 0, math.radians(rz) * 0.15)   # xoay nhẹ: xoay mạnh đưa giọt bên của một lớp ra trước, che nửa ngọn lửa
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.modifiers.new("Min", "SUBSURF").levels = 2
    d = ob.modifiers.new("Phong", "DISPLACE")
    d.texture, d.texture_coords, d.texture_coords_object = t_disp, "OBJECT", ripple
    d.strength, d.mid_level = disp, 0.5
    bd = ob.modifiers.new("Lac", "SIMPLE_DEFORM")
    bd.deform_method, bd.deform_axis = "BEND", "Y"
    F.keys(bd, "angle", [(0, 0.0), (P / 4, 0.12), (3 * P / 4, -0.12), (P, 0.0)])
    ob.data.materials.append(flame_material(name, col, th, math.radians(rz), band, gk))

F.setup_render((0, -30, 1.75), 4.9, 352, 352)
sc.render.engine = "BLENDER_EEVEE"
try:
    sc.eevee.taa_render_samples = 16
except Exception:
    pass
sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"
F.run(OUT, "lua_bl", (0, -30, 1.75), 4.9, 352, 352, frames=FRAMES, save=SAVE, save_frame=1, loop=True, anchor_xz=(0, 0.0))
