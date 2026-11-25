# Sinh 2 sprite nấc chỉ số hình bình hành (người dùng 2026-11-24): nền trắng viền mực, lớp màu (trắng có gạch sáp chéo, nhân màu lúc chạy).
# Cỡ hiển thị 60 x 30 (rộng gấp đôi cao), nghiêng 11; ảnh 2x = 120 x 60. Vẽ ở 8x rồi thu nhỏ cho mịn.
import random, sys
from PIL import Image, ImageDraw

# chạy: py -3 -I nac_binh_hanh.py [thư mục ra] (mặc định: Assets/03 Art/Kit của project chứa script)
import os
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'Assets', '03 Art', 'Kit')
S = 8
W, H, SL, PAD = 120, 60, 22, 4  # khung ảnh 2x, độ nghiêng, lề trong suốt
INK = (43, 33, 24, 255)

def para(inset):
    # hình bình hành nghiêng phải (đỉnh lệch phải), thu vào inset px (2x)
    x0, x1, y0, y1 = PAD, W - PAD, PAD, H - PAD
    h, d = y1 - y0, inset
    k = d * ((SL * SL + h * h) ** 0.5) / h  # cạnh nghiêng dời ngang k thì cách cạnh cũ đúng d
    pts = [(x0 + k + SL * (h - d) / h, y0 + d), (x1 - k - SL * d / h, y0 + d),
           (x1 - k - SL * (h - d) / h, y1 - d), (x0 + k + SL * d / h, y1 - d)]
    return [(x * S, y * S) for x, y in pts]

def wobble(pts, amp, n=10):
    # nét tay hơi rung: chia mỗi cạnh thành n đoạn, lệch nhẹ
    rnd = random.Random(7)
    res = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        for j in range(n):
            t = j / n
            res.append((a[0] + (b[0] - a[0]) * t + rnd.uniform(-amp, amp) * S, a[1] + (b[1] - a[1]) * t + rnd.uniform(-amp, amp) * S))
    return res

# 1. nền: trắng, viền mực 5 px (2x)
img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
outer = wobble(para(0), 0.35)
d.polygon(outer, fill=INK)
d.polygon(wobble(para(5), 0.3), fill=(255, 255, 255, 255))
img.resize((W, H), Image.LANCZOS).save(out + "/nac_binh_hanh.png")

# 2. lớp màu: trắng, gạch sáp chéo xám nhạt (nhân màu thành sẫm hơn một bậc), nằm trong viền trắng 4 px
img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
mask = Image.new("L", (W * S, H * S), 0)
ImageDraw.Draw(mask).polygon(wobble(para(9), 0.25), fill=255)
fill = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
fd = ImageDraw.Draw(fill)
step, lw = 13 * S, 4 * S
for x in range(-H * S, W * S + H * S, step):
    fd.line([(x + SL * S, 0), (x, H * S)], fill=(214, 214, 214, 255), width=lw)
img.paste(fill, (0, 0), mask)
img.resize((W, H), Image.LANCZOS).save(out + "/nac_binh_hanh_mau.png")
print("ok")
