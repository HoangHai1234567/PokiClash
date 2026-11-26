# Cắt mảnh cậu thám hiểm (nhìn sau lưng) từ tờ gốc rig goc_rig.png (Magnific, không viền, nền hồng #F933D5) cho rig AtomSpine.
# GD_Claude/32_BenCau_Scene.md mục 2. Ra: atom/images/<mảnh>.png (nửa cỡ, cắt sát), geo.json (khung mảnh + khớp, toạ độ nửa cỡ,
# gốc ảnh trái trên), xem_manh.png (soát: mỗi mảnh một màu).
# Phần bị che vẽ bù bằng mã: tay kéo dài vào dưới áo choàng, quần kéo lên dưới vạt áo, chân kéo lên dưới quần, cổ dưới tóc,
# thân áo kem sau áo choàng (lộ ra khi áo bay).
# Chạy: py -3 -I chuan_bi.py
import os, sys, json
import numpy as np
import cv2
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
# 2026-11-26 bản 3: tờ gốc có tay đang cầm cần (người dùng: "tay không cần cử động, gen 2 tay bình thường"); thân trùng
# goc_rig.png (IoU 0,992, không lệch)
SRC = os.path.join(HERE, "goc_tay_cam.png")
OUT = os.path.join(HERE, "atom", "images")
os.makedirs(OUT, exist_ok=True)
SCALE = 0.5
BG = np.array([249, 51, 213])
CROSS = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))


def comp_keep(mask, min_area=200):
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    keep = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= min_area]
    return np.isin(lab, keep)


def fill_holes(m):
    ff = np.pad(m.astype(np.uint8), 1)
    cv2.floodFill(ff, None, (0, 0), 2)
    return ff[1:-1, 1:-1] != 2


