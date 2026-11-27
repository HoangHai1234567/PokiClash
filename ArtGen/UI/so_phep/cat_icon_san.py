# -*- coding: utf-8 -*-
"""Đường Chinh Phục (trước là Sổ Phép, người dùng 2026-11-27: "không làm cái kiểu nét nét nữa, đổi sang một câu chuyện gần với việc chinh
phục các con quái vật hơn"): cắt icon chủ đề săn quái thay các icon bút, mực, sổ.
Tấm gen bằng GPT 2.6 qua Magnific (1k high, 95 credit, nền trong, ảnh mẫu là tấm icon cũ tai_ve/luoi_icon.png):
tai_ve/luoi_icon_san.png, lưới 4 x 3. 10 ô đầu thay icon ô cùng id, ô 11 là icon tiền "nanh" (nanh.png), ô 12 để dự phòng.
Huy hiệu sảnh tai_ve/nut_chinh_phuc.png (GPT 2.6, ảnh mẫu huy hiệu cũ nut_so_phep + nut_hang) -> Assets/03 Art/Hud/nut_so_phep.png,
256 x 256, hình tròn chạm mép như cat_nut.py (giữ tên file để prefab sảnh khỏi đổi).
    py -3 -I ArtGen/UI/so_phep/cat_icon_san.py
"""
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# POKI_XEM_THU=<thư mục>: ghi ra đó để xem trước, không đụng Assets (Unity dùng chung nhiều phiên)
OUT = os.environ.get("POKI_XEM_THU") or os.path.join(ROOT, "Assets", "03 Art", "SoPhep")
HUD = os.environ.get("POKI_XEM_THU") or os.path.join(ROOT, "Assets", "03 Art", "Hud")
SIDE, PAD, COLS, ROWS = 128, 6, 4, 3
CELLS = ["muc_cho", "tiep_suc", "tiep_noi", "chua_te", "chot_3", "but_chi", "trang_cuoi", "net_ket", "bia_so", "chot_4", "nanh", None]


def icons():
    # gán từng mảng điểm (liền theo 8 hướng, tính trên cả tấm) cho ô chứa tâm của nó: icon tràn mép ô vẫn đủ, phần tràn sang ô bên không
    # lẫn vào; bỏ chấm vụn (< 0,4% ô); nở mặt nạ 2 điểm giữ mép mờ của nét
    from scipy import ndimage
    im = Image.open(os.path.join(HERE, "tai_ve", "luoi_icon_san.png")).convert("RGBA")
    a = np.array(im)
    H, W = a.shape[:2]
    cw, ch = W / COLS, H / ROWS
    m = a[..., 3] >= 40
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    idx = range(1, n + 1)
    sizes = ndimage.sum(m, lab, idx)
    cents = ndimage.center_of_mass(m, lab, idx)
    total = 0
    for i, nid in enumerate(CELLS):
        if not nid:
            continue
        cx, cy = i % COLS, i // COLS
        mine = [k + 1 for k, (yc, xc) in enumerate(cents)
                if sizes[k] >= 0.004 * cw * ch and int(xc // cw) == cx and int(yc // ch) == cy]
        keep = ndimage.binary_dilation(np.isin(lab, mine), iterations=2)
        ys, xs = np.where(keep)
        b = a.copy()
        b[..., 3] = np.where(keep, b[..., 3], 0)
        cell = Image.fromarray(b).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
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
    print("ghi", sum(1 for c in CELLS if c), "icon", SIDE, "px, tổng", total // 1024, "KB ->", OUT)


def badge():
    s = np.array(Image.open(os.path.join(HERE, "tai_ve", "nut_chinh_phuc.png")).convert("RGBA"))
    m = s[..., 3] > 16
    ys, xs = np.where(m)
    cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
    r = max(ys.max() - ys.min(), xs.max() - xs.min()) / 2 + 1
    yy, xx = np.mgrid[0:s.shape[0], 0:s.shape[1]]
    d = np.hypot(yy - cy, xx - cx)
    s[..., 3] = (s[..., 3] * np.clip(r + 1 - d, 0, 1)).astype(np.uint8)
    side = int(np.ceil(2 * r + 4))
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.alpha_composite(Image.fromarray(s), (int(round(side / 2 - cx)), int(round(side / 2 - cy))))
    sq = sq.resize((256, 256), Image.LANCZOS)
    p = os.path.join(HUD, "nut_so_phep.png")
    sq.save(p, optimize=True)
    print("huy hiệu ->", p, os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__":
    icons()
    badge()
