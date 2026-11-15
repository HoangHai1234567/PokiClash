# -*- coding: utf-8 -*-
"""Ảnh động xem trước từng clip của rig da mình (WebP lặp), vẽ bằng bộ vẽ Python của quai (không cần trình duyệt): để người dùng xem
chuyển động khi không mở được rig/xem.html. Chỉ có hình của mình; KHÔNG chạy với NL_GOC=1.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/inbox/nui_lua_1/_xem_dong.py [clip...]   → rig/dong/<clip>.webp
"""
import os
import sys
import time

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
import nui_lua_rig as R  # noqa: E402
from quai import hoat, soi  # noqa: E402

if R.GOC:
    raise SystemExit("không xuất ảnh động của da gốc")
NEN = (150, 150, 150)
RONG = 620                                   # bề ngang tối đa (px)
# clip: (số vòng lặp ghép liền để khói khép vòng, cứ mấy khung lấy một)
CACH = {"idle": (3, 2), "walk": (3, 1)}


def main(chi):
    sk, info = R.dung()
    ve0 = soi.Ve(sk)
    clips = R.lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    bo = tuple(b for b, *_ in info["khoi"])
    cao = soi.chieu_cao(ve0, idle0, bo) - info["dat_y"]
    clips = R.lam_clip(sk, info, cao)
    aura = hoat.nuong(sk, clips[-1])
    ra = os.path.join(HERE, "..", "nui_lua_non", "rig", "dong") if R.CHIBI else os.path.join(R.G.BASE, "rig", "dong")
    os.makedirs(ra, exist_ok=True)
    for c in clips[:-1]:
        if chi and c.ten not in chi:
            continue
        t0 = time.time()
        fr = hoat.nuong(sk, c)
        vong, buoc = CACH.get(c.ten, (1, 1))
        if c.loop and len(fr) == int(round(c.dur * 30)) + 1:
            fr = fr[:-1]
        fr = hoat.phu_aura(fr * vong, aura, sk)[::buoc]
        if not c.loop:                       # giữ khung cuối nửa giây rồi mới lặp lại
            fr = fr + [fr[-1]] * (15 // buoc)
        Bx = soi._union([ve0.bao(P) for P in fr], 0.03)
        sc = min(0.5, RONG / (Bx[2] - Bx[0]))
        ims = [ve0.ve(P, Bx, sc, bg=NEN, ss=2).convert("RGB") for P in fr]
        p = os.path.join(ra, c.ten + ".webp")
        ims[0].save(p, save_all=True, append_images=ims[1:], duration=int(round(1000 * buoc / 30)), loop=0, quality=72, method=4,
                    minimize_size=True)
        print(f"{c.ten}: {len(ims)} khung {ims[0].size}, {os.path.getsize(p) // 1024} KB, {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
