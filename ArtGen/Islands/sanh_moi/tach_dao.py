# Tách từng đảo của bản đồ sảnh (người dùng 2026-11-19: "tách từng đảo 1 ra rồi xếp chúng lại là được"; "khi drag ra rìa vẫn phải thấy
# mây và nước"; "sao mây che luôn cả các đảo"). build_sanh.py gọi:
#   land_mask(img)          : đất (đảo + vật nhỏ trên biển: thuyền, đá, san hô), bỏ nét mảnh (nét mực vành mây cũ), lấp lỗ (sông trong đảo)
#   cut_islands(img, ...)   : mỗi đảo (theo vùng hệ, điểm đất gán cho vùng gần nhất) một ảnh trong suốt: giữ viền bọt ven bờ, mép bờ mềm
#                             dần vào biển; mép cắt giữa hai đảo cứng và chồng 2 px (xếp lại không lộ khe); kèm ánh sáng trên đảo (ảnh
#                             trắng, toả từ mốc giữa đảo; game cộng sáng màu hệ, thở nhẹ: người dùng "glowing ... để biết có thể click")
#   sea_tile()              : biển lát 1024 x 1024 (mặt biển chuyến tàu x 2 + nét sóng, nối liền bốn phía)
#   ring_clouds(land, ...)  : mây vành chỉ trên biển, cách bờ, dày dần ra xa, có cả ngoài mép ảnh
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

COAST = 12  # px tranh gốc giữ thêm quanh bờ (bọt sóng, nước ven bờ)
FEATHER = 5  # px mép bờ mềm


def land_mask(img):
    a = np.asarray(img.convert("RGB"), dtype=np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    sea = (b > 185) & (g > 140) & (r < 150) & ((b - r) > 80)
    land = ~sea
    core = ndimage.binary_opening(land, iterations=3)
    lab, n = ndimage.label(core)
    sizes = ndimage.sum(core, lab, range(1, n + 1))
    core = np.isin(lab, np.where(sizes >= 600)[0] + 1)
    core = ndimage.binary_fill_holes(core)
    final = core | (land & ndimage.binary_dilation(core, iterations=4))
    return ndimage.binary_fill_holes(final)


def poly_mask(poly, shape):
    m = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(m) > 0


def cut_islands(img, land, realms, scale=2, pad=24):
    """realms: [(zone, at, poly)] toạ độ ảnh. Trả [(zone, ảnh RGBA đã phóng, (x0, y0, x1, y1) toạ độ ảnh)]."""
    H, W = land.shape
    # vùng gần nhất cho từng điểm đất (khoảng cách tới đa giác vùng)
    dists = []
    for zone, at, poly in realms:
        pm = poly_mask(poly, land.shape)
        dists.append(ndimage.distance_transform_edt(~pm))
    owner = np.argmin(np.stack(dists), axis=0)
    coast = ndimage.binary_dilation(land, iterations=COAST)
    # mép bờ mềm: alpha theo khoảng cách ra ngoài vùng giữ
    dout = ndimage.distance_transform_edt(~coast)
    din = ndimage.distance_transform_edt(coast)
    soft = np.clip(0.5 + (din - dout) / (2 * FEATHER), 0, 1)
    soft[din > FEATHER] = 1
    src = img.convert("RGB")
    big = src.resize((W * scale, H * scale), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))
    out = []
    for k, (zone, at, poly) in enumerate(realms):
        mine = owner == k
        # vùng cắt cứng giữa hai đảo: nới 2 px sang đảo bên cạnh để xếp lại không lộ khe
        mine_ext = ndimage.binary_dilation(mine, iterations=2)
        alpha = np.where(mine_ext & (din > 0), soft, 0).astype(np.float32)
        # chỉ giữ phần thuộc đảo này: đất của mình + nước ven bờ của mình
        if alpha.max() <= 0:
            continue
        ys, xs = np.nonzero(alpha > 0.01)
        x0, x1 = max(0, xs.min() - pad), min(W, xs.max() + pad)
        y0, y1 = max(0, ys.min() - pad), min(H, ys.max() + pad)
        a_img = Image.fromarray((alpha[y0:y1, x0:x1] * 255).astype(np.uint8), "L")
        a_img = a_img.resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.BILINEAR)
        crop = big.crop((x0 * scale, y0 * scale, x1 * scale, y1 * scale)).convert("RGBA")
        crop.putalpha(a_img)
        # ánh sáng trên đảo (người dùng: "glowing tính từ giữa đảo thôi, không làm viền, làm đảo sáng"): đất của đảo nhân vệt sáng toả
        # từ mốc giữa đảo, mờ dần ra mép; game vẽ trên ảnh đảo bằng material cộng sáng, nhuộm màu hệ, thở nhẹ
        own = (mine & land).astype(np.float32)
        own = ndimage.gaussian_filter(own, sigma=2)
        yy, xx = np.mgrid[0:H, 0:W]
        R = 0.62 * max(x1 - x0, y1 - y0)
        dist = np.hypot(xx - at[0], yy - at[1]) / R
        rad = np.clip(1 - dist, 0, 1) ** 1.4
        g = own * rad
        g = g / max(1e-6, g.max())
        gx0, gy0, gx1, gy1 = x0, y0, x1, y1
        ga = (g[gy0:gy1, gx0:gx1] * 255).astype(np.uint8)
        glow = Image.new("RGBA", (gx1 - gx0, gy1 - gy0), (255, 255, 255, 0))
        glow.putalpha(Image.fromarray(ga, "L"))
        out.append((zone, crop, (x0, y0, x1, y1), glow, (gx0, gy0, gx1, gy1)))
    return out


