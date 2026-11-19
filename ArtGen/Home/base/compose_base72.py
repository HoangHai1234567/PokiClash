# Ghép ảnh nền đảo Nhà 72 x 72 ô (người dùng dặn 2026-11-19: đảo to ra cho quái đi khắp nơi, máy không cần thấy hết đảo)
# từ mảnh của nền 48 x 48 cũ (home_base_48.png). Cùng mật độ px mỗi ô (30,4 px một ô theo bề ngang) nên nét giữ nguyên độ nét:
# - cỏ, rừng nền, biển: ghép vá (quilting) từ vùng sạch của nền cũ, mép mềm;
# - bờ cát hai cạnh dưới: lấy dải bờ cũ, lặp dọc cạnh mới, nối bằng đường cắt ít lệch nhất (min-cut);
# - cụm vách + thác + hồ (ô rừng (0,0), (0,1), (1,0)) và vách phải (5,0): phóng 1,5 cho vừa ô rừng 12 x 12;
# - suối: dải suối cũ lặp dọc trục gy (mở rộng dần lên 1,5 lần ở chỗ đổ ra từ hồ), cửa suối giữ nguyên;
# - hồ ven biển, bến: giữ cỡ; mạch quặng phóng 1,25 cho vừa Mỏ 6 x 6.
# Ra: Assets/03 Art/Home/home_base.png, khối home_base của home_art.json; in features cho balance.json (toạ độ đo trên mặt nạ đã ghép);
# ảnh soi lưới ArtGen/Home/base/preview_72_luoi.png.
# Chạy: py -3 -I compose_base72.py
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(HERE, "home_base_48.png")
OUT_PNG = os.path.join(ROOT, "Assets", "03 Art", "Home", "home_base.png")
META = os.path.join(ROOT, "Assets", "03 Art", "Home", "home_art.json")

src = np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32)
SH, SW = src.shape[:2]
C = 1460 / 48  # px ảnh mỗi ô theo bề ngang
oTX, oTY, OG = 723.44, -30.0, 48
G = 72
nTX, nTY = 1105.0, 60.0
W, H = 2210, 1330  # biển dưới mũi đảo đủ chỗ cho tàu cập bến (2026-11-19)
rng = np.random.default_rng(20261119)


def oP(gx, gy): return np.array([oTX + (gx - gy) * C / 2, oTY + (gx + gy) * C / 4])


def nP(gx, gy): return np.array([nTX + (gx - gy) * C / 2, nTY + (gx + gy) * C / 4])


def cell_of(x, y, TX, TY):
    u = (x - TX) / (C / 2)
    v = (y - TY) / (C / 4)
    return (u + v) / 2, (v - u) / 2


def sample(img, xs, ys):
    out = np.zeros(xs.shape + (img.shape[2],), np.float32)
    for c in range(img.shape[2]):
        out[..., c] = ndi.map_coordinates(img[..., c], [ys, xs], order=1, mode="nearest")
    return out


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


# ---------- vùng của ảnh cũ ----------
oy, ox = np.mgrid[0:SH, 0:SW].astype(np.float32)
ogx, ogy = cell_of(ox + 0.5, oy + 0.5, oTX, oTY)
R, Gc, B = src[..., 0], src[..., 1], src[..., 2]
grassy = (Gc > 196) & (Gc - B > 80) & (R > 135)
# vật lạ trên đồng cỏ (vách, hồ, suối, quặng, bến, bờ): khối không phải cỏ lớn hơn búi cỏ
lab, n = ndi.label(~grassy)
sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
big = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 400])
o_inside = (ogx > 2) & (ogy > 2) & (ogx < OG - 2) & (ogy < OG - 2)
clean_grass = o_inside & ~ndi.binary_dilation(big, iterations=14)
# biển xa bờ: dưới hai cạnh dưới hơn 55 px, xa bến
def below_edges(x, y, TX, TY, g):
    L, Bt, Rt = (TX - g * C / 2, TY + g * C / 4), (TX, TY + g * C / 2), (TX + g * C / 2, TY + g * C / 4)
    yl = L[1] + (x - L[0]) * 0.5
    yr = Rt[1] - (x - Rt[0]) * 0.5
    return np.where(x < Bt[0], y - yl, y - yr)
