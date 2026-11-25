# -*- coding: utf-8 -*-
"""Thư viện dùng chung cho bộ NƯỚC dựng bằng Blender (Eevee, màu phẳng xanh dương, không phát sáng), tách từ nuoc_blender.py (tia nước,
người dùng duyệt màu 2026-11-24: "gam màu nên là xanh dương thôi, phối màu giống tia gốc"). Dùng với fxbl.py (khung giờ, render, khoá).
"""
import math
import random

import bmesh
import bpy

import fxbl as F

TAU = 2 * math.pi
# chỉ xanh dương, đo từ tia gốc (water.mp4): sáng #64F8FA/#49D8F4, giữa #3EB1E0, đậm #378EB8
C = dict(bot="#EAFBFF", sang="#93E8FF", chinh="#4FCDF6", giua="#3AA8E4", dam="#2A7BC8", sau="#1F5BAA")
STOPS = [(0.0, "dam"), (0.31, "giua"), (0.37, "sang"), (0.39, "chinh"), (0.64, "sang"), (0.76, "bot")]
# lam NHẠT pha bọt trắng (người dùng 2026-11-24 xem bộ theo repo: "màu không ổn, để màu xanh nhạt, có mix bọt trắng thôi"):
# nền lam nhạt, vệt lam nhạt hơi sâu cho có dòng chảy, mảng bọt trắng; không lam đậm / lam giữa
C["nhat"] = "#7ED9F6"
STOPS_NHAT = [(0.0, "nhat"), (0.36, "sang"), (0.64, "bot")]
rnd = random.Random(5)


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


def out_alpha(m, nt, L_, color_socket, alpha_socket=None, alpha=1.0):
    """Emission (màu từ socket) trộn Transparent theo alpha; có alpha thì chế độ trong mờ mịn (BLENDED, mặc định dither lấm tấm)."""
    o = node(nt, "ShaderNodeOutputMaterial", (1200, 0))
    e = node(nt, "ShaderNodeEmission", (900, 80))
    e.inputs["Strength"].default_value = 1.0
    L_.new(color_socket, e.inputs["Color"])
    if alpha_socket is None and alpha >= 1:
        L_.new(e.outputs[0], o.inputs["Surface"])
        return
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
    for el, (pos, key) in zip(els, stops):
        el.position, el.color = pos, F.lin(C.get(key, key))
    return r


def flat(name, key, alpha=1.0):
    m, nt, L_ = new_mat(name)
    rgb = node(nt, "ShaderNodeRGB", (600, 0))
    rgb.outputs[0].default_value = F.lin(C.get(key, key))
    out_alpha(m, nt, L_, rgb.outputs[0], alpha=alpha)
    return m


def keyed_value(nt, loc, pairs):
    v = node(nt, "ShaderNodeValue", loc)
    for t, val in pairs:
        v.outputs[0].default_value = val
        v.outputs[0].keyframe_insert("default_value", frame=F.fr(t))
    return v.outputs[0]


