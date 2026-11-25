# -*- coding: utf-8 -*-
"""Lốc xoáy lửa lấy THẲNG từ file mẫu đã mua "Updated and Simplified Tornado 280.blend" (CodyWinch), giữ nguyên rig gốc
(lattice + chuỗi warp, noise lắc, lớp thân / tia / sét, Thin ép về trục), chỉ đổi sang màu phẳng của game, bỏ sàn / đèn / khối volume,
camera trực giao góc ngang, nền trong, render Workbench tô phẳng.

    blender.exe -b --disable-autoexec "<mẫu>.blend" --python loc_tu_mau.py -- <thư_mục_ra> [khung_đầu khung_cuối bước] [--khoi]
Mặc định khung 41→135 bước 2 (48 khung = 2 s ở 24 fps). --khoi: giữ lớp khói của mẫu (mặc định ẩn, khói do AtomSpine rải).
"""
import json
import math
import os
import sys

import bpy

a = sys.argv[sys.argv.index("--") + 1:]
OUT = a[0]
nums = [x for x in a[1:] if not x.startswith("--") and not x.endswith(".blend")]
F0, F1, STEP = (int(nums[0]), int(nums[1]), int(nums[2])) if len(nums) >= 3 else (41, 135, 2)
KEEP_SMOKE = "--khoi" in a
os.makedirs(OUT, exist_ok=True)


def lin(h):
    h = h.lstrip("#")

    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return tuple(f(int(h[i:i + 2], 16)) for i in (0, 2, 4)) + (1.0,)


MAU = {  # vật liệu gốc → màu phẳng của game, tông rực cháy (người dùng chê bản đỏ sẫm "ngả nâu", 2026-11-24)
    "Shadow": "#E0302A", "Orange": "#FF9A26", "Highlight": "#FFE14D", "Smoke": "#9A8A80",
    "Red Sparks": "#FFD94A", "Blue Lightning": "#FFF6D6",
}
NUOC = "--nuoc" in a   # lốc NƯỚC (bộ nước 2026-11-24): cùng rig, màu xanh dương của tia nước (nuocbl.C), khói thành hơi nước trắng xanh
if NUOC:
    MAU = {"Shadow": "#2A7BC8", "Orange": "#4FCDF6", "Highlight": "#93E8FF", "Smoke": "#D2F1FF",
           "Red Sparks": "#EAFBFF", "Blue Lightning": "#EAFBFF"}
TEN = "loc_nuoc" if NUOC else "loc_bl"
sc = bpy.context.scene
for m in bpy.data.materials:
    if m.name in MAU:
        col = lin(MAU[m.name])
        m.diffuse_color = col
        if m.use_nodes:
            for nd in m.node_tree.nodes:
                if nd.bl_idname == "ShaderNodeEmission":
                    nd.inputs["Color"].default_value = col
for ob in sc.objects:
    if ob.type == "MESH" and ob.name in ("Plane", "Cube"):
        ob.hide_render = True
    if ob.name == "Smoke" and not KEEP_SMOKE:
        ob.hide_render = True

