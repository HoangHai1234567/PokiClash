# Chim, bướm, ong cho màn Nhà (người dùng 2026-11-23: "thêm chim chóc, bướm ong ... cho sinh động"). Vẽ tay giả lập theo nét lá gió
# (ArtGen/Home/wind/make_leaves.py): tô phẳng mỗi vùng một màu, viền mực nâu sẫm, không bóng, không quầng. Vẽ to gấp 4 rồi thu nhỏ.
# Ra: Assets/Resources/HomeLife/<tên>.png (HomeLife.cs nạp bằng Resources.Load), kèm .meta kiểu Sprite nếu chưa có.
#   bướm: butterfly_1..4 (nhìn từ trên, cánh xoè; game co giãn ngang để vỗ cánh)
#   ong: bee_1 (cánh xoè), bee_2 (cánh khép) (nhìn từ trên, đầu hướng lên)
#   chim: bird_<a|b>_1..3 (nhìn ngang, đầu sang phải; 1 cánh giương, 2 cánh ngang, 3 cánh cụp)
# Chạy: py -3 -I ArtGen/Home/life/make_life.py
import math
import os
import sys
import uuid

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "Resources", "HomeLife")
META_SRC = os.path.join(ROOT, "Assets", "03 Art", "Home", "home_leaf_1.png.meta")
INK = (66, 42, 26, 255)
K = 4


def canvas(w, h):
    im = Image.new("RGBA", (w * K, h * K), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def poly(d, pts, fill, ink=1.6):
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=INK, width=max(1, int(ink * K)), joint="curve")


def blob(cx, cy, rx, ry, rot=0.0, n=48, wob=None):
    """Elip (xoay rot độ), wob(t) nhân bán kính để méo nhẹ cho ra nét tay."""
    a = math.radians(rot)
    pts = []
    for i in range(n):
        t = i / n * 2 * math.pi
        k = wob(t) if wob else 1.0
        x, y = math.cos(t) * rx * k, math.sin(t) * ry * k
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return pts


def save(im, w, h, name):
    os.makedirs(OUT, exist_ok=True)
    im = im.resize((w, h), Image.LANCZOS)
    path = os.path.join(OUT, name + ".png")
    im.save(path)
    meta = path + ".meta"
    if not os.path.exists(meta):
        src = open(META_SRC, encoding="utf-8").read().splitlines()
        src[1] = "guid: " + uuid.uuid4().hex
        open(meta, "w", encoding="utf-8", newline="\n").write("\n".join(src) + "\n")
    return path


# ---------- bướm (nhìn từ trên, đầu hướng lên) ----------

def butterfly(name, wing, tip, spot, w=56, h=46):
    im, d = canvas(w, h)
    W, H = w * K, h * K
    cx, cy = W / 2, H * 0.52
    for side in (-1, 1):
        # cánh trước: giọt to chếch lên ngoài; cánh sau: giọt nhỏ chếch xuống ngoài
        fore = blob(cx + side * W * 0.22, cy - H * 0.13, W * 0.21, H * 0.27, rot=side * -28,
                    wob=lambda t: 1 - 0.12 * max(0, math.sin(t * 2)) ** 3)
        hind = blob(cx + side * W * 0.17, cy + H * 0.17, W * 0.15, H * 0.2, rot=side * 22)
        poly(d, hind, wing)
        poly(d, fore, wing)
        # mép cánh trước sẫm (một mảng phẳng) và chấm sáng
        tip_pts = blob(cx + side * W * 0.33, cy - H * 0.27, W * 0.1, H * 0.11, rot=side * -28)
        d.polygon(tip_pts, fill=tip)
        for (ox, oy, r) in ((0.3, -0.22, 0.03), (0.36, -0.12, 0.025)):
            x, y, rr = cx + side * W * ox, cy + H * oy, W * r
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=spot)
        x, y, rr = cx + side * W * 0.18, cy + H * 0.2, W * 0.04
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=spot)
    # thân thon và râu
    body = blob(cx, cy, W * 0.035, H * 0.3)
    poly(d, body, INK, ink=0.8)
    for side in (-1, 1):
        x0, y0 = cx + side * W * 0.01, cy - H * 0.28
        x1, y1 = cx + side * W * 0.12, cy - H * 0.46
        d.line([(x0, y0), ((x0 + x1) / 2 + side * W * 0.02, (y0 + y1) / 2), (x1, y1)], fill=INK, width=int(1.1 * K))
        d.ellipse([x1 - 1.6 * K, y1 - 1.6 * K, x1 + 1.6 * K, y1 + 1.6 * K], fill=INK)
    save(im, w, h, name)


# ---------- ong (nhìn từ trên, đầu hướng lên) ----------

def bee(name, open_wings, w=36, h=36):
    im, d = canvas(w, h)
    W, H = w * K, h * K
    cx, cy = W / 2, H * 0.56
    wing = (236, 246, 255, 255)
    for side in (-1, 1):
        if open_wings:
            pts = blob(cx + side * W * 0.22, cy - H * 0.16, W * 0.17, H * 0.12, rot=side * -35)
        else:
            pts = blob(cx + side * W * 0.13, cy + H * 0.02, W * 0.09, H * 0.2, rot=side * 12)
        poly(d, pts, wing, ink=1.3)
    body = blob(cx, cy + H * 0.04, W * 0.16, H * 0.24)
    poly(d, body, (250, 206, 64, 255), ink=1.4)
    # sọc nâu: dải ngang cắt theo thân
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).polygon(body, fill=255)
    stripes = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripes)
    for oy in (0.02, 0.15):
        y = cy + H * oy
        sd.rectangle([0, y - H * 0.035, W, y + H * 0.035], fill=(92, 58, 34, 255))
    im.paste(stripes, (0, 0), Image.composite(stripes, Image.new("RGBA", im.size, (0, 0, 0, 0)), mask).split()[3])
    d = ImageDraw.Draw(im)
    d.line(body + [body[0]], fill=INK, width=int(1.4 * K), joint="curve")
    head = blob(cx, cy - H * 0.22, W * 0.1, H * 0.09)
    poly(d, head, (92, 58, 34, 255), ink=1.2)
    save(im, w, h, name)


