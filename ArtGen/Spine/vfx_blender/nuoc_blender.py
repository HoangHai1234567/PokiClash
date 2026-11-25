# -*- coding: utf-8 -*-
"""Tia nước bắn (1,5 s, 36 khung) theo clip mẫu người dùng đưa (C:/Users/ADMIN/Videos/water.mp4, 0–1,4 s; 2026-11-24):
1. 0–0,12 s: tia MẢNH lao từ miệng tới đích (bông toé nhỏ ở miệng);
2. 0,16–0,3 s: tia PHÌNH thành ống nước dày đầu tròn (vượt cỡ rồi về), vài tấm nước lớn xoè ra như cánh quạt rồi tan;
3. giữ ~0,8 s: vệt lam đậm gợn sóng TRÔI dọc ống (shader nhiễu kéo dài theo trục, trượt theo giờ), hai dải nước xoắn ốc quấn quanh,
   bông nước gai nhọn ở đích đập theo nhịp (toé NGƯỢC về người bắn + vài vệt xuyên ra sau đích), giọt bắn;
4. 1,1–1,46 s: đuôi tia rời miệng, bay nốt vào đích, mảnh dần rồi hết — đuôi TAN RÁCH theo ngưỡng (hai ngưỡng dọc trục, beam_mat).
Luật dự án: không phát sáng / bloom, màu phẳng 4 tông lam + bọt trắng (skill vfx-petclash mục 1c), dải xoắn / tấm quạt trong mờ ~0,8.
Eevee (cần alpha), Emission 1, View Standard, nền trong. Tia nằm ngang, miệng ở gốc (0, 0), đích ở x = L, bắn sang PHẢI.
    blender.exe -b --factory-startup --python nuoc_blender.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import math
import os
import random
import sys

import bmesh
import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402

OUT, FRAMES, SAVE = F.args()
_a = sys.argv[sys.argv.index("--") + 1:]
PHAN = _a[_a.index("--phan") + 1] if "--phan" in _a else "all"   # all | tia (tia + bông toé miệng) | trung (va chạm ở đích)
N = 36
sc = F.reset(N)
L = 10.0
TAU = 2 * math.pi
rnd = random.Random(5)
# chỉ xanh dương, đo từ tia gốc (k-means khung giữ tia): sáng #64F8FA/#49D8F4, giữa #3EB1E0, đậm #378EB8 (bỏ ngọc lam / lục của bản 1)
C = dict(bot="#EAFBFF", sang="#93E8FF", chinh="#4FCDF6", giua="#3AA8E4", dam="#2A7BC8", sau="#1F5BAA")
truc = F.empty("Truc")   # hệ toạ độ chung của mọi mảnh ống (vân liền qua chỗ nối thân / đầu tròn)

# ---------------------------------------------------------------- nhịp ống: (giờ, x đuôi, x đầu, bán kính)
BEAM = [(0.0, 0.0, 0.3, 0.05), (0.1, 0.0, L, 0.07), (0.16, 0.0, L, 0.1), (0.22, 0.0, L, 0.5), (0.27, 0.0, L, 0.68), (0.34, 0.0, L, 0.53),
        (0.5, 0.0, L, 0.57), (0.66, 0.0, L, 0.51), (0.82, 0.0, L, 0.57), (0.98, 0.0, L, 0.52), (1.1, 0.0, L, 0.55), (1.2, 1.3, L, 0.47),
        (1.32, 5.6, L, 0.36), (1.42, 9.4, L, 0.22), (1.46, L - 0.05, L, 0.04), (1.5, L, L, 0.0)]


def node(nt, kind, loc=(0, 0), **props):
    n = nt.nodes.new(kind)
    n.location = loc
    for k, v in props.items():
        setattr(n, k, v)
    return n


def new_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes.clear()
    return m, m.node_tree, m.node_tree.links


def out_alpha(nt, L_, color_socket, alpha_socket=None, alpha=1.0):
    """Emission (màu từ socket) trộn Transparent theo alpha."""
    o = node(nt, "ShaderNodeOutputMaterial", (1200, 0))
    e = node(nt, "ShaderNodeEmission", (900, 80))
    e.inputs["Strength"].default_value = 1.0
    L_.new(color_socket, e.inputs["Color"])
    if alpha_socket is None and alpha >= 1:
        L_.new(e.outputs[0], o.inputs["Surface"])
        return
    for m in bpy.data.materials:           # trong mờ mịn (mặc định Eevee là dither → lấm tấm hạt nhiễu)
        if m.node_tree == nt:
            m.surface_render_method = "BLENDED"
    mx = node(nt, "ShaderNodeMixShader", (1050, 0))
    tr = node(nt, "ShaderNodeBsdfTransparent", (900, -80))
    if alpha_socket is not None:
        L_.new(alpha_socket, mx.inputs["Fac"])
    else:
        mx.inputs["Fac"].default_value = alpha
    L_.new(tr.outputs[0], mx.inputs[1])
    L_.new(e.outputs[0], mx.inputs[2])
    L_.new(mx.outputs[0], o.inputs["Surface"])


def ramp(nt, loc, stops):
    r = node(nt, "ShaderNodeValToRGB", loc)
    r.color_ramp.interpolation = "CONSTANT"
    els = r.color_ramp.elements
    while len(els) < len(stops):
        els.new(0.5)
    for el, (pos, hexc) in zip(els, stops):
        el.position, el.color = pos, F.lin(hexc)
    return r


def flat(name, hexc, alpha=1.0):
    m, nt, L_ = new_mat(name)
    rgb = node(nt, "ShaderNodeRGB", (600, 0))
    rgb.outputs[0].default_value = F.lin(hexc)
    out_alpha(nt, L_, rgb.outputs[0], alpha=alpha)
    return m


def keyed_value(nt, loc, pairs):
    v = node(nt, "ShaderNodeValue", loc)
    for t, val in pairs:
        v.outputs[0].default_value = val
        v.outputs[0].keyframe_insert("default_value", frame=F.fr(t))
    return v.outputs[0]


# ---------------------------------------------------------------- vật liệu ống nước
def beam_mat():
    m, nt, L_ = new_mat("Nuoc")
    tc = node(nt, "ShaderNodeTexCoord", (-900, 0))
    tc.object = truc
    mp = node(nt, "ShaderNodeMapping", (-700, 0))
    mp.inputs["Scale"].default_value = (0.11, 3.6, 3.6)       # kéo rất dài theo trục → vệt thấu kính dài, mảnh như tia gốc
    for t, x in ((0, 0.0), (1.5, -2.4)):              # vân trôi sang +x (theo dòng nước)
        mp.inputs["Location"].default_value[0] = x
        mp.inputs["Location"].keyframe_insert("default_value", index=0, frame=F.fr(t))
    nz = node(nt, "ShaderNodeTexNoise", (-500, 0))
    nz.inputs["Scale"].default_value = 1.2
    nz.inputs["Detail"].default_value = 0.0
    nz.inputs["Distortion"].default_value = 0.25
    L_.new(tc.outputs["Object"], mp.inputs["Vector"])
    L_.new(mp.outputs["Vector"], nz.inputs["Vector"])
    # vân: đậm (hiếm) → lam → ngọc → lam nhạt (nền) → bọt trắng (lấm tấm)
    # vệt đậm (lõi lam đậm, viền giữa, mép sáng mảnh) trên nền lam chính; vệt nhạt ở phía trên
    rv = ramp(nt, (-250, 0), [(0.0, C["dam"]), (0.31, C["giua"]), (0.37, C["sang"]), (0.39, C["chinh"]), (0.64, C["sang"]), (0.76, C["bot"])])
    L_.new(nz.outputs["Fac"], rv.inputs["Fac"])
    # vệt sáng dọc mặt trên (pháp tuyến hướng lên) và viền ở mép bóng (Layer Weight facing)
    geo = node(nt, "ShaderNodeNewGeometry", (-500, -300))
    sp = node(nt, "ShaderNodeSeparateXYZ", (-300, -300))
    L_.new(geo.outputs["Normal"], sp.inputs["Vector"])
    hi = node(nt, "ShaderNodeMath", (-100, -300), operation="GREATER_THAN")
    hi.inputs[1].default_value = 0.86
    L_.new(sp.outputs["Z"], hi.inputs[0])
    lw = node(nt, "ShaderNodeLayerWeight", (-300, -500))
    lw.inputs["Blend"].default_value = 0.5
    rim = node(nt, "ShaderNodeMath", (-100, -500), operation="GREATER_THAN")
    rim.inputs[1].default_value = 0.78
    L_.new(lw.outputs["Facing"], rim.inputs[0])
    m1 = node(nt, "ShaderNodeMixRGB", (150, 0), blend_type="MIX")
    L_.new(hi.outputs[0], m1.inputs["Fac"])
    L_.new(rv.outputs["Color"], m1.inputs["Color1"])
    m1.inputs["Color2"].default_value = F.lin(C["bot"])
    m2 = node(nt, "ShaderNodeMixRGB", (350, 0), blend_type="MIX")
    L_.new(rim.outputs[0], m2.inputs["Fac"])
    L_.new(m1.outputs["Color"], m2.inputs["Color1"])
    m2.inputs["Color2"].default_value = F.lin(C["sang"])   # mép ống SÁNG như tia gốc
    # HAI NGƯỠNG dọc trục (học tia ống của repo abitofgamedev/water_vfx; người dùng 2026-11-24 "làm cả đi"): m = x + (vân − 0,5)·1,6
    # (vân kéo dài theo trục → mép rách thành sợi dọc dòng); hiện khi ngưỡng_đuôi < m < ngưỡng_đầu. Ngưỡng đuôi nằm ngoài miệng (−0,9)
    # lúc đang nhả rồi quét qua cả ống khi đuôi rời miệng (1,1 → 1,46 s): đuôi tan rách từ miệng thay vì cắt tròn; ngưỡng đầu = đầu ống
    # + 0,9 (chỉ cắt lúc tia mảnh đang lao tới → đầu tia rách bọt).
    pos = node(nt, "ShaderNodeSeparateXYZ", (-700, -800))
    L_.new(tc.outputs["Object"], pos.inputs["Vector"])
    mm = node(nt, "ShaderNodeMath", (-300, -800), operation="MULTIPLY_ADD")
    L_.new(nz.outputs["Fac"], mm.inputs[0])
    mm.inputs[1].default_value = 1.6
    L_.new(pos.outputs["X"], mm.inputs[2])
    mm2 = node(nt, "ShaderNodeMath", (-150, -800), operation="ADD")
    L_.new(mm.outputs[0], mm2.inputs[0])
    mm2.inputs[1].default_value = -0.8
    x0k = keyed_value(nt, (-300, -1000), [(t, (a - 0.9) if a <= 0 else a) for t, a, b, r in BEAM])
    x1k = keyed_value(nt, (-300, -1100), [(t, b + 0.9) for t, a, b, r in BEAM])
    g0 = node(nt, "ShaderNodeMath", (0, -900), operation="GREATER_THAN")
    L_.new(mm2.outputs[0], g0.inputs[0])
    L_.new(x0k, g0.inputs[1])
    g1 = node(nt, "ShaderNodeMath", (0, -1050), operation="LESS_THAN")
    L_.new(mm2.outputs[0], g1.inputs[0])
    L_.new(x1k, g1.inputs[1])
    al = node(nt, "ShaderNodeMath", (200, -950), operation="MULTIPLY")
    L_.new(g0.outputs[0], al.inputs[0])
    L_.new(g1.outputs[0], al.inputs[1])
    out_alpha(nt, L_, m2.outputs["Color"], al.outputs[0])
    m.use_backface_culling = True   # khối kín trong mờ (BLENDED): bỏ mặt sau kẻo vẽ đè lẫn → sọc theo vòng lưới
    return m


MAT = beam_mat()


def link(ob):
    sc.collection.objects.link(ob)
    return ob


def cylinder_x(name, seg=40, rings=24):
    """Ống dọc trục x từ 0 tới 1, bán kính 1, không nắp."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rows = []
    for i in range(rings + 1):
        x = i / rings
        rows.append([bm.verts.new((x, math.cos(TAU * j / seg), math.sin(TAU * j / seg))) for j in range(seg)])
    for i in range(rings):
        for j in range(seg):
            bm.faces.new((rows[i][j], rows[i][(j + 1) % seg], rows[i + 1][(j + 1) % seg], rows[i + 1][j]))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    return me


