# -*- coding: utf-8 -*-
"""Thư viện dựng VFX anime trong Blender (chạy trong blender -b): lớp vỏ Emission phẳng, trọng số từ texture, ăn mòn bằng Mask,
gradient bằng texture Blend gắn Empty, vỡ mảnh bằng Geometry Nodes, render Workbench tô phẳng nền trong.
Cách làm và lý do: skill vfx-petclash/blender_anime_fx.md. Mẫu dùng: phun_blender.py, cau_blender.py, no_blender.py.
"""
import json
import math
import os

import bmesh
import bpy
from mathutils import Vector

FPS = 24
PAL = {"kem": "#FFF6D6", "vang": "#FFD94A", "cam": "#FFA43A", "do": "#E8452E", "than": "#6E1A2A"}


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


def reset(n_frames):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, n_frames
    return sc


def empty(name, loc=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.location, e.scale, e.rotation_euler = loc, scale, rot
    bpy.context.scene.collection.objects.link(e)
    return e


def clouds(name, scale, basis="BLENDER_ORIGINAL", depth=2, contrast=1.0):
    t = bpy.data.textures.new(name, "CLOUDS")
    t.noise_scale, t.noise_basis, t.noise_type, t.noise_depth, t.contrast = scale, basis, "SOFT_NOISE", depth, contrast
    return t


def blend_tex(name="Grad"):
    t = bpy.data.textures.get(name) or bpy.data.textures.new(name, "BLEND")
    t.progression = "LINEAR"
    return t


def half_sphere(name, fn, subdiv=5, keep_y=0.06):
    """Nửa quả cầu phía camera (y âm): lỗ thủng là thủng thật. fn(x, y, z) -> Vector nắn hình."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > keep_y], context="VERTS")
    for v in bm.verts:
        v.co = fn(*v.co)
    bm.to_mesh(me)
    bm.free()
    return me


def shell(name, me, color, parent, groups):
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = parent
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = lin(color)
    me.materials.append(mat)
    allv = list(range(len(me.vertices)))
    for g in groups:
        ob.vertex_groups.new(name=g).add(allv, 0.0, "REPLACE")
    return ob


def vwe(ob, nm, group, tex, mapobj, const=1.0):
    """Nhóm đang 0 → trọng số = giá trị texture (toạ độ theo Empty mapobj)."""
    m = ob.modifiers.new(nm, "VERTEX_WEIGHT_EDIT")
    m.vertex_group, m.falloff_type, m.invert_falloff = group, "LINEAR", True
    m.mask_constant, m.mask_texture, m.mask_tex_use_channel = const, tex, "INT"
    m.mask_tex_mapping, m.mask_tex_map_object = "OBJECT", mapobj
    return m


def mix(ob, nm, a, b, mode, const=1.0):
    m = ob.modifiers.new(nm, "VERTEX_WEIGHT_MIX")
    m.vertex_group_a, m.vertex_group_b, m.mix_mode, m.mix_set, m.mask_constant = a, b, mode, "ALL", const
    return m


def displace(ob, nm, group=None, strength=0.0):
    d = ob.modifiers.new(nm, "DISPLACE")
    if group:
        d.vertex_group = group
    d.mid_level, d.direction, d.strength = 0.0, "NORMAL", strength
    return d


def mask(ob, nm, group, threshold):
    m = ob.modifiers.new(nm, "MASK")
    m.vertex_group, m.threshold = group, threshold
    return m


def smooth(ob, iters):
    s = ob.modifiers.new("Tron", "SMOOTH")
    s.factor, s.iterations = 1.0, iters
    return s


def angular(ob, ratio=0.3):
    d = ob.modifiers.new("GocCanh", "DECIMATE")
    d.decimate_type, d.ratio = "COLLAPSE", ratio
    return d


def shatter_group(name, t0, speed, gravity, radial=0.0, jitter=(1.6, 0.6, 2.0), bias=(0.3, 0.0, 0.45),
                  vor_scale=1.6, center=(0, 0, 0)):
    """Mảnh tàn: mỗi đảo lưới đi một hướng theo tâm của nó (không kéo giãn), cộng trọng lực, từ giây t0.
    hướng = radial·chuẩn(tâm − center) + (màu Voronoi(tâm) − 0,5)·jitter + bias."""
    ng = bpy.data.node_groups.new(name, "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, Lk = ng.nodes, ng.links

    def vm(op, b=None):
        n = N.new("ShaderNodeVectorMath")
        n.operation = op
        if b is not None:
            n.inputs[1].default_value = b
        return n

    def m(op, b=None):
        n = N.new("ShaderNodeMath")
        n.operation = op
        if b is not None:
            n.inputs[1].default_value = b
        return n

    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")
    sp = N.new("GeometryNodeSetPosition")
    pos = N.new("GeometryNodeInputPosition")
    isl = N.new("GeometryNodeInputMeshIsland")
    acc = N.new("GeometryNodeAccumulateField"); acc.data_type = "FLOAT_VECTOR"; acc.domain = "POINT"
    cnt = N.new("GeometryNodeAccumulateField"); cnt.data_type = "FLOAT"; cnt.domain = "POINT"
    gid = lambda nd: [i for i in nd.inputs if i.name in ("Group ID", "Group Index")][0]
    val = lambda nd: [i for i in nd.inputs if i.name == "Value" and i.enabled][0]
    tot = lambda nd: [o for o in nd.outputs if o.name == "Total" and o.enabled][0]
    val(cnt).default_value = 1.0
    inv = N.new("ShaderNodeMath"); inv.operation = "DIVIDE"; inv.inputs[0].default_value = 1.0
    cen = vm("SCALE")
    vor = N.new("ShaderNodeTexVoronoi"); vor.voronoi_dimensions = "3D"; vor.feature = "F1"
    vor.inputs["Scale"].default_value = vor_scale
    rad = vm("SUBTRACT", center)
    nrm = vm("NORMALIZE")
    radk = vm("SCALE")
    radk.inputs["Scale"].default_value = radial
    jsub = vm("SUBTRACT", (0.5, 0.5, 0.5))
    jmul = vm("MULTIPLY", jitter)
    add1 = vm("ADD")
    add2 = vm("ADD", bias)
    st = N.new("GeometryNodeInputSceneTime")
    tsub = m("SUBTRACT", t0)
    tmax = m("MAXIMUM", 0.0)
    spd = m("MULTIPLY", speed)
    vsc = vm("SCALE")
    tt = m("MULTIPLY")
    gm = m("MULTIPLY", -0.5 * gravity)
    cxyz = N.new("ShaderNodeCombineXYZ")
    out = vm("ADD")
    for a, b in [(gi.outputs[0], sp.inputs["Geometry"]), (sp.outputs["Geometry"], go.inputs[0]),
                 (pos.outputs["Position"], val(acc)), (isl.outputs["Island Index"], gid(acc)),
                 (isl.outputs["Island Index"], gid(cnt)), (tot(cnt), inv.inputs[1]), (tot(acc), cen.inputs[0]),
                 (inv.outputs[0], cen.inputs["Scale"]), (cen.outputs[0], vor.inputs["Vector"]),
                 (cen.outputs[0], rad.inputs[0]), (rad.outputs[0], nrm.inputs[0]), (nrm.outputs[0], radk.inputs[0]),
                 (vor.outputs["Color"], jsub.inputs[0]), (jsub.outputs[0], jmul.inputs[0]),
                 (radk.outputs[0], add1.inputs[0]), (jmul.outputs[0], add1.inputs[1]), (add1.outputs[0], add2.inputs[0]),
                 (st.outputs["Seconds"], tsub.inputs[0]), (tsub.outputs[0], tmax.inputs[0]), (tmax.outputs[0], spd.inputs[0]),
                 (add2.outputs[0], vsc.inputs[0]), (spd.outputs[0], vsc.inputs["Scale"]),
                 (tmax.outputs[0], tt.inputs[0]), (tmax.outputs[0], tt.inputs[1]), (tt.outputs[0], gm.inputs[0]),
                 (gm.outputs[0], cxyz.inputs["Z"]), (vsc.outputs[0], out.inputs[0]), (cxyz.outputs[0], out.inputs[1]),
                 (out.outputs[0], sp.inputs["Offset"])]:
        Lk.new(a, b)
    return ng


def add_nodes(ob, ng):
    g = ob.modifiers.new(ng.name, "NODES")
    g.node_group = ng
    return g


def flat_star(name, n, ro, ri, color, y=-3.0, center=(0, 0), rot=0.0):
    """Ngôi sao phẳng quay mặt về camera (mặt phẳng XZ), màu phẳng."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = []
    for i in range(2 * n):
        a = rot + i * math.pi / n
        r = ro if i % 2 == 0 else ri
        vs.append(bm.verts.new((center[0] + r * math.cos(a), y, center[1] + r * math.sin(a))))
    bm.faces.new(vs)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = lin(color)
    me.materials.append(mat)
    return ob


def setup_render(cam_xyz, ortho, w, h):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("Cam")
    cd.type, cd.ortho_scale = "ORTHO", ortho
    cam = bpy.data.objects.new("Cam", cd)
    cam.location, cam.rotation_euler = cam_xyz, (math.radians(90), 0, 0)
    sc.collection.objects.link(cam)
    sc.camera = cam
    r = sc.render
    r.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light, sc.display.shading.color_type = "FLAT", "MATERIAL"
    sc.display.render_aa = "16"
    r.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100
    r.image_settings.file_format, r.image_settings.color_mode = "PNG", "RGBA"


def run(out, prefix, cam_xyz, ortho, w, h, frames=None, save=None, save_frame=1, loop=False, anchor_xz=(0, 0)):
    """Lưu .blend (nếu có), render các khung vào out (đường dẫn tuyệt đối), ghi info.json (điểm neo theo px)."""
    sc = bpy.context.scene
    if save:
        sc.frame_set(save_frame)
        bpy.ops.wm.save_as_mainfile(filepath=save)
    os.makedirs(out, exist_ok=True)
    frames = frames or list(range(sc.frame_start, sc.frame_end + 1))
    for f in frames:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, f"{prefix}_{f - 1:02d}.png")
        bpy.ops.render.render(write_still=True)
    upp = ortho / w
    anchor = [round((anchor_xz[0] - cam_xyz[0]) / upp + w / 2), round(h / 2 - (anchor_xz[1] - cam_xyz[2]) / upp)]
    json.dump(dict(count=sc.frame_end, w=w, h=h, fps=FPS, loop=loop, anchor=anchor),
              open(os.path.join(out, "info.json"), "w"))
    print("OK", len(frames), "khung, neo", anchor)


