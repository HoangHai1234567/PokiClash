# -*- coding: utf-8 -*-
"""Cầu nước (lặp 24 khung = 1 s), bộ nước Blender cùng màu tia nước (nuocbl.py): mặt cầu là nước chảy (vệt thấu kính lam xoay quanh
trục đứng, mép phập phồng), ba dòng nước xoáy (cung hở thon đuôi, mép rách) quay quanh trên các quỹ đạo nghiêng, bong bóng trắng trôi trong cầu, giọt bắn ra PHÍA SAU
(cầu bay sang PHẢI); cầu nhỏ giọt: 5 cục nước rời đuôi, tan lấm tấm (học repo water_vfx). Dùng cho chiêu n_cau (ợ cầu nước), đạn nước n_dan, ngọc trai n_ngoc. Neo tâm cầu.
    blender.exe -b --factory-startup --python cau_nuoc_bl.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
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
N = 24
P = N / F.FPS
sc = F.reset(N)
TAU = W.TAU
rnd = W.rnd

truc = F.empty("Truc")
MAT = W.flow_mat("CauNuoc", truc, scale=(0.55, 0.55, 2.6), spin=(P, 2, 1), hi_axis="Z", hi_th=0.8, rim_th=0.74, noise_scale=1.4)
ball = W.link(bpy.data.objects.new("Cau", W.sphere("Cau", 48, 24)))
ball.data.materials.append(MAT)
ball.modifiers.new("Min", "SUBSURF").levels = 1
rip = F.empty("Ripple")
F.keys(rip, "rotation_euler", [(0, 0.0), (P, TAU)], 2)
tex = bpy.data.textures.new("Gon", "CLOUDS")
tex.noise_scale = 0.9
d = ball.modifiers.new("Phong", "DISPLACE")
d.texture, d.texture_coords, d.texture_coords_object, d.strength, d.mid_level = tex, "OBJECT", rip, 0.16, 0.5


def arc_mesh(name, R, wd, span_deg, n=80):
    """Dòng nước xoáy (người dùng: "vòng nước xung quanh chưa đẹp" — bỏ vòng tròn đều như vành sao Thổ): cung HỞ span_deg độ, thon từ
    đuôi (mảnh như sợi) tới đầu (dày, tròn), bán kính tăng nhẹ về đầu (xoắn ốc), UV u dọc cung, v ngang dải."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    a_, b_ = [], []
    span = math.radians(span_deg)
    for i in range(n + 1):
        u = i / n
        t = span * u
        w = wd * (u ** 0.8) * (1 - u ** 6) ** 0.5 + 0.01          # đuôi mảnh → đầu dày, mũi tròn
        r = R + 0.14 * u
        a_.append(bm.verts.new(((r + w / 2) * math.cos(t), (r + w / 2) * math.sin(t), 0)))
        b_.append(bm.verts.new(((r - w / 2) * math.cos(t), (r - w / 2) * math.sin(t), 0)))
    for i in range(n):
        f = bm.faces.new((b_[i], b_[i + 1], a_[i + 1], a_[i]))
        for lp, (u, v) in zip(f.loops, ((i / n, 0), ((i + 1) / n, 0), ((i + 1) / n, 1), (i / n, 1))):
            lp[uv].uv = (u, v)
    bm.to_mesh(me)
    bm.free()
    return me


