# Hình ô lát của Nhà, vẽ bằng code theo nét game (tô chì gạch, nét mực rung), học cách Clash of Critters làm ô đường, ô nước:
# nền ô + "môi" chờm theo từng mép + tuýp góc trong + vách bờ của ô nước. Code (HomeScene) ghép theo ô hàng xóm nên các ô luôn liền.
# Thứ bậc chờm: cỏ > đường đá > cát > đất > nước. Mép giữa hai loại do loại thấp hơn vẽ môi của loại cao hơn chờm vào mình.
# Mọi ảnh cùng khung 224 x 128: chân thoi ô lát (2 x 2 ô lưới = 192 x 96 px ở zoom 1) đặt giữa, góc trên ở (112, 16).
# Ra Assets/03 Art/Home/tiles/: fill_<loại>.png, lip_<loại>_<mép>.png (mép 0..3 = +tx, +ty, -tx, -ty), cor_<loại>_<góc>.png (góc 0..3 =
# (+tx,+ty) dưới, (-tx,+ty) trái, (-tx,-ty) trên, (+tx,-ty) phải), bank_<mép>.png (mép 2, 3 của ô nước). Chạy: py -3 -I make_tiles.py
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Home", "tiles")
os.makedirs(OUT, exist_ok=True)
SS = 4  # vẽ phóng 4 lần rồi thu nhỏ cho nét mượt
W, H = 224, 128
TOP, RIGHT, BOT, LEFT = (112, 16), (208, 64), (112, 112), (16, 64)
INK = (64, 44, 32, 255)


def sample_grass():
    b = Image.open(os.path.join(ROOT, "Assets", "03 Art", "Home", "home_base.png")).convert("RGB")
    a = np.asarray(b).astype(int)[440:470, 690:760].reshape(-1, 3)
    g = a[(a[:, 1] > a[:, 0] + 20) & (a[:, 1] > 150)]
    return tuple(int(v) for v in np.median(g, axis=0)) if len(g) else (150, 210, 90)


GRASS = sample_grass()
COL = {
    "grass": GRASS,
    "stone": (196, 190, 178),
    "sand": (240, 218, 160),
    "dirt": (205, 160, 104),
    "water": (92, 170, 228),
}
PRIO = ["water", "dirt", "sand", "stone", "grass"]


def P(p):
    return (p[0] * SS, p[1] * SS)


def canvas():
    return Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))


def diamond_mask(grow=1.5):
    """chân thoi ô lát, phình ra grow px để hai ô cùng loại chồng khít (không lộ vệt khử răng cưa)"""
    m = Image.new("L", (W * SS, H * SS), 0)
    g = grow
    ImageDraw.Draw(m).polygon([P((TOP[0], TOP[1] - g)), P((RIGHT[0] + 2 * g, RIGHT[1])), P((BOT[0], BOT[1] + g)), P((LEFT[0] - 2 * g, LEFT[1]))], fill=255)
    return m


def darker(c, k=0.78):
    return tuple(int(v * k) for v in c[:3])


def lighter(c, k=0.18):
    return tuple(int(v + (255 - v) * k) for v in c[:3])


def over(img, mask, draw_fn):
    """vẽ lên một lớp riêng rồi phủ chồng (alpha_composite) trong vùng mask: nét mờ không đục thủng nền"""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay))
    la = np.asarray(lay.split()[3]).astype(np.uint16) * np.asarray(mask).astype(np.uint16) // 255
    lay.putalpha(Image.fromarray(la.astype(np.uint8)))
    img.alpha_composite(lay)


def hatch(img, mask, col, rnd, n=260, ln=(10, 22), alpha=70, ang=-0.55):
    """gạch chì: nét ngắn chéo, nhạt, trong vùng mask"""
    mw, mh = mask.size
    mp = mask.load()

    def fn(d):
        for _ in range(n):
            x, y = rnd.uniform(0, mw), rnd.uniform(0, mh)
            if mp[int(min(mw - 1, x)), int(min(mh - 1, y))] < 128:
                continue
            L = rnd.uniform(*ln) * SS
            a = ang + rnd.uniform(-0.15, 0.15)
            d.line([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], fill=col + (alpha,), width=SS)
    over(img, mask, fn)