def sphere(name):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=20, radius=1.0)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    return me


body = link(bpy.data.objects.new("Ong", cylinder_x("Ong")))
capA = link(bpy.data.objects.new("DuoiTron", sphere("DuoiTron")))
capB = link(bpy.data.objects.new("DauTron", sphere("DauTron")))
for ob in (body, capA, capB):
    ob.data.materials.append(MAT)
for t, x0, x1, r in BEAM:
    f = F.fr(t)
    xb = max(0.0, x0 - 1.0)        # thân dư 1 đơn vị sau đuôi: ngưỡng đuôi cắt rách trên phần dư này (vật liệu, hai ngưỡng)
    body.location, body.scale = (xb, 0, 0), (max(1e-3, x1 - xb), max(1e-3, r), max(1e-3, r))
    capA.location, capA.scale = (x0, 0, 0), ((max(1e-3, r),) * 3 if x0 <= 0 else (1e-3,) * 3)   # đuôi rời miệng: bỏ nắp tròn, mép rách
    capB.location, capB.scale = (x1, 0, 0), (max(1e-3, r * 1.06),) * 3
    for ob in (body, capA, capB):
        ob.keyframe_insert("location", frame=f)
        ob.keyframe_insert("scale", frame=f)


def beam_at(t):
    for (ta, a0, a1, ra), (tb, b0, b1, rb) in zip(BEAM, BEAM[1:]):
        if ta <= t <= tb:
            k = (t - ta) / max(1e-6, tb - ta)
            return a0 + (b0 - a0) * k, a1 + (b1 - a1) * k, ra + (rb - ra) * k
    return BEAM[-1][1:]