def standard_stack(ob, van, van_tex, vmin, vmin_tex, fine_k=0.22, grads=(), disp=0.35, disp_keys=None, th=0.5,
                   th_keys=None, push=0.0, smooth_it=25, angular_ratio=None, twist=None, shatter=None):
    """Chuỗi modifier chuẩn (mục 3 của skill): W = vân + vân nhỏ; D = vân (phồng); gradient nhân vào W / D;
    Displace ×2; Mask theo ngưỡng; Smooth; (mép gãy); (xoắn); đẩy lớp; (vỡ mảnh).
    grads: dict(group, tex, empty, w=hằng trộn vào W, d=hằng trộn vào D, mode='MUL')."""
    vwe(ob, "Van", "W", van_tex, van)
    vwe(ob, "VanMin", "F", vmin_tex, vmin)
    mix(ob, "ChepD", "D", "W", "SET")
    mix(ob, "CongMin", "W", "F", "ADD", fine_k)
    for g in grads:
        vwe(ob, "G" + g["group"], g["group"], g["tex"], g["empty"])
        mode = g.get("mode", "MUL")
        if g.get("w") is not None:
            mix(ob, "W" + g["group"], "W", g["group"], mode, g["w"])
        if g.get("d") is not None:
            mix(ob, "D" + g["group"], "D", g["group"], mode, g["d"])
    d1 = displace(ob, "Phong", "D", disp)
    ob.modifiers.new("Min", "SUBSURF").levels = 1
    d2 = displace(ob, "Phong2", "D", disp * 0.5)
    if disp_keys:
        keys(d1, "strength", disp_keys)
        keys(d2, "strength", [(t, v * 0.5) for t, v in disp_keys])
    mk = mask(ob, "AnMon", "W", th)
    if th_keys:
        keys(mk, "threshold", th_keys)
    smooth(ob, smooth_it)
    if angular_ratio:
        angular(ob, angular_ratio)
    if twist:
        sd = ob.modifiers.new("Xoan", "SIMPLE_DEFORM")
        sd.deform_method, sd.deform_axis, sd.angle = "TWIST", "Z", twist
    displace(ob, "DayRa", None, push)
    if shatter:
        add_nodes(ob, shatter)
    return mk


def two_tone(ob, back_color):
    """Mặt sau (y > 0) một màu khác (nguội hơn): nhìn qua lỗ thủng thấy vách sau tối hơn, có chiều sâu."""
    mat = bpy.data.materials.new(ob.name + "_sau")
    mat.diffuse_color = lin(back_color)
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        if p.center.y > 0:
            p.material_index = 1


def args():
    import sys
    a = sys.argv[sys.argv.index("--") + 1:]
    out = a[0]
    frames = [int(x) for x in a[a.index("--frames") + 1].split(",")] if "--frames" in a else None
    save = a[a.index("--save") + 1] if "--save" in a else None
    return out, frames, save