def flow_color(nt, L_, vec, scale=(0.11, 3.6, 3.6), move=None, spin=None, hi_axis="Z", hi_th=0.86, rim_th=0.78, stops=STOPS,
               distortion=0.25, noise_scale=1.2, vol=None, rim_key="sang"):
    """MÀU NƯỚC XANH của bộ nước (vệt thấu kính dài theo một trục, ramp CONSTANT 6 bậc lam, vệt sáng theo pháp tuyến hi_axis, mép
    sáng Layer Weight) trên socket toạ độ `vec` (Object hoặc UV). move = (giờ_cuối, (dx, dy, dz)) trượt toạ độ (một lượt / dòng chảy);
    spin = (chu kỳ, trục, số vòng) xoay toạ độ (lặp liền). vol = (lx, ly, lz, k): tô KHỐI kiểu cel — cộng k·(pháp tuyến · hướng
    sáng) vào giá trị vân trước ramp → mặt khuất ra tông sâu, mặt hướng sáng ra bọt trắng, vẫn dải màu phẳng (người dùng: cầu
    của repo "nhìn rất 3D"). Trả về socket màu."""
    mp = node(nt, "ShaderNodeMapping", (-700, 0))
    if spin:
        P, ax, turns = spin
        rot = node(nt, "ShaderNodeMapping", (-800, 200))
        for t, a in ((0, 0.0), (P, turns * TAU)):
            rot.inputs["Rotation"].default_value[ax] = a
            rot.inputs["Rotation"].keyframe_insert("default_value", index=ax, frame=F.fr(t))
        L_.new(vec, rot.inputs["Vector"])
        L_.new(rot.outputs["Vector"], mp.inputs["Vector"])
    else:
        L_.new(vec, mp.inputs["Vector"])
    mp.inputs["Scale"].default_value = scale
    if move:
        t1, d = move
        for t, k in ((0, 0.0), (t1, 1.0)):
            mp.inputs["Location"].default_value = (d[0] * k, d[1] * k, d[2] * k)
            mp.inputs["Location"].keyframe_insert("default_value", frame=F.fr(t))
    nz = node(nt, "ShaderNodeTexNoise", (-500, 0))
    nz.inputs["Scale"].default_value = noise_scale
    nz.inputs["Detail"].default_value = 0.0
    nz.inputs["Distortion"].default_value = distortion
    L_.new(mp.outputs["Vector"], nz.inputs["Vector"])
    rv = ramp(nt, (-250, 0), stops)
    if vol:
        lx, ly, lz, kv = vol
        gv = node(nt, "ShaderNodeNewGeometry", (-700, 300))
        dp = node(nt, "ShaderNodeVectorMath", (-500, 300), operation="DOT_PRODUCT")
        L_.new(gv.outputs["Normal"], dp.inputs[0])
        ln = (lx * lx + ly * ly + lz * lz) ** 0.5
        dp.inputs[1].default_value = (lx / ln, ly / ln, lz / ln)
        fv = node(nt, "ShaderNodeMath", (-380, 200), operation="MULTIPLY_ADD")
        L_.new(dp.outputs["Value"], fv.inputs[0])
        fv.inputs[1].default_value = kv
        L_.new(nz.outputs["Fac"], fv.inputs[2])
        L_.new(fv.outputs[0], rv.inputs["Fac"])
    else:
        L_.new(nz.outputs["Fac"], rv.inputs["Fac"])
    geo = node(nt, "ShaderNodeNewGeometry", (-500, -300))
    sp = node(nt, "ShaderNodeSeparateXYZ", (-300, -300))
    L_.new(geo.outputs["Normal"], sp.inputs["Vector"])
    hi = node(nt, "ShaderNodeMath", (-100, -300), operation="GREATER_THAN")
    hi.inputs[1].default_value = hi_th
    L_.new(sp.outputs[hi_axis], hi.inputs[0])
    lw = node(nt, "ShaderNodeLayerWeight", (-300, -500))
    lw.inputs["Blend"].default_value = 0.5
    rim = node(nt, "ShaderNodeMath", (-100, -500), operation="GREATER_THAN")
    rim.inputs[1].default_value = rim_th
    L_.new(lw.outputs["Facing"], rim.inputs[0])
    m1 = node(nt, "ShaderNodeMixRGB", (150, 0), blend_type="MIX")
    L_.new(hi.outputs[0], m1.inputs["Fac"])
    L_.new(rv.outputs["Color"], m1.inputs["Color1"])
    m1.inputs["Color2"].default_value = F.lin(C["bot"])
    m2 = node(nt, "ShaderNodeMixRGB", (350, 0), blend_type="MIX")
    L_.new(rim.outputs[0], m2.inputs["Fac"])
    L_.new(m1.outputs["Color"], m2.inputs["Color1"])
    m2.inputs["Color2"].default_value = F.lin(C.get(rim_key, rim_key))   # rim_key: màu dải mép (mặc định lam sáng)
    return m2.outputs["Color"]


