# Phần động của đảo Thủy vùng đất (GD_Claude/18, góp ý 2026-11-18: "đảo nhiều chi tiết nhưng còn tĩnh, mây, thuyền cũng tĩnh").
# - cat_vat(): cắt mây, hải âu, thuyền khỏi ảnh nền thành hình rời (nền trong suốt), vá chỗ trống bằng mảng biển lấy từ chính ảnh;
#   game cho chúng trôi, lượn, dập dềnh (IslandAnim: drift, glide, boat).
# - anim_items(): danh sách món động khoá land_thuy trong island_anim.json (toạ độ ảnh nền gốc 1344 x 752, chưa đắp biển).
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

# tên hình, khung (ảnh nền gốc), cách lấy (largest: khối lớn nhất; boat: mọi khối trừ phần đảo ở góc trên phải), kiểu động, tốc / bán kính
VAT = [
    ("land_thuy_may_1", (48, 6, 172, 60), "largest", "drift", 0.0035),
    ("land_thuy_may_2", (1192, 615, 1326, 680), "largest", "drift", 0.0028),
    ("land_thuy_chim_1", (408, 10, 466, 44), "largest", "glide", 2.2),
    ("land_thuy_chim_2", (1118, 14, 1178, 44), "largest", "glide", 1.8),
    ("land_thuy_chim_3", (1163, 38, 1234, 72), "largest", "glide", 2.6),
    ("land_thuy_thuyen", (36, 568, 152, 678), "boat", "boat", 0),
]


