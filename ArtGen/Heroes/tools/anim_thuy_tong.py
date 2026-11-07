"""Tờ tổng soi nhanh tools/anim_thuy.py: mỗi dạng một hàng, khung then chốt của đòn đánh và chiêu cuối quanh khung trúng.

    py -3 ArtGen/Heroes/tools/anim_thuy_tong.py <ảnh ra.png> [dạng ...]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw  # noqa: E402

import anim_thuy as m  # noqa: E402
from anim_thuy_choreo import CHOREO  # noqa: E402


def row(form, scale=0.42, enemy=(1.4, 1.4)):
    a = m.Anim(form)
    CHOREO[form](a)
    a.finish()
    a.pack()
    a.rep = a.report()
    r = a.rig
    H = r.H
    fx0, fy0 = r.foot
    view = (fx0 - 0.9 * H, fy0 - 3.25 * H, fx0 + 2.7 * H, fy0 + 0.35 * H)
    k = 300 / H * scale  # mọi dạng cùng cỡ trên tờ
    tiles = []
    for c in ("1_4", "1_6"):
        fr = a.anim_out["clips"][c]["frames"]
        hit = a.rep[c]["hit"]
        picks = [6, hit - 6, hit - 2, hit, hit + 4] if c == "1_4" else [8, hit - 12, hit - 6, hit - 2, hit, hit + 5]
        far = c in a.anim_out.get("far_center", {})
        for i in picks:
            i = max(0, min(len(fr) - 1, i))
            rows = m.pull_far(a, c, fr[i], enemy) if far else fr[i]
            box = None
            if far:
                tx, ty = fx0 + enemy[0] * H, fy0 - enemy[1] * H
                box = (tx - 0.3 * H, ty - 0.45 * H, tx + 0.3 * H, ty + 0.45 * H)
            tiles.append((f"{c}:{i}" + ("*" if i == hit else ""), m.render(a, rows, view, k, box)))
    tw, th = tiles[0][1].size
    out = Image.new("RGB", (tw * len(tiles), th + 14), "white")
    d = ImageDraw.Draw(out)
    for j, (lab, im) in enumerate(tiles):
        out.paste(im.convert("RGB"), (j * tw, 14))
        d.text((j * tw + 3, 1), (form + " " if j == 0 else "") + lab, fill=(200, 0, 0) if "*" in lab else (0, 0, 0))
        d.line([(j * tw, 0), (j * tw, th + 14)], fill=(200, 200, 200))
    return out


if __name__ == "__main__":
    out = sys.argv[1]
    forms = sys.argv[2:] or list(CHOREO)
    rows = [row(f) for f in forms]
    W = max(r.width for r in rows)
    S = Image.new("RGB", (W, sum(r.height for r in rows)), "white")
    y = 0
    for r in rows:
        S.paste(r, (0, y))
        y += r.height
    S.save(out)
    print(out)
