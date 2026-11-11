# -*- coding: utf-8 -*-
"""tm06 dạng 2: cận đầu–cổ ở các khung xoay mạnh nhất (skill chồm gầm, cast há, hit, die), nền xám, không lưới; ra
inbox/tm06_2/rig/can_dau_co.png.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm06_can_co.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw  # noqa: E402

from quai import anh, hoat, soi  # noqa: E402

import tm06 as T  # noqa: E402
import tm06_d2  # noqa: E402


def main():
    sk, info = tm06_d2.dung2()
    cl = {c.ten: c for c in tm06_d2.clips2(sk, info)}
    ve = soi.Ve(sk)
    # tìm khung đầu xoay mạnh nhất (góc thế giới xương dau lệch dáng gốc) trong skill
    import math
    fr = {n: hoat.nuong(sk, cl[n]) for n in ("skill", "cast", "hit", "die", "attack")}
    a0 = math.degrees(math.atan2(sk.W0["dau"][1, 0], sk.W0["dau"][0, 0]))

    def goc(P):
        W = sk.the_gioi(P)
        return abs(((math.degrees(math.atan2(W["dau"][1, 0], W["dau"][0, 0])) - a0) + 180) % 360 - 180)
    pick = []
    for n in ("skill", "cast", "hit", "attack", "die"):
        i = max(range(len(fr[n]) - (8 if n == "die" else 0)), key=lambda j: goc(fr[n][j]))
        pick.append((n, i, goc(fr[n][i])))
    o = 420
    out = Image.new("RGB", (o * len(pick), o + 24), (255, 255, 255))
    d = ImageDraw.Draw(out)
    f = anh.font(15)
    for c, (n, i, g) in enumerate(pick):
        P = fr[n][i]
        W = sk.the_gioi(P)
        x, y = W["co"][:2, 2]
        r = 95
        im = ve.ve(P, (x - r * 0.6, y - r, x + r * 1.4, y + r), o / (2 * r), bg=(150, 150, 150), ss=2)
        out.paste(im.convert("RGB").resize((o, o)), (c * o, 24))
        d.text((c * o + 6, 4), f"{n} {i / 30:.2f}s · đầu xoay {g:.1f}°", fill=(0, 0, 0), font=f)
    ra = T.inbox(2, "rig", "can_dau_co.png")
    out.save(ra)
    print(ra, [(n, round(i / 30, 2), round(g, 1)) for n, i, g in pick])


if __name__ == "__main__":
    main()
