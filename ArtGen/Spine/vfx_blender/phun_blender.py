# -*- coding: utf-8 -*-
"""Phun lửa dựng bằng Blender theo kỹ thuật anime FX (skill vfx-petclash/blender_anime_fx.md), render ra khung 2D.

    blender.exe -b --factory-startup --python phun_blender.py -- <thư_mục_ra_tuyệt_đối> [--frames 1,10,20] [--save x.blend]

- Lưới gốc: nửa quả cầu (phía camera) nắn thành phễu: nhọn ở miệng (x=0), phình ở cuối (x=L).
- 5 lớp vỏ Emission phẳng ngoài → trong: kem, vàng, cam, đỏ, đỏ sẫm. Cùng một trường trọng số (texture Clouds trôi theo +X),
  ngưỡng Mask lệch theo lớp: lớp ngoài thủng trước → lửa nguội dần, cuối cùng còn đảo đỏ sẫm = mảnh tàn.
- Đuôi đứt từ gốc: texture Blend (gradient) gắn Empty "Duoi" chạy từ miệng ra, nhân vào trọng số.
- Mảnh tàn bung + rơi: Geometry Nodes, mỗi ô Voronoi (theo vị trí) một hướng, cộng trọng lực, bắt đầu từ T_VO.
- Render Workbench tô phẳng (màu = diffuse_color), nền trong, camera trực giao nhìn từ -Y, 24 khung/giây.
"""
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
FRAMES = None
SAVE = None
if "--frames" in argv:
    FRAMES = [int(x) for x in argv[argv.index("--frames") + 1].split(",")]
if "--save" in argv:
    SAVE = argv[argv.index("--save") + 1]

FPS = 24
T_END = 2.05
L = 6.0            # chiều dài luồng lửa (đơn vị Blender)
T_VO = 1.45        # giây bắt đầu vỡ mảnh
SPEED = 1.15       # tốc độ bung mảnh
G = 4.5            # trọng lực mảnh
W_PX, H_PX = 720, 400
ORTHO = 9.8
CAM = (L / 2 + 0.75, -30.0, 0.35)

# Ngưỡng Mask từng lớp theo giờ (giây: ngưỡng). Đo phân bố trọng số W (do_trong_so.py, 2026-11-24): phân vị
# 5% 0,46 · 20% 0,57 · 40% 0,655 · 60% 0,72 · 80% 0,79 · 95% 0,90 → ngưỡng = phân vị (1 − tỉ lệ phủ muốn có).
LAYERS = [  # (tên, màu sRGB, khoá ngưỡng, đẩy ra)
    ("kem", "#FFF6D6", [(0, 0.79), (0.7, 0.83), (0.95, 1.05)], 0.10),
    ("vang", "#FFD94A", [(0, 0.30), (0.65, 0.44), (0.85, 0.57), (1.05, 0.70), (1.25, 0.81), (1.4, 1.05)], 0.075),
    ("cam", "#FFA43A", [(0, 0.34), (0.85, 0.42), (1.05, 0.54), (1.25, 0.67), (1.45, 0.79), (1.6, 1.05)], 0.05),
    ("do", "#E8452E", [(0, 0.38), (1.0, 0.44), (1.15, 0.50), (1.35, 0.655), (1.55, 0.75), (1.75, 1.05)], 0.025),
    ("than", "#6E1A2A", [(0, 0.42), (1.2, 0.46), (1.4, 0.60), (1.55, 0.72), (1.7, 0.82), (1.85, 0.92), (1.95, 1.05)], 0.0),
]


def lin(h):
    h = h.lstrip("#")

    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return tuple(f(int(h[i:i + 2], 16)) for i in (0, 2, 4)) + (1.0,)


def fr(t):
    return 1 + t * FPS


def keys(owner, prop, pairs, index=-1):
    for t, v in pairs:
        if index >= 0:
            getattr(owner, prop)[index] = v
        else:
            setattr(owner, prop, v)
        owner.keyframe_insert(data_path=prop, index=index, frame=fr(t))


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start = 1
sc.frame_end = int(round(T_END * FPS)) + 1

# ---------------------------------------------------------------- điều khiển (Empty)
def empty(name, loc=(0, 0, 0), scale=(1, 1, 1)):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    e.scale = scale
    sc.collection.objects.link(e)
    return e


