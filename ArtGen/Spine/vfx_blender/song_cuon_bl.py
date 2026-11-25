# -*- coding: utf-8 -*-
"""Sóng cuộn (một lượt 1,1 s, 27 khung), bộ nước Blender (nuocbl.py), làm theo ảnh mẫu người dùng gửi 2026-11-24 ("VFX Overview Water
Wave", ABitOfGameDev, YouTube Shorts DMdmmbkFwgw: "cách làm chiêu wave trong blender"). Cách làm của mẫu, dựng lại bằng màu phẳng lam:
1. LƯỚI GỐC: một tấm cong — chân thon nhọn nằm trên đất ở chỗ phát (gốc), loe rộng và dựng dần thành vách, đầu xa cuộn mào lăn về trước;
   dáng mỗi khung bằng shape key (cùng số đỉnh). Mặt cắt dọc tính bằng góc tăng dần theo cung (θ = θmax·q^p): cong mạnh dần về mũi mào.
2. NƯỚC TRÔI: nhiễu kéo dài theo dòng (toạ độ UV dọc tấm), trượt từ gốc về mào theo giờ; ramp CONSTANT 4 bậc lam; mặt dưới (mặt sau của
   tấm, thấy trong lòng mào) tối hơn một bậc.
3. MẶT NẠ TAN TỪ DƯỚI: alpha cứng = (u + nhiễu kéo dọc − D(t)) > 0, D chạy từ gốc tới mào → mép tan thành răng giọt; bọt mào tan sau cùng.
4. BỌT (trắng phẳng): dải dày ở mào mép dưới rách theo nhiễu, viền hai mép (mép trái dày), vệt bọt lấm tấm trôi theo dòng.
5. BỌT VĂNG + giọt rơi từ mào lúc tan; BÔNG TOÉ Ở CHÂN lúc sóng bật lên.
Hướng: người dùng xem bản nhìn dọc như mẫu (ψ 62°, máy chếch 32°): "góc này nhìn không rõ, cứ làm bản nhìn hơi chéo ngang"; thử
mào cuộn về trước (nhìn thấy lưng sóng, mào chụp ra khoảng trống) → "bị ngược rồi". Chốt: giữ mào cuộn úp lên mặt sóng như mẫu, quay
sóng để MẶT LÕM nhìn về đích (bên phải) chếch về máy: hướng chân → vách ψ = 140° (vách bên trái hơi lùi sâu), máy chếch xuống 18°.
Sóng trôi về phía chân (đích), bông toé ở chân, bọt và giọt văng về phía đích. (Bản nhìn dọc cũ: render/song_cuon_nhin_doc.)
Đối xứng ngang: lật ngang trong game cho bên kia. Neo: chân sóng (0, 0, 0) trên đất = phía đích. Tuỳ chọn --psi / --pitch (độ).
    blender.exe -b --factory-startup --python song_cuon_bl.py -- <thư_mục_ra> [--frames ..] [--save x.blend]
"""
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402
import nuocbl as W  # noqa: E402

OUT, FRAMES, SAVE = F.args()
T_END = 1.1
N = int(round(T_END * F.FPS)) + 1          # 27 khung
sc = F.reset(N)
TAU = W.TAU
rnd = W.rnd
NU, NW = 72, 26                             # trạm dọc tấm (gốc → mũi mào), trạm ngang
_a = sys.argv[sys.argv.index("--") + 1:]
PSI = math.radians(float(_a[_a.index("--psi") + 1]) if "--psi" in _a else 140.0)       # hướng chân → vách: 140° = vách bên TRÁI hơi lùi sâu, mặt lõm quay về đích (phải) chếch về máy
PITCH = math.radians(float(_a[_a.index("--pitch") + 1]) if "--pitch" in _a else 18.0)  # máy nhìn chếch xuống
D_ = Vector((math.cos(PSI), math.sin(PSI), 0))      # trục đi
L_ = Vector((-math.sin(PSI), math.cos(PSI), 0))     # trục ngang (mặt đất)
Z_ = Vector((0, 0, 1))
S0 = 6.4                                    # dài cung mặt cắt (đơn vị Blender) khi sóng đủ cỡ
HW = 1.7                                   # nửa bề ngang ở mào


