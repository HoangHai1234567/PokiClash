# Khung mẫu cho bộ mảnh môi trường Nhà (GD_Claude/22_Critters_Home.md mốc A5, học vách cao nguyên và bãi biển home Clash of Critters).
# Toạ độ theo px bản đồ Nhà (ô 96 x 48, một bước dọc cạnh "\" = (48, 24) px); ảnh ra GPT 2.6 3:2 1k = 1536 x 1024 = cỡ thật trên bản đồ.
#   refs/frame_vach.png : 4 chỗ 768 x 512: 1, 2 = đoạn vách thẳng 8 ô dọc cạnh "\" (mép cỏ trên, mặt vách cao H xuống); 3 = đầu vách bên
#                         phải (vách kết thúc, đổ xuống thành đá, bụi); 4 = đầu vách bên trái. Cạnh "/" dùng bản lật ngang.
#   refs/frame_bien.png : 6 chỗ 512 x 512, mỗi chỗ một chân thoi cát (2 ô, chỗ 4 là 3 ô) cho đồ ven biển.
#   refs/hill_style.png : khối đồi có vách vẽ sẵn trên ảnh nền home_base.png (mẫu nét vách).
# Chạy: py -3 -I ArtGen/Home/kit/make_kit_refs.py
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)
INK, GREY, GRASS, FACE, SAND = (60, 40, 30), (190, 190, 190), (150, 205, 110), (226, 196, 160), (240, 222, 170)
STEP = (48, 24)   # một ô dọc cạnh "\"
H = 200           # cao mặt vách (px bản đồ, khoảng 2 ô; bằng mặt vách khối đồi vẽ sẵn trên nền)
LIP = 22          # dải cỏ mép trên


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def wall(d, x0, y0, cells, open_left=True, open_right=True):
    """Mặt vách: mép trên từ (x0, y0) đi theo cạnh "\" cells ô; mặt cao H xuống. Trả khung (x0, y0, x1, y1) của mảnh."""
    x1, y1 = x0 + STEP[0] * cells, y0 + STEP[1] * cells
    face = [(x0, y0), (x1, y1), (x1, y1 + H), (x0, y0 + H)]
    d.polygon(face, fill=FACE, outline=INK)
    lip = [(x0, y0 - LIP / 2), (x1, y1 - LIP / 2), (x1, y1 + LIP / 2), (x0, y0 + LIP / 2)]
    d.polygon(lip, fill=GRASS, outline=INK)
    # đầu hở (nối đoạn kế tiếp): nét đứt kéo dài
    for open_, (xa, ya), sgn in ((open_left, (x0, y0), -1), (open_right, (x1, y1), 1)):
        if not open_:
            continue
        for k in range(4):
            a = (xa + sgn * (8 + k * 16) * 2, ya + sgn * (8 + k * 16))
            b = (xa + sgn * (16 + k * 16) * 2, ya + sgn * (16 + k * 16))
            d.line([a, b], fill=GREY, width=3)
            d.line([(a[0], a[1] + H), (b[0], b[1] + H)], fill=GREY, width=3)
    return x0, y0, x1, y1


def frame_vach():
    im = Image.new("RGB", (1536, 1024), (255, 255, 255))
    d = ImageDraw.Draw(im)
    f = font(34)
    # 1, 2: đoạn thẳng 8 ô
    for k, (cx, cy) in enumerate([(0, 0), (768, 0)]):
        wall(d, cx + 192, cy + 40, 8)
        d.text((cx + 40, cy + 40), str(k + 1), fill=INK, font=f)
    # 3: đầu phải: 4 ô vách, rồi một đoạn 2 ô đổ dốc xuống mặt cỏ (vùng chấm)
    cx, cy = 0, 512
    x0, y0, x1, y1 = wall(d, cx + 150, cy + 30, 4, open_left=True, open_right=False)
    end = [(x1, y1 - LIP / 2), (x1 + 150, y1 + H - 20), (x1 + 60, y1 + H + 30), (x1, y1 + H)]
    d.polygon(end, fill=(236, 230, 214), outline=INK)
    d.text((cx + 40, cy + 40), "3", fill=INK, font=f)
    # 4: đầu trái: một đoạn đổ dốc, rồi 4 ô vách
    cx, cy = 768, 512
    x0, y0, x1, y1 = wall(d, cx + 330, cy + 30, 4, open_left=False, open_right=True)
    end = [(x0, y0 - LIP / 2), (x0, y0 + H), (x0 - 70, y0 + H + 20), (x0 - 170, y0 + 60)]
    d.polygon(end, fill=(236, 230, 214), outline=INK)
    d.text((cx + 40, cy + 40), "4", fill=INK, font=f)
    d.line([(768, 0), (768, 1024)], fill=GREY, width=2)
    d.line([(0, 512), (1536, 512)], fill=GREY, width=2)
    im.save(os.path.join(OUT, "frame_vach.png"))


def frame_bien():
    im = Image.new("RGB", (1536, 1024), (255, 255, 255))
    d = ImageDraw.Draw(im)
    f = font(34)
    for k in range(6):
        cx, cy = (k % 3) * 512, (k // 3) * 512
        cells = 3 if k == 3 else 2
        DW = 96 * cells
        mx, by = cx + 256, cy + 470
        q = [(mx, by - DW / 2), (mx + DW / 2, by - DW / 4), (mx, by), (mx - DW / 2, by - DW / 4)]
        d.polygon(q, fill=SAND, outline=INK)
        d.line([(mx - 220, by - DW / 4), (mx - 220, cy + 40), (mx + 220, cy + 40), (mx + 220, by - DW / 4)], fill=GREY, width=2)
        d.text((cx + 30, cy + 30), str(k + 1), fill=INK, font=f)
    im.save(os.path.join(OUT, "frame_bien.png"))


def hill_style():
    base = Image.open(os.path.join(ROOT, "Assets", "03 Art", "Home", "home_base.png")).convert("RGB")
    crop = base.crop((740, 30, 1510, 345))  # cụm ba khối đồi có thác ở mũi trên
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
    crop.save(os.path.join(OUT, "hill_style.png"))


if __name__ == "__main__":
    frame_vach()
    frame_bien()
    hill_style()
    json.dump({"step": STEP, "H": H, "lip": LIP, "seg_cells": 8, "cap_cells": 4}, open(os.path.join(OUT, "kit_geom.json"), "w"))
    print("ok")