def flow_mat(name, coord_obj, scale=(0.11, 3.6, 3.6), move=None, spin=None, hi_axis="Z", hi_th=0.86, rim_th=0.78, stops=STOPS,
             distortion=0.25, noise_scale=1.2, vol=None, rim_key="sang"):
    """Nước chảy trên toạ độ Object của coord_obj (xem flow_color)."""
    m, nt, L_ = new_mat(name)
    tc = node(nt, "ShaderNodeTexCoord", (-900, 0))
    tc.object = coord_obj
    col = flow_color(nt, L_, tc.outputs["Object"], scale, move, spin, hi_axis, hi_th, rim_th, stops, distortion, noise_scale, vol, rim_key)
    out_alpha(m, nt, L_, col)
    return m


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def smooth(me):
    for p in me.polygons:
        p.use_smooth = True
    return me


def sphere(name, u=40, v=20):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=1.0)
    bm.to_mesh(me)
    bm.free()
    return smooth(me)


def flat_poly(name, pts):
    """Đa giác phẳng mặt XZ (quay về camera), quạt từ tâm (0, 0); pts = [(x, z)]."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    c = bm.verts.new((0, 0, 0))
    ring = [bm.verts.new((x, 0, z)) for x, z in pts]
    for i in range(len(ring)):
        bm.faces.new((c, ring[i], ring[(i + 1) % len(ring)]))
    bm.to_mesh(me)
    bm.free()
    return me


def star_mesh(name, pts, ri_k=0.38, seg=7, power=2):
    """Sao gai lõm phẳng (gốc ở tâm): pts = [(góc độ, dài)], giữa hai gai cạnh lõm vào tới ri_k × dài (to bản khi ri_k lớn)."""
    pts = sorted(pts)
    out = []
    for i, (a, ln) in enumerate(pts):
        a2, ln2 = pts[(i + 1) % len(pts)]
        if a2 <= a:
            a2 += 360
        for s in range(seg):
            u = s / seg
            am = math.radians(a + (a2 - a) * u)
            r = (ln * (1 - u) + ln2 * u) * (ri_k + (1 - ri_k) * abs(2 * u - 1) ** power)
            out.append((r * math.cos(am), r * math.sin(am)))
    return flat_poly(name, out)


def blob_mesh(name, lobes, ph, stretch=1.5, n=36):
    """Mảnh nước cuộn: khối tròn nhiều múi (mép gợn), kéo dài theo x."""
    pts = []
    for i in range(n):
        a = TAU * i / n
        r = 1 + 0.26 * math.sin(lobes * a + ph) + 0.12 * math.sin((lobes + 3) * a + 2 * ph)
        pts.append((stretch * r * math.cos(a), r * math.sin(a)))
    return flat_poly(name, pts)


def blade_mesh(name, length, base, curve=0.0, notch=0.0):
    """Lá nước nhọn: gốc (0, 0), mũi (length, 0), hai mép cong nhẹ, mép dưới có khía."""
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


def obj(name, me, mat, loc=(0, 0, 0), ang_deg=0.0):
    """Vật phẳng mặt XZ; ang_deg: góc ngược kim đồng hồ trên màn hình (quay quanh y)."""
    ob = link(bpy.data.objects.new(name, me))
    ob.data.materials.append(mat)
    ob.location = loc
    ob.rotation_euler = (0, -math.radians(ang_deg), 0)
    return ob


def key_scale(ob, pairs, axes=None):
    for t, s in pairs:
        if axes:
            ob.scale = tuple(max(1e-3, s * a) for a in axes)
        else:
            ob.scale = (max(1e-3, s),) * 3
        ob.keyframe_insert("scale", frame=F.fr(t))


def swap_keys(obs, t0, t1, step=2):
    """Các dạng thay nhau hiện mỗi `step` khung trong [t0, t1] (hide_render)."""
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


def ballistic(ob, p0, v, t0, life, g=5.0, size=1.0, grow=(0.45, 1.1), align=True, y=None, steps=6):
    """Vật bay theo đường đạn mặt XZ từ t0 trong life giây: nở (grow) rồi co mất; align: xoay theo vận tốc."""
    vx, vz = v
    yy = p0[1] if y is None else y
    ts = [0.0, max(0.0, t0 - 0.01)] + [t0 + life * i / steps for i in range(steps + 1)] + [t0 + life + 0.01]
    for t in ts:
        if t < t0 or t > t0 + life:
            ob.scale = (1e-3,) * 3
            ob.location = p0
        else:
            s = t - t0
            q = s / life
            ob.location = (p0[0] + vx * s, yy, p0[2] + vz * s - 0.5 * g * s * s)
            ss = size * (grow[0] + grow[1] * q) * (1 - q ** 3)
            ob.scale = (max(1e-3, ss),) * 3
            if align:
                ob.rotation_euler = (0, -math.atan2(vz - g * s, vx), 0)
                ob.keyframe_insert("rotation_euler", frame=F.fr(t))
        ob.keyframe_insert("location", frame=F.fr(t))
        ob.keyframe_insert("scale", frame=F.fr(t))


def drop(name, mat, r):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0)
    ob = bpy.context.active_object
    ob.name = name
    ob.data.materials.append(mat)
    return ob


def eevee(cam, w, h, upp):
    F.setup_render(cam, upp * w, w, h)
    sc = bpy.context.scene
    sc.camera.data.sensor_fit = "HORIZONTAL"   # khung DỌC: mặc định Blender lấy ortho theo cạnh dài (chiều cao) → sai tỉ lệ px và điểm neo
    sc.render.engine = "BLENDER_EEVEE"
    try:
        sc.eevee.taa_render_samples = 16
    except Exception:
        pass
    sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"


UPP = 15.2 / 750      # cùng tỉ lệ px với tia nước (nuoc_blender.py) để các hiệu ứng nước cùng cỡ nét


# ---------------------------------------------------------------- TAN THEO NGƯỠNG × MẶT NẠ MỀM (học repo abitofgamedev/water_vfx,
# skill vfx-petclash/hoc_water_vfx_abitofgamedev.md; mặt nạ tự sinh bằng mat_na_nuoc.py → mat_na/*.png)
MASK_DIR = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "mat_na")


def mask_img(name):
    """Ảnh mặt nạ xám (Non-Color) trong mat_na/, nạp một lần."""
    im = bpy.data.images.get(name + ".png")
    if im is None:
        im = bpy.data.images.load(__import__("os").path.join(MASK_DIR, name + ".png"))
        im.colorspace_settings.name = "Non-Color"
    return im


def mask_mat(name, mask, thr, key="bot", rim=None, inner=None, tiling=(1.0, 1.0), noise_scale=5.0, nk=0.65, offset=None,
             alpha=1.0, extension="REPEAT", back=None):
    """Vật liệu tan theo NGƯỠNG: v = mặt_nạ_mềm(uv·tiling) × (1 − nk + nk·nhiễu(uv + lệch)); điểm hiện khi v > ngưỡng(t).
    thr = [(giờ, ngưỡng)] tăng dần (repo dùng 0,1 → 1 theo đời hạt): chỗ mặt nạ mỏng tan trước, mép luôn sắc.
    key = màu phẳng; rim = (dải, key_mép): phần v < ngưỡng + dải tô màu mép (viền khác tông chạy theo mép đang tan);
    inner = (mức, key_lõi): phần v > mức tô màu lõi. offset = lệch nhiễu (mỗi bản một hình từ cùng mặt nạ); alpha nhân thêm.
    extension: REPEAT (vành / ống dán lặp) hoặc CLIP (sprite, ngoài ảnh = 0). back = key màu mặt sau (lòng vương miện tối hơn).
    Lưới phải có UV (quad, ring_cone, ...)."""
    m, nt, L_ = new_mat(name)
    tc = node(nt, "ShaderNodeTexCoord", (-1400, 0))
    mp = node(nt, "ShaderNodeMapping", (-1200, 150))
    mp.inputs["Scale"].default_value = (tiling[0], tiling[1], 1.0)
    L_.new(tc.outputs["UV"], mp.inputs["Vector"])
    ti = node(nt, "ShaderNodeTexImage", (-1000, 150))
    ti.image, ti.extension, ti.interpolation = mask_img(mask), extension, "Cubic"
    L_.new(mp.outputs["Vector"], ti.inputs["Vector"])
    mp2 = node(nt, "ShaderNodeMapping", (-1200, -200))
    o = offset if offset is not None else (rnd.uniform(-9, 9), rnd.uniform(-9, 9), rnd.uniform(-9, 9))
    mp2.inputs["Location"].default_value = o
    L_.new(tc.outputs["UV"], mp2.inputs["Vector"])
    nz = node(nt, "ShaderNodeTexNoise", (-1000, -200))
    nz.inputs["Scale"].default_value = noise_scale
    nz.inputs["Detail"].default_value = 1.0
    nz.inputs["Distortion"].default_value = 0.3
    L_.new(mp2.outputs["Vector"], nz.inputs["Vector"])
    mr = node(nt, "ShaderNodeMapRange", (-800, -200))            # nhiễu Blender dồn quanh 0,5 → kéo giãn 0,3..0,7 thành 0..1
    mr.clamp = True
    mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = 0.3, 0.7
    L_.new(nz.outputs["Fac"], mr.inputs["Value"])
    f = node(nt, "ShaderNodeMath", (-600, -200), operation="MULTIPLY_ADD")
    L_.new(mr.outputs["Result"], f.inputs[0])
    f.inputs[1].default_value, f.inputs[2].default_value = nk, 1 - nk
    v = node(nt, "ShaderNodeMath", (-450, 0), operation="MULTIPLY")
    L_.new(ti.outputs["Color"], v.inputs[0])
    L_.new(f.outputs[0], v.inputs[1])
    th = keyed_value(nt, (-600, 250), thr)
    d = node(nt, "ShaderNodeMath", (-300, 100), operation="SUBTRACT")
    L_.new(v.outputs[0], d.inputs[0])
    L_.new(th, d.inputs[1])
    vis = node(nt, "ShaderNodeMath", (-150, 100), operation="GREATER_THAN")
    L_.new(d.outputs[0], vis.inputs[0])
    vis.inputs[1].default_value = 0.0
    col = node(nt, "ShaderNodeRGB", (-150, 400))
    col.outputs[0].default_value = F.lin(C.get(key, key))
    cs = col.outputs[0]
    if back:
        geo = node(nt, "ShaderNodeNewGeometry", (-150, 650))
        mb = node(nt, "ShaderNodeMixRGB", (50, 600), blend_type="MIX")
        L_.new(geo.outputs["Backfacing"], mb.inputs["Fac"])
        L_.new(cs, mb.inputs["Color1"])
        mb.inputs["Color2"].default_value = F.lin(C.get(back, back))
        cs = mb.outputs["Color"]
    if inner:
        lv, ik = inner
        ii = node(nt, "ShaderNodeMath", (0, 500), operation="GREATER_THAN")
        L_.new(v.outputs[0], ii.inputs[0])
        ii.inputs[1].default_value = lv
        mx = node(nt, "ShaderNodeMixRGB", (200, 400), blend_type="MIX")
        L_.new(ii.outputs[0], mx.inputs["Fac"])
        L_.new(cs, mx.inputs["Color1"])
        mx.inputs["Color2"].default_value = F.lin(C.get(ik, ik))
        cs = mx.outputs["Color"]
    if rim:
        band, rk = rim
        ed = node(nt, "ShaderNodeMath", (0, 250), operation="LESS_THAN")
        L_.new(d.outputs[0], ed.inputs[0])
        ed.inputs[1].default_value = band
        mx = node(nt, "ShaderNodeMixRGB", (400, 300), blend_type="MIX")
        L_.new(ed.outputs[0], mx.inputs["Fac"])
        L_.new(cs, mx.inputs["Color1"])
        mx.inputs["Color2"].default_value = F.lin(C.get(rk, rk))
        cs = mx.outputs["Color"]
    a = vis.outputs[0]
    if alpha < 1:
        am = node(nt, "ShaderNodeMath", (100, 0), operation="MULTIPLY")
        L_.new(a, am.inputs[0])
        am.inputs[1].default_value = alpha
        a = am.outputs[0]
    out_alpha(m, nt, L_, cs, a)
    return m


def uv_sphere(name, u=40, v=20):
    """Cầu bán kính 1 CÓ UV (cho mask_mat; sphere() không có UV)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=1.0, calc_uvs=True)
    bm.to_mesh(me)
    bm.free()
    return smooth(me)


