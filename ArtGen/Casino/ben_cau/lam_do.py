# Đồ nhỏ cho scene Bến câu (GD_Claude/32): phao, giọt nước, con cá (trắng, tô màu theo hệ lúc chạy, chờ C8 có hình cá thật).
# Vẽ bằng mã cho nhẹ, nét chì như nền: tô phẳng + vân chì gạch chéo nhẹ, viền nâu mảnh như vật trên ảnh nền (không bóng, không sáng).
# Ra: Assets/03 Art/Casino/BenCau/ben_cau_phao.png, ben_cau_giot.png, ben_cau_ca.png. Chạy: py -3 -I lam_do.py
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Casino", "BenCau"))
INK = (92, 52, 30, 255)
K = 4  # vẽ to 4 lần rồi thu nhỏ cho mép mượt
rng = np.random.default_rng(7)


def hatch(im, strength=22):
    # vân chì: gạch chéo -38° đứt quãng, nhân tối nhẹ trong vùng có màu
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx * np.cos(np.radians(-38)) + yy * np.sin(np.radians(-38))) / (2.2 * K)
    v = (-xx * np.sin(np.radians(-38)) + yy * np.cos(np.radians(-38))) / (9.0 * K)
    noise = rng.random((h // (3 * K) + 2, w // (3 * K) + 2))
    n = np.kron(noise, np.ones((3 * K, 3 * K)))[:h, :w]
    line = ((np.sin(u * np.pi * 2) > 0.55) & (np.sin(v * 6.28 + n * 6) > -0.3)).astype(np.float32)
    k = 1 - line * strength / 255.0 - (n - 0.5) * 0.05
    a[..., :3] *= k[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


def finish(big, name):
    big = hatch(big)
    small = big.resize((big.width // K, big.height // K), Image.LANCZOS)
    small.save(os.path.join(OUT, name))
    print(name, small.size)


def phao():
    W, H = 44 * K, 64 * K
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = W // 2
    lw = int(1.6 * K)
    # que trên
    d.rectangle([cx - 2 * K, 4 * K, cx + 2 * K, 26 * K], fill=(250, 244, 230, 255), outline=INK, width=lw)
    # thân: nửa trên trắng, nửa dưới đỏ (hình giọt tròn)
    box = [cx - 18 * K, 20 * K, cx + 18 * K, 58 * K]
    d.ellipse(box, fill=(232, 72, 52, 255))
    d.pieslice(box, 180, 360, fill=(250, 246, 236, 255))
    d.ellipse(box, outline=INK, width=lw)
    d.line([box[0] + lw, 39 * K, box[2] - lw, 39 * K], fill=INK, width=lw)
    finish(im, "ben_cau_phao.png")


def giot():
    W, H = 20 * K, 26 * K
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([3 * K, 8 * K, 17 * K, 23 * K], fill=(246, 252, 255, 255))
    d.polygon([(10 * K, 1 * K), (4 * K, 14 * K), (16 * K, 14 * K)], fill=(246, 252, 255, 255))
    im = im.filter(ImageFilter.GaussianBlur(0.6 * K))
    a = np.asarray(im).copy()
    a[..., 3] = np.where(a[..., 3] > 110, 255, 0)
    finish(Image.fromarray(a, "RGBA"), "ben_cau_giot.png")


def ca():
    W, H = 120 * K, 64 * K
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lw = int(1.8 * K)
    body = [22 * K, 10 * K, 104 * K, 54 * K]
    tail = [(26 * K, 32 * K), (4 * K, 12 * K), (10 * K, 32 * K), (4 * K, 52 * K)]
    fin = [(60 * K, 12 * K), (72 * K, 2 * K), (80 * K, 14 * K)]
    for poly in (tail, fin):
        d.polygon(poly, fill=(255, 255, 255, 255))
    d.ellipse(body, fill=(255, 255, 255, 255))
    # viền
    d.polygon(tail, outline=INK)
    d.line(tail + [tail[0]], fill=INK, width=lw)
    d.line(fin, fill=INK, width=lw)
    d.ellipse(body, outline=INK, width=lw)
    # mắt, mang
    d.ellipse([88 * K, 24 * K, 95 * K, 31 * K], fill=INK)
    d.arc([70 * K, 16 * K, 88 * K, 48 * K], 290, 70, fill=INK, width=lw)
    finish(im, "ben_cau_ca.png")


if __name__ == "__main__":
    phao()
    giot()
    ca()
