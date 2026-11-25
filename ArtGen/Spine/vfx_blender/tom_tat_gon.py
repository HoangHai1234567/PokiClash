# -*- coding: utf-8 -*-
"""Tóm tắt GỌN JSON của doc_blend.py cho file nhiều object: chuỗi modifier trùng nhau chỉ in một lần, kèm driver, keyframe,
texture, vật liệu (node + ramp + màu Emission).   py -3 -I tom_tat_gon.py <file.json> [...]"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
SHOW = {"DISPLACE": ["strength", "direction", "vertex_group", "texture", "texture_coords", "texture_coords_object"],
        "SIMPLE_DEFORM": ["deform_method", "angle", "factor", "deform_axis", "origin"], "CURVE": ["object", "deform_axis"],
        "ARRAY": ["count", "relative_offset_displace", "use_object_offset", "offset_object", "fit_type", "curve"],
        "SCREW": ["angle", "screw_offset", "steps", "axis", "iterations"], "WAVE": ["height", "width", "speed"],
        "CAST": ["factor"], "SUBSURF": ["levels"], "SMOOTH": ["iterations"], "SOLIDIFY": ["thickness"],
        "LATTICE": ["object"], "HOOK": ["object"], "WARP": ["object_from", "object_to", "strength"],
        "VERTEX_WEIGHT_EDIT": ["vertex_group", "remove_threshold", "use_remove", "mask_texture", "mask_tex_map_object",
                               "mask_constant", "falloff_type"],
        "VERTEX_WEIGHT_MIX": ["vertex_group_a", "vertex_group_b", "mix_mode", "mask_constant"],
        "VERTEX_WEIGHT_PROXIMITY": ["target", "proximity_mode", "min_dist", "max_dist"],
        "MASK": ["vertex_group", "invert_vertex_group", "threshold"], "DECIMATE": ["ratio"],
        "PARTICLE_SYSTEM": [], "NODES": ["node_group"], "SURFACE_DEFORM": ["target"], "SHRINKWRAP": ["target"],
        "BOOLEAN": ["object", "operation"], "REMESH": ["mode", "octree_depth", "voxel_size"]}


def s(v):
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, list):
        return "(" + ",".join(s(x) for x in v[:3]) + ")"
    return str(v).replace("<Object:", "@").replace("Texture:", "T:").replace(">", "").replace("<", "")


def main(path):
    D = json.load(open(path, encoding="utf-8"))
    sc = D["scene"]
    print(f"\n# {os.path.basename(path)} frames {sc['frames']} fps {sc['fps']} {sc['engine']} {sc['view_transform']} "
          f"res {sc['res'][:2]} transp {sc['film_transparent']} cam {sc['camera']}")
    sigs = {}
    for o in D["objects"]:
        mods = []
        for m in o["modifiers"]:
            p = m["props"]
            kv = ",".join(f"{k}={s(p[k])}" for k in SHOW.get(m["type"], []) if k in p and p[k] not in ("", None))
            mods.append(f"{m['type']}({kv})")
        sig = " > ".join(mods)
        an = o.get("anim") or {}
        drv = [f"{d['path']}='{d['expr']}'<-{s(d['vars'][0]['targets'][0]['id'])}.{d['vars'][0]['targets'][0]['ttype']}"
               for d in an.get("drivers", []) if d["vars"] and d["vars"][0]["targets"]]
        fc = [f"{f['path']}[{f['idx']}] {len(f['keys'])}k f{f['keys'][0][0]:g}-{f['keys'][-1][0]:g}: "
              f"{s(f['keys'][0][1])}->{s(f['keys'][-1][1])}{' ' + ','.join(f['mods']) if f['mods'] else ''}"
              for f in an.get("fcurves", []) if f["keys"]]
        head = f"- {o['name']} [{o['type']}]"
        if o["type"] == "MESH":
            head += f" v={o.get('verts')} mat={','.join(s(x) for x in o.get('materials', []))}"
        head += f" loc{s(o['loc'])} rot{s(o['rot'])} scl{s(o['scale'])}"
        if o.get("parent"):
            head += f" parent={s(o['parent'])}"
        if o.get("hide_render"):
            head += " HIDE"
        print(head)
        if sig:
            print("    mods = same as " + sigs[sig] if sig in sigs else "    mods: " + sig)
            sigs.setdefault(sig, o["name"])
        for d in drv[:6]:
            print("    drv", d)
        for a in fc[:6]:
            print("    anim", a)
    for t in D["textures"]:
        p = t["props"]
        print(f"  TEX {t['name']} {t['type']} scale={s(p.get('noise_scale'))} basis={p.get('noise_basis')} "
              f"{p.get('distance_metric', '')} contrast={s(p.get('contrast'))}")
        for f in (t.get("anim") or {}).get("fcurves", []):
            print(f"      anim {f['path']} {f['keys'][0][1]}->{f['keys'][-1][1]}")
    for m in D["materials"]:
        tr = m.get("tree") or {}
        ns = [n["type"].replace("ShaderNode", "") for n in tr.get("nodes", []) if n["type"] != "ShaderNodeOutputMaterial"]
        em = [s(n["inputs"].get("Color")) for n in tr.get("nodes", []) if n["type"] == "ShaderNodeEmission"]
        rp = [n["ramp"]["els"] for n in tr.get("nodes", []) if n.get("ramp")]
        print(f"  MAT {m['name']} diffuse={s(m['diffuse'])} nodes={ns} emis={em}" + (f" ramp={rp}" if rp else ""))
        for l in tr.get("links", [])[:8]:
            print(f"      link {l}")
    for g in D.get("node_groups", []):
        print(f"  NODEGROUP {g['name']} {g['type']} nodes={[n['type'] for n in (g['tree'] or {}).get('nodes', [])][:20]}")


for a in sys.argv[1:]:
    main(a)
