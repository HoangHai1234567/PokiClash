# -*- coding: utf-8 -*-
"""Sóng nước 3D (một lượt 1,5 s, 36 khung), bộ nước Blender (nuocbl.py). Người dùng chê bản 2D: "sóng nước chưa mượt, làm bằng blender
đi" → mặt nước 3D thật nhìn chếch xuống 14°:
- THÂN: tấm lưới (dọc mặt cắt × sâu) — mặt nước phẳng phía sau → sườn sau thoải → mào → mặt trước dốc lõm → mặt nước phía trước;
- MÀO: tấm cuộn theo cung tròn từ đỉnh lao về trước rồi chúc xuống, đổ ụp lúc vỡ;
- KHỐI ĐẶC đùn theo chiều sâu (thấy mặt cắt phía trước + mặt sóng chạy ra sau); mỗi hàng lệch pha (mào xiên), cao giảm ở hai đầu;
- thông số theo giờ nội suy Catmull-Rom (bản 2D dùng ease từng đoạn → sóng khựng ở mỗi mốc);
- màu theo ĐỘ CAO (đậm ở chân → lam giữa → lam chính → lam sáng → bọt ở mào) cộng nhiễu trôi theo dòng, viền sáng mép; mũi mào trắng bọt;
- lúc đổ: sao gai nước + mảnh cuộn + giọt ở mặt trước.
Hình mỗi khung dựng bằng shape key (cùng số đỉnh). Dùng cho n_song (sóng thần lan trên đất). Neo: gốc (0, 0, 0) — chân sau, giữa chiều sâu.
    blender.exe -b --factory-startup --python song_nuoc_bl.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import json
import math
import os
import sys

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402
import nuocbl as W  # noqa: E402

OUT, FRAMES, SAVE = F.args()
N = 36
sc = F.reset(N)
TAU = W.TAU
rnd = W.rnd
NU, NL, NV = 90, 36, 28          # trạm dọc mặt cắt (thân, mào), hàng theo chiều sâu
YD = 1.4                         # nửa chiều sâu


def cr(keys, t):
    """Catmull-Rom qua [(t, v)] (vận tốc liền, không khựng ở mốc); ngoài khoảng thì giữ đầu / cuối."""
    if t <= keys[0][0]:
        return keys[0][1]
    if t >= keys[-1][0]:
        return keys[-1][1]
    for i in range(len(keys) - 1):
        t1, v1 = keys[i]
        t2, v2 = keys[i + 1]
        if t1 <= t <= t2:
            t0, v0 = keys[i - 1] if i > 0 else (2 * t1 - t2, 2 * v1 - v2)
            t3, v3 = keys[i + 2] if i + 2 < len(keys) else (2 * t2 - t1, 2 * v2 - v1)
            u = (t - t1) / (t2 - t1)
            m1 = (v2 - v0) / (t2 - t0) * (t2 - t1)
            m2 = (v3 - v1) / (t3 - t1) * (t2 - t1)
            h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
            return h00 * v1 + h10 * m1 + h01 * v2 + h11 * m2
    return keys[-1][1]


H_ = [(0, 0.05), (0.2, 1.2), (0.4, 2.3), (0.7, 2.6), (0.9, 2.55), (1.05, 2.0), (1.22, 1.0), (1.38, 0.35), (1.5, 0.06)]
XC = [(0, 0.9), (0.2, 1.6), (0.4, 2.5), (0.7, 3.9), (0.9, 4.8), (1.05, 5.4), (1.22, 5.9), (1.5, 6.4)]
XB = [(0, -0.2), (0.4, 0.0), (0.7, 0.7), (0.9, 1.4), (1.22, 3.2), (1.5, 5.4)]
RC = [(0, 0.15), (0.4, 0.68), (0.7, 1.0), (0.9, 1.15), (1.05, 1.05), (1.22, 0.7), (1.5, 0.15)]   # cuộn to: mào vồng hẳn ra trước
TH = [(0, 20), (0.4, 110), (0.7, 185), (0.9, 230), (1.05, 255), (1.22, 272), (1.5, 280)]
DROP = [(0, 0.0), (0.85, 0.0), (1.05, 0.45), (1.25, 0.85), (1.5, 1.0)]


def row_params(t, y):
    """Mỗi hàng sâu y lệch pha (hàng gần camera — y âm — đi trước một chút: mào xiên), cao giảm ở hai đầu, mào lượn theo sâu."""
    tt = max(0.0, min(1.5, t - 0.04 * (y + YD) / (2 * YD)))   # hàng xa trễ chút: mào xiên ra sau
    amp = 1 - 0.32 * (y + YD) / (2 * YD)        # hàng gần camera (y âm) cao nhất → mặt cắt trước quyết định dáng, khoảng hở dưới mào không bị hàng sau lấp
    H = cr(H_, tt) * amp
    xc = cr(XC, tt) + 0.22 * math.sin(1.4 * y + 0.6)
    return H, xc, cr(XB, tt) + 0.15 * math.sin(1.1 * y), cr(RC, tt) * (0.85 + 0.15 * amp), cr(TH, tt), cr(DROP, tt)


def body_top(t, y):
    """Mặt trên thân (NU+1 điểm x, z): phẳng sau → sườn sau → mào → mặt trước lõm → phẳng trước."""
    H, xc, xb, Rc, th, drop = row_params(t, y)
    xf = xc + 0.42 * H + 0.2
    pts = []
    for i in range(NU + 1):
        u = i / NU
        if u < 0.08:
            k = u / 0.08
            pts.append((xb - 0.5 + 0.5 * k, 0.0))
        elif u < 0.62:
            k = (u - 0.08) / 0.54
            s_ = k * k * (3 - 2 * k)
            pts.append((xb + (xc - xb) * k, H * s_ ** 1.15))
        elif u < 0.92:
            k = (u - 0.62) / 0.3
            pts.append((xc + (xf - xc) * k, H * (1 - k) ** 1.8))
        else:
            k = (u - 0.92) / 0.08
            pts.append((xf + 0.3 * k, 0.0))
    return pts


def body_ring(t, y):
    """Mặt cắt KHỐI ĐẶC: mặt trên trái → phải, rồi đáy (trên đất) phải → trái. Nắp = dải giữa trên[i] và đáy[i]."""
    top = body_top(t, y)
    return top + [(x, 0.0) for x, z in reversed(top)]


def lip_ring(t, y):
    """Mào dày: cung ngoài (đỉnh 90° cuộn về trước) rồi cung trong ngược lại; dày giảm tới mũi; đổ ụp thì bẹt trên mặt nước."""
    H, xc, xb, Rc, th, drop = row_params(t, y)
    cx, cz = xc + 0.04, H - Rc - drop * 0.55 * H
    outer, inner = [], []
    for i in range(NL + 1):
        u = i / NL
        a = math.radians(90 - th * u)
        thick = Rc * 0.62 * (1 - u) ** 0.85 + 0.03
        ri = max(0.01, Rc - thick)
        outer.append((cx + Rc * math.cos(a), max(0.0, cz + Rc * math.sin(a))))
        inner.append((cx + ri * math.cos(a), max(0.0, cz + ri * math.sin(a))))
    return outer + list(reversed(inner))


def solid_mesh(name, n, ring_fn):
    """Khối đùn theo chiều sâu: mỗi hàng một vòng 2(n+1) điểm (n+1 trên / ngoài, n+1 dưới / trong ngược lại); mặt bên nối hàng kề,
    nắp ở hai đầu là các dải giữa điểm i và điểm đối diện. UV u = vị trí dọc mặt cắt (i / n), v = hàng sâu."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    K = 2 * (n + 1)
    rows = []
    for j in range(NV + 1):
        y = -YD + 2 * YD * j / NV
        rows.append([bm.verts.new((x, y, z)) for x, z in ring_fn(0.0, y)])
    def uvu(k):
        return (k if k <= n else K - 1 - k) / n
    for j in range(NV):
        for k in range(K):
            k2 = (k + 1) % K
            f = bm.faces.new((rows[j][k], rows[j][k2], rows[j + 1][k2], rows[j + 1][k]))
            for lp, (uu, vv) in zip(f.loops, ((uvu(k), j / NV), (uvu(k2), j / NV), (uvu(k2), (j + 1) / NV), (uvu(k), (j + 1) / NV))):
                lp[uv].uv = (uu, vv)
    for j in (0, NV):
        for i in range(n):
            f = bm.faces.new((rows[j][i], rows[j][i + 1], rows[j][K - 2 - i], rows[j][K - 1 - i]))
            for lp, uu in zip(f.loops, (i / n, (i + 1) / n, (i + 1) / n, i / n)):
                lp[uv].uv = (uu, j / NV)
    bm.to_mesh(me)
    bm.free()
    return W.smooth(me)


