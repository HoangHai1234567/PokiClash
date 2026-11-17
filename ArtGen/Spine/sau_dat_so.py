# -*- coding: utf-8 -*-
"""Sâu đất (sau_dat): so rig với concept đã duyệt CÙNG KHUNG (khung concept = goc_ca_con: s px / đơn vị, tâm cx, cy).
    sau_dat_so.py [clip] [giây]    → inbox/sau_dat_1/mau/_so_rig_concept.png (concept | rig | chồng) + _so_dau.png (cận đầu)
                                     + inbox/sau_dat_xem_so.html"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sau_dat_rig as R  # noqa: E402
from quai import hoat, soi  # noqa: E402

W, H = 1536, 1024


def main(a):
    clip = a[0] if a else "idle"
    t = float(a[1]) if len(a) > 1 else 0.0
    sk, info = R.dung()
    clips = R.lam_clip(sk, info)
    c = [x for x in clips if x.ten == clip][0]
    P = hoat.nuong(sk, c)[min(int(round(t * 30)), int(round(c.dur * 30)))]
    j = json.load(open(os.path.join(R.G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    box = (cx - (W / 2) / s, cy - (H / 2) / s, cx + (W / 2) / s, cy + (H / 2) / s)
    rig = soi.Ve(sk).ve(P, box, s, bg=None, ss=2).resize((W, H), Image.LANCZOS)
    con = Image.open(os.path.join(R.G.TAI, "L1_duyet.png")).convert("RGBA").resize((W, H))
    nen = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    r1 = nen.copy()
    r1.alpha_composite(rig)
    chong = Image.blend(con, r1, 0.5)
    tong = Image.new("RGB", (W * 3 // 2, H // 2), "white")
    for i, im in enumerate([con, r1, chong]):
        tong.paste(im.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    p1 = os.path.join(R.G.MAU, "_so_rig_concept.png")
    tong.save(p1)
    hop = (560, 220, 1120, 700)
    dau = Image.new("RGB", (560 * 3, 480), "white")
    for i, im in enumerate([con, r1, chong]):
        dau.paste(im.convert("RGB").crop(hop), (i * 560, 0))
    p2 = os.path.join(R.G.MAU, "_so_dau.png")
    dau.save(p2)
    html = os.path.join(HERE, "inbox", "sau_dat_xem_so.html")
    open(html, "w", encoding="utf-8").write(
        "<!doctype html><meta charset=utf-8><title>Sâu đất: so rig với concept</title><style>body{font:15px sans-serif;margin:16px;"
        "background:#f4f1ea}img{max-width:100%;display:block;margin:6px 0 18px;border:1px solid #ccc}</style>"
        "<h1>Sâu đất: concept đã duyệt và rig (cùng khung)</h1>"
        "<h2>Concept đã duyệt (L1_duyet.png)</h2><img src='sau_dat_1/tai_ve/L1_duyet.png'>"
        f"<h2>Cận đầu: concept | rig ({clip} {t:.2f} s) | chồng 50 %</h2><img src='sau_dat_1/mau/_so_dau.png'>"
        "<h2>Cả con: concept | rig | chồng</h2><img src='sau_dat_1/mau/_so_rig_concept.png'>")
    print(p1, p2, html)


if __name__ == "__main__":
    main(sys.argv[1:])
