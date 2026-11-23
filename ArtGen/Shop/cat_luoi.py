# Cắt tờ gen nền trong theo lưới hàng × cột thành từng ảnh (gọt sát phần có nét + lề) vào Assets/03 Art/Shop/<tiền tố>_<số>.png.
# Chạy: py -3 -I ArtGen/Shop/cat_luoi.py <tờ nguồn> <hàng> <cột> <tiền tố>
#   ví dụ: py -3 -I ArtGen/Shop/cat_luoi.py ArtGen/Shop/bi/goi_bi_a.png 2 3 goi_bi  → goi_bi_1..6 (trái → phải, trên → dưới)
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Shop")
PAD = 6


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    src, rows, cols, prefix = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    a = im.getchannel("A").point(lambda v: 255 if v >= 100 else 0)
    os.makedirs(OUT, exist_ok=True)
    k = 0
    for r in range(rows):
        for c in range(cols):
            k += 1
            box = (c * w // cols, r * h // rows, (c + 1) * w // cols, (r + 1) * h // rows)
            bb = a.crop(box).getbbox()
            if not bb:
                print(f"ô {k}: trống")
                continue
            x0, y0 = box[0] + bb[0], box[1] + bb[1]
            x1, y1 = box[0] + bb[2], box[1] + bb[3]
            cut = im.crop((max(0, x0 - PAD), max(0, y0 - PAD), min(w, x1 + PAD), min(h, y1 + PAD)))
            path = os.path.join(OUT, f"{prefix}_{k}.png")
            cut.save(path)
            print(f"ô {k}: {cut.size[0]}x{cut.size[1]} → {path}")


if __name__ == "__main__":
    main()
