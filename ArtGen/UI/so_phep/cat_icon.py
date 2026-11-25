# -*- coding: utf-8 -*-
"""Cắt 20 icon ô Sổ Phép từ tấm lưới 5 x 4 (người dùng 2026-11-24: "cần gen thì gọi gpt gen, tối ưu ảnh dung lượng").
Tấm gen bằng GPT (Magnific, model gpt-2-6, nền trong suốt, 95 credit) theo kiểu bộ icon sẵn có (ảnh mẫu ghép 8 icon Fallback/Icons):
tai_ve/luoi_icon.png. Mỗi ô: lọc chấm vụn (mảng điểm phủ nhỏ hơn 0,4% ô), cắt sát hình kèm lề, thu vừa 128 x 128 (ô hiện icon 104 px) (giữ tỉ lệ, đặt giữa),
lưu PNG tối ưu vào Assets/03 Art/SoPhep/<id>.png theo thứ tự ô trong balance.json khối "sophep".
    py -3 -I ArtGen/UI/so_phep/cat_icon.py
"""
import json, os
from collections import deque
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(HERE, "tai_ve", "luoi_icon.png")
OUT = os.path.join(ROOT, "Assets", "03 Art", "SoPhep")
SIDE, PAD, COLS, ROWS = 128, 6, 5, 4

ids = [n["id"] for n in json.load(open(os.path.join(ROOT, "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8"))["sophep"]["nodes"]]
assert len(ids) == COLS * ROWS
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert("RGBA")
W, H = im.size
cw, ch = W / COLS, H / ROWS


def clean(cell):
    # bỏ các mảng điểm phủ nhỏ (chấm vụn quanh icon), giữ mảng lớn
    w, h = cell.size
    a = cell.split()[3].load()
    seen = [[False] * h for _ in range(w)]
    keep = Image.new("L", (w, h), 0)
    kp = keep.load()
    minArea = 0.004 * w * h
    for x0 in range(w):
        for y0 in range(h):
            if seen[x0][y0] or a[x0, y0] < 40:
                continue
            comp, q = [], deque([(x0, y0)])
            seen[x0][y0] = True
            while q:
                x, y = q.popleft()
                comp.append((x, y))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and not seen[nx][ny] and a[nx, ny] >= 40:
                            seen[nx][ny] = True
                            q.append((nx, ny))
            if len(comp) >= minArea:
                for x, y in comp:
                    kp[x, y] = 255
    # nở mặt nạ 2 điểm để giữ mép mờ của nét
    from PIL import ImageFilter
    keep = keep.filter(ImageFilter.MaxFilter(5))
    r, g, b, al = cell.split()
    al = Image.composite(al, Image.new("L", (w, h), 0), keep)
    return Image.merge("RGBA", (r, g, b, al))


import sys
sys.stdout.reconfigure(encoding="utf-8")
total = 0
for i, nid in enumerate(ids):
    cx, cy = i % COLS, i // COLS
    cell = im.crop((round(cx * cw), round(cy * ch), round((cx + 1) * cw), round((cy + 1) * ch)))
    cell = clean(cell)
    box = cell.split()[3].point(lambda v: 255 if v > 24 else 0).getbbox()
    if box:
        cell = cell.crop(box)
    w, h = cell.size
    k = (SIDE - 2 * PAD) / max(w, h)
    cell = cell.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIDE, SIDE), (0, 0, 0, 0))
    canvas.alpha_composite(cell, ((SIDE - cell.width) // 2, (SIDE - cell.height) // 2))
    p = os.path.join(OUT, nid + ".png")
    canvas.save(p, optimize=True)
    total += os.path.getsize(p)
print("ghi", len(ids), "icon", SIDE, "px, tổng", total // 1024, "KB ->", OUT)
