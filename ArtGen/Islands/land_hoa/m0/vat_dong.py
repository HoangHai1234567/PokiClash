# Phần động của đảo Hỏa vùng đất (chép từ land_moc/m0, 2026-11-19) (GD_Claude/18, góp ý 2026-11-18: "đảo nhiều chi tiết nhưng còn tĩnh, mây, thuyền cũng tĩnh").
# - cat_vat(): cắt mây, hải âu, thuyền khỏi ảnh nền thành hình rời (nền trong suốt), vá chỗ trống bằng mảng biển lấy từ chính ảnh;
#   game cho chúng trôi, lượn, dập dềnh (IslandAnim: drift, glide, boat).
# - anim_items(): danh sách món động khoá land_hoa trong island_anim.json (toạ độ ảnh nền gốc 1344 x 752, chưa đắp biển).
# - đảo Hỏa (người dùng 2026-11-19: "làm mấy cái khói bốc lên thành anim đi cho sinh động"): ảnh nền đã xoá hết khói, hơi nước;
#   game vẽ cột khói nhiều múi (IslandAnim plume) ở lỗ phun, lò đồng, ống khói lò rèn, suối nóng, miệng núi lửa; tàn lửa chạy dọc
#   sông dung nham (rivers, IslandAnim Flow).
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

# tên hình, khung (ảnh nền gốc), cách lấy (largest: khối lớn nhất; boat: mọi khối trừ phần đảo ở góc trên phải), kiểu động, tốc / bán kính
VAT = [
    ("land_hoa_may_1", (6, 4, 160, 82), "largest", "drift", 0.0035),
    ("land_hoa_may_2", (1160, 626, 1340, 722), "largest", "drift", 0.0028),
    ("land_hoa_chim_1", (1205, 15, 1288, 62), "largest", "glide", 2.2),
    ("land_hoa_chim_2", (1266, 44, 1326, 84), "largest", "glide", 1.8),
    ("land_hoa_chim_3", (6, 536, 82, 584), "largest", "glide", 2.6),
    ("land_hoa_thuyen", (24, 606, 146, 706), "boat", "boat", 0),
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
                if yy.max() < 16:  # mẩu chim hải âu bay sát trên cột buồm (đảo Mộc), chim cắt riêng
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
STEAM, SMOKE, ASH = "#f2ece2", "#a1958f", "#857a76"  # màu đáy cột: hơi nước trắng ngà, khói lò xám, khói núi lửa xám sẫm
# phần tử thứ 4 (nếu có): khoá thêm cho món (plume: c màu đáy, n số múi, l đời múi, v chiều gió)
TINH = [
    ("foam", (57, 168), 22), ("foam", (1297, 152), 22), ("foam", (1296, 578), 20), ("foam", (40, 470), 20), ("foam", (930, 715), 20),
    ("ripple", (225, 535), 22), ("ripple", (455, 522), 22), ("ripple", (500, 665), 18), ("ripple", (640, 85), 26),  # suối nóng
    ("wave", (210, 728), 46), ("wave", (470, 742), 46), ("wave", (1010, 735), 46), ("wave", (1320, 470), 40),
    ("wave", (22, 300), 40), ("wave", (1322, 250), 40), ("wave", (300, -60), 46), ("wave", (900, -80), 46), ("wave", (1150, -40), 40),
    # cột khói, hơi nước (gió thổi sang phải)
    ("plume", (178, 120), 24, {"c": STEAM, "v": 1}), ("plume", (270, 90), 20, {"c": STEAM, "v": 1, "n": 6, "l": 3.4}),  # lỗ phun
    ("plume", (600, 80), 26, {"c": STEAM, "v": 1, "n": 6, "l": 3.4}), ("plume", (690, 70), 24, {"c": STEAM, "v": 1, "n": 6, "l": 3.6}),  # ao rùa
    ("plume", (1242, 222), 26, {"c": SMOKE, "v": 1}),  # ống khói lò rèn
    ("plume", (1162, 440), 20, {"c": SMOKE, "v": 1, "n": 6, "l": 3.4}),  # lò nung tượng đất
    ("plume", (229, 534), 22, {"c": STEAM, "v": 1, "n": 6, "l": 3.0}), ("plume", (457, 520), 22, {"c": STEAM, "v": 1, "n": 6, "l": 3.2}),
    ("plume", (500, 664), 18, {"c": STEAM, "v": 1, "n": 5, "l": 2.8}),  # ao suối nóng
]
SONG = [("lava", [(622, 462), (655, 505), (705, 560), (760, 605), (805, 645), (832, 690), (842, 722)], 18)]
# thêm mây trôi dùng lại hình mây đã cắt (khoảng trời trống phía trên đảo, biển đắp thêm)
MAY_THEM = [("land_hoa_may_2", (420, -70), 0.0022), ("land_hoa_may_1", (980, -45), 0.0031), ("land_hoa_may_1", (1250, 600), 0.0026)]


# vành mây: bề ngang một đám mây (tỉ lệ bề ngang ảnh); giới hạn kéo, zoom (land.pan) tính theo đây
FRAME_S = 0.15

# đèn ban đêm (DayNight): lửa lò, đèn đá, ao dung nham, lò rèn, miệng núi lửa, thác dung nham, ma trơi tím (toạ độ ảnh nền gốc, cỡ px)
LIGHTS = [
    ("glow", (540, 82), 40), ("glow", (627, 64), 40), ("glow", (707, 106), 40), ("glow", (402, 118), 34), ("glow", (360, 75), 50),
    ("glow", (1245, 300), 50), ("glow", (565, 228), 90), ("glow", (292, 478), 40), ("glow", (1160, 490), 40),
    ("glow", (915, 270), 40), ("glow", (95, 330), 30)]


def anim_items(cuts, W, H, pad_t, pad_l=0):
    """khoá land_hoa của island_anim.json; toạ độ tỉ lệ theo ảnh nền đã đắp biển (W x H, đắp pad_t ở trên, pad_l bên trái)"""
    def P(x, y):
        return round((x + pad_l) / W, 4), round((y + pad_t) / H, 4)
    items = []
    for t in TINH:
        k, (x, y), w = t[:3]
        u, v = P(x, y)
        it = {"k": k, "x": u, "y": v, "s": round(w / W, 4)}
        if len(t) > 3:
            it.update(t[3])
        items.append(it)
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
    frame = {"a": ["land_hoa_may_2"], "s": FRAME_S, "fill": "#fdf5e7"}  # một hình cho cả vành: gộp lệnh vẽ
    rivers = [{"k": k, "w": round(rw / W, 4), "pts": [list(P(x, y)) for x, y in pts]} for k, pts, rw in SONG]
    return {"items": items, "rivers": rivers, "lights": lights, "frame": frame}
