# -*- coding: utf-8 -*-
"""Ảnh động xem trước từng clip của rig da mình (WebP lặp), vẽ bằng bộ vẽ Python của quai: để người dùng xem chuyển động trên artifact.
Chỉ có hình của mình; KHÔNG chạy với TS_GOC=1. Chiêu cuối ghép skill + cung nhảy giả (thay cho code game) + skill_land thành `chieu_cuoi`.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/inbox/tinh_sat_1/_xem_dong.py [clip...]   → rig/dong/<clip>.webp
"""
import os
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
import tinh_sat_rig as R  # noqa: E402
from quai import hoat, soi  # noqa: E402

if R.GOC:
    raise SystemExit("không xuất ảnh động của da gốc")
NEN = (150, 150, 150)
RONG = 560
CACH = {"idle": (1, 2), "walk": (2, 1)}


def luu(ims, p, buoc):
    ims[0].save(p, save_all=True, append_images=ims[1:], duration=int(round(1000 * buoc / 30)), loop=0, quality=74, method=4,
                minimize_size=True)


def main(chi):
    sk, info = R.dung()
    ve0 = soi.Ve(sk)
    clips = R.lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    clips = R.lam_clip(sk, info, cao)
    ra = os.path.join(R.G.BASE, "rig", "dong")
    os.makedirs(ra, exist_ok=True)
    fr_all = {c.ten: hoat.nuong(sk, c) for c in clips}
    for c in clips:
        if c.ten in ("skill", "skill_land") or (chi and c.ten not in chi):
            continue
        t0 = time.time()
        fr = fr_all[c.ten]
        vong, buoc = CACH.get(c.ten, (1, 1))
        if c.loop and len(fr) == int(round(c.dur * 30)) + 1:
            fr = fr[:-1]
        fr = (fr * vong)[::buoc]
        if not c.loop:
            fr = fr + [fr[-1]] * (12 // buoc)
        Bx = soi._union([ve0.bao(P) for P in fr], 0.03)
        sc = min(0.8, RONG / (Bx[2] - Bx[0]))
        ims = [ve0.ve(P, Bx, sc, bg=NEN, ss=2).convert("RGB") for P in fr]
        p = os.path.join(ra, c.ten + ".webp")
        luu(ims, p, buoc)
        print(f"{c.ten}: {len(ims)} khung {ims[0].size}, {os.path.getsize(p) // 1024} KB, {time.time() - t0:.0f} s", flush=True)
    if not chi or "chieu_cuoi" in chi:
        # như game (AolaSticker.Jump, bản "treo ở đỉnh" sẽ làm cho con này): rời ở `bat` của skill, chạm ở `cham_dat` của skill_land, chỗ đáp =
        # đầu đối thủ (62 % chiều cao đối thủ), đè 0,16 s rồi bật về 0,42 s. Đối thủ là khối xám giữ chỗ (không phải hình thật).
        from PIL import ImageDraw
        a, b = fr_all["skill"], fr_all["skill_land"]
        t_bat, d_sk, t_cham = R.T_BAT, R.D_SKILL, R.T_CHAM
        X, H_DT = 1.5 * cao, 0.95 * cao
        to = (X, 0.62 * H_DT)
        up = to[1] * 0.35 + 0.85 * cao

        def doc(u):                                   # độ cao cung (0..1): lên nhanh, TREO ở đỉnh, cắm xuống nhanh
            if u < 0.42:
                return 1 - (1 - u / 0.42) ** 2
            if u < 0.62:
                return 1.0
            return 1 - ((u - 0.62) / 0.38) ** 2

        def nhay(T):
            t0, t1 = t_bat, d_sk + t_cham
            if T <= t0:
                return 0.0, 0.0
            if T < t1:
                u = (T - t0) / (t1 - t0)
                ux = 1 - (1 - u) ** 1.5
                return to[0] * ux, to[1] * u + up * doc(u)
            v = (T - t1 - 0.16) / 0.42
            if v <= 0:
                return to
            if v >= 1:
                return 0.0, 0.0
            s = v * v * (3 - 2 * v)
            return to[0] * (1 - s), to[1] * (1 - s) + 0.4 * cao * 4 * v * (1 - v)

        seq = [(i / 30.0, P) for i, P in enumerate(a)] + [(d_sk + i / 30.0, P) for i, P in enumerate(b)]
        T_het = d_sk + t_cham + 0.16 + 0.42
        while seq[-1][0] < T_het + 0.3:
            seq.append((seq[-1][0] + 1 / 30.0, b[-1]))
        fr = []
        for T, P in seq:
            Q = P.copy()
            g = Q._g("move")
            ox, oy = nhay(T)
            g[0] += ox
            g[1] += oy
            fr.append(Q)
        Bx = soi._union([ve0.bao(P) for P in fr], 0.03)
        Bx = (min(Bx[0], X - 0.45 * cao), min(Bx[1], -10.0), max(Bx[2], X + 0.45 * cao), Bx[3])
        sc = min(0.8, (RONG * 1.6) / (Bx[2] - Bx[0]))
        ims = []
        for Q in fr:
            nen = ve0.ve(Q, Bx, sc, bg=NEN, ss=2).convert("RGB")
            # đối thủ giữ chỗ vẽ dưới tướng: dán tướng lên khung có khối xám
            khung = Image.new("RGB", nen.size, NEN)
            d = ImageDraw.Draw(khung)
            x0, x1 = (X - 0.32 * cao - Bx[0]) * sc, (X + 0.32 * cao - Bx[0]) * sc
            y0, y1 = (Bx[3] - H_DT * 0.62) * sc, (Bx[3] - 0.0) * sc
            d.rounded_rectangle([x0, y0, x1, y1], radius=int(0.12 * cao * sc), fill=(118, 118, 124), outline=(70, 70, 76), width=3)
            m = Image.eval(Image.fromarray(np.abs(np.asarray(nen).astype(int) - np.array(NEN)).sum(2).clip(0, 255).astype(np.uint8)),
                           lambda v: 255 if v > 6 else 0)
            khung.paste(nen, (0, 0), m)
            ims.append(khung)
        p = os.path.join(ra, "chieu_cuoi.webp")
        luu(ims, p, 1)
        print(f"chieu_cuoi: {len(ims)} khung {ims[0].size}, {os.path.getsize(p) // 1024} KB", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
