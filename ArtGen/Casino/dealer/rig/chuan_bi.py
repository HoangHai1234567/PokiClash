# Chuẩn bị mảnh để rig Lão Mực trong AtomSpine (GD_Claude/31 mốc D2, bản 2). Đọc L1_goc_rig.png (1024 x 1536, nền xanh lơ,
# không viền) và các mảnh đã cắt ở manh/ (cat_manh.py), ghi ra ../atom/images/:
#   than.png       thân + đầu + chỏm + chân + giày. KHÔNG còn mẩu tay nào (bản 1 giữ "khớp vai" ở thân nên khi tay vươn hướng khác
#                  thì mẩu đó đứng lại ở vai); chỗ nơ và chỗ lưỡi trai che thì tô đen lại bằng vân của chính thân.
#   no.png         nơ đỏ (mảnh riêng, có xương cánh nơ; vẽ TRƯỚC tay để che gốc tay như ảnh gốc)
#   luoi_trai.png  lưỡi trai (xanh + đai kem + nút vàng)
#   tay_trai.png / tay_phai.png  ống tay DỰNG LẠI bằng mã: dải thẳng đều bề rộng, hai đầu bo tròn, vân chì lấy từ mặt (vùng đen
#                  sạch), không có nịt tay áo. Gốc ống là một chỏm tròn nằm trong thân, dưới cánh nơ: xoay hướng nào vai cũng tròn.
#   nit_trai.png / nit_phai.png  nịt tay áo đỏ + khoá vàng, mảnh cứng gắn một đốt tay (tay giãn dài nịt không bị kéo dãn)
#   mat_XX.png, mieng_XX.png (co theo tỉ lệ đầu), tay_XX.png (bàn tay, co theo cỡ găng ảnh gốc)
# và ../atom/geo.json: chỗ đặt (left, top trên khung 1024 x 1536), cỡ, các mốc khớp.
# Bản 1 (giữ khớp vai ở thân) lưu ở ban1/.
# Chạy: py -3 -I chuan_bi.py
import json, math, os, sys
import numpy as np
import cv2
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
IMG = os.path.join(ATOM, "images")
os.makedirs(IMG, exist_ok=True)
CYAN = np.array([58, 208, 255], float)
W, H = 1024, 1536
ORIGIN = (512, 1460)  # mặt đất giữa hai chân
ARM_R = 24.5          # nửa bề rộng ống tay (đo trên ảnh gốc: rộng vuông góc ~50 px)

# mốc khớp (px ảnh L1)
J = {
    # vai: trong thân, dưới cánh nơ; cổ tay: trên trục tay ảnh gốc, ngay mép cổ găng
    "vai_trai": (432, 566), "co_tay_trai": (238, 856),
    "vai_phai": (592, 566), "co_tay_phai": (782, 856),
    "hong": (512, 1000), "bung": (512, 900), "nguc": (512, 790), "vai": (512, 680), "co": (512, 575), "dau": (514, 548),
    "dinh_dau": (514, 215),
    "dui_trai": (400, 1030), "goi_trai": (398, 1170), "co_chan_trai": (402, 1320), "ban_chan_trai": (345, 1405),
    "dui_phai": (622, 1030), "goi_phai": (624, 1170), "co_chan_phai": (620, 1320), "ban_chan_phai": (678, 1405),
    "mat": (522, 378), "mieng": (522, 468),
    "luoi": (545, 225), "luoi2": (665, 232), "luoi3": (790, 258),
    "chom1": (430, 222), "chom2": (452, 122), "chom3": (504, 62), "chom4": (538, 104),
    "mai1": (338, 422), "mai2": (266, 352),
    "no": (512, 572), "no_t": (492, 572), "no_t2": (420, 570), "no_p": (532, 572), "no_p2": (604, 570),
}


def load_rgba():
    a = np.asarray(Image.open(os.path.join(HERE, "L1_goc_rig.png")).convert("RGB")).astype(float)
    d = np.sqrt(((a - CYAN) ** 2).sum(2))
    al = np.clip((d - 70) / 40, 0, 1)
    rgb = a.copy()
    spill = (rgb[..., 2] > np.maximum(rgb[..., 0], rgb[..., 1]) + 30) & (al < 1)
    rgb[spill, 2] = np.maximum(rgb[spill, 0], rgb[spill, 1])
    return rgb, al


def largest(al, thr=0.02):
    """Giữ khối liền lớn nhất (mẩu rời lơ lửng, vụn bỏ đi)."""
    m = (al > thr).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n <= 2:
        return al
    big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return al * (lab == big)


