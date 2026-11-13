# -*- coding: utf-8 -*-
"""Thú một sừng đảo Mộc (mã làm việc giac_moc; con gốc của rig: monster_3804, game tham khảo). Tướng thứ 9 đảo Mộc (suất moc_tinh, ải 60).

Người dùng 2026-11-13: sinh vật lớn đi bốn chân, một sừng trên đầu; các phần trên lưng đổi thành dây leo, hoa...; trong bụng có một quả
cầu năng lượng kiểu trái tim phát sáng (luôn có sẵn), chiêu cuối mở bụng (open_01 + open_02) rồi bắn tia từ đó.
Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

    giac_moc.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3804/mo/<tên>_<k>.jpg + bảng
    giac_moc.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part (tên slot) + viền từng part → mo/nhom_<tên>.jpg
    giac_moc.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3804/parts/ + tờ tổng (chỉ để xem)
"""
import json
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
from quai.soi import _tris  # noqa: E402
import to_manh  # noqa: E402

CODE = "giac_moc"
MON = "monster_3804"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
ATT = "att_idle0.json"
F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
F2 = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
NEN = (120, 125, 140)

# nhóm part theo tên slot của họ (thứ tự xét: cái đầu tiên khớp thì lấy)
NHOM = [
    ("toc_lung_sau", r"^P_beifa", (150, 90, 60)),            # hai mảng tóc / bờm to sau lưng
    ("long_lung", r"^B_beimao", (70, 170, 90)),              # 18 chùm lông / gai mềm trên lưng (chuỗi nhiều xương)
    ("da_lung", r"^S_shitou", (160, 160, 170)),              # 5 tảng đá / tinh thể trên lưng (cứng)
    ("gai_lung", r"^P_bei_", (220, 200, 90)),                # 5 gai / xương sống lưng
    ("chan_sau_xa", r"^TH_tuiL", (90, 140, 230)),
    ("chan_truoc_xa", r"^TQ_tuiL", (120, 190, 250)),
    ("chan_sau_gan", r"^TH_tuiR", (230, 120, 90)),
    ("chan_truoc_gan", r"^TQ_tuiR", (250, 170, 110)),
    ("long_chan", r"^P_tuimao", (200, 120, 220)),            # túm lông ở chân
    ("sung_chan", r"^P_tuijiao", (240, 240, 120)),           # gai / cựa ở chân
    ("than", r"^P_shenti", (235, 235, 235)),
    ("co_than", r"^B_bozi_1$|^P_bozi", (200, 200, 255)),
    ("nguc_A", r"^B_bozi_A", (255, 60, 160)),
    ("nguc_B", r"^B_bozi_B", (255, 120, 60)),
    ("nguc_C", r"^B_bozi_C", (60, 220, 220)),
    ("nguc_D", r"^B_bozi_D", (140, 255, 80)),
    ("nguc_E", r"^B_bozi_E", (170, 110, 255)),
    ("nguc_F", r"^B_bozi_F", (255, 230, 60)),
    ("dau", r"^P_tou|^B_tou", (255, 255, 255)),
    ("toc_dau", r"^P_toufa", (120, 80, 160)),
]


def nhom_cua(slot):
    for ten, rx, mau in NHOM:
        if re.search(rx, slot):
            return ten, mau
    return "khac", (255, 0, 0)


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


def rig_goc():
    return os.path.join(sxs(), "web", "assets", "Monster", MON)


def scan():
    return os.path.join(sxs(), "scan", MON)


_C = {}


def nap(att=None):
    att = att or ATT
    if _C.get("att") != att:
        atlas, imgs = _C.get("atlas"), _C.get("imgs")
        if atlas is None:
            atlas, imgs = to_manh.nap(rig_goc(), MON)
        D = json.load(open(os.path.join(scan(), att), encoding="utf-8"))
        atts = sorted([a for a in D["atts"] if a.get("region") in imgs and a["cur"] and a["slot"] != "shadow"], key=lambda a: a["order"])
        _C.update(att=att, atlas=atlas, imgs=imgs, atts=atts, bones=D["bones"])
    return _C["atlas"], _C["imgs"], _C["atts"]


