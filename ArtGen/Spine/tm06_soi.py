# -*- coding: utf-8 -*-
"""tm06: soi cận các chỗ nối (cổ, gốc đuôi, đỉnh chân, vai, gốc mang) ở nhiều khung, nền xám để thấy khe hở; ra rig/soi_noi.png.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm06_soi.py 2
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw  # noqa: E402

from quai import anh, hoat, soi  # noqa: E402

import tm06 as T  # noqa: E402

CHO = {2: [("co", "dau", 70), ("goc duoi", "duoi0", 70), ("chan1", "chan10", 60), ("chan3", "chan30", 60), ("chan4", "chan40", 60),
           ("mang", "mang_n10", 70)],
       1: [("co", "dau", 60), ("goc duoi", "duoi0", 60), ("vai gan", "tay_n0", 50), ("vai xa", "tay_x0", 50), ("hong t", "chan_t0", 55),
           ("hong p", "chan_p0", 55), ("mang", "mang_n10", 60)]}
KHUNG = {2: [("idle", 0.0), ("idle", 1.6), ("attack", 0.62), ("cast", 0.9), ("skill", 1.3), ("hit", 0.08), ("die", 1.1)],
         1: [("idle", 0.0), ("attack", 0.48), ("cast", 0.62), ("skill", 1.05), ("skill", 0.28), ("hit", 0.08), ("die", 0.9)]}


def main(k):
    if k == 2:
        import tm06_d2
        sk, info = tm06_d2.dung2()
        cl = tm06_d2.clips2(sk, info)
    else:
        sk, info = T.dung1()
        cl = T.clips1(sk, info)
    cd = {c.ten: c for c in cl}
    fr = {}
    ve = soi.Ve(sk)
    cho = [c for c in CHO[k] if c[1] in sk.bi]
    o = 220
    out = Image.new("RGB", (o * len(cho), (o + 18) * len(KHUNG[k])), (255, 255, 255))
    d = ImageDraw.Draw(out)
    f = anh.font(13)
    for r, (cn, t) in enumerate(KHUNG[k]):
        if cn not in fr:
            fr[cn] = hoat.nuong(sk, cd[cn])
        P = fr[cn][min(len(fr[cn]) - 1, int(round(t * 30)))]
        W = sk.the_gioi(P)
        for c, (nm, b, rr) in enumerate(cho):
            x, y = W[b][:2, 2]
            im = ve.ve(P, (x - rr, y - rr, x + rr, y + rr), o / (2 * rr), bg=(150, 150, 150), ss=2)
            out.paste(im.convert("RGB").resize((o, o)), (c * o, r * (o + 18) + 18))
            d.text((c * o + 4, r * (o + 18) + 2), f"{cn} {t:.2f}s · {nm}", fill=(0, 0, 0), font=f)
    ra = T.inbox(k, "rig", "soi_noi.png")
    out.save(ra)
    print(ra, out.size)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