def fill_holes(mask):
    m = mask.astype(np.uint8)
    pad = cv2.copyMakeBorder(m, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    cv2.floodFill(pad, None, (0, 0), 2)
    return pad[1:-1, 1:-1] != 2


def save(name, rgb, al, pad=6):
    ys, xs = np.where(al > 0.03)
    y0, y1 = max(0, ys.min() - pad), min(H, ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(W, xs.max() + pad + 1)
    out = np.dstack([rgb[y0:y1, x0:x1], al[y0:y1, x0:x1] * 255]).clip(0, 255).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(IMG, name + ".png"))
    return {"left": int(x0), "top": int(y0), "w": int(x1 - x0), "h": int(y1 - y0)}


# vùng đen sạch làm nguồn vân chì (mặt để trống): hình chữ nhật trong đĩa đầu, dưới lưỡi trai
SRC = (402, 302, 608, 502)  # x0, y0, x1, y1


def black_tex(rgb, xx, yy, ox=0, oy=0):
    """Vân chì đen của thân tại (xx, yy): lấy từ vùng SRC, lặp kiểu xoay 180 độ từng ô (không lộ mối nối, nét chéo giữ hướng)."""
    sw, sh = SRC[2] - SRC[0], SRC[3] - SRC[1]
    kx = np.floor_divide(xx + ox, sw)
    ky = np.floor_divide(yy + oy, sh)
    fx = np.mod(kx, 2) == 1
    fy = np.mod(ky, 2) == 1
    u = np.mod(xx + ox, sw)
    v = np.mod(yy + oy, sh)
    # lặp gương theo từng trục; ô lật một trục thì nét chéo đổi hướng, nên lật luôn trục kia (thành xoay 180 độ)
    flip = fx ^ fy
    u2 = np.where(fx, sw - 1 - u, u)
    v2 = np.where(fy, sh - 1 - v, v)
    u3 = np.where(flip, sw - 1 - u2, u2)
    return rgb[(SRC[1] + v2).astype(int), (SRC[0] + u3).astype(int)]


def make_arm(rgb, S, E, seed):
    """Ống tay thẳng từ S (vai) tới E (cổ tay): chỏm tròn hai đầu, mép hơi rung như nét tay, vân chì đen."""
    yy, xx = np.mgrid[0:H, 0:W]
    dx, dy = E[0] - S[0], E[1] - S[1]
    L = math.hypot(dx, dy)
    ex, ey = dx / L, dy / L
    u = (xx - S[0]) * ex + (yy - S[1]) * ey
    v = -(xx - S[0]) * ey + (yy - S[1]) * ex
    uc = np.clip(u, 0, L + 4)          # dài thêm 4 px chui vào cổ găng
    d = np.sqrt((u - uc) ** 2 + v ** 2)
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6.28, 3)
    r = ARM_R + 0.9 * np.sin(u * 0.105 + ph[0]) + 0.6 * np.sin(u * 0.31 + ph[1]) + 0.35 * np.sin(u * 0.83 + ph[2])
    al = np.clip((r - d) / 1.6 + 0.5, 0, 1)
    tex = black_tex(rgb, xx, yy, ox=seed * 37, oy=seed * 91)
    return tex, al


NHAND = 12   # 1..10: tờ L3 (cat_manh.py); 11, 12: tờ L4 (hai tay nhìn nghiêng từ phía mu, ngón cái ở trên)