def cr(keys, t):
    """Catmull-Rom qua [(t, v)]: vận tốc liền, không khựng ở mốc; ngoài khoảng giữ đầu / cuối."""
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


GROW = [(0, 0.2), (0.06, 0.62), (0.14, 0.92), (0.24, 1.0), (1.1, 1.06)]       # tấm bật lên rất nhanh (mẫu: hiện gần đủ cỡ ngay)
WID = [(0, 0.45), (0.1, 0.82), (0.24, 1.0), (1.1, 1.12)]
THETA = [(0, 60), (0.08, 130), (0.2, 200), (0.4, 235), (0.7, 258), (1.1, 275)]   # mào cuộn úp lại lên mặt sóng (như mẫu)   # mào cuộn dần, lăn về trước
SHIFT = [(0, 0.0), (0.25, -0.3), (1.1, -0.9)]                                   # cả sóng trôi về phía đích (phía chân)
DIS = [(0, -0.3), (0.3, -0.22), (0.42, 0.02), (0.62, 0.42), (0.8, 0.74), (0.95, 0.98), (1.1, 1.3)]   # mép tan: gốc → mào


def profile(t, w):
    """Mặt cắt dọc (NU+1 điểm (x, z)) ở hàng ngang w ∈ [-1, 1]: góc tiếp tuyến θ(q) = θmax·q^3 (phẳng ở chân, dựng dần thành vách,
    mũi cuộn úp lại về phía chân — như mẫu); hai mép ngắn và cuộn ít hơn giữa."""
    S = S0 * cr(GROW, t) * (1 - 0.16 * w * w)
    th = math.radians(cr(THETA, t)) * (1 - 0.1 * w * w)
    ds = S / NU
    x = z = 0.0
    pts = [(0.0, 0.0)]
    for i in range(NU):
        q = (i + 0.5) / NU
        a = th * q ** 3.0
        x += ds * math.cos(a)
        z += ds * math.sin(a)
        pts.append((x, max(0.0, z)))
    return pts


def halfw(u, t):
    """Nửa bề ngang theo vị trí dọc: chân thon nhọn ở gốc, loe đủ rộng từ ~70 % cung."""
    k = min(1.0, u / 0.7)
    k = k * k * (3 - 2 * k)
    return HW * cr(WID, t) * (0.05 + 0.95 * k ** 0.8)


def points(t):
    sh = cr(SHIFT, t)
    out = []
    for j in range(NW + 1):
        w = -1 + 2 * j / NW
        pr = profile(t, w)
        for i, (x, z) in enumerate(pr):
            u = i / NU
            sag = 0.12 * w * w * math.sin(math.pi * min(1.0, u * 1.3))     # lòng tấm hơi trũng theo ngang
            p = D_ * (x + sh) + L_ * (w * halfw(u, t)) + Z_ * (z + sag)
            out.append(p)
    return out


def sheet_mesh(name):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    vs = [bm.verts.new(p) for p in points(0.0)]
    R = NU + 1
    for j in range(NW):
        for i in range(NU):
            a, b, c, d = j * R + i, j * R + i + 1, (j + 1) * R + i + 1, (j + 1) * R + i
            f = bm.faces.new((vs[a], vs[b], vs[c], vs[d]))
            for lp, (uu, vv) in zip(f.loops, ((i / NU, j / NW), ((i + 1) / NU, j / NW), ((i + 1) / NU, (j + 1) / NW), (i / NU, (j + 1) / NW))):
                lp[uv].uv = (uu, vv)
    bm.to_mesh(me)
    bm.free()
    return W.smooth(me)


