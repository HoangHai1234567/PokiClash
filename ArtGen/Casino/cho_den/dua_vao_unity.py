# -*- coding: utf-8 -*-
"""Nền thật màn Chợ đen (GD_Claude/29 mục C8, 2026-11-27; thay nền màu gỗ tạm). Gen Magnific GPT 2.6 2k high (175 credit), file prompt
luot_1_nen.txt, ảnh mẫu: world_style.png (nét), casino_ct_cho.png (hình chợ trên đảo), hd_nen.jpg (cách bố cục nền dọc của đảo).
Không người, không chữ (người dùng 2026-11-27 giữ chốt "Lão Mực là gương mặt duy nhất của đảo", không vẽ lái buôn). Giữa là vách ván
trống để kệ 8 ô của màn đè lên.
Thu về 1152 x 2048 (9:16, cùng cỡ các nền phủ màn của đảo), JPEG 90 → Assets/03 Art/Casino/Cho/cho_nen.jpg; ArtImporter nhập ở 2048.
Xong chạy menu "PokiClash/Prefab/Đảo Casino/Chợ đen: dựng scene" (Editor/CasinoMarketMenu.cs đặt ảnh phủ kín Canvas/Nen).
    py -3 -I ArtGen/Casino/cho_den/dua_vao_unity.py
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "tai_ve", "nen_cho.png")
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Casino", "Cho"))
os.makedirs(OUT_DIR, exist_ok=True)
im = Image.open(SRC).convert("RGB")
W, H = 1152, 2048
# cắt giữa cho đúng 9:16 rồi thu nhỏ
r = im.width / im.height
if r > W / H:
    w = round(im.height * W / H)
    im = im.crop(((im.width - w) // 2, 0, (im.width - w) // 2 + w, im.height))
elif r < W / H:
    h = round(im.width * H / W)
    im = im.crop((0, (im.height - h) // 2, im.width, (im.height - h) // 2 + h))
im = im.resize((W, H), Image.LANCZOS)
dst = os.path.join(OUT_DIR, "cho_nen.jpg")
im.save(dst, quality=90, optimize=True)
print("ghi", dst, im.size, os.path.getsize(dst) // 1024, "KB")