def cut_side_hands():
    """Cắt tờ L4_tay_nghieng.png (nền xanh lơ, 2 món): trái = bàn tay mở dựng đứng (tay_11), phải = nắm tay dựng nghiêng (tay_12),
    co về đúng tỉ lệ các tay tờ L3 (bàn tay mở dài bằng tay_09) rồi ghi vào manh/ như các tay khác."""
    src = os.path.join(HERE, "L4_tay_nghieng.png")
    a = np.asarray(Image.open(src).convert("RGB")).astype(float)
    d = np.sqrt(((a - CYAN) ** 2).sum(2))
    al = np.clip((d - 70) / 40, 0, 1)
    rgb = a.copy()
    spill = (rgb[..., 2] > np.maximum(rgb[..., 0], rgb[..., 1]) + 30) & (al < 1)
    rgb[spill, 2] = np.maximum(rgb[spill, 0], rgb[spill, 1])
    n, lab, st, _ = cv2.connectedComponentsWithStats((al > 0.5).astype(np.uint8), 8)
    big = sorted(range(1, n), key=lambda i: -st[i, cv2.CC_STAT_AREA])[:2]
    big.sort(key=lambda i: st[i, cv2.CC_STAT_LEFT])

    # tỉ lệ: bàn tay mở dựng đứng (món trái) dài bằng bàn tay úp tay_09 của tờ L3; nắm tay dùng chung hệ số (cùng một tờ)
    ref_len = Image.open(os.path.join(HERE, "manh", "tay_09.png")).width
    f = ref_len / float(st[big[0], cv2.CC_STAT_WIDTH])
    for idx, i in zip((11, 12), big):
        x, y, w, h = st[i, 0], st[i, 1], st[i, 2], st[i, 3]
        pad = 4
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), x + w + pad, y + h + pad
        m = (lab[y0:y1, x0:x1] == i)
        m = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        out = np.dstack([rgb[y0:y1, x0:x1], al[y0:y1, x0:x1] * m * 255]).clip(0, 255)
        im = Image.fromarray(out.astype(np.uint8), "RGBA")
        im = im.resize((max(1, round(im.width * f)), max(1, round(im.height * f))), Image.LANCZOS)
        im = defringe(im)
        im.save(os.path.join(HERE, "manh", f"tay_{idx:02d}.png"))
        print(f"tay_{idx:02d}: cắt {w} x {h} -> co {f:.3f} = {im.size}")


def defringe(im):
    """Mép bán trong suốt của mắt / miệng còn ánh xanh lơ của nền (thành một vòng xám quanh mí trên mặt đen): thay màu các điểm
    mép bằng màu trung bình của điểm đặc kề bên."""
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    al = a[..., 3]
    opq = (cv2.erode((al >= 250).astype(np.uint8), np.ones((3, 3), np.uint8))).astype(np.float32)
    k = (0, 0)
    num = cv2.GaussianBlur(a[..., :3] * opq[..., None], k, 2.0)
    den = cv2.GaussianBlur(opq, k, 2.0)[..., None]
    fill = num / np.maximum(den, 1e-4)
    edge = (opq < 0.5) & (den[..., 0] > 0.02)
    a[..., :3][edge] = fill[edge]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


