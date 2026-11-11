# -*- coding: utf-8 -*-
"""Kẻ lưới toạ độ lên concept dòng cá voi biến dị để đọc số cho CFG (pixel concept, y xuống).

    py -3 -I ArtGen/Spine/ca_voi_luoi.py <k> [x0 y0 x1 y1 [phóng]]   →  inbox/ca_voi_<k>/mau/luoi[_x0_y0].png
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))


def main(a):
    k = int(a[0])
    src = os.path.join(HERE, "inbox", f"ca_voi_{k}", "tai_ve", "L1_duyet.png")
    im = Image.open(src).convert("RGB")
    box = [int(v) for v in a[1:5]] if len(a) >= 5 else [0, 0, im.width, im.height]
    z = float(a[5]) if len(a) > 5 else 1.0
    c = im.crop(box)
    c = c.resize((round(c.width * z), round(c.height * z)), Image.LANCZOS)
    d = ImageDraw.Draw(c)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    buoc = 50 if z < 1.6 else (20 if z < 3.5 else 10)
    lon = 100 if buoc == 50 else (100 if buoc == 20 else 50)
    for x in range((box[0] // buoc) * buoc, box[2] + 1, buoc):
        X = (x - box[0]) * z
        d.line([(X, 0), (X, c.height)], fill=(255, 0, 0) if x % lon == 0 else (255, 170, 170), width=1)
        if x % lon == 0:
            d.text((X + 2, 2), str(x), fill=(200, 0, 0), font=f)
    for y in range((box[1] // buoc) * buoc, box[3] + 1, buoc):
        Y = (y - box[1]) * z
        d.line([(0, Y), (c.width, Y)], fill=(0, 0, 255) if y % lon == 0 else (170, 170, 255), width=1)
        if y % lon == 0:
            d.text((2, Y + 2), str(y), fill=(0, 0, 200), font=f)
    out = os.path.join(HERE, "inbox", f"ca_voi_{k}", "mau", "luoi.png" if len(a) < 5 else f"luoi_{box[0]}_{box[1]}.png")
    c.save(out)
    print(out, c.size)


if __name__ == "__main__":
    main(sys.argv[1:])