WIND = "--gio" in a
if WIND:
    import bmesh
    for ob in sc.objects:
        if ob.name == "Smoke":
            ob.hide_render = False
    FPS_SRC = sc.render.fps
    T_FADE0, T_FADE1 = 112 / FPS_SRC, 128 / FPS_SRC        # tắt cùng lúc lốc ép về trục (khung gốc 96–132)

    def flat_mat(name, hexcol):
        m = bpy.data.materials.new(name)
        m.diffuse_color = lin(hexcol)
        return m

    # ---- gió cuốn: dải mảnh cong theo cung xoắn ốc quanh lốc, vuốt nhọn hai đầu, mỗi dải quay một tốc độ
    ARCS = [  # (cao z, bán kính, độ dài cung (độ), bề rộng, tốc độ (vòng/giây gốc), góc đầu, nghiêng)
        (0.8, 2.2, 150, 0.16, 0.6, 0, 18), (2.6, 2.3, 130, 0.14, 0.45, 120, -22), (4.4, 2.9, 165, 0.18, 0.55, 240, 15),
        (6.2, 3.6, 140, 0.18, 0.4, 60, -20), (7.9, 4.3, 170, 0.2, 0.5, 200, 24), (9.4, 4.9, 125, 0.16, 0.36, 300, -16),
        (5.2, 3.2, 110, 0.12, 0.65, 150, 28),
    ]
    mat_gio = flat_mat("Gio", "#EAFBFF" if NUOC else "#FFF3D2")
    for i, (z, R, L, wd, spd, a0, tilt) in enumerate(ARCS):
        me = bpy.data.meshes.new("gio%d" % i)
        bm = bmesh.new()
        n = 48
        top, bot = [], []
        for k in range(n + 1):
            u = k / n
            ph = math.radians(a0 + u * L)
            w = wd * math.sin(math.pi * u) ** 0.8
            zz = z + 1.5 * u                                 # xoắn dốc lên như luồng gió cuốn
            top.append(bm.verts.new((R * math.cos(ph), R * math.sin(ph), zz + w / 2)))
            bot.append(bm.verts.new((R * math.cos(ph), R * math.sin(ph), zz - w / 2)))
        for k in range(n):
            bm.faces.new((top[k], top[k + 1], bot[k + 1], bot[k]))
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mat_gio)
        ob = bpy.data.objects.new("gio%d" % i, me)
        sc.collection.objects.link(ob)
        ob.rotation_euler = (math.radians(tilt), 0, 0)
        bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
        for fr_, ang in ((F0, 0.0), (F1, spd * 2 * math.pi * (F1 - F0) / FPS_SRC)):
            ob.rotation_euler[2] = ang
            ob.keyframe_insert("rotation_euler", index=2, frame=fr_)
        for fr_, sv in ((F0, 1.0), (int(T_FADE0 * FPS_SRC), 1.0), (int(T_FADE1 * FPS_SRC), 0.0)):
            ob.scale = (sv, sv, sv)
            ob.keyframe_insert("scale", frame=fr_)

    # ---- tro + tàn lửa bay vòng: Geometry Nodes, điểm quay quanh trục theo phễu, bốc dần lên, tắt cùng lốc
    def orbit_group(name, count, seed, r0, r1, s0, s1, w0, w1, rise, mat):
        ng = bpy.data.node_groups.new(name, "GeometryNodeTree")
        ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
        ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
        NN, LL = ng.nodes, ng.links
        idx = NN.new("GeometryNodeInputIndex")

        def rnd(lo, hi, sd):
            r = NN.new("FunctionNodeRandomValue")
            r.data_type = "FLOAT"
            r.inputs["Min"].default_value = lo
            r.inputs["Max"].default_value = hi
            r.inputs["Seed"].default_value = sd
            LL.new(idx.outputs[0], r.inputs["ID"])
            return [o for o in r.outputs if o.name == "Value" and o.enabled][0]

        def m(op, x_=None, y_=None):
            nd = NN.new("ShaderNodeMath")
            nd.operation = op
            for k_, v_ in ((0, x_), (1, y_)):
                if v_ is None:
                    continue
                if isinstance(v_, (int, float)):
                    nd.inputs[k_].default_value = v_
                else:
                    LL.new(v_, nd.inputs[k_])
            return nd.outputs[0]

        go = NN.new("NodeGroupOutput")
        pts = NN.new("GeometryNodePoints")
        pts.inputs["Count"].default_value = count
        st = NN.new("GeometryNodeInputSceneTime")
        t = st.outputs["Seconds"]
        Hh = 10.4
        r = rnd(r0, r1, seed)
        h0 = rnd(0, Hh, seed + 1)
        th0 = rnd(0, 6.283, seed + 2)
        w = rnd(w0, w1, seed + 3)
        sz = rnd(s0, s1, seed + 4)
        h = m("FLOORED_MODULO", m("ADD", h0, m("MULTIPLY", t, rise)), Hh)
        reff = m("MULTIPLY", r, m("ADD", 0.45, m("MULTIPLY", h, 0.6 / Hh)))
        th = m("ADD", th0, m("MULTIPLY", w, t))
        x = m("MULTIPLY", reff, m("COSINE", th))
        y = m("MULTIPLY", reff, m("SINE", th))
        cxyz = NN.new("ShaderNodeCombineXYZ")
        LL.new(x, cxyz.inputs["X"])
        LL.new(y, cxyz.inputs["Y"])
        LL.new(h, cxyz.inputs["Z"])
        LL.new(cxyz.outputs[0], pts.inputs["Position"])
        mr = NN.new("ShaderNodeMapRange")
        mr.clamp = True
        mr.inputs["From Min"].default_value = T_FADE0
        mr.inputs["From Max"].default_value = T_FADE1
        mr.inputs["To Min"].default_value = 1.0
        mr.inputs["To Max"].default_value = 0.0
        LL.new(t, mr.inputs["Value"])
        scl = m("MULTIPLY", sz, mr.outputs["Result"])
        ico = NN.new("GeometryNodeMeshIcoSphere")
        ico.inputs["Radius"].default_value = 1.0
        ico.inputs["Subdivisions"].default_value = 1
        iop = NN.new("GeometryNodeInstanceOnPoints")
        LL.new(pts.outputs[0], iop.inputs["Points"])
        LL.new(ico.outputs["Mesh"], iop.inputs["Instance"])
        LL.new(scl, iop.inputs["Scale"])
        rl = NN.new("GeometryNodeRealizeInstances")
        smat = NN.new("GeometryNodeSetMaterial")
        smat.inputs["Material"].default_value = mat
        LL.new(iop.outputs[0], rl.inputs[0])
        LL.new(rl.outputs[0], smat.inputs["Geometry"])
        LL.new(smat.outputs[0], go.inputs[0])
        holder = bpy.data.objects.new(name, bpy.data.meshes.new(name))
        sc.collection.objects.link(holder)
        md = holder.modifiers.new(name, "NODES")
        md.node_group = ng
        return holder

    orbit_group("TanLua", 34, 11, 1.6, 5.2, 0.07, 0.14, 1.2, 2.2, 0.9, flat_mat("Tan", "#93E8FF" if NUOC else "#FFB02E"))
    orbit_group("TanVang", 18, 23, 1.4, 4.6, 0.05, 0.1, 1.5, 2.6, 1.1, flat_mat("TanVang", "#EAFBFF" if NUOC else "#FFE14D"))
    orbit_group("Tro", 30, 37, 2.0, 6.0, 0.06, 0.13, 0.9, 1.7, 0.7, flat_mat("Tro", "#4FCDF6" if NUOC else "#5F534D"))

