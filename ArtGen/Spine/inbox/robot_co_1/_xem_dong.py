# -*- coding: utf-8 -*-
"""Ảnh động xem trước từng clip của rig robot cổ (WebP lặp), vẽ bằng bộ vẽ Python của quai. Đòn, chiêu mana, chiêu cuối đều đứng tại chỗ
(đạn, cầu năng lượng, tên lửa là VFX + code ở bước vào game): khối xám là chỗ đối thủ. Chỉ để xem trong máy (chuyển động gốc là của game
tham khảo).

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/inbox/robot_co_1/_xem_dong.py [clip...]   → rig/dong/<clip>.webp
"""
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
import robot_co_rig as R  # noqa: E402
from quai import soi  # noqa: E402

NEN = (150, 150, 150)
RONG = 560
X_DT, H_DT = 1.7, 0.85                                  # chân đối thủ cách chân mình, chiều cao đối thủ (× chiều cao)


def luu(ims, p, buoc):
    ims[0].save(p, save_all=True, append_images=ims[1:], duration=int(round(1000 * buoc / 30)), loop=0, quality=74, method=4,
                minimize_size=True)


def ve_khung(ve0, fr, cao, doi=None, rong=RONG):
    Bx = soi._union([ve0.bao(P) for P in fr], 0.03)
    if doi:
        Bx = (min(Bx[0], -0.8 * cao), min(Bx[1], -20.0), max(Bx[2], (X_DT + 0.45) * cao), max(Bx[3], 1.1 * cao))
    sc = min(0.8, rong / (Bx[2] - Bx[0]))
    ims = []
    for P in fr:
        nen = ve0.ve(P, Bx, sc, bg=NEN, ss=2).convert("RGB")
        if doi:
            khung = Image.new("RGB", nen.size, NEN)
            d = ImageDraw.Draw(khung)
            x0, x1 = ((X_DT - 0.3) * cao - Bx[0]) * sc, ((X_DT + 0.3) * cao - Bx[0]) * sc
            y0, y1 = (Bx[3] - H_DT * cao) * sc, (Bx[3] - 0.0) * sc
            d.rounded_rectangle([x0, y0, x1, y1], radius=int(0.12 * cao * sc), fill=(118, 118, 124), outline=(70, 70, 76), width=3)
            m = Image.eval(Image.fromarray(np.abs(np.asarray(nen).astype(int) - np.array(NEN)).sum(2).clip(0, 255).astype(np.uint8)),
                           lambda v: 255 if v > 6 else 0)
            khung.paste(nen, (0, 0), m)
            nen = khung
        ims.append(nen)
    return ims


def main(chi):
    sk, info = R.dung()
    ve0 = soi.Ve(sk)
    clips = R.lam_clip(sk, info)
    idle0 = R.nuong(sk, [c for c in clips if c.ten == "idle"][0])[0]
    cao = soi.chieu_cao(ve0, idle0)
    ra = os.path.join(R.RA, "dong")
    os.makedirs(ra, exist_ok=True)
    for c in clips:
        if chi and c.ten not in chi:
            continue
        t0 = time.time()
        fr = R.nuong(sk, c)
        if c.loop and len(fr) == int(round(c.dur * 30)) + 1:
            fr = fr[:-1]
        doi = c.ten in ("attack", "skill", "cast")
        vong = 2 if c.ten in ("idle", "walk") else 1
        fr = fr * vong
        if not c.loop:
            fr = [fr[0]] * 6 + fr + [fr[-1]] * 12 if c.ten != "appear" else fr + [fr[-1]] * 15
        ims = ve_khung(ve0, fr, cao, doi, RONG * (1.5 if doi else 1.0))
        p = os.path.join(ra, c.ten + ".webp")
        luu(ims, p, 1)
        print(f"{c.ten}: {len(ims)} khung {ims[0].size}, {os.path.getsize(p) // 1024} KB, {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
