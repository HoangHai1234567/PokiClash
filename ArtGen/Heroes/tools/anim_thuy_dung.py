"""So clip đứng: bản gốc aola (hàng trên) với bản viết lại của anim_thuy.py (hàng dưới), mỗi dạng 6 khung.

    py -3 ArtGen/Heroes/tools/anim_thuy_dung.py <ảnh ra.png> <dạng> [...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw  # noqa: E402

import anim_thuy as m  # noqa: E402
from anim_thuy_choreo import CHOREO  # noqa: E402


def goc_render(pid, fi, view, scale):
    root = os.path.join(m.AOLA_DIR, "reskin", f"goc_{pid}")
    d = json.load(open(os.path.join(root, "export", "anim.json"), encoding="utf-8"))
    fr = d["clips"]["1_1"]["frames"]
    rows = fr[fi % len(fr)]
    x0, y0, x1, y1 = view
    W, H = int((x1 - x0) * scale), int((y1 - y0) * scale)
    out = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    for r in rows:
        p = os.path.normpath(os.path.join(root, d["sprites"][r[0]]))
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        a, b, c, dd, tx, ty = r[1:7]
        A, B, C, D = a * scale, b * scale, c * scale, dd * scale
        TX, TY = (tx - x0) * scale, (ty - y0) * scale
        det = A * D - B * C
        if abs(det) < 1e-9:
            continue
        ia, ib, ic, idd = D / det, -C / det, -B / det, A / det
        L = im.transform((W, H), Image.AFFINE, (ia, ib, -(ia * TX + ib * TY), ic, idd, -(ic * TX + idd * TY)), resample=Image.BILINEAR)
        out.alpha_composite(L)
    return out, len(fr)


def rows_for(form, scale=0.6):
    a = m.Anim(form)
    CHOREO[form](a)
    a.finish()
    a.pack()
    r = a.rig
    bx = r.body
    pad = 0.15 * r.H
    view = (bx[0] - pad, bx[1] - pad, bx[2] + pad, r.foot[1] + 0.1 * r.H)
    k = 170 / (view[3] - view[1])
    idle = a.anim_out["clips"]["1_1"]["frames"]
    pid = int(form.split("_")[1])
    top, bot = [], []
    _, ng = goc_render(pid, 0, view, k)
    for i in range(6):
        top.append(goc_render(pid, int(i * ng / 6), view, k)[0])
        bot.append(m.render(a, idle[int(i * len(idle) / 6)], view, k))
    return form, top, bot


if __name__ == "__main__":
    out = sys.argv[1]
    data = [rows_for(f) for f in sys.argv[2:]]
    tw = max(t.width for _, top, _ in data for t in top)
    th = max(t.height for _, top, _ in data for t in top)
    S = Image.new("RGB", (70 + 6 * tw, len(data) * 2 * th), "white")
    d = ImageDraw.Draw(S)
    for j, (form, top, bot) in enumerate(data):
        y = j * 2 * th
        d.text((2, y + 4), form + " goc", fill=(0, 0, 0))
        d.text((2, y + th + 4), "moi", fill=(160, 0, 0))
        for i in range(6):
            S.paste(top[i].convert("RGB"), (70 + i * tw, y))
            S.paste(bot[i].convert("RGB"), (70 + i * tw, y + th))
        d.line([(0, y + 2 * th - 1), (S.width, y + 2 * th - 1)], fill=(150, 150, 150))
    S.save(out)
    print(out)