def sea_tile(ship_dir, size=1024, seed=31):
    """Mặt biển lát của chuyến tàu (512) ghép 2 x 2, rải nét sóng trắng nối liền bốn phía (đơn vị UI = px)."""
    tile = Image.open(os.path.join(ship_dir, "tau_bien.png")).convert("RGBA")
    out = Image.new("RGBA", (size, size))
    for x in range(0, size, tile.width):
        for y in range(0, size, tile.height):
            out.paste(tile, (x, y))
    waves = []
    for i in range(1, 5):
        f = os.path.join(ship_dir, f"tau_song_{i}.png")
        if os.path.exists(f):
            waves.append(Image.open(f).convert("RGBA"))
    rng = np.random.default_rng(seed)
    for _ in range(22):
        w = waves[rng.integers(len(waves))]
        if rng.random() < 0.5:
            w = w.transpose(Image.FLIP_LEFT_RIGHT)
        x, y = int(rng.integers(size)), int(rng.integers(size))
        for ox in (-size, 0, size):
            for oy in (-size, 0, size):
                out.paste(w, (x + ox - w.width // 2, y + oy - w.height // 2), w)
    return out.convert("RGB")


def ring_clouds(land, avoid, margin=440, seed=57, near=105, step=(104, 64)):
    """Mây trên biển: cách đất (kể cả vật nhỏ) >= near px, càng xa càng dày; lưới phủ cả lề ngoài ảnh (margin)."""
    H, W = land.shape
    big = np.zeros((H + 2 * margin, W + 2 * margin), bool)
    big[margin:margin + H, margin:margin + W] = land
    d = ndimage.distance_transform_edt(~big)
    rng = np.random.default_rng(seed)
    out = []
    row = 0
    for y in range(-margin, H + margin, step[1]):
        off = (row % 2) * step[0] / 2
        row += 1
        for x in range(-margin, W + margin, step[0]):
            jx, jy = x + off + rng.uniform(-16, 16), y + rng.uniform(-10, 10)
            ix = int(np.clip(jx + margin, 0, W + 2 * margin - 1))
            iy = int(np.clip(jy + margin, 0, H + 2 * margin - 1))
            dd = d[iy, ix]
            if dd < near:
                continue
            p = np.clip((dd - near) / 120, 0.5, 1)  # rìa dày mây (người dùng: "làm thêm mây ở rìa")
            if rng.random() > p:
                continue
            if any(x0 - 60 < jx < x1 + 60 and y0 - 40 < jy < y1 + 60 for x0, y0, x1, y1 in avoid):
                continue
            out.append((jx, jy, rng.uniform(230, 300), int(rng.random() < 0.5)))
    out.sort(key=lambda c: c[1])
    return out


# chi tiết chính của từng đảo phát sáng (người dùng 2026-11-19: "chọn 1 chi tiết chính của đảo làm sáng lên, ví dụ đảo mộc là cái cây,
# đảo kim là ông mặt trời, đảo hỏa là miệng núi lửa, đảo thổ là đền mặt trời"; không làm sáng loang cả đảo vì "màu nó mờ đi").
# Vùng (toạ độ tranh gốc 1024 x 1536) + bộ lọc màu ra đúng hình chi tiết; quầng sáng chỉ ở vòng ngoài hình (bên trong trống: chi tiết giữ
# nguyên màu, nét), game cộng sáng màu hệ, thở nhẹ.
LANDMARKS = {
    "moc": ("box", (95, 545, 395, 770), "wood"),     # thân, rễ cây thần (cam nâu, xoáy)
    "kim": ("circle", (790, 150, 60), "gold"),       # ông mặt trời trên tháp chuông
    "hoa": ("ellipse", (380, 97, 108, 50), "lava"),  # hồ dung nham trong miệng núi lửa
    "tho": ("box", (690, 462, 868, 578), "gold"),    # mặt trời vàng, mái đền
    "thuy": ("box", (445, 1030, 578, 1172), "stone"),  # cổng rồng đá trắng
}


def landmark_glow(img, zone, top, scale=2, pad=34):
    """Ảnh quầng sáng quanh chi tiết chính của đảo (trắng, alpha), khung (x0, y0, x1, y1) theo toạ độ ảnh nới (cộng top)."""
    if zone not in LANDMARKS:
        return None, None
    kind, prm, filt = LANDMARKS[zone]
    a = np.asarray(img.convert("RGB"), dtype=np.int16)
    H, W = a.shape[:2]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    yy, xx = np.mgrid[0:H, 0:W]
    if kind == "box":
        x0, y0, x1, y1 = prm
        region = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
    elif kind == "circle":
        cx, cy, rr = prm
        region = np.hypot(xx - cx, yy - cy) < rr
    else:
        cx, cy, rx, ry = prm
        region = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 < 1
    mx, mn = a.max(2), a.min(2)
    if filt == "gold":
        f = (r > 195) & (g > 140) & (b < 120) & (r - b > 90)
    elif filt == "lava":
        f = (r > 200) & (g > 80) & (b < 100) & (r - b > 110)
    elif filt == "wood":
        f = (r > 170) & (g > 80) & (g < 185) & (b < 120) & (r - g > 40)
    else:  # stone: đá trắng, xám nhạt
        f = (mn > 175) & (mx - mn < 40)
    m = region & f
    m = ndimage.binary_closing(m, iterations=2)
    lab, n = ndimage.label(m)
    if n == 0:
        return None, None
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    m = np.isin(lab, np.where(sizes >= max(30, sizes.max() * 0.04))[0] + 1)
    m = ndimage.binary_fill_holes(m)
    ys, xs = np.nonzero(m)
    x0, x1 = max(0, xs.min() - pad), min(W, xs.max() + pad)
    y0, y1 = max(0, ys.min() - pad), min(H, ys.max() + pad)
    sub = m[y0:y1, x0:x1].astype(np.float32)
    halo = ndimage.gaussian_filter(ndimage.binary_dilation(sub > 0, iterations=3).astype(np.float32), sigma=7)
    halo = np.clip(halo / max(1e-6, halo.max()) * 1.7, 0, 1)
    inner = ndimage.gaussian_filter(sub, sigma=1.2)
    ring = np.clip(halo - inner * 1.05, 0, 1)
    al = Image.fromarray((ring * 255).astype(np.uint8), "L").resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.BILINEAR)
    out = Image.new("RGBA", al.size, (255, 255, 255, 0))
    out.putalpha(al)
    return out, (x0, y0 + top, x1, y1 + top)
