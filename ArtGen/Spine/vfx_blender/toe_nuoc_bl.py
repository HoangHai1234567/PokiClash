# -*- coding: utf-8 -*-
"""Cụm TOÉ NƯỚC nhiều lớp (học repo abitofgamedev/water_vfx — Splash.prefab, skill vfx-petclash/hoc_water_vfx_abitofgamedev.md mục 2),
bộ nước Blender (nuocbl.py, màu phẳng lam, không phát sáng). Người dùng 2026-11-24: "làm cả đi" (A thư viện tan theo ngưỡng, B cụm toé,
C tia hai ngưỡng + vũng, D cầu vỡ lấm tấm). Đòn tới từ TRÁI sang PHẢI (lật ngang cho bên kia).
  --phan toe  (1 s, 24 khung, neo = ĐIỂM TRÚNG trên thân đích): chớp sao kem → vương miện vành nón ngửa về người đánh (skill 1b:
              "nước toé mão ngược về người bắn"), nở đủ cỡ ~0,22 s; mặt nạ NGÓN (ngon_*) tan theo ngưỡng: ngón mảnh dần, đầu ngón
              đứt thành giọt, mép tan viền bọt trắng, lòng trong tối hơn; vương miện nhỏ thứ hai lệch góc; 8 chấm toé (sprite cụm
              chấm, tan 0,14 → 1 trong 0,5 s); 10 vệt nước bay ngược + trọng lực; 22 giọt.
              (Bản thử đầu dùng mặt nạ mây loang cho vương miện → vỡ vụn thành mảnh, không ra dáng vương miện.)
  --phan vung (1,2 s, 29 khung, neo = TÂM VŨNG trên đất, đặt dưới chân đích): 2 vũng loang (decal nằm đất, nở đủ ở 0,16 s, tan chậm
              theo ngưỡng) + 3 vệt loang trượt về phía trước (hướng đòn) rồi tan.
  --phan cau  (1 s, 24 khung, neo = điểm trúng): như toe + THÂN CẦU NƯỚC tới nơi bẹp lại rồi vỡ thành lấm tấm (ngưỡng trên nhiễu mịn
              scale 40, như cầu nước của repo) — dùng khi cầu nước / đạn nước trúng.
Máy chếch xuống 20° (thấy vũng trên đất); sprite phẳng quay mặt về máy.
    blender.exe -b --factory-startup --python toe_nuoc_bl.py -- <thư_mục_ra> --phan toe|vung|cau [--frames ..] [--save x.blend]
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
_a = sys.argv[sys.argv.index("--") + 1:]
PHAN = _a[_a.index("--phan") + 1] if "--phan" in _a else "toe"
T = 1.2 if PHAN == "vung" else 1.0
N = int(round(T * F.FPS))
sc = F.reset(N)
TAU = W.TAU
rnd = W.rnd
PITCH = math.radians(20)


def face_cam(o, spin=0.0):
    o.rotation_mode = "YXZ"
    o.rotation_euler = (-PITCH, spin, 0)


def key_s(o, pairs, axes=(1, 1, 1)):
    for t, s in pairs:
        o.scale = tuple(max(1e-3, s * a) for a in axes)
        o.keyframe_insert("scale", frame=F.fr(t))


def ease_out(q):
    return 1 - (1 - q) ** 2.2


BOT, SANG, CHINH = W.flat("Bot", "bot"), W.flat("Sang", "sang"), W.flat("Chinh", "chinh")


def splash_part(with_ball=False):
    # ---- chớp sao kem 0–0,13 s (lớp sáng sau, lớp kem trước)
    for li, (mat, s2, y) in enumerate(((SANG, 1.25, 0.05), (BOT, 0.9, -0.05))):
        pts = [(a + rnd.uniform(-12, 12), (1.0 if k % 2 == 0 else 0.62) * s2) for k, a in enumerate(range(0, 360, 45))]
        o = W.obj(f"Chop{li}", W.star_mesh(f"Chop{li}", pts, 0.34), mat, (-0.1, y - 0.6, 0.0))
        face_cam(o, rnd.uniform(0, TAU))
        key_s(o, [(0, 0.0), (0.03, 0.9), (0.07, 1.0), (0.13, 0.0)])
    # ---- vương miện vành nón ngửa về phía người đánh (trục chếch −x, lên), ngón nước mọc từ chân, nở nhanh rồi tan theo ngưỡng:
    # ngón mảnh dần, đầu ngón đứt thành giọt (mặt nạ ngon_*, lặp 2 lần quanh vành); lòng trong (mặt sau) tối hơn một bậc
    for k, (ang, yaw, sc_, t0, t1, mk, til) in enumerate(((-42, 0, 1.0, 0.0, 0.22, "ngon_0", 2.0), (-58, 25, 0.62, 0.03, 0.26, "ngon_1", 1.5))):
        ring = W.link(bpy.data.objects.new(f"VuongMien{k}", W.ring_cone(f"VuongMien{k}", 0.3, 1.65, 1.5, flare=1.3)))
        ring.data.materials.append(W.mask_mat(f"VM{k}", mk, [(0, 0.02), (0.22, 0.08), (1.0, 0.95)], key="chinh", inner=(0.82, "giua"),
                                              rim=(0.05, "bot"), back="giua", tiling=(til, 1.0), noise_scale=4.0, nk=0.45))
        ring.rotation_mode = "ZYX"
        ring.rotation_euler = (0, math.radians(ang), math.radians(yaw))
        ring.location = (-0.2, 0.15 * k, -0.25)
        key_s(ring, [(0, 0.0), (t0, 0.3 * sc_), (t1, sc_), (1.0, 1.1 * sc_)])
    # ---- 8 chấm toé (sprite cụm chấm), phía sau / trên điểm trúng, nở rồi tan theo ngưỡng 0,14 → 1 trong 0,5 s
    for k in range(8):
        t0 = rnd.uniform(0.04, 0.18)
        life = rnd.uniform(0.42, 0.55)
        s = rnd.uniform(1.0, 1.7)
        p = Vector((-rnd.uniform(0.3, 1.8), -0.9 - 0.02 * k, rnd.uniform(-0.2, 1.5)))
        o = W.link(bpy.data.objects.new(f"Cham{k}", W.quad(f"Cham{k}", s, s)))
        key, rk = (("sang", "chinh") if k % 3 else ("bot", "sang"))
        o.data.materials.append(W.mask_mat(f"ChamM{k}", f"cham_{k % 3}", [(t0, 0.14), (t0 + life, 1.0)], key=key, rim=(0.06, rk),
                                           extension="CLIP", noise_scale=4.0))
        face_cam(o, rnd.uniform(0, TAU))
        drift = Vector((-rnd.uniform(0.2, 0.7), 0, rnd.uniform(-0.1, 0.4)))
        for i in range(7):
            q = i / 6
            t = t0 + life * q
            o.location = p + drift * ease_out(q)
            o.keyframe_insert("location", frame=F.fr(t))
        key_s(o, [(0, 0.0), (max(0.0, t0 - 0.01), 0.0), (t0, 0.6), (t0 + life * 0.4, 1.0), (t0 + life, 1.1)])
    # ---- 10 vệt nước (lá thon, đầu dày đi trước) bay ngược về người đánh + trọng lực
    for k in range(10):
        a = math.radians(rnd.uniform(100, 165))
        v = rnd.uniform(4.0, 6.2)
        o = W.obj(f"Vet{k}", W.blade_mesh(f"Vet{k}", -rnd.uniform(0.7, 1.1), rnd.uniform(0.1, 0.16), notch=0.3), SANG if k % 2 else CHINH,
                  (0, -0.5, 0))
        W.ballistic(o, (rnd.uniform(-0.3, 0.1), -0.5 - 0.01 * k, rnd.uniform(-0.2, 0.4)), (v * math.cos(a), v * math.sin(a)),
                    rnd.uniform(0.0, 0.08), rnd.uniform(0.42, 0.55), g=9.0, size=1.0, grow=(0.7, 0.5))
    # ---- 22 giọt
    for k in range(22):
        a = math.radians(rnd.uniform(55, 178))
        v = rnd.uniform(3.0, 6.8)
        o = W.drop(f"Giot{k}", (BOT, SANG, CHINH)[k % 3], 1)
        W.ballistic(o, (rnd.uniform(-0.4, 0.2), -0.6, rnd.uniform(-0.3, 0.5)), (v * math.cos(a), v * math.sin(a)), rnd.uniform(0.0, 0.12),
                    rnd.uniform(0.38, 0.6), g=9.0, size=rnd.uniform(0.04, 0.09), grow=(1.0, 0.0), align=False)
    if with_ball:
        # ---- thân cầu nước tới nơi: bẹp lại rồi vỡ thành lấm tấm (ngưỡng trên nhiễu mịn)
        ball = W.link(bpy.data.objects.new("CauVo", W.uv_sphere("CauVo")))
        ball.data.materials.append(W.mask_mat("CauVoM", "dac_2", [(0, 0.0), (0.04, 0.06), (0.2, 1.0)], key="chinh", inner=(0.5, "sang"),
                                              rim=(0.05, "bot"), tiling=(2.0, 1.0), noise_scale=40.0, nk=0.9))
        ball.data.materials[0].use_backface_culling = True   # khối kín trong mờ (BLENDED): bỏ mặt sau kẻo vẽ đè lẫn → sọc theo vòng lưới
        ball.location = (-0.35, 0.3, 0.0)
        for t, sx, sz in ((0, 0.95, 0.95), (0.05, 0.62, 1.12), (0.12, 0.45, 1.3), (0.2, 0.4, 1.35)):
            ball.scale = (sx, 1.0, sz)
            ball.keyframe_insert("scale", frame=F.fr(t))


def puddle_part():
    # ---- 2 vũng loang nằm trên đất (decal), nở đủ ở 0,16 s, giữ rồi tan theo ngưỡng
    for k, (s, off, t0, mk) in enumerate(((2.8, (0, 0), 0.0, "vung_0"), (1.9, (0.7, 0.35), 0.05, "vung_1"))):
        o = W.link(bpy.data.objects.new(f"Vung{k}", W.quad(f"Vung{k}", s, s * 0.8, "XY")))
        o.data.materials.append(W.mask_mat(f"VungM{k}", mk, [(t0, 0.03), (0.45, 0.12), (1.2, 1.0)], key="sang", inner=(0.7, "bot"),
                                           rim=(0.05, "nhat"), extension="CLIP", noise_scale=3.5, alpha=0.88))
        o.location = (off[0], off[1], 0.002 * (k + 1))
        o.rotation_euler = (0, 0, rnd.uniform(-0.4, 0.4))
        key_s(o, [(0, 0.0), (t0, 0.2), (t0 + 0.16, 1.0), (1.2, 1.06)])
    # ---- 3 vệt loang trượt về phía trước (hướng đòn, +x) rồi tan
    for k in range(3):
        t0 = 0.04 + 0.05 * k
        life = rnd.uniform(0.75, 1.0)
        d = rnd.uniform(1.4, 2.6)
        s = rnd.uniform(0.9, 1.3)
        o = W.link(bpy.data.objects.new(f"Loang{k}", W.quad(f"Loang{k}", s * 1.4, s, "XY")))
        o.data.materials.append(W.mask_mat(f"LoangM{k}", f"vung_{(k + 2) % 3}", [(t0, 0.08), (t0 + life, 1.0)], key="sang",
                                           inner=(0.72, "bot"), rim=(0.06, "nhat"), extension="CLIP", noise_scale=4.0, alpha=0.88))
        y0 = rnd.uniform(-0.5, 0.5)
        o.rotation_euler = (0, 0, rnd.uniform(-0.3, 0.3))
        for i in range(7):
            q = i / 6
            o.location = (0.4 + d * ease_out(q), y0, 0.004 + 0.001 * k)
            o.keyframe_insert("location", frame=F.fr(t0 + life * q))
        key_s(o, [(0, 0.0), (t0, 0.3), (t0 + 0.15, 0.9), (t0 + life, 1.0)])


if PHAN == "vung":
    puddle_part()
    WPX, HPX, CX, CY, PREFIX = 420, 220, 0.9, 0.0, "vung_nuoc"
else:
    splash_part(PHAN == "cau")
    WPX, HPX, CX, CY, PREFIX = 560, 460, -1.0, 0.4, ("cau_vo" if PHAN == "cau" else "toe_nuoc")

# ---- máy trực giao chếch xuống PITCH; neo tính bằng chiếu thật
right, up = Vector((1, 0, 0)), Vector((0, math.sin(PITCH), math.cos(PITCH)))
view = Vector((0, math.cos(PITCH), -math.sin(PITCH)))
cam_p = right * CX + up * CY - view * 40
W.eevee(tuple(cam_p), WPX, HPX, W.UPP)
sc.camera.rotation_euler = (math.radians(90) - PITCH, 0, 0)
sc.camera.data.clip_end = 200
F.run(OUT, PREFIX, tuple(cam_p), W.UPP * WPX, WPX, HPX, frames=FRAMES, save=SAVE, save_frame=6)
pp = world_to_camera_view(sc, sc.camera, Vector((0, 0, 0)))
info_p = os.path.join(OUT, "info.json")
info = json.load(open(info_p))
info["anchor"] = [round(pp.x * WPX), round((1 - pp.y) * HPX)]
json.dump(info, open(info_p, "w"))
print("khung", WPX, HPX, "neo that", info["anchor"])