# ---------------- vật liệu: nước trôi + bọt + mặt nạ tan
def noise(nt, L, vec, loc, scale, dist=0.3):
    nz = W.node(nt, "ShaderNodeTexNoise", loc)
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 1.0
    nz.inputs["Roughness"].default_value = 0.45
    nz.inputs["Distortion"].default_value = dist
    L.new(vec, nz.inputs["Vector"])
    return nz.outputs["Fac"]


def mapping(nt, L, vec, loc, scale, move=None, offset=(0, 0, 0)):
    """Mapping trên UV; move = tốc độ trượt dọc u (đơn vị UV / giây), khoá tuyến tính 0 → T_END."""
    mp = W.node(nt, "ShaderNodeMapping", loc)
    mp.inputs["Scale"].default_value = scale
    L.new(vec, mp.inputs["Vector"])
    for t in (0, T_END):
        mp.inputs["Location"].default_value = (offset[0] - (move or 0) * t, offset[1], offset[2])
        mp.inputs["Location"].keyframe_insert("default_value", frame=F.fr(t))
    return mp.outputs["Vector"]


def math_(nt, L, op, *vals):
    """Nút Math; vals = các đầu vào (socket hoặc số), phần tử cuối là vị trí nút."""
    *vals, loc = vals
    m = W.node(nt, "ShaderNodeMath", loc, operation=op)
    for k, v in enumerate(vals):
        if isinstance(v, (int, float)):
            m.inputs[k].default_value = v
        else:
            L.new(v, m.inputs[k])
    return m.outputs[0]


