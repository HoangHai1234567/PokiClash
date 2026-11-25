# -*- coding: utf-8 -*-
"""Đưa LỐC NƯỚC Blender đã duyệt (người dùng 2026-11-24: "lốc nước ok rồi"; frames/loc_nuoc, 48 khung một lượt, dựng bằng
vfx_blender/loc_tu_mau.py --gio --nuoc) vào game, thay khung lốc cũ — người dùng 2026-11-25: "update nốt các vfx thủy mới vào đi".
Lấy khung 0–23 (phễu đã thành hình, đang xoay; từ ~36 lốc sụp) làm vòng lặp 24 khung đúng số khung cũ, cắt quanh thân lốc về đúng tỉ lệ
FbDef cũ (HatFlip.cs: loc_nuoc 238:251, loc_nuoc_bao 240:249, neo giữa đáy 0,01) rồi GHI ĐÈ cùng tên → giữ GUID, không sửa HatFlip.cs.
Ảnh cũ chép lưu ở ArtGen/Spine/vfx_lua_toon/frames/_cu_hat_fb_loc_nuoc/ trước khi ghi đè.
    py -3 -I xuat_loc_nuoc.py
"""
import glob
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "frames", "loc_nuoc")
DST = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Fx", "Hat"))
BAK = os.path.join(HERE, "frames", "_cu_hat_fb_loc_nuoc")
os.makedirs(BAK, exist_ok=True)
for f in glob.glob(os.path.join(DST, "hat_fb_loc_nuoc_*.png")):
    b = os.path.join(BAK, os.path.basename(f))
    if not os.path.exists(b):
        shutil.copyfile(f, b)
Y0, Y1, CX = 6, 328, 240          # khung gộp của bộ Blender: y 6–327, chân lốc ở y 324 (neo 240, 324), tâm x 240
for name, (aw, ah) in (("loc_nuoc", (238, 251)), ("loc_nuoc_bao", (240, 249))):
    h = Y1 - Y0
    w = round(h * aw / ah)
    x0 = CX - w // 2
    for i in range(24):
        im = Image.open(os.path.join(SRC, f"loc_nuoc_{i:02d}.png")).convert("RGBA")
        out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        out.paste(im.crop((max(0, x0), Y0, min(im.width, x0 + w), Y1)), (max(0, -x0), 0))
        out.save(os.path.join(DST, f"hat_fb_{name}_{i:02d}.png"), optimize=True)
    print(name, w, "x", h)
print("ok, backup:", BAK)
