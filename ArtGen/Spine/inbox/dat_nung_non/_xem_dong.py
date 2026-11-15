# -*- coding: utf-8 -*-
"""Ảnh động xem trước từng clip của Viêm Dũng (dạng 2) / Viêm Dũng Nhi (dạng 1, DN_NON=1), WebP lặp, vẽ bằng bộ vẽ Python của quai (không
cần trình duyệt): để người dùng xem chuyển động khi không mở được rig/xem.html. Chỉ có hình của mình; KHÔNG chạy với DN_GOC=1.

    [DN_NON=1] py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/inbox/dat_nung_non/_xem_dong.py [clip...]   → <rig>/dong/<clip>.webp
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
import dat_nung_rig as R  # noqa: E402
from quai import hoat, soi  # noqa: E402

if R.GOC:
    raise SystemExit("không xuất ảnh động của da gốc")
NEN = (150, 150, 150)
RONG = 560                                   # bề ngang tối đa (px)
BUOC = {"idle": 2, "walk": 1}                # cứ mấy khung lấy một (mặc định 2: 15 khung / giây)


def main(chi):
    sk, info = R.dung()
    ve0 = soi.Ve(sk)
    clips = R.lam_clip(sk, info)
    ra = os.path.join(R.RA, "dong")
    os.makedirs(ra, exist_ok=True)
    for c in clips:
        if chi and c.ten not in chi:
            continue
        t0 = time.time()
        fr = hoat.nuong(sk, c)
        buoc = BUOC.get(c.ten, 2)
        if c.loop and len(fr) == int(round(c.dur * 30)) + 1:
            fr = fr[:-1]
        fr = fr[::buoc]
        if not c.loop:                       # giữ khung cuối nửa giây rồi mới lặp lại
            fr = fr + [fr[-1]] * (15 // buoc)
        Bx = soi._union([ve0.bao(P) for P in fr], 0.03)
        sc = min(0.5, RONG / (Bx[2] - Bx[0]))
        ims = [ve0.ve(P, Bx, sc, bg=NEN, ss=2).convert("RGB") for P in fr]
        p = os.path.join(ra, c.ten + ".webp")
        ims[0].save(p, save_all=True, append_images=ims[1:], duration=int(round(1000 * buoc / 30)), loop=0, quality=70, method=4,
                    minimize_size=True)
        print(f"{c.ten}: {len(ims)} khung {ims[0].size}, {os.path.getsize(p) // 1024} KB, {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
