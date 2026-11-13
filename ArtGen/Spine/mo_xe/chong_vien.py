# -*- coding: utf-8 -*-
"""Vẽ viền lưới các slot (lọc theo tiền tố) của rig đã đổi tỉ lệ lên ảnh concept, để chọn cách cắt.
    chong_vien.py <atomik> <ti_le.json> <concept.png> <khung x0,y0,x1,y1> <tiền tố,...> <ra.png> [crop x0,y0,x1,y1]"""
import json
import os
import sys
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atomik_dang as A  # noqa: E402

J, img, _ = A.load(sys.argv[1])
A.scale_bones(J, json.load(open(sys.argv[2], encoding="utf-8")))
P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
im = Image.open(sys.argv[3]).convert("RGB")
to_rig, to_px, z = A.canvas_map([float(v) for v in sys.argv[4].split(",")], im.width, im.height)
d = ImageDraw.Draw(im)
pre = sys.argv[5].split(",")
pal = [(255, 0, 0), (0, 0, 255), (255, 0, 255), (0, 150, 0), (255, 130, 0), (0, 190, 190), (120, 60, 0), (90, 0, 160)]
S = J["slots"]
for s, a, V, al in P.items():
    nm = S[s]["name"]
    hit = [i for i, p in enumerate(pre) if nm.startswith(p)]
    if not hit:
        continue
    c = pal[hit[0] % len(pal)]
    p = to_px(V)
    tr = np.array(J["atts"][a]["tris"]).reshape(-1, 3)
    E = Counter(tuple(sorted((t[i], t[(i + 1) % 3]))) for t in tr for i in range(3))
    for (i, j), n in E.items():
        if n == 1:
            d.line([tuple(p[i]), tuple(p[j])], fill=c, width=2)
    d.text(tuple(p.mean(0)), nm, fill=c)
for x in range(0, im.width, 50):
    d.line([(x, 0), (x, 6 if x % 100 else 12)], fill=(0, 0, 0))
    if x % 100 == 0:
        d.text((x + 2, 12), str(x), fill=(0, 0, 0))
for y in range(0, im.height, 50):
    d.line([(0, y), (6 if y % 100 else 12, y)], fill=(0, 0, 0))
    if y % 100 == 0:
        d.text((14, y + 2), str(y), fill=(0, 0, 0))
if len(sys.argv) > 7:
    im = im.crop(tuple(int(v) for v in sys.argv[7].split(",")))
im.save(sys.argv[6])
