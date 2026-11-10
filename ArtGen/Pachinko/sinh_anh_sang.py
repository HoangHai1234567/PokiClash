# Ảnh ánh sáng của máy bi sinh bằng code (2026-11-10). Người dùng: chép ánh sáng, gradient của máy bi tham khảo (lớp quầng mềm,
# tia, cột sáng, vệt lia, chấm LED). Ảnh mềm thuần (alpha chuyển dần) GPT vẽ không cắt nền sạch được, nên sinh ở đây. Ảnh trắng,
# game tô màu (Image.color) và có thể vẽ bằng material cộng sáng (PokiClash/UIAdditive). Tên tiền tố pk_g_ (không trùng Fallback).
#   pk_g_quang   quầng tròn mềm (lõi sáng, tắt dần ra mép)
#   pk_g_vong    vòng sáng mềm (vòng lan khi trúng)
#   pk_g_tia     tia sáng mềm toả từ tâm (16 tia dài ngắn xen nhau), đặt sau rương, thưởng, xoay chậm
#   pk_g_cot     cột sáng đứng: sáng ở đáy, tắt dần lên trên, mềm hai mép (từ rương mở, từ ô đáy)
#   pk_g_lia     dải sáng lia: dải đứng mềm hai bên (game nghiêng và quét qua bảng số, thanh cấp)
#   pk_g_doc     gradient dọc: trắng ở đáy, trong suốt ở đỉnh (sáng ô, ánh trên thanh)
#   pk_g_led     một chấm LED mềm, ô 32 px để lát (Image.Type.Tiled) phủ màn bảng số
#   pk_g_sao     lấp lánh bốn cánh mềm (chớp trên chữ số, trên rương)
# Chạy: py -3 -I ArtGen/Pachinko/sinh_anh_sang.py  (ghi Assets/03 Art/Pachinko/pk_g_*.png)
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "Assets" / "03 Art" / "Pachinko"


def save(alpha, name):
    a = np.clip(alpha, 0, 1)
    rgba = np.zeros(a.shape + (4,), np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = np.round(a * 255).astype(np.uint8)
    p = OUT / f"{name}.png"
    Image.fromarray(rgba).save(p, optimize=True)
    print(f"  {p.name} {a.shape[1]} x {a.shape[0]}, {p.stat().st_size // 1024} KB")


def grid(w, h):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    return (x + 0.5) / w * 2 - 1, (y + 0.5) / h * 2 - 1  # -1..1


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def glow(n=256):
    x, y = grid(n, n)
    r = np.sqrt(x * x + y * y)
    a = np.exp(-(r / 0.42) ** 2) * 0.85 + np.exp(-(r / 0.16) ** 2) * 0.15
    return a * (1 - smooth((r - 0.85) / 0.15))


def ring(n=256):
    x, y = grid(n, n)
    r = np.sqrt(x * x + y * y)
    a = np.exp(-((r - 0.72) / 0.11) ** 2)
    return a * (1 - smooth((r - 0.9) / 0.1))


def rays(n=512, count=16):
    x, y = grid(n, n)
    r = np.sqrt(x * x + y * y)
    th = np.arctan2(y, x)
    k = (th / (2 * np.pi) * count) % 1  # 0..1 trong một cặp tia
    idx = np.floor((th / (2 * np.pi) + 0.5) * count).astype(int)
    width = np.where(idx % 2 == 0, 0.30, 0.18)  # tia rộng, hẹp xen nhau
    length = np.where(idx % 2 == 0, 0.98, 0.72)
    core = np.exp(-(np.abs(k - 0.5) / (width * 1.3)) ** 2)  # giữa tia sáng nhất, mềm dần ra khe
    fall = (1 - smooth(r / length)) * smooth(r / 0.12)
    centre = np.exp(-(r / 0.22) ** 2) * 0.6
    return np.maximum(core * fall, centre) * (1 - smooth((r - 0.92) / 0.08))


def column(w=128, h=512):
    x, y = grid(w, h)
    t = (y + 1) / 2  # 0 đỉnh, 1 đáy
    side = np.exp(-(x / 0.55) ** 2)
    core = np.exp(-(x / 0.18) ** 2) * 0.5
    up = t ** 1.6
    return np.clip(side * up + core * up * up, 0, 1) * smooth((1 - t) / 0.03)  # đáy mềm vài px


def sweep(w=128, h=256):
    x, _ = grid(w, h)
    return np.exp(-(x / 0.45) ** 2) * 0.8 + np.exp(-(x / 0.12) ** 2) * 0.2


def vgrad(w=8, h=256):
    _, y = grid(w, h)
    t = (y + 1) / 2
    return t ** 1.8


def led(n=32):
    x, y = grid(n, n)
    r = np.sqrt(x * x + y * y)
    return np.exp(-(r / 0.42) ** 2) * (1 - smooth((r - 0.8) / 0.2))


def sparkle(n=192):
    x, y = grid(n, n)
    r = np.sqrt(x * x + y * y)
    arm = np.exp(-(np.abs(x) / 0.05) ** 2) * (1 - smooth(np.abs(y) / 0.95)) + \
        np.exp(-(np.abs(y) / 0.05) ** 2) * (1 - smooth(np.abs(x) / 0.95))
    return np.clip(arm + np.exp(-(r / 0.16) ** 2), 0, 1)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    save(glow(), "pk_g_quang")
    save(ring(), "pk_g_vong")
    save(rays(), "pk_g_tia")
    save(column(), "pk_g_cot")
    save(sweep(), "pk_g_lia")
    save(vgrad(), "pk_g_doc")
    save(led(), "pk_g_led")
    save(sparkle(), "pk_g_sao")


if __name__ == "__main__":
    main()