def wave_mat(name, lip=False, boost=0.0):
    """Màu theo độ cao (z / 2,8) + nhiễu trôi theo dòng; viền sáng ở mép bóng; mào: mũi (u > 0,9) trắng bọt."""
    m, nt, L_ = W.new_mat(name)
    tc = W.node(nt, "ShaderNodeTexCoord", (-1100, 0))
    pos = W.node(nt, "ShaderNodeSeparateXYZ", (-900, 200))
    L_.new(tc.outputs["Object"], pos.inputs["Vector"])
    mp = W.node(nt, "ShaderNodeMapping", (-900, -100))
    mp.inputs["Scale"].default_value = (0.4, 1.2, 1.6)
    for t, x in ((0, 0.0), (1.5, -2.2)):
        mp.inputs["Location"].default_value[0] = x
        mp.inputs["Location"].keyframe_insert("default_value", index=0, frame=F.fr(t))
    L_.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = W.node(nt, "ShaderNodeTexNoise", (-700, -100))
    nz.inputs["Scale"].default_value = 1.6
    nz.inputs["Detail"].default_value = 0.0
    nz.inputs["Distortion"].default_value = 0.35
    L_.new(mp.outputs["Vector"], nz.inputs["Vector"])
    hz = W.node(nt, "ShaderNodeMath", (-700, 200), operation="MULTIPLY")
    L_.new(pos.outputs["Z"], hz.inputs[0])
    hz.inputs[1].default_value = 0.8 / 2.8
    nzk = W.node(nt, "ShaderNodeMath", (-500, -100), operation="MULTIPLY_ADD")
    L_.new(nz.outputs["Fac"], nzk.inputs[0])
    nzk.inputs[1].default_value = 0.26
    nzk.inputs[2].default_value = -0.03 + boost   # mào sáng hơn thân một bậc → móc cuộn đọc rõ
    fac = W.node(nt, "ShaderNodeMath", (-350, 100), operation="ADD")
    L_.new(hz.outputs[0], fac.inputs[0])
    L_.new(nzk.outputs[0], fac.inputs[1])
    if lip and boost:      # mào sáng dần dọc cung (u 0,1 → 0,35): ranh màu với thân đi theo dải, không thành đường dọc ở chỗ mào bắt đầu
        nzk.inputs[2].default_value = -0.03
        uvl = W.node(nt, "ShaderNodeSeparateXYZ", (-900, -300))
        L_.new(tc.outputs["UV"], uvl.inputs["Vector"])
        ram = W.node(nt, "ShaderNodeMapRange", (-700, -300))
        ram.clamp = True
        ram.inputs["From Min"].default_value, ram.inputs["From Max"].default_value = 0.1, 0.35
        ram.inputs["To Min"].default_value, ram.inputs["To Max"].default_value = 0.0, boost
        L_.new(uvl.outputs["X"], ram.inputs["Value"])
        f2 = W.node(nt, "ShaderNodeMath", (-250, 100), operation="ADD")
        L_.new(fac.outputs[0], f2.inputs[0])
        L_.new(ram.outputs["Result"], f2.inputs[1])
        fac = f2
    rv = W.ramp(nt, (-150, 100), [(0.0, "dam"), (0.2, "giua"), (0.4, "chinh"), (0.62, "sang"), (0.79, "bot")])
    L_.new(fac.outputs[0], rv.inputs["Fac"])
    lw = W.node(nt, "ShaderNodeLayerWeight", (-350, -300))
    lw.inputs["Blend"].default_value = 0.5
    rim = W.node(nt, "ShaderNodeMath", (-150, -300), operation="GREATER_THAN")
    rim.inputs[1].default_value = 0.985   # gần như tắt: khối đặc có cạnh nắp / mặt trên → viền sáng thành đường vắt ngang
    L_.new(lw.outputs["Facing"], rim.inputs[0])
    col = W.node(nt, "ShaderNodeMixRGB", (100, 0), blend_type="MIX")
    L_.new(rim.outputs[0], col.inputs["Fac"])
    L_.new(rv.outputs["Color"], col.inputs["Color1"])
    col.inputs["Color2"].default_value = F.lin(W.C["sang"])
    uvs = W.node(nt, "ShaderNodeSeparateXYZ", (-900, -500))
    L_.new(tc.outputs["UV"], uvs.inputs["Vector"])
    if lip:                                           # mũi mào trắng bọt
        tip = W.node(nt, "ShaderNodeMath", (-150, -550), operation="GREATER_THAN")
        L_.new(uvs.outputs["X"], tip.inputs[0])
        tip.inputs[1].default_value = 0.9
        c2 = W.node(nt, "ShaderNodeMixRGB", (280, 0), blend_type="MIX")
        L_.new(tip.outputs[0], c2.inputs["Fac"])
        L_.new(col.outputs["Color"], c2.inputs["Color1"])
        c2.inputs["Color2"].default_value = F.lin(W.C["bot"])
        col = c2
    W.out_alpha(m, nt, L_, col.outputs["Color"])
    return m