clean_sea = (below_edges(ox, oy, oTX, oTY, OG) > 55) & ~((ox > 620) & (ox < 830))
seaish = (B > 160) & (B - R > 40) | ((R > 215) & (Gc > 215) & (B > 215))
clean_sea &= ndi.binary_erosion(seaish | ndi.binary_closing(seaish, iterations=3), iterations=2) | (below_edges(ox, oy, oTX, oTY, OG) > 80)
clean_forest = ((ogx < -1.5) | (ogy < -1.5)) & (oy < oTY + OG * C / 4 - 25) & ~((ox > 470) & (ox < 1000) & (oy < 260))


# ---------- vùng của ảnh mới ----------
ny, nx = np.mgrid[0:H, 0:W].astype(np.float32)
ngx, ngy = cell_of(nx + 0.5, ny + 0.5, nTX, nTY)
inside = (ngx >= 0) & (ngy >= 0) & (ngx <= G) & (ngy <= G)
vy = nTY + G * C / 4
outer_top = ((ngx < 0) | (ngy < 0)) & ~((ngx > G) | (ngy > G))
corner = ((ngx < 0) & (ngy > G)) | ((ngy < 0) & (ngx > G))
forest = ~inside & (outer_top | (corner & (ny < vy)))
sea = ~inside & ~forest


# ---------- ghép vá ----------
def window(h, w, f):
    def ramp(k):
        t = np.ones(k, np.float32)
        m = max(1, int(k * f))
        r = smooth(np.linspace(0, 1, m + 2)[1:-1])
        t[:m] = r
        t[-m:] = r[::-1]
        return t
    return np.outer(ramp(h), ramp(w))