def quad(name, w, h, plane="XZ"):
    """Tấm chữ nhật tâm (0, 0) có UV 0..1: XZ = đứng quay về máy (sprite), XY = nằm trên đất (decal)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    if plane == "XZ":
        pts = [(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)]
    else:
        pts = [(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)]
    vs = [bm.verts.new(p) for p in pts]
    f = bm.faces.new(vs)
    for lp, (u, v) in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        lp[uv].uv = (u, v)
    bm.to_mesh(me)
    bm.free()
    return me


def ring_cone(name, r0, r1, h, nu=56, nv=10, flare=1.4):
    """Vành nón loe (vương miện nước, lưới "sóng" của repo là kiểu này): trục +Z, bán kính r0 → r1, cao h·v^flare.
    UV: u quanh vành (0..1, có đường nối), v từ mép trong (0) ra mép ngoài (1). Hai mặt cùng vật liệu (single-sided mesh)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    grid = []
    for j in range(nv + 1):
        v = j / nv
        r = r0 + (r1 - r0) * v
        z = h * v ** flare
        grid.append([bm.verts.new((r * math.cos(TAU * i / nu), r * math.sin(TAU * i / nu), z)) for i in range(nu + 1)])
    for j in range(nv):
        for i in range(nu):
            f = bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
            for lp, (u, v) in zip(f.loops, ((i / nu, j / nv), ((i + 1) / nu, j / nv), ((i + 1) / nu, (j + 1) / nv), (i / nu, (j + 1) / nv))):
                lp[uv].uv = (u, v)
    bm.to_mesh(me)
    bm.free()
    return smooth(me)