# ---------------------------------------------------------------- dải nước xoắn ốc (trong mờ, mép rách, hiện trong cửa sổ x của ống)
def ribbon_mat(name):
    m, nt, L_ = new_mat(name)
    tc = node(nt, "ShaderNodeTexCoord", (-900, 0))
    sp = node(nt, "ShaderNodeSeparateXYZ", (-700, 0))
    L_.new(tc.outputs["UV"], sp.inputs["Vector"])
    # mép rách: nhiễu theo UV cộng độ gần giữa dải (v ở 0,5)
    nz = node(nt, "ShaderNodeTexNoise", (-700, -250))
    nz.inputs["Scale"].default_value = 6.0
    nz.inputs["Detail"].default_value = 0.5
    L_.new(tc.outputs["UV"], nz.inputs["Vector"])
    dv = node(nt, "ShaderNodeMath", (-500, 100), operation="SUBTRACT")
    L_.new(sp.outputs["Y"], dv.inputs[0])
    dv.inputs[1].default_value = 0.5
    av = node(nt, "ShaderNodeMath", (-350, 100), operation="ABSOLUTE")
    L_.new(dv.outputs[0], av.inputs[0])
    inv = node(nt, "ShaderNodeMath", (-200, 100), operation="SUBTRACT")
    inv.inputs[0].default_value = 0.5
    L_.new(av.outputs[0], inv.inputs[1])                  # 0,5 ở giữa dải → 0 ở mép
    s = node(nt, "ShaderNodeMath", (-50, 0), operation="MULTIPLY_ADD")
    L_.new(inv.outputs[0], s.inputs[0])
    s.inputs[1].default_value = 1.6
    L_.new(nz.outputs["Fac"], s.inputs[2])
    keep = node(nt, "ShaderNodeMath", (100, 0), operation="GREATER_THAN")
    L_.new(s.outputs[0], keep.inputs[0])
    keep.inputs[1].default_value = 0.78
    # cửa sổ x: hiện giữa đuôi và đầu ống (x của dải = u × L)
    ux = node(nt, "ShaderNodeMath", (-500, -500), operation="MULTIPLY")
    L_.new(sp.outputs["X"], ux.inputs[0])
    ux.inputs[1].default_value = L
    x0 = keyed_value(nt, (-500, -650), [(t, a) for t, a, b, r in BEAM])
    x1 = keyed_value(nt, (-500, -750), [(t, b) for t, a, b, r in BEAM])
    g0 = node(nt, "ShaderNodeMath", (-300, -550), operation="GREATER_THAN")
    L_.new(ux.outputs[0], g0.inputs[0])
    L_.new(x0, g0.inputs[1])
    g1 = node(nt, "ShaderNodeMath", (-300, -700), operation="LESS_THAN")
    L_.new(ux.outputs[0], g1.inputs[0])
    L_.new(x1, g1.inputs[1])
    w = node(nt, "ShaderNodeMath", (-100, -600), operation="MULTIPLY")
    L_.new(g0.outputs[0], w.inputs[0])
    L_.new(g1.outputs[0], w.inputs[1])
    a = node(nt, "ShaderNodeMath", (300, -200), operation="MULTIPLY")
    L_.new(keep.outputs[0], a.inputs[0])
    L_.new(w.outputs[0], a.inputs[1])
    # đứt đoạn: nhiễu thấp tần theo u (trôi theo giờ) → mỗi dải chỉ hiện 2–3 khúc, không thành lò xo đều
    mpu = node(nt, "ShaderNodeMapping", (-700, -950))
    mpu.inputs["Scale"].default_value = (3.2, 0.2, 1.0)
    for t, x in ((0, 0.0), (1.5, -2.4)):
        mpu.inputs["Location"].default_value[0] = x
        mpu.inputs["Location"].keyframe_insert("default_value", index=0, frame=F.fr(t))
    L_.new(tc.outputs["UV"], mpu.inputs["Vector"])
    nk = node(nt, "ShaderNodeTexNoise", (-500, -950))
    nk.inputs["Scale"].default_value = 1.0
    nk.inputs["Detail"].default_value = 0.0
    L_.new(mpu.outputs["Vector"], nk.inputs["Vector"])
    gk = node(nt, "ShaderNodeMath", (-300, -950), operation="GREATER_THAN")
    L_.new(nk.outputs["Fac"], gk.inputs[0])
    gk.inputs[1].default_value = 0.47
    a1 = node(nt, "ShaderNodeMath", (400, -300), operation="MULTIPLY")
    L_.new(a.outputs[0], a1.inputs[0])
    L_.new(gk.outputs[0], a1.inputs[1])
    a2 = node(nt, "ShaderNodeMath", (450, -200), operation="MULTIPLY")
    L_.new(a1.outputs[0], a2.inputs[0])
    a2.inputs[1].default_value = 0.72
    # hai tông: nửa trước sáng (bọt), nửa sau lam nhạt — theo v
    tone = node(nt, "ShaderNodeMath", (100, 250), operation="GREATER_THAN")
    L_.new(sp.outputs["Y"], tone.inputs[0])
    tone.inputs[1].default_value = 0.62
    mx = node(nt, "ShaderNodeMixRGB", (300, 250), blend_type="MIX")
    L_.new(tone.outputs[0], mx.inputs["Fac"])
    mx.inputs["Color1"].default_value = F.lin(C["sang"])
    mx.inputs["Color2"].default_value = F.lin(C["bot"])
    out_alpha(nt, L_, mx.outputs["Color"], a2.outputs[0])
    return m


