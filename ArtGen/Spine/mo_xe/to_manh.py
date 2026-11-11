# -*- coding: utf-8 -*-
"""Tờ mổ mảnh của một rig Spine: xem người ta TÁCH MẢNH thế nào (dùng trước khi chia mảnh cho tướng làm theo con gốc đó).

    to_manh.py anh  <thư mục rig> <tên> <ra.png>              mọi vùng ảnh trong atlas (đã gỡ xoay, khung gốc), tên và cỡ
    to_manh.py dang <thư mục rig> <tên> <att.json> <ra.png> [cột]   một dáng (att.json của `chay.py att`): cả con + viền từng mảnh,
                                                              rồi TỪNG MẢNH vẽ riêng trên nền cả con mờ, ghi slot, hình, thứ tự vẽ,
                                                              xương bám (mảnh nào đè mảnh nào, phần khuất của mỗi mảnh ra sao)

Ví dụ (con rắn monster_3247, kết quả ở D:/Ripper/SwordxStaff/scan/monster_3247/):
    py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/mo_xe/chay.py att <rig> monster_3247 att_goc.json
    py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/mo_xe/chay.py att <rig> monster_3247 att_run.json "anim=run_01&t=0.1"
    py -3 -I ArtGen/Spine/mo_xe/to_manh.py anh  <rig> monster_3247 manh_anh.png
    py -3 -I ArtGen/Spine/mo_xe/to_manh.py dang <rig> monster_3247 att_goc.json manh_dang_goc.png
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from quai.soi import _tris  # noqa: E402

FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
NEN = (120, 125, 140)
MAU = [(255, 80, 80), (255, 200, 60), (90, 220, 90), (80, 200, 255), (200, 120, 255), (255, 140, 200), (255, 255, 255), (255, 150, 60)]


def doc_atlas(p):
    R, cur = {}, None
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        if not ln.strip():
            continue
        if not ln.startswith(("\t", " ")):
            if ":" in ln:
                continue
            cur = ln.strip()
            R[cur] = {"rotate": 0}
        elif cur:
            k, v = [s.strip() for s in ln.split(":", 1)]
            if k in ("bounds", "offsets"):
                R[cur][k] = [int(x) for x in v.split(",")]
            elif k == "rotate":
                R[cur][k] = 90 if v == "true" else (0 if v == "false" else int(v))
    return R


def vung(page, r):
    """ảnh gốc của một vùng: gỡ xoay, trả về khung gốc chưa cắt (để uv của lưới dùng thẳng)."""
    x, y, w, h = r["bounds"]
    deg = r["rotate"]
    im = page.crop((x, y, x + h, y + w)) if deg in (90, 270) else page.crop((x, y, x + w, y + h))
    if deg:
        # atlas Spine 4: degrees 90 = vùng lưu xoay 90 độ; gỡ bằng xoay THEO chiều kim (PIL rotate góc âm). Xoay sai chiều thì mảnh lộn
        # 180 độ (hạt đậu, khối tròn nhìn vẫn "đúng", chỉ lộ ở mặt: lỗi đã gặp 2026-11-11)
        im = im.rotate(-deg, expand=True)
    if "offsets" in r:
        ox, oy, ow, oh = r["offsets"]
        full = Image.new("RGBA", (ow, oh), (0, 0, 0, 0))
        full.paste(im, (ox, oh - oy - im.height))
        im = full
    return im


def nap(rig, ten):
    atlas = doc_atlas(os.path.join(rig, ten + ".atlas"))
    page = Image.open(os.path.join(rig, ten + ".png")).convert("RGBA")
    return atlas, {n: vung(page, r) for n, r in atlas.items()}


def to_anh(rig, ten, ra, z=3):
    atlas, imgs = nap(rig, ten)
    ten_ = sorted(imgs, key=lambda n: -imgs[n].width * imgs[n].height)
    W = 2400
    x = y = 20
    hh = 0
    cho = []
    for n in ten_:
        w, h = imgs[n].width * z, imgs[n].height * z
        if x + w + 20 > W:
            x, y, hh = 20, y + hh + 50, 0
        cho.append((n, x, y))
        x += max(w, 150) + 30
        hh = max(hh, h)
    out = Image.new("RGB", (W, y + hh + 50), NEN)
    d = ImageDraw.Draw(out)
    for n, x, y in cho:
        im = imgs[n].resize((imgs[n].width * z, imgs[n].height * z), Image.LANCZOS)
        out.paste(im, (x, y + 22), im)
        d.text((x, y), f"{n} {imgs[n].width}x{imgs[n].height}", fill=(255, 255, 255), font=FONT)
    out.save(ra)
    print(ra, out.size, len(ten_), "vùng")


def to_dang(rig, ten, att_json, ra, cot=5, S=3.0):
    atlas, imgs = nap(rig, ten)
    D = json.load(open(att_json, encoding="utf-8"))
    bones = [b["name"] for b in D["bones"]]
    atts = sorted([a for a in D["atts"] if a.get("region") in imgs], key=lambda a: (a["order"], not a["cur"]))
    P = np.array([v for a in atts if a["cur"] or D["anim"] for v in np.array(a["xy"]).reshape(-1, 2).tolist()])
    x0, y0, x1, y1 = P[:, 0].min() - 15, P[:, 1].min() - 15, P[:, 0].max() + 15, P[:, 1].max() + 15
    cw, ch = int((x1 - x0) * S), int((y1 - y0) * S)

    def hinh(a):
        im = imgs[a["region"]]
        V = np.array(a["xy"], float).reshape(-1, 2)
        V = np.stack([(V[:, 0] - x0) * S, (y1 - V[:, 1]) * S], 1)
        if a["type"].endswith("MeshAttachment"):
            UV = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
            tr = np.array(a["tris"]).reshape(-1, 3)
            vien = V[:a["hull"]]
        else:                                   # region: 4 góc BL, UL, UR, BR của vùng đã cắt
            r = atlas[a["region"]]
            ox, oy, ow, oh = r.get("offsets", [0, 0, im.width, im.height])
            w, h = (r["bounds"][3], r["bounds"][2]) if r["rotate"] in (90, 270) else (r["bounds"][2], r["bounds"][3])
            UV = np.array([[ox, oh - oy], [ox, oh - oy - h], [ox + w, oh - oy - h], [ox + w, oh - oy]], float)
            tr = np.array([[0, 1, 2], [2, 3, 0]])
            vien = V
        return im, V, UV, tr, vien

    def ve(ds, mo=1.0):
        layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        for a in ds:
            im, V, UV, tr, _ = hinh(a)
            lay = Image.new("RGBa", (cw, ch), (0, 0, 0, 0))
            _tris(lay, im.convert("RGBa"), V, UV, tr)
            layer.alpha_composite(lay.convert("RGBA"))
        if mo < 1:
            arr = np.asarray(layer).copy()
            arr[..., 3] = (arr[..., 3] * mo).astype(np.uint8)
            layer = Image.fromarray(arr, "RGBA")
        return layer

    hien = [a for a in atts if a["cur"] and a.get("alpha", 1) > 0.01]
    cells = []
    c0 = Image.new("RGBA", (cw, ch), NEN + (255,))
    c0.alpha_composite(ve(hien))
    dd = ImageDraw.Draw(c0)
    for i, a in enumerate(hien):
        v = hinh(a)[4]
        pts = [tuple(p) for p in v.tolist()]
        dd.line(pts + [pts[0]], fill=MAU[i % len(MAU)] + (255,), width=2)
    dd.text((6, 4), ("dáng gốc" if not D["anim"] else f"{D['anim']} @ {D['t']} s") + ": cả con + viền từng mảnh", fill=(255, 255, 255), font=FONT)
    cells.append(c0)
    mo_nen = ve(hien, 0.2)
    for i, a in enumerate(atts):
        c = Image.new("RGBA", (cw, ch), NEN + (255,))
        c.alpha_composite(mo_nen)
        c.alpha_composite(ve([a]))
        dd = ImageDraw.Draw(c)
        v = hinh(a)[4]
        pts = [tuple(p) for p in v.tolist()]
        dd.line(pts + [pts[0]], fill=MAU[i % len(MAU)] + (255,), width=2)
        xb = sorted({bones[b] for w in a.get("w", []) for b, _ in w}) or [a["bone"]]
        im = imgs[a["region"]]
        dd.text((6, 4), f"[{a['order']}] slot {a['slot']}" + ("" if a["cur"] else "  (KHÔNG bật ở dáng này)"), fill=(255, 255, 255), font=FONT)
        dd.text((6, 22), f"ảnh {a['region']} {im.width}x{im.height}, {a['type'].replace('Attachment', '').strip('_')}", fill=(255, 255, 255), font=FONT)
        dd.text((6, 40), "xương: " + ", ".join(xb), fill=(255, 255, 200), font=FONT)
        cells.append(c)
    hang = (len(cells) + cot - 1) // cot
    out = Image.new("RGB", (cot * cw, hang * ch), NEN)
    for j, c in enumerate(cells):
        out.paste(c.convert("RGB"), ((j % cot) * cw, (j // cot) * ch))
    out.save(ra)
    print(ra, out.size, len(atts), "hình; thứ tự vẽ:", [a["slot"] for a in hien])


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["anh"]:
        to_anh(a[1], a[2], a[3])
    elif a[:1] == ["dang"]:
        to_dang(a[1], a[2], a[3], a[4], int(a[5]) if len(a) > 5 else 5)
    else:
        print(__doc__)
