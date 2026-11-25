# -*- coding: utf-8 -*-
"""Bộ nước LÀM THEO REPO abitofgamedev/water_vfx (người dùng 2026-11-24: "nhìn không khác mấy, làm lại vfx theo hướng repo tôi gửi"
rồi "đổi texture trong suốt sang kiểu nước xanh như của mình"): lấy DÁNG, BỐ CỤC, NHỊP của repo (skill vfx-petclash/
hoc_water_vfx_abitofgamedev.md), thay chất nước trong suốt (khúc xạ + Fresnel) bằng NƯỚC XANH của bộ nước (nuocbl.flow_color: vệt
thấu kính lam 6 bậc, vệt sáng, mép sáng) + tan theo ngưỡng / dải hai ngưỡng (nuocbl.water_mat). Không phát sáng, màu phẳng.
  --phan cau  Cầu ném (lặp 1 s): cầu nước rung như thạch (dời đỉnh theo nhiễu, nảy dẹt nhẹ) + ĐUÔI cục nước nhỏ dần (repo: 10/giây,
              cỡ 0,64 → 0,26, trọng lực nhẹ) tan lấm tấm theo tuổi + giọt. Bay sang PHẢI, neo tâm cầu.
  --phan toe  Toé đất (1 s): 2 vành vương miện thấp loang trên đất (repo SplashWave: nở đủ ~0,25 s, mặt nạ mây loang lặp 4,14 × 0,91
              quanh vành, ngưỡng 0,11 → 1), 14 chấm toé, 10 vệt nước bay toả + trọng lực, 30 giọt, 2 vũng nằm đất. Neo tâm trên đất.
  --phan ong  Tia ống (1,6 s): ống nước uốn vòng cung từ miệng (trái) sang đích (phải), rung theo nhiễu, vệt nước chảy dọc ống; dải
              hai ngưỡng: hiện từ miệng tới đích (0–0,3 s) rồi tan từ miệng (1,0–1,38 s) (repo WaterTube); bông nước ở miệng; ở đích
              toé lặp (vương miện ngửa về phía tới + chấm toé + giọt) suốt lúc ống chạm. Neo miệng; điểm chạm = cuối ống (in ra).
  --phan roi  Roi nước (1 s): cùng ống vòng cung nhưng chỉ một ĐOẠN nước chạy dọc đường (repo roi spline), tới đích thì toé.
  BỘ v2 ("dựa theo shader của họ rồi tự build ... tất cả theo ý mình, lốc nước ok rồi"): chất nước chung WATER (lam nhạt + bọt,
  khối cel, mép lam sâu), cầu và thương bằng METABALL (đuôi liền thân), thêm:
  --phan tia (1,6 s) tia nước thẳng · thuong (lặp 0,5 s) thương nước · phun (1,6 s) mạch phun · than (1 s) toé trúng thân ·
  vo (1 s) cầu vỡ.
Vũng dưới chân đích: bộ vung_nuoc (toe_nuoc_bl.py --phan vung) ghép trễ ở trang xem.
    blender.exe -b --factory-startup --python nuoc_repo_bl.py -- <thư_mục_ra> --phan cau|toe|ong|roi [--frames ..] [--save x.blend]
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxbl as F  # noqa: E402
import nuocbl as W  # noqa: E402

OUT, FRAMES, SAVE = F.args()
_a = sys.argv[sys.argv.index("--") + 1:]
PHAN = _a[_a.index("--phan") + 1] if "--phan" in _a else "cau"
T = {"cau": 1.0, "toe": 1.0, "ong": 1.6, "roi": 1.0, "tia": 1.6, "thuong": 0.5, "phun": 1.6, "than": 1.0, "vo": 1.0}[PHAN]
N = int(round(T * F.FPS))
sc = F.reset(N)
TAU = W.TAU
rnd = W.rnd
PITCH = math.radians({"cau": 8, "toe": 28, "ong": 8, "roi": 8, "tia": 4, "thuong": 4, "phun": 12, "than": 20, "vo": 20}[PHAN])
Z = Vector((0, 0, 1))
# CHẤT NƯỚC CHUNG của bộ v2: lam nhạt + bọt trắng (STOPS_NHAT), khối cel 3 dải theo hướng sáng (vol), mép lam sâu (rim "nhat") —
# thay khúc xạ + Fresnel của repo bằng dải phẳng; vệt sáng theo pháp tuyến tắt (ranh răng cưa theo mặt lưới).
WATER = dict(hi_axis="Z", hi_th=2.0, rim_th=0.6, rim_key="nhat", noise_scale=1.4, stops=W.STOPS_NHAT, vol=(-0.45, -0.55, 0.75, 0.16))
FLAT = dict(WATER, vol=None)    # vật nằm ngửa trên đất (vũng): không tô khối (pháp tuyến hằng)
BOT, SANG = W.flat("Bot", "bot"), W.flat("Sang", "sang")
CHINH = GIUA = W.flat("Nhat", "nhat")   # hạt nhỏ cũng chỉ lam nhạt + trắng


def face_cam(o, spin=0.0):
    o.rotation_mode = "YXZ"
    o.rotation_euler = (-PITCH, spin, 0)


def key_s(o, pairs, axes=(1, 1, 1)):
    for t, s in pairs:
        o.scale = tuple(max(1e-3, s * a) for a in axes)
        o.keyframe_insert("scale", frame=F.fr(t))


def fly(o, p0, v, t0, life, size, g=9.0, grow=(1.0, 0.0), steps=6):
    """Bay đường đạn 3D từ t0 trong life giây, nở / co theo grow, ẩn ngoài khoảng."""
    ts = [0.0, max(0.0, t0 - 0.01)] + [t0 + life * k / steps for k in range(steps + 1)] + [t0 + life + 0.01]
    for t in ts:
        if t < t0 or t > t0 + life:
            o.scale = (1e-3,) * 3
            o.location = p0
        else:
            s = t - t0
            q = s / life
            o.location = p0 + v * s - Z * (0.5 * g * s * s)
            o.scale = (max(1e-3, size * (grow[0] + grow[1] * q) * (1 - q ** 3)),) * 3
        o.keyframe_insert("location", frame=F.fr(t))
        o.keyframe_insert("scale", frame=F.fr(t))


def wobble(ob, strength, size=0.8, period=None, drift=(0, 0, 0)):
    """Rung như thạch (repo WaterVertexDisplacement): dời đỉnh theo pháp tuyến × nhiễu mây, toạ độ nhiễu xoay vòng (lặp liền nếu
    period) và trôi theo drift."""
    e = F.empty(ob.name + "_Rung")
    P = period or T
    for t, a in ((0, 0.0), (P, TAU)):
        e.rotation_euler = (a * 0.5, 0, a)
        e.keyframe_insert("rotation_euler", frame=F.fr(t))
    if any(drift):
        for t, k in ((0, 0.0), (T, 1.0)):
            e.location = Vector(drift) * k
            e.keyframe_insert("location", frame=F.fr(t))
    tex = bpy.data.textures.new(ob.name + "_Gon", "CLOUDS")
    tex.noise_scale = size
    d = ob.modifiers.new("Rung", "DISPLACE")
    d.texture, d.texture_coords, d.texture_coords_object, d.strength, d.mid_level = tex, "OBJECT", e, strength, 0.5


def crown(name, pos, axis, t0, t1, t_end, size, mask="ngon_0", til=2.0, r0=0.3, r1=1.6, h=1.4, flare=1.3, thr_end=0.95):
    """Vương miện vành nón nước xanh, trục `axis`, nở 0,3 → 1 trong [t0, t1], tan theo mặt nạ tới t_end (viền bọt trắng)."""
    ring = W.link(bpy.data.objects.new(name, W.ring_cone(name, r0, r1, h, flare=flare)))
    ring.data.materials.append(W.water_mat(name + "M", coord="UV", flow=dict(scale=(7.0, 1.4, 1.0), move=(T, (0, -2.0, 0)), **WATER),
                                           mask=mask, thr=[(t0, 0.02), (t1, 0.08), (t_end, thr_end)], tiling=(til, 1.0), noise_scale=4.0,
                                           nk=0.45, edge=(0.05, "bot")))
    ring.rotation_mode = "QUATERNION"
    ring.rotation_quaternion = Z.rotation_difference(Vector(axis).normalized())
    ring.location = pos
    key_s(ring, [(0, 0.0), (max(0.0, t0 - 0.01), 0.0), (t0, 0.3 * size), (t1, size), (t_end, 1.1 * size), (t_end + 0.01, 0.0)])
    return ring


def blob(name, pos, t0, life, s, mk, drift=(0, 0, 0)):
    """Chấm toé nước xanh (sprite cụm chấm), tan theo ngưỡng 0,14 → 1 trong life giây, viền bọt trắng."""
    o = W.link(bpy.data.objects.new(name, W.quad(name, s, s)))
    o.data.materials.append(W.water_mat(name + "M", coord="UV", flow=dict(scale=(2.2, 2.2, 1.0), **WATER), mask=mk,
                                        thr=[(t0, 0.14), (t0 + life, 1.0)], extension="CLIP", noise_scale=4.0, edge=(0.06, "bot")))
    face_cam(o, rnd.uniform(0, TAU))
    for i in range(7):
        q = i / 6
        o.location = Vector(pos) + Vector(drift) * (1 - (1 - q) ** 2)
        o.keyframe_insert("location", frame=F.fr(t0 + life * q))
    key_s(o, [(0, 0.0), (max(0.0, t0 - 0.01), 0.0), (t0, 0.6), (t0 + life * 0.4, 1.0), (t0 + life, 1.1), (t0 + life + 0.01, 0.0)])
    return o


def burst(tag, p, back, t0, n_blob=6, n_drop=14, n_trail=4, size=1.0, star=True):
    """Một lượt toé tại p, toé NGƯỢC theo hướng `back` (đơn vị, mặt XZ): chớp sao, chấm toé, giọt, vệt."""
    bx, bz = back.x, back.z
    if star:
        pts = [(a + rnd.uniform(-12, 12), (1.0 if k % 2 == 0 else 0.6) * 0.9 * size) for k, a in enumerate(range(0, 360, 45))]
        o = W.obj(f"{tag}Chop", W.star_mesh(f"{tag}Chop", pts, 0.34), BOT, p - Vector((0, 0.8, 0)))
        face_cam(o, rnd.uniform(0, TAU))
        key_s(o, [(0, 0.0), (max(0.0, t0 - 0.01), 0.0), (t0 + 0.03, 0.9), (t0 + 0.07, 1.0), (t0 + 0.13, 0.0)])
    for k in range(n_blob):
        q0 = t0 + rnd.uniform(0.0, 0.12)
        off = Vector((bx, 0, bz)) * rnd.uniform(0.2, 1.3) + Vector((rnd.uniform(-0.5, 0.5), -0.9 - 0.02 * k, rnd.uniform(-0.4, 0.8)))
        blob(f"{tag}Cham{k}", p + off * size, q0, rnd.uniform(0.4, 0.55), rnd.uniform(0.9, 1.6) * size, f"cham_{k % 3}",
             drift=Vector((bx, 0, bz + 0.2)) * rnd.uniform(0.2, 0.6))
    for k in range(n_drop):
        a = math.atan2(bz, bx) + rnd.uniform(-1.1, 1.1)
        v = Vector((math.cos(a), 0, math.sin(a) + 0.4)) * rnd.uniform(3.0, 6.5) * size
        fly(W.drop(f"{tag}Giot{k}", (BOT, SANG, CHINH)[k % 3], 1), p + Vector((0, -0.7, 0)), v, t0 + rnd.uniform(0, 0.1),
            rnd.uniform(0.38, 0.55), rnd.uniform(0.04, 0.09) * size)
    for k in range(n_trail):
        a = math.atan2(bz, bx) + rnd.uniform(-0.8, 0.8)
        sp = rnd.uniform(4.0, 6.0) * size
        o = W.obj(f"{tag}Vet{k}", W.blade_mesh(f"{tag}Vet{k}", -rnd.uniform(0.7, 1.0) * size, 0.13 * size, notch=0.3), CHINH if k % 2 else GIUA,
                  p + Vector((0, -0.6, 0)))
        W.ballistic(o, tuple(p + Vector((0, -0.6 - 0.01 * k, 0))), (sp * math.cos(a), sp * math.sin(a)), t0 + rnd.uniform(0, 0.08),
                    rnd.uniform(0.42, 0.52), g=9.0, size=1.0, grow=(0.7, 0.5))


# ===================================================================== CẦU NÉM
def part_cau():
    """Cầu ném bằng METABALL (người dùng: cầu repo "rất 3D, đuôi không bị tách", của mình "đuôi cứ kiểu bị tách ra"): mọi cục cùng một
    họ metaball nên tự hoà thành MỘT khối — đuôi liền thân, thon dần, chót tự thắt lại thành giọt (cục nhỏ dưới ngưỡng thì tách / mất).
    Repo liền nhờ hạt cầu chồng dày + khúc xạ; ở đây đục, màu nước xanh nhạt tô khối cel 3 dải (flow_color vol)."""
    P = T
    truc = F.empty("Truc")
    mat = W.flow_mat("CauNem", truc, scale=(0.55, 0.55, 2.6), spin=(P, 2, 1), **WATER)

    def elem(name, r):
        mb = bpy.data.metaballs.new(name)
        mb.resolution, mb.render_resolution, mb.threshold = 0.1, 0.04, 0.6
        e = mb.elements.new()
        e.radius, e.stiffness = r, 2.0
        o = W.link(bpy.data.objects.new(name, mb))
        return o

    base = elem("CauMB", 1.4)                  # đối tượng gốc của họ: vật liệu + độ mịn lấy từ đây
    base.data.materials.append(mat)
    for i in range(9):                          # nảy dẹt nhẹ hai nhịp mỗi vòng (thạch)
        k = math.sin(TAU * 2 * i / 8)
        base.scale = (1 + 0.06 * k, 1, 1 - 0.06 * k)
        base.keyframe_insert("scale", frame=F.fr(P * i / 8))
    # rung kiểu thạch: 4 cục nhỏ chạy vòng sát mặt trong cầu → mặt cầu phồng xẹp chỗ này chỗ kia (lặp liền: số vòng nguyên)
    for k, (tilt, turns, rr, dist) in enumerate(((20, 1, 0.55, 0.62), (75, -1, 0.5, 0.6), (130, 2, 0.45, 0.66), (-40, -2, 0.5, 0.58))):
        o = elem(f"CauMB.{k + 1:03d}", rr)
        ph = rnd.uniform(0, TAU)
        for i in range(N + 1):
            a = ph + TAU * turns * i / N
            v = Vector((math.cos(a), math.sin(a), 0)) * dist
            v.rotate(__import__("mathutils").Euler((math.radians(tilt), math.radians(tilt * 0.5), 0)))
            o.location = v
            o.keyframe_insert("location", frame=F.fr(P * i / N))
    # đuôi: 16 cục lệch pha đều, sinh trong lòng cầu, lùi ra sau, nhỏ dần, rơi nhẹ → hoà liền thành đuôi thon (repo 0,64 → 0,26)
    NB = 16
    for k in range(NB):
        ph = k / NB
        jz, jy = rnd.uniform(-0.12, 0.12), rnd.uniform(-0.1, 0.1)
        o = elem(f"CauMB.{k + 10:03d}", 1.0)
        for i in range(N + 1):
            q = (i / N + ph) % 1.0
            o.location = (-0.7 - 2.8 * q, jy, jz * (1 - q) - 0.38 * q * q)
            sz = 0.52 * (1 - q) ** 0.9 + 0.05
            o.scale = (sz * 1.15, sz, sz)
            o.keyframe_insert("location", frame=F.fr(P * i / N))
            o.keyframe_insert("scale", frame=F.fr(P * i / N))
    # giọt rời ở chót đuôi + văng (khác họ metaball → không hoà)
    for k in range(10):
        ob = W.drop(f"Giot{k}", (BOT, SANG, CHINH)[k % 3], 1)
        ph = k / 10
        a0 = math.radians(rnd.uniform(-50, 50))
        sp = rnd.uniform(1.0, 1.8)
        sz = rnd.uniform(0.05, 0.09)
        for i in range(N + 1):
            q = (i / N + ph) % 1.0
            ob.location = (-2.2 - sp * q, -0.4, 0.2 * math.sin(a0) + 0.5 * math.sin(a0) * q - 0.8 * q * q - 0.3)
            s_ = sz * (1 - q) ** 0.7
            ob.scale = (s_ * 1.4, s_, s_)
            ob.keyframe_insert("location", frame=F.fr(P * i / N))
            ob.keyframe_insert("scale", frame=F.fr(P * i / N))
    return 320, 240, -1.3, -0.4, "cau_nem", True


# ===================================================================== TOÉ ĐẤT
def part_toe():
    for k, (r1, h, sz, t0, t1, mk, rz) in enumerate(((2.0, 1.0, 1.0, 0.0, 0.25, "loang_0", 0), (1.65, 1.25, 0.85, 0.03, 0.31, "loang_1", 40))):
        ring = W.link(bpy.data.objects.new(f"VanhDat{k}", W.ring_cone(f"VanhDat{k}", 0.5, r1, h, flare=1.5)))
        ring.data.materials.append(W.water_mat(f"VanhDatM{k}", coord="UV", flow=dict(scale=(7.0, 1.3, 1.0), move=(T, (0, -1.6, 0)), **WATER),
                                               mask=mk, thr=[(0, 0.11), (T, 1.0)], tiling=(4.14, 0.91), noise_scale=5.0, nk=0.65,
                                               edge=(0.035, "bot")))
        ring.rotation_euler = (0, 0, math.radians(rz))
        ring.location = (0, 0.05 * k, 0)
        key_s(ring, [(0, 0.0), (t0, 0.33 * sz), (t1, sz), (T, 1.12 * sz)])
    for k in range(14):                                       # chấm toé quanh tâm, trên đất
        a = rnd.uniform(0, TAU)
        r = rnd.uniform(0.3, 1.6)
        p = Vector((r * math.cos(a) * 1.2, -0.9 + r * math.sin(a) * 0.5, rnd.uniform(0.3, 1.4)))
        blob(f"Cham{k}", p, rnd.uniform(0.0, 0.12), rnd.uniform(0.42, 0.55), rnd.uniform(1.0, 1.9), f"cham_{k % 3}",
             drift=Vector((math.cos(a) * 0.5, 0, rnd.uniform(0.1, 0.5))))
    for k in range(10):                                       # vệt nước bay toả + trọng lực (repo: tốc 5,9, đời 0,52)
        a = math.radians(rnd.uniform(35, 145))
        sp = rnd.uniform(4.5, 6.2)
        o = W.obj(f"Vet{k}", W.blade_mesh(f"Vet{k}", -rnd.uniform(0.7, 1.1), 0.14, notch=0.3), CHINH if k % 2 else GIUA, (0, -0.8, 0.2))
        W.ballistic(o, (rnd.uniform(-0.4, 0.4), -0.8 - 0.01 * k, 0.2), (sp * math.cos(a), sp * math.sin(a)), rnd.uniform(0, 0.06),
                    rnd.uniform(0.45, 0.55), g=9.0, size=1.0, grow=(0.7, 0.5))
    for k in range(30):                                       # giọt (repo 30, cỡ 0,03–0,08, tốc 5,9, trọng lực)
        a = rnd.uniform(0, TAU)
        v = Vector((math.cos(a) * rnd.uniform(1.5, 3.5), math.sin(a) * rnd.uniform(1.0, 2.0), rnd.uniform(3.0, 5.5)))
        fly(W.drop(f"Giot{k}", (BOT, SANG, CHINH)[k % 3], 1), Vector((0, -0.2, 0.2)), v, rnd.uniform(0, 0.1), rnd.uniform(0.4, 0.55),
            rnd.uniform(0.04, 0.08))
    for k, (s, off, t0, mk) in enumerate(((3.4, (0, 0), 0.0, "vung_0"), (2.3, (0.8, 0.4), 0.05, "vung_1"))):   # 2 vũng (repo cỡ 4)
        o = W.link(bpy.data.objects.new(f"Vung{k}", W.quad(f"Vung{k}", s, s * 0.85, "XY")))
        o.data.materials.append(W.water_mat(f"VungM{k}", coord="UV", flow=dict(scale=(1.6, 1.6, 1.0), **FLAT), mask=mk,
                                            thr=[(t0, 0.02), (0.4, 0.1), (T, 1.0)], extension="CLIP", noise_scale=3.5, edge=(0.05, "bot")))
        o.location = (off[0], off[1], -0.01 - 0.002 * k)
        key_s(o, [(0, 0.0), (t0, 0.2), (t0 + 0.16, 1.0), (T, 1.05)])
    return 520, 400, 0.0, 0.6, "toe_dat", False


# ===================================================================== TIA ỐNG / ROI NƯỚC
L, H = 10.0, 2.6


def path(s):
    return Vector((L * s, 0, H * 4 * s * (1 - s) - 0.4 * s))


def part_ong(roi=False):
    rad = (lambda s: 0.34 * (0.7 + 0.3 * math.sin(math.pi * s) ** 0.5)) if not roi else (lambda s: 0.3 * (0.75 + 0.25 * math.sin(math.pi * s)))
    tube = W.link(bpy.data.objects.new("Ong", W.arc_tube("Ong", path, rad, 28, 160)))
    if roi:   # một đoạn nước chạy dọc vòng cung (roi), tới đích lúc ~0,36 s
        band = ([(0, -0.5), (0.1, -0.42), (0.3, 0.28), (0.5, 1.2)], [(0, -0.05), (0.18, 0.55), (0.36, 1.2)])
        t_hit, hold = 0.34, 0.0
    else:     # hiện từ miệng tới đích rồi tan từ miệng (repo WaterTube: hai ngưỡng trên một dải dọc ống)
        band = ([(0, -0.3), (1.0, -0.3), (1.12, 0.25), (1.26, 0.7), (1.38, 1.2)], [(0, -0.1), (0.12, 0.45), (0.22, 0.85), (0.3, 1.2)])
        t_hit, hold = 0.28, 1.05
    tube.data.materials.append(W.water_mat("OngM", coord="UV", flow=dict(scale=(1.8, 3.2, 1.0), move=(T, (0, -5.0, 0)), **FLAT),   # FLAT: tắt vệt sáng đỉnh — ranh pháp tuyến răng cưa theo mặt lưới thành sọc
                                           band=band, band_amp=0.06, band_scale=(4.0, 18.0, 1.0)))
    # ống kín vẽ trong mờ (BLENDED vì có alpha): mặt trong bị vẽ đè lẫn với mặt ngoài → sọc răng lược theo từng vòng lưới. Bỏ mặt sau.
    tube.data.materials[0].use_backface_culling = True
    try:
        tube.data.materials[0].use_transparency_overlap = False
    except AttributeError:
        pass
    # không rung ống: dời đỉnh làm mặt lưới vênh → vệt sáng đỉnh / mép nhấp nháy theo từng vòng lưới thành sọc răng lược (đã thử 0,12 và 0,06)
    # bông nước ở miệng lúc phóng
    burst("Mieng", path(0.0) + Vector((0.2, 0, 0)), Vector((0.6, 0, 0.8)).normalized(), 0.0, n_blob=3, n_drop=8, n_trail=0, size=0.6)
    # toé ở đích: ngược hướng tới (tiếp tuyến cuối ống)
    p1 = path(1.0)
    tg = (path(1.0) - path(0.97)).normalized()
    back = Vector((-tg.x, 0, -tg.z + 0.6)).normalized()
    times = [t_hit] if roi else [t_hit, t_hit + 0.3, t_hit + 0.6]
    for k, tb in enumerate(times):
        crown(f"VM{k}", p1 - tg * 0.15 + Vector((0, 0.1 * k, 0)), back, tb, tb + 0.18, tb + (0.55 if roi else 0.5), 0.85 if k else 1.0,
              mask=f"ngon_{k % 3}")
        burst(f"Dich{k}", p1, back, tb, n_blob=6 if k == 0 else 4, n_drop=14, n_trail=4 if k == 0 else 2, size=1.0, star=(k == 0))
    if not roi:   # toé nhỏ lặp liên tục giữa các lượt lớn suốt lúc ống chạm
        tb = t_hit + 0.15
        while tb < hold + 0.25:
            burst(f"Lap{int(tb * 100)}", p1, back, tb, n_blob=2, n_drop=6, n_trail=1, size=0.7, star=False)
            tb += 0.15
    print("diem cham (px tu mieng):", round((p1.x) / W.UPP), round(-(p1.z) / W.UPP))
    return 700, 320, L / 2, 1.0, ("roi_nuoc" if roi else "tia_ong"), False


# ===================================================================== bộ v2: phần dùng chung
def metaball(name, r, mat=None):
    """Một cục metaball (cùng tiền tố tên trước dấu chấm = cùng họ, tự hoà). Đối tượng gốc (không số) mang vật liệu + độ mịn."""
    mb = bpy.data.metaballs.new(name)
    mb.resolution, mb.render_resolution, mb.threshold = 0.1, 0.04, 0.6
    e = mb.elements.new()
    e.radius, e.stiffness = r, 2.0
    o = W.link(bpy.data.objects.new(name, mb))
    if mat is not None:
        mb.materials.append(mat)
    return o


def cull(ob):
    """Khối kín có alpha (BLENDED): bỏ mặt sau, kẻo mặt trong vẽ đè lẫn thành sọc theo vòng lưới."""
    for m in ob.data.materials:
        m.use_backface_culling = True
        try:
            m.use_transparency_overlap = False
        except AttributeError:
            pass


def water_tube(name, pth, rad, band, flow_scale, flow_move, nu=40, nv=200):
    tube = W.link(bpy.data.objects.new(name, W.arc_tube(name, pth, rad, nu, nv)))
    tube.data.materials.append(W.water_mat(name + "M", coord="UV", flow=dict(scale=flow_scale, move=(T, flow_move), **WATER), band=band,
                                           band_amp=0.05, band_scale=(4.0, 20.0, 1.0)))
    cull(tube)
    return tube


# ===================================================================== TIA NƯỚC (thẳng)
def part_tia():
    """Tia nước v2: ống thẳng hơi gợn (miệng thon), đầu tia lao tới đích trong 0,1 s rồi PHÌNH (vượt cỡ rồi về, phập phồng), vệt nước
    chảy rất nhanh dọc ống, đuôi tan rách từ miệng 1,1–1,46 s (dải hai ngưỡng); đích toé NGƯỢC về người bắn liên tục (vương miện +
    chấm toé + giọt), bông nước ở miệng. Neo miệng; điểm chạm (10, 0) = 493 px."""
    L2 = 10.0
    pth = lambda s_: Vector((L2 * s_, 0, 0.16 * math.sin(TAU * 1.5 * s_) * math.sin(math.pi * s_)))
    rad = lambda s_: 0.5 * (0.55 + 0.45 * min(1.0, s_ / 0.12))
    band = ([(0, -0.3), (1.1, -0.3), (1.25, 0.35), (1.38, 0.8), (1.46, 1.2)], [(0, -0.05), (0.1, 1.2)])
    tube = water_tube("Tia", pth, rad, band, (1.8, 4.5, 1.0), (0, -8.0, 0))
    for t, r in ((0, 0.3), (0.1, 0.35), (0.16, 0.5), (0.22, 1.2), (0.27, 1.0), (0.5, 1.08), (0.7, 0.96), (0.9, 1.06), (1.1, 1.0), (1.25, 0.8),
                 (1.46, 0.45)):
        tube.scale = (1, r, r)
        tube.keyframe_insert("scale", frame=F.fr(t))
    burst("Mieng", Vector((0.25, 0, 0)), Vector((0.6, 0, 0.8)).normalized(), 0.0, n_blob=3, n_drop=8, n_trail=0, size=0.6)
    p1 = Vector((L2, 0, 0))
    back = Vector((-1, 0, 0.55)).normalized()
    for k, tb in enumerate((0.1, 0.42, 0.74, 1.06)):
        crown(f"VM{k}", p1 + Vector((0.1, 0.1 * k, 0)), back, tb, tb + 0.16, tb + 0.48, 1.0 if k == 0 else 0.8, mask=f"ngon_{k % 3}")
        burst(f"Dich{k}", p1, back, tb, n_blob=6 if k == 0 else 4, n_drop=14, n_trail=4 if k == 0 else 2, size=1.0, star=(k == 0))
    tb = 0.22
    while tb < 1.4:
        burst(f"Lap{int(tb * 100)}", p1, back, tb, n_blob=2, n_drop=6, n_trail=1, size=0.7, star=False)
        tb += 0.12
    return 700, 300, L2 / 2, 0.3, "tia_nuoc2", False


# ===================================================================== THƯƠNG NƯỚC (lặp)
def part_thuong():
    """Thương nước v2: mũi khoan nước metaball thuôn (đầu nhọn về PHẢI), vệt xoắn quanh trục (toạ độ quay quanh x, lặp liền), đuôi
    cục nước liền thân xoắn nhẹ thon dần, giọt văng sau. Lặp 0,5 s. Neo gốc mũi (0, 0)."""
    P = T
    truc = F.empty("Truc")
    mat = W.flow_mat("Thuong", truc, scale=(0.22, 1.3, 1.3), spin=(P, 0, 1), **WATER)
    head = metaball("ThuongMB", 1.0, mat)
    head.location, head.scale = (0.4, 0, 0), (1.8, 0.5, 0.5)
    for j, (x, sx, sr, r) in enumerate(((1.55, 1.2, 0.3, 0.85), (2.35, 0.9, 0.16, 0.8), (2.85, 0.6, 0.08, 0.7))):   # mũi vuốt nhọn dần
        tip = metaball(f"ThuongMB.{j + 1:03d}", r)
        tip.location, tip.scale = (x, 0, 0), (sx, sr, sr)
    NB = 10
    for k in range(NB):
        ph = k / NB
        o = metaball(f"ThuongMB.{k + 10:03d}", 1.0)
        a0 = TAU * k / NB
        for i in range(N + 1):
            q = (i / N + ph) % 1.0
            a = a0 + TAU * 1.5 * q
            o.location = (-0.3 - 2.3 * q, 0.16 * q * math.cos(a), 0.16 * q * math.sin(a))
            sz = 0.4 * (1 - q) ** 0.9 + 0.04
            o.scale = (sz * 1.4, sz, sz)
            o.keyframe_insert("location", frame=F.fr(P * i / N))
            o.keyframe_insert("scale", frame=F.fr(P * i / N))
    for k in range(8):
        ob = W.drop(f"Giot{k}", (BOT, SANG, CHINH)[k % 3], 1)
        ph = k / 8
        a0 = math.radians(rnd.uniform(-60, 60))
        sp = rnd.uniform(1.2, 2.0)
        sz = rnd.uniform(0.04, 0.07)
        for i in range(N + 1):
            q = (i / N + ph) % 1.0
            ob.location = (-1.6 - sp * q, -0.4, 0.5 * math.sin(a0) * (0.4 + q) - 0.3 * q * q)
            s_ = sz * (1 - q) ** 0.7
            ob.scale = (s_ * 1.4, s_, s_)
            ob.keyframe_insert("location", frame=F.fr(P * i / N))
            ob.keyframe_insert("scale", frame=F.fr(P * i / N))
    return 420, 140, -0.8, 0.0, "thuong_nuoc2", True


# ===================================================================== MẠCH PHUN
def part_phun():
    """Mạch phun v2: vành toé + vũng ở chân → cột nước dựng từ đất (đầu cột lên đỉnh 0,1–0,3 s, phình rồi phập phồng, vệt nước chảy
    lên), đỉnh vương miện toé ngửa lên + giọt rơi quanh cột; 1,0–1,45 s cột SỤP từ trên xuống (ngưỡng đầu hạ về 0), giọt rơi. Neo chân
    cột trên đất."""
    H2 = 4.4
    pth = lambda s_: Vector((0.14 * math.sin(TAU * s_ * 1.2), 0, H2 * s_))
    rad = lambda s_: 0.55 * (1 - 0.25 * s_)
    band = ([(0, -0.3)], [(0, -0.05), (0.1, 0.05), (0.3, 1.2), (1.0, 1.2), (1.2, 0.6), (1.45, -0.1)])
    col = water_tube("Cot", pth, rad, band, (1.8, 3.0, 1.0), (0, -6.0, 0))
    for t, r in ((0, 0.4), (0.2, 1.15), (0.35, 1.0), (0.6, 1.07), (0.85, 0.97), (1.0, 1.0), (1.3, 0.8), (1.45, 0.6)):
        col.scale = (r, r, 1)
        col.keyframe_insert("scale", frame=F.fr(t))
    top = Vector((0, 0, H2))
    for k, tb in enumerate((0.3, 0.6)):
        crown(f"Dinh{k}", top + Vector((0, 0.1 * k, -0.2)), Vector((0, 0, 1)), tb, tb + 0.18, tb + 0.55, 0.9 if k == 0 else 0.75,
              mask=f"ngon_{k % 3}")
        burst(f"DinhToe{k}", top, Vector((0, 0, 1)), tb, n_blob=5, n_drop=14, n_trail=3, size=0.9, star=False)
    for k in range(26):
        t0 = rnd.uniform(0.3, 1.3)
        a = rnd.uniform(0, TAU)
        v = Vector((math.cos(a) * rnd.uniform(0.8, 2.0), math.sin(a) * 0.8, rnd.uniform(0.5, 2.5)))
        h = H2 if t0 < 1.0 else H2 * max(0.2, 1 - (t0 - 1.0) / 0.45)
        fly(W.drop(f"Roi{k}", (BOT, SANG, CHINH)[k % 3], 1), Vector((0, -0.5, h)), v, t0, rnd.uniform(0.5, 0.8), rnd.uniform(0.05, 0.1))
    ring = W.link(bpy.data.objects.new("VanhChan", W.ring_cone("VanhChan", 0.5, 1.7, 0.7, flare=1.5)))
    ring.data.materials.append(W.water_mat("VanhChanM", coord="UV", flow=dict(scale=(7.0, 1.3, 1.0), move=(T, (0, -1.6, 0)), **WATER),
                                           mask="loang_0", thr=[(0, 0.11), (0.9, 1.0)], tiling=(4.14, 0.91), noise_scale=5.0, edge=(0.035, "bot")))
    key_s(ring, [(0, 0.0), (0.0, 0.33), (0.25, 1.0), (0.9, 1.12)])
    for k, (s_, off, mk) in enumerate(((2.6, (0, 0), "vung_0"), (1.8, (0.5, 0.3), "vung_1"))):
        o = W.link(bpy.data.objects.new(f"VungChan{k}", W.quad(f"VungChan{k}", s_, s_ * 0.85, "XY")))
        o.data.materials.append(W.water_mat(f"VungChanM{k}", coord="UV", flow=dict(scale=(1.6, 1.6, 1.0), **FLAT), mask=mk,
                                            thr=[(0, 0.02), (0.6, 0.1), (T, 1.0)], extension="CLIP", noise_scale=3.5, edge=(0.05, "bot")))
        o.location = (off[0], off[1], -0.01 - 0.002 * k)
        key_s(o, [(0, 0.0), (0.02, 0.2), (0.2, 1.0), (T, 1.05)])
    return 380, 440, 0.0, 2.2, "mach_phun2", False


# ===================================================================== TOÉ TRÚNG THÂN / CẦU VỠ
def part_than(with_ball=False):
    """Toé nước v2 khi lao, húc, đạn trúng THÂN đích (đòn từ trái): chớp sao, 2 vương miện ngửa ngược về người đánh (ngón mảnh rồi
    đứt), chấm toé, vệt, giọt. with_ball: thêm cầu nước metaball tới nơi bẹp lại rồi vỡ lấm tấm (speck). Neo điểm trúng."""
    back = Vector((-1, 0, 0.75)).normalized()
    crown("VM0", Vector((-0.15, 0, -0.2)), back, 0.0, 0.2, 0.75, 1.0, mask="ngon_0")
    crown("VM1", Vector((-0.1, 0.15, -0.25)), Vector((-0.8, 0.3, 0.9)).normalized(), 0.03, 0.25, 0.7, 0.65, mask="ngon_1", til=1.5)
    burst("Toe", Vector((0, 0, 0)), back, 0.0, n_blob=8, n_drop=22, n_trail=8, size=1.0, star=True)
    if with_ball:
        truc = F.empty("Truc")
        mat = W.water_mat("CauVoM", coord="OBJ", coord_obj=truc, flow=dict(scale=(0.55, 0.55, 2.6), **WATER),
                          speck=([(0, 0.0), (0.04, 0.05), (0.2, 1.0)], 30.0))
        ball = metaball("VoMB", 1.4, mat)
        mat.use_backface_culling = True
        ball.location = (-0.4, 0.3, 0.0)
        for t, sx, sz in ((0, 0.95, 0.95), (0.05, 0.62, 1.12), (0.12, 0.45, 1.3), (0.2, 0.4, 1.35)):
            ball.scale = (sx, 1.0, sz)
            ball.keyframe_insert("scale", frame=F.fr(t))
    return 520, 420, -0.8, 0.4, ("cau_vo2" if with_ball else "toe_nuoc2"), False



WPX, HPX, CX, CY, PREFIX, LOOP = {"cau": part_cau, "toe": part_toe, "ong": part_ong, "roi": lambda: part_ong(True), "tia": part_tia,
                                  "thuong": part_thuong, "phun": part_phun, "than": part_than, "vo": lambda: part_than(True)}[PHAN]()

# ---- máy trực giao chếch xuống PITCH; neo (gốc toạ độ) tính bằng chiếu thật
right, up = Vector((1, 0, 0)), Vector((0, math.sin(PITCH), math.cos(PITCH)))
view = Vector((0, math.cos(PITCH), -math.sin(PITCH)))
cam_p = right * CX + up * CY - view * 40
W.eevee(tuple(cam_p), WPX, HPX, W.UPP)
sc.camera.rotation_euler = (math.radians(90) - PITCH, 0, 0)
sc.camera.data.clip_end = 200
F.run(OUT, PREFIX, tuple(cam_p), W.UPP * WPX, WPX, HPX, frames=FRAMES, save=SAVE, save_frame=8, loop=LOOP)
pp = world_to_camera_view(sc, sc.camera, Vector((0, 0, 0)))
info_p = os.path.join(OUT, "info.json")
info = json.load(open(info_p))
info["anchor"] = [round(pp.x * WPX), round((1 - pp.y) * HPX)]
json.dump(info, open(info_p, "w"))
print("khung", WPX, HPX, "neo that", info["anchor"])
