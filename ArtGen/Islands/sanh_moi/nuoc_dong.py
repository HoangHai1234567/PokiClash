# Nước chảy trên bản đồ sảnh (người dùng 2026-11-23: "các phần nước suối này vẫn hơi tĩnh, học hỏi Kingdom Rush 5 ... làm nước động hơn").
# Học từ KR5 (ArtGen/ThamKhao/KR5, D:\Ripper\KingdomRush5): thác là tấm nước có vệt sáng trôi xuống (chuỗi 9 khung), chân thác có cụm
# bọt cuộn + vòng gợn toả ra; sông là nét bọt trắng trôi xuôi, phình rồi mờ; mặt biển có đốm lấp lánh đổi hình. Ở đây không vẽ lại thác:
# shader PokiClash/UIFlowWater cuộn chính nét vẽ của bản đồ theo hướng chảy (giữ nét tay), cộng vệt sáng / bọt sinh theo nhiễu.
# Ra (chạy lại được, không đụng ảnh đảo):
#   Assets/03 Art/Islands/sanh_nuoc_<đảo>.png               : ảnh phủ nước từng đảo (cỡ ảnh đảo x2), RGB = màu nước lan ra ngoài mép (lấy
#                                                             mẫu lệch không ăn vào bờ), A = mặt nạ nước
#   Assets/03 Art/Baked/Islands/Resources/sanh_nuoc_<đảo>_hc.png : trường hướng chảy (1/4 cỡ ảnh phủ): R, G = hướng (x phải, y xuống)
#                                                             * 0,5 + 0,5; B = 1 ở thác (chảy thẳng xuống), 0 ở sông
#   Assets/03 Art/Islands/Anim/anim_bot_*.png, anim_vong.png, anim_lap_*.png : bọt chân thác, vòng gợn, đốm lấp lánh (vẽ phẳng, không viền mực)
#   khoá world_map trong island_anim.json: "flows" (ảnh phủ theo đảo) và các món "splash" / "rings" / "glint" (thay "foam" cũ ở chân thác)
#   nuoc_dong/xem_<đảo>.gif : xem trước cùng công thức shader
# Toạ độ trong file này: ảnh nới 1024 x 1796 (= world_map.png / 2, tranh gốc + TOP 90 của build_sanh.py).
# Chạy: py -3 -I nuoc_dong.py [--xem]
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tach_dao  # noqa: E402
sys.path.insert(0, os.path.join(HERE, "trung_sanh"))
import trung_sanh  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Islands")
ANIM_DIR = os.path.join(ART, "Anim")
FLOW_DIR = os.path.join(ROOT, "Assets", "03 Art", "Baked", "Islands", "Resources")
PREVIEW = os.path.join(HERE, "nuoc_dong")
W1, H1 = 1024, 1796

# vùng được có nước chảy (chữ nhật x0, y0, x1, y1), trừ EXCLUDE (vách băng đảo Kim: vệt lam là băng, để yên)
REGIONS = [(100, 420, 560, 1075), (630, 1275, 725, 1400)]
EXCLUDE = [(405, 380, 610, 600)]
# thác: trong ô này nước chảy thẳng xuống (vệt trôi nhanh); chân thác (x, y) có bọt cuộn và vòng gợn
FALLS = [
    ((168, 446, 188, 482), (178, 484), 0.7),   # Mộc trên, thác nhỏ dưới dòng từ núi lửa
    ((256, 503, 290, 558), (273, 560), 0.9),
    ((316, 578, 348, 632), (332, 634), 0.9),
    ((468, 640, 497, 692), (479, 695), 0.9),   # hẻm Mộc – Thổ, dưới cầu treo
    ((468, 752, 492, 808), (483, 811), 0.85),
    ((125, 986, 165, 1058), (145, 1063), 0.95),  # Mộc dưới, đổ ra biển
    ((199, 993, 242, 1068), (221, 1073), 0.95),
    ((643, 1289, 714, 1378), (679, 1384), 0.95),  # đảo Thủy
]
SOURCES = [(128, 432), (268, 896)]  # đầu nguồn: dòng từ núi lửa, dòng từ bậc cây thần; cụm khác lấy điểm cao nhất
RIVER_SPEED = 13.0  # px ảnh nới / giây (vệt bọt sông trôi)
FALL_SPEED = 42.0   # px ảnh nới / giây (vệt thác trôi xuống)
PERIOD = 15.0       # px ảnh nới giữa hai dải bọt sông (pha ghi vào trường)
# lấp lánh mặt biển (KR5 WaterSparks): vũng gần đảo, ven bờ
GLINTS = [(300, 1215), (585, 1180), (790, 1305), (255, 1470), (860, 1460), (95, 1255), (500, 1105), (930, 1195), (70, 1110)]