times = [i / F.FPS for i in range(N)]
for name, nu, fn, mat in (("Than", NU, body_ring, wave_mat("Song")), ("Mao", NL, lip_ring, wave_mat("SongMao", True, 0.16))):
    ob = W.link(bpy.data.objects.new(name, solid_mesh(name, nu, fn)))
    ob.data.materials.append(mat)
    if name == "Mao":
        ob.location.y = -0.05          # nắp mào không trùng mặt phẳng nắp thân (khỏi nhấp nháy)
    ob.shape_key_add(name="Goc")
    for i, t in enumerate(times):
        kb = ob.shape_key_add(name=f"K{i:02d}")
        idx = 0
        for j in range(NV + 1):
            y = -YD + 2 * YD * j / NV
            for x, z in fn(t, y):
                kb.data[idx].co = (x, y, z)
                idx += 1
        for fr_ in (i, i + 1, i + 2):
            if 1 <= fr_ <= N:
                kb.value = 1.0 if fr_ == i + 1 else 0.0
                kb.keyframe_insert("value", frame=fr_)

# ---- đổ ụp ở mặt trước (gần camera): sao gai nước + mảnh cuộn + giọt
BOT, SANG, CHINH = W.flat("Bot", "bot"), W.flat("Sang", "sang"), W.flat("Chinh", "chinh")
GIUA_M = W.flat("GiuaMo", "giua", 0.88)
t_crash = 0.98
H0, xc0, *_ = row_params(t_crash, -YD * 0.6)
xcr = xc0 + 0.7
for li, (mat, s2, yy, rik) in enumerate(((GIUA_M, 1.0, -1.6, 0.34), (SANG, 0.72, -1.65, 0.42))):
    obs = []
    for v in range(3):
        pts = [(rnd.uniform(15, 45), 1.6 * s2), (rnd.uniform(60, 85), 2.0 * s2), (rnd.uniform(95, 125), 1.8 * s2), (rnd.uniform(140, 165), 1.3 * s2),
               (270, 0.12 * s2)]
        ob = W.obj(f"Do{li}_{v}", W.star_mesh(f"Do{li}_{v}", [(a, l * rnd.uniform(0.8, 1.15)) for a, l in pts], rik), mat, (xcr, yy - 0.01 * v, 0.1))
        ob.rotation_euler[0] = math.radians(-14)     # quay mặt về camera nghiêng
        W.key_scale(ob, [(0, 0.0), (t_crash, 0.0), (t_crash + 0.06, 0.9), (t_crash + 0.2, 1.1), (t_crash + 0.36, 0.8), (1.45, 0.0)])
        obs.append(ob)
    W.swap_keys(obs, t_crash, 1.45, 2)
