# Dán bến tàu (ảnh GPT sửa vùng góc đông nam đảo Thủy, ben_tau_vung_1.png) vào bản đồ thế giới:
# 1. thu ảnh sửa về cỡ vùng cắt (464 x 309), dò tỉ lệ + dời cho khớp ảnh gốc ở phần không đổi (ngoài vùng bến);
# 2. mặt nạ = chỗ khác ảnh gốc nhiều, trong khung bến (bến, thùng, vòng bọt quanh cọc, chỗ bỏ đá / san hô), nở + làm mềm mép;
# 3. ra concept_I_ben_tau.png (bản đồ 1024 x 1536 có bến), build_sanh.py đọc ảnh này.
# py -3 -I ghep_ben.py  [--soi]  (--soi: ảnh soi mặt nạ ra soi_ghep_ben.png)
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SANH = os.path.dirname(HERE)
SRC = os.path.join(SANH, "concept_I_bo_pha_le_1.png")
EDIT = os.path.join(HERE, "ben_tau_vung_1.png")
OUT = os.path.join(SANH, "concept_I_ben_tau.png")
BOX = (560, 1200, 1024, 1509)  # vùng đã gửi GPT (toạ độ bản đồ 1024 x 1536)
# khung được phép đổi (toạ độ bản đồ): bến + thùng ở đầu bến + chỗ bỏ hòn đá, san hô bên phải
KEEP = [(630, 1330, 906, 1422), (866, 1306, 916, 1342)]
# chỗ bỏ hòn đá + san hô: thay hẳn (không xét khác biệt)
FULL = [(842, 1334, 950, 1410)]


def fit(orig, edit):
    """Dò tỉ lệ s và dời (dx, dy) để edit khớp orig ngoài khung đổi (sai số tuyệt đối trung bình)."""
    w, h = orig.size
    o = np.asarray(orig.convert("L"), dtype=np.float32)
    m = np.ones((h, w), bool)
    for x0, y0, x1, y1 in KEEP + FULL:
        m[max(0, y0 - BOX[1] - 10):y1 - BOX[1] + 10, max(0, x0 - BOX[0] - 10):x1 - BOX[0] + 10] = False
    best = None
    for s in np.arange(0.96, 1.045, 0.01):
        big = edit.resize((round(w * s), round(h * s)), Image.LANCZOS)
        b = np.asarray(big.convert("L"), dtype=np.float32)
        cx, cy = (b.shape[1] - w) / 2, (b.shape[0] - h) / 2
        for dy in range(-8, 9, 2):
            for dx in range(-8, 9, 2):
                x0, y0 = int(round(cx + dx)), int(round(cy + dy))
                if x0 < 0 or y0 < 0 or x0 + w > b.shape[1] or y0 + h > b.shape[0]:
                    pad = np.full((h, w), np.nan, np.float32)
                    sx0, sy0 = max(0, x0), max(0, y0)
                    sx1, sy1 = min(b.shape[1], x0 + w), min(b.shape[0], y0 + h)
                    pad[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = b[sy0:sy1, sx0:sx1]
                    win = pad
                else:
                    win = b[y0:y0 + h, x0:x0 + w]
                d = np.abs(win - o)
                v = np.nanmean(d[m])
                if best is None or v < best[0]:
                    best = (v, s, dx, dy)
    return best


def warp(edit, size, s, dx, dy):
    w, h = size
    big = edit.resize((round(w * s), round(h * s)), Image.LANCZOS)
    cx, cy = (big.width - w) / 2, (big.height - h) / 2
    x0, y0 = int(round(cx + dx)), int(round(cy + dy))
    out = Image.new("RGB", (w, h))
    out.paste(big, (-x0, -y0))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    src = Image.open(SRC).convert("RGB")
    orig = src.crop(BOX)
    w, h = orig.size
    edit = Image.open(EDIT).convert("RGB")
    # dò thô ở cỡ vùng cắt (ảnh sửa thu về gấp đôi rồi khớp ở cỡ gốc)
    small = edit.resize((w, h), Image.LANCZOS)
    v, s, dx, dy = fit(orig, small)
    print(f"khớp: sai {v:.1f}, tỉ lệ {s:.2f}, dời ({dx}, {dy})")
    al = warp(edit.resize((w * 2, h * 2), Image.LANCZOS).resize((w, h), Image.LANCZOS), (w, h), s, dx, dy)

    # so trên ảnh đã làm mờ: bỏ qua vân chì GPT vẽ lại, chỉ bắt chỗ đổi thật (bến, vòng bọt, thùng)
    a = np.asarray(al.filter(ImageFilter.GaussianBlur(1.6)), dtype=np.int16)
    o = np.asarray(orig.filter(ImageFilter.GaussianBlur(1.6)), dtype=np.int16)
    diff = np.abs(a - o).sum(2)
    mask = np.zeros((h, w), np.uint8)
    for x0, y0, x1, y1 in KEEP:
        sub = diff[y0 - BOX[1]:y1 - BOX[1], x0 - BOX[0]:x1 - BOX[0]]
        mask[y0 - BOX[1]:y1 - BOX[1], x0 - BOX[0]:x1 - BOX[0]] = np.where(sub > 55, 255, 0)
    mk = Image.fromarray(mask).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(3))
    # lấp lỗ trong mặt bến (ván cùng màu cát có thể không vượt ngưỡng)
    mk = mk.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7))
    # cắt mặt nạ trong khung đổi rồi làm mềm mép
    clip = Image.new("L", (w, h), 0)
    from PIL import ImageDraw
    dr = ImageDraw.Draw(clip)
    for x0, y0, x1, y1 in KEEP:
        dr.rectangle([x0 - BOX[0], y0 - BOX[1], x1 - BOX[0], y1 - BOX[1]], fill=255)
    mk = Image.fromarray(np.minimum(np.asarray(mk), np.asarray(clip)))
    dr2 = ImageDraw.Draw(mk)
    for x0, y0, x1, y1 in FULL:
        dr2.rounded_rectangle([x0 - BOX[0], y0 - BOX[1], x1 - BOX[0], y1 - BOX[1]], radius=14, fill=255)
    mk = mk.filter(ImageFilter.GaussianBlur(2.2))
    patched = Image.composite(al, orig, mk)
    out = src.copy()
    out.paste(patched, BOX[:2])
    out.save(OUT)
    print("ra", OUT)
    if "--soi" in sys.argv:
        z = 2
        sheet = Image.new("RGB", (w * z * 3, h * z), "white")
        sheet.paste(orig.resize((w * z, h * z)), (0, 0))
        sheet.paste(patched.resize((w * z, h * z)), (w * z, 0))
        red = Image.new("RGB", (w, h), (255, 0, 0))
        sheet.paste(Image.composite(red, orig, mk).resize((w * z, h * z)), (w * z * 2, 0))
        sheet.save(os.path.join(HERE, "soi_ghep_ben.png"))


if __name__ == "__main__":
    main()
