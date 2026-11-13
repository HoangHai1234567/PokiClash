# -*- coding: utf-8 -*-
"""Tờ khung soi một .atomik bằng bộ vẽ atomik_dang (chép AtomikPose):  to_khung.py <atomik> <ra.png> clip:giây,clip:giây,... [cot=4] [o=420]"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atomik_dang as A  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

J, img, _ = A.load(sys.argv[1])
cs = [x.split(":") for x in sys.argv[3].split(",")]
cot = int(sys.argv[4]) if len(sys.argv) > 4 else 4
o = int(sys.argv[5]) if len(sys.argv) > 5 else 420
P = A.Pose(J)
bxs = []
for c, t in cs:
    P.at(A.clip(J, c), float(t))
    if P.items():
        bxs.append(A.bounds(P))
x0 = min(b[0] for b in bxs); y0 = min(b[1] for b in bxs); x1 = max(b[2] for b in bxs); y1 = max(b[3] for b in bxs)
pad = 0.04 * max(x1 - x0, y1 - y0)
box = (x0 - pad, y0 - pad, x1 + pad, y1 + pad)
sc = o / max(box[2] - box[0], box[3] - box[1])
rows = (len(cs) + cot - 1) // cot
W, H = round((box[2] - box[0]) * sc), round((box[3] - box[1]) * sc)
sheet = Image.new("RGB", (W * cot, (H + 16) * rows), (150, 150, 150))
d = ImageDraw.Draw(sheet)
for i, (c, t) in enumerate(cs):
    P.at(A.clip(J, c), float(t))
    im = A.render(J, img, P, box, sc, bg=(150, 150, 150), ss=2)
    x, y = (i % cot) * W, (i // cot) * (H + 16)
    sheet.paste(im.convert("RGB"), (x, y + 16))
    d.text((x + 4, y + 2), f"{c} {t}s", fill=(0, 0, 0))
sheet.save(sys.argv[2])
print(sys.argv[2], sheet.size)
