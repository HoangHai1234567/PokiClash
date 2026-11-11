# -*- coding: utf-8 -*-
"""tm06: kẻ lưới toạ độ lên ảnh (concept hoặc mảnh) để đọc toạ độ khớp, khung bao bộ phận.

    py -3 -I ArtGen/Spine/tm06_luoi.py <ảnh> <ra.png> [bước=50] [x0,y0,x1,y1] [phóng=1]
"""
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")


def ke(src, out, buoc=50, hop=None, phong=1.0):
    im = Image.open(src).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    im = bg.convert("RGB")
    x0, y0 = 0, 0
    if hop:
        x0, y0, x1, y1 = hop
        im = im.crop(hop)
    if phong != 1:
        im = im.resize((int(im.width * phong), int(im.height * phong)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    gx = (x0 // buoc + 1) * buoc if x0 % buoc else x0
    while (gx - x0) * phong < im.width:
        X = (gx - x0) * phong
        strong = gx % (buoc * 2) == 0
        d.line([(X, 0), (X, im.height)], fill=(255, 0, 0) if strong else (255, 170, 170), width=1)
        if strong:
            d.text((X + 2, 2), str(gx), fill=(200, 0, 0), font=f)
        gx += buoc
    gy = (y0 // buoc + 1) * buoc if y0 % buoc else y0
    while (gy - y0) * phong < im.height:
        Y = (gy - y0) * phong
        strong = gy % (buoc * 2) == 0
        d.line([(0, Y), (im.width, Y)], fill=(0, 0, 255) if strong else (170, 170, 255), width=1)
        if strong:
            d.text((2, Y + 2), str(gy), fill=(0, 0, 200), font=f)
        gy += buoc
    im.save(out)
    print(out, im.size)


if __name__ == "__main__":
    a = sys.argv[1:]
    hop = tuple(int(v) for v in a[3].split(",")) if len(a) > 3 and a[3] != "-" else None
    ke(a[0], a[1], int(a[2]) if len(a) > 2 else 50, hop, float(a[4]) if len(a) > 4 else 1.0)
