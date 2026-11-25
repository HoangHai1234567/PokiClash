# -*- coding: utf-8 -*-
"""Đọc cấu trúc một file .blend (chạy trong Blender, không mở giao diện, chặn script nhúng):

    blender.exe -b --disable-autoexec <file.blend> --python doc_blend.py -- <ra.json>

Ghi: cảnh (khung, fps, engine, độ phân giải, nền trong, quản lý màu, bloom), từng object (kiểu, vị trí, cha, nhóm đỉnh,
chuỗi modifier đủ thuộc tính, vật liệu), texture, cây node vật liệu, driver, keyframe (đường cong theo thuộc tính).
"""
import json
import sys

import bpy

out_path = sys.argv[sys.argv.index("--") + 1]


def val(v):
    if hasattr(v, "name") and hasattr(v, "bl_rna"):
        return f"<{v.bl_rna.identifier}:{v.name}>"
    if hasattr(v, "__len__") and not isinstance(v, str):
        try:
            return [val(x) for x in v][:16]
        except Exception:
            return str(v)
    if isinstance(v, float):
        return round(v, 4)
    return v if isinstance(v, (int, str, bool, type(None))) else str(v)


def props(obj, skip=("rna_type", "name", "type", "bl_rna")):
    d = {}
    for p in obj.bl_rna.properties:
        k = p.identifier
        if k in skip or p.type == "COLLECTION":
            continue
        try:
            d[k] = val(getattr(obj, k))
        except Exception:
            pass
    return d


def curve_map(cm):
    try:
        return [[round(p.location[0], 3), round(p.location[1], 3)] for p in cm.curves[0].points]
    except Exception:
        return None


def anim_of(idblock):
    ad = getattr(idblock, "animation_data", None)
    if not ad:
        return None
    res = {}
    act = ad.action
    if act:
        fcs = []
        try:
            fcs = list(act.fcurves)
        except Exception:
            try:  # hành động nhiều lớp (Blender 4.4+)
                for layer in act.layers:
                    for strip in layer.strips:
                        for cb in strip.channelbags:
                            fcs += list(cb.fcurves)
            except Exception:
                pass
        res["action"] = act.name
        res["fcurves"] = [dict(path=f.data_path, idx=f.array_index,
                               keys=[[round(k.co[0], 2), round(k.co[1], 4), k.interpolation] for k in f.keyframe_points][:24],
                               mods=[m.type for m in f.modifiers])
                          for f in fcs]
    if ad.drivers:
        res["drivers"] = []
        for f in ad.drivers:
            dr = f.driver
            res["drivers"].append(dict(path=f.data_path, idx=f.array_index, type=dr.type, expr=dr.expression,
                                       vars=[dict(name=v.name, type=v.type,
                                                  targets=[dict(id=val(t.id), path=t.data_path, ttype=t.transform_type,
                                                                space=t.transform_space)
                                                           for t in v.targets])
                                             for v in dr.variables]))
    return res


def node_tree(nt):
    if not nt:
        return None
    nodes = []
    for n in nt.nodes:
        nd = dict(name=n.name, type=n.bl_idname)
        ins = {}
        for s in n.inputs:
            if not s.is_linked and hasattr(s, "default_value"):
                ins[s.name] = val(s.default_value)
        nd["inputs"] = ins
        if n.bl_idname in ("ShaderNodeValToRGB", "CompositorNodeValToRGB"):
            cr = n.color_ramp
            nd["ramp"] = dict(interp=cr.interpolation,
                              els=[[round(e.position, 3), [round(c, 3) for c in e.color]] for e in cr.elements])
        for extra in ("blend_type", "operation", "noise_dimensions", "feature", "distance", "coloring", "musgrave_type"):
            if hasattr(n, extra):
                nd[extra] = getattr(n, extra)
        nodes.append(nd)
    links = [f"{l.from_node.name}.{l.from_socket.name} -> {l.to_node.name}.{l.to_socket.name}" for l in nt.links]
    return dict(nodes=nodes, links=links)


sc = bpy.context.scene
rd = sc.render
D = dict(file=bpy.data.filepath, version=list(bpy.data.version))
D["scene"] = dict(name=sc.name, frames=[sc.frame_start, sc.frame_end], fps=rd.fps, engine=rd.engine,
                  res=[rd.resolution_x, rd.resolution_y, rd.resolution_percentage],
                  film_transparent=getattr(rd, "film_transparent", None),
                  view_transform=sc.view_settings.view_transform, look=sc.view_settings.look,
                  camera=val(sc.camera), world=val(sc.world))
try:
    D["scene"]["world_color"] = val(sc.world.color)
    D["scene"]["world_nodes"] = node_tree(sc.world.node_tree) if sc.world.use_nodes else None
except Exception:
    pass
D["scene"]["anim"] = anim_of(sc)
D["objects"] = []
for ob in bpy.data.objects:
    o = dict(name=ob.name, type=ob.type, loc=val(ob.location), rot=val(ob.rotation_euler), scale=val(ob.scale),
             parent=val(ob.parent), hide_render=ob.hide_render, data=val(ob.data))
    if ob.type == "MESH":
        o["verts"] = len(ob.data.vertices)
        o["vgroups"] = [g.name for g in ob.vertex_groups]
        o["materials"] = [val(s.material) for s in ob.material_slots]
    if ob.type == "EMPTY":
        o["empty"] = [ob.empty_display_type, round(ob.empty_display_size, 3)]
    if ob.type == "CAMERA":
        o["cam"] = dict(type=ob.data.type, ortho=round(ob.data.ortho_scale, 3), lens=round(ob.data.lens, 2))
    mods = []
    for m in ob.modifiers:
        md = dict(name=m.name, type=m.type, props=props(m))
        for cm in ("map_curve",):
            if hasattr(m, cm):
                md[cm] = curve_map(getattr(m, cm))
        mods.append(md)
    o["modifiers"] = mods
    o["anim"] = anim_of(ob)
    if ob.data is not None:
        o["data_anim"] = anim_of(ob.data)
    D["objects"].append(o)
D["textures"] = []
for t in bpy.data.textures:
    td = dict(name=t.name, type=t.type, props=props(t))
    td["anim"] = anim_of(t)
    D["textures"].append(td)
D["materials"] = []
for m in bpy.data.materials:
    md = dict(name=m.name, diffuse=val(m.diffuse_color), use_nodes=m.use_nodes,
              blend=getattr(m, "blend_method", None), shadow=getattr(m, "shadow_method", None))
    if m.use_nodes:
        md["tree"] = node_tree(m.node_tree)
    md["anim"] = anim_of(m)
    D["materials"].append(md)
D["actions"] = [a.name for a in bpy.data.actions]
D["node_groups"] = [dict(name=g.name, type=g.bl_idname, tree=node_tree(g)) for g in bpy.data.node_groups]
D["texts"] = [dict(name=t.name, lines=len(t.lines)) for t in bpy.data.texts]
json.dump(D, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("OK", out_path, len(D["objects"]), "objects")