def torn_mat(name, key, alpha, seed):
    """Trong mờ, mép rách (nhiễu theo UV cộng độ gần giữa dải), đứt khúc theo u."""
    m, nt, L_ = W.new_mat(name)
    tc = W.node(nt, "ShaderNodeTexCoord", (-900, 0))
    sp = W.node(nt, "ShaderNodeSeparateXYZ", (-700, 0))
    L_.new(tc.outputs["UV"], sp.inputs["Vector"])
    nz = W.node(nt, "ShaderNodeTexNoise", (-700, -250))
    nz.noise_dimensions = "4D"
    nz.inputs["Scale"].default_value = 7.0
    nz.inputs["W"].default_value = seed
    L_.new(tc.outputs["UV"], nz.inputs["Vector"])
    dv = W.node(nt, "ShaderNodeMath", (-500, 100), operation="SUBTRACT")
    L_.new(sp.outputs["Y"], dv.inputs[0])
    dv.inputs[1].default_value = 0.5
    av = W.node(nt, "ShaderNodeMath", (-350, 100), operation="ABSOLUTE")
    L_.new(dv.outputs[0], av.inputs[0])
    inv = W.node(nt, "ShaderNodeMath", (-200, 100), operation="SUBTRACT")
    inv.inputs[0].default_value = 0.5
    L_.new(av.outputs[0], inv.inputs[1])
    s = W.node(nt, "ShaderNodeMath", (-50, 0), operation="MULTIPLY_ADD")
    L_.new(inv.outputs[0], s.inputs[0])
    s.inputs[1].default_value = 1.6
    L_.new(nz.outputs["Fac"], s.inputs[2])
    keep = W.node(nt, "ShaderNodeMath", (100, 0), operation="GREATER_THAN")
    L_.new(s.outputs[0], keep.inputs[0])
    keep.inputs[1].default_value = 0.66
    a = W.node(nt, "ShaderNodeMath", (300, 0), operation="MULTIPLY")
    L_.new(keep.outputs[0], a.inputs[0])
    a.inputs[1].default_value = alpha
    rgb = W.node(nt, "ShaderNodeRGB", (600, 200))
    rgb.outputs[0].default_value = F.lin(W.C[key])
    W.out_alpha(m, nt, L_, rgb.outputs[0], a.outputs[0])
    return m


# 3 dòng nước xoáy trên các quỹ đạo nghiêng khác nhau, quay vòng (số vòng nguyên mỗi chu kỳ → lặp liền), đi trước rồi ra SAU cầu
# quỹ đạo gần nằm ngang (tilt quanh x 24–32°, tỉ lệ elip ≈ sin tilt ≈ 0,4–0,5) → elip: nửa dưới đi TRƯỚC cầu, nửa trên khuất SAU; yaw quanh trục nhìn → elip chéo
# (2026-11-24: thử thay bằng nước bắn quanh viền, người dùng xem xong bảo "cầu nước để lại bản cũ" → giữ dòng xoáy)
DONG = [(1.42, 0.36, 235, 24, 22, 1, "sang", 0.9), (1.34, 0.26, 200, 156, -30, 1, "bot", 0.92), (1.52, 0.2, 165, 32, 68, 2, "chinh", 0.8)]
for k, (R, wd, span, tilt, yaw, turns, key, al) in enumerate(DONG):
    ob = W.link(bpy.data.objects.new(f"Vong{k}", arc_mesh(f"Vong{k}", R, wd, span)))
    ob.data.materials.append(torn_mat(f"VongMat{k}", key, al, 1.7 + k))
    ob.rotation_euler = (math.radians(tilt), math.radians(yaw), 0)
    ob.rotation_mode = "XYZ"
    for t, a in ((0, 0.0), (P, turns * TAU)):
        ob.delta_rotation_euler = (0, 0, a)
        ob.keyframe_insert("delta_rotation_euler", index=2, frame=F.fr(t))

# bong bóng trắng trôi trong cầu (đĩa phẳng trước mặt cầu), vòng tròn kín mỗi chu kỳ
BOT = W.flat("BotCau", "bot")
for k in range(5):
    b = W.obj(f"Bong{k}", W.flat_poly(f"Bong{k}", [(math.cos(TAU * i / 20), math.sin(TAU * i / 20)) for i in range(20)]), BOT)   # bong bóng tròn
    r0, a0, sz = rnd.uniform(0.25, 0.6), rnd.uniform(0, TAU), rnd.uniform(0.06, 0.12)
    for i in range(9):
        t = P * i / 8
        a = a0 + TAU * i / 8 * (1 if k % 2 else -1)
        b.location = (r0 * math.cos(a) * 0.9, -1.12, r0 * math.sin(a) * 0.8)
        s = sz * (0.8 + 0.2 * math.sin(TAU * i / 8 * 2 + k))
        b.scale = (s, s, s)
        b.keyframe_insert("location", frame=F.fr(t))
        b.keyframe_insert("scale", frame=F.fr(t))