def helix(name, pitch, phase, width, rho=1.0, n=260):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv_l = bm.loops.layers.uv.new("UVMap")
    top, bot = [], []
    for i in range(n + 1):
        u = i / n
        x = u * L
        th = TAU * x / pitch + phase
        wv = width * (0.55 + 0.45 * math.sin(math.pi * u) ** 0.5)
        for lst, dv in ((top, 0.5), (bot, -0.5)):
            lst.append(bm.verts.new((x + dv * wv, rho * math.cos(th), rho * math.sin(th))))
    for i in range(n):
        f = bm.faces.new((bot[i], bot[i + 1], top[i + 1], top[i]))
        for lp, (uu, vv) in zip(f.loops, ((i / n, 0), ((i + 1) / n, 0), ((i + 1) / n, 1), (i / n, 1))):
            lp[uv_l].uv = (uu, vv)
    bm.to_mesh(me)
    bm.free()
    return me


RIB = ribbon_mat("DaiXoan")
for k, (pitch, ph, wd, spin) in enumerate([(5.2, 0.0, 0.95, -1), (4.0, math.pi, 0.62, -1)]):
    ob = link(bpy.data.objects.new(f"DaiXoan{k}", helix(f"DaiXoan{k}", pitch, ph, wd)))
    ob.data.materials.append(RIB)
    for t in (0.0, 0.18, 0.26, 0.3, 0.5, 0.7, 0.9, 1.1, 1.2, 1.32, 1.42, 1.5):
        r = beam_at(t)[2]
        s = 0.0 if t < 0.18 else (1.6 + 0.3 * k) * r
        ob.scale = (1, max(1e-3, s), max(1e-3, s))
        ob.keyframe_insert("scale", frame=F.fr(t))
    for t, a in ((0, 0.0), (1.5, spin * 3 * TAU * (1 if k == 0 else 1.4))):
        ob.rotation_euler[0] = a
        ob.keyframe_insert("rotation_euler", index=0, frame=F.fr(t))