def finish(img):
    return img.resize((W, H), Image.LANCZOS)


def fill(kind, seed):
    rnd = random.Random(seed)
    m = diamond_mask()
    img = canvas()
    base = Image.new("RGBA", img.size, COL[kind] + (255,))
    img.paste(base, (0, 0), m)
    d = ImageDraw.Draw(img)
    if kind == "dirt":
        hatch(img, m, darker(COL[kind]), rnd, 320)
        def peb(dd):
            for _ in range(40):  # sỏi, hạt đất
                x, y = rnd.uniform(30, 194) * SS, rnd.uniform(24, 104) * SS
                r = rnd.uniform(1.2, 2.6) * SS
                dd.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=darker(COL[kind], 0.68) + (200,))
        over(img, m, peb)
    elif kind == "sand":
        hatch(img, m, darker(COL[kind], 0.86), rnd, 220, alpha=55)
        def dots(dd):
            for _ in range(70):
                x, y = rnd.uniform(30, 194) * SS, rnd.uniform(24, 104) * SS
                r = rnd.uniform(0.7, 1.4) * SS
                dd.ellipse([x - r, y - r, x + r, y + r], fill=darker(COL[kind], 0.72) + (190,))
        over(img, m, dots)
    elif kind == "stone":
        hatch(img, m, darker(COL[kind], 0.85), rnd, 160, alpha=45)
        # đá cuội: viên tròn dẹt, viền mực
        for gy in range(3):
            for gx in range(4):
                u, v = (gx + 0.5 + rnd.uniform(-0.2, 0.2)) / 4, (gy + 0.5 + rnd.uniform(-0.2, 0.2)) / 3
                x = TOP[0] + (u - v) * 96
                y = TOP[1] + (u + v) * 48
                rx, ry = rnd.uniform(15, 20), rnd.uniform(7, 10)
                box = [P((x - rx, y - ry)), P((x + rx, y + ry))]
                box = [box[0][0], box[0][1], box[1][0], box[1][1]]
                d.ellipse(box, fill=lighter(COL[kind], rnd.uniform(0.05, 0.25)) + (255,), outline=darker(COL[kind], 0.55) + (255,), width=int(1.6 * SS))
        img.putalpha(Image.fromarray(np.minimum(np.asarray(img.split()[3]), np.asarray(m))))
    elif kind == "water":
        hatch(img, m, lighter(COL[kind], 0.35), rnd, 180, ln=(14, 30), alpha=90, ang=0.0)
        def ripple(dd):
            for _ in range(9):  # gợn trắng
                x, y = rnd.uniform(50, 174) * SS, rnd.uniform(34, 96) * SS
                w = rnd.uniform(8, 14) * SS
                dd.arc([x - w, y - w * 0.4, x + w, y + w * 0.4], 200, 340, fill=(255, 255, 255, 220), width=int(1.8 * SS))
        over(img, m, ripple)
    return finish(img)


# mép e: hai đầu (a, b) và pháp tuyến hướng vào trong ô
EDGES = {0: (RIGHT, BOT), 1: (BOT, LEFT), 2: (LEFT, TOP), 3: (TOP, RIGHT)}  # +tx dưới phải, +ty dưới trái, -tx trên trái, -ty trên phải
CORNERS = {0: BOT, 1: LEFT, 2: TOP, 3: RIGHT}
CENTER = (112, 64)


def inward(a, b):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    nx, ny = CENTER[0] - mx, CENTER[1] - my
    l = math.hypot(nx, ny)
    return nx / l, ny / l


