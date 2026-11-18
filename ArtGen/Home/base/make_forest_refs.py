# Bản phác cho khối rừng 8 x 8 ô (ô rừng chưa mở của Nhà): khung 1024 x 1024, chân thoi 2:1 rộng 900 px, góc dưới ở (512, 990),
# cây mọc cao lên phía trên. Ảnh gen ra cùng khung này, nền trắng phẳng để tách nền bằng tô loang.
# Chạy: py -3 -I make_forest_refs.py
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)
W = H = 1024
DW = 900
BOT = (512, 990)
INK = (60, 40, 30)


def diamond():
    cx, by = BOT
    return [(cx, by - DW / 2), (cx + DW / 2, by - DW / 4), (cx, by), (cx - DW / 2, by - DW / 4)]


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


im = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(im)
q = diamond()
d.polygon(q, fill=(178, 214, 128), outline=INK)
# vùng cây được phép mọc: từ chân thoi lên tới y = 120
d.line([(q[3][0], q[3][1]), (q[3][0], 120)], fill=(200, 200, 200), width=2)
d.line([(q[1][0], q[1][1]), (q[1][0], 120)], fill=(200, 200, 200), width=2)
d.line([(q[3][0], 120), (q[1][0], 120)], fill=(200, 200, 200), width=2)
d.text((512, 90), "trees may rise up to here", fill=(150, 150, 150), font=font(24), anchor="mm")
d.text((512, 780), "diamond = ground footprint (2:1)", fill=INK, font=font(26), anchor="mm")
im.save(os.path.join(OUT, "forest_layout.png"))
print("ok", q)
