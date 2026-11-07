"""Dáng nghỉ của các dạng đã nhập, ghi số mảnh (idle_parts) và cây khớp (anim_moi.parent) lên hình.

    py -3 -I ArtGen/Heroes/tools/rig_sheet.py <ảnh ra.png> <dạng> [<dạng> ...] [--rev <commit>]
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aola_form import Form  # noqa: E402


def piece_rows(f):
    """số mảnh -> chỉ số hàng ở khung đầu clip đứng (idle_parts theo thứ tự vẽ; mảnh 'top' mọi khung nằm cuối)"""
    rows = f.clips["1_1"]["frames"][0]
    ip = f.anim["idle_parts"]
    return {p: i for i, p in enumerate(ip)} if len(ip) == len(rows) else None


def draw(f, scale=1.6):
    rows = f.clips["1_1"]["frames"][0]
    im = f.render(rows, scale=scale)
    bs = [f.bbox(r) for r in rows]
    x0, y0 = min(b[0] for b in bs) - 10, min(b[1] for b in bs) - 10
    d = ImageDraw.Draw(im)
    pr = piece_rows(f) or {}
    am = f.anim.get("anim_moi", {})
    piv = am.get("pivot", {})
    par = am.get("parent", {})
    for p, i in pr.items():
        b = bs[i]
        cx, cy = ((b[0] + b[2]) / 2 - x0) * scale, ((b[1] + b[3]) / 2 - y0) * scale
        if str(p) in piv:
            px, py = (piv[str(p)][0] - x0) * scale, (piv[str(p)][1] - y0) * scale
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 0, 0))
            d.line([(px, py), (cx, cy)], fill=(255, 120, 120))
        lab = f"{p}" + (f">{par.get(str(p))}" if str(p) in par else "")
        d.rectangle([cx - 2, cy - 2, cx + 7 * len(lab), cy + 11], fill=(255, 255, 210))
        d.text((cx, cy - 1), lab, fill=(0, 0, 160))
    d.text((4, 4), f.form + f" root {am.get('root')}", fill=(160, 0, 0))
    return im


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("forms", nargs="+")
    ap.add_argument("--rev")
    ap.add_argument("--scale", type=float, default=1.6)
    a = ap.parse_args()
    ims = [draw(Form(fm, a.rev), a.scale) for fm in a.forms]
    W = sum(i.width for i in ims)
    H = max(i.height for i in ims)
    S = Image.new("RGB", (W, H), "white")
    x = 0
    for i in ims:
        S.paste(i.convert("RGB"), (x, 0))
        x += i.width
    S.save(a.out)
