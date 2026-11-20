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
#   pk_g_chum    chùm tia sáng toả lên từ một điểm ở đáy (rương mở, theo ảnh mẫu người dùng gửi 2026-11-21: tia dài ngắn, rộng hẹp
#                xen nhau, sáng ở gốc tắt dần ra ngọn, nền quạt mờ); gốc ở (0,5; 0,03) tính từ đáy
#   pk_g_loe     loé ngang ở gốc chùm tia: lõi tròn sáng + vệt ngang mảnh
# Chạy: py -3 -I ArtGen/Pachinko/sinh_anh_sang.py  (ghi Assets/03 Art/Pachinko/pk_g_*.png); thêm --moi: chỉ ghi pk_g_chum, pk_g_loe
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


def fan(n=512, count=17, seed=11):
    """Chùm tia toả lên: gốc ở giữa đáy, tia trong ±74° quanh trục đứng."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:n, 0:n].astype(np.float32)
    ox, oy, R = n / 2, n * 0.97, n * 0.94
    dx, dy = x + 0.5 - ox, oy - (y + 0.5)  # dy dương: lên trên
    r = np.sqrt(dx * dx + dy * dy) / R
    phi = np.arctan2(dx, np.maximum(dy, 1e-3))  # 0 = thẳng lên
    angs = np.linspace(-74, 74, count) + rng.uniform(-4, 4, count)
    keep = 1.0
    for i, a in enumerate(angs):
        wide = i % 3 == 0
        sig = np.radians(rng.uniform(3.2, 5.0) if wide else rng.uniform(1.1, 2.2))
        length = rng.uniform(0.78, 1.0) if wide else rng.uniform(0.45, 0.9)
        length *= 1 - 0.25 * (abs(a) / 74) ** 2  # tia hai bên ngắn hơn tia giữa
        inten = rng.uniform(0.55, 0.8) if wide else rng.uniform(0.7, 1.0)
        across = np.exp(-((phi - np.radians(a)) / sig) ** 2)
        along = (1 - smooth(r / length)) ** 1.4
        keep = keep * (1 - inten * across * along)  # chồng kiểu screen: không cháy trắng chỗ tia gặp nhau
    beams = 1 - keep
    haze = 0.22 * np.exp(-(phi / 1.05) ** 2) * (1 - smooth(r / 0.75)) ** 1.6
    core = np.exp(-(r / 0.07) ** 2)
    a = 1 - (1 - beams) * (1 - haze) * (1 - core)
    a *= smooth((dy / R + 0.02) / 0.04)  # dưới gốc tắt nhanh
    return a * (1 - smooth((r - 0.96) / 0.04))


def flare(w=512, h=128):
    x, y = grid(w, h)
    xs, ys = x, y * h / w  # toạ độ cùng tỉ lệ theo bề ngang
    r = np.sqrt(xs * xs + ys * ys)
    streak = np.exp(-(np.abs(y) / 0.16) ** 2) * (1 - smooth(np.abs(x))) ** 2.2
    core = np.exp(-(r / 0.05) ** 2) + 0.5 * np.exp(-(r / 0.1) ** 2)  # mép trên / dưới ảnh ở r 0,25: lõi đã tắt hẳn
    return np.clip(np.maximum(streak, core), 0, 1) * (1 - smooth((np.abs(y) - 0.8) / 0.2))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    save(fan(), "pk_g_chum")
    save(flare(), "pk_g_loe")
    if "--moi" in sys.argv:
        return
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