# ---------------------------------------------------------------- mảnh phẳng quay mặt về camera (mặt XZ): cánh quạt, gai bông nước
def blade_mesh(name, length, base, curve=0.0, notch=0.0):
    """Lá nước nhọn: gốc ở (0,0), mũi ở (length, 0) (trục x), hai mép cong nhẹ, mép sau có khía."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    n = 10
    up, dn = [], []
    for i in range(n + 1):
        u = i / n
        wd = base * (1 - u) ** 0.85 * (1 + 0.35 * math.sin(math.pi * u))
        bend = curve * u * u * length
        up.append(bm.verts.new((u * length, 0, bend + wd / 2)))
        dn.append(bm.verts.new((u * length, 0, bend - wd / 2 * (1 - notch * math.sin(TAU * 2.5 * u) ** 2))))
    for i in range(n):
        bm.faces.new((dn[i], dn[i + 1], up[i + 1], up[i]))
    bm.to_mesh(me)
    bm.free()
    return me


def blade(name, mat, pos, ang_deg, length, base, curve=0.0, notch=0.0):
    ob = link(bpy.data.objects.new(name, blade_mesh(name, length, base, curve, notch)))
    ob.data.materials.append(mat)
    ob.location = pos
    ob.rotation_euler = (0, -math.radians(ang_deg), 0)      # quay quanh y: góc đo ngược kim đồng hồ trên màn hình
    return ob


def key_scale(ob, pairs):
    for t, s in pairs:
        ob.scale = (max(1e-3, s),) * 3
        ob.keyframe_insert("scale", frame=F.fr(t))


# cánh quạt lúc ống phình: 4 tấm lớn trong mờ xoè ra phía sau-trên / sau-dưới rồi tan (cỡ lên, đổi sang trong suốt bằng co nhỏ)
QUAT = flat("Quat", C["sang"], 0.85)   # trong mờ ít: trên nền cát sáng màu lam mờ ngả xanh xám
for k, (x, ang, ln, bs) in enumerate([(2.3, 148, 2.7, 1.2), (3.8, 208, 2.7, 1.1), (5.6, 138, 2.6, 1.0), (7.2, 218, 2.1, 0.85)]):
    ob = blade(f"Quat{k}", QUAT, (x, -0.2, 0), ang, ln, bs, 0.12 * (1 if ang < 180 else -1), 0.35)
    t0 = 0.17 + 0.03 * k
    key_scale(ob, [(0, 0), (t0, 0), (t0 + 0.08, 1.0), (t0 + 0.2, 1.15), (t0 + 0.3, 0)])

# bông nước ở đích (x = L), theo tia gốc: SAO GAI LÕM lớn (tấm nước nhọn cạnh lõm) toả lên / xuống / ngược về người bắn và một tấm
# dài XUYÊN ra sau đích; hai lớp (sau lam giữa trong mờ, trước lam sáng) + lõi trắng; mỗi lớp 3 dạng thay nhau mỗi 2 khung (gai đổi dáng
# như đang toé) + đập cỡ; mảnh nước cuộn (khối múi tròn có điểm sáng) bay ra theo đợt; giọt.
BOT, SANG, CHINH = flat("Bot", C["bot"]), flat("Sang", C["sang"]), flat("Chinh", C["chinh"])
GIUA_M = flat("GiuaMo", C["giua"], 0.88)


def star_mesh(name, pts, ri_k=0.16, seg=7):
    """Sao gai lõm phẳng (mặt XZ, gốc ở tâm): pts = [(góc độ, dài)], giữa hai gai cạnh lõm vào tới ri_k × dài."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    pts = sorted(pts)
    c = bm.verts.new((0, 0, 0))
    ring = []
    for i, (a, ln) in enumerate(pts):
        a2, ln2 = pts[(i + 1) % len(pts)]
        if a2 <= a:
            a2 += 360
        for sgm in range(seg):
            u = sgm / seg
            am = math.radians(a + (a2 - a) * u)
            r = (ln * (1 - u) + ln2 * u) * (ri_k + (1 - ri_k) * abs(2 * u - 1) ** 2)
            ring.append(bm.verts.new((r * math.cos(am), 0, r * math.sin(am))))
    for i in range(len(ring)):
        bm.faces.new((c, ring[i], ring[(i + 1) % len(ring)]))
    bm.to_mesh(me)
    bm.free()
    return me