def water_mat(name, coord="UV", coord_obj=None, flow=None, mask=None, thr=None, tiling=(1.0, 1.0), noise_scale=5.0, nk=0.65,
              offset=None, extension="REPEAT", edge=None, band=None, band_amp=0.25, band_scale=(3.0, 14.0, 1.0), alpha=1.0, speck=None):
    """NƯỚC XANH của mình (flow_color) mà tan được như repo water_vfx:
    - mask + thr: mặt nạ mềm × nhiễu so với ngưỡng theo giờ (như mask_mat); edge = (dải, key) tô viền bọt theo mép đang tan.
    - band = (đuôi, đầu): hai danh sách [(giờ, v)] — hiện khi đuôi < m < đầu, m = v (UV dọc ống) + (nhiễu − 0,5)·band_amp·2:
      nước hiện từ gốc tới ngọn rồi tan từ gốc (tia ống, roi nước). Nhiễu kéo dài dọc ống (band_scale) → mép rách thành sợi.
    - speck = ([(giờ, ngưỡng)], scale): tan LẤM TẤM — nhiễu mịn trên toạ độ `coord` so với ngưỡng theo giờ (khối không UV:
      metaball; repo: cầu nước mờ dần thì vỡ thành chấm).
    coord: "UV" (ống, vành, cầu UV) hoặc "OBJ" (toạ độ Object của coord_obj). flow = tham số flow_color."""
    m, nt, L_ = new_mat(name)
    tc = node(nt, "ShaderNodeTexCoord", (-1600, 0))
    if coord_obj is not None:
        tc.object = coord_obj
    vec = tc.outputs["UV"] if coord == "UV" else tc.outputs["Object"]
    col = flow_color(nt, L_, vec, **(flow or {}))
    alpha_s = None
    if mask:
        mp = node(nt, "ShaderNodeMapping", (-1400, -700))
        mp.inputs["Scale"].default_value = (tiling[0], tiling[1], 1.0)
        L_.new(tc.outputs["UV"], mp.inputs["Vector"])
        ti = node(nt, "ShaderNodeTexImage", (-1200, -700))
        ti.image, ti.extension, ti.interpolation = mask_img(mask), extension, "Cubic"
        L_.new(mp.outputs["Vector"], ti.inputs["Vector"])
        mp2 = node(nt, "ShaderNodeMapping", (-1400, -1000))
        mp2.inputs["Location"].default_value = offset if offset is not None else (rnd.uniform(-9, 9), rnd.uniform(-9, 9), rnd.uniform(-9, 9))
        L_.new(tc.outputs["UV"], mp2.inputs["Vector"])
        nz = node(nt, "ShaderNodeTexNoise", (-1200, -1000))
        nz.inputs["Scale"].default_value = noise_scale
        nz.inputs["Detail"].default_value = 1.0
        nz.inputs["Distortion"].default_value = 0.3
        L_.new(mp2.outputs["Vector"], nz.inputs["Vector"])
        mr = node(nt, "ShaderNodeMapRange", (-1000, -1000))
        mr.clamp = True
        mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = 0.3, 0.7
        L_.new(nz.outputs["Fac"], mr.inputs["Value"])
        f = node(nt, "ShaderNodeMath", (-850, -1000), operation="MULTIPLY_ADD")
        L_.new(mr.outputs["Result"], f.inputs[0])
        f.inputs[1].default_value, f.inputs[2].default_value = nk, 1 - nk
        v = node(nt, "ShaderNodeMath", (-700, -800), operation="MULTIPLY")
        L_.new(ti.outputs["Color"], v.inputs[0])
        L_.new(f.outputs[0], v.inputs[1])
        th = keyed_value(nt, (-850, -600), thr)
        d = node(nt, "ShaderNodeMath", (-550, -700), operation="SUBTRACT")
        L_.new(v.outputs[0], d.inputs[0])
        L_.new(th, d.inputs[1])
        vis = node(nt, "ShaderNodeMath", (-400, -700), operation="GREATER_THAN")
        L_.new(d.outputs[0], vis.inputs[0])
        vis.inputs[1].default_value = 0.0
        alpha_s = vis.outputs[0]
        if edge:
            band_, ek = edge
            ed = node(nt, "ShaderNodeMath", (-400, -500), operation="LESS_THAN")
            L_.new(d.outputs[0], ed.inputs[0])
            ed.inputs[1].default_value = band_
            mx = node(nt, "ShaderNodeMixRGB", (550, 0), blend_type="MIX")
            L_.new(ed.outputs[0], mx.inputs["Fac"])
            L_.new(col, mx.inputs["Color1"])
            mx.inputs["Color2"].default_value = F.lin(C.get(ek, ek))
            col = mx.outputs["Color"]
    if band:
        tail, head = band
        sp = node(nt, "ShaderNodeSeparateXYZ", (-1400, -1400))
        L_.new(tc.outputs["UV"], sp.inputs["Vector"])
        mpb = node(nt, "ShaderNodeMapping", (-1400, -1600))
        mpb.inputs["Scale"].default_value = band_scale
        mpb.inputs["Location"].default_value = (rnd.uniform(-9, 9), rnd.uniform(-9, 9), 0)
        L_.new(tc.outputs["UV"], mpb.inputs["Vector"])
        nzb = node(nt, "ShaderNodeTexNoise", (-1200, -1600))
        nzb.inputs["Scale"].default_value = 1.0
        nzb.inputs["Detail"].default_value = 1.0
        L_.new(mpb.outputs["Vector"], nzb.inputs["Vector"])
        mm = node(nt, "ShaderNodeMath", (-1000, -1500), operation="MULTIPLY_ADD")
        L_.new(nzb.outputs["Fac"], mm.inputs[0])
        mm.inputs[1].default_value = 2 * band_amp
        L_.new(sp.outputs["Y"], mm.inputs[2])
        mm2 = node(nt, "ShaderNodeMath", (-850, -1500), operation="ADD")
        L_.new(mm.outputs[0], mm2.inputs[0])
        mm2.inputs[1].default_value = -band_amp
        tk, hk = keyed_value(nt, (-1000, -1750), tail), keyed_value(nt, (-1000, -1850), head)
        g0 = node(nt, "ShaderNodeMath", (-700, -1600), operation="GREATER_THAN")
        L_.new(mm2.outputs[0], g0.inputs[0])
        L_.new(tk, g0.inputs[1])
        g1 = node(nt, "ShaderNodeMath", (-700, -1750), operation="LESS_THAN")
        L_.new(mm2.outputs[0], g1.inputs[0])
        L_.new(hk, g1.inputs[1])
        ab = node(nt, "ShaderNodeMath", (-550, -1650), operation="MULTIPLY")
        L_.new(g0.outputs[0], ab.inputs[0])
        L_.new(g1.outputs[0], ab.inputs[1])
        if alpha_s is None:
            alpha_s = ab.outputs[0]
        else:
            ab2 = node(nt, "ShaderNodeMath", (-400, -1650), operation="MULTIPLY")
            L_.new(alpha_s, ab2.inputs[0])
            L_.new(ab.outputs[0], ab2.inputs[1])
            alpha_s = ab2.outputs[0]
    if speck:
        sthr, ssc = speck
        mps = node(nt, "ShaderNodeMapping", (-1400, -2000))
        mps.inputs["Location"].default_value = (rnd.uniform(-9, 9), rnd.uniform(-9, 9), rnd.uniform(-9, 9))
        L_.new(vec, mps.inputs["Vector"])
        nzs = node(nt, "ShaderNodeTexNoise", (-1200, -2000))
        nzs.inputs["Scale"].default_value = ssc
        nzs.inputs["Detail"].default_value = 1.0
        L_.new(mps.outputs["Vector"], nzs.inputs["Vector"])
        mrs = node(nt, "ShaderNodeMapRange", (-1000, -2000))
        mrs.clamp = True
        mrs.inputs["From Min"].default_value, mrs.inputs["From Max"].default_value = 0.3, 0.7
        L_.new(nzs.outputs["Fac"], mrs.inputs["Value"])
        ths = keyed_value(nt, (-1000, -2200), sthr)
        gs = node(nt, "ShaderNodeMath", (-800, -2050), operation="GREATER_THAN")
        L_.new(mrs.outputs["Result"], gs.inputs[0])
        L_.new(ths, gs.inputs[1])
        if alpha_s is None:
            alpha_s = gs.outputs[0]
        else:
            ms = node(nt, "ShaderNodeMath", (-600, -2050), operation="MULTIPLY")
            L_.new(alpha_s, ms.inputs[0])
            L_.new(gs.outputs[0], ms.inputs[1])
            alpha_s = ms.outputs[0]
    if alpha_s is not None and alpha < 1:
        am = node(nt, "ShaderNodeMath", (-250, -1000), operation="MULTIPLY")
        L_.new(alpha_s, am.inputs[0])
        am.inputs[1].default_value = alpha
        alpha_s = am.outputs[0]
    out_alpha(m, nt, L_, col, alpha_s, alpha if alpha_s is None else 1.0)
    return m