def wave_mat():
    m, nt, L = W.new_mat("SongCuon")
    tc = W.node(nt, "ShaderNodeTexCoord", (-1600, 0))
    uvs = W.node(nt, "ShaderNodeSeparateXYZ", (-1400, 300))
    L.new(tc.outputs["UV"], uvs.inputs["Vector"])
    U, V = uvs.outputs["X"], uvs.outputs["Y"]
    # nước trôi: vệt thấu kính dài theo dòng (u), trượt từ gốc về mào
    flow = mapping(nt, L, tc.outputs["UV"], (-1400, 0), (2.6, 7.5, 1.0), move=1.1)
    n1 = noise(nt, L, flow, (-1200, 0), 1.0, 0.35)
    hz = math_(nt, L, "MULTIPLY_ADD", U, 0.16, n1, (-1000, 100))            # gần mào sáng hơn một chút
    hz = math_(nt, L, "ADD", hz, -0.08, (-850, 100))
    # lam nhạt + bọt trắng (bộ nước v2, người dùng: "để màu xanh nhạt, có mix bọt trắng thôi"); mặt sau (lòng mào) lam nhạt hơi sâu
    front = W.ramp(nt, (-650, 200), [(0.0, "nhat"), (0.38, "sang"), (0.66, "bot")])
    back = W.ramp(nt, (-650, -50), [(0.0, "nhat"), (0.62, "sang")])
    L.new(hz, front.inputs["Fac"])
    L.new(hz, back.inputs["Fac"])
    geo = W.node(nt, "ShaderNodeNewGeometry", (-650, -300))
    base = W.node(nt, "ShaderNodeMixRGB", (-400, 100), blend_type="MIX")
    L.new(geo.outputs["Backfacing"], base.inputs["Fac"])
    L.new(front.outputs["Color"], base.inputs["Color1"])
    L.new(back.outputs["Color"], base.inputs["Color2"])
    # bọt: dải mào (mép dưới rách, kéo vệt xuống), viền hai mép, vệt lấm tấm trôi
    fm = mapping(nt, L, tc.outputs["UV"], (-1400, -400), (3.0, 11.0, 1.0), move=0.5, offset=(0, 0, 3.7))
    n2 = noise(nt, L, fm, (-1200, -400), 1.0, 0.5)
    crest_u = math_(nt, L, "MULTIPLY_ADD", n2, 0.3, U, (-1000, -400))         # u + 0,3·nhiễu (mép dưới dải bọt rách, kéo vệt xuống)
    ct = W.keyed_value(nt, (-1000, -250), [(0, 1.04), (0.1, 0.97), (0.24, 0.86)])   # dải bọt dày dần khi mào cuộn (mới dựng chỉ viền mỏng)
    crest = math_(nt, L, "GREATER_THAN", crest_u, ct, (-850, -400))
    vc = math_(nt, L, "SUBTRACT", V, 0.5, (-1200, -650))
    va = math_(nt, L, "ABSOLUTE", vc, 0, (-1050, -650))
    em = mapping(nt, L, tc.outputs["UV"], (-1400, -800), (4.0, 9.0, 1.0), move=1.1, offset=(0, 0, 7.1))
    n3 = noise(nt, L, em, (-1200, -800), 1.0, 0.4)
    edge_v = math_(nt, L, "MULTIPLY_ADD", n3, 0.26, va, (-900, -650))      # mép bọt rách
    left = math_(nt, L, "LESS_THAN", V, 0.5, (-900, -850))
    th_e = math_(nt, L, "MULTIPLY_ADD", left, -0.03, 0.6, (-750, -850))      # mép trái (v < 0,5) dày hơn
    edge = math_(nt, L, "GREATER_THAN", edge_v, th_e, (-600, -700))
    fl = mapping(nt, L, tc.outputs["UV"], (-1400, -1100), (5.0, 26.0, 1.0), move=1.1, offset=(0, 0, 11.3))
    n4 = noise(nt, L, fl, (-1200, -1100), 1.0, 0.2)
    fleck = math_(nt, L, "GREATER_THAN", n4, 0.64, (-900, -1100))
    foam = math_(nt, L, "MAXIMUM", crest, edge, (-450, -500))
    foam = math_(nt, L, "MAXIMUM", foam, fleck, (-300, -600))
    col = W.node(nt, "ShaderNodeMixRGB", (0, 0), blend_type="MIX")
    L.new(foam, col.inputs["Fac"])
    L.new(base.outputs["Color"], col.inputs["Color1"])
    col.inputs["Color2"].default_value = F.lin(W.C["bot"])
    patch = math_(nt, L, "LESS_THAN", n2, 0.4, (-300, -300))                 # bọt mào hai tông: mảng lam nhạt lốm đốm trong dải trắng
    patch = math_(nt, L, "MULTIPLY", patch, crest, (-150, -300))
    col2 = W.node(nt, "ShaderNodeMixRGB", (150, 0), blend_type="MIX")
    L.new(patch, col2.inputs["Fac"])
    L.new(col.outputs["Color"], col2.inputs["Color1"])
    col2.inputs["Color2"].default_value = F.lin(W.C["sang"])
    col = col2
    # mặt nạ tan: alpha = (u + 0,22·nhiễu kéo dọc + 0,09·mào − D(t)) > 0 → răng giọt; mào tan sau cùng
    dm = mapping(nt, L, tc.outputs["UV"], (-1400, -1400), (2.0, 13.0, 1.0), offset=(0, 0, 5.3))
    n5 = noise(nt, L, dm, (-1200, -1400), 1.0, 0.3)
    ue = math_(nt, L, "MULTIPLY_ADD", n5, 0.22, U, (-1000, -1400))
    ue = math_(nt, L, "MULTIPLY_ADD", crest, 0.09, ue, (-850, -1400))
    dv = W.keyed_value(nt, (-1000, -1650), [(i / F.FPS, cr(DIS, i / F.FPS)) for i in range(N)])
    al = math_(nt, L, "SUBTRACT", ue, dv, (-700, -1450))
    al = math_(nt, L, "GREATER_THAN", al, 0.11, (-550, -1450))               # +0,11 bù trung bình nhiễu (0,22·0,5)
    W.out_alpha(m, nt, L, col.outputs["Color"], al)
    return m


ob = W.link(bpy.data.objects.new("SongCuon", sheet_mesh("SongCuon")))
ob.data.materials.append(wave_mat())
ob.shape_key_add(name="Goc")
for i in range(N):
    t = i / F.FPS
    kb = ob.shape_key_add(name=f"K{i:02d}")
    for k, p in enumerate(points(t)):
        kb.data[k].co = p
    for f_ in (i, i + 1, i + 2):
        if 1 <= f_ <= N:
            kb.value = 1.0 if f_ == i + 1 else 0.0
            kb.keyframe_insert("value", frame=f_)