def star_pts(scale):
    """Gai: lên, xuống, ngược về người bắn (trên / dưới trục), một tấm xuyên ra sau đích (dài), vài gai phụ."""
    base = [(rnd.uniform(95, 120), 2.0), (rnd.uniform(145, 165), 2.4), (rnd.uniform(195, 215), 2.2), (rnd.uniform(240, 265), 1.8),
            (rnd.uniform(-6, 6), 2.7), (rnd.uniform(35, 55), 1.4)]
    return [(a, ln * scale * rnd.uniform(0.75, 1.2)) for a, ln in base]


def swap_keys(obs, t0, t1, step=2):
    """Các dạng thay nhau hiện mỗi `step` khung trong [t0, t1] (hide_render, giữ nguyên tới khoá sau)."""
    f0, f1 = int(round(F.fr(t0))), int(round(F.fr(t1)))
    for ob in obs:
        ob.hide_render = True
        ob.keyframe_insert("hide_render", frame=1)
    k = 0
    for f in range(f0, f1 + 1, step):
        for j, ob in enumerate(obs):
            ob.hide_render = j != k % len(obs)
            ob.keyframe_insert("hide_render", frame=f)
        k += 1
    for ob in obs:
        ob.hide_render = True
        ob.keyframe_insert("hide_render", frame=f1 + 1)


