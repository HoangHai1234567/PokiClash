# Vẽ hình hiệu ứng tạm cho máy bi Unity (ảnh thay thế, Assets/03 Art/Fallback): gần trắng để code tô màu, như bảng P4 của
# ArtGen/Pachinko/PROMPTS.md. Có ảnh gen cùng tên trong Assets/03 Art/Pachinko thì ArtLibrary dùng ảnh gen thay.
#   fx_glow    quầng tròn mềm (loé, quầng sau đinh, chớp)
#   fx_ring    vòng sáng mỏng (vòng lan)
#   fx_sparkle sao bốn cánh nhỏ
#   fx_star    sao năm cánh mập, viền mực (sao bắn ra)
#   fx_streak  vệt thuôn ngang, đầu sáng bên phải (tia, vệt chéo)
#   fx_puff    cụm khói nhỏ (lúc thả bi)
#   pk_bumper  nấm đỏ chấm trắng (nấm động, phồng xẹp khi bị chạm; ảnh tĩnh máy không vẽ nấm nữa)
#   py -3 -I scripts/draw_machine_fx.py "../Assets/03 Art/Fallback"
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

INK = (43, 33, 24, 255)
WHITE = (255, 255, 255, 255)
BUMPER = (232, 85, 63, 255)


def white(alpha):
    img = Image.new('RGBA', alpha.size, (255, 255, 255, 0))
    img.putalpha(alpha)
    return img


def _max(a, b):
    from PIL import ImageChops
    return ImageChops.lighter(a, b)


def radial(size, alpha_of_r):
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    px = img.load()
    c = (size - 1) / 2
    for y in range(size):
        for x in range(size):
            r = math.hypot(x - c, y - c) / (size / 2)
            a = max(0.0, min(1.0, alpha_of_r(r)))
            px[x, y] = (255, 255, 255, int(round(a * 255)))
    return img


def glow():
    # lõi sáng đặc rồi tắt dần mềm tới mép
    return radial(128, lambda r: min(1.0, 1.25 * (1 - r) ** 1.3) if r < 1 else 0)


def ring():
    return radial(128, lambda r: math.exp(-((r - 0.8) / 0.09) ** 2) if r < 1 else 0)


def sparkle():
    s, ss = 128, 4
    big = Image.new('RGBA', (s * ss, s * ss), (255, 255, 255, 0))
    d = ImageDraw.Draw(big)
    c = s * ss / 2
    for ang in (0, 90):
        a = math.radians(ang)
        ca, sa = math.cos(a), math.sin(a)
        L, W = c * 0.96, c * 0.16
        pts = [(c + ca * L, c + sa * L), (c - sa * W, c + ca * W), (c - ca * L, c - sa * L), (c + sa * W, c - ca * W)]
        d.polygon(pts, fill=WHITE)
    a = big.resize((s, s), Image.LANCZOS).getchannel('A')
    halo = glow().getchannel('A').point(lambda v: v * 0.5)
    return white(_max(a, halo))


def star():
    s, ss = 128, 4
    big = Image.new('RGBA', (s * ss, s * ss), (255, 255, 255, 0))
    d = ImageDraw.Draw(big)
    c = s * ss / 2
    R, r = c * 0.86, c * 0.46
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = R if i % 2 == 0 else r
        pts.append((c + math.cos(a) * rr, c + 0.04 * c + math.sin(a) * rr))
    d.polygon(pts, fill=WHITE, outline=INK, width=int(5 * ss))
    return big.resize((s, s), Image.LANCZOS)


def streak():
    w, h = 256, 48
    img = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    px = img.load()
    for y in range(h):
        for x in range(w):
            u = x / (w - 1)  # 0 đuôi → 1 đầu
            half = 0.5 * (0.15 + 0.85 * u ** 0.7)  # thuôn về đuôi
            v = abs((y + 0.5) / h - 0.5)
            edge = max(0.0, 1 - v / half) if half > 0 else 0
            head = min(1.0, (1 - u) / 0.12)  # đầu tròn mềm
            a = (u ** 0.8) * edge ** 1.2 * head
            px[x, y] = (255, 255, 255, int(round(max(0, min(1, a)) * 255)))
    return img


def puff():
    s, ss = 128, 4
    big = Image.new('RGBA', (s * ss, s * ss), (255, 255, 255, 0))
    d = ImageDraw.Draw(big)
    for cx, cy, r in ((0.5, 0.56, 0.3), (0.3, 0.6, 0.2), (0.7, 0.6, 0.21), (0.42, 0.4, 0.2), (0.6, 0.42, 0.18)):
        d.ellipse([(cx - r) * s * ss, (cy - r) * s * ss, (cx + r) * s * ss, (cy + r) * s * ss], fill=WHITE)
    return white(big.resize((s, s), Image.LANCZOS).getchannel('A').filter(ImageFilter.GaussianBlur(3)))


def bumper():
    # cùng nét với nấm của ảnh tĩnh cũ (draw_machine.py): r 15 đơn vị máy, viền 3, bốn chấm trắng; ảnh 2 px mỗi đơn vị
    K, ss = 2, 4
    r, pad = 15, 2
    s = int((2 * r + 2 * pad) * K)
    big = Image.new('RGBA', (s * ss, s * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    k = K * ss
    c = (r + pad) * k
    w = int(round(3 * k))
    d.ellipse([c - r * k, c - r * k, c + r * k, c + r * k], fill=BUMPER, outline=INK, width=w)
    for dx, dy, rr in ((-6, -5, 3.5), (5, -7, 2.6), (6, 4, 3), (-3, 6, 2.2)):
        d.ellipse([c + (dx - rr) * k, c + (dy - rr) * k, c + (dx + rr) * k, c + (dy + rr) * k], fill=WHITE)
    return big.resize((s, s), Image.LANCZOS)


def main(dst):
    os.makedirs(dst, exist_ok=True)
    for name, fn in (('fx_glow', glow), ('fx_ring', ring), ('fx_sparkle', sparkle), ('fx_star', star),
                     ('fx_streak', streak), ('fx_puff', puff), ('pk_bumper', bumper)):
        img = fn()
        path = os.path.join(dst, name + '.png')
        img.save(path)
        print('ghi', path, img.size)


if __name__ == '__main__':
    main(sys.argv[1])