def corners_inside(mask, ph, pw):
    ii = np.pad(mask.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    s = ii[ph:, pw:] - ii[:-ph, pw:] - ii[ph:, :-pw] + ii[:-ph, :-pw]
    return np.nonzero(s == ph * pw)


def quilt(target, smask, ph, pw, seed, feather=0.3):
    r = np.random.default_rng(seed)
    ys, xs = corners_inside(smask, ph, pw)
    assert len(ys) > 0, "không có chỗ lấy mẫu"
    layer = np.zeros((H, W, 3), np.float32)
    tys, txs = np.nonzero(target)
    y0, y1, x0, x1 = tys.min() - ph, tys.max() + 1, txs.min() - pw, txs.max() + 1
    # lượt 1: lát kín không mép mềm; lượt 2: vá ngẫu nhiên mép mềm, thứ tự ngẫu nhiên
    for pas, (step_y, step_x, win) in enumerate([(ph, pw, np.ones((ph, pw), np.float32)), (int(ph * 0.42), int(pw * 0.42), window(ph, pw, feather))]):
        spots = [(y, x) for y in range(y0, y1, step_y) for x in range(x0, x1, step_x)]
        if pas == 1:
            spots = [(y + int(r.integers(-step_y // 3, step_y // 3 + 1)), x + int(r.integers(-step_x // 3, step_x // 3 + 1))) for y, x in spots]
            r.shuffle(spots)
        for y, x in spots:
            ya, yb, xa, xb = max(0, y), min(H, y + ph), max(0, x), min(W, x + pw)
            if ya >= yb or xa >= xb or not target[ya:yb, xa:xb].any():
                continue
            k = int(r.integers(len(ys)))
            patch = src[ys[k]:ys[k] + ph, xs[k]:xs[k] + pw][ya - y:yb - y, xa - x:xb - x]
            w = win[ya - y:yb - y, xa - x:xb - x, None]
            layer[ya:yb, xa:xb] = layer[ya:yb, xa:xb] * (1 - w) + patch * w
    return layer


grow = lambda m, k: ndi.binary_dilation(m, iterations=k)
L_grass = quilt(grow(inside, 10), clean_grass, 96, 150, 1)
L_forest = quilt(grow(forest, 10), clean_forest, 84, 120, 2, 0.25)
L_sea = quilt(grow(sea, 10), clean_sea, 90, 150, 3)
soft = lambda m: ndi.gaussian_filter(m.astype(np.float32), 2.2)[..., None]
wg, wf, ws = soft(inside), soft(forest), soft(sea)
out = (L_grass * wg + L_forest * wf + L_sea * ws) / np.maximum(wg + wf + ws, 1e-4)


# ---------- dải bờ cát ----------
def fit_beach(xa, xb, left):
    # mép trên bãi cát (ngay dưới nét mực) theo cột, khớp đường thẳng bỏ điểm lệch
    xs, ys = [], []
    for x in range(xa, xb):
        L, Bt, Rt = oP(0, OG), oP(OG, OG), oP(OG, 0)
        y0 = (L[1] + (x - L[0]) * 0.5) if left else (Rt[1] - (x - Rt[0]) * 0.5)
        col = src[int(y0) - 25:int(y0) + 25, x]
        sand = (col[:, 0] > 200) & (col[:, 1] > 160) & (col[:, 1] < col[:, 0]) & (col[:, 2] < 185) & (col[:, 0] - col[:, 2] > 55)  # cát: đỏ hơn lục (cỏ sáng thì lục hơn)
        idx = np.nonzero(sand)[0]
        if len(idx):
            xs.append(x)
            ys.append(int(y0) - 25 + idx[0])
    xs, ys = np.array(xs, float), np.array(ys, float)
    p = np.polyfit(xs, ys, 1)
    for _ in range(3):
        res = ys - np.polyval(p, xs)
        keep = np.abs(res - np.median(res)) < 4
        p = np.polyfit(xs[keep], ys[keep], 1)
    # độ trôi chậm của mép cát quanh đường thẳng (bờ vẽ tay không thẳng): trung vị trượt 41 px, nội suy cho mọi cột
    res = ys - np.polyval(p, xs)
    keep = np.abs(res - np.median(res)) < 6
    drift = ndi.median_filter(res[keep], size=41, mode="nearest")
    allx = np.arange(xa, xb, dtype=float)
    return p, np.interp(allx, xs[keep], drift)


def mincut_mask(A, Bm):
    e = ((A - Bm) ** 2).sum(2)
    h, o = e.shape
    cost = e.copy()
    for i in range(1, h):
        prev = cost[i - 1]
        cost[i] += np.minimum(np.minimum(np.r_[np.inf, prev[:-1]], prev), np.r_[prev[1:], np.inf])
    path = np.zeros(h, int)
    path[-1] = int(cost[-1].argmin())
    for i in range(h - 2, -1, -1):
        j = path[i + 1]
        lo, hi = max(0, j - 1), min(o, j + 2)
        path[i] = lo + int(cost[i, lo:hi].argmin())
    m = (np.arange(o)[None, :] >= path[:, None]).astype(np.float32)
    return ndi.uniform_filter1d(m, 5, axis=1)


def tile_strip(strip, length, overlap, seed):
    # nối nhiều bản dải (cao h, dài L) cho đủ length, mỗi bản bắt đầu ở chỗ ngẫu nhiên
    r = np.random.default_rng(seed)
    h, L, _ = strip.shape
    out_s = strip[:, :min(L, length)].copy()
    while out_s.shape[1] < length:
        # chọn chỗ bắt đầu của bản sau sao cho đoạn chồng khớp nhất (lệch bình phương nhỏ nhất), rồi mới cắt min-cut
        tail = out_s[:, -overlap:]
        best, boff = None, 0
        for off in range(0, max(1, L - overlap - L // 3), 3):
            e = float(((strip[:, off:off + overlap] - tail) ** 2).mean())
            e *= 1 + 0.15 * r.random()
            if best is None or e < best:
                best, boff = e, off
        nxt = strip[:, boff:]
        m = mincut_mask(out_s[:, -overlap:], nxt[:, :overlap])[..., None]
        joined = out_s[:, -overlap:] * (1 - m) + nxt[:, :overlap] * m
        out_s = np.concatenate([out_s[:, :-overlap], joined, nxt[:, overlap:]], 1)
    return out_s[:, :length]


V0, V1 = 16, 78
for left in (True, False):
    xa, xb = (250, 640) if left else (790, 1110)
    p, drift = fit_beach(xa, xb, left)
    # dải cũ theo (v, x): v là độ lệch dọc so với mép cát (đã nắn thẳng độ trôi để các bản nối không lệch bậc)
    vs = np.arange(-V0, V1 + 1, dtype=np.float32)
    xs = np.arange(xa, xb, dtype=np.float32)
    XX, VV = np.meshgrid(xs, vs)
    strip = sample(src, XX, np.polyval(p, XX) + drift[None, :].astype(np.float32) + VV)
    # độ lệch mép cát so với cạnh lưới cũ, giữ y nguyên ở cạnh mới
    L0, B0, R0 = oP(0, OG), oP(OG, OG), oP(OG, 0)
    mid = (xa + xb) / 2
    theo = (L0[1] + (mid - L0[0]) * 0.5) if left else (R0[1] - (mid - R0[0]) * 0.5)
    d0 = np.polyval(p, mid) + float(np.mean(drift)) - theo
    Ln, Bn, Rn = nP(0, G), nP(G, G), nP(G, 0)
    tx0, tx1 = (int(Ln[0]) - 40, int(Bn[0]) + 30) if left else (int(Bn[0]) - 30, int(Rn[0]) + 40)
    tx0, tx1 = max(0, tx0), min(W, tx1)
    tstrip = tile_strip(strip, tx1 - tx0, 70, 11 if left else 12)
    line = (lambda x: Ln[1] + (x - Ln[0]) * 0.5 + d0) if left else (lambda x: Rn[1] - (x - Rn[0]) * 0.5 + d0)
    cols = np.arange(tx0, tx1)
    ytop = line(cols) - V0
    for i, x in enumerate(cols):
        y_a, y_b = int(np.floor(ytop[i])), int(np.ceil(ytop[i] + V0 + V1))
        y_a, y_b = max(0, y_a), min(H, y_b)
        if y_a >= y_b:
            continue
        yy = np.arange(y_a, y_b, dtype=np.float32)
        v = yy - line(x)
        cs = sample(tstrip, np.full_like(yy, i), v + V0)
        a = smooth((v + V0) / 7) * (1 - smooth((v - (V1 - 26)) / 26))
        # qua mũi dưới thì thôi (không cho cát cạnh này chìa sang cạnh kia), mờ trong 8 px
        a = a * (smooth((Bn[0] + 6 - x) / 8) if left else smooth((x - (Bn[0] - 6)) / 8))
        out[y_a:y_b, x] = out[y_a:y_b, x] * (1 - a[:, None]) + cs * a[:, None]
    if left:
        beach_left = (p, d0)
    else:
        beach_right = (p, d0)


# ---------- dán mảnh ----------
def poly_mask(points, shape=(SH, SW)):
    im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in points], fill=255)
    return np.asarray(im).astype(np.float32) / 255


def blob_mask(x0, y0, x1, y1, grow_px=3):
    sub = ~grassy[y0:y1, x0:x1]
    lb, k = ndi.label(sub)
    if k == 0:
        return np.zeros((SH, SW), np.float32)
    sz = ndi.sum(np.ones_like(lb), lb, range(1, k + 1))
    m = ndi.binary_fill_holes(lb == (int(np.argmax(sz)) + 1))
    m = ndi.binary_dilation(m, iterations=grow_px)
    full = np.zeros((SH, SW), np.float32)
    full[y0:y1, x0:x1] = m
    return full


def rect_mask(x0, y0, x1, y1, f=10):
    m = np.zeros((SH, SW), np.float32)
    yy = np.arange(SH)[:, None]
    xx = np.arange(SW)[None, :]
    ax = smooth((xx - x0) / f) * smooth((x1 - xx) / f)
    ay = smooth((yy - y0) / f) * smooth((y1 - yy) / f)
    return (ax * ay).astype(np.float32)


placed = {}  # tên → mặt nạ trên ảnh mới (để đo ô)


def paste(name, mask_old, a_old, a_new, k, feather=1.2):
    # điểm p mới ↔ (p - a_new) / k + a_old
    if feather > 0:
        mask_old = ndi.gaussian_filter(mask_old, feather)
    ys, xs = np.nonzero(mask_old > 0.01)
    bx0, bx1, by0, by1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    nx0 = int(np.floor((bx0 - a_old[0]) * k + a_new[0])) - 2
    nx1 = int(np.ceil((bx1 - a_old[0]) * k + a_new[0])) + 2
    ny0 = int(np.floor((by0 - a_old[1]) * k + a_new[1])) - 2
    ny1 = int(np.ceil((by1 - a_old[1]) * k + a_new[1])) + 2
    nx0, ny0, nx1, ny1 = max(0, nx0), max(0, ny0), min(W, nx1), min(H, ny1)
    gy_, gx_ = np.mgrid[ny0:ny1, nx0:nx1].astype(np.float32)
    sx = (gx_ - a_new[0]) / k + a_old[0]
    sy = (gy_ - a_new[1]) / k + a_old[1]
    col = sample(src, sx, sy)
    m = ndi.map_coordinates(mask_old, [sy, sx], order=1, mode="constant")[..., None]
    out[ny0:ny1, nx0:nx1] = out[ny0:ny1, nx0:nx1] * (1 - m) + col * m
    full = np.zeros((H, W), np.float32)
    full[ny0:ny1, nx0:nx1] = m[..., 0]
    placed[name] = full


# suối cũ: đường tâm theo cột
def fit_stream():
    xs, ys, ws = [], [], []
    for x in range(290, 620):
        y_exp = 445 + (x - 215) * (-217 / 475)
        y0 = int(y_exp) - 30
        col = src[y0:y0 + 60, x]
        water = ((col[:, 2] > 160) & (col[:, 2] - col[:, 0] > 40)) | ((col[:, 0] > 215) & (col[:, 1] > 215) & (col[:, 2] > 215))
        idx = np.nonzero(water)[0]
        if len(idx) < 4:
            continue
        xs.append(x)
        ys.append(y0 + (idx[0] + idx[-1]) / 2)
        ws.append(idx[-1] - idx[0] + 1)
    p = np.polyfit(xs, ys, 1)
    return p, float(np.median(ws))


sp, swid = fit_stream()
hw = swid / 2 + 5  # nửa bề dày dọc kể cả nét mực bờ

# cụm vách + thác + hồ: phóng 1,5, góc trước-dưới của vách trái ↔ góc dưới ô rừng (0,1)
CLIFF = [(487, 141), (597, 87), (629, 101), (629, 76), (740, 31), (845, 76), (845, 100), (866, 90), (978, 139), (978, 182), (868, 235),
         (806, 236), (800, 244), (738, 248), (690, 240), (664, 232), (598, 233), (487, 183)]
A_cl, N_cl, K_cl = np.array([597.5, 231.0]), nP(12, 24), 1.5
T_cl = lambda p: (np.asarray(p, float) - A_cl) * K_cl + N_cl

# suối mới: theo trục gy (dốc -0,5) từ dưới hồ tới cạnh dưới trái; chỗ ra khỏi hồ phóng 1,5 rồi thu dần về 1
x_pool = 690.0
s_out_new = T_cl([x_pool, np.polyval(sp, x_pool)])
Ln = nP(0, G)
line_new = lambda x: s_out_new[1] + (x - s_out_new[0]) * (-0.5)
pl, d0l = beach_left
beach_new = lambda x: Ln[1] + (x - Ln[0]) * 0.5 + d0l
x_mouth_new = s_out_new[1] + 0.5 * s_out_new[0] - (Ln[1] - 0.5 * Ln[0] + d0l)  # -0,5x + c1 = 0,5x + c2
# cửa suối cũ: giao đường tâm suối với mép cát
x_mouth_old = (pl[1] - sp[1]) / (sp[0] - pl[0])
y_mouth_old = np.polyval(sp, x_mouth_old)
# dải suối cũ theo (v, x) trên đoạn sạch, nối dài bằng đường cắt ít lệch nhất
vm0 = int(np.ceil(hw + 6))
XX, VV = np.meshgrid(np.arange(300, 600, dtype=np.float32), np.arange(-vm0, vm0 + 1, dtype=np.float32))
s_strip = sample(src, XX, np.polyval(sp, XX) + VV)
xs_new = np.arange(int(x_mouth_new) - 10, int(s_out_new[0]) + 30)
taper = 1.0 + 0.5 * smooth((xs_new - (s_out_new[0] - 140)) / 140)  # 1 → 1,5 ở chỗ ra khỏi hồ
tpos = np.concatenate([[0], np.cumsum(1 / taper[:-1])])  # vị trí trên dải cũ (px)
s_tiled = tile_strip(s_strip, int(tpos[-1]) + 3, 40, 21)
vmax = vm0 * 1.5 + 2
stream_m = np.zeros((H, W), np.float32)
for i, x in enumerate(xs_new):
    yc = line_new(x)
    y_a, y_b = max(0, int(yc - vmax - 2)), min(H, int(yc + vmax + 3))
    yy = np.arange(y_a, y_b, dtype=np.float32)
    v = (yy - yc) / taper[i]
    cs = sample(s_tiled, np.full_like(yy, tpos[i]), v + vm0)
    a = 1 - smooth((np.abs(v) - hw) / 5)
    out[y_a:y_b, x] = out[y_a:y_b, x] * (1 - a[:, None]) + cs * a[:, None]
    stream_m[y_a:y_b, x] = np.maximum(stream_m[y_a:y_b, x], (np.abs(v) < swid / 2).astype(np.float32))
placed["stream"] = stream_m

# cửa suối: giữ cỡ, giao suối–mép cát cũ ↔ mới
y_mouth_new = beach_new(x_mouth_new)
print("suối cũ", sp, "rộng", swid, "bờ trái cũ", pl, "cửa cũ", x_mouth_old, y_mouth_old, "cửa mới", x_mouth_new, y_mouth_new, "ra hồ", s_out_new)
paste("mouth", rect_mask(int(x_mouth_old) - 72, int(y_mouth_old) - 22, int(x_mouth_old) + 30, int(y_mouth_old) + 56, 14),
      (x_mouth_old, y_mouth_old), (x_mouth_new, y_mouth_new), 1.0, 0)

# hồ ven biển, mạch quặng
paste("lake2", blob_mask(112, 322, 266, 412), (189, 367), (205.6, 639.5), 1.0)
paste("ore1", blob_mask(405, 390, 578, 460, 4), (491, 425), nP(30, 66), 1.25)  # ô rừng (2,5), vòng 1 quanh khoảnh đầu giữa đảo
paste("ore2", blob_mask(955, 333, 1132, 418, 4), (1044, 375), nP(54, 18), 1.25)

# cụm vách (sau suối để hồ đè lên đầu suối), vách phải
paste("cliffs", poly_mask(CLIFF), A_cl, N_cl, K_cl)
RCLIFF = [(1150, 338), (1258, 282), (1392, 336), (1392, 376), (1264, 432), (1153, 381)]
paste("rcliff", poly_mask(RCLIFF), (1263.0, 428.0), nP(G, 12), 1.5)

# bến: giữ cỡ, mũi dưới cũ ↔ mới
paste("dock", rect_mask(682, 638, 768, 732, 14), oP(OG, OG), nP(G, G), 1.0, 0)  # mờ dần trước mép dưới ảnh cũ

# bến tàu ở mũi dưới (2026-11-19, cho chuyến tàu sảnh ↔ Nhà): GPT vẽ lại vùng cắt BEN_BOX (ben_nha.txt, ra ben_nha_1.png); dán phần
# đổi (cầu, cọc, vòng bọt, thùng) theo chỗ khác ảnh gốc trong khung bến, mép mềm
BEN_BOX = (887, 1040, 1322, 1330)
BEN_KEEP = (166, 44, 270, 272)  # khung được đổi, toạ độ trong vùng cắt 435 x 290
ben_png = os.path.join(HERE, "ben_nha_1.png")
if os.path.exists(ben_png):
    bx0, by0, bx1, by1 = BEN_BOX
    bw, bh = bx1 - bx0, by1 - by0
    orig = np.clip(out[by0:by1, bx0:bx1], 0, 255)
    edit = np.asarray(Image.open(ben_png).convert("RGB").resize((bw, bh), Image.LANCZOS)).astype(np.float32)
    diff = np.abs(ndi.gaussian_filter(edit, (1.6, 1.6, 0)) - ndi.gaussian_filter(orig, (1.6, 1.6, 0))).sum(2)
    k0, k1 = np.zeros((bh, bw), bool), np.zeros((bh, bw), bool)
    kx0, ky0, kx1, ky1 = BEN_KEEP
    k0[ky0:ky1, kx0:kx1] = True
    k1[ky0 + 6:ky1 - 4, kx0 + 14:kx1 - 14] = True  # lõi cầu: lấy hẳn
    m = (diff > 70) & k0
    m = ndi.binary_closing(m, iterations=3)
    m = ndi.binary_fill_holes(m) | k1
    m = ndi.binary_dilation(m, iterations=3) & k0
    a_ = ndi.gaussian_filter(m.astype(np.float32), 2.0)[..., None]
    out[by0:by1, bx0:bx1] = orig * (1 - a_) + edit * a_
    print("bến: dán", int(m.sum()), "px")

img = np.clip(out, 0, 255).astype(np.uint8)
Image.fromarray(img).save(OUT_PNG)

# ---------- đo ô cho features ----------
def cells_where(mask, thr=0.5):
    cs = []
    for gx in range(-2, G + 2):
        for gy in range(-2, G + 2):
            c = nP(gx + 0.5, gy + 0.5)
            x, y = int(round(c[0])), int(round(c[1]))
            if 0 <= x < W and 0 <= y < H and mask[y, x] > thr:
                cs.append((gx, gy))
    return cs


def water_of(name):
    m = placed[name] > 0.5
    a = img.astype(int)
    wat = (a[..., 2] > 160) & (a[..., 2] - a[..., 0] > 40)
    return (m & wat).astype(np.float32)


def bbox(cs):
    xs = [c[0] for c in cs]
    ys = [c[1] for c in cs]
    return min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1


feat = []
pool = cells_where(water_of("cliffs"))
pool = [c for c in pool if c[0] >= 12 and c[1] >= 12]  # bỏ thác trên vách
gx, gy, w, d = bbox(pool)
feat.append({"kind": "lake", "gx": gx, "gy": gy, "w": w, "d": d})
gx, gy, w, d = bbox(cells_where(water_of("lake2")))
feat.append({"kind": "lake", "gx": gx, "gy": gy, "w": w, "d": d})
st = [c for c in cells_where(placed["stream"]) if c[1] >= 0 and c[1] < G and (c[0], c[1]) not in pool]
st_gx = int(round(np.median([c[0] for c in st])))
gys = [c[1] for c in st if c[0] == st_gx]
feat.append({"kind": "stream", "gx": st_gx, "gy": min(gys), "w": 1, "d": G - min(gys)})
for nm, (cx, cy) in (("ore1", (30, 66)), ("ore2", (54, 18))):
    feat.append({"kind": "ore", "gx": cx - 3, "gy": cy - 3, "w": 6, "d": 6})
feat.append({"kind": "fertile", "gx": 38, "gy": 62, "w": 8, "d": 8})
print("features:", json.dumps(feat))
ore_cells = {nm: len(cells_where(placed[nm], 0.6)) for nm in ("ore1", "ore2")}
print("ô dưới mảng quặng vẽ:", ore_cells, "suối gx", st_gx, "từ gy", min(gys), "bề rộng mặt nạ (ô theo gx):", sorted(set(c[0] for c in st)))

# ---------- khối home_base ----------
meta = json.load(open(META, encoding="utf-8"))
meta["home_base"] = {"w": W, "h": H, "kind": "base", "top": [nTX, nTY], "diamondW": G * C, "grid": G, "stretchX": 1.0}
json.dump(meta, open(META, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- ảnh soi lưới ----------
pv = Image.fromarray(img).convert("RGB")
dr = ImageDraw.Draw(pv)
for k in range(0, G + 1, 12):
    dr.line([tuple(nP(k, 0)), tuple(nP(k, G))], fill=(255, 0, 0), width=1)
    dr.line([tuple(nP(0, k)), tuple(nP(G, k))], fill=(255, 0, 0), width=1)
for f in feat:
    q = [tuple(nP(f["gx"], f["gy"])), tuple(nP(f["gx"] + f["w"], f["gy"])), tuple(nP(f["gx"] + f["w"], f["gy"] + f["d"])), tuple(nP(f["gx"], f["gy"] + f["d"]))]
    dr.polygon(q, outline=(255, 0, 255))
pv.save(os.path.join(HERE, "preview_72_luoi.png"))
print("ok", OUT_PNG, W, H)
