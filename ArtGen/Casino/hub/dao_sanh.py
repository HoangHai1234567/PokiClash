# -*- coding: utf-8 -*-
"""Đảo Casino trên bản đồ sảnh (GD_Claude/29 mục C8, 2026-11-27; người dùng chọn "thu nhỏ hình đảo có sẵn", không gen mới).
Ghép nền đảo trống Assets/03 Art/Casino/casino_dao.png với các công trình cố định casino_ct_<mã>.png đúng khung casino_art.json
(không lấy lều sự kiện leu_*: lều chỉ dựng theo lịch), bỏ dải đồi xa và nét sóng rời ở mép trên (chỉ giữ mảng đảo liền lớn nhất,
gồm cả viền bọt), cắt sát, thu về rộng 760 px → Assets/03 Art/Islands/sanh_dao_casino.png. Menu "PokiClash/Prefab/Sảnh: đảo Casino"
(Editor/HubCasinoMenu.cs) đặt ảnh ở góc dưới trái bản đồ.
    py -3 -I ArtGen/Casino/hub/dao_sanh.py
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Casino")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Islands", "sanh_dao_casino.png")
if "--xem" in sys.argv:  # chỉ ghi bản xem vào thư mục này, không ghi Assets
    OUT = os.path.join(HERE, "xem_dao_sanh.png")
WIDTH = 760
TOP_CUT = 96  # px ảnh đảo trống (cao 1360): dải đồi xa + sóng ở mép trên


def largest(mask):
    """Mảng liền lớn nhất (4 hướng), quét theo hàng để khỏi đệ quy sâu."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    best, best_n, n = 0, 0, 0
    for y0, x0 in zip(*np.nonzero(mask)):
        if lab[y0, x0]:
            continue
        n += 1
        stack = [(y0, x0)]
        lab[y0, x0] = n
        cnt = 0
        while stack:
            y, x = stack.pop()
            cnt += 1
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n
                    stack.append((yy, xx))
        if cnt > best_n:
            best, best_n = n, cnt
    return lab == best


def main():
    base = Image.open(os.path.join(ART, "casino_dao.png")).convert("RGBA")
    art = json.load(open(os.path.join(ART, "casino_art.json"), encoding="utf-8-sig"))
    rects = art["items"]  # mã → {x0, y0, x1, y1} px ảnh đảo trống
    # mảng đảo liền lớn nhất trên ảnh thu nhỏ (cho nhanh), phóng lại làm mặt nạ
    k = 4
    small = np.asarray(base.resize((base.width // k, base.height // k)))[..., 3] > 40
    small[: TOP_CUT // k, :] = False  # dải đồi xa ở mép trên dính liền với nét sóng: cắt hẳn trước khi tìm mảng đảo
    keep = largest(small)
    keep_full = np.asarray(Image.fromarray((keep * 255).astype(np.uint8)).resize(base.size, Image.NEAREST)) > 0
    a = np.asarray(base).copy()
    a[..., 3] = np.where(keep_full, a[..., 3], 0)
    img = Image.fromarray(a, "RGBA")
    # công trình cố định, xếp theo đáy (gần người xem vẽ sau) như màn đảo
    items = []
    for code, r in rects.items():
        if code.startswith("leu_"):
            continue
        p = os.path.join(ART, f"casino_ct_{code}.png")
        if not os.path.exists(p):
            continue
        if isinstance(r, dict):
            x0, y0, x1, y1 = r["x0"], r["y0"], r["x1"], r["y1"]
        else:
            x0, y0, x1, y1 = r
        items.append((y1, code, p, (x0, y0, x1, y1)))
    for _, code, p, (x0, y0, x1, y1) in sorted(items):
        ct = Image.open(p).convert("RGBA").resize((int(round(x1 - x0)), int(round(y1 - y0))), Image.LANCZOS)
        img.alpha_composite(ct, (int(round(x0)), int(round(y0))))
    box = img.getbbox()
    img = img.crop(box)
    h = round(img.height * WIDTH / img.width)
    img = img.resize((WIDTH, h), Image.LANCZOS)
    img.save(OUT, optimize=True)
    print("ghi", OUT, img.size, "khung cắt", box, "công trình", len(items))


if __name__ == "__main__":
    main()
