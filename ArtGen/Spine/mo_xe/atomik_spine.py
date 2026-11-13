# -*- coding: utf-8 -*-
"""convert(path) -> (spine_json dict, atlas text, png bytes, atomik json). Tách từ atomik_xem.py."""
import gzip
import json
import struct


def convert(SRC):
    b = open(SRC, "rb").read()
    assert b[:4] == b"ATMK", "không phải .atomik"
    ver = struct.unpack("<H", b[4:6])[0]
    d = gzip.decompress(b[6:])
    n = struct.unpack("<I", d[:4])[0]
    J = json.loads(d[4:4 + n].decode("utf-8"))
    m = struct.unpack("<I", d[4 + n:8 + n])[0]
    png = d[8 + n:8 + n + m]
    W, H = struct.unpack(">II", png[16:24])
    name = J.get("rigName") or os.path.splitext(os.path.basename(SRC))[0]

    bones = J["bones"]
    bone_names = [bn["name"] for bn in bones]
    slots = J["slots"]
    atts = J["atts"]

    sk = {"skeleton": {"spine": "4.2.00", "hash": name, "x": 0, "y": 0, "width": 0, "height": 0}, "bones": [], "slots": [],
          "skins": [{"name": "default", "attachments": {}}], "animations": {}}
    for bn in bones:
        o = {"name": bn["name"]}
        if bn["parent"] >= 0:
            o["parent"] = bone_names[bn["parent"]]
        for k, kk, dv in (("x", "x", 0), ("y", "y", 0), ("rot", "rotation", 0), ("sx", "scaleX", 1), ("sy", "scaleY", 1)):
            if abs(bn.get(k, dv) - dv) > 1e-9:
                o[kk] = bn[k]
        if bn.get("noScale"):
            o["inherit"] = "noScale"
        sk["bones"].append(o)

    # mặt nạ cắt: thêm slot clipping ngay trước slot đầu khoảng
    masks = J.get("masks") or []
    mask_at = {mk["slot"]: mk for mk in masks}
    slot_names = [s["name"] for s in slots]
    att_name = {}  # chỉ số att -> tên trong skin
    skin = sk["skins"][0]["attachments"]
    for i, a in enumerate(atts):
        att_name[i] = a["name"]
    for si, s in enumerate(slots):
        if si in mask_at:
            mk = mask_at[si]
            cn = f"__clip_{si}"
            sk["slots"].append({"name": cn, "bone": bone_names[mk["bone"]], "attachment": cn})
            skin[cn] = {cn: {"type": "clipping", "end": slot_names[mk["end"]], "vertexCount": len(mk["verts"]) // 2,
                             "vertices": mk["verts"]}}
        o = {"name": s["name"], "bone": bone_names[s["bone"]]}
        if s.get("att", -1) >= 0:
            o["attachment"] = atts[s["att"]]["name"]
        fade = s.get("fade", 0.0) or 0.0
        if fade > 0:
            o["color"] = "ffffff%02x" % round(255 * (1 - min(1, fade)))
        sk["slots"].append(o)
    for i, a in enumerate(atts):
        sn = slot_names[a["slot"]]
        uv = a["uvs"]
        uvs = []
        for j in range(0, len(uv), 2):
            uvs += [round(uv[j], 6), round(1 - uv[j + 1], 6)]
        skin.setdefault(sn, {})[a["name"]] = {"type": "mesh", "path": "all", "uvs": uvs, "triangles": a["tris"],
                                              "vertices": a["wInfo"], "hull": 0, "width": 0, "height": 0}


    def curve1(k, o, S):
        kind = int(k[o + 2]) if S == 7 else int(k[o + 3])
        if kind == 1:
            return "stepped"
        if kind == 2:
            return k[o + 3:o + 7] if S == 7 else k[o + 4:o + 12]
        return None


    for an in J["anims"]:
        A = {}
        for tl in an.get("tls") or []:
            k = tl["keys"]
            S = 7 if tl["type"] == 0 else 12
            arr = []
            for o in range(0, len(k), S):
                e = {"time": k[o]}
                if tl["type"] == 0:
                    e["value"] = k[o + 1]
                else:
                    e["x"], e["y"] = k[o + 1], k[o + 2]
                c = curve1(k, o, S)
                if c is not None and o + S < len(k):
                    e["curve"] = c
                arr.append(e)
            kind = ("rotate", "translate", "scale")[tl["type"]]
            A.setdefault("bones", {}).setdefault(bone_names[tl["bone"]], {})[kind] = arr
        for s in an.get("sk") or []:
            arr = [{"time": t, "name": (atts[ai]["name"] if ai >= 0 else None)} for t, ai in zip(s["times"], s["atts"])]
            A.setdefault("slots", {}).setdefault(slot_names[s["slot"]], {})["attachment"] = arr
        for s in an.get("sa") or []:
            k = s["keys"]
            arr = []
            for o in range(0, len(k), 7):
                e = {"time": k[o], "value": max(0.0, min(1.0, k[o + 1]))}
                c = curve1(k, o, 7)
                if c is not None and o + 7 < len(k):
                    e["curve"] = c
                arr.append(e)
            A.setdefault("slots", {}).setdefault(slot_names[s["slot"]], {})["alpha"] = arr
        evs = an.get("ev") or []
        if evs:
            A["events"] = [{"time": e["t"], "name": e["name"], **({"string": e["s"]} if e.get("s") else {})} for e in evs]
            for e in evs:
                sk.setdefault("events", {})[e["name"]] = {}
        # giữ đúng thời lượng clip: thêm khoá rỗng ở cuối bằng một timeline xoay của root
        A.setdefault("bones", {}).setdefault("root", {}).setdefault("rotate", [{"time": 0, "value": 0}])
        rr = A["bones"]["root"]["rotate"]
        if rr[-1]["time"] < an["dur"] - 1e-4:
            if bones[0].get("name") == "root" and len(rr) == 1 and rr[0].get("value", 0) == 0:
                rr.append({"time": an["dur"], "value": 0})
        A["__dur"] = an["dur"]
        sk["animations"][an["name"]] = A
    for A in sk["animations"].values():
        A.pop("__dur", None)

    atlas = name + ".png\nsize: %d,%d\nfilter: Linear,Linear\nall\nbounds: 0,0,%d,%d\n" % (W, H, W, H)
    return sk, atlas, png, J
