# -*- coding: utf-8 -*-
"""Ảnh động xem trước từng clip của rig quặng sắt (WebP lặp), vẽ bằng bộ vẽ Python của quai, kèm phần game làm (giả lập như game):
- attack, skill: sân nắn cú lao / đường đào tới 72 % quãng tới đối thủ (AolaSticker.Lunge: o = (k·R − I)·m);
- cast: tay bay trên xương fly_* được co quãng tới đối thủ và chĩa theo hướng bay thật (AolaActor.FarAtomik, farAim).
Đối thủ là khối xám giữ chỗ, đứng XA hơn chỗ mặc định trong rig để thấy code co quãng. Chỉ để xem trong máy (chuyển động gốc là của game
tham khảo). QS_GOC=1: bản da gốc tạm.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/inbox/quang_sat_1/_xem_dong.py [clip...]   → rig/dong/<clip>.webp
"""
import math
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
import quang_sat_rig as R  # noqa: E402
from quai import hoat, soi  # noqa: E402

NEN = (150, 150, 150)
RONG = 560
CACH = {"idle": (1, 2), "walk": (2, 1)}
X_DT = 1.9                                              # chân đối thủ cách chân mình (× chiều cao)
H_DT = 0.95                                             # chiều cao đối thủ (× chiều cao)


def luu(ims, p, buoc):
    ims[0].save(p, save_all=True, append_images=ims[1:], duration=int(round(1000 * buoc / 30)), loop=0, quality=74, method=4,
                minimize_size=True)


def lunge(sk, fr, cao):
    """như AolaSticker.Lunge: dời đỉnh của xương move tới 72 % quãng tới đối thủ; trả độ lệch thêm của từng khung."""
    m = np.array([sk.the_gioi(P)["move"][:2, 2] for P in fr])
    m = m - m[0]
    # làm mượt 5 khung như AtomikMotion
    ms = np.array([m[max(0, i - 2):i + 3].mean(0) for i in range(len(m))])
    pk = ms[int(np.argmax(np.hypot(*ms.T)))]
    M = float(np.hypot(*pk))
    if M <= 1e-6:
        return np.zeros_like(m)
    tx, ty = 0.72 * X_DT * cao, 0.0
    k = math.hypot(tx, ty) / M
    ang = math.atan2(ty, tx) - math.atan2(pk[1], pk[0])
    cs, sn = math.cos(ang) * k, math.sin(ang) * k
    return np.stack([m[:, 0] * cs - m[:, 1] * sn - m[:, 0], m[:, 0] * sn + m[:, 1] * cs - m[:, 1]], 1)


def far_atomik(sk, P, cao):
    """như AolaActor.FarAtomik: far tới giữa thân đối thủ; fly_* dời theo phần quãng đã bay (x); xương con chĩa theo hướng bay thật."""
    Q = P.copy()
    fb = sk.W0["far"][:2, 2]
    dich = np.array([X_DT * cao, 0.45 * H_DT * cao])
    o = dich - fb
    g = Q._g("far")
    g[0] += o[0]
    g[1] += o[1]
    for b in [x["name"] for x in sk.bones if x["name"].startswith("fly")]:
        x0 = sk.W0[b][0, 2]
        span = fb[0] - x0
        lx = x0 + Q.t.get(b, [0, 0, 0, 1, 1])[0]
        w = min(1.0, max(0.0, (lx - x0) / span)) if span > 1 else 1.0
        gb = Q._g(b)
        gb[0] += o[0] * w
        gb[1] += o[1] * w
        A = sk.W0[b][:2, 2]
        a0 = math.atan2(fb[1] - A[1], fb[0] - A[0])
        a1 = math.atan2(fb[1] + o[1] - A[1], fb[0] + o[0] - A[0])
        f = min(1.0, max(0.0, w / 0.22))
        f = f * f * (3 - 2 * f)
        for c in [x["name"] for x in sk.bones if x["parent"] == b]:
            d = (math.degrees(a1 - a0) + 180.0) % 360.0 - 180.0
            Q._g(c)[2] += d * f
    return Q


def ve_khung(ve0, fr, cao, doi=None, rong=RONG):
    Bx = soi._union([ve0.bao(P) for P in fr], 0.03)
    if doi:
        Bx = (min(Bx[0], -0.9 * cao), min(Bx[1], -20.0), max(Bx[2], (X_DT + 0.45) * cao), max(Bx[3], 1.1 * cao))
    sc = min(0.8, rong / (Bx[2] - Bx[0]))
    ims = []
    for P in fr:
        nen = ve0.ve(P, Bx, sc, bg=NEN, ss=2).convert("RGB")
        if doi:
            khung = Image.new("RGB", nen.size, NEN)
            d = ImageDraw.Draw(khung)
            x0, x1 = ((X_DT - 0.32) * cao - Bx[0]) * sc, ((X_DT + 0.32) * cao - Bx[0]) * sc
            y0, y1 = (Bx[3] - H_DT * cao * 0.75) * sc, (Bx[3] - 0.0) * sc
            d.rounded_rectangle([x0, y0, x1, y1], radius=int(0.12 * cao * sc), fill=(118, 118, 124), outline=(70, 70, 76), width=3)
            yd = (Bx[3] - 0.0) * sc
            d.line([0, yd, khung.width, yd], fill=(128, 128, 128), width=2)
            m = Image.eval(Image.fromarray(np.abs(np.asarray(nen).astype(int) - np.array(NEN)).sum(2).clip(0, 255).astype(np.uint8)),
                           lambda v: 255 if v > 6 else 0)
            khung.paste(nen, (0, 0), m)
            nen = khung
        ims.append(nen)
    return ims


def main(chi):
    sk, info = R.dung()
    ve0 = soi.Ve(sk)
    clips, than_cast = R.lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    R.them_tay_bay(sk, info, than_cast, cao)
    ve0 = soi.Ve(sk)
    clips, _ = R.lam_clip(sk, info, cao)
    ra = os.path.join(R.RA, "dong")
    os.makedirs(ra, exist_ok=True)
    for c in clips:
        if chi and c.ten not in chi:
            continue
        t0 = time.time()
        fr = R.nuong(sk, c)
        vong, buoc = CACH.get(c.ten, (1, 1))
        if c.loop and len(fr) == int(round(c.dur * 30)) + 1:
            fr = fr[:-1]
        doi = c.ten in ("attack", "skill", "cast")
        if c.ten in ("attack", "skill"):
            o = lunge(sk, fr, cao)
            fr = [P.copy() for P in fr]
            for P, d in zip(fr, o):
                g = P._g("move")
                g[0] += float(d[0])
                g[1] += float(d[1])
        elif c.ten == "cast":
            fr = [far_atomik(sk, P, cao) for P in fr]
        fr = (fr * vong)[::buoc]
        if not c.loop:
            fr = fr + [fr[-1]] * (12 // buoc)
        ims = ve_khung(ve0, fr, cao, doi, RONG * (1.6 if doi else 1.0))
        p = os.path.join(ra, c.ten + ".webp")
        luu(ims, p, buoc)
        print(f"{c.ten}: {len(ims)} khung {ims[0].size}, {os.path.getsize(p) // 1024} KB, {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