goc = empty("Goc")                       # gốc tại miệng: phóng to luồng lửa
van = empty("Van")                       # toạ độ vân Clouds (trôi theo +X)
min_ = empty("VanMin", scale=(0.5, 0.5, 0.5))
duoi = empty("Duoi", loc=(-6, 0, 0), scale=(1.1, 1, 1))  # gradient cắt đuôi
thon = empty("Thon", loc=(0.35 * L, 0, 0), scale=(0.35 * L, 1, 1))   # 0 ở miệng → 1 ở 0,7L: phồng ít sát miệng
dau = empty("Dau", loc=(0.3 * L, 0, 0), scale=(-0.3 * L, 1, 1))      # 1 ở miệng → 0 ở 0,6L: giữ nóng sát miệng
mep = empty("Mep", loc=(0.2, 0, 0), scale=(-1.3, 1, 1))               # mép đầu lửa: 1 phía sau mép, 0 phía trước

# bùng từ từ: mép đầu vươn từ miệng ra hết luồng trong ~0,7 s (nhanh rồi chậm), bề dày tăng dần, rồi to thêm khi giữ
keys(mep, "location", [(0, 0.3), (0.12, 1.0), (0.25, 2.7), (0.4, 4.4), (0.55, 5.9), (0.72, L + 1.6)], 0)
keys(goc, "scale", [(0, 0.92), (0.7, 1.0), (T_END, 1.06)], 0)
keys(goc, "scale", [(0, 0.3), (0.15, 0.45), (0.35, 0.72), (0.6, 0.93), (0.85, 1.0), (T_END, 1.12)], 1)
keys(goc, "scale", [(0, 0.3), (0.15, 0.45), (0.35, 0.72), (0.6, 0.93), (0.85, 1.0), (T_END, 1.12)], 2)
keys(van, "location", [(0, 0.0), (T_END, -4.4)], 0)
keys(van, "location", [(0, 0.0), (T_END, -0.9)], 2)
keys(van, "scale", [(0, 1.0), (T_END, 1.35)], 0)
keys(van, "scale", [(0, 1.0), (T_END, 1.35)], 2)
keys(min_, "location", [(0, 0.0), (T_END, -5.5)], 0)
keys(duoi, "location", [(0, -6.0), (1.18, -6.0), (1.2, -1.2), (1.6, 0.5 * L), (T_END, 0.5 * L + 0.4)], 0)

# ---------------------------------------------------------------- texture
t_van = bpy.data.textures.new("Van", "CLOUDS")
t_van.noise_scale = 0.55
t_van.noise_basis = "BLENDER_ORIGINAL"
t_van.noise_type = "SOFT_NOISE"
t_van.noise_depth = 2
t_min = bpy.data.textures.new("VanMin", "CLOUDS")
t_min.noise_scale = 0.12
t_min.noise_basis = "VORONOI_F1"
t_min.contrast = 3
t_duoi = bpy.data.textures.new("Duoi", "BLEND")
t_duoi.progression = "LINEAR"


# ---------------------------------------------------------------- lưới gốc: nửa cầu nắn thành phễu
def base_mesh(name):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=5, radius=1.0)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.06], context="VERTS")
    for v in bm.verts:
        x, y, z = v.co
        s = (x + 1) / 2
        g = 0.07 + 1.55 * (s ** 1.25)
        v.co = Vector((s * L, y * g, z * g + 0.25 * s * s))  # ngóc lên nhẹ về cuối
    bm.to_mesh(me)
    bm.free()
    return me