def pulse(ob, peak, t0=0.1, t1=1.44):
    pairs = [(0, 0.0), (t0, 0.0), (t0 + 0.03, 0.35 * peak), (0.2, 0.5 * peak), (0.3, 1.08 * peak)]
    t = 0.3
    while t < t1 - 0.12:
        t += 0.1 + rnd.uniform(-0.02, 0.02)
        pairs.append((t, rnd.uniform(0.82, 1.1) * peak))
    pairs += [(t1 - 0.04, 0.55 * peak), (t1, 0.0)]
    key_scale(ob, pairs)


HX = L - 0.12                                            # tâm va chạm (mặt trước đích)
for li, (mat, sc_, y) in enumerate(((GIUA_M, 1.0, -0.62), (SANG, 0.72, -0.7))):
    obs = []
    for v in range(3):
        ob = link(bpy.data.objects.new(f"Sao{li}_{v}", star_mesh(f"Sao{li}_{v}", star_pts(sc_), 0.36 if li == 0 else 0.42)))
        ob.data.materials.append(mat)
        ob.location = (HX, y - 0.01 * v, 0)
        ob.rotation_euler = (0, math.radians(rnd.uniform(-8, 8)), 0)
        pulse(ob, 1.0)
        obs.append(ob)
    swap_keys(obs, 0.12, 1.44, 2)
loi = F.flat_star("LoiNuoc", 7, 0.8, 0.5, C["bot"], y=0.0, center=(0, 0))
loi.location = (HX, -0.78, 0)
loi.data.materials.clear()
loi.data.materials.append(BOT)
pulse(loi, 1.0)
for t in (0.0, 0.5, 1.0, 1.5):                           # lõi xoay chậm cho khỏi đứng im
    loi.rotation_euler[1] = math.radians(-40 * t)
    loi.keyframe_insert("rotation_euler", index=1, frame=F.fr(t))


