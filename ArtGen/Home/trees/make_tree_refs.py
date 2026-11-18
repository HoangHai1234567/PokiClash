# Khung cho tờ cây rời của Nhà (rải ngẫu nhiên trong ô rừng chưa mở, thay khối rừng lặp lại; người dùng dặn 2026-11-18).
# frame_5.png (1792 x 1008, ra 16:9 1344 x 752): 5 chỗ, mỗi chỗ một chân thoi cỏ nhỏ (rộng 200 px ở bản phác = 2 ô lưới ở ảnh ra
# khoảng 150 px), gốc cây đứng giữa chân thoi; cây mọc cao tới khung xám. Chạy: py -3 -I make_tree_refs.py
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)
INK, GREY = (60, 40, 30), (205, 205, 205)


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


im = Image.new("RGB", (1792, 1008), (255, 255, 255))
d = ImageDraw.Draw(im)
DW, BOT, TOP = 200, 960, 60
for k in range(5):
    cx = 179 + k * 358
    q = [(cx, BOT - DW / 2), (cx + DW / 2, BOT - DW / 4), (cx, BOT), (cx - DW / 2, BOT - DW / 4)]
    d.polygon(q, fill=(178, 214, 128), outline=INK)
    d.line([(cx - 160, BOT - DW / 4), (cx - 160, TOP), (cx + 160, TOP), (cx + 160, BOT - DW / 4)], fill=GREY, width=2)
    d.text((cx, BOT - DW / 4), str(k + 1), fill=INK, font=font(36), anchor="mm")
im.save(os.path.join(OUT, "frame_5.png"))
print("ok")
