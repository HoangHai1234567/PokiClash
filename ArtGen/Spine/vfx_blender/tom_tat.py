# -*- coding: utf-8 -*-
"""Tóm tắt JSON do doc_blend.py ghi thành chữ gọn: py -3 -I tom_tat.py <tên trong doc/ | đường dẫn .json> [...]"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = {
    "VERTEX_WEIGHT_EDIT": ["vertex_group", "default_weight", "use_add", "add_threshold", "use_remove", "remove_threshold",
                           "falloff_type", "invert_falloff", "mask_constant", "mask_texture", "mask_tex_use_channel",
                           "mask_tex_mapping", "mask_tex_map_object", "mask_vertex_group", "normalize"],
    "VERTEX_WEIGHT_MIX": ["vertex_group_a", "vertex_group_b", "default_weight_a", "default_weight_b", "mix_mode",
                          "mix_set", "mask_constant", "mask_texture", "normalize"],
    "VERTEX_WEIGHT_PROXIMITY": ["vertex_group", "target", "proximity_mode", "min_dist", "max_dist", "falloff_type",
                                "mask_constant", "mask_texture"],
    "DISPLACE": ["strength", "mid_level", "direction", "space", "vertex_group", "texture", "texture_coords",
                 "texture_coords_object"],
    "MASK": ["mode", "vertex_group", "invert_vertex_group", "threshold"],
    "SMOOTH": ["factor", "iterations", "vertex_group", "use_x", "use_y", "use_z"],
    "SUBSURF": ["levels", "render_levels"],
    "ARRAY": ["count", "relative_offset_displace", "use_object_offset", "offset_object", "fit_type"],
    "SIMPLE_DEFORM": ["deform_method", "angle", "factor", "deform_axis", "origin", "limits", "vertex_group"],
    "CURVE": ["object", "deform_axis", "vertex_group"],
    "SOLIDIFY": ["thickness", "offset", "use_flip_normals", "use_rim"],
    "WAVE": ["height", "width", "speed", "narrowness", "time_offset", "use_x", "use_y", "vertex_group", "texture"],
    "CAST": ["cast_type", "factor", "radius", "use_x", "use_y", "use_z", "vertex_group"],
    "SCREW": ["angle", "screw_offset", "steps", "axis", "object", "iterations"],
    "LATTICE": ["object", "vertex_group", "strength"],
    "HOOK": ["object", "strength", "falloff_type", "falloff_radius"],
    "WARP": ["object_from", "object_to", "strength", "falloff_type", "falloff_radius", "texture"],
    "DECIMATE": ["decimate_type", "ratio"],
    "MIRROR": ["use_axis"],
    "BEVEL": ["width", "segments"],
    "EDGE_SPLIT": ["split_angle"],
    "TRIANGULATE": [],
    "PARTICLE_SYSTEM": [],
}
TEXK = ["noise_scale", "noise_basis", "noise_type", "noise_depth", "distance_metric", "color_mode", "intensity", "contrast",
        "use_color_ramp", "turbulence", "marble_type", "wood_type", "progression", "musgrave_type", "nabla",
        "minkovsky_exponent", "weight_1", "weight_2", "weight_3", "weight_4", "noise_intensity"]


def short(v):
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, list):
        return "(" + ",".join(short(x) for x in v[:4]) + ")"
    return str(v)


def anim_txt(a, ind="      "):
    if not a:
        return []
    out = []
    for f in a.get("fcurves", []):
        ks = f["keys"]
        if not ks:
            continue
        rng = f"f{ks[0][0]:g}->{ks[-1][0]:g}"
        vals = " ".join(f"{k[0]:g}:{k[1]:g}" for k in ks[:8])
        out.append(f"{ind}~ {f['path']}[{f['idx']}] {len(ks)}k {rng} [{vals}] {ks[0][2]}{' mods=' + ','.join(f['mods']) if f['mods'] else ''}")
    for d in a.get("drivers", []):
        vs = "; ".join(f"{v['name']}={v['targets'][0]['id']}.{v['targets'][0]['ttype'] or v['targets'][0]['path']}"
                       for v in d["vars"] if v["targets"])
        out.append(f"{ind}= driver {d['path']}[{d['idx']}] {d['type']} '{d['expr']}' {vs}")
    return out


def summarize(name):
    path = name if name.endswith(".json") else os.path.join(HERE, "doc", name + ".json")
    name = os.path.splitext(os.path.basename(path))[0]
    D = json.load(open(path, encoding="utf-8"))
    s = D["scene"]
    print(f"# {name}  (blender {D['version']})")
    print(f"scene frames {s['frames']} fps {s['fps']} engine {s['engine']} res {s['res']} transparent {s['film_transparent']}"
          f" view {s['view_transform']}/{s['look']} cam {s['camera']} world {s.get('world_color')}")
    for l in anim_txt(s.get("anim"), "  "):
        print(l)
    for o in D["objects"]:
        head = f"- {o['name']} [{o['type']}] loc{short(o['loc'])} rot{short(o['rot'])} scl{short(o['scale'])}"
        if o.get("parent"):
            head += f" parent={o['parent']}"
        if o.get("hide_render"):
            head += " HIDE_RENDER"
        if o["type"] == "MESH":
            head += f" v={o['verts']} vg={o['vgroups']} mat={o['materials']}"
        if o.get("cam"):
            head += f" cam={o['cam']}"
        print(head)
        for m in o["modifiers"]:
            keys = KEYS.get(m["type"])
            p = m["props"]
            if keys is None:
                kv = {k: v for k, v in p.items() if not k.startswith("show_") and k not in ("is_override_data", "persistent_uid")}
                kv = dict(list(kv.items())[:10])
            else:
                kv = {k: p[k] for k in keys if k in p}
            kv = {k: v for k, v in kv.items() if v not in ("", None)}
            txt = " ".join(f"{k}={short(v)}" for k, v in kv.items())
            extra = f" curve={m['map_curve']}" if m.get("map_curve") and kv.get("falloff_type") == "CURVE" else ""
            print(f"    · {m['type']} '{m['name']}' {txt}{extra}")
        for l in anim_txt(o.get("anim")) + anim_txt(o.get("data_anim")):
            print(l)
    for t in D["textures"]:
        p = t["props"]
        kv = " ".join(f"{k}={short(p[k])}" for k in TEXK if k in p)
        print(f"  TEX {t['name']} {t['type']} {kv}")
        for l in anim_txt(t.get("anim"), "      "):
            print(l)
    for m in D["materials"]:
        line = f"  MAT {m['name']} diffuse={short(m['diffuse'])} blend={m.get('blend')}"
        print(line)
        tr = m.get("tree")
        if tr:
            for n in tr["nodes"]:
                if n["type"] in ("NodeFrame", "NodeReroute"):
                    continue
                ins = {k: v for k, v in n["inputs"].items() if k in ("Color", "Strength", "Base Color", "Emission",
                                                                      "Emission Color", "Emission Strength", "Fac",
                                                                      "Alpha", "Scale", "Value")}
                r = f" ramp={n['ramp']}" if n.get("ramp") else ""
                print(f"      node {n['type']} {short(ins) if ins else ''}{r}")
            for l in tr["links"]:
                print(f"      link {l}")
        for l in anim_txt(m.get("anim"), "      "):
            print(l)
    if D.get("texts"):
        print("  TEXTS", D["texts"])
    print()


for n in sys.argv[1:]:
    summarize(n)
