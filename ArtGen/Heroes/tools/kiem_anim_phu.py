"""Kiểm kê animation phụ của bản gốc aola mà dạng vẽ lại còn thiếu (người dùng dặn 2026-11-07: "các con hôm qua làm chưa có đầy
đủ animation như con gốc, đặc biệt là phần nước bao quanh/các animation phụ, gen thêm và bù vào").

Bản gốc <aola>/reskin/goc_<id>/export/anim.json: mảnh = hàng khung đầu clip đứng (số mảnh như Rig_Numbered); mảnh có khung con
(tên hình c<n>_<k>) là mảnh tự chạy (nước chảy, bọt, tua, mắt chớp). Dạng vẽ lại (Resources/<dạng>) chỉ có một hình mỗi mảnh.

    py -3 ArtGen/Heroes/tools/kiem_anim_phu.py <ảnh ra.png> [dạng ...]
In: mỗi dạng, mảnh tự chạy (số khung con, có trong dạng mới không), mảnh bị bỏ khi ghép; tờ ảnh: khung con gốc cạnh hình mới.
"""
import collections
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aola_form import Form  # noqa: E402

AOLA = next(p for p in ("E:/ProjectAtomik/aola", "D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper") if os.path.isdir(p))
BASE = "4d7557b"


def cname(p):
    return os.path.basename(p)[:-4]


def base(n):
    return n.split("_")[0]


def goc(pid):
    d = json.load(open(os.path.join(AOLA, "reskin", f"goc_{pid}", "export", "anim.json"), encoding="utf-8"))
    sp = d["sprites"]
    fr = d["clips"]["1_1"]["frames"]
    f0 = [cname(sp[r[0]]) for r in fr[0]]
    var = collections.defaultdict(list)
    for f in fr:
        for r in f:
            n = cname(sp[r[0]])
            if n not in var[base(n)]:
                var[base(n)].append(n)
    return d, sp, fr, f0, var


def inventory(form):
    pid = int(form.split("_")[1])
    d, sp, fr, f0, var = goc(pid)
    f = Form(form, rev=BASE)
    have = set(f.anim["idle_parts"])
    out = []
    for i, n in enumerate(f0, 1):
        b = base(n)
        k = len(var[b])
        if k > 1 or i not in have:
            out.append(dict(piece=i, char=n, frames=k, kept=i in have, subs=var[b]))
    return pid, f, out, sp


def sheet(forms, path, cell=96):
    rows = []
    for form in forms:
        pid, f, inv, sp = inventory(form)
        line = [(f"{form}", None)]
        for it in inv:
            subs = it["subs"][:8]
            for j, n in enumerate(subs):
                p = os.path.join(AOLA, "reskin", f"pet{pid}_parts", "chars", n + ".png")
                im = Image.open(p).convert("RGBA") if os.path.exists(p) else None
                line.append((f"{it['piece']}{'' if it['kept'] else 'X'} {j}/{it['frames']}" if j == 0 else f"{j}", im))
        rows.append(line)
    W = max(len(r) for r in rows) * cell
    S = Image.new("RGB", (W, len(rows) * (cell + 14)), "white")
    d = ImageDraw.Draw(S)
    for y, r in enumerate(rows):
        for x, (lab, im) in enumerate(r):
            X, Y = x * cell, y * (cell + 14)
            d.text((X + 2, Y + 1), lab, fill=(180, 0, 0) if "X" in lab else (0, 0, 0))
            if im is not None:
                t = im.copy()
                t.thumbnail((cell - 4, cell - 4))
                bg = Image.new("RGBA", t.size, (235, 235, 235, 255))
                bg.alpha_composite(t)
                S.paste(bg.convert("RGB"), (X + 2, Y + 14))
    S.save(path)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    out = sys.argv[1]
    forms = sys.argv[2:]
    for form in forms:
        pid, f, inv, sp = inventory(form)
        print(form, "; ".join(f"{it['piece']}:{it['char']} x{it['frames']}{'' if it['kept'] else ' BỎ'}" for it in inv))
    sheet(forms, out)