def blob_mesh(name, lobes, ph):
    """Mảnh nước cuộn: khối tròn nhiều múi (mép gợn), gốc ở tâm, kéo dài theo x."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    c = bm.verts.new((0, 0, 0))
    ring = []
    n = 36
    for i in range(n):
        a = TAU * i / n
        r = 1 + 0.26 * math.sin(lobes * a + ph) + 0.12 * math.sin((lobes + 3) * a + 2 * ph)
        ring.append(bm.verts.new((1.5 * r * math.cos(a), 0, r * math.sin(a))))
    for i in range(n):
        bm.faces.new((c, ring[i], ring[(i + 1) % n]))
    bm.to_mesh(me)
    bm.free()
    return me


GZ = 5.0
for k in range(18):
    t0 = (0.14, 0.3, 0.48, 0.66, 0.84, 1.02)[k // 3] + rnd.uniform(0, 0.05)
    a = math.radians(rnd.choice((rnd.uniform(110, 160), rnd.uniform(200, 250), rnd.uniform(35, 70), rnd.uniform(-70, -35))))
    v = rnd.uniform(3.2, 5.2)
    life = rnd.uniform(0.32, 0.46)
    size = rnd.uniform(0.18, 0.3)
    ob = link(bpy.data.objects.new(f"Cuon{k}", blob_mesh(f"Cuon{k}", rnd.choice((3, 4, 5)), rnd.uniform(0, TAU))))
    ob.data.materials.append(SANG if k % 3 else CHINH)
    hi_ = link(bpy.data.objects.new(f"CuonSang{k}", blob_mesh(f"CuonSang{k}", 3, rnd.uniform(0, TAU))))
    hi_.data.materials.append(BOT)
    hi_.parent = ob
    hi_.location, hi_.scale = (0.25, -0.02, 0.18), (0.42, 0.42, 0.42)
    vx, vz = v * math.cos(a), v * math.sin(a)
    for t in [0.0, t0 - 0.01] + [t0 + life * i / 6 for i in range(7)] + [t0 + life + 0.01]:
        if t < t0 or t > t0 + life:
            ob.scale = (1e-3,) * 3
            ob.location = (HX, -0.9, 0)
        else:
            sx = t - t0
            q = sx / life
            ob.location = (HX + vx * sx, -0.9, vz * sx - 0.5 * GZ * sx * sx)
            ss = size * (0.45 + 1.1 * q) * (1 - q ** 3)
            ob.scale = (ss, ss, ss)
            dvz = vz - GZ * sx
            ob.rotation_euler = (0, -math.atan2(dvz, vx), 0)
            ob.keyframe_insert("rotation_euler", frame=F.fr(t))
        ob.keyframe_insert("location", frame=F.fr(t))
        ob.keyframe_insert("scale", frame=F.fr(t))

# bông toé nhỏ ở miệng (đầu tia mảnh và lúc phình)
for k in range(5):
    ang = 110 + 140 * k / 4 + rnd.uniform(-10, 10)
    ob = blade(f"Mieng{k}", (BOT, SANG)[k % 2], (0.15, -0.5, 0), ang, rnd.uniform(0.7, 1.2), 0.3, 0, 0.2)
    key_scale(ob, [(0, 0.2), (0.06, 1.0), (0.14, 0.6), (0.24, 1.2), (0.36, 0.7), (0.6, 0.5), (1.1, 0.5), (1.2, 0)])

# ---------------------------------------------------------------- giọt bắn: bay theo đường đạn, trọng lực, tắt dần (co lại)
GIOT = (BOT, SANG, CHINH)
G = 9.0
for k in range(46):
    if k < 30:          # từ bông nước ở đích, toé ngược / lên / xuống
        t0 = rnd.uniform(0.14, 1.3)
        p0 = (L - 0.3, -0.8, rnd.uniform(-0.3, 0.3))
        a = math.radians(rnd.uniform(105, 255))
        v = rnd.uniform(4, 8)
    else:               # dọc ống lúc phình
        t0 = rnd.uniform(0.2, 0.42)
        p0 = (rnd.uniform(1, 8), -0.8, rnd.choice((-1, 1)) * 0.5)
        a = math.radians(rnd.uniform(60, 120) * (1 if p0[2] > 0 else -1))
        v = rnd.uniform(2.5, 5)
    life = rnd.uniform(0.3, 0.55)
    rr = rnd.uniform(0.05, 0.11)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0)
    ob = bpy.context.active_object
    ob.name = f"Giot{k}"
    ob.data.materials.append(GIOT[k % 3])
    vx, vz = v * math.cos(a), v * math.sin(a)
    steps = [0.0] + [t0 + life * i / 6 for i in range(7)] + [t0 + life + 0.02]
    for t in steps:
        if t < t0 or t > t0 + life:
            ob.scale = (1e-3,) * 3
            ob.location = p0
        else:
            s = t - t0
            ob.location = (p0[0] + vx * s, p0[1], p0[2] + vz * s - 0.5 * G * s * s)
            q = 1 - (s / life) ** 2
            ob.scale = (rr * q * 1.35, rr * q, rr * q)
        ob.keyframe_insert("location", frame=F.fr(t))
        ob.keyframe_insert("scale", frame=F.fr(t))

# ---------------------------------------------------------------- tách phần (người dùng 2026-11-24: "phần va chạm nên tách riêng ra")
# tia: bỏ sao gai / lõi / mảnh cuộn / giọt ở đích; trung: chỉ giữ chúng. Cùng nhịp 36 khung, cùng tỉ lệ px (0,02027 đơn vị / px) để ghép
# lại khớp; tia neo ở miệng (0, 0), va chạm neo ở điểm chạm (HX, 0) → trong game đặt va chạm ở thân đối thủ với khoảng cách bất kỳ.
VA = ("Sao", "LoiNuoc", "Cuon")
def _la_va(ob):
    if ob.name.startswith(VA):
        return True
    return ob.name.startswith("Giot") and int(ob.name[4:]) < 30
if PHAN != "all":
    for ob in list(sc.objects):
        if ob.type in ("MESH",) and (_la_va(ob) != (PHAN == "trung")):
            bpy.data.objects.remove(ob, do_unlink=True)

# ---------------------------------------------------------------- render
UPP = 15.2 / 750
if PHAN == "trung":
    W, H = 380, 330
    CAM = (HX + 0.35, -30, 0.0)
    PREFIX, ANCHOR = "nuoc_trung", (HX, 0)
else:
    W, H = 750, 330
    CAM = (L / 2 + 1.1, -30, 0.0)   # rộng sang phải: tấm nước xuyên ra sau đích dài tới x ≈ 13,2
    PREFIX, ANCHOR = ("nuoc_tia" if PHAN == "tia" else "nuoc_bl"), (0, 0)
F.setup_render(CAM, UPP * W, W, H)
sc.render.engine = "BLENDER_EEVEE"
try:
    sc.eevee.taa_render_samples = 16
except Exception:
    pass
sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"
F.run(OUT, PREFIX, CAM, UPP * W, W, H, frames=FRAMES, save=SAVE, save_frame=10, anchor_xz=ANCHOR)
