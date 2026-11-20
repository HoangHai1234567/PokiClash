# Ảnh cho biển Nhà kiểu Clash of Critters (GD_Claude/22_Critters_Home.md mục 4, shader PokiClash/UIHomeSea). Tự sinh, không dùng ảnh của họ.
# - home_sea.png (cùng tỉ lệ home_base.png, nửa cỡ): R dải mờ rộng, G dải vừa, B dải sắc sát bờ (1 ở bờ, 0 ra xa), A = vùng biển được
#   shader tô (biển nối ra rìa ảnh; hồ, suối bên trong giữ nguyên ảnh vẽ). Khoảng cách đo theo px ảnh nền gốc.
# - home_sea_flow.png 128 x 128: nhiễu dòng chảy RG lặp liền (tổng sóng sin tần số nguyên).
# - home_sea_caustic.png 512 x 512: G = mạng vân sáng dưới nước lặp liền (Voronoi F2 - F1), R = 0.
# - home_river.png (nửa cỡ ảnh nền): nước trong đảo cho vệt nước chảy (thác đổ xuống, suối về biển, lòng hồ đứng), xem build_river.
# Ra: Assets/03 Art/Baked/Home/. Chạy: py -3 -I make_home_sea.py [--preview]  (--preview ghép thử một khung ra sea/preview_sea.png)
import os, sys
import numpy as np
import cv2
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
CROSS = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))


def morph(mask, op, it):
    return cv2.morphologyEx(mask.astype(np.uint8), op, CROSS, iterations=it) > 0


def dilate(mask, it):
    return cv2.dilate(mask.astype(np.uint8), CROSS, iterations=it) > 0


def fill_holes(mask):
    m = mask.astype(np.uint8).copy()
    h, w = m.shape
    ff = np.pad(m, 1)
    cv2.floodFill(ff, None, (0, 0), 2)
    return (ff[1:-1, 1:-1] != 2)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(ROOT, "Assets", "03 Art", "Home", "home_base.png")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Baked", "Home")
os.makedirs(OUT, exist_ok=True)

# dải (px ảnh nền gốc 2210 rộng; một ô lưới khoảng 30 px ảnh gốc)
WIDE, MID, SHARP0, SHARP1 = 230.0, 105.0, 3.0, 24.0


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def sea_mask():
    a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    # cùng cách nhận biển như make_home_dist.py: xanh dương sáng nối ra mép dưới, trái, phải
    seaish = morph((B > 170) & (B - R > 45) & (G > 120), cv2.MORPH_CLOSE, 2)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(seaish.astype(np.uint8), connectivity=4)
    band = np.zeros_like(seaish)
    band[-8:] = True
    band[:, :8] = band[:, -8:] = True
    edge = [i for i in set(np.unique(lab[band & seaish])) - {0} if stats[i, cv2.CC_STAT_AREA] > 2000]
    sea = morph(np.isin(lab, edge), cv2.MORPH_OPEN, 1)
    holes = fill_holes(sea) & ~sea
    hn, hl, hs, _ = cv2.connectedComponentsWithStats(holes.astype(np.uint8), connectivity=4)
    small = np.isin(hl, [i for i in range(1, hn) if hs[i, cv2.CC_STAT_AREA] < 4000])
    sea = sea | small
    # đốm "đất" lẻ ở mép ảnh (nét sóng trắng vẽ tay): coi là biển, kẻo dải bờ mọc vòng quanh chúng
    ln, ll, ls, _ = cv2.connectedComponentsWithStats((~sea).astype(np.uint8), connectivity=4)
    specks = np.isin(ll, [i for i in range(1, ln) if ls[i, cv2.CC_STAT_AREA] < 400])
    return a, sea | specks


