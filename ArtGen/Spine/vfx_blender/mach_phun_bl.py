# -*- coding: utf-8 -*-
"""Xoáy nước rồi MẠCH PHUN (một lượt 1,6 s, 38 khung), bộ nước Blender (nuocbl.py): 0–0,45 s xoáy nước dưới chân (hai nhánh xoắn ốc
dẹt trên đất, quay nhanh dần) → 0,42 s cột nước phun vọt lên (ống nước đứng, vệt lam chảy NGƯỢC lên), bông nước gai ở đỉnh cột và ở chân,
mảnh nước cuộn + giọt văng từ đỉnh rơi xuống → 1,1 s cột sụp xuống, bông chân bung lần cuối, xoáy tan. Dùng cho n_xoay (trồi lên dưới
chân đối thủ). Neo chân cột (0, 0), trên mặt đất.
    blender.exe -b --factory-startup --python mach_phun_bl.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import math
import os
import sys

import bmesh
import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402
import nuocbl as W  # noqa: E402

OUT, FRAMES, SAVE = F.args()
N = 38
sc = F.reset(N)
TAU = W.TAU
rnd = W.rnd
BOT, SANG, CHINH = W.flat("Bot", "bot"), W.flat("Sang", "sang"), W.flat("Chinh", "chinh")
GIUA_M, SANG_M = W.flat("GiuaMo", "giua", 0.85), W.flat("SangMo", "sang", 0.8)

# ---- xoáy nước dưới đất: hai nhánh xoắn ốc phẳng (mặt XZ) trong một Empty dẹt theo z (nhìn ngang thành elip nằm trên đất)
xo_det = F.empty("XoayDet", loc=(0, -0.2, 0.05), scale=(1, 1, 0.28))   # cha ép dẹt (elip trên đất)
xo = F.empty("Xoay")                                                    # con quay bên trong: nhánh quay trong elip cố định
xo.parent = xo_det


def spiral(name, ph, turns=1.6, r0=0.15, r1=1.7, w0=0.06, w1=0.32, n=90):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    a_, b_ = [], []
    for i in range(n + 1):
        u = i / n
        th = ph + TAU * turns * u
        r = r0 + (r1 - r0) * u
        w = w0 + (w1 - w0) * math.sin(math.pi * min(1, u * 1.2)) ** 0.7
        a_.append(bm.verts.new(((r + w / 2) * math.cos(th), 0, (r + w / 2) * math.sin(th))))
        b_.append(bm.verts.new(((r - w / 2) * math.cos(th), 0, (r - w / 2) * math.sin(th))))
    for i in range(n):
        bm.faces.new((b_[i], b_[i + 1], a_[i + 1], a_[i]))
    bm.to_mesh(me)
    bm.free()
    return me


nhanh = []
for k, (ph, mat) in enumerate(((0, GIUA_M), (math.pi, SANG_M), (math.pi / 2, BOT))):
    ob = W.link(bpy.data.objects.new(f"Nhanh{k}", spiral(f"Nhanh{k}", ph, w1=(0.32, 0.26, 0.12)[k])))
    ob.data.materials.append(mat)
    ob.parent = xo
    ob.location = (0, -0.01 * k, 0)
    nhanh.append(ob)
    W.key_scale(ob, [(0, 0.0), (0.12, 0.7), (0.4, 1.0), (1.0, 1.05), (1.35, 0.6), (1.5, 0.0)])
for t, a in ((0, 0.0), (0.45, -2.2 * TAU), (1.5, -6.5 * TAU)):          # quay nhanh dần
    xo.rotation_euler[1] = -a
    xo.keyframe_insert("rotation_euler", index=1, frame=F.fr(t))

# ---- cột nước: ống đứng bán kính r, cao h(t); vệt chảy NGƯỢC lên (trượt toạ độ theo −z)
truc = F.empty("Truc")
MAT = W.flow_mat("Cot", truc, scale=(2.6, 2.6, 0.13), move=(1.6, (0, 0, -2.6)), hi_axis="X", hi_th=0.82, rim_th=0.76)


def cyl_z(name, seg=36, rings=20):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rows = [[bm.verts.new((math.cos(TAU * j / seg), math.sin(TAU * j / seg), i / rings)) for j in range(seg)] for i in range(rings + 1)]
    for i in range(rings):
        for j in range(seg):
            bm.faces.new((rows[i][j], rows[i][(j + 1) % seg], rows[i + 1][(j + 1) % seg], rows[i + 1][j]))
    bm.to_mesh(me)
    bm.free()
    return W.smooth(me)


COT = [(0.0, 0.0, 0.0), (0.42, 0.0, 0.3), (0.5, 2.6, 0.62), (0.58, 4.4, 0.55), (0.7, 4.0, 0.5), (0.82, 4.3, 0.53), (0.95, 4.05, 0.5),
       (1.08, 4.2, 0.48), (1.22, 2.6, 0.42), (1.34, 1.0, 0.34), (1.42, 0.2, 0.2), (1.46, 0.0, 0.0)]
cot = W.link(bpy.data.objects.new("Cot", cyl_z("Cot")))
cot.data.materials.append(MAT)
dau = W.link(bpy.data.objects.new("DauCot", W.sphere("DauCot")))
dau.data.materials.append(MAT)
for t, h, r in COT:
    f = F.fr(t)
    cot.scale = (max(1e-3, r), max(1e-3, r), max(1e-3, h))
    dau.location, dau.scale = (0, 0, h), (max(1e-3, r * 1.12),) * 3
    for ob in (cot, dau):
        ob.keyframe_insert("scale", frame=f)
    dau.keyframe_insert("location", frame=f)


def h_at(t):
    for (ta, ha, ra), (tb, hb, rb) in zip(COT, COT[1:]):
        if ta <= t <= tb:
            k = (t - ta) / max(1e-6, tb - ta)
            return ha + (hb - ha) * k, ra + (rb - ra) * k
    return 0.0, 0.0


def star_pts(scale, a_lo, a_hi, n):
    return [(a_lo + (a_hi - a_lo) * (i + 0.5) / n + rnd.uniform(-10, 10), scale * rnd.uniform(1.1, 2.0)) for i in range(n)] + \
        [(270 + rnd.uniform(-20, 20), scale * 0.5)]


# ---- bông nước ở đỉnh cột (gai toả lên và sang hai bên), đi theo đỉnh; bông ở chân (gai xoè lên hai bên)
def splash_set(name, a_lo, a_hi, n, sc_, t0, t1, follow, base_z=0.0):
    for li, (mat, s2, y, rik) in enumerate(((GIUA_M, 1.0, -0.65, 0.34), (SANG, 0.72, -0.72, 0.42))):
        obs = []
        for v in range(3):
            ob = W.obj(f"{name}{li}_{v}", W.star_mesh(f"{name}{li}_{v}", star_pts(sc_ * s2, a_lo, a_hi, n), rik), mat, (0, y - 0.01 * v, base_z))
            obs.append(ob)
            pairs = [(0, 0.0), (t0, 0.0), (t0 + 0.06, 1.1)]
            t = t0 + 0.06
            while t < t1 - 0.1:
                t += 0.1 + rnd.uniform(-0.02, 0.02)
                pairs.append((t, rnd.uniform(0.8, 1.1)))
            pairs += [(t1, 0.0)]
            W.key_scale(ob, pairs)
            if follow:
                for tt in [t0 + i * (t1 - t0) / 16 for i in range(17)]:
                    hh, _ = h_at(tt)
                    ob.location = (0, y - 0.01 * v, hh + 0.1)
                    ob.keyframe_insert("location", frame=F.fr(tt))
        W.swap_keys(obs, t0, t1, 2)


splash_set("Dinh", 15, 165, 6, 1.0, 0.46, 1.3, True)
splash_set("Chan", 20, 160, 5, 0.75, 0.4, 1.5, False, 0.05)

# ---- mảnh nước cuộn + giọt văng từ đỉnh, rơi xuống
for k in range(16):
    t0 = rnd.uniform(0.5, 1.15)
    hh, _ = h_at(t0)
    a = math.radians(rnd.uniform(25, 155))
    v = rnd.uniform(2.6, 4.2)
    ob = W.obj(f"Cuon{k}", W.blob_mesh(f"Cuon{k}", rnd.choice((3, 4, 5)), rnd.uniform(0, TAU)), SANG if k % 3 else CHINH)
    hi = W.obj(f"CuonSang{k}", W.blob_mesh(f"CuonSang{k}", 3, rnd.uniform(0, TAU)), BOT)
    hi.parent = ob
    hi.location, hi.scale = (0.25, -0.02, 0.18), (0.42, 0.42, 0.42)
    W.ballistic(ob, (0, -0.9, hh), (v * math.cos(a), v * math.sin(a)), t0, rnd.uniform(0.5, 0.75), g=7.0, size=rnd.uniform(0.18, 0.28))
DR = (BOT, SANG, CHINH)
for k in range(28):
    t0 = rnd.uniform(0.45, 1.3)
    hh, _ = h_at(t0)
    a = math.radians(rnd.uniform(20, 160))
    v = rnd.uniform(2.0, 4.6)
    ob = W.drop(f"Giot{k}", DR[k % 3], 1)
    W.ballistic(ob, (rnd.uniform(-0.2, 0.2), -0.8, hh), (v * math.cos(a), v * math.sin(a)), t0, rnd.uniform(0.45, 0.7), g=8.0,
                size=rnd.uniform(0.05, 0.1), grow=(1.0, 0.0), align=False)

CAM = (0, -30, 2.95)
W.eevee(CAM, 280, 384, W.UPP)
F.run(OUT, "mach_phun", CAM, W.UPP * 280, 280, 384, frames=FRAMES, save=SAVE, save_frame=16, anchor_xz=(0, 0))