def water_mask(src):
    a = np.asarray(src, dtype=np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mn, mx = a.min(2), a.max(2)
    blue = (b > 170) & (g > 120) & (r < 170) & ((b - r) > 60)
    white = (mn > 200) & (mx - mn < 45)
    land = tach_dao.land_mask(src)
    inner = ndimage.binary_erosion(land, iterations=3)
    allowed = np.zeros(blue.shape, bool)
    for x0, y0, x1, y1 in REGIONS:
        allowed[y0:y1, x0:x1] = True
    for x0, y0, x1, y1 in EXCLUDE:
        allowed[y0:y1, x0:x1] = False
    w = blue & inner & allowed
    w = ndimage.binary_opening(w, iterations=1)
    lab, n = ndimage.label(ndimage.binary_dilation(w, iterations=2))
    sizes = ndimage.sum(w, lab, range(1, n + 1))
    w &= np.isin(lab, np.where(sizes >= 40)[0] + 1)
    # thác: mọi điểm ngả lam hoặc trắng trong ô thác (trừ nét mực, đá xám, rêu)
    fall = np.zeros_like(w)
    for (x0, y0, x1, y1), _, _ in FALLS:
        sub = a[y0:y1, x0:x1]
        sb, sr = sub[..., 2], sub[..., 0]
        smn, smx = sub.min(2), sub.max(2)
        fall[y0:y1, x0:x1] = ((sb > sr + 30) & (sb > 150)) | ((smn > 190) & (smx - smn < 55))
    fall = ndimage.binary_closing(fall, iterations=1) & ~(mx < 90)
    w |= fall
    # vệt trắng (bọt vẽ sẵn) nằm trong lòng sông
    w |= white & allowed & inner & ndimage.binary_dilation(w, iterations=2)
    w = ndimage.binary_closing(w, iterations=1) & allowed & (mx > 90)
    falls = np.zeros(w.shape, np.float32)
    for (x0, y0, x1, y1), _, _ in FALLS:
        falls[y0:y1, x0:x1] = 1
    falls *= w
    return w, falls


def flow_field(w, falls):
    """Hướng chảy: dốc của khoảng cách đi trong lòng nước tính từ đầu nguồn (Dijkstra 8 hướng); thác chảy thẳng xuống."""
    H, W = w.shape
    idx = -np.ones(w.shape, np.int64)
    ys, xs = np.nonzero(w)
    idx[ys, xs] = np.arange(len(xs))
    rows, cols, wts = [], [], []
    for dy, dx, c in [(0, 1, 1.0), (1, 0, 1.0), (1, 1, 1.414), (1, -1, 1.414)]:
        y2, x2 = ys + dy, xs + dx
        ok = (y2 >= 0) & (y2 < H) & (x2 >= 0) & (x2 < W)
        y2, x2, a = y2[ok], x2[ok], idx[ys[ok], xs[ok]]
        bb = idx[y2, x2]
        m = bb >= 0
        rows += [a[m], bb[m]]
        cols += [bb[m], a[m]]
        wts += [np.full(m.sum(), c), np.full(m.sum(), c)]
    g = coo_matrix((np.concatenate(wts), (np.concatenate(rows), np.concatenate(cols))), shape=(len(xs), len(xs))).tocsr()
    lab, n = ndimage.label(w, structure=np.ones((3, 3)))
    srcs = []
    for k in range(1, n + 1):
        cy, cx = np.nonzero(lab == k)
        best = None
        for sx, sy in SOURCES:
            d = np.hypot(cx - sx, cy - sy)
            j = int(np.argmin(d))
            if d[j] < 18:
                best = j
        if best is None:
            best = int(np.argmin(cy))  # điểm cao nhất của cụm
        srcs.append(idx[cy[best], cx[best]])
    dist = dijkstra(g, directed=False, indices=srcs, min_only=True)
    D = np.zeros(w.shape, np.float32)
    D[ys, xs] = np.where(np.isfinite(dist), dist, 0)
    # dốc có trọng số mặt nạ (ngoài nước không kéo lệch)
    m = w.astype(np.float32)
    sig = 2.0
    Ds = ndimage.gaussian_filter(D * m, sig) / np.maximum(ndimage.gaussian_filter(m, sig), 1e-4)
    gy, gx = np.gradient(Ds)
    # thác: thẳng xuống
    gx = np.where(falls > 0, 0, gx)
    gy = np.where(falls > 0, 1, gy)
    nrm = np.hypot(gx, gy) + 1e-6
    gx, gy = gx / nrm, gy / nrm
    # mượt hướng (nối sông – thác không gãy), chuẩn hoá lại
    gx = ndimage.gaussian_filter(gx * m, 1.5) / np.maximum(ndimage.gaussian_filter(m, 1.5), 1e-4)
    gy = ndimage.gaussian_filter(gy * m, 1.5) / np.maximum(ndimage.gaussian_filter(m, 1.5), 1e-4)
    nrm = np.hypot(gx, gy) + 1e-6
    gx, gy = gx / nrm, gy / nrm
    fl = ndimage.gaussian_filter(falls, 1.0)
    return gx * m, gy * m, fl, D


def fill_out(arr, mask):
    """Giá trị ngoài mặt nạ lấy theo điểm trong mặt nạ gần nhất (lấy mẫu lệch không ăn vào bờ)."""
    _, (iy, ix) = ndimage.distance_transform_edt(~mask, return_indices=True)
    return arr[iy, ix]


# ---------- công thức shader (giữ khớp UIFlowWater.shader) ----------
def h21(qx, qy):
    return np.modf(np.sin(qx * 127.1 + qy * 311.7) * 43758.5453)[0] % 1.0


def vnoise(px, py):
    ix, iy = np.floor(px), np.floor(py)
    fx, fy = px - ix, py - iy
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    a, b = h21(ix, iy), h21(ix + 1, iy)
    c, d = h21(ix, iy + 1), h21(ix + 1, iy + 1)
    return (a + (b - a) * fx) + ((c + (d - c) * fx) - (a + (b - a) * fx)) * fy


def sample(img, x, y):
    """Bilinear, kẹp mép. img HxWxC float."""
    H, W = img.shape[:2]
    x = np.clip(x, 0, W - 1.001)
    y = np.clip(y, 0, H - 1.001)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    a, b = img[y0, x0], img[y0, x0 + 1]
    c, d = img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def sstep(a, b, x):
    k = np.clip((x - a) / (b - a), 0, 1)
    return k * k * (3 - 2 * k)


WHITE = np.array([0.985, 1.0, 1.0])
DEEP = np.array([0.15, 0.47, 0.84])


def shade(col, flow, t, scale=2.0):
    """Nét bọt chồng lên nét vẽ nền (nền giữ nguyên). col: HxWx4 (0..1) ảnh phủ (A = mặt nạ nước); flow: HxWx3 trường (R, G = cos, sin
    pha khoảng cách theo dòng; B = thác) đã phóng về cỡ ảnh phủ. Trả HxWx4: màu nét, A = độ phủ. Khớp UIFlowWater.shader."""
    H, W = col.shape[:2]
    py, px = np.mgrid[0:H, 0:W].astype(np.float32)
    ph = np.arctan2(flow[..., 1] * 2 - 1, flow[..., 0] * 2 - 1) / (2 * np.pi)  # pha s / PERIOD, -0,5..0,5
    fall = flow[..., 2]
    mask = col[..., 3]
    # sông (KR5 WavesRiver): vệt bọt nằm ngang dòng trôi xuôi; dải lệch pha theo nhiễu cho cong, đứt khúc, hiện rồi tan theo nhiễu
    k = ph - t * RIVER_SPEED / PERIOD + (vnoise(px * 0.035, py * 0.035) - 0.5) * 0.7
    band = k % 1.0
    stroke = sstep(0.0, 0.06, band) * (1 - sstep(0.13, 0.2, band))
    under = sstep(0.2, 0.24, band) * (1 - sstep(0.24, 0.3, band))
    dash = sstep(0.42, 0.52, vnoise(px * 0.06 + 3.7, py * 0.06 + t * 0.35))
    # sát bờ mỏng dần (không đè nét mực bờ)
    inner = sstep(0.55, 0.95, mask)
    river_w = stroke * dash * inner * (1 - fall)
    river_d = under * dash * inner * (1 - fall) * 0.45
    # thác (KR5 thác: vệt sáng trôi xuống): vệt dọc trắng và lam đậm, trôi nhanh
    sy = py - t * FALL_SPEED * scale
    n1 = vnoise(px * 0.30, sy * 0.05)
    n2 = vnoise(px * 0.24 + 7.3, sy * 0.035 + 3.1)
    fall_w = sstep(0.66, 0.70, n1) * fall * inner
    fall_d = sstep(0.30, 0.26, n2) * fall * inner * 0.6
    a_w = np.maximum(river_w, fall_w)
    a_d = np.maximum(river_d, fall_d) * (1 - a_w)
    a = np.clip(a_w + a_d, 0, 1)
    rgb = (WHITE * a_w[..., None] + DEEP * a_d[..., None]) / np.maximum(a, 1e-4)[..., None]
    return np.concatenate([rgb, (a * mask)[..., None]], axis=2)


# ---------- hình bọt, vòng gợn, lấp lánh (vẽ phẳng, viền lam, không viền mực) ----------
FOAM = (255, 255, 255, 255)
EDGE = (120, 188, 236, 255)   # mép bọt: lam nhạt (KR5: mép là màu đậm hơn của chính nó, không viền mực)
LIGHT = (214, 236, 250, 255)  # đáy múi
RING = (92, 170, 228, 255)    # mép vòng gợn


def draw_puff(rng, size=128):
    """Cụm bọt chân thác: 4–6 múi tròn chồng, ruột trắng, mép lam, một vệt lam nhạt ở đáy múi."""
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    blobs = []
    for i in range(rng.integers(4, 7)):
        r = rng.uniform(0.17, 0.27) * S
        x = S / 2 + rng.uniform(-0.2, 0.2) * S
        y = S * 0.58 + rng.uniform(-0.14, 0.12) * S - (r - 0.2 * S) * 0.6
        blobs.append((x, y, r))
    blobs.sort(key=lambda b: b[1])
    edge = 0.022 * S
    for x, y, r in blobs:
        d.ellipse([x - r - edge, y - r - edge, x + r + edge, y + r + edge], fill=EDGE)
    for x, y, r in blobs:
        d.ellipse([x - r, y - r, x + r, y + r], fill=FOAM)
    for x, y, r in blobs:  # vệt lam nhạt ở đáy múi (phẳng, mép cứng)
        d.chord([x - r * 0.82, y - r * 0.2, x + r * 0.82, y + r * 0.9], 20, 160, fill=LIGHT)
    for x, y, r in blobs[:2]:  # vài giọt bắn
        a = rng.uniform(-2.6, -0.5)
        gx, gy = x + math.cos(a) * r * 1.6, y + math.sin(a) * r * 1.5
        gr = r * 0.16
        d.ellipse([gx - gr - edge * 0.7, gy - gr - edge * 0.7, gx + gr + edge * 0.7, gy + gr + edge * 0.7], fill=EDGE)
        d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=FOAM)
    return trim(im.resize((size, size), Image.LANCZOS))


