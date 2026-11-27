# Sinh sprite trắng (tô màu bằng màu Image) cho màn Sổ Phép nền tối (người dùng 2026-11-27: "nền tối thôi để nổi bật các skill tree, làm
# dạng cây hoặc graph toả ra nối bằng line"). Nét vẽ tay hơi rung như bút mực, mép khử răng cưa. Ra Assets/03 Art/SoPhep/ui/.
#   py -3 -I sinh_ui_toi.py
# - sp_dia.png      đĩa tròn đặc (nền ô)
# - sp_vong.png     vòng viền dày mỏng theo lực tay (viền ô)
# - sp_vong_chon.png vòng đứt nét (ô đang chọn, code cho xoay chậm)
# - sp_net.png      dải đường nối, mép mềm theo bề ngang (kéo dài theo x)
# - sp_bang.png     băng bo tròn đặc (băng tên chương, cắt 9 ô viền 40 px do SoPhepMenu đặt)
# - sp_bang_vien.png viền của băng trên
# - sp_cham.png     ô lát chấm sao mờ cho nền tối (lát lặp)
import math, os, random
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "SoPhep", "ui"))
os.makedirs(OUT, exist_ok=True)
SS = 4  # siêu lấy mẫu để khử răng cưa


def save(a, name):
    """a: mảng alpha 0..1 cỡ (H*SS, W*SS) -> ảnh trắng, alpha thu nhỏ"""
    h, w = a.shape[0] // SS, a.shape[1] // SS
    a = a.reshape(h, SS, w, SS).mean(axis=(1, 3))
    img = np.zeros((h, w, 4), np.uint8)
    img[..., :3] = 255
    img[..., 3] = np.clip(a * 255 + 0.5, 0, 255).astype(np.uint8)
    Image.fromarray(img, "RGBA").save(os.path.join(OUT, name))
    print("ghi", name, (w, h))


def wobble(theta, seed, amp):
    """bán kính rung theo góc: vài sóng chậm như tay vẽ"""
    rnd = random.Random(seed)
    r = np.zeros_like(theta)
    for k in (2, 3, 5, 7):
        r += amp / k * np.sin(k * theta + rnd.uniform(0, 6.28))
    return r


def polar(n):
    y, x = np.mgrid[0:n, 0:n].astype(np.float32)
    c = (n - 1) / 2
    dx, dy = x - c, y - c
    return np.hypot(dx, dy), np.arctan2(dy, dx)


# ---------- đĩa ----------
N = 256 * SS
r, th = polar(N)
R = 118 * SS + wobble(th, 1, 2.2 * SS)
save(np.clip(R - r + 0.5, 0, 1), "sp_dia.png")

# ---------- vòng (dày mỏng theo lực tay) ----------
Rm = 112 * SS + wobble(th, 2, 2.0 * SS)
half = (7.0 + 1.6 * np.sin(th * 2 + 0.7) + 0.8 * np.sin(th * 5 + 2.1)) * SS
save(np.clip(half - np.abs(r - Rm) + 0.5, 0, 1), "sp_vong.png")

# ---------- vòng đứt nét ----------
Rs = 120 * SS + wobble(th, 3, 1.2 * SS)
halfs = 4.5 * SS
ring = np.clip(halfs - np.abs(r - Rs) + 0.5, 0, 1)
seg = (th + math.pi) / (2 * math.pi) * 18  # 18 đoạn
dash = np.clip((0.62 - np.abs((seg % 1) - 0.5) * 2) * 6 + 0.5, 0, 1)  # gạch chiếm ~60% mỗi đoạn, đầu tròn mềm
save(ring * np.clip(dash, 0, 1), "sp_vong_chon.png")

# ---------- dải đường nối (64 x 16): lõi đặc 6 px, mép mềm 5 px mỗi bên ----------
H, W = 16 * SS, 64 * SS
yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
d = np.abs(yy - (H - 1) / 2) / SS
a = np.clip(1 - (d - 3) / 5, 0, 1)
save(a, "sp_net.png")


# ---------- băng bo tròn 128 x 96, bán kính 40 ----------
def roundbox(w, h, rad, wob_seed=None):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    px, py = x - (w - 1) / 2, y - (h - 1) / 2
    bx, by = w / 2 - 2 * SS, h / 2 - 2 * SS
    qx, qy = np.abs(px) - bx + rad, np.abs(py) - by + rad
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - rad


sd = roundbox(128 * SS, 96 * SS, 40 * SS)
save(np.clip(-sd + 0.5, 0, 1), "sp_bang.png")
save(np.clip(3.2 * SS - np.abs(sd + 4 * SS) + 0.5, 0, 1), "sp_bang_vien.png")

# ---------- chấm sao mờ lát lặp 256 x 256 ----------
T = 256 * SS
a = np.zeros((T, T), np.float32)
rnd = random.Random(7)
y, x = np.mgrid[0:T, 0:T].astype(np.float32)
for i in range(26):
    cx, cy = rnd.uniform(0, T), rnd.uniform(0, T)
    rad = rnd.choice([1.2, 1.4, 1.8, 2.4, 3.2]) * SS
    br = rnd.uniform(0.35, 1.0)
    for ox in (-T, 0, T):  # lát liền mép
        for oy in (-T, 0, T):
            dd = np.hypot(x - cx - ox, y - cy - oy)
            a = np.maximum(a, br * np.clip(rad - dd + 0.5, 0, 1))
save(a, "sp_cham.png")