for k in range(14):
    t0 = t_crash + rnd.uniform(0, 0.25)
    a = math.radians(rnd.uniform(25, 150))
    v = rnd.uniform(2.6, 4.4)
    ob = W.obj(f"Cuon{k}", W.blob_mesh(f"Cuon{k}", rnd.choice((3, 4, 5)), rnd.uniform(0, TAU)), SANG if k % 3 else CHINH)
    hi = W.obj(f"CuonSang{k}", W.blob_mesh(f"CuonSang{k}", 3, rnd.uniform(0, TAU)), BOT)
    hi.parent = ob
    hi.location, hi.scale = (0.25, -0.02, 0.18), (0.42, 0.42, 0.42)
    W.ballistic(ob, (xcr + rnd.uniform(-0.8, 0.4), -1.5, rnd.uniform(0.3, 1.4)), (v * math.cos(a), v * math.sin(a)), t0, rnd.uniform(0.4, 0.6),
                g=7.0, size=rnd.uniform(0.2, 0.3))
DR = (BOT, SANG, CHINH)
for k in range(34):
    t0 = rnd.uniform(0.3, 1.3)
    y0 = rnd.uniform(-YD, YD)
    H, xc, *_ = row_params(t0, y0)
    a = math.radians(rnd.uniform(20, 140))
    v = rnd.uniform(1.8, 4.0)
    ob = W.drop(f"Giot{k}", DR[k % 3], 1)
    W.ballistic(ob, (xc + rnd.uniform(-0.2, 0.6), y0 - 0.2, H * rnd.uniform(0.75, 1.0)), (v * math.cos(a), v * math.sin(a)), t0,
                rnd.uniform(0.35, 0.6), g=8.0, size=rnd.uniform(0.05, 0.1), grow=(1.0, 0.0), align=False)

# ---- camera chếch xuống 14°, trực giao; điểm neo tính bằng chiếu thật (F.run giả định camera nằm ngang)
WPX, HPX = 470, 270
CAM = (3.4, -30, 1.45 + 30 * math.tan(math.radians(14)))
W.eevee(CAM, WPX, HPX, W.UPP)
sc.camera.rotation_euler = (math.radians(90 - 14), 0, 0)
F.run(OUT, "song_nuoc", CAM, W.UPP * WPX, WPX, HPX, frames=FRAMES, save=SAVE, save_frame=18, anchor_xz=(0, 0))
p = world_to_camera_view(sc, sc.camera, __import__("mathutils").Vector((0, 0, 0)))
info_p = os.path.join(OUT, "info.json")
info = json.load(open(info_p))
info["anchor"] = [round(p.x * WPX), round((1 - p.y) * HPX)]
json.dump(info, open(info_p, "w"))
print("neo that", info["anchor"])