def draw_ring(size=160):
    """Vòng gợn: elip đứt quãng ba đoạn dày mỏng, trắng viền lam (nhìn nghiêng nên dẹt)."""
    S = size * 4
    im = Image.new("RGBA", (S, S // 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    box = [0.08 * S, 0.08 * S / 2, 0.92 * S, 0.92 * S / 2]
    for a0, a1, wd in [(195, 330, 0.026), (350, 470, 0.02), (490, 520, 0.016)]:
        d.arc(box, a0, a1, fill=RING, width=int(wd * S + 0.016 * S))
    for a0, a1, wd in [(197, 328, 0.026), (352, 468, 0.02), (492, 518, 0.016)]:
        d.arc([box[0] + 0.008 * S, box[1] + 0.008 * S, box[2] - 0.008 * S, box[3] - 0.008 * S], a0, a1, fill=FOAM, width=int(wd * S))
    return trim(im.resize((size, size // 2), Image.LANCZOS))


def draw_glint(rng, size=96):
    """Đốm lấp lánh mặt nước: 3–5 hạt trắng (thoi nhỏ, chấm) viền lam nhạt."""
    S = size * 4
    im = Image.new("RGBA", (S, S // 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(rng.integers(3, 6)):
        x, y = rng.uniform(0.15, 0.85) * S, rng.uniform(0.25, 0.75) * S / 2
        r = rng.uniform(0.035, 0.07) * S * (1.6 if i == 0 else 1)
        pts.append((x, y, r, i == 0))
    for x, y, r, star in pts:
        e = 0.02 * S
        if star:
            poly = [(x, y - r * 1.5), (x + r * 0.45, y), (x, y + r * 1.5), (x - r * 0.45, y)]
            polyw = [(x - r * 1.9, y), (x, y - r * 0.4), (x + r * 1.9, y), (x, y + r * 0.4)]
            for p in (poly, polyw):
                d.polygon(grow(p, x, y, e), fill=(120, 196, 238, 255))
            for p in (poly, polyw):
                d.polygon(p, fill=FOAM)
        else:
            d.ellipse([x - r - e, y - r * 0.6 - e, x + r + e, y + r * 0.6 + e], fill=(120, 196, 238, 255))
            d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=FOAM)
    return trim(im.resize((size, size // 2), Image.LANCZOS))


def grow(poly, cx, cy, e):
    out = []
    for x, y in poly:
        dx, dy = x - cx, y - cy
        l = math.hypot(dx, dy) + 1e-6
        out.append((x + dx / l * e * 1.8, y + dy / l * e * 1.8))
    return out


def trim(im, pad=2):
    bb = im.getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def main():
    xem = "--xem" in sys.argv
    big = Image.open(os.path.join(ART, "world_map.png")).convert("RGB")
    src = big.resize((W1, H1), Image.LANCZOS)
    w, falls = water_mask(src)
    gx, gy, fl, D = flow_field(w, falls)
    print("điểm nước", int(w.sum()))
    hub = json.load(open(os.path.join(ART, "hub_map.json"), encoding="utf-8"))
    os.makedirs(FLOW_DIR, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    bigA = np.asarray(big, dtype=np.float32) / 255
    # mặt nạ nước ở cỡ x2: điểm ảnh lam / trắng / trong thác nằm trong vùng nước x1 (nới 1 px)
    w2 = np.asarray(Image.fromarray((ndimage.binary_dilation(w, iterations=1) * 255).astype(np.uint8)).resize(big.size, Image.NEAREST)) > 0
    a2 = np.asarray(big, dtype=np.int16)
    r2, g2, b2 = a2[..., 0], a2[..., 1], a2[..., 2]
    mn2, mx2 = a2.min(2), a2.max(2)
    waterish = (((b2 > r2 + 30) & (b2 > 140)) | ((mn2 > 190) & (mx2 - mn2 < 55))) & (mx2 > 90)
    w2 &= waterish
    w2 = ndimage.binary_opening(w2, iterations=1)
    flows = []
    for isl in hub["islands"]:
        zone = isl["zone"]
        u0, v0, u1, v1 = isl["rect"]
        X0, Y0, X1, Y1 = round(u0 * W1), round(v0 * H1), round(u1 * W1), round(v1 * H1)
        alpha = np.asarray(Image.open(os.path.join(ART, isl["sprite"] + ".png")).convert("RGBA"))[..., 3]
        own = np.zeros(w2.shape, bool)
        hh, ww = alpha.shape
        own[Y0 * 2:Y0 * 2 + hh, X0 * 2:X0 * 2 + ww] = alpha > 200
        mine = w2 & own
        if mine.sum() < 200:
            continue
        ys, xs = np.nonzero(mine)
        pad = 8
        bx0, by0 = max(0, (xs.min() - pad) // 4 * 4), max(0, (ys.min() - pad) // 4 * 4)
        bx1, by1 = min(big.width, (xs.max() + pad + 4) // 4 * 4), min(big.height, (ys.max() + pad + 4) // 4 * 4)
        m = mine[by0:by1, bx0:bx1]
        rgb = bigA[by0:by1, bx0:bx1]
        rgb_f = fill_out(rgb, m)
        am = ndimage.gaussian_filter(m.astype(np.float32), 0.6)
        am = np.clip((am - 0.25) / 0.5, 0, 1)
        col = np.concatenate([rgb_f, am[..., None]], axis=2)
        Image.fromarray((col * 255 + 0.5).astype(np.uint8), "RGBA").save(os.path.join(ART, f"sanh_nuoc_{zone}.png"), optimize=True)
        # trường dòng chảy cỡ ảnh nới (1/2 ảnh phủ): R, G = cos, sin pha khoảng cách đi theo lòng nước (s / PERIOD; mã hoá góc để lấy mẫu
        # bilinear không gãy ở chỗ pha quay vòng), B = thác. Ngoài nước lấy giá trị điểm nước gần nhất
        fx0, fy0, fx1, fy1 = bx0 // 2, by0 // 2, bx1 // 2, by1 // 2
        wm = w[fy0:fy1, fx0:fx1]
        fD, ffl = D[fy0:fy1, fx0:fx1], fl[fy0:fy1, fx0:fx1]
        if wm.any():
            fD, ffl = fill_out(fD, wm), fill_out(ffl, wm)
        ang = 2 * np.pi * fD / PERIOD
        enc = np.stack([np.cos(ang) * 0.5 + 0.5, np.sin(ang) * 0.5 + 0.5, np.clip(ffl, 0, 1)], axis=2)
        flow_img = Image.fromarray((enc * 255 + 0.5).astype(np.uint8), "RGB")
        flow_img.save(os.path.join(FLOW_DIR, f"sanh_nuoc_{zone}_hc.png"))
        rect = [round(bx0 / big.width, 5), round(by0 / big.height, 5), round(bx1 / big.width, 5), round(by1 / big.height, 5)]
        flows.append({"zone": zone, "sprite": f"sanh_nuoc_{zone}", "flow": f"sanh_nuoc_{zone}_hc", "rect": rect,
                      "box": [round(u0, 5), round(v0, 5), round(u1, 5), round(v1, 5)]})
        print("đảo", zone, "ảnh phủ", (bx1 - bx0, by1 - by0), "điểm nước", int(m.sum()))
        if xem:
            preview(zone, big, (bx0, by0, bx1, by1), col, np.asarray(flow_img.resize((bx1 - bx0, by1 - by0), Image.BILINEAR), np.float32) / 255)
    # hình bọt, vòng gợn, lấp lánh
    rng = np.random.default_rng(11)
    for i in range(1, 4):
        draw_puff(rng).save(os.path.join(ANIM_DIR, f"anim_bot_{i}.png"))
    draw_ring().save(os.path.join(ANIM_DIR, "anim_vong.png"))
    for i in range(1, 4):
        draw_glint(rng).save(os.path.join(ANIM_DIR, f"anim_lap_{i}.png"))
    patch_anim(flows)


def patch_anim(flows):
    """Ghi vào khoá world_map của island_anim.json: flows + bọt / vòng gợn chân thác + lấp lánh; bỏ "foam" (bọt hình dán cũ ở chân thác)."""
    path = os.path.join(ART, "island_anim.json")
    raw = open(path, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    anim = json.loads(raw.decode("utf-8"))
    entry = anim.setdefault("world_map", {"items": [], "rivers": [], "lights": []})
    apply(entry, flows)
    trung_sanh.apply(entry)  # easter egg sảnh (trung_sanh/trung_sanh.py)
    open(path, "w", encoding="utf-8", newline=nl).write(json.dumps(anim, ensure_ascii=False, indent=1))
    print("đã ghi khoá world_map:", len(flows), "ảnh phủ,", len(entry["items"]), "món")


OWN = {"splash", "rings", "glint", "foam"}


def apply(entry, flows=None):
    """build_sanh.py gọi lại sau khi ghi khoá world_map (giữ phần nước động khi dựng lại bản đồ)."""
    if flows is None:
        flows = entry.get("flows", [])
    entry["flows"] = flows
    items = [it for it in entry.get("items", []) if it.get("k") not in OWN]
    P = lambda x, y: (round(x / W1, 4), round(y / H1, 4))
    for (x0, y0, x1, y1), (bx, by), k in FALLS:
        u, v = P(bx, by)
        wdt = (x1 - x0) * k
        items.append({"k": "splash", "x": u, "y": v, "s": round(wdt * 0.5 / W1, 4)})
        items.append({"k": "rings", "x": u, "y": round(v + 3 / H1, 4), "s": round(wdt * 1.15 / W1, 4)})
    for x, y in GLINTS:
        u, v = P(x, y)
        items.append({"k": "glint", "x": u, "y": v, "s": round(26 / W1, 4)})
    entry["items"] = items


def preview(zone, big, box, col, flow):
    bx0, by0, bx1, by1 = box
    base = np.asarray(big.crop(box), np.float32) / 255
    frames = []
    for f in range(30):
        t = f / 15
        o = shade(col, flow, t)
        a = o[..., 3:4]
        img = base * (1 - a) + o[..., :3] * a
        frames.append(Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)))
    frames[0].save(os.path.join(PREVIEW, f"xem_{zone}.gif"), save_all=True, append_images=frames[1:], duration=66, loop=0)
    # ảnh soi pha dòng chảy (dải màu theo pha: dải phải nằm ngang dòng)
    ph = np.arctan2(flow[..., 1] * 2 - 1, flow[..., 0] * 2 - 1) / (2 * np.pi) % 1.0
    hue = np.stack([ph, 1 - ph, np.full_like(ph, 0.4)], 2)
    vis =base * (1 - (col[..., 3:4] > 0.5) * 0.7) + np.where(flow[..., 2:3] > 0.5, np.array([1.0, 0, 1.0]), hue) * (col[..., 3:4] > 0.5) * 0.7
    Image.fromarray((np.clip(vis, 0, 1) * 255).astype(np.uint8)).save(os.path.join(PREVIEW, f"pha_{zone}.jpg"), quality=88)


if __name__ == "__main__":
    main()