def lip(kind, e, seed, depth=16.0, out=3.0):
    """môi chờm của loại kind phủ lên ô bên trong mép e: dải vỏ sò từ mép (lấn ra ngoài over px) vào trong depth px"""
    rnd = random.Random(seed)
    a, b = EDGES[e]
    nx, ny = inward(a, b)
    pts_out, pts_in = [], []
    N = 48
    ph = rnd.uniform(0, 6.28)
    for i in range(N + 1):
        t = i / N
        x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        # vỏ sò: nhiều nhịp tròn, nhỏ dần về hai đầu cho góc khép
        taper = min(1, t * 6, (1 - t) * 6)
        s = abs(math.sin(t * math.pi * 4.5 + ph)) * 0.6 + 0.4 + 0.08 * math.sin(t * 19 + ph * 2)
        dd = depth * s * (0.35 + 0.65 * taper)
        pts_out.append((x - nx * out, y - ny * out))
        pts_in.append((x + nx * dd, y + ny * dd))
    img = canvas()
    poly = [P(p) for p in pts_out + pts_in[::-1]]
    d = ImageDraw.Draw(img)
    c = COL[kind]
    d.polygon(poly, fill=c + (255,))
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    hatch(img, m, darker(c, 0.8), rnd, 90, ln=(6, 12), alpha=80)
    if kind == "grass":  # vài ngọn cỏ ở mép trong
        for i in range(2, N - 1, 5):
            x, y = pts_in[i]
            h = rnd.uniform(3, 6)
            d.line([P((x, y)), P((x + rnd.uniform(-1.5, 1.5), y - h))], fill=darker(c, 0.6) + (255,), width=int(1.4 * SS))
    d.line([P(p) for p in pts_in], fill=INK, width=int(1.7 * SS), joint="curve")
    return finish(img)


def corner(kind, k, seed, r=13.0):
    """tuýp góc trong: loại kind chờm vào góc k của ô (khi hai mép kề cùng loại với ô, ô chéo khác)"""
    rnd = random.Random(seed)
    cx, cy = CORNERS[k]
    vx, vy = CENTER[0] - cx, CENTER[1] - cy
    l = math.hypot(vx, vy)
    vx, vy = vx / l, vy / l
    img = canvas()
    d = ImageDraw.Draw(img)
    pts = []
    for i in range(25):
        ang = i / 24 * math.pi
        rr = r * (0.85 + 0.25 * abs(math.sin(i * 1.7 + rnd.uniform(0, 1))))
        # nửa vòng hướng vào trong ô, dẹt theo 2:1
        ux, uy = math.cos(ang), math.sin(ang)
        px = cx + (ux * -vy + uy * vx) * rr * 1.6
        py = cy + (ux * vx + uy * vy) * rr * 0.8
        pts.append((px, py))
    poly = [P(p) for p in pts]
    d.polygon(poly, fill=COL[kind] + (255,))
    d.line(poly[1:-1], fill=INK, width=int(1.6 * SS), joint="curve")
    return finish(img)


def bank(e, seed, depth=15.0):
    """vách bờ đất ở mép xa (-tx, -ty) của ô nước: thấy thành đất nâu dưới môi cỏ"""
    rnd = random.Random(seed)
    a, b = EDGES[e]
    nx, ny = inward(a, b)
    top_pts = [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t) for t in [i / 30 for i in range(31)]]
    bot_pts = [(x + nx * 2, y + depth + ny * 2 + math.sin(i * 0.9 + rnd.uniform(0, 1)) * 1.2) for i, (x, y) in enumerate(top_pts)]
    img = canvas()
    d = ImageDraw.Draw(img)
    poly = [P(p) for p in top_pts + bot_pts[::-1]]
    soil = (150, 104, 66)
    d.polygon(poly, fill=soil + (255,))
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    hatch(img, m, darker(soil, 0.7), rnd, 120, ln=(3, 7), alpha=120, ang=1.57)
    d.line([P(p) for p in bot_pts], fill=INK, width=int(1.6 * SS))
    d.line([P(p) for p in bot_pts], fill=(255, 255, 255, 200), width=int(1.0 * SS))  # viền bọt sát nước
    return finish(img)


if __name__ == "__main__":
    for k, kind in enumerate(["dirt", "sand", "stone", "water"]):
        fill(kind, 10 + k).save(os.path.join(OUT, f"fill_{kind}.png"))
    for kind in ["grass", "stone", "sand", "dirt"]:
        for e in range(4):
            lip(kind, e, 100 + e + PRIO.index(kind) * 10).save(os.path.join(OUT, f"lip_{kind}_{e}.png"))
            corner(kind, e, 200 + e + PRIO.index(kind) * 10).save(os.path.join(OUT, f"cor_{kind}_{e}.png"))
    for e in (2, 3):
        bank(e, 300 + e).save(os.path.join(OUT, f"bank_{e}.png"))
    print("ok", OUT, "cỏ", GRASS)