def luoi(a):
    atlas, imgs, _ = nap(_C.get("att"))
    im = imgs[a["region"]]
    if "uv" in a:
        return np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3)
    r = atlas[a["region"]]
    ox, oy, ow, oh = r.get("offsets", [0, 0, im.width, im.height])
    w, h = (r["bounds"][3], r["bounds"][2]) if r["rotate"] in (90, 270) else (r["bounds"][2], r["bounds"][3])
    return (np.array([[ox, oh - oy], [ox, oh - oy - h], [ox + w, oh - oy - h], [ox + w, oh - oy]], float),
            np.array([[0, 1, 2], [2, 3, 0]]))


def part_goc(a):
    """ảnh một part của con gốc cắt đúng theo lưới của nó."""
    _, imgs, _ = nap(_C.get("att"))
    im = imgs[a["region"]].convert("RGBA")
    uv, tr = luoi(a)
    m = Image.new("L", (im.width * 4, im.height * 4), 0)
    d = ImageDraw.Draw(m)
    for t in tr:
        d.polygon([tuple(uv[i] * 4) for i in t], fill=255, outline=255)
    A = np.asarray(im).copy()
    A[..., 3] = (A[..., 3].astype(np.float32) * np.asarray(m.resize(im.size, Image.LANCZOS)) / 255.0).astype(np.uint8)
    return Image.fromarray(A, "RGBA")


def xuong_bam(a, bn):
    w = a.get("w")
    if not w:
        return a["bone"]
    bs = {}
    for v in w:
        for b, ww in v:
            bs[bn[b]] = bs.get(bn[b], 0) + ww
    return " ".join(f"{b}:{v / len(w):.2f}" for b, v in sorted(bs.items(), key=lambda q: -q[1]))


def _khung(atts, S, hop=None):
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    if hop:
        x0, y0, x1, y1 = hop
    else:
        x0, y0, x1, y1 = P[:, 0].min() - 20, P[:, 1].min() - 20, P[:, 0].max() + 20, P[:, 1].max() + 20
    cw, ch = int((x1 - x0) * S), int((y1 - y0) * S)
    return cw, ch, (lambda V: np.stack([(V[:, 0] - x0) * S, (y1 - V[:, 1]) * S], 1))


def _lop(a, imgs, cw, ch, T):
    im = imgs[a["region"]]
    uv, tr = luoi(a)
    lay = Image.new("RGBa", (cw, ch), (0, 0, 0, 0))
    _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
    return lay.convert("RGBA")


