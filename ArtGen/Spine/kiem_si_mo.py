# -*- coding: utf-8 -*-
"""Kiếm sĩ rừng: tờ MỔ từng part của con gốc monster_3620 ở một dáng (mặc định khung 0 idle): mỗi ô = cả con mờ + MỘT part tô đậm có viền
đỏ, ghi thứ tự vẽ, slot, xương bám (trọng số), cỡ ảnh vùng. Chỉ để xem nội bộ (hình của nhà phát hành game gốc).

    kiem_si_mo.py [att json] [tên ra]     → <SXS>/scan/monster_3620/mo/<tên>_<k>.jpg (mỗi tờ 20 ô) + in bảng
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
from quai.soi import _tris  # noqa: E402
import kiem_si as KS  # noqa: E402

F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)


def main(att="att_idle0.json", ten="idle0", S=0.42, cot=5, hang=4):
    KS.ATT = att
    KS._C.clear()
    atlas, imgs, atts = KS.nap()
    D = json.load(open(os.path.join(KS.scan(), att), encoding="utf-8"))
    bn = [b["name"] for b in D["bones"]]
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min() - 20, P[:, 1].min() - 20, P[:, 0].max() + 20, P[:, 1].max() + 20
    cw, ch = int((x1 - x0) * S), int((y1 - y0) * S)
    T = lambda V: np.stack([(V[:, 0] - x0) * S, (y1 - V[:, 1]) * S], 1)   # noqa: E731

    def lop(a):
        im = imgs[a["region"]]
        uv, tr = KS.luoi(a)
        lay = Image.new("RGBa", (cw, ch), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
        return lay.convert("RGBA")

    lops = [lop(a) for a in atts]
    ca = Image.new("RGBA", (cw, ch), (120, 125, 140, 255))
    for l_ in lops:
        ca.alpha_composite(l_)
    mo = Image.blend(Image.new("RGBA", (cw, ch), (120, 125, 140, 255)), ca, 0.28)
    ra = os.path.join(KS.scan(), "mo")
    os.makedirs(ra, exist_ok=True)
    n = cot * hang
    for k in range(0, len(atts), n):
        to = Image.new("RGB", (cw * cot, (ch + 44) * hang), (60, 62, 70))
        d = ImageDraw.Draw(to)
        for j, a in enumerate(atts[k:k + n]):
            o = mo.copy()
            o.alpha_composite(lops[k + j])
            al = np.asarray(lops[k + j])[..., 3] > 60
            vien = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1))
            arr = np.asarray(o).copy()
            arr[vien] = (255, 60, 60, 255)
            x, y = (j % cot) * cw, (j // cot) * (ch + 44)
            to.paste(Image.fromarray(arr, "RGBA").convert("RGB"), (x, y + 44))
            w = a.get("w")
            if w:
                bs = {}
                for v in w:
                    for b, ww in v:
                        bs[bn[b]] = bs.get(bn[b], 0) + ww
                xb = " ".join(f"{b}:{v / len(w):.2f}" for b, v in sorted(bs.items(), key=lambda q: -q[1]))
            else:
                xb = a["bone"]
            im = imgs[a["region"]]
            d.text((x + 4, y + 2), f"{a['order']} {a['slot']}  ({im.width}×{im.height})", fill=(255, 255, 255), font=F)
            d.text((x + 4, y + 22), xb[:70], fill=(255, 220, 120), font=F)
        p = os.path.join(ra, f"{ten}_{k // n}.jpg")
        to.save(p, quality=88)
        print(p, to.size)


if __name__ == "__main__":
    main(*sys.argv[1:3])