def crest_point(t, w):
    pr = profile(t, w)
    best = max(range(len(pr)), key=lambda i: pr[i][1])        # đỉnh cao nhất của mặt cắt
    x, z = pr[best]
    u = best / NU
    return D_ * (x + cr(SHIFT, t)) + L_ * (w * halfw(u, t)) + Z_ * z


def face_cam(o, spin=0.0):
    """Vật phẳng mặt XZ quay về máy nghiêng; spin = xoay trong mặt phẳng của nó (quay quanh y trước, rồi nghiêng quanh x)."""
    o.rotation_mode = "YXZ"
    o.rotation_euler = (-PITCH, spin, 0)


def fly(o, p0, v, t0, life, size, g=7.0, grow=(0.5, 1.0), steps=6):
    """Bay theo đường đạn 3D từ t0 trong life giây: nở rồi co mất."""
    ts = [0.0, max(0.0, t0 - 0.01)] + [t0 + life * k / steps for k in range(steps + 1)] + [t0 + life + 0.01]
    for t in ts:
        if t < t0 or t > t0 + life:
            o.scale = (1e-3,) * 3
            o.location = p0
        else:
            s = t - t0
            q = s / life
            o.location = p0 + v * s - Z_ * (0.5 * g * s * s)
            ss = size * (grow[0] + grow[1] * q) * (1 - q ** 3)
            o.scale = (max(1e-3, ss),) * 3
        o.keyframe_insert("location", frame=F.fr(t))
        o.keyframe_insert("scale", frame=F.fr(t))


BOT, SANG, CHINH = W.flat("Bot", "bot"), W.flat("Sang", "sang"), W.flat("Nhat", "nhat")

# ---- bọt văng hai bên (mép trái dày → văng nhiều hơn), từ nửa trên vách lúc sóng đang cuộn
for k in range(18):
    side = -1 if k % 3 else 1
    t0 = rnd.uniform(0.1, 0.62)
    w = side * rnd.uniform(0.85, 1.0)
    pc = crest_point(t0, w)
    p0 = pc - Z_ * rnd.uniform(0.1, 0.9) - D_ * rnd.uniform(0.0, 0.5)
    v = L_ * (side * rnd.uniform(0.5, 1.2)) + Z_ * rnd.uniform(0.8, 2.2) - D_ * rnd.uniform(0.6, 1.8)   # văng lên rồi rơi về phía đích
    o = W.obj(f"VangBen{k}", W.blob_mesh(f"VangBen{k}", rnd.choice((3, 4, 5)), rnd.uniform(0, TAU), stretch=rnd.uniform(1.3, 2.2)),
              BOT if k % 4 else SANG)
    face_cam(o, rnd.uniform(0, TAU))
    fly(o, p0, v, t0, rnd.uniform(0.32, 0.5), rnd.uniform(0.07, 0.16))

# ---- bụi bọt bắn về trước từ mũi mào lúc lăn
for k in range(12):
    t0 = rnd.uniform(0.25, 0.7)
    w = rnd.uniform(-0.8, 0.8)
    p0 = crest_point(t0, w) - D_ * 0.3
    v = -D_ * rnd.uniform(1.0, 2.4) + Z_ * rnd.uniform(0.2, 1.2) + L_ * rnd.uniform(-0.6, 0.6)
    o = W.obj(f"BuiMao{k}", W.blob_mesh(f"BuiMao{k}", rnd.choice((3, 4)), rnd.uniform(0, TAU), stretch=1.4), BOT)
    face_cam(o)
    fly(o, p0, v, t0, rnd.uniform(0.3, 0.45), rnd.uniform(0.06, 0.12))

