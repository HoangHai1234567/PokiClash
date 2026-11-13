# -*- coding: utf-8 -*-
"""Voọc Tướng dạng 1 (kiem_si_non): đổi màu LÔNG cam của concept đã chọn sang xám (người dùng 2026-11-13, chọn L2_kiem_cun: "con này nhưng đổi
màu lông sang gần giống dạng [lớn] nhưng nhạt hơn"). Đổi bằng mã để giữ y từng nét của ảnh đã chọn (gen lại thì GPT vẽ khác).

Cách: điểm lông = sắc cam (hue 12–42°), độ bão hoà cao, không quá tối; trọng số mềm theo độ bão hoà và khoảng cách sắc (điểm nhoè giữa lông và
nét mực / nền trắng nhận một phần). Màu mới = màu đích × (độ sáng điểm / độ sáng trung vị của lông): giữ vân chì sáp. Không đụng (da đo s ≈ 0,48, lông s ≈ 0,82 → ngưỡng 0,62–0,72): da mặt, tay,
chân (bão hoà thấp), bờm kem, khăn, lá, vải chuôi; vùng gỉ trên lưỡi kiếm, kiếm cách gỗ, tròng mắt (loại theo chỗ).

    kiem_si_non_long.py [màu đích hex ...]    → inbox/kiem_si_non/tai_ve/L2_kiem_cun_<hex>.png + tờ so mau/_so_long.png
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TAI = os.path.join(HERE, "inbox", "kiem_si_non", "tai_ve")
MAU = os.path.join(HERE, "inbox", "kiem_si_non", "mau")
NGUON = os.path.join(TAI, "L2_kiem_cun.png")
LON = (0x40, 0x3E, 0x3A)                         # lông than của dạng lớn (prompt concept khi_mu)
# vùng không đổi (px trên ảnh 1536 × 1024): lưỡi kiếm phần lộ bên trái thân (có mảng gỉ cam), kiếm cách gỗ, mắt
LOAI = [("hop", 260, 500, 485, 720), ("hop", 925, 745, 1000, 865), ("tron", 1080, 400, 48)]


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mat_long(im):
    a = np.asarray(im.convert("RGB"), float) / 255.0
    hsv = np.asarray(im.convert("RGB").convert("HSV"), float) / 255.0
    h, s, v = hsv[..., 0] * 360.0, hsv[..., 1], hsv[..., 2]
    w = np.clip((s - 0.62) / 0.10, 0, 1) * np.clip(1 - (np.abs(h - 27.0) - 11.0) / 6.0, 0, 1) * np.clip((v - 0.30) / 0.15, 0, 1)
    H, W_ = w.shape
    yy, xx = np.mgrid[0:H, 0:W_]
    for z in LOAI:
        if z[0] == "hop":
            w[(xx >= z[1]) & (xx <= z[3]) & (yy >= z[2]) & (yy <= z[4])] = 0
        else:
            w[(xx - z[1]) ** 2 + (yy - z[2]) ** 2 <= z[3] ** 2] = 0
    L = a @ np.array([0.299, 0.587, 0.114])
    return a, w, L


def doi(im, dich):
    a, w, L = mat_long(im)
    L_med = float(np.median(L[w > 0.95]))
    T = np.array(dich, float) / 255.0
    moi = np.clip(T[None, None, :] * (L / L_med)[..., None], 0, 1)
    out = a * (1 - w[..., None]) + moi * w[..., None]
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8)), float((w > 0.5).mean())


def main(a):
    dich = a or ["#6F6A63", "#8E8982"]
    im = Image.open(NGUON).convert("RGB")
    ra = [("gốc (cam)", im)]
    for d in dich:
        o, ty = doi(im, hex_rgb(d))
        pth = os.path.join(TAI, f"L2_kiem_cun_{d.lstrip('#').lower()}.png")
        o.save(pth)
        print(pth, f"lông {ty * 100:.1f} % ảnh")
        ra.append((d, o))
    # tờ so: gốc | các màu | dạng lớn
    lon = Image.open(os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")).convert("RGB")
    ra.append(("dạng lớn", lon))
    w_, h_ = 768, 512
    so = Image.new("RGB", (w_ * len(ra), h_ + 30), (255, 255, 255))
    d_ = ImageDraw.Draw(so)
    for i, (t, x) in enumerate(ra):
        so.paste(x.resize((w_, h_)), (i * w_, 30))
        d_.text((i * w_ + 10, 8), t.replace("ố", "o").replace("ạ", "a").replace("ớ", "o").replace("á", "a"), fill=(0, 0, 0))
    pth = os.path.join(MAU, "_so_long.png")
    so.save(pth)
    print(pth, so.size)


if __name__ == "__main__":
    main(sys.argv[1:])