# giọt bắn ra sau (−x), lệch pha đều để lặp liền: mỗi giọt bay đúng một chu kỳ rồi lặp lại từ đầu
DR = (W.flat("GiotBot", "bot"), W.flat("GiotSang", "sang"), W.flat("GiotChinh", "chinh"))
for k in range(12):
    ob = W.drop(f"Giot{k}", DR[k % 3], 1)
    ph = k / 12
    a0 = rnd.uniform(-60, 60)
    sp = rnd.uniform(1.4, 2.4)
    sz = rnd.uniform(0.05, 0.1)
    p0 = (-0.9 * math.cos(math.radians(a0)), -0.3, 0.9 * math.sin(math.radians(a0)))
    for i in range(13):
        q = (i / 12 + ph) % 1.0
        t = P * i / 12
        ob.location = (p0[0] - sp * q, p0[1], p0[2] + 0.6 * math.sin(math.radians(a0)) * q - 0.6 * q * q)
        s = sz * (1 - q) ** 0.7
        ob.scale = (s * 1.4, s, s)
        ob.keyframe_insert("location", frame=F.fr(t))
        ob.keyframe_insert("scale", frame=F.fr(t))

# cầu NHỎ GIỌT khi bay (học repo abitofgamedev/water_vfx — WaterBall: hệ hạt cầu nhỏ 10/giây, cỡ 0,64 → 0,26, trọng lực nhẹ; tan lấm
# tấm theo ngưỡng trên nhiễu mịn): 5 cục nước rời đuôi cầu, lùi ra sau, rơi nhẹ, nhỏ dần, tan lấm tấm. Khoá MỖI KHUNG (lệch pha k/5,
# quay vòng đúng một chu kỳ) → lặp liền; chỗ quay vòng nằm giữa hai khung nên không lộ nội suy.
for k in range(5):
    ph = k / 5
    z0 = rnd.uniform(-0.35, 0.35)
    back = rnd.uniform(1.3, 1.8)
    s0 = rnd.uniform(0.34, 0.44)
    thr = []
    blob_ = W.link(bpy.data.objects.new(f"NhoGiot{k}", W.uv_sphere(f"NhoGiot{k}", 24, 12)))
    for i in range(N + 1):
        q = (i / N + ph) % 1.0
        t = P * i / N
        blob_.location = (-0.75 - back * q, 0.15, z0 * (1 - 0.3 * q) - 0.35 * q * q)
        sz = s0 * (1 - 0.68 * q)
        blob_.scale = (sz * (1.25 - 0.25 * q), sz, sz)
        blob_.keyframe_insert("location", frame=F.fr(t))
        blob_.keyframe_insert("scale", frame=F.fr(t))
        thr.append((t, 0.04 + 0.9 * q ** 1.6))
    blob_.data.materials.append(W.mask_mat(f"NhoGiotM{k}", f"dac_{k % 3}", thr, key="chinh", inner=(0.55, "sang"), rim=(0.05, "bot"),
                                           tiling=(2.0, 1.0), noise_scale=30.0, nk=0.85))

CAM = (-0.6, -30, -0.25)
W.eevee(CAM, 240, 196, W.UPP)
F.run(OUT, "cau_nuoc", CAM, W.UPP * 240, 240, 196, frames=FRAMES, save=SAVE, save_frame=1, loop=True, anchor_xz=(0, 0))