def mo(att="att_idle0.json", ten="idle0", S=0.24, cot=6, hang=4):
    S = float(S)
    _, imgs, atts = nap(att)
    D = json.load(open(os.path.join(scan(), att), encoding="utf-8"))
    bn = [b["name"] for b in D["bones"]]
    cw, ch, T = _khung(atts, S)
    lops = [_lop(a, imgs, cw, ch, T) for a in atts]
    ca = Image.new("RGBA", (cw, ch), NEN + (255,))
    for l_ in lops:
        ca.alpha_composite(l_)
    mo_ = Image.blend(Image.new("RGBA", (cw, ch), NEN + (255,)), ca, 0.28)
    ra = os.path.join(scan(), "mo")
    os.makedirs(ra, exist_ok=True)
    n = cot * hang
    bang = []
    for k in range(0, len(atts), n):
        to = Image.new("RGB", (cw * cot, (ch + 44) * hang), (60, 62, 70))
        d = ImageDraw.Draw(to)
        for j, a in enumerate(atts[k:k + n]):
            o = mo_.copy()
            o.alpha_composite(lops[k + j])
            al = np.asarray(lops[k + j])[..., 3] > 60
            vien = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1))
            arr = np.asarray(o).copy()
            arr[vien] = (255, 60, 60, 255)
            x, y = (j % cot) * cw, (j // cot) * (ch + 44)
            to.paste(Image.fromarray(arr, "RGBA").convert("RGB"), (x, y + 44))
            xb = xuong_bam(a, bn)
            im = imgs[a["region"]]
            d.text((x + 4, y + 2), f"{a['order']} {a['slot']} ({im.width}×{im.height})", fill=(255, 255, 255), font=F)
            d.text((x + 4, y + 22), xb[:48], fill=(255, 220, 120), font=F)
            bang.append((a["order"], a["slot"], a["region"], im.width, im.height, len(a["xy"]) // 2, xb))
        p = os.path.join(ra, f"{ten}_{k // n}.jpg")
        to.save(p, quality=86)
        print(p, to.size)
    with open(os.path.join(ra, f"{ten}_bang.txt"), "w", encoding="utf-8") as f:
        for b in bang:
            f.write("\t".join(str(x) for x in b) + "\n")


def nhom(att="att_idle0.json", ten="idle0", S=0.9, hop=None):
    """cả con: bên trái hình thật, bên phải tô màu theo nhóm + viền từng part + số thứ tự vẽ."""
    S = float(S)
    if isinstance(hop, str):
        hop = [float(x) for x in hop.split(",")]
    _, imgs, atts = nap(att)
    cw, ch, T = _khung(atts, S, hop)
    that = Image.new("RGBA", (cw, ch), NEN + (255,))
    to = Image.new("RGBA", (cw, ch), (40, 42, 50, 255))
    d = ImageDraw.Draw(to)
    nhan = []
    for a in atts:
        lay = _lop(a, imgs, cw, ch, T)
        that.alpha_composite(lay)
        al = np.asarray(lay)[..., 3] > 60
        if not al.any():
            continue
        _, mau = nhom_cua(a["slot"])
        arr = np.asarray(to).copy()
        g = np.asarray(lay.convert("L")).astype(np.float32) / 255.0
        for c in range(3):
            arr[..., c][al] = (mau[c] * (0.45 + 0.55 * g[al])).astype(np.uint8)
        vien = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1))
        arr[vien] = (20, 20, 20, 255)
        to = Image.fromarray(arr, "RGBA")
        ys, xs = np.nonzero(al)
        nhan.append((int(xs.mean()), int(ys.mean()), str(a["order"])))
    d = ImageDraw.Draw(to)
    for x, y, s in nhan:
        d.text((x - 6, y - 7), s, fill=(0, 0, 0), font=F, stroke_width=2, stroke_fill=(255, 255, 255))
    ra = Image.new("RGB", (cw * 2, ch + 30 * ((len(NHOM) + 4) // 5)), (30, 30, 36))
    ra.paste(that.convert("RGB"), (0, 0))
    ra.paste(to.convert("RGB"), (cw, 0))
    d = ImageDraw.Draw(ra)
    for i, (t, _, mau) in enumerate(NHOM):
        x, y = 10 + (i % 5) * (cw * 2 // 5), ch + 4 + (i // 5) * 30
        d.rectangle([x, y, x + 22, y + 22], fill=mau)
        d.text((x + 28, y), t, fill=(255, 255, 255), font=F2)
    os.makedirs(os.path.join(scan(), "mo"), exist_ok=True)
    p = os.path.join(scan(), "mo", f"nhom_{ten}.jpg")
    ra.save(p, quality=88)
    print(p, ra.size)


def part_het():
    """mọi part cắt theo lưới ra file riêng + tờ tổng xếp theo nhóm (chỉ để xem)."""
    _, imgs, atts = nap("att_goc.json")
    ra = os.path.join(scan(), "parts")
    os.makedirs(ra, exist_ok=True)
    ds = []
    for a in atts:
        im = part_goc(a)
        im.save(os.path.join(ra, f"{a['order']:03d}_{a['slot']}.png"))
        ds.append((a, im))
    # tờ tổng: xếp kệ theo thứ tự vẽ, nền xám
    Wt, x, y, hh = 2200, 10, 10, 0
    cho = []
    for a, im in ds:
        if x + im.width + 10 > Wt:
            x, y, hh = 10, y + hh + 30, 0
        cho.append((x, y))
        x += im.width + 14
        hh = max(hh, im.height)
    to = Image.new("RGBA", (Wt, y + hh + 40), NEN + (255,))
    d = ImageDraw.Draw(to)
    for (a, im), (x, y) in zip(ds, cho):
        to.alpha_composite(im, (x, y))
        d.text((x, y + im.height + 2), f"{a['order']}", fill=(255, 255, 255), font=F)
    p = os.path.join(scan(), "parts", "_tong.jpg")
    to.convert("RGB").save(p, quality=88)
    print(p, to.size, len(ds), "part")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "mo":
        mo(*sys.argv[2:5])
    elif cmd == "nhom":
        nhom(*sys.argv[2:6])
    elif cmd == "part_goc":
        part_het()
    else:
        print(__doc__)