# ---- giọt rơi từ mào lúc tan (mẫu: răng giọt lam rồi vài giọt rơi)
for k in range(18):
    t0 = rnd.uniform(0.72, 1.0)
    w = rnd.uniform(-0.95, 0.95)
    p0 = crest_point(t0, w) - Z_ * rnd.uniform(0.0, 0.5)
    v = -D_ * rnd.uniform(0.2, 0.9) + Z_ * rnd.uniform(-0.5, 0.6)
    o = W.drop(f"GiotRoi{k}", (CHINH, SANG, BOT)[k % 3], 1)
    fly(o, p0, v, t0, rnd.uniform(0.25, 0.4), rnd.uniform(0.05, 0.1), g=9.0, grow=(1.0, 0.0))

# ---- bông toé ở gốc lúc sóng bật lên (sao gai lõm phẳng, hai lớp, đổi dạng mỗi 2 khung)
for li, (mat, s2, rik) in enumerate(((SANG, 1.0, 0.36), (BOT, 0.66, 0.42))):
    obs = []
    for vv in range(3):
        pts = [(rnd.uniform(20, 50), 1.3 * s2), (rnd.uniform(65, 90), 1.7 * s2), (rnd.uniform(95, 120), 1.5 * s2),
               (rnd.uniform(135, 160), 1.1 * s2), (rnd.uniform(200, 340), 0.15 * s2)]
        o = W.obj(f"ToeGoc{li}_{vv}", W.star_mesh(f"ToeGoc{li}_{vv}", [(a, l * rnd.uniform(0.85, 1.15)) for a, l in pts], rik), mat,
                  D_ * 0.35 - Vector((0, 0.02 * (li + 1), 0)))
        face_cam(o)
        W.key_scale(o, [(0, 0.0), (0.03, 0.55), (0.12, 0.8), (0.26, 0.6), (0.42, 0.0)])
        obs.append(o)
    W.swap_keys(obs, 0.0, 0.42, 2)
for k in range(10):
    a = math.radians(rnd.uniform(30, 150))
    p0 = D_ * 0.3 + Z_ * 0.1
    v = Vector((math.cos(a), 0, math.sin(a))) * rnd.uniform(2.0, 3.4) - D_ * 0.5
    o = W.drop(f"GiotGoc{k}", (SANG, BOT, CHINH)[k % 3], 1)
    fly(o, p0, v, rnd.uniform(0.0, 0.08), rnd.uniform(0.3, 0.45), rnd.uniform(0.05, 0.09), g=9.0, grow=(1.0, 0.0))

# ---- máy: trực giao, nhìn chếch xuống PITCH; khung vừa mọi điểm của tấm qua mọi khung (+ lề cho bọt văng)
right, up = Vector((1, 0, 0)), Vector((0, math.sin(PITCH), math.cos(PITCH)))
xs, ys = [], []
for i in range(N):
    for p in points(i / F.FPS)[::7]:
        xs.append(p.dot(right))
        ys.append(p.dot(up))
pad = 1.1
x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - 0.5, max(ys) + pad
WPX = int(math.ceil((x1 - x0) / W.UPP / 2) * 2)
HPX = int(math.ceil((y1 - y0) / W.UPP / 2) * 2)
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
view = Vector((0, math.cos(PITCH), -math.sin(PITCH)))
cam_p = right * cx + up * cy - view * 40
W.eevee(tuple(cam_p), WPX, HPX, W.UPP)
sc.camera.rotation_euler = (math.radians(90) - PITCH, 0, 0)
sc.camera.data.clip_end = 200
F.run(OUT, "song_cuon", tuple(cam_p), W.UPP * WPX, WPX, HPX, frames=FRAMES, save=SAVE, save_frame=10)
pp = world_to_camera_view(sc, sc.camera, Vector((0, 0, 0)))
info_p = os.path.join(OUT, "info.json")
info = json.load(open(info_p))
info["anchor"] = [round(pp.x * WPX), round((1 - pp.y) * HPX)]
json.dump(info, open(info_p, "w"))
print("khung", WPX, HPX, "neo that", info["anchor"])
