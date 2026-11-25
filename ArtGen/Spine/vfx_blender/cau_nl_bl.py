# -*- coding: utf-8 -*-
"""Cầu NĂNG LƯỢNG kiểu "Energy Ball" (CodyWinch, file mẫu đã mua ở AtomSpine refs/blender_anime_fx), người dùng chọn 2026-11-24 cho cầu
năng lượng các tướng Mộc / Kim / Thổ (thay cầu hạt CauLa, RbCau, cầu đầu nòng tia, Mặt Trời Thổ Tinh).
Lấy THẲNG file mẫu (như loc_tu_mau.py): giữ chuỗi modifier gốc (Voronoi → trọng số → Displace ×2 → Smooth; lớp năng lượng = Edge − Texture,
Mask theo ngưỡng → gân sáng lộ qua khe giữa các múi thân), chỉ:
- đổi màu phẳng theo bộ (--bo moc|vang|troi), bỏ sàn / đèn, nền trong, View Standard, không bloom;
- LẶP: núm "Disp Control" (Empty gắn texture) xoay đúng một vòng quanh trục của nó trong N khung (mẫu gốc gần như đứng yên, chỉ tăng
  ngưỡng một lượt); ngưỡng "Energy Threshold" khoá quanh mức gân lộ rõ (khung ~55 của mẫu), thở 2 nhịp mỗi vòng;
- camera trực giao nhìn ngang (cùng hướng camera mẫu), khung vuông.
    blender.exe -b --disable-autoexec "<mẫu Energy Ball 2 8.blend>" --python cau_nl_bl.py -- <thư_mục_ra> --bo moc [--n 24]
        [--nguong 0.60] [--tho 0.035] [--frames 1,7] [--save x.blend]
Ra: <thư_mục_ra>/cau_nl_NN.png + info.json (neo = tâm cầu, px). Cắt bằng vfx_lua_toon/cat_nl.py.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Euler, Matrix, Vector

a = sys.argv[sys.argv.index("--") + 1:]
OUT = a[0]


def opt(name, default, cast=str):
    return cast(a[a.index(name) + 1]) if name in a else default


BO = opt("--bo", "moc")
N = opt("--n", 36, int)                  # 1,5 s một vòng: 24 khung (15°/khung) xoay hơi gắt
NGUONG = opt("--nguong", 0.53, float)    # ngưỡng Mask lớp năng lượng (mẫu: 0,717 → 0,78 → 0,568; thấp = lộ nhiều gân). Thử 2026-11-24:
                                         # 0,60 gân lấm tấm, 0,53 giống khung cuối mẫu, 0,45 trở xuống gân lấn thành nền (thân thành đốm)
THO = opt("--tho", 0.03, float)          # biên độ thở của ngưỡng
FRAMES = [int(x) for x in opt("--frames", "").split(",") if x] or None
SAVE = opt("--save", None)
W = H = opt("--px", 288, int)
ORTHO = opt("--ortho", 7.4, float)

# màu phẳng (thân, gân) theo bộ — tông tươi hợp sân sáng (skill vfx-petclash 1b), thân đủ đậm để gân sáng nổi lên
MAU = {
    "moc": ("#1E9E6E", "#E6F77E"),    # lục ngọc (MocTuoi gac_da / bom_la) + gân chanh kem: Gạc Đá, Lộc Phong, đầu nòng tia lá
    "vang": ("#F08A22", "#FFF1A8"),   # cam vàng (KmNang) + gân kem vàng: Thần Cơ, Pháo Giáp, đầu nòng tia vàng (Giác Mộc, Nhật Vương)
    "troi": ("#E8582A", "#FFD94A"),   # cam đỏ + gân vàng (TtLua): Mặt Trời của Thổ Tinh
}
THAN, GAN = MAU[BO]


def lin(h):
    h = h.lstrip("#")

    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return tuple(f(int(h[i:i + 2], 16)) for i in (0, 2, 4)) + (1.0,)


sc = bpy.context.scene
for m in bpy.data.materials:
    col = {"Black": THAN, "Energy": GAN}.get(m.name)
    if not col or not m.use_nodes:
        continue
    m.diffuse_color = lin(col)
    for nd in m.node_tree.nodes:
        if nd.type == "EMISSION":
            nd.inputs["Color"].default_value = lin(col)
            nd.inputs["Strength"].default_value = 1.0
    m.surface_render_method = "DITHERED"   # đặc (alpha 1), không cần trộn trong mờ
for ob in sc.objects:
    if ob.type in ("LIGHT",) or ob.name.lower().startswith("floor"):
        ob.hide_render = True

# --- lặp: xoá khoá gốc của núm; xoay CỨNG không gian texture quanh TÂM CẦU đúng VONG vòng trong N khung (núm mẫu nằm cách tâm ~6,8 đơn
# vị: xoay quanh chính nó thì vân quét qua cầu rất gắt, mỗi khung một hình khác hẳn), trục gần đứng hơi nghiêng → múi trôi ngang như hành
# tinh tự quay; thêm dịch vòng nhỏ (một vòng / N) để múi biến dạng dần thay vì chỉ trôi; ngưỡng khoá + thở 2 nhịp / vòng.
# Khoá MỌI khung nên nội suy không ảnh hưởng (chỉ render khung nguyên).
sc.frame_start, sc.frame_end = 1, N
sc.render.fps = 24
ctl = bpy.data.objects["Disp Control"]
thr = bpy.data.objects["Energy Threshold"]
for ob in (ctl, thr):
    ob.animation_data_clear()
sc.frame_set(1)
M0 = ctl.matrix_world.copy()
tam = bpy.data.objects["Main Body"].location.copy()
TRUC = Vector([float(x) for x in opt("--truc", "0.25,0.35,1").split(",")]).normalized()
LECH = opt("--lech", 0.35, float)       # bán kính dịch vòng (đơn vị cảnh)
VONG = opt("--vong", 1, int)            # số vòng xoay mỗi chu kỳ (nguyên để lặp liền)
for i in range(N + 1):
    f = 1 + i
    u = i / N
    R = Matrix.Translation(tam) @ Matrix.Rotation(2 * math.pi * VONG * u, 4, TRUC) @ Matrix.Translation(-tam)
    off = Vector((LECH * math.cos(2 * math.pi * u), LECH * math.sin(2 * math.pi * u), 0.0))
    ctl.matrix_world = Matrix.Translation(off) @ R @ M0
    ctl.keyframe_insert("location", frame=f)
    ctl.keyframe_insert("rotation_euler", frame=f)
    ctl.keyframe_insert("scale", frame=f)
    thr.location.z = NGUONG + THO * math.sin(2 * math.pi * 2 * u)
    thr.keyframe_insert("location", index=2, frame=f)

# --- camera trực giao nhìn ngang về tâm cầu (camera mẫu ở +X nhìn −X)
body = bpy.data.objects["Main Body"]
cz = body.location.z
cam = sc.camera
cam.data.type = "ORTHO"
cam.data.ortho_scale = ORTHO
cam.data.sensor_fit = "HORIZONTAL"
cam.location = (20.0, 0.0, cz)
cam.rotation_euler = Euler((math.pi / 2, 0, math.pi / 2), "XYZ")
cam.data.clip_end = 100

r = sc.render
r.engine = "BLENDER_EEVEE"
try:
    sc.eevee.taa_render_samples = 16
    sc.eevee.use_bloom = False
except Exception:
    pass
r.resolution_x, r.resolution_y, r.resolution_percentage = W, H, 100
r.film_transparent = True
sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"
r.image_settings.file_format, r.image_settings.color_mode = "PNG", "RGBA"

if SAVE:
    sc.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=SAVE)
os.makedirs(OUT, exist_ok=True)
for f in FRAMES or range(1, N + 1):
    sc.frame_set(f)
    r.filepath = os.path.join(OUT, f"cau_nl_{f - 1:02d}.png")
    bpy.ops.render.render(write_still=True)
json.dump(dict(count=N, w=W, h=H, fps=24, loop=True, anchor=[W // 2, H // 2], bo=BO, than=THAN, gan=GAN, nguong=NGUONG),
          open(os.path.join(OUT, "info.json"), "w"))
print("OK cau_nl", BO, N, "khung")