# ---------- chim (nhìn từ trên chéo xuống như góc máy isometric, bay sang phải) ----------
# Thân dọc theo đường bay, hai cánh xoè lên (cánh xa) và xuống (cánh gần, to hơn chút) trên màn. Khung 1: xoè hết (lượn), 2: nâng nửa,
# 3: cụp (đầu cánh vuốt về sau). Game đổi khung để vỗ cánh, lượn thì giữ khung 1.

def bird(name, frame, back, belly, w=72, h=72):
    im, d = canvas(w, h)
    W, H = w * K, h * K
    cx, cy = W * 0.5, H * 0.5
    span = {1: 0.44, 2: 0.29, 3: 0.15}[frame]
    sweep = {1: 0.1, 2: 0.16, 3: 0.24}[frame]  # đầu cánh lùi về sau bao nhiêu (theo W)

    def wing(side, k):
        # side -1: cánh xa (lên trên), +1: cánh gần (xuống dưới); k: cỡ
        sx, sy = cx + W * 0.06, cy + side * H * 0.04       # vai
        tx, ty = cx - W * sweep, cy + side * H * span * k  # đầu cánh
        rx, ry = cx - W * 0.16, cy + side * H * 0.03       # gốc sau (sát thân)
        pts = []
        for i in range(19):  # mép trước: cong phồng về phía trước
            t = i / 18
            x = sx + (tx - sx) * t + math.sin(t * math.pi) * W * 0.09
            y = sy + (ty - sy) * t
            pts.append((x, y))
        n = 3  # mép sau: 3 múi lông vũ
        for j in range(n):
            ax, ay = tx + (rx - tx) * j / n, ty + (ry - ty) * j / n
            bx, by = tx + (rx - tx) * (j + 1) / n, ty + (ry - ty) * (j + 1) / n
            for i in range(1, 9):
                t = i / 8
                x = ax + (bx - ax) * t - math.sin(t * math.pi) * W * 0.035
                y = ay + (by - ay) * t
                pts.append((x, y))
        return pts

    far = tuple(max(0, int(c * 0.84)) for c in back[:3]) + (255,)
    poly(d, wing(-1, 0.88), far)
    # đuôi xoè hình quạt chẻ
    tail = [(cx - W * 0.14, cy - H * 0.05), (cx - W * 0.36, cy - H * 0.1), (cx - W * 0.3, cy), (cx - W * 0.36, cy + H * 0.1),
            (cx - W * 0.14, cy + H * 0.05)]
    poly(d, tail, back)
    # thân (lưng nhìn từ trên), bụng lộ một dải phía dưới
    body = blob(cx + W * 0.02, cy, W * 0.2, H * 0.09, wob=lambda t: 1 + 0.12 * math.cos(t))
    poly(d, body, back)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).polygon(body, fill=255)
    bel = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(bel).polygon(blob(cx + W * 0.04, cy + H * 0.07, W * 0.17, H * 0.05), fill=belly)
    im.paste(bel, (0, 0), Image.composite(bel, Image.new("RGBA", im.size, (0, 0, 0, 0)), mask).split()[3])
    d = ImageDraw.Draw(im)
    d.line(body + [body[0]], fill=INK, width=int(1.6 * K), joint="curve")
    # đầu, mỏ, mắt (mắt bên gần người xem)
    hx, hy, hr = cx + W * 0.23, cy + H * 0.01, W * 0.085
    poly(d, blob(hx, hy, hr, hr * 0.92), back)
    beak = [(hx + hr * 0.8, hy - hr * 0.28), (hx + hr * 1.65, hy + hr * 0.05), (hx + hr * 0.8, hy + hr * 0.36)]
    poly(d, beak, (244, 168, 60, 255), ink=1.2)
    ex, ey = hx + hr * 0.25, hy + hr * 0.12
    d.ellipse([ex - 1.8 * K, ey - 1.8 * K, ex + 1.8 * K, ey + 1.8 * K], fill=INK)
    d.ellipse([ex - 0.5 * K, ey - 1.2 * K, ex + 0.5 * K, ey - 0.2 * K], fill=(255, 255, 255, 255))
    # cánh gần (trước thân)
    poly(d, wing(1, 1.0), back)
    save(im, w, h, name)


if __name__ == "__main__":
    butterfly("butterfly_1", (247, 164, 58, 255), (120, 66, 36, 255), (255, 244, 214, 255))   # cam
    butterfly("butterfly_2", (248, 216, 74, 255), (150, 110, 40, 255), (255, 250, 226, 255))  # vàng
    butterfly("butterfly_3", (126, 200, 240, 255), (52, 104, 168, 255), (240, 250, 255, 255)) # lam
    butterfly("butterfly_4", (246, 190, 214, 255), (196, 96, 140, 255), (255, 246, 250, 255)) # hồng
    bee("bee_1", True)
    bee("bee_2", False)
    for f in (1, 2, 3):
        bird("bird_a_%d" % f, f, (178, 122, 74, 255), (250, 236, 206, 255))  # sẻ nâu
        bird("bird_b_%d" % f, f, (78, 128, 200, 255), (252, 244, 228, 255))  # én lam
    print("ok ->", OUT)