# ---------------------------------------------------------------- Geometry Nodes: mảnh tàn bung + rơi
def shatter_group():
    ng = bpy.data.node_groups.new("VoManh", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, Lk = ng.nodes, ng.links
    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")
    sp = N.new("GeometryNodeSetPosition")
    pos = N.new("GeometryNodeInputPosition")
    vor = N.new("ShaderNodeTexVoronoi")
    vor.voronoi_dimensions = "3D"
    vor.feature = "F1"
    vor.inputs["Scale"].default_value = 1.6
    st = N.new("GeometryNodeInputSceneTime")
    sub = N.new("ShaderNodeMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = T_VO
    mx = N.new("ShaderNodeMath"); mx.operation = "MAXIMUM"; mx.inputs[1].default_value = 0.0
    vsub = N.new("ShaderNodeVectorMath"); vsub.operation = "SUBTRACT"; vsub.inputs[1].default_value = (0.5, 0.5, 0.5)
    vmul = N.new("ShaderNodeVectorMath"); vmul.operation = "MULTIPLY"; vmul.inputs[1].default_value = (1.6, 0.6, 2.0)
    vadd = N.new("ShaderNodeVectorMath"); vadd.operation = "ADD"; vadd.inputs[1].default_value = (0.3, 0.0, 0.45)
    spd = N.new("ShaderNodeMath"); spd.operation = "MULTIPLY"; spd.inputs[1].default_value = SPEED
    vsc = N.new("ShaderNodeVectorMath"); vsc.operation = "SCALE"
    tt = N.new("ShaderNodeMath"); tt.operation = "MULTIPLY"
    gm = N.new("ShaderNodeMath"); gm.operation = "MULTIPLY"; gm.inputs[1].default_value = -0.5 * G
    cxyz = N.new("ShaderNodeCombineXYZ")
    vadd2 = N.new("ShaderNodeVectorMath"); vadd2.operation = "ADD"
    Lk.new(gi.outputs[0], sp.inputs["Geometry"])
    Lk.new(sp.outputs["Geometry"], go.inputs[0])
    isl = N.new("GeometryNodeInputMeshIsland")
    acc = N.new("GeometryNodeAccumulateField"); acc.data_type = "FLOAT_VECTOR"; acc.domain = "POINT"
    cnt = N.new("GeometryNodeAccumulateField"); cnt.data_type = "FLOAT"; cnt.domain = "POINT"
    gid = lambda nd: [i for i in nd.inputs if i.name in ("Group ID", "Group Index")][0]
    val = lambda nd: [i for i in nd.inputs if i.name == "Value" and i.enabled][0]
    tot = lambda nd: [o for o in nd.outputs if o.name == "Total" and o.enabled][0]
    val(cnt).default_value = 1.0
    inv = N.new("ShaderNodeMath"); inv.operation = "DIVIDE"; inv.inputs[0].default_value = 1.0
    cen = N.new("ShaderNodeVectorMath"); cen.operation = "SCALE"
    Lk.new(pos.outputs["Position"], val(acc))
    Lk.new(isl.outputs["Island Index"], gid(acc))
    Lk.new(isl.outputs["Island Index"], gid(cnt))
    Lk.new(tot(cnt), inv.inputs[1])
    Lk.new(tot(acc), cen.inputs[0])
    Lk.new(inv.outputs[0], cen.inputs["Scale"])
    Lk.new(cen.outputs[0], vor.inputs["Vector"])
    Lk.new(st.outputs["Seconds"], sub.inputs[0])
    Lk.new(sub.outputs[0], mx.inputs[0])
    Lk.new(vor.outputs["Color"], vsub.inputs[0])
    Lk.new(vsub.outputs[0], vmul.inputs[0])
    Lk.new(vmul.outputs[0], vadd.inputs[0])
    Lk.new(vadd.outputs[0], vsc.inputs[0])
    Lk.new(mx.outputs[0], spd.inputs[0])
    Lk.new(spd.outputs[0], vsc.inputs["Scale"])
    Lk.new(mx.outputs[0], tt.inputs[0])
    Lk.new(mx.outputs[0], tt.inputs[1])
    Lk.new(tt.outputs[0], gm.inputs[0])
    Lk.new(gm.outputs[0], cxyz.inputs["Z"])
    Lk.new(vsc.outputs[0], vadd2.inputs[0])
    Lk.new(cxyz.outputs[0], vadd2.inputs[1])
    Lk.new(vadd2.outputs[0], sp.inputs["Offset"])
    return ng


NG = shatter_group()

# ---------------------------------------------------------------- 5 lớp vỏ
DISP = [(0, 0.10), (0.3, 0.30), (0.7, 0.55), (1.2, 0.72), (T_END, 0.92)]

for idx, (name, col, th_keys, push) in enumerate(LAYERS):
    me = base_mesh(name)
    ob = bpy.data.objects.new(name, me)
    sc.collection.objects.link(ob)
    ob.parent = goc
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = lin(col)
    me.materials.append(mat)
    allv = list(range(len(me.vertices)))
    for g in ("W", "D", "F", "P", "T", "J", "Q"):
        vg = ob.vertex_groups.new(name=g)
        vg.add(allv, 0.0, "REPLACE")
    M = ob.modifiers

    def vwe(nm, group, tex, mapobj, const=1.0):
        m = M.new(nm, "VERTEX_WEIGHT_EDIT")
        m.vertex_group = group
        m.falloff_type = "LINEAR"
        m.invert_falloff = True           # nhóm đang 0 → mới = 1, trộn theo texture: trọng số = giá trị texture
        m.mask_constant = const
        m.mask_texture = tex
        m.mask_tex_use_channel = "INT"
        m.mask_tex_mapping = "OBJECT"
        m.mask_tex_map_object = mapobj
        return m

    def mix(nm, a, b, mode, const=1.0):
        m = M.new(nm, "VERTEX_WEIGHT_MIX")
        m.vertex_group_a, m.vertex_group_b = a, b
        m.mix_mode, m.mix_set, m.mask_constant = mode, "ALL", const
        return m

    vwe("Van", "W", t_van, van)
    vwe("VanMin", "F", t_min, min_)
    mix("ChepD", "D", "W", "SET")
    mix("CongMin", "W", "F", "ADD", 0.22)
    vwe("Thon", "T", t_duoi, thon)
    mix("ThonD", "D", "T", "MUL")
    vwe("Dau", "J", t_duoi, dau)
    mix("NongDau", "W", "J", "ADD", 0.3)
    vwe("Mep", "Q", t_duoi, mep)
    mix("MepW", "W", "Q", "MUL")
    mix("MepD", "D", "Q", "MUL")
    vwe("Duoi", "P", t_duoi, duoi)
    mix("DuoiNhieu", "P", "W", "ADD", 0.4)   # mép đứt đuôi xé theo vân, cắt chung mọi lớp (không thành dải màu)
    d1 = M.new("Phong", "DISPLACE"); d1.vertex_group = "D"; d1.mid_level = 0.0; d1.direction = "NORMAL"
    M.new("Min", "SUBSURF").levels = 1
    d2 = M.new("Phong2", "DISPLACE"); d2.vertex_group = "D"; d2.mid_level = 0.0; d2.direction = "NORMAL"
    mk = M.new("AnMon", "MASK"); mk.vertex_group = "W"
    mk2 = M.new("CatDuoi", "MASK"); mk2.vertex_group = "P"; mk2.threshold = 0.72 + 0.03 * idx
    sm = M.new("Tron", "SMOOTH"); sm.factor = 1.0; sm.iterations = 25
    if name in ("do", "than"):  # lớp nguội thành mảnh tàn: mép sắc cạnh như giấy cháy
        sm.iterations = 8
        dec = M.new("GocCanh", "DECIMATE"); dec.decimate_type = "COLLAPSE"; dec.ratio = 0.3
    d3 = M.new("DayRa", "DISPLACE"); d3.mid_level = 0.0; d3.strength = push; d3.direction = "NORMAL"
    gn = M.new("VoManh", "NODES"); gn.node_group = NG
    keys(d1, "strength", DISP)
    keys(d2, "strength", [(t, v * 0.5) for t, v in DISP])
    keys(mk, "threshold", th_keys)

# ---------------------------------------------------------------- camera, render
cam_d = bpy.data.cameras.new("Cam")
cam_d.type = "ORTHO"
cam_d.ortho_scale = ORTHO
cam = bpy.data.objects.new("Cam", cam_d)
cam.location = CAM
cam.rotation_euler = (math.radians(90), 0, 0)
sc.collection.objects.link(cam)
sc.camera = cam
r = sc.render
r.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "FLAT"
sc.display.shading.color_type = "MATERIAL"
sc.display.render_aa = "16"
r.film_transparent = True
sc.view_settings.view_transform = "Standard"
r.resolution_x, r.resolution_y, r.resolution_percentage = W_PX, H_PX, 100
r.image_settings.file_format = "PNG"
r.image_settings.color_mode = "RGBA"

if SAVE:
    sc.frame_set(20)  # mở file là thấy lửa đang to
    bpy.ops.wm.save_as_mainfile(filepath=SAVE)
os.makedirs(OUT, exist_ok=True)
frames = FRAMES or list(range(sc.frame_start, sc.frame_end + 1))
for f in frames:
    sc.frame_set(f)
    r.filepath = os.path.join(OUT, f"phun_bl_{f - 1:02d}.png")
    bpy.ops.render.render(write_still=True)
upp = ORTHO / W_PX
anchor = [round((0 - CAM[0]) / upp + W_PX / 2), round(H_PX / 2 + CAM[2] / upp)]
json.dump(dict(count=sc.frame_end, w=W_PX, h=H_PX, fps=FPS, anchor=anchor),
          open(os.path.join(OUT, "info.json"), "w"))
print("OK", len(frames), "khung, neo", anchor)
