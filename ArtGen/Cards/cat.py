# -*- coding: utf-8 -*-
"""Cắt tranh thẻ chung từ tấm GPT (ArtGen/Cards/tai_ve/luot_NN.png, lưới bo_cuc_<k> của build.py) thành từng ảnh 448 x 280.

    py -3 -I ArtGen/Cards/cat.py 1            # cắt lượt 1 vào ArtGen/Cards/cat/<id>.png
    py -3 -I ArtGen/Cards/cat.py 1 --file luot_01_2.png

Mỗi ô: lấy vùng quanh chỗ ô trong bo_cuc (nới 40 px), tìm khung không trắng (ô có viền mực, khe trắng), cắt nới ra OUTSET px để GIỮ
viền mực rung GPT vẽ (game không vẽ viền thẳng), phần trắng ngoài viền (nối với mép ảnh) làm trong suốt, rồi thu về 448 x 280 RGBA
(16:10; trên thẻ hiện 272 x 170). Đưa vào game: ArtGen/Cards/vao_game.py.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cat")
W, H, PW, PH, PER = 1536, 1024, 464, 290, 9
SIZE = (448, 280)
OUTSET = 3
NOI = 40
TRANG = 232  # điểm có cả ba kênh trên mức này là trắng giấy ngoài viền


def nen_trong(tile):
    """Trắng ngoài viền mực (vùng trắng liền với mép ảnh) thành trong suốt; trắng bên trong viền giữ nguyên."""
    rgb = tile.convert("RGB")
    w, h = rgb.size
    mask = Image.new("L", (w, h), 0)
    src, mk = rgb.load(), mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            if r > TRANG and g > TRANG and b > TRANG:
                mk[x, y] = 255
    for x in range(w):
        for y in (0, h - 1):
            if mk[x, y] == 255:
                ImageDraw.floodfill(mask, (x, y), 128, thresh=0)
    for y in range(h):
        for x in (0, w - 1):
            if mk[x, y] == 255:
                ImageDraw.floodfill(mask, (x, y), 128, thresh=0)
    alpha = mask.point(lambda v: 0 if v == 128 else 255)
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out


def o_tranh(k):
    rows = math.ceil(k / 3)
    ch = H / 3
    top = (H - rows * ch) / 2
    boxes = []
    for i in range(k):
        r, c = divmod(i, 3)
        x0 = round(c * (W / 3) + (W / 3 - PW) / 2)
        y0 = round(top + r * ch + (ch - PH) / 2)
        boxes.append((x0, y0, x0 + PW, y0 + PH))
    return boxes


def khung(im, box, noi_doc=NOI):
    """Khung vật thể không trắng trong vùng box nới NOI px ngang, noi_doc px dọc (toạ độ ảnh)."""
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = max(0, x0 - NOI), max(0, y0 - noi_doc), min(im.width, x1 + NOI), min(im.height, y1 + noi_doc)
    vung = im.crop((x0, y0, x1, y1)).convert("L").point(lambda v: 255 if v < 235 else 0)
    # bỏ chấm lẻ: chỉ tính hàng / cột có đủ điểm tối
    w, h = vung.size
    px = vung.load()
    cols = [sum(1 for y in range(h) if px[x, y]) for x in range(w)]
    rows = [sum(1 for x in range(w) if px[x, y]) for y in range(h)]
    xs = [i for i, v in enumerate(cols) if v > h * 0.25]
    ys = [i for i, v in enumerate(rows) if v > w * 0.25]
    if not xs or not ys:
        return None
    return (x0 + xs[0], y0 + ys[0], x0 + xs[-1] + 1, y0 + ys[-1] + 1)


def main(argv):
    n = int(argv[0])
    name = argv[argv.index("--file") + 1] if "--file" in argv else f"luot_{n:02d}.png"
    src = os.path.join(HERE, "tai_ve", name)
    data = json.load(open(os.path.join(HERE, "canh_the_chung.json"), encoding="utf-8"))["cards"]
    cards = data[(n - 1) * PER: n * PER]
    im = Image.open(src).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    # tấm một hàng (lượt cuối 3 thẻ): GPT hay vẽ ô cao hơn khuôn, dò dọc rộng hơn (không có hàng khác để lẫn)
    noi_doc = 200 if len(cards) <= 3 else NOI
    for c, box in zip(cards, o_tranh(len(cards))):
        k = khung(im, box, noi_doc)
        if not k:
            print(f"  {c['id']}: KHÔNG thấy ô quanh {box}")
            continue
        x0, y0, x1, y1 = k
        tile = im.crop((max(0, x0 - OUTSET), max(0, y0 - OUTSET), min(W, x1 + OUTSET), min(H, y1 + OUTSET)))
        r = tile.width / tile.height
        if r < 1.45:
            # GPT vẽ ô cao hơn khuôn (lượt 9, 2026-11-27: 466 x 383): cắt bớt trên dưới tới 1,45 rồi mới thu về 16:10 (bóp dọc ~10%)
            h = round(tile.width / 1.45)
            top = (tile.height - h) // 2
            full = tile
            tile = full.crop((0, top, full.width, top + h))
            # dán lại dải viền mực trên / dưới của ô gốc (cắt giữa làm mất viền)
            b = 11
            tile.paste(full.crop((0, 0, full.width, b)), (0, 0))
            tile.paste(full.crop((0, full.height - b, full.width, full.height)), (0, h - b))
            print(f"  {c['id']}: ô cao {tile.width}x{h + 2 * top} ({r:.2f}), cắt giữa còn {tile.width}x{h}")
        elif abs(r - 1.6) > 0.08:
            print(f"  {c['id']}: ô lệch tỉ lệ {tile.width}x{tile.height} ({r:.2f}), vẫn thu về 16:10")
        nen_trong(tile).resize(SIZE, Image.LANCZOS).save(os.path.join(OUT, c["id"] + ".png"), optimize=True)
        print(f"  {c['id']}: ô {x1 - x0}x{y1 - y0} tại ({x0},{y0})")


if __name__ == "__main__":
    main(sys.argv[1:])
