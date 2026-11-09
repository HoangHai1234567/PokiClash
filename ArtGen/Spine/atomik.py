# -*- coding: utf-8 -*-
"""Xuất định dạng .atomik (animation xương riêng của PokiClash, Unity nhập bằng AtomikImporter) từ JSON Spine 4.2 + atlas.

    py -3 -I ArtGen/Spine/atomik.py <skeleton.json> <file.atlas> <out.atomik> [--name tên]

File .atomik = "ATMK" + uint16 phiên bản + gzip( uint32 dài JSON + JSON utf-8 + uint32 dài PNG + PNG atlas ).
JSON viết đúng khuôn JsonUtility của Unity đọc được (không có từ điển):
  bones[]: rigName? không; mỗi xương {name, parent, x, y, rot, sx, sy, noScale}
  slots[] (thứ tự vẽ sau -> trước): {name, bone, att}  att = chỉ số trong atts, -1 = trống
  atts[]: {slot, name, uvs[] (UV Unity, gốc dưới trái), tris[], wInfo[]}
     wInfo mỗi đỉnh: n, rồi n lần (xương, x, y, trọng số); x, y theo xương đó ở tư thế gốc, đơn vị pixel, y lên.
     Mảnh cứng (region) và lưới không trọng số đều đổi về dạng này (một xương, trọng số 1).
  anims[]: {name, dur, tls[], sk[]}
     tls: {bone, type, keys[]}: type 0 xoay, sải 7 [t, v, kiểu, c1..c4]; 1 dời, 2 tỉ lệ, sải 12 [t, x, y, kiểu, 8 số]
          kiểu 0 thẳng, 1 bậc, 2 bezier (điểm điều khiển tuyệt đối như Spine 4.2: theo từng thuộc tính cx1 cy1 cx2 cy2)
     sk: {slot, times[], atts[]}  đổi hình trong slot (chớp mắt)
     sa: {slot, keys[]}  độ đậm slot (bản 2, timeline "alpha" của Spine 4.2), sải 7 như xoay
  game (bản 2, tuỳ chọn): thông tin trận khi rig là dạng tướng (AtomikGame trong Unity): fps, height, hitClips, hitTimes,
     lunge, stay, muzzle, beam, beamStyle, move, shadow. --game <tệp.json>
"""
import io
import json
import math
import os
import struct
import sys
import gzip

VERSION = 2