W, H, ORTHO, CX, CZ = (480, 440, 16.0, 0.0, 5.2) if WIND else (320, 400, 10.8, 0.0, 5.3)
cd = bpy.data.cameras.new("CamGame")
cd.type, cd.ortho_scale = "ORTHO", ORTHO
cam = bpy.data.objects.new("CamGame", cd)
cam.location, cam.rotation_euler = (CX, -40, CZ), (math.radians(90), 0, 0)
sc.collection.objects.link(cam)
sc.camera = cam
r = sc.render
r.engine = "BLENDER_WORKBENCH"
sc.display.shading.light, sc.display.shading.color_type = "FLAT", "MATERIAL"
sc.display.shading.show_object_outline = False
sc.display.render_aa = "16"
r.film_transparent = True
sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"
r.resolution_x, r.resolution_y, r.resolution_percentage = W, H, 100
r.image_settings.file_format, r.image_settings.color_mode = "PNG", "RGBA"
if "--save" in a:   # lưu bản đã đổi màu ra file riêng (không ghi đè file mẫu)
    bpy.ops.wm.save_as_mainfile(filepath=a[a.index("--save") + 1], copy=True)
frames = list(range(F0, F1 + 1, STEP))
for i, f in enumerate(frames):
    sc.frame_set(f)
    r.filepath = os.path.join(OUT, f"{TEN}_{i:02d}.png")
    bpy.ops.render.render(write_still=True)
upp = ORTHO / W
anchor = [round(W / 2 - CX / upp), round(H / 2 + CZ / upp)]   # chân lốc (0, 0, 0)
json.dump(dict(count=len(frames), w=W, h=H, fps=24, loop=False, anchor=anchor, src_frames=[F0, F1, STEP]),
          open(os.path.join(OUT, "info.json"), "w"))
print("OK", len(frames), "khung, neo", anchor)
