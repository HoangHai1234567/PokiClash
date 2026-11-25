# -*- coding: utf-8 -*-
"""Nổ nước khi trúng (một lượt ~0,9 s, 22 khung), bộ nước Blender (nuocbl.py), cùng ngôn ngữ hình với bông va chạm của tia nước:
chớp sao trắng 2 khung → sao gai lõm to bản (lớp sau lam giữa, lớp trước lam sáng, đổi dáng mỗi 2 khung) bung ra rồi mỏng dần và co →
vòng mảnh nước cuộn + giọt toả ra mọi phía rồi rơi → vài bọt nhỏ đọng. Dùng cho n_va (nước toé lúc lao / húc / quật tới), cầu nước vỡ,
đạn nước trúng. Neo tâm nổ.
    blender.exe -b --factory-startup --python no_nuoc_bl.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402
import nuocbl as W  # noqa: E402

OUT, FRAMES, SAVE = F.args()
N = 22
sc = F.reset(N)
rnd = W.rnd
BOT, SANG, CHINH = W.flat("Bot", "bot"), W.flat("Sang", "sang"), W.flat("Chinh", "chinh")
GIUA_M = W.flat("GiuaMo", "giua", 0.9)

# chớp: sao trắng 8 gai, hiện 2 khung
ch = F.flat_star("Chop", 8, 1.1, 0.42, W.C["bot"], y=0.0, center=(0, 0))
ch.location = (0, -1.0, 0)
ch.data.materials.clear()
ch.data.materials.append(BOT)
W.key_scale(ch, [(0, 0.5), (0.04, 1.25), (0.09, 0.9), (0.13, 0.0)])


def star_pts(scale):
    n = 7
    a0 = rnd.uniform(0, 360)
    return [(a0 + 360 * i / n + rnd.uniform(-14, 14), scale * rnd.uniform(1.4, 2.4)) for i in range(n)]


# sao gai bung: phồng nhanh tới 0,15 s, giữ, nở thêm chút rồi co mất ở 0,5 s
for li, (mat, sc_, y, rik) in enumerate(((GIUA_M, 1.0, -0.6, 0.34), (SANG, 0.74, -0.7, 0.42))):
    obs = []
    for v in range(3):
        ob = W.obj(f"Sao{li}_{v}", W.star_mesh(f"Sao{li}_{v}", star_pts(sc_), rik), mat, (0, y - 0.01 * v, 0), rnd.uniform(-10, 10))
        W.key_scale(ob, [(0, 0.0), (0.02, 0.3), (0.15, 1.05), (0.3, 1.15), (0.42, 0.75), (0.5, 0.0)])
        obs.append(ob)
    W.swap_keys(obs, 0.02, 0.5, 2)
loi = F.flat_star("Loi", 7, 0.85, 0.5, W.C["bot"], y=0.0, center=(0, 0))
loi.location = (0, -0.85, 0)
loi.data.materials.clear()
loi.data.materials.append(BOT)
W.key_scale(loi, [(0, 0.0), (0.03, 0.9), (0.14, 1.0), (0.3, 0.7), (0.42, 0.0)])

# vòng mảnh nước cuộn toả ra (có chấm sáng), rồi rơi
for k in range(14):
    a = math.radians(360 * k / 14 + rnd.uniform(-10, 10))
    v = rnd.uniform(3.2, 5.0)
    ob = W.obj(f"Cuon{k}", W.blob_mesh(f"Cuon{k}", rnd.choice((3, 4, 5)), rnd.uniform(0, W.TAU)), SANG if k % 3 else CHINH)
    hi = W.obj(f"CuonSang{k}", W.blob_mesh(f"CuonSang{k}", 3, rnd.uniform(0, W.TAU)), BOT)
    hi.parent = ob
    hi.location, hi.scale = (0.25, -0.02, 0.18), (0.42, 0.42, 0.42)
    W.ballistic(ob, (0.4 * math.cos(a), -0.9, 0.4 * math.sin(a)), (v * math.cos(a), v * math.sin(a) + 1.0), rnd.uniform(0.04, 0.1),
                rnd.uniform(0.42, 0.62), g=6.0, size=rnd.uniform(0.22, 0.34))

# giọt nhỏ
DR = (BOT, SANG, CHINH)
for k in range(26):
    a = math.radians(rnd.uniform(0, 360))
    v = rnd.uniform(2.6, 5.6)
    ob = W.drop(f"Giot{k}", DR[k % 3], 1)
    W.ballistic(ob, (0.3 * math.cos(a), -0.8, 0.3 * math.sin(a)), (v * math.cos(a), v * math.sin(a) + 1.2), rnd.uniform(0.03, 0.2),
                rnd.uniform(0.35, 0.6), g=7.0, size=rnd.uniform(0.06, 0.12), grow=(1.0, 0.0), align=False)

CAM = (0, -30, -0.5)
W.eevee(CAM, 360, 420, W.UPP)
F.run(OUT, "no_nuoc", CAM, W.UPP * 360, 360, 420, frames=FRAMES, save=SAVE, save_frame=4, anchor_xz=(0, 0))
