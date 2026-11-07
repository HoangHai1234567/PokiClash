"""Tờ khung clip của dạng đã nhập (soi animation không cần Unity).

    py -3 -I ArtGen/Heroes/tools/anim_sheet.py <dạng> <ảnh ra.png> [--clips 1_4,1_6] [--step 2] [--rev <commit>] [--far]

--far: kéo hình ở xa về chỗ đối thủ giả định (cách chân 1,5 lần chiều cao, cao ngang giữa thân) như trận.
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aola_form import Form  # noqa: E402


def idle_info(f):
    rows = f.clips["1_1"]["frames"][0]
    bs = [f.bbox(r) for r in rows if r[0] != f.shadow]
    x0, y0 = min(b[0] for b in bs), min(b[1] for b in bs)
    x1, y1 = max(b[2] for b in bs), max(b[3] for b in bs)
    sh = [r for r in rows if r[0] == f.shadow]
    if sh:
        b = f.bbox(sh[0])
        foot = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
    else:
        foot = ((x0 + x1) / 2, y1)
    return dict(x0=x0, y0=y0, x1=x1, y1=y1, H=y1 - y0, foot=foot)


def far_rows(f, clip, rows, target):
    """như AolaActor.Render: hình không có trong dáng đứng, tâm xa hơn FarRamp·H về trước, kéo dần về target"""
    g = idle_info(f)
    H = g["H"]
    idle = {r[0] for fr in f.clips["1_1"]["frames"] for r in fr}
    c = f.clips[clip]
    fc = f.anim.get("far_center", {}).get(clip)
    anchor = g["foot"]
    if fc is None:
        xs = []
        for fr in c["frames"]:
            for r in fr:
                if r[0] in idle:
                    continue
                b = f.bbox(r)
                cx = (b[0] + b[2]) / 2 - anchor[0]
                if cx > 1.5 * H:
                    xs.append((cx, (b[1] + b[3]) / 2 - anchor[1]))
        if not xs:
            return rows
        fcx = (min(x for x, _ in xs) + max(x for x, _ in xs)) / 2
        fcy = (min(y for _, y in xs) + max(y for _, y in xs)) / 2
    else:
        fcx, fcy = fc[0] - anchor[0], fc[1] - anchor[1]
    out = []
    r0 = 1.0 * H
    for r in rows:
        if r[0] in idle:
            out.append(r)
            continue
        b = f.bbox(r)
        d = (b[0] + b[2]) / 2 - anchor[0]
        if d > r0 and fcx > r0:
            w = min(1, max(0, (d - r0) / (fcx - r0)))
            sx, sy = w * (target[0] * H - fcx), w * (target[1] * H - fcy)
            r = list(r)
            r[5] += sx
            r[6] += sy
        out.append(r)
    return out


def sheet(form, out, clips=("1_4", "1_5", "1_6"), step=2, rev=None, far=None, cols=12, scale=0.9):
    f = Form(form, rev)
    g = idle_info(f)
    H = g["H"]
    fx, fy = g["foot"]
    view = (fx - 1.0 * H, fy - 2.6 * H, fx + 2.6 * H, fy + 0.5 * H)
    tiles = []
    for c in clips:
        if c not in f.clips:
            continue
        fr = f.clips[c]["frames"]
        for i in range(0, len(fr), step):
            rows = fr[i]
            if far is not None:
                rows = far_rows(f, c, rows, far)
            im = f.render(rows, view=view, scale=scale)
            tiles.append((f"{c}:{i}", im))
    tw, th = tiles[0][1].size
    rows_n = (len(tiles) + cols - 1) // cols
    S = Image.new("RGB", (cols * tw, rows_n * (th + 16)), "white")
    d = ImageDraw.Draw(S)
    for k, (lab, im) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * (th + 16)
        S.paste(im.convert("RGB"), (x, y + 16))
        d.text((x + 3, y + 2), lab, fill="black")
        d.line([(x, y), (x, y + th + 16)], fill=(200, 200, 200))
    S.save(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("form")
    ap.add_argument("out")
    ap.add_argument("--clips", default="1_4,1_5,1_6")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--rev")
    ap.add_argument("--far", action="store_true")
    ap.add_argument("--cols", type=int, default=12)
    ap.add_argument("--scale", type=float, default=0.9)
    a = ap.parse_args()
    sheet(a.form, a.out, a.clips.split(","), a.step, a.rev, (1.5, -0.45) if a.far else None, a.cols, a.scale)