def sea_mask(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (B > 195) & (G > 165) & (R < 190) & (B - R > 45)


def _patch_fill(a, sea, box, rng, P=48):
    """mảng biển đắp cho một khung: đóng chồng các mảng biển sạch P px lấy từ chính ảnh"""
    H, W, _ = a.shape
    frac = ndi.uniform_filter(sea.astype(np.float32), P)
    ys, xs = np.nonzero(frac > 0.995)
    ok = (ys > P // 2) & (ys < H - P // 2) & (xs > P // 2) & (xs < W - P // 2)
    ys, xs = ys[ok], xs[ok]
    x0, y0, x1, y1 = box
    acc = np.zeros((y1 - y0, x1 - x0, 3), np.float32)
    ws = np.zeros((y1 - y0, x1 - x0), np.float32)
    g = np.exp(-((np.arange(P) - P / 2 + 0.5) ** 2) / (2 * (P / 4) ** 2))
    win = np.outer(g, g).astype(np.float32)
    for yy in range(y0 - P // 2, y1, P // 3):
        for xx in range(x0 - P // 2, x1, P // 3):
            i = rng.integers(len(ys))
            patch = a[ys[i] - P // 2:ys[i] + P // 2, xs[i] - P // 2:xs[i] + P // 2]
            ya, xa, yb, xb = max(y0, yy), max(x0, xx), min(y1, yy + P), min(x1, xx + P)
            if yb <= ya or xb <= xa:
                continue
            pw = win[ya - yy:yb - yy, xa - xx:xb - xx]
            acc[ya - y0:yb - y0, xa - x0:xb - x0] += patch[ya - yy:yb - yy, xa - xx:xb - xx] * pw[..., None]
            ws[ya - y0:yb - y0, xa - x0:xb - x0] += pw
    return acc / np.maximum(ws, 1e-6)[..., None]


def cat_vat(img):
    """trả (ảnh nền đã vá, [(tên, hình RGBA phóng 2 lần, tâm (x, y) ảnh gốc, bề ngang ảnh gốc, kiểu, tham số)])"""
    a = np.asarray(img).astype(np.float32)
    sea = sea_mask(a)
    out = a.copy()
    rng = np.random.default_rng(11)
    cuts = []
    for name, (x0, y0, x1, y1), how, kind, par in VAT:
        sub = ~sea[y0:y1, x0:x1]
        sub = ndi.binary_opening(sub, iterations=1)
        lab, n = ndi.label(sub)
        if n == 0:
            continue
        sizes = ndi.sum(sub, lab, range(1, n + 1))
        if how == "largest":
            m = lab == (int(np.argmax(sizes)) + 1)
        else:  # thuyền + vệt sóng; bỏ khối chạm mép phải phía trên (vách đảo)
            m = np.zeros_like(sub)
            for i in range(1, n + 1):
                if sizes[i - 1] < 6:
                    continue
                yy, xx = np.nonzero(lab == i)
                if xx.max() >= (x1 - x0) - 3 and yy.min() < 40:
                    continue
                if xx.mean() > (x1 - x0) * 0.7 and yy.mean() < (y1 - y0) * 0.35:  # vệt bọt bờ ở góc trên phải
                    continue
                m |= lab == i
        m = ndi.binary_fill_holes(m)
        m = ndi.binary_dilation(m, iterations=1)
        full = np.zeros(sea.shape, bool)
        full[y0:y1, x0:x1] = m
        ys, xs = np.nonzero(full)
        bx0, by0, bx1, by1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
        alpha = Image.fromarray((full[by0:by1, bx0:bx1] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
        rgba = Image.fromarray(a[by0:by1, bx0:bx1].astype(np.uint8)).convert("RGBA")
        rgba.putalpha(alpha)
        if kind in ("drift", "glide"):
            # mây, chim (2026-11-18, mây sảnh dùng chung): khử viền xanh biển dính mép (điểm ngả xanh trong dần, phần còn lại thành
            # màu mực của nét viền), phóng 4 lần có làm nét cho mây to ở sảnh không nhòe; cỡ hiện trong game theo dữ liệu, không đổi
            q = np.asarray(rgba).astype(np.float32)
            s = np.clip((q[..., 2] - q[..., 0] - 25) / 60, 0, 1)
            ink = np.array([34, 27, 24], np.float32)
            q[..., :3] = q[..., :3] * (1 - s[..., None]) + ink * s[..., None]
            q[..., 3] *= 1 - s
            q[q[..., 3] < 250, :3] = ink  # điểm trong suốt / nửa trong mang màu mực, phóng ảnh không trộn màu biển trở lại mép
            rgba = Image.fromarray(q.clip(0, 255).astype(np.uint8))
            rgba = rgba.resize(((bx1 - bx0) * 4, (by1 - by0) * 4), Image.LANCZOS).filter(
                ImageFilter.UnsharpMask(radius=2, percent=90, threshold=2))
        else:
            rgba = rgba.resize(((bx1 - bx0) * 2, (by1 - by0) * 2), Image.LANCZOS)
        cuts.append((name, rgba, ((bx0 + bx1) / 2, (by0 + by1) / 2), bx1 - bx0, kind, par))
        # vá: chỗ vật (nới 3 px) thay bằng biển, mép làm mềm
        hole = ndi.binary_dilation(full, iterations=3)
        fb = (max(0, bx0 - 30), max(0, by0 - 30), min(a.shape[1], bx1 + 30), min(a.shape[0], by1 + 30))
        fill = _patch_fill(a, sea & ~hole, fb, rng)
        soft = np.asarray(Image.fromarray((hole * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
        k = soft[fb[1]:fb[3], fb[0]:fb[2], None]
        out[fb[1]:fb[3], fb[0]:fb[2]] = out[fb[1]:fb[3], fb[0]:fb[2]] * (1 - k) + fill * k
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), cuts


# món động có sẵn trong IslandAnim, toạ độ ảnh nền gốc (đọc trên lưới _luoi_q_*.png), cỡ = bề ngang món (px ảnh gốc)
TINH = [
    ("swirl", (812, 65), 120),                                   # xoáy nước cạnh đền rồng
    ("foam", (535, 105), 26), ("foam", (398, 312), 22), ("foam", (830, 222), 24), ("foam", (868, 262), 22),
    ("foam", (928, 478), 22), ("foam", (838, 548), 24), ("foam", (1058, 614), 24), ("foam", (372, 420), 22),
    ("ripple", (250, 505), 34), ("ripple", (335, 560), 30), ("ripple", (110, 150), 34), ("ripple", (245, 135), 30),
    ("ripple", (622, 566), 40), ("ripple", (1010, 470), 34), ("ripple", (585, 640), 22), ("ripple", (690, 655), 20),
    ("sparkle", (112, 118), 14), ("sparkle", (238, 98), 14), ("sparkle", (1000, 118), 16), ("sparkle", (1150, 140), 16),
    ("sparkle", (1120, 210), 14), ("sparkle", (1062, 300), 16), ("sparkle", (1212, 298), 16), ("sparkle", (1226, 392), 16),
    ("sparkle", (982, 330), 14), ("sparkle", (650, 98), 14),
    ("leaf", (520, 560), 16), ("leaf", (790, 555), 16), ("leaf", (470, 285), 14), ("leaf", (860, 400), 14), ("leaf", (300, 470), 14),
    ("rain", (565, 300), 70), ("rain", (715, 300), 60), ("rain", (765, 318), 60),
    ("wave", (200, 712), 46), ("wave", (500, 728), 46), ("wave", (900, 726), 46), ("wave", (1290, 420), 40),
    ("wave", (30, 300), 40), ("wave", (1318, 200), 40), ("wave", (300, -60), 46), ("wave", (900, -80), 46), ("wave", (1150, -40), 40),
]
# thêm mây trôi dùng lại hình mây đã cắt (khoảng trời trống phía trên đảo, biển đắp thêm)
MAY_THEM = [("land_thuy_may_2", (420, -70), 0.0022), ("land_thuy_may_1", (980, -45), 0.0031), ("land_thuy_may_1", (60, 420), 0.0026)]


# vành mây: bề ngang một đám mây (tỉ lệ bề ngang ảnh); giới hạn kéo, zoom (land.pan) tính theo đây
FRAME_S = 0.15

# đèn ban đêm (DayNight): đèn hải đăng quét vòng, quầng đèn ở đền, tháp mưa, nấm phát sáng vực hang (toạ độ ảnh nền gốc, cỡ px)
LIGHTS = [
    ("beam", (97, 304), 260), ("glow", (97, 304), 70),
    ("glow", (650, 112), 90), ("glow", (652, 345), 60),
    ("glow", (1062, 300), 46), ("glow", (1212, 298), 46), ("glow", (1226, 392), 46), ("glow", (982, 330), 40),
]


def anim_items(cuts, W, H, pad_t, pad_l=0):
    """khoá land_thuy của island_anim.json; toạ độ tỉ lệ theo ảnh nền đã đắp biển (W x H, đắp pad_t ở trên, pad_l bên trái)"""
    def P(x, y):
        return round((x + pad_l) / W, 4), round((y + pad_t) / H, 4)
    items = []
    for k, (x, y), w in TINH:
        u, v = P(x, y)
        items.append({"k": k, "x": u, "y": v, "s": round(w / W, 4)})
    for name, rgba, (x, y), w, kind, par in cuts:
        u, v = P(x, y)
        it = {"k": kind, "a": name, "x": u, "y": v, "s": round(w / W, 4)}
        if par:
            it["v"] = par
        items.append(it)
    widths = {name: w for name, rgba, c, w, kind, par in cuts}
    for name, (x, y), v in MAY_THEM:
        u, vv = P(x, y)
        items.append({"k": "drift", "a": name, "x": u, "y": vv, "s": round(widths.get(name, 120) / W, 4), "v": v})
    lights = []
    for k, (x, y), w in LIGHTS:
        u, v = P(x, y)
        lights.append({"k": k, "x": u, "y": v, "s": round(w / W, 4)})
    # vành mây quanh mép ảnh (IslandAnim frame): che biển ngoài ảnh lệch tông; hình mây đã cắt phóng to, ruột mây làm màu phủ ngoài
    frame = {"a": ["land_thuy_may_2"], "s": FRAME_S, "fill": "#fdf5e7"}  # một hình cho cả vành: gộp lệnh vẽ
    return {"items": items, "rivers": [], "lights": lights, "frame": frame}