def main():
    rgb, al = load_rgba()
    yy, xx = np.mgrid[0:H, 0:W]
    lum = rgb.mean(2)
    sat = rgb.max(2) - rgb.min(2)
    solid = al > 0.5
    vis = al > 0.02
    geo = {"canvas": [W, H], "origin": list(ORIGIN), "J": J, "parts": {}, "arm_r": ARM_R}

    cream = (lum > 170) & (sat < 90)
    red = (rgb[..., 0] > 150) & (rgb[..., 0] > rgb[..., 1] + 50)
    gold = (rgb[..., 0] > 180) & (rgb[..., 1] > 120) & (rgb[..., 2] < 110)
    reddish = red | gold | ((rgb[..., 0] > rgb[..., 1] + 25) & (rgb[..., 0] > 80))
    # đỏ cam tươi của nơ / nịt (236, 76, 46), khác đỏ rượu của áo gi lê (154, 55, 54): lục hơn lam rõ
    bright = (rgb[..., 0] > 195) & (rgb[..., 1] - rgb[..., 2] > 14) & (rgb[..., 0] > rgb[..., 1] + 70) & (rgb[..., 1] < 135)

    # ---------- nơ: khối đỏ quanh cổ ----------
    bow = bright & (yy > 515) & (yy < 628) & (xx > 405) & (xx < 618)
    bow = cv2.morphologyEx(bow.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    bow = fill_holes(bow).astype(np.uint8)
    bow = cv2.morphologyEx(bow, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))  # bỏ hai mẩu chữ V vàng cam
    n, lab, st, _ = cv2.connectedComponentsWithStats(bow.astype(np.uint8), 8)
    bow = lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))
    bow_soft = cv2.dilate(bow.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    geo["parts"]["no"] = save("no", rgb, al * bow_soft)

    # ---------- nịt tay áo: đỏ + vàng trên hai tay ----------
    for side, x0, x1 in (("trai", 290, 395), ("phai", 630, 735)):
        box = (xx > x0) & (xx < x1) & (yy > 625) & (yy < 725)
        m = box & (bright | gold)
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        m = fill_holes(m).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
        m = lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))
        ms = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8)
        g = save("nit_" + side, rgb, np.clip(ms * 1.3, 0, 1) * (al > 0.3))
        ys, xs = np.where(m)
        g["tam"] = [float(xs.mean()), float(ys.mean())]
        geo["parts"]["nit_" + side] = g

    # ---------- bàn tay + cổ găng: bỏ khỏi thân ----------
    hands = vis & (yy > 845) & (yy < 1100) & ((xx < 300) | (xx > 724))

    # ---------- lưỡi trai ----------
    green = (rgb[..., 1] > rgb[..., 0] + 25) & (rgb[..., 1] > rgb[..., 2] - 30) & (lum > 60)
    visor = solid & (yy < 320) & (green | cream | gold)
    visor = cv2.morphologyEx(visor.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    visor = cv2.morphologyEx(visor, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(visor, 8)
    visor = np.isin(lab, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 800])
    visor_soft = cv2.dilate(visor.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    visor_ring = cv2.dilate(visor.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0

    # ---------- thân ----------
    body_al = al.copy()
    body_rgb = rgb.copy()
    body_al[hands] = 0
    # cắt tay: (a) mọi thứ ngoài mép thân ở tầm cổ (thân ở đây rộng 421..604, bị nơ che);
    #          (b) phần đen bám sát mép áo gi lê ngay dưới nơ (tay chạm áo tới y ~ 660);
    #          (c) phần còn lại của tay rời hẳn thân: rụng khi lấy khối liền lớn nhất.
    TL, TR = 421, 604
    neck_band = (yy >= 532) & (yy <= 614)
    body_al[neck_band & ((xx < TL) | (xx > TR))] = 0
    vest_l = TL - (yy - 612) * 0.39   # mép trái áo: (421, 612) -> (335, 830)
    vest_r = TR + (yy - 612) * 0.39
    arm_zone = (yy > 606) & (yy < 672)
    body_al[arm_zone & (xx < vest_l + 6) & ~reddish] = 0
    body_al[arm_zone & (xx > vest_r - 6) & ~reddish] = 0

    tex_all = black_tex(rgb, xx, yy, ox=61, oy=17)
    # chỗ nơ che: tô đen (cổ + vai trong)
    bow_fill = cv2.dilate(bow.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    bow_fill &= (xx >= TL + 1) & (xx <= TR - 1)
    body_rgb[bow_fill] = tex_all[bow_fill]
    body_al[bow_fill] = 1.0

    # chỗ lưỡi trai che đầu / gốc chỏm: tô đen. Vùng tô = đĩa đầu (khớp từ nửa dưới: tâm 506, 363, bán kính 188) hợp với bao lồi
    # của chỏm tóc + nửa trên trái của đầu, để lưỡi trai bay lên (sốc) không lộ đỉnh đầu bị vát hay cục vuông chỗ đai.
    dark_solid = solid & (lum < 90) & ~visor_soft
    HC, HR = (506.0, 363.0), 187.0
    disc = (xx - HC[0]) ** 2 + (yy - HC[1]) ** 2 <= HR * HR
    geo["dau_tron"] = [HC[0], HC[1], HR]
    base = ((disc & (yy < 420)) | (dark_solid & (yy < 260) & (xx < 560))).astype(np.uint8)
    region = cv2.morphologyEx(base, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (71, 71))) > 0
    # tô lại TRỌN phần lưỡi trai từng che (kể cả điểm đen sẵn có ở mép đai: chúng sẫm hơn, để lại sẽ thành một vệt)
    fill = (region & visor_ring) | (disc & (yy < 330) & ~dark_solid)
    body_rgb[fill] = tex_all[fill]
    body_al[fill] = 1.0
    body_al[visor_soft & ~fill] = 0
    body_al[visor_ring & ~fill & (lum > 85)] = 0
    teal = (body_rgb[..., 1] - body_rgb[..., 0] > 50) & (body_rgb[..., 2] - body_rgb[..., 0] > 40)
    body_al[teal] = 0
    bm = (body_al > 0.02).astype(np.uint8)
    core = cv2.morphologyEx(bm, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    keep = cv2.dilate(core, np.ones((5, 5), np.uint8)) & bm
    body_al = largest(body_al * keep)
    # gai mảnh quanh chỗ lưỡi trai cũ (mép đai sót lại): mở bằng elip 15 px ở vùng đỉnh đầu
    top = (body_al > 0.3).astype(np.uint8)
    top_open = cv2.morphologyEx(top, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    top_keep = cv2.dilate(top_open, np.ones((3, 3), np.uint8)) > 0
    body_al[(yy < 330) & ~top_keep] = 0
    # vụn đỏ / vàng của nịt còn sót ngoài mép áo
    stray = (yy > 600) & (yy < 730) & ((xx < vest_l - 2) | (xx > vest_r + 2))
    body_al[stray] = 0
    body_al = largest(body_al)
    geo["parts"]["than"] = save("than", body_rgb, body_al)
    geo["parts"]["luoi_trai"] = save("luoi_trai", rgb, al * visor_soft)

    # ---------- ống tay dựng lại ----------
    for side, seed in (("trai", 1), ("phai", 2)):
        tex, a = make_arm(rgb, J["vai_" + side], J["co_tay_" + side], seed)
        geo["parts"]["tay_" + side] = save("tay_" + side, tex, a, pad=4)

    # ---------- mắt, miệng ----------
    head_w = 350
    ref_eye = Image.open(os.path.join(HERE, "manh", "mat_01.png")).width
    ref_mouth = Image.open(os.path.join(HERE, "manh", "mieng_01.png")).width
    s_eye = head_w * 0.62 / ref_eye
    s_mouth = head_w * 0.58 / ref_mouth
    geo["scale_eye"], geo["scale_mouth"] = s_eye, s_mouth
    for kind, s, n in (("mat", s_eye, 10), ("mieng", s_mouth, 10)):
        for i in range(1, n + 1):
            im = Image.open(os.path.join(HERE, "manh", f"{kind}_{i:02d}.png"))
            im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
            im = defringe(im)
            im.save(os.path.join(IMG, f"{kind}_{i:02d}.png"))
            geo["parts"][f"{kind}_{i:02d}"] = {"w": im.width, "h": im.height}

    # ---------- bàn tay ----------
    cut_side_hands()
    h01 = Image.open(os.path.join(HERE, "manh", "tay_01.png")).height
    s_hand = 235.0 / h01
    geo["scale_hand"] = s_hand
    geo["n_hand"] = NHAND
    for i in range(1, NHAND + 1):
        im = Image.open(os.path.join(HERE, "manh", f"tay_{i:02d}.png")).convert("RGBA")
        if i == 9:
            # bàn tay úp (tay_09) trên tờ L3 vẽ ngón cái (ngón ngắn nhất) ở mép DƯỚI; đặt lên bàn thì ngón cái rơi về phía người
            # chơi (người dùng trả 2026-11-26: "ngón cái phải ở gần người, ngón út ở phía người chơi"). Lật dọc ảnh ngay từ đây
            # để mọi clip dùng tay_09 đều có ngón cái ở mép trên (phía bụng Lão Mực).
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        a = np.asarray(im).astype(float)
        aa = a[..., 3] > 128
        blk = (aa & (a[..., :3].mean(2) < 110)).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(blk, 8)
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        ys, xs = np.where(lab == big)
        sy, sx = ys.mean(), xs.mean()
        cy, cx = np.where(aa)
        cyy, cxx = cy.mean(), cx.mean()
        d = np.array([cxx - sx, cyy - sy])
        d /= np.linalg.norm(d) + 1e-9
        if i >= 11:
            d = np.array([1.0, 0.0])    # hai tay nghiêng vẽ nằm ngang, mép dưới phẳng: giữ đúng trục ngang của ảnh
        s = s_hand
        im2 = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
        im2.save(os.path.join(IMG, f"tay_{i:02d}.png"))
        along = (xs - sx) * d[0] + (ys - sy) * d[1]
        root = np.array([sx, sy]) + d * along.min()
        geo["parts"][f"tay_{i:02d}"] = {"w": im2.width, "h": im2.height, "goc": [float(root[0] * s), float(root[1] * s)],
                                        "huong": [float(d[0]), float(d[1])], "s": s}
    with open(os.path.join(ATOM, "geo.json"), "w", encoding="utf-8") as f:
        json.dump(geo, f, ensure_ascii=False, indent=1)
    print("đã ghi", len(geo["parts"]), "mảnh vào", IMG)
    for k in ("than", "no", "luoi_trai", "tay_trai", "tay_phai", "nit_trai", "nit_phai"):
        print(k, geo["parts"][k])

    # tờ soi mảnh
    soi = os.path.join(HERE, "soi")
    os.makedirs(soi, exist_ok=True)
    sheet = Image.new("RGB", (1560, 1450), (255, 0, 255))
    x = 10
    for k in ("than", "tay_trai", "tay_phai", "no", "nit_trai", "nit_phai"):
        im = Image.open(os.path.join(IMG, k + ".png"))
        sheet.paste(im, (x, 10), im)
        x += im.width + 14
    sheet.save(os.path.join(soi, "D2b_manh.png"))


if __name__ == "__main__":
    main()