def build_mask(sea):
    P0 = 60
    padded = np.pad(sea, P0, constant_values=True).astype(np.uint8)  # ngoài ảnh coi là biển
    d = cv2.distanceTransform(padded, cv2.DIST_L2, 5)[P0:-P0, P0:-P0]  # khoảng cách từ biển tới đất gần nhất
    r = 1 - smooth(0, WIDE, d)
    g = 1 - smooth(0, MID, d)
    b = 1 - smooth(SHARP0, SHARP1, d)
    # vùng tô: biển, mép mềm 2 px, lấn lên bờ 2 px cho vạch bọt chạm cát
    a = cv2.GaussianBlur(dilate(sea, 2).astype(np.float32), (0, 0), 1.2)
    m = np.stack([r, g, b, np.clip(a, 0, 1)], -1)
    H, W = sea.shape
    img = Image.fromarray((m * 255 + 0.5).astype(np.uint8), "RGBA").resize((W // 2, H // 2), Image.LANCZOS)
    return img, d


def build_river(base, sea):
    """Nước trong đảo (thác, suối, hồ) cho vệt nước chảy của UIHomeSea, thay thác 4 khung của Critters.
    R = vùng nước, G/B = hướng chảy (x, y theo ảnh, y xuống; 0,5 = 0), A = tốc (1 thác, suối chậm hơn, lòng hồ 0)."""
    R, G, B = base[..., 0], base[..., 1], base[..., 2]
    wat = (B > 170) & (B - R > 45) & (G > 120)
    inland = wat & ~dilate(sea, 3)
    n, lab, st, _ = cv2.connectedComponentsWithStats(inland.astype(np.uint8), connectivity=8)
    H, W = sea.shape
    out = np.zeros((H, W, 4), np.float32)
    out[..., 1] = out[..., 2] = 0.5
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < 300:
            continue
        comp = lab == i
        inner = cv2.distanceTransform(comp.astype(np.uint8), cv2.DIST_L2, 3)  # bề rộng dòng: suối hẹp, lòng hồ rộng
        if h > 1.4 * w and a < 6000:            # thác: dải hẹp cao, đổ thẳng xuống
            d, speed = (0.0, 1.0), np.ones_like(inner)
        elif w > 3 * h or h > 3 * w or a > 8000:  # hồ + suối dài: chảy từ đầu xa mũi dưới về phía cửa suối (đáy bbox)
            ys, xs = np.where(comp)
            lo = np.argmax(ys)
            hi = np.argmin(ys)
            v = np.array([xs[lo] - xs[hi], ys[lo] - ys[hi]], float)
            d = tuple(v / max(np.linalg.norm(v), 1e-6))
            speed = np.clip((8.0 - inner) / 5.0, 0, 1) * 0.4  # suối chảy, lòng hồ đứng
        else:                                   # hồ nhỏ: đứng yên
            d, speed = (0.0, 0.0), np.zeros_like(inner)
        m = cv2.GaussianBlur(comp.astype(np.float32), (0, 0), 0.8)
        out[comp, 0] = 1
        out[comp, 1] = 0.5 + 0.5 * d[0]
        out[comp, 2] = 0.5 + 0.5 * d[1]
        out[comp, 3] = speed[comp]
        print("  nước trong đảo", (x, y, w, h), "hướng", tuple(round(c, 2) for c in d))
    img = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA").resize((W // 2, H // 2), Image.NEAREST)
    return img


def tile_noise(n=128, seed=3):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:n, 0:n] / n * 2 * np.pi
    ch = []
    for _ in range(2):
        v = np.zeros((n, n))
        for _k in range(14):
            fx, fy = rng.integers(-5, 6, 2)
            if fx == 0 and fy == 0: continue
            amp = 1.0 / (abs(fx) + abs(fy))
            v += amp * np.sin(fx * x + fy * y + rng.uniform(0, 2 * np.pi))
        v = (v - v.min()) / (v.max() - v.min())
        ch.append(v)
    rgb = np.stack([ch[0], ch[1], np.zeros((n, n))], -1)
    return Image.fromarray((rgb * 255 + 0.5).astype(np.uint8), "RGB")


def tile_caustic(n=512, cells=7, seed=11):
    rng = np.random.default_rng(seed)
    pts = (np.stack(np.mgrid[0:cells, 0:cells], -1).reshape(-1, 2) + rng.uniform(0.15, 0.85, (cells * cells, 2))) / cells
    y, x = (np.mgrid[0:n, 0:n] + 0.5) / n
    f1 = np.full((n, n), 9.0); f2 = np.full((n, n), 9.0)
    for px, py in pts:
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                dd = np.hypot(x - (px + ox), y - (py + oy))
                f2 = np.where(dd < f1, f1, np.minimum(f2, dd))
                f1 = np.minimum(f1, dd)
    e = (f2 - f1) * cells  # 0 trên đường ranh
    line = np.exp(-(e / 0.09) ** 2)
    line = cv2.GaussianBlur(line.astype(np.float32), (0, 0), 1.0)
    line /= line.max()
    rgb = np.stack([np.zeros((n, n)), line, np.zeros((n, n))], -1)
    return Image.fromarray((rgb * 255 + 0.5).astype(np.uint8), "RGB")


def hexc(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


# số mặc định của shader (đổi ở vật liệu home_sea.mat)
P = dict(base=hexc("4fa7e3"), wave=hexc("6fc9ee"), edge=hexc("9fe3f2"), foam=hexc("f2fdff"), caustic=np.array([0.06, 0.07, 0.07]),
         angle=0.61, speed=(1.0, 4.0), move=0.055, foamMove=0.01, gStr=0.3, grain=0.55, cScale=(5.0, 3.0), flowScale=2.0, flowFine=(6.0, 3.0),
         crisp=1.0, foamCut=0.5, edgeCut=0.22, steps=0)


def cut(x, c, crisp, w=0.035):
    """crisp = 0: giữ dải mềm như Critters; 1: mép sắc như nét vẽ (không quầng)."""
    hard = smooth(c - w, c + w, x)
    return x + (hard - x) * crisp


def preview(base_rgb, mask_img, flow, caus, t=7.0):
    """Mô phỏng UIHomeSea ngoài Unity (một khung) để soi màu, dải, bọt."""
    H, W = base_rgb.shape[:2]
    m = np.asarray(mask_img.resize((W, H), Image.BILINEAR)).astype(float) / 255
    fl = np.asarray(flow).astype(float) / 255
    ca = np.asarray(caus).astype(float) / 255
    v, u = np.mgrid[0:H, 0:W]
    uv = np.stack([(u + 0.5) / W, 1 - (v + 0.5) / H], -1)

    def samp(img, q):  # lặp liền, gần nhất là đủ để soi
        h, w = img.shape[:2]
        x = (np.floor(q[..., 0] * w).astype(int)) % w
        y = (np.floor((1 - q[..., 1]) * h).astype(int)) % h
        return img[y, x]

    def samp_clamp(img, q):
        h, w = img.shape[:2]
        x = np.clip((q[..., 0] * w).astype(int), 0, w - 1)
        y = np.clip(((1 - q[..., 1]) * h).astype(int), 0, h - 1)
        return img[y, x]

    tt = t / 20 * np.array(P["speed"])
    asp = np.array([max(W / H, 1), max(H / W, 1)])
    c = uv - 0.5
    s, co = np.sin(P["angle"]), np.cos(P["angle"])
    cc = c * asp
    rot = np.stack([co * cc[..., 0] - s * cc[..., 1], s * cc[..., 0] + co * cc[..., 1]], -1) + 0.5
    nA = samp(fl, uv * np.array(P["flowFine"]) + tt)[..., :2] - 0.5
    nB = samp(fl, rot * P["flowScale"] + tt)[..., :2] - 0.5
    bot0 = samp_clamp(m, uv + nA * P["foamMove"])[..., 2]
    bot = cut(bot0, P["foamCut"], P["crisp"])
    rg = samp_clamp(m, uv + nB * P["move"])[..., :2]
    rw = rg[..., 0]
    if P["steps"] > 0:
        k = P["steps"]
        rw = (np.floor(rw * k) + smooth(0.45, 0.55, (rw * k) % 1)) / k
    col = P["base"] + (P["wave"] - P["base"]) * rw[..., None]
    edge = cut(np.clip(rg[..., 1] - bot0, 0, 1), P["edgeCut"], P["crisp"]) * (1 - bot)
    band2 = np.clip(rg[..., 0] ** 2 - bot - edge, 0, 1)
    col = col + (P["edge"] - col) * edge[..., None]
    cg = samp(ca, uv * np.array(P["cScale"]) + nB[..., :1] * P["gStr"])[..., 1]
    col = col + (cg * (1 - band2))[..., None] * P["caustic"]
    lum = base_rgb.mean(-1, keepdims=True)
    ref = np.median(lum[m[..., 3] > 0.9])
    grain = 1 + (lum / max(ref, 1e-3) - 1) * P["grain"]
    col = col * grain
    col = col + (P["foam"] - col) * bot[..., None]
    out = base_rgb + (col - base_rgb) * m[..., 3:4]
    return np.clip(out, 0, 1)


if __name__ == "__main__":
    base, sea = sea_mask()
    mask, _ = build_mask(sea)
    mask.save(os.path.join(OUT, "home_sea.png"))
    flow = tile_noise(); flow.save(os.path.join(OUT, "home_sea_flow.png"))
    caus = tile_caustic(); caus.save(os.path.join(OUT, "home_sea_caustic.png"))
    river = build_river(base, sea); river.save(os.path.join(OUT, "home_river.png"))
    print("ok home_sea", mask.size, "biển", int(sea.sum()), "px; flow", flow.size, "; caustic", caus.size)
    if "--preview" in sys.argv:
        img = preview(base.astype(float) / 255, mask, flow, caus)
        Image.fromarray((img * 255).astype(np.uint8)).save(os.path.join(HERE, "preview_sea.png"))
        print("preview", os.path.join(HERE, "preview_sea.png"))