def read_atlas(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8")]
    page, size, regions, cur = None, None, {}, None
    for l in lines:
        if not l.strip():
            continue
        if page is None:
            page = l.strip()
            continue
        if ":" in l:
            k, v = [s.strip() for s in l.split(":", 1)]
            nums = [float(x) for x in v.replace(" ", "").split(",") if x.replace(".", "").replace("-", "").isdigit()]
            if cur is None:
                if k == "size":
                    size = nums
            elif k == "xy":
                regions[cur]["xy"] = nums
            elif k == "size":
                regions[cur]["size"] = nums
            elif k == "bounds":
                regions[cur]["xy"], regions[cur]["size"] = nums[:2], nums[2:]
            elif k == "rotate" and v not in ("false", "0"):
                sys.exit(f"atlas: vùng {cur} bị xoay, chưa hỗ trợ")
        else:
            cur = l.strip()
            regions[cur] = {}
    return page, size, regions


def bez_keys(frames, props, defaults):
    """khoá Spine 4.2 -> mảng phẳng; curve trên khoá i áp cho đoạn i -> i+1."""
    out = []
    for f in frames:
        row = [f.get("time", 0.0)] + [f.get(p, d) for p, d in zip(props, defaults)]
        c = f.get("curve")
        if c == "stepped":
            row += [1] + [0] * (4 * len(props))
        elif isinstance(c, list):
            row += [2] + list(c) + [0] * (4 * len(props) - len(c))
        else:
            row += [0] + [0] * (4 * len(props))
        out += [round(float(x), 5) for x in row]
    return out


def convert(skel_path, atlas_path, out_path, name=None, game=None):
    sk = json.load(open(skel_path, encoding="utf-8"))
    page, asize, regions = read_atlas(atlas_path)
    png_path = os.path.join(os.path.dirname(atlas_path), page)
    AW, AH = asize[:2]
    bones = []
    bi = {}
    for b in sk["bones"]:
        bi[b["name"]] = len(bones)
        bones.append({"name": b["name"], "parent": bi[b["parent"]] if "parent" in b else -1,
                      "x": b.get("x", 0.0), "y": b.get("y", 0.0), "rot": b.get("rotation", 0.0),
                      "sx": b.get("scaleX", 1.0), "sy": b.get("scaleY", 1.0),
                      "noScale": b.get("inherit", b.get("transform", "normal")) in ("noScale", "noScaleOrReflection")})
    slots = [{"name": s["name"], "bone": bi[s["bone"]], "att": -1} for s in sk["slots"]]
    si = {s["name"]: i for i, s in enumerate(slots)}
    skin = next(s for s in sk["skins"] if s["name"] == "default")["attachments"]
    atts, ai = [], {}

    def region_uv(rname, u, v):  # u, v trong vùng (0..1, v xuống) -> UV Unity của cả atlas (v lên)
        r = regions[rname]
        x, y = r["xy"]
        w, h = r["size"]
        return round((x + u * w) / AW, 6), round(1 - (y + v * h) / AH, 6)

    for sname, amap in skin.items():
        slot = si[sname]
        for aname, a in amap.items():
            typ = a.get("type", "region")
            rname = a.get("path", aname)
            uvs, tris, w = [], [], []
            if typ == "region":
                x, y, wd, ht = a.get("x", 0), a.get("y", 0), a["width"], a["height"]
                r = math.radians(a.get("rotation", 0))
                sxx, syy = a.get("scaleX", 1), a.get("scaleY", 1)
                corners = [(-wd / 2, ht / 2, 0, 0), (wd / 2, ht / 2, 1, 0), (wd / 2, -ht / 2, 1, 1), (-wd / 2, -ht / 2, 0, 1)]
                for cx, cy, u, v in corners:
                    cx, cy = cx * sxx, cy * syy
                    px = x + cx * math.cos(r) - cy * math.sin(r)
                    py = y + cx * math.sin(r) + cy * math.cos(r)
                    w += [1, slots[slot]["bone"], round(px, 3), round(py, 3), 1]
                    uvs += list(region_uv(rname, u, v))
                tris = [0, 1, 2, 2, 3, 0]
            elif typ == "mesh":
                ruv = a["uvs"]
                n = len(ruv) // 2
                for i in range(n):
                    uvs += list(region_uv(rname, ruv[2 * i], ruv[2 * i + 1]))
                tris = a["triangles"]
                vs = a["vertices"]
                if len(vs) == 2 * n:  # không trọng số: theo xương của slot
                    for i in range(n):
                        w += [1, slots[slot]["bone"], vs[2 * i], vs[2 * i + 1], 1]
                else:
                    w = list(vs)
            else:
                print(f"  bỏ qua attachment {sname}/{aname} kiểu {typ}")
                continue
            ai[(sname, aname)] = len(atts)
            atts.append({"slot": slot, "name": aname, "uvs": uvs, "tris": tris, "wInfo": w})
    for s in sk["slots"]:
        if s.get("attachment"):
            slots[si[s["name"]]]["att"] = ai[(s["name"], s["attachment"])]
    anims = []
    for an, a in sk.get("animations", {}).items():
        tls, dur = [], 0.0
        for bname, tmap in a.get("bones", {}).items():
            for kind, frames in tmap.items():
                if kind == "rotate":
                    tls.append({"bone": bi[bname], "type": 0, "keys": bez_keys(frames, ["value"], [0.0])})
                elif kind in ("translate", "scale"):
                    d = 0.0 if kind == "translate" else 1.0
                    tls.append({"bone": bi[bname], "type": 1 if kind == "translate" else 2,
                                "keys": bez_keys(frames, ["x", "y"], [d, d])})
                else:
                    print(f"  bỏ qua timeline {bname}/{kind}")
                    continue
                dur = max(dur, max(f.get("time", 0.0) for f in frames))
        skl, sal = [], []
        for sname, smap in a.get("slots", {}).items():
            fr = smap.get("attachment", [])
            if fr:
                skl.append({"slot": si[sname], "times": [f.get("time", 0.0) for f in fr],
                            "atts": [ai.get((sname, f["name"]), -1) if f.get("name") else -1 for f in fr]})
                dur = max(dur, max(f.get("time", 0.0) for f in fr))
            af = smap.get("alpha", [])
            if af:
                sal.append({"slot": si[sname], "keys": bez_keys(af, ["value"], [1.0])})
                dur = max(dur, max(f.get("time", 0.0) for f in af))
            for kind in smap:
                if kind not in ("attachment", "alpha"):
                    print(f"  bỏ qua timeline slot {sname}/{kind}")
        anims.append({"name": an, "dur": round(dur, 5), "tls": tls, "sk": skl, "sa": sal})
    data = {"rigName": name or os.path.splitext(os.path.basename(out_path))[0], "version": VERSION, "ppu": 100.0,
            "bones": bones, "slots": slots, "atts": atts, "anims": anims}
    if game:
        data["game"] = game
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    png = open(png_path, "rb").read()
    body = io.BytesIO()
    body.write(struct.pack("<I", len(js)))
    body.write(js)
    body.write(struct.pack("<I", len(png)))
    body.write(png)
    with open(out_path, "wb") as f:
        f.write(b"ATMK" + struct.pack("<H", VERSION))
        f.write(gzip.compress(body.getvalue(), 9))
    nv = sum(len(a["uvs"]) // 2 for a in atts)
    print(f"{out_path}: {len(bones)} xương, {len(slots)} slot, {len(atts)} hình, {nv} đỉnh, "
          f"{len(anims)} animation, {os.path.getsize(out_path) // 1024} KB (JSON {len(js) // 1024} KB, PNG {len(png) // 1024} KB)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    nm, gm = None, None
    if "--name" in a:
        i = a.index("--name")
        nm = a[i + 1]
        del a[i:i + 2]
    if "--game" in a:
        i = a.index("--game")
        gm = json.load(open(a[i + 1], encoding="utf-8"))
        del a[i:i + 2]
    convert(a[0], a[1], a[2], nm, gm)
