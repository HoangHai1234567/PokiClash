# Khung cho ảnh công trình Nhà (GD_Claude/21_Nha_Home.md): mọi tờ giữ cùng cỡ ô ở ảnh gen ra (khoảng 90 px mỗi ô theo bề ngang),
# chân thoi 2:1, góc dưới chĩa xuống. Ảnh gen ra cùng khung, nền trắng phẳng để tách nền.
# - frame_3x4.png (1792 x 1008, ra 16:9 1344 x 752): 3 chỗ công trình 4 x 4 (chân thoi 480 px ở bản phác = 360 px ở ảnh ra)
# - frame_6.png (1024 x 1024, ra 1:1): 1 công trình 6 x 6 (chân thoi 540 px)
# - frame_4x2.png (1792 x 1008): 4 chỗ món 2 x 2 (chân thoi 240 px ở bản phác = 180 px ở ảnh ra)
# Chạy: py -3 -I make_building_refs.py
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)
INK = (60, 40, 30)
GREY = (205, 205, 205)


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def slot(d, cx, bottom, dw, top, label):
    q = [(cx, bottom - dw / 2), (cx + dw / 2, bottom - dw / 4), (cx, bottom), (cx - dw / 2, bottom - dw / 4)]
    d.polygon(q, fill=(178, 214, 128), outline=INK)
    x0, x1 = cx - dw / 2, cx + dw / 2
    d.line([(x0, q[3][1]), (x0, top), (x1, top), (x1, q[1][1])], fill=GREY, width=2)
    d.text((cx, bottom - dw / 4), label, fill=INK, font=font(40), anchor="mm")
    return q


def sheet(name, size, slots):
    im = Image.new("RGB", size, (255, 255, 255))
    d = ImageDraw.Draw(im)
    meta = []
    for (cx, bottom, dw, top, label) in slots:
        meta.append(slot(d, cx, bottom, dw, top, label))
    im.save(os.path.join(OUT, name))
    return meta


if __name__ == "__main__":
    sheet("frame_3x4.png", (1792, 1008), [(300, 950, 480, 90, "1"), (896, 950, 480, 90, "2"), (1492, 950, 480, 90, "3")])
    sheet("frame_6.png", (1024, 1024), [(512, 990, 540, 60, "1")])
    sheet("frame_4x2.png", (1792, 1008), [(224, 950, 240, 420, "1"), (672, 950, 240, 420, "2"), (1120, 950, 240, 420, "3"), (1568, 950, 240, 420, "4")])
    print("ok", OUT)