def arc_tube(name, path, radius, nu=24, nv=120):
    """Ống uốn theo đường `path(s) -> Vector` (s 0..1), bán kính radius(s); UV: u quanh ống, v = s dọc ống. Không nắp (hai đầu
    do dải hai ngưỡng cắt rách)."""
    from mathutils import Vector
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    rows = []
    side = None
    for j in range(nv + 1):
        s_ = j / nv
        p = path(s_)
        tg = (path(min(1.0, s_ + 1e-3)) - path(max(0.0, s_ - 1e-3))).normalized()
        # khung TRUYỀN SONG SONG: hướng ngang của vòng trước chiếu lên mặt vuông góc tiếp tuyến mới → không lật. (Bản cũ lấy tg × Z:
        # ống gần thẳng đứng thì khung lật 180° mỗi khi ống nghiêng đổi bên → toạ độ quanh ống nhảy, vệt màu bị cắt ngang.)
        if side is None:
            ref = Vector((0, 0, 1)) if abs(tg.z) < 0.7 else Vector((0, -1, 0))
            side = tg.cross(ref)
        else:
            side = side - tg * side.dot(tg)
        side.normalize()
        upv = side.cross(tg).normalized()
        r = radius(s_)
        rows.append([bm.verts.new(p + (side * math.cos(TAU * i / nu) + upv * math.sin(TAU * i / nu)) * r) for i in range(nu + 1)])
    for j in range(nv):
        for i in range(nu):
            f = bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
            for lp, (u_, v_) in zip(f.loops, ((i / nu, j / nv), ((i + 1) / nu, j / nv), ((i + 1) / nu, (j + 1) / nv), (i / nu, (j + 1) / nv))):
                lp[uv].uv = (u_, v_)
    bm.to_mesh(me)
    bm.free()
    return smooth(me)