def main():
    img = np.asarray(Image.open(SRC).convert("RGB")).astype(np.int32)
    h, w, _ = img.shape
    R, G, B = img[..., 0], img[..., 1], img[..., 2]
    fg = np.abs(img - BG).sum(-1) > 90
    fg = comp_keep(cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, CROSS) > 0, 500)
    yy, xx = np.mgrid[0:h, 0:w]
    teal = (G - R > 40) & (B - R > 25)
    red = (R > 170) & (R - G > 115) & (B < 95)

    # áo choàng: mảng lam (cả mũ trùm), khăn đỏ ở cổ, khuy vàng, vá lỗ bên trong
    cloak = fg & teal & (yy > 500) & (yy < 1060)
    cloak = comp_keep(cloak, 5000)
    scarf = fg & red & (yy > 495) & (yy < 600) & (xx > 380) & (xx < 640)
    gold = fg & (R > 200) & (G > 110) & (B < 130) & (R - B > 110) & (xx > 440) & (xx < 580) & (yy > 560) & (yy < 670)  # khuy
    cloak = fill_holes(cloak | scarf | gold) & fg
    cloak = cv2.morphologyEx(cloak.astype(np.uint8), cv2.MORPH_CLOSE, CROSS, iterations=2) > 0
    cloak &= fg

    head = fg & ~cloak & (yy < 560)
    head = comp_keep(head, 3000)
    # chỏm tóc (ahoge): đa giác quanh lọn cong; phần chân chỏm (y >= 140) để lại cả trong đầu cho khỏi hở khi chỏm lắc
    poly = np.zeros((h, w), np.uint8)
    cv2.fillPoly(poly, [np.array([[410, 46], [604, 46], [604, 75], [525, 95], [502, 120], [495, 150], [487, 172], [413, 172],
                                  [406, 120]], np.int32)], 1)
    tuft = head & poly.astype(bool)
    head &= ~(tuft & (yy < 140))

    rest = fg & ~cloak & ~head & ~tuft
    k5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    # tay cầm cần: chỉ thấy tay áo và khuỷu hai bên (bàn tay khuất trước người); tay cứng, không có xương riêng
    arm_l = rest & (yy > 570) & (yy < 830) & (xx < 365)
    arm_r = rest & (yy > 570) & (yy < 830) & (xx > 655)
    arm_l = comp_keep(cv2.morphologyEx(arm_l.astype(np.uint8), cv2.MORPH_OPEN, k5) > 0, 1500)
    arm_r = comp_keep(cv2.morphologyEx(arm_r.astype(np.uint8), cv2.MORPH_OPEN, k5) > 0, 1500)
    shorts = rest & (yy >= 960) & (yy < 1104) & ~arm_l & ~arm_r
    legs = rest & (yy >= 1092)
    brown = (R - B > 70) & (R > 120)
    boot_cut = 1186
    boot = legs & (yy >= boot_cut) & brown
    boot = cv2.morphologyEx(boot.astype(np.uint8), cv2.MORPH_CLOSE, CROSS, iterations=2) > 0
    boot = fill_holes(boot) & legs
    # cổ chân phía trên cuff ủng giữ trong ủng nếu nằm dưới vạch cuff
    shin = legs & ~boot
    left = xx < 512
    parts = {
        "toc_chom": tuft,
        "dau": head,
        "ao_choang": cloak,
        "tay_t": arm_l, "tay_p": arm_r,
        "quan": shorts,
        "chan_t": shin & left, "chan_p": shin & ~left,
        "ung_t": boot & left, "ung_p": boot & ~left,
    }
    for k in list(parts):
        parts[k] = comp_keep(parts[k], 300)

    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., :3] = img.astype(np.uint8)
    rgba[..., 3] = 255

    def colour_of(mask):
        c = img[mask]
        return np.median(c, axis=0).astype(np.uint8) if len(c) else np.array([200, 200, 200], np.uint8)

    def texture_fill(dst_mask, src_mask):
        # tô vùng bù bằng mẫu vân của chính mảnh (dịch ô ngẫu nhiên), giữ nét chì
        out = np.zeros((h, w, 3), np.uint8)
        ys, xs = np.nonzero(src_mask)
        if len(ys) == 0:
            return out
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        patch = img[y0:y1 + 1, x0:x1 + 1].astype(np.uint8)
        pm = src_mask[y0:y1 + 1, x0:x1 + 1]
        med = colour_of(src_mask)
        patch[~pm] = med
        ph, pw = patch.shape[:2]
        dys, dxs = np.nonzero(dst_mask)
        out[dys, dxs] = patch[(dys - y0) % ph, (dxs - x0) % pw]
        return out

    pix = {}  # bộ đệm riêng của mảnh có vẽ bù (không ghi vào ảnh chung, kẻo đè mảnh khác)

    def buf(k):
        return pix.setdefault(k, rgba.copy())

    def extend_up(mask, rows, shrink=0.0):
        # kéo mép trên của mảnh lên `rows` px (phần nằm dưới mảnh khác), hơi thu bề ngang thành đầu tròn
        ys, xs = np.nonzero(mask)
        top = ys.min()
        band = mask[top:top + 6].any(0)
        cols = np.nonzero(band)[0]
        if len(cols) == 0:
            return mask
        x0, x1 = cols.min(), cols.max()
        cx, rx = (x0 + x1) / 2, (x1 - x0) / 2
        add = np.zeros_like(mask)
        for i in range(1, rows + 1):
            t = i / rows
            r = rx * (1 - shrink * t * t)
            add[top - i, int(cx - r):int(cx + r) + 1] = True
        return mask | add

    cover_cloak = cv2.erode(parts["ao_choang"].astype(np.uint8), CROSS, iterations=2) > 0
    cover_shorts = cv2.erode(parts["quan"].astype(np.uint8), CROSS, iterations=2) > 0
    # tay: bù phần nằm dưới mép áo choàng (áo lắc thì không lộ mép cắt), vân áo kem của chính tay
    k25 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51))
    for k in ("tay_t", "tay_p"):
        m = parts[k]
        add = (cv2.dilate(m.astype(np.uint8), k25) > 0) & cover_cloak & ~m
        sleeve = m & (img[..., 1] > 215) & (img[..., 2] > 160)
        buf(k)[add, :3] = texture_fill(add, sleeve if sleeve.any() else m)[add]
        parts[k] = m | add
    # quần: kéo lên dưới vạt áo
    m = parts["quan"]
    m2 = extend_up(m, 70, shrink=0.1)
    add = m2 & ~m & cover_cloak
    m2 = m | add
    buf("quan")[add, :3] = texture_fill(add, m)[add]
    parts["quan"] = m2
    # chân: kéo lên dưới quần
    for k in ("chan_t", "chan_p"):
        m = parts[k]
        m2 = extend_up(m, 40, shrink=0.05)
        add = m2 & ~m & cover_shorts
        m2 = m | add
        skin = m & (img[..., 1] > 180) & (img[..., 2] > 120) & (img[..., 0] > 230)
        buf(k)[add, :3] = texture_fill(add, skin if skin.any() else m)[add]
        parts[k] = m2
    # cổ: khúc da dưới tóc (sau tóc, che bởi khăn / áo)
    m = parts["dau"]
    neck = np.zeros_like(m)
    cv2.ellipse(neck.view(np.uint8), (512, 548), (46, 44), 0, 0, 360, 1, -1)
    neck = neck.astype(bool) & ~m & ~cover_cloak  # cổ nằm sau áo choàng: không vẽ đè lên khăn, khuy
    skin = m & (img[..., 0] > 235) & (img[..., 1] > 180) & (img[..., 2] > 120)
    buf("dau")[neck, :3] = texture_fill(neck, skin if skin.any() else m)[neck]
    parts["dau"] = m | neck
    # thân áo kem sau áo choàng
    body = np.zeros((h, w), np.uint8)
    # hẹp hơn áo choàng ở mọi chỗ (người dùng 2026-11-26: mảng kem lòi ra cạnh áo khi áo lắc)
    pts = np.array([[420, 570], [604, 570], [628, 760], [620, 980], [404, 980], [396, 760]], np.int32)
    cv2.fillPoly(body, [pts], 1)
    body = body.astype(bool)
    sleeve = parts["tay_t"] & (img[..., 1] > 215) & (img[..., 2] > 160)
    buf("than")[body, :3] = texture_fill(body, sleeve)[body]
    parts["than"] = body

    geo = {"canvas": [int(w * SCALE), int(h * SCALE)], "origin": [int(512 * SCALE), int(1418 * SCALE)], "parts": {}}
    vis = np.zeros((h, w, 3), np.uint8) + 40
    rng = np.random.default_rng(3)
    for k, m in parts.items():
        ys, xs = np.nonzero(m)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        crop = pix.get(k, rgba)[y0:y1, x0:x1].copy()
        crop[..., 3] = np.where(m[y0:y1, x0:x1], 255, 0)
        # mép mềm 1 px để khỏi răng cưa
        a = crop[..., 3].astype(np.float32)
        a = cv2.GaussianBlur(a, (3, 3), 0.7)
        crop[..., 3] = a.clip(0, 255).astype(np.uint8)
        im = Image.fromarray(crop, "RGBA")
        sw, sh = max(1, round((x1 - x0) * SCALE)), max(1, round((y1 - y0) * SCALE))
        im = im.resize((sw, sh), Image.LANCZOS)
        im.save(os.path.join(OUT, k + ".png"))
        geo["parts"][k] = {"left": round(x0 * SCALE, 1), "top": round(y0 * SCALE, 1), "w": sw, "h": sh}
        vis[m] = rng.integers(60, 255, 3)
        print(f"{k:10s} x {x0}-{x1} y {y0}-{y1}  -> {sw}x{sh}")
    json.dump(geo, open(os.path.join(HERE, "geo.json"), "w"), indent=1)
    Image.fromarray(vis).save(os.path.join(HERE, "xem_manh.png"))


if __name__ == "__main__":
    main()
